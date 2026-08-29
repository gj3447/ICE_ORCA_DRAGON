# raw-\(C\) endpoint·spectral·RAQ 인증 연결부

> 작성일: 2026-08-29
> 지위: 다음 독립 계산을 고르기 위한 범위·인증 메모. 물리학, 양자중력 또는 TOE 결론이 아니다.

## 현재 실제로 확보된 것

선언된 실수 fiber 방정식은

\[
u''=A(Q;\lambda,\kappa)u,
\qquad
A=36\pi^4e^{2Q}+6\pi^2\lambda e^{3Q/2}-\kappa^2
\]

이고, 이번 계산의 범위는

\[
Q\ge4,\qquad |\lambda|\le10^{-4},\qquad
0\le\kappa\le8
\]

뿐이다. `raw_c_plus_endpoint_liouville_green_tail_bound`는 이 상자에서
\(A>0\)임과 Liouville--Green residual의 적분 가능성을 exact/rational
envelope로 검사했다. 실행 결과는 exact 22/22, theorem/scope guard 3/3이며,
격리 재현도 `REPRO`, `needs-attention 0`이다.

\(Q_+=4\)에서 관측된 보수적 예산은

\[
V_{\rm analytic}=7.73284516076509\times10^{-5},\qquad
V_{\rm bar}=9.44888512660652\times10^{-5},
\]

\[
E_{\rm bar}=e^{V_{\rm bar}/2}-1
=4.72455416684847\times10^{-5},
\]

\[
\frac{|(\log u)'-(\log w)'|}{\sqrt A}
\le \frac{2E_{\rm bar}}{1-E_{\rm bar}}
=9.44955478303119\times10^{-5}.
\]

여기서 \(w\)는 recessive Liouville--Green proxy다. 마지막 식은
\(\sqrt A\)-정규화 로그미분 **차이**이지 \((\log w)'\)에 대한 상대오차가
아니다. 전체 amplitude \((u,u')\) datum이나 그 \(\lambda\) 미분을 봉입한
결과도 아니다. 이 해석은 [NIST DLMF §2.7(iii), 특히 2.7.23--2.7.25](https://dlmf.nist.gov/2.7.iii)의
오차와 미분 오차 조항에 한정된다.

즉, 무한대의 recessive 조건을 유한 \(Q_+=4\)의 초기 datum으로 바꿀 때
생기는 **실수축 plus-tail 오차 예산** 하나는 확보됐다. 두 \(p\) 부호가
같은 \(|p|=\sqrt{2/3}\,\kappa\) coefficient를 갖는다는 범위 밖의
\(p\)-mixing extension 결론은 아니다.

### 같은 날 추가된 \(\lambda=0\) exact anchor

그 뒤 `python-flint==0.9.0`을 lock하고
`raw_c_lambda_zero_bessel_ball_transport`를 clean committed source에서
실행했다. 정확히 \(\lambda=0\)이면 \(x=6\pi^2e^Q\)에 대해 recessive 해가

\[
u_+(Q;\kappa)=K_{i\kappa}(x)
\]

이므로 수치 fundamental matrix 없이 \(+\infty\to Q_0=-4\) 방향을 exact
special function으로 전달할 수 있다. 관측 결과는 exact 4/4, Arb ball
35/35, theorem/scope guard 5개였고, 선언한 다섯 coarse bracket 각각에 적어도
하나의 real sign-changing zero가 있음을 인증했다. 각 고정밀 bracket의 exact
폭은

\[
1/20282409603651670423947251286016
\]

이다. bracket 전체에서 \(K_{i\kappa}(x_0)\)와 Wronskian은 0을 배제했고,
후자는 1을 포함했다. 격리 재현은 `REPRO`, `needs-attention 0`이었다.

이 결과는 아래 목록의 1번에서 **\(\lambda=0\) exact direction만** 닫는다.
\(F_\lambda\), nonzero-\(\lambda\) validated transport와 비실수 resolvent는
닫지 않는다.

### 같은 날 추가된 \(\lambda=0\) differentiated plus-tail datum

번호 없는 `raw_c_lambda_zero_differentiated_plus_tail`은 direction의 임의
amplitude에 무관한

\[
h(4;\kappa)=\left.\partial_\lambda[-u_Q/u]\right|_{\lambda=0}
\]

를 같은 다섯 root bracket 전체에서 봉입했다. 올바른 plus-end 조건은
\(h(\infty)=0\)이 아니라 \(u^2h\to0\)이고, 이에 따라

\[
h(Q)=u(Q)^{-2}\int_Q^\infty A_\lambda(s)u(s)^2\,ds,
\]

\[
h(4;\kappa)=\frac{1}{\sqrt{6\pi^2}\,K_{i\kappa}(x_+)^2}
\int_{x_+}^\infty\sqrt{x}\,K_{i\kappa}(x)^2\,dx
\]

를 사용했다. finite part는 rigorous `acb.integral`, improper tail은
DLMF 10.32.9의 integral representation으로부터 얻은 별도 analytic bound로
감쌌다. 실행 결과는 exact 9/9, Arb-ball 70/70, theorem/scope guard 6개다.
다섯 개별 enclosure는 모두 양수이고 전체 범위는 약
\(3.6942432085987834\)에서 \(3.6942535712156082\), 개별 폭은
\(4.62\times10^{-26}\) 이하, analytic tail upper bound는
\(6.02\times10^{-28}\) 이하이다. 격리 재현도 `REPRO`, needs-attention 0이다.

이 결과 자체는 **정확히 \(\lambda=0\), 다섯 bracket에서의 \(h(4)\)**만
닫는다. 아래의 후속 Green endpoint 계산이 별도로 \(J(-4)\)와 endpoint-only
\(h(-4)\)를 닫았지만, nonzero-\(\lambda\) tail, declared minus-end
\(\Gamma_1\) derivative, 정규화된 \(F_\lambda\), spectral/RAQ 출력은 그대로
열려 있다.

### 같은 날 추가된 \(\lambda=0\) node-safe Green endpoint

번호 없는 `raw_c_lambda_zero_node_safe_green_transport`는 pole이 생길 수 있는
\(h\)를 interior node 사이로 전개하지 않고

\[
J=-W(u,\partial_\lambda u)=u^2h,
\qquad J_Q=-A_\lambda u^2
\]

를 매끈한 변수로 사용했다. exact Bessel representation은

\[
J(-4;\kappa)=\frac1{\sqrt{6\pi^2}}
\int_{6\pi^2e^{-4}}^\infty
\sqrt{x}\,K_{i\kappa}(x)^2\,dx
\]

를 준다. finite part를 여섯 고정 positive-real subsegment에서 rigorous
`acb.integral`로 감싸고 \(x\ge32\)는 DLMF 10.32.9 기반 analytic tail로
더했다. clean bounded run은 exact 7/7, Arb-ball 61/61, guard 6개와 다섯
bracket 5/5를 통과했고 격리 재현도 `REPRO`다. bracket별 endpoint
\(h(-4)\)는 약

\[
0.1428500395,\ 0.5356890492,\ 0.9097203283,\
1.2870710317,\ 1.6705600982
\]

의 엄밀한 positive ball로 닫혔다.

이는 기존 \(h(4)\) 상태를 수치 전파한 것이 아니라 direct Green-integral
endpoint construction이다. \(h(4)u(4)^2\)는 magnitude sentinel일 뿐
\(J(-4)=\int_{-4}^4A_\lambda u^2+J(4)\)의 별도 numerical decomposition은
검사하지 않았다.

## 아직 끊긴 연결부

현재 결과에서 다음 결론으로 가는 논리적 연결은 모두 비어 있다.

1. nonzero-\(\lambda\)에서 declared minus-end \(\Gamma_1\) functional과
   reference-field boundary contribution; \(\lambda=0\) direction, \(h(4)\),
   direct smooth \(J(-4)\)와 endpoint-only \(h(-4)\)는 다섯 bracket에서 좁게 완료
2. 그 functional과 finite-\(Q_0\) proxy의 관계를 포함한 endpoint
   \(F\), declared \(F_\lambda\)와 root-velocity bound
3. \(\operatorname{Im}z>0\)에서 선택한 자기수반 extension의 resolvent와
   Weyl--Titchmarsh \(m(z)\)
4. \(m\)-함수의 경계값/Stieltjes 자료로부터 얻는 spectral measure,
   multiplicity와 support
5. 명시적 dense test space 위의 zero-fiber evaluation, rigging form의
   유한성·양성, null quotient와 observable action
6. 선택된 raw-\(C\) RAQ와 \(H=fC\)의 독립 domain/RAQ 사이 비교

Weyl \(m\)-함수는 단순히 실수축 characteristic root를 보간한 함수가 아니다.
선택한 자기수반 경계조건, 비실수 resolvent 해와 spectral transform을 함께
고정해야 한다. 이 순서의 operator-theoretic 기준선은 Eckhardt--Gesztesy--Nichols--Teschl,
[“Weyl-Titchmarsh Theory for Sturm-Liouville Operators with Distributional Potentials”](https://arxiv.org/abs/1208.4677)에
둔다. 이 논문이 현재 ICE fiber에 대한 결론을 대신한다는 뜻은 아니다.

## 다음 최소 인증 단위

가장 가까운 독립 질문은 “nonzero-\(\lambda\)에서 선언한 minus-end
\(\Gamma_1\) functional을 reference field와 같은 domain convention으로
정의하고, finite-\(Q_0\) proxy에 빠진 left-boundary contribution까지
outward-rounded enclosure로 검증할 수 있는가?”다. \(\lambda=0\) direct
Green endpoint는 이미 닫혔으며, generic normalized \(F_\lambda\)나 root
velocity를 이 boundary functional보다 먼저 선언하면 안 된다.

### 입력

- 현재 \(J(-4),h(-4)\) 결과의 input/result/runner hash와 다섯 certified ball
- \(\Gamma_{1,p}u=-\lim_{Q\to-\infty}W(u,c_p)\)의 selected reference field,
  normalization, maximal-domain convention과 measurable \(p\)-dependence
- nonzero-\(\lambda\)에서 \(Q_0\) 왼쪽까지 포함하는 boundary variation
  identity와 analytic/validated remainder
- plus-end direction 또는 amplitude normalization을 어디에 쓰는지의 명시적
  구분
- coefficient·rounding·minus-end truncation을 모두 포함하는 interval/ball
  arithmetic convention

### 반드시 검증할 것

- minus-end cutoff 제거 또는 analytic tail remainder와 outward rounding
- reference Wronskian boundary map의 normalization/extension dependence
- \(Q<Q_0\) left contribution을 누락한 finite-proxy 식을 fail-closed로 거부
- parameter subdivision과 precision 증가에 대한 enclosure overlap/refinement
- direct Green identity, boundary variation equation과 finite difference 대조를
  하되 finite difference를 인증 근거로 사용하지 않는 구분
- recessive direction만 고정한 상태에서 normalization-dependent
  \(F_\lambda\), eigenvalue slope 또는 root velocity를 출력하지 않는 guard

### 가능한 좁은 결과

- `CERTIFIED_NONZERO_LAMBDA_GAMMA1_VARIATION`: 선언한 extension과 실수 box에서
  minus-end boundary variation enclosure를 얻음
- `SUBDIVISION_REQUIRED`: 일부 parameter subbox만 인증됨
- `BOUNDARY_VARIATION_NOT_CERTIFIED`: minus-end remainder, domain dependence 또는
  precision budget 때문에 enclosure가 닫히지 않음

어느 결과도 자동으로 비실수 resolvent, spectral measure 또는 RAQ를 승인하지
않는다. real endpoint 인증 뒤에도 별도의 complex-\(z\) 계산에서 Herglotz/Nevanlinna
부호, conjugation symmetry, resolvent identity와 boundary-condition dependence를
검사해야 한다.

## 현재 구현 상태와 남은 선택지

`python-flint==0.9.0`과 그 Linux wheel hash는 이제 `pyproject.toml`과
`uv.lock`에 고정됐다. Arb complex-ball Bessel 평가를 사용한 \(\lambda=0\)
certificate도 같은 backend의 80/120-digit nesting과 0 배제 조건을 통과했다.
두 precision tier는 **같은 구현의 반복**이지 독립 backend 검산은 아니다.

\(\lambda=0\) endpoint의 남은 장애물은 일반 ball arithmetic이나 node
crossing이 아니다. exact Bessel Green route가 그 endpoint를 직접 닫았다.
현재 장애물은 nonzero-\(\lambda\) minus-end boundary functional이다.
python-flint의 special-function inclusion만으로 moving-domain boundary
variation과 \(Q\to-\infty\) remainder가 자동 인증되지는 않는다. 다음 구현은
둘 중 하나를 명시적으로 선택해야 한다.

- Arb 위에 minus-end reference pair와 boundary variation의 interval Taylor
  remainder를 좁은 parameter subbox용으로 직접 구성한다.
- CAPD::DynSys 또는 VNODE-LP 같은 validated ODE backend를 별도 도입하고,
  lock/source/version/rounding semantics와 작은 analytic anchor 회귀를 함께
  커밋한다.

두 경로 모두 이제 확보한 \(J(-4),h(-4)\) datum을 regression anchor로 쓸 수
있지만, 그 사실만으로 declared \(\Gamma_1\) derivative나
normalization-dependent amplitude가 인증되지는 않는다. 새 dependency, 대형
계산 또는 descendant 실행은 이 메모가 자동 승인하지 않는다.

## 이후 RAQ까지의 정확한 순서

```text
real plus-tail bound                    완료(현재 좁은 범위)
  -> lambda=0 exact Bessel transport    완료(실수 direction과 5 existence brackets)
    -> scale-invariant h tail datum     완료(lambda=0, 5 brackets의 h(4))
      -> direct smooth Green endpoint   완료(lambda=0, 5 brackets의 J(-4), endpoint h(-4))
        -> nonzero-lambda minus-end Gamma1 functional  오픈
          -> declared F_lambda/slope    오픈
      -> nonreal resolvent + Weyl m     오픈
        -> spectral measure/support     오픈
          -> test space + rigging form  오픈
            -> positivity/null quotient 오픈
              -> raw-C RAQ              오픈
                -> C versus H=fC        별도 비교
```

이 순서를 건너뛰고 실수축 root/Jacobian만으로 \(\delta(C)\), physical inner
product 또는 양자적 \(C\leftrightarrow H\) 동치를 선언하는 것은 현재 evidence의
범위를 넘는다.
