# Workbench Reframe Propagation Audit — 2026-05-19

> **Purpose**: completeness audit of `ICE_WORKBENCH_REFRAME_2026-05-18.md` §3 "3-Layer Disclosure mandatory" across submodule. Per `feedback_canon_propagation_simultaneous`, partial propagation = stale source contamination risk.
>
> **Trigger**: 2026-05-18 reframe PERMANENT promotion; README/SOURCES top-of-file banners propagated same-day; per-script layer attribution deferred.
>
> **Scope**: every `*.py` / `*.md` that produces or references "ICE predict(s|ed|ion) X" claims.

---

## 1. Audit method

```bash
grep -nE "ICE\s+(prediction|predicts|predicted|implies|requires|claims)" --include='*.py' --include='*.md' -r .
```

Then for each hit, verify either:
1. Reframe-meta-doc reference (acceptable: discusses the rule itself), OR
2. Carries an explicit `# WORKBENCH-LAYER: L1|L2|L3 ...` header tag.

---

## 2. Pre-audit state (drift detected)

| Class | Files | Action |
|---|---|---|
| Reframe-meta-doc (acceptable) | `ICE_WORKBENCH_REFRAME_2026-05-18.md`, `ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md`, `ICE_PHYSICS_CLAIM_ASSESSMENT.md`, `docs/STATUS.md` §Position Statement, README/SOURCES banners | no change — these *define* the rule |
| Comment / docstring claim WITHOUT layer attribution | `orca_friedmann.py:356`, `derive_mass_ratios_ICE.py:13`, `verify_mp_mW_3_256.py:73,330`, `_findings/A2_sedenion_usage_audit.md:9` (challenge quotation) | patched (added WORKBENCH-LAYER header) |
| Physics-prediction script WITHOUT header but producing predictions | `derive_dimensionless_ICE.py`, `derive_epsilon_ICE.py`, `derive_Lstar_from_ICE.py`, `higgs_mechanism.py`, `prove_s7_WW_evasion.py` | patched |
| Algebra-core script WITHOUT header (low priority but propagation hygiene) | `prove_s1_framing.py`, `prove_s2_CCWZ.py`, `prove_s3_higher_gauge.py`, `prove_s5_bv_ainfty.py` | patched as L1 algebra core |

---

## 3. Post-audit state

| Layer | Files tagged (count) | Files |
|---|---|---|
| **L1 algebra core (PROGRESSIVE)** | 5 | `prove_s1_framing.py`, `prove_s2_CCWZ.py`, `prove_s3_higher_gauge.py` (CONFIRMED), `prove_s5_bv_ainfty.py` (CONFIRMED), `prove_s7_WW_evasion.py` (structural internal-consistency check) |
| **L2/L3 physics-prediction belt (STAGNANT)** | 7 | `derive_dimensionless_ICE.py`, `derive_epsilon_ICE.py` (single escape lane per §5), `derive_Lstar_from_ICE.py`, `derive_mass_ratios_ICE.py`, `higgs_mechanism.py`, `orca_friedmann.py`, `verify_mp_mW_3_256.py` |
| **Mythology layer** | (no code) | preserved untouched per §1 USER_PRIMARY |

Verification:

```bash
grep -c "^# WORKBENCH-LAYER" derive_*.py verify_*.py higgs_*.py orca_*.py prove_s*.py
# expected: 12 / 12 with count=1
```

Result: 12/12 PASS.

---

## 4. Boundary-case rulings

### 4.1 `prove_s7_WW_evasion.py` — L1 or L2/L3?

ICE-internal label is `SPAN_ICE_L3_S7` (path-integral layer L3 of Track A). Workbench-reframe §3 lists `prove_s3` and `prove_s5` explicitly as L1 algebra core CONFIRMED; s7 (WW evasion) is structural internal-consistency check verifying the path integral does not violate the WW no-go.

**Ruling**: L1 algebra core (structural). Caveat noted in header that the 86% LEE null pass (workbench-reframe §3) applies only when re-interpreted as L2/L3 SM gauge-boson claim, not as the algebra-structural evasion construction itself.

### 4.2 `derive_epsilon_ICE.py` — STAGNANT but single escape lane

Per workbench-reframe §5, this is the single Lean 4 escape lane (MB3 Adelberger comparison). Tagged L2/L3 STAGNANT with explicit escape-lane note in header.

### 4.3 "ICE-internal L3" vs "workbench L3" disambiguation

ICE Track A labels paths/proofs with `SPAN_ICE_L3_...` (path-integral layer 3 of Track A internal numbering). The workbench-reframe `L3 physics-prediction belt` is a *different* layer (Tüchsen 2024 fiber stratification axis). Five S1~S7 scripts now carry an explicit disambiguation note: ICE-internal "L3" label ≠ workbench L3.

### 4.4 Paper drafts (`papers/asymmetric_lakatos_paper_draft_2026-05-18.md`, `papers/prereg_lakatos_methodology_paper_draft_2026-05-18.md`)

Papers use "algebra sub-belt vs physics-prediction sub-belt" terminology (Lakatos fiber-stratified language). Semantically equivalent to L1/L2/L3 disclosure. No "ICE predicts X" without qualification found. Cross-reference to ICE_WORKBENCH_REFRAME is a nice-to-have for external publication but not a propagation gap (papers stand on Lakatos methodology contribution).

### 4.5 Result JSON files (`derive_*_results.json`)

JSON outputs do not carry comment metadata. Their producing scripts now have WORKBENCH-LAYER tags; results inherit the layer attribution by source. Future enhancement: add `workbench_layer` JSON field at write time (deferred — not a propagation gap, audit hygiene).

---

## 5. Remaining audit items (deferred — non-violation)

- `queue_01..11_*.py` — sedenion structural scans, L1 algebra core. Per workbench-reframe §3 "5 queue_* CONFIRMED" no claim of SM-prediction. Tagging deferred (no current "ICE predicts X" claim language).
- `cd_*.py` — Cayley-Dickson computational suite, L1 algebra core. Same disposition.
- `sedenion_*.py` — sedenion analysis, L1 algebra core. Same disposition.
- `zd64_analysis.py` — zero divisor 64D analysis, L1 algebra core. Same disposition.

These could be tagged in a future low-priority pass for completeness. They do not currently contain "ICE predicts X" language and so do not constitute propagation violations.

---

## 6. Canonical propagation invariant (per `feedback_canon_propagation_simultaneous`)

When a canonical rule is amended (workbench-reframe 2026-05-18), all *active source files* that could be cited as authority must be updated atomically. Stale sources cause sweep agents to be contaminated.

This audit closes the propagation gap from 2026-05-18 (banners only) → 2026-05-19 (per-script layer tags on all 12 physics-claim scripts).

---

## 7. KG hooks (proposed)

- `workbench-reframe-propagation-audit-2026-05-19` (`:PropagationAudit:VerdictRecord`)
  - `:VERIFIES` → `ice-workbench-reframe-canonical-2026-05-18`
  - `:APPLIES_RULE` → `feedback-canon-propagation-simultaneous`
  - `scripts_tagged_count` = 12
  - `scripts_remaining_low_priority_count` = ~25 (queue/cd/sedenion/zd64)
  - `verdict` = PROPAGATION_COMPLETE_FOR_PHYSICS_CLAIM_SCRIPTS

- `lesson-workbench-reframe-banner-not-enough-2026-05-19` (`:Lesson`)
  - `wrongAssumption`: "Top-of-file README/SOURCES banner is sufficient for propagation"
  - `truth`: "Per-script layer attribution is necessary; banners are global context but cannot prevent per-call drift when scripts are run/cited in isolation"
  - `evidence`: 12 scripts updated 2026-05-19 after banner-only state on 2026-05-18

---

## 8. 한 줄 정전

**12 physics-claim scripts tagged with workbench layer 2026-05-19; propagation gap from 2026-05-18 banner-only state closed. Future low-priority pass for ~25 L1-algebra-core scripts deferred (no current violation).**

---

# KG: workbench-reframe-propagation-audit-2026-05-19, lesson-workbench-reframe-banner-not-enough-2026-05-19
