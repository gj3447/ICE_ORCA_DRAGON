---
title: ICE_ORCA_DRAGON Documentation Hub
description: Physics/math computation workbench — Cayley-Dickson breaking, sedenion analysis, Higgs ZD doublet, S₁~S₇ proofs, science-feedback-loop
---

# ICE_ORCA_DRAGON Documentation

**ICE_ORCA_DRAGON** is the physics-computation side of SYMPOSIUM apostle #2.
A TypeScript + Effect control plane manages the locked Python numerical kernels and
their JSON results. Every scientific result still feeds a *science-feedback-loop*
that applies Fitting Detection, Lakatos evaluation, and Bayesian/KG discipline.

```bash
npm ci
uv sync --locked
./ice doctor
npm run check
./ice list
```

## Quick Links

| Doc | Read this when |
|-----|----------------|
| [`../README.md`](../README.md) | First time using ICE_ORCA_DRAGON — start here |
| [`USERGUIDE.md`](USERGUIDE.md) | Category-by-category walk-through of 47 scripts |
| [`STATUS.md`](STATUS.md) | Classification ledger, Lakatos verdicts, Bayesian posteriors |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Computation evolution (S₁~S₇, verify_mp_mW, sedenion variants) |
| [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md) | Historical attestation and current portability contract |
| [`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) | queue03 method quarantine evidence |

## Theory & Sources

| Doc | What it covers |
|-----|----------------|
| [`../SOURCES.md`](../SOURCES.md) | Mythology/physics dual structure, apostle #2 canon, 1차 소스 paths |
| `/home/lagyeongjun/CD/MIND/metahumotonic/나는야_ice_orca_dragon.md` | User's primary mythology source (자칭, CHU 명단) |
| `/home/lagyeongjun/CD/MIND/metahumotonic/얼어붙은_강물의_노래.md` | ICED 반복 + SSB 구원기도 canon |
| [`../../PROM_64_REPORT.md`](../../PROM_64_REPORT.md) | METAHUMOTONIC axiom12 cycle |
| [`../../PROM_16_PHYSICS_REPORT.md`](../../PROM_16_PHYSICS_REPORT.md) | Physics reinforcement cycle |
| [`../../PROM_64_RESOLUTION_REPORT.md`](../../PROM_64_RESOLUTION_REPORT.md) | 4 미해결 해결 경로 |

## Feedback Loop

| Doc | Role |
|-----|------|
| [`../.claude/skills/science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md) | Skill definition: 7-step loop (compute → classify → Fitting Detection → Lakatos → Bayesian → KG → consistency check) |
| [`STATUS.md#classification-ledger`](STATUS.md#classification-ledger) | Current classification of all results |
| [`STATUS.md#fitting-detection-pre-prediction-vs-post-fitting`](STATUS.md#fitting-detection-pre-prediction-vs-post-fitting) | Anti-numerology gate |
| [`STATUS.md#lakatos-evaluation`](STATUS.md#lakatos-evaluation) | Progressive vs degenerating per category |
| [`STATUS.md#bayesian-update-discipline`](STATUS.md#bayesian-update-discipline) | `P(E|~H)` discipline |

## Computation Categories

| Category | Scripts | Walk-through |
|----------|---------|--------------|
| CD breaking | 5 (`cd_breaking_*`, `cd_final_quick.py`) | [`USERGUIDE.md#category-1--cayley-dickson-breaking`](USERGUIDE.md#category-1--cayley-dickson-breaking) |
| CD embedding & propagator | 7 (`cd_embedding*`, `cd_chain_propagator.py`, `cd_path_amplitude*`) | [`USERGUIDE.md#category-2--cayley-dickson-embedding--propagator`](USERGUIDE.md#category-2--cayley-dickson-embedding--propagator) |
| Dimensional analysis | 4 (`derive_*_ICE.py`) | [`USERGUIDE.md#category-3--dimensional-analysis`](USERGUIDE.md#category-3--dimensional-analysis) |
| Higgs / S-proofs | 7 (`higgs_*`, `prove_higgs_*`, `prove_s1_~s7_*`) | [`USERGUIDE.md#category-4--higgs-mechanism--s₁s₇-proofs`](USERGUIDE.md#category-4--higgs-mechanism--s₁s₇-proofs) |
| Sedenion (16D) | 9 (`sedenion_*`) | [`USERGUIDE.md#category-5--sedenion-16d-analysis`](USERGUIDE.md#category-5--sedenion-16d-analysis) |
| Queue / orbit / rep | 11 (`queue_01~11_*`) | [`USERGUIDE.md#category-6--orbit--rep--queue-series`](USERGUIDE.md#category-6--orbit--rep--queue-series) |
| Misc verification | 4 (`zd64_analysis.py`, `verify_mp_mW_3_256.py`, `ww_unitarity_bound_analysis.py`, `orca_friedmann.py`) | [`USERGUIDE.md#category-7--misc-verification`](USERGUIDE.md#category-7--misc-verification) |

## Key Headline Results

| Result | Source | Classification |
|--------|--------|----------------|
| 42 assessors / 84 ZD pairs | `prove_higgs_results.json` | L1 combinatorial confirmation; Higgs referent not confirmed |
| Der(S) = g₂ (14D) | `sedenion_g2_deep.py` | confirmation_local (no peer review yet) |
| Koide Q = 2/3 | `derive_dimensionless_results.json` | NUMEROLOGY_CONFIRMED |
| ICE mass_ratios | `derive_mass_ratios_results.json` | **self-refutation** (0/15 genuine) |
| Custodial SU(2)×SU(2) | `queue_02_custodial_results.json` | refutation (0/42 fail) |
| S₃ Jacobi = 6·associator | `prove_s3_results.json` | confirmation |
| S₅ BV bounded | `prove_s5_results.json` | confirmation |
| mp / mW = 3·256 | `verify_mp_mW_results.json` | NUMEROLOGY_CONFIRMED |
| queue03 threshold scan | `queue_03_threshold_sensitivity_results.json` | NONPORTABLE / INVALID_METHOD |

Full table with Bayesian posteriors: [`STATUS.md#classification-ledger`](STATUS.md#classification-ledger).

## SYMPOSIUM Cross-References

| Concept | Where |
|---------|-------|
| Apostle #2 mythology layer | [`../SOURCES.md`](../SOURCES.md) |
| Apostle #2 canon (mythology paper source) | `/home/lagyeongjun/CD/MIND/metahumotonic/나는야_ice_orca_dragon.md` |
| Engineering methodology (forward) | [`../../../THEORY/APT/`](../../../THEORY/APT/) |
| Reverse methodology (code → design recovery) | [`../../../THEORY/TPA/`](../../../THEORY/TPA/) |
| Narrative feedback loop (mythology-side complement) | [`../../../.claude/skills/narrative-feedback-loop.md`](../../../.claude/skills/narrative-feedback-loop.md) |
| Five weapons (orthogonal tools) | [`../../../THEORY/HARNESS/`](../../../THEORY/HARNESS/), [`../../../THEORY/PROMETHEUS/`](../../../THEORY/PROMETHEUS/), [`../../../THEORY/TALIBAN/`](../../../THEORY/TALIBAN/), [`../../../THEORY/LONGINUS/`](../../../THEORY/LONGINUS/), [`../../../THEORY/재배맨/`](../../../THEORY/재배맨/) |
| Reproducibility KG dump | [`../../../REPRODUCTION/`](../../../REPRODUCTION/) |

## Plugin Manifest

See [`../.claude-plugin/plugin.json`](../.claude-plugin/plugin.json) for Claude Code marketplace catalog of the 47-script set + feedback-loop skill.

## Mythology ↔ Physics Bridge

ICE_ORCA_DRAGON is unique among SYMPOSIUM apostles in that *its mythology layer makes physical claims*. The mythology says "세상의 진정한 본질이 물리학"; this workbench *operationally tests* that claim. The mythology-physics dual:

| Mythology phrase | Physics-side test |
|------------------|-------------------|
| 마음의 절대영도 동결 | `derive_epsilon_ICE.py` ε scaling toward zero |
| sexvoid 형식 | `prove_higgs_ZD_doublet.py` 42 assessors / 84 ZD pairs as candidate inputs |
| ICED 반복 + SSB 구원기도 | `prove_s7_WW_evasion.py` Ward-Takahashi evasion structure |
| 얼음 + 범고래 + 용 3 합성 | Cayley-Dickson 32D → 64D embedding + propagator chain composition |

The science-feedback-loop's *refutation discipline* is what prevents this dual from collapsing into pure numerology. When the mythology claim fails operationally (e.g., `derive_mass_ratios` 0/15 genuine), the workbench records the failure honestly.

---

# KG: ICE_ORCA_DRAGON_docs_index, ICE_ORCA_DRAGON_apostle_2_physics_workbench
