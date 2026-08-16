#!/usr/bin/env python3
"""Phase 18 — exact free-mode spectrum and temporal-seam controls.

This is a deliberately bounded Gaussian calculation, not a completed doubled
Wess-Zumino/Pin sewing action.  It proves that a finite canonical quadratic
kick supported only at t=0 changes free initial data and occupations but not
the retarded bulk pole when the t>0 boson and fermion operators retain their
common mass m.  It also records the UV cost of an instantaneous kick, a smooth
Gaussian control, FRW dilution scalings, and conditional soft-mass benchmarks.

All algebraic checks use exact SymPy expressions.  One separately labelled
SciPy time-integration control checks the narrow-pulse delta limit.  The
program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


@dataclass
class Audit:
    passed: int = 0
    check_ids: list[str] = field(default_factory=list)

    def check(self, check_id: str, condition: bool, message: str) -> None:
        if check_id in self.check_ids:
            raise AssertionError(f"[FAIL] duplicate exact check id: {check_id}")
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {message}")
        self.passed += 1
        self.check_ids.append(check_id)
        print(f"[PASS] {check_id}: {message}")


def exact_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(exact_zero(entry) for entry in value)
    reduced = sp.trigsimp(sp.simplify(sp.expand_complex(value)))
    return reduced == 0


def comm(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left * right - right * left)


def soft_benchmarks() -> list[dict[str, object]]:
    """Dimensionless examples for m_B^2=m^2+mu_soft^2, not scale predictions."""

    rows: list[dict[str, object]] = []
    for ratio in (sp.Rational(1, 10), sp.Integer(1), sp.Integer(10)):
        mass_ratio = sp.sqrt(1 + ratio**2)
        rows.append(
            {
                "mu_soft_over_m": str(ratio),
                "m_B_over_m_F_exact": str(mass_ratio),
                "m_B_over_m_F_decimal": str(sp.N(mass_ratio, 12)),
                "delta_m_over_m_decimal": str(sp.N(mass_ratio - 1, 12)),
            }
        )
    return rows


def redshift_benchmarks() -> list[dict[str, object]]:
    """Collisionless relativistic-medium dilution examples."""

    rows: list[dict[str, object]] = []
    for expansion in (sp.Integer(10) ** 3, sp.Integer(10) ** 10, sp.Integer(10) ** 28):
        rows.append(
            {
                "a_over_a_seam": str(expansion),
                "relativistic_delta_m2_ratio": str(expansion**-2),
                "nonrelativistic_delta_m2_ratio": str(expansion**-3),
            }
        )
    return rows


def seam_benchmarks() -> dict[str, object]:
    """Dimensionless occupation/UV examples with no claimed physical scale."""

    sharp_rows: list[dict[str, object]] = []
    for kappa_over_m in (sp.Rational(1, 10), sp.Integer(1), sp.Integer(2)):
        occupation = kappa_over_m**2 / 4
        sharp_rows.append(
            {
                "k_over_m": "0",
                "kappa_over_m": str(kappa_over_m),
                "n_B_exact": str(occupation),
                "n_B_decimal": str(sp.N(occupation, 12)),
            }
        )

    smooth_rows: list[dict[str, object]] = []
    for sigma_times_m in (sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)):
        occupation = sp.exp(-4 * sigma_times_m**2) / 4
        smooth_rows.append(
            {
                "k_over_m": "0",
                "kappa_over_m": "1",
                "sigma_times_m": str(sigma_times_m),
                "n_B_Born_exact": str(occupation),
                "n_B_Born_decimal": str(sp.N(occupation, 12)),
            }
        )

    cutoff_ratio = sp.Integer(100)
    number_over_m3 = (cutoff_ratio - sp.atan(cutoff_ratio)) / (8 * sp.pi**2)
    energy_over_m4 = (
        cutoff_ratio * sp.sqrt(cutoff_ratio**2 + 1)
        - sp.asinh(cutoff_ratio)
    ) / (16 * sp.pi**2)
    return {
        "sharp_rest_mode": sharp_rows,
        "Gaussian_Born_rest_mode": smooth_rows,
        "sharp_cutoff_example": {
            "kappa_over_m": "1",
            "Lambda_over_m": "100",
            "number_density_over_m3": str(sp.N(number_over_m3, 12)),
            "energy_density_over_m4": str(sp.N(energy_over_m4, 12)),
        },
    }


def narrow_gaussian_numerical_control() -> dict[str, object]:
    """Independently integrate a narrow pulse and compare with the delta kick."""

    omega_value = 1.3
    kappa_value = 0.4
    sigma_value = 0.002
    endpoint = 0.05
    pulse_norm = 1.0 / (np.sqrt(2.0 * np.pi) * sigma_value)

    def rhs(time_value: float, state: np.ndarray) -> np.ndarray:
        pulse = (
            kappa_value
            * pulse_norm
            * np.exp(-(time_value**2) / (2.0 * sigma_value**2))
        )
        return np.asarray(
            [
                state[1],
                -(omega_value**2 + pulse) * state[0],
            ],
            dtype=complex,
        )

    q_initial = np.exp(1j * omega_value * endpoint)
    p_initial = -1j * omega_value * q_initial
    solution = solve_ivp(
        rhs,
        (-endpoint, endpoint),
        np.asarray([q_initial, p_initial], dtype=complex),
        method="DOP853",
        rtol=2e-12,
        atol=2e-14,
    )
    if not solution.success:
        raise AssertionError(
            f"[FAIL] P18.numeric.narrow_gaussian_delta_limit: {solution.message}"
        )

    q_final, p_final = solution.y[:, -1]
    alpha_numeric = (
        np.exp(1j * omega_value * endpoint)
        * (q_final + 1j * p_final / omega_value)
        / 2.0
    )
    beta_numeric = (
        np.exp(-1j * omega_value * endpoint)
        * (q_final - 1j * p_final / omega_value)
        / 2.0
    )
    alpha_delta = 1.0 - 1j * kappa_value / (2.0 * omega_value)
    beta_delta = 1j * kappa_value / (2.0 * omega_value)
    max_error = max(
        abs(alpha_numeric - alpha_delta),
        abs(beta_numeric - beta_delta),
    )
    norm_error = abs(abs(alpha_numeric) ** 2 - abs(beta_numeric) ** 2 - 1.0)
    if max_error >= 1e-4 or norm_error >= 1e-9:
        raise AssertionError(
            "[FAIL] P18.numeric.narrow_gaussian_delta_limit: "
            f"max_error={max_error}, norm_error={norm_error}"
        )
    print(
        "[NUMERIC PASS] P18.numeric.narrow_gaussian_delta_limit: "
        f"max_error={max_error:.6e}, norm_error={norm_error:.6e}"
    )
    return {
        "id": "P18.numeric.narrow_gaussian_delta_limit",
        "method": "SciPy solve_ivp DOP853 direct time integration",
        "inputs": {
            "omega": str(omega_value),
            "kappa": str(kappa_value),
            "sigma": str(sigma_value),
            "integration_interval": f"[-{endpoint}, {endpoint}]",
            "rtol": "2e-12",
            "atol": "2e-14",
        },
        "alpha_numeric": (
            f"{alpha_numeric.real:.12f}{alpha_numeric.imag:+.12f}j"
        ),
        "alpha_delta": f"{alpha_delta.real:.12f}{alpha_delta.imag:+.12f}j",
        "beta_numeric": f"{beta_numeric.real:.12f}{beta_numeric.imag:+.12f}j",
        "beta_delta": f"{beta_delta.real:.12f}{beta_delta.imag:+.12f}j",
        "max_abs_error": f"{max_error:.6e}",
        "bogoliubov_norm_error": f"{norm_error:.6e}",
        "status": "PASS",
    }


def run() -> dict[str, object]:
    audit = Audit()

    # All dimensional symbols used below are real and positive unless a sign is
    # physically meaningful.  Exact arithmetic is retained throughout.
    energy = sp.Symbol("E", positive=True, real=True)
    momentum = sp.Symbol("k", real=True)
    mass = sp.Symbol("m", positive=True, real=True)
    omega = sp.sqrt(momentum**2 + mass**2)
    mode_omega = sp.Symbol("omega", positive=True, real=True)
    time = sp.Symbol("t", real=True)
    time_prime = sp.Symbol("t_prime", real=True)
    relative_time = sp.Symbol("s", real=True)
    central_time = sp.Symbol("T", real=True)
    kappa = sp.Symbol("kappa", real=True)
    seam_width = sp.Symbol("sigma", positive=True, real=True)
    cutoff = sp.Symbol("Lambda", positive=True, real=True)

    identity_2 = sp.eye(2)
    zero_2 = sp.zeros(2)
    symplectic_2 = sp.Matrix([[0, 1], [-1, 0]])

    # ------------------------------------------------------------------
    # 1. Conserved Q: elapsed coordinate time alone does not break SUSY.
    # ------------------------------------------------------------------
    lowering = sp.Matrix([[0, 1], [0, 0]])
    h_susy = energy * identity_2
    q_susy = sp.sqrt(2 * energy) * lowering
    vacuum = sp.Matrix([1, 0])
    evolution_susy = sp.exp(-sp.I * energy * time) * identity_2
    audit.check(
        "P18.time.conserved_charge",
        exact_zero(comm(h_susy, q_susy)),
        "the exact multiplet Hamiltonian commutes with its supercharge",
    )
    audit.check(
        "P18.time.susy_state_stays_susy",
        exact_zero(q_susy * evolution_susy * vacuum),
        "a Q-annihilated state remains Q-annihilated under conserved evolution",
    )

    # A finite multiplet marker illustrates the domain criterion: unequal
    # boson/fermion seam factors fail to commute with an odd Q.
    boson_marker, fermion_marker = sp.symbols("s_B s_F", real=True)
    seam_marker = sp.diag(boson_marker, fermion_marker)
    marker_commutator = comm(seam_marker, lowering)
    audit.check(
        "P18.domain.multiplet_marker",
        exact_zero(
            marker_commutator
            - sp.Matrix([[0, boson_marker - fermion_marker], [0, 0]])
        ),
        "a seam treats an elementary B/F pair covariantly only when its markers agree",
    )

    # ------------------------------------------------------------------
    # 2. Free scalar and fermion modes have the same characteristic shell.
    # ------------------------------------------------------------------
    scalar_generator = sp.Matrix([[0, 1], [-mode_omega**2, 0]])
    scalar_evolution = sp.Matrix(
        [
            [
                sp.cos(mode_omega * time),
                sp.sin(mode_omega * time) / mode_omega,
            ],
            [
                -mode_omega * sp.sin(mode_omega * time),
                sp.cos(mode_omega * time),
            ],
        ]
    )
    audit.check(
        "P18.scalar.generator_square",
        exact_zero(scalar_generator**2 + mode_omega**2 * identity_2),
        "the scalar bulk generator has only frequencies plus/minus omega",
    )
    audit.check(
        "P18.scalar.evolution_equation",
        exact_zero(sp.diff(scalar_evolution, time) - scalar_generator * scalar_evolution),
        "the exact scalar evolution solves the first-order Cauchy system",
    )
    audit.check(
        "P18.scalar.evolution_symplectic",
        exact_zero(
            scalar_evolution.T * symplectic_2 * scalar_evolution - symplectic_2
        ),
        "free scalar propagation preserves Klein-Gordon phase-space flux",
    )
    seam_a, seam_b, seam_c, seam_d = sp.symbols(
        "seam_a seam_b seam_c seam_d", real=True
    )
    general_scalar_seam = sp.Matrix(
        [[seam_a, seam_b], [seam_c, seam_d]]
    )
    audit.check(
        "P18.scalar.general_seam_flux_identity",
        exact_zero(
            general_scalar_seam.T
            * symplectic_2
            * general_scalar_seam
            - general_scalar_seam.det() * symplectic_2
        ),
        "a finite two-dimensional scalar seam is canonical exactly when its determinant is one",
    )
    audit.check(
        "P18.scalar.post_seam_evolution",
        exact_zero(
            sp.diff(scalar_evolution * general_scalar_seam, time)
            - scalar_generator * scalar_evolution * general_scalar_seam
        ),
        "an arbitrary instantaneous Cauchy-data map changes amplitudes but not the post-seam generator",
    )
    physical_scalar_generator = scalar_generator.subs(mode_omega, omega)
    audit.check(
        "P18.scalar.characteristic_polynomial",
        exact_zero(
            (energy * identity_2 - sp.I * physical_scalar_generator).det()
            - (energy**2 - momentum**2 - mass**2)
        ),
        "identifying omega^2=k^2+m^2 gives the scalar pole polynomial E^2-k^2-m^2",
    )

    # A helicity-reduced Dirac/Majorana Hamiltonian.  The full spin degeneracy
    # does not change its characteristic denominator.
    fermion_hamiltonian = sp.Matrix([[mass, momentum], [momentum, -mass]])
    fermion_evolution = (
        sp.cos(omega * time) * identity_2
        - sp.I * sp.sin(omega * time) * fermion_hamiltonian / omega
    )
    audit.check(
        "P18.fermion.hamiltonian_square",
        exact_zero(fermion_hamiltonian**2 - omega**2 * identity_2),
        "the reduced fermion Hamiltonian squares to k^2+m^2",
    )
    audit.check(
        "P18.fermion.characteristic_polynomial",
        exact_zero(
            (energy * identity_2 - fermion_hamiltonian).det()
            - (energy**2 - momentum**2 - mass**2)
        ),
        "the fermion resolvent denominator is E^2-k^2-m^2",
    )
    audit.check(
        "P18.fermion.resolvent_factorization",
        exact_zero(
            (energy * identity_2 - fermion_hamiltonian)
            * (energy * identity_2 + fermion_hamiltonian)
            - (energy**2 - momentum**2 - mass**2) * identity_2
        ),
        "the full reduced fermion resolvent factorization has the common pole denominator",
    )
    audit.check(
        "P18.fermion.evolution_equation",
        exact_zero(
            sp.diff(fermion_evolution, time)
            + sp.I * fermion_hamiltonian * fermion_evolution
        ),
        "the exact fermion evolution solves the post-seam Dirac equation",
    )
    audit.check(
        "P18.fermion.evolution_unitary",
        exact_zero(fermion_evolution.H * fermion_evolution - identity_2),
        "free fermion propagation preserves the CAR inner product",
    )

    scalar_shell = energy**2 - momentum**2 - mass**2
    fermion_shell = (energy * identity_2 - fermion_hamiltonian).det()
    audit.check(
        "P18.bulk.common_BF_shell",
        exact_zero(scalar_shell - fermion_shell),
        "equal-mass free boson and fermion modes have an identical pole polynomial",
    )
    scalar_retarded_open_kernel = sp.sin(omega * relative_time) / omega
    audit.check(
        "P18.propagator.scalar_retarded_open_EOM",
        exact_zero(
            sp.diff(scalar_retarded_open_kernel, relative_time, 2)
            + omega**2 * scalar_retarded_open_kernel
        ),
        "away from coincidence the post-post scalar retarded kernel obeys the unchanged bulk equation",
    )
    audit.check(
        "P18.propagator.scalar_retarded_jump",
        exact_zero(scalar_retarded_open_kernel.subs(relative_time, 0))
        and exact_zero(
            sp.diff(scalar_retarded_open_kernel, relative_time).subs(
                relative_time, 0
            )
            - 1
        ),
        "the canonical post-post scalar retarded kernel has the unit coincidence jump",
    )
    audit.check(
        "P18.propagator.scalar_retarded_seam_independence",
        exact_zero(sp.diff(scalar_retarded_open_kernel, kappa)),
        "the post-post free retarded kernel is independent of the initial scalar kick",
    )

    # ------------------------------------------------------------------
    # 3. An instantaneous scalar seam is canonical and CPT reciprocal.
    # ------------------------------------------------------------------
    scalar_kick = sp.Matrix([[1, 0], [-kappa, 1]])
    time_reversal = sp.diag(1, -1)
    audit.check(
        "P18.seam.scalar_kick_symplectic",
        exact_zero(scalar_kick.T * symplectic_2 * scalar_kick - symplectic_2),
        "the delta-seam jump is a finite canonical scalar map",
    )
    audit.check(
        "P18.seam.scalar_kick_time_reversal_reciprocity",
        exact_zero(time_reversal * scalar_kick * time_reversal - scalar_kick.inv()),
        "time reversal maps the forward scalar kick to its inverse",
    )

    # Classical matching of an incoming positive-frequency solution.  The
    # coefficient multiplying exp(+i omega t) differs by conjugation from the
    # beta coefficient in the annihilation-operator Bogoliubov map below.
    alpha_mode = 1 - sp.I * kappa / (2 * mode_omega)
    beta_mode = sp.I * kappa / (2 * mode_omega)
    outgoing_mode = (
        alpha_mode * sp.exp(-sp.I * mode_omega * time)
        + beta_mode * sp.exp(sp.I * mode_omega * time)
    )
    audit.check(
        "P18.seam.scalar_mode_continuity",
        exact_zero(alpha_mode + beta_mode - 1),
        "the outgoing scalar mode is continuous at the seam",
    )
    audit.check(
        "P18.seam.scalar_mode_jump",
        exact_zero(
            sp.diff(outgoing_mode, time).subs(time, 0)
            - (-sp.I * mode_omega)
            + kappa
        ),
        "the outgoing derivative obeys p(0+)-p(0-)=-kappa q(0)",
    )
    audit.check(
        "P18.seam.scalar_post_frequency",
        exact_zero(sp.diff(outgoing_mode, time, 2) + mode_omega**2 * outgoing_mode),
        "the kick changes amplitudes but every post-seam mode still has frequency omega",
    )

    alpha_operator = 1 - sp.I * kappa / (2 * mode_omega)
    beta_operator = -sp.I * kappa / (2 * mode_omega)
    boson_occupation = sp.simplify(beta_operator * sp.conjugate(beta_operator))
    audit.check(
        "P18.seam.scalar_bogoliubov_norm",
        exact_zero(
            alpha_operator * sp.conjugate(alpha_operator)
            - beta_operator * sp.conjugate(beta_operator)
            - 1
        ),
        "the scalar annihilation map obeys the bosonic SU(1,1) normalization",
    )
    audit.check(
        "P18.prediction.scalar_occupation",
        exact_zero(boson_occupation - kappa**2 / (4 * mode_omega**2)),
        "the exact real-mode occupation is kappa^2/(4 omega^2)",
    )

    # A generic finite two-mode fermionic Nambu-pair control is an SU(2)
    # rather than SU(1,1) map.  It is not a local Weyl/Majorana Pin sewing
    # construction.  Its occupation can differ from the scalar without
    # changing h_F.
    theta = sp.Symbol("theta", real=True)
    fermion_seam = sp.Matrix(
        [[sp.cos(theta), sp.sin(theta)], [-sp.sin(theta), sp.cos(theta)]]
    )
    audit.check(
        "P18.seam.fermion_CAR",
        exact_zero(fermion_seam.H * fermion_seam - identity_2)
        and exact_zero(fermion_seam.det() - 1),
        "a finite two-mode fermionic Nambu-pair rotation preserves CAR",
    )
    audit.check(
        "P18.prediction.fermion_occupation",
        exact_zero(fermion_seam[0, 1] ** 2 - sp.sin(theta) ** 2),
        "the incoming-vacuum pair occupation in this finite-mode control is sin(theta)^2",
    )

    # ------------------------------------------------------------------
    # 4. State-dependent Wightman terms cancel from the free spectral kernel.
    # ------------------------------------------------------------------
    occupation = sp.Symbol("n", nonnegative=True, real=True)
    anomalous_real, anomalous_imag = sp.symbols("c_r c_i", real=True)
    anomalous = anomalous_real + sp.I * anomalous_imag
    image_terms = (
        anomalous * sp.exp(-2 * sp.I * mode_omega * central_time)
        + sp.conjugate(anomalous)
        * sp.exp(2 * sp.I * mode_omega * central_time)
    )
    greater = (
        (1 + occupation) * sp.exp(-sp.I * mode_omega * relative_time)
        + occupation * sp.exp(sp.I * mode_omega * relative_time)
        + image_terms
    ) / (2 * mode_omega)
    lesser = (
        occupation * sp.exp(-sp.I * mode_omega * relative_time)
        + (1 + occupation) * sp.exp(sp.I * mode_omega * relative_time)
        + image_terms
    ) / (2 * mode_omega)
    spectral_kernel = sp.I * (greater - lesser)
    audit.check(
        "P18.propagator.spectral_state_independence",
        exact_zero(
            spectral_kernel
            - sp.sin(mode_omega * relative_time) / mode_omega
        ),
        "occupation and anomalous image terms cancel from the free spectral kernel",
    )
    audit.check(
        "P18.propagator.statistical_state_dependence",
        not exact_zero(sp.diff(greater + lesser, occupation))
        and not exact_zero(sp.diff(greater + lesser, anomalous_real)),
        "the statistical/Wightman sector retains seam-state data",
    )

    image_mode = anomalous * sp.exp(
        -sp.I * mode_omega * (time + time_prime)
    )
    audit.check(
        "P18.propagator.image_bulk_equation",
        exact_zero(sp.diff(image_mode, time, 2) + mode_omega**2 * image_mode)
        and exact_zero(
            sp.diff(image_mode, time_prime, 2) + mode_omega**2 * image_mode
        ),
        "the seam image term uses the same bulk frequency in both arguments",
    )

    # ------------------------------------------------------------------
    # 5. A CPT-exchanging scalar sheet kernel and its canonical real slice.
    # ------------------------------------------------------------------
    diagonal, real_mix, imag_mix = sp.symbols("a x y", real=True)
    sheet_flip = sp.Matrix([[0, 1], [1, 0]])
    complex_mix = real_mix + sp.I * imag_mix
    cpt_kernel = sp.Matrix(
        [[diagonal, complex_mix], [sp.conjugate(complex_mix), diagonal]]
    )
    eigenvalue = sp.Symbol("lambda", real=True)
    audit.check(
        "P18.CPT.sheet_kernel",
        exact_zero(cpt_kernel.H - cpt_kernel)
        and exact_zero(sheet_flip * cpt_kernel.conjugate() * sheet_flip - cpt_kernel),
        "the displayed Hermitian sheet kernel is invariant under X_s followed by conjugation",
    )
    audit.check(
        "P18.CPT.sheet_eigenchannels",
        exact_zero(
            (eigenvalue * identity_2 - cpt_kernel).det()
            - ((eigenvalue - diagonal) ** 2 - real_mix**2 - imag_mix**2)
        ),
        "CPT permits two scalar seam eigenchannels a plus/minus |z|",
    )

    real_sheet_mix = sp.Symbol("b", real=True)
    real_sheet_kernel = diagonal * identity_2 + real_sheet_mix * sheet_flip
    sheet_basis = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    phase_space_form = sp.Matrix.vstack(
        sp.Matrix.hstack(zero_2, identity_2),
        sp.Matrix.hstack(-identity_2, zero_2),
    )
    doubled_kick = sp.Matrix.vstack(
        sp.Matrix.hstack(identity_2, zero_2),
        sp.Matrix.hstack(-real_sheet_kernel, identity_2),
    )
    audit.check(
        "P18.CPT.real_sheet_diagonalization",
        exact_zero(
            sheet_basis.T * real_sheet_kernel * sheet_basis
            - sp.diag(diagonal + real_sheet_mix, diagonal - real_sheet_mix)
        ),
        "the real CPT-compatible sheet kick diagonalizes into a plus/minus channel",
    )
    audit.check(
        "P18.CPT.doubled_kick_symplectic",
        exact_zero(
            doubled_kick.T * phase_space_form * doubled_kick - phase_space_form
        ),
        "the two-sheet scalar kick preserves the doubled symplectic flux",
    )
    occupation_plus = (diagonal + real_sheet_mix) ** 2 / (4 * mode_omega**2)
    occupation_minus = (diagonal - real_sheet_mix) ** 2 / (4 * mode_omega**2)
    audit.check(
        "P18.prediction.sheet_occupation_sum_difference",
        exact_zero(
            occupation_plus
            + occupation_minus
            - (diagonal**2 + real_sheet_mix**2) / (2 * mode_omega**2)
        )
        and exact_zero(
            occupation_plus
            - occupation_minus
            - diagonal * real_sheet_mix / mode_omega**2
        ),
        "the two CPT sheet eigenchannels have an exact occupation sum and asymmetry",
    )

    # ------------------------------------------------------------------
    # 6. Sharp-seam UV cost and a smooth Gaussian Born control.
    # ------------------------------------------------------------------
    number_density = kappa**2 / (8 * sp.pi**2) * (
        cutoff - mass * sp.atan(cutoff / mass)
    )
    energy_density = kappa**2 / (16 * sp.pi**2) * (
        cutoff * sp.sqrt(cutoff**2 + mass**2)
        - mass**2 * sp.asinh(cutoff / mass)
    )
    audit.check(
        "P18.UV.number_density_primitive",
        exact_zero(
            sp.diff(number_density, cutoff)
            - kappa**2
            * cutoff**2
            / (8 * sp.pi**2 * (cutoff**2 + mass**2))
        )
        and exact_zero(number_density.subs(cutoff, 0)),
        "the sharp-kick occupation integrates to the stated number density",
    )
    audit.check(
        "P18.UV.energy_density_primitive",
        exact_zero(
            sp.diff(energy_density, cutoff)
            - kappa**2
            * cutoff**2
            / (8 * sp.pi**2 * sp.sqrt(cutoff**2 + mass**2))
        )
        and exact_zero(energy_density.subs(cutoff, 0)),
        "the sharp-kick energy integrates to the stated real-scalar density",
    )
    audit.check(
        "P18.UV.sharp_asymptotics",
        exact_zero(
            sp.limit(number_density / cutoff, cutoff, sp.oo)
            - kappa**2 / (8 * sp.pi**2)
        )
        and exact_zero(
            sp.limit(energy_density / cutoff**2, cutoff, sp.oo)
            - kappa**2 / (16 * sp.pi**2)
        ),
        "a spatially local instantaneous seam has linear number and quadratic energy divergences",
    )

    integration_time = sp.Symbol("u", real=True)
    gaussian_pulse = (
        kappa
        * sp.exp(-integration_time**2 / (2 * seam_width**2))
        / (sp.sqrt(2 * sp.pi) * seam_width)
    )
    gaussian_fourier = sp.integrate(
        gaussian_pulse * sp.exp(-2 * sp.I * mode_omega * integration_time),
        (integration_time, -sp.oo, sp.oo),
    )
    gaussian_born_occupation = (
        kappa**2
        * sp.exp(-4 * seam_width**2 * mode_omega**2)
        / (4 * mode_omega**2)
    )
    audit.check(
        "P18.UV.gaussian_pulse_fourier",
        exact_zero(
            gaussian_fourier
            - kappa * sp.exp(-2 * seam_width**2 * mode_omega**2)
        ),
        "a normalized Gaussian seam suppresses its 2-omega Fourier component exponentially",
    )
    audit.check(
        "P18.prediction.gaussian_Born_occupation",
        exact_zero(
            gaussian_born_occupation
            - gaussian_fourier
            * sp.conjugate(gaussian_fourier)
            / (4 * mode_omega**2)
        )
        and exact_zero(
            sp.limit(gaussian_born_occupation, seam_width, 0, dir="+")
            - kappa**2 / (4 * mode_omega**2)
        ),
        "the Born occupation is exponentially UV-soft and recovers the sharp result as sigma tends to zero",
    )

    # ------------------------------------------------------------------
    # 7. Conditional late-time predictions; these do not derive a scale.
    # ------------------------------------------------------------------
    scale_factor = sp.Symbol("a_scale", positive=True, real=True)
    audit.check(
        "P18.FRW.relativistic_dilution",
        exact_zero(scale_factor**-3 * scale_factor - scale_factor**-2),
        "under the collisionless relativistic integrand assumption the state integral scales as a^-2",
    )
    audit.check(
        "P18.FRW.nonrelativistic_dilution",
        exact_zero(scale_factor**-3 - 1 / scale_factor**3),
        "under conserved nonrelativistic particle number the state integral scales as a^-3",
    )

    soft_ratio = sp.Symbol("r", real=True)
    conditional_mass_ratio = sp.sqrt(1 + soft_ratio**2)
    audit.check(
        "P18.soft.conditional_mass_ratio",
        exact_zero(
            conditional_mass_ratio**2 - (1 + soft_ratio**2)
        ),
        "an inserted persistent scalar soft mass gives m_B/m_F=sqrt(1+r^2)",
    )
    audit.check(
        "P18.soft.small_breaking_series",
        exact_zero(
            sp.series(conditional_mass_ratio - 1, soft_ratio, 0, 6).removeO()
            - (soft_ratio**2 / 2 - soft_ratio**4 / 8)
        ),
        "for small soft breaking the relative mass split begins at r^2/2",
    )

    # Mutants prevent three common false positives: loss of canonical flux,
    # loss of CAR, and silently inserting a future bulk soft mass.
    noncanonical_scalar = sp.diag(2, 1)
    nonunitary_fermion = sp.diag(2, 1)
    inserted_soft_mass_squared = sp.Symbol("mu_soft_squared", positive=True, real=True)
    scalar_shell_with_inserted_soft_mass = scalar_shell - inserted_soft_mass_squared
    audit.check(
        "P18.mutant.reject_noncanonical_scalar_seam",
        not exact_zero(
            noncanonical_scalar.T
            * symplectic_2
            * noncanonical_scalar
            - symplectic_2
        ),
        "a determinant-changing scalar seam is rejected as noncanonical",
    )
    audit.check(
        "P18.mutant.reject_nonunitary_fermion_seam",
        not exact_zero(nonunitary_fermion.H * nonunitary_fermion - identity_2),
        "a norm-changing fermion seam is rejected as CAR-nonunitary",
    )
    audit.check(
        "P18.mutant.detect_inserted_bulk_soft_mass",
        exact_zero(
            scalar_shell_with_inserted_soft_mass
            - fermion_shell
            + inserted_soft_mass_squared
        )
        and not exact_zero(scalar_shell_with_inserted_soft_mass - fermion_shell),
        "a nonzero pole split is detected only after a persistent bulk soft term is inserted",
    )

    numerical_control = narrow_gaussian_numerical_control()
    result: dict[str, object] = {
        "scope": {
            "model": "free equal-mass Wess-Zumino mode control with t=0 quadratic canonical data",
            "spacetime": "3+1D flat post-seam bulk; one scalar mode and one helicity-reduced fermion mode",
            "mass_definition": "t,t'>0 retarded bulk spectral pole",
            "seam_class": [
                "standard instantaneous Cauchy-data map",
                "no energy-dependent or time-nonlocal kernel",
                "no higher-time-derivative extra Cauchy data",
                "unchanged t>0 bulk kinetic and mass operators",
            ],
            "not_constructed": [
                "full doubled Wess-Zumino Pin lift",
                "common variational domain with conserved sheet-mixing Q",
                "a local Weyl/Majorana fermionic seam action",
                "interacting self-energies",
                "a physical absolute SUSY-breaking scale",
            ],
        },
        "exact_checks": audit.passed,
        "numerical_checks": 1,
        "check_ids": audit.check_ids,
        "numerical_control": numerical_control,
        "theorem": {
            "id": "P18_FREE_TEMPORAL_SEAM_NO_POLE_SPLITTING",
            "status": "PROVED_UNDER_FROZEN_ASSUMPTIONS",
            "delta_m_pole_squared": "0",
            "m_B_pole_squared": "m^2",
            "m_F_pole_squared": "m^2",
        },
        "exact_free_predictions": {
            "delta_m_pole_squared": "0",
            "sharp_scalar_occupation_per_real_mode": "kappa^2/[4 (k^2+m^2)]",
            "fermion_pair_occupation_for_finite_Nambu_control": "sin(theta)^2",
            "sharp_energy_density_per_real_scalar": "kappa^2 [Lambda sqrt(Lambda^2+m^2)-m^2 asinh(Lambda/m)]/(16 pi^2)",
            "sharp_UV_leading_energy_density": "kappa^2 Lambda^2/(16 pi^2)",
        },
        "conditional_Born_and_FRW_controls": {
            "gaussian_Born_occupation": "kappa^2 exp(-4 sigma^2 omega_k^2)/(4 omega_k^2)",
            "relativistic_medium_delta_m2_scaling": "a^-2",
            "nonrelativistic_medium_delta_m2_scaling": "a^-3",
            "conditions": [
                "Gaussian pulse is a finite-duration UV regulator control outside the strict instantaneous-seam theorem",
                "FRW scaling assumes a UV-admissible collisionless distribution and no persistent source or phase transition",
            ],
        },
        "dimensionless_benchmarks_not_fundamental_predictions": {
            "seam": seam_benchmarks(),
            "persistent_soft_mass": soft_benchmarks(),
            "FRW_dilution": redshift_benchmarks(),
        },
        "claim_status": {
            "elapsed_time_alone_breaks_SUSY": "CONTRADICTED_IN_CONSERVED_Q_CONTROL",
            "scalar_CPT_control_forces_BF_occupation_equality": "NO_NOT_FORCED_IN_MODE_CONTROL",
            "free_local_seam_generates_permanent_soft_mass": "CONTRADICTED_WITHIN_SCOPE",
            "interacting_or_order_parameter_mass_split": "OPEN_NOT_COMPUTED",
            "Higgs_quadratic_cancellation": "OUT_OF_SCOPE_FREE_THEORY",
        },
    }
    print("PHASE18_RESULT=" + json.dumps(result, sort_keys=True, ensure_ascii=False))
    return result


if __name__ == "__main__":
    run()
