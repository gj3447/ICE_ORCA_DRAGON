#!/usr/bin/env python3
"""Phase 16 — direct BGG single-source parent and FLRW tangency calculation.

The calculation uses only the conventions and component formulas printed in
Binétruy, Girardi and Grimm, hep-th/0005225v1:

* CPN.13 for the bosonic torsion equation,
* the curvature two-form and the literal ``ab`` contraction in CPN.26,
* CPN.59 and the combined CPN.130 action at ``W = 0``, and
* CPN.40, CPN.75, CPN.77 and CPN.85 for two exact tangency witnesses, and
* CPN.93 and its conjugate CPN.99 for the rolling-clock background-invariance check.

It deliberately contains no research-contract, commit-order, ontology, or
classification machinery.  All arithmetic is exact SymPy arithmetic and the
program writes no files.

Run:
    uv run --with sympy python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import sympy as sp


SOURCE = "Binétruy–Girardi–Grimm, hep-th/0005225v1"


@dataclass
class Audit:
    passed: int = 0

    def check(self, name: str, condition: bool, statement: str) -> None:
        if not condition:
            raise AssertionError(f"{name}: {statement}")
        self.passed += 1
        print(f"[PASS] {name}: {statement}")


def exact_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    value = sp.simplify(value)
    if isinstance(value, sp.MatrixBase):
        return value == sp.zeros(*value.shape)
    return value == 0


# Positive background parameters and independent coordinate-time jets.
M_P, V_0, a, N = sp.symbols("M_P V_0 a N", positive=True)
adot, addot, Ndot, Nddot = sp.symbols(
    "adot addot Ndot Nddot", real=True
)
Xdot, Tdot, Ydot = sp.symbols("Xdot Tdot Ydot", real=True)
p_X, p_T, p_Y = sp.symbols("p_X p_T p_Y", real=True)

ETA = (-1, 1, 1, 1)


def d_dt(expression: sp.Expr) -> sp.Expr:
    """Total derivative on the finite FLRW jet used in this calculation."""

    jet = {a: adot, adot: addot, N: Ndot, Ndot: Nddot}
    return sp.expand(
        sum(sp.diff(expression, variable) * derivative for variable, derivative in jet.items())
    )


def d_coord(coordinate: int, expression: sp.Expr) -> sp.Expr:
    return d_dt(expression) if coordinate == 0 else sp.S.Zero


def coframe() -> sp.Matrix:
    return sp.diag(N, a, a, a)


def inverse_coframe() -> sp.Matrix:
    # E[a,m] is the matrix inverse of e[m,a].  The lower Lorentz label is
    # conventional here; no extra eta factor belongs in this inverse.
    return sp.diag(1 / N, 1 / a, 1 / a, 1 / a)


def solve_bgg_connection() -> tuple[list[list[list[sp.Expr]]], dict[tuple[int, int, int], sp.Expr]]:
    """Solve CPN.13 plus omega_(mab)=-omega_(mba), rather than using CPN.15."""

    e = coframe()
    keys: list[tuple[int, int, int]] = []
    unknowns: list[sp.Symbol] = []
    for m in range(4):
        for left in range(4):
            for right in range(left + 1, 4):
                keys.append((m, left, right))
                unknowns.append(sp.Symbol(f"omega_{m}_{left}_{right}"))
    lower_independent = dict(zip(keys, unknowns, strict=True))

    def omega_lower(m: int, left: int, right: int) -> sp.Expr:
        if left == right:
            return sp.S.Zero
        if left < right:
            return lower_independent[(m, left, right)]
        return -lower_independent[(m, right, left)]

    def omega_mixed(m: int, lower: int, upper: int) -> sp.Expr:
        return ETA[upper] * omega_lower(m, lower, upper)

    equations: list[sp.Expr] = []
    # CPN.13 at psi=0:
    # d_n e_m^A + e_m^b omega_(n b)^A - (m <-> n) = 0.
    for n in range(4):
        for m in range(n + 1, 4):
            for upper in range(4):
                equation = d_coord(n, e[m, upper])
                equation += sum(
                    e[m, lower] * omega_mixed(n, lower, upper)
                    for lower in range(4)
                )
                equation -= d_coord(m, e[n, upper])
                equation -= sum(
                    e[n, lower] * omega_mixed(m, lower, upper)
                    for lower in range(4)
                )
                equations.append(sp.expand(equation))

    solution_set = sp.linsolve(equations, unknowns)
    if solution_set is sp.EmptySet or len(solution_set) != 1:
        raise AssertionError("CPN.13 did not have one exact connection solution")
    solution_tuple = next(iter(solution_set))
    if any(value.free_symbols & set(unknowns) for value in solution_tuple):
        raise AssertionError("CPN.13 connection solution retained a free connection component")
    solution = dict(zip(unknowns, solution_tuple, strict=True))

    mixed = [
        [[sp.S.Zero for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for m in range(4):
        for lower in range(4):
            for upper in range(4):
                mixed[m][lower][upper] = sp.simplify(
                    omega_mixed(m, lower, upper).subs(solution)
                )
    solved_lower = {
        key: sp.simplify(symbol.subs(solution))
        for key, symbol in lower_independent.items()
    }
    return mixed, solved_lower


def bgg_curvature(
    omega: list[list[list[sp.Expr]]],
) -> list[list[list[list[sp.Expr]]]]:
    """Build R[n,m,b_lower,a_upper] from R_b^a=d omega_b^a+omega_b^c omega_c^a."""

    curvature = [
        [
            [[sp.S.Zero for _ in range(4)] for _ in range(4)]
            for _ in range(4)
        ]
        for _ in range(4)
    ]
    for n in range(4):
        for m in range(4):
            for lower in range(4):
                for upper in range(4):
                    component = d_coord(n, omega[m][lower][upper])
                    component -= d_coord(m, omega[n][lower][upper])
                    component += sum(
                        omega[m][lower][middle] * omega[n][middle][upper]
                        - omega[n][lower][middle] * omega[m][middle][upper]
                        for middle in range(4)
                    )
                    curvature[n][m][lower][upper] = sp.simplify(component)
    return curvature


def contract_cpn26(
    curvature: list[list[list[list[sp.Expr]]]],
) -> sp.Expr:
    """Literal CPN.26: e_a^n e_b^m (R_nm)^(ab).

    With storage R[n,m,b_lower,a_upper], the first printed upper index
    comes from raising the stored lower connection index.  Hence the exact
    array access is R[n,m,a,b] with eta[a], not R[n,m,b,a] with eta[b].
    """

    E = inverse_coframe()
    return sp.simplify(
        sum(
            E[a_index, n]
            * E[b_index, m]
            * ETA[a_index]
            * curvature[n][m][a_index][b_index]
            for n in range(4)
            for m in range(4)
            for a_index in range(4)
            for b_index in range(4)
        )
    )


def swapped_ba_diagnostic(
    curvature: list[list[list[list[sp.Expr]]]],
) -> sp.Expr:
    """The forbidden storage-order/``ba`` reading, retained only as a sign diagnostic."""

    E = inverse_coframe()
    return sp.simplify(
        sum(
            E[a_index, n]
            * E[b_index, m]
            * ETA[b_index]
            * curvature[n][m][b_index][a_index]
            for n in range(4)
            for m in range(4)
            for a_index in range(4)
            for b_index in range(4)
        )
    )


def pauli_and_spin32_projector() -> tuple[list[sp.Matrix], sp.Matrix]:
    """Exact spatial Clifford matrices and the right-acting vector-spinor projector."""

    sigma = [
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    ]
    # At the identity tetrad the induced matrices are Gamma_i=-sigma_i.
    gamma = [-matrix for matrix in sigma]
    # For row spinors rho_i=sum_j psi_j P_i^j, the flattened right-acting
    # matrix has input block j and output block i.
    projector = sp.zeros(6, 6)
    for j in range(3):
        for i in range(3):
            block = sp.eye(2) if i == j else sp.zeros(2)
            block -= sp.Rational(1, 3) * gamma[j] * gamma[i]
            projector[2 * j : 2 * j + 2, 2 * i : 2 * i + 2] = block
    return gamma, projector


def run() -> dict[str, object]:
    audit = Audit()

    omega, omega_lower = solve_bgg_connection()
    expected_nonzero = {
        (1, 0, 1): adot / N,
        (2, 0, 2): adot / N,
        (3, 0, 3): adot / N,
    }
    audit.check(
        "P16.connection",
        all(
            sp.simplify(value - expected_nonzero.get(key, 0)) == 0
            for key, value in omega_lower.items()
        ),
        "CPN.13 uniquely gives omega_(i 0 i)=adot/N and no other lower-pair component",
    )
    audit.check(
        "P16.connection_mixed",
        all(
            sp.simplify(omega[i][0][i] - adot / N) == 0
            and sp.simplify(omega[i][i][0] - adot / N) == 0
            for i in range(1, 4)
        ),
        "raising the final Lorentz index gives the two required equal mixed components",
    )

    curvature = bgg_curvature(omega)
    audit.check(
        "P16.curvature_antisymmetry",
        all(
            exact_zero(
                curvature[n][m][lower][upper]
                + curvature[m][n][lower][upper]
            )
            for n in range(4)
            for m in range(4)
            for lower in range(4)
            for upper in range(4)
        ),
        "R[n,m] is antisymmetric in the reverse-order two-form coordinate pair",
    )
    Q = (
        addot / (a * N**2)
        + adot**2 / (a**2 * N**2)
        - adot * Ndot / (a * N**3)
    )
    R_bgg = contract_cpn26(curvature)
    R_ba = swapped_ba_diagnostic(curvature)
    audit.check(
        "P16.CPN26_ab",
        exact_zero(R_bgg + 6 * Q),
        "the literal printed ab contraction gives calR_BGG=-6Q",
    )
    audit.check(
        "P16.CPN26_ba_mutation",
        exact_zero(R_ba - 6 * Q) and not exact_zero(R_ba - R_bgg),
        "the transposed ba/storage reading gives the opposite +6Q and is rejected",
    )

    determinant = V_0 * N * a**3
    L_gravity_raw = sp.simplify(determinant * (-M_P**2 / 2) * R_bgg)
    B = 3 * M_P**2 * V_0 * a**2 * adot / N
    C = M_P**2 * V_0 * a * adot**2 / N
    dot_B = sp.simplify(d_dt(B))
    audit.check(
        "P16.raw_boundary",
        exact_zero(L_gravity_raw - (dot_B - 3 * C)),
        "CPN.130 gives L_EH,raw=dot(B)-3C at arbitrary lapse",
    )
    L_gravity_first = sp.simplify(L_gravity_raw - dot_B)
    audit.check(
        "P16.first_order_gravity",
        exact_zero(L_gravity_first + 3 * C)
        and not L_gravity_first.has(addot, Ndot, Nddot),
        "subtracting the one temporal endpoint leaves -3C and no higher jet",
    )

    Phi_dot = (Tdot + sp.I * Ydot) / sp.sqrt(2)
    Phi_bar_dot = (Tdot - sp.I * Ydot) / sp.sqrt(2)
    scalar_product = sp.expand(Phi_dot * Phi_bar_dot)
    L_scalar = sp.simplify(V_0 * a**3 * scalar_product / N)
    audit.check(
        "P16.same_source_scalar",
        exact_zero(scalar_product - (Tdot**2 + Ydot**2) / 2)
        and not scalar_product.has(sp.I),
        "the positive physical field bridge gives (Tdot^2+Ydot^2)/2",
    )

    adot_from_X = a * Xdot / (sp.sqrt(6) * M_P)
    L_first = sp.simplify((L_gravity_first + L_scalar).subs(adot, adot_from_X))
    prefactor = V_0 * a**3 / N
    expected_L = prefactor * (-Xdot**2 + Tdot**2 + Ydot**2) / 2
    audit.check(
        "P16.first_order_L",
        exact_zero(L_first - expected_L),
        "X=sqrt(6) M_P ln(a) gives the Lorentzian (-,+,+) kinetic form",
    )
    velocities = (Xdot, Tdot, Ydot)
    hessian = sp.hessian(L_first, velocities)
    expected_hessian = prefactor * sp.diag(-1, 1, 1)
    audit.check(
        "P16.hessian",
        exact_zero(hessian - expected_hessian),
        "the exact velocity Hessian is (V0 a^3/N) diag(-1,+1,+1)",
    )
    audit.check(
        "P16.hessian_invariants",
        hessian.rank() == 3
        and exact_zero(hessian.det() + prefactor**3),
        "the Hessian has rank 3, determinant -prefactor^3, and inertia (1,0,2)",
    )

    derived_momenta = [sp.diff(L_first, velocity) for velocity in velocities]
    expected_momenta = [-prefactor * Xdot, prefactor * Tdot, prefactor * Ydot]
    audit.check(
        "P16.momenta",
        all(
            exact_zero(observed - expected)
            for observed, expected in zip(derived_momenta, expected_momenta, strict=True)
        ),
        "the canonical momenta carry the same (-,+,+) signature",
    )
    velocity_solution = {
        Xdot: -p_X / prefactor,
        Tdot: p_T / prefactor,
        Ydot: p_Y / prefactor,
    }
    Hamiltonian = sp.simplify(
        (p_X * Xdot + p_T * Tdot + p_Y * Ydot - L_first).subs(
            velocity_solution
        )
    )
    expected_H = N * (-p_X**2 + p_T**2 + p_Y**2) / (2 * V_0 * a**3)
    audit.check(
        "P16.Hamiltonian",
        exact_zero(Hamiltonian - expected_H),
        "the exact kinetic Hamiltonian is N(-pX^2+pT^2+pY^2)/(2V0a^3)",
    )

    # --- Off-shell homogeneous FLRW tangency: two independent witnesses. ---
    gamma, projector = pauli_and_spin32_projector()
    audit.check(
        "P16.spin32_projector",
        exact_zero(projector * projector - projector) and projector.rank() == 4,
        "the right-acting spatial spin-3/2 projector is idempotent with complex rank four",
    )
    generic_lambda = sp.Matrix([[sp.Symbol("lambda_1"), sp.Symbol("lambda_2")]])
    gamma_trace_candidate = sp.Matrix.hstack(
        *(generic_lambda * gamma_i for gamma_i in gamma)
    )
    audit.check(
        "P16.spin32_candidate_kernel",
        exact_zero(gamma_trace_candidate * projector),
        "a pure spatial gamma-trace gravitino is annihilated by P_3/2",
    )

    sigma = [-gamma_i for gamma_i in gamma]
    epsilon_row = sp.Matrix([[1, 0]])
    chi_row = sp.Matrix([[1, 0]])
    chibar_column = sp.Matrix([[1], [0]])
    vector_bilinear = [
        sp.simplify((chi_row * sigma_i * chibar_column)[0])
        for sigma_i in sigma
    ]
    audit.check(
        "P16.clean_spinor_bilinear",
        vector_bilinear == [0, 0, 1],
        "the chi^1 chibar^dot1 coefficient is the exact spatial vector (0,0,1)",
    )

    # CPN.85 at b=M=psi=dA=0 contains
    # delta b_i=(F epsilon sigma_i chibar + Fbar epsilonbar barsigma_i chi)/sqrt(2).
    b3_coefficient = sp.simplify(
        (epsilon_row * sigma[2] * chibar_column)[0] / sp.sqrt(2)
    )
    audit.check(
        "P16.off_shell_b_i_obstruction",
        b3_coefficient == 1 / sp.sqrt(2),
        "delta b_3 has the nonzero F epsilon^1 chibar^dot1 coefficient 1/sqrt(2)",
    )

    # CPN.40 and CPN.75 at the same clean point give
    # delta psi_i=(i/2)(chi sigma_i chibar) epsilon.
    delta_psi = sp.Matrix.hstack(
        *(
            sp.I * sp.Rational(1, 2) * component * epsilon_row
            for component in vector_bilinear
        )
    )
    rho_residual = sp.simplify(delta_psi * projector)
    expected_rho = sp.Matrix(
        [[0, -sp.I / 6, 0, -sp.Rational(1, 6), sp.I / 3, 0]]
    )
    audit.check(
        "P16.spin32_obstruction",
        exact_zero(rho_residual - expected_rho) and not exact_zero(rho_residual),
        "the chi^1 chibar^dot1 epsilon^1 coefficient has a nonzero P_3/2 projection",
    )
    gamma_trace = sp.zeros(1, 2)
    for i in range(3):
        gamma_trace += rho_residual[:, 2 * i : 2 * i + 2] * gamma[i]
    audit.check(
        "P16.spin32_residual_trace",
        exact_zero(gamma_trace),
        "the nonzero residual is gamma-traceless, so it is a genuine discarded spin-3/2 mode",
    )

    # A complementary bosonic-background check uses CPN.93.  On the W=0
    # auxiliary equation F=0, with psi=chi=0 and a real homogeneous rolling
    # scalar, delta chi is an invertible linear map of the barred SUSY
    # parameter.  This is a Killing-spinor/background-invariance statement,
    # not a loss of the underlying local gauge symmetry.
    proper_clock_rate = sp.Symbol("D_tau_A", real=True, nonzero=True)
    epsilon_lower = sp.Matrix([[0, -1], [1, 0]])
    clock_susy_map = sp.I * sp.sqrt(2) * proper_clock_rate * epsilon_lower
    audit.check(
        "P16.rolling_clock_no_residual_susy",
        clock_susy_map.rank() == 2
        and exact_zero(clock_susy_map.det() + 2 * proper_clock_rate**2),
        "for W=0, F=0 and nonzero real clock rate, delta chi=0 has only the zero SUSY parameter",
    )

    result: dict[str, object] = {
        "source": SOURCE,
        "exact_checks": audit.passed,
        "bosonic_kinetic_parent": {
            "status": "PASS",
            "scope": "the (X,T,Y) velocity subblock after the one endpoint; lapse and algebraic auxiliary constraints are not included",
            "curvature": sp.sstr(R_bgg),
            "curvature_over_Q": -6,
            "raw_gravity": sp.sstr(L_gravity_raw),
            "boundary_identity": "L_EH_raw = dot(B) - 3 C",
            "first_order_lagrangian": sp.sstr(L_first),
            "hessian": sp.sstr(hessian),
            "rank": 3,
            "determinant": sp.sstr(hessian.det()),
            "inertia_negative_zero_positive": [1, 0, 2],
            "kinetic_hamiltonian": sp.sstr(Hamiltonian),
            "lapse_primary_constraint": "p_N=0",
        },
        "specified_off_shell_flrw_gamma_trace_tangency": {
            "status": "FAIL_BY_EXACT_CLEAN_POINT_COUNTEREXAMPLE",
            "scope": "analyst-defined discarded normals e_i^a b_a=0 and P_3/2 psi=0, BGG source b_a, arbitrary homogeneous complexified Grassmann chi/chibar, F/Fbar, and SUSY parameters",
            "b3_monomial": "F epsilon^1 chibar^dot1",
            "b3_coefficient": sp.sstr(b3_coefficient),
            "rho_monomial": "chi^1 chibar^dot1 epsilon^1",
            "rho_coefficient_vector": [sp.sstr(value) for value in rho_residual],
            "reason": "CPN.85 excites the constructed spatial projection b_i=e_i^a b_a and independently CPN.40+CPN.75+CPN.77 excite a discarded spin-3/2 mode",
        },
        "rolling_chiral_clock_background": {
            "status": "NO_NONZERO_PRESERVED_SUSY_PARAMETER",
            "scope": "bosonic W=0 on-shell auxiliary slice F=0 with nonzero real homogeneous proper-time rate D_tau A=N^-1 dA/dt and Lorentzian-conjugate SUSY parameters",
            "delta_chi_parameter_map_rank": 2,
            "interpretation": "with Lorentzian conjugate SUSY parameters the background is not SUSY-invariant; the underlying local gauge symmetry is not removed",
        },
        "scope_guard": {
            "full_4d_local_susy": "NOT_REFUTED",
            "other_bosonic_or_killing_spinor_subslices": "NOT_TESTED",
            "shifted_auxiliary_basis": "NOT_TESTED",
            "temporal_branch_supercharge": "NOT_TESTED",
            "full_all_fermion_residual": "NOT_COMPUTED; exact clean-point counterexamples suffice for the scoped tangency failure",
            "tangency_engine": "NOT_A_FULL_CPN_TRANSCRIPTION; it evaluates surviving BGG coefficients at one exact point of the specified truncation",
        },
    }
    print("PHASE16_RESULT=" + json.dumps(result, sort_keys=True, ensure_ascii=False))
    return result


if __name__ == "__main__":
    run()
