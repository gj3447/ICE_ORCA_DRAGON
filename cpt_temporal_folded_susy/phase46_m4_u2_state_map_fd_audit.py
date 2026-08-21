#!/usr/bin/env python3
"""Phase 46: audit the historical u2 state-map finite-difference plateau.

The three Phase-42 roots and the historical three-step u2 ladder stay fixed.
For every signed perturbation this calculation consumes the complete pinned
Phase-42 production/tight/Radau endpoints and newly integrates the independently
reconstructed Phase-43 exact-decimal local flow RHS.  It does not search for
roots, retune parameters, or make a global intersection claim.
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
INPUT_PATH = SCRIPT_PATH.with_name("PHASE46_M4_U2_STATE_MAP_FD_AUDIT_INPUTS.json")
PHASE42_INPUT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json"
)
PHASE42_CHECKPOINT_PATH = SCRIPT_PATH.with_name("PHASE42_M4_FIXED_ROOT_CHECKPOINT.json")
PHASE42_RESULT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json"
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

INPUT_COMMIT = "3a7c905e1cc634b7cea40f127f2d9975ce99b78e"
INPUT_SHA256 = "e69f31aeedc4078a9c801757399890d4c4f5ae01b1f24eb915567f3a2efe8b16"
PHASE42_INPUT_SHA256 = "1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6"
RESULT_SCHEMA = "ice-phase46-u2-state-map-fd-audit/v1"
RESULT_PREFIX = "RESULT_JSON="


class InvalidRun(RuntimeError):
    """A frozen input, solver, or retained-result invariant failed."""


def progress(message: str) -> None:
    print(f"[Phase46] {message}", file=sys.stderr, flush=True)


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
            return {
                "shape": list(value.shape),
                "complex128_pairs": [
                    [float(item.real), float(item.imag)] for item in flat
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


def symmetric_relative(left: np.ndarray, right: np.ndarray) -> float:
    left_array = np.asarray(left)
    right_array = np.asarray(right)
    denominator = max(
        float(np.linalg.norm(left_array)),
        float(np.linalg.norm(right_array)),
        1.0e-300,
    )
    return float(np.linalg.norm(left_array - right_array) / denominator)


def phase41_plateau(first: np.ndarray, second: np.ndarray) -> float:
    return float(
        np.linalg.norm(np.asarray(first) - np.asarray(second))
        / max(float(np.linalg.norm(first)), 1.0e-30)
    )


def validate_frozen_inputs(manifest: Mapping[str, Any]) -> dict[str, Any]:
    if sha256_path(INPUT_PATH) != INPUT_SHA256:
        raise InvalidRun("Phase46 input manifest hash drift")
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


def source_solver_record(solution: Any, xi_values: np.ndarray, spec: Mapping[str, Any]) -> dict[str, Any]:
    if not bool(solution.success):
        raise InvalidRun(f"{spec['method']} integration failed: {solution.message}")
    if not np.all(np.isfinite(xi_values)):
        raise InvalidRun(f"{spec['method']} integration produced nonfinite state")
    xi_norm_max = float(np.max(np.linalg.norm(xi_values, axis=0)))
    if xi_norm_max >= 40.0:
        raise InvalidRun(f"{spec['method']} integration exceeded xi-norm cap")
    return {
        "success": True,
        "message": str(solution.message),
        "method": str(spec["method"]),
        "rtol": float(spec["rtol"]),
        "atol": float(spec["atol"]),
        "max_step": float(spec["max_step"]),
        "nfev": int(solution.nfev),
        "njev": None if solution.njev is None else int(solution.njev),
        "nlu": None if solution.nlu is None else int(solution.nlu),
        "accepted_steps": int(solution.t.size - 1),
        "stored_times": int(solution.t.size),
        "xi_norm_max": xi_norm_max,
    }


def independent_flow_rhs(
    phase43: ModuleType,
    evaluator: Any,
    saddle_mp: list[Any],
    linear_mp: Any,
    xi: np.ndarray,
    dps: int,
) -> np.ndarray:
    with mp.workdps(dps):
        xi_mp = [phase43.mp_complex_from_binary64(item) for item in xi]
        raw = phase43.reference_flow(evaluator, saddle_mp, linear_mp, xi_mp)
        output = np.asarray(
            [complex(float(value.real), float(value.imag)) for value in raw],
            dtype=np.complex128,
        )
    if not np.all(np.isfinite(output)):
        raise InvalidRun(f"nonfinite independent {dps}-dps flow RHS")
    return output


def integrate_one(
    phase42: ModuleType,
    phase43: ModuleType,
    context: Any,
    point: Any,
    parameters: np.ndarray,
    path_name: str,
    spec: Mapping[str, Any],
    evaluator: Any,
    saddle_mp: list[Any],
    linear_mp: Any,
    independent_dps: int,
) -> dict[str, Any]:
    omega, _derivative = phase42.affine_chart_direction(context, parameters[7:13])
    launch = point.saddle.launch_matrix(1.0)
    initial_xi = 1.0e-4 * (launch @ omega)
    flow_time = float(parameters[13])
    evaluation_count = 0

    if path_name == "production_source_dop853":
        state_z, tangent, integration = context.phase41.integrate_chart(
            point.model,
            point.saddle,
            context.fixed,
            context.chart,
            parameters[7:13],
            flow_time,
            1.0e-4,
            1.0,
            with_tangent=False,
            method="DOP853",
        )
        if tangent is not None:
            raise InvalidRun("production state-only map unexpectedly returned tangent")
        state_z = np.asarray(state_z, dtype=np.complex128)
        final_w = state_z / context.coordinate_scales
        final_xi = np.linalg.solve(
            context.fixed.linear_map, final_w - point.saddle.saddle_w
        )
        solver = {
            "success": True,
            "message": "pinned Phase41 integrate_chart state-only map",
            "method": "DOP853",
            "rtol": float(spec["rtol"]),
            "atol": float(spec["atol"]),
            "max_step": float(spec["max_step"]),
            "nfev": None,
            "njev": None,
            "nlu": None,
            "accepted_steps": int(integration["solver_steps"]) - 1,
            "stored_times": int(integration["solver_steps"]),
            "xi_norm_max": float(integration["xi_norm_max"]),
        }
    else:
        if path_name == "tight_source_dop853":
            rhs: Callable[[float, np.ndarray], np.ndarray] = lambda _time, xi: (
                context.phase41.flow_xi(point.model, point.saddle, context.fixed, xi)
            )
            solution = solve_ivp(
                rhs,
                (0.0, flow_time),
                initial_xi,
                method="DOP853",
                rtol=float(spec["rtol"]),
                atol=float(spec["atol"]),
                max_step=float(spec["max_step"]),
            )
            xi_values = np.asarray(solution.y, dtype=np.complex128)
        elif path_name == "tight_source_radau":
            real_initial = context.phase41.interleaved(initial_xi)

            def real_rhs(_time: float, real_xi: np.ndarray) -> np.ndarray:
                nonlocal evaluation_count
                evaluation_count += 1
                if evaluation_count % 50 == 0:
                    progress(
                        f"{point.label}: Radau source RHS "
                        f"evaluations={evaluation_count}"
                    )
                xi = phase42.uninterleaved(real_xi)
                return context.phase41.interleaved(
                    context.phase41.flow_xi(
                        point.model, point.saddle, context.fixed, xi
                    )
                )

            solution = solve_ivp(
                real_rhs,
                (0.0, flow_time),
                real_initial,
                method="Radau",
                rtol=float(spec["rtol"]),
                atol=float(spec["atol"]),
                max_step=float(spec["max_step"]),
            )
            real_y = np.asarray(solution.y, dtype=float)
            xi_values = np.empty((7, real_y.shape[1]), dtype=np.complex128)
            xi_values.real[...] = real_y[0::2]
            xi_values.imag[...] = real_y[1::2]
        elif path_name == "independent_exact_80dps_dop853":

            def reference_rhs(_time: float, xi: np.ndarray) -> np.ndarray:
                nonlocal evaluation_count
                evaluation_count += 1
                if evaluation_count % 500 == 0:
                    progress(
                        f"{point.label}: independent RHS evaluations={evaluation_count}"
                    )
                return independent_flow_rhs(
                    phase43,
                    evaluator,
                    saddle_mp,
                    linear_mp,
                    xi,
                    independent_dps,
                )

            solution = solve_ivp(
                reference_rhs,
                (0.0, flow_time),
                initial_xi,
                method="DOP853",
                rtol=float(spec["rtol"]),
                atol=float(spec["atol"]),
                max_step=float(spec["max_step"]),
            )
            xi_values = np.asarray(solution.y, dtype=np.complex128)
        else:
            raise InvalidRun(f"undeclared state path: {path_name}")

        final_xi = xi_values[:, -1]
        solver = source_solver_record(solution, xi_values, spec)
        solver["instrumented_rhs_evaluations"] = (
            evaluation_count
            if path_name
            in ("tight_source_radau", "independent_exact_80dps_dop853")
            else None
        )
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
        "endpoint_xi": final_xi,
        "endpoint_state_z": state_z,
        "residual": residual,
        "solver": solver,
    }


def decode_phase42_complex_vector(value: Any, *, label: str) -> np.ndarray:
    try:
        output = np.asarray(
            [complex(float(item[0]), float(item[1])) for item in value],
            dtype=np.complex128,
        )
    except (TypeError, ValueError, IndexError) as exc:
        raise InvalidRun(f"cannot decode Phase42 complex vector: {label}") from exc
    if output.shape != (7,) or not np.all(np.isfinite(output)):
        raise InvalidRun(f"invalid Phase42 complex vector: {label}")
    return output


def retained_phase42_state_map(
    phase42_result: Mapping[str, Any],
    point_label: str,
    path_name: str,
    step: float,
    sign: int,
) -> dict[str, Any]:
    tier_by_path = {
        "production_source_dop853": "production_state",
        "tight_source_dop853": "tight_state",
        "tight_source_radau": "radau_state",
    }
    try:
        tier = tier_by_path[path_name]
    except KeyError as exc:
        raise InvalidRun(f"no Phase42 retained tier for {path_name}") from exc
    direction = "plus" if sign == 1 else "minus"
    key = (
        f"endpoint|{point_label}|{tier}|affine|col=8|"
        f"h={format(step, '.17g')}|{direction}"
    )
    try:
        slot = phase42_result["slot_ledger"][key]
    except KeyError as exc:
        raise InvalidRun(f"missing Phase42 endpoint slot: {key}") from exc
    if slot.get("terminal_status") != "SUCCESS" or slot.get("error") is not None:
        raise InvalidRun(f"incomplete Phase42 endpoint slot: {key}")
    metadata = slot["metadata"]
    if (
        metadata.get("point") != point_label
        or metadata.get("tier") != tier
        or metadata.get("column") != 8
        or float(metadata.get("h")) != step
        or int(metadata.get("sign")) != sign
        or metadata.get("chart_kind") != "affine"
    ):
        raise InvalidRun(f"Phase42 endpoint metadata drift: {key}")
    payload = slot["payload"]
    residual = np.asarray(payload["scaled_residual"], dtype=np.float64)
    if residual.shape != (14,) or not np.all(np.isfinite(residual)):
        raise InvalidRun(f"invalid Phase42 retained residual: {key}")
    return {
        "initial_xi": decode_phase42_complex_vector(
            payload["initial_xi"], label=f"{key}.initial_xi"
        ),
        "endpoint_xi": decode_phase42_complex_vector(
            payload["endpoint_xi"], label=f"{key}.endpoint_xi"
        ),
        "endpoint_state_z": decode_phase42_complex_vector(
            payload["k_state_z"], label=f"{key}.k_state_z"
        ),
        "residual": residual,
        "solver": dict(payload["solver"]),
        "retained_source": {
            "artifact": PHASE42_RESULT_PATH.relative_to(REPO_ROOT).as_posix(),
            "slot_key": key,
            "terminal_status": slot["terminal_status"],
        },
    }


def run() -> dict[str, Any]:
    manifest, _manifest_raw = load_unique_json(INPUT_PATH)
    if manifest.get("schema") != "ice-phase46-u2-state-map-fd-audit-inputs/v1":
        raise InvalidRun("Phase46 input schema drift")
    input_validation = validate_frozen_inputs(manifest)

    progress("load pinned Phase-42 context and Phase-43 independent reference")
    phase42 = load_module("ice_phase42_for_phase46", PHASE42_SCRIPT_PATH)
    phase43 = load_module("ice_phase43_for_phase46", PHASE43_SCRIPT_PATH)
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
    phase45_result, _ = load_unique_json(PHASE45_RESULT_PATH)

    numerics = manifest["fixed_numerics"]
    thresholds = manifest["fixed_metrics_and_thresholds"]
    steps = [float(value) for value in numerics["central_difference_steps_in_order"]]
    signs = [int(value) for value in numerics["perturbation_signs_in_order"]]
    paths = [str(value) for value in numerics["state_paths_in_order"]]
    if steps != [2.0e-6, 5.0e-7, 1.0e-7] or signs != [1, -1]:
        raise InvalidRun("frozen u2 step/sign ladder drift")

    all_historical_reproduced = True
    all_historical_failed = True
    all_precision_probes = True
    all_independent_ladders = True
    all_tight_endpoints = True
    all_radau_endpoints = True
    all_tight_columns = True
    all_radau_columns = True
    all_phase45_columns = True
    points: dict[str, Any] = {}

    for label in manifest["scope"]["targets_in_order"]:
        progress(
            f"{label}: consume 18 pinned source endpoints and solve "
            "6 independent state maps"
        )
        point = context.points[label]
        evaluator = phase43.make_reference_evaluators(
            format(point.source_point[0], ".17g"),
            format(point.source_point[1], ".17g"),
        )
        with mp.workdps(120):
            saddle_mp = [
                phase43.mp_complex_from_binary64(item)
                for item in point.saddle.saddle_w
            ]
            linear_mp = phase43.mp_real_matrix_from_numpy(context.fixed.linear_map)

        retained: dict[str, dict[str, Any]] = {name: {} for name in paths}
        precision_probes: list[dict[str, Any]] = []
        for step in steps:
            for sign in signs:
                slot = f"h={step:.1e},sign={sign:+d}"
                parameters = point.parameters.copy()
                parameters[8] += sign * step
                for path_name in paths:
                    if path_name == "independent_exact_80dps_dop853":
                        progress(f"{label}: {slot} newly integrate {path_name}")
                        record = integrate_one(
                            phase42,
                            phase43,
                            context,
                            point,
                            parameters,
                            path_name,
                            numerics["state_solvers"][path_name],
                            evaluator,
                            saddle_mp,
                            linear_mp,
                            int(numerics["independent_rhs_dps"]),
                        )
                    else:
                        record = retained_phase42_state_map(
                            phase42_result, label, path_name, step, sign
                        )
                    retained[path_name][slot] = record
                    if path_name == "independent_exact_80dps_dop853":
                        for location, xi in (
                            ("launch", record["initial_xi"]),
                            ("endpoint", record["endpoint_xi"]),
                        ):
                            rhs50 = independent_flow_rhs(
                                phase43, evaluator, saddle_mp, linear_mp, xi, 50
                            )
                            rhs80 = independent_flow_rhs(
                                phase43, evaluator, saddle_mp, linear_mp, xi, 80
                            )
                            precision_probes.append(
                                {
                                    "slot": slot,
                                    "location": location,
                                    "relative_50dps_to_80dps": symmetric_relative(
                                        rhs50, rhs80
                                    ),
                                }
                            )

        columns: dict[str, list[np.ndarray]] = {}
        plateaus: dict[str, list[float]] = {}
        for path_name in paths:
            path_columns: list[np.ndarray] = []
            for step in steps:
                plus = retained[path_name][f"h={step:.1e},sign=+1"]["residual"]
                minus = retained[path_name][f"h={step:.1e},sign=-1"]["residual"]
                path_columns.append((plus - minus) / (2.0 * step))
            columns[path_name] = path_columns
            plateaus[path_name] = [
                phase41_plateau(first, second)
                for first, second in zip(path_columns[:-1], path_columns[1:])
            ]

        historical = phase42_result["phase41_negative_control"]["points"][label]
        historical_plateau = float(historical["u2_plateau"])
        production_plateau = plateaus["production_source_dop853"][0]
        historical_error = abs(production_plateau - historical_plateau)
        precision_probe_max = max(
            item["relative_50dps_to_80dps"] for item in precision_probes
        )
        independent_plateau_max = max(
            plateaus["independent_exact_80dps_dop853"]
        )

        endpoint_metrics: dict[str, list[dict[str, Any]]] = {
            "tight_source_dop853": [],
            "tight_source_radau": [],
        }
        for source_path in endpoint_metrics:
            for step in steps:
                for sign in signs:
                    slot = f"h={step:.1e},sign={sign:+d}"
                    endpoint_metrics[source_path].append(
                        {
                            "slot": slot,
                            "relative_to_independent": symmetric_relative(
                                retained[source_path][slot]["endpoint_state_z"],
                                retained["independent_exact_80dps_dop853"][slot][
                                    "endpoint_state_z"
                                ],
                            ),
                        }
                    )
        tight_endpoint_max = max(
            item["relative_to_independent"]
            for item in endpoint_metrics["tight_source_dop853"]
        )
        radau_endpoint_max = max(
            item["relative_to_independent"]
            for item in endpoint_metrics["tight_source_radau"]
        )
        tight_column_relatives = [
            symmetric_relative(source, reference)
            for source, reference in zip(
                columns["tight_source_dop853"],
                columns["independent_exact_80dps_dop853"],
            )
        ]
        radau_column_relatives = [
            symmetric_relative(source, reference)
            for source, reference in zip(
                columns["tight_source_radau"],
                columns["independent_exact_80dps_dop853"],
            )
        ]
        phase45_jacobian = np.asarray(
            phase45_result["points"][label]["root_jacobians"][
                "independent_exact_80dps"
            ],
            dtype=np.float64,
        )
        phase45_u2_column = phase45_jacobian[:, 8]
        phase45_column_relatives = [
            symmetric_relative(column, phase45_u2_column)
            for column in columns["independent_exact_80dps_dop853"]
        ]

        tests = {
            "historical_production_plateau_reproduced": historical_error
            <= float(thresholds["historical_u2_plateau_reproduction_absolute_max"]),
            "historical_production_plateau_fails": historical_plateau
            > float(thresholds["historical_u2_plateau_failure_threshold"]),
            "independent_precision_probes_pass": precision_probe_max
            <= float(
                thresholds["independent_50dps_to_80dps_rhs_probe_relative_max"]
            ),
            "independent_full_ladder_passes": independent_plateau_max
            <= float(thresholds["stable_adjacent_step_relative_change_max"]),
            "tight_source_endpoints_agree": tight_endpoint_max
            <= float(thresholds["tight_source_endpoint_to_independent_relative_max"]),
            "radau_source_endpoints_agree": radau_endpoint_max
            <= float(thresholds["radau_source_endpoint_to_independent_relative_max"]),
            "tight_source_columns_agree": max(tight_column_relatives)
            <= float(thresholds["tight_source_D2_to_independent_relative_max"]),
            "radau_source_columns_agree": max(radau_column_relatives)
            <= float(thresholds["radau_source_D2_to_independent_relative_max"]),
            "independent_columns_agree_with_phase45_tangent": max(
                phase45_column_relatives
            )
            <= float(
                thresholds[
                    "independent_D2_to_phase45_tangent_column_relative_max"
                ]
            ),
        }
        all_historical_reproduced &= tests[
            "historical_production_plateau_reproduced"
        ]
        all_historical_failed &= tests["historical_production_plateau_fails"]
        all_precision_probes &= tests["independent_precision_probes_pass"]
        all_independent_ladders &= tests["independent_full_ladder_passes"]
        all_tight_endpoints &= tests["tight_source_endpoints_agree"]
        all_radau_endpoints &= tests["radau_source_endpoints_agree"]
        all_tight_columns &= tests["tight_source_columns_agree"]
        all_radau_columns &= tests["radau_source_columns_agree"]
        all_phase45_columns &= tests[
            "independent_columns_agree_with_phase45_tangent"
        ]

        points[label] = {
            "source_point": list(point.source_point),
            "base_parameters": point.parameters,
            "steps": steps,
            "retained_state_maps": retained,
            "finite_difference_columns_by_step": columns,
            "adjacent_plateaus": plateaus,
            "precision_probes": precision_probes,
            "endpoint_metrics": endpoint_metrics,
            "phase45_independent_tangent_u2_column": phase45_u2_column,
            "metrics": {
                "historical_phase41_u2_plateau": historical_plateau,
                "recomputed_production_first_pair_plateau": production_plateau,
                "historical_reproduction_absolute_error": historical_error,
                "independent_precision_probe_relative_max": precision_probe_max,
                "independent_full_ladder_plateau_max": independent_plateau_max,
                "tight_source_endpoint_to_independent_relative_max": tight_endpoint_max,
                "radau_source_endpoint_to_independent_relative_max": radau_endpoint_max,
                "tight_source_columns_to_independent_relative_max": max(
                    tight_column_relatives
                ),
                "radau_source_columns_to_independent_relative_max": max(
                    radau_column_relatives
                ),
                "independent_columns_to_phase45_tangent_relative_max": max(
                    phase45_column_relatives
                ),
                "per_step_tight_source_column_relatives": tight_column_relatives,
                "per_step_radau_source_column_relatives": radau_column_relatives,
                "per_step_independent_to_phase45_tangent_relatives": phase45_column_relatives,
            },
            "tests": tests,
        }

    independent_prerequisites = all(
        (
            all_historical_reproduced,
            all_historical_failed,
            all_precision_probes,
            all_independent_ladders,
            all_phase45_columns,
        )
    )
    source_agreement = all(
        (
            all_tight_endpoints,
            all_radau_endpoints,
            all_tight_columns,
            all_radau_columns,
        )
    )
    labels = manifest["classification"]
    if independent_prerequisites and source_agreement:
        classification = labels["production_artifact_label"]
    elif independent_prerequisites and not source_agreement:
        classification = labels["local_rhs_repair_label"]
    else:
        classification = labels["inconclusive_label"]

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 46,
        "run_status": "VALID_RUN",
        "classification": classification,
        "aggregate_tests": {
            "all_historical_production_plateaus_reproduced": all_historical_reproduced,
            "all_historical_production_plateaus_fail": all_historical_failed,
            "all_independent_precision_probes_pass": all_precision_probes,
            "all_independent_full_ladders_pass": all_independent_ladders,
            "all_tight_source_endpoints_agree": all_tight_endpoints,
            "all_radau_source_endpoints_agree": all_radau_endpoints,
            "all_tight_source_columns_agree": all_tight_columns,
            "all_radau_source_columns_agree": all_radau_columns,
            "all_independent_columns_agree_with_phase45_tangent": all_phase45_columns,
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
            "phase": 46,
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
