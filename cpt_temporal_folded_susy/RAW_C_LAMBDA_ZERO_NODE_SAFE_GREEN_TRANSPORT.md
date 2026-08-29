# Raw-C lambda-zero node-safe Green endpoint certificate

## 좁은 질문과 답

정확히 \(\lambda=0\)이고, 앞선 modified-Bessel 계산이 고정한 다섯
\(\kappa\) bracket 전체에서 다음 질문에는 이제 **예**라고 답할 수 있다.

> Riccati 변수 \(h=\partial_\lambda(-u_Q/u)\)를 solution node 사이로 직접
> 전개하지 않고도 \(Q_0=-4\)의 매끈한 differentiated Wronskian과 endpoint
> \(h\)를 엄밀한 ball로 구성할 수 있는가?

사용한 매끈한 변수는

\[
J(Q;\kappa)=-W_Q(u,\partial_\lambda u)=u(Q)^2h(Q;\kappa)
\]

이다. 실행 결과는 exact 7/7, Arb-ball 61/61, theorem/scope guard 6개,
다섯 bracket 5/5 인증과 격리 재현 `REPRO`다.

이 결과는 \(Q=4\)의 기존 \(h(4)\) datum을 상태벡터로 수치 전파한 것이
아니다. exact Bessel Green 적분으로 \(J(-4)\)를 직접 구성한 endpoint
certificate다.

## pole을 피하는 항등식

선언한 fiber 방정식과 forcing은

\[
u_{QQ}=A u,
\qquad
A=36\pi^4e^{2Q}+6\pi^2\lambda e^{3Q/2}-\kappa^2,
\qquad
A_\lambda=6\pi^2e^{3Q/2}
\]

이다. \(v=\partial_\lambda u|_{\lambda=0}\)라 두면

\[
v_{QQ}=A_0v+A_\lambda u,
\qquad
W(u,v)_Q=A_\lambda u^2.
\]

따라서

\[
J=-W(u,v)=u^2h,
\qquad
J_Q=-A_\lambda u^2,
\qquad
J(Q)=\int_Q^\infty A_\lambda(s)u(s)^2\,ds>0.
\]

\(u=0\)이면 \(h=J/u^2\)는 정의되지 않거나 pole을 가질 수 있지만,
Wronskian \(J\)는 그대로 매끈하다. 이번 runner는 열린 구간에서 \(h\)를
한 번도 나누거나 전개하지 않는다. \(Q_0\)에서만 전체 bracket의
\(u(Q_0)\ne0\)를 먼저 인증한 뒤 \(h(Q_0)=J(Q_0)/u(Q_0)^2\)를 만든다.

정확히 \(\lambda=0\)에서는

\[
C=6\pi^2,
\qquad x=Ce^Q,
\qquad u(Q;\kappa)=K_{i\kappa}(x),
\]

이므로

\[
J(Q_0;\kappa)
=\frac{1}{\sqrt C}
\int_{x_0}^{\infty}\sqrt{x}\,K_{i\kappa}(x)^2\,dx,
\qquad x_0=Ce^{-4}.
\]

이 식이 node를 지나가는 direct Green endpoint construction이다.

## rigorous finite quadrature와 analytic tail

finite part는 다음 여섯 positive-real subsegment로 고정했다.

\[
[x_0,1.5],\ [1.5,2],\ [2,4],\ [4,8],\ [8,16],\ [16,32].
\]

각 exact-rational \(\kappa\) bracket 전체를 하나의 Arb parameter ball로
넣어 `python-flint==0.9.0`의 finite `acb.integral` enclosure를 더했다.
80/120 decimal-digit 두 tier는 같은 backend의 refinement이지 독립 구현이
아니다. 60번의 finite quadrature에서 callback 14,216회와 Bessel 평가
14,236회를 사용했고 ODE, root solve, finite difference는 0회다.

[DLMF 10.32.9](https://dlmf.nist.gov/10.32.E9)의 integral representation과
\(|\cos(\kappa t)|\le1\), \(\cosh t\ge1+t^2/2\)로

\[
|K_{i\kappa}(x)|
\le e^{-x}\sqrt{\frac{\pi}{2x}}
\]

를 얻는다. 따라서 수치 적분을 무한구간으로 호출하지 않고

\[
0\le
\frac1{\sqrt C}\int_X^\infty\sqrt{x}K_{i\kappa}(x)^2\,dx
\le \frac{\pi e^{-2X}}{4\sqrt{CX}},
\qquad X=32,
\]

를 별도로 더했다. 관측된 tail upper bound는 모든 tier에서
\(2.894\times10^{-30}\)보다 작다. finite straight-line integral과 수동
improper-tail 분리는 [FLINT integration 문서](https://flintlib.org/doc/acb_calc.html)의
계약을 따른다. Arb의 midpoint-radius inclusion 의미는
[Johansson (2017)](https://arxiv.org/abs/1611.02831)에 둔다.

## 관측된 endpoint certificate

아래 값은 midpoint 샘플이 아니라 각 inherited bracket **전체**의
outward-rounded intersection이다.

| root bracket | certified \(J(-4)\) | certified \(h(-4)=J/K_{i\kappa}(x_0)^2\) |
|---:|---:|---:|
| 1 | \([8.6743397336076293551261172458\!\times10^{-4},\ 8.6743397336076293551261674594\!\times10^{-4}]\) | \([0.1428500395337029935245653093,\ 0.1428500395337029935245661363]\) |
| 2 | \([3.7674235167675853593046306432\!\times10^{-6},\ 3.7674235167675853593049496752\!\times10^{-6}]\) | \([0.5356890492103620097315588890,\ 0.5356890492103620097316042528]\) |
| 3 | \([4.5216349131610544509851782792\!\times10^{-8},\ 4.5216349131610544509857113157\!\times10^{-8}]\) | \([0.9097203282712884098095777421,\ 0.9097203282712884098096849868]\) |
| 4 | \([8.4506491205391687382938311821\!\times10^{-10},\ 8.4506491205391687383249885642\!\times10^{-10}]\) | \([1.2870710317325033289980484235,\ 1.2870710317325033290027939023]\) |
| 5 | \([2.0702793087478715852856238366\!\times10^{-11},\ 2.0702793087478715855805009295\!\times10^{-11}]\) | \([1.6705600981682216906715754491,\ 1.6705600981682216909095227750]\) |

모든 lower bound가 0보다 크다. 따라서 고정한 \(\lambda=0\), 다섯
bracket scope에서는 smooth \(J(-4)>0\)와 endpoint-only \(h(-4)>0\)가
인증됐다.

## 실패를 숨기지 않은 수치 경로

첫 clean run은 \([x_0,64]\) 하나의 긴 finite integral을 사용했다. exact
항등식과 모든 endpoint 부호는 유지됐지만 일부 bracket에서 사전 선언한
width/refinement gate를 닫지 못해
`LAMBDA_ZERO_NODE_SAFE_GREEN_WRONSKIAN_ENDPOINT_CONSTRUCTION_NOT_CERTIFIED`로
기록했다. 그 결과는 commit `b10da50`의 역사에 남아 있다. 이는 방정식의
반례가 아니라 enclosure geometry의 실패다.

후속 source는 같은 질문과 같은 Green 항등식을 여섯 고정 subsegment와
\(x\ge32\) analytic tail로 재구성했다. 성공 verdict는 실패를 삭제하거나
물리적 반증으로 재해석해서 얻은 것이 아니다.

## 선언된 경계조건과 섞으면 안 되는 것

finite proxy를 \(F_0(\kappa)=u_Q(Q_0;\kappa)\)라 쓰면 그 root에서만

\[
\frac{\partial_\lambda F_0}{u(Q_0)}=-h(Q_0)
\]

라는 endpoint Wronskian 식이 성립한다. 그러나 저장소가 선언한 raw-\(C\)
extension 경계는 finite Neumann 값이 아니라 minus-end functional

\[
\Gamma_{1,p}u=-\lim_{Q\to-\infty}W(u,c_p)
\]

이다. \(\lambda=0\)에서는 reference equation 때문에 우연히
\(\Gamma_1=u_Q(Q_0)\)로 환원되지만, \(\lambda\ne0\)에서는

\[
\Gamma_1(u)=u_Q(Q_0)
-\lambda\int_{-\infty}^{Q_0}A_\lambda(Q)u(Q)c_p(Q)\,dQ
\]

의 left-boundary contribution이 생긴다. 그러므로 이번 \(h(-4)\)를
declared-extension \(F_\lambda\), eigenvalue slope 또는 root velocity로
부를 수 없다.

또한 기존 \(h(4)u(4)^2\)는 positive magnitude sentinel로만 검사했다.
\(J(-4)=\int_{-4}^{4}A_\lambda u^2+J(4)\)를 별도로 수치 분해해 overlap한
것이 아니므로 “\(h(4)\) 상태를 전파했다”고 쓰지 않는다.

## 다음 실제 연결부와 explicit nulls

P1의 다음 핵심 장애물은 nonzero-\(\lambda\)에서 minus-end
\(\Gamma_1\) functional과 reference-field contribution을 같은 domain
convention으로 정의하고 검증하는 것이다. 그 뒤에만 finite-\(Q_0\) proxy
derivative와 declared extension derivative의 관계를 물을 수 있다.

다음은 계속 명시적 null이다.

- raw \(h\)의 interior-node trajectory와 nonzero-\(\lambda\) transport;
- endpoint \(F_\lambda\) amplitude, declared \(\Gamma_1\) derivative,
  eigenvalue slope와 root velocity;
- 각 bracket root의 uniqueness와 전체 root census completeness;
- nonreal resolvent, Weyl \(m\), spectral measure, rigging test space/map,
  physical inner product와 raw-\(C\) RAQ;
- \(C\leftrightarrow H=fC\) 양자동치, BFV, 관측 likelihood;
- 물리학, 양자중력 또는 TOE 주장.

## 실행·재현·provenance

```text
./ice run raw_c_lambda_zero_node_safe_green_transport
./ice repro --only raw_c_lambda_zero_node_safe_green_transport
npm run check
```

- final runner commit: `8bbb7bd`;
- certified result commit: `7e52ba9`;
- input SHA-256:
  `005a47aab13238f6b7bf0c5a67fb1218d739e7839dfdc99cadd9ebdb74bb4346`;
- runner SHA-256:
  `a056cdbdf23424d017afe2a445d4ea0f4f6f4f4a90e0814a922cf5d49f1b4717`;
- result-file SHA-256:
  `e0d53cb50d8ad5bfb7afca67a7c5223d4ac4d2fdebf8718833acc58c2eee304b`;
- canonical result payload SHA-256, excluding its self field:
  `9667d2ff56b0dfc41bfeb4d24e4c09ab2ba77ee4439906a5a8743bd5e0f43c4f`.

격리 재현은 `REPRO 1`, needs-attention 0이고 `npm run check`는 68/68
test pass다. 이 검사는 계산과 제어면의 재현성을 말할 뿐 물리적 승격을
뜻하지 않는다.
