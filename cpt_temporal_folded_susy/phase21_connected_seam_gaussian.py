#!/usr/bin/env python3
"""Phase 21 — normalized connected two-sheet Gaussian seam control.

This executable answers a deliberately bounded question raised after the
Phase 20 WDW-envelope calculation: does normalization canonically identify
the no-seam baseline, and what follows if one then chooses to exclude it?

For a positive Euclidean two-sheet Gaussian it derives three distinct
objects: the normalized partition ratio R, the nonempty bridge remainder
R-1, and the connected vacuum generator log R.  It then checks when their
large-flux tails are summable.  The calculation does not derive the seam
kernel from three-form supergravity and does not promote any determinant to
a Wheeler-DeWitt/Born probability.  The program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import mpmath as mp
import sympy as sp


@dataclass
class Audit:
    exact_passed: int = 0
    numerical_passed: int = 0
    exact_ids: list[str] = field(default_factory=list)
    numerical_ids: list[str] = field(default_factory=list)
    exact_records: list[dict[str, str]] = field(default_factory=list)
    numerical_records: list[dict[str, str]] = field(default_factory=list)

    def exact(self, check_id: str, condition: bool, statement: str) -> None:
        self._check_unique(check_id)
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.exact_passed += 1
        self.exact_ids.append(check_id)
        self.exact_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[PASS] {check_id}: {statement}")

    def numerical(self, check_id: str, condition: bool, statement: str) -> None:
        self._check_unique(check_id)
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {statement}")
        self.numerical_passed += 1
        self.numerical_ids.append(check_id)
        self.numerical_records.append(
            {"id": check_id, "status": "PASS", "statement": statement}
        )
        print(f"[NUMERIC PASS] {check_id}: {statement}")

    def _check_unique(self, check_id: str) -> None:
        if check_id in self.exact_ids or check_id in self.numerical_ids:
            raise AssertionError(f"[FAIL] duplicate check id: {check_id}")


def exact_zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.factor(expression)) == 0


def single_mode_controls(audit: Audit) -> dict[str, object]:
    a_plus, a_minus = sp.symbols("A_plus A_minus", positive=True, real=True)
    coupling = sp.symbols("C", real=True)
    rho = sp.symbols("rho", real=True)
    kernel = sp.Matrix([[a_plus, -coupling], [-coupling, a_minus]])
    determinant = sp.factor(kernel.det())
    inverse = sp.simplify(kernel.inv())
    schur_minus = sp.factor(a_minus - coupling**2 / a_plus)

    audit.exact(
        "P21.gaussian.kernel_determinant",
        exact_zero(determinant - (a_plus * a_minus - coupling**2)),
        "det M=A_plus A_minus-C^2",
    )
    audit.exact(
        "P21.gaussian.schur_factorization",
        exact_zero(determinant - a_plus * schur_minus),
        "the determinant equals A_plus times the minus-sheet Schur complement",
    )
    audit.exact(
        "P21.gaussian.inverse_covariance",
        inverse
        == sp.Matrix(
            [
                [a_minus, coupling],
                [coupling, a_plus],
            ]
        )
        / determinant,
        "the exact covariance has cross entry C/(A_plus A_minus-C^2)",
    )

    ratio_squared = sp.factor(a_plus * a_minus / determinant)
    ratio_rho = 1 / sp.sqrt(1 - rho**2)
    audit.exact(
        "P21.gaussian.normalized_ratio",
        exact_zero(
            ratio_squared.subs(coupling, rho * sp.sqrt(a_plus * a_minus))
            - ratio_rho**2
        ),
        "[Z(C)/(Z_plus Z_minus)]^2=1/(1-rho^2)",
    )
    audit.exact(
        "P21.gaussian.no_seam_baseline",
        sp.simplify(ratio_rho.subs(rho, 0)) == 1,
        "the normalized ratio is exactly one when the cross-sheet coupling vanishes",
    )

    connected_remainder = ratio_rho - 1
    connected_generator = -sp.log(1 - rho**2) / 2
    ratio_series = sp.series(connected_remainder, rho, 0, 8).removeO()
    log_series = sp.series(connected_generator, rho, 0, 8).removeO()
    audit.exact(
        "P21.gaussian.nonempty_bridge_series",
        exact_zero(
            ratio_series
            - (
                rho**2 / 2
                + 3 * rho**4 / 8
                + 5 * rho**6 / 16
            )
        ),
        "R-1=rho^2/2+3rho^4/8+5rho^6/16+O(rho^8)",
    )
    audit.exact(
        "P21.gaussian.connected_log_series",
        exact_zero(
            log_series - (rho**2 / 2 + rho**4 / 4 + rho**6 / 6)
        ),
        "log R=rho^2/2+rho^4/4+rho^6/6+O(rho^8)",
    )
    audit.exact(
        "P21.gaussian.remainder_is_exponential_of_connected",
        exact_zero(connected_remainder - (sp.exp(connected_generator) - 1)),
        "R-1=exp(log R)-1, so it includes products of connected vacuum rings",
    )
    audit.exact(
        "P21.gaussian.order_four_disconnected_piece",
        exact_zero(sp.Rational(3, 8) - (sp.Rational(1, 4) + sp.Rational(1, 8))),
        "the rho^4 coefficient 3/8 contains a connected 1/4 plus a disconnected 1/8",
    )

    cross_covariance = coupling / determinant
    derivative_log_ratio = sp.diff(
        -sp.log(1 - coupling**2 / (a_plus * a_minus)) / 2,
        coupling,
    )
    audit.exact(
        "P21.gaussian.source_derivative_correlation",
        exact_zero(derivative_log_ratio - cross_covariance),
        "d log R/dC equals the connected cross-sheet two-point function",
    )
    audit.exact(
        "P21.gaussian.ratio_even_correlation_odd",
        sp.simplify(ratio_squared.subs(coupling, -coupling) - ratio_squared) == 0
        and sp.simplify(
            cross_covariance.subs(coupling, -coupling) + cross_covariance
        )
        == 0,
        "the determinant ratio forgets the sign of C while the cross correlation retains it",
    )

    scale = sp.symbols("A", positive=True, real=True)
    symmetric_kernel = kernel.subs({a_plus: scale, a_minus: scale})
    eigenvalues = sorted(
        [sp.factor(value) for value in symmetric_kernel.eigenvals()],
        key=str,
    )
    audit.exact(
        "P21.gaussian.symmetric_normal_modes",
        set(eigenvalues) == {scale - coupling, scale + coupling},
        "the symmetric-sheet normal-mode eigenvalues are A-C and A+C",
    )

    return {
        "euclidean_action": (
            "S_E=(A_plus x_plus^2+A_minus x_minus^2)/2-C x_plus x_minus"
        ),
        "stability_domain": "A_plus>0, A_minus>0, C^2<A_plus A_minus",
        "normalized_partition_ratio": "R=(1-rho^2)^(-1/2)",
        "whitened_coupling": "rho=C/sqrt(A_plus A_minus)",
        "zero_bridge_removed_remainder": "R-1",
        "connected_vacuum_generator": "W_cross=log R=-log(1-rho^2)/2",
        "cross_sheet_covariance": "C/(A_plus A_minus-C^2)",
        "interpretation": (
            "R-1 removes the zero-bridge term but is not itself the connected "
            "vacuum functional; log R is the connected vacuum sum."
        ),
    }


def multimode_controls(audit: Audit) -> dict[str, object]:
    a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", positive=True, real=True)
    c1, c2 = sp.symbols("c1 c2", real=True)
    r1, r2, t = sp.symbols("r1 r2 t", real=True)
    a_plus = sp.diag(a1, a2)
    a_minus = sp.diag(b1, b2)
    cross = sp.diag(c1, c2)
    block = a_plus.row_join(-cross).col_join((-cross.T).row_join(a_minus))
    schur = a_minus - cross.T * a_plus.inv() * cross

    audit.exact(
        "P21.multimode.schur_determinant",
        exact_zero(block.det() - a_plus.det() * schur.det()),
        "the two-mode block determinant obeys the Schur-complement identity",
    )
    ratio_squared = sp.factor(a_plus.det() * a_minus.det() / block.det())
    ratio_squared_target = sp.factor(
        1
        / (
            (1 - c1**2 / (a1 * b1))
            * (1 - c2**2 / (a2 * b2))
        )
    )
    audit.exact(
        "P21.multimode.determinant_ratio",
        exact_zero(ratio_squared - ratio_squared_target),
        "the normalized two-mode ratio factors over whitened singular values",
    )

    log_ratio_scaled = -sp.log(1 - t**2 * r1**2) / 2 - sp.log(
        1 - t**2 * r2**2
    ) / 2
    trace_series = sp.series(log_ratio_scaled, t, 0, 6).removeO()
    audit.exact(
        "P21.multimode.connected_trace_expansion",
        exact_zero(
            trace_series
            - t**2 * (r1**2 + r2**2) / 2
            - t**4 * (r1**4 + r2**4) / 4
        ),
        "log R=Tr(K^T K)/2+Tr[(K^T K)^2]/4+... for two diagonal modes",
    )

    whitened_block = sp.Matrix(
        [
            [1, 0, -r1, 0],
            [0, 1, 0, -r2],
            [-r1, 0, 1, 0],
            [0, -r2, 0, 1],
        ]
    )
    expected_characteristic = sp.expand(
        (t - (1 - r1))
        * (t - (1 + r1))
        * (t - (1 - r2))
        * (t - (1 + r2))
    )
    audit.exact(
        "P21.multimode.positivity_singular_value_gate",
        exact_zero(
            (t * sp.eye(4) - whitened_block).det()
            - expected_characteristic
        ),
        "positive convergence requires every whitened singular value to be below one",
    )

    return {
        "block_kernel": "M=[[A_plus,-C],[-C^T,A_minus]]",
        "whitened_kernel": "K=A_plus^(-1/2) C A_minus^(-1/2)",
        "normalized_ratio": "det(I-K^T K)^(-1/2)",
        "connected_generator": (
            "log R=(1/2) sum_{j>=1} Tr[(K^T K)^j]/j"
        ),
        "finite_mode_stability": "largest singular value of K is below one",
        "infinite_mode_unregularized_gate": (
            "K must at least be Hilbert-Schmidt: sum_j singular_value_j^2<infinity"
        ),
    }


def flux_tail_controls(audit: Audit) -> dict[str, object]:
    n = sp.symbols("n", positive=True, integer=True)
    a0, charge, kappa = sp.symbols("a0 q kappa", positive=True, real=True)
    eta = sp.symbols("eta", positive=True, real=True)
    gamma = sp.symbols("gamma", positive=True, real=True)
    dimension = sp.symbols("d", real=True)
    stiffness = a0 + charge**2 * n**2
    rho_squared = kappa**2 / stiffness**2
    remainder = 1 / sp.sqrt(1 - rho_squared) - 1
    connected_generator = -sp.log(1 - rho_squared) / 2
    decoupled_partition = 2 * sp.pi / stiffness
    unnormalized_difference = decoupled_partition * remainder

    audit.exact(
        "P21.flux.absolute_coupling_remainder_tail",
        exact_zero(
            sp.limit(n**4 * remainder, n, sp.oo)
            - kappa**2 / (2 * charge**4)
        ),
        "for A_n=a0+q^2 n^2 and constant C=kappa, R_n-1 is asymptotic to kappa^2/(2q^4 n^4)",
    )
    audit.exact(
        "P21.flux.absolute_coupling_log_tail",
        exact_zero(
            sp.limit(n**4 * connected_generator, n, sp.oo)
            - kappa**2 / (2 * charge**4)
        ),
        "the connected generator has the same leading n^-4 tail",
    )
    audit.exact(
        "P21.flux.sector_partition_difference_tail",
        exact_zero(
            sp.limit(n**6 * unnormalized_difference, n, sp.oo)
            - sp.pi * kappa**2 / charge**6
        ),
        "the actual one-mode sector difference Z_n(C)-Z_n(0)=Z_n(0)(R_n-1) has an n^-6 tail",
    )

    relative_remainder = 1 / sp.sqrt(1 - eta**2) - 1
    audit.exact(
        "P21.flux.relative_coupling_constant_tail",
        exact_zero(
            sp.limit(
                1
                / sp.sqrt(1 - (eta * stiffness) ** 2 / stiffness**2)
                - 1,
                n,
                sp.oo,
            )
            - relative_remainder
        ),
        "if C_n=eta A_n, the zero-bridge remainder approaches a nonzero constant",
    )

    # Shell degeneracy in d flux dimensions scales as r^(d-1).  The
    # convergence threshold therefore depends on which sector weight is used.
    audit.exact(
        "P21.flux.normalized_ratio_lattice_dimension_threshold",
        sp.solve_univariate_inequality(
            dimension - 1 - 4 < -1, dimension
        )
        == (dimension < 4),
        "the n^-4 tails of R_n-1 and log R_n are summable on Z^d only for d<4",
    )
    audit.exact(
        "P21.flux.sector_difference_lattice_dimension_threshold",
        sp.solve_univariate_inequality(
            dimension - 1 - 6 < -1, dimension
        )
        == (dimension < 6),
        "the n^-6 tail of Z_n(C)-Z_n(0) is summable on Z^d only for d<6",
    )
    audit.exact(
        "P21.flux.relative_sector_difference_dimension_threshold",
        sp.solve_univariate_inequality(
            dimension - 1 - 2 < -1, dimension
        )
        == (dimension < 2),
        "for C_n=eta A_n the n^-2 sector-difference tail is summable only for d<2",
    )

    wdw_argument = gamma / (charge**2 * n**2)
    hh_excess = sp.exp(wdw_argument) - 1
    tunneling_deficit = 1 - sp.exp(-wdw_argument)
    audit.exact(
        "P21.flux.WDW_HH_excess_tail",
        exact_zero(
            sp.limit(n**2 * hh_excess, n, sp.oo) - gamma / charge**2
        ),
        "the positive HH excess exp(gamma/V_n)-1 has an n^-2 tail when V_n grows as n^2",
    )
    audit.exact(
        "P21.flux.WDW_tunneling_deficit_tail",
        exact_zero(
            sp.limit(n**2 * tunneling_deficit, n, sp.oo)
            - gamma / charge**2
        ),
        "the positive tunneling deficit 1-exp(-gamma/V_n) has the same n^-2 tail",
    )
    audit.exact(
        "P21.flux.WDW_reference_lattice_dimension_threshold",
        sp.solve_univariate_inequality(
            dimension - 1 - 2 < -1, dimension
        )
        == (dimension < 2),
        "an n^-2 WDW reference-difference tail is summable on Z^d only for d<2",
    )

    regulator = sp.symbols("epsilon", positive=True, real=True)
    abel_constant_sum = sp.coth(regulator / 2)
    abel_series = sp.series(abel_constant_sum, regulator, 0, 4).removeO()
    audit.exact(
        "P21.regularization.constant_tail_finite_part",
        exact_zero(
            abel_series
            - (2 / regulator + regulator / 6 - regulator**3 / 360)
        ),
        "the Abel-regulated two-sided constant sum has divergence 2/epsilon and zero constant finite part",
    )

    return {
        "toy_flux_stiffness": "A_n=a0+q^2 n^2",
        "constant_absolute_coupling": {
            "C_n": "kappa",
            "R_n_minus_1_tail": "kappa^2/(2 q^4 n^4)",
            "single_flux_sum": "CONVERGENT_IF_kappa<a0",
            "R_minus_1_and_log_R_flux_lattice": "CONVERGENT_ONLY_FOR_d<4",
            "unnormalized_sector_difference_tail": "pi kappa^2/(q^6 n^6)",
            "unnormalized_sector_difference_flux_lattice": (
                "CONVERGENT_ONLY_FOR_d<6"
            ),
        },
        "constant_relative_coupling": {
            "C_n": "eta A_n",
            "R_n_minus_1_tail": "(1-eta^2)^(-1/2)-1",
            "R_minus_1_flux_lattice": "DIVERGENT_FOR_ALL_d>=1",
            "unnormalized_sector_difference_tail": "proportional to n^-2",
            "unnormalized_sector_difference_flux_lattice": (
                "CONVERGENT_ONLY_FOR_d<2"
            ),
        },
        "WDW_reference_subtractions": {
            "HH_positive_excess": "exp(gamma/V_n)-1",
            "tunneling_positive_deficit": "1-exp(-gamma/V_n)",
            "tail_for_V_n_proportional_to_n_squared": "n^-2",
            "flux_lattice": "CONVERGENT_ONLY_FOR_d<2",
            "warning": (
                "These weights are not derived by the Gaussian determinant; "
                "the comparison only exposes the asymptotic effect of a reference subtraction."
            ),
        },
        "regularization_warning": (
            "Assigning a finite part to the constant tail does not create a "
            "countably additive positive probability measure."
        ),
    }


def numerical_flux_control(audit: Audit) -> dict[str, object]:
    mp.mp.dps = 60
    a0 = mp.mpf(2)
    charge = mp.mpf(1)
    kappa = mp.mpf(1)

    def stiffness(index: int | mp.mpf) -> mp.mpf:
        return a0 + charge**2 * index**2

    def remainder(index: int | mp.mpf) -> mp.mpf:
        rho = kappa / stiffness(index)
        return 1 / mp.sqrt(1 - rho**2) - 1

    def connected(index: int | mp.mpf) -> mp.mpf:
        rho = kappa / stiffness(index)
        return -mp.log(1 - rho**2) / 2

    def sector_difference(index: int | mp.mpf) -> mp.mpf:
        decoupled_partition = 2 * mp.pi / stiffness(index)
        return decoupled_partition * remainder(index)

    total_remainder = remainder(0) + 2 * mp.nsum(
        lambda index: remainder(index), [1, mp.inf]
    )
    total_connected = connected(0) + 2 * mp.nsum(
        lambda index: connected(index), [1, mp.inf]
    )
    partial_10 = mp.fsum(remainder(index) for index in range(-10, 11))
    partial_100 = mp.fsum(remainder(index) for index in range(-100, 101))
    partial_1000 = mp.fsum(remainder(index) for index in range(-1000, 1001))
    flat_remainder_p0 = remainder(0) / total_remainder
    total_sector_difference = sector_difference(0) + 2 * mp.nsum(
        lambda index: sector_difference(index), [1, mp.inf]
    )
    flat_sector_difference_p0 = sector_difference(0) / total_sector_difference

    audit.numerical(
        "P21.numeric.absolute_coupling_sum",
        abs(total_remainder - mp.mpf("0.319002816952369856065634397246"))
        < mp.mpf("1e-30"),
        "the toy single-flux zero-bridge remainder sums to 0.319002816952369856...",
    )
    audit.numerical(
        "P21.numeric.connected_generator_sum",
        abs(total_connected - mp.mpf("0.304386389797735255006234666282"))
        < mp.mpf("1e-30"),
        "the toy single-flux connected generator sums to 0.304386389797735255...",
    )
    audit.numerical(
        "P21.numeric.truncation_convergence",
        abs(partial_10 - total_remainder) < mp.mpf("3e-4")
        and abs(partial_100 - total_remainder) < mp.mpf("4e-7")
        and abs(partial_1000 - total_remainder) < mp.mpf("4e-10"),
        "N=10,100,1000 symmetric cutoffs converge with the n^-4 tail",
    )
    audit.numerical(
        "P21.numeric.flat_remainder_zero_sector_peak",
        abs(flat_remainder_p0 - mp.mpf("0.48495038337655114054854403353"))
        < mp.mpf("1e-29")
        and all(remainder(0) > remainder(index) for index in range(1, 20)),
        "under an imposed flat sector measure, normalized positive R_n-1 toy weights peak at n=0 with p0=0.484950...",
    )
    audit.numerical(
        "P21.numeric.sector_partition_difference_sum",
        abs(
            total_sector_difference
            - mp.mpf("0.776167636301807464652496010855")
        )
        < mp.mpf("1e-30"),
        "including the n-dependent decoupled partition gives sum_n[Z_n(C)-Z_n(0)]=0.776167636301807...",
    )
    audit.numerical(
        "P21.numeric.sector_partition_prior_dependence",
        abs(
            flat_sector_difference_p0
            - mp.mpf("0.626161221040221692700998785334")
        )
        < mp.mpf("1e-30")
        and abs(flat_sector_difference_p0 - flat_remainder_p0) > mp.mpf("0.1"),
        "retaining Z_n(0) changes the normalized positive toy n=0 weight from 0.484950... to 0.626161...",
    )

    eta = mp.mpf("0.5")
    constant_remainder = 1 / mp.sqrt(1 - eta**2) - 1
    relative_100 = (2 * 100 + 1) * constant_remainder
    relative_200 = (2 * 200 + 1) * constant_remainder
    audit.numerical(
        "P21.numeric.relative_coupling_linear_divergence",
        abs(relative_200 / relative_100 - mp.mpf(401) / 201)
        < mp.mpf("1e-50"),
        "a constant relative coupling makes the symmetric cutoff sum grow exactly with 2N+1",
    )

    return {
        "parameters": {"a0": "2", "q": "1", "kappa": "1"},
        "stability_margin": "min_n(A_n-|C_n|)=1",
        "sum_over_integer_flux_R_minus_1": mp.nstr(total_remainder, 32),
        "sum_over_integer_flux_log_R": mp.nstr(total_connected, 32),
        "flat_measure_p_n0_from_R_minus_1": mp.nstr(flat_remainder_p0, 32),
        "sum_over_integer_flux_ZC_minus_Z0": mp.nstr(
            total_sector_difference, 32
        ),
        "flat_measure_p_n0_from_ZC_minus_Z0": mp.nstr(
            flat_sector_difference_p0, 32
        ),
        "symmetric_partial_sums": {
            "N=10": mp.nstr(partial_10, 32),
            "N=100": mp.nstr(partial_100, 32),
            "N=1000": mp.nstr(partial_1000, 32),
        },
        "interpretation": (
            "p_n proportional to R_n-1 is only a normalized positive toy "
            "weighting under an imposed flat sector measure; no exclusive event "
            "projector or decoherence functional is constructed. The actual "
            "sector difference carries an additional Z_n(0)."
        ),
    }


def run() -> dict[str, object]:
    audit = Audit()
    single_mode = single_mode_controls(audit)
    multimode = multimode_controls(audit)
    flux_tail = flux_tail_controls(audit)
    numerical = numerical_flux_control(audit)

    result: dict[str, object] = {
        "phase": "P21",
        "calculation": "normalized connected two-sheet Gaussian seam control",
        "exact_checks": audit.exact_passed,
        "numerical_checks": audit.numerical_passed,
        "exact_check_ids": audit.exact_ids,
        "numerical_check_ids": audit.numerical_ids,
        "exact_check_records": audit.exact_records,
        "numerical_check_records": audit.numerical_records,
        "single_mode": single_mode,
        "multimode": multimode,
        "flux_tail": flux_tail,
        "numerical_toy": numerical,
        "claim_status": {
            "normalization_identifies_the_zero_seam_baseline_as_one": (
                "SUPPORTED"
            ),
            "normalization_forces_zero_bridge_subtraction": (
                "CONTRADICTED_NOT_FORCED"
            ),
            "chosen_zero_bridge_exclusion_equals_R_minus_1": (
                "SUPPORTED_CONDITIONALLY"
            ),
            "R_minus_1_is_the_connected_vacuum_functional": "CONTRADICTED",
            "log_R_is_the_connected_vacuum_generator": "SUPPORTED",
            "subtraction_alone_guarantees_flux_normalizability": "CONTRADICTED",
            "constant_absolute_kernel_with_A_n_growing_as_n_squared_is_summable": (
                "SUPPORTED_IN_SINGLE_FLUX_TOY"
            ),
            "connected_Gaussian_ratio_is_a_physical_WDW_flux_probability": (
                "OPEN_NOT_DERIVED"
            ),
            "R_minus_1_alone_is_the_unnormalized_flux_sector_weight": (
                "CONTRADICTED_WITHOUT_A_FLAT_NORMALIZED_SECTOR_PRIOR"
            ),
            "three_form_CPT_seam_selects_an_inflationary_flux_sector": (
                "OPEN_NOT_COMPUTED"
            ),
        },
        "scope_guard": {
            "what_is_computed": [
                "one positive Euclidean real-boson two-sheet Gaussian",
                "finite-mode Schur determinant and connected trace expansion",
                "single-flux asymptotics for two explicit kernel scalings",
                "a bounded numerical sum for A_n=2+n^2 and C_n=1",
                "the distinction among R, R-1, and log R",
                "the distinction between R_n-1 and Z_n(0)(R_n-1)",
            ],
            "what_is_not_computed": [
                "a three-form supergravity derivation of A_n or C_n",
                "a membrane transition amplitude or flux master equation",
                "oriented n-to-n-plus-or-minus-one transitions or their rates",
                "a Wheeler-DeWitt solution, current, inner product, or Born measure",
                "a Lorentzian contour or Osterwalder-Schrader reflection-positive field theory",
                "scalar, tensor, chiralino, gravitino, or ghost functional determinants",
                "a normalizable distribution over both flux n and inflaton phi",
                "an inflationary initial value, e-fold count, or observable prediction",
            ],
            "central_interpretation": (
                "normalized path-integral division makes the no-cross-sheet term "
                "exactly one.  Choosing to exclude that term gives R-1, but the "
                "subtraction is not forced by normalization.  The linked-cluster "
                "object is log R, and neither expression is a universe probability "
                "without a sector measure, state prescription, and decoherence/inner product. "
                "Across flux sectors, dropping Z_n(0) is itself a prior convention."
            ),
        },
        "next_calculation": {
            "target": (
                "derive the actual flux- and harmonic-dependent cross-sheet kernel "
                "from a three-form SUGRA boundary state or membrane action"
            ),
            "minimum_gates": [
                "positive/stable Euclidean kernel or a specified Lorentzian contour",
                "UV Hilbert-Schmidt or renormalized determinant control",
                "a physical flux-sector measure and decoherence functional",
                "a finite joint distribution in n and phi with an interior peak",
            ],
        },
    }
    print("PHASE21_RESULT=" + json.dumps(result, sort_keys=True))
    return result


if __name__ == "__main__":
    run()
