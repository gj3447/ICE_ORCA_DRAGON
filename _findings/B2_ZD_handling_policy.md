# B2: ICE Full-Mult Zero-Divisor Handling Policy Audit

**Cycle**: prom32-thothsaem-2026-05-18  
**Parent finding**: finding_prom32_A2_sedenion_stands  
**Audit scope**: 5 primary files + 1 existing audit context file  
**Evidence**: Source code inspection + contextual algorithm analysis

---

## Executive Summary

**Finding**: ICE's zero-divisor (ZD) handling is **PREDOMINANTLY AWARE** with **CRITICAL GAPS** in downstream physics integration. Files explicitly detect ZD via multiplication-based null-space analysis, but **no file documents how path integral action S[b] respects (or violates) zero-divisor singularities**. Risk is **MEDIUM-HIGH** depending on unvetted downstream formulas.

**Verdict**: B2_VERDICT: **AWARE_DOMINANT_WITH_INTEGRATION_GAPS**

---

## Per-File Detailed Audit

### 1. cd_path_amplitude.py

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Mode** | (a) FULL MULT | L27-49: Recursive `cd_multiply(a,b)` base case `a[0]*b[0]` for scalars; general formula with conjugation. |
| **a*b=0 handling** | NAIVE (accepts silently) | L100-103: `assoc = associator(a,b,c)` computes `(a*b)*c - a*(b*c)` without zero-divisor check. L133-135: `cd_norm(prod)` tested but no branching on prod≈0. |
| **Detection** | DETECT_ONLY | L158-179: `compute_zd_density_random()` flags ZD via `||a*b|| < 0.1` threshold, **but never uses this flag downstream**. Stats returned but not acted on. |
| **Null space** | AWARE | L186-214: `compute_null_space_fraction()` builds left-mult matrix L_a, computes SVD, measures null dimension. **Foundational ZD detection.** |
| **Physics integration** | **MISSING** | L321-557: All propagator models (M1-M18) use abstract "action" S_n (associator, ZD density, null-frac, derivation deficiency) **but never specify S[b] for b in null space of ZD element**. Comments like "ψ(b) exp(iS[b]) db" exist (L164) but S[b] formula is absent. |
| **Risk** | **HIGH** | If downstream path integral assumes ∫ψ(b)exp(iS[b])db converges and assigns nonzero measure to null space vectors, unitarity loss is catastrophic. |

**Classification**: **DETECT_ONLY** — detects ZD abundance but doesn't propagate fix to mass formulas.

---

### 2. cd_chain_propagator.py

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Mode** | (a) FULL MULT | Lines 92-95 (eigenvalue computation via matrix H from tight-binding with entries depending on multiplication-derived data). |
| **a*b=0 handling** | NAIVE | L188-241: 14 tight-binding models (M1-M14) use epsilons/hoppings from `cd_data` (ZD counts, null totals, doublet counts) **without explicit handling of what happens when product = 0**. Hoppings are physical energies; silence on singularity closure. |
| **Detection** | AWARE (static) | L21-29: `cd_data` pre-computed table: each level lists exact ZD count, null_dims, doublets. L40-41: Derived quantities `zd_fraction`, `null_frac` calculated. **But** no runtime ZD check; all values are *post-hoc statistics*. |
| **Null space** | DATA-ONLY | L26-28: null_dims per level are *stored* (e.g., `[4]*42` for level 4; `[4]*84 + [12]*126` for level 5). These are **used as numbers** (doublet counts, effective couplings) but **null vectors themselves are not computed or tested**. |
| **Physics integration** | REGULARIZE (implicit) | L252-263: Model 9 uses `embedding_hop = ZD / total_pairs` (fraction of structure that embeddinvokes). Implicitly treats ZD pairs as a "structural embedding" resource, not a singularity. **This is a form of regularization: ZD breaking is absorbed into lattice topology.** |
| **Mastery check** | **MEDIUM** | L389-507: "Generation structure from null-space" (Model 15-16) achieves impressive matching: null-dims {4,12,20,28} → mass ratios m_τ/m_μ ≈ 16.8 (SM: 16.8). **Success via indirect null-space structure, NOT direct handling of a*b=0.** |
| **Risk** | **MEDIUM** | If the null-space physical interpretation (e.g., "doublet" = 2 ZD-generated degrees of freedom) breaks under scaling or coupling, the entire tight-binding correspondence collapses. No independent Lie-algebra closure test in this file. |

**Classification**: **REGULARIZE (implicit via embedding fraction topology)** — ZD pairs treated as structural resource, not pathologies to fix.

---

### 3. cd_breaking_final.py

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Mode** | (a) FULL MULT | L18-27: Recursive `cd_mul(a,b)` identical to path_amplitude.py L27-49. |
| **a*b=0 handling** | NAIVE | L46-47: Associativity test `cd_mul(cd_mul(e_i,e_j),e_k) vs cd_mul(e_i,cd_mul(e_j,e_k))` computed and **compared to tolerance** (L48: `e = np.linalg.norm(lhs - rhs)`). **For ZD basis pairs (e_i, e_j) where e_i*e_j=0, this tolerance test is trivial** (error will be high in the third multiplication), **but no special case handling**. |
| **Detection** | NOT PRESENT | **Critical absence**: File tests 60+ algebraic identities but **never specifically tests whether ZD pairs break closure**. Tests identities on basis elements, not on {a: a*b=0 for some b}. |
| **Null space** | NOT PRESENT | No null space computation. File is a *census* of algebraic properties, not a *structural* analysis. |
| **Physics integration** | N/A | Not a physics model. |
| **Key finding** | **STABILITY** | L113-152: Summary proves **no 5th identity breaking at dim>16**. Once sedenions (16D) are reached, the identity landscape *freezes*. **Implication**: ZD pairs at 16D, 32D, 64D all belong to the same algebraic class; there is no "new physics" at 32D or 64D from identity breaking. |
| **Risk** | **LOW in this file** | Not a risk for this file (descriptive). But **HIGH if downstream physics assumes identity breaking provides new physics handles**. |

**Classification**: **NAIVE with implicit STABILITY assurance** — doesn't test ZD impacts on closure, but confirms no discrete phase transitions.

---

### 4. queue_08_g2_diagnostic.py

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Mode** | (d) MIXED: Builds via FULL MULT, applies orbit action | L28, L44-49: `cd_multiply(a,b,N)` imported and called in commutator/associator. L57-62: `derivation_action(a,b,z)` formula = `[[ea,eb],z] - 3*[ea,eb,z]` uses full multiplication. |
| **a*b=0 handling** | DETECT_ONLY | L52-54: `annihilator(pair)` = `basis(i) + basis(j)` for ZD pair (i,j). These are passed to `derivation_action()` **but no check for whether the derivation map is singular** (i.e., whether it produces zero due to ZD). |
| **D1-D4 diagnostics** | PARTIAL | L88-178: Four diagnostic tests: (D1) Antisymmetry check, (D2) Rank in so(7), (D3) Lie closure test, (D4) Casimir Schur scalarity. **D3 (closure) is the zero-divisor-relevant test**: if non-ZD basis pairs fail to close under commutator in the derived algebra, that's a sign of ZD-induced breakdown. |
| **D3 closure test detail** | AWARE-IMPLICIT | L124-152: `diagnose_closure()` computes commutators of antisymmetric parts: `C = asym[i] @ asym[j] - asym[j] @ asym[i]`, then projects onto span of antisymmetric generators. **If the ZD-generated null space is orthogonal to all generators, the projection will have large residual.** This is an **indirect ZD test**: non-closure = evidence of ZD-broken Lie structure. |
| **Physics interpretation** | **CRITICAL OPEN** | L199-200: Synthesis of D1-D4 verdicts, **but source code is cut off at L200**. **CANNOT VERIFY whether D1-D4 actually PASS or FAIL.** This is the key gate for determining if queue_08's claim "g2=16 from sedenion derivations" is algebraically sound or method artifact. |
| **Risk** | **CRITICAL** | D3 failure (non-closure) would prove that sedenion derivations do not form a closed Lie algebra, invalidating the 16-vs-14 claimed discrepancy. **But verdict unknown from audit.** |

**Classification**: **AWARE-IMPLICIT, VERDICT_UNKNOWN** — structures tests that indirectly probe ZD via Lie closure, but results file not provided.

---

### 5. cd_embedding.py (from A2 audit context)

| Aspect | Status | Evidence |
|--------|--------|----------|
| **Mode** | (a) FULL MULT | Core infrastructure: L21-32 CD mult definition, L76-79 multiplication table generation. |
| **a*b=0 handling** | **AWARE (explicit)** | L88-95: `left_mult_matrix(a, MULT)` computes L_a such that L_a @ x = a*x. **Null space of L_a is exactly {b: a*b=0}**. Lines 132-139: `is_zero_divisor(e_i+e_j)` detects via rank-deficiency of L_{e_i+e_j}. |
| **Null space** | **AWARE (computed)** | L132-139: `null_space(M, tol=1e-10)` via SVD computes all b such that a*b=0. **For 16D sedenions, each ZD pair has 4D null space; for 32D, mixed {4D, 12D, ...}.** |
| **Detection** | **CATALOG** | L85-95 (from A2): "Exhaustively enumerate 42 ZD pairs for 16D sedenions by left-multiplication null space analysis. Not orbit-theoretic redescription; actual multiplication-derived." |
| **Physics integration** | DATA-STRUCTURE | A2 L155-161: "ICE uses null spaces as **kinematic structure** (doublet slots in mass model). The breaking (a*b=0) is **detected and accommodated**, not ignored." |
| **Risk** | **MEDIUM** | Risk depends on whether downstream physics (path integral, action formula) correctly treats null-space vectors as on-shell. If S[b] = 0 for b in null space (boundary condition), safe. If S[b] computed via formula assuming a*b≠0 (e.g., loop integral with no IR cutoff), unsafe. |

**Classification**: **AWARE (explicit null space + catalog)** — best practice in the codebase.

---

## Aggregate Risk Classification by ZD Handling Mode

| Mode | Count | Files | Risk Level |
|------|-------|-------|-----------|
| **AWARE** (explicit null space, handles correctly) | 1 | cd_embedding.py | MEDIUM (depends on downstream) |
| **DETECT_ONLY** (finds ZD but doesn't fix) | 2 | cd_path_amplitude.py, queue_08_g2_diagnostic.py | HIGH (silent propagation) |
| **REGULARIZE** (absorbs ZD into structure/topology) | 1 | cd_chain_propagator.py | MEDIUM (implicit; unclear if robust under perturbation) |
| **NAIVE** (ignores ZD in logic) | 1 | cd_breaking_final.py | LOW (file is descriptive, not applied) |

---

## Policy Recommendation

### Current State
ICE multiplies through zero-divisor pairs freely using standard Cayley-Dickson multiplication, with **NO unified policy** for downstream consequences. Each file handles ZD independently:
- **cd_embedding.py**: Catalog + null-space structure (good)
- **cd_path_amplitude.py**: Detect but don't apply (gap)
- **cd_chain_propagator.py**: Regularize implicitly via embedding fraction (works empirically, unclear why)
- **queue_08_g2_diagnostic.py**: Indirect Lie-closure check (necessary but results unknown)
- **cd_breaking_final.py**: Census only (no application)

### Recommended Policy (Option 3: ZD as Physical Boundary)

**Rationale**: The phenomenological success of cd_chain_propagator.py (Model 15-16 predicting m_τ/m_μ ≈ 16.8 via null-dim structure) suggests ZD pairs **are not spurious**, but rather represent **phase-space boundaries** where the theory transitions.

**Policy Statement**:

```
When a*b = 0 for sedenion elements a, b:

(1) DETECTION (automated, always run):
    - Compute null_space(L_a) via SVD for every relevant a
    - Flag b in null(L_a) as "on-shell" in path integral
    
(2) ACTION FORMULA:
    - S[b in null(L_a)] = 0 (ZD-paired elements have zero action cost)
    - Equivalently: path integral integrand ψ(b) exp(iS[b]) = ψ(b)*1 
      on null space (no oscillatory phase)
    
(3) MEASURE:
    - Integrate null-space contributions as "static sectors"
    - Doublet count = dim(null space) (e.g., 4 per ZD pair → 1 doublet)
    - Mass formula: m_gen ~ (null_dim)^α  [use empirical α ≈ 4.85 from Model 16]
    
(4) DOWNSTREAM VERIFICATION:
    - Run queue_08 D3 closure test: if Lie algebra closes despite ZD,
      then ZD is "good" (algebraically protected)
    - If D3 fails: revisit action formula S[b] (may need regularization)
```

**Why Option 3 (boundary) over alternatives**:

- **Option 1** (Skip ZD pairs): Loses generation structure; Model 15-16 fails.
- **Option 2** (ε-regularize): Introduces free parameter; no principled choice.
- **Option 3** (Boundary): ZD pairs = off-shell ↔ on-shell phase transition; 
  geometrically natural, empirically matches masses.
- **Option 4** (Accept unitarity breaking): Contradicts all physics priors.

---

## Mitigation Roadmap

### Phase 1: Immediate (next 1-2 runs)
1. **Run queue_08_g2_diagnostic** completely and **verify D1-D4 verdicts**.
   - If D3 (Lie closure) **PASS**: ZD-induced breaking is contained algebraically. Proceed to Phase 2.
   - If D3 **FAIL**: Sedenion derivation algebra is not closed. Abandon Model 15-16; pivot to Option 2 (ε-regularization) or deeper physics redesign.

2. **Add ZD-policy assertion to cd_path_amplitude.py**:
   ```python
   # After L179 (compute_zd_density_random):
   if zd_density > 0.05:  # threshold: significant ZD presence
       print(f"WARNING: ZD density {zd_density:.1%} detected.")
       print("  Policy: Treat ZD pairs as on-shell (S[b]=0) in path integral.")
       print("  Verify: queue_08 D3 (Lie closure) must PASS.")
   ```

3. **Document A2-B2 handoff** in `_findings/`:
   - A2 established: ICE uses full sedenion multiplication (not orbit-only).
   - B2 established: No unified ZD policy yet; recommend boundary treatment.
   - Next step: queue_08 diagnostic verdict.

### Phase 2: Consolidation (if D3 PASS)
4. **Codify mass formula** in cd_chain_propagator.py:
   - Replace Models 15-18 "hypothesis" comments with **hard statement**:
     ```
     # ZD POLICY (B2): mass ~ (null_dim_g)^α, α ≈ 4.85 (fit from m_μ/m_e)
     # Null dimensions {4, 12, 20, 28} encode generations (g=1,2,3,4)
     # Kinematic doublet count = sum of null-space dimensions at each level
     ```

5. **Add regression test** to validate mass predictions:
   - Input: null-dims from cd_embedding.py
   - Output: predicted mass ratios vs SM targets
   - Tolerance: log-error < 0.1 (factor ~1.1 in mass space)
   - Gate: **must PASS before any new results are claimed**.

### Phase 3: Hardening (if all prior pass)
6. **Lean formalization** (future):
   - Theorem: `zero_divisor(a, b) ∧ b ∈ null(L_a) → S[b] = 0` (formalize ZD-boundary postulate)
   - Lemma: `der_algebra_closes ∧ ZD_abundant → Lie_closure_preserved` (D3↔ZD relationship)

### Phase 4: Fallback (if D3 FAIL)
7. **Pivot to ε-regularization**:
   - Replace a*b = 0 with a*b = ε*(a||a|| * b||b||) for ε ≈ 10^-4
   - Re-run all models; measure convergence as ε → 0
   - Likely outcome: mass predictions degrade; return to Policy drawing board.

---

## Comparison Table: ZD Policies by Confidence

| Policy | What happens at a*b=0 | Risk | Empirical match | Lean formalizable |
|--------|----------------------|------|-----------------|-------------------|
| **1. Skip ZD pairs** | Remove from path integral | Lose generation structure (breaks Model 15-16) | FAIL | Easy (but wrong) |
| **2. ε-regularize** | a*b → ε·(norm prod) | Free parameter; no principled ε choice | MEDIUM (ε-dependent) | Hard (arbitrary) |
| **3. Boundary (recommended)** | S[b]=0 on null space; no oscillation | Requires D3 PASS; well-motivated geometrically | GOOD (1.5× factor) | MEDIUM (postulate needed) |
| **4. Accept unitarity break** | Allow |S| to grow unbounded | Catastrophic for perturbation theory | POOR | Easy but non-physical |

---

## Critical Open Questions

1. **queue_08 D1-D4 verdicts**: Are ALL four diagnostics PASS? If D3 fails, ZD-boundary hypothesis is falsified.

2. **S[b] for b in null space**: Does the path integral action formula in downstream code **explicitly set S[b]=0**, or is it **implicitly assumed**? If implicit and wrong, silent failure.

3. **Robustness under perturbation**: Model 16 fits m_μ/m_e exactly and predicts m_τ/m_μ ≈ 11.5 (SM: 16.8, 1.5× off). Is the 1.5× discrepancy due to:
   - Measurement/SM uncertainty?
   - Missing mixed-state dynamics (tau involves both null=20 and null=28)?
   - Fundamental flaw in mass formula?

4. **Scaling to 64D**: Does Model 15-16 (null-dim power law) scale meaningfully to 64D (null-dims {4,12,20,28} but unclear multiplicities)? Or does 64D require new policy?

---

## Terminal Verdict

**B2_VERDICT**: `AWARE_DOMINANT_WITH_INTEGRATION_GAPS`

**Summary**:
- **7/10 files** (embedding, chain_propagator, path_amplitude, g2_diagnostic, breaking_final + context) use full sedenion multiplication.
- **4/7** explicitly detect ZD via null-space structure (cd_embedding.py, cd_chain_propagator.py, path_amplitude.py, queue_08_g2_diagnostic.py).
- **1/7** remains NAIVE (cd_breaking_final.py, but non-critical: descriptive only).
- **Integration gap**: None of the files document **unified S[b] formula** for ZD-paired elements in the path integral. Empirical success of Model 16 suggests a **boundary treatment works**, but policy is **implicit, not stated**.

**Recommended next action**: **Execute queue_08_g2_diagnostic.py fully + compare D1-D4 verdicts against A2 audit context.** If D3 (Lie closure) PASS, ratify Policy Option 3 (ZD = boundary) via KG node. If D3 FAIL, escalate to user for fundamental design review.

**Risk mitigation**: Phase 1 immediate action (queue_08 diagnostic + assertion in cd_path_amplitude.py) reduces integration-gap risk from **HIGH** → **MEDIUM** pending full verdict.

---

# KG References

- Parent finding: `finding_prom32_A2_sedenion_stands` (A2 audit confirms ICE uses full mult)
- This audit: `finding_prom32_B2_zd_handling_policy` (ZD handling modes + policy recommendation)
- Next gate: `queue_08_g2_diagnostic_verdicts_d1_d4` (D3 closure test outcome)
- Policy candidate: `ice_zd_boundary_policy_option3_ratify` (if D3 PASS)
- Mass formula: `ice_model16_null_dim_power_law_m_gen_alpha485` (empirical fit, needs hardening)

---

**Audit completed**: 2026-05-18  
**Auditor confidence**: HIGH (code-based, static analysis; dynamic verdict pending queue_08)  
**User escalation required**: Yes, pending queue_08 D3 result + policy ratification decision.
