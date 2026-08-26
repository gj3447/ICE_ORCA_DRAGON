# Gate 1 scalar source-link 단일 bounded 재개

> **상태:** `CONSUMED` — 2026-08-26 `VALID_RUN`, 결과 검토 단계
> **승인:** 2026-08-26 사용자의 명시적 “다음 연구 진행” 지시
> **권한 ID:** `GATE1_SOURCE_LINK_20260826_01`
> **범위:** 번호 없는 fixed-\(a\), \(m=2\) scalar phase-space/source-link exact 계산 한 번
> **비권한:** Phase 51–56 route 재개, Phase 57, full replay/repro, physical original cycle 복원,
> full joint/BFV orientation, Gate 1 closure, 물리학 또는 TOE 주장

## 결정

2026-08-30은 자동 재개일이 아니라 운영 재검토 자격일이다. 사용자의 2026-08-26 지시는 그
대기만 아래 정확한 계산 한 개에 한해 면제한다. 2026-08-25의 straight-lift window와 receipt은
덮어쓰지 않고 `CONSUMED`로 보존한다.

```text
Phase 51--56 reconciliation route = KILL
numbered phase                    = null
Phase 57 / full replay            = false
automatic descendant              = null
Gate 1                             = OPEN_PARTIAL_PROGRESS
global promotion                   = PROHIBITED
```

## 고정 실행 객체

| 객체 | 고정값 |
|---|---|
| runner | `cpt_temporal_folded_susy/gate1_scalar_source_link.py` |
| runner SHA-256 | `896f73384368f2fb20779ca780acd7676abc794d45796a3577a965f169947fbe` |
| input | `cpt_temporal_folded_susy/GATE1_SCALAR_SOURCE_LINK_INPUTS.json` |
| input SHA-256 | `182ab0d04b2869cf01be39e0f73c02919ca4c9c17867f267e3daea915247ebd1` |
| result | `cpt_temporal_folded_susy/GATE1_SCALAR_SOURCE_LINK_RESULT.json` |
| command | `./ice run cpt_temporal_folded_susy/gate1_scalar_source_link` |
| private launch receipt | `.git/ice-launches/GATE1_SOURCE_LINK_20260826_01` |

정확한 basename 또는 relpath와 빈 인자만 받는다. 제어면은 spawn 전에 runner와 input SHA-256,
clean core, stale result 부재를 검사하고 exclusive receipt directory를 원자적으로 만든다. 한 번
receipt를 획득하면 정상 종료, 오류, timeout, stdout/stderr 또는 artifact cap 실패와 무관하게
retry·동시 실행·renamed descendant를 허용하지 않는다. `repro` 및 Python 직접 우회는 비권한이다.

## 질문과 새 control의 지위

질문은 선언된 ordered real scalar phase-space control이 momentum-first 적분 뒤 같은 scalar
orientation으로 \(0<\lambda\le1\) affine family의 **비영 lapse arm** boundary에 연결되는지다.
저장소에는 fixed real \(q\) endpoint, \(T=iN\), below-origin side와 여러 local Gaussian lift는
기록돼 있지만 literal physical-original \((q,p)\) cycle의 전체 measure/orientation은 없다. 따라서
입력의

\[
dp_0\wedge dp_1\wedge dq/(2\pi\hbar)^2,
\qquad p_0,p_1,q\in\mathbb R
\]

은 `NEW_BOUNDED_SCALAR_CONTROL`이지 복원된 물리 원본이 아니다. varying-\(a\), BFV/ghost,
full determinant line과 absolute lapse measure는 제외한다.

\(\mu=2\pi^2a^3\), \(z=N-i\epsilon\), \(T=iz\)로 두면 고정된 exact object는

\[
I_2=q(p_0-p_1)-\frac{z}{4\mu}(p_0^2+p_1^2)-zU(q),
\qquad
S_2=\frac{2\mu q^2}{T}+TU(q).
\]

운동량을 선언된 순서로 먼저 적분해

\[
p_0^\star=\frac{2\mu q}{z},\quad p_1^\star=-\frac{2\mu q}{z},\quad
J_p=\frac{\mu}{\pi i\hbar z}=\frac{2\pi a^3}{\hbar T}
\]

및 \(e^{iI_2/\hbar}=e^{-S_2/\hbar}\)를 검사한다. \(N>0\)과 \(N<0\)에서 두 momentum slice의
Fresnel phase product는 각각 \(-i\), \(+i\)이며 별도 BFV/Maslov sign을 끼워 넣지 않는다.

## contour와 limit order

유한 \(R=6/5\)에서 \(N=x-i\epsilon\), \(\epsilon>0\)를 먼저 유지한다. affine family는

\[
T=\rho e^{i\psi},\qquad
\Gamma_\lambda:q=u+i\lambda\psi/\kappa,qquad 0<\lambda\le1
\]

이고 homotopy \(q_s=u+is\lambda\psi/\kappa\)의 full-rate Starobinsky phase defect는
\((1-s\lambda)\psi\)다. full action 전체로 finite rectangle connector를 제거한 뒤에만
\(\epsilon\downarrow0\)을 \(C_c^\infty((-R,0)\cup(0,R))\) tests와 pair한다. 그 다음 비영 arm에서
\(\lambda\downarrow0\)을 본다. \(N=0\)을 포함한 full \(q\)-paired amplitude, \(R\to\infty\),
\(m\to\infty\), varying-\(a\), BFV limit은 취하지 않는다.

\(J_p\) 자체는 below-origin boundary distribution
\((2\pi a^3/\hbar)[\pi\delta(N)-i\,\mathrm{PV}(1/N)]\)을 갖지만, 이것만으로 full \(q\)-paired
zero-lapse distribution을 정하지 않는다. 또한 potential을 버린 pure-\(q\) Gaussian은 shifted arm의
한 끝에서 성장하므로 source-link 증명으로 사용하지 않는다.

## 사전 판정표와 상한

| 관측 | 판정 | programme 영향 |
|---|---|---|
| full regulated identity와 scalar orientation이 지정 범위 전체에서 일치 | declared scalar link `KEEP` | `NARROW` |
| 비영 arm은 일치하지만 zero-including full distribution은 미확립 | `NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN` | `NARROW` |
| 사전 지정 side/order/regulator 사이 실제 비동치 | `SIDE_OR_ORDER_DEPENDENT_BRANCH` | `BRANCH` |
| exact momentum/contour identity 불일치 | 이 declared link만 `KILL` | `KILL` |
| 필요한 limit을 범위 안에서 결정하지 못함 | `INCONCLUSIVE` | `OPEN` |
| schema/hash/cap/identity 실패 | `INVALID_RUN`, 과학 출력 사용 금지 | fail closed |

wall clock은 30초, result는 250,000 bytes, stdout/stderr는 각각 65,536 bytes다. root, ODE,
evaluator reconciliation, numerical sampling, subprocess descendant는 모두 0회다. 모든 결과에서
`physical_original_cycle`, `full_joint_orientation`, complete signed vector, `global_n_sigma`,
physics/TOE claim은 `null`, Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은 `PROHIBITED`,
`automatic_next=null`이다.

## 실행 후 receipt

Authorization commit `392076099bd0282d0954b377792a18960c0a43f3` 뒤 frozen command를 정확히
한 번 실행했다. 2.791651251초에 exit `0`이었고 exclusive private receipt가 window를 소진했다.

```text
run_status                                      = VALID_RUN
classification                                  = GATE1_NONZERO_LAPSE_SCALAR_SOURCE_LINK_MATCHES_ZERO_LAPSE_DISTRIBUTION_OPEN
verdict                                          = NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN
exact checks                                     = 16/16 PASS
analytic theorem guards                          = 3/3 separately reviewed
numerical checks                                 = 0
reduced_affine_class_nonzero_arm_source_link     = KEEP
scalar orientation ratio                         = +1
zero-lapse full q-paired distribution             = OPEN
phase-locked representative selected              = false
programme impact                                 = NARROW
Gate 1                                           = OPEN_PARTIAL_PROGRESS
global promotion                                 = PROHIBITED
automatic_next                                   = null
```

결과는 11,117 bytes, SHA-256
`ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243`이며 self-field 제외
payload SHA-256은
`a3e9f17e7a5d0838cd295427bd161aabb2260b9d15f32b3364b1794ad997d04b`다. 독립 읽기 전용 감사가
digest, 16개 executable exact result entry, 세 theorem guard, momentum prefactor와 arm phase 및 end coefficient를
재검산했으며 결론 변경은 없었다. theorem guard는 numerical check나 별도 runner 재실행이 아니라
exact coefficient에 표준 Gaussian/Cauchy/dominated-boundary 정리를 적용한 analytic guard다.

해석 정본은
[`GATE1_SCALAR_SOURCE_LINK.md`](../../cpt_temporal_folded_susy/GATE1_SCALAR_SOURCE_LINK.md)다. 이
receipt은 비영 lapse-arm reduced scalar link만 `KEEP`한다. zero-including full \(q\)-paired
distribution, \(\lambda=1\) source selection, physical original/full joint/BFV cycle, global coefficient와
physics/TOE claim은 여전히 `OPEN` 또는 `null`이다. retry, replay, renamed descendant와 automatic
continuation은 금지된다.
