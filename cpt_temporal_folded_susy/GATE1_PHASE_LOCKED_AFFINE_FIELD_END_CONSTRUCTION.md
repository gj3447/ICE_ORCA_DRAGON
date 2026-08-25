# Gate 1 — phase-locked affine field-end construction

## 결론

기존 straight-lift 결과가 배제한 것은 endpoint anchor를 지나는 homogeneous line
\(\delta=qy\)다. 같은 fixed-\(a\), \(m=2\) scalar action에서 lapse의 위상에 맞춰

\[
T=\rho e^{i\psi},\qquad
\delta_\psi^\infty(x)=x+\frac{i\psi}{\kappa},\qquad
\kappa=\sqrt{\frac23},
\]

를 택하면 finite lower-bypass 전체

\[
0<r\leq\rho\leq R<\infty,
\qquad -\frac\pi2\leq\psi\leq\frac\pi2
\]

에서 두 \(\phi_1\) 끝이 \(e^{-S_2}\) convention의 relative-good region으로 **균일하게**
간다. 또한 standard smooth cutoff로 Phase-39의 중앙 field window를 정확히 유지하면서 바깥쪽만
이 affine end로 굽힐 수 있다.

```text
analytic_status       = EXACT_DERIVATION_INDEPENDENTLY_REVIEWED
field_end_decision    = BRANCH
programme_impact      = NARROW_STRAIGHT_KILL_AND_OPEN_EXPLICIT_CURVED_BRANCH
Gate 1                = OPEN_PARTIAL_PROGRESS
physical_original_cycle = null
global_n_sigma        = null
physics_claim         = null
TOE_claim             = null
automatic_next        = null
```

이는 새 runner 실행이나 numbered Phase가 아니다. 활성 Ragnarok containment 아래 기존 exact
action을 실행 없이 재분석한 analytic result다.

## Source, convention과 정확한 범위

출발점은 Phase 39에서 이미 축약되고 straight-lift 계산에서 독립 대조된 fixed-\(a\) action이다.

\[
S_2(\delta,T)
=\frac{4\pi^2a^3\delta^2}{T}
+2\pi^2T\left[-3a+\frac34a^3
\left(1-e^{-\kappa(\phi+\delta/2)}\right)^2\right],
\qquad a>0,\quad \phi\in\mathbb R.
\]

적분 convention은 \(e^{-S_2}\)이므로 good end는
\(\operatorname{Re}S_2\to+\infty\)를 요구한다. 이 relative-cycle framing은
[Witten, *Analytic Continuation Of Chern-Simons Theory*, §3.1.1](https://arxiv.org/abs/1001.2933)
에서 가져오지만, 그 논문이 여기의 중력 action이나 original cycle을 선택하는 것은 아니다.
[Banihashemi–Jacobson, *On the lapse contour in the gravitational path integral*](https://doi.org/10.1103/PhysRevD.111.066014)은
configuration representation의 below-origin lapse contour를 다루지만 이 field lift를 선택하지
않는다.

이번 결과가 포함하는 것은 다음뿐이다.

- fixed positive \(a\)와 real boundary \(\phi\);
- Phase-39 \(m=2\) scalar의 한 complex \(\phi_1\) fiber;
- finite regulator \(r\leq |T|\leq R\)인 lower-bypass arm과 cap;
- scalar integrand \(e^{-S_2}\)의 두 field end.

Varying complex \(a_1\), \(r\to0\), \(R\to\infty\), joint infinity, canonical momenta,
gauge/BFV body, Pfaffian/Pin orientation과 physical original cycle은 포함하지 않는다.

## Exact phase cancellation

\(E=e^{-\kappa\phi}\), \(b=\psi/\kappa\), \(\delta=x+ib\)를 대입하면

\[
\begin{aligned}
\operatorname{Re}S_2
={}&\frac{4\pi^2a^3}{\rho}
\left[(x^2-b^2)\cos\psi+2xb\sin\psi\right]\\
&+2\pi^2\rho\left[
\left(-3a+\frac34a^3\right)\cos\psi
-\frac32a^3E e^{-\kappa x/2}\cos\frac\psi2
+\frac34a^3E^2e^{-\kappa x}
\right].
\end{aligned}
\]

핵심 identity는

\[
T e^{-\kappa\delta}
=\rho e^{i\psi}e^{-\kappa x}e^{-i\psi}
=\rho e^{-\kappa x}>0
\]

이다. Starobinsky full-rate exponential의 oscillatory phase가 lapse phase와 정확히 상쇄된다.

### \(x\to-\infty\)

\[
\lim_{x\to-\infty}
e^{\kappa x}\operatorname{Re}S_2
=\frac32\pi^2a^3\rho E^2>0.
\]

Half-rate 항은 \(O(e^{-\kappa x/2})\), kinetic은 \(O(x^2)\)이므로 positive full-rate 항이
지배한다. \(\rho\geq r>0\)이므로 이 결론은 frozen finite regulator에서 균일하다.

### \(x\to+\infty\)

Interior cap \(|\psi|<\pi/2\)에서는

\[
\lim_{x\to+\infty}\frac{\operatorname{Re}S_2}{x^2}
=\frac{4\pi^2a^3}{\rho}\cos\psi>0.
\]

두 arm endpoint \(\psi=s\pi/2\)에서는 quadratic가 사라지지만

\[
\lim_{x\to+\infty}\frac{\operatorname{Re}S_2}{x}
=\frac{4\pi^3a^3}{\kappa\rho}>0.
\]

균일성은 \(|\psi|\leq\pi/4\)와 \(\pi/4\leq|\psi|\leq\pi/2\)로 나누면 직접 보인다.
첫 구간에서는 \(\cos\psi\geq1/\sqrt2\)인 quadratic가, 둘째 구간에서는
\(2x(\psi/\kappa)\sin\psi\)의 positive linear lower bound가 발산한다. 따라서 cap endpoint로
접근하는 \(\psi(x)\) escape도 이 결론을 피하지 못한다.

결국 fixed \(0<r\leq\rho\leq R\)에서

\[
\operatorname{Re}S_2\longrightarrow+\infty
\quad (x\to\pm\infty)
\]

가 \(\psi\) 전체에 균일하다. Affine tail에서 \(d\delta/dx=1\)이므로 이 reduced scalar
fiber integral은 양끝에서 절대 수렴한다. 이는 BFV determinant나 다른 measure factor를 포함한
full path integral의 수렴 주장과는 다르다.

## Phase-39 중앙 window를 유지하는 compact bend

Phase 39의 field window를 \(|y_\phi|\leq Y\), \(Y=0.25\)라 하자. 원래 cap/arm field line은

\[
\delta=e^{i\psi/2}y_\phi.
\]

\(X_\psi=Y\cos(\psi/2)>0\)를 두고 다음 standard \(C^\infty\) step을 사용한다.

\[
p(u)=\begin{cases}0,&u\leq0,\\e^{-1/u},&u>0,\end{cases}
\qquad
B(u)=\frac{p(u)}{p(u)+p(1-u)},
\]

\[
\chi_\psi(x)=B\!\left(\frac{x^2-X_\psi^2}{3X_\psi^2}\right),
\qquad
h_\psi(x)=(1-\chi_\psi)x\tan\frac\psi2
+\chi_\psi\frac\psi\kappa,
\]

\[
\boxed{\ \delta_\psi(x)=x+i h_\psi(x)\ }.
\]

- \(|x|\leq X_\psi\): \(\chi=0\)이고
  \(\delta_\psi=e^{i\psi/2}y_\phi\),
  \(y_\phi=x/\cos(\psi/2)\). 중앙 window의 기하를 정확히 보존한다.
- \(|x|\geq2X_\psi\): \(\chi=1\)이고
  \(\delta_\psi=x+i\psi/\kappa\). 위 exact good ends를 갖는다.
- \(\operatorname{Re}\delta_\psi=x\)이므로 contour는 injective이고
  \(d\delta/dx=1+i h_\psi'(x)\neq0\)라 orientation이 퇴화하지 않는다.
- \(\delta_{-\psi}(x)=\overline{\delta_\psi(x)}\)이므로 두 lapse arm의 conjugation pairing도
  보존한다.
- \(T\neq0\)이고 action은 \(\delta\)에 entire이므로 compact connector에는 field singularity가
  없다.

비자명한 compact cutoff가 open interval에서 원래 line과 정확히 같으면서 globally
real-analytic일 수는 없다. 위 construction은 smooth real relative cycle이다. Globally analytic
parameterization을 별도 요구한다면 piecewise-analytic central segment, finite connectors와 affine
rays로 읽어야 한다.

## Reduced end components와 EQUIVALENCE 경계

고정 \(T=\rho e^{i\psi}\)에서 \(\delta=iv\)인 vertical divider를 보자. Kinetic real part는

\[
-\frac{4\pi^2a^3v^2}{\rho}\cos\psi\leq0
\]

이고 potential real part는 \(v\)에 대해 bounded다. 따라서 충분히 큰 \(M\)에 대해
\(\{\operatorname{Re}S_2\geq M\}\)는 \(\operatorname{Re}\delta=0\)을 통과하지 못한다.
Phase-locked contour의 negative-\(x\)와 positive-\(x\) 끝은 이 reduced one-complex-dimensional
fiber의 서로 다른 good-region components에 있다. 같은 끝으로 갔다 돌아오는 hairpin이라는
이유만으로 `EQUIVALENCE` 처리할 수는 없다.

이 component 판정은 varying \(a\)와 \(T\)까지 함께 infinity로 보내는 full joint relative
homology 판정이 아니다.

## 기존 KILL의 정확한 경계

Straight-lift runner가 exhaust한 변수는

\[
\delta=qy,\qquad q=u+iv,\quad y\in\mathbb R,
\]

즉 \(\delta=0\) anchor를 지나는 homogeneous straight line이다. 이번 affine tail
\(\delta=x+i\psi/\kappa\)는 \(\psi\neq0\)에서 그 class에 속하지 않고, 중앙 window에 붙인 전체
contour도 nonlinear이다. 따라서:

- 기존 Phase-39 straight completion `KILL`은 유지된다.
- 기존 문서의 “all constant straight lines”는 구현된 **anchor-through** scope로 읽어야 한다.
- Affine-translated straight lines나 compactly bent contours까지 KILL했다고 읽으면 과장이다.
- 새 construction은 `EQUIVALENCE`가 아니라 explicit `BRANCH`다.

## 독립 검토와 남은 핵심

두 독립 읽기 검토가 reduced action을 별도로 전개해 같은 real-part identity, 두 normalized limit,
uniform-\(\psi\) split, cutoff gluing과 기존 KILL의 scope 경계를 확인했다. 새 Python/SymPy runner,
root, ODE, evaluator, numerical sample은 실행하지 않았다. 그러므로 이 기록은 exact analytic proof와
독립 algebra review이지 새 execution receipt가 아니다.

계산으로 확인된 사실:

- finite lower-bypass 전체의 fixed-\(a\) scalar \(\phi_1\) fiber에 두 uniform good ends를 갖는
  explicit phase-locked family가 있다.
- 이 family는 원래 중앙 field window와 정확히 같게 compactly bend할 수 있다.
- 기존 no-go는 anchor-through \(\delta=qy\) class의 no-go이지 affine/curved universal no-go가
  아니다.

해석:

- Gate 1의 첫 field-end obstruction에는 실제 탈출구가 있다.
- 다음 최소 discriminator는 이 phase-locked branch가 하나의 source-derived regulator/original
  class에서 선택되는지 여부다.

열린 문제:

- complex \(a_1\) field faces와 mixed \((a_1,\phi_1)\) infinities;
- \(r\to0\), \(R\to\infty\)와 joint escape sequences;
- compact connector가 만드는 추가 upward-manifold crossings;
- complete saddle, upward-cycle, sheet, end와 Stokes census;
- physical original cycle, determinant/Pfaffian/Pin orientation, complete signed vector.

따라서 Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은 `PROHIBITED`이고
`physical_original_cycle`, `global_n_sigma`, physics/TOE claim은 계속 `null`이다.
