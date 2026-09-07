# Gaussian Ward pairing의 a=2 경계 극한

2026-09-07 · SUPPORTING_METHOD · 해석적 유도 정본.

질문 하나: 선언한 매끄러운 시험함수 쌍에 대해 전체 Gaussian Ward pairing의
규제 제거 극한은 a=2 Green 경계형식과 같은가?
출력 하나: 아래의 경계 쌍선형 함수와 수렴 상계.
비주장 하나: 물리적 BFV 상태·자기수반 실현·원래 적분 경로를 구성하지 않는다.

기존 [Ward 보고서](STAROBINSKY_BFV_SEAM_WARD.md)의 flat density, Weyl ordering,
hbar=1, ghost/Berezin convention 및 box를 그대로 사용한다. 사전 planner는
INSUFFICIENT_ROUTE_EVIDENCE였으므로 이 계산은 core G1 진전으로 세지 않는다.
직접 줄이는 질문은 open:starobinsky-seam-ward-cutoff-boundary-limit의 한 면 사례다.

## 1. 시험공간과 실제 pairing

M=(0,infinity) x R x R, q=(a,phi,N),
B=[1/2,2] x [-1,2] x [1/4,2], chi=1_B로 둔다.

\[
f(a)=-{1\over24\pi^2a},\quad b(a)={1\over4\pi^2a^3},\quad
W(a,\phi)=-6\pi^2a+{3\over2}\pi^2a^3(1-e^{-\sqrt{2/3}\phi})^2-{f''(a)\over4},
\]
\[
H=-\partial_a(f\partial_a)-b\partial_\phi^2+W,\quad
D_\tau(z)=(2\pi\tau)^{-3/2}e^{-|z|^2/(2\tau)},\quad
F_\tau(x,y)=\chi(x)\chi(y)D_\tau(x-y).
\]

u,v는 실수 C_c^\infty(M)이며, B의 경계에서는 a=2 면에만 닿게 한다:
a=1/2, phi=-1,2, N=1/4,2의 근방에서 0이다.
a=2를 가로질러 매끄럽게 정의된 시험함수이며 이 면에서 0이라고 가정하지 않는다.
이는 진단용 시험공간이지 물리적 BRST cohomology나 선택된 자기수반 domain이 아니다.

분포 pairing은 M x M 위에서 정의한다. 따라서 hard indicator의 도함수도 포함되고,
delta-prime에 indicator의 임의 경계값을 곱하는 처방을 넣지 않는다.

\[
\mathcal B_\tau[u,v]
=\langle (H_x-H_y)F_\tau,u(x)v(y)\rangle
=\int_{B\times B}D_\tau(x-y)A(x,y)\,dx\,dy,
\quad
A(x,y)=(Hu)(x)v(y)-u(x)(Hv)(y).
\tag{1}
\]

둘째 등식은 compact ambient tests에서 H의 formal transpose가 H라는 사실이다.
가정한 적분 극한을 식 (1)에 대입해서 만든 정의가 아니다.
H의 계수는 B 근방에서 매끄럽고 모든 적분은 a>=1/2 안에 있으므로 a=0의
연산자 확장이나 Gaussian의 반직선 밖 동역학을 사용하지 않는다.

전체 graded Ward 식은 c1*g*(H1-H2)F_tau - i*rho1*g*(d_N1+d_N2)F_tau다.
g=(c2+c1)(rho2-rho1), generator 순서 (c1,c2,rho1,rho2)를 유지한다.
왼쪽에서 rho1을 곱하고 c1*c2*rho1*rho2 계수를 +1로 추출하는 Berezin dual은
c1*g를 +1로 읽고 rho1*g를 0으로 읽는다. 따라서 (1)은 실제로 검출되는 Ward 성분이다.
더욱이 이 시험공간에서는 N-face의 시험함수 값이 0이고 Gaussian의 diagonal
N derivative가 0이므로 primary N pairing 자체도 모든 tau>0에서 0이다.
Phi face와 lower-a face의 pairing도 시험함수의 지지 조건으로 0이다.

## 2. 약한 극한과 명시적인 O(sqrt(tau)) 상계

L=max_{B x B, i=1,2,3}|partial_{y_i} A(x,y)|,
M0=max_{q in B}|A(q,q)|로 둔다. Compactness와 smoothness로 둘 다 유한하다.
이 상계는 선택한 u,v에 대한 것이며 모든 정규화 상태 위의 operator-norm 상계가 아니다.

A(x,y)-A(x,x)를 빼고 더하면 첫 오차는 좌표별 평균값 정리로
L sum_i |y_i-x_i| 이하이다. 각 Gaussian 좌표의 절대 일차 모멘트는
E|Z_i|=sqrt(2*tau/pi)이므로 그 적분은 3 Vol(B) L sqrt(2*tau/pi) 이하이다.

남은 질량 손실은 정확히

\[
\int_B\left(1-\int_B D_\tau(x-y)\,dy\right)dx
=\mathbb E[\operatorname{Vol}(B)-\operatorname{Vol}(B\cap(B+Z))].
\]

변 길이를 ell_i, d_i=min(|Z_i|,ell_i)로 쓰면 overlap은 product_i(ell_i-d_i)다.
그 차이는

\[
d_1\ell_2\ell_3+(\ell_1-d_1)d_2\ell_3
+(\ell_1-d_1)(\ell_2-d_2)d_3
\leq\sum_i |Z_i|\prod_{j\ne i}\ell_j.
\]

같은 Gaussian shift를 한 번 평균하므로 양쪽 면이라는 이유로 2를 다시 곱하지 않는다.
ell=(3/2,3,7/4)에서 Vol(B)=63/8, sum_i product_{j ne i}ell_j=99/8이다. 따라서

\[
\boxed{\left|\mathcal B_\tau[u,v]-\int_B A(q,q)\,dq\right|
\leq \left({189\over8}L+{99\over8}M_0\right)\sqrt{2\tau/\pi}.}
\tag{2}
\]

이는 선택한 시험함수 쌍마다 실제 pairing의 수렴을 보인다. 경계 한 점에서 Gaussian
질량이 절반으로 보이는 현상은 전체 적분에 1/2를 남기지 않는다: boundary layer의
체적 효과가 위 식에서 0으로 간다. 개별 delta/delta-prime face 항을 따로 극한으로
옮기거나 상쇄 전에 각각 유한하다고 가정하지 않았다.

## 3. 극한에서 남는 경계형식

직접 미분하면

\[
(Hu)v-u(Hv)
=\partial_a\{f(u\partial_av-v\partial_au)\}
+\partial_\phi\{b(u\partial_\phi v-v\partial_\phi u)\}.
\]

W는 대각 적분에서 정확히 상쇄된다. 유한 tau의 off-diagonal potential 차이는
상쇄된다고 가정하지 않았으며 식 (2)의 오차에 포함된다.
시험함수의 지지 조건과 FTC를 적용하면

\[
\boxed{\lim_{\tau\downarrow0}\mathcal B_\tau[u,v]
=f(2)\int (u\partial_av-v\partial_au)|_{a=2}\,d\phi\,dN,\qquad
f(2)=-{1\over48\pi^2}.}
\tag{3}
\]

이 부호는 upper-a outward face와 식 (1)의 순서에 해당한다.
u와 v를 바꾸면 부호가 뒤집힌다. 모든 면 근방에서 0인 interior test pair는
식 (3)이 0이 된다. 따라서 interior weak removal과 nonzero cutoff-face limit은 양립한다.

## 4. C-infinity 비영 예시와 경계조건 대조

명시적 smooth cutoff를 구성할 수 있다. E(t)=exp(-1/t) for t>0, E(t)=0 otherwise,
S(t)=E(t)/(E(t)+E(1-t))로 둔다. eta(a)=S(4a-6)S(10-4a)는
[3/2,5/2]에 지지되고 [7/4,9/4]에서 1이다.
psi는 E(1-4 phi^2)E(1-16(N-1)^2)를 양의 L2 norm으로 나눈 함수다.
그 지지는 phi in [-1/2,1/2], N in [3/4,5/4]이며 integral psi^2=1이다.

u=eta(a)psi(phi,N), v=(a-1)eta(a)psi(phi,N)를 택하면 a=2의 jets는
(u,u_a,v,v_a)=psi*(1,0,1,1)이다. 따라서

\[
\boxed{\mathcal B_0[u,v]=-{1\over48\pi^2}\ne0.}
\]

이 값은 이전 off-diagonal defect/Gaussian 비율 -3*pi^2/8과 다른 객체다.
이번에는 명시한 시험함수에 적분한 경계 극한이다. psi의 L2 정규화는 진단 convention이며
물리적 확률이나 physical Hilbert product를 정한 것이 아니다.

대조는 같은 정리의 다른 시험함수 쌍이다.

- Common Dirichlet: u_D=(a-2)eta psi, v_D=(a-2)^2 eta psi이면 두 경계값이 0이고 flux=0.
- Common real Robin: u_R=exp(r(a-2))eta psi,
  v_R=(1+(a-2)^2)exp(r(a-2))eta psi이면 r in R에 대해
  u_a=r u, v_a=r v at a=2이므로 flux=0.

Robin 쌍은 동일한 함수 두 개를 사용한 자명한 antisymmetry 검사가 아니다.
이 대조는 각 경계조건 안에서의 쌍선형 소거이며, Dirichlet과 Robin이 같은 물리 이론이라는
가정도, 이 조건을 선택해야 한다는 물리적 유도도 아니다.

## 5. 검증과 재사용 범위

주된 위험은 sign/unit 및 distribution-domain 혼동이다. 관련 control 세 묶음만 사용한다:
formal transpose/Green 부호와 ghost dual; Gaussian moment/box overlap와 수렴 상수;
비영 witness 및 Dirichlet/Robin 경계 jet 대조.

Runner는 직접 symbolic operator differentiation과 Gaussian moment 적분, overlap algebra,
ghost coefficient 및 boundary jets를 검사한다. Lean은 다섯 개의 finite real boundary-jet
정리만 검증한다. 식 (1)--(3)의 분포·해석적 증명은 이 문서이며 Lean에서 형식화되지 않았다.
독립 수학 읽기 감사가 pairing, overlap bound, orientation 및 witness를 확인했다.
아직 계산을 실행하지 않은 이 문서는 실제 실행의 성공 표시가 아니다. 실제 출력은
STAROBINSKY_WARD_FACE_LIMIT_RESULT.json와 인접 완료 보고서가 기록한다.

[CMR의 BV-BFV 경계 상태·gluing](https://arxiv.org/html/1507.01221#S2.SS3)은 경계
연산자·상태·측도를 함께 맞춰야 한다는 방법 문맥이다. 그 시공간 경계와 여기의 a=2
field-coordinate cutoff를 동일시하지 않으며, 그 논문을 식 (3)의 증거로 사용하지 않는다.
원래 Starobinsky convention의 계보는
[polynomial BFV chart](STAROBINSKY_POLYNOMIAL_BFV_CHART.md)에 남아 있다.

다른 면, complex sesquilinear physical product, self-adjoint extension, 경계 선택의 물리적
동등성, bulk BFV source, N=0 contact, 원래 relative cycle, Big Bang 및 TOE는 해결하지 않았다.
