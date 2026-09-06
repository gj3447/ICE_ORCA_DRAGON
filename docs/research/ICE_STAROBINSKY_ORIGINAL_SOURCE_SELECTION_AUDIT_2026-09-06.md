# Starobinsky original source: CPT 접합 입력의 원문 감사

2026-09-06 · **SUPPORTING_METHOD / SOURCE_AUDIT**.

## 질문과 결론

> 기존 CPT fold와 Starobinsky source 기록이 두 history의 접합 작용과
> 원래 joint integration cycle을 실제로 정하는가?

확인한 기록에서의 판정은 **`SOURCE_UNDERDETERMINED_IN_INSPECTED_RECORDS`**다.
고정 경계값을 가진 유한 작용과 일부 momentum Gaussian ray는 있다. 같은 모델의
접합 작용·생성관계와 완성된 joint relative class는 없다. 이는 아래에서 확인한
문서들의 명시적인 미완료 진술에 근거하며, 존재할 수 있는 모든 외부 원문의 부재를
주장하는 것이 아니다.

따라서 CPT 접합이 기존 scalar momentum mismatch를 보상한다는 결론도, 보상할 수
없다는 결론도 내리지 않는다. [실수 compact-closure 반증](ICE_STAROBINSKY_REAL_COMPACT_CLOSURE_OBSTRUCTION_2026-09-06.md)은
경계항 없는 smooth real completion만 배제한다. 미정인 CPT source를 그 특수한
completion과 동일시하지 않는다.

## 선언된 객체와 빠진 연결

| 확인한 객체 | 실제로 고정한 것 | 같은 Starobinsky source에 주지 않는 것 |
| --- | --- | --- |
| frozen canonical \(I_2\) | 두 동일한 Dirichlet endpoint, 유한 two-cell action, momentum orientation | 두 continuum history의 CPT 접합 작용과 original joint cycle |
| centered Gaussian rays | 선언한 branch의 유한 momentum pushforward | scale/scalar/lapse의 전체 cycle과 absolute BFV measure |
| \(P_{\rm fold}\) | doubled real projector witness | action의 불변성, bosonic junction equation, common physical domain |
| free Wess–Zumino seam map | 다른 모델의 finite canonical Cauchy-data map | Starobinsky \((a,\phi;p_a,p_\phi)\)에 대한 생성관계 |
| 국소 constrained \(S_C\) | 선언한 branch의 principal action과 국소 composition | quantum kernel·seam state·전역 integration class |

첫 두 행의 원문은 [bosonic canonical-source pushforward §1–2, §7](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md)다.
그 문서는 \((a_0,\phi_0)=(a_2,\phi_2)=(a_b,\phi_b)\)와
\((a_1,\phi_1)=(a_b+x,\phi_b+q)\)를 둔 \(I_2\)를 고정한다.
momentum Gaussian을 계산하는 처방과 physical cycle의 선택을 분리하고, 후자는
미해결로 남긴다. \(I_2\)의 fixed-endpoint 변분을 trace의 자유 endpoint 변분이나
별도 seam functional \(S_\Sigma\)로 바꾸는 근거는 그 기록에 없다.

마지막 행의 [principal-branch 보고서](../../cpt_temporal_folded_susy/STAROBINSKY_PRINCIPAL_BRANCH.md)는
국소 classical 객체를 별도로 구성했다. frozen midpoint와의 값·미분 차이도 기록하므로,
이 \(S_C\)를 frozen \(I_2\)와 같은 exact quantum source라고 부를 수 없다.

## CPT 관련 원문이 명시한 한계

[Phase 17의 temporal-seam 절](../../cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md)은
\(J_{\rm fold}=K_s\otimes\gamma_0\), \(P_{\rm fold}=(1+J_{\rm fold})/2\)를
reality/projector witness로 제시한다. 같은 문단이 action, charge, positivity,
junction condition을 검증하지 않았다고 명시한다.

[Phase 18 §1](../../cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md)은
flat \(3+1\) free equal-mass Wess–Zumino mode의 순간적인 유한 quadratic map을
다룬다. 완성된 doubled sewing action도 아니라고 적는다. 이 map을 현재 scalar
momentum jump에 적용하려면 새 모델 대응과 접합 데이터를 별도로 정의해야 한다.

[Phase 21 §3–4](../../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md)는
actual three-form seam action에서 coupling·charge/tension·boundary ensemble을
유도하는 일이 남았다고 한다. [Phase 28의 completion route](../../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md)도
BFV-reduced seam state에서 double-three-form SUGRA로 가는 연결을 design gate로 둔다.
그 방향 표시를 이미 도출한 Starobinsky 접합식으로 읽지 않는다.

[Phase 31](../../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md)의
endpoint-vanishing ghosts는 fixed-\(q\) kernel용 조건이다. finite-cutoff BFV
quadratic diagnostic이 absolute quantum seam weight를 준다는 주장은 없다.
endpoint \(p_a\) clock을 도입하면 polarization과 boundary Legendre term이 바뀐다는
동일 문서의 구별도 유지한다.

[CPT README의 Foundational construction 항목](../../cpt_temporal_folded_susy/README.md)은
bulk-plus-seam action을 실제로 변분하는 일을 미래 작업으로 적는다.
[geometry/CPT/SUSY 직관 지도](../../research/intuition/ICE_GEOMETRY_CPT_SUSY_INTUITION_MAP_2026-09-03.md#the-only-honest-bridge-between-the-lanes)의
\(S_{\rm pair}\ ?=S_{\rm SUGRA}[\Phi_+]+S_{\rm SUGRA}[\Phi_-]+S_\Sigma\) 역시
물음표를 명시하고, variational domain과 constraint algebra가 없다고 설명한다.

## 기존 운동량 차이에 적용하는 정확한 질문

실수 equal-Dirichlet continuum branch와 \(\phi_b>0\)에서 이미 얻은 것은

\[
 \Delta p_\phi=p_{\phi,R}-p_{\phi,L}
 =\frac{2\pi^2}{\phi_b}[a^3\phi\phi']_L^R>0
\]

다. CPT라는 이름만으로 이 항의 부호를 뒤집거나 소거할 수는 없다. 필요한 것은
양측 polarization, orientation/conjugation의 canonical one-form 작용, 실제
boundary functional 또는 canonical generating relation이다. 추가 seam field가
있다면 그 변분도 포함해야 한다. lapse/ghost 경계조건과 measure는 그 relation에
맞아야 한다. 이 입력이 주어진 뒤에야 signed scalar junction 식과 \(\Delta p_\phi\)를
비교할 수 있다.

이것은 새 전역 연구 계약이나 승인 목록이 아니라, 현재 접합식을 쓸 수 없는 이유다.
하나의 local junction이 성립해도 모든 good end·sheet·Stokes·orientation을 포함한
G1 joint relative class를 대신하지 않는다.

## 외부 문헌에서 실제로 제공하는 대안

[Bramberger–Hertog–Lehners–Vreys, arXiv:1701.05399v1](https://arxiv.org/html/1701.05399v1)의
§II eq. (6)은 closed Einstein-scalar 모델의 두 경계 transition amplitude를 쓴다.
§III eqs. (9)–(10)은 복소 bounce의 대칭면에 \(a'=\phi'=0\)을 두고, Hamiltonian
constraint로 bounce scale을 정한다. §IV.1은 켤레 saddle로 얻는 시간 반전 history와
실제 transition을 구별한다. CPT 켤레를 취하는 연산 자체가 접합 작용은 아니다.

이 논문의 inflationary 수치 예는 quadratic potential이고, 경계는 WKB classicality를
만족하는 영역에 둔다. 현재 Starobinsky potential과 finite interior endpoint에 대해
같은 saddle 선택이나 고전성 조건을 증명하지 않는다. Appendix A의 경로 비교도
선택한 saddle의 **복소 시간 평면 경로**를 다룬다. 이를 모든 off-shell lapse·field·ghost를
포함하는 ICE의 **원래 functional integration cycle**로 동일시하지 않는다.
이는 모델 대응과 source 선택을 명시해 검토할 수 있는 방법 선행례다.

[Boyle–Finn–Turok의 CPT-symmetric universe](https://arxiv.org/abs/1803.08928)는
Big Bang 양쪽의 CPT 반사와 preferred vacuum을 제안한다. 그 이름만으로 이 저장소의
closed Starobinsky interior seam functional을 제공한다고 추론하지 않는다.

## 사용자 원문과 모델링 선택

이번에 sibling checkout의 [나는야 ice orca dragon](../../../MIND/metahumotonic/%EB%82%98%EB%8A%94%EC%95%BC_ice_orca_dragon.md)을
직접 찾고 읽었다. 짧은 narrative 목록과 “그냥 모든것은 하이퍼그래프”라는 문장은
있지만, 위 action·boundary state·lapse contour·junction 식은 없다.
원문이 없다는 뜻이 아니다. 이 원문에서 구체적인 물리 처방을 소급해 추론할 수 없다는
뜻이다. 원문과 sibling checkout은 수정하지 않았다.

새 boundary/source 처방을 **선언한 모델링 가설**로 연구하는 것은 가능하다. 다만
그 선택을 기존 원문에서 유도된 original source라고 쓰면 안 된다. 별도 원문이 있다면
그 자료와 먼저 대조하고, 없다면 candidate의 추가 가정과 기존 benchmark와의 차이를
명시해야 한다. 이 감사는 어느 새 candidate도 이미 채택하거나 검증했다고 주장하지 않는다.

## 검토 기록과 지위

- 사전 planner는 `CURRENT_BLOCKER_CANDIDATE`였다. 실제 결과는 source 입력 감사이며
  G1 class/vector의 구성·해소가 아니므로 **supporting**으로 둔다.
- `./ice harness check`: 473/473 hash, 오류 0. graph context와 실제 문서를 함께 읽었다.
- 문헌 검색: `./ice literature search "CPT cosmology scalar seam two boundary transition quantum singularities" --json`,
  `2026-09-06T14:40:38.769Z`. 검색 metadata가 아니라 위 primary text를 판정 근거로 썼다.
- 주된 위험은 `inference`: projector/action, fixed-boundary/trace, time-contour/joint-cycle의
  세 혼동을 독립 읽기 검토로 대조했다. 새 numerical runner나 관측 분석은 실행하지 않았다.

기존 scoped 결과와 G1의 미해결 상태는 유지된다. 이번 감사는 새 물리 발견이나 TOE의
성립 근거가 아니며, canonical evidence edge·repro manifest·자동 후속 작업을 만들지 않는다.
