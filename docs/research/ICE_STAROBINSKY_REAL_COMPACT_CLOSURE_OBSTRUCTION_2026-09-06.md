# Starobinsky 실수 compact closure의 경계 항등식

2026-09-06 · **SUPPORTING_METHOD / ANALYTIC OBSTRUCTION**.

## 질문과 범위

다음 한 가지를 묻는다.

> 기존의 실수 Dirichlet seed를 scalar seam source 없이 smooth real periodic,
> regular two-pole, 또는 real turning-equator source로 닫을 수 있는가?

여기서 “닫는다”는 실수 \(O(4)\), 공간 단면이 \(S^3\)인 Euclidean minisuperspace 안에서
스칼라 경계항이 사라지는 completion을 뜻한다. 결론은 **아니다**. 이 특정
closure들은 비자명한 실수 Starobinsky scalar solution과 양립하지 않는다.

이는 analytic supporting result다. 원래 lapse--field--gauge cycle, BFV source,
complex saddle, measure, physical state, 또는 G1 global intersection을 만들거나
배제하지 않는다. 사전 planner는 `INSUFFICIENT_ROUTE_EVIDENCE`였고, 이 메모도
supporting 지위를 유지한다.

## 선언한 실수 방정식

[Phase 24](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md#1-frozen-model-and-supplied-benchmark)의 proper-time Euclidean convention에서

\[
 V(\phi)=\frac34(1-e^{-\beta\phi})^2,\qquad \beta=\sqrt{2/3},
\]
\[
 \phi''+3\frac{a'}a\phi'=V_{,\phi},\qquad
 \mathcal C=a'^2-1-\frac{a^2}{3}\left(\frac12\phi'^2-V\right)=0.
\tag{1}
\]

길이 \(T=R-L>0\)인 유한 연결 구간, 실수 \(C^2\) 해, \(a>0\)인 interior와
매끈하고 유한한 scalar를 가정한다. 첫 식은

\[
 (a^3\phi')'=a^3V_{,\phi}.
\tag{2}
\]

를 준다.

## 정확한 경계 항등식

(2)에 \(\phi\)를 곱해 적분하면

\[
 B_{L,R}:=[a^3\phi\phi']_L^R
 =\int_L^R a^3\bigl((\phi')^2+\phi V_{,\phi}\bigr)\,d\tau.
\tag{3}
\]

Starobinsky potential에서는

\[
 \phi V_{,\phi}=
 \frac{3\beta}{2}\phi e^{-\beta\phi}(1-e^{-\beta\phi})\geq0,
\tag{4}
\]

이고 등호는 \(\phi=0\)일 때뿐이다. 이는 \(\phi>0\)에서는 두 인자가 양수이고
\(\phi<0\)에서는 둘 다 음수이기 때문이다. \(V''\)의 부호나 potential의 convexity는
쓰지 않는다.

따라서 \(B_{L,R}=0\)이면 integrand가 거의 모든 interior에서 영이고,
연속성으로

\[
 \phi'=0,\qquad \phi=0
\tag{5}
\]

가 전 구간에서 성립한다.

## 사라지는 경계항의 세 경우

- **두 regular pole:** 표준 smooth pole에서 \(a\to0\), scalar는 finite이며
  \(\phi'\)도 regular하다. 양끝의 \(a^3\phi\phi'\)가 0이다.
- **regular pole에서 real-to-real equator까지:** pole 쪽 항은 0이고, 여기서
  말하는 turning equator에는 \(a'=\phi'=0\)을 요구한다. 실수 Euclidean derivative가
  \(\tau=\tau_e+it\)에서 실수 Lorentzian derivative로 매끈히 계속되려면 이 조건이
  필요하다. \(a'=0\)만으로는 (3)의 경계항이 사라지지 않는다.
- **smooth periodic gluing:** \(a,\phi,\phi'\)가 같은 orientation으로 smooth-match하면
  endpoint terms가 cancel한다.

세 경우 모두 (5)를 강제한다. 이제 (1)의 constraint에
\(\phi=\phi'=V=0\)을 대입하면

\[
 a'^2=1.
\tag{6}
\]

그러므로 이 \(O(4)\) closed-FRW ansatz 안에서는 turning point \(a'=0\)도,
두 regular pole 사이에서 되돌아오는 compact solution도 없다. 매끈한 양의 periodic
\(a\)도 극값에서 \(a'=0\)이어야 하므로 불가능하다. 다만 \(\phi=0, a=\tau\)인
한-pole flat ball의 유한 구간은 허용된다. 임의의 모든 유한 cap을 배제한 것은 아니다.

## 기존 equal-Dirichlet seed와의 관계

양끝 \(q_- =q_+=(a_b,\phi_b)\), \(\phi_b>0\)는 (3)의 경계항을 없애지 않는다.
이 경계값과 연속성 때문에 양끝 근방에서 (3)의 integrand는 양수다. 따라서
\(B_{L,R}>0\)이고

\[
 p_{\phi,R}-p_{\phi,L}
 =2\pi^2\bigl(a_R^3\phi'_R-a_L^3\phi'_L\bigr)
 =\frac{2\pi^2}{\phi_b}B_{L,R}>0,
\tag{7}
\]

여기서 \(p_\phi=2\pi^2a^3\phi'\)다. [Phase 24의 endpoint convention](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md#2-what-is-varied)은
\(\nabla I=(-p_-,p_+)\)를 사용한다.

미분 가능한 fixed-time principal branch \(S_T\)가 존재하는 곳에서, 양끝 \(\phi\)를
같이 바꾸는 diagonal derivative는

\[
 \frac{d}{d\phi_b}S_T(a_b,\phi_b;a_b,\phi_b)
 =p_{\phi,R}-p_{\phi,L}>0.
\tag{8}
\]

constraint-extremized principal action에서도 같은 식은 lapse modulus가 실제로
stationary이고 \(\partial_T S=-H_E=0\)인 branch에서 envelope theorem으로
따라온다. 즉 \(dT/d\phi_b\) 항을 임의로 버리면 안 된다.

이는 diagonal kernel 자체를 금지하지 않는다. 단지 scalar seam source 없이 그
common-\(\phi\) diagonal을 integrated trace의 stationary condition으로 요구하는
이 closure 후보는 (8)과 양립하지 않는다. 기존 continuum certificate는 equal
endpoint value가 reflection symmetry나 momentum matching을 뜻하지 않는다고 이미
명시한다([certificate memo](ICE_STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_2026-09-06.md)). 따라서 이 결과는 그 local seed, [principal-branch flow](../../cpt_temporal_folded_susy/STAROBINSKY_PRINCIPAL_BRANCH.md), 또는 [Morse fiber result](../../cpt_temporal_folded_susy/STAROBINSKY_MORSE_FIBER_POSITIVITY.md)를 바꾸지 않는다.
실수 smooth stationary point의 부재를 trace 적분값이 0이라는 결론으로 바꾸지도 않는다.

## 제외 범위와 문헌 위치

이 논증은 complex saddles, singular/noncompact ends, non-Dirichlet scalar source,
다른 topology 및 full four-dimensional compact geometry의 no-go가 아니다.
고전 방정식의 검사이므로 quantum ordering이나 물리적 spectrum도 판정하지 않는다.
특히 \(\phi=0\)인 full Einstein-scalar 방정식은 Ricci-flat vacuum으로 가지만,
다른 topology의 compact Ricci-flat geometry를 이 minisuperspace 계산으로 배제하지
않는다. CPT fold도 이름만으로 이 가정을 만족하지 않는다. orientation reversal,
복소 켤레, corner/seam 작용에는 고유한 junction 조건이 필요하며, distributional
scalar source가 있으면 (3) 자체에 그 항을 포함해야 한다.

Chen--Yeh--Yeom은 closed homogeneous Starobinsky-type model에서 compact
Hartle--Hawking state를 특정 no-boundary prescription으로 다룬다
([arXiv:1903.12045, §II.1, §III.1--2](https://arxiv.org/html/1903.12045)). 그 논문의
equator 연결에는 slow-roll constant-potential 근사가 들어간다. 여기서는 그 배경을
기울기가 0이 아닌 Starobinsky potential의 **정확한 all-real regular cap**으로 읽는
해석만 제한한다. 근사 power spectrum 계산이나 Hartle–Hawking proposal 전체를
반박하지 않는다. Jonas--Lehners의 abstract도
regular no-boundary solutions가 **complex** equations-of-motion solutions에 의존한다고
명시한다([arXiv:2008.04134](https://arxiv.org/abs/2008.04134)); 그 경우는 여기서
제외했다.

문헌 검색 기록: `2026-09-06T14:23:23.349Z`, query
`Starobinsky quantum cosmology no boundary Lorentzian path integral contour`.

## 검토와 disposition

주된 실패 위험은 `inference`다. 독립적인 읽기 검토로 (i) 두 scalar 부호에서의
\(\phi V'\)와 Euclidean constraint 부호, (ii) Dirichlet 경계와 smooth gluing의 차이,
(iii) flat-ball 및 complex/topology 예외를 대조했다. 증명은 (1)--(8)의 해석적 유도이고,
새 numerical runner·재실행·관측 데이터 분석은 하지 않았다. 신규성은 입증하지 않았다.

제외되는 것은 **경계항 없는 실수 smooth closure**다. 기존 equal-endpoint branch와
G1 original relative class의 미해결 상태는 유지된다. 남는 source 후보는 자기
boundary/seam 작용 또는 complex contour를 별도로 명시해야 하며, 이 결과가 그것을
선택하거나 후속 계산을 자동 생성하지 않는다. 방법 메모와 직관 지도의 연결만 추가하고
canonical evidence edge와 repro manifest는 변경하지 않는다.
