#!/usr/bin/env python3
"""Phase 17 — exact algebra for a real-line time fold without a scalar clock.

The program keeps four logically distinct structures separate:

1. a standard local 4D N=1 positive-energy fiber;
2. a linear pullback that exchanges the two open time half-lines;
3. a fundamental doubled-sheet theory with an off-diagonal supercharge; and
4. Schwinger-Keldysh BRST supersymmetry on a doubled real-time contour.

No rolling scalar, cosmological clock, research contract, or result file is
used.  All checks use exact SymPy matrices and the program writes no files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import sympy as sp


@dataclass
class Audit:
    passed: int = 0

    def check(self, check_id: str, condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(f"[FAIL] {check_id}: {message}")
        self.passed += 1
        print(f"[PASS] {check_id}: {message}")


def exact_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(sp.trigsimp(sp.simplify(entry)) == 0 for entry in value)
    return sp.trigsimp(sp.simplify(value)) == 0


def anti(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left * right + right * left)


def comm(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left * right - right * left)


def standard_closure(
    charges: list[sp.Matrix], energy: sp.Symbol, branch_dimension: int
) -> bool:
    dimension = 4 * branch_dimension
    for alpha, q_alpha in enumerate(charges):
        if not exact_zero(q_alpha * q_alpha):
            return False
        for beta, q_beta in enumerate(charges):
            if not exact_zero(anti(q_alpha, q_beta)):
                return False
            target = (
                2 * energy * sp.eye(dimension)
                if alpha == beta
                else sp.zeros(dimension)
            )
            if not exact_zero(anti(q_alpha, q_beta.H) - target):
                return False
    return True


def run() -> dict[str, object]:
    audit = Audit()
    energy = sp.Symbol("E", positive=True, real=True)
    theta = sp.Symbol("theta", real=True)
    phase = sp.Symbol("phi", real=True)

    identity_2 = sp.eye(2)
    branch_sign = sp.diag(-1, 1)
    branch_flip = sp.Matrix([[0, 1], [1, 0]])
    projector_minus = sp.diag(1, 0)
    projector_plus = sp.diag(0, 1)

    audit.check(
        "P17.branch_reflection",
        exact_zero(branch_flip**2 - identity_2)
        and exact_zero(branch_flip.H * branch_flip - identity_2)
        and exact_zero(branch_flip * branch_sign * branch_flip + branch_sign),
        "the linear fold is a unitary involution that exchanges the two half-line labels",
    )
    audit.check(
        "P17.branch_projectors",
        exact_zero(branch_flip * projector_plus - projector_minus * branch_flip)
        and exact_zero(branch_flip * projector_minus - projector_plus * branch_flip),
        "the fold swaps the negative- and positive-half projectors",
    )

    # Minimal generic massive/rest-frame 4D N=1 fiber: two CAR modes.
    lowering = sp.Matrix([[0, 1], [0, 0]])
    fermion_parity_1 = sp.diag(1, -1)
    a_1 = sp.kronecker_product(lowering, identity_2)
    a_2 = sp.kronecker_product(fermion_parity_1, lowering)
    fermion_parity = sp.kronecker_product(
        fermion_parity_1, fermion_parity_1
    )
    q_fiber = [sp.sqrt(2 * energy) * a_1, sp.sqrt(2 * energy) * a_2]

    audit.check(
        "P17.N1_CAR",
        standard_closure(q_fiber, energy, 1),
        "two exact CAR modes realize the positive-energy 4D N=1 rest-frame algebra",
    )
    audit.check(
        "P17.N1_fermion_parity",
        all(exact_zero(anti(fermion_parity, charge)) for charge in q_fiber),
        "both Weyl supercharge components are odd under physical fermion parity",
    )

    full_projector_minus = sp.kronecker_product(projector_minus, sp.eye(4))
    full_projector_plus = sp.kronecker_product(projector_plus, sp.eye(4))
    physical_parity = sp.kronecker_product(identity_2, fermion_parity)
    sheet_sign = sp.kronecker_product(branch_sign, sp.eye(4))

    local_charges = [
        sp.kronecker_product(identity_2, charge) for charge in q_fiber
    ]
    audit.check(
        "P17.local_standard_closure",
        standard_closure(local_charges, energy, 2),
        "the same-t local charge retains the standard algebra on both halves",
    )
    audit.check(
        "P17.local_same_half",
        all(
            exact_zero(full_projector_minus * charge * full_projector_plus)
            and exact_zero(full_projector_plus * charge * full_projector_minus)
            for charge in local_charges
        ),
        "a support-local charge has exactly zero open-half cross blocks",
    )

    fold_charges = [
        sp.kronecker_product(branch_flip, charge) for charge in q_fiber
    ]
    audit.check(
        "P17.fold_fixed_fiber_closure",
        standard_closure(fold_charges, energy, 2),
        "the bidirectional sheet flip preserves the fixed-positive-energy N=1 algebra",
    )
    audit.check(
        "P17.fold_physical_parity",
        all(exact_zero(anti(physical_parity, charge)) for charge in fold_charges),
        "the folded charge remains odd under physical fermion parity",
    )
    fold_cross_ranks = [
        (
            (full_projector_minus * charge * full_projector_plus).rank(),
            (full_projector_plus * charge * full_projector_minus).rank(),
        )
        for charge in fold_charges
    ]
    audit.check(
        "P17.fold_bidirectional_exchange",
        fold_cross_ranks == [(2, 2), (2, 2)]
        and all(exact_zero(anti(sheet_sign, charge)) for charge in fold_charges),
        "each folded Weyl charge has nonzero rank-two cross blocks in both directions",
    )

    bad_combined_parity = sp.kronecker_product(branch_sign, fermion_parity)
    audit.check(
        "P17.half_sign_is_not_fermion_parity",
        all(exact_zero(comm(bad_combined_parity, charge)) for charge in fold_charges)
        and any(
            not exact_zero(anti(bad_combined_parity, charge))
            for charge in fold_charges
        ),
        "multiplying fermion parity by time-half sign makes the folded charge even and is rejected",
    )

    # Closure permits a continuous family; it does not dynamically select a fold.
    mixing = sp.cos(theta) * identity_2 + sp.I * sp.sin(theta) * branch_flip
    mixed_charges = [sp.kronecker_product(mixing, charge) for charge in q_fiber]
    audit.check(
        "P17.unitary_mixing_family",
        exact_zero(mixing.H * mixing - identity_2)
        and standard_closure(mixed_charges, energy, 2),
        "a continuous unitary local/fold interpolation preserves the algebra for every real theta",
    )
    cross_weight = sp.trigsimp(
        (projector_minus * mixing * projector_plus).H
        * (projector_minus * mixing * projector_plus)
    )
    audit.check(
        "P17.mixing_not_selected",
        exact_zero(cross_weight - sp.diag(0, sp.sin(theta) ** 2)),
        "the branch-exchange weight is sin(theta)^2, so closure alone does not select it",
    )

    phased_flip = sp.Matrix(
        [[0, sp.exp(sp.I * phase)], [sp.exp(-sp.I * phase), 0]]
    )
    branch_rephase = sp.diag(
        sp.exp(-sp.I * phase / 2), sp.exp(sp.I * phase / 2)
    )
    audit.check(
        "P17.exchange_phase_family",
        exact_zero(phased_flip.H * phased_flip - identity_2)
        and exact_zero(phased_flip**2 - identity_2)
        and exact_zero(branch_rephase * phased_flip * branch_rephase.H - branch_flip),
        "the pure-exchange phase is removable by an unanchored branch rephasing",
    )

    even_projector = (sp.eye(4) + fermion_parity) / 2
    odd_projector = (sp.eye(4) - fermion_parity) / 2
    controlled_sheet_change = sp.kronecker_product(
        identity_2, even_projector
    ) + sp.kronecker_product(branch_flip, odd_projector)
    audit.check(
        "P17.local_fold_basis_equivalence",
        exact_zero(controlled_sheet_change.H * controlled_sheet_change - sp.eye(8))
        and all(
            exact_zero(
                controlled_sheet_change
                * local
                * controlled_sheet_change.H
                - folded
            )
            for local, folded in zip(local_charges, fold_charges, strict=True)
        ),
        "without a physical sheet anchor, local and exchange charges are related by a parity-controlled basis change",
    )

    one_way = sp.Matrix([[0, 0], [1, 0]])
    one_way_charges = [sp.kronecker_product(one_way, charge) for charge in q_fiber]
    audit.check(
        "P17.one_way_cross",
        all(
            (full_projector_plus * charge * full_projector_minus).rank() == 2
            and exact_zero(full_projector_minus * charge * full_projector_plus)
            for charge in one_way_charges
        ),
        "a one-way arrow can be inserted algebraically",
    )
    audit.check(
        "P17.one_way_closure_rejected",
        not standard_closure(one_way_charges, energy, 2),
        "the one-way arrow fails the standard N=1 adjoint closure",
    )
    nonunitary = sp.diag(1, 2)
    audit.check(
        "P17.nonunitary_branch_mutation",
        not standard_closure(
            [sp.kronecker_product(nonunitary, charge) for charge in q_fiber],
            energy,
            2,
        ),
        "a nonunitary branch factor cannot preserve the standard closure",
    )

    # A symmetric finite support control makes the locality/translation issue exact.
    time_reflection = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    derivative = sp.Matrix([[0, 1, 0], [-1, 0, 1], [0, -1, 0]])
    time_momentum = -sp.I * derivative
    time_sign = sp.diag(-1, 0, 1)
    audit.check(
        "P17.reflection_reverses_time_momentum",
        exact_zero(time_reflection * time_momentum * time_reflection + time_momentum),
        "the time pullback reverses the signed translation generator",
    )
    reflected_grid_charge = sp.kronecker_product(time_reflection, q_fiber[0])
    grid_momentum = sp.kronecker_product(time_momentum, sp.eye(4))
    audit.check(
        "P17.reflection_translation_obstruction",
        exact_zero(anti(grid_momentum, reflected_grid_charge))
        and not exact_zero(comm(grid_momentum, reflected_grid_charge)),
        "the reflection-composed charge anticommutes rather than commutes with signed time translation",
    )
    audit.check(
        "P17.sharp_half_not_translation_invariant",
        not exact_zero(comm(time_momentum, time_sign)),
        "the sharp sign-of-coordinate split is not invariant under time translation at the seam",
    )
    audit.check(
        "P17.signed_time_generator_not_positive_closure",
        set(time_momentum.eigenvals())
        == {0, -sp.sqrt(2), sp.sqrt(2)},
        "a signed full-line time generator has a negative eigenvalue and cannot equal a physical-adjoint anticommutator",
    )

    # A fixed t=0 seam would have to preserve only translations tangent to it.
    # For a Lorentzian-real Weyl parameter, however, the normal component of
    # the standard N=1 closure vector is a strictly positive norm square.
    zeta_real = sp.symbols("zeta_1r zeta_1i zeta_2r zeta_2i", real=True)
    normal_translation = sum(component**2 for component in zeta_real)
    normal_hessian = sp.hessian(normal_translation, zeta_real)
    audit.check(
        "P17.real_temporal_seam_closure_obstruction",
        exact_zero(normal_hessian - 2 * sp.eye(4))
        and normal_hessian.is_positive_definite is True,
        "v^0=|zeta_1|^2+|zeta_2|^2 vanishes only for the zero real SUSY parameter",
    )
    complex_zeta = sp.Matrix([1, 0])
    independent_bar_zeta = sp.Matrix([0, 1])
    audit.check(
        "P17.complexified_temporal_seam_control",
        exact_zero((complex_zeta.T * independent_bar_zeta)[0])
        and independent_bar_zeta != complex_zeta.conjugate(),
        "a nonzero tangent complexified parameter exists only after abandoning Lorentzian conjugacy",
    )

    # Geometric pullback is complex-linear; physical Wigner time reversal includes K.
    complex_structure = sp.Matrix([[0, -1], [1, 0]])
    conjugation_real = sp.diag(1, -1)
    full_complex_structure = sp.kronecker_product(identity_2, complex_structure)
    geometric_reflection_real = sp.kronecker_product(branch_flip, identity_2)
    physical_time_reversal_real = sp.kronecker_product(
        branch_flip, conjugation_real
    )
    audit.check(
        "P17.geometric_reflection_linearity",
        exact_zero(comm(geometric_reflection_real, full_complex_structure)),
        "the bare pullback is a complex-linear operation on history functions",
    )
    audit.check(
        "P17.physical_time_reversal_antilinearity",
        exact_zero(anti(physical_time_reversal_real, full_complex_structure))
        and not exact_zero(
            comm(physical_time_reversal_real, full_complex_structure)
        ),
        "Wigner time reversal is anti-complex-linear and is not itself a conventional supercharge",
    )

    # Spatial versus temporal codimension-one projectors in mostly-plus signature.
    gamma_space = sp.diag(1, -1, 1, -1)
    real_half_space = (sp.eye(4) + gamma_space) / 2
    audit.check(
        "P17.spatial_boundary_real_half",
        exact_zero(gamma_space**2 - sp.eye(4))
        and exact_zero(real_half_space**2 - real_half_space)
        and real_half_space.rank() == 2,
        "a spacelike normal admits a real rank-two half-supersymmetry projector",
    )

    real_complex_unit = sp.Matrix([[0, 1], [-1, 0]])
    gamma_time = sp.kronecker_product(identity_2, real_complex_unit)
    temporal_plus = (sp.eye(4) + sp.I * gamma_time) / 2
    temporal_minus = (sp.eye(4) - sp.I * gamma_time) / 2
    audit.check(
        "P17.temporal_boundary_complex_half",
        exact_zero(gamma_time**2 + sp.eye(4))
        and exact_zero(anti(gamma_time, gamma_space))
        and exact_zero(temporal_plus**2 - temporal_plus)
        and temporal_plus.rank() == 2
        and exact_zero(temporal_plus.conjugate() - temporal_minus),
        "a timelike normal produces conjugate complex rank-two projectors",
    )
    real_majorana_equations = (temporal_plus - sp.eye(4)).applyfunc(
        sp.re
    ).col_join((temporal_plus - sp.eye(4)).applyfunc(sp.im))
    audit.check(
        "P17.temporal_boundary_no_real_half",
        real_majorana_equations.rank() == 4
        and len(real_majorana_equations.nullspace()) == 0,
        "a single-copy standard temporal projector preserves no nonzero real Majorana parameter",
    )

    doubled_normal = sp.kronecker_product(real_complex_unit, gamma_time)
    doubled_projector = (sp.eye(8) + doubled_normal) / 2
    doubled_sheet_sign = sp.kronecker_product(branch_sign, sp.eye(4))
    audit.check(
        "P17.doubled_real_temporal_projector",
        exact_zero(doubled_normal**2 - sp.eye(8))
        and exact_zero(doubled_projector**2 - doubled_projector)
        and doubled_projector.rank() == 4
        and all(entry.is_real is not False for entry in doubled_projector),
        "an extra real two-sheet complex structure yields a real rank-four fold projector",
    )
    audit.check(
        "P17.doubled_projector_mixes_sheets",
        exact_zero(anti(doubled_normal, doubled_sheet_sign))
        and (
            sp.kronecker_product(projector_minus, sp.eye(4))
            * doubled_normal
            * sp.kronecker_product(projector_plus, sp.eye(4))
        ).rank()
        == 4,
        "the admissible doubled real normal genuinely mixes the two sheets",
    )

    # A minimal abstract quartet realizes the topological SK BRST algebra.
    # This finite witness does not construct the full contour operator algebra
    # or a positive ghost inner product. Basis: (average, ghost, antighost,
    # difference).
    q_sk = sp.zeros(4)
    q_sk[1, 0] = 1
    q_sk[3, 2] = -1
    qbar_sk = sp.zeros(4)
    qbar_sk[2, 0] = 1
    qbar_sk[3, 1] = 1
    sk_parity = sp.diag(1, -1, -1, 1)
    audit.check(
        "P17.SK_BRST_algebra",
        exact_zero(q_sk**2)
        and exact_zero(qbar_sk**2)
        and exact_zero(anti(q_sk, qbar_sk)),
        "an abstract SK quartet carries two nilpotent mutually anticommuting BRST charges",
    )
    audit.check(
        "P17.SK_BRST_parity",
        exact_zero(anti(sk_parity, q_sk))
        and exact_zero(anti(sk_parity, qbar_sk)),
        "the Schwinger-Keldysh BRST charges are ghost-odd",
    )
    average, ghost, antighost, difference = [sp.eye(4).col(index) for index in range(4)]
    audit.check(
        "P17.SK_difference_exact",
        exact_zero(qbar_sk * ghost - difference)
        and exact_zero(-q_sk * antighost - difference),
        "the contour difference operator is BRST exact",
    )
    # This sign-indefinite matrix is only a contour-spectrum control.  It is
    # neither derived from the quartet nor asserted to commute with it.
    signed_contour_control = sp.diag(0, -energy, energy, 0)
    audit.check(
        "P17.SK_signed_contour_control_not_positive_H",
        set(signed_contour_control.eigenvals()) == {0, -energy, energy}
        and exact_zero(anti(q_sk, qbar_sk)),
        "a signed contour spectrum has both energy signs and is not a positive physical-adjoint SUSY Hamiltonian",
    )

    result: dict[str, object] = {
        "time_model": "t is the base coordinate on R; no scalar clock or rolling background",
        "exact_checks": audit.passed,
        "standard_local_N1": {
            "algebra": "PASS_ON_FIXED_POSITIVE_ENERGY_FIBER",
            "half_exchange": "ZERO_BY_SUPPORT_LOCALITY",
            "interpretation": "standard Q changes fermion parity at the same spacetime point",
        },
        "linear_reflection_composed_charge": {
            "fixed_fiber_algebra": "PASS",
            "half_exchange_ranks_per_Weyl_component": fold_cross_ranks,
            "locality": "FAIL_NONLOCAL_ON_THE_UNFOLDED_TIME_LINE",
            "time_translation": "FAIL_ANTICOMMUTES_WITH_SIGNED_P_T",
        },
        "fundamental_doubled_sheet": {
            "algebra": "PASS_WITH_BIDIRECTIONAL_UNITARY_FLIP",
            "one_way_arrow": "FAILS_STANDARD_ADJOINT_CLOSURE",
            "physical_time_half_identification": "OPEN_NEW_ACTION_PROBLEM_NOT_EVIDENCE_FOR_BARE_LITERAL_HALVES",
            "continuous_mixing": "NOT_SELECTED_BY_THE_SUPERALGEBRA",
        },
        "temporal_boundary_reality": {
            "ordinary_real_fixed_seam_subalgebra": "ZERO_ONLY",
            "single_copy_real_preserved_parameters": 0,
            "doubled_real_projector_rank": 4,
            "doubled_physical_bulk_boundary_action": "OPEN",
        },
        "physical_time_reversal": {
            "complex_linearity": "FAIL_ANTIUNITARY",
            "role": "DISCRETE_AUTOMORPHISM_OR_SEWING_MAP_NOT_A_SUPERCHARGE",
        },
        "schwinger_keldysh_timefold": {
            "BRST_superalgebra": "PASS_ABSTRACT_QUARTET_WITNESS",
            "difference_operator": "BRST_EXACT",
            "particle_superpartner_interpretation": "NO",
            "full_contour_operator_algebra_and_ghost_metric": "NOT_CONSTRUCTED",
        },
        "most_promising_open_construction": {
            "name": "DOUBLED_REAL_SHEET_MIXING_FOLD_CANDIDATE",
            "next_required": [
                "a source-defined Pin or Clifford lift and reflection cocycle",
                "a real Lorentzian doubled bulk-plus-interface action",
                "a variationally admissible t=0 gluing domain",
                "a conserved complex-linear fermionic charge on that domain",
                "compatibility of the sheet-mixing projector with that charge",
                "a physical sheet anchor and basis-invariant observable",
            ],
        },
        "scope_guard": {
            "literal_local_Q_exchanges_coordinate_halves": "CONTRADICTED",
            "nonlocal_or_fundamental_doubled_exchange": "ALGEBRAICALLY_ALLOWED",
            "full_4D_SUGRA_interface": "NOT_YET_CONSTRUCTED",
            "CPT_or_Pin_pairing": "BOSONIC_DISCRETE_PAIRING_NOT_PARTICLE_SUSY",
        },
    }
    print("PHASE17_RESULT=" + json.dumps(result, sort_keys=True, ensure_ascii=False))
    return result


if __name__ == "__main__":
    run()
