# Compact lapse 복합체의 실제 contraction과 남는 cohomology

2026-09-07 · SUPPORTING_METHOD · analytic construction.

질문: 기존 시험복합체의 상태를 지우지 않고 primary constraint를 제거하며,
반대쪽 graded dual과의 pairing을 보존하는가?
출력: 실제 적분 사상에 의한 chain homotopy equivalence와 cohomology 판별.
비주장: positive physical product, quantum interval amplitude, 원래 적분 경로 또는 G1 해결이 아니다.

## 1. 실제 공간과 적분 사상

[기존 Cauchy 유도](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md)의 B, flat density,
unscaled Weyl H, p=−i∂N, repaired Neumann Φ를 그대로 쓴다.
Face 근방에서 0이라는 조건은 다른 변수들에 대해 **uniform collar**를 뜻한다.
Compact face의 열린 근방이라는 원래 표현이 이를 보장한다. 각 N slice마다 별개의
비균일 collar만 허용하는 더 큰 공간에 적용하지 않는다.

Ψ는 [1/2,2]×[−1,2] 위 ambient smooth restrictions 중 lower-a와 두 φ-face의
uniform collars에서 0이고 ∂a H^k v|₂=0 for all k≥0인 공간이다.
I=[N₋,N₊]=[1/4,2], real χ∈Cc∞(I°), ∫Iχ=1을 고른다. 정의:

\[
 R_Nu=\int_Iu\,dN,\quad J_\chi v=\chi(N)v,\quad
 K_\chi u=i\int_{N_-}^N\bigl(u(t)-\chi(t)R_Nu\bigr)dt.
 \tag{1}
\]

R_NΦ⊂Ψ, JχΨ⊂Φ, KχΦ⊂Φ다. 마지막 포함에서 upper-N collar는
integrand의 전체 적분이 0이므로 성립한다. 단순 indefinite integral은 upper collar를
깨뜨리지만 (1)의 subtraction은 그것을 복구한다. Lower-N collar는 적분 시작점에서
성립한다. Lower-a/φ collars는 uniformity로 보존된다. H가 N에 무관하므로 적분과
교환하고, a=2의 모든 H/p jets도 보존된다. m≥1인 p^m K에는 아래 pK 식을 사용한다.
K와 p가 commute한다고 주장하지 않는다.

\[
 R_NJ_\chi=1,\quad R_Np=0,\quad
 pK_\chi=1-J_\chi R_N,\quad K_\chi p=1,
 \tag{2}
\]
\[
 R_NH=HR_N,\quad HJ_\chi=J_\chi H,\quad HK_\chi=K_\chi H.
 \tag{3}
\]

미적분 기본정리와 N collars로 직접 따른다. 특히 Kp=1의 lower trace는 0이다.
Ambient C∞ seminorm topology에서 세 사상은 continuous다. 유한 I에서 L² 적분
estimate로 보조 L² 공간 사이의 bounded extension도 존재하지만 H나 p의 self-adjoint
completion, gauge-group integration을 뜻하지 않는다.

## 2. 전체 chain maps와 homotopy

C⁰=Φ, C¹=Φ², C²=Φ, q₀u=(Hu,pu), q₁(x,y)=Hy−px다.
축소 복합체 D는 **degree 1,2**에 Ψ,Ψ를 두고 d=H, 다른 degree는 0이다.

\[
 F^0=0,\ F^1(x,y)=R_Ny,\ F^2z=R_Nz;
 \quad I^1y=(0,J_\chi y),\ I^2z=J_\chi z.
 \tag{4}
\]

(2)–(3)으로 F q = d F, q I = I d, F I = id_D이다. I d는 inclusion과
d의 합성이다. Homotopy는

\[
 h^1(x,y)=K_\chi y,\quad h^2z=(-K_\chi z,0),\quad
 1-IF=qh+hq.
 \tag{5}
\]

실제 degree별 항등식은

\[
 h^1q_0u=u,\quad
 q_0h^1(x,y)+h^2q_1(x,y)=(x,y)-(0,J_\chi R_Ny),
 \quad q_1h^2z=z-J_\chi R_Nz.
 \tag{6}
\]

따라서 단순 injective embedding과 달리 **cohomology를 보존하는 chain homotopy
equivalence**를 구성했다. 앞서 top class를 지운 coefficient-only dual로의 embedding은
여전히 quasi-isomorphism이 아니다. 이번 사상은 그 실패한 사상을 정당화하지 않는다.

## 3. H¹도 0이고, 비영 class는 H²에 남는다

\[
 H^0(C)=0,\qquad H^1(C)\cong\ker(H:\Psi\to\Psi),\qquad
 H^2(C)\cong\Psi/H\Psi.
 \tag{7}
\]

Hv=0인 v∈Ψ를 φ 양쪽과 lower-a 바깥으로 0으로 연장한다. Collars 때문에 smooth하며
방정식도 보존된다. x=log a, v=aχ로 바꾸면 기존의 normally hyperbolic operator P다.
Lower-a 아래의 전체 Cauchy surface에서 초기값과 도함수가 0이다. 열린 globally
hyperbolic extension의 Cauchy uniqueness로 v=0이다. Upper-a 이후로 0 연장할 필요는
없으며, 주어진 slab 안의 domain of dependence에 uniqueness를 적용한다.
[Bär–Ginoux–Pfäffle Thm 3.2.11](https://arxiv.org/pdf/0806.1036v1)의 smooth-coefficient
가정과 log-a 변환은 기존 pinned 유도에 명시돼 있다. 따라서 **H¹(C)=0**이다.

H²는 0이 아니다. 기존 Neumann Cauchy 해 s_g에 대해
\(t_g[v]=\int s_gv\,da\,d\phi\)라 두면 t_gH=0이고
\(T_g=t_gR_N\)다. 기존 compact Gram sections가 임의 유한 n의 독립 class를
검출하므로 H²(C), Ψ/HΨ는 무한차원이다. Exactness의 명시적 동치:

\[
 z\in\operatorname{im}q_1\quad\Longleftrightarrow\quad
 R_Nz\in H\Psi.
 \tag{8}
\]

역방향에서 R_Nz=Hv이면 z=q₁(−Kχz,Jχv)이다. 이것은 H 역연산자를 새로
가정하거나 계산한 것이 아니다. 임의의 coker class를 모든 smooth Neumann seeds가
분리한다는 완전성 정리는 여기서 주장하지 않는다.

## 4. 선택 변화와 실제 graded pairing

허용 선택군은 동일 I에서 ∫χ=1인 모든 real compact smooth χ다. R_N은 χ와
무관하다. R_Nz=R_Nw이면 z−w=q₁(−Kχ(z−w),0)이므로 서로 다른 χ가 고른
대표는 같은 top class를 준다. 예컨대 Jχ₁v−Jχ₀v는 exact다.
이는 **대표 bump 선택의 불변성**이며, 경계조건·contour·모든 gauge choice에 대한
물리적 불변성으로 확장하지 않는다.

[graded dual 유도](STAROBINSKY_GRADED_DUAL_SEWING_DERIVATION.md)에서 실제 evaluation은
T_g[z]=t_g[R_Nz]다. 축소 전후 같은 값을 주고 q₁-exact 대표를 소거한다.
Thus dual transfer F^t and I^t preserves this pairing; algebraic transpose of (5) gives
the dual chain homotopy with the declared degree signs. T_g는 선택한 C∞ topology에도
연속이므로 적어도 이 실제 family에는 algebraic-only existence 문제도 없다.
전체 continuous dual의 exactness/closed-range 정리를 추정하지 않는다.

Nonzero pairing은 bilinear이며 positive norm이 아니다. Ghost degree 2와 반대쪽
degree −2를 짝짓는다; 단순 degree shift는 물리 ghost-number-zero 선언이 아니다.
구간 source의 quantization map, half-density/Berezin normalization, residual pushforward는
[source 검토](../docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md)의
별도 입력이다.

## 5. 검증 경계

Primary failure class는 `inference`: 연산자 정의역·차수·source 유형의 혼동이다.
Controls는 (i) 실제 H/p와 collar subtraction, (ii) 전체 chain homotopy 및 graded Ward
부호, (iii) source/anti-linear convention의 독립 대조다. Runner
`./ice run starobinsky_primary_reduction_graded_sewing`는 기호 항등식과 두 Lean modules를
검증한다. Smooth support/적분 존재와 Cauchy uniqueness 적용은 이 해석적 증명 및 독립
검토이며 Lean이 formalize하지 않는다. 실제 출력·입력 hash·환경·실패는 raw result 정본이다.

Planner의 INSUFFICIENT_ROUTE_EVIDENCE/STOP_OR_REFRAME은 core 분류에 대한 것이다.
명시한 missing object는 current test-state complex의 equivalence/pairing이며
open:starobinsky-seam-ward-boundary-state-limit의 supporting 질문으로 수행한다.
G1 original joint class→G2 kernel→G3 gluing→G4 states→G5 interactions→full-theory/
empirical review의 upstream blocker를 해소했다고 세지 않는다.
