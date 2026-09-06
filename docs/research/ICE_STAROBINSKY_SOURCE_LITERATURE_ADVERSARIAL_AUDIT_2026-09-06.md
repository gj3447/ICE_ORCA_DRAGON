# Starobinsky source 문헌: 적분 처방을 가져오기 전의 두 검사

2026-09-06 · **SUPPORTING_METHOD / SOURCE_ADMISSIBILITY_REVIEW**.

Franken–Kaimakkamis–Partouche–Toumbas의
[*Ordering-Independent Wheeler–DeWitt Equation for Flat Minisuperspace Models*,
arXiv:2512.23656v2](https://arxiv.org/html/2512.23656v2)를 같은 모델의 source 후보로 검토했다.
그대로 ICE의 전역 source로 가져올 수 없다는 결론이다. 아래 두 문제는 논문에 적힌
실수 field contour와 fixed-endpoint positive-lapse 처방에 대한 것이며, 모든 ordering
결과나 가능한 보완을 반박하는 주장이 아니다.

## 1. 관련성이 있는 부분

논문의 “flat”은 공간 곡률 0이 아니라 **minisuperspace target metric의 flatness**다.
§5.1은 closed spatial \(S^3\) Starobinsky Einstein-scalar action과 Dirichlet boundary
term을 다룬다. 그 논문의 potential 계수 \(M^2\)를 ICE 단위의 \(3/4\)로 맞추면
§5.1 eq. (5.79)는 [Phase 24](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md)의
Lorentzian continuation과 같은 functional form이다. 반면 §2 eq. (2.18)의 lapse 범위는
양의 반직선이다. 이를 ICE의 미정인 full joint source와 동일시하지 않는다.

## 2. 공통 규제 부호가 실제로 감쇠시키는가

논문 §3 eqs. (3.36)–(3.38)는 실수 Lorentzian target의 Gaussian과 공통
\((1+i\kappa)\), \(\kappa>0\) 처방을 제시한다. 이 처방을 문자 그대로 적용해 보자.
\(\hbar,\Delta t>0\), \(\eta=\operatorname{diag}(-1,+1)\)이면 exponent는

\[
{i(1+i\kappa)\over2\hbar\Delta t}(-x_0^2+x_1^2),
\qquad
\operatorname{Re}(\text{exponent})
={\kappa x_0^2-\kappa x_1^2\over2\hbar\Delta t}.
\]

따라서 timelike 실수 축에서는 성장한다. 부호를 반대로 바꾸면 spacelike 축이 성장한다.
**공통 부호 하나로 두 실수 축의 절대 수렴을 얻을 수 없다.**
이 반례는 potential이나 discretization error에 의존하지 않는다.

예를 들어 quadratic part만 보면 \(x_0=e^{-i\pi/4}y_0\),
\(x_1=e^{+i\pi/4}y_1\)의 서로 반대 회전은 원래 순허수 exponent를 두 감쇠 Gaussian으로
바꾼다. 하지만 이를 실제 target boundary, nonlinear potential, endpoint, Jacobian과
함께 허용되는 contour deformation으로 구성하는 것은 별도 문제다. 논문의 일반적인
lapse-contour 언급은 이 field-contour 자료를 제공하지 않는다.

ICE에서는 이미 [finite bosonic pushforward §3](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md)이
retained gravity/scalar real momentum axes의 공통 lateral 부호 문제를 다룬다. 이번
검토는 그것을 새로운 물리 발견으로 세는 대신, 같은 실패 원리를 이 문헌의 **configuration
Gaussian 처방**에 적용해 source 수입을 제한한다.

## 3. 양의 lapse 적분은 어떤 끝점 항을 남기는가

논문 eqs. (3.45)–(3.49)의 homogeneous WDW 유도에는 zero-lapse 항 처리가 필요하다.
정규화된 fixed-interior-endpoint propagator \(K(t)\)는, 그 모델의 적절한 measure에 대해,

\[
i\hbar\partial_tK(t)=\widehat H K(t),\qquad K(0)=\mathbf1
\]

을 만족해야 한다. zero-time identity의 kernel은 \(\delta_\mu(q,q_i)\)다.
큰 \(t\) 끝을 제어하는 Abel regulator를 명시하면

\[
G_\eta=\int_0^\infty e^{-\eta t}K(t)\,dt,\qquad \eta>0,
\]

\[
(\widehat H-i\hbar\eta)G_\eta=-i\hbar\mathbf1.
\]

마지막 식은 integration by parts로 직접 나온다. 경계와 극한이 정의될 때
\(\eta\downarrow0\)에서 남는 source는 \(-i\hbar\delta_\mu(q,q_i)\)다.
이는 globally homogeneous constraint equation이 아니라 Green-kernel equation이다.
\(q_i\)를 피한 test support에서는 homogeneous 식을 얻을 수 있다.

이 부호와 contact를 확인하는 독립적인 finite spectral control도 가능하다.
\(\hbar=1\), \(H=\operatorname{diag}(1,-1)\)에 대해 정확히

\[
G_\eta=\operatorname{diag}\!\left({1\over\eta+i},{1\over\eta-i}\right),
\qquad (H-i\eta)G_\eta=-i\mathbf1.
\]

이 식은 양자 우주론의 해결이 아니라, half-line integral에서 identity source를 버릴 수
없음을 확인하는 정규화 control이다. pointwise decay를 distributional delta의 소멸로
바꾸면 안 된다. 특히 ICE의 equal **interior** endpoint는 contact를 피하는 조건이 아니다.
그 위치에서 delta를 유한 숫자로 평가하는 것도 허용하지 않는다.

다른 boundary state, 상대 contour, source-free construction이 이 항을 다르게 처리할 수는
있다. 다만 그런 입력을 선언하지 않고 fixed-endpoint half-line kernel에 덧씌우지 않는다.
논문의 eq. (3.48)에 등장하는 history-dependent imaginary-lapse sign도 하나의 고정
holomorphic integration cycle을 대신하지 못한다.

## 4. 연구에서 채택하는 결론

이 문헌의 같은 모델 action과 field-redefinition/measure 논의는 참고한다. 다음 항목은
추가 자료가 생기기 전에는 수입하지 않는다.

- 공통 \(\kappa\)가 실수 Lorentzian Gaussian 전체를 절대 수렴시킨다는 해석.
- positive-lapse fixed-endpoint kernel이 초기점까지 포함해 homogeneous WDW state라는 해석.
- 별도 field contour·relative end·full BFV orientation 없이 G1 source가 주어졌다는 해석.

이 결론은 [직관 연결 지도](../../research/intuition/ICE_ABSTRACTION_CONNECTIVITY_MAP_2026-09-06.md)의
“작용 → amplitude → state” 사이에서 빠진 입력을 구체적으로 가리킨다. 기존
[경계 ideal 메모](ICE_STAROBINSKY_BFV_BOUNDARY_IDEAL_METHOD_2026-09-06.md)와도 독립된
source 질문이다. 같은 모델의 고전적 좌표 변환은 따로 유도할 수 있지만, 그것만으로
위 두 source 문제를 해결했다고 해석하지 않는다.

## 5. 검토 범위와 provenance

- 2026-09-06 웹 검색으로 해당 v2 원문을 찾고 §2, §3 eqs. (3.36)–(3.49), §5.1,
  §6을 읽었다. 첫 검색은 `Starobinsky minisuperspace Hamiltonian polynomial canonical
  transformation scalar field R squared quantum cosmology`였다.
- 두 독립 read-only 검토가 규제의 실수부 부호, zero-time contact, source/ordering 구별을
  대조했다. 유효한 보완 가능성을 남기도록 결론을 제한했다.
- 주된 위험은 `inference`다. 관련 control은 timelike/spacelike 부호 대조와 normalized
  half-line operator identity다. 위 식들은 손으로 유도·대입했고 수치 실행을 주장하지 않는다.
- 일반적 conformal-sign 문제와 Green-function contact는 알려진 원리다. 이번 문헌 적용의
  우선권·신규성은 입증하지 않았으며 새 물리, TOE, 독립 관측 이상으로 승격하지 않는다.
- 원문 저자에게 연락하거나 외부에 게시하지 않았다. 이 검토는 repository-local 방법 메모이고
  canonical evidence/status 또는 repro manifest를 변경하지 않는다.
