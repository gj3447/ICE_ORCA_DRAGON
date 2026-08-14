# ICE_ORCA_DRAGON user guide

> Guide to the 42 entries currently exposed by the TypeScript/Effect CLI. Historical source files are
> not automatically runnable entries; `./ice list --json` is authoritative.

## Setup

```bash
npm ci
uv sync --locked
./ice doctor
```

`doctor` validates the Node major, package lock, Python version, uv lock, and required numerical
packages. A READY report describes the environment, not the truth of a scientific claim.

## Discover before running

```bash
./ice list
./ice list --json
./ice info prove_s3_higher_gauge
```

Do not infer a CLI name from an old filename or a prose inventory. If `./ice info <name>` fails, choose a
name from the live list. Source variants containing words such as `search`, `final`, `part2`, or `v2` may
be historical implementation files rather than catalog entries.

## Run one kernel

```bash
./ice run cd_path_amplitude_v2
./ice run derive_mass_ratios_ICE
./ice run prove_higgs_ZD_doublet
./ice run queue_02_4condition_diagnostic
```

Arguments after `--` are passed to the Python kernel as an argv array:

```bash
./ice run <name> -- --flag value
```

Direct execution can write a result JSON next to the script. Inspect `git status --short` after the run.

## Runnable areas

The table is orientation, not a replacement for `./ice list`.

| Area | Current runnable examples |
|---|---|
| sedenion ground truth | `avenue3_phase1_groundtruth`, `naesengmoon_indep_sedenion` |
| Cayley–Dickson | `cd_path_amplitude_v2`, `ice_convention_invariance` |
| Claim B falsifiers | `claimB_associator_growth_falsifier`, `claimB_associator_distribution`, `claimB_truncation_stability`, `claimB_zd_nullity_spectrum` |
| dimensional analysis | `derive_dimensionless_ICE`, `derive_epsilon_ICE`, `derive_Lstar_from_ICE`, `derive_mass_ratios_ICE` |
| preregistration checks | `gravity_prereg_predictions`, `ice_prereg_check`, `ice_prereg_predictions` |
| Higgs and S-proofs | `prove_higgs_ZD_doublet`, `prove_s1_framing`, `prove_s2_CCWZ`, `prove_s3_higher_gauge`, `prove_s5_bv_ainfty`, `prove_s7_WW_evasion` |
| queue diagnostics | `queue_01_orbit_analysis`, `queue_02_4condition_diagnostic`, `queue_03_threshold_sensitivity_scan`, `queue_04_hosotani_toy`, `queue_05_coleman_weinberg`, `queue_06_cooperative_vacuum`, `queue_08_g2_diagnostic`, `queue_09_SS3TG`, `queue_10_group_of_6`, `queue_11_xor_invariant` |
| numerology controls | `numerology_hidden_scan`, `numerology_hidden_scan_v2_target_categories_2026-05-20`, `numerology_mc_judge`, `numerology_mc_judge_v3_abc` |
| other falsifiers/checks | `igrueqft_locality_falsifier`, `mb3_adelberger_verdict`, `verify_mp_mW_3_256`, `wilmot_theta_preservation_test`, `ww_unitarity_bound_analysis` |

## Read a result JSON

Result schemas differ because the kernels answer different questions. Inspect structure before selecting a
field:

```bash
jq 'keys' <result>.json
jq '.' <result>.json
```

Preserve the distinction between:

- computed observables
- thresholds or configuration
- a script's own interpretation/verdict field
- provenance and preregistration metadata

A stored verdict string is evidence about what that historical run reported. It does not independently
ratify a Contract or change current confidence.

## Reproduce mapped outputs

```bash
./ice repro --list
./ice repro
./ice repro --only prove_s5_bv_ainfty
```

`--only` accepts names in `./ice repro --list`, not every runnable name. The harness executes in an
Effect-scoped temporary copy and compares fresh JSON with `git show HEAD:<mapped-output>` using a
field-aware semantic contract.

Current expected ledger:

| Count/status | Meaning |
|---|---|
| 12 `REPRO` | mapped outputs satisfy their comparator |
| 1 `NONPORTABLE_FAIL` | queue03 uses a basis-dependent legacy metric |
| 1 `SUPERSEDED` | queue06 is retained as historical output, not a live success |

The overall exit code is therefore nonzero by design. Do not loosen a global tolerance to make queue03
green. See [`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md).

## Choose T0, T1, or T2

Declare the highest applicable tier before looking at new output.

### T0 — engineering

Use for docs, CLI, harness, dependency, or refactor work that does not evaluate a scientific claim.
Definition of done is the requested artifact plus directly relevant checks. Examples:

```bash
npm run check                 # TypeScript/Effect control plane
uv sync --locked              # Python/lock change
./ice doctor
./ice run <affected-name>     # numerical kernel change
```

### T1 — frozen reproduction

Record command, args, environment, frozen baseline, comparator, and diff. T1 confirms whether a result
reproduces under that contract; it does not increment confidence. If the observed outcome materially
affects a claim, escalate to T2.

### T2 — claim-impact work

Before execution, state:

- target claim and algebra/physics fiber
- preregistered or post-hoc status
- null and multiplicity plan when applicable
- frozen comparator/falsifier

After execution, record independent axes:

```text
claim_relation: SUPPORTS | CONTRADICTS | INCONCLUSIVE
novelty: REPRODUCTION | DISCOVERY_CANDIDATE
fitting_risk: NULL_PASS | NUMEROLOGY_HOLD | NOT_APPLICABLE | NOT_ASSESSED
```

Bayes is numerical only when `H`, `E`, a frozen prior, both likelihoods, and selection/dependence are
explicit. Do not multiply repeated runs of the same data as independent evidence. Lakatos is assessed
only for a declared programme/fiber at a checkpoint with a baseline and longitudinal window.

The full contract is
[`../.claude/skills/science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md).

## Persistence after T2

The default output is the T2 report. Only material/reusable evidence should become a provenance-bearing
`PENDING` proposal. Ordinary execution cannot directly:

- increment Contract confidence
- mark a claim `REFUTED`
- create a canonical Span or Possibility
- supersede an existing node
- begin recursive discovery work

Ratification is a separate authorized action against an identified pending evidence record. A discovery
may record one bounded follow-up; its child is independently tiered.

## Adding a runnable kernel

1. Keep import-time work cheap; put execution under `if __name__ == "__main__":`.
2. Emit deterministic, schema-stable JSON where practical.
3. Add the script where the catalog discovery rules can see it.
4. Verify it appears in `./ice list` and resolves through `./ice info`.
5. Run the locked environment and targeted case.
6. Add a reproduction mapping only when a committed output and comparator policy are justified.

## Common mistakes

| Mistake | Correction |
|---|---|
| citing an old `*_final.py` name as runnable | use `./ice list` and `./ice info` |
| treating a numerical match as confirmation | use T2 registration/null gates when it affects a claim |
| treating reproduction as independent evidence | T1 records repeatability; identical data are not a second `E` |
| applying Lakatos to each script | reserve it for declared programme/fiber checkpoints |
| auto-writing KG after every result | local report first; selected PENDING evidence; separate ratification |
| hiding method dependence with tolerance | quarantine or version a corrected invariant method |

## Related documents

- [`../README.md`](../README.md): overview and quick start
- [`STATUS.md`](STATUS.md): engineering status and historical scientific ledger
- [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md): historical attestation plus erratum
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): contribution checks
