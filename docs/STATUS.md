# ICE_ORCA_DRAGON Status

> Classification ledger, Lakatos verdicts, Bayesian posteriors, known limitations.
> Quick overview: [`../README.md`](../README.md). Script walk-through: [`USERGUIDE.md`](USERGUIDE.md).

> ⚠️ **2026-06-05 reframe reconciliation**: the "Current State" / "Classification Ledger" / "Lakatos Evaluation" tables below **predate the 2026-05-18 workbench reframe** and read in the old physics-programme frame. The CANONICAL verdict is the **bifurcated** one (see the Position Statement §below + `../ICE_WORKBENCH_REFRAME_2026-05-18.md`): **L1 algebra = PROGRESSIVE / L2-L3 physics belt = DEGENERATING-STAGNANT (Tüchsen 2024), 0 SIGNAL_GENUINE** per `../L2L3_NUMEROLOGY_LEDGER_2026-06-01.md`. Where a table below says "progressive" without a layer, read it as **L1-only**; physics-referent "confirmations" (e.g. *42 ZD as Higgs candidates*) are demoted to **NUMEROLOGY (DEAD)**.

---

## Current State

| Component | Value |
|-----------|-------|
| Python scripts | 47 |
| JSON result files | 22 (18 `_results.json` + 4 `finding_*.json` / `derive_*_results.json`) |
| Result JSONs with `verdict` field | 18/18 + 1 MC judge meta (19/19 total) |
| Categories | 7 (CD breaking / CD embedding / dim analysis / Higgs+S-proofs / sedenion / queue / misc) |
| Feedback-loop skill | `.claude/skills/science-feedback-loop.md` (v1, 2026-04-21+) |
| Classification ledger | See [the ledger below](#classification-ledger) |
| Verdict distribution | 6 CONFIRMED / 4 CONFIRMATION_LOCAL / 3 REFUTED / 2 NUMEROLOGY_CONFIRMED / 2 METHOD_ARTIFACT / 1 NUMEROLOGY_HOLD / 1 INCONCLUSIVE (+1 MC judge meta=RESOLVED) |
| Numerology MC judge | `numerology_mc_judge.py` → `numerology_mc_results.json` (P(E\|~H) computed under explicit null models, 2026-05-17) |
| Control plane | Node 24 + strict TypeScript + Effect 3; exact packages in `package-lock.json` |
| Numerical runtime | Python 3.13 + NumPy/SciPy/SymPy; exact packages in `uv.lock` |
| Mapped-output audit | 12 semantic `REPRO` + 1 `NONPORTABLE_FAIL` + 1 `SUPERSEDED` (2026-08-14) |
| Lakatos overall verdict | **BIFURCATED** (canonical, 2026-05-18 reframe): **L1 algebra = PROGRESSIVE** / **L2-L3 physics belt = DEGENERATING-STAGNANT** (Tüchsen 2024 EJPS third category). Physics belt: **0 SIGNAL_GENUINE** (10 NUMEROLOGY + 1 WEAK ember ε) per `../L2L3_NUMEROLOGY_LEDGER_2026-06-01.md`. The old blanket "progressive (11 conf > 3 ref)" is pre-reframe and superseded — see `lesson-prom16-hypercomplex-program-bifurcated-verdict-2026-05-18`. |

---

## Tooling and reproduction status (2026-08-14)

`./ice` is an Effect-powered TypeScript control plane. It discovers and runs the
legacy Python numerical kernels, verifies both lock contracts, models subprocess and
timeout failures in the typed error channel, and performs mapped-output reproduction
inside a scoped temporary copy. `npm run check` runs strict typechecking plus local
Effect/Vitest contracts; GitHub Actions is not yet wired.

The reproduction command is intentionally not all-green:

- 12 portable mappings reproduce under field-aware semantic comparison;
- `queue_03_threshold_sensitivity_scan` is `NONPORTABLE_FAIL` because an entrywise
  commutator maximum is evaluated in an arbitrary SciPy null-space basis;
- `queue_06_cooperative_vacuum` is `SUPERSEDED` because its committed repaired JSON
  comes from `inconclusive_redo.py`, not the historical named script;
- queue04's circular optimizer coordinates and spread alone use `atol=1e-6`; other
  structure/types/categories remain exact and ordinary floats remain tight.

The queue03 threshold artifact is distinct from `queue_03_rep_results.json`, which is
the output of the separate archived representation-decomposition experiment. See
[`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md)
and [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md).

---

## Classification Ledger

The science-feedback-loop classifies every result into one of four categories. Refutations and self-refutations are first-class outcomes.

### Confirmations (6 CONFIRMED + 4 CONFIRMATION_LOCAL = 10)

| Result | Source | External grounding | Bayesian posterior | Lakatos |
|--------|--------|--------------------|--------------------| --------|
| 42 sedenion assessors / 84 ZD pairs (L1 combinatorics only) | `prove_higgs_results.json` | Lygeros 2006 "42 Assessors" | high for the count; Higgs referent remains L2/L3 numerology | progressive at L1 only |
| S₃ Jacobi = 6·associator | `prove_s3_results.json` | FDA structure constant computation | high (algebraic identity) | progressive |
| S₅ BV bounded | `prove_s5_results.json` | all_zero + all_bounded checks | high (consistency) | progressive |
| Der(S) = g₂ (14D) | `sedenion_g2_deep.py` | g₂ literature (14-dim Lie algebra known) | medium-high (numeric only) | **CONFIRMATION_LOCAL** — no external peer review yet |
| 7×6 = 42 orbit | `queue_01_orbit_results.json` | matches sedenion ZD count | high (consistent with S₃ orbit on 42) | progressive |
| Uniform Casimir 0.75 across 42 pairs | `queue_03_rep_results.json` | rep-decomposition regularity (single bucket) | high (algebraic uniformity) | progressive |
| XOR invariant 105/105 | `queue_11_xor_results.json` | sedenion mult XOR match 100% | high (full invariant) | progressive |
| Wilmot 2025 Moufang pattern | (cross-cycle, history) | Wilmot 2025 | medium | progressive |
| Hosotani vacuum (3 cases) | `queue_04_hosotani_results.json` | toy SSB + θ→π convergence | medium (toy, no external) | **CONFIRMATION_LOCAL** |
| Coleman-Weinberg SSB (4/4) | `queue_05_cw_results.json` | bounded V_min across regimes | medium (toy) | **CONFIRMATION_LOCAL** |
| ~~g₂ structure (16 gen)~~ — demoted | `queue_08_g2_results.json` | ~~commutant_dim=1, 7 orbit reps~~ | n/a | **METHOD_ARTIFACT** (see diagnostic below) |
| Z₆ exclusion pattern | `queue_10_group6_results.json` | each orbit excludes 1 first + 1 second index | medium (combinatorial) | **CONFIRMATION_LOCAL** |

### Refutations (3 REFUTED, of which 2 are self-refutations)

| Result | Source | Verdict | Action taken |
|--------|--------|---------|--------------|
| ICE mass ratios | `derive_mass_ratios_results.json` | **REFUTED** (self) — "ICE cannot genuinely derive (0/15 genuine)" | Contract `derive_mass_ratios` status=REFUTED. Higher Span re-review triggered. |
| ICE L_star prediction | `derive_Lstar_results.json` | **REFUTED** (self) — "ICE cannot uniquely predict L_star from internal structure" | Contract `derive_Lstar` status=REFUTED. |
| Custodial SU(2)×SU(2) | `queue_02_custodial_results.json` + `queue_02_4condition_diagnostic_results.json` | **REFUTED structurally** — 100% of 42 pairs FAIL_BOTH_CLOSURE (c1, c2 residual median 3.94, c3 median 1.97). The 1.93 cross-commutator was SYMPTOM; root cause is projection onto 2D ZD null-space breaks Lie closure (non-alternative sedenion ambient). Test was measuring cross-commutators of non-Lie objects. | Contract `custodial_naive_embedding` status=REFUTED. PROM 16 R4 pivot (Aut(𝕊)=G₂×S₃ native commuting SU(2)×SU(2)) still needed but requires projection-faithful Lie construction (queue_08 was METHOD_ARTIFACT). |
| T₂ mechanism | (session log, see feedback-loop skill md) | refutation | Step 4 Contract patched |

### Discoveries

| Result | Triggered | Re-entry |
|--------|-----------|----------|
| ZD null space structure | (session log, see feedback-loop skill md) | new `:Span` created, /apt-sp dispatched |

### Numerology — MC discrimination (2026-05-17 resolution)

Three HOLD items were judged by Monte Carlo P(E|~H) under explicit null models
(`numerology_mc_judge.py` → `numerology_mc_results.json`). Decision rule:

| P(E\|~H) range | Verdict |
|----------------|---------|
| < 0.01 (look-elsewhere corrected) | SIGNAL_GENUINE |
| 0.01 ≤ P < 0.5 | SIGNAL_WEAK |
| ≥ 0.5 | NUMEROLOGY_CONFIRMED |

| Result | Source | Null model | P(E\|~H) | Verdict |
|--------|--------|-----------|---------|---------|
| Koide Q = 2/3 (and 7 other observables) | `derive_dimensionless_results.json` | 499 random ratios from ICE-like atomic integer set, look-elsewhere over 8 targets | **1.000** | **NUMEROLOGY_CONFIRMED** |
| mp / mW = 3·256 literal | `verify_mp_mW_results.json` (layer1) | direct comparison | rel_diff=88.8% even with reciprocal interpretation | **NUMEROLOGY_CONFIRMED** |
| mp / mW = a·2^n best-fit | `verify_mp_mW_results.json` (layer3) | random R log-uniform, a∈[1,500000] × n∈{14..19} search | **0.812** | **NUMEROLOGY_CONFIRMED** |
| ε power-law passes Adelberger | `derive_epsilon_results.json` | random eps0/r0/alpha power laws | 0.238 | NUMEROLOGY_HOLD (gate non-trivial; but no ICE pre-prediction of unique form) |
| c = 4·ln(2) | (session log) | not yet MC-judged | — | `:NUMEROLOGY_HOLD` |
| Bekenstein connection | (session log) | not yet MC-judged | — | `:NUMEROLOGY_HOLD` |

**Key insight**: For Koide_Q the 499-candidate ensemble drawn from any small-integer atomic set produces near-hits to 2/3 (or any small-rational target) with p ≈ 1. The "match" carries zero information. For mp/mW the search space ~3M (a,n) pairs achieves arbitrary R within 0.1% in ~80% of cases — rational approximation theory, not physics.

### Method artifacts

| Result | Original claim | Diagnostic finding |
|--------|----------------|--------------------|
| g₂ rep on 7 orbits (`queue_08_g2`) | 16 independent generators with commutant_dim=1 → "G₂ fundamental rep" | (D2) so(7) rank=16 ≠ g₂'s 14; (D4) Casimir eigenvalues `[-3, -2.5×5, -0.5]` spread 2.5 violates Schur scalarity. Root cause: octonion inner-derivation formula `D_{a,b}(z) = [[e_a,e_b],z] - 3[e_a,e_b,z]` applied to *non-alternative* sedenion ambient does not close as a 14-dim Lie algebra. The script's "commutant_dim=1" was an artifact of an ad-hoc projection and a non-Killing-form Casimir sum. **The 16-vs-14 gap is method, not physics.** |
| queue03 legacy threshold scan | portable custodial pass/fail threshold | `scipy.linalg.null_space` admits arbitrary orthogonal bases, while `max(abs(commutator entry))` is basis-dependent. Valid basis changes move values by up to 30.77% and change categorical counts. **NONPORTABLE / INVALID_METHOD; no tolerance relaxation.** |

### Inconclusive (1 remaining after 2026-05-17 method-bug fixes via `inconclusive_redo.py`)

| Result | Original issue | Resolution | Remaining gap |
|--------|----------------|------------|---------------|
| Cooperative vacuum (`queue_06_coop`) | gamma_critical=null (n_trials=20 too low) | Re-run with n_trials=200 → **gamma_critical=0.0**; single-orbit vacuum found at γ=0 already → CONFIRMATION_LOCAL of single-orbit-selection, but the *cooperative* mechanism claim is **REFUTED** because α-perturbation alone selects orbit 1 without needing γ-repulsion | Reclassified to CONFIRMATION_LOCAL with sub-verdict that cooperative-mechanism title is misleading |
| S₃ action (`queue_09_s3`) | group_order=1 from 10000-sample of 12! (~5×10⁸ permutations, too sparse) | Direct 6! = 720 enumeration → finds 720 = S₆ valid index-realizations | Test is *too permissive*: orbit-membership-preservation alone admits the full S₆. The proper S₃ ⊂ Aut(𝕊) = G₂×S₃ test requires sedenion-multiplication-preservation; **INCONCLUSIVE** until that gate is added |

---

## Classification Definitions

### 1. Confirmation
Computation matches a *pre-registered* prediction in the KG `:Contract`. Action: `Contract.confidence += δ`, `last_confirmed = today`.

### 2. Refutation
Computation contradicts a pre-registered prediction. Action: `Contract.status = 'REFUTED'`, parent Span flagged `needs_review = true`.

### 3. Discovery
Result is *novel* — no pre-existing Contract anticipates it. Action: create `:Span {discovered_from: <calc>, status: 'NEW'}` and **re-enter PH2** by dispatching `/apt-sp <new_span_id>`. The workbench thus self-extends.

### 4. Numerology
Numerical coincidence without pre-prediction or with high `P(E|~H)`. Action: `Contract.status = 'NUMEROLOGY_HOLD'` + create `:Possibility` node at low confidence.

Source: [`.claude/skills/science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md).

---

## Fitting Detection (pre-prediction vs post-fitting)

This is the **anti-numerology gate**. For every claimed confirmation, the loop asks: was the prediction registered in the KG **before** the computation ran?

| Detection | Action |
|-----------|--------|
| **pre-prediction** | counts as genuine confirmation |
| **post-fitting** with high `P(E|~H)` | demoted to `:NUMEROLOGY_HOLD` / `:Possibility` |
| **post-fitting** with low `P(E|~H)` and external grounding | counts as `confirmation_local`, requires external peer review for full canon |
| **unknown** | `:VerdictPending` — manual user verdict required |

Provenance check: compare git timestamp of `:Contract` creation against the computation result file's mtime.

### Known historical fitting acknowledgment — UEQFT/ICE 287/15 denominator (2026-02-07)

KG node `UEQFT_ICE_CLUE_ANALYSIS_2026_02_07` (clue_C_honest field) explicitly records: *"15를 분모로 고른 이유가 결과 맞추기. 287/14=20.5, 287/16=17.9도 가능했음."* (English: 287/15 denominator was post-hoc fitting; 287/14 and 287/16 were also computationally available, suppressed after target observation.) `alpha_derivation_status = 'numerology_suspected'`, `alpha_verdict = 'HIGH_RISK - 라그랑지안 직접 유도 필요'`. Documented here per `lesson-prom32-thothsaem-ueqft-claims-2026-05-17` documentation-KG gap recommendation.

---

## Lakatos Evaluation

| Status | Definition | Action |
|--------|------------|--------|
| **progressive** | Research program produces *new* predictions, some confirmed | confidence ↑, continue program |
| **degenerating** | Only re-explains existing data, no novel predictions | confidence ↓, archive program or pivot |

### Per-category Lakatos verdict (2026-05-14)

| Category | Verdict | Reason |
|----------|---------|--------|
| CD breaking | **progressive** | 32D↔64D breaking pattern leads to ZD doublet candidates |
| CD embedding | **progressive** | propagator chain composes, path amplitudes computed |
| Dimensional analysis | **degenerating** (locally) | mass_ratios self-refuted (0/15 genuine); Koide Q is numerology |
| Higgs / S-proofs | **progressive** | S₃ Jacobi, S₅ BV, S₇ WW all yield new structural insights |
| Sedenion (16D) | **progressive** | Der(S)=g₂ verified; SU(2)/SU(3) embeddings extend program |
| Queue series | **mixed** | queue_01 progressive (42 orbit) but queue_02 refutation (custodial fail) |
| Misc verification | **pending** | mp/mW Fitting Detection unresolved |

**Overall** (canonical, post-2026-05-18 reframe): **BIFURCATED**. The *L1 algebra core* is PROGRESSIVE (S₃ Jacobi, S₅ BV, Der(S)=g₂, XOR invariant — genuine structural results). The *L2/L3 physics-prediction belt* is DEGENERATING/STAGNANT (Tüchsen 2024). The "42 ZD as Higgs candidates" is **no longer a progressive novel prediction** — it is NUMEROLOGY (DEAD, p_corr=1.0, 2026-06-01 ledger). Applying a single blanket "confirmations outweigh refutations" Lakatos status to a program that is progressive on the algebra axis and degenerating on the physics axis is drift (`lesson-prom16-hypercomplex-program-bifurcated-verdict-2026-05-18`).

---

## Bayesian Update Discipline

For every Contract update:

```
P(H|E) = P(E|H) · P(H) / P(E)
P(E) = P(E|H) · P(H) + P(E|~H) · P(~H)
```

The **critical term is `P(E|~H)`** — "could this evidence have appeared even without the theory being true?"

- If `P(E|~H)` is high (e.g., a 2/3 ratio appears in countless unrelated contexts) → evidence is *weak*, even if `P(E|H) = 1`.
- If `P(E|~H)` is low (e.g., a specific 42-pair structure with internal consistency) → evidence is *strong*.

Numerology gate: `P(E|~H) > 0.5` ⇒ automatic `:NUMEROLOGY_HOLD` regardless of `P(E|H)`.

---

## KG Canon

ICE_ORCA_DRAGON KG nodes. **⚠️ Reconciled 2026-06-05**: the table that lived here previously listed *aspirational/recommended* node names that were **never materialized** — exact-name queries return **0 rows** (verified by cypher). The rows below are the ACTUAL canonical nodes in Neo4j as of 2026-06-05:

| Node (real) | Type | Role |
|------|------|------|
| `ice-workbench-reframe-canonical-2026-05-18` | `:CanonicalReframe` | Canonical position — ICE = HypercomplexHypothesisTestbench |
| `numerology-verdict-ice-L2L3-2026-06-01` | `:ValidationResult` | L2/L3 belt = 0 SIGNAL_GENUINE / 10 NUMEROLOGY / 1 WEAK (ε) |
| `vr-sci-naesengmoon-ice-2026-06-01` | `:ValidationResult` | Scientific-naesengmoon audit, status=SPLIT_VERDICT |
| `escape-lane-MB1-MB3-MB4-synthesis-2026-05-19` | `:EscapeLaneVerdict` | MB1 escape lane (structurally closed by enumeration 2026-06-05) |
| `CONTRACT: Der(S) = g2 (dim=14)` | `:Contract` | L1 algebra, VERIFIED (conf 1.0; was non-executable until 2026-06-01 cd_embedding fix) |
| `Koide Q = 2/3` / `Koide Q = 2/3 (Z₃ 대칭)` | `:Claim` / `:ICEClaim` | L2 physics, NUMEROLOGY (p_corr→1.0) |
| `oq8-derive_mass_ratios_ICE-FAIL_HARD-2026-05-18` | `:ScriptVerdict` | mass-ratio self-refutation, FAIL_HARD |

> The 7 names previously listed here (`Contract_42_ZD_Higgs_doublet`, `Contract_DerS_eq_g2`, `Possibility_Koide_Q_two_thirds`, `Possibility_mp_mW_3_256`, `Contract_custodial_naive_embedding`, `Contract_derive_mass_ratios`, `Verdict_mass_ratios_2026_self_refutation`) **do not exist in Neo4j** — recommended schema, never created. Enumerate live nodes with `MATCH (n) WHERE n.name CONTAINS 'ice-' OR n.name CONTAINS 'ICE' RETURN n.name`.

KG source: dgx worker MongoDB + Neo4j + Redis (see `CLAUDE.md` → `reference_kg_infra_topology.md`).

---

## Known Limitations

### L1 — No automated CI

Scripts are run manually. There is no GitHub Actions / pre-commit hook that re-runs all 47 scripts on every push. If a script breaks (e.g., numpy API change), it will not be detected until manual re-run.

### L2 — Numerology gate operationalized 2026-05-17 (partial)

**Resolution**: `numerology_mc_judge.py` operationalizes P(E|~H) ≥ 0.5 via explicit MC null models. Three HOLD items processed: Koide Q (P=1.000), mp/mW literal (88.8% rel_diff), mp/mW layer3 (P=0.812) all promoted to **NUMEROLOGY_CONFIRMED**. ε power-law remains HOLD (pass-rate 0.238 — gate non-trivial but no pre-prediction).

**Remaining**: c=4·ln(2) and Bekenstein-connection are session-log items without dedicated result JSONs; need MC null models built before judgment. Hard cases that survive MC (P near boundary) still require human verdict — the rule is now mechanical for the easy cases.

### L3 — Verdict field generalization (partial fix 2026-05-17)

**Status**: 18/18 existing result JSONs now carry a top-level `verdict` field (taxonomy: CONFIRMED / CONFIRMATION_LOCAL / REFUTED / NUMEROLOGY_HOLD / INCONCLUSIVE) plus `verdict_reasoning`, `verdict_source`, `verdict_date`. Distribution: 6 CONFIRMED + 4 CONFIRMATION_LOCAL + 3 REFUTED + 3 NUMEROLOGY_HOLD + 2 INCONCLUSIVE.

**Backfill provenance**: `_patch_verdict_backfill.py` (15 new) + `_patch_verdict_legacy_normalize.py` (3 legacy prose → taxonomy, prose preserved as `verdict_reasoning`).

**Remaining gap**: 29 scripts (of 47) do not emit `_results.json` at all (e.g., `cd_breaking_*`, `cd_embedding_*`, `sedenion_*`, `prove_s1/s2/s3/s7`). Forward fix: each script's JSON-dump path should write a `verdict` field. Not yet done.

# KG: Roadmap #4 partially RESOLVED (backfill complete) — forward enforcement on scripts pending.

### L4 — Der(S) = g₂ has no external peer review

The numerical verification is solid, but no arXiv preprint exists. STATUS remains `confirmation_local`. External submission is a recommended next action.

### L5 — Custodial refutation not yet pivoted

`queue_02` refutes the naive custodial embedding. The legacy queue03 threshold scan is
now quarantined as basis-dependent and cannot provide a "next embedding" candidate.
A basis-invariant v2 needs new preregistration and must first gate closure,
nondegeneracy, and rank 6. The program remains locally degenerating in custodial.

### L6 — Discovery re-entry is manual

When a result is classified `discovery`, `/apt-sp` dispatch is currently manual. A future enhancement: feedback-loop skill auto-dispatches `/apt-sp` and reports the new Span ID.

---

## Position Statement (2026-05-18 — promoted from 2026-05-17 partial retreat)

> User verdict "그렇게 해줘봐봐" (2026-05-18) → PROMOTED partial retreat → **PERMANENT workbench-reframe** per PROM 16 meta-diagnosis (`prom16-hypercomplex-physics-meta-2026-05-18`).

Canonical position (`ICE_WORKBENCH_REFRAME_2026-05-18.md`, supersedes `ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md`):

- **ICE classification**: `:HypercomplexHypothesisTestbench` (was `:PhysicsTheoryProgramme`)
- **L1 Algebra core**: PROGRESSIVE, retained as primary value (Brown 1967 Aut(𝕊)=G₂×S₃, Moreno 1998 Z(𝕊)≅G₂, Reggiani 2024, 5 queue_* CONFIRMED)
- **L2/L3 Physics-prediction belt**: DEGENERATING / STAGNANT (Tüchsen 2024 EJPS third category applied)
- **Mythology layer (USER_PRIMARY)**: PRESERVED untouched (Eilu va-Eilu — narrative-feedback-loop)
- **Single Lean 4 escape lane**: P2 zero-divisor filtration uniqueness (`MIND/lean_formalization/sedenion_uniqueness/`), P=0.04 standalone; workbench-reframe insulates sunk cost
- **5-year discriminator P1-P5 window 2026-2031**: 현재 0/5 satisfied; 1개라도 PASS → reframe 재검토
- **Cross-apostle firewall**: 12사도 #2 6-family CONFIRMED row untouched (family-expansion-pattern §5-D 변경 없음)

### 3-Layer Disclosure (mandatory for all ICE outputs)

Statements must distinguish: *algebra layer* (progressive) vs *workbench tested* (numerology hold) vs *mythology references* (USER_PRIMARY preserved). "ICE predicts X" without layer attribution is forbidden.

---

## Roadmap

> Updated post PROM 16 `prom16-ice-residual-2026-05-17`.

1. **External peer review for Der(S) = g₂** — submit arXiv preprint (g₂ 16-vs-14 in `queue_08_g2` confirmed METHOD_ARTIFACT, 2026-05-17 — non-alternative sedenion ambient breaks octonion derivation formula closure)
2. ✅ **MC p-value tests for numerology candidates** — Koide Q + mp/mW done (`numerology_mc_judge.py`). Remaining: c=4·ln(2), Bekenstein-connection.
3. **Custodial-preserving embedding search** — PROM 16 outcome: pivot to Aut(𝕊) = G₂×S₃ native commuting SU(2)×SU(2) (R4 in PROM_16_REPORT.md). Precondition: R1 4-condition diagnostic.
4. **Self-verdict field on all 47/53 scripts** — partial (18/18 result JSONs done; 30 scripts still produce no JSON). PROM 16 outcome: `_verdict_auto_emit.py` zero-mod hook (R3) + pyastsim canonical pruning 53→~20 (R5).
5. **CI integration** — local strict TypeScript + Effect/Vitest gate is implemented
   (`npm run check`), but GitHub Actions and scheduled mapped-output audits remain unwired.
6. **Auto-dispatch /apt-sp on discovery** — close the recursive loop programmatically
7. **Sedenion-multiplication-preservation gate for queue_09_s3** — PROM 16 outcome: SS3TG triple-gate (R2) signed-permutation M-preservation + BSGS + S₃ presentation. CAVEAT: Aut(𝕊) S₃ factor contested by Wilmot 2025 — `:CompetingVerdict` flag needed.
8. **NEW**: ε P2 zero-divisor filtration (R7) — SYMPOSIUM-novel candidate for MB1 form-uniqueness theorem. Sedenion-derived ε(r) has NO literature precedent (PROM 16 confirmed); P2 = n_eff = 16 − dim(ZD-locus) → forced ε(r) ∝ 1/r^(n_eff+1).
9. **NEW**: 6-criterion promotion bar MB1-MB6 (lesson-prom16-A4-S4) — operationalize NUMEROLOGY_HOLD → SIGNAL transition. NF3 insight: MB1 form-uniqueness theorem obviates trials factor (single proof obligation replaces diffuse LEE patching).
10. **NEW**: Aut(𝕊) dispute resolution — Brown 1967 G₂×S₃ vs Wilmot 2025 G₂-only. SYMPOSIUM should flag `:CompetingVerdict`; Lean 4 formalization on Mathlib CayleyDickson is the resolution path.

---

## SYMPOSIUM Context

ICE_ORCA_DRAGON's science-feedback-loop is the **truth filter** side of the 2026-04-30 closure:

| Side | Loop | Where |
|------|------|-------|
| Science (this workbench) | science-feedback-loop | `.claude/skills/science-feedback-loop.md` |
| Narrative (mythology, THEORY/) | narrative-feedback-loop | `SYMPOSIUM/.claude/skills/narrative-feedback-loop.md` |

Three essential differences from narrative-feedback-loop:

1. Science loop *can* close (refutation is terminal); narrative loop preserves machloket (Eilu va-Eilu).
2. Science loop uses Bayesian update; narrative loop uses hermeneutic circle update.
3. Science loop's pre-prediction discipline; narrative loop's USER_PRIMARY absolute priority.

# KG: ICE_ORCA_DRAGON_status, science-feedback-loop-canonical-ice, narrative-feedback-loop-canonical-2026-04-30
