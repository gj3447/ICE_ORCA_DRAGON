# 연속 source 후보 인증: 인터넷 1차 문헌으로 보완한 설계

2026-09-06. 기준: `bdbca0e`의
[현재 연구 적대적 검토](ICE_CURRENT_RESEARCH_ADVERSARIAL_REVIEW_2026-09-06.md).
지위: `SUPPORTING_METHOD`, 문헌 검토와 미실행 설계.

후속 실행은 [국소 연속 endpoint certificate 결과](ICE_STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_2026-09-06.md)에
기록했다. 아래는 그 실행 전에 고정한 문헌·설계 기록이며, 설치·실행 여부에 관한 문장은
이 설계 시점의 상태를 뜻한다.

**보완 결론:** 제안한 constrained shooting 인증에는 문헌상 구체적인 구현 경로가 있다.
다만 `F`의 근사 root에 interval 연산을 덧붙이는 것으로 끝나지 않는다. 연속 flow와
그 미분 자체의 enclosure, 미지의 proper length `T`에 대한 미분, 전 구간의 `a>0`
보장이 필요하다. 성공해도 국소 branch 인증이며 original integration cycle을 정하지 않는다.

## 1. 읽은 원문이 실제로 제공하는 것

| 1차 자료와 확인 위치 | 사용할 수 있는 근거 | ICE에 남는 일 |
|---|---|---|
| [Kapela–Mrozek–Wilczak–Zgliczyński, CAPD::DynSys (2021), §4.1–4.2](https://arxiv.org/html/2010.07097) | `C1` flow·변분 방정식을 감싸고 interval Newton으로 BVP를 인증하는 실제 예제; 다변수 zero 판정식 (10) | Starobinsky RHS, 3변수 residual, domain tube와 runtime을 직접 검증 |
| [Rump, Verification methods (2010), Theorem 13.3 / (13.8)](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf) | Krawczyk inclusion의 존재·유일성·Jacobian regularity 조건 | `F`와 `DF`를 모두 연속 문제의 참값을 포함하는 enclosure로 입력 |
| [Bahr–Dittrich–Steinhaus (2011), §2 / (2.3)–(2.7)](https://arxiv.org/html/1101.4775) | classical perfect action, vertex translation, quantum measure를 구별 | local classical action만으로 BFV·물리적 measure를 채우지 않음 |
| [Dittrich–Höhn (2013), §5.3 / Theorems 5.2–5.3](https://arxiv.org/html/1303.4294) | pre/post constraint, Hessian 및 Lagrangian two-form의 null 구조와 gauge 관계 | 작은 고유값이나 좌표상의 정지점을 gauge 존재/부재와 동일시하지 않음 |
| [Marrero–Martín de Diego–Martínez (2016), §5.3 / (5.13)](https://arxiv.org/pdf/1608.01586) | regular Lagrangian의 국소 exact discrete action과 그 boundary-value 정의 | 작은 시간·국소 조건을 확인; `T≈0.7`의 전 구간이나 constrained BFV로 자동 확대하지 않음 |
| [Witten (2010), §2.2 / (2.16), §3.1.2 / (3.12)](https://arxiv.org/html/1001.2933) | `n_sigma=<C,K_sigma>`와 Stokes에서의 thimble jump | source cycle `C`, global upward cycle, orientation, end census를 따로 구성 |
| [Feldbrugge–Lehners–Turok (2017), §II / (6)–(8)](https://arxiv.org/html/1703.02076) | minisuperspace에서도 original domain을 정한 후 intersection으로 기여 saddle을 판별하는 예 | 다른 potential·boundary·contour의 모델 사례이며 ICE의 contour 선택 근거가 아님 |

문헌이 정한 일반 방법과 아래 ICE-specific 설계를 구별한다. 어느 논문도 이 저장소의
Starobinsky certificate, BFV source, G1 intersection 또는 TOE 결과를 제공하지 않는다.

## 2. 기존 3변수 질문을 실행 가능한 수학적 형태로 보완

앞선 문서의 경계값과 residual `F(y)`를 그대로 사용한다.
`y=(v_a,-,v_phi,-,T)`이며 proper-time의 full Euler–Lagrange state를
`u=(a,v_a,phi,v_phi)`로 둔다. 해당 RHS는
[Phase 24 runner의 euclidean_rhs](../../cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py)에
기록되어 있다. `C=0`에서만 맞는 scale equation으로 교체하면 다른 off-shell map을 인증한다.

### 미지의 최종 시간도 변분 방정식에 포함

`s=tau/T`로 바꾸어 항상 `s∈[0,1]`에서 다음 5차원 계를 사용한다.
이것은 이 메모의 적용 설계이며 CAPD 논문에 실린 ICE 예제가 아니다.

```math
z=(a,v_a,\phi,v_\phi,T),\qquad
\frac{dz}{ds}=g(z)=(T f(u),0),\qquad
z(0)=(a_b,v_{a,-},\phi_b,v_{\phi,-},T).
```

```math
\frac{dM}{ds}=Dg(z)M,\qquad M(0)=I_5.
```

flow와 `M`을 초기 box 전체에 대해 함께 감싼다. `M(1)`에서 1-based index로
rows `(1,3)`, columns `(2,4,5)`를 취하면 `DF`의 첫 두 행이다.
마지막 행은 초기 constraint의 해석적 미분이다.

```math
DF(y)=\begin{pmatrix}
M_{1,2}&M_{1,4}&M_{1,5}\\
M_{3,2}&M_{3,4}&M_{3,5}\\
2v_{a,-}&-a_b^2v_{\phi,-}/3&0
\end{pmatrix}.
```

따라서 `T`의 구간만 바꾸고 fixed-time initial-data Jacobian을 재사용하는 실수를 막는다.
autonomous original flow의 항등식 `∂T Phi_T(u0)=f(Phi_T(u0))`는 이 시간 미분 열을
대조하는 방법이다. 이 항등식을 수치적으로 검사했다는 뜻은 아니다.

### 승인되는 출력은 inclusion certificate

정확히 표현한 유한 중심 `y0`, 양의 반지름을 가진 box `Y=y0+[-r,r]`, 고정 실수 점행렬 `B`와
연속 문제의 enclosure `[F0]⊇F(y0)`, `[J]⊇DF(Y)`를 사용한다.

```math
[K]=y_0-B[F_0]+(I-B[J])(Y-y_0).
```

각 성분에서 엄격한 `[K]⊂int(Y)`를 outward rounding으로 검증하면 Rump Theorem 13.3의 충분조건을
적용할 수 있다. 이것은 해당 box의 유일한 regular root를 인증한다.
실패하면 `INCONCLUSIVE`다. `0∉[F_i(Y)]` 같은 별도의 exclusion 없이 `NO_ROOT`를 쓰지 않는다.
이때 `[F0]`와 `[J]`가 단순히 수치 적분 결과를 둘러싼 임의 반지름이어서는 안 된다.

certificate에는 `Y`, `[F0]`, `[J]`, `B`, `[K]`, strict inclusion 여유와
전 구간 `a`의 양의 하한을 남기면 된다. `T`의 양의 하한과 모든 ODE step의
existence/truncation enclosure도 이 숫자들의 유효성을 뒷받침해야 한다.
에너지 항등식 `H_E=-6π²a C`, `dH_E/dtau=0`은 초기 `C=0`의 전 구간 전파를 설명한다.
출력 형식은 다음 실제 runner를 설계할 때 정하며, 지금 새 ledger나 실행 계약을 만들지 않는다.

## 3. 구현 선택과 실패 시 처리

**우선 검토할 경로는 CAPD의 rigorous C1 solver다.** 논문 §4.1은
`IMap`, `IOdeSolver`, `ITimeMap`, `C1HORect2Set`을 사용하고 §4.2에는 multiprecision
사례도 있다. `exp`와 rational expression은 그 문헌의 arithmetic/AD 예제로 표현 가능함을
확인했다. 실제 enclosure가 `a=0`을 건드리면 이 문제의 RHS 사용 조건은 깨진다.
논문의 toy runtime은 ICE의 120초 실행 가능성을 보장하지 않는다.

[공식 CAPD 저장소](https://github.com/CAPDGroup/CAPD)는 C++ build 경로를 제공한다.
현재 [pyproject.toml](../../pyproject.toml)의 네 Python dependency에 CAPD는 포함되지 않는다.
따라서 현재 환경에서 즉시 실행 가능하거나 설치·통합이 끝났다고 기록하지 않는다.
실제 채택 때는 source revision, build, precision/rounding과 clean runner의 제어면 경로를
고정하고 공통 runtime·artifact 제한 안에서 실행해야 한다. 이번에는 설치·build를 하지 않았다.

대안은 [Lessard–Reinhardt (2014)](https://epubs.siam.org/doi/10.1137/13090883X)의
Chebyshev 계수 공간과 radii-polynomial 방식이다. 논문 abstract는 analytic ODE의
IVP/BVP 해를 contraction으로 인증한다고 명시한다. 이 대안의 상세 정리·구현을 이번에
전부 검토하지 않았으며 추천 1순위로 승격하지 않는다. shooting enclosure의 wrapping이
실제로 병목일 때 별도 설계를 검토할 자료다. 실패했다고 자동으로 두 번째 계산을 돌리지 않는다.

## 4. 새로 명시할 한계: turning point의 좌표 시계

다음은 BDS의 reparametrization 구조와 저장소의 기준 해를 결합한 **해석적 추론**이다.
Phase 24는 중앙에서 `a'=phi'=0`인 reflection-symmetric seed를 공급한다.
그 지점에서 좌표만의 시계 `chi(a,phi)`는

```math
\delta\chi=\epsilon(\chi_a a'+\chi_\phi\phi')=0
```

이므로 그 시계로 reparametrization orbit을 횡단하는 gauge slice를 정의할 수 없다.
full lapse/embedding/phase-space generator까지 0이라는 뜻은 아니다.
local-lapse audit은 full `(x,q,T,r)` Hessian을 검사했으므로 이 주의점이 그 반례를
회피하지도 않는다. 또한 같은 양끝 경계값만으로 모든 root의 reflection symmetry가
증명되는 것은 아니다. 새 BVP 인증이 중앙 시계·FP determinant·gauge-null mode의
인증까지 포함하는 것으로 서술하지 않는다.

classical principal function을 얻더라도 quantum measure는 별도이며,
좌표상의 zero direction 하나만으로 genuine gauge structure를 판정하지 않는다는 점은
BDS §2와 Dittrich–Höhn §5.3의 구분에 부합한다.

## 5. G1에 주는 것과 주지 않는 것

실수 box의 인증은 선택한 국소 branch의 witness다. 원래 ODE와 endpoint map의
복소 근방 holomorphy, 특이점 회피 및 해당 Jacobian의 비퇴화를 정당화하면 국소
holomorphic implicit-function 논의를 할 수 있다. 단순한 실수 root uniqueness만으로
global complex continuation을 얻지는 못한다. 이는 아직 계산한 complex tube가 아니다.

그 이후에도 `n_sigma=<C,K_sigma>`에는 source-defined `C`와 global `K_sigma`가 필요하다.
Stokes에서의 기저 변화, caustic/branch 문제, good end와 orientation을 local germ으로
대체할 수 없다. 따라서 인증 결과를 사용하려는 consumer는
`open:gate1-starobinsky-exact-gauge-preserving-element-source`의 local branch 전제로
한정한다. original-cycle blocker를 해소했다는 graph edge를 만들지 않는다.

보완된 단일 질문은 그대로다. **고정된 boundary의 constrained endpoint map을 실제
연속 flow와 derivative enclosure로 감쌌을 때, 하나의 정해진 box에서 strict inclusion이
성립하는가?** 이번 문헌 검색은 이 질문의 구현 근거와 실패 판정을 구체화했다.

## 검색·검토 기록

- 조회일: 2026-09-06 UTC. CAPD 논문, Rump 저자 PDF, BDS·Dittrich–Höhn·Witten·FLT
  HTML, exact-discrete-Lagrangian PDF의 위 위치를 읽었다. Chebyshev 대안은 publisher
  abstract 수준으로 명시했다. 검색 결과의 인용 횟수를 증거로 쓰지 않았다.
- repository discovery command:
  `./ice literature search 'validated boundary value problems interval Newton Hamiltonian shooting' --json`.
  OpenAlex 조회 시각은 `2026-09-06T10:44:47.271Z`; 결과가 주로 다른 분야여서 증거로 채택하지 않았다.
- 웹 검색어에는 `CAPD DynSys library rigorous numerics dynamical systems C1 time map`,
  `Rump verification methods Krawczyk operator`, `Lessard Reinhardt Chebyshev series`를 사용했다.
  exact-discrete-Lagrangian arXiv HTML 조회 실패 후 PDF를 읽었다.
- 논문별 방법·scope 검토를 세 read-only AI 검토와 대조했다. 새 연구 runner, historical
  replay, dependency 설치 또는 physics 검증을 수행하지 않았다.
- 두 문서의 상대 파일 링크 11개가 존재함을 확인했고, 후속 수식 검토에서 시간 확장,
  Jacobian 행·열 선택과 Krawczyk 가정에 commit을 막는 오류는 발견되지 않았다.
- 이번 변경은 기존 판정의 수정이 아닌 supporting 설계 보완이므로 ontology·repro manifest는
  그대로 둔다. 기존 untracked output 경로도 보존한다.
