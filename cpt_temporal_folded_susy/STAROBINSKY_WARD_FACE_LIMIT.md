# a=2 경계에서는 Gaussian 규제를 제거해도 시험함수 의존 Ward 항이 남는다

2026-09-07 · SUPPORTING_METHOD / SCOPED_ANALYTIC_RESULT.

선언한 실수 smooth compact 시험함수에 적분한 전체 Ward 잔여항은 Gaussian 폭을
없애면 **a=2 Green 경계형식**으로 수렴한다. 명시한 정규화 시험함수 쌍의 극한은
**-1/(48*pi^2)**이고, 같은 Dirichlet 또는 같은 real Robin 조건의 쌍에서는 **0**이다.
기호 검산 18/18, Lean 경계대수 정리 5/5가 실제로 통과했다.

이는 hard field-coordinate cutoff가 남기는 시험함수 의존 경계함수다.
물리적 BFV 상태, 자기수반 domain, 빅뱅의 경계 작용이나 원래 적분 경로를 만든 결과가 아니다.

## 무엇을 실제로 계산·증명했는가

기존 Weyl/flat-density Starobinsky H, box B와 Gaussian D_tau를 고정하고
F_tau=chi_B(q1)chi_B(q2)D_tau(q1-q2)를 사용했다.
u,v는 a=2 면에만 닿는 실수 C_c-infinity ambient test functions다.
Berezin dual도 선언하여 실제 nonzero constraint-ghost 성분을 읽었다.

\[
\mathcal B_\tau[u,v]
=\langle(H_1-H_2)F_\tau,u\otimes v\rangle
\longrightarrow
-{1\over48\pi^2}\int(u\partial_av-v\partial_au)|_{a=2}\,d\phi\,dN.
\]

분포 도함수를 시험함수로 옮긴 뒤 Gaussian의 절대 일차 모멘트와 box overlap을
이용했다. A(x,y)=(Hu)(x)v(y)-u(x)(Hv)(y),
L=max|partial_{y_i}A|, M0=max|A(q,q)|에 대해

\[
|\mathcal B_\tau-\mathcal B_0|
\leq \left({189\over8}L+{99\over8}M_0\right)\sqrt{2\tau/\pi}.
\]

상계는 각 고정된 시험함수 쌍에 적용된다. Operator-norm 수렴이나 a=0까지의
continuum completion은 아니다. 전체 pairing의 극한에 1/2를 추가할 이유는 없으며,
개별 face delta/delta-prime 항을 상쇄 전에 따로 극한으로 옮기지 않았다.

| 시험함수 조건 | 적분 Ward 극한 |
| --- | --- |
| 모든 경계 근방에서 0인 interior pair | 0 |
| u=eta psi, v=(a-1)eta psi; eta=1 near a=2, integral psi^2=1 | -1/(48*pi^2) |
| Common Dirichlet, 두 경계값이 0 | 0 |
| Common real Robin, u_a=r u 및 v_a=r v | 0 |

명시적인 C-infinity eta와 psi, 서로 다른 두 Robin 시험함수, 방향 부호 및 전체 유도는
[해석적 유도](STAROBINSKY_WARD_FACE_LIMIT_DERIVATION.md)에 있다.
이 표의 경계조건들은 서로 다른 진단 조건이다. 같은 물리 내용을 나타내는 선택군이라고
증명하지 않았으므로 이것을 choice-invariance 통과로 기록하지 않는다.

## 검증 범위

- [Runner](starobinsky_ward_face_limit.py): 실제 Weyl operator 미분, Green identity,
  ghost dual, Gaussian moment와 overlap algebra, 비영 예시 및 경계조건 대조.
- [Lean](../formal/cpt_sewing/CptSewing/WardFace.lean): 경계 jet의 antisymmetry,
  Dirichlet/Robin 소거 및 upper-face 비영 계수. 분포극한 정리는 Lean 범위 밖이다.
- 해석적 수렴 증명: source commit에 고정된 유도 문서. 독립 수학 읽기 감사로
  compact support, formal transpose, O(sqrt(tau)) 상수와 부호를 검토했다.

실제 명령과 출력:

    ./ice run starobinsky_ward_face_limit
    SCOPED_A2_WARD_LIMIT_EQUALS_GREEN_FACE_FUNCTIONAL
    exact controls: 18; Lean theorems: 5
    a=2 normalized test witness: -1/(48*pi**2); common Dirichlet/real Robin limit: 0
    analytic paired error <= (189*L/8+99*M0/8)*sqrt(2*tau/pi); no physical source or cycle

Exit 0, elapsed 4.116181204095483 s, source commit
015dec477f28da101804ce5bd197b20dcbcdf5f7. Python/SymPy 환경, Lean 4.33.0/mathlib pin,
source hashes와 실제 정리별 axiom audit는
[raw result](STAROBINSKY_WARD_FACE_LIMIT_RESULT.json)가 단일 정본이다.
수치 quadrature나 tolerance sweep은 사용하지 않았다.

## KG에서의 연결

~~~mermaid
flowchart LR
  Finite["기존: 모든 양의 폭에서 exact closure 실패"] -->|"후속 극한 질문"| Weak["이번: 시험함수 pairing과 O(sqrt tau) 수렴"]
  Weak -->|"극한을 결정"| Green["a=2 Green 경계형식"]
  Green -->|"경계 jets에 따라"| Cases["비영 예시 / Dirichlet·Robin 소거"]
  Point["점별 값과 분포극한의 구별"] --- Weak
  Lapse["N=0 lapse contact"] -. "다른 경계 객체" .- Green
  Green -->|"한 면 사례만 해소"| Open["다른 면·domain·물리 상태·full BFV source: OPEN"]
~~~

Canonical CPT graph는 concept/claim/evidence/scope/artifact/open problem을 구분한다.
기존 finite-width contradiction은 유지하고 경계상태·경계극한 질문 두 개를 한 면의
부분 해소로 갱신한다. 다른 ontology graph의 결과를 evidence로 합치지 않는다.

기존 RDF named-dataset / JSON-LD 1.1 projection과 PROV-O 출처 표현을 사용하고
SHACL로 typed graph를 검사한다. 연구 개념은 ICE local vocabulary이며 외부 표준
물리 온톨로지와 동치라고 선언하지 않는다.
[SHACL](https://www.w3.org/TR/shacl/)은 RDF 조건 검사,
[PROV-O](https://www.w3.org/TR/prov-o/)는 출처 표현의 표준이지 과학적 참의 판정이 아니다.

읽기 경로:

    ./ice ontology guide --graph cpt --path starobinsky-seam-ward-regulator-removal

물리적 해석에는 같은 모델의 full BFV source, physical state/product와 관측량이 여전히
필요하다. 이 계산으로 원래 경로, G1 global intersection vector 또는 TOE가 완성되지는 않는다.
