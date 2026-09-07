# 실제 compact-test complex의 degree-reversed dual과 seam pairing

2026-09-07 · SUPPORTING_METHOD · 해석적/대수적 유도.

질문: compact-test BFV complex의 올바른 graded dual에서 top-ghost detector와
evaluation seam pairing은 무엇이며, 이전 coefficient-only dual의 소거와 어떻게 다른가?
출력: degree-reversed algebraic dual complex, Ward 부호, top detector 판별식.
비주장: 양의 물리 내적, anti-linear CPT, self-adjoint realization, BFV quantum kernel,
original integration cycle 또는 G1 해소를 구성하지 않는다.

## 1. 실제 three-term compact-test complex

고정한 repaired carrier \(\Phi\)에서 \([H,p_N]=0\)이고 \(H\Phi,p_N\Phi\subset\Phi\)다.
선택 ghost order \(c\rho\)에 대해

\[
C^0=\Phi,\qquad C^1=\Phi\oplus\Phi,\qquad C^2=\Phi,
\]
\[
q_0u=(Hu,p_Nu),\qquad q_1(x,y)=Hy-p_Nx.
\tag{1}
\]

따라서 \(q_1q_0=Hp_N-p_NH=0\). 여기서 \(x\)는 \(c\)-coefficient, \(y\)는
\(\rho\)-coefficient다. 이 규약은 앞선 `STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_DERIVATION.md`의
\(c\rho(Hy-p_Nx)\)와 같다.

이전 coefficient-only algebraic dual은 같은 ghost degree를 유지한 별도 대상이었다.
그곳에서 top class가 사라졌다는 결과는 아래의 graded dual에 대한 결과가 아니다.

## 2. 차수를 뒤집은 dual complex와 Ward 부호

algebraic dual을 \(X^*=\operatorname{Hom}_{\mathbb C}(X,\mathbb C)\)로 두고

\[
D^0=(C^2)^*,\qquad D^1=(C^1)^*,\qquad D^2=(C^0)^*,
\]
\[
\delta_0=q_1^t,\qquad \delta_1=-q_0^t.
\tag{2}
\]

로 정의한다. 본문의 D 차수 0,1,2는 실제 dual 차수 −2,−1,0을 +2로 표시한
bookkeeping이다. Physical ghost degree를 바꾸지 않는다. Primal-first evaluation의
Ward 규약으로 differential 부호를 선택했다. 표준 Hom differential
\(d_{\mathrm{Hom}}\lambda=(-1)^{|\lambda|+1}\lambda q\)와는 전체 부호가 반대이며,
각 degree의 \((-1)^{|\lambda|}\) 사상으로 isomorphic하다.
그러면 \(\delta_1\delta_0=-(q_1q_0)^t=0\)다. Evaluation pairing의
두 Ward 항등식은

\[
(\delta_1\lambda_1)(u)+\lambda_1(q_0u)=0,
\qquad
\lambda_2(q_1v)-(\delta_0\lambda_2)(v)=0.
\tag{3}
\]

이다. 이것이 이 선택의 부호를 고정한다.

Berezin bookkeeping으로 primal element
\(u+c x+\rho y+c\rho z\)와 dual tuple
\((\lambda_2,\lambda_c,\lambda_\rho,\lambda_0)\)의 pairing은

\[
\langle -, -\rangle_\mathrm{ev}
=\lambda_2(z)+\lambda_c(x)+\lambda_\rho(y)+\lambda_0(u).
\tag{4}
\]

로 둔다. 형식적으로 dual polynomial을

\[
\lambda_2+c\lambda_\rho-\rho\lambda_c+c\rho\lambda_0
\]

로 쓰고 **이 dual polynomial을 왼쪽에**, primal polynomial을 오른쪽에 곱한 뒤
\(\int d\rho\,dc\;c\rho=1\)을 택하면 식 (4)의 coefficient가 나온다.
Dual coefficient의 evaluation은 해당 primal coefficient에 적용한다.
Ghost polynomial의 degree는 위 D의 bookkeeping이고, physical dual degree는 −2를 더한다.
이는 complex **bilinear** evaluation이다. 켤레, 양의성, orientation/CPT lift를 넣지 않았다.

## 3. 실제 \(T_g\)는 top-boundary detector다

Neumann Cauchy dual functional은 \(T_gH=T_gp_N=0\)이다. 식 (1)에서

\[
T_gq_1(x,y)=T_g(Hy-p_Nx)=0.
\tag{5}
\]

따라서 \(T_g\in D^0\)는 \(\delta_0\)-closed다. \(D^{-1}=0\)이므로 \(T_g\ne0\)이면
그 graded-dual class는 nonzero다. 또한 \(T_g(z)\ne0\)인 \(z\in C^2\)가 있으면
\(z\notin\operatorname{im}q_1\)이다. 실제로 interior compact bump에서 만든 previous
nonzero witness를 \(z\)로 쓸 수 있다.

더 일반적으로 finite label space \(E\), \(R:C^2\to E\), section \(J:E\to C^2\)와
\(RJ=I\)가 있고, \(\lambda R\)가 \(\delta_0\)-closed라면

\[
(\lambda R)(Je)=\lambda e.
\tag{6}
\]

이다. \(\lambda e\ne0\)이면 \(Je\)는 top boundary가 아니다. 이는 finite Gram section의
정확한 pairing 역할을 기록할 뿐, 그 section이 physical observable 또는 complete state
space라는 뜻은 아니다. [실제 primary contraction](STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md)의
R_N에 대해서는 T_g=t_gR_N이므로 축소 전후 evaluation이 정확히 보존된다.

## 4. descent와 남는 작업

식 (3)은 pairing이 cohomology에 내려가기 위한 algebraic Ward 조건이다. 비퇴화성은
전체 algebraic dual을 쓸 때 quotient-separation으로 따로 논할 수 있지만, 현재 실제
\(T_g\) family가 \(H^2(C)\) 전체를 분리하는지는 아직 보이지 않았다. 위 결과는 그 family가
적어도 명시한 top classes를 검출한다는 방향만 준다.

이 complex는 compact-test carrier의 것이다. coefficient-only dual, closed self-adjoint
\(p_N\) domain, BV--BFV boundary state module은 서로 다른 대상이다. 특히 \(D^2=(C^0)^*\)
에 물리 state degree를 임의로 부여하거나, 식 (4)를 positive metric/CPT sewing이라고
해석하지 않는다. 실제 quantum sewing에는 graded boundary fields, ghost/orientation action,
seam kernel, residual BV data와 mQME/pushforward가 계속 필요하다.

## 5. 형식 검증 경계

`GradedDualSewing.lean`은 (2)–(3), closed detector의 boundary 판별, finite section evaluation을
일반 complex-linear maps로만 검증한다. actual \(T_g\)의 PDE/Green 구성, finite Gram bump
section, carrier topology 및 physical interpretation은 이 유도문에 남는다. 새 runner의 raw
result가 생기기 전까지 이 문서는 실행 성공 기록이 아니다.
