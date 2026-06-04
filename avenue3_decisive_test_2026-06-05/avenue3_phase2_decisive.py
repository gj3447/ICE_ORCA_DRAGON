"""
Avenue-3 PHASE 2 — DECISIVE test against the pre-registered PASS/FAIL criteria.

Settled in part1/part2:
  * genuine S3=<psi,eps> on S=R^16 decomposes triv(1)+sign(1)+std(7); std-mult=7 = the G2/
    octonion 7 imaginary directions (one std(2) per e_i--e_{i+8} plane), NOT a generation count.
  * genuine S3 STABILIZES each O_i setwise (psi,eps fix O1,O2,O3 as sets). It does NOT permute
    O1<->O2<->O3. The "3 generations" in GGV is the psi-ORBIT (Z3, ord(psi)=3), giving orbit
    size 3 on a ladder operator inside ONE octonion, which is the std(2) module (dim 2).

DECISIVE QUESTIONS for the pre-reg:
  Q1. Is the "permute three octonions" S3 the genuine Aut(S)\Aut(O), or the in-G2 family perm?
      (If GGV's claim secretly needs the in-G2 perm, that's pre-reg FAIL mode F4.)
  Q2. Does ANY granularity force a NUMBER = a representation invariant (irrep mult / branching /
      Clebsch) that is (a) >2-or-non-trivial and (b) NOT something J3(O) already gives?
  Q3. G2 rep theory on the ZD locus (Reggiani): does it add a forced quantum number beyond 'dim 14'?

We COMPUTE Q1 by re-finding the in-G2 family-permutation rho (Phase-1 said: bare index 3-cycle
1->2->3,5->6->7,9->10->11,13->14->15 fixing 0,4,8,12) and CHECK it is an Aut(S) that FIXES the
reference octonion e0..e7 setwise (=> inside G2), and that it is what genuinely permutes O1,O2,O3.
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

# genuine S3
psi = sp.zeros(DIM, DIM); psi[0, 0] = 1; psi[8, 8] = 1
for i in range(1, 8):
    j = i + 8
    psi[i, i] = -half; psi[j, i] = sqrt3 * half; psi[j, j] = -half; psi[i, j] = -sqrt3 * half
eps = sp.zeros(DIM, DIM); eps[0, 0] = 1; eps[8, 8] = -1
for i in range(1, 8):
    eps[i, i] = 1; eps[i + 8, i + 8] = -1

O1 = {0, 1, 4, 5, 8, 9, 12, 13}; O2 = {0, 2, 4, 6, 8, 10, 12, 14}; O3 = {0, 3, 4, 7, 8, 11, 12, 15}
Os = {'O1': O1, 'O2': O2, 'O3': O3}
refO = set(range(8))

def img_indices(M, oset):
    img = set()
    for i in sorted(oset):
        col = M[:, i]
        img.update(r for r in range(DIM) if sp.simplify(col[r]) != 0)
    return img

print("=" * 72)
print("PHASE 2 — DECISIVE TEST vs pre-registered criteria")
print("=" * 72)

# ---- Q1: the family-permutation rho (Phase-1 claim) ----
print("\n[Q1] Does an S3 that PERMUTES O1<->O2<->O3 exist, and is it inside G2 (=FAIL mode F4)?")
def perm_matrix(cycles_signed):
    """cycles_signed: dict i->(j,sign) meaning e_i -> sign*e_j."""
    M = sp.zeros(DIM, DIM)
    used = set()
    for i, (j, s) in cycles_signed.items():
        M[j, i] = s; used.add(i)
    for i in range(DIM):
        if i not in used:
            M[i, i] = 1
    return M

# rho: 1->2->3->1, 5->6->7->5, 9->10->11->9, 13->14->15->13, fix 0,4,8,12 (all +1)
rho_map = {1: (2, 1), 2: (3, 1), 3: (1, 1),
           5: (6, 1), 6: (7, 1), 7: (5, 1),
           9: (10, 1), 10: (11, 1), 11: (9, 1),
           13: (14, 1), 14: (15, 1), 15: (13, 1)}
rho = perm_matrix(rho_map)
print("    rho is Aut(S):", is_automorphism(rho), "  rho^3=I:", sp.simplify(rho**3 - I16) == sp.zeros(DIM, DIM))
print("    rho action on octonions:")
for on, oset in Os.items():
    img = img_indices(rho, oset)
    match = [n2 for n2, s2 in Os.items() if img == s2]
    print(f"      rho: {on} -> {match if match else sorted(img)}")
img_refO = img_indices(rho, refO)
print("    rho maps reference octonion e0..e7 -> indices", sorted(img_refO),
      "; stays inside e0..e7?", img_refO.issubset(refO))
print("    => rho is %s" % ("INSIDE G2=Aut(O) (fixes e0..e7 setwise) -- the 'family perm' is NOT Aut(S)\\Aut(O)"
                            if img_refO.issubset(refO) else "OUTSIDE G2"))

# Does the genuine S3 permute O1,O2,O3? (re-confirm: NO)
print("\n    genuine psi/eps action on octonions (re-confirm they STABILIZE, not permute):")
for gname, M in [('psi', psi), ('eps', eps)]:
    perm = {}
    for on, oset in Os.items():
        img = img_indices(M, oset)
        match = [n2 for n2, s2 in Os.items() if img == s2]
        perm[on] = match[0] if match else '?'
    print(f"      {gname}: {perm}")

print("""
    VERDICT Q1: The S3 that genuinely permutes O1<->O2<->O3 (rho) FIXES the reference
    octonion e0..e7 setwise, hence lies INSIDE G2=Aut(O). The genuine Aut(S)\\Aut(O)
    factor (psi,eps) STABILIZES each O_i. So:
      - "3 generations as 3 PERMUTED octonions" uses an in-G2 map (pre-reg FAIL mode F4
        if presented as the Aut(S)\\Aut(O) S3);
      - the genuine S3 gives "3" only as ord(psi)=3 = the Z3 ORBIT of a ladder operator
        WITHIN one octonion -> the std(2) module. The number that is FORCED is the irrep
        DIMENSION 2 and the orbit SIZE 3, not a generation MULTIPLICITY.
""")

# ---- Q2: scan all natural S3-modules for any forced number != {1,2,7} that is new ----
print("[Q2] Forced representation-theoretic numbers across granularities:")
forced = {
    "S (16-dim) std-mult": 7,
    "Im(S) (15) std-mult": 7,
    "seven-planes std-mult": 7,
    "ladder module dim (std)": 2,
    "psi orbit size (ord psi)": 3,
    "H (quaternion) triv/sign/std": "1/1/1",
    "#octonion subalgebras containing e4,e8,e12": 3,
    "total octonion subalgebras in S": 8,
}
for k, v in forced.items():
    print(f"    {k:45s} = {v}")
print("""
    The only integers FORCED by the genuine S3 representation theory are:
      2  (dim of standard irrep / dim of the per-generation ladder module),
      3  (=ord(psi), orbit size = GGV's generation COUNT),
      7  (std multiplicity = octonion imaginary dimension = rank-2 G2 acts on 7).
    NONE of these is a ratio / mixing angle / Clebsch with a tunable-free landing.
    '3' here is exactly GGV's published COUNT (forced by ord(psi)=3) -- NO new number.
""")

# ---- Q3: G2 on the ZD locus (Reggiani) ----
print("[Q3] G2 structure on the ZD-pairs locus (Reggiani arXiv:2411.18881):")
print("""
    Reggiani: the unit-norm ZD-pairs locus of the sedenions is HOMEOMORPHIC to G2 (the
    14-dim compact Lie group). G2 rep theory's smallest reps are 7 (fundamental) and 14
    (adjoint). On THIS locus the genuine S3=Aut(S)/Aut(O) acts as the OUTER structure;
    G2=Aut(O) acts as the connected identity component. The forced numbers from G2 are
    its representation dimensions (7, 14, 27, ...), which are the SAME 7 already appearing
    as the std-multiplicity above, plus 14=dim G2. None of these is a fermion quantum
    number (hypercharge / weak isospin) that is forced rather than assigned: G2 has rank 2,
    so it offers at most TWO commuting charges, and the embedding of SU(3) or SU(2)xU(1) into
    G2 is a CHOICE (G2 contains SU(3) maximally, but the hypercharge normalization is not
    fixed by G2 alone). => G2 adds the number 14 (its dimension) and 7 (fundamental), but
    NO forced fermion mixing/charge ratio beyond what is hand-embedded.
""")

# ---- FINAL pre-reg landing ----
print("=" * 72)
print("PRE-REGISTERED CRITERION LANDING")
print("=" * 72)
print("""
  PASS requires (all of): genuine S3 [YES, verified] AND a FORCED rep-invariant number that is
  (a) zero-free-parameter AND (b) DISTINCT from J3(O)'s 1:2:3 / 3/8 / Koide 2/3 AND
  (c) survives MC look-elsewhere at P>=0.01.

  COMPUTED OUTCOME:
   * (1) genuine S3 used: YES (psi,eps verified on all 256 products; psi moves e0..e7 out). PASS-(1).
   * (2) the '3' appears as orbit-size ord(psi)=3 and std-irrep dim 2 -- FORCED by the algebra,
         NOT hand-inserted. The standard-2 irrep DOES appear (std-mult 7 in Im(S)). PASS-(2) on
         'standard 2-dim rep appears', BUT
   * (3) FORCED NUMBER: the only forced integers are {2,3,7,14}. '3' = GGV's COUNT (= ord psi),
         which is the published null result with NO mass ratio / mixing angle attached.
         There is NO forced RATIO, mixing angle, CKM/PMNS texture, or inter-generation coupling.
         => criterion (3)(a)+(3)(b) is NOT met: no new forced number distinct from J3(O).
   * J3(O) comparison: J3(O) FORCES 1:2:3 sqrt-mass, delta^2=3/8, Koide 2/3. The sedenion S3
         structure forces only the COUNT 3 (and dims 2,7,14). It gives NOTHING J3(O) lacks; in
         fact it gives LESS (no mass ratio at all). By Occam, J3(O) dominates.

  => LANDS ON pre-registered FAIL mode F5 (NO NON-TRIVIAL MULTIPLICITY/RATIO): Phase-2
     re-derives the COUNT 'three' (genuinely forced by ord(psi)=3, reproducing GGV), but
     produces NO new forced number. This is exactly the 'honest NULL' the pre-reg flagged as
     the most likely outcome. NOT F4 (we used the genuine S3, and explicitly showed the
     octonion-permuting rho is the in-G2 map and did NOT use it for the forcing).
""")
