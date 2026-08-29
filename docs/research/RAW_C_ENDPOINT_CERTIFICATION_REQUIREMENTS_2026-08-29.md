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
아니다. 이 해석은 [NIST DLMF §2.7(iii), 특히 2.7.23--2.7.25](https://dlmf.nist.gov/2.7.iii)의
오차와 미분 오차 조항에 한정된다.

즉, 무한대의 recessive 조건을 유한 \(Q_+=4\)의 초기 datum으로 바꿀 때
생기는 **실수축 plus-tail 오차 예산** 하나는 확보됐다. 두 \(p\) 부호가
같은 \(|p|=\sqrt{2/3}\,\kappa\) coefficient를 갖는다는 범위 밖의
\(p\)-mixing extension 결론은 아니다.

## 아직 끊긴 연결부

현재 결과에서 다음 결론으로 가는 논리적 연결은 모두 비어 있다.

1. \(Q_+=4\to Q_0=-4\)의 검증된 fundamental-matrix 또는 projective
   transport enclosure
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

가장 가까운 독립 질문은 “tail bound가 주는 초기 interval을
\([-4,4]\)에서 끝까지 전달해 endpoint datum과 그 \(\lambda\)-민감도를
동시에 감쌀 수 있는가?”다. 다음 계산을 열 경우 최소 입력과 출력은 다음처럼
고정한다.

### 입력

- 현재 결과의 input/result/runner hash와 \(Q_+=4\) tail error budget
- 선택한 real parameter box와 endpoint/boundary convention
- first-order system \(Y'=B(Q;\lambda,\kappa)Y\) 및
  \(\partial_\lambda Y\) variational system
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

## 현재 구현 장애와 선택지

잠금 파일을 감사한 결과, 직접 Python 의존성은 NumPy 2.5.2, SciPy 1.18.0,
SymPy 1.14.0이고 mpmath 1.3.0은 SymPy의 전이 의존성이다. `pyproject.toml`과
`uv.lock`에는 python-flint/Arb 또는 validated interval ODE backend가 없다.
따라서 기존 SciPy ODE의 작은 tolerance나 두 cutoff의 일치는 **rigorous
enclosure**로 승격할 수 없다.

다음 구현은 둘 중 하나를 명시적으로 선택해야 한다.

- 현재 잠금 안에서 rational/Taylor remainder와 directed bounds를 직접 구성해
  작은 subbox를 인증한다.
- 별도 dependency 변경으로 검증된 ball/interval backend를 도입하고 lock,
  source/version, rounding semantics와 독립 회귀 검사를 함께 커밋한다.

어느 선택도 아직 이루어지지 않았다. 패키지 설치, 대형 계산, descendant 실행은
이 메모가 자동 승인하지 않는다.

## 이후 RAQ까지의 정확한 순서

```text
real plus-tail bound                    완료(현재 좁은 범위)
  -> validated [-4,4] transport         오픈
    -> endpoint F/F_lambda enclosure    오픈
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
