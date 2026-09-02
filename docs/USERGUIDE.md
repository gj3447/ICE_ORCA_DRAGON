# ICE_ORCA_DRAGON user guide

> Guide to the 75 committed entries currently exposed by the TypeScript/Effect CLI. Historical source files are
> not automatically runnable entries; `./ice list --json` is authoritative.

## Setup

```bash
git lfs install --local
git lfs pull --include="cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json"
npm ci
uv sync --locked
./ice doctor
```

The LFS pull hydrates the 529,370,671-byte Phase-44 evidence object; ontology hash validation requires
the hydrated bytes rather than the 134-byte pointer. `doctor` validates the Node major, package lock,
Python version, uv lock, and required numerical packages. A READY report describes the environment, not
the truth of a scientific claim.

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
./ice ontology guide --path current-status-in-five-stops
./ice ontology guide --graph hypercomplex --path hyper-projection-failure
./ice ontology guide --graph igrueqft --path igrueqft-negative-result-to-open-theory
./ice ontology show legacy::claim:DECLARED_P15_SET_HAS_GENUINE_PDG_SIGNAL
./ice ontology trace cpt::claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
```

Use `--graph hypercomplex`, `--graph legacy`, `--graph cpt`, or `--graph igrueqft` to restrict a query. A qualified ID such
as `legacy::claim:...` is unambiguous even when local IDs overlap. Cross-graph guide paths are
navigation-only: the four graphs remain independent research or memory graphs, not automatic physics
verdicts or external-KG mutations.

`./ice ontology validate` is the full integrity gate: it streams and hashes every tracked artifact,
including the 529 MB Phase-44 LFS object. `summary`, `show`, `trace`, and `guide` instead validate the
collection schema, graph semantics, and repository paths without reopening artifact payloads, so normal
navigation still works before that large LFS object is hydrated.

### Default CPT/TOE route and collection cohesion

Use the live summary rather than a copied node, edge, or hash total:

```bash
./ice ontology summary --json
./ice agent plan "<one bounded CPT question>" --graph cpt --json
./ice ontology show cpt::policy:toe-directed-critical-path-routing
./ice ontology show cpt::open:gate1-original-cycle-signed-global-intersections
./ice ontology guide --path cpt-role-bands-no-promotion
./ice ontology guide --graph cpt --path toe-current-critical-path
./ice ontology guide --graph cpt --path gate1-typed-object-handoff
./ice ontology guide --graph cpt --path v0-supporting-bridge-portfolio
./ice ontology guide --graph cpt --path p1-exact-real-root-handoff
./ice ontology guide --graph cpt --path p4-weyl-measure-raq-handoff
./ice ontology guide --path choice-invariance-cross-domain-audit
```

For core CPT work, the current G1 blocker is the default path; G2--G5 require compatible upstream typed
outputs. The P1--P7 V0 map is a supporting portfolio and does not automatically unblock the gate path.
The role-band view separates TOE core, the two G1 subblockers, supporting P1--P7 work and frozen
non-executable history. A fresh raw-C handoff should use the compact P1 and P4 paths: P1 starts with an
exact zero-evaluation bridge, while P4 is blocked at the complex-tail theorem before any endpoint runner.
A proposal is core-labelled only after human review identifies its canonical blocker, missing typed
object, bounded falsifiable output, and changed evidence edge. The planner is a review aid and never
authorizes execution or a physics claim.

For any proposed broad model, physics, empirical, or TOE interpretation, also read the
choice-invariance path. Promotion requires predeclared admissible choices, a mechanism-carrying typed
object, and two independent consumers inside the same graph. Reusing one residual or pointing to another
graph is not independence; a scoped result remains valid when this broader test is not met. There are no
current passing results. The authoritative policy is
[ICE_CHOICE_INVARIANCE_CROSS_DOMAIN_PROMOTION_2026-09-02.md](decisions/ICE_CHOICE_INVARIANCE_CROSS_DOMAIN_PROMOTION_2026-09-02.md).

For a policy, navigation, or multi-graph change, inspect the complete collection:

```bash
./ice ontology review --graph all --base HEAD
```

Keep the four graphs as independent evidence boundaries. The cohesion rule is to update the existing
canonical record and its explicit relations, then expose it through a reading path or quick answer; do
not duplicate a claim across graphs or infer corroboration from nearby topics. Validation rejects a
component with no programme anchor, and summary reports weak-component cohesion. Historical records
remain provenance and are not deleted or reinterpreted to simplify a route.

### Export and inspect the standards interoperability view

```bash
./ice ontology export --format dataset-jsonld --graph cpt > /tmp/cpt-research-dataset.jsonld
./ice ontology export --format nquads --graph cpt > /tmp/cpt-research-graph.nq
./ice ontology shacl --graph cpt --json
./ice ontology sparql 'ASK WHERE { GRAPH <urn:ice-orca-dragon:resource:graph:cpt> { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } }' --graph cpt
./ice ontology competency --json
./ice ontology crate output/cpt-review-crate --graph cpt --json
```

The native collection and graph JSON remain authoritative. The generated named RDF dataset adds
source-to-export PROV-O lineage and is checked with the bundled SHACL 1.0 Core shapes. SPARQL is a
restricted local 1.1 subset with structural, row, byte, and time bounds; it is not a general endpoint.
RO-Crate creation reserves one new direct child under `output/`, never overwrites an existing target,
packages RDF-equivalent enriched JSON-LD/N-Quads plus the explicitly digested compatibility JSON-LD,
and does not copy raw result files. These views improve interchange and
review; they do not ratify a claim or authorize a calculation.

`ontology competency` runs a small versioned ASK-only suite for durable content invariants: four graph
boundaries, the G1 dependency spine, P1/P4 non-promotion, one scoped claim/evidence chain, the absence of
Phase 57, and the retained negative or inconclusive boundaries in the other programmes. It tests the
graph representation, not the truth of the physics. The current human-oriented map is the
[research graph atlas](research/ICE_RESEARCH_GRAPH_ATLAS_2026-09-02.md).

### Use the graph-aware harness for research engineering context

```bash
./ice harness context cpt::open:gate1-original-cycle-signed-global-intersections --depth 2
./ice harness impact docs/decisions/ICE_LEAN_RESEARCH_RULES_2026-08-31.md
./ice harness check
```

`context` gives a bounded evidence/scope/policy/open-problem neighborhood for review before a material
change. `impact` maps an exact registered path to its graph context and explicitly reports unregistered
paths without forcing ontology registration. `check` is the full graph hash/evidence integrity gate. None
of these commands authorizes a kernel, promotes a scientific claim, or generates the next calculation;
the raw result remains the complete ledger. The operating design is documented in
[the graph-aware harness decision](decisions/ICE_GRAPH_AWARE_HARNESS_2026-09-01.md).

### Discover literature without widening execution permissions

```bash
./ice literature search "constrained quantization rigging map" --limit 10
./ice literature search "CPT symmetric universe" --json
npm run --silent mcp
```

`literature search` queries OpenAlex's public works graph and returns a time-stamped, maximum-20-result
discovery record. Read and cite the relevant primary source before using it in a research statement. It
does not run a kernel, write a raw result, add an ontology node, or authorize further work. `npm run --silent
mcp` starts the same bounded harness and discovery surface for an MCP host over stdio; it negotiates MCP
2026-07-28 with 2025-era compatibility and keeps stdout exclusively for protocol data. See [the MCP and
skill integration decision](decisions/ICE_RESEARCH_MCP_SKILL_INTEGRATION_2026-09-01.md).

### Turn source reading into bounded intuition data

```bash
./ice intuition validate --json
./ice intuition search "Which typed object separates unresolved intersections from zero?" \
  --target cpt::open:gate1-original-cycle-signed-global-intersections --json
```

`intuition search` federates one exact canonical open problem and bounded canonical GraphRAG context
with matching source-linked question lenses. Its explicit links are navigation data only: the sidecar is
not registered in the canonical ontology, is never ranked as evidence, and cannot authorize a runner.
Inspect the primary source and retain at most one bounded falsifiable question for `agent plan`. Keep
`UNRESOLVED`, `OUT_OF_SCOPE`, and a computed integer zero distinct. See the
[scientific-intuition signal-layer decision](decisions/ICE_SCIENTIFIC_INTUITION_SIGNAL_LAYER_2026-09-02.md).

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
./ice run phase30_conformal_bfv_determinant_line
./ice run phase31_homogeneous_bfv_superhessian
./ice run phase32_below_origin_lapse_intersection
./ice run phase33_fold_airy_uniformization
./ice run phase34_directed_fold_dual_continuation
./ice run phase35_reduced_detline_transport
./ice run phase36_airy_gauss_manin_connection
./ice run phase37_closed_fold_holonomy
./ice run phase38_joint_cycle_identifiability
./ice run phase39_finite_joint_intersection
./ice run phase40_m3_reflection_odd_intersection
./ice run phase41_m4_two_source_intersection
./ice run phase42_m4_fixed_root_checkpoint
./ice run phase42_m4_fixed_root_tangent_disentanglement
./ice run phase43_m4_high_precision_local_rhs_arbitration
```

Phase 41 is an example where exit 0 means a structurally valid typed run, while its payload reports
7/7 exact and 8/9 numerical contracts. The remaining numerical record is the explicit
`TANGENT_CONTROL_FAILED` plateau result; do not rewrite it as a nine-pass run or an infrastructure
failure.

Phase 42 is the corresponding diagnostic example: exit 0 means `VALID_TYPED_RUN`, while the payload
contains exactly 8/8 exact and 6/8 numerical passes. Its
`LOCAL_VARIATIONAL_IDENTITY_NOT_SUPPORTED` and
`REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE` records are retained scientific outcomes, not an invalid
run. The full tangent-disentanglement runner is heavyweight, may take hours, writes no repository file,
and emits one large `RESULT_JSON=` transport record. The committed 7.5 MB raw result is the captured
artifact; do not silently replace it with a prose-only summary.

Phase 43 preserves the same typed-run distinction: exit 0 accompanies 7/7 exact and 4/6 numerical
contracts. The two numerical `FAIL` records are complete non-invalidating scientific outcomes for the
source-agreement and all-33 finite-difference universal predicates. They preserve the observed 13/90
NumPy64-output tolerance crossings and five exceptions to the all-33 rule; they are not transport
failures and do not prove a wrong formula or unique code defect. The runner emits one approximately
51 MB `RESULT_JSON=` record and writes no result file itself. Use the committed 50,974,375-byte raw
capture as the byte-full authority instead of attempting to summarize away the non-PASS records.

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
| CPT × Temporal-Folded SUSY | `phase17_time_line_fold_algebra`, `phase18_gaussian_seam_spectrum`, `phase19_closed_sugra_bounce`, `phase20_two_sheet_wdw_selection`, `phase21_connected_seam_gaussian`, `phase22_finite_mode_seam_density`, `phase23_homogeneous_minisuperspace_density`, `phase24_connected_starobinsky_interval`, `phase25_connected_lapse_scan`, `phase26_global_lapse_flow`, `phase27_lorentzian_lapse_endpoint`, `phase28_thimble_bfv_intersection`, `phase29_zero_lapse_uniform_kernel`, `phase30_conformal_bfv_determinant_line`, `phase31_homogeneous_bfv_superhessian`, `phase32_below_origin_lapse_intersection`, `phase33_fold_airy_uniformization`, `phase34_directed_fold_dual_continuation`, `phase35_reduced_detline_transport`, `phase36_airy_gauss_manin_connection`, `phase37_closed_fold_holonomy`, `phase38_joint_cycle_identifiability`, `phase39_finite_joint_intersection`, `phase40_m3_reflection_odd_intersection`, `phase41_m4_two_source_intersection`, `phase42_m4_fixed_root_checkpoint`, `phase42_m4_fixed_root_tangent_disentanglement`, `phase43_m4_high_precision_local_rhs_arbitration` |
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
- provenance and historical preregistration metadata only when it is present

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

New unnumbered work follows the active [lean research rules](decisions/ICE_LEAN_RESEARCH_RULES_2026-08-31.md).
No tier declaration, universal preregistration contract, or KG ratification is required. Use the smallest
relevant checks. Examples:

```bash
npm run check                 # TypeScript/Effect control plane
uv sync --locked              # Python/lock change
./ice doctor
./ice run <affected-name>     # numerical kernel change
```

For a new calculation, state one question, one output, and one non-claim; record the source
equations/conventions, command, environment, input, actual output, and failures in one raw record or
adjacent memo. Choose the relevant failure class—algebra/sign/unit, discretization/truncation,
solver/spectrum, gauge, or inference—and use only its 1--3 most relevant controls. An independent
derivation, symbolic identity, limiting case, precision/refinement sweep, basis/gauge variation, or
certified enclosure is useful only when it lowers that risk. Reproduction establishes repeatability, not
truth. Keep finite computed facts, numerical error, model interpretation, and open physical hypotheses
separate.

Preregistration and multiplicity/global-significance machinery are for confirmatory empirical work with
external data, not for ordinary deterministic exploration. Record exploratory searches as exploratory;
for a confirmatory likelihood, fix the primary observable and search/cut/nuisance/stopping choices before
looking at the decisive result, then disclose changes.

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
- [`../cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md`](../cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md): declared lateralized Airy basis identities and two sampled root-sheet laterals; the common-dual/global-contour choice remains open
- [`audits/REPRODUCIBILITY_2026-06-08.md`](audits/REPRODUCIBILITY_2026-06-08.md): historical attestation plus erratum
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): contribution checks
