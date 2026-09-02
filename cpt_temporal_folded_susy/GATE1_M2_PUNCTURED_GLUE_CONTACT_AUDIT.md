# Gate 1 frozen-$m=2$ punctured glue/contact audit

> **실행 상태:** `VALID_RUN`
> **계산 판정:** `SOURCE_UNDERDETERMINES_PUNCTURED_GLUE_AND_ZERO_LAPSE_EXTENSION`
> **인식론적 지위:** `SCOPED_INCONCLUSIVE_SUPPORTING_METHOD`
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 결론부터

현재 frozen-$A$, $m=2$ local source 기록은 음의 lapse arm의 접합과 $N=0$
접촉항을 유일하게 고르지 못한다. 이 감사가 계산한 것은 다음 두 개의 서로 다른
미결정성이다.

1. $C/|N|$와 $C/N$은 $N<0$에서 이미 부호가 반대다. 따라서
   $N=0$에 지지된 $c\delta(N)$를 아무리 더해도 두 punctured distribution을
   서로 바꿀 수 없다.
2. 두 punctured branch 가운데 하나를 먼저 고르더라도 scaling degree가
   $\omega=d=1$인 임계 경우이므로, **같은 scaling degree를 갖는 extension**은
   각각 하나의 $c\delta(N)$ 자유도를 남긴다.

그러므로 이 결과가 제거하는 것은 “현재 local flat-tangent source만으로 접합 부호와
zero-lapse contact가 둘 다 유일하게 정해진다”는 지름길뿐이다. 완전한 source-defined
joint relative cycle이 추가 자료로 이들을 선택할 가능성은 여전히 열려 있다. 새 물리,
물리적 contour, 절대 measure 또는 TOE를 발견한 결과가 아니다.

## 소비된 scalar one-shot과 다른 질문

과거 [`gate1_scalar_zero_lapse_extension.py`](gate1_scalar_zero_lapse_extension.py)는 full
Starobinsky $q$-paired holomorphic amplitude의 boundary와 scaling degree $1/2$를 묻다가
exact-check harness false negative로 소진되었다. 이번 runner는 그 계산이나 check를
재실행·복제하지 않는다.

이번 입력은 유효한
[`GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json`](GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json)
에서 이미 계산된 frozen-$A$ flat-tangent 식만 상속한다.

\[
C=\frac{\sqrt{\mu_g\mu_s}}{2\pi\hbar}
 =\frac{\sqrt6\,\pi A^2}{\hbar}>0,
\qquad
K_{\mathbb R}(N)=\frac{C}{|N|},
\qquad
K_{\rm sheet}(N)=\frac{C}{N}\quad(N\ne0).
\]

질문은 이 두 **이미 계산된 punctured kernel**의 차이가 point-supported contact인지,
그리고 scaling degree만으로 각 extension이 유일해지는지뿐이다.

## 정확한 분리

$N>0$에서는 두 kernel이 같지만 $N<0$에서는

\[
K_{\mathbb R}(N)-K_{\rm sheet}(N)=\frac{2C}{|N|}.
\]

$(-2,-1)$ 안에 지지된 nonnegative $C_c^\infty$ probe ψ를 택하면

\[
\langle K_{\mathbb R}-K_{\rm sheet},\psi\rangle
=2C\int_{-2}^{-1}\frac{\psi(N)}{|N|}\,dN>0,
\qquad
\langle c\delta,\psi\rangle=0.
\]

따라서 이는 contact ambiguity가 아니라 그보다 앞선 **discrete negative-arm glue**
문제다. benchmark $A=3.5668031935672753$, $ℏ=1$에서 $C=97.90024790286824$이고,
수치 pairing은 `80.20857954120878` (`pairing/C=0.8192888297973233`)였다.

## branch를 고른 뒤의 contact family

이 감사는 다음 convention을 명시적으로 쓴다.

\[
\left\langle \operatorname{Pf}_{\mu}\frac1{|N|},\varphi\right\rangle
=\lim_{\epsilon\downarrow0}
\left[
\int_{|N|>\epsilon}\frac{\varphi(N)}{|N|}\,dN
+2\varphi(0)\log(\mu\epsilon)
\right].
\]

그러면

\[
\operatorname{Pf}_{\mu'}\frac{C}{|N|}
-\operatorname{Pf}_{\mu}\frac{C}{|N|}
=2C\log\frac{\mu'}{\mu}\,\delta(N).
\]

따라서 같은 scaling degree를 유지하는 두 family는

\[
\operatorname{Pf}_{\mu}\frac{C}{|N|}+c\delta(N),
\qquad
\operatorname{PV}\frac{C}{N}+c\delta(N)
\]

이다. $\mu=1/2,1,2,4$의 독립 compact-bump quadrature는 위 scale shift를 최대
`2.220446049250313e-16` 잔차로 재현했다. 직접 cutoff 식도 subtracted finite part로
`1.1111142e-5 → 6.9444456e-7 → 4.3402779e-8` 순서로 수렴했다.

“same-scaling-degree”는 “추가 조건 아래 유일”과 다르다. 예를 들어 signed branch에
oddness와 exact homogeneous scaling을 별도로 요구하면 $\operatorname{PV}(1/N)$이
구별될 수 있다. 그러나 그런 조건은 현재 local source에서 유도되지 않았으며, even
$1/|N|$ finite part에는 logarithmic scale anomaly가 남는다.

## lateral 처방이 하는 일과 하지 않는 일

선택된 signed branch에서는

\[
\frac1{N-i0}=\operatorname{PV}\frac1N+i\pi\delta(N),
\qquad
\frac1{N+i0}=\operatorname{PV}\frac1N-i\pi\delta(N).
\]

Gaussian probe의 Poisson-kernel quadrature는 ε를 `0.2, 0.05, 0.01, 0.002`로 줄일 때
lower pairing을 `2.54161, 2.97192, 3.10646, 3.13452`로 얻어 $+π$에 수렴했고,
upper pairing은 정확히 반대 부호였다. analytic formula와의 최대 quadrature 잔차는
`3.1086244689504383e-15`였다.

이 처방은 **signed $C/N$ glue를 이미 선택한 뒤** contact coefficient를 고른다. 그것이
real $C/|N|$에서 signed negative arm을 유도하는 것은 아니다. Banihashemi–Jacobson의
below-origin contour도 그 논문의 integration order와 constraint convention 안에서 재사용하는
comparator이지, 이 workbench의 joint determinant orientation이나 physical original cycle을
가져오는 근거가 아니다.

## 실행과 검산

정본 실행:

```text
./ice run gate1_m2_punctured_glue_contact_audit
```

관측 출력:

```text
run_status=VALID_RUN
verdict=SOURCE_UNDERDETERMINES_PUNCTURED_GLUE_AND_ZERO_LAPSE_EXTENSION
exact=7/7 PASS
numerical=4/4 PASS
theorem_guards=3/3 VERIFIED
quadratures=16
sampling_points=12
automatic_next=null
```

| 항목 | 값 |
| --- | --- |
| input SHA-256 | `627340c5d861f940b2ada36809c917f6c090ae2d8c970c578fd49ef67d5cd55f` |
| upstream result SHA-256 | `f7d64a09eeb4132e4975b056ee76eedfa32b75c7d29ca1a78bede5b052a66bc6` |
| runner SHA-256 | `f4d21da8cce590233e84748e5d57f944e486144807c294c3911539f049c42c8d` |
| result SHA-256 | `52a63f1fc686d003501d961b566562fac157af8fbd79f43e35de5da549491a8a` |
| payload digest | `255520fc4694ef9f12f8df5b3f09c722228270fb0d2d39bcde31bcbb3e246a5e` |
| result bytes | `13,229` |
| environment | Python 3.13.5, SymPy 1.14.0, SciPy 1.18.0 |

runner와 input은 commit `9276d32520a33d3106c56edf648b1f79b0c3566c`에서 먼저 고정했다.
첫 clean 실행은 결과를 쓰기 전에 shifted-list `zip(strict=True)` harness 오류로 끝났고,
수학 조건이나 threshold를 바꾸지 않은 한 줄 수정은
`6e73c4d7d0e52abfeab6709fa07056db4fc7f366`에 기록했다. 그 뒤 위 정본 명령이 exit 0으로
끝났다. 독립 read-only 감사가 Python canonical payload digest, 모든 check 수, scale-shift
부호와 계수, cutoff 수렴, lateral 부호, negative-support 분리를 재계산해 통과시켰다.

## 남아 있는 물리 경계

다음 출력은 전부 `null` 또는 `OPEN`이다.

- source-defined/physical joint relative cycle과 source-to-thimble deformation
- full joint orientation과 absolute determinant/Pfaffian line
- complete global signed intersection vector와 $n_\sigma$
- nonreal singular Weyl $m(z)$, spectral measure와 transform
- rigging map, physical product와 RAQ completion
- physics claim, empirical discriminator와 TOE claim

특히 이 lapse contact 감사는 fixed-$p$ 비실수 endpoint ratio
$M=-\Gamma_1/\Gamma_0$, Herglotz identity, Stieltjes inversion, measurable $p$-field 또는
rigging product를 하나도 공급하지 않는다. 따라서 실근 결과를 Weyl 함수로 부르는 오류와
마찬가지로, 이 결과를 $m(z)$, spectral measure 또는 RAQ로 승격하면 안 된다.

## 1차 문헌

- Brunetti–Fredenhagen, [*Microlocal Analysis and Interacting Quantum Field Theories*](https://arxiv.org/abs/math-ph/9903028), 특히 scaling degree $\omega\ge d$ extension 정리.
- Dang, [*Extension of distributions, scalings and renormalization of QFT on Riemannian manifolds*](https://arxiv.org/abs/1411.3670), Hadamard finite part와 singular-set-supported extension 차이.
- Banihashemi–Jacobson, [*On the lapse contour in the gravitational path integral*](https://arxiv.org/abs/2405.10307v3), momentum-first below-origin contour comparator.

정본 machine ledger는
[`GATE1_M2_PUNCTURED_GLUE_CONTACT_AUDIT_RESULT.json`](GATE1_M2_PUNCTURED_GLUE_CONTACT_AUDIT_RESULT.json)이다.
