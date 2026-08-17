# PROM 16 Report — ICE_ORCA_DRAGON 잔여 4 항목 통합 리서치

> **cycle_id**: `prom16-ice-residual-2026-05-17`
> **N**: 16 (4 axis × 4 sub-axis)
> **Date**: 2026-05-17
> **Findings**: `_findings/prom16-ice-residual/f_A{1..4}_S{1..4}.json` (16/16 verified)

## Axis × Sub-axis Matrix

|        | S1 canonical-refs | S2 industry-impl | S3 alternatives | S4 pitfalls |
|--------|-------------------|------------------|-----------------|-------------|
| **A1** queue_09 S₃ proper test | f_A1_S1 | f_A1_S2 | f_A1_S3 | f_A1_S4 |
| **A2** custodial pivot | f_A2_S1 | f_A2_S2 | f_A2_S3 | f_A2_S4 |
| **A3** 29 no-JSON enforcement | f_A3_S1 | f_A3_S2 | f_A3_S3 | f_A3_S4 |
| **A4** ε pre-prediction | f_A4_S1 | f_A4_S2 | f_A4_S3 | f_A4_S4 |

---

## 0. 사전 지식 (KG Pre-fetch summary)

- ICE_ORCA_DRAGON 53 Python scripts / 18 result JSON / verdict 분포 6 CONFIRMED + 4 CONFIRMATION_LOCAL + 3 REFUTED + 2 NUMEROLOGY_CONFIRMED + 2 METHOD_ARTIFACT + 1 NUMEROLOGY_HOLD + 1 INCONCLUSIVE (2026-05-17 second pass)
- 12사도 #2 ICE의 6-family는 family-expansion-pattern CONFIRMED
- 5무기: Prometheus / Naesengmoon / Longinus / Harness / 재배맨; 본 cycle은 Prometheus 활용
- 기존 `numerology_mc_judge.py` (P(E|~H) decision rule) + `queue_08_g2_diagnostic.py` (4-test 진단) 이번 라운드에서 빌드 완료
- Aut(𝕊) 정전: Brown 1967 G₂ × S₃ — 단 **Wilmot 2025 (arXiv:2512.07210)이 S₃ 부분 contests**, OPEN

---

## 1. 합의 (Consensus, 3+ findings agree)

### C1. queue_09 proper S₃ test = Sedenion S3 Triple-Gate (SS3TG)

**Agreed by**: f_A1_S1, f_A1_S3, f_A1_S4 (+ partial f_A1_S2)

**Gate composition** (모두 동시 통과 필요):
- **G1 multiplication-table preservation**: ∀ (i,j) ∈ {0..15}² (256 entries): σ(e_i · e_j) = σ(e_i) · σ(e_j) with **signed-permutation** representation (π, ε) — sign tracking mandatory, ordered iteration over all 256 (not i<j).
- **G2 BSGS order**: Schreier-Sims deterministic |G|=6 check (NOT random sampling — pitfall b: P(miss)~1).
- **G3 S₃ presentation**: 두 generators r, s 존재 satisfying r³=s²=(rs)²=e — distinguishes S₃ from Z₆ (set-collision).
- **G4 optional**: GAP `StructureDescription()` → "S3" oracle (EPJ-C 2023 canonical).

**Forbidden anti-patterns**: orbit-membership-only (1-closure trap → S₆) / random 12!-sampling / octonion D_{a,b} formula transport (categorical error — Lie tool on discrete π₀) / unordered pairs / |G|-counting alone / single-generator.

### C2. queue_02 custodial naive ansatz DEFINITIVELY refuted; pivot to Aut(𝕊) = G₂ × S₃ native commuting SU(2)×SU(2)

**Agreed by**: f_A2_S1, f_A2_S3, f_A2_S4 (+ pivot mechanics f_A2_S2)

- ICE의 max_commutator 1.91–1.96은 algebraic ceiling (2)의 95–98% → **structural refutation, not threshold issue**. 두 candidate generator가 본질적으로 같은 SU(2) 안에서 living, ~70% subspace overlap.
- BSM 측 5 pivot strategies: **'t Hooft self-dual / anti-self-dual split** (canonical, PIVOT A), quaternionic L/R multiplication (PIVOT B), MCHM SO(5)/SO(4) coset (PIVOT C), bidoublet matrix Σ (PIVOT D), η η̄ orthogonality sanity check (PIVOT E).
- **Top recommendation**: Aut(𝕊) = G₂ × S₃ 의 G₂ factor 내부에 SU(2) × SU(2) direct product 가 native하게 존재 — Aut(𝕊)는 multiplication preserving by definition → ZD-locus 도 preserve. 예상 yield: 14–28/42 pairs pass.
- 사전 진단 필수: 4 conditions (c1 SU(2)_L closure, c2 SU(2)_R closure, c3 cross-commutator, c4 Y consistency [Y, T_L]=0) — 현재 queue_02 는 **c3만 테스트**, c1/c2 가 sedenion 비-alternativity 로 인해 ~70% 자체 실패할 가능성.

### C3. 29 no-JSON 측 verdict 자동 emission = zero-mod 3-layer hook + pytest CI

**Agreed by**: f_A3_S1, f_A3_S2 (+ Variant-prune precondition f_A3_S4)

- **즉시 적용 (legacy retrofit)**: `_verdict_auto_emit.py` ~80 LOC, `atexit + sys.excepthook + signal.SIGTERM` 3-layer, sitecustomize.py 또는 single import. **idempotent merge** via `setdefault()` → 기존 18 JSON 절대 보존. structural verdict는 `COMPLETED|ERROR`만 (`CONFIRMED` 자동 set 금지, MT_RubberStampVerdict 회피).
- **장기 (CI weekly)**: pytest + pytest-json-report + pytest-regressions + GitHub Actions cron `0 6 * * 1`. 기존 `.github/workflows/pytest.yml` 확장. 8-step plan: idempotent main()→test wrappers→conftest fixtures→regression baselines→JSON aggregation→cron workflow→failure notification→drift KG feedback.
- **선결 조건 (f_A3_S4)**: 53 scripts 측 family-prefix bucketing + AST-diff (pyastsim/pycode-similar, NOT md5 — 동일 family 도 hash 다름) → **~20 canonical + 3 tooling**. Variant 측 `_archive/variants/` 이동.
- **REJECTED**: pydantic per-script touch (`_patch_verdict_*.py` 측 이미 실패 evidence), papermill/nbconvert (wrong input format), MLflow/Sacred Phase 1 (ML-shaped, overkill).

### C4. ε(r) pure-algebra 측 unique form 도출은 현재 literature에 NO PRECEDENT

**Agreed by**: f_A4_S1, f_A4_S2, f_A4_S4 (+ partial f_A4_S3 hybrid path)

- **모든 hypercomplex 측 program** (Dixon R⊗C⊗H⊗O, Furey octonion SM, Sorgsepp-Lõhmus ternary, Köplinger conic sedenions, Demir-Tanişli sedenion grav-EM, Wei sedenion curved space) **NONE derive ε(r)** — they reformulate known equations in 16-component algebra.
- ADD's 1/r^(n+1) FORCED-UNIQUE (pure Gauss law in (3+n+1)-dim). RS2 logarithmic + 1/(kr)² UNIQUE given AdS₅. RS1/KK Yukawa-form UNIQUE but params SELECTED. CY landscape: α up to 20, params moduli-dependent.
- Sedenion 16D 측 obstructions: (i) algebraic basis, not spatial manifold → Gauss-flux dilution argument 불가; (ii) zero divisors break norm/composition → flux conservation 불가; (iii) Z(𝕊)≅G₂ (Moreno 1998 + Düvel et al. 2024 arXiv:2411.18881) is rigorous theorem but NOT a gravity prediction.
- **Current NUMEROLOGY_HOLD verdict EXTERNALLY VALIDATED** — field 측 sedenion-derived ε(r) precedent 없음.

### C5. ε promotion bar = 6-criterion (MB1–MB6), 현재 0/6 fully met

**Agreed by**: f_A4_S4 (primary) + f_A4_S1 / f_A4_S3 (corroborate)

- **MB1 form-uniqueness theorem** (mandatory) — Lean 4 preferred per SYMPOSIUM canon
- **MB2 parameter traceability** — every numeric → ICE invariant symbolic expression
- **MB3 independent observable prediction** (mandatory) — beyond Adelberger (Casimir-grav / EP / PPN β-1 / planet perihelion)
- **MB4 :PreregisteredPrediction KG node** timestamp before comparison
- **MB5 trials-factor audit** — current 7 forms × 3 scales × 0.238 per-trial null pass → **0.86 family-wise null pass** (gate 거의 자동 통과 under null)
- **MB6 sensitivity + necessity counterfactual proof** — remove any of 5 ICE-distinctive elements → form changes (sensitivity); no alternative algebra reproduces same form (necessity)
- SIGNAL 격상: ≥4/6 (MB1 + MB3 mandatory). CONFIRMED: 6/6 + external replication.
- **NF3 핵심 통찰**: MB1 form-uniqueness theorem 증명 시 trials factor = 1 → MB5 LEE penalty 자동 obviate. 즉 단일 high-leverage 증명 obligation 이 diffuse statistical patching 을 대체.

---

## 2. 분기/대립 (Divergence)

### D1. Aut(𝕊) S₃ factor 존재 — Brown 1967 vs Wilmot 2025

- **f_A1_S1 / f_A1_S2** 정전: Brown 1967 Pacific J. Math. + 50+ year 인용 chain (Eakin-Sathaye, Moreno, Kirshtein, Cawagas, Gillard-Gresnigt, Furey-Hughes, Masi 2021) → Aut(𝕊) = G₂ × S₃.
- **f_A1_S1 caveat 측 발견**: Wilmot 2025 (arXiv:2512.07210 + 2505.11747)은 calibration-Θ argument 로 Brown 의 doubling rotation 이 canonical 3-form 보존 못함 → **Aut(𝕊) = G₂ only**, S₃ 거부.
- 또는 양측이 다른 object 측 dispute: algebra Aut (Wilmot G₂) vs minimal-ideal action via Spin(8) triality (physics lit G₂ × S₃).
- **SYMPOSIUM 처리**: `:CompetingVerdict` flag, 사용자 verdict 없이 어느 쪽도 고집 금지.

### D2. ε(r) unique form 도출 가능성 — A4-S1/S2 측 NO vs A4-S3 측 hybrid YES

- **f_A4_S1 + f_A4_S2**: pure algebra 알고 form 측 unique 도출 NO precedent. Compactification topology / EFT matching geometric input 필요.
- **f_A4_S3**: (c) AC decoupling + (b) EFT naturalness hybrid → **two-branch unique pre-prediction**: Yukawa exp(−r/λ_G₂) (alternative G₂ subalgebra branch, AC applies) **OR** power-law (r₀/r)⁴ (non-alternative branch, AC fails, dim-8 surviving operators). Branch selection rule = M_G₂ vs Λ_sed/√7 (algebraic).
- **Resolution**: f_A4_S3 측 hybrid 도 결국 "alternative vs non-alternative split" 이라는 algebraic 측 prior commit 이 필요 — 순수 algebra 단독은 아님. Path 측 SYMPOSIUM-novel 후보 (f_A4_S2 측 P2 zero-divisor filtration 과 연결 가능).
- Λ_sed = M_pl/√7 quantitative estimate 측 **NUMEROLOGY_HOLD** sub-candidate (numerology_mc_judge 측 재검증 필요).

### D3. Legacy retrofit pathway — sitecustomize (A3-S1) vs libcst codemod (A3-S3)

- **f_A3_S1**: atexit + excepthook via sitecustomize.py — **zero source modification**, 가장 invasive 적음.
- **f_A3_S3**: libcst codemod 측 transformer — 단일 commit 으로 53 scripts 측 uniform shape, schema 측 명시적 commit.
- **Resolution**: 양립 가능. Phase 1 sitecustomize (즉시 효과, no commit), Phase 2 libcst (장기 정전화 — schema 측 source-of-truth 화).

---

## 3. Open Questions

| OQ | 내용 | Resolution path | Priority |
|---|---|---|---|
| OQ1 | Aut(𝕊) = G₂ vs G₂ × S₃ — Wilmot 2025 dispute | 사용자 verdict OR 양측 양립 정전화 (`:CompetingVerdict`) | HIGH |
| OQ2 | G₂-holonomy 7-manifold 측 KK Yukawa α-value? (n-torus α=2n, n-sphere α=n+1 만 tabulated; G₂-manifold 측 literature gap) | PROM 16/32 dedicated cycle | MEDIUM |
| OQ3 | f_A4_S2 P2 zero-divisor filtration → n_eff = 16 − dim(ZD-locus) 측 forced ε(r) ∝ 1/r^(n_eff+1) 도출 가능? | SYMPOSIUM-novel 시도 | HIGH (high-leverage if successful) |
| OQ4 | 12사도 #2 ICE 측 6-family ↔ custodial SO(4) 측 6 generators 측 structural match? | code-level structural test | MEDIUM |
| OQ5 | Sedenion ZD propagator non-invertibility 측 true AC failure or gauge artifact? | f_A4_S3 측 hybrid path 측 핵심 정전화 | MEDIUM |
| OQ6 | NUMEROLOGY_HOLD 측 split: HOLD_PROMOTABLE (path to MB1 visible) vs HOLD_STALLED (no path)? | KG ontology 정전화 | LOW |
| OQ7 | ICE 53 → ~20 canonical 측 election 측 사용자 verdict (default heuristic: latest mtime + smallest LOC + suffix in {final, definitive}) | 사용자 1회 verdict (blanket-proceed 가능) | MEDIUM |
| OQ8 | Mathlib Lean 4 측 sedenion-automorphism theorem 측 부재 (CayleyDickson 측 존재) → SYMPOSIUM 기여 후보 | Lean 4 형식화 plan | LOW |

---

## 4. 권장 후속 작업 (ActionPlan)

### 즉시 실행 (R1–R3, Phase ACTION)

**R1. queue_02 4-condition diagnostic 재실행** (f_A2_S4 제안)
- 42 ZD pairs 각각에 c1 (SU(2)_L closure), c2 (SU(2)_R closure), c3 (cross-commutator, 기존), c4 (Y consistency) 모두 기록
- 가설 검정: c1/c2 가 ~70% 측 자체 실패 (sedenion 비-alternativity) → 1.93 cross-commutator 는 symptom 이지 root cause 가 아님
- ETA: ~30분, no new physics, queue_02_custodial_check_v2.py 신규

**R2. queue_09 SS3TG triple-gate 구현** (f_A1_S4 제안)
- `queue_09_S3_action_v2.py`: signed-permutation (π, ε) representation + 256-entry M-preservation + Schreier-Sims BSGS + S₃ presentation r³=s²=(rs)²=e
- Pre-built: hypercomplex Python 측 e_matrix() 활용
- Cross-validate: Wilmot's geoalg + GAP LOOPS bound (loop-level)
- ETA: 2-3 시간

**R3. `_verdict_auto_emit.py` 설치** (f_A3_S1 제안)
- ~80 LOC drop-in (atexit + excepthook + SIGTERM)
- Idempotent merge via setdefault — 18 기존 JSON 절대 보존
- sitecustomize.py OR per-script `import _verdict_auto_emit`
- ETA: 1 시간

### 중기 (R4–R7, Phase FUTURE)

**R4. Aut(𝕊) commuting SU(2)×SU(2) embedding 시도** (f_A2_S3 제안)
- `queue_02b_custodial_check_AutS.py`: build_AutS_generators(n=4) → split_into_SU2_pair() → find_AutS_preserving_pairs()
- 예상 yield: 14–28/42 pass
- 사용자 verdict 게이트: Wilmot dispute (OQ1) → S₃ 가정 사용 여부

**R5. 53 → ~20 canonical pruning** (f_A3_S4 제안)
- pyastsim cluster (threshold ≥0.80) → user election → `_archive/variants/`
- KG `:VariantOf` edges
- Default heuristic: latest mtime + smallest LOC + suffix in {final, definitive}

**R6. pytest weekly CI 구축** (f_A3_S2 제안)
- `tests/ice/` wrappers (~20 canonical) + conftest.py + pytest-regressions baselines
- `.github/workflows/ice-weekly.yml` cron `0 6 * * 1` + failure notification

**R7. ε P2 zero-divisor filtration 시도** (f_A4_S2 + f_A4_S3 measured)
- 가설: n_eff = 16 − dim(ZD-locus) → forced ε(r) ∝ 1/r^(n_eff+1)
- 성공 시 SYMPOSIUM-novel contribution; MB1 form-uniqueness theorem 측 첫 후보
- 사용자 verdict 게이트: novel research 본격 진입

### 장기 (R8–R10, Phase MAINTAIN/MONITOR)

**R8.** Lean 4 형식화 — Mathlib `CayleyDickson` 위에 Sedenion + Automorphism theorem (Wilmot dispute 측 settle 후보)
**R9.** G₂-holonomy 7-manifold KK Yukawa α-value 계산 (OQ2)
**R10.** Wilmot dispute resolution 측 사용자 verdict 후 정전 update + family-expansion-pattern 측 #2 ICE 측 sub-family 측 6-family 측 자체 검증 update

---

## 5. Lesson 결정화 후보

| Lesson ID | wrongAssumption | truth |
|---|---|---|
| `lesson-prom16-A1-S4-SS3TG-triple-gate-2026-05-17` | orbit-membership 보존 단독 = S₃ test | 1-closure trap → S₆; signed-permutation M-preservation + BSGS + S₃ presentation triple-gate 필요 |
| `lesson-prom16-A2-S4-naive-custodial-4condition-2026-05-17` | [T_L, T_R]=0 단독 test (condition iii) 가 custodial gate | 4 conditions (i SU(2)_L closure, ii SU(2)_R closure, iii cross-commutator, iv Y consistency) 모두 필요; sedenion 비-alternativity 로 c1/c2 가 c3 보다 먼저 실패 |
| `lesson-prom16-A3-S1-zero-mod-retrofit-2026-05-17` | per-script edit (pydantic) 가 47 scripts 측 scaling 됨 | `_patch_verdict_*.py` 측 evidence 가 per-script retrofit 실패 증명; atexit+excepthook+SIGTERM 3-layer 측 zero-mod 가 dominant strategy |
| `lesson-prom16-A4-S4-promotion-bar-MB1-MB6-2026-05-17` | Adelberger pass + 5/7 forms surviving = SIGNAL evidence | MB1 form-uniqueness theorem MANDATORY; trials-factor 86% family-wise null pass; MB1 증명 시 trials factor=1 → LEE obviate (NF3 high-leverage insight) |
| `lesson-prom16-aut-S-citation-dispute-2026-05-17` | Brown 1967 Aut(𝕊) = G₂ × S₃ 측 50+ year 인용 chain → 정전 settled | Wilmot 2025 (arXiv:2512.07210) 측 calibration-Θ argument 가 Brown 의 S₃ doubling rotations 거부; `:CompetingVerdict` 측 양측 양립 정전화 필요 |

---

## 6. Filesystem dispersion (Step 6.5 slot resolve)

| Layer | 산출 | 본 cycle |
|---|---|---|
| L1 | `METAHUMOTONIC/ICE_ORCA_DRAGON/PROM_16_REPORT.md` (this) | ✅ |
| L2 | axis-split MD per axis (`A1_queue09_s3.md` 등) | ⏳ axis_count=4 ≥ threshold 4 → 산출 권장 (사용자 verdict 게이트, 생략 가능) |
| L3 | `_findings/prom16-ice-residual/f_*.json` 16개 | ✅ |
| L4 | KG nodes/edges | ⏳ (neo4j MCP 측 본 cycle 미접근, 후속 결정화 작업 필요) |
| L5 | MinIO mirror | ⏳ optional (canon-track 여부 사용자 verdict) |
| L6 | `:UpperWorldRef` (60+ 학술/책/OSS refs cited in findings) | refs 측 16 finding JSON 측 보존 |
| L7 | 새 skill 결정화 | ✅ 후보 5 lessons (위 §5), HIGH consensus 5+ 시 skill 격상 |

---

## 7. Cycle 통계

- **subagent dispatch**: 16/16 successful (single-message parallel)
- **avg tokens per agent**: ~67k
- **avg duration**: ~180s
- **total wall time**: ~12 min parallel
- **citations harvested**: 60+ unique academic/OSS refs across 4 axes
- **novel SYMPOSIUM contributions identified**: 4
  1. SS3TG sedenion S₃ triple-gate (unpublished in OSS)
  2. queue_02 4-condition diagnostic + Aut(𝕊) native embedding pivot
  3. 53→20 canonical pruning + zero-mod verdict retrofit pattern
  4. ε form-uniqueness theorem + MB1-MB6 promotion bar (NF3 LEE obviate insight)

# KG: cycle prom16-ice-residual-2026-05-17, 5 lesson candidates, 8 OQ, 10 ActionPlan items (R1-R10), 16 findings written verified=true gate_passed=true
