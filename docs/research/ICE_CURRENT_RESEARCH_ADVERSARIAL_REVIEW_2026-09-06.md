# ICE 현재 연구 적대적 검토와 보완 제안

검토일: 2026-09-06. 기준 commit: `4d5b18997feb6b9cce1def6c53239f0996d83031`.
지위: `SUPPORTING_METHOD` — 기존 결과의 수학·추론 검토와 설계 제안.
새 runner 실행, 신규 계산 결과, core 진전 판정 또는 연구 graph의 상태 변경은 아니다.

## 판단

**최근 세 가지 scoped negative result를 뒤집을 오류는 이번 검토에서 확인하지 못했다.
가장 필요한 보완은 동일한 shortcut을 더 반증하는 일이 아니라, 기존 연속 제약 해를
검증된 국소 source 후보로 발전시키고 그 후보와 frozen midpoint 모델의 관계를 명시하는 것이다.**

현재 첫 병목은 여전히 `open:gate1-original-cycle-signed-global-intersections`다.
같은 모델의 source, measure, boundary/gauge 조건을 갖춘 regulated joint relative class와
완전한 oriented global intersection vector가 없다. 그러나 이것은 모든 연속 해나
Hamilton–Jacobi 자료가 없다는 뜻도, 교차수가 0이라는 뜻도 아니다.

검토 범위는 현재 CPT 경로의 source compatibility, incidence ledger, 9월 4일의
local-lapse/HJ 결과와 관련 Phase 24/39 원문이다. 다른 세 graph 전체, 저장소의 모든
계산, 새로운 물리학 또는 TOE의 타당성을 검증했다는 주장이 아니다. 세 read-only AI
검토를 병행하고 핵심 유도를 대조했으며, 독립 외부 재현이나 사람의 수학 심사를 대신하지 않는다.

## 1. 공격을 견딘 결과와 정확한 한계

| 대상 | 이번에 대조한 결정적 근거 | 유지되는 결론 | 성립하지 않는 확대 해석 |
|---|---|---|---|
| [V0 → Starobinsky BFV 이식](../../cpt_temporal_folded_susy/GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY.md) | `C_Star-C_V0=2π²a³V`; `{p_phi,C_Star}=-2π²a³V'`; 내부 변수에 의존하는 action 차이 | 기존 V0 source를 그대로 동일시할 수 없음 | Starobinsky BFV source 자체의 불가능성 |
| [두 local lapse 후보](../../cpt_temporal_folded_susy/GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST.md) | exact saddle box의 full Hessian 가역성, `∂²_r S=8π²K/T³≠0` | 그 후보에는 선언한 nonzero gauge generator가 없음 | 모든 다른 작용·보조변수·연속극한에서 gauge 복원이 불가능함 |
| [midpoint fixed-time HJ 동일성](../../cpt_temporal_folded_susy/GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT.md) | diagonal residual `R_HJ=π²t²D/4`; exact witness `45π²/1024>0` | 이 witness를 포함하는 영역에서 선언된 정확한 함수 동일성 실패 | 근사법의 무용성, lapse-extremized principal function의 부재 |
| [incidence 원결과](../../cpt_temporal_folded_susy/GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_RESULT.json) | 입력으로 정한 14개 기록: `INTEGER=0`, `UNRESOLVED=12`, `OUT_OF_SCOPE=2` | 이 기록들로 global integer를 채울 자격이 없음 | global intersection vector를 계산해 0을 얻었음 |

HJ 반례는 손유도로도 확인된다. `q0=q1=q`에서 midpoint kinetic 항의 endpoint
미분은 0이고 `p_A=π²t U_A`, `∂t S=2π²U`이다. 따라서
`H_E=p_A G^{AB}p_B/(4π²)-2π²U`를 대입하면 `R_HJ=π²t²D/4`가 남는다.
`a=2`, `exp(-sqrt(2/3)phi)=1/2`에서 `U_a=-3/4`, `U_phi=sqrt(6)`이므로
`D=-U_a²/(6a)+U_phi²/a³=45/64`다. float tolerance에 의존하는 반례가 아니다.

local-lapse 반례의 논리도 유효하다. off-shell identity `S_,A R^A=0`를 미분해
stationary point에 제한하면 `H_AB R^B=0`이다. 기록된 full Hessian이 가역이면
내부 정점까지 함께 움직이는 generator도 그 지점에서 nonzero일 수 없다.
다만 이번 검토에서는 Arb 계산을 재실행하지 않고 기존 enclosure와 구현을 읽었다.

또한 두 셀에 같은 `K,W`가 나타난다는 사실은 오류가 아니다.
[Phase 39 §2](../../cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md)는
같은 양끝 경계와 하나의 내부 정점을 사용한다. 두 증분이 `+(x,q)`, `-(x,q)`이고
midpoint가 같으므로 같은 항이 생긴다. 이는 실제 두 셀 격자의 대칭 축약이며,
정확한 연속 trajectory의 composition을 증명한 것은 아니다.

## 2. 우선 보완할 연구상의 약점

### A. 새로운 source를 만들어도 기존 교차수 자료가 자동으로 따라오지 않는다

새 perfect/improved action `S_new`와 frozen `S_2`는 별도 객체다.
둘이 같은 potential을 쓴다는 사실이나 작은 국소 action 차이만으로 saddle, good end,
sheet, Stokes jump, orientation 또는 integration cycle이 같아지지 않는다.
기존 tail bound와 local sign은 원래 action에서의 유효한 기록으로 보존하되,
새 source의 evidence로 사용하려면 해당 영역의 map/deformation과 필요한 경계 제어를
별도로 보여야 한다. 이것이 현재 source 교체 제안의 가장 큰 미해결 연결이다.

여기서 우선순위는 **작용을 얼마나 비슷하게 썼는가**보다 **어떤 해와 source를 같은
것으로 비교하는가**다. 국소 HJ 인증만 얻어도 global cycle은 여전히 미해결이다.
Picard–Lefschetz 문헌은 적분 cycle을 기술하는 수학적 틀을 제공할 뿐 ICE의 cycle을
선택해 주지 않는다. [Witten, §3](https://arxiv.org/abs/1001.2933).

### B. 정확한 유한 격자 대칭과 제어된 연속 복원을 구별해야 한다

현재 graph의 exact-gauge-preserving source는 정당한 강한 목표다. 그러나 고정된
`m=2`에서 gauge zero mode가 없다는 반례를, 잔차와 극한을 제어하는 모든 근사 연구의
금지 근거로 확대하면 안 된다. [Bahr–Dittrich–Steinhaus §1–2, §4](https://arxiv.org/html/1101.4775)는
naive discretization의 대칭 파괴, perfect action, 연속극한·차수별 복원을 구별한다.
그 논문의 단순한 parametrized mechanics가 ICE의 복원 정리를 제공하지는 않는다.

고정 시간 `W(q0,q1;T)`에는 `∂T W+H_E=0`을, lapse를 extremize한 constrained
principal function에는 endpoint constraint `H_E(q1,∂1 S_C)=0`을 물어야 한다.
후자는 존재와 branch 선택부터 확인해야 한다. approximation을 선택하면 잔차의 정의,
균일한 오차 범위, refinement에 따른 복원 기준을 제출해야 하며, 수치 수렴 몇 점을
continuum theorem으로 쓰면 안 된다. exact 목표를 이 검토가 임의로 바꾸지는 않는다.

### C. 이미 있는 연속 해를 없는 것처럼 다시 찾지 말아야 한다

[Phase 24 §1–2](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md)는
이미 같은 `M_P=M=1` Starobinsky Euclidean action에서
`phi_center=1`, `T0=0.7`을 공급한 기준 해와 constrained shooting 문제를 기록한다.
경계 변화 때 초기 속도 둘과 proper length를 함께 풀며, endpoint gradient와
rank-one mixed Hessian도 수치적으로 조사했다.

이 기록은 **새 해의 seed와 convention 확인에 유용한 supporting benchmark**다.
물리적 초기 상태를 선택하지 않으며, 임의 경계 근방의 엄밀한 존재·유일성 인증도 아니다.
단지 같은 runner를 다시 실행하거나 rank-one 수치를 더 정밀하게 만드는 일은 현재
부족한 객체를 바꾸지 않는다. 새 작업을 한다면 validated continuum endpoint map처럼
현재 기록에 없는 인증을 출력해야 한다.

### D. 검사 개수와 증거의 종류를 혼동하지 말아야 한다

source audit의 일부 `MISMATCH/MISSING` 항목은 고정한 기존 기록에 대한 분류이고,
incidence ledger의 [classifier](../../cpt_temporal_folded_susy/gate1_original_cycle_intersection_incidence_ledger.py)는
manifest의 prerequisite Boolean을 읽는다. hash와 독립 result-reader는 무결성·분류
일관성을 점검하지만 누락된 saddle을 발견하거나 물리적 전제를 독립 검증하지 않는다.
이는 현재 fail-closed 결론을 무효화하지 않는다.

따라서 연구 진행은 `PASS` 총수 대신 **새로 확보한 수학적 객체와 아직 없는 객체**로
보고하는 편이 정확하다. ledger 전체를 다시 포장하는 작업은 현재 과학 병목보다
우선하지 않는다. 다음 실질적 증거를 재사용할 때 그 증거의 정확한 source locator와
유도 경로를 대조하면 된다.

## 3. 다음 질문 하나: 기존 continuum seed의 constrained endpoint map 인증

**제안일 뿐 실행하거나 존재를 주장하지 않는다.**

같은 날 후속 [인터넷 1차 문헌 보완](ICE_CONTINUUM_CERTIFICATE_LITERATURE_SUPPLEMENT_2026-09-06.md)에서
CAPD의 validated C1 flow와 Rump의 inclusion 정리에 맞춰 미지의 `T` 미분 및 인증식을
구체화했다. Phase 24 중앙의 turning point에서는 좌표만의 시계가 횡단성을 잃는다는 점도
추가했다. 아래 BVP 인증은 그 시계나 original relative cycle을 구성하는 작업이 아니다.

질문: Phase 24의 continuum seed에 대응하는, 아래 정확한 경계값을 잇는 constrained
shooting 문제는 사전에 정한 유한 box 안에서 유일한 regular zero를 가지는가?

```text
q_- = q_+ = (3.5668031935672753, 1.0185809464006637)
y = (v_a,-, v_phi,-, T)
F(y) = (a(T;y)-a_+, phi(T;y)-phi_+, C(q_-,v_-))
C = v_a^2 - 1 - a^2*(v_phi^2/2 - V(phi))/3
```

소수 경계값은 정확한 입력으로 고정한다. Phase 24가 수치 적분으로 생성했던 경계의
정확한 연속값이라고 가정하지 않는다. 기록된
`y≈(0.09984512855,-0.10663777161,0.7)`은 탐색 seed일 뿐 인증 중심이나 정답이 아니다.
proper-time gauge에서 `T>0`을 쓰고, 전 구간 `a>0`인 국소 실수 branch를 대상으로 한다.
이 선택은 물리적 lapse contour 선택이 아니다.

- **출력 하나:** `F`의 validated flow와 derivative enclosure에 근거한 유한 box의
  존재·유일성 certificate, 또는 `INCONCLUSIVE`. 인증 실패 자체는 부존재가 아니다.
  실제 exclusion을 보인 경우에만 그 box의 `NO_ROOT`를 말할 수 있다.
- **주된 실패원인:** `solver`. control은 (1) ODE/variational flow의 균일 enclosure와
  `a=0` 회피, (2) interval Newton/Krawczyk inclusion 및 endpoint-map regularity,
  (3) 독립적으로 유도한 full Euler–Lagrange 식·constraint 일관성의 세 개로 제한한다.
- **중요한 구현 조건:** `C=0`에서만 유효한 축약 ODE를 off-shell shooting derivative에
  쓰지 않는다. Phase 24의 full scale equation과 constraint-reduced 식은
  `-C/(2a)`만큼 다르므로 derivative enclosure가 달라진다.
  full flow의 보존 에너지는 `H_E=-6π²a C`이므로, `a>0`과 `C(0)=0`에서
  전 구간의 `C=0`이 따른다는 propagation identity도 certificate에 명시한다.
- **비주장:** 이 certificate만으로 BFV source, exact cell composition, gauge quotient의
  global uniqueness, physical cycle, 전체 saddle census 또는 G1 해소를 주장하지 않는다.

이 출력은 `open:gate1-starobinsky-exact-gauge-preserving-element-source`의
**named continuum branch/regular endpoint-map 전제**에만 들어갈 후보이다.
그 다음 G1 relative class/intersections → G2 CFU → G3 Pfaffian → G4 positive product/closure
→ G5 invariant interacting effect → full-theory/empirical review라는 의존 경로는 그대로다.
source/measure/old-kernel comparison을 만들기 전까지 이 인증은 supporting prerequisite이며,
core-label은 해당 missing object와 evidence edge의 별도 검토 없이는 부여하지 않는다.

일반 bounded runtime 내에서 validated ODE가 가능한지도 설계 때 확인해야 한다.
불가능하면 `INCONCLUSIVE`로 종료하거나 실행 전에 범위를 재검토한다. 이 제안은
Phase 51–56 reconciliation, historical replay, 자동 cutoff ladder를 재개하지 않는다.
성공하더라도 새 작용·composition·BFV 계산을 자동 생성하지 않는다.

## 4. 이번 검토의 실제 확인 기록

- `git status --short`: 시작 때 `output/ice-core-bridge-reuse-2026-08-31/`만 untracked.
  해당 기존 경로는 읽기·수정·stage 대상에서 제외했다.
- `./ice status --json`: `BOUNDED_SCIENCE_OPEN_KILLED_RECONCILIATION_CLOSED`,
  Gate 1 `OPEN_PARTIAL_PROGRESS`, global promotion `PROHIBITED`.
- `./ice ontology guide --path choice-invariance-cross-domain-audit`: 정상 조회.
- 아래 planner 질의: `CURRENT_BLOCKER_CANDIDATE`, checkpoint
  `research-agent:b1cfd9c72d3da4d88fda`. navigation 결과이며 승인·새 evidence가 아니다.
- `./ice harness check`: **466/466 hashes verified, errors 0, warnings 75**.
  경고 전체를 이번에 해소하거나 과학적 검증으로 해석하지 않았다.
- 세 최신 raw result의 SHA-256을 Node로 다시 계산하여 각각 인접 보고서와 일치함을 확인.
  `VALID_RUN`과 check count는 기존 raw record에서 읽은 값이며 이번 재실행 결과가 아니다.
- 문서의 상대 파일 링크 7개가 모두 존재함을 확인했다. 후속 read-only 수학 검토에서
  제안한 3변수 residual과 off-shell derivative 조건의 오류는 발견되지 않았다.

```bash
./ice agent plan 'open:gate1-original-cycle-signed-global-intersections: audit missing source-defined regulated joint relative class and compatible Starobinsky m2 BFV source. Output: explicit source-compatibility obstruction or compatible candidate, no global vector. Path: G1 cycle/intersections -> G2 CFU -> G3 Pfaffian -> G4 closure/positive product -> G5 order -> full-theory/empirical review -> TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW. Risk: gauge; check exact HJ identity.' --graph cpt --json
```

확인 중 실패도 남긴다. 첫 planner 질의는 500자 제한을 넘어 거절됐고 위 질의로
수정했다. 문서가 안내하는 `./ice ontology guide --graph cpt --path gate1-typed-object-handoff`는
`ONTOLOGY_READING_PATH_NOT_FOUND`로 실패해 canonical open node와 원문을 직접 읽었다.
incidence ledger의 같은 이름 `.md`는 존재하지 않아 raw JSON·runner·graph를 읽었다.
이 navigation 문제를 연구 결과의 반증으로 세지 않았다.

문헌은 2026-09-06 원문 페이지를 조회했다. 추가 방법론 대조는
[Dittrich–Höhn, §3.5와 §5.3](https://arxiv.org/html/1303.4294)의 effective action과
constraint/gauge 구분이다. 이 보고서의 후속 제안은 해당 논문의 ICE 적용 정리가 아니다.

이 문서는 기존 claim/evidence/scope 판정을 바꾸지 않는 검토 메모이므로 ontology나
repro manifest에 새 항목을 추가하지 않는다. 사용자 원문 narrative는 그대로 보존한다.
