# Gate 1 단일 bounded 재개

> **상태:** `CALC_AUTHORIZED` — 실행 전
> **승인:** 2026-08-25 사용자의 명시적 즉시 연구 재개 지시
> **범위:** 번호 없는 direct Gate-1 end-admissibility 계산 한 개
> **비권한:** Phase 51–56 경로 재개, Phase 57, full replay, Gate 1 closure, 물리학 또는 TOE 주장

## 결정

2026-08-30은 과학적 필요조건이 아니라 2026-08-23 회로 차단기의 예정된 운영 재검토일이었다.
사용자가 2026-08-25 즉시 연구 재개를 명시했으므로 그 대기 조건만 아래 **정확한 한 계산**에
한해 면제한다. 일반 core 재개나 자동 다음 계산은 허용하지 않는다.

```text
BOUNDED_PAUSE
  -> GATE1_BOUNDED_RESUME / GATE1_DIRECT_20260825_01

Phase 51--56 reconciliation route = KILL
numbered next phase                = null
automatic descendant              = null
Gate 1                             = OPEN_PARTIAL_PROGRESS
global promotion                   = PROHIBITED
```

## 고정된 실행 객체

| 객체 | 고정값 |
|---|---|
| runner | `cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility.py` |
| runner SHA-256 | `c2cfac73e303d0f46d86c1577fc31cc1cd2ff5e0dfd809e9bdd6b75a38aaaa7e` |
| input | `cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_INPUTS.json` |
| input SHA-256 | `a3bc97461c7989cd5bb471accf46f0c2196de41c3030e9eef2248c4f09a47fdb` |
| result | `cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_RESULT.json` |
| 명령 | `./ice run cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility` |

정확한 basename 또는 relpath만 받으며 unique-prefix, 인자, retry/replay suffix와 이름을 바꾼
후손은 거부한다. runner hash와 clean core tree가 맞아야 실행된다. Python 직접 호출은 허용하지
않는다.

## 계산 질문

Phase 39는 (m=2) finite-window configuration chain과 local cap intersection을 만들었지만,
field window를 무한대로 보낸 straight Gaussian lift가 relative good end인지 계산하지 않았다.
이번 계산은 그 선행 필요조건만 공격한다.

고정 slice는

\[
a_1=a_\partial,\qquad
\phi_1=\phi_\partial+q_s y,\qquad
q_s=e^{si\pi/4},\qquad
T=siN_0,\quad s=\pm1, N_0>0
\]

이고, Phase 39의 두-element scalar에서 같은 식을 직접 축약한다. 적분 convention은
\(e^{-S_2}\)다. 따라서 Witten의 relative-homology convention에서 좋은 무한 끝의 필요조건은

\[
\operatorname{Re}(-S_2)\to-\infty
\quad\Longleftrightarrow\quad
\operatorname{Re}S_2\to+\infty
\]

이다. [Witten, arXiv:1001.2933v4, §3.1.1](https://arxiv.org/abs/1001.2933)은 이
relative-cycle 틀만 제공하며 이 중력 action이나 물리 원본 cycle을 선택하지 않는다.
[Banihashemi–Jacobson, arXiv:2405.10307](https://arxiv.org/abs/2405.10307)은 momenta를 먼저
적분한 configuration representation에서 below-origin lapse contour를 지지하지만 field lift나
그 수렴성을 정하지 않는다.

정확 계산은 Phase-39 ray의 명시적 bad subsequence뿐 아니라 더 넓은 상수 직선
\(q=u+iv\) class를 세 경우로 분할한다.

- (suv<0): exponential이 감쇠하는 끝에서 kinetic real part가 음의 이차식이다.
- (uv=0): kinetic real part가 0이고 적어도 한 끝의 나머지 real part가 0 또는 bounded다.
- (suv>0): 양의 kinetic보다 Starobinsky exponential의 음의 subsequence가 우세할 수 있는지
  정확히 검사한다.

이는 curved/piecewise field contour, nonzero-\(\operatorname{Re}T\) lateral, 다른 regulator나
full joint/BFV cycle을 미리 배제하지 않는다.

## 실행 전 ledger

입력 JSON은 action, 좌표 순서, lapse/field embedding, orientation, (T=0) divisor, endpoint
prescription, regulator, Stokes 비사용 경계, 모든 알려진 relative-end category, short-circuit된
saddle/upward/sheet 역할, source, 판정표와 null 출력을 직렬화한다. 물리 원본 cycle, BFV body,
Stokes chamber와 전체 saddle census가 없다는 사실은 non-null인 것처럼 꾸미지 않는다.

이 계산은 그 누락을 건너뛰어 intersection을 계산하지 않는다. 더 앞선 필요조건인 field-end
admissibility가 실패하면 즉시 후보를 분류하며, 실패하지 않아도 자동으로 dual census를 시작하지
않고 `OPEN`으로 끝낸다.

| 결과 | Phase-39 local 결과 | straight 후보 | 상수직선 model class | Gate 1 |
|---|---|---|---|---|
| exact bad end + 독립 direct-action 일치 | `KEEP` | `KILL` | `KILL` | `OPEN_PARTIAL_PROGRESS`, programme `NARROW` |
| bad end 미확정, 실행 유효 | `KEEP` | `OPEN` | `OPEN` | `OPEN_PARTIAL_PROGRESS` |
| 단순 재매개화만 확인 | `KEEP` | `EQUIVALENCE` | `EQUIVALENCE` | `OPEN_PARTIAL_PROGRESS` |
| manifest/식/독립 검산 mismatch | `KEEP` | 결과 사용 금지 | 결과 사용 금지 | `OPEN_PARTIAL_PROGRESS`, run invalid |

모든 경우 `physical_original_cycle`, complete vector, `global_n_sigma`, physics/TOE claim은
`null`이고 global promotion은 `PROHIBITED`다.

## 자원 및 재귀 상한

| 항목 | 상한 |
|---|---:|
| wall clock | 30초 |
| result artifact | 250,000 bytes |
| stdout / stderr | 각 65,536 bytes |
| root / ODE / evaluator reconciliation | 각 0회 |
| bad-subsequence samples | arm당 6개 |
| automatic descendants | 0개 |

제어면은 Effect scoped process와 timeout으로 wall-clock을 강제하고, stdout/stderr 및 결과 크기를
검사한다. 계산 자체는 exact SymPy 경로와 별도로 구성한 80-decimal direct two-element action
경로를 같은 bounded 실행 안에서 비교한다. 이는 동일 공식을 다른 정밀도로 재호출하는 것이 아니라
축약식과 원래 scalar evaluation을 독립적으로 대조하는 mutation control이다.

실행 뒤에는 성공·실패와 무관하게 이 exact window를 소비 상태로 바꾸고 자동 retry를 만들지
않는다. 다음 연구 질문은 이 결과를 먼저 해석한 뒤 별도 bounded 승인으로만 연다.
