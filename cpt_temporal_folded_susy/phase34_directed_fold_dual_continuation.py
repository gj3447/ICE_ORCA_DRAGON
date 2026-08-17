#!/usr/bin/env python3
"""Phase 34 -- directed reduced-dual continuation through the P25 fold.

This executable follows the reflection-symmetric fixed-boundary stationary
family through the real Dirichlet fold of Phases 25 and 33.  It fixes the
soft-coordinate orientation, seeds the conjugate complex sheets from the
Airy 3/2 law, and continues the upper constant-Im W branch at fixed Re T.
In the declared flat complex-T metric that branch is pointwise parallel to
the reduced dual field ``dT/ds=-conj(W_T)``.

The calculation is deliberately a bounded, reduced stationary-family test.
It does not integrate the full joint field--lapse Picard--Lefschetz flow,
transport a determinant line, enumerate all sheets, or assign a global
intersection coefficient.  The script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import root

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase26_global_lapse_flow as p26
    from . import phase33_fold_airy_uniformization as p33
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase26_global_lapse_flow as p26
    import phase33_fold_airy_uniformization as p33


SEED_DELTA = 2.0e-4
SEED_TAU = 2.0e-4
SMALL_STEP = 0.01
LARGE_STEP = 0.04
ROBUST_MAX_REAL_T = 13.0
SELECTED_SMALL_TAUS = (
    2.0e-4,
    1.0e-3,
    2.0e-3,
    5.0e-3,
    1.0e-2,
    2.0e-2,
    5.0e-2,
    1.0e-1,
    2.0e-1,
    5.0e-1,
    1.0,
    1.7,
)


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

    def _unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"duplicate check id: {check_id}")

    def exact(self, check_id: str, condition: bool, statement: str) -> None:
        self._unique(check_id)
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[PASS] {check_id}: {statement}")

    def numerical(self, check_id: str, condition: bool, statement: str) -> None:
        self._unique(check_id)
        if not condition:
            raise AssertionError(f"[NUMERIC FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")


def deterministic_right_null(vector: np.ndarray) -> np.ndarray:
    """Normalize the fold null vector and orient it toward increasing a_c."""

    oriented = np.asarray(vector, dtype=float).copy()
    if oriented.shape != (2,) or not np.all(np.isfinite(oriented)):
        raise ValueError("the soft vector must be a finite two-vector")
    if oriented[0] == 0.0:
        raise ValueError("the increasing-a_c orientation is undefined")
    if oriented[0] < 0.0:
        oriented = -oriented
    return oriented / np.linalg.norm(oriented)


def exact_controls(audit: Audit) -> dict[str, object]:
    test_vector = np.array([3.0, -4.0])
    oriented = deterministic_right_null(test_vector)
    opposite = deterministic_right_null(-test_vector)
    audit.exact(
        "P34.orientation.deterministic_soft_vector",
        np.array_equal(oriented, opposite)
        and oriented[0] > 0.0
        and np.array_equal(oriented, np.array([0.6, -0.8])),
        "v_R and -v_R give the same unit soft vector with positive a_c component",
    )

    tau, action_coefficient, energy_scale, soft_radius = sp.symbols(
        "tau C m R", positive=True, real=True
    )
    kappa = action_coefficient / (2 * energy_scale)
    regular_imaginary_action = -energy_scale * kappa * tau ** sp.Rational(3, 2)
    singular_imaginary_action = (
        action_coefficient * tau ** sp.Rational(3, 2) / 2
    )
    audit.exact(
        "P34.seed.Airy_three_halves_constant_phase",
        sp.simplify(regular_imaginary_action + singular_imaginary_action)
        == 0,
        "kappa=C/(2|W_Tc|) cancels the leading imaginary action on the upper fold sheet",
    )

    imaginary_derivative = sp.symbols("b", real=True)
    derivative = -energy_scale + sp.I * imaginary_derivative
    slope = -sp.im(derivative) / sp.re(derivative)
    tangent = 1 + sp.I * slope
    dual = -sp.conjugate(derivative)
    action_change = sp.expand_complex(derivative * tangent)
    audit.exact(
        "P34.flow.constant_phase_is_reduced_dual",
        sp.simplify(dual - energy_scale * tangent) == 0
        and sp.simplify(sp.im(action_change)) == 0
        and sp.simplify(
            sp.re(action_change)
            + (energy_scale**2 + imaginary_derivative**2) / energy_scale
        )
        == 0,
        "for Re W_T<0, y'=-Im W_T/Re W_T is a positive reparametrization of -conj(W_T)",
    )

    fold_time = sp.symbols("T_c", real=True)
    upper_time = (
        fold_time + tau + sp.I * kappa * tau ** sp.Rational(3, 2)
    )
    upper_soft = -sp.I * soft_radius * sp.sqrt(tau)
    audit.exact(
        "P34.conjugation.upper_lower_fold_arms",
        sp.conjugate(upper_time)
        == fold_time - sp.I * kappa * tau ** sp.Rational(3, 2) + tau
        and sp.conjugate(upper_soft) == sp.I * soft_radius * sp.sqrt(tau),
        "real coefficients pair the upper T arm and Im u<0 sheet with their lower conjugates",
    )

    delta = sp.symbols("delta", positive=True, real=True)
    projected_speed = sp.symbols("v_T", positive=True, real=True)
    delta_speed = -projected_speed
    real_soft_plus = soft_radius * sp.sqrt(delta)
    real_soft_minus = -soft_radius * sp.sqrt(delta)
    plus_speed = sp.diff(real_soft_plus, delta) * delta_speed
    minus_speed = sp.diff(real_soft_minus, delta) * delta_speed
    audit.exact(
        "P34.flow.both_real_sheets_enter_fold",
        sp.simplify(real_soft_plus * plus_speed)
        == -projected_speed * soft_radius**2 / 2
        and sp.simplify(real_soft_minus * minus_speed)
        == -projected_speed * soft_radius**2 / 2,
        "u=plus/minus R sqrt(T_c-T) both move toward u=0 when the projected dual has dT/ds>0",
    )

    return {
        "soft_coordinate": (
            "u=v_R^T(center-center_c), with ||v_R||=1 and (v_R)_a>0"
        ),
        "upper_seed": (
            "T=T_c+tau+i[C/(2|W_Tc|)]tau^(3/2), "
            "u=-i R sqrt(tau)"
        ),
        "lower_seed": "the complex conjugate of the upper seed",
        "constant_phase_slope": "d(Im T)/d(Re T)=-Im(W_T)/Re(W_T)",
        "declared_reduced_dual": "dT/ds=-conj(W_T) in the flat complex-T metric",
        "metric_scope": (
            "a positive scalar Hermitian rescaling changes only the parameter; "
            "the full joint field-lapse metric and flow are not computed"
        ),
    }


def complex_variational_matrix(state: np.ndarray) -> np.ndarray:
    """Holomorphic continuation of the Phase-25 4x4 variational matrix."""

    scale, scale_velocity, phi, phi_velocity = state[:4]
    return np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [
                -(1.0 - scale_velocity**2) / (2.0 * scale**2)
                - phi_velocity**2 / 4.0
                - p25.potential(phi) / 2.0,
                -scale_velocity / scale,
                -scale * p25.potential_prime(phi) / 2.0,
                -scale * phi_velocity / 2.0,
            ],
            [0.0, 0.0, 0.0, 1.0],
            [
                3.0 * scale_velocity * phi_velocity / scale**2,
                -3.0 * phi_velocity / scale,
                p25.potential_second(phi),
                -3.0 * scale_velocity / scale,
            ],
        ],
        dtype=np.complex128,
    )


def symmetric_half_flow(proper_length: complex, center: np.ndarray) -> np.ndarray:
    """Integrate from the reflection center to the right boundary."""

    initial = np.array(
        [center[0], 0.0j, center[1], 0.0j, 0.0j], dtype=np.complex128
    )

    def rhs(_s: float, augmented: np.ndarray) -> np.ndarray:
        state = augmented[:4]
        return proper_length * np.concatenate(
            [
                p25.configuration_rhs(state),
                [p25.action_lagrangian(state)],
            ]
        ) / 2.0

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        initial,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=0.025,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1]


def symmetric_residual(
    unknown: np.ndarray, real_time: float, boundary: np.ndarray
) -> np.ndarray:
    proper_length = complex(real_time, unknown[0])
    center = np.array(
        [
            complex(unknown[1], unknown[2]),
            complex(unknown[3], unknown[4]),
        ]
    )
    half_final = symmetric_half_flow(proper_length, center)
    endpoint_delta = half_final[[0, 2]] - boundary[:2]
    return np.array(
        [
            endpoint_delta[0].real,
            endpoint_delta[0].imag,
            endpoint_delta[1].real,
            endpoint_delta[1].imag,
            (2.0 * half_final[4]).imag,
        ]
    )


def solve_symmetric_constant_phase(
    real_time: float, boundary: np.ndarray, guess: np.ndarray
) -> tuple[np.ndarray, float]:
    solved = root(
        lambda unknown: symmetric_residual(unknown, real_time, boundary),
        guess,
        method="hybr",
        tol=1e-10,
        options={"maxfev": 500},
    )
    residual_norm = float(
        np.linalg.norm(symmetric_residual(solved.x, real_time, boundary))
    )
    if not np.all(np.isfinite(solved.x)) or residual_norm > 5e-8:
        raise RuntimeError(
            f"symmetric constant-phase solve failed at Re T={real_time}: "
            f"{residual_norm}; {solved.message}"
        )
    return solved.x.copy(), residual_norm


def full_flow_and_variation(
    proper_length: complex, boundary: np.ndarray, velocity: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the full complex BVP together with its 4x4 Jacobi map."""

    state = np.array(
        [boundary[0], velocity[0], boundary[1], velocity[1]],
        dtype=np.complex128,
    )
    initial = np.concatenate(
        [state, [0.0j], np.eye(4, dtype=np.complex128).ravel()]
    )

    def rhs(_s: float, augmented: np.ndarray) -> np.ndarray:
        configuration = augmented[:4]
        matrix = augmented[5:].reshape(4, 4)
        return proper_length * np.concatenate(
            [
                p25.configuration_rhs(configuration),
                [p25.action_lagrangian(configuration)],
                (complex_variational_matrix(configuration) @ matrix).ravel(),
            ]
        )

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        initial,
        method="DOP853",
        rtol=2e-11,
        atol=2e-13,
        max_step=0.025,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]
    return final[:5], final[5:].reshape(4, 4)


def pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def p33_seed_data(
    boundary: np.ndarray, fold: dict[str, object], right_null: np.ndarray
) -> dict[str, object]:
    branches = p33.solve_two_branches(boundary, fold, SEED_DELTA)
    lower, upper = branches
    action_gap = abs(float(upper["action"]) - float(lower["action"]))
    action_coefficient = action_gap / SEED_DELTA**1.5
    center_difference = np.asarray(upper["center"]) - np.asarray(
        lower["center"]
    )
    soft_radius = float(center_difference @ right_null) / (
        2.0 * np.sqrt(SEED_DELTA)
    )

    fold_center = np.asarray(fold["center"], dtype=float)
    fold_time = float(fold["proper_length"])
    fold_endpoint, _ = p25.midpoint_endpoint(fold_center, fold_time)
    fold_solution = p25.solve_fixed_time(
        fold_time, boundary, -fold_endpoint[[1, 3]]
    )
    fold_w_t = float(-fold_solution.energy)
    kappa = action_coefficient / (2.0 * abs(fold_w_t))

    real_sheets: list[dict[str, object]] = []
    for branch in branches:
        center = np.asarray(branch["center"], dtype=float)
        endpoint, _ = p25.midpoint_endpoint(center, fold_time - SEED_DELTA)
        solution = p25.solve_fixed_time(
            fold_time - SEED_DELTA,
            boundary,
            -endpoint[[1, 3]],
        )
        real_sheets.append(
            {
                "center": center.tolist(),
                "u": float(right_null @ (center - fold_center)),
                "W": float(solution.action),
                "W_T": float(-solution.energy),
                "endpoint_residual": float(solution.endpoint_residual),
            }
        )

    return {
        "seed_delta": SEED_DELTA,
        "action_gap": action_gap,
        "action_gap_coefficient": action_coefficient,
        "soft_radius_coefficient": soft_radius,
        "fold_W_T": fold_w_t,
        "kappa": kappa,
        "real_sheets": real_sheets,
    }


def selected_taus(fold_time: float) -> tuple[float, ...]:
    final_taus = (12.0 - fold_time, ROBUST_MAX_REAL_T - fold_time)
    return tuple(sorted(set(SELECTED_SMALL_TAUS + final_taus)))


def point_record(
    tau: float,
    fold_time: float,
    fold_center: np.ndarray,
    right_null: np.ndarray,
    boundary: np.ndarray,
    unknown: np.ndarray,
    root_residual: float,
) -> dict[str, object]:
    proper_length = complex(fold_time + tau, unknown[0])
    center = np.array(
        [
            complex(unknown[1], unknown[2]),
            complex(unknown[3], unknown[4]),
        ]
    )
    half_final = symmetric_half_flow(proper_length, center)
    velocity = -half_final[[1, 3]]
    action = complex(2.0 * half_final[4])
    derivative = p26.complex_w_derivative(boundary, velocity)
    full_final, monodromy = full_flow_and_variation(
        proper_length, boundary, velocity
    )
    velocity_block = monodromy[np.ix_([0, 2], [1, 3])]
    singular_values = np.linalg.svd(velocity_block, compute_uv=False)

    lower_final, _ = full_flow_and_variation(
        np.conjugate(proper_length), boundary, np.conjugate(velocity)
    )
    slope = float(-derivative.imag / derivative.real)
    soft_coordinate = complex(right_null @ (center - fold_center))

    return {
        "tau": float(tau),
        "T": pair(proper_length),
        "center": [pair(center[0]), pair(center[1])],
        "u": pair(soft_coordinate),
        "W": pair(action),
        "W_T": pair(derivative),
        "constant_phase_slope": slope,
        "root_residual": float(root_residual),
        "full_endpoint_residual": float(
            np.linalg.norm(full_final[[0, 2]] - boundary[2:])
        ),
        "sigma_min_Bv": float(singular_values[-1]),
        "det_Bv": pair(complex(np.linalg.det(velocity_block))),
        "lower_T": pair(np.conjugate(proper_length)),
        "lower_center": [pair(np.conjugate(center[0])), pair(np.conjugate(center[1]))],
        "lower_endpoint_residual": float(
            np.linalg.norm(lower_final[[0, 2]] - boundary[2:])
        ),
        "conjugation_residual": float(
            np.linalg.norm(lower_final - np.conjugate(full_final))
        ),
    }


def continue_upper_arm(
    boundary: np.ndarray,
    fold: dict[str, object],
    right_null: np.ndarray,
    seed: dict[str, object],
) -> list[dict[str, object]]:
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    soft_radius = float(seed["soft_radius_coefficient"])
    kappa = float(seed["kappa"])

    center_seed = (
        fold_center
        - 1.0j * soft_radius * np.sqrt(SEED_TAU) * right_null
    )
    unknown = np.array(
        [
            kappa * SEED_TAU**1.5,
            center_seed[0].real,
            center_seed[0].imag,
            center_seed[1].real,
            center_seed[1].imag,
        ]
    )

    targets = selected_taus(fold_time)
    current_tau = SEED_TAU
    unknown, residual = solve_symmetric_constant_phase(
        fold_time + current_tau, boundary, unknown
    )
    records = [
        point_record(
            current_tau,
            fold_time,
            fold_center,
            right_null,
            boundary,
            unknown,
            residual,
        )
    ]

    for target in targets[1:]:
        final_residual = residual
        while target - current_tau > 1e-13:
            step = SMALL_STEP if current_tau < 0.1 else LARGE_STEP
            next_tau = min(target, current_tau + step)
            unknown, final_residual = solve_symmetric_constant_phase(
                fold_time + next_tau, boundary, unknown
            )
            current_tau = next_tau
        records.append(
            point_record(
                target,
                fold_time,
                fold_center,
                right_null,
                boundary,
                unknown,
                final_residual,
            )
        )
    return records


def unknown_from_record(record: dict[str, object]) -> np.ndarray:
    center = record["center"]
    return np.array(
        [
            float(record["T"][1]),
            float(center[0][0]),
            float(center[0][1]),
            float(center[1][0]),
            float(center[1][1]),
        ]
    )


def center_from_unknown(unknown: np.ndarray) -> np.ndarray:
    return np.array(
        [
            complex(unknown[1], unknown[2]),
            complex(unknown[3], unknown[4]),
        ]
    )


def computed_curve_derivatives(
    records: list[dict[str, object]],
    boundary: np.ndarray,
    fold_time: float,
    fold_center: np.ndarray,
    right_null: np.ndarray,
) -> list[dict[str, float]]:
    """Differentiate independently re-solved nearby BVPs, not the HJ formula."""

    requested_taus = (0.001, 0.01, 0.1, 0.5, 1.7, 12.0 - fold_time)
    records_by_tau = {round(float(record["tau"]), 12): record for record in records}
    checks: list[dict[str, float]] = []
    for tau in requested_taus:
        record = records_by_tau[round(float(tau), 12)]
        center_unknown = unknown_from_record(record)
        step = min(1.0e-3, max(1.0e-5, 1.0e-2 * tau))
        minus_unknown, minus_residual = solve_symmetric_constant_phase(
            fold_time + tau - step,
            boundary,
            center_unknown,
        )
        plus_unknown, plus_residual = solve_symmetric_constant_phase(
            fold_time + tau + step,
            boundary,
            center_unknown,
        )

        numerical_slope = float(
            (plus_unknown[0] - minus_unknown[0]) / (2.0 * step)
        )
        hj_slope = float(record["constant_phase_slope"])
        relative_slope_error = abs(numerical_slope - hj_slope) / max(
            1.0, abs(hj_slope)
        )

        center = center_from_unknown(center_unknown)
        minus_center = center_from_unknown(minus_unknown)
        plus_center = center_from_unknown(plus_unknown)
        center_jump = max(
            float(np.linalg.norm(minus_center - center)),
            float(np.linalg.norm(plus_center - center)),
        )
        center_midpoint_error = float(
            np.linalg.norm((minus_center + plus_center) / 2.0 - center)
        )
        minus_soft = complex(right_null @ (minus_center - fold_center))
        plus_soft = complex(right_null @ (plus_center - fold_center))
        checks.append(
            {
                "tau": float(tau),
                "centered_step": float(step),
                "numerical_dImT_dtau": numerical_slope,
                "HJ_constant_phase_slope": hj_slope,
                "relative_slope_error": float(relative_slope_error),
                "nearby_root_residual_max": max(minus_residual, plus_residual),
                "center_jump_max": center_jump,
                "center_midpoint_error": center_midpoint_error,
                "minus_ImT": float(minus_unknown[0]),
                "plus_ImT": float(plus_unknown[0]),
                "minus_Imu": float(minus_soft.imag),
                "plus_Imu": float(plus_soft.imag),
            }
        )
    return checks


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, _velocity, _action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    right_null = deterministic_right_null(
        np.asarray(fold["right_null_vector"], dtype=float)
    )
    seed = p33_seed_data(boundary, fold, right_null)
    records = continue_upper_arm(boundary, fold, right_null, seed)
    derivative_checks = computed_curve_derivatives(
        records,
        boundary,
        fold_time,
        fold_center,
        right_null,
    )

    audit.numerical(
        "P34.seed.frozen_P33_coefficients",
        abs(float(seed["action_gap_coefficient"]) - 93.02721) < 8e-4
        and abs(float(seed["soft_radius_coefficient"]) - 1.185174) < 8e-5
        and abs(float(seed["fold_W_T"]) + 73.72585376) < 2e-6
        and abs(float(seed["kappa"]) - 0.6308995) < 2e-6,
        "the directed seed is reconstructed from the last P33 action-gap, soft-radius, and fold W_T data",
    )

    real_sheets = seed["real_sheets"]
    audit.numerical(
        "P34.flow.actual_real_sheets_enter_fold",
        float(real_sheets[0]["u"]) < 0.0 < float(real_sheets[1]["u"])
        and all(float(sheet["W_T"]) < -70.0 for sheet in real_sheets)
        and max(float(sheet["endpoint_residual"]) for sheet in real_sheets)
        < 2e-8,
        "both actual real sheets have W_T<0 and their projected dual orientation points toward the fold",
    )

    audit.numerical(
        "P34.continuation.actual_complex_BVP",
        max(float(record["root_residual"]) for record in records) < 5e-8
        and max(float(record["full_endpoint_residual"]) for record in records)
        < 8e-8,
        "every frozen upper-arm point solves the symmetric root system and the independently reintegrated full endpoint problem",
    )

    audit.numerical(
        "P34.continuation.constant_ImW_and_decreasing_ReW",
        max(abs(float(record["W"][1])) for record in records) < 5e-8
        and all(float(record["W_T"][0]) < 0.0 for record in records)
        and np.all(np.diff([float(record["W"][0]) for record in records]) < 0.0),
        "the upper branch keeps Im W fixed while Re W and Re W_T remain decreasing and negative",
    )

    audit.numerical(
        "P34.flow.computed_curve_derivative",
        max(check["relative_slope_error"] for check in derivative_checks)
        < 2e-5
        and max(check["nearby_root_residual_max"] for check in derivative_checks)
        < 5e-8
        and max(check["center_jump_max"] for check in derivative_checks) < 0.01
        and max(check["center_midpoint_error"] for check in derivative_checks)
        < 2e-5
        and all(
            check["minus_ImT"] < check["plus_ImT"]
            and check["minus_Imu"] < 0.0
            and check["plus_Imu"] < 0.0
            for check in derivative_checks
        ),
        "centered differences of independently re-solved nearby BVPs agree with -Im(W_T)/Re(W_T) and stay on the upper branch",
    )

    small_records = [record for record in records if record["tau"] <= 0.01]
    seed_ratios = np.array(
        [
            float(record["T"][1]) / float(record["tau"]) ** 1.5
            for record in small_records
        ]
    )
    fitted_exponent = float(
        np.polyfit(
            np.log([float(record["tau"]) for record in small_records]),
            np.log([float(record["T"][1]) for record in small_records]),
            1,
        )[0]
    )
    audit.numerical(
        "P34.seed.imaginary_time_three_halves",
        abs(seed_ratios[0] - float(seed["kappa"])) < 1e-5
        and np.all(np.diff(seed_ratios) < 0.0)
        and abs(fitted_exponent - 1.5) < 5e-4,
        "Im T/tau^(3/2) converges to the P33 seed coefficient at the fold",
    )

    audit.numerical(
        "P34.conjugation.lower_arm",
        max(float(record["lower_endpoint_residual"]) for record in records)
        < 8e-8
        and max(float(record["conjugation_residual"]) for record in records)
        < 2e-10,
        "complex conjugation supplies a lower constant-phase endpoint branch with the same bounded accuracy",
    )

    audit.numerical(
        "P34.Jacobi.no_sampled_complex_zero",
        min(float(record["sigma_min_Bv"]) for record in records) > 0.04
        and all(
            np.isfinite(float(record["sigma_min_Bv"])) for record in records
        ),
        "the sampled complex continuation has no endpoint-Jacobi zero (not a proof for unsampled points or modes)",
    )

    audit.numerical(
        "P34.intersection.bounded_lapse_base_disjointness",
        min(float(record["T"][0]) for record in records) > fold_time
        and max(float(record["T"][0]) for record in records)
        <= ROBUST_MAX_REAL_T + 2e-12
        and min(abs(complex(*record["T"])) for record in records) > 9.0,
        "the monotone-ReT bounded arms remain disjoint from the imaginary T axis and every Phase32 cap with r<=0.1",
    )

    return {
        "boundary": boundary.tolist(),
        "fold": {
            "T_c": fold_time,
            "center": fold_center.tolist(),
            "right_null_oriented": right_null.tolist(),
        },
        "seed": seed,
        "small_tau_seed_ratios": seed_ratios.tolist(),
        "small_tau_fitted_exponent": fitted_exponent,
        "computed_curve_derivative_checks": derivative_checks,
        "robust_max_ReT": ROBUST_MAX_REAL_T,
        "records": records,
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P34",
        "calculation": "bounded directed fold continuation of the reduced stationary family",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_right_projected_dual_has_a_bounded_reduced_continuation_through_the_fold": "SUPPORTED_THROUGH_ReT_13_ON_THE_TRACKED_STATIONARY_FAMILY",
            "the_continuation_adds_a_crossing_with_the_Phase32_lapse_base_contour": "NOT_SEEN_ON_THE_BOUNDED_TRACKED_ARMS",
            "the_sampled_complex_arm_contains_another_endpoint_Jacobi_zero": "NOT_SEEN_AT_THE_FROZEN_POINTS",
            "this_is_the_full_joint_field_lapse_dual": "OPEN_NOT_COMPUTED",
            "the_global_intersection_coefficient_n_sigma_is_fixed": "OPEN_REQUIRES_COMPLETE_RELATIVE_CYCLES_AND_DETERMINANT_LINE",
            "all_complex_sheets_and_good_ends_are_enumerated": "OPEN_NOT_COMPUTED",
        },
        "scope_guard": {
            "computed": [
                "the deterministic P25 soft-vector orientation",
                "the P33 Airy 3/2 seed and its numerical convergence",
                "upper and lower reflection-symmetric constant-ImW fixed-boundary sheets",
                "pointwise alignment with -conj(W_T) in the declared reduced flat T metric",
                "endpoint Jacobi singular values on a table bounded by ReT<=13",
                "lapse-base disjointness from the Phase32 imaginary axis and r<=0.1 caps on that bounded table",
            ],
            "not_computed": [
                "the full joint field-lapse gradient flow or its metric",
                "an oriented Airy connection matrix or determinant-line transport",
                "all complex sheets, unsampled Jacobi zeros, good ends, or infinity",
                "a global Picard-Lefschetz intersection coefficient",
                "inhomogeneous fluctuations, a WDW density, or a physical quantum state",
            ],
        },
        "next_calculation": (
            "lift one regulated field-lapse relative cycle and its determinant line, "
            "then continue every joint dual arm and good end"
        ),
    }
    print("PHASE34_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
