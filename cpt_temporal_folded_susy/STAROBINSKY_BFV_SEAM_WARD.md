# Starobinsky 양자 경계 접합: Gaussian 규제의 Ward defect

2026-09-07 · **SUPPORTING_METHOD / SCOPED_NEGATIVE_RESULT**.

[이전 제안](../docs/research/ICE_BFV_CPT_SEAM_WARD_SOURCE_PROPOSAL_2026-09-07.md)의 양자 경계
pairing을 하나 명시하고 BRST 잔여항을 도출했다. 선언한 좌표 Gaussian은 **모든 τ>0에서
정확한 BFV-closed seam이 아니다.** 같은 모형 안의 witness에서 잔여항/Gaussian은
−3π²/8이다. 기호 검산 **23/23**, Lean 정리 **7개**가 통과했다. 선택한 box의 두 copy에
대해 a,φ,N의 하한/상한 **12개 face**에 해당하는 delta와 delta-prime 계수도 기록했다.

질문은 유한 폭 Gaussian이 선언한 Starobinsky boundary BRST charge에 대해 닫히는가다.
이 결과는 그 후보를 배제한다. Full time-sliced bulk source, physical CPT,
self-adjoint realization, original relative class 또는 G1 해소라는 주장은 하지 않는다.
사전 planner도 `INSUFFICIENT_ROUTE_EVIDENCE`였으며 supporting으로 구현했다.

## 1. 실제로 정의한 경계 객체

기존 homogeneous Lorentzian Starobinsky H_L을 사용하되 양자화는 **flat bosonic density와
Weyl ordering, ℏ=1**로 선언한다. 이는 모델링 입력이며 유일한 physical ordering이 아니다.

\[
f(a)=-\frac1{24\pi^2a},\quad b(a)=\frac1{4\pi^2a^3},\quad
U(a,\phi)=-6\pi^2a+\frac32\pi^2a^3(1-e^{-\beta\phi})^2,
\quad\beta=\sqrt{2/3},
\]
\[
\widehat H_W=-f\partial_a^2-f'\partial_a-\frac14f''-b\partial_\phi^2+U,
\qquad\widehat\Omega_i=c_i\widehat H_{W,i}-i\rho_i\partial_{N_i}.
\]

Polarization은 (a,φ,N;c,ρ)다. Conjugate momenta는 미분 연산자로 표현한다.
Momentum matching delta를 별도로 곱하지 않는다. 각 copy의 실수 범위는
D=[1/2,2]×[−1,2]×[1/4,2]이며 χ_i는 그 hard indicator다.

\[
D_\tau=(2\pi\tau)^{-3/2}
\exp\!\left[-\frac{(a_1-a_2)^2+(\phi_1-\phi_2)^2+(N_1-N_2)^2}{2\tau}\right],
\quad g=(c_2+c_1)(\rho_2-\rho_1),
\]
\[
\boxed{K_\tau=\chi_1\chi_2D_\tau\,g.}
\]

τ>0는 선언한 reduced coordinate units에서의 smoothing width다. Gaussian은 R³에서
정규화한 것을 사용하며 box 경계 근처에서 다시 나누어 정규화하지 않는다. 모든 odd
변수는 하나의 graded exterior algebra에 속하고 순서는 (c₁,c₂,ρ₁,ρ₂)다.

Berezin fiber 적분은 **∫dρ₂ dc₂[A(c₁,ρ₁)c₂ρ₂]=A(c₁,ρ₁)**로 선언했다. 독립적인
bit-mask exterior multiplication으로 1,c₂,ρ₂,c₂ρ₂의 네 기저를 적분하여 각각
1,−c₁,ρ₁,−c₁ρ₁을 얻는지 검사했다. 따라서 선택한 ghost pullback을 실제로 구현한다.
이것은 특정 boundary measure 규약이며 중력의 absolute determinant line을 만들지 않는다.

## 2. 양자 Ward 식과 정확한 interior 반례

전체 graded algebra에서는 c₂g=−c₁g, ρ₂g=ρ₁g다. 따라서 F=χ₁χ₂Dτ에 대해

\[
(\widehat\Omega_1+\widehat\Omega_2)(Fg)
=c_1g(\widehat H_1-\widehat H_2)F
-i\rho_1g(\partial_{N_1}+\partial_{N_2})F.
\tag{1}
\]

c₁g는 0이 아니다. Copy-2 ghosts를 commuting 변수로 처리하면 이 식을 얻지 못한다.
Lean은 명시적인 degree-1/2/3 exterior coefficient table에서 이 factorization과
nonzero ghost coefficient를 검증한다. Gaussian의 실제 미분은 SymPy가 수행한다.

x=a₁−a₂, y=φ₁−φ₂로 두면 box interior에서 primary derivative는 0이고,

\[
\frac{(\widehat H_1-\widehat H_2)D_\tau}{D_\tau}
=-(f_1-f_2)(x^2/\tau^2-1/\tau)+(f'_1+f'_2)x/\tau
-\frac14(f''_1-f''_2)
-(b_1-b_2)(y^2/\tau^2-1/\tau)+(U_1-U_2).
\tag{2}
\]

이는 예측식을 입력해 0이라고 기록한 것이 아니다. 양쪽 H를 실제 Gaussian에
각각 미분 적용한 식과 (2)의 차이를 정확히 검사했다.

\[
a_1=a_2=1,\quad\phi_1=0,\quad\phi_2=\log 2/\beta,\quad N_1=N_2=1
\]

을 대입하면 kinetic coefficient 차이가 모두 사라져

\[
\boxed{(\widehat H_1-\widehat H_2)D_\tau/D_\tau=-3\pi^2/8\ne0}
\tag{3}
\]

가 된다. 이 점은 D×D의 interior다: 0<log 2<1, β>1/2이므로 0<φ₂<2다.
Dτ>0이므로 모든 양의 τ에서 실제 smooth interior defect가 비영이다. 상자의 경계에만
지지되는 항으로 이 interior 결함을 상쇄할 수 없다. Constant-coefficient/no-potential
대조에서는 동일 Gaussian의 Hamiltonian 차이가 정확히 0이었다. 이 대조 모형을 ICE
evidence로 이식하지 않았다.

(3)은 τ→0 분포 극한을 배제하지 않는다. 고정된 off-diagonal witness의 Gaussian 자체는
그 극한에서 작아진다. 유한 τ의 exact closure와 compact-test distributional convergence는
다른 주장이다. 특정 Gaussian 실패를 모든 regulator나 BFV source의 불가능성으로 확대하지 않는다.

## 3. cutoff terms를 실제 face에 옮겼다

한 copy의 smooth window χ에 대한 정확한 commutator는

\[
[\widehat H,\chi]D_\tau
=-fD_\tau\chi_{aa}-(2f\partial_aD_\tau+f'D_\tau)\chi_a
-bD_\tau\chi_{\phi\phi}-2b\partial_\phi D_\tau\chi_\phi.
\tag{4}
\]

χ_x=sδ(x−x_b), χ_xx=sδ′(x−x_b), 하한 s=+1·상한 s=−1을 대입한다.
A(x)δ′_b=A(x_b)δ′_b−A′(x_b)δ_b를 사용하면 f′ 항이 소거되어, a face의 canonical
계수는

\[
-o_i s f(a_b)\left[D_\tau|_{a_b}\,\delta'_{a_b}
+(\partial_{a_i}D_\tau)|_{a_b}\,\delta_{a_b}\right],
\quad o_1=+1,\ o_2=-1.
\tag{5}
\]

φ face도 f→b와 a→φ로 같다. 여기에 c₁g와 다른 다섯 좌표의 indicator를 곱한다.
N face는 전체 −iρ₁g를 인수로 하여 sDτ|_{N_b}δ_{N_b}다. 다른 좌표의 indicator와
normal delta는 서로 다른 변수의 tensor-product distribution으로 해석한다.
교차 미분항이 없으므로 별도의 corner delta-product 항은 도출되지 않는다.

[Raw result](STAROBINSKY_BFV_SEAM_WARD_RESULT.json)의
`symbolic.defect.box_face_ledger`에는 12개 face의 **실제 위치를 대입한 계수**가 있다.
최종 cutoff Ward 식은 (2)의 χ₁χ₂ interior 항과 이 ledger의 합이다.

하한 N=1/4 face는 N=0 contact가 아니고, 상한 N=2 face는 무한대가 아니다.
여기에는 시간 진화 kernel과 short-time identity가 없으므로 positive-lapse Green의
contact, 전체 lapse 적분, fixed-time composition을 검증했다고 쓰지 않는다.

## 4. 원래 delta seam과 무엇이 다른가

Smooth compact interior test functions에서 H_W는 formally symmetric다. 직접 검산한
Green identity는 wHz−zHw=∂_a[f(z∂_aw−w∂_az)]+∂_φ[b(z∂_φw−w∂_φz)]다.
따라서 **형식적 distribution pairing**인 δ(q₁−q₂)g는 interior에서 (1)에 대해 닫힌다.
이는 a=0의 self-adjoint domain이나 physical Hilbert space를 선택한 정리가 아니다.
이번 작업은 그 delta를 유한 좌표 Gaussian으로 바꾸면 정확한 intertwining을 잃는다는
차이를 직접 계산한 것이다.

[Cattaneo–Mnev–Reshetikhin §2.4.4](https://arxiv.org/html/1507.01221#S2.SS4.SSS4)는
polarization, 경계 pairing 및 residual-field pushforward가 맞물려야 한다는 방법 근거다.
그 논문의 섭동적 gluing 결과를 이 finite Gaussian의 closure 증거로 사용하지 않았다.
H_L의 원래 convention은 [polynomial BFV chart 보고서](STAROBINSKY_POLYNOMIAL_BFV_CHART.md)에 있다.

## 5. 실행·검증과 정확한 남은 객체

```text
./ice run starobinsky_bfv_seam_ward
SCOPED_GAUSSIAN_SEAM_HAS_NONZERO_BFV_WARD_DEFECT
exact controls: 23; Lean theorems: 7
finite-width witness: (H1-H2)D_tau / D_tau = -3*pi**2/8
cutoff faces retained; full trajectory and original relative cycle remain open
```

실제 exit 0, elapsed 4.055415472947061 s, source commit
`ce7b8c5fe711712c2f107ac08481cfed8bad6a72`다. Python/SymPy version, Lean 4.33.0 및
mathlib pin, source hash, 모든 symbolic check와 Lean theorem type/axiom 출력은 raw가 정본이다.

최초 실행은 두 실수 potential 정의의 `noncomputable` annotation 누락으로 실패했다.
실패 raw는 `c2213b3`에 보존했고, annotation 수정 뒤 22 checks/7 theorems가 통과했다.
최종 읽기 검토에서 일반 window 식을 실제 12개 box face의 canonical 계수로 완성했고,
현재 최종 실행은 23 checks/7 theorems를 통과했다. 실패를 tolerance로 숨기지 않았다.

[Lean source](../formal/cpt_sewing/CptSewing/SeamWard.lean)는 ghost coefficient algebra,
diagonal lapse-shift identity와 y=exp(−βφ) potential coefficient의 증명이다. Gaussian
미분, 분포 연산, continuum BFV를 Lean에서 증명한 것은 아니다. 현재 proof source를
새로 elaborate하고 각 theorem의 공리 의존성을 검사했으며 표준 propext/Classical.choice/
Quot.sound만 허용했다. Imported compiled dependencies는 기존과 같은 신뢰 기반이다.
[Runner](starobinsky_bfv_seam_ward.py)는 별도 bit-mask algebra와 SymPy 미분을 사용한다.

주된 실패 위험은 gauge다. 대조는 (i) graded/Berezin 및 wrong-sign control,
(ii) 직접 미분·Green identity·실제 cutoff face 계수,
(iii) potential-bearing 정확한 반례와 constant-coefficient control이다.
독립 읽기 검토로 각 부호와 적용 범위를 확인했다.

재사용할 출력은 **명시한 boundary pairing과 실패하는 regulator의 정확한 Ward 식**이다.
Named consumer는 `open:gate1-starobinsky-finite-m2-replacement-bfv-source`의 boundary-kernel
입력이다. 실제 finite bulk source, continuum-compatible element, zero-lapse contact,
BRST-compatible regulator와 original joint relative class는 계속 미해결이다.
다음 source에서 이 Gaussian을 그대로 exact BFV seam으로 채택할 수 없다는 좁은 결론이다.
