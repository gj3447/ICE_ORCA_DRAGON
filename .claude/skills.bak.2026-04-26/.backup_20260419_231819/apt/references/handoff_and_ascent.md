# Phase Handoff Protocol & Bottom-Up Ascent

## SP → ST Handoff

### What /apt-sp must do before handing off:

1. **Label** the Span as AtomicSpan:
```cypher
MATCH (s:AptSpan {name: $span_name})
SET s:AtomicSpan,
    s.is_atomic = true,
    s.can_express_output_type = true,
    s.type_captures_meaning = true,
    s.can_write_function = true,
    s.can_write_test = true
```

2. **Verify** dense KG links exist (at least 3 USES/INFORMED_BY):
```cypher
MATCH (s:AptSpan {name: $span_name})-[r]-()
WHERE type(r) IN ['USES','USES_PATTERN','INFORMED_BY']
RETURN count(r) AS density  // must be ≥ 3
```

### What /apt-st checks on entry:
```cypher
MATCH (s:AtomicSpan {name: $span_name})
WHERE s.can_express_output_type = true
AND s.type_captures_meaning = true
AND s.can_write_function = true
AND s.can_write_test = true
RETURN s.name  // must return exactly 1 row
```

If query returns empty → rejected, return to /apt-sp.

---

## ST → SCW Handoff

### What /apt-st must do before handing off:

1. ST node created with CRYSTALLIZES_TO from AtomicSpan
2. Contract with ALL fields populated:
```cypher
MATCH (st:SemanticTwin {name: $st_name})-[:HAS_CONTRACT]->(c:AptContract)
RETURN c.input_spec IS NOT NULL AS has_input,
       c.output_spec IS NOT NULL AS has_output,
       c.precondition IS NOT NULL AS has_pre,
       c.postcondition IS NOT NULL AS has_post,
       c.acceptance_test IS NOT NULL AS has_test,
       c.target_file IS NOT NULL AS has_target
// ALL must be true
```
3. Task with acceptance criteria:
```cypher
MATCH (st:SemanticTwin {name: $st_name})-[:HAS_TASK]->(t:SemanticTask)
RETURN t.name, t.acceptance_criteria IS NOT NULL AS has_criteria
```

### What /apt-scw checks on entry:
Same query as above. If any field is null → rejected, return to /apt-st.

---

## SCW → SP Feedback (Discovery: new Span needed)

### Data to carry back:
```cypher
MERGE (note:AptArchNote {name: 'DISCOVERY_' + $timestamp})
SET note.description = $what_was_found,
    note.source_phase = 'SCW',
    note.source_contract = $contract_name,
    note.action_needed = $action,  // one of the enum below
    note.created_at = datetime()
```

### action_needed enum:
| Value | Meaning |
|-------|---------|
| `new_span_needed` | Missing functionality not covered by any Span |
| `span_too_coarse` | Target file needs multiple concerns → split the parent Span |
| `dependency_missing` | External dependency not in KG → add to Requirement Graph |
| `integration_gap` | Two Contracts don't type-match → revise one or both |

---

## SCW → ST Feedback (Contract revision needed)

```cypher
MATCH (st:SemanticTwin {name: $st_name})
SET st.status = 'stale',
    st.stale_reason = $reason,
    st.stale_at = datetime()
```

When to mark stale vs create new:
- **Stale**: acceptance test was wrong, type signature needs change → fix existing Contract
- **New ST**: the AtomicSpan itself was wrong (too broad/narrow) → unmark AtomicSpan, return to SP, re-decompose, create fresh ST

---

## Bottom-Up Ascent Protocol

When you encounter existing code without APT structure (e.g., `lx3/pipeline/`, legacy `prism/modules/`):

### Step 1: Code → Contract Inference
Read the source file. Extract:
- Function signature → `input_spec`, `output_spec`
- Docstring/comments → `description`, `precondition`
- Existing tests → `acceptance_test`
- File path → `target_file`

```cypher
MERGE (c:AptContract:PrismSemanticContract {name: 'CT_' + $inferred_name})
SET c.input_spec = $input_from_code,
    c.output_spec = $output_from_code,
    c.acceptance_test = $tests_from_code,
    c.target_file = $file_path,
    c.source = 'bottom_up_inference',
    c.status = 'inferred'
```

### Step 2: Contract → ST
```cypher
MERGE (st:SemanticTwin:AptNode {name: 'ST_' + $name})
SET st.status = 'inferred'
MERGE (st)-[:HAS_CONTRACT]->(c)
// Also create MATERIALIZES to existing code
MERGE (src:SourceCodeNode {name: 'SRC_' + $name})
SET src.file_path = $file_path, src.status = 'pre_existing'
MERGE (c)-[:MATERIALIZES]->(src)
```

### Step 3: ST → Span Reconstruction
```cypher
// Create parent Span and attach
MERGE (span:AptSpan:AtomicSpan {name: $span_name})
SET span.is_atomic = true, span.source = 'bottom_up_reconstruction'
MERGE (span)-[:CRYSTALLIZES_TO]->(st)
// Attach to existing SP hierarchy
MATCH (parent:AptSpan {name: $parent_span})
MERGE (parent)-[:DECOMPOSES_TO]->(span)
```

### Step 4: Validate
```cypher
// Check the reconstructed chain is reachable from SA
MATCH path = (sa:DefinitionAnchor)-[*1..10]->(span:AptSpan {name: $span_name})
RETURN length(path) AS hops  // should be > 0
```

Bottom-up inferred nodes get `source: 'bottom_up_inference'` so they can be distinguished from top-down designed nodes and reviewed.
