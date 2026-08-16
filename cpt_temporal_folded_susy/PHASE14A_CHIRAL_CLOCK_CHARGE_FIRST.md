# Phase 14A — compact chiral-clock charge-first audit

> 최초 실행: `./ice run phase14a_chiral_clock_charge_first` →
> **24 exact PASS, 7 executable mutants rejected, 6 scope guards, exit 0**.
>
> 두 독립 replay가 같은 commit과 SHA-256에서 같은 count와 판정을 재현했다.
> 전체 selected-template 판정은 **`INCONCLUSIVE_UNCONSTRUCTED`**이다.

- cycle: `cpt-temporal-folded-susy-2026-08-16-phase14a`
- tier: `T2`
- preregistration: `PHASE14A_RESEARCH_CONTRACT.json`, commit
  `86194e16f9ddb585292ff6569bc415163e917c99`
- frozen source packet / pre-run ledger: commit `9dd5333`
- first-run executable: commit `6d6b0f7ada9fd8dfdf6475ca8e90f095d9b9e01c`
- executable SHA-256:
  `1c92f295329d511e661f5d8b9d83b6f767e3c8aee45be86e98f6cc95c133bb2b`
- first-run receipt timestamp / actor: `2026-08-16T06:35:43Z` / Codex
- environment: Node 24.13.0, Python 3.13.5, SymPy 1.14.0, uv 0.12.3
- machine-readable result: `PHASE14A_RUN_RESULT.json`
- scientific verdict: `UNJUDGED` 유지
- programme appraisal: `UNAPPRAISED` 유지
- 식 번호: **E167–E170**

## 0. 결론부터

주 target은
`P14A_SELECTED_GOLDSTINO_RT_TEMPLATE_NONZERO_PHYSICAL_CHARGE`, literal-core target은
`P14A_LITERAL_BRANCH_SUPERPARTNER`다.

이번 계산으로 세 가지를 구분했다.

1. **골드스티노 gauge residual — 닫힘.** $p_T\ne0$인 rolling chiral-clock
   background에서는
   $\delta\upsilon/\delta\epsilon=-(\alpha/2)I_4$가 full rank이고,
   gauge $\upsilon=0$을 보존하는 nonzero local-SUSY parameter가 없다.
2. **Regge–Teitelboim 공간경계 채널 — 이 route에서 없음.** Smooth compact
   $T^3$에는 실제 spatial boundary나 asymptotic end가 없으므로 해당 surface
   integration locus가 없다.
3. **전체 selected template — 아직 판정 불가.** Compact matter-coupled
   4D $N=1$ 모형의 differentiable graded Dirac generator를 실제로 유도하지 않았다.
   따라서 formal constraint quotient를 physical charge census로 승격할 수 없고,
   conditional completeness 및 equivalence-class deduplication도 보류된다.

결국 **두 obvious local-SUSY channel은 음성이지만**, nonzero physical charge의 selected
template 전체는 `INCONCLUSIVE_UNCONSTRUCTED`이다. 관계적 팽창/수축 projector와
cross-branch block을 전혀 만들지 않았으므로 “반대 시간가지=superpartner”도 여전히
`INCONCLUSIVE/OUT_OF_SCOPE`이다.

## 1. 사전등록·소스 분리·최초 실행 순서

결과 관측 전에 다음 순서를 고정했다.

1. 연구 계약 commit `86194e1`
2. 세 source의 version/hash/scope와 pre-run charge ledger commit `9dd5333`
3. 두 차례 read-only static audit
4. 수정된 executable commit `6d6b0f7`
5. 위 committed executable의 최초 실행

세 source는 하나의 parent model로 합성하지 않았다.

- Kallosh–Kofman–Linde–Van Proeyen,
  [hep-th/0006179v3](https://arxiv.org/abs/hep-th/0006179v3): bosonic
  flat-FLRW에서의 goldstino variation, equations (7.15)–(7.16)
- Henneaux–Matulich–Neogi,
  [arXiv:2004.07299v2](https://arxiv.org/abs/2004.07299v2): pure asymptotically-flat
  SUGRA의 constraint-plus-boundary template와 equations (II.33)–(II.35)의 sign
- Martínez-Pérez–Ramírez,
  [arXiv:2510.20072v1](https://arxiv.org/abs/2510.20072v1): matter-free classical
  FLRW ansatz/transformation scope control only

세 번째 source는 chiral matter action, canonical algebra, physical charge, $T^3$, 또는
quantization을 주지 않는다. 두 번째 source의 asymptotic charge formula도 FLRW에 직접
가져오지 않았다. Source file name, version, main-TeX SHA-256은
`PHASE14A_SOURCE_PACKET.json`에 동결되어 있다.

Martínez-Pérez–Ramírez의 equations (62a)–(62b)는
$\delta(N/a)=0$만 주며 $N=a$를 고유하게 정하지 않는다. 또한 아래 specialization은
$W$가 한 점에서 0인 경우가 아니라 함수로서 $W\equiv0$인 경우다.

## 2. E167 — exact bosonic clock skeleton

Flat FLRW에서 lapse를 유지하고


\[
H_N=\frac{\dot a}{Na},\qquad
K_{ij}K^{ij}=3H_N^2,\qquad K^2=9H_N^2
\]

를 쓰면 ADM Einstein kinetic term과 canonical complex scalar term은

\[
L_{\rm EH}=-\frac{3M_P^2V_0a\dot a^2}{N},\qquad
L_Z=\frac{V_0a^3}{2N}(\dot T^2+\dot Y^2),
\]

\[
Z=\frac{T+iY}{\sqrt2},\qquad X=\sqrt6M_P\ln a
\]

이다. 따라서

\[
L_B=\frac{V_0a^3}{2N}
\left(-\dot X^2+\dot T^2+\dot Y^2\right),
\]

\[
p_X=-\frac{V_0a^3}{N}\dot X,\quad
p_T=\frac{V_0a^3}{N}\dot T,\quad
p_Y=\frac{V_0a^3}{N}\dot Y,
\]

\[
H_B=\frac{N}{2V_0a^3}C_B,\qquad
C_B=-p_X^2+p_T^2+p_Y^2.
\tag{E167}
\]

Clock bracket는

\[
\{T,C_B\}=2p_T
\]

이고 executable은 $p_T=+|p_T|$와 $p_T=-|p_T|$를 각각 exact하게 검사했다.
즉 사전등록된 $p_T\ne0$ 양쪽 orientation에서 $T$는 monotonic patch를 이룬다.

## 3. E168 — goldstino residual gate

Frozen model은

\[
K_{\rm phys}=Z\bar Z,\qquad
\mathcal K=K_{\rm phys}/M_P^2,\qquad W\equiv0,
\]

이며 vector/gauging이 없다. 따라서 $m=e^{\mathcal K/2}W$, $D_i m$, $V_F$,
$V_D$, $m_{3/2}$가 모두 0이다. Proper-time derivative
$D_\tau=N^{-1}d/dt$로 Kallosh source의 coefficient를 canonical momentum에 연결하면

\[
\alpha=|D_\tau Z|^2
=\frac{(D_\tau T)^2+(D_\tau Y)^2}{2}
=\frac{p_T^2+p_Y^2}{2V_0^2a^6}>0
\quad(p_T\ne0).
\tag{E168}
\]

Source sign은

\[
-2\,\delta_\epsilon\upsilon=\alpha\epsilon,
\]

따라서 real Majorana parameter space에서

\[
\frac{\delta\upsilon}{\delta\epsilon}
=-\frac{\alpha}{2}I_4,\qquad
\operatorname{rank}=4,\qquad
\det=\frac{\alpha^4}{16},\qquad
\dim\ker=0.
\tag{E169}
\]

이는 **goldstino unitary gauge를 보존하는 nonzero residual parameter가 없다**는
부분결론이다. 다음을 뜻하지 않는다.

- 4D action에 local supersymmetry가 없다.
- 모든 reduced/dressed/nonlocal fermionic charge가 없다.
- 팽창·수축 branch가 교환되지 않는다.

또한 on-shell flat-FLRW Friedmann identity
$\alpha=3M_P^2H^2$는 $H\to-H$에 even이므로 이 식 자체는 branch
exchange map을 공급하지 않는다.

## 4. E170 — compact spatial boundary와 formal quotient

Henneaux source에서 exact sign anchor는

\[
S_\epsilon=i\int_\Sigma d^3x\,\epsilon^T\mathcal S+B_{\rm Susy},
\qquad
\delta B_{\rm Susy}=-i\oint_{S_\infty}d^2S_i\,
\epsilon^T\gamma^{im}\delta\psi_m,
\]

\[
B_{\rm Susy}=-i\epsilon_0^T\oint_{S_\infty}d^2S_i\,
\gamma^{im}\psi_m.
\]

Executable은 마지막 식을 변분해 source sign을 재현하고 wrong-sign mutant를 거부했다.
이것은 FLRW generator의 differentiability derivation이 아니라 **source sign regression**이다.
Separately printed equations (III.8)/(III.13)과의 normalization equivalence도 주장하지 않는다.

$T^3$ fundamental cube의 oriented faces는

\[
(-1,+1,-1,+1,-1,+1)
\]

이고 periodic identification 뒤 세 쌍이 정확히 0으로 상쇄된다. 따라서 frozen topology에서는

\[
\partial\Sigma=\varnothing,
\qquad B_{\rm Susy}^{\rm RT}\;\text{integration locus absent}.
\tag{E170}
\]

Temporal endpoint나 이전 Phase 12 collar는 이 spatial RT surface를 대신하지 않는다.

반면 bulk control은 이미

\[
G_{\rm bulk}=i\sum_A\epsilon^A\mathcal S_A
\]

라고 **가정된** formal expression을 ideal
$(\mathcal S_0,\ldots,\mathcal S_3)$로 quotient하면 0이라는 항등식만 확인한다.
Compact chiral-matter SUGRA에서 해당 $G_{\rm bulk}$가 실제 differentiable graded
first-class generator라는 유도, reality condition, Lorentz constraint, canonical bracket,
reducibility가 없다. 이 formal control의 물리 evidence weight는 0이며 G4는
`NOT_DERIVED`이다.

## 5. Observed charge ledger

Frozen pre-run ledger `PHASE14A_CHARGE_LEDGER.json`은 소급 수정하지 않았다. 관측 결과는 별도
`PHASE14A_RUN_RESULT.json`에 기록했다.

| candidate | observed result | physical status |
|---|---|---|
| proper bulk local-SUSY representative | formal ideal quotient $=0$ | actual graded Dirac bridge `UNCONSTRUCTED` |
| goldstino-gauge residual | kernel dimension $0$ | no surviving parameter in the frozen linearized gauge |
| RT spatial-boundary improvement | actual boundary components $0$ | `NOT_APPLICABLE_IN_THIS_ROUTE` |
| independent reduced/dressed charge | not searched | `OUTSIDE_CANDIDATE_CLASS` |

따라서 observed completeness는 `UNPROVED_STANDARD_DIRAC_DECOMPOSITION`, deduplication은
`DEFERRED_PENDING_CANONICAL_BRIDGE`이다. 세 label을 임의의 영행렬 하나로 미리 합치지 않았다.

## 6. Frozen verdict precedence와 실제 판정

Executable은 다음 순서를 독립 함수로 검사한다.

1. `INVALID`
2. 모든 support gate를 통과한 positive physical witness
3. complete selected-template의 all-zero 결과
4. 그 밖에는 `INCONCLUSIVE_UNCONSTRUCTED`

실제 결과에서는 G0/G1은 pass했고 G2/G3은 음성이지만, graded matter-SUGRA Dirac
decomposition이 `False`이므로 3번의 completeness 조건을 만족하지 않는다. 따라서

\[
\boxed{\texttt{INCONCLUSIVE\_UNCONSTRUCTED}}
\]

이다. 이는 사전등록 contract의 precedence와 일치한다.

## 7. T2 독립 분류

| target claim | fiber / layer | inference | qualification | novelty | registration | fitting risk |
|---|---|---|---|---|---|---|
| selected Phase 14A template에 nonzero physical charge가 있다 | PHYSICS / PHYSICS_MAPPING | `INCONCLUSIVE` | `UNCONSTRUCTED` | REPRODUCTION | PREREGISTERED | NOT_APPLICABLE |
| 반대 relational branch가 superpartner다 | PHYSICS / PHYSICS_MAPPING | `INCONCLUSIVE` | `OUT_OF_SCOPE` | REPRODUCTION | PREREGISTERED | NOT_APPLICABLE |

계약 target과 별개인 observed subgate status는 다음과 같다.

| observed gate | exact status |
|---|---|
| G2 goldstino-gauge residual | `NO_NONZERO_GOLDSTINO_GAUGE_RESIDUAL` |
| G3 compact RT spatial boundary | `NOT_APPLICABLE_IN_THIS_ROUTE` |
| G4 graded matter-SUGRA canonical bridge | `NOT_DERIVED` |
| G5 completeness / deduplication | `DEFERRED_PENDING_CANONICAL_BRIDGE` |

- reproduction: first run과 두 independent replay 모두
  `24 PASS / 7 mutants / 6 guards`, exit 0
- comparison policy: exact SymPy equality/rank/nullspace; floating tolerance 없음
- Bayes: `NOT_ESTIMABLE` — prior와 likelihood를 사전 고정하지 않음
- Lakatos: `NOT_APPLICABLE` — programme checkpoint가 아님
- KG action: `NONE`
- ratification request: `none`

## 8. 재현·공학 receipt

- all four `PHASE14A*.json` files parsed successfully with Python's JSON decoder
- `python3 -m py_compile cpt_temporal_folded_susy/phase14a_chiral_clock_charge_first.py` → PASS
- `./ice doctor` → locked Node/Python/SymPy runtime `READY`
- `./ice info phase14a_chiral_clock_charge_first` → catalog 등록, mapped legacy output 없음
- `./ice list --json` → 45 runnable entries
- `./ice run phase12_boundary_twist_interface` → 38 PASS / 9 mutants / exit 0
- `./ice run phase13a_lorentzian_branch_supercharge` → 21 PASS / 8 mutants / exit 0
- `./ice run phase14a_chiral_clock_charge_first` → 24 PASS / 7 mutants / 6 guards / exit 0
- `npm run check` → typecheck와 12 tests PASS
- `git diff --check` 및 ANSI-control-byte 검사 → PASS

## 9. 다음 gate

Phase 14B relational projector/cross-branch 계산은 열지 않는다. 현재 필요한 것은 별도 사전등록된
**canonical bridge cycle**이다.

최소 deliverable은 같은 compact chiral-clock model에서 다음을 한 번에 만드는 것이다.

1. 4D matter-coupled $N=1$ action에서 reduced canonical variables와 reality conditions 유도
2. lapse/gravitino multipliers를 제거하지 않은 Hamiltonian·Lorentz·SUSY constraints
3. differentiable generator와 actual compact topology의 boundary term
4. graded first-class closure와 proper-gauge quotient
5. 그 뒤에만 observed charge equivalence classes와 completeness 재판정

이 bridge가 실패하면 selected local-SUSY template은 그 새 contract 안에서 비로소 scoped
`CONTRADICTS` 후보가 된다. 통과하더라도 nonzero physical charge가 실제로 살아남아야만 별도
Phase 14B를 열 수 있다. 이번 결과는 기존 scientific verdict, programme appraisal, canon 또는
Contract confidence를 변경하지 않는다.
