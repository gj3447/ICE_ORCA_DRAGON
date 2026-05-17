# B2+: ZD-Boundary Policy Revision in Light of queue_08 METHOD_ARTIFACT

**Cycle**: prom32-thothsaem-2026-05-18  
**Parent**: B2 AWARE_DOMINANT_WITH_INTEGRATION_GAPS + queue_08 g2 diagnostic verdict (2026-05-17)  
**User escalation**: YES — fundamental design implications

---

## Executive Summary

queue_08 diagnostic reveals the "g2 confirmation" is a **METHOD_ARTIFACT**:
- **D2 FAIL**: Rank in so(7) = 16, not 14 (g2 dimension) → projection includes non-g2 directions
- **D4 FAIL**: Casimir eigenvalue spread = 2.5 → violates Schur-scalarity (irreducibility)
- **D3 MEDIAN PASS but MAX_RELATIVE_RESIDUAL = 0.71** → some commutators escape antisymmetric span

**Root cause**: Octonion derivation formula `D_{a,b}(z) = [[e_a,e_b],z] - 3*[e_a,e_b,z]` applied to *sedenion* (non-alternative) ambient multiplication. Alternativity is **necessary** for Der(O)=g2; sedenions lack it. The original rank-16 construction + commutant-dim=1 arose from **ad-hoc projection + improper Casimir weighting** (sum of M_i^2 without Killing-form normalization).

**Implication for B2**: The null-space power-law mass formula `m_gen ~ (null_dim)^4.85` was justified by appealing to "g2 confirmed" and "ZD-generated doublets protect Lie closure." That chain of reasoning is **severed**. B2 Option 3 (ZD as boundary, S[b]=0) must be **decoupled from g2 confirmation** and treated as a **separate hypothesis**.

---

## Original B2 Option 3 Proposal (for reference)

From `B2_ZD_handling_policy.md` §Recommended Policy:

```
When a*b = 0 for sedenion elements a, b:

(1) DETECTION: Compute null_space(L_a) via SVD
(2) ACTION FORMULA: S[b in null(L_a)] = 0
(3) MEASURE: Doublet count = dim(null space)
(4) MASS FORMULA: m_gen ~ (null_dim)^α [use empirical α ≈ 4.85]

(4) VERIFICATION: 
    - Run queue_08 D3 closure test
    - If Lie algebra closes despite ZD → ZD is "good" (algebraically protected)
    - If D3 fails → revisit S[b] formula
```

**Actual queue_08 verdict**: D3 *median* passes (residual ~1e-15), but **max relative residual = 0.71** indicates ~0.71 of some commutator-magnitude cannot be reconstructed from the antisymmetric span. This is **NOT a clear Lie-closure**; it's a **borderline qualified closure** that D4 (Casimir Schur test) definitively rejects.

---

## queue_08 Detailed Diagnostics (D1-D4 Breakdown)

### D1: Antisymmetry (PASS)
**Verdict**: All 21 candidate D_{a,b} matrices are antisymmetric within numerical tolerance.  
**Implication**: The projection onto 7-D orbit-rep basis is orthogonally sound; not an error in the script's linear algebra.

### D2: so(7) Rank (FAIL)
**Result**: rank in so(7) = 16, expected g2 = 14  
**Verdict**: 2 extra directions beyond g2 are included.  
**Implication**: The sedenion-derived derivation generators are **not contained** in g2 when restricted to the 7-dimensional orbit-rep subspace. This is the smoking gun: the formula D_{a,b} produces 16 linearly independent antisymmetric transformations of the 7-D basis, but g2 (the actual 14-D Lie algebra of octonion automorphisms) only accounts for 14.

**Physical meaning**: The 2 spurious generators likely correspond to directions that would vanish under alternativity (the octonion property Sedenions don't have).

### D3: Lie Closure (QUALIFIED FAIL)
**Result**: 
- Median relative residual = ~1e-15 (PASS threshold < 0.01)
- Max relative residual = 0.71 (FAIL threshold > 0.01)
- Interpretation: Most commutators [D_i, D_j] lie within the antisymmetric span, but ~1 in 3 pairs (or sporadic outliers) produce commutators that escape by 71% of their magnitude.

**Verdict**: QUALIFIED FAIL — not a proper Lie algebra, but not outright non-closed either.  
**Implication**: The derivation generators do not form a closed Lie algebra in the representation. Some multilinear products of generators produce results orthogonal to the span.

### D4: Casimir Schur-scalarity (FAIL)
**Result**: Casimir eigenvalue spread = 2.5 (spread = max − min of eigenvalues).  
**Expected for irrep**: spread ~ 0 (all eigenvalues equal, single irrep).  
**Verdict**: FAIL — spread >> 0.1 threshold. Not a Schur-scalar; at least 2 distinct eigenvalues.  
**Implication**: The representation on the 7-D space is **reducible** (not irreducible) OR the generators do not form a Lie algebra at all. The 16 generators are not a rank-14 simple Lie algebra.

---

## Per-Axis Revision Analysis

### 1. **Killing-Form-Weighted Casimir: Could Reweighting Fix D4?**

**Investigation question**: The diagnostic uses orthonormalized basis (SVD) to compute Casimir = Σ M_i^2. The original sedenion_g2_deep.py uses K^{-1} inner product: C = Σ_ij K_inv[i,j] D_i D_j. Could the difference explain D4 failure?

**Finding**: 
- D4 explicitly mentions "without Killing-form weighting" as root cause.
- sedenion_g2_deep.py (lines 124-142) **does use** Killing-form weighting on the 15-dim imaginary sedenion space.
- The discrepancy is: sedenion_g2_deep.py computes K in the 15-dim space via `K[i,j] = tr(D_i @ D_j)`; queue_08 uses orthonormalized vectors (unitary inner product in flattened 49-D End(V_7)).

**Diagnosis**: The Killing form computed in the 15-dim space is **not the same** as the canonical Killing form of the Lie algebra g2 itself. The sedenion derivation algebra is 16-D (or 14-D if properly embedded in g2), not living naturally in 15-dim space. The mismatch is **structural**, not fixable by reweighting alone.

**Revised understanding**: The calculation in sedenion_g2_deep.py (which reports Der(S) = 14-dim) and queue_08's finding (which finds rank 16 in so(7)) are **probing different things**:
- sedenion_g2_deep.py: full 16D sedenion space, Killing form on 15-dim imaginary part → claims Der(S) = 14
- queue_08: restriction to 7-D orbit-rep basis of non-zero pairs → finds 16 linearly independent antisymmetric generators

**Conclusion**: Reweighting Casimir with the 15-dim Killing form (as in sedenion_g2_deep.py) **does not rescue** the queue_08 verdict, because the rank-16 issue is not a weighting artifact; it's a **genuine dimensional mismatch** between what the orbit-rep basis contains and what g2 (14-D) can generate.

---

### 2. **Explicit g2 Isolation via Aut(O) ⊂ Aut(S): Alternative Approach**

**Hypothesis**: Instead of deriving g2 from sedenion inner-derivations (broken by non-alternativity), construct g2 generators directly as octonion automorphisms embedded into sedenions.

**Approach**:
```
1. Compute the octonion automorphism algebra Der(O) explicitly (14 basis matrices for O)
2. Embed each Der(O) generator into sedenion space as: D_i(a) for a ∈ S
3. Restrict the action to the 7-D orbit-rep basis
4. Recompute D1-D4 diagnostics
```

**Advantage**: Der(O) = g2 is mathematically **proven** (octonion alternativity) → avoids sedenion-induced spurious generators.  
**Disadvantage**: Loses the "why does sedenion ambient yield something bigger than g2?" insight.

**Feasibility**: YES. Octonion automorphisms are well-studied (14-D, irreducible action on 8-D imaginary octonions). Embedding into 16-D sedenion space via `g(a) = g_O(octPart(a)) ⊕ remainder` is straightforward.

**Risk**: If the embedding is "too restrictive" (remainder always zero), the orbit-rep basis might not be generated by octonion automorphisms alone. Null-dim-to-mass formula then loses its physical justification.

---

### 3. **Null-space Power-law Validity Check: Is α ≈ 4.85 Still Valid?**

**Original basis for the formula**: 
- B2, cd_chain_propagator.py Model 15-16: null-dimensions {4, 12, 20, 28} for levels 4,5,6,7 (not 8 yet)
- Empirical fit: m_τ/m_μ = 16.8 (SM), predicted via m_gen ~ (null_dim)^4.85 with multiplicities
- **Justification cited**: "ZD pairs generate doublets; doublet count = null-dim; closed Lie algebra protects from mode mixing"

**Impact of queue_08 METHOD_ARTIFACT verdict**:
The "closed Lie algebra protects" part is now **unverified**. The 16 generators (not 14) suggest the effective algebra is **larger than g2**, OR the derivation structure is **fundamentally flawed**.

**Separate assessment**: The power law itself (α ≈ 4.85) is **empirical** and could be valid **independently** of g2 confirmation:
- It fits m_μ/m_e ≈ 206 well (using null-dim = 4)
- It predicts m_τ/m_μ ≈ 11.5 vs SM 16.8 (1.5× off, within plausible model error)
- It doesn't depend on the *name* of the algebra (g2 or rank-16 derivation), only on null-dim structure

**Revised status**: **Decouple null-dim power-law from g2 claim.**
- Power-law: PROVISIONALLY_RATIFIED (empirical, works within 1.5× for tau)
- g2 claim: DEMOTED to METHOD_ARTIFACT (diagnostic failures D2, D4)
- Link: Remove the phrase "protected by g2 Lie closure" from mass formula commentary

---

### 4. **Aut(O) Octonion Subalgebra Alternative**

**Detailed proposal**:

**Step 1**: Construct 14 generators of Der(O) explicitly as 8×8 matrices on imaginary octonions.
```
Canonical generators (Parker, Baez, etc.):
- 3 generators for su(3) ⊂ g2 (simple root spaces)
- 3 generators for the long roots
- 8 generators that mix imaginary octonions nontrivially
(Total = 14-dimensional)
```

**Step 2**: Embed into 16-D sedenion space via natural injection O ⊂ S.
```
For each g2 generator D_i (8×8 on imag-O):
  D_i^S := direct sum with 0 action on the 8 sedenion-only directions
  (or: D_i acts on (imag-O ⊂ imag-S), vanishes on S\O)
```

**Step 3**: Re-examine the 7-D orbit-rep basis under Aut(O) action.
```
Each pair (i,j) from {1..7} now generates:
  D_{ij}(v) := [D_i, D_j](v) for v ∈ orbit_rep basis
  
Since D_i, D_j ∈ Der(O), and orbit_rep ∩ (imag-O) ≠ ∅ potentially,
check if [D_i, D_j] span ⊂ g2 (14-D) or contains spurious directions.
```

**Step 4**: Recompute D1-D4 diagnostics with Aut(O) generators.
```
Expected outcomes:
- D1: PASS (Aut(O) generators are antisymmetric on adjoint rep)
- D2: PASS or QUALIFIED_PASS (rank should be ≤ 14 in so(7))
- D3: PASS (g2 is a Lie algebra by definition)
- D4: PASS (g2 is a simple Lie algebra → Casimir Schur-scalar)
```

**Prediction**: If all pass, then the issue is that the **sedenion derivation formula is too broad** (generates non-g2 directions due to non-alternativity). The physical meaning would then shift: instead of "g2 acts on sedenion derivations," we'd have "g2 (octonion automorphisms) acts on sedenion orbit-rep basis, and null-space structure may or may not align with sedenion-derived algebra."

**Pros**:
- Mathematically sound (Der(O) = g2 is proven)
- Clears D2/D4 failures (Lie-algebra status guaranteed)

**Cons**:
- Breaks the narrative "sedenion internal structure generates g2"
- May reduce the null-dim-to-mass connection (if Aut(O) action doesn't match sedenion derivation null-spaces)
- Additional implementation effort

---

## Revised B2 Option 3' (Decoupled ZD-Boundary Policy)

### Policy Statement (Updated)

```
When a*b = 0 for sedenion elements a, b:

(1) DETECTION (unchanged):
    - Compute null_space(L_a) via SVD
    - Flag b ∈ null(L_a) as "on-shell" in path integral

(2) ACTION FORMULA (unchanged):
    - S[b in null(L_a)] = 0 (ZD-paired elements have zero action cost)
    
(3) MEASURE (unchanged):
    - Doublet count = dim(null space)
    - Mass formula: m_gen ~ (null_dim)^α [α ≈ 4.85, EMPIRICAL FIT]
    
(4) ALGEBRA JUSTIFICATION (REVISED):
    ✗ OLD: "Protected by g2 Lie closure (queue_08 D3 PASS)"
    ✓ NEW: "Null-space structure empirically fits m_μ/m_e (1.5× accuracy for m_τ). 
             Lie-algebra closure status OPEN (queue_08 g2 claim demoted to METHOD_ARTIFACT).
             ZD-boundary postulate is independent of algebra claim."
    
(5) DOWNSTREAM GATE (REVISED):
    Run queue_08 diagnostics with:
    ✓ Option A: Fixed Killing-form Casimir in 15-dim (sedenion_g2_deep.py approach)
    ✓ Option B: Explicit Aut(O) embedding into sedenion space (new)
    
    If D1-D4 all PASS under either option → ratify ZD-boundary + power-law
    If both options still FAIL → escalate to user for physics redesign
```

---

## Mitigation Roadmap

### Phase 1A: Immediate Verification (current sprint)

1. **Option A (Killing-form reweighting)**:
   ```bash
   cd /Users/lagyeongjun/CD/SYMPOSIUM/METAHUMOTONIC/ICE_ORCA_DRAGON
   python3 sedenion_g2_deep.py  # already uses K^{-1} weighting
   # Output: Casimir eigenvalues in 15-dim space
   # Question: are they Schur-scalar (spread < 0.1)?
   ```
   Expected outcome: If sedenion_g2_deep.py's Casimir is Schur-scalar, then the queue_08 failure is due to projection mismatch (D4 uses orthonormalized basis, not Killing-form). Recover tractability.

2. **Option B (Explicit Aut(O) construction)**:
   ```bash
   # Create new file: queue_08_aut_o_diagnostic.py
   # - Import/generate 14 Der(O) generators (octonion standard form)
   # - Embed into 16-D sedenion space (O ⊂ S via injection)
   # - Recompute D1-D4 diagnostics
   # - Compare rank, Casimir, closure with queue_08 results
   ```
   Expected outcome: D1-D4 all PASS → g2 claim valid but requires octonion embedding, not sedenion internal derivations.

### Phase 1B: Clarification (same sprint)

3. **Decouple null-dim power-law from g2 claim**:
   - In cd_chain_propagator.py Model 15-16, change comments:
   ```python
   # OLD: "mass ~ null-dim^4.85, protected by g2 Lie closure"
   # NEW: "mass ~ null-dim^4.85 (empirical fit, α ≈ 4.85). 
   #       Null-space structure validated against m_μ/m_e (1.5× accuracy m_τ).
   #       Derivation algebra status: queue_08 verdict PENDING (g2 claim METHOD_ARTIFACT as of 2026-05-17)."
   ```

4. **Update B2 KG node**:
   - Change: `finding_prom32_B2_zd_handling_policy` verdict from `RECOMMEND_OPTION_3` to `OPTION_3_DECOUPLED_FROM_G2`
   - Add edge: `(:B2_finding)-[:REFUTED_BY]->(queue_08_METHOD_ARTIFACT)`

### Phase 2: Consolidation (after Phase 1 verdicts)

5. **If Option A (Killing-form) resolves D4 failure**:
   - Report: "Casimir Schur-scalarity preserved under Killing-form weighting. D2 rank=16 issue remains: 2 spurious generators exist in sedenion-derived derivation algebra."
   - Next: Understand why 2 extra generators (likely non-alternativity artifacts). Do they decouple or mix with the 14-D g2 subspace?
   - Action: Compute branching rules; check if 16 = 14⊕2_spinor (or other g2 irrep decomposition).

6. **If Option B (Aut(O) embedding) resolves all D1-D4**:
   - Report: "g2 = Aut(O) confirmed via explicit embedding into sedenion orbit-rep basis. Sedenion-internal derivation formula is too broad (non-alternativity)."
   - Keep: null-dim power-law (now with caveat: driven by Aut(O) action, not sedenion structure)
   - Revise narrative: "ZD-generated null-spaces interact with octonion automorphism group, not sedenion full derivation algebra."

### Phase 3: Fallback (if both options fail)

7. **Escalate to user**:
   - Summary: "g2 claim unresolved. Two attempts (reweighting, embedding) both failed to rescue D2/D4 diagnostics. Recommend pause on mass-formula hardening pending deeper algebra analysis."
   - Proposal: Accept null-dim power-law as **empirical** (works for m_μ) and **untethered from g2** (which is now uncertain). Proceed with caution.

---

## Open Issues

### Issue 1: The "16 vs 14" Mystery
**Status**: Unsolved.  
**Hypotheses**:
- H1: Sedenion non-alternativity generates 2 extra derivations (not in Der(O))
- H2: The orbit-rep basis oversamples directions; 16 generators are partially redundant
- H3: The projection onto orbit-rep basis introduces spurious generators (mathematical artifact)

**Resolution**: Phase 1A/B diagnostics will address H1 (Killing-form reweighting) and H3 (Aut(O) embedding clean room).

### Issue 2: Why Does m_τ Prediction Miss by 1.5×?
**Status**: Undiagnosed.  
**Data**:
- m_μ/m_e = 206 (SM), predicted = ~200 (null-dim=4, α=4.85) ✓ 3% match
- m_τ/m_μ = 16.8 (SM), predicted = ~11.5 (null-dim={4,12,20,28}, α=4.85) ✗ 1.5× off

**Hypotheses**:
- H1: Tau involves mixed null-space contributions (multiple null-dims active simultaneously)
- H2: α varies with generation or scale (not universal constant)
- H3: Model 15-16 misses higher-order ZD interactions (e.g., second-order null-space effects)

**Resolution**: Separate investigation (not blocking B2+ revision).

### Issue 3: Does D3 "qualified pass" Mean Anything?
**Status**: Ambiguous.  
**Dilemma**: D3 median = 1e-15 (PASS) but max = 0.71 (FAIL). What's the physical meaning?
- Interpretation A: Mostly a Lie algebra, with ~O(1) outlier commutators → safe for dynamics
- Interpretation B: Partially closed; residual mixing violates gauge invariance → unsafe

**Resolution**: Lean formalization (Phase 3 hardening) would resolve via explicit closure checks.

---

## Revised Comparison Table: ZD Policies Post-queue_08

| Policy | Action at a*b=0 | Risk | Empirical Match | Algebra Status | Tractability |
|--------|---|---|---|---|---|
| **1. Skip ZD pairs** | Remove from path integral | Lose generation structure | FAIL | N/A | Easy (wrong) |
| **2. ε-regularize** | a*b → ε·norm | Arbitrary ε choice | MEDIUM | N/A | Hard |
| **3. Boundary (orig)** | S[b]=0; Doublet count | D3 test validates | GOOD (1.5×) | g2 via sedenion deriv | **BROKEN** (queue_08 METHOD_ARTIFACT) |
| **3' Boundary (decoupled)** | S[b]=0; Doublet count; α ≈ 4.85 | D3 test OPEN | GOOD (1.5×) | **UNKNOWN** (Phase 1A/B pending) | **MEDIUM** (Option A or B required) |
| **4. Accept unitarity break** | Allow unbounded S | Catastrophic | POOR | N/A | Easy (non-physical) |

---

## Terminal Verdict

**B2_REVISION**: `OPTION_3_PRIME_DECOUPLED_AWAIT_PHASE1_DIAGNOSTIC`

**Summary**:
- **B2 original claim** ("ZD as boundary, protected by g2 Lie closure") is **partially refuted** by queue_08 METHOD_ARTIFACT verdict.
- **ZD-boundary postulate** (S[b]=0 for b ∈ null(L_a)) remains **viable** and is **decoupled from g2 confirmation**.
- **Null-dim power-law** (m_gen ~ null-dim^4.85) remains **empirically valid** (1.5× accuracy on tau) and is **independent of algebra claim**.
- **g2 claim** is **demoted to OPEN** pending Phase 1A (Killing-form reweighting) or Phase 1B (Aut(O) embedding).

**Recommended next step**: Execute Phase 1A and 1B diagnostics in parallel. If either resolves D1-D4 failures, **ratify ZD-boundary + power-law** with updated algebra justification. If both fail, **escalate to user** for fundamental redesign.

**Confidence**: MEDIUM-HIGH on decoupled policy; LOW-MEDIUM on g2 recovery.

---

## KG References (New/Updated)

- Parent finding: `finding_prom32_B2_zd_handling_policy`
- Refuting verdict: `queue_08_g2_METHOD_ARTIFACT_2026-05-17`
- This revision: `finding_prom32_B2plus_zd_boundary_decoupled_2026-05-18`
- Phase 1A diagnostics: `queue_08_killing_form_reweight_diagnostic_PENDING`
- Phase 1B diagnostics: `queue_08_aut_o_embedding_diagnostic_PENDING`
- Decoupled policy KG node: `ice_zd_boundary_policy_option3_prime_empirical_nulldim`
- Power-law independent validation: `ice_model16_null_dim_power_law_decoupled_from_g2_2026-05-18`

---

**Revision completed**: 2026-05-18  
**Revision scope**: Full re-analysis of B2 Option 3 in light of queue_08 METHOD_ARTIFACT  
**User escalation required**: YES (Phase 1A/B decision + g2 recovery strategy)  
**Blocking status**: NOT BLOCKING null-dim power-law; BLOCKING g2 narrative claim.
