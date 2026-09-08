# Starobinsky: 두 가지 고전적 relative primary 경계 축약

2026-09-08 · `SUPPORTING_METHOD`

**첫 번째 단계의 결과:** 실제 고전적 BFV 경계 자료와 bulk 분해 뒤 남은 두
끝점 항을 함께 보존하는 축약 관계 두 개를 구성했다. 두 관계의 특성 방향을
몫내면 같은 matter/minimal BFV 경계공간을 얻는다. 물리적 상태공간이나 양자
CPT 접합을 구성했다는 결론은 아니다.

## 무엇을 만들었나

고정한 source chart에서
\(\Omega_{\rm ext}=cH_L+\rho\Pi\),
\(\alpha_{\rm ext}=p_a\delta a+p_\phi\delta\phi+\Pi\delta N+
\bar\rho\delta c+\bar c\delta\rho\)이며,
\(QN=-\rho,\ Q\bar c=\Pi,\ Q\Pi=Q\rho=0\)이다.

| 선택한 경계조건 | 허용 변분과 source 항 소거 | 몫내는 primary 방향 |
| --- | --- | --- |
| \(M:\Pi=\bar c=0\) | \(\bar c=0\)이 두 항을 모두 소거 | \(N,\rho\) |
| \(P(N_0):N=N_0,\rho=0\) | \(\rho=0\)이 작용 항을 소거하고 \(\delta N=\delta\rho=0\)이 one-form pullback을 고정 | \(\Pi,\bar c\) |

여기서 \(N_0\)는 chart 안에 선언한 끝점 자료다. 양의 lapse body chart에서는
\(N_0>0\)로 잡는다. 이 계산이 그 값을 물리적으로 선택하지는 않는다.

공통 축약 대상은
\[
\mathcal B_{\rm red}=(a,\phi;p_a,p_\phi\mid c,\bar\rho),\quad
\alpha_{\rm red}=p_a\delta a+p_\phi\delta\phi+\bar\rho\delta c,
\quad \Omega_{\rm red}=cH_L.
\]
포함사상 \(\iota_X\)와 특성 몫사상 \(r_X\), \(X=M,P\), 에 대해
\[
\iota_X^*\alpha_{\rm ext}=r_X^*\alpha_{\rm red},\quad
\iota_X^*\Omega_{\rm ext}=r_X^*\Omega_{\rm red},\quad
dr_X Q_{\rm ext}=Q_{\rm red}\circ r_X
\]
를 확인했다. 전체 경계조건은 coisotropic이다. Primary 부분과
\(\mathcal B_{\rm ext}^{-}\times\mathcal B_{\rm red}\) 안의 축약 그래프가
graded Lagrangian이며, 물질 부분까지 포함한 전체 경계조건을 Lagrangian이라고
부르지 않는다.

```mermaid
flowchart LR
  S["source의 두 끝점 항"] --> M["Π = bar c = 0"]
  S --> P["N = N₀, ρ = 0"]
  M -->|"특성 방향의 몫"| R["같은 고전적 B_red, α_red, Ω_red"]
  P -->|"특성 방향의 몫"| R
  R -. "양자화 자료와 실제 비교사상 필요" .-> Q["양자 경계공간 · 연산자 · 접합"]
```

## 어떤 잘못된 연결을 차단했나

Source 식의 \(\bar c=-\sigma^+\)를 사용하면 남는 항은
\(+[\bar c\rho]_{s_-}^{s_+}\)와
\(-[\bar c\delta N]_{s_-}^{s_+}\)이다.

* \(\bar c=0\) 하나만 두어도 두 항은 사라지지만,
  \(Q\bar c=\Pi\) 때문에 BFV 보존은 실패할 수 있다.
* \(\rho=0\) 하나만 두면 작용 항만 사라지고
  \(-\bar c\delta N\)가 남는다. 비영인 formal odd generator와
  \(\delta N=1\)이 명시적 반례다.
* \(N=N_0\)만 두면 \(QN=-\rho\)가 경계조건을 깨뜨릴 수 있다.

따라서 **작용의 경계항, BV one-form의 허용 변분, Q의 접선성**을 함께 봐야 한다.
두 선택은 이 세 조건을 실제로 만족하는 예이며 모든 경계조건의 분류는 아니다.
Matter 제약은 아직 남는다. 예를 들어 축약 대상에서도
\(a=1,\phi=p_a=p_\phi=0\)이면 \(H_L=-6\pi^2\ne0\)이다.

## 검증과 재현

실행 명령은 `./ice run starobinsky_relative_primary_boundary`이며
[현재 raw result](./STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY_RESULT.json)가 전체 검사와
입력 hash·환경·Lean 진단의 단일 정본이다.

* 최종 source commit: `de866944face31542e27e74880b7eea02161bc5e`.
* 최종 상태: `SCOPED_TWO_CLASSICAL_RELATIVE_PRIMARY_REDUCTIONS`.
* 관측한 exact symbolic 검사: 40/40 통과.
* Lean 4.33.0 정리: 13개, warning-as-error 및 전이적 axiom 검사 통과.
* 최종 실행 시간: 28.047초. 수치 근사나 PDE 적분은 수행하지 않았다.

첫 실행은 40개 symbolic 검사를 통과했지만 Lean의 덧셈 순서 증명과 unused simp
인자에서 실패했다. 그 raw는 `87a746f`에 보존되어 있다. 두 번째 실행은 증명
목표를 닫았으나 분기별 unused simp 경고 6개로 거부되었고 raw는 `de86694`에
보존했다. 실제로 불필요한 인자를 제거한 세 번째 실행이 최종 통과했으며, 경고나
허용 axiom 기준을 완화하지 않았다. 같은 runner의 재실행은 수정 후 검증이며
독립적인 물리 증거가 아니다.

[Lean 모듈](../formal/cpt_sewing/CptSewing/RelativePrimaryBoundary.lean)은 복소수
계수로 된 선형 generator 모델의 nilpotence, 두 불변 부분공간, 가환하는 투영과
one-form 계수만 증명한다. Odd 변수의 실제 Grassmann 곱은 별도의 graded
symbolic 검사에서 다룬다. \(P\)의 zero tangent one-form 검사는 선언한
\(\delta N=\delta\rho=0\)를 대입한 항등식이며 독립적인 해석학 정리가 아니다.
기하학적 특성 몫과 canonical relation의 차원 논증은
[유도문](./STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY_DERIVATION.md) §§3–6에 있다.

주 실패 원인은 `inference`로 잡고 관련 통제 세 묶음만 사용했다: graded Q와
투영, 상대 경계 pullback과 특성 block, 단일 조건의 반례. 별도 검토자는 실제
source 부호, superdimension과 고전적/양자적 대상의 구분을 대조했다. 이것은
독립적인 source/PDE/양자 적분 재현을 뜻하지 않는다.

## 남은 순서와 연결 범위

다음 질문은 이 고전적 관계에 맞는 **polarization, 측도·half-density,
잔여장과 gauge-fixing 자료가 실제 양자 경계 연산자를 만드는가**이다.
그 연산자와 기존 compact-\(N\) test complex 사이에는 별도의 quantum chain map이
필요하다. 이 차이가 해소되기 전에는 기존 \(R_N,J_\chi,K_\chi\)를 지금의
고전적 \(r_M,r_P\)와 같은 사상으로 부를 수 없다. 두 고전적 몫이 같다는 사실만으로
기존 top cohomology를 없애거나 physical ghost degree를 재지정하지 않는다.

관측가능량·내적의 양립성과 실제 CPT 접합은 이 양자 입력 다음에 검사해야 한다.
비유일성 자체는 실패가 아니며, 선언한 선택들을 비교할 대상과 조건이 먼저 필요하다.

`open:starobinsky-seam-ward-boundary-state-limit`에서 선택한 고전적 relative
reduction 한 부분만 진전시켰다. Planner의 검색어 기반 `CURRENT_BLOCKER_CANDIDATE`
표시는 부정문 속 original cycle/intersection 용어에도 반응했으므로 직접 분류를
검토해 `SUPPORTING_METHOD`로 유지했다. 원래 joint cycle, 전 saddle/sheet/end
census와 signed intersection vector를 만들지 않았으므로 G1→G2→G3→G4→G5와
full-theory/empirical review의 종료 조건은 이번 결과로 바뀌지 않는다.

Source convention은 [CMW §§8–9.1](https://arxiv.org/html/2012.13270#S9.SS1)와
[기존 local source 유도](../docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md)를
사용했다. 고전적 boundary 자료와 양자화의 추가 입력 구분은
[CMR quantum BV–BFV](https://arxiv.org/html/1507.01221#S2.SS1)와 대조했다.
