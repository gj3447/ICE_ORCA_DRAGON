#!/usr/bin/env python3
"""Phase 56: lambda-half launch provenance and residual conditioning.

The runner imports the pinned Phase-55 validator/evaluator machinery, performs
one Phase-53-algorithm saddle solve at the saved ``phi_plus`` lambda=0.5 root,
and evaluates the frozen 2 x 2 center/launch factorial under two DOP853
profiles.  It never solves or replays a Gamma--K root or continuation.

Progress goes to stderr.  Exactly one strict ``RESULT_JSON=...`` record goes
to stdout.  The runner itself writes no repository files.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass, field
from decimal import Decimal
import hashlib
import importlib.util
import inspect
import json
import math
import os
from pathlib import Path
import scipy.integrate
import scipy.optimize
import sys
import traceback
from types import ModuleType, SimpleNamespace
from typing import Any, Callable, Iterable, Mapping, Sequence

sys.dont_write_bytecode = True

import numpy as np


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_INPUTS.json"
)
P55_RUNNER_PATH = SCRIPT_PATH.with_name(
    "phase55_p53_root_fixed_launch_schedule_transfer.py"
)

MANIFEST_COMMIT = "24b2d6d7f207941e782dfe9ceae08af6b2d2d24b"
MANIFEST_BLOB_OID = "0024f4e0fcdd0718c7bdc813412b348edd0589a6"
MANIFEST_SHA256 = "94c2d0074e0d2a36f3ecb5d99e437ef2915948bbd059154f10098a890f30fb7c"
MANIFEST_SIZE_BYTES = 28688
RESULT_SCHEMA = "ice-phase56-lambda-half-launch-provenance-residual-conditioning/v1"
RESULT_PREFIX = "RESULT_JSON="

SOURCE = "phi_plus"
LAMBDA_VALUE = 0.5
CENTER_ORDER = ("P50", "fresh")
LAUNCH_ORDER = ("P50", "fresh")
CORNER_ORDER = (
    "P50_center__P50_launch",
    "P50_center__fresh_launch",
    "fresh_center__P50_launch",
    "fresh_center__fresh_launch",
)
PROFILE_ORDER = ("primary", "refined_diagnostic")
FRACTION_ORDER = (0.0, 0.25, 0.5, 0.75, 1.0)
COORDINATE_LABELS = (
    "a1", "phi1", "a2", "phi2", "a3", "phi3", "a4", "phi4", "T"
)
EXACT_CHECK_IDS = (
    "P56.inputs.recursive_pins_commits_blobs_self_digests_and_runner_binding",
    "P56.target.single_phi_plus_lambda_half_root_saddle_endpoint_and_baseline_subtrees",
    "P56.algorithm.one_fresh_saddle_solve_and_zero_other_root_or_replay_calls",
    "P56.launch.two_centers_two_launches_and_exact_2x2_corner_construction",
    "P56.ODE.eight_profile_corner_attempts_five_fraction_slots_and_placeholders",
    "P56.conventions.EL_long_fixed_sum_ordinary_transpose_single_outer_conjugation_and_solver_boundary",
    "P56.residual.full_vector_identity_effect_definitions_and_T_component_index",
    "P56.guard.historical_immutability_classification_precedence_and_global_nulls",
)
NUMERICAL_CHECK_IDS = (
    "P56.saddle.fresh_Phase53_algorithm_and_launch_validity",
    "P56.newton.static_prediction_linear_identity_and_finite_comparison",
    "P56.baseline.primary_P50_P50_reproduces_Phase55",
    "P56.ODE.eight_attempt_completion_finiteness_callback_counts_and_xi_norm",
    "P56.gates.all_corner_profile_endpoint_and_residual_ledgers_complete",
    "P56.profile.all_corner_three_gate_vectors_stable",
    "P56.recovery.fresh_fresh_both_profiles_vs_saved_target",
    "P56.arithmetic.residual_identities_center_launch_interaction_and_T_conditioning",
)
CLASSIFICATION_PRECEDENCE = (
    "INVALID_RUN",
    "P56_FRESH_SADDLE_OR_LAUNCH_RECONSTRUCTION_NONPASS",
    "P56_PHASE55_P50_BASELINE_NOT_REPRODUCED",
    "P56_FACTORIAL_ODE_COMPLETION_OR_FLOW_NORM_NONPASS",
    "P56_LAMBDA_HALF_GATE_SOLVER_PROFILE_UNSTABLE",
    "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET",
    "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_DOES_NOT_RECOVER_SAVED_LAMBDA_HALF_TARGET",
)

ALLOWED_SOLVE_IVP = scipy.integrate.solve_ivp


class InvalidRun(RuntimeError):
    """A frozen byte, exact topology, convention, or finite-value gate failed."""


def progress(message: str) -> None:
    print(f"[Phase56] {message}", file=sys.stderr, flush=True)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_module(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise InvalidRun(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


P55 = load_module("ice_phase55_for_phase56", P55_RUNNER_PATH)


def require(mapping: Mapping[str, Any], key: str, *, where: str) -> Any:
    if key not in mapping:
        raise InvalidRun(f"missing {where}.{key}")
    return mapping[key]


def decimal(value: Any, *, label: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except Exception as error:
        raise InvalidRun(f"invalid decimal at {label}: {value!r}") from error
    if not result.is_finite():
        raise InvalidRun(f"nonfinite decimal at {label}")
    return result


def finite_array(value: Any, *, role: str) -> np.ndarray:
    try:
        return P55.require_finite_array(
            np.asarray(value), gate_id="P56.finite", role=role
        )
    except Exception as error:
        raise InvalidRun(str(error)) from error


def canonical_bytes(value: Any) -> bytes:
    return P55.canonical_bytes(value)


def git_output(*arguments: str) -> str:
    return P55.git_output(*arguments)


def pointer_get(payload: Any, pointer: str) -> Any:
    return P55.pointer_get(payload, pointer)


def decode_complex_record(value: Any, *, label: str) -> np.ndarray:
    if not isinstance(value, Mapping):
        return finite_array(np.asarray(value, dtype=np.clongdouble), role=label)
    shape = tuple(int(item) for item in require(value, "shape", where=label))
    if "clongdouble_decimal_pairs" in value:
        pairs = require(value, "clongdouble_decimal_pairs", where=label)
        if len(pairs) != math.prod(shape):
            raise InvalidRun(f"clongdouble pair count drift at {label}")
        output = np.asarray(
            [
                np.clongdouble(np.longdouble(str(real)))
                + np.clongdouble(1j) * np.clongdouble(np.longdouble(str(imaginary)))
                for real, imaginary in pairs
            ],
            dtype=np.clongdouble,
        ).reshape(shape)
    elif "numpy_complex_pairs" in value:
        pairs = np.asarray(value["numpy_complex_pairs"], dtype=float)
        if pairs.shape != (math.prod(shape), 2):
            raise InvalidRun(f"numpy pair shape drift at {label}")
        output = np.asarray(pairs[:, 0] + 1j * pairs[:, 1], dtype=np.clongdouble).reshape(shape)
    else:
        raise InvalidRun(f"unsupported complex record at {label}")
    return finite_array(output, role=label)


@dataclass
class Contract:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)

    def add_exact(
        self, check_id: str, passed: bool, statement: str, details: Any = None
    ) -> None:
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "exact",
            "passed": bool(passed),
            "status": "PASS" if passed else "FAIL",
            "statement": statement,
        }
        if details is not None:
            record["details"] = details
        self.exact.append(record)

    def add_numerical(
        self,
        check_id: str,
        status: str,
        statement: str,
        details: Any = None,
        causal_failure_ids: Sequence[str] = (),
        *,
        applicable: bool = True,
        evaluated: bool | None = None,
    ) -> None:
        if status not in ("PASS", "NONPASS", "NOT_EVALUATED"):
            raise InvalidRun(f"invalid numerical status: {status}")
        record: dict[str, Any] = {
            "id": check_id,
            "kind": "numerical",
            "passed": status == "PASS",
            "status": status,
            "applicable": bool(applicable),
            "evaluated": (
                status != "NOT_EVALUATED" if evaluated is None else bool(evaluated)
            ),
            "statement": statement,
        }
        if details is not None:
            record["details"] = details
        if causal_failure_ids:
            record["causal_failure_ids"] = list(causal_failure_ids)
        self.numerical.append(record)


@dataclass
class InputBundle:
    manifest: dict[str, Any]
    manifest_raw: bytes
    phase55_bundle: Any
    phase55_result: Mapping[str, Any]
    observed: Mapping[str, Any]
    expected_sha: Mapping[str, str]
    consumed_paths: tuple[Path, ...]
    runtime: Mapping[str, Any]
    runner_guard: Mapping[str, Any]


def validate_runtime(
    manifest: Mapping[str, Any], phase55_result: Mapping[str, Any]
) -> Mapping[str, Any]:
    observed = P55.runtime_record()
    required = manifest["phase55_baseline_contract"]["required_runtime_contract"]
    phase55_runtime = require(phase55_result, "runtime", where="Phase55 result")
    key_map = {
        "python_implementation": "python_implementation",
        "python_version": "python_version",
        "numpy_version": "numpy_version",
        "scipy_version": "scipy_version",
        "sympy_version": "sympy_version",
        "mpmath_version": "mpmath_version",
        "longdouble_itemsize_bytes": "longdouble_itemsize_bytes",
        "clongdouble_itemsize_bytes": "clongdouble_itemsize_bytes",
        "longdouble_mantissa_bits_excluding_implicit": "longdouble_mantissa_bits_excluding_implicit",
        "longdouble_epsilon": "longdouble_epsilon",
    }
    for required_key, observed_key in key_map.items():
        if str(observed.get(observed_key)) != str(required[required_key]):
            raise InvalidRun(f"runtime drift at {required_key}")
        if str(observed.get(observed_key)) != str(phase55_runtime.get(observed_key)):
            raise InvalidRun(f"runtime differs from Phase55 at {required_key}")
    required_threads = manifest["execution_environment"]["required_thread_environment"]
    thread_record = observed.get("thread_environment", {})
    for key, expected in required_threads.items():
        if os.environ.get(key) != expected or thread_record.get(key) != expected:
            raise InvalidRun(f"required thread environment drift: {key}")
    return observed


def validate_inputs(*, authoritative: bool) -> InputBundle:
    manifest, raw = P55.load_unique_json(INPUT_PATH)
    if len(raw) != MANIFEST_SIZE_BYTES or sha256_bytes(raw) != MANIFEST_SHA256:
        raise InvalidRun("Phase56 manifest byte identity drift")
    if (
        manifest.get("schema")
        != "ice-phase56-lambda-half-launch-provenance-residual-conditioning-inputs/v1"
        or manifest.get("phase") != 56
        or manifest.get("status") != "FROZEN_BEFORE_RUNNER_OR_ANY_PHASE56_OUTPUT"
    ):
        raise InvalidRun("Phase56 manifest schema/phase/status drift")
    checks = manifest["check_contract"]
    if tuple(checks["exact_check_ids"]) != EXACT_CHECK_IDS:
        raise InvalidRun("Phase56 exact check ID/order drift")
    if tuple(checks["numerical_check_ids"]) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("Phase56 numerical check ID/order drift")
    if tuple(manifest["classification_precedence"]) != CLASSIFICATION_PRECEDENCE:
        raise InvalidRun("Phase56 classification precedence drift")
    manifest_guard = P55.committed_blob_guard(
        str(INPUT_PATH.relative_to(REPO_ROOT)), MANIFEST_COMMIT
    )
    if (
        manifest_guard["working_blob_oid"] != MANIFEST_BLOB_OID
        or manifest_guard["committed_blob_oid"] != MANIFEST_BLOB_OID
    ):
        raise InvalidRun("Phase56 manifest commit/blob drift")

    direct = manifest["pinned_inputs"]
    if tuple(direct) != ("phase55_manifest", "phase55_runner", "phase55_result"):
        raise InvalidRun("Phase56 direct pin order drift")
    direct_records: dict[str, Any] = {}
    direct_paths: list[Path] = []
    direct_payloads: dict[str, Mapping[str, Any]] = {}
    for label, specification in direct.items():
        try:
            record, path, payload = P55.validate_declared_path(label, specification)
        except Exception as error:
            raise InvalidRun(str(error)) from error
        direct_records[str(path.relative_to(REPO_ROOT))] = record
        direct_paths.append(path)
        if payload is not None:
            direct_payloads[label] = payload
    phase55_result = direct_payloads["phase55_result"]
    phase55_spec = direct["phase55_result"]
    if (
        len(phase55_result.get("exact_checks", ()))
        != int(phase55_spec["required_exact_check_count"])
        or len(phase55_result.get("numerical_checks", ()))
        != int(phase55_spec["required_numerical_check_count"])
        or not all(item.get("status") == "PASS" for item in phase55_result["exact_checks"])
    ):
        raise InvalidRun("Phase55 result check topology drift")

    try:
        phase55_bundle = P55.validate_inputs(authoritative=False)
    except Exception as error:
        raise InvalidRun(f"transitive Phase55 validation failed: {error}") from error
    observed = dict(phase55_bundle.observed_pins)
    for relative, record in direct_records.items():
        if relative in observed and str(observed[relative]["sha256"]) != str(record["sha256"]):
            raise InvalidRun(f"recursive/direct declaration conflict: {relative}")
        observed[relative] = record
    if len(observed) != int(manifest["pin_validation"]["expected_unique_consumed_path_count_after_recursive_flattening"]):
        raise InvalidRun(f"Phase56 flattened pin count drift: {len(observed)}")
    expected_sha = {relative: str(record["sha256"]) for relative, record in observed.items()}
    path_map = {
        str(path.relative_to(REPO_ROOT)): path
        for path in (*phase55_bundle.consumed_paths, P55.INPUT_PATH, P55.SCRIPT_PATH, *direct_paths)
    }
    if set(path_map) != set(expected_sha):
        raise InvalidRun("Phase56 consumed path set drift")

    runtime = validate_runtime(manifest, phase55_result)
    runner_guard: dict[str, Any] = {
        "authoritative": authoritative,
        "manifest_commit": MANIFEST_COMMIT,
        "manifest_blob_oid": MANIFEST_BLOB_OID,
        "manifest_sha256": MANIFEST_SHA256,
        "manifest_commit_blob_guard": manifest_guard,
        "runner_sha256_at_start": sha256_path(SCRIPT_PATH),
        "runner_commit": None,
        "runner_clean": None,
        "manifest_is_ancestor": None,
    }
    if authoritative:
        relative = str(SCRIPT_PATH.relative_to(REPO_ROOT))
        dirty = git_output("status", "--porcelain=v1", "--", relative)
        runner_commit = git_output("log", "-1", "--format=%H", "--", relative)
        if not runner_commit or dirty:
            raise InvalidRun("authoritative Phase56 runner must be committed and clean")
        if runner_commit == MANIFEST_COMMIT or not P55.is_ancestor(MANIFEST_COMMIT, runner_commit):
            raise InvalidRun("Phase56 runner commit must descend from manifest commit")
        runner_guard.update(
            {
                "runner_commit": runner_commit,
                "runner_clean": True,
                "manifest_is_ancestor": True,
                "runner_commit_blob_guard": P55.committed_blob_guard(relative, runner_commit),
            }
        )
    return InputBundle(
        manifest=manifest,
        manifest_raw=raw,
        phase55_bundle=phase55_bundle,
        phase55_result=phase55_result,
        observed=observed,
        expected_sha=expected_sha,
        consumed_paths=tuple(path_map[key] for key in sorted(path_map)),
        runtime=runtime,
        runner_guard=runner_guard,
    )


def post_rehash(bundle: InputBundle) -> Mapping[str, Any]:
    expected = dict(bundle.expected_sha)
    expected[str(INPUT_PATH.relative_to(REPO_ROOT))] = MANIFEST_SHA256
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
        records.append({"path": relative, "sha256": digest, "unchanged_after_evaluation": True})
    if len(records) != 31 or len({record["path"] for record in records}) != 31:
        raise InvalidRun("Phase56 post-rehash path count drift")
    return {"count": 31, "records": records, "all_unchanged": True}


@dataclass(frozen=True)
class SelectedTarget:
    target: Any
    phase53_saddle_summary: Mapping[str, Any]
    phase55_saved_target: Mapping[str, Any]
    phase55_launch: Mapping[str, Any]
    phase55_primary_attempt: Mapping[str, Any]
    phase55_relation_projection: Mapping[str, Any]
    phase55_states: tuple[np.ndarray, ...]
    phase55_residual: np.ndarray


def digest_guard(
    value: Any, *, expected_bytes: int | None, expected_sha: str, label: str
) -> None:
    raw = canonical_bytes(value)
    if (expected_bytes is not None and len(raw) != expected_bytes) or sha256_bytes(raw) != expected_sha:
        raise InvalidRun(f"canonical subtree drift: {label}")


def select_target(bundle: InputBundle) -> SelectedTarget:
    try:
        targets = P55.extract_targets(bundle.phase55_bundle)
    except Exception as error:
        raise InvalidRun(f"Phase55 target extraction failed: {error}") from error
    if len(targets) != 3 or float(targets[1].lambda_value) != LAMBDA_VALUE:
        raise InvalidRun("selected lambda-half target order drift")
    target = targets[1]
    contract = bundle.manifest["selected_lambda_half_contract"]
    phase53 = P55.loaded_suffix(
        bundle.phase55_bundle, "PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json"
    )
    phase50 = P55.loaded_suffix(
        bundle.phase55_bundle, "PHASE50_M4_M5_JOINT_SADDLE_HOMOTOPY_RESULT.json"
    )
    root_payload = pointer_get(phase53, contract["root_pointer_in_phase53"])
    saddle_payload = pointer_get(phase50, contract["phase50_saddle_pointer"])
    endpoint_payload = pointer_get(phase53, contract["saved_endpoint_pointer_in_phase53"])
    digest_guard(root_payload, expected_bytes=None, expected_sha=contract["root_sha256"], label="root")
    digest_guard(saddle_payload, expected_bytes=None, expected_sha=contract["phase50_saddle_sha256"], label="P50 saddle")
    digest_guard(endpoint_payload, expected_bytes=None, expected_sha=contract["saved_endpoint_sha256"], label="saved endpoint")
    saddle_summary = pointer_get(phase53, contract["phase53_saddle_summary_pointer"])
    digest_guard(
        saddle_summary,
        expected_bytes=int(contract["phase53_saddle_summary_canonical_bytes"]),
        expected_sha=contract["phase53_saddle_summary_sha256"],
        label="Phase53 saddle summary",
    )
    if any(
        saddle_summary.get(key) != value
        for key, value in contract["phase53_saddle_summary"].items()
    ):
        raise InvalidRun("Phase53 saddle summary value drift")
    if (
        target.parameters.shape != (18,)
        or target.p50_saddle.shape != (9,)
        or target.saved_endpoint_z.shape != (9,)
        or float(target.parameters[17]) != float(contract["saved_flow_time"])
        or str(target.saved_scaled_residual) != str(contract["saved_scaled_residual_max_abs_decimal"])
    ):
        raise InvalidRun("selected target vector/scalar drift")

    phase55 = bundle.phase55_result
    baseline = bundle.manifest["phase55_baseline_contract"]
    saved_target = pointer_get(phase55, baseline["saved_target_pointer"])
    launch = pointer_get(phase55, baseline["launch_pointer"])
    primary_attempt = pointer_get(phase55, baseline["primary_ode_attempt_pointer"])
    for value, prefix, label in (
        (saved_target, "saved_target", "Phase55 saved target"),
        (launch, "launch", "Phase55 launch"),
        (primary_attempt, "primary_ode_attempt", "Phase55 primary attempt"),
    ):
        digest_guard(
            value,
            expected_bytes=int(baseline[f"{prefix}_canonical_bytes"]),
            expected_sha=baseline[f"{prefix}_sha256"],
            label=label,
        )
    saved_endpoint_relation = phase55["relation_ledgers"]["saved_Phase53_endpoint_reproduction"][1]
    scaled_residual_relation = phase55["relation_ledgers"]["scaled_residuals"][2]
    relation_projection = {
        "saved_endpoint": saved_endpoint_relation,
        "scaled_residual": scaled_residual_relation,
    }
    digest_guard(
        relation_projection,
        expected_bytes=int(baseline["primary_relation_projection_canonical_bytes"]),
        expected_sha=baseline["primary_relation_projection_sha256"],
        label="Phase55 primary relation projection",
    )
    state_contract = baseline["all_five_physical_states_selection"]
    state_records = [pointer_get(phase55, pointer) for pointer in state_contract["pointers_in_phase55_result"]]
    attributes = state_contract["required_attributes_in_order"]
    if [float(record.get("fraction")) for record in state_records] != list(FRACTION_ORDER):
        raise InvalidRun("Phase55 baseline fraction order drift")
    if any(
        record.get("family") != attributes["family"]
        or record.get("trajectory_backend") != attributes["trajectory_backend"]
        or float(record.get("lambda")) != LAMBDA_VALUE
        or record.get("status") != "EVALUATED"
        for record in state_records
    ):
        raise InvalidRun("Phase55 baseline state attributes drift")
    states = tuple(
        decode_complex_record(record["physical_state_z"], label=f"Phase55 state fraction={fraction}")
        for record, fraction in zip(state_records, FRACTION_ORDER, strict=True)
    )
    residual = finite_array(
        np.asarray(scaled_residual_relation["residual_vector_interleaved"], dtype=float),
        role="Phase55 primary residual vector",
    )
    if residual.shape != (18,):
        raise InvalidRun("Phase55 primary residual vector shape drift")
    return SelectedTarget(
        target=target,
        phase53_saddle_summary=saddle_summary,
        phase55_saved_target=saved_target,
        phase55_launch=launch,
        phase55_primary_attempt=primary_attempt,
        phase55_relation_projection=relation_projection,
        phase55_states=states,
        phase55_residual=residual,
    )


def preenumerated_topology(manifest: Mapping[str, Any]) -> Mapping[str, Any]:
    corner_parts = {
        "P50_center__P50_launch": ("P50", "P50"),
        "P50_center__fresh_launch": ("P50", "fresh"),
        "fresh_center__P50_launch": ("fresh", "P50"),
        "fresh_center__fresh_launch": ("fresh", "fresh"),
    }
    attempts = [f"attempt:{profile}:{corner}" for profile in PROFILE_ORDER for corner in CORNER_ORDER]
    fractions = [f"state:{profile}:{corner}:fraction={fraction:g}" for profile in PROFILE_ORDER for corner in CORNER_ORDER for fraction in FRACTION_ORDER]
    endpoints = [f"endpoint:{profile}:{corner}" for profile in PROFILE_ORDER for corner in CORNER_ORDER]
    residuals = [f"residual:{profile}:{corner}" for profile in PROFILE_ORDER for corner in CORNER_ORDER]
    scalar_gates = [
        f"gate:{profile}:{corner}:{gate}"
        for profile in PROFILE_ORDER
        for corner in CORNER_ORDER
        for gate in ("saved_endpoint_relative", "scaled_residual_absolute", "saved_residual_scalar_difference")
    ]
    overall = [f"overall:{profile}:{corner}" for profile in PROFILE_ORDER for corner in CORNER_ORDER]
    identities = [f"identity:{profile}:{corner}" for profile in PROFILE_ORDER for corner in CORNER_ORDER]
    effects = [f"effect:{profile}:{effect}" for profile in PROFILE_ORDER for effect in ("center", "launch", "interaction")]
    stability = [f"stability:{corner}" for corner in CORNER_ORDER]
    payload = {
        "center_order": list(CENTER_ORDER),
        "launch_order": list(LAUNCH_ORDER),
        "corner_order": list(CORNER_ORDER),
        "corner_parts": corner_parts,
        "profile_order": list(PROFILE_ORDER),
        "fraction_order": list(FRACTION_ORDER),
        "attempt_ids": attempts,
        "fraction_state_ids": fractions,
        "endpoint_ids": endpoints,
        "residual_ids": residuals,
        "scalar_gate_ids": scalar_gates,
        "overall_gate_ids": overall,
        "residual_identity_ids": identities,
        "factorial_effect_ids": effects,
        "profile_stability_ids": stability,
    }
    counts = {
        "center_records": len(CENTER_ORDER),
        "launch_records": len(LAUNCH_ORDER),
        "factorial_corner_records": len(CORNER_ORDER),
        "solver_profile_records": len(PROFILE_ORDER),
        "ODE_attempt_slots": len(attempts),
        "fraction_state_slots": len(fractions),
        "endpoint_records": len(endpoints),
        "scaled_residual_vector_records": len(residuals),
        "scalar_target_gate_records": len(scalar_gates),
        "overall_corner_gate_records": len(overall),
        "saved_endpoint_residual_identity_records": len(identities),
        "factorial_effect_records": len(effects),
        "profile_stability_records": len(stability),
    }
    expected = manifest["required_outputs"]["preenumerated_record_topology"]
    for key, value in counts.items():
        if int(expected[key]) != value:
            raise InvalidRun(f"preenumerated count drift at {key}")
    if tuple(manifest["factorial_contract"]["center_order"]) != CENTER_ORDER or tuple(manifest["factorial_contract"]["launch_order"]) != LAUNCH_ORDER or tuple(manifest["factorial_contract"]["corner_order"]) != CORNER_ORDER or tuple(manifest["ode_contract"]["profile_order"]) != PROFILE_ORDER or tuple(manifest["ode_contract"]["fraction_order"]) != FRACTION_ORDER:
        raise InvalidRun("preenumerated deterministic order drift")
    if not all(len(values) == len(set(values)) for values in (attempts, fractions, endpoints, residuals, scalar_gates, overall, identities, effects, stability)):
        raise InvalidRun("preenumerated key uniqueness failure")
    raw = canonical_bytes(payload)
    return {"payload": payload, "counts": counts, "canonical_bytes": len(raw), "sha256": sha256_bytes(raw)}


@dataclass
class TopologyGuard:
    setup: Any
    counters: dict[str, int] = field(default_factory=lambda: {
        "allowed_fresh_saddle_root": 0,
        "forbidden_root": 0,
        "saddle_cache_miss": 0,
        "saddle_cache_hit": 0,
        "runner_solve_ivp": 0,
        "forbidden_solve_ivp": 0,
        "Gamma_K_root_or_continuation": 0,
        "inherited_integrate_k": 0,
        "tangent_or_event": 0,
        "finite_difference": 0,
        "reflection": 0,
        "action_or_first_cap": 0,
    })
    restores: list[tuple[Any, str, Any]] = field(default_factory=list)
    root_scope: bool = False
    expected_seed_sha256: str | None = None
    last_root_solution: Any | None = None

    def replace(self, owner: Any, name: str, value: Any) -> None:
        if hasattr(owner, name):
            self.restores.append((owner, name, getattr(owner, name)))
            setattr(owner, name, value)

    def raising(self, counter: str, role: str) -> Callable[..., Any]:
        def sentinel(*_args: Any, **_kwargs: Any) -> Any:
            self.counters[counter] += 1
            raise InvalidRun(f"forbidden Phase56 call escaped guard: {role}")
        sentinel.__name__ = f"phase56_forbidden_{role.replace('.', '_')}"
        return sentinel

    def install(self) -> None:
        p51 = self.setup.p51
        original_root = p51.root
        original_public_root = scipy.optimize.root

        def allowed_root(function: Any, seed: Any, *args: Any, **kwargs: Any) -> Any:
            seed_array = np.ascontiguousarray(np.asarray(seed, dtype=float))
            options = kwargs.get("options")
            if (
                not self.root_scope
                or self.counters["allowed_fresh_saddle_root"] != 0
                or sha256_bytes(seed_array.tobytes(order="C")) != self.expected_seed_sha256
                or kwargs.get("method") != "hybr"
                or not callable(kwargs.get("jac"))
                or not isinstance(options, Mapping)
                or float(options.get("xtol", -1)) != 1.0e-11
                or int(options.get("maxfev", -1)) != 200
            ):
                self.counters["forbidden_root"] += 1
                raise InvalidRun("fresh saddle root call signature/seed/scope drift")
            self.counters["allowed_fresh_saddle_root"] += 1
            solution = original_root(function, seed, *args, **kwargs)
            self.last_root_solution = solution
            return solution

        self.replace(p51, "root", allowed_root)
        self.replace(scipy.optimize, "root", self.raising("forbidden_root", "scipy.optimize.root"))
        self.replace(scipy.integrate, "solve_ivp", self.raising("forbidden_solve_ivp", "scipy.integrate.solve_ivp"))
        candidate_modules = [
            p51, self.setup.p52, self.setup.p53, self.setup.p54,
            self.setup.factory.phase41, self.setup.factory.phase50, P55,
        ]
        for module in tuple(sys.modules.values()):
            module_file = getattr(module, "__file__", None)
            if not module_file:
                continue
            try:
                resolved = Path(module_file).resolve()
                in_pinned_tree = resolved.parent == SCRIPT_PATH.parent
                is_phase56_runner = resolved == SCRIPT_PATH
            except (OSError, RuntimeError):
                in_pinned_tree = False
                is_phase56_runner = False
            if (
                in_pinned_tree
                and not is_phase56_runner
                and module not in candidate_modules
            ):
                candidate_modules.append(module)
        for module in candidate_modules:
            for name, value in tuple(vars(module).items()):
                if module is p51 and name == "root":
                    continue
                if value is original_public_root:
                    self.replace(module, name, self.raising("forbidden_root", f"{module.__name__}.{name}"))
                if value is ALLOWED_SOLVE_IVP:
                    self.replace(module, name, self.raising("forbidden_solve_ivp", f"{module.__name__}.{name}"))
        for name in ("solve_root", "solve_path"):
            self.replace(p51, name, self.raising("Gamma_K_root_or_continuation", f"phase51.{name}"))
        for name in ("finite_difference_jacobian_control", "outer_tangent_control", "flow_ledger", "cse_validation", "cse_trajectory_validation"):
            self.replace(p51, name, self.raising("finite_difference", f"phase51.{name}"))
        self.replace(p51, "reflected_state_distances", self.raising("reflection", "phase51.reflected_state_distances"))
        self.replace(p51, "integrate_k", self.raising("inherited_integrate_k", "phase51.integrate_k"))
        self.replace(self.setup.repaired, "action_only", self.raising("action_or_first_cap", "repaired.action_only"))

        original_saddle = p51.SourceContext.saddle
        def guarded_saddle(source: Any, lambda_value: float) -> np.ndarray:
            key = round(float(lambda_value), 14)
            if key in source._saddle_cache:
                self.counters["saddle_cache_hit"] += 1
            else:
                self.counters["saddle_cache_miss"] += 1
                if not self.root_scope or key != LAMBDA_VALUE or self.counters["saddle_cache_miss"] != 1:
                    raise InvalidRun(f"undeclared saddle cache miss at lambda={key}")
            return original_saddle(source, lambda_value)
        self.replace(p51.SourceContext, "saddle", guarded_saddle)

    @contextmanager
    def allow_one_fresh_root(self, seed: np.ndarray):
        if self.root_scope:
            raise InvalidRun("nested fresh-root scope")
        self.root_scope = True
        self.expected_seed_sha256 = sha256_bytes(
            np.ascontiguousarray(np.asarray(seed, dtype=float)).tobytes(order="C")
        )
        try:
            yield
        finally:
            self.root_scope = False
            self.expected_seed_sha256 = None

    def restore(self) -> None:
        for owner, name, original in reversed(self.restores):
            setattr(owner, name, original)
        self.restores.clear()

    def assert_forbidden_zero(self) -> None:
        allowed = {"allowed_fresh_saddle_root", "saddle_cache_miss", "saddle_cache_hit", "runner_solve_ivp"}
        escaped = {key: value for key, value in self.counters.items() if key not in allowed and value}
        if escaped:
            raise InvalidRun(f"forbidden topology counters nonzero: {escaped}")


@contextmanager
def guarded_topology(setup: Any):
    guard = TopologyGuard(setup)
    guard.install()
    try:
        yield guard
    finally:
        guard.restore()


def saddle_evaluation(setup: Any, saddle: np.ndarray, *, role: str) -> tuple[Mapping[str, Any], np.ndarray, np.ndarray]:
    with setup.repaired.mode("gradient_hessian", consumer=f"Phase56.{role}"):
        _action, gradient, hessian = setup.repaired.evaluate(
            LAMBDA_VALUE, np.asarray(saddle, dtype=np.clongdouble)
        )
    gradient = finite_array(np.asarray(gradient, dtype=np.clongdouble), role=f"{role}:gradient")
    hessian = finite_array(np.asarray(hessian, dtype=np.clongdouble), role=f"{role}:hessian")
    if gradient.shape != (9,) or hessian.shape != (9, 9):
        raise InvalidRun(f"saddle evaluation shape drift at {role}")
    real_hessian = np.asarray(hessian.real, dtype=float)
    eigenvalues = finite_array(np.linalg.eigvalsh(real_hessian), role=f"{role}:eigenvalues")
    inertia = {
        "negative": int(np.count_nonzero(eigenvalues < 0.0)),
        "positive": int(np.count_nonzero(eigenvalues > 0.0)),
        "zero": int(np.count_nonzero(eigenvalues == 0.0)),
    }
    record = {
        "role": role,
        "lambda": LAMBDA_VALUE,
        "saddle_w": np.asarray(saddle, dtype=float),
        "gradient": gradient,
        "hessian_real_eigenvalues": eigenvalues,
        "gradient_max_abs_decimal": P55.ld_text(np.max(np.abs(gradient))),
        "hessian_imag_max_abs_decimal": P55.ld_text(np.max(np.abs(hessian.imag))),
        "hessian_min_abs_real_eigenvalue_decimal": P55.ld_text(np.min(np.abs(eigenvalues))),
        "hessian_inertia": inertia,
        "finite": True,
    }
    return record, gradient, hessian


def saddle_gates(record: Mapping[str, Any], *, distance: str | None, manifest: Mapping[str, Any]) -> Mapping[str, Any]:
    gates = manifest["fresh_saddle_and_launch_contract"]["fresh_saddle_gates"]
    outcomes = {
        "gradient": decimal(record["gradient_max_abs_decimal"], label="fresh gradient") <= decimal(gates["gradient_max_abs_max"], label="fresh gradient threshold"),
        "distance": distance is not None and decimal(distance, label="fresh distance") <= decimal(gates["distance_to_pinned_phase50_max"], label="fresh distance threshold"),
        "hessian_gap": decimal(record["hessian_min_abs_real_eigenvalue_decimal"], label="fresh gap") >= decimal(gates["hessian_min_abs_eigenvalue_min"], label="fresh gap threshold"),
        "hessian_imag": decimal(record["hessian_imag_max_abs_decimal"], label="fresh imag") <= decimal(gates["hessian_imag_max_abs_max"], label="fresh imag threshold"),
        "inertia": record["hessian_inertia"] == gates["required_inertia"],
    }
    return {"outcomes": outcomes, "passed": all(outcomes.values()), "thresholds": gates}


@dataclass
class LaunchRuntime:
    label: str
    status: str
    passed: bool
    failure_id: str | None
    node: Any | None
    initial_xi_long: np.ndarray | None
    initial_xi_buffer: np.ndarray | None
    record: Mapping[str, Any]


def launch_from_center(
    setup: Any,
    target: SelectedTarget,
    center_label: str,
    center: np.ndarray,
    manifest: Mapping[str, Any],
) -> LaunchRuntime:
    context = setup.context
    context._saddle_cache[round(LAMBDA_VALUE, 14)] = np.asarray(center, dtype=float).copy()
    try:
        with setup.repaired.mode(
            "gradient_hessian", consumer=f"Phase56.{center_label}_launch_Hessian"
        ):
            node = context.node(LAMBDA_VALUE, radius=1.0e-4, shape_key="lambda_1")
    except Exception as error:
        if isinstance(error, setup.p51.NumericalFailure):
            failure = f"reconstruction:{center_label}:launch_nonpass"
            return LaunchRuntime(
                label=center_label,
                status="NONPASS",
                passed=False,
                failure_id=failure,
                node=None,
                initial_xi_long=None,
                initial_xi_buffer=None,
                record={
                    "label": center_label,
                    "status": "NONPASS",
                    "failure_id": failure,
                    "exception_type": type(error).__name__,
                    "message": str(error),
                },
            )
        raise InvalidRun(f"undeclared {center_label} launch exception: {error}") from error
    omega, _derivative = context.chart.direction(target.target.parameters[9:17])
    launch_coefficient = np.asarray(node.factor_inverse, dtype=np.longdouble) @ np.asarray(node.launch_w, dtype=np.clongdouble)
    initial_xi = np.clongdouble(node.sphere_radius) * (
        launch_coefficient @ np.asarray(omega, dtype=np.longdouble)
    )
    initial_buffer = np.ascontiguousarray(initial_xi, dtype=np.complex128)
    initial_w = np.asarray(center, dtype=np.clongdouble) + np.asarray(
        node.factor, dtype=np.longdouble
    ) @ np.asarray(initial_xi, dtype=np.clongdouble)
    initial_z = np.asarray(setup.context.scales5, dtype=np.longdouble) * initial_w
    for role, value in (
        ("factor", node.factor), ("factor_inverse", node.factor_inverse),
        ("launch_w", node.launch_w), ("omega", omega), ("initial_xi", initial_xi),
        ("initial_state_w5", initial_w), ("initial_physical_state_z", initial_z),
    ):
        finite_array(value, role=f"{center_label}_launch:{role}")
    identity = np.eye(9)
    factor = np.asarray(node.factor, dtype=float)
    factor_inverse = np.asarray(node.factor_inverse, dtype=float)
    factor_inverse_left = np.linalg.norm(factor @ factor_inverse - identity) / np.linalg.norm(identity)
    factor_inverse_right = np.linalg.norm(factor_inverse @ factor - identity) / np.linalg.norm(identity)
    launch_gates = manifest["fresh_saddle_and_launch_contract"]["launch_gates"]
    launch_record = node.launch_record
    outcomes = {
        "hessian_imag": decimal(launch_record["hessian_imag_max_abs"], label="launch Hessian imaginary") <= decimal(launch_gates["hessian_imag_max_abs_max"], label="launch Hessian imaginary threshold"),
        "inertia": launch_record["hessian_inertia"] == launch_gates["required_inertia"],
        "factor_mobility": decimal(launch_record["factor_relative_residual"], label="factor mobility") <= decimal(launch_gates["factor_mobility_relative_max"], label="factor mobility threshold"),
        "orientation": float(launch_record["signed_frame_determinant"]) > 0.0,
    }
    passed = all(outcomes.values())
    failure = None if passed else f"reconstruction:{center_label}:launch_gate_nonpass"
    return LaunchRuntime(
        label=center_label,
        status="PASS" if passed else "NONPASS",
        passed=passed,
        failure_id=failure,
        node=node,
        initial_xi_long=np.asarray(initial_xi, dtype=np.clongdouble),
        initial_xi_buffer=initial_buffer,
        record={
            "label": center_label,
            "source": SOURCE,
            "lambda": LAMBDA_VALUE,
            "status": "PASS" if passed else "NONPASS",
            "failure_id": failure,
            "policy": (
                "P50_SADDLE_PINNED_PHASE56_BASELINE_RECONSTRUCTION"
                if center_label == "P50"
                else "FRESH_PHASE53_ALGORITHM_PHASE56_RECONSTRUCTION"
            ),
            "center_w": np.asarray(center, dtype=float),
            "radius": float(node.sphere_radius),
            "shape_key": node.shape_key,
            "flow_time": float(target.target.parameters[17]),
            "exact_Phase53_launch_claim": False,
            "outcomes": outcomes,
            "saddle_w": P55.reconstructed_object_hash("saddle_w", node.saddle_w),
            "factor": P55.reconstructed_object_hash("factor", node.factor),
            "factor_inverse": P55.reconstructed_object_hash("factor_inverse", node.factor_inverse),
            "launch_w": P55.reconstructed_object_hash("launch_w", node.launch_w),
            "chart_direction": P55.reconstructed_object_hash("chart_direction", omega),
            "initial_xi": P55.reconstructed_object_hash("initial_xi", initial_xi),
            "initial_state_w5": P55.reconstructed_object_hash("initial_state_w5", initial_w),
            "initial_physical_state_z": P55.reconstructed_object_hash("initial_physical_state_z", initial_z),
            "initial_xi_complex128": {
                "dtype": str(initial_buffer.dtype),
                "C_contiguous": bool(initial_buffer.flags.c_contiguous),
                "byte_count": int(initial_buffer.nbytes),
                "raw_bytes_sha256": sha256_bytes(initial_buffer.tobytes(order="C")),
                "single_cast_from_clongdouble": True,
            },
            "factor_inverse_identity_diagnostics": {
                "factor_times_inverse_relative": P55.ld_text(factor_inverse_left),
                "inverse_times_factor_relative": P55.ld_text(factor_inverse_right),
            },
            "node_launch_record": launch_record,
        },
    )


@dataclass
class FreshCalculation:
    p50_record: Mapping[str, Any]
    fresh_record: Mapping[str, Any]
    fresh_center: np.ndarray | None
    fresh_passed: bool
    fresh_failure_id: str | None
    newton_record: Mapping[str, Any]
    launches: Mapping[str, LaunchRuntime]
    p50_baseline_launch_passed: bool
    p50_baseline_launch_comparison: Mapping[str, Any]
    phase_wide_prerequisite: bool


def calculate_fresh_and_launches(
    setup: Any,
    selected: SelectedTarget,
    manifest: Mapping[str, Any],
    guard: TopologyGuard,
) -> FreshCalculation:
    context = setup.context
    context.evaluator = setup.repaired
    if context._saddle_cache:
        raise InvalidRun("saddle cache populated before Phase56 fresh solve")
    p50 = np.asarray(selected.target.p50_saddle, dtype=float)
    p50_record, gradient0, hessian0 = saddle_evaluation(setup, p50, role="P50_saddle")
    h_real = np.asarray(hessian0.real, dtype=float)
    g_real = np.asarray(gradient0.real, dtype=float)
    try:
        delta_newton = np.linalg.solve(h_real, -g_real)
    except np.linalg.LinAlgError as error:
        raise InvalidRun(f"Newton prediction solve failed: {error}") from error
    finite_array(delta_newton, role="Newton displacement")
    linear_residual = h_real @ delta_newton + g_real
    predicted = p50 + delta_newton
    predicted_record, predicted_gradient, _predicted_hessian = saddle_evaluation(
        setup, predicted, role="Newton_predicted_saddle"
    )
    newton_record: dict[str, Any] = {
        "formula": "delta_s_N=-solve(H_real(P50),g_real(P50))",
        "predicted_displacement": delta_newton,
        "predicted_center": predicted,
        "predicted_displacement_norm_decimal": P55.ld_text(np.linalg.norm(delta_newton)),
        "predicted_displacement_max_abs_decimal": P55.ld_text(np.max(np.abs(delta_newton))),
        "linear_solve_residual": linear_residual,
        "linear_solve_residual_max_abs_decimal": P55.ld_text(np.max(np.abs(linear_residual))),
        "linear_solve_threshold_decimal": manifest["fresh_saddle_and_launch_contract"]["newton_prediction"]["required_linear_solve_residual_max_abs"],
        "gradient_at_P50": gradient0,
        "gradient_at_predicted_point": predicted_gradient,
        "predicted_point_evaluation": predicted_record,
        "actual_comparison": None,
    }
    fresh: np.ndarray | None = None
    fresh_failure: str | None = None
    solver_exception: str | None = None
    try:
        with guard.allow_one_fresh_root(p50):
            with setup.repaired.mode("gradient_hessian", consumer="Phase56.SourceContext.saddle"):
                fresh = np.asarray(context.saddle(LAMBDA_VALUE), dtype=float)
    except Exception as error:
        if isinstance(error, setup.p51.NumericalFailure):
            solver_exception = str(error)
            fresh_failure = "reconstruction:fresh:saddle_nonpass"
        else:
            raise InvalidRun(f"fresh saddle solve exception: {error}") from error
    solver_record = dict(context._saddle_records.get(round(LAMBDA_VALUE, 14), {}))
    if guard.counters["allowed_fresh_saddle_root"] != 1 or guard.counters["saddle_cache_miss"] != 1:
        raise InvalidRun("fresh saddle one-root topology drift")
    if fresh is None and guard.last_root_solution is not None:
        solved_x = np.asarray(getattr(guard.last_root_solution, "x", []), dtype=float)
        if solved_x.shape == (9,) and np.all(np.isfinite(solved_x)):
            fresh = solved_x.copy()
    if fresh is None:
        for value in solver_record.values():
            if isinstance(value, (float, int)) and not isinstance(value, bool) and not np.isfinite(value):
                raise InvalidRun("nonfinite failed fresh saddle record")
        fresh_record = {
            "role": "fresh_saddle",
            "status": "NONPASS",
            "failure_id": fresh_failure,
            "solver_record": solver_record,
            "solver_exception": solver_exception,
            "historical_summary": selected.phase53_saddle_summary,
        }
        fresh_passed = False
    else:
        fresh_eval, fresh_gradient, fresh_hessian = saddle_evaluation(setup, fresh, role="fresh_saddle")
        displacement = fresh - p50
        distance = P55.ld_text(np.linalg.norm(displacement))
        gates = saddle_gates(fresh_eval, distance=distance, manifest=manifest)
        solver_success = bool(solver_record.get("solver_success"))
        accepted = bool(solver_record.get("accepted"))
        fresh_passed = bool(solver_success and accepted and gates["passed"])
        fresh_failure = None if fresh_passed else "reconstruction:fresh:saddle_gate_nonpass"
        actual_norm = float(np.linalg.norm(displacement))
        predicted_norm = float(np.linalg.norm(delta_newton))
        cosine = None if actual_norm == 0.0 or predicted_norm == 0.0 else float(np.dot(displacement, delta_newton) / (actual_norm * predicted_norm))
        prediction_error = displacement - delta_newton
        newton_record["actual_comparison"] = {
            "actual_displacement": displacement,
            "actual_displacement_norm_decimal": P55.ld_text(actual_norm),
            "actual_displacement_max_abs_decimal": P55.ld_text(np.max(np.abs(displacement))),
            "actual_minus_predicted": prediction_error,
            "actual_minus_predicted_norm_decimal": P55.ld_text(np.linalg.norm(prediction_error)),
            "actual_minus_predicted_relative_decimal": P55.ld_text(np.linalg.norm(prediction_error) / max(actual_norm, 1.0e-100)),
            "cosine": cosine,
            "gradient_at_fresh_solved_point": fresh_gradient,
        }
        summary_differences = {
            key: P55.ld_text(abs(np.longdouble(str(solver_record[key])) - np.longdouble(str(selected.phase53_saddle_summary[key]))))
            for key in ("distance_to_pinned_phase50", "gradient_max_abs", "hessian_min_abs_eigenvalue")
            if key in solver_record
        }
        fresh_record = {
            **fresh_eval,
            "status": "PASS" if fresh_passed else "NONPASS",
            "failure_id": fresh_failure,
            "distance_to_pinned_phase50_decimal": distance,
            "solver_record": solver_record,
            "gates": gates,
            "historical_Phase53_summary": selected.phase53_saddle_summary,
            "historical_summary_absolute_differences": summary_differences,
            "exact_historical_saddle_byte_identity_claimed": False,
        }

    p50_launch = launch_from_center(setup, selected, "P50", p50, manifest)
    expected_digest = manifest["phase55_baseline_contract"]["primary_p50_initial_xi_complex128_raw_c_order_sha256"]
    expected_bytes = int(manifest["phase55_baseline_contract"]["primary_p50_initial_xi_complex128_raw_c_order_bytes"])
    current_boundary = p50_launch.record.get("initial_xi_complex128", {})
    historical_boundary = selected.phase55_launch["solver_boundary_initial_xi"]
    historical_hashes = selected.phase55_launch["hashes"]
    hash_outcomes = {
        key: bool(
            p50_launch.passed
            and p50_launch.record.get(key, {}).get("sha256")
            == historical_hashes[key]["sha256"]
        )
        for key in historical_hashes
    }
    structure_outcomes = {
        "source": p50_launch.record.get("source") == selected.phase55_launch["source"],
        "lambda": p50_launch.record.get("lambda") == selected.phase55_launch["lambda"],
        "status": p50_launch.record.get("status") == selected.phase55_launch["status"],
        "radius": p50_launch.record.get("radius") == selected.phase55_launch["radius"],
        "shape_key": p50_launch.record.get("shape_key") == selected.phase55_launch["shape_key"],
        "flow_time": p50_launch.record.get("flow_time") == selected.phase55_launch["flow_time"],
        "exact_Phase53_launch_claim": (
            p50_launch.record.get("exact_Phase53_launch_claim")
            == selected.phase55_launch["exact_Phase53_launch_claim"]
        ),
        "node_launch_record": (
            P55.json_ready(p50_launch.record.get("node_launch_record"))
            == selected.phase55_launch["node_launch_record"]
        ),
    }
    boundary_outcomes = {
        key: current_boundary.get(key) == historical_boundary[key]
        for key in (
            "dtype",
            "C_contiguous",
            "byte_count",
            "raw_bytes_sha256",
            "single_cast_from_clongdouble",
        )
    }
    boundary_outcomes["manifest_byte_count"] = (
        current_boundary.get("byte_count") == expected_bytes
    )
    boundary_outcomes["manifest_sha256"] = (
        current_boundary.get("raw_bytes_sha256") == expected_digest
    )
    p50_launch_comparison = {
        "hash_outcomes": hash_outcomes,
        "structure_outcomes": structure_outcomes,
        "solver_boundary_outcomes": boundary_outcomes,
        "all_passed": bool(
            p50_launch.passed
            and all(hash_outcomes.values())
            and all(structure_outcomes.values())
            and all(boundary_outcomes.values())
        ),
    }
    p50_launch_digest_ok = bool(p50_launch_comparison["all_passed"])
    launches: dict[str, LaunchRuntime] = {"P50": p50_launch}
    if fresh is not None and fresh_passed:
        fresh_launch = launch_from_center(setup, selected, "fresh", fresh, manifest)
    else:
        cause = fresh_failure or "reconstruction:fresh:saddle_nonpass"
        fresh_launch = LaunchRuntime(
            label="fresh", status="NOT_EVALUATED", passed=False,
            failure_id=cause, node=None, initial_xi_long=None, initial_xi_buffer=None,
            record={"label": "fresh", "status": "NOT_EVALUATED", "causal_failure_id": cause},
        )
    launches["fresh"] = fresh_launch
    if p50_launch.node is not None and fresh_launch.node is not None:
        if not np.array_equal(np.asarray(p50_launch.node.factor), np.asarray(fresh_launch.node.factor)) or not np.array_equal(np.asarray(p50_launch.node.factor_inverse), np.asarray(fresh_launch.node.factor_inverse)):
            raise InvalidRun("cross-center factor/factor-inverse exact equality failed")
    phase_wide = bool(fresh_passed and fresh_launch.passed)
    return FreshCalculation(
        p50_record=p50_record,
        fresh_record=fresh_record,
        fresh_center=fresh,
        fresh_passed=fresh_passed,
        fresh_failure_id=fresh_failure,
        newton_record=newton_record,
        launches=launches,
        p50_baseline_launch_passed=p50_launch_digest_ok,
        p50_baseline_launch_comparison=p50_launch_comparison,
        phase_wide_prerequisite=phase_wide,
    )


@dataclass(frozen=True)
class CornerRuntime:
    name: str
    center_label: str
    launch_label: str
    node: Any
    initial_xi_buffer: np.ndarray
    record: Mapping[str, Any]


@dataclass
class AttemptRuntime:
    profile: str
    corner: str
    status: str
    failure_id: str | None
    record: Mapping[str, Any]
    xi_by_fraction: dict[float, np.ndarray]


def construct_corners(setup: Any, fresh: FreshCalculation) -> tuple[Mapping[str, CornerRuntime], list[Mapping[str, Any]]]:
    p50_launch = fresh.launches["P50"]
    fresh_launch = fresh.launches["fresh"]
    if not fresh.phase_wide_prerequisite or p50_launch.node is None or fresh_launch.node is None or fresh.fresh_center is None:
        cause = (
            p50_launch.failure_id
            or fresh.fresh_failure_id
            or fresh_launch.failure_id
            or "reconstruction:factorial_input_unavailable"
        )
        return {}, [
            {
                "corner": corner,
                "center": "P50" if corner.startswith("P50_center") else "fresh",
                "launch": "P50" if corner.endswith("P50_launch") else "fresh",
                "status": "NOT_EVALUATED",
                "causal_failure_id": cause,
            }
            for corner in CORNER_ORDER
        ]
    centers = {
        "P50": np.asarray(fresh.p50_record["saddle_w"], dtype=float),
        "fresh": np.asarray(fresh.fresh_center, dtype=float),
    }
    launches = {"P50": p50_launch, "fresh": fresh_launch}
    common_factor = np.asarray(p50_launch.node.factor, dtype=float)
    output: dict[str, CornerRuntime] = {}
    records: list[Mapping[str, Any]] = []
    for corner in CORNER_ORDER:
        center_label, launch_label = {
            "P50_center__P50_launch": ("P50", "P50"),
            "P50_center__fresh_launch": ("P50", "fresh"),
            "fresh_center__P50_launch": ("fresh", "P50"),
            "fresh_center__fresh_launch": ("fresh", "fresh"),
        }[corner]
        launch = launches[launch_label]
        if launch.initial_xi_buffer is None:
            raise InvalidRun(f"available corner lacks initial xi: {corner}")
        node = SimpleNamespace(
            source=setup.context,
            lambda_value=LAMBDA_VALUE,
            saddle_w=centers[center_label].copy(),
            factor=common_factor,
        )
        buffer = np.ascontiguousarray(launch.initial_xi_buffer.copy(), dtype=np.complex128)
        initial_w = np.asarray(node.saddle_w, dtype=np.clongdouble) + np.asarray(common_factor, dtype=np.longdouble) @ np.asarray(buffer, dtype=np.clongdouble)
        initial_z = np.asarray(setup.context.scales5, dtype=np.longdouble) * initial_w
        finite_array(initial_z, role=f"{corner}:initial_z")
        record = {
            "corner": corner,
            "center": center_label,
            "launch": launch_label,
            "status": "PASS",
            "factor_source": "common_exact_P50_and_fresh_factor",
            "initial_xi_complex128_raw_c_order_sha256": sha256_bytes(buffer.tobytes(order="C")),
            "initial_xi_byte_count": int(buffer.nbytes),
            "initial_state_w5": initial_w,
            "initial_physical_state_z": initial_z,
        }
        output[corner] = CornerRuntime(corner, center_label, launch_label, node, buffer, record)
        records.append(record)
    z = {corner: np.asarray(output[corner].record["initial_physical_state_z"], dtype=np.clongdouble) for corner in CORNER_ORDER}
    interaction = z["fresh_center__fresh_launch"] - z["fresh_center__P50_launch"] - z["P50_center__fresh_launch"] + z["P50_center__P50_launch"]
    interaction_max = P55.ld_text(np.max(np.abs(interaction)))
    if decimal(interaction_max, label="initial factorial interaction") > Decimal("5e-18"):
        raise InvalidRun("initial factorial interaction identity failed")
    for record in records:
        record["common_initial_factorial_interaction_max_abs_decimal"] = interaction_max
    return output, records


def attempt_id(profile: str, corner: str) -> str:
    return f"attempt:{profile}:{corner}"


def state_id(profile: str, corner: str, fraction: float) -> str:
    return f"state:{profile}:{corner}:fraction={fraction:g}"


def placeholder_attempts(cause: str) -> list[AttemptRuntime]:
    output: list[AttemptRuntime] = []
    for profile in PROFILE_ORDER:
        for corner in CORNER_ORDER:
            output.append(
                AttemptRuntime(
                    profile=profile,
                    corner=corner,
                    status="NOT_ATTEMPTED_UPSTREAM_RECONSTRUCTION_NONPASS",
                    failure_id=cause,
                    record={
                        "attempt_id": attempt_id(profile, corner),
                        "profile": profile,
                        "corner": corner,
                        "status": "NOT_ATTEMPTED_UPSTREAM_RECONSTRUCTION_NONPASS",
                        "causal_failure_id": cause,
                        "returned_t_eval_count": 0,
                        "fraction_slots": [
                            {"state_id": state_id(profile, corner, fraction), "fraction": fraction, "status": "NOT_EVALUATED", "causal_failure_id": cause}
                            for fraction in FRACTION_ORDER
                        ],
                    },
                    xi_by_fraction={},
                )
            )
    return output


def run_odes(
    setup: Any,
    corners: Mapping[str, CornerRuntime],
    selected: SelectedTarget,
    manifest: Mapping[str, Any],
    guard: TopologyGuard,
) -> tuple[list[AttemptRuntime], Any]:
    evaluator = P55.ScheduleEvaluator(setup)
    attempts: list[AttemptRuntime] = []
    profiles = manifest["ode_contract"]["profiles"]
    flow_time = float(selected.target.parameters[17])
    t_eval = np.asarray(FRACTION_ORDER, dtype=float) * flow_time
    if t_eval[0] != 0.0 or t_eval[-1] != flow_time:
        raise InvalidRun("Phase56 t_eval endpoint drift")
    for profile in PROFILE_ORDER:
        specification = profiles[profile]
        for corner_name in CORNER_ORDER:
            corner = corners[corner_name]
            aid = attempt_id(profile, corner_name)
            before = corner.initial_xi_buffer.tobytes(order="C")
            calls_before = int(evaluator.calls["EL_long"])
            guard.counters["runner_solve_ivp"] += 1
            solution = ALLOWED_SOLVE_IVP(
                lambda _time, xi, node=corner.node: evaluator.rhs("EL_long", node, xi),
                (0.0, flow_time),
                corner.initial_xi_buffer.copy(),
                method="DOP853",
                rtol=float(specification["rtol"]),
                atol=float(specification["atol"]),
                max_step=float(specification["max_step"]),
                t_eval=t_eval,
                events=None,
            )
            if before != corner.initial_xi_buffer.tobytes(order="C"):
                raise InvalidRun(f"retained initial xi mutated: {aid}")
            returned = int(np.asarray(solution.t).size)
            if returned < 0 or returned > len(FRACTION_ORDER) or not np.array_equal(np.asarray(solution.t), t_eval[:returned]):
                raise InvalidRun(f"solve_ivp returned invalid t_eval prefix: {aid}")
            callback_delta = int(evaluator.calls["EL_long"]) - calls_before
            if callback_delta != int(solution.nfev) or evaluator.calls["EL_std"] != 0:
                raise InvalidRun(f"ODE callback binding drift: {aid}")
            raw_y = np.asarray(solution.y)
            if returned == 0 and raw_y.size == 0:
                raw_y = np.empty((9, 0), dtype=np.complex128)
            y = finite_array(raw_y, role=f"{aid}:returned_xi")
            if y.shape != (9, returned):
                raise InvalidRun(f"ODE returned state shape drift: {aid}")
            xi_by_fraction = {
                fraction: np.asarray(y[:, index], dtype=np.complex128).copy()
                for index, fraction in enumerate(FRACTION_ORDER[:returned])
            }
            norms = [P55.ld_text(np.linalg.norm(np.asarray(xi, dtype=np.clongdouble))) for xi in xi_by_fraction.values()]
            norm_max = max(norms, key=lambda item: decimal(item, label="xi norm")) if norms else None
            norm_pass = bool(norm_max is not None and decimal(norm_max, label="xi norm max") < Decimal("40"))
            completed = bool(solution.success and returned == 5 and norm_pass)
            failure = None if completed else f"{aid}:completion_or_flow_norm_nonpass"
            fraction_slots = [
                {
                    "state_id": state_id(profile, corner_name, fraction),
                    "fraction": fraction,
                    "status": "EVALUATED" if index < returned else "NOT_EVALUATED",
                    **({} if index < returned else {"causal_failure_id": failure}),
                }
                for index, fraction in enumerate(FRACTION_ORDER)
            ]
            attempts.append(
                AttemptRuntime(
                    profile=profile,
                    corner=corner_name,
                    status="PASS" if completed else "NONPASS",
                    failure_id=failure,
                    record={
                        "attempt_id": aid,
                        "profile": profile,
                        "corner": corner_name,
                        "status": "PASS" if completed else "NONPASS",
                        "failure_id": failure,
                        "solver_success": bool(solution.success),
                        "message": str(solution.message),
                        "method": "DOP853",
                        "rtol": float(specification["rtol"]),
                        "atol": float(specification["atol"]),
                        "max_step": float(specification["max_step"]),
                        "nfev": int(solution.nfev),
                        "njev": int(solution.njev),
                        "nlu": int(solution.nlu),
                        "runner_RHS_callback_count_delta": callback_delta,
                        "runner_RHS_callback_count_equals_nfev": True,
                        "returned_t_eval_count": returned,
                        "returned_fraction_order": list(FRACTION_ORDER[:returned]),
                        "fraction_slots": fraction_slots,
                        "returned_t_eval_xi_norm_decimals": norms,
                        "returned_t_eval_xi_norm_max_decimal": norm_max,
                        "returned_t_eval_xi_norm_strict_threshold_decimal": "40",
                        "returned_t_eval_xi_norm_pass": norm_pass,
                        "adaptive_internal_step_count_reported": False,
                        "with_tangent": False,
                        "event": False,
                    },
                    xi_by_fraction=xi_by_fraction,
                )
            )
    if len(attempts) != 8 or guard.counters["runner_solve_ivp"] != 8:
        raise InvalidRun("eight-attempt ODE topology drift")
    return attempts, evaluator


@dataclass
class Ledgers:
    states: list[Mapping[str, Any]]
    endpoints: list[Mapping[str, Any]]
    residuals: list[Mapping[str, Any]]
    scalar_gates: list[Mapping[str, Any]]
    overall_gates: list[Mapping[str, Any]]
    identities: list[Mapping[str, Any]]
    effects: list[Mapping[str, Any]]
    stability: list[Mapping[str, Any]]
    baseline: Mapping[str, Any]
    saved_residual: Mapping[str, Any]


def residual_vector(setup: Any, gamma: np.ndarray, z: np.ndarray, *, role: str) -> np.ndarray:
    # This cast-before-subtraction order is the Phase55 scientific gate.
    scaled = (
        np.asarray(gamma, dtype=np.complex128)
        - np.asarray(z, dtype=np.complex128)
    ) / np.asarray(setup.context.scales5, dtype=np.float64)
    residual = finite_array(setup.p51.interleaved(scaled), role=role)
    if residual.shape != (18,):
        raise InvalidRun(f"residual vector shape drift: {role}")
    return np.asarray(residual, dtype=float)


def max_decimal(values: Any) -> str:
    array = finite_array(values, role="maximum")
    return P55.ld_text(np.max(np.abs(np.asarray(array, dtype=np.longdouble)), initial=np.longdouble(0)))


def build_ledgers(
    setup: Any,
    selected: SelectedTarget,
    fresh: FreshCalculation,
    corners: Mapping[str, CornerRuntime],
    attempts: Sequence[AttemptRuntime],
    manifest: Mapping[str, Any],
) -> Ledgers:
    by_key = {(attempt.profile, attempt.corner): attempt for attempt in attempts}
    if len(by_key) != 8:
        raise InvalidRun("attempt index cardinality drift")
    gamma = finite_array(
        setup.p51.gamma_cap(setup.context, selected.target.parameters[:9])[0],
        role="saved Gamma cap state",
    )
    saved_z = np.asarray(selected.target.saved_endpoint_z, dtype=np.clongdouble)
    saved_residual = residual_vector(setup, gamma, saved_z, role="saved endpoint residual")
    saved_max = max_decimal(saved_residual)
    saved_scalar = str(selected.target.saved_scaled_residual)
    baseline_thresholds = manifest["phase55_baseline_contract"]["baseline_reproduction_thresholds"]
    saved_scalar_difference = abs(decimal(saved_max, label="saved residual maximum") - decimal(saved_scalar, label="saved scalar"))
    if saved_scalar_difference > decimal(baseline_thresholds["scaled_residual_scalar_absolute_difference"], label="saved scalar reproduction threshold"):
        raise InvalidRun("recomputed saved endpoint residual does not reproduce saved scalar")
    saved_residual_record = {
        "construction": "interleaved((gamma.astype(complex128)-saved_z.astype(complex128))/scales.astype(float64))",
        "vector": saved_residual,
        "maximum_decimal": saved_max,
        "pinned_saved_scalar_decimal": saved_scalar,
        "absolute_difference_decimal": str(saved_scalar_difference),
        "threshold_decimal": baseline_thresholds["scaled_residual_scalar_absolute_difference"],
        "passed": True,
    }

    states: list[Mapping[str, Any]] = []
    materialized: dict[tuple[str, str, float], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for profile in PROFILE_ORDER:
        for corner_name in CORNER_ORDER:
            attempt = by_key[(profile, corner_name)]
            corner = corners.get(corner_name)
            for fraction in FRACTION_ORDER:
                sid = state_id(profile, corner_name, fraction)
                if corner is None or fraction not in attempt.xi_by_fraction:
                    cause = attempt.failure_id or fresh.fresh_failure_id or "state:unavailable"
                    states.append({
                        "state_id": sid, "profile": profile, "corner": corner_name,
                        "fraction": fraction, "status": "NOT_EVALUATED",
                        "causal_failure_id": cause,
                    })
                    continue
                xi = np.asarray(attempt.xi_by_fraction[fraction], dtype=np.clongdouble)
                w = np.asarray(corner.node.saddle_w, dtype=np.clongdouble) + np.asarray(corner.node.factor, dtype=np.longdouble) @ xi
                z = np.asarray(setup.context.scales5, dtype=np.longdouble) * w
                finite_array(z, role=f"{sid}:physical_z")
                materialized[(profile, corner_name, fraction)] = (xi, w, z)
                states.append({
                    "state_id": sid, "profile": profile, "corner": corner_name,
                    "fraction": fraction, "status": "EVALUATED",
                    "xi": xi, "state_w5": w, "physical_state_z": z,
                    "xi_norm_decimal": P55.ld_text(np.linalg.norm(xi)),
                    "state_materialization": "scales5*(selected_center+common_factor@xi)",
                })
    if len(states) != 40:
        raise InvalidRun("fraction-state ledger count drift")

    endpoints: list[Mapping[str, Any]] = []
    residuals: list[Mapping[str, Any]] = []
    scalar_gates: list[Mapping[str, Any]] = []
    overall_gates: list[Mapping[str, Any]] = []
    identities: list[Mapping[str, Any]] = []
    endpoint_arrays: dict[tuple[str, str], np.ndarray] = {}
    residual_arrays: dict[tuple[str, str], np.ndarray] = {}
    gate_vectors: dict[tuple[str, str], tuple[bool, bool, bool]] = {}
    gate_contract = manifest["residual_and_gate_contract"]
    thresholds = gate_contract["target_gates"]
    identity_threshold = decimal(gate_contract["identity_max_abs_threshold"], label="residual identity threshold")
    for profile in PROFILE_ORDER:
        for corner_name in CORNER_ORDER:
            key = (profile, corner_name)
            endpoint = materialized.get((profile, corner_name, 1.0))
            if endpoint is None:
                cause = by_key[key].failure_id or fresh.fresh_failure_id or "endpoint:unavailable"
                endpoints.append({"endpoint_id": f"endpoint:{profile}:{corner_name}", "profile": profile, "corner": corner_name, "status": "NOT_EVALUATED", "causal_failure_id": cause})
                residuals.append({"residual_id": f"residual:{profile}:{corner_name}", "profile": profile, "corner": corner_name, "status": "NOT_EVALUATED", "causal_failure_id": cause})
                for gate in ("saved_endpoint_relative", "scaled_residual_absolute", "saved_residual_scalar_difference"):
                    scalar_gates.append({"gate_id": f"gate:{profile}:{corner_name}:{gate}", "profile": profile, "corner": corner_name, "gate": gate, "status": "NOT_EVALUATED", "causal_failure_id": cause})
                overall_gates.append({"overall_id": f"overall:{profile}:{corner_name}", "profile": profile, "corner": corner_name, "status": "NOT_EVALUATED", "causal_failure_id": cause})
                identities.append({"identity_id": f"identity:{profile}:{corner_name}", "profile": profile, "corner": corner_name, "status": "NOT_EVALUATED", "causal_failure_id": cause})
                continue
            z = np.asarray(endpoint[2], dtype=np.clongdouble)
            endpoint_arrays[key] = z
            comparison = P55.directed_state_metric(z, saved_z)
            endpoint_pass = decimal(comparison["relative_decimal"], label="endpoint gate") <= decimal(thresholds["saved_endpoint_relative_max"], label="endpoint gate threshold")
            endpoints.append({
                "endpoint_id": f"endpoint:{profile}:{corner_name}", "profile": profile,
                "corner": corner_name, "status": "PASS" if endpoint_pass else "NONPASS",
                "physical_state_z": z, "saved_endpoint_z": saved_z,
                "threshold_decimal": thresholds["saved_endpoint_relative_max"],
                "passed": endpoint_pass, **comparison,
            })
            residual = residual_vector(setup, gamma, z, role=f"{profile}:{corner_name}:residual")
            residual_arrays[key] = residual
            residual_max = max_decimal(residual)
            residual_pass = decimal(residual_max, label="corner residual") <= decimal(thresholds["scaled_residual_max_abs_max"], label="residual threshold")
            scalar_difference = abs(decimal(residual_max, label="corner residual") - decimal(saved_scalar, label="saved residual scalar"))
            scalar_pass = scalar_difference <= decimal(thresholds["saved_residual_scalar_absolute_difference_max"], label="saved scalar difference threshold")
            residuals.append({
                "residual_id": f"residual:{profile}:{corner_name}", "profile": profile,
                "corner": corner_name, "status": "PASS" if residual_pass and scalar_pass else "NONPASS",
                "vector_interleaved": residual, "maximum_decimal": residual_max,
                "absolute_pass": residual_pass,
                "saved_scalar_decimal": saved_scalar,
                "saved_scalar_absolute_difference_decimal": str(scalar_difference),
                "saved_scalar_difference_pass": scalar_pass,
                "construction": "interleaved((gamma.astype(complex128)-z.astype(complex128))/scales.astype(float64))",
            })
            gate_vector = (endpoint_pass, residual_pass, scalar_pass)
            gate_vectors[key] = gate_vector
            for gate, passed, value, threshold in (
                ("saved_endpoint_relative", endpoint_pass, comparison["relative_decimal"], thresholds["saved_endpoint_relative_max"]),
                ("scaled_residual_absolute", residual_pass, residual_max, thresholds["scaled_residual_max_abs_max"]),
                ("saved_residual_scalar_difference", scalar_pass, str(scalar_difference), thresholds["saved_residual_scalar_absolute_difference_max"]),
            ):
                scalar_gates.append({
                    "gate_id": f"gate:{profile}:{corner_name}:{gate}", "profile": profile,
                    "corner": corner_name, "gate": gate, "status": "PASS" if passed else "NONPASS",
                    "value_decimal": value, "threshold_decimal": threshold, "passed": passed,
                })
            overall_pass = all(gate_vector)
            overall_gates.append({
                "overall_id": f"overall:{profile}:{corner_name}", "profile": profile,
                "corner": corner_name, "status": "PASS" if overall_pass else "NONPASS",
                "ordered_gate_names": ["saved_endpoint_relative", "scaled_residual_absolute", "saved_residual_scalar_difference"],
                "ordered_gate_vector": list(gate_vector), "corner_target_pass": overall_pass,
            })

            # Cast both endpoints before subtraction.  This must not be a
            # longdouble-first difference followed by a cast.
            endpoint_difference_c128 = np.asarray(z, dtype=np.complex128) - np.asarray(saved_z, dtype=np.complex128)
            rhs_complex = -endpoint_difference_c128 / np.asarray(setup.context.scales5, dtype=np.float64)
            identity_rhs = np.asarray(setup.p51.interleaved(rhs_complex), dtype=float)
            identity_lhs = np.asarray(residual - saved_residual, dtype=float)
            closure = identity_lhs - identity_rhs
            closure_max = max_decimal(closure)
            if decimal(closure_max, label="saved endpoint residual identity") > identity_threshold:
                raise InvalidRun(f"saved endpoint residual identity failed: {profile}:{corner_name}")
            absolute_identity_lhs = np.abs(identity_lhs)
            dominant = int(np.argmax(absolute_identity_lhs))
            coordinate = dominant // 2
            global_maximum = float(np.max(absolute_identity_lhs))
            T_maximum = float(np.max(absolute_identity_lhs[16:18]))
            identities.append({
                "identity_id": f"identity:{profile}:{corner_name}", "profile": profile,
                "corner": corner_name, "status": "PASS",
                "residual_difference_lhs": identity_lhs,
                "negative_scaled_endpoint_difference_rhs": identity_rhs,
                "closure_vector": closure, "closure_max_abs_decimal": closure_max,
                "threshold_decimal": gate_contract["identity_max_abs_threshold"],
                "dominant_residual_difference": {
                    "interleaved_index": dominant,
                    "coordinate_index": coordinate,
                    "coordinate_label": COORDINATE_LABELS[coordinate],
                    "part": "real" if dominant % 2 == 0 else "imaginary",
                    "value_decimal": P55.ld_text(identity_lhs[dominant]),
                    "scale_decimal": P55.ld_text(np.asarray(setup.context.scales5, dtype=np.longdouble)[coordinate]),
                },
                "T_component": {
                    "physical_endpoint_difference_real_decimal": P55.ld_text(endpoint_difference_c128[8].real),
                    "physical_endpoint_difference_imag_decimal": P55.ld_text(endpoint_difference_c128[8].imag),
                    "residual_difference_real_decimal": P55.ld_text(identity_lhs[16]),
                    "residual_difference_imag_decimal": P55.ld_text(identity_lhs[17]),
                    "scale_decimal": P55.ld_text(np.asarray(setup.context.scales5, dtype=np.longdouble)[8]),
                    "attains_maximum": T_maximum == global_maximum,
                },
            })
    if not (len(endpoints) == 8 and len(residuals) == 8 and len(scalar_gates) == 24 and len(overall_gates) == 8 and len(identities) == 8):
        raise InvalidRun("endpoint/residual/gate ledger count drift")

    baseline = build_baseline_ledger(
        selected, fresh, by_key, materialized, endpoint_arrays, residual_arrays,
        gate_vectors, manifest,
    )
    effects = build_effect_ledgers(endpoint_arrays, residual_arrays, setup, manifest, attempts)
    stability = build_stability_ledgers(endpoint_arrays, residual_arrays, gate_vectors, attempts, manifest)
    return Ledgers(states, endpoints, residuals, scalar_gates, overall_gates, identities, effects, stability, baseline, saved_residual_record)


def build_baseline_ledger(
    selected: SelectedTarget,
    fresh: FreshCalculation,
    attempts: Mapping[tuple[str, str], AttemptRuntime],
    materialized: Mapping[tuple[str, str, float], tuple[np.ndarray, np.ndarray, np.ndarray]],
    endpoints: Mapping[tuple[str, str], np.ndarray],
    residuals: Mapping[tuple[str, str], np.ndarray],
    gate_vectors: Mapping[tuple[str, str], tuple[bool, bool, bool]],
    manifest: Mapping[str, Any],
) -> Mapping[str, Any]:
    key = ("primary", "P50_center__P50_launch")
    baseline = manifest["phase55_baseline_contract"]
    thresholds = baseline["baseline_reproduction_thresholds"]
    attempt = attempts[key]
    state_records: list[Mapping[str, Any]] = []
    all_states_pass = True
    for fraction, reference in zip(FRACTION_ORDER, selected.phase55_states, strict=True):
        state = materialized.get((key[0], key[1], fraction))
        if state is None:
            all_states_pass = False
            state_records.append({"fraction": fraction, "status": "NOT_EVALUATED", "causal_failure_id": attempt.failure_id})
            continue
        comparison = P55.directed_state_metric(state[2], reference)
        passed = decimal(comparison["relative_decimal"], label="Phase55 state reproduction") <= decimal(thresholds["all_five_physical_states_relative_max"], label="Phase55 state threshold")
        all_states_pass = all_states_pass and passed
        state_records.append({"fraction": fraction, "status": "PASS" if passed else "NONPASS", "passed": passed, "threshold_decimal": thresholds["all_five_physical_states_relative_max"], **comparison})
    endpoint = endpoints.get(key)
    residual = residuals.get(key)
    endpoint_comparison = None if endpoint is None else P55.directed_state_metric(endpoint, selected.phase55_states[-1])
    endpoint_pass = bool(endpoint_comparison is not None and decimal(endpoint_comparison["relative_decimal"], label="Phase55 endpoint reproduction") <= decimal(thresholds["endpoint_relative_to_phase55_primary"], label="Phase55 endpoint threshold"))
    endpoint_to_saved = None if endpoint is None else P55.directed_state_metric(
        endpoint, selected.target.saved_endpoint_z
    )
    endpoint_scalar_pass = bool(
        endpoint_to_saved is not None
        and abs(
            decimal(endpoint_to_saved["relative_decimal"], label="current endpoint-to-saved")
            - decimal(baseline["expected_endpoint_relative_to_saved_decimal"], label="expected endpoint-to-saved")
        )
        <= decimal(thresholds["scaled_residual_scalar_absolute_difference"], label="endpoint scalar reproduction threshold")
    )
    residual_difference = None if residual is None else max_decimal(np.asarray(residual) - np.asarray(selected.phase55_residual))
    residual_vector_pass = bool(residual_difference is not None and decimal(residual_difference, label="Phase55 residual vector reproduction") <= decimal(thresholds["scaled_residual_vector_max_abs_difference"], label="Phase55 residual vector threshold"))
    current_residual_max = None if residual is None else max_decimal(residual)
    current_saved_difference = None if current_residual_max is None else str(abs(decimal(current_residual_max, label="current residual") - decimal(selected.target.saved_scaled_residual, label="saved residual")))
    expected_residual_max = baseline["expected_scaled_residual_max_abs_decimal"]
    expected_saved_difference = baseline["expected_saved_scalar_absolute_difference_decimal"]
    scalar_pass = bool(
        current_residual_max is not None
        and abs(decimal(current_residual_max, label="current residual") - decimal(expected_residual_max, label="expected residual")) <= decimal(thresholds["scaled_residual_scalar_absolute_difference"], label="scalar threshold")
        and abs(decimal(current_saved_difference, label="current saved difference") - decimal(expected_saved_difference, label="expected saved difference")) <= decimal(thresholds["scaled_residual_scalar_absolute_difference"], label="scalar threshold")
    )
    expected_gate = baseline["required_primary_gate_vector"]
    current_gate = gate_vectors.get(key)
    gate_mapping = None if current_gate is None else {
        "saved_endpoint_relative_pass": current_gate[0],
        "scaled_residual_absolute_pass": current_gate[1],
        "saved_residual_scalar_difference_pass": current_gate[2],
        "overall_target_pass": all(current_gate),
    }
    gate_pass = gate_mapping == expected_gate
    nfev_pass = int(attempt.record.get("nfev", -1)) == int(baseline["expected_primary_nfev"])
    initial_digest_pass = fresh.p50_baseline_launch_passed
    passed = bool(
        attempt.status == "PASS" and initial_digest_pass and nfev_pass and all_states_pass
        and endpoint_pass and endpoint_scalar_pass and residual_vector_pass and scalar_pass and gate_pass
    )
    return {
        "status": "PASS" if passed else "NONPASS",
        "passed": passed,
        "Phase55_launch_reproduction": fresh.p50_baseline_launch_comparison,
        "initial_xi_digest_and_launch_structure_pass": initial_digest_pass,
        "nfev_pass": nfev_pass,
        "expected_nfev": baseline["expected_primary_nfev"],
        "observed_nfev": attempt.record.get("nfev"),
        "all_five_state_comparisons": state_records,
        "all_five_states_pass": all_states_pass,
        "endpoint_comparison": endpoint_comparison,
        "endpoint_pass": endpoint_pass,
        "endpoint_to_saved_comparison": endpoint_to_saved,
        "expected_endpoint_relative_to_saved_decimal": baseline["expected_endpoint_relative_to_saved_decimal"],
        "endpoint_to_saved_scalar_reproduction_pass": endpoint_scalar_pass,
        "residual_vector_max_abs_difference_decimal": residual_difference,
        "residual_vector_pass": residual_vector_pass,
        "observed_residual_max_abs_decimal": current_residual_max,
        "observed_saved_scalar_absolute_difference_decimal": current_saved_difference,
        "scalar_reproduction_pass": scalar_pass,
        "required_gate_vector": expected_gate,
        "observed_gate_vector": gate_mapping,
        "gate_vector_pass": gate_pass,
    }


def build_effect_ledgers(
    endpoints: Mapping[tuple[str, str], np.ndarray],
    residuals: Mapping[tuple[str, str], np.ndarray],
    setup: Any,
    manifest: Mapping[str, Any],
    attempts: Sequence[AttemptRuntime],
) -> list[Mapping[str, Any]]:
    output: list[Mapping[str, Any]] = []
    threshold_text = manifest["factorial_contract"]["effect_ledger_per_profile"]["full_vector_reconstruction_identity_max_abs"]
    threshold = decimal(threshold_text, label="factorial closure threshold")
    by_attempt = {(item.profile, item.corner): item for item in attempts}
    names = {
        "00": "P50_center__P50_launch",
        "01": "P50_center__fresh_launch",
        "10": "fresh_center__P50_launch",
        "11": "fresh_center__fresh_launch",
    }
    for profile in PROFILE_ORDER:
        keys = {code: (profile, corner) for code, corner in names.items()}
        if not all(key in endpoints and key in residuals for key in keys.values()):
            cause = next((by_attempt[key].failure_id for key in keys.values() if by_attempt[key].failure_id), "factorial:unavailable")
            for effect in ("center", "launch", "interaction"):
                output.append({"effect_id": f"effect:{profile}:{effect}", "profile": profile, "effect": effect, "status": "NOT_EVALUATED", "causal_failure_id": cause})
            continue
        z = {code: np.asarray(endpoints[key], dtype=np.clongdouble) for code, key in keys.items()}
        r = {code: np.asarray(residuals[key], dtype=np.longdouble) for code, key in keys.items()}
        z_effects = {"center": z["10"] - z["00"], "launch": z["01"] - z["00"], "interaction": z["11"] - z["10"] - z["01"] + z["00"]}
        r_effects = {"center": r["10"] - r["00"], "launch": r["01"] - r["00"], "interaction": r["11"] - r["10"] - r["01"] + r["00"]}
        z_closure = (z["11"] - z["00"]) - (z_effects["center"] + z_effects["launch"] + z_effects["interaction"])
        r_closure = (r["11"] - r["00"]) - (r_effects["center"] + r_effects["launch"] + r_effects["interaction"])
        z_max = max_decimal(z_closure)
        r_max = max_decimal(r_closure)
        if decimal(z_max, label="endpoint factorial closure") > threshold or decimal(r_max, label="residual factorial closure") > threshold:
            raise InvalidRun(f"factorial reconstruction identity failed: {profile}")
        for effect in ("center", "launch", "interaction"):
            endpoint_effect = z_effects[effect]
            residual_effect = r_effects[effect]
            dominant = int(np.argmax(np.abs(residual_effect)))
            output.append({
                "effect_id": f"effect:{profile}:{effect}", "profile": profile,
                "effect": effect, "status": "PASS",
                "endpoint_effect_vector": endpoint_effect,
                "endpoint_effect_norm_decimal": P55.ld_text(np.linalg.norm(endpoint_effect)),
                "endpoint_effect_max_abs_decimal": max_decimal(endpoint_effect),
                "scaled_residual_effect_vector": residual_effect,
                "scaled_residual_effect_norm_decimal": P55.ld_text(np.linalg.norm(residual_effect)),
                "scaled_residual_effect_max_abs_decimal": max_decimal(residual_effect),
                "endpoint_reconstruction_closure_max_abs_decimal": z_max,
                "residual_reconstruction_closure_max_abs_decimal": r_max,
                "closure_threshold_decimal": threshold_text,
                "dominant_residual_component": {"interleaved_index": dominant, "coordinate_index": dominant // 2, "coordinate_label": COORDINATE_LABELS[dominant // 2], "part": "real" if dominant % 2 == 0 else "imaginary"},
                "T_components": {
                    "endpoint_real_decimal": P55.ld_text(endpoint_effect[8].real),
                    "endpoint_imag_decimal": P55.ld_text(endpoint_effect[8].imag),
                    "residual_real_decimal": P55.ld_text(residual_effect[16]),
                    "residual_imag_decimal": P55.ld_text(residual_effect[17]),
                    "scale_decimal": P55.ld_text(np.asarray(setup.context.scales5, dtype=np.longdouble)[8]),
                },
                "causal_or_dominance_label_assigned": False,
            })
    if len(output) != 6:
        raise InvalidRun("factorial effect ledger count drift")
    return output


def build_stability_ledgers(
    endpoints: Mapping[tuple[str, str], np.ndarray],
    residuals: Mapping[tuple[str, str], np.ndarray],
    gate_vectors: Mapping[tuple[str, str], tuple[bool, bool, bool]],
    attempts: Sequence[AttemptRuntime],
    manifest: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    output: list[Mapping[str, Any]] = []
    contract = manifest["residual_and_gate_contract"]["profile_stability"]
    attempt_map = {(item.profile, item.corner): item for item in attempts}
    for corner in CORNER_ORDER:
        primary = ("primary", corner)
        refined = ("refined_diagnostic", corner)
        if primary not in endpoints or refined not in endpoints or primary not in residuals or refined not in residuals:
            cause = attempt_map[primary].failure_id or attempt_map[refined].failure_id or "stability:unavailable"
            output.append({"stability_id": f"stability:{corner}", "corner": corner, "status": "NOT_EVALUATED", "causal_failure_id": cause})
            continue
        endpoint_metric = P55.directed_state_metric(endpoints[refined], endpoints[primary])
        residual_difference = max_decimal(np.asarray(residuals[refined]) - np.asarray(residuals[primary]))
        gate_equal = gate_vectors[primary] == gate_vectors[refined]
        p50_nonpass = True if corner != "P50_center__P50_launch" else (not all(gate_vectors[primary]) and not all(gate_vectors[refined]))
        endpoint_pass = decimal(endpoint_metric["relative_decimal"], label="cross-profile endpoint") <= decimal(contract["endpoint_cross_profile_relative_difference_max"], label="cross-profile endpoint threshold")
        residual_pass = decimal(residual_difference, label="cross-profile residual") <= decimal(contract["scaled_residual_cross_profile_max_abs_difference_max"], label="cross-profile residual threshold")
        passed = bool(gate_equal and p50_nonpass and endpoint_pass and residual_pass)
        output.append({
            "stability_id": f"stability:{corner}", "corner": corner,
            "status": "PASS" if passed else "NONPASS", "passed": passed,
            "primary_gate_vector": list(gate_vectors[primary]),
            "refined_gate_vector": list(gate_vectors[refined]),
            "gate_vectors_equal": gate_equal,
            "P50_P50_target_NONPASS_both_profiles": p50_nonpass,
            "endpoint_cross_profile": endpoint_metric,
            "endpoint_threshold_decimal": contract["endpoint_cross_profile_relative_difference_max"],
            "endpoint_pass": endpoint_pass,
            "scaled_residual_cross_profile_max_abs_difference_decimal": residual_difference,
            "residual_threshold_decimal": contract["scaled_residual_cross_profile_max_abs_difference_max"],
            "residual_pass": residual_pass,
        })
    if len(output) != 4:
        raise InvalidRun("profile stability ledger count drift")
    return output


def required_global_nulls() -> Mapping[str, Any]:
    return {
        "historical_Phase51_classification_after": None,
        "historical_Phase53_classification_after": None,
        "historical_Phase55_classification_after": None,
        "continuation_reclassification": None,
        "full_semantic_replay_performed": False,
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


def ragnarok_containment() -> Mapping[str, Any]:
    """Operational closeout overlay; it does not alter the frozen scientific classifier."""
    return {
        "schema": "ice-ragnarok-circuit-breaker/v1",
        "decision_path": "docs/decisions/ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md",
        "operational_state": "BOUNDED_PAUSE",
        "continuation_route": "KILL",
        "kill_scope": "PHASE_51_TO_56_SAVED_BACKEND_AND_RECONSTRUCTED_LAUNCH_RECONCILIATION",
        "next_phase": None,
        "full_replay_authorized": False,
        "phase57_authorized": False,
        "candidate_label_is_execution_authorization": False,
        "scientific_route": "OPEN",
        "gate1": "OPEN_PARTIAL_PROGRESS",
    }


def evaluator_convention_guard(setup: Any) -> Mapping[str, Any]:
    rhs_source = inspect.getsource(P55.ScheduleEvaluator.rhs)
    gradient_source = inspect.getsource(P55.ScheduleEvaluator.dimension_gradient)
    native_stages_source = inspect.getsource(setup.p52.native_stages)
    residual_source = inspect.getsource(residual_vector)
    effect_source = inspect.getsource(build_effect_ledgers)
    record = {
        "ScheduleEvaluator_rhs_source_sha256": sha256_bytes(rhs_source.encode("utf-8")),
        "ScheduleEvaluator_dimension_gradient_source_sha256": sha256_bytes(gradient_source.encode("utf-8")),
        "Phase52_native_stages_source_sha256": sha256_bytes(native_stages_source.encode("utf-8")),
        "Phase56_residual_vector_source_sha256": sha256_bytes(residual_source.encode("utf-8")),
        "Phase56_effect_ledger_source_sha256": sha256_bytes(effect_source.encode("utf-8")),
        "EL_long_fixed_array_sum_present": "fixed_array_sum" in gradient_source,
        "ordinary_transpose_state_map_present": "slot.node.factor.T" in native_stages_source,
        "conjugate_transpose_absent": ".conj().T" not in native_stages_source and ".conjugate().T" not in native_stages_source,
        "one_completed_complex128_solver_boundary_cast": rhs_source.count("dtype=np.complex128") == 1,
        "one_outer_minus_conjugation_consumed": native_stages_source.count("-np.conjugate(contracted)") == 1 and '"outer_minus_conjugation"' in rhs_source,
        "residual_casts_both_operands_before_subtraction": "np.asarray(gamma, dtype=np.complex128)" in residual_source and "np.asarray(z, dtype=np.complex128)" in residual_source,
        "effect_definitions_present": all(token in effect_source for token in ('"center"', '"launch"', '"interaction"')),
        "Phase53_exact_action_gradient_Hessian_identity": setup.symbolic_ledger["phase53_exact_identity"],
    }
    record["passed"] = bool(
        record["EL_long_fixed_array_sum_present"]
        and record["ordinary_transpose_state_map_present"]
        and record["conjugate_transpose_absent"]
        and record["one_completed_complex128_solver_boundary_cast"]
        and record["one_outer_minus_conjugation_consumed"]
        and record["residual_casts_both_operands_before_subtraction"]
        and record["effect_definitions_present"]
        and all(all(values.values()) for values in record["Phase53_exact_action_gradient_Hessian_identity"].values())
    )
    if not record["passed"]:
        raise InvalidRun("Phase56 evaluator/convention source guard failed")
    return record


def exact_checks(
    contract: Contract,
    bundle: InputBundle,
    selected: SelectedTarget,
    preenumeration: Mapping[str, Any],
    convention: Mapping[str, Any],
    *,
    authoritative: bool,
    counters: Mapping[str, int],
    corner_records: Sequence[Mapping[str, Any]] | None,
    attempts: Sequence[AttemptRuntime] | None,
) -> None:
    conditions = [
        (
            len(bundle.observed) == 29
            and bundle.runner_guard["manifest_commit_blob_guard"]["commit_blob_matches"],
            "29 recursive pins, commits, blobs, strict JSON/self-digests, runtime, and runner binding validate",
            {"consumed_path_count": len(bundle.observed), "runner_guard": bundle.runner_guard},
        ),
        (
            float(selected.target.lambda_value) == LAMBDA_VALUE
            and selected.target.parameters.shape == (18,)
            and selected.target.p50_saddle.shape == (9,)
            and selected.target.saved_endpoint_z.shape == (9,),
            "one phi_plus lambda-half root, P50 saddle, endpoint, saddle summary, and Phase55 baseline subtree set is exact",
            {"source": SOURCE, "lambda": LAMBDA_VALUE},
        ),
        (
            counters.get("allowed_fresh_saddle_root", 0) == (1 if authoritative else 0)
            and counters.get("saddle_cache_miss", 0) == (1 if authoritative else 0)
            and all(counters.get(key, 0) == 0 for key in ("forbidden_root", "Gamma_K_root_or_continuation", "inherited_integrate_k", "tangent_or_event", "finite_difference", "reflection", "action_or_first_cap")),
            "authoritative mode permits one fresh saddle solve and no other root/replay route; validate-only permits none",
            {"guard_counters": dict(counters)},
        ),
        (
            tuple(preenumeration["payload"]["corner_order"]) == CORNER_ORDER
            and (corner_records is None or len(corner_records) == 4),
            "two centers, two Hessian-derived launches, and four ordered factorial corners retain the frozen definitions",
            {"corner_order": list(CORNER_ORDER)},
        ),
        (
            preenumeration["counts"]["ODE_attempt_slots"] == 8
            and preenumeration["counts"]["fraction_state_slots"] == 40
            and (attempts is None or len(attempts) == 8)
            and counters.get("runner_solve_ivp", 0) in ((0, 8) if authoritative else (0,)),
            "eight profile/corner attempts and forty ordered fraction slots are preenumerated and retained",
            {"preenumerated_counts": preenumeration["counts"]},
        ),
        (
            convention["passed"],
            "EL_long fixed summation, ordinary transpose, one outer conjugation, and one completed solver-boundary cast remain bound",
            convention,
        ),
        (
            tuple(COORDINATE_LABELS)[8] == "T"
            and manifest_effect_definitions_valid(bundle.manifest),
            "full-vector residual identities and center/launch/interaction definitions retain T as physical component 8",
            {"coordinate_labels": list(COORDINATE_LABELS), "T_interleaved_indices": [16, 17]},
        ),
        (
            tuple(bundle.manifest["classification_precedence"]) == CLASSIFICATION_PRECEDENCE
            and bundle.manifest["required_outputs"]["historical_Phase53_classification_preserved_as"] == "PHI_PLUS_M5_ELEMENT_LOCAL_FULL_CONTINUATION_REPLAY_INCONCLUSIVE"
            and bundle.manifest["required_outputs"]["historical_Phase55_classification_preserved_as"] == "P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS"
            and {
                key: bundle.manifest["required_outputs"].get(key)
                for key in required_global_nulls()
            }
            == required_global_nulls()
            and bundle.manifest["scope"]["calculation_workbench_only"] is True
            and bundle.manifest["scope"]["phase56_is_diagnostic_only"] is True,
            "historical classifications, precedence, calculation-workbench scope, and every global/physics/TOE null remain immutable",
            {"classification_precedence": list(CLASSIFICATION_PRECEDENCE), "required_global_nulls": required_global_nulls()},
        ),
    ]
    for check_id, (passed, statement, details) in zip(EXACT_CHECK_IDS, conditions, strict=True):
        contract.add_exact(check_id, passed, statement, details)
    if not all(record["passed"] for record in contract.exact):
        raise InvalidRun("one or more Phase56 exact checks failed")


def manifest_effect_definitions_valid(manifest: Mapping[str, Any]) -> bool:
    definitions = manifest["factorial_contract"]["effect_ledger_per_profile"]
    return bool(
        definitions["center_effect"] == "z_fresh_center__P50_launch - z_P50_center__P50_launch"
        and definitions["launch_effect"] == "z_P50_center__fresh_launch - z_P50_center__P50_launch"
        and "z_fresh_center__fresh_launch" in definitions["interaction"]
        and set(definitions["applies_independently_to"]) == {"endpoint complex vector", "scaled-residual interleaved real vector"}
    )


def execution_topology(
    *, validate_only: bool, counters: Mapping[str, int], attempts: Sequence[AttemptRuntime] | None
) -> Mapping[str, Any]:
    return {
        "source_count": 1,
        "lambda_count": 1,
        "saved_root_count": 1,
        "pinned_P50_center_count": 1,
        "fresh_saddle_solve_slot_count": 1,
        "newton_prediction_slot_count": 1,
        "center_record_count": 2,
        "launch_record_count": 2,
        "factorial_corner_record_count": 4,
        "solver_profile_record_count": 2,
        "ODE_attempt_slot_count": 8,
        "fraction_state_slot_count": 40,
        "actual_root_call_count": counters.get("allowed_fresh_saddle_root", 0),
        "actual_solve_ivp_call_count": counters.get("runner_solve_ivp", 0),
        "validate_only": validate_only,
        "Gamma_K_root_solve_count": 0,
        "continuation_or_replay_count": 0,
        "tangent_ODE_count": 0,
        "event_integration_count": 0,
        "finite_difference_count": 0,
        "reflection_count": 0,
        "action_or_first_cap_count": 0,
        "attempt_statuses": [] if attempts is None else [item.status for item in attempts],
        "guard_counters": dict(counters),
    }


def base_result(
    bundle: InputBundle,
    selected: SelectedTarget,
    setup: Any,
    preenumeration: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "phase": 56,
        "source": SOURCE,
        "lambda": LAMBDA_VALUE,
        "declared_result_path": bundle.manifest["required_outputs"]["result_path"],
        "manifest_identity": {
            "commit": MANIFEST_COMMIT,
            "blob_oid": MANIFEST_BLOB_OID,
            "sha256": MANIFEST_SHA256,
            "size_bytes": MANIFEST_SIZE_BYTES,
        },
        "runner_binding": bundle.runner_guard,
        "runtime": bundle.runtime,
        "input_pin_validation": {"consumed_path_count": len(bundle.observed), "records": bundle.observed},
        "selected_target": {
            "parameters": selected.target.parameters,
            "p50_saddle": selected.target.p50_saddle,
            "saved_endpoint_z": selected.target.saved_endpoint_z,
            "saved_scaled_residual_max_abs_decimal": selected.target.saved_scaled_residual,
            "phase53_saddle_summary": selected.phase53_saddle_summary,
        },
        "symbolic_and_evaluator_binding": {
            "science_source": SOURCE,
            "phase53_projection_sha256": setup.symbolic_ledger["phase53_projection_sha256"],
            "phase53_exact_identity": setup.symbolic_ledger["phase53_exact_identity"],
            "EL_long_only": True,
            "EL_std_ODE_count": 0,
        },
        "preenumerated_record_topology": preenumeration,
        "historical_Phase53_classification_preserved_as": "PHI_PLUS_M5_ELEMENT_LOCAL_FULL_CONTINUATION_REPLAY_INCONCLUSIVE",
        "historical_Phase55_classification_preserved_as": "P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS",
        "next_phase": None,
        "ragnarok_containment": ragnarok_containment(),
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
    }


def common_preflight(*, authoritative: bool) -> tuple[InputBundle, SelectedTarget, Any, Mapping[str, Any], Mapping[str, Any]]:
    progress("validating Phase56 manifest, Phase55 result, and 29 recursively pinned paths")
    bundle = validate_inputs(authoritative=authoritative)
    selected = select_target(bundle)
    progress("reconstructing the pinned Phase53 EL_long evaluator without a solve")
    try:
        setup = P55.build_static_setup(bundle.phase55_bundle)
    except Exception as error:
        raise InvalidRun(f"Phase55 static setup failed: {error}") from error
    if setup.context.label != SOURCE or setup.context._saddle_cache:
        raise InvalidRun("Phase56 source context/cache topology drift")
    setup.context.evaluator = setup.repaired
    preenumeration = preenumerated_topology(bundle.manifest)
    convention = evaluator_convention_guard(setup)
    return bundle, selected, setup, preenumeration, convention


def validation_placeholder_ledgers(
    preenumeration: Mapping[str, Any],
) -> Mapping[str, Any]:
    cause = "validate-only:authoritative_numerics_skipped"
    frozen = preenumeration["payload"]
    attempts = []
    states = []
    for profile in PROFILE_ORDER:
        for corner in CORNER_ORDER:
            attempts.append({"attempt_id": attempt_id(profile, corner), "profile": profile, "corner": corner, "status": "NOT_EVALUATED", "causal_failure_id": cause})
            for fraction in FRACTION_ORDER:
                states.append({"state_id": state_id(profile, corner, fraction), "profile": profile, "corner": corner, "fraction": fraction, "status": "NOT_EVALUATED", "causal_failure_id": cause})
    def placeholders(
        record_ids: Sequence[str], id_key: str
    ) -> list[Mapping[str, Any]]:
        return [
            {
                id_key: record_id,
                "status": "NOT_EVALUATED",
                "causal_failure_id": cause,
            }
            for record_id in record_ids
        ]
    return {
        "ODE_attempts": attempts,
        "fraction_states": states,
        "endpoints": placeholders(frozen["endpoint_ids"], "endpoint_id"),
        "scaled_residuals": placeholders(frozen["residual_ids"], "residual_id"),
        "scalar_target_gates": placeholders(frozen["scalar_gate_ids"], "gate_id"),
        "overall_corner_gates": placeholders(frozen["overall_gate_ids"], "overall_id"),
        "saved_endpoint_residual_identities": placeholders(
            frozen["residual_identity_ids"], "identity_id"
        ),
        "factorial_effects": placeholders(
            frozen["factorial_effect_ids"], "effect_id"
        ),
        "profile_stability": placeholders(
            frozen["profile_stability_ids"], "stability_id"
        ),
    }


def numerical_checks(
    contract: Contract,
    fresh: FreshCalculation,
    attempts: Sequence[AttemptRuntime],
    ledgers: Ledgers,
    manifest: Mapping[str, Any],
) -> Mapping[str, Any]:
    fresh_launch = fresh.launches["fresh"]
    saddle_launch_pass = bool(fresh.fresh_passed and fresh_launch.passed)
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[0],
        "PASS" if saddle_launch_pass else "NONPASS",
        "the one fresh Phase53-algorithm saddle and its Hessian-derived launch satisfy every frozen finite gate",
        {"fresh_saddle": fresh.fresh_record, "fresh_launch": fresh_launch.record},
    )
    newton_threshold = manifest["fresh_saddle_and_launch_contract"]["newton_prediction"]["required_linear_solve_residual_max_abs"]
    newton_pass = bool(
        fresh.newton_record.get("actual_comparison") is not None
        and decimal(fresh.newton_record["linear_solve_residual_max_abs_decimal"], label="Newton residual") <= decimal(newton_threshold, label="Newton threshold")
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[1],
        "PASS" if newton_pass else "NONPASS",
        "the static Newton prediction solves H_real delta=-g_real to the frozen residual while retaining its descriptive actual comparison",
        fresh.newton_record,
    )
    baseline_pass = bool(ledgers.baseline.get("passed"))
    primary_baseline_attempt = next(
        item
        for item in attempts
        if item.profile == "primary"
        and item.corner == "P50_center__P50_launch"
    )
    baseline_applicable = not primary_baseline_attempt.status.startswith(
        "NOT_ATTEMPTED"
    )
    baseline_causes = (
        [str(primary_baseline_attempt.failure_id)]
        if not baseline_applicable and primary_baseline_attempt.failure_id
        else []
    )
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[2],
        "PASS" if baseline_pass else "NONPASS",
        "the primary P50/P50 corner reproduces the pinned Phase55 launch, five states, endpoint, residuals, nfev, and gate vector",
        ledgers.baseline,
        baseline_causes,
        applicable=baseline_applicable,
        evaluated=baseline_applicable,
    )
    if all(item.status.startswith("NOT_ATTEMPTED") for item in attempts):
        ode_status = "NONPASS"
        ode_applicable = False
        ode_evaluated = False
        ode_causes = list(dict.fromkeys(str(item.failure_id) for item in attempts if item.failure_id))
    else:
        ode_status = "PASS" if all(item.status == "PASS" for item in attempts) else "NONPASS"
        ode_applicable = True
        ode_evaluated = True
        ode_causes = []
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[3], ode_status,
        "all eight profile/corner ODE attempts complete five finite samples with callback=nfev and xi norm below 40",
        {"attempt_count": len(attempts), "statuses": [item.status for item in attempts]},
        ode_causes,
        applicable=ode_applicable,
        evaluated=ode_evaluated,
    )
    ledger_records = [*ledgers.endpoints, *ledgers.residuals, *ledgers.scalar_gates, *ledgers.overall_gates]
    missing_ledgers = [record for record in ledger_records if record.get("status") == "NOT_EVALUATED"]
    gates_status = "NONPASS" if missing_ledgers else "PASS"
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[4], gates_status,
        "all eight endpoint/residual vectors, twenty-four scalar gates, and eight overall gate records are complete",
        {"endpoint_count": len(ledgers.endpoints), "residual_count": len(ledgers.residuals), "scalar_gate_count": len(ledgers.scalar_gates), "overall_gate_count": len(ledgers.overall_gates)},
        list(dict.fromkeys(str(item.get("causal_failure_id")) for item in missing_ledgers if item.get("causal_failure_id"))),
        applicable=not missing_ledgers,
        evaluated=not missing_ledgers,
    )
    stability_missing = [item for item in ledgers.stability if item.get("status") == "NOT_EVALUATED"]
    stability_status = "NONPASS" if stability_missing else ("PASS" if all(item.get("status") == "PASS" for item in ledgers.stability) else "NONPASS")
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[5], stability_status,
        "all four corners retain the same target-gate vector and remain within endpoint/residual cross-profile thresholds",
        {"records": ledgers.stability},
        list(dict.fromkeys(str(item.get("causal_failure_id")) for item in stability_missing if item.get("causal_failure_id"))),
        applicable=not stability_missing,
        evaluated=not stability_missing,
    )
    overall_index = {(item.get("profile"), item.get("corner")): item for item in ledgers.overall_gates}
    fresh_keys = [(profile, "fresh_center__fresh_launch") for profile in PROFILE_ORDER]
    if any(overall_index.get(key, {}).get("status") == "NOT_EVALUATED" for key in fresh_keys):
        recovery_status = "NONPASS"
        recovery_applicable = False
        recovery_evaluated = False
    else:
        recovery_status = "PASS" if all(overall_index[key].get("corner_target_pass") is True for key in fresh_keys) else "NONPASS"
        recovery_applicable = True
        recovery_evaluated = True
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[6], recovery_status,
        "the fresh/fresh corner passes all three unchanged target gates under both solver profiles",
        {"fresh_fresh_records": [overall_index.get(key) for key in fresh_keys]},
        applicable=recovery_applicable,
        evaluated=recovery_evaluated,
    )
    arithmetic_records = [*ledgers.identities, *ledgers.effects]
    arithmetic_missing = [item for item in arithmetic_records if item.get("status") == "NOT_EVALUATED"]
    arithmetic_status = "NONPASS" if arithmetic_missing else ("PASS" if all(item.get("status") == "PASS" for item in arithmetic_records) else "NONPASS")
    contract.add_numerical(
        NUMERICAL_CHECK_IDS[7], arithmetic_status,
        "saved-endpoint residual identities and both-profile center/launch/interaction reconstructions close with T conditioning retained",
        {"identity_count": len(ledgers.identities), "effect_count": len(ledgers.effects)},
        list(dict.fromkeys(str(item.get("causal_failure_id")) for item in arithmetic_missing if item.get("causal_failure_id"))),
        applicable=not arithmetic_missing,
        evaluated=not arithmetic_missing,
    )
    if tuple(record["id"] for record in contract.numerical) != NUMERICAL_CHECK_IDS:
        raise InvalidRun("Phase56 numerical check order drift")
    return {
        "fresh_saddle_and_launch_pass": saddle_launch_pass,
        "newton_linear_identity_pass": newton_pass,
        "Phase55_baseline_pass": baseline_pass,
        "all_eight_ODEs_pass": ode_status == "PASS",
        "gate_ledgers_complete": gates_status == "PASS",
        "profile_stability_pass": stability_status == "PASS",
        "fresh_fresh_both_profiles_pass": recovery_status == "PASS",
        "arithmetic_identities_pass": arithmetic_status == "PASS",
    }


def choose_classification(
    fresh: FreshCalculation,
    attempts: Sequence[AttemptRuntime],
    ledgers: Ledgers,
) -> str:
    if not fresh.phase_wide_prerequisite:
        return "P56_FRESH_SADDLE_OR_LAUNCH_RECONSTRUCTION_NONPASS"
    if ledgers.baseline.get("passed") is not True:
        return "P56_PHASE55_P50_BASELINE_NOT_REPRODUCED"
    if not all(item.status == "PASS" for item in attempts):
        return "P56_FACTORIAL_ODE_COMPLETION_OR_FLOW_NORM_NONPASS"
    if not all(item.get("status") == "PASS" for item in ledgers.stability):
        return "P56_LAMBDA_HALF_GATE_SOLVER_PROFILE_UNSTABLE"
    overall = {
        (item["profile"], item["corner"]): bool(item.get("corner_target_pass"))
        for item in ledgers.overall_gates
        if item.get("status") != "NOT_EVALUATED"
    }
    recovered = all(
        overall.get((profile, "fresh_center__fresh_launch"), False)
        for profile in PROFILE_ORDER
    )
    return (
        "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET"
        if recovered
        else "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_DOES_NOT_RECOVER_SAVED_LAMBDA_HALF_TARGET"
    )


def validation_only_result() -> Mapping[str, Any]:
    bundle, selected, setup, preenumeration, convention = common_preflight(authoritative=False)
    zero_counters = {key: 0 for key in TopologyGuard(setup).counters}
    contract = Contract()
    exact_checks(
        contract, bundle, selected, preenumeration, convention,
        authoritative=False, counters=zero_counters, corner_records=None, attempts=None,
    )
    cause = "validate-only:authoritative_numerics_skipped"
    for check_id in NUMERICAL_CHECK_IDS:
        contract.add_numerical(
            check_id, "NOT_EVALUATED",
            "predeclared; validate-only performs zero saddle/root and zero ODE evaluations",
            causal_failure_ids=[cause],
            applicable=False,
            evaluated=False,
        )
    placeholders = validation_placeholder_ledgers(preenumeration)
    rehash = post_rehash(bundle)
    result = base_result(bundle, selected, setup, preenumeration)
    result.update({
        "mode": "validate-only",
        "run_status": "VALIDATION_ONLY",
        "classification": None,
        "exact_checks": contract.exact,
        "numerical_checks": contract.numerical,
        "fresh_saddle": None,
        "newton_prediction": None,
        "launch_records": [
            {"label": label, "status": "NOT_EVALUATED", "causal_failure_id": cause}
            for label in LAUNCH_ORDER
        ],
        "factorial_corner_records": [
            {"corner": corner, "status": "NOT_EVALUATED", "causal_failure_id": cause}
            for corner in CORNER_ORDER
        ],
        "ODE_attempts": placeholders["ODE_attempts"],
        "ledgers": {key: value for key, value in placeholders.items() if key != "ODE_attempts"},
        "execution_topology": execution_topology(validate_only=True, counters=zero_counters, attempts=None),
        "post_evaluation_rehash": rehash,
        "classification_prerequisites": {"evaluated": False, "scientific_label_allowed": False},
        "qualified_later_full_replay_launch_policy_candidate": None,
        "computed_facts": [
            "29 recursive pins, one lambda-half target, the Phase53 EL_long evaluator, and every output slot were validated",
            "zero root and zero solve_ivp calls were made",
        ],
        "interpretation": "Validation-only selects no Phase56 scientific diagnostic label.",
    })
    P55.reject_numeric_identity_fields(result)
    return P55.with_self_digest(result)


def authoritative_result() -> Mapping[str, Any]:
    bundle, selected, setup, preenumeration, convention = common_preflight(authoritative=True)
    progress("running exactly one fresh lambda-half saddle solve and reconstructing both launches")
    with guarded_topology(setup) as guard:
        fresh = calculate_fresh_and_launches(setup, selected, bundle.manifest, guard)
        corners, corner_records = construct_corners(setup, fresh)
        if corners:
            progress("running the eight frozen EL_long profile/corner ODE attempts")
            attempts, evaluator = run_odes(setup, corners, selected, bundle.manifest, guard)
        else:
            cause = (
                fresh.launches["P50"].failure_id
                or fresh.fresh_failure_id
                or fresh.launches["fresh"].failure_id
                or "reconstruction:factorial_input_nonpass"
            )
            attempts = placeholder_attempts(cause)
            evaluator = P55.ScheduleEvaluator(setup)
        progress("building endpoint, residual, factorial-effect, and profile-stability ledgers")
        ledgers = build_ledgers(setup, selected, fresh, corners, attempts, bundle.manifest)
        guard.assert_forbidden_zero()
        counters = dict(guard.counters)
    if counters["runner_solve_ivp"] not in (0, 8):
        raise InvalidRun("authoritative solve_ivp call count outside frozen topology")
    if fresh.phase_wide_prerequisite and counters["runner_solve_ivp"] != 8:
        raise InvalidRun(
            "fresh prerequisite passed without the manifest-required eight solve_ivp calls"
        )
    progress("rehashing all 31 consumed/runner paths before classification")
    rehash = post_rehash(bundle)
    contract = Contract()
    exact_checks(
        contract, bundle, selected, preenumeration, convention,
        authoritative=True, counters=counters, corner_records=corner_records, attempts=attempts,
    )
    prerequisites = numerical_checks(contract, fresh, attempts, ledgers, bundle.manifest)
    classification = choose_classification(fresh, attempts, ledgers)
    candidate = (
        "fresh_Phase53_algorithm_center_and_launch"
        if classification == "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET"
        else None
    )
    result = base_result(bundle, selected, setup, preenumeration)
    result.update({
        "mode": "authoritative",
        "run_status": "VALID_RUN",
        "classification": classification,
        "exact_checks": contract.exact,
        "numerical_checks": contract.numerical,
        "P50_saddle_evaluation": fresh.p50_record,
        "fresh_saddle": fresh.fresh_record,
        "newton_prediction": fresh.newton_record,
        "launch_records": [fresh.launches[label].record for label in LAUNCH_ORDER],
        "factorial_corner_records": corner_records,
        "ODE_attempts": [item.record for item in attempts],
        "ODE_hot_loop_binding": {
            "backend": "EL_long",
            "callback_counts": evaluator.calls,
            "runner_solve_ivp_call_count": counters["runner_solve_ivp"],
            "EL_long_accumulation": "Phase53.fixed_array_sum_clongdouble",
            "sole_solver_boundary_output_cast": "complex128",
        },
        "ledgers": {
            "fraction_states": ledgers.states,
            "endpoints": ledgers.endpoints,
            "scaled_residuals": ledgers.residuals,
            "scalar_target_gates": ledgers.scalar_gates,
            "overall_corner_gates": ledgers.overall_gates,
            "saved_endpoint_residual_identities": ledgers.identities,
            "factorial_effects": ledgers.effects,
            "profile_stability": ledgers.stability,
            "Phase55_primary_baseline_reproduction": ledgers.baseline,
            "saved_endpoint_reconstructed_residual": ledgers.saved_residual,
        },
        "execution_topology": execution_topology(validate_only=False, counters=counters, attempts=attempts),
        "post_evaluation_rehash": rehash,
        "classification_prerequisites": prerequisites,
        "qualified_later_full_replay_launch_policy_candidate": candidate,
        "evaluation_order": [
            "one_P50_gradient_Hessian_and_Newton_prediction",
            "one_fresh_Phase53_algorithm_saddle_root",
            "P50_and_fresh_Hessian_launch_reconstruction",
            "primary_four_corner_ODEs_then_refined_four_corner_ODEs",
            "forty_fraction_states_and_eight_endpoint_residual_gate_sets",
            "two_profile_factorial_effects_and_four_profile_stability_records",
            "post_numerical_31_path_rehash",
            "classification_precedence_dispatch",
        ],
        "computed_facts": [
            "one fresh saddle solve and a fixed 2x2 center/launch factorial were evaluated at the saved phi_plus lambda-half root",
            "both solver profiles used only the coherent Phase53 element-local long state RHS",
            "full residual identities and center/launch/interaction vectors were retained without a post-observation dominance label",
        ],
        "interpretation": "This is a bounded finite-dimensional launch-provenance diagnostic, not a full replay, global cycle, physics, or TOE result.",
    })
    P55.reject_numeric_identity_fields(result)
    return P55.with_self_digest(result)


def invalid_result(error: BaseException, *, validate_only: bool) -> Mapping[str, Any]:
    cause = "invalid_run:validity_prerequisite_failure"
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 56,
        "mode": "validate-only" if validate_only else "authoritative",
        "run_status": "INVALID_RUN",
        "classification": "INVALID_RUN",
        "declared_result_path": "cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_RESULT.json",
        "error": {"type": type(error).__name__, "message": str(error), "failure_id": cause},
        "exact_checks": [
            {"id": check_id, "kind": "exact", "passed": False, "status": "FAIL", "evaluated": False, "statement": "not evaluated because a validity prerequisite failed", "causal_failure_id": cause}
            for check_id in EXACT_CHECK_IDS
        ],
        "numerical_checks": [
            {"id": check_id, "kind": "numerical", "passed": False, "status": "NOT_EVALUATED", "applicable": False, "evaluated": False, "statement": "not evaluated because the run is invalid", "causal_failure_ids": [cause]}
            for check_id in NUMERICAL_CHECK_IDS
        ],
        "execution_topology": None,
        "historical_Phase53_classification_preserved_as": "PHI_PLUS_M5_ELEMENT_LOCAL_FULL_CONTINUATION_REPLAY_INCONCLUSIVE",
        "historical_Phase55_classification_preserved_as": "P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS",
        "qualified_later_full_replay_launch_policy_candidate": None,
        "next_phase": None,
        "ragnarok_containment": ragnarok_containment(),
        "required_global_nulls": required_global_nulls(),
        **required_global_nulls(),
        "interpretation": "No scientific Phase56 label is permitted because a validity prerequisite failed.",
    }
    P55.reject_numeric_identity_fields(result)
    return P55.with_self_digest(result)


def emit_result(payload: Mapping[str, Any]) -> None:
    ready = P55.json_ready(payload)
    raw = json.dumps(ready, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    print(f"{RESULT_PREFIX}{raw}", flush=True)


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-only", action="store_true",
        help="validate all pins, evaluator bindings, and preenumerated slots with zero root/ODE calls",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        result = validation_only_result() if arguments.validate_only else authoritative_result()
    except Exception as error:
        traceback.print_exc(file=sys.stderr)
        emit_result(invalid_result(error, validate_only=arguments.validate_only))
        return 2
    emit_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
