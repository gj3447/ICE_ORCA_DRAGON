# Gate 1 $m=2$ asymmetric scale-tail pair

> **실행 상태:** `VALID_RUN`
> **계산 판정:** `KEEP_SCOPED_ASYMMETRIC_SCALE_TAIL_PAIR_ON_DECLARED_FINITE_WINDOW`
> **인식론적 지위:** `SCOPED_CONSTRUCTIVE_SCALE_END_CERTIFICATE`
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 결론부터

직전 계산에서 KILL된 것은 선언된 $q=0$ finite nonzero-lapse 범위에서 Phase 39의
antipodal half-angle **product line**을 그대로 연장하는 방식이었다. 그 결과는 scale
방향의 모든 contour에 대한 no-go가 아니다. 이번 계산은 서로 $2\pi/3$ 떨어진 두 개의
비대칭 ray를 scale box의 양쪽 face에 따로 붙였다. 그 결과, 기존의 compact scalar
window와 finite nonzero-lapse envelope 전체에서 두 scale end 모두

\[
\operatorname{Re}S_2\longrightarrow+\infty
\]

로 간다는 uniform exact certificate를 얻었다. 따라서 이 두 end는 $e^{-S_2}$
convention에서 sectorially good하다.

이것은 **scale face 두 개만 살린 결과**다. scalar infinity, scale--scalar mixed
corner, full relative chain, source-defined original cycle, zero lapse, orientation 또는 global
intersection을 만들지 않는다. 새 물리나 TOE를 발견한 결과도 아니다.

## 고정한 범위

Phase-39의 equal-endpoint two-segment midpoint action에서

\[
x=a_1-a_\partial,\qquad q=\phi_1-\phi_\partial,\qquad
A=a_\partial+\frac{x}{2},\qquad \Phi=\phi_\partial+\frac q2,
\]

\[
T=\rho e^{i\psi},\qquad
\frac15\leq\rho\leq\frac65,\qquad
-\frac\pi2\leq\psi\leq\frac\pi2,
\]

\[
q=e^{i\psi/2}y_\phi,\qquad |y_\phi|\leq\frac14
\]

를 사용했다. $\rho$ envelope은 직전 scale-end audit이 선언한 finite envelope이며,
$|y_a|,|y_\phi|\leq1/4$ face는 Phase-39 local field box에서 온다. $q$를 무한대로
보내거나 $T\to0,\infty$를 취하지 않는다.

## 일반 bounded-$q$ scale polynomial

두 midpoint element를 원래 식에서 다시 합치면

\[
S_2=-\frac{24\pi^2Ax^2}{T}
+\frac{4\pi^2A^3q^2}{T}
+2\pi^2T\{-3A+A^3V(\Phi)\},
\]

\[
V(\Phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\Phi}\right)^2.
\]

$q,T$를 고정했을 때 $x$에 대한 cubic coefficient는 정확히

\[
\mathcal A_3(q,T)=\pi^2\left[
\frac{-12+q^2/2}{T}+\frac{T}{4}V(\Phi)
\right]
\]

이다. 이번 계산은 직전 $q=0$ 축약 계수를 복사하지 않고 일반 $q$ action에서 이
계수를 다시 추출했다.

## 두 비대칭 ray

Phase-39 local scale angle과 face radius를

\[
\beta=\frac\psi2-\frac\pi2,\qquad R=\frac14
\]

로 놓고 $r\geq R$에서

\[
x_R(r)=R e^{i\beta}+e^{i\alpha_R}(r-R),
\qquad \alpha_R=\frac\psi3-\frac\pi3,
\]

\[
x_L(r)=-R e^{i\beta}+e^{i\alpha_L}(r-R),
\qquad \alpha_L=\frac\psi3+\frac\pi3
\]

를 선언했다. $r=R$에서 각각 기존 $y_a=+1/4$와 $y_a=-1/4$ face에 정확히
붙는다. 접선까지 매끈하게 맞춘 connector가 아니라, face에서 corner를 허용한
continuous piecewise-smooth attachment다.

두 방향은 antipodal하지 않고

\[
\alpha_L-\alpha_R=\frac{2\pi}{3},\qquad
e^{3i\alpha_R}=e^{3i\alpha_L}=-e^{i\psi}
\]

를 만족한다. 또한 complex conjugation은 $(R,\psi)$ tail을 $(L,-\psi)$ tail로
교환한다.

## uniform positive margin

$|q|\leq1/4$이고 $\phi_\partial>1$이므로
$\operatorname{Re}\Phi>7/8$. 또한 $\sqrt{2/3}>4/5$이고, 양의 Taylor 항만 쓴

\[
\sum_{n=0}^{4}\frac{(7/10)^n}{n!}>2
\]

로부터 $e^{-7/10}<1/2$를 얻는다. 따라서

\[
|V(\Phi)|
<\frac34\left(1+\frac12\right)^2
=\frac{27}{16}.
\]

어느 쪽 ray에서도 cubic real coefficient는 같고

\[
\frac{1}{\pi^2}\operatorname{Re}
\left(\mathcal A_3e^{3i\alpha_{R,L}}\right)
=\operatorname{Re}\left[
\frac{12-q^2/2}{\rho}
-\frac{\rho e^{2i\psi}}4V(\Phi)
\right].
\]

따라서 선언된 window 전체에서

\[
\frac{1}{\pi^2}\operatorname{Re}
\left(\mathcal A_3e^{3i\alpha_{R,L}}\right)
>
\frac{12-1/32}{6/5}-\frac{(6/5)(27/16)}4
=\frac{9089}{960}>0.
\]

$S_2$는 각 fixed $(q,T)$ fiber에서 정확한 cubic polynomial이다. 남은 quadratic
이하 계수와 두 face offset은 compact parameter window에서 continuous하고 bounded하다.
그러므로 하나의 공통한 충분히 큰 radius 이후에는 cubic 하한이 lower-order 항을
지배하며, 두 tail에서 uniform하게 $\operatorname{Re}S_2\to+\infty$다.

## 직전 KILL과의 관계

직전 half-angle line은 한 straight parameter line이어서 두 방향이 $\pi$만큼 떨어진
antipodal pair였다. cubic polynomial은 그 두 끝에서 부호가 반대가 되므로 nonzero
lapse phase마다 한쪽이 나빴다. 이번 두 ray는 $2\pi/3$ 떨어져 cube가 같다. 따라서

- 이전 KILL은 그대로 유효하고,
- 이번 KEEP도 동시에 유효하며,
- 결론은 “straight product shortcut은 실패하지만 다른 scale sectors는 존재한다”이다.

Phase-39의 두 local $+1$ 기록은 여전히 local record일 뿐이며, 이번 ray가 그 값을
global integer로 승격하지 않는다.

## 독립 원식 수치 control

수치 control은 cubic polynomial을 action evaluator로 쓰지 않았다. 80 decimal digits로
원래 두-element action을 직접 평가했다.

- $\rho\in\{1/5,6/5\}$
- $\psi/\pi\in\{-1/2,0,1/2\}$
- $y_\phi\in\{-1/4,0,1/4\}$
- left/right 두 tail
- $r\in\{10^3,4\times10^3,1.6\times10^4\}$
- 총 108 samples, root/ODE/quadrature 0

exact coefficient floor는
$\pi^2(9089/960)=93.442535834897\ldots$이고 sampled predicted minimum은
$97.621051317075\ldots$였다. 108개 모두 $\operatorname{Re}S_2/r^3>0$였으며
finite-radius minimum은 $97.641721878977\ldots$였다. 각 36개 radius sequence의
마지막 relative error는 사전 선언한 $5\times10^{-3}$보다 작았고, 전체 maximum은
$3.9182\times10^{-4}$였다. conjugation-pair residual은 80-digit evaluation에서 0이었다.

## 실행과 provenance

정본 실행은 다음 하나다.

```text
./ice run gate1_m2_asymmetric_scale_tail_pair
```

관측 출력:

```text
run_status=VALID_RUN
verdict=KEEP_SCOPED_ASYMMETRIC_SCALE_TAIL_PAIR_ON_DECLARED_FINITE_WINDOW
exact=11/11 PASS
numerical=4/4 PASS
theorem_guards=5/5 VERIFIED
sampling_points=108
automatic_next=null
```

| 항목 | 값 |
| --- | --- |
| runner definition commit | `e2d61f9df86325e56abb13413ae5164b3866ea6f` |
| input SHA-256 | `aa7021ec68c1910ae458bfbab7cdf13e4d3234ade93fbdbaf9484f6586c270ce` |
| runner SHA-256 | `49f6c48dd1acb311d95f26e320a0f029666815197d826035875a5d4ecb653b2d` |
| result SHA-256 | `36fdf578fc249b154d626b8baa341907c27998562c53d346402009bad45d2930` |
| payload digest | `6ae298ae5dc2ab3d989415cb90940db646f7ff6a250a66a12f86485e4a83c8ce` |
| result bytes | `44,620` |
| observed wall time | `3.293 s` |
| environment | Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0 |

독립 read-only 감사가 canonical payload digest, input/runner/upstream hashes, 일반-$q$
cubic coefficient, potential bound, $9089/960$ margin, 108개 원식 표본, 36개 convergence
sequence, conjugation pair와 모든 fail-closed null을 재계산해 통과시켰다. runner를
재실행하거나 결과를 수정하지 않았다.

## 남은 실제 병목

이번 결과 뒤에도 다음은 열린 상태다.

- $q\to\pm\infty$ scalar ends와 correlated scale--scalar mixed corners
- cubic-degeneracy locus에서 quadratic 이하 항까지 포함한 $q$-dependent fiber 전이
- complete joint end/singularity/Stokes census와 full relative chain
- source-derived gauge/BFV original cycle과 source-to-thimble deformation
- $T\to0$, lapse infinity, contact/gluing 및 regulator removal
- determinant/Pfaffian orientation과 complete global signed intersection vector
- singular Weyl $m(z)$, spectral measure, RAQ, physical product
- empirical discriminator, physics claim과 TOE claim

다음 계산은 일반 coefficient

\[
H(q,T)=2q^2-48+T^2V(\phi_\partial+q/2)
\]

의 zero와 scalar asymptotic sectors를 포함하는 **사전 선언된 unbounded
$q$-dependent fiber 하나**를 검사해야 한다. $H=0$을 곧바로 bad end나 no-go로
부르면 안 되며, 그 지점에서는 quadratic 이하 계수로 판정을 내려야 한다. 이것은 다음
설계 제약이지 자동 실행 승인이나 존재 증명이 아니다.

## 1차 문헌 경계

- Witten, [*Analytic Continuation Of Chern-Simons Theory*](https://arxiv.org/abs/1001.2933),
  §3: relative-cycle와 good-end/Morse framework만 재사용한다. 이 model의 action,
  source cycle 또는 coefficient를 공급하지 않는다.
- Pham, [*La descente des cols par les onglets de Lefschetz, avec vues sur
  Gauss--Manin*](https://www.numdam.org/item/AST_1985__130__11_0.pdf): polynomial
  Laplace integral의 infinity singularity 경고를 비교 기준으로만 쓴다. 이번 계산은 full
  infinity census가 아니다.
- Hien, [*Periods for rank 1 irregular singular connections on
  surfaces*](https://arxiv.org/abs/math/0505474): meromorphic rapid-decay homology에 필요한
  compactification/divisor data를 비교 기준으로만 쓴다. 그런 global data를 얻었다고
  간주하지 않는다.

정본 machine ledger는
[`GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_RESULT.json`](GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_RESULT.json)이다.
