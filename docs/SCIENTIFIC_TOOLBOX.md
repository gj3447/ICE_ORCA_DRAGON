# Scientific toolbox

Installed on dev-01 on 2026-08-16. These tools support calculations; none imposes a research contract or
turns a symbolic identity into physical evidence.

For version-specific commands, environment separation, examples, and the local offline-manual index, see
[`SCIENTIFIC_CLI_MANUAL.md`](SCIENTIFIC_CLI_MANUAL.md).

## Ready now

| Tool | Installed version | Best use |
|---|---:|---|
| [Cadabra](https://cadabra.science/) | 2.5.14 | spinors, gamma matrices, Fierz identities, vielbeine, curvature, anticommuting fields |
| [JupyterLab](https://jupyter.org/) | 4.6.3 | interactive exact/numerical checks and plots |
| [SymPy](https://www.sympy.org/) | 1.14.0 | exact algebra, Hessians, Legendre transforms, symbolic regression tests |
| [python-flint](https://github.com/flintlib/python-flint) | 0.9.0 | independent exact arithmetic and Arb-style ball arithmetic |
| [SciPy](https://scipy.org/) | 1.17.1 | numerical linear algebra, integration, optimization |
| [Astropy](https://www.astropy.org/) | 8.0.1 | units, constants, coordinates, cosmology utilities |
| [Pint](https://pint.readthedocs.io/) / uncertainties | 0.25.3 / 3.2.3 | dimensional and uncertainty checks |
| [Z3](https://github.com/Z3Prover/z3) | 5.1.0 | finite logical/algebraic side conditions |
| [marimo](https://marimo.io/) | 0.23.16 | reproducible reactive Python notebooks |
| [Snakemake](https://snakemake.readthedocs.io/) | 9.25.1 | multi-engine calculation pipelines and cached dependencies |
| [Lean](https://lean-lang.org/) / Lake | 4.33.0 / 5.0.0 | formal checks of stable algebraic lemmas |
| [Julia](https://julialang.org/) | 1.12.7 | symbolic-to-numeric and differential-equation work |
| [Symbolics.jl](https://symbolics.juliasymbolics.org/) | 7.36.0 | independent symbolic transformations |
| [OrdinaryDiffEq.jl](https://docs.sciml.ai/OrdinaryDiffEq/stable/) | 7.6.0 | cosmological background and perturbation ODEs |

The Jupyter tool environment also contains NumPy, pandas, Matplotlib, mpmath, NetworkX, and an
IPython kernel. It is isolated by `uv tool`; it does not modify this repository's `uv.lock`. The two
Python environments intentionally differ: the repository `.venv` currently has SciPy 1.18.0, while
the Jupyter tool environment has SciPy 1.17.1.

## Common commands

```bash
cadabra2 --version
jupyter-lab
marimo edit
snakemake --cores all

/home/lagyeongjun/.elan/bin/lean --version
/home/lagyeongjun/.elan/bin/lake --version

/home/lagyeongjun/.juliaup/bin/julia
# Julia: using Symbolics, OrdinaryDiffEq
```

For repository calculations, prefer the locked environment:

```bash
uv run python path/to/check.py
./ice run <kernel>
```

Use Cadabra and SymPy/FLINT as independent engines when a tensor or sign result is important. Lean is
most useful after the formulas and conventions are stable; it cannot establish that a chosen model is
realized in nature.

## Codex skills

Installed under `~/.codex/skills`:

- official: `jupyter-notebook`, `pdf`
- individually reviewed from K-Dense's scientific collection: `sympy`, `astropy`,
  `uncertainty-and-units`
- repository-specific: `ice-research-workbench` (versioned source:
  [`skills/ice-research-workbench/`](../skills/ice-research-workbench/))

`ice-research-workbench` is installed through Codex's native skill discovery. It is not advertised as
the still-in-review Skills Over MCP extension.

The large third-party scientific skill collection was not installed wholesale. Individual skill files
can contain procedural instructions or shell actions, so additions should remain explicit and reviewable.
Newly installed skills become available after a Codex restart/new turn.

## MCP status

- `npm run --silent mcp` launches the repository-local `ice-orca-dragon-research` server over stdio,
  built with MCP TypeScript SDK v2. Its `serveStdio` entry negotiates the modern MCP 2026-07-28 era
  and retains 2025-era compatibility for existing hosts.
  `--silent` suppresses npm's own stdout banner, leaving stdout exclusively for MCP messages. It is
  read-only and exposes bounded graph context/impact/integrity, GraphRAG retrieval/evaluation,
  SHACL validation, restricted local SPARQL queries, RO-Crate preview, durable-run audit, and a maximum-20-result
  OpenAlex works search. It never executes kernels, writes files, mutates the ontology, or authorizes
  a next task. Explicit durable-run creation/review and RO-Crate output remain CLI-only operations.
  `./ice literature search "<query>" --json` provides the same public literature-discovery path without an
  MCP host.
- The existing ontology MCP is a read-only SYMPOSIUM knowledge-graph/schema service. Its
  `ontology_contract_get` name refers to a graph schema contract, not research preregistration, and it
  does not gate calculations.
- [Wolfram Research AgentTools](https://github.com/WolframResearch/AgentTools) is the strongest official
  calculation MCP found. It was not connected because this host has no activated Wolfram runtime.
- Community Jupyter, arXiv, Semantic Scholar, and Zotero MCP servers remain disconnected. They add broad
  notebook/file/network, arbitrary-code, credentials, or account permissions. OpenAlex is used only through
  the reviewed, local read-only adapter above.

MCPs should be connected only for a concrete missing capability, with a pinned package/repository and the
smallest permissions possible.

## Practical order for the SUSY/cosmology work

1. Transcribe the one-source action and conventions once.
2. Cross-check curvature, spinor, and Fierz algebra in Cadabra and SymPy/FLINT.
3. Check dimensions with Pint/Astropy units.
4. Solve only the surviving background/perturbation equations with SciPy or OrdinaryDiffEq.
5. Formalize a few stable lemmas in Lean if they remain central.

This replaces mandatory preregistration paperwork with direct calculations, reproducible commands, and
independent checks proportional to the risk.
