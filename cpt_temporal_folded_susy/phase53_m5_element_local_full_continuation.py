#!/usr/bin/env python3
"""Phase 53: rerun the complete Phase-51 continuation with the Phase-52 repair.

The Phase-51 continuation engine is imported rather than copied.  Its sole
scientific substitution is ``build_long_evaluator``: action, gradient, and
Hessian are generated as three separate source-substituted, per-element,
long-namespace CSE families and accumulated in the frozen left-to-right order.
The gradient family is required to be byte/fingerprint-identical to the
Phase-52 element-gradient projection.  The production tangent flow therefore
uses the repaired element-local Hessian too; a gradient-only/non-CSE-Hessian
hybrid is forbidden.

The program writes no repository files.  Progress goes to stderr and exactly
one ``RESULT_JSON=...`` record goes to stdout.

An inherited numerical non-pass that Phase 51 captures in a completed
semantic record remains ``INCONCLUSIVE``.  A failure during Phase 51's initial
six-node saddle/evaluator construction prevents the inherited engine from
producing a valid complete replay and is therefore ``INVALID_RUN``; Phase 53
does not substitute a pinned or terminal saddle to force continuation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import math
import os
import platform
import subprocess
import sys
import traceback
from contextlib import ExitStack, contextmanager, nullcontext
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath as mp
import numpy as np
import scipy
import sympy as sp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_INPUTS.json"
)
P51_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase51_m5_gamma_k_local_continuation.py"
)
P52_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase52_m5_cse_runtime_dtype_and_rhs_repair.py"
)

INPUT_COMMIT = "c2f29917c974f19f4178e85e3b48dd057c316e69"
INPUT_SHA256 = "551acf717e8f7d53353ce962fef2301d11fd2c16db64d8500e768842ddbef71a"

RESULT_SCHEMA = "ice-phase53-m5-element-local-full-continuation/v1"
RESULT_PREFIX = "RESULT_JSON="
M4 = 7
M5 = 9
SOURCE_ORDER = ("phi_plus", "phi_minus")
LAMBDA_ORDER = (0.0, 0.5, 1.0)
EXPECTED_P52_FULL_LEDGER_SHA256 = (
    "ef5c95e3e864b1cfc52828e75f61c31b6b661a5ba725cba57c22e1f0d34eb060"
)
EXPECTED_P52_ELEMENT_PROJECTION_SHA256 = (
    "8359762ba056bd7a300bceba8d4bf7e83e22149f5795c37f5b6ee0a4a212ad4e"
)
EXPECTED_P52_ELEMENT_PROJECTION_BYTES = 4141

EXACT_CHECK_IDS = (
    "P53.inputs.byte_pins_self_digests_and_committed_blobs",
    "P53.contract.Phase51_semantics_inherited_except_evaluator",
    "P53.symbolic.action_gradient_hessian_element_identities",
    "P53.symbolic.Phase52_gradient_DAG_exact_reuse",
    "P53.symbolic.action_hessian_CSE_back_substitution",
    "P53.dtype.full_evaluator_raw_clongdouble",
    "P53.conventions.fixed_order_complete_evaluator_and_solver_boundary",
    "P53.guard.local_global_physics_TOE_nulls",
)

# The manifest freezes these exact strings.  They are kept together so a
# finalized manifest/key mismatch fails before any expensive continuation.
NUMERICAL_CHECK_IDS = (
    "P53.reference.six_slot_80_120_full_evaluator",
    "P53.saddles.Phase50_reproduction",
    "P53.intersections.lambda0_lifts",
    "P53.intersections.fine_forward_both_sources",
    "P53.intersections.coarse_and_reverse",
    "P53.reflection.independent_phi_pair",
    "P53.derivative.full_J_at_0_half_1",
    "P53.tangent.lambda_half",
    "P53.evaluator.full_repaired_pairs_and_trajectories",
    "P53.endpoint.radius_and_shape",
    "P53.guard.full_semantic_replay_topology_and_nulls",
)

P51_NUMERICAL_IDS = (
    "P51.saddles.Phase50_reproduction",
    "P51.intersections.lambda0_lifts",
    "P51.intersections.fine_forward_both_sources",
    "P51.intersections.coarse_and_reverse",
    "P51.reflection.independent_phi_pair",
    "P51.derivative.full_J_at_0_half_1",
    "P51.tangent.lambda_half",
    "P51.evaluator.CSE_nonCSE_pairs",
    "P51.endpoint.radius_and_shape",
    "P51.guard.classification_and_nulls",
)


class InvalidRun(RuntimeError):
    """A frozen byte, symbolic, dtype, convention, or serialization guard failed."""


def progress(message: str) -> None:
    print(f"[Phase53] {message}", file=sys.stderr, flush=True)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    payload = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(
            InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
        ),
    )
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")

    def require_finite_tree(value: Any, location: str) -> None:
        if isinstance(value, float) and not math.isfinite(value):
            raise InvalidRun(f"nonfinite parsed JSON number at {location}")
        if isinstance(value, Mapping):
            for key, item in value.items():
                require_finite_tree(item, f"{location}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                require_finite_tree(item, f"{location}[{index}]")

    require_finite_tree(payload, path.name)
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
    return np.format_float_scientific(
        number, precision=24, unique=False, trim="k"
    )


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        array = np.asarray(value)
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
            pairs = []
            for item in array.reshape(-1):
                real = float(item.real)
                imaginary = float(item.imag)
                if not math.isfinite(real) or not math.isfinite(imaginary):
                    raise InvalidRun("nonfinite NumPy complex array")
                pairs.append([real, imaginary])
            return {
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "numpy_complex_pairs": pairs,
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
            raise InvalidRun("nonfinite NumPy complex")
        return {
            "dtype": str(value.dtype),
            "real": float(value.real),
            "imag": float(value.imag),
        }
    if isinstance(value, complex):
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise InvalidRun("nonfinite Python complex")
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, mp.mpc):
        if not mp.isfinite(value.real) or not mp.isfinite(value.imag):
            raise InvalidRun("nonfinite mpmath complex")
        return {
            "mp_decimal_pair": [mp.nstr(value.real, 45), mp.nstr(value.imag, 45)]
        }
    if isinstance(value, mp.mpf):
        if not mp.isfinite(value):
            raise InvalidRun("nonfinite mpmath real")
        return {"mp_decimal": mp.nstr(value, 45)}
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
    output["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(output)
    ).hexdigest()
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
    observed = hashlib.sha256(canonical_bytes(stripped)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


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
            f"declared commit does not contain pinned working bytes: {relative}"
        )
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
        "mpmath_version": mp.__version__,
        "longdouble_itemsize_bytes": int(np.dtype(np.longdouble).itemsize),
        "clongdouble_itemsize_bytes": int(np.dtype(np.clongdouble).itemsize),
        "longdouble_mantissa_bits_excluding_implicit": int(
            np.finfo(np.longdouble).nmant
        ),
        "longdouble_epsilon": str(np.finfo(np.longdouble).eps),
        "platform": platform.platform(),
        "thread_environment": {
            name: os.environ.get(name) for name in thread_names
        },
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
            "status": "PASS" if passed else "INCONCLUSIVE",
            "statement": statement,
        }
        if details is not None:
            record["details"] = dict(details)
        self.numerical.append(record)


@dataclass
class InputBundle:
    manifest: dict[str, Any]
    manifest_raw: bytes
    observed: dict[str, Any]
    loaded_json: dict[str, dict[str, Any]]
    p51_manifest: dict[str, Any]
    p52_manifest: dict[str, Any]
    p51_result: dict[str, Any]
    p52_result: dict[str, Any]
    p51_runner_path: Path
    p52_runner_path: Path
    runner_guard: dict[str, Any]


def _loaded_by_basename(
    loaded: Mapping[str, dict[str, Any]],
    observed: Mapping[str, Mapping[str, Any]],
    basename: str,
) -> dict[str, Any]:
    matches = [
        loaded[label]
        for label, record in observed.items()
        if label in loaded and Path(str(record["path"])).name == basename
    ]
    if len(matches) != 1:
        raise InvalidRun(f"expected exactly one pinned JSON named {basename}")
    return matches[0]


def _pinned_path_by_basename(
    observed: Mapping[str, Mapping[str, Any]], basename: str
) -> Path:
    matches = [
        REPO_ROOT / str(record["path"])
        for label, record in observed.items()
        if not label.startswith("phase51_transitive::")
        and Path(str(record["path"])).name == basename
    ]
    if len(matches) != 1:
        raise InvalidRun(f"expected exactly one pinned path named {basename}")
    return matches[0]


def validate_inputs(*, authoritative: bool) -> InputBundle:
    if INPUT_COMMIT == "MANIFEST_PENDING" or INPUT_SHA256 == "MANIFEST_PENDING":
        raise InvalidRun("Phase53 manifest commit/SHA placeholders remain")
    manifest, manifest_raw = load_unique_json(INPUT_PATH)
    if hashlib.sha256(manifest_raw).hexdigest() != INPUT_SHA256:
        raise InvalidRun("Phase53 manifest SHA drift")
    if (
        manifest.get("schema")
        != "ice-phase53-m5-element-local-full-continuation-inputs/v1"
        or manifest.get("phase") != 53
    ):
        raise InvalidRun("Phase53 manifest schema/phase drift")
    checks = require(manifest, "checks", where="manifest")
    if tuple(require(checks, "exact", where="checks")) != EXACT_CHECK_IDS:
        raise InvalidRun("Phase53 exact check IDs drift")
    if tuple(require(checks, "numerical", where="checks")) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("Phase53 numerical check IDs drift")

    observed_runtime = runtime_record()
    expected_runtime = require(manifest, "runtime_contract", where="manifest")
    aliases = {"python": "python_version", "numpy": "numpy_version", "scipy": "scipy_version", "sympy": "sympy_version", "mpmath": "mpmath_version"}
    for expected_key, expected_value in expected_runtime.items():
        if expected_key in ("blas_and_thread_environment", "policy"):
            continue
        actual_key = aliases.get(str(expected_key), str(expected_key))
        if actual_key == "platform" or actual_key not in observed_runtime:
            continue
        if str(observed_runtime[actual_key]) != str(expected_value):
            raise InvalidRun(
                f"runtime contract drift for {expected_key}: "
                f"{observed_runtime[actual_key]} != {expected_value}"
            )
    required_threads = require(
        require(
            expected_runtime,
            "blas_and_thread_environment",
            where="runtime_contract",
        ),
        "required_environment",
        where="runtime_contract.blas_and_thread_environment",
    )
    thread_drift = {
        str(name): {
            "expected": str(expected),
            "observed": os.environ.get(str(name)),
        }
        for name, expected in required_threads.items()
        if os.environ.get(str(name)) != str(expected)
    }
    if thread_drift:
        raise InvalidRun(f"frozen thread environment drift: {thread_drift}")

    observed: dict[str, Any] = {}
    loaded: dict[str, dict[str, Any]] = {}
    pinned = require(manifest, "pinned_inputs", where="manifest")
    for label, raw_specification in pinned.items():
        if not isinstance(raw_specification, Mapping):
            raise InvalidRun(f"invalid pinned input: {label}")
        specification = raw_specification
        where = f"pinned_inputs.{label}"
        relative = str(require(specification, "path", where=where))
        commit = str(require(specification, "commit", where=where))
        path = REPO_ROOT / relative
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != str(require(specification, "sha256", where=where)):
            raise InvalidRun(f"pinned input SHA drift: {label}")
        if "size_bytes" in specification and len(raw) != int(specification["size_bytes"]):
            raise InvalidRun(f"pinned input size drift: {label}")
        if path.suffix == ".json":
            payload = parse_unique_json_bytes(path, raw)
            loaded[label] = payload
            expected_self = specification.get(
                "result_payload_sha256_without_self",
                specification.get("self_digest"),
            )
            if expected_self is not None:
                observed_self = verify_self_digest(payload, label=label)
                if observed_self != str(expected_self):
                    raise InvalidRun(f"pinned result self digest drift: {label}")
            if "required_run_status" in specification and payload.get(
                "run_status"
            ) != specification["required_run_status"]:
                raise InvalidRun(f"pinned required run status drift: {label}")
            if "required_classification" in specification and payload.get(
                "classification"
            ) != specification["required_classification"]:
                raise InvalidRun(f"pinned required classification drift: {label}")
        blob_guard = committed_blob_guard(relative, commit)
        if "git_blob_oid" in specification and (
            blob_guard["working_blob_oid"] != specification["git_blob_oid"]
            or blob_guard["committed_blob_oid"] != specification["git_blob_oid"]
        ):
            raise InvalidRun(f"declared Git blob OID drift: {label}")
        observed[label] = {
            "path": relative,
            "commit": commit,
            "sha256": digest,
            "size_bytes": len(raw),
            "role": specification.get("role"),
            **blob_guard,
        }

    p51_manifest = _loaded_by_basename(
        loaded, observed, "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json"
    )
    p52_manifest = _loaded_by_basename(
        loaded, observed, "PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_INPUTS.json"
    )
    p51_result = _loaded_by_basename(
        loaded, observed, "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_RESULT.json"
    )
    p52_result = _loaded_by_basename(
        loaded, observed, "PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_RESULT.json"
    )
    p51_runner_path = _pinned_path_by_basename(
        observed, "phase51_m5_gamma_k_local_continuation.py"
    )
    p52_runner_path = _pinned_path_by_basename(
        observed, "phase52_m5_cse_runtime_dtype_and_rhs_repair.py"
    )
    if p51_result.get("run_status") != "VALID_RUN":
        raise InvalidRun("pinned Phase51 historical result status drift")
    if p52_result.get("run_status") != "VALID_RUN" or not p52_result.get(
        "Phase53_full_rerun_required_before_any_local_supported_label"
    ):
        raise InvalidRun("pinned Phase52 readiness boundary drift")
    if (
        p52_result.get("generated_callable_ledger_sha256")
        != EXPECTED_P52_FULL_LEDGER_SHA256
    ):
        raise InvalidRun("pinned Phase52 generated ledger drift")

    # The flattened Phase53 pins must agree with the same transitive bytes
    # named by the inherited manifests.  This catches a locally consistent
    # but cross-manifest-inconsistent rewrite.
    flattened_by_path = {
        str(record["path"]): specification
        for specification, record in (
            (pinned[label], observed[label]) for label in pinned
        )
    }
    for inherited_label, inherited_manifest in (
        ("Phase51", p51_manifest),
        ("Phase52", p52_manifest),
    ):
        for nested_label, nested in require(
            inherited_manifest, "pinned_inputs", where=f"{inherited_label} manifest"
        ).items():
            relative = str(require(nested, "path", where=f"{inherited_label}.{nested_label}"))
            if relative not in flattened_by_path:
                continue
            flat = flattened_by_path[relative]
            for field_name in ("commit", "sha256"):
                if str(flat.get(field_name)) != str(nested.get(field_name)):
                    raise InvalidRun(
                        f"flattened/{inherited_label} nested {field_name} drift: {relative}"
                    )

    # Recheck every transitive Phase51 byte/commit, including locks and the
    # Phase41/42/49/50 sources loaded by the imported engine.
    for nested_label, raw_specification in require(
        p51_manifest, "pinned_inputs", where="Phase51 manifest"
    ).items():
        if not isinstance(raw_specification, Mapping):
            raise InvalidRun(f"invalid Phase51 transitive pin: {nested_label}")
        where = f"Phase51 pinned_inputs.{nested_label}"
        relative = str(require(raw_specification, "path", where=where))
        commit = str(require(raw_specification, "commit", where=where))
        raw = (REPO_ROOT / relative).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != str(require(raw_specification, "sha256", where=where)):
            raise InvalidRun(f"Phase51 transitive SHA drift: {nested_label}")
        observed[f"phase51_transitive::{nested_label}"] = {
            "path": relative,
            "commit": commit,
            "sha256": digest,
            "size_bytes": len(raw),
            "role": "Phase51 transitive pin",
            **committed_blob_guard(relative, commit),
        }

    runner_guard: dict[str, Any] = {
        "authoritative": authoritative,
        "runner_sha256_at_start": sha256_path(SCRIPT_PATH),
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
            raise InvalidRun("authoritative Phase53 runner must be committed and clean")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", INPUT_COMMIT, commit],
            cwd=REPO_ROOT,
            check=False,
        ).returncode == 0
        if not ancestor or commit == INPUT_COMMIT:
            raise InvalidRun("Phase53 runner commit must postdate its manifest")
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
    return InputBundle(
        manifest=manifest,
        manifest_raw=manifest_raw,
        observed=observed,
        loaded_json=loaded,
        p51_manifest=p51_manifest,
        p52_manifest=p52_manifest,
        p51_result=p51_result,
        p52_result=p52_result,
        p51_runner_path=p51_runner_path,
        p52_runner_path=p52_runner_path,
        runner_guard=runner_guard,
    )


def fixed_scalar_sum(values: Sequence[Any]) -> np.clongdouble:
    total = np.clongdouble(0)
    for value in values:
        total = np.clongdouble(total + np.clongdouble(value))
    return total


def fixed_array_sum(values: Sequence[Any], shape: tuple[int, ...]) -> np.ndarray:
    total = np.zeros(shape, dtype=np.clongdouble)
    for value in values:
        array = np.asarray(value, dtype=np.clongdouble).reshape(shape)
        for index in np.ndindex(shape):
            total[index] = np.clongdouble(total[index] + array[index])
    return total


def call_generated(
    p52: ModuleType,
    callable_set: Any,
    values: Sequence[Any],
    expected_count: int,
) -> np.ndarray:
    raw = p52.flatten_raw(callable_set.function(tuple(values)))
    if len(raw) != expected_count:
        raise InvalidRun(
            f"generated output-count drift: {len(raw)} != {expected_count}"
        )
    array = np.asarray(raw, dtype=np.clongdouble)
    if not np.all(np.isfinite(array)):
        raise InvalidRun("generated evaluator produced a nonfinite value")
    return array


@dataclass
class ElementDimensionPlan:
    dimension: int
    variables: tuple[sp.Symbol, ...]
    float_elements: tuple[sp.Expr, ...]
    exact_elements: tuple[sp.Expr, ...]
    global_action_expr: sp.Expr
    global_gradient_expr: tuple[sp.Expr, ...]
    global_hessian_expr: tuple[sp.Expr, ...]
    global_expression_provenance: str
    global_expression_sha256: str
    action_long: tuple[Any, ...]
    gradient_long: tuple[Any, ...]
    hessian_long: tuple[Any, ...]
    action_plain: tuple[Any, ...]
    gradient_plain: tuple[Any, ...]
    hessian_plain: tuple[Any, ...]
    exact_identity: Mapping[str, bool]
    ledger: tuple[Mapping[str, Any], ...]
    calls: dict[str, int] = field(
        default_factory=lambda: {
            "production_action": 0,
            "production_gradient": 0,
            "production_hessian": 0,
            "plain_action": 0,
            "plain_gradient": 0,
            "plain_hessian": 0,
        }
    )

    def action_only(
        self, p52: ModuleType, values: Sequence[Any], *, plain: bool = False
    ) -> np.clongdouble:
        action_sets = self.action_plain if plain else self.action_long
        prefix = "plain" if plain else "production"
        actions = [
            call_generated(p52, item, values, 1)[0] for item in action_sets
        ]
        self.calls[f"{prefix}_action"] += 1
        return fixed_scalar_sum(actions)

    def gradient_only(
        self, p52: ModuleType, values: Sequence[Any], *, plain: bool = False
    ) -> np.ndarray:
        gradient_sets = self.gradient_plain if plain else self.gradient_long
        prefix = "plain" if plain else "production"
        gradients = [
            call_generated(p52, item, values, self.dimension)
            for item in gradient_sets
        ]
        self.calls[f"{prefix}_gradient"] += 1
        return fixed_array_sum(gradients, (self.dimension,))

    def hessian_only(
        self, p52: ModuleType, values: Sequence[Any], *, plain: bool = False
    ) -> np.ndarray:
        hessian_sets = self.hessian_plain if plain else self.hessian_long
        prefix = "plain" if plain else "production"
        hessians = [
            call_generated(p52, item, values, self.dimension**2).reshape(
                self.dimension, self.dimension
            )
            for item in hessian_sets
        ]
        self.calls[f"{prefix}_hessian"] += 1
        return fixed_array_sum(hessians, (self.dimension, self.dimension))

    def gradient_hessian(
        self, p52: ModuleType, values: Sequence[Any], *, plain: bool = False
    ) -> tuple[np.ndarray, np.ndarray]:
        return (
            self.gradient_only(p52, values, plain=plain),
            self.hessian_only(p52, values, plain=plain),
        )

    def evaluate(
        self, p52: ModuleType, values: Sequence[Any], *, plain: bool
    ) -> tuple[np.clongdouble, np.ndarray, np.ndarray]:
        return (
            self.action_only(p52, values, plain=plain),
            self.gradient_only(p52, values, plain=plain),
            self.hessian_only(p52, values, plain=plain),
        )


@dataclass
class SourcePlans:
    source_label: str
    m4: ElementDimensionPlan
    m5: ElementDimensionPlan


class ElementCallableAdapter:
    """The minimal ``LongCallableSet.evaluate`` interface used by Phase 51."""

    def __init__(
        self,
        p52: ModuleType,
        plan: ElementDimensionPlan,
        historical_plain: Any,
    ) -> None:
        self.p52 = p52
        self.plan = plan
        self.dimension = plan.dimension
        self.historical_plain = historical_plain

    def evaluate(
        self, values: np.ndarray, *, plain: bool
    ) -> tuple[np.clongdouble, np.ndarray, np.ndarray]:
        if plain:
            # The inherited paired/trajectory control is the pinned Phase-51
            # global non-CSE backend, not a newly invented per-element plain
            # implementation.
            return self.historical_plain.evaluate(values, plain=True)
        return self.plan.evaluate(self.p52, values, plain=plain)


class CompleteElementLocalEvaluator:
    """Selective repaired production evaluator plus the pinned P51 control."""

    def __init__(
        self,
        *,
        source_label: str,
        anchor4: np.ndarray,
        anchor5: np.ndarray,
        inverse_basis_long: np.ndarray,
        kappa_a: np.longdouble,
        kappa_phi: np.longdouble,
        p52: ModuleType,
        m4_plan: ElementDimensionPlan,
        m5_plan: ElementDimensionPlan,
        historical: Any,
    ) -> None:
        self.source_label = source_label
        self.delta_a = historical.delta_a
        self.delta_phi = historical.delta_phi
        self.anchor4 = anchor4
        self.anchor5 = anchor5
        self.inverse_basis_long = inverse_basis_long
        self.kappa_a = kappa_a
        self.kappa_phi = kappa_phi
        self.p52 = p52
        self.m4_plan = m4_plan
        self.m5_plan = m5_plan
        self.historical = historical
        self.m4 = ElementCallableAdapter(p52, m4_plan, historical.m4)
        self.m5 = ElementCallableAdapter(p52, m5_plan, historical.m5)
        self._mode_stack: list[str] = ["full"]
        self.consumer_bindings: list[dict[str, Any]] = []

    def record_binding(self, mode: str, consumer: str) -> None:
        key = (consumer, mode)
        if any(
            (record["consumer"], record["mode"]) == key
            for record in self.consumer_bindings
        ):
            return
        production_hessian_functions = [
            item.function
            for plan in (self.m4_plan, self.m5_plan)
            for item in plan.hessian_long
        ]
        historical_plain_functions = (
            self.historical.m4.joint_plain,
            self.historical.m5.joint_plain,
        )
        hessian_is_repaired = bool(
            production_hessian_functions
            and all(
                function is not historical
                for function in production_hessian_functions
                for historical in historical_plain_functions
            )
        )
        self.consumer_bindings.append(
            {
                "consumer": consumer,
                "mode": mode,
                "production_evaluator_identity": id(self),
                "m4_action_family_identity": id(self.m4_plan.action_long),
                "m4_gradient_family_identity": id(self.m4_plan.gradient_long),
                "m4_hessian_family_identity": id(self.m4_plan.hessian_long),
                "m5_action_family_identity": id(self.m5_plan.action_long),
                "m5_gradient_family_identity": id(self.m5_plan.gradient_long),
                "m5_hessian_family_identity": id(self.m5_plan.hessian_long),
                "historical_plain_evaluator_identity": id(self.historical),
                "hessian_is_repaired_not_historical_plain": hessian_is_repaired,
                "no_hybrid": bool(
                    hessian_is_repaired
                    and self.m4_plan.gradient_long
                    is not self.m4_plan.hessian_long
                    and self.m5_plan.gradient_long
                    is not self.m5_plan.hessian_long
                ),
            }
        )

    @contextmanager
    def mode(self, name: str, *, consumer: str):
        if name not in ("action", "gradient", "gradient_hessian", "full"):
            raise InvalidRun(f"unknown evaluator mode: {name}")
        self._mode_stack.append(name)
        self.record_binding(name, consumer)
        try:
            yield
        finally:
            observed = self._mode_stack.pop()
            if observed != name:
                raise InvalidRun("evaluator mode stack corruption")

    def _coordinates(
        self, w5: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        w_long = np.asarray(w5, dtype=np.clongdouble).reshape(M5)
        coordinates = self.inverse_basis_long @ (
            w_long - np.asarray(self.anchor5, dtype=np.clongdouble)
        )
        w4 = np.asarray(self.anchor4, dtype=np.clongdouble) + coordinates[:M4]
        return w_long, coordinates, w4

    def action_only(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> np.clongdouble:
        if plain:
            return np.clongdouble(
                self.historical.evaluate(lambda_value, w5, plain=True)[0]
            )
        w_long, coordinates, w4 = self._coordinates(w5)
        action4 = self.m4_plan.action_only(self.p52, w4)
        action0 = np.clongdouble(
            action4
            + np.clongdouble("0.5") * self.kappa_a * coordinates[7] ** 2
            + np.clongdouble("0.5") * self.kappa_phi * coordinates[8] ** 2
        )
        action1 = self.m5_plan.action_only(self.p52, w_long)
        lam = np.longdouble(lambda_value)
        return np.clongdouble((np.longdouble(1) - lam) * action0 + lam * action1)

    def gradient_only(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> np.ndarray:
        if plain:
            return np.asarray(
                self.historical.evaluate(lambda_value, w5, plain=True)[1],
                dtype=np.clongdouble,
            )
        w_long, coordinates, w4 = self._coordinates(w5)
        gradient4 = self.m4_plan.gradient_only(self.p52, w4)
        gradient_c = np.concatenate(
            [
                gradient4,
                np.asarray(
                    [
                        self.kappa_a * coordinates[7],
                        self.kappa_phi * coordinates[8],
                    ],
                    dtype=np.clongdouble,
                ),
            ]
        )
        gradient0 = np.asarray(
            self.inverse_basis_long.T @ gradient_c, dtype=np.clongdouble
        )
        gradient1 = self.m5_plan.gradient_only(self.p52, w_long)
        lam = np.longdouble(lambda_value)
        return np.asarray(
            (np.longdouble(1) - lam) * gradient0 + lam * gradient1,
            dtype=np.clongdouble,
        )

    def hessian_only(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> np.ndarray:
        if plain:
            return np.asarray(
                self.historical.evaluate(lambda_value, w5, plain=True)[2],
                dtype=np.clongdouble,
            )
        w_long, _coordinates, w4 = self._coordinates(w5)
        hessian4 = self.m4_plan.hessian_only(self.p52, w4)
        hessian_c = np.zeros((M5, M5), dtype=np.clongdouble)
        hessian_c[:M4, :M4] = hessian4
        hessian_c[7, 7] = self.kappa_a
        hessian_c[8, 8] = self.kappa_phi
        hessian0 = np.asarray(
            self.inverse_basis_long.T @ hessian_c @ self.inverse_basis_long,
            dtype=np.clongdouble,
        )
        hessian1 = self.m5_plan.hessian_only(self.p52, w_long)
        lam = np.longdouble(lambda_value)
        return np.asarray(
            (np.longdouble(1) - lam) * hessian0 + lam * hessian1,
            dtype=np.clongdouble,
        )

    def gradient_hessian(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> tuple[np.ndarray, np.ndarray]:
        if plain:
            values = self.historical.evaluate(lambda_value, w5, plain=True)
            return (
                np.asarray(values[1], dtype=np.clongdouble),
                np.asarray(values[2], dtype=np.clongdouble),
            )
        return (
            self.gradient_only(lambda_value, w5),
            self.hessian_only(lambda_value, w5),
        )

    def evaluate(
        self, lambda_value: float, w5: np.ndarray, *, plain: bool = False
    ) -> tuple[np.clongdouble, np.ndarray, np.ndarray]:
        if plain:
            return self.historical.evaluate(lambda_value, w5, plain=True)
        mode = self._mode_stack[-1]
        if mode == "action":
            action = self.action_only(lambda_value, w5)
            return (
                action,
                np.zeros(M5, dtype=np.clongdouble),
                np.zeros((M5, M5), dtype=np.clongdouble),
            )
        if mode == "gradient":
            gradient = self.gradient_only(lambda_value, w5)
            return (
                np.clongdouble(0),
                gradient,
                np.zeros((M5, M5), dtype=np.clongdouble),
            )
        if mode == "gradient_hessian":
            gradient, hessian = self.gradient_hessian(lambda_value, w5)
            return np.clongdouble(0), gradient, hessian
        self.record_binding("full", "CompleteElementLocalEvaluator.evaluate")
        return (
            self.action_only(lambda_value, w5),
            self.gradient_only(lambda_value, w5),
            self.hessian_only(lambda_value, w5),
        )


@dataclass
class ExecutionAudit:
    """Counters for executions that Phase 51 did not expose explicitly."""

    scope_stack: list[str] = field(default_factory=lambda: ["ordinary"])
    fd_residual_calls: int = 0
    fd_cache_hits: int = 0
    fd_cache_misses: int = 0
    fd_integrations: list[dict[str, Any]] = field(default_factory=list)
    outer_partial_integrations: list[dict[str, Any]] = field(default_factory=list)
    flow_action_integrations: list[dict[str, Any]] = field(default_factory=list)
    flow_event_integrations: list[dict[str, Any]] = field(default_factory=list)
    cache_backend_keys: set[tuple[int, str]] = field(default_factory=set)
    cache_key_schema_check_count: int = 0
    cache_key_schema_all_valid: bool = True
    integrate_invocation_count: int = 0
    integrate_solver_steps_sum: int = 0
    unique_saddle_solves: list[dict[str, Any]] = field(default_factory=list)
    solve_root_records: list[dict[str, Any]] = field(default_factory=list)
    authoritative_reference_slots: list[Any] = field(default_factory=list)
    plain_backend_integration_scopes: list[str] = field(default_factory=list)
    integrate_attempt_records: list[dict[str, Any]] = field(default_factory=list)

    @property
    def scope(self) -> str:
        return self.scope_stack[-1]

    @contextmanager
    def enter(self, name: str):
        self.scope_stack.append(name)
        try:
            yield
        finally:
            observed = self.scope_stack.pop()
            if observed != name:
                raise InvalidRun("execution-audit scope stack corruption")

    def summary(self) -> dict[str, Any]:
        return {
            "full_J_state_only_residual_call_count": self.fd_residual_calls,
            "full_J_cache_hit_count": self.fd_cache_hits,
            "full_J_cache_miss_and_actual_K_integration_count": self.fd_cache_misses,
            "full_J_captured_K_integration_count": len(self.fd_integrations),
            "outer_tangent_partial_lambda_state_integration_count": len(
                self.outer_partial_integrations
            ),
            "flow_action_trajectory_integration_count": len(
                self.flow_action_integrations
            ),
            "flow_first_cap_event_integration_count": len(
                self.flow_event_integrations
            ),
            "cache_backend_identity_keys": [
                {"evaluator_identity": key[0], "backend": key[1]}
                for key in sorted(self.cache_backend_keys)
            ],
            "cache_key_schema_check_count": self.cache_key_schema_check_count,
            "cache_key_includes_evaluator_and_backend_identity": (
                self.cache_key_schema_all_valid
                and self.cache_key_schema_check_count > 0
            ),
            "all_integrate_k_invocation_count": self.integrate_invocation_count,
            "all_integrate_k_solver_steps_sum": self.integrate_solver_steps_sum,
            "unique_saddle_solve_count": len(self.unique_saddle_solves),
            "unique_saddle_solves": self.unique_saddle_solves,
            "solve_root_call_count": len(self.solve_root_records),
            "solve_root_records": self.solve_root_records,
            "plain_backend_integration_scopes": self.plain_backend_integration_scopes,
            "integrate_attempt_records": self.integrate_attempt_records,
            "full_J_integrations": self.fd_integrations,
            "outer_tangent_partial_lambda_integrations": self.outer_partial_integrations,
            "flow_action_trajectory_integrations": self.flow_action_integrations,
            "flow_first_cap_event_integrations": self.flow_event_integrations,
        }


class EvaluatorFactory:
    def __init__(
        self,
        p51: ModuleType,
        p52: ModuleType,
        p52_result: Mapping[str, Any],
        phase52_evaluators: Mapping[str, Any],
        historical_evaluators: Mapping[str, Any],
    ) -> None:
        self.p51 = p51
        self.p52 = p52
        self.p52_result = p52_result
        self.phase52_evaluators = phase52_evaluators
        self.historical_evaluators = historical_evaluators
        self.original_builder = p51.build_long_evaluator
        self.phase41 = load_module(
            "ice_phase41_symbolic_for_phase53", p51.PHASE41_SOURCE_PATH
        )
        self.phase50 = load_module(
            "ice_phase50_symbolic_for_phase53", p51.PHASE50_SOURCE_PATH
        )
        self.plans: dict[str, SourcePlans] = {}
        self.evaluators: dict[str, Any] = {}
        self.execution = ExecutionAudit()

    def substituted_elements(
        self, dimension: int, delta_a: float, delta_phi: float
    ) -> tuple[
        tuple[sp.Symbol, ...],
        tuple[sp.Expr, ...],
        tuple[sp.Expr, ...],
        sp.Expr,
    ]:
        if dimension == M4:
            family = self.phase41.build_symbolic_family()
            scales = self.phase41.COORDINATE_SCALES
        elif dimension == M5:
            family = self.phase50.build_m5_symbolic_family()
            scales = self.phase50.coordinate_scales(self.phase41, 5)
        else:
            raise InvalidRun(f"unsupported element dimension: {dimension}")
        float_substitutions: dict[sp.Symbol, sp.Expr] = {
            family.boundary_a: sp.Float(str(self.phase41.BASE_A), 50),
            family.boundary_phi: sp.Float(str(self.phase41.BASE_PHI), 50),
            family.delta_a: sp.Float(str(delta_a), 50),
            family.delta_phi: sp.Float(str(delta_phi), 50),
        }
        exact_substitutions: dict[sp.Symbol, sp.Expr] = {
            family.boundary_a: sp.Rational(str(self.phase41.BASE_A)),
            family.boundary_phi: sp.Rational(str(self.phase41.BASE_PHI)),
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
        exact_global = sp.expand(family.action_z).subs(exact_substitutions)
        return tuple(family.variables_w), float_elements, exact_elements, exact_global

    def build_dimension(
        self,
        source_label: str,
        dimension: int,
        delta_a: float,
        delta_phi: float,
    ) -> ElementDimensionPlan:
        variables, float_elements, exact_elements, exact_global = (
            self.substituted_elements(dimension, delta_a, delta_phi)
        )
        if dimension == M4:
            global_model = self.phase41.numeric_model(delta_a, delta_phi)
            global_expression_provenance = "phase41.numeric_model"
        else:
            global_model = self.phase50.m5_numeric_model(delta_a, delta_phi)
            global_expression_provenance = "phase50.m5_numeric_model"
        global_action_expr = global_model.action_expr
        global_gradient_expr = tuple(global_model.gradient_expr)
        global_hessian_expr = tuple(global_model.hessian_expr)
        if (
            len(global_gradient_expr) != dimension
            or len(global_hessian_expr) != dimension**2
            or set(global_action_expr.free_symbols) - set(variables)
            or any(
                set(expression.free_symbols) - set(variables)
                for expression in global_gradient_expr + global_hessian_expr
            )
        ):
            raise InvalidRun("independent global symbolic model shape/symbol drift")
        global_expression_raw = json.dumps(
            {
                "action": sp.srepr(global_action_expr),
                "gradient": [sp.srepr(item) for item in global_gradient_expr],
                "hessian": [sp.srepr(item) for item in global_hessian_expr],
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        global_expression_sha256 = hashlib.sha256(
            global_expression_raw
        ).hexdigest()
        # These functions are the authoritative Phase-52 expression route.
        if dimension == M4:
            p52_gradients, exact_gradients, identity_gradient = (
                self.p52.element_gradients_m4(
                    self.phase41, delta_a, delta_phi
                )
            )
        else:
            p52_gradients, exact_gradients, identity_gradient = (
                self.p52.element_gradients_m5(
                    self.phase41, self.phase50, delta_a, delta_phi
                )
            )
        hessians = tuple(
            tuple(
                sp.diff(gradient_component, variable)
                for gradient_component in element_gradient
                for variable in variables
            )
            for element_gradient in p52_gradients
        )
        exact_hessians = tuple(
            tuple(
                sp.diff(gradient_component, variable)
                for gradient_component in element_gradient
                for variable in variables
            )
            for element_gradient in exact_gradients
        )
        identity_hessian = tuple(
            sp.diff(component, variable)
            for component in identity_gradient
            for variable in variables
        )

        action_long = tuple(
            self.p52.make_generated_callable(
                (element,), variables, long_namespace=True
            )
            for element in float_elements
        )
        reused_dimension = getattr(
            self.phase52_evaluators[source_label],
            "m4" if dimension == M4 else "m5",
        )
        gradient_long = tuple(reused_dimension.element_long)
        if tuple(reused_dimension.element_gradients) != tuple(p52_gradients):
            raise InvalidRun("Phase52 reusable gradient expression family drift")
        hessian_long = tuple(
            self.p52.make_generated_callable(
                element, variables, long_namespace=True
            )
            for element in hessians
        )
        action_plain = tuple(
            self.p52.make_plain_callable((element,), variables)
            for element in float_elements
        )
        gradient_plain = tuple(
            self.p52.make_plain_callable(element, variables)
            for element in p52_gradients
        )
        hessian_plain = tuple(
            self.p52.make_plain_callable(element, variables)
            for element in hessians
        )

        action_identity = sp.expand(sum(exact_elements) - exact_global) == 0
        gradient_identity = all(
            sp.expand(
                sum(element[index] for element in exact_gradients)
                - identity_gradient[index]
            )
            == 0
            for index in range(dimension)
        )
        hessian_identity = all(
            sp.expand(
                sum(element[index] for element in exact_hessians)
                - identity_hessian[index]
            )
            == 0
            for index in range(dimension**2)
        )
        action_gradient_derivative_consistency = all(
            sp.expand(sp.diff(exact_global, variables[index]) - identity_gradient[index])
            == 0
            for index in range(dimension)
        )
        gradient_hessian_derivative_consistency = all(
            sp.expand(
                sp.diff(identity_gradient[row], variables[column])
                - identity_hessian[row * dimension + column]
            )
            == 0
            for row in range(dimension)
            for column in range(dimension)
        )
        hessian_symmetry = all(
            sp.expand(
                identity_hessian[row * dimension + column]
                - identity_hessian[column * dimension + row]
            )
            == 0
            for row in range(dimension)
            for column in range(dimension)
        )
        expected_elements = self.p52_result["symbolic_evaluator_ledger"][
            source_label
        ]["elements"]["m4" if dimension == M4 else "m5"]
        ledger: list[Mapping[str, Any]] = []
        for index, (
            action,
            gradient,
            hessian,
            plain_action,
            plain_gradient,
            plain_hessian,
        ) in enumerate(
            zip(
                action_long,
                gradient_long,
                hessian_long,
                action_plain,
                gradient_plain,
                hessian_plain,
                strict=True,
            )
        ):
            expected_gradient = expected_elements[index]
            gradient_record = {
                "back_substitution": self.p52.exact_back_substitution(gradient),
                "dag_sha256": gradient.dag_sha256,
                "index": index,
                "replacement_count": gradient.replacement_count,
                "source_sha256": gradient.source_sha256,
            }
            ledger.append(
                {
                    "index": index,
                    "action": {
                        "replacement_count": action.replacement_count,
                        "source_sha256": action.source_sha256,
                        "dag_sha256": action.dag_sha256,
                        "back_substitution": self.p52.exact_back_substitution(action),
                    },
                    "gradient": gradient_record,
                    "gradient_exact_Phase52_entry": gradient_record
                    == expected_gradient,
                    "hessian": {
                        "replacement_count": hessian.replacement_count,
                        "source_sha256": hessian.source_sha256,
                        "dag_sha256": hessian.dag_sha256,
                        "back_substitution": self.p52.exact_back_substitution(hessian),
                    },
                    "plain": {
                        "action_source_sha256": plain_action.source_sha256,
                        "action_dag_sha256": plain_action.dag_sha256,
                        "gradient_source_sha256": plain_gradient.source_sha256,
                        "gradient_dag_sha256": plain_gradient.dag_sha256,
                        "hessian_source_sha256": plain_hessian.source_sha256,
                        "hessian_dag_sha256": plain_hessian.dag_sha256,
                        "CSE_replacement_count": 0,
                    },
                }
            )
        plan = ElementDimensionPlan(
            dimension=dimension,
            variables=variables,
            float_elements=float_elements,
            exact_elements=exact_elements,
            global_action_expr=global_action_expr,
            global_gradient_expr=global_gradient_expr,
            global_hessian_expr=global_hessian_expr,
            global_expression_provenance=global_expression_provenance,
            global_expression_sha256=global_expression_sha256,
            action_long=action_long,
            gradient_long=gradient_long,
            hessian_long=hessian_long,
            action_plain=action_plain,
            gradient_plain=gradient_plain,
            hessian_plain=hessian_plain,
            exact_identity={
                "action": action_identity,
                "gradient": gradient_identity,
                "hessian": hessian_identity,
                "d_action_equals_gradient": action_gradient_derivative_consistency,
                "d_gradient_equals_hessian": gradient_hessian_derivative_consistency,
                "hessian_symmetric": hessian_symmetry,
            },
            ledger=tuple(ledger),
        )
        self.p51.CSE_EXACT_LEDGER.append(
            {
                "source": source_label,
                "dimension": dimension,
                "construction": "separate_element_action_gradient_hessian_CSE",
                "output_count": len(float_elements)
                * (1 + dimension + dimension**2),
                "replacement_count": sum(
                    item.replacement_count
                    for family in (action_long, gradient_long, hessian_long)
                    for item in family
                ),
                "exact_back_substitution": bool(
                    all(
                        record[family]["back_substitution"]
                        for record in ledger
                        for family in ("action", "gradient", "hessian")
                    )
                ),
                "no_gradient_only_nonCSE_hessian_hybrid": True,
            }
        )
        return plan

    def build(
        self,
        source_label: str,
        delta_a: float,
        delta_phi: float,
        kappa_a: float,
        kappa_phi: float,
        basis_bytes: bytes,
    ) -> Any:
        if source_label in self.evaluators:
            return self.evaluators[source_label]
        m4 = self.build_dimension(
            source_label, M4, float(delta_a), float(delta_phi)
        )
        m5 = self.build_dimension(
            source_label, M5, float(delta_a), float(delta_phi)
        )
        embedding = self.phase50.build_embedding()
        historical = self.historical_evaluators[source_label]
        expected_basis = np.asarray(
            self.phase50.build_embedding().basis, dtype="<f8"
        ).tobytes()
        if basis_bytes != expected_basis:
            raise InvalidRun("historical/repaired evaluator basis binding drift")
        evaluator = CompleteElementLocalEvaluator(
            source_label=source_label,
            anchor4=self.phase50.anchor_w(
                self.phase41, 4, delta_a, delta_phi
            ),
            anchor5=self.phase50.anchor_w(
                self.phase41, 5, delta_a, delta_phi
            ),
            inverse_basis_long=np.asarray(
                embedding.inverse_basis, dtype=np.longdouble
            ),
            kappa_a=np.longdouble(kappa_a),
            kappa_phi=np.longdouble(kappa_phi),
            p52=self.p52,
            m4_plan=m4,
            m5_plan=m5,
            historical=historical,
        )
        self.plans[source_label] = SourcePlans(source_label, m4, m5)
        self.evaluators[source_label] = evaluator
        return evaluator

    def install(self) -> None:
        self.p51.CSE_EXACT_LEDGER.clear()

        @lru_cache(maxsize=None)
        def repaired_builder(
            source_label: str,
            delta_a: float,
            delta_phi: float,
            kappa_a: float,
            kappa_phi: float,
            basis_bytes: bytes,
        ) -> Any:
            return self.build(
                source_label,
                delta_a,
                delta_phi,
                kappa_a,
                kappa_phi,
                basis_bytes,
            )

        self.repaired_builder = repaired_builder
        self.p51.build_long_evaluator = repaired_builder

        original_integrate_k = self.p51.integrate_k
        original_flow_ledger = self.p51.flow_ledger
        original_saddle = self.p51.SourceContext.saddle
        original_node = self.p51.SourceContext.node
        original_fd = self.p51.finite_difference_jacobian_control
        original_outer = self.p51.outer_tangent_control
        original_reflection = self.p51.reflected_state_distances
        original_solve_root = self.p51.solve_root
        original_cse_validation = self.p51.cse_validation
        original_cse_trajectory_validation = self.p51.cse_trajectory_validation
        pinned_p51_source = Path(
            self.p51.__file__ or self.p51.SCRIPT_PATH
        ).read_text(encoding="utf-8")
        self.fallback_source_guard = {
            "historical_Phase51_result_not_loaded_by_runner": (
                "PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_RESULT.json"
                not in pinned_p51_source
            ),
            "random_API_absent": all(
                token not in pinned_p51_source
                for token in ("np.random", "random.random", "default_rng")
            ),
            "array_clipping_absent": "np.clip(" not in pinned_p51_source,
            "chart_recentering_API_absent": "recenter" not in pinned_p51_source.lower(),
            "independent_phi_minus_continuation_present": (
                "minus_fine = solve_path(minus, fine_nodes, minus.p42_seed"
                in pinned_p51_source
            ),
        }
        integrate_source = inspect.getsource(original_integrate_k)
        node_rhs_source = inspect.getsource(self.p51.Node.rhs_long)
        self.convention_source_guard = {
            "pinned_integrate_k_source_sha256": hashlib.sha256(
                integrate_source.encode("utf-8")
            ).hexdigest(),
            "pinned_Node_rhs_long_source_sha256": hashlib.sha256(
                node_rhs_source.encode("utf-8")
            ).hexdigest(),
            "ordinary_transpose_present": "factor_long.T @ gradient" in integrate_source,
            "conjugate_transpose_absent": ".conj().T" not in integrate_source
            and ".conjugate().T" not in integrate_source,
            "one_outer_minus_conjugation_per_state_and_tangent_RHS": (
                integrate_source.count("-np.conjugate(factor_long.T @ gradient)")
                == 2
            ),
            "single_solver_boundary_state": (
                integrate_source.count(
                    "np.asarray(derivative_long, dtype=np.complex128)"
                )
                == 1
            ),
            "single_solver_boundary_tangent": (
                integrate_source.count(
                    "np.asarray(combined, dtype=np.complex128)"
                )
                == 1
            ),
        }

        def repaired_node_rhs(
            node: Any, xi: np.ndarray, *, plain: bool = False
        ) -> np.ndarray:
            w = node.xi_to_w_long(xi)
            evaluator = node.source.evaluator
            if isinstance(evaluator, CompleteElementLocalEvaluator):
                evaluator.record_binding("gradient", "Node.rhs_long")
                gradient = evaluator.gradient_only(
                    node.lambda_value, w, plain=plain
                )
            else:
                gradient = evaluator.evaluate(
                    node.lambda_value, w, plain=plain
                )[1]
            return -np.conjugate(
                np.asarray(node.factor.T, dtype=np.longdouble) @ gradient
            )

        def repaired_integrate_k(
            node: Any,
            chart_parameters: np.ndarray,
            flow_time: float,
            *,
            with_tangent: bool,
            t_eval: np.ndarray | None = None,
            event: bool = False,
            plain_backend: bool = False,
        ) -> Any:
            evaluator = node.source.evaluator
            mode = "gradient_hessian" if with_tangent else "gradient"
            if isinstance(evaluator, CompleteElementLocalEvaluator):
                context = evaluator.mode(
                    mode,
                    consumer=(
                        "integrate_k.tangent_rhs"
                        if with_tangent
                        else "integrate_k.state_rhs"
                    ),
                )
            else:
                context = nullcontext()
            attempt = {
                "source": node.source.label,
                "lambda": float(node.lambda_value),
                "with_tangent": bool(with_tangent),
                "event": bool(event),
                "plain_backend": bool(plain_backend),
                "scope": self.execution.scope,
                "status": "ATTEMPTED",
            }
            self.execution.integrate_attempt_records.append(attempt)
            self.execution.integrate_invocation_count += 1
            try:
                with context:
                    output = original_integrate_k(
                        node,
                        chart_parameters,
                        flow_time,
                        with_tangent=with_tangent,
                        t_eval=t_eval,
                        event=event,
                        plain_backend=plain_backend,
                    )
            except (self.p51.NumericalFailure, FloatingPointError, ValueError) as error:
                attempt.update(
                    {
                        "status": "INCONCLUSIVE",
                        "error_type": type(error).__name__,
                        "message": str(error),
                    }
                )
                raise
            integration = dict(output[2])
            integration.update(
                {
                    "source": node.source.label,
                    "lambda": float(node.lambda_value),
                    "with_tangent": bool(with_tangent),
                    "event": bool(event),
                    "plain_backend": bool(plain_backend),
                }
            )
            attempt.update(
                {
                    "status": "PASS",
                    "solver_steps": int(integration.get("solver_steps", 0)),
                }
            )
            self.execution.integrate_solver_steps_sum += int(
                integration.get("solver_steps", 0)
            )
            if plain_backend:
                self.execution.plain_backend_integration_scopes.append(
                    self.execution.scope
                )
            if self.execution.scope == "fd_state_integration":
                self.execution.fd_integrations.append(integration)
            elif self.execution.scope == "outer_partial_integration":
                self.execution.outer_partial_integrations.append(integration)
            elif self.execution.scope == "flow_ledger":
                if event:
                    self.execution.flow_event_integrations.append(integration)
                else:
                    self.execution.flow_action_integrations.append(integration)
            return output

        def repaired_state_only_residual(
            node: Any,
            parameters: np.ndarray,
            k_cache: dict[tuple[Any, ...], np.ndarray] | None = None,
        ) -> np.ndarray:
            p = np.asarray(parameters, dtype=float)
            gamma = self.p51.gamma_cap(node.source, p[:9])[0]
            evaluator = node.source.evaluator
            backend = "phase53_element_local_production"
            key = (
                id(evaluator),
                backend,
                *(float(value) for value in p[9:18]),
            )
            is_fd = self.execution.scope == "full_J_control"
            is_outer = self.execution.scope == "outer_tangent_control"
            if is_fd:
                self.execution.fd_residual_calls += 1
                self.execution.cache_backend_keys.add((id(evaluator), backend))
                self.execution.cache_key_schema_check_count += 1
                self.execution.cache_key_schema_all_valid = bool(
                    self.execution.cache_key_schema_all_valid
                    and len(key) == 11
                    and key[0] == id(evaluator)
                    and key[1] == backend
                )
            if k_cache is not None and key in k_cache:
                k_state = k_cache[key]
                if is_fd:
                    self.execution.fd_cache_hits += 1
            else:
                nested_scope = (
                    "fd_state_integration"
                    if is_fd
                    else "outer_partial_integration"
                    if is_outer
                    else "ordinary_state_integration"
                )
                with self.execution.enter(nested_scope):
                    k_state = self.p51.integrate_k(
                        node, p[9:17], float(p[17]), with_tangent=False
                    )[0]
                if k_cache is not None:
                    k_cache[key] = k_state
                if is_fd:
                    self.execution.fd_cache_misses += 1
            return self.p51.interleaved(
                (gamma - k_state) / node.source.scales5
            )

        cache_key_source = inspect.getsource(repaired_state_only_residual)
        self.cache_key_source_guard = bool(
            "id(evaluator)" in cache_key_source
            and "backend" in cache_key_source
            and "*(float(value) for value in p[9:18])" in cache_key_source
        )

        def repaired_saddle(source: Any, lambda_value: float) -> np.ndarray:
            evaluator = source.evaluator
            if not isinstance(evaluator, CompleteElementLocalEvaluator):
                return original_saddle(source, lambda_value)
            key = round(float(lambda_value), 14)
            cache_miss = key not in source._saddle_cache
            if cache_miss:
                attempt = {
                    "source": source.label,
                    "lambda": key,
                    "status": "ATTEMPTED",
                    "accepted": False,
                }
                self.execution.unique_saddle_solves.append(attempt)
            else:
                attempt = None
            try:
                with evaluator.mode(
                    "gradient_hessian", consumer="SourceContext.saddle"
                ):
                    output = original_saddle(source, lambda_value)
            except (self.p51.NumericalFailure, FloatingPointError, ValueError) as error:
                if attempt is not None:
                    attempt.update(
                        {
                            "status": "INCONCLUSIVE",
                            "error_type": type(error).__name__,
                            "message": str(error),
                        }
                    )
                raise
            if attempt is not None:
                attempt.update(
                    {
                        "status": "PASS",
                        "accepted": bool(
                            source._saddle_records.get(key, {}).get(
                                "accepted", False
                            )
                        ),
                    }
                )
            return output

        def repaired_node(source: Any, *arguments: Any, **keywords: Any) -> Any:
            evaluator = source.evaluator
            if not isinstance(evaluator, CompleteElementLocalEvaluator):
                return original_node(source, *arguments, **keywords)
            with evaluator.mode(
                "gradient_hessian", consumer="SourceContext.node.launch_Hessian"
            ):
                return original_node(source, *arguments, **keywords)

        def repaired_flow_ledger(node: Any, parameters: np.ndarray) -> Any:
            evaluator = node.source.evaluator
            if not isinstance(evaluator, CompleteElementLocalEvaluator):
                return original_flow_ledger(node, parameters)
            with self.execution.enter("flow_ledger"):
                with evaluator.mode(
                    "action", consumer="flow_ledger.action_samples"
                ):
                    return original_flow_ledger(node, parameters)

        def repaired_fd(*arguments: Any, **keywords: Any) -> Any:
            with self.execution.enter("full_J_control"):
                return original_fd(*arguments, **keywords)

        def repaired_outer(*arguments: Any, **keywords: Any) -> Any:
            with self.execution.enter("outer_tangent_control"):
                return original_outer(*arguments, **keywords)

        def repaired_solve_root(
            node: Any, seed: np.ndarray, *, label: str
        ) -> Any:
            attempt = {
                "label": label,
                "source": node.source.label,
                "lambda": float(node.lambda_value),
                "accepted": False,
                "status": "ATTEMPTED",
                "production_evaluator_identity": id(node.source.evaluator),
            }
            self.execution.solve_root_records.append(attempt)
            try:
                output = original_solve_root(node, seed, label=label)
            except (self.p51.NumericalFailure, FloatingPointError, ValueError) as error:
                attempt.update(
                    {
                        "status": "INCONCLUSIVE",
                        "error_type": type(error).__name__,
                        "message": str(error),
                    }
                )
                raise
            _root, record = output
            record.setdefault("lambda", float(node.lambda_value))
            record.setdefault("label", label)
            record.setdefault("accepted", False)
            attempt.update(
                {
                    "accepted": bool(record.get("accepted", False)),
                    "status": record.get("status"),
                }
            )
            return output

        def repaired_cse_validation(
            source: Any, lambdas: Sequence[float]
        ) -> Any:
            output = original_cse_validation(source, lambdas)
            for raw_lambda in lambdas:
                lambda_value = float(raw_lambda)
                node = source.node(lambda_value)
                state_w5 = np.asarray(
                    node.saddle_w, dtype=np.clongdouble
                ) + np.clongdouble(node.sphere_radius) * (
                    np.asarray(node.launch_w, dtype=np.clongdouble)
                    @ np.asarray(source.chart.center, dtype=np.longdouble)
                )
                inverse = np.asarray(
                    source.evaluator.inverse_basis_long, dtype=np.longdouble
                )
                coordinates = inverse @ (
                    state_w5
                    - np.asarray(source.evaluator.anchor5, dtype=np.clongdouble)
                )
                state_w4 = np.asarray(
                    source.evaluator.anchor4, dtype=np.clongdouble
                ) + coordinates[:M4]
                self.execution.authoritative_reference_slots.append(
                    self.p52.Slot(
                        source=source,
                        node=node,
                        source_label=source.label,
                        lambda_value=lambda_value,
                        state_w5=state_w5,
                        state_w4=state_w4,
                    )
                )
            return output

        def repaired_cse_trajectory_validation(
            *arguments: Any, **keywords: Any
        ) -> Any:
            with self.execution.enter("validation_trajectory"):
                return original_cse_trajectory_validation(
                    *arguments, **keywords
                )

        def repaired_reflection(
            plus_path: Mapping[str, Any],
            minus_path: Mapping[str, Any],
            plus_source: Any,
            minus_source: Any,
        ) -> Any:
            with ExitStack() as stack:
                for source in (plus_source, minus_source):
                    if isinstance(
                        source.evaluator, CompleteElementLocalEvaluator
                    ):
                        stack.enter_context(
                            source.evaluator.mode(
                                "action",
                                consumer="reflected_state_distances.saddle_action",
                            )
                        )
                return original_reflection(
                    plus_path, minus_path, plus_source, minus_source
                )

        self.p51.Node.rhs_long = repaired_node_rhs
        self.p51.integrate_k = repaired_integrate_k
        self.p51.state_only_residual = repaired_state_only_residual
        self.p51.SourceContext.saddle = repaired_saddle
        self.p51.SourceContext.node = repaired_node
        self.p51.flow_ledger = repaired_flow_ledger
        self.p51.finite_difference_jacobian_control = repaired_fd
        self.p51.outer_tangent_control = repaired_outer
        self.p51.reflected_state_distances = repaired_reflection
        self.p51.solve_root = repaired_solve_root
        self.p51.cse_validation = repaired_cse_validation
        self.p51.cse_trajectory_validation = repaired_cse_trajectory_validation

    def p52_projection(self) -> tuple[dict[str, Any], bytes, str]:
        ledger = self.p52_result["symbolic_evaluator_ledger"]
        projection = {
            "source_order": list(SOURCE_ORDER),
            "elements": [
                {
                    "source": source,
                    "m4": ledger[source]["elements"]["m4"],
                    "m5": ledger[source]["elements"]["m5"],
                }
                for source in SOURCE_ORDER
            ],
        }
        raw = json.dumps(
            projection,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return projection, raw, hashlib.sha256(raw).hexdigest()

    def generated_gradient_projection(
        self,
    ) -> tuple[dict[str, Any], bytes, str]:
        projection = {
            "source_order": list(SOURCE_ORDER),
            "elements": [
                {
                    "source": source,
                    "m4": [
                        dict(record["gradient"])
                        for record in self.plans[source].m4.ledger
                    ],
                    "m5": [
                        dict(record["gradient"])
                        for record in self.plans[source].m5.ledger
                    ],
                }
                for source in SOURCE_ORDER
            ],
        }
        raw = json.dumps(
            projection,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return projection, raw, hashlib.sha256(raw).hexdigest()

    def exact_summary(self) -> dict[str, Any]:
        return {
            source: {
                dimension: {
                    "exact_identity": getattr(plans, dimension).exact_identity,
                    "independent_plain_global_reference": {
                        "builder": getattr(
                            plans, dimension
                        ).global_expression_provenance,
                        "expression_sha256": getattr(
                            plans, dimension
                        ).global_expression_sha256,
                    },
                    "elements": list(getattr(plans, dimension).ledger),
                }
                for dimension in ("m4", "m5")
            }
            for source, plans in self.plans.items()
        }

    def call_summary(self) -> dict[str, Any]:
        return {
            source: {
                dimension: dict(getattr(plans, dimension).calls)
                for dimension in ("m4", "m5")
            }
            for source, plans in self.plans.items()
        }

    def binding_summary(self) -> dict[str, Any]:
        return {
            source: {
                "consumer_bindings": evaluator.consumer_bindings,
                "plain_backend_is_saved_pinned_Phase51_evaluator": (
                    evaluator.historical is not evaluator
                ),
                "plain_backend_identity": id(evaluator.historical),
                "production_identity": id(evaluator),
                "action_gradient_hessian_families_pairwise_distinct": all(
                    len(
                        {
                            id(plan.action_long),
                            id(plan.gradient_long),
                            id(plan.hessian_long),
                        }
                    )
                    == 3
                    for plan in (
                        self.plans[source].m4,
                        self.plans[source].m5,
                    )
                ),
            }
            for source, evaluator in self.evaluators.items()
        }

    def cache_summary(self) -> dict[str, Any]:
        def record(callable_value: Any) -> Any:
            info = getattr(callable_value, "cache_info", lambda: None)()
            if info is None:
                return None
            return {
                "hits": info.hits,
                "misses": info.misses,
                "maxsize": info.maxsize,
                "currsize": info.currsize,
            }

        return {
            "original_Phase51_builder": record(self.original_builder),
            "Phase53_repaired_builder": record(self.repaired_builder),
            "Phase51_CSE_exact_ledger_count": len(self.p51.CSE_EXACT_LEDGER),
            "full_J_cache_key_source_includes_evaluator_backend_and_parameters": (
                self.cache_key_source_guard
            ),
        }


@dataclass
class Preflight:
    bundle: InputBundle
    p51: ModuleType
    p52: ModuleType
    factory: EvaluatorFactory
    contexts: list[Any]
    slots: list[Any]
    slot_origin: str
    context_validation: dict[str, Any]


def build_preflight(bundle: InputBundle) -> Preflight:
    p51 = load_module("ice_phase51_for_phase53", bundle.p51_runner_path)
    p52 = load_module("ice_phase52_for_phase53", bundle.p52_runner_path)
    # Reproduce the pinned Phase52 construction order first.  This yields the
    # actual gradient callable objects, including their deterministic SymPy
    # Dummy identifiers/source bytes, rather than merely copying ledger hashes.
    p51.CSE_EXACT_LEDGER.clear()
    if hasattr(p51.build_long_evaluator, "cache_clear"):
        p51.build_long_evaluator.cache_clear()
    original_contexts, original_validation = p52.build_phase51_contexts(
        p51, bundle.p51_manifest
    )
    phase52_evaluators, phase52_ledger = p52.build_symbolic_evaluators(
        p51, original_contexts
    )
    if phase52_ledger != bundle.p52_result["symbolic_evaluator_ledger"]:
        raise InvalidRun("reconstructed Phase52 symbolic evaluator ledger drift")
    factory = EvaluatorFactory(
        p51,
        p52,
        bundle.p52_result,
        phase52_evaluators,
        {context.label: context.evaluator for context in original_contexts},
    )
    factory.install()
    contexts, context_validation = p52.build_phase51_contexts(
        p51, bundle.p51_manifest
    )
    if [context.label for context in contexts] != list(SOURCE_ORDER):
        raise InvalidRun("Phase51 source context order drift")
    # Validation/reference slots use the pinned Phase50 saddles directly, so
    # --validate-only never invokes a saddle/root solve.
    for context in contexts:
        for lambda_value in LAMBDA_ORDER:
            key = round(float(lambda_value), 14)
            if key not in context.p50_saddles:
                raise InvalidRun(
                    f"missing pinned Phase50 reference saddle: {context.label}:{key}"
                )
            context._saddle_cache[key] = np.asarray(
                context.p50_saddles[key], dtype=float
            ).copy()
    provisional_slots = p52.build_slots(contexts, SOURCE_ORDER, LAMBDA_ORDER)
    slots: list[Any] = []
    for slot in provisional_slots:
        frozen_pairs = bundle.p52_result["reference_validation"][slot.key][
            "input_lift"
        ]["state_w5_25_digit_pairs"]
        state_w5 = np.asarray(
            [
                np.clongdouble(np.longdouble(real))
                + np.clongdouble(1j) * np.clongdouble(np.longdouble(imaginary))
                for real, imaginary in frozen_pairs
            ],
            dtype=np.clongdouble,
        )
        inverse = np.asarray(
            slot.source.evaluator.inverse_basis_long, dtype=np.longdouble
        )
        coordinates = inverse @ (
            state_w5
            - np.asarray(slot.source.evaluator.anchor5, dtype=np.clongdouble)
        )
        state_w4 = np.asarray(
            slot.source.evaluator.anchor4, dtype=np.clongdouble
        ) + coordinates[:M4]
        slots.append(
            p52.Slot(
                source=slot.source,
                node=slot.node,
                source_label=slot.source_label,
                lambda_value=slot.lambda_value,
                state_w5=state_w5,
                state_w4=state_w4,
            )
        )
    if (
        len(slots) != 6
        or [slot.source_label for slot in slots]
        != [source for source in SOURCE_ORDER for _ in LAMBDA_ORDER]
        or [float(slot.lambda_value) for slot in slots]
        != list(LAMBDA_ORDER) * len(SOURCE_ORDER)
    ):
        raise InvalidRun("six-slot source/lambda preenumeration drift")
    if set(factory.plans) != set(SOURCE_ORDER) or len(p51.CSE_EXACT_LEDGER) != 4:
        raise InvalidRun("complete evaluator construction count drift")
    context_validation = {
        "Phase52_order_original_context_validation": original_validation,
        "Phase53_repaired_context_validation": context_validation,
    }
    return Preflight(
        bundle=bundle,
        p51=p51,
        p52=p52,
        factory=factory,
        contexts=contexts,
        slots=slots,
        slot_origin="pinned_Phase52_six_slot_input_for_implementation_trace_only",
        context_validation=context_validation,
    )


def _merge_count(target: dict[str, int], source: Mapping[str, Any]) -> None:
    for key, value in source.items():
        target[str(key)] = target.get(str(key), 0) + int(value)


def dtype_audit(
    preflight: Preflight, slots: Sequence[Any] | None = None
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    all_pass = True
    audited_slots = list(preflight.slots if slots is None else slots)
    for slot in audited_slots:
        plans = preflight.factory.plans[slot.source_label]
        for dimension_name, plan, state in (
            ("m4", plans.m4, slot.state_w4),
            ("m5", plans.m5, slot.state_w5),
        ):
            for family_name, family, output_count in (
                ("action", plan.action_long, 1),
                ("gradient", plan.gradient_long, plan.dimension),
                ("hessian", plan.hessian_long, plan.dimension**2),
            ):
                temporary_counts: dict[str, int] = {}
                raw_counts: dict[str, int] = {}
                per_element: list[dict[str, Any]] = []
                for index, callable_set in enumerate(family):
                    raw, trace = preflight.p52.traced_call(callable_set, state)
                    passed = bool(
                        raw.size == output_count
                        and trace["replacement_count"]
                        == trace["traced_temporary_count"]
                        and trace["raw_output_count"] == output_count
                        and trace["all_temporary_scalars_exact_clongdouble"]
                        and trace["all_raw_scalars_exact_clongdouble"]
                        and trace["replacement_names_exact"]
                        and trace["return_object_identity_exact"]
                    )
                    all_pass = bool(all_pass and passed)
                    _merge_count(
                        temporary_counts, trace["temporary_dtype_counts"]
                    )
                    _merge_count(raw_counts, trace["raw_output_dtype_counts"])
                    per_element.append(
                        {
                            "index": index,
                            "passed": passed,
                            **trace,
                        }
                    )
                records.append(
                    {
                        "slot": slot.key,
                        "source": slot.source_label,
                        "lambda": float(slot.lambda_value),
                        "dimension": dimension_name,
                        "family": family_name,
                        "element_count": len(family),
                        "expected_output_count_per_element": output_count,
                        "temporary_dtype_counts": temporary_counts,
                        "raw_output_dtype_counts": raw_counts,
                        "passed": all(item["passed"] for item in per_element),
                        "elements": per_element,
                    }
                )
    return {
        "slot_count": len(audited_slots),
        "trace_record_count": len(records),
        "all_traces_complete_and_exact_clongdouble": all_pass,
        "audited_callable_objects_are_production_bound": all(
            preflight.factory.evaluators[source].m4_plan
            is preflight.factory.plans[source].m4
            and preflight.factory.evaluators[source].m5_plan
            is preflight.factory.plans[source].m5
            for source in SOURCE_ORDER
        ),
        "records": records,
    }


def exact_evaluator_audit(preflight: Preflight) -> dict[str, Any]:
    factory = preflight.factory
    _p52_projection, p52_raw, p52_digest = factory.p52_projection()
    generated_projection, generated_raw, generated_digest = (
        factory.generated_gradient_projection()
    )
    identities = {
        source: {
            dimension: dict(getattr(factory.plans[source], dimension).exact_identity)
            for dimension in ("m4", "m5")
        }
        for source in SOURCE_ORDER
    }
    identity_pass = all(
        bool(value)
        for source in identities.values()
        for dimension in source.values()
        for value in dimension.values()
    )
    gradient_entries_exact = all(
        bool(record["gradient_exact_Phase52_entry"])
        for source in SOURCE_ORDER
        for plan in (factory.plans[source].m4, factory.plans[source].m5)
        for record in plan.ledger
    )
    action_hessian_backsub = all(
        bool(record[family]["back_substitution"])
        for source in SOURCE_ORDER
        for plan in (factory.plans[source].m4, factory.plans[source].m5)
        for record in plan.ledger
        for family in ("action", "hessian")
    )
    all_backsub = all(
        bool(record[family]["back_substitution"])
        for source in SOURCE_ORDER
        for plan in (factory.plans[source].m4, factory.plans[source].m5)
        for record in plan.ledger
        for family in ("action", "gradient", "hessian")
    )
    projection_pass = bool(
        p52_digest == EXPECTED_P52_ELEMENT_PROJECTION_SHA256
        and generated_digest == EXPECTED_P52_ELEMENT_PROJECTION_SHA256
        and p52_raw == generated_raw
        and len(p52_raw) == EXPECTED_P52_ELEMENT_PROJECTION_BYTES
        and gradient_entries_exact
    )
    return {
        "exact_identities": identities,
        "all_action_gradient_hessian_element_and_derivative_identities": identity_pass,
        "Phase52_full_generated_callable_ledger_sha256": preflight.bundle.p52_result.get(
            "generated_callable_ledger_sha256"
        ),
        "Phase52_projection_sha256": p52_digest,
        "Phase53_generated_projection_sha256": generated_digest,
        "projection_canonical_bytes": len(generated_raw),
        "projection_byte_identical": p52_raw == generated_raw,
        "projection_exact_reuse_passed": projection_pass,
        "generated_projection": generated_projection,
        "action_hessian_CSE_back_substitution_passed": action_hessian_backsub,
        "all_three_plan_families_back_substitute": all_backsub,
        "complete_ledger": factory.exact_summary(),
    }


def fixed_order_and_binding_audit(
    preflight: Preflight,
    calls: Mapping[str, Any],
    binding: Mapping[str, Any],
) -> dict[str, Any]:
    scalar_source = inspect.getsource(fixed_scalar_sum)
    array_source = inspect.getsource(fixed_array_sum)
    plan_source = inspect.getsource(ElementDimensionPlan)
    expected_consumers = {
        "SourceContext.saddle",
        "SourceContext.node.launch_Hessian",
        "integrate_k.state_rhs",
        "integrate_k.tangent_rhs",
        "Node.rhs_long",
        "flow_ledger.action_samples",
        "reflected_state_distances.saddle_action",
        "CompleteElementLocalEvaluator.evaluate",
    }
    consumer_sets = {
        source: {
            record["consumer"] for record in details["consumer_bindings"]
        }
        for source, details in binding.items()
    }
    consumer_set_exact = all(
        consumer_sets.get(source) == expected_consumers
        for source in SOURCE_ORDER
    )
    no_hybrid_derived = all(
        all(
            record["no_hybrid"]
            and record["hessian_is_repaired_not_historical_plain"]
            for record in binding[source]["consumer_bindings"]
        )
        and binding[source][
            "action_gradient_hessian_families_pairwise_distinct"
        ]
        and binding[source][
            "plain_backend_is_saved_pinned_Phase51_evaluator"
        ]
        for source in SOURCE_ORDER
    )
    call_paths_complete = all(
        all(
            int(calls[source][dimension][f"production_{family}"]) > 0
            for family in ("action", "gradient", "hessian")
        )
        and all(
            int(calls[source][dimension][f"plain_{family}"]) == 0
            for family in ("action", "gradient", "hessian")
        )
        for source in SOURCE_ORDER
        for dimension in ("m4", "m5")
    )
    scalar_probe = [
        np.clongdouble("1e20"),
        np.clongdouble("-1e20"),
        np.clongdouble(1),
    ]
    scalar_manual = np.clongdouble(0)
    for value in scalar_probe:
        scalar_manual = np.clongdouble(scalar_manual + value)
    array_probe = [
        np.asarray([[value, -value]], dtype=np.clongdouble)
        for value in scalar_probe
    ]
    array_manual = np.zeros((1, 2), dtype=np.clongdouble)
    for value in array_probe:
        for index in np.ndindex((1, 2)):
            array_manual[index] = np.clongdouble(
                array_manual[index] + value[index]
            )
    runtime_probe_exact = bool(
        fixed_scalar_sum(scalar_probe) == scalar_manual
        and np.array_equal(fixed_array_sum(array_probe, (1, 2)), array_manual)
    )
    source_guard = bool(
        "for value in values" in scalar_source
        and "np.sum" not in scalar_source
        and "math.fsum" not in scalar_source
        and "mp.fsum" not in scalar_source
        and "for value in values" in array_source
        and "for index in np.ndindex(shape)" in array_source
        and "np.sum" not in array_source
        and "fixed_scalar_sum(actions)" in plan_source
        and "fixed_array_sum(gradients" in plan_source
        and "fixed_array_sum(hessians" in plan_source
    )
    return {
        "passed": bool(
            consumer_set_exact
            and no_hybrid_derived
            and call_paths_complete
            and runtime_probe_exact
            and source_guard
        ),
        "expected_consumer_set": sorted(expected_consumers),
        "observed_consumer_sets": {
            source: sorted(values) for source, values in consumer_sets.items()
        },
        "consumer_set_exact": consumer_set_exact,
        "no_hybrid_derived_from_callable_identities": no_hybrid_derived,
        "production_all_three_families_called_and_per_element_plain_unused": call_paths_complete,
        "fixed_order_runtime_probe_exact": runtime_probe_exact,
        "fixed_order_source_guard": source_guard,
        "fixed_scalar_sum_source_sha256": hashlib.sha256(
            scalar_source.encode("utf-8")
        ).hexdigest(),
        "fixed_array_sum_source_sha256": hashlib.sha256(
            array_source.encode("utf-8")
        ).hexdigest(),
    }


def mp_fixed_sum(values: Sequence[Any]) -> mp.mpc:
    total = mp.mpc(0)
    for value in values:
        total = mp.mpc(total + mp.mpc(value))
    return total


def mp_fixed_vectors(
    vectors: Sequence[Sequence[Any]], length: int
) -> list[mp.mpc]:
    output = [mp.mpc(0) for _ in range(length)]
    for vector in vectors:
        if len(vector) != length:
            raise InvalidRun("mp fixed vector accumulation length drift")
        for index in range(length):
            output[index] = mp.mpc(output[index] + mp.mpc(vector[index]))
    return output


def direct_dimension_reference(
    p52: ModuleType,
    plan: ElementDimensionPlan,
    values: Sequence[Any],
    digits: int,
) -> dict[str, Any]:
    dimension = plan.dimension
    # The plain reference is deliberately not reconstructed from any Phase-53
    # element or generated-callable output.  These three expressions come from
    # the pinned Phase-41/50 independent global numeric-model builders.
    plain_action = p52.direct_evalf_gradient(
        (plan.global_action_expr,), plan.variables, values, digits
    )[0]
    plain_gradient = p52.direct_evalf_gradient(
        plan.global_gradient_expr, plan.variables, values, digits
    )
    plain_hessian = p52.direct_evalf_gradient(
        plan.global_hessian_expr, plan.variables, values, digits
    )

    cse_actions = [
        p52.direct_evalf_cse_gradient(
            callable_set, plan.variables, values, digits
        )[0]
        for callable_set in plan.action_long
    ]
    cse_gradients = [
        p52.direct_evalf_cse_gradient(
            callable_set, plan.variables, values, digits
        )
        for callable_set in plan.gradient_long
    ]
    cse_hessians = [
        p52.direct_evalf_cse_gradient(
            callable_set, plan.variables, values, digits
        )
        for callable_set in plan.hessian_long
    ]
    return {
        "plain_global_expression_source": plan.global_expression_provenance,
        "plain_global_expression_sha256": plan.global_expression_sha256,
        "plain": {
            "action": mp.mpc(plain_action),
            "gradient": [mp.mpc(value) for value in plain_gradient],
            "hessian": [mp.mpc(value) for value in plain_hessian],
        },
        "symbolic_CSE": {
            "action": mp_fixed_sum(cse_actions),
            "gradient": mp_fixed_vectors(cse_gradients, dimension),
            "hessian": mp_fixed_vectors(cse_hessians, dimension**2),
        },
    }


def reference_vector_digest_summary(
    reference: Mapping[str, Any], digits: int
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for backend in ("plain", "symbolic_CSE"):
        vectors = reference[backend]
        canonical = {
            quantity: [
                [
                    mp.nstr(mp.mpc(value).real, n=digits + 5, strip_zeros=False),
                    mp.nstr(mp.mpc(value).imag, n=digits + 5, strip_zeros=False),
                ]
                for value in vector
            ]
            for quantity, vector in vectors.items()
        }
        raw = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        summary[backend] = {
            "quantity_vector_lengths": {
                quantity: len(vector) for quantity, vector in vectors.items()
            },
            "canonical_decimal_digits": digits + 5,
            "canonical_bytes": len(raw),
            "canonical_sha256": hashlib.sha256(raw).hexdigest(),
        }
    return summary


def _mp_matrix(flat: Sequence[Any], rows: int, columns: int) -> mp.matrix:
    if len(flat) != rows * columns:
        raise InvalidRun("mp matrix shape drift")
    return mp.matrix(
        [
            [mp.mpc(flat[row * columns + column]) for column in range(columns)]
            for row in range(rows)
        ]
    )


def _mp_flat(matrix: mp.matrix) -> list[mp.mpc]:
    return [
        mp.mpc(matrix[row, column])
        for row in range(matrix.rows)
        for column in range(matrix.cols)
    ]


def compose_full_reference(
    p52: ModuleType,
    slot: Any,
    plans: SourcePlans,
    digits: int,
) -> dict[str, dict[str, Any]]:
    with mp.workdps(digits + 30):
        source = slot.source
        state5 = p52.mp_frozen_state_vector(slot.state_w5)
        inverse = p52.mp_matrix_real(source.evaluator.inverse_basis_long)
        anchor5 = p52.mp_vector(source.evaluator.anchor5)
        anchor4 = p52.mp_vector(source.evaluator.anchor4)
        coordinates = p52.mp_matvec(
            inverse,
            [state5[index] - anchor5[index] for index in range(M5)],
        )
        state4 = [anchor4[index] + coordinates[index] for index in range(M4)]
        dimension4 = direct_dimension_reference(
            p52, plans.m4, state4, digits
        )
        dimension5 = direct_dimension_reference(
            p52, plans.m5, state5, digits
        )
        lam = p52.mp_real(np.longdouble(slot.lambda_value))
        complement = mp.mpf(1) - lam
        inverse_t = inverse.T
        factor = p52.mp_matrix_real(slot.node.factor)
        kappa_a = p52.mp_real(source.evaluator.kappa_a)
        kappa_phi = p52.mp_real(source.evaluator.kappa_phi)

        def compose(backend: str) -> dict[str, Any]:
            value4 = dimension4[backend]
            value5 = dimension5[backend]
            action0 = (
                value4["action"]
                + mp.mpf("0.5") * kappa_a * coordinates[7] ** 2
                + mp.mpf("0.5") * kappa_phi * coordinates[8] ** 2
            )
            gradient_c = [*value4["gradient"]]
            gradient_c.extend(
                [kappa_a * coordinates[7], kappa_phi * coordinates[8]]
            )
            gradient0 = p52.mp_matvec(inverse_t, gradient_c)
            hessian_c = mp.matrix(M5, M5)
            hessian4 = _mp_matrix(value4["hessian"], M4, M4)
            for row in range(M4):
                for column in range(M4):
                    hessian_c[row, column] = hessian4[row, column]
            hessian_c[7, 7] = kappa_a
            hessian_c[8, 8] = kappa_phi
            hessian0 = inverse_t * hessian_c * inverse
            hessian5 = _mp_matrix(value5["hessian"], M5, M5)
            action = complement * action0 + lam * value5["action"]
            gradient = [
                complement * gradient0[index]
                + lam * value5["gradient"][index]
                for index in range(M5)
            ]
            hessian = complement * hessian0 + lam * hessian5
            contracted = p52.mp_matvec(factor.T, gradient)
            rhs = [-mp.conj(value) for value in contracted]
            factor_hessian = factor.T * hessian * factor
            return {
                "action": [mp.mpc(action)],
                "gradient": [mp.mpc(value) for value in gradient],
                "hessian": _mp_flat(hessian),
                "completed_state_RHS": [mp.mpc(value) for value in rhs],
                "canonical_Hessian_actions": _mp_flat(hessian),
                "canonical_factor_Hessian_actions": _mp_flat(factor_hessian),
            }

        return {
            "plain": compose("plain"),
            "symbolic_CSE": compose("symbolic_CSE"),
            "plain_global_expression_sources": {
                "m4": {
                    "builder": dimension4["plain_global_expression_source"],
                    "sha256": dimension4["plain_global_expression_sha256"],
                },
                "m5": {
                    "builder": dimension5["plain_global_expression_source"],
                    "sha256": dimension5["plain_global_expression_sha256"],
                },
            },
        }


def production_slot_values(p52: ModuleType, slot: Any) -> dict[str, Any]:
    action, gradient, hessian = slot.source.evaluator.evaluate(
        slot.lambda_value, slot.state_w5, plain=False
    )
    factor = np.asarray(slot.node.factor, dtype=np.longdouble)
    rhs = -np.conjugate(factor.T @ gradient)
    factor_hessian = factor.T @ hessian @ factor
    return {
        "action": p52.mp_vector(np.asarray([action], dtype=np.clongdouble)),
        "gradient": p52.mp_vector(gradient),
        "hessian": p52.mp_vector(hessian.reshape(-1)),
        "completed_state_RHS": p52.mp_vector(rhs),
        "canonical_Hessian_actions": p52.mp_vector(hessian.reshape(-1)),
        "canonical_factor_Hessian_actions": p52.mp_vector(
            factor_hessian.reshape(-1)
        ),
    }


def mp_metric(left: Sequence[Any], right: Sequence[Any]) -> dict[str, Any]:
    if len(left) != len(right):
        raise InvalidRun("mp metric vector length drift")
    differences = [mp.mpc(a) - mp.mpc(b) for a, b in zip(left, right, strict=True)]
    absolute = mp.sqrt(mp.fsum(abs(value) ** 2 for value in differences))
    left_norm = mp.sqrt(mp.fsum(abs(value) ** 2 for value in left))
    right_norm = mp.sqrt(mp.fsum(abs(value) ** 2 for value in right))
    relative = absolute / max(left_norm, right_norm, mp.mpf("1e-100"))
    maximum = max((abs(value) for value in differences), default=mp.mpf(0))
    return {
        "symmetric_normwise_relative": mp.mpf(relative),
        "normwise_absolute": mp.mpf(absolute),
        "maximum_component_absolute": mp.mpf(maximum),
    }


def six_slot_reference_audit(
    preflight: Preflight, slots: Sequence[Any] | None = None
) -> dict[str, Any]:
    p52_thresholds = require(
        preflight.bundle.p52_manifest, "thresholds", where="Phase52 manifest"
    )
    p51_thresholds = require(
        preflight.bundle.p51_manifest, "thresholds", where="Phase51 manifest"
    )
    thresholds = {
        "80_vs_120": mp.mpf(
            str(require(p52_thresholds, "mpmath_80_vs_120_relative_max", where="Phase52 thresholds"))
        ),
        "symbolic_CSE_vs_plain": mp.mpf(
            str(require(p52_thresholds, "mpmath_CSE_vs_nonCSE_relative_max", where="Phase52 thresholds"))
        ),
        "gradient_to_120": mp.mpf(
            str(require(p52_thresholds, "candidate_gradient_to_120dps_relative_max", where="Phase52 thresholds"))
        ),
        "RHS_to_120": mp.mpf(
            str(require(p52_thresholds, "candidate_RHS_to_120dps_relative_max", where="Phase52 thresholds"))
        ),
        "common_action_Hessian_action": mp.mpf(
            str(require(p51_thresholds, "CSE_nonCSE_hessian_action_relative_max", where="Phase51 thresholds"))
        ),
    }
    records: list[dict[str, Any]] = []
    all_pass = True
    audited_slots = list(preflight.slots if slots is None else slots)
    for slot in audited_slots:
        progress(f"direct 80/120-decimal full reference: {slot.key}")
        reference80 = compose_full_reference(
            preflight.p52,
            slot,
            preflight.factory.plans[slot.source_label],
            80,
        )
        reference120 = compose_full_reference(
            preflight.p52,
            slot,
            preflight.factory.plans[slot.source_label],
            120,
        )
        with mp.workdps(150):
            reference_provenance = reference120[
                "plain_global_expression_sources"
            ]
            if (
                reference80["plain_global_expression_sources"]
                != reference_provenance
                or reference_provenance["m4"]["builder"]
                != "phase41.numeric_model"
                or reference_provenance["m5"]["builder"]
                != "phase50.m5_numeric_model"
            ):
                raise InvalidRun("independent global reference provenance drift")
            reference_vector_digests = {
                "80_decimal": reference_vector_digest_summary(reference80, 80),
                "120_decimal": reference_vector_digest_summary(reference120, 120),
            }
            production = production_slot_values(preflight.p52, slot)
            metrics: dict[str, Any] = {}
            slot_pass = True
            for quantity in reference120["plain"]:
                metric_80_120 = mp_metric(
                    reference80["plain"][quantity],
                    reference120["plain"][quantity],
                )
                metric_cse_plain = mp_metric(
                    reference120["symbolic_CSE"][quantity],
                    reference120["plain"][quantity],
                )
                metric_cse_plain_80 = mp_metric(
                    reference80["symbolic_CSE"][quantity],
                    reference80["plain"][quantity],
                )
                metric_production = mp_metric(
                    production[quantity], reference120["plain"][quantity]
                )
                if quantity == "gradient":
                    production_threshold = thresholds["gradient_to_120"]
                elif quantity == "completed_state_RHS":
                    production_threshold = thresholds["RHS_to_120"]
                else:
                    production_threshold = thresholds[
                        "common_action_Hessian_action"
                    ]
                quantity_pass = bool(
                    metric_80_120["symmetric_normwise_relative"]
                    <= thresholds["80_vs_120"]
                    and metric_cse_plain["symmetric_normwise_relative"]
                    <= thresholds["symbolic_CSE_vs_plain"]
                    and metric_cse_plain_80["symmetric_normwise_relative"]
                    <= thresholds["symbolic_CSE_vs_plain"]
                    and metric_production["symmetric_normwise_relative"]
                    <= production_threshold
                )
                slot_pass = bool(slot_pass and quantity_pass)
                metrics[quantity] = {
                    "80_vs_120": metric_80_120,
                    "symbolic_CSE_vs_plain_80": metric_cse_plain_80,
                    "symbolic_CSE_vs_plain_120": metric_cse_plain,
                    "production_vs_plain_120": metric_production,
                    "production_threshold": production_threshold,
                    "passed": quantity_pass,
                }
            probe_records: list[dict[str, Any]] = []
            for column in range(M5):
                indices = [row * M5 + column for row in range(M5)]
                plain80 = [
                    reference80["plain"]["hessian"][index]
                    for index in indices
                ]
                cse80 = [
                    reference80["symbolic_CSE"]["hessian"][index]
                    for index in indices
                ]
                plain120 = [
                    reference120["plain"]["hessian"][index]
                    for index in indices
                ]
                cse120 = [
                    reference120["symbolic_CSE"]["hessian"][index]
                    for index in indices
                ]
                production_probe = [
                    production["hessian"][index] for index in indices
                ]
                probe_metrics = {
                    "80_vs_120": mp_metric(plain80, plain120),
                    "symbolic_CSE_vs_plain_80": mp_metric(cse80, plain80),
                    "symbolic_CSE_vs_plain_120": mp_metric(cse120, plain120),
                    "production_vs_plain_120": mp_metric(
                        production_probe, plain120
                    ),
                }
                probe_pass = bool(
                    probe_metrics["80_vs_120"]["symmetric_normwise_relative"]
                    <= thresholds["80_vs_120"]
                    and probe_metrics["symbolic_CSE_vs_plain_80"][
                        "symmetric_normwise_relative"
                    ]
                    <= thresholds["symbolic_CSE_vs_plain"]
                    and probe_metrics["symbolic_CSE_vs_plain_120"][
                        "symmetric_normwise_relative"
                    ]
                    <= thresholds["symbolic_CSE_vs_plain"]
                    and probe_metrics["production_vs_plain_120"][
                        "symmetric_normwise_relative"
                    ]
                    <= thresholds["common_action_Hessian_action"]
                )
                slot_pass = bool(slot_pass and probe_pass)
                probe_records.append(
                    {
                        "probe_index": column,
                        "probe_label": f"canonical_complex_basis_e{column}",
                        "action": "complete_Hessian_times_probe",
                        "metrics": probe_metrics,
                        "passed": probe_pass,
                    }
                )
        all_pass = bool(all_pass and slot_pass)
        records.append(
            {
                "slot": slot.key,
                "source": slot.source_label,
                "lambda": float(slot.lambda_value),
                "input_state_w5": np.asarray(
                    slot.state_w5, dtype=np.clongdouble
                ),
                "plain_global_expression_sources": reference_provenance,
                "reference_vector_digests": reference_vector_digests,
                "metrics": metrics,
                "Hessian_canonical_basis_probe_count": len(probe_records),
                "Hessian_canonical_basis_probes": probe_records,
                "passed": slot_pass,
            }
        )
    return {
        "slot_count": len(records),
        "precision_tiers_decimal_digits": [80, 120],
        "thresholds": thresholds,
        "all_slots_passed": all_pass,
        "Hessian_canonical_basis_probe_total": sum(
            record["Hessian_canonical_basis_probe_count"] for record in records
        ),
        "records": records,
        "backend_boundary": (
            "plain uses the independent pinned Phase41 numeric_model and "
            "Phase50 m5_numeric_model global action/gradient/Hessian expressions; "
            "symbolic-CSE uses the Phase53 element plans through direct SymPy "
            "back-substitution; only production invokes generated callables"
        ),
    }


def _all_numeric_leaves_finite(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(_all_numeric_leaves_finite(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return all(_all_numeric_leaves_finite(item) for item in value)
    if isinstance(value, np.ndarray):
        return bool(np.all(np.isfinite(value)))
    if isinstance(value, (float, np.floating, complex, np.complexfloating)):
        return bool(np.all(np.isfinite(value)))
    return True


def execution_topology_audit(
    preflight: Preflight, engine: Mapping[str, Any]
) -> dict[str, Any]:
    expected = require(
        require(
            require(
                preflight.bundle.manifest,
                "phase51_contract_inheritance",
                where="manifest",
            ),
            "semantic_replay",
            where="phase51_contract_inheritance",
        ),
        "expected_topology",
        where="phase51_contract_inheritance.semantic_replay",
    )
    paths = {
        "phi_plus_fine_forward": engine["primary_phi_plus"]["fine_forward"]["records"],
        "phi_plus_coarse_forward": engine["primary_phi_plus"]["coarse_forward"]["records"],
        "phi_plus_fine_reverse": engine["primary_phi_plus"]["fine_reverse"]["records"],
        "phi_minus_fine_forward": engine["independent_phi_minus_reflection"]["fine_forward"]["records"],
    }
    expected_paths = expected["primary_and_reflection_path_root_records"]
    path_counts = {key: len(value) for key, value in paths.items()}
    continuation = preflight.bundle.p51_manifest["continuation"]
    expected_path_lambdas = {
        "phi_plus_fine_forward": [float(value) for value in continuation["fine_forward"]],
        "phi_plus_coarse_forward": [float(value) for value in continuation["coarse_forward"]],
        "phi_plus_fine_reverse": [float(value) for value in continuation["fine_reverse"]],
        "phi_minus_fine_forward": [float(value) for value in continuation["fine_forward"]],
    }
    path_structure_exact = True
    preenumerated_path_slots: dict[str, list[dict[str, Any]]] = {}
    for key, records in paths.items():
        expected_lambdas = expected_path_lambdas[key]
        observed_lambdas = [float(record["lambda"]) for record in records]
        if (
            len(records) > len(expected_lambdas)
            or observed_lambdas != expected_lambdas[: len(observed_lambdas)]
        ):
            raise InvalidRun(f"semantic path slot reorder/extra drift: {key}")
        path_object = (
            engine["independent_phi_minus_reflection"]["fine_forward"]
            if key == "phi_minus_fine_forward"
            else engine["primary_phi_plus"][
                {
                    "phi_plus_fine_forward": "fine_forward",
                    "phi_plus_coarse_forward": "coarse_forward",
                    "phi_plus_fine_reverse": "fine_reverse",
                }[key]
            ]
        )
        if [float(value) for value in path_object["requested_lambdas"]] != expected_lambdas:
            raise InvalidRun(f"semantic requested path mesh drift: {key}")
        slots: list[dict[str, Any]] = []
        by_lambda = {float(record["lambda"]): record for record in records}
        attempted_node_count = int(path_object.get("attempted_node_count", 0))
        for index, lambda_value in enumerate(expected_lambdas):
            record = by_lambda.get(lambda_value)
            executed = bool(record is not None and index < attempted_node_count)
            slots.append(
                {
                    "lambda": lambda_value,
                    "executed": executed,
                    "accepted": bool(
                        executed and record and record.get("accepted", False)
                    ),
                    "status": (
                        record.get("status", "PASS" if record.get("accepted") else "INCONCLUSIVE")
                        if executed and record is not None
                        else "INCONCLUSIVE_NOT_EXECUTED_AFTER_TERMINATION"
                    ),
                }
            )
        preenumerated_path_slots[key] = slots
        path_structure_exact = bool(
            path_structure_exact
            and len(records) == int(expected_paths[key])
        )

    outer_records = engine["outer_lambda_tangent_control"].get("records", [])
    if len(outer_records) > int(
        expected["outer_lambda_tangent_records"]["record_count"]
    ):
        raise InvalidRun("outer-tangent extra record topology drift")
    expected_outer_steps = [
        float(value)
        for value in preflight.bundle.p51_manifest["controls"]["path_tangent"][
            "steps"
        ]
    ]
    if [float(record["step"]) for record in outer_records] != expected_outer_steps[:len(outer_records)]:
        raise InvalidRun("outer-tangent step/order drift")
    outer_roots = [
        record[key]
        for record in outer_records
        for key in ("plus_root_record", "minus_root_record")
    ]
    endpoint_records = list(engine["endpoint_mutations"].values())
    if len(endpoint_records) != int(expected["endpoint_mutations"]["record_count"]):
        raise InvalidRun("endpoint-mutation record topology drift")
    semantic_roots = [
        record for records in paths.values() for record in records
    ] + outer_roots + endpoint_records
    root_attempts = len(semantic_roots)
    root_accepted = sum(
        bool(record.get("accepted", False)) for record in semantic_roots
    )
    if root_attempts > int(expected["accepted_semantic_root_total"]):
        raise InvalidRun("extra semantic root attempt topology drift")

    saddle_records = [
        record
        for source in SOURCE_ORDER
        for record in engine["saddle_reproduction"][source].values()
    ]
    saddle_attempts = len(saddle_records)
    saddle_accepted = sum(
        bool(record and record.get("accepted", False)) for record in saddle_records
    )
    expected_saddles = expected["saddle_records"]
    unique_saddles = preflight.factory.execution.unique_saddle_solves
    if saddle_attempts > int(expected_saddles["attempt_count"]) or len(
        unique_saddles
    ) > int(
        expected_saddles[
            "unique_saddle_solves_including_four_outer_tangent_off_mesh_values"
        ]
    ):
        raise InvalidRun("extra saddle execution topology drift")

    path_ledgers = [
        ledger
        for label in (
            "phi_plus:fine",
            "phi_plus:coarse",
            "phi_plus:reverse",
            "phi_minus:fine",
            "endpoint_controls",
        )
        for ledger in engine["flow_ledgers"][label].values()
    ]
    outer_ledgers = [
        record[key]
        for record in outer_records
        for key in ("plus_flow_ledger", "minus_flow_ledger")
    ]
    ledgers = path_ledgers + outer_ledgers
    ledger_expected = expected["action_and_first_cap_ledgers"]
    ledger_valid = all(
        ledger.get("sample_count") == int(ledger_expected["samples_per_ledger"])
        and ledger.get("first_cap_event_status")
        == ledger_expected["required_event_status"]
        and ledger.get("status") == ledger_expected["required_check_status"]
        and ledger.get("passed") is True
        and _all_numeric_leaves_finite(ledger)
        for ledger in ledgers
    )
    if len(ledgers) > int(ledger_expected["total"]):
        raise InvalidRun("extra action/first-cap ledger topology drift")

    evaluator_pairs = engine["evaluator_validation"][
        "same_point_source_lambda_pairs"
    ]
    evaluator_pair_count = sum(
        len(value["records"]) for value in evaluator_pairs.values()
    )
    trajectories = engine["evaluator_validation"][
        "phi_plus_solved_trajectory_reintegrations"
    ]
    trajectory_fraction_count = sum(
        len(value.get("points", [])) for value in trajectories.values()
    )
    if evaluator_pair_count != int(
        expected["evaluator_same_point_records"]["total"]
    ) or trajectory_fraction_count != int(
        expected["trajectory_reintegrations"]["total_fraction_records"]
    ):
        raise InvalidRun("evaluator pair/trajectory slot topology drift")
    paired_integrations = [
        value[key]
        for value in trajectories.values()
        for key in ("CSE_integration", "nonCSE_integration")
        if key in value
    ]

    finite_difference = engine["finite_difference_controls"]
    fd_column_records = sum(
        sum(len(column["steps"]) for column in value.get("per_column", []))
        for value in finite_difference.values()
    )
    execution = preflight.factory.execution
    fd_expected = expected["full_J_finite_difference_controls"]
    fd_spec = preflight.bundle.p51_manifest["controls"]["full_J_FD"]
    fd_keys = [f"lambda={float(value):.1f}" for value in fd_spec["lambdas"]]
    if list(finite_difference) != fd_keys[: len(finite_difference)]:
        raise InvalidRun("full-J lambda slot/order drift")
    gamma_steps = [float(value) for value in fd_spec["steps"]["Gamma_y_and_psi"]]
    k_steps = [
        float(value)
        for value in fd_spec["steps"][
            "K_old_u1_through_u6_and_added_u"
        ]
    ]
    time_steps = [float(value) for value in fd_spec["steps"]["K_flow_time"]]
    fd_columns_exact = all(
        len(control.get("per_column", [])) == 18
        and [int(column["column"]) for column in control.get("per_column", [])]
        == list(range(18))
        and all(
            [float(value) for value in column["steps"]]
            == (gamma_steps if index <= 8 else k_steps if index <= 16 else time_steps)
            for index, column in enumerate(control.get("per_column", []))
        )
        for control in finite_difference.values()
    )
    fd_columns_structural = all(
        [int(column["column"]) for column in control.get("per_column", [])]
        == list(range(len(control.get("per_column", []))))
        and all(
            [float(value) for value in column["steps"]]
            == (gamma_steps if index <= 8 else k_steps if index <= 16 else time_steps)
            for index, column in enumerate(control.get("per_column", []))
        )
        for control in finite_difference.values()
    )
    if not fd_columns_structural:
        raise InvalidRun("full-J column index/step/order structural drift")
    cache_backend_exact = bool(
        len(execution.cache_backend_keys) == 1
        and {backend for _identity, backend in execution.cache_backend_keys}
        == {"phase53_element_local_production"}
        and {identity for identity, _backend in execution.cache_backend_keys}
        == {id(preflight.factory.evaluators["phi_plus"])}
        and execution.cache_key_schema_check_count
        == int(fd_expected["state_only_residual_calls_total"])
        and execution.cache_key_schema_all_valid
        and preflight.factory.cache_key_source_guard
    )
    fd_topology = bool(
        len(finite_difference) == int(fd_expected["lambda_count"])
        and fd_column_records == int(fd_expected["total_column_step_records"])
        and execution.fd_residual_calls
        == int(fd_expected["state_only_residual_calls_total"])
        and execution.fd_cache_misses
        == int(fd_expected["actual_state_integrations_total"])
        and execution.fd_cache_hits == int(fd_expected["K_cache_hits_total"])
        and len(execution.fd_integrations)
        == int(fd_expected["actual_state_integrations_total"])
        and fd_columns_exact
        and cache_backend_exact
    )
    if (
        len(finite_difference) > int(fd_expected["lambda_count"])
        or fd_column_records > int(fd_expected["total_column_step_records"])
        or execution.fd_residual_calls
        > int(fd_expected["state_only_residual_calls_total"])
        or execution.fd_cache_misses
        > int(fd_expected["actual_state_integrations_total"])
        or execution.fd_cache_hits > int(fd_expected["K_cache_hits_total"])
    ):
        raise InvalidRun("extra full-J execution topology drift")

    action_integrations = execution.flow_action_integrations
    event_integrations = execution.flow_event_integrations
    outer_integrations = execution.outer_partial_integrations
    base_integrations = (
        action_integrations
        + event_integrations
        + paired_integrations
        + outer_integrations
    )
    base_expected = expected["DOP853_records"]
    composition = base_expected["composition"]
    composition_counts = {
        "action_trajectory_integrations": len(action_integrations),
        "first_cap_event_integrations": len(event_integrations),
        "paired_production_and_control_trajectory_integrations": len(
            paired_integrations
        ),
        "outer_tangent_plus_minus_state_integrations": len(outer_integrations),
    }
    if len(base_integrations) > int(base_expected["required_record_count"]) or any(
        composition_counts[key] > int(composition[key])
        for key in composition_counts
    ):
        raise InvalidRun(f"extra retained DOP853 topology drift: {composition_counts}")
    base_solver_steps = sum(
        int(record["solver_steps"]) for record in base_integrations
    )
    historical_steps = int(base_expected["historical_phase51_solver_steps_sum"])
    fallback_source = preflight.factory.fallback_source_guard
    expected_root_evaluator_ids = {
        id(preflight.factory.evaluators[source]) for source in SOURCE_ORDER
    }
    path_label_prefixes = {
        "phi_plus_fine_forward": "phi_plus:fine",
        "phi_plus_coarse_forward": "phi_plus:coarse",
        "phi_plus_fine_reverse": "phi_plus:reverse",
        "phi_minus_fine_forward": "phi_minus:fine",
    }
    declared_root_labels = {
        f"{path_label_prefixes[key]}:lambda={lambda_value:.12g}"
        for key, lambdas in expected_path_lambdas.items()
        for lambda_value in lambdas
    }
    declared_root_labels.update(
        f"outer-{direction}-h={step:.3g}"
        for step in expected_outer_steps
        for direction in ("plus", "minus")
    )
    endpoint_spec = preflight.bundle.p51_manifest["controls"]["endpoint"]
    launch_radius = float(
        preflight.bundle.p51_manifest["launch_chart"]["launch_radius"]
    )
    declared_root_labels.update(
        f"endpoint-radius-{float(radius) / launch_radius:g}"
        for radius in endpoint_spec["radius_controls"]
    )
    declared_root_labels.update(
        f"endpoint-shape-lambda_{float(shape):g}"
        for shape in endpoint_spec["shape_controls"]
    )
    runtime_root_labels = [
        str(record["label"]) for record in execution.solve_root_records
    ]
    accepted_semantic_labels = {
        str(record["label"])
        for record in semantic_roots
        if record.get("accepted", False) and "label" in record
    }
    copied_root_evidence = bool(
        len(declared_root_labels)
        == int(expected["accepted_semantic_root_total"])
        and len(runtime_root_labels) == len(set(runtime_root_labels))
        and set(runtime_root_labels).issubset(declared_root_labels)
        and accepted_semantic_labels.issubset(set(runtime_root_labels))
        and all(
            record["production_evaluator_identity"]
            in expected_root_evaluator_ids
            for record in execution.solve_root_records
        )
    )
    no_fallback_conditions = {
        "historical_result_reuse": bool(
            fallback_source["historical_Phase51_result_not_loaded_by_runner"]
        ),
        "copied_roots": copied_root_evidence,
        "random_restarts": bool(fallback_source["random_API_absent"]),
        "reflected_seed_substitutions": bool(
            fallback_source["independent_phi_minus_continuation_present"]
        ),
        "mesh_insertions": bool(
            all(
                len(slots) == len(expected_path_lambdas[key])
                for key, slots in preenumerated_path_slots.items()
            )
        ),
        "chart_recentering": bool(
            fallback_source["chart_recentering_API_absent"]
        ),
        "clipping": bool(fallback_source["array_clipping_absent"]),
        "favorable_step_or_solver_replacement": bool(
            fd_columns_structural
            and [float(record["step"]) for record in outer_records]
            == expected_outer_steps[:len(outer_records)]
            and all(
                record.get("solver_method") == "DOP853"
                for record in base_integrations + execution.fd_integrations
            )
        ),
        "validation_backend_used_for_production": bool(
            all(
                scope == "validation_trajectory"
                for scope in execution.plain_backend_integration_scopes
            )
        ),
    }
    if set(no_fallback_conditions) != set(expected["no_fallback_ledger"]):
        raise InvalidRun("no-fallback evidence slot drift")
    no_fallback = {
        key: 0 if condition else 1
        for key, condition in no_fallback_conditions.items()
    }
    if any(no_fallback.values()):
        raise InvalidRun(f"a prohibited fallback was observed: {no_fallback}")
    return {
        "passed": bool(
            saddle_accepted == int(expected_saddles["accepted_count"])
            and root_accepted == int(expected["accepted_semantic_root_total"])
            and ledger_valid
            and path_structure_exact
            and len(unique_saddles)
            == int(
                expected_saddles[
                    "unique_saddle_solves_including_four_outer_tangent_off_mesh_values"
                ]
            )
            and len(base_integrations) == int(base_expected["required_record_count"])
            and fd_topology
        ),
        "saddles": {
            "attempt_count": saddle_attempts,
            "accepted_count": saddle_accepted,
            "unique_saddle_solve_count": len(unique_saddles),
            "unique_records": unique_saddles,
        },
        "semantic_roots": {
            "path_counts": path_counts,
            "preenumerated_path_slots": preenumerated_path_slots,
            "attempt_count": root_attempts,
            "accepted_count": root_accepted,
        },
        "action_and_first_cap_ledgers": {
            "count": len(ledgers),
            "all_passed_finite_first_cap_101": ledger_valid,
        },
        "evaluator_same_point_record_count": evaluator_pair_count,
        "trajectory_fraction_record_count": trajectory_fraction_count,
        "full_J": {
            "column_step_record_count": fd_column_records,
            **execution.summary(),
        },
        "retained_nonroot_nonFD_DOP853": {
            "count": len(base_integrations),
            "composition": composition_counts,
            "solver_steps_sum": base_solver_steps,
            "historical_Phase51_solver_steps_sum_descriptive_only": historical_steps,
            "solver_steps_difference_descriptive_only": base_solver_steps
            - historical_steps,
            "records": base_integrations,
        },
        "data_dependent_root_solver_integrate_k_invocation_count": (
            execution.integrate_invocation_count
            - len(execution.fd_integrations)
            - len(base_integrations)
        ),
        "no_fallback_ledger": no_fallback,
        "no_fallback_evidence": {
            "conditions": no_fallback_conditions,
            "pinned_source_guards": fallback_source,
            "declared_root_label_count": len(declared_root_labels),
            "declared_root_labels_sha256": hashlib.sha256(
                json.dumps(
                    sorted(declared_root_labels),
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
            "runtime_root_labels": runtime_root_labels,
            "runtime_root_labels_unique": len(runtime_root_labels)
            == len(set(runtime_root_labels)),
            "runtime_root_labels_have_no_extra": set(
                runtime_root_labels
            ).issubset(declared_root_labels),
            "accepted_semantic_labels": sorted(accepted_semantic_labels),
            "accepted_semantic_labels_all_executed": (
                accepted_semantic_labels.issubset(set(runtime_root_labels))
            ),
            "solve_root_records": execution.solve_root_records,
            "plain_backend_integration_scopes": execution.plain_backend_integration_scopes,
        },
    }


def _historical_array(value: Any, *, label: str) -> np.ndarray:
    if isinstance(value, Mapping) and "complex128_pairs" in value:
        shape = tuple(int(item) for item in value["shape"])
        pairs = np.asarray(value["complex128_pairs"], dtype=float)
        if pairs.shape != (int(np.prod(shape)), 2):
            raise InvalidRun(f"historical complex array shape drift: {label}")
        output = (pairs[:, 0] + 1.0j * pairs[:, 1]).reshape(shape)
    else:
        output = np.asarray(value)
    if not np.all(np.isfinite(output)):
        raise InvalidRun(f"nonfinite historical comparison array: {label}")
    return output


def historical_semantic_comparison(
    preflight: Preflight, engine: Mapping[str, Any]
) -> dict[str, Any]:
    historical = preflight.bundle.p51_result
    path_specs = (
        (
            "phi_plus:fine_forward",
            engine["primary_phi_plus"]["fine_forward"],
            historical["primary_phi_plus"]["fine_forward"],
            "phi_plus",
        ),
        (
            "phi_plus:coarse_forward",
            engine["primary_phi_plus"]["coarse_forward"],
            historical["primary_phi_plus"]["coarse_forward"],
            "phi_plus",
        ),
        (
            "phi_plus:fine_reverse",
            engine["primary_phi_plus"]["fine_reverse"],
            historical["primary_phi_plus"]["fine_reverse"],
            "phi_plus",
        ),
        (
            "phi_minus:fine_forward",
            engine["independent_phi_minus_reflection"]["fine_forward"],
            historical["independent_phi_minus_reflection"]["fine_forward"],
            "phi_minus",
        ),
    )
    context_by_source = {
        context.label: context for context in preflight.contexts
    }
    path_records: dict[str, Any] = {}
    maximum_state = 0.0
    maximum_parameters = 0.0
    topology_exact = True
    orientation_exact = True
    for label, current_path, old_path, source_label in path_specs:
        current_records = current_path["records"]
        old_records = old_path["records"]
        if len(current_records) != len(old_records):
            raise InvalidRun(f"historical path length drift: {label}")
        records: list[dict[str, Any]] = []
        scales = np.asarray(
            context_by_source[source_label].scales5, dtype=float
        )
        for index, (current, old) in enumerate(
            zip(current_records, old_records, strict=True)
        ):
            lambda_exact = float(current["lambda"]) == float(old["lambda"])
            accepted_exact = bool(current.get("accepted")) == bool(
                old.get("accepted")
            )
            topology_exact = bool(topology_exact and lambda_exact and accepted_exact)
            if not current.get("accepted", False) or not old.get(
                "accepted", False
            ):
                records.append(
                    {
                        "lambda": float(current.get("lambda", old["lambda"])),
                        "lambda_and_acceptance_exact": lambda_exact
                        and accepted_exact,
                        "normalized_state_distance": None,
                        "parameter_distance": None,
                        "orientation_signs_exact": None,
                        "comparison_status": "INCONCLUSIVE_RECORD_RETAINED",
                    }
                )
                continue
            current_state = np.asarray(
                current["intersection_z"], dtype=np.complex128
            )
            old_state = _historical_array(
                old["intersection_z"], label=f"{label}[{index}].state"
            ).astype(np.complex128)
            state_distance = float(
                np.linalg.norm(
                    preflight.p51.interleaved(
                        (current_state - old_state) / scales
                    )
                )
            )
            current_parameters = np.asarray(current["parameters"], dtype=float)
            old_parameters = np.asarray(old["parameters"], dtype=float)
            parameter_distance = float(
                np.linalg.norm(current_parameters - old_parameters)
            )
            current_signs = (
                current["direct_orientation"]["sign"],
                current["root_jacobian_orientation"]["sign"],
            )
            old_signs = (
                old["direct_orientation"]["sign"],
                old["root_jacobian_orientation"]["sign"],
            )
            signs_exact = current_signs == old_signs
            orientation_exact = bool(orientation_exact and signs_exact)
            maximum_state = max(maximum_state, state_distance)
            maximum_parameters = max(maximum_parameters, parameter_distance)
            records.append(
                {
                    "lambda": float(current["lambda"]),
                    "lambda_and_acceptance_exact": lambda_exact
                    and accepted_exact,
                    "normalized_state_distance": state_distance,
                    "parameter_distance": parameter_distance,
                    "orientation_signs_exact": signs_exact,
                }
            )
        path_records[label] = records
    current_checks = {
        record["id"]: bool(record["passed"])
        for record in engine["numerical_checks"]
    }
    historical_checks = {
        record["id"]: bool(record["passed"])
        for record in historical["numerical_checks"]
    }
    return {
        "historical_Phase51_classification": historical["classification"],
        "replayed_inner_Phase51_classification": engine["classification"],
        "path_topology_and_acceptance_exact": topology_exact,
        "orientation_signs_exact": orientation_exact,
        "maximum_normalized_path_state_distance": maximum_state,
        "maximum_path_parameter_distance": maximum_parameters,
        "paths": path_records,
        "Phase51_numerical_check_status_comparison": {
            check_id: {
                "historical_passed": historical_checks[check_id],
                "replayed_passed": current_checks[check_id],
                "changed": historical_checks[check_id]
                != current_checks[check_id],
            }
            for check_id in P51_NUMERICAL_IDS
        },
        "interpretation": (
            "descriptive comparison only: Phase51 is immutable and its raw "
            "dtype protocol remains NOT_UPHELD; Phase53 is a separate replay"
        ),
    }


def run_calculation() -> dict[str, Any]:
    progress("validating authoritative commit/blob/runtime prerequisites")
    bundle = validate_inputs(authoritative=True)
    progress("constructing and auditing the complete repaired evaluator")
    preflight = build_preflight(bundle)
    symbolic = exact_evaluator_audit(preflight)
    null_guard = local_null_guard(bundle.manifest)

    # Discard only validation-slot saddle caches: p51.run constructs fresh
    # SourceContext objects and executes its complete immutable semantics.
    progress("replaying the complete pinned Phase51 continuation semantics")
    engine = preflight.p51.run()
    if engine.get("run_status") != "VALID_RUN":
        raise InvalidRun("wrapped Phase51 engine did not complete a valid replay")
    preflight.p51.verify_self_digest(engine, label="Phase53 wrapped Phase51 engine")
    engine_original_self_digest = engine[
        "result_payload_sha256_without_self"
    ]

    authoritative_slots = preflight.factory.execution.authoritative_reference_slots
    if (
        len(authoritative_slots) != 6
        or [slot.source_label for slot in authoritative_slots]
        != [source for source in SOURCE_ORDER for _ in LAMBDA_ORDER]
        or [float(slot.lambda_value) for slot in authoritative_slots]
        != list(LAMBDA_ORDER) * len(SOURCE_ORDER)
    ):
        raise InvalidRun("authoritative Phase51 evaluator slot capture drift")
    progress("raw-tracing the six actual repaired Phase51 evaluator slots")
    dtype = dtype_audit(preflight, authoritative_slots)
    progress("running independent six-slot 80/120-decimal reference")
    reference = six_slot_reference_audit(preflight, authoritative_slots)

    topology = execution_topology_audit(preflight, engine)
    historical_comparison = historical_semantic_comparison(preflight, engine)
    binding = preflight.factory.binding_summary()
    calls = preflight.factory.call_summary()
    convention = preflight.factory.convention_source_guard
    cache_guard = preflight.factory.cache_summary()
    fixed_binding = fixed_order_and_binding_audit(
        preflight, calls, binding
    )

    inheritance = require(
        bundle.manifest,
        "phase51_contract_inheritance",
        where="manifest",
    )
    semantic_replay = require(
        inheritance, "semantic_replay", where="phase51_contract_inheritance"
    )
    expected_inner_exact = list(
        require(
            semantic_replay,
            "required_phase51_exact_check_ids",
            where="phase51_contract_inheritance.semantic_replay",
        )
    )
    expected_inner_numerical = list(
        require(
            semantic_replay,
            "required_phase51_numerical_check_ids",
            where="phase51_contract_inheritance.semantic_replay",
        )
    )
    if [record["id"] for record in engine["exact_checks"]] != expected_inner_exact:
        raise InvalidRun("wrapped Phase51 exact semantic slots drifted")
    if [record["id"] for record in engine["numerical_checks"]] != expected_inner_numerical:
        raise InvalidRun("wrapped Phase51 numerical semantic slots drifted")
    inner_exact_pass = all(
        bool(record["passed"]) for record in engine["exact_checks"]
    ) and all(
        bool(record["passed"])
        for record in engine["internal_validation_subchecks"]["exact"]
    )
    if not inner_exact_pass:
        raise InvalidRun("an inherited Phase51 exact/internal prerequisite failed")

    contract = Contract()
    contract.add_exact(
        EXACT_CHECK_IDS[0],
        bool(
            len(bundle.observed)
            >= int(bundle.manifest["pin_validation"]["flattened_pin_count"])
            and bundle.runner_guard["manifest_commit_blob_guard"][
                "commit_blob_matches"
            ]
        ),
        "all frozen bytes, self-digests, named commits, and working/commit blobs agree",
        {
            "manifest_commit": INPUT_COMMIT,
            "flattened_pin_count": bundle.manifest["pin_validation"][
                "flattened_pin_count"
            ],
            "runner_guard": bundle.runner_guard,
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[1],
        bool(
            inner_exact_pass
            and inheritance["only_permitted_overlay"]["no_other_override"]
            and [record["id"] for record in engine["numerical_checks"]]
            == list(P51_NUMERICAL_IDS)
        ),
        "the complete Phase51 semantic contract is inherited with only the evaluator overlay",
        {
            "inner_exact_checks": engine["exact_checks"],
            "overlay": inheritance["only_permitted_overlay"],
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[2],
        bool(
            symbolic[
                "all_action_gradient_hessian_element_and_derivative_identities"
            ]
        ),
        "exact-decimal element sums equal action/gradient/Hessian, derivatives agree, and Hessians are symmetric",
        {"identities": symbolic["exact_identities"]},
    )
    contract.add_exact(
        EXACT_CHECK_IDS[3],
        bool(symbolic["projection_exact_reuse_passed"]),
        "the production element-gradient plans exactly reuse the Phase52 projection and fingerprint",
        {
            "Phase52_projection_sha256": symbolic[
                "Phase52_projection_sha256"
            ],
            "Phase53_projection_sha256": symbolic[
                "Phase53_generated_projection_sha256"
            ],
            "canonical_bytes": symbolic["projection_canonical_bytes"],
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[4],
        bool(
            symbolic["action_hessian_CSE_back_substitution_passed"]
            and symbolic["all_three_plan_families_back_substitute"]
        ),
        "every separate element action and Hessian CSE plan back-substitutes exactly",
    )
    contract.add_exact(
        EXACT_CHECK_IDS[5],
        bool(
            dtype["all_traces_complete_and_exact_clongdouble"]
            and dtype["audited_callable_objects_are_production_bound"]
        ),
        "all raw generated temporaries and outputs are exact np.clongdouble at all six slots",
        {
            "slot_count": dtype["slot_count"],
            "trace_record_count": dtype["trace_record_count"],
        },
    )
    fixed_and_bound = bool(
        all(
            value
            for key, value in convention.items()
            if key not in (
                "pinned_integrate_k_source_sha256",
                "pinned_Node_rhs_long_source_sha256",
            )
        )
        and fixed_binding["passed"]
        and len(preflight.p51.CSE_EXACT_LEDGER) == 4
    )
    contract.add_exact(
        EXACT_CHECK_IDS[6],
        fixed_and_bound,
        "fixed-order complete evaluator consumers retain ordinary transpose, one outer conjugation, and one solver-boundary cast",
        {
            "convention_source_guard": convention,
            "callable_bindings": binding,
            "cache_guard": cache_guard,
            "fixed_order_and_binding_audit": fixed_binding,
        },
    )
    contract.add_exact(
        EXACT_CHECK_IDS[7],
        bool(null_guard["passed"]),
        "the local replay retains every global, physics, contradiction, cutoff, continuum, and TOE null boundary",
        null_guard,
    )

    contract.add_numerical(
        NUMERICAL_CHECK_IDS[0],
        bool(reference["all_slots_passed"]),
        "all six slots satisfy the frozen 80/120-decimal and production/full-reference thresholds",
        {
            "slot_count": reference["slot_count"],
            "thresholds": reference["thresholds"],
        },
    )
    inner_by_id = {
        record["id"]: record for record in engine["numerical_checks"]
    }
    for p53_id, p51_id in zip(
        NUMERICAL_CHECK_IDS[1:10], P51_NUMERICAL_IDS[:9], strict=True
    ):
        inner = inner_by_id[p51_id]
        statement = str(inner["statement"])
        if p51_id == "P51.evaluator.CSE_nonCSE_pairs":
            statement = (
                "the complete repaired action/gradient/Hessian evaluator agrees "
                "with the saved pinned Phase51 global non-CSE control at every "
                "paired point and trajectory fraction"
            )
        contract.add_numerical(
            p53_id,
            bool(inner["passed"]),
            statement,
            {"inherited_check_id": p51_id, "inner_status": inner["status"]},
        )
    guard_inner = inner_by_id[P51_NUMERICAL_IDS[9]]
    inner_internal_numerical_pass = all(
        bool(record["passed"])
        for record in engine["internal_validation_subchecks"]["numerical"]
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[10],
        bool(
            guard_inner["passed"]
            and topology["passed"]
            and null_guard["passed"]
            and inner_internal_numerical_pass
        ),
        "the full semantic replay has the exact frozen execution topology, no fallback, and local/global nulls",
        {
            "inherited_check_id": P51_NUMERICAL_IDS[9],
            "topology_passed": topology["passed"],
            "inner_internal_numerical_subchecks_passed": inner_internal_numerical_pass,
            "no_fallback_ledger": topology["no_fallback_ledger"],
        },
    )
    if [record["id"] for record in contract.exact] != list(EXACT_CHECK_IDS):
        raise InvalidRun("Phase53 exact output slot drift")
    if [record["id"] for record in contract.numerical] != list(
        NUMERICAL_CHECK_IDS
    ):
        raise InvalidRun("Phase53 numerical output slot drift")

    progress("rehashing every consumed byte before classification selection")
    rehash = post_rehash(bundle)
    all_numerical = all(record["passed"] for record in contract.numerical)
    classification_spec = bundle.manifest["classification"]
    classification = (
        classification_spec["supported"]["label"]
        if all_numerical
        else classification_spec["inconclusive"]["label"]
    )
    promoted_output = engine.get("promoted_output") if all_numerical else None
    if all_numerical and promoted_output is None:
        raise InvalidRun("supported replay lacks its scoped local candidate object")

    required_outputs = bundle.manifest["required_outputs"]
    global_keys = (
        "contradicted_output_allowed",
        "required_independent_contradiction_certificate",
        "straight_arm_intersections_searched",
        "cap_reintersections_searched",
        "continuous_direction_coverage_proved",
        "root_exhaustion_proved",
        "all_saddles_and_upward_components_complete",
        "non_Stokes_chamber_certified",
        "all_relative_good_ends_classified",
        "physical_original_cycle_derived",
        "common_determinant_line_constructed",
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "physics_claim",
        "TOE_claim",
    )
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 53,
        "run_status": "VALID_RUN",
        "classification": classification,
        "input_provenance": {
            "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "manifest_commit": INPUT_COMMIT,
            "manifest_sha256": INPUT_SHA256,
            "runner_path": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "runner_sha256": sha256_path(SCRIPT_PATH),
            "pinned_inputs": bundle.observed,
            "post_rehash": rehash,
        },
        "runtime": runtime_record(),
        "exact_checks": contract.exact,
        "numerical_checks": contract.numerical,
        "symbolic_evaluator_audit": symbolic,
        "raw_dtype_audit": dtype,
        "six_slot_full_evaluator_reference": reference,
        "complete_repaired_evaluator": {
            "call_counts": calls,
            "callable_bindings": binding,
            "builder_cache_guard": cache_guard,
            "convention_and_solver_boundary_guard": convention,
            "fixed_order_and_binding_audit": fixed_binding,
        },
        "execution_topology": topology,
        "historical_Phase51_semantic_comparison": historical_comparison,
        "wrapped_Phase51_semantic_replay": {
            "original_Phase51_serialization_self_digest_verified": True,
            "original_Phase51_serialization_self_digest": engine_original_self_digest,
            "embedded_payload_representation": (
                "Phase53 dtype-explicit JSON; nested Phase51 self field removed "
                "because this representation intentionally differs"
            ),
            "payload_without_original_self_field": {
                key: value
                for key, value in engine.items()
                if key != "result_payload_sha256_without_self"
            },
        },
        "promoted_output": promoted_output,
        "promoted_output_scope": (
            required_outputs["promoted_output_policy"]["scope"]
            if promoted_output is not None
            else None
        ),
        "global_promotion": required_outputs["global_promotion"],
        "gate1": required_outputs["gate1"],
        **{key: required_outputs[key] for key in global_keys},
        "computed_facts": (
            "One complete pinned Phase51 semantic replay and six fixed high-precision "
            "evaluator reference slots under one coherent repaired element-local evaluator."
        ),
        "interpretation": (
            "A passing result supports only the declared finite-dimensional local "
            "candidate on the frozen diagonal path."
        ),
        "open_physical_hypothesis": (
            "Global cycles, continuum/cutoff limits, physics, and TOE claims remain open/null."
        ),
        "historical_boundary": (
            "Phase51 remains immutable and its stronger raw dtype protocol is NOT_UPHELD; "
            "Phase53 does not rewrite or promote that historical raw result."
        ),
    }
    return with_self_digest(payload)


def local_null_guard(manifest: Mapping[str, Any]) -> dict[str, Any]:
    required = require(manifest, "required_outputs", where="manifest")
    null_keys = (
        "required_independent_contradiction_certificate",
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "physics_claim",
        "TOE_claim",
    )
    false_keys = (
        "contradicted_output_allowed",
        "straight_arm_intersections_searched",
        "cap_reintersections_searched",
        "continuous_direction_coverage_proved",
        "root_exhaustion_proved",
        "all_saddles_and_upward_components_complete",
        "non_Stokes_chamber_certified",
        "all_relative_good_ends_classified",
        "physical_original_cycle_derived",
        "common_determinant_line_constructed",
    )
    policy = require(
        required, "promoted_output_policy", where="required_outputs"
    )
    passed = bool(
        all(required.get(key) is None for key in null_keys)
        and all(required.get(key) is False for key in false_keys)
        and required.get("global_promotion") == "PROHIBITED"
        and required.get("gate1") == "OPEN_PARTIAL_PROGRESS"
        and policy.get("inconclusive") is None
        and policy.get("global_interpretation_allowed") is False
        and manifest["classification"].get(
            "contradicted_selectable_by_runner"
        )
        is False
    )
    return {
        "passed": passed,
        "null_keys": {key: required.get(key) for key in null_keys},
        "false_keys": {key: required.get(key) for key in false_keys},
        "global_promotion": required.get("global_promotion"),
        "gate1": required.get("gate1"),
        "promoted_output_policy": policy,
    }


def post_rehash(bundle: InputBundle) -> dict[str, Any]:
    records: dict[str, Any] = {}
    for label, start in bundle.observed.items():
        path = REPO_ROOT / str(start["path"])
        observed_sha = sha256_path(path)
        if observed_sha != start["sha256"]:
            raise InvalidRun(f"consumed input changed during run: {label}")
        records[label] = {
            "path": start["path"],
            "sha256_at_start": start["sha256"],
            "sha256_at_end": observed_sha,
            "unchanged": True,
        }
    manifest_sha = sha256_path(INPUT_PATH)
    runner_sha = sha256_path(SCRIPT_PATH)
    if manifest_sha != INPUT_SHA256:
        raise InvalidRun("Phase53 manifest changed during run")
    if runner_sha != bundle.runner_guard["runner_sha256_at_start"]:
        raise InvalidRun("Phase53 runner changed during run")
    return {
        "inputs": records,
        "manifest_sha256_at_end": manifest_sha,
        "runner_sha256_at_end": runner_sha,
        "all_consumed_bytes_unchanged": True,
    }


def validate_only_payload() -> dict[str, Any]:
    progress("validating manifest, pins, runtime, and thread environment")
    bundle = validate_inputs(authoritative=False)
    progress("constructing separate per-element action/gradient/Hessian plans")
    preflight = build_preflight(bundle)
    progress("checking exact identities and the Phase52 gradient projection")
    symbolic = exact_evaluator_audit(preflight)
    progress("tracing every raw temporary/output at all six frozen slots")
    dtype = dtype_audit(preflight)
    null_guard = local_null_guard(bundle.manifest)
    convention = preflight.factory.convention_source_guard
    prerequisite_status = {
        "symbolic_identities": symbolic[
            "all_action_gradient_hessian_element_and_derivative_identities"
        ],
        "Phase52_projection": symbolic["projection_exact_reuse_passed"],
        "action_hessian_back_substitution": symbolic[
            "action_hessian_CSE_back_substitution_passed"
        ],
        "raw_dtype": dtype["all_traces_complete_and_exact_clongdouble"],
        "production_object_binding": dtype[
            "audited_callable_objects_are_production_bound"
        ],
        "conventions": all(
            value
            for key, value in convention.items()
            if key not in (
                "pinned_integrate_k_source_sha256",
                "pinned_Node_rhs_long_source_sha256",
            )
        ),
        "null_guard": null_guard["passed"],
    }
    validation_pass = all(prerequisite_status.values())
    if not validation_pass:
        projection_debug = {
            "Phase52_projection_sha256": symbolic[
                "Phase52_projection_sha256"
            ],
            "Phase53_generated_projection_sha256": symbolic[
                "Phase53_generated_projection_sha256"
            ],
            "projection_canonical_bytes": symbolic[
                "projection_canonical_bytes"
            ],
            "gradient_entry_match_count": sum(
                bool(record["gradient_exact_Phase52_entry"])
                for source in SOURCE_ORDER
                for plan in (
                    preflight.factory.plans[source].m4,
                    preflight.factory.plans[source].m5,
                )
                for record in plan.ledger
            ),
            "gradient_entry_total": sum(
                len(plan.ledger)
                for source in SOURCE_ORDER
                for plan in (
                    preflight.factory.plans[source].m4,
                    preflight.factory.plans[source].m5,
                )
            ),
        }
        raise InvalidRun(
            "Phase53 validate-only prerequisite conjunction failed: "
            + json.dumps(
                {
                    "prerequisites": prerequisite_status,
                    "projection": projection_debug,
                    "conventions": convention,
                },
                sort_keys=True,
            )
        )
    rehash = post_rehash(bundle)
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 53,
        "run_status": "VALIDATION_ONLY",
        "classification": None,
        "evidence_role": "implementation validation only; no scientific replay",
        "input_provenance": {
            "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
            "manifest_commit": INPUT_COMMIT,
            "manifest_sha256": INPUT_SHA256,
            "runner_path": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "runner_sha256": sha256_path(SCRIPT_PATH),
            "pinned_inputs": bundle.observed,
            "post_rehash": rehash,
        },
        "runtime": runtime_record(),
        "source_lambda_slots": [
            {
                "key": slot.key,
                "source": slot.source_label,
                "lambda": float(slot.lambda_value),
                "point": preflight.slot_origin,
            }
            for slot in preflight.slots
        ],
        "symbolic_evaluator_audit": symbolic,
        "raw_dtype_audit": dtype,
        "convention_and_solver_boundary_guard": convention,
        "callable_binding_guard": preflight.factory.binding_summary(),
        "builder_cache_guard": preflight.factory.cache_summary(),
        "local_global_physics_TOE_null_guard": null_guard,
        "phase51_context_input_validation": preflight.context_validation,
        "prerequisite_status": prerequisite_status,
        "validate_only_forbidden_work": {
            "saddle_solves": 0,
            "root_solves": 0,
            "ODE_integrations": 0,
            "continuations": 0,
            "endpoint_mutations": 0,
            "finite_difference_controls": 0,
            "classification_selected": False,
            "canonical_result_written": False,
        },
    }
    return with_self_digest(payload)


def invalid_payload(error: BaseException) -> dict[str, Any]:
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 53,
        "run_status": "INVALID_RUN",
        "classification": "INVALID_RUN",
        "error_type": type(error).__name__,
        "error": str(error),
        "failure_boundary": (
            "A failure before the pinned Phase51 engine returns a valid complete "
            "semantic replay is INVALID_RUN. Numerical failures captured inside "
            "that completed replay remain retained INCONCLUSIVE records; no pinned "
            "or terminal saddle substitution is permitted."
        ),
        "traceback": traceback.format_exc(),
        "manifest_path": str(INPUT_PATH.relative_to(REPO_ROOT)),
        "manifest_commit": INPUT_COMMIT,
        "manifest_sha256_expected": INPUT_SHA256,
        "runner_sha256": sha256_path(SCRIPT_PATH),
    }
    return with_self_digest(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="construct and audit the evaluator without scientific numerical work",
    )
    arguments = parser.parse_args()
    try:
        payload = (
            validate_only_payload()
            if arguments.validate_only
            else run_calculation()
        )
        exit_code = 0
    except Exception as error:  # noqa: BLE001 - strict single-record failure channel
        payload = invalid_payload(error)
        exit_code = 2
    print(
        RESULT_PREFIX
        + json.dumps(
            json_ready(payload),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ),
        flush=True,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
