# OQ3 + OQ4 timestamp audit (external paper appropriation 검증)

> **Date**: 2026-05-18
> **Cycle**: autoloop iter 16-25 (60-iter midnight mode)
> **Predecessor**: `OQ8_TIMESTAMP_AUDIT_2026-05-18` + `ICE_PREDICTIONS_AUDIT_BATCH_2026-05-18`

---

## 1. 질문

- **OQ3**: Krasnov 2024 ECM + Gresnigt 2022-2024 측 'falsifiable mass-ratio relations beyond SM' 측 *pre-registered by ICE* 측 vs *post-hoc 측 appropriation*?
- **OQ4**: Singh δ²=3/8 spread 측 ICE algebra 측 *내재적 derivation* 측 vs *PDG-reverse-engineered post-hoc*?

답: 두 측 모두 **APPROPRIATION_NOT_PREDICTION** — external 외부 연구 측 retrospective 측 cited, ICE 측 prior pre-registered claim 측 *없음*.

---

## 2. Available evidence (local)

### 2.1 Local arXiv IDs (직접 cited in ICE findings)

| reference | arXiv | publication | ICE-citation context |
|------|------|------|------|
| Gresnigt 2024 ISQS28 | arXiv:2407.01580 | 2024-07 | f_A2_S3 측 "cleanest hypothesis-B signature" |
| Gresnigt/Furey 2024 EPJC | — (Cl(8)) | 2024 | f_A4_S2 측 PROGRESSIVE evidence |
| Furey 2025 Annalen der Physik | — (Z₂⁵-graded superalgebra) | 2025 | f_A4_S2 |
| Reggiani 2024 | arXiv:2411.18881 | 2024-11 | f_A1_S1 측 "ZD(𝕊) ≅ V₂(ℝ⁷)" |
| Tang 2024 Symmetry | — | 2024 | f_A4_S2 |
| Wilmot 2025 | — | 2025 | f_A4_S2 |
| Furey-Hughes 2023 | — | 2023 | f_A4_S2 + ICE_PHYSICS_CLAIM_ASSESSMENT |
| Gillard-Gresnigt 2019 | — | 2019 | ICE_PHYSICS_CLAIM_ASSESSMENT |
| Krasnov 2024 ECM | — (no local arXiv ID) | 2024 | PROM_16_META_DIAGNOSIS_REPORT (OQ3 측 origin) |
| Singh δ²=3/8 | — (no local arXiv ID) | unknown | PROM_16_META_DIAGNOSIS_REPORT (OQ4 측 origin) |

### 2.2 ICE-internal 측 mythology

- `MIND/metahumotonic/나는야_ice_orca_dragon.md` 측 birth time: **2026-03-27 02:08:49**
- SYMPOSIUM monorepo git init: **2026-05-11**
- `derive_*_ICE.py` git first commit: **2026-05-11 13:34:29** (단일 init commit)

### 2.3 Gap 계산

| external paper | publication | gap to USER_PRIMARY (2026-03-27) | gap to ICE script init (2026-05-11) |
|------|------|------|------|
| Gresnigt 2024 ISQS28 | 2024-07 | **−20 months** (paper 측 먼저) | **−22 months** (paper 측 먼저) |
| Gresnigt/Furey 2024 EPJC | 2024 (avg mid-year) | **−21 months** | **−23 months** |
| Furey 2025 | 2025 (avg mid-year) | **−9 months** | **−11 months** |
| Reggiani 2024 | 2024-11 | **−16 months** | **−18 months** |
| Tang 2024 | 2024 | **−21 months** | **−23 months** |
| Wilmot 2025 | 2025 | **−9 months** | **−11 months** |
| Furey-Hughes 2023 | 2023 | **−33 months** | **−35 months** |
| Gillard-Gresnigt 2019 | 2019 | **−84 months** (7 years 측 먼저) | **−86 months** |
| Krasnov 2024 ECM | 2024 | **−21 months** | **−23 months** |
| Singh δ²=3/8 (year unknown ≤2024) | ≤2024 | **≤ −21 months** | **≤ −23 months** |

**모든 external 측 paper 측 ICE 측 *both* mythology AND script 측 *먼저*.**

---

## 3. OQ3 verdict — Krasnov 2024 + Gresnigt 2022-2024

### 3.1 Pre-registration test

**조건**: ICE 측 specific falsifiable claim 측 pre-register 측 후 측 Krasnov/Gresnigt 측 paper 측 *confirm*?

**측정**:
- ICE 측 falsifiable claim 측 pre-registration 측 *존재하지 않음* (sha256-committed prediction file 측 없음)
- ICE 측 mythology (2026-03-27) 측 *모든 Gresnigt papers* 측 후
- ICE 측 script init (2026-05-11) 측 *모든 Gresnigt papers* 측 후
- `f_A2_S3.json` 측 명시: "Gresnigt 2024 ISQS28 = cleanest hypothesis-B signature: original projection failed for U(1)_em, FIXED projection recovers physics. **Same algebra, different projection.**"
  → "FIXED projection" 측 *Gresnigt* 측 fix, NOT ICE 측 prediction

**OQ3 verdict**: **APPROPRIATION_NOT_PREDICTION**
- ICE 측 Gresnigt et al 측 *외부 결과* 측 retrospectively cite 측 algebra-axis Progressive evidence
- ICE 측 *prior* pre-registered claim 측 *없음*
- Lakatos progressive 측 정의 (novel confirmed prediction) 측 *fail*

### 3.2 Krasnov ECM 측 same pattern

local 측 arXiv ID 측 없음. 그러나 "Krasnov 2024 ECM" 측 *year 2024* 측 ICE init (2026-05-11) 측 *17+ months 측 먼저*. Pre-registration 측 동일하게 fail.

---

## 4. OQ4 verdict — Singh δ²=3/8

### 4.1 알고리즘적 verification

**조건**: Singh δ²=3/8 측 ICE algebra 측 *내재적 derivation* 측 가능?

**측정**:
- ICE algebra-axis 측 derivation: G₂ Casimir / S₃ Weyl element / sedenion ZD orbit 측 결합 측 δ² = ? 측 explicit 측 closed-form derivation 측 *없음* (52 ICE scripts 측 grep 결과 no Singh derivation)
- Singh paper 측 PDG-derived value (lepton CP δ_CP = 3/8 ≈ 0.375 measured) 측 reference
- ICE 측 explanation 측 "δ²=3/8 측 spread" 측 PDG measurement 측 *후* 측 algebra-axis 측 plausible match 측 retrospective claim

**OQ4 verdict**: **POSTDICTION_NOT_DERIVATION**
- ICE 측 Singh δ²=3/8 측 *내재적* 측 derive 측 closed-form 측 *없음*
- PDG-derived value 측 reference (year unknown but ≤2024) 측 ICE init (2026-05-11) 측 *먼저*
- 측 "algebra 측 plausible match" 측 *retrospective claim* 측 fitting category

---

## 5. 두 OQ 측 결과 요약

| OQ | verdict | reason |
|------|------|------|
| **OQ3** (Krasnov 2024 + Gresnigt 2022-2024) | **APPROPRIATION_NOT_PREDICTION** | external papers 측 ICE 측 *모두* 측 먼저, ICE 측 pre-registered claim 측 *없음* |
| **OQ4** (Singh δ²=3/8) | **POSTDICTION_NOT_DERIVATION** | ICE 측 내재적 derivation 측 *없음*, PDG-derived value 측 retrospective match |

---

## 6. Lakatos 측 함의

### 6.1 algebra-axis (sub-fiber Progressive)

- external 측 정전 (Gresnigt, Furey, Reggiani, Tang, Wilmot 2019-2025) 측 *exist*
- 그러나 이 측 ICE 측 *contribution* 측 아님 — external research 측 ICE 측 referencing
- algebra-axis 측 Progressive 측 *legitimate* (외부 정전 측 reproduction + verify), 그러나 ICE-novel 측 아님

### 6.2 physics-prediction-axis (sub-fiber Stagnant)

- OQ3 측 OQ4 측 둘다 *retroactive* appropriation/fitting
- pre-registered prediction 측 0개
- Stagnant verdict 측 강화

### 6.3 Asymmetric Lakatos cycle-novel theorem 측 backing 강화

- physics-fiber 측 Stagnant 측 *empirical evidence 측 추가 2 instances* (OQ3 + OQ4)
- 누적: OQ8 4 FAIL + batch 11 FAIL + OQ3 + OQ4 = **17 instances of physics-fiber retrodiction**
- algebra-fiber Progressive 측 *external verify* 측 confirmed (Brown 1967 / Moreno 1998 / Reggiani 2024 / Gresnigt 2024 / Furey 2024)

---

## 7. Bayesian update

- prior posterior (post batch audit): P(ICE physics-prediction validated) = **0.04**
- OQ3 + OQ4 evidence: 0/2 pre-registered, 2/2 retrospective appropriation
- likelihood factor: 0.7 (weak evidence — already saturated)
- updated posterior: **P ≈ 0.03** (workbench-reframe permanent confidence 강화)

---

## 8. NUMEROLOGY_REGISTRY 측 추가 후보

- **Singh δ²=3/8 = 0.375** 측 algebra-axis 측 plausible matches 측 *MC null gate 측 적용 필요*:
  - G₂ structure: long²/short² = 3, Weyl order = 12 → 3/12 = 0.25 (no match)
  - S₃ permutations: 3!/8 = 0.75 (no match)
  - sedenion ZD orbit: 42/112 = 0.375 ✓ **PLAUSIBLE NUMEROLOGY MATCH** (42 ZD pairs / 112 ?) → MC null model 필요
- **Krasnov mass-ratio claims** 측 specific values 측 local 측 없음 → external 측 reference 측 fetch 필요

---

## 9. KG ingestion 계획

- `:OQ3OQ4AuditResult:VerdictRecord {name: 'oq3-oq4-timestamp-audit-2026-05-18'}` — 본 보고서 측 결정화
- `:Verdict {name: 'OQ3-APPROPRIATION_NOT_PREDICTION-2026-05-18'}`
- `:Verdict {name: 'OQ4-POSTDICTION_NOT_DERIVATION-2026-05-18'}`
- `:NumerologyClassification:HoldCandidate {name: 'singh-delta-sq-3-over-8-mc-gate-needed-2026-05-18'}` — MC null model 측 적용 후 결정

---

## 10. 후속 action

- iter 26-40: self-numerology MC audit (Task #3) — Singh δ²=3/8 측 42/112 = 0.375 match 측 MC null model 측 적용
- iter 41-55: pre-registered NEW prediction derivation — sha256 commit BEFORE PDG comparison (이번 audit 측 pre-registration failure 측 lesson 측 적용)

---

# KG: oq3-oq4-timestamp-audit-2026-05-18, appropriation-not-prediction-pattern-2026-05-18
