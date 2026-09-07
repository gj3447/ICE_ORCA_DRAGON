# 실제 유한 쌍대 lift와 canonical BFV 경계조건의 구성·판별

2026-09-07 · SUPPORTING_METHOD · SCOPED analytic derivation.

질문: 현재 compact-N repaired carrier에서 쌍대 해의 유한 작용을 실제 관측가능량으로
올리고, a=2 Cauchy cut을 선언한 canonical BFV 경계조건으로 사용할 수 있는가?
출력: 실제 finite-rank lift의 구성과 adjoint-domain obstruction, 같은 고전 제약의
fixed-a/free-ghost 접성 판별 및 ghost를 고정한 adapted endpoint 후보.
비주장: 전체 self-adjoint H+p_N domain, 물리 observable/내적, quantum CPT/sewing,
original relative cycle 또는 G1을 완성하지 않는다.

기준은 `03be96699ec4f3c18dff36efe5f8531a4e016eda`의
[문헌 검토](STAROBINSKY_OBSERVABLE_SEWING_SOURCE_REVIEW.md),
[쌍대 해](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md),
[실제 Weyl 관측가능량](STAROBINSKY_OBSERVABLE_SELECTION_DERIVATION.md)이다.
Planner는 `INSUFFICIENT_ROUTE_EVIDENCE / NOT_ELIGIBLE`이며, 이 결과는
`open:starobinsky-seam-ward-boundary-state-limit`의 supporting domain/경계 입력만 좁힌다.
G1 원래 joint class·signed intersections → G2 kernel → G3 gluing → G4 state/domain
→ G5 interaction → full-theory/empirical review의 upstream 입력은 제공하지 않는다.

## 1. 현재 carrier를 유지한 실제 유한 lift

보조 공간은 K=L²(B), B=[1/2,2]×[-1,2]×[1/4,2], flat density이고,
Φ=Φ_N은 기존 repaired Neumann 시험공간이다. H,p_N은 Φ를 보존하며
p=p_N=−i∂_N은 그 위에서 symmetric이고 injective다. 후자는 pu=0이면 u가
N-independent인데 N-collar 조건이 u=0을 강제하기 때문이다. Φ는 완비 Hilbert
공간이 아니며, 아래 수반은 K의 L² 수반을 뜻한다.

독립 compact seeds g₁,…,g_n의 실제 Neumann Cauchy 해 s_i=s_{g_i}를 쓰고

\[
T_i(u)=\int_B s_i u,\qquad R(u)=(T_1(u),\ldots,T_n(u))
\tag{1}
\]

로 둔다. T_i는 K에도 bounded이고 RH=Rp=0 on Φ이다. s_i의 B° 위 선형독립은
interior tests와 terminal trace로부터 따른다. 이를 이용하면 ζ∈C_c^∞(B°), ζ≥0를
골라 다음 행렬을 positive definite로 만들 수 있다:

\[
G_{ij}=\int_B\zeta s_i\overline{s_j}.
\tag{2}
\]

구체적 존재 논증: s_i의 선형독립성으로 evaluation vectors가 C^n을 span하는
유한 개의 내부 점을 고른다. 그 점들의 작은 근방에서 양수인 compact bump들의
합을 ζ로 택하면, c*Gc=0은 그 모든 evaluation에서 해당 선형결합이 0임을 뜻하므로
c=0이다. PDE의 임의 열린 집합 unique continuation을 가정하지 않았다.

f_k=ζ overline{s_k}, v_j=Σ_k f_k(G⁻¹)_{kj}라 하면 v_j∈C_c^∞(B°)⊂Φ이고
T_i(v_j)=δ_ij다. 따라서

\[
Jz=\sum_jz_jv_j,\qquad RJ=I_{\mathbb C^n},\qquad
O_A=JAR:K\longrightarrow K
\tag{3}
\]

는 임의의 행렬 A에 대해 실제 bounded finite-rank 연산자이며 O_A Φ⊂Φ다.
그 작용은 정확히 RO_A=AR이고, RO_AJ=A이므로 A≠0이면 O_A≠0이다.
예를 들어 g₁=g₀, g₂=φg₀와 A=[[0,1],[1,0]]는 두 쌍대 성분을 교환한다.
g₀는 기존 compact bump다. 이 구성은 유한 행렬만 가정한 abstract relabelling이
아니라 실제 Cauchy 함수·bump 적분·Gram inverse로 정의한 시험공간 연산자다.
다만 Gram 적분의 수치값이나 PDE array를 계산했다는 뜻은 아니다.

## 2. 이 lift는 왜 관측가능량 조건을 통과하지 못하는가

식 (3)은 Rp=0 때문에 O_Ap=0이다. 만약 pO_A=O_Ap도 성립하면 pO_A=0이고,
p의 Φ 위 injectivity로 O_A=0이다. 따라서 A≠0이면 **p_N과의 strong commutation이
반드시 실패**한다. H와의 commutator까지 별도 논증 없이 비영이라고 쓰지 않는다.

더 강하게, Φ 위에 O와 그 수반 O*가 모두 작용하고 Op=0이면

\[
0=\langle Op u,v\rangle
=\langle p u,O^*v\rangle
=\langle u,pO^*v\rangle\qquad(u,v\in\Phi).
\tag{4}
\]

Φ의 양의 nondegenerate L² 내적과 pO*v∈Φ로부터 pO*v=0, 이어 O*v=0이다.
다시 수반 관계를 쓰면 O=0이다. 이 논증은 self-adjoint closure나 완비성을
요구하지 않는다. **현재 carrier에서 p를 오른쪽에서 소거하는 비영 연산자는
carrier를 보존하는 수반을 함께 가질 수 없다.**

식 (3)의 bounded K-adjoint를 직접 보면 같은 장애물이 드러난다.
O_A†=R†A†J†의 image는 N-independent인 overline{s_i}들의 span 안에 있다.
그 비영 원소는 N-collar를 만족하지 않는다. Φ는 K에 dense이고 A≠0이므로
O_A†가 Φ 전체에서 0일 수도 없다. 따라서 O_A†Φ⊄Φ다.
이것이 실제 finite-rank 후보의 [RAQ observable-* domain 조건](https://arxiv.org/html/gr-qc/9812024)
실패다. 비자명한 label 행렬이 존재한다는 사실로 이 조건을 대체하지 않는다.

이 결과는 **모든 lift의 부재**가 아니다. RO=AR를 만족하는 일반 O는

\[
O=JAR+B,\qquad RB=0
\tag{5}
\]

로 쓸 수 있다. B=O−JAR가 그 예다. 비영 O가 수반 조건을 통과하려면 Op=Bp가
항등적으로 0이어서는 안 된다. 즉 제약의 image처럼 R이 지운 방향에도 실제
작용을 남겨야 한다. 이것은 필요조건이며 B를 구성했다는 뜻은 아니다.
임의의 kernel 보정이 strong/weak BRST 또는 adjoint 조건을 만족하는 것도 아니다.

## 3. 정의역의 선택에서 이번에 해결한 범위

기존 [유한 N 구간 검토](STAROBINSKY_OBSERVABLE_SEWING_SOURCE_REVIEW.md#3-새-해석적-판별-compact-n-소거는-자기수반-lapse-영모드를-정하지-않는다)의
scalar-phase self-adjoint 확장 비교는 그대로다. 본 작업은 원래 interval 끝점을
붙이거나 positive lapse를 전 실수축으로 확장하지 않았다. 현재 Φ의 정확한 역할은
미분적 test complex이며, 모든 유한 gauge 변환의 불변공간 또는 self-adjoint core로
승격하지 않는다. [Bonneau–Faraut–Valent §5.3, Appendix A](https://arxiv.org/html/quant-ph/0103153).

이번 구성의 비영 O_A는 이 원래 Φ에서 실제로 정의되지만 물리 observable 조건을
실패한다. 따라서 기존 내적의 w 자유도를 이것으로 제한할 수 없다. Seed의
−i∂_φ를 형식적으로 symmetric하게 요구하면 w'=0이라는 식을 얻을 수 있어도,
그 연산자를 실제로 lift하지 않은 채 물리 내적 선택이라고 기록하지 않는다.

## 4. 같은 고전 제약의 canonical BFV 경계 data

양자 Weyl H와 구별하여, [고정한 고전 Hamiltonian](STAROBINSKY_POLYNOMIAL_BFV_CHART.md)을 쓴다:

\[
H_L=-\frac{p_a^2}{24\pi^2a}+\frac{p_\phi^2}{4\pi^2a^3}
-6\pi^2a+\frac32\pi^2a^3F(\phi),\quad
F=(1-e^{-\beta\phi})^2,\quad\beta=\sqrt{2/3}.
\tag{6}
\]

실수 a>0의 finite canonical chart이며, 임의의 과거 momentum cutoff를 승계하지
않는다. Even 좌표는 (a,φ,N;p_a,p_φ,Π), odd 좌표는 (c,barρ,ρ,barc)이고 ghost
number는 (1,−1,1,−1)이다. 기존에 선언한 primitive와 charge를 유지한다:

\[
\alpha=p_a\delta a+p_\phi\delta\phi+\Pi\delta N
+\bar\rho\delta c+\bar c\delta\rho,\quad
\omega=\delta\alpha,\quad\Omega=cH_L+\rho\Pi.
\tag{7}
\]

정확히 pinned exterior helper의 {q,p}=1, odd canonical bracket symmetric +1,
오른쪽/왼쪽 odd derivative를 쓴다. [Source proposal](../docs/research/ICE_BFV_CPT_SEAM_WARD_SOURCE_PROPOSAL_2026-09-07.md)의 QF={Ω,F} 순서이므로

\[
\begin{aligned}
Qa&=\frac{c p_a}{12\pi^2a},& Q\phi&=-\frac{c p_\phi}{2\pi^2a^3},&QN&=-\rho,\\
Qp_a&=c\partial_aH_L,&Qp_\phi&=c\partial_\phi H_L,&Q\Pi&=0,\\
Qc&=Q\rho=0,&Q\bar\rho&=H_L,&Q\bar c&=\Pi.
\end{aligned}
\tag{8}
\]

Even 성분의 부호를 {F,Ω}의 Hamiltonian flow와 섞지 않는다. {Ω,Ω}=0은
H_L의 N 독립성과 두 제약의 가환성에서 따른다. 이 canonical charge는 현재
동차 모델의 선언된 BFV 후보이며 원래 covariant bulk에서 유도한 CMR 경계장
전체라고 하지 않는다.

## 5. free ghost를 둔 정확한 fixed-a 제약면의 접성 실패

정확한 a=2 조건을 보존하면서 c를 독립적인 자유 ghost로 두는 후보를 검사한다.
Qa=0의 c 계수는 p_a=0을 요구하고, 이 조건의 접성은 H_{L,a}=0을 요구한다.
고전 제약 H_L=0 위에서 p_a=0을 넣고 p_φ²를 소거하면

\[
H_{L,a}=3\pi^2(3a^2F-8).
\tag{9}
\]

예를 들어 a=2,φ=0,p_a=0,p_φ=8√6π²,Π=0은 H_L=0이지만
H_{L,a}=−24π²라서 Qp_a=−24π²c≠0이다.

예외 후보 F=2/3도 한 단계 더 검사한다. a=2에서 H_L=H_{L,a}=0은
p_φ²=128π⁴를 요구한다. 한편 원래 bosonic bracket은 p_a=0에서

\[
\{H_L,H_{L,a}\}=-\frac9{2a}p_\phi F'(\phi).
\tag{10}
\]

z=e^{-βφ}>0이고 F=(1−z)²=2/3이면 F'=2βz(1−z)≠0이며 p_φ≠0이다.
따라서 H_{L,a}=0 조건의 Q-접성도 실패한다. **이 정확한 fixed-a=2,
실수 constraint-body, 독립 free-c ansatz 안에는 Q-invariant locus가 없다.**
Ghost 제한, ghost를 포함한 변형 경계식, 변형된 charge 또는 추가 장을 다루는
보편적 no-go로 확대하지 않는다.

Lean의 실제 유한 실수 판별에는 p=p_φ/π²를 써서

\[
p^2/32-12+12(1-z)^2=0,\qquad
-3p^2/64-6+18(1-z)^2=0,\qquad pz(1-z)=0,
\tag{11}
\]

와 z>0의 동시 불가능성을 쓴다. 식 (6)·(8)·(10)에서 식 (11)로 가는 대응은
해석적 유도와 symbolic coefficient 검산이고, Lean은 그 뒤의 실수 polynomial
모순을 검증한다. 파동함수의 ∂_a s를 고전 p_a로 놓지 않았다.

## 6. 구성 가능한 ghost-fixed canonical endpoint

상수 a₀>0,φ₀,N₀에 대해

\[
L_{q_0}=\{a=a_0,\phi=\phi_0,N=N_0,c=\rho=0\}
\tag{12}
\]

를 택하고 (p_a,p_φ,Π,barρ,barc)를 자유롭게 둔다. α의 pullback은 0이고,
even 6개 중 3개·odd 4개 중 2개의 canonical 방향을 가지므로 finite graded
Lagrangian이다. Ω|L=0이며, 식 (8)에서 (12)를 정의하는 모든 좌표의 Q-변화는
0이다. Qbarρ=H_L, Qbarc=Π는 자유롭게 둔 방향이므로 접성을 깨지 않는다.
따라서 이 **ghost-fixed endpoint 후보는 실제 선언한 finite canonical BFV에서
adapted 조건의 유한 canonical 대응을 만족**한다. 이 구성에는 H_L=Π=0을 body에 추가로 요구하지 않는다.

이는 c와 ρ를 0으로 대입한 경계조건의 구성이지, ghost sector를 계산 전체에서
삭제하라는 처방이 아니다. Endpoints에서 gauge parameter를 제한하는 의미가
있지만, 허용 bulk gauge군이나 원래 적분 source가 이를 선택했다고 하지 않는다.
[CMR의 adapted 경계조건 §3.7과 bulk–boundary data §3.1.1](https://arxiv.org/pdf/1201.0290)을
우리 원래 이론에 적용하려면 bulk의 제한사상과 경계 symplectic reduction을
따로 구성해야 한다.

현재 N/D 공간은 Weyl H의 quantum Cauchy data이다. 식 (12)의 고전 configuration/
ghost endpoint와는 다른 객체이며, 그 사이의 양자화·편극 대응은 아직 없다.
따라서 (12)를 얻었다고 N–D Wronskian, 가중 내적 F_w, K 또는 실제 CPT 접합이
선택됐다고 하지 않는다. Quantum state module·seam kernel·residual BV·mQME와
pushforward는 [CMR quantum §2.3–2.4](https://arxiv.org/html/1507.01221)의 별도 구성 대상이다.

## 7. 검사 범위와 다음에 필요한 입력

주된 위험은 **domain**이다. 관련 controls는 actual finite-lift/수반 조건,
원래 graded bracket의 부호 및 constrained tangency counterexample, 그리고
실패하는 free-ghost branch와 성립하는 ghost-fixed endpoint branch의 대조다.
새 내적이나 ghost 조건을 독립적인 물리 선택군으로 승격하지 않는다.

Runner `./ice run starobinsky_quotient_lift_bfv_boundary`는 실제 canonical Q table,
식 (9)–(11), endpoint tangent/charge 조건 및 두 Lean module을 검사한다.
Finite-dimensional Gram section의 실제 PDE/bump 존재, p_N의 Φ 위 injectivity와
formal symmetry, Lagrangian 차원/primitive 해석은 이 유도문의 analytic 입력이다.
검산 성공 여부는 실행 후의 raw result만 정본이며, 이 source 자체는 실행 receipt가 아니다.

다음 observable 후보는 (5)의 kernel 방향 작용까지 포함해야 한다. 다음 BFV 후보는
(12)의 endpoint와 원래 source/quantum state의 대응을 제공해야 한다. 둘 중 하나를
가정으로 숨기고 w 선택이나 CPT 완성을 주장하지 않는다. 이 결과는 새로운 후속
계산을 자동 승인하지 않는다.
