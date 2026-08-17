#!/usr/bin/env python3
"""Phase 35 -- reduced endpoint-Jacobi determinant-line transport.

This executable continues the complex endpoint Jacobi determinant
``det B_v`` along the upper/lower dual-aligned reduced stationary-family
branches constructed in Phase 34.  Phase 34 did not orient the incoming
Picard--Lefschetz cycle into either outgoing branch, and this determinant
transport does not supply that missing connection.
It fixes a coordinate/basis convention, unwraps the determinant phase without
crossing zero on a dense sampled table, and lifts that path to either of the
two square-root sheets.

The output is a relative, finite-dimensional endpoint result.  It is not an
absolute determinant orientation, a regularized field-theory determinant, a
BFV superdeterminant, or a global Picard--Lefschetz intersection number.  The
script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp

try:  # package import
    from . import phase25_connected_lapse_scan as p25
    from . import phase34_directed_fold_dual_continuation as p34
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25
    import phase34_directed_fold_dual_continuation as p34


MIN_TAU = 2.0e-6
MAX_CONTINUATION_STEP = 0.04
DENSE_RECORD_STEP = 0.08
ROBUST_MAX_REAL_T = p34.ROBUST_MAX_REAL_T
NEAR_FOLD_TAUS = (
    2.0e-6,
    5.0e-6,
    1.0e-5,
    2.0e-5,
    5.0e-5,
    1.0e-4,
    2.0e-4,
    5.0e-4,
    1.0e-3,
    2.0e-3,
    5.0e-3,
    1.0e-2,
    2.0e-2,
    5.0e-2,
    1.0e-1,
)
ANCHOR_TAUS = (0.2, 0.5, 1.0, 1.7, 2.211374431918758)
FINITE_DIFFERENCE_TAUS = (1.0e-3, 1.0e-2, 1.0e-1, 0.5, 1.7)


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


def pair(value: complex) -> list[float]:
    return [float(value.real), float(value.imag)]


def seed_estimator(
    seed: dict[str, object], recorded_key: str, legacy_key: str
) -> float:
    """Read the hardened P34 name while remaining reproducible on its commit."""

    if recorded_key in seed:
        return float(seed[recorded_key])
    return float(seed[legacy_key])


def exact_controls(audit: Audit) -> dict[str, str]:
    x, y = sp.symbols("x y", real=True)
    determinant = x + sp.I * y
    lower_determinant = sp.conjugate(determinant)
    audit.exact(
        "P35.conjugation.real_ODE_determinant",
        lower_determinant == x - sp.I * y
        and sp.expand(determinant * lower_determinant) == x**2 + y**2,
        "real analytically continued equations pair det Bv with its conjugate and give a positive pair product away from zero",
    )

    radius_0, radius_1 = sp.symbols("r_0 r_1", positive=True, real=True)
    theta_0, increment = sp.symbols("theta_0 Delta", real=True)
    z_0 = radius_0 * sp.exp(sp.I * theta_0)
    z_1 = radius_1 * sp.exp(sp.I * (theta_0 + increment))
    normalized_ratio = (z_1 / z_0) / (radius_1 / radius_0)
    audit.exact(
        "P35.phase.principal_increment_recursion",
        sp.simplify(normalized_ratio - sp.exp(sp.I * increment)) == 0,
        "theta_(j+1)=theta_j+Arg(d_(j+1)/d_j) lifts the sampled determinant phase when each increment is chosen in (-pi,pi]",
    )

    lift_0 = sp.sqrt(radius_0) * sp.exp(sp.I * theta_0 / 2)
    lift_1 = sp.sqrt(radius_1) * sp.exp(
        sp.I * (theta_0 + increment) / 2
    )
    inverse_lift_ratio = (1 / lift_1) / (1 / lift_0)
    audit.exact(
        "P35.sqrt.sampled_half_phase_lift_squares",
        sp.simplify(lift_0**2 - z_0) == 0
        and sp.simplify(lift_1**2 - z_1) == 0
        and sp.simplify((lift_1 / lift_0) ** 2 - z_1 / z_0) == 0
        and sp.simplify(inverse_lift_ratio**2 - z_0 / z_1) == 0,
        "the sampled half-phase lift squares to det Bv, while the corresponding inverse-square-root transport has the opposite half phase",
    )

    audit.exact(
        "P35.sqrt.absolute_sign_ambiguity",
        sp.simplify((-lift_0) ** 2 - lift_0**2) == 0
        and sp.simplify(
            sp.sqrt(radius_0)
            * sp.exp(sp.I * (theta_0 + 2 * sp.pi) / 2)
            + lift_0
        )
        == 0,
        "changing the initial lift sign, equivalently shifting the phase by 2pi, leaves the determinant unchanged",
    )

    tau, coefficient = sp.symbols("tau C_det", positive=True, real=True)
    upper_fold = -sp.I * coefficient * sp.sqrt(tau)
    lower_fold = sp.conjugate(upper_fold)
    audit.exact(
        "P35.fold.oriented_minus_i_square_root",
        sp.simplify(upper_fold / (-sp.I * sp.sqrt(tau)) - coefficient)
        == 0
        and sp.simplify(lower_fold - sp.I * coefficient * sp.sqrt(tau))
        == 0,
        "in the declared row/column and soft-vector orientation the upper determinant is -i C_det sqrt(tau), while the lower is its conjugate",
    )

    audit.exact(
        "P35.pair.relative_phase_cancellation",
        sp.simplify(upper_fold * lower_fold - coefficient**2 * tau) == 0,
        "the conjugate reduced bosonic endpoint pair cancels its relative phase, without asserting a full BFV/SUGRA superdeterminant cancellation",
    )

    return {
        "endpoint_block": "B_v=M_[(a,phi),(a_dot,phi_dot)]",
        "basis_order": "rows=(a,phi), columns=(a_dot,phi_dot)",
        "soft_orientation": "the P34 unit right-null vector has positive a_c component",
        "upper_fold_convention": "det B_v ~ -i C_det sqrt(tau), C_det>0",
        "unwrapped_phase": (
            "theta_0=Arg d_0; theta_(j+1)=theta_j+Arg(d_(j+1)/d_j), "
            "with principal increments in (-pi,pi]"
        ),
        "square_root_lift": "g_j=sqrt(|d_j|) exp(i theta_j/2); g and -g are the two lifts",
    }


def dense_targets(endpoint_tau: float) -> tuple[float, ...]:
    linear = np.arange(0.1, endpoint_tau, DENSE_RECORD_STEP)
    values = NEAR_FOLD_TAUS + ANCHOR_TAUS + (float(endpoint_tau),) + tuple(
        float(value) for value in linear
    )
    # Decimal anchor values such as 0.5 and the corresponding arange value
    # can differ by one binary ulp.  They are the same continuation target,
    # so deduplicate them in the root solver's 1e-12 key convention.
    unique = {round(value, 12): float(value) for value in values}
    return tuple(
        unique[key]
        for key in sorted(unique)
        if unique[key] <= endpoint_tau + 1e-13
    )


def determinant_record(
    tau: float,
    fold_time: float,
    boundary: np.ndarray,
    unknown: np.ndarray,
    root_residual: float,
) -> tuple[dict[str, object], np.ndarray, np.ndarray]:
    proper_length = complex(fold_time + tau, unknown[0])
    center = p34.center_from_unknown(unknown)
    half_final = p34.symmetric_half_flow(proper_length, center)
    velocity = -half_final[[1, 3]]
    full_final, monodromy = p34.full_flow_and_variation(
        proper_length, boundary, velocity
    )
    velocity_block = monodromy[np.ix_([0, 2], [1, 3])]
    determinant = complex(np.linalg.det(velocity_block))
    singular_values = np.linalg.svd(velocity_block, compute_uv=False)
    record = {
        "tau": float(tau),
        "T": pair(proper_length),
        "center": [pair(center[0]), pair(center[1])],
        "det_Bv": pair(determinant),
        "abs_det_Bv": float(abs(determinant)),
        "principal_arg_det_Bv": float(np.angle(determinant)),
        "sigma_min_Bv": float(singular_values[-1]),
        "root_residual": float(root_residual),
        "endpoint_residual": float(
            np.linalg.norm(full_final[[0, 2]] - boundary[2:])
        ),
    }
    return record, velocity, full_final


def dense_upper_branch(
    boundary: np.ndarray,
    fold: dict[str, object],
    seed: dict[str, object],
    right_null: np.ndarray,
) -> tuple[list[dict[str, object]], dict[float, np.ndarray]]:
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    endpoint_tau = ROBUST_MAX_REAL_T - fold_time
    targets = dense_targets(endpoint_tau)

    first_tau = targets[0]
    center_seed = (
        fold_center
        - 1.0j
        * seed_estimator(
            seed, "recorded_soft_radius_ratio", "soft_radius_coefficient"
        )
        * np.sqrt(first_tau)
        * right_null
    )
    unknown = np.array(
        [
            seed_estimator(seed, "recorded_kappa_estimator", "kappa")
            * first_tau**1.5,
            center_seed[0].real,
            center_seed[0].imag,
            center_seed[1].real,
            center_seed[1].imag,
        ]
    )

    records: list[dict[str, object]] = []
    unknowns: dict[float, np.ndarray] = {}
    current_tau = first_tau
    unknown, residual = p34.solve_symmetric_constant_phase(
        fold_time + current_tau, boundary, unknown
    )
    record, _velocity, _final = determinant_record(
        current_tau, fold_time, boundary, unknown, residual
    )
    records.append(record)
    unknowns[round(current_tau, 12)] = unknown.copy()

    for target in targets[1:]:
        while target - current_tau > 1e-13:
            next_tau = min(target, current_tau + MAX_CONTINUATION_STEP)
            unknown, residual = p34.solve_symmetric_constant_phase(
                fold_time + next_tau, boundary, unknown
            )
            current_tau = next_tau
        record, _velocity, _final = determinant_record(
            target, fold_time, boundary, unknown, residual
        )
        records.append(record)
        unknowns[round(target, 12)] = unknown.copy()
    return records, unknowns


def unwrap_determinants(
    determinants: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    if determinants.ndim != 1 or len(determinants) == 0:
        raise ValueError("determinants must be a nonempty vector")
    if np.any(np.abs(determinants) == 0.0):
        raise ValueError("a zero determinant has no sampled phase lift")
    phases = np.empty(len(determinants), dtype=float)
    increments = np.empty(max(0, len(determinants) - 1), dtype=float)
    phases[0] = float(np.angle(determinants[0]))
    for index in range(1, len(determinants)):
        increment = float(np.angle(determinants[index] / determinants[index - 1]))
        increments[index - 1] = increment
        phases[index] = phases[index - 1] + increment
    return phases, increments


def lower_conjugacy_checks(
    records: list[dict[str, object]],
    unknowns: dict[float, np.ndarray],
    boundary: np.ndarray,
    fold_time: float,
) -> list[dict[str, object]]:
    selected = (MIN_TAU, 1.0e-3, 1.0e-2, 1.0e-1, 1.0, records[-1]["tau"])
    by_tau = {round(float(record["tau"]), 12): record for record in records}
    checks: list[dict[str, object]] = []
    for tau in selected:
        key = round(float(tau), 12)
        record = by_tau[key]
        unknown = unknowns[key]
        proper_length = complex(*record["T"])
        center = p34.center_from_unknown(unknown)
        half_final = p34.symmetric_half_flow(proper_length, center)
        velocity = -half_final[[1, 3]]
        lower_final, lower_monodromy = p34.full_flow_and_variation(
            np.conjugate(proper_length), boundary, np.conjugate(velocity)
        )
        lower_block = lower_monodromy[np.ix_([0, 2], [1, 3])]
        lower_determinant = complex(np.linalg.det(lower_block))
        upper_determinant = complex(*record["det_Bv"])
        checks.append(
            {
                "tau": float(tau),
                "det_upper": pair(upper_determinant),
                "det_lower": pair(lower_determinant),
                "relative_conjugacy_residual": float(
                    abs(lower_determinant - np.conjugate(upper_determinant))
                    / max(1.0, abs(upper_determinant))
                ),
                "lower_endpoint_residual": float(
                    np.linalg.norm(lower_final[[0, 2]] - boundary[2:])
                ),
            }
        )
    return checks


def local_finite_difference_checks(
    records: list[dict[str, object]],
    unknowns: dict[float, np.ndarray],
    boundary: np.ndarray,
    fold_time: float,
) -> list[dict[str, float]]:
    by_tau = {round(float(record["tau"]), 12): record for record in records}
    checks: list[dict[str, float]] = []
    for tau in FINITE_DIFFERENCE_TAUS:
        key = round(tau, 12)
        record = by_tau[key]
        center_unknown = unknowns[key]
        center_determinant = complex(*record["det_Bv"])
        step = min(1.0e-3, max(2.0e-6, 1.0e-2 * tau))
        local: list[tuple[float, complex, float]] = []
        for shifted_tau in (tau - step, tau + step):
            solved, residual = p34.solve_symmetric_constant_phase(
                fold_time + shifted_tau, boundary, center_unknown
            )
            shifted_record, _velocity, _final = determinant_record(
                shifted_tau, fold_time, boundary, solved, residual
            )
            local.append(
                (shifted_tau, complex(*shifted_record["det_Bv"]), residual)
            )
        minus_det = local[0][1]
        plus_det = local[1][1]
        minus_increment = float(np.angle(minus_det / center_determinant))
        plus_increment = float(np.angle(plus_det / center_determinant))
        checks.append(
            {
                "tau": float(tau),
                "step": float(step),
                "minus_phase_increment": minus_increment,
                "plus_phase_increment": plus_increment,
                "centered_phase_derivative": float(
                    np.angle(plus_det / minus_det) / (2.0 * step)
                ),
                "phase_midpoint_defect": float(
                    abs(minus_increment + plus_increment)
                ),
                "relative_det_jump_max": float(
                    max(
                        abs(minus_det - center_determinant),
                        abs(plus_det - center_determinant),
                    )
                    / abs(center_determinant)
                ),
                "nearby_root_residual_max": float(
                    max(local[0][2], local[1][2])
                ),
            }
        )
    return checks


def numerical_controls(audit: Audit) -> dict[str, object]:
    boundary, _velocity, _action = p25.benchmark()
    fold = p25.locate_symmetric_fold(boundary)
    fold_time = float(fold["proper_length"])
    fold_center = np.asarray(fold["center"], dtype=float)
    right_null = p34.deterministic_right_null(
        np.asarray(fold["right_null_vector"], dtype=float)
    )
    seed = p34.p33_seed_data(boundary, fold, right_null)
    records, unknowns = dense_upper_branch(boundary, fold, seed, right_null)

    determinants = np.array(
        [complex(*record["det_Bv"]) for record in records],
        dtype=np.complex128,
    )
    phases, increments = unwrap_determinants(determinants)
    for record, phase in zip(records, phases, strict=True):
        record["unwrapped_arg_det_Bv"] = float(phase)
        record["sqrt_lift_phase"] = float(phase / 2.0)

    audit.numerical(
        "P35.detline.no_sampled_zero",
        len(records) >= 50
        and min(abs(determinants)) > 10.0
        and min(float(record["sigma_min_Bv"]) for record in records) > 5e-3
        and max(float(record["root_residual"]) for record in records) < 5e-8
        and max(float(record["endpoint_residual"]) for record in records)
        < 8e-8,
        "the dense upper-branch table contains no sampled endpoint-Jacobi zero and every BVP remains solved",
    )

    normalized_sections = determinants / np.abs(determinants)
    lifted_sections = np.sqrt(np.abs(determinants)) * np.exp(0.5j * phases)
    inverse_sqrt_sections = 1.0 / lifted_sections
    audit.numerical(
        "P35.phase.sampled_unwrap_and_square_root",
        max(abs(np.exp(1.0j * phases) - normalized_sections)) < 2e-14
        and max(abs(lifted_sections**2 - determinants) / np.abs(determinants))
        < 3e-14
        and max(
            abs(
                inverse_sqrt_sections / np.abs(inverse_sqrt_sections)
                - np.exp(-0.5j * phases)
            )
        )
        < 2e-14,
        "the recursive phase lifts det Bv, and the associated inverse-square-root factor carries the opposite half phase",
    )

    audit.numerical(
        "P35.phase.recorded_increment_consistency",
        np.all(increments > 0.0)
        and max(abs(increments)) < 0.16
        and float(phases[-1] - phases[0]) > np.pi,
        "the recorded upper determinant phases advance with positive adjacent increments, none near a principal branch-cut jump",
    )

    near_indices = [
        index
        for index, record in enumerate(records)
        if float(record["tau"]) <= 2.0e-4
    ]
    near_taus = np.array([float(records[index]["tau"]) for index in near_indices])
    near_determinants = determinants[near_indices]
    near_phase_errors = np.array(
        [abs(float(phases[index]) + np.pi / 2.0) for index in near_indices]
    )
    near_coefficients = near_determinants / (-1.0j * np.sqrt(near_taus))
    phase_exponent = float(
        np.polyfit(np.log(near_taus), np.log(near_phase_errors), 1)[0]
    )
    audit.numerical(
        "P35.fold.finite_resolution_minus_i_sqrt",
        near_phase_errors[0] < 1.6e-3
        and np.all(np.diff(near_phase_errors) > 0.0)
        and 0.47 < phase_exponent < 0.53
        and near_coefficients[0].real > 1.0e4
        and abs(near_coefficients[0].imag / near_coefficients[0].real)
        < 1.6e-3
        and max(abs(np.diff(near_coefficients.real))) < 1.0,
        "the recorded near-fold samples are finite-resolution consistent with det Bv=-i C_det sqrt(tau) and C_det positive",
    )

    lower_checks = lower_conjugacy_checks(
        records, unknowns, boundary, fold_time
    )
    independently_integrated_upper = np.array(
        [complex(*check["det_upper"]) for check in lower_checks]
    )
    independently_integrated_lower = np.array(
        [complex(*check["det_lower"]) for check in lower_checks]
    )
    upper_spot_phases, _upper_spot_increments = unwrap_determinants(
        independently_integrated_upper
    )
    lower_spot_phases, _lower_spot_increments = unwrap_determinants(
        independently_integrated_lower
    )
    # The full lower table follows analytically from the real-ODE conjugacy;
    # only the selected determinants above are independently reintegrated.
    lower_determinants = np.conjugate(determinants)
    lower_phases, lower_increments = unwrap_determinants(lower_determinants)
    audit.numerical(
        "P35.conjugation.lower_detline",
        max(
            float(check["relative_conjugacy_residual"])
            for check in lower_checks
        )
        < 2e-12
        and max(float(check["lower_endpoint_residual"]) for check in lower_checks)
        < 8e-8
        and max(abs(lower_spot_phases + upper_spot_phases)) < 2e-12
        and max(abs(lower_phases + phases)) < 2e-14
        and max(abs(lower_increments + increments)) < 2e-14,
        "six separate conjugate-input integrations spot-check the analytic conjugate lift constructed across the full sampled table",
    )

    finite_difference_checks = local_finite_difference_checks(
        records, unknowns, boundary, fold_time
    )
    audit.numerical(
        "P35.continuation.independent_finite_differences",
        all(
            check["minus_phase_increment"] < 0.0
            < check["plus_phase_increment"]
            and check["centered_phase_derivative"] > 0.0
            for check in finite_difference_checks
        )
        and max(
            check["phase_midpoint_defect"] for check in finite_difference_checks
        )
        < 3e-4
        and max(
            check["relative_det_jump_max"] for check in finite_difference_checks
        )
        < 0.02
        and max(
            check["nearby_root_residual_max"]
            for check in finite_difference_checks
        )
        < 5e-8,
        "independently re-solved two-sided BVPs stay on the same locally smooth determinant branch",
    )

    by_tau = {round(float(record["tau"]), 12): record for record in records}
    phase34_start = complex(*by_tau[round(2.0e-4, 12)]["det_Bv"])
    phase34_end = determinants[-1]
    audit.numerical(
        "P35.regression.P34_anchor_determinants",
        abs(phase34_start - complex(2.10846218665, -144.7597664306))
        / abs(phase34_start)
        < 1e-8
        and abs(phase34_end - complex(-191673.337128, 465022.387273))
        / abs(phase34_end)
        < 1e-8,
        "the dense transport reproduces the Phase-34 near-fold and ReT=13 endpoint determinant anchors",
    )

    determinant_phase_rotation = float(phases[-1] - phases[0])
    formal_minus_pi_over_2_reference_rotation = float(
        phases[-1] + np.pi / 2.0
    )
    determinant_unit_transport = complex(
        np.exp(1.0j * determinant_phase_rotation)
    )
    sqrt_section_unit_transport = complex(
        np.exp(0.5j * determinant_phase_rotation)
    )
    inverse_sqrt_unit_transport = complex(
        np.exp(-0.5j * determinant_phase_rotation)
    )
    independent_lower_rotation = float(
        lower_spot_phases[-1] - lower_spot_phases[0]
    )
    pair_phase_residual = float(
        abs(
            np.exp(1.0j * determinant_phase_rotation)
            * np.exp(1.0j * independent_lower_rotation)
            - 1.0
        )
    )
    audit.numerical(
        "P35.pair.reduced_relative_phase_cancels",
        pair_phase_residual < 2e-12,
        "the sampled upper transport and separate conjugate-input lower spot integrations have cancelling relative endpoint phases",
    )

    selected_taus = set(
        NEAR_FOLD_TAUS
        + ANCHOR_TAUS
        + (float(records[-1]["tau"]),)
    )
    selected_records = [
        record
        for record in records
        if any(abs(float(record["tau"]) - tau) < 1e-12 for tau in selected_taus)
    ]
    return {
        "boundary": boundary.tolist(),
        "fold": {
            "T_c": fold_time,
            "center": fold_center.tolist(),
            "right_null_oriented": right_null.tolist(),
        },
        "sample_count": len(records),
        "tau_range": [float(records[0]["tau"]), float(records[-1]["tau"])],
        "min_abs_det_Bv": float(min(abs(determinants))),
        "min_sigma_Bv": float(
            min(float(record["sigma_min_Bv"]) for record in records)
        ),
        "max_principal_increment": float(max(abs(increments))),
        "near_fold": {
            "phase_errors_from_minus_pi_over_2": near_phase_errors.tolist(),
            "phase_error_power": phase_exponent,
            "det_over_minus_i_sqrt_tau": [
                pair(value) for value in near_coefficients
            ],
            "C_det_smallest_tau": float(near_coefficients[0].real),
        },
        "relative_transport": {
            "upper_start_phase": float(phases[0]),
            "upper_endpoint_phase": float(phases[-1]),
            "upper_rotation_from_tau_min": determinant_phase_rotation,
            "upper_rotation_from_formal_minus_pi_over_2_reference": (
                formal_minus_pi_over_2_reference_rotation
            ),
            "independent_lower_spot_rotation": independent_lower_rotation,
            "determinant_unit_transport": pair(determinant_unit_transport),
            "one_sqrt_section_unit_transport": pair(
                sqrt_section_unit_transport
            ),
            "other_sqrt_section_unit_transport": pair(
                -sqrt_section_unit_transport
            ),
            "one_inverse_sqrt_prefactor_unit_transport": pair(
                inverse_sqrt_unit_transport
            ),
            "other_inverse_sqrt_prefactor_unit_transport": pair(
                -inverse_sqrt_unit_transport
            ),
            "absolute_lift_sign": "UNFIXED",
            "conjugate_pair_phase_residual": pair_phase_residual,
        },
        "lower_conjugacy_checks": lower_checks,
        "finite_difference_checks": finite_difference_checks,
        "selected_records": selected_records,
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P35",
        "calculation": (
            "relative endpoint-Jacobi determinant-line transport on the "
            "bounded P34 dual-aligned reduced stationary-family branch pair"
        ),
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_tracked_reduced_endpoint_determinant_line_is_transportable": (
                "SUPPORTED_ON_THE_SAMPLED_P34_BRANCH_PAIR_THROUGH_ReT_13"
            ),
            "the_incoming_PL_cycle_is_oriented_into_one_outgoing_branch": (
                "OPEN_NOT_FIXED_BY_RELATIVE_ENDPOINT_DETERMINANT_TRANSPORT"
            ),
            "the_recorded_upper_near_fold_phase_is_consistent_with_minus_pi_over_2": (
                "SUPPORTED_AT_FINITE_RESOLUTION_IN_THE_DECLARED_ENDPOINT_BASIS"
            ),
            "the_conjugate_reduced_bosonic_endpoint_phases_cancel": (
                "SUPPORTED_RELATIVELY_NOT_A_FULL_SUPERDETERMINANT_RESULT"
            ),
            "the_absolute_determinant_or_Maslov_orientation_is_fixed": (
                "OPEN_REQUIRES_AN_ORIENTED_ORIGINAL_CYCLE_AND_REGULATOR"
            ),
            "there_are_no_unsampled_or_other_sheet_Jacobi_zeros": (
                "OPEN_NOT_PROVED"
            ),
            "the_full_BFV_SUGRA_superdeterminant_is_transported": (
                "OPEN_NOT_COMPUTED"
            ),
            "the_global_intersection_coefficient_n_sigma_is_fixed": (
                "OPEN_REQUIRES_ALL_JOINT_DUALS_GOOD_ENDS_AND_ORIENTATIONS"
            ),
        },
        "scope_guard": {
            "computed": [
                "the complex 2x2 endpoint Jacobi determinant in the declared (a,phi)/(a_dot,phi_dot) order",
                "a dense sampled table with no recorded zero and its recursively unwrapped phase",
                "the two sampled square-root lifts relative to the first regulated point",
                "the opposite half phase of the corresponding inverse-square-root endpoint factor",
                "finite-resolution consistency with the -i sqrt(tau) near-fold law in the frozen orientation",
                "six separate conjugate-input lower spot checks and local two-sided BVP continuity checks",
            ],
            "not_computed": [
                "an absolute determinant/Maslov orientation or original-cycle normalization",
                "an oriented incoming-to-outgoing Picard-Lefschetz connection at the fold",
                "zeros between samples, other sheets, inhomogeneous modes, or good ends",
                "a regularized full field-lapse BFV/SUGRA superdeterminant",
                "complete relative cycles or a global Picard-Lefschetz coefficient",
                "a WDW density matrix or physical quantum state",
            ],
        },
        "next_calculation": (
            "continue the oriented original and every joint dual cycle with the "
            "regulated BFV superdeterminant line, including all good ends"
        ),
    }
    print("PHASE35_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
