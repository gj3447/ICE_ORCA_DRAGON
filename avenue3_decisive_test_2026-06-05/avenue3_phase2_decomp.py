"""
Avenue-3 PHASE 2 — S3-representation decomposition of the sedenion ZD locus.

Builds on Phase-1 VERIFIED ground truth (avenue3_phase1_*.py):
  * exact-arithmetic CD multiplication table (16x16),
  * 42 assessors / 84 primitive ZD units / 7 box-kites,
  * GENUINE S3 = Aut(S)\\Aut(O) = <psi, eps> (psi^3=I, eps^2=I, eps psi eps = psi^-1,
    psi moves e0..e7 OUT of e0..e7; both VERIFIED automorphisms on all 256 products).

GOAL (pre-registered Phase-2 task):
  1. Form the S3-representation on the ZD locus at several granularities.
  2. Decompose into irreps (trivial 1, sign 1', standard 2) via CHARACTER THEORY:
     for each conjugacy class compute the character = trace of the rep matrix
     (= #fixed points for a permutation rep), then m_irrep = <chi, chi_irrep>.
  3. Check whether the "3" is FORCED (regular rep / standard-2 multiplicity) or
     only a hand-assigned count.
  4. Extract any non-trivial multiplicity / ratio / Clebsch.

RIGOR: every action is COMPUTED. The S3 elements are the genuine VERIFIED automorphisms
as LINEAR maps on R^16 (psi, eps are 16x16 matrices). We do NOT hand-pick a permutation
on labels. When we need the action on the ZD locus we push the actual ZD *elements* (as
16-vectors) through psi/eps and find where they land.

S3 conjugacy classes (orders): {e} (1 elt), {3 transposition-type order-2: eps, psi eps, psi^2 eps}
(3 elts), {2 order-3: psi, psi^2} (2 elts).
Character table of S3:
            e    (12)[order2, 3 elts]   (123)[order3, 2 elts]
  triv  1   1         1                      1
  sign  1' 1        -1                       1
  std   2   2         0                     -1
"""
import itertools
from fractions import Fraction as F
import sympy as sp
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()

# ---------------------------------------------------------------------------
# linear algebra over the 16-dim space using exact sympy
# ---------------------------------------------------------------------------
half = sp.Rational(1, 2)
sqrt3 = sp.sqrt(3)
I16 = sp.eye(DIM)

def vmulM(u, v):
    """sedenion product of two 16-col-vectors via the exact table."""
    res = sp.zeros(DIM, 1)
    for i in range(DIM):
        if u[i] == 0:
            continue
        for j in range(DIM):
            if v[j] == 0:
                continue
            k, s = table[i][j]
            res[k] += u[i] * v[j] * s
    return res

def is_automorphism(M):
    cols = [M[:, j] for j in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k, s = table[i][j]
            if sp.simplify(s * cols[k] - vmulM(cols[i], cols[j])) != sp.zeros(DIM, 1):
                return False
    return True

# psi : 2pi/3 rotation in the seven e_i -- e_{i+8} planes (i=1..7), e0,e8 fixed
psi = sp.zeros(DIM, DIM); psi[0, 0] = 1; psi[8, 8] = 1
for i in range(1, 8):
    j = i + 8
    psi[i, i] = -half; psi[j, i] = sqrt3 * half
    psi[j, j] = -half; psi[i, j] = -sqrt3 * half

# eps : per-plane reflection diag(1,-1) (e_i->e_i, e_{i+8}->-e_{i+8}), e8 -> -e8, e0 fixed
eps = sp.zeros(DIM, DIM); eps[0, 0] = 1; eps[8, 8] = -1
for i in range(1, 8):
    eps[i, i] = 1; eps[i + 8, i + 8] = -1

print("=" * 72)
print("PHASE 2 — S3-rep decomposition of the sedenion ZD locus")
print("=" * 72)
print("\n[0] Re-verify the genuine S3 (not asserted):")
print("    psi is Aut(S):", is_automorphism(psi), "  psi^3=I:", sp.simplify(psi**3 - I16) == sp.zeros(DIM, DIM))
print("    eps is Aut(S):", is_automorphism(eps), "  eps^2=I:", eps * eps == I16)
print("    eps psi eps = psi^-1:", sp.simplify(eps * psi * eps - psi * psi) == sp.zeros(DIM, DIM))
refO = set(range(8))
imgpsi = set()
for i in range(8):
    col = psi[:, i]
    imgpsi.update(r for r in range(DIM) if col[r] != 0)
print("    psi moves e0..e7 OUT of e0..e7 (genuine Aut(S)\\Aut(O)):", not imgpsi.issubset(refO))

# enumerate the six group elements as matrices
g_e   = I16
g_psi = psi
g_psi2 = sp.simplify(psi * psi)
g_eps  = eps
g_psieps = sp.simplify(psi * eps)
g_psi2eps = sp.simplify(psi * psi * eps)
group = {
    'e': g_e, 'psi': g_psi, 'psi2': g_psi2,
    'eps': g_eps, 'psi*eps': g_psieps, 'psi2*eps': g_psi2eps,
}
# conjugacy classes of S3
cls_e   = ['e']
cls_rot = ['psi', 'psi2']           # order-3 class, 2 elements
cls_ref = ['eps', 'psi*eps', 'psi2*eps']  # order-2 class, 3 elements
for name in cls_ref:
    M = group[name]
    assert sp.simplify(M * M - I16) == sp.zeros(DIM, DIM), f"{name} not order 2"
for name in cls_rot:
    M = group[name]
    assert sp.simplify(M**3 - I16) == sp.zeros(DIM, DIM), f"{name} not order 3"
print("\n[0b] 6 group elements built; classes verified:",
      "e(1) | rot order3:", cls_rot, "(2) | refl order2:", cls_ref, "(3)")

# ---------------------------------------------------------------------------
# S3 irrep characters (standard S3 character table)
#   class:      e      order3(2 elts)   order2(3 elts)
#   sizes:      1      2                3
CHAR = {
    'triv': {'e': 1, 'rot': 1, 'ref': 1},
    'sign': {'e': 1, 'rot': 1, 'ref': -1},
    'std':  {'e': 2, 'rot': -1, 'ref': 0},
}
CLASS_SIZE = {'e': 1, 'rot': 2, 'ref': 3}
GROUP_ORDER = 6

def decompose(chi):
    """chi: dict {'e':val,'rot':val,'ref':val}. Returns multiplicities of triv,sign,std."""
    mult = {}
    for irr, ic in CHAR.items():
        s = sum(CLASS_SIZE[c] * chi[c] * ic[c] for c in ('e', 'rot', 'ref'))
        m = sp.Rational(s, GROUP_ORDER)
        mult[irr] = m
    return mult

# ===========================================================================
# REP A — natural 16-dim representation on the sedenion algebra (for reference)
# ===========================================================================
print("\n" + "=" * 72)
print("[A] Natural 16-dim rep of S3 on the sedenion algebra S = R^16")
print("=" * 72)
chiA = {
    'e':   sp.trace(group['e']),
    'rot': sp.simplify(sp.trace(group['psi'])),
    'ref': sp.simplify(sp.trace(group['eps'])),
}
print("    character (trace) on classes  e/rot/ref:", chiA)
multA = decompose(chiA)
print("    decomposition: triv=%s sign=%s std=%s" % (multA['triv'], multA['sign'], multA['std']))
print("    (dim check: triv+sign+2*std =", multA['triv'] + multA['sign'] + 2 * multA['std'], "should be 16)")

# ===========================================================================
# REP B — PERMUTATION rep on the 42 assessors
# ===========================================================================
print("\n" + "=" * 72)
print("[B] PERMUTATION rep of S3 on the 42 ASSESSORS")
print("=" * 72)

# rebuild the 42 assessors and the primitive ZD units (as 16-vectors)
def vmulF(u, v):
    res = [F(0)] * DIM
    for i in range(DIM):
        if u[i] == 0: continue
        for j in range(DIM):
            if v[j] == 0: continue
            k, s = table[i][j]
            res[k] += u[i] * v[j] * s
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
zd_units = set()
for p, q in ann_ord:
    zd_units.add(p); zd_units.add(q)
assessors = sorted(set((a, b) for (a, b, s) in zd_units))
print("    #assessors =", len(assessors), "(expect 42)")
print("    #primitive ZD units =", len(zd_units), "(expect 84)")

# To act on assessors we need the action on the 2-plane span{e_a,e_b}. Since psi/eps are
# LINEAR maps mixing e_i with e_{i+8}, an assessor plane is generally NOT mapped to another
# assessor coordinate-plane. We therefore identify the action by tracking the SET of ZD
# *subspaces*. The clean, well-defined permutation action of Aut(S) on the ZD locus is on
# the set of 2-dim "assessor planes" {span(e_a,e_b)}; we compute g(plane) and find which
# assessor plane (if any) it equals AS A SUBSPACE.

def assessor_plane_basis(a, b):
    va = sp.zeros(DIM, 1); va[a] = 1
    vb = sp.zeros(DIM, 1); vb[b] = 1
    return [va, vb]

def in_span(vecs, w):
    """is column-vector w in span of the list 'vecs'? exact rank test."""
    M = sp.Matrix.hstack(*vecs)
    Maug = sp.Matrix.hstack(M, w)
    return M.rank() == Maug.rank()

def same_plane(b1, b2):
    """do 2-vector bases b1,b2 span the same subspace?"""
    return in_span(b2, b1[0]) and in_span(b2, b1[1]) and in_span(b1, b2[0]) and in_span(b1, b2[1])

# Precompute the 42 assessor plane bases.
plane_basis = {ax: assessor_plane_basis(*ax) for ax in assessors}

def perm_on_assessors(M):
    """Return a permutation dict ax-> ax' such that M(plane(ax)) == plane(ax'),
       or None for that ax if image is not an assessor plane (off-locus)."""
    perm = {}
    for ax in assessors:
        b = plane_basis[ax]
        gb = [sp.simplify(M * b[0]), sp.simplify(M * b[1])]
        found = None
        for ax2 in assessors:
            if same_plane(gb, plane_basis[ax2]):
                found = ax2; break
        perm[ax] = found
    return perm

# This is expensive (42 * 42 rank tests per element); compute only for class reps.
print("    Computing assessor-plane action for class representatives (this is the load-bearing part)...")
permE = {ax: ax for ax in assessors}          # identity
permRot = perm_on_assessors(group['psi'])      # order-3 representative
permRef = perm_on_assessors(group['eps'])      # order-2 representative

def fixed_and_closed(perm):
    mapped = sum(1 for ax in assessors if perm[ax] is not None)
    fixed = sum(1 for ax in assessors if perm[ax] == ax)
    closed = all(perm[ax] is not None for ax in assessors)
    return mapped, fixed, closed

mE = fixed_and_closed(permE); mR = fixed_and_closed(permRot); mF = fixed_and_closed(permRef)
print(f"    identity : mapped-onto-assessor {mE[0]}/42, fixed {mE[1]}, closed {mE[2]}")
print(f"    psi(rot) : mapped-onto-assessor {mR[0]}/42, fixed {mR[1]}, closed {mR[2]}")
print(f"    eps(ref) : mapped-onto-assessor {mF[0]}/42, fixed {mF[1]}, closed {mF[2]}")

if mR[2] and mF[2]:
    # genuine permutation rep on 42 assessors. character = #fixed points.
    chiB = {'e': mE[1], 'rot': mR[1], 'ref': mF[1]}
    print("    permutation character (#fixed pts) e/rot/ref:", chiB)
    multB = decompose(chiB)
    print("    decomposition of the 42-assessor PERM rep: triv=%s sign=%s std=%s"
          % (multB['triv'], multB['sign'], multB['std']))
    print("    dim check triv+sign+2std =", multB['triv'] + multB['sign'] + 2 * multB['std'], "(expect 42)")
else:
    print("    !! S3 does NOT closed-permute the 42 coordinate assessor planes.")
    print("       The assessor planes are NOT preserved as a SET by the genuine S3 (psi mixes e_i,e_{i+8}).")
    print("       => the '42 assessors' is NOT an S3-set; the perm rep on coordinate assessors is ill-defined.")
    print("       Reporting partial fixed/closed data above. We pivot to the box-kite & ladder actions (Reps C,D).")
