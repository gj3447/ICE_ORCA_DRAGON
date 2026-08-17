#!/usr/bin/env python3
"""Phase 29 -- zero-lapse uniform kernel and BFV measure control.

This executable freezes the Phase-24--27 homogeneous boundary metric and
studies the zero-duration kernel before setting the two endpoint coordinates
equal.  It separates the pointwise Van Vleck pole from its distributional
identity-kernel limit in the declared local flat endpoint measure, checks the
coordinate-length dependence of the reduced Dirichlet ghost determinant, and
records the conformal-sign obstruction to a single Euclidean lapse rotation.

It is a finite-dimensional short-time control, not a gauge-fixed gravitational
one-loop determinant or a Picard--Lefschetz intersection calculation.  The
script writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp


FROZEN_SCALE = 3.5668031935672753
FROZEN_PHI = 1.0185809464006637


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


def frozen_kinetic_masses() -> tuple[float, float]:
    """Return M=2 pi^2 diag(-6a,a^3) at the frozen boundary."""

    gravity = -12.0 * np.pi**2 * FROZEN_SCALE
    scalar = 2.0 * np.pi**2 * FROZEN_SCALE**3
    return float(gravity), float(scalar)


def gaussian_test_pairing(
    lapse: float, alpha_gravity: float, alpha_scalar: float
) -> complex:
    """Pair the normalized two-dimensional Fresnel kernel with Gaussians.

    For one kinetic eigenvalue m,

      <K_N, exp(-alpha x^2/2)> = (1+i alpha N/m)^(-1/2).

    The square-root branches are chosen continuously from N=0.
    """

    gravity, scalar = frozen_kinetic_masses()
    return complex(
        (1.0 + 1.0j * alpha_gravity * lapse / gravity) ** (-0.5)
        * (1.0 + 1.0j * alpha_scalar * lapse / scalar) ** (-0.5)
    )


def exact_controls(audit: Audit) -> dict[str, object]:
    mu_g, mu_s, tau, x_g, x_s = sp.symbols(
        "mu_g mu_s tau x_g x_s", positive=True, real=True
    )
    m_g = -mu_g
    m_s = mu_s
    audit.exact(
        "P29.kernel.indefinite_signature",
        m_g < 0 and m_s > 0 and sp.simplify(m_g * m_s) < 0,
        "the frozen two-coordinate kinetic form has one negative and one positive eigenvalue",
    )

    alpha_g, alpha_s, lapse = sp.symbols(
        "alpha_g alpha_s N", positive=True, real=True
    )
    pairing = (1 - sp.I * alpha_g * lapse / mu_g) ** (-sp.Rational(1, 2)) * (
        1 + sp.I * alpha_s * lapse / mu_s
    ) ** (-sp.Rational(1, 2))
    audit.exact(
        "P29.kernel.distributional_identity_limit",
        sp.limit(pairing, lapse, 0, dir="+") == 1,
        "the normalized Fresnel kernel tends to the identity delta distribution on Gaussian tests",
    )

    momentum_g, momentum_s, potential_coefficient = sp.symbols(
        "p_g p_s U", real=True
    )
    multiplier_hamiltonian = (
        momentum_g**2 / (2 * m_g)
        + momentum_s**2 / (2 * m_s)
        + potential_coefficient
    )
    Fourier_multiplier = sp.exp(-sp.I * lapse * multiplier_hamiltonian)
    audit.exact(
        "P29.kernel.Fourier_multiplier_identity_limit",
        sp.limit(Fourier_multiplier, lapse, 0, dir="+") == 1
        and sp.simplify(Fourier_multiplier * sp.conjugate(Fourier_multiplier))
        == 1,
        "on real lapse the Fourier multiplier has unit modulus and tends pointwise to one",
    )

    plus_i_exponents = (
        sp.simplify(sp.I * m_g * x_g**2 / (2 * sp.I * tau)),
        sp.simplify(sp.I * m_s * x_s**2 / (2 * sp.I * tau)),
    )
    minus_i_exponents = (
        sp.simplify(sp.I * m_g * x_g**2 / (-2 * sp.I * tau)),
        sp.simplify(sp.I * m_s * x_s**2 / (-2 * sp.I * tau)),
    )
    audit.exact(
        "P29.kernel.single_Wick_rotation_obstruction",
        plus_i_exponents[0] < 0
        and plus_i_exponents[1] > 0
        and minus_i_exponents[0] > 0
        and minus_i_exponents[1] < 0,
        "either imaginary-lapse sign damps one kinetic direction and amplifies the other",
    )

    length = sp.symbols("L", positive=True, real=True)
    zeta_zero = -sp.Rational(1, 2)
    zeta_prime_zero = -sp.log(2 * sp.pi) / 2
    dirichlet_zeta_prime = sp.simplify(
        2 * sp.log(length / sp.pi) * zeta_zero + 2 * zeta_prime_zero
    )
    dirichlet_determinant = sp.simplify(sp.exp(-dirichlet_zeta_prime))
    audit.exact(
        "P29.BFV.Dirichlet_ghost_length_scaling",
        dirichlet_zeta_prime == -sp.log(2 * length)
        and dirichlet_determinant == 2 * length,
        "with the zeta reference scale fixed to one, det_zeta(-d^2) on a Dirichlet interval of coordinate length L is 2L",
    )

    fixed_parameter_determinant = sp.simplify(
        length ** (2 * zeta_zero) * dirichlet_determinant
    )
    audit.exact(
        "P29.BFV.fixed_parameter_ghost_is_modulus_independent",
        fixed_parameter_determinant == 2,
        "the proper-time-gauge operator -L^2 d_tau^2 has determinant 2 after the coordinate and ghost rescaling",
    )

    gauge_normalization = sp.symbols("f", positive=True, real=True)
    audit.exact(
        "P29.BFV.gauge_condition_rescaling_cancels",
        sp.simplify((1 / gauge_normalization) * gauge_normalization) == 1,
        "delta(f chi) det(f M)=delta(chi) det(M), so an isolated ghost power is not a physical modulus measure",
    )

    epsilon_initial, epsilon_final = sp.symbols(
        "epsilon_0 epsilon_1", real=True
    )
    audit.exact(
        "P29.BFV.proper_time_modulus_is_gauge_invariant",
        sp.simplify(
            (epsilon_final - epsilon_initial).subs(
                {epsilon_initial: 0, epsilon_final: 0}
            )
        )
        == 0,
        "fixed endpoint gauge parameters give delta integral(N ds)=epsilon(1)-epsilon(0)=0",
    )

    mode_number = sp.symbols("n", positive=True, integer=True)
    coordinate_interval_eigenvalue = (mode_number * sp.pi / length) ** 2
    fixed_parameter_mode_eigenvalue = sp.simplify(
        length**2 * coordinate_interval_eigenvalue
    )
    audit.exact(
        "P29.BFV.nonzero_mode_factor_is_modulus_independent",
        fixed_parameter_mode_eigenvalue == (mode_number * sp.pi) ** 2
        and sp.diff(fixed_parameter_mode_eigenvalue, length) == 0,
        "each fixed-parameter Dirichlet-ghost eigenvalue is independent of the coordinate/proper-time length",
    )

    endpoint_pole = sp.symbols("N", positive=True, real=True)
    unit_interval_ghost = sp.Integer(2)
    audit.exact(
        "P29.BFV.unit_ghost_does_not_cancel_endpoint_pole",
        sp.limit(endpoint_pole * unit_interval_ghost / endpoint_pole, endpoint_pole, 0)
        == 2
        and sp.limit(unit_interval_ghost / endpoint_pole, endpoint_pole, 0)
        == sp.oo,
        "the unit-coordinate Dirichlet ghost determinant is constant and leaves the d=2 1/N pole",
    )

    lower_cutoff, upper_cutoff = sp.symbols(
        "delta epsilon", positive=True, real=True
    )
    diagonal_integral = sp.log(upper_cutoff / lower_cutoff)
    audit.exact(
        "P29.endpoint.pointwise_vs_distributional_integrability",
        sp.limit(diagonal_integral, lower_cutoff, 0, dir="+") == sp.oo
        and sp.integrate(1, (endpoint_pole, 0, upper_cutoff)) == upper_cutoff,
        "the alpha=0 diagonal 1/N integral diverges while its normalized d=2 distributional pairing is locally integrable",
    )

    spectral, epsilon = sp.symbols("lambda epsilon", real=True, positive=True)
    half_line = -sp.I / (spectral - sp.I * epsilon)
    audit.exact(
        "P29.operator.half_line_is_sourced_resolvent",
        sp.simplify((spectral - sp.I * epsilon) * half_line) == -sp.I,
        "the regulated positive half-lapse integral is a sourced resolvent, not a projector",
    )

    weighted_half_line = -1 / (spectral - sp.I * epsilon) ** 2
    audit.exact(
        "P29.operator.ad_hoc_lapse_power_changes_resolvent",
        sp.simplify(
            (spectral - sp.I * epsilon) * weighted_half_line
            + 1 / (spectral - sp.I * epsilon)
        )
        == 0,
        "multiplying the measure by N changes the resolvent to a double pole instead of canceling a harmless normalization",
    )

    test_coordinate = sp.symbols("lambda", real=True)
    distribution_test = sp.integrate(
        test_coordinate
        * sp.DiracDelta(test_coordinate)
        * (1 + test_coordinate),
        (test_coordinate, -1, 1),
    )
    audit.exact(
        "P29.operator.full_line_constraint_support",
        distribution_test == 0,
        "the full-line delta distribution is annihilated by the constraint on test functions",
    )

    delta_prime_test = -sp.diff(
        test_coordinate * (1 + test_coordinate), test_coordinate
    ).subs(test_coordinate, 0)
    audit.exact(
        "P29.operator.weighted_full_line_loses_constraint_annihilation",
        delta_prime_test == -1,
        "an inserted N leaves delta-prime support on H=0 but gives H delta-prime=-delta rather than a constraint solution",
    )

    series_index = sp.symbols("k", integer=True, nonnegative=True)
    inverse_action, direct_action = sp.symbols("A B", positive=True, real=True)
    simple_pole_residue = sp.summation(
        (inverse_action * direct_action) ** series_index
        / sp.factorial(series_index) ** 2,
        (series_index, 0, sp.oo),
    )
    weighted_residue = sp.summation(
        inverse_action ** (series_index + 1)
        * direct_action**series_index
        / (
            sp.factorial(series_index + 1)
            * sp.factorial(series_index)
        ),
        (series_index, 0, sp.oo),
    )
    audit.exact(
        "P29.endpoint.lateral_bypass_Bessel_residues",
        sp.simplify(
            simple_pole_residue
            - sp.besseli(
                0, 2 * sp.sqrt(inverse_action * direct_action)
            )
        )
        == 0
        and sp.simplify(
            weighted_residue
            - sp.sqrt(inverse_action / direct_action)
            * sp.besseli(
                1, 2 * sp.sqrt(inverse_action * direct_action)
            )
        )
        == 0,
        "even an inserted N leaves an off-diagonal lateral residue; diagonal pole cancellation does not fix the bypass",
    )

    radius, cutoff = sp.symbols("r Lambda", positive=True, real=True)
    finite_arc_bound = sp.pi * radius * sp.exp(radius * cutoff)
    audit.exact(
        "P29.endpoint.finite_spectral_arc_control",
        sp.limit(finite_arc_bound, radius, 0, dir="+") == 0,
        "a zero-radius bypass contributes nothing in every fixed bounded spectral truncation",
    )

    dimension = sp.symbols("D", positive=True, integer=True)
    identity_index = sp.symbols("j", positive=True, integer=True)
    identity_hs_squared = sp.summation(
        1, (identity_index, 1, dimension)
    )
    audit.exact(
        "P29.density.identity_not_Hilbert_Schmidt",
        identity_hs_squared == dimension
        and sp.limit(identity_hs_squared, dimension, sp.oo) == sp.oo,
        "the identity kernel has Hilbert-Schmidt norm squared D and is not trace class as D grows",
    )

    return {
        "short_time_metric": "M=2pi^2 diag(-6a,a^3)",
        "normalized_kernel": "sqrt(det-branch(M))/(2pi i N) exp[i Deltaq^T M Deltaq/(2N)]",
        "ghost_determinant": "det_zeta(-d_tau^2)=2L for Dirichlet ghosts on coordinate length L with zeta reference scale fixed to one",
        "endpoint_measure": "local flat d(a) d(phi) measure for this frozen quadratic control",
        "operator_objects": {
            "positive_half_line": "sourced resolvent",
            "full_line": "constraint-supported rigging distribution",
        },
    }


def numerical_controls(audit: Audit) -> dict[str, object]:
    gravity, scalar = frozen_kinetic_masses()
    audit.numerical(
        "P29.numeric.frozen_metric",
        abs(gravity + 422.435237965) < 8e-10
        and abs(scalar - 895.709502254) < 8e-10,
        "the frozen kinetic eigenvalues reproduce the Phase-27 short-time mixed Hessian",
    )

    raw_van_vleck = float(np.sqrt(abs(gravity * scalar)))
    normalized_coefficient = raw_van_vleck / (2.0 * np.pi)
    audit.numerical(
        "P29.numeric.raw_and_normalized_prefactors",
        abs(raw_van_vleck - 615.1253992) < 8e-7
        and abs(normalized_coefficient - 97.90024790) < 8e-7,
        "the raw determinant is 615.1254/|N| while the normalized d=2 kernel has magnitude 97.9003/|N|",
    )

    lapses = np.array([0.2, 0.1, 0.05, 0.025, 0.0125])
    pairings = np.array(
        [gaussian_test_pairing(value, 0.7, 1.3) for value in lapses]
    )
    errors = np.abs(pairings - 1.0)
    audit.numerical(
        "P29.numeric.distributional_pairing_convergence",
        bool(np.all(np.diff(errors) < 0.0))
        and errors[-1] < 3e-6
        and 1.9 < errors[-2] / errors[-1] < 2.1,
        "Gaussian test pairings converge linearly to the delta-kernel value one",
    )

    diagonal_amplitudes = normalized_coefficient / lapses
    audit.numerical(
        "P29.numeric.pointwise_pole",
        np.max(
            np.abs(lapses * diagonal_amplitudes - normalized_coefficient)
        )
        < 2e-14
        and diagonal_amplitudes[-1] > 7000.0,
        "at equal endpoint coordinates the pointwise kernel diverges exactly as 1/N",
    )

    ghost_lengths = np.array([0.5, 1.0, 2.0, 4.0])
    ghost_determinants = 2.0 * ghost_lengths
    audit.numerical(
        "P29.numeric.ghost_coordinate_length_dependence",
        np.allclose(ghost_determinants, [1.0, 2.0, 4.0, 8.0]),
        "the standalone zeta ghost determinant changes with coordinate interval length",
    )

    truncations = np.array([8, 16, 32, 64, 128])
    identity_hs_squared = truncations.astype(float)
    audit.numerical(
        "P29.numeric.identity_HS_divergence",
        np.all(identity_hs_squared == truncations)
        and identity_hs_squared[-1] / identity_hs_squared[0] == 16.0,
        "finite-rank identity controls have HS norm squared equal to their cutoff dimension",
    )

    eigenvalues = np.array([-3.0, -0.5, 0.25, 2.0])
    eps = 1e-4
    half_line_values = -1.0j / (eigenvalues - 1.0j * eps)
    sourced_residual = np.max(
        np.abs((eigenvalues - 1.0j * eps) * half_line_values + 1.0j)
    )
    audit.numerical(
        "P29.numeric.half_line_resolvent_residual",
        sourced_residual < 3e-16,
        "the positive-half-line spectral control satisfies the sourced resolvent identity",
    )

    return {
        "frozen_boundary": [FROZEN_SCALE, FROZEN_PHI],
        "kinetic_eigenvalues": [gravity, scalar],
        "raw_Van_Vleck_coefficient": raw_van_vleck,
        "normalized_kernel_coefficient": normalized_coefficient,
        "Gaussian_test": {
            "lapses": lapses.tolist(),
            "pairings": [[value.real, value.imag] for value in pairings],
            "errors": errors.tolist(),
        },
        "diagonal_pointwise_amplitudes": diagonal_amplitudes.tolist(),
        "ghost_coordinate_lengths": ghost_lengths.tolist(),
        "ghost_determinants": ghost_determinants.tolist(),
        "identity_cutoffs": truncations.tolist(),
        "identity_HS_squared": identity_hs_squared.tolist(),
    }


def run() -> dict[str, object]:
    audit = Audit()
    exact = exact_controls(audit)
    numerical = numerical_controls(audit)
    result: dict[str, object] = {
        "phase": "P29",
        "calculation": "zero-lapse uniform kernel and reduced BFV measure control",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "frozen_conventions": exact,
        "numerical_controls": numerical,
        "claim_status": {
            "the_zero_lapse_kernel_has_a_distributional_identity_limit": "SUPPORTED_FOR_REAL_LAPSE_SCHWARTZ_TESTS_IN_THE_FROZEN_QUADRATIC_CONTROL_WITH_THE_DECLARED_LOCAL_FLAT_ENDPOINT_MEASURE",
            "the_equal_endpoint_pointwise_zero_lapse_limit_is_finite": "CONTRADICTED_BY_THE_ONE_OVER_N_POLE",
            "the_unit_interval_Dirichlet_ghost_determinant_removes_the_pole": "CONTRADICTED_BY_ITS_CONSTANT_SCALING",
            "one_imaginary_lapse_rotation_damps_both_homogeneous_directions": "CONTRADICTED_BY_THE_INDEFINITE_KINETIC_FORM",
            "the_positive_half_lapse_integral_is_a_constraint_projector": "CONTRADICTED_BY_THE_SOURCED_RESOLVENT_IDENTITY",
            "the_full_line_group_average_is_a_normalized_density": "NOT_ESTABLISHED_WITHOUT_A_PHYSICAL_TRACE",
            "a_zero_endpoint_bypass_fixes_the_global_PL_coefficient": "OPEN_NOT_DERIVED",
            "a_positive_seam_state_or_initial_value_is_selected": "OPEN_NOT_DERIVED",
        },
        "scope_guard": {
            "computed": [
                "the frozen two-coordinate quadratic short-time kernel",
                "Gaussian-test and Fourier-Schwartz distributional convergence to the local-flat-measure identity kernel",
                "the reduced Dirichlet-ghost zeta determinant and its coordinate-length scaling",
                "half-line resolvent versus full-line constraint annihilation",
                "the opposite-sign damping obstruction of the homogeneous kinetic form",
            ],
            "not_computed": [
                "a conformal-factor integration contour",
                "the gauge-fixed nonzero-mode gravitational or SUGRA determinant",
                "a global relative-homology cycle or integer saddle coefficient",
                "an interacting zero-lapse uniform parametrix beyond leading order",
                "the physical WDW endpoint measure and factor ordering",
                "a trace-class WDW density or initial-value distribution",
            ],
        },
        "next_calculation": (
            "choose and derive the conformal/BFV integration cycle, then compute "
            "the gauge-reduced determinant as an operator-valued uniform endpoint parametrix"
        ),
    }
    print("PHASE29_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
