# CPT 접합과 original cycle: 경계 관계에서 source를 만드는 설계

2026-09-06 · **DESIGN_CANDIDATE / SUPPORTING_METHOD**.

## 제안

현재의 가장 구체적인 후보는 **추가 막이 없는 CPT-compatible 경계 관계를 먼저 쓰고,
경계 상태와 Lorentzian source를 별도로 정의하는 것**이다. 경계 변분을 계산한 뒤
남는 항이 있을 때만 이를 상쇄하는 seam action을 구한다. 이 방식은 접합 계수를 기존
saddle에 맞추는 자유도를 줄이고, source가 무엇을 계산하는지를 먼저 드러낸다.

문헌에 ICE의 완성된 source가 있다는 뜻은 아니다. 아래는 기존 연구 위에 얹는 선언된
후보와 판별 방법이다. 새 original relative class, global intersection vector, 물리 상태
또는 과학적 발견이 이번에 구성되었다고 주장하지 않는다.

```mermaid
flowchart LR
  T["CPT의 장·운동량 작용"] --> B["경계 관계와 남는 변분"]
  B --> S["seam kernel / 경계 상태"]
  S --> G["규제된 original joint cycle"]
  G --> N["기여 saddle와 signed intersection"]
```

화살표는 필요한 입력의 연결이다. 한 상자가 다음 상자의 성립을 증명하지 않는다.
기존 [source 감사](ICE_STAROBINSKY_ORIGINAL_SOURCE_SELECTION_AUDIT_2026-09-06.md),
[면적 seam 반례](ICE_STAROBINSKY_AREA_SEAM_JUNCTION_OBSTRUCTION_2026-09-06.md),
[polynomial BFV chart](../../cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md)는
각각 원문 입력, 특정 후보의 실패, source를 표현할 좌표 자료를 제공한다.

## 1. CPT가 주는 조건과 주지 않는 선택

Boyle–Finn–Turok의 긴 논문 [arXiv:1803.08930, §II.4–5, eqs. (43)–(50)](https://arxiv.org/html/1803.08930)은
서로 다른 CPT-invariant vacuum의 family를 명시한다. 그중 preferred vacuum은 해당
배경의 점근적 입자수·에너지 기대값을 최소화하는 기준으로 고른다. 따라서 그 논문조차
“CPT 대칭 하나로 모든 상태가 유일하게 정해진다”는 근거는 아니다. 특히 ICE의 유한
interior 경계에는 그 점근적 관측자와 입자 개념이 아직 없다.

이 문헌의 Big-Bang radiation 배경 및 test-field vacuum 선택을 closed \(S^3\)
Starobinsky의 lapse–field–ghost 적분 cycle로 옮길 수는 없다. 가져올 수 있는 원리는
**반사 대칭을 만족하는 family를 정한 뒤, 그 안의 상태 선택 근거를 따로 제시한다**는 것이다.

## 2. seam action을 구하는 직접적인 방법

[Cattaneo–Schiavina의 ADM BV–BFV 분석](https://arxiv.org/html/1509.05762),
Proposition 2.2와 Theorem 2.5는 bulk action의 boundary variation에서 canonical 경계
형식과 ghost를 포함하는 경계 구조를 얻는다. GHY 항은 boundary primitive의 exact
부분에 영향을 주므로 action convention과 함께 기록해야 한다. 이 결과는 space/time-like
경계의 ADM 이론에 대한 것이며 complex CPT seam의 완성 정리는 아니다.

ICE의 실수 homogeneous bosonic 경계에서 우선

\[
 q=(a,\phi),\quad p=(p_a,p_\phi),\quad
 \alpha=p_a\,\delta a+p_\phi\,\delta\phi,\quad \omega=\delta\alpha
\tag{1}
\]

를 사용한다. Scalaron을 CP-even 실수 scalar로 두는 **선언된 후보**는

\[
 T_\Sigma:(a,\phi;p_a,p_\phi)\longmapsto(a,\phi;-p_a,-p_\phi).
\tag{2}
\]

이때 손으로 바로 검산할 수 있는 것은

\[
 T_\Sigma^*\alpha=-\alpha,\qquad
 T_\Sigma^*\omega=-\omega,\qquad H_L\circ T_\Sigma=H_L.
\tag{3}
\]

마지막 식은 [같은 모델의 \(H_L\)](../../cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md)가
momentum에 quadratic이고 \(\phi\)는 바꾸지 않기 때문이다. Starobinsky potential은
\(\phi\mapsto-\phi\)에 대칭이 아니므로 scalar 부호를 임의로 뒤집는 mirror 처방은
이 후보와 다르다.

두 경계의 총 primitive를 \(\alpha_1+\alpha_2\)로 쓰는 convention에서는

\[
 \left.(\alpha_1+\alpha_2)\right|_{\operatorname{Graph}(T_\Sigma)}=0.
\tag{4}
\]

따라서 이 **실수 bosonic 경계 관계**에는 추가 \(S_\Sigma=0\)이 가능한 후보다.
총 형식이 \(\alpha_1-\alpha_2\)인 convention에서는 identity graph가 이 역할을 한다.
이미 orientation을 뒤집은 곳에 (2)의 부호를 다시 넣으면 다른 접합식이 된다.

일반적으로 선택한 관계 \(L\)에 남는 경계 1-form을
\(b=(s_1\alpha_1+s_2\alpha_2)|_L\)라 쓰자. Total action에 **\(+S_\Sigma\)**를 더할 때
필요한 조건은

\[
 \boxed{\delta S_\Sigma=-b.}
\tag{5}
\]

\(b=0\)이면 별도 interaction이 필요 없다. \(b=\delta I\)가 exact이면
\(S_\Sigma=-I\)로 작용을 구한다. \(\delta b\ne0\)이면 현재 field space에서 함수 하나를
더해 상쇄할 수 없다.
closed이지만 globally non-exact이면 국소 생성함수는 가능해도 전역 단일값 작용은 아직 없다.
추가 seam field가 필요하다면 그 동역학과 경계 phase space도 실제로 정의해야 한다.

(4)는 실제 glued solution의 존재를 증명하지 않는다. 기존 real equal-endpoint 해를
두 번 쓰면 자동으로 (2)를 만족하는 것도 아니다. 이 계산은 real ghost-number-zero
경계에 한정되며, fermion/Pin 구조, lapse primary pair, odd variables, BFV charge,
complex anti-linear lift와 quantum pairing은 별도로 남는다. 기존 면적 seam no-go가
동일한 물리의 부호 변경으로 사라졌다는 뜻도 아니다.

## 3. 경계 상태를 명시하면 접합의 양자적 뜻이 드러난다

[CMR의 perturbative BV–BFV gluing, §1.1–1.5](https://arxiv.org/html/1507.01221)은
경계 polarization을 정한 상태의 pairing과 BV pushforward로 접합을 다룬다.
고전 운동량 일치만으로 양자 measure나 kernel이 생기지 않는 이유다. 이 논문의
perturbative BF-like 구성은 nonperturbative Einstein–Starobinsky 적분을 제공하지 않는다.

별도의 positive Hilbert space와 그 위 antiunitary \(\Theta\)가 이미 정의되었다고
가정하면, CPT-compatible **상태 family**를 만드는 간단한 후보는

\[
 \rho_{\rm CPT}=\frac12\left(\rho+\Theta\rho\Theta^{-1}\right).
\tag{6}
\]

\(\rho\)가 positive normalized trace-class이고 \(\Theta^2\)가 central phase이면
(6)도 positive·normalized·CPT-invariant다. 이는 antiunitary conjugation이 positivity와
실수인 trace를 보존한다는 직접 대수적 사실이다. 보통 mixed state가 되며 vacuum을
유일하게 고르지 않는다. \(\Theta\)가 사용한 constraint subspace와 operator domain을
보존하는지, dynamics도 CPT-covariant인지 추가로 확인해야 한다. (6)이 gravity의 positive
physical Hilbert space나 G4를 만들어 주지는 않는다.

경계 상태가 path integral에 어떤 항으로 나타나는지 보여 주는 다른 primary 예는
[Di Tucci–Lehners, arXiv:1903.06757](https://arxiv.org/html/1903.06757)다. 그 논문은
positive cosmological constant 모델에서 초기 경계에
\(\alpha q_0+q_0^2/(2\beta)\)를 넣어 Robin 조건을 만들며, 이를 초기 크기와 운동량의
불확실성을 가진 상태로 해석한다. 경계 조건을 바꾸면 lapse saddle과 singularity도
바뀐다. 논문은 thimble을 통한 정의도 명시하므로, boundary term이 기존 real contour와의
동치를 자동 증명한 것으로 읽지 않는다. 그 \(q\)는 \(a^2\)이고 모델은 상수 \(\Lambda\)다.
수치 계수나 안정성을 ICE로 복사하지 않고 **경계 상태가 source의 일부**라는 예로 쓴다.

## 4. CPT와 closed-time-path를 구별하는 대조

[Crossley–Glorioso–Liu, §II.1 eqs. (85)–(94)](https://arxiv.org/html/1511.03646)은
밀도행렬의 진화를

\[
 Z[J_+,J_-]=\operatorname{Tr}\bigl(U[J_+]\rho_0U[J_-]^\dagger\bigr)
\tag{7}
\]

로 쓴다. Path integral에는 \(S_+-S_-\), 초기 \(\rho_0(q_{+,i},q_{-,i})\), 마지막의
ordinary trace sewing \(q_{+,f}=q_{-,f}\)가 각각 들어간다. 마지막 경계 변분은
\((p_{+,f}-p_{-,f})\delta q_f\)다. 이 minus sign에 CPT를 이유로 또 momentum reversal을
넣지 않는다. (7)의 두 branch는 ket/bra이며 그것만으로 두 물리적 우주가 아니다.

정규화된 상태와 unitary \(U\)에서는 \(Z[J,J]=1\)이다. 이는 source 구성의 좋은
대조지만, \(\Theta\) 자체를 ordinary trace 안에 넣는 식으로 CPT seam을 정의하지
않는다. Anti-linear operator에는 일반적인 basis-independent linear trace를 그대로
적용할 수 없다. 별도 linear seam insertion도 (7)의 normalization을 자동 상속하지 않는다.

또한 이 대조는 **fixed-lapse unitary evolution**에만 그대로 적용된다.
\(\int dN\,U_N\)인 Green operator나 group average는 unitary evolution이 아니므로
\(\operatorname{Tr}(G\rho G^\dagger)=1\)을 요구하면 잘못된 판별이 된다.

## 5. original cycle은 어떤 적분을 정의하는지에서 시작한다

현재의 두 interior boundary 문제를 유지한다면, 첫 source 가설로는 **Lorentzian
transition kernel과 positive-lapse Green prescription**을 명시하는 안이 검토하기 좋다.
이는 CPT가 선택한 답이 아니라, 계산할 대상을 전이 문제로 정한 모델링 선택이다.
physical constraint state를 목표로 한다면 full-lapse rigging construction을 별도 source로
정의해야 한다. 두 적분을 convergence가 좋은 쪽으로 바꿔 같은 source라 부르면 안 된다.

지정한 self-adjoint \(\widehat H\), 공통 domain, \(\hbar=1\)의 operator control에서는

\[
 U_N=e^{-iN\widehat H},\qquad
 G_\epsilon=\int_0^\infty dN\,e^{-\epsilon N}U_N
 =-i(\widehat H-i\epsilon)^{-1},\qquad
 (\widehat H-i\epsilon)G_\epsilon=-i\mathbf1.
\tag{8}
\]

이에 비해 \(\int_{\mathbb R}dN\,U_N=2\pi\delta(\widehat H)\)는 적절한 test space에서
정의하는 distributional group averaging이다. 이 구별은 이미
[Phase 27 §2](../../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md)와
[source 문헌 감사](ICE_STAROBINSKY_SOURCE_LITERATURE_ADVERSARIAL_AUDIT_2026-09-06.md)에 있다.
재발견으로 세지 않는다. (8)의 abstract operator identity는 ICE의 self-adjoint realization이나
phase-space Fubini interchange를 증명하지 않는다.

실제 original **joint** cycle에는 lapse 선 하나보다 많은 정보가 들어간다.
\(N=0\) contact와 큰 \(|N|\)의 끝, \(a>0\) 경계와 scalar·momentum의 원래 domain,
BFV ghost endpoint polarization 및 Berezin measure, bosonic orientation과 regulator의
제거 순서를 같은 source로 명시해야 한다. 한 공통 \(N\mp i0\)가 retained gravity/scalar
real momentum 축을 모두 감쇠시킨다는 처방은
[기존 finite pushforward 검사](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md)에서
실패했다. 별도 규제나 복소 momentum ray를 택할 때에는 그 정의와 원래 oscillatory
source와의 관계를 보여야 한다.

[Feldbrugge–Lehners–Turok, §II eqs. (6)–(9)](https://arxiv.org/html/1703.02076)의
Picard–Lefschetz 구성은 주어진 original domain에서 시작하여
\(n_\sigma=\langle\Gamma_{\rm orig},\mathcal K_\sigma\rangle\)로 기여를 판정한다.
우리가 채택할 방법은 이 순서다. 가장 마음에 드는 saddle의 thimble을 original source라고
역지정하지 않는다. 처음부터 thimble-defined state를 가설로 삼을 수도 있지만, 그 경우는
다른 source 선택이며 기존 Lorentzian source에서 도출되었다는 주장이 아니다.

규제된 finite-dimensional bosonic body에서 상대 class를 쓸 때에는 ambient complex
space, singular divisor, decay ends와 cutoff faces를 정해야 한다. Ghost는 그 위 ordinary
bosonic contour로 그리지 않고 Berezin/BFV 자료로 함께 처리한다. 모든 field를 먼저
적분해 lapse-only contour로 줄이는 단계에도 normalization·branch·끝의 동치가 필요하다.
[polynomial chart](../../cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md)의
\(N=24\pi^2u^{3/2}n\)도 field-dependent lapse ends와 square-root/log lift를 그대로
운반해야 한다. 독립적인 \((u,v,n)\) box로 교체하면 다른 source가 된다.

## 6. 지금 검토할 작업 단위와 판별 기준

첫 출력은 **같은 모델의 경계 source 명세 하나**다. 그 안에 (2)의 real bosonic 후보를
어떤 oriented boundary에 쓰는지, full homogeneous BFV extension이 가능한지,
\(+S_\Sigma\)가 상쇄해야 할 실제 1-form, boundary kernel/polarization, Green인지
rigging인지의 의미를 함께 고정한다. 이 명세가 다음 global 계산의 입력이다.

| 순서 | 만들어야 할 것 | 그 단계에서 후보를 구별하는 결과 |
| --- | --- | --- |
| 경계 | 실제 BFV boundary relation과 \(b\) | \(b=0\), exact defect, 또는 관계/field-space 보완 필요 |
| 상태와 kernel | 선언한 경계 상태, measure, operator/domain 또는 이에 준하는 규제 source | CPT covariance·constraint compatibility; fixed-lapse composition/identity가 맞는가 |
| original chain | 같은 source의 \(\Gamma_{m,\epsilon}\)와 모든 boundary/end | Green의 contact 또는 rigging의 constraint support와 일치하는가 |
| global transport | 그 chain의 saddle/sheet/singular/Stokes/good-end census | 빠짐없는 oriented intersection vector; 안정적 zero vector도 허용 |

이 표는 계산을 자동 생성하는 실행 계약이 아니다. 지금은 사용자 요청에 따라 source를
정의할 방법을 설계했다. 기존 fixed midpoint, local constrained \(S_C\), exact quantum
kernel은 서로 다른 객체이므로 입력을 소급해 동일시하지 않는다.

발견 후보가 되려면 이 처방에서 **임의로 맞추지 않은 구별 가능한 결과**가 나와야 한다.
같은 source를 나타내야 하는 사전 선언된 gauge·regulator·chart 선택을 바꿔도 남는지,
같은 graph 안의 독립된 downstream consumer 둘 이상에 같은 mechanism이 나타나는지를
따로 검토한다. 경계 상태의 width, lapse source type, topology를 바꾸는 것은 보통 물리
가정의 변경이며 단순 gauge sweep이 아니다. CPT-symmetric 상태를 만들 수 있다는 대수적
사실이나 SK normalization 자체는 새 물리 신호가 아니다.

## 검색·검토 기록

- 문헌 검색: `./ice literature search "CPT quantum cosmology boundary state Lorentzian path integral Robin" --json`,
  `2026-09-06T16:39:03.119Z`. 위 링크의 primary text를 별도로 읽었다.
- 사전 planner는 `CURRENT_BLOCKER_CANDIDATE`였으나 실제 출력은 construction design이다.
  Canonical blocker는 `open:gate1-original-cycle-signed-global-intersections`, missing object는
  source-defined regulated joint relative class다. 설계의 bounded 출력은 경계 관계·source
  type·끝 조건을 구별하는 후보 명세이며 그 class의 존재 증명이 아니다.
- dependency는 G1 → G2 uniform kernel → G3 absolute determinant/gluing → G4 physical
  state/domain → G5 persistent interaction → full-theory/empirical review다. 현재 계획을
  G1 해소나 downstream 진전으로 세지 않는다.
- 독립 읽기 검토로 (2)–(5)의 orientation/exactness, (6)의 antiunitary positivity 가정,
  (7)–(8)의 unitary/resolvent 구별과 primary 문헌의 모델 범위를 대조했다.
  주된 실패 위험은 `inference`; 관련 부호는 손으로 대입했다. 새 runner는 실행하지 않았다.

이 문서는 연구 설계와 직관 연결이다. Canonical evidence edge와 repro manifest는 변경하지 않는다.

2026-09-07 [후속 BFV/Ward source 제안](ICE_BFV_CPT_SEAM_WARD_SOURCE_PROPOSAL_2026-09-07.md)은
ghost/lapse까지의 고전 경계 반사 후보, positive-lapse source의 CPT covariance,
독립 lapse 적분과 접합 순서, 실제 cutoff/regulator의 Ward defect를 구체화한다.
다음 출력은 하나의 finite sewn source의 경계 defect이며, original class는 여전히 미해결이다.
