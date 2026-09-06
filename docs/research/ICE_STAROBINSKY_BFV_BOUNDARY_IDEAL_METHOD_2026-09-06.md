# Starobinsky source의 scale-factor 경계: 무엇을 보완해야 하는가

2026-09-06 · **SUPPORTING_METHOD** · 정확한 수식에 대한 방법 메모.

양수 scale factor만 적분한다는 선언에는 경계에서 게이지 변환을 어떻게 처리할지가 빠져
있다. 이 메모는 그 빈칸을 한 식으로 확인하고, 경계의 대수적 조건 하나를 제시한다.
결론은 **선언한 고전 Abelian BFV differential 아래에서 bare hard-cutoff face의 ideal은
불변이 아니며, minimal ghost를 함께 제한하면 그 ideal의 불변성만 복구할 수 있다**는
것이다. 전체 적분 경로의 구성이나 새 물리 발견으로 해석하지 않는다.

직관적으로는 적분 영역에 울타리를 놓은 뒤, 같은 물리 상태를 나타내는 게이지 변환이
그 울타리를 넘는지 확인하는 문제다. 울타리에서 변환을 제한하는 방법은 가능하지만,
그 제한이 원래 이론의 경계 조건과 맞는지까지 자동으로 결정되지는 않는다.

## 1. 기존 연구의 정확한 출발점

현재 G1 open은 `open:gate1-original-cycle-signed-global-intersections`다.
필요한 전체 객체는 같은 action·polarization·gauge·orientation을 갖춘 regulated joint
relative cycle이다. 이미 있는 조각들은 다음과 같다.

| 기존 자료 | 확보된 범위 | 이 메모로 넘어올 때 남는 차이 |
|---|---|---|
| [Phase 24](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md), [continuum certificate](ICE_STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_2026-09-06.md) | Euclidean action과 한 국소 constrained real root | 전체 field-history 적분 영역은 제공하지 않음 |
| [Phase 28 §7](../../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md) | 같은 모델의 Euclidean-continued reduced BFV 대수, Dirichlet ghost, 남는 lapse modulus | undeformed Lorentzian source나 전체 측도는 아님 |
| [bosonic canonical pushforward](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md) | finite Gaussian rays, Wick 부호, conformal prescription의 필요성 | nonlinear scale-factor ends와 full BFV glue는 열려 있음 |
| [affine phase-band class](../../cpt_temporal_folded_susy/GATE1_AFFINE_PHASE_BAND_RELATIVE_CLASS.md), [phase-locked ends](../../cpt_temporal_folded_susy/GATE1_PHASE_LOCKED_AFFINE_FIELD_END_CONSTRUCTION.md) | fixed-a의 finite-regulator scalar relative class/end 구성 | a를 적분 변수로 풀어 놓은 joint BFV domain과 다름 |

따라서 “어떠한 relative class도 없다”는 표현은 잘못이다. 고정한 축소 범위의 구성은
존재한다. 여기서는 그것을 unfixed-a source로 확대할 때 생기는 경계 조건만 살핀다.
[V=0 BFV 이식 반례](../../cpt_temporal_folded_susy/GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY.md)도
그대로 유지한다.

## 2. 한 질문, 한 출력, 적용 범위

질문은 다음과 같다.

> 같은 Starobinsky constraint에 대해, 추가 ghost/boundary prescription 없는
> \(a\geq\varepsilon>0\) cutoff face가 BRST-invariant face를 이루는가?

출력은 아래의 boundary ideal test와 exact on-shell witness다. \(a\ne0\)에서의
고전 BFV 대수를 다루며, \(\varepsilon\)은 고정한 양수다. gauge parameter의 Grassmann
성분과 cutoff 숫자 \(\varepsilon\)은 서로 다른 객체다. 이 결과로는 원래 cycle,
\(n_\sigma\), 적분의 수렴, Ward identity, physical state를 주장하지 않는다.

planner에는 source-defined regulated joint class 또는 정확한 경계 장애물을 출력으로
명시했다. 분류는 `CURRENT_BLOCKER_CANDIDATE`였지만, 실제로 이 메모가 공급하는 것은
source constructor의 한 필요조건뿐이다. 전체 relative class를 공급하지 않으므로
G1 resolution으로 세지 않는다. 의존 경로는 G1 stable global vector → G2 CFU → G3
BFV/Pfaffian/Pin → G4 positive domain/closure → G5 persistent effect → full 3+1,
UV, GR+QFT, normalized observable/likelihood와 external review다.

## 3. 부호와 constraint를 먼저 고정한다

Phase 24의 Dirichlet-reduced Euclidean action에서 \(T=iN\),
\(e^{-I_E}=e^{iS_L}\) convention을 사용하면 Lorentzian phase-space action은

\[
S_L=\int ds\,[p_a\dot a+p_\phi\dot\phi-NH_L],
\]

\[
H_L=-\frac{p_a^2}{24\pi^2a}+\frac{p_\phi^2}{4\pi^2a^3}
      -6\pi^2a+2\pi^2a^3V(\phi),\qquad
V=\frac34(1-e^{-\beta\phi})^2,\quad \beta=\sqrt{2/3}.
\]

이는 \(H_E\)의 potential 항을 그대로 Lorentzian이라고 이름 붙인 것이 아니다.
\(H_E\)의 그 항은 \(+6\pi^2a-2\pi^2a^3V\)다. 위 식은 국소 해의 Lorentzian
기여 여부나 integration contour의 analytic continuation을 인증하지 않는다.

하나의 Abelian Hamiltonian constraint와 lapse momentum \(\Pi\)에 대해

\[
\Omega=cH_L+\rho\Pi,\qquad QF=\{F,\Omega\}_{\mathrm{graded}}
\]

로 쓴다. \(c\)는 minimal constraint ghost, \(\rho\)는 lapse primary constraint의
ghost다. \(H_L\)가 \(N,\Pi\)와 무관하고 \(\{H_L,H_L\}=0\)이므로 이 대수에서
\(Q^2=0\), \(Qc=0\)이다. quantum ordering/anomaly 판정은 여기서 하지 않는다.

## 4. 경계가 불변이라는 가정을 깨는 정확한 예

\(a\ne0\)인 국소 함수 superalgebra에서 bare face의 ideal을
\(\mathcal I_\varepsilon=\langle a-\varepsilon\rangle\)로 놓으면

\[
Q(a-\varepsilon)=-\frac{c\,p_a}{12\pi^2a}.
\]

이를 face에서 제한해도 일반적으로 0이 아니다. 따라서
\(Q\mathcal I_\varepsilon\not\subset\mathcal I_\varepsilon\)다.
단순히 constraint 밖에서만 생기는 문제도 아니다. 다음 family는 실제 양수
Starobinsky potential에서 constraint를 만족한다.

\[
0<\varepsilon\leq1,\quad a=\varepsilon,\quad
\phi_*={\ln2\over\beta},\quad V(\phi_*)={3\over16},\quad
p_a=12\pi^2\varepsilon,
\]

\[
p_\phi^2=48\pi^4\varepsilon^4-\tfrac32\pi^4\varepsilon^6
=\tfrac32\pi^4\varepsilon^4(32-\varepsilon^2)>0.
\]

어느 실수 부호의 \(p_\phi\)를 택해도 직접 대입하면

\[
H_L=-6\pi^2\varepsilon+
\left(12\pi^2\varepsilon-\tfrac38\pi^2\varepsilon^3\right)
-6\pi^2\varepsilon+\tfrac38\pi^2\varepsilon^3=0,
\]

\[
X_{H_L}a=-\frac{p_a}{12\pi^2a}=-1.
\]

그러므로 **constraint surface에서도 이 face를 가로지르는 flow가 있다**.
이 witness는 한 phase-space point의 family다. 전체 궤적, 인증된 Euclidean branch,
\(a=0\)까지의 flow, 또는 수렴하는 BFV path integral을 만든 예는 아니다.

## 5. 가능한 대수적 보완과 그 한계

face에서 minimal ghost도 제한하는 ideal

\[
\mathcal J_\varepsilon=\langle a-\varepsilon,c\rangle
\]

을 선언하면 \(Q(a-\varepsilon)\in\mathcal J_\varepsilon\), \(Qc=0\)이므로
derivation의 곱 법칙으로 \(Q\mathcal J_\varepsilon\subset\mathcal J_\varepsilon\)다.
이것은 경계 ideal 수준의 명시적인 보완 후보다.

이는 minimal-ghost algebra의 보존 ideal이며, 완성된 물리적 boundary condition은 아니다.
\(c=0\)은 그 face에서 허용 게이지 변환을 제한한다. antighost·nonminimal
multiplier 조건, gauge fermion, boundary polarization과 action boundary term,
Liouville/BFV measure는 아직 정하지 않았다. 이 ideal만으로 전체 게이지군의 동등한
표현, boundary flux의 실제 소거, physical projector를 주장할 수 없다.
다른 선택으로는 적합한 paired-face cancellation이나 relative-divisor 처방도 있을 수
있지만 여기서 구성하지 않았다. \(\varepsilon\to0\)에서 \(1/a\) 계수가 특이해지므로
고정 \(\varepsilon\)의 ideal 계산을 그대로 극한으로 옮기지 않는다.

즉 source 후보의 판별 질문은 구체적으로 좁혀진다.

> 이 후보는 bare face에 머무는가, 아니면 동일한 action과 ghost·measure 조건에서
> 경계 제한 또는 flux cancellation을 실제로 정의하는가?

후자는 별도 construction이 필요한 질문이며, 여기의 ideal 조건 하나는 충분조건이 아니다.

## 6. 왜 발견으로 승격하지 않는가

invariant action만으로 path integral의 constraint 성질을 보장할 수 없다는 일반론은
오래된 것이다. [Halliwell–Hartle 1991의 원문, pp. 1170–1171](https://web.physics.ucsb.edu/~quniverse/papers/wf_inv_op_const-halliwell86.pdf)은
measure와 history class의 불변성도 전제한다. [Halliwell 1988의 초록](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.38.2468)은
minisuperspace BFV에서 multiplier 적분 범위와 positive-metric restriction 문제를 다룬다고
명시한다. 후자는 공개 초록 범위만 확인했으며 그 논문의 미열람 본문 정리를 인용하지 않는다.

[Banihashemi–Jacobson v3 §II](https://arxiv.org/html/2405.10307v3)는 momentum-first lapse
contour와 trace-momentum gauge 가정을 함께 다룬다. 그 가정을 retained real \(p_a\)
block에 이식할 수 없다는 점은 기존 pushforward 문서의 반례가 이미 설명했다.
그 논문의 §II 각주 2도 positive spatial metric의 canonical-domain 문제를 해결하지 않고
논의 범위에서 유보한다. 따라서 해당 lapse 처방을 이 메모의 경계 문제에 대한 해결로
인용하지 않는다.
[Witten §3](https://arxiv.org/html/1001.2933)의 relative-cycle 방법도 source의 action,
허용 end와 cycle을 명시한 뒤 사용하는 형식이다. 이 자료들은 ICE의 원래 cycle을 선택해
주지 않는다.

새 메모의 효용은 알려진 원리를 현재 source의 정확한 변수·부호·경계에 적용해 보완
질문을 만드는 데 있다. 신규성이나 독립적인 물리 현상은 확인되지 않았다. 선택군 아래의
불변 효과, 같은 모델의 독립 관측 consumer, false-signal 제거를 갖춘 mechanism을
구성한 것이 아니므로 physics/TOE 승격을 하지 않는다.

## 7. 확인 기록

- principal failure는 `gauge`다. 관련 control은 Euclidean/Lorentzian 부호 대조,
  양수 potential에서의 exact on-constraint witness, bare/repaired ideal 비교 세 가지다.
- 수식은 본문에서 직접 유도·대입했고 별도 read-only 검토가 같은 witness와 ideal closure를
  독립 대조했다. 숫자 적분, Python runner, 계산 결과 JSON은 만들거나 재실행하지 않았다.
- source 발견 query는 `./ice literature search "BFV minisuperspace boundary integration domain Halliwell" --json`
  및 웹 검색이다. OpenAlex 응답 시각은 `2026-09-06T12:57:26.853Z`였고 관련 work metadata를
  반환했다. 발견 metadata와 위에서 읽은 원문은 역할이 다르다. 문헌 검색이 신규성을 증명하지 않는다.
- 사전 planner의 첫 입력은 500자 상한을 초과해 exit 2였고, 500자 이내로 재작성한
  source-domain 질문은 exit 0 / `CURRENT_BLOCKER_CANDIDATE`였다. planner는 실행 승인이나
  evidence가 아니며 이 메모는 supporting method로 남는다.
- canonical graph의 기존 claim/evidence/status와 root certificate를 바꾸지 않는다.
  이 방법 메모를 별도의 evidence edge, repro entry, 자동 계산 요청으로 만들지 않았다.
