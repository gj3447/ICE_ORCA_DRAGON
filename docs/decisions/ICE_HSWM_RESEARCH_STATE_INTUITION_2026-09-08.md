# HSWM 연구 상태와 직관을 만드는 역할 관계

2026-09-08 · `SUPPORTING_METHOD` · 실제 연구를 소비자로 둔 인터페이스 확장.

HSWM에 연구 질문의 종류만 넘기던 v1 위에 **출처를 고정한 가정·반례·누락 객체와
여러 입력을 함께 요구하는 관계**를 얹었다. 이 상태는 실제 HSWM 중첩 router에
domain/map/obstruction 문맥을 공급한다. LLM 셀은 그 객체들을 연결한 가설, 이유,
반증 조건과 하나의 다음 검사를 구조화된 JSON으로 돌려준다.

이 확장이 원래 HSWM의 최종 형태를 충족했다는 뜻은 아니다. 원래 목표는 LLM token에서
역할을 가진 n-ary traversal과 trajectory를 만들고, 검토한 결과가 소유권 있는 관계
수정과 다음 행동 변화로 이어지는 진화하는 macro-neural hypergraph/world model이다.
이를 고정된 연구 절차로 재정의하지 않는다. 이번 구현은 그 목표 중 **역할이 드러나는
연구 입력, 상태를 읽는 중첩 선택, 추적 가능한 제안**을 ICE에서 먼저 사용할 수 있게 한다.

## 원래 계획과 이번 구현의 대응

| 원래 HSWM 방향 | 이번에 실제 사용하는 것 | 아직 검증하지 않은 것 |
| --- | --- | --- |
| 역할을 가진 n-ary 관계 | 각 입력에 role을 붙인 `requires/motivates/obstructs/analogy`, 공동 전제·소비자·반증 조건 | 관계 의미의 학습, 연속 Θ/R 표현 또는 인과성 |
| 재귀적·중첩된 구성 | HSWM의 `researcher → semantic-review → command cell` 실제 호출 | 자율적 위계 발명, HSWM-of-HSWMs 완성 |
| 상태에 따라 다른 행동 | domain/map/obstruction을 읽는 실제 guard와 route 선택 | 학습이 선택을 개선했다는 비교 실험 |
| 결과→검토→수정 | 실제 trajectory와 명시적 useful feedback, relation revision | 독립 인과 credit, LLM 가중치 갱신 |
| 직관적 연결 생성 | 기존 객체 2개 이상을 연결한 LLM 가설·설명·반증 조건·읽기 순서 | 새 topology의 자동 채택, 물리적 발견 또는 KG 대비 우월성 |

대조한 원래 계획은 sibling `HSWM/docs/canon/HSWM_CONSTITUTION_2026-08-20.md`,
`HSWM/docs/canon/HSWM_ADAPTIVE_RESEARCH_STRATEGY_2026-08-30.md`,
`HSWM/docs/research/HSWM_FRACTAL_SCIENTIFIC_CONNECTIONS_2026-08-28.md`와 README다.
이들은 목표와 구현 경계를 읽는 자료다. 이번 작업은 sibling 소스를 수정하지 않는다.

## 연구 상태를 읽는 방법

첫 소비자는 [primary boundary 연구 지도](../research/ICE_HSWM_BOUNDARY_INTUITION_2026-09-08.md)와
[검토한 상태 파일](../../research/hswm/primary-boundary-state.v1.json)이다. 상태는 12개 객체,
6개 역할 관계, SHA-256으로 고정한 5개 출처와 기존 CPT anchor를 가진다. 출처의 보고를
정리한 상태이며, hash 검증이 그 보고를 독립 증명하거나 모든 출처를 새로 읽는 것은 아니다.

```bash
./ice research intuition research/hswm/primary-boundary-state.v1.json
./ice research intuition research/hswm/primary-boundary-state.v1.json \
  --without quantum-boundary-tuple --json
```

`intuition`은 어떤 전제를 **함께** 요구하는지, 빠진 입력, 다음 소비자, 관계의 이유와
반증 조건을 Mermaid와 문장으로 펼친다. `INPUTS_PRESENT`는 알려진 입력이 있다는 뜻이다.
관계의 출력은 여전히 `missing`일 수 있다. 후보가 전제로 쓰이면 `CONDITIONAL`이며,
`analogy`는 탐색용이다. 어느 표기도 결론을 자동 승격하지 않는다.

`--without`은 해당 기록을 가상으로 빼는 검사다. 기존의 `missing` 진단을 제거하면
`unknown`이 된다. 객체가 없다는 증거, 실제 boundary condition 변경, 과학적 반증 또는
인과 개입은 아니다. 원본 상태 파일·canonical ontology는 바뀌지 않는다.

실제 HSWM `plan --cell semantic-review`에서 확인한 두 선택은 다음과 같다.

| 상태 | domain / map / obstruction | 실제 선택 |
| --- | --- | --- |
| 원본 | missing / missing / present | `relation:declare-domain` → `domain` |
| domain 기록 가상 제거 | unknown / missing / present | `relation:recover-domain-context` → `connections` |

현재 v2 조건은 상호 배타적이다. HSWM이 `LEARNED_CONTEXTUAL_SCORE`를 출력해도 이
두 선택의 차이는 선언한 guard의 효과다. feedback이 학습된 직관을 만들었다고 읽지 않는다.
초기 `predicted_success=0.5`도 물리적 확률이나 유용성의 측정치가 아니다.

## 실행과 상태 보존

```bash
./ice research run "<한 boundary-state 질문>" \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit \
  --state-file research/hswm/primary-boundary-state.v1.json \
  --reference cpt_temporal_folded_susy/STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY.md \
  --mode investigate --tier supporting --budget 600 --json
./ice research state --profile v2 --json
./ice research graph --profile v2 --json
./ice research feedback EPISODE --useful true --source "검토 근거" --json
```

v2 manifest는 `config/hswm-research.v2.json`, DB는
`.ice/hswm-research/runtime.v2.sqlite3`다. v1 manifest와 `runtime.sqlite3`를 보존한다.
feedback은 episode의 invocation에서 profile을 읽는다.

실제 route는 `references → semantic-review → synthesize`다. 중첩 router가 정의역,
비교사상, 알려진 장애물 또는 문맥 복구 셀 중 하나를 선택한다. 명시한 compute mode만
`./ice run` 셀을 추가한다. 이 supporting state profile은 core tier와 결합할 수 없다.

모든 semantic cell은 state 파일의 SHA-256, 선언한 출처 hash, 같은 graph의 실제
anchor를 다시 확인한다. USL이 준비한 `--reference` 파일도 LLM 셀에서 재확인한다.
LLM에 제공하는 것은 검토한 전체 상태와 사용자가 지정한 참조의 제한된 원문 발췌다.
파일을 읽었다는 provenance와 모델의 의미 이해는 서로 다른 검증이다.

출력은 `ice-research-proposal/v1`이다. 기존 객체 ID만 참조할 수 있고, 각 연결에
공동 전제·추가 가정·이유·반증 조건, 그리고 `HYPOTHESIS`/`QUESTION`을 요구한다.
parser는 알 수 없는 객체·승격 상태·추가 필드·중복 참조를 거부한다. 이 구조를 통과해도
내용은 과학적으로 틀릴 수 있으므로 source와 대조한다. 모델이 state나 ontology에
직접 새 객체를 쓰지는 않는다.

## 관측한 실패

최초 v2 회차 `cf5eb529-9e05-4811-9fe4-f9124e3c1fe0`는 USL 참조 준비 뒤 model service의
`invalid_json_schema`로 실패했다. `uniqueItems`가 지원되지 않는다는 실제 400 오류를
보존했다. 전송 schema에서만 그 키를 제거했고, 로컬 parser의 중복 검사는 유지했다.
실패 회차를 유용한 연구 결과로 피드백하지 않았다.

두 번째 `1122b46d-624c-4821-af7f-47f3608c69cf`는 실제 JSON 제안을 얻었지만,
중복 가정 ID 때문에 로컬 parser에서 거부됐다. 같은 원문에 존재하지 않는 세부 객체 ID도
있었다. 이후 provider schema의 ID를 state의 실제 객체 enum으로 한정하고, 중복 금지와
두 연결 이내의 응답을 명시했다. 거부된 raw JSON도 로컬 episode에 보존한다. 이 실패는
형식을 제한해도 모델이 올바른 연구 관계를 만든다고 보장할 수 없음을 보여준다.

## 완료 범위

이 상태 지도는 기존 결과를 재배열해 다음 연구 검토에 공급한다. 과학적 claim·scope·G1
지위를 바꾸지 않으므로 새로운 evidence edge를 만들지 않는다. 정책 파일 변경에 따른
기존 policy hash만 갱신한다. 전체 graph 검사는 공학적 회귀 검사이며 물리적 판단이 아니다.
실제 연구 회차의 산출물과 검토 결과는 아래 실행 기록에서 별도로 다룬다.

## 실제 회차와 연구 결과

```bash
./ice research run 'P(N0) 고전적 축약 하나에서 양자 경계 carrier·정의역·ghost 차수와 U_P 후보를 명시하라. N=N0 평가와 rho 성분 제거를 쓴 후보가 BFV chain-map 검사를 통과해도 기존 compact-N 비영 top class와 detector pairing을 보존하는지 공격하라. 기존 적분 contraction과 어떤 입력이 달라지는지, 하나의 판별 검사를 구체적으로 써라.' \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit \
  --state-file research/hswm/primary-boundary-state.v1.json \
  --reference cpt_temporal_folded_susy/STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY.md \
  --reference cpt_temporal_folded_susy/STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md \
  --reference cpt_temporal_folded_susy/STAROBINSKY_PRIMARY_REDUCTION_GRADED_SEWING.md \
  --mode investigate --tier supporting --budget 600 --json
```

- Episode `c8247949-b803-4620-9c2e-b235d86330d3`: `SUCCEEDED`, 222.48561781039461초.
- 실제 leaf 호출 3개: `references`, `domain`, `synthesize`. router 포함 trajectory 5개.
- 실제 root 선택 `relation:research-with-state`; 중첩 선택 `relation:declare-domain`.
- USL 선언·선택 자원 5개, resolver call 5회, 거부 0개.
- Codex `0.153.4`, 설치 설정의 `gpt-6-astra`, reasoning effort `low`.
- Manifest bytes SHA-256: `03657c8c0b5cb748047ad52bf2a940803b770b33c546059306cbd5de0802b10a`.
- State bytes SHA-256: `5a97e3f3af6fa6633d4fc33473edea27d7b3219dd41d9b93ebca219783ddbf2d`.
- 보존한 [최종 모델 제안 원문](../../research/hswm/primary-boundary-pilot-proposal.v1.json)
  SHA-256: `eca99a34db160b9085d2401bd3e8325d001d7f043fd271faaf8b9dbc7e05c1f2`.

원문은 수정하지 않았다. 전체 prompt·원문 발췌·runtime interface fingerprints·각 stage 출력과
실패는 `.ice/hswm-research/episodes/<episode>/`에 있다. 여기의 Git 제안 원문은 가설 기록이지
계산 RESULT나 ontology evidence가 아니다. LLM 호출은 같은 텍스트의 재생성을 보장하지 않는다.

제안은 점 평가와 rho 제거를 함께 쓰는 형식적 `U_P`를 쓰고, 일반 상태의 BFV 교환식과
검출 가능한 top class의 소실을 따로 검사하도록 구체화했다. 조건부 판별값은
`(전체 chain 결함, 원 pairing, 영상, 적분 contraction 뒤 pairing) = (0,1,0,1)`이다.
이 값들은 실제 새 runner의 출력이 아니라, 선언한 입력 아래 모델이 제시한 검사 예상값이다.
후보를 질문에 명시했으므로 자율적인 새 사상 발견이나 HSWM의 독립적 발견으로 쓰지 않는다.

독립적인 source 대조에서 sign 규약과 degree별 식, `R_N p=0`, detector의 반전된 차수와
비물리적 bilinear pairing을 검토했다. **rho 제거가 top 상태 소실의 직접 원인**이고,
bump를 평가점 밖에 놓는 것은 점 평가와 적분을 비교하는 추가 직관이다. 또한
relative boundary slice를 bulk BV gauge fixing으로 읽으면 안 되며, N 없는 target으로
N-collar와 p_N jets를 그대로 옮긴다고 쓰면 안 된다. 이 검토를 반영한 설명은
[연구 지도의 후보 검토](../research/ICE_HSWM_BOUNDARY_INTUITION_2026-09-08.md)에 있다.

최종 제안은 source-derived tuple·comparison map·allowed test pair를 모두 `missing`으로
유지했다. 중간 domain 제안은 가정으로 지정했다는 이유로 `missing: []`를 썼다. renderer는
이런 생략을 그대로 표시하지 않고, 원본 state에서 미확보인 검사 입력도 반드시 표시한다.
사람이 선언한 후보가 검증된 source 입력으로 바뀌지는 않는다.

산출물 검토 후 useful feedback을 기록해 `FEEDBACK_RECORDED`, `WEIGHTS_UPDATED`를
확인했다. 이는 반례 설계의 유용성에 대한 검토이며 scientific success는 계속 `null`이다.
실제 state 조회에서 root `research-with-state`만 observations 1, revision 2가 됐고,
중첩 `declare-domain`은 observations 0, revision 1이었다. 현재 feedback이 내부 관계에
독립적으로 credit을 배분한다고 주장하지 않는다.
상호 배타적 guard 때문에 이 revision을 더 나은 경로 선택의 증거로 해석하지 않는다.

## 검증

`npm run graph:release-check`는 typecheck와 179개 테스트, 전체 ontology·SHACL·competency·
GraphRAG·agent 검사, corpus coverage, production advisory와 SBOM까지 통과했다.
이후 missing 입력 표시 보완은 focused test와 typecheck로 별도 확인했다.
`ontology review`는 CPT 정책 hash와 timestamp 변경만 보고했고,
`graphrag diff --base HEAD --limit 12 --json`도 검토했다.
`harness check`: hash 544/544, errors 0, warnings 75. 기존 warning은 이 확장에서
없어졌다고 보고하지 않는다. 연구 상태와 최종 원문은 별도로 parse했고, 실제 HSWM 경로
비교와 완성된 회차는 위 기록대로 관측했다.
