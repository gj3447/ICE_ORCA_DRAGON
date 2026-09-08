# KG 연결성 감사: 반복되는 패턴과 빠진 비교

2026-09-08 · 기준 commit `353a35780d4bf37765f015435dd19f36811e0386`.

**빠진 비교 연결 4개를 확인해 보완했다.** 가장 유용한 패턴은, 축약하거나 공간을 바꾸어 얻은 결과에 원래의 정의역·상태 선택·경계·orientation 정보가 자동으로 따라오지는 않는다는 것이다. 이는 여러 기록을 비교해 얻은 **연구 방법상의 해석**이며, 공통 물리 메커니즘의 발견은 아니다.

전체 범위는 네 canonical graph와 기존 collection/intuition 경로다. 정밀 대조는 최근 Starobinsky의 8개 개념과 기존 CPT의 operator/RAQ, lapse 적분, determinant/Pin 자료 사이에서 했다. 모든 가능한 개념쌍을 소스 수준에서 완전 조사했다고 주장하지 않는다. 기존 계산을 재실행하거나 새로운 물리 계산을 설계하지 않았다.

## 1. 연결돼 있다는 것과 설명하는 연결이 있다는 것은 다르다

기준 그래프는 네 programme 각각에서 하나의 weak component를 가진다. 하지만 공통 programme, 문서 또는 논문을 거쳐 갈 수 있다는 사실만으로 두 결과의 수학적 관계가 생기지는 않는다. 특히 지난 [직관 지도](ICE_RESEARCH_INTUITION_KG_MAP_2026-09-07.md)의 문서 artifact는 설명의 허브이지 증거의 허브가 아니다.

비교 경로를 찾을 때는 다음 여섯 관계만 남기고 방향을 무시한 최단 경로를 계산했다.

`ABOUT`, `CONTRASTS_WITH`, `EXTENDS`, `FOLLOW_UP_TO`, `MOTIVATES`, `BLOCKED_BY`.

소속·정책·문서·출처·실행 artifact를 지나는 지름길은 이 검사에서 제외했다. 이 필터도 **발견 후보를 찾기 위한 탐색 조건**일 뿐이다. 역방향 traversal이나 open problem을 통과한 경로는 논리적 함의가 아니며, 짧은 거리는 좋은 연구의 점수가 아니다.

아래 ID는 모두 `cpt::concept:` 접두사를 가진다. 기존의 직접 연결은 네 쌍 모두 0개였다.

| 비교 | 시작 ID | 상대 ID | 기존 최단 경로 | 보완 |
| --- | --- | --- | --- | --- |
| C1: 미분적 제약 소거와 spectral RAQ | `starobinsky-observable-common-domain-and-star-product` | `raw-c-weyl-spectral-raq-bridge-design` | 11 edges | 직접 `CONTRASTS_WITH` |
| C2: 상태 자유도와 operator extension 선택 | `starobinsky-admissible-choice-invariance-versus-state-selection` | `raw-c-constant-boundary-direct-integral` | 11 edges | 직접 `CONTRASTS_WITH` |
| C3: N이라는 기호의 서로 다른 역할 | `starobinsky-source-time-versus-carrier-lapse-coordinate` | `positive-half-lapse-resolvent-versus-projector` | 5 edges | 직접 `CONTRASTS_WITH` |
| C4: 고전 끝점 orientation과 quantum line | `starobinsky-source-boundary-quantization-handoff` | `reduced-bosonic-half-form-versus-fermion-pfaffian-and-pin` | 8 edges | 직접 `CONTRASTS_WITH` |

네 관계는 **어떤 대상을 다른 대상으로 오인하면 안 되는지**를 설명한다. 공통 연산자, 동일한 상태공간, quantum equivalence 또는 증거 이전을 선언하지 않는다. 보완 뒤의 직접 경로 길이 1은 색인 개선만 뜻한다.

## 2. 놓치기 쉬웠던 네 패턴

### C1. 미분 연산을 견디는 공간이 유한 gauge 변환까지 견디는 것은 아니다

최근 Starobinsky의 compact-N carrier에서는 미분적 제약 소거가 가능하다. 하지만 그 사실을 자기수반 제약의 스펙트럼 영점이나 group averaging으로 옮기려면 정의역을 더 확인해야 한다. [관측가능량·접합 소스 검토 §2–3](../../cpt_temporal_folded_susy/STAROBINSKY_OBSERVABLE_SEWING_SOURCE_REVIEW.md)는 이 간격을 명시적 구간 예로 보여준다.

\[
D(P_\theta)=\{u\in H^1(I):u(N_+)=e^{i\theta}u(N_-)\},\qquad
L(u)=\int_Iu\,dN.
\]

Collar 함수에서는 \(L(Pu)=0\)이지만, 전체 확장 정의역에서는

\[
L(P_\theta u)=-i(e^{i\theta}-1)u(N_-).
\]

따라서 같은 형식적 미분식에서도 끝점 조건이 바뀌면 다른 스펙트럼 문제가 된다. Collar는 미분 아래 남지만 유한 translation 아래 보존되지 않는다. 이 비교는 선언한 scalar-phase 구간 확장군에 한정된다. 모든 BFV/RAQ 구현의 불가능성 정리가 아니다. 유한 구간 운동량 확장의 원문은 [Bonneau–Faraut–Valent §5.3](https://arxiv.org/html/quant-ph/0103153)이다.

기존 [raw-C Weyl–spectral–RAQ 설계의 Ordered gates](ICE_RAW_C_WEYL_SPECTRAL_RAQ_BRIDGE_DESIGN_2026-09-01.md)는 별도의 모델에서 extension → spectral transform → invariant test space → rigging product → observable intertwining을 요구한다. 이번 연결은 두 모델의 **서로 다른 미완성 입력**을 직접 비교하게 한다. Raw-C RAQ가 이미 완성됐거나 Starobinsky의 해법이라고 말하지 않는다. 공통 carrier와 관측가능량·수반의 조건에 관한 방법 출처는 [Giulini–Marolf §II.1–II.2](https://arxiv.org/html/gr-qc/9812024)다.

### C2. 양의 내적의 존재, 상태 선택, 표현 선택은 세 질문이다

Starobinsky의 Cauchy-label 구성에는 임의의 smooth positive weight \(w\)가 남는다. 양의성과 선언한 반선형 교환을 만족한다는 조건만으로 \(w\)가 결정되지 않는다. [같은 소스 검토 §4](../../cpt_temporal_folded_susy/STAROBINSKY_OBSERVABLE_SEWING_SOURCE_REVIEW.md)에 구성과 범위가 있다.

Raw-C 쪽에서도 [\(\Gamma_{1,p}=0\) direct-integral extension](../../cpt_temporal_folded_susy/RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL.md)의 경계선은 별도로 선언한 양자화 자료다. Parity, BFV 또는 물리적 경계 원리에서 선택한 결과가 아니다. 두 자유도는 같은 선택군이 아니며, 경계선을 바꾸는 것이 단순 gauge 변환이라는 결론도 없다.

예전 [Phase 23의 P230–P231](../../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md)에도 비슷한 질문이 있었다. 그 toy 모델의 양의 정규화 density는 별도로 공급한 clock/frequency와 preparation operator \(B_L\)을 사용한다. 이 역사적 비교는 독서용으로만 남긴다. 현재 Starobinsky의 \(w\)와 \(B_L\)을 같은 물리 데이터로 잇는 사상은 구성되지 않았다.

**여러 상태가 남는다는 것 자체는 모순이 아니다.** 특정 상태를 이론에서 유도한다는 주장을 하려면 추가 선택 원리가 필요하고, 어떤 선택을 단순 표현의 차이라고 부르려면 정의역과 관측가능량까지 운반하는 동치 사상이 필요하다.

### C3. 같은 N을 적분해도 세 종류의 작업일 수 있다

| 표기 또는 작업 | 실제 대상 | 그 결과만으로 얻지 못하는 것 |
| --- | --- | --- |
| source의 \(N(s)\), \(\int ds\) | 시간에 따른 lapse field와 interval 작용 | 경계 test complex의 contraction |
| \(R_N,J_\chi,K_\chi\) | 고정된 compact boundary coordinate N 위의 선형사상 | gauge-group average, spectral projector |
| half/full-line lapse 적분 | 선언한 제약 연산자 또는 spectral parameter에 대한 함수·분포 | 위 두 구성과의 동일성, 물리적 원래 cycle 선택 |

[Primary reduction](../../cpt_temporal_folded_susy/STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md)의 compact-coordinate 적분을 [Phase 27 §2](../../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md)의 lapse 연산자 적분과 구별해야 한다. 후자에서도 양의 반직선의 damped 적분은 sourced resolvent이고, 전 실수선의 형식적 group average는 constraint-supported distribution이다. 적분 기호와 변수 이름이 같다는 사실은 연결 사상을 대신하지 않는다.

### C4. 끝점의 부호를 맞췄다는 것과 quantum orientation을 구성했다는 것은 다르다

[Source-induced interval BV–BFV §3–3.1](ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md)은 incoming-minus-outgoing의 고전 경계 규약과 bulk 축약 뒤 남는 두 자료를 추적한다.

\[
-[\sigma^+\rho]_{\partial I},\qquad +[\sigma^+\delta N]_{\partial I}.
\]

이는 determinant line의 trivialization, fermion Pfaffian 또는 Pin lift를 구성한 결과가 아니다. 기존 [Phase 37의 Result 및 scope](../../cpt_temporal_folded_susy/PHASE37_CLOSED_FOLD_HOLONOMY.md)도 sampled bosonic half-form의 부호 귀환과 물리적 fermionic/Pin 자료를 구분한다. 두 기록을 직접 비교하면 **부호를 계산한 대상이 무엇인가**를 먼저 묻게 된다. Interval framework의 원문은 [CMW §9.1](https://arxiv.org/html/2012.13270#S9.SS1)이며, 원문 자체가 이 저장소의 quantum CPT kernel을 제공하지는 않는다.

## 3. 연결하지 않은 후보도 결과다

| 후보 패턴 | 판단 | 이유 |
| --- | --- | --- |
| Bulk doublet 축약 ↔ Schur momentum 소거 | 방법 비유만 보존 | 두 축약 모두 남는 자료가 있지만 endpoint primitive와 contour/determinant 자료는 다른 대상이다. 직접 `EXTENDS`나 evidence 관계의 근거가 없다. |
| Bulk endpoint 항 ↔ Galerkin projection remainder | 새 edge 없음 | 생략한 정보라는 표현은 같아도 연산과 잔여항의 mechanism이 다르다. |
| Ward 규제 극한 ↔ raw-C finite Weyl proxy | 새 edge 없음 | 공유한 규제군·극한 위상·비교 사상이 없다. |
| Chain cohomology ↔ selected-H/Mc spectral measure | 새 edge 없음 | 동형사상이나 norm의 비교만으로 제약·정의역·ghost degree를 운반하지 못한다. |
| 네 graph의 representation/selection 문제 | 기존 collection 경로 유지 | 공통 감사 질문이지 공통 물리 메커니즘이 아니다. 이미 choice-invariance와 전체 직관 경로가 있다. |
| 비영 graded pairing ↔ persistent interacting pole | 기존 분리 유지 | 상태·pairing 정보는 pole 자료가 아니다. G4/G5 질문은 이미 별도로 등록돼 있다. |

특히 compact complex의 \(H^2\)와 degree-reversed dual detector의 연결, coefficient-only dual의 top exactness와의 구분, bulk 축약 뒤 두 endpoint 항은 **이미 연결돼 있었다**. 같은 질문 노드나 collection path를 또 만들지 않았다.

## 4. KG 반영 범위와 재검토 기준

기존 concept 사이에 C1–C4의 `CONTRASTS_WITH` 4개를 추가했다. 이 보고서 artifact 하나와 문서 소속·설명 관계 5개를 함께 색인한다. 새 과학 claim/evidence, source, sidecar signal, open problem, execution dependency 또는 reading path는 추가하지 않는다. 기존 node의 판정과 기존 edge는 유지한다.

이 비교를 향후 물리적 연결로 바꾸려면 명시적인 입력·출력 사상이 필요하다. 그 사상은 필요한 support/정의역, 관측가능량과 수반, 내적 또는 경계 자료를 실제로 보존해야 한다. 허용 선택 아래의 불변성과 독립 consumer 검토도 별도다. 현재 G1 original joint cycle/global intersections와 source-compatible quantum boundary state/kernel은 계속 OPEN이다.

변경 후 검증 명령은 `./ice ontology validate`, `./ice ontology review --graph all --base HEAD`, `./ice graphrag diff --base HEAD --limit 12 --json`, `./ice harness check`, `npm run graph:release-check`다. 실행 결과는 이 작업의 completion commit 본문에 기록한다. 구조 검증을 물리학의 참·거짓 판정으로 읽지 않는다.

기준 경로 길이는 다음 read-only 코드로 재확인할 수 있다. 그래프 감사를 위한 코드이며 과학 runner를 실행하지 않는다.

```python
import collections, json, subprocess
g = json.loads(subprocess.check_output([
    "git", "show", "353a357:ontology/cpt-temporal-folded-susy/graph.json"
]))
relations = {"ABOUT", "CONTRASTS_WITH", "EXTENDS", "FOLLOW_UP_TO", "MOTIVATES", "BLOCKED_BY"}
adj = collections.defaultdict(set)
for e in g["edges"]:
    if e["relation"] in relations:
        adj[e["from"]].add(e["to"])
        adj[e["to"]].add(e["from"])
pairs = [
    ("starobinsky-observable-common-domain-and-star-product", "raw-c-weyl-spectral-raq-bridge-design"),
    ("starobinsky-admissible-choice-invariance-versus-state-selection", "raw-c-constant-boundary-direct-integral"),
    ("starobinsky-source-time-versus-carrier-lapse-coordinate", "positive-half-lapse-resolvent-versus-projector"),
    ("starobinsky-source-boundary-quantization-handoff", "reduced-bosonic-half-form-versus-fermion-pfaffian-and-pin"),
]
for a, b in pairs:
    a, b = "concept:" + a, "concept:" + b
    q, distance = collections.deque([a]), {a: 0}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                q.append(v)
    print(distance.get(b))  # 11, 11, 5, 8; None would mean no filtered path.
```
