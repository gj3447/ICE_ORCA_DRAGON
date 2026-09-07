# 관측가능량·내적 선택·BFV/CPT 접합의 문헌 기반 적대적 검토

2026-09-07 UTC · SUPPORTING_METHOD · SCOPED analytic/source review.

**기존 1차 strong 관측가능량 분류와 N–D Cauchy pairing은 명시한 범위에서 유지된다.
그러나 실제 물리 상태와 접합으로 넘어가는 데 필요한 연결은 생각보다 앞단에 있다.**
현재 compact-N 시험공간은 아래 자기수반 lapse 확장들의 graph core나 유한 gauge
변환의 불변공간이 아니다. 또한 N/D는 아직 BFV 경계 편극으로 식별되지 않았다.
양의 form과 반선형 교환 involution을 함께 요구해도 임의의 양수 함수가 남는다는
Cauchy-label 수준의 비유일성 예를 명시한다.

질문 하나: 현재 관측가능량–쌍대 상태–N/D pairing을 실제 observable/physical-product/
BFV-CPT sewing으로 해석할 때 어떤 추론이 문헌의 가정을 통과하지 못하는가?
출력 하나: 기존 결과의 유효 범위, 두 해석적 판별, 다음 구성의 필요한 입력을 대조한 검토서.
비주장: 새 물리, 완성된 RAQ/BFV/CPT, 원래 적분 경로 또는 G1 해소를 얻었다고 하지 않는다.

## 1. 무엇을 검토했고 무엇을 유지하는가

기준 commit은 `3fafc6ca4132eefd2e5c3e08eca3e351d1470d78`이다. 실제 operator,
flat density, hbar=1, B=[1/2,2]×[-1,2]×[1/4,2], repaired Φ_N/Φ_D 및 compact
seed G=C_c^∞((-1,2);C)는 기존 [Cauchy 유도](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md)와
[관측가능량 유도](STAROBINSKY_OBSERVABLE_SELECTION_DERIVATION.md)를 따른다.

| 검토한 주장 | 판정 | 정확한 경계 |
|---|---|---|
| 실제 unscaled H와 p_N의 1차 smooth local strong commutant는 cI+d p_N | 유지 | 계수 비교와 실제 potential의 대칭 제거. weak·고차·비국소 대수는 별도 |
| O ker T⊂ker T iff T∘O=λT, T≠0 | 유지 | 추상 endomorphism의 몫공간 판별이며 실제 O의 존재 정리는 아님 |
| 선택한 rank-one form과 formal star의 호환성 | 유지 | 등거리 보존은 별도. O=cI+d p_N에서 norm은 |c| 배로 변함 |
| Neumann/Dirichlet compact Cauchy 해족과 W_ND | 유지·범위 명료화 | 선언한 full-line Cauchy lift 사이 pairing. 전체 Φ_N*×Φ_D*의 pairing은 아님 |
| p_N Φ⊂Φ로 자기수반 gauge 작용까지 확보 | 불성립 | §3의 유한 N 인자에서 명시적 domain/group 장애물 |
| N/D Wronskian으로 BFV polarization 또는 실제 CPT를 확보 | 근거 없음 | §5의 graded 경계장과 원래 bulk의 대응이 먼저 필요 |
| 양의성·반선형 교환·involution으로 내적 선택 | 불충분 | §4의 모든 양의 w가 그 Cauchy-label 조건들을 만족 |

기존 문서는 마지막 세 승격을 이미 유보했다. 이번 검토는 그 유보의 구체적 이유를
보강한다. 기존 실행 결과나 Lean 정리의 반례를 발견했다고 보고하는 것은 아니다.

## 2. RAQ가 실제로 요구하는 것과 현재의 작은 대수

[Giulini–Marolf, *On the Generality of Refined Algebraic Quantization*, §II.1–II.2,
식 (4)–(7)](https://arxiv.org/html/gr-qc/9812024)는 보조 Hilbert 공간, 자기수반 제약,
공통 시험공간 및 그 위 observable-* 대수를 전제로 한다. 물리 내적의 수반 관계와
rigging map의 intertwining이 필요하다. 일반적인 observable 자체를 등거리 변환으로
요구하는 조건은 아니다. 자기수반 observable의 유한 unitary 작용과 구별해야 한다.

현재 T≠0이면 η_T(u)[v]=overline{T(u)}T(v)라는 반선형 rank-one 후보를 쓸 수 있다.
이것은 양의 Hermitian form이고, C[H,p_N]에서는 모든 제약이 소거되어 형식적
intertwining을 만족한다. 하지만 이 몫에서 그 대수는 상수뿐이어서 모든 seed가
똑같이 보인다. 이는 독립적으로 정한 비자명한 물리 observable 대수의 표현을 얻은
것이 아니다. 일반 c에 대해

\[
F_T(Ou,v)=F_T(u,O^*v),\qquad
F_T(Ou,Ov)=|c|^2F_T(u,v).
\]

두 식은 서로 다른 조건이다. |c|≠1이라는 이유만으로 observable이 부적격이라고
판정하지 않는다. 실제 self-adjoint realization과 그 unitary group은 아직 따로 필요하다.

Seed Qg=φg, Pg=−ig'의 작용을 Cauchy 해 label에 쓰는 것과 시험공간 관측가능량을
구성하는 것도 다르다. R(u)(g)=T_g(u)에 대해 필요한 식은

\[
R O_A=A'R,\qquad A'\operatorname{Ran}R\subseteq\operatorname{Ran}R.
\]

범위 불변성 다음에도 Φ 보존 lift, 그 연속성·정의역 및 adjoint 호환성을 검사해야
한다. 대수적 section만 택하면 분석적 문제가 사라지는 것은 아니다. 반대로 지금
그런 lift가 없다는 사실을 모든 nonlocal/weak lift의 불가능성 정리로 쓰지도 않는다.
쌍대 transpose는 합성 순서를 뒤집으며, RAQ의 adjoint를 포함한 쌍대 작용과도
규약을 맞춰야 한다.

[Giulini–Marolf, *A Uniqueness Theorem for Constraint Quantization*, §III의 정리](https://arxiv.org/html/gr-qc/9902045)는
L¹ 수렴, 적분된 gauge 대수 아래의 불변성, 비영 group average 등의 가정 아래에서
rigging map을 전체 상수배까지 제한한다. 현재 carrier가 그 가정을 만족한다고
확인하지 않았으므로 이 정리로 해·내적의 유일성을 가져올 수 없다. 이 유일성
정리의 가정이 모든 RAQ 방식의 필요조건이라는 주장도 하지 않는다.

## 3. 새 해석적 판별: compact-N 소거는 자기수반 lapse 영모드를 정하지 않는다

전체 H의 domain을 분류하지 않고 **N 한 인자의 scalar-phase 확장군**만 고정한다.
I=[N_-,N_+]=[1/4,2], ℓ=7/4, H_N=L²(I), P=−i∂_N이다.
[Bonneau–Faraut–Valent, §5.3 식 (14)–(15), Appendix A.3](https://arxiv.org/html/quant-ph/0103153)의
유한 구간 결과를 이 규약으로 옮기면

\[
D(P_\theta)=\{u\in H^1(I):u(N_+)=e^{i\theta}u(N_-)\},\qquad
\operatorname{spec}(P_\theta)=
\left\{\frac{2\pi n+\theta}{\ell}:n\in\mathbb Z\right\}.
\tag{1}
\]

θ는 mod 2π로 읽는다. 영모드는 θ=0일 때만 있다. 이 θ군을 같은 물리를 나타내는
허용 선택군으로 선언하는 것은 아니다. 아직 선택되지 않은 operator realization의
차이를 드러내는 비교군이다.

다음 세 논증은 식 (1)과 실제 collar 조건에서 직접 얻는 해석적 검산이다.

**Graph core 실패.** P_θ의 graph norm은 ‖u‖²+‖u'‖²의 제곱근, 즉 H¹ norm이다.
Collar 함수들의 그 norm에 대한 closure는 H¹_0(I)이고 양 끝 trace가 모두 0이다.
반면 v_θ(N)=exp(iθ(N−N_-)/ℓ)는 D(P_θ)에 속하면서 끝 trace가 비영이다.
따라서 collar-only 공간은 어느 P_θ의 graph core도 아니다. H¹ 경계 trace의
연속성 때문에 collar 함수의 어떤 부분공간으로도 이 간극을 메울 수 없다.

**유한 gauge 작용의 불변성 실패.** U_θ(t)=exp(−itP_θ)는 quasi-periodic extension을
이용한 translation이다. 비영 collar 함수의 내부 비영 값을 한 endpoint로 옮기는 t를
택하면 U_θ(t)u의 endpoint trace는 비영이다. 위상은 그 값을 0으로 만들지 않는다.
따라서 비영 collar-only 공간은 모든 U_θ(t) 아래 불변일 수 없다.
미분을 몇 번 적용해도 collar가 남는다는 사실은 이 유한 변환을 보장하지 않는다.

**쌍대 소거의 직접 반례.** L(u)=∫_Iu dN이면 모든 collar 함수에서 L(Pu)=0이다.
하지만 전체 D(P_θ)에서는

\[
L(P_\theta u)=-i\{u(N_+)-u(N_-)\}
=-i(e^{i\theta}-1)u(N_-).
\tag{2}
\]

θ≠0에서 v_θ를 넣으면 비영이다. L은 collar 제약을 소거하면서도 그 자기수반
확장의 영 고유함수로 작용하지 않는다. θ=0에서는 L(P_0u)=0이고 상수 영모드가
있지만, collar 공간의 core/group 문제는 여전히 남는다.

실제 Φ_N과 Φ_D에도 N-collar가 있으므로 위 trace와 translation 장애물은 고정
scalar phase의 N 작용을 다른 변수에 항등적으로 적용할 때 남는다. 이는 전체
결합 H+p_N의 모든 자기수반 확장, operator-valued endpoint condition, 모든 RAQ
또는 BFV 경로에 대한 no-go는 아니다. 특히 Φ가 operator core여야만 모든 추상
쌍대 구성을 할 수 있다는 주장을 하지 않는다. **현재의 미분적 소거를 full-domain
스펙트럼 또는 group averaging의 근거로 옮기는 추론이 실패한다**는 판별이다.

## 4. 새 비유일성 예: 양의 내적과 교환 involution을 동시에 만들어도 선택은 남는다

κ=1/(48π²)>0, S_N={s_g:g∈G}, S_D={t_h:h∈G}라 하자. 선언된 Cauchy 해족은
초기 value/derivative trace로 구별되어 S_N∩S_D={0}이고

\[
W(s_g,t_h)=-\kappa\int gh,\qquad W(S_N,S_N)=W(S_D,S_D)=0.
\]

[-1,2]의 열린 근방에서 smooth하고 엄격히 양수인 **임의의 실수 함수 w**를 고른다.
곱셈 w와 w⁻¹는 G를 보존한다. 다음 반선형 사상을 Cauchy label에서 정의한다:

\[
\Theta_w s_g=t_{w\bar g},\qquad
\Theta_w t_h=s_{w^{-1}\bar h}.
\tag{3}
\]

직접 대입하면 S_N⊕S_D에서

\[
\Theta_w^2=I,\qquad
W(\Theta_w x,\Theta_w y)=-\overline{W(x,y)}.
\tag{4}
\]

실제로 N×D에서는 W(t_{w bar g},s_{w⁻¹ bar h})=κ∫bar g bar h이고, 같은 편극은
양쪽 모두 0이다. 따라서 첫 slot에 반선형인 form을

\[
F_w(s_g,s_h):=-W(s_h,\Theta_w s_g)
=\kappa\int w\,\bar g h
\tag{5}
\]

로 두면 비영 g에서 F_w(s_g,s_g)>0이다. 예를 들어 w=1과 w=2+φ²는 모두
식 (3)–(5)를 만족하지만 고정 seed 식별 아래 서로 다른 form을 준다.
전체 상수배를 넘어선 자유도가 남는다. 적절한 사상으로 두 Hilbert 표현이 동등할
가능성을 배제하지 않으며, 동등성을 판정할 물리 observable 대수도 아직 없다.

이것은 원래 W에서 직접 유도하고 독립 검토한 **Cauchy-label 수준의 예**다.
Θ_w를 실제 CPT로 부르지 않는다. 반대 orientation·ghost·BFV differential과의
작용은 주지 않았고, F_w를 물리/RAQ 내적으로 확정하지 않는다. 실제 CPT에 가능한
모든 선택을 식 (3)이 분류한다는 주장도 아니다. 여기서 확인한 것은 양의성·교환·
involution·위 W covariance만으로는 w가 결정되지 않는다는 사실이다.

## 5. N/D Cauchy 공간을 BFV 편극으로 쓰기 전에 필요한 대응

우선 N/D는 solution Cauchy data (q,p)=(s|₂,∂_a s|₂)의 보손 symplectic 형식에
관한 상보적인 Lagrangian 부분공간이다. 여기서 p는 **coordinate derivative**이며
정준 momentum이나 metric unit normal과 자동으로 같지 않다. 이 data의 s는
minisuperspace 제약방정식의 해다. a=2의 cutoff/Cauchy 면을 곧바로 원래 spacetime
또는 worldline의 접합면 Σ로 식별할 수도 없다.

[CMR, *Classical BV theories on manifolds with boundary*, §3.1.1 식 (5)–(9),
§3.7](https://arxiv.org/pdf/1201.0290)는 graded 경계장 공간, ghost number 0의 symplectic
형식, degree 1의 cohomological field와 BFV action 및 bulk 제한사상을 사용한다.
고정 경계조건을 쓰는 경우에는 Lagrangian이 그 field에 접하고 boundary one-form과
호환하는 adapted 조건도 검사한다. 이는 현재 무한 jet 조건의 H,p_N 불변성만으로
따라오지 않는다.

따라서 기존 모형의 원래 phase space/작용에서
(F_Σ^∂,α_Σ^∂,ω_Σ^∂,Q_Σ^∂,S_Σ^∂,π)를 도출하고, 위 Cauchy data와의 사상이
있는지 먼저 확인해야 한다. 별도로 s를 새 고전장으로 취급해 symplectic 이론을
만들면 양자화 층을 추가하는 셈이므로 원래 모형의 BFV 구조를 얻었다고 할 수 없다.
기존 graph에 BFV 후보가 있다는 사실도 이 **같은 H·density·domain·seam**과의
정확한 대응을 대신하지 못한다.

## 6. 실제 quantum 접합에서 검사할 항등식

[CMR, *Perturbative quantum gauge theories on manifolds with boundary*, §2.3,
식 (2.22), §2.4.4 식 (2.36), Remark 2.37](https://arxiv.org/html/1507.01221)의 접합은
편극에 따른 graded state modules와 그 사이의 적분 kernel, residual BV fields와
pushforward를 사용한다. 함수의 Wronskian 자체가 이 quantum 적분 kernel은 아니다.
특히 transverse pairing에는 half-density와 편극 변환 kernel이 들어간다.

모형에 맞춰 orientation, 좌/우 module, ghost 순서와 Berezin 규약을 고정한 뒤
실제 pairing B에 대해, 표준 tensor differential 규약이라면

\[
B(\Omega_+x,y)+(-1)^{|x|}B(x,\Omega_-y)=0
\tag{6}
\]

를 검사한다. 식 (6)은 그 규약을 택했을 때의 chain-map 조건이며, 부호를 모든
BFV/CPT 문헌에 보편적으로 적용하지 않는다. 현재 on-shell Hs=p_Ns=0은 이
off-shell graded 식의 대체물이 아니다. Pairing이 cohomology에 내려가는 것,
그 위 비퇴화성과 양의성도 각각 확인해야 한다.

실제 CPT 후보 Θ에는 전체 경계 변수와 ghost의 작용, Θ², Ω와의 intertwining,
pairing covariance가 필요하다. 이어 residual Δ와 Z를 실제로 구성하여

\[
(\hbar^2\Delta+\Omega)Z=0,\qquad
Z_M=P_*(Z_{M_1}*_{\Sigma}Z_{M_2})
\tag{7}
\]

를 확인해야 한다. 이 추상 형식이 실제 source-defined 적분 cycle이나 규제 제거를
구성해 주지는 않는다. K=conjugation 또는 §4의 Θ_w만 넣어 식 (7)이 완성됐다고
기록하지 않는다.

## 7. Cauchy 정리가 주는 범위와 제한

[Bär–Ginoux–Pfäffle, *Wave Equations on Lorentzian Manifolds and Quantization*,
Theorems 3.2.11–12, printed pp.85–87](https://arxiv.org/pdf/0806.1036v1)를 다시 대조했다.
사용한 열린 R_x×R_φ extension은 globally hyperbolic이고 potential은 smooth하며
terminal data는 compact smooth다. 따라서 이 적용은 유지된다. 다만 이 정리는
유한 box의 자기수반 경계값 문제를 풀거나 유한 φ-box의 lateral flux를 없애지 않는다.

G=C_c^∞((-1,2))에서 g↦T_g의 injectivity도 유지된다. T_g=0이면 interior compact
tests로 s_g=0 on B°이고, smooth terminal trace에서 g=0을 회복한다. 이 논증은
seed 전체가 선언한 φ interval 안에 있다는 사실을 쓴다. D 쪽은 derivative trace를
같은 방식으로 회복한다.

그러므로 W는 **선언한 compact-seed 쌍대 image에 full-line Cauchy lift로 운반한
pairing**으로 읽을 수 있다. 임의의 Φ_N*와 Φ_D* 원소 전체에 정의된 intrinsic
pairing이나 임의 full-line representative와 무관한 보존 법칙이라고 확대하지 않는다.
W에는 N/ghost integration도 아직 포함되지 않는다.

## 8. 보완 순서와 검증 기록

먼저 현재의 collar carrier를 어느 분석적 역할에 쓸지 고정해야 한다. 제한된 test
complex로 유지할 수는 있지만, 같은 공간에 유한 gauge invariance를 동시에 주장할
수는 없다. 다른 carrier나 lapse realization을 제안하면 기존 T_g와의 비교 사상과
H-domain/Green compatibility를 다시 제공해야 한다. 주기 경계조건을 선택한다는
말만으로 원래 interval gauge 기하가 정당화되지는 않는다.

| 필요한 출력 | 다음에 판별할 수 있는 내용 |
|---|---|
| 동일 모형에서 명시한 operator domains와 gauge/observable carrier | 제약 소거가 어느 자기수반·쌍대·group 해석에서 성립하는지 |
| 비자명 observable 하나의 실제 lift와 adjoint/domain 관계 | rank-one 선택이 살아남는지, 더 큰 해공간이 필요한지 |
| 원래 작용의 BFV 경계 data와 N/D Cauchy data의 대응 | 현재 pairing이 그 경계 구조에 실제로 사용될 수 있는지 |
| 전체 graded seam kernel 및 CPT 작용 | 식 (6), cohomology pairing, 선택된 내적의 양의성 |
| residual BV/mQME/pushforward와 upstream source-cycle 입력 | 선언한 route의 실제 접합 및 규제 제거 |

이 순서는 supporting 연구의 의존관계다. 새 계산을 자동 승인하는 queue가 아니다.
현재 core blocker `open:gate1-original-cycle-signed-global-intersections`는 그대로다.
Planner 분류는 `INSUFFICIENT_ROUTE_EVIDENCE`, core eligibility는 `NOT_ELIGIBLE`였고,
choice-invariance/cross-domain 경계를 읽은 뒤 이 검토를 supporting으로 분류했다.
별도 ontology graph의 비슷한 결과를 여기의 증거로 가져오지 않았다.

문헌 검토일은 2026-09-07 UTC다. 검색어는 `BV-BFV polarization gluing quantum mechanics`,
`refined algebraic quantization uniqueness observable rigging map`,
`Bonneau Faraut Valent self adjoint extensions momentum finite interval`를 포함했다.
검색 요약만으로 결론을 내리지 않고 위 여섯 primary 원문의 해당 절·식과 기존
source를 직접 대조했다. 외부 PDF나 검색 cache는 저장소에 추가하지 않았다.

주된 실패원인은 **inference/domain**이다. 관련 control은 (i) finite-N endpoint
trace와 full-domain boundary term, (ii) w와 w⁻¹의 compact-seed 보존 및 pairing
부호, (iii) Cauchy data와 graded BFV 경계 data의 타입 대조다. 독립 검토에서
RAQ/lift, PDE/Green, BFV/CPT를 나누어 확인하고 식 (1)–(5)의 별도 검산을 받았다.

이번 검토는 해석적 증명과 원문 대조다. **새 수치 계산이나 Lean 실행을 하지 않았다.**
기존 30개 기호 검산·16개 Lean 정리는
[기존 raw result](STAROBINSKY_OBSERVABLE_SELECTION_RESULT.json)의 범위에서만 유효하며,
새 Sobolev/core·unitary group·w-family 논증을 Lean이 증명했다고 세지 않는다.
고정된 runner 입력과 과거 raw result는 수정하지 않는다.
