---
name: ice-research-workbench
description: Use for ICE_ORCA_DRAGON research, research-harness, ontology, or scholarly-literature work that benefits from bounded graph context and source discovery. Do not use for unrelated coding tasks.
---

# ICE research workbench

Treat this repository as a computational workbench, not as an automatic physics-claim engine. Preserve its mythology layer while keeping finite calculations, numerical error, model interpretation, and empirical hypotheses separate.

## Route the task narrowly

- For a proposed CPT core research task, first run `./ice agent plan "<one blocker question>" --graph cpt --json` (or `ice_research_workflow_plan`). The user-declared TOE objective is not established evidence. Only `CURRENT_BLOCKER_CANDIDATE` may proceed to core-labelled human calculation-design review; all other classifications must stop/reframe or remain explicitly supporting, maintenance, or archive work.
- The present core blocker is `open:gate1-original-cycle-signed-global-intersections`. A core question must name one missing typed object, one bounded falsifiable output, and its dependency path through the next gate to the terminal review criteria. P1--P7 are supporting by default; a P-lane task becomes a core-routing candidate only when human review names the exact G1--G5 missing object and evidence edge it would change.
- For a material change to a claim, direct evidence, scope, or open problem, begin with `./ice harness context <node-id>` or `./ice harness impact <path>`. Use `./ice harness check` before relying on tracked graph hashes.
- For source discovery, use `./ice literature search "<query>" --json` or the read-only `ice_literature_search` MCP tool. Record the time-stamped query and read the primary source before treating a result as support.
- For a selected OpenAlex work, use `./ice literature neighbors <work-id> --json` or `ice_literature_neighbors`. It is a bounded citation-discovery neighborhood, not citation verification.
- For cross-record local context, use `./ice graphrag search "<question>" --graph <key> --depth 0..3` or `ice_graphrag_search`. Its TextUnits are canonical ontology projections, and its hybrid score is BM25 plus a deterministic lexical hash vector and explicit graph traversal—not a learned embedding or an LLM answer.
- To prepare an inspectable handoff, use `./ice agent plan "<question>" --graph cpt --json` or `ice_research_workflow_plan`. The checkpoint is `AWAITING_HUMAN_REVIEW`; it never persists itself, approves a core-progress label, or authorizes `./ice run`.
- For one bounded calculation, follow the lean rules: fix one question, one output, and one non-claim; choose one principal failure class and only the relevant 1--3 controls; run only a clean committed runner through `./ice run`.
- For a long-lived regression contract, use `./ice repro`; do not add every exploratory calculation to the reproduction manifest.

## Non-negotiable boundaries

- Graph context is a memory/index and change-review input. It does not ratify a claim, authorize a calculation, mutate the ontology, or generate a successor task.
- `TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW` is the strongest repository completion label. It requires the full theory and empirical criteria in the active TOE routing decision and is not a claim that a TOE has been discovered or accepted.
- OpenAlex results are discovery metadata. They are not independent evidence, a substitute for the cited paper, or permission to infer a physical conclusion.
- GraphRAG retrieval is also review context, not a synthesized conclusion. Add learned embeddings, model extraction, or additional agent automation only after a benchmark and explicit review.
- The MCP surface is read-only. It does not execute Python, write files, create ontology nodes, or call arbitrary notebook/code tools.
- Historical numbered Phase 51--56 descendants remain blocked. Do not bypass `./ice` with direct Python execution.

When a task changes files, preserve unrelated dirty changes, perform proportionate validation, and make the repository-local commit required by its worktree rules. Do not push unless the user explicitly asks.
