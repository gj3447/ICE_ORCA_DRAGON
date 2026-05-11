---
name: science-feedback-loop
description: 과학 발견 피드백 루프. 계산 결과를 KG에 반영하고 이론을 자동 수정/발전시킨다.
triggers:
  - 피드백 루프
  - feedback loop
  - 발견
  - discovery
  - 검증 결과
---

# Science Feedback Loop

계산/검증 결과가 나올 때마다 이 루프를 실행한다.

## 루프 구조

```
           ┌─────────────────────────────────┐
           │                                 │
           ▼                                 │
    [1. 계산/검증 실행]                       │
           │                                 │
           ▼                                 │
    [2. 결과 분류]                            │
       ├─ confirmation → [3a] confidence ↑   │
       ├─ refutation → [3b] Contract 수정    │
       ├─ discovery → [3c] 새 Span → PH2 ───┘ (재귀!)
       └─ numerology → [3d] HOLD 태깅
           │
           ▼
    [4. Fitting Detection]
       사전예측 vs 사후피팅 판별
           │
           ▼
    [5. Lakatos 평가]
       progressive: 새 예측 있음 → 이론 강화
       degenerating: 기존만 설명 → 이론 약화
           │
           ▼
    [6. Bayesian Update]
       P(H|E) = P(E|H)·P(H) / P(E)
       핵심: P(E|~H) — "이 이론 없이도 나올 확률"
           │
           ▼
    [7. KG 업데이트]
       Contract confidence 갱신
       Span grade 갱신
       SA→SP→ST 일관성 체크
```

## 각 단계 상세

### 3a. Confirmation
```cypher
MATCH (c:Contract) WHERE c.name = '{name}'
SET c.confidence = c.confidence + {delta},
    c.last_confirmed = date()
```

### 3b. Refutation
```cypher
MATCH (c:Contract) WHERE c.name = '{name}'
SET c.status = 'REFUTED',
    c.refuted_by = '{evidence}',
    c.refuted_date = date()
// 상위 Span 재검토 트리거
MATCH (s:Span)-[:CRYSTALLIZES_TO]->(:SemanticTwin)-[:HAS_CONTRACT]->(c)
SET s.needs_review = true
```

### 3c. Discovery (재귀 진입)
```cypher
CREATE (new_span:Span {
  name: 'ORCA_Span_Discovery_{topic}',
  discovered_from: '{원래 계산}',
  status: 'NEW'
})
// PH2 재진입: /apt-sp로 새 span 분해
```

### 3d. Numerology Detection
```cypher
MATCH (c:Contract) WHERE c.name = '{name}'
SET c.status = 'NUMEROLOGY_HOLD',
    c.numerology_note = '{이유}'
// Possibility로 전환
CREATE (p:Possibility {name: 'POSSIBILITY: {hint}', confidence: {low_value}})
```

## 오늘 세션의 피드백 루프 실행 기록

| 순서 | 계산 | 결과 유형 | 액션 |
|------|------|----------|------|
| 1 | T₂ 메커니즘 검증 | **refutation** | Step 4 Contract 수정 |
| 2 | ZD null space 분석 | **discovery** | 새 Span 생성, PH2 재진입 |
| 3 | SU(2) doublet 검증 | **confirmation** | confidence 0.90 |
| 4 | 14 non-ZD 구조 | **confirmation** | Fano 7+7 확인 |
| 5 | Der(S) 계산 | **confirmation** | g₂ dim=14 확인 |
| 6 | c=4ln(2) 해석 | **numerology** | NUMEROLOGY_HOLD |
| 7 | Bekenstein 연결 | **numerology** | NUMEROLOGY_HOLD |
| 8 | Wilmot 2025 검증 | **confirmation** | Moufang 패턴 확인 |

피드백 루프 8회 실행 → 3 confirmations, 1 refutation, 1 discovery, 2 numerology
→ Lakatos: PROGRESSIVE (discovery + confirmations > numerology)
