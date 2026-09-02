# Gate 1 $m=2$ half-angle product scale-end admissibility audit

> **실행 상태:** `VALID_RUN`
> **계산 판정:** `KILL_PHASE39_HALF_ANGLE_PRODUCT_SCALE_RAY_COMPLETION_ON_DECLARED_FINITE_LAPSE_DOMAIN`
> **인식론적 지위:** `SCOPED_FALSIFIER_OF_ONE_NATURAL_SCALE_COMPLETION`
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 결론부터

Phase 39의 half-angle scale line을 그대로 무한 연장하고, $q=0$ scalar slice를
보존한 채 알려진 scalar good tails와 곱으로 붙이는 가장 자연스러운 completion은
허용되지 않는다. 정확한 $m=2$ action에서 모든 nonzero lapse phase마다 scale 방향의
두 끝 중 하나가

\[
\operatorname{Re}S_2\longrightarrow-\infty
\]

로 가기 때문이다. 따라서 그 끝은 $e^{-S_2}$ relative cycle의 good region에 있지
않다.

이것은 **한 product completion의 KILL**이다. 비대칭 cubic-sector ray,
$q$-dependent scale fiber, 일반 mixed $(a,\phi)$ contour, zero-lapse contact 또는
source-defined joint relative cycle에 대한 no-go가 아니다. Phase 39의 두 local $+1$
후보도 그대로 local record로 남으며 global integer로 승격되지 않는다. 새 물리나
TOE를 발견한 결과가 아니다.

## 고정한 질문과 범위

상속한 equal-endpoint two-segment midpoint action은

\[
S_2=2\pi^2\sum_{e=0}^{1}\left[
\frac{-6a_{e+1/2}(\Delta a_e)^2
+a_{e+1/2}^3(\Delta\phi_e)^2}{2Th}
+Th\{-3a_{e+1/2}+a_{e+1/2}^3V(\phi_{e+1/2})\}
\right],\qquad h=\frac12,
\]

\[
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\phi}\right)^2.
\]

이번 감사에서는

\[
x=a_1-a_\partial,\quad q=\phi_1-\phi_\partial=0,\quad
A=a_\partial+\frac{x}{2},\quad T=\rho e^{i\psi},
\]

\[
x=e^{i(\psi/2-\pi/2)}y,qquad y\in\mathbb R,qquad
\frac15\leq\rho\leq\frac65,\quad -\frac\pi2\leq\psi\leq\frac\pi2
\]

만 검사했다. $q=0$은 Phase-39 cap의 $y_\phi=0$이며, 후속 compact-bent
phase-locked scalar contour가 정확히 보존하는 중앙 window 안에 있다.

## exact reduction

$q=0$에서 두 midpoint element는 같으므로 action은 정확히

\[
S_2=-\frac{24\pi^2A x^2}{T}
+2\pi^2T\{-3A+A^3V_0\},
\qquad V_0=V(\phi_\partial),\quad 0<V_0<\frac34
\]

로 줄어든다. $y^3$ 항의 실수 계수는

\[
L(\psi,\rho)
=\pi^2\left[
\frac{12\sin(\psi/2)}{\rho}
-\frac{V_0\rho}{4}\sin\frac{5\psi}{2}
\right].
\]

$u=\psi/2\in(0,\pi/4]$에 대해

\[
5\sin u-\sin5u
=4\sin^3u\left(5-4\sin^2u\right)>0.
\]

따라서

\[
\frac{L}{\pi^2}
=\left(\frac{12}{\rho}-\frac{5V_0\rho}{4}\right)\sin u
+\frac{V_0\rho}{4}(5\sin u-\sin5u)>0.
\]

선언된 상한에서 첫 괄호의 uniform margin은

\[
\frac{12}{6/5}-\frac{5(3/4)(6/5)}4=\frac{71}{8}>0
\]

이다. $L$은 $\psi$의 odd function이므로

\[
\operatorname{sign}L=\operatorname{sign}\psi\qquad(\psi\ne0).
\]

결국 $\psi>0$에서는 $y\to-\infty$, $\psi<0$에서는
$y\to+\infty$가 cubic bad end다.

고립된 $\psi=0$ slice에서는 cubic real part가 0이고 quadratic coefficient가

\[
\pi^2a_\partial\left(\frac{24}{\rho}-\frac32\rho V_0\right)>0
\]

이다. 괄호의 uniform margin은 $373/20$이므로 이 한 slice의 두 끝은 좋다.
그러나 주변의 모든 nonzero $\psi$에 존재하는 bad end를 없애지는 않는다.

## 독립 수치 control

수치 control은 축약된 cubic 식을 action evaluator로 사용하지 않았다. 원래 두-element
complex action을 80 decimal digits로 직접 평가했다.

- $(\rho,\psi)$ 8쌍: 세 arm radii의 $\psi=\pm\pi/2$와
  $\rho=3/10$, $\psi=\pm\pi/4$
- 각 쌍에서 $|y|=10^4,4\times10^4,1.6\times10^5$
- 총 24 samples, root/ODE/quadrature 0

모든 sample에서 predicted bad 방향의 $\operatorname{Re}S_2/|y|^3$는 음수였다.
8개 error sequence가 모두 단조 감소했고 마지막 relative error는
$6.31\times10^{-5}$에서 $1.17\times10^{-4}$ 사이로, 사전 고정한
$5\times10^{-4}$보다 작았다. conjugate arms의 최대 직접-action residual은
$1.08\times10^{-78}$이었다.

## 실행과 provenance

정본 실행은 다음 하나다.

```text
./ice run gate1_m2_scale_half_angle_end_admissibility
```

관측 출력:

```text
run_status=VALID_RUN
verdict=KILL_PHASE39_HALF_ANGLE_PRODUCT_SCALE_RAY_COMPLETION_ON_DECLARED_FINITE_LAPSE_DOMAIN
exact=10/10 PASS
numerical=3/3 PASS
theorem_guards=4/4 VERIFIED
sampling_points=24
automatic_next=null
```

| 항목 | 값 |
| --- | --- |
| runner definition commit | `f2dd4d1efa6ff160d0c0b0eb1e26b7b4dc7e06e3` |
| input SHA-256 | `09c9e20caad28dcde82e2b7bde318f2fb9901b850786ea9b2238af0ce156234c` |
| runner SHA-256 | `91fee2af3ca78fb6f06134613b11751eb242644d5542fc8eee7665032072f30c` |
| result SHA-256 | `ea0aa4ec3c7e9965e0d9e1f4a4731d848fd9d7b8ac6ccc48729070332b3f46de` |
| payload digest | `8dc8fb867819a57c45972e48c5a6b27d0c2e49f9db399c183c2809f99763356e` |
| result bytes | `16,127` |
| environment | Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0 |

독립 read-only 감사가 canonical payload digest, input/runner/upstream hashes, exact
계수와 두 margin, 8개 convergence sequence, arm conjugation 및 모든 fail-closed null을
재계산해 통과시켰다. runner를 재실행하거나 결과를 수정하지 않았다.

## 남은 문제

이번 결과 뒤에도 다음은 열린 상태다.

- asymmetric cubic-sector 또는 $q$-dependent fibered scale tails
- complete scale/scalar mixed-corner end census
- source-derived gauge/BFV joint cycle과 source-to-thimble deformation
- zero-lapse glue/contact selection과 regulator removal
- full determinant/Pfaffian orientation과 complete global signed intersection vector
- nonreal singular Weyl $m(z)$, spectral measure, RAQ와 physical product
- empirical discriminator, physics claim과 TOE claim

다음 설계가 성공하려면 적어도 scale tail이 lapse phase에 따라 서로 다른 cubic good
sectors를 선택하거나, $q$와 함께 휘어져 이 $q=0$ product bad end를 무한 경계에서
유지하지 않아야 한다. 이는 설계 제약이지 다음 계산의 자동 승인이나 존재 증명은 아니다.

## 1차 문헌 경계

- Witten, [*Analytic Continuation Of Chern-Simons Theory*](https://arxiv.org/abs/1001.2933),
  §§3.1.1, 3.1.5: relative cycle과 good-end/Morse framework만 재사용한다. 이 model의
  action이나 original cycle을 공급하지 않는다.
- Banihashemi–Jacobson,
  [*On the lapse contour in the gravitational path integral*](https://arxiv.org/abs/2405.10307v3):
  그 논문의 integration order에서 below-origin lapse prescription을 비교하는 데만 쓴다.
  Phase-39 scale lift나 bad field end를 선택·수정하지 않는다.

정본 machine ledger는
[`GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_RESULT.json`](GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_RESULT.json)이다.
