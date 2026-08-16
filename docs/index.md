---
title: ICE_ORCA_DRAGON Documentation Hub
description: TypeScript/Effect control plane for locked Python hypercomplex computations and tiered scientific evidence handling.
---

# ICE_ORCA_DRAGON documentation

ICE_ORCA_DRAGON is a standalone computation workbench. Its TypeScript/Effect control plane discovers,
runs, and reproduces locked Python kernels. The live catalog contains 45 runnable entries; verify the
current set with `./ice list --json` rather than copied prose counts.

```bash
npm ci
uv sync --locked
./ice doctor
npm run check
./ice list
```

## Core documents

| Document | Purpose |
|---|---|
| [`../README.md`](../README.md) | overview, CLI, tier policy, current reproduction ledger |
| [`USERGUIDE.md`](USERGUIDE.md) | live-catalog usage and kernel workflow |
| [`STATUS.md`](STATUS.md) | current engineering state and bounded historical scientific ledger |
| [`SCIENTIFIC_TOOLBOX.md`](SCIENTIFIC_TOOLBOX.md) | installed symbolic, numerical, workflow, and formal-verification tools |
| [`../cpt_temporal_folded_susy/README.md`](../cpt_temporal_folded_susy/README.md) | CPT × Temporal-Folded SUSY phase index, current boundary, and sequencing gates |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | contribution and verification workflow |
| [`../CHANGELOG.md`](../CHANGELOG.md) | historical repository evolution |
| [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md) | historical attestation plus current erratum |
| [`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) | queue03 method-quarantine evidence |
| [`../SOURCES.md`](../SOURCES.md) | source and mythology/physics provenance |

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
