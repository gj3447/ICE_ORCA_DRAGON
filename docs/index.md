---
title: ICE_ORCA_DRAGON Documentation Hub
description: TypeScript/Effect control plane for locked Python hypercomplex computations and tiered scientific evidence handling.
---

# ICE_ORCA_DRAGON documentation

ICE_ORCA_DRAGON is a standalone computation workbench. Its TypeScript/Effect control plane discovers,
runs, and reproduces locked Python kernels. The live catalog contains 42 runnable entries; verify the
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
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | contribution and verification contract |
| [`../CHANGELOG.md`](../CHANGELOG.md) | historical repository evolution |
| [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md) | historical attestation plus current erratum |
| [`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) | queue03 method-quarantine evidence |
| [`../SOURCES.md`](../SOURCES.md) | source and mythology/physics provenance |

## Feedback policy

Only T2 claim-impact work invokes the full scientific loop.

| Tier | Short rule |
|---|---|
| T0 | engineering artifact + directly relevant checks |
| T1 | frozen reproduction receipt; no confidence change |
| T2 | declare target/fiber and preregistration before execution, then apply all relevant evidence gates |

For T2, relation, novelty, fitting risk, and target/fiber are independent axes. Null/multiplicity checks,
numerical Bayes, and Lakatos are conditional gates, not seven mandatory steps for every calculation.
Material/reusable evidence may become a `PENDING` proposal; canonical mutation requires separate
authorized ratification. Discovery records a bounded follow-up instead of recursively dispatching itself.

See [`../AGENTS.md`](../AGENTS.md) and
[`../.claude/skills/science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md).

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
The repository-native policy remains the standalone
[`science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md); it is not falsely declared as a
plugin skill directory. Runtime dependency contracts remain in `package.json`/`package-lock.json` and
`pyproject.toml`/`uv.lock`, not in custom manifest fields.
