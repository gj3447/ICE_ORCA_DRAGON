"""
Reconcile the de Marrais numbers definitively and find the 7 box-kites + S3.

de Marrais "Box-Kites" terminology, made precise by COMPUTATION:
  ASSESSOR        = an unordered axis-pair {a,b}, a<b in 1..15, such that BOTH
                    e_a+e_b and e_a-e_b are zero divisors (a "diagonal" with two
                    "vents"/orientations). Count = ?
  PRIMITIVE ZD    = a single primitive element e_a +/- e_b that annihilates
                    some other primitive element. Count = ?
  ZD PAIR         = an unordered mutually-or-one-way annihilating pair of
                    primitive elements. Count = ?
  BOX-KITE        = the connected component of the "annihilation graph" on the
                    42 assessors, indexed by a "strut constant". Should be 7,
                    each with 6 assessors.
"""
import itertools
from fractions import Fraction as F
from avenue3_phase1_groundtruth import build_table, e, DIM

table = build_table()

def vmul(u, v):
    res = [F(0)] * DIM
    for i in range(DIM):
        if u[i] == 0: continue
        for j in range(DIM):
            if v[j] == 0: continue
            k, sgn = table[i][j]
            res[k] += u[i] * v[j] * sgn
    return res

def vec(a, b, s):
    v = [F(0)] * DIM
    v[a] = F(1); v[b] = F(s)
    return v

prim_all = [(a, b, s) for a, b in itertools.combinations(range(1, DIM), 2) for s in (1, -1)]

# annihilation: X*Y = 0 (ordered, since ZD annihilation is direction sensitive)
ann_ordered = []
for (a, b, s) in prim_all:
    X = vec(a, b, s)
    for (c, d, t) in prim_all:
        if vmul(X, vec(c, d, t)) == [F(0)] * DIM:
            ann_ordered.append(((a, b, s), (c, d, t)))

zd_units = set()
for p, q in ann_ordered:
    zd_units.add(p); zd_units.add(q)

# --- Definition probes -------------------------------------------------
print("DEFINITION PROBES")
print(f"  # primitive imaginary-pair elements total (a<b, +/-): {len(prim_all)}")
print(f"  # distinct primitive units that are ZD (annihilate something): {len(zd_units)}")
print(f"  # ordered annihilating pairs X*Y=0: {len(ann_ordered)}")

unord = set(frozenset((p, q)) for p, q in ann_ordered if p != q)
print(f"  # unordered annihilating pairs: {len(unord)}")

axes_zd = set((a, b) for (a, b, s) in zd_units)
print(f"  # distinct axis-pairs {{a,b}} appearing in ZD units (ASSESSORS): {len(axes_zd)}")

# Both signs present per axis?
from collections import Counter
axis_signs = {}
for (a, b, s) in zd_units:
    axis_signs.setdefault((a, b), set()).add(s)
both = sum(1 for v in axis_signs.values() if v == {1, -1})
print(f"  # axes where BOTH +e_b and -e_b are ZD units: {both}  (of {len(axis_signs)})")

# So: 42 axes, each with 2 signs => 84 primitive units. 84 units pair up.
# de Marrais '168' and '84': two competing conventions exist in the literature.
#   - If "primitive unit ZD" counts e_a +/- e_b for a<b only: 84 units.
#   - If it counts ORDERED (e_a+e_b annihilates left vs right separately) or counts
#     a,b in BOTH orders (e_a+e_b and e_b+e_a as distinct labels): doubles to 168.
# Probe: how many ordered axis labels (a,b) with a!=b (both directions) carry ZD?
axes_ordered = set()
for (a, b, s) in zd_units:
    axes_ordered.add((a, b)); axes_ordered.add((b, a))
print(f"  # ordered axis labels (a,b),(b,a): {len(axes_ordered)}  (= 2 x assessors = 84)")
print(f"  # primitive units counting e_a+e_b and e_b+e_a separately: {2*len(zd_units)}  (=168)")

# --- Box-kites: connected components of the assessor annihilation graph -----
# Build a graph on the 42 assessors (axis-pairs). Two assessors are connected if
# some orientation of one annihilates some orientation of the other.
assessors = sorted(axes_zd)
adj = {A: set() for A in assessors}
for p, q in ann_ordered:
    A = p[:2]; B = q[:2]
    if A != B:
        adj[A].add(B); adj[B].add(A)

# connected components
seen = set()
components = []
for A in assessors:
    if A in seen: continue
    stack = [A]; comp = set()
    while stack:
        x = stack.pop()
        if x in seen: continue
        seen.add(x); comp.add(x)
        stack.extend(adj[x] - seen)
    components.append(comp)

print("\nBOX-KITE STRUCTURE (connected components of assessor annihilation graph)")
print(f"  # connected components: {len(components)}")
print(f"  component sizes: {sorted(len(c) for c in components)}")

# de Marrais strut-constant: each box-kite is indexed by the XOR of the two indices
# of any assessor in it? Let's test: for each assessor (a,b), compute a XOR b, and
# also compute the "strut constant" = the high-bit pattern. In the CD/twisted-group
# picture, e_a*e_b = +/- e_{a XOR b} when they live in same octonion; the ZD couplings
# come from the index XOR with the doubling bit 8.
print("\n  per-assessor index XOR (a^b):")
for comp in components:
    xors = sorted(set(a ^ b for (a, b) in comp))
    print(f"    size {len(comp):2d}  XOR-values {xors}  assessors {sorted(comp)}")
