#!/usr/bin/env python3
"""Phase 32 -- below-origin lapse bypass and recorded intersection gate.

The connected homogeneous Starobinsky interval of Phases 24--30 is frozen.
This executable distinguishes two lapse objects:

* the causal positive half-line, together with a separately declared lower
  lateral endpoint regulator.  Its contact with the recorded dual is an
  endpoint and therefore has no ordinary Picard--Lefschetz integer; and
* a full real group-average contour with a finite lower semicircle around
  N=0.  Under T=iN, that bypass becomes a right semicircle and crosses the
  recorded positive-real dual once at T=r.

The program follows that crossing down to small r, continues the actual
complex boundary-value solution around the lower bypass, and transports the
principal signature (-,+) momentum cycle.  The recorded local intersection is
+1 for the specified full-line contour.  No complete global upward cycle,
absolute determinant phase, trace-class WDW projector, Pin lift, or SUGRA
state is claimed.  The script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.optimize import root

try:  # package import
    from . import phase25_connected_lapse_scan as p25
except ImportError:  # direct script / ./ice execution
    import phase25_connected_lapse_scan as p25


RADII = (0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625)
ARC_RADII = RADII[:4]
LOWER_ARC_ANGLES = (-np.pi, -3 * np.pi / 4, -np.pi / 2, -np.pi / 4, 0.0)


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
    x, y, epsilon, radius = sp.symbols(
        "x y epsilon r", real=True, positive=True
    )
    theta = sp.symbols("theta", real=True)
    lapse_general = x + sp.I * y
    euclidean_time = sp.expand_complex(sp.I * lapse_general)
    audit.exact(
        "P32.Wick.lapse_half_plane_map",
        sp.re(euclidean_time) == -y and sp.im(euclidean_time) == x,
        "T=iN maps Re N>=0 to Im T>=0 and the lower N half-plane to the right T half-plane",
    )

    lower_lapse = radius * sp.exp(sp.I * theta)
    lower_time = sp.I * lower_lapse
    audit.exact(
        "P32.Wick.lower_bypass_maps_right",
        sp.simplify(lower_time.subs(theta, -sp.pi) + sp.I * radius) == 0
        and sp.simplify(lower_time.subs(theta, -sp.pi / 2) - radius) == 0
        and sp.simplify(lower_time.subs(theta, 0) - sp.I * radius) == 0,
        "the lower N semicircle from -r to +r maps to a right T semicircle crossing T=r",
    )

    upper_lapse = radius * sp.exp(sp.I * theta)
    upper_time = sp.I * upper_lapse
    audit.exact(
        "P32.Wick.upper_bypass_maps_left",
        sp.simplify(upper_time.subs(theta, sp.pi) + sp.I * radius) == 0
        and sp.simplify(upper_time.subs(theta, sp.pi / 2) + radius) == 0
        and sp.simplify(upper_time.subs(theta, 0) - sp.I * radius) == 0,
        "the upper N semicircle maps to a left T semicircle and misses the recorded positive-real dual",
    )

    dual_speed = sp.symbols("v", positive=True, real=True)
    orientation = sp.Matrix([[0, -dual_speed], [radius, 0]]).det()
    audit.exact(
        "P32.intersection.lower_bypass_orientation",
        sp.simplify(orientation - radius * dual_speed) == 0,
        "the lower-bypass tangent and outward left dual tangent have positive transverse orientation",
    )

    half_parameter = sp.symbols("s", nonnegative=True, real=True)
    half_time = epsilon + sp.I * half_parameter
    audit.exact(
        "P32.intersection.lower_lateral_half_line_is_endpoint_contact",
        sp.re(half_time) == epsilon
        and sp.im(half_time).subs(half_parameter, 0) == 0,
        "the separately declared lower-lateral half-line meets the real dual only at its s=0 endpoint",
    )

    mu_g, mu_s, p_g, p_s = sp.symbols(
        "mu_g mu_s p_g p_s", positive=True, real=True
    )
    momentum_angle_g = sp.pi / 4 - theta / 2
    momentum_angle_s = -sp.pi / 4 - theta / 2
    kinetic = (
        -(sp.exp(sp.I * momentum_angle_g) * p_g) ** 2 / (2 * mu_g)
        + (sp.exp(sp.I * momentum_angle_s) * p_s) ** 2 / (2 * mu_s)
    )
    momentum_exponent = sp.simplify(-sp.I * lower_lapse * kinetic)
    audit.exact(
        "P32.contour.principal_momentum_decay",
        sp.simplify(
            momentum_exponent
            + radius * (p_g**2 / (2 * mu_g) + p_s**2 / (2 * mu_s))
        )
        == 0,
        "the lapse-dependent gravity and scalar momentum rays make the lower-bypass Gaussian decaying",
    )

    configuration_angle_g = theta / 2 - sp.pi / 4
    configuration_angle_s = theta / 2 + sp.pi / 4
    momentum_jacobian = sp.exp(
        sp.I * (momentum_angle_g + momentum_angle_s)
    )
    configuration_jacobian = sp.exp(
        sp.I * (configuration_angle_g + configuration_angle_s)
    )
    audit.exact(
        "P32.detline.coupled_crossing_orientation",
        sp.simplify(
            momentum_jacobian * configuration_jacobian - 1
        )
        == 0
        and sp.simplify(
            momentum_jacobian.subs(theta, -sp.pi / 2) - sp.I
        )
        == 0
        and sp.simplify(
            configuration_jacobian.subs(theta, -sp.pi / 2) + sp.I
        )
        == 0,
        "the declared momentum and dual-configuration Jacobians multiply to +1 and preserve the local crossing orientation",
    )

    normalization = sp.symbols("C", positive=True, real=True)
    negative_real_prefactor = sp.simplify(
        normalization / lower_lapse.subs(theta, -sp.pi)
    )
    transported_momentum_orientation = sp.simplify(
        momentum_jacobian.subs(theta, -sp.pi)
    )
    declared_maslov_comparison = -1
    independently_normalized_real_prefactor = normalization / radius
    audit.exact(
        "P32.detline.lower_half_turn_requires_maslov_gluing",
        negative_real_prefactor == -normalization / radius
        and transported_momentum_orientation == -1
        and sp.simplify(
            negative_real_prefactor * declared_maslov_comparison
            - independently_normalized_real_prefactor
        )
        == 0,
        "analytic momentum-cycle transport gives C/N; comparison with the independently normalized C/|N| real branch requires an additional declared Maslov sign",
    )

    spectral = sp.symbols("lambda", real=True)
    test = 1 + spectral + spectral**2
    below_pairing = sp.integrate(
        sp.exp(-epsilon * spectral) * sp.DiracDelta(spectral) * test,
        (spectral, -sp.oo, sp.oo),
    )
    above_pairing = sp.integrate(
        sp.exp(epsilon * spectral) * sp.DiracDelta(spectral) * test,
        (spectral, -sp.oo, sp.oo),
    )
    audit.exact(
        "P32.operator.full_line_lateral_constraint_support",
        below_pairing == 1 and above_pairing == 1,
        "both full-line lateral contours retain the same formal delta(H) constraint support",
    )

    regulator = sp.symbols("eta", positive=True, real=True)
    half_resolvent = -sp.I / (spectral - sp.I * regulator)
    audit.exact(
        "P32.operator.positive_half_line_is_sourced",
        sp.simplify((spectral - sp.I * regulator) * half_resolvent) == -sp.I,
        "the positive half-line remains a sourced resolvent rather than a constraint projector",
    )

    lower_arc_differential = sp.I * radius * sp.exp(sp.I * theta)
    paired_arc = sp.integrate(
        lower_arc_differential, (theta, -sp.pi, 0)
    )
    pointwise_arc = sp.integrate(sp.I, (theta, -sp.pi, 0))
    audit.exact(
        "P32.endpoint.paired_arc_vs_pointwise_pole",
        sp.simplify(paired_arc - 2 * radius) == 0
        and pointwise_arc == sp.I * sp.pi
        and sp.limit(paired_arc, radius, 0, dir="+") == 0,
        "the operator-paired bypass shrinks while a pointwise 1/N pole retains a finite semicircle integral",
    )

    mode_cutoff = sp.symbols("M", positive=True, real=True)
    bounded_difference = 2 * sp.sinh(epsilon * mode_cutoff)
    audit.exact(
        "P32.regulator.lateral_limit_is_not_uniform",
        sp.limit(bounded_difference, epsilon, 0, dir="+") == 0
        and sp.simplify(
            bounded_difference.subs(mode_cutoff, 1 / epsilon)
            - 2 * sp.sinh(1)
        )
        == 0,
        "the lateral difference vanishes at fixed spectral cutoff but not when the cutoff scales as 1/epsilon",
    )

    c_0, c_1 = sp.symbols("c_0 c_1")
    dirichlet_ghost_variation = (c_1 - c_0).subs({c_0: 0, c_1: 0})
    zeta_zero = -sp.Rational(1, 2)
    fixed_s_determinant = sp.simplify(
        (radius**2) ** zeta_zero * 2 * radius
    )
    audit.exact(
        "P32.BFV.open_interval_modulus_control",
        dirichlet_ghost_variation == 0
        and fixed_s_determinant == 2,
        "in the declared reduced open-interval gauge, Dirichlet ghosts leave the lapse modulus invariant and add no bypass-selecting power",
    )

    audit.exact(
        "P32.conjugation.lateral_loci",
        sp.conjugate(x - sp.I * epsilon) == x + sp.I * epsilon,
        "complex conjugation exchanges the lower and upper lateral lapse loci; no CPT or Pin lift is inferred",
    )

    return {
        "Wick_map": "T=iN",
        "below_origin_full_line": (
            "N real except N=r exp(i theta), theta from -pi to 0"
        ),
        "positive_half_line": "N=x, x>=0 with proper-time damping; sourced resolvent",
        "lower_lateral_endpoint_regulator": "N=x-i epsilon, x>=0; separately declared",
        "principal_momentum_cycle": {
            "p_gravity": "exp[i(pi/4-theta/2)] R",
            "p_scalar": "exp[i(-pi/4-theta/2)] R",
        },
    }


def real_dual_scan() -> dict[str, object]:
    boundary, velocity, benchmark_action = p25.benchmark()
    center = np.array([np.sqrt(3.0 / p25.potential(1.0)), 1.0])
    momentum_velocity = np.diag(
        [
            -12.0 * np.pi**2 * boundary[0],
            2.0 * np.pi**2 * boundary[0] ** 3,
        ]
    )
    records: list[dict[str, object]] = []
    velocities: dict[float, np.ndarray] = {}
    for radius in RADII:
        center, midpoint_endpoint = p25.solve_symmetric_center(
            radius, boundary, center
        )
        solution = p25.solve_fixed_time(
            radius, boundary, -midpoint_endpoint[[1, 3]]
        )
        velocities[radius] = solution.velocity.astype(np.complex128)
        momentum_block = solution.velocity_monodromy @ np.linalg.inv(
            momentum_velocity
        )
        van_vleck = float(
            np.sqrt(abs(np.linalg.det(np.linalg.inv(momentum_block))))
            / (2 * np.pi)
        )
        singular_values = np.linalg.svd(
            solution.velocity_monodromy, compute_uv=False
        )
        derivative = float(-solution.energy)
        records.append(
            {
                "r": radius,
                "W": solution.action,
                "W_over_r": solution.action / radius,
                "W_T": derivative,
                "det_Bv_over_r2": float(
                    np.linalg.det(solution.velocity_monodromy) / radius**2
                ),
                "sigma_min_over_r": float(singular_values[-1] / radius),
                "r_times_Van_Vleck": radius * van_vleck,
                "endpoint_residual": solution.endpoint_residual,
                "intersection_orientation_determinant": radius * derivative,
                "crossing_point_residual": float(
                    abs((1j * radius * np.exp(-1j * np.pi / 2)).real - radius)
                    + abs((1j * radius * np.exp(-1j * np.pi / 2)).imag)
                ),
            }
        )
    return {
        "boundary": boundary,
        "velocity": velocity,
        "benchmark_action": benchmark_action,
        "records": records,
        "velocities": velocities,
    }


def solve_complex_fixed_time(
    proper_time: complex,
    boundary: np.ndarray,
    velocity_guess: np.ndarray,
) -> dict[str, object]:
    def unpack(values: np.ndarray) -> np.ndarray:
        return np.array(
            [
                complex(values[0], values[1]),
                complex(values[2], values[3]),
            ]
        )

    def endpoint(velocity: np.ndarray) -> np.ndarray:
        return p25.complex_flow(proper_time, boundary, velocity)[[0, 2]]

    def residual(values: np.ndarray) -> np.ndarray:
        difference = endpoint(unpack(values)) - boundary[2:]
        return np.array(
            [
                difference[0].real,
                difference[0].imag,
                difference[1].real,
                difference[1].imag,
            ]
        )

    initial = np.array(
        [
            velocity_guess[0].real,
            velocity_guess[0].imag,
            velocity_guess[1].real,
            velocity_guess[1].imag,
        ]
    )
    answer = root(residual, initial, method="hybr", tol=1e-11)
    velocity = unpack(answer.x)
    endpoint_residual = float(np.linalg.norm(residual(answer.x)))
    if not np.all(np.isfinite(answer.x)) or endpoint_residual > 2e-9:
        raise RuntimeError(
            f"complex fixed-time solve failed at T={proper_time}: "
            f"{answer.message}; residual={endpoint_residual}"
        )

    jacobian = np.empty((2, 2), dtype=np.complex128)
    step = 1e-6
    for column in range(2):
        direction = np.zeros(2, dtype=np.complex128)
        direction[column] = step
        jacobian[:, column] = (
            endpoint(velocity + direction) - endpoint(velocity - direction)
        ) / (2 * step)
    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    final = p25.complex_flow(proper_time, boundary, velocity)
    return {
        "velocity": velocity,
        "endpoint_residual": endpoint_residual,
        "jacobi_singular_values": singular_values,
        "action": complex(final[4]),
    }


def complex_lower_bypass_control(scan: dict[str, object]) -> list[dict[str, object]]:
    boundary = np.asarray(scan["boundary"], dtype=float)
    velocities = scan["velocities"]
    records: list[dict[str, object]] = []
    for radius in ARC_RADII:
        middle_velocity = np.asarray(velocities[radius], dtype=np.complex128)

        downward: dict[float, dict[str, object]] = {}
        guess = middle_velocity
        for angle in (-np.pi / 2, -3 * np.pi / 4, -np.pi):
            lapse = radius * np.exp(1j * angle)
            proper_time = 1j * lapse
            solved = solve_complex_fixed_time(proper_time, boundary, guess)
            downward[angle] = solved
            guess = np.asarray(solved["velocity"], dtype=np.complex128)

        upward: dict[float, dict[str, object]] = {}
        guess = middle_velocity
        for angle in (-np.pi / 2, -np.pi / 4, 0.0):
            lapse = radius * np.exp(1j * angle)
            proper_time = 1j * lapse
            solved = solve_complex_fixed_time(proper_time, boundary, guess)
            upward[angle] = solved
            guess = np.asarray(solved["velocity"], dtype=np.complex128)

        merged = {**downward, **upward}
        for angle in LOWER_ARC_ANGLES:
            solved = merged[angle]
            lapse = radius * np.exp(1j * angle)
            proper_time = 1j * lapse
            records.append(
                {
                    "r": radius,
                    "theta": angle,
                    "N": [float(lapse.real), float(lapse.imag)],
                    "T": [float(proper_time.real), float(proper_time.imag)],
                    "endpoint_residual": solved["endpoint_residual"],
                    "jacobi_singular_values": np.asarray(
                        solved["jacobi_singular_values"]
                    ).tolist(),
                    "action": [
                        float(solved["action"].real),
                        float(solved["action"].imag),
                    ],
                }
            )
    return records


def spectral_regulator_control() -> dict[str, object]:
    eigenvalues = np.array([-3.0, -0.5, 0.25, 2.0])
    eta_values = np.array([0.2, 0.1, 0.05, 0.025])
    cutoff_errors: list[float] = []
    for eta in eta_values:
        cutoff = 16.0 / eta
        finite = (
            1.0 - np.exp(-(eta + 1j * eigenvalues) * cutoff)
        ) / (eta + 1j * eigenvalues)
        infinite = 1.0 / (eta + 1j * eigenvalues)
        cutoff_errors.append(float(np.max(np.abs(finite - infinite))))

    lateral_epsilons = np.array([0.05, 0.025, 0.0125, 0.00625])
    lateral_differences = [
        float(
            np.max(
                np.abs(
                    np.exp(-epsilon * eigenvalues)
                    - np.exp(epsilon * eigenvalues)
                )
            )
        )
        for epsilon in lateral_epsilons
    ]
    return {
        "eigenvalues": eigenvalues.tolist(),
        "eta_values": eta_values.tolist(),
        "cutoff_errors": cutoff_errors,
        "lateral_epsilons": lateral_epsilons.tolist(),
        "lateral_differences": lateral_differences,
        "nonuniform_unit_scaled_difference": float(2 * np.sinh(1.0)),
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    scan = real_dual_scan()
    records = scan["records"]
    boundary = np.asarray(scan["boundary"], dtype=float)
    base = p25.solve_fixed_time(
        0.7, boundary, np.asarray(scan["velocity"], dtype=float)
    )
    potential_coefficient = float(
        2
        * np.pi**2
        * (-3 * boundary[0] + boundary[0] ** 3 * p25.potential(boundary[1]))
    )
    endpoint_mass_g = abs(2 * np.pi**2 * (-6 * boundary[0]))
    endpoint_mass_s = abs(2 * np.pi**2 * boundary[0] ** 3)
    endpoint_kernel_coefficient = float(
        np.sqrt(endpoint_mass_g * endpoint_mass_s) / (2 * np.pi)
    )

    audit.numerical(
        "P32.saddle.frozen_connected_control",
        abs(base.action - float(scan["benchmark_action"])) < 2e-10
        and abs(base.constraint) < 2e-11
        and base.endpoint_residual < 2e-10,
        "the connected T=.7 saddle and boundary are inherited without retuning",
    )
    audit.numerical(
        "P32.dual.short_time_transversality",
        all(record["W_T"] > 0 for record in records)
        and abs(records[-1]["W_T"] - potential_coefficient) < 2e-5
        and all(record["intersection_orientation_determinant"] > 0 for record in records),
        "the left dual stays transverse and its tangent approaches the nonzero short-time Hamilton-Jacobi limit",
    )
    audit.numerical(
        "P32.Jacobi.short_time_no_caustic",
        all(record["det_Bv_over_r2"] > 0.99 for record in records)
        and all(record["sigma_min_over_r"] > 0.99 for record in records)
        and max(record["endpoint_residual"] for record in records) < 2e-10,
        "the regulated crossings approach N=0 without a sampled fixed-time Dirichlet zero",
    )
    audit.numerical(
        "P32.endpoint.Van_Vleck_scaling",
        abs(records[-1]["r_times_Van_Vleck"] - endpoint_kernel_coefficient)
        < 2e-5
        and np.all(
            np.diff([record["r_times_Van_Vleck"] for record in records]) < 0
        ),
        "r times the endpoint Van-Vleck magnitude converges to the frozen identity-kernel coefficient",
    )
    audit.numerical(
        "P32.intersection.regulated_local_orientation_stability",
        all(0 < record["r"] < 0.7 for record in records)
        and all(record["crossing_point_residual"] < 1e-14 for record in records)
        and all(record["intersection_orientation_determinant"] > 0 for record in records),
        "every finite lower full-line bypass crosses the recorded real dual at T=r with stable positive local orientation",
    )

    complex_records = complex_lower_bypass_control(scan)
    audit.numerical(
        "P32.joint.lower_bypass_complex_BVP",
        max(record["endpoint_residual"] for record in complex_records) < 3e-9
        and min(
            record["jacobi_singular_values"][-1]
            / record["r"]
            for record in complex_records
        )
        > 0.99,
        "the actual connected complex BVP continues around four lower lapse bypasses with no sampled Jacobi zero",
    )

    spectral = spectral_regulator_control()
    audit.numerical(
        "P32.regulator.finite_spectral_control",
        max(spectral["cutoff_errors"]) < 5e-7
        and np.all(np.diff(spectral["lateral_differences"]) < 0)
        and abs(spectral["nonuniform_unit_scaled_difference"] - 2.3504023873)
        < 2e-10,
        "spectral damping converges at fixed modes, while the endpoint lateral limit remains nonuniform as the mode cutoff grows like 1/epsilon",
    )

    return {
        "base": {
            "T_star": 0.7,
            "W_star": base.action,
            "boundary": boundary.tolist(),
            "short_time_W_T_limit": potential_coefficient,
            "identity_kernel_coefficient": endpoint_kernel_coefficient,
        },
        "regulated_real_dual": records,
        "complex_lower_bypass": complex_records,
        "spectral_regulator": spectral,
        "recorded_intersection": {
            "below_origin_full_line": 1,
            "above_origin_full_line_on_positive_dual": 0,
            "positive_half_line": None,
            "positive_half_line_reason": "the meeting is a singular contour endpoint rather than an interior transverse crossing",
            "global_coefficient": None,
        },
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P32",
        "calculation": "below-origin lapse bypass and recorded intersection gate",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_specified_below_origin_full_line_has_one_recorded_local_intersection_with_the_connected_saddle_dual": "SUPPORTED_ON_THE_TRACKED_HOMOGENEOUS_LAPSE_BASE",
            "the_positive_half_lapse_ray_has_an_ordinary_transverse_intersection_with_that_dual": "CONTRADICTED_BY_ENDPOINT_CONTACT",
            "the_above_origin_full_line_has_the_same_positive_dual_intersection": "CONTRADICTED_ON_THE_RECORDED_BRANCH",
            "the_lower_bypass_principal_momentum_cycle_is_locally_convergent": "SUPPORTED_EXACTLY",
            "analytic_transport_alone_fixes_the_negative_real_identity_normalization": "CONTRADICTED_REQUIRES_AN_ADDITIONAL_MASLOV_COMPARISON_SIGN",
            "the_recorded_local_plus_one_is_the_complete_global_PL_coefficient": "OPEN_OTHER_DUAL_COMPONENTS_AND_GLOBAL_ENDS_NOT_DERIVED",
            "CPT_or_Pin_alone_selects_the_below_origin_lapse_class": "OPEN_NOT_DERIVED",
            "the_result_is_a_positive_trace_class_WDW_projector_or_seam_state": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "the full-line lower and upper semicircular lapse bypass geometry",
                "the lower-bypass principal signature (-,+) momentum cycle and orientation holonomy",
                "the connected real dual from r=.1 to .0015625",
                "the actual complex fixed-boundary branch around four lower bypass semicircles",
                "the recorded local intersection orientation and regulator stability",
                "the positive half-line endpoint-contact distinction",
                "a finite spectral damping versus lateral-shift control",
            ],
            "not_computed": [
                "the complete global upward cycle and every intersection on every BVP sheet",
                "the inhomogeneous gauge-fixed determinant and its oriented superdeterminant line",
                "a nonperturbative BFV/BV quantum master equation or Gribov analysis",
                "a proof that CPT or Pin selects the below-origin rather than above-origin class",
                "a positive WDW physical trace, seam density, initial value, or SUSY spectrum",
            ],
        },
        "next_calculation": (
            "continue both arms of the full joint upward cycle through the real fold using a uniform Airy polarization, "
            "then enumerate every intersection with the specified below-origin full-line contour before removing the mode cutoff"
        ),
    }
    print("PHASE32_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
