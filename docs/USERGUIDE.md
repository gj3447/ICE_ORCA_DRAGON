# ICE_ORCA_DRAGON user guide

> Guide to the 60 committed entries currently exposed by the TypeScript/Effect CLI. Historical source files are
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

Research claims are a separate catalog from runnable kernels. Inspect and validate them by stable ID:

```bash
./ice ontology validate
./ice ontology summary
./ice ontology show claim:P17_STANDARD_LOCAL_Q_HALF_EXCHANGE
./ice ontology trace claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
```

This graph is a searchable evidence map, not an automatic physics verdict or external-KG mutation.

## Run one kernel

```bash
./ice run cd_path_amplitude_v2
./ice run derive_mass_ratios_ICE
./ice run prove_higgs_ZD_doublet
./ice run queue_02_4condition_diagnostic
./ice run phase19_closed_sugra_bounce
./ice run phase20_two_sheet_wdw_selection
./ice run phase21_connected_seam_gaussian
./ice run phase22_finite_mode_seam_density
./ice run phase23_homogeneous_minisuperspace_density
./ice run phase24_connected_starobinsky_interval
./ice run phase25_connected_lapse_scan
./ice run phase26_global_lapse_flow
./ice run phase27_lorentzian_lapse_endpoint
./ice run phase28_thimble_bfv_intersection
./ice run phase29_zero_lapse_uniform_kernel
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
| CPT × Temporal-Folded SUSY | `phase17_time_line_fold_algebra`, `phase18_gaussian_seam_spectrum`, `phase19_closed_sugra_bounce`, `phase20_two_sheet_wdw_selection`, `phase21_connected_seam_gaussian`, `phase22_finite_mode_seam_density`, `phase23_homogeneous_minisuperspace_density`, `phase24_connected_starobinsky_interval`, `phase25_connected_lapse_scan`, `phase26_global_lapse_flow`, `phase27_lorentzian_lapse_endpoint`, `phase28_thimble_bfv_intersection`, `phase29_zero_lapse_uniform_kernel` |
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
green. See [`audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md).

## Run a scientific task

No tier declaration or preregistration contract is required. Use the smallest relevant checks. Examples:

```bash
npm run check                 # TypeScript/Effect control plane
uv sync --locked              # Python/lock change
./ice doctor
./ice run <affected-name>     # numerical kernel change
```

For a new calculation, record the source equations/conventions, command, environment, input, and actual
output. Use an independent derivation, symbolic identity, limiting case, or precision sweep when it
materially lowers error risk. Reproduction establishes repeatability, not truth. Keep computed facts,
physical interpretation, and open hypotheses separate.

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
| treating a numerical match as confirmation | check alternatives, units, selection effects, and a null model when relevant |
| treating reproduction as independent evidence | repeated execution establishes repeatability, not independent support |
| hiding method dependence with tolerance | quarantine or version a corrected invariant method |

## Related documents

- [`../README.md`](../README.md): overview and quick start
- [`STATUS.md`](STATUS.md): engineering status and historical scientific ledger
- [`../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md`](../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md): closed-SUGRA bounce existence calculation
- [`../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md`](../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md): leading WDW initial-value selection control
- [`../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md`](../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md): normalized connected Gaussian seam and flux-prior control
- [`../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md`](../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md): finite-mode seam density and noncompact zero-mode obstruction
- [`../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md`](../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md): constrained rigging-map density and quadratic zero-root obstruction
- [`../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md`](../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md): connected interval response and constraint-reduced mixed channel
- [`../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md`](../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md): proper-length saddle, Schur reduction, and real simple fold
- [`../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md`](../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md): bounded constant-phase arm and Airy fold control
- [`../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md`](../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md): Lorentzian half-line and zero-lapse endpoint control
- [`../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md): bounded crossing and reduced BFV--BRST diagnostic
- [`../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md`](../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md): distributional identity-kernel and reduced BFV modulus-measure control
- [`audits/REPRODUCIBILITY_2026-06-08.md`](audits/REPRODUCIBILITY_2026-06-08.md): historical attestation plus erratum
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): contribution checks
