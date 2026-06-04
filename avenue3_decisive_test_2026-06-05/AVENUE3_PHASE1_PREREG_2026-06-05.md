# Avenue-3 Phase 1 — Ground Truth + PRE-REGISTRATION (2026-06-05)

> Decisive test: does the sedenion ZD locus carry a FORCED 3-generation flavor
> structure with a non-trivial multiplicity/ratio that GGV did NOT hand-assign and
> J3(O) does NOT already give? This file is the CONTRACT Phase 2 must honor.
> Every number below was COMPUTED (exact rational/sympy arithmetic), not asserted.

## CD convention (FIXED)
`(a,b)(c,d) = (a c - conj(d) b, d a + b conj(c))`. Basis e0..e15; e1..e7 = reference octonion.
Verified: e0 identity; e_i^2 = -1 (i>=1); non-commutative; non-associative; non-alternative
(genuine sum-based test: associator (e1+e10, e1+e10, e4) = -2 e15 != 0); octonion subalgebra
e0..e7 IS alternative.

## Verified ZD counts (avenue3_phase1_SUMMARY.py)
| quantity | computed | de Marrais |
|---|---|---|
| Assessors (distinct axis-pairs {a,b}) | **42** | 42 |
| primitive units e_a+/-e_b (a<b) that are ZD | **84** | (= 2 x 42) |
| primitive ZDs counting both index orders | **168** | 168 |
| standard ZD pairs (e_a+e_b)(e_c+e_d)=0, 4 distinct idx, + signs | **84** | 84 |
| ordered annihilating pairs X*Y=0 | **336** | — |
| box-kites (connected components) | **7**, each 6 assessors | 7 |

### 42-vs-84 RESOLUTION (definitive)
ICE docs ("42 ZD pairs") conflated the **Assessor count (42)** with the **pair count**.
42 = assessors. The pair count is **84** (canonical de Marrais) or **168** (both-order /
unordered annihilating units). The deep-dive flag was CORRECT.

## Three octonion subalgebras (GGV eqns 24-26/56-58; all confirmed in my list of exactly 8)
- O1 = {e0,e1,e4,e5,e8,e9,e12,e13}
- O2 = {e0,e2,e4,e6,e8,e10,e12,e14}
- O3 = {e0,e3,e4,e7,e8,e11,e12,e15}
- O1 ∩ O2 ∩ O3 = {e0,e4,e8,e12} = quaternion H. (eqn 27)

## Genuine S3 = Aut(S)\Aut(O) (avenue3_phase1_genuine_s3_final.py / SUMMARY)
- psi (order 3): 2pi/3 rotation in the seven e_i--e_{i+8} planes;
  psi(e_i)=-1/2 e_i + (sqrt3/2) e_{i+8}, psi(e_{i+8})=-1/2 e_{i+8} - (sqrt3/2) e_i, psi(e8)=e8.
  VERIFIED genuine Aut(S) (phi(xy)=phi(x)phi(y) on all 256 basis products); psi^3=I; maps
  e0..e7 OUTSIDE e0..e7 => genuinely NOT Aut(O).
- eps (order 2): eps(e_i)=e_i, eps(e_{i+8})=-e_{i+8}, eps(e8)=-e8. VERIFIED Aut(S); eps^2=I;
  eps psi eps = psi^-1. |<eps,psi>| = 6 = S3.
- Inner automorphisms x->e_u x e_u^-1 are NONE (S non-associative) — eps is not inner.
- This genuine S3 STABILIZES each O_i setwise. The "3 generations" = the **orbit of size 3**
  of psi acting on a ladder operator A_i (each A_i stays in its own O_i; orbit {A_i, psi A_i,
  psi^2 A_i} has size 3). The "3" is FORCED by ord(psi)=3 (A3 = Z3 = unique nontrivial cyclic
  normal subgroup of S3). VERIFIED on GGV ladder ops A1,A2,A3 (eqns 59-61).
- SEPARATE caveat: a "family permutation" S3 = <rho,tau> that permutes O1<->O2<->O3 as SETS
  also exists and is a genuine Aut(S), BUT it fixes the reference octonion e0..e7 setwise
  (Fano-plane triality) => it sits INSIDE G2=Aut(O), so it is NOT the Aut(S)\Aut(O) factor.
  Do NOT confuse the two.

---

# PRE-REGISTRATION (written BEFORE any Phase-2 decomposition)

## What must be tested
A decomposition of the 42-assessor / 7-box-kite ZD locus (or the C(x)S ladder-operator
representation) UNDER the genuine S3 = <eps,psi>, asking whether it FORCES a 3-generation
flavor structure carrying a non-trivial multiplicity or ratio.

## PASS criterion (first real signal) — ALL of the following, fixed in advance
1. The S3 used is EXACTLY the verified genuine Aut(S)\Aut(O) = <eps,psi> above
   (psi^3=I, eps^2=I, eps psi eps=psi^-1, psi moves e0..e7 out of e0..e7). No other map.
2. Decomposing the ZD locus (42 assessors / 168 primitive units / 7 box-kites) OR the
   ladder-operator module as an S3-representation yields a multiplicity structure whose
   "3" appears as the dimension/multiplicity of an S3-irrep ORBIT (the 2-dim standard rep
   appearing, or a regular-rep copy), i.e. the 3 is the S3-orbit count psi forces — NOT a
   number put in by hand and NOT merely "168/56=3" style arithmetic.
3. The decomposition produces a FORCED NUMBER that is:
   (a) a representation-theoretic invariant (an irrep multiplicity, a branching ratio of
       dimensions, a fixed Clebsch-Gordan / character-table entry), determined entirely by
       S3 + the algebra, with ZERO free parameters chosen to land on it; AND
   (b) something J3(O) does NOT already give. J3(O) (Singh/Bhatt) already forces delta^2=3/8,
       sqrt(m) ratios 1:2:3, Koide 2/3. A PASS number must be DISTINCT from {3/8, 1:2:3, 2/3,
       Koide} — e.g. a mixing-angle constraint, a CKM/PMNS texture zero, an inter-generation
       coupling ratio, or a degeneracy-lifting pattern that J3(O) is silent on.
4. The number survives a MC null / look-elsewhere check (numerology_mc_judge.py protocol):
   P(E~H) >= 0.01 after look-elsewhere correction over the catalogue of S3-invariants that
   COULD have been reported.

## FAIL criterion — ANY of the following kills it
- F1 POST-HOC LABELING: the "3" is obtained by counting O1,O2,O3 (or 42=6x7, 168=...) and
  then NAMING it "3 generations" with no representation forcing it. Counting-then-labeling
  is not a forced multiplicity.
- F2 J3(O) DUPLICATION: the only forced number reproduces something J3(O) already gives
  (3/8, 1:2:3, Koide 2/3) — then sedenions ADD NOTHING; the simpler J3(O) wins (Occam).
- F3 LOOK-ELSEWHERE DEATH: the number passes only because many candidate S3-invariants were
  scanned and one happened to match; P(E~H) < 0.01 after correction => NUMEROLOGY_HOLD.
- F4 WRONG S3: the structure uses the family-permutation <rho,tau> (inside G2) or any
  hand-picked permutation instead of the genuine <eps,psi>, OR a map not verified to satisfy
  phi(xy)=phi(x)phi(y). Then it is not an Aut(S)\Aut(O) result at all.
- F5 NO NON-TRIVIAL MULTIPLICITY/RATIO: GGV's published result is a COUNT (three) with NO
  forced mass ratio / mixing angle. If Phase 2 only re-derives "three" with no new number,
  that REPRODUCES GGV (valid) but is NOT a PASS for "forced flavor structure" — it is the
  honest NULL: "S3 forces three generations as a count; it does NOT force a flavor ratio."

## Honest prior (stated now)
Most likely Phase-2 outcome by the literature: GGV themselves report only the count "three"
and explicitly NO forced mass ratio/mixing angle. The genuine expectation is F5 (the count is
real and forced by ord(psi)=3, but no non-trivial flavor number is forced). A genuine PASS
would be a NEW result beyond both GGV and J3(O). This prereg is designed so that re-deriving
"three" cannot be dressed up as a PASS.
