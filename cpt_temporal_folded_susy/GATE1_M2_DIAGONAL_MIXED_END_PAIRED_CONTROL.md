# Gate 1 $m=2$ diagonal mixed action end with paired sign control

> **실행 상태:** `VALID_RUN`
> **계산 판정:** `KEEP_SCOPED_DIAGONAL_MIXED_ACTION_END_WITH_SIGN_CONTROL`
> **대조군 판정:** `KILL_SIGN_FLIPPED_DIAGONAL_MIXED_ACTION_END`
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 결론부터

finite nonzero-lapse envelope 전체에서 scale과 scalar를 함께 무한대로 보내는 한 대각선

\[
x=s,\qquad q=s e^{i\psi/2},\qquad
T=\rho e^{i\psi},\qquad s\longrightarrow+\infty
\]

을 검사했다. 선언된 범위

\[
\frac15\leq\rho\leq\frac65,
\qquad -\frac\pi2\leq\psi\leq\frac\pi2
\]

에서 이 tail은 정확히

\[
\operatorname{Re}S_2
\geq \frac{989\pi^2}{122880}s^5>0
\qquad(s\geq48)
\]

를 만족한다. 따라서 `exp(-S_2)`의 **한 scoped action-decay 후보**로 남길 수 있다.

같은 $q,T$에서 $x=-s$로 부호만 바꾼 false-signal control은

\[
\operatorname{Re}S_2
\leq-\frac{181\pi^2}{69120}s^5<0
\qquad(s\geq36)
\]

이므로 확실한 bad action tail이다. 이 반대 부호 대조군이 함께 통과했기 때문에, 양의 결과를
$q^2/T$의 complex phase 처리나 실수부 부호 오류가 만든 가짜신호로 볼 가능성을 줄였다.

이것은 complete mixed-end census가 아니다. compact Phase-39 chain과의 connector, amplitude와
measure, 다른 scale--scalar 비율과 phase, source-defined relative cycle 및 signed global
intersection vector는 전혀 정해지지 않았다. 새 물리나 TOE 결과도 아니다.

## 왜 이 질문을 골랐는가

처음 고려한 $H(q,T)=0$ transition 단독 감사는 정확한 supporting calculation이지만,
graph-aware planner에서 TOE 핵심 경로의 current blocker가 아닌 것으로 판정됐다. 그 runner는
실행하거나 커밋하지 않았다.

질문을 정본 open node
`open:gate1-original-cycle-signed-global-intersections`의 mixed-boundary census에 직접 연결한 뒤
planner를 다시 실행했고, 다음을 얻었다.

- routing classification: `CURRENT_BLOCKER_CANDIDATE`
- checkpoint: `research-agent:ba782db61c0f82ed34b3`
- missing typed object: incomplete end census에 들어갈 한 scoped action-decay 후보 기록
- bounded output: 한 diagonal tail의 uniform real-action bound
- false-signal control: 같은 $q,T$에서 $x=-s$가 반대 부호를 내는지 확인

Planner 자체는 실행 권한을 주지 않는다. 현재 사용자 요청을 human review로 읽되, 계산 결과를
current blocker 전체의 해결이라고 세지 않는 범위로 고정했다.

## 정확한 action과 phase cancellation

경계값을 $a_\partial,\phi_\partial$라 하고

\[
A=a_\partial+\frac{x}{2},\qquad
\Phi=\phi_\partial+\frac q2,
\]

\[
V(\Phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\Phi}\right)^2
\]

로 두면, 원래 두 element를 직접 더한 equal-endpoint $m=2$ action은

\[
S_2=-\frac{24\pi^2Ax^2}{T}
 +\frac{4\pi^2A^3q^2}{T}
 +2\pi^2T\left(-3A+A^3V(\Phi)\right).
\]

선언된 scalar/lapse correlation에서는

\[
\frac{q^2}{T}
=\frac{s^2e^{i\psi}}{\rho e^{i\psi}}
=\frac{s^2}{\rho}>0
\]

가 정확히 성립한다. 따라서 scalar kinetic term이 mixed scaling의 $s^5$ leading order를
결정한다.

### 양의 diagonal

$x=s$이면 $A=a_\partial+s/2$이고 scalar kinetic polynomial은

\[
P_+(s)=\frac{\pi^2}{\rho}
\left(\frac{s^5}{2}+3a_\partial s^4
+6a_\partial^2s^3+4a_\partial^3s^2\right).
\]

따라서

\[
\lim_{s\to\infty}\frac{\operatorname{Re}S_2}{s^5}
=\frac{\pi^2}{2\rho}>0.
\]

### 부호 반전 control

$x=-s$이면 $A=a_\partial-s/2$이고

\[
P_-(s)=\frac{\pi^2}{\rho}
\left(-\frac{s^5}{2}+3a_\partial s^4
-6a_\partial^2s^3+4a_\partial^3s^2\right),
\]

\[
\lim_{s\to\infty}\frac{\operatorname{Re}S_2}{s^5}
=-\frac{\pi^2}{2\rho}<0.
\]

이 control은 $A$가 음수가 되는 asymptotic polynomial direction에서 action 부호만 검산한다.
물리적 scale branch나 두 번째 admissible contour라고 해석하지 않는다.

## uniform remainder bound

$|\psi|\leq\pi/2$이면 $\cos(\psi/2)\geq1/\sqrt2$다. 또한
$\phi_\partial>1$, $\sqrt{2/3}>4/5$, $e^{4/5}>2$이므로 선언된 두 tail에서

\[
\left|e^{-\sqrt{2/3}\,\Phi}\right|<\frac12,
\qquad |V(\Phi)|<\frac{27}{16}.
\]

$a_\partial<4$와 lapse bounds를 함께 사용하면 양의 tail에서

\[
\left|\operatorname{Re}(S_2-P_+)\right|
<\pi^2\frac{150633}{160}s^3.
\]

여기서 상수는 scale kinetic $540$, lapse-linear $162/5$, bounded-potential
$59049/160$을 따로 계산해 더한 값이다. $P_+\geq(5\pi^2/12)s^5$이고 $s\geq48$이면

\[
\frac{\operatorname{Re}S_2}{s^5}
\geq\pi^2\left(\frac5{12}-\frac{150633}{160s^2}\right)
\geq\frac{989\pi^2}{122880}>0.
\]

control에서는 $s\geq16$일 때 $A\leq-s/4$이고

\[
P_-(s)\leq-\frac{5\pi^2}{96}s^5,
\qquad
\left|\operatorname{Re}(S_2-P_-)\right|
<\pi^2\frac{10257}{160}s^3.
\]

$s\geq36$이면 앞의 음의 upper bound가 나온다. 두 결론 모두 $\rho,\psi$ 전체에 균일하다.

## 원래 action 수치 대조

runner는 추출된 leading polynomial을 수치 evaluator로 재사용하지 않고, 원래 두 midpoint
element를 80-digit complex arithmetic으로 직접 더했다. 표본은

- $\rho\in\{1/5,7/10,6/5\}$,
- $\psi/\pi\in\{-1/2,0,1/2\}$,
- $s\in\{2000,8000,32000\}$,
- $x/s\in\{+1,-1\}$

의 $54$개다.

검산 결과:

- positive diagonal의 최소 $\operatorname{Re}S_2/s^5$: `4.11508591544112058` $>0$;
- sign-flipped control의 최대 $\operatorname{Re}S_2/s^5$: `-4.06846422556604782` $<0$;
- 마지막 반경의 최대 leading-coefficient 상대오차:
  `0.000668924696806123 < 0.002`;
- 모든 18개 sequence의 오차가 strict decrease;
- exact one-sided bound의 최소 여유: `0.00275982234472288 > 0`;
- $q^2/T=s^2/\rho$ 최대 상대잔차: 약 $9.91\times10^{-82}$;
- $\psi\leftrightarrow-\psi$ conjugation 상대잔차: `0`;
- sampled $|V|$ 최대값: `0.75 < 27/16`.

독립 read-only 감사가 raw result와 self-excluding digest, input/runner 및 다섯 upstream hash,
54개 sample의 부호·bound·수렴과 모든 fail-closed output을 다시 확인했다.

## 실제 실행과 provenance

source/input 선행 commit:

```text
65344030ea690c08ec046aa408d36eb0cef6c0c3
```

실행 명령:

```bash
./ice run gate1_m2_diagonal_mixed_end_paired_control
```

stdout:

```text
VALID_RUN
KEEP_SCOPED_DIAGONAL_MIXED_ACTION_END_WITH_SIGN_CONTROL
KILL_SIGN_FLIPPED_DIAGONAL_MIXED_ACTION_END
exact=10/10
numerical=6/6
theorem_guards=5/5
samples=54
gate1=OPEN_PARTIAL_PROGRESS
global_promotion=PROHIBITED
automatic_next=null
```

- input SHA-256: `ed4d7835c3672832b522c50b2e774afab161df45163bdd361651ea3ffdc94057`
- runner SHA-256: `55172b2dc4324660ebfd734fda2b841d5966cacc187f0089ed919d0e0de19ea5`
- raw result SHA-256: `089962d1f2452e4906eb103ab647bf305aeec72cf02d621727d977829d5f7ca9`
- payload digest: `d932d09a115246eb0974f2e4530a5bd104160986e98be7db06558c863ee18647`
- result size: `45,126` bytes
- environment: Python `3.13.5`, SymPy `1.14.0`, mpmath `1.3.0`

Payload digest는 저장된 execution timestamp를 포함하므로 내부 무결성 검사는 재현되지만,
서로 다른 재실행 사이에 같은 digest를 요구하는 run-invariant identifier는 아니다.

## 계산된 사실과 아직 열려 있는 것

계산된 사실:

- 하나의 명시적 correlated scale--scalar direction은 finite lapse envelope 전체에서 uniform
  positive action decay를 갖는다.
- 같은 scalar/lapse phase에서 scale sign을 뒤집으면 uniform bad action direction이 된다.
- direct original-action evaluator가 두 반대 leading sign을 구분한다.

해석:

- incomplete Gate-1 end census에 **한 action-decay 후보 기록**을 추가할 수 있다.
- positive result는 phase bookkeeping에 무감각한 자동 양성값이 아니다.

계속 열린 문제:

- 모든 weighted scale--scalar ratio, scalar phase, coordinate face와 joint escape의 exhaustion;
- 이번 ray를 compact cap 또는 source-derived regulated original cycle에 붙이는 connector/homotopy;
- amplitude, determinant/Pfaffian line, measure와 lapse endpoint;
- complete saddle, singularity, Stokes, upward-cycle와 oriented intersection census;
- singular Weyl $m(z)$, spectral measure, RAQ, observable와 likelihood;
- physics claim과 TOE claim.

따라서 `complete_mixed_end_census`, `physical_original_cycle`, `global_n_sigma`, physics 및 TOE는
모두 `null`이고 Gate 1은 닫히지 않았다.

## 1차 문헌 경계

- Witten, [*Analytic Continuation Of Chern-Simons Theory*](https://arxiv.org/abs/1001.2933),
  §3의 relative good-end 언어만 사용한다. 이 계산은 full relative pair, Lefschetz thimble,
  homology basis 또는 original cycle을 구성하지 않는다.
- Hien, [*Periods for rank 1 irregular singular connections on
  surfaces*](https://arxiv.org/abs/math/0505474)의 rapid-decay homology는 compactification,
  normal-crossing divisor와 good meromorphic irregular connection을 요구한다. 여기서는 그
  가정을 만들지 않았으므로 직접 action bound를 Hien 정리의 적용으로 부르지 않는다.
- Starobinsky exponential 때문에 원래 scalar 좌표에서 phase는 polynomial이 아니다. complex
  cover, logarithmic branch, amplitude와 divisor data 없이 Newton-polyhedron 또는 toric
  compactification 기준을 적용하지 않았다.

정본 machine ledger는
[`GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_RESULT.json`](GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_RESULT.json)이다.
