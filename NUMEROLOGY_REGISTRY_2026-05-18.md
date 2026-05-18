# Numerology Registry — ICE_ORCA_DRAGON (KG seed)

> **Function**: 본 세션 누적 수비학 분류 측 정전화 + KG ingestion seed
> **Trigger**: 사용자 verdict "수비학좀 정리좀 해줘 / kg 에 수비학인거 정리좀 해줘" (2026-05-18)
> **Predecessor**: `numerology_mc_judge.py` + `numerology_mc_results.json` (2026-05-17 정전화)

---

## 0. 정의 + 결정 규칙

**수비학 (numerology)** = 수치 매칭 / 사후 피팅 / look-elsewhere 효과 / 검색공간 인플레이션 으로 인해 자연 추정 발생하는 outcome 을 "발견" 으로 오인하는 패턴.

**결정 규칙** (`numerology_mc_judge.py` 2026-05-17 정전화):

| P(E|~H) | Verdict |
|---|---|
| < 0.01 (look-elsewhere 보정 후) | SIGNAL_GENUINE |
| 0.01 ≤ P < 0.5 | SIGNAL_WEAK |
| ≥ 0.5 | NUMEROLOGY_CONFIRMED |

수치-매칭 claim 의 default = NUMEROLOGY. MC null model + LEE 보정 후 ≥0.01 통과만 SIGNAL 자격.

---

## 1. NUMEROLOGY_CONFIRMED (P(E|~H) ≥ 0.5, MC-judged)

### N-1. Koide Q = 2/3 (ICE 도출 주장)

| Field | Value |
|---|---|
| KG node | `numerology-koide-q-2-3-ICE-2026-05-17` |
| Source | `derive_dimensionless_results.json` |
| Original claim | "Koide Q = 2/3 measured 가 ICE 의 G2/SU3/XOR_min/ZD 등 small-integer 측 ratio 측 도출됨 (3 개 formula 일치)" |
| MC null model | 499 random ratios from ICE-like atomic integer set, look-elsewhere over 8 targets |
| **P(E|~H)** | **1.000** |
| Verdict | NUMEROLOGY_CONFIRMED |
| Provenance | `numerology_mc_judge.py` 2026-05-17, MC trials = 20000 |
| Interpretation | 499-ratio 측 ensemble 측 어떤 small-rational target 도 거의 확실하게 hit (p≈1). "match" 측 zero information |

### N-2. mp/mW = 3·256 (literal)

| Field | Value |
|---|---|
| KG node | `numerology-mp-mw-3-256-literal-2026-05-17` |
| Source | `verify_mp_mW_results.json` layer1 |
| Original claim | "Proton/W 측 mass ratio 측 = 3·256 = 768" |
| Direct test | Observed mp/mW ≈ 0.01168; predicted 768 → rel_diff = 88.8% (n_sigma = 26.2) |
| Reciprocal test | 1/(3·256) = 0.00130 vs observed 0.01168 → still 88.8% off |
| Verdict | NUMEROLOGY_CONFIRMED |
| Interpretation | Order-of-magnitude 측 빗나감 — 어떤 charitable interpretation 으로도 fit 안 됨 |

### N-3. mp/mW = a·2^n (layer3 search-space inflation)

| Field | Value |
|---|---|
| KG node | `numerology-mp-mw-a-2n-search-2026-05-17` |
| Source | `verify_mp_mW_results.json` layer3 |
| Original claim | "8 가지 mass ratio (mp/mZ, mW/mZ 등) 측 a·2^n 형식 측 fit" |
| MC null model | random R log-uniform ∈ [1e-4, 1e2]; a ∈ [1, 500000] × n ∈ {14..19} search |
| Search space size | ~3,000,000 (a, n) pairs per ratio |
| **P(E|~H)** | **0.812** (81.2% random R fits within 0.1%) |
| Verdict | NUMEROLOGY_CONFIRMED |
| Interpretation | Rational approximation theory, not physics. Search space 측 폭발 |

---

## 2. NUMEROLOGY_HOLD (pending MC or partial)

### N-4. ε(r) Adelberger power-law screening

| Field | Value |
|---|---|
| KG node | `numerology-epsilon-adelberger-screening-2026-05-17` |
| Source | `derive_epsilon_results.json` |
| Original claim | "7 functional form 측 5 개 Adelberger pass = ICE 측 modified gravity 측 derive" |
| MC null model | random eps0 / r0 / alpha log-uniform; Adelberger gate check |
| **P(E|~H)** | **0.238** (gate non-trivial but not stringent) |
| Verdict | **NUMEROLOGY_HOLD** (P 측 SIGNAL_WEAK 구간 측 0.01-0.5 안) |
| Why HOLD not CONFIRMED | Adelberger gate 측 teeth 측 있음 (23.8% pass rate ≠ 100%) |
| Why HOLD not SIGNAL | ICE 측 pre-prediction 측 없음 — 7 form enumeration 측 post-hoc |
| Path to resolution | MB1 form-uniqueness theorem (Lean 4 sister project) — 측 forced form 측 도출 시 SIGNAL 승급 가능 |

### N-5. c = 4·ln(2) (session log, not yet MC-judged)

| Field | Value |
|---|---|
| KG node | `numerology-c-4ln2-2026-04-mid` |
| Source | Session log (pre-2026-05-17, no script artifact) |
| Original claim | "specific dimensionless ratio c 측 = 4·ln(2)" |
| MC null model | NOT YET BUILT |
| Verdict | NUMEROLOGY_HOLD (no MC test) |
| Action | numerology_mc_judge.py 측 extend 측 가능 |

### N-6. Bekenstein connection (session log)

| Field | Value |
|---|---|
| KG node | `numerology-bekenstein-connection-2026-04-mid` |
| Source | Session log (pre-2026-05-17) |
| Original claim | "Bekenstein entropy bound 측 ICE structure 측 connection" |
| MC null model | NOT YET BUILT |
| Verdict | NUMEROLOGY_HOLD |
| Action | Same as N-5 |

### N-7. OQ2 n_eff = 11 (PULLED_BACK 2026-05-18)

| Field | Value |
|---|---|
| KG node | `numerology-oq2-n-eff-11-PULLED-BACK-2026-05-18` |
| Source | `OQ2_DECISION_LOG_2026-05-18.md` STATUS UPDATE banner |
| Original claim | "Spatial fiber dim = 11 측 ε(r) ∝ 1/r^12 측 derive" |
| Lifecycle | RATIFIED_DELEGATED (morning) → audit by user → PULLED_BACK (same day) |
| Why numerology | 5-candidate space {4, 9, 11, 12, 14} + post-hoc rationalization; numerology_mc_judge gate bypassed with prose; 1/r^12 unfalsifiable without forced ε_0 |
| Honest retraction | Yes (2026-05-18 fourteenth pass) |
| Verdict | NUMEROLOGY_HOLD (pulled back, no longer claimed) |

---

## 3. METHOD_ARTIFACT (algebra projection errors creating fake "discoveries")

### M-1. queue_08 g₂ representation (16 generators claim)

| Field | Value |
|---|---|
| KG node | `method-artifact-queue08-g2-16gen-2026-05-17` |
| Source | `queue_08_g2_results.json` |
| Original claim | "independent_generators = 16, commutant_dim = 1 → G₂ fundamental rep 측 7 orbit reps 측 carry" |
| Diagnostic test | `queue_08_g2_diagnostic.py` 4-test suite |
| D1 antisymmetry | PASS (21/21 antisym) |
| D2 so(7) rank | **FAIL** (16 ≠ g₂의 14) |
| D3 Lie closure | median PASS, max residual 0.71 (일부 commutator 안 닫힘) |
| D4 Casimir Schur | **FAIL** (eigenvalues [-3, -2.5×5, -0.5], spread 2.5) |
| Root cause | Octonion inner-derivation formula `D_{a,b}(z) = [[e_a,e_b],z] - 3[e_a,e_b,z]` 측 *non-alternative* sedenion ambient 측 적용 측 닫힌 14-dim Lie 대수 미형성 |
| Verdict | METHOD_ARTIFACT (이전 CONFIRMATION_LOCAL 측 강등) |

### M-2. queue_06 cooperative vacuum (mechanism claim)

| Field | Value |
|---|---|
| KG node | `method-artifact-queue06-cooperative-mechanism-2026-05-17` |
| Source | `queue_06_coop_results.json` |
| Original claim | "γ-driven cooperative SSB 측 7 orbit 측 single-orbit vacuum 측 select" |
| Re-run (inconclusive_redo.py 2026-05-17) | n_trials=200 측 fix → gamma_critical = 0.0 |
| Actual finding | α-perturbation (-1.2 vs -1.0) 측 *단독으로* 측 orbit 1 측 select. γ-repulsion 측 *필요 없음* |
| Sub-verdict | single_orbit_selection = CONFIRMATION_LOCAL (perturbation-driven); **cooperative_mechanism = REFUTED** |
| Verdict | METHOD_ARTIFACT (claim 측 mechanism 측 misleading) |

---

## 4. REFUTED (self-refutation, pre-existing 정전)

### R-1. ICE mass ratios derive_mass_ratios

| Field | Value |
|---|---|
| KG node | `refuted-ice-mass-ratios-self-2026-05-14` |
| Source | `derive_mass_ratios_results.json` |
| Verdict | REFUTED (self) — "ICE cannot genuinely derive (0/15 genuine)" |
| Self-refutation | Yes, prose verdict in JSON |

### R-2. ICE L_star prediction

| Field | Value |
|---|---|
| KG node | `refuted-ice-Lstar-self-2026-05-17` |
| Source | `derive_Lstar_results.json` |
| Verdict | REFUTED (self) — "ICE cannot uniquely predict L_star from internal structure" |
| Normalized | 2026-05-17 (legacy prose → taxonomy) |

---

## 5. REFUTED structurally (test gate broken, not "wrong number")

### S-1. Custodial SU(2)×SU(2) queue_02

| Field | Value |
|---|---|
| KG node | `refuted-custodial-su2xsu2-queue02-structural-2026-05-17` |
| Source | `queue_02_custodial_results.json` + `queue_02_4condition_diagnostic_results.json` |
| Original claim | "42 ZD pairs 측 custodial SU(2)×SU(2) embedding 측 가능" |
| Test result | n_success=0, n_fail=42; max_commutator 1.91-1.96 |
| R1 4-condition diagnostic (2026-05-17) | 100% (42/42) FAIL_BOTH_CLOSURE — c1 (left closure) + c2 (right closure) residual median 3.94; c3 (cross-commutator, 기존) median 1.97 |
| Root cause | 2D ZD null-space projection 측 Lie closure 자체 측 무너짐. naive custodial test 측 *Lie algebra 도 아닌 객체* 측 cross-commutator 측 측정 |
| Verdict | REFUTED structurally (1.93 측 symptom, 원인 = projection 무대 ill-posed) |

---

## 6. Adjacent claims (verified borderline, NOT numerology but in same neighborhood)

### V-1. 42 ZD pairs (count itself)

| Field | Value |
|---|---|
| KG node | `verified-42-zd-pairs-count-CONFIRMED-canonical` |
| External canon | Lygeros 2006 "42 Assessors"; Cawagas 2004; Moreno 1998 |
| Verdict | CONFIRMED (algebra-level count) |
| Numerology adjacent | 42 = Higgs doublet candidate claim 측 *physics interpretation* 측 NUMEROLOGY_HOLD (queue_02 측 SU(2)×SU(2) refuted, 측 "Higgs doublet" 측 무대 측 ill-posed) |

### V-2. Casimir 0.75 uniformity (queue_03)

| KG node | `verified-casimir-075-uniform-CONFIRMED-2026-05-17` |
| Verdict | CONFIRMED (algebra-level invariant) |
| Numerology adjacent | 0.75 = ¾ = SU(2) spin-½ Casimir; consistent with 2D rep across 42 pairs. *Not* a sedenion-specific numerology — generic SU(2) result |

### V-3. XOR invariant 105/105 (queue_11)

| KG node | `verified-sedenion-xor-105-CONFIRMED-2026-05-17` |
| Verdict | CONFIRMED (full sedenion multiplication invariant) |
| Numerology adjacent | None — 100% match 측 strong algebraic invariant |

---

## 7. Meta-numerology (program-level)

### M-meta-1. Hypercomplex → SM 측 50-year stagnation

| Field | Value |
|---|---|
| KG node | `meta-numerology-hypercomplex-sm-50yr-stagnant-2026-05-18` |
| Source | PROM 16 meta-diagnosis f_A4_S1 + f_A4_S2 + f_A4_S3 |
| Programs audited | Dixon 1990-2025 / Furey 2015-2026 / Manogue-Dray 1999-2024 / Köplinger 2006-2023 / Cawagas-descendants 2004-2026 |
| Novel confirmed predictions | **0 genuinely novel** (Koide G₂ Casimir = post-diction, derivation came AFTER PDG confirmation) |
| Lakatos classification | STAGNANT (Tüchsen 2024 EJPS third category) — hard core 보존 + sharp prediction 부재 |
| Falsified predictions | Kaiser 1984 neutron QM null + Procopio 2017 photon null + FAU 2025 |
| Auxiliary hypotheses (protective belt) | Dixon hidden 6D antimatter / Furey deferred top quark / Singh Majorana-only neutrinos / Köplinger untestable QG modulus |
| Implication | ICE 측 6th program in pattern. *Workbench-reframe* 측 honest landing |

---

## 8. PULL_BACK history (verdict reversals)

### P-1. OQ2 n_eff = 11 PULL_BACK (2026-05-18)

| Field | Value |
|---|---|
| KG node | `pullback-oq2-n-eff-11-numerology-hazard-2026-05-18` |
| Original verdict | RATIFIED_DELEGATED 2026-05-18 morning |
| User audit trigger | "지금까지 한거 수비학은 없냐 ㅇㅇ?" |
| Reversal verdict | PULLED_BACK same-day |
| Reason | Internal rule violation (numerology_mc_judge bypassed with prose) + unfalsifiable claim |
| Lesson saved | `lesson-symposium-internal-rule-violation-self-correction-2026-05-18` (memory file) |
| Sunk cost insulation | CONFIRMED — workbench / algebra / mythology layer 측 손상 없이 pull 가능 |

---

## 9. MC null model coverage (gap analysis)

| Item | Has MC null model? | P(E|~H) |
|---|---|---|
| N-1 Koide Q = 2/3 | ✓ | 1.000 |
| N-2 mp/mW 3·256 literal | ✓ (direct comparison) | 88.8% rel_diff |
| N-3 mp/mW a·2^n | ✓ | 0.812 |
| N-4 ε Adelberger | ✓ | 0.238 |
| N-5 c = 4·ln(2) | ✗ (session log, not in script) | unknown |
| N-6 Bekenstein | ✗ (session log) | unknown |
| N-7 OQ2 n_eff=11 | ✗ (rationale 측 prose) | rule-bypass instance |

**Gap action**: extend `numerology_mc_judge.py` 측 N-5/N-6 측 cover. N-7 측 PULL_BACK 측 resolved.

---

## 10. KG ingestion plan (when neo4j MCP loaded)

```cypher
// 본 registry 측 KG seed — direct neo4j write 본 세션 측 tool 미로드, deferred
// 다음 세션 측 db-query skill 측 활용 측 ingest

// Numerology classification nodes
UNWIND [
  {id: "numerology-koide-q-2-3-ICE-2026-05-17", verdict: "NUMEROLOGY_CONFIRMED", p: 1.000},
  {id: "numerology-mp-mw-3-256-literal-2026-05-17", verdict: "NUMEROLOGY_CONFIRMED", rel_diff: 0.888},
  {id: "numerology-mp-mw-a-2n-search-2026-05-17", verdict: "NUMEROLOGY_CONFIRMED", p: 0.812},
  {id: "numerology-epsilon-adelberger-screening-2026-05-17", verdict: "NUMEROLOGY_HOLD", p: 0.238},
  {id: "numerology-c-4ln2-2026-04-mid", verdict: "NUMEROLOGY_HOLD", p: null},
  {id: "numerology-bekenstein-connection-2026-04-mid", verdict: "NUMEROLOGY_HOLD", p: null},
  {id: "numerology-oq2-n-eff-11-PULLED-BACK-2026-05-18", verdict: "PULLED_BACK", reason: "rule_violation"},
  {id: "method-artifact-queue08-g2-16gen-2026-05-17", verdict: "METHOD_ARTIFACT", failed_gates: ["D2", "D4"]},
  {id: "method-artifact-queue06-cooperative-mechanism-2026-05-17", verdict: "METHOD_ARTIFACT", root_cause: "alpha_perturbation_alone_suffices"},
  {id: "refuted-ice-mass-ratios-self-2026-05-14", verdict: "REFUTED_SELF", count: "0/15 genuine"},
  {id: "refuted-ice-Lstar-self-2026-05-17", verdict: "REFUTED_SELF"},
  {id: "refuted-custodial-su2xsu2-queue02-structural-2026-05-17", verdict: "REFUTED_STRUCTURAL", count: "42/42 fail"},
  {id: "meta-numerology-hypercomplex-sm-50yr-stagnant-2026-05-18", verdict: "STAGNANT_PROGRAM", programs: 5, years: 50},
  {id: "pullback-oq2-n-eff-11-numerology-hazard-2026-05-18", verdict: "HONEST_RETRACTION", same_day: true}
] AS row
MERGE (n:NumerologyClassification {id: row.id})
  SET n += row;

// Edges to canonical references
MATCH (n:NumerologyClassification)
MATCH (loop:FeedbackLoopOntology {name: "agent-feedback-loop-canonical-2026-04-27"})
MERGE (n)-[:INSTANCE_OF_FEEDBACK_LOOP]->(loop);

MATCH (n:NumerologyClassification {id: "numerology-oq2-n-eff-11-PULLED-BACK-2026-05-18"})
MATCH (lesson:Lesson {id: "lesson-symposium-internal-rule-violation-self-correction-2026-05-18"})
MERGE (n)-[:RESOLVED_BY]->(lesson);
```

---

## 11. 한 줄 정리

> ICE_ORCA_DRAGON 측 numerology landscape: **3 CONFIRMED + 4 HOLD + 2 METHOD_ARTIFACT + 2 REFUTED self + 1 REFUTED structural + 1 STAGNANT meta-program + 1 PULL_BACK = 14 items**. MC coverage 5/7 (N-5/N-6 측 gap). 본 세션 측 PULL_BACK (N-7) 측 internal rule self-correction 측 demonstration.

# KG: numerology-registry-canonical-2026-05-18 (`:CanonicalRegistry:KG_Seed`, INSTANCE_OF_FEEDBACK_LOOP agent-feedback-loop-canonical-2026-04-27)
