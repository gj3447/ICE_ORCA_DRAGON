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
4. `./ice agent plan <question>` creates a serializable workflow checkpoint. The
   only completed automatic work is bounded local retrieval. Source expansion,
   evidence review, calculation design, and every `./ice run` decision remain
   explicitly human-reviewed; its execution step is `NOT_AUTHORIZED`.
5. The same surfaces are available over local stdio MCP as
   `ice_graphrag_summary`, `ice_graphrag_search`,
   `ice_literature_neighbors`, and `ice_research_workflow_plan`.

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
tool boundaries, inspectable state, and evaluation before added orchestration
complexity. It does not call a model API or require an API key. See [OpenAI's
current model and agent guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5).

## Evaluation and upgrade boundary

`evaluateGraphRag` is a deterministic retrieval evaluator for a deliberately
small set of stable, predeclared canonical node locators. It reports retrieval
recall only. `evaluateResearchAgentRouting` checks that an emitted workflow
still requires human review and cannot authorize execution. Neither assesses a
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

PROV-O and RO-Crate exports remain separate interoperability decisions. Their
serializations can describe provenance and packaging, but cannot replace the
native evidence semantics or ratify a conclusion. See [PROV-O](https://www.w3.org/TR/prov-o/)
and the [RO-Crate specification](https://www.researchobject.org/ro-crate/specification.html).

## Operating examples

```bash
./ice graphrag summary --json
./ice graphrag search "bounded provenance evidence" --graph cpt --limit 12 --depth 1
./ice literature neighbors W2741809807 --limit 10 --json
./ice agent plan "Which primary source constrains this finite result?" --graph cpt --json
npm run --silent mcp
```

All output is retrieval, discovery, or human-review planning context. It does
not change a claim, add an ontology record, run a numerical kernel, persist an
agent checkpoint, approve a calculation, or create a successor task.
