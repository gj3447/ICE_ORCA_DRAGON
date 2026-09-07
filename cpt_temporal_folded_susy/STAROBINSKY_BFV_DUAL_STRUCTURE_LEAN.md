# BFV 시험공간·쌍대 제약·양의 몫공간의 Lean 4 정리

2026-09-07 · SUPPORTING_METHOD · 조건부 대수 정리의 형식 검증.

**기존의 복소수 계수 대수 4개에서, 실제 추상 벡터공간·선형 제약·몫공간을
다루는 Lean 정리 36개로 확장했다.** 세 모듈 모두 Lean 4.33.0 커널 검증과
axiom audit를 통과했다. 이전 Cauchy 해석 증명을 Lean으로 모두 옮겼다는 뜻은 아니다.
그 증명이 제공해야 하는 가정을 정리의 인자로 드러내고, 그 이후의 대수적 추론을
형식화했다.

질문: 어떤 명시적 가정에서 repaired carrier, 비영 constrained dual, 선택한 양의
quotient와 kinematic conjugation이 이어지는가?
출력: 세 모듈의 kernel-checked theorem bundle.
비주장: actual PDE/Green 적분 증명·선택된 물리 내적·full CPT 접합·G1 진전.
Planner 분류는 `INSUFFICIENT_ROUTE_EVIDENCE`였으며 supporting formalization으로
진행했다. Choice-invariance path도 읽었고 선택된 seed나 form의 물리적 유일성을
추가로 주장하지 않았다.

## 세 파일이 증명하는 내용

| Lean 모듈 | 검증한 정리 | 중요한 입력·범위 |
|---|---|---|
| [BFVCore.lean](../formal/cpt_sewing/CptSewing/BFVCore.lean) | 반복 경계조건의 안정성과 최대성, minimal complex의 제곱 0, primary가 단사이면 degree-zero cycles가 0 | 추상 경계 함수와 연산자; H,p의 가환성이나 p의 단사성을 필요할 때 명시 |
| [ConstrainedDual.lean](../formal/cpt_sewing/CptSewing/ConstrainedDual.lean) | 두 constraint range의 span 소거, form의 양쪽 제약 소거, 양의 witness, 다른 kernel, Green/on-shell에서 비영 constrained dual | 선택한 bulk s의 Green 관계·on-shell·nonzero witness |
| [DualQuotient.lean](../formal/cpt_sewing/CptSewing/DualQuotient.lean) | 실제 Φ/ker T, T≠0이면 C와 선형동형, 양의 sesquilinear form, K의 quotient 하강·involution·covariance | 비영 복소 선형함수; K covariance와 involution은 명시 가정 |

### 1. 경계조건의 반복으로 안정한 carrier를 정의한다

`repairedCore H p boundary z`는 모든 k,m에 대해
boundary(H^[k](p^[m](v)))=z인 원소의 집합이다. Lean은 p 안정성,
H와 p가 가환할 때 H 안정성, 그리고 같은 경계조건을 만족하는 모든 공통 불변
집합이 이 core에 포함됨을 증명한다. 이는 집합과 함수에 관한 정확한 결과다.
실제 differential operator의 closed domain이나 graph norm을 구성하지 않는다.

Minimal coefficient complex는
d0(v)=(Hv,pv), d1(α,β)=Hβ−pα로 정의된다.
`minimal_complex_square_zero`는 가환성에서 d1(d0(v))=0을 증명한다.
`degree_zero_trivial_of_primary_injective`는 primary 단사성을 가정해 d0(v)=0↔v=0을
증명한다. 실제 compact N-collar가 그 단사성을 준다는 해석적 논증은
[이전 audit](STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md)에 남아 있다.

### 2. 실제 쌍대 함수 타입과 제약을 연결한다

`constrainedDual H p`는 복소 선형 쌍대공간에서 T∘H=T∘p=0인 submodule이다.
핵심 정리 `pairing_onShell_nonzero_constrainedDual`은 다음 결론을 준다.

```lean
∃ T ∈ constrainedDual H p, T ≠ 0
```

이를 얻기 위해 `pair : S →ₗ[ℂ] Module.Dual ℂ V`, bulk vector s, witness w와 함께
다음 입력을 요구한다.

- `greenH`: 모든 시험함수 u에 대해 pair(s)(Hu)=pair(As)(u).
- `greenP`: 모든 시험함수 u에 대해 pair(s)(pu)=−pair(Bs)(u).
- `onShellH`, `onShellP`: As=0, Bs=0.
- `witness`: pair(s)(w)≠0.

Green 입력은 **선택한 s에 대해서만** 요구한다. 모든 bulk vector가 Neumann 조건을
유지한다고 전제하지 않으므로 이전의 H-domain 반례와 충돌하지 않는다.
이 입력들이 실제 Cauchy 해와 적분에 대해 성립한다는 증명은
[유도문 §§2–3](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md)의 해석적 부분이다.

### 3. scalar 예시를 넘어 실제 몫공간을 만든다

`StateQuotient T`는 정의상 `V ⧸ LinearMap.ker T`다.
`quotientFunctional`은 대표 선택과 무관하며 단사다. T≠0이면 T가 C로 전사임을
증명하고 `quotientEquivComplex T hT`로 실제 선형동형을 구성한다.

그 quotient 위 form은
F(q,r)=conj(quotientFunctional(T)(q))·quotientFunctional(T)(r)다.
Lean은 오른쪽 선형성, 왼쪽 켤레선형성, Hermitian 대칭, diagonal 비음성,
F(q,q).re=0↔q=0을 각각 증명한다. 이는 양의 sesquilinear form이며, 선택된
물리 Hilbert 공간의 instance나 observable representation은 정의하지 않았다.

T(Kv)=conj(Tv)가 주어지면 kernel 관계가 보존됨을 증명한다. 따라서 K가 quotient에
내려가고, 대표의 involution을 가정하면 quotient에서도 involution이며 form은
켤레 covariance를 만족한다. Full CPT의 ghosts, boundary orientation 및 sewing
kernel은 이 K에 포함되지 않는다.

## 검증 경계와 실행 기록

이전 [Cauchy 결과](STAROBINSKY_DUAL_CAUCHY.md)의 PDE 존재·유일성·finite propagation,
seed injectivity, 실제 적분의 Green 소거, 전체 R_φ KG form의 영성은 이번 Lean
정리의 결론이 아니다. 실제 Weyl operator를 위 추상 타입들로 완전히 실현하는 작업도
남아 있다. 따라서 KG-zero claim에 새로운 Lean evidence를 붙이지 않는다.

실행 명령은 `./ice run starobinsky_bfv_dual_structure_lean`이다.
최종 결과는 `SCOPED_LEAN_BFV_DUAL_STRUCTURE_WITH_EXPLICIT_ANALYTIC_HYPOTHESES`이며,
BFVCore **7/7**, ConstrainedDual **12/12**, DualQuotient **17/17**, 총 **36/36**이다.
`sorry`/`admit`/새 local axiom을 허용하지 않았고, 사용된 axiom을
`propext`, `Classical.choice`, `Quot.sound` 범위로 감사했다. Warning-as-error를 유지했다.

첫 source `c95d64b`의 실제 audit에서는 ConstrainedDual 12개만 통과했다.
BFVCore의 불필요한 `change`, quotient API의 대표 인자 누락, unused simp 인자와
중첩 conjugation subtraction rewrite를 수정했다. 수정 source `c0e57c8` 뒤 재시도는
untracked 실패 JSON 때문에 제어면에서 실행 전에 차단됐다. 해당 자체 생성 진단을
임시 보관하고 깨끗한 core에서 정식 명령으로 최종 검증했다. 최초 compiler 실패를
수학적 반례나 통과 결과로 보고하지 않는다.

[Raw result](STAROBINSKY_BFV_DUAL_STRUCTURE_LEAN_RESULT.json)가 최종 실제 명령·시간·환경·
source commit·hash·각 theorem signature와 axiom 결과의 단일 ledger다.
[Proof index](../formal/cpt_sewing/bfv-dual-structure-proof-index.json)와
[runner](starobinsky_bfv_dual_structure_lean.py)는 누락된 theorem을 거부한다.
기존 scalar proof와 역사적 raw result는 수정하지 않았다.

주된 실패원인은 `inference`다. Control은 (1) 가정이 드러나는 theorem signature,
(2) 모든 theorem의 kernel/axiom 및 strict warning 검사, (3) 모듈 경계와 이전
해석적 논증에 대한 독립 코드 검토다. 검증 통과는 이 조건부 대수 추론의 성공이며
실제 물리적 선택이나 새 과학적 발견을 뜻하지 않는다.
