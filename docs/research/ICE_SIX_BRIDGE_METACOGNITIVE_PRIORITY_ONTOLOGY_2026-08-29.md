# ICE 여섯 연결부 메타인지 우선순위 온톨로지

> 기준일: 2026-08-29
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

현재 가장 빠른 1순위는 raw-\(C\)의 **differentiated plus-tail와 node-safe
\(F,F_\lambda\) 검증**이다. 이유는 다음과 같다.

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
| P1 | raw-\(C\) differentiated tail와 node-safe \(F,F_\lambda\) | **부분 돌파**: \(\lambda=0\) exact transport와 실근 존재 구간 5개 ball 인증 | \(\partial_\lambda\) tail datum + node crossing을 포함한 outward enclosure | tail derivative 미봉입, chart denominator가 0 포함, enclosure 비중첩/폭발 | P4 |
| P2 | full \(S^3\) SVT/Gaunt와 ADM cubic coefficient | 독립 착수 가능; 현재는 restricted zonal subvertices뿐 | scalar/vector/TT와 lapse/shift·matter를 같은 convention으로 cubic까지 구성 | basis/convention 불일치, 누락 sector, cutoff tail 미측정 | P3 |
| P3 | 고전 HDA/Jacobi와 cutoff remainder 분리 | 오픈 | full-before-project bracket, Jacobiator, \(L\) scaling 및 analytic remainder | 유한 cutoff defect를 continuum anomaly로 오인하지 않는 `UNCLASSIFIED_REMAINDER` | P5 |
| P4 | nonreal Weyl \(m\), spectral measure, raw-\(C\) RAQ와 \(C/H\) 비교 | 독립 method 착수 가능; real-axis 일치는 P1과 만남 | self-adjoint domain·measurable \(p\)-family·test space·positive rigging form·observable intertwining | Herglotz 부호/positivity/domain map 실패 또는 extension dependence | equivalence 판정 및 raw-\(C\) representation을 쓸 경우 P5 |
| P5 | 고전 BFV charge와 quantum nilpotency/anomaly | 고전 charge는 P3에 의존; raw-\(C\) physical core 적용은 P4도 필요 | 실제 structure functions와 common invariant core에서 \(\Omega^2\) defect 분해 | ordering/domain/regulator/truncation defect를 구분해 기록 | P7 |
| P6 | contour·Gribov·determinant line·gluing을 포함한 absolute BFV | 방법 연구는 병렬, gravity 적용은 P3/P5와 만남 | boundary QME, gauge coverage, absolute orientation, regulator removal과 gluing | contour/Gribov/gluing/line orientation 중 실패 위치를 분리 | P7 |
| P7 | 두 clock relational observable → BO/decoherence → \(V\ne0\) CLASS/Cobaya likelihood | downstream | 동일 physical product의 clock 비교, primordial spectra, pinned likelihood | clock chart/inner-product/initial-state/reheating 부재면 likelihood 금지 | 관측 비교 |

의존성은 다음과 같다.

```text
P1 real-axis derivative endpoint ──┐
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
| `OPEN` | 각 bracket의 root uniqueness와 \([0,8]\) 전체 census completeness |
| `OPEN_P1` | parameter-differentiated plus-tail boundary datum |
| `OPEN_P1` | node-safe validated propagation과 endpoint \(F_\lambda\) enclosure |
| `OPEN_P4` | nonreal Weyl \(m\), spectral measure, test space, rigging map, RAQ |
| `NULL` | raw-\(C\)/selected-\(H\) quantum equivalence, physics, quantum gravity, TOE |

### 바로 다음의 가장 작은 독립 계산

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

가장 작은 다음 계산은 amplitude보다 scale-invariant인

\[
g=-u'/u,\qquad h=\partial_\lambda g,
\qquad h'=2gh-A_\lambda
\]

의 \(Q\ge4\) differentiated Volterra/Riccati tail enclosure 하나다. 기존 tail
theorem은 이 \(h(4)\) 오차를 주지 않는다. 그 계산이 닫힌 뒤 node를 통과하는
Prüfer/projective atlas로 민감도를 전달한다. 한 가능한 chart는

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

P1의 fail-closed 조건은 다음과 같다.

- differentiated tail variation이 적분 가능하거나 작다는 증명이 없음;
- plus-end normalization을 선언하지 않은 채 amplitude \(F_\lambda\)를 출력함;
- interval chart의 denominator가 0을 포함하고 안전한 chart 전환도 없음;
- refinement/precision 증가 시 enclosure가 중첩하지 않음;
- Wronskian lower bound가 0을 배제하지 못함;
- 선언한 width/resource cap 안에서 \(F_\lambda\) 부호 또는 bound가 닫히지 않음.

어느 경우도 “가설 전체가 틀림”이 아니다. 정확한 실패 위치와 subbox를
`UNRESOLVED`로 남긴다.

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
P1 open problem, 새 \(\lambda=0\) claim/evidence, 나머지 P2–P7 open problem으로
따라간다. `CITES` edge는 방법·정리 출처이지 claim support가 아니다. support는
오직 tracked result와 evidence snapshot의 `HAS_EVIDENCE` edge가 담당한다.

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
./ice run raw_c_lambda_zero_bessel_ball_transport
./ice repro --only raw_c_lambda_zero_bessel_ball_transport
./ice ontology validate
./ice ontology summary
npm run check
```

세부 수식과 exact intervals는
`cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT.md`와
그 인접 result JSON에 있다. 전체 task 분해는
`ICE_QUANTUM_GRAVITY_EXECUTION_DAG_2026-08-28.md`, P1 인증 순서는
`RAW_C_ENDPOINT_CERTIFICATION_REQUIREMENTS_2026-08-29.md`가 담당한다.
