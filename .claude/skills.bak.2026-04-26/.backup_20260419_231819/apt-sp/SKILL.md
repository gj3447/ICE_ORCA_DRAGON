---
name: apt-sp
description: >
  APT SemanticPyramid (SP) phase — universal recursive Span decomposition.
  Invoke when: planning any project's architecture, decomposing features, creating Spans,
  analyzing where new work fits in the KG hierarchy, or breaking big tasks into smaller pieces.
  Project-agnostic (works for ANY SemanticAnchor in the KG).
  Enforces: D(S) recurrence, C(S) crystallization predicate, 6 constraints,
  dense INFORMED_BY linking, RefinementGate verification.
  Lean 4 formal axioms: lean/apt-axioms/AptAxioms/Basic.lean
  Documented violation (PH3->PH5 skip) proves: never skip SP.
---

# APT SP: SemanticPyramid Recursive Descent (Universal)

# KG: TASK_Skill_APT_SP
# KG: CONTRACT_Skill_APT_SP

SP is **one world** containing Spans in layers. Decompose abstract intent into concrete, implementable units. Never implement here — that belongs to ST and SCW.

## Mathematical Foundation

### Definition: SemanticPyramid

Let SA be a SemanticAnchor (project identity, exactly 1 per project). SP is the set of all Spans reachable from SA via DECOMPOSES_TO:

```
SP = { S | SA -[:DECOMPOSES_TO*]-> S }
```

SP forms a **directed acyclic graph** (DAG), not a tree. Spans have N:N parent-child relationships (spider web topology). Same-layer siblings are fully independent (zero mutual dependency).

### The Decomposition Function D(S)

D(S) is a **recurrence relation** analogous to Dynamic Programming:

```
D(S):
  IF C(S) = true  ->  label S as AtomicSpan, hand off to /apt-st
  IF C(S) = false  ->  decompose S into {S_1, ..., S_k} where k >= 2
                        for each S_i: apply D(S_i)
```

**Termination**: All paths reach C(S)=true in finite steps (TerminationGuarantee constraint). There is no depth limit — recursion stops when and only when C(S)=true.

### The Crystallization Predicate C(S)

```
C(S) = tau(S) AND sigma(S) AND nu(S) AND iota(S) AND delta(S)
```

All **five** conditions must hold simultaneously:

| # | Symbol | Condition | Test | Failure action |
|---|--------|-----------|------|----------------|
| 1 | **tau(S)** | Type Expressibility | `def f(x: ConcreteDTO) -> ConcreteDTO` writable? | Split by output type boundary |
| 2 | **sigma(S)** | Semantic Completeness | One function captures full meaning? | Narrow domain scope |
| 3 | **nu(S)** | Implementation Feasibility | Single file 200~500 lines? | Isolate unknowns into sub-Span |
| 4 | **iota(S)** | Test Feasibility | `assert result.field == specific_value` writable? | Sharpen spec with examples |
| 5 | **delta(S)** | Decomposition Diseconomy | Splitting creates <100-line fragments? | Merge up if too fine, split if >500 |

**C(S) is the ONLY termination mechanism.** No heuristic depth limits.

### The Crystallization Verification Procedure

Run in order. Stop at first FAIL:

```
Step 1 [tau]: Can I write `def xxx(input: ConcreteDTO) -> ConcreteDTO`?
  FAIL if types are vague ("data", "result", "object", "any")
  Types must be concrete, domain-specific, singular

Step 2 [sigma]: Does one function capture the FULL meaning?
  FAIL if 2+ independent verbs needed ("X and also Y")
  One Span = one semantic unit

Step 3 [nu]: Will implementation be 200~500 lines in ONE file?
  FAIL if >500 (decompose further) or <100 (merge with sibling)
  Sweet spot: balances cohesion with manageability

Step 4 [iota]: Can I write `assert result.field == specific_value`?
  FAIL if criteria are fuzzy ("works correctly", "properly handles")
  Must have concrete, verifiable test assertions

Step 5 [delta]: Would splitting produce fragments too small to stand alone?
  PASS if further splitting creates >overhead than it saves
  FAIL if separable concerns still exist
```

All 5 PASS -> AtomicSpan. Any FAIL -> the failed condition tells you HOW to decompose.

## Before You Start: Query the KG

Never create a Span without checking what exists. Duplication is the most common SP error.

```cypher
-- Find existing Spans near your work area
MATCH (n:AptSpan) WHERE n.name CONTAINS $keyword
RETURN n.name, n.description, labels(n), n.is_atomic

-- Find the SemanticAnchor for the project
MATCH (sa:SemanticAnchor) WHERE sa.name CONTAINS $project
RETURN sa.name, sa.description

-- Trace decomposition tree from any ancestor
MATCH path = (ancestor:AptSpan {name: $name})-[:DECOMPOSES_TO*1..10]->(leaf)
WHERE NOT (leaf)-[:DECOMPOSES_TO]->()
RETURN [n IN nodes(path) | n.name] AS chain, length(path) AS depth
ORDER BY depth DESC LIMIT 10

-- Check for orphan LeafSpans (incomplete decomposition)
MATCH (sa:SemanticAnchor {name: $sa_name})-[:DECOMPOSES_TO*]->(leaf:AptSpan)
WHERE NOT (leaf)-[:DECOMPOSES_TO]->() AND NOT leaf:AtomicSpan
RETURN leaf.name AS needs_evaluation, leaf.depth AS depth
```

## Six Constraints

| Constraint | Formal | Enforcement |
|-----------|--------|-------------|
| **BranchingInvariant** | k >= 2 in D(S) | Decomposing into 1 child is renaming, not decomposing |
| **TerminationGuarantee** | All paths finite | If stuck, abstraction level is wrong — re-approach |
| **HorizontalParallelism** | siblings: zero mutual dependency | `(a)-[:DEPENDS_ON]->(b)` where same parent = **decomposition error** |
| **SpanPlanningNature** | Spans are plans | Spans describe meaning, never code |
| **DepthInvariant** | depth = hops from SA | AtomicSpan at hop 2 and hop 9 equally valid if C(S)=true |
| **NamePrefixCaveat** | L*_ = legacy | `is_atomic` property and C(S) determine truth, not name prefix |

## Dense Linking Before Descent (CRITICAL)

**Axiom**: Span external link density improves descent quality. Higher INFORMED_BY count = better decomposition.

Before applying D(S), enrich the Span:

```cypher
-- Find relevant knowledge to link
MATCH (n) WHERE n.name CONTAINS $concept
AND any(l IN labels(n) WHERE l IN [
  'DesignPattern', 'SymConcept', 'AgentSkill', 'Agent',
  'AptPrinciple', 'AptConstraint', 'AptGate', 'AptClarificationNote',
  'AptGapAnalysis', 'AptIssue', 'MCPServer', 'Domain'
])
RETURN n.name, labels(n), n.description LIMIT 20

-- Link knowledge
MATCH (s:AptSpan {name: $span_name})
MATCH (k {name: $knowledge_name})
MERGE (s)-[:INFORMED_BY {reason: $why_relevant}]->(k)
```

**Minimum 5 INFORMED_BY per Span before decomposing.** More is better.

## Creating a Span

```cypher
MATCH (parent:AptSpan {name: $parent_name})
MERGE (child:AptSpan:SymConcept {name: $child_name})
SET child.description = $description,
    child.depth = parent.depth + 1,
    child.is_atomic = false,
    child.status = 'active',
    child.created_at = datetime()
MERGE (parent)-[:DECOMPOSES_TO]->(child)
```

Then immediately enrich with INFORMED_BY (see above).

## RefinementGate (post-decomposition verification)

After creating children, verify the decomposition quality:

| Check | Question | Cypher verification |
|-------|----------|-------------------|
| **Coverage** | Do children collectively cover parent's full meaning? | Compare parent.description scope vs union of child descriptions |
| **Consistency** | No contradictions between children? | Review child descriptions for conflicts |
| **Independence** | No sibling dependencies? | `MATCH (p)-[:DECOMPOSES_TO]->(a), (p)-[:DECOMPOSES_TO]->(b) WHERE a<>b AND (a)-[:DEPENDS_ON]->(b) RETURN a,b` must be empty |

```cypher
-- Independence check (MUST return empty)
MATCH (parent:AptSpan {name: $parent_name})-[:DECOMPOSES_TO]->(a:AptSpan)
MATCH (parent)-[:DECOMPOSES_TO]->(b:AptSpan)
WHERE a <> b AND (a)-[:DEPENDS_ON]->(b)
RETURN a.name AS dependent, b.name AS dependency
```

If any check fails, re-decompose.

## AtomicSpan vs LeafSpan

- **LeafSpan**: currently has no children (state). May need further decomposition.
- **AtomicSpan**: C(S)=true verified (judgment). Ready for /apt-st.

A LeafSpan where C(S)=false is an **incomplete decomposition**, not an AtomicSpan.

```cypher
-- Mark as AtomicSpan after C(S) passes
MATCH (s:AptSpan {name: $span_name})
SET s:AtomicSpan, s.is_atomic = true,
    s.crystallization_check = $check_results
```

## Output

When SP phase completes for a branch:
- Span nodes exist with DECOMPOSES_TO relationships forming a DAG
- Each Span has >= 5 INFORMED_BY links to existing KG knowledge
- Leaf Spans are labeled AtomicSpan with C(S) check recorded
- RefinementGate passed for each decomposition level
- No sibling dependencies (HorizontalParallelism verified)
- Ready to hand off to /apt-st for crystallization

## Write-Time Integrity Rules (CRITICAL)

These rules prevent naming/duplication issues discovered during the 2026-03-24 audit.

### Rule 1: MERGE, Never CREATE for Spans
```cypher
-- CORRECT
MERGE (child:AptSpan:SymConcept {name: $child_name})
-- WRONG
CREATE (child:AptSpan:SymConcept {name: $child_name})
```

### Rule 2: Leaf Atom Naming Convention
Leaf atoms (C(S)=true) MUST use `ATOM_{PROJECT}_` prefix:
```cypher
// When marking as atomic
MATCH (s:AptSpan {name: $span_name})
// If name doesn't start with ATOM_, rename it
WITH s, CASE WHEN NOT s.name STARTS WITH 'ATOM_'
  THEN 'ATOM_' + replace(replace(s.name, 'SP_', ''), 'SPAN_', '')
  ELSE s.name END AS correctName
SET s.name = correctName, s:AtomicSpan, s.is_atomic = true
```

Intermediate spans use `SPAN_{PROJECT}_L{level}_` prefix. Legacy `SP_*` prefix is forbidden for new nodes.

### Rule 3: Status Must Not Be Null
```cypher
SET child.status = COALESCE(child.status, 'active')  // never null
```

Valid statuses: `planned | in_progress | active | completed | archived | superseded | deferred | blocked`

## What NOT to do here

- Do not write Contracts. That's ST.
- Do not write code. That's SCW.
- Do not skip C(S) verification. The documented PH3->PH5 violation happened because C(S) was skipped.
- Do not create Spans without INFORMED_BY links. Blind decomposition produces poor children.
- **Do not use CREATE for Span nodes** — always MERGE to prevent duplicates.
- **Do not use legacy SP_/SPAN_ prefix for new leaf atoms** — use ATOM_ prefix.
