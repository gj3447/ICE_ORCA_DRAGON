#!/usr/bin/env python3
"""Phase 13A — Lorentzian local-SUGRA WKB branch-supercharge kill test.

This executable keeps three logically separate statements apart.

P13A-1 is a formal principal-symbol control.  The matter-coupled,
Lorentzian k=+1 FRW reduction of 4D N=1 supergravity in Moniz,
arXiv:gr-qc/9606047, has a complex-linear first-order local SUSY constraint.
The executable imports only the partial_a and partial_phi principal terms of
its equation (9).  Acting on a formal phase exp(+/- i lambda W), those terms
retain the input phase.  W is not a solved Moniz Hamilton--Jacobi function,
and the finite +/- direct sum below is not a relational spectral projector.
This control therefore has no standalone verdict on physical cosmological
branches.

P13A-2 is an exact finite positive-kernel witness.  We deliberately build an
odd Q that flips both formal sheet label and fermion parity off shell.  If a
toy kernel is ker C for C={Q,Q^dagger} on a positive finite Hilbert space, Q
and Q^dagger vanish there.  This is not derived from the Moniz or
Eder--Sahlmann constraints, adjoint, or physical inner product.

P13A-3 is a generic two-mode CAR null control.  It shows that odd operators
can close on an even symbol while remaining diagonal in a formal sheet label.
It is not a normalized or executable reproduction of Eder--Sahlmann: their
volume shifts, Theta term, reality conditions, ordering, domain, and residual
SUSY-constraint structure terms are absent.

The finite positive-kernel attempt and the inference "closure implies sheet
exchange" are contradicted in their exact toy scopes.  The literal relational
branch=superpartner claim remains INCONCLUSIVE/UNCONSTRUCTED because no
relational projector, common physical domain, or distinct reduced/asymptotic
fermionic charge is built here.

Contract: PHASE13A_RESEARCH_CONTRACT.json (PREREGISTERED before this file).
Verification:
    uv run --with sympy python3 phase13a_lorentzian_branch_supercharge.py
"""

from __future__ import annotations

import sys
from collections.abc import Callable

import sympy as sp


class Audit:
    """Exact-check recorder; no floating tolerance or numerical fallback."""

    def __init__(self) -> None:
        self.passed = 0
        self.mutants_rejected = 0

    def check(self, check_id: str, condition: bool, statement: str) -> None:
        if not condition:
            raise AssertionError(f"{check_id}: {statement}")
        self.passed += 1
        print(f"[PASS] {check_id}: {statement}")

    def reject(self, check_id: str, condition: bool, statement: str) -> None:
        if not condition:
            raise AssertionError(f"{check_id}: mutant survived — {statement}")
        self.mutants_rejected += 1
        print(f"[MUTANT REJECTED] {check_id}: {statement}")


def kron(*matrices: sp.MatrixBase) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return sp.Matrix(result)


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def commutator(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left * right - right * left)


def anticommutator(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(left * right + right * left)


def projector_from_vector(vector: sp.Matrix) -> sp.Matrix:
    norm = sp.simplify((vector.H * vector)[0])
    return sp.simplify(vector * vector.H / norm)


def two_mode_car() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Return annihilators, creators, and parity for two fermion modes."""
    identity = sp.eye(2)
    z = sp.diag(1, -1)
    annihilator = sp.Matrix([[0, 1], [0, 0]])
    a_chi = kron(annihilator, identity)
    a_psi = kron(z, annihilator)
    adag_chi = a_chi.H
    adag_psi = a_psi.H
    parity = kron(z, z)
    return a_chi, a_psi, adag_chi, adag_psi, parity


def part_source_wkb_locality(audit: Audit) -> None:
    """Formal Moniz-principal-term control: derivatives retain WKB phase."""
    scale = sp.symbols("a", positive=True)
    wavelength = sp.symbols("lambda", real=True, nonzero=True)
    # phi and phi_bar are independent complex chart symbols for formal
    # differentiation.  No conjugation relation or physical HJ solution is
    # inferred from them.
    scalar, scalar_bar = sp.symbols("phi phi_bar")
    phase = sp.Function("W")(scale, scalar, scalar_bar)

    wave_plus = sp.exp(sp.I * wavelength * phase)
    wave_minus = sp.exp(-sp.I * wavelength * phase)
    expected_a_plus = sp.I * wavelength * sp.diff(phase, scale)
    expected_phi_plus = sp.I * wavelength * sp.diff(phase, scalar)

    audit.check(
        "P13A.source.wkb_plus_phase",
        sp.simplify(sp.diff(wave_plus, scale) / wave_plus - expected_a_plus)
        == 0
        and sp.simplify(
            sp.diff(wave_plus, scalar) / wave_plus - expected_phi_plus
        )
        == 0,
        "the imported formal first-order derivatives retain exp(+i lambda W)",
    )
    audit.check(
        "P13A.source.wkb_minus_phase",
        sp.simplify(sp.diff(wave_minus, scale) / wave_minus + expected_a_plus)
        == 0
        and sp.simplify(
            sp.diff(wave_minus, scalar) / wave_minus + expected_phi_plus
        )
        == 0,
        "the imported formal first-order derivatives retain exp(-i lambda W)",
    )

    # Eq. (9) principal coefficients for one spinor component.  Multiplicative
    # lower-order fermion terms also retain the phase and hence cannot add an
    # off-diagonal WKB canonical relation.
    coeff_chi_plus = sp.simplify(
        wavelength
        * (1 + scalar * scalar_bar)
        * sp.diff(phase, scalar)
        / sp.sqrt(2)
    )
    coeff_psi_plus = sp.simplify(
        -sp.I
        * wavelength
        * scale
        * sp.diff(phase, scale)
        / (2 * sp.sqrt(6))
    )
    coeff_chi_minus = -coeff_chi_plus
    coeff_psi_minus = -coeff_psi_plus
    audit.check(
        "P13A.source.principal_sign",
        sp.simplify(coeff_chi_plus + coeff_chi_minus) == 0
        and sp.simplify(coeff_psi_plus + coeff_psi_minus) == 0,
        "reversing the full WKB covector changes the principal-symbol sign, not the WKB phase",
    )

    _, _, create_chi, create_psi, parity_f = two_mode_car()
    branch_z = sp.diag(1, -1)
    branch_x = sp.Matrix([[0, 1], [1, 0]])
    identity_b = sp.eye(2)
    identity_f = sp.eye(4)
    formal_plus = (identity_b + branch_z) / 2
    formal_minus = (identity_b - branch_z) / 2

    # Use independent generic endpoint symbols so the zero cross blocks do
    # not depend on the special full-covector reversal relation above.
    x_plus, y_plus, x_minus, y_minus = sp.symbols(
        "x_plus y_plus x_minus y_minus", nonzero=True
    )
    symbol_plus = x_plus * create_chi + y_plus * create_psi
    symbol_minus = x_minus * create_chi + y_minus * create_psi
    local_symbol = kron(formal_plus, symbol_plus) + kron(
        formal_minus, symbol_minus
    )
    branch_grading = kron(branch_z, identity_f)
    fermion_parity = kron(identity_b, parity_f)
    formal_plus_full = kron(formal_plus, identity_f)
    formal_minus_full = kron(formal_minus, identity_f)

    audit.check(
        "P13A.source.fermion_odd",
        zero_matrix(anticommutator(fermion_parity, local_symbol)),
        "the imported formal principal symbol is fermion odd",
    )
    audit.check(
        "P13A.source.branch_diagonal",
        zero_matrix(commutator(branch_grading, local_symbol))
        and zero_matrix(formal_minus_full * local_symbol * formal_plus_full)
        and zero_matrix(formal_plus_full * local_symbol * formal_minus_full),
        "the formal direct-sum encoding is sheet diagonal by construction; it is not a relational-projector result",
    )
    plus_block = sp.simplify(formal_plus_full * local_symbol * formal_plus_full)
    minus_block = sp.simplify(formal_minus_full * local_symbol * formal_minus_full)
    audit.check(
        "P13A.source.diagonal_nonzero",
        plus_block.subs({x_plus: 2, y_plus: 3, x_minus: 5, y_minus: 7}).rank()
        > 0
        and minus_block.subs(
            {x_plus: 2, y_plus: 3, x_minus: 5, y_minus: 7}
        ).rank()
        > 0,
        "both formal phase sheets have a nonzero generic within-sheet odd symbol",
    )
    audit.check(
        "P13A.source.exchange_identity_fails",
        not zero_matrix(
            local_symbol * formal_plus_full - formal_minus_full * local_symbol
        )
        and not zero_matrix(
            local_symbol * formal_minus_full - formal_plus_full * local_symbol
        ),
        "the formal sheet-diagonal control fails both exchange intertwiners",
    )

    appended_reflection = kron(branch_x, identity_f)
    audit.check(
        "P13A.source.appended_reflection",
        zero_matrix(anticommutator(branch_grading, appended_reflection))
        and (
            formal_minus_full * appended_reflection * formal_plus_full
        ).rank()
        == 4,
        "an explicit sheet reflection exchanges the formal labels, but it is an extra operator absent from the imported principal terms",
    )
    audit.reject(
        "P13A.mutant.local_means_exchange",
        zero_matrix(formal_minus_full * local_symbol * formal_plus_full)
        and plus_block.subs(
            {x_plus: 2, y_plus: 3, x_minus: 5, y_minus: 7}
        ).rank()
        > 0,
        "fermion oddness within a formal sheet was misreported as relational branch exchange",
    )
    conjugation_witness = sp.Matrix([1 + sp.I, 2 - sp.I])
    conjugated = conjugation_witness.applyfunc(sp.conjugate)
    conjugated_after_i = (sp.I * conjugation_witness).applyfunc(sp.conjugate)
    audit.reject(
        "P13A.mutant.cpt_is_complex_linear_q",
        zero_matrix(conjugated_after_i + sp.I * conjugated)
        and not zero_matrix(conjugated_after_i - sp.I * conjugated),
        "complex conjugation obeys K(i psi)=-i K(psi), unlike a complex-linear supercharge",
    )


def part_positive_physical_kernel(audit: Audit) -> None:
    """An explicit finite off-shell sheet flip vanishes on ker{Q,Q^dag}."""
    branch_x = sp.Matrix([[0, 1], [1, 0]])
    branch_z = sp.diag(1, -1)
    fermion_x = branch_x
    fermion_z = branch_z
    identity_b = sp.eye(2)
    identity_c = sp.eye(3)
    identity_f = sp.eye(2)

    differential = sp.Matrix([[0, 0, 0], [0, 0, 0], [1, -1, 0]])
    differential_dag = differential.H
    cochain_laplacian = anticommutator(differential, differential_dag)
    q = kron(branch_x, differential, fermion_x)
    q_dag = q.H
    constraint = anticommutator(q, q_dag)
    expected_constraint = kron(identity_b, cochain_laplacian, identity_f)
    branch_grading = kron(branch_z, identity_c, identity_f)
    fermion_parity = kron(identity_b, identity_c, fermion_z)

    audit.check(
        "P13A.kernel.nilpotent",
        zero_matrix(q * q) and zero_matrix(q_dag * q_dag),
        "the explicit finite Q and Q^dagger are nilpotent",
    )
    audit.check(
        "P13A.kernel.odd_and_exchange",
        zero_matrix(anticommutator(fermion_parity, q))
        and zero_matrix(anticommutator(branch_grading, q)),
        "off shell Q flips both fermion parity and the formal sheet grading",
    )
    audit.check(
        "P13A.kernel.positive_closure",
        zero_matrix(constraint - expected_constraint)
        and cochain_laplacian.eigenvals() == {sp.Integer(0): 1, sp.Integer(2): 2}
        and constraint.eigenvals() == {sp.Integer(0): 4, sp.Integer(2): 8},
        "C={Q,Q^dagger}=I tensor C0 tensor I with exact spectrum 0^4 and 2^8",
    )
    audit.check(
        "P13A.kernel.constraint_commutes",
        zero_matrix(commutator(constraint, branch_grading))
        and zero_matrix(commutator(constraint, fermion_parity))
        and zero_matrix(commutator(constraint, q))
        and zero_matrix(commutator(constraint, q_dag)),
        "the positive constraint preserves formal-sheet/parity grading and commutes with its differentials",
    )
    audit.check(
        "P13A.kernel.norm_identity",
        zero_matrix(constraint - q * q.H - q.H * q),
        "<v,Cv>=||Qv||^2+||Q^dagger v||^2 on the positive finite Hilbert space",
    )

    harmonic = sp.Matrix([1, 1, 0])
    harmonic_projector = projector_from_vector(harmonic)
    toy_kernel_projector = kron(identity_b, harmonic_projector, identity_f)
    p_plus = kron((identity_b + branch_z) / 2, identity_c, identity_f)
    p_minus = kron((identity_b - branch_z) / 2, identity_c, identity_f)
    f_plus = kron(identity_b, identity_c, (identity_f + fermion_z) / 2)
    f_minus = kron(identity_b, identity_c, (identity_f - fermion_z) / 2)

    audit.check(
        "P13A.kernel.projector",
        zero_matrix(toy_kernel_projector * toy_kernel_projector - toy_kernel_projector)
        and zero_matrix(constraint * toy_kernel_projector)
        and toy_kernel_projector.rank() == 4
        and len(constraint.nullspace()) == 4,
        "the toy projector spans exactly the four-dimensional positive-constraint kernel",
    )
    cell_ranks = [
        (toy_kernel_projector * branch * parity).rank()
        for branch in (p_plus, p_minus)
        for parity in (f_plus, f_minus)
    ]
    audit.check(
        "P13A.kernel.all_cells_occupied",
        cell_ranks == [1, 1, 1, 1],
        "every formal-sheet/parity cell of the toy kernel has rank one",
    )
    off_shell_forward = p_minus * f_minus * q * p_plus * f_plus
    off_shell_backward = p_plus * f_plus * q * p_minus * f_minus
    audit.check(
        "P13A.kernel.off_shell_nonzero",
        off_shell_forward.rank() > 0 and off_shell_backward.rank() > 0,
        "the explicit Q has nonzero off-shell sheet/parity-flipping blocks",
    )
    kernel_forward = (
        p_minus
        * f_minus
        * toy_kernel_projector
        * q
        * toy_kernel_projector
        * p_plus
        * f_plus
    )
    kernel_backward = (
        p_plus
        * f_plus
        * toy_kernel_projector
        * q
        * toy_kernel_projector
        * p_minus
        * f_minus
    )
    audit.check(
        "P13A.kernel.kernel_map_zero",
        zero_matrix(q * toy_kernel_projector)
        and zero_matrix(q_dag * toy_kernel_projector)
        and kernel_forward.rank() == 0
        and kernel_backward.rank() == 0,
        "the induced Q map between occupied toy-kernel sheet sectors is exactly zero",
    )

    branch_diagonal_mutant = kron(identity_b, differential, fermion_x)
    fermion_even_mutant = kron(branch_x, differential, identity_f)
    audit.reject(
        "P13A.mutant.odd_but_branch_diagonal",
        zero_matrix(anticommutator(fermion_parity, branch_diagonal_mutant))
        and zero_matrix(p_minus * branch_diagonal_mutant * p_plus),
        "fermion-odd Q without branch exchange was accepted",
    )
    audit.reject(
        "P13A.mutant.branch_flip_but_fermion_even",
        zero_matrix(anticommutator(branch_grading, fermion_even_mutant))
        and zero_matrix(commutator(fermion_parity, fermion_even_mutant)),
        "a fermion-even branch reflection was accepted as a supercharge",
    )
    audit.reject(
        "P13A.mutant.off_shell_only",
        off_shell_forward.rank() > 0 and kernel_forward.rank() == 0,
        "nonzero off-shell rank was reported without positive-kernel projection",
    )

    # A one-sided kernel can conceal the other differential.  The cochain
    # vector e3 lies in ker Q but not ker Q^dagger.
    branch_plus_vector = sp.Matrix([1, 0])
    cochain_e3 = sp.Matrix([0, 0, 1])
    fermion_plus_vector = sp.Matrix([1, 0])
    one_sided_witness = kron(
        branch_plus_vector, cochain_e3, fermion_plus_vector
    )
    audit.reject(
        "P13A.mutant.one_sided_constraint",
        zero_matrix(q * one_sided_witness)
        and not zero_matrix(q_dag * one_sided_witness),
        "using only Q^dagger Q leaves states on which Q^dagger acts nontrivially",
    )

    theta = sp.pi / 2
    rotation = sp.Matrix(
        [[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]]
    )
    flavor_transport = kron(identity_f, rotation)
    flavor_parity = kron(fermion_z, sp.eye(2))
    audit.reject(
        "P13A.mutant.even_flavor_transport_is_q",
        zero_matrix(commutator(flavor_parity, flavor_transport))
        and not zero_matrix(anticommutator(flavor_parity, flavor_transport)),
        "whole-multiplet flavor transport commutes with fermion parity and is not Q",
    )


def part_generic_car_closure_null_control(audit: Audit) -> None:
    """Generic odd CAR operators can close while remaining sheet diagonal."""
    a_chi, a_psi, adag_chi, adag_psi, parity_f = two_mode_car()
    annihilators = [a_chi, a_psi]
    creators = [adag_chi, adag_psi]
    identity_f = sp.eye(4)
    identity_b = sp.eye(2)
    branch_z = sp.diag(1, -1)
    k_symbol = sp.symbols("k", nonzero=True, real=True)
    local_bosonic_symbol = sp.diag(k_symbol, -k_symbol)
    hamiltonian_symbol = kron(local_bosonic_symbol**2, identity_f)
    fermion_parity = kron(identity_b, parity_f)
    branch_grading = kron(branch_z, identity_f)
    p_plus = kron((identity_b + branch_z) / 2, identity_f)
    p_minus = kron((identity_b - branch_z) / 2, identity_f)

    left = [kron(local_bosonic_symbol, op) for op in annihilators]
    right = [kron(local_bosonic_symbol, op) for op in creators]
    car_ok = True
    closure_ok = True
    for index in range(2):
        for other in range(2):
            target = hamiltonian_symbol if index == other else sp.zeros(8)
            car_ok = car_ok and zero_matrix(
                anticommutator(annihilators[index], creators[other])
                - (sp.eye(4) if index == other else sp.zeros(4))
            )
            closure_ok = closure_ok and zero_matrix(
                anticommutator(left[index], right[other]) - target
            )

    audit.check(
        "P13A.closure.two_mode_car",
        car_ok,
        "the two reduced fermion modes obey the exact CAR",
    )
    audit.check(
        "P13A.closure.left_right",
        closure_ok,
        "generic left/right odd CAR operators close on delta_AB times an even symbol",
    )
    audit.check(
        "P13A.closure.odd",
        all(
            zero_matrix(anticommutator(fermion_parity, operator))
            for operator in left + right
        ),
        "every generic left/right CAR operator is fermion odd",
    )
    audit.check(
        "P13A.closure.branch_preserving",
        all(
            zero_matrix(commutator(branch_grading, operator))
            and zero_matrix(p_minus * operator * p_plus)
            and zero_matrix(p_plus * operator * p_minus)
            for operator in left + right
        )
        and zero_matrix(commutator(branch_grading, hamiltonian_symbol)),
        "CAR closure and the even symbol are simultaneously formal-sheet diagonal",
    )
    audit.reject(
        "P13A.mutant.closure_implies_exchange",
        not zero_matrix(hamiltonian_symbol)
        and all(zero_matrix(p_minus * operator * p_plus) for operator in left),
        "nonzero generic CAR closure was reported as proof of relational branch exchange",
    )


def run_part(label: str, fn: Callable[[Audit], None], audit: Audit) -> None:
    print(f"\n=== {label} ===")
    fn(audit)


def main() -> int:
    audit = Audit()
    run_part(
        "P13A-1 formal Moniz-principal-term WKB control",
        part_source_wkb_locality,
        audit,
    )
    run_part(
        "P13A-2 finite positive-kernel sheet map",
        part_positive_physical_kernel,
        audit,
    )
    run_part(
        "P13A-3 generic CAR closure null control",
        part_generic_car_closure_null_control,
        audit,
    )
    print(
        "\n[OPEN] P13A-G4: no gauge-independent relational branch projector, "
        "common physical inner product, or distinct nonzero boundary/reduced "
        "fermionic charge was constructed in the selected 4D source model."
    )
    print(
        f"\nALL EXACT CHECKS PASSED: {audit.passed} positive checks; "
        f"{audit.mutants_rejected} semantic mutants rejected."
    )
    print(
        "CORRECTED SCOPED INFERENCE: the finite positive-kernel attempt and "
        "the logic 'CAR closure implies sheet exchange' are CONTRADICTED in "
        "their toy scopes.  The formal WKB control is INCONCLUSIVE."
    )
    print(
        "CORE INFERENCE: P13A_LITERAL_WKB_BRANCH_SUPERPARTNER remains "
        "INCONCLUSIVE/UNCONSTRUCTED because G4 has no relational spectral "
        "projector, common physical domain/inner product, or distinct nonzero charge."
    )
    print(
        "SEQUENCING: stop the core chain here.  A Phase13B spatial S-matrix "
        "would be an auxiliary interface project with zero evidential weight "
        "for the literal cosmological claim."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
