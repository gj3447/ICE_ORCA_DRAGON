---
name: science-feedback-loop
description: 과학 observable·가설 지지/반박·null 또는 multiplicity·Contract/Span 판단을 바꾸는 T2 계산과 검증에만 적용하는 증거 피드백 루프. 일반 코드·문서·테스트(T0)나 동결 계산의 단순 재현(T1)에는 사용하지 않는다.
---

# Science Feedback Loop

이 스킬을 일반 완료 의례로 사용하지 말라. 먼저 아래 적용 tier를 고정하라.

## 적용 게이트

| Tier | 범위 | 필수 조치 |
|---|---|---|
| T0 일반 공학 | 문서, CLI, 리팩터링, 의존성, 타입/단위검사, 재현 하네스 | 관련 테스트와 실행 근거만 남겨라. 과학 분류·Bayes·Lakatos·science-evidence KG를 생략하라. |
| T1 동결 재현 | 기존 방법·observable·해석을 바꾸지 않는 재실행 | 환경·명령·출력 diff·사전등록 여부를 남겨라. 일치만으로 confidence를 바꾸지 말라. |
| T2 과학 주장 영향 | 새/변경 observable, 가설 지지·반박, null/multiplicity, 과학 주장에 영향을 주는 방법 결함, Contract/Span 판단 변화 | 아래 전체 게이트를 적용하라. |

여러 tier가 겹치면 가장 높은 tier를 결과 관측 전에 선택하라. T0/T1에서 T2로 승격할 수는
있지만 불리하거나 null인 결과를 본 뒤 T2를 낮추지 말라. T2에 코드 변경이 포함되면 T0의
관련 공학 검사도 수행하라.

T1에서 유의한 drift나 주장에 영향을 주는 방법 결함을 발견하면 T2로 승격하라. 단순 실행 실패,
누락 의존성, 포맷 차이처럼 과학 증거가 아닌 문제는 T0에서 처리하라.

## T2 절차

### 1. 결과를 보기 전에 판정 계약을 고정하라

가능한 항목만 명시하되, 결과를 본 뒤 소급해 만들지 말라.

- 가설 `H`와 관측/산출물 `E`
- target claim과 증거 층위(`ALGEBRAIC` / `NUMERICAL` / `PHYSICS_MAPPING`)
- 예상 방향 또는 허용 영역
- 적용 가능한 경우 null model과 `P(E|~H)` 산정법
- 적용 가능한 경우 multiplicity와 look-elsewhere 보정
- metric, tolerance, 제외 필드, 판정 임계값
- 사전등록 위치와 날짜

이미 결과를 본 경우 `POST_HOC`로 표시하고 confirmation으로 승격하지 말라.

### 2. 계산과 재현 근거를 보존하라

실행 명령, 인자, 잠금 환경, 입력과 출력 경로, 날짜, actor, 코드 commit을 기록하라. 원본 결과를
덮어쓰지 말고 새 방법은 새 버전·새 사전등록·새 baseline으로 분리하라. 구조와 범주를 exact로,
수치는 사전에 정한 field-specific 정책으로 비교하라.

### 3. 결과를 서로 독립인 축으로 분류하라

강제로 하나의 라벨만 고르지 말고 다음 축을 각각 기록하라.

- **추론**: `SUPPORTS` / `CONTRADICTS` / `INCONCLUSIVE`
- **신규성**: `REPLICATION` / `DISCOVERY_CANDIDATE`
- **등록**: `PREREGISTERED` / `POST_HOC`
- **피팅 위험**: `CONTROLLED` / `NUMEROLOGY_RISK` / `NUMEROLOGY_HOLD` / `NOT_ASSESSED` / `NOT_APPLICABLE`

`CONFIRMATION`은 사전등록된 판정 계약과 적용 가능한 재현/null 게이트를 모두 통과한 경우에만
보조 라벨로 사용하라. `REFUTED` 정전 변경은 사전등록된 falsifier, 검증, ratification을 모두
통과한 경우에만 사용하라. 계산 사실과 그 물리 해석의 라벨을 분리하라.

### 4. 필요한 추론만 수행하라

- fitting 위험의 적용 가능성을 먼저 판단하고, 수비학 의심을 승격 근거로 사용하지 말라. 적용
  가능하다면 같은 primitive의 MC null과
  look-elsewhere 보정으로 정량화한 뒤에만 `NUMEROLOGY_HOLD`를 확정하라.
- Lakatos 평가는 개별 실행마다 하지 말고 새 예측이나 보호가설 변경을 검토하는 연구 프로그램
  checkpoint에서만 하라. program/fiber, 비교 baseline, 평가 window를 먼저 선언하라.
  `PROGRESSIVE`는 novel excess empirical content와 독립 corroboration이 있을 때만,
  `DEGENERATING`은 corroborated novelty 없이 ad-hoc belt 변경이 누적된 longitudinal 근거가
  있을 때만 사용하라. 그 외에는 count-vote하지 말고 `UNDETERMINED`로 두라.
- 수치 Bayesian update는 prior, `P(E|H)`, `P(E|~H)`가 결과 전에 정의된 경우에만 수행하라.
  selection과 증거 간 dependence도 명시하라. 하나라도 없으면 `NOT_ESTIMABLE`로 기록하고
  confidence를 바꾸지 말라. 같은 데이터나 출력의 재실행을 독립 `E`로 다시 곱하지 말라.
  임의 delta를 더하지 말라.

### 5. evidence와 정전 변경을 분리하라

여러 세션에서 재사용할 T2 결과만 provenance가 붙은 `PENDING` evidence로 KG에 기록하라.
evidence 작성과 동시에 Contract confidence/status, Span grade, 기존 canon을 수정하지 말라.
독립 재현이나 사용자 검토는 ratification의 근거이지 그 자체가 ratification은 아니다. 기존
pending evidence ID와 명시된 ratifier 권한을 확인한 별도 절차에서만 정전 변경을 수행하라.
일반 T2 실행이 자신을 ratify하지 못하게 하라.

새 `:Lesson`을 만들 가치가 있는 반복 가능하고 비자명한 방법 교훈이라면 `wrongAssumption`,
`truth`, 재발 방지, provenance와 KG 계약상의 `lakatos_mechanism`을 채워라. 평범한 오류를 이
스키마에 맞추려고 Lesson으로 승격하지 말라.

### 6. discovery를 무조건 재귀시키지 말라

`DISCOVERY_CANDIDATE`는 bounded 후속 작업으로 등록하라. 부모 작업은 현재 범위의 결론과 한계를
남기고 완료할 수 있다. 발견이 현재 판정을 막거나 사용자가 명시적으로 범위를 확장했을 때만
PH2 또는 새 span으로 재귀 진입하고, 자식 작업의 tier는 독립적으로 다시 정하라.

## 최소 보고 형식

```text
tier: T2
provenance: <command, environment, commit, paths, date, actor>
target: <claim and ALGEBRAIC | NUMERICAL | PHYSICS_MAPPING layer>
registration: PREREGISTERED | POST_HOC
inference: SUPPORTS | CONTRADICTS | INCONCLUSIVE
novelty: REPLICATION | DISCOVERY_CANDIDATE
fitting_risk: CONTROLLED | NUMEROLOGY_RISK | NUMEROLOGY_HOLD | NOT_ASSESSED | NOT_APPLICABLE
reproduction: <result and comparison policy>
bayes: NOT_APPLICABLE | NOT_ESTIMABLE | <inputs and result>
lakatos: NOT_APPLICABLE | UNDETERMINED | <checkpoint verdict and reason>
kg_action: NONE | EVIDENCE_PENDING
ratification_request: <pending evidence id + authorized ratifier, or none>
follow_up: <bounded next task or none>
```

세션별 실행 기록을 이 스킬 본문에 누적하지 말라. 실행 기록은 결과 문서와 handoff에 남기고,
이 파일에는 재사용 가능한 절차만 유지하라.
