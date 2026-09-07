# BFV/CPT 접합을 실제 source로 만드는 다음 구성

2026-09-07 · **DESIGN_CANDIDATE / SUPPORTING_METHOD**.

추천하는 다음 출력은 **하나의 finite sewn BFV source와 그 boundary Ward defect**다.
적용 범위는 기존 동차 Starobinsky 축약 모형의 lapse/ghost를 포함하는 BFV extension이다.
[기존 설계](ICE_CPT_SEWING_ORIGINAL_CYCLE_CONSTRUCTION_DESIGN_2026-09-06.md)의 실수 경계
항등식을 ghost/lapse까지 확장한 뒤, 실제 경계 pairing과 cutoff faces를 함께 명시한다.
아래 고전 부호와 operator 대조는 손 전개 및 독립 읽기 검토다. 이번에 새 Lean 정리,
양자 source, original relative class 또는 G1 해소가 검증되었다고 표시하지 않는다.

```mermaid
flowchart LR
  A["검증된 실수 경계 대수"] --> B["ghost/lapse 포함 고전 BFV 관계"]
  B --> C["polarization·측도·양자 접합 커널"]
  C --> D["규제된 joint chain과 모든 경계면"]
  D --> E["Ward defect·zero-lapse contact"]
  E --> F["허용 상대 경로와 global intersections"]
```

이것은 작업 의존 관계다. A만 기존 Lean 결과이며 나머지 화살표는 구성 의무다.

## 1. 고전 BFV lift는 구체적으로 쓸 수 있다

[같은 모델의 convention](../../cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md)을
유지한다. Even bracket은 antisymmetric, odd canonical bracket은 symmetric +1이며,
odd 변수 c, ρ는 ghost number +1, barρ, barc는 −1이다.

\[
\alpha_{\rm BFV}=p_a\delta a+p_\phi\delta\phi+\Pi\delta N
 +\bar\rho\delta c+\bar c\delta\rho,\quad
\Omega=cH_L+\rho\Pi,\quad\Psi=-N\bar\rho.
\]

선언할 real boundary map 후보는

\[
\mathcal T:(a,\phi,N;p_a,p_\phi,\Pi;c,\bar\rho,\rho,\bar c)
\mapsto(a,\phi,N;-p_a,-p_\phi,-\Pi;-c,\bar\rho,\rho,-\bar c).
\tag{1}
\]

각 canonical pair에 대입하면

\[
\mathcal T^*\alpha_{\rm BFV}=-\alpha_{\rm BFV},\quad
\mathcal T^*\Omega=-\Omega,\quad\mathcal T^*\Psi=\Psi.
\tag{2}
\]

Anti-Poisson 성질과 함께 QF={Ω,F}에 대해

\[
\mathcal T^*(QF)=-\{\mathcal T^*\Omega,\mathcal T^*F\}
=Q(\mathcal T^*F)
\]

가 된다. Gauge-fixed Hamiltonian −{Ω,Ψ}도 보존한다.
Polynomial chart에서도 (u,v,n)은 고정, (P_u,P_v,π_n)은 반사,
(C,B,R,D)→(−C,B,R,−D)로 운반하면 G→−G, k→−k, h→h다.
이는 canonical chart의 재표현이지 독립 evidence가 아니다.

두 경계의 primitive를 α₁+α₂로 선언하면 LΣ=Graph(𝒯)에서 그 제한은 0이다.
따라서 **이 고전 관계에서는 추가 interaction SΣ=0이 가능한 후보**다.
실제 bulk/GHY 및 polarization boundary term에서 남는 1-form b가 다르면
δSΣ=−b를 풀어야 한다. b가 nonclosed면 현재 경계 변수의 scalar action 하나로
상쇄할 수 없고, closed but nonexact면 전역 단일값 생성함수의 장애물이 남는다.

(1)은 점별 real boundary map이다. 좌표시간 반전, complex conjugation,
Pin/fermion lift, ghost mode span과 endpoint 조건의 보존을 포함하지 않는다.
특히 기존 Euclidean sine/cosine truncation을 Lorentzian source로 자동 이식하지 않는다.
[Cattaneo–Schiavina, Theorem 2.5](https://arxiv.org/html/1509.05762)는 ADM bulk 변분에서
BV–BFV 경계 자료를 얻는 방법의 근거이며, ICE의 complex seam 존재 정리는 아니다.

## 2. SΣ=0과 양자 접합 kernel은 별개 객체다

실제 구성 단위는 (boundary BFV space, α, Ω, orientation, LΣ,
polarization, ordered Berezin measure, boundary kernel)의 묶음이어야 한다.
좌표와 운동량의 두 matching delta를 무조건 곱하면 polarization을 과도하게 고정할 수 있다.
한 polarization 또는 서로 쌍대인 두 polarization을 고르고, (1)의 관계를 구현하는
분포/적분 kernel과 ghost 적분 순서를 실제로 유도해야 한다.

[CMR §2.4.4, eqs. (2.36)–(2.37)](https://arxiv.org/html/1507.01221)는 경계 상태의
pairing 뒤 residual fields에 대한 BV pushforward로 접합한다. Polarization을 바꾸면
생성함수의 경계 phase가 나타날 수 있다. SΣ=0이라는 고전 결과로 이 phase나
half-density normalization까지 1이라고 놓을 수 없다. Boundary BFV 연산자의
intertwining과 modified quantum master equation도 확인해야 한다. 이 문헌은
섭동적 구성으로, ICE의 비섭동 적분 측도나 경로를 제공하지 않는다.

[Cattaneo–Mnev–Wernli](https://www.aimsciences.org/article/doi/10.3934/jgm.2022010)는
제약된 interval dynamics와 HJ action의 양자화를 직접 다룬다. 다만 논문의 해당
polarization-change 구성에는 양쪽 endpoint momentum에 constraint가 linear라는
제한이 있다. ICE H_L은 quadratic이므로 그 정리를 조건 확인 없이 가져오지 않는다.
Positive physical Hilbert space는 여기서 구성했다고 가정하지 않는다. 먼저 BFV
boundary cochain pairing을 만들고, positivity 및 quantum CPT의 물리적 구현은 따로 남긴다.

## 3. positive lapse와 CPT에 대한 두 가지 operator 대조

아래는 self-adjoint H, domain을 보존하는 antiunitary Θ, ΘHΘ⁻¹=H가 **이미 주어진**
operator model의 정확한 대조다. ICE의 해당 domain/Θ는 아직 구성되지 않았다. ℏ=1로 둔다.

\[
U_T=e^{-iTH},\quad
G_\epsilon=\int_0^\infty e^{-\epsilon T}U_T\,dT
=-i(H-i\epsilon)^{-1},\quad\epsilon>0.
\]

첫째, anti-linearity가 i의 부호를 바꾸므로

\[
\Theta G_\epsilon\Theta^{-1}=G_\epsilon^\dagger
=+i(H+i\epsilon)^{-1}.
\tag{3}
\]

따라서 positive-lapse source에 요구할 것은 conjugate/adjoint source와의 covariance다.
Gε 자체의 CPT invariance를 요구하면 다른 조건을 검사하게 된다. 이 식은 실제
two-copy BFV seam을 선택하지 않으며, constraint projector도 만들어 주지 않는다.

둘째, ordinary serial composition에서 두 조각의 lapse를 독립 적분하면

\[
G_\epsilon^2=\int_0^\infty T e^{-\epsilon T}U_T\,dT
=-\partial_\epsilon G_\epsilon.
\tag{4}
\]

단일 total-proper-time transition을 목표로 선언한다면, 먼저 fixed-time kernel의
합성 U_{T₂}U_{T₁}=U_{T₁+T₂}와 identity limit를 확인하고 total modulus 하나를 적분한다.
두 독립 propagator가 목적이면 G²가 맞는 다른 대상이다. (4)를 실제 CPT seam의
합성식으로 동일시하지 않는다. Full-real-lapse group averaging도 별도 source 선택이다.

## 4. original chain은 실수 유한 적분의 정의부터 명시한다

첫 규제 후보에는 시간 분할 수 m, 경계 polarization, ordering/discretization과
고정 양수 δ,A,Φ,P,ν,L,PΠ를 선언한다. Bosonic body의 표본 범위는

\[
\delta\le a_j\le A,\quad |\phi_j|\le\Phi,\quad
|p_{a,j}|,|p_{\phi,j}|\le P,\quad
\nu\le N_j\le L,\quad |\Pi_j|\le P_\Pi.
\tag{5}
\]

이 범위를 두 branch에 주고, seam에서는 선택한 kernel 또는 그 관계에 맞게
pushforward한다. Ghost는 실수 contour 변수가 아니라 선언한 순서의 Berezin 적분이다.
Smooth finite coefficients와 적절히 정의된 seam pairing이면 finite integral을
출발점으로 삼을 수 있다. 이 문서는 아직 그 full kernel을 제공하지 않는다.

중간 N_j를 모두 하나의 N으로 줄이는 단계도 증명이 필요하다. Ψ=−N barρ와 Π의
Fourier 적분이 proper-time 조건을 만들지만, 유한 Π cutoff에서는 delta가 아닌
규제된 kernel이다. dot N=0을 먼저 강제한 식과 primary-pair 적분을 둘 다 유지해
같은 자유도를 중복 처리하지 않는다. 단순 midpoint action은 시험용 discretization일
뿐이며 기존 exact gauge-preserving element나 quantum kernel로 승격하지 않는다.

수렴 대조로 e^{−ηR}, R=Σ(p_a²+p_φ²), η>0를 추가할 수 있으나 다음 구별이 핵심이다.

\[
\mathcal T^*R=R,\qquad
QR=2c(p_a\partial_a H_L+p_\phi\partial_\phi H_L)\ne0
\quad\text{(일반적인 한 canonical copy).}
\tag{6}
\]

**반사 대칭을 가진 regulator도 BRST 대칭을 깰 수 있다.** BRST 변수변환의 Ward 식에는
cutoff faces의 flux, regulator insertion, discretization defect가 남을 수 있다.
Q-closed/Q-exact 규제를 택하더라도 경계 flux의 소거는 별도다. η를 작게 해 residual이
작아 보이는 것만으로 이 항들을 지우지 않는다. 기존
[운동량 pushforward 검사](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md)가
보였듯 하나의 lapse i0 shift가 중력/물질의 반대 kinetic sign을 가진 실수 축을 모두
감쇠시키는 것도 아니다. (5)의 compactness와 축 감쇠, lapse resolvent 처방을 구별한다.

(5)의 chain은 적분 범위를 선언한 시작점이다. Physical original cycle로 인정하려면
ambient complex space, singular divisor, 모든 cutoff faces와 good ends, orientation,
regulator 제거 순서 및 분포 극한을 명시해야 한다. 어떤 boundary를 허용하는지 정하지
않은 채 relative class가 완성됐다고 쓰지 않는다. ν↓0에서 K_T→Id가 확인되어야
(H−iε)Gε=−i Id의 contact가 맞는다. N=0 face를 버려 이를 0으로 만들면 다른 source다.

Polynomial chart로 옮길 때는 u=a², v=u exp(−βφ)의 correlated bounds와
n=N/(24π²u^{3/2})를 각 표본에 운반한다. dot N=0은 d(fn)/ds=0이고, dot n=0이 아니다.
u=0이나 독립 (u,v,n) box를 추가하면 source를 변경한다.
[Feldbrugge–Lehners–Turok §II, eqs. (6)–(10)](https://arxiv.org/html/1703.02076)의
교훈은 이 original domain을 먼저 정한 뒤 upward-cycle 교차로 thimble 계수를 얻는 순서다.
그 논문의 단순 모델 contour가 ICE의 joint chain을 대신하지 않는다.

## 5. 다음 한 작업의 출력과 폐기 조건

질문: **한 선언된 finite boundary polarization과 source에서 BFV 접합의 Ward defect를
실제 cutoff/zero-lapse 항까지 포함해 도출할 수 있는가?** 출력은 해당 defect의 식과
그 식에 필요한 source 자료 하나다. Kernel 또는 finite BRST 연산자를 아직 정의하지
못하면 그 누락 자체를 출력하며, 정의되지 않은 적분의 residual을 0으로 기록하지 않는다.

주된 위험은 gauge다. 관련 대조는 (i) full graded sign와 boundary kernel intertwining,
(ii) regulator/cutoff flux의 직접 계산, (iii) 선언한 source type에 맞는 fixed-lapse
composition 및 zero-lapse contact다. Nonzero defect가 정의된 경계항으로 설명되지
않으면 그 source 후보를 수정하거나 닫는다. 접합 identity의 반복 증명만으로 이 검사를
대체하지 않는다.

Lean의 다음 역할은 실제 graded boundary algebra와 도출한 defect 항등식을 검증하는
것이다. Unknown kernel, measure, limit를 axiom으로 선언한 뒤 theorem 이름만 늘리지 않는다.
Finite source가 정의된 뒤에야 같은 source를 나타내는 chart/gauge/regulator 선택군에서
class와 oriented intersection이 유지되는지 검사한다. 경계 상태, lapse 적분의 반직선/전직선,
위상 자체를 바꾸는 것은 단순 gauge 변경으로 묶지 않는다.

## 검토와 provenance

- Canonical blocker: `open:gate1-original-cycle-signed-global-intersections`.
  Missing object: source-defined regulated joint relative class. 이번 출력은 그 source의
  설계 후보와 obstruction 식이며 class 자체가 아니다.
- 유효한 `./ice agent plan ... --graph cpt --json` 결과는
  `CURRENT_BLOCKER_CANDIDATE`. 첫 호출은 질문 500자 상한으로 거절됐고 짧게 수정했다.
  Planner는 근거나 승인으로 쓰지 않았다. 이 문서는 core 계산 결과로 세지 않는다.
- Dependency: G1 → G2 uniform kernel → G3 determinant/gluing → G4 state/domain
  → G5 interaction → full-theory/empirical external review.
- `./ice harness context`와 choice-invariance guide, 해당 canonical-target intuition
  조회를 읽었다. Intuition signal은 navigation으로만 사용했다.
- 2026-09-07 문헌 discovery의 `./ice literature search`는 OpenAlex HTTP 429로
  실패했다. Web 검색으로 위 primary papers의 본문/출판사 원문을 읽었다.
- 독립 읽기 검토는 (1)–(2)의 graded signs/BRST, (3)–(4)의 antiunitary/resolvent 부호,
  finite-chain regulator와 primary-pair 한계를 대조했다. 새 scientific runner는 실행하지 않았다.
- 방법 메모이므로 canonical claim/evidence 상태와 repro manifest는 바꾸지 않는다.
  새로운 물리적 발견, 물리 CPT 구현 또는 G1 완료를 주장하지 않는다.
