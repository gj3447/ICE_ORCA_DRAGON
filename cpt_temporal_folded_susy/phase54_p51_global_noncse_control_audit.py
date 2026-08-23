#!/usr/bin/env python3
"""Phase 54: static audit of the Phase-51 global non-CSE evaluator.

The runner consumes exactly the six launch states retained by Phase 53 and
compares a frozen two-by-two evaluator matrix plus two contextual controls.
It does not solve a saddle or another root and it does not integrate or replay
any continuation.  Progress is written to stderr and exactly one
``RESULT_JSON=...`` object is written to stdout.

``--validate-only`` verifies pins, runtime, slots, symbolic plans, callable
bindings, topology, and the Phase-53 production projection without evaluating
the six native/reference numerical records.
"""

from __future__ import annotations

import argparse
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
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Iterable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
from mpmath import mp
import numpy as np
import scipy
import sympy as sp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT_INPUTS.json"
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

INPUT_COMMIT = "c020a13a0c2c7963920ca17365f27fe6544fa0d9"
INPUT_INTRODUCTION_COMMIT = "cceaf7b91318627bea9ae5dca287716e971eb043"
INPUT_SHA256 = "4a8f6282a09659e24dc938fa4ae1383c8b5c61f4e2f231b21fcde61637b1fc97"
INPUT_BLOB_OID = "e065da49560a74008f1520eee4d73afdc8c89e97"
INPUT_SIZE_BYTES = 28734
RESULT_SCHEMA = "ice-phase54-p51-global-noncse-control-audit/v1"
RESULT_PREFIX = "RESULT_JSON="

M4 = 7
M5 = 9
SOURCE_ORDER = ("phi_plus", "phi_minus")
LAMBDA_ORDER = (0.0, 0.5, 1.0)
STAGE_ORDER = (
    "m4_raw_gradient",
    "m4_lifted_gradient",
    "m5_raw_gradient",
    "lambda_blended_gradient",
    "A_lambda_transpose_contraction",
    "outer_minus_conjugation",
)
STAGE_DIMENSIONS = (7, 9, 9, 9, 9, 9)
EVALUATOR_ORDER = (
    "GN_std",
    "GN_long",
    "EL_std",
    "EL_long",
    "phase51_global_CSE_context",
    "phase52_long_namespace_joint_CSE_context",
)
CORE_EVALUATORS = ("GN_std", "GN_long", "EL_std", "EL_long")
CONTEXT_EVALUATORS = (
    "phase51_global_CSE_context",
    "phase52_long_namespace_joint_CSE_context",
)
SELECTOR_STAGES = ("lambda_blended_gradient", "outer_minus_conjugation")
TELESCOPE_LEFT_ORDER = (
    "GN_std",
    "GN_long",
    "EL_std",
    "phase51_global_CSE_context",
    "phase52_long_namespace_joint_CSE_context",
)
CONTROLLED_CONTRASTS = (
    ("GN_std", "GN_long", "printer_and_namespace_only"),
    ("EL_std", "EL_long", "callable_and_accumulator_precision_only"),
    ("GN_std", "EL_std", "global_noncse_vs_element_local_schedule_standard"),
    ("GN_long", "EL_long", "global_noncse_vs_element_local_schedule_long"),
)

EXACT_CHECK_IDS = (
    "P54.inputs.byte_pins_commits_blobs_and_self_digests",
    "P54.slots.exact_Phase53_six_launch_state_bytes",
    "P54.contract.core_2x2_evaluator_bindings_and_controlled_differences",
    "P54.contract.two_contextual_evaluator_bindings_and_six_stage_order",
    "P54.reference.direct_global_expression_independence",
    "P54.conventions.ordinary_transpose_single_outer_conjugation",
    "P54.guard.static_classification_and_global_nulls",
)
NUMERICAL_CHECK_IDS = (
    "P54.reference.80_120_and_symbolic_CSE_plain_stability",
    "P54.matrix.GN_std_vs_direct_120",
    "P54.matrix.GN_long_vs_direct_120",
    "P54.matrix.EL_std_vs_direct_120",
    "P54.matrix.EL_long_vs_direct_120",
    "P54.context.Phase51_global_CSE_vs_direct_120",
    "P54.context.Phase52_long_namespace_joint_CSE_vs_direct_120",
    "P54.arithmetic.core_contrasts_and_six_stage_telescopes",
)

REFERENCE_THRESHOLD = Decimal("1e-40")
NATIVE_THRESHOLD = Decimal("5e-10")
TELESCOPE_THRESHOLD = Decimal("5e-18")
EXPECTED_PROJECTION_SHA256 = (
    "8359762ba056bd7a300bceba8d4bf7e83e22149f5795c37f5b6ee0a4a212ad4e"
)
EXPECTED_PROJECTION_BYTES = 4141
TEMPORARY_NAME = re.compile(r"^x[0-9]+$")
IDENTITY_KEY = re.compile(r"(^|_)(id|identity|object_id|callable_id)(_|$)", re.I)


class InvalidRun(RuntimeError):
    """A frozen pin, binding, topology, numerical, or null guard failed."""


def progress(message: str) -> None:
    print(f"[Phase54] {message}", file=sys.stderr, flush=True)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require(mapping: Mapping[str, Any], key: str, *, where: str) -> Any:
    if key not in mapping:
        raise InvalidRun(f"missing {where}.{key}")
    return mapping[key]


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path}")
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


def finite_float(value: Any, *, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise InvalidRun(f"nonfinite {label}")
    return number


def ld_text(value: Any) -> str:
    number = np.longdouble(value)
    if not np.isfinite(number):
        raise InvalidRun("cannot serialize a nonfinite longdouble")
    return np.format_float_scientific(number, precision=24, unique=False, trim="k")


def mp_text(value: Any, digits: int = 50) -> str:
    number = mp.mpf(value)
    if not mp.isfinite(number):
        raise InvalidRun("cannot serialize a nonfinite mpmath real")
    return mp.nstr(number, n=digits, strip_zeros=False)


def exact_decimal(value: Any, *, label: str) -> Decimal:
    """Parse a retained decimal string without mpmath context rounding."""

    try:
        number = Decimal(str(value))
    except InvalidOperation as error:
        raise InvalidRun(f"invalid retained decimal at {label}: {value!r}") from error
    if not number.is_finite():
        raise InvalidRun(f"nonfinite retained decimal at {label}")
    return number


def json_ready(value: Any) -> Any:
    """Convert numerical objects without ever emitting a process-local id()."""
    if isinstance(value, np.ndarray):
        array = np.asarray(value)
        if np.iscomplexobj(array):
            if not np.all(np.isfinite(array)):
                raise InvalidRun("nonfinite NumPy complex array")
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
                    [finite_float(item.real, label="array real"),
                     finite_float(item.imag, label="array imag")]
                    for item in array.reshape(-1)
                ],
            }
        if not np.all(np.isfinite(array)):
            raise InvalidRun("nonfinite NumPy real array")
        if array.dtype == np.dtype(np.longdouble):
            return {
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "longdouble_decimals": [ld_text(item) for item in array.reshape(-1)],
            }
        return {
            "shape": list(array.shape),
            "dtype": str(array.dtype),
            "values": [json_ready(item) for item in array.reshape(-1)],
        }
    if isinstance(value, np.clongdouble):
        return {
            "dtype": str(value.dtype),
            "clongdouble_decimal_pair": [ld_text(value.real), ld_text(value.imag)],
        }
    if isinstance(value, np.longdouble):
        return {"dtype": str(value.dtype), "longdouble_decimal": ld_text(value)}
    if isinstance(value, np.complexfloating):
        if not np.isfinite(value.real) or not np.isfinite(value.imag):
            raise InvalidRun("nonfinite NumPy complex scalar")
        return {
            "dtype": str(value.dtype),
            "real": finite_float(value.real, label="complex real"),
            "imag": finite_float(value.imag, label="complex imaginary"),
        }
    if isinstance(value, complex):
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise InvalidRun("nonfinite Python complex")
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, mp.mpc):
        if not mp.isfinite(value.real) or not mp.isfinite(value.imag):
            raise InvalidRun("nonfinite mpmath complex")
        return {"mp_decimal_pair": [mp_text(value.real), mp_text(value.imag)]}
    if isinstance(value, mp.mpf):
        return {"mp_decimal": mp_text(value)}
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return finite_float(value, label="float")
    return value


def canonical_bytes(payload: Mapping[str, Any]) -> bytes:
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
    key = "result_payload_sha256_without_self"
    if key not in payload:
        key = "checkpoint_payload_sha256_without_self"
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
    """Guard against accidentally serializing Python id(...) evidence."""
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
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "passed": bool(passed),
            "status": "PASS" if passed else "NONPASS",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.numerical.append(record)


@dataclass(frozen=True)
class PinRecord:
    label: str
    path: str
    commit: str
    sha256: str
    size_bytes: int
    blob_oid: str


@dataclass
class InputBundle:
    manifest: dict[str, Any]
    manifest_raw: bytes
    observed_runtime: dict[str, Any]
    observed_pins: dict[str, Any]
    loaded_json: dict[str, dict[str, Any]]
    p52_manifest: dict[str, Any]
    p53_manifest: dict[str, Any]
    p52_result: dict[str, Any]
    p53_result: dict[str, Any]
    runner_guard: dict[str, Any]
    consumed_paths: tuple[Path, ...]


def _pin_commit(specification: Mapping[str, Any], *, where: str) -> str:
    value = specification.get("git_commit", specification.get("commit"))
    if not isinstance(value, str) or not value:
        raise InvalidRun(f"missing {where}.git_commit/commit")
    return value


def _pin_blob(specification: Mapping[str, Any]) -> str | None:
    value = specification.get("git_blob_oid")
    return str(value) if value is not None else None


def validate_pin(
    label: str,
    specification: Mapping[str, Any],
    *,
    loaded_json: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], Path]:
    where = f"pin {label}"
    relative = str(require(specification, "path", where=where))
    commit = _pin_commit(specification, where=where)
    expected_sha = str(require(specification, "sha256", where=where))
    path = REPO_ROOT / relative
    if not path.is_file():
        raise InvalidRun(f"pinned path is not a file: {relative}")
    raw = path.read_bytes()
    observed_sha = sha256_bytes(raw)
    if observed_sha != expected_sha:
        raise InvalidRun(f"pinned SHA drift: {label}")
    expected_size = specification.get("size_bytes")
    if expected_size is not None and len(raw) != int(expected_size):
        raise InvalidRun(f"pinned size drift: {label}")
    payload: dict[str, Any] | None = None
    if path.suffix == ".json":
        payload = parse_unique_json_bytes(path, raw)
        loaded_json[label] = payload
        expected_self = specification.get(
            "result_payload_sha256_without_self", specification.get("self_digest")
        )
        if expected_self is not None:
            observed_self = verify_self_digest(payload, label=label)
            if observed_self != str(expected_self):
                raise InvalidRun(f"pinned self digest drift: {label}")
        required_status = specification.get(
            "required_run_status", specification.get("run_status")
        )
        if required_status is not None and payload.get("run_status") != required_status:
            raise InvalidRun(f"pinned run status drift: {label}")
        required_classification = specification.get(
            "required_classification", specification.get("classification")
        )
        if (
            required_classification is not None
            and payload.get("classification") != required_classification
        ):
            raise InvalidRun(f"pinned classification drift: {label}")
    blob_guard = committed_blob_guard(relative, commit)
    expected_blob = _pin_blob(specification)
    if expected_blob is not None and (
        blob_guard["working_blob_oid"] != expected_blob
        or blob_guard["committed_blob_oid"] != expected_blob
    ):
        raise InvalidRun(f"pinned Git blob drift: {label}")
    return (
        {
            "path": relative,
            "commit": commit,
            "sha256": observed_sha,
            "size_bytes": len(raw),
            "git_blob_oid": blob_guard["working_blob_oid"],
            "strict_JSON": payload is not None,
            "self_digest_verified": bool(
                payload is not None
                and (
                    "result_payload_sha256_without_self" in specification
                    or "self_digest" in specification
                )
            ),
            **blob_guard,
        },
        path,
    )


def _find_direct_payload(
    loaded: Mapping[str, dict[str, Any]], label: str
) -> dict[str, Any]:
    if label not in loaded:
        raise InvalidRun(f"missing loaded JSON pin {label}")
    return loaded[label]


def _compare_duplicate_declarations(
    declarations: Mapping[str, list[tuple[str, Mapping[str, Any]]]]
) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for relative in sorted(declarations):
        records = declarations[relative]
        commits = {_pin_commit(spec, where=label) for label, spec in records}
        digests = {str(require(spec, "sha256", where=label)) for label, spec in records}
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
        ledger.append(
            {
                "path": relative,
                "declaration_roles": [label for label, _spec in records],
                "declaration_count": len(records),
                "commit_equal": len(commits) == 1,
                "sha256_equal": len(digests) == 1,
                "declared_size_equal_where_present": len(sizes) <= 1,
                "declared_blob_equal_where_present": len(blobs) <= 1,
            }
        )
    return ledger


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


def validate_inputs(*, authoritative: bool) -> InputBundle:
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    if len(manifest_raw) != INPUT_SIZE_BYTES:
        raise InvalidRun("Phase54 manifest size drift")
    if sha256_bytes(manifest_raw) != INPUT_SHA256:
        raise InvalidRun("Phase54 manifest SHA drift")
    if (
        manifest.get("schema")
        != "ice-phase54-p51-global-noncse-control-audit-inputs/v1"
        or manifest.get("phase") != 54
    ):
        raise InvalidRun("Phase54 manifest schema/phase drift")
    if manifest.get("manifest_introduction_commit") != INPUT_INTRODUCTION_COMMIT:
        raise InvalidRun("Phase54 manifest introduction-commit drift")
    checks = require(manifest, "checks", where="manifest")
    if tuple(require(checks, "exact", where="checks")) != EXACT_CHECK_IDS:
        raise InvalidRun("Phase54 exact check ID/order drift")
    if tuple(require(checks, "numerical", where="checks")) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("Phase54 numerical check ID/order drift")
    if tuple(manifest["stage_contract"]["order"]) != STAGE_ORDER:
        raise InvalidRun("Phase54 stage order drift")
    if tuple(manifest["evaluators"]["order"]) != EVALUATOR_ORDER:
        raise InvalidRun("Phase54 evaluator order drift")
    if not is_ancestor(INPUT_INTRODUCTION_COMMIT, INPUT_COMMIT):
        raise InvalidRun("manifest introduction commit is not an ancestor of bound commit")
    manifest_relative = str(INPUT_PATH.relative_to(REPO_ROOT))
    manifest_guard = committed_blob_guard(manifest_relative, INPUT_COMMIT)
    if manifest_guard["working_blob_oid"] != INPUT_BLOB_OID:
        raise InvalidRun("Phase54 manifest bound blob drift")

    observed_runtime = validate_runtime(manifest)
    loaded: dict[str, dict[str, Any]] = {}
    observed: dict[str, Any] = {}
    consumed: set[Path] = {INPUT_PATH, SCRIPT_PATH}
    direct = require(manifest, "pinned_inputs", where="manifest")
    expected_direct = (
        "phase52_manifest",
        "phase52_runner",
        "phase52_result",
        "phase53_manifest",
        "phase53_runner",
        "phase53_result",
    )
    if tuple(direct) != expected_direct:
        raise InvalidRun("Phase54 direct pinned-input key/order drift")
    declarations: dict[str, list[tuple[str, Mapping[str, Any]]]] = {}
    for label, specification in direct.items():
        if not isinstance(specification, Mapping):
            raise InvalidRun(f"invalid direct pin declaration: {label}")
        record, path = validate_pin(label, specification, loaded_json=loaded)
        observed[label] = record
        consumed.add(path)
        declarations.setdefault(record["path"], []).append((label, specification))

    p52_manifest = _find_direct_payload(loaded, "phase52_manifest")
    p53_manifest = _find_direct_payload(loaded, "phase53_manifest")
    p52_result = _find_direct_payload(loaded, "phase52_result")
    p53_result = _find_direct_payload(loaded, "phase53_result")
    for parent_label, parent in (
        ("phase52_manifest", p52_manifest),
        ("phase53_manifest", p53_manifest),
    ):
        nested = require(parent, "pinned_inputs", where=parent_label)
        for child_label, specification in nested.items():
            if not isinstance(specification, Mapping):
                raise InvalidRun(f"invalid transitive pin {parent_label}.{child_label}")
            role = f"{parent_label}::{child_label}"
            relative = str(require(specification, "path", where=role))
            declarations.setdefault(relative, []).append((role, specification))

    duplicate_ledger = _compare_duplicate_declarations(declarations)
    # Validate every unique transitive declaration in addition to the six
    # direct Phase-54 artifacts.  Prefer the richer declaration where the same
    # path is named by both inherited manifests.
    for relative in sorted(declarations):
        if relative in {record["path"] for record in observed.values()}:
            continue
        choices = declarations[relative]
        label, specification = max(
            choices,
            key=lambda item: (
                "git_blob_oid" in item[1],
                "size_bytes" in item[1],
                "result_payload_sha256_without_self" in item[1],
            ),
        )
        record, path = validate_pin(label, specification, loaded_json=loaded)
        observed[label] = record
        consumed.add(path)

    if p52_result.get("run_status") != "VALID_RUN" or p53_result.get(
        "run_status"
    ) != "VALID_RUN":
        raise InvalidRun("pinned Phase52/53 result status drift")
    if p52_result.get("classification") != direct["phase52_result"].get(
        "required_classification"
    ):
        raise InvalidRun("pinned Phase52 classification drift")
    if p53_result.get("classification") != direct["phase53_result"].get(
        "required_classification"
    ):
        raise InvalidRun("pinned Phase53 classification drift")

    runner_guard: dict[str, Any] = {
        "authoritative": authoritative,
        "runner_sha256_at_start": sha256_path(SCRIPT_PATH),
        "runner_commit": None,
        "runner_clean": None,
        "manifest_introduction_is_ancestor_of_bound_manifest": True,
        "manifest_bound_commit": INPUT_COMMIT,
        "manifest_bound_blob_oid": INPUT_BLOB_OID,
        "manifest_commit_blob_guard": manifest_guard,
        "cross_manifest_declarations": duplicate_ledger,
    }
    if authoritative:
        runner_relative = str(SCRIPT_PATH.relative_to(REPO_ROOT))
        dirty = git_output("status", "--porcelain=v1", "--", runner_relative)
        commit = git_output("log", "-1", "--format=%H", "--", runner_relative)
        if not commit or dirty:
            raise InvalidRun("authoritative Phase54 runner must be committed and clean")
        if commit == INPUT_COMMIT or not is_ancestor(INPUT_COMMIT, commit):
            raise InvalidRun("Phase54 runner commit must descend from the bound manifest")
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
        loaded_json=loaded,
        p52_manifest=p52_manifest,
        p53_manifest=p53_manifest,
        p52_result=p52_result,
        p53_result=p53_result,
        runner_guard=runner_guard,
        consumed_paths=tuple(sorted(consumed)),
    )


def post_rehash(bundle: InputBundle) -> dict[str, Any]:
    observed: list[dict[str, Any]] = []
    initial_by_path = {
        str(record["path"]): str(record["sha256"])
        for record in bundle.observed_pins.values()
    }
    initial_by_path[str(INPUT_PATH.relative_to(REPO_ROOT))] = INPUT_SHA256
    initial_by_path[str(SCRIPT_PATH.relative_to(REPO_ROOT))] = str(
        bundle.runner_guard["runner_sha256_at_start"]
    )
    for path in bundle.consumed_paths:
        relative = str(path.relative_to(REPO_ROOT))
        digest = sha256_path(path)
        expected = initial_by_path.get(relative)
        if expected is None or digest != expected:
            raise InvalidRun(f"post-evaluation byte drift: {relative}")
        observed.append(
            {"path": relative, "sha256": digest, "unchanged_after_evaluation": True}
        )
    return {"count": len(observed), "records": observed, "all_unchanged": True}


def loaded_json_by_basename(bundle: InputBundle, basename: str) -> dict[str, Any]:
    matches = [
        bundle.loaded_json[label]
        for label, record in bundle.observed_pins.items()
        if label in bundle.loaded_json and Path(str(record["path"])).name == basename
    ]
    # The same immutable JSON may have been validated through both inherited
    # manifests; object equality collapses those duplicate declarations.
    unique: list[dict[str, Any]] = []
    for item in matches:
        if not any(item == prior for prior in unique):
            unique.append(item)
    if len(unique) != 1:
        raise InvalidRun(f"expected one pinned JSON payload named {basename}")
    return unique[0]


@dataclass
class TopologyGuard:
    saddle_solve_count: int = 0
    root_solve_count: int = 0
    ODE_integration_count: int = 0
    trajectory_fraction_count: int = 0
    continuation_or_classification_replay_count: int = 0

    def record(self) -> dict[str, Any]:
        return {
            "saddle_solve_count": self.saddle_solve_count,
            "root_solve_count": self.root_solve_count,
            "ODE_integration_count": self.ODE_integration_count,
            "trajectory_fraction_count": self.trajectory_fraction_count,
            "continuation_or_classification_replay_count": (
                self.continuation_or_classification_replay_count
            ),
        }


def install_static_only_guards(p51: ModuleType, topology: TopologyGuard) -> None:
    def prohibited_root(*_args: Any, **_kwargs: Any) -> Any:
        topology.root_solve_count += 1
        raise InvalidRun("Phase54 prohibits every root/saddle solve")

    def prohibited_ode(*_args: Any, **_kwargs: Any) -> Any:
        topology.ODE_integration_count += 1
        raise InvalidRun("Phase54 prohibits every ODE integration")

    # These are the names resolved by SourceContext.saddle and integrate_k in
    # the pinned Phase-51 module.  Phase54 never calls either route.
    p51.root = prohibited_root
    p51.solve_ivp = prohibited_ode


@dataclass(frozen=True)
class StaticSetup:
    p51: ModuleType
    p52: ModuleType
    p53: ModuleType
    contexts: tuple[Any, ...]
    evaluators: Mapping[str, Any]
    phase52_symbolic_ledger: Mapping[str, Any]
    topology: TopologyGuard
    phase51_context_audit: Mapping[str, Any]


def build_static_setup(bundle: InputBundle) -> StaticSetup:
    progress("loading pinned Phase51/52/53 implementations")
    p51 = load_module("ice_phase51_for_phase54", P51_RUNNER_PATH)
    p52 = load_module("ice_phase52_for_phase54", P52_RUNNER_PATH)
    p53 = load_module("ice_phase53_for_phase54", P53_RUNNER_PATH)
    topology = TopologyGuard()
    install_static_only_guards(p51, topology)
    p51_manifest = loaded_json_by_basename(
        bundle, "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json"
    )
    contexts_raw, p51_context_audit = p52.build_phase51_contexts(p51, p51_manifest)
    contexts = tuple(contexts_raw)
    if tuple(source.label for source in contexts) != SOURCE_ORDER:
        raise InvalidRun("Phase51 source-context order drift")
    if topology.record() != {
        "saddle_solve_count": 0,
        "root_solve_count": 0,
        "ODE_integration_count": 0,
        "trajectory_fraction_count": 0,
        "continuation_or_classification_replay_count": 0,
    }:
        raise InvalidRun("static context construction crossed a prohibited topology")
    progress("binding global and element-local symbolic evaluator plans")
    evaluators, ledger = p52.build_symbolic_evaluators(p51, contexts)
    if tuple(evaluators) != SOURCE_ORDER:
        raise InvalidRun("symbolic evaluator source order drift")
    return StaticSetup(
        p51=p51,
        p52=p52,
        p53=p53,
        contexts=contexts,
        evaluators=evaluators,
        phase52_symbolic_ledger=ledger,
        topology=topology,
        phase51_context_audit=p51_context_audit,
    )


def canonical_state_bytes(record: Mapping[str, Any]) -> bytes:
    return json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def parse_frozen_state(
    p52: ModuleType, state_record: Mapping[str, Any], *, slot_key: str
) -> np.ndarray:
    if state_record.get("dtype") != str(np.dtype(np.clongdouble)):
        raise InvalidRun(f"Phase53 state dtype drift at {slot_key}")
    if state_record.get("shape") != [M5]:
        raise InvalidRun(f"Phase53 state shape drift at {slot_key}")
    pairs = state_record.get("clongdouble_decimal_pairs")
    if not isinstance(pairs, list) or len(pairs) != M5:
        raise InvalidRun(f"Phase53 decimal-pair count drift at {slot_key}")
    output = np.empty(M5, dtype=np.clongdouble)
    for index, pair in enumerate(pairs):
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or not all(isinstance(item, str) for item in pair)
        ):
            raise InvalidRun(f"invalid Phase53 decimal pair at {slot_key}[{index}]")
        real = np.longdouble(pair[0])
        imaginary = np.longdouble(pair[1])
        if not np.isfinite(real) or not np.isfinite(imaginary):
            raise InvalidRun(f"nonfinite Phase53 decimal pair at {slot_key}[{index}]")
        if p52.ld_text(real) != pair[0] or p52.ld_text(imaginary) != pair[1]:
            raise InvalidRun(f"Phase53 decimal round-trip drift at {slot_key}[{index}]")
        output[index] = np.clongdouble(real) + np.clongdouble("1j") * np.clongdouble(
            imaginary
        )
    return output


def static_factor(p51: ModuleType, source: Any, lambda_value: float) -> np.ndarray:
    mobility = p51.geodesic_spd(source.mobility0, source.mobility1, lambda_value)
    factor = (
        p51.symmetric_power(mobility, 0.5)
        @ p51.symmetric_power(source.mobility0, -0.5)
        @ source.factor0
    )
    if lambda_value == 0.0:
        factor = source.factor0.copy()
    factor_array = np.asarray(factor, dtype=float)
    if factor_array.shape != (M5, M5) or not np.all(np.isfinite(factor_array)):
        raise InvalidRun("static factor reconstruction failed")
    return factor_array


def build_static_slots(
    bundle: InputBundle, setup: StaticSetup
) -> tuple[list[Any], list[dict[str, Any]]]:
    source_records = require(
        require(
            bundle.p53_result,
            "six_slot_full_evaluator_reference",
            where="Phase53 result",
        ),
        "records",
        where="Phase53 six-slot reference",
    )
    frozen = require(require(bundle.manifest, "slots", where="manifest"), "records", where="slots")
    if len(source_records) != 6 or len(frozen) != 6:
        raise InvalidRun("Phase53/Phase54 six-slot count drift")
    contexts = {source.label: source for source in setup.contexts}
    slots: list[Any] = []
    ledger: list[dict[str, Any]] = []
    expected_order = [
        (source_label, lambda_value)
        for source_label in SOURCE_ORDER
        for lambda_value in LAMBDA_ORDER
    ]
    for index, ((source_label, lambda_value), result_record, frozen_record) in enumerate(
        zip(expected_order, source_records, frozen, strict=True)
    ):
        expected_key = f"{source_label}:lambda={lambda_value:.1f}"
        if (
            result_record.get("slot") != expected_key
            or result_record.get("source") != source_label
            or float(result_record.get("lambda")) != lambda_value
            or frozen_record.get("slot") != expected_key
        ):
            raise InvalidRun(f"Phase53 slot order/label drift at index {index}")
        state_record = require(
            result_record, "input_state_w5", where=f"Phase53 slot {expected_key}"
        )
        state_bytes = canonical_state_bytes(state_record)
        state_digest = sha256_bytes(state_bytes)
        if (
            len(state_bytes) != int(frozen_record["state_canonical_bytes"])
            or state_digest != frozen_record["state_sha256"]
        ):
            raise InvalidRun(f"Phase53 frozen state digest drift at {expected_key}")
        state5 = parse_frozen_state(setup.p52, state_record, slot_key=expected_key)
        source = contexts[source_label]
        inverse = np.asarray(source.evaluator.inverse_basis_long, dtype=np.longdouble)
        coordinates = inverse @ (
            state5 - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
        )
        state4 = np.asarray(source.evaluator.anchor4, dtype=np.clongdouble) + coordinates[:M4]
        factor = static_factor(setup.p51, source, lambda_value)
        node = SimpleNamespace(factor=factor)
        slot = setup.p52.Slot(
            source=source,
            node=node,
            source_label=source_label,
            lambda_value=lambda_value,
            state_w5=state5,
            state_w4=np.asarray(state4, dtype=np.clongdouble),
        )
        if slot.key != expected_key:
            raise InvalidRun(f"constructed slot key drift at {expected_key}")
        slots.append(slot)
        ledger.append(
            {
                "index": index,
                "slot": expected_key,
                "source": source_label,
                "lambda": lambda_value,
                "state_pointer": (
                    f"/six_slot_full_evaluator_reference/records/{index}/input_state_w5"
                ),
                "state_canonical_bytes": len(state_bytes),
                "state_sha256": state_digest,
                "input_state_w5_decimal_pairs": [
                    [str(pair[0]), str(pair[1])]
                    for pair in state_record["clongdouble_decimal_pairs"]
                ],
                "input_state_w5": state5,
                "derived_state_w4": np.asarray(state4, dtype=np.clongdouble),
                "factor_sha256": sha256_bytes(
                    np.asarray(factor, dtype="<f8").tobytes()
                ),
                "saddle_or_root_used": False,
            }
        )
    return slots, ledger


def scalar_record(p52: ModuleType, value: Any) -> dict[str, Any]:
    array = np.asarray(value)
    if not np.all(np.isfinite(array)):
        raise InvalidRun("nonfinite traced scalar")
    return {"dtype": p52.scalar_dtype(value), "value": json_ready(value)}


@dataclass(frozen=True)
class RawCall:
    values: tuple[Any, ...]
    trace: Mapping[str, Any]
    invocation_result: Any


def trace_raw_callable(
    p52: ModuleType,
    callable_set: Any,
    values: Sequence[Any],
    *,
    invoker: Callable[[], Any] | None = None,
) -> RawCall:
    """Capture a lambdified return before any wrapper coercion.

    ``invoker`` is used for the two actual Phase-51 LongCallableSet.evaluate
    routes, so the captured callable is nested inside the historical wrapper
    rather than called as a look-alike.
    """
    captured_locals: dict[str, Any] = {}
    captured_returns: list[Any] = []
    target_code = callable_set.function.__code__
    previous = sys.gettrace()
    if previous is not None:
        raise InvalidRun("preexisting Python trace hook makes raw audit ambiguous")

    def tracer(frame: Any, event: str, argument: Any) -> Any:
        if frame.f_code is target_code:
            if event == "return":
                captured_locals.update(frame.f_locals)
                captured_returns.append(argument)
            return tracer
        return tracer if event == "call" and frame.f_code is target_code else None

    try:
        sys.settrace(tracer)
        invocation_result = (
            callable_set.function(tuple(values)) if invoker is None else invoker()
        )
    finally:
        sys.settrace(previous)
    if len(captured_returns) != 1:
        raise InvalidRun("raw callable trace did not capture exactly one return")
    raw = captured_returns[0]
    if type(raw) not in (list, tuple):
        raise InvalidRun("raw generated-callable output container drift")
    temporaries = {
        name: value
        for name, value in captured_locals.items()
        if TEMPORARY_NAME.fullmatch(name)
    }
    expected_names = {str(symbol) for symbol, _expression in callable_set.replacements}
    if set(temporaries) != expected_names:
        raise InvalidRun(
            f"raw CSE temporary-name drift: {sorted(temporaries)} != {sorted(expected_names)}"
        )
    raw_values = tuple(p52.flatten_raw(raw))
    temporary_records = [
        {"role": name, **scalar_record(p52, temporaries[name])}
        for name in sorted(temporaries, key=lambda item: int(item[1:]))
    ]
    raw_records = [
        {"output_index": index, **scalar_record(p52, value)}
        for index, value in enumerate(raw_values)
    ]
    raw_dtype_counts: dict[str, int] = {}
    for record in raw_records:
        dtype = str(record["dtype"])
        raw_dtype_counts[dtype] = raw_dtype_counts.get(dtype, 0) + 1
    temporary_dtype_counts: dict[str, int] = {}
    for record in temporary_records:
        dtype = str(record["dtype"])
        temporary_dtype_counts[dtype] = temporary_dtype_counts.get(dtype, 0) + 1
    return RawCall(
        values=raw_values,
        invocation_result=invocation_result,
        trace={
            "replacement_count": callable_set.replacement_count,
            "traced_temporary_count": len(temporary_records),
            "temporary_dtype_counts": temporary_dtype_counts,
            "temporary_records": temporary_records,
            "all_temporary_scalars_exact_clongdouble": all(
                type(value) is np.clongdouble for value in temporaries.values()
            ),
            "raw_output_count": len(raw_records),
            "raw_output_container_type": type(raw).__name__,
            "raw_output_dtype_counts": raw_dtype_counts,
            "raw_output_records": raw_records,
            "all_raw_scalars_exact_clongdouble": all(
                type(value) is np.clongdouble for value in raw_values
            ),
            "replacement_names_exact": True,
            "return_alias_captured_exactly_once": True,
            "source_sha256": callable_set.source_sha256,
            "dag_sha256": callable_set.dag_sha256,
        },
    )


@dataclass(frozen=True)
class DimensionBindings:
    dimension: int
    GN_std: Any
    GN_long: Any
    EL_std: tuple[Any, ...]
    EL_long: tuple[Any, ...]
    phase51_global_CSE_context: Any
    phase52_long_namespace_joint_CSE_context: Any


@dataclass(frozen=True)
class SourceBindings:
    source_label: str
    m4: DimensionBindings
    m5: DimensionBindings


def make_long_plain_joint(p52: ModuleType, dimension: Any) -> Any:
    outputs = tuple(dimension.baseline_plain.outputs)
    variables = tuple(dimension.variables)
    function = sp.lambdify(
        (variables,),
        outputs,
        modules=p52.LONG_MODULES,
        cse=False,
        printer=p52.LongNumPyPrinter(),
    )
    source = inspect.getsource(function)
    if "numpy." in source or "np." in source:
        raise InvalidRun("GN_long source contains a NumPy namespace fallback")
    undeclared = set(function.__code__.co_names) - set(p52.LONG_MODULES)
    if undeclared:
        raise InvalidRun(f"GN_long used undeclared generated globals: {sorted(undeclared)}")
    dag = sp.srepr(sp.Tuple(*outputs))
    callable_set = p52.GeneratedCallable(
        function=function,
        replacements=(),
        reduced=outputs,
        outputs=outputs,
        source_sha256=sha256_bytes(source.encode("utf-8")),
        dag_sha256=sha256_bytes(dag.encode("utf-8")),
    )
    if callable_set.dag_sha256 != dimension.baseline_plain.dag_sha256:
        raise InvalidRun("GN_long changed the unreduced joint output tuple/DAG")
    if tuple(callable_set.outputs) != tuple(dimension.baseline_plain.outputs):
        raise InvalidRun("GN_long changed joint output arity/order")
    if not p52.exact_back_substitution(callable_set):
        raise InvalidRun("GN_long non-CSE back-substitution failed")
    return callable_set


def element_plan_equal(left: Any, right: Any) -> bool:
    return bool(
        tuple(left.outputs) == tuple(right.outputs)
        and tuple(left.replacements) == tuple(right.replacements)
        and tuple(left.reduced) == tuple(right.reduced)
        and left.replacement_count == right.replacement_count
        and left.dag_sha256 == right.dag_sha256
    )


def build_dimension_bindings(p52: ModuleType, dimension: Any) -> DimensionBindings:
    expected_joint_count = dimension.dimension + dimension.dimension**2
    if (
        len(dimension.baseline_plain.outputs) != expected_joint_count
        or len(dimension.baseline_joint.outputs) != expected_joint_count
        or len(dimension.long_joint.outputs) != expected_joint_count
    ):
        raise InvalidRun("global joint gradient-plus-Hessian output arity drift")
    gn_long = make_long_plain_joint(p52, dimension)
    standard_elements = tuple(
        p52.make_generated_callable(
            expressions, dimension.variables, long_namespace=False
        )
        for expressions in dimension.element_gradients
    )
    if len(standard_elements) != len(dimension.element_long):
        raise InvalidRun("EL_std/EL_long element count drift")
    for index, (standard, long) in enumerate(
        zip(standard_elements, dimension.element_long, strict=True)
    ):
        if not element_plan_equal(standard, long):
            raise InvalidRun(f"EL_std changed the canonical element plan at {index}")
        if not p52.exact_back_substitution(standard) or not p52.exact_back_substitution(
            long
        ):
            raise InvalidRun(f"element plan back-substitution failed at {index}")
        if standard.source_sha256 == long.source_sha256:
            raise InvalidRun(f"EL_std falsely reused the EL_long generated source at {index}")
    return DimensionBindings(
        dimension=dimension.dimension,
        GN_std=dimension.baseline_plain,
        GN_long=gn_long,
        EL_std=standard_elements,
        EL_long=tuple(dimension.element_long),
        phase51_global_CSE_context=dimension.baseline_joint,
        phase52_long_namespace_joint_CSE_context=dimension.long_joint,
    )


def element_ledger(callables: Sequence[Any], p52: ModuleType) -> list[dict[str, Any]]:
    return [
        {
            "index": index,
            "replacement_count": callable_set.replacement_count,
            "dag_sha256": callable_set.dag_sha256,
            "source_sha256": callable_set.source_sha256,
            "back_substitution": p52.exact_back_substitution(callable_set),
        }
        for index, callable_set in enumerate(callables)
    ]


def build_projection(
    source_bindings: Mapping[str, SourceBindings], p52: ModuleType
) -> dict[str, Any]:
    return {
        "source_order": list(SOURCE_ORDER),
        "elements": [
            {
                "source": source_label,
                "m4": element_ledger(source_bindings[source_label].m4.EL_long, p52),
                "m5": element_ledger(source_bindings[source_label].m5.EL_long, p52),
            }
            for source_label in SOURCE_ORDER
        ],
    }


def callable_binding_record(
    p52: ModuleType,
    dimension: Any,
    bindings: DimensionBindings,
    source: Any,
    dimension_name: str,
) -> dict[str, Any]:
    historical_set = getattr(source.evaluator, dimension_name)
    historical_plain = historical_set.joint_plain
    historical_cse = historical_set.joint_cse
    return {
        "dimension": bindings.dimension,
        "joint_output_arity": bindings.dimension + bindings.dimension**2,
        "joint_output_order": "gradient_then_row_major_Hessian",
        "GN_std": {
            "role": "actual_pinned_Phase51_LongCallableSet.evaluate_plain_joint",
            "actual_historical_joint_plain_callable_bound": (
                bindings.GN_std.function is historical_plain
            ),
            "source_sha256": bindings.GN_std.source_sha256,
            "dag_sha256": bindings.GN_std.dag_sha256,
            "replacement_count": bindings.GN_std.replacement_count,
            "back_substitution": p52.exact_back_substitution(bindings.GN_std),
            "post_call_boundary": "LongCallableSet_np_asarray_clongdouble",
        },
        "GN_long": {
            "role": "same_unreduced_joint_tuple_LongNumPyPrinter_LONG_MODULES",
            "same_outputs_as_GN_std": (
                tuple(bindings.GN_long.outputs) == tuple(bindings.GN_std.outputs)
            ),
            "same_DAG_as_GN_std": (
                bindings.GN_long.dag_sha256 == bindings.GN_std.dag_sha256
            ),
            "distinct_generated_source_from_GN_std": (
                bindings.GN_long.source_sha256 != bindings.GN_std.source_sha256
            ),
            "source_sha256": bindings.GN_long.source_sha256,
            "dag_sha256": bindings.GN_long.dag_sha256,
            "replacement_count": bindings.GN_long.replacement_count,
            "back_substitution": p52.exact_back_substitution(bindings.GN_long),
            "post_call_boundary": "np_asarray_clongdouble_same_as_historical",
        },
        "EL_std": {
            "role": "canonical_element_CSE_standard_NumPy_complex128_LTR",
            "element_count": len(bindings.EL_std),
            "elements": element_ledger(bindings.EL_std, p52),
            "plans_equal_EL_long": all(
                element_plan_equal(left, right)
                for left, right in zip(bindings.EL_std, bindings.EL_long, strict=True)
            ),
            "all_generated_sources_distinct_from_EL_long": all(
                left.source_sha256 != right.source_sha256
                for left, right in zip(bindings.EL_std, bindings.EL_long, strict=True)
            ),
            "accumulator_dtype": "complex128",
            "post_complete_sum_boundary": "np_asarray_clongdouble",
        },
        "EL_long": {
            "role": "exact_Phase53_production_gradient_projection",
            "element_count": len(bindings.EL_long),
            "elements": element_ledger(bindings.EL_long, p52),
            "accumulator_dtype": str(np.dtype(np.clongdouble)),
            "fixed_sum_implementation_role": "Phase53.fixed_array_sum",
        },
        "phase51_global_CSE_context": {
            "role": "actual_pinned_Phase51_LongCallableSet.evaluate_CSE_joint",
            "actual_historical_joint_CSE_callable_bound": (
                bindings.phase51_global_CSE_context.function is historical_cse
            ),
            "source_sha256": bindings.phase51_global_CSE_context.source_sha256,
            "dag_sha256": bindings.phase51_global_CSE_context.dag_sha256,
            "replacement_count": (
                bindings.phase51_global_CSE_context.replacement_count
            ),
            "back_substitution": p52.exact_back_substitution(
                bindings.phase51_global_CSE_context
            ),
        },
        "phase52_long_namespace_joint_CSE_context": {
            "role": "Phase52_LongNumPyPrinter_LONG_MODULES_joint_CSE",
            "source_sha256": (
                bindings.phase52_long_namespace_joint_CSE_context.source_sha256
            ),
            "dag_sha256": (
                bindings.phase52_long_namespace_joint_CSE_context.dag_sha256
            ),
            "replacement_count": (
                bindings.phase52_long_namespace_joint_CSE_context.replacement_count
            ),
            "same_CSE_DAG_as_Phase51_context": (
                bindings.phase52_long_namespace_joint_CSE_context.dag_sha256
                == bindings.phase51_global_CSE_context.dag_sha256
            ),
            "back_substitution": p52.exact_back_substitution(
                bindings.phase52_long_namespace_joint_CSE_context
            ),
        },
    }


def build_evaluator_bindings(
    bundle: InputBundle, setup: StaticSetup
) -> tuple[dict[str, SourceBindings], dict[str, Any]]:
    output: dict[str, SourceBindings] = {}
    ledger: dict[str, Any] = {}
    contexts = {source.label: source for source in setup.contexts}
    for source_label in SOURCE_ORDER:
        source_evaluators = setup.evaluators[source_label]
        bindings = SourceBindings(
            source_label=source_label,
            m4=build_dimension_bindings(setup.p52, source_evaluators.m4),
            m5=build_dimension_bindings(setup.p52, source_evaluators.m5),
        )
        output[source_label] = bindings
        ledger[source_label] = {
            "m4": callable_binding_record(
                setup.p52,
                source_evaluators.m4,
                bindings.m4,
                contexts[source_label],
                "m4",
            ),
            "m5": callable_binding_record(
                setup.p52,
                source_evaluators.m5,
                bindings.m5,
                contexts[source_label],
                "m5",
            ),
        }
    projection = build_projection(output, setup.p52)
    projection_bytes = canonical_bytes(projection)
    projection_digest = sha256_bytes(projection_bytes)
    p53_audit = require(
        bundle.p53_result, "symbolic_evaluator_audit", where="Phase53 result"
    )
    if (
        projection_digest != EXPECTED_PROJECTION_SHA256
        or len(projection_bytes) != EXPECTED_PROJECTION_BYTES
        or projection != p53_audit.get("generated_projection")
        or projection_digest != p53_audit.get("Phase53_generated_projection_sha256")
        or projection_digest != p53_audit.get("Phase52_projection_sha256")
        or int(p53_audit.get("projection_canonical_bytes", -1))
        != EXPECTED_PROJECTION_BYTES
    ):
        raise InvalidRun("EL_long Phase53 production projection binding drift")
    expected_from_p52 = {
        "source_order": list(SOURCE_ORDER),
        "elements": [
            {
                "source": source_label,
                "m4": bundle.p52_result["symbolic_evaluator_ledger"][source_label][
                    "elements"
                ]["m4"],
                "m5": bundle.p52_result["symbolic_evaluator_ledger"][source_label][
                    "elements"
                ]["m5"],
            }
            for source_label in SOURCE_ORDER
        ],
    }
    if projection != expected_from_p52:
        raise InvalidRun("EL_long projection differs from pinned Phase52 ledger")
    def core_dimension_gates(record: Mapping[str, Any]) -> bool:
        return bool(
            record["GN_std"]["actual_historical_joint_plain_callable_bound"]
            and record["GN_std"]["back_substitution"]
            and record["GN_long"]["same_outputs_as_GN_std"]
            and record["GN_long"]["same_DAG_as_GN_std"]
            and record["GN_long"]["distinct_generated_source_from_GN_std"]
            and record["GN_long"]["back_substitution"]
            and record["EL_std"]["plans_equal_EL_long"]
            and record["EL_std"]["all_generated_sources_distinct_from_EL_long"]
            and all(
                bool(element["back_substitution"])
                for element in record["EL_std"]["elements"]
            )
            and bool(record["EL_long"]["element_count"])
            and all(
                bool(element["back_substitution"])
                for element in record["EL_long"]["elements"]
            )
        )

    def contextual_dimension_gates(record: Mapping[str, Any]) -> bool:
        return bool(
            record["phase51_global_CSE_context"][
                "actual_historical_joint_CSE_callable_bound"
            ]
            and record["phase51_global_CSE_context"]["back_substitution"]
            and record["phase52_long_namespace_joint_CSE_context"][
                "same_CSE_DAG_as_Phase51_context"
            ]
            and record["phase52_long_namespace_joint_CSE_context"][
                "back_substitution"
            ]
        )

    core_bindings = all(
        core_dimension_gates(record[dimension_name])
        for record in ledger.values()
        for dimension_name in ("m4", "m5")
    )
    contextual_bindings = all(
        contextual_dimension_gates(record[dimension_name])
        for record in ledger.values()
        for dimension_name in ("m4", "m5")
    )
    all_bindings = core_bindings and contextual_bindings
    if not all_bindings:
        raise InvalidRun("one or more evaluator binding invariants failed")
    return output, {
        "source_order": list(SOURCE_ORDER),
        "by_source": ledger,
        "Phase53_production_projection": projection,
        "Phase53_production_projection_sha256": projection_digest,
        "Phase53_production_projection_canonical_bytes": len(projection_bytes),
        "projection_byte_identical_to_Phase52_and_Phase53": True,
        "all_core_DAG_source_and_back_substitution_gates_passed": core_bindings,
        "all_contextual_DAG_and_back_substitution_gates_passed": (
            contextual_bindings
        ),
        "all_recorded_evaluator_binding_gates_passed": all_bindings,
        "callable_relationship_evidence_policy": (
            "stable role labels, source/DAG hashes, and equivalence booleans only"
        ),
        "numeric_Python_id_values_serialized": False,
    }


def fixed_complex128_sum(
    contributions: Sequence[np.ndarray], dimension: int
) -> np.ndarray:
    total = np.zeros(dimension, dtype=np.complex128)
    for contribution in contributions:
        values = np.asarray(contribution, dtype=np.complex128).reshape(dimension)
        for index in range(dimension):
            total[index] = np.complex128(total[index] + values[index])
    return total


def raw_vector_without_coercion(values: Sequence[Any]) -> np.ndarray:
    output = np.asarray(tuple(values))
    if output.ndim != 1 or not np.all(np.isfinite(output)):
        raise InvalidRun("raw complete gradient could not be retained as a finite vector")
    return output


def evaluate_joint_dimension(
    setup: StaticSetup,
    source: Any,
    dimension_name: str,
    bindings: DimensionBindings,
    values: np.ndarray,
    variant: str,
) -> dict[str, Any]:
    dimension = bindings.dimension
    output_count = dimension + dimension**2
    historical = getattr(source.evaluator, dimension_name)
    if variant == "GN_std":
        callable_set = bindings.GN_std
        raw_call = trace_raw_callable(
            setup.p52,
            callable_set,
            values,
            invoker=lambda: historical.evaluate(values, plain=True),
        )
        action, historical_gradient, historical_hessian = raw_call.invocation_result
        post_boundary = np.asarray(raw_call.values, dtype=np.clongdouble).reshape(
            output_count
        )
        if not np.array_equal(
            post_boundary[:dimension],
            np.asarray(historical_gradient, dtype=np.clongdouble),
        ) or not np.array_equal(
            post_boundary[dimension:].reshape(dimension, dimension),
            np.asarray(historical_hessian, dtype=np.clongdouble),
        ):
            raise InvalidRun("GN_std trace disagrees with LongCallableSet.evaluate")
        if not np.isfinite(action):
            raise InvalidRun("GN_std historical action side output is nonfinite")
        stage_ready = np.asarray(historical_gradient, dtype=np.clongdouble)
        wrapper = "actual_LongCallableSet.evaluate_plain_np_asarray_clongdouble"
        wrapper_equal = True
    elif variant == "phase51_global_CSE_context":
        callable_set = bindings.phase51_global_CSE_context
        raw_call = trace_raw_callable(
            setup.p52,
            callable_set,
            values,
            invoker=lambda: historical.evaluate(values, plain=False),
        )
        action, historical_gradient, historical_hessian = raw_call.invocation_result
        post_boundary = np.asarray(raw_call.values, dtype=np.clongdouble).reshape(
            output_count
        )
        if not np.array_equal(
            post_boundary[:dimension],
            np.asarray(historical_gradient, dtype=np.clongdouble),
        ) or not np.array_equal(
            post_boundary[dimension:].reshape(dimension, dimension),
            np.asarray(historical_hessian, dtype=np.clongdouble),
        ):
            raise InvalidRun("Phase51 global-CSE trace disagrees with evaluate")
        if not np.isfinite(action):
            raise InvalidRun("Phase51 global-CSE historical action side output is nonfinite")
        stage_ready = np.asarray(historical_gradient, dtype=np.clongdouble)
        wrapper = "actual_LongCallableSet.evaluate_CSE_np_asarray_clongdouble"
        wrapper_equal = True
    elif variant == "GN_long":
        callable_set = bindings.GN_long
        raw_call = trace_raw_callable(setup.p52, callable_set, values)
        post_boundary = np.asarray(raw_call.values, dtype=np.clongdouble).reshape(
            output_count
        )
        stage_ready = post_boundary[:dimension]
        wrapper = "declared_same_np_asarray_clongdouble_boundary"
        wrapper_equal = True
    elif variant == "phase52_long_namespace_joint_CSE_context":
        callable_set = bindings.phase52_long_namespace_joint_CSE_context
        raw_call = trace_raw_callable(setup.p52, callable_set, values)
        post_boundary = np.asarray(raw_call.values, dtype=np.clongdouble).reshape(
            output_count
        )
        stage_ready = post_boundary[:dimension]
        wrapper = "Phase52_joint_CSE_np_asarray_clongdouble_boundary"
        wrapper_equal = True
    else:
        raise InvalidRun(f"unknown joint evaluator variant: {variant}")
    if variant in (
        "GN_long",
        "phase52_long_namespace_joint_CSE_context",
    ) and not (
        raw_call.trace["all_temporary_scalars_exact_clongdouble"]
        and raw_call.trace["all_raw_scalars_exact_clongdouble"]
    ):
        raise InvalidRun(
            f"{variant} produced a non-clongdouble temporary or raw scalar "
            f"at {dimension_name}"
        )
    if len(raw_call.values) != output_count:
        raise InvalidRun(f"joint output-count drift for {variant}:{dimension_name}")
    raw_gradient = raw_vector_without_coercion(raw_call.values[:dimension])
    if stage_ready.dtype != np.dtype(np.clongdouble) or not np.all(
        np.isfinite(stage_ready)
    ):
        raise InvalidRun(f"stage-ready joint gradient dtype drift for {variant}")
    return {
        "variant": variant,
        "dimension": dimension_name,
        "raw_joint_output_count": output_count,
        "raw_joint_tuple_before_wrapper": raw_call.trace["raw_output_records"],
        "trace": raw_call.trace,
        "complete_raw_gradient_before_common_boundary": raw_gradient,
        "complete_raw_gradient_dtype": str(raw_gradient.dtype),
        "stage_ready_gradient": stage_ready,
        "stage_ready_gradient_dtype": str(stage_ready.dtype),
        "declared_wrapper_boundary": wrapper,
        "captured_post_boundary_equals_declared_path": wrapper_equal,
        "gradient_slice": [0, dimension],
        "Hessian_slice_retained_but_not_used": [dimension, output_count],
    }


def evaluate_element_dimension(
    setup: StaticSetup,
    dimension_name: str,
    bindings: DimensionBindings,
    values: np.ndarray,
    variant: str,
) -> dict[str, Any]:
    dimension = bindings.dimension
    if variant == "EL_std":
        callables = bindings.EL_std
        accumulator_dtype = np.dtype(np.complex128)
    elif variant == "EL_long":
        callables = bindings.EL_long
        accumulator_dtype = np.dtype(np.clongdouble)
    else:
        raise InvalidRun(f"unknown element evaluator variant: {variant}")
    contribution_arrays: list[np.ndarray] = []
    contribution_records: list[dict[str, Any]] = []
    traces: list[Mapping[str, Any]] = []
    for element_index, callable_set in enumerate(callables):
        raw_call = trace_raw_callable(setup.p52, callable_set, values)
        if len(raw_call.values) != dimension:
            raise InvalidRun(
                f"element gradient output-count drift at {variant}:{dimension_name}:{element_index}"
            )
        if variant == "EL_long" and not (
            raw_call.trace["all_temporary_scalars_exact_clongdouble"]
            and raw_call.trace["all_raw_scalars_exact_clongdouble"]
        ):
            raise InvalidRun(
                "EL_long produced a non-clongdouble temporary or raw scalar at "
                f"{dimension_name}:{element_index}"
            )
        raw_vector = raw_vector_without_coercion(raw_call.values)
        if variant == "EL_std":
            contribution = np.asarray(raw_vector, dtype=np.complex128)
        else:
            contribution = np.asarray(raw_vector, dtype=np.clongdouble)
        if not np.all(np.isfinite(contribution)):
            raise InvalidRun("element contribution became nonfinite")
        contribution_arrays.append(contribution)
        traces.append(raw_call.trace)
        contribution_records.append(
            {
                "element_index": element_index,
                "raw_contribution_before_coercion": raw_vector,
                "raw_contribution_dtype": str(raw_vector.dtype),
                "contribution_at_accumulator_boundary": contribution,
                "accumulator_boundary_dtype": str(contribution.dtype),
                "source_sha256": callable_set.source_sha256,
                "dag_sha256": callable_set.dag_sha256,
                "replacement_count": callable_set.replacement_count,
            }
        )
    if variant == "EL_std":
        summed = fixed_complex128_sum(contribution_arrays, dimension)
    else:
        # This is the exact production projection helper imported from Phase53.
        summed = setup.p53.fixed_array_sum(contribution_arrays, (dimension,))
    if summed.dtype != accumulator_dtype:
        raise InvalidRun(f"{variant} accumulator dtype drift")
    complete_before_boundary = np.asarray(summed).copy()
    stage_ready = np.asarray(complete_before_boundary, dtype=np.clongdouble)
    if stage_ready.dtype != np.dtype(np.clongdouble) or not np.all(
        np.isfinite(stage_ready)
    ):
        raise InvalidRun(f"stage-ready element gradient dtype drift for {variant}")
    return {
        "variant": variant,
        "dimension": dimension_name,
        "element_count": len(callables),
        "element_contributions": contribution_records,
        "traces": traces,
        "fixed_left_to_right_componentwise": True,
        "accumulator_dtype": str(accumulator_dtype),
        "complete_raw_gradient_before_common_boundary": complete_before_boundary,
        "complete_raw_gradient_dtype": str(complete_before_boundary.dtype),
        "stage_ready_gradient": stage_ready,
        "stage_ready_gradient_dtype": str(stage_ready.dtype),
        "declared_wrapper_boundary": (
            "complete_complex128_sum_then_np_asarray_clongdouble"
            if variant == "EL_std"
            else "complete_clongdouble_sum_already_at_common_boundary"
        ),
        "captured_post_boundary_equals_declared_path": True,
    }


def evaluate_native_slot(
    setup: StaticSetup,
    slot: Any,
    source_bindings: SourceBindings,
) -> dict[str, Any]:
    variants: dict[str, Any] = {}
    source = slot.source
    for variant in EVALUATOR_ORDER:
        if variant in ("EL_std", "EL_long"):
            result4 = evaluate_element_dimension(
                setup, "m4", source_bindings.m4, slot.state_w4, variant
            )
            result5 = evaluate_element_dimension(
                setup, "m5", source_bindings.m5, slot.state_w5, variant
            )
        else:
            result4 = evaluate_joint_dimension(
                setup,
                source,
                "m4",
                source_bindings.m4,
                slot.state_w4,
                variant,
            )
            result5 = evaluate_joint_dimension(
                setup,
                source,
                "m5",
                source_bindings.m5,
                slot.state_w5,
                variant,
            )
        stages = setup.p52.native_stages(
            slot,
            np.asarray(result4["stage_ready_gradient"], dtype=np.clongdouble),
            np.asarray(result5["stage_ready_gradient"], dtype=np.clongdouble),
        )
        if tuple(stages) != STAGE_ORDER:
            raise InvalidRun(f"native stage order drift at {slot.key}:{variant}")
        for stage, dimension in zip(STAGE_ORDER, STAGE_DIMENSIONS, strict=True):
            vector = np.asarray(stages[stage])
            if (
                vector.shape != (dimension,)
                or vector.dtype != np.dtype(np.clongdouble)
                or not np.all(np.isfinite(vector))
            ):
                raise InvalidRun(f"native stage shape/dtype drift at {slot.key}:{variant}:{stage}")
        variants[variant] = {
            "m4_call": result4,
            "m5_call": result5,
            "stages": stages,
            "common_downstream_arithmetic": (
                "Phase52.native_stages_clongdouble_inverse_lift_blend_ordinary_"
                "factor_transpose_single_outer_minus_conjugation"
            ),
        }
    if tuple(variants) != EVALUATOR_ORDER:
        raise InvalidRun("native evaluator order drift")
    return variants


def vector_digest(value: Any) -> dict[str, Any]:
    record = json_ready(np.asarray(value))
    raw = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return {"sha256": sha256_bytes(raw), "canonical_bytes": len(raw)}


def mp_vector_digest(p52: ModuleType, value: Sequence[Any], digits: int) -> dict[str, Any]:
    record = p52.mp_vector_record(value, digits=digits)
    raw = canonical_bytes(record)
    return {
        "sha256": sha256_bytes(raw),
        "canonical_bytes": len(raw),
        "retained_vector": record,
    }


def mp_comparison(left: Sequence[Any], right: Sequence[Any]) -> dict[str, Any]:
    if len(left) != len(right):
        raise InvalidRun("mp comparison vector-length mismatch")
    difference = [mp.mpc(a) - mp.mpc(b) for a, b in zip(left, right, strict=True)]
    left_norm = mp.sqrt(mp.fsum(abs(mp.mpc(item)) ** 2 for item in left))
    right_norm = mp.sqrt(mp.fsum(abs(mp.mpc(item)) ** 2 for item in right))
    difference_norm = mp.sqrt(mp.fsum(abs(item) ** 2 for item in difference))
    relative = difference_norm / max(left_norm, right_norm, mp.mpf("1e-100"))
    maximum = max((abs(item) for item in difference), default=mp.mpf("0"))
    return {
        "symmetric_relative_decimal": mp_text(relative),
        "difference_norm_absolute_decimal": mp_text(difference_norm),
        "difference_max_component_absolute_decimal": mp_text(maximum),
        "difference_vector": {
            "shape": [len(difference)],
            "mp_decimal_pairs": [
                [mp_text(item.real, 45), mp_text(item.imag, 45)]
                for item in difference
            ],
        },
    }


def stage_active(stage: str, lambda_value: float) -> bool:
    if stage in ("m4_raw_gradient", "m4_lifted_gradient"):
        return lambda_value != 1.0
    if stage == "m5_raw_gradient":
        return lambda_value != 0.0
    return True


def threshold_for_stage(_stage: str) -> Decimal:
    # Both frozen gradient and completed-RHS limits are 5e-10.  The explicit
    # stage field retained below still distinguishes their semantic roles.
    return NATIVE_THRESHOLD


def reference_slot_from_decimal_pairs(
    p52: ModuleType,
    slot: Any,
    evaluators: Any,
    digits: int,
    state_w5_decimal_pairs: Sequence[Sequence[str]],
) -> dict[str, Any]:
    """Evaluate the two symbolic references from the pinned JSON strings.

    In particular, the mpmath state is not reconstructed from
    ``slot.state_w5``.  Native clongdouble reconstruction is an independent
    Phase54 guard used only by the native evaluator matrix.
    """
    if digits not in (80, 120):
        raise InvalidRun(f"undeclared reference precision tier: {digits}")
    if len(state_w5_decimal_pairs) != M5:
        raise InvalidRun("direct mpmath state decimal-pair count drift")
    retained_pairs: list[list[str]] = []
    for index, pair in enumerate(state_w5_decimal_pairs):
        if (
            len(pair) != 2
            or not isinstance(pair[0], str)
            or not isinstance(pair[1], str)
        ):
            raise InvalidRun(f"invalid direct mpmath state pair at index {index}")
        retained_pairs.append([pair[0], pair[1]])

    with mp.workdps(digits + 30):
        state5: list[mp.mpc] = []
        for real_text, imaginary_text in retained_pairs:
            number = mp.mpc(mp.mpf(real_text), mp.mpf(imaginary_text))
            if not mp.isfinite(number.real) or not mp.isfinite(number.imag):
                raise InvalidRun("direct decimal-pair mpmath state is nonfinite")
            state5.append(number)

        source = slot.source
        inverse = p52.mp_matrix_real(source.evaluator.inverse_basis_long)
        anchor5 = p52.mp_vector(source.evaluator.anchor5)
        anchor4 = p52.mp_vector(source.evaluator.anchor4)
        coordinates = p52.mp_matvec(
            inverse,
            [state5[index] - anchor5[index] for index in range(M5)],
        )
        state4 = [anchor4[index] + coordinates[index] for index in range(M4)]
        direct4 = p52.direct_evalf_gradient(
            evaluators.m4.global_gradient,
            evaluators.m4.variables,
            state4,
            digits,
        )
        direct5 = p52.direct_evalf_gradient(
            evaluators.m5.global_gradient,
            evaluators.m5.variables,
            state5,
            digits,
        )
        cse4 = p52.direct_evalf_cse_gradient(
            evaluators.m4.reference_gradient_cse,
            evaluators.m4.variables,
            state4,
            digits,
        )
        cse5 = p52.direct_evalf_cse_gradient(
            evaluators.m5.reference_gradient_cse,
            evaluators.m5.variables,
            state5,
            digits,
        )

        def stages(
            gradient4: Sequence[Any], gradient5: Sequence[Any]
        ) -> dict[str, list[mp.mpc]]:
            gradient_c = [mp.mpc(value) for value in gradient4]
            gradient_c.extend(
                [
                    p52.mp_real(source.evaluator.kappa_a) * coordinates[7],
                    p52.mp_real(source.evaluator.kappa_phi) * coordinates[8],
                ]
            )
            lifted = p52.mp_matvec(inverse.T, gradient_c)
            lam = p52.mp_real(np.longdouble(slot.lambda_value))
            blended = [
                (mp.mpf(1) - lam) * lifted[index] + lam * gradient5[index]
                for index in range(M5)
            ]
            factor = p52.mp_matrix_real(slot.node.factor)
            contracted = p52.mp_matvec(factor.T, blended)
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
        input_mp_record = p52.mp_vector_record(state5, digits=digits)
        pair_bytes = json.dumps(
            retained_pairs,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        return {
            "digits": digits,
            "direct": direct_stages,
            "CSE": cse_stages,
            "CSE_to_direct_relative_by_stage": {
                stage: p52.mp_relative(cse_stages[stage], direct_stages[stage])
                for stage in STAGE_ORDER
            },
            "input_lift": {
                "state_w5_25_digit_pairs": retained_pairs,
                "state_w5_decimal_pairs_exact_from_Phase53_JSON": retained_pairs,
                "state_w5_decimal_sha256": sha256_bytes(pair_bytes),
                "state_w5_decimal_pairs_sha256": sha256_bytes(pair_bytes),
                "state_w5_mpmath_values": input_mp_record,
                "state_w5_constructed_directly_with_mpf_mpc": True,
                "state_w5_native_clongdouble_consumed_for_reference_lift": False,
                "native_evaluator_output_consumed": False,
                "w4_recomputed_entirely_in_mpmath": True,
            },
        }


def reference_independence_record(setup: StaticSetup) -> dict[str, Any]:
    reference_source = inspect.getsource(reference_slot_from_decimal_pairs)
    direct_source = inspect.getsource(setup.p52.direct_evalf_gradient)
    cse_source = inspect.getsource(setup.p52.direct_evalf_cse_gradient)
    native_source = inspect.getsource(setup.p52.native_stages)
    expressions: dict[str, Any] = {}
    for source_label in SOURCE_ORDER:
        evaluator = setup.evaluators[source_label]
        expressions[source_label] = {
            "m4_global_gradient_srepr_sha256": sha256_bytes(
                sp.srepr(sp.Tuple(*evaluator.m4.global_gradient)).encode("utf-8")
            ),
            "m5_global_gradient_srepr_sha256": sha256_bytes(
                sp.srepr(sp.Tuple(*evaluator.m5.global_gradient)).encode("utf-8")
            ),
            "m4_reference_CSE_DAG_sha256": evaluator.m4.reference_gradient_cse.dag_sha256,
            "m5_reference_CSE_DAG_sha256": evaluator.m5.reference_gradient_cse.dag_sha256,
            "m4_reference_CSE_back_substitution": setup.p52.exact_back_substitution(
                evaluator.m4.reference_gradient_cse
            ),
            "m5_reference_CSE_back_substitution": setup.p52.exact_back_substitution(
                evaluator.m5.reference_gradient_cse
            ),
        }
    direct_has_no_lambdify = "lambdify" not in direct_source
    cse_has_no_lambdify = "lambdify" not in cse_source
    reference_calls_both = (
        "direct_evalf_gradient" in reference_source
        and "direct_evalf_cse_gradient" in reference_source
    )
    native_not_called = "native_stages" not in reference_source
    direct_pair_lift_bound = (
        "mp.mpc(mp.mpf(real_text), mp.mpf(imaginary_text))" in reference_source
    )
    native_state_attribute_absent = (
        "state_w5" not in reference_slot_from_decimal_pairs.__code__.co_names
    )
    inherited_reference_slot_not_called = "p52.reference_slot(" not in reference_source
    reference_back_substitutions_passed = all(
        bool(record[f"{dimension}_reference_CSE_back_substitution"])
        for record in expressions.values()
        for dimension in ("m4", "m5")
    )
    if not (
        direct_has_no_lambdify
        and cse_has_no_lambdify
        and reference_calls_both
        and native_not_called
        and direct_pair_lift_bound
        and native_state_attribute_absent
        and inherited_reference_slot_not_called
        and reference_back_substitutions_passed
    ):
        raise InvalidRun("direct-reference independence source guard failed")
    return {
        "expression_sources": {
            "m4": "pinned phase41.numeric_model source-substituted global gradient",
            "m5": "pinned phase50.m5_numeric_model source-substituted global gradient",
        },
        "by_source": expressions,
        "direct_evalf_function_source_sha256": sha256_bytes(
            direct_source.encode("utf-8")
        ),
        "symbolic_CSE_evalf_function_source_sha256": sha256_bytes(
            cse_source.encode("utf-8")
        ),
        "reference_slot_function_source_sha256": sha256_bytes(
            reference_source.encode("utf-8")
        ),
        "native_stages_function_source_sha256": sha256_bytes(
            native_source.encode("utf-8")
        ),
        "unreduced_direct_path_has_no_lambdify": direct_has_no_lambdify,
        "symbolic_CSE_path_has_no_lambdify": cse_has_no_lambdify,
        "reference_calls_direct_and_symbolic_CSE_paths": reference_calls_both,
        "reference_does_not_call_native_stages": native_not_called,
        "state_lift_constructs_mpmath_directly_from_decimal_pair_strings": (
            direct_pair_lift_bound
        ),
        "state_lift_does_not_read_slot_state_w5": native_state_attribute_absent,
        "inherited_P52_reference_slot_not_called": inherited_reference_slot_not_called,
        "all_reference_CSE_back_substitution_gates_passed": (
            reference_back_substitutions_passed
        ),
        "native_output_consumed_by_reference": False,
        "independence_scope": "finite symbolic arithmetic only; not a physical model",
    }


def convention_binding_record(setup: StaticSetup) -> dict[str, Any]:
    native_source = inspect.getsource(setup.p52.native_stages)
    reference_source = inspect.getsource(reference_slot_from_decimal_pairs)
    native_ordinary = "slot.node.factor.T" in native_source
    native_outer = "-np.conjugate(contracted)" in native_source
    reference_ordinary = "factor.T" in reference_source
    reference_outer = "-mp.conj(value)" in reference_source
    hermitian_spelling_absent = all(
        token not in native_source + reference_source
        for token in ("conj().T", "conjugate().T", ".H")
    )
    if not all(
        (
            native_ordinary,
            native_outer,
            reference_ordinary,
            reference_outer,
            hermitian_spelling_absent,
        )
    ):
        raise InvalidRun("ordinary-transpose/single-conjugation source binding failed")
    return {
        "native_ordinary_factor_transpose_bound": native_ordinary,
        "native_single_outer_minus_conjugation_bound": native_outer,
        "reference_ordinary_factor_transpose_bound": reference_ordinary,
        "reference_single_outer_minus_conjugation_bound": reference_outer,
        "Hermitian_transpose_spelling_absent": hermitian_spelling_absent,
        "stage_order": list(STAGE_ORDER),
        "native_source_sha256": sha256_bytes(native_source.encode("utf-8")),
        "reference_source_sha256": sha256_bytes(reference_source.encode("utf-8")),
        "reference_implementation_role": (
            "Phase54_local_direct_decimal_pair_mpmath_reference"
        ),
    }


def evaluate_references(
    setup: StaticSetup,
    slots: Sequence[Any],
    state_decimal_pairs_by_slot: Mapping[str, Sequence[Sequence[str]]],
) -> tuple[
    dict[str, dict[int, Mapping[str, Any]]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    bool,
]:
    internal: dict[str, dict[int, Mapping[str, Any]]] = {}
    vector_ledger: list[dict[str, Any]] = []
    comparison_ledger: list[dict[str, Any]] = []
    all_passed = True
    if set(state_decimal_pairs_by_slot) != {slot.key for slot in slots}:
        raise InvalidRun("reference decimal-pair slot map drift")
    for slot in slots:
        progress(f"direct SymPy/mpmath references: {slot.key}")
        tiers: dict[int, Mapping[str, Any]] = {}
        for digits in (80, 120):
            reference = reference_slot_from_decimal_pairs(
                setup.p52,
                slot,
                setup.evaluators[slot.source_label],
                digits,
                state_decimal_pairs_by_slot[slot.key],
            )
            if reference.get("digits") != digits:
                raise InvalidRun(f"reference precision-tag drift at {slot.key}:{digits}")
            tiers[digits] = reference
            for reference_variant in ("direct", "CSE"):
                stages = reference[reference_variant]
                if tuple(stages) != STAGE_ORDER:
                    raise InvalidRun("reference stage order drift")
                for stage, dimension in zip(
                    STAGE_ORDER, STAGE_DIMENSIONS, strict=True
                ):
                    vector = stages[stage]
                    if len(vector) != dimension or any(
                        not mp.isfinite(mp.mpc(item).real)
                        or not mp.isfinite(mp.mpc(item).imag)
                        for item in vector
                    ):
                        raise InvalidRun("reference vector shape/finite drift")
                    vector_ledger.append(
                        {
                            "slot": slot.key,
                            "source": slot.source_label,
                            "lambda": slot.lambda_value,
                            "precision_decimal_digits": digits,
                            "reference_variant": reference_variant,
                            "stage": stage,
                            "dimension": dimension,
                            "vector": mp_vector_digest(
                                setup.p52, vector, digits=digits
                            ),
                        }
                    )
            for stage in STAGE_ORDER:
                with mp.workdps(160):
                    metric = mp_comparison(
                        reference["CSE"][stage], reference["direct"][stage]
                    )
                relative = exact_decimal(
                    metric["symmetric_relative_decimal"],
                    label=f"reference symbolic-CSE comparison {slot.key}:{digits}:{stage}",
                )
                passed = relative <= REFERENCE_THRESHOLD
                all_passed = all_passed and passed
                comparison_ledger.append(
                    {
                        "kind": "symbolic_CSE_vs_unreduced_direct",
                        "slot": slot.key,
                        "precision_decimal_digits": digits,
                        "stage": stage,
                        "threshold": "1e-40",
                        "metric": metric,
                        "passed": passed,
                    }
                )
        internal[slot.key] = tiers
        for stage in STAGE_ORDER:
            with mp.workdps(160):
                metric = mp_comparison(
                    tiers[80]["direct"][stage], tiers[120]["direct"][stage]
                )
            relative = exact_decimal(
                metric["symmetric_relative_decimal"],
                label=f"reference 80/120 comparison {slot.key}:{stage}",
            )
            passed = relative <= REFERENCE_THRESHOLD
            all_passed = all_passed and passed
            comparison_ledger.append(
                {
                    "kind": "direct_80_vs_direct_120",
                    "slot": slot.key,
                    "precision_decimal_digits": [80, 120],
                    "stage": stage,
                    "threshold": "1e-40",
                    "metric": metric,
                    "passed": passed,
                }
            )
    if len(vector_ledger) != 144:
        # 72 unreduced direct vectors and 72 symbolic-CSE vectors.
        raise InvalidRun("reference vector topology drift")
    if len(comparison_ledger) != 108:
        raise InvalidRun("reference comparison topology drift")
    return internal, vector_ledger, comparison_ledger, all_passed


def evaluate_native_all(
    setup: StaticSetup,
    slots: Sequence[Any],
    bindings: Mapping[str, SourceBindings],
) -> tuple[
    dict[str, Mapping[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    internal: dict[str, Mapping[str, Any]] = {}
    call_audit: list[dict[str, Any]] = []
    stage_ledger: list[dict[str, Any]] = []
    for slot in slots:
        progress(f"six native evaluator variants: {slot.key}")
        variants = evaluate_native_slot(setup, slot, bindings[slot.source_label])
        internal[slot.key] = variants
        for variant in EVALUATOR_ORDER:
            record = variants[variant]
            call_audit.append(
                {
                    "slot": slot.key,
                    "source": slot.source_label,
                    "lambda": slot.lambda_value,
                    "evaluator": variant,
                    "m4_call": record["m4_call"],
                    "m5_call": record["m5_call"],
                    "common_downstream_arithmetic": record[
                        "common_downstream_arithmetic"
                    ],
                }
            )
            for stage, dimension in zip(STAGE_ORDER, STAGE_DIMENSIONS, strict=True):
                vector = record["stages"][stage]
                stage_ledger.append(
                    {
                        "slot": slot.key,
                        "source": slot.source_label,
                        "lambda": slot.lambda_value,
                        "evaluator": variant,
                        "stage": stage,
                        "dimension": dimension,
                        "active": stage_active(stage, slot.lambda_value),
                        "vector": vector,
                        "vector_digest": vector_digest(vector),
                    }
                )
    if len(call_audit) != 36 or len(stage_ledger) != 216:
        raise InvalidRun("native evaluator/stage topology drift")
    return internal, call_audit, stage_ledger


def native_reference_comparisons(
    setup: StaticSetup,
    slots: Sequence[Any],
    native: Mapping[str, Mapping[str, Any]],
    references: Mapping[str, Mapping[int, Mapping[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, str], dict[str, Any]]]:
    ledger: list[dict[str, Any]] = []
    index: dict[tuple[str, str, str], dict[str, Any]] = {}
    for slot in slots:
        reference = references[slot.key][120]["direct"]
        for evaluator in EVALUATOR_ORDER:
            stages = native[slot.key][evaluator]["stages"]
            for stage in STAGE_ORDER:
                with mp.workdps(160):
                    metric = setup.p52.native_to_mp_comparison_record(
                        stages[stage], reference[stage]
                    )
                relative = exact_decimal(
                    metric["symmetric_relative_decimal"],
                    label=f"native/direct comparison {slot.key}:{evaluator}:{stage}",
                )
                threshold = threshold_for_stage(stage)
                passed = relative <= threshold
                active = stage_active(stage, slot.lambda_value)
                record = {
                    "slot": slot.key,
                    "source": slot.source_label,
                    "lambda": slot.lambda_value,
                    "evaluator": evaluator,
                    "stage": stage,
                    "active": active,
                    "gate_applied": active,
                    "threshold_name": (
                        "completed_RHS_stage_relative_max"
                        if stage in (
                            "A_lambda_transpose_contraction",
                            "outer_minus_conjugation",
                        )
                        else "gradient_stage_relative_max"
                    ),
                    "threshold": "5e-10",
                    "metric": metric,
                    "passed": passed,
                    "status": (
                        "PASS"
                        if passed
                        else ("NONPASS" if active else "NONPASS_INACTIVE_DIAGNOSTIC")
                    ),
                }
                ledger.append(record)
                index[(slot.key, evaluator, stage)] = record
    if len(ledger) != 216 or len(index) != 216:
        raise InvalidRun("native-to-direct comparison topology drift")
    return ledger, index


def core_contrast_records(
    setup: StaticSetup,
    slots: Sequence[Any],
    native: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    ledger: list[dict[str, Any]] = []
    for slot in slots:
        for left, right, controlled_change in CONTROLLED_CONTRASTS:
            for stage in STAGE_ORDER:
                metric = setup.p52.comparison_record(
                    native[slot.key][left]["stages"][stage],
                    native[slot.key][right]["stages"][stage],
                )
                ledger.append(
                    {
                        "slot": slot.key,
                        "source": slot.source_label,
                        "lambda": slot.lambda_value,
                        "left": left,
                        "right": right,
                        "controlled_change": controlled_change,
                        "stage": stage,
                        "active": stage_active(stage, slot.lambda_value),
                        "metric": metric,
                        "threshold": None,
                        "role": "controlled arithmetic contrast; not a label gate",
                    }
                )
    if len(ledger) != 144:
        raise InvalidRun("core controlled-contrast topology drift")
    return ledger


def telescope_records(
    setup: StaticSetup,
    slots: Sequence[Any],
    native: Mapping[str, Mapping[str, Any]],
    references: Mapping[str, Mapping[int, Mapping[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], bool]:
    stage_ledger: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    all_passed = True
    for slot in slots:
        middle = native[slot.key]["EL_long"]["stages"]
        reference = references[slot.key][120]["direct"]
        for left in TELESCOPE_LEFT_ORDER:
            telescope = setup.p52.telescope_record(
                native[slot.key][left]["stages"], middle, reference
            )
            maximum = exact_decimal(
                telescope["maximum_relative_closure"],
                label=f"telescope summary {slot.key}:{left}",
            )
            summary_passed = maximum <= TELESCOPE_THRESHOLD
            all_passed = all_passed and summary_passed
            summaries.append(
                {
                    "slot": slot.key,
                    "left": left,
                    "middle": "EL_long",
                    "right": "direct_global_120",
                    "maximum_relative_closure": telescope[
                        "maximum_relative_closure"
                    ],
                    "outer_minus_conjugation_unexplained_relative": telescope[
                        "outer_minus_conjugation_unexplained_relative"
                    ],
                    "threshold": "5e-18",
                    "passed": summary_passed,
                }
            )
            for stage in STAGE_ORDER:
                stage_record = telescope["stages"][stage]
                closure = np.asarray(
                    stage_record["closure_vector"], dtype=np.clongdouble
                )
                relative = exact_decimal(
                    stage_record["relative_closure"],
                    label=f"telescope stage {slot.key}:{left}:{stage}",
                )
                passed = relative <= TELESCOPE_THRESHOLD
                all_passed = all_passed and passed
                stage_ledger.append(
                    {
                        "slot": slot.key,
                        "source": slot.source_label,
                        "lambda": slot.lambda_value,
                        "left": left,
                        "middle": "EL_long",
                        "right": "direct_global_120",
                        "stage": stage,
                        "active": stage_active(stage, slot.lambda_value),
                        **stage_record,
                        "closure_norm_absolute": float(np.linalg.norm(closure)),
                        "closure_max_component_absolute": float(
                            np.max(np.abs(closure), initial=np.longdouble(0))
                        ),
                        "threshold": "5e-18",
                        "passed": passed,
                    }
                )
    if len(stage_ledger) != 180 or len(summaries) != 30:
        raise InvalidRun("six-stage telescope topology drift")
    return stage_ledger, summaries, all_passed


def convention_numerical_proof(
    setup: StaticSetup,
    slots: Sequence[Any],
    native: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for slot in slots:
        factor_t = np.asarray(slot.node.factor.T, dtype=np.longdouble)
        for evaluator in EVALUATOR_ORDER:
            stages = native[slot.key][evaluator]["stages"]
            expected_contracted = np.asarray(
                factor_t
                @ np.asarray(
                    stages["lambda_blended_gradient"], dtype=np.clongdouble
                ),
                dtype=np.clongdouble,
            )
            expected_outer = np.asarray(
                -np.conjugate(expected_contracted), dtype=np.clongdouble
            )
            contraction_equal = np.array_equal(
                expected_contracted,
                np.asarray(
                    stages["A_lambda_transpose_contraction"],
                    dtype=np.clongdouble,
                ),
            )
            outer_equal = np.array_equal(
                expected_outer,
                np.asarray(stages["outer_minus_conjugation"], dtype=np.clongdouble),
            )
            if not contraction_equal or not outer_equal:
                raise InvalidRun(
                    f"ordinary-transpose/single-conjugation numerical drift at "
                    f"{slot.key}:{evaluator}"
                )
            records.append(
                {
                    "slot": slot.key,
                    "evaluator": evaluator,
                    "ordinary_transpose_recomputation_equal": contraction_equal,
                    "single_outer_minus_conjugation_recomputation_equal": outer_equal,
                }
            )
    if len(records) != 36:
        raise InvalidRun("convention proof topology drift")
    return {"record_count": len(records), "records": records, "all_passed": True}


def max_metric_decimal(
    records: Iterable[Mapping[str, Any]], pointer: Sequence[str]
) -> str:
    maximum: Decimal | None = None
    maximum_text: str | None = None
    for record in records:
        value: Any = record
        for key in pointer:
            value = value[key]
        value_text = str(value)
        number = exact_decimal(value_text, label="/".join(pointer))
        if maximum is None or number > maximum:
            maximum = number
            maximum_text = value_text
    if maximum_text is None:
        raise InvalidRun(f"cannot summarize an empty metric ledger at {'/'.join(pointer)}")
    return maximum_text


def selector_and_classification(
    comparison_index: Mapping[tuple[str, str, str], Mapping[str, Any]],
    slots: Sequence[Any],
    *,
    reference_passed: bool,
    telescopes_passed: bool,
    topology_passed: bool,
) -> tuple[list[dict[str, Any]], dict[str, bool], str, bool, dict[str, Any]]:
    selector_records: list[dict[str, Any]] = []
    selector_pass: dict[str, bool] = {}
    for evaluator in CORE_EVALUATORS:
        evaluator_passed = True
        for slot in slots:
            for stage in SELECTOR_STAGES:
                source = comparison_index[(slot.key, evaluator, stage)]
                record = {
                    "slot": slot.key,
                    "source": slot.source_label,
                    "lambda": slot.lambda_value,
                    "evaluator": evaluator,
                    "stage": stage,
                    "threshold": "5e-10",
                    "symmetric_relative_decimal": source["metric"][
                        "symmetric_relative_decimal"
                    ],
                    "passed": bool(source["passed"]),
                }
                evaluator_passed = evaluator_passed and record["passed"]
                selector_records.append(record)
        selector_pass[evaluator] = evaluator_passed
    if len(selector_records) != 48:
        raise InvalidRun("core selector topology drift")
    prerequisites = {
        "reference_80_120_and_symbolic_CSE_gates_passed": reference_passed,
        "all_five_chain_telescope_closures_passed": telescopes_passed,
        "exact_topology_and_global_nulls_passed": topology_passed,
        "all_core_selector_records_complete": len(selector_records) == 48,
        "EL_long_selector_passed_all_12_records": selector_pass["EL_long"],
    }
    valid = all(prerequisites.values())
    if not valid:
        return selector_records, selector_pass, "INVALID_RUN", False, prerequisites
    if selector_pass["GN_std"]:
        label = (
            "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_ACCURACY_NONPASS_NOT_"
            "CONFIRMED_ON_PHASE53_SIX_SLOTS"
        )
    elif selector_pass["GN_long"] and not selector_pass["EL_std"]:
        label = (
            "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_LONG_"
            "PRECISION_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS"
        )
    elif selector_pass["EL_std"] and not selector_pass["GN_long"]:
        label = (
            "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_ELEMENT_"
            "LOCAL_SCHEDULE_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS"
        )
    elif selector_pass["GN_long"] and selector_pass["EL_std"]:
        label = (
            "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_BOTH_"
            "LONG_PRECISION_AND_ELEMENT_LOCAL_SCHEDULE_INDEPENDENTLY_"
            "SUFFICIENT_ON_PHASE53_SIX_SLOTS"
        )
    else:
        label = (
            "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_"
            "PRECISION_X_SCHEDULE_INTERACTION_REQUIRED_ON_PHASE53_SIX_SLOTS"
        )
    allowed = {
        "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_LONG_PRECISION_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS",
        "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_ELEMENT_LOCAL_SCHEDULE_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS",
        "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_BOTH_LONG_PRECISION_AND_ELEMENT_LOCAL_SCHEDULE_INDEPENDENTLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS",
        "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_PRECISION_X_SCHEDULE_INTERACTION_REQUIRED_ON_PHASE53_SIX_SLOTS",
        "P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_ACCURACY_NONPASS_NOT_CONFIRMED_ON_PHASE53_SIX_SLOTS",
    }
    if label not in allowed:
        raise InvalidRun("classification dispatch produced an undeclared label")
    return selector_records, selector_pass, label, True, prerequisites


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


def expected_count_record(*, evaluated: bool) -> dict[str, Any]:
    expected = {
        "slot_count": 6,
        "core_matrix_evaluator_count": 4,
        "contextual_evaluator_count": 2,
        "native_evaluator_count": 6,
        "stage_count": 6,
        "native_stage_vector_count": 216,
        "direct_reference_stage_vector_count": 72,
        "symbolic_CSE_reference_stage_vector_count": 72,
        "native_to_direct_120_comparison_count": 216,
        "core_controlled_contrast_record_count": 144,
        "core_selector_record_count": 48,
        "telescope_record_count": 180,
        "saddle_solve_count": 0,
        "root_solve_count": 0,
        "ODE_integration_count": 0,
        "trajectory_fraction_count": 0,
        "continuation_or_classification_replay_count": 0,
    }
    return {
        "expected": expected,
        "evaluation_performed": evaluated,
        "predeclared_before_numerical_evaluation": True,
    }


def add_static_exact_checks(
    contract: Contract,
    bundle: InputBundle,
    slot_ledger: Sequence[Mapping[str, Any]],
    binding_ledger: Mapping[str, Any],
    reference_binding: Mapping[str, Any],
    convention_binding: Mapping[str, Any],
    topology: Mapping[str, Any],
) -> None:
    contract.add_exact(
        EXACT_CHECK_IDS[0],
        True,
        "all direct and transitive byte, commit, blob, runtime, and self-digest pins matched",
        {
            "direct_pin_count": 6,
            "validated_unique_pin_count": len(bundle.observed_pins),
            "manifest_commit": INPUT_COMMIT,
            "manifest_blob_oid": INPUT_BLOB_OID,
            "manifest_sha256": INPUT_SHA256,
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[1],
        len(slot_ledger) == 6,
        "the exact ordered Phase53 six launch-state objects and decimal pairs were consumed",
        {
            "slot_count": len(slot_ledger),
            "state_digests": [record["state_sha256"] for record in slot_ledger],
        },
    )
    core_binding_passed = bool(
        binding_ledger["projection_byte_identical_to_Phase52_and_Phase53"]
        and binding_ledger[
            "all_core_DAG_source_and_back_substitution_gates_passed"
        ]
        and binding_ledger["numeric_Python_id_values_serialized"] is False
        and len(CONTROLLED_CONTRASTS) == 4
    )
    contract.add_exact(
        EXACT_CHECK_IDS[2],
        core_binding_passed,
        "the core 2x2 cells preserve their declared joint/element DAG and arithmetic differences",
        {
            "core_evaluators": list(CORE_EVALUATORS),
            "controlled_contrasts": [list(item) for item in CONTROLLED_CONTRASTS],
            "Phase53_projection_sha256": binding_ledger[
                "Phase53_production_projection_sha256"
            ],
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[3],
        tuple(EVALUATOR_ORDER[-2:]) == CONTEXT_EVALUATORS
        and binding_ledger[
            "all_contextual_DAG_and_back_substitution_gates_passed"
        ]
        and tuple(STAGE_ORDER) == tuple(topology["declared_stage_order"]),
        "both contextual evaluators and the six-stage order are exactly bound",
        {
            "contextual_evaluators": list(CONTEXT_EVALUATORS),
            "stage_order": list(STAGE_ORDER),
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[4],
        bool(
            reference_binding["unreduced_direct_path_has_no_lambdify"]
            and reference_binding["symbolic_CSE_path_has_no_lambdify"]
            and reference_binding[
                "state_lift_constructs_mpmath_directly_from_decimal_pair_strings"
            ]
            and reference_binding["state_lift_does_not_read_slot_state_w5"]
            and reference_binding[
                "all_reference_CSE_back_substitution_gates_passed"
            ]
            and not reference_binding["native_output_consumed_by_reference"]
        ),
        "the direct global evalf and symbolic-CSE references are independent of native outputs",
        reference_binding,
    )
    contract.add_exact(
        EXACT_CHECK_IDS[5],
        all(
            bool(convention_binding[key])
            for key in (
                "native_ordinary_factor_transpose_bound",
                "native_single_outer_minus_conjugation_bound",
                "reference_ordinary_factor_transpose_bound",
                "reference_single_outer_minus_conjugation_bound",
                "Hermitian_transpose_spelling_absent",
            )
        ),
        "ordinary transpose and exactly one outer minus-conjugation are bound",
        convention_binding,
    )
    topology_passed = all(
        int(topology[key]) == 0
        for key in (
            "saddle_solve_count",
            "root_solve_count",
            "ODE_integration_count",
            "trajectory_fraction_count",
            "continuation_or_classification_replay_count",
        )
    )
    contract.add_exact(
        EXACT_CHECK_IDS[6],
        topology_passed,
        "the run is static and every continuation/global/physics/TOE output remains null",
        {"execution_topology": topology, "required_global_nulls": required_global_nulls()},
    )


def add_numerical_checks(
    contract: Contract,
    reference_records: Sequence[Mapping[str, Any]],
    native_records: Sequence[Mapping[str, Any]],
    telescope_records_all: Sequence[Mapping[str, Any]],
    *,
    reference_passed: bool,
    telescopes_passed: bool,
) -> None:
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[0],
        reference_passed,
        "direct 80/120 and symbolic-CSE/unreduced references stay below 1e-40",
        {
            "record_count": len(reference_records),
            "maximum_symmetric_relative_decimal": max_metric_decimal(
                reference_records, ("metric", "symmetric_relative_decimal")
            ),
            "threshold": "1e-40",
        },
    )
    evaluator_check_ids = dict(
        zip(EVALUATOR_ORDER, NUMERICAL_CHECK_IDS[1:7], strict=True)
    )
    for evaluator in EVALUATOR_ORDER:
        active = [
            record
            for record in native_records
            if record["evaluator"] == evaluator and record["active"]
        ]
        passed = all(bool(record["passed"]) for record in active)
        contract.add_numerical(
            evaluator_check_ids[evaluator],
            passed,
            f"{evaluator} active stages compared with direct-global 120 digits",
            {
                "active_record_count": len(active),
                "all_stage_record_count": sum(
                    record["evaluator"] == evaluator for record in native_records
                ),
                "maximum_active_symmetric_relative_decimal": max_metric_decimal(
                    active, ("metric", "symmetric_relative_decimal")
                ),
                "threshold": "5e-10",
                "nonpass_is_diagnostic_unless_a_scientific_prerequisite_says_otherwise": True,
            },
        )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[7],
        telescopes_passed,
        "all controlled contrasts were retained and all five-chain telescopes closed below 5e-18",
        {
            "controlled_contrast_record_count": 144,
            "telescope_record_count": len(telescope_records_all),
            "maximum_telescope_relative_closure": max(
                (float(record["relative_closure"]) for record in telescope_records_all),
                default=0.0,
            ),
            "threshold": "5e-18",
        },
    )


def topology_record(setup: StaticSetup) -> dict[str, Any]:
    return {
        "declared_stage_order": list(STAGE_ORDER),
        "slot_count": 6,
        "core_matrix_evaluator_count": 4,
        "contextual_evaluator_count": 2,
        "native_evaluator_count": 6,
        "stage_count": 6,
        **setup.topology.record(),
        "source_context_node_called": False,
        "Phase51_saddle_method_called": False,
        "Phase51_integrate_k_called": False,
        "static_factor_reconstruction_only": True,
    }


def common_preamble(
    *, authoritative: bool
) -> tuple[
    InputBundle,
    StaticSetup,
    list[Any],
    list[dict[str, Any]],
    dict[str, SourceBindings],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    Contract,
]:
    progress("validating frozen byte/runtime/Git provenance")
    bundle = validate_inputs(authoritative=authoritative)
    setup = build_static_setup(bundle)
    slots, slot_ledger = build_static_slots(bundle, setup)
    bindings, binding_ledger = build_evaluator_bindings(bundle, setup)
    reference_binding = reference_independence_record(setup)
    convention_binding = convention_binding_record(setup)
    topology = topology_record(setup)
    contract = Contract()
    add_static_exact_checks(
        contract,
        bundle,
        slot_ledger,
        binding_ledger,
        reference_binding,
        convention_binding,
        topology,
    )
    if tuple(record["id"] for record in contract.exact) != EXACT_CHECK_IDS:
        raise InvalidRun("exact check emission order drift")
    return (
        bundle,
        setup,
        slots,
        slot_ledger,
        bindings,
        binding_ledger,
        reference_binding,
        convention_binding,
        contract,
    )


def base_result(
    bundle: InputBundle,
    setup: StaticSetup,
    slot_ledger: Sequence[Mapping[str, Any]],
    binding_ledger: Mapping[str, Any],
    reference_binding: Mapping[str, Any],
    convention_binding: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "phase": 54,
        "scope": {
            "calculation_workbench_only": True,
            "states": "exact six Phase53 launch states",
            "calculation": "six-stage static evaluator arithmetic audit",
            "roots_or_saddles": False,
            "ODE_or_trajectory": False,
            "continuation_or_classification_replay": False,
            "physics_or_TOE": False,
        },
        "input_provenance": {
            "manifest": {
                "path": str(INPUT_PATH.relative_to(REPO_ROOT)),
                "commit": INPUT_COMMIT,
                "introduction_commit": INPUT_INTRODUCTION_COMMIT,
                "git_blob_oid": INPUT_BLOB_OID,
                "sha256": INPUT_SHA256,
                "size_bytes": INPUT_SIZE_BYTES,
            },
            "pinned_artifacts": bundle.observed_pins,
            "runner_guard": bundle.runner_guard,
            "Phase51_context_input_audit": setup.phase51_context_audit,
            "volatile_identity_policy": {
                "Phase53_numeric_id_values_used_as_evidence": False,
                "Phase54_numeric_Python_id_values_serialized": False,
                "stable_evidence": [
                    "callable role labels",
                    "generated source SHA256",
                    "symbolic DAG SHA256",
                    "explicit alias/equivalence booleans",
                ],
            },
        },
        "runtime": bundle.observed_runtime,
        "slots": {
            "source_order": list(SOURCE_ORDER),
            "lambda_order": list(LAMBDA_ORDER),
            "count": len(slot_ledger),
            "records": list(slot_ledger),
        },
        "evaluator_bindings": binding_ledger,
        "reference_independence": reference_binding,
        "convention_binding": convention_binding,
        "execution_topology": topology_record(setup),
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
    }


def validation_only_result() -> dict[str, Any]:
    (
        bundle,
        setup,
        _slots,
        slot_ledger,
        _bindings,
        binding_ledger,
        reference_binding,
        convention_binding,
        contract,
    ) = common_preamble(authoritative=False)
    progress("validate-only: numerical slot/reference evaluation intentionally skipped")
    result = base_result(
        bundle,
        setup,
        slot_ledger,
        binding_ledger,
        reference_binding,
        convention_binding,
    )
    result.update(
        {
            "run_status": "VALIDATION_ONLY",
            "classification": None,
            "exact_checks": contract.exact,
            "numerical_checks": [
                {
                    "id": check_id,
                    "kind": "numerical",
                    "passed": None,
                    "status": "NOT_EVALUATED_VALIDATE_ONLY",
                    "statement": "predeclared; authoritative numerical evaluation skipped",
                }
                for check_id in NUMERICAL_CHECK_IDS
            ],
            "counts": {
                **expected_count_record(evaluated=False),
                "actual_validate_only": {
                    "slot_count": len(slot_ledger),
                    "bound_native_evaluator_count": len(EVALUATOR_ORDER),
                    "bound_stage_count": len(STAGE_ORDER),
                    "native_stage_vector_count": 0,
                    "direct_reference_stage_vector_count": 0,
                    "symbolic_CSE_reference_stage_vector_count": 0,
                    "native_to_direct_120_comparison_count": 0,
                    "core_controlled_contrast_record_count": 0,
                    "core_selector_record_count": 0,
                    "telescope_record_count": 0,
                },
            },
            "scientific_classification_prerequisites": {
                "evaluated": False,
                "scientific_label_allowed_in_validate_only": False,
            },
            "post_evaluation_rehash": post_rehash(bundle),
            "computed_facts": [
                "all frozen pins, slots, symbolic plans, evaluator bindings, and static topology validated",
                "no native or reference numerical slot was evaluated in validate-only mode",
            ],
            "interpretation": (
                "Validation-only is not a scientific Phase54 outcome and does not confirm "
                "or fail to confirm the Phase51 historical-control accuracy nonpass."
            ),
        }
    )
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def authoritative_result() -> dict[str, Any]:
    (
        bundle,
        setup,
        slots,
        slot_ledger,
        bindings,
        binding_ledger,
        reference_binding,
        convention_binding,
        contract,
    ) = common_preamble(authoritative=True)

    # Evaluate the independent references before any native candidate at each
    # phase of the run.  The reference implementation consumes only symbolic
    # expressions and the pinned state/factor data.
    state_decimal_pairs_by_slot = {
        str(record["slot"]): record["input_state_w5_decimal_pairs"]
        for record in slot_ledger
    }
    references, reference_vectors, reference_comparisons, reference_passed = (
        evaluate_references(setup, slots, state_decimal_pairs_by_slot)
    )
    native, raw_call_audit, native_stage_ledger = evaluate_native_all(
        setup, slots, bindings
    )
    convention_proof = convention_numerical_proof(setup, slots, native)
    native_comparisons, comparison_index = native_reference_comparisons(
        setup, slots, native, references
    )
    contrasts = core_contrast_records(setup, slots, native)
    telescopes, telescope_summaries, telescopes_passed = telescope_records(
        setup, slots, native, references
    )

    actual_counts = {
        "slot_count": len(slots),
        "core_matrix_evaluator_count": len(CORE_EVALUATORS),
        "contextual_evaluator_count": len(CONTEXT_EVALUATORS),
        "native_evaluator_count": len(EVALUATOR_ORDER),
        "stage_count": len(STAGE_ORDER),
        "native_stage_vector_count": len(native_stage_ledger),
        "direct_reference_stage_vector_count": sum(
            record["reference_variant"] == "direct" for record in reference_vectors
        ),
        "symbolic_CSE_reference_stage_vector_count": sum(
            record["reference_variant"] == "CSE" for record in reference_vectors
        ),
        "native_to_direct_120_comparison_count": len(native_comparisons),
        "core_controlled_contrast_record_count": len(contrasts),
        "core_selector_record_count": 48,
        "telescope_record_count": len(telescopes),
        **setup.topology.record(),
    }
    expected = expected_count_record(evaluated=True)["expected"]
    topology_passed = actual_counts == expected
    selector_records, selector_pass, classification, scientifically_valid, prerequisites = (
        selector_and_classification(
            comparison_index,
            slots,
            reference_passed=reference_passed,
            telescopes_passed=telescopes_passed,
            topology_passed=topology_passed,
        )
    )
    if len(selector_records) != actual_counts["core_selector_record_count"]:
        raise InvalidRun("selector actual-count drift")
    add_numerical_checks(
        contract,
        reference_comparisons,
        native_comparisons,
        telescopes,
        reference_passed=reference_passed,
        telescopes_passed=telescopes_passed,
    )
    if tuple(record["id"] for record in contract.numerical) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("numerical check emission order drift")

    reference_slot_ledger = [
        {
            "slot": slot.key,
            "tiers": [
                {
                    "precision_decimal_digits": digits,
                    "input_lift": references[slot.key][digits]["input_lift"],
                }
                for digits in (80, 120)
            ],
        }
        for slot in slots
    ]
    result = base_result(
        bundle,
        setup,
        slot_ledger,
        binding_ledger,
        reference_binding,
        convention_binding,
    )
    result.update(
        {
            "run_status": "VALID_RUN" if scientifically_valid else "INVALID_RUN",
            "classification": classification,
            "exact_checks": contract.exact,
            "numerical_checks": contract.numerical,
            "counts": {
                **expected_count_record(evaluated=True),
                "actual": actual_counts,
                "exact_match": topology_passed,
            },
            "evaluation_order": [
                "all_direct_and_symbolic_CSE_references_80_120",
                "all_six_native_evaluators",
                "native_to_direct_comparisons",
                "controlled_contrasts",
                "five_chain_telescopes",
                "active_blended_gradient_and_outer_RHS_classification",
            ],
            "reference_validation": {
                "precision_tiers_decimal_digits": [80, 120],
                "authoritative_tier_decimal_digits": 120,
                "reference_slot_input_lifts": reference_slot_ledger,
                "stage_vectors": reference_vectors,
                "comparison_records": reference_comparisons,
                "all_stability_gates_passed": reference_passed,
                "direct_reference_stage_vector_count": actual_counts[
                    "direct_reference_stage_vector_count"
                ],
                "symbolic_CSE_reference_stage_vector_count": actual_counts[
                    "symbolic_CSE_reference_stage_vector_count"
                ],
            },
            "raw_dtype_and_callable_boundary_audit": {
                "records": raw_call_audit,
                "record_count": len(raw_call_audit),
                "common_post_callable_boundary": (
                    "one complete-gradient np.clongdouble boundary followed by shared "
                    "Phase52.native_stages arithmetic"
                ),
                "numeric_Python_id_values_serialized": False,
            },
            "native_stage_values": native_stage_ledger,
            "native_to_direct_120_comparisons": native_comparisons,
            "core_controlled_contrasts": contrasts,
            "stage_telescopes": {
                "records": telescopes,
                "chain_summaries": telescope_summaries,
                "all_closures_passed": telescopes_passed,
            },
            "convention_numerical_proof": convention_proof,
            "classification_selector_records": selector_records,
            "classification_selector_pass_by_core_evaluator": selector_pass,
            "scientific_classification_prerequisites": prerequisites,
            "historical_boundary": {
                "Phase51_result_mutated_or_reclassified": False,
                "Phase53_result_mutated_or_reclassified": False,
                "contextual_controls_select_classification": False,
                "classification_scope": (
                    "confirm/not-confirm historical Phase51 global non-CSE active "
                    "gradient/completed-RHS accuracy nonpass on six static states"
                ),
            },
            "computed_facts": [
                "six fixed source-by-lambda states were evaluated at six declared static stages",
                "four core arithmetic cells and two contextual controls were compared to direct-global 120 digits",
                "classification used only the completed active blend and outer-RHS selectors",
            ],
            "interpretation": (
                "The label localizes finite evaluator arithmetic on six saved states only. "
                "It is not a root, trajectory, continuation, global-cycle, physics, or TOE result."
            ),
            "post_evaluation_rehash": post_rehash(bundle),
        }
    )
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def invalid_result(error: BaseException, *, validate_only: bool) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 54,
        "run_status": "INVALID_RUN",
        "classification": "INVALID_RUN",
        "mode": "validate-only" if validate_only else "authoritative",
        "error": {
            "type": type(error).__name__,
            "message": str(error),
        },
        "exact_checks": [],
        "numerical_checks": [],
        "execution_topology": None,
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
        "interpretation": (
            "No scientific Phase54 label is permitted because a validity prerequisite failed."
        ),
    }
    reject_numeric_identity_fields(result)
    return with_self_digest(result)


def emit_result(payload: Mapping[str, Any]) -> None:
    ready = json_ready(payload)
    print(
        RESULT_PREFIX
        + json.dumps(
            ready,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ),
        flush=True,
    )


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate pins, slots, bindings, and topology without numerical evaluation",
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
        emit_result(result)
        return 0 if result.get("run_status") != "INVALID_RUN" else 1
    except Exception as error:  # retain one machine-readable terminal record
        traceback.print_exc(file=sys.stderr)
        emit_result(invalid_result(error, validate_only=arguments.validate_only))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
