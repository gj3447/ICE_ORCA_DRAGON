#!/usr/bin/env python3
"""Phase 22 — finite-mode CPT-like seam density control.

This executable constructs an exact thermofield-double-like purification for
one free supersymmetric oscillator with omega>0 and beta>0.  It checks the
fixed-energy SUSY algebra, density-matrix normalization and positivity, a
graded anti-linear sheet involution, finite cross-sheet correlations, and the
elementary Schwinger--Keldysh trace identity.  It also proves that the same
unregulated noncompact Gaussian ansatz has no trace-class omega=0 limit.

The result is a finite-mode state-preparation witness.  It is not a 4d Pin
lift, a physical thermal-SUSY vacuum, a BRST construction, a WDW projector, or
a full gravitino--Goldstino--ghost seam state.  The program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import sympy as sp


@dataclass
class Audit:
    exact_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)

    def exact(self, check_id: str, condition: bool, statement: str) -> None:
        if check_id in self.exact_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[PASS] {check_id}: {statement}")


def exact_zero(expression: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(expression, sp.MatrixBase):
        return (
            expression.applyfunc(
                lambda entry: sp.simplify(sp.factor(entry.rewrite(sp.exp)))
            ).is_zero_matrix
            is True
        )
    return sp.simplify(sp.factor(expression.rewrite(sp.exp))) == 0


def susy_oscillator_controls(audit: Audit) -> dict[str, object]:
    omega = sp.symbols("omega", positive=True, real=True)
    root = sp.sqrt(2 * omega)
    # Basis: |1_B,0_F>, |0_B,1_F> in the E=omega supermultiplet.
    charge = root * sp.Matrix([[0, 1], [0, 0]])
    adjoint = charge.H
    hamiltonian = omega * sp.eye(2)
    parity = sp.diag(1, -1)

    audit.exact(
        "P22.susy.charge_nilpotent",
        exact_zero(charge * charge),
        "the fixed-energy odd charge obeys Q^2=0",
    )
    audit.exact(
        "P22.susy.adjoint_nilpotent",
        exact_zero(adjoint * adjoint),
        "the positive-Hilbert adjoint obeys (Q^dagger)^2=0",
    )
    audit.exact(
        "P22.susy.positive_closure",
        exact_zero(charge * adjoint + adjoint * charge - 2 * hamiltonian),
        "{Q,Q^dagger}=2H on the E=omega supermultiplet",
    )
    audit.exact(
        "P22.susy.energy_conservation",
        exact_zero(hamiltonian * charge - charge * hamiltonian),
        "[H,Q]=0 on the fixed-energy supermultiplet",
    )
    audit.exact(
        "P22.susy.fermion_oddness",
        exact_zero(parity * charge + charge * parity),
        "the charge anticommutes with fermion parity",
    )

    return {
        "basis": ["|1_B,0_F>", "|0_B,1_F>"],
        "hamiltonian": "omega I_2",
        "charge": "sqrt(2 omega) |1_B,0_F><0_B,1_F|",
        "scope": "one invariant positive-energy supermultiplet of the full oscillator",
    }


def density_and_theta_controls(audit: Audit) -> dict[str, object]:
    r, omega = sp.symbols("r omega", positive=True, real=True)
    cutoff = sp.symbols("N", integer=True, nonnegative=True)
    positive_parameter = sp.symbols("t", positive=True, real=True)
    convergent_r = positive_parameter / (1 + positive_parameter)
    boson_partial_norm = 1 - convergent_r ** (cutoff + 1)
    fermion_state = sp.Matrix([1, 0, 0, sp.I * sp.sqrt(r)]) / sp.sqrt(1 + r)
    fermion_norm = (fermion_state.H * fermion_state)[0]
    rho_f = sp.diag(1, r) / (1 + r)
    rho_pair = sp.simplify(fermion_state * fermion_state.H)
    coefficient_matrix = sp.diag(1, sp.I * sp.sqrt(r)) / sp.sqrt(1 + r)
    reduced_from_partial_trace = sp.simplify(
        coefficient_matrix * coefficient_matrix.H
    )
    z_boson = 1 / (1 - r)
    z_fermion = 1 + r
    partition = (1 + r) / (1 - r)

    audit.exact(
        "P22.density.boson_geometric_norm",
        sp.limit(boson_partial_norm, cutoff, sp.oo) == 1,
        "the bosonic TFD geometric series has unit norm for 0<r<1",
    )
    audit.exact(
        "P22.density.fermion_pair_norm",
        exact_zero(fermion_norm - 1),
        "the graded fermion pair has unit norm",
    )
    audit.exact(
        "P22.density.pure_projector_hermitian",
        exact_zero(rho_pair - rho_pair.H),
        "the normalized pair defines a Hermitian pure density matrix",
    )
    audit.exact(
        "P22.density.pure_projector_trace_one",
        exact_zero(sp.trace(rho_pair) - 1),
        "the pure pair density matrix has unit trace",
    )
    audit.exact(
        "P22.density.pure_projector_idempotent_rank_one",
        exact_zero(rho_pair * rho_pair - rho_pair) and rho_pair.rank() == 1,
        "the pure pair density matrix is idempotent and rank one",
    )
    audit.exact(
        "P22.density.partial_trace",
        exact_zero(reduced_from_partial_trace - rho_f),
        "the coefficient-matrix partial trace gives diag(1,r)/(1+r)",
    )
    audit.exact(
        "P22.density.reduced_trace",
        exact_zero(sp.trace(rho_f) - 1),
        "the reduced fermion density matrix has unit trace",
    )
    audit.exact(
        "P22.density.full_reduced_positivity",
        sp.simplify((1 - convergent_r) / (1 + convergent_r)).is_positive
        is True
        and convergent_r.is_positive is True,
        "all Gibbs eigenweights are positive because p_(n,f)=(1-r)r^(n+f)/(1+r) with 0<r<1",
    )
    audit.exact(
        "P22.density.gibbs_partition",
        exact_zero(z_boson * z_fermion - partition),
        "Z=Z_B Z_F=(1+r)/(1-r) follows from the boson and fermion factors",
    )

    # Equal Gibbs weights in every positive-energy SUSY doublet.
    level = sp.symbols("m", integer=True, positive=True)
    weight_boson = r**level / partition
    weight_fermion = r ** ((level - 1) + 1) / partition
    audit.exact(
        "P22.density.supermultiplet_equal_weights",
        exact_zero(weight_boson - weight_fermion),
        "rho_plus gives equal weight to both states in every E=m omega supermultiplet",
    )

    mean_energy_over_omega = convergent_r / (
        1 - convergent_r
    ) + convergent_r / (1 + convergent_r)
    audit.exact(
        "P22.density.finite_temperature_not_zero_energy",
        exact_zero(
            mean_energy_over_omega
            - 2 * convergent_r / (1 - convergent_r**2)
        )
        and mean_energy_over_omega.is_positive is True,
        "<H>/omega=2r/(1-r^2)>0, so finite-r is not the positive-H vacuum",
    )

    graded_swap = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -1],
        ]
    )
    total_parity = sp.diag(1, -1, -1, 1)
    number_total = sp.diag(0, 1, 1, 2)

    audit.exact(
        "P22.theta.involution_square",
        graded_swap * graded_swap.conjugate() == sp.eye(4),
        "Theta_toy=S_g K squares to one in the displayed occupation convention",
    )
    audit.exact(
        "P22.theta.state_invariance",
        exact_zero(graded_swap * fermion_state.conjugate() - fermion_state),
        "the phase-i fermion pair is invariant under the graded anti-linear swap",
    )
    audit.exact(
        "P22.theta.parity_compatibility",
        exact_zero(graded_swap * total_parity - total_parity * graded_swap),
        "the toy involution commutes with total fermion parity",
    )
    audit.exact(
        "P22.theta.energy_compatibility",
        exact_zero(graded_swap * number_total - number_total * graded_swap),
        "the toy involution preserves the doubled occupation energy",
    )

    ordinary_swap = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    audit.exact(
        "P22.theta.ungraded_swap_mutant_rejected",
        not exact_zero(ordinary_swap * fermion_state.conjugate() - fermion_state),
        "an ungraded sheet-swap mutant does not preserve the phase-i pair",
    )

    return {
        "r": "exp(-beta omega), 0<r<1",
        "boson_factor": "sqrt(1-r) sum_n r^(n/2)|n,n>",
        "fermion_factor": "(|00>+i sqrt(r)|11>)/sqrt(1+r)",
        "reduced_state": "rho_plus=Z^-1 exp(-beta H)",
        "partition": "Z=(1+r)/(1-r)",
        "theta": "(boson sheet swap tensor graded fermion swap) K",
        "warning": "Theta_toy is not a spacetime Clifford/Pin lift",
    }


def correlation_and_sk_controls(audit: Audit) -> dict[str, object]:
    beta, omega = sp.symbols("beta omega", positive=True, real=True)
    x = beta * omega / 2
    r = sp.exp(-2 * x)
    variance = (1 + r) / (2 * omega * (1 - r))
    cross = sp.sqrt(r) / (omega * (1 - r))
    coefficient = sp.simplify(cross / variance)

    audit.exact(
        "P22.bridge.local_covariance",
        exact_zero(variance - sp.coth(x) / (2 * omega)),
        "<x_plus^2>=coth(beta omega/2)/(2 omega)",
    )
    audit.exact(
        "P22.bridge.cross_covariance",
        exact_zero(cross - 1 / (2 * omega * sp.sinh(x))),
        "<x_plus x_minus>=1/[2 omega sinh(beta omega/2)]",
    )
    audit.exact(
        "P22.bridge.normalized_coefficient",
        exact_zero(coefficient - sp.sech(x)),
        "the normalized cross-sheet coefficient is sech(beta omega/2)",
    )

    dtn = omega * sp.Matrix(
        [[sp.coth(x), -sp.csch(x)], [-sp.csch(x), sp.coth(x)]]
    )
    audit.exact(
        "P22.bridge.amplitude_density_factor_two",
        exact_zero(dtn.inv()[0, 1] / 2 - cross),
        "the density covariance is one half of the Euclidean amplitude-kernel inverse",
    )

    r_symbol = sp.symbols("r", positive=True, real=True)
    rho_f = sp.diag(1, r_symbol) / (1 + r_symbol)
    unitary = sp.diag(1, sp.I)
    audit.exact(
        "P22.SK.equal_source_unitarity",
        exact_zero(sp.trace(unitary * rho_f * unitary.H) - 1),
        "Tr(U rho U^dagger)=1 for the exact finite CAR source rotation",
    )
    audit.exact(
        "P22.SK.wrong_adjoint_mutant_rejected",
        exact_zero(
            sp.trace(unitary * rho_f * unitary) - (1 - r_symbol) / (1 + r_symbol)
        )
        and sp.simplify((1 - r_symbol) / (1 + r_symbol) - 1) != 0,
        "replacing U^dagger by U fails the normalized closed-time-path identity",
    )

    return {
        "cross_covariance": "1/[2 omega sinh(beta omega/2)]",
        "normalized_coefficient": "sech(beta omega/2)",
        "euclidean_interval": "L=beta/2",
        "kernel_distinction": "the wavefunction uses K_DtN while |Psi|^2 has covariance (2K_DtN)^-1",
        "SK_identity": "Tr(U rho_plus U^dagger)=1",
        "warning": "this is unitarity, not a constructed SK BRST quartet",
    }


def zero_mode_controls(audit: Audit) -> dict[str, object]:
    beta, omega = sp.symbols("beta omega", positive=True, real=True)
    r = sp.exp(-beta * omega)
    z_boson = 1 / (1 - r)
    z_fermion = 1 + r
    variance = sp.coth(beta * omega / 2) / (2 * omega)
    stiffness = omega * sp.tanh(beta * omega / 2)

    audit.exact(
        "P22.zero_mode.boson_partition_diverges",
        sp.limit(z_boson, omega, 0, dir="+") == sp.oo
        and sp.limit(beta * omega * z_boson, omega, 0, dir="+") == 1,
        "Z_B diverges as 1/(beta omega) in the noncompact oscillator limit",
    )
    audit.exact(
        "P22.zero_mode.fermion_partition_finite",
        sp.limit(z_fermion, omega, 0, dir="+") == 2,
        "the fermion partition remains finite and tends to two",
    )
    audit.exact(
        "P22.zero_mode.coordinate_variance_diverges",
        sp.limit(variance, omega, 0, dir="+") == sp.oo
        and sp.limit(beta * omega**2 * variance, omega, 0, dir="+") == 1,
        "the coordinate covariance diverges as 1/(beta omega^2)",
    )
    audit.exact(
        "P22.zero_mode.diagonal_stiffness_vanishes",
        sp.limit(stiffness, omega, 0, dir="+") == 0
        and sp.limit(
            stiffness / (beta * omega**2 / 2), omega, 0, dir="+"
        )
        == 1,
        "the diagonal Gaussian stiffness vanishes as beta omega^2/2",
    )

    return {
        "limit": "omega->0+ at fixed beta>0",
        "boson_partition": "Z_B~1/(beta omega) -> infinity",
        "fermion_partition": "Z_F->2",
        "coordinate_variance": "<x^2>~1/(beta omega^2) -> infinity",
        "diagonal_stiffness": "Omega~beta omega^2/2 ->0",
        "interpretation": (
            "the unregulated noncompact free Gaussian has no trace-class zero-mode "
            "limit; this does not decide a compact zero mode or the interacting "
            "gravitational inflaton minisuperspace"
        ),
    }


def run() -> dict[str, object]:
    audit = Audit()
    susy = susy_oscillator_controls(audit)
    density = density_and_theta_controls(audit)
    bridge = correlation_and_sk_controls(audit)
    zero_mode = zero_mode_controls(audit)

    result: dict[str, object] = {
        "phase": "P22",
        "calculation": "finite-mode CPT-like seam density control",
        "exact_checks": audit.exact_passed,
        "numerical_checks": 0,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": [],
        "exact_check_records": audit.exact_records,
        "numerical_check_records": [],
        "susy_oscillator": susy,
        "density_and_theta": density,
        "bridge_and_SK": bridge,
        "zero_mode": zero_mode,
        "claim_status": {
            "positive_frequency_TFD_like_density_is_normalized_and_positive": "SUPPORTED_IN_FINITE_MODE_CONTROL",
            "reduced_Gibbs_density_commutes_with_fixed_mode_supercharges": "SUPPORTED_AS_COVARIANCE_NOT_VACUUM_SUSY",
            "graded_anti_linear_sheet_involution_exists": "SUPPORTED_AS_TOY_REAL_STRUCTURE",
            "full_4d_Pin_lift_from_toy_involution": "OPEN_NOT_CONSTRUCTED",
            "finite_density_satisfies_equal_source_SK_normalization": "SUPPORTED_AS_UNITARITY_IDENTITY",
            "free_noncompact_zero_mode_has_a_trace_class_TFD_limit": "CONTRADICTED",
            "finite_mode_state_selects_flux_or_inflaton_initial_data": "OPEN_NOT_COMPUTED",
            "full_gravitino_Goldstino_ghost_seam_density_exists": "OPEN_NOT_COMPUTED",
        },
        "scope_guard": {
            "what_is_computed": [
                "one free 0+1 supersymmetric oscillator",
                "omega>0 and beta>0 exact thermofield-double-like purification",
                "fixed-energy positive-Hilbert SUSY algebra",
                "mode-level graded anti-linear sheet involution",
                "finite cross-sheet density covariance",
                "elementary density-matrix Schwinger-Keldysh trace identity",
                "the omega->0+ limit in the unregulated noncompact oscillator representation",
            ],
            "what_is_not_computed": [
                "an unbroken physical thermal supersymmetry generator",
                "a 4d Clifford or Pin lift",
                "an infinite-mode Hilbert-Schmidt or UV-renormalized product state",
                "an SK ghost quartet or BRST cohomology",
                "a gravitino-Goldstino-ghost boundary kernel",
                "a Wheeler-DeWitt physical projector, current, or Born measure",
                "a distribution over flux n or inflaton phi0",
                "a persistent SUSY-breaking scale or observable particle spectrum",
            ],
        },
        "obstruction_guards": [
            {
                "id": "P22.guard.free_noncompact_zero_mode_trace_class",
                "target": "a trace-class omega=0 limit of the displayed free Gaussian state",
                "observed_status": "EXPECTED_OBSTRUCTION_CONFIRMED",
                "supporting_check_ids": [
                    "P22.zero_mode.boson_partition_diverges",
                    "P22.zero_mode.coordinate_variance_diverges",
                    "P22.zero_mode.diagonal_stiffness_vanishes",
                ],
                "scope": "unregulated noncompact L2(R) oscillator limit at fixed beta>0",
            }
        ],
        "next_calculation": {
            "homogeneous_sector": (
                "replace the free omega=0 insertion by the constrained complex-cap "
                "minisuperspace action, primed determinant, collective-coordinate "
                "Jacobian, and physical WDW current"
            ),
            "local_sugra_sector": (
                "derive the coupled gauge-fixed gravitino-Goldstino-ghost boundary "
                "operator and test the projected density for positivity and trace class"
            ),
        },
    }
    print("PHASE22_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
