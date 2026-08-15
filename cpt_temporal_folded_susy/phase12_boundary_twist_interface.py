#!/usr/bin/env python3
"""Phase 12 — boundary-twist theorem and endpoint-covariant N=1 witness.

This executable has two deliberately separate layers.

P12A is an exact finite-canonical theorem.  For

    S = integral [p.qdot - N C - a(u) J] du,

an autonomous Hamiltonian generator J with {C,J}=0 is removable from the
open-interval bulk by its time-dependent Hamiltonian flow.  The operation is
not automatically a gauge transformation: it transports the endpoint
polarization and leaves an endpoint symplectic twist and, in general, a
boundary generating function.  The weak dilation {C,J}=-2C is covered only
after the lapse is rescaled.

P12B is a conditional interface existence witness in a 4D rigid N=1
Wess-Zumino parent.  A BPS-wall chiral field Phi and a spectator flavor
doublet Z have a holomorphic rotating mass matrix.  The selected quadratic
reduction transports the scalar and Weyl-fermion flavor indices with the same
kinematic frame connection, while the scalar differential expressions have
the expected formal supersymmetric-QM factorization.  Given external oriented
endpoint data, a reduced open frame component is basis-invariant; the formal
bulk source selectors below do not construct a localized endpoint detector.
An Eto-Sakai-type matter-coupled SUGRA candidate receives only one partial
algebraic P12C check here.  This does NOT construct a rank-changing temporal
seam, prove local-SUGRA/BV/BFV closure, exchange bosons with fermions, derive
kappa=pi/2, or show that SUSY is pre-Big-Bang time.

Contract: PHASE12_RESEARCH_CONTRACT.json (POST_HOC; no confirmation label).
Verification:
    uv run --with sympy python3 phase12_boundary_twist_interface.py
"""

from __future__ import annotations

import sys
from collections.abc import Callable

import sympy as sp


class Audit:
    """Small exact-check recorder; no tolerance or numerical fallback."""

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


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def poisson(
    f: sp.Expr,
    g: sp.Expr,
    qs: list[sp.Symbol],
    ps: list[sp.Symbol],
) -> sp.Expr:
    return sp.expand(
        sum(
            sp.diff(f, q) * sp.diff(g, p)
            - sp.diff(f, p) * sp.diff(g, q)
            for q, p in zip(qs, ps)
        )
    )


def rotation(angle: sp.Expr) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.cos(angle), -sp.sin(angle)],
            [sp.sin(angle), sp.cos(angle)],
        ]
    )


def part_a_general_generators(audit: Audit) -> None:
    """General Phase-11 strong and weak generator identities."""
    b1, b2, r, c = sp.symbols("b1 b2 r c", real=True)
    d00, d01, d02, d11, d12, d22 = sp.symbols(
        "d00 d01 d02 d11 d12 d22", real=True
    )
    eta = sp.diag(-1, 1, 1)
    m_strong = sp.Matrix(
        [
            [0, b1, b2],
            [b1, 0, r],
            [b2, -r, 0],
        ]
    )
    d_symmetric = sp.Matrix(
        [
            [d00, d01, d02],
            [d01, d11, d12],
            [d02, d12, d22],
        ]
    )

    omega = sp.zeros(6, 6)
    omega[0:3, 3:6] = sp.eye(3)
    omega[3:6, 0:3] = -sp.eye(3)
    constraint_form = sp.zeros(6, 6)
    constraint_form[3:6, 3:6] = eta

    def flow_generator(m_block: sp.Matrix) -> sp.Matrix:
        hessian = sp.zeros(6, 6)
        hessian[0:3, 3:6] = m_block
        hessian[3:6, 0:3] = m_block.T
        hessian[3:6, 3:6] = d_symmetric
        return omega * hessian

    k_strong = flow_generator(m_strong)
    audit.check(
        "P12A.general.hamiltonian",
        zero_matrix(k_strong.T * omega + omega * k_strong),
        "the entire M in so(1,2), D symmetric class generates a symplectic flow",
    )
    audit.check(
        "P12A.general.constraint",
        zero_matrix(k_strong.T * constraint_form + constraint_form * k_strong),
        "the entire strong class preserves the Bianchi-I quadratic constraint",
    )

    m_weak = m_strong + c * sp.eye(3)
    k_weak = flow_generator(m_weak)
    weak_residual = sp.simplify(
        k_weak.T * constraint_form + constraint_form * k_weak
        + 2 * c * constraint_form
    )
    audit.check(
        "P12A.general.weak",
        zero_matrix(weak_residual),
        "the Phase-11-classified extension M_strong+cI gives {C,J}=-2c C",
    )

    q = sp.Matrix(sp.symbols("q0 q1 q2", real=True))
    p = sp.Matrix(sp.symbols("p0 p1 p2", real=True))
    dq = sp.Matrix(sp.symbols("dq0 dq1 dq2", real=True))
    dp = sp.Matrix(sp.symbols("dp0 dp1 dp2", real=True))
    x_p = -m_strong * p
    d_x_q = m_strong.T * dq + d_symmetric * dp
    lie_canonical_one_form = sp.expand((x_p.T * dq)[0] + (p.T * d_x_q)[0])
    endpoint_density = sp.expand((p.T * d_symmetric * p)[0] / 2)
    d_endpoint_density = sp.expand(
        sum(sp.diff(endpoint_density, p[i]) * dp[i] for i in range(3))
    )
    audit.check(
        "P12A.general.one_form_lie_derivative",
        sp.simplify(lie_canonical_one_form - d_endpoint_density) == 0,
        "for arbitrary allowed M and symmetric D, L_X(p.dq)=d[p^T D p/2], yielding the integrated boundary F",
    )


def part_a_rotation_profile(audit: Audit) -> None:
    """Phase-7 rotation: exact one-form identity and profile-only holonomy."""
    theta, theta_dot = sp.symbols("theta theta_dot", real=True)
    qp, qm, pp, pm = sp.symbols("Q_p Q_m P_p P_m", real=True)
    qpd, qmd, ppd, pmd = sp.symbols(
        "Qdot_p Qdot_m Pdot_p Pdot_m", real=True
    )
    q = sp.Matrix([qp, qm])
    p = sp.Matrix([pp, pm])
    qdot = sp.Matrix([qpd, qmd])
    pdot = sp.Matrix([ppd, pmd])
    del pdot  # the cotangent rotation identity does not need Pdot

    rot = rotation(theta)
    b = sp.Matrix([[0, -1], [1, 0]])
    audit.check(
        "P12A.rotation.connection",
        zero_matrix(rot.T * sp.diff(rot, theta) - b),
        "R(theta)^T dR/dtheta is exactly the beta-plane generator B",
    )

    old_qdot = rot * qdot + theta_dot * sp.diff(rot, theta) * q
    old_p = rot * p
    h_sigma = sp.expand((p.T * b * q)[0])
    kinetic_residual = sp.simplify(
        (old_p.T * old_qdot)[0]
        - (p.T * qdot)[0]
        - theta_dot * h_sigma
    )
    audit.check(
        "P12A.rotation.one_form",
        kinetic_residual == 0,
        "p.dq=P.dQ+H_Sigma dtheta with no extra boundary generator for D=0",
    )
    audit.check(
        "P12A.rotation.generator",
        sp.simplify(h_sigma - (pm * qp - pp * qm)) == 0,
        "the connection is exactly Phase 7 H_Sigma=P_m Q_p-P_p Q_m",
    )
    audit.check(
        "P12A.rotation.constraint",
        sp.simplify((old_p.T * old_p)[0] - (p.T * p)[0]) == 0,
        "the rotation leaves the anisotropy momentum norm unchanged",
    )

    u = sp.symbols("u", real=True)
    delta, kappa = sp.symbols("delta kappa", real=True, positive=True)
    rho_cos = (1 + sp.cos(sp.pi * u / delta)) / (2 * delta)
    rho_poly = sp.Rational(15, 16) * (1 - (u / delta) ** 2) ** 2 / delta
    int_cos = sp.integrate(rho_cos, (u, -delta, delta))
    int_poly = sp.integrate(rho_poly, (u, -delta, delta))
    c1_endpoints = all(
        sp.simplify(expr) == 0
        for expr in (
            rho_cos.subs(u, -delta),
            rho_cos.subs(u, delta),
            sp.diff(rho_cos, u).subs(u, -delta),
            sp.diff(rho_cos, u).subs(u, delta),
            rho_poly.subs(u, -delta),
            rho_poly.subs(u, delta),
            sp.diff(rho_poly, u).subs(u, -delta),
            sp.diff(rho_poly, u).subs(u, delta),
        )
    )
    audit.check(
        "P12A.profile.normalized",
        sp.simplify(int_cos - 1) == 0
        and sp.simplify(int_poly - 1) == 0
        and c1_endpoints,
        "two different zero-extended C1 collar shapes have the same unit integral",
    )
    audit.check(
        "P12A.profile.endpoint_twist",
        sp.simplify(kappa * int_cos - kappa * int_poly) == 0,
        "equal integrated coupling gives the same endpoint angle kappa",
    )


def part_a_shear_and_boundary(audit: Audit) -> None:
    """Momentum shear: the necessary nonzero boundary generating function."""
    theta, theta_dot = sp.symbols("theta theta_dot", real=True)
    qp, qm, pp, pm = sp.symbols("Q_p Q_m P_p P_m", real=True)
    qpd, qmd, ppd, pmd = sp.symbols(
        "Qdot_p Qdot_m Pdot_p Pdot_m", real=True
    )
    q = sp.Matrix([qp, qm])
    p = sp.Matrix([pp, pm])
    qdot = sp.Matrix([qpd, qmd])
    pdot = sp.Matrix([ppd, pmd])
    d = sp.Matrix([[0, 1], [1, 0]])
    j_shear = sp.expand((p.T * d * p)[0] / 2)
    boundary_f = sp.expand(theta * j_shear)
    boundary_f_dot = sp.expand(
        sp.diff(boundary_f, theta) * theta_dot
        + sp.diff(boundary_f, pp) * ppd
        + sp.diff(boundary_f, pm) * pmd
    )
    old_qdot = qdot + theta_dot * d * p + theta * d * pdot
    one_form_residual = sp.expand(
        (p.T * old_qdot)[0]
        - (p.T * qdot)[0]
        - theta_dot * j_shear
        - boundary_f_dot
    )
    audit.check(
        "P12A.shear.one_form",
        one_form_residual == 0,
        "cross-shear obeys p.dq=P.dQ+J_shear dtheta+d(theta J_shear)",
    )
    audit.check(
        "P12A.shear.constraint",
        j_shear == pp * pm
        and sp.simplify(
            poisson(
                (pp**2 + pm**2) / 2,
                j_shear,
                [qp, qm],
                [pp, pm],
            )
        )
        == 0,
        "the cross-shear Poisson-commutes with the momentum-only constraint",
    )
    audit.reject(
        "P12A.mutant.shear_boundary_omitted",
        sp.simplify(boundary_f_dot) != 0,
        "omitting the D-dependent endpoint generating function leaves dF/du",
    )
    delta_p = sp.Matrix(sp.symbols("delta_Pp delta_Pm", real=True))
    transported_endpoint = sp.simplify(theta * d * delta_p)
    delta_q_transported = -transported_endpoint
    delta_boundary_f = sp.simplify(theta * (p.T * d * delta_p)[0])
    boundary_variation = sp.simplify(
        (p.T * delta_q_transported)[0] + delta_boundary_f
    )
    audit.check(
        "P12A.shear.endpoint_polarization",
        boundary_variation == 0,
        "delta Q=-theta D delta P cancels P.delta Q against delta F at the endpoint",
    )
    audit.reject(
        "P12A.mutant.endpoint_polarization",
        transported_endpoint != sp.zeros(2, 1),
        "fixed old q is not fixed Q: delta Q+theta D delta P=0 must be transported",
    )


def part_a_boost_and_bad_generators(audit: Audit) -> None:
    """Representative boost plus two non-invariant negative fixtures."""
    theta, theta_dot = sp.symbols("theta theta_dot", real=True)
    qa, qp, pa, pp = sp.symbols("Q_a Q_p P_a P_p", real=True)
    qad, qpd = sp.symbols("Qdot_a Qdot_p", real=True)
    q = sp.Matrix([qa, qp])
    p = sp.Matrix([pa, pp])
    qdot = sp.Matrix([qad, qpd])
    eta = sp.diag(-1, 1)
    boost = sp.Matrix(
        [
            [sp.cosh(theta), sp.sinh(theta)],
            [sp.sinh(theta), sp.cosh(theta)],
        ]
    )
    boost_inv = boost.subs(theta, -theta)
    a = sp.Matrix([[0, 1], [1, 0]])
    old_qdot = boost * qdot + theta_dot * sp.diff(boost, theta) * q
    old_p = boost_inv * p
    j_boost = sp.expand((p.T * a * q)[0])
    audit.check(
        "P12A.boost.one_form",
        sp.simplify(
            (old_p.T * old_qdot)[0]
            - (p.T * qdot)[0]
            - theta_dot * j_boost
        )
        == 0,
        "the alpha-beta boost collar is also an endpoint cotangent lift",
    )
    audit.check(
        "P12A.boost.constraint",
        sp.simplify((old_p.T * eta * old_p)[0] - (p.T * eta * p)[0]) == 0,
        "the boost preserves the Lorentzian minisuperspace momentum form",
    )

    qpm, qmm, ppm, pmm = sp.symbols("q_p q_m p_p p_m", real=True)
    qs = [qpm, qmm]
    ps = [ppm, pmm]
    pa_mutant = sp.symbols("p_alpha_mutant", real=True)
    c_free = sp.Rational(1, 2) * (ppm**2 + pmm**2)
    c_lorentzian = sp.Rational(1, 2) * (
        -pa_mutant**2 + ppm**2 + pmm**2
    )
    j_bad = qpm * pmm + qmm * ppm
    bad_bracket = poisson(c_free, j_bad, qs, ps)
    bad_on_shell = {
        qpm: 0,
        qmm: 0,
        pa_mutant: 5,
        ppm: 3,
        pmm: 4,
    }
    audit.reject(
        "P12A.mutant.symmetric_squeezer",
        sp.simplify(bad_bracket + 2 * ppm * pmm) == 0
        and c_lorentzian.subs(bad_on_shell) == 0
        and bad_bracket.subs(bad_on_shell) == -24,
        "the symmetric pair squeezer is nonzero on C=0, so it is neither strong nor projectively first-class",
    )

    wp, wm = sp.symbols("omega_p omega_m", real=True, positive=True)
    c_unequal = c_lorentzian + sp.Rational(1, 2) * (
        wp**2 * qpm**2 + wm**2 * qmm**2
    )
    j_rotation = pmm * qpm - ppm * qmm
    unequal_bracket = poisson(c_unequal, j_rotation, qs, ps)
    expected = qpm * qmm * (wm**2 - wp**2)
    unequal_on_shell = {
        qpm: 1,
        qmm: 1,
        pa_mutant: sp.sqrt(5),
        ppm: 0,
        pmm: 0,
        wp: 1,
        wm: 2,
    }
    audit.reject(
        "P12A.mutant.unequal_frequency",
        sp.simplify(unequal_bracket - expected) == 0
        and c_unequal.subs(unequal_on_shell) == 0
        and unequal_bracket.subs(unequal_on_shell) == 3,
        "the unequal-frequency bracket is nonzero on C_omega=0 and blocks projective bulk equivalence",
    )


def part_a_weak_dilation(audit: Audit) -> None:
    """Weak removal is off-shell only with the lapse redefinition."""
    theta, theta_dot = sp.symbols("theta theta_dot", real=True)
    q_symbols = sp.symbols("Q0 Q1 Q2", real=True)
    p_symbols = sp.symbols("P0 P1 P2", real=True)
    qdot_symbols = sp.symbols("Qdot0 Qdot1 Qdot2", real=True)
    q = sp.Matrix(q_symbols)
    p = sp.Matrix(p_symbols)
    qdot = sp.Matrix(qdot_symbols)
    old_q = sp.exp(theta) * q
    old_p = sp.exp(-theta) * p
    old_qdot = sp.exp(theta) * (qdot + theta_dot * q)
    j_dil = sp.expand((p.T * q)[0])
    audit.check(
        "P12A.dilation.one_form",
        sp.simplify(
            (old_p.T * old_qdot)[0]
            - (p.T * qdot)[0]
            - theta_dot * j_dil
        )
        == 0,
        "dilation gives p.dq=P.dQ+(P.Q)dtheta",
    )
    eta = sp.diag(-1, 1, 1)
    c_new = sp.expand((p.T * eta * p)[0] / 2)
    c_old = sp.expand((old_p.T * eta * old_p)[0] / 2)
    audit.check(
        "P12A.dilation.constraint_scale",
        sp.simplify(c_old - sp.exp(-2 * theta) * c_new) == 0,
        "C scales by exp(-2 theta), matching {C,q.p}=-2C",
    )
    lapse = sp.symbols("N", real=True)
    lapse_new = lapse * sp.exp(-2 * theta)
    audit.check(
        "P12A.dilation.lapse",
        sp.simplify(-lapse * c_old + lapse_new * c_new) == 0,
        "N_new=N exp(-2 theta) restores the ordinary off-shell bulk constraint term",
    )
    no_rescale_residual = sp.simplify(-lapse * c_old + lapse * c_new)
    audit.reject(
        "P12A.mutant.dilation_lapse_omitted",
        no_rescale_residual != 0,
        "without lapse rescaling the transformed bulk action is not the baseline action",
    )


def part_b_parent_mass_and_connection(audit: Audit) -> None:
    """Holomorphic spectator mass family and matched component connection."""
    phi = sp.symbols("Phi")
    v = sp.symbols("v", real=True, positive=True)
    kappa = sp.symbols("kappa", real=True)
    m1, m2 = sp.symbols("m1 m2", real=True, nonzero=True)
    theta = sp.simplify(kappa * (phi + v) / (2 * v))
    rot = rotation(theta)
    b = sp.Matrix([[0, -1], [1, 0]])
    mass = sp.simplify(rot * sp.diag(m1, m2) * rot.T)

    audit.check(
        "P12B.parent.rotation",
        zero_matrix(rot.T * rot - sp.eye(2))
        and sp.simplify(rot.det() - 1) == 0,
        "R is in SO(2,C) holomorphically and restricts to SO(2) on the real wall slice",
    )
    audit.check(
        "P12B.parent.mass_symmetric",
        zero_matrix(mass - mass.T),
        "M(Phi)=R diag(m1,m2) R^T is a symmetric holomorphic superpotential mass",
    )
    audit.check(
        "P12B.parent.endpoints",
        zero_matrix(mass.subs(phi, -v) - sp.diag(m1, m2))
        and zero_matrix(
            mass.subs({phi: v, kappa: sp.pi / 2}) - sp.diag(m2, m1)
        ),
        "the selected kappa=pi/2 input swaps the two asymptotic mass axes",
    )

    wall_coordinate, coupling = sp.symbols("z lambda", real=True, positive=True)
    wall_profile = v * sp.tanh(coupling * v * wall_coordinate)
    wall_rhs = coupling * (v**2 - wall_profile**2)
    wall_equation = sp.simplify(sp.diff(wall_profile, wall_coordinate) - wall_rhs)
    f_endpoint_minus = sp.simplify(coupling * (v**2 - (-v) ** 2))
    f_endpoint_plus = sp.simplify(coupling * (v**2 - v**2))
    audit.check(
        "P12B.parent.rigid_bps_wall",
        wall_equation == 0
        and sp.limit(wall_profile, wall_coordinate, -sp.oo) == -v
        and sp.limit(wall_profile, wall_coordinate, sp.oo) == v
        and f_endpoint_minus == 0
        and f_endpoint_plus == 0,
        "Phi=v tanh(lambda v z), Z=0 solves Phi'=lambda(v^2-Phi^2) and reaches F-flat vacua",
    )

    z1, z2 = sp.symbols("Z1 Z2")
    z = sp.Matrix([z1, z2])
    w_spectator = sp.expand((z.T * mass * z)[0] / 2)
    zero_subs = {z1: 0, z2: 0}
    spectator_decouples = (
        sp.simplify(w_spectator.subs(zero_subs)) == 0
        and sp.simplify(sp.diff(w_spectator, z1).subs(zero_subs)) == 0
        and sp.simplify(sp.diff(w_spectator, z2).subs(zero_subs)) == 0
        and sp.simplify(sp.diff(w_spectator, phi).subs(zero_subs)) == 0
        and sp.simplify(
            sp.diff(w_spectator, phi, z1).subs(zero_subs)
        )
        == 0
        and sp.simplify(
            sp.diff(w_spectator, phi, z2).subs(zero_subs)
        )
        == 0
    )
    audit.check(
        "P12B.parent.spectator_background",
        spectator_decouples,
        "at Z=0 the spectator sector changes neither the wall equations nor the mixed W_PhiZi block",
    )

    source_minus, source_plus = sp.symbols("j_minus j_plus")
    n_minus_1, n_minus_2, n_plus_1, n_plus_2 = sp.symbols(
        "n_minus_1 n_minus_2 n_plus_1 n_plus_2"
    )
    h_minus = sp.simplify((1 - phi / v) / 2)
    h_plus = sp.simplify((1 + phi / v) / 2)
    delta_w_source = sp.expand(
        source_minus
        * h_minus
        * (n_minus_1 * z1 + n_minus_2 * z2)
        + source_plus * h_plus * (n_plus_1 * z1 + n_plus_2 * z2)
    )
    source_support = (
        h_minus.subs(phi, -v) == 1
        and h_minus.subs(phi, v) == 0
        and h_plus.subs(phi, -v) == 0
        and h_plus.subs(phi, v) == 1
    )
    source_off = sp.simplify(
        delta_w_source.subs({source_minus: 0, source_plus: 0})
    )
    audit.check(
        "P12B.parent.formal_source_selectors",
        source_support and source_off == 0,
        "formal chiral bulk selectors take complementary endpoint values and j_plus=j_minus=0 leaves the parent unchanged",
    )

    degenerate_mass = sp.simplify(mass.subs(m2, m1) - m1 * sp.eye(2))
    audit.reject(
        "P12B.mutant.degenerate_endpoint_frame",
        zero_matrix(degenerate_mass),
        "m1=m2 erases all theta-dependence and cannot anchor a flavor eigenframe",
    )

    zb1, zb2 = sp.symbols("Zbar1 Zbar2")
    kahler_spectator = z1 * zb1 + z2 * zb2
    kahler_metric = sp.Matrix(
        2,
        2,
        lambda i, j: sp.diff(
            sp.diff(kahler_spectator, [z1, z2][i]), [zb1, zb2][j]
        ),
    )
    audit.check(
        "P12B.parent.kahler_metric",
        kahler_metric == sp.eye(2),
        "the spectator flavor sector has a positive canonical Kahler metric",
    )

    theta_symbol = sp.symbols("theta", real=True)
    component_rot = rotation(theta_symbol)
    connection = sp.simplify(
        component_rot.T * sp.diff(component_rot, theta_symbol)
    )
    audit.check(
        "P12B.components.matched_connection",
        zero_matrix(connection - b),
        "scalar canonical variables and Weyl-fermion flavor indices inherit the same kinematic B",
    )
    theta_prime = sp.symbols("Theta_prime", real=True)
    flavor_connection = theta_prime * b
    audit.check(
        "P12B.components.real_slice_connection",
        zero_matrix(flavor_connection.H + flavor_connection)
        and zero_matrix(component_rot.H * component_rot - sp.eye(2)),
        "on the selected real slice A_z=Theta_prime B is anti-Hermitian and R is unitary",
    )


def part_b_quadratic_factorization(audit: Audit) -> None:
    """Exact rigid scalar differential factorization along a real wall."""
    wall_coordinate = sp.symbols("z", real=True)
    mass_11 = sp.Function("m_11", real=True)(wall_coordinate)
    mass_12 = sp.Function("m_12", real=True)(wall_coordinate)
    mass_22 = sp.Function("m_22", real=True)(wall_coordinate)
    mass = sp.Matrix([[mass_11, mass_12], [mass_12, mass_22]])
    test_field = sp.Matrix(
        [
            sp.Function("f_1", real=True)(wall_coordinate),
            sp.Function("f_2", real=True)(wall_coordinate),
        ]
    )

    def d_operator(field: sp.Matrix) -> sp.Matrix:
        return sp.diff(field, wall_coordinate) + mass * field

    def d_adjoint_operator(field: sp.Matrix) -> sp.Matrix:
        return -sp.diff(field, wall_coordinate) + mass * field

    def h_plus(field: sp.Matrix) -> sp.Matrix:
        return (
            -sp.diff(field, wall_coordinate, 2)
            + (mass * mass + sp.diff(mass, wall_coordinate)) * field
        )

    def h_minus(field: sp.Matrix) -> sp.Matrix:
        return (
            -sp.diff(field, wall_coordinate, 2)
            + (mass * mass - sp.diff(mass, wall_coordinate)) * field
        )

    x1, x2, y1, y2 = sp.symbols("x_1 x_2 y_1 y_2", real=True)
    mass_phi_11, mass_phi_12, mass_phi_22 = sp.symbols(
        "M_Phi_11 M_Phi_12 M_Phi_22", real=True
    )
    phi_prime = sp.symbols("Phi_prime", real=True)
    mass_phi = sp.Matrix(
        [[mass_phi_11, mass_phi_12], [mass_phi_12, mass_phi_22]]
    )
    x_field = sp.Matrix([x1, x2])
    y_field = sp.Matrix([y1, y2])
    complex_field = (x_field + sp.I * y_field) / sp.sqrt(2)
    conjugate_field = (x_field - sp.I * y_field) / sp.sqrt(2)
    fz_quadratic = (mass * conjugate_field).T * (mass * complex_field)
    fphi_cross = (
        phi_prime
        * (
            (complex_field.T * mass_phi * complex_field)[0]
            + (conjugate_field.T * mass_phi * conjugate_field)[0]
        )
        / 2
    )
    scalar_potential = sp.expand(fz_quadratic[0] + fphi_cross)
    expected_scalar_potential = sp.expand(
        (
            x_field.T
            * (mass * mass + phi_prime * mass_phi)
            * x_field
        )[0]
        / 2
        + (
            y_field.T
            * (mass * mass - phi_prime * mass_phi)
            * y_field
        )[0]
        / 2
    )
    audit.check(
        "P12B.quadratic.superpotential_hessian",
        sp.simplify(scalar_potential - expected_scalar_potential) == 0,
        "the same W gives V2=x^T(M^2+M_z')x/2+y^T(M^2-M_z')y/2 when M_z'=Phi' M_Phi",
    )

    audit.check(
        "P12B.quadratic.factorization",
        zero_matrix(d_operator(d_adjoint_operator(test_field)) - h_plus(test_field))
        and zero_matrix(
            d_adjoint_operator(d_operator(test_field)) - h_minus(test_field)
        ),
        "H_plus=D D_formal and H_minus=D_formal D as differential expressions for the two scalar sectors",
    )
    audit.check(
        "P12B.quadratic.intertwining",
        zero_matrix(d_operator(h_minus(test_field)) - h_plus(d_operator(test_field)))
        and zero_matrix(
            d_adjoint_operator(h_plus(test_field))
            - h_minus(d_adjoint_operator(test_field))
        ),
        "D H_minus=H_plus D and D_formal H_plus=H_minus D_formal exactly",
    )


def part_b_endpoint_flavor_identity(audit: Audit) -> None:
    """Selected homogeneous endpoint SUSY-variation flavor covariance."""
    theta_b, theta_f = sp.symbols("theta_b theta_f", real=True)
    rb = rotation(theta_b)
    rf = rotation(theta_f)
    grading = sp.diag(1, 1, -1, -1)
    matched_component_transport = sp.diag(1, 1, 1, 1)
    matched_component_transport[0:2, 0:2] = rb
    matched_component_transport[2:4, 2:4] = rb
    audit.check(
        "P12B.susy.parity_even",
        zero_matrix(
            grading * matched_component_transport
            - matched_component_transport * grading
        ),
        "the interface transports whole multiplets and does not exchange boson with fermion",
    )

    kappa = sp.symbols("kappa", real=True)
    m1, m2 = sp.symbols("m1 m2", real=True)
    u_endpoint = rotation(kappa)
    mass_minus = sp.diag(m1, m2)
    mass_plus = sp.simplify(u_endpoint * mass_minus * u_endpoint.T)
    bosonic_transport = sp.diag(1, 1, 1, 1)
    bosonic_transport[0:2, 0:2] = u_endpoint
    bosonic_transport[2:4, 2:4] = u_endpoint
    omega4 = sp.zeros(4, 4)
    omega4[0:2, 2:4] = sp.eye(2)
    omega4[2:4, 0:2] = -sp.eye(2)
    s_minus = sp.Matrix.hstack(sp.I * mass_minus, sp.eye(2))
    s_plus = sp.Matrix.hstack(sp.I * mass_plus, sp.eye(2))
    audit.check(
        "P12B.susy.endpoint_mass_covariance",
        zero_matrix(mass_plus * u_endpoint - u_endpoint * mass_minus)
        and zero_matrix(
            bosonic_transport.T * omega4 * bosonic_transport - omega4
        ),
        "M_plus U=U M_minus and diag(U,U) is canonical on endpoint bosonic phase data",
    )
    audit.check(
        "P12B.susy.endpoint_flavor_symbol",
        zero_matrix(s_plus * bosonic_transport - u_endpoint * s_minus),
        "S(M_plus) diag(U,U)=U S(M_minus) is the selected homogeneous endpoint flavor identity",
    )

    identity_fermion_mutant = sp.simplify(
        s_plus * bosonic_transport - sp.eye(2) * s_minus
    )
    audit.reject(
        "P12B.mutant.endpoint_boson_only",
        identity_fermion_mutant != sp.zeros(2, 4),
        "keeping the endpoint chiralino flavor fixed breaks the selected endpoint flavor identity",
    )

    mass_plus_mismatch = sp.simplify(rb * mass_minus * rb.T)
    bosonic_mismatch = sp.diag(1, 1, 1, 1)
    bosonic_mismatch[0:2, 0:2] = rb
    bosonic_mismatch[2:4, 2:4] = rb
    s_plus_mismatch = sp.Matrix.hstack(sp.I * mass_plus_mismatch, sp.eye(2))
    mismatch = sp.simplify(
        s_plus_mismatch * bosonic_mismatch - rf * s_minus
    )
    unequal_fixture = mismatch.subs(
        {
            theta_b: sp.pi / 2,
            theta_f: 0,
            m1: 1,
            m2: 2,
        }
    )
    audit.reject(
        "P12B.mutant.unequal_component_angles",
        unequal_fixture != sp.zeros(2, 4),
        "independent boson and fermion angles fail the selected endpoint flavor identity",
    )


def part_b_conditional_endpoint_covariance(audit: Audit) -> None:
    """Open transport is relational given external oriented endpoint data."""
    alpha_plus, alpha_minus, kappa = sp.symbols(
        "alpha_plus alpha_minus kappa", real=True
    )
    g_plus = rotation(alpha_plus)
    g_minus = rotation(alpha_minus)
    u_open = rotation(kappa)
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])
    u_transformed = sp.simplify(g_plus * u_open * g_minus.T)
    n_plus = g_plus * e1
    n_minus = g_minus * e1
    anchored = sp.simplify((e1.T * u_open * e1)[0])
    anchored_transformed = sp.trigsimp(
        (n_plus.T * u_transformed * n_minus)[0]
    )
    audit.check(
        "P12B.anchor.covariance",
        sp.trigsimp(anchored_transformed - anchored) == 0,
        "n_plus^T U n_minus is invariant under independent endpoint SO(2) bases",
    )
    audit.check(
        "P12B.anchor.nontrivial_channels",
        sp.trigsimp(anchored - sp.cos(kappa)) == 0
        and sp.trigsimp((e2.T * u_open * e1)[0] - sp.sin(kappa)) == 0,
        "oriented external-data frame components retain cos(kappa) and sin(kappa)",
    )
    audit.check(
        "P12B.anchor.unanchored_removable",
        zero_matrix(u_open.T * u_open - sp.eye(2)),
        "without anchors, choosing g_plus=U^T and g_minus=I sends the open U to identity",
    )
    co_moving_wilson_line = rotation(-kappa)
    audit.check(
        "P12B.anchor.transport_convention",
        zero_matrix(co_moving_wilson_line - u_open.T),
        "the fixed-frame endpoint map U=R_plus R_minus^{-1} is the inverse of the co-moving Wilson line",
    )
    anchors_held_fixed = sp.trigsimp(
        (e1.T * u_transformed * e1)[0] - anchored
    )
    witness = sp.simplify(
        anchors_held_fixed.subs(
            {alpha_plus: sp.pi / 2, alpha_minus: 0, kappa: 0}
        )
    )
    audit.reject(
        "P12B.mutant.anchors_not_transformed",
        witness == -1,
        "holding anchor coordinates fixed during a basis change makes the reduced frame component basis-dependent",
    )


def part_c_classical_sugra_template(audit: Audit) -> None:
    """One algebraic gate for an Eto-Sakai-type matter-coupled candidate."""
    phi, z1, z2 = sp.symbols("Phi Z1 Z2")
    v, coupling = sp.symbols("v lambda", nonzero=True)
    gravity, additive, kappa = sp.symbols("kappa_g a kappa")
    m1, m2 = sp.symbols("m1 m2")
    theta = kappa * (phi + v) / (2 * v)
    rot = rotation(theta)
    mass = sp.simplify(rot * sp.diag(m1, m2) * rot.T)
    z = sp.Matrix([z1, z2])
    w_wall = coupling * (v**2 * phi - phi**3 / 3)
    w_spectator = (z.T * mass * z)[0] / 2
    holomorphic_kahler = phi**2 + z1**2 + z2**2
    w_local = sp.exp(-gravity**2 * holomorphic_kahler / 2) * (
        w_wall + w_spectator + additive
    )
    z_fields = [z1, z2]
    local_hessian = sp.Matrix(
        2,
        2,
        lambda i, j: sp.diff(w_local, z_fields[i], z_fields[j]).subs(
            {z1: 0, z2: 0}
        ),
    )
    expected = sp.exp(-gravity**2 * phi**2 / 2) * (
        mass - gravity**2 * (w_wall + additive) * sp.eye(2)
    )
    audit.check(
        "P12C.template.local_mass_eigenframe",
        zero_matrix(local_hessian - expected),
        "the Eto-Sakai-type candidate adds only a common identity shift to the spectator holomorphic Hessian",
    )
    print(
        "[OPEN] P12C matter-coupled local-SUGRA candidate: physical fermion mass, "
        "warp/gravitino mixing, boundary domain, and full constraints were not checked."
    )


def run_part(label: str, fn: Callable[[Audit], None], audit: Audit) -> None:
    print(f"\n=== {label} ===")
    fn(audit)


def main() -> int:
    audit = Audit()
    run_part("P12A general strong/weak classes", part_a_general_generators, audit)
    run_part("P12A Phase-7 rotation and profile", part_a_rotation_profile, audit)
    run_part("P12A momentum shear and endpoint form", part_a_shear_and_boundary, audit)
    run_part("P12A boost and negative fixtures", part_a_boost_and_bad_generators, audit)
    run_part("P12A weak dilation", part_a_weak_dilation, audit)
    run_part("P12B 4D-parent template reduction", part_b_parent_mass_and_connection, audit)
    run_part("P12B rigid scalar differential factorization", part_b_quadratic_factorization, audit)
    run_part("P12B endpoint flavor identity", part_b_endpoint_flavor_identity, audit)
    run_part(
        "P12B conditional endpoint covariance",
        part_b_conditional_endpoint_covariance,
        audit,
    )
    run_part("P12C partial matter-coupled template", part_c_classical_sugra_template, audit)
    print(
        f"\nALL EXACT CHECKS PASSED: {audit.passed} positive checks; "
        f"{audit.mutants_rejected} semantic mutants rejected."
    )
    print(
        "SCOPE: finite bulk-equivalence theorem + conditional rigid internal-flavor "
        "N=1 interface witness; NOT a physical endpoint detector, temporal seam, "
        "or proof of pre-Big-Bang SUSY."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
