---
name: ice-research-workbench
description: Use for ICE_ORCA_DRAGON research, ontology interoperability, graph-harness, durable human-review orchestration, or scholarly-literature work that benefits from bounded graph context and source discovery. Do not use for unrelated coding tasks.
---

# ICE research workbench

Treat this repository as a computational workbench, not as an automatic physics-claim engine. Preserve its mythology layer while keeping finite calculations, numerical error, model interpretation, and empirical hypotheses separate.

## Route the task narrowly

- For a proposed CPT core research task, first run `./ice agent plan "<one blocker question>" --graph cpt --json` (or `ice_research_workflow_plan`). The user-declared TOE objective is not established evidence. Only `CURRENT_BLOCKER_CANDIDATE` may proceed to core-labelled human calculation-design review; all other classifications must stop/reframe or remain explicitly supporting, maintenance, or archive work.
- The present core blocker is `open:gate1-original-cycle-signed-global-intersections`. A core question must name one missing typed object, one bounded falsifiable output, and its dependency path through the next gate to the terminal review criteria. P1--P7 are supporting by default; a P-lane task becomes a core-routing candidate only when human review names the exact G1--G5 missing object and evidence edge it would change.
- For a material change to a claim, direct evidence, scope, or open problem, begin with `./ice harness context <node-id>` or `./ice harness impact <path>`. Use `./ice harness check` before relying on tracked graph hashes.
- For standards interchange, keep native ontology JSON authoritative. Use `./ice ontology export --format dataset-jsonld` or `./ice ontology export --format nquads`, plus `./ice ontology shacl` and the bounded restricted local SPARQL 1.1 subset exposed by `./ice ontology sparql`, for named-dataset inspection. Use `./ice ontology crate output/<new-name>` only when the user explicitly wants a non-overwriting RO-Crate 1.3 metadata/export package; it does not copy raw results.
- For source discovery, use `./ice literature search "<query>" --json` or the read-only `ice_literature_search` MCP tool. Record the time-stamped query and read the primary source before treating a result as support.
- For a selected OpenAlex work, use `./ice literature neighbors <work-id> --json` or `ice_literature_neighbors`. It is a bounded citation-discovery neighborhood, not citation verification.
- For cross-record local context, use `./ice graphrag search "<question>" --graph <key> --depth 0..3` or `ice_graphrag_search`. Its TextUnits are canonical ontology projections, and its hybrid score is BM25 plus a deterministic lexical hash vector and explicit graph traversal—not a learned embedding or an LLM answer.
- When the user asks for scientific intuition around a canonical open problem, use `./ice intuition search "<question>" --target <graph>::<open:node> --json` or `ice_scientific_intuition_search`. Inspect `canonical_target` and `canonical_context` first, then treat `non_authoritative_signals` only as source-linked question lenses. The derived federated links support navigation; they do not merge the sidecar into the canonical graph. Read the cited primary source and let a human retain at most one bounded falsifiable question before returning to `./ice agent plan`; never feed a signal directly into a runner or durable handoff.
- Before accepting a material navigation or retrieval change, run `./ice graphrag eval --limit 12 --json`, `./ice graphrag diff --base HEAD --limit 12 --json`, and `./ice agent eval --json` after `./ice ontology review`. These suites control canonical-locator retrieval and routing/handoff boundaries only; inspect movement with the native graph and source context. Do not add a case for every experiment.
- To preview an inspectable handoff, use `./ice agent plan "<question>" --graph cpt --json` or `ice_research_workflow_plan`; the preview never persists itself. If the user explicitly requests a process-spanning review record, use `./ice agent run create ... --id <run-id>`, copy its current trace tip into exactly one `agent run review`, then use `agent run audit`. Persisted records pin the control plane and graph inputs and use a SHA-256 event chain for self-consistency, not as a hostile-writer signature; `STOPPED` and `CLOSED` are both non-executing terminal states.
- For one bounded calculation, follow the lean rules: fix one question, one output, and one non-claim; choose one principal failure class and only the relevant 1--3 controls; run only a clean committed runner through `./ice run`.
- For a long-lived regression contract, use `./ice repro`; do not add every exploratory calculation to the reproduction manifest.

## Non-negotiable boundaries

- Graph context, RDF/SHACL/SPARQL output, PROV-O lineage, and RO-Crate metadata are memory/interchange/change-review inputs. They do not ratify a claim, authorize a calculation, mutate the ontology, or generate a successor task.
- `TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW` is the strongest repository completion label. It requires the full theory and empirical criteria in the active TOE routing decision and is not a claim that a TOE has been discovered or accepted.
- OpenAlex results are discovery metadata. They are not independent evidence, a substitute for the cited paper, or permission to infer a physical conclusion.
- GraphRAG retrieval is also review context, not a synthesized conclusion. Add learned embeddings, model extraction, or additional agent automation only after a benchmark and explicit review.
- Scientific-intuition sidecar records are exploratory navigation cues, never canonical claims, evidence, rankings, probabilities, or execution authority. Preserve `UNRESOLVED` separately from numerical zero and `OUT_OF_SCOPE`; a schema-valid cue can still be scientifically useless.
- The MCP surface is read-only. It may validate/query/preview/audit, but it does not execute Python, create/review durable runs, write crates, create ontology nodes, or call arbitrary notebook/code tools. Its stdio entry negotiates MCP 2026-07-28 with legacy compatibility. The Tasks extension remains unused because this repository exposes no deferred execution job and never authorizes an automatic successor run.
- Historical numbered Phase 51--56 descendants remain blocked. Do not bypass `./ice` with direct Python execution.

When a task changes files, preserve unrelated dirty changes, perform proportionate validation, and make the repository-local commit required by its worktree rules. Do not push unless the user explicitly asks.
