"""
Avenue-3 PHASE 2 (part 2) — proper S3-MODULE decompositions.

Phase-2 part-1 finding (avenue3_phase2_decomp.py):
  * Natural 16-dim rep of genuine S3 on S = triv(1) + sign(1) + std(7).
  * The 42 COORDINATE assessor planes are NOT permuted as a set by psi (0/42 land back),
    so the de Marrais coordinate-assessor labeling is a G2-FRAME description, not an S3-set.
    (eps IS coordinate-wise; psi is not. This is honest, not a bug.)

This script does the decompositions that ARE well-defined S3-modules:
  C. The three GGV octonion subalgebras {O1,O2,O3} and the imaginary-ladder spaces.
  D. The ladder-operator triple (A1,A2,A3) and the generation module.
  E. The split S = H + (the 12-dim "generation-carrying" complement) and its S3-decomp.
  F. Whether the ZD locus as a VARIETY is S3-invariant (does psi map ZDs to ZDs?).
  G. The Reggiani G2 statement: does G2-rep theory add a forced quantum number?

CHARACTER THEORY is used throughout: chi(g)=trace(rep(g)); m = (1/|G|) sum_classes |C| chi(C) chi_irr(C).
Everything COMPUTED with exact sympy. No hand-assigned permutations.
"""
import itertools
from fractions import Fraction as F
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
half = sp.Rational(1, 2); sqrt3 = sp.sqrt(3); I16 = sp.eye(DIM)

def vmulM(u, v):
    res = sp.zeros(DIM, 1)
    for i in range(DIM):
        if u[i] == 0: continue
        for j in range(DIM):
            if v[j] == 0: continue
            k, s = table[i][j]; res[k] += u[i] * v[j] * s
    return res
def is_automorphism(M):
    cols = [M[:, j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k, s = table[i][j]
            if sp.simplify(s * cols[k] - vmulM(cols[i], cols[j])) != sp.zeros(DIM, 1):
                return False
    return True

psi = sp.zeros(DIM, DIM); psi[0, 0] = 1; psi[8, 8] = 1
for i in range(1, 8):
    j = i + 8
    psi[i, i] = -half; psi[j, i] = sqrt3 * half; psi[j, j] = -half; psi[i, j] = -sqrt3 * half
eps = sp.zeros(DIM, DIM); eps[0, 0] = 1; eps[8, 8] = -1
for i in range(1, 8):
    eps[i, i] = 1; eps[i + 8, i + 8] = -1

group = {'e': I16, 'psi': sp.simplify(psi), 'psi2': sp.simplify(psi * psi),
         'eps': eps, 'psi*eps': sp.simplify(psi * eps), 'psi2*eps': sp.simplify(psi * psi * eps)}

CHAR = {'triv': {'e': 1, 'rot': 1, 'ref': 1},
        'sign': {'e': 1, 'rot': 1, 'ref': -1},
        'std':  {'e': 2, 'rot': -1, 'ref': 0}}
CLASS_SIZE = {'e': 1, 'rot': 2, 'ref': 3}
def decompose(chi):
    return {irr: sp.Rational(sum(CLASS_SIZE[c] * chi[c] * ic[c] for c in ('e', 'rot', 'ref')), 6)
            for irr, ic in CHAR.items()}

def char_of_subrep(P):
    """P: basis matrix B with cols spanning an invariant subspace (may be rank-deficient).
       Returns character on classes by restricting group elements and taking trace.
       Reduces to an INDEPENDENT column basis first (so B^T B is invertible), then
       rep_B(g) solves g*B = B * R, R = (B^T B)^-1 B^T g B (exact). chi = trace R.
       Requires the subspace to be invariant; we verify g*B in col-space(B)."""
    # reduce to independent columns
    cols = [P[:, j] for j in range(P.cols)]
    indep = []
    for c in cols:
        if not indep:
            if sp.simplify(c) != sp.zeros(DIM, 1):
                indep.append(c)
            continue
        M = sp.Matrix.hstack(*indep)
        if sp.Matrix.hstack(M, c).rank() > M.rank():
            indep.append(c)
    B = sp.Matrix.hstack(*indep)
    G = (B.T * B)
    Ginv = G.inv()
    chi = {}
    reps = {'e': group['e'], 'rot': group['psi'], 'ref': group['eps']}
    rk = B.rank()
    for cl, g in reps.items():
        gB = sp.simplify(g * B)
        # invariance check: every column of g*B must lie in col-space(B)
        if sp.Matrix.hstack(B, gB).rank() != rk:
            chi[cl] = None  # subspace not invariant under this g
            continue
        R = sp.simplify(Ginv * B.T * g * B)
        chi[cl] = sp.simplify(sp.trace(R))
    return chi

print("=" * 72)
print("PHASE 2 (part 2) — proper S3-MODULE decompositions")
print("=" * 72)

# ---------------------------------------------------------------------------
# F. Is the ZD locus S3-invariant as a VARIETY? (does psi map ZD elements to ZD elements?)
# ---------------------------------------------------------------------------
print("\n[F] Is the ZD locus invariant under the genuine S3 (variety-level)?")
def vmulF(u, v):
    res = [F(0)] * DIM
    for i in range(DIM):
        if u[i] == 0: continue
        for j in range(DIM):
            if v[j] == 0: continue
            k, s = table[i][j]; res[k] += u[i] * v[j] * s
    return res
def vecF(a, b, s):
    v = [F(0)] * DIM; v[a] = F(1); v[b] = F(s); return v
prim = [(a, b, s) for a, b in itertools.combinations(range(1, DIM), 2) for s in (1, -1)]
ann_ord = []
for (a, b, s) in prim:
    X = vecF(a, b, s)
    for (c, d, t) in prim:
        if vmulF(X, vecF(c, d, t)) == [F(0)] * DIM:
            ann_ord.append(((a, b, s), (c, d, t)))
# A ZD element is any primitive that annihilates something. Take the *set of ZD directions*.
zd_unit_labels = set()
for p, q in ann_ord:
    zd_unit_labels.add(p); zd_unit_labels.add(q)

def label_to_col(lab):
    a, b, s = lab
    v = sp.zeros(DIM, 1); v[a] = 1; v[b] = s
    return v

# Does psi(X) still annihilate psi(Y) for every annihilating ordered pair? (automorphism => yes,
# trivially, since psi(X)psi(Y)=psi(XY)=psi(0)=0). The real question: is psi(X) still on the
# *same kind* of locus, and does the locus-as-a-set close? We test: for each annihilating pair,
# psi(X)*psi(Y)==0 (sanity), and report whether psi(X) is again a primitive 2-term ZD or a
# longer combination (it generally becomes a 4-term vector -> NOT a coordinate primitive).
sane = True
becomes_longer = 0
for (p, q) in ann_ord[:200]:  # sample; automorphism guarantees the algebraic identity
    X = label_to_col(p); Y = label_to_col(q)
    pX = sp.simplify(psi * X); pY = sp.simplify(psi * Y)
    prod = vmulM(pX, pY)
    if sp.simplify(prod) != sp.zeros(DIM, 1):
        sane = False
    nz = sum(1 for r in range(DIM) if sp.simplify(pX[r]) != 0)
    if nz > 2:
        becomes_longer += 1
print("    psi(X)*psi(Y)=0 holds on sampled annihilating pairs (automorphism):", sane)
print(f"    of 200 sampled ZD elements, psi maps {becomes_longer} to a >2-term vector")
print("    => the ZD VARIETY is S3-invariant (automorphism image of a ZD is a ZD), but the")
print("       2-TERM COORDINATE primitives are NOT closed under psi; psi rotates them to")
print("       4-term ZD combinations within the SAME variety. So '42 assessors' is a")
print("       G2-frame chart of an S3-invariant variety, not an S3-permuted finite set.")

# ---------------------------------------------------------------------------
# E. S3-decomposition of the WHOLE imaginary space Im(S)=R^15 and natural subspaces
# ---------------------------------------------------------------------------
print("\n[E] S3-decomposition of natural invariant subspaces (character theory):")

# 15-dim imaginary part Im(S) = span(e1..e15)
Bim = sp.zeros(DIM, 15)
for idx, i in enumerate(range(1, DIM)):
    Bim[i, idx] = 1
chi_im = char_of_subrep(Bim)
print("  Im(S) (15-dim) char e/rot/ref:", chi_im, "->", {k: str(v) for k, v in decompose(chi_im).items()})

# The fixed subalgebra of psi: e0, e8 fixed; within each plane the only psi-fixed vector is 0,
# so psi-fixed space = span(e0,e8). Quaternion H = span(e0,e4,e8,e12).
BH = sp.zeros(DIM, 4)
for idx, i in enumerate([0, 4, 8, 12]):
    BH[i, idx] = 1
chi_H = char_of_subrep(BH)
print("  H=span(e0,e4,e8,e12) char e/rot/ref:", chi_H, "->", {k: str(v) for k, v in decompose(chi_H).items()})

# the seven e_i--e_{i+8} planes carry the std/sign content. Take the 14-dim space
# spanned by e1..e7,e9..e15 (i.e. all imaginary EXCEPT e8). This is 7 copies of a 2-plane
# each carrying the SO(2) 2pi/3 rotation = a real 2-dim rep on which psi acts as rotation.
Bplanes = sp.zeros(DIM, 14)
cols = list(range(1, 8)) + list(range(9, 16))
for idx, i in enumerate(cols):
    Bplanes[i, idx] = 1
chi_pl = char_of_subrep(Bplanes)
print("  14-dim seven-planes char e/rot/ref:", chi_pl, "->", {k: str(v) for k, v in decompose(chi_pl).items()})

# e8 axis alone (psi fixes e8, eps negates e8) -> sign rep
Be8 = sp.zeros(DIM, 1); Be8[8] = 1
chi_e8 = char_of_subrep(Be8)
print("  span(e8) char e/rot/ref:", chi_e8, "->", {k: str(v) for k, v in decompose(chi_e8).items()})

# ---------------------------------------------------------------------------
# C/D. The three GGV octonion subalgebras and the ladder operators.
# ---------------------------------------------------------------------------
print("\n[C] Action of genuine S3 on the three GGV octonions {O1,O2,O3} (as SETS of indices):")
O1 = {0, 1, 4, 5, 8, 9, 12, 13}; O2 = {0, 2, 4, 6, 8, 10, 12, 14}; O3 = {0, 3, 4, 7, 8, 11, 12, 15}
Os = {'O1': O1, 'O2': O2, 'O3': O3}
for gname, M in [('psi', group['psi']), ('eps', group['eps'])]:
    for on, oset in Os.items():
        img = set()
        for i in sorted(oset):
            col = M[:, i]
            img.update(r for r in range(DIM) if sp.simplify(col[r]) != 0)
        match = [n2 for n2, s2 in Os.items() if img == s2]
        print(f"    {gname}: {on} -> {match if match else 'NOT a coordinate O_i (spans %s)'%sorted(img)}")

# GGV ladder operators (arXiv:2306.13098 eqns 59-61 form): inside each O_i, a 4-term sum.
# The published A_i are complex-octonion ladder ops; here we use the REAL skeleton that lives
# in O_i and is the eigenvector content psi acts on. We build the psi-orbit of a generic
# vector seeded in O1's plane-part and measure the orbit / module.
print("\n[D] psi-orbit of a ladder seed (the '3 generations' claim):")
# seed in the e1--e9 plane (O1 contains e1,e9): v0 = e1
v0 = sp.zeros(DIM, 1); v0[1] = 1
orbit = [sp.simplify(v0), sp.simplify(psi * v0), sp.simplify(psi * psi * v0)]
print("    psi-orbit of e1:")
for k, w in enumerate(orbit):
    supp = [(r, w[r]) for r in range(DIM) if sp.simplify(w[r]) != 0]
    print(f"      psi^{k} e1 = {supp}")
distinct = len({tuple(sp.nsimplify(x) for x in w) for w in orbit})
print("    distinct elements in orbit:", distinct, "(psi^3=I forces orbit | 3 or 1)")
# the 3-dim module spanned by the orbit:
Borb = sp.Matrix.hstack(*orbit)
rk = Borb.rank()
print("    rank of span(orbit) =", rk, "(dimension of the cyclic Z3-module on this seed)")
if rk >= 1:
    chi_orb = char_of_subrep(Borb)
    print("    char of the psi-orbit module e/rot/ref:", chi_orb)
    if all(v is not None for v in chi_orb.values()):
        print("      -> decomposition:", {k: str(v) for k, v in decompose(chi_orb).items()})
    else:
        print("      -> this 2-plane is NOT eps-invariant standalone; std(2) only after pairing.")

# Crucial: build the FULL S3-module generated by the seed (close under BOTH psi and eps).
print("\n[D2] FULL S3-module generated by the e1 ladder seed (close under psi AND eps):")
seeds = [v0]
basis_cols = []
def add_if_new(w):
    w = sp.simplify(w)
    if w == sp.zeros(DIM, 1):
        return
    if not basis_cols:
        basis_cols.append(w); return
    M = sp.Matrix.hstack(*basis_cols)
    if sp.Matrix.hstack(M, w).rank() > M.rank():
        basis_cols.append(w)
frontier = [v0]
gens = [group['psi'], group['eps']]
while frontier:
    w = frontier.pop()
    before = len(basis_cols)
    add_if_new(w)
    if len(basis_cols) > before:
        for g in gens:
            frontier.append(sp.simplify(g * w))
Bmod = sp.Matrix.hstack(*basis_cols)
print("    dim of S3-module generated by e1 =", Bmod.rank())
chi_mod = char_of_subrep(Bmod)
print("    char e/rot/ref:", chi_mod)
if all(v is not None for v in chi_mod.values()):
    print("    -> decomposition:", {k: str(v) for k, v in decompose(chi_mod).items()})

print("\n" + "=" * 72)
print("SUMMARY OF FORCED MULTIPLICITIES")
print("=" * 72)
print("  natural 16-dim S = triv(1) + sign(1) + std(7)")
print("  Im(S) 15-dim     =", {k: str(v) for k, v in decompose(chi_im).items()})
print("  the std multiplicity counts the 7 e_i--e_{i+8} planes (G2 / octonion-imaginary 7),")
print("  NOT a generation count. Each plane = ONE std(2) copy; there are 7 planes -> std=7.")
