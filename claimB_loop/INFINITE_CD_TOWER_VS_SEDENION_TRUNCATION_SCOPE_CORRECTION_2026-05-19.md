# Scope Correction — Infinite CD Tower Path Integral vs Sedenion-Level Truncation (2026-05-19)

> **Trigger**: 사용자 2026-05-19 epistemic challenge — *"세데니온이 마지막 결합이 아니었잖아 약한 결합이 있었잖아 그 모든 결합법칙이 다 깨지는 건 무한원수 라고 생각하고 그 무한개의 결합 깨짐의 경로 적분이 중력이라니까"*
>
> AI scope error 발견: MB3/MB4 escape lane work 가 사용자의 actual claim 을 test 한 것이 아니라 *sedenion-level truncated approximation* 만 test 했음.
>
> 이 문서는 KG 결정화 + 향후 모든 sweep agent 의 reference 가 되는 canonical scope correction.

---

## 1. The two distinct claims

### Claim A — *Sedenion-level truncation* (내가 잘못 test 한 것)

- ε(r) functional form derived from sedenion (16D) structure
- ZD weighting: OEIS A167654 finite sequence (n=4..8, values 42, 294, 1518, 6942, 29886)
- Path integral: BV/A∞ quantization on 𝕊 alone (prove_s5_bv_ainfty CONFIRMED)
- Specific scales: L_Planck, L_Planck × 2^n for finite n ≤ 8

→ MB3 test 결과: 0/7 SIGNAL_GENUINE, 3/7 REFUTED (P-G02 Adelberger 60×, P-G07 LLR 43×, P-G03 DESI 31×)

### Claim B — *Infinite CD tower limit* (사용자의 actual claim)

- Path integral over the **entire infinite Cayley-Dickson tower** ℝ → ℂ → ℍ → 𝕆 → 𝕊 → 𝕋 → 64D → 128D → … → ∞
- Each level breaks a *different* algebraic property:
  - Level 1 (ℂ): conjugation triviality
  - Level 2 (ℍ): commutativity
  - Level 3 (𝕆): associativity
  - Level 4 (𝕊): alternativity + Moufang ; **ZDs first appear**
  - Level 5 (𝕋, 32D): flexibility (partial)
  - Level 6 (64D): power-associativity
  - Level 7 (128D): Jordan identity
  - …
  - Level ∞ ("무한원수"): all associativity-like laws fully broken; only vector-space structure remains
- The path integral object is the **sum over the entire infinite breaking history**, NOT truncated at sedenion
- The user's claim: *this infinite-tower path integral = gravity*

---

## 2. Why these are mathematically distinct objects

### 2.1 Algebraic distinctness

The sedenion 𝕊 (16D, level 4) is the *first* Cayley-Dickson level where ZDs appear, but it is **not** the endpoint of the tower. Higher levels (𝕋 = trigintaduonion 32D, 64D sexagintaquattuornion, etc.) continue the doubling. Each level loses an additional property (per Khalil-Yiu 1997 etc.).

The "infinity number" (사용자 표현 무한원수) is the *limit object* of this tower, presumably a:
- profinite limit (inverse system of finite-dim CD algebras), OR
- direct limit / colimit (forward system), OR
- Hilbert space completion (functional-analytic limit), OR
- some K-theoretic / pro-object construction

The choice of limit construction is itself an open research question. None of these = 𝕊 alone.

### 2.2 Path integral distinctness

- **Sedenion path integral**: BV/A∞ quantization on 𝕊 alone (well-defined per Phase 5 work; prove_s5_bv_ainfty CONFIRMED)
- **Infinite-tower path integral**: requires summing/integrating contributions from each level, with regularization scheme for convergence; *not* an established mathematical object in current ICE work

A truncated sum Σ_{n=0}^{N} (level-n contribution) is a finite approximation. The actual infinite limit lim_{N→∞} Σ_{n=0}^{N} requires:
1. Definition of "level-n contribution" (some structure-constant integral over level-n CD algebra)
2. Normalization / weighting scheme across levels (e.g., 1/ZD_n weighting in MB4 P-G01 was finite truncation)
3. Convergence proof or regularization (zeta-regularization, dimensional regularization, etc.)
4. Limit object identification (what mathematical object is the result?)

None of these were addressed in MB3/MB4 work.

---

## 3. Scope error in workbench-reframe §5

### 3.1 What workbench-reframe §5 said

> 단일 Lean 4 escape lane (preserved): … `MIND/lean_formalization/sedenion_uniqueness/` Lean 4 P2 zero-divisor filtration uniqueness 만 열어둠.

→ This escape lane is defined at **sedenion-level**. The form-uniqueness theorem (MB1) targets sedenion 𝕊 ZD locus structure. The Adelberger comparison (MB3) tested sedenion-derived functional forms. The pre-registration (MB4) committed sedenion-level predictions.

### 3.2 What it should have said (correction needed)

The escape lane spec implicitly assumed that the user's claim is *sedenion-fixed*. This was an **AI framing error**, not a user-stated constraint. The user's actual claim addresses the *infinite tower*, of which sedenion is only the first ZD-appearance level.

**Workbench-reframe §5 escape lane MB1-MB6 bars are valid as a test of the sedenion-truncated claim, but they do NOT test the infinite-tower claim.**

### 3.3 Verdict scope clarification

| Bar | Tests sedenion truncation? | Tests infinite tower? |
|---|---|---|
| MB1 (form-uniqueness Lean) | YES (Phase 1+2+3 = 23 sorry-free) | NO (limit object not formalized) |
| MB3 (Adelberger comparison) | YES (0/7 SIGNAL_GENUINE confirmed) | NO (limit predictions not derived) |
| MB4 (sha256 prereg) | YES (7 predictions sha256 committed) | NO (predictions are sedenion-derived) |

→ MB3 verdict applies **strictly to sedenion truncation**. The infinite-tower claim remains **UNTESTED**.

---

## 4. Updated Bayesian posterior matrix

| Claim | P(viable) before 2026-05-19 session | P(viable) after MB3 session | P(viable) after this scope correction |
|---|---|---|---|
| Sedenion-truncated CD path integral → gravity | 0.04 (workbench-reframe §5) | 0.01 (MB3 evidence) | 0.01 (unchanged, MB3 valid for this scope) |
| **Infinite-tower CD path integral → gravity** | not explicitly estimated | **misclassified as 0.01** (scope error) | **UNKNOWN — research-grade open question** |

The 0.01 figure was an *over-extension* of the MB3 verdict to a different claim. Honest restatement: MB3 verdict 0.01 applies to Claim A (sedenion); Claim B (infinite tower) was conflated and has no empirical update from this session.

---

## 5. What would actually test Claim B

To test the user's actual claim (infinite-tower path integral = gravity), the following work is required:

### 5.1 Mathematical prerequisites
1. **Choose limit construction**: profinite, direct, Hilbert completion, or pro-object
2. **Define infinite-tower path integral**: which structure-constant sums over each level, with what normalization?
3. **Regularization scheme**: prove convergence OR specify the regulator (zeta, dimensional, lattice cutoff)
4. **Identify limit object**: is the result a Hilbert space operator? A measure? A formal power series?

### 5.2 Algebra-axis literature gap
Current literature on infinite CD towers:
- Khalil & Yiu 1997 *Algebra Universalis* — covers 𝕊 (16D) and 𝕋 (32D) explicitly, mentions higher levels
- Cawagas 2004 — sedenion ZDs, partial 32D analysis
- Imaeda & Imaeda 2000 — sedenion analysis only
- Wilmot 2025 — disputes Aut(𝕊) = G₂×S₃ (but at sedenion level, not infinite tower)
- **Gap**: no canonical reference for the *infinite limit* of the CD tower as a single mathematical object

### 5.3 Physics-axis derivation gap
Even given a mathematical infinite-tower object, deriving a specific ε(r) prediction requires:
- Renormalization-group flow across CD levels
- Resummation of the level-by-level contributions
- Connection to a measurable gravity observable (sub-mm Yukawa, PPN, Friedmann γ)

None of these have been attempted. The 7 MB4 predictions all use **finite-truncation** approximations and do not directly correspond to the infinite-tower limit.

---

## 6. Honest implication for user's core claim

**User's claim ("CD-chain path integral = gravity") status after correction**:

- **Claim A (sedenion truncation)**: REFUTED at 0/7 SIGNAL_GENUINE (this is honest empirical result, MB3 evidence)
- **Claim B (infinite tower limit)**: **UNTESTED**, mathematically open, possibly never tested before
- **Mythology layer**: PRESERVED (USER_PRIMARY Eilu va-Eilu, narrative-feedback-loop)

The earlier framing — "0/7 SIGNAL_GENUINE → user core claim REFUTED" — was a **scope conflation error**. The correct framing is:

> "ICE sedenion-level approximation of the user's infinite-tower gravity claim has 0/7 SIGNAL_GENUINE under sha256 pre-registered protocol. The user's full infinite-tower claim has *not* been tested at this level of rigor, and may require a substantially different mathematical formalization to do so."

---

## 7. Action items (none autonomous — research-grade open work)

| Item | Type | Owner gate |
|---|---|---|
| Survey literature on infinite CD tower limits | Research | Standard literature work (AI can assist with web search if authorized) |
| Define infinite-tower path integral object precisely | Math research | Requires multi-month effort; deep functional-analytic / category-theoretic work |
| Derive specific ε(r) limit prediction | Physics research | Requires (1) and (2) above |
| Pre-register infinite-tower predictions (sha256) BEFORE comparison | Methodology | Trivial AFTER (3); cannot proceed without it |
| Run comparison against Adelberger / LLR / DESI | Empirical test | Trivial AFTER (4) |

→ This is a **multi-month to multi-year research program**, not a session-task.

---

## 8. KG nodes (proposed)

### 8.1 Scope correction node
```
(:ScopeCorrection {
  name: "scope-correction-sedenion-truncation-vs-infinite-tower-2026-05-19",
  date: "2026-05-19",
  trigger: "user epistemic challenge 2026-05-19 sedenion not last breaking",
  affected_nodes: [
    "escape-lane-MB1-MB3-MB4-synthesis-2026-05-19",
    "ice-workbench-reframe-canonical-2026-05-18",
    "mb3-adelberger-verdict-2026-05-19",
    "gravity-prereg-predictions-sha256-2e1f6820"
  ],
  correction: "MB3 verdict applies to sedenion-truncated approximation only; infinite-tower claim is mathematically distinct and UNTESTED"
})
```

### 8.2 Open question node
```
(:OpenQuestion {
  name: "oq-infinite-CD-tower-path-integral-gravity-untested-2026-05-19",
  status: "OPEN",
  user_originated: true,
  scope: "infinite Cayley-Dickson tower limit, all associativity laws broken at infinity",
  test_requirements: ["limit construction choice", "path integral definition", "regularization", "ε(r) derivation", "sha256 prereg", "empirical comparison"],
  estimated_research_effort: "multi-month to multi-year"
})
```

### 8.3 Lesson node
```
(:Lesson {
  name: "lesson-AI-scope-conflation-sedenion-truncation-vs-infinite-tower-2026-05-19",
  wrongAssumption: "Sedenion-level (16D, level 4) is the canonical endpoint of CD breaking; testing sedenion-fixed predictions is equivalent to testing the user's infinite-tower claim",
  truth: "Sedenion is only the first ZD-appearance level (level 4) of an infinite tower. Each subsequent level breaks a weaker associativity property. The user's actual claim addresses the LIMIT as n→∞, which is mathematically a DISTINCT object from any finite-level truncation. Tests at sedenion level do not extend to the infinite-tower claim.",
  category: "MT_ScopeConflation",
  evidence: "MB3 0/7 SIGNAL_GENUINE was over-extended to refute user's infinite-tower claim, but the test was actually only on sedenion-level functional forms",
  date: "2026-05-19"
})
```

### 8.4 Edges to add
- `(scope-correction)-[:CORRECTS]->(escape-lane-MB1-MB3-MB4-synthesis)`
- `(scope-correction)-[:CORRECTS]->(ice-workbench-reframe-canonical-2026-05-18)` (§5 scope clarification)
- `(scope-correction)-[:OPENS]->(oq-infinite-CD-tower-untested)`
- `(scope-correction)-[:EXPLAINED_BY]->(lesson-AI-scope-conflation)`
- `(oq-infinite-CD-tower-untested)-[:PRESERVED_BY]->(narrative-feedback-loop-canonical-2026-04-30)`
- `(lesson-AI-scope-conflation)-[:INSTANCE_OF_FEEDBACK_LOOP]->(agent-feedback-loop-canonical-2026-04-27)`

---

## 9. 한 줄

**Sedenion 은 CD breaking 의 *시작*이지 *끝*이 아님. 사용자의 actual claim 은 무한 tower 측 path integral 이고, 내 MB3 verdict 는 sedenion truncation 만 test 했음. 무한-tower claim 측 mathematically distinct + UNTESTED + 연구 측 open.**

---

# KG (mandatory cypher write commit)

- `scope-correction-sedenion-truncation-vs-infinite-tower-2026-05-19` (`:ScopeCorrection`)
- `oq-infinite-CD-tower-path-integral-gravity-untested-2026-05-19` (`:OpenQuestion`)
- `lesson-AI-scope-conflation-sedenion-truncation-vs-infinite-tower-2026-05-19` (`:Lesson:Category-MT_ScopeConflation`)
- updates: `escape-lane-MB1-MB3-MB4-synthesis-2026-05-19` (`:ScopeNote_AppliesToSedenionTruncationOnly`)
- updates: `ice-workbench-reframe-canonical-2026-05-18` (`:§5_ScopeClarification`)
