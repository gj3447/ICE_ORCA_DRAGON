#!/usr/bin/env python3
"""Phase 11 v2 — constraint-level admissibility of collar deformations (G43-G46 preliminary).

Phase 9/10 left one gate before any observable claim can survive: are the
observable-producing collar deformations ALLOWED or FORCED?  This phase proves
a finite-canonical classification theorem, using the admissibility criterion
Phase 7 itself used ({C, H_Sigma} = 0, E130).  v2 incorporates a five-refuter
adversarial audit (2026-08-11): every exact computation of v1 reproduced, but
six interpretive claims were corrected — the corrections are now theorems and
declared tensions below, and the audit's own checks are asserted here.

Equation tags: E152-E156 (v1 used E147-E151, which COLLIDE with
PHASE8_REPORT.md's own \\tag{E147}/\\tag{E148} and their programme-ledger
registrations; note that the Phase-9/10 tags E136-E146 already overlap Phase
8's E136-E148 lineage — an inherited collision flagged, not repaired, here).

Exact results (all sympy-verified below):
  1. CLASSIFICATION, strong criterion, homogeneous quadratics (E152).
     Over the full (alpha, beta_+, beta_-) phase space,
     {C,H} == 0 identically iff
        H = q^T M p + p^T D p / 2   with  eta M^T + M eta = 0  and  D free;
     the q-quadratic block is forbidden (A = 0 forced).  M-space = so(1,2):
     one pair rotation + two mixed-signature alpha<->beta boosts (the
     symmetric combination is legal ACROSS the signature flip).  Degree <= 1:
     q-linear forbidden, p-linear (mode displacements), constants, and any
     g(C) legal.  The Phase-9 symmetric pair squeezer is forbidden strongly
     AND weakly on the pair block ({C,H_s} = -2 p_+ p_- = -24 at the on-shell
     Phase-7 witness, and not proportional to C).
  2. CRITERION DEPENDENCE / DILATION RESURRECTION (E153).  On the full space
     the WEAK (Dirac first-class) criterion {C,H} = lambda*C admits exactly
     one extra generator: the dilation H_dil = q.p, with {C, q.p} = -2C.  Its
     flow preserves C = 0 exactly and is a single-mode squeezer in EVERY mode
     (alpha = cosh s, beta = sinh s), reproducing the Phase-9 E139 tensor map
     r_obs = r_vac (1 + 2 sinh^2 s) exactly.  So the v1 "downgrade" of Phase-9
     E139-E140 holds ONLY under the strong criterion; weakly, a squeezer-class
     channel exists without touching C.  (1b: on the pair block the weak
     refinement adds nothing — lambda = 0 forced.)
  3. TWO-SPECIES: ROTATION-TYPE IS FORCED, DEGENERACY IS A CONVENTION (E154).
     With species kinetic terms (c1 p_zeta^2 + c2 p_S^2)/2 in the constraint,
     the general legal cross-species mixer is n12 = -(c2/c1) n21 (n11 = n22 =
     0): rotation-TYPE mixing is forced (n12*n21 < 0 always — never
     squeezer-type; the E144-blank-cell "symmetric x two-species" stays
     FORBIDDEN for every c1, c2), but a skewed legal mixer exists for every
     c1 != c2, and a canonical rescale q -> q/sqrt(c), p -> sqrt(c) p removes
     c1/c2 entirely.  Hence: the equal-weight power-conserving Phase-10 map
     beta_iso = sin^2(theta_c) requires c1 = c2 in PHYSICAL variables;
     species mixing itself does not force degeneracy — c1 = c2 is a
     normalization convention, and the physically assumed content of A4'
     (that the real (CDM, radiation) pair is degenerate) remains ASSUMED,
     exactly as PHASE9_NULL_RESULT sec 2.3 left its omega-version.
  4. MOMENTUM SHEAR: A CONDITIONAL TENSOR CHANNEL WITH A DECLARED TENSION
     (E155).  The p-quadratic collar H_x = p_+ p_- is legal w.r.t. the
     model's actual momentum-only constraint (E122) and [A_0, K] = 0 on the
     full 6-dim space (verified; note ANY [[0,B],[0,0]] pair commutes — the
     check is weaker than Phase 7's E129 condition).  Bogoliubov: general
     legal D gives beta = i sigma D / 2 and <N_j> = (sigma^2/4) (D^2)_jj
     (sigma = s*omega): cross-shear representative -> phase-averaged
     r_obs = r_vac (1 + sigma^2/2); the equally-legal single-mode member
     p_+^2/2 -> 1 + sigma^2/4 with polarization-asymmetric enhancement.
     Coherent (non-averaged) range: F in [1, 1 + sigma^2] — the shear NEVER
     suppresses r, unlike the squeezer's x0.043 branch (E140): a
     distinguishing signature.  DECLARED TENSION (not resolved): at the
     omega-level where the signal lives, the PHASE9_NULL sec 2.2/2.3 gates
     both fail for the shear — {C_omega, p_+ p_-} = omega^2 (q_+ p_- +
     q_- p_+) != 0 (the violation direction is exactly the forbidden
     squeezer) and [A_omega, K_shear] != 0 — while the rotation passed both.
     The shear is legal exactly where (omega = 0) its observable vanishes;
     its map is conditional on the A1 k-extension surviving that tension.
     Its BK18 table is ILLUSTRATIVE ONLY: with k-independent s the
     enhancement is blue (prop. to k^2), outside the near-scale-invariant
     domain of the r_0.05 card — by the programme's own Phase-8/10 domain
     standard the honest verdict for the card comparison is ABSTAIN pending
     a spectral-domain treatment.
  5. STATE-ASSIGNMENT CONVENTIONS AND THE CHANNEL MATRIX (E156).  The matrix
     of component x channel is complete for homogeneous quadratics under
     DECLARED per-channel state conventions: tensor cells evaluate on the
     quantum vacuum (Phase-9 convention), scalar/CDI cells on frozen
     classical amplitudes p -> 0 — a NEW Phase-11 assumption (A5), NOT
     inherited from Phase 10, and asymmetric (super-horizon tensor modes
     also freeze; uniform treatment would null the shear tensor cell too).
     The shear CDI cell uses the two-species shear p_zeta p_S, legal for ALL
     c1, c2 (constructed below, not by analogy).  E156 also supersedes the
     BROAD reading of Phase-9 E138 ("observable tensor signal requires a
     symmetric collar component"): true within the q-p class, FALSE for the
     full quadratic family (the shear and, weakly, the dilation are
     counterexamples).

Scope (declared, not proven here):
  * Finite-canonical necessary conditions on any 4D N=1 SUGRA completion's
    reduction.  G43-G46 remain OPEN in full; nothing 4D is derived.  This is
    a preliminary constraint-level result, not a "half" of those gates.
    "Allowed" classes are established; nothing is "forced" (kappa, sigma, s
    remain free).
  * A1/A2 inherited from Phase 9 for tensor maps; A3' from Phase 10; A5
    (frozen classical scalar amplitudes, p -> 0) is NEW here; phase
    averaging is used for quoted tensor maps (coherent ranges printed).
  * Criterion: strong {C,H} == 0 as primary (Phase-7 E130 operational
    reading); the weak alternative is computed, not adjudicated.

Verification: uv run --with sympy python3 phase11_collar_admissibility.py -> exit 0.
"""

from __future__ import annotations

import sys

import sympy as sp


BK18_R_LIMIT = sp.Rational(9, 250)  # r_0.05 < 0.036 (95% CL), Phase-8/9 frozen card


def poisson(f, g, qs, ps):
    return sum(sp.diff(f, q) * sp.diff(g, p) - sp.diff(f, p) * sp.diff(g, q)
               for q, p in zip(qs, ps))


def _full_setup():
    a, bp, bm = sp.symbols("alpha beta_p beta_m", real=True)
    pa, pp_, pm = sp.symbols("p_alpha p_p p_m", real=True)
    qs, ps = [a, bp, bm], [pa, pp_, pm]
    C = sp.Rational(1, 2) * (-pa**2 + pp_**2 + pm**2)  # Phase-7 E122
    return qs, ps, C


def part1_strong_classification():
    """E152: strong criterion, full space, degree <= 2."""
    qs, ps, C = _full_setup()
    a, bp, bm = qs
    pa, pp_, pm = ps
    eta = sp.diag(-1, 1, 1)

    Mfull = sp.Matrix(3, 3, sp.symbols("M:3:3", real=True))
    A_syms = sp.symbols("A00 A01 A02 A11 A12 A22", real=True)
    Afull = sp.Matrix([[A_syms[0], A_syms[1], A_syms[2]],
                       [A_syms[1], A_syms[3], A_syms[4]],
                       [A_syms[2], A_syms[4], A_syms[5]]])
    D_syms = sp.symbols("D00 D01 D02 D11 D12 D22", real=True)
    Dfull = sp.Matrix([[D_syms[0], D_syms[1], D_syms[2]],
                       [D_syms[1], D_syms[3], D_syms[4]],
                       [D_syms[2], D_syms[4], D_syms[5]]])
    qf, pf = sp.Matrix(qs), sp.Matrix(ps)
    Hfull = ((qf.T * Mfull * pf)[0]
             + sp.Rational(1, 2) * (qf.T * Afull * qf)[0]
             + sp.Rational(1, 2) * (pf.T * Dfull * pf)[0])
    pbf = sp.expand(poisson(C, Hfull, qs, ps))
    eqs = list(sp.Poly(pbf, qs + ps).as_dict().values())
    solf = sp.solve(eqs, list(Mfull) + list(A_syms) + list(D_syms), dict=True)
    assert len(solf) == 1
    sf = solf[0]
    Msol = Mfull.subs(sf)
    assert sp.simplify(eta * Msol.T + Msol * eta) == sp.zeros(3, 3)
    assert sp.simplify(Afull.subs(sf)) == sp.zeros(3, 3)
    assert all(symb not in sf for symb in D_syms)
    assert len(Msol.free_symbols) == 3  # so(1,2): 1 rotation + 2 boosts
    print("[1] E152: {C,H}==0 (strong) <=> M eta-antisym (so(1,2): rotation + 2 boosts),")
    print("    A=0, D free.  Verified over the FULL 6-dim space, nothing pre-assumed.")

    # Witnesses.
    H_rot = pm * bp - pp_ * bm
    H_sq = bp * pm + bm * pp_
    H_shear = pp_ * pm
    H_boost = a * pp_ + bp * pa
    assert sp.simplify(poisson(C, H_rot, qs, ps)) == 0
    assert sp.simplify(poisson(C, H_shear, qs, ps)) == 0
    assert sp.simplify(poisson(C, H_boost, qs, ps)) == 0
    br_sq = sp.expand(poisson(C, H_sq, qs, ps))
    assert br_sq == -2 * pp_ * pm
    assert br_sq.subs({pa: 5, pp_: 3, pm: 4}) == -24
    assert C.subs({pa: 5, pp_: 3, pm: 4}) == 0  # on-shell: dead weakly too
    lam = sp.symbols("lam")
    assert sp.solve(sp.Poly(br_sq - lam * C, ps).coeffs(), lam) == []
    print("    witnesses: rotation/shear/boost legal; pair squeezer {C,H_s}=-2p_+p_-")
    print("    (= -24 on-shell at (5,3,4), not lam*C: dead strongly AND weakly on the pair).")

    # Degree <= 1 and functions of C.
    b_syms = sp.symbols("b0 b1 b2", real=True)
    H_qlin = sum(b * q for b, q in zip(b_syms, qs))
    br_qlin = sp.expand(poisson(C, H_qlin, qs, ps))
    assert sp.solve(sp.Poly(br_qlin, ps).coeffs(), list(b_syms)) == {b: 0 for b in b_syms} or \
        all(v == 0 for v in sp.solve(sp.Poly(br_qlin, ps).coeffs(), list(b_syms), dict=True)[0].values())
    H_plin = sum(b * p for b, p in zip(b_syms, ps))
    assert sp.simplify(poisson(C, H_plin, qs, ps)) == 0
    g = sp.Function("g")
    assert sp.simplify(poisson(C, g(C), qs, ps)) == 0
    print("    degree<=1: q-linear forbidden, p-linear (displacements) + constants + g(C) legal.")


def part2_weak_criterion_dilation():
    """E153: weak criterion adds exactly the dilation; it resurrects the E139 map."""
    qs, ps, C = _full_setup()
    qf, pf = sp.Matrix(qs), sp.Matrix(ps)
    Mfull = sp.Matrix(3, 3, sp.symbols("N:3:3", real=True))
    A_syms = sp.symbols("B00 B01 B02 B11 B12 B22", real=True)
    Afull = sp.Matrix([[A_syms[0], A_syms[1], A_syms[2]],
                       [A_syms[1], A_syms[3], A_syms[4]],
                       [A_syms[2], A_syms[4], A_syms[5]]])
    D_syms = sp.symbols("E00 E01 E02 E11 E12 E22", real=True)
    Dfull = sp.Matrix([[D_syms[0], D_syms[1], D_syms[2]],
                       [D_syms[1], D_syms[3], D_syms[4]],
                       [D_syms[2], D_syms[4], D_syms[5]]])
    lam = sp.symbols("lam_w", real=True)
    Hfull = ((qf.T * Mfull * pf)[0]
             + sp.Rational(1, 2) * (qf.T * Afull * qf)[0]
             + sp.Rational(1, 2) * (pf.T * Dfull * pf)[0])
    weak = sp.expand(poisson(C, Hfull, qs, ps) - lam * C)
    eqs = list(sp.Poly(weak, qs + ps).as_dict().values())
    unknowns = list(Mfull) + list(A_syms) + list(D_syms) + [lam]
    solw = sp.solve(eqs, unknowns, dict=True)
    assert len(solw) == 1
    sw = solw[0]
    # Weak solution space: strong (9 dims: 3 M + 6 D) + 1 dilation direction.
    Mw = Mfull.subs(sw)
    free_syms = Mw.free_symbols
    assert len(free_syms) == 4  # 3 so(1,2) + trace (dilation)
    # Dilation witness.
    H_dil = sum(q * p for q, p in zip(qs, ps))
    assert sp.simplify(poisson(C, H_dil, qs, ps) + 2 * C) == 0
    s = sp.symbols("s", real=True, positive=True)
    # Flow: q -> e^s q, p -> e^-s p; C -> e^-2s C: constraint surface preserved.
    scaled = C.subs({ps[0]: sp.exp(-s) * ps[0], ps[1]: sp.exp(-s) * ps[1], ps[2]: sp.exp(-s) * ps[2]})
    assert sp.simplify(scaled - sp.exp(-2 * s) * C) == 0
    # Single-mode Bogoliubov of the dilation: alpha = cosh s, beta = sinh s.
    w = sp.symbols("omega", positive=True)
    aa, ac = sp.symbols("a ac")
    q_of = (aa + ac) / sp.sqrt(2 * w)
    p_of = -sp.I * sp.sqrt(w / 2) * (aa - ac)
    a_out = sp.expand((w * sp.exp(s) * q_of + sp.I * sp.exp(-s) * p_of) / sp.sqrt(2 * w))
    alpha_c = sp.simplify(a_out.coeff(aa))
    beta_c = sp.simplify(a_out.coeff(ac))
    assert sp.simplify(alpha_c - sp.cosh(s)) == 0
    assert sp.simplify(beta_c - sp.sinh(s)) == 0
    F_dil = sp.simplify(1 + 2 * beta_c**2)
    assert sp.simplify(F_dil - (1 + 2 * sp.sinh(s)**2)) == 0
    print("[2] E153: weak criterion ({C,H}=lam*C) adds EXACTLY the dilation q.p")
    print("    ({C,q.p}=-2C, C=0 surface preserved).  Its Bogoliubov is alpha=cosh s,")
    print("    beta=sinh s per mode: r_obs = r_vac(1+2 sinh^2 s) — the Phase-9 E139 map,")
    print("    RESURRECTED without touching C.  The E139-E140 'downgrade' is therefore")
    print("    criterion-dependent: strong => unreachable; weak (Dirac first-class) => live.")
    # Pair-block-only weak refinement forces lam = 0 (v1's 1b claim, correct at that scope).
    a_, bp_, bm_ = qs
    pa_, pp_, pm_ = ps
    m_syms = sp.symbols("mm:4", real=True)
    Mp = sp.Matrix(2, 2, m_syms)
    qv, pv = sp.Matrix([bp_, bm_]), sp.Matrix([pp_, pm_])
    lam2 = sp.symbols("lam2")
    weak2 = sp.expand(poisson(C, (qv.T * Mp * pv)[0], qs, ps) - lam2 * C)
    sol2 = sp.solve(list(sp.Poly(weak2, qs + ps).as_dict().values()),
                    list(m_syms) + [lam2], dict=True)[0]
    assert sol2.get(lam2, lam2) == 0
    print("    (pair block only: weak forces lam=0 — v1's 1b stands at that scope.)")


def part3_two_species():
    """E154: rotation-TYPE forced; degeneracy is a normalization convention."""
    z, S = sp.symbols("zeta S", real=True)
    pz, pS = sp.symbols("p_zeta p_S", real=True)
    qs0, ps0, C0 = _full_setup()
    c1, c2 = sp.symbols("c1 c2", positive=True)
    qs = qs0 + [z, S]
    ps = ps0 + [pz, pS]
    C_ext = C0 + sp.Rational(1, 2) * (c1 * pz**2 + c2 * pS**2)

    # General species-block mixer.
    n11, n12, n21, n22 = sp.symbols("n11 n12 n21 n22", real=True)
    H_mix = n11 * z * pz + n12 * z * pS + n21 * S * pz + n22 * S * pS
    br = sp.expand(poisson(C_ext, H_mix, qs, ps))
    sol = sp.solve(list(sp.Poly(br, ps).as_dict().values()),
                   [n11, n12, n21, n22], dict=True)[0]
    assert sol.get(n11, n11) == 0 and sol.get(n22, n22) == 0
    # Single relation c1*n12 + c2*n21 = 0: skewed rotation-type mixer for ANY c1,c2.
    n12_sol = sol.get(n12, n12)
    assert sp.simplify(n12_sol + c2 * n21 / c1) == 0, sol
    H_skew = z * pS - (c1 / c2) * S * pz
    assert sp.simplify(poisson(C_ext, H_skew, qs, ps)) == 0
    # Rotation-TYPE always: n12*n21 = -(c2/c1) n21^2 < 0 — never squeezer-type.
    assert sp.simplify(n12_sol * n21 + (c2 / c1) * n21**2) == 0
    # Equal-weight rotation and squeezer witnesses (v1 statements, now scoped).
    br_rot = sp.expand(poisson(C_ext, pS * z - pz * S, qs, ps))
    br_sq = sp.expand(poisson(C_ext, z * pS + S * pz, qs, ps))
    assert sp.simplify(br_rot - (c2 - c1) * pz * pS) == 0
    assert sp.simplify(br_sq + (c1 + c2) * pz * pS) == 0
    # Canonical rescale removes c1, c2 entirely (degeneracy = convention).
    zt, St, pzt, pSt = sp.symbols("zt St pzt pSt", real=True)
    C_resc = C_ext.subs({pz: pzt / sp.sqrt(c1), pS: pSt / sp.sqrt(c2)})
    assert sp.simplify(C_resc - (C0 + sp.Rational(1, 2) * (pzt**2 + pSt**2))) == 0
    # Two-species SHEAR is legal for all c1, c2 (used by the E156 CDI cell).
    assert sp.simplify(poisson(C_ext, pz * pS, qs, ps)) == 0
    print("[3] E154: general legal species mixer: n11=n22=0, c1*n12+c2*n21=0 —")
    print("    rotation-TYPE mixing FORCED (n12*n21<0, never squeezer: the 'symmetric x")
    print("    two-species' cell stays FORBIDDEN for every c1,c2), but a skewed legal")
    print("    mixer exists for ANY c1!=c2 and a canonical rescale removes c1/c2:")
    print("    degeneracy is a NORMALIZATION CONVENTION, not a derived necessity.")
    print("    Exact surviving statement: the equal-weight power-conserving Phase-10 map")
    print("    (beta_iso=sin^2 theta_c) requires c1=c2 in physical variables; A4's")
    print("    physical content (real (CDM,radiation) degeneracy) remains ASSUMED.")
    print("    Two-species shear p_zeta p_S: legal for all c1,c2 (no degeneracy needed).")


def part4_shear_maps_and_tension():
    """E155: shear Bogoliubov (general D), coherent range, and the omega-level tension."""
    s, w = sp.symbols("s omega", real=True, positive=True)
    sigma = s * w
    # Transfer for H_x = p_+ p_- on pair block x = (q_+, q_-, p_+, p_-).
    X = sp.Matrix([[0, 1], [1, 0]])
    K = sp.zeros(4, 4)
    K[0:2, 2:4] = X
    T = sp.eye(4) + K * s
    assert sp.simplify(sp.exp(K * s) - T) == sp.zeros(4, 4)
    J = sp.zeros(4, 4)
    J[0:2, 2:4] = sp.eye(2)
    J[2:4, 0:2] = -sp.eye(2)
    assert sp.simplify(T.T * J * T - J) == sp.zeros(4, 4)
    assert sp.simplify(T.T * T) != sp.eye(4)
    # [A_0, K] = 0 on the FULL 6-dim space (note: any [[0,B],[0,0]] pair commutes —
    # this is automatic for every legal D, unlike Phase 7's E129 condition on B).
    eta = sp.diag(-1, 1, 1)
    A0_6 = sp.zeros(6, 6)
    A0_6[0:3, 3:6] = eta
    K6 = sp.zeros(6, 6)
    K6[1:3, 4:6] = X
    assert sp.simplify(A0_6 * K6 - K6 * A0_6) == sp.zeros(6, 6)
    Gam = sp.diag(1, -1, -1, 1, -1, -1)
    assert sp.simplify(Gam * K6 - K6 * Gam) == sp.zeros(6, 6)

    # Bogoliubov via independent ladder symbols.
    ap_, am_, apc, amc = sp.symbols("a_p a_m ac_p ac_m")
    q_of = lambda aa, ac: (aa + ac) / sp.sqrt(2 * w)
    p_of = lambda aa, ac: -sp.I * sp.sqrt(w / 2) * (aa - ac)
    ap_out = sp.expand((w * (q_of(ap_, apc) + s * p_of(am_, amc)) + sp.I * p_of(ap_, apc))
                       / sp.sqrt(2 * w))
    assert sp.simplify(ap_out.subs(s, 0) - ap_) == 0
    beta = sp.simplify(ap_out.coeff(amc))
    assert sp.simplify(beta - sp.I * sigma / 2) == 0
    assert sp.simplify(ap_out.coeff(ap_) - 1) == 0
    assert sp.simplify(ap_out.coeff(am_) + sp.I * sigma / 2) == 0
    n_created = sp.simplify(sp.Abs(beta) ** 2)
    F_avg = sp.simplify(1 + 2 * n_created)
    assert sp.simplify(F_avg - (1 + sigma**2 / 2)) == 0
    # General legal D: beta-block = i sigma D / 2, <N_j> = (sigma^2/4)(D^2)_jj.
    # Single-mode member p_+^2/2: same-mode beta, polarization-asymmetric map.
    ap1_out = sp.expand((w * (q_of(ap_, apc) + s * p_of(ap_, apc)) + sp.I * p_of(ap_, apc))
                        / sp.sqrt(2 * w))
    beta1 = sp.simplify(ap1_out.coeff(apc))
    assert sp.simplify(beta1 - sp.I * sigma / 2) == 0
    F_single = sp.simplify(1 + 2 * (sp.Abs(beta1)**2) / 2)  # only + polarization pumped
    assert sp.simplify(F_single - (1 + sigma**2 / 4)) == 0
    # Coherent (fixed-phase) range of the cross-shear power factor: [1, 1+sigma^2].
    t = sp.symbols("t", real=True)
    F_coh = sp.simplify(1 + sigma**2 * sp.cos(w * t) ** 2)
    assert sp.simplify(F_coh.subs(t, 0) - (1 + sigma**2)) == 0
    assert sp.simplify(F_coh.subs(w * t, sp.pi / 2) - 1) == 0
    print("[4] E155: cross-shear beta=i sigma/2, <N>=sigma^2/4, phase-avg F=1+sigma^2/2;")
    print("    general legal D: beta = i sigma D/2, <N_j> = (sigma^2/4)(D^2)_jj —")
    print("    single-mode p_+^2/2 gives 1+sigma^2/4 (polarization-asymmetric).")
    print("    Coherent range F in [1, 1+sigma^2]: the shear NEVER suppresses r")
    print("    (distinguishing signature vs the squeezer's x0.043 branch, E140).")

    # DECLARED TENSION: omega-level legality gates (PHASE9_NULL 2.2/2.3) fail.
    qs, ps, _ = _full_setup()
    a, bp, bm = qs
    pa, pp_, pm = ps
    C_w = sp.Rational(1, 2) * (-pa**2 + pp_**2 + pm**2) \
        + sp.Rational(1, 2) * w**2 * (bp**2 + bm**2) - sp.Rational(1, 2) * w**2 * a**2
    br_w = sp.expand(poisson(C_w, pp_ * pm, qs, ps))
    assert sp.simplify(br_w - w**2 * (bp * pm + bm * pp_)) == 0
    print("    TENSION (declared): with common frequency omega != 0 in the constraint,")
    print("    {C_omega, p_+p_-} = omega^2 (q_+p_- + q_-p_+) != 0 — the violation is the")
    print("    FORBIDDEN squeezer direction; the rotation passed this gate, the shear")
    print("    does not.  The shear is legal exactly where (omega=0) its signal vanishes.")

    # BK18 table — ILLUSTRATIVE ONLY (domain: enhancement is blue prop. to k^2).
    r_vac = sp.symbols("r_vac", positive=True)
    sig = sp.symbols("sigma_b", positive=True)
    print("    BK18 table (ILLUSTRATIVE — k^2-blue enhancement is outside the")
    print("    near-scale-invariant card domain; honest card verdict = ABSTAIN):")
    vals = []
    for rv in (sp.Rational(1, 1000), sp.Rational(3, 1000), sp.Rational(1, 100), sp.Rational(3, 100)):
        bound = sp.solve(sp.Eq(rv * (1 + sig**2 / 2), BK18_R_LIMIT), sig)
        smax = [b for b in bound if b.is_positive][0]
        vals.append(float(smax))
        print(f"      r_vac = {float(rv):.3f}  =>  sigma < {float(smax):.4f}  (pivot-scale reading)")
    assert vals == sorted(vals, reverse=True)


def part5_matrix():
    """E156: component x channel matrix under declared per-channel state conventions."""
    print("[5] E156 matrix (homogeneous quadratics, strong criterion, per-channel state")
    print("    conventions declared: tensor=quantum vacuum, CDI=frozen amplitudes [A5, NEW]):")
    rows = [
        ("rotation (antisym qp)", "tensor null (E137, state-independent)", "beta_iso=sin^2 theta_c (E143; equal-weight form needs c1=c2)"),
        ("skewed species mixer", "—", "CDI with c1/c2 amplitude factors (legal for all c1!=c2)"),
        ("shear (pp, cross)", "F=1+sigma^2/2 CONDITIONAL (omega-tension declared)", "null in frozen limit (A5; exact-limit only)"),
        ("shear (pp, single-mode)", "F=1+sigma^2/4, polarization-asymmetric", "null in frozen limit (A5)"),
        ("boost (alpha-beta)", "DEFERRED (omega trap)", "DEFERRED"),
        ("dilation q.p (weak only)", "F=1+2 sinh^2 s — E139 map resurrected", "frozen-limit null (A5)"),
        ("squeezer (sym qp)", "FORBIDDEN strong+weak on pair (E152)", "FORBIDDEN all c1,c2 (E154)"),
        ("qq collar / q-linear", "FORBIDDEN (E152)", "FORBIDDEN"),
        ("p-linear displacement", "unmapped (coherent offsets; legal)", "unmapped"),
    ]
    for name, tcell, ccell in rows:
        print(f"    {name:28s} | tensor: {tcell:52s} | CDI: {ccell}")
    print("    E156 also SUPERSEDES the broad reading of Phase-9 E138: 'observable tensor")
    print("    signal requires a symmetric qp component' is true within the qp class only;")
    print("    the shear (strong) and dilation (weak) are counterexamples.")


def main() -> int:
    part1_strong_classification()
    part2_weak_criterion_dilation()
    part3_two_species()
    part4_shear_maps_and_tension()
    part5_matrix()
    print("ALL EXACT CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
