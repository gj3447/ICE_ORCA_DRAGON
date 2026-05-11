# APT v5 Getting Started

## Glossary

| Term | Definition |
|------|-----------|
| **SA** | SemanticAnchor — project identity. One per project. |
| **SP** | SemanticPyramid — one world containing Spans in layers. Where decomposition happens. |
| **ST** | SemanticTwin — crystallized spec. Contract + Task pair. |
| **SCW** | SourceCodeWorld — actual code that implements an ST's Contract. |
| **Span** | A planning-unit node inside SP. NOT an SA, NOT an ST. |
| **AtomicSpan** | A Span where C(S)=true. Ready to cross to ST. |
| **LeafSpan** | A Span with no children yet. May or may not be atomic. |
| **D(S)** | Decomposition function. Recursively splits S until C(S)=true. |
| **C(S)** | Crystallization predicate. C(S) = tau ∧ sigma ∧ nu ∧ iota. |
| **tau(S)** | Type expressibility — can output be a typed signature? |
| **sigma(S)** | Semantic completeness — does the type capture full meaning? |
| **nu(S)** | Implementation feasibility — can you write the function now? |
| **iota(S)** | Test feasibility — can you write a concrete test now? |
| **Crystallization Frontier** | The boundary between SP and ST. Only CRYSTALLIZES_TO crosses it. |
| **Mold** | Architectural tool grouping. 6 molds: Governance, Intent, Boundary, Execution, Assurance, Memory. |
| **Contract** | Typed I/O spec (input, output, pre/post conditions, acceptance test, target file). Lives only at ST. |
| **Twin Registry** | Tracks ST lifecycle: draft → crystallized → implemented → validated → stale → broken. |

## PH1: Check the SemanticAnchor

```cypher
MATCH (sa:DefinitionAnchor) RETURN sa.name
// PRISM → "PRISM_Manufacturing_Inspection"
// If empty → project hasn't been bootstrapped. Create one:
// MERGE (sa:DefinitionAnchor:PrismPyramid {name: $project_name})
// SET sa.domain = $domain, sa.description = $desc
```

For PRISM, the SA already exists. You never need to create it.

## PH2: Find Your RootIntentSpan

Every task belongs somewhere in the existing SP hierarchy. Find it:

```cypher
// What top-level Spans exist?
MATCH (n:SemanticSpan) RETURN n.name
// PRISM → PRISM_Capture, PRISM_Inspect, PRISM_Validate, PRISM_Present, PRISM_Persist, PRISM_Serve

// Which L2 Span covers your area?
MATCH (n:AptSpan) WHERE n.name CONTAINS $keyword RETURN n.name, labels(n)
```

## Hello World: Adding a Health Check Endpoint

### Step 1: Phase detection (/apt)
```cypher
MATCH (n:AptSpan) WHERE n.name CONTAINS 'Health' RETURN n.name, labels(n)
// If exists → check its phase. If not → need SP decomposition.
```

### Step 2: SP decomposition (/apt-sp)
Say we need to add health checks under the API layer.

```cypher
// Find parent
MATCH (api:AptSpan) WHERE api.name CONTAINS 'API' AND NOT (api)<-[:DECOMPOSES_TO]-()
RETURN api.name  // Find the right parent Span
```

Decompose into children (k ≥ 2):
- Span_HealthLiveness: "process alive check"
- Span_HealthReadiness: "dependency checks (PG, MinIO, Neo4j)"

Check C(S) for each:
- tau: `HealthResult(status: str, checks: dict)` — expressible? YES
- sigma: captures full meaning? YES (status + per-dependency details)
- nu: can write the function? YES (`async def liveness(): return {"status": "ok"}`)
- iota: can write test? YES (`assert response.status_code == 200`)

C(S) = true → mark as AtomicSpan.

### Step 3: ST crystallization (/apt-st)
```cypher
MERGE (st:SemanticTwin:AptNode {name: 'ST_HealthLiveness'})
SET st.status = 'draft'
// ... CRYSTALLIZES_TO from AtomicSpan
// ... HAS_CONTRACT with typed spec
// ... HAS_TASK with acceptance criteria
```

### Step 4: TDD implementation (/apt-scw)
```python
# Test first (from Contract acceptance_test):
def test_health_liveness():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# Then implement in target_file:
@router.get("/health/live")
async def liveness():
    return {"status": "ok"}
```

### Step 5: KG materialization
```cypher
MATCH (c:AptContract {name: 'CT_HealthLiveness'})
MERGE (src:SourceCodeNode {name: 'SRC_HealthLiveness'})
SET src.file_path = 'prism_server/api/routers/health.py'
MERGE (c)-[:MATERIALIZES]->(src)
```

## Which Skill First?

```
"I need to..."
  ├── "...figure out where this goes" → /apt (phase detection)
  ├── "...plan/design/decompose" → /apt-sp
  ├── "...write a contract/spec" → /apt-st
  ├── "...write code" → /apt-scw (but check: is there a Contract?)
  ├── "...check APT compliance" → /apt (validation)
  ├── "...report a problem with APT" → /apt (feedback section)
  └── "...understand APT" → read this file
```
