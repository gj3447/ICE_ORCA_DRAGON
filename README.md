<div align="center">

# ICE_ORCA_DRAGON — Physics/Math Computation Workbench

**Cayley–Dickson and sedenion experiments, structural proofs, and reproducibility checks**

[![Runnable kernels](https://img.shields.io/badge/Runnable_kernels-44-3776ab?style=for-the-badge&logo=python&logoColor=white)](#run-a-kernel)
[![Control plane](https://img.shields.io/badge/Control_plane-TypeScript_%2B_Effect-3178c6?style=for-the-badge)](package.json)
[![Science policy](https://img.shields.io/badge/Science_policy-T0%2FT1%2FT2-10b981?style=for-the-badge)](.claude/skills/science-feedback-loop.md)
[![License](https://img.shields.io/badge/License-AGPL--3.0--or--later-yellow?style=for-the-badge)](LICENSING.md)

</div>

ICE_ORCA_DRAGON is a standalone hypercomplex-computation repository. The canonical dev-01 checkout is
`/home/lagyeongjun/CD/ICE_ORCA_DRAGON`; it has its own Git history and `origin`. SYMPOSIUM may link to
this repository for context, but no longer embeds it as a submodule or runtime dependency.

The current CLI exposes **44 runnable Python kernels**. `./ice list --json` is the authority for the
live catalog; historical source inventories may contain additional scripts that are not runnable entries.
Fourteen committed outputs are mapped into the isolated reproduction ledger.

## Scientific scope

This repository is a hypothesis testbench, not a finished physics theory. Reports must keep these layers
separate:

| Layer | Meaning |
|---|---|
| L1 algebra | exact or numerical statements about hypercomplex algebra and computation |
| L2/L3 physics belt | proposed physical interpretations and empirical discriminators |
| mythology | user-primary narrative material preserved separately from scientific evidence |

“ICE predicts X” is incomplete without a layer, target claim, and evidence status. Historical verdicts
remain documented in [`docs/STATUS.md`](docs/STATUS.md); they are not instructions to mutate current
canon automatically.

## Quick start

The control plane is strict TypeScript using Effect. Numerical kernels run in the Python environment
locked by `uv.lock`.

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
```

`npm run ice -- <command>` is the package-script equivalent. `./ice` is the repository entry point.

## Run a kernel

Use a name returned by `./ice list`:

```bash
# Cayley–Dickson path computation
./ice info cd_path_amplitude_v2
./ice run cd_path_amplitude_v2

# Independent sedenion checks
./ice run avenue3_phase1_groundtruth
./ice run naesengmoon_indep_sedenion

# Structural and diagnostic cases
./ice run prove_higgs_ZD_doublet
./ice run prove_s3_higher_gauge
./ice run queue_02_4condition_diagnostic
./ice run queue_08_g2_diagnostic
./ice run queue_09_SS3TG
```

Direct runs may update a kernel's result file. Inspect `git status` afterward. Use `./ice repro` when the
goal is a non-destructive comparison against committed mapped outputs.

## Reproduction ledger

```bash
./ice repro --list
./ice repro
```

The harness copies tracked/candidate files into an Effect-scoped temporary directory, deletes each mapped
output before execution, runs cases serially, and performs a structural/semantic comparison against the
committed baseline. The current 14-case ledger is intentionally not all-green:

- 12 `REPRO`
- `queue_03_threshold_sensitivity_scan`: `NONPORTABLE_FAIL`
- `queue_06_cooperative_vacuum`: `SUPERSEDED`

Queue 03 is quarantined because its legacy entrywise commutator maximum depends on an arbitrary
null-space basis. A broad tolerance would conceal a method defect, so the ledger exits nonzero until a
separately versioned and preregistered invariant method exists. See
[`QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](QUEUE03_PORTABILITY_AUDIT_2026-08-14.md).

## Choose the feedback tier before execution

Use the highest applicable tier. Declare it before observing the output; a T0/T1 result that materially
affects a scientific claim escalates to T2, and a T2 run is never downgraded afterward.

| Tier | Use when | Definition of done |
|---|---|---|
| T0 | docs, CLI, harness, locks, or other non-claim engineering | requested artifact plus directly relevant checks |
| T1 | frozen-input reproduction | command/args/environment/baseline/comparator/diff; no confidence change |
| T2 | result can support, contradict, or create a scientific claim | target claim and fiber, preregistration status, all applicable evidence gates, independent classifications |

For T2, classify independent axes rather than forcing one verdict:

- claim relation: `SUPPORTS | CONTRADICTS | INCONCLUSIVE`
- novelty: `REPRODUCTION | DISCOVERY_CANDIDATE`
- fitting risk: `NULL_PASS | NUMEROLOGY_HOLD | NOT_APPLICABLE | NOT_ASSESSED`
- target: explicit claim plus algebra/physics fiber

Null and multiplicity plans apply when statistically meaningful. Numerical Bayes requires an explicit
hypothesis/evidence pair, frozen prior, both likelihoods, and selection/dependence treatment; rerunning the
same data is not independent evidence. Lakatos applies only at a declared programme/fiber checkpoint with
a baseline and longitudinal window.

Ordinary T0/T1 work stays in test logs and reproduction receipts. Reusable/material T2 results may be
proposed as provenance-bearing `PENDING` evidence. They do not directly increment confidence, mark a
Contract refuted, create a canonical Span/Possibility, or supersede anything. Canonical mutation needs an
identified pending evidence record and separate authorized ratification. Discovery creates one bounded
follow-up candidate, not automatic recursion.

The executable policy is [`AGENTS.md`](AGENTS.md) and
[`science-feedback-loop.md`](.claude/skills/science-feedback-loop.md).

## Computation areas

| Area | Representative runnable entries |
|---|---|
| Cayley–Dickson | `cd_path_amplitude_v2`, `ice_convention_invariance` |
| dimensional/numerical claims | `derive_dimensionless_ICE`, `derive_Lstar_from_ICE`, `derive_mass_ratios_ICE` |
| Higgs and S-proofs | `prove_higgs_ZD_doublet`, `prove_s1_framing`, `prove_s2_CCWZ`, `prove_s3_higher_gauge`, `prove_s5_bv_ainfty`, `prove_s7_WW_evasion` |
| sedenion ground truth | `avenue3_phase1_groundtruth`, `naesengmoon_indep_sedenion` |
| queue diagnostics | `queue_01_orbit_analysis`, `queue_02_4condition_diagnostic`, `queue_03_threshold_sensitivity_scan`, `queue_04_hosotani_toy`, `queue_08_g2_diagnostic`, `queue_09_SS3TG`, `queue_11_xor_invariant` |
| numerology controls | `numerology_mc_judge`, `numerology_mc_judge_v3_abc`, `numerology_hidden_scan` |

Always use `./ice list` for the complete live set.

## Development

```bash
npm run typecheck
npm test
npm run check
```

For Python/kernel changes, also verify the locked environment and the directly affected cases:

```bash
uv sync --locked
./ice doctor
./ice info <name>
./ice run <name>
# only when the name is in ./ice repro --list
./ice repro --only <name>
```

## Documentation

| Document | Purpose |
|---|---|
| [`docs/USERGUIDE.md`](docs/USERGUIDE.md) | runnable catalog usage and category guide |
| [`docs/STATUS.md`](docs/STATUS.md) | current engineering status plus historical scientific ledger |
| [`docs/index.md`](docs/index.md) | documentation map |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | contribution and verification contract |
| [`REPRODUCIBILITY_2026-06-08.md`](REPRODUCIBILITY_2026-06-08.md) | historical attestation and current erratum |
| [`SOURCES.md`](SOURCES.md) | mythology/physics sources and provenance |

## License

AGPL-3.0-or-later, with a separate commercial-license option. See
[`LICENSING.md`](LICENSING.md).
