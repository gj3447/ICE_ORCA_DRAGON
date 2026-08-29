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

## 아직 끊긴 연결부

현재 결과에서 다음 결론으로 가는 논리적 연결은 모두 비어 있다.

1. nonzero-\(\lambda\)의 \(Q_+=4\to Q_0=-4\) 검증 transport와
   parameter-differentiated tail datum; \(\lambda=0\) direction은 exact Bessel로
   좁게 완료
2. 그 enclosure가 포함하는 endpoint \(F\)와 \(F_\lambda\)의 rigorous bound
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

가장 가까운 독립 질문은 “현재 tail theorem을 \(\lambda\)로 미분해
scale-invariant \(h=\partial_\lambda[-u'/u]\)의 \(Q_+=4\) datum 하나를
감쌀 수 있는가?”다. node-safe \([-4,4]\) 전달과 정규화된
\(F_\lambda\)는 그 다음의 별도 계산이다. 다음 계산을 열 경우 최소 입력과
출력은 다음처럼 고정한다.

### 입력

- 현재 결과의 input/result/runner hash와 \(Q_+=4\) tail error budget
- 선택한 real parameter box와 endpoint/boundary convention
- Riccati tail equation \(g'=g^2-A\)와 differentiated equation
  \(h'=2gh-A_\lambda\), 그리고 differentiated
  Volterra/Liouville--Green remainder
- 후속 amplitude 계산을 위한 plus-end \(\lambda\)-normalization 후보; 이
  계산은 normalization을 선택하지 않으면 \(h\)까지만 출력
- overflow를 피하기 위한 scaling/projective chart와 chart-switch rule
- coefficient·rounding·truncation을 모두 포함하는 interval/ball arithmetic
  convention

### 반드시 검증할 것

- 각 step의 local truncation remainder와 outward rounding
- Wronskian enclosure가 0을 배제하는지 여부
- step subdivision과 precision 증가에 대한 enclosure nesting
- chart pole 또는 turning-point 후보가 생기면 성공으로 숨기지 않는
  `UNRESOLVED_SUBBOX` 출력
- direct integration, variational equation, finite difference 사이의 대조를
  하되 finite difference를 인증 근거로 사용하지 않는 구분
- endpoint \(F,F_\lambda\)가 tail uncertainty와 transport uncertainty를 모두
  포함하는지에 대한 fail-closed check
- recessive direction만 고정한 상태에서 normalization-dependent
  \(F_\lambda\) amplitude를 출력하지 않는 guard

### 가능한 좁은 결과

- `CERTIFIED_REAL_ENDPOINT_BOX`: 선언한 실수 box에서 endpoint enclosure를
  얻음
- `SUBDIVISION_REQUIRED`: 일부 parameter subbox만 인증됨
- `TRANSPORT_NOT_CERTIFIED`: 폭발, pole, remainder 또는 precision budget 때문에
  enclosure가 닫히지 않음

어느 결과도 자동으로 비실수 resolvent, spectral measure 또는 RAQ를 승인하지
않는다. real endpoint 인증 뒤에도 별도의 complex-\(z\) 계산에서 Herglotz/Nevanlinna
부호, conjugation symmetry, resolvent identity와 boundary-condition dependence를
검사해야 한다.

## 현재 구현 상태와 남은 선택지

`python-flint==0.9.0`과 그 Linux wheel hash는 이제 `pyproject.toml`과
`uv.lock`에 고정됐다. Arb complex-ball Bessel 평가를 사용한 \(\lambda=0\)
certificate도 같은 backend의 80/120-digit nesting과 0 배제 조건을 통과했다.
두 precision tier는 **같은 구현의 반복**이지 독립 backend 검산은 아니다.

남은 장애물은 일반 ball arithmetic의 부재가 아니라 validated
parameter-dependent ODE다. python-flint의 special-function inclusion만으로
ODE truncation/wrapping과 chart switch가 자동 인증되지는 않는다. 다음 구현은
둘 중 하나를 명시적으로 선택해야 한다.

- Arb 위에 interval Taylor remainder와 Prüfer/projective chart 전환을 좁은
  parameter subbox용으로 직접 구성한다.
- CAPD::DynSys 또는 VNODE-LP 같은 validated ODE backend를 별도 도입하고,
  lock/source/version/rounding semantics와 작은 analytic anchor 회귀를 함께
  커밋한다.

어느 경로도 differentiated tail datum을 대신하지 않는다. 해당 datum을 먼저
해석적으로 봉입해야 한다. 새 dependency, 대형 계산 또는 descendant 실행은
이 메모가 자동 승인하지 않는다.

## 이후 RAQ까지의 정확한 순서

```text
real plus-tail bound                    완료(현재 좁은 범위)
  -> lambda=0 exact Bessel transport    완료(실수 direction과 5 existence brackets)
    -> scale-invariant h tail datum     오픈
      -> node-safe h transport          오픈
        -> normalized F_lambda          오픈
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
