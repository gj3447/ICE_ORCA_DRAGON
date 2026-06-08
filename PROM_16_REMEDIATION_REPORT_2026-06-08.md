# PROM 16 — ICE_ORCA_DRAGON 잔여 gap 해결 방안 (2026-06-08)

> `/prom 16` — 4 gap축 × 4 렌즈 = 16 cell 웹 리서치 → 합의/충돌 synthesis → **나생문 적대검증**.
> workflow: `ice-remediation-prom-16` (wf_cd3995bd-422, 27 agent / 2.09M tok / 23분).
> cycle anchor: KG `lesson-ice-remediation-prom16-2026-06-08`.
> 정전 전제: ICE = `:HypercomplexHypothesisTestbench` (2026-05-18 reframe). L1 대수=PROGRESSIVE / L2-L3 물리=STAGNANT / 신화=USER_PRIMARY(손 안 댐).

---

## 0. 한 줄

**적대검증이 4 gap 전부의 naive 권고를 뒤집었다. 진짜 DO_NOW는 A1(재현성)뿐 — 단 "재실행→커밋"이 아니라 손으로 backfill된 verdict provenance를 *보존하며* 경로만 고치는 것. A2(수비학)는 도구·판결이 *이미 존재*해서 PARK(stale 라벨 reconcile만), A3(Lean)는 4 sorry 중 3개가 vacuous `True := by sorry`라 split-OPTIONAL, A4(TOE 재오픈)는 정직하게 PARK(닫힘 강화 + 인용 2건 정정).**

리서치 셀은 일반론적으로 "고쳐라"를 냈지만, 적대검증 + 직접 실측이 각 권고가 *이미 닫힌 것을 재오픈*하거나 *기존 자산을 파괴*함을 적발했다. 이 보고의 가치는 **하지 말아야 할 것의 발견**에 있다.

---

## 1. Consensus (9, 모두 HIGH)

| # | cells | 합의 |
|---|---|---|
| C1 | A1×4 | A1 재현성 gap의 단일 직접 원인 = 14 스크립트의 하드코딩 `open("/Users/lagyeongjun/CD/AGENT/...")`. 정전 해법 = 이미 검증된 `ROOT = pathlib.Path(__file__).parent` 패턴으로 1:1 교체. |
| C2 | A1×4 | exit 0 ≠ 재현. 기준 = (코드 실행 → 파일 생성 → committed JSON과 bit-identical). sympy.Fraction exact 산술이 부동소수 비결정성 제거 → hash-match 가능 → CI에 `git diff --exit-code` 또는 golden-file gate. |
| C3 | A2×4 | 3관측량의 naive local p는 거짓 GENUINE. look-elsewhere(trials factor) 보정 필수. |
| C4 | A2×3 | A2 게이트는 실행 *전* pre-registration(후보집합+tolerance+에너지스케일 고정) mandatory. post-hoc menu selection + trials factor 미보정 = 어떤 연속량도 소분수에 맞출 수 있음. |
| C5 | A2,A4 | sin²θ_W=3/8(0.375)은 측정값 0.231과 ~62% 괴리 → ICE 고유 예측 아닌 GUT(SU5) 재발견의 명백한 실패. MC 없이 직접 REFUTED. |
| C6 | A3×4 | Lean sorry oracle의 유일한 compiler-attested 기준 = `lake build` 경고(`declaration uses 'sorry'`) 0줄 **AND** `#print axioms`에 `sorryAx` 부재. grep 카운트는 docstring 문자열 과다계산 → oracle 부적격. lake build exit 0만으론 불충분. |
| C7 | A4×4 | sedenion S₃(Aut(𝕊)=G₂×S₃)가 강제하는 건 이산 {2,3,7,14}뿐, 연속량은 J₃(𝕆)가 강제하거나 외부 매개변수가 채움. avenue3 FAIL은 이 경계와 정합. |
| C8 | A4×3 | TOE 재오픈 게이트 = 4조건 동시: (1) J₃(𝕆)가 안 주는 새 연속 관측량 (2) 세드니온/ZD-locus의 *대수적* 강제(post-hoc fit 아님) (3) MC look-elsewhere 후 p<0.01 (4) Koide/cubic/Singh route로 미설명. |
| C9 | A4×3 | 2025-2026 유일 활성 예측 라인 = Singh J₃(𝕆_ℂ)/E8 (세드니온 아님). 세드니온 ZD 방향에서 MC 통과한 새 연속 관측량 = **0건**. |

---

## 2. Divergence — 충돌 (4) + 직접 실측 해소

리서치 셀 간 수치/대상 불일치를 synthesis와 **내 직접 grep**이 해소.

| 충돌 | 셀 주장 | 실측 해소 |
|---|---|---|
| D1 abs-path 파일 수 | "11개" | **14개** (`derive_{dimensionless,Lstar,mass_ratios}`, `prove_{higgs_ZD_doublet,s3_higher_gauge,s5_bv_ainfty}`, `queue_{01,03,04,05,06,10,11}`, `verify_mp_mW_3_256`). ROI 무영향(둘 다 동일 mechanical 교체). |
| D2 look-elsewhere 구현 | any-target 루프로 "자동 보정" | **단일-ratio null + 명시 Bonferroni** 가 옳음. any-target 앙상블은 p~1로 포화 → 감도 상실(과보정). |
| D3 Lean CI 대상 repo | "ICE에 lake build CI" | **ICE 트리엔 .lean/lakefile 0개.** 실제 파일은 `/CD/MIND/lean_formalization/sedenion_uniqueness/` (lakefile.toml + lean-toolchain 존재). CI는 그쪽에 걸어야. |
| D4 4 sorry 성격 | "모두 trivial stub" | **3 stub(`True := by sorry`) + 1 genuine-conjectural**(SedenionPhase3:129 form_uniqueness_conjecture). 타입교체(R2)가 sorry 제거에 선행. |

### 직접 실측 (memory: critic 수치·파일 claim 재검증 필수)
```
/CD/AGENT/ abs-path write    : 14 파일  ✓ (셀 "11" = undercount)
ROOT = Path(__file__).parent : 10 파일  (synthesis "6"도 undercount)
queue_01 phantom verdict     : JSON 4회 / .py 0회  ✓ (수동 backfill 확정)
ICE 트리 .lean / lakefile    : 0 / 0
MIND/.../sedenion_uniqueness : CayleyDickson/SedenionPhase1-3/SedenionUniqueness.lean + lakefile.toml + lean-toolchain  ✓
```

---

## 3. Open Questions — 단독/저신뢰 (singletons)

| # | cell | 열린 질문 |
|---|---|---|
| OQ1 | A4S2 | **Wilmot 2025 (arXiv:2512.07210)** 가 Aut(𝕊)=G₂ (S₃ 없음) 주장하며 Brown 1967 반박. 미해소 시 S₃-기반 세대 구조 전체 흔들림. 단 avenue3가 genuine outer S₃ 존재를 256 product 전수로 *이미* 검증 → `:CompetingVerdict` 양립 유지. |
| OQ2 | A3S3 | `#print axioms` transitivity 버그 (lean4 issue #8840, 미해결): collectAxioms가 axiom→axiom 재귀 수집 못 함. ICE 단순 tactic sorry는 영향권 밖이나 native_decide 도입 시 sorryAx 누락 가능. |
| OQ3 | A1S3 | committed JSON vs 계산 출력의 phantom 경계. 순수 계산 출력과 수동 해석/verdict를 어떻게 구분 기록할지 (→ §4 A1에서 `computed_keys` provenance로 해소 제안). |
| OQ4 | A4S4 | Singh δ_CP 류 예측이 2026-2027 T2K/NOvA/Hyper-K로 falsify 가능 — J₃(𝕆) 라인 모니터링 대상. **단 §4 A4의 출처 정정 선행.** |

---

## 4. 권장 후속 작업 — 적대검증 교정본 (naive 권고 ✗)

> 각 gap의 리서치 권고를 나생문 렌즈가 *반증*했고, priority가 전부 바뀌었다. 아래는 **교정본**.

### A1 — 재현성 :: **DO_NOW** (단 함정 회피)
naive "14 경로 교체 → 재실행 → 새 JSON 커밋"은 **isSound=False**. 이유:
- committed JSON은 손으로 backfill된 verdict provenance(`verdict_reasoning`/`self_refutation`/`sub_verdicts`/`verdict_source`, `_patch_verdict_backfill.py` + commit 4c5a458) 보유. 스크립트는 이 필드 **emit 0건**. 재실행→덮어쓰면 `derive_mass_ratios REFUTED`·`queue_06 cooperative-mechanism REFUTED` 등 self_refutation 주석 소실 = **Eilu va-Eilu / no-discard / science-feedback-loop verdict taxonomy 위반**.
- `_verdict_auto_emit.py` 가 이미 존재(docstring: "Idempotent: merges via setdefault(). NEVER overwrites pre-existing verdict, preserves 18+ explicit-verdict scripts") → **한 파일에 계산+verdict 공존이 의도된 설계**. queue_01만 별도 파일로 떼면 컨벤션 깸(drift).
- queue_03 committed JSON = *아카이브된 다른 스크립트*(queue_03_rep_decomposition.py) 출력 → 명명된 스크립트의 1:1 매핑 부재 → 생성은 reproduction 아닌 NEW artifact. queue_06 source = `inconclusive_redo.py`. verify_mp_mW = AGENT-dir 출력조차 absent(미실행).

**교정 실행안** (effort ~2-3h, STATE_AUDIT item #5 포섭):
1. **순서 강제**: ① 14 abs-path → repo-root cwd-상대 경로 교체(파일별 결정론적 edit, `git diff` 눈검증, **sed 일괄 금지**). ② 각 스크립트 재실행이 committed JSON을 byte-identical 재생성하는지 확인. **③ 그 다음에야** `uv run python X.py && git diff --exit-code X.json` 을 Makefile/CI에 배선.
2. **덮어쓰기 금지**: verdict provenance는 기존 `_verdict_auto_emit.py` in-file merge로 보존. 각 `_results.json`에 `computed_keys`(스크립트가 실제 emit하는 키 목록) 1필드 추가 → phantom 경계를 *in-place* 명시(파일 분리 X).
3. queue_03/queue_06/verify_mp_mW는 1:1 매핑 부재 → "재현"이 아니라 NEW artifact / 미실행으로 정직 문서화.
4. 골든 템플릿 = queue_02/08/09 (cwd-write). 환경 pin = pyproject.toml + uv.lock (sympy 1.14, numpy 1.26).
5. **게이트 라벨 = REPRODUCIBILITY attestation**("exit-0이 기록된 수를 실제로 썼는가"), correctness/물리진리 주장 **아님** → green CI를 L2/L3 부활로 오독 금지.

### A2 — 수비학 변별 :: **PARK** (→ Occam reconcile만 OPTIONAL)
naive "3관측량에 MC null 신설"은 **isSound=False, 두 검증자 모두 PARK**. 이유:
- **도구 이미 존재**: `ice_prereg_check.py:82-119` 가 단일-ratio `mc_null()` + Bonferroni `p_corr=min(1, p_raw*n_trials)` + 동일 임계(<0.01/<0.5/≥0.5)를 *글자 그대로* 구현. 신설 = 재발명.
- **2/3 이미 판결**: `numerology-weinberg-angle-confirmed-2026-05-18`(p_raw 0.001, **p_corr 0.811**, NUMEROLOGY_CONFIRMED) + `numerology-cabibbo-angle-confirmed-2026-05-18`(p_raw 0.0034, **p_corr 1.0**, NUMEROLOGY_CONFIRMED). frozen `ice_prereg_predictions_2026-05-18.json`(sha256 0bbcbe40)에 등록됨. → `L2L3_NUMEROLOGY_LEDGER_2026-06-01.md`의 "UNTESTED=3" 라벨이 **stale**.
- avenue3 verdict 명시: 이미 numerology로 본 claim에 정교한 null을 새로 짓는 것 = "manufacturing-a-number category error."

**교정 실행안** (effort ~1h, OPTIONAL):
1. **Occam reconcile**: ledger 22-23행 "UNTESTED" → "already-tested-NUMEROLOGY (2026-05-18)" 정정(stale↔canonical drift 해소).
2. 유일한 진짜 미실행 = **CP phase(δ_CP)** 하나. 신규 함수 없이 `PDG_OBSERVABLES`에 1줄(δ_CKM≈1.137 rad PDG2024) 추가 → 기존 Bonferroni 파이프라인 1회 실행 → ledger 마지막 gap 종결(예상 NUMEROLOGY). `derive_dimensionless`의 stale 1.36 rad은 frozen prereg 변조 금지 — 후보값 note로만.
3. 어떤 결과도 TOE band(~0.3%) 못 올림 disclaimer 명기.

### A3 — Lean sorry oracle :: **OPTIONAL (split)**
naive "4 sorry oracle화"는 **isSound=False**. 대상 repo는 `/CD/MIND/lean_formalization/sedenion_uniqueness/`(lakefile.toml + mathlib v4.30.0-rc2 require, 단 `.lake/lake-manifest.json` 부재 = **한 번도 빌드 안 됨**).

**split 교정안**:
- **[L1 순수수학, 진짜 신호 — OPTIONAL]** `CayleyDickson:140 cdtower_dim`(dim=2^n, 귀납) + `:147 sedenion_has_zero_divisors` 만 `True`→실제 prop 타입교체 + 증명. **메커니즘 정정**: `decide`/`norm_num` 단독 불가(ℝ는 computable DecidableEq 없음, classical noncomputable). 올바른 전략 = Cawagas 2004 concrete 유리수 witness → `ext`로 16성분 분해 → `norm_num`/`ring`, a≠0·b≠0은 수동 `ne_zero`. 닫으면 PROGRESSIVE L1 enrichment.
- **[L2-L3 물리, 신호 0 — OPEN_DEFERRED 유지]** `SedenionUniqueness:110 epsilon_form_uniqueness` + `SedenionPhase3:129 form_uniqueness_conjecture` *둘 다* axiom-blocked(`user_verdict_spatial_fiber` re-blocked / `algebraically_forced` placeholder)라 타입교체해도 discharge 불가. escape lane은 이미 `STRUCTURALLY_CLOSED_BY_ENUMERATION`(build_required=false) → oracle화 신호 0. **"의미있는 증명" 서사 붙이지 말 것**(closed 물리층 PASS 분장 금지).
- **oracle gate 정정**: `grep -c "declaration uses 'sorry'"` 는 빌드 *성공* 시에만 warning emit → 빌드 실패면 grep=0을 "sorry 제거"로 오판. ① 먼저 `lake build` 실제 컴파일(.lake 부재 = exit0≠재현, A1과 동형 함정) ② regression = source-regex sorry-token count(빌드 무관) == 4 ③ `#print axioms` 는 빌드 성공 시 부가검증.
- **[PARK]** full Aut(𝕊)=G₂×S₃ Lean 형식화 = 16-24 person-wk(G₂·octonion을 Mathlib에 선축적해야), ROI 0(수학은 Eakin-Sathaye 1990로 기증명, 형식화는 naming/infra; 성공해도 새 연속관측량 0).

### A4 — TOE 재오픈 :: **OPTIONAL / XS** (닫힘 강화 + 인용 정정)
핵심 명제(avenue3 FAIL = 최종 boundary + 4조건 게이트)는 falsifier 통과 → 유지. 단 **두 하위주장 반증**:
1. **"Furey 5-checkpoint"는 canon에 부재.** `FUREY_CxO_PROGRAMME_SCAFFOLD`에는 28 primitive·4×4 axis·15 prediction만 있고 "5-checkpoint"·(3)카이랄성·(5)비독립세대 항목 없음. 게다가 Furey case-study PROM 16은 SCAFFOLD_READY/**미실행**. → 인용 **삭제**(또는 dispatch 실제 실행 후 재검토).
2. **Singh δ_CP=±π/2 = misattribution.** canon Singh 값은 δ²=3/8(POSTDICTION + NUMEROLOGY_CONFIRMED, OQ4)이지 ±π/2 아님. ±π/2는 별개 PMNS 문헌값. → 출처 **분리/정정**.
3. Gresnigt H-overlap 경로(공유 quaternion core {e0,e4,e8,e12}, S3가 3 octonion permute)는 avenue3 prereg line 33에서 *이미 계산됨* = 정확히 F1(counting-then-labeling)+F4(wrong S3, octonion-permuting ρ는 G₂ 안쪽). KR_GRESNIGT는 "proven(count 3)"이나 forced 연속 flavor 0.

**교정 실행안** (effort ~30min, OPTIONAL):
- avenue3 RESULTS.md/KG에 "Gresnigt-overlap + G₂-coset CP 경로 = *별개 미개척 아닌 이미 닫힌 sub-case*" 1줄 명시.
- KG `KR_GRESNIGT_S3_THREE_GENERATIONS` → `verdict-avenue3-decisive-test-FAIL-F5-2026-06-05` `REFINED_BY` edge(롱기누스 바인딩, **삭제 금지**).
- Furey 5-checkpoint 인용 삭제 + Singh 귀속 정정(Verdict provenance로 첨부, AI-사견 Comment 아님).
- 재오픈 게이트는 그대로 — J₃(𝕆)가 침묵하는 *새* 연속 관측량 등장 시에만 (Gresnigt 재계산 아님).

---

## 5. 종합 priority (적대검증 후)

| gap | naive 셀 | 적대검증 교정 | effort |
|---|---|---|---|
| **A1** 재현성 | DO_NOW (덮어써라) | **DO_NOW** (보존하며 경로만, 덮어쓰기 금지) | 2-3h |
| **A2** 수비학 | DO_NOW (MC 신설) | **PARK** → Occam ledger reconcile + δ_CP 1회만 OPTIONAL | 1h |
| **A3** Lean | OPTIONAL (4 oracle화) | **OPTIONAL split** (L1 2개 증명 / L2-L3 2개 OPEN_DEFERRED / full=PARK) | 1-2h(L1) |
| **A4** TOE 재오픈 | OPTIONAL (Furey gate) | **OPTIONAL/XS** (닫힘 강화 + 인용 2건 정정, 신규 탐색 금지) | 30min |

**한 줄**: 살아있는 진짜 작업은 **A1(보존형 재현성 fix)** 하나, 나머지는 위생(A2 reconcile / A3 L1 enrich / A4 닫힘 강화)뿐. TOE 부활·Mathlib full proof는 PARK이 정직하다. **신화 layer는 USER_PRIMARY로 손 안 댐.**

---

## KG
- cycle anchor: `lesson-ice-remediation-prom16-2026-06-08` (`:Lesson`, lakatos_mechanism=lemma-incorporation)
- 16 `:ResearchFinding` (`finding_iceRemed_A1S1` … `A4S4`), `HAS_RESEARCH` from anchor, `PromBatchWrite` gate marker
- 4 `:ActionPlan` (gap별 교정본) + `lesson-ice-naive-remediation-reintroduces-drift-2026-06-08` (adversarial 메타교훈)
- linked: `verdict-avenue3-decisive-test-FAIL-F5-2026-06-05`, `escape-lane-MB1-MB3-MB4-synthesis-2026-05-19`, `numerology-{weinberg,cabibbo}-angle-confirmed-2026-05-18`, `ice-workbench-reframe-canonical-2026-05-18`
