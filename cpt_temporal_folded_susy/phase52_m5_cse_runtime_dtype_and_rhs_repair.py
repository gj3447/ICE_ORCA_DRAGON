#!/usr/bin/env python3
"""Phase 52: audit and repair the Phase-51 static evaluator arithmetic.

This runner evaluates six frozen source-by-lambda launch states.  It does not
solve a Gamma--K root or integrate a nonlinear trajectory.  Progress is sent
to stderr and exactly one ``RESULT_JSON=...`` record is sent to stdout.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import math
import platform
import re
import subprocess
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
from mpmath import mp
import numpy as np
import scipy
import sympy as sp
from sympy.printing.numpy import NumPyPrinter


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_INPUTS.json"
)
P51_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase51_m5_gamma_k_local_continuation.py"
)
P51_MANIFEST_PATH = SCRIPT_PATH.with_name(
    "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json"
)
P51_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_RESULT.json"
)

INPUT_COMMIT = "75cce4131cea3a1b69eed4436caaf72ce50b9b11"
INPUT_SHA256 = "5766d8cdaf599428d01eeb785c319ba9418e3c5e56f6275fd9d1229d4f7e0238"
RESULT_SCHEMA = "ice-phase52-m5-cse-runtime-dtype-and-rhs-repair/v1"
RESULT_PREFIX = "RESULT_JSON="
EXPECTED_GENERATED_LEDGER_SHA256 = (
    "ef5c95e3e864b1cfc52828e75f61c31b6b661a5ba725cba57c22e1f0d34eb060"
)
M4 = 7
M5 = 9
TEMPORARY_NAME = re.compile(r"^x[0-9]+$")
LAMBDIFY_DUMMY_NAME = re.compile(r"_Dummy_[0-9]+")


class InvalidRun(RuntimeError):
    """A frozen provenance, exact, runtime, or serialization contract failed."""


def progress(message: str) -> None:
    print(f"[Phase52] {message}", file=sys.stderr, flush=True)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path.name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def parse_unique_json_bytes(path: Path, raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            output[key] = value
        return output

    payload = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(
            InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
        ),
    )
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")
    return payload


def load_unique_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    return parse_unique_json_bytes(path, raw), raw


def canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    output = dict(payload)
    output.pop("result_payload_sha256_without_self", None)
    output["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(output)
    ).hexdigest()
    return output


def verify_self_digest(payload: Mapping[str, Any], *, label: str) -> None:
    key = "result_payload_sha256_without_self"
    if key not in payload:
        key = "checkpoint_payload_sha256_without_self"
    expected = payload.get(key)
    if not isinstance(expected, str):
        raise InvalidRun(f"{label} lacks a self digest")
    stripped = dict(payload)
    stripped.pop(key, None)
    observed = hashlib.sha256(canonical_bytes(stripped)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self digest mismatch")


def finite_float(value: Any, *, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise InvalidRun(f"nonfinite {label}")
    return number


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        array = np.asarray(value)
        if np.iscomplexobj(array):
            flat = array.reshape(-1)
            return {
                "shape": list(array.shape),
                "clongdouble_decimal_pairs": [
                    [ld_text(item.real), ld_text(item.imag)]
                    for item in flat
                ],
            }
        return [json_ready(item) for item in array.tolist()]
    if isinstance(value, np.clongdouble):
        return {
            "clongdouble_decimal_pair": [ld_text(value.real), ld_text(value.imag)]
        }
    if isinstance(value, np.longdouble):
        return {"longdouble_decimal": ld_text(value)}
    if isinstance(value, np.complexfloating):
        if not np.isfinite(value.real) or not np.isfinite(value.imag):
            raise InvalidRun("nonfinite NumPy complex scalar")
        return {
            "real": finite_float(value.real, label="complex real"),
            "imag": finite_float(value.imag, label="complex imag"),
        }
    if isinstance(value, complex):
        number = complex(value)
        return {
            "real": finite_float(number.real, label="complex real"),
            "imag": finite_float(number.imag, label="complex imag"),
        }
    if isinstance(value, mp.mpc):
        if not mp.isfinite(value.real) or not mp.isfinite(value.imag):
            raise InvalidRun("nonfinite mpmath complex scalar")
        return {"mp_decimal_pair": [mp.nstr(value.real, 40), mp.nstr(value.imag, 40)]}
    if isinstance(value, mp.mpf):
        if not mp.isfinite(value):
            raise InvalidRun("nonfinite mpmath real scalar")
        return {"mp_decimal": mp.nstr(value, 40)}
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return finite_float(value, label="float")
    return value


@dataclass
class Contract:
    exact: list[dict[str, Any]]
    numerical: list[dict[str, Any]]

    def __init__(self) -> None:
        self.exact = []
        self.numerical = []

    def add_exact(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "exact",
            "passed": bool(passed),
            "status": "PASS" if passed else "INVALID_RUN",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.exact.append(record)
        if not passed:
            raise InvalidRun(f"{check_id}: {statement}")

    def add_numerical(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
        *,
        failure_status: str = "INCONCLUSIVE",
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "passed": bool(passed),
            "status": "PASS" if passed else failure_status,
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.numerical.append(record)


class LongNumPyPrinter(NumPyPrinter):
    """Emit all value-bearing non-integer constants through clongdouble."""

    def __init__(self) -> None:
        super().__init__({"fully_qualified_modules": False})

    def _print_Float(self, expression: sp.Float) -> str:
        return f"CLD({str(expression)!r})"

    def _print_Rational(self, expression: sp.Rational) -> str:
        decimal = str(sp.N(expression, 80))
        return f"CLD({decimal!r})"

    def _print_Pi(self, _expression: sp.Expr) -> str:
        return f"CLD({str(sp.N(sp.pi, 80))!r})"

    def _print_ImaginaryUnit(self, _expression: sp.Expr) -> str:
        return "CLD('1j')"

    def _print_exp(self, expression: sp.Expr) -> str:
        return f"EXP({self._print(expression.args[0])})"

    def _print_Integer(self, expression: sp.Integer) -> str:
        return f"CLD({str(expression)!r})"

    def _print_Pow(self, expression: sp.Pow) -> str:
        if expression.exp.is_Integer:
            return f"({self._print(expression.base)})**{int(expression.exp)}"
        if expression.exp == sp.Rational(1, 2):
            return f"SQRT({self._print(expression.base)})"
        if expression.exp == sp.Rational(-1, 2):
            return f"CLD('1')/SQRT({self._print(expression.base)})"
        raise InvalidRun(f"unsupported noninteger power in long printer: {expression.exp}")


def cld_literal(value: Any) -> np.clongdouble:
    if not isinstance(value, str):
        raise InvalidRun("CLD accepts decimal string literals only")
    output = np.clongdouble(value)
    if not np.isfinite(output.real) or not np.isfinite(output.imag):
        raise InvalidRun("CLD produced a nonfinite value")
    return output


def cld_sqrt(value: Any) -> np.clongdouble:
    if type(value) is not np.clongdouble:
        raise InvalidRun("SQRT input is not exact np.clongdouble")
    output = np.sqrt(value)
    if type(output) is not np.clongdouble or not np.isfinite(output):
        raise InvalidRun("SQRT output dtype/finite contract failed")
    return output


def cld_exp(value: Any) -> np.clongdouble:
    if type(value) is not np.clongdouble:
        raise InvalidRun("EXP input is not exact np.clongdouble")
    output = np.exp(value)
    if type(output) is not np.clongdouble or not np.isfinite(output):
        raise InvalidRun("EXP output dtype/finite contract failed")
    return output


LONG_MODULES: dict[str, Any] = {
    "CLD": cld_literal,
    "SQRT": cld_sqrt,
    "EXP": cld_exp,
}


@dataclass(frozen=True)
class GeneratedCallable:
    function: Callable[..., Any]
    replacements: tuple[tuple[sp.Symbol, sp.Expr], ...]
    reduced: tuple[sp.Expr, ...]
    outputs: tuple[sp.Expr, ...]
    source_sha256: str
    dag_sha256: str

    @property
    def replacement_count(self) -> int:
        return len(self.replacements)


def make_generated_callable(
    outputs: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
    *,
    long_namespace: bool,
) -> GeneratedCallable:
    ordered = tuple(outputs)
    captured_plan: dict[str, Any] = {}

    def canonical_cse(expressions: Sequence[sp.Expr]) -> tuple[Any, Any]:
        replacements_raw, reduced_raw = sp.cse(expressions, order="canonical")
        if captured_plan:
            raise InvalidRun("lambdify invoked its CSE callback more than once")
        captured_plan["replacements"] = tuple(replacements_raw)
        captured_plan["reduced"] = tuple(reduced_raw)
        return replacements_raw, reduced_raw

    function = sp.lambdify(
        (tuple(variables),),
        ordered,
        modules=LONG_MODULES if long_namespace else "numpy",
        cse=canonical_cse,
        printer=LongNumPyPrinter() if long_namespace else None,
    )
    if set(captured_plan) != {"replacements", "reduced"}:
        raise InvalidRun("lambdify did not expose its exact CSE plan")
    replacements = captured_plan["replacements"]
    reduced = captured_plan["reduced"]
    source = inspect.getsource(function)
    if long_namespace and ("numpy." in source or "np." in source):
        raise InvalidRun("long callable source contains a silent NumPy namespace fallback")
    if long_namespace and not set(function.__code__.co_names).issubset(LONG_MODULES):
        raise InvalidRun(
            "long callable used undeclared globals: "
            f"{sorted(set(function.__code__.co_names) - set(LONG_MODULES))}"
        )
    dag = sp.srepr(sp.Tuple(*[sp.Tuple(symbol, expression) for symbol, expression in replacements]))
    dag += sp.srepr(sp.Tuple(*reduced))
    return GeneratedCallable(
        function=function,
        replacements=replacements,
        reduced=reduced,
        outputs=ordered,
        source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        dag_sha256=hashlib.sha256(dag.encode("utf-8")).hexdigest(),
    )


def prohibited_reference_callable(*_arguments: Any) -> Any:
    raise InvalidRun("the direct SymPy CSE reference plan is not executable code")


def make_direct_symbolic_cse_plan(
    outputs: Sequence[sp.Expr],
) -> GeneratedCallable:
    """Construct a canonical CSE plan without lambdify or native execution."""
    ordered = tuple(outputs)
    replacements_raw, reduced_raw = sp.cse(ordered, order="canonical")
    replacements = tuple(replacements_raw)
    reduced = tuple(reduced_raw)
    dag_payload = {
        "replacements": [
            [str(symbol), sp.srepr(expression)]
            for symbol, expression in replacements
        ],
        "reduced": [sp.srepr(expression) for expression in reduced],
    }
    dag_bytes = canonical_bytes(dag_payload)
    return GeneratedCallable(
        function=prohibited_reference_callable,
        replacements=replacements,
        reduced=reduced,
        outputs=ordered,
        source_sha256=hashlib.sha256(
            b"direct-sympy-cse-plan-no-lambdify\0" + dag_bytes
        ).hexdigest(),
        dag_sha256=hashlib.sha256(dag_bytes).hexdigest(),
    )


def exact_back_substitution(callable_set: GeneratedCallable) -> bool:
    reconstructed = list(callable_set.reduced)
    for symbol, replacement in reversed(callable_set.replacements):
        reconstructed = [item.xreplace({symbol: replacement}) for item in reconstructed]
    return all(
        rebuilt == original or sp.expand(rebuilt - original) == 0
        for rebuilt, original in zip(reconstructed, callable_set.outputs)
    )


def flatten_raw(value: Any) -> list[Any]:
    if isinstance(value, np.ndarray):
        return list(value.reshape(-1))
    if isinstance(value, (list, tuple)):
        output: list[Any] = []
        for item in value:
            output.extend(flatten_raw(item))
        return output
    return [value]


def scalar_dtype(value: Any) -> str:
    if isinstance(value, np.generic):
        return str(value.dtype)
    if isinstance(value, float):
        return "python_float64"
    if isinstance(value, complex):
        return "python_complex128"
    if isinstance(value, int):
        return "python_int"
    array = np.asarray(value)
    return str(array.dtype)


def traced_call(
    callable_set: GeneratedCallable, values: Sequence[Any]
) -> tuple[np.ndarray, dict[str, Any]]:
    captured: dict[str, Any] = {}
    captured_return: list[Any] = []
    target_code = callable_set.function.__code__
    previous = sys.gettrace()
    if previous is not None:
        raise InvalidRun("preexisting Python trace hook makes the dtype audit ambiguous")

    def tracer(frame: Any, event: str, argument: Any) -> Any:
        if frame.f_code is target_code:
            if event == "return":
                captured.update(frame.f_locals)
                captured_return.append(argument)
            return tracer
        return tracer if event == "call" and frame.f_code is target_code else None

    try:
        sys.settrace(tracer)
        raw = callable_set.function(tuple(values))
    finally:
        sys.settrace(previous)
    if type(raw) not in (list, tuple):
        raise InvalidRun(
            "generated callable raw output container drifted before coercion: "
            f"{type(raw).__module__}.{type(raw).__qualname__}"
        )
    temporaries = {
        name: value for name, value in captured.items() if TEMPORARY_NAME.fullmatch(name)
    }
    expected_names = {str(symbol) for symbol, _expression in callable_set.replacements}
    if set(temporaries) != expected_names:
        raise InvalidRun(
            "CSE trace replacement-name mismatch: "
            f"observed={sorted(temporaries)} expected={sorted(expected_names)}"
        )
    if len(captured_return) != 1 or captured_return[0] is not raw:
        raise InvalidRun("trace return object identity/completeness failure")
    temp_counts: dict[str, int] = {}
    for value in temporaries.values():
        array = np.asarray(value)
        if not np.all(np.isfinite(array)):
            raise InvalidRun("nonfinite traced CSE temporary")
        dtype = scalar_dtype(value)
        temp_counts[dtype] = temp_counts.get(dtype, 0) + 1
    raw_values = flatten_raw(raw)
    raw_counts: dict[str, int] = {}
    for value in raw_values:
        array = np.asarray(value)
        if not np.all(np.isfinite(array)):
            raise InvalidRun("nonfinite raw generated-callable output")
        dtype = scalar_dtype(value)
        raw_counts[dtype] = raw_counts.get(dtype, 0) + 1
    return np.asarray(raw_values, dtype=np.clongdouble), {
        "replacement_count": callable_set.replacement_count,
        "traced_temporary_count": len(temporaries),
        "temporary_dtype_counts": temp_counts,
        "raw_output_count": len(raw_values),
        "raw_output_container_type": type(raw).__name__,
        "raw_output_dtype_counts": raw_counts,
        "all_temporary_scalars_exact_clongdouble": all(
            type(value) is np.clongdouble for value in temporaries.values()
        ),
        "all_raw_scalars_exact_clongdouble": all(
            type(value) is np.clongdouble for value in raw_values
        ),
        "replacement_names_exact": True,
        "return_object_identity_exact": True,
        "source_sha256": callable_set.source_sha256,
        "dag_sha256": callable_set.dag_sha256,
    }


def ld_text(value: Any) -> str:
    number = np.longdouble(value)
    if not np.isfinite(number):
        raise InvalidRun("cannot lift a nonfinite longdouble")
    text = np.format_float_scientific(
        number, precision=24, unique=False, trim="k"
    )
    if np.longdouble(text) != number:
        raise InvalidRun("longdouble decimal round-trip failed")
    if number == 0 and np.signbit(np.longdouble(text)) != np.signbit(number):
        raise InvalidRun("longdouble signed-zero round-trip failed")
    return text


def mp_real(value: Any) -> mp.mpf:
    return mp.mpf(ld_text(value))


def mp_complex(value: Any) -> mp.mpc:
    number = np.clongdouble(value)
    return mp.mpc(mp_real(number.real), mp_real(number.imag))


def mp_vector(value: Any) -> list[mp.mpc]:
    array = np.asarray(value, dtype=np.clongdouble).reshape(-1)
    return [mp_complex(item) for item in array]


def mp_frozen_state_vector(value: Any) -> list[mp.mpc]:
    array = np.asarray(value)
    if array.dtype != np.dtype(np.clongdouble):
        raise InvalidRun("frozen reference state is not exact clongdouble")
    return [mp_complex(item) for item in array.reshape(-1)]


def mp_matrix_real(value: Any) -> mp.matrix:
    array = np.asarray(value, dtype=np.longdouble)
    return mp.matrix(
        [
            [mp_real(array[row, column]) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def mp_norm(value: Sequence[Any]) -> mp.mpf:
    return mp.sqrt(mp.fsum(abs(item) ** 2 for item in value))


def mp_relative(left: Sequence[Any], right: Sequence[Any]) -> mp.mpf:
    if len(left) != len(right):
        raise InvalidRun("mp relative vector length mismatch")
    difference = mp_norm([left[index] - right[index] for index in range(len(left))])
    return difference / max(mp_norm(left), mp_norm(right), mp.mpf("1e-100"))


def native_relative(left: Any, right: Any) -> float:
    left_array = np.asarray(left, dtype=np.clongdouble).reshape(-1)
    right_array = np.asarray(right, dtype=np.clongdouble).reshape(-1)
    numerator = np.linalg.norm(left_array - right_array)
    denominator = max(
        np.linalg.norm(left_array), np.linalg.norm(right_array), np.longdouble("1e-100")
    )
    return float(numerator / denominator)


def mp_vector_record(value: Sequence[Any], digits: int = 60) -> dict[str, Any]:
    pairs: list[list[str]] = []
    for item in value:
        real = mp.re(item)
        imaginary = mp.im(item)
        if not mp.isfinite(real) or not mp.isfinite(imaginary):
            raise InvalidRun("cannot serialize a nonfinite mpmath vector value")
        pairs.append(
            [mp.nstr(real, digits), mp.nstr(imaginary, digits)]
        )
    return {
        "shape": [len(value)],
        "mp_decimal_pairs": pairs,
    }


def require(mapping: Mapping[str, Any], key: str, *, where: str) -> Any:
    if key not in mapping:
        raise InvalidRun(f"missing {where}.{key}")
    return mapping[key]


def git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def committed_blob_guard(relative: str, commit: str) -> dict[str, Any]:
    working_blob = git_output("hash-object", "--", relative)
    committed_blob = git_output("rev-parse", f"{commit}:{relative}")
    if working_blob != committed_blob:
        raise InvalidRun(
            f"declared commit does not contain the pinned working bytes: {relative}"
        )
    return {
        "working_blob_oid": working_blob,
        "committed_blob_oid": committed_blob,
        "commit_blob_matches": True,
    }


def runtime_record() -> dict[str, Any]:
    return {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "sympy_version": sp.__version__,
        "mpmath_version": mpmath.__version__,
        "longdouble_itemsize_bytes": int(np.dtype(np.longdouble).itemsize),
        "clongdouble_itemsize_bytes": int(np.dtype(np.clongdouble).itemsize),
        "longdouble_mantissa_bits_excluding_implicit": int(
            np.finfo(np.longdouble).nmant
        ),
        "longdouble_epsilon": str(np.finfo(np.longdouble).eps),
        "platform": platform.platform(),
    }


def validate_inputs(
    manifest: Mapping[str, Any], manifest_raw: bytes, *, authoritative: bool
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if hashlib.sha256(manifest_raw).hexdigest() != INPUT_SHA256:
        raise InvalidRun("Phase52 manifest SHA drift")
    if manifest.get("schema") != (
        "ice-phase52-m5-cse-runtime-dtype-and-rhs-repair-inputs/v1"
    ) or manifest.get("phase") != 52:
        raise InvalidRun("Phase52 manifest schema/phase drift")
    checks = require(manifest, "checks", where="manifest")
    outputs = require(manifest, "required_outputs", where="manifest")
    if (
        len(require(checks, "exact", where="checks")) != 7
        or len(require(checks, "numerical", where="checks")) != 7
        or outputs.get("exact_check_count") != 7
        or outputs.get("numerical_check_count") != 7
    ):
        raise InvalidRun("Phase52 declared check counts drifted")

    observed_runtime = runtime_record()
    expected_runtime = require(manifest, "runtime_contract", where="manifest")
    runtime_keys = (
        "python_implementation",
        "python_version",
        "numpy_version",
        "scipy_version",
        "sympy_version",
        "mpmath_version",
        "longdouble_itemsize_bytes",
        "clongdouble_itemsize_bytes",
        "longdouble_mantissa_bits_excluding_implicit",
        "longdouble_epsilon",
    )
    for key in runtime_keys:
        if str(observed_runtime[key]) != str(require(expected_runtime, key, where="runtime_contract")):
            raise InvalidRun(
                f"runtime contract drift for {key}: "
                f"{observed_runtime[key]} != {expected_runtime[key]}"
            )

    observed: dict[str, Any] = {}
    loaded: dict[str, dict[str, Any]] = {}
    pinned = require(manifest, "pinned_inputs", where="manifest")
    for label, specification_raw in pinned.items():
        if not isinstance(specification_raw, Mapping):
            raise InvalidRun(f"invalid pinned input record: {label}")
        specification = specification_raw
        relative = str(require(specification, "path", where=f"pinned_inputs.{label}"))
        path = REPO_ROOT / relative
        pinned_raw = path.read_bytes()
        digest = hashlib.sha256(pinned_raw).hexdigest()
        expected = str(require(specification, "sha256", where=f"pinned_inputs.{label}"))
        if digest != expected:
            raise InvalidRun(f"pinned input SHA drift: {label}")
        size = len(pinned_raw)
        if "size_bytes" in specification and size != int(specification["size_bytes"]):
            raise InvalidRun(f"pinned input size drift: {label}")
        if path.suffix == ".json":
            payload = parse_unique_json_bytes(path, pinned_raw)
            loaded[label] = payload
            if "result_payload_sha256_without_self" in specification:
                verify_self_digest(payload, label=label)
                if payload.get("result_payload_sha256_without_self") != specification.get(
                    "result_payload_sha256_without_self"
                ):
                    raise InvalidRun(f"pinned result self digest drift: {label}")
        commit = str(require(specification, "commit", where=f"pinned_inputs.{label}"))
        observed[label] = {
            "path": relative,
            "commit": commit,
            "sha256": digest,
            "size_bytes": size,
            "role": specification.get("role"),
            **committed_blob_guard(relative, commit),
        }

    p51_manifest = loaded.get("phase51_manifest")
    p51_result = loaded.get("phase51_result")
    if p51_manifest is None or p51_result is None:
        raise InvalidRun("Phase51 pinned JSON inputs were not loaded")
    p51_spec = pinned["phase51_result"]
    if (
        p51_result.get("run_status") != p51_spec.get("run_status")
        or p51_result.get("classification") != p51_spec.get("classification")
    ):
        raise InvalidRun("Phase51 historical status/classification drift")

    p51_pinned = require(p51_manifest, "pinned_inputs", where="Phase51 manifest")
    for nested_label, specification_raw in p51_pinned.items():
        if not isinstance(specification_raw, Mapping):
            raise InvalidRun(f"invalid Phase51 transitive pin: {nested_label}")
        specification = specification_raw
        where = f"Phase51 pinned_inputs.{nested_label}"
        relative = str(require(specification, "path", where=where))
        commit = str(require(specification, "commit", where=where))
        path = REPO_ROOT / relative
        pinned_raw = path.read_bytes()
        digest = hashlib.sha256(pinned_raw).hexdigest()
        expected = str(require(specification, "sha256", where=where))
        if digest != expected:
            raise InvalidRun(f"Phase51 transitive input SHA drift: {nested_label}")
        size = len(pinned_raw)
        if "size_bytes" in specification and size != int(specification["size_bytes"]):
            raise InvalidRun(f"Phase51 transitive input size drift: {nested_label}")
        observed[f"phase51_transitive::{nested_label}"] = {
            "path": relative,
            "commit": commit,
            "sha256": digest,
            "size_bytes": size,
            "role": "Phase51 transitive pin",
            **committed_blob_guard(relative, commit),
        }

    runner_guard = {
        "runner_sha256_at_start": sha256_path(SCRIPT_PATH),
        "authoritative": authoritative,
        "runner_commit": None,
        "runner_clean": None,
        "manifest_is_ancestor": None,
        "manifest_commit_blob_guard": committed_blob_guard(
            str(INPUT_PATH.relative_to(REPO_ROOT)), INPUT_COMMIT
        ),
    }
    if authoritative:
        relative_runner = str(SCRIPT_PATH.relative_to(REPO_ROOT))
        dirty = git_output("status", "--porcelain=v1", "--", relative_runner)
        commit = git_output("log", "-1", "--format=%H", "--", relative_runner)
        if not commit or dirty:
            raise InvalidRun("authoritative Phase52 runner must be committed and clean")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", INPUT_COMMIT, commit],
            cwd=REPO_ROOT,
            check=False,
        ).returncode == 0
        if not ancestor or commit == INPUT_COMMIT:
            raise InvalidRun("Phase52 runner commit does not postdate its manifest")
        runner_guard.update(
            {
                "runner_commit": commit,
                "runner_clean": True,
                "manifest_is_ancestor": True,
                "runner_commit_blob_guard": committed_blob_guard(
                    relative_runner, commit
                ),
            }
        )
    return observed, p51_manifest, p51_result, runner_guard


@dataclass(frozen=True)
class Slot:
    source: Any
    node: Any
    source_label: str
    lambda_value: float
    state_w5: np.ndarray
    state_w4: np.ndarray

    @property
    def key(self) -> str:
        return f"{self.source_label}:lambda={self.lambda_value:.1f}"


def build_phase51_contexts(
    p51: ModuleType, p51_manifest: Mapping[str, Any]
) -> tuple[list[Any], dict[str, Any]]:
    p51_audit = p51.Audit()
    _observed, checkpoint, _phase49, phase50_result = p51.validate_inputs(
        p51_manifest, p51_audit
    )
    phase50 = load_module("ice_phase50_for_phase52", p51.PHASE50_SOURCE_PATH)
    numerics = p51.parse_numerics(p51_manifest)
    thresholds = p51.parse_thresholds(p51_manifest)
    bounds = p51.parse_bounds(p51_manifest)
    contexts = [
        p51.source_context(
            label,
            p51_manifest,
            checkpoint,
            phase50_result,
            phase50,
            numerics,
            thresholds,
            bounds,
        )
        for label in ("phi_plus", "phi_minus")
    ]
    return contexts, {
        "phase51_internal_exact_checks": p51_audit.exact,
        "phase51_source_context_order": [item.label for item in contexts],
    }


def build_slots(
    contexts: Sequence[Any], source_order: Sequence[str], lambda_order: Sequence[float]
) -> list[Slot]:
    by_label = {context.label: context for context in contexts}
    slots: list[Slot] = []
    for label in source_order:
        source = by_label[label]
        for lambda_value_raw in lambda_order:
            lambda_value = float(lambda_value_raw)
            node = source.node(lambda_value)
            state_w5 = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.clongdouble(
                node.sphere_radius
            ) * (
                np.asarray(node.launch_w, dtype=np.clongdouble)
                @ np.asarray(source.chart.center, dtype=np.longdouble)
            )
            coordinates = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble) @ (
                state_w5 - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
            )
            state_w4 = np.asarray(source.evaluator.anchor4, dtype=np.clongdouble) + coordinates[:M4]
            slots.append(
                Slot(
                    source=source,
                    node=node,
                    source_label=label,
                    lambda_value=lambda_value,
                    state_w5=state_w5,
                    state_w4=state_w4,
                )
            )
    return slots


def semantic_numeric_differences(
    current: Any, historical: Any, *, path: str
) -> list[dict[str, Any]]:
    if isinstance(current, Mapping) and isinstance(historical, Mapping):
        if set(current) != set(historical):
            raise InvalidRun(f"Phase51 semantic key drift at {path}")
        output: list[dict[str, Any]] = []
        for key in sorted(current):
            output.extend(
                semantic_numeric_differences(
                    current[key], historical[key], path=f"{path}.{key}"
                )
            )
        return output
    if isinstance(current, (list, tuple)) and isinstance(historical, (list, tuple)):
        if len(current) != len(historical):
            raise InvalidRun(f"Phase51 semantic sequence-length drift at {path}")
        output = []
        for index, (left, right) in enumerate(zip(current, historical)):
            output.extend(
                semantic_numeric_differences(
                    left, right, path=f"{path}[{index}]"
                )
            )
        return output
    numeric = (int, float, np.integer, np.floating)
    if (
        isinstance(current, numeric)
        and not isinstance(current, (bool, np.bool_))
        and isinstance(historical, numeric)
        and not isinstance(historical, (bool, np.bool_))
    ):
        left = finite_float(current, label=f"current {path}")
        right = finite_float(historical, label=f"historical {path}")
        return [{"path": path, "absolute_difference": abs(left - right)}]
    if type(current) is not type(historical) or current != historical:
        raise InvalidRun(f"Phase51 semantic nonnumeric drift at {path}")
    return []


def reproduce_phase51_records(
    p51: ModuleType,
    contexts: Sequence[Any],
    p51_result: Mapping[str, Any],
    lambdas: Sequence[float],
) -> dict[str, Any]:
    historical_all = p51_result["evaluator_validation"]["same_point_source_lambda_pairs"]
    records: dict[str, Any] = {}
    maximum = 0.0
    structural = True
    for source in contexts:
        current = p51.cse_validation(source, lambdas)
        historical = historical_all[source.label]
        difference_records = semantic_numeric_differences(
            current, historical, path=source.label
        )
        differences = [record["absolute_difference"] for record in difference_records]
        maximum = max(maximum, max(differences, default=0.0))
        structural = bool(
            structural
            and [record.get("point") for record in current["records"]]
            == [record.get("point") for record in historical["records"]]
            and [record.get("cse_dtypes") for record in current["records"]]
            == [record.get("cse_dtypes") for record in historical["records"]]
        )
        records[source.label] = {
            "recomputed": current,
            "historical": historical,
            "maximum_absolute_numeric_difference": max(differences, default=0.0),
            "numeric_leaf_differences": difference_records,
        }
    return {
        "records": records,
        "maximum_absolute_numeric_difference": maximum,
        "structural_fields_match": structural,
    }


def make_plain_callable(
    outputs: Sequence[sp.Expr], variables: Sequence[sp.Symbol]
) -> GeneratedCallable:
    ordered = tuple(outputs)
    function = sp.lambdify((tuple(variables),), ordered, modules="numpy", cse=False)
    source = inspect.getsource(function)
    dag = sp.srepr(sp.Tuple(*ordered))
    return GeneratedCallable(
        function=function,
        replacements=(),
        reduced=ordered,
        outputs=ordered,
        source_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        dag_sha256=hashlib.sha256(dag.encode("utf-8")).hexdigest(),
    )


def normalized_lambdify_source(function: Callable[..., Any]) -> str:
    return LAMBDIFY_DUMMY_NAME.sub("_Dummy_N", inspect.getsource(function))


def bind_phase51_callable(
    reconstructed: GeneratedCallable,
    phase51_function: Callable[..., Any],
    *,
    label: str,
) -> tuple[GeneratedCallable, dict[str, Any]]:
    """Bind the plan to the actual pinned Phase-51 production callable."""
    reconstructed_normalized = normalized_lambdify_source(
        reconstructed.function
    )
    phase51_source = inspect.getsource(phase51_function)
    phase51_normalized = LAMBDIFY_DUMMY_NAME.sub("_Dummy_N", phase51_source)
    alpha_equivalent = phase51_normalized == reconstructed_normalized
    expected_names = {
        str(symbol) for symbol, _expression in reconstructed.replacements
    }
    actual_names = set(phase51_function.__code__.co_varnames)
    replacement_locals_present = expected_names.issubset(actual_names)
    if not alpha_equivalent or not replacement_locals_present:
        raise InvalidRun(
            f"Phase51 production callable drift at {label}: "
            f"alpha_equivalent={alpha_equivalent}, "
            f"replacement_locals_present={replacement_locals_present}"
        )
    bound = GeneratedCallable(
        function=phase51_function,
        replacements=reconstructed.replacements,
        reduced=reconstructed.reduced,
        outputs=reconstructed.outputs,
        source_sha256=hashlib.sha256(phase51_source.encode("utf-8")).hexdigest(),
        dag_sha256=reconstructed.dag_sha256,
    )
    return bound, {
        "actual_pinned_phase51_callable_used": True,
        "alpha_normalized_source_equal": alpha_equivalent,
        "replacement_locals_present": replacement_locals_present,
        "reconstructed_raw_source_sha256": reconstructed.source_sha256,
        "phase51_raw_source_sha256": bound.source_sha256,
        "normalized_source_sha256": hashlib.sha256(
            phase51_normalized.encode("utf-8")
        ).hexdigest(),
    }


@dataclass(frozen=True)
class DimensionEvaluators:
    dimension: int
    variables: tuple[sp.Symbol, ...]
    global_gradient: tuple[sp.Expr, ...]
    baseline_joint: GeneratedCallable
    baseline_plain: GeneratedCallable
    long_joint: GeneratedCallable
    reference_gradient_cse: GeneratedCallable
    element_gradients: tuple[tuple[sp.Expr, ...], ...]
    element_long: tuple[GeneratedCallable, ...]
    element_identity: bool
    executable_float_identity_diagnostic: Mapping[str, Any]
    phase51_callable_binding: Mapping[str, Any]


@dataclass(frozen=True)
class SourceEvaluators:
    source_label: str
    m4: DimensionEvaluators
    m5: DimensionEvaluators


def element_gradients_m4(
    phase41: ModuleType, delta_a: float, delta_phi: float
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    tuple[sp.Expr, ...],
]:
    family = phase41.build_symbolic_family()
    float_substitutions: dict[sp.Symbol, sp.Expr] = {
        family.boundary_a: sp.Float(str(phase41.BASE_A), 50),
        family.boundary_phi: sp.Float(str(phase41.BASE_PHI), 50),
        family.delta_a: sp.Float(str(delta_a), 50),
        family.delta_phi: sp.Float(str(delta_phi), 50),
    }
    exact_substitutions: dict[sp.Symbol, sp.Expr] = {
        family.boundary_a: sp.Rational(str(phase41.BASE_A)),
        family.boundary_phi: sp.Rational(str(phase41.BASE_PHI)),
        family.delta_a: sp.Rational(str(delta_a)),
        family.delta_phi: sp.Rational(str(delta_phi)),
    }
    for index, variable in enumerate(family.variables_z):
        float_substitutions[variable] = (
            sp.Float(str(phase41.COORDINATE_SCALES[index]), 50)
            * family.variables_w[index]
        )
        exact_substitutions[variable] = (
            sp.Rational(str(phase41.COORDINATE_SCALES[index]))
            * family.variables_w[index]
        )
    float_elements = tuple(
        element.subs(float_substitutions) for element in family.elements
    )
    exact_elements = tuple(
        element.subs(exact_substitutions) for element in family.elements
    )

    def gradients(elements: Sequence[sp.Expr]) -> tuple[tuple[sp.Expr, ...], ...]:
        return tuple(
            tuple(sp.diff(element, variable) for variable in family.variables_w)
            for element in elements
        )

    float_gradients = gradients(float_elements)
    exact_gradients = gradients(exact_elements)
    exact_expanded = sp.expand(family.action_z).subs(exact_substitutions)
    identity_gradient = tuple(
        sp.diff(exact_expanded, variable) for variable in family.variables_w
    )
    return float_gradients, exact_gradients, identity_gradient


def element_gradients_m5(
    phase41: ModuleType,
    phase50: ModuleType,
    delta_a: float,
    delta_phi: float,
) -> tuple[
    tuple[tuple[sp.Expr, ...], ...],
    tuple[tuple[sp.Expr, ...], ...],
    tuple[sp.Expr, ...],
]:
    family = phase50.build_m5_symbolic_family()
    scales = phase50.coordinate_scales(phase41, 5)
    float_substitutions: dict[sp.Symbol, sp.Expr] = {
        family.boundary_a: sp.Float(str(phase41.BASE_A), 50),
        family.boundary_phi: sp.Float(str(phase41.BASE_PHI), 50),
        family.delta_a: sp.Float(str(delta_a), 50),
        family.delta_phi: sp.Float(str(delta_phi), 50),
    }
    exact_substitutions: dict[sp.Symbol, sp.Expr] = {
        family.boundary_a: sp.Rational(str(phase41.BASE_A)),
        family.boundary_phi: sp.Rational(str(phase41.BASE_PHI)),
        family.delta_a: sp.Rational(str(delta_a)),
        family.delta_phi: sp.Rational(str(delta_phi)),
    }
    for index, variable in enumerate(family.variables_z):
        float_substitutions[variable] = (
            sp.Float(str(scales[index]), 50) * family.variables_w[index]
        )
        exact_substitutions[variable] = (
            sp.Rational(str(scales[index])) * family.variables_w[index]
        )
    float_elements = tuple(
        element.subs(float_substitutions) for element in family.elements
    )
    exact_elements = tuple(
        element.subs(exact_substitutions) for element in family.elements
    )

    def gradients(elements: Sequence[sp.Expr]) -> tuple[tuple[sp.Expr, ...], ...]:
        return tuple(
            tuple(sp.diff(element, variable) for variable in family.variables_w)
            for element in elements
        )
    float_gradients = gradients(float_elements)
    exact_gradients = gradients(exact_elements)
    exact_expanded = sp.expand(family.action_z).subs(exact_substitutions)
    identity_gradient = tuple(
        sp.diff(exact_expanded, variable) for variable in family.variables_w
    )
    return float_gradients, exact_gradients, identity_gradient


def build_dimension_evaluators(
    gradient: Sequence[sp.Expr],
    hessian: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
    element_gradients: Sequence[Sequence[sp.Expr]],
    identity_element_gradients: Sequence[Sequence[sp.Expr]],
    identity_gradient: Sequence[sp.Expr],
    phase51_joint_cse: Callable[..., Any],
    phase51_joint_plain: Callable[..., Any],
    binding_label: str,
) -> DimensionEvaluators:
    gradient_tuple = tuple(gradient)
    joint = tuple([*gradient_tuple, *tuple(hessian)])
    reconstructed_joint = make_generated_callable(
        joint, variables, long_namespace=False
    )
    long_joint = make_generated_callable(joint, variables, long_namespace=True)
    reconstructed_plain = make_plain_callable(joint, variables)
    baseline_joint, joint_binding = bind_phase51_callable(
        reconstructed_joint,
        phase51_joint_cse,
        label=f"{binding_label}:joint_CSE",
    )
    baseline_plain, plain_binding = bind_phase51_callable(
        reconstructed_plain,
        phase51_joint_plain,
        label=f"{binding_label}:nonCSE",
    )
    reference_gradient_cse = make_direct_symbolic_cse_plan(gradient_tuple)
    element_tuple = tuple(tuple(items) for items in element_gradients)
    element_long = tuple(
        make_generated_callable(items, variables, long_namespace=True)
        for items in element_tuple
    )
    identity_elements = tuple(tuple(items) for items in identity_element_gradients)
    identity = all(
        sp.expand(
            sum(elements[index] for elements in identity_elements)
            - identity_gradient[index]
        )
        == 0
        for index in range(len(gradient_tuple))
    )
    float_residuals = [
        sp.expand(
            sum(elements[index] for elements in element_tuple)
            - gradient_tuple[index]
        )
        for index in range(len(gradient_tuple))
    ]
    probe = {
        variable: sp.Rational(index + 1, 10)
        for index, variable in enumerate(variables)
    }
    probe_absolute = [
        float(abs(complex(sp.N(residual.subs(probe), 30))))
        for residual in float_residuals
    ]
    return DimensionEvaluators(
        dimension=len(gradient_tuple),
        variables=tuple(variables),
        global_gradient=gradient_tuple,
        baseline_joint=baseline_joint,
        baseline_plain=baseline_plain,
        long_joint=long_joint,
        reference_gradient_cse=reference_gradient_cse,
        element_gradients=element_tuple,
        element_long=element_long,
        element_identity=identity,
        executable_float_identity_diagnostic={
            "exact_zero_by_component": [residual == 0 for residual in float_residuals],
            "symbolic_residual_srepr_sha256": [
                hashlib.sha256(sp.srepr(residual).encode("utf-8")).hexdigest()
                for residual in float_residuals
            ],
            "deterministic_probe_absolute_by_component": probe_absolute,
            "maximum_deterministic_probe_absolute": max(probe_absolute, default=0.0),
            "interpretation": "50-digit SymPy Float expansion-order residual; retained diagnostic, not the exact-decimal identity ledger",
        },
        phase51_callable_binding={
            "joint_CSE": joint_binding,
            "nonCSE": plain_binding,
        },
    )


def build_symbolic_evaluators(
    p51: ModuleType, contexts: Sequence[Any]
) -> tuple[dict[str, SourceEvaluators], dict[str, Any]]:
    phase41 = load_module("ice_phase41_for_phase52", p51.PHASE41_SOURCE_PATH)
    phase50 = load_module("ice_phase50_symbolic_for_phase52", p51.PHASE50_SOURCE_PATH)
    family4 = phase41.build_symbolic_family()
    family5 = phase50.build_m5_symbolic_family()
    output: dict[str, SourceEvaluators] = {}
    ledger: dict[str, Any] = {}
    for source in contexts:
        model4 = phase41.numeric_model(source.delta_a, source.delta_phi)
        model5 = phase50.m5_numeric_model(source.delta_a, source.delta_phi)
        elements4, exact_elements4, identity4 = element_gradients_m4(
            phase41, source.delta_a, source.delta_phi
        )
        elements5, exact_elements5, identity5 = element_gradients_m5(
            phase41, phase50, source.delta_a, source.delta_phi
        )
        m4 = build_dimension_evaluators(
            tuple(model4.gradient_expr),
            tuple(model4.hessian_expr),
            family4.variables_w,
            elements4,
            exact_elements4,
            identity4,
            source.evaluator.m4.joint_cse,
            source.evaluator.m4.joint_plain,
            f"{source.label}:m4",
        )
        m5 = build_dimension_evaluators(
            tuple(model5.gradient_expr),
            tuple(model5.hessian_expr),
            family5.variables_w,
            elements5,
            exact_elements5,
            identity5,
            source.evaluator.m5.joint_cse,
            source.evaluator.m5.joint_plain,
            f"{source.label}:m5",
        )
        output[source.label] = SourceEvaluators(source.label, m4, m5)
        ledger[source.label] = {
            "element_identity": {
                "reference": "separate exact-decimal Rational source family",
                "m4": m4.element_identity,
                "m5": m5.element_identity,
            },
            "executable_Float_identity_rounding_diagnostic": {
                "m4": m4.executable_float_identity_diagnostic,
                "m5": m5.executable_float_identity_diagnostic,
            },
            "phase51_production_callable_binding": {
                "m4": m4.phase51_callable_binding,
                "m5": m5.phase51_callable_binding,
            },
            "joint": {
                "m4": {
                    "replacement_count": m4.baseline_joint.replacement_count,
                    "dag_sha256": m4.baseline_joint.dag_sha256,
                    "baseline_source_sha256": m4.baseline_joint.source_sha256,
                    "baseline_plain_source_sha256": m4.baseline_plain.source_sha256,
                    "baseline_plain_dag_sha256": m4.baseline_plain.dag_sha256,
                    "long_source_sha256": m4.long_joint.source_sha256,
                    "back_substitution": exact_back_substitution(m4.baseline_joint),
                    "long_same_DAG": m4.long_joint.dag_sha256
                    == m4.baseline_joint.dag_sha256,
                },
                "m5": {
                    "replacement_count": m5.baseline_joint.replacement_count,
                    "dag_sha256": m5.baseline_joint.dag_sha256,
                    "baseline_source_sha256": m5.baseline_joint.source_sha256,
                    "baseline_plain_source_sha256": m5.baseline_plain.source_sha256,
                    "baseline_plain_dag_sha256": m5.baseline_plain.dag_sha256,
                    "long_source_sha256": m5.long_joint.source_sha256,
                    "back_substitution": exact_back_substitution(m5.baseline_joint),
                    "long_same_DAG": m5.long_joint.dag_sha256
                    == m5.baseline_joint.dag_sha256,
                },
            },
            "reference_gradient": {
                "m4": {
                    "construction": "direct_sp.cse_without_lambdify",
                    "replacement_count": m4.reference_gradient_cse.replacement_count,
                    "dag_sha256": m4.reference_gradient_cse.dag_sha256,
                    "source_sha256": m4.reference_gradient_cse.source_sha256,
                    "back_substitution": exact_back_substitution(m4.reference_gradient_cse),
                },
                "m5": {
                    "construction": "direct_sp.cse_without_lambdify",
                    "replacement_count": m5.reference_gradient_cse.replacement_count,
                    "dag_sha256": m5.reference_gradient_cse.dag_sha256,
                    "source_sha256": m5.reference_gradient_cse.source_sha256,
                    "back_substitution": exact_back_substitution(m5.reference_gradient_cse),
                },
            },
            "elements": {
                "m4": [
                    {
                        "index": index,
                        "replacement_count": item.replacement_count,
                        "dag_sha256": item.dag_sha256,
                        "source_sha256": item.source_sha256,
                        "back_substitution": exact_back_substitution(item),
                    }
                    for index, item in enumerate(m4.element_long)
                ],
                "m5": [
                    {
                        "index": index,
                        "replacement_count": item.replacement_count,
                        "dag_sha256": item.dag_sha256,
                        "source_sha256": item.source_sha256,
                        "back_substitution": exact_back_substitution(item),
                    }
                    for index, item in enumerate(m5.element_long)
                ],
            },
        }
    return output, ledger


def generated_ledger_sha256(
    ledger: Mapping[str, Any], source_order: Sequence[str]
) -> str:
    ordered: list[dict[str, Any]] = []
    for source_label in source_order:
        source = ledger[source_label]
        for dimension in ("m4", "m5"):
            joint = source["joint"][dimension]
            ordered.extend(
                [
                    {
                        "source": source_label,
                        "dimension": dimension,
                        "variant": "baseline_joint_CSE",
                        "replacement_count": joint["replacement_count"],
                        "source_sha256": joint["baseline_source_sha256"],
                        "dag_sha256": joint["dag_sha256"],
                    },
                    {
                        "source": source_label,
                        "dimension": dimension,
                        "variant": "baseline_nonCSE",
                        "replacement_count": 0,
                        "source_sha256": joint["baseline_plain_source_sha256"],
                        "dag_sha256": joint["baseline_plain_dag_sha256"],
                    },
                    {
                        "source": source_label,
                        "dimension": dimension,
                        "variant": "long_namespace_joint_CSE",
                        "replacement_count": joint["replacement_count"],
                        "source_sha256": joint["long_source_sha256"],
                        "dag_sha256": joint["dag_sha256"],
                    },
                ]
            )
            reference = source["reference_gradient"][dimension]
            ordered.append(
                {
                    "source": source_label,
                    "dimension": dimension,
                    "variant": "reference_gradient_CSE_DAG",
                    "replacement_count": reference["replacement_count"],
                    "source_sha256": reference["source_sha256"],
                    "dag_sha256": reference["dag_sha256"],
                }
            )
            for element in source["elements"][dimension]:
                ordered.append(
                    {
                        "source": source_label,
                        "dimension": dimension,
                        "variant": "element_local_long_CSE",
                        "element_index": element["index"],
                        "replacement_count": element["replacement_count"],
                        "source_sha256": element["source_sha256"],
                        "dag_sha256": element["dag_sha256"],
                    }
                )
    return hashlib.sha256(canonical_bytes({"callables": ordered})).hexdigest()


STAGE_ORDER = (
    "m4_raw_gradient",
    "m4_lifted_gradient",
    "m5_raw_gradient",
    "lambda_blended_gradient",
    "A_lambda_transpose_contraction",
    "outer_minus_conjugation",
)


def fixed_element_sum(contributions: Sequence[np.ndarray], dimension: int) -> np.ndarray:
    total = np.zeros(dimension, dtype=np.clongdouble)
    for contribution in contributions:
        values = np.asarray(contribution, dtype=np.clongdouble).reshape(dimension)
        for index in range(dimension):
            total[index] = np.clongdouble(total[index] + values[index])
    return total


def native_stages(
    slot: Slot, gradient4: np.ndarray, gradient5: np.ndarray
) -> dict[str, np.ndarray]:
    source = slot.source
    inverse = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble)
    coordinates = inverse @ (
        slot.state_w5 - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
    )
    gradient_c = np.concatenate(
        [
            np.asarray(gradient4, dtype=np.clongdouble).reshape(M4),
            np.asarray(
                [
                    source.evaluator.kappa_a * coordinates[7],
                    source.evaluator.kappa_phi * coordinates[8],
                ],
                dtype=np.clongdouble,
            ),
        ]
    )
    lifted = np.asarray(inverse.T @ gradient_c, dtype=np.clongdouble)
    lam = np.longdouble(slot.lambda_value)
    blended = np.asarray(
        (np.longdouble(1) - lam) * lifted
        + lam * np.asarray(gradient5, dtype=np.clongdouble),
        dtype=np.clongdouble,
    )
    contracted = np.asarray(
        np.asarray(slot.node.factor.T, dtype=np.longdouble) @ blended,
        dtype=np.clongdouble,
    )
    outer = np.asarray(-np.conjugate(contracted), dtype=np.clongdouble)
    return {
        "m4_raw_gradient": np.asarray(gradient4, dtype=np.clongdouble),
        "m4_lifted_gradient": lifted,
        "m5_raw_gradient": np.asarray(gradient5, dtype=np.clongdouble),
        "lambda_blended_gradient": blended,
        "A_lambda_transpose_contraction": contracted,
        "outer_minus_conjugation": outer,
    }


def evaluate_slot_native(
    slot: Slot, evaluators: SourceEvaluators
) -> dict[str, Any]:
    variants: dict[str, Any] = {}
    for label, selector in (
        ("baseline_joint_CSE", "baseline_joint"),
        ("baseline_nonCSE", "baseline_plain"),
        ("long_namespace_joint_CSE", "long_joint"),
    ):
        callable4 = getattr(evaluators.m4, selector)
        callable5 = getattr(evaluators.m5, selector)
        raw4, trace4 = traced_call(callable4, slot.state_w4)
        raw5, trace5 = traced_call(callable5, slot.state_w5)
        if raw4.size != M4 + M4 * M4 or raw5.size != M5 + M5 * M5:
            raise InvalidRun(f"joint evaluator output-count drift at {slot.key}:{label}")
        gradient4 = raw4[:M4]
        gradient5 = raw5[:M5]
        variants[label] = {
            "stages": native_stages(slot, gradient4, gradient5),
            "trace": {"m4": trace4, "m5": trace5},
        }

    element4: list[np.ndarray] = []
    trace_elements4: list[dict[str, Any]] = []
    for callable_set in evaluators.m4.element_long:
        raw, trace = traced_call(callable_set, slot.state_w4)
        if raw.size != M4:
            raise InvalidRun("m4 element-gradient output-count drift")
        element4.append(raw)
        trace_elements4.append(trace)
    element5: list[np.ndarray] = []
    trace_elements5: list[dict[str, Any]] = []
    for callable_set in evaluators.m5.element_long:
        raw, trace = traced_call(callable_set, slot.state_w5)
        if raw.size != M5:
            raise InvalidRun("m5 element-gradient output-count drift")
        element5.append(raw)
        trace_elements5.append(trace)
    gradient4 = fixed_element_sum(element4, M4)
    gradient5 = fixed_element_sum(element5, M5)
    variants["element_local_long_CSE"] = {
        "stages": native_stages(slot, gradient4, gradient5),
        "trace": {"m4_elements": trace_elements4, "m5_elements": trace_elements5},
        "element_contributions": {"m4": element4, "m5": element5},
    }
    return variants


def sympy_from_mp(value: Any, digits: int) -> sp.Expr:
    number = mp.mpc(value)
    real_text = mp.nstr(number.real, n=digits, strip_zeros=False)
    imag_text = mp.nstr(number.imag, n=digits, strip_zeros=False)
    return sp.Float(real_text, digits) + sp.I * sp.Float(imag_text, digits)


def sympy_number_to_mp(value: sp.Expr, digits: int) -> mp.mpc:
    numeric = sp.N(value, digits)
    real, imaginary = numeric.as_real_imag()
    output = mp.mpc(mp.mpf(str(sp.N(real, digits))), mp.mpf(str(sp.N(imaginary, digits))))
    if not mp.isfinite(output.real) or not mp.isfinite(output.imag):
        raise InvalidRun("direct SymPy evalf produced a nonfinite value")
    return output


def direct_evalf_gradient(
    expressions: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
    values: Sequence[Any],
    digits: int,
) -> list[mp.mpc]:
    if len(variables) != len(values):
        raise InvalidRun("direct SymPy reference input-length mismatch")
    substitutions = {
        variable: sympy_from_mp(value, digits + 20)
        for variable, value in zip(variables, values, strict=True)
    }
    output: list[mp.mpc] = []
    for expression in expressions:
        evaluated = expression.evalf(digits, subs=substitutions)
        if evaluated.free_symbols:
            raise InvalidRun("direct SymPy reference left unresolved symbols")
        output.append(sympy_number_to_mp(evaluated, digits))
    return output


def direct_evalf_cse_gradient(
    callable_set: GeneratedCallable,
    variables: Sequence[sp.Symbol],
    values: Sequence[Any],
    digits: int,
) -> list[mp.mpc]:
    if len(variables) != len(values):
        raise InvalidRun("direct SymPy CSE-reference input-length mismatch")
    substitutions: dict[sp.Symbol, sp.Expr] = {
        variable: sympy_from_mp(value, digits + 20)
        for variable, value in zip(variables, values, strict=True)
    }
    for symbol, expression in callable_set.replacements:
        evaluated = expression.evalf(digits, subs=substitutions)
        if evaluated.free_symbols:
            raise InvalidRun(
                f"direct SymPy CSE reference left unresolved symbols at {symbol}"
            )
        substitutions[symbol] = evaluated
    output: list[mp.mpc] = []
    for expression in callable_set.reduced:
        evaluated = expression.evalf(digits, subs=substitutions)
        if evaluated.free_symbols:
            raise InvalidRun("direct SymPy CSE reduced output left unresolved symbols")
        output.append(sympy_number_to_mp(evaluated, digits))
    return output


def mp_matvec(matrix: mp.matrix, vector: Sequence[Any]) -> list[mp.mpc]:
    result = matrix * mp.matrix(list(vector))
    return [mp.mpc(result[index]) for index in range(result.rows)]


def reference_slot(
    slot: Slot, evaluators: SourceEvaluators, digits: int
) -> dict[str, Any]:
    with mp.workdps(digits + 30):
        source = slot.source
        state5 = mp_frozen_state_vector(slot.state_w5)
        inverse = mp_matrix_real(source.evaluator.inverse_basis_long)
        anchor5 = mp_vector(source.evaluator.anchor5)
        anchor4 = mp_vector(source.evaluator.anchor4)
        coordinates = mp_matvec(
            inverse,
            [state5[index] - anchor5[index] for index in range(M5)],
        )
        state4 = [anchor4[index] + coordinates[index] for index in range(M4)]
        direct4 = direct_evalf_gradient(
            evaluators.m4.global_gradient,
            evaluators.m4.variables,
            state4,
            digits,
        )
        direct5 = direct_evalf_gradient(
            evaluators.m5.global_gradient,
            evaluators.m5.variables,
            state5,
            digits,
        )
        cse4 = direct_evalf_cse_gradient(
            evaluators.m4.reference_gradient_cse,
            evaluators.m4.variables,
            state4,
            digits,
        )
        cse5 = direct_evalf_cse_gradient(
            evaluators.m5.reference_gradient_cse,
            evaluators.m5.variables,
            state5,
            digits,
        )

        def stages(gradient4: Sequence[Any], gradient5: Sequence[Any]) -> dict[str, list[mp.mpc]]:
            gradient_c = [*gradient4]
            gradient_c.extend(
                [
                    mp_real(source.evaluator.kappa_a) * coordinates[7],
                    mp_real(source.evaluator.kappa_phi) * coordinates[8],
                ]
            )
            lifted = mp_matvec(inverse.T, gradient_c)
            lam = mp_real(np.longdouble(slot.lambda_value))
            blended = [
                (mp.mpf(1) - lam) * lifted[index] + lam * gradient5[index]
                for index in range(M5)
            ]
            factor = mp_matrix_real(slot.node.factor)
            contracted = mp_matvec(factor.T, blended)
            outer = [-mp.conj(value) for value in contracted]
            return {
                "m4_raw_gradient": [mp.mpc(value) for value in gradient4],
                "m4_lifted_gradient": lifted,
                "m5_raw_gradient": [mp.mpc(value) for value in gradient5],
                "lambda_blended_gradient": blended,
                "A_lambda_transpose_contraction": contracted,
                "outer_minus_conjugation": outer,
            }

        direct_stages = stages(direct4, direct5)
        cse_stages = stages(cse4, cse5)
        input_strings = [
            [ld_text(value.real), ld_text(value.imag)]
            for value in np.asarray(slot.state_w5, dtype=np.clongdouble)
        ]
        return {
            "digits": digits,
            "direct": direct_stages,
            "CSE": cse_stages,
            "CSE_to_direct_relative_by_stage": {
                stage: mp_relative(cse_stages[stage], direct_stages[stage])
                for stage in STAGE_ORDER
            },
            "input_lift": {
                "state_w5_25_digit_pairs": input_strings,
                "state_w5_decimal_sha256": hashlib.sha256(
                    json.dumps(input_strings, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
                "w4_recomputed_entirely_in_mpmath": True,
            },
        }


def native_from_mp(value: Sequence[Any]) -> np.ndarray:
    output = np.empty(len(value), dtype=np.clongdouble)
    for index, item in enumerate(value):
        number = mp.mpc(item)
        real = np.longdouble(mp.nstr(number.real, 40))
        imaginary = np.longdouble(mp.nstr(number.imag, 40))
        output[index] = np.clongdouble(real) + np.clongdouble("1j") * np.clongdouble(imaginary)
    return output


def cancellation_record(
    contributions: Sequence[np.ndarray], completed: np.ndarray
) -> dict[str, Any]:
    completed_array = np.asarray(completed, dtype=np.clongdouble).reshape(-1)
    terms = [np.asarray(item, dtype=np.clongdouble).reshape(-1) for item in contributions]
    indices: list[float] = []
    for component in range(completed_array.size):
        numerator = sum((abs(item[component]) for item in terms), np.longdouble(0))
        denominator = max(abs(completed_array[component]), np.longdouble("1e-100"))
        indices.append(float(numerator / denominator))
    return {"per_component": indices, "maximum": max(indices, default=0.0)}


def stage_cancellation(slot: Slot, element_variant: Mapping[str, Any]) -> dict[str, Any]:
    stages = element_variant["stages"]
    contributions4 = element_variant["element_contributions"]["m4"]
    contributions5 = element_variant["element_contributions"]["m5"]
    source = slot.source
    inverse = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble)
    coordinates = inverse @ (
        slot.state_w5 - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
    )
    gradient_c = np.concatenate(
        [
            stages["m4_raw_gradient"],
            np.asarray(
                [
                    source.evaluator.kappa_a * coordinates[7],
                    source.evaluator.kappa_phi * coordinates[8],
                ],
                dtype=np.clongdouble,
            ),
        ]
    )
    lift_terms = [inverse.T[:, index] * gradient_c[index] for index in range(M5)]
    lam = np.longdouble(slot.lambda_value)
    blend_terms = [
        (np.longdouble(1) - lam) * stages["m4_lifted_gradient"],
        lam * stages["m5_raw_gradient"],
    ]
    factor_t = np.asarray(slot.node.factor.T, dtype=np.longdouble)
    contraction_terms = [
        factor_t[:, index] * stages["lambda_blended_gradient"][index]
        for index in range(M5)
    ]
    return {
        "m4_raw_gradient": cancellation_record(
            contributions4, stages["m4_raw_gradient"]
        ),
        "m4_lifted_gradient": cancellation_record(
            lift_terms, stages["m4_lifted_gradient"]
        ),
        "m5_raw_gradient": cancellation_record(
            contributions5, stages["m5_raw_gradient"]
        ),
        "lambda_blended_gradient": cancellation_record(
            blend_terms, stages["lambda_blended_gradient"]
        ),
        "A_lambda_transpose_contraction": cancellation_record(
            contraction_terms, stages["A_lambda_transpose_contraction"]
        ),
        "outer_minus_conjugation": cancellation_record(
            [-np.conjugate(stages["A_lambda_transpose_contraction"])],
            stages["outer_minus_conjugation"],
        ),
    }


def comparison_record(left: Any, right: Any) -> dict[str, Any]:
    left_array = np.asarray(left, dtype=np.clongdouble).reshape(-1)
    right_array = np.asarray(right, dtype=np.clongdouble).reshape(-1)
    difference = left_array - right_array
    return {
        "symmetric_relative": native_relative(left_array, right_array),
        "difference_norm_absolute": float(np.linalg.norm(difference)),
        "difference_max_component_absolute": float(
            np.max(np.abs(difference), initial=np.longdouble(0))
        ),
        "difference_vector": difference,
    }


def native_to_mp_comparison_record(
    native: Any, reference: Sequence[Any]
) -> dict[str, Any]:
    """Compare a native candidate with the full retained MP reference."""
    left = mp_vector(np.asarray(native, dtype=np.clongdouble).reshape(-1))
    right = [mp.mpc(value) for value in reference]
    if len(left) != len(right):
        raise InvalidRun("native-to-MP comparison length mismatch")
    difference = [
        left[index] - right[index] for index in range(len(left))
    ]
    relative = mp_relative(left, right)
    norm_absolute = mp_norm(difference)
    maximum_absolute = max(
        (abs(value) for value in difference), default=mp.mpf("0")
    )
    return {
        "symmetric_relative": float(relative),
        "symmetric_relative_decimal": mp.nstr(relative, 50),
        "difference_norm_absolute_decimal": mp.nstr(norm_absolute, 50),
        "difference_max_component_absolute_decimal": mp.nstr(
            maximum_absolute, 50
        ),
        "difference_vector": mp_vector_record(difference, digits=40),
        "comparison_arithmetic": "mpmath_at_160_dps_without_reference_downcast",
    }


def telescope_record(
    baseline: Mapping[str, np.ndarray],
    candidate: Mapping[str, np.ndarray],
    reference: Mapping[str, Sequence[Any]],
) -> dict[str, Any]:
    records: dict[str, Any] = {}
    maximum = 0.0
    for stage in STAGE_ORDER:
        base = np.asarray(baseline[stage], dtype=np.clongdouble)
        repaired = np.asarray(candidate[stage], dtype=np.clongdouble)
        ref = native_from_mp(reference[stage])
        baseline_to_candidate = base - repaired
        candidate_to_reference = repaired - ref
        baseline_to_reference = base - ref
        closure = (
            baseline_to_candidate
            + candidate_to_reference
            - baseline_to_reference
        )
        denominator = max(
            np.linalg.norm(baseline_to_candidate),
            np.linalg.norm(candidate_to_reference),
            np.linalg.norm(baseline_to_reference),
            np.longdouble("1e-100"),
        )
        relative = float(np.linalg.norm(closure) / denominator)
        maximum = max(maximum, relative)
        records[stage] = {
            "baseline_to_candidate": baseline_to_candidate,
            "candidate_to_reference": candidate_to_reference,
            "baseline_to_reference": baseline_to_reference,
            "closure_vector": closure,
            "relative_closure": relative,
        }
    contraction_difference = (
        np.asarray(baseline["A_lambda_transpose_contraction"], dtype=np.clongdouble)
        - np.asarray(candidate["A_lambda_transpose_contraction"], dtype=np.clongdouble)
    )
    outer_difference = (
        np.asarray(baseline["outer_minus_conjugation"], dtype=np.clongdouble)
        - np.asarray(candidate["outer_minus_conjugation"], dtype=np.clongdouble)
    )
    outer_residual = outer_difference + np.conjugate(contraction_difference)
    outer_relative = float(
        np.linalg.norm(outer_residual)
        / max(
            np.linalg.norm(outer_difference),
            np.linalg.norm(contraction_difference),
            np.longdouble("1e-100"),
        )
    )
    maximum = max(maximum, outer_relative)
    return {
        "stages": records,
        "outer_minus_conjugation_unexplained_relative": outer_relative,
        "maximum_relative_closure": maximum,
    }


def trace_contracts(
    native_results: Mapping[str, Mapping[str, Any]], manifest: Mapping[str, Any]
) -> dict[str, Any]:
    observations = manifest["disclosed_feasibility_pilots"][
        "observations_known_before_freeze"
    ]
    expected = observations["baseline_CSE_temporary_dtype_counts"]
    baseline_ok = True
    repaired_ok = True
    records: dict[str, Any] = {}
    for slot_key, variants in native_results.items():
        baseline = variants["baseline_joint_CSE"]["trace"]
        long_joint = variants["long_namespace_joint_CSE"]["trace"]
        element = variants["element_local_long_CSE"]["trace"]
        slot_record: dict[str, Any] = {
            "baseline_joint_CSE": baseline,
            "baseline_binary64_normalized_counts": {},
            "long_namespace_joint_CSE": long_joint,
            "element_local_long_CSE": element,
        }
        for dimension in ("m4", "m5"):
            trace = baseline[dimension]
            expected_trace = expected[dimension]
            dtype_counts = trace["temporary_dtype_counts"]
            normalized_binary64 = int(dtype_counts.get("float64", 0)) + int(
                dtype_counts.get("python_float64", 0)
            )
            slot_record["baseline_binary64_normalized_counts"][dimension] = {
                "numpy_float64": int(dtype_counts.get("float64", 0)),
                "python_float64": int(dtype_counts.get("python_float64", 0)),
                "normalized_binary64": normalized_binary64,
                "expected_binary64": int(expected_trace["float64"]),
            }
            baseline_ok = bool(
                baseline_ok
                and trace["traced_temporary_count"] == int(expected_trace["total"])
                and trace["replacement_count"] == int(expected_trace["total"])
                and sum(int(value) for value in dtype_counts.values())
                == int(expected_trace["total"])
                and set(dtype_counts).issubset(
                    {"float64", "python_float64", "complex256"}
                )
                and normalized_binary64 == int(expected_trace["float64"])
                and dtype_counts.get("complex256", 0)
                == int(expected_trace["complex256"])
            )
            repaired_trace = long_joint[dimension]
            repaired_ok = bool(
                repaired_ok
                and repaired_trace["traced_temporary_count"]
                == repaired_trace["replacement_count"]
                and repaired_trace["all_temporary_scalars_exact_clongdouble"]
                and repaired_trace["all_raw_scalars_exact_clongdouble"]
                and repaired_trace["raw_output_count"]
                == (M4 + M4 * M4 if dimension == "m4" else M5 + M5 * M5)
            )
        for dimension, count in (("m4_elements", M4), ("m5_elements", M5)):
            for trace in element[dimension]:
                repaired_ok = bool(
                    repaired_ok
                    and trace["traced_temporary_count"] == trace["replacement_count"]
                    and trace["all_temporary_scalars_exact_clongdouble"]
                    and trace["all_raw_scalars_exact_clongdouble"]
                    and trace["raw_output_count"] == count
                )
        records[slot_key] = slot_record
    return {
        "baseline_hidden_float64_counts_reproduced": baseline_ok,
        "both_repaired_variants_exact_clongdouble": repaired_ok,
        "records": records,
    }


def symbolic_contracts(
    ledger: Mapping[str, Any], manifest: Mapping[str, Any]
) -> dict[str, Any]:
    observations = manifest["disclosed_feasibility_pilots"][
        "observations_known_before_freeze"
    ]["baseline_CSE_temporary_dtype_counts"]
    element_identity = True
    back_substitution = True
    fingerprints = True
    replacement_counts = True
    phase51_binding = True
    for source in ledger.values():
        element_identity = bool(
            element_identity
            and source["element_identity"]["m4"]
            and source["element_identity"]["m5"]
        )
        for dimension in ("m4", "m5"):
            binding = source["phase51_production_callable_binding"][dimension]
            phase51_binding = bool(
                phase51_binding
                and all(
                    record["actual_pinned_phase51_callable_used"]
                    and record["alpha_normalized_source_equal"]
                    and record["replacement_locals_present"]
                    for record in binding.values()
                )
            )
            joint = source["joint"][dimension]
            back_substitution = bool(
                back_substitution
                and joint["back_substitution"]
                and source["reference_gradient"][dimension]["back_substitution"]
                and all(
                    record["back_substitution"]
                    for record in source["elements"][dimension]
                )
            )
            fingerprints = bool(
                fingerprints
                and joint["long_same_DAG"]
                and source["reference_gradient"][dimension]["construction"]
                == "direct_sp.cse_without_lambdify"
                and all(
                    isinstance(value, str) and len(value) == 64
                    for value in (
                        joint["dag_sha256"],
                        joint["baseline_source_sha256"],
                        joint["baseline_plain_source_sha256"],
                        joint["baseline_plain_dag_sha256"],
                        joint["long_source_sha256"],
                        source["reference_gradient"][dimension]["dag_sha256"],
                        source["reference_gradient"][dimension]["source_sha256"],
                    )
                )
            )
            replacement_counts = bool(
                replacement_counts
                and joint["replacement_count"] == int(observations[dimension]["total"])
            )
    return {
        "element_gradient_sum_identity": element_identity,
        "all_CSE_back_substitutions_exact": back_substitution,
        "fingerprints_complete_and_joint_DAG_shared": fingerprints,
        "baseline_joint_replacement_counts_frozen": replacement_counts,
        "actual_Phase51_production_callables_bound": phase51_binding,
    }


def guard_contract(manifest: Mapping[str, Any]) -> bool:
    required = manifest["required_outputs"]
    classification = manifest["classification"]
    return bool(
        all(
            required.get(key) is None
            for key in (
                "promoted_output",
                "bounded_chain_signed_sum",
                "complete_global_signed_intersection_vector",
                "global_n_sigma",
                "cutoff_limit",
                "continuum_limit",
            )
        )
        and classification.get("Phase51_raw_result_mutated") is False
        and classification.get("Phase51_scientific_label_may_be_promoted") is False
        and classification.get("global_promotion") == "PROHIBITED"
        and classification.get("Gate1") == "OPEN_PARTIAL_PROGRESS"
    )


def run_calculation() -> dict[str, Any]:
    progress("validating frozen bytes, self digests, runtime, and committed runner")
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    observed, p51_manifest, p51_result, runner_guard = validate_inputs(
        manifest, manifest_raw, authoritative=True
    )
    p51_result_sha_at_start = sha256_path(P51_RESULT_PATH)
    p51 = load_module("ice_phase51_for_phase52", P51_RUNNER_PATH)
    contexts, p51_context_validation = build_phase51_contexts(p51, p51_manifest)
    slot_spec = manifest["slots"]
    source_order = [str(value) for value in slot_spec["source_order"]]
    lambda_order = [float(value) for value in slot_spec["lambda_order"]]
    slots = build_slots(contexts, source_order, lambda_order)

    progress("reproducing the six immutable Phase51 evaluator records")
    reproduction = reproduce_phase51_records(
        p51, contexts, p51_result, lambda_order
    )
    progress("building global, joint-CSE, and element-local symbolic evaluators")
    evaluators, symbolic_ledger = build_symbolic_evaluators(p51, contexts)
    symbolic = symbolic_contracts(symbolic_ledger, manifest)
    generated_fingerprint = generated_ledger_sha256(symbolic_ledger, source_order)
    symbolic["generated_callable_ledger_sha256"] = generated_fingerprint
    symbolic["expected_generated_callable_ledger_sha256"] = (
        EXPECTED_GENERATED_LEDGER_SHA256
    )
    if (
        EXPECTED_GENERATED_LEDGER_SHA256 == "FINGERPRINT_PENDING"
        or generated_fingerprint != EXPECTED_GENERATED_LEDGER_SHA256
    ):
        raise InvalidRun(
            "authoritative generated-callable ledger fingerprint is pending or drifted: "
            f"observed={generated_fingerprint}, expected={EXPECTED_GENERATED_LEDGER_SHA256}"
        )

    progress("tracing baseline and repaired runtime dtypes at six slots")
    native_results: dict[str, dict[str, Any]] = {}
    for slot in slots:
        native_results[slot.key] = evaluate_slot_native(
            slot, evaluators[slot.source_label]
        )
    dtype_audit = trace_contracts(native_results, manifest)

    progress("evaluating independent direct and CSE references at 80/120 dps")
    references: dict[str, dict[int, Any]] = {}
    for slot in slots:
        references[slot.key] = {
            digits: reference_slot(slot, evaluators[slot.source_label], digits)
            for digits in (80, 120)
        }

    thresholds = manifest["thresholds"]
    reference_tier_limit = mp.mpf(str(thresholds["mpmath_80_vs_120_relative_max"]))
    reference_cse_limit = mp.mpf(str(thresholds["mpmath_CSE_vs_nonCSE_relative_max"]))
    gradient_limit = mp.mpf(
        str(thresholds["candidate_gradient_to_120dps_relative_max"])
    )
    rhs_limit = mp.mpf(str(thresholds["candidate_RHS_to_120dps_relative_max"]))
    telescope_limit = float(thresholds["native_telescope_relative_closure_max"])

    reference_records: dict[str, Any] = {}
    candidate_records: dict[str, Any] = {}
    telescope_records: dict[str, Any] = {}
    cancellation_records: dict[str, Any] = {}
    max_80_120 = mp.mpf(0)
    max_cse_plain = mp.mpf(0)
    max_long_gradient = mp.mpf("0")
    max_long_rhs = mp.mpf("0")
    max_element_gradient = mp.mpf("0")
    max_element_rhs = mp.mpf("0")
    max_telescope = 0.0
    with mp.workdps(160):
        for slot in slots:
            ref80 = references[slot.key][80]
            ref120 = references[slot.key][120]
            precision_by_stage: dict[str, Any] = {}
            cse_by_tier: dict[str, Any] = {}
            for stage in STAGE_ORDER:
                precision_relative = mp_relative(
                    ref80["direct"][stage], ref120["direct"][stage]
                )
                max_80_120 = max(max_80_120, precision_relative)
                precision_by_stage[stage] = {
                    "relative": precision_relative,
                    "direct_80": mp_vector_record(ref80["direct"][stage]),
                    "direct_120": mp_vector_record(ref120["direct"][stage]),
                }
            for digits in (80, 120):
                tier = references[slot.key][digits]
                cse_by_tier[str(digits)] = {}
                for stage in STAGE_ORDER:
                    relative = tier["CSE_to_direct_relative_by_stage"][stage]
                    max_cse_plain = max(max_cse_plain, relative)
                    cse_by_tier[str(digits)][stage] = {
                        "relative": relative,
                        "CSE": mp_vector_record(tier["CSE"][stage]),
                    }
            reference_records[slot.key] = {
                "input_lift": ref120["input_lift"],
                "direct_80_vs_120": precision_by_stage,
                "CSE_to_direct_by_tier": cse_by_tier,
            }

            slot_candidates: dict[str, Any] = {}
            for variant_label in (
                "long_namespace_joint_CSE",
                "element_local_long_CSE",
            ):
                stages = native_results[slot.key][variant_label]["stages"]
                comparisons = {
                    stage: native_to_mp_comparison_record(
                        stages[stage], ref120["direct"][stage]
                    )
                    for stage in STAGE_ORDER
                }
                gradient_relative = mp.mpf(
                    comparisons["lambda_blended_gradient"][
                        "symmetric_relative_decimal"
                    ]
                )
                rhs_relative = mp.mpf(
                    comparisons["outer_minus_conjugation"][
                        "symmetric_relative_decimal"
                    ]
                )
                if variant_label == "long_namespace_joint_CSE":
                    max_long_gradient = max(max_long_gradient, gradient_relative)
                    max_long_rhs = max(max_long_rhs, rhs_relative)
                else:
                    max_element_gradient = max(max_element_gradient, gradient_relative)
                    max_element_rhs = max(max_element_rhs, rhs_relative)
                slot_candidates[variant_label] = {
                    "stage_comparisons_to_direct_120dps": comparisons,
                    "gradient_relative": float(gradient_relative),
                    "gradient_relative_decimal": mp.nstr(gradient_relative, 50),
                    "RHS_relative": float(rhs_relative),
                    "RHS_relative_decimal": mp.nstr(rhs_relative, 50),
                }
            baseline_plain = native_results[slot.key]["baseline_nonCSE"]["stages"]
            baseline_cse = native_results[slot.key]["baseline_joint_CSE"]["stages"]
            slot_candidates["historical_baseline_pair"] = {
                stage: comparison_record(baseline_cse[stage], baseline_plain[stage])
                for stage in STAGE_ORDER
            }
            candidate_records[slot.key] = slot_candidates

            telescope = telescope_record(
                native_results[slot.key]["baseline_joint_CSE"]["stages"],
                native_results[slot.key]["element_local_long_CSE"]["stages"],
                ref120["direct"],
            )
            max_telescope = max(max_telescope, telescope["maximum_relative_closure"])
            telescope_records[slot.key] = telescope
            cancellation_records[slot.key] = stage_cancellation(
                slot, native_results[slot.key]["element_local_long_CSE"]
            )

    reproduction_pass = bool(
        reproduction["structural_fields_match"]
        and reproduction["maximum_absolute_numeric_difference"]
        <= float(thresholds["phase51_record_reproduction_absolute_max"])
    )
    baseline_violation_reproduced = bool(
        dtype_audit["baseline_hidden_float64_counts_reproduced"]
    )
    repaired_dtype_pass = bool(dtype_audit["both_repaired_variants_exact_clongdouble"])
    reference_pass = bool(
        max_80_120 <= reference_tier_limit and max_cse_plain <= reference_cse_limit
    )
    long_accuracy_pass = bool(
        max_long_gradient <= gradient_limit and max_long_rhs <= rhs_limit
    )
    element_pass = bool(
        max_element_gradient <= gradient_limit and max_element_rhs <= rhs_limit
    )
    telescope_pass = bool(max_telescope <= telescope_limit)
    null_guard_pass = guard_contract(manifest)
    pin_sha256_at_end = {
        label: sha256_path(REPO_ROOT / str(record["path"]))
        for label, record in observed.items()
    }
    pinned_bytes_unchanged = all(
        pin_sha256_at_end[label] == str(record["sha256"])
        for label, record in observed.items()
    )
    manifest_unchanged = sha256_path(INPUT_PATH) == INPUT_SHA256

    contract = Contract()
    contract.add_exact(
        "P52.inputs.byte_pins_self_digests_and_manifest_before_runner",
        bool(
            runner_guard["runner_clean"]
            and runner_guard["manifest_is_ancestor"]
            and hashlib.sha256(manifest_raw).hexdigest() == INPUT_SHA256
            and manifest_unchanged
            and pinned_bytes_unchanged
        ),
        "the frozen manifest, runtime, byte pins, self digests, and committed post-manifest runner validate",
        {
            "validated_inputs": observed,
            "pin_sha256_at_end": pin_sha256_at_end,
            "pinned_bytes_unchanged": pinned_bytes_unchanged,
            "manifest_unchanged": manifest_unchanged,
            "runner_guard": runner_guard,
        },
    )
    state_records = []
    state_pass = bool(
        len(slots) == int(slot_spec["count"])
        and [slot.source_label for slot in slots]
        == [label for label in source_order for _value in lambda_order]
        and [slot.lambda_value for slot in slots]
        == [value for _label in source_order for value in lambda_order]
    )
    for slot in slots:
        recomputed = np.asarray(slot.node.saddle_w, dtype=np.clongdouble) + np.clongdouble(
            slot.node.sphere_radius
        ) * (
            np.asarray(slot.node.launch_w, dtype=np.clongdouble)
            @ np.asarray(slot.source.chart.center, dtype=np.longdouble)
        )
        exact = bool(
            slot.state_w5.dtype == np.dtype(np.clongdouble)
            and np.array_equal(slot.state_w5, recomputed)
        )
        state_pass = bool(state_pass and exact)
        state_records.append(
            {
                "slot": slot.key,
                "exact_formula_reconstruction": exact,
                "state_w5": slot.state_w5,
                "state_w4_native_diagnostic_only": slot.state_w4,
            }
        )
    contract.add_exact(
        "P52.slots.exact_Phase51_six_state_construction",
        state_pass,
        "exactly six ordered center-launch states are reconstructed from the pinned Phase51 source context",
        {"slots": state_records},
    )
    contract.add_exact(
        "P52.symbolic.element_gradient_sum_identity",
        symbolic["element_gradient_sum_identity"],
        "the exact-decimal Rational source-family element sums equal its globally expanded gradient, while executable Float residuals remain explicit",
        {"symbolic": symbolic_ledger},
    )
    contract.add_exact(
        "P52.symbolic.CSE_back_substitution_and_DAG_fingerprints",
        bool(
            symbolic["all_CSE_back_substitutions_exact"]
            and symbolic["fingerprints_complete_and_joint_DAG_shared"]
            and symbolic["baseline_joint_replacement_counts_frozen"]
            and symbolic["actual_Phase51_production_callables_bound"]
        ),
        "the actual pinned Phase51 production callables are alpha-bound to exact back-substituted DAGs with frozen replacement counts and retained fingerprints",
        symbolic,
    )
    contract.add_exact(
        "P52.dtype.trace_completeness_and_raw_output_guard",
        repaired_dtype_pass,
        "every repaired replacement and every raw joint or element output is traced before coercion as exact np.clongdouble",
        {
            "both_repaired_variants_exact_clongdouble": repaired_dtype_pass,
            "joint_raw_counts": {"m4": 56, "m5": 90},
            "element_raw_counts": {"m4": 7, "m5": 9},
        },
    )
    contract.add_exact(
        "P52.conventions.stage_order_transpose_and_reference_isolation",
        bool(
            tuple(manifest["metrics"]["stage_order"]) == STAGE_ORDER
            and set(references) == {slot.key for slot in slots}
        ),
        "the frozen stage order, ordinary A_lambda transpose, one final minus-conjugation, and direct-evalf reference isolation are retained",
        {
            "stage_order": STAGE_ORDER,
            "A_lambda_operation": "ordinary_transpose",
            "outer_operation": "exactly_one_final_minus_conjugation",
            "reference_w4": "recomputed_from_decimal_lifted_w5_in_mpmath",
            "reference_lambdify_used": False,
            "extra_phi_minus_conjugation": False,
        },
    )
    contract.add_exact(
        "P52.guard.historical_nonrewrite_and_global_nulls",
        bool(null_guard_pass and sha256_path(P51_RESULT_PATH) == p51_result_sha_at_start),
        "the historical Phase51 result is byte-unchanged and all global/cutoff/continuum outputs remain null or prohibited",
        {
            "phase51_result_sha256_before": p51_result_sha_at_start,
            "phase51_result_sha256_after": sha256_path(P51_RESULT_PATH),
            "global_promotion": manifest["classification"]["global_promotion"],
        },
    )

    scientific_prerequisites = bool(
        reproduction_pass
        and baseline_violation_reproduced
        and reference_pass
        and repaired_dtype_pass
        and telescope_pass
        and null_guard_pass
    )
    classification_spec = manifest["classification"]
    if scientific_prerequisites and element_pass:
        classification = classification_spec[
            "primary_if_all_prerequisites_and_element_candidate_gradient_and_RHS_pass"
        ]
    elif scientific_prerequisites:
        classification = classification_spec[
            "if_all_prerequisites_but_element_candidate_gradient_or_RHS_fails"
        ]
    else:
        classification = classification_spec[
            "if_a_scientific_reference_or_reproduction_prerequisite_is_incomplete_without_invalidating_the_run"
        ]

    contract.add_numerical(
        "P52.reproduction.Phase51_six_slot_evaluator_records",
        reproduction_pass,
        "all six historical Phase51 evaluator records reproduce by semantic JSON path",
        {
            "maximum_absolute_numeric_difference": reproduction[
                "maximum_absolute_numeric_difference"
            ],
            "threshold": float(thresholds["phase51_record_reproduction_absolute_max"]),
        },
    )
    contract.add_numerical(
        "P52.audit.Phase51_all_CSE_temporaries_clongdouble",
        baseline_violation_reproduced,
        "the historical all-temporaries-clongdouble proposition is reproducibly false with the frozen m4/m5 counts",
        {
            "historical_all_temporaries_clongdouble": False,
            "typed_historical_failure": "P51_CSE_DTYPE_CONTRACT_VIOLATION_REPRODUCED",
            "counts_reproduced": baseline_violation_reproduced,
            "non_infrastructure_failure": True,
        },
    )
    contract.add_numerical(
        "P52.reference.mpmath_80_120_and_CSE_plain_stability",
        reference_pass,
        "direct SymPy evalf is stable from 80 to 120 digits and its directly evaluated CSE DAG agrees with the unreduced expressions",
        {
            "maximum_80_vs_120_relative": mp.nstr(max_80_120, 40),
            "maximum_CSE_vs_plain_relative": mp.nstr(max_cse_plain, 40),
            "thresholds": {
                "80_vs_120": str(reference_tier_limit),
                "CSE_vs_plain": str(reference_cse_limit),
            },
        },
    )
    contract.add_numerical(
        "P52.repair.long_namespace_joint_CSE",
        long_accuracy_pass,
        "the mandatory-dtype long-namespace joint-CSE negative control is assessed against direct 120-dps gradients and RHS values",
        {
            "accuracy_role": classification_spec[
                "long_namespace_joint_CSE_accuracy_role"
            ],
            "mandatory_dtype_passed": repaired_dtype_pass,
            "maximum_gradient_relative": mp.nstr(max_long_gradient, 50),
            "maximum_RHS_relative": mp.nstr(max_long_rhs, 50),
            "gradient_threshold": str(gradient_limit),
            "RHS_threshold": str(rhs_limit),
        },
        failure_status="DIAGNOSTIC_NEGATIVE_CONTROL_ACCURACY_NONPASS",
    )
    contract.add_numerical(
        "P52.repair.element_local_long_CSE",
        element_pass,
        "the fixed-order element-local long-CSE candidate is assessed against direct 120-dps gradients and RHS values",
        {
            "maximum_gradient_relative": mp.nstr(max_element_gradient, 50),
            "maximum_RHS_relative": mp.nstr(max_element_rhs, 50),
            "gradient_threshold": str(gradient_limit),
            "RHS_threshold": str(rhs_limit),
        },
        failure_status="STATIC_RHS_REPAIR_NOT_SUFFICIENT",
    )
    contract.add_numerical(
        "P52.arithmetic.stage_telescope_and_cancellation",
        telescope_pass,
        "the baseline-to-candidate plus candidate-to-reference telescope closes at every stage and cancellation ledgers are retained",
        {
            "maximum_relative_closure": max_telescope,
            "threshold": telescope_limit,
        },
    )
    valid_labels = {
        classification_spec[
            "primary_if_all_prerequisites_and_element_candidate_gradient_and_RHS_pass"
        ],
        classification_spec[
            "if_all_prerequisites_but_element_candidate_gradient_or_RHS_fails"
        ],
        classification_spec[
            "if_a_scientific_reference_or_reproduction_prerequisite_is_incomplete_without_invalidating_the_run"
        ],
    }
    contract.add_numerical(
        "P52.guard.classification_and_nulls",
        bool(classification in valid_labels and null_guard_pass),
        "classification is selected only from the frozen local diagnostic labels and every global output remains null",
        {
            "classification": classification,
            "scientific_prerequisites": scientific_prerequisites,
            "element_candidate_passed": element_pass,
        },
    )
    if [record["id"] for record in contract.exact] != manifest["checks"]["exact"]:
        raise InvalidRun("emitted exact-check order drift")
    if [record["id"] for record in contract.numerical] != manifest["checks"]["numerical"]:
        raise InvalidRun("emitted numerical-check order drift")
    if sha256_path(SCRIPT_PATH) != runner_guard["runner_sha256_at_start"]:
        raise InvalidRun("Phase52 runner bytes changed during execution")

    required = manifest["required_outputs"]
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 52,
        "run_status": "VALID_RUN",
        "classification": classification,
        "counts": {
            "exact_passed": sum(record["passed"] for record in contract.exact),
            "exact_total": len(contract.exact),
            "numerical_passed": sum(record["passed"] for record in contract.numerical),
            "numerical_total": len(contract.numerical),
        },
        "provenance": {
            "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "manifest_commit": INPUT_COMMIT,
            "manifest_sha256": INPUT_SHA256,
            "runner_path": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "runner_commit": runner_guard["runner_commit"],
            "runner_sha256": runner_guard["runner_sha256_at_start"],
            "canonical_result_path": str(
                SCRIPT_PATH.with_name(
                    "PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_RESULT.json"
                ).relative_to(REPO_ROOT)
            ),
            "validated_inputs": observed,
            "runtime": runtime_record(),
        },
        "exact_checks": contract.exact,
        "numerical_checks": contract.numerical,
        "phase51_context_validation": p51_context_validation,
        "phase51_six_record_reproduction": reproduction,
        "symbolic_evaluator_ledger": symbolic_ledger,
        "generated_callable_ledger_sha256": generated_fingerprint,
        "runtime_dtype_audit": dtype_audit,
        "reference_validation": reference_records,
        "candidate_assessment": candidate_records,
        "stage_telescopes": telescope_records,
        "cancellation_ledgers": cancellation_records,
        "native_stage_values": {
            slot_key: {
                variant: record["stages"]
                for variant, record in variants.items()
            }
            for slot_key, variants in native_results.items()
        },
        "scientific_prerequisites": {
            "Phase51_records_reproduced": reproduction_pass,
            "baseline_hidden_float64_violation_reproduced": baseline_violation_reproduced,
            "reference_complete_and_stable": reference_pass,
            "both_repaired_dtype_contracts_passed": repaired_dtype_pass,
            "stage_telescope_passed": telescope_pass,
            "null_guard_passed": null_guard_pass,
            "long_namespace_accuracy_negative_control_passed": long_accuracy_pass,
            "element_local_gradient_and_RHS_passed": element_pass,
        },
        "Phase51_raw_result_mutated": False,
        "Phase51_historical_emitted_status": classification_spec[
            "Phase51_historical_emitted_status"
        ],
        "Phase51_protocol_validity": "NOT_UPHELD",
        "Phase51_protocol_validity_after_confirmed_hidden_float64": classification_spec[
            "Phase51_protocol_validity_after_confirmed_hidden_float64"
        ],
        "Phase53_full_rerun_required_before_any_local_supported_label": classification_spec[
            "Phase53_full_rerun_required_before_any_local_supported_label"
        ],
        "promoted_output": required["promoted_output"],
        "bounded_chain_signed_sum": required["bounded_chain_signed_sum"],
        "complete_global_signed_intersection_vector": required[
            "complete_global_signed_intersection_vector"
        ],
        "global_n_sigma": required["global_n_sigma"],
        "cutoff_limit": required["cutoff_limit"],
        "continuum_limit": required["continuum_limit"],
        "global_promotion": classification_spec["global_promotion"],
        "Gate1": classification_spec["Gate1"],
        "interpretation_boundary": manifest["run_semantics"]["boundary"],
    }
    return with_self_digest(json_ready(payload))


def validate_only() -> dict[str, Any]:
    progress("validate-only: checking frozen inputs and building six symbolic contexts")
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    observed, p51_manifest, _p51_result, runner_guard = validate_inputs(
        manifest, manifest_raw, authoritative=False
    )
    p51 = load_module("ice_phase51_for_phase52_validate", P51_RUNNER_PATH)
    contexts, p51_context_validation = build_phase51_contexts(p51, p51_manifest)
    source_order = [str(value) for value in manifest["slots"]["source_order"]]
    lambda_order = [float(value) for value in manifest["slots"]["lambda_order"]]
    slots = build_slots(contexts, source_order, lambda_order)
    _evaluators, ledger = build_symbolic_evaluators(p51, contexts)
    symbolic = symbolic_contracts(ledger, manifest)
    generated_fingerprint = generated_ledger_sha256(ledger, source_order)
    fingerprint_matches = bool(
        EXPECTED_GENERATED_LEDGER_SHA256 == "FINGERPRINT_PENDING"
        or generated_fingerprint == EXPECTED_GENERATED_LEDGER_SHA256
    )
    passed = bool(
        len(slots) == 6
        and symbolic["element_gradient_sum_identity"]
        and symbolic["all_CSE_back_substitutions_exact"]
        and symbolic["fingerprints_complete_and_joint_DAG_shared"]
        and symbolic["baseline_joint_replacement_counts_frozen"]
        and symbolic["actual_Phase51_production_callables_bound"]
        and fingerprint_matches
        and sha256_path(SCRIPT_PATH) == runner_guard["runner_sha256_at_start"]
    )
    if not passed:
        raise InvalidRun(
            "validate-only symbolic/source contract failed: "
            f"slots={len(slots)}, symbolic={symbolic}"
        )
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 52,
        "run_status": "VALIDATION_ONLY",
        "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "runner_sha256": runner_guard["runner_sha256_at_start"],
        "validated_inputs": observed,
        "runtime": runtime_record(),
        "phase51_context_validation": p51_context_validation,
        "slot_order": [slot.key for slot in slots],
        "symbolic_contracts": symbolic,
        "symbolic_evaluator_ledger": ledger,
        "generated_callable_ledger_sha256": generated_fingerprint,
        "expected_generated_callable_ledger_sha256": EXPECTED_GENERATED_LEDGER_SHA256,
        "generated_callable_ledger_fingerprint_matches_or_pending": fingerprint_matches,
    }
    return with_self_digest(json_ready(payload))


def invalid_payload(error: Exception) -> dict[str, Any]:
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 52,
        "run_status": "INVALID_RUN",
        "classification": "INVALID_RUN",
        "failure": {
            "type": type(error).__name__,
            "message": str(error)[:4096],
            "traceback": traceback.format_exc(limit=10),
        },
        "promoted_output": None,
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "cutoff_limit": None,
        "continuum_limit": None,
        "global_promotion": "PROHIBITED",
        "Gate1": "OPEN_PARTIAL_PROGRESS",
    }
    return with_self_digest(json_ready(payload))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate pins, six source states, and symbolic evaluator construction without the numerical audit",
    )
    arguments = parser.parse_args()
    try:
        output = validate_only() if arguments.validate_only else run_calculation()
        verify_self_digest(output, label="Phase52 emitted payload")
        print(RESULT_PREFIX + canonical_bytes(output).decode("utf-8"), flush=True)
        return 0
    except Exception as error:
        output = invalid_payload(error)
        verify_self_digest(output, label="Phase52 invalid payload")
        print(RESULT_PREFIX + canonical_bytes(output).decode("utf-8"), flush=True)
        progress(f"INVALID_RUN: {type(error).__name__}: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
