# 경계항 소거만으로 BFV 불변 시험공간이 정해지지는 않는다

2026-09-07 · SUPPORTING_METHOD / SCOPED_EXACT_RESULT.

**a=2의 Robin 또는 Dirichlet 조건만 모든 ghost 성분에 똑같이 부과하는
smooth 시험공간은 Ω=cH+ρp_N 아래 불변이 아니다.**
복소 경계형식과 실제 Weyl H를 미분해 매끄러운 반례를 구성했고,
기호 검사 17개와 Lean 유한 대수 정리 5개가 통과했다.

이 결과는 앞서 확인한 Ward 경계항의 소거를 뒤집지 않는다. 소거에 쓰는 함수공간을
BFV가 보존하는 상태공간으로 사용하려면 무엇을 더 지정해야 하는지 드러낸다.
자기수반 Robin/Dirichlet 확장이나 모든 BRST domain을 배제하는 결과는 아니다.

## 실제로 추가한 판별

이전과 같은 flat density와 Starobinsky Weyl H를 사용한다. 시험함수는 a=2 이외의
box 면 근방에서 0이다. B_r u=(∂_a−r(φ,N))u|₂로 표기한다.

| 검사 | 도출한 조건 또는 반례 | 의미 |
| --- | --- | --- |
| 모든 복소 boundary trace 쌍의 Green 소거 | r=bar(r) | Real Robin family가 남고 특정 계수는 선택되지 않는다. |
| K:u→bar(u)의 경계조건 보존 | r가 실수 | K는 여기서 kinematic conjugation이며 full CPT lift는 아니다. |
| p_N=−i∂_N이 전체 Robin 시험공간을 보존 | ∂_N r=0 | r=N은 Green/K를 통과해도 p_N에서 실패한다. |
| H가 같은 Robin 시험공간을 보존 | v₃=(a−2)³ηψ에 대해 B_rHv₃=ψ/(8π²)≠0 | 모든 r에 통하는 명시적 반례다. |
| H가 같은 Dirichlet 시험공간을 보존 | v₂=(a−2)²ηψ에 대해 Hv₂|₂=ψ/(24π²)≠0 | Dirichlet로 바꾸는 것만으로 이 ansatz가 수리되지 않는다. |

η는 경계 근방에서 1인 smooth cutoff이며 ψ는 face interior의 비영 smooth compact
함수다. 따라서 반례는 실제 시험함수로 실현된다. 표의 마지막 두 수치는
boundary-condition residual이며 Ward anomaly나 에너지·관측량이 아니다.

직관적으로 경계조건은 함수값과 첫 미분을 묶지만, H를 적용한 함수의 경계조건에는
세 번째 미분까지 들어간다. 처음 조건이 0이라는 사실만으로 새 조건도 0이 되지는 않는다.
Potential과 횡방향 미분을 포함한 실제 H의 전체 판별식은
[해석적 유도 §4](STAROBINSKY_WARD_DOMAIN_DERIVATION.md)에 있다.

## 보완 방향을 어디까지 구체화했는가

검사 대상은 모든 ghost 계수에 같은 D_r^sm을 쓰는 D_r^sm⊗Λ(c,ρ)였다.
이 방식을 유지하려면 조건을 적용할 연산의 범위도 함께 지정해야 한다.
예를 들어 모든 B_rH^k p_N^m u=0인 smooth 함수의 집합을 쓰면
[H,p_N]=0에 의해 H와 p_N 아래 대수적으로 불변이다. 이 집합은 interior compact
tests를 포함하므로 보조 L²(B,flat)에서 조밀한 부분집합을 갖는다.

하지만 그것이 선택한 closed operator의 **graph core**인지, 비영 face trace를
허용하는지, 물리적 BRST cohomology와 양의 내적을 주는지는 아직 미해결이다.
Ghost degree마다 다른 domain을 사용하는 접근도 이번 반례가 배제하지 않는다.
실제 domain 및 quantum CPT trace action을 확보해야 상태·접합으로 넘길 수 있다.

자기수반 연산자도 그 전체 domain을 자기 자신으로 보낼 필요는 없다.
따라서 이 구별은 핵심이다. 문헌상 domain과 연산의 구별은
[Bonneau–Faraut–Valent의 §2·4·7.1](https://arxiv.org/html/quant-ph/0103153),
boundary-form parametrization은
[Asorey–Ibort–Marmo의 §2](https://arxiv.org/html/hep-th/0403048)를 참고했다.
후자의 regular elliptic 정리를 이 indefinite WDW 문제의 자기수반성 증명으로
사용하지 않았다. 문헌의 일반 이론을 이번 모델의 새 발견으로 주장하지 않는다.

## KG 연결과 남은 질문

~~~mermaid
flowchart LR
  Limit["기존: Gaussian pairing → a=2 Green 항"] -->|"허용 시험공간 검토"| Flux["복소 Green 소거: real Robin"]
  Flux -->|"필요하지만 충분하지 않음"| Domain["같은 공간에 Ω를 적용할 수 있는가?"]
  Primary["Primary lapse constraint p_N"] -->|"r_N=0 요구"| Domain
  H["실제 Weyl H의 3차 boundary jet"] -->|"단순 Robin/Dirichlet ansatz 반례"| Domain
  Domain -->|"기존 상태 질문을 구체화"| Open["Closed/graded domain · CPT trace action: OPEN"]
  SA["자기수반 domain과 불변 시험공간의 구별"] --- Domain
~~~

이 연결은 기존 CPT graph의 concept/claim/scope/evidence/artifact/open problem으로
기록한다. Native JSON이 정본이고, 기존 RDF/JSON-LD·PROV-O projection과 SHACL은
기억·출처·형식 검사를 담당한다. 외부 표준 물리 ontology와의 동치를 선언하지 않는다.

기존 읽기 경로:

    ./ice ontology guide --graph cpt --path starobinsky-seam-ward-regulator-removal

경계상태 질문은 부분 해소 상태로 남는다. 원래 적분 경로, G1의 oriented global
intersection vector, 물리적 CPT 위반이나 빅뱅 해석에는 새 evidence가 생기지 않았다.

## 실제 검증

    ./ice run starobinsky_ward_domain
    SCOPED_LOCAL_WARD_CANCELLATION_DOES_NOT_DEFINE_INVARIANT_BFV_TEST_SPACE
    exact controls: 17; Lean theorems: 5
    Robin flux: real r; primary preservation: partial_N r=0
    cubic H boundary residual: psi/(8*pi**2); Dirichlet H trace: psi/(24*pi**2)
    same-space BFV ansatz fails; no self-adjointness no-go or physical CPT conclusion

Exit 0, elapsed 3.398441942874342 s. Source commit
`b48948bed6ef1efe1200d36acc9ed10c8574ed58`.
Python 3.13.5, SymPy 1.14.0, Lean 4.33.0,
mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.
실행·환경·hash·check 및 axiom audit 정본은
[raw result](STAROBINSKY_WARD_DOMAIN_RESULT.json)이다.

[Lean](../formal/cpt_sewing/CptSewing/WardDomain.lean)은 finite complex flux와
real normal jets만 검증한다. 함수공간 결론은 pinned analytic derivation 및 독립
수학 읽기 검토가 담당한다. 수치 근사나 tolerance sweep은 사용하지 않았다.
