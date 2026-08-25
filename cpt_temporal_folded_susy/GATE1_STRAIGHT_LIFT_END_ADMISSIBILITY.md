# Gate 1 — straight-lift relative-end admissibility

## 결과

번호 없는 bounded 계산 `Gate1StraightLiftEndAdmissibility`는 Phase 39의 \(m=2\)
finite-window configuration chain을 endpoint anchor를 지나는 상수 방향 직선 field line으로 무한 연장하는 후보를
배제한다.

```text
run_status           = VALID_RUN
candidate_decision   = KILL
model_class_decision = KILL_CONSTANT_STRAIGHT_FIELD_LINES_ON_DECLARED_SLICE
programme_impact     = NARROW
Gate 1               = OPEN_PARTIAL_PROGRESS
global_n_sigma       = null
automatic_next       = null
```

이는 Phase 39의 finite-window local intersection 후보와 두 local sign \(+1\)을 취소하지
않는다. 배제되는 것은 fixed-\(a\), pure-imaginary-lapse \(m=2\) slice에서의 **무한 상수
직선 \(\phi\)-completion**이다. 여기서 result의 `CONSTANT_STRAIGHT`는 frozen runner가 실제로
case split한 \(\delta=qy\), 즉 anchor-through homogeneous line을 뜻한다. Affine-translated line은
그 class에 포함되지 않는다. Curved/piecewise field contour,
nonzero-\(\operatorname{Re}T\) lateral, 다른 regulator와 full joint/BFV cycle은 열려 있다.

## 입력, source와 convention

실행 전에 다음을 동결했다.

- input: `GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_INPUTS.json`, SHA-256
  `a3bc97461c7989cd5bb471accf46f0c2196de41c3030e9eef2248c4f09a47fdb`;
- runner: `gate1_straight_lift_end_admissibility.py`, SHA-256
  `c2cfac73e303d0f46d86c1577fc31cc1cd2ff5e0dfd809e9bdd6b75a38aaaa7e`;
- Phase-39 inherited input SHA-256:
  `b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4`;
- integrand convention: \(e^{-S_2}\);
- singular divisor: \(T=0\), inherited lower bypass;
- exact caps: 30 seconds, 250,000-byte result, root/ODE/evaluator calls 0,
  automatic descendants 0.

[Witten, *Analytic Continuation Of Chern-Simons Theory*, arXiv:1001.2933v4,
§3.1.1](https://arxiv.org/abs/1001.2933)은 \(e^{\mathcal I}\) 적분의 noncompact
relative-cycle 끝이 \(\operatorname{Re}\mathcal I\to-\infty\)인 영역에 있어야 함을
정식화한다. 여기서는 \(\mathcal I=-S_2\)이므로 필요한 good-end 조건은

\[
\operatorname{Re}S_2\longrightarrow+\infty
\]

이다. 이 source는 현재 중력 action이나 물리 원본 cycle을 선택하지 않는다.
[Banihashemi–Jacobson, *On the lapse contour in the gravitational path integral*,
arXiv:2405.10307](https://arxiv.org/abs/2405.10307)은 momenta를 lapse보다 먼저 적분하는
configuration representation에서 below-origin contour를 지지하지만, field lift의 모양이나
수렴성을 정하지 않는다.

## 정확 계산

Phase 39 action에서

\[
a_1=a_\partial,\qquad
\phi_1=\phi_\partial+q_s y,\qquad
q_s=e^{s i\pi/4},\qquad
T=s iN_0,\quad s=\pm1,\quad N_0>0
\]

로 두면 같은 two-element scalar가 정확히

\[
S_2=2\pi^2\left[
\frac{2a^3q_s^2y^2}{s iN_0}
+s iN_0\left(-3a+\frac34a^3
\left(1-e^{-\kappa(\phi+q_sy/2)}\right)^2\right)
\right],
\qquad \kappa=\sqrt{\frac23}
\]

로 축약된다.

### Phase-39 ray의 명시적 bad end

\(y=-t\)에서

\[
t_j=\sqrt3\left(\frac\pi2+2\pi j\right),\qquad
A_j=e^{-\kappa\phi+t_j/(2\sqrt3)}
\]

를 선택하면 양·음 lapse arm이 정확히 같은 real part를 갖고

\[
\operatorname{Re}S_2(-t_j)
=2\pi^2a^3\left[
\frac{2t_j^2}{N_0}
-\frac{3N_0}{4}\left(A_j^2-\sqrt2(-1)^jA_j\right)
\right].
\]

따라서

\[
\lim_{j\to\infty}e^{-t_j/\sqrt3}
\operatorname{Re}S_2(-t_j)
=-\frac32\pi^2N_0a^3e^{-2\kappa\phi}<0.
\]

즉 이 escape sequence에서 \(\operatorname{Re}S_2\to-\infty\)이고
\(|e^{-S_2}|\to\infty\)다. 반대쪽 \(y=+t\)에서는 Starobinsky exponential이 감쇠하고

\[
\frac{\operatorname{Re}S_2(+t)}{t^2}
\longrightarrow\frac{4\pi^2a^3}{N_0}>0,
\]

이므로 한쪽 끝만 좋다. Relative cycle에는 양쪽 끝이 필요하므로 straight completion은
admissible하지 않다.

### 상수 직선 model class

더 일반적으로 \(q=u+iv\), \(T=s iN_0\)이면

\[
\operatorname{Re}S_{\mathrm{kinetic}}
=\frac{8\pi^2a^3}{N_0}\,suv\,y^2.
\]

세 disjoint case가 모든 상수 직선을 소진한다.

1. \(suv<0\): \(uy>0\)인 exponential-decay end에서 음의 quadratic가
   \(-\infty\)로 간다.
2. \(uv=0\): kinetic real part가 0이고 적어도 한 끝에서 potential real part가 0 또는
   bounded라 \(+\infty\) good end가 아니다.
3. \(suv>0\): kinetic은 양수지만 exponential-growth end에서
   \(t_j=(\pi/2+2\pi j)/(\kappa|v|)\) subsequence의 음의 full-rate exponential이
   quadratic와 half-rate 항을 압도한다.

따라서 이 declared slice에서는 어떤 anchor-through homogeneous complex straight
\(\phi\)-line \(\delta=qy\)도 두 field end를
모두 good으로 만들지 못한다.

## 실제 실행과 독립 검산

실행 명령:

```bash
./ice run cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility
```

실제 stdout 요약:

```text
run_status=VALID_RUN
classification=GATE1_PHASE39_STRAIGHT_FIELD_RAY_COMPLETION_HAS_BAD_NEGATIVE_PHI_ENDS
exact_checks=14
numerical_checks=5
candidate_decision=KILL
model_class_decision=KILL_CONSTANT_STRAIGHT_FIELD_LINES_ON_DECLARED_SLICE
programme_impact=NARROW
gate1_decision=OPEN_PARTIAL_PROGRESS
global_n_sigma=null
automatic_next=null
result_bytes=13624
```

환경은 Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0,
Linux `7.0.14-5-pve` x86_64였다. 명령 호출부에서 관측한 wall time은 2.42초였다.

독립 numerical path는 축약된 real-part 식을 다시 평가하지 않고, 원래 두 element를 80-decimal
precision complex arithmetic으로 직접 합산했다.

- bad-end closed form과 full action 최대 상대오차: \(2.1420019\times10^{-79}\);
- 양·음 arm real part 최대 상대차: \(0\);
- \(j=6\) leading-scale ratio: \(-0.999999990353330728\), \(-1\)과 거리
  \(9.6466693\times10^{-9}\);
- positive end \(t=80\)에서
  \(\operatorname{Re}S/t^2=1791.41900450776356\), exact coefficient
  \(1791.41900450775594\)와 상대오차 \(4.2508589\times10^{-15}\).

result 파일 SHA-256은
`821fbd88601b886acdd02fc77d5a877d7f6f8257454c9d3f39aa033b644b99b9`, self-field를 제외한
canonical payload SHA-256은
`b7b90718ca963a4ee22c97d02cac52699b0e7e95d4eb93d5856264cd1cd92b93`다. 후자는 별도
`jq -cS` 경로로 다시 계산해 일치시켰다.

### 실행 후 독립 구현 감사

고정 runner와 result는 실행 provenance를 보존하기 위해 수정하지 않았다. 별도 읽기 검토에서
결론을 바꾸는 식·부호·수치 오류는 발견되지 않았지만 다음 구현 한계를 확인했다.

- `exact_checks=14`는 result entry 수다. 이 중 12개는 SymPy identity/limit를 실제로
  평가하고, `G1.guard.bad_end_short_circuits_global_outputs`와
  `G1.model_class.constant_straight_line_cases_are_exhaustive` 두 개는 runner가 literal `True`로
  기록한 선언적 guard다. 독립 검토는 각각 bad escape sequence에서 global promotion을 금지하는
  정책과 \(suv<0\), \(uv=0\), \(suv>0\)의 상호 배타적·완전한 경우분할을 따로 확인했다.
- `exact_calculation.unscaled_exponential_limit`는 실제로
  \(\lim e^{-t_j/\sqrt3}\operatorname{Re}S_2(-t_j)\)의 계수다. payload의 필드명만 부정확하며
  바로 옆 `bad_subsequence_scaled_limit`와 본문 식을 정본 의미로 읽는다.
- nested decision 문자열 `...ON_FIXED_A_PURE_IMAGINARY_LAPSE_SLICE`와 top-level
  `...ON_DECLARED_SLICE`는 같은 동결 slice를 가리키는 두 표기다. 기계 판정은 top-level
  `model_class_decision`을 정본으로 사용한다.
- `KILL_CONSTANT_STRAIGHT_FIELD_LINES...`라는 result label은 intercept 없는 frozen ansatz
  \(\delta=qy\)의 표기다. 이후 exact analytic review는 phase-locked affine tail
  \(\delta=x+i\arg(T)/\kappa\)가 두 good ends를 가질 수 있음을 보였다. 따라서 이 label을
  모든 affine straight line의 no-go로 확장하지 않는다. 별도 construction과 경계는
  [`GATE1_PHASE_LOCKED_AFFINE_FIELD_END_CONSTRUCTION.md`](GATE1_PHASE_LOCKED_AFFINE_FIELD_END_CONSTRUCTION.md)에
  기록한다.

## 계산된 사실, 해석, 열린 문제

계산된 사실:

- Phase-39 두 arm의 직선 \(\phi\) lift는 한쪽에 exact bad subsequence가 있다.
- declared slice의 모든 anchor-through homogeneous complex straight \(\phi\)-line
  \(\delta=qy\) class가 적어도 한 good-end
  조건을 잃는다.

해석:

- Phase-39 ray는 local Gaussian 방향으로는 쓸 수 있지만 무한 original-cycle completion으로는
  쓸 수 없다.
- 다음 honest branch는 nonlinear/curved good-end contour, piecewise contour,
  nonzero-\(\operatorname{Re}T\) lateral 또는 다른 regulator다.

열린 문제:

- 물리적으로 유도된 original joint cycle, momenta/gauge/BFV body와 orientation line;
- redesigned cycle의 cap, scale-factor, lapse 및 모든 sheet/end census;
- Stokes chamber, saddle/upward-cycle census와 complete signed intersection vector.

따라서 `physical_original_cycle`, complete vector, `global_n_sigma`, physics/TOE claim은 모두
`null`이고 Gate 1은 계속 `OPEN_PARTIAL_PROGRESS`다. 이 결과가 자동 다음 계산을 승인하지 않는다.
