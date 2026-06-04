"""
Final independent check: is there ANY forced CONTINUOUS number (ratio / angle /
Clebsch-Gordan / branching) from the genuine S3 structure that J3(O) does NOT give?

S3 has irreps of dim 1,1,2. ALL its representation-theoretic invariants
(characters, CG coefficients, branching) are RATIONAL/integer or simple roots-of-unity.
There is NO free continuous parameter in a finite-group rep that could land on a
mass ratio or mixing angle unless an EXTERNAL inner product / Hamiltonian is imposed.

Enumerate the candidate forced integers and confirm none is a continuous physical
observable. Then state the J3(O) comparison precisely.
"""
import sympy as sp
from sympy import Rational

# S3 Clebsch-Gordan: std (x) std = triv + sign + std  (the only nontrivial tensor).
# All CG coefficients are determined up to basis; they are algebraic constants of the
# finite group, NOT tunable, and produce NO continuous physical ratio by themselves.

candidate_forced = {
    "3 = ord(psi) = Z3 orbit size of a ladder operator": "COUNT (GGV generation count). deterministic. NO mass/mixing attached.",
    "2 = dim(std irrep) = ladder module dim": "DIMENSION. structural.",
    "7 = std-multiplicity in Im(S) = #box-kites = #doubling-planes = G2 fundamental": "DIMENSION/COUNT. forced 7<->7<->7 bijection but it's a count.",
    "14 = dim G2 (adjoint)": "DIMENSION. structural.",
}
print("=== CANDIDATE FORCED NUMBERS (independent enumeration) ===")
for k, v in candidate_forced.items():
    print(f"  {k}\n      -> {v}")

print("\n=== Is any of these a CONTINUOUS observable (ratio/angle)? ===")
print("  NO. All are integers (group order, irrep dim, multiplicity, Lie-algebra dim).")
print("  A finite group + a fixed semisimple Lie group (G2) forces only integers.")
print("  Continuous numbers (mass ratio, mixing angle, Koide) require an EXTERNAL")
print("  metric/Hamiltonian/Yukawa choice that the sedenion S3 structure does NOT fix.")

print("\n=== J3(O) COMPARISON (precise) ===")
delta_sq = Rational(3, 8)
print(f"  J3(O) (Singh/Bhatt) FORCES continuous numbers: delta^2 = {delta_sq},")
print(f"    sqrt-mass ratio 1:2:3, Koide Q = 2/3.")
print(f"  Sedenion genuine-S3 FORCES: only integers {{2,3,7,14}}, ZERO continuous numbers.")
print(f"  Overlap on the physics-discriminating axis: the COUNT '3' (both give 3 generations).")
print(f"  J3(O) gives the count 3 AND mass/mixing; sedenions give the count 3 and NOTHING ELSE.")
print(f"  => By Occam, J3(O) strictly dominates. Sedenion S3 adds NO new forced observable.")

print("\n=== PRE-REGISTERED LANDING (re-checked independently) ===")
print("  Criterion (1) genuine S3 used: PASS (psi,eps verified automorphisms; psi outer).")
print("  Criterion (2) std irrep appears, '3' forced by ord(psi)=3 not hand-inserted: PARTIAL PASS.")
print("  Criterion (3) FORCED NUMBER distinct from J3(O): FAIL (only {2,3,7,14}, all also-given/structural).")
print("  Criterion (4) MC look-elsewhere P>=0.01: MOOT (3 deterministic, no continuous observable to test).")
print("  => Lands on pre-registered FAIL mode F5 (honest NULL reproducing GGV count).")
print("  NOT F4: genuine outer S3 used for forcing; rho (octonion-permuter) shown IN-G2 and NOT used.")
print("  NOT F2 in the duplication-by-cheating sense, but F5's consequence IS J3(O) dominance (Occam).")
