# Phase 18 — temporal seam은 자유 Wess–Zumino pole을 갈라놓는가?

## 결과부터

이번 Phase의 답은 명확한 **null result**다.

\[
\boxed{
 m_{B,\mathrm{pole}}^2=m_{F,\mathrm{pole}}^2=m^2,
 \qquad
 \Delta m_{\mathrm{pole}}^2=0
}
\]

단, 이것은 아래에 동결한 자유이론·국소 seam 범위 안의 정리다. \(t=0\)에만 지지된
유한한 quadratic canonical sewing은 나가는 상태의 occupation과 anomalous correlation을
바꿀 수 있고 그 상태는 SUSY가 아닐 수 있다. 그러나 \(t>0\) bulk의 운동방정식이 그대로라면
retarded spectral pole은 옮기지 못한다.

따라서 다음 두 문장은 동시에 참이다.

\[
\boxed{\text{seam은 state/domain 수준에서 SUSY를 깰 수 있다}}
\]

\[
\boxed{\text{그 사실만으로 영구적인 superpartner 질량분열은 생기지 않는다}}
\]

이 계산은 “시간의 흐름이 SUSY를 깬다”는 주장을 반박하고, 더 좁은 질문인 “한 번의
temporal seam이 자유 particle spectrum을 갈라놓는가?”에도 **아니오**라고 답한다. 그러므로
현재 단계에서 SUSY 비관측을 설명했다고 말할 수 없다. 다음 비자명한 계산은 interacting
Schwinger–Keldysh self-energy와 지속적인 order parameter가 있는 경우다.

실행체는
[`phase18_gaussian_seam_spectrum.py`](phase18_gaussian_seam_spectrum.py)이며, 고정된 SymPy
환경에서 47개의 exact check와 별도 SciPy 수치 적분 control 1개를 통과한다.

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py
```

관측 결과:

```text
47 exact PASS
1 numerical PASS
PHASE18_RESULT={..."delta_m_pole_squared":"0"...}
```

## 1. 무엇을 증명했고 무엇을 증명하지 않았는가

### 동결 가정

정리의 범위는 다음 여섯 조건이다.

1. \(t\neq0\) bulk는 \(3+1\)차원 flat spacetime의 free equal-mass Wess–Zumino mode다.
   복소 scalar와 Weyl/Majorana fermion의 공통 질량은 \(m>0\)이다.
2. seam은 standard Cauchy data에 작용하는 \(t=0\)의 순간적 유한 quadratic map이다.
   Energy-dependent/time-nonlocal kernel과 higher-time-derivative extra data는 제외한다.
3. scalar Cauchy-data map은 symplectic이고 finite-mode fermion Nambu map은 CAR-unitary다.
4. seam 뒤 \(t>0\)의 kinetic operator와 bulk mass parameter는 바뀌지 않는다.
5. 미래까지 남는 seam field, memory kernel, \(F/D\)-condensate 또는 외부 bath가 없다.
6. “질량”은 \(t,t'>0\) retarded spectral function의 pole로 정의한다.

이 Phase는 완성된 doubled Wess–Zumino sewing action이 아니다. 특히 Phase 17에서 열린
full Pin/Clifford lift, 공통 variational domain, 보존되는 sheet-mixing \(Q\), physical-sheet
observable을 구성하지 않았다. 두-sheet 절은 scalar kernel의 CPT-compatible control일 뿐이다.

### 정리

위 조건 아래 어떤 유한 canonical seam map을 선택해도

\[
m_{B,\mathrm{pole}}^2=m_{F,\mathrm{pole}}^2=m^2.
\]

Seam은 occupation, squeezing, \(t+t'\) image term, cross-seam 또는 source-projected
amplitude를 바꿀 수 있다. 특정 관측자의 operator overlap을 0으로 만들 수도 있다. 그러나
canonical post-post retarded residue는 그대로이며, overlap zero를 pole 이동이나 무한 질량으로
읽을 수는 없다.

## 2. 첫 단계 — 시간의 흐름 자체는 SUSY breaking이 아니다

보존된 supercharge가 있으면

\[
[H,Q]=0.
\]

초기 상태가 \(Q|\psi(0)\rangle=0\)을 만족할 때

\[
\begin{aligned}
Q|\psi(t)\rangle
&=Qe^{-iHt}|\psi(0)\rangle\\
&=e^{-iHt}Q|\psi(0)\rangle\\
&=0.
\end{aligned}
\]

그러므로 elapsed coordinate time은 SUSY를 깨는 원인이 아니다. 실행체는 한 B/F doublet의
유한행렬 control에서 \([H,Q]=0\)과 위 식을 exact하게 확인한다.

Seam이 있는 경우 물어야 하는 조건은 다르다. 허용 Cauchy-data domain을
\(\mathcal D_\Sigma\)라 하면 SUSY가 보존되려면

\[
Q:\mathcal D_\Sigma\longrightarrow\mathcal D_\Sigma
\]

여야 한다. 단순한 B/F marker

\[
S_\Sigma=\begin{pmatrix}s_B&0\\0&s_F\end{pmatrix},
\qquad
Q\propto\begin{pmatrix}0&1\\0&0\end{pmatrix}
\]

에 대해서도

\[
[S_\Sigma,Q]
\propto(s_B-s_F)Q
\]

이므로 \(s_B\ne s_F\)이면 seam domain은 elementary multiplet을 보존하지 않는다. 이는
**domain/action breaking**을 말할 뿐 아직 **mass splitting**을 말하지 않는다.

현재 derivative-free scalar defect에 대해 contact/improvement term을 생략한 schematic Ward
identity는

\[
\partial_\mu J_Q^\mu(x)
=\delta(x^0)\,\mathcal B_\Sigma(\mathbf x)
\]

이다. 더 일반적인 derivative seam에는 \(\delta'(t)\) contact term 등이 생길 수 있다. 어느
경우든 breaking의 지지가 seam에만 있으면 \(t>0\) open bulk의 local current equation은 다시
표준식이다. 먼 미래까지 상수 효과가 남으려면 zero-frequency mode, 보존된 finite-density
population, long memory 또는 condensate 같은 별도 운반체가 필요하다.

## 3. 두 번째 단계 — 자유 bulk의 공통 pole

### Scalar

공간 momentum \(\mathbf k\)를 고정하고

\[
\omega_{\mathbf k}^2=\mathbf k^2+m^2
\]

라 하자. \(Y=(q,p)^T\)의 Cauchy generator는

\[
A_B=
\begin{pmatrix}
0&1\\
-\omega_{\mathbf k}^2&0
\end{pmatrix},
\qquad
A_B^2=-\omega_{\mathbf k}^2I.
\]

따라서

\[
R_B(t)=e^{A_Bt}
=
\begin{pmatrix}
\cos\omega t&\sin\omega t/\omega\\
-\omega\sin\omega t&\cos\omega t
\end{pmatrix}
\]

이고 \(J=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)\)에 대해

\[
R_B^TJR_B=J.
\]

유한 seam map \(M_B\)가 있더라도 미래 해는

\[
Y(t)=R_B(t)M_BY(0^-)
\]

이다. \(M_B\)는 초기 진폭만 바꾸며 \(R_B\)의 characteristic frequency
\(\pm\omega_{\mathbf k}\)를 바꾸지 못한다.

### Fermion

실행체의 helicity-reduced Hamiltonian은 다음과 같다. 여기서 \(k\)의 부호는 basis
convention이고 \(k^2=\mathbf k^2\)다.

\[
h_F(\mathbf k)=
\begin{pmatrix}
m&k\\
k&-m
\end{pmatrix},
\qquad
h_F^2=(\mathbf k^2+m^2)I.
\]

따라서

\[
(zI-h_F)^{-1}
=\frac{zI+h_F}{z^2-\mathbf k^2-m^2}.
\]

Boson과 fermion의 characteristic polynomial은 정확히 같다.

\[
D_B(p^0,\mathbf k)=D_F(p^0,\mathbf k)
=(p^0)^2-\mathbf k^2-m^2.
\]

### Retarded 함수

\(t,t'>0\)인 두 점의 retarded propagation은

\[
G_B^R(t,t';\mathbf k)
=\theta(t-t')\frac{\sin[\omega_{\mathbf k}(t-t')]}{\omega_{\mathbf k}},
\]

\[
S_F^R(t,t';\mathbf k)
=-i\theta(t-t')e^{-ih_F(t-t')}.
\]

그러므로 둘의 pole은 \(p_0^2=\mathbf k^2+m^2\)에 있다. Boundary kernel을 Dyson 형태로
적으면 그 이유가 더 직접적이다.

\[
G(t,t')=G_0(t-t')+G_0(t,0)\,T_\Sigma\,G_0(0,t').
\]

여기서 이 식의 \(G\)는 retarded 함수가 아니라 contour/Feynman/Wightman propagator이고
\(T_\Sigma\)는 dressed boundary kernel이다. 두 번째 항은 두 개의 bulk on-shell leg를 곱한
separable initial-state correction으로 statistical correlation과 cross-seam amplitude를
바꾼다. 반면 \(t,t'>0\) post-post retarded 함수에서는 causality 때문에
\(G_0^R(0,t')=0\)이므로 이 boundary correction이 정확히 사라진다. 어느 경우에도
\(\theta(t)m_{\rm soft}^2\) 같은 uniform future bulk operator가 생성된 것은 아니다.

전역 time-translation symmetry는 seam 때문에 없으므로 전체 spacetime에 하나의
\(G(p^0,\mathbf k)\)를 정의하고 boundary oscillation을 pole로 읽으면 안 된다. 상호작용 계산에서는

\[
G_R(T,\Omega,\mathbf k)
=\int d\tau\,e^{i\Omega\tau}
G_R\!\left(T+\frac\tau2,T-\frac\tau2;\mathbf k\right)
\]

라는 Wigner transform의 \(T\to\infty\) spectral peak를 사용해야 한다.

## 4. 세 번째 단계 — CPT-compatible하지만 SUSY가 아닌 명시적 seam

복소 scalar에 다음 defect를 넣는다.

\[
S_\Sigma=-\kappa\int_{t=0}d^3x\,|\phi|^2,
\qquad \kappa\in\mathbb R.
\]

이 scalar functional은 action 수준에서 CPT-even이다. 반면

\[
\delta\phi=\sqrt2\,\epsilon\psi
\]

이므로 일반적으로

\[
\delta S_\Sigma
=-\sqrt2\kappa\int_{t=0}d^3x
\left(\phi^\dagger\epsilon\psi
+\phi\bar\epsilon\bar\psi\right)
\ne0.
\]

즉 CPT compatibility가 SUSY invariance를 뜻하지 않는다. 이것은 seam functional에 대한
진술이며 선택한 전역 quantum state까지 CPT invariant임을 증명한 것은 아니다.

실수 scalar mode 하나의 matching은

\[
q(0^+)=q(0^-),
\qquad
p(0^+)=p(0^-)-\kappa q(0),
\]

또는

\[
K_B=
\begin{pmatrix}
1&0\\
-\kappa&1
\end{pmatrix}.
\]

정준성과 time-reversed reciprocity는 각각

\[
K_B^TJK_B=J,
\qquad
\mathsf T K_B\mathsf T=K_B^{-1},
\qquad
\mathsf T=\operatorname{diag}(1,-1)
\]

로 exact하게 성립한다.

입사 positive-frequency mode를 matching하면

\[
u_{\rm out}(t)
=\left(1-\frac{i\kappa}{2\omega}\right)e^{-i\omega t}
+\frac{i\kappa}{2\omega}e^{+i\omega t}.
\]

동일한 결과를 annihilation operator로 쓰면

\[
a_+
=\left(1-\frac{i\kappa}{2\omega}\right)a_-
-\frac{i\kappa}{2\omega}a_-^\dagger.
\]

두 식의 두 번째 계수 부호가 다른 것은 mode coefficient와 operator Bogoliubov coefficient의
conjugation convention 때문이다. 정준 조건은

\[
|\alpha_B|^2-|\beta_B|^2=1
\]

이고 정확한 occupation은

\[
\boxed{
n_B(\mathbf k)=|\beta_B|^2
=\frac{\kappa^2}{4(\mathbf k^2+m^2)}
}.
\]

Incoming vacuum의 두 mode를 묶은 finite fermionic Nambu-pair control에는 예를 들어

\[
U_F(\theta)=
\begin{pmatrix}
\cos\theta&\sin\theta\\
-\sin\theta&\cos\theta
\end{pmatrix},
\qquad U_F^\dagger U_F=I,
\]

를 쓸 수 있고

\[
\boxed{n_F(\mathbf k)=\sin^2\theta}
\]

이다. 이것은 local Weyl/Majorana seam action이나 fermionic Pin lift의 구성이 아니다.
\(\theta=0\)이면 \(n_F=0\)이므로 \(n_B\ne n_F\)인 non-SUSY outgoing state를
명시적으로 만들 수 있다. 그런데도 양쪽 pole은 여전히 \(m\)이다.

\[
\boxed{
n_B\ne n_F
\quad\text{이지만}\quad
m_{B,\mathrm{pole}}=m_{F,\mathrm{pole}}=m
}
\]

이것이 state SUSY breaking과 spectrum splitting을 구별하는 exact witness다.

## 5. 네 번째 단계 — Wightman 신호와 spectral pole의 분리

Raw Wightman convention
\(W^>(t,t')=\langle q(t)q(t')\rangle\)을 쓴다. 물리적 Gaussian scalar state는
\(n\ge0\), \(|c|^2\le n(n+1)\)을 만족하며, pure squeezed state에서는 등호가 성립한다.
그 greater function에는

\[
\begin{aligned}
W_B^>(t,t';\mathbf k)=\frac1{2\omega}\bigl[&
(1+n)e^{-i\omega(t-t')}+ne^{+i\omega(t-t')}\\
&+ce^{-i\omega(t+t')}+c^*e^{+i\omega(t+t')}
\bigr]
\end{aligned}
\]

처럼 occupation \(n\)과 anomalous coefficient \(c\)가 들어간다. Lesser function과의
차를 취하면 이 값들이 모두 상쇄되어

\[
i(W^>-W^<)=\frac{\sin[\omega(t-t')]}{\omega}
\]

만 남는다. 즉 statistical/Keldysh sector는 seam을 기억하지만 spectral commutator는 기억하지
않는다. Collins의 initial-action propagator도 free propagation과 initial-state correction을
분리한다. 이 Phase의 계산은 그 가장 작은 exact mode control이다.

Seam이 만든 \(t+t'\) 항은 중앙시간 \(T=(t+t')/2\)에서 \(2\omega\)로 진동한다. 유한시간
Fourier window가 만드는 peak broadening이나 side lobe를 새 particle mass로 판정하면 안 된다.

## 6. 두 time-sheet scalar control

Sheet exchange를 \(X_s=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\), CPT의
anti-linearity를 complex conjugation으로 표현한다. Hermitian quadratic scalar kernel

\[
K_\Sigma=
\begin{pmatrix}
a&z\\z^*&a
\end{pmatrix},
\qquad a\in\mathbb R
\]

은

\[
X_sK_\Sigma^*X_s=K_\Sigma
\]

를 만족한다. 그 두 eigenchannel의 kick strength는

\[
\kappa_\pm=a\pm|z|.
\]

특히 real slice \(z=b\in\mathbb R\)에서는 doubled phase-space kick이 symplectic이고

\[
n_\pm(\mathbf k)
=\frac{(a\pm b)^2}{4\omega_{\mathbf k}^2}.
\]

따라서

\[
n_++n_-=\frac{a^2+b^2}{2\omega_{\mathbf k}^2},
\qquad
n_+-n_-=\frac{ab}{\omega_{\mathbf k}^2}.
\]

CPT-compatible sheet exchange는 scalar channel asymmetry 자체를 금지하지 않는다. 더 중요하게,
이 두 channel도 같은 bulk \(\omega_{\mathbf k}\)를 사용한다. 이 계산은 full fermionic Pin lift나
global CPT vacuum construction을 대신하지 않는다.

## 7. 다섯 번째 단계 — sharp seam의 UV 비용

실수 scalar 한 자유도당 주입된 mode energy는

\[
\Delta E_B(\mathbf k)
=\omega_{\mathbf k}n_B(\mathbf k)
=\frac{\kappa^2}{4\omega_{\mathbf k}}.
\]

공간 cutoff \(\Lambda\)를 두면 number density는

\[
\mathcal N_B^{\rm real}(\Lambda)
=\frac{\kappa^2}{8\pi^2}
\left[
\Lambda-m\arctan\frac\Lambda m
\right],
\]

energy density는

\[
\rho_B^{\rm real}(\Lambda)
=\frac{\kappa^2}{16\pi^2}
\left[
\Lambda\sqrt{\Lambda^2+m^2}
-m^2\operatorname{arsinh}\frac\Lambda m
\right].
\]

따라서

\[
\mathcal N_B^{\rm real}\sim\frac{\kappa^2\Lambda}{8\pi^2},
\qquad
\rho_B^{\rm real}\sim\frac{\kappa^2\Lambda^2}{16\pi^2}.
\]

복소 scalar의 두 real component가 같은 kick을 받으면 이 값은 두 배다. 즉 이상적인
\(\delta(t)\) seam은 continuum에서 UV-regular/Hadamard finite-energy state가 아니다. 이
tree-level 무한 excitation energy는 boundary counterterm만 붙여 물리적 finite-energy state로
바꿀 수 없고, temporal smoothing 또는 UV completion이 필요하다. 상호작용 loop에서 생기는
별도의 initial-state UV divergence는 initial surface에 국소화되어 boundary counterterm을
요구할 수 있으며 bulk renormalization과 구별해야 한다.

다음 정규화된 Gaussian pulse는 엄밀한 \(t=0\)-supported theorem의 일부가 아니라 sharp
seam을 유한시간 quench로 바꾼 **UV-regulator control**이다.

\[
\kappa_\sigma(t)
=\frac{\kappa}{\sqrt{2\pi}\sigma}
e^{-t^2/(2\sigma^2)}
\]

는

\[
\widetilde\kappa_\sigma(2\omega)
=\kappa e^{-2\sigma^2\omega^2}
\]

를 주고, Born approximation에서는

\[
\boxed{
n_{B,\sigma}^{\rm Born}(\mathbf k)
=\frac{\kappa^2}{4\omega_{\mathbf k}^2}
e^{-4\sigma^2\omega_{\mathbf k}^2}
}
\]

이다. 이것은 high-\(k\) excitation을 지수적으로 누른다. 단, 유한 \(\sigma\) 식은 Born 결과이며
arbitrary strong smooth pulse의 exact solution이라고 주장하지 않는다.

## 8. 실제로 나온 예측값

### Parameter-free pole 예측

동결 범위 안에서 물리적 scale 입력 없이 나오는 유일한 pole 예측은

\[
\boxed{\Delta m_{\mathrm{pole}}^2=0}
\]

이다. 이것은 “원하던 결과가 아니다”가 아니라 이 모델 class에 대한 falsifying null result다.

### Sharp seam의 dimensionless benchmark

\(k=0\)에서

\[
n_B=\frac14\left(\frac\kappa m\right)^2.
\]

| \(\kappa/m\) | \(n_B(k=0)\) |
|---:|---:|
| \(0.1\) | \(0.0025\) |
| \(1\) | \(0.25\) |
| \(2\) | \(1\) |

\(\kappa/m=1,\;\Lambda/m=100\)이면 실수 scalar 하나에 대해

\[
\frac{\mathcal N_B}{m^3}=1.2467470749,
\qquad
\frac{\rho_B}{m^4}=63.2953538393.
\]

Cutoff가 커질수록 두 값이 각각 선형·제곱으로 발산하므로 이 숫자는 fundamental prediction이
아니라 sharp-seam pathology benchmark다.

### Smooth Gaussian Born benchmark

\(k=0,\;\kappa/m=1\)에서

| \(\sigma m\) | \(n_{B,\sigma}^{\rm Born}\) |
|---:|---:|
| \(0\) | \(0.25\) |
| \(0.5\) | \(e^{-1}/4=0.0919698603\) |
| \(1\) | \(e^{-4}/4=0.00457890972\) |

따라서 seam duration을 한 Compton time 정도로 늘리는 것만으로 rest-mode Born production도
sharp limit의 약 \(1.83\%\)로 줄어든다.

### 독립 수치 검산

Exact SymPy 유도와 별도로, 같은 실행체가
\[
\ddot q+\left[\omega^2+\kappa_\sigma(t)\right]q=0
\]
을 SciPy solve_ivp의 DOP853으로 직접 적분한다. 입력은
\(\omega=1.3,\;\kappa=0.4,\;\sigma=0.002,\;t\in[-0.05,0.05]\),
rtol \(=2\times10^{-12}\), atol \(=2\times10^{-14}\)다. 관측값은 다음과 같다.

    alpha_numeric = 0.999999680077 - 0.153776727111j
    alpha_delta   = 1.000000000000 - 0.153846153846j
    beta_numeric  = 0.000000000000 + 0.153774646656j
    beta_delta    = 0.000000000000 + 0.153846153846j
    max_abs_error = 7.150719e-05
    norm_error    = 3.330669e-16

이는 좁은 Gaussian의 direct evolution이 analytic delta-kick coefficient에 수렴하고
\(|\alpha|^2-|\beta|^2=1\)을 수치 정밀도 안에서 보존한다는 독립 검산이다. 이 한 점 검사는
arbitrary pulse에 대한 오차 정리나 interacting result가 아니다.

## 9. 상호작용을 넣으면 무엇이 달라지는가

자유이론에서 초기상태는 retarded pole에 들어가지 않는다. 상호작용이 있으면 occupation이
self-energy loop에 들어가 medium quasiparticle dispersion을 바꿀 수 있다. 시간병진 대칭이 없는
상태에서는

\[
G_{B,R}^{-1}(T,p)=p^2-m^2-\Pi_B^R(T,p),
\]

\[
S_{F,R}^{-1}(T,p)=\slashed p-m-\Sigma_F^R(T,p)
\]

의 Wigner-space spectral peak를 비교해야 한다. 다음 식은 계산 결과가 아니라 Phase 19의
parameterized target이다.

\[
\begin{aligned}
\Delta M_{\rm qp}^2(T,p)
={}&g^2\sum_{s=B,F}
\int\frac{d^3q}{(2\pi)^3}
\frac{f_s(T,q)}{a^3E_s(q/a)}
K_s(T;p,q)\\
&+\Delta_{\rm coh}(T,p)
+\Delta_{\langle\phi\rangle}(T,p)
+O(\text{higher loops/gradients}).
\end{aligned}
\]

여기서 \(K_s\)는 외부·내부 momentum과 선택한 action에 의존하는 loop kernel이고,
\(\Delta_{\rm coh}\)는 anomalous correlator, \(\Delta_{\langle\phi\rangle}\)는 nonzero one-point
background의 항이다. Hartree 또는 momentum-independent hard-loop 근사에서만
\(K_s\to C_s\)로 두어

\[
\mathcal I_s(a)
=\int\frac{d^3q}{(2\pi)^3}
\frac{f_s(q)}{a^3E_s(q/a)},
\qquad
\Delta M_{\rm qp}^2
\simeq g^2(C_B\mathcal I_B+C_F\mathcal I_F)
\]

로 축약할 수 있다. 계수 또는 kernel은 선택한 interacting Wess–Zumino action, regulator와
renormalization condition에서 실제로 유도해야 한다. CPT는 particle/antiparticle 관계를
제한하지만 일반적으로 \(f_B=f_F\)를 강제하지 않으므로 질량차의 크기나 부호도 CPT만으로
정해지지 않는다. Fermion에 하나의 \(M_F\)를 붙이는 것 역시 등방적 상태의
\(\mathbf p=0\)에서 width가 작은 단일 peak가 있다는 조건부 표기다. 일반 medium에는 여러
fermionic branch와 유한 width가 생길 수 있다.

이 식을 sharp Phase 18 state에 그대로 대입할 수도 없다. 그 scalar occupation은
\(f_B(k)\sim\kappa^2/(4k^2)\)이므로

\[
\mathcal I_B^{\rm sharp}(\Lambda)
\sim\frac{\kappa^2}{8\pi^2}\log\frac{\Lambda}{m}.
\]

또 momentum-independent \(\theta\)를 쓴 fermion CAR control은
\(\mathcal I_F\sim\sin^2\theta\,\Lambda^2/(4\pi^2)\)다. 따라서 Phase 19 계산은 smooth
UV-admissible \(\beta_s(k)\) 또는 명시적으로 boundary-renormalized state를 먼저 요구한다.
Phase 18의 constant-\(\theta\) 행렬은 physical UV state가 아니라 통계와 pole을 분리하는
finite-mode algebraic witness다.

상호작용 quench가 late-time non-SUSY quasiparticle mass를 남길 수 있다는 제한된 선행
proof-of-principle은 있다. 그러나 Hung–Smolkin–Sorkin 결과는 \(2+1\)차원
\(\mathcal N=1\) large-\(N\) vector model의 Hartree–Fock/stationary approximation이다. 이를
4D Wess–Zumino vacuum pole이나 오늘날 superpartner spectrum의 증명으로 인용하면 안 된다.

## 10. 조건부 FRW dilution scaling control

Collisionless comoving distribution \(f_s(q)\)가 보존되고, 앞 절의 Hartree 또는
momentum-independent kernel 근사에서 \(\Delta M_{\rm state}^2\propto\mathcal I_s\)라고 하자.
상대론적 영역에서는

\[
\mathcal I_s(a)
=\frac1{a^2}\int\frac{d^3q}{(2\pi)^3}
\frac{f_s(q)}{\sqrt{q^2+a^2m_s^2}}.
\]

그러므로 전체 구간이 상대론적인 극한에서는

\[
\mathcal I_s(a)\propto a^{-2},
\qquad
\Delta M_{\rm state}^2(a)\propto a^{-2},
\]

비상대론적이고 particle number가 보존되면

\[
\mathcal I_s(a)\propto a^{-3},
\qquad
\Delta M_{\rm state}^2(a)\propto a^{-3}.
\]

따라서 단순한 seam-produced bath만 있다면

\[
\boxed{
\lim_{a\to\infty}\Delta M_{\rm state}^2(a)=0
}
\]

이다. 여기에는 영원한 팽창, 지속적 particle production·condensation·phase transition이
없다는 조건이 들어간다. \(t=0\)이 \(a=0\)인 특이 surface라면 비율을 바로 정의할 수 없으므로,
유한 폭을 가진 matching surface \(a_\Sigma>0\)를 먼저 택해야 한다. 팽창비
\(R=a/a_\Sigma\)에 대한 두 극한의 suppression은 다음과 같다.

| \(R\) | relativistic \(\Delta M_{\rm state}^2(a)/\Delta M_{\rm state}^2(a_\Sigma)\) | nonrelativistic \(\Delta M_{\rm state}^2(a)/\Delta M_{\rm state}^2(a_\Sigma)\) |
|---:|---:|---:|
| \(10^3\) | \(10^{-6}\) | \(10^{-9}\) |
| \(10^{10}\) | \(10^{-20}\) | \(10^{-30}\) |
| \(10^{28}\) | \(10^{-56}\) | \(10^{-84}\) |

실제 history가 relativistic에서 nonrelativistic으로 전이하면 두 scaling을 구간별로 이어야 한다.
공통 vacuum mass \(m\ne0\)에 대한 작은 correction이면
\(M_B-M_F\simeq\Delta M^2/(2m)\)도 같은 scaling을 따른다. 반면 state effect가 massless
mode의 전체 질량을 만든다면 \(M_{\rm rel}\propto a^{-1}\),
\(M_{\rm nr}\propto a^{-3/2}\)다.

이것은 detailed cosmology의 수치예측이 아니라 collisionless scaling control이다. Reheating,
rescattering, entropy production, curvature coupling을 넣으면 다시 계산해야 한다. 정확한 결론은
한 번 생성된 population이 오늘날 일정한 **vacuum soft parameter**로 그대로 남는 메커니즘이
아니라는 것이다. 오늘날 큰 medium quasiparticle shift를 주장하려면 유한 \(a_\Sigma\), 초기
energy density와 Friedmann backreaction을 함께 만족시켜야 한다.

## 11. 영구 질량분열에 필요한 구조

영구적인 vacuum pole split을 얻으려면 seam이 단순한 입자분포가 아니라 지속적인 vacuum
order parameter를 선택해야 한다. 예를 들어 hidden chiral field

\[
X=x+\sqrt2\theta\psi_X+\theta^2F_X
\]

가 seam 이후 metastable vacuum에 정착하여

\[
F_X\longrightarrow F_\star\ne0
\]

가 된다고 하자. 그러면 조건부로

\[
K\supset Z_i(X,\bar X)\Phi_i^\dagger\Phi_i,
\qquad
m_i^2
=-|F^X|^2
\partial_X\partial_{\bar X}\ln Z_i\big|_{X_\star}.
\]

예를 들어 \(X_\star=0\) 부근에서
\(Z_i=1-c_iX^\dagger X/M_*^2\)로 convention을 정하면

\[
m_i^2\simeq c_i\frac{|F_\star|^2}{M_*^2}.
\]

Gauge kinetic function에 대해서는 일반적으로

\[
M_a
=\frac12(\operatorname{Re}f_a)^{-1}
F^X\partial_Xf_a.
\]

\(f_a=f_{a0}+k_aX/M_*+\cdots\)이면 convention-dependent gauge normalization까지 포함하여
\(M_a\sim k_aF_\star/M_*\)의 scaling을 얻는다. 정확한 부호·\(1/2\)·\(g_a^2\) 계수는
\(K,W,f_a\)와 canonical normalization에서 결정해야 한다.

이때는 state density의 redshift와 달리 vacuum soft term이 남을 수 있다. 그러나 \(F_X\)는
임의의 상수가 아니라 \(K,W\)의 auxiliary equation으로 결정되어야 하고, visible coupling도
실제로 nonzero여야 한다. Seam이 정말로 그 vacuum을 선택한다는 것을 다음 조건과 함께
증명해야 한다.

\[
\partial_XV_{\rm eff}
=\partial_{\bar X}V_{\rm eff}=0,
\qquad
\text{full real Hessian of }V_{\rm eff}>0,
\qquad
F_X(X_\star)\ne0.
\]

Vacuum lifetime, Friedmann backreaction, \(F_\star\)가 만드는 vacuum energy도 동시에 검사해야
한다. Goldstino 또는 supergravity의 gravitino sector와 두 sheet의 vacuum choice가 global CPT
조건에 맞는지도 확인해야 한다. 이 추가 구조 없이 “seam이 soft mass를 만들었다”고 말하면
원인을 결론에 삽입한 것이다.

단순 tree-level benchmark로
\(m_B^2=m^2+\mu_{\rm soft}^2,\;m_F=m,\;\mu_{\rm soft}^2\ge0\),
\(r=\mu_{\rm soft}/m\)라 두면

\[
\frac{m_B}{m_F}=\sqrt{1+r^2}.
\]

| \(r\) | \(m_B/m_F\) | \((m_B-m_F)/m_F\) |
|---:|---:|---:|
| \(0.1\) | \(1.0049875621\) | \(0.0049875621\) |
| \(1\) | \(1.4142135624\) | \(0.4142135624\) |
| \(10\) | \(10.0498756211\) | \(9.0498756211\) |

이 표는 persistent soft parameter를 **넣었을 때**의 tree-level algebraic response이며
loop-corrected pole도, seam으로부터 그 term을 유도한 예측도 아니다.

## 12. Higgs UV cancellation 판정

자유 Phase 18에는 loop가 없으므로 Higgs naturalness를 검사할 수 없다. 다음 Phase에서는
vacuum, state-dependent, boundary-local 부분을 분리해야 한다.

\[
\Pi_H(\Lambda)
=A_2\Lambda^2
+A_{\log}\log\frac\Lambda\mu
+A_0+\cdots.
\]

여기서 raw \(A_2\)는 regulator-dependent하다. Naive hard cutoff가 SUSY Ward identity를
스스로 깨서 가짜 power term을 만들 수도 있다. 따라서 검사는 SUSY-preserving regulator와
counterterm prescription, 또는 Wilsonian heavy-threshold matching으로 수행해야 한다. 의미
있는 판정 대상은 표기상의 cutoff 항이 아니라 physical power sensitivity다.

검사 목표는 다음과 같다.

1. Bulk SUSY relation이 유지되면 vacuum piece에서 \(A_2^{\rm bulk}=0\)인가?
2. Seam이 만든 새 divergence는 \(t=0\) boundary counterterm에만 국소화되는가?
3. 영구 breaking이 있다면 생성된 operator가 soft class인가, hard coupling mismatch인가?
4. Soft인 경우 residual sensitivity가 대략

   \[
   \delta m_H^2\sim
   \frac{c\,g^2}{16\pi^2}\Delta m_{\rm multiplet}^2
   \log\frac{\Lambda_{\rm med}^2}{M_{\rm loop}^2}
   \]

   꼴인지, 아니면 \(\Lambda^2\)가 되살아나는가?

여기서 \(c\), 부호, multiplicity와 IR mass는 모델 의존이고
\(\Lambda_{\rm med}\)는 mediation/matching scale이다. \(A_2^{\rm bulk}=0\)만으로 naturalness가
증명되는 것도 아니다. 큰 finite threshold가 남는지도 따로 검사해야 한다. 또한 현재
Wess–Zumino scalar proxy를 실제 Higgs에 연결하려면 top/stop, gauge/gaugino,
Higgs/higgsino sector를 모두 포함해야 한다.

이 네 항목을 계산하기 전에는 “visible SUSY는 없지만 UV cancellation은 남는다”는 문장은
열린 가설이다. Girardello–Grisaru의 soft-breaking 분류는 비교 기준이지 temporal seam에 대한
자동 판정이 아니다. 이 검사는 sharp state가 아니라 smooth 또는 명시적으로
boundary-renormalized state에서 occupation과 anomalous \(t+t'\) divergence를 모두 추적해야
한다.

## 13. 반증 가능한 결과표

| 계산 결과 | 올바른 해석 | 프로그램에 미치는 영향 |
|---|---|---|
| Free \(G_R\) pole 동일, Keldysh만 다름 | initial-state SUSY breaking | 이번 Phase의 정확한 결과; free seam-only pole-splitting 설명은 실패 |
| Interacting \(M_B(T)\ne M_F(T)\), \(a^{-2}\) 또는 \(a^{-3}\) 소멸 | medium/quasiparticle splitting | 초기 우주 효과는 가능, 오늘날 vacuum spectrum 설명은 약함 |
| State가 희석된 뒤에도 \(F_\star\ne0\), vacuum pole 분리 | seam-triggered vacuum selection 후보 | 영구 SUSY breaking route가 열림 |
| 동시에 \(A_2^{\rm bulk}=0\), soft logarithm만 남음 | UV softness 유지 | “temporal SUSY without visible SUSY”의 핵심 성공조건 |
| Physical \(A_2^{\rm bulk}\ne0\) | hard bulk breaking | SUSY의 자연성 이점 상실 |
| Seam state의 energy density가 무한 | non-Hadamard/inadmissible initial state | smoothing 또는 UV completion 없이는 모델 폐기 |
| 관측된 고유 질량비·우주론 신호가 계산값과 불일치 | 모델별 반증 | “SUSY 비관측” 자체보다 훨씬 강한 시험 |

논리적으로 SUSY 비관측은 temporal seam의 증명이 아니다.

\[
\text{temporal seam model}\Rightarrow\text{possible SUSY breaking}
\]

이어도 역은 성립하지 않는다. 이 모델이 실증적 가설이 되려면 \(F_\star/M_*\), gaugino ratio,
scalar soft pattern 또는 cosmological signal 사이의 고유 관계를 실제 action으로부터 유도해야
한다.

## 14. 계산 사실, 해석, 열린 문제

### 계산으로 확인됨

- 보존된 \(Q\) 아래에서 elapsed time alone은 SUSY 상태를 깨지 않는다.
- 자유 equal-mass B/F mode의 retarded denominator는 동일하다.
- scalar delta seam kick은 canonical이고 time-reversal reciprocal이다.
- 그 seam은 occupation \(n_B=\kappa^2/(4\omega^2)\)를 만들지만 pole을 옮기지 않는다.
- Wightman/statistical 함수는 seam data를 기억하고 spectral commutator는 기억하지 않는다.
- sharp local seam은 number density에 선형, energy density에 제곱 UV divergence를 만든다.
- Gaussian pulse의 Born occupation은 \(e^{-4\sigma^2\omega^2}\)로 UV-soft하다.

### 제한된 해석

- “CPT는 보존하지만 SUSY는 seam에서 깨진다”는 action/domain witness는 가능하다.
- 그러나 이 breaking은 우선 non-SUSY initial state를 뜻하며 soft spectrum을 뜻하지 않는다.
- 한 번의 noncompact temporal seam은 compact spatial Scherk–Schwarz twist처럼 energy level을
  양자화하지 않는다.

### 아직 열림

- full doubled Wess–Zumino/Pin sewing action과 공통 variational domain
- interacting \(4d\) Wess–Zumino Schwinger–Keldysh self-energy
- FRW backreaction과 late-time dephasing/thermalization
- persistent \(F/D\)-order parameter의 동역학적 생성
- Higgs quadratic sensitivity의 bulk/boundary/state 분해
- 오늘날 GeV/TeV 질량값 또는 고유 mass-ratio prediction

마지막 항목은 특히 중요하다. 현재 입력에는 \(\kappa,\sigma,\theta,g,F_\star,M_*\)를 정하는
microphysics가 없다. 따라서 임의의 \(10^X\,\mathrm{GeV}\)를 쓰는 것은 예측이 아니라 scale
삽입이다.

## 15. 다음 최소 계산

Phase 19의 최소 목표는 interacting \(4d\) Wess–Zumino model에서 다음을 동시에 계산하는
것이다.

1. UV-admissible \(\beta_B(k),\beta_F(k)\)를 주는 smooth CPT/Pin-constrained seam action을 유도한다.
2. Schwinger–Keldysh one-loop \(\Pi_B^R(T,p)\), \(\Sigma_F^R(T,p)\)를 계산한다.
3. Vacuum, stationary occupation, anomalous \(t+t'\), boundary-transient term을 분리한다.
4. FRW scale factor를 넣고 \(T\to\infty\) 또는 \(a\to\infty\) limit을 취한다.
5. Pole split, width, energy density와 \(A_2^{\rm bulk}\)를 한꺼번에 검사한다.

그 판정식은

\[
\boxed{
\lim_{T\to\infty}
\left[M_B^2(T)-M_F^2(T)\right]
\stackrel{?}{\ne}0
}
\]

이다. 비영 상수가 나오더라도 medium effect인지 vacuum soft term인지 구별해야 한다.

## 16. 출처와 사용 범위

- J. Wess and B. Zumino, “A Lagrangian Model Invariant Under Supergauge Transformations,”
  [Phys. Lett. B 49 (1974) 52–54](https://doi.org/10.1016/0370-2693%2874%2990578-4).
  Free/interacting Wess–Zumino multiplet의 기준점으로 사용했다.
- H. Collins, “Initial state propagators,”
  [JHEP 11 (2013) 077, arXiv:1309.2656](https://arxiv.org/abs/1309.2656).
  Initial action이 free propagation과 state-dependent propagator correction을 분리한다는 비교
  기준으로 사용했다.
- H. Collins and R. Holman, “Renormalization of initial conditions and the trans-Planckian problem
  of inflation,” [Phys. Rev. D 71 (2005) 085009, hep-th/0501158](https://arxiv.org/abs/hep-th/0501158).
  Initial-state divergence와 boundary counterterm의 범위를 확인하는 데 사용했다.
- L.-Y. Hung, M. Smolkin and E. Sorkin, “(Non) supersymmetric quantum quenches,”
  [JHEP 12 (2013) 022, arXiv:1307.0376](https://arxiv.org/abs/1307.0376).
  \(2+1d\), large-\(N\), Hartree–Fock interacting-quench proof-of-principle로만 사용했다.
- L. Girardello and M. T. Grisaru, “Soft Breaking of Supersymmetry,”
  [Nucl. Phys. B 194 (1982) 65–76](https://doi.org/10.1016/0550-3213%2882%2990512-0).
  미래 soft/hard operator 판정의 기준으로만 사용했다.
- L. Boyle and N. Turok, “Two-Sheeted Universe, Analyticity and the Arrow of Time,”
  [arXiv:2109.06204](https://arxiv.org/abs/2109.06204).
  두 analytic sheet가 isometry로 교환되는 우주론적 동기를 제공하지만 SUSY/Pin seam
  construction이나 이 Phase의 no-pole-splitting 정리를 제공하는 출처는 아니다.

## 최종 판정

\[
\boxed{
\begin{gathered}
\text{시간의 흐름 자체는 SUSY를 깨지 않는다.}\\
\text{한 번의 canonical temporal seam은 non-SUSY 상태를 만들 수 있다.}\\
\text{하지만 자유 bulk의 B/F pole mass는 정확히 갈라지지 않는다.}
\end{gathered}
}
\]

그러므로 “우주의 시간적 접합 구조가 SUSY 비관측의 원인”이라는 문장은 아직 가설이다.
이번 Phase가 좁힌 올바른 route는

\[
\boxed{
\text{seam}
\to
\text{persistent vacuum/order parameter selection}
\to
\text{soft bulk terms}
}
\]

이며, 가운데 화살표를 실제 동역학으로 증명하는 것이 다음 결정타다.
