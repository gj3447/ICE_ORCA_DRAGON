# Read-only research MCP and skill integration (2026-09-01)

## Decision

Adopt the MCP TypeScript SDK v2 through a repository-local **stdio, read-only** server and install the
`ice-research-workbench` Codex skill. This extends the graph-aware harness with bounded agent-facing
research context and public scholarly discovery, without turning the graph or an agent loop into a
research authority.

The implementation is deliberately small:

- `ice_research_context`, `ice_research_impact`, and `ice_research_check` expose the existing local
  graph-harness queries and integrity check;
- `ice_ontology_shacl_validate`, `ice_ontology_sparql_query`, and
  `ice_ontology_ro_crate_preview` expose offline graph interoperability without file writes;
- `ice_graphrag_*`, `ice_research_workflow_plan`,
  `ice_research_workflow_evaluate`, and `ice_research_run_audit` expose bounded
  retrieval regression plus non-executing workflow inspection;
- `ice_literature_search` calls the public [OpenAlex works API](https://help.openalex.org/api/) with a
  10-second timeout and a 20-work maximum;
- `ice_research_capabilities` makes the tool and non-authorization boundaries machine-readable;
- `./ice literature search` is the matching human CLI; and
- `skills/ice-research-workbench/` is the versioned source for the installed Codex skill at
  `~/.codex/skills/ice-research-workbench`.

The skill is a native filesystem-installed Codex skill, not a claim of support for the still-in-review
[Skills Over MCP extension](https://modelcontextprotocol.io/community/working-groups/skills-over-mcp).
The MCP server and skill are connected by the skill workflow and the host configuration, not by an
experimental protocol advertisement.

The server uses the [`@modelcontextprotocol/server` v2
SDK](https://ts.sdk.modelcontextprotocol.io/v2/) `serveStdio` entry point. It negotiates the modern
[MCP 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) era and retains negotiated
2025-era compatibility for existing stdio hosts. Standard stdio requires that the protocol owns stdout;
startup and error diagnostics therefore use stderr only.

## Why this boundary

The local ontology already provides graph structure, hash-backed evidence locators, and scope/open-problem
context. OpenAlex adds a public citation-aware scholarly graph suitable for source discovery. Together,
they cover the useful research-engineering gap without granting a language model arbitrary notebook,
shell, file-write, or third-party account permission.

The selected server is a local implementation rather than an unreviewed registry server. The MCP Registry
is metadata discovery, not a trust decision; each server still requires separate permission and
dependency review. The current [MCP Registry guidance](https://modelcontextprotocol.io/registry/about)
supports that posture.

## Explicit non-goals

- No automatic successor graph, recursive research loop, swarm, or autonomous acceptance rule is added.
- No tool may run a Python kernel, write a result, mutate the ontology, stage/commit, or push.
- A passing graph check validates graph/provenance structure, not a scientific interpretation.
- An OpenAlex record is discovery metadata, not independent evidence. A primary source must be read and
  cited before it informs a research statement.
- Wolfram, Jupyter, Zotero, Semantic Scholar, and third-party MCP servers remain disconnected. They either
  require unavailable credentials/runtimes or add broader execution/file/network/account scopes than this
  use case needs.

## Operating guidance

Run the server from the repository root with `npm run --silent mcp`; the `--silent` flag prevents npm's
own stdout banner from corrupting stdio protocol messages. Configure an MCP host to launch that command
with this repository as its working directory. For Codex, register the absolute current repository path
from the repository root with:

```bash
codex mcp add ice-research -- npm --prefix "$PWD" run --silent mcp
```

Use `./ice literature search "<query>" --json` for the
same OpenAlex discovery surface without an MCP host.

The installed skill routes material graph changes through the harness, source discovery through OpenAlex,
interoperability through the offline RDF/SHACL/SPARQL/PROV-O/RO-Crate layer, durable handoffs through
explicit CLI-only state transitions, and numerical work through the existing lean bounded-runner rules.
It does not apply to unrelated coding, does not create ontology records by default, and does not change
the active execution circuit breaker. The MCP Tasks extension stays disabled because these tools do not
represent deferred execution jobs and a task protocol would not authorize an automatic successor run.

## Validation

- Typecheck and Vitest cover OpenAlex bounds, graph interoperability, durable state/self-consistency handling,
  routing evaluation, exact tool discovery, a legacy in-memory MCP handshake, and pinned modern
  `2026-07-28` stdio negotiation.
- `./ice harness check` remains the full repository graph/hash/evidence integrity gate.
- `./ice ontology shacl --graph all` is the projection-shape gate; `./ice agent eval` is the
  routing/handoff boundary regression.
- The skill source and installed copy pass the skill-creator structural validator.
