---
title: ICE_ORCA_DRAGON Documentation Hub
description: TypeScript/Effect control plane for locked Python research computations and layered scientific evidence handling.
---

# ICE_ORCA_DRAGON documentation

ICE_ORCA_DRAGON is a standalone computation workbench. Its TypeScript/Effect control plane discovers,
runs, and reproduces locked Python kernels. The committed catalog contains 64 runnable entries; verify the
current set with `./ice list --json` rather than copied prose counts.

```bash
npm ci
uv sync --locked
./ice doctor
npm run check
./ice list
./ice ontology validate
```

## Core documents

| Document | Purpose |
|---|---|
| [`../README.md`](../README.md) | overview, repository layout, CLI, scientific scope, and current snapshot |
| [`USERGUIDE.md`](USERGUIDE.md) | live-catalog usage and kernel workflow |
| [`STATUS.md`](STATUS.md) | current engineering state and bounded historical scientific ledger |
| [`../research/README.md`](../research/README.md) | organized hypercomplex/legacy-prediction code and report map |
| [`SCIENTIFIC_TOOLBOX.md`](SCIENTIFIC_TOOLBOX.md) | installed symbolic, numerical, workflow, and formal-verification tools |
| [`SCIENTIFIC_CLI_MANUAL.md`](SCIENTIFIC_CLI_MANUAL.md) | version-specific commands, examples, official documentation, and offline-manual index |
| [`../ontology/README.md`](../ontology/README.md) | typed research graph, evidence snapshots, validation, and lookup commands |
| [`../ontology/cpt-temporal-folded-susy/README.md`](../ontology/cpt-temporal-folded-susy/README.md) | readable CPT × Temporal-Folded SUSY concept and evidence map |
| [`../cpt_temporal_folded_susy/README.md`](../cpt_temporal_folded_susy/README.md) | CPT × Temporal-Folded SUSY phase index, current boundary, and sequencing gates |
| [`../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md`](../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md) | closed-SUGRA background existence calculation and initial-value caveat |
| [`../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md`](../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md) | leading two-sheet WDW selection control and conditional curvature conversion |
| [`../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md`](../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md) | normalized connected two-sheet Gaussian seam control and flux-prior caveat |
| [`../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md`](../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md) | finite-mode seam density control and noncompact zero-mode obstruction |
| [`../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md`](../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md) | constrained minisuperspace rigging-map density control and zero-root obstruction |
| [`../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md`](../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md) | connected real interval response and constraint-reduced rank-one channel |
| [`../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md`](../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md) | connected lapse saddle, Schur reduction, local complex descent, and real-branch fold |
| [`../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md`](../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md) | bounded constant-phase lapse arm and real-fold Airy uniformization |
| [`../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md`](../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md) | Lorentzian Wick convention, half-line resolvent, and raw zero-lapse endpoint singularity |
| [`../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md) | bounded crossing and reduced BFV--BRST proper-length diagnostic |
| [`../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md`](../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md) | distributional zero-lapse identity kernel, BFV modulus measure, and conformal-sign obstruction |
| [`../cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md`](../cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md) | finite-cutoff coupled conformal/lapse tangent cycle, relative determinant magnitude, and determinant-line obstruction |
| [`../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md`](../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md) | unreduced canonical lift, nonzero homogeneous BFV quartets, relative normalization, and clock-polarization obstruction |
| [`../cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md) | positive-half-line endpoint contact versus a declared below-origin projected lapse-base crossing; signed joint intersection remains open |
| [`../cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md`](../cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md) | simple-fold Airy action scale, separate-saddle divergence, local solution-rank obstruction, and global contour gate |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | contribution and verification workflow |
| [`../CHANGELOG.md`](../CHANGELOG.md) | historical repository evolution |
| [`audits/README.md`](audits/README.md) | reproducibility and method-audit index |
| [`decisions/README.md`](decisions/README.md) | active workbench-scope decisions |
| [`provenance/SOURCES.md`](provenance/SOURCES.md) | source and mythology/physics provenance |

## Scientific workflow

There is no mandatory tier or preregistration contract. Record the source equations and conventions, run
the smallest useful calculation, preserve its command/environment/output, and check high-risk algebra or
numerics independently. Reports must distinguish computed facts, physical interpretation, and open
speculation. See [`../AGENTS.md`](../AGENTS.md).

## Current execution map

| Need | Command |
|---|---|
| inspect environment | `./ice doctor` |
| list runnable kernels | `./ice list` or `./ice list --json` |
| inspect one entry | `./ice info <name>` |
| execute one entry | `./ice run <name>` |
| list mapped reproduction cases | `./ice repro --list` |
| run isolated ledger | `./ice repro` |
| validate research graph | `./ice ontology validate` |
| read current research summary | `./ice ontology summary` |
| trace one claim | `./ice ontology trace <node-id>` |

The mapped ledger currently reports 12 `REPRO`, queue03 `NONPORTABLE_FAIL`, and queue06
`SUPERSEDED`. A nonzero overall exit is expected while those explicit statuses remain.

## External integration

The upstream repository is [gj3447/ICE_ORCA_DRAGON](https://github.com/gj3447/ICE_ORCA_DRAGON).
It is developed and released independently. Related integration documents live in the
[SYMPOSIUM repository](https://github.com/gj3447/symposium):

- [APT](https://github.com/gj3447/symposium/tree/main/THEORY/APT)
- [TPA](https://github.com/gj3447/symposium/tree/main/THEORY/TPA)
- [Narrative feedback policy](https://github.com/gj3447/symposium/blob/main/.claude/skills/narrative-feedback-loop.md)
- [Naesengmoon](https://github.com/gj3447/symposium/tree/main/THEORY/%EB%82%98%EC%83%9D%EB%AC%B8)
- [Reproduction snapshot](https://github.com/gj3447/symposium/tree/main/REPRODUCTION)

These are optional integration references, not runtime dependencies of the standalone workbench.

## Plugin manifest

[`../.claude-plugin/plugin.json`](../.claude-plugin/plugin.json) carries portable package metadata.
Runtime dependency contracts remain in `package.json`/`package-lock.json` and
`pyproject.toml`/`uv.lock`, not in custom manifest fields.
