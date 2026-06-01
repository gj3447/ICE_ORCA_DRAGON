# 과학나생문 (Scientific Naesengmoon) 적대 검증 — ICE_ORCA_DRAGON

> cycle: `sci-naesengmoon-ice-2026-06-01` · lens: `scientific` (4 sub-lens, 직교, short-circuit, UNANIMOUS_PASS)
> VR: `vr-sci-naesengmoon-ice-2026-06-01` (KG, 4 USED_LENS + 3 AdversarialChallenge)
> executor (parent) ≠ reviewer (`naesengmoon-ensemble-critic`) — 자기검증 아님 (D20).
> LensSet 정의: `SYMPOSIUM/THEORY/나생문/LENSES/scientific.md`

**3-Layer Disclosure** (ICE 정전 의무, `ICE_WORKBENCH_REFRAME_2026-05-18.md` §3): 본 문서의 verdict는 ICE를 `:HypercomplexHypothesisTestbench`로 다룬다. "ICE predicts X" 금지 — layer 명시 형식 준수.

---

## 1. claim × sub-lens verdict

| claim (layer) | SCI-A 반증가능성 | SCI-B 통계·과정 | SCI-C 재현성 | SCI-D 인과 | 집계 |
|---|---|---|---|---|---|
| **L1 Aut(𝕊)=G₂×S₃** (algebra) | PASS — progressive, 외부 정전 grounded, 반례 1개면 무너짐 (반증가능) | N/A (정리, MC null 부적용) | PASS — prove_s3/s5 + queue_* CONFIRMED, 결정론적 재현 | N/A (정리는 인과 claim 아님) | **PASS** |
| **L2 Koide Q=2/3** | REFUTE — degenerating, Z₃ 사후부착, novel content 0 → SCI-A 단락 | oracle: **NUMEROLOGY_CONFIRMED** P=0.999 (20000 trials) | reproducible-but-wrong | REFUTE — mechanism 미식별, association | **REFUTE** |
| **L2 mp/mW** (3×256 + a²ⁿ) | REFUTE — derive_* self-REFUTED 0/15 | oracle: **NUMEROLOGY_CONFIRMED** ×2 | reproducible-but-wrong | REFUTE | **REFUTE** (null 가장 contestable, AC2) |
| **L3 P01 Higgs doublet** (g₂→2) | REFUTE — pre-reg verified했으나 degenerating | oracle: p_raw=0.038 → **p_corr=1.0** look-elsewhere kill = NUMEROLOGY | reproducible | REFUTE | **REFUTE** (가장 견고) |
| **L3 custodial/Higgs 일반** | REFUTE — queue_02 100% FAIL_BOTH_CLOSURE, 0/6 MB | post-hoc, 다중비교 미보정 | reproducible | mechanism≠proof | **REFUTE** |
| **ε epsilon** (Adelberger) | CONDITIONAL — degenerating belt, oracle 신호 boundary | oracle: **SIGNAL_WEAK** (0.01≤P<0.5) | reproducible | 인과 미식별 | **escalate-to-oracle = SIGNAL_WEAK 종착** |

---

## 2. layer 최종 verdict

| layer | verdict |
|---|---|
| **L1 algebra** | **PASS** (만장일치, 단 AC4 정정 후) — AC1 해소 + **AC4: 첫 audit은 stale했음** (아래 §6) |
| **L2/L3 physics belt** | **REFUTE** — SCI-A 단락 + SCI-B oracle + SCI-D 3중 over-determined |
| **ε epsilon** | **SIGNAL_WEAK boundary** (종착, 재실행 불요) |
| **신화 layer** | 적용범위 밖 (USER_PRIMARY, Eilu va-Eilu, erase 0) |
| **reframe 정합성** | **INDEPENDENT_RECONFIRM + 1 refinement (SCI-D 별개축)** |

---

## 3. 핵심 발견

1. **L1 진짜 PASS** — 과학 lens가 reframe "L1 보존"을 독립 재확인.
2. **L2/L3는 SCI-A에서 단락** — degenerating이라 SCI-B oracle 부르기 전 이미 falsifiability gate 탈락. oracle은 불필요 확증(load-bearing 아님) = reframe demotion이 oracle 없이도 성립.
3. **SCI-B oracle이 독립적으로 같은 REFUTE** — 두 직교 경로(degenerating + numerology) 같은 결론 = 견고성↑.
4. **SCI-D = reframe에 없던 제3 실패축** — 숫자 맞아도 인과 mechanism 미식별 = association이지 prediction 아님. numerology와 별개. demotion over-determined.
5. **P01이 가장 견고한 REFUTE** — p_corrected=1.0, null-shape 무관 look-elsewhere만으로 kill.
6. **ε은 boundary 종착** — oracle 이미 실행, SIGNAL_WEAK 자체가 verdict. 닫지 않고 정직 라벨.

---

## 4. 함정 자기점검

- **SCI-B null misspecification** (AC2, MEDIUM, OPEN): ICE atomic-set null = ADEQUATE이나 유일 합리적 선택은 아님. Koide/P01은 look-elsewhere dominate라 robust, **mp/mW만 null contestable**. 단 어차피 REFUTE라 verdict 불변.
- **SCI-C reproducible-but-wrong** (확인): ICE 계산 전부 2-run idempotent이나 L2/L3 REFUTE. 재현성 ≠ validity 분리 정확.
- **SCI-D 무한 교란 regress** (AC3, LOW, 회피): L1에 SCI-D 미적용 (정리에 DAG 요구 = category error). 적용했으면 L1 부당 기각될 뻔.
- **L1 S₃ grounding** (AC1, MEDIUM, **RESOLVED 2026-06-01**): `Aut(𝕊)=G₂×S₃` = 확립된 수학 (Aut(O)×S₃; S₃=octonion 아닌 sedenion 고유 대칭). 외부 다중 grounding ([Nature Sci Rep 2021 s41598-021-01814-1](https://www.nature.com/articles/s41598-021-01814-1) + sedenion 표현론). Brown 1967 verbatim 여부 무관 — 수학 content 정확. **L1 PASS 확정.**

---

## 5. reframe 일관성 판정 = INDEPENDENT_RECONFIRM

과학나생문은 workbench reframe(L1 보존 / L2·L3 demoted / mythology untouched)을 **새 결함 없이 독립 재확인** + 1 refinement: SCI-D causal-identification gap = numerology와 별개 실패축 → demotion이 세 번째 직교 사유로 over-determined. mythology layer는 적용범위 밖 (손대지 않음, erase 0).

**OQ1 경험적 확증**: 본 audit이 short-circuit 실행을 실제 사용 (L2/L3가 SCI-A에서 단락) → "직교 위상 + 순차 실행" 양립(사용자 verdict 2026-06-01)이 실전에서 작동함을 보임.

---

---

## 6. AC4 정정 — 첫 audit이 놓친 진짜 문제 (사용자 epistemic challenge 2026-06-01)

> 사용자 challenge: "나생문이 ICE 문제 못 잡았냐?" → **맞음.** 첫 audit은 reframe를 재확인만 했고 새 결함을 못 잡았다.

**실측으로 드러난 진짜 결함** (`challenge-ice-L1-proofs-nonexecutable-cd_embedding-2026-06-01`, HIGH, CONFIRMED_DEFECT):

- L1 증명 스크립트 **13개**(prove_s1/s2/s3/s5/s7 + prove_higgs_ZD + queue_01/02/03/08/09/10/11)가 현재 `ModuleNotFoundError: cd_embedding`으로 **실행 불가**.
- 원인: `cd_embedding.py`(13 importers의 live 공유 의존성)가 commit `930abbb` (PROM16-OQ7 default heuristic)로 `_archive/variants/`로 **over-archive**됨. occam이 variants 존재를 보고 base를 superseded로 오판, reverse-dep 미확인.
- 즉 **"L1 PROGRESSIVE/CONFIRMED/재현가능" verdict는 stale** — 그 결론을 만든 증명들이 실행조차 안 됐다.

**왜 첫 audit이 놓쳤나**: SCI-C(재현성)에 PASS를 줬으나 *실제로 스크립트를 안 돌리고* KG "CONFIRMED" 메타데이터만 읽음 = **reproducibility theater** (SCI-C가 경고하는 바로 그 함정을 SCI-C가 범함). + parent가 critic에 결론을 미리 먹여 confirmation-primed. (`lesson-sci-naesengmoon-scic-theater-self-violation-2026-06-01`)

**Fix (empirically verified)**: `cd_embedding.py` `_archive→top-level` 복원 → 13 스크립트 재실행 **PASS=13 FAIL=0**. L1은 이제 *실제로* 재현가능 (복원 전엔 거짓이었음).

**교훈**: (1) SCI-C verdict는 반드시 실제 실행(exit + 2-run diff)에, KG metadata 금지. (2) occam archive는 import reverse-dep mandatory(live importer>0이면 archive 금지). (3) adversarial audit에 결론 선주입 금지.

---

*KG 영속: `vr-sci-naesengmoon-ice-2026-06-01` (4 USED_LENS + RAISED_CHALLENGE ×4: AC1 RESOLVED / AC2 OPEN / AC3 avoided / **AC4 CONFIRMED_DEFECT→fixed**). Lesson `lesson-sci-naesengmoon-scic-theater-self-violation-2026-06-01`. HAS_VALIDATION → ICE_WORKBENCH_REFRAME_2026-05-18.*
