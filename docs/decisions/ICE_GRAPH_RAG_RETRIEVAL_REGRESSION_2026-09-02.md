# Versioned GraphRAG retrieval regression standard

Date: 2026-09-02

Status: accepted

## Decision

`ontology/graphrag-evaluation-suite.json` is the reviewable, versioned
retrieval-regression suite for the repository-local GraphRAG surface. Each case
fixes a stable natural-language query, expected graph-qualified canonical node
locator, optional graph selector and bounded expansion depth. The suite is a
control for navigation quality: it does not test scientific truth, citation
entailment, model reasoning, or a calculation result.

Two read-only commands use that suite:

```bash
./ice graphrag eval --limit 12 --json
./ice graphrag diff --base HEAD --limit 12 --json
```

`eval` evaluates the semantically valid working ontology. It reports
expected-locator pass rate, mean reciprocal rank, mean expected-locator recall
and per-case ranks.
`diff` evaluates the same current suite over one committed ontology revision and
the semantically valid working ontology, then reports rank, retrieved-unit and pass-status
movement. Its historical index retains any semantic-validation error as report
metadata so a previously committed, later-corrected non-retrieval defect does
not make comparison impossible. The working tree remains required to pass the
native collection validator.

The MCP server exposes the same read-only operations as
`ice_graphrag_evaluate` and `ice_graphrag_diff`.

## Standard next-work workflow

Use the smallest appropriate subset. For a question or a proposal, retrieve and
plan before editing a graph or writing a runner:

```bash
./ice graphrag search "<one bounded question>" --graph <key> --depth 1
./ice agent plan "<one bounded question>" --graph cpt --json
```

For a material canonical graph change, verify both the direct impact and
navigation regression before accepting the edit:

```bash
./ice harness impact <registered-repository-path>
# edit the canonical graph and collection record only when the material record changed
./ice ontology review --graph <key|all> --base HEAD
./ice graphrag eval --limit 12 --json
./ice graphrag diff --base HEAD --limit 12 --json
npm run graph:check
```

Use `./ice ontology export --format jsonld` only when a generated interchange
view is actually needed. It remains derived output, not a second graph source.
Use OpenAlex only as bounded source discovery; read a primary source before
adding an evidence or source assertion.

Add a suite case only when its canonical locator, wording and use in future
navigation review are stable. Rename or delete a case only with its matching
canonical graph change and an inspected revision diff. Routine prose edits,
intermediate experiments and every bounded calculation do not require a new
case, graph record, agent checkpoint or repro manifest.

## Boundaries

- A passing retrieval case neither validates a scientific conclusion nor
  authorizes execution, promotion or a successor task.
- A rank change requires human inspection of native graph context, sources and
  the semantic review. It is not an automatic graph repair.
- The current raw `RESULT.json` remains the complete execution-check ledger;
  this suite stores only canonical navigation locators.
- The planner and MCP tools are read-only review aids. They cannot write a
  runner, create an ontology record or invoke `./ice run`.

This standard adds an auditable quality control around the native graph without
introducing a vector database, model-extracted facts, an external graph write or
an autonomous research loop.
