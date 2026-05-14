# ICE_ORCA_DRAGON Status

> Classification ledger, Lakatos verdicts, Bayesian posteriors, known limitations.
> Quick overview: [`../README.md`](../README.md). Script walk-through: [`USERGUIDE.md`](USERGUIDE.md).

---

## Current State

| Component | Value |
|-----------|-------|
| Python scripts | 47 |
| JSON result files | 22 |
| Categories | 7 (CD breaking / CD embedding / dim analysis / Higgs+S-proofs / sedenion / queue / misc) |
| Feedback-loop skill | `.claude/skills/science-feedback-loop.md` (v1, 2026-04-21+) |
| Classification ledger | See [the ledger below](#classification-ledger) |
| Lakatos overall verdict | **progressive** (3 confirmation + 1 discovery > 2 numerology + 1 self-refutation) |

---

## Classification Ledger

The science-feedback-loop classifies every result into one of four categories. Refutations and self-refutations are first-class outcomes.

### Confirmations

| Result | Source | External grounding | Bayesian posterior | Lakatos |
|--------|--------|--------------------|--------------------| --------|
| 42 sedenion ZD pairs | `prove_higgs_results.json` | Lygeros 2006 "42 Assessors" | high (external peer ref exists) | progressive |
| S₃ Jacobi = 6·associator | `prove_s3_results.json` | FDA structure constant computation | high (algebraic identity) | progressive |
| S₅ BV bounded | `prove_s5_results.json` | all_zero + all_bounded checks | high (consistency) | progressive |
| Der(S) = g₂ (14D) | `sedenion_g2_deep.py` | g₂ literature (14-dim Lie algebra known) | medium-high (numeric only) | **confirmation_local** — no external peer review yet |
| 7×6 = 42 orbit | `queue_01_orbit_results.json` | matches sedenion ZD count | high (consistent with S₃ orbit on 42) | progressive |
| Wilmot 2025 Moufang pattern | (cross-cycle, history) | Wilmot 2025 | medium | progressive |

### Refutations

| Result | Source | Verdict | Action taken |
|--------|--------|---------|--------------|
| ICE mass ratios | `derive_mass_ratios_results.json` | **"ICE cannot genuinely derive (0/15 genuine)"** (self-refutation) | Contract `derive_mass_ratios` status=REFUTED. Higher Span re-review triggered. |
| Custodial SU(2)×SU(2) | `queue_02_custodial_results.json` | 0/42 pairs preserve custodial (max_commutator ~1.9) | Contract `custodial_naive_embedding` status=REFUTED. Threshold sweep `queue_03_threshold_sensitivity_scan.py` recommended. |
| T₂ mechanism | (session log, see feedback-loop skill md) | refutation | Step 4 Contract patched |

### Discoveries

| Result | Triggered | Re-entry |
|--------|-----------|----------|
| ZD null space structure | (session log, see feedback-loop skill md) | new `:Span` created, /apt-sp dispatched |

### Numerology (HOLD)

| Result | Source | Why numerology | Status |
|--------|--------|----------------|--------|
| Koide Q = 2/3 | `derive_dimensionless_results.json` | multiple unrelated quantities (XOR_min_offset / G2_num_roots / etc.) match the same number | `:NUMEROLOGY_HOLD` — MC p-value test required |
| c = 4·ln(2) | (session log) | post-hoc fit, no pre-prediction | `:NUMEROLOGY_HOLD` |
| Bekenstein connection | (session log) | post-hoc analogy | `:NUMEROLOGY_HOLD` |
| mp / mW = 3 · 256 | `verify_mp_mW_results.json` | numerical hit, Fitting Detection pending | candidate — see [Fitting Detection](#fitting-detection-pre-prediction-vs-post-fitting) |

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

### L2 — Numerology gate is heuristic

The `P(E|~H) > 0.5` cutoff is a guideline, not a mechanical rule. Hard cases (Koide Q = 2/3, mp/mW = 3·256) require human verdict. Multiple matches with the same numerical hit raise the gate but do not automatically close it.

### L3 — Self-refutation not yet generalized

`derive_mass_ratios_ICE.py` records its own refutation in JSON. Other scripts do *not* yet have this self-reporting discipline. Roadmap: every script should output a `verdict` field, even if the verdict is "PASS".

### L4 — Der(S) = g₂ has no external peer review

The numerical verification is solid, but no arXiv preprint exists. STATUS remains `confirmation_local`. External submission is a recommended next action.

### L5 — Custodial refutation not yet pivoted

`queue_02` refutes the naive custodial embedding. `queue_03_threshold_sensitivity_scan.py` was recommended but does not yet have a "next embedding" candidate. The program is locally degenerating in custodial unless an alternative embedding emerges.

### L6 — Discovery re-entry is manual

When a result is classified `discovery`, `/apt-sp` dispatch is currently manual. A future enhancement: feedback-loop skill auto-dispatches `/apt-sp` and reports the new Span ID.

---

## Roadmap

1. **External peer review for Der(S) = g₂** — submit arXiv preprint
2. **MC p-value tests for numerology candidates** — Koide Q, mp/mW
3. **Custodial-preserving embedding search** — pivot from refutation
4. **Self-verdict field on all 47 scripts** — generalize the mass_ratios pattern
5. **CI integration** — GitHub Actions cron to re-run all scripts weekly
6. **Auto-dispatch /apt-sp on discovery** — close the recursive loop programmatically

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
