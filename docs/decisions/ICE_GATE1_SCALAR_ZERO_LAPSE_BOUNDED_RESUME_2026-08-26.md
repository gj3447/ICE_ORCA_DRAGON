# Gate 1 scalar zero-lapse extension 단일 bounded 재개

> **상태:** `CONSUMED_INVALID_RUN_NO_RESULT`
> **승인:** `GATE1_ZERO_LAPSE_20260826_01`
> **범위:** 번호 없는 fixed-\(a\), \(m=2\) full \(q\)-paired scalar boundary 계산 한 번
> **Gate 1:** 실행 결과와 무관하게 `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 결정

사용자의 2026-08-26 지시는 직전 source-link 결과가 명시한 다음 장애물, 즉 같은 declared
scalar control의 \(N=0\) 분포 extension을 한 번 검사할 권한으로 해석한다. 이 권한은
Phase 51→56의 killed saved-backend/reconstructed-launch 경로, Phase 57, full replay, 재시도,
`repro`, 이름을 바꾼 후손 또는 TOE 승격을 열지 않는다.

이 window는 authorization commit
`1f0fc7d17cc704577db601071e46563a37db24f0` 뒤 실제 runner invocation 한 번으로 소진됐다.
실행은 `2026-08-26T05:42:12Z`에 시작해 Bash 기준 `2.349 s` 뒤 exit `1`로 끝났고,
exclusive receipt는 `2026-08-26T05:42:14.025056895Z`에 생성됐다. result 파일은 쓰이지
않았다. 따라서 이 문서 아래의 계산 대상과 판정표는 동결된 **사전 계획**이며, 어느 과학 판정
행도 이번 실행 결과로 선택되지 않았다.

실패 check는 `G1.zero.global_lower_offset`이다. 바로 앞 square rewrite check는 통과했지만,
두 번째 check가 `simplify(lhs) == unsimplified_rhs` 형태의 SymPy structural equality를 사용해
수학적으로 같은 서로 다른 expression tree를 `False`로 판정했다. 독립 read-only 감사는
zero-difference predicate가 올바른 검사라고 확인했다. 그러므로 이 실패는
`HARNESS_STRUCTURAL_EQUALITY_FALSE_NEGATIVE_NOT_SCIENTIFIC_COUNTEREVIDENCE`이며 아래 square
identity나 tail bound의 반증이 아니다. 동시에 유효 result가 없으므로 canonical boundary,
scaling degree 또는 extension verdict의 증거도 아니다.

기존 source-link one-shot은 비영 lapse arm의 reduced scalar link와 orientation \(+1\)만
`KEEP`하고, tests crossing \(N=0\)의 full \(q\)-paired distribution을 `OPEN`으로 남겼다.
이번 계산은 그 한 점만 직접 겨냥한다. Phase 29의 endpoint vector
\(\Delta q=(\Delta a,\Delta\phi)\) kernel, Phase 30의 full signature-\((-,+)\) determinant
line, Phase 32의 projected crossing sign은 서로 다른 대상이며 합치거나 재계산하지 않는다.

## 동결 실행체

| 항목 | 값 |
| --- | --- |
| authorization | `GATE1_ZERO_LAPSE_20260826_01` |
| numbered phase | `null` |
| runner | `cpt_temporal_folded_susy/gate1_scalar_zero_lapse_extension.py` |
| runner SHA-256 | `f7a7135f5d17ce283ef3dfe444b052499f85b9b3b6956be93a81d34ed106c58e` |
| input | `cpt_temporal_folded_susy/GATE1_SCALAR_ZERO_LAPSE_EXTENSION_INPUTS.json` |
| input SHA-256 | `5667cb42bbc7eb72ae50de05cc1b0abfbc12bf22c8036f6c59c6f5427644cd0e` |
| upstream result SHA-256 | `ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243` |
| result | `cpt_temporal_folded_susy/GATE1_SCALAR_ZERO_LAPSE_EXTENSION_RESULT.json` |
| command | `./ice run cpt_temporal_folded_susy/gate1_scalar_zero_lapse_extension` |
| args | none |
| maximum launches | 1 |
| automatic next | `null` |

`ice run`은 clean `cpt_temporal_folded_susy/` tree, runner/input SHA-256, exact name, no args와
기존 upstream result hash를 검사한다. 실행 전에 `.git/ice-launches/GATE1_ZERO_LAPSE_20260826_01`
exclusive receipt를 원자적으로 만들므로 성공, 실패, timeout 모두 창을 소진한다. 미리 존재하는
result는 stale artifact로 거부한다. 직접 Python 실행은 승인 표면이 아니다.

## 계산 대상

기존에 동결된

\[
T=\epsilon+iN,\qquad
c=\frac{4\pi^2a^3}{\hbar},
\]

\[
u(q)=\frac{2\pi^2}{\hbar}
\left[-3a+a^3V(\phi+q/2)\right],\qquad
V(\varphi)=\frac34(1-e^{-\kappa\varphi})^2
\]

를 사용해 full real-\(q\) amplitude

\[
\mathcal A(T)=\frac{2\pi a^3}{\hbar T}
\int_{\mathbb R}dq\,
\exp\!\left[-\frac{cq^2}{T}-Tu(q)\right]
\]

의 canonical boundary가 \(C_c^\infty((-R,R))\), \(R=6/5\)에서 존재하는지 검사한다.
핵심은 local Gaussian을 반복하는 것이 아니라 full negative-\(q\) Starobinsky tail을 포함한
전역 bound다.

정확한 square identity는

\[
u(q)=-\frac{6\pi^2a}{\hbar}
+\frac{3\pi^2a^3}{2\hbar}
\left(1-e^{-\kappa\phi}e^{-\kappa q/2}\right)^2
\]

이며, 이것이 다음 bound를 주는지 검사한다.

\[
|\mathcal A(\epsilon+iN)|
\le
\sqrt{\frac{\pi a^3}{\hbar}}
e^{6\pi^2a\epsilon/\hbar}\epsilon^{-1/2}.
\]

그 뒤 \(F_r(w)=\sqrt r\,\mathcal A(rw)\)의 right-half-plane normal-family limit과 canonical
boundary continuity를 분리된 analytic theorem guard로 적용한다. 예상 leading boundary는

\[
\sqrt{\frac{\pi a^3}{\hbar}}
\begin{cases}
e^{-i\pi/4}N^{-1/2},&N>0,\\
e^{+i\pi/4}|N|^{-1/2},&N<0.
\end{cases}
\]

## 정리와 한정

- Chakrabarti–Shafikov, [arXiv:1505.01230](https://arxiv.org/abs/1505.01230), Proposition 2.2,
  Theorem 1.1, Theorem 2.4와 Proposition 2.7의 polynomial-growth topology, distributional boundary
  current, canonical ambient extension과 continuous boundary map을 finite-\(R\) smooth boundary
  segment에 국소화해 사용한다. 구체적으로 scaled family의 localized \(A^{-1}\) uniform bound와
  compact \(A^{-1}\to A^{-2}\) inclusion으로 compact-open convergence를 \(A^{-2}\) convergence로
  올린 뒤 boundary map을 적용한다.
- Brunetti–Fredenhagen, [arXiv:math-ph/9903028](https://arxiv.org/abs/math-ph/9903028),
  Theorem 5.2의 scaling-degree-preserving extension 정리를 1차원 lapse에 사용한다.

`unique`는 반드시 **scaling degree \(1/2\)를 보존하는 extension 가운데 유일**하다는 뜻이다.
\(\delta^{(k)}\)는 scaling degree \(1+k\)이므로 같은 degree에서 허용되지 않는다. 임의의 더 높은
degree 분포를 인위적으로 더하는 행위 자체가 논리적으로 불가능하다고 주장하지 않는다.

또한 momentum prefactor만의
\(\delta+\operatorname{PV}\) boundary를 full amplitude에 항별로 곱하지 않는다. \(q\) integral은
\(T=0\)에서 smooth multiplier가 아니므로 finite \(\epsilon\)의 전체 곱을 먼저 pairing한다.

## 사전 판정표

| 조건 | verdict | 영향 |
| --- | --- | --- |
| 전역 tail bound, canonical boundary, nonzero scaling limit, degree-preserving uniqueness 모두 성립 | `UNIQUE_SCALING_DEGREE_PRESERVING_EXTENSION` | `NARROW` |
| canonical boundary가 고정 point support 또는 degree \(\ge1\)을 가짐 | `CANONICAL_EXTENSION_WITH_POINT_SUPPORT` | `BRANCH` |
| side/test-space/limit-order 의존 | `SIDE_OR_LIMIT_ORDER_DEPENDENT_BRANCH` | `BRANCH` |
| distributional extension 부재 | `NO_DISTRIBUTIONAL_EXTENSION` | 이 declared scalar zero-lapse completion만 `KILL` |
| 결정 불가 | `INCONCLUSIVE` | `OPEN` |

어느 행도 physical original cycle, full joint orientation, complete signed vector, `global_n_sigma`,
physics claim 또는 TOE claim을 만들지 않는다. 그 필드는 모두 `null`, global promotion은
`PROHIBITED`, Gate 1은 `OPEN_PARTIAL_PROGRESS`, `automatic_next=null`이다.

실제 실행은 판정표에 도달하기 전에 harness check에서 중단됐다. authoritative 상태는
`INVALID_RUN`, scientific verdict와 decision-table row는 `null`, zero-lapse distribution은 직전
source-link 결과의 `OPEN`을 그대로 상속한다.

## 자원과 금지면

```text
wall clock                 <= 30 s
result artifact            <= 250,000 bytes
stdout / stderr            <= 65,536 / 65,536 bytes
root / ODE                 = 0 / 0
evaluator reconciliation   = 0
numerical samples          = 0
automatic descendants      = 0
```

제외 범위는 varying \(a,p_a\), conformal/gravitational block, BFV/ghost/Pfaffian, determinant-line
orientation, \(R\to\infty\), \(m\to\infty\), continuum/cutoff theorem, \(\lambda=1\) selection,
physical measure, original joint cycle, global intersection과 모든 physics/TOE 승격이다.

실제 stdout은 비어 있었고 exit `1`, wall time `2.349 s`, exact PASS 1개 뒤 exact FAIL 1개,
theorem guard와 numerical check는 각각 0개였다. result가 없으므로 result bytes/hash/self-digest는
모두 `null`이다. receipt가 window를 소비했으며 retry, `repro`, 수정 runner 실행과 automatic
descendant는 새 명시적 승인 없이는 금지한다. Gate 1과 모든 global/physics/TOE null 경계는
변하지 않는다.
