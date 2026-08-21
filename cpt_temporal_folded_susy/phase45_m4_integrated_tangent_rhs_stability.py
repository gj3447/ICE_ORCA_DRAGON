#!/usr/bin/env python3
"""Phase 45: integrated-tangent stability under an independent local RHS.

This calculation keeps the three Phase-42 roots and one source NumPy64 state
trajectory fixed.  Along that trajectory it integrates the six chart tangent
columns with the Phase-41 NumPy64 Hessian action and with the independently
rebuilt Phase-43 exact-decimal action at 50 and 80 decimal digits.  It performs
no root search, orientation selection, determinant-line construction, or
global-cycle calculation.
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
from typing import Any, Callable, Mapping

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
    "PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_INPUTS.json"
)
PHASE42_INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE42_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json"
)
PHASE42_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase42_m4_fixed_root_tangent_disentanglement.py"
)
PHASE43_SCRIPT_PATH = SCRIPT_PATH.with_name(
    "phase43_m4_high_precision_local_rhs_arbitration.py"
)

INPUT_COMMIT = "a5eac15e54a4f6e4aec8381b526a61c22fd0570f"
INPUT_SHA256 = "34d88f6f080b9720a056d8406c1d8e807fc0578d98f30a6aa5d010fbed5d3a87"
PHASE42_INPUT_SHA256 = "1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6"
RESULT_SCHEMA = "ice-phase45-integrated-tangent-rhs-stability/v1"
RESULT_PREFIX = "RESULT_JSON="


class InvalidRun(RuntimeError):
    """A pinned input, solver, or retained-result invariant failed."""


def progress(message: str) -> None:
    print(f"[Phase45] {message}", file=sys.stderr, flush=True)


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
            flat = np.asarray(value, dtype=np.complex128).reshape(-1)
            pairs = [[float(item.real), float(item.imag)] for item in flat]
            return {"shape": list(value.shape), "complex128_pairs": pairs}
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


def symmetric_relative(left: np.ndarray, right: np.ndarray) -> float:
    left_array = np.asarray(left)
    right_array = np.asarray(right)
    denominator = max(
        float(np.linalg.norm(left_array)),
        float(np.linalg.norm(right_array)),
        1.0e-300,
    )
    return float(np.linalg.norm(left_array - right_array) / denominator)


def normalized_sign(matrix: np.ndarray) -> int:
    values = np.asarray(matrix, dtype=np.float64)
    norms = np.linalg.norm(values, axis=0)
    if np.any(~np.isfinite(norms)) or np.any(norms <= 0.0):
        raise InvalidRun("cannot normalize a zero/nonfinite Jacobian column")
    sign, _logabs = np.linalg.slogdet(values / norms)
    if sign not in (-1.0, 1.0):
        raise InvalidRun("normalized Jacobian is singular")
    return int(sign)


def solver_record(solution: Any) -> dict[str, Any]:
    if not bool(solution.success) or solution.sol is None:
        raise InvalidRun(f"DOP853 integration failed: {solution.message}")
    if not np.all(np.isfinite(solution.y)):
        raise InvalidRun("DOP853 integration produced a nonfinite value")
    return {
        "success": True,
        "message": str(solution.message),
        "nfev": int(solution.nfev),
        "accepted_steps": int(solution.t.size - 1),
        "stored_times": int(solution.t.size),
    }


def reference_tangent_action(
    phase43: ModuleType,
    evaluator: Any,
    saddle_mp: list[Any],
    linear_mp: Any,
    xi: np.ndarray,
    tangent: np.ndarray,
    dps: int,
) -> np.ndarray:
    with mp.workdps(dps):
        xi_mp = mp.matrix(
            [phase43.mp_complex_from_binary64(item) for item in xi]
        )
        tangent_mp = mp.matrix(
            tangent.shape[0],
            tangent.shape[1],
        )
        for row in range(tangent.shape[0]):
            for column in range(tangent.shape[1]):
                tangent_mp[row, column] = phase43.mp_complex_from_binary64(
                    tangent[row, column]
                )
        w_mp = mp.matrix(saddle_mp) + linear_mp * xi_mp
        hessian_w = phase43.matrix_mp(
            evaluator.exact_hessian(tuple(w_mp)), 7, 7
        )
        action = linear_mp.T * hessian_w * linear_mp * tangent_mp
        output = np.empty(tangent.shape, dtype=np.complex128)
        for row in range(tangent.shape[0]):
            for column in range(tangent.shape[1]):
                value = -mp.conj(action[row, column])
                output[row, column] = complex(float(value.real), float(value.imag))
    if not np.all(np.isfinite(output)):
        raise InvalidRun(f"nonfinite independent {dps}-dps tangent RHS")
    return output


def integrate_state(
    phase42: ModuleType,
    context: Any,
    point: Any,
    solver_spec: Mapping[str, Any],
) -> tuple[Any, dict[str, Any], np.ndarray, np.ndarray]:
    parameters = point.parameters
    omega, derivative = phase42.affine_chart_direction(
        context, parameters[7:13]
    )
    launch = point.saddle.launch_matrix(1.0)
    initial_xi = 1.0e-4 * (launch @ omega)
    initial_tangent = 1.0e-4 * (launch @ derivative)
    solution = solve_ivp(
        lambda _time, xi: context.phase41.flow_xi(
            point.model, point.saddle, context.fixed, xi
        ),
        (0.0, float(parameters[13])),
        initial_xi,
        method=str(solver_spec["method"]),
        rtol=float(solver_spec["rtol"]),
        atol=float(solver_spec["atol"]),
        max_step=float(solver_spec["max_step"]),
        dense_output=True,
    )
    return solution, solver_record(solution), initial_xi, initial_tangent


def integrate_tangent(
    state_solution: Any,
    flow_time: float,
    initial_tangent: np.ndarray,
    rhs: Callable[[np.ndarray, np.ndarray], np.ndarray],
    solver_spec: Mapping[str, Any],
    fractions: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    def flattened_rhs(time: float, flat: np.ndarray) -> np.ndarray:
        xi = np.asarray(state_solution.sol(time), dtype=np.complex128)
        tangent = np.asarray(flat, dtype=np.complex128).reshape(7, 6)
        return rhs(xi, tangent).reshape(-1)

    solution = solve_ivp(
        flattened_rhs,
        (0.0, flow_time),
        initial_tangent.reshape(-1),
        method=str(solver_spec["method"]),
        rtol=float(solver_spec["rtol"]),
        atol=float(solver_spec["atol"]),
        max_step=float(solver_spec["max_step"]),
        dense_output=True,
    )
    record = solver_record(solution)
    samples = np.asarray(
        solution.sol(flow_time * fractions), dtype=np.complex128
    ).T.reshape(fractions.size, 7, 6)
    return samples, record


def root_jacobian(
    context: Any,
    point: Any,
    endpoint_xi: np.ndarray,
    endpoint_tangent: np.ndarray,
) -> np.ndarray:
    linear_z = np.diag(context.coordinate_scales) @ context.fixed.linear_map
    tangent_z = linear_z @ endpoint_tangent
    time_tangent_z = linear_z @ context.phase41.flow_xi(
        point.model, point.saddle, context.fixed, endpoint_xi
    )
    k_frame = context.phase41.real_frame(
        np.column_stack([tangent_z, time_tangent_z])
    )
    _gamma_state, gamma_tangent = context.phase41.gamma_cap(
        point.model, point.parameters[:6], float(point.parameters[6])
    )
    gamma_frame = context.phase41.real_frame(gamma_tangent)
    return context.row_scales[:, None] * np.column_stack(
        [gamma_frame, -k_frame]
    )


def validate_frozen_inputs(manifest: Mapping[str, Any]) -> dict[str, Any]:
    if sha256_path(INPUT_PATH) != INPUT_SHA256:
        raise InvalidRun("Phase45 input manifest hash drift")
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


def run() -> dict[str, Any]:
    manifest, _manifest_raw = load_unique_json(INPUT_PATH)
    if manifest.get("schema") != "ice-phase45-integrated-tangent-rhs-stability-inputs/v1":
        raise InvalidRun("Phase45 input schema drift")
    input_validation = validate_frozen_inputs(manifest)

    progress("load pinned Phase-42 context and Phase-43 reference")
    phase42 = load_module("ice_phase42_for_phase45", PHASE42_SCRIPT_PATH)
    phase43 = load_module("ice_phase43_for_phase45", PHASE43_SCRIPT_PATH)
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
    phase42_result, _ = load_unique_json(PHASE42_RESULT_PATH)

    numerics = manifest["fixed_numerics"]
    thresholds = manifest["fixed_metrics_and_thresholds"]
    fractions = np.asarray(numerics["sample_fractions"], dtype=np.float64)
    if not np.array_equal(fractions, np.array([0.0, 0.25, 0.5, 0.75, 1.0])):
        raise InvalidRun("sample fractions drift")

    points: dict[str, Any] = {}
    all_precision_pass = True
    all_source_tangent_pass = True
    all_source_jacobian_pass = True
    all_r4_pass = True
    all_sign_pass = True
    all_historical_fail = True

    for label in manifest["scope"]["targets_in_order"]:
        progress(f"{label}: build independent evaluator")
        point = context.points[label]
        evaluator = phase43.make_reference_evaluators(
            format(point.source_point[0], ".17g"),
            format(point.source_point[1], ".17g"),
        )
        state_solution, state_solver, initial_xi, initial_tangent = integrate_state(
            phase42,
            context,
            point,
            numerics["state_solver"],
        )
        flow_time = float(point.parameters[13])
        sample_times = flow_time * fractions
        state_samples = np.asarray(
            state_solution.sol(sample_times), dtype=np.complex128
        ).T
        endpoint_xi = state_samples[-1]

        source_rhs = lambda xi, tangent: -np.conjugate(
            context.phase41.hessian_xi(
                point.model, point.saddle, context.fixed, xi
            )
            @ tangent
        )
        tangent_samples: dict[str, np.ndarray] = {}
        tangent_solvers: dict[str, Any] = {}
        progress(f"{label}: source NumPy64 tangent")
        tangent_samples["source_numpy64"], tangent_solvers["source_numpy64"] = (
            integrate_tangent(
                state_solution,
                flow_time,
                initial_tangent,
                source_rhs,
                numerics["tangent_solver"],
                fractions,
            )
        )

        # Lift the binary64 geometry once above both requested evaluation
        # precisions.  This prevents the ambient default mpmath precision from
        # becoming an undeclared input to either reference path.
        with mp.workdps(120):
            saddle_mp = [
                phase43.mp_complex_from_binary64(item)
                for item in point.saddle.saddle_w
            ]
            linear_mp = phase43.mp_real_matrix_from_numpy(
                context.fixed.linear_map
            )
        for dps in (50, 80):
            path_name = f"independent_exact_{dps}dps"
            progress(f"{label}: independent exact {dps}-dps tangent")

            def reference_rhs(
                xi: np.ndarray,
                tangent: np.ndarray,
                *,
                digits: int = dps,
            ) -> np.ndarray:
                return reference_tangent_action(
                    phase43,
                    evaluator,
                    saddle_mp,
                    linear_mp,
                    xi,
                    tangent,
                    digits,
                )

            tangent_samples[path_name], tangent_solvers[path_name] = integrate_tangent(
                state_solution,
                flow_time,
                initial_tangent,
                reference_rhs,
                numerics["tangent_solver"],
                fractions,
            )

        jacobians = {
            name: root_jacobian(context, point, endpoint_xi, samples[-1])
            for name, samples in tangent_samples.items()
        }
        r4 = np.asarray(
            phase42_result["finite_difference_diagnostics"]["points"][label][
                "J_R4"
            ],
            dtype=np.float64,
        )
        historical = phase42_result["phase41_negative_control"]["points"][label]
        historical_plateau = float(historical["u2_plateau"])

        fraction_metrics = []
        for index, fraction in enumerate(fractions):
            fraction_metrics.append(
                {
                    "fraction": float(fraction),
                    "reference_50_to_80": symmetric_relative(
                        tangent_samples["independent_exact_50dps"][index],
                        tangent_samples["independent_exact_80dps"][index],
                    ),
                    "source_to_reference_80": symmetric_relative(
                        tangent_samples["source_numpy64"][index],
                        tangent_samples["independent_exact_80dps"][index],
                    ),
                }
            )
        reference_precision_max = max(
            record["reference_50_to_80"] for record in fraction_metrics
        )
        source_reference_tangent_max = max(
            record["source_to_reference_80"] for record in fraction_metrics
        )
        source_reference_jacobian = symmetric_relative(
            jacobians["source_numpy64"],
            jacobians["independent_exact_80dps"],
        )
        reference_r4 = symmetric_relative(
            jacobians["independent_exact_80dps"], r4
        )
        reference_sign = normalized_sign(jacobians["independent_exact_80dps"])

        tests = {
            "reference_precision_stable": reference_precision_max
            <= float(thresholds["reference_50dps_to_80dps_tangent_relative_max"]),
            "source_tangent_agrees_with_reference": source_reference_tangent_max
            <= float(thresholds["source_to_reference_tangent_relative_max"]),
            "source_root_jacobian_agrees_with_reference": source_reference_jacobian
            <= float(thresholds["source_to_reference_root_jacobian_relative_max"]),
            "reference_root_jacobian_agrees_with_R4": reference_r4
            <= float(
                thresholds["reference_root_jacobian_to_phase42_R4_relative_max"]
            ),
            "reference_normalized_sign_matches": reference_sign
            == int(thresholds["reference_root_jacobian_normalized_sign_must_equal"]),
            "historical_u2_plateau_still_fails": historical_plateau
            > float(thresholds["historical_u2_plateau_failure_threshold"]),
        }
        all_precision_pass &= tests["reference_precision_stable"]
        all_source_tangent_pass &= tests["source_tangent_agrees_with_reference"]
        all_source_jacobian_pass &= tests[
            "source_root_jacobian_agrees_with_reference"
        ]
        all_r4_pass &= tests["reference_root_jacobian_agrees_with_R4"]
        all_sign_pass &= tests["reference_normalized_sign_matches"]
        all_historical_fail &= tests["historical_u2_plateau_still_fails"]

        points[label] = {
            "source_point": list(point.source_point),
            "flow_time": flow_time,
            "initial_xi": initial_xi,
            "initial_tangent": initial_tangent,
            "sample_times": sample_times,
            "state_samples": state_samples,
            "state_solver": state_solver,
            "tangent_samples": tangent_samples,
            "tangent_solvers": tangent_solvers,
            "root_jacobians": jacobians,
            "phase42_R4_root_jacobian": r4,
            "fraction_metrics": fraction_metrics,
            "metrics": {
                "reference_50dps_to_80dps_tangent_relative_max": reference_precision_max,
                "source_to_reference_tangent_relative_max": source_reference_tangent_max,
                "source_to_reference_root_jacobian_relative": source_reference_jacobian,
                "reference_root_jacobian_to_phase42_R4_relative": reference_r4,
                "reference_root_jacobian_normalized_sign": reference_sign,
                "historical_phase41_u2_plateau": historical_plateau,
                "historical_phase41_failed_columns": historical[
                    "failed_plateau_columns"
                ],
            },
            "tests": tests,
        }

    stable = all(
        (
            all_precision_pass,
            all_source_tangent_pass,
            all_source_jacobian_pass,
            all_r4_pass,
            all_sign_pass,
            all_historical_fail,
        )
    )
    repaired = all(
        (all_precision_pass, all_r4_pass, all_sign_pass)
    ) and not all((all_source_tangent_pass, all_source_jacobian_pass))
    labels = manifest["classification"]
    if stable:
        classification = labels["stable_label"]
    elif repaired:
        classification = labels["repaired_label"]
    else:
        classification = labels["inconclusive_label"]

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 45,
        "run_status": "VALID_RUN",
        "classification": classification,
        "aggregate_tests": {
            "all_reference_precision_stable": all_precision_pass,
            "all_source_tangents_agree_with_reference": all_source_tangent_pass,
            "all_source_root_jacobians_agree_with_reference": all_source_jacobian_pass,
            "all_reference_root_jacobians_agree_with_R4": all_r4_pass,
            "all_reference_normalized_signs_match": all_sign_pass,
            "all_historical_u2_plateaus_still_fail": all_historical_fail,
        },
        "thresholds": thresholds,
        "points": points,
        "provenance": {
            "input_manifest_commit": INPUT_COMMIT,
            "input_manifest_sha256": INPUT_SHA256,
            "validated_inputs": input_validation,
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
            "historical_phase41_contract_unchanged": True,
            "root_search_or_retuning": "NOT_RUN",
            "global_cycle_or_intersection": None,
            "global_promotion": "PROHIBITED",
            "gate1": "OPEN_PARTIAL_PROGRESS",
        },
    }
    digest_payload = dict(result)
    result["result_payload_sha256_without_self"] = hashlib.sha256(
        canonical_bytes(digest_payload)
    ).hexdigest()
    return result


def main() -> int:
    try:
        result = run()
        print(RESULT_PREFIX + canonical_bytes(result).decode("utf-8"))
        return 0
    except Exception as exc:
        invalid = {
            "schema": RESULT_SCHEMA,
            "phase": 45,
            "run_status": "INVALID_RUN",
            "error": f"{type(exc).__name__}: {exc}",
            "classification": None,
            "global_promotion": "PROHIBITED",
            "gate1": "OPEN_PARTIAL_PROGRESS",
        }
        print(RESULT_PREFIX + canonical_bytes(invalid).decode("utf-8"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
