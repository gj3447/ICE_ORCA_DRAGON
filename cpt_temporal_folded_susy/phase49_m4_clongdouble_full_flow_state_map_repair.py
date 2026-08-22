#!/usr/bin/env python3
"""Phase 49: clongdouble full-flow state-map repair control.

Source state formation, the generated Phase-41 gradient callable, the L.T
contraction, and outer minus-conjugation are evaluated together in NumPy
clongdouble.  The complete flow is projected once to complex128 at the DOP853
RHS boundary.  The program writes no files and performs no root search.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Mapping, Sequence

sys.dont_write_bytecode = True

import mpmath
import numpy as np
import scipy
import sympy
from mpmath import mp
from scipy.integrate import solve_ivp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent
INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_INPUTS.json"
)
PHASE42_INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE42_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase42_m4_fixed_root_tangent_disentanglement.py"
)
PHASE43_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase43_m4_high_precision_local_rhs_arbitration.py"
)
PHASE45_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_RESULT.json"
)
PHASE46_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE46_M4_U2_STATE_MAP_FD_AUDIT_RESULT.json"
)
PHASE47_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_RESULT.json"
)
PHASE48_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP_RESULT.json"
)

INPUT_COMMIT = "57d1431653e01969a0a136d7f847a63f81ea2daf"
INPUT_SHA256 = "ec97937fd4643b2d3ebfccc70ff82e4348ea92086b5b0588aec33bf24fdebcc5"
PHASE42_INPUT_SHA256 = (
    "1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6"
)
RESULT_SCHEMA = "ice-phase49-clongdouble-full-flow-state-map-repair/v1"
RESULT_PREFIX = "RESULT_JSON="


class InvalidRun(RuntimeError):
    """A frozen input, platform, retained reference, or solver invariant failed."""


def progress(message: str) -> None:
    print(f"[Phase49] {message}", file=sys.stderr, flush=True)


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


def load_unique_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise InvalidRun(f"duplicate JSON key in {path.name}: {key}")
            result[key] = value
        return result

    payload = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(
            InvalidRun(f"nonfinite JSON token in {path.name}: {token}")
        ),
    )
    if not isinstance(payload, dict):
        raise InvalidRun(f"top-level JSON is not an object: {path.name}")
    return payload, raw


def json_ready(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            array = np.asarray(value, dtype=np.complex128)
            return {
                "shape": list(array.shape),
                "complex128_pairs": [
                    [float(item.real), float(item.imag)]
                    for item in array.reshape(-1)
                ],
            }
        return np.asarray(value).tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return [float(value.real), float(value.imag)]
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise InvalidRun("attempted to retain a nonfinite float")
    return value


def canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        json_ready(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def verify_self_digest(payload: Mapping[str, Any], *, label: str) -> str:
    expected = str(payload.get("result_payload_sha256_without_self"))
    without = dict(payload)
    without.pop("result_payload_sha256_without_self", None)
    observed = hashlib.sha256(canonical_bytes(without)).hexdigest()
    if observed != expected:
        raise InvalidRun(f"{label} self-excluding digest mismatch")
    return observed


def validate_inputs(manifest: Mapping[str, Any]) -> dict[str, Any]:
    if sha256_path(INPUT_PATH) != INPUT_SHA256:
        raise InvalidRun("Phase49 input manifest hash drift")
    if manifest.get("schema") != (
        "ice-phase49-clongdouble-full-flow-state-map-repair-inputs/v1"
    ):
        raise InvalidRun("Phase49 input schema drift")
    if manifest.get("phase") != 49:
        raise InvalidRun("Phase49 input phase drift")
    scope = manifest["scope"]
    if scope["targets_in_order"] != ["shared_zero", "phi_plus", "a_plus"]:
        raise InvalidRun("Phase49 target order drift")
    if scope["central_difference_steps_in_order"] != [2.0e-6, 5.0e-7, 1.0e-7]:
        raise InvalidRun("Phase49 step order drift")
    if scope["perturbation_signs_in_order"] != [1, -1]:
        raise InvalidRun("Phase49 sign order drift")
    if scope["trajectory_sample_fractions_in_order"] != [0.0, 0.25, 0.5, 0.75, 1.0]:
        raise InvalidRun("Phase49 fraction order drift")
    observed: dict[str, Any] = {}
    for label, specification in manifest["pinned_inputs"].items():
        path = REPO_ROOT / str(specification["path"])
        digest = sha256_path(path)
        if digest != specification["sha256"]:
            raise InvalidRun(f"pinned input hash drift: {label}")
        observed[label] = {
            "path": specification["path"],
            "commit": specification["commit"],
            "sha256": digest,
        }
    return observed


def platform_contract(manifest: Mapping[str, Any]) -> dict[str, Any]:
    expected = manifest["fixed_platform_contract"]
    info = np.finfo(np.longdouble)
    observed = {
        "clongdouble_itemsize_bytes": int(np.dtype(np.clongdouble).itemsize),
        "longdouble_itemsize_bytes": int(np.dtype(np.longdouble).itemsize),
        "longdouble_mantissa_bits_excluding_implicit_bit": int(info.nmant),
        "longdouble_epsilon": str(info.eps),
    }
    tests = {
        "clongdouble_itemsize_matches": observed["clongdouble_itemsize_bytes"]
        == int(expected["numpy_clongdouble_itemsize_bytes"]),
        "longdouble_itemsize_matches": observed["longdouble_itemsize_bytes"]
        == int(expected["numpy_longdouble_itemsize_bytes"]),
        "longdouble_mantissa_matches": observed[
            "longdouble_mantissa_bits_excluding_implicit_bit"
        ]
        == int(expected["numpy_longdouble_mantissa_bits_excluding_implicit_bit"]),
        "longdouble_epsilon_matches": observed["longdouble_epsilon"]
        == str(expected["numpy_longdouble_epsilon"]),
    }
    return {"observed": observed, "tests": tests, "all_passed": all(tests.values())}


def decode_complex_record(value: Any, *, label: str) -> np.ndarray:
    if not isinstance(value, Mapping) or value.get("shape") != [7]:
        raise InvalidRun(f"{label}: complex-vector shape drift")
    pairs = value.get("complex128_pairs")
    if not isinstance(pairs, list) or len(pairs) != 7:
        raise InvalidRun(f"{label}: complex-pair count drift")
    output = np.empty(7, dtype=np.complex128)
    output.real = [float(pair[0]) for pair in pairs]
    output.imag = [float(pair[1]) for pair in pairs]
    if not np.all(np.isfinite(output)):
        raise InvalidRun(f"{label}: nonfinite complex vector")
    return output


def symmetric_relative(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left)
    b = np.asarray(right)
    denominator = max(
        float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1.0e-300
    )
    return float(np.linalg.norm(a - b) / denominator)


def phase41_plateau(first: np.ndarray, second: np.ndarray) -> float:
    return float(
        np.linalg.norm(np.asarray(first) - np.asarray(second))
        / max(float(np.linalg.norm(first)), 1.0e-30)
    )


def hybrid_flow(model: Any, saddle: Any, fixed: Any, xi: np.ndarray) -> np.ndarray:
    xi_long = np.asarray(xi, dtype=np.clongdouble).reshape(7)
    linear_long = np.asarray(fixed.linear_map, dtype=np.clongdouble)
    saddle_long = np.asarray(
        saddle.saddle_w, dtype=np.clongdouble
    ).reshape(7)
    w_long = np.asarray(
        saddle_long + linear_long @ xi_long, dtype=np.clongdouble
    ).reshape(7)
    raw_gradient_long = np.asarray(model.gradient_function(tuple(w_long)))
    if raw_gradient_long.dtype != np.dtype(np.clongdouble):
        raise InvalidRun(
            "generated gradient callable did not retain clongdouble evaluation"
        )
    gradient_long = np.asarray(raw_gradient_long, dtype=np.clongdouble).reshape(7)
    flow_long = np.asarray(
        -np.conjugate(linear_long.T @ gradient_long),
        dtype=np.clongdouble,
    ).reshape(7)
    flow = np.asarray(flow_long, dtype=np.complex128).reshape(7)
    if not np.all(np.isfinite(flow)):
        raise InvalidRun("hybrid flow produced a nonfinite value")
    return flow


def independent_flow(
    phase43: ModuleType,
    evaluator: Any,
    saddle64: np.ndarray,
    linear64: np.ndarray,
    xi64: np.ndarray,
    dps: int,
) -> np.ndarray:
    with mp.workdps(dps):
        saddle = [phase43.mp_complex_from_binary64(item) for item in saddle64]
        linear = phase43.mp_real_matrix_from_numpy(linear64)
        xi = [phase43.mp_complex_from_binary64(item) for item in xi64]
        raw = phase43.reference_flow(evaluator, saddle, linear, xi)
        output = np.empty(7, dtype=np.complex128)
        output.real = [float(item.real) for item in raw]
        output.imag = [float(item.imag) for item in raw]
    if not np.all(np.isfinite(output)):
        raise InvalidRun("independent local flow produced a nonfinite value")
    return output


def solver_record(solution: Any, xi_values: np.ndarray, spec: Mapping[str, Any]) -> dict[str, Any]:
    if not bool(solution.success) or solution.sol is None:
        raise InvalidRun(f"hybrid DOP853 integration failed: {solution.message}")
    if not np.all(np.isfinite(xi_values)):
        raise InvalidRun("hybrid DOP853 integration produced nonfinite state")
    xi_norm_max = float(np.max(np.linalg.norm(xi_values, axis=0)))
    if xi_norm_max >= 40.0:
        raise InvalidRun("hybrid DOP853 integration exceeded xi-norm cap")
    return {
        "success": True,
        "message": str(solution.message),
        "method": str(spec["method"]),
        "rtol": float(spec["rtol"]),
        "atol": float(spec["atol"]),
        "max_step": float(spec["max_step"]),
        "dense_output": bool(spec["dense_output"]),
        "nfev": int(solution.nfev),
        "njev": None if solution.njev is None else int(solution.njev),
        "nlu": None if solution.nlu is None else int(solution.nlu),
        "accepted_steps": int(solution.t.size - 1),
        "stored_times": int(solution.t.size),
        "xi_norm_max": xi_norm_max,
    }


def integrate_hybrid(
    phase42: ModuleType,
    phase43: ModuleType,
    context: Any,
    point: Any,
    parameters: np.ndarray,
    evaluator: Any,
    spec: Mapping[str, Any],
    fractions: np.ndarray,
    reference_dps: int,
) -> dict[str, Any]:
    omega, _derivative = phase42.affine_chart_direction(context, parameters[7:13])
    launch = point.saddle.launch_matrix(1.0)
    initial_xi = 1.0e-4 * (launch @ omega)
    flow_time = float(parameters[13])
    evaluation_count = 0

    def rhs(_time: float, xi: np.ndarray) -> np.ndarray:
        nonlocal evaluation_count
        evaluation_count += 1
        if evaluation_count % 2000 == 0:
            progress(f"{point.label}: hybrid RHS evaluations={evaluation_count}")
        return hybrid_flow(point.model, point.saddle, context.fixed, xi)

    solution = solve_ivp(
        rhs,
        (0.0, flow_time),
        initial_xi,
        method=str(spec["method"]),
        rtol=float(spec["rtol"]),
        atol=float(spec["atol"]),
        max_step=float(spec["max_step"]),
        dense_output=bool(spec["dense_output"]),
    )
    xi_values = np.asarray(solution.y, dtype=np.complex128)
    solver = solver_record(solution, xi_values, spec)
    solver["instrumented_rhs_evaluations"] = evaluation_count
    sample_times = flow_time * fractions
    sample_xi = np.asarray(solution.sol(sample_times), dtype=np.complex128).T
    if sample_xi.shape != (len(fractions), 7) or not np.all(np.isfinite(sample_xi)):
        raise InvalidRun("hybrid dense trajectory sample shape/finiteness drift")
    saddle64 = np.asarray(point.saddle.saddle_w, dtype=np.complex128).reshape(7)
    linear64 = np.asarray(context.fixed.linear_map, dtype=np.float64)
    local_probes: list[dict[str, Any]] = []
    for fraction, xi in zip(fractions, sample_xi):
        repaired = hybrid_flow(point.model, point.saddle, context.fixed, xi)
        reference = independent_flow(
            phase43,
            evaluator,
            saddle64,
            linear64,
            xi,
            reference_dps,
        )
        local_probes.append(
            {
                "fraction": float(fraction),
                "xi": xi,
                "hybrid_flow": repaired,
                "independent_flow": reference,
                "symmetric_relative": symmetric_relative(repaired, reference),
                "max_component_absolute": float(np.max(np.abs(repaired - reference))),
            }
        )
    final_xi = xi_values[:, -1]
    state_z = context.coordinate_scales * (
        point.saddle.saddle_w + context.fixed.linear_map @ final_xi
    )
    gamma_state, _gamma_tangent = context.phase41.gamma_cap(
        point.model, parameters[:6], float(parameters[6])
    )
    residual = context.phase41.interleaved(
        (gamma_state - state_z) / context.coordinate_scales
    )
    return {
        "initial_xi": initial_xi,
        "trajectory_samples": local_probes,
        "endpoint_xi": final_xi,
        "endpoint_state_z": state_z,
        "residual": residual,
        "solver": solver,
    }


def result_with_self_digest(payload: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(result)
    ).hexdigest()
    return result


def run() -> dict[str, Any]:
    manifest, _ = load_unique_json(INPUT_PATH)
    validated_inputs = validate_inputs(manifest)
    platform_validation = platform_contract(manifest)
    if not platform_validation["all_passed"]:
        raise InvalidRun("NumPy long-double platform contract failed")
    progress("load pinned Phase 42 context and retained Phase 45-48 controls")
    phase42 = load_module("ice_phase42_for_phase49", PHASE42_SCRIPT_PATH)
    phase43 = load_module("ice_phase43_for_phase49", PHASE43_SCRIPT_PATH)
    phase42_manifest, _ = phase42.read_pinned_json(
        PHASE42_INPUT_PATH,
        PHASE42_INPUT_SHA256,
        label="Phase42 input manifest",
    )
    checkpoint, checkpoint_raw = phase42.read_pinned_json(
        PHASE42_CHECKPOINT_PATH,
        manifest["pinned_inputs"]["phase42_checkpoint"]["sha256"],
        label="Phase42 checkpoint",
    )
    context = phase42.rehydrate_checkpoint(
        phase42_manifest, checkpoint, checkpoint_raw
    )
    phase45, _ = load_unique_json(PHASE45_RESULT_PATH)
    phase46, _ = load_unique_json(PHASE46_RESULT_PATH)
    phase47, _ = load_unique_json(PHASE47_RESULT_PATH)
    phase48, _ = load_unique_json(PHASE48_RESULT_PATH)
    phase45_digest = verify_self_digest(phase45, label="Phase45 result")
    phase46_digest = verify_self_digest(phase46, label="Phase46 result")
    phase47_digest = verify_self_digest(phase47, label="Phase47 result")
    phase48_digest = verify_self_digest(phase48, label="Phase48 result")
    if phase45.get("run_status") != "VALID_RUN":
        raise InvalidRun("Phase45 result status drift")
    if phase46.get("run_status") != "VALID_RUN":
        raise InvalidRun("Phase46 result status drift")
    if phase47.get("run_status") != "VALID_RUN":
        raise InvalidRun("Phase47 result status drift")
    if phase48.get("run_status") != "VALID_RUN":
        raise InvalidRun("Phase48 result status drift")
    phase46_prerequisite = bool(
        phase46["aggregate_tests"]["all_independent_full_ladders_pass"]
        and phase46["aggregate_tests"][
            "all_independent_columns_agree_with_phase45_tangent"
        ]
    )
    phase47_counts = phase47["aggregate_metrics"]
    phase47_prerequisite = bool(
        phase47["classification"]
        == "LOCAL_SOURCE_GRADIENT_MIXED_ARITHMETIC_BUDGET_SUPPORTED"
        and phase47_counts[
            "largest_delta_norm_counts_across_state_slots_descriptive_only"
        ]["D_gradient_evaluation"]
        == 36
        and phase47_counts[
            "largest_delta_norm_counts_across_paired_Dh_slots_descriptive_only"
        ]["D_gradient_evaluation"]
        == 18
    )
    phase48_prerequisite = bool(
        phase48["classification"]
        == "GRADIENT_ONLY_CLONGDOUBLE_STATE_MAP_REPAIR_NOT_SUFFICIENT"
        and not phase48["aggregate_tests"][
            "all_hybrid_Dh_columns_agree_with_independent"
        ]
        and not phase48["aggregate_tests"][
            "all_hybrid_Dh_columns_agree_with_phase45_tangent"
        ]
    )

    scope = manifest["scope"]
    numerics = manifest["fixed_numerics"]
    thresholds = manifest["fixed_metrics_and_thresholds"]
    steps = [float(value) for value in scope["central_difference_steps_in_order"]]
    signs = [int(value) for value in scope["perturbation_signs_in_order"]]
    fractions = np.asarray(
        scope["trajectory_sample_fractions_in_order"], dtype=np.float64
    )
    solver_spec = numerics["hybrid_state_solver"]
    reference_dps = int(numerics["independent_local_flow_probe_dps"])
    points: dict[str, Any] = {}
    all_integrations = True
    all_local_flow = True
    all_endpoints = True
    all_columns = True
    all_tangent = True
    all_ladders = True
    integration_count = 0

    for label in scope["targets_in_order"]:
        progress(f"{label}: build independent evaluator")
        point = context.points[label]
        evaluator = phase43.make_reference_evaluators(
            format(point.source_point[0], ".17g"),
            format(point.source_point[1], ".17g"),
        )
        hybrid_records: dict[str, Any] = {}
        independent_records = phase46["points"][label]["retained_state_maps"][
            "independent_exact_80dps_dop853"
        ]
        local_flow_max = 0.0
        endpoint_state_relatives: list[float] = []
        endpoint_xi_relatives: list[float] = []
        residual_relatives: list[float] = []
        for step in steps:
            for sign in signs:
                slot = f"h={step:.1e},sign={sign:+d}"
                progress(f"{label}: integrate full-flow hybrid {slot}")
                parameters = point.parameters.copy()
                parameters[int(scope["parameter_index"])] += sign * step
                record = integrate_hybrid(
                    phase42,
                    phase43,
                    context,
                    point,
                    parameters,
                    evaluator,
                    solver_spec,
                    fractions,
                    reference_dps,
                )
                reference = independent_records[slot]
                reference_state = decode_complex_record(
                    reference["endpoint_state_z"],
                    label=f"{label}/{slot}/independent endpoint_state_z",
                )
                reference_xi = decode_complex_record(
                    reference["endpoint_xi"],
                    label=f"{label}/{slot}/independent endpoint_xi",
                )
                reference_residual = np.asarray(reference["residual"], dtype=np.float64)
                local_max = max(
                    float(probe["symmetric_relative"])
                    for probe in record["trajectory_samples"]
                )
                state_relative = symmetric_relative(
                    record["endpoint_state_z"], reference_state
                )
                xi_relative = symmetric_relative(record["endpoint_xi"], reference_xi)
                residual_relative = symmetric_relative(
                    record["residual"], reference_residual
                )
                record["comparisons_to_phase46_independent"] = {
                    "trajectory_local_flow_relative_max": local_max,
                    "endpoint_state_z_symmetric_relative": state_relative,
                    "endpoint_xi_symmetric_relative": xi_relative,
                    "residual_symmetric_relative": residual_relative,
                    "retained_reference_path": (
                        f"$.points.{label}.retained_state_maps."
                        f"independent_exact_80dps_dop853.{slot}"
                    ),
                }
                hybrid_records[slot] = record
                integration_count += 1
                local_flow_max = max(local_flow_max, local_max)
                endpoint_state_relatives.append(state_relative)
                endpoint_xi_relatives.append(xi_relative)
                residual_relatives.append(residual_relative)
                all_integrations = all_integrations and bool(record["solver"]["success"])

        hybrid_columns: list[np.ndarray] = []
        independent_columns: list[np.ndarray] = []
        for step in steps:
            plus = np.asarray(
                hybrid_records[f"h={step:.1e},sign=+1"]["residual"], dtype=np.float64
            )
            minus = np.asarray(
                hybrid_records[f"h={step:.1e},sign=-1"]["residual"], dtype=np.float64
            )
            hybrid_columns.append((plus - minus) / (2.0 * step))
            reference_plus = np.asarray(
                independent_records[f"h={step:.1e},sign=+1"]["residual"],
                dtype=np.float64,
            )
            reference_minus = np.asarray(
                independent_records[f"h={step:.1e},sign=-1"]["residual"],
                dtype=np.float64,
            )
            independent_columns.append(
                (reference_plus - reference_minus) / (2.0 * step)
            )
        hybrid_plateaus = [
            phase41_plateau(first, second)
            for first, second in zip(hybrid_columns[:-1], hybrid_columns[1:])
        ]
        column_relatives = [
            symmetric_relative(hybrid, reference)
            for hybrid, reference in zip(hybrid_columns, independent_columns)
        ]
        tangent_column = np.asarray(
            phase45["points"][label]["root_jacobians"][
                "independent_exact_80dps"
            ],
            dtype=np.float64,
        )[:, int(scope["parameter_index"])]
        tangent_relatives = [
            symmetric_relative(column, tangent_column) for column in hybrid_columns
        ]
        metrics = {
            "trajectory_local_flow_to_independent_relative_max": local_flow_max,
            "endpoint_state_to_independent_relative_max": max(endpoint_state_relatives),
            "endpoint_xi_to_independent_relative_max": max(endpoint_xi_relatives),
            "residual_to_independent_relative_max": max(residual_relatives),
            "hybrid_Dh_to_independent_relative_max": max(column_relatives),
            "hybrid_Dh_to_phase45_tangent_relative_max": max(tangent_relatives),
            "hybrid_adjacent_plateau_max": max(hybrid_plateaus),
            "per_step_hybrid_Dh_to_independent_relatives": column_relatives,
            "per_step_hybrid_Dh_to_phase45_tangent_relatives": tangent_relatives,
        }
        tests = {
            "trajectory_local_flow_agrees": local_flow_max
            <= float(thresholds["hybrid_trajectory_local_flow_to_independent_relative_max"]),
            "endpoint_state_agrees": max(endpoint_state_relatives)
            <= float(thresholds["hybrid_endpoint_state_to_independent_relative_max"]),
            "all_Dh_columns_agree_with_independent": max(column_relatives)
            <= float(thresholds["hybrid_Dh_column_to_independent_relative_max"]),
            "all_Dh_columns_agree_with_phase45_tangent": max(tangent_relatives)
            <= float(thresholds["hybrid_Dh_column_to_phase45_tangent_relative_max"]),
            "full_hybrid_ladder_is_stable": max(hybrid_plateaus)
            <= float(thresholds["hybrid_stable_adjacent_step_relative_change_max"]),
        }
        all_local_flow = all_local_flow and tests["trajectory_local_flow_agrees"]
        all_endpoints = all_endpoints and tests["endpoint_state_agrees"]
        all_columns = all_columns and tests["all_Dh_columns_agree_with_independent"]
        all_tangent = all_tangent and tests[
            "all_Dh_columns_agree_with_phase45_tangent"
        ]
        all_ladders = all_ladders and tests["full_hybrid_ladder_is_stable"]
        points[label] = {
            "source_point": list(point.source_point),
            "steps": steps,
            "hybrid_state_maps": hybrid_records,
            "hybrid_finite_difference_columns_by_step": hybrid_columns,
            "independent_finite_difference_columns_by_step": independent_columns,
            "phase45_independent_tangent_u2_column": tangent_column,
            "hybrid_adjacent_plateaus": hybrid_plateaus,
            "metrics": metrics,
            "tests": tests,
        }

    prerequisites = all(
        (
            platform_validation["all_passed"],
            all_integrations,
            integration_count == int(scope["new_hybrid_state_path_count"]),
            phase46_prerequisite,
            phase47_prerequisite,
            phase48_prerequisite,
        )
    )
    repair_passed = all(
        (all_local_flow, all_endpoints, all_columns, all_tangent, all_ladders)
    )
    labels = manifest["classification"]
    if prerequisites and repair_passed:
        classification = labels["repair_supported_label"]
    elif prerequisites:
        classification = labels["repair_not_sufficient_label"]
    else:
        classification = labels["inconclusive_label"]
    result = {
        "schema": RESULT_SCHEMA,
        "phase": 49,
        "run_status": "VALID_RUN",
        "classification": classification,
        "aggregate_tests": {
            "platform_contract_passes": platform_validation["all_passed"],
            "all_18_hybrid_integrations_complete": all_integrations,
            "hybrid_integration_count_is_18": integration_count
            == int(scope["new_hybrid_state_path_count"]),
            "phase46_independent_prerequisites_pass": phase46_prerequisite,
            "phase47_gradient_localization_prerequisites_pass": phase47_prerequisite,
            "phase48_gradient_only_negative_control_prerequisites_pass": phase48_prerequisite,
            "all_hybrid_trajectory_local_flow_probes_pass": all_local_flow,
            "all_hybrid_endpoints_agree": all_endpoints,
            "all_hybrid_Dh_columns_agree_with_independent": all_columns,
            "all_hybrid_Dh_columns_agree_with_phase45_tangent": all_tangent,
            "all_hybrid_full_ladders_are_stable": all_ladders,
        },
        "platform_validation": platform_validation,
        "thresholds": thresholds,
        "points": points,
        "provenance": {
            "input_manifest_commit": INPUT_COMMIT,
            "input_manifest_sha256": INPUT_SHA256,
            "validated_inputs": validated_inputs,
            "phase45_result_self_digest": phase45_digest,
            "phase46_result_self_digest": phase46_digest,
            "phase47_result_self_digest": phase47_digest,
            "phase48_result_self_digest": phase48_digest,
            "runner_sha256": sha256_path(SCRIPT_PATH),
            "runtime": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "sympy": sympy.__version__,
                "mpmath": mpmath.__version__,
            },
        },
        "interpretation_boundary": {
            "calculation_workbench_only": True,
            "historical_phase41_phase45_phase46_phase47_phase48_results_unchanged": True,
            "full_flow_platform_specific_ablation": True,
            "formal_endpoint_error_propagator_bound": None,
            "new_tangent_integration": "NOT_RUN_PHASE45_REFERENCE_REUSED",
            "root_search_or_retuning": "NOT_RUN",
            "global_promotion": "PROHIBITED",
            "gate1": "OPEN_PARTIAL_PROGRESS",
        },
    }
    return result_with_self_digest(result)


def main() -> int:
    try:
        result = run()
        print(RESULT_PREFIX + canonical_bytes(result).decode("utf-8"))
        return 0
    except Exception as exc:
        emergency = result_with_self_digest(
            {
                "schema": RESULT_SCHEMA,
                "phase": 49,
                "run_status": "INVALID_RUN",
                "classification": "CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_INCONCLUSIVE",
                "error_type": type(exc).__name__,
                "error": str(exc)[:4096],
                "provenance": {
                    "input_manifest_commit": INPUT_COMMIT,
                    "input_manifest_sha256": INPUT_SHA256,
                    "runner_sha256": sha256_path(SCRIPT_PATH),
                },
            }
        )
        print(RESULT_PREFIX + canonical_bytes(emergency).decode("utf-8"))
        print(f"Phase49 invalid run: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
