# Phase 15R — single-source parent-sign repair

> 최초 실행: `uv run --with sympy python3
> cpt_temporal_folded_susy/phase15r_parent_sign_reproduction.py` →
> **47 exact PASS, 17 mutant categories / 18 fixtures rejected,
> 4 scope guards, 24/24 known-prior matches, exit 0**.
>
> 독립 read-only replay가 모든 수식·관성지수·후보 상태·target 판정을 재현했다.
> 유일한 차이는 실행 시점에 따라 달라지는 `provenance.head_commit`이다.

- cycle: `cpt-temporal-folded-susy-2026-08-16-phase15r`
- tier / novelty: `T2 / REPRODUCTION`
- contract commit: `34dd2d3fc533d94113f5ea98d3eafc3721565be4`
- source/convention packet commit: `72819da9d9c078b1f7c0d4942d8f069e9c75d656`
- executable commit: `433b4920155d63afd07f74a5800f88c25216d94d`
- executable SHA-256:
  `af3e3d021e995833a634b1fb7afda7d1cd4faace60113bb425d467301424f40d`
- first-run result: `PHASE15R_RUN_RESULT.json`
- replay receipt: `PHASE15R_REPLAY_RECEIPT.json`
- equations: **E171–E176**

## 0. 결론부터

Phase 14A에서 쓰던 보손 clock skeleton과 실제 off-shell local-SUGRA formula family가
**같은 단일 4D source parent에서 동시에 나오는가**를 먼저 점검했다. 결과는 두 target으로
갈렸다.

1. `P15R_BOSONIC_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS`
   → **`VALID / SUPPORTS / NONE`**. Frozen Hohl/Kallosh 두-source census에서
   Kallosh 계열은 ADM-compatible Lorentzian kinetic inertia ((1,0,2))를 재현한다.
2. `P15R_FULL_OFFSHELL_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS`
   → **`VALID / CONTRADICTS /
   NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS`**. 같은 Kallosh source에는 다음 tangency
   계산에 필요한 target old-minimal auxiliary-retaining action과 완전한 변환계가 없고,
   그 formula family를 가진 Hohl source는 frozen parent map에서 보손 부호를 통과하지 못한다.

따라서 현재 허용되는 결론은 다음뿐이다.

\[
\boxed{\text{bosonic parent exists in the frozen census}}
\]

\[
\boxed{\text{no full same-source off-shell parent exists in that census}}
\]

이것은 **Temporal-Folded SUSY, 시간가지 교환, 또는 pre-Big-Bang=superpartner의 증명이나
반증이 아니다**. Phase 15A의 tangency/projector 계산도 재개하지 않았다.

## 1. 왜 repair cycle이 필요했나

Phase 15A는 완성 executable commit 전에 Hohl curvature-sign 결과가 관측되어 sequencing이
깨졌다. 그 cycle은 `INVALID / INCONCLUSIVE / PREREG_OR_PROVENANCE_INVALID`로 보존하고,
관측된 부호를 known prior로 공개한 fresh Phase 15R reproduction cycle을 열었다.

Phase 15R 순서는 다음과 같다.

1. contract 단독 commit
2. 두 primary source의 version/hash/line scope, typo packet, source-tag graph와 coverage matrix commit
3. complete sign-only executable 단독 commit
4. 그 commit에서 최초 실행
5. result commit
6. 변경 없는 executable의 독립 replay와 별도 receipt

Executable을 commit하기 전에는 import, compile, 또는 실행하지 않았다. 세 독립 정적 감사가
동일 SHA-256에 대해 blocker 없음으로 판정한 뒤 최초 실행했다.

## 2. Source census와 non-stacking rule

Frozen primary census는 정확히 두 source다.

- Hohl, [arXiv:2005.09504v1](https://arxiv.org/abs/2005.09504v1),
  `sugra_lagrangian.tex`, SHA-256
  `12722fb7ed5e7c52c2011a632cd5c57e218a843888ce9e15ada6c64a4d52fec6`
- Kallosh–Kofman–Linde–Van Proeyen,
  [hep-th/0006179v3](https://arxiv.org/abs/hep-th/0006179v3),
  `Gravitino.tex`, SHA-256
  `81c4ab799f2cd943bb53fec6f8607267a46090b222a9fc659144902862431af7`

ADM Einstein-plus-canonical-scalar calculation은 zero-evidence internal control이고 primary
candidate 수에 넣지 않았다. 세 branch는 서로 다른 symbols와 source tags로 계산했다.
Hohl action/transformation과 Kallosh curvature를 결합하는 식의 source stacking은
`INVALID_SOURCE_STACKING`이다.

이 census는 4D \(N=1\) SUGRA 문헌 전체가 아니다. 따라서 full target의 `CONTRADICTS`는
**이 두 source에 한정**되며 universal no-go가 아니다.

## 3. E171 — source-native curvature

Arbitrary lapse를 유지하고

\[
ds^2=-N^2dt^2+a^2d\mathbf x^2,
\]

\[
Q=\frac{\ddot a}{aN^2}
 +\frac{\dot a^2}{a^2N^2}
 -\frac{\dot a\dot N}{aN^3}
\tag{E171}
\]

를 정의한다. Hohl branch는 source의 coframe spin connection과 lower-first curvature product를
직접 전사해

\[
R_H=+6Q
\]

를 얻었다. Kallosh branch는 그 source의 coordinate-curvature order를 독립적으로 전사해

\[
R_K=-6Q
\]

를 얻었다. Kallosh 결과는 conformal-time relation과 printed de Sitter anchor
\(R_K=-12H^2\)를 동시에 통과했다. ADM internal control은 별도 Christoffel graph에서
\(R_{\rm ADM}=+6Q\)를 재현했다.

`N=1` 조기 대입, \(\dot N\) 삭제, curvature order 교환, Hohl connection storage transpose는
모두 exact mutant로 거부됐다.

## 4. E172 — raw action과 유일한 endpoint removal

Frozen endpoint는

\[
B=\frac{3M_P^2V_0a^2\dot a}{N}.
\]

각 source 자체의 Einstein coefficient를 사용하면

\[
L_{H,\rm raw}=-\dot B
 +\frac{3M_P^2V_0a\dot a^2}{N},
\]

\[
L_{K,\rm raw}=+\dot B
 -\frac{3M_P^2V_0a\dot a^2}{N}.
\tag{E172}
\]

따라서 Hohl은 \(+\dot B\), Kallosh와 ADM은 \(-\dot B\)를 정확히 한 번 적용해야
first-order bulk representative가 된다. Raw second-order Lagrangian에 ordinary velocity
Hessian을 부여하지 않았다. Endpoint omission과 double application도 모두 거부됐다.

Matter는 각 source의 자체 action coefficient와 field normalization으로

\[
Z=\frac{T+iY}{\sqrt2},\qquad
\dot Z\dot{\bar Z}=\frac{\dot T^2+\dot Y^2}{2}
\]

를 독립적으로 재현했다. Source 간 scalar normalization도 섞지 않았다.

## 5. E173 — first-order Hessian과 inertia

\[
X=\sqrt6M_P\ln a
\]

를 적용한 결과는

\[
L_{H,\rm first}
=\frac{V_0a^3}{2N}
\left(+\dot X^2+\dot T^2+\dot Y^2\right),
\]

\[
L_{K,\rm first}
=\frac{V_0a^3}{2N}
\left(-\dot X^2+\dot T^2+\dot Y^2\right).
\tag{E173}
\]

따라서 \((X,T,Y)\) velocity Hessian의 inertia
\((n_-,n_0,n_+)\)는

| branch | rank | determinant sign | inertia | target |
|---|---:|---:|---:|---|
| Hohl | 3 | positive | \((0,0,3)\) | fail |
| Kallosh | 3 | negative | \((1,0,2)\) | pass |
| ADM internal | 3 | negative | \((1,0,2)\) | pass, evidence weight 0 |

이다. Real nonsingular derivative-free point map, positive lapse, positive densitization은
Sylvester inertia를 바꾸지 않는다. Hohl의 all-positive block을 허용된 equivalence로
\((-1,+1,+1)\)로 만들 수 없다. Einstein sign flip, imaginary \(X\), negative densitizer는
repair가 아니라 frozen invalid mutant다.

## 6. E174 — 허용 equivalence 아래 inertia 불변

Registered velocity-dependent endpoint \(B\)를 정확히 한 번 제거한 뒤, 추가로 허용되는
\(dF(q,t)/dt\)는 velocity Hessian을 바꾸지 않는다. Frozen real equivalence class에서

\[
\nabla^2_{\dot q}\!\left(\frac{dF(q,t)}{dt}\right)=0,
\qquad
G\mapsto G'=d\,J^TGJ,
\quad J\in GL(3,\mathbb R),\quad d>0,
\]

\[
\operatorname{Inertia}(G')=\operatorname{Inertia}(G).
\tag{E174}
\]

따라서 Hohl의 all-positive block은 이 class 안에서 basis artifact가 아니다. 이 식은
cosmological observable이나 branch map을 구성하지 않는다.

## 7. E175 — coverage와 후보 분리

Bosonic sign test와 full-offshell source coverage를 같은 후보별로 결합하면

| source | bosonic test | frozen formula coverage | candidate status |
|---|---|---|---|
| Hohl | fail, inertia \((0,0,3)\) | available, disclosed glyph caveats | `REJECT_SIGN` |
| Kallosh | pass, inertia \((1,0,2)\) | target old-minimal family incomplete | `BOSONIC_PARENT_ONLY` |

이다. 따라서

\[
\begin{aligned}
\text{bosonic selection}&=\texttt{SINGLE\_ELIGIBLE},\\
\text{full-offshell selection}&=\texttt{NONE\_ELIGIBLE}.
\end{aligned}
\tag{E175}
\]

Kallosh source에는 superconformal auxiliary-retaining 표현이 있지만, 이를 target
\(M,\bar M,b_a,F,\bar F\) old-minimal family와 동일시하지 않았다. 반대로 Hohl의 formula
family coverage가 있다는 이유로 보손 inertia failure를 무시하지 않았다.

## 8. E176 — 두 target의 독립 판정

Candidate selection을 target existence 판정과 혼동하지 않으면

\[
\begin{aligned}
P_{\rm bosonic}
 &= (\texttt{VALID},\texttt{SUPPORTS},\texttt{NONE}),\\
P_{\rm full\ offshell}
 &= (\texttt{VALID},\texttt{CONTRADICTS},
 \texttt{NO\_VALID\_SINGLE\_PARENT\_IN\_FROZEN\_CENSUS}).
\end{aligned}
\tag{E176}
\]

Novelty는 `REPRODUCTION`, registration은 `PREREGISTERED`다. Fitting/null/multiplicity와
Lakatos는 `NOT_APPLICABLE`, numerical Bayes는 `NOT_ESTIMABLE`, KG action과 ratification
request는 없다.

## 9. 독립 replay

최초 실행은 executable commit `433b492`에서 수행했고, result commit `3a9fec4` 뒤
독립 agent가 같은 command를 한 번 재실행했다.

- replay exit: 0
- replay executable SHA-256: 최초 실행과 동일
- worktree: 전후 clean
- exact counts: 47 PASS, 17 mutant categories / 18 fixtures, 4 scope guards,
  24 scientific observations와 24/24 known-prior matches
- 수식, Hessian, inertia, candidate, census, selection, target: 모두 동일

정규화한 machine payload hash와 science-terminal subset hash도 각각 일치했다. Replay의
`head_commit`만 result commit을 가리키며, `executable_add_commit`과 모든 immutable hash는
최초 실행과 같다.

## 10. 프로그램에 주는 의미와 다음 관문

이 cycle은 중요한 오류 하나를 막았다. **보손 부호를 주는 source와 off-shell 변환계를 주는
source를 조립해 하나의 parent라고 부를 수 없다.** 그렇게 하면 원하는 답은 만들 수 있지만
단일 4D action에서 유도했다는 주장은 사라진다.

따라서 Phase 15 tangency는 닫힌 상태를 유지한다. 다음 단계는 둘 중 하나다.

1. auxiliary-retaining action, 필요한 local transformations, Lorentzian curvature/action sign을
   같은 source 안에서 모두 공급하는 새 primary parent candidate를 별도 사전등록한다.
   Kugo–Yokokura–Yoshioka 계열은 **검토 후보**일 뿐이며, source-internal
   Euclidean/Lorentzian bridge가 닫히기 전에는 parent가 아니다.
2. 그런 candidate가 없으면 full single-parent route를 중단한다. Hohl transformation-only
   계산이나 Kallosh action+Hohl transformation stacking은 core thesis의 증거로 쓰지 않는다.

새 candidate cycle이 통과하더라도 그것은 겨우 4D parent를 확보하는 단계다. 그 뒤에야
Bianchi-I homogeneous SUSY tangency, full Dirac/BFV closure, relational branch projector,
nonzero \(Q_{\rm phys}\), cross-branch observable을 순서대로 요구할 수 있다.

현재 literal Temporal-Folded SUSY core는 계속

\[
\boxed{\texttt{INCONCLUSIVE / UNCONSTRUCTED}}
\]

이며, 자연의 증거 또는 고유 관측 예측은 아직 0이다.
