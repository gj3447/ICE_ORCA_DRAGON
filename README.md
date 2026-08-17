<div align="center">

# ICE_ORCA_DRAGON — Physics/Math Computation Workbench

**Hypercomplex experiments and CPT × Temporal-Folded SUSY calculations with reproducible checks**

[![Runnable kernels](https://img.shields.io/badge/Committed_kernels-53-3776ab?style=for-the-badge&logo=python&logoColor=white)](#current-snapshot)
[![Reproduction ledger](https://img.shields.io/badge/Repro_cases-14-10b981?style=for-the-badge)](#reproduction-ledger)
[![Control plane](https://img.shields.io/badge/Control_plane-TypeScript_%2B_Effect-3178c6?style=for-the-badge)](package.json)
[![License](https://img.shields.io/badge/License-AGPL--3.0--or--later-yellow?style=for-the-badge)](LICENSING.md)

</div>

ICE_ORCA_DRAGON is a standalone computation workbench with two active research tracks:

- Cayley–Dickson, sedenion, zero-divisor, and legacy numerical-claim tests;
- CPT × Temporal-Folded SUSY, closed-FRW/SUGRA, WDW, and two-sheet seam controls.

It is a hypothesis testbench, not a finished physics theory. Exact calculations, numerical evidence,
physical interpretations, and open conjectures are kept separate. The canonical development checkout is
`/home/lagyeongjun/CD/ICE_ORCA_DRAGON`; SYMPOSIUM may link here for context but is not a runtime
dependency.

## Current snapshot

| Surface | Committed state at this revision | Authority |
|---|---:|---|
| runnable Python kernels | 53 | `./ice list --json` |
| mapped reproduction cases | 14 | `./ice repro --list` |
| reproduction result | 12 `REPRO`, 1 `NONPORTABLE_FAIL`, 1 `SUPERSEDED` | `./ice repro` |
| research ontology | 199 nodes, 381 edges, 42 claims | `./ice ontology summary` |
| latest runnable CPT seam phase | Phase 22 | [`cpt_temporal_folded_susy/README.md`](cpt_temporal_folded_susy/README.md) |

The counts above describe the committed repository snapshot. `./ice list --json` is the authority for a
working tree that contains additional local kernels.

## Quick start

The control plane is strict TypeScript using Effect. Numerical kernels use the Python environment locked
by `uv.lock`.

```bash
npm ci
uv sync --locked
./ice doctor
./ice list
```

Canonical commands:

```bash
./ice doctor
./ice list [--json]
./ice info <name>
./ice run <name> [-- <kernel args>]
./ice repro [--list] [--only <mapped-name>]
./ice ontology validate
./ice ontology summary
```

`npm run ice -- <command>` is the package-script equivalent. `./ice` is the repository entry point.

## Repository layout

The repository root is intentionally limited to entry points, policy, package metadata, lockfiles, and
legal documents. Research code and historical reports live in named areas.

| Path | Contents | Runnable catalog |
|---|---|---:|
| [`ice`](ice), [`src/`](src), [`test/`](test) | Effect control plane and its tests | control plane |
| [`research/hypercomplex/`](research/hypercomplex) | Cayley–Dickson/sedenion kernels and adjacent JSON results | included |
| [`research/legacy_predictions/`](research/legacy_predictions) | dimensional, preregistration, and numerology-era kernels/results | included |
| [`cpt_temporal_folded_susy/`](cpt_temporal_folded_susy) | current phase scripts, reports, and frozen inputs | included |
| [`claimB_loop/`](claimB_loop) and named experiment directories | focused research programmes | included when a script has a main guard |
| [`ontology/`](ontology) | typed claims, evidence snapshots, scopes, sources, and open problems | not applicable |
| [`docs/`](docs) | current guides, decisions, audits, and provenance | excluded |
| [`_archive/`](_archive), [`_findings/`](_findings), [`papers/`](papers), [`output/`](output) | historical/non-runnable material and generated references | excluded |

Python scripts that import local helpers remain colocated with them. Result JSON files stay beside their
producer so direct runs and isolated reproduction use the same path contract.

## Run a kernel

Use a name returned by `./ice list` rather than depending on a physical path:

```bash
# Hypercomplex calculations
./ice info cd_path_amplitude_v2
./ice run cd_path_amplitude_v2
./ice run prove_s3_higher_gauge
./ice run queue_08_g2_diagnostic

# Legacy dimensional/numerology controls
./ice run derive_dimensionless_ICE
./ice run ice_prereg_check

# Current CPT × Temporal-Folded SUSY track
./ice run phase19_closed_sugra_bounce
./ice run phase20_two_sheet_wdw_selection
./ice run phase21_connected_seam_gaussian
./ice run phase22_finite_mode_seam_density
```

Direct runs may update an adjacent result file. Inspect `git status` afterward. Use `./ice repro` for a
non-destructive comparison against committed mapped outputs.

## Reproduction ledger

```bash
./ice repro --list
./ice repro
```

The harness copies tracked and candidate files into an Effect-scoped temporary directory, deletes each
mapped output before execution, runs cases serially, and compares the fresh result with the committed
baseline. The current ledger intentionally exits nonzero:

- 12 portable cases reproduce;
- `queue_03_threshold_sensitivity_scan` is quarantined because its legacy entrywise metric depends on an
  arbitrary null-space basis;
- `queue_06_cooperative_vacuum` is marked `SUPERSEDED` because a repaired script generated its baseline.

See the [Queue 03 portability audit](docs/audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) and the
[reproducibility record](docs/audits/REPRODUCIBILITY_2026-06-08.md).

## Research ontology

The repository-local [CPT × Temporal-Folded SUSY research graph](ontology/cpt-temporal-folded-susy/README.md)
links scoped claims, executable evidence, sources, and open problems. It is a memory/index layer, not a
research contract or automatic physics verdict.

```bash
./ice ontology validate
./ice ontology summary
./ice ontology show claim:P16_BGG_BOSONIC_KINETIC_PARENT
./ice ontology trace claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
```

## Scientific scope

Reports use the following disclosure layers:

| Layer | Meaning |
|---|---|
| L1 algebra | exact or numerical statements about the implemented algebra/computation |
| L2/L3 physics belt | proposed physical interpretations and empirical discriminators |
| mythology | user-primary narrative material preserved separately from scientific evidence |

“ICE predicts X” is incomplete without a target claim, layer, assumptions, and evidence status. The
governing decision is [the workbench reframe](docs/decisions/ICE_WORKBENCH_REFRAME_2026-05-18.md); the
working rules are in [`AGENTS.md`](AGENTS.md).

## Development

```bash
npm run typecheck
npm test
npm run check
./ice doctor
```

For a Python/kernel change, also run the directly affected entry and, when mapped, its isolated repro
case:

```bash
./ice info <name>
./ice run <name>
./ice repro --only <name>
```

## Documentation

| Document | Purpose |
|---|---|
| [`docs/index.md`](docs/index.md) | documentation map |
| [`docs/USERGUIDE.md`](docs/USERGUIDE.md) | CLI and runnable-catalog guide |
| [`docs/STATUS.md`](docs/STATUS.md) | engineering status and bounded scientific ledger |
| [`research/README.md`](research/README.md) | organized research-code and report map |
| [`cpt_temporal_folded_susy/README.md`](cpt_temporal_folded_susy/README.md) | complete CPT phase index and current boundary |
| [`ontology/README.md`](ontology/README.md) | research-graph format and CLI entry points |
| [`docs/decisions/`](docs/decisions) | governing scope decisions |
| [`docs/audits/`](docs/audits) | reproducibility and method audits |
| [`docs/provenance/SOURCES.md`](docs/provenance/SOURCES.md) | mythology/physics sources and provenance |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | contribution and verification workflow |

## License

AGPL-3.0-or-later, with a separate commercial-license option. See
[`LICENSING.md`](LICENSING.md).
