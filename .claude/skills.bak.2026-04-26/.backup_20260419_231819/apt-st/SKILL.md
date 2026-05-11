---
name: apt-st
description: >
  APT SemanticTwin (ST) phase — universal crystallization of AtomicSpans
  into typed Contracts and Tasks. Invoke when: an AtomicSpan is ready for contract definition,
  writing typed specifications, defining acceptance criteria, or creating SemanticTwin nodes.
  Governs PH4 (ST Crystallization). Project-agnostic — works for ANY SemanticAnchor.
  Enforces: Contracts only at ST level, 5 crystallization criteria validation,
  Contract-as-Mask principle, Curry-Howard typed specification.
  Lean 4 formal axioms: lean/apt-axioms/AptAxioms/Basic.lean
  Use after /apt-sp has produced AtomicSpans, never before.
---

# APT ST: SemanticTwin Crystallization (Universal)

# KG: TASK_Skill_APT_ST
# KG: CONTRACT_Skill_APT_ST

ST is the specification space where abstract Spans become concrete, typed contracts. **APT's sole bottleneck is Contract quality.** A bad Contract produces bad code that passes bad tests.

## Mathematical Foundation

### Definition: Crystallization Frontier

The Crystallization Frontier F is the boundary between SP and ST worlds:

```
F = { (S, T) | S in SP, S:AtomicSpan, T in ST, S -[:CRYSTALLIZES_TO]-> T }
```

**CRYSTALLIZES_TO is the ONLY relationship crossing F.** No other path exists between SP and ST. This is a hard topological constraint.

### Definition: SemanticTwin

A SemanticTwin T is a pair:

```
T = (Contract, Task)

where:
  Contract : typed agreement between parallel tasks
  Task     : TDD completion condition with acceptance criteria
```

The mapping is:

```
crystallize : AtomicSpan -> SemanticTwin
crystallize(S) = (contract(S), task(S))

where:
  contract(S) = { input_type, output_type, precondition, postcondition, semantic_meaning }
  task(S)     = { acceptance_criteria, target_file, estimated_lines }
```

### Contract-as-Mask Principle

From Principle_ContractAsMask:

```
Contract = Diffusion Mask
  - Fixed (unmasked): type signatures, invariants, pre/post conditions
  - Generated (masked): implementation body

Contract quality = mask quality = generation quality
```

DiffuCoder (Apple), Mercury (Inception), Gemini Diffusion (Google) validate this at production level. **If the Contract types are right, independent tasks compose correctly. If wrong, individual tests pass but integration fails.**

### Curry-Howard Correspondence

```
Types are propositions.
Implementations are proofs.
A Contract's type signature IS the specification.
An implementation that type-checks IS a proof of correctness (at the type level).
```

## Prerequisites

Before entering ST, an AtomicSpan must have passed all **5** crystallization criteria in /apt-sp:

```
C(S) = tau(S) AND sigma(S) AND nu(S) AND iota(S) AND delta(S) = true
```

If unsure, go back to SP and verify. **Never crystallize a non-atomic Span.**

```cypher
-- Verify AtomicSpan status
MATCH (s:AptSpan {name: $span_name})
RETURN s.is_atomic, s.crystallization_check, labels(s)
```

## Step 1: Create the SemanticTwin node

```cypher
MATCH (as:AtomicSpan {name: $atom_name})
// Guard: must be AtomicSpan
WHERE as.is_atomic = true

MERGE (st:SemanticTwin:AptNode {name: 'ST_' + replace($atom_name, 'ATOM_', '')})
SET st.status = 'crystallized',
    st.created_at = datetime()
MERGE (as)-[:CRYSTALLIZES_TO]->(st)
RETURN st.name
```

## Step 2: Author the Contract — typed agreement

Contract = typed agreement between parallel tasks ensuring independent work integrates.

**Analogy**: construction site where electrical and plumbing teams work simultaneously. Without the agreement "pipe at position 3," they collide. The Contract IS that agreement.

### Contract Structure

```
Contract = {
  input_type:       concrete params/dataclass/schema (NEVER abstract)
  output_type:      concrete return type/response (NEVER abstract)
  precondition:     testable boolean condition on input state
  postcondition:    verifiable guarantee on output state
  semantic_meaning: domain interpretation (units, coordinate frame, etc.)
}
```

### Contract Quality Checklist

| Check | Concrete example | Anti-pattern |
|-------|-----------------|-------------|
| **Types are concrete** | `float32[N,3]`, `PhaseDecision`, `ValidationResult` | "data", "result", "object", "any" |
| **Preconditions testable** | "span must exist as AptSpan in KG" | "valid input" |
| **Postconditions verifiable** | "output.allowed == False when phase mismatch" | "correct output" |
| **Semantic meaning explicit** | "millimeters in ROBOT_BASE frame" | "a distance value" |
| **No Span-level attachment** | Contract -> ST via HAS_CONTRACT | Contract -> Span (FORBIDDEN) |
| **Shared where applicable** | One Contract for 3 STs that use same type | Duplicate contracts per ST |

### Contract Sandwich Structure

One Contract can span multiple SemanticTwins (shared agreement):

```
CONTRACT_X (agreed type shape)
  |-- ST_A  <- adheres to CONTRACT_X
  |-- ST_B  <- adheres to CONTRACT_X
  +-- ST_C  <- adheres to CONTRACT_X
```

**Typed agreements auto-resolve integration.** If Task A outputs `TypeX` and Task B inputs `TypeX`, they compose without coordination.

```cypher
MERGE (c:AptContract:ContractDef {name: $contract_name})
SET c.description = $description,
    c.input_type = $input_type,
    c.output_type = $output_type,
    c.precondition = $precondition,
    c.postcondition = $postcondition,
    c.semantic_meaning = $semantic_meaning,
    c.status = 'defined',
    c.created_at = datetime()
WITH c
MATCH (st:SemanticTwin {name: $st_name})
MERGE (st)-[:HAS_CONTRACT]->(c)
```

## Step 3: Author the Task — TDD completion condition

Task = the actual work unit. Single file, ~500 lines, with concrete acceptance criteria.

```
Task = {
  acceptance_criteria : Task -> Bool  (pure function determining completion)
  target_file         : single file path
  estimated_lines     : 200~500 sweet spot
}
```

**Contract does NOT contain**: acceptance_test, target_file, implementation.
**Task does NOT contain**: type definitions, invariants (those are in Contract).

```cypher
MERGE (task:SemanticTask:AptTask {name: $task_name})
SET task.acceptance_criteria = $criteria,
    task.target_file = $target_file,
    task.estimated_lines = $lines,
    task.status = 'defined',
    task.created_at = datetime()
WITH task
MATCH (st:SemanticTwin {name: $st_name})
MERGE (st)-[:HAS_TASK]->(task)
```

## Step 4: Tau-Check the Contract (automated validation)

After creating the Contract, run tau(S) validation:

```
tau_check(Contract):
  1. Parse input_type → are all types concrete? (no "data", "result", "any")
  2. Parse output_type → same check
  3. Precondition → is it a boolean expression? (not prose)
  4. Postcondition → is it verifiable? (not "works correctly")
  5. Semantic_meaning → is domain context present?

  Score: count(pass) / 5.0
  PASS if score >= 0.8 (allow 1 soft field like semantic_meaning)
```

If tau_check fails, the Contract is too vague. Sharpen types before proceeding.

## Contract Lifecycle FSM

```
Draft -> Active -> Amended -> Fulfilled
  |                  ^           |
  v                  |           v
Rejected         (change)    Archived

Transitions:
  Draft -> Active    : tau_check passes
  Active -> Amended  : Contract changed (impact analysis required)
  Active -> Fulfilled: all Tasks pass acceptance_criteria
  Amended -> Active  : re-validated after change
  * -> Rejected      : fundamental design flaw discovered
```

```cypher
-- Update Contract status
MATCH (c:AptContract {name: $contract_name})
SET c.status = $new_status, c.updated_at = datetime()
```

## Task Exploration: Finding Acceptance Criteria

Writing acceptance criteria follows the scientific method:

```
1. Hypothesize — propose a criterion
2. Test       — attempt implementation against it
3. Observe    — does it capture what matters?
4. Revise     — adjust based on evidence
5. Converge   — settle on reliable criteria
```

If you can't find criteria that work, the Span needs further decomposition (go back to /apt-sp).

## Output

When ST crystallization completes:
- SemanticTwin nodes linked via CRYSTALLIZES_TO from AtomicSpans
- Contract nodes with concrete typed specs (input/output/pre/post/semantic)
- Task nodes with acceptance criteria, target_file, estimated_lines
- tau_check passed for each Contract
- Twin lifecycle status = 'crystallized'
- Ready for /apt-scw TDD implementation

## Write-Time Integrity Rules (CRITICAL)

These rules prevent the data quality issues discovered during the 2026-03-24 audit: duplicate twins, orphan contracts, null statuses, naming inconsistencies.

### Rule 1: MERGE, Never CREATE

**Always use MERGE for Twin and Contract nodes.** CREATE causes duplicates when the same crystallization runs multiple times or across sessions.

```cypher
-- CORRECT: idempotent
MERGE (st:SemanticTwin:AptTwin {name: 'ST_OM_...'})

-- WRONG: creates duplicates
CREATE (st:SemanticTwin:AptTwin {name: 'ST_OM_...'})
```

**Neo4j Constraints enforced:**
- `apt_twin_unique`: AptTwin.name IS UNIQUE
- `apt_sprint_unique`: AptSprint.name IS UNIQUE

### Rule 2: Chain Completeness — Atom → Twin → Contract in One Transaction

Never create an Atom without its Twin, or a Twin without its Contract. The full chain must be established atomically:

```cypher
// Create complete chain: Atom → Twin → Contract
MATCH (atom:AptSpan {name: $atom_name})
WHERE atom.is_atomic = true

MERGE (st:SemanticTwin:AptTwin {name: 'ST_' + replace($atom_name, 'ATOM_', '')})
SET st.status = COALESCE(st.status, 'crystallized'),
    st.created_at = COALESCE(st.created_at, datetime())
MERGE (atom)-[:CRYSTALLIZES_TO]->(st)

MERGE (ct:AptContract {name: 'CT_' + replace($atom_name, 'ATOM_', '')})
SET ct.status = COALESCE(ct.status, 'defined'),
    ct.created_at = COALESCE(ct.created_at, datetime())
MERGE (st)-[:HAS_CONTRACT]->(ct)
```

### Rule 3: Naming Convention Enforcement

| Node Type | Required Prefix | Example |
|-----------|----------------|---------|
| Leaf Atom | `ATOM_{PROJECT}_` | `ATOM_OM_GPU_CLI` |
| Twin | `ST_{PROJECT}_` | `ST_OM_GPU_CLI` |
| Contract | `CT_{PROJECT}_` | `CT_OM_GPU_CLI` |
| Sprint | `SPRINT_{PROJECT}_` | `SPRINT_OM_1_Storage` |

**Derivation rule**: `ATOM_OM_Foo` → `ST_OM_Foo` → `CT_OM_Foo`

Legacy prefixes (`SP_OM_*`, `SPAN_OM_*` for leaf atoms) are **forbidden for new nodes**. If encountered, rename to `ATOM_OM_*`.

### Rule 4: Status Must Not Be Null

Every APT node must have a non-null status from this enum:

```
planned | in_progress | crystallized | implemented | completed | verified |
active | archived | superseded | deferred | blocked
```

Set status explicitly on every MERGE/SET:
```cypher
SET n.status = COALESCE(n.status, 'planned')  // never leave null
```

### Rule 5: Post-Write Verification

After any batch ST creation, run this integrity check:

```cypher
// Verify: no orphan twins, no missing contracts, no null statuses
MATCH (root:AptSpan {name: $root})-[:DECOMPOSES_TO*1..6]->(atom)
WHERE NOT (atom)-[:DECOMPOSES_TO]->()
OPTIONAL MATCH (atom)-[:CRYSTALLIZES_TO]->(tw)
OPTIONAL MATCH (tw)-[:HAS_CONTRACT]->(ct)
WITH count(atom) AS atoms, count(tw) AS twins, count(ct) AS contracts
RETURN atoms, twins, contracts,
  atoms - twins AS missing_twin, twins - contracts AS missing_contract
// ALL differences must be 0
```

### Rule 6: Shared Contracts Use Explicit Multi-MERGE

When one Contract serves multiple Twins (e.g., `CT_OM_K8sInputValidation` shared by 3 compute twins), link explicitly:

```cypher
MATCH (ct:AptContract {name: 'CT_OM_K8sInputValidation'})
MATCH (st:SemanticTwin) WHERE st.name IN ['ST_OM_Compute_Create', 'ST_OM_Compute_Delete', 'ST_OM_Compute_Scale']
MERGE (st)-[:HAS_CONTRACT]->(ct)
```

Do NOT create separate Contract nodes with the same semantic meaning.

## What NOT to do here

- Do not write code. That's SCW.
- Do not decompose further. That's SP. If Contract writing reveals need for splitting, go back to /apt-sp.
- Do not attach Contracts to non-AtomicSpan nodes.
- Do not put acceptance_test or target_file on Contracts (those belong on Tasks).
- Do not create abstract/vague Contracts ("data" -> "result"). Concrete types only.
- **Do not use CREATE for Twin/Contract nodes** — always MERGE to prevent duplicates.
- **Do not leave status as null** — explicitly set on every node creation.
