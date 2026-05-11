---
name: apt-scw
description: >
  APT SourceCodeWorld (SCW) phase — universal TDD implementation
  of crystallized Contracts. Invoke when: implementing code from a Contract, writing tests
  from acceptance criteria, materializing a Contract as source code, or doing actual coding
  work after ST crystallization. Project-agnostic — works for ANY SemanticAnchor.
  Governs PH5 (TDD implementation) and PH6 (KG feedback).
  Enforces: test-first from Contract, single-file targeting, MATERIALIZES tracking,
  KG feedback on discoveries, Strange Loop TDD, Thompson Sampling gap resolution.
  Lean 4 formal axioms: lean/apt-axioms/AptAxioms/Basic.lean
  Never start coding without a crystallized Contract.
---

# APT SCW: SourceCodeWorld Implementation (Universal)

# KG: TASK_Skill_APT_SCW
# KG: CONTRACT_Skill_APT_SCW

SCW is where Contracts become running code. The discipline is TDD — write tests first from the Contract's acceptance criteria, then implement until they pass. **Code is the Contract's materialization, nothing more.**

## Mathematical Foundation

### Definition: Materialization

Let C be a Contract and S be source code. Materialization is the function:

```
materialize : Contract -> SourceCode
materialize(C) = S  such that:
  typeof(S.input)  = C.input_type
  typeof(S.output) = C.output_type
  S satisfies C.precondition => C.postcondition
  S passes C.acceptance_criteria
```

The materialization is **correct** iff all acceptance criteria pass. This is a constructive proof in the Curry-Howard sense: the code IS the proof that the Contract's type proposition is satisfiable.

### The TDD Strange Loop

```
Acceptance Criteria ARE the tests
Tests ARE the specification
Specification IS the Contract
Contract IS the type proposition
Implementation IS the proof

=> Writing tests first = writing the specification first = proving from the proposition
```

This is a **Strange Loop** (Hofstadter): the hierarchy is circular but each traversal produces progress. Red->Green->Refactor spirals upward.

### Specification Amnesia (primary anti-pattern)

```
P(amnesia) increases with:
  - time since last Contract read
  - lines of code written without test reference
  - number of "seems right" decisions without Contract check

Guard: before writing ANY function, re-read Contract.input_type and Contract.output_type
```

## Prerequisites

Before writing any code:

```cypher
-- Verify Contract exists and is ready
MATCH (st:SemanticTwin {name: $st_name})-[:HAS_CONTRACT]->(c)
MATCH (st)-[:HAS_TASK]->(t:SemanticTask)
RETURN c.name, c.input_type, c.output_type, c.precondition, c.postcondition,
       c.acceptance_test, t.target_file, t.acceptance_criteria, t.status
```

ALL of these must be non-null. If any is missing, go back to /apt-st.

## TDD Workflow: Red -> Green -> Refactor

### Step 1: Write AcceptanceCriteria tests FIRST (Red)

Convert each acceptance criterion into a test function **before writing any implementation code**:

```python
# KG: TASK_xxx
# KG: CONTRACT_xxx

def test_acceptance_criterion_1():
    """From CONTRACT_xxx.acceptance_test: '<specific scenario>'"""
    result = function_under_test(concrete_input)
    assert result.field == expected_value
    assert isinstance(result, ExpectedType)
```

Run the tests. They **MUST fail**. If they pass without implementation, the test is wrong or the Contract is trivial.

### Step 2: Implement minimum code to pass (Green)

Write code in the Task's `target_file`. Follow Contract type signatures exactly:

```python
# KG: TASK_xxx
# KG: CONTRACT_xxx

def function_under_test(input: ContractInputType) -> ContractOutputType:
    # KG: CONTRACT_xxx (input_type -> output_type)
    # precondition check
    assert input satisfies Contract.precondition

    # implementation
    ...

    # postcondition guarantee
    assert result satisfies Contract.postcondition
    return result
```

**500-line maximum per file.** If implementation needs more, STOP. Go back to /apt-sp — the AtomicSpan needs further decomposition. Large files are a decomposition failure, not a coding problem.

### Step 3: Refactor while tests stay green

Apply SOLID principles. Re-run tests after every change. If tests break, revert.

### Step 4: Record MATERIALIZES in KG

```cypher
MATCH (c:AptContract {name: $contract_name})
MERGE (src:AptSourceCode:SourceCodeWorld {name: $source_name})
SET src.file_path = $target_file,
    src.status = 'implemented',
    src.lines = $actual_lines,
    src.updated_at = datetime()
MERGE (c)-[:MATERIALIZES]->(src)

// Update Task status
WITH src
MATCH (t:SemanticTask {name: $task_name})
SET t.status = 'completed', t.completed_at = datetime()
```

## KG Reference Comments (mandatory)

Every source file MUST include KG reference comments:

```python
# KG: TASK_xxx           <- which Task this file implements
# KG: CONTRACT_xxx       <- which Contract(s) it conforms to

def my_function(input: InputType) -> OutputType:
    # KG: CONTRACT_xxx (input_type -> output_type)
    ...
```

These create bidirectional traceability: KG -> code (via target_file), code -> KG (via comments).

## PH6: KG Feedback Loop

Implementation reveals things SP/ST missed. **Never silently patch — record in KG.**

### Recording AptFeedback

```cypher
CREATE (f:AptFeedback {
    name: $feedback_name,
    source_phase: 'SCW',
    discovery_type: $type,
    // 'missing_span' | 'contract_gap' | 'type_mismatch' | 'perf_issue' | 'edge_case'
    description: $description,
    category: $category,
    // 'Bug' | 'Confusion' | 'Improvement' | 'Missing' | 'Violation'
    created_at: datetime()
})
WITH f
MATCH (task:SemanticTask {name: $task_name})
MERGE (f)-[:DISCOVERED_IN]->(task)
```

### Feedback Actions

| Discovery type | Action |
|---------------|--------|
| **missing_span** | Record feedback -> /apt-sp -> new Span -> /apt-st -> return here |
| **contract_gap** | Record feedback -> /apt-st -> update Contract -> rewrite tests -> fix code |
| **type_mismatch** | Record feedback -> fix Contract types -> propagate to dependent STs |
| **perf_issue** | Record feedback -> may need architectural Span revision |
| **edge_case** | Record feedback -> add to acceptance_criteria -> add test -> fix code |

**Silent patches (fixing without recording) create drift between KG model and code. This IS Specification Amnesia.**

## Gap Resolution: Thompson Sampling

When multiple implementation approaches exist without a clear winner:

```
1. Query KG for existing candidates:
   MATCH (g:AptGapAnalysis)-[:HAS_CANDIDATE]->(c:GapCandidate)
   WHERE g.name = $gap_name AND c.status <> 'rejected'
   RETURN c.name, c.positive_count, c.negative_count,
          toFloat(c.positive_count)/(c.positive_count + c.negative_count + 1) AS score
   ORDER BY score DESC

2. Apply Thompson Sampling:
   - 70% probability: pick highest score (exploit)
   - 30% probability: pick untried/least-tried (explore)
   - Never use same candidate 3x consecutively (path dependency prevention)

3. After implementation, update score:
   MATCH (c:GapCandidate {name: $candidate})
   SET c.positive_count = c.positive_count + $pos,
       c.negative_count = c.negative_count + $neg

4. Adoption: positive >= 3 AND negative <= 1 -> adopted
   Rejection: negative >= 3 -> rejected
```

## FulfillmentGate (post-implementation)

After all tests pass, verify Contract fulfillment:

```
FulfillmentGate(Task, Contract):
  1. All acceptance_criteria tests pass
  2. Output type matches Contract.output_type
  3. Preconditions checked in code
  4. Postconditions guaranteed in code
  5. KG ref comments present
  6. File <= 500 lines

  ALL must pass. If any fails, iterate.
```

## IntegrationGate (post-merge)

When multiple parallel Tasks are integrated:

```
IntegrationGate(Tasks[], ParentContract):
  1. Individual FulfillmentGates all pass
  2. Combined output satisfies ParentContract
  3. No type conflicts between Task outputs
  4. Integration test passes (not just unit tests)

  Failure -> check Contract compatibility -> may need Contract amendment
```

## Agent Anti-Patterns

| Anti-pattern | Guard |
|-------------|-------|
| **Gold Plating** | Only implement what's in the Contract |
| **Specification Amnesia** | Re-read Contract before every function |
| **Test Afterthought** | Tests BEFORE code (Red phase first) |
| **Silent Patch** | ALWAYS record AptFeedback for discoveries |
| **Monolith Creep** | Stop at 500 lines, go back to SP |
| **Vibe Coding** | Every decision traceable to Contract field |

## Output

When SCW completes:
- Tests written and passing (TDD Red->Green->Refactor complete)
- Code in target_file conforming to Contract types (500-line max)
- KG ref comments at top of file and on key functions
- MATERIALIZES relationship in KG
- SemanticTask status = 'completed'
- AptFeedback nodes for any discoveries (PH6)
- FulfillmentGate passed
- Gap candidates updated with Thompson Sampling scores if applicable

## What NOT to do here

- Do not start without a crystallized Contract. Ever.
- Do not write tests after code. TDD Strange Loop demands Red first.
- Do not silently fix bugs. Record AptFeedback.
- Do not exceed 500 lines. Decomposition failure, not coding problem.
- Do not ignore Contract types. Vibe Coding is the enemy.
