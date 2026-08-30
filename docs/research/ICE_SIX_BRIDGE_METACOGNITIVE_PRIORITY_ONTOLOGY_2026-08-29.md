# ICE 여섯 연결부 메타인지 우선순위 온톨로지

> 기준일: 2026-08-29; 2026-08-30 scoped update 포함
> 지위: repository-local 계산 워크벤치의 의사결정·기억 지도. 물리학 이론,
> 양자중력 완성, 외부 KG ratification 또는 TOE 주장이 아니다.

## 0. 여기서 “완전한 메타인지”가 뜻하는 것

이 문서는 현 프로그램에 대해 다음 질문을 빠짐없이 답할 수 있다는 제한된
의미에서 **decision-complete**다.

1. 무엇을 실제로 계산했는가?
2. 어느 방정식·가정·scope에서만 성립하는가?
3. 무엇은 문헌에서 가져온 theorem/method이고, 무엇은 repository evidence인가?
4. 어떤 반례·실패 출력이면 현재 경로를 멈추거나 바꿔야 하는가?
5. 다음 계산이 성공해야만 어느 후속 주장이 열리는가?
6. 여전히 명시적 `null`인 결론은 무엇인가?

문헌 전체를 망라했다거나 프로그램을 물리적으로 완성했다는 뜻은 아니다.
메타인지 층은 다음 일곱 종류를 섞지 않는다.

| 층 | 의미 | KG 표현 |
|---|---|---|
| 계산 사실 | committed runner의 실제 출력 | `claim` + `HAS_EVIDENCE` |
| theorem transfer | 출처의 정리와 검증한 가정 | `CITES`; 계산 evidence가 아님 |
| 방법 후보 | 다음 장애물을 풀 수 있는 알고리즘 | `open_problem` + `CITES` |
| 해석 | 계산 사실이 허용하는 좁은 의미 | concept/document summary |
| 미해결 | 필요한 산출물이 없음 | `open_problem` |
| 차단 | 선행 입력이 없어 지금 결론을 낼 수 없음 | `BLOCKED_BY` |
| 금지된 승격 | 물리·양자중력·TOE 또는 자동 후속 | explicit null / policy |

모든 우선순위는 사람이 고른 연구 순서일 뿐 실행 권한이 아니다. 한 계산의
성공·실패가 다음 계산을 자동 생성하지 않는다.

## 1. 우선순위 결론

현재 가장 빠른 1순위는 raw-\(C\)의 **actual nonzero-\(\lambda\)
sharp Riccati chart에서 전역 nonlinear remainder를 panelwise하게 좁히고
validated \(\lambda\)-sensitivity로 sign separation 가능성을 시험하는 것**이다.
scale-invariant differentiated plus-tail datum과 direct smooth Green endpoint는
정확히 \(\lambda=0\), 다섯 root bracket에서 좁게 완료됐고, 2026-08-30에는
선언한 fixed-reference \(\Gamma_1\) identity의 left correction 및 zero-shell
derivative도 좁게 닫혔다. 이어 actual direction과 fixed \(1/4\) width gate도
root bracket 1에서 닫혔지만 모든 endpoint interval은 아직 0을 포함한다. 이유는
다음과 같다.

- 이미 선언해 둔 candidate self-adjoint boundary line, coarse root, finite-cutoff
  \(F_\lambda\) 대조와 real plus-tail bound가 있다.
- \(\lambda=0\)에는 exact modified-Bessel 해가 있어 무한대에서
  \(Q_0=-4\)까지의 한 축을 수치 ODE 없이 닫을 수 있다.
- 이 연결은 real-axis endpoint와 local Jacobian route를 인증한다. nonreal Weyl
  \(m\) construction은 선택한 extension에서 독립적으로 착수 가능하고, 두
  경로는 spectral/RAQ 단계에서 교차검사되어야 한다.
- 실패해도 어느 node/chart/tail assumption에서 막혔는지 좁게 남길 수 있다.

운영 우선순위는 아래와 같다. 원래 여섯 연결부에서 closed-\(S^3\)의
“cubic construction”과 “HDA/Jacobi 판정”을 서로 다른 인식 단계로 분리했기
때문에 일곱 행이다.

| 순위 | 목표 | 현재 상태 | 성공 게이트 | 실패·반증 출력 | 후속 연결 |
|---:|---|---|---|---|---|
| P1 | raw-\(C\) actual nonzero-\(\lambda\) plus-recessive solution과 minus-end \(\Gamma_1\) remainder | **sharp-direction/width 부분 돌파**: exact backward-\(x\) variation-of-constants와 global \(0\le J_{\rho^2}\le J_0\) bound가 actual \(Q=4\to Q_s\) direction을 좁게 봉입했고 six scale-free width는 \(0.06370\)–\(0.06378<1/4\) | global nonlinear box의 panelwise Picard/affine refinement와 validated \(\lambda\)-sensitivity/sign separation; 0을 피할 때에만 continuation을 별도 검토 | sensitivity/sign separation 실패, domain/reference/normalization drift, tier 비중첩 | P4 |
| P2 | full \(S^3\) SVT/Gaunt와 ADM cubic coefficient | 독립 착수 가능; restricted zonal subvertices, fixed-background matter \(HH\), 그리고 scalar linear ADM momentum generator까지 있음 | scalar/vector/TT와 gravity·lapse/shift·matter를 같은 convention으로 cubic까지 구성 | basis/convention 불일치, transverse shift 누락, cutoff tail 미측정 | P3 |
| P3 | 고전 HDA/Jacobi와 cutoff remainder 분리 | **scoped 부분 돌파**: zonal fixed-background matter \(HH\)에서 \(L=2\) omitted \(k=3\) remainder와 \(L=3,4\) 복구를 exact 분리 | full gravity+matter constraint의 \(DD,DH,HH\), Jacobiator, \(L\) scaling 및 analytic remainder | 유한 cutoff defect를 continuum anomaly로 오인하지 않는 `UNCLASSIFIED_REMAINDER` | P5 |
| P4 | nonreal Weyl \(m\), spectral measure, raw-\(C\) RAQ와 \(C/H\) 비교 | 독립 method 착수 가능; real-axis 일치는 P1과 만남 | self-adjoint domain·measurable \(p\)-family·test space·positive rigging form·observable intertwining | Herglotz 부호/positivity/domain map 실패 또는 extension dependence | equivalence 판정 및 raw-\(C\) representation을 쓸 경우 P5 |
| P5 | 고전 BFV charge와 quantum nilpotency/anomaly | 고전 charge는 P3에 의존; raw-\(C\) physical core 적용은 P4도 필요 | 실제 structure functions와 common invariant core에서 \(\Omega^2\) defect 분해 | ordering/domain/regulator/truncation defect를 구분해 기록 | P7 |
| P6 | contour·Gribov·determinant line·gluing을 포함한 absolute BFV | 방법 연구는 병렬, gravity 적용은 P3/P5와 만남 | boundary QME, gauge coverage, absolute orientation, regulator removal과 gluing | contour/Gribov/gluing/line orientation 중 실패 위치를 분리 | P7 |
| P7 | 두 clock relational observable → BO/decoherence → \(V\ne0\) CLASS/Cobaya likelihood | downstream | 동일 physical product의 clock 비교, primordial spectra, pinned likelihood | clock chart/inner-product/initial-state/reheating 부재면 likelihood 금지 | 관측 비교 |

의존성은 다음과 같다.

```text
P1 declared-boundary derivative ───┐
                                    ├─► spectral/RAQ cross-check
P4 nonreal m / raw-C RAQ ──────────┘                    ───────┐
                                                              ├─► P5 quantum BFV* ─┐
P2 full S3 ADM cubic ──────────► P3 HDA/Jacobi ───────────────┘                   │
                                                                                 ├─► P7 clocks/BO/likelihood
P6 boundary/absolute-BFV method lane ──(gravity application meets P3/P5)────────┘
```

P2와 P6의 방법 연구는 P1과 병렬로 시작할 수 있다. 이는 자동 실행 순서가
아니며, P1 결과 하나가 그 작업을 승인하지 않는다. `*` 고전 BFV charge는
P3만으로 시작할 수 있고, P4 의존성은 raw-\(C\) physical Hilbert/core를 quantum
BFV representation에 사용할 때 생긴다.

## 2. P1에서 이번에 실제로 돌파한 것

정확히 \(\lambda=0\)에서

\[
x=6\pi^2e^Q,
\qquad
x^2u_{xx}+xu_x-(x^2-\kappa^2)u=0,
\]

이므로 recessive direction은

\[
u_+(Q;\kappa)=K_{i\kappa}(x)
\]

이다. endpoint characteristic는

\[
F(\kappa)=\partial_Qu_+(-4;\kappa)
=-\frac{x_0}{2}
\left[K_{i\kappa-1}(x_0)+K_{i\kappa+1}(x_0)\right].
\]

`raw_c_lambda_zero_bessel_ball_transport`의 clean bounded run은 다음을
관측했다.

- exact identity 4/4, Arb ball check 35/35, theorem/scope guard 5개;
- 다섯 개의 서로 겹치지 않는 sign-changing interval에 각각 적어도 한 개의
  실근 존재;
- 각 120-digit rational bracket 폭
  \(1/20282409603651670423947251286016\approx4.93\times10^{-32}\);
- 모든 bracket band에서 \(K_{i\kappa}(x_0)\ne0\);
- \(W_Q(K_{i\kappa},I_{i\kappa})\) ball이 1을 포함하고 0을 배제;
- \(Q=4\) exact Bessel/WKB normalized difference 최대
  \(1.195463\times10^{-8}\), exact rational envelope에서 재구성한
  tail budget \(9.449555\times10^{-5}\) 안에 포함;
- ODE, root solver, quadrature 호출 0; ball Bessel evaluation 1,685/5,000;
- 격리 재현 `REPRO`, needs-attention 0.

[DLMF modified-Bessel identities](https://dlmf.nist.gov/10)와
[Arb midpoint-radius arithmetic](https://arxiv.org/abs/1611.02831)은 각각
theorem/convention과 inclusion arithmetic의 1차 출처다. 실수성은 단순히
허수 ball이 0을 포함한다는 사실로 주장하지 않고
\(K_{-\nu}=K_\nu\)와 conjugation을 함께 사용했다.

### 해결된 것과 해결되지 않은 것

| 판정 | 내용 |
|---|---|
| `CLOSED_NARROW` | \(\lambda=0\) real recessive direction의 exact \(+\infty\to Q_0\) 표현 |
| `CLOSED_NARROW` | 선언한 다섯 bracket 각각의 실수 sign-changing root 존재 |
| `CLOSED_NARROW` | 같은 다섯 bracket 전체에서 scale-invariant \(h(4)=\partial_\lambda[-u'/u]_{\lambda=0}\) outward enclosure |
| `CLOSED_NARROW` | 같은 다섯 bracket 전체에서 direct smooth \(J(-4)=-W(u,\partial_\lambda u)>0\)와 endpoint-only \(h(-4)>0\) outward enclosure |
| `OPEN` | 각 bracket의 root uniqueness와 \([0,8]\) 전체 census completeness |
| `PARTIAL_P1` | nonzero-\(\lambda\) minus-end \(\Gamma_1/v(-4)\) outer functional과 reference tail은 finite하게 닫혔으나 sharp width/sign은 미완 |
| `OPEN_P1` | 위 functional을 닫은 뒤의 declared endpoint \(F_\lambda\), eigenvalue slope 또는 root velocity |
| `OPEN_P4` | nonreal Weyl \(m\), spectral measure, test space, rigging map, RAQ |
| `NULL` | raw-\(C\)/selected-\(H\) quantum equivalence, physics, quantum gravity, TOE |

### 이번에 닫힌 scale-invariant tail datum

\(v=\partial_\lambda u|_{\lambda=0}\)는, 먼저 \(\lambda\)-의존
normalization을 고정했을 때,

\[
v''-A_0v=A_\lambda u,
\quad
A_0=36\pi^4e^{2Q}-\kappa^2,
\quad
A_\lambda=6\pi^2e^{3Q/2}
\]

를 만족한다. recessive **direction**만으로는 일반 \(F_\lambda\)의 크기가
정의되지 않는다. \(u_\lambda\mapsto c(\lambda)u_\lambda\)이면
\(v\mapsto c(0)v+c'(0)u\)이기 때문이다. 따라서 amplitude를 쓸 경우
예를 들어 \(u_\lambda/w_\lambda\to1\) 같은 plus-end normalization과
\(w_\lambda\)의 action 기준점을 먼저 고정해야 한다.

amplitude보다 scale-invariant인

\[
g=-u'/u,\qquad h=\partial_\lambda g,
\qquad h'=2gh-A_\lambda
\]

에 대해 plus-end 조건은 \(h(\infty)=0\)이 아니라
\(u(Q)^2h(Q)\to0\)이다. 따라서 정확히 \(\lambda=0\)에서

\[
h(Q)=u(Q)^{-2}\int_Q^\infty A_\lambda(s)u(s)^2\,ds>0.
\]

\(C=6\pi^2\), \(x=Ce^Q\), \(u=K_{i\kappa}(x)\)를 쓰면

\[
h(4;\kappa)=\frac{1}{\sqrt C\,K_{i\kappa}(x_+)^2}
\int_{x_+}^{\infty}\sqrt{x}\,K_{i\kappa}(x)^2\,dx.
\]

`raw_c_lambda_zero_differentiated_plus_tail`은 이 항등식, rigorous finite
`acb.integral`, DLMF 10.32.9에서 따온 별도 analytic tail bound를 결합했다.
clean bounded run에서 exact 9/9, Arb-ball 70/70, theorem/scope guard 6개가
통과했다. 다섯 root bracket 전체에서 \(h(4)\)는

\[
3.6942432085987834 < h(4;\kappa)
< 3.6942535712156082
\]

안에 있고, 개별 enclosure 폭은 \(3.34\times10^{-26}\)에서
\(4.62\times10^{-26}\), analytic tail upper bound는 모두
\(6.02\times10^{-28}\)보다 작다. 80/120-digit 결과는 같은 backend의
precision refinement이지 독립 구현이 아니다. 격리 재현은 `REPRO`,
needs-attention 0이다.

### 이번에 추가로 닫힌 direct node-safe Green endpoint

\(J=-W(u,\partial_\lambda u)=u^2h\)는 \(u\)의 node에서도 매끈하고
\(J_Q=-A_\lambda u^2\)를 만족한다. 따라서 \(h\)를 node 사이로 나누어
전개하지 않고

\[
J(-4;\kappa)=\frac1{\sqrt{6\pi^2}}
\int_{6\pi^2e^{-4}}^\infty\sqrt{x}\,K_{i\kappa}(x)^2\,dx
\]

를 직접 ball-certify할 수 있다. `raw_c_lambda_zero_node_safe_green_transport`의
clean bounded run은 exact 7/7, Arb-ball 61/61, guard 6개, 다섯 bracket
5/5와 격리 `REPRO`를 통과했다. bracket 전체의 endpoint \(h(-4)\)는 각각

\[
0.1428500395,\quad0.5356890492,\quad0.9097203283,\quad
1.2870710317,\quad1.6705600982
\]

부근의 엄밀한 positive interval이다. 처음의 single-segment quadrature는
width gate를 닫지 못해 `NOT_CERTIFIED`로 보존했고, 같은 항등식을 여섯 fixed
subsegment와 \(x\ge32\) analytic tail로 재구성한 뒤 성공했다.

이것은 기존 \(h(4)\) datum의 numerical propagation이 아니라 direct exact
Green-integral endpoint construction이다. \(h(4)u(4)^2\)는 magnitude
sentinel이며 별도 \(Q=4\to-4\) decomposition equality는 계산하지 않았다.

### 선택적 explicit compact decomposition route (현재 primary blocker 아님)

lambda-zero endpoint 값 자체는 위 direct Green route로 닫혔다. 아래의
Prüfer/projective atlas는 \(h(4)\) datum을 실제 compact state/flux로 분해해
전파하는 독립적인 cross-check가 필요할 때 쓸 수 있지만, 현재 P1의 primary
blocker는 아니다. 한 가능한 chart는

\[
u=\rho\sin\theta,\qquad u'=\rho\cos\theta,
\]

\[
\theta'=\cos^2\theta-A\sin^2\theta,
\qquad
(\log\rho)'=(1+A)\sin\theta\cos\theta.
\]

\(\phi=\partial_\lambda\theta\),
\(\zeta=\partial_\lambda\log\rho\)에 대해서는

\[
\phi'=-2(1+A)\sin\theta\cos\theta\,\phi-A_\lambda\sin^2\theta,
\]

\[
\zeta'=A_\lambda\sin\theta\cos\theta
 +(1+A)\cos(2\theta)\phi.
\]

여기서 \(\theta\)는 node를 지나 연속적으로 올린 unwrapped lift여야 한다.
실제 root family에는 node가 있으므로 한 개의 Riccati chart
\(u'/u\)만으로 \([-4,4]\) 전체를 인증하면 안 된다. 구현 후보는
[CAPD::DynSys](https://arxiv.org/abs/2010.07097)와
[VNODE-LP](https://vericomp.fiw.hs-wismar.de/solvers/view/VNODE-LP)이고,
특이 Sturm--Liouville 문제에서 interval ODE와 oscillation theory를 결합해
보증 eigenvalue bound를 만든 선례는
[Brown--McCormack--Marletta](https://onlinelibrary.wiley.com/doi/10.1002/%28SICI%291522-2616%28200005%29213%3A1%3C17%3A%3AAID-MANA17%3E3.0.CO%3B2-R)다.
이 문헌들은 현재 fiber의 \(F_\lambda\)를 대신 계산하지 않는다.

이 선택적 compact-decomposition cross-check의 fail-closed 조건은 다음과 같다.

- 입력 \(h(4)\) ball 또는 local ODE remainder를 누락함;
- plus-end normalization을 선언하지 않은 채 amplitude \(F_\lambda\)를 출력함;
- interval chart의 denominator가 0을 포함하고 안전한 chart 전환도 없음;
- refinement/precision 증가 시 enclosure가 중첩하지 않음;
- Wronskian lower bound가 0을 배제하지 못함;
- 선언한 width/resource cap 안에서 \(F_\lambda\) 부호 또는 bound가 닫히지 않음.

어느 경우도 “가설 전체가 틀림”이 아니다. 정확한 실패 위치와 subbox를
`UNRESOLVED`로 남긴다.

### 실제 다음 P1 blocker: nonzero-\(\lambda\) minus-end \(\Gamma_1\)

선언된 raw-\(C\) extension은 finite-\(Q_0\) Neumann 조건이 아니라

\[
\Gamma_{1,p}u=-\lim_{Q\to-\infty}W(u,c_p)=0
\]

이다. \(\lambda=0\)에서는 reference equation 때문에
\(\Gamma_1=u_Q(Q_0)\)로 환원되지만, \(\lambda\ne0\)이면

\[
\Gamma_1(u)=u_Q(Q_0)-\lambda
\int_{-\infty}^{Q_0}6\pi^2e^{3Q/2}u(Q)c_p(Q)\,dQ
\]

의 left-boundary contribution이 생긴다. 따라서 direct \(h(-4)\)를
declared \(F_\lambda\), eigenvalue slope 또는 root velocity로 읽을 수 없다.
다음 계산은 selected reference field, normalization, minus-end remainder와
measurable \(p\)-family를 고정한 뒤 이 boundary variation을 검증해야 한다.
그 전까지 normalized/declared amplitude 출력은 `null`이다.

### 2026-08-30 scoped update: declared \(\Gamma_1\) zero-shell variation

번호 없는 `raw_c_declared_gamma1_boundary_variation`은 위의 fixed reference
pair \(c_p,s_p\)와 declared \(\Gamma_{1,p}=0\) domain을 바꾸지 않았다. 이
runner는 exact 11/11, Arb-ball 60/60, theorem/scope guard 6개를 통과해 다섯
inherited full \(\kappa\) bracket에서 다음만 좁게 인증했다.

\[
\Gamma_{1,p}(u_\lambda)=u_{\lambda,Q}(Q_0)-\lambda
\int_{-\infty}^{Q_0} A_\lambda(Q)u_\lambda(Q)c_p(Q)\,dQ,
\]

\(\lambda=0\) zero-shell root에서의 normalized declared derivative, explicit
left correction, 그리고 K-scaled representative의 \(\partial_\lambda\Gamma_1\)
box다. 두 punctured real \(\lambda\) box
\([-10^{-4},-10^{-8}]\), \([10^{-8},10^{-4}]\)에서는 actual solution 값이 아니라
declared minus-tail \(L^2(f\,dQ)\) norm **per unit** correction-functional operator
bound만 봉입했다. 80/120-digit tier는 같은 backend refinement이지 독립 구현이
아니다.

따라서 old finite-\(Q_0\) proxy가 declared \(\Gamma_1\)와 \(\lambda\ne0\)에서도
같다는 식은 이제 명시적으로 배제된다. 반대로 이 결과는 actual nonzero-\(\lambda\)
plus-recessive \(u_\lambda\), \(\Gamma_1(u_\lambda)\) value 또는 its remainder,
root continuation/velocity, root uniqueness, nonreal spectral data, RAQ, 물리학,
양자중력 또는 TOE 주장을 만들지 않는다. P1의 next blocker는 바로 그 actual
solution과 remainder의 validated construction이다.

### 2026-08-30 P1 actual nonzero-\(\lambda\) coarse enclosure

번호 없는 `raw_c_actual_nonzero_lambda_gamma1_coarse_enclosure`는 root bracket
#1과 두 punctured \(\lambda\) box에서 그 actual-family 공백을 **coarse
analytic enclosure** 수준으로 좁혔다. LG-selected actual recessive solution을
\(u_\lambda(4)=A_\lambda(4)^{-1/4}\)로 rescale하고, \(x\ge3\) Riccati
invariant region, \(x=3\to Q_0\) node-safe two-state Grönwall, \(Q<Q_0\)
rotating-frame Volterra tail을 순서대로 결합했다. exact 14/14, Arb 29/29,
guard 6개와 isolated `REPRO`가 통과했고 \(\lambda=0\) exact Bessel family도
두 precision tier에서 envelope 안에 들었다.

계산된 사실은 actual selected family와 전체 minus tail의 **유한 outward
bound**다. 두 \(\Gamma_1\) interval은 모두 약 \(10^{1410}\) 규모이며 0을
포함한다. 그러므로 P1은 `actual solution 없음`에서 `actual family의 coarse
boundedness 있음`으로 이동했지만, sharp endpoint/sign/root continuation은
아직 열려 있다. 다음 blocker는 compact Grönwall을 Bessel/LG-preconditioned
validated interval Taylor 또는 동등한 sharp transfer enclosure로 교체하는
것이다. 같은 backend의 80/120-digit overlap은 독립 구현 검증이 아니다.

### 2026-08-30 P1 barrier-outer interval-Taylor 판정

`raw_c_actual_nonzero_lambda_hybrid_validated_transfer`는 compact Grönwall 대신
16-step order-12 interval Taylor와 whole-step \(D_{13}|h|^{13}/13!\) remainder를
실제로 적용했다. 단, \(Q_s=-29/10\) 입력은 actual trajectory의 sharp datum이
아니라 inherited barrier 전체 \(\rho\in[-1,1]\)였다. 그러므로 이 계산은
selected actual family를 포함하는 모든 barrier-admissible direction의 outer
transfer다.

관측 결과는 exact 14/14, Arb 113/119, guard 5, isolated `REPRO`다. 실패한 6개는
모두 width \(<1/4\) gate이고, 나머지 여섯 tier는 \(v(-4)>0\), finite quotient
tail, precision overlap을 만족했다. \(\lambda=0\) Bessel inclusion도 두 tier에서
통과했다. width가 약 \(1.203\)으로 80/120 digits에서 거의 같다는 사실은 현재
병목이 rounding이 아니라 switch-direction 폭임을 지목한다.

따라서 이 시점 P1의 다음 수는 `segment 수 증가`가 아니라 다음 한 문장이었다.

> root bracket 1과 두 \(\lambda\) box에서 actual plus-recessive
> \(\rho(Q_s;\kappa,\lambda)\)를 \([-1,1]\)보다 충분히 좁게 outward
> certify할 수 있는가?

이 질문은 아래 별도 계산으로 실행됐고, 현재 compact/tail map을 sharp actual
family에 다시 적용했다.

### 2026-08-30 P1 sharp actual-direction contraction

그 별도 계산 raw_c_actual_direction_sharp_contraction_transfer는 exact
backward-\(x\) variation-of-constants, global \(0\le J_{\rho^2}\le J_0\) nonlinear
bound, monotone 512/1024-panel kernel-mass enclosure를 실제 plus-recessive
direction에 적용했다. exact 18/18, Arb-ball 133/133, guard 6와 isolated REPRO가
통과했다. 여섯 sharp-switch \(\rho\) width는 약 \(0.12778\),
downstream scale-free \(\Gamma_1\) width는 \(0.06370\)–\(0.06378\)로 모두
\(1/4\) 아래다.

하지만 여섯 \(g\) interval은 모두 0을 포함한다. 따라서 이건 sharp direction과
width의 workbench result이지 sign, root, spectrum, RAQ 또는 physics 결론이
아니다. P1의 다음 명시적 blocker는 global nonlinear box의 panelwise
Picard/affine refinement와 sharp chart 내부의 validated
\(\lambda\)-sensitivity/sign separation이다.

## 3. P2–P3: closed-\(S^3\) ADM와 HDA

현재 repository는 scalar-derived convention, full-sector **counting** ledger,
그리고 restricted zonal conformal curvature/trace-kinetic/\(V=0\) matter
subvertex를 갖는다. 이것들은 full ADM constraint가 아니다.

[Lindblom--Taylor--Zhang](https://arxiv.org/abs/1709.08020)은 \(S^3\)의
scalar/vector/tensor harmonic eigenvalue·divergence·trace·orthonormality
convention을 제공한다. [Nandi--Shankaranarayanan](https://arxiv.org/abs/1512.02539)은
cosmological perturbation의 all-order Hamiltonian 절차를, 후속
[noncanonical-scalar 논문](https://arxiv.org/abs/1606.05747)은 3·4차 interaction
Hamiltonian 예를 제공한다. 이들은 repository의 closed-\(S^3\) full HDA
coefficient나 cutoff remainder를 자동으로 주지 않는다.

P2 성공에는 명시적 low-mode SVT representative, chirality, 모든 필요한
Gaunt/Clebsch--Gordan coefficient, background scale/shear, scalar matter,
lapse와 shift가 같은 ADM convention에 있어야 한다. P3는 constraint를 먼저
continuum에서 bracket한 뒤 project한 값과, projected constraint를 bracket한
값의 차이를 기록해야 한다. 유한 cutoff에서 Jacobiator가 nonzero라는 사실만으로
quantum anomaly를 선언할 수 없다.

이번 `closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger`는 이 원칙을
작은 nontrivial packet에서 실제로 확인했다. fixed-background matter 범위에서
ambient \(HH\)와 momentum target은 \(5/(\pi^2a^2)\)로 같았다. \(L=2\)의
projected bracket 0과의 차이는 정확히 omitted \(k=3\) canonical channel이고,
\(L=3,4\)에서는 그 channel이 복구되어 remainder가 0이 됐다. 이는 scoped
classical matter identity와 cutoff provenance의 진전이며, full ADM/HDA/Jacobi나
quantum BFV anomaly freedom의 증거는 아니다.

별도 `closed_s3_linear_scalar_adm_momentum_constraint_ledger`는 unit-\(S^3\)
scalar metric pair에 대해
\(D_L^{(1)}=\sum L_n(\Pi_{E,n}-\lambda_n\Pi_{\zeta,n}/3)\)를 31/31 exact
check로 고정했다. 이는 earlier longitudinal coordinate convention을 실제 ADM
momentum projection과 연결한 진전이다. 그러나 gradient-shift commutator에 필요한
transverse-vector sector, Hamiltonian constraint와 모든 \(DD/DH/HH\), Jacobi가
빠져 있으므로 full HDA 진전으로 승격하지 않는다.

고전 hypersurface-deformation algebra의 기준선은 Teitelboim/HKT이고,
repository의 성공 게이트는 그 continuum identity를 인용하는 것이 아니라
선언한 \(S^3\) coefficients가 실제로 재현하는지와 discarded remainder가
\(L\)에 따라 어떻게 줄어드는지를 계산하는 것이다.

## 4. P4: singular spectral theory, RAQ, constraint rescaling

P1의 real root 정보만으로 \(\delta(C)\) 또는 spectral density를 만들 수 없다.
반대로 선택한 self-adjoint extension의 nonreal resolvent 연구는 P1의
\(F_\lambda\)를 기다리지 않고 시작할 수 있다. 다만 real-axis boundary-value와
root/Jacobian 일치가 후속 교차검사다.
필요한 순서는 다음이다.

```text
selected self-adjoint extension
  -> nonreal resolvent and Weyl m(z)
  -> boundary values / spectral measure / multiplicity
  -> measurable p-direct integral
  -> dense test space and rigging form
  -> positivity, null quotient, observable action
  -> raw-C RAQ
  -> independent comparison with H=fC
```

[Eckhardt et al.](https://arxiv.org/abs/1208.4677)은 singular
Weyl--Titchmarsh \(m\)-function, self-adjoint boundary condition과 spectral
transform의 operator-theoretic 기준선이다. [Marolf의 single-constraint
RAQ](https://arxiv.org/abs/gr-qc/9508015)은 auxiliary structure와 rigging-map
선택 문제를 명시한다. 가장 중요한 경고는
[Louko--Martínez-Pascual](https://arxiv.org/abs/1107.1092)이다. 고전적으로
rescale된 constraint family도 양자화에서는 동치, 자기수반 확장 부재, 또는
extension/superselection ambiguity의 서로 다른 경우로 갈린다. 따라서
\(H=fC\)라는 고전식 자체가 양자동치의 증거는 아니다.

성공 판정은 extension·test space·observable class를 명시한 제한적
`EQUIVALENT_IN_DECLARED_CLASS` 또는 구체적 `INEQUIVALENT_WITNESS`여야 한다.
global하고 자동적인 equivalence label은 허용하지 않는다.

## 5. P5–P6: BFV charge, anomaly, absolute amplitude

두 문제는 구분한다.

- P5: 실제 ADM/HDA structure functions에서 고전 BFV charge를 만들고,
  선택한 common operator core에서 quantum nilpotency defect를 계산한다.
- P6: boundary polarization, lapse contour, Gribov coverage, boson/ghost
  superdeterminant, determinant/Pfaffian line orientation, regulator removal과
  gluing을 모두 포함하는 amplitude 문제다.

[classical BV--BFV](https://arxiv.org/abs/1201.0290)는 bulk BV와 boundary BFV,
corners를 연결하고, [quantum BV--BFV](https://arxiv.org/abs/1507.01221)는
cutting/gluing과 양립하는 perturbative framework를 제시한다. 2026년의
[Rejzner--Schiavina](https://arxiv.org/abs/2607.13765)는 smoothened boundary의
pAQFT/BV-BFV에서 modified master equations와 renormalized boundary BFV
operator를 구성하며, boundary QME failure를 curvature로 다룬다. 하지만
그 논문의 explicit leading-order 회수는 causal cylinder의 Abelian
Yang--Mills이고, 이 repository의 중력 absolute measure나 anomaly freedom을
완성하지 않는다.

현재 finite Ward/Pfaffian/toy-gluing 결과는 상대 determinant bookkeeping을
줄였을 뿐이다. absolute BFV 성공 게이트는 한 regulator에서의 cancellation이
아니라 다음 전체의 동시 성립이다.

1. gauge slice의 orbit coverage와 Gribov boundary;
2. lapse modulus/contour와 singular endpoint의 relative-homology class;
3. determinant/Pfaffian line의 absolute orientation과 zero crossing;
4. boundary polarization/QME;
5. two-slab gluing과 regulator removal.

## 6. P7: relational clocks에서 관측 likelihood까지

두 clock 비교는 서로 다른 reduced theory의 숫자를 곧바로 비교하는 일이
아니다. clock-neutral Dirac theory, physical inner product와 공통 observable
class가 필요하다. [Höhn--Vanrietvelde](https://arxiv.org/abs/1810.04153)는
Dirac-quantized theory를 통해 clock choice를 전환하는 방법을 제시하고,
[relational dynamics trinity](https://arxiv.org/abs/2007.00580)는 frequency
sector별 relational Dirac observable, Page--Wootters, deparametrization의
동치를 다룬다. 이는 현재 closed cosmology operator에서의 적용 결과가 아니다.

BO correction의 unitarity도 inner product와 time gauge에 의존한다는
[Chataignier--Krämer](https://arxiv.org/abs/2011.06426)의 분석 때문에,
clock/physical product를 건너뛰고 power spectrum correction으로 이동하면
안 된다.

관측 연결에는 적어도 \(V\ne0\) background, perturbation-generating initial
state, closed-mode evolution, reheating/late-time transfer와 primordial scalar/
tensor spectra가 필요하다. 그 뒤에야 [CLASS](https://github.com/lesgourg/class_public)로
observable spectra를 만들고 [Cobaya](https://cobaya.readthedocs.io/en/stable/)의
likelihood interface로 평가한다. 비교 기준은
[ACT DR6](https://arxiv.org/abs/2503.14452v2)와
[SPT-3G D1](https://arxiv.org/abs/2506.20707v2)처럼 version-pinned data/
likelihood여야 한다. 현재 \(V=0\) massless-scalar local model은 standard
inflation/reheating을 제공하지 않으므로 직접 CMB likelihood는 차단 상태다.

## 7. 철학적 함의—계산 범위를 넘지 않는 선

1. **고전적 같은 식은 양자적으로 같은 이론이 아니다.** domain, measure,
   extension과 observable algebra가 양자화 자료다.
2. **경계조건은 단순 기술 선택이 아니다.** limit-circle end의 boundary line은
   self-adjoint operator와 spectrum을 바꿀 수 있으므로 명시해야 한다.
3. **유한 truncation의 비폐쇄는 anomaly와 다르다.** omitted-mode remainder를
   측정한 뒤에야 continuum algebra failure를 논할 수 있다.
4. **상대 determinant는 absolute amplitude가 아니다.** contour, Gribov,
   line orientation과 gluing이 빠지면 normalization/phase는 미결이다.
5. **시간은 관계적일 수 있어도 관측 예측은 자동으로 나오지 않는다.** clock
   전환, physical product, state preparation과 late-time transfer가 별도다.
6. **부정적 결과는 대개 scope를 자른다.** 명시한 operator/ordering/chart가
   실패했다는 사실과 모든 양자중력 경로의 실패를 구분한다.

## 8. KG 읽기 규칙과 상태 갱신 규칙

KG에서 먼저 `concept:gate1-v0-six-bridge-metacognitive-priority-map`을 읽고,
\(\lambda=0\) Bessel anchor, \(h(4)\) tail, direct Green endpoint의 세
claim/evidence를 거쳐 retarget된 nonzero-\(\lambda\) \(\Gamma_1\) open
problem과 나머지 P2–P7 open problem으로 따라간다. `CITES` edge는
방법·정리 출처이지 claim support가 아니다. support는 오직 tracked result와
evidence snapshot의 `HAS_EVIDENCE` edge가 담당한다.

상태는 다음 사건이 있을 때만 바꾼다.

- 새로운 계산이 claim의 지위·scope 또는 직접 evidence를 실질적으로 바꿈;
- 독립 재현이 기존 결과를 뒤집거나 scope를 좁힘;
- primary source의 가정을 잘못 옮겼음이 확인됨;
- 다음 open problem의 성공 게이트가 실제로 충족됨.

문구 정리, 같은 backend의 precision 증가, 문헌 추가만으로 claim을 승격하지
않는다. 외부 KG writer와 정확한 대응 UID가 없으므로 local graph가 정본이고,
외부 bridge에는 UID를 만들지 않고 `UNRESOLVED`를 유지한다.

## 9. 이번 결과의 재현·검증 경로

```text
./ice info raw_c_lambda_zero_bessel_ball_transport
./ice info raw_c_lambda_zero_differentiated_plus_tail
./ice info raw_c_lambda_zero_node_safe_green_transport
./ice repro --only raw_c_lambda_zero_node_safe_green_transport
./ice ontology validate
./ice ontology summary
npm run check
```

세부 수식과 exact intervals는
`cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT.md`,
`cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_DIFFERENTIATED_PLUS_TAIL.md`,
`cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_NODE_SAFE_GREEN_TRANSPORT.md`와
각 인접 result JSON에 있다. 전체 task 분해는
`ICE_QUANTUM_GRAVITY_EXECUTION_DAG_2026-08-28.md`, P1 인증 순서는
`RAW_C_ENDPOINT_CERTIFICATION_REQUIREMENTS_2026-08-29.md`가 담당한다.
