# ICE graph-aware harness

> **Status:** ACTIVE — graph-aware engineering layer for the computational workbench
> **Effective:** 2026-09-01
> **Authority:** connects repository-local research graphs to context lookup, change-impact review,
> and integrity verification.
> **Non-authority:** physical claims, execution authorization, automatic successor selection, ontology
> promotion, or reopening the killed Ragnarok route.

## Decision

New work uses a **graph-aware, human-directed harness**.  The existing typed ontology remains the
small, material research-memory graph; raw `RESULT.json` remains the single source for a calculation's
complete check ledger.  The harness makes the graph operational for engineering decisions without
turning it into a recursive research contract.

The model is PROV-informed: source, policy, artifact, evidence, scope, claim, and open-problem records
are distinct graph entities, and their explicit relations supply review context.  It deliberately does
not claim that the emerging labels “graph engineering”, “harness engineering”, and “loop engineering”
form one universal standard.  Here they mean the bounded repository implementation below.

## Loop

```text
human selects one independently scoped question
  -> ./ice harness context <node>         (evidence/scope/policy/open-problem context)
  -> change a clean committed runner or document
  -> ./ice run <name>                     (when a calculation is appropriate)
  -> raw result / adjacent note records actual output and failure
  -> ./ice harness impact <path>          (registered change context)
  -> material graph change? -- yes --> update ontology -> ./ice harness check
                         \-- no  --> retain the raw record only
  -> human decides whether another independent question is justified
```

The arrows are an observability and review loop, not a sequential scientific gate.  In particular,
`context`, `impact`, and `check` never grant an execution permit and never create an automatic next
task.  A new calculation still needs its own question, inputs, assumptions, main failure class, and
proportionate control under the lean rules.

## Harness commands

```bash
./ice harness context <node-id> [--graph <key>] [--depth 0..32] [--limit 1..256] [--json]
./ice harness impact <repository-relative-path> [--graph <key>] [--depth 0..32] [--limit 1..256] [--json]
./ice harness check [--graph <key>] [--json]
```

- `context` is a bounded graph neighborhood, grouped into claims, evidence, scope, sources, artifacts,
  policies, and open problems. `--limit` defaults to 64 returned nodes and reports truncation explicitly.
  It is designed to show what a proposed change may depend on or narrow; it is not a work queue.
- `impact` matches exact hash-tracked artifact/policy paths and graph/guide manifests.  An unregistered
  path is reported honestly as unregistered; that does not force a node to be created.
- `check` performs the full collection hash/evidence validation used by `ontology validate`, presented
  as a single harness integrity check.  A pass verifies the record structure and tracked bytes, not a
  numerical or physical interpretation.

The command payload fixes `automatic_follow_up=false`, `execution_authorization=NOT_GRANTED`, and
`raw_result_check_ledger=SINGLE_SOURCE` so that callers cannot mistake a graph traversal for research
approval.

## Why this is useful

1. **Impact before overwrite.** A hash-tracked artifact or policy can be located with its nearby claims,
   evidence, scopes, and open problems before a change rewrites the provenance record.
2. **Evidence stays local and inspectable.** The raw result stays complete while the graph stores only
   the small set of locators needed to navigate it; this avoids duplicated ledgers and drift.
3. **Failure stays visible.** Contradicted, inconclusive, and open nodes remain in the same context as
   supported nodes, so an apparent positive result cannot quietly bypass its recorded exclusions.
4. **Cheap integrity boundary.** One explicit post-change check confirms IDs, relations, hashes, and
   evidence-snapshot links without making every calculation a full historical replay.

## Boundaries and sources

This augments, and does not replace,
[`ICE_LEAN_RESEARCH_RULES_2026-08-31.md`](ICE_LEAN_RESEARCH_RULES_2026-08-31.md) or
[`ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md`](ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md).  The
numbered Phase 51–56 reconciliation route remains killed.  New computation remains the clean,
unnumbered bounded core governed by `./ice run`.

- The [W3C PROV Primer](https://www.w3.org/TR/prov-primer/) supplies the provenance distinction among
  entities, activities, agents, derivations, and plans used as the conceptual basis here.
- Kim and Hwang's [*Harness Engineering: A Governance Framework for AI-Driven Software Engineering*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6372119)
  motivates treating context, constraint, and convergence as distinct engineering concerns.  It is a
  recent framing, not a governing external standard for this repository.
