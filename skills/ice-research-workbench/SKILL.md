---
name: ice-research-workbench
description: Use for ICE_ORCA_DRAGON research, research-harness, ontology, or scholarly-literature work that benefits from bounded graph context and source discovery. Do not use for unrelated coding tasks.
---

# ICE research workbench

Treat this repository as a computational workbench, not as an automatic physics-claim engine. Preserve its mythology layer while keeping finite calculations, numerical error, model interpretation, and empirical hypotheses separate.

## Route the task narrowly

- For a material change to a claim, direct evidence, scope, or open problem, begin with `./ice harness context <node-id>` or `./ice harness impact <path>`. Use `./ice harness check` before relying on tracked graph hashes.
- For source discovery, use `./ice literature search "<query>" --json` or the read-only `ice_literature_search` MCP tool. Record the time-stamped query and read the primary source before treating a result as support.
- For one bounded calculation, follow the lean rules: fix one question, one output, and one non-claim; choose one principal failure class and only the relevant 1--3 controls; run only a clean committed runner through `./ice run`.
- For a long-lived regression contract, use `./ice repro`; do not add every exploratory calculation to the reproduction manifest.

## Non-negotiable boundaries

- Graph context is a memory/index and change-review input. It does not ratify a claim, authorize a calculation, mutate the ontology, or generate a successor task.
- OpenAlex results are discovery metadata. They are not independent evidence, a substitute for the cited paper, or permission to infer a physical conclusion.
- The MCP surface is read-only. It does not execute Python, write files, create ontology nodes, or call arbitrary notebook/code tools.
- Historical numbered Phase 51--56 descendants remain blocked. Do not bypass `./ice` with direct Python execution.

When a task changes files, preserve unrelated dirty changes, perform proportionate validation, and make the repository-local commit required by its worktree rules. Do not push unless the user explicitly asks.
