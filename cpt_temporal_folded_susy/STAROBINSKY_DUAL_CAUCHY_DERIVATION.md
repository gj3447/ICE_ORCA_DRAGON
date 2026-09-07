# 실제 Weyl 제약의 Neumann Cauchy 쌍대 해와 내적 판별

2026-09-07 · SUPPORTING_METHOD · 해석적 유도 정본.

질문: 같은 repaired 시험공간의 쌍대에서 H와 p_N을 동시에 소거하는 비영 해를
구성하고, 그 해에 자연 KG 내적 또는 명시한 양의 form을 줄 수 있는가?
출력: Neumann Cauchy data로 정의한 쌍대 해족과 그 두 form의 판별.
비주장: 선택된 물리적 Hilbert 공간·RAQ·full CPT/BFV 접합·original cycle을 구성하지 않는다.

사전 planner는 INSUFFICIENT_ROUTE_EVIDENCE였다. 직접 줄이는 질문은
open:starobinsky-seam-ward-boundary-state-limit의 simultaneous dual-state 존재 부분이다.
G1의 source-defined original class와 signed global intersections를 주지 않으므로
G1→G2→G3→G4→G5→full-theory/empirical review의 core 진전은 아니다.
Choice-invariance path를 읽었으며 여기서 선택한 Neumann condition, seed 및 form이
같은 물리 내용을 나타내는 허용 선택군이라는 증명은 없다.

## 1. 실제 operator와 시험공간

[기존 state-criterion audit](STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md)의
B=[1/2,2]×[-1,2]×[1/4,2], flat density, hbar=1, Weyl ordering을 유지한다.
이번에는 r=0을 명시적으로 선택한다. 이것은 CPT가 선택해 준 조건이 아니다.

\[
H=-\partial_a(f\partial_a)-b\partial_\phi^2+W,\quad
f=-\frac1{24\pi^2a},\quad b=\frac1{4\pi^2a^3},\quad W=U-f''/4,
\]
\[
U=-6\pi^2a+\frac32\pi^2a^3(1-e^{-\beta\phi})^2,\qquad
\beta=\sqrt{2/3},\qquad p_N=-i\partial_N.
\]

Φ는 모든 a=2 이외 face 근방에서 0인 ambient complex smooth 함수의 B 제한 중
∂_a(H^k p_N^m u)|₂=0 for every k,m≥0인 함수다. 이전과 같은 repaired carrier의
Neumann 경우다. HΦ⊂Φ와 p_NΦ⊂Φ, interior C_c^∞(B°)⊂Φ는 이전 유도에 따른다.
Degree-zero minimal test cohomology가 0이라는 이전 결론은 그대로 유지한다.

## 2. 정확한 Cauchy 문제로 해를 구성한다

x=log a, s(a,φ)=aχ(x,φ)로 쓰면 직접 미분으로

\[
24\pi^2a^2 H[a\chi(\log a,\phi)]
=P\chi=\chi_{xx}-6\chi_{\phi\phi}+V(x,\phi)\chi,
\]
\[
V=-\frac12-144\pi^4e^{4x}
+36\pi^4e^{6x}(1-e^{-\beta\phi})^2.
\tag{1}
\]

Weyl correction은 정규형의 −1/2에 기여한다. LB ordering의 Morse 결과를
가져오거나 potential을 버리지 않았다. 이 변환은 방정식의 정확한 재표현이며
quantum inner product의 unitary equivalence를 주장하지 않는다.

열린 전체 R_x×R_φ에서 metric −dx²+dφ²/6을 쓰면 P의 principal part는
normally hyperbolic scalar wave operator다. V는 실수 smooth lower-order coefficient다.
각 x=constant는 spacelike Cauchy surface다. 따라서
[Bär–Ginoux–Pfäffle, Theorem 3.2.11](https://arxiv.org/pdf/0806.1036v1)의 존재·유일성과
finite propagation을 적용할 수 있다. 닫힌 slab를 boundary 없는 manifold라고 놓고
적용한 것이 아니라 열린 globally hyperbolic extension에서 풀고 slab에 제한한다.

x₂=log 2, g∈C_c^∞((-1,2);C)에 대해

\[
\chi(x_2,\phi)=g(\phi)/2,\qquad
\chi_x(x_2,\phi)=-g(\phi)/2
\tag{2}
\]

라는 compact smooth Cauchy data와 Pχ=0을 준다. 유일 smooth 해를 χ_g라 하고
s_g=aχ_g로 두면 Hs_g=0, s_g(2,φ)=g(φ), ∂_a s_g(2,φ)=0이다.
실수 g에는 유일성에 의해 실수 s_g가 대응한다. 또한

\[
\operatorname{supp}s_g(a,\cdot)
\subset\operatorname{supp}g+[-\sqrt6|\log(a/2)|,\sqrt6|\log(a/2)|].
\]

a∈[1/2,2]에서 이 폭은 √6 log 4 이하라 finite causal region은 compact하다.
V가 φ→−∞에서 무한히 커져도 이 compact region에서는 smooth bounded coefficients다.
해가 φ-box 밖으로 전파되는 것은 허용한다. 시험함수가 φ faces 근방에서 0이기
때문에 아래 B 위 dual pairing에 그 해를 사용할 수 있다. a=0 극한은 다루지 않는다.

이 구성은 명시한 Cauchy problem으로 해를 유일하게 정의하는 해석적 구성이다.
닫힌 특수함수 표현이나 수치 PDE solution array를 계산했다고 보고하지 않는다.

## 3. 같은 Φ의 비영 simultaneous dual functional

N과 무관하게 s_g를 연장하고, complex-linear functional

\[
T_g[u]=\int_B s_g(a,\phi)u(a,\phi,N)\,da\,d\phi\,dN
\tag{3}
\]

를 정의한다. 유한 B에서 s_g는 smooth bounded이므로 이 함수는 보조 L² norm에도
연속이다. 대표는 bar(s_g)이지만 N-collar 조건을 만족하지 않으므로 일반적으로 Φ의
원소는 아니다.

H는 flat measure에서 formally self-transpose다. Hs_g=0 및 Green identity를 쓰면
T_g[Hu]는 경계형식뿐이다. Lower-a와 두 φ faces는 u의 collar 조건으로 0이고,
upper-a에서는 u_a=s_g,a=0이므로 0이다. N 미분에는 u의 N-collar 조건을 쓴다.

\[
\boxed{T_g[Hu]=0,\qquad T_g[p_Nu]=0\quad (u\in\Phi).}
\tag{4}
\]

g≠0이면 s_g는 upper face 바로 안쪽에서도 비영이다. 그 작은 내부 영역에서
u=bar(s_g)ζ, ζ≥0인 비영 smooth compact bump를 택하면 u∈C_c^∞(B°)⊂Φ이고
T_g[u]=∫|s_g|²ζ>0이다. 더 나아가 T_g=0이면 interior tests에 대한 분포가 0이라
s_g=0 on B°, smooth trace g=0이다. 따라서 g↦T_g는 injective complex-linear map이다.
이는 infinite-dimensional simultaneous dual-solution family이며 physical BRST product는 아니다.

## 4. 이 해족의 KG form은 모두 0이다

실수 V에 대해 j_x=bar(χ₁)χ₂,x−bar(χ₁,x)χ₂는
∂_x j_x=6∂_φ[bar(χ₁)χ₂,φ−bar(χ₁,φ)χ₂]를 만족한다.
Finite propagation과 compact Cauchy data로 전체 R_φ 적분의 lateral term은 0이다.
따라서

\[
J(\chi_1,\chi_2)=i\int_{\mathbb R}j_x\,d\phi
\]

는 x에 무관하다. 식 (2)의 terminal data는 χ_x=−χ라서 J=0이다. 따라서
**이 Neumann 해족 위 KG form은 모든 쌍에서 0**이고 그 form으로 비영 해를 정규화할 수 없다.
일반적인 common real Robin r에서도 χ_x=(2r−1)χ라 같은 terminal 소거가 성립한다.
Conservation은 전체 R_φ 적분에 대한 것이다. 유한 φ-box에 해를 잘라 놓고 lateral
flux가 없다고 가정하지 않았다. 이 결과는 다른 polarization/positive-frequency construction을
배제하거나 모든 positive product의 부재를 뜻하지 않는다.

## 5. 선택한 rank-one positive form은 만들 수 있지만 물리적 선택은 아니다

E(t)=e^{−1/t} for t>0, 0 otherwise로 두고 실수 seed
g₀(φ)=E(1−4φ²)를 고정한다. T=T_{g₀}로 놓으면

\[
F_T(u,v)=\overline{T[u]}T[v]
\tag{5}
\]

는 Hermitian positive semidefinite이고 두 slot에서 H,p_N을 소거한다.
Kernel은 ker T이며, T≠0이므로 Φ/ker T→C, [u]↦T[u]는 positive one-dimensional
inner-product space와의 isometric isomorphism이다. 이는 선택한 rank-one quotient다.

K:u→bar(u)에 대해 real s_{g₀} 때문에 T[Ku]=bar(T[u])다. 따라서 K는 quotient에서
complex conjugation으로 내려가는 antiunitary involution이다. 이것은 **kinematic K**이며
ghost와 양쪽 boundary orientations를 포함한 full CPT lift가 아니다.

이 양의 form은 비정준적이다. λ>0에 대해 λF_T도 가능하며, 또 다른 실수 seed
g₁=φg₀는 g₀와 독립이고 §3의 injectivity로 T_{g₁}도 독립이다. 대응하는 두 rank-one
forms는 kernel부터 다르다. Positivity와 K covariance만으로 seed나 정규화가 선택되지 않는다.

식 (5)를 RAQ rigging map이라고 승격하지 않는다. 고정한 observable-* algebra와의
intertwining, constraint self-adjoint realizations, group averaging, ghost product,
bulk/seam kernel 및 physical interpretation을 제공하지 않았기 때문이다.
[Giulini–Marolf §II](https://arxiv.org/html/gr-qc/9812024)의 조건은 이 남은 구별의 문헌 근거다.
CMR의 residual BV fields, modified QME 및 gluing obligations도 기존 audit대로 남는다.

## 6. 검산과 출처 경계

주된 실패원인은 `inference`: dual solution과 임의의 positive form을 물리적 선택으로
오인하는 것이다. 관련 control 세 묶음은 실제 Weyl의 coordinate/conjugation 변환,
Green/Neumann 및 전체 φ current, rank-one positivity와 K/nonuniqueness 대조다.

Runner는 미분·jet·복소 coefficient identities만 검사한다. Lean은 finite rank-one
Hermitian/positive/kernel/K identities만 검증한다. PDE 존재·유일성, finite propagation,
dual injectivity와 quotient 해석은 이 문서 및 primary Cauchy theorem을 이용한 해석적
증명이며 Lean에 형식화되지 않았다. 독립 수학 검토에서 방정식 변환, dual boundary terms,
KG degeneracy와 rank-one scope를 대조했다.

Primary theorem: C. Bär, N. Ginoux, F. Pfäffle, *Wave Equations on Lorentzian
Manifolds and Quantization*, arXiv:0806.1036v1, Theorems 3.2.11–12, printed p.85–87.
Discovery 명령은 `./ice literature search "normally hyperbolic Cauchy problem compactly supported smooth data finite propagation conserved symplectic current complex structure Lorentzian" --json`,
UTC 2026-09-07T06:45:05.371Z이며 해당 primary theorem을 직접 읽었다.
이 일반 PDE 정리는 새로운 물리 발견으로 주장하지 않는다.

실제 실행·환경·입력 hashes와 체크는 `STAROBINSKY_DUAL_CAUCHY_RESULT.json`에 남긴다.
아직 실행하지 않은 이 유도문 자체는 검증 성공 기록이 아니다.
