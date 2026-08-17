#!/usr/bin/env python3
"""Phase 33 -- simple-fold Airy uniformization and intersection scope gate.

The connected homogeneous Starobinsky boundary-value family of Phase 25 is
continued to its recorded simple Dirichlet fold.  The two real fixed-length
branches are resolved ever closer to the fold, their action gap is converted
to the invariant Airy scale, and the singular type-1 Van Vleck behavior is
separated from the regular local uniform solution space.

The calculation establishes a local fold normal form.  It does not select an
Ai/Bi combination, a global relative cycle, a Picard--Lefschetz coefficient,
or a physical WDW/seam state.  The script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25


DELTAS = (0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002)


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


def exact_controls(audit: Audit) -> dict[str, object]:
    u = sp.symbols("u", real=True)
    zeta, action_gap = sp.symbols(
        "zeta DeltaW", positive=True, real=True
    )
    normal_form = u**3 / 3 - zeta * u
    stationary_plus = sp.sqrt(zeta)
    stationary_minus = -sp.sqrt(zeta)
    derivative = sp.diff(normal_form, u)
    audit.exact(
        "P33.normal_form.stationary_points",
        sp.simplify(derivative.subs(u, stationary_plus)) == 0
        and sp.simplify(derivative.subs(u, stationary_minus)) == 0,
        "the canonical fold phase has stationary points u=plus/minus sqrt(zeta)",
    )

    canonical_gap = sp.simplify(
        normal_form.subs(u, stationary_minus)
        - normal_form.subs(u, stationary_plus)
    )
    audit.exact(
        "P33.normal_form.action_gap",
        sp.simplify(canonical_gap - sp.Rational(4, 3) * zeta ** sp.Rational(3, 2))
        == 0,
        "the two canonical fold actions differ by 4 zeta^(3/2)/3",
    )

    zeta_from_gap = (sp.Rational(3, 4) * action_gap) ** sp.Rational(2, 3)
    audit.exact(
        "P33.normal_form.invariant_Airy_scale",
        sp.simplify(
            sp.Rational(4, 3) * zeta_from_gap ** sp.Rational(3, 2)
            - action_gap
        )
        == 0,
        "the magnitude zeta=(3 DeltaW/4)^(2/3) is fixed by the branch-action gap",
    )

    hessian_plus = sp.diff(normal_form, u, 2).subs(u, stationary_plus)
    hessian_minus = sp.diff(normal_form, u, 2).subs(u, stationary_minus)
    gaussian_magnitude = sp.simplify(1 / sp.sqrt(abs(hessian_plus)))
    audit.exact(
        "P33.normal_form.branch_prefactor_divergence",
        hessian_plus == 2 * sp.sqrt(zeta)
        and hessian_minus == -2 * sp.sqrt(zeta)
        and gaussian_magnitude == sp.sqrt(2) / (2 * zeta ** sp.Rational(1, 4)),
        "separate saddle prefactors diverge as zeta^(-1/4) at the fold",
    )

    airy_ai = sp.airyai(zeta)
    airy_bi = sp.airybi(zeta)
    airy_ai_zero = sp.expand_func(sp.airyai(0))
    airy_bi_zero = sp.expand_func(sp.airybi(0))
    audit.exact(
        "P33.Airy.two_regular_solutions",
        sp.simplify(sp.diff(airy_ai, zeta, 2) - zeta * airy_ai) == 0
        and sp.simplify(sp.diff(airy_bi, zeta, 2) - zeta * airy_bi) == 0
        and airy_ai_zero.is_finite is True
        and airy_bi_zero.is_finite is True,
        "Ai and Bi solve the local Airy equation and have finite exact values at the fold",
    )

    wronskian_at_zero = sp.expand_func(
        sp.airyai(0) * sp.airybiprime(0)
        - sp.airyaiprime(0) * sp.airybi(0)
    )
    audit.exact(
        "P33.Airy.local_regularity_does_not_select_cycle",
        sp.simplify(wronskian_at_zero - 1 / sp.pi) == 0,
        "the nonzero Ai/Bi Wronskian leaves a two-dimensional regular local ODE solution space; admissible lifted gravitational cycles are not inferred",
    )

    amplitude_plus, amplitude_minus = sp.symbols(
        "G_plus G_minus", real=True
    )
    amplitude_even = (amplitude_plus + amplitude_minus) / 2
    amplitude_odd = (
        amplitude_plus - amplitude_minus
    ) / (2 * sp.sqrt(zeta))
    audit.exact(
        "P33.CFU.amplitude_data_are_distinct_from_cycle_choice",
        sp.simplify(
            amplitude_even + amplitude_odd * sp.sqrt(zeta) - amplitude_plus
        )
        == 0
        and sp.simplify(
            amplitude_even - amplitude_odd * sp.sqrt(zeta) - amplitude_minus
        )
        == 0,
        "even and odd analytic-amplitude data reconstruct the two saddle amplitudes independently of the Airy contour choice",
    )

    benchmark_fold = sp.Rational(9788625568, 10**9)
    patch_radius = sp.Integer(1)
    largest_phase32_bypass = sp.Rational(1, 10)
    audit.exact(
        "P33.intersection.local_fold_patch_disjoint_from_imaginary_lapse_axis",
        benchmark_fold - patch_radius - largest_phase32_bypass > 0,
        "a radius-one T-plane patch around the recorded fold is disjoint from the imaginary-axis full-lapse contour and every Phase-32 bypass",
    )

    return {
        "canonical_fold_phase": "Phi(u,zeta)=u^3/3-zeta u",
        "Airy_action_scale_magnitude": "zeta_action=(3 abs(DeltaW)/4)^(2/3)",
        "dimensionless_Airy_argument": "z=zeta_action/hbar^(2/3) in the declared real e^(-W/hbar) canonical chart; any complex phase requires a separately derived canonical-map/exponent branch",
        "local_contour_solution_basis": "Ai(z), Bi(z), or rotated-Ai equivalents; the relative cycle selects a combination but local ODE regularity does not",
        "generic_CFU_amplitude_structure": "A(zeta) hbar^(1/3) Airy_C(z)+B(zeta) hbar^(2/3) Airy_C_prime(z)+higher terms for a chosen contour C",
        "local_fold_patch_radius": 1.0,
    }


def deterministic_right_null(fold: dict[str, object]) -> np.ndarray:
    vector = np.asarray(fold["right_null_vector"], dtype=float)
    if vector[0] < 0:
        vector = -vector
    return vector / np.linalg.norm(vector)


def solve_two_branches(
    boundary: np.ndarray,
    fold: dict[str, object],
    delta: float,
) -> list[dict[str, object]]:
    fold_center = np.asarray(fold["center"], dtype=float)
    right_null = deterministic_right_null(fold)
    reference_delta = 0.0086255681
    guess_scale = 0.12 * np.sqrt(delta / reference_delta)
    branches: list[dict[str, object]] = []
    for sign in (-1.0, 1.0):
        proper_length = float(fold["proper_length"]) - delta
        guess = fold_center + sign * guess_scale * right_null
        center, endpoint = p25.solve_symmetric_center(
            proper_length, boundary, guess
        )
        solution = p25.solve_fixed_time(
            proper_length, boundary, -endpoint[[1, 3]]
        )
        singular_values = np.linalg.svd(
            solution.velocity_monodromy, compute_uv=False
        )
        determinant = float(np.linalg.det(solution.velocity_monodromy))
        branches.append(
            {
                "center": center,
                "action": float(solution.action),
                "det_Bv": determinant,
                "sigma_min": float(singular_values[-1]),
                "endpoint_residual": float(solution.endpoint_residual),
            }
        )
    branches.sort(key=lambda branch: float(branch["center"][0]))
    return branches


def fold_scan() -> dict[str, object]:
    boundary, _velocity, _action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    right_null = deterministic_right_null(fold)
    records: list[dict[str, object]] = []

    for delta in DELTAS:
        lower, upper = solve_two_branches(boundary, fold, delta)
        action_gap = abs(float(upper["action"]) - float(lower["action"]))
        airy_scale = (0.75 * action_gap) ** (2.0 / 3.0)
        center_difference = np.asarray(upper["center"]) - np.asarray(
            lower["center"]
        )
        soft_projection = float(center_difference @ right_null)
        transverse_difference = center_difference - soft_projection * right_null
        records.append(
            {
                "delta": delta,
                "proper_length": float(fold["proper_length"]) - delta,
                "centers": [
                    np.asarray(lower["center"]).tolist(),
                    np.asarray(upper["center"]).tolist(),
                ],
                "actions": [float(lower["action"]), float(upper["action"])],
                "action_gap": action_gap,
                "action_gap_over_delta_3_2": action_gap / delta**1.5,
                "Airy_action_scale_magnitude": airy_scale,
                "Airy_action_scale_over_delta": airy_scale / delta,
                "det_Bv_over_sqrt_delta": [
                    float(lower["det_Bv"]) / np.sqrt(delta),
                    float(upper["det_Bv"]) / np.sqrt(delta),
                ],
                "sigma_min_over_sqrt_delta": [
                    float(lower["sigma_min"]) / np.sqrt(delta),
                    float(upper["sigma_min"]) / np.sqrt(delta),
                ],
                "scaled_endpoint_Van_Vleck_proxies": [
                    delta**0.25 / np.sqrt(abs(float(lower["det_Bv"]))),
                    delta**0.25 / np.sqrt(abs(float(upper["det_Bv"]))),
                ],
                "soft_center_separation_over_sqrt_delta": soft_projection
                / np.sqrt(delta),
                "transverse_center_separation_over_delta": float(
                    np.linalg.norm(transverse_difference) / delta
                ),
                "endpoint_residual_max": max(
                    float(lower["endpoint_residual"]),
                    float(upper["endpoint_residual"]),
                ),
            }
        )

    fold_center = np.asarray(fold["center"], dtype=float)
    fold_endpoint, _ = p25.midpoint_endpoint(
        fold_center, float(fold["proper_length"])
    )
    fold_solution = p25.solve_fixed_time(
        float(fold["proper_length"]),
        boundary,
        -fold_endpoint[[1, 3]],
    )

    tail = records[-4:]
    tail_deltas = np.asarray([record["delta"] for record in tail])

    def log_slope(values: np.ndarray) -> float:
        return float(np.polyfit(np.log(tail_deltas), np.log(values), 1)[0])

    gap_values = np.asarray([record["action_gap"] for record in tail])
    airy_values = np.asarray(
        [record["Airy_action_scale_magnitude"] for record in tail]
    )
    sigma_values = [
        np.asarray(
            [
                record["sigma_min_over_sqrt_delta"][branch]
                * np.sqrt(record["delta"])
                for record in tail
            ]
        )
        for branch in (0, 1)
    ]
    van_vleck_values = [
        np.asarray(
            [
                record["scaled_endpoint_Van_Vleck_proxies"][branch]
                / record["delta"] ** 0.25
                for record in tail
            ]
        )
        for branch in (0, 1)
    ]
    scaling_fits = {
        "tail_point_count": len(tail),
        "action_gap_log_slope": log_slope(gap_values),
        "Airy_scale_log_slope": log_slope(airy_values),
        "soft_singular_value_log_slopes": [
            log_slope(values) for values in sigma_values
        ],
        "endpoint_Van_Vleck_proxy_log_slopes": [
            log_slope(values) for values in van_vleck_values
        ],
    }
    return {
        "boundary": boundary.tolist(),
        "fold": fold,
        "fold_action": float(fold_solution.action),
        "fold_W_T": float(-fold_solution.energy),
        "records": records,
        "scaling_fits": scaling_fits,
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    scan = fold_scan()
    fold = scan["fold"]
    records = scan["records"]
    scaling_fits = scan["scaling_fits"]

    audit.numerical(
        "P33.fold.frozen_simple_fold_control",
        abs(float(fold["proper_length"]) - 9.7886255681) < 3e-9
        and max(abs(value) for value in fold["residual"]) < 2e-8
        and float(fold["half_length_transversality"]) > 0.5
        and float(fold["quadratic_transversality"]) > 0.36,
        "the previously recorded Dirichlet caustic is a transverse simple fold",
    )
    audit.numerical(
        "P33.fold.two_branch_action_gap_three_halves",
        all(record["action_gap"] > 0 for record in records)
        and np.all(
            np.diff(
                [record["action_gap_over_delta_3_2"] for record in records]
            )
            > 0
        )
        and abs(scaling_fits["action_gap_log_slope"] - 1.5) < 5e-5
        and abs(records[-1]["action_gap_over_delta_3_2"] - 93.0272) < 8e-4,
        "the recorded two-branch action gap has a last-four-point log slope consistent with delta^(3/2)",
    )
    audit.numerical(
        "P33.fold.Airy_scale_linear",
        np.all(
            np.diff(
                [record["Airy_action_scale_over_delta"] for record in records]
            )
            > 0
        )
        and abs(scaling_fits["Airy_scale_log_slope"] - 1.0) < 3e-5
        and abs(records[-1]["Airy_action_scale_over_delta"] - 16.94783) < 8e-5,
        "the recorded invariant Airy action-scale magnitude has a last-four-point log slope consistent with T_c-T",
    )
    audit.numerical(
        "P33.fold.soft_Jacobi_square_root",
        all(
            record["det_Bv_over_sqrt_delta"][0] < 0
            and record["det_Bv_over_sqrt_delta"][1] > 0
            for record in records
        )
        and max(
            abs(value - 0.5)
            for value in scaling_fits["soft_singular_value_log_slopes"]
        )
        < 0.012
        and abs(
            records[-1]["sigma_min_over_sqrt_delta"][0]
            - records[-1]["sigma_min_over_sqrt_delta"][1]
        )
        < 0.07,
        "the recorded soft Jacobi singular values have last-four-point slopes consistent with sqrt(delta), and the two branch determinants have opposite signs",
    )
    audit.numerical(
        "P33.fold.separate_endpoint_prefactor_quarter_power",
        all(
            np.isfinite(value)
            for record in records
            for value in record["scaled_endpoint_Van_Vleck_proxies"]
        )
        and max(
            abs(value + 0.25)
            for value in scaling_fits["endpoint_Van_Vleck_proxy_log_slopes"]
        )
        < 0.012
        and np.all(
            np.diff(
                [
                    abs(
                        record["scaled_endpoint_Van_Vleck_proxies"][1]
                        - record["scaled_endpoint_Van_Vleck_proxies"][0]
                    )
                    for record in records
                ]
            )
            < 0
        )
        and max(
            abs(
                records[-1]["scaled_endpoint_Van_Vleck_proxies"][index]
                - records[-2]["scaled_endpoint_Van_Vleck_proxies"][index]
            )
            for index in (0, 1)
        )
        < 4e-4,
        "the recorded endpoint Jacobi/Van-Vleck proxies have last-four-point slopes consistent with delta^(-1/4), while their finite rescaled branch values approach each other",
    )
    audit.numerical(
        "P33.fold.actual_BVP_residuals",
        max(record["endpoint_residual_max"] for record in records) < 2e-8,
        "both actual fixed-boundary branches solve the endpoint problem at every recorded delta",
    )
    audit.numerical(
        "P33.fold.is_not_a_lapse_saddle",
        abs(float(scan["fold_W_T"]) + 73.72585376) < 2e-6
        and abs(float(scan["fold_W_T"])) > 70,
        "the Dirichlet fold has nonzero W_T and is not an additional lapse saddle",
    )

    return scan


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P33",
        "calculation": "simple-fold Airy uniformization and intersection scope gate",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_recorded_Dirichlet_caustic_has_a_local_Airy_fold_scale": "SUPPORTED_BY_EXACT_NORMAL_FORM_AND_NUMERICAL_SCALING",
            "the_divergent_separate_Van_Vleck_branches_necessarily_imply_a_divergent_exact_kernel": "CONTRADICTED_IN_THE_CANONICAL_FOLD_NORMAL_FORM_NOT_A_CLAIM_ABOUT_THE_UNCOMPUTED_FULL_MEASURE",
            "local_regularity_at_the_fold_uniquely_selects_an_Airy_contour_solution": "CONTRADICTED_BY_THE_NONZERO_Ai_Bi_WRONSKIAN",
            "the_recorded_fold_is_an_additional_lapse_saddle": "CONTRADICTED_BY_NONZERO_W_T",
            "the_radius_one_fold_patch_adds_an_intersection_with_the_imaginary_full_lapse_contour": "CONTRADICTED_IN_THE_LOCAL_T_PLANE_PATCH",
            "Airy_uniformization_fixes_the_complete_global_PL_coefficient": "OPEN_REQUIRES_THE_ORIGINAL_RELATIVE_CYCLE_AND_COMPLETE_DUAL",
            "a_positive_trace_class_WDW_or_quantum_seam_state_is_obtained": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "the canonical simple-fold normal form and invariant Airy action-scale magnitude",
                "two actual real fixed-boundary branches down to T_c-T=0.0002",
                "action-gap, Jacobi-soft-mode, determinant-sign, and branch-prefactor scaling",
                "the local two-dimensional regular Airy ODE solution space; admissible lifted gravitational cycles are not inferred",
                "nonstationarity of the fold in the lapse direction",
                "local T-plane disjointness of a radius-one fold patch and the imaginary lapse contour",
            ],
            "not_computed": [
                "an off-real canonical-map or exponent branch for the Airy argument, and the separately selected Airy contour/Stokes combination",
                "the analytic amplitude coefficients multiplying the chosen Airy function and its derivative, or a uniformized absolute prefactor",
                "the continuation of every full joint dual arm beyond the fold patch",
                "the global determinant line, BFV superorientation, or complete intersection matrix",
                "inhomogeneous SUGRA modes, a WDW density, an initial-value peak, or a SUSY scale",
            ],
        },
        "next_calculation": (
            "choose and lift one complete regulated relative cycle, transport the oriented determinant line into the Airy chart, "
            "fix its Airy contour/Stokes multiplier and analytic amplitude data, then continue every joint dual arm"
        ),
    }
    print("PHASE33_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
