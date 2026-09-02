# Evidence-first GraphRAG and human-approved agent orchestration

Date: 2026-09-01

Status: accepted

## Decision

Add a repository-local, deterministic GraphRAG retrieval layer and a serializable
research-agent workflow planner around the existing research ontology. They are
read-only engineering aids; the canonical `research-graph/v1` JSON remains the
authored graph, and raw `RESULT.json` remains the complete execution-check ledger.

The available components are:

1. `./ice graphrag summary` and `./ice graphrag search` project each canonical
   ontology node into a stable, graph-qualified TextUnit. A result preserves the
   node locator, source/artifact/policy locator where applicable, structural
   community, score components, and explicit-relation breadcrumbs.
2. The local index uses deterministic Louvain communities over declared ontology
   relations, BM25, a deterministic lexical hash vector, and depth-0--3 relation
   expansion. It is built at query time from the native graph; it does not write a
   vector database or a second graph serialization.
3. `./ice literature neighbors <OpenAlex-work-id>` retrieves one bounded external
   citation neighborhood: the selected work, at most 20 outgoing-reference IDs,
   at most 20 related-work IDs, and at most 20 incoming citing works. It makes two
   time-stamped, read-only OpenAlex requests rather than crawling the literature
   graph.
4. `./ice agent plan <question>` creates a read-only serializable workflow
   preview. The v2 plan applies the active TOE navigation profile after bounded
   local retrieval. Only a specifically anchored current-blocker question can
   reach human calculation-design review; downstream, supporting, and
   unanchored questions emit `STOP_OR_REFRAME`.
5. `./ice agent run create|review|show|audit` is the explicit durable layer.
   It pins resolved HEAD, the complete TypeScript control plane and its launcher/package
   manifests, collection, selected graph, and retrieved local document hashes;
   persists under ignored `.ice/agent-runs/`; appends SHA-256-chained typed human
   decisions; refuses stale trace tips and revision drift; and permits only
   ROUTE → EVIDENCE → DESIGN → `CLOSED` or an explicit
   `STOPPED`. Neither terminal state grants core-progress or execution authority.
6. The read-only surfaces are available over local stdio MCP as
   `ice_graphrag_summary`, `ice_graphrag_search`,
   `ice_literature_neighbors`, `ice_research_workflow_plan`,
   `ice_research_workflow_evaluate`, and `ice_research_run_audit`. MCP can
   inspect and audit but cannot create or review a persisted run.

## Why this is the present implementation

Microsoft GraphRAG identifies TextUnit provenance, entity/relation extraction,
community hierarchy, community summaries, and local/global/DRIFT retrieval as
important patterns. This repository can obtain the first and the structural
community/retrieval parts directly from its already-curated ontology, without
silently introducing model-extracted facts. The implementation deliberately calls
its representation a **deterministic lexical hash vector**, not a learned semantic
embedding, and calls its community description a **structural summary**, not an
LLM summary. See the [GraphRAG index documentation](https://github.com/microsoft/graphrag/blob/main/docs/index.md)
and its [TextUnit data-flow documentation](https://github.com/microsoft/graphrag/blob/main/docs/index/default_dataflow.md).

OpenAlex has references, cited-by relationships, and related works suitable for
bounded primary-source discovery; its returned metadata is not a citation
entailment check. See the [OpenAlex API recipes](https://help.openalex.org/how-to/api-recipes/).

MCP annotations express host-facing hints rather than enforcement. Local tools
therefore declare `openWorldHint: false`; the OpenAlex tools declare
`openWorldHint: true`; all tools enforce read-only behavior in their own
implementation. See the [MCP tool-annotation guidance](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/).

The workflow state machine follows current agent-engineering practice of explicit
tool boundaries, inspectable state, durable checkpoints, typed handoffs, and
evaluation before added orchestration complexity. It does not call a model API
or require an API key. See [OpenAI's
current model and agent guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5).

MCP 2025-11-25 Tasks are intentionally not used. They are an experimental
deferred-result protocol for long-running requests, while this repository needs
a local human-review record that cannot become an execution request. The
durable run state therefore stays an explicit CLI-owned file; every MCP tool
remains synchronous and read-only.

## Evaluation and upgrade boundary

`evaluateGraphRag` is a deterministic retrieval evaluator for a deliberately
small set of stable, predeclared canonical node locators. It reports retrieval
recall only. `evaluateResearchAgentRouting` checks that an emitted workflow
requires blocker-route review, cannot bypass an upstream dependency into
calculation design, and cannot authorize either execution or a core-progress
label. `./ice agent eval` additionally runs fixed current-blocker, downstream,
supporting, and unanchored cases through the durable ROUTE/EVIDENCE/DESIGN
handoffs, including final event-chain self-consistency and non-authorization audits. The
chain detects accidental or partial rewrites but is not a signature against a writer who
can recompute it. None assesses a
physical conclusion, citation correctness, scientific truth, or model reasoning.

Before enabling learned embeddings, LLM entity/relation extraction, hierarchical
LLM community reports, an external vector store, or an execution-capable agent,
add a reviewable benchmark containing:

- source-backed retrieval cases and a frozen baseline;
- citation-accuracy review for external links;
- measured retrieval quality and failure slices relative to this deterministic
  baseline; and
- agent route and human-handoff evaluation, including a test that execution is
  still impossible without separate authorization.

PROV-O and RO-Crate exports remain separate interoperability layers. Their
serializations describe provenance and packaging, but cannot replace the
native evidence semantics or ratify a conclusion. See [PROV-O](https://www.w3.org/TR/prov-o/)
and [RO-Crate Metadata Specification 1.3](https://w3id.org/ro/crate/1.3).

## Operating examples

```bash
./ice graphrag summary --json
./ice graphrag search "bounded provenance evidence" --graph cpt --limit 12 --depth 1
./ice literature neighbors W2741809807 --limit 10 --json
./ice agent eval --json
./ice agent plan "Gate 1 original joint cycle and signed global intersection vector" --graph cpt --json
./ice agent run create "Gate 1 original joint cycle and signed global intersection vector" --id g1-review --graph cpt --json
./ice agent run show g1-review --json
./ice agent run review g1-review --stage route --decision approve --rationale "reviewed scope" --tip <current-trace-tip>
./ice agent run audit g1-review --json
npm run --silent mcp
```

All output is retrieval, discovery, or human-review context. The TOE
objective profile is navigation policy rather than evidence. Output does not
change a claim, add an ontology record, run a numerical kernel, approve core
progress or a calculation, or create a successor task. Only the explicit
`agent run create|review` commands write local ignored workflow state.
