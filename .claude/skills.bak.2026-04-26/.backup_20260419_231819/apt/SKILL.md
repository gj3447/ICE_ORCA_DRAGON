---
name: apt
description: >
  APT v5 orchestrator — coordinates the SP→ST→SCW phase flow and validates APT compliance.
  Use as the entry point for ANY development task. Project-agnostic (works for ANY SemanticAnchor).
  This skill determines which phase you're in, invokes the correct phase skill (/apt-sp, /apt-st, /apt-scw),
  and validates transitions between phases. Also use for APT health checks, KG integrity audits,
  and verifying that existing work follows APT axioms.
  Lean 4 formal axioms: lean/apt-axioms/AptAxioms/Basic.lean
  Trigger on: "start work on", "implement", "develop", "what phase am I in", "apt check", "validate apt",
  "audit kg", "where should this go", or any general development request.
---

# APT v5 Orchestrator

This is the master coordinator for APT development. It determines which phase applies and delegates to the phase-specific skill.

## Phase Detection

Before doing anything, determine the current phase by querying the KG:

```cypher
// What phase is the target work area in?
MATCH (span:AptSpan {name: $target_span})
OPTIONAL MATCH (span)-[:CRYSTALLIZES_TO]->(st:SemanticTwin)
OPTIONAL MATCH (st)-[:HAS_CONTRACT]->(c:AptContract)
OPTIONAL MATCH (c)-[:MATERIALIZES]->(src:SourceCodeNode)
RETURN span.name,
  CASE
    WHEN src IS NOT NULL THEN 'PH5/PH6: SCW (code exists, use /apt-scw for feedback)'
    WHEN c IS NOT NULL THEN 'PH5: SCW (contract ready, use /apt-scw to implement)'
    WHEN st IS NOT NULL THEN 'PH4: ST (twin exists but no contract, use /apt-st)'
    WHEN span:AtomicSpan THEN 'PH4: ST (atomic, ready to crystallize, use /apt-st)'
    ELSE 'PH3: SP (needs decomposition, use /apt-sp)'
  END AS current_phase
```

## Flow Control

Phases are NOT sequential steps that the whole project goes through together. Each **branch** (each Span path from SA to leaf) progresses independently. At any moment, branch A might be in PH3 (decomposing), branch B in PH4 (crystallizing), and branch C in PH5 (coding). This is by design — horizontal parallelism means sibling branches are fully independent.

```
User Request
    │
    ▼
[/apt] Phase Detection (per branch, not global)
    │
    ├── Branch not decomposed ──→ /apt-sp (PH2+PH3)
    │                                  │
    │                        C(S)=true ▼
    │                             /apt-st (PH4)
    │                                  │
    │                   Contract ready ▼
    │                            /apt-scw (PH5+PH6)
    │                                  │
    │               Discovery ─────────┘──→ back to /apt-sp or /apt-st
    │
    ├── Branch has AtomicSpan ──→ /apt-st (PH4)
    ├── Branch has Contract ────→ /apt-scw (PH5)
    └── Branch has code ────────→ /apt-scw (PH6 feedback)
```

Layers (L1, L2, ...) and phases (PH1-PH6) are NOT fixed positions. They are states that each branch occupies independently. The L*_ prefix is a legacy naming convention, not a semantic layer assignment.

## Core Concepts

### Task
A **Task** is a ~500-line vibe coding unit with explicit acceptance criteria. Tasks are the atomic unit of work in SCW — each Task maps to one Contract and produces one code artifact. The 500-line target keeps code reviewable and testable.

### Contract
A **Contract** is a typed agreement between parallel tasks. Think of it like a construction site where the electrical team and plumbing team agree on exact pipe positions before either starts work. Contracts specify input types, output types, and acceptance tests so that independently-developed tasks compose correctly. (DTOs/Schemas are one way to express contracts, but the concept is broader — it's the agreement itself, not just the data format.)

### SP Decomposition (DP Principle)
Span Planning follows the Dynamic Programming principle: decompose into independent subproblems with no cross-dependencies between siblings. Solved spans are memoized — once a branch reaches AtomicSpan, it never needs re-decomposition (unless discovery invalidates it).

### Gap Resolution Pipeline (Thompson Sampling)
When gaps are discovered during any phase, the Gap Resolution Pipeline applies Thompson Sampling:
- **70% exploitation** — resolve known gaps using existing KG knowledge and established patterns
- **30% exploration** — investigate novel approaches, discover new patterns, probe unknown areas

## Mold Flow (from KG)

The APT Mold Usage Protocol defines the operational flow:

```
Governance Mold ─STARTS_WITH→ Intent Mold ─NEXT→ Boundary Mold ─NEXT→ Execution Mold ─NEXT→ Assurance Mold
     │                │              │              │              │
     │ Hook Engine     │ Span Planner │ Contract Reg │ Work Queue   │ Eval Harness
     │ Agent Profile   │ Req Graph    │ Twin Registry│ Subagent Rtr │
     │                │              │              │ Runtime Trace│
     │                │              │              │              │
     └─── /apt ───────┘── /apt-sp ───┘── /apt-st ──┘── /apt-scw ──┘

     Memory Mold ─CROSS_CUTS→ (all phases)
     │ Memory Tier Manager / Reflection Memory / Checkpoint Ledger
```

## Validation Commands

### Full APT Health Check
```cypher
// 1. Contracts misplaced on non-AtomicSpan
MATCH (span)-[:HAS_CONTRACT]->(c:AptContract)
WHERE NOT span:AtomicSpan AND NOT span:SemanticTwin
RETURN 'VIOLATION: Contract on non-atomic' AS check, span.name, c.name

// 2. Horizontal independence violation (dynamic — checks any same-parent siblings)
MATCH (parent:AptSpan)-[:DECOMPOSES_TO]->(a:AptSpan)
MATCH (parent)-[:DECOMPOSES_TO]->(b:AptSpan)
WHERE a <> b AND (a)-[:DEPENDS_ON]->(b)
RETURN 'VIOLATION: Sibling dependency' AS check, a.name, b.name, parent.name

// 3. Unterminated decomposition paths
MATCH (leaf:AptSpan)
WHERE NOT (leaf)-[:DECOMPOSES_TO]->() AND NOT leaf:AtomicSpan
AND NOT leaf.name STARTS WITH 'SP_'
RETURN 'WARNING: Unterminated path' AS check, leaf.name

// 4. AtomicSpan without ST
MATCH (as:AtomicSpan)
WHERE NOT (as)-[:CRYSTALLIZES_TO]->()
AND NOT (as)-[:HAS_CONTRACT]->()
RETURN 'TODO: Needs crystallization' AS check, as.name

// 5. Contract without target_file
MATCH (c:AptContract)
WHERE c.target_file IS NULL AND c.status = 'defined'
RETURN 'WARNING: Missing target_file' AS check, c.name
```

### Data Quality Audit (added 2026-03-24)

Run these after any batch APT write operation. Each query MUST return empty or zero differences.

```cypher
// 6. Duplicate Twin nodes (same name, multiple nodes)
MATCH (tw:AptTwin)
WITH tw.name AS name, count(tw) AS cnt WHERE cnt > 1
RETURN 'VIOLATION: Duplicate Twin' AS check, name, cnt

// 7. Duplicate Contract nodes
MATCH (ct:AptContract)
WITH ct.name AS name, count(ct) AS cnt WHERE cnt > 1
RETURN 'VIOLATION: Duplicate Contract' AS check, name, cnt

// 8. Chain completeness: Atom → Twin → Contract (per project root)
MATCH (root:AptSpan {name: $root})-[:DECOMPOSES_TO*1..6]->(atom)
WHERE NOT (atom)-[:DECOMPOSES_TO]->()
OPTIONAL MATCH (atom)-[:CRYSTALLIZES_TO]->(tw)
OPTIONAL MATCH (tw)-[:HAS_CONTRACT]->(ct)
WITH count(atom) AS atoms, count(tw) AS twins, count(ct) AS contracts
WHERE atoms <> twins OR twins <> contracts
RETURN 'VIOLATION: Broken chain' AS check, atoms, twins, contracts

// 9. Null status on any APT node
MATCH (n) WHERE (n:AptSpan OR n:AptTwin OR n:AptContract OR n:AptSprint)
AND n.status IS NULL
RETURN 'VIOLATION: Null status' AS check, n.name, labels(n)

// 10. Naming convention violations (leaf atoms must be ATOM_*)
MATCH (root:AptSpan)-[:DECOMPOSES_TO*1..6]->(atom)
WHERE NOT (atom)-[:DECOMPOSES_TO]->()
AND NOT atom.name STARTS WITH 'ATOM_'
AND atom.name <> root.name
RETURN 'WARNING: Non-standard atom name' AS check, atom.name

// 11. Orphan contracts (not reachable from any Twin)
MATCH (ct:AptContract) WHERE NOT ()-[:HAS_CONTRACT]->(ct)
RETURN 'WARNING: Orphan contract' AS check, ct.name
```

### Neo4j Constraints (enforced at DB level)
```
apt_twin_unique:   AptTwin.name IS UNIQUE
apt_sprint_unique: AptSprint.name IS UNIQUE
```

Note: AptContract and AptSpan uniqueness cannot be enforced globally due to cross-project name collisions. Enforce at application level via MERGE (never CREATE) and post-write verification.

### Phase Transition Guards

**Before /apt-sp**: Does the target Span exist in KG? Is SA established?
```cypher
MATCH (sa:SemanticAnchor) RETURN sa.name  // should return project's SA node
MATCH (span:AptSpan {name: $target}) RETURN span.name, labels(span)
```

**Before /apt-st** (C(S) gate): All **5** crystallization criteria must be verified.
```cypher
MATCH (span:AptSpan {name: $target})
RETURN span:AtomicSpan AS is_atomic,
  span.can_express_output_type AS tau,     // (1) tau: Can express output as typed contract?
  span.type_captures_meaning AS sigma,      // (2) sigma: Semantically complete?
  span.can_write_function AS nu,            // (3) nu: Implementable as single ~500-line file?
  span.can_write_test AS iota,             // (4) iota: Can write concrete acceptance test?
  span.decomposition_diseconomy AS delta   // (5) delta: Further decomposition is diseconomical? (200~500 lines sweet spot)
// ALL 5 must be true. If any is null/false → return to /apt-sp
```

**Before /apt-scw** (Contract completeness gate):
```cypher
MATCH (st:SemanticTwin {name: $target})-[:HAS_CONTRACT]->(c:AptContract)
RETURN c.name,
  c.input_spec IS NOT NULL AS has_input,
  c.output_spec IS NOT NULL AS has_output,
  c.acceptance_test IS NOT NULL AS has_test,
  c.target_file IS NOT NULL AS has_target
// ALL must be true. If any is false → return to /apt-st
```

**After /apt-scw** (materialization verification):
```cypher
MATCH (c:AptContract {name: $ct})-[:MATERIALIZES]->(src:SourceCodeNode)
MATCH (st:SemanticTwin)-[:HAS_TASK]->(task:SemanticTask)
WHERE (st)-[:HAS_CONTRACT]->(c)
RETURN src.status, task.status  // both should be 'completed'/'passing'
```

## Project-Specific Invariants

Each SemanticAnchor may define domain invariants. Check with:
```cypher
MATCH (sa:SemanticAnchor {name: $project})-[:HAS_INVARIANT]->(inv)
RETURN inv.name, inv.description, inv.check_query
```

## When to Use Each Skill

| Situation | Skill | Why |
|-----------|-------|-----|
| "Implement feature X" | `/apt` → detect phase → delegate | Don't assume phase |
| "Plan the architecture for Y" | `/apt-sp` directly | Clearly SP work |
| "Write the contract for Z" | `/apt-st` directly | Clearly ST work |
| "Code the function for W" | `/apt-scw` directly | Clearly SCW work |
| "Check APT compliance" | `/apt` validation | Orchestrator handles |
| "Where does this feature go?" | `/apt` + KG query | Phase detection |

## Feedback / 불만사항 / 문의사항

APT 방법론이나 스킬 사용 중 문제가 발생하면 KG에 기록해주세요. 방법론 개선의 핵심 입력입니다.

### 피드백 기록 방법
```cypher
MERGE (fb:AptFeedback {name: $title})
SET fb.category = $category,  // Bug, Confusion, Missing, Improvement, Violation
    fb.description = $description,
    fb.context = $what_you_were_doing,
    fb.phase = $which_phase,  // SP, ST, SCW
    fb.skill = $which_skill,  // apt-sp, apt-st, apt-scw
    fb.severity = $severity,  // critical, major, minor, suggestion
    fb.status = 'open',
    fb.created_at = datetime()
WITH fb
MATCH (queue:AptFeedbackQueue {name: 'APT_Feedback_Queue'})
MERGE (queue)-[:HAS_FEEDBACK]->(fb)
```

### 카테고리
| 카테고리 | 언제 사용 |
|---------|---------|
| **Bug** | 스킬이 잘못된 안내를 하거나 KG 쿼리가 틀린 경우 |
| **Confusion** | APT 개념이 혼란스러워서 clarification이 필요한 경우 |
| **Missing** | APT에 빠진 규칙/제약/도구가 있는 경우 |
| **Improvement** | 더 나은 방법이 있다고 생각되는 경우 |
| **Violation** | APT 위반 사례를 발견한 경우 (PH3→PH5 직행 같은) |

### 기존 피드백 확인
```cypher
MATCH (queue:AptFeedbackQueue)-[:HAS_FEEDBACK]->(fb:AptFeedback)
WHERE fb.status = 'open'
RETURN fb.name, fb.category, fb.severity, fb.created_at
ORDER BY fb.created_at DESC
```

### 피드백 해결 처리
```cypher
MATCH (fb:AptFeedback {name: $title})
SET fb.status = 'resolved',
    fb.resolution = $how_it_was_fixed,
    fb.resolved_at = datetime()
```

문제를 발견하면 **즉시 기록**하세요. 나중에 기억 안 납니다. 사소한 것도 기록하세요 — 사소한 혼란이 쌓이면 큰 APT 위반으로 이어집니다.

## Theoretical Foundations

APT is informed by concepts from multiple disciplines:

| Domain | Influence |
|--------|-----------|
| **Dynamic Programming** | SP decomposition follows DP principle — independent subproblems, memoization of solved spans |
| **Diffusion** | Iterative refinement from noise to structure (SA → SP → ST → SCW) |
| **Category Theory** | Contracts as morphisms, composition guarantees, functorial mappings |
| **Von Neumann Architecture** | Stored-program analogy — KG is memory, agents are processors |
| **Monte Carlo / Thompson Sampling** | Gap Resolution Pipeline — 70% exploitation (known gaps), 30% exploration (discovery) |
| **DDD (Domain-Driven Design)** | Bounded contexts, ubiquitous language, aggregates |
| **Unix Philosophy** | Do one thing well, compose via pipes (contracts as pipes) |
| **CSP (Communicating Sequential Processes)** | Parallel tasks communicate only through contracts, no shared state |
| **OSI Model** | Layered abstraction with clean interfaces between layers |
| **Scientific Method** | Kuhn (paradigm shifts in schema evolution), Goedel (incompleteness — no perfect ontology), Strange Loop (self-referential KG), Autopoiesis (self-maintaining system) |

## KG Reference Convention

All code files MUST include KG reference comments linking to their originating Task and Contract nodes:

```python
# KG: TASK_xxx — links this file to its SemanticTask node
# KG: CONTRACT_xxx — links this file to its AptContract node
```

This enables traceability from code back to the KG planning artifacts.

## Reference

- `references/getting_started.md` — **Start here.** Glossary, PH1/PH2 bootstrap, Hello World example, "which skill first?" decision tree.
- `references/handoff_and_ascent.md` — Phase handoff checklists (SP→ST→SCW), feedback data contracts, bottom-up ascent protocol.
- `references/full_methodology.md` — Complete APT v5 spec (498 lines, all 17 clarification notes).
- Phase skills: `/apt-sp`, `/apt-st`, `/apt-scw` each have their own `references/kg_tools.md` with error recovery and multi-agent protocols.
