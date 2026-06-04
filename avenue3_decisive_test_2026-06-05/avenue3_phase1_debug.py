"""
Debug pass: pin down the alternativity check and the exact ZD count semantics
against de Marrais (math/0011260) / Cawagas (2004) / Lygeros (2006).

Key definitions (de Marrais "The 42 Assessors and the Box-Kites of the Sedenions"):
  - A sedenion zero divisor of primitive type is a sum of TWO imaginary units:
        D = e_a + e_b   (or with a minus sign).
  - The set of mutually-annihilating such D's.  de Marrais counts:
        168 primitive zero-divisor UNITS
        these form 84 mutually-orthogonal PAIRS
        organized as 42 ASSESSORS (an assessor = a +/- diagonal axis pair, i.e.
            {e_a+e_b, e_a-e_b} is ONE assessor / "carbon atom" with two "valence" lines)
        organized into 7 BOX-KITES (each box-kite = 6 assessors = the ZD structure
            attached to one "strut constant" = one of the 7 octonion-index labels
            that does NOT appear... actually indexed by the 7 nonzero values of the
            high-bit XOR pattern).  7 box-kites x 6 assessors = 42 assessors.
"""
import itertools
from fractions import Fraction as F
from avenue3_phase1_groundtruth import build_table, e, DIM

table = build_table()

def vmul(u, v):
    res = [F(0)] * DIM
    for i in range(DIM):
        if u[i] == 0:
            continue
        for j in range(DIM):
            if v[j] == 0:
                continue
            k, sgn = table[i][j]
            res[k] += u[i] * v[j] * sgn
    return res

def vec(a, b, s):
    v = [F(0)] * DIM
    v[a] = F(1)
    v[b] = F(s)
    return v

# --- Fix the alternativity check ---------------------------------------
# Alternative algebra: associator (x,x,y)=0 and (y,x,x)=0 for ALL x,y in the algebra,
# not just basis elements. But for a *-algebra built by CD, non-alternativity must
# show up on SOME triple. The basis-only left-alternative test (e_i,e_i,e_j) is
# degenerate because e_i*e_i = -e0 (scalar), so it ALWAYS associates trivially.
# The real test: pick generic-ish elements, or test the flexible/alternative law on
# mixed basis triples (e_i, e_j, e_k) all distinct and check the associator, then
# check the genuine alternative identity (x,x,y) with x a SUM.
def assoc(i, j, k):
    k1, s1 = table[i][j]
    k2, s2 = table[k1][k]
    left = (k2, s1 * s2)
    k3, s3 = table[j][k]
    k4, s4 = table[i][k3]
    right = (k4, s3 * s4)
    return left, right

# left-alternative on basis is trivially true since e_i^2 = -e0. Test with sums:
def left_alt_fails():
    """Find x (a sum of two units) and basis y with (x,x,y) != 0."""
    for a, b in itertools.combinations(range(1, DIM), 2):
        x = vec(a, b, 1)
        for y_idx in range(1, DIM):
            y = e(y_idx)
            xx = vmul(x, x)
            left = vmul(vmul(x, x), y)
            right = vmul(x, vmul(x, y))
            if left != right:
                return (a, b, y_idx, left, right)
    return None

# octonions ARE alternative: same test inside 0..7 must NEVER fail
def left_alt_fails_oct():
    for a, b in itertools.combinations(range(1, 8), 2):
        x = vec(a, b, 1)
        for y_idx in range(1, 8):
            y = e(y_idx)
            left = vmul(vmul(x, x), y)
            right = vmul(x, vmul(x, y))
            if left != right:
                return (a, b, y_idx)
    return None

print("Left-alternative law on sedenions (sum x):", left_alt_fails())
print("Left-alternative law inside octonions 0..7:", left_alt_fails_oct(), "(None = alternative, as expected)")

# Concrete known sedenion ZD (classic example): (e3 + e10)(e6 + e15) ?
# de Marrais canonical: (e1+e10)(e5+e14)=0 etc depend on convention. Let's just SEARCH.
print("\n--- Classic ZD example search (e_a+e_b)(e_c+e_d)=0, all distinct ---")
examples = []
for a, b in itertools.combinations(range(1, DIM), 2):
    for c, d in itertools.combinations(range(1, DIM), 2):
        if len({a, b, c, d}) < 4:
            continue
        X = vec(a, b, 1)
        Y = vec(c, d, 1)
        if vmul(X, Y) == [F(0)] * DIM:
            examples.append((a, b, c, d))
print(f"  count of (e_a+e_b)(e_c+e_d)=0 with 4 distinct indices, all + signs: {len(examples)}")
print(f"  first 5: {examples[:5]}")

# Now the careful counting. de Marrais terminology:
# PRIMITIVE ZERO-DIVISOR UNIT = a single primitive element D=e_a+/-e_b that annihilates
#   SOMETHING (left OR right). Count DISTINCT such D.
# ASSESSOR = the pair {e_a+e_b, e_a-e_b} sharing the SAME two axes {a,b}: a "diagonal".
# So: n_assessors = (number of distinct unordered axis-pairs {a,b} that carry ZD structure).
# n_primitive_units = 2 * n_assessors  (the +/- variants), IF both signs are ZDs.
# n_zd_pairs (de Marrais "84") = number of mutually-annihilating UNORDERED pairs of units.

# Build the set of primitive units that are zero divisors (annihilate something):
prim_all = []
for a, b in itertools.combinations(range(1, DIM), 2):
    for s in (1, -1):
        prim_all.append((a, b, s))

zd_units = set()
ann_ordered = set()
for (a, b, s) in prim_all:
    X = vec(a, b, s)
    for (c, d, t) in prim_all:
        Y = vec(c, d, t)
        if vmul(X, Y) == [F(0)] * DIM:
            zd_units.add((a, b, s))
            zd_units.add((c, d, t))
            ann_ordered.add(((a, b, s), (c, d, t)))

print("\n--- Counting (primitive units = sums of two imaginary units, +/- ) ---")
print(f"  distinct primitive units that are zero divisors: {len(zd_units)}")
axes = set((a, b) for (a, b, s) in zd_units)
print(f"  distinct axis-pairs {{a,b}} carrying ZD structure (= ASSESSORS): {len(axes)}")
print(f"  ordered annihilating unit pairs: {len(ann_ordered)}")
unord = set(frozenset((p, q)) for (p, q) in ann_ordered if p != q)
print(f"  unordered annihilating unit pairs (de Marrais '84'?): {len(unord)}")

# Diagonal self-pairs: does e_a+e_b annihilate e_a-e_b (same axes)?
selfdiag = sum(1 for (p, q) in ann_ordered if p[:2] == q[:2] and p[2] != q[2])
print(f"  ordered (e_a+e_b)*(e_a-e_b)=0 same-axis annihilations: {selfdiag}")
