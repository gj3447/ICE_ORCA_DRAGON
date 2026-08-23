#!/usr/bin/env python3
"""Phase 55: root-fixed, P50-saddle-pinned trajectory schedule transfer.

This calculation consumes exactly three saved Phase-53 ``phi_plus`` roots,
reconstructs three launches from the corresponding pinned Phase-50 saddles,
and compares one coherent element-local standard-arithmetic state RHS with
the Phase-53 element-local long-arithmetic production state RHS.  No saddle,
Gamma--K root, tangent, continuation, reflection, mutation, or action ledger
is solved or replayed.

Progress is written to stderr.  Exactly one strict ``RESULT_JSON=...`` record
is written to stdout.  The runner writes no repository files.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import re
import subprocess
import sys
import traceback
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Iterable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
from mpmath import mp
import numpy as np
import scipy
import scipy.integrate
import scipy.optimize
import sympy as sp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER_INPUTS.json"
)
P51_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase51_m5_gamma_k_local_continuation.py"
)
P52_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase52_m5_cse_runtime_dtype_and_rhs_repair.py"
)
P53_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase53_m5_element_local_full_continuation.py"
)
P54_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase54_p51_global_noncse_control_audit.py"
)

INPUT_INTRODUCTION_COMMIT = "de9fb6d22c44d5a271324967a85a4062264d6c1c"
INPUT_COMMIT = "10bb1ca9f735e6abc885206c049506da49c3a96e"
INPUT_BLOB_OID = "bb7b9c2409528918cf8a91d7ac3265d817cbfc2c"
INPUT_SHA256 = "7d5730252356c886671c1d9877bcbb44e49f7e3830d5307d25f6ed951418685d"
INPUT_SIZE_BYTES = 54905

RESULT_SCHEMA = "ice-phase55-p53-root-fixed-launch-schedule-transfer/v1"
RESULT_PREFIX = "RESULT_JSON="
M4 = 7
M5 = 9
SOURCE = "phi_plus"
LAMBDA_ORDER = (0.0, 0.5, 1.0)
BACKEND_ORDER = ("EL_long", "EL_std")
FRACTION_ORDER = (0.0, 0.25, 0.5, 0.75, 1.0)
CORE_ORDER = ("GN_std", "GN_long", "EL_std", "EL_long")
STAGE_ORDER = (
    "m4_raw_gradient",
    "m4_lifted_gradient",
    "m5_raw_gradient",
    "lambda_blended_gradient",
    "A_lambda_transpose_contraction",
    "outer_minus_conjugation",
)
STAGE_DIMENSIONS = (7, 9, 9, 9, 9, 9)
SELECTOR_STAGES = ("lambda_blended_gradient", "outer_minus_conjugation")
PRODUCTION_CONTRASTS = (
    ("GN_std", "GN_long", "printer_and_namespace_only"),
    ("EL_std", "EL_long", "callable_and_accumulator_precision_only"),
    ("GN_std", "EL_std", "global_noncse_vs_element_local_schedule_standard"),
    ("GN_long", "EL_long", "global_noncse_vs_element_local_schedule_long"),
)
CANDIDATE_CONTRASTS = (
    ("EL_std", "EL_long", "callable_and_accumulator_precision_only"),
)
PRODUCTION_TELESCOPE_LEFT = ("GN_std", "GN_long", "EL_std")
CANDIDATE_TELESCOPE_LEFT = ("EL_std",)

EXACT_CHECK_IDS = (
    "P55.inputs.byte_pins_commits_blobs_self_digests_and_corrected_Phase54",
    "P55.roots.three_saved_phi_plus_root_and_endpoint_digests",
    "P55.launch.zero_solve_P50_saddle_pinned_reconstruction_and_identical_initials",
    "P55.evaluators.Phase54_core_bindings_and_Phase53_EL_long_projection",
    "P55.ODE.six_attempt_slot_fraction_and_failure_placeholder_topology",
    "P55.conventions.fixed_sum_Decimal_gates_ordinary_transpose_single_outer_conjugation_and_boundary",
    "P55.reference.direct_global_independence_and_state_lift",
    "P55.guard.validator_scope_historical_immutability_and_global_nulls",
)
NUMERICAL_CHECK_IDS = (
    "P55.reference.thirty_state_80_120_stability",
    "P55.reconstruction.EL_long_saved_Phase53_endpoints_and_residuals",
    "P55.production_states.core_schedule_matrix_vs_direct_120",
    "P55.candidate_states.EL_std_and_EL_long_vs_direct_120",
    "P55.same_point.EL_std_EL_long_blend_and_completed_RHS",
    "P55.trajectory.all_fraction_and_endpoint_state_transfer",
    "P55.residual.candidate_absolute_and_candidate_production_transfer",
    "P55.arithmetic.telescopes_finiteness_solver_completion_and_returned_sample_xi_norm",
)

REFERENCE_THRESHOLD = Decimal("1e-40")
NATIVE_THRESHOLD = Decimal("5e-10")
TELESCOPE_THRESHOLD = Decimal("5e-18")
STATE_THRESHOLD = Decimal("2e-7")
XI_NORM_THRESHOLD = Decimal("40")
SADDLE_GRADIENT_THRESHOLD = Decimal("2e-8")
SADDLE_GAP_THRESHOLD = Decimal("0.1")
SADDLE_HESSIAN_IMAG_THRESHOLD = Decimal("5e-10")
EXPECTED_PROJECTION_SHA256 = (
    "8359762ba056bd7a300bceba8d4bf7e83e22149f5795c37f5b6ee0a4a212ad4e"
)
EXPECTED_PROJECTION_BYTES = 4141
REQUIRED_PHASE54_CLASSIFICATION = (
    "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_"
    "ELEMENT_LOCAL_SCHEDULE_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS"
)
REQUIRED_PHASE53_CLASSIFICATION = (
    "PHI_PLUS_M5_ELEMENT_LOCAL_FULL_CONTINUATION_REPLAY_INCONCLUSIVE"
)
PHASE56_CANDIDATE_BOUNDARY = (
    "The conditional output qualifies only the EL_std state-RHS schedule. "
    "Phase 56 must separately freeze saddle, launch-Hessian, action, "
    "tangent/Hessian, and any full-evaluator backend choices."
)
SUPERSEDED_PHASE54_RESULT_COMMIT = "0ed3d7f"
IDENTITY_KEY = re.compile(
    r"(^id$|(^|_)(python_id|object_id|callable_id|evaluator_identity|"
    r"family_identity|process_local_identity)(_|$))",
    re.IGNORECASE,
)
TEMPORARY_NAME = re.compile(r"^x[0-9]+$")

ALLOWED_SOLVE_IVP = scipy.integrate.solve_ivp


class InvalidRun(RuntimeError):
    """A frozen byte, exact contract, topology, or finite-value gate failed."""


class NonfiniteRun(InvalidRun):
    """An evaluated value was nonfinite and therefore cannot enter JSON."""

    def __init__(
        self,
        message: str,
        *,
        gate_id: str,
        role: str,
        component_index: str,
        dtype: str,
        value_class: str,
    ) -> None:
        super().__init__(message)
        self.details = {
            "finite": False,
            "gate_id": gate_id,
            "role": role,
            "component_index": component_index,
            "dtype": dtype,
            "value_class": value_class,
        }


def progress(message: str) -> None:
    print(f"[Phase55] {message}", file=sys.stderr, flush=True)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require(mapping: Mapping[str, Any], key: str, *, where: str) -> Any:
    if key not in mapping:
        raise InvalidRun(f"missing {where}.{key}")
    return mapping[key]


def exact_decimal(value: Any, *, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise InvalidRun(f"invalid retained decimal at {label}: {value!r}") from error
    if not result.is_finite():
        raise InvalidRun(f"nonfinite retained decimal at {label}")
    return result


def decimal_max(records: Iterable[Mapping[str, Any]], key: str) -> str:
    winner: str | None = None
    maximum: Decimal | None = None
    for record in records:
        text = str(require(record, key, where="decimal maximum record"))
        number = exact_decimal(text, label=key)
        if maximum is None or number > maximum:
            maximum = number
            winner = text
    if winner is None:
        raise InvalidRun(f"empty decimal maximum at {key}")
    return winner


def value_class(value: Any) -> str:
    number = np.asarray(value)
    if np.any(np.isnan(number)):
        return "NaN"
    positive = np.any(np.isposinf(number))
    negative = np.any(np.isneginf(number))
    if positive and not negative:
        return "+Infinity"
    if negative and not positive:
        return "-Infinity"
    return "mixed_nonfinite"


def require_finite_array(
    value: Any,
    *,
    gate_id: str,
    role: str,
) -> np.ndarray:
    array = np.asarray(value)
    mask = ~np.isfinite(array)
    if np.any(mask):
        first = tuple(int(item) for item in np.argwhere(mask)[0])
        raise NonfiniteRun(
            f"nonfinite evaluated value at {role}{first}",
            gate_id=gate_id,
            role=role,
            component_index="/".join(str(item) for item in first),
            dtype=str(array.dtype),
            value_class=value_class(array[mask]),
        )
    return array


def ld_text(value: Any) -> str:
    number = np.longdouble(value)
    if not np.isfinite(number):
        raise NonfiniteRun(
            "cannot serialize nonfinite longdouble",
            gate_id="P55.serialization.finite",
            role="longdouble_serialization",
            component_index="scalar",
            dtype=str(number.dtype),
            value_class=value_class(number),
        )
    text = np.format_float_scientific(
        number, precision=24, unique=False, trim="k"
    )
    rebuilt = np.longdouble(text)
    if rebuilt != number or (
        number == 0 and np.signbit(rebuilt) != np.signbit(number)
    ):
        raise InvalidRun("25-digit longdouble round-trip failed")
    return text


def shortest_ld_text(value: Any) -> str:
    number = np.longdouble(value)
    if not np.isfinite(number):
        raise NonfiniteRun(
            "cannot hash nonfinite reconstructed scalar",
            gate_id="P55.launch.reconstruction_finite",
            role="reconstruction_hash",
            component_index="scalar",
            dtype=str(number.dtype),
            value_class=value_class(number),
        )
    text = np.format_float_scientific(number, unique=True, trim="k")
    rebuilt = np.longdouble(text)
    if rebuilt != number or (
        number == 0 and np.signbit(rebuilt) != np.signbit(number)
    ):
        raise InvalidRun("shortest longdouble round-trip failed")
    return text


def mp_text(value: Any, digits: int = 50) -> str:
    number = mp.mpf(value)
    if not mp.isfinite(number):
        raise NonfiniteRun(
            "cannot serialize nonfinite mpmath value",
            gate_id="P55.serialization.finite",
            role="mpmath_serialization",
            component_index="scalar",
            dtype="mpmath.mpf",
            value_class="NaN" if mp.isnan(number) else ("+Infinity" if number > 0 else "-Infinity"),
        )
    return mp.nstr(number, n=digits, strip_zeros=False)


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        array = require_finite_array(
            value,
            gate_id="P55.serialization.finite",
            role="numpy_array",
        )
        if np.iscomplexobj(array):
            if array.dtype == np.dtype(np.clongdouble):
                return {
                    "shape": list(array.shape),
                    "dtype": str(array.dtype),
                    "clongdouble_decimal_pairs": [
                        [ld_text(item.real), ld_text(item.imag)]
                        for item in array.reshape(-1)
                    ],
                }
            return {
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "numpy_complex_pairs": [
                    [float(item.real), float(item.imag)]
                    for item in array.reshape(-1)
                ],
            }
        if array.dtype == np.dtype(np.longdouble):
            return {
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "longdouble_decimals": [ld_text(item) for item in array.reshape(-1)],
            }
        return [json_ready(item) for item in array.tolist()]
    if isinstance(value, np.clongdouble):
        require_finite_array(
            value,
            gate_id="P55.serialization.finite",
            role="clongdouble_scalar",
        )
        return {
            "clongdouble_decimal_pair": [ld_text(value.real), ld_text(value.imag)]
        }
    if isinstance(value, np.longdouble):
        return {"longdouble_decimal": ld_text(value)}
    if isinstance(value, np.complexfloating):
        require_finite_array(
            value,
            gate_id="P55.serialization.finite",
            role="numpy_complex_scalar",
        )
        return {
            "dtype": str(value.dtype),
            "real": float(value.real),
            "imag": float(value.imag),
        }
    if isinstance(value, np.floating):
        number = float(value)
        if not math.isfinite(number):
            raise NonfiniteRun(
                "nonfinite NumPy float",
                gate_id="P55.serialization.finite",
                role="numpy_float_scalar",
                component_index="scalar",
                dtype=str(value.dtype),
                value_class=value_class(value),
            )
        return number
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, complex):
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise NonfiniteRun(
                "nonfinite Python complex",
                gate_id="P55.serialization.finite",
                role="python_complex_scalar",
                component_index="scalar",
                dtype="complex",
                value_class=value_class(value),
            )
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, mp.mpc):
        if not mp.isfinite(value.real) or not mp.isfinite(value.imag):
            raise NonfiniteRun(
                "nonfinite mpmath complex",
                gate_id="P55.serialization.finite",
                role="mpmath_complex_scalar",
                component_index="scalar",
                dtype="mpmath.mpc",
                value_class="NaN",
            )
        return {
            "mp_decimal_pair": [mp_text(value.real, 50), mp_text(value.imag, 50)]
        }
    if isinstance(value, mp.mpf):
        return {"mp_decimal": mp_text(value, 50)}
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise NonfiniteRun(
                "nonfinite Python float",
                gate_id="P55.serialization.finite",
                role="python_float_scalar",
                component_index="scalar",
                dtype="float",
                value_class=value_class(value),
            )
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise InvalidRun("nonfinite Decimal cannot be serialized")
        return str(value)
    return value


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        json_ready(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    output = dict(payload)
    output.pop("result_payload_sha256_without_self", None)
    output["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(output)
    )
    return output


def verify_self_digest(payload: Mapping[str, Any], *, label: str) -> str:
    key = (
        "result_payload_sha256_without_self"
        if "result_payload_sha256_without_self" in payload
        else "checkpoint_payload_sha256_without_self"
    )
    expected = payload.get(key)
    if not isinstance(expected, str):
        raise InvalidRun(f"{label} lacks a self-excluding digest")
    stripped = dict(payload)
    stripped.pop(key, None)
    observed = sha256_bytes(canonical_bytes(stripped))
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


def reject_numeric_identity_fields(value: Any, pointer: str = "") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            child = f"{pointer}/{key}"
            if IDENTITY_KEY.search(str(key)) and isinstance(
                item, (int, np.integer)
            ) and not isinstance(item, (bool, np.bool_)):
                raise InvalidRun(f"numeric process-local identity field at {child}")
            reject_numeric_identity_fields(item, child)
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            reject_numeric_identity_fields(item, f"{pointer}/{index}")


def parse_unique_json_bytes(path: Path, raw: bytes) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            output[key] = value
        return output

    try:
        payload = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_constant=lambda token: (_ for _ in ()).throw(
                InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InvalidRun(f"strict JSON parse failed for {path.name}: {error}") from error
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")

    def finite_tree(value: Any, pointer: str) -> None:
        if isinstance(value, float) and not math.isfinite(value):
            raise InvalidRun(f"nonfinite parsed JSON number at {pointer}")
        if isinstance(value, Mapping):
            for key, item in value.items():
                finite_tree(item, f"{pointer}/{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                finite_tree(item, f"{pointer}/{index}")

    finite_tree(payload, path.name)
    return payload


def load_unique_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    return parse_unique_json_bytes(path, raw), raw


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def is_ancestor(older: str, newer: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def _pin_commit(specification: Mapping[str, Any], *, where: str) -> str:
    value = specification.get("git_commit", specification.get("commit"))
    if not isinstance(value, str) or not value:
        raise InvalidRun(f"missing {where}.git_commit/commit")
    return value


def committed_blob_guard(relative: str, commit: str) -> dict[str, Any]:
    working_blob = git_output("hash-object", "--", relative)
    committed_blob = git_output("rev-parse", f"{commit}:{relative}")
    if working_blob != committed_blob:
        raise InvalidRun(f"declared commit does not contain working bytes: {relative}")
    return {
        "working_blob_oid": working_blob,
        "committed_blob_oid": committed_blob,
        "commit_blob_matches": True,
    }


def runtime_record() -> dict[str, Any]:
    thread_names = (
        "OPENBLAS_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "BLIS_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "GOTO_NUM_THREADS",
    )
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
        "thread_environment": {name: os.environ.get(name) for name in thread_names},
        "numpy_build_configuration": getattr(np.__config__, "CONFIG", {}),
    }


def validate_runtime(manifest: Mapping[str, Any]) -> dict[str, Any]:
    observed = runtime_record()
    expected = require(manifest, "runtime_contract", where="manifest")
    for key in (
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
    ):
        if str(observed[key]) != str(require(expected, key, where="runtime_contract")):
            raise InvalidRun(
                f"runtime contract drift for {key}: {observed[key]} != {expected[key]}"
            )
    required_environment = require(
        expected, "required_environment", where="runtime_contract"
    )
    drift = {
        str(name): {"expected": str(value), "observed": os.environ.get(str(name))}
        for name, value in required_environment.items()
        if os.environ.get(str(name)) != str(value)
    }
    if drift:
        raise InvalidRun(f"frozen thread environment drift: {drift}")
    return observed


@dataclass
class Contract:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)

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
        status: str,
        statement: str,
        details: Mapping[str, Any] | None = None,
        causal_failure_ids: Sequence[str] | None = None,
    ) -> None:
        if status not in ("PASS", "NONPASS", "NOT_EVALUATED"):
            raise InvalidRun(f"invalid numerical status: {status}")
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "passed": status == "PASS",
            "status": status,
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        if causal_failure_ids:
            record["causal_failure_ids"] = list(causal_failure_ids)
        self.numerical.append(record)


@dataclass
class InputBundle:
    manifest: dict[str, Any]
    manifest_raw: bytes
    observed_runtime: dict[str, Any]
    observed_pins: dict[str, Any]
    loaded_by_path: dict[str, dict[str, Any]]
    consumed_paths: tuple[Path, ...]
    runner_guard: dict[str, Any]

    def json_by_basename(self, basename: str) -> dict[str, Any]:
        matches = [
            payload
            for relative, payload in self.loaded_by_path.items()
            if Path(relative).name == basename
        ]
        unique: list[dict[str, Any]] = []
        for payload in matches:
            if not any(payload == prior for prior in unique):
                unique.append(payload)
        if len(unique) != 1:
            raise InvalidRun(f"expected exactly one loaded JSON named {basename}")
        return unique[0]


def compare_declarations(
    declarations: Mapping[str, list[tuple[str, Mapping[str, Any]]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for relative in sorted(declarations):
        records = declarations[relative]
        commits = {_pin_commit(spec, where=label) for label, spec in records}
        digests = {
            str(require(spec, "sha256", where=label)) for label, spec in records
        }
        sizes = {
            int(spec["size_bytes"])
            for _label, spec in records
            if "size_bytes" in spec
        }
        blobs = {
            str(spec["git_blob_oid"])
            for _label, spec in records
            if "git_blob_oid" in spec
        }
        if len(commits) != 1 or len(digests) != 1 or len(sizes) > 1 or len(blobs) > 1:
            raise InvalidRun(f"cross-manifest pin disagreement: {relative}")
        output.append(
            {
                "path": relative,
                "declaration_roles": [label for label, _spec in records],
                "declaration_count": len(records),
                "commit_equal": True,
                "sha256_equal": True,
                "declared_size_equal_where_present": True,
                "declared_blob_equal_where_present": True,
            }
        )
    return output


def choose_richest_declaration(
    records: Sequence[tuple[str, Mapping[str, Any]]]
) -> tuple[str, Mapping[str, Any]]:
    return max(
        records,
        key=lambda item: (
            "git_blob_oid" in item[1],
            "size_bytes" in item[1],
            "result_payload_sha256_without_self" in item[1],
            "required_schema" in item[1],
        ),
    )


def validate_declared_path(
    label: str,
    specification: Mapping[str, Any],
) -> tuple[dict[str, Any], Path, dict[str, Any] | None]:
    where = f"pin {label}"
    relative = str(require(specification, "path", where=where))
    commit = _pin_commit(specification, where=where)
    expected_sha = str(require(specification, "sha256", where=where))
    path = REPO_ROOT / relative
    if not path.is_file() or REPO_ROOT not in path.resolve().parents:
        raise InvalidRun(f"pinned path is not a repository file: {relative}")
    raw = path.read_bytes()
    observed_sha = sha256_bytes(raw)
    if observed_sha != expected_sha:
        raise InvalidRun(f"pinned SHA drift: {label}")
    if "size_bytes" in specification and len(raw) != int(specification["size_bytes"]):
        raise InvalidRun(f"pinned size drift: {label}")
    payload: dict[str, Any] | None = None
    if path.suffix == ".json":
        payload = parse_unique_json_bytes(path, raw)
        expected_self = specification.get(
            "result_payload_sha256_without_self", specification.get("self_digest")
        )
        if expected_self is not None:
            observed_self = verify_self_digest(payload, label=label)
            if observed_self != str(expected_self):
                raise InvalidRun(f"pinned self digest drift: {label}")
        required_schema = specification.get("required_schema")
        if required_schema is not None and payload.get("schema") != required_schema:
            raise InvalidRun(f"pinned schema drift: {label}")
        required_status = specification.get(
            "required_run_status", specification.get("run_status")
        )
        if required_status is not None and payload.get("run_status") != required_status:
            raise InvalidRun(f"pinned run status drift: {label}")
        required_classification = specification.get(
            "required_classification", specification.get("classification")
        )
        if required_classification is not None and payload.get(
            "classification"
        ) != required_classification:
            raise InvalidRun(f"pinned classification drift: {label}")
    blob = committed_blob_guard(relative, commit)
    expected_blob = specification.get("git_blob_oid")
    if expected_blob is not None and (
        blob["working_blob_oid"] != str(expected_blob)
        or blob["committed_blob_oid"] != str(expected_blob)
    ):
        raise InvalidRun(f"pinned Git blob drift: {label}")
    return (
        {
            "path": relative,
            "commit": commit,
            "sha256": observed_sha,
            "size_bytes": len(raw),
            "git_blob_oid": blob["working_blob_oid"],
            "strict_JSON": payload is not None,
            "self_digest_verified": bool(
                payload is not None
                and (
                    "result_payload_sha256_without_self" in specification
                    or "self_digest" in specification
                )
            ),
            **blob,
        },
        path,
        payload,
    )


def _strict_load_declared_json(specification: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    relative = str(require(specification, "path", where=label))
    path = REPO_ROOT / relative
    raw = path.read_bytes()
    if sha256_bytes(raw) != str(require(specification, "sha256", where=label)):
        raise InvalidRun(f"pre-flatten manifest SHA drift: {label}")
    return parse_unique_json_bytes(path, raw)


def validate_inputs(*, authoritative: bool) -> InputBundle:
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    if len(manifest_raw) != INPUT_SIZE_BYTES:
        raise InvalidRun("Phase55 manifest size drift")
    if sha256_bytes(manifest_raw) != INPUT_SHA256:
        raise InvalidRun("Phase55 manifest SHA drift")
    if (
        manifest.get("schema")
        != "ice-phase55-p53-root-fixed-launch-schedule-transfer-inputs/v1"
        or manifest.get("phase") != 55
        or manifest.get("manifest_introduction_commit")
        != INPUT_INTRODUCTION_COMMIT
    ):
        raise InvalidRun("Phase55 manifest schema/phase/introduction drift")
    checks = require(manifest, "checks", where="manifest")
    if tuple(require(checks, "exact", where="checks")) != EXACT_CHECK_IDS:
        raise InvalidRun("Phase55 exact check ID/order drift")
    if tuple(require(checks, "numerical", where="checks")) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("Phase55 numerical check ID/order drift")
    if not is_ancestor(INPUT_INTRODUCTION_COMMIT, INPUT_COMMIT):
        raise InvalidRun("manifest introduction is not an ancestor of effective commit")
    manifest_relative = str(INPUT_PATH.relative_to(REPO_ROOT))
    manifest_blob = committed_blob_guard(manifest_relative, INPUT_COMMIT)
    if manifest_blob["working_blob_oid"] != INPUT_BLOB_OID:
        raise InvalidRun("Phase55 effective manifest blob drift")
    observed_runtime = validate_runtime(manifest)

    direct = require(manifest, "pinned_inputs", where="manifest")
    if tuple(direct) != ("phase54_manifest", "phase54_runner", "phase54_result"):
        raise InvalidRun("Phase55 top-level pin order drift")
    declarations: dict[str, list[tuple[str, Mapping[str, Any]]]] = {}
    for label, spec in direct.items():
        if not isinstance(spec, Mapping):
            raise InvalidRun(f"invalid top-level pin: {label}")
        relative = str(require(spec, "path", where=f"pinned_inputs.{label}"))
        declarations.setdefault(relative, []).append((label, spec))

    phase54_manifest = _strict_load_declared_json(
        direct["phase54_manifest"], label="phase54_manifest"
    )
    phase54_nested = require(
        phase54_manifest, "pinned_inputs", where="Phase54 manifest"
    )
    for label, spec in phase54_nested.items():
        if not isinstance(spec, Mapping):
            raise InvalidRun(f"invalid Phase54 nested pin: {label}")
        relative = str(require(spec, "path", where=f"Phase54.{label}"))
        declarations.setdefault(relative, []).append((f"Phase54::{label}", spec))

    for manifest_label in ("phase52_manifest", "phase53_manifest"):
        spec = phase54_nested[manifest_label]
        nested_manifest = _strict_load_declared_json(spec, label=manifest_label)
        for label, nested_spec in require(
            nested_manifest, "pinned_inputs", where=manifest_label
        ).items():
            if not isinstance(nested_spec, Mapping):
                raise InvalidRun(f"invalid {manifest_label} nested pin: {label}")
            relative = str(require(nested_spec, "path", where=f"{manifest_label}.{label}"))
            declarations.setdefault(relative, []).append(
                (f"{manifest_label}::{label}", nested_spec)
            )

    duplicate_ledger = compare_declarations(declarations)
    expected_unique = int(
        manifest["pin_validation"][
            "expected_unique_consumed_path_count_after_recursive_flattening"
        ]
    )
    if len(declarations) != expected_unique or expected_unique != 26:
        raise InvalidRun(
            f"recursive pin path count drift: {len(declarations)} != {expected_unique}"
        )
    observed: dict[str, Any] = {}
    loaded_by_path: dict[str, dict[str, Any]] = {}
    consumed: list[Path] = []
    for relative in sorted(declarations):
        label, spec = choose_richest_declaration(declarations[relative])
        record, path, payload = validate_declared_path(label, spec)
        observed[relative] = record
        consumed.append(path)
        if payload is not None:
            loaded_by_path[relative] = payload

    phase54_result = loaded_by_path[
        "cpt_temporal_folded_susy/PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT_RESULT.json"
    ]
    phase54_spec = direct["phase54_result"]
    if (
        phase54_result.get("classification") != REQUIRED_PHASE54_CLASSIFICATION
        or len(phase54_result.get("exact_checks", []))
        != int(phase54_spec["required_exact_check_count"])
        or len(phase54_result.get("numerical_checks", []))
        != int(phase54_spec["required_numerical_check_count"])
        or phase54_result.get("classification_selector_pass_by_core_evaluator")
        != phase54_spec["required_selector_matrix"]
        or _pin_commit(phase54_spec, where="phase54_result")
        == SUPERSEDED_PHASE54_RESULT_COMMIT
    ):
        raise InvalidRun("corrected Phase54 result contract drift")

    required_p53 = manifest["pin_validation"]["required_transitive_phase53"]
    for role, basename in (
        ("manifest", "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_INPUTS.json"),
        ("runner", "phase53_m5_element_local_full_continuation.py"),
        ("result", "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json"),
    ):
        match = [record for relative, record in observed.items() if Path(relative).name == basename]
        if len(match) != 1:
            raise InvalidRun(f"Phase53 transitive {role} path multiplicity drift")
        expected = required_p53[role]
        if any(
            str(match[0][key]) != str(expected[expected_key])
            for key, expected_key in (
                ("commit", "git_commit"),
                ("git_blob_oid", "git_blob_oid"),
                ("sha256", "sha256"),
                ("size_bytes", "size_bytes"),
            )
        ):
            raise InvalidRun(f"Phase53 transitive {role} identity drift")
    phase53_result = next(
        payload
        for relative, payload in loaded_by_path.items()
        if Path(relative).name == "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json"
    )
    if phase53_result.get("classification") != REQUIRED_PHASE53_CLASSIFICATION:
        raise InvalidRun("Phase53 historical classification drift")

    runner_guard: dict[str, Any] = {
        "authoritative": authoritative,
        "manifest_introduction_commit": INPUT_INTRODUCTION_COMMIT,
        "manifest_effective_commit": INPUT_COMMIT,
        "manifest_effective_blob_oid": INPUT_BLOB_OID,
        "manifest_commit_blob_guard": manifest_blob,
        "runner_sha256_at_start": sha256_path(SCRIPT_PATH),
        "runner_commit": None,
        "runner_clean": None,
        "manifest_is_ancestor": None,
        "cross_manifest_declarations": duplicate_ledger,
    }
    if authoritative:
        runner_relative = str(SCRIPT_PATH.relative_to(REPO_ROOT))
        dirty = git_output("status", "--porcelain=v1", "--", runner_relative)
        commit = git_output("log", "-1", "--format=%H", "--", runner_relative)
        if not commit or dirty:
            raise InvalidRun("authoritative Phase55 runner must be committed and clean")
        if commit == INPUT_COMMIT or not is_ancestor(INPUT_COMMIT, commit):
            raise InvalidRun("Phase55 runner commit must descend from effective manifest")
        runner_guard.update(
            {
                "runner_commit": commit,
                "runner_clean": True,
                "manifest_is_ancestor": True,
                "runner_commit_blob_guard": committed_blob_guard(
                    runner_relative, commit
                ),
            }
        )

    return InputBundle(
        manifest=manifest,
        manifest_raw=manifest_raw,
        observed_runtime=observed_runtime,
        observed_pins=observed,
        loaded_by_path=loaded_by_path,
        consumed_paths=tuple(consumed),
        runner_guard=runner_guard,
    )


def post_rehash(bundle: InputBundle) -> dict[str, Any]:
    expected = {
        relative: str(record["sha256"])
        for relative, record in bundle.observed_pins.items()
    }
    expected[str(INPUT_PATH.relative_to(REPO_ROOT))] = INPUT_SHA256
    expected[str(SCRIPT_PATH.relative_to(REPO_ROOT))] = str(
        bundle.runner_guard["runner_sha256_at_start"]
    )
    paths = [*bundle.consumed_paths, INPUT_PATH, SCRIPT_PATH]
    records: list[dict[str, Any]] = []
    for path in paths:
        relative = str(path.relative_to(REPO_ROOT))
        digest = sha256_path(path)
        if digest != expected.get(relative):
            raise InvalidRun(f"post-evaluation byte drift: {relative}")
        records.append(
            {"path": relative, "sha256": digest, "unchanged_after_evaluation": True}
        )
    if len(records) != 28:
        raise InvalidRun("post-rehash path count drift")
    return {"count": len(records), "records": records, "all_unchanged": True}


def pointer_get(payload: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise InvalidRun(f"invalid JSON pointer: {pointer}")
    value = payload
    for raw in pointer.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, Mapping):
            if token not in value:
                raise InvalidRun(f"missing JSON pointer token {token!r} in {pointer}")
            value = value[token]
        elif isinstance(value, list):
            try:
                value = value[int(token)]
            except (ValueError, IndexError) as error:
                raise InvalidRun(f"invalid list token {token!r} in {pointer}") from error
        else:
            raise InvalidRun(f"JSON pointer traversed a scalar: {pointer}")
    return value


def loaded_suffix(bundle: InputBundle, name: str) -> Mapping[str, Any]:
    matches = [
        value
        for path, value in bundle.loaded_by_path.items()
        if Path(path).name == name
    ]
    if len(matches) != 1 or not isinstance(matches[0], Mapping):
        raise InvalidRun(f"expected exactly one loaded {name}")
    return matches[0]


def decode_numpy_complex_pairs(record: Any, *, label: str) -> np.ndarray:
    if not isinstance(record, Mapping):
        array = np.asarray(record)
        return require_finite_array(
            array, gate_id="P55.roots.finite", role=label
        )
    shape = tuple(int(item) for item in require(record, "shape", where=label))
    pairs = np.asarray(
        require(record, "numpy_complex_pairs", where=label), dtype=float
    )
    if pairs.shape != (math.prod(shape), 2):
        raise InvalidRun(f"numpy-complex-pair shape drift at {label}")
    array = (pairs[:, 0] + 1.0j * pairs[:, 1]).reshape(shape)
    return require_finite_array(array, gate_id="P55.roots.finite", role=label)


@dataclass(frozen=True)
class TargetRecord:
    lambda_value: float
    lambda_key: str
    parameters: np.ndarray
    p50_saddle: np.ndarray
    fine_record: Mapping[str, Any]
    intersection_z: np.ndarray
    saved_endpoint_z: np.ndarray
    saved_scaled_residual: str
    declarations: Mapping[str, Any]


def extract_targets(bundle: InputBundle) -> tuple[TargetRecord, ...]:
    contract = require(
        bundle.manifest,
        "saved_root_and_target_contract",
        where="Phase55 manifest",
    )
    if (
        contract.get("source") != SOURCE
        or contract.get("path") != "fine_forward"
        or tuple(contract.get("lambda_order", ())) != LAMBDA_ORDER
        or int(contract.get("root_parameter_count", -1)) != 18
    ):
        raise InvalidRun("saved root contract order/source drift")
    declarations = require(contract, "records", where="saved root contract")
    if not isinstance(declarations, list) or len(declarations) != 3:
        raise InvalidRun("saved root declaration count drift")
    p50 = loaded_suffix(bundle, "PHASE50_M4_M5_JOINT_SADDLE_HOMOTOPY_RESULT.json")
    p53 = loaded_suffix(bundle, "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json")
    output: list[TargetRecord] = []
    for index, (lam, declaration) in enumerate(
        zip(LAMBDA_ORDER, declarations, strict=True)
    ):
        if not isinstance(declaration, Mapping) or float(declaration.get("lambda")) != lam:
            raise InvalidRun(f"target declaration lambda drift at {index}")
        saddle_record = pointer_get(p50, str(declaration["p50_saddle_record_pointer"]))
        saddle_payload = pointer_get(p50, str(declaration["p50_saddle_pointer"]))
        root_payload = pointer_get(p53, str(declaration["root_pointer"]))
        fine = pointer_get(p53, str(declaration["fine_record_pointer"]))
        intersection_payload = pointer_get(
            p53, str(declaration["intersection_state_pointer"])
        )
        residual_payload = pointer_get(
            p53, str(declaration["saved_scaled_residual_pointer"])
        )
        endpoint_payload = pointer_get(p53, str(declaration["saved_endpoint_pointer"]))

        for role, payload, size_key, digest_key in (
            ("p50 saddle", saddle_payload, "p50_saddle_canonical_bytes", "p50_saddle_sha256"),
            ("root", root_payload, "root_canonical_bytes", "root_sha256"),
            (
                "intersection state",
                intersection_payload,
                "intersection_state_canonical_bytes",
                "intersection_state_sha256",
            ),
            (
                "saved endpoint",
                endpoint_payload,
                "saved_endpoint_canonical_bytes",
                "saved_endpoint_sha256",
            ),
        ):
            encoded = canonical_bytes(payload)
            if (
                len(encoded) != int(declaration[size_key])
                or sha256_bytes(encoded) != str(declaration[digest_key])
            ):
                raise InvalidRun(f"{role} subtree digest drift for lambda={lam}")
        if not isinstance(saddle_record, Mapping) or (
            float(saddle_record.get("lambda")) != lam
            or saddle_record.get("accepted") is not True
            or saddle_record.get("finite") is not True
            or saddle_record.get("hessian_inertia")
            != {"negative": 5, "positive": 4, "zero": 0}
        ):
            raise InvalidRun(f"P50 saddle structural drift for lambda={lam}")
        if not isinstance(fine, Mapping) or (
            float(fine.get("lambda")) != lam
            or fine.get("label") != declaration["fine_record_required_label"]
            or fine.get("accepted") is not True
            or fine.get("status") != "PASS"
            or fine.get("parameters") != root_payload
        ):
            raise InvalidRun(f"Phase53 fine record structural drift for lambda={lam}")
        if residual_payload != declaration["saved_scaled_residual_max_abs"]:
            raise InvalidRun(f"saved residual scalar drift for lambda={lam}")
        parameters = require_finite_array(
            np.asarray(root_payload, dtype=float),
            gate_id="P55.roots.finite",
            role=f"lambda={lam}:root",
        )
        saddle = require_finite_array(
            np.asarray(saddle_payload, dtype=float),
            gate_id="P55.roots.finite",
            role=f"lambda={lam}:P50_saddle",
        )
        intersection = decode_numpy_complex_pairs(
            intersection_payload, label=f"lambda={lam}:intersection_z"
        )
        endpoint = decode_numpy_complex_pairs(
            endpoint_payload, label=f"lambda={lam}:saved_endpoint_z"
        )
        if (
            parameters.shape != (18,)
            or saddle.shape != (M5,)
            or intersection.shape != (M5,)
            or endpoint.shape != (M5,)
        ):
            raise InvalidRun(f"target vector shape drift for lambda={lam}")
        output.append(
            TargetRecord(
                lambda_value=lam,
                lambda_key=f"lambda={lam:.1f}",
                parameters=parameters,
                p50_saddle=saddle,
                fine_record=fine,
                intersection_z=np.asarray(intersection, dtype=np.complex128),
                saved_endpoint_z=np.asarray(endpoint, dtype=np.complex128),
                saved_scaled_residual=str(residual_payload),
                declarations=declaration,
            )
        )
    return tuple(output)


@dataclass
class StaticSetup:
    p51: ModuleType
    p52: ModuleType
    p53: ModuleType
    p54: ModuleType
    contexts: tuple[Any, ...]
    context: Any
    evaluators: Mapping[str, Any]
    repaired: Any
    factory: Any
    bindings: Any
    binding_ledger: Mapping[str, Any]
    symbolic_ledger: Mapping[str, Any]
    phase52_result: Mapping[str, Any]
    phase53_result: Mapping[str, Any]


def stable_binding_ledger(
    p52: ModuleType,
    p54: ModuleType,
    bindings: Any,
    evaluator_dimensions: Any,
    historical: Any,
) -> dict[str, Any]:
    ledger: dict[str, Any] = {}
    for dimension_name in ("m4", "m5"):
        dimension = getattr(evaluator_dimensions, dimension_name)
        bound = getattr(bindings, dimension_name)
        historical_set = getattr(historical, dimension_name)
        record = p54.callable_binding_record(
            p52, dimension, bound, SimpleNamespace(evaluator=historical), dimension_name
        )
        # The helper records no numeric ids, but keep the Phase55 policy explicit.
        reject_numeric_identity_fields(record)
        ledger[dimension_name] = record
    return ledger


def build_static_setup(bundle: InputBundle) -> StaticSetup:
    progress("loading pinned Phase51--54 modules and symbolic contexts")
    p51 = load_module("ice_phase51_for_phase55", P51_RUNNER_PATH)
    p52 = load_module("ice_phase52_for_phase55", P52_RUNNER_PATH)
    p53 = load_module("ice_phase53_for_phase55", P53_RUNNER_PATH)
    p54 = load_module("ice_phase54_for_phase55", P54_RUNNER_PATH)
    phase51_manifest = loaded_suffix(
        bundle, "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json"
    )
    phase52_result = loaded_suffix(
        bundle, "PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_RESULT.json"
    )
    phase53_result = loaded_suffix(
        bundle, "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json"
    )
    if hasattr(p51.build_long_evaluator, "cache_clear"):
        p51.build_long_evaluator.cache_clear()
    contexts, context_ledger = p52.build_phase51_contexts(p51, phase51_manifest)
    if [item.label for item in contexts] != ["phi_plus", "phi_minus"]:
        raise InvalidRun("Phase51 context source order drift")
    context = contexts[0]
    if len(context.p50_saddles) != 17 or context._saddle_cache:
        raise InvalidRun("inherited P50 saddle-map/cache topology drift")
    historical = {item.label: item.evaluator for item in contexts}
    evaluators, symbolic_ledger = p52.build_symbolic_evaluators(p51, contexts)
    expected_symbolic = phase52_result.get("symbolic_evaluator_ledger")
    if symbolic_ledger != expected_symbolic:
        raise InvalidRun("Phase52 symbolic evaluator ledger drift")
    all_bindings: dict[str, Any] = {}
    all_binding_ledgers: dict[str, Any] = {}
    for source_label in ("phi_plus", "phi_minus"):
        source_eval = evaluators[source_label]
        bound = p54.SourceBindings(
            source_label=source_label,
            m4=p54.build_dimension_bindings(p52, source_eval.m4),
            m5=p54.build_dimension_bindings(p52, source_eval.m5),
        )
        all_bindings[source_label] = bound
        all_binding_ledgers[source_label] = stable_binding_ledger(
            p52,
            p54,
            bound,
            source_eval,
            historical[source_label],
        )
    source_bindings = all_bindings[SOURCE]
    projection = {
        "source_order": ["phi_plus", "phi_minus"],
        "elements": [
            {
                "source": source_label,
                "m4": p54.element_ledger(all_bindings[source_label].m4.EL_long, p52),
                "m5": p54.element_ledger(all_bindings[source_label].m5.EL_long, p52),
            }
            for source_label in ("phi_plus", "phi_minus")
        ],
    }
    projection_raw = canonical_bytes(projection)
    p53_symbolic = require(
        phase53_result, "symbolic_evaluator_audit", where="Phase53 result"
    )
    expected_projection = {
        "source_order": ["phi_plus", "phi_minus"],
        "elements": [
            {
                "source": source_label,
                "m4": phase52_result["symbolic_evaluator_ledger"][source_label]["elements"]["m4"],
                "m5": phase52_result["symbolic_evaluator_ledger"][source_label]["elements"]["m5"],
            }
            for source_label in ("phi_plus", "phi_minus")
        ],
    }
    if (
        projection != expected_projection
        or projection != p53_symbolic.get("generated_projection")
        or len(projection_raw) != EXPECTED_PROJECTION_BYTES
        or sha256_bytes(projection_raw) != EXPECTED_PROJECTION_SHA256
        or p53_symbolic.get("Phase53_generated_projection_sha256")
        != EXPECTED_PROJECTION_SHA256
        or p53_symbolic.get("Phase52_projection_sha256")
        != EXPECTED_PROJECTION_SHA256
    ):
        raise InvalidRun("Phase53 EL_long projection drift")
    factory = p53.EvaluatorFactory(
        p51, p52, phase52_result, evaluators, historical
    )
    embedding = factory.phase50.build_embedding()
    repaired = factory.build(
        SOURCE,
        context.delta_a,
        context.delta_phi,
        float(context.evaluator.kappa_a),
        float(context.evaluator.kappa_phi),
        np.asarray(embedding.basis, dtype="<f8").tobytes(),
    )
    if repaired is not factory.evaluators[SOURCE]:
        raise InvalidRun("repaired evaluator factory identity drift")
    if not all(
        all(bool(value) for value in plan.exact_identity.values())
        for plan in (factory.plans[SOURCE].m4, factory.plans[SOURCE].m5)
    ):
        raise InvalidRun("Phase53 exact action/gradient/Hessian identity drift")
    for by_dimension in all_binding_ledgers.values():
      for record in by_dimension.values():
        if not (
            record["GN_std"]["actual_historical_joint_plain_callable_bound"]
            and record["GN_std"]["back_substitution"]
            and record["GN_long"]["same_outputs_as_GN_std"]
            and record["GN_long"]["same_DAG_as_GN_std"]
            and record["GN_long"]["back_substitution"]
            and record["EL_std"]["plans_equal_EL_long"]
            and record["EL_std"]["all_generated_sources_distinct_from_EL_long"]
            and all(item["back_substitution"] for item in record["EL_std"]["elements"])
            and all(item["back_substitution"] for item in record["EL_long"]["elements"])
        ):
            raise InvalidRun("Phase54 core evaluator binding drift")
    gradient_identity_binding: dict[str, Any] = {}
    for dimension_name in ("m4", "m5"):
        repaired_gradient_long = getattr(
            factory.plans[SOURCE], dimension_name
        ).gradient_long
        audited_el_long = getattr(source_bindings, dimension_name).EL_long
        object_identity = all(
            left is right
            for left, right in zip(
                repaired_gradient_long, audited_el_long, strict=True
            )
        )
        stable_pairs = [
            {
                "element_index": index,
                "same_callable_object_in_process": left is right,
                "source_sha256": left.source_sha256,
                "dag_sha256": left.dag_sha256,
            }
            for index, (left, right) in enumerate(
                zip(repaired_gradient_long, audited_el_long, strict=True)
            )
        ]
        if not object_identity:
            raise InvalidRun(
                f"P53 EL_long/audit binding object drift at {dimension_name}"
            )
        gradient_identity_binding[dimension_name] = {
            "all_same_callable_objects_in_process": object_identity,
            "stable_element_bindings": stable_pairs,
            "numeric_Python_id_values_serialized": False,
        }
    return StaticSetup(
        p51=p51,
        p52=p52,
        p53=p53,
        p54=p54,
        contexts=tuple(contexts),
        context=context,
        evaluators=evaluators,
        repaired=repaired,
        factory=factory,
        bindings=source_bindings,
        binding_ledger={
            "by_source": all_binding_ledgers,
            "science_source": SOURCE,
            "P53_hot_loop_gradient_identity_binding": gradient_identity_binding,
        },
        symbolic_ledger={
            "phase51_context": context_ledger,
            "phase52": symbolic_ledger,
            "phase53_projection": projection,
            "phase53_projection_sha256": sha256_bytes(projection_raw),
            "phase53_projection_canonical_bytes": len(projection_raw),
            "phase53_exact_identity": {
                "m4": dict(factory.plans[SOURCE].m4.exact_identity),
                "m5": dict(factory.plans[SOURCE].m5.exact_identity),
            },
        },
        phase52_result=phase52_result,
        phase53_result=phase53_result,
    )


@dataclass
class TopologyGuard:
    counters: dict[str, int] = field(
        default_factory=lambda: {
            "scipy_optimize_root": 0,
            "module_root_alias": 0,
            "saddle_cache_hit": 0,
            "saddle_cache_miss": 0,
            "inherited_integrate_k": 0,
            "inherited_solve_ivp": 0,
            "Gamma_K_root_routine": 0,
            "runner_solve_ivp": 0,
            "tangent_ODE": 0,
            "event_integration": 0,
            "continuation_or_replay": 0,
            "finite_difference": 0,
            "reflection": 0,
            "endpoint_mutation": 0,
            "action_or_first_cap": 0,
        }
    )
    restores: list[tuple[Any, str, Any]] = field(default_factory=list)

    def replace(self, owner: Any, name: str, value: Any) -> None:
        if hasattr(owner, name):
            self.restores.append((owner, name, getattr(owner, name)))
            setattr(owner, name, value)

    def raising(self, counter: str, role: str) -> Callable[..., Any]:
        def sentinel(*_args: Any, **_kwargs: Any) -> Any:
            self.counters[counter] += 1
            raise InvalidRun(f"forbidden Phase55 call escaped guard: {role}")

        sentinel.__name__ = f"phase55_forbidden_{role}"
        return sentinel

    def install(self, setup: StaticSetup) -> None:
        original_root = scipy.optimize.root
        self.replace(
            scipy.optimize,
            "root",
            self.raising("scipy_optimize_root", "scipy.optimize.root"),
        )
        candidate_modules: list[ModuleType] = [
            setup.p51,
            setup.p52,
            setup.p53,
            setup.p54,
            setup.factory.phase41,
            setup.factory.phase50,
        ]
        for module in tuple(sys.modules.values()):
            module_file = getattr(module, "__file__", None)
            if not module_file:
                continue
            try:
                in_pinned_tree = Path(module_file).resolve().parent == SCRIPT_PATH.parent
            except (OSError, RuntimeError):
                in_pinned_tree = False
            if in_pinned_tree and module not in candidate_modules:
                candidate_modules.append(module)
        for module in candidate_modules:
            for name, value in tuple(vars(module).items()):
                if value is original_root:
                    self.replace(
                        module,
                        name,
                        self.raising("module_root_alias", f"{module.__name__}.{name}"),
                    )
        for name in ("solve_root", "solve_path"):
            self.replace(
                setup.p51,
                name,
                self.raising("Gamma_K_root_routine", f"phase51.{name}"),
            )
        for name in (
            "finite_difference_jacobian_control",
            "outer_tangent_control",
            "flow_ledger",
            "cse_validation",
            "cse_trajectory_validation",
        ):
            self.replace(
                setup.p51,
                name,
                self.raising("continuation_or_replay", f"phase51.{name}"),
            )
        self.replace(
            setup.p51,
            "reflected_state_distances",
            self.raising("reflection", "phase51.reflected_state_distances"),
        )
        self.replace(
            setup.p51,
            "integrate_k",
            self.raising("inherited_integrate_k", "phase51.integrate_k"),
        )
        self.replace(
            setup.p51,
            "solve_ivp",
            self.raising("inherited_solve_ivp", "phase51.solve_ivp"),
        )
        self.replace(
            scipy.integrate,
            "solve_ivp",
            self.raising("inherited_solve_ivp", "public scipy.integrate.solve_ivp bypass"),
        )
        self.replace(
            setup.repaired,
            "action_only",
            self.raising("action_or_first_cap", "Phase53.repaired.action_only"),
        )
        for dimension_name in ("m4", "m5"):
            self.replace(
                getattr(setup.factory.plans[SOURCE], dimension_name),
                "action_only",
                self.raising(
                    "action_or_first_cap",
                    f"Phase53.{dimension_name}_plan.action_only",
                ),
            )
        original_saddle = setup.p51.SourceContext.saddle

        def cached_saddle(source: Any, lambda_value: float) -> np.ndarray:
            key = round(float(lambda_value), 14)
            if key not in source._saddle_cache:
                self.counters["saddle_cache_miss"] += 1
                raise InvalidRun(f"SourceContext.saddle cache miss at lambda={key}")
            self.counters["saddle_cache_hit"] += 1
            return original_saddle(source, lambda_value)

        self.replace(setup.p51.SourceContext, "saddle", cached_saddle)

    def restore(self) -> None:
        for owner, name, original in reversed(self.restores):
            setattr(owner, name, original)
        self.restores.clear()

    def assert_zero_forbidden(self) -> None:
        allowed_nonzero = {"saddle_cache_hit", "runner_solve_ivp"}
        escaped = {
            key: value
            for key, value in self.counters.items()
            if key not in allowed_nonzero and value != 0
        }
        if escaped:
            raise InvalidRun(f"forbidden-call topology nonzero: {escaped}")


@contextmanager
def guarded_topology(setup: StaticSetup):
    guard = TopologyGuard()
    guard.install(setup)
    try:
        yield guard
    finally:
        guard.restore()


def reconstructed_object_hash(role: str, value: Any) -> dict[str, Any]:
    array = require_finite_array(
        np.asarray(value),
        gate_id="P55.launch.reconstruction_finite",
        role=role,
    )
    if np.iscomplexobj(array):
        components: Any = [
            [shortest_ld_text(item.real), shortest_ld_text(item.imag)]
            for item in np.asarray(array, dtype=np.clongdouble).reshape(-1, order="C")
        ]
        logical_dtype = "clongdouble"
    else:
        components = [
            shortest_ld_text(item)
            for item in np.asarray(array, dtype=np.longdouble).reshape(-1, order="C")
        ]
        logical_dtype = "longdouble"
    payload = {
        "role": role,
        "shape": list(array.shape),
        "logical_dtype": logical_dtype,
        "C_order_scalar_components": components,
    }
    raw = canonical_bytes(payload)
    return {
        "canonical": payload,
        "canonical_bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "raw_x87_storage_hashed": False,
    }


@dataclass
class LaunchRecord:
    target: TargetRecord
    passed: bool
    failure_id: str | None
    fixed_saddle_validation: Mapping[str, Any]
    node: Any | None = None
    omega: np.ndarray | None = None
    initial_xi_long: np.ndarray | None = None
    initial_xi_buffer: np.ndarray | None = None
    initial_state_w5: np.ndarray | None = None
    record: Mapping[str, Any] | None = None


def validate_fixed_saddles(
    setup: StaticSetup, targets: Sequence[TargetRecord]
) -> list[LaunchRecord]:
    if setup.context._saddle_cache:
        raise InvalidRun("saddle cache was populated before Phase55 validation")
    setup.context.evaluator = setup.repaired
    output: list[LaunchRecord] = []
    for target in targets:
        lam = target.lambda_value
        with setup.repaired.mode(
            "gradient_hessian", consumer=f"Phase55.fixed_saddle.lambda={lam:.1f}"
        ):
            _action, gradient, hessian = setup.repaired.evaluate(
                lam, np.asarray(target.p50_saddle, dtype=np.clongdouble)
            )
        gradient = require_finite_array(
            np.asarray(gradient, dtype=np.clongdouble),
            gate_id="P55.launch.fixed_saddle_finite",
            role=f"lambda={lam}:fixed_saddle_gradient",
        )
        hessian = require_finite_array(
            np.asarray(hessian, dtype=np.clongdouble),
            gate_id="P55.launch.fixed_saddle_finite",
            role=f"lambda={lam}:fixed_saddle_Hessian",
        )
        if gradient.shape != (M5,) or hessian.shape != (M5, M5):
            raise InvalidRun(f"fixed-saddle gradient/Hessian shape drift at lambda={lam}")
        real_hessian = np.asarray(hessian.real, dtype=np.longdouble)
        eigenvalues = require_finite_array(
            np.linalg.eigvalsh(np.asarray(real_hessian, dtype=float)),
            gate_id="P55.launch.fixed_saddle_finite",
            role=f"lambda={lam}:fixed_saddle_Hessian_eigenvalues",
        )
        gradient_max = ld_text(np.max(np.abs(gradient)))
        hessian_imag_max = ld_text(np.max(np.abs(hessian.imag)))
        gap = ld_text(np.min(np.abs(eigenvalues)))
        inertia = {
            "negative": int(np.count_nonzero(eigenvalues < 0.0)),
            "positive": int(np.count_nonzero(eigenvalues > 0.0)),
            "zero": int(np.count_nonzero(eigenvalues == 0.0)),
        }
        passed = bool(
            exact_decimal(gradient_max, label="saddle gradient")
            <= SADDLE_GRADIENT_THRESHOLD
            and exact_decimal(gap, label="saddle Hessian gap")
            >= SADDLE_GAP_THRESHOLD
            and exact_decimal(hessian_imag_max, label="saddle Hessian imaginary")
            <= SADDLE_HESSIAN_IMAG_THRESHOLD
            and inertia == {"negative": 5, "positive": 4, "zero": 0}
        )
        failure_id = None if passed else f"reconstruction:lambda={lam:.1f}:fixed_saddle_nonpass"
        output.append(
            LaunchRecord(
                target=target,
                passed=passed,
                failure_id=failure_id,
                fixed_saddle_validation={
                    "source": SOURCE,
                    "lambda": lam,
                    "status": "PASS" if passed else "NONPASS",
                    "finite": True,
                    "gradient_max_abs_decimal": gradient_max,
                    "gradient_max_abs_threshold_decimal": str(SADDLE_GRADIENT_THRESHOLD),
                    "hessian_min_abs_real_eigenvalue_decimal": gap,
                    "hessian_min_abs_eigenvalue_threshold_decimal": str(SADDLE_GAP_THRESHOLD),
                    "hessian_imag_max_abs_decimal": hessian_imag_max,
                    "hessian_imag_max_abs_threshold_decimal": str(SADDLE_HESSIAN_IMAG_THRESHOLD),
                    "hessian_inertia": inertia,
                    "required_inertia": {"negative": 5, "positive": 4, "zero": 0},
                    "eigenvalues": eigenvalues,
                    "failure_id": failure_id,
                },
            )
        )
    if len(output) != 3:
        raise InvalidRun("fixed-saddle validation attempt count drift")
    return output


def reconstruct_launches(
    setup: StaticSetup,
    launches: list[LaunchRecord],
) -> None:
    for launch in launches:
        target = launch.target
        lam = target.lambda_value
        if not launch.passed:
            launch.record = {
                "source": SOURCE,
                "lambda": lam,
                "status": "NOT_EVALUATED",
                "causal_failure_id": launch.failure_id,
                "reason": "fixed_saddle_scientific_nonpass",
            }
            continue
        setup.context._saddle_cache[round(lam, 14)] = target.p50_saddle.copy()
        try:
            flow_time = float(target.parameters[17])
            if not (
                setup.context.bounds.lower[17]
                <= flow_time
                <= setup.context.bounds.upper[17]
            ):
                raise InvalidRun(f"saved flow time left frozen bounds at lambda={lam}")
            with setup.repaired.mode(
                "gradient_hessian", consumer=f"Phase55.launch_Hessian.lambda={lam:.1f}"
            ):
                node = setup.context.node(
                    lam, radius=1.0e-4, shape_key="lambda_1"
                )
            omega, _derivative = setup.context.chart.direction(target.parameters[9:17])
            launch_xi = np.asarray(node.factor_inverse, dtype=np.longdouble) @ np.asarray(
                node.launch_w, dtype=np.clongdouble
            )
            initial_xi = np.clongdouble(node.sphere_radius) * (
                launch_xi @ np.asarray(omega, dtype=np.longdouble)
            )
            initial_w = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.asarray(
                node.factor, dtype=np.longdouble
            ) @ np.asarray(initial_xi, dtype=np.clongdouble)
            initial_z = np.asarray(
                setup.context.scales5, dtype=np.longdouble
            ) * initial_w
            for role, value in (
                ("node.factor", node.factor),
                ("node.launch_w", node.launch_w),
                ("chart.direction", omega),
                ("initial_xi", initial_xi),
                ("initial_state_w5", initial_w),
                ("initial_physical_state_z", initial_z),
            ):
                require_finite_array(
                    value,
                    gate_id="P55.launch.reconstruction_finite",
                    role=f"lambda={lam}:{role}",
                )
            initial_buffer = np.ascontiguousarray(initial_xi, dtype=np.complex128)
            buffer_digest = sha256_bytes(initial_buffer.tobytes(order="C"))
            launch.node = node
            launch.omega = np.asarray(omega, dtype=np.longdouble)
            launch.initial_xi_long = np.asarray(initial_xi, dtype=np.clongdouble)
            launch.initial_xi_buffer = initial_buffer
            launch.initial_state_w5 = initial_w
            launch.record = {
                "source": SOURCE,
                "lambda": lam,
                "status": "PASS",
                "policy": "P50_SADDLE_PINNED_PHASE55_RECONSTRUCTION",
                "radius": 1.0e-4,
                "shape_key": "lambda_1",
                "flow_time": flow_time,
                "exact_Phase53_launch_claim": False,
                "hashes": {
                    "saddle_w": reconstructed_object_hash("saddle_w", node.saddle_w),
                    "factor": reconstructed_object_hash("factor", node.factor),
                    "launch_w": reconstructed_object_hash("launch_w", node.launch_w),
                    "chart_direction": reconstructed_object_hash("chart_direction", omega),
                    "initial_xi": reconstructed_object_hash("initial_xi", initial_xi),
                    "initial_state_w5": reconstructed_object_hash(
                        "initial_state_w5", initial_w
                    ),
                    "initial_physical_state_z": reconstructed_object_hash(
                        "initial_physical_state_z", initial_z
                    ),
                },
                "initial_physical_state_z": initial_z,
                "solver_boundary_initial_xi": {
                    "dtype": str(initial_buffer.dtype),
                    "C_contiguous": bool(initial_buffer.flags.c_contiguous),
                    "byte_count": int(initial_buffer.nbytes),
                    "raw_bytes_sha256": buffer_digest,
                    "single_cast_from_clongdouble": True,
                },
                "node_launch_record": node.launch_record,
            }
        except NonfiniteRun:
            raise
        except InvalidRun:
            raise
        except Exception as error:
            if not isinstance(error, setup.p51.NumericalFailure):
                raise InvalidRun(
                    f"undeclared launch reconstruction exception at lambda={lam}: "
                    f"{type(error).__name__}: {error}"
                ) from error
            launch.passed = False
            launch.failure_id = f"reconstruction:lambda={lam:.1f}:launch_nonpass"
            launch.record = {
                "source": SOURCE,
                "lambda": lam,
                "status": "NONPASS",
                "causal_failure_id": launch.failure_id,
                "exception_type": type(error).__name__,
                "message": str(error),
            }


class ScheduleEvaluator:
    def __init__(self, setup: StaticSetup) -> None:
        self.setup = setup
        self.calls = {backend: 0 for backend in BACKEND_ORDER}

    def dimension_gradient(
        self, backend: str, dimension_name: str, values: np.ndarray
    ) -> np.ndarray:
        if backend not in BACKEND_ORDER:
            raise InvalidRun(f"undeclared schedule backend: {backend}")
        bindings = getattr(self.setup.bindings, dimension_name)
        dimension = int(bindings.dimension)
        callables = bindings.EL_long if backend == "EL_long" else bindings.EL_std
        contributions: list[np.ndarray] = []
        for callable_set in callables:
            raw = self.setup.p52.flatten_raw(callable_set.function(tuple(values)))
            if len(raw) != dimension:
                raise InvalidRun(
                    f"hot-loop output arity drift at {backend}:{dimension_name}"
                )
            raw_array = require_finite_array(
                np.asarray(tuple(raw)),
                gate_id="P55.ODE.RHS_finite",
                role=f"{backend}:{dimension_name}:element_gradient",
            )
            contributions.append(
                np.asarray(
                    raw_array,
                    dtype=np.clongdouble if backend == "EL_long" else np.complex128,
                )
            )
        if backend == "EL_long":
            summed = self.setup.p53.fixed_array_sum(contributions, (dimension,))
            if summed.dtype != np.dtype(np.clongdouble):
                raise InvalidRun("EL_long hot-loop accumulator dtype drift")
        else:
            summed = self.setup.p54.fixed_complex128_sum(contributions, dimension)
            if summed.dtype != np.dtype(np.complex128):
                raise InvalidRun("EL_std hot-loop accumulator dtype drift")
        return np.asarray(summed, dtype=np.clongdouble)

    def stages(self, backend: str, node: Any, state_w5: np.ndarray) -> Mapping[str, np.ndarray]:
        if backend not in BACKEND_ORDER:
            raise InvalidRun(f"undeclared schedule backend: {backend}")
        source = node.source
        inverse = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble)
        coordinates = inverse @ (
            np.asarray(state_w5, dtype=np.clongdouble)
            - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
        )
        state_w4 = np.asarray(source.evaluator.anchor4, dtype=np.clongdouble) + coordinates[:M4]
        gradient4 = self.dimension_gradient(backend, "m4", state_w4)
        gradient5 = self.dimension_gradient(backend, "m5", state_w5)
        slot = self.setup.p52.Slot(
            source=source,
            node=node,
            source_label=SOURCE,
            lambda_value=float(node.lambda_value),
            state_w5=np.asarray(state_w5, dtype=np.clongdouble),
            state_w4=np.asarray(state_w4, dtype=np.clongdouble),
        )
        stages = self.setup.p52.native_stages(slot, gradient4, gradient5)
        if tuple(stages) != STAGE_ORDER:
            raise InvalidRun("hot-loop native stage order drift")
        for stage, dimension in zip(STAGE_ORDER, STAGE_DIMENSIONS, strict=True):
            vector = require_finite_array(
                np.asarray(stages[stage]),
                gate_id="P55.ODE.RHS_finite",
                role=f"{backend}:hot_loop:{stage}",
            )
            if vector.shape != (dimension,) or vector.dtype != np.dtype(np.clongdouble):
                raise InvalidRun(
                    f"hot-loop native stage shape/dtype drift at {backend}:{stage}"
                )
        self.calls[backend] += 1
        return stages

    def rhs(self, backend: str, node: Any, xi: np.ndarray) -> np.ndarray:
        if backend not in BACKEND_ORDER:
            raise InvalidRun(f"undeclared ODE backend: {backend}")
        xi_long = np.asarray(xi, dtype=np.clongdouble)
        state = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.asarray(
            node.factor, dtype=np.longdouble
        ) @ xi_long
        derivative = self.stages(backend, node, state)["outer_minus_conjugation"]
        require_finite_array(
            derivative,
            gate_id="P55.ODE.RHS_finite",
            role=f"{backend}:completed_state_RHS",
        )
        boundary = np.asarray(derivative, dtype=np.complex128)
        require_finite_array(
            boundary,
            gate_id="P55.ODE.RHS_finite",
            role=f"{backend}:complex128_solver_boundary_RHS",
        )
        return boundary


@dataclass
class AttemptResult:
    launch: LaunchRecord
    backend: str
    status: str
    failure_id: str | None
    record: Mapping[str, Any]
    xi_by_fraction: dict[float, np.ndarray]


def run_state_odes(
    launches: Sequence[LaunchRecord],
    evaluator: ScheduleEvaluator,
    guard: TopologyGuard,
) -> list[AttemptResult]:
    attempts: list[AttemptResult] = []
    for launch in launches:
        target = launch.target
        lam = target.lambda_value
        for backend in BACKEND_ORDER:
            attempt_id = f"attempt:lambda={lam:.1f}:{backend}"
            if not launch.passed or launch.node is None or launch.initial_xi_buffer is None:
                failure = str(launch.failure_id)
                attempts.append(
                    AttemptResult(
                        launch=launch,
                        backend=backend,
                        status="NOT_ATTEMPTED_UPSTREAM_RECONSTRUCTION_NONPASS",
                        failure_id=failure,
                        record={
                            "attempt_id": attempt_id,
                            "source": SOURCE,
                            "lambda": lam,
                            "backend": backend,
                            "status": "NOT_ATTEMPTED_UPSTREAM_RECONSTRUCTION_NONPASS",
                            "causal_failure_id": failure,
                            "returned_t_eval_count": 0,
                            "fraction_order": list(FRACTION_ORDER),
                            "fraction_slots": [
                                {
                                    "fraction": fraction,
                                    "state_id": state_key(lam, backend, fraction),
                                    "status": "NOT_EVALUATED",
                                    "causal_failure_id": failure,
                                }
                                for fraction in FRACTION_ORDER
                            ],
                        },
                        xi_by_fraction={},
                    )
                )
                continue
            flow_time = float(target.parameters[17])
            t_eval = np.asarray(FRACTION_ORDER, dtype=float) * flow_time
            if t_eval[0] != 0.0 or t_eval[-1] != flow_time:
                raise InvalidRun(f"t_eval endpoint drift at lambda={lam}")
            before = launch.initial_xi_buffer.tobytes(order="C")
            expected_initial_digest = launch.record["solver_boundary_initial_xi"][
                "raw_bytes_sha256"
            ]
            if sha256_bytes(before) != expected_initial_digest:
                raise InvalidRun("solver-boundary initial-xi digest drift")
            calls_before = dict(evaluator.calls)
            guard.counters["runner_solve_ivp"] += 1
            solution = ALLOWED_SOLVE_IVP(
                lambda _time, xi, backend=backend, node=launch.node: evaluator.rhs(
                    backend, node, xi
                ),
                (0.0, flow_time),
                launch.initial_xi_buffer.copy(),
                method="DOP853",
                rtol=2.0e-10,
                atol=2.0e-12,
                max_step=0.04,
                t_eval=t_eval,
                events=None,
            )
            after = launch.initial_xi_buffer.tobytes(order="C")
            if before != after:
                raise InvalidRun("solve_ivp mutated retained initial-xi buffer")
            returned = int(np.asarray(solution.t).size)
            if returned < 0 or returned > len(FRACTION_ORDER):
                raise InvalidRun("solve_ivp returned invalid t_eval count")
            if not np.array_equal(np.asarray(solution.t), t_eval[:returned]):
                raise InvalidRun("solve_ivp returned a non-prefix t_eval sequence")
            if not solution.success and returned == len(FRACTION_ORDER):
                raise InvalidRun(
                    "failed solve_ivp result cannot retain all five requested samples"
                )
            callback_delta = evaluator.calls[backend] - calls_before[backend]
            other_backend = "EL_std" if backend == "EL_long" else "EL_long"
            if (
                callback_delta != int(solution.nfev)
                or evaluator.calls[other_backend] != calls_before[other_backend]
            ):
                raise InvalidRun(
                    f"ODE callback/nfev binding drift at {attempt_id}: "
                    f"callback_delta={callback_delta}, nfev={solution.nfev}"
                )
            raw_y = np.asarray(solution.y)
            if returned == 0 and raw_y.size == 0:
                raw_y = np.empty((M5, 0), dtype=np.complex128)
            y = require_finite_array(
                raw_y,
                gate_id="P55.ODE.returned_state_finite",
                role=f"{attempt_id}:returned_xi",
            )
            if y.shape != (M5, returned):
                raise InvalidRun(f"solve_ivp returned state shape drift at {attempt_id}")
            xi_by_fraction = {
                fraction: np.asarray(y[:, index], dtype=np.complex128).copy()
                for index, fraction in enumerate(FRACTION_ORDER[:returned])
            }
            norms = [ld_text(np.linalg.norm(np.asarray(xi, dtype=np.clongdouble))) for xi in xi_by_fraction.values()]
            norm_max = None
            if norms:
                norm_max = max(norms, key=lambda text: exact_decimal(text, label="xi norm"))
            success = bool(solution.success and returned == len(FRACTION_ORDER))
            failure_id = None if success else f"{attempt_id}:solver_nonpass"
            fraction_slots = [
                {
                    "fraction": fraction,
                    "state_id": state_key(lam, backend, fraction),
                    "status": "EVALUATED" if index < returned else "NOT_EVALUATED",
                    **(
                        {}
                        if index < returned
                        else {"causal_failure_id": str(failure_id)}
                    ),
                }
                for index, fraction in enumerate(FRACTION_ORDER)
            ]
            attempts.append(
                AttemptResult(
                    launch=launch,
                    backend=backend,
                    status="PASS" if success else "NONPASS",
                    failure_id=failure_id,
                    record={
                        "attempt_id": attempt_id,
                        "source": SOURCE,
                        "lambda": lam,
                        "backend": backend,
                        "status": "PASS" if success else "NONPASS",
                        "failure_id": failure_id,
                        "solver_success": bool(solution.success),
                        "message": str(solution.message),
                        "nfev": int(solution.nfev),
                        "runner_RHS_callback_count_delta": callback_delta,
                        "runner_RHS_callback_count_equals_nfev": True,
                        "njev": int(solution.njev),
                        "nlu": int(solution.nlu),
                        "returned_t_eval_count": returned,
                        "returned_fraction_order": list(FRACTION_ORDER[:returned]),
                        "fraction_slots": fraction_slots,
                        "adaptive_internal_step_count_reported": False,
                        "returned_t_eval_xi_norm_decimals": norms,
                        "returned_t_eval_xi_norm_max_decimal": norm_max,
                        "returned_t_eval_xi_norm_strict_threshold_decimal": str(XI_NORM_THRESHOLD),
                        "returned_t_eval_xi_norm_pass": bool(
                            norm_max is not None
                            and exact_decimal(norm_max, label="xi norm max") < XI_NORM_THRESHOLD
                        ),
                        "method": "DOP853",
                        "rtol": 2.0e-10,
                        "atol": 2.0e-12,
                        "max_step": 0.04,
                        "with_tangent": False,
                        "event": False,
                    },
                    xi_by_fraction=xi_by_fraction,
                )
            )
    if len(attempts) != 6:
        raise InvalidRun("logical ODE attempt count drift")
    successful_launches = sum(launch.passed for launch in launches)
    if guard.counters["runner_solve_ivp"] != 2 * successful_launches:
        raise InvalidRun("runner solve_ivp call-count rule failed")
    if guard.counters["runner_solve_ivp"] not in (0, 2, 4, 6):
        raise InvalidRun("runner solve_ivp count outside allowed set")
    return attempts


def state_key(lam: float, backend: str, fraction: float) -> str:
    return f"state:{SOURCE}:lambda={lam:.1f}:{backend}:fraction={fraction:g}"


def stage_active(stage: str, lam: float) -> bool:
    if stage in ("m4_raw_gradient", "m4_lifted_gradient"):
        return lam != 1.0
    if stage == "m5_raw_gradient":
        return lam != 0.0
    return True


def native_metric(left: Any, right: Any) -> dict[str, Any]:
    a = require_finite_array(
        np.asarray(left, dtype=np.clongdouble),
        gate_id="P55.audit.finite",
        role="native_metric_left",
    ).reshape(-1)
    b = require_finite_array(
        np.asarray(right, dtype=np.clongdouble),
        gate_id="P55.audit.finite",
        role="native_metric_right",
    ).reshape(-1)
    if a.shape != b.shape:
        raise InvalidRun("native comparison shape drift")
    difference = a - b
    numerator = np.linalg.norm(difference)
    denominator = max(
        np.linalg.norm(a), np.linalg.norm(b), np.longdouble("1e-100")
    )
    return {
        "symmetric_relative_decimal": ld_text(numerator / denominator),
        "difference_norm_absolute_decimal": ld_text(numerator),
        "difference_max_component_absolute_decimal": ld_text(
            np.max(np.abs(difference), initial=np.longdouble(0))
        ),
        "difference_vector": difference,
    }


def native_to_mp(value: Any) -> list[mp.mpc]:
    array = require_finite_array(
        np.asarray(value, dtype=np.clongdouble),
        gate_id="P55.audit.finite",
        role="native_to_mp",
    ).reshape(-1)
    return [mp.mpc(ld_text(item.real), ld_text(item.imag)) for item in array]


def mp_metric(left: Sequence[Any], right: Sequence[Any]) -> dict[str, Any]:
    if len(left) != len(right):
        raise InvalidRun("mp comparison length drift")
    a = [mp.mpc(item) for item in left]
    b = [mp.mpc(item) for item in right]
    difference = [x - y for x, y in zip(a, b, strict=True)]
    norm = mp.sqrt(mp.fsum(abs(item) ** 2 for item in difference))
    anorm = mp.sqrt(mp.fsum(abs(item) ** 2 for item in a))
    bnorm = mp.sqrt(mp.fsum(abs(item) ** 2 for item in b))
    relative = norm / max(anorm, bnorm, mp.mpf("1e-100"))
    maximum = max((abs(item) for item in difference), default=mp.mpf("0"))
    return {
        "symmetric_relative_decimal": mp_text(relative),
        "difference_norm_absolute_decimal": mp_text(norm),
        "difference_max_component_absolute_decimal": mp_text(maximum),
        "difference_vector": {
            "shape": [len(difference)],
            "mp_decimal_pairs": [
                [mp_text(item.real, 45), mp_text(item.imag, 45)]
                for item in difference
            ],
        },
    }


def summarize_dimension_call(record: Mapping[str, Any]) -> dict[str, Any]:
    traces = record.get("traces")
    if traces is None:
        traces = [record.get("trace", {})]
    summaries = []
    for trace in traces:
        summaries.append(
            {
                key: trace.get(key)
                for key in (
                    "replacement_count",
                    "traced_temporary_count",
                    "temporary_dtype_counts",
                    "all_temporary_scalars_exact_clongdouble",
                    "raw_output_count",
                    "raw_output_container_type",
                    "raw_output_dtype_counts",
                    "all_raw_scalars_exact_clongdouble",
                    "replacement_names_exact",
                    "return_alias_captured_exactly_once",
                    "source_sha256",
                    "dag_sha256",
                )
            }
        )
    output = {
        "variant": record["variant"],
        "dimension": record["dimension"],
        "complete_raw_gradient_dtype": record["complete_raw_gradient_dtype"],
        "stage_ready_gradient_dtype": record["stage_ready_gradient_dtype"],
        "declared_wrapper_boundary": record["declared_wrapper_boundary"],
        "captured_post_boundary_equals_declared_path": record[
            "captured_post_boundary_equals_declared_path"
        ],
        "trace_summaries": summaries,
    }
    if "element_count" in record:
        output.update(
            {
                "element_count": record["element_count"],
                "fixed_left_to_right_componentwise": record[
                    "fixed_left_to_right_componentwise"
                ],
                "accumulator_dtype": record["accumulator_dtype"],
                "element_plan_bindings": [
                    {
                        "element_index": item["element_index"],
                        "raw_contribution_dtype": item["raw_contribution_dtype"],
                        "accumulator_boundary_dtype": item[
                            "accumulator_boundary_dtype"
                        ],
                        "source_sha256": item["source_sha256"],
                        "dag_sha256": item["dag_sha256"],
                        "replacement_count": item["replacement_count"],
                    }
                    for item in record["element_contributions"]
                ],
            }
        )
    else:
        output.update(
            {
                "raw_joint_output_count": record["raw_joint_output_count"],
                "gradient_slice": record["gradient_slice"],
                "Hessian_slice_retained_but_not_used": record[
                    "Hessian_slice_retained_but_not_used"
                ],
                "raw_joint_decimal_digest": record.get("raw_joint_decimal_digest"),
                "action_side_output_evaluated": record.get(
                    "action_side_output_evaluated", False
                ),
            }
        )
    return output


def audit_global_joint_gradient(
    setup: StaticSetup,
    dimension_name: str,
    bindings: Any,
    values: np.ndarray,
    variant: str,
) -> dict[str, Any]:
    if variant not in ("GN_std", "GN_long"):
        raise InvalidRun(f"undeclared global joint variant: {variant}")
    dimension = int(bindings.dimension)
    callable_set = bindings.GN_std if variant == "GN_std" else bindings.GN_long
    # Phase55 binds directly to the frozen gradient-plus-Hessian function.  It
    # intentionally does not call LongCallableSet.evaluate(..., plain=True),
    # whose historical wrapper evaluates an action side output first.
    raw_call = setup.p54.trace_raw_callable(setup.p52, callable_set, values)
    expected_count = dimension + dimension**2
    if len(raw_call.values) != expected_count:
        raise InvalidRun(f"global joint output-count drift at {variant}:{dimension_name}")
    if variant == "GN_long" and not (
        raw_call.trace["all_temporary_scalars_exact_clongdouble"]
        and raw_call.trace["all_raw_scalars_exact_clongdouble"]
    ):
        raise InvalidRun(f"GN_long raw scalar dtype drift at {dimension_name}")
    post_boundary = require_finite_array(
        np.asarray(raw_call.values, dtype=np.clongdouble),
        gate_id="P55.audit.native_stage_finite",
        role=f"{variant}:{dimension_name}:joint_gradient_Hessian",
    )
    gradient = np.asarray(post_boundary[:dimension], dtype=np.clongdouble)
    raw_digest_payload = {
        "variant": variant,
        "dimension": dimension_name,
        "source_sha256": callable_set.source_sha256,
        "dag_sha256": callable_set.dag_sha256,
        "raw_joint": [
            [ld_text(item.real), ld_text(item.imag)] for item in post_boundary
        ],
    }
    return {
        "variant": variant,
        "dimension": dimension_name,
        "raw_joint_output_count": expected_count,
        "trace": raw_call.trace,
        "complete_raw_gradient_dtype": str(gradient.dtype),
        "stage_ready_gradient": gradient,
        "stage_ready_gradient_dtype": str(gradient.dtype),
        "declared_wrapper_boundary": (
            "direct_bound_GN_std_joint_function_then_complete_np_asarray_clongdouble"
            if variant == "GN_std"
            else "direct_bound_GN_long_joint_function_then_complete_np_asarray_clongdouble"
        ),
        "captured_post_boundary_equals_declared_path": True,
        "gradient_slice": [0, dimension],
        "Hessian_slice_retained_but_not_used": [dimension, expected_count],
        "raw_joint_decimal_digest": sha256_bytes(canonical_bytes(raw_digest_payload)),
        "action_side_output_evaluated": False,
    }


def audit_native_variants(
    setup: StaticSetup,
    node: Any,
    state_w5: np.ndarray,
    variants: Sequence[str],
) -> dict[str, Any]:
    source = node.source
    inverse = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble)
    coordinates = inverse @ (
        np.asarray(state_w5, dtype=np.clongdouble)
        - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
    )
    state_w4 = np.asarray(source.evaluator.anchor4, dtype=np.clongdouble) + coordinates[:M4]
    slot = setup.p52.Slot(
        source=source,
        node=node,
        source_label=SOURCE,
        lambda_value=float(node.lambda_value),
        state_w5=np.asarray(state_w5, dtype=np.clongdouble),
        state_w4=np.asarray(state_w4, dtype=np.clongdouble),
    )
    audit_setup = SimpleNamespace(p52=setup.p52, p53=setup.p53)
    output: dict[str, Any] = {}
    for variant in variants:
        if variant in ("GN_std", "GN_long"):
            call4 = audit_global_joint_gradient(
                setup,
                "m4",
                setup.bindings.m4,
                state_w4,
                variant,
            )
            call5 = audit_global_joint_gradient(
                setup,
                "m5",
                setup.bindings.m5,
                state_w5,
                variant,
            )
        else:
            call4 = setup.p54.evaluate_element_dimension(
                audit_setup, "m4", setup.bindings.m4, state_w4, variant
            )
            call5 = setup.p54.evaluate_element_dimension(
                audit_setup, "m5", setup.bindings.m5, state_w5, variant
            )
        stages = setup.p52.native_stages(
            slot,
            np.asarray(call4["stage_ready_gradient"], dtype=np.clongdouble),
            np.asarray(call5["stage_ready_gradient"], dtype=np.clongdouble),
        )
        if tuple(stages) != STAGE_ORDER:
            raise InvalidRun("sample audit native stage order drift")
        for stage, dimension in zip(STAGE_ORDER, STAGE_DIMENSIONS, strict=True):
            vector = require_finite_array(
                np.asarray(stages[stage]),
                gate_id="P55.audit.native_stage_finite",
                role=f"{variant}:{stage}",
            )
            if vector.shape != (dimension,) or vector.dtype != np.dtype(np.clongdouble):
                raise InvalidRun(f"native stage shape/dtype drift at {variant}:{stage}")
        output[variant] = {
            "m4_call": summarize_dimension_call(call4),
            "m5_call": summarize_dimension_call(call5),
            "stages": stages,
        }
    return output


def direct_reference(
    setup: StaticSetup,
    node: Any,
    state_w5: np.ndarray,
    digits: int,
) -> dict[str, Any]:
    if digits not in (80, 120):
        raise InvalidRun("undeclared direct-reference precision")
    native_state = np.asarray(state_w5)
    if native_state.dtype != np.dtype(np.clongdouble) or native_state.shape != (M5,):
        raise InvalidRun("direct reference requires completed native clongdouble state_w5")
    pairs = [[ld_text(item.real), ld_text(item.imag)] for item in native_state]
    pair_raw = canonical_bytes(pairs)
    with mp.workdps(digits + 30):
        state5 = [mp.mpc(mp.mpf(real), mp.mpf(imag)) for real, imag in pairs]
        source = node.source
        inverse = setup.p52.mp_matrix_real(source.evaluator.inverse_basis_long)
        anchor5 = setup.p52.mp_vector(source.evaluator.anchor5)
        anchor4 = setup.p52.mp_vector(source.evaluator.anchor4)
        coordinates = setup.p52.mp_matvec(
            inverse,
            [state5[index] - anchor5[index] for index in range(M5)],
        )
        state4 = [anchor4[index] + coordinates[index] for index in range(M4)]
        source_eval = setup.evaluators[SOURCE]
        gradient4 = setup.p52.direct_evalf_gradient(
            source_eval.m4.global_gradient,
            source_eval.m4.variables,
            state4,
            digits,
        )
        gradient5 = setup.p52.direct_evalf_gradient(
            source_eval.m5.global_gradient,
            source_eval.m5.variables,
            state5,
            digits,
        )
        gradient_c = [mp.mpc(item) for item in gradient4]
        gradient_c.extend(
            [
                setup.p52.mp_real(source.evaluator.kappa_a) * coordinates[7],
                setup.p52.mp_real(source.evaluator.kappa_phi) * coordinates[8],
            ]
        )
        lifted = setup.p52.mp_matvec(inverse.T, gradient_c)
        lam = setup.p52.mp_real(np.longdouble(node.lambda_value))
        blended = [
            (mp.mpf(1) - lam) * lifted[index] + lam * gradient5[index]
            for index in range(M5)
        ]
        factor = setup.p52.mp_matrix_real(node.factor)
        contracted = setup.p52.mp_matvec(factor.T, blended)
        outer = [-mp.conj(item) for item in contracted]
        stages = {
            "m4_raw_gradient": [mp.mpc(item) for item in gradient4],
            "m4_lifted_gradient": lifted,
            "m5_raw_gradient": [mp.mpc(item) for item in gradient5],
            "lambda_blended_gradient": blended,
            "A_lambda_transpose_contraction": contracted,
            "outer_minus_conjugation": outer,
        }
        return {
            "digits": digits,
            "stages": stages,
            "raw_gradients": {"m4": gradient4, "m5": gradient5},
            "input_lift": {
                "state_w5_25_digit_pairs": pairs,
                "state_w5_decimal_pairs_sha256": sha256_bytes(pair_raw),
                "state_w5_constructed_directly_with_mpf_mpc": True,
                "completed_native_state_w5_consumed": True,
                "raw_xi_consumed": False,
                "scaled_physical_z_consumed": False,
                "native_evaluator_output_consumed": False,
                "NumPy_lambdify_invoked": False,
                "symbolic_CSE_invoked": False,
                "w4_recomputed_entirely_in_mpmath": True,
            },
        }


def telescope_metric(
    left: Any,
    middle: Any,
    reference: Sequence[Any],
) -> dict[str, Any]:
    with mp.workdps(160):
        a = native_to_mp(left)
        b = native_to_mp(middle)
        c = [mp.mpc(item) for item in reference]
        if not (len(a) == len(b) == len(c)):
            raise InvalidRun("telescope vector length drift")
        ab = [x - y for x, y in zip(a, b, strict=True)]
        bc = [x - y for x, y in zip(b, c, strict=True)]
        ac = [x - y for x, y in zip(a, c, strict=True)]
        closure = [x + y - z for x, y, z in zip(ab, bc, ac, strict=True)]
        norm = lambda values: mp.sqrt(mp.fsum(abs(item) ** 2 for item in values))
        closure_norm = norm(closure)
        relative = closure_norm / max(
            norm(ab), norm(bc), norm(ac), mp.mpf("1e-100")
        )
        text = mp_text(relative)
        if exact_decimal(text, label="telescope closure") > TELESCOPE_THRESHOLD:
            raise InvalidRun("evaluated telescope closure exceeded frozen threshold")
        return {
            "closure_relative_decimal": text,
            "closure_norm_absolute_decimal": mp_text(closure_norm),
            "threshold_decimal": str(TELESCOPE_THRESHOLD),
            "passed": True,
            "complete_three_link_chain": True,
        }


@dataclass
class AuditLedger:
    sampled_states: list[dict[str, Any]] = field(default_factory=list)
    native_stage_vectors: list[dict[str, Any]] = field(default_factory=list)
    active_native_comparisons: list[dict[str, Any]] = field(default_factory=list)
    direct_reference_stage_vectors: list[dict[str, Any]] = field(default_factory=list)
    native_to_direct_120_comparisons: list[dict[str, Any]] = field(default_factory=list)
    selectors: list[dict[str, Any]] = field(default_factory=list)
    controlled_contrasts: list[dict[str, Any]] = field(default_factory=list)
    telescopes: list[dict[str, Any]] = field(default_factory=list)
    raw_reference_gradients: list[dict[str, Any]] = field(default_factory=list)


def placeholder(
    role: str,
    state_id: str,
    failure_id: str,
    **fields: Any,
) -> dict[str, Any]:
    return {
        "status": "NOT_EVALUATED",
        "role": role,
        "state_id": state_id,
        "causal_failure_id": failure_id,
        **fields,
    }


def append_state_descendant_placeholders(
    ledger: AuditLedger,
    *,
    state_id_value: str,
    lam: float,
    family: str,
    backend: str,
    fraction: float,
    failure_id: str,
) -> None:
    variants = CORE_ORDER if family == "production" else ("EL_std", "EL_long")
    contrasts = PRODUCTION_CONTRASTS if family == "production" else CANDIDATE_CONTRASTS
    telescope_left = (
        PRODUCTION_TELESCOPE_LEFT if family == "production" else CANDIDATE_TELESCOPE_LEFT
    )
    common = {
        "family": family,
        "source": SOURCE,
        "lambda": lam,
        "trajectory_backend": backend,
        "fraction": fraction,
    }
    for variant in variants:
        for stage in STAGE_ORDER:
            active = stage_active(stage, lam)
            ledger.native_stage_vectors.append(
                placeholder(
                    "native_stage_vector",
                    state_id_value,
                    failure_id,
                    evaluator=variant,
                    stage=stage,
                    active=active,
                    **common,
                )
            )
            if active:
                ledger.active_native_comparisons.append(
                    placeholder(
                        "active_native_to_direct_120_comparison",
                        state_id_value,
                        failure_id,
                        evaluator=variant,
                        stage=stage,
                        active=True,
                        **common,
                    )
                )
            ledger.native_to_direct_120_comparisons.append(
                placeholder(
                    "native_to_direct_120_comparison",
                    state_id_value,
                    failure_id,
                    evaluator=variant,
                    stage=stage,
                    active=active,
                    **common,
                )
            )
        for stage in SELECTOR_STAGES:
            ledger.selectors.append(
                placeholder(
                    "classification_selector",
                    state_id_value,
                    failure_id,
                    evaluator=variant,
                    stage=stage,
                    active=True,
                    **common,
                )
            )
    for digits in (80, 120):
        for dimension in ("m4", "m5"):
            ledger.raw_reference_gradients.append(
                placeholder(
                    "direct_reference_raw_gradient",
                    state_id_value,
                    failure_id,
                    digits=digits,
                    dimension=dimension,
                    active=(lam != 1.0 if dimension == "m4" else lam != 0.0),
                    **common,
                )
            )
        for stage in STAGE_ORDER:
            ledger.direct_reference_stage_vectors.append(
                placeholder(
                    "direct_reference_stage_vector",
                    state_id_value,
                    failure_id,
                    digits=digits,
                    stage=stage,
                    active=stage_active(stage, lam),
                    **common,
                )
            )
    for left, right, mechanism in contrasts:
        for stage in STAGE_ORDER:
            ledger.controlled_contrasts.append(
                placeholder(
                    "controlled_contrast",
                    state_id_value,
                    failure_id,
                    left=left,
                    right=right,
                    mechanism=mechanism,
                    stage=stage,
                    active=stage_active(stage, lam),
                    **common,
                )
            )
    for left in telescope_left:
        for stage in STAGE_ORDER:
            ledger.telescopes.append(
                placeholder(
                    "telescope",
                    state_id_value,
                    failure_id,
                    left=left,
                    middle="EL_long",
                    right="direct_global_120",
                    stage=stage,
                    active=stage_active(stage, lam),
                    **common,
                )
            )


def append_evaluated_state_audit(
    ledger: AuditLedger,
    setup: StaticSetup,
    attempt: AttemptResult,
    fraction: float,
    xi: np.ndarray,
) -> None:
    launch = attempt.launch
    node = launch.node
    if node is None:
        raise InvalidRun("evaluated state lacks launch node")
    lam = launch.target.lambda_value
    family = "production" if attempt.backend == "EL_long" else "candidate"
    sid = state_key(lam, attempt.backend, fraction)
    xi_long = np.asarray(xi, dtype=np.clongdouble)
    state_w5 = require_finite_array(
        np.asarray(node.saddle_w, dtype=np.clongdouble)
        + np.asarray(node.factor, dtype=np.longdouble) @ xi_long,
        gate_id="P55.audit.state_finite",
        role=f"{sid}:state_w5",
    )
    z = require_finite_array(
        np.asarray(node.source.scales5, dtype=np.longdouble) * state_w5,
        gate_id="P55.audit.state_finite",
        role=f"{sid}:physical_z",
    )
    variants = CORE_ORDER if family == "production" else ("EL_std", "EL_long")
    native = audit_native_variants(setup, node, state_w5, variants)
    reference80 = direct_reference(setup, node, state_w5, 80)
    reference120 = direct_reference(setup, node, state_w5, 120)
    common = {
        "family": family,
        "source": SOURCE,
        "lambda": lam,
        "trajectory_backend": attempt.backend,
        "fraction": fraction,
    }
    ledger.sampled_states.append(
        {
            "status": "EVALUATED",
            "role": "sampled_state",
            "state_id": sid,
            **common,
            "xi": xi_long,
            "state_w5": state_w5,
            "physical_state_z": z,
            "state_materialization": "scales5*(saddle_w+factor@xi)",
            "xi_norm_decimal": ld_text(np.linalg.norm(xi_long)),
            "native_evaluator_audit": {
                variant: {
                    "m4_call": native[variant]["m4_call"],
                    "m5_call": native[variant]["m5_call"],
                }
                for variant in variants
            },
            "reference_input_lift": reference120["input_lift"],
        }
    )
    with mp.workdps(160):
        stability_by_stage: dict[str, Mapping[str, Any]] = {}
        for stage in STAGE_ORDER:
            stability = mp_metric(
                reference80["stages"][stage], reference120["stages"][stage]
            )
            if (
                exact_decimal(
                    stability["symmetric_relative_decimal"],
                    label="80/120 reference stability",
                )
                > REFERENCE_THRESHOLD
            ):
                raise InvalidRun(f"direct reference 80/120 instability at {sid}:{stage}")
            stability_by_stage[stage] = stability
        for digits, reference in ((80, reference80), (120, reference120)):
            for stage in STAGE_ORDER:
                stability = stability_by_stage[stage]
                ledger.direct_reference_stage_vectors.append(
                    {
                        "status": "EVALUATED",
                        "role": "direct_reference_stage_vector",
                        "state_id": sid,
                        "digits": digits,
                        "stage": stage,
                        "active": stage_active(stage, lam),
                        "vector": setup.p52.mp_vector_record(
                            reference["stages"][stage], digits=50
                        ),
                        "reference_80_vs_120": stability,
                        "reference_80_vs_120_threshold_decimal": str(REFERENCE_THRESHOLD),
                        "reference_stability_pass": True,
                        **common,
                    }
                )
        for digits, reference in ((80, reference80), (120, reference120)):
            for dimension in ("m4", "m5"):
                ledger.raw_reference_gradients.append(
                    {
                        "status": "EVALUATED",
                        "role": "direct_reference_raw_gradient",
                        "state_id": sid,
                        "digits": digits,
                        "dimension": dimension,
                        "active": (
                            lam != 1.0 if dimension == "m4" else lam != 0.0
                        ),
                        "vector": setup.p52.mp_vector_record(
                            reference["raw_gradients"][dimension], digits=50
                        ),
                        "direct_unreduced_evalf": True,
                        "symbolic_CSE": False,
                        "native_evaluator_invoked": False,
                        **common,
                    }
                )
        for variant in variants:
            for stage in STAGE_ORDER:
                active = stage_active(stage, lam)
                vector = native[variant]["stages"][stage]
                comparison = mp_metric(
                    native_to_mp(vector), reference120["stages"][stage]
                )
                passed = bool(
                    exact_decimal(
                        comparison["symmetric_relative_decimal"],
                        label="native/direct comparison",
                    )
                    <= NATIVE_THRESHOLD
                )
                ledger.native_stage_vectors.append(
                    {
                        "status": "EVALUATED",
                        "role": "native_stage_vector",
                        "state_id": sid,
                        "evaluator": variant,
                        "stage": stage,
                        "active": active,
                        "vector": vector,
                        **common,
                    }
                )
                comparison_record = {
                    "status": "PASS" if passed else "NONPASS",
                    "role": "native_to_direct_120_comparison",
                    "state_id": sid,
                    "evaluator": variant,
                    "stage": stage,
                    "active": active,
                    "threshold_decimal": str(NATIVE_THRESHOLD),
                    "passed": passed,
                    **comparison,
                    **common,
                }
                ledger.native_to_direct_120_comparisons.append(comparison_record)
                if active:
                    ledger.active_native_comparisons.append(
                        {
                            **comparison_record,
                            "role": "active_native_to_direct_120_comparison",
                        }
                    )
                if stage in SELECTOR_STAGES:
                    ledger.selectors.append(
                        {
                            **comparison_record,
                            "role": "classification_selector",
                        }
                    )
        contrasts = (
            PRODUCTION_CONTRASTS if family == "production" else CANDIDATE_CONTRASTS
        )
        for left, right, mechanism in contrasts:
            for stage in STAGE_ORDER:
                comparison = native_metric(
                    native[left]["stages"][stage], native[right]["stages"][stage]
                )
                ledger.controlled_contrasts.append(
                    {
                        "status": "EVALUATED",
                        "role": "controlled_contrast",
                        "state_id": sid,
                        "left": left,
                        "right": right,
                        "mechanism": mechanism,
                        "stage": stage,
                        "active": stage_active(stage, lam),
                        **comparison,
                        **common,
                    }
                )
        telescope_left = (
            PRODUCTION_TELESCOPE_LEFT
            if family == "production"
            else CANDIDATE_TELESCOPE_LEFT
        )
        for left in telescope_left:
            for stage in STAGE_ORDER:
                ledger.telescopes.append(
                    {
                        "status": "PASS",
                        "role": "telescope",
                        "state_id": sid,
                        "left": left,
                        "middle": "EL_long",
                        "right": "direct_global_120",
                        "stage": stage,
                        "active": stage_active(stage, lam),
                        **telescope_metric(
                            native[left]["stages"][stage],
                            native["EL_long"]["stages"][stage],
                            reference120["stages"][stage],
                        ),
                        **common,
                    }
                )


def build_audit_ledger(
    setup: StaticSetup, attempts: Sequence[AttemptResult]
) -> AuditLedger:
    ledger = AuditLedger()
    for attempt in attempts:
        lam = attempt.launch.target.lambda_value
        family = "production" if attempt.backend == "EL_long" else "candidate"
        for fraction in FRACTION_ORDER:
            sid = state_key(lam, attempt.backend, fraction)
            if fraction in attempt.xi_by_fraction:
                append_evaluated_state_audit(
                    ledger,
                    setup,
                    attempt,
                    fraction,
                    attempt.xi_by_fraction[fraction],
                )
            else:
                failure_id = attempt.failure_id or str(attempt.launch.failure_id)
                ledger.sampled_states.append(
                    placeholder(
                        "sampled_state",
                        sid,
                        failure_id,
                        family=family,
                        source=SOURCE,
                        trajectory_backend=attempt.backend,
                        fraction=fraction,
                        **{"lambda": lam},
                    )
                )
                append_state_descendant_placeholders(
                    ledger,
                    state_id_value=sid,
                    lam=lam,
                    family=family,
                    backend=attempt.backend,
                    fraction=fraction,
                    failure_id=failure_id,
                )
    return ledger


def directed_state_metric(candidate: Any, reference: Any) -> dict[str, Any]:
    candidate_array = require_finite_array(
        np.asarray(candidate, dtype=np.clongdouble),
        gate_id="P55.state_transfer.finite",
        role="candidate_state",
    ).reshape(-1)
    reference_array = require_finite_array(
        np.asarray(reference, dtype=np.clongdouble),
        gate_id="P55.state_transfer.finite",
        role="reference_state",
    ).reshape(-1)
    if candidate_array.shape != reference_array.shape:
        raise InvalidRun("state-transfer comparison shape drift")
    difference = candidate_array - reference_array
    norm = np.linalg.norm(difference)
    denominator = max(np.linalg.norm(reference_array), np.longdouble("1e-30"))
    return {
        "relative_decimal": ld_text(norm / denominator),
        "difference_norm_absolute_decimal": ld_text(norm),
        "difference_max_component_absolute_decimal": ld_text(
            np.max(np.abs(difference), initial=np.longdouble(0))
        ),
        "difference_vector": difference,
    }


def materialize_attempt_state(
    attempt: AttemptResult, fraction: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    if fraction not in attempt.xi_by_fraction:
        return None
    node = attempt.launch.node
    if node is None:
        raise InvalidRun("available ODE state lacks launch node")
    xi = np.asarray(attempt.xi_by_fraction[fraction], dtype=np.clongdouble)
    w5 = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.asarray(
        node.factor, dtype=np.longdouble
    ) @ xi
    z = np.asarray(node.source.scales5, dtype=np.longdouble) * w5
    require_finite_array(
        z,
        gate_id="P55.state_transfer.finite",
        role=f"lambda={node.lambda_value}:{attempt.backend}:fraction={fraction}:z",
    )
    return xi, w5, z


@dataclass
class RelationLedger:
    initial_state_identities: list[dict[str, Any]] = field(default_factory=list)
    trajectory_pairs: list[dict[str, Any]] = field(default_factory=list)
    endpoint_pairs: list[dict[str, Any]] = field(default_factory=list)
    scaled_residuals: list[dict[str, Any]] = field(default_factory=list)
    candidate_production_residual_pairs: list[dict[str, Any]] = field(default_factory=list)
    saved_endpoint_reproduction: list[dict[str, Any]] = field(default_factory=list)


def first_missing_failure(*attempts: AttemptResult) -> str:
    for attempt in attempts:
        if attempt.failure_id:
            return attempt.failure_id
        if attempt.launch.failure_id:
            return str(attempt.launch.failure_id)
    raise InvalidRun("missing downstream input has no causal failure ID")


def build_relation_ledger(
    setup: StaticSetup,
    launches: Sequence[LaunchRecord],
    attempts: Sequence[AttemptResult],
) -> RelationLedger:
    output = RelationLedger()
    by_key = {
        (attempt.launch.target.lambda_value, attempt.backend): attempt
        for attempt in attempts
    }
    if len(by_key) != 6:
        raise InvalidRun("attempt index cardinality drift")
    residual_by_key: dict[tuple[float, str], np.ndarray] = {}
    for launch in launches:
        lam = launch.target.lambda_value
        long_attempt = by_key[(lam, "EL_long")]
        std_attempt = by_key[(lam, "EL_std")]
        if launch.passed and launch.initial_xi_buffer is not None:
            retained = launch.initial_xi_buffer.tobytes(order="C")
            digest = sha256_bytes(retained)
            if digest != launch.record["solver_boundary_initial_xi"]["raw_bytes_sha256"]:
                raise InvalidRun("initial-xi retained buffer digest drift")
            output.initial_state_identities.append(
                {
                    "status": "PASS",
                    "role": "initial_state_identity",
                    "source": SOURCE,
                    "lambda": lam,
                    "EL_long_input_sha256": digest,
                    "EL_std_input_sha256": digest,
                    "byte_identical": True,
                    "byte_count": len(retained),
                    "same_C_contiguous_native_complex128_buffer_source": True,
                }
            )
        else:
            output.initial_state_identities.append(
                {
                    "status": "NOT_EVALUATED",
                    "source": SOURCE,
                    "lambda": lam,
                    "role": "initial_state_identity",
                    "causal_failure_id": str(launch.failure_id),
                }
            )

        for fraction in FRACTION_ORDER:
            long_state = materialize_attempt_state(long_attempt, fraction)
            std_state = materialize_attempt_state(std_attempt, fraction)
            if long_state is None or std_state is None:
                output.trajectory_pairs.append(
                    {
                        "status": "NOT_EVALUATED",
                        "role": "backend_paired_fraction",
                        "source": SOURCE,
                        "lambda": lam,
                        "fraction": fraction,
                        "causal_failure_id": first_missing_failure(
                            *(
                                attempt
                                for attempt, state in (
                                    (long_attempt, long_state),
                                    (std_attempt, std_state),
                                )
                                if state is None
                            )
                        ),
                    }
                )
                continue
            comparison = directed_state_metric(std_state[2], long_state[2])
            passed = exact_decimal(
                comparison["relative_decimal"], label="trajectory state transfer"
            ) <= STATE_THRESHOLD
            output.trajectory_pairs.append(
                {
                    "status": "PASS" if passed else "NONPASS",
                    "role": "backend_paired_fraction",
                    "source": SOURCE,
                    "lambda": lam,
                    "fraction": fraction,
                    "threshold_decimal": str(STATE_THRESHOLD),
                    "passed": passed,
                    "compared_physical_z_not_xi": True,
                    **comparison,
                }
            )

        long_endpoint = materialize_attempt_state(long_attempt, 1.0)
        std_endpoint = materialize_attempt_state(std_attempt, 1.0)
        if long_endpoint is None or std_endpoint is None:
            output.endpoint_pairs.append(
                {
                    "status": "NOT_EVALUATED",
                    "role": "endpoint_pair",
                    "source": SOURCE,
                    "lambda": lam,
                    "causal_failure_id": first_missing_failure(
                        *(
                            attempt
                            for attempt, state in (
                                (long_attempt, long_endpoint),
                                (std_attempt, std_endpoint),
                            )
                            if state is None
                        )
                    ),
                }
            )
        else:
            comparison = directed_state_metric(std_endpoint[2], long_endpoint[2])
            passed = exact_decimal(
                comparison["relative_decimal"], label="endpoint transfer"
            ) <= STATE_THRESHOLD
            output.endpoint_pairs.append(
                {
                    "status": "PASS" if passed else "NONPASS",
                    "role": "endpoint_pair",
                    "source": SOURCE,
                    "lambda": lam,
                    "threshold_decimal": str(STATE_THRESHOLD),
                    "passed": passed,
                    **comparison,
                }
            )

        if long_endpoint is None:
            output.saved_endpoint_reproduction.append(
                {
                    "status": "NOT_EVALUATED",
                    "source": SOURCE,
                    "lambda": lam,
                    "role": "EL_long_saved_Phase53_endpoint_reproduction",
                    "causal_failure_id": first_missing_failure(long_attempt),
                }
            )
        else:
            comparison = directed_state_metric(
                long_endpoint[2], launch.target.saved_endpoint_z
            )
            passed = exact_decimal(
                comparison["relative_decimal"], label="saved endpoint reproduction"
            ) <= STATE_THRESHOLD
            output.saved_endpoint_reproduction.append(
                {
                    "status": "PASS" if passed else "NONPASS",
                    "source": SOURCE,
                    "lambda": lam,
                    "role": "EL_long_saved_Phase53_endpoint_reproduction",
                    "threshold_decimal": str(STATE_THRESHOLD),
                    "passed": passed,
                    "saved_endpoint_z": launch.target.saved_endpoint_z,
                    **comparison,
                }
            )

        cap_state, _cap_tangent = setup.p51.gamma_cap(
            setup.context, launch.target.parameters[:9]
        )
        for backend, attempt, endpoint in (
            ("EL_long", long_attempt, long_endpoint),
            ("EL_std", std_attempt, std_endpoint),
        ):
            if endpoint is None:
                output.scaled_residuals.append(
                    {
                        "status": "NOT_EVALUATED",
                        "role": "scaled_residual",
                        "source": SOURCE,
                        "lambda": lam,
                        "backend": backend,
                        "causal_failure_id": first_missing_failure(attempt),
                    }
                )
                continue
            scaled_complex = (
                np.asarray(cap_state, dtype=np.complex128)
                - np.asarray(endpoint[2], dtype=np.complex128)
            ) / np.asarray(setup.context.scales5, dtype=float)
            residual = require_finite_array(
                setup.p51.interleaved(scaled_complex),
                gate_id="P55.residual.finite",
                role=f"lambda={lam}:{backend}:scaled_residual",
            )
            maximum = ld_text(np.max(np.abs(np.asarray(residual, dtype=np.longdouble))))
            absolute_pass = exact_decimal(
                maximum, label="scaled residual maximum"
            ) <= STATE_THRESHOLD
            record: dict[str, Any] = {
                "status": "PASS" if absolute_pass else "NONPASS",
                "role": "scaled_residual",
                "source": SOURCE,
                "lambda": lam,
                "backend": backend,
                "residual_vector_interleaved": residual,
                "residual_max_abs_decimal": maximum,
                "absolute_threshold_decimal": str(STATE_THRESHOLD),
                "absolute_pass": absolute_pass,
                "construction": "interleaved((gamma_cap(parameters[:9])[0]-z_endpoint)/scales5)",
            }
            if backend == "EL_long":
                saved = exact_decimal(
                    launch.target.saved_scaled_residual,
                    label="saved scaled residual",
                )
                difference = abs(exact_decimal(maximum, label="residual") - saved)
                difference_text = str(difference)
                saved_pass = difference <= STATE_THRESHOLD
                record.update(
                    {
                        "saved_Phase53_scaled_residual_max_abs_decimal": launch.target.saved_scaled_residual,
                        "saved_scalar_absolute_difference_decimal": difference_text,
                        "saved_scalar_difference_threshold_decimal": str(STATE_THRESHOLD),
                        "saved_scalar_pass": saved_pass,
                        "status": "PASS" if absolute_pass and saved_pass else "NONPASS",
                    }
                )
            output.scaled_residuals.append(record)
            residual_by_key[(lam, backend)] = np.asarray(residual, dtype=float)

        if (lam, "EL_long") not in residual_by_key or (lam, "EL_std") not in residual_by_key:
            output.candidate_production_residual_pairs.append(
                {
                    "status": "NOT_EVALUATED",
                    "role": "candidate_production_scaled_residual_difference",
                    "source": SOURCE,
                    "lambda": lam,
                    "causal_failure_id": first_missing_failure(
                        *(
                            attempt
                            for backend, attempt in (
                                ("EL_long", long_attempt),
                                ("EL_std", std_attempt),
                            )
                            if (lam, backend) not in residual_by_key
                        )
                    ),
                }
            )
        else:
            difference = np.abs(
                residual_by_key[(lam, "EL_std")]
                - residual_by_key[(lam, "EL_long")]
            )
            maximum = ld_text(np.max(np.asarray(difference, dtype=np.longdouble)))
            passed = exact_decimal(
                maximum, label="candidate/production residual difference"
            ) <= STATE_THRESHOLD
            output.candidate_production_residual_pairs.append(
                {
                    "status": "PASS" if passed else "NONPASS",
                    "role": "candidate_production_scaled_residual_difference",
                    "source": SOURCE,
                    "lambda": lam,
                    "difference_vector_absolute": difference,
                    "difference_max_abs_decimal": maximum,
                    "threshold_decimal": str(STATE_THRESHOLD),
                    "passed": passed,
                }
            )
    if not (
        len(output.initial_state_identities) == 3
        and len(output.trajectory_pairs) == 15
        and len(output.endpoint_pairs) == 3
        and len(output.scaled_residuals) == 6
        and len(output.candidate_production_residual_pairs) == 3
        and len(output.saved_endpoint_reproduction) == 3
    ):
        raise InvalidRun("relation ledger topology drift")
    return output


LEDGER_COUNT_KEYS = {
    "sampled_states": "total_sampled_state_or_failure_placeholder_count",
    "native_stage_vectors": "native_stage_vector_or_placeholder_record_count",
    "active_native_comparisons": "active_native_stage_comparison_or_placeholder_record_count",
    "direct_reference_stage_vectors": "direct_reference_stage_vector_or_placeholder_record_count_80_and_120_combined",
    "native_to_direct_120_comparisons": "native_to_direct_120_comparison_or_placeholder_record_count",
    "selectors": "selector_or_placeholder_record_count",
    "controlled_contrasts": "controlled_contrast_or_placeholder_record_count",
    "telescopes": "telescope_or_placeholder_record_count",
    "raw_reference_gradients": "direct_reference_raw_gradient_evaluation_or_placeholder_record_count",
}


def count_audit_ledger(
    manifest: Mapping[str, Any], ledger: AuditLedger
) -> dict[str, Any]:
    expected_contract = require(
        manifest, "expected_audit_counts", where="Phase55 manifest"
    )
    expected: dict[str, int] = {}
    actual: dict[str, int] = {}
    evaluated: dict[str, int] = {}
    placeholders: dict[str, int] = {}
    for attribute, manifest_key in LEDGER_COUNT_KEYS.items():
        records = getattr(ledger, attribute)
        expected[attribute] = int(expected_contract[manifest_key])
        actual[attribute] = len(records)
        evaluated[attribute] = sum(
            record.get("status") != "NOT_EVALUATED" for record in records
        )
        placeholders[attribute] = sum(
            record.get("status") == "NOT_EVALUATED" for record in records
        )
        if actual[attribute] != expected[attribute]:
            raise InvalidRun(
                f"fixed audit ledger count drift for {attribute}: "
                f"{actual[attribute]} != {expected[attribute]}"
            )
        if evaluated[attribute] + placeholders[attribute] != actual[attribute]:
            raise InvalidRun(f"audit evaluated/placeholder partition drift at {attribute}")
    production_states = sum(
        item.get("status") == "EVALUATED" and item.get("family") == "production"
        for item in ledger.sampled_states
    )
    candidate_states = sum(
        item.get("status") == "EVALUATED" and item.get("family") == "candidate"
        for item in ledger.sampled_states
    )
    relations = {
        "native_stage_vectors": 24 * production_states + 12 * candidate_states,
        "native_to_direct_120_comparisons": 24 * production_states
        + 12 * candidate_states,
        "direct_reference_stage_vectors": 12
        * (production_states + candidate_states),
        "selectors": 8 * production_states + 4 * candidate_states,
        "controlled_contrasts": 24 * production_states + 6 * candidate_states,
        "telescopes": 18 * production_states + 6 * candidate_states,
        "raw_reference_gradients": 4 * (production_states + candidate_states),
        "sampled_states": production_states + candidate_states,
    }
    for key, expected_evaluated in relations.items():
        if evaluated[key] != expected_evaluated:
            raise InvalidRun(
                f"evaluated-count relation drift at {key}: "
                f"{evaluated[key]} != {expected_evaluated}"
            )
    active_from_native = sum(
        record.get("status") != "NOT_EVALUATED" and record.get("active") is True
        for record in ledger.native_stage_vectors
    )
    if evaluated["active_native_comparisons"] != active_from_native:
        raise InvalidRun("active native comparison evaluated-count relation drift")
    return {
        "expected": expected,
        "actual": actual,
        "evaluated": evaluated,
        "placeholders": placeholders,
        "production_evaluated_sampled_states": production_states,
        "candidate_evaluated_sampled_states": candidate_states,
        "exact_fixed_slot_match": True,
        "evaluated_count_relations_passed": True,
    }


def assert_actual_key_sequences(
    ledger: AuditLedger,
    relations: RelationLedger,
    preenumeration: Mapping[str, Any],
    attempts: Sequence[AttemptResult],
    launches: Sequence[LaunchRecord],
) -> dict[str, Any]:
    def lam_text(record: Mapping[str, Any]) -> str:
        return f"lambda={float(record['lambda']):.1f}"

    actual_audit: dict[str, list[str]] = {
        "sampled_states": [str(record["state_id"]) for record in ledger.sampled_states],
        "native_stage_vectors": [
            f"{record['state_id']}:{record['evaluator']}:{record['stage']}"
            for record in ledger.native_stage_vectors
        ],
        "active_native_comparisons": [
            f"{record['state_id']}:{record['evaluator']}:{record['stage']}"
            for record in ledger.active_native_comparisons
        ],
        "direct_reference_stage_vectors": [
            f"{record['state_id']}:{record['digits']}:{record['stage']}"
            for record in ledger.direct_reference_stage_vectors
        ],
        "native_to_direct_120_comparisons": [
            f"{record['state_id']}:{record['evaluator']}:{record['stage']}"
            for record in ledger.native_to_direct_120_comparisons
        ],
        "selectors": [
            f"{record['state_id']}:{record['evaluator']}:{record['stage']}"
            for record in ledger.selectors
        ],
        "controlled_contrasts": [
            f"{record['state_id']}:{record['left']}->{record['right']}:"
            f"{record['mechanism']}:{record['stage']}"
            for record in ledger.controlled_contrasts
        ],
        "telescopes": [
            f"{record['state_id']}:{record['left']}->{record['middle']}->"
            f"{record['right']}:{record['stage']}"
            for record in ledger.telescopes
        ],
        "raw_reference_gradients": [
            f"{record['state_id']}:{record['digits']}:{record['dimension']}"
            for record in ledger.raw_reference_gradients
        ],
    }
    actual_relations = {
        "initial_state_identities": [
            lam_text(record) for record in relations.initial_state_identities
        ],
        "trajectory_pairs": [
            f"{lam_text(record)}:fraction={float(record['fraction']):g}"
            for record in relations.trajectory_pairs
        ],
        "endpoint_pairs": [lam_text(record) for record in relations.endpoint_pairs],
        "scaled_residuals": [
            f"{lam_text(record)}:{record['backend']}"
            for record in relations.scaled_residuals
        ],
        "candidate_production_residual_pairs": [
            lam_text(record)
            for record in relations.candidate_production_residual_pairs
        ],
        "saved_endpoint_reproduction": [
            lam_text(record) for record in relations.saved_endpoint_reproduction
        ],
    }
    expected_payload = preenumeration["payload"]
    expected_audit = expected_payload["audit_ledger_keys"]
    expected_relations = expected_payload["relation_ledger_keys"]
    role_by_ledger = {
        "sampled_states": "sampled_state",
        "native_stage_vectors": "native_stage_vector",
        "active_native_comparisons": "active_native_to_direct_120_comparison",
        "direct_reference_stage_vectors": "direct_reference_stage_vector",
        "native_to_direct_120_comparisons": "native_to_direct_120_comparison",
        "selectors": "classification_selector",
        "controlled_contrasts": "controlled_contrast",
        "telescopes": "telescope",
        "raw_reference_gradients": "direct_reference_raw_gradient",
    }
    for key, actual_keys in actual_audit.items():
        if actual_keys != list(expected_audit[key]):
            mismatch = next(
                (
                    index
                    for index, (actual, expected) in enumerate(
                        zip(actual_keys, expected_audit[key], strict=False)
                    )
                    if actual != expected
                ),
                min(len(actual_keys), len(expected_audit[key])),
            )
            raise InvalidRun(f"canonical audit key/order drift at {key}[{mismatch}]")
        if len(actual_keys) != len(set(actual_keys)):
            raise InvalidRun(f"duplicate canonical audit key at {key}")
        records = getattr(ledger, key)
        if any(record.get("role") != role_by_ledger[key] for record in records):
            raise InvalidRun(f"audit role drift at {key}")
        if any("lambda" not in record for record in records):
            raise InvalidRun(f"audit lambda-key drift at {key}")
    for key, actual_keys in actual_relations.items():
        if actual_keys != list(expected_relations[key]):
            raise InvalidRun(f"canonical relation key/order drift at {key}")
        if len(actual_keys) != len(set(actual_keys)):
            raise InvalidRun(f"duplicate canonical relation key at {key}")
    relation_roles = {
        "initial_state_identities": "initial_state_identity",
        "trajectory_pairs": "backend_paired_fraction",
        "endpoint_pairs": "endpoint_pair",
        "scaled_residuals": "scaled_residual",
        "candidate_production_residual_pairs": "candidate_production_scaled_residual_difference",
        "saved_endpoint_reproduction": "EL_long_saved_Phase53_endpoint_reproduction",
    }
    for key, expected_role in relation_roles.items():
        if any(
            record.get("role") != expected_role
            for record in getattr(relations, key)
        ):
            raise InvalidRun(f"canonical relation role drift at {key}")
    for records in (
        ledger.native_stage_vectors,
        ledger.active_native_comparisons,
        ledger.direct_reference_stage_vectors,
        ledger.native_to_direct_120_comparisons,
        ledger.selectors,
        ledger.controlled_contrasts,
        ledger.telescopes,
        ledger.raw_reference_gradients,
    ):
        if any(not isinstance(record.get("active"), bool) for record in records):
            raise InvalidRun("activity flag missing or non-boolean in canonical ledger")

    attempt_by_key = {
        (attempt.launch.target.lambda_value, attempt.backend): attempt
        for attempt in attempts
    }
    launch_by_lambda = {
        launch.target.lambda_value: launch for launch in launches
    }
    if len(attempt_by_key) != 6 or len(launch_by_lambda) != 3:
        raise InvalidRun("semantic ledger validation attempt/launch index drift")
    state_metadata = {
        state_key(lam, backend, fraction): {
            "lambda": lam,
            "trajectory_backend": backend,
            "family": "production" if backend == "EL_long" else "candidate",
            "fraction": fraction,
        }
        for lam in LAMBDA_ORDER
        for backend in BACKEND_ORDER
        for fraction in FRACTION_ORDER
    }

    def require_exact_state_context(record: Mapping[str, Any], *, ledger_name: str) -> Mapping[str, Any]:
        state_id_value = record.get("state_id")
        if state_id_value not in state_metadata:
            raise InvalidRun(f"undeclared state_id in {ledger_name}: {state_id_value!r}")
        metadata = state_metadata[str(state_id_value)]
        if (
            record.get("source") != SOURCE
            or type(record.get("lambda")) is not float
            or record.get("lambda") != metadata["lambda"]
            or record.get("trajectory_backend") != metadata["trajectory_backend"]
            or record.get("family") != metadata["family"]
            or type(record.get("fraction")) is not float
            or record.get("fraction") != metadata["fraction"]
        ):
            raise InvalidRun(f"state context field drift in {ledger_name}:{state_id_value}")
        return metadata

    def expected_state_failure(metadata: Mapping[str, Any]) -> str | None:
        attempt = attempt_by_key[
            (float(metadata["lambda"]), str(metadata["trajectory_backend"]))
        ]
        if float(metadata["fraction"]) in attempt.xi_by_fraction:
            return None
        failure_id = attempt.failure_id or attempt.launch.failure_id
        if not isinstance(failure_id, str) or not failure_id:
            raise InvalidRun("unavailable state has no exact upstream failure ID")
        return failure_id

    def require_exact_placeholder_cause(
        record: Mapping[str, Any], expected_failure: str | None, *, role: str
    ) -> None:
        if expected_failure is None:
            if record.get("status") == "NOT_EVALUATED" or record.get(
                "causal_failure_id"
            ) is not None:
                raise InvalidRun(f"available {role} was replaced by a placeholder")
        elif (
            record.get("status") != "NOT_EVALUATED"
            or record.get("causal_failure_id") != expected_failure
        ):
            raise InvalidRun(f"{role} placeholder cause differs from upstream failure")

    audit_domains = {
        "sampled_states": {"EVALUATED", "NOT_EVALUATED"},
        "native_stage_vectors": {"EVALUATED", "NOT_EVALUATED"},
        "active_native_comparisons": {"PASS", "NONPASS", "NOT_EVALUATED"},
        "direct_reference_stage_vectors": {"EVALUATED", "NOT_EVALUATED"},
        "native_to_direct_120_comparisons": {"PASS", "NONPASS", "NOT_EVALUATED"},
        "selectors": {"PASS", "NONPASS", "NOT_EVALUATED"},
        "controlled_contrasts": {"EVALUATED", "NOT_EVALUATED"},
        "telescopes": {"PASS", "NOT_EVALUATED"},
        "raw_reference_gradients": {"EVALUATED", "NOT_EVALUATED"},
    }
    for ledger_name in LEDGER_COUNT_KEYS:
        for record in getattr(ledger, ledger_name):
            metadata = require_exact_state_context(record, ledger_name=ledger_name)
            if record.get("status") not in audit_domains[ledger_name]:
                raise InvalidRun(f"status-domain drift in {ledger_name}")
            expected_failure = expected_state_failure(metadata)
            require_exact_placeholder_cause(
                record, expected_failure, role=ledger_name
            )
            family = str(metadata["family"])
            lam = float(metadata["lambda"])
            allowed_evaluators = (
                CORE_ORDER if family == "production" else ("EL_std", "EL_long")
            )
            if ledger_name in (
                "native_stage_vectors",
                "active_native_comparisons",
                "native_to_direct_120_comparisons",
                "selectors",
            ) and record.get("evaluator") not in allowed_evaluators:
                raise InvalidRun(f"evaluator-domain drift in {ledger_name}")
            if ledger_name in (
                "native_stage_vectors",
                "active_native_comparisons",
                "direct_reference_stage_vectors",
                "native_to_direct_120_comparisons",
                "selectors",
                "controlled_contrasts",
                "telescopes",
            ):
                stage = record.get("stage")
                if stage not in STAGE_ORDER:
                    raise InvalidRun(f"stage-domain drift in {ledger_name}")
                if record.get("active") is not stage_active(str(stage), lam):
                    raise InvalidRun(f"stage activity drift in {ledger_name}")
                if ledger_name == "active_native_comparisons" and record.get(
                    "active"
                ) is not True:
                    raise InvalidRun("inactive stage entered active comparison ledger")
            if ledger_name == "selectors" and record.get("stage") not in SELECTOR_STAGES:
                raise InvalidRun("selector stage-domain drift")
            if ledger_name == "direct_reference_stage_vectors" and record.get(
                "digits"
            ) not in (80, 120):
                raise InvalidRun("direct-reference precision-tier drift")
            if ledger_name == "raw_reference_gradients":
                dimension = record.get("dimension")
                if record.get("digits") not in (80, 120) or dimension not in (
                    "m4",
                    "m5",
                ):
                    raise InvalidRun("raw-reference tier/dimension drift")
                expected_activity = lam != 1.0 if dimension == "m4" else lam != 0.0
                if record.get("active") is not expected_activity:
                    raise InvalidRun("raw-reference dimension activity drift")
            if ledger_name == "controlled_contrasts":
                allowed_contrasts = (
                    PRODUCTION_CONTRASTS
                    if family == "production"
                    else CANDIDATE_CONTRASTS
                )
                if (
                    record.get("left"),
                    record.get("right"),
                    record.get("mechanism"),
                ) not in allowed_contrasts:
                    raise InvalidRun("controlled-contrast domain drift")
            if ledger_name == "telescopes":
                allowed_left = (
                    PRODUCTION_TELESCOPE_LEFT
                    if family == "production"
                    else CANDIDATE_TELESCOPE_LEFT
                )
                if (
                    record.get("left") not in allowed_left
                    or record.get("middle") != "EL_long"
                    or record.get("right") != "direct_global_120"
                ):
                    raise InvalidRun("telescope-chain domain drift")

    def exact_attempt_failure(lam: float, backend: str, fraction: float) -> str | None:
        attempt = attempt_by_key[(lam, backend)]
        if fraction in attempt.xi_by_fraction:
            return None
        failure_id = attempt.failure_id or attempt.launch.failure_id
        if not isinstance(failure_id, str) or not failure_id:
            raise InvalidRun("relation prerequisite lacks upstream failure ID")
        return failure_id

    def first_missing_backend_failure(lam: float, fraction: float) -> str | None:
        for backend in BACKEND_ORDER:
            failure_id = exact_attempt_failure(lam, backend, fraction)
            if failure_id is not None:
                return failure_id
        return None

    for relation_name in relation_roles:
        for record in getattr(relations, relation_name):
            if (
                record.get("source") != SOURCE
                or type(record.get("lambda")) is not float
                or record.get("lambda") not in LAMBDA_ORDER
            ):
                raise InvalidRun(f"relation source/lambda drift in {relation_name}")
            lam = float(record["lambda"])
            if relation_name == "initial_state_identities":
                launch = launch_by_lambda[lam]
                expected_failure = None if launch.passed else launch.failure_id
            elif relation_name == "trajectory_pairs":
                if type(record.get("fraction")) is not float or record.get(
                    "fraction"
                ) not in FRACTION_ORDER:
                    raise InvalidRun("trajectory-pair fraction drift")
                expected_failure = first_missing_backend_failure(
                    lam, float(record["fraction"])
                )
            elif relation_name == "endpoint_pairs":
                expected_failure = first_missing_backend_failure(lam, 1.0)
            elif relation_name == "scaled_residuals":
                backend = record.get("backend")
                if backend not in BACKEND_ORDER:
                    raise InvalidRun("scaled-residual backend drift")
                expected_failure = exact_attempt_failure(lam, str(backend), 1.0)
            elif relation_name == "candidate_production_residual_pairs":
                expected_failure = first_missing_backend_failure(lam, 1.0)
            else:
                expected_failure = exact_attempt_failure(lam, "EL_long", 1.0)
            require_exact_placeholder_cause(
                record,
                expected_failure,
                role=f"relation:{relation_name}",
            )
    observed_payload = {
        "audit_ledger_keys": actual_audit,
        "relation_ledger_keys": actual_relations,
    }
    observed_sha = sha256_bytes(canonical_bytes(observed_payload))
    if observed_sha != preenumeration["sha256"]:
        raise InvalidRun("actual canonical ledger-key digest differs from preenumeration")
    return {
        "actual_key_payload_sha256": observed_sha,
        "preenumerated_key_payload_sha256": preenumeration["sha256"],
        "all_exact_sequences_equal": True,
        "all_keys_unique": True,
        "all_roles_sources_state_contexts_domains_and_activity_flags_validated": True,
        "all_NOT_EVALUATED_causes_exactly_match_frozen_upstream_order": True,
    }


def preenumerated_topology() -> dict[str, Any]:
    keys: dict[str, list[str]] = {key: [] for key in LEDGER_COUNT_KEYS}
    relation_keys: dict[str, list[str]] = {
        "initial_state_identities": [],
        "trajectory_pairs": [],
        "endpoint_pairs": [],
        "scaled_residuals": [],
        "candidate_production_residual_pairs": [],
        "saved_endpoint_reproduction": [],
    }
    for lam in LAMBDA_ORDER:
        for backend in BACKEND_ORDER:
            family = "production" if backend == "EL_long" else "candidate"
            variants = CORE_ORDER if family == "production" else ("EL_std", "EL_long")
            contrasts = (
                PRODUCTION_CONTRASTS if family == "production" else CANDIDATE_CONTRASTS
            )
            telescope_left = (
                PRODUCTION_TELESCOPE_LEFT
                if family == "production"
                else CANDIDATE_TELESCOPE_LEFT
            )
            for fraction in FRACTION_ORDER:
                sid = state_key(lam, backend, fraction)
                keys["sampled_states"].append(sid)
                for variant in variants:
                    for stage in STAGE_ORDER:
                        keys["native_stage_vectors"].append(f"{sid}:{variant}:{stage}")
                        keys["native_to_direct_120_comparisons"].append(
                            f"{sid}:{variant}:{stage}"
                        )
                        if stage_active(stage, lam):
                            keys["active_native_comparisons"].append(
                                f"{sid}:{variant}:{stage}"
                            )
                    for stage in SELECTOR_STAGES:
                        keys["selectors"].append(f"{sid}:{variant}:{stage}")
                for digits in (80, 120):
                    for stage in STAGE_ORDER:
                        keys["direct_reference_stage_vectors"].append(
                            f"{sid}:{digits}:{stage}"
                        )
                    for dimension in ("m4", "m5"):
                        keys["raw_reference_gradients"].append(
                            f"{sid}:{digits}:{dimension}"
                        )
                for left, right, mechanism in contrasts:
                    for stage in STAGE_ORDER:
                        keys["controlled_contrasts"].append(
                            f"{sid}:{left}->{right}:{mechanism}:{stage}"
                        )
                for left in telescope_left:
                    for stage in STAGE_ORDER:
                        keys["telescopes"].append(
                            f"{sid}:{left}->EL_long->direct_global_120:{stage}"
                        )
        relation_keys["initial_state_identities"].append(f"lambda={lam:.1f}")
        relation_keys["endpoint_pairs"].append(f"lambda={lam:.1f}")
        relation_keys["candidate_production_residual_pairs"].append(f"lambda={lam:.1f}")
        relation_keys["saved_endpoint_reproduction"].append(f"lambda={lam:.1f}")
        for fraction in FRACTION_ORDER:
            relation_keys["trajectory_pairs"].append(
                f"lambda={lam:.1f}:fraction={fraction:g}"
            )
        for backend in BACKEND_ORDER:
            relation_keys["scaled_residuals"].append(f"lambda={lam:.1f}:{backend}")
    payload = {"audit_ledger_keys": keys, "relation_ledger_keys": relation_keys}
    return {
        "payload": payload,
        "sha256": sha256_bytes(canonical_bytes(payload)),
        "counts": {
            **{key: len(value) for key, value in keys.items()},
            **{key: len(value) for key, value in relation_keys.items()},
        },
        "all_keys_unique_within_ledger": all(
            len(value) == len(set(value))
            for value in (*keys.values(), *relation_keys.values())
        ),
    }


def causal_ids(records: Sequence[Mapping[str, Any]]) -> list[str]:
    return list(
        dict.fromkeys(
            str(record["causal_failure_id"])
            for record in records
            if record.get("status") == "NOT_EVALUATED"
            and record.get("causal_failure_id")
        )
    )


def aggregate_schedule_matrix(ledger: AuditLedger) -> dict[str, Any]:
    production = [
        record for record in ledger.selectors if record.get("family") == "production"
    ]
    missing = [record for record in production if record.get("status") == "NOT_EVALUATED"]
    if missing:
        first_failure_id = missing[0].get("causal_failure_id")
        if not isinstance(first_failure_id, str) or not first_failure_id:
            raise InvalidRun(
                "first missing production selector lacks a causal failure ID"
            )
        return {
            "status": "NOT_EVALUATED",
            "role": "aggregate_schedule_attribution",
            "source": SOURCE,
            "matrix": None,
            "causal_failure_id": first_failure_id,
            "complete_production_selector_count": len(production) - len(missing),
            "required_selector_count": 120,
        }
    if len(production) != 120:
        raise InvalidRun("production aggregate selector count drift")
    matrix = {
        evaluator: all(
            record.get("passed") is True
            for record in production
            if record.get("evaluator") == evaluator
        )
        for evaluator in CORE_ORDER
    }
    if any(
        sum(record.get("evaluator") == evaluator for record in production) != 30
        for evaluator in CORE_ORDER
    ):
        raise InvalidRun("per-evaluator production selector count drift")
    required_matrix = {
        "GN_std": False,
        "GN_long": False,
        "EL_std": True,
        "EL_long": True,
    }
    return {
        "status": "PASS" if matrix == required_matrix else "NONPASS",
        "role": "aggregate_schedule_attribution",
        "source": SOURCE,
        "matrix": matrix,
        "required_matrix": required_matrix,
        "matrix_exact_match": matrix == required_matrix,
        "complete_production_selector_count": 120,
        "pointwise_GN_nonpass_required": False,
    }


def all_status(records: Sequence[Mapping[str, Any]], status: str = "PASS") -> bool:
    return bool(records) and all(record.get("status") == status for record in records)


def evaluate_outcome(
    contract: Contract,
    launches: Sequence[LaunchRecord],
    attempts: Sequence[AttemptResult],
    audit: AuditLedger,
    relations: RelationLedger,
) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
    aggregate = aggregate_schedule_matrix(audit)
    reconstruction_ok = bool(
        all(launch.passed and launch.node is not None for launch in launches)
        and all(
            attempt.status == "PASS"
            and attempt.record.get("returned_t_eval_xi_norm_pass") is True
            for attempt in attempts
            if attempt.backend == "EL_long"
        )
        and sum(
            record.get("status") == "EVALUATED"
            and record.get("family") == "production"
            for record in audit.sampled_states
        )
        == 15
        and all_status(relations.saved_endpoint_reproduction)
        and all_status(
            [
                record
                for record in relations.scaled_residuals
                if record.get("backend") == "EL_long"
            ]
        )
    )
    evaluated_el_long_active = [
        record
        for record in audit.active_native_comparisons
        if record.get("evaluator") == "EL_long"
        and record.get("status") != "NOT_EVALUATED"
    ]
    el_long_baseline_ok = bool(
        evaluated_el_long_active
        and all(record.get("passed") is True for record in evaluated_el_long_active)
    )
    candidate_active = [
        record
        for record in audit.active_native_comparisons
        if record.get("family") == "candidate"
    ]
    candidate_missing = [
        record for record in candidate_active if record.get("status") == "NOT_EVALUATED"
    ]
    candidate_direct_ok = bool(
        candidate_active
        and not candidate_missing
        and all(record.get("passed") is True for record in candidate_active)
    )
    same_point_records = [
        record
        for record in audit.controlled_contrasts
        if record.get("left") == "EL_std"
        and record.get("right") == "EL_long"
        and record.get("stage") in SELECTOR_STAGES
    ]
    same_point_missing = [
        record for record in same_point_records if record.get("status") == "NOT_EVALUATED"
    ]
    same_point_ok = bool(
        len(same_point_records) == 60
        and not same_point_missing
        and all(
            exact_decimal(
                record["symmetric_relative_decimal"], label="same-point contrast"
            )
            <= NATIVE_THRESHOLD
            for record in same_point_records
        )
    )
    trajectory_ok = all_status(relations.trajectory_pairs) and all_status(
        relations.endpoint_pairs
    )
    candidate_residual_records = [
        record
        for record in relations.scaled_residuals
        if record.get("backend") == "EL_std"
    ]
    residual_ok = all_status(candidate_residual_records) and all_status(
        relations.candidate_production_residual_pairs
    )
    all_attempts_ok = all(
        attempt.status == "PASS"
        and attempt.record.get("returned_t_eval_xi_norm_pass") is True
        for attempt in attempts
    )
    zero_placeholders = all(
        not any(record.get("status") == "NOT_EVALUATED" for record in records)
        for records in (
            audit.sampled_states,
            audit.native_stage_vectors,
            audit.active_native_comparisons,
            audit.direct_reference_stage_vectors,
            audit.native_to_direct_120_comparisons,
            audit.selectors,
            audit.controlled_contrasts,
            audit.telescopes,
            audit.raw_reference_gradients,
            relations.initial_state_identities,
            relations.trajectory_pairs,
            relations.endpoint_pairs,
            relations.scaled_residuals,
            relations.candidate_production_residual_pairs,
            relations.saved_endpoint_reproduction,
        )
    )
    all_reference_slots = audit.direct_reference_stage_vectors
    all_telescope_slots = audit.telescopes

    def numerical_status(
        records: Sequence[Mapping[str, Any]], passed: bool
    ) -> tuple[str, list[str]]:
        missing = [record for record in records if record.get("status") == "NOT_EVALUATED"]
        return ("NOT_EVALUATED", causal_ids(missing)) if missing else (
            "PASS" if passed else "NONPASS",
            [],
        )

    status, causes = numerical_status(
        all_reference_slots,
        len(all_reference_slots) == 360,
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[0],
        status,
        "all available direct-global references passed exact 80/120 stability",
        {"fixed_slot_count": len(all_reference_slots)},
        causes,
    )
    reconstruction_records = [
        *relations.saved_endpoint_reproduction,
        *[
            record
            for record in relations.scaled_residuals
            if record.get("backend") == "EL_long"
        ],
    ]
    status, causes = numerical_status(reconstruction_records, reconstruction_ok)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[1], status, "EL_long reconstructed saved endpoints and residuals", causal_failure_ids=causes
    )
    aggregate_causes = (
        [str(aggregate["causal_failure_id"])]
        if aggregate["status"] == "NOT_EVALUATED"
        else []
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[2],
        "NOT_EVALUATED" if aggregate["status"] == "NOT_EVALUATED" else aggregate["status"],
        "complete fifteen-production-state aggregate schedule matrix",
        aggregate,
        aggregate_causes,
    )
    status, causes = numerical_status(candidate_active, candidate_direct_ok)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[3], status, "candidate-state EL_std and EL_long active stages versus direct 120", causal_failure_ids=causes
    )
    status, causes = numerical_status(same_point_records, same_point_ok)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[4], status, "same-point EL_std/EL_long blend and completed RHS", causal_failure_ids=causes
    )
    trajectory_records = [*relations.trajectory_pairs, *relations.endpoint_pairs]
    status, causes = numerical_status(trajectory_records, trajectory_ok)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[5], status, "all physical trajectory fractions and endpoints transferred", causal_failure_ids=causes
    )
    residual_records = [
        *candidate_residual_records,
        *relations.candidate_production_residual_pairs,
    ]
    status, causes = numerical_status(residual_records, residual_ok)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[6], status, "candidate absolute and candidate/production residual transfer", causal_failure_ids=causes
    )
    arithmetic_records = [*all_telescope_slots, *[attempt.record for attempt in attempts]]
    status, causes = numerical_status(
        arithmetic_records,
        all_attempts_ok
        and all(
            record.get("status") == "PASS" for record in all_telescope_slots
        ),
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[7], status, "telescopes, finiteness, solver completion, and returned-sample xi norm", causal_failure_ids=causes
    )
    if tuple(record["id"] for record in contract.numerical) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("numerical check order drift")

    if not reconstruction_ok:
        classification = (
            "P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS"
        )
    elif not el_long_baseline_ok:
        classification = (
            "P55_EL_LONG_DIRECT_REFERENCE_BASELINE_NONPASS_ON_PHASE55_SAMPLED_STATES"
        )
    elif aggregate.get("matrix_exact_match") is not True:
        classification = (
            "P55_PHASE54_SCHEDULE_ONLY_ATTRIBUTION_NOT_REPRODUCED_ON_"
            "PHASE55_RECONSTRUCTED_TRAJECTORY_SAMPLE_SET"
        )
    elif (
        all_attempts_ok
        and zero_placeholders
        and candidate_direct_ok
        and same_point_ok
        and trajectory_ok
        and residual_ok
    ):
        classification = (
            "P55_EL_STD_TRAJECTORY_SCHEDULE_TRANSFER_QUALIFIED_ON_THREE_"
            "P53_ROOTS_WITH_P50_SADDLE_PINNED_LAUNCHES"
        )
    else:
        classification = (
            "P55_EL_STD_TRAJECTORY_SCHEDULE_TRANSFER_NOT_QUALIFIED_ON_THREE_"
            "P53_ROOTS_WITH_P50_SADDLE_PINNED_LAUNCHES"
        )
    prerequisites = {
        "reconstruction_pass": reconstruction_ok,
        "EL_long_active_direct_reference_baseline_pass": el_long_baseline_ok,
        "aggregate_schedule_matrix": aggregate,
        "candidate_direct_pass": candidate_direct_ok,
        "same_point_pass": same_point_ok,
        "trajectory_and_endpoint_pass": trajectory_ok,
        "candidate_residual_pass": residual_ok,
        "all_six_solver_attempts_and_xi_norm_pass": all_attempts_ok,
        "zero_NOT_EVALUATED_placeholders": zero_placeholders,
    }
    return classification, aggregate, prerequisites


def required_global_nulls() -> dict[str, Any]:
    return {
        "historical_Phase51_classification_after": None,
        "historical_Phase53_classification_after": None,
        "continuation_reclassification": None,
        "straight_arm_intersections_searched": False,
        "cap_reintersections_searched": False,
        "root_exhaustion_proved": False,
        "all_saddles_and_upward_components_complete": False,
        "physical_original_cycle_derived": False,
        "common_determinant_line_constructed": False,
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "cutoff_limit": None,
        "continuum_limit": None,
        "promoted_output": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "physics_claim": None,
        "TOE_claim": None,
    }


def validate_preenumeration(
    manifest: Mapping[str, Any], record: Mapping[str, Any]
) -> None:
    if record.get("all_keys_unique_within_ledger") is not True:
        raise InvalidRun("preenumerated ledger keys are not unique")
    expected = manifest["expected_audit_counts"]
    mapping = {
        "sampled_states": "total_sampled_state_or_failure_placeholder_count",
        "native_stage_vectors": "native_stage_vector_or_placeholder_record_count",
        "active_native_comparisons": "active_native_stage_comparison_or_placeholder_record_count",
        "direct_reference_stage_vectors": "direct_reference_stage_vector_or_placeholder_record_count_80_and_120_combined",
        "native_to_direct_120_comparisons": "native_to_direct_120_comparison_or_placeholder_record_count",
        "selectors": "selector_or_placeholder_record_count",
        "controlled_contrasts": "controlled_contrast_or_placeholder_record_count",
        "telescopes": "telescope_or_placeholder_record_count",
        "raw_reference_gradients": "direct_reference_raw_gradient_evaluation_or_placeholder_record_count",
    }
    for key, expected_key in mapping.items():
        if int(record["counts"][key]) != int(expected[expected_key]):
            raise InvalidRun(f"preenumerated count drift at {key}")
    relation_expected = {
        "initial_state_identities": 3,
        "trajectory_pairs": 15,
        "endpoint_pairs": 3,
        "scaled_residuals": 6,
        "candidate_production_residual_pairs": 3,
        "saved_endpoint_reproduction": 3,
    }
    for key, value in relation_expected.items():
        if int(record["counts"][key]) != value:
            raise InvalidRun(f"preenumerated relation count drift at {key}")


def exact_checks(
    contract: Contract,
    bundle: InputBundle,
    targets: Sequence[TargetRecord],
    setup: StaticSetup,
    launches: Sequence[LaunchRecord],
    preenumeration: Mapping[str, Any],
    guard_counters: Mapping[str, int],
    attempts: Sequence[AttemptResult] | None,
    relations: RelationLedger | None,
) -> None:
    contract.add_exact(
        EXACT_CHECK_IDS[0],
        len(bundle.observed_pins) == 26,
        "26 recursive pins, commits, blobs, bytes, self-digests, and corrected Phase54 validated",
        {
            "consumed_path_count": len(bundle.observed_pins),
            "effective_manifest_commit": INPUT_COMMIT,
            "effective_manifest_blob_oid": INPUT_BLOB_OID,
            "effective_manifest_sha256": INPUT_SHA256,
            "corrected_Phase54_classification": REQUIRED_PHASE54_CLASSIFICATION,
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[1],
        len(targets) == 3
        and tuple(target.lambda_value for target in targets) == LAMBDA_ORDER,
        "three saved phi_plus roots, P50 saddles, intersections, residual scalars, and endpoints matched frozen digests",
    )
    identity_records_valid = bool(
        relations is None
        or len(relations.initial_state_identities) == 3
        and all(
            record.get("status") == "NOT_EVALUATED"
            or record.get("byte_identical") is True
            for record in relations.initial_state_identities
        )
    )
    contract.add_exact(
        EXACT_CHECK_IDS[2],
        len(launches) == 3
        and identity_records_valid
        and guard_counters.get("scipy_optimize_root", -1) == 0
        and guard_counters.get("module_root_alias", -1) == 0
        and guard_counters.get("saddle_cache_miss", -1) == 0
        and guard_counters.get("saddle_cache_hit", -1)
        == 2 * sum(launch.passed for launch in launches)
        and guard_counters.get("Gamma_K_root_routine", -1) == 0,
        "zero-solve P50-pinned launch topology and identical backend initial buffers retained",
        {
            "fixed_saddle_validation_count": len(launches),
            "successful_launch_count": sum(launch.passed for launch in launches),
            "required_saddle_cache_hit_count": 2
            * sum(launch.passed for launch in launches),
            "observed_saddle_cache_hit_count": guard_counters.get(
                "saddle_cache_hit"
            ),
            "guard_counters": dict(guard_counters),
        },
    )
    binding = setup.binding_ledger["P53_hot_loop_gradient_identity_binding"]
    contract.add_exact(
        EXACT_CHECK_IDS[3],
        setup.symbolic_ledger["phase53_projection_sha256"]
        == EXPECTED_PROJECTION_SHA256
        and setup.symbolic_ledger["phase53_projection_canonical_bytes"]
        == EXPECTED_PROJECTION_BYTES
        and all(
            record["all_same_callable_objects_in_process"] is True
            for record in binding.values()
        ),
        "Phase54 four-core bindings and full Phase53 projection validated; science uses phi_plus only",
        {
            "projection_sha256": setup.symbolic_ledger[
                "phase53_projection_sha256"
            ],
            "projection_canonical_bytes": setup.symbolic_ledger[
                "phase53_projection_canonical_bytes"
            ],
            "science_source": SOURCE,
            "hot_loop_identity_binding": binding,
        },
    )
    successful_launch_count = sum(launch.passed for launch in launches)
    expected_solver_calls = 0 if attempts is None else 2 * successful_launch_count
    attempt_topology = (
        guard_counters.get("runner_solve_ivp") == expected_solver_calls
        and guard_counters.get("runner_solve_ivp") in (0, 2, 4, 6)
        and (
            attempts is None
            or (
                len(attempts) == 6
                and sum(attempt.backend == "EL_long" for attempt in attempts) == 3
                and sum(attempt.backend == "EL_std" for attempt in attempts) == 3
                and [
                    (attempt.launch.target.lambda_value, attempt.backend)
                    for attempt in attempts
                ]
                == [
                    (lam, backend)
                    for lam in LAMBDA_ORDER
                    for backend in BACKEND_ORDER
                ]
                and all(
                    [slot.get("fraction") for slot in attempt.record["fraction_slots"]]
                    == list(FRACTION_ORDER)
                    and [slot.get("state_id") for slot in attempt.record["fraction_slots"]]
                    == [
                        state_key(
                            attempt.launch.target.lambda_value,
                            attempt.backend,
                            fraction,
                        )
                        for fraction in FRACTION_ORDER
                    ]
                    and len(attempt.record["fraction_slots"]) == 5
                    and sum(
                        slot.get("status") == "EVALUATED"
                        for slot in attempt.record["fraction_slots"]
                    )
                    == len(attempt.xi_by_fraction)
                    and all(
                        slot.get("status") in ("EVALUATED", "NOT_EVALUATED")
                        for slot in attempt.record["fraction_slots"]
                    )
                    for attempt in attempts
                )
            )
        )
    )
    contract.add_exact(
        EXACT_CHECK_IDS[4],
        attempt_topology and bool(preenumeration["all_keys_unique_within_ledger"]),
        "six attempt slots, five fractions, and every downstream evaluated/placeholder key were predeclared",
        {
            "preenumeration_sha256": preenumeration["sha256"],
            "preenumerated_counts": preenumeration["counts"],
            "attempt_records_emitted": 0 if attempts is None else len(attempts),
            "logical_EL_long_record_count": 0
            if attempts is None
            else sum(attempt.backend == "EL_long" for attempt in attempts),
            "logical_EL_std_record_count": 0
            if attempts is None
            else sum(attempt.backend == "EL_std" for attempt in attempts),
            "expected_runner_solve_ivp_call_count": expected_solver_calls,
            "observed_runner_solve_ivp_call_count": guard_counters.get(
                "runner_solve_ivp"
            ),
            "allowed_runner_solve_ivp_call_counts": [0, 2, 4, 6],
            "fraction_slot_count_per_attempt": 5,
            "fraction_key_order": list(FRACTION_ORDER),
        },
    )
    p52_stage_source = inspect.getsource(setup.p52.native_stages)
    fixed_long_source = inspect.getsource(setup.p53.fixed_array_sum)
    fixed_std_source = inspect.getsource(setup.p54.fixed_complex128_sum)
    convention_pass = bool(
        "factor.T" in p52_stage_source
        and ".conj().T" not in p52_stage_source
        and ".conjugate().T" not in p52_stage_source
        and p52_stage_source.count("-np.conjugate(contracted)") == 1
        and "for index in np.ndindex(shape)" in fixed_long_source
        and "for index in range(dimension)" in fixed_std_source
        and re.search(r"(?<![A-Za-z0-9_])sum\(", fixed_long_source) is None
        and re.search(r"(?<![A-Za-z0-9_])sum\(", fixed_std_source) is None
    )
    contract.add_exact(
        EXACT_CHECK_IDS[5],
        convention_pass,
        "fixed left-to-right sums, Decimal gates, ordinary transpose, one outer conjugation, and one solver cast bound",
        {
            "Decimal_gate_type": str(type(NATIVE_THRESHOLD).__name__),
            "common_stage_source_sha256": sha256_bytes(
                p52_stage_source.encode("utf-8")
            ),
        },
    )
    reference_source = inspect.getsource(direct_reference)
    contract.add_exact(
        EXACT_CHECK_IDS[6],
        "direct_evalf_gradient" in reference_source
        and "direct_evalf_cse_gradient" not in reference_source
        and "state_w5" in reference_source,
        "direct-global reference is unreduced/CSE-free and lifts completed state_w5 decimals",
        {
            "reference_source_sha256": sha256_bytes(
                reference_source.encode("utf-8")
            ),
            "precision_tiers": [80, 120],
        },
    )
    forbidden_zero = all(
        guard_counters.get(key, -1) == 0
        for key in (
            "scipy_optimize_root",
            "module_root_alias",
            "saddle_cache_miss",
            "inherited_integrate_k",
            "inherited_solve_ivp",
            "Gamma_K_root_routine",
            "tangent_ODE",
            "event_integration",
            "continuation_or_replay",
            "finite_difference",
            "reflection",
            "endpoint_mutation",
            "action_or_first_cap",
        )
    )
    contract.add_exact(
        EXACT_CHECK_IDS[7],
        forbidden_zero and all(value is None or value is False or isinstance(value, str) for value in required_global_nulls().values()),
        "validator scope, historical immutability, forbidden-call counters, and global null boundary retained",
        {"forbidden_call_counters": dict(guard_counters)},
    )
    if tuple(record["id"] for record in contract.exact) != EXACT_CHECK_IDS:
        raise InvalidRun("exact check order drift")


def execution_topology(
    launches: Sequence[LaunchRecord],
    attempts: Sequence[AttemptResult] | None,
    guard_counters: Mapping[str, int],
    audit: AuditLedger | None,
    relations: RelationLedger | None,
) -> dict[str, Any]:
    return {
        "source_count": 1,
        "lambda_count": 3,
        "consumed_root_count": 3,
        "inherited_context_loaded_saddle_record_count": 17,
        "scientifically_selected_fixed_saddle_count": 3,
        "fixed_saddle_validation_attempt_count": len(launches),
        "launch_reconstruction_attempt_or_scientific_nonpass_placeholder_record_count": len(launches),
        "evaluated_launch_reconstruction_count": sum(launch.passed for launch in launches),
        "saddle_solve_count": 0,
        "Gamma_K_root_solve_count": 0,
        "ODE_attempt_or_upstream_placeholder_record_count": 0 if attempts is None else len(attempts),
        "EL_long_attempt_or_upstream_placeholder_record_count": 0
        if attempts is None
        else sum(attempt.backend == "EL_long" for attempt in attempts),
        "EL_std_attempt_or_upstream_placeholder_record_count": 0
        if attempts is None
        else sum(attempt.backend == "EL_std" for attempt in attempts),
        "actual_solve_ivp_call_count": guard_counters.get("runner_solve_ivp", 0),
        "tangent_ODE_attempt_count": 0,
        "event_integration_attempt_count": 0,
        "trajectory_fraction_value_count": 5,
        "sampled_state_or_failure_placeholder_count": 0
        if audit is None
        else len(audit.sampled_states),
        "backend_paired_fraction_record_or_placeholder_count": 0
        if relations is None
        else len(relations.trajectory_pairs),
        "endpoint_pair_record_or_placeholder_count": 0
        if relations is None
        else len(relations.endpoint_pairs),
        "initial_state_identity_record_or_upstream_nonpass_placeholder_count": 3
        if relations is None
        else len(relations.initial_state_identities),
        "scaled_residual_record_or_placeholder_count": 0
        if relations is None
        else len(relations.scaled_residuals),
        "Gamma_K_continuation_node_ledger_count": 0,
        "continuation_or_classification_replay_count": 0,
        "finite_difference_count": 0,
        "reflection_count": 0,
        "endpoint_mutation_count": 0,
        "action_or_first_cap_ledger_count": 0,
        "guard_counters": dict(guard_counters),
    }


def base_result(
    bundle: InputBundle,
    setup: StaticSetup,
    targets: Sequence[TargetRecord],
    launches: Sequence[LaunchRecord],
    preenumeration: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "phase": 55,
        "source": SOURCE,
        "historical_Phase53_classification_preserved_as": (
            REQUIRED_PHASE53_CLASSIFICATION
        ),
        "Phase56_candidate_boundary": PHASE56_CANDIDATE_BOUNDARY,
        "manifest_identity": {
            "introduction_commit": INPUT_INTRODUCTION_COMMIT,
            "effective_commit": INPUT_COMMIT,
            "effective_blob_oid": INPUT_BLOB_OID,
            "sha256": INPUT_SHA256,
            "size_bytes": INPUT_SIZE_BYTES,
        },
        "runner_binding": bundle.runner_guard,
        "runtime": bundle.observed_runtime,
        "input_pin_validation": {
            "consumed_path_count": len(bundle.observed_pins),
            "records": bundle.observed_pins,
        },
        "saved_targets": [
            {
                "source": SOURCE,
                "lambda": target.lambda_value,
                "parameters": target.parameters,
                "p50_saddle": target.p50_saddle,
                "intersection_z": target.intersection_z,
                "saved_endpoint_z": target.saved_endpoint_z,
                "saved_scaled_residual_max_abs_decimal": target.saved_scaled_residual,
                "frozen_declarations": target.declarations,
            }
            for target in targets
        ],
        "symbolic_and_evaluator_binding": {
            "symbolic_ledger": setup.symbolic_ledger,
            "binding_ledger": setup.binding_ledger,
            "Phase53_plain_true_semantics": "GN_std_historical_global_nonCSE_only",
            "EL_std_uses_Phase53_plain_true": False,
            "science_source": SOURCE,
        },
        "fixed_saddle_validations": [
            launch.fixed_saddle_validation for launch in launches
        ],
        "launch_reconstructions": [launch.record for launch in launches],
        "preenumerated_record_topology": preenumeration,
        "historical_boundary": {
            "Phase51_result_mutated_or_reclassified": False,
            "Phase53_result_mutated_or_reclassified": False,
            "Phase53_classification_preserved_as": REQUIRED_PHASE53_CLASSIFICATION,
            "exact_Phase53_launch_claim_allowed": False,
        },
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
    }


def common_preamble(
    *, authoritative: bool
) -> tuple[
    InputBundle,
    tuple[TargetRecord, ...],
    StaticSetup,
    list[LaunchRecord],
    Mapping[str, Any],
    Mapping[str, int],
]:
    bundle = validate_inputs(authoritative=authoritative)
    targets = extract_targets(bundle)
    setup = build_static_setup(bundle)
    preenumeration = preenumerated_topology()
    validate_preenumeration(bundle.manifest, preenumeration)
    with guarded_topology(setup) as guard:
        launches = validate_fixed_saddles(setup, targets)
        reconstruct_launches(setup, launches)
        guard.assert_zero_forbidden()
        counters = dict(guard.counters)
    return bundle, targets, setup, launches, preenumeration, counters


def validation_only_result() -> dict[str, Any]:
    bundle, targets, setup, launches, preenumeration, counters = common_preamble(
        authoritative=False
    )
    contract = Contract()
    exact_checks(
        contract,
        bundle,
        targets,
        setup,
        launches,
        preenumeration,
        counters,
        attempts=None,
        relations=None,
    )
    for check_id in NUMERICAL_CHECK_IDS:
        contract.add_numerical(
            check_id,
            "NOT_EVALUATED",
            "predeclared; validate-only mode performs no ODE or sampled-state evaluation",
            causal_failure_ids=["validate-only:authoritative_numerics_skipped"],
        )
    rehash = post_rehash(bundle)
    result = base_result(bundle, setup, targets, launches, preenumeration)
    result.update(
        {
            "mode": "validate-only",
            "run_status": "VALIDATION_ONLY",
            "classification": None,
            "exact_checks": contract.exact,
            "numerical_checks": contract.numerical,
            "ODE_attempts": [],
            "execution_topology": execution_topology(
                launches, None, counters, None, None
            ),
            "audit_ledgers": None,
            "relation_ledgers": None,
            "counts": {
                "preenumerated": preenumeration["counts"],
                "evaluated_numerical_records": 0,
            },
            "post_evaluation_rehash": rehash,
            "scientific_classification_prerequisites": {
                "evaluated": False,
                "scientific_label_allowed_in_validate_only": False,
            },
            "qualified_Phase56_state_RHS_candidate": None,
            "computed_facts": [
                "all 26 pins, both-source symbolic projection, four-core bindings, and three saved targets validated",
                "three P50-pinned launch reconstruction slots were processed without a saddle or Gamma--K root solve",
                "all authoritative audit and relation keys were preenumerated; no solve_ivp or sampled-state reference was evaluated",
            ],
            "interpretation": (
                "Validation-only is not a scientific Phase55 outcome and selects no "
                "schedule-transfer label."
            ),
        }
    )
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def authoritative_result() -> dict[str, Any]:
    bundle = validate_inputs(authoritative=True)
    targets = extract_targets(bundle)
    setup = build_static_setup(bundle)
    preenumeration = preenumerated_topology()
    validate_preenumeration(bundle.manifest, preenumeration)
    with guarded_topology(setup) as guard:
        launches = validate_fixed_saddles(setup, targets)
        reconstruct_launches(setup, launches)
        schedule = ScheduleEvaluator(setup)
        attempts = run_state_odes(launches, schedule, guard)
        audit = build_audit_ledger(setup, attempts)
        relations = build_relation_ledger(setup, launches, attempts)
        guard.assert_zero_forbidden()
        counters = dict(guard.counters)
    # Frozen precedence requires a complete post-numerical byte rehash before
    # any scientific classification branch is selected.
    rehash = post_rehash(bundle)
    audit_counts = count_audit_ledger(bundle.manifest, audit)
    key_sequence_validation = assert_actual_key_sequences(
        audit, relations, preenumeration, attempts, launches
    )
    contract = Contract()
    exact_checks(
        contract,
        bundle,
        targets,
        setup,
        launches,
        preenumeration,
        counters,
        attempts=attempts,
        relations=relations,
    )
    classification, aggregate, prerequisites = evaluate_outcome(
        contract, launches, attempts, audit, relations
    )
    qualified_label = (
        "P55_EL_STD_TRAJECTORY_SCHEDULE_TRANSFER_QUALIFIED_ON_THREE_"
        "P53_ROOTS_WITH_P50_SADDLE_PINNED_LAUNCHES"
    )
    result = base_result(bundle, setup, targets, launches, preenumeration)
    result.update(
        {
            "mode": "authoritative",
            "run_status": "VALID_RUN",
            "classification": classification,
            "exact_checks": contract.exact,
            "numerical_checks": contract.numerical,
            "ODE_attempts": [attempt.record for attempt in attempts],
            "ODE_hot_loop_binding": {
                "backend_order": list(BACKEND_ORDER),
                "callback_counts": schedule.calls,
                "runner_solve_ivp_call_count": counters["runner_solve_ivp"],
                "P53_plain_true_used_for_EL_std": False,
                "EL_long_accumulation": "Phase53.fixed_array_sum_clongdouble",
                "EL_std_accumulation": "Phase54.fixed_complex128_sum_then_clongdouble",
                "common_downstream": "Phase52.native_stages",
                "sole_solver_boundary_output_cast": "complex128",
            },
            "execution_topology": execution_topology(
                launches, attempts, counters, audit, relations
            ),
            "counts": {
                "audit": audit_counts,
                "actual_canonical_key_sequence_validation": key_sequence_validation,
            },
            "audit_ledgers": {
                "sampled_states": audit.sampled_states,
                "native_stage_vectors": audit.native_stage_vectors,
                "active_native_stage_comparisons": audit.active_native_comparisons,
                "direct_reference_stage_vectors": audit.direct_reference_stage_vectors,
                "native_to_direct_120_comparisons": audit.native_to_direct_120_comparisons,
                "classification_selectors": audit.selectors,
                "controlled_contrasts": audit.controlled_contrasts,
                "telescopes": audit.telescopes,
                "direct_reference_raw_gradients": audit.raw_reference_gradients,
            },
            "relation_ledgers": {
                "initial_state_identities": relations.initial_state_identities,
                "backend_paired_fractions": relations.trajectory_pairs,
                "endpoint_pairs": relations.endpoint_pairs,
                "scaled_residuals": relations.scaled_residuals,
                "candidate_production_scaled_residual_pairs": relations.candidate_production_residual_pairs,
                "saved_Phase53_endpoint_reproduction": relations.saved_endpoint_reproduction,
            },
            "aggregate_production_schedule_attribution": aggregate,
            "scientific_classification_prerequisites": prerequisites,
            "qualified_Phase56_state_RHS_candidate": (
                "EL_std_state_RHS_schedule_only"
                if classification == qualified_label
                else None
            ),
            "Phase56_candidate_boundary": PHASE56_CANDIDATE_BOUNDARY,
            "post_evaluation_rehash": rehash,
            "evaluation_order": [
                "three_fixed_P50_saddle_EL_long_gradient_Hessian_validations",
                "three_pass_only_cache_and_SourceContext_node_launch_reconstructions",
                "six_lambda_major_backend_minor_state_only_DOP853_attempt_slots",
                "thirty_ordered_sample_or_failure_placeholder_slots",
                "direct_unreduced_80_120_then_native_four_or_two_cell_state_audits",
                "physical_state_endpoint_and_scaled_residual_relations",
                "post_numerical_28_path_rehash",
                "classification_precedence_dispatch",
            ],
            "computed_facts": [
                "three saved Phase53 roots were consumed without solving a root or saddle",
                "EL_long and coherent element-local EL_std used the same initial complex128 bytes at every reconstructed launch",
                "all fixed audit and relation slots were retained as evaluated records or causal placeholders",
            ],
            "interpretation": (
                "The Phase55 label is a bounded finite-arithmetic computation-workbench "
                "result on three saved roots. It is not a new root, global cycle, physics, "
                "or TOE claim."
            ),
        }
    )
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def invalid_result(error: BaseException, *, validate_only: bool) -> dict[str, Any]:
    causal_failure_id = "invalid_run:validity_prerequisite_failure"
    details: dict[str, Any] = {
        "type": type(error).__name__,
        "message": str(error),
        "failure_id": causal_failure_id,
    }
    if isinstance(error, NonfiniteRun):
        details["nonfinite"] = error.details
    result = {
        "schema": RESULT_SCHEMA,
        "phase": 55,
        "mode": "validate-only" if validate_only else "authoritative",
        "run_status": "INVALID_RUN",
        "classification": "INVALID_RUN",
        "historical_Phase53_classification_preserved_as": (
            REQUIRED_PHASE53_CLASSIFICATION
        ),
        "Phase56_candidate_boundary": PHASE56_CANDIDATE_BOUNDARY,
        "error": details,
        "exact_checks": [
            {
                "id": check_id,
                "kind": "exact",
                "passed": False,
                "status": "INVALID_RUN",
                "evaluated": False,
                "statement": (
                    "not evaluated because the run failed a validity prerequisite; "
                    "no observation is claimed"
                ),
                "causal_failure_id": causal_failure_id,
            }
            for check_id in EXACT_CHECK_IDS
        ],
        "numerical_checks": [
            {
                "id": check_id,
                "kind": "numerical",
                "passed": False,
                "status": "NOT_EVALUATED",
                "evaluated": False,
                "statement": (
                    "not evaluated because the run is invalid; no numerical "
                    "observation is claimed"
                ),
                "causal_failure_ids": [causal_failure_id],
            }
            for check_id in NUMERICAL_CHECK_IDS
        ],
        "execution_topology": None,
        "qualified_Phase56_state_RHS_candidate": None,
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
        "interpretation": (
            "No scientific Phase55 label is permitted because a validity prerequisite failed."
        ),
    }
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def emit_result(payload: Mapping[str, Any]) -> None:
    ready = json_ready(payload)
    raw = json.dumps(
        ready,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    print(f"{RESULT_PREFIX}{raw}", flush=True)


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="bind pins/evaluators/launches and preenumerate ledgers without solve_ivp",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        result = (
            validation_only_result()
            if arguments.validate_only
            else authoritative_result()
        )
    except Exception as error:
        traceback.print_exc(file=sys.stderr)
        emit_result(invalid_result(error, validate_only=arguments.validate_only))
        return 2
    emit_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
