# 관측가능량·선택한 내적·상보적 경계 접합의 세 단계 판별

2026-09-07 · SUPPORTING_METHOD · SCOPED.

**실제 H의 1차 국소 강한 관측가능량을 분류했고, 이 범위에서는 현재의 해나 내적이
선택되지 않는다는 결과를 얻었다.** 한편 같은 Neumann 편극의 zero pairing을
Neumann–Dirichlet 사이의 비퇴화 보손 pairing으로 보완했다. 이것은 전체 BFV/CPT
접합의 완성이 아니다.

| 요청한 단계 | 실제 수행한 결과 | 남는 구별 |
|---|---|---|
| 제약·경계조건과 양립하는 관측가능량 | 실제 unscaled Weyl H와 p_N의 smooth 1차 국소 strong commutant는 cI+d p_N로 완전히 분류됨. 이들과 formal adjoints는 repaired Φ를 보존함 | 고차·weak/BRST·관계론적·비국소 관측가능량 전체를 분류한 것은 아님 |
| ker T와 내적 보존 | 이 대수와 C[H,p_N]는 모든 T_g에 동일한 scalar로 작용. 선택한 kernel을 보존하고 formal star와 내적이 호환됨. 실제 norm 보존은 scalar의 절댓값이 1일 때뿐 | seed·정규화를 선택하지 못하며, 비가환 seed label 작용은 실제 시험공간 관측가능량으로 lift되지 않음 |
| 살아남는 상태의 접합 | 실제 H의 N 및 D Cauchy 해족을 써서 비퇴화한 N×D bosonic Green pairing 구성 | oriented ghosts·양자 CPT 교환사상·실제 BFV kernel·residual BV 및 mQME/pushforward·original cycle은 OPEN |

질문은 위 관측가능량–rank-one 선택–seam 후보의 조합이 어디까지 성립하는가다.
출력은 좁은 strong class의 비선택 결과와 상보적 bosonic pairing이다.
G1의 원래 적분 class나 signed intersection vector를 주지 않으므로 core TOE
진전으로 세지 않는다. 구체적 scope와 전 증명은
[유도문](STAROBINSKY_OBSERVABLE_SELECTION_DERIVATION.md)에 있다.

## 1. 가장 단순한 실제 관측가능량은 선택 원리를 제공하지 않는다

같은 Weyl ordering, flat density, hbar=1과 finite box를 유지한다.
Smooth coefficient의 1차 미분연산자 O에 대해 [H,O]=[p_N,O]=0을 요구했다.
이 항등식은 on-shell에서만이 아니라 시험함수 위에서 성립해야 한다.
Φ가 모든 interior compact tests를 포함하므로 미분연산자의 계수 비교가 가능하다.

원래 H를 r=(4π√6/3)a^(3/2), θ=√(3/8)φ로 바꾸고 similarity를 적용하면
flat Lorentzian wedge의 wave operator와

\[
Q=-A r^{2/3}+\frac9{64}r^2(1-e^{-4\theta/3})^2-\frac2{9r^2},\quad A>0
\]

를 얻는다. 2차 commutator 계수는 Killing 장을 제한하고, 실제 Q를 보존하라는
조건은 남은 두 translation과 boost를 모두 제거한다. 이는 finite open radial
interval의 서로 다른 거듭제곱 계수에 관한 증명이다. a→0 극한이나 수치 표본으로
완전성을 주장하지 않았다. Scaled constraint의 symmetry를 가져오지도 않았다.

따라서 O=cI+d p_N뿐이다. H,p_N이 Φ를 보존하고 그 위에서 formally symmetric이므로
이 대수와 formal star도 Φ에서 잘 정의된다. 더 나아가 constraint-generated
polynomial 대수는

\[
T_g[P(H,p_N)u]=P(0,0)T_g[u]
\]

로 작용한다. 모든 seed가 똑같이 보이므로 이 대수로는 어느 T_g나 양의 정규화를
택해야 하는지 결정할 수 없다. Formal symmetry와 closed self-adjoint realization은
구별한다. [RAQ의 domain·observable·rigging 조건](https://arxiv.org/html/gr-qc/9812024).

## 2. 비영 1차원 선택의 판별식을 Lean으로 고정했다

실제 kernel 조건은

\[
O(\ker T)\subseteq\ker T
\quad\Longleftrightarrow\quad
T\circ O=\lambda_O T,\qquad T\ne0.
\]

[ObservableSelection.lean](../formal/cpt_sewing/CptSewing/ObservableSelection.lean)은
이 동치, kernel-failure witness, 공통 고유함수에 작용한 commutator의 소거,
비영 scalar commutator와 rank-one의 충돌, constraint 고유값 0 및 form covariance를
검증한다. 추상 O를 우리 모형의 물리 관측가능량이라고 선언하지 않는다.

여기서 내적의 수반 관계와 등거리 보존은 구별해야 한다. O=cI+d p_N는 제약 몫에서
c로 작용하므로

\[
F_T(Ou,Ov)=|c|^2F_T(u,v),\qquad
F_T(Ou,v)=F_T(u,O^*v).
\]

두 번째 formal-star 호환성은 모든 c,d에 대해 성립하지만, 첫 번째 식의 실제
내적·norm 보존은 |c|=1일 때뿐이다. 이는 Lean의 두 slot covariance 식에서
바로 따른다. 어느 조건도 seed나 양의 정규화를 선택하지 않는다.

예컨대 seed Qg=φg, Pg=−ig'는 비가환이지만, 이를 Cauchy 해의 label에서 시험공간
연산자로 옮길 lift는 아직 없다. 단순 φ 곱셈과 −i∂φ는 실제 H와 교환하지 않는다.
만약 T_g(O_Q u)=T_(Qg)(u)를 요구한다면, 선택한 bump g₀에서 Qg₀가 g₀의 배수가
아니므로 기존 injectivity와 위 판별식으로 ker T_g₀ 보존이 실패한다.
이는 조건부로 그 특정 rank-one 선택을 배제하며 더 큰 해공간을 배제하지 않는다.

## 3. 상보적인 보손 접합까지 구성했다

Neumann 쪽은 s_g(2)=g, ∂a s_g(2)=0이고, 반대편에 t_h(2)=0,
∂a t_h(2)=h인 Dirichlet Cauchy 해를 구성했다. 두 쪽 모두 실제 H 및 p_N 제약을
만족한다. D 쪽에는 모든 H^k p_N^m 값 trace가 0인 repaired Φ_D를 따로 선언하여,
그 쌍대 제약 소거도 Green 식으로 확인했다. 존재 논증은 같은 열린 R² extension의
[Cauchy 정리](https://arxiv.org/pdf/0806.1036v1)를 사용한다.

명시한 Green 순서 ∫[(Hs)t−s(Ht)]와 coordinate ∂a convention에서

\[
W_{N,D}(s_g,t_h)=-\frac1{48\pi^2}\int_{\mathbb R}g(\phi)h(\phi)\,d\phi.
\]

이 bilinear pairing은 양쪽에서 비퇴화다. 반면 N×N과 D×D는 각각 0이다.
[SeamPolarization.lean](../formal/cpt_sewing/CptSewing/SeamPolarization.lean)은
finite boundary jets의 이 소거/비소거 계수와 K covariance를 검증한다.
해의 존재, 적분의 비퇴화 및 full-R current conservation은 유도문의 해석적 증명이다.
유한 φ-box에서 lateral flux가 사라진다고 가정하지 않았다.

여기서 W는 **복소 bilinear bosonic pairing**이다. 양의 물리 내적과 동일시하지
않는다. K=conjugation은 각 편극을 보존하므로 비영 N 해를 D 쪽으로 보내지 못한다.
이 상보적 pairing을 이용하려면 실제 CPT와 편극 변환을 어떻게 결합할지 별도의
근거가 필요하다. 이 결과는 CPT가 반드시 N과 D를 교환해야 한다는 보편적 주장이 아니다.
다른 편극이나 접합 route는 이 계산으로 배제되지 않는다.

CMR의 전체 접합은 경계 BFV 작용과 양립하는 pairing에 더해 residual BV pushforward와
mQME를 요구한다. 아직 그 객체를 구성하지 않았으며, on-shell에서 제약이 0인 것만으로
off-shell graded Ward identity를 통과했다고 기록하지 않는다.
[CMR §2.4.4, 식 (2.36), Remark 2.37](https://arxiv.org/html/1507.01221).

따라서 다음 판단은 더 구체적이다. **비자명한 관측가능량의 실제 lift와 그 작용으로
닫힌 해공간을 정한 뒤, 상보적 보손 pairing을 ghost·orientation·residual BV 구조와
연결할 수 있는가?** 현재의 scalar 대수만으로 선택된 물리 상태라고 승격하지 않는다.

## 실행 기록과 검증 범위

- 명령: `./ice run starobinsky_observable_selection`.
- 최종 status: `SCOPED_FIRST_ORDER_OBSERVABLE_NONSELECTION_AND_COMPLEMENTARY_BOSONIC_PAIRING`.
- 실제 unscaled operator/commutator/current 기호 검산 **30/30**.
- Lean 4.33.0: ObservableSelection **8/8**, SeamPolarization **8/8**, 총 **16/16**.
- 허용 axioms: `propext`, `Classical.choice`, `Quot.sound`; strict warnings 유지.

첫 source `3f18c1d`에서 기호 검산은 30개 모두 통과했지만 Lean은 예약 토큰 λ를
binder로 쓴 구문과 곱의 결합순서 증명을 거부했다. 수정 commit `b84a70e` 뒤 자체
생성 실패 JSON을 임시 보존하고 clean core의 정식 명령으로 전체 검증했다.
최종 환경·시간·full source commit·입력 hashes·각 정리의 signature/axiom은
[raw result](STAROBINSKY_OBSERVABLE_SELECTION_RESULT.json)에 있다.

Runner는 [source](starobinsky_observable_selection.py), 정리 목록은
[proof index](../formal/cpt_sewing/observable-selection-proof-index.json)로 고정했다.
연산자 클래스의 완전성, smooth Cauchy/Green 적분과 domain 해석은 analytic proof이며
Lean으로 그 전체를 형식화한 것은 아니다. 독립 검토에서 실제 H의 similarity 및
분류, seed lift의 한계, N×D 계수/비퇴화와 full CPT의 구별을 대조했다.
