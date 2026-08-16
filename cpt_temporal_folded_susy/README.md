# CPT × Temporal-Folded SUSY — ICE ORCA DRAGON 물리 연구 둥지

> **정책 (사용자 지시 2026-08-11)**: 물리학 연구는 ICE_ORCA_DRAGON(사도 #2, 물리학
> 대통합 — 자연법칙 축) 기반으로 간다. 이 디렉터리가 CPT×TFSUSY 프로그램의 ICE측
> 정본 둥지이며, Phase 12+ 신규 물리 산출물은 여기서 태어난다.

## 역사적 코퍼스

Phase 1–10 전체(102+ 파일: 검증기·manifest·LakatoTree receipt 포함)는
`SYMPOSIUM/FINDINGS/cpt-temporal-folded-susy-2026-08-09/`에 있다. Phase 7/8
manifest·receipt가 그 경로들을 sha-바인딩하므로 **이동하지 않는다** (Longinus
바인딩 보존). 이 둥지는 Phase 11부터의 정본 + 역사 코퍼스로의 포인터다.

## 수록

| 파일 | 내용 |
|---|---|
| `phase11_collar_admissibility.py` | Phase 11 v2 유도·검증 실행체 (단일 명령: `uv run --with sympy python3 phase11_collar_admissibility.py` → exit 0) |
| `PHASE11_COLLAR_ADMISSIBILITY.md` | Phase 11 v2 보고서 — E152–E156 (collar 허용/금지 분류, dilation 부활, 종-혼합 회전-형 강제, shear 조건부 채널) |
| `PHASE12_RESEARCH_CONTRACT.json` | Phase 12 T2 판정 계약 (`POST_HOC`; P12A boundary twist / P12B rigid \(N=1\) witness / P12C local-SUGRA gate 분리) |
| `phase12_boundary_twist_interface.py` | Phase 12 exact 실행체 — collar canonical-removability, rigid BPS wall, scalar formal factorization, multiplet 공통 flavor frame, conditional endpoint covariance 및 의미 변형 검사 |
| `PHASE12_BOUNDARY_TWIST_INTERFACE.md` | Phase 12 보고서 — E157–E162. 보손 collar는 bulk SUSY가 아니며, whole-multiplet rigid \(N=1\) spatial interface witness는 구성; local SUGRA/시간 fold는 OPEN |
| `PHASE13A_RESEARCH_CONTRACT.json` | Phase 13A T2 사전등록 계약 — Lorentzian local-SUGRA branch-\(Q\)의 formal symbol, positive-kernel, closure, physical-domain gate를 실행 전 고정 |
| `phase13a_lorentzian_branch_supercharge.py` | Phase 13A exact 실행체 — Moniz principal-symbol control, finite positive-kernel obstruction, CAR closure countercontrol 및 의미 변형 검사 |
| `PHASE13A_ADVERSARIAL_ERRATUM.json` | 최초 실행의 과도한 core 판정을 원 계약을 수정하지 않고 정정한 `POST_HOC_CORRECTED` 적대검토 기록 |
| `PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md` | Phase 13A 보고서 — E163–E166. 두 algebraic 지름길은 닫혔고 literal branch=superpartner core는 `INCONCLUSIVE/UNCONSTRUCTED` |
| `PHASE14A_RESEARCH_CONTRACT.json` | Phase 14A T2 사전등록 계약 — compact chiral-clock route의 goldstino residual, RT spatial boundary, proper-bulk quotient gate를 결과 전에 고정 |
| `PHASE14A_SOURCE_PACKET.json` | Kallosh·Henneaux·Martínez-Pérez–Ramírez source version/hash/scope와 정규화 bridge의 frozen packet |
| `PHASE14A_CHARGE_LEDGER.json` | 실행 전 동결한 immutable candidate ledger; observed status는 별도 result receipt에 기록 |
| `phase14a_chiral_clock_charge_first.py` | Phase 14A exact 실행체 — bosonic clock, goldstino residual, compact topology, formal quotient와 verdict precedence 검사 |
| `PHASE14A_RUN_RESULT.json` | 최초 실행 및 두 independent replay, observed gates, T2 classification을 담은 post-run receipt |
| `PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md` | Phase 14A 보고서 — E167–E170. G2/G3은 닫혔지만 canonical bridge 미구성으로 selected target은 `INCONCLUSIVE/UNCONSTRUCTED` |
| `PHASE15A_RESEARCH_CONTRACT.json` / `PHASE15A_SOURCE_PACKET.json` / `PHASE15A_CONVENTION_MAP.json` / `PHASE15A_MODE_COMPENSATOR_LEDGER.json` | Phase 15A off-shell tangency 입력. 완성 executable commit 전 K1 sign을 관측해 cycle은 실행하지 않고 sequence-invalid로 봉인 |
| `PHASE15A_SEQUENCE_BREACH.json` | Phase 15A의 `INVALID / INCONCLUSIVE / PREREG_OR_PROVENANCE_INVALID` 기록과 K2 방화벽 |
| `PHASE15R_RESEARCH_CONTRACT.json` / `PHASE15R_SOURCE_CONVENTION_PACKET.json` | Known prior를 공개한 fresh T2 reproduction contract와 Hohl/Kallosh 두-source census |
| `phase15r_parent_sign_reproduction.py` | Phase 15R source-native curvature/action/scalar/Legendre/inertia 및 full-offshell coverage 실행체 |
| `PHASE15R_RUN_RESULT.json` / `PHASE15R_REPLAY_RECEIPT.json` | 최초 실행과 독립 replay 영수증. 47 PASS, 17 mutant categories / 18 fixtures, 4 guards |
| `PHASE15R_PARENT_SIGN_REPAIR.md` | Phase 15R 보고서 — E171–E176. Kallosh는 bosonic parent only, frozen census에는 full same-source parent가 없음 |

SYMPOSIUM측 원본 커밋: `c1f10f6` (2026-08-11, 5-반박자 적대감사 경유 v2).

## 현재 경계 (Phase 15R)

- Phase 11 strong 허용 class와 unrestricted-lapse rescaling을 포함한 weak dilation은 명시한
  가정 아래 open-interval bulk에서 canonical frame change로 제거되며 endpoint
  twist/polarization/boundary generator로 이동한다.
- 정칙 4D rigid \(N=1\) spatial BPS wall에서 scalar/chiralino에 같은 kinematic internal-flavor
  connection이 생기고 scalar differential expressions가 formal factorize되는 witness를 구성했다.
  이것은 physical endpoint detector, pre-Big-Bang branch나 local SUGRA completion의 증명이 아니다.
- Phase 13A의 generic CAR countercontrol은 closure만으로 branch exchange가 따라오지 않음을
  보였고, 양의 finite square-root toy의 physical-kernel map도 정확히 0이었다.
- gauge-independent relational branch projector, 공통 physical domain/inner product, local gauge
  constraint와 구별되는 nonzero \(Q_{\rm phys}\)의 결합은 아직 `UNCONSTRUCTED`다. 따라서 literal
  core는 증명·보편 반증 어느 쪽도 아니며 `INCONCLUSIVE`다.
- Phase 14A는 \(C_B=-p_X^2+p_T^2+p_Y^2\), 양·음 \(p_T\ne0\) clock patch와
  \(\alpha=(p_T^2+p_Y^2)/(2V_0^2a^6)>0\)를 exact하게 재현했다. 그 결과
  goldstino-gauge residual kernel은 0이다.
- Smooth compact \(T^3\)에서 RT spatial-boundary channel은
  `NOT_APPLICABLE_IN_THIS_ROUTE`다. 그러나 differentiable graded matter-SUGRA Dirac generator는
  유도되지 않아 template completeness와 equivalence-class deduplication은 보류됐고 selected
  charge target은 `INCONCLUSIVE_UNCONSTRUCTED`다.
- Phase 15A는 complete executable commit 전에 Hohl parent-sign 결과가 관측되어
  `INVALID / INCONCLUSIVE / PREREG_OR_PROVENANCE_INVALID`로 봉인됐다. 그 cycle의 K2 tangency와
  projector는 평가하지 않았다.
- Fresh Phase 15R은 Hohl/Kallosh source를 섞지 않고 재현했다. Hohl은 first-order kinetic
  inertia \((0,0,3)\)으로 bosonic sign gate를 통과하지 못하고, Kallosh는 \((1,0,2)\)를
  통과하지만 target old-minimal auxiliary/transform coverage가 없다.
- 따라서 frozen two-source census에서는 bosonic target이 `VALID/SUPPORTS`, full same-source
  target이 `VALID/CONTRADICTS/NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS`다. 이는 문헌 전체 no-go나
  Temporal-Folded SUSY core 판정이 아니다.

## 다음 계산

Phase 14A의 residual·boundary subgates는 닫혔지만 proper-bulk canonical bridge가 열리지 않았고,
Phase 15R은 기존 두 source 중 full same-source parent가 없음을 확인했다.

1. Lorentzian Einstein/scalar 부호, auxiliary-retaining action, local transformations를 **한 primary
   source 안에서** 주는 Binetruy–Girardi–Grimm parent를 직접 축약하고 부호·Hessian을 계산한다.
2. 같은 source가 실제로 필요한 성분을 주면 Bianchi-I homogeneous SUSY tangency를 계산한다.
   실패하거나 식이 빠지면 그 사실을 즉시 결과로 남기고 다른 source를 검토한다.
3. P12B full Green function/S-matrix는 별도 **spatial-interface auxiliary** 연구로만 수행할 수
   있으며, canonical charge gate 전에는 cosmological branch 주장에 대한 evidence weight가 0이다.
4. 이산/anomaly-fixed wall과 higher-derivative bounce는 auxiliary response가 non-null일 때만
   별도 계산한다. spatial wall의 시간 analytic continuation은 증거로 쓰지 않는다.
