#!/usr/bin/env python3
"""Phase 26 -- global complex-lapse flow on the connected interval.

This executable continues the Phase-25 complex fixed-boundary saddle well
beyond its local constant-phase segment.  It keeps the calculation on one
explicit reflection-symmetric analytic sheet, verifies the Picard--Lefschetz
flow sign for ``exp(-W)``, records a projection turn and a bounded return
segment, and checks the independent real fold against the Airy 3/2 law.

The recorded complex arm is deliberately stopped at a large shooting-data
norm.  That stop is not promoted to a theorem about its endpoint.  Nor does
this script assign an intersection number: the original Lorentzian contour,
the zero-lapse bypass, the Faddeev--Popov measure, and the bulk determinant are
separate gates (treated at short time in Phase 27).  The script writes no
files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.optimize import root

try:
    import phase25_connected_lapse_scan as p25
except ModuleNotFoundError:  # Package import; direct execution uses the branch above.
    from . import phase25_connected_lapse_scan as p25


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

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

    def _unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"duplicate check id: {check_id}")


def endpoint_residual(final: np.ndarray, boundary: np.ndarray) -> float:
    return float(np.linalg.norm(final[[0, 2]] - boundary[2:]))


def initial_velocity_from_imag_chart(unknown: np.ndarray) -> np.ndarray:
    return np.array(
        [complex(unknown[1], unknown[2]), complex(unknown[3], unknown[4])]
    )


def complex_w_derivative(boundary: np.ndarray, velocity: np.ndarray) -> complex:
    scale = complex(boundary[0])
    phi = complex(boundary[1])
    scale_velocity, phi_velocity = velocity
    constraint = (
        scale_velocity**2
        - 1.0
        - scale**2
        * (0.5 * phi_velocity**2 - p25.potential(phi))
        / 3.0
    )
    return complex(6.0 * np.pi**2 * scale * constraint)


def constant_phase_at_real_time(
    real_time: float,
    boundary: np.ndarray,
    guess: np.ndarray,
) -> tuple[np.ndarray, complex, np.ndarray]:
    """Continue Im W=0 using Re T as the chart coordinate.

    Unknown order is ``(Im T, Re va, Im va, Re vphi, Im vphi)``.
    """

    def residual(unknown: np.ndarray) -> np.ndarray:
        proper_length = complex(real_time, unknown[0])
        velocity = np.array(
            [
                complex(unknown[1], unknown[2]),
                complex(unknown[3], unknown[4]),
            ]
        )
        final = p25.complex_flow(proper_length, boundary, velocity)
        delta = final[[0, 2]] - boundary[2:]
        return np.array(
            [
                delta[0].real,
                delta[0].imag,
                delta[1].real,
                delta[1].imag,
                final[4].imag,
            ]
        )

    solved = root(residual, guess, method="hybr", tol=1e-11)
    residual_norm = float(np.linalg.norm(residual(solved.x)))
    if not np.all(np.isfinite(solved.x)) or residual_norm > 5e-8:
        raise RuntimeError(
            f"fixed-ReT constant-phase solve failed at {real_time}: "
            f"{residual_norm}"
        )
    unknown = solved.x.copy()
    proper_length = complex(real_time, unknown[0])
    velocity = np.array(
        [complex(unknown[1], unknown[2]), complex(unknown[3], unknown[4])]
    )
    final = p25.complex_flow(proper_length, boundary, velocity)
    return unknown, proper_length, final


def point_record(
    proper_length: complex,
    final: np.ndarray,
    velocity: np.ndarray,
    boundary: np.ndarray,
    chart: str,
) -> dict[str, object]:
    derivative = complex_w_derivative(boundary, velocity)
    return {
        "chart": chart,
        "T": [float(proper_length.real), float(proper_length.imag)],
        "W": [float(final[4].real), float(final[4].imag)],
        "W_T": [float(derivative.real), float(derivative.imag)],
        "velocity": [
            [float(velocity[0].real), float(velocity[0].imag)],
            [float(velocity[1].real), float(velocity[1].imag)],
        ],
        "velocity_norm": float(np.linalg.norm(velocity)),
        "endpoint_residual": endpoint_residual(final, boundary),
    }


def continue_upper_arm(
    boundary: np.ndarray,
    base_velocity: np.ndarray,
) -> list[dict[str, object]]:
    """Continue one upper constant-phase arm through three coordinate charts."""

    base = p25.solve_fixed_time(0.7, boundary, base_velocity)
    imaginary_guess = np.array(
        [0.7, base.velocity[0], 0.0, base.velocity[1], 0.0]
    )
    records: list[dict[str, object]] = []

    imaginary_targets = [
        0.025,
        0.05,
        0.1,
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
        1.25,
        1.5,
        1.75,
        2.0,
        2.1,
        2.2,
        2.3,
        2.35,
        2.4,
        2.425,
        2.45,
        2.46,
        2.47,
        2.474,
        2.4747,
    ]
    for imaginary_time in imaginary_targets:
        imaginary_guess, proper_length, final = p25.constant_phase_point(
            imaginary_time, boundary, imaginary_guess
        )
        velocity = initial_velocity_from_imag_chart(imaginary_guess)
        records.append(
            point_record(proper_length, final, velocity, boundary, "fixed_ImT")
        )

    real_guess = np.array(
        [
            proper_length.imag,
            imaginary_guess[1],
            imaginary_guess[2],
            imaginary_guess[3],
            imaginary_guess[4],
        ]
    )
    real_targets = [
        3.05,
        3.1,
        3.2,
        3.3,
        3.5,
        3.7,
        4.0,
        4.2,
        4.3,
        4.34,
        4.36,
        4.37,
    ]
    for real_time in real_targets:
        real_guess, proper_length, final = constant_phase_at_real_time(
            real_time, boundary, real_guess
        )
        velocity = np.array(
            [
                complex(real_guess[1], real_guess[2]),
                complex(real_guess[3], real_guess[4]),
            ]
        )
        records.append(
            point_record(proper_length, final, velocity, boundary, "fixed_ReT")
        )

    imaginary_guess = np.array(
        [
            proper_length.real,
            real_guess[1],
            real_guess[2],
            real_guess[3],
            real_guess[4],
        ]
    )
    return_targets = [0.98, 0.9, 0.8, 0.7, 0.6]
    for imaginary_time in return_targets:
        imaginary_guess, proper_length, final = p25.constant_phase_point(
            imaginary_time, boundary, imaginary_guess
        )
        velocity = initial_velocity_from_imag_chart(imaginary_guess)
        records.append(
            point_record(
                proper_length,
                final,
                velocity,
                boundary,
                "fixed_ImT_return",
            )
        )

    return records


def exact_controls(audit: Audit) -> dict[str, object]:
    u, v = sp.symbols("u v", real=True)
    derivative = u + sp.I * v
    along_descent = sp.expand(derivative * sp.conjugate(derivative))
    audit.exact(
        "P26.flow.exp_minus_W_sign",
        sp.re(along_descent) == u**2 + v**2
        and sp.im(along_descent) == 0,
        "dT/ds=conj(W_T) increases Re W and preserves Im W",
    )

    mu, x, y = sp.symbols("mu x y", positive=True, real=True)
    local_action = -mu * (x + sp.I * y) ** 2 / 2
    audit.exact(
        "P26.saddle.local_tangents",
        sp.simplify(sp.re(sp.expand_complex(local_action)))
        == mu * (-x**2 + y**2) / 2,
        "negative lapse curvature makes the imaginary tangent convergent for exp(-W)",
    )

    control, soft, b, c = sp.symbols("delta u b c", nonzero=True)
    fold_action = b * control * soft + c * soft**3 / 3
    roots = sp.solve(sp.diff(fold_action, soft), soft)
    action_gap = sp.simplify(
        fold_action.subs(soft, roots[0])
        - fold_action.subs(soft, roots[1])
    )
    audit.exact(
        "P26.fold.Airy_three_halves_law",
        sp.simplify(action_gap**2 + sp.Rational(16, 9) * b**3 * control**3 / c)
        == 0,
        "a generic cubic fold has an action gap proportional to delta^(3/2)",
    )

    # With u=z^3, integral_0^1 sqrt(z)/sqrt(1-z^3) dz
    # becomes B(1/2,1/2)/3 exactly.  Encoding the substitution avoids a
    # version-dependent unevaluated definite Integral in SymPy.
    plateau_integral = sp.beta(sp.Rational(1, 2), sp.Rational(1, 2)) / 3
    plateau_value = sp.simplify(
        2
        * sp.sqrt(3 / sp.Rational(3, 4))
        * plateau_integral.rewrite(sp.gamma)
    )
    audit.exact(
        "P26.asymptotic.plateau_projected_length",
        plateau_value == 4 * sp.pi / 3,
        "the frozen V=3/4 plateau control has projected round-trip length 4pi/3",
    )
    return {
        "flow": "dT/ds=conj(W_T) for the convergent exp(-W) thimble",
        "fold_normal_form": "Phi=b delta u+c u^3/3",
        "plateau_projected_length": "4pi/3",
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, base_velocity, benchmark_action = p25.benchmark()
    base = p25.solve_fixed_time(0.7, boundary, base_velocity)
    audit.numerical(
        "P26.saddle.base",
        abs(base.action - benchmark_action) < 2e-10
        and abs(base.constraint) < 2e-11,
        "the continued arm starts at the frozen T=0.7 lapse saddle",
    )

    arm = continue_upper_arm(boundary, base_velocity)
    actions = np.array([record["W"][0] for record in arm])
    phase_residuals = np.array([abs(record["W"][1]) for record in arm])
    endpoint_residuals = np.array(
        [record["endpoint_residual"] for record in arm]
    )
    audit.numerical(
        "P26.flow.constant_phase_and_monotone_ReW",
        float(np.max(phase_residuals)) < 8e-8
        and float(np.max(endpoint_residuals)) < 8e-8
        and bool(np.all(np.diff(actions) > 0.0))
        and actions[-1] > 4.0e4,
        "the recorded upper arm keeps Im W fixed while Re W rises above 4e4",
    )

    times = np.array(
        [complex(record["T"][0], record["T"][1]) for record in arm]
    )
    derivatives = np.array(
        [
            complex(record["W_T"][0], record["W_T"][1])
            for record in arm
        ]
    )
    alignments = []
    for index in range(1, len(times) - 1):
        tangent = times[index + 1] - times[index - 1]
        flow = np.conjugate(derivatives[index])
        alignments.append(
            float(np.real(np.conjugate(flow) * tangent) / (abs(flow) * abs(tangent)))
        )
    audit.numerical(
        "P26.flow.gradient_alignment",
        min(alignments) > 0.94,
        "the oriented constant-phase curve follows the exp(-W) gradient direction",
    )

    imaginary_parts = np.array([time.imag for time in times])
    turn_index = int(np.argmax(imaginary_parts))
    audit.numerical(
        "P26.flow.projection_turn",
        2.4746 < imaginary_parts[turn_index] < 2.4750
        and 3.03 < times[turn_index].real < 3.11
        and times[-1].imag < 0.7
        and times[-1].real > 4.3,
        "the tracked BVP branch turns in its T-plane projection and returns to smaller Im T",
    )

    velocity_norms = np.array([record["velocity_norm"] for record in arm])
    audit.numerical(
        "P26.flow.field_norm_stop",
        50.0 < velocity_norms[-1] < 80.0,
        "the bounded continuation stops on a declared large shooting-data norm, not a proven endpoint",
    )

    upper = next(
        record
        for record in arm
        if abs(record["T"][1] - 0.4) < 1e-12
        and record["chart"] == "fixed_ImT"
    )
    upper_velocity = np.array(
        [
            complex(upper["velocity"][0][0], upper["velocity"][0][1]),
            complex(upper["velocity"][1][0], upper["velocity"][1][1]),
        ]
    )
    lower_guess = np.array(
        [
            upper["T"][0],
            upper_velocity[0].real,
            -upper_velocity[0].imag,
            upper_velocity[1].real,
            -upper_velocity[1].imag,
        ]
    )
    _, lower_time, lower_final = p25.constant_phase_point(
        -0.4, boundary, lower_guess
    )
    audit.numerical(
        "P26.flow.conjugate_lower_arm",
        abs(lower_time - np.conjugate(complex(*upper["T"]))) < 2e-9
        and abs(lower_final[4] - np.conjugate(complex(*upper["W"]))) < 2e-8,
        "real coefficients and real endpoints give a conjugate lower arm",
    )

    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    fold_center, fold_half = p25.solve_symmetric_center(
        fold_time, boundary, np.asarray(fold["center"], dtype=float)
    )
    fold_solution = p25.solve_fixed_time(
        fold_time, boundary, -fold_half[[1, 3]]
    )
    fold_derivative = -fold_solution.energy
    audit.numerical(
        "P26.fold.not_a_lapse_saddle",
        abs(fold_derivative + 73.72585376) < 3e-6,
        "the real Dirichlet fold has nonzero W_T and is not a new lapse saddle",
    )

    upper_center = np.asarray(fold["bracket_centers"][0], dtype=float)
    lower_center = np.asarray(fold["bracket_centers"][1], dtype=float)
    fold_samples = []
    for proper_length in [9.78, 9.784, 9.786, 9.787, 9.788, 9.7883, 9.7885]:
        upper_center, upper_half = p25.solve_symmetric_center(
            proper_length, boundary, upper_center
        )
        lower_center, lower_half = p25.solve_symmetric_center(
            proper_length, boundary, lower_center
        )
        upper_solution = p25.solve_fixed_time(
            proper_length, boundary, -upper_half[[1, 3]]
        )
        lower_solution = p25.solve_fixed_time(
            proper_length, boundary, -lower_half[[1, 3]]
        )
        delta = fold_time - proper_length
        action_gap = abs(upper_solution.action - lower_solution.action)
        center_gap = float(np.linalg.norm(upper_center - lower_center))
        fold_samples.append(
            {
                "T": proper_length,
                "delta": delta,
                "action_gap": action_gap,
                "action_gap_over_delta_3_2": action_gap / delta**1.5,
                "center_gap_over_sqrt_delta": center_gap / np.sqrt(delta),
            }
        )
    action_ratios = np.array(
        [sample["action_gap_over_delta_3_2"] for sample in fold_samples]
    )
    center_ratios = np.array(
        [sample["center_gap_over_sqrt_delta"] for sample in fold_samples]
    )
    audit.numerical(
        "P26.fold.Airy_scaling",
        abs(action_ratios[-1] - 93.0274) < 8e-3
        and np.ptp(action_ratios[-4:]) < 8e-3
        and abs(center_ratios[-1] - 2.37036) < 8e-4,
        "the two real sheets obey the generic fold action and coordinate scaling laws",
    )

    real_center, real_half = p25.solve_symmetric_center(
        9.78, boundary, np.asarray(fold["bracket_centers"][0])
    )
    real_late = p25.solve_fixed_time(9.78, boundary, -real_half[[1, 3]])
    audit.numerical(
        "P26.contour.positive_real_not_recorded_decay_cycle",
        base.action > 1.0 and real_late.action < -1.0e3,
        "on the recorded real sheet Re W decreases by more than 10^3 before the fold",
    )

    return {
        "boundary": boundary.tolist(),
        "base": {
            "T": 0.7,
            "W": base.action,
            "W_TT": -8.923143038336717,
        },
        "upper_arm": arm,
        "upper_arm_min_gradient_alignment": min(alignments),
        "stop_reason": "FIELD_NORM_CUTOFF_CONTROL",
        "projection_turn": {
            "T": [times[turn_index].real, times[turn_index].imag],
            "W": actions[turn_index],
        },
        "plateau_projected_endpoint_candidate": {
            "T": [float(4 * np.pi / 3), 0.0],
            "status": "EXACT_FOR_THE_FROZEN_PLATEAU_ASYMPTOTIC_CONTROL_ONLY",
        },
        "real_fold": {
            "T_c": fold_time,
            "center": fold_center.tolist(),
            "W_T": fold_derivative,
            "samples": fold_samples,
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P26",
        "calculation": "bounded global complex-lapse flow and real-fold uniform control",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_model": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "a_long_constant_phase_convergent_complex_arm_exists": "SUPPORTED_ON_THE_RECORDED_ANALYTIC_SHEET",
            "the_projection_turn_alone_establishes_a_caustic_or_new_saddle": "NOT_INFERRED_WITHOUT_A_JACOBI_TEST",
            "the_recorded_field_norm_stop_is_the_exact_thimble_endpoint": "OPEN_NOT_PROVED",
            "the_plateau_asymptotic_control_has_projected_length_4pi_over_3": "SUPPORTED_EXACTLY_FOR_THE_PLATEAU_CONTROL",
            "the_full_Starobinsky_arm_reaches_4pi_over_3": "OPEN_ASYMPTOTIC_EXISTENCE_NOT_DERIVED",
            "the_real_Dirichlet_fold_is_a_lapse_saddle": "CONTRADICTED_BY_NONZERO_W_T",
            "the_real_fold_requires_a_two_sheet_Airy_uniformization": "SUPPORTED_BY_THREE_HALVES_AND_SQUARE_ROOT_SCALING",
            "the_positive_real_Euclidean_T_sheet_is_a_convergent_relative_cycle": "NOT_SUPPORTED_ON_THE_RECORDED_BRANCH",
            "the_Lorentzian_contour_intersection_number_has_been_computed": "OPEN_ENDPOINT_AND_MEASURE_REQUIRED",
            "a_positive_quantum_seam_state_or_initial_value_has_been_selected": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "one reflection-symmetric analytic complex-BVP sheet",
                "a long constant-Im-W arm through a projection turn and bounded return segment",
                "the conjugate lower-arm control",
                "the real simple-fold nonstationarity and Airy scaling overlap",
                "the exact frozen-plateau projected-length control",
            ],
            "not_computed": [
                "all complex or nonsymmetric BVP sheets",
                "a proof of the recorded arm's asymptotic endpoint",
                "the original Lorentzian contour's lateral relative homology",
                "the Faddeev-Popov measure or gauge-fixed bulk determinant",
                "a Stokes matrix, integer intersection coefficient, WDW state, or density",
                "fermion, gravitino, ghost, Pin, or local-SUGRA completion",
            ],
        },
        "next_calculation": (
            "combine the Phase-27 zero-lapse endpoint with a BFV/FP measure and "
            "a uniform determinant before counting lateral intersections"
        ),
    }
    print("PHASE26_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
