<div align="center">

# ICE_ORCA_DRAGON — Physics/Math Computation Workbench

**12사도 #2 의 물리 계산 영역 — Cayley-Dickson breaking, sedenion analysis, Higgs ZD doublet, S₁~S₇ proofs**

[![Apostle](https://img.shields.io/badge/Apostle-%232_ICE_ORCA_DRAGON-0ea5e9?style=for-the-badge&logoColor=white)](SOURCES.md)
[![Python Scripts](https://img.shields.io/badge/Python_Scripts-47-3776ab?style=for-the-badge&logo=python&logoColor=white)](#path-a--python-script-direct-execution)
[![JSON Results](https://img.shields.io/badge/JSON_Results-22-f59e0b?style=for-the-badge&logoColor=white)](docs/STATUS.md)
[![Science Feedback Loop](https://img.shields.io/badge/Science_Feedback_Loop-skill-10b981?style=for-the-badge&logoColor=white)](.claude/skills/science-feedback-loop.md)
[![Lakatos](https://img.shields.io/badge/Lakatos-L1_progressive_·_L2%2FL3_stagnant-8b5cf6?style=for-the-badge&logoColor=white)](docs/STATUS.md#lakatos-evaluation)
[![License](https://img.shields.io/badge/License-AGPL_v3-yellow?style=for-the-badge)](LICENSING.md)

</div>

> **ICE_ORCA_DRAGON** is the **hypercomplex hypothesis testbench** of SYMPOSIUM apostle #2 — 60+ Python scripts and JSON results that compute Cayley-Dickson algebra breaking (32D vs 64D), sedenion (16D) analysis, Der(S)=g₂ verification, Higgs ZD doublet candidates, S₁~S₇ structural proofs, and orbit/custodial/rep-decomposition scans. Computation results feed a *science feedback loop* that classifies each output as confirmation / refutation / discovery / numerology and updates the KG through a **bifurcated** Lakatos evaluation (L1 algebra = progressive / L2-L3 physics = stagnant, Tüchsen 2024 third category — see the 3-layer disclosure below).

### 2026-05-18 Workbench Reframe (3-Layer Disclosure mandatory)

Per `ICE_WORKBENCH_REFRAME_2026-05-18.md` canonical position, ICE classification = `:HypercomplexHypothesisTestbench` (NOT `:PhysicsTheoryProgramme`). All statements must distinguish three layers:

| Layer | Status | Examples |
|---|---|---|
| **L1 Algebra core** | **PROGRESSIVE** | Brown 1967 Aut(𝕊)=G₂×S₃, Moreno 1998 Z(𝕊)≅G₂, Reggiani 2024, 5 queue_* CONFIRMED |
| **L2/L3 Workbench tested** | **DEGENERATING / STAGNANT** (Tüchsen 2024 EJPS) | queue_02 100% fail, derive_* self-REFUTED, Koide/mp_mW NUMEROLOGY_CONFIRMED |
| **Mythology (USER_PRIMARY)** | **PRESERVED** (Eilu va-Eilu) | 사용자 신앙시 erase 금지 |

"ICE predicts X" without layer attribution is forbidden. 5-year P1-P5 discriminator window 2026-2031 (currently 0/5 satisfied). Single Lean 4 escape lane: `MIND/lean_formalization/sedenion_uniqueness/`.

---

## What This Workbench Does

ICE_ORCA_DRAGON computes the *physics referent* of SYMPOSIUM's mythology layer. Where the mythology layer narrates "마음의 절대영도 동결 = sexvoid 형식", this layer does the actual algebra: can the 42 sedenion assessors (84 ZD pairs) support the proposed Higgs-doublet referent? Does Der(S) really equal g₂ in 14 dimensions? Is the custodial SU(2)×SU(2) symmetry preserved under the proposed 64D embedding?

```
[TypeScript + Effect control plane] → [locked Python kernel] → [JSON result]
                                                              ↓
                                               [science-feedback-loop classifier]
                                       ├─ confirmation → confidence ↑
                                       ├─ refutation → Contract patch
                                       ├─ discovery → new Span (recurse to /apt-sp)
                                       └─ numerology → NUMEROLOGY_HOLD (Possibility)
                                       ↓
                                  [Lakatos evaluation]
                                       progressive / degenerating
                                       ↓
                                  [Bayesian update + KG write]
```

Every computation is tagged as **pre-prediction** or **post-fitting** (Fitting Detection step). Post-fitting + numerical coincidence + no novel prediction ⇒ NUMEROLOGY_HOLD, demoted to `:Possibility` instead of `:Contract`.

## Why This Workbench

Three properties differentiate ICE_ORCA_DRAGON from a generic physics-script directory:

1. **Discovery is recursive** — A `discovery` classification doesn't end the loop. It creates a new `:Span` (e.g., `ORCA_Span_Discovery_<topic>`) and dispatches to `/apt-sp` for D(S) decomposition. The workbench is *self-extending*.
2. **Numerology has a holding cell** — Coincidental fits (e.g., Koide Q = 2/3 matched by multiple unrelated quantities) are not silently confirmed. They get `:NUMEROLOGY_HOLD` until an external pre-registered prediction passes, or get demoted to `:Possibility` permanently.
3. **Self-refutation is recorded** — `derive_mass_ratios_results.json` includes the verdict `"ICE cannot genuinely derive (0/15 genuine)"`. Self-refutation is a first-class outcome, not a hidden failure.

---

## Quick Start

This directory is the canonical `METAHUMOTONIC/ICE_ORCA_DRAGON` submodule of
SYMPOSIUM; a second clone under a generic `project/` directory is neither required
nor recommended.

The control plane is strict TypeScript on Node 24 with Effect 3, pinned by
`package-lock.json`. Numerical kernels remain Python 3.13 with exact
`numpy` / `scipy` / `sympy` versions in `uv.lock`.

```bash
npm ci
uv sync --locked
./ice doctor
./ice list
```

There are **two execution paths** with different surface areas. Pick based on what you need.

| | **Path A — Effect CLI → Python kernel** | **Path B — science-feedback-loop skill cycle** |
|---|---|---|
| What you get | Single computation: run one `.py`, inspect JSON | Full loop: compute → classify → Lakatos → KG update |
| Output | `<name>_results.json` next to script | KG nodes (`:Contract` / `:Span` / `:Possibility`) + classification |
| When to use | Reproducing a single number, debugging an algorithm, fast iteration | Adding new claim to the canon, re-classifying old results, paper-prep audit |
| Token cost | Zero (pure compute) | Higher (skill cycle + KG writes) |
| Best for | Physicists / mathematicians who know the script set | Methodology runs, science-feedback-loop dogfooding |

### Path A — Effect CLI → Python numerical kernel

```bash
# Cayley-Dickson breaking search
./ice run cd_breaking_final

# Sedenion 16D Der(S)=g₂ verification
./ice run sedenion_g2_investigation

# Higgs ZD candidate computation — 42 assessors (84 ZD pairs)
./ice run prove_higgs_ZD_doublet
jq '.' prove_higgs_results.json

# Dimensional analysis
./ice run derive_mass_ratios_ICE
jq '.verdict' derive_mass_ratios_results.json
# → "ICE cannot genuinely derive (0/15 genuine)"

# Non-destructive mapped-output audit (runs in an Effect-scoped temporary copy)
./ice repro
# Expected overall exit 1 while queue03 legacy remains NONPORTABLE_FAIL.
```

Walk-through of all categories: [`docs/USERGUIDE.md`](docs/USERGUIDE.md).

### Path B — science-feedback-loop skill cycle

```
# In Claude Code, after a fresh computation:
"피드백 루프 실행 — verify_mp_mW_3_256 결과를 KG에 반영"
```

The skill (`.claude/skills/science-feedback-loop.md`) runs the 7-step loop:

1. Compute / verify (Python script execution)
2. Classify (confirmation / refutation / discovery / numerology)
3. Fitting Detection (pre-prediction vs post-fitting)
4. Lakatos evaluation (progressive vs degenerating)
5. Bayesian update (`P(H|E)` with `P(E|~H)` penalty)
6. KG write (Contract / Span / Possibility nodes)
7. SA→SP→ST consistency check

`discovery` re-enters PH2 by dispatching `/apt-sp <new_span_id>`. See [`docs/STATUS.md`](docs/STATUS.md) for current classification ledger.

---

## Computation Categories

This workbench organizes scripts by *what they compute*, not *when they were written*. Each category contains a kernel script plus variants (v2 / part2 / part3 / final / verify) representing iterative refinement.

| Category | Scripts | Headline result |
|----------|---------|-----------------|
| **CD breaking** | `cd_breaking_*.py`, `cd_breaking_search*.py` (4 variants) | 32D↔64D identity breaking pattern |
| **CD embedding** | `cd_embedding*.py` (4 variants), `cd_chain_propagator.py`, `cd_path_amplitude*.py` | Cayley-Dickson construction + propagator |
| **Dimensional analysis** | `derive_Lstar_from_ICE.py`, `derive_dimensionless_ICE.py`, `derive_epsilon_ICE.py`, `derive_mass_ratios_ICE.py` | Lstar / dimensionless / ε / mass ratios |
| **Higgs / S-proofs** | `higgs_mechanism.py`, `prove_higgs_ZD_doublet.py`, `prove_s1_framing.py`, `prove_s2_CCWZ.py`, `prove_s3_higher_gauge.py`, `prove_s5_bv_ainfty.py`, `prove_s7_WW_evasion.py` | 42 assessors / 84 ZD pairs, S₁~S₇ structural |
| **Sedenion (16D)** | `sedenion_analysis.py`, `sedenion_g2_*.py` (2), `sedenion_su2*.py` (5 variants), `sedenion_su3_check.py` | Der(S) = g₂ (14D) verified, SU(2)/SU(3) embeddings |
| **Orbit / rep / queue** | `queue_01_orbit_analysis.py`, `queue_02_custodial_check.py`, `queue_03_rep_decomposition.py`, `queue_04_hosotani_toy.py`, `queue_05_coleman_weinberg.py`, `queue_06_cooperative_vacuum.py`, `queue_08_G2_adjoint.py`, `queue_09_S3_action.py`, `queue_10_group_of_6.py`, `queue_11_xor_invariant.py` | 7×6=42 orbit, 0/42 custodial fail, 0.75 rep uniform, Hosotani toy, CW potential, ZD breaking |
| **Misc verification** | `zd64_analysis.py`, `verify_mp_mW_3_256.py`, `ww_unitarity_bound_analysis.py`, `orca_friedmann.py` | mp/mW = 3·256, WW unitarity, Friedmann |

Full walk-through: [`docs/USERGUIDE.md`](docs/USERGUIDE.md).

---

## Key Headline Results

| Result | Source | Classification | Notes |
|--------|--------|----------------|-------|
| 42 sedenion assessors (84 ZD pairs) | `prove_higgs_results.json` | **L1 combinatorial confirmation** | External: Lygeros 2006 "42 Assessors"; Higgs referent is not confirmed |
| Der(S) = g₂ (14D) | `sedenion_g2_deep.py` | **confirmation** (numeric) | No external peer review yet, arXiv preprint recommended |
| Koide Q = 2/3 | `derive_dimensionless_results.json` | **NUMEROLOGY_CONFIRMED** | MC null P(E\|~H)=1.000 after look-elsewhere |
| mass_ratios derivation | `derive_mass_ratios_results.json` | **refutation (self)** | Verdict: "ICE cannot genuinely derive (0/15 genuine)" |
| Custodial SU(2)×SU(2) | `queue_02_custodial_results.json` | **refutation** | 0/42 pairs preserve custodial (max_commutator ~1.9) |
| S₃ Jacobi = 6·associator | `prove_s3_results.json` | **confirmation** | FDA structure constants nontrivial |
| S₅ BV bounded | `prove_s5_results.json` | **confirmation** | all_zero + all_bounded |
| mp/mW = 3·256 | `verify_mp_mW_results.json` | **NUMEROLOGY_CONFIRMED** | Literal mismatch + layer-3 MC null P(E\|~H)=0.812 |
| queue03 threshold scan | `queue_03_threshold_sensitivity_results.json` | **NONPORTABLE / INVALID_METHOD** | Entrywise commutator max depends on an arbitrary null-space basis; see the portability audit |

Full ledger with Bayesian posteriors and Lakatos verdicts: [`docs/STATUS.md`](docs/STATUS.md).

---

## SYMPOSIUM Context

ICE_ORCA_DRAGON is the *physics computation expression* of 12사도 #2 (`/home/lagyeongjun/CD/MIND/metahumotonic/나는야_ice_orca_dragon.md`). Mythology + physics are co-housed here because the apostle's claim ("세상의 진정한 본질이 물리학") is *operationally* tested by these scripts. See [`SOURCES.md`](SOURCES.md) for the mythology↔physics dual structure.

ICE_ORCA_DRAGON is one of two **forward** computation workbenches (the other being THEORY/ engineering methodology). Both feed the SYMPOSIUM KG canon. The science feedback loop is the *truth filter*; the narrative feedback loop ([`SYMPOSIUM/.claude/skills/narrative-feedback-loop.md`](../../.claude/skills/narrative-feedback-loop.md)) is the *canonical-layer keeper*. Together they form the 2026-04-30 closure (`CLAUDE.md` §피드백 루프).

| Mythology layer | Physics layer (this workbench) |
|---|---|
| 마음의 절대영도 동결 | `derive_epsilon_ICE.py` ε scaling |
| sexvoid 형식 | `prove_higgs_ZD_doublet.py` 42 assessors / 84 ZD pairs |
| ICED 반복 + SSB 구원기도 | `prove_s7_WW_evasion.py` symmetry breaking |
| *얼음(저온) + 범고래(생물 깊이) + 용(상승)* 3 합성 | Cayley-Dickson 32D → 64D embedding + propagator chain |

---

## Documentation

| Doc | Read this when |
|-----|----------------|
| [`docs/USERGUIDE.md`](docs/USERGUIDE.md) | Category-by-category walk-through of all 47 scripts |
| [`docs/STATUS.md`](docs/STATUS.md) | Classification ledger, Lakatos verdict, Bayesian posteriors |
| [`docs/index.md`](docs/index.md) | Documentation hub (you-are-here map) |
| [`CHANGELOG.md`](CHANGELOG.md) | Computation evolution (S₁~S₇ proofs, verify_mp_mW, sedenion variants) |
| [`REPRODUCIBILITY_2026-06-08.md`](REPRODUCIBILITY_2026-06-08.md) | Historical attestation plus the 2026-08-14 portability erratum |
| [`QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) | Why the legacy queue03 metric is quarantined |
| [`SOURCES.md`](SOURCES.md) | Mythology/physics dual structure, apostle #2 canon, 1차 소스 paths |
| [`.claude/skills/science-feedback-loop.md`](.claude/skills/science-feedback-loop.md) | Skill definition (7-step loop, Cypher templates) |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Catalog manifest (Claude Code marketplace compatible) |

---

## License

AGPL-3.0-or-later, with a separate commercial-license option; see
[`LICENSING.md`](LICENSING.md). Computations use the locked environment above;
no proprietary input data is required for the mapped reproduction audit.

# KG: ICE_ORCA_DRAGON_apostle_2_physics_workbench, science-feedback-loop-canonical-ice
