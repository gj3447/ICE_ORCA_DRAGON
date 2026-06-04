"""
Three octonion subalgebras inside S (Gresnigt-Gourlay-Varma 2023, arXiv:2306.13098)
and the genuine S3 = Aut(S)/Aut(O) that permutes them.

Strategy:
  1. Identify octonion subalgebras of S = 8-dim subspaces span{e0, e_{i1..i7}} that are
     closed under multiplication AND alternative (so genuinely O, not just closed).
  2. GGV use the COMPLEX sedenion; the three generations are three O subalgebras that
     SHARE a common quaternion (or the e0..e7 'reference' octonion) and are permuted by S3.
  3. Find Aut(S): permutation-with-signs maps phi on basis that preserve the product
     table. Then identify the subgroup that fixes e1..e7 setwise (=G2 part lands in
     Aut(O)) vs the part that permutes the THREE octonions (the extra S3).
"""
import itertools
from fractions import Fraction as F
from avenue3_phase1_groundtruth import build_table, DIM

table = build_table()
# integer sign table for speed
T = [[table[i][j] for j in range(DIM)] for i in range(DIM)]

def basis_mul(i, j):
    return T[i][j]  # (k, sign)

# ----------------------------------------------------------------------
# 1. Find all octonion subalgebras: 7-subsets S of {1..15} such that
#    span{e0} + span{e_s : s in S} is closed under multiplication and alternative.
#    A 7-set of imaginary units forms an octonion iff it is closed under the
#    "multiplication-up-to-sign" (a Fano-like structure) and alternative.
# ----------------------------------------------------------------------
def is_octonion_index_set(S):
    """S: frozenset of 7 imaginary indices. Closed under +/- product & alternative."""
    Sset = set(S)
    # closure up to sign and reality: e_a*e_b must be +/- e_c with c in S (a!=b), and e_a^2=-e0
    for a in Sset:
        for b in Sset:
            if a == b:
                continue
            k, s = basis_mul(a, b)
            if k == 0:  # would mean e_a*e_b is scalar => only if a==b
                return False
            if k not in Sset:
                return False
    # alternative test inside the subalgebra (left & right alternative on basis sums)
    # Build vmul restricted; cheaper: test associator (x,x,y) for x=e_a+e_b, y=e_c.
    def vmul(u, v):
        res = [F(0)] * DIM
        for i in range(DIM):
            if u[i] == 0: continue
            for j in range(DIM):
                if v[j] == 0: continue
                k, sg = T[i][j]
                res[k] += u[i] * v[j] * sg
        return res
    idxs = sorted(Sset)
    for a, b in itertools.combinations(idxs, 2):
        x = [F(0)] * DIM; x[a] = F(1); x[b] = F(1)
        for c in idxs:
            y = [F(0)] * DIM; y[c] = F(1)
            if vmul(vmul(x, x), y) != vmul(x, vmul(x, y)):
                return False
            if vmul(vmul(y, x), x) != vmul(y, vmul(x, x)):
                return False
    return True

print("Searching all 7-subsets of {1..15} that form octonion subalgebras...")
oct_sets = []
for S in itertools.combinations(range(1, DIM), 7):
    if is_octonion_index_set(frozenset(S)):
        oct_sets.append(frozenset(S))
print(f"  # octonion subalgebras found: {len(oct_sets)}")
# The reference one:
ref = frozenset(range(1, 8))
print(f"  reference {{1..7}} is octonion: {ref in oct_sets}")

# ----------------------------------------------------------------------
# 2. GGV three-octonion construction.
#    GGV: in the complex sedenion, define three octonion subalgebras that each
#    contain a fixed quaternion and are permuted by S3. A natural realization:
#    take the e0..e7 octonion as 'reference', and two more octonions obtained by
#    'rotating' the doubled (8..15) part. Concretely GGV's three O's pairwise
#    intersect in a common quaternion-ish/complex subalgebra.
#
#    We DERIVE the three from the box-kite/S3 orbit structure rather than hand-pick:
#    look for a triple of octonion index-sets that (a) pairwise intersect in the SAME
#    sub-set and (b) are permuted by a common automorphism (computed in step 3).
# ----------------------------------------------------------------------
print(f"\n  All octonion index sets (sample): {[tuple(sorted(s)) for s in oct_sets[:8]]}")
# How do they intersect with {1..7}?
contain_quat = {}
for s in oct_sets:
    inter = tuple(sorted(s & ref))
    contain_quat.setdefault(len(inter), 0)
    contain_quat[len(inter)] += 1
print(f"  intersection-size-with-{{1..7}} histogram: {contain_quat}")

# ----------------------------------------------------------------------
# 3. Find Aut(S) as signed permutations of e1..e15 preserving the product table.
#    This is expensive in general; we instead VERIFY a specific S3 that GGV/Eakin-
#    Sathaye predict, and confirm it permutes three octonions and preserves mult.
#
#    Eakin-Sathaye 1990: Aut(S) = G2 x S3. The S3 acts on the 'doubling' structure.
#    A clean generating set for the S3: it permutes the three "imaginary quaternionic
#    triples" in the doubled part / equivalently the three octonions sharing e1..e3.
# ----------------------------------------------------------------------
# Save octonion sets for the S3 search
import json
with open("avenue3_octonion_sets.json", "w") as f:
    json.dump([sorted(s) for s in oct_sets], f)
print(f"\n  saved {len(oct_sets)} octonion index sets to avenue3_octonion_sets.json")
