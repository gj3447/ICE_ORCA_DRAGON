# ICE_ORCA_DRAGON Status

> Classification ledger, Lakatos verdicts, Bayesian posteriors, known limitations.
> Quick overview: [`../README.md`](../README.md). Script walk-through: [`USERGUIDE.md`](USERGUIDE.md).

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
| Lakatos overall verdict | **progressive** (11 confirmation > 3 refutation + 2 numerology + 1 inconclusive; novel predictions present, look-elsewhere effects quantified) |

---

## Classification Ledger

The science-feedback-loop classifies every result into one of four categories. Refutations and self-refutations are first-class outcomes.

### Confirmations (6 CONFIRMED + 4 CONFIRMATION_LOCAL = 10)

| Result | Source | External grounding | Bayesian posterior | Lakatos |
|--------|--------|--------------------|--------------------| --------|
| 42 sedenion ZD pairs | `prove_higgs_results.json` | Lygeros 2006 "42 Assessors" | high (external peer ref exists) | progressive |
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

### Method artifact (1, demoted from CONFIRMATION_LOCAL via `queue_08_g2_diagnostic.py`)

| Result | Original claim | Diagnostic finding |
|--------|----------------|--------------------|
| g₂ rep on 7 orbits (`queue_08_g2`) | 16 independent generators with commutant_dim=1 → "G₂ fundamental rep" | (D2) so(7) rank=16 ≠ g₂'s 14; (D4) Casimir eigenvalues `[-3, -2.5×5, -0.5]` spread 2.5 violates Schur scalarity. Root cause: octonion inner-derivation formula `D_{a,b}(z) = [[e_a,e_b],z] - 3[e_a,e_b,z]` applied to *non-alternative* sedenion ambient does not close as a 14-dim Lie algebra. The script's "commutant_dim=1" was an artifact of an ad-hoc projection and a non-Killing-form Casimir sum. **The 16-vs-14 gap is method, not physics.** |

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

**Overall**: progressive — confirmations + discoveries outweigh refutations + numerology, *and* the program produces novel predictions (e.g., 42 ZD as Higgs candidates) rather than only re-explaining.

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

ICE_ORCA_DRAGON canon nodes (recommended):

| Node | Type | Role |
|------|------|------|
| `ICE_ORCA_DRAGON_apostle_2_physics_workbench` | `:Workbench` | Top-level workbench |
| `science-feedback-loop-canonical-ice` | `:FeedbackLoopOntology` | Loop definition |
| `Contract_derive_mass_ratios` | `:Contract` | status=REFUTED (self) |
| `Contract_42_ZD_Higgs_doublet` | `:Contract` | status=CONFIRMED (external Lygeros 2006) |
| `Contract_DerS_eq_g2` | `:Contract` | status=CONFIRMED_LOCAL (numeric only, no peer review) |
| `Contract_custodial_naive_embedding` | `:Contract` | status=REFUTED (queue_02) |
| `Possibility_Koide_Q_two_thirds` | `:Possibility` | status=NUMEROLOGY_HOLD |
| `Possibility_mp_mW_3_256` | `:Possibility` | status=NUMEROLOGY_HOLD (Fitting Detection pending) |
| `Verdict_mass_ratios_2026_self_refutation` | `:Verdict` | linked to Contract_derive_mass_ratios |

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

`queue_02` refutes the naive custodial embedding. `queue_03_threshold_sensitivity_scan.py` was recommended but does not yet have a "next embedding" candidate. The program is locally degenerating in custodial unless an alternative embedding emerges.

### L6 — Discovery re-entry is manual

When a result is classified `discovery`, `/apt-sp` dispatch is currently manual. A future enhancement: feedback-loop skill auto-dispatches `/apt-sp` and reports the new Span ID.

---

## Position Statement (2026-05-17)

> User verdict "2번으로 한번 드가줘봐봐" → physics-prediction layer 부분 후퇴 formalized.

Canonical position (`ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md`):

- **Math layer**: CONFIRMED, robust (Aut(𝕊) = G₂ × S₃ via R2 SS3TG, 7 confirmation results retained)
- **Mythology layer (USER_PRIMARY)**: PRESERVED untouched (Eilu va-Eilu — narrative-feedback-loop)
- **Physics-prediction layer**: PARTIAL RETREAT (Higgs doublet / custodial / Koide / mp/mW / ε form all REFUTED or NUMEROLOGY)
- **Reversibility**: 5 RESUMPTION_HOOK triggers — R4 PASS, R7 PASS, Wilmot dispute settled, user verdict, new empirical evidence

The retreat is partial and reversible. Math + mythology layers retain ICE's role as 12사도 #2; only the *direct physics-prediction* claim is demoted.

---

## Roadmap

> Updated post PROM 16 `prom16-ice-residual-2026-05-17`.

1. **External peer review for Der(S) = g₂** — submit arXiv preprint (g₂ 16-vs-14 in `queue_08_g2` confirmed METHOD_ARTIFACT, 2026-05-17 — non-alternative sedenion ambient breaks octonion derivation formula closure)
2. ✅ **MC p-value tests for numerology candidates** — Koide Q + mp/mW done (`numerology_mc_judge.py`). Remaining: c=4·ln(2), Bekenstein-connection.
3. **Custodial-preserving embedding search** — PROM 16 outcome: pivot to Aut(𝕊) = G₂×S₃ native commuting SU(2)×SU(2) (R4 in PROM_16_REPORT.md). Precondition: R1 4-condition diagnostic.
4. **Self-verdict field on all 47/53 scripts** — partial (18/18 result JSONs done; 30 scripts still produce no JSON). PROM 16 outcome: `_verdict_auto_emit.py` zero-mod hook (R3) + pyastsim canonical pruning 53→~20 (R5).
5. **CI integration** — PROM 16 outcome: pytest+pytest-json-report+regressions+GH Actions cron `0 6 * * 1` (R6 8-step plan in PROM_16_REPORT.md).
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
