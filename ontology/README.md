# Research ontology memory

> This directory is a human-readable memory and index over repository evidence. It is **not** a preregistration, research contract, scientific verdict, or knowledge-graph (KG) ratification. The machine-readable graph and run snapshots remain the traceable records; the prose pages are navigation aids.

## Current collection

| Programme | Human entry point | Machine record | Evidence and sources |
| --- | --- | --- | --- |
| CPT × Temporal-Folded SUSY | [Programme guide](./cpt-temporal-folded-susy/README.md) | [Research graph](./cpt-temporal-folded-susy/graph.json) | [Evidence guide](./cpt-temporal-folded-susy/references/evidence.md) · [Source inventory](./cpt-temporal-folded-susy/references/source-inventory.md) |

The graph uses [`research-graph/v1`](./schema/research-graph-v1.schema.json). The Phase 16–48 snapshots use [`research-run-evidence/v1`](./schema/research-run-evidence-v1.schema.json).

At the recorded `2026-08-22T04:08:22Z` graph update, the collection has 667 nodes and
1928 edges. Validation verifies 127/127 stored hashes (123 artifacts and 4 policies). The
Phase 16–48 run snapshots contain 445 named exact checks, all `PASS`, and 289 typed numerical-ledger
checks: 281 `PASS`, seven `FAIL`, and one `INCONCLUSIVE`. Phase 42 preserves one protocol-defined local
identity non-support result as `FAIL` and one derivative-reference result as `INCONCLUSIVE`. Phase 43
adds two complete, non-invalidating `FAIL` records for false universal PASS predicates: 13/90 local
NumPy64 outputs cross the frozen source threshold, and only 28/33 disclosed anomalies satisfy the
finite-difference rule, so its all-33 predicate fails. None of these typed non-PASS records invalidates
its zero-exit run. Phase 44 adds eight exact and seven numerical `PASS` records: exact identity of the
declared source and independent formulas, closed all-slot telescopes, and declared forward-error-model
coverage for all 13 disclosed mismatches and all 77 controls. These are local pinned-platform arithmetic
results, not a unique-cause, integrated-tangent, or global-cycle result. Phase 45 adds three exact and
six numerical `PASS` records: the independent 50/80-digit integrated tangents are stable under the
retained projection, source/reference tangents and root Jacobians agree at the `1e-12` scale, and the
historical `u2` failure remains unchanged. This narrows the local issue toward state-map finite
differences without rewriting Phase 41 or closing Gate 1. Phase 46 adds three exact and eight numerical
`PASS` records: the independent state-map ladder and Phase-45 tangent agree at all three roots, while
source endpoints that are close at the `1e-9` scale amplify into tight/Radau derivative-column failures.
Its scoped local-flow repair does not identify a wrong formula or one unique arithmetic/solver cause,
rewrite Phase 41, or close Gate 1. Phase 47 adds three exact and six numerical `PASS` records: all 36
retained-state and 18 paired-derivative signed telescopes close, independent 80/120-digit projections
agree, and the generated gradient-evaluation delta is the largest retained stage norm in every slot.
This descriptive localization neither identifies one unique suboperation nor integrates or validates a
gradient-only repair; intermediate propagation and solver accumulation remain open. One legacy
Phase 48 adds three exact `PASS`, seven numerical `PASS`, and three complete non-invalidating numerical
`FAIL` records. All eighteen gradient-only clongdouble paths, ninety intermediate local-flow probes,
and endpoint-state limits pass, but only one of three full ladders is stable and every root misses both
all-step derivative-reference limits. This useful negative control contradicts sufficiency of the
gradient-only adapter without weakening the Phase-46 independent full-flow result. One legacy
separately recorded Phase-18 numerical control brings the numerical-record total to 290 (282
pass, seven fail, one inconclusive). These
counts describe repository records, not independent replications or global scientific
confidence.

## Read and validate it

```bash
./ice ontology validate
./ice ontology summary
./ice ontology show claim:P16_BGG_BOSONIC_KINETIC_PARENT
./ice ontology trace claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
./ice ontology trace claim:P20_LEADING_DE_SITTER_WDW_ENVELOPE_SELECTS_5P44 --depth 2
./ice ontology trace claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY --depth 2
./ice ontology trace claim:P24_CONSTRAINT_PRESERVING_MIXED_HESSIAN_HAS_RANK_ONE --depth 2
./ice ontology trace claim:P28_DIRICHLET_BFV_GHOST_REMOVES_PROPER_LENGTH_ZERO_MODE --depth 2
./ice ontology trace claim:P29_FROZEN_QUADRATIC_KERNEL_HAS_DELTA_FLAT_IDENTITY_LIMIT --depth 2
./ice ontology trace claim:P30_FINITE_CUTOFF_LOCAL_COUPLED_FIELD_LAPSE_CYCLE_EXISTS --depth 2
./ice ontology trace claim:P31_PROPER_TIME_CANONICAL_DETERMINANT_SIGN_IS_STABLE --depth 2
./ice ontology trace claim:P32_SPECIFIED_BELOW_ORIGIN_FULL_LINE_HAS_RECORDED_PROJECTED_BASE_CROSSING --depth 2
./ice ontology trace claim:P33_RECORDED_DIRICHLET_CAUSTIC_HAS_SIMPLE_FOLD_AIRY_SCALE --depth 2
./ice ontology trace claim:P34_BOUNDED_DIRECTED_CONSTANT_PHASE_PAIR_EXISTS_BEYOND_FOLD --depth 2
./ice ontology trace claim:P35_TRACKED_REDUCED_ENDPOINT_DETERMINANT_LINE_IS_TRANSPORTABLE --depth 2
./ice ontology trace claim:P35_RELATIVE_ENDPOINT_TRANSPORT_FIXES_ABSOLUTE_MASLOV_ORIENTATION --depth 2
./ice ontology trace claim:P36_EXACT_LOCAL_AIRY_GAUSS_MANIN_CONNECTION_IS_FIXED --depth 2
./ice ontology trace claim:P36_PHASE32_PLUS_PHASE35_UNIQUELY_SELECTS_ONE_OUTGOING_FOLD_ARM --depth 2
./ice ontology trace claim:P37_LOCAL_BVP_ROOT_COVER_HAS_NONTRIVIAL_Z2_MONODROMY --depth 2
./ice ontology trace claim:P37_SAMPLED_REDUCED_HALF_FORM_HAS_CONDITIONAL_ORDER_FOUR_HOLONOMY --depth 2
./ice ontology trace claim:P37_ROOT_MONODROMY_ALONE_BREAKS_PHASE17_BASIS_EQUIVALENCE --depth 2
./ice ontology trace claim:P38_RECORDED_DATA_DO_NOT_LICENSE_INVERSE_JOINT_CYCLE_RECONSTRUCTION --depth 2
./ice ontology trace claim:P38_ROOT_SWAP_CAN_REPLACE_GAUSS_MANIN_CYCLE_TRANSPORT --depth 2
./ice ontology trace claim:P38_CONDITIONAL_GAMMA0_INPUT_MAPS_TO_BOTH_LOCAL_ARMS --depth 2
./ice ontology trace claim:P38_SAMPLED_TRACKED_ARMS_REMAIN_PROJECTED_DISJOINT_THROUGH_RET16 --depth 2
./ice ontology trace claim:P38_BOUNDED_LEDGER_SUFFICES_TO_FIX_GLOBAL_INTERSECTION_VECTOR --depth 2
./ice ontology trace claim:P39_FROZEN_M2_ACTION_HAS_GENUINE_POSITIVE_T_DISCRETE_JOINT_SADDLE --depth 2
./ice ontology trace claim:P39_DECLARED_M2_CAP_PIECES_HAVE_LOCAL_SIX_REAL_PLUS_ONE_CANDIDATES_ON_ONE_FROZEN_K_PATCH --depth 2
./ice ontology trace claim:P39_TWO_FROZEN_CAP_LOCAL_CANDIDATES_SUFFICE_TO_FIX_GLOBAL_INTERSECTION_VECTOR --depth 2
./ice ontology trace claim:P40_RANK_ONE_PHI_SOURCE_HAS_ANCHOR_SUBTRACTED_SIGN_REVERSING_ODD_RESPONSE --depth 2
./ice ontology trace claim:P40_FIVE_SAMPLED_M3_CAP_CANDIDATES_HAVE_LOCAL_FULL_R10_SIGN_PLUS_ONE --depth 2
./ice ontology trace claim:P40_RECORDED_LOCAL_M3_DATA_DO_NOT_LICENSE_BOUNDED_CHAIN_OR_GLOBAL_INTERSECTION_INFERENCE --depth 2
./ice ontology trace claim:P41_TWO_SOURCE_ODD_SUSCEPTIBILITY_HAS_STABLE_NUMERICAL_RANK_TWO --depth 2
./ice ontology trace claim:P41_FIVE_PRIMARY_M4_CAP_CANDIDATES_HAVE_LOCAL_FULL_R14_SIGN_PLUS_ONE --depth 2
./ice ontology trace claim:P41_RETAINED_TANGENT_CONTROL_FAILURE_LEAVES_BOTH_SOURCE_ROBUSTNESS_CLAIMS_INCONCLUSIVE --depth 2
./ice ontology trace claim:P41_RECORDED_LOCAL_M4_DATA_DO_NOT_LICENSE_CANONICAL_CROSS_CUTOFF_OR_GLOBAL_INTERSECTION_INFERENCE --depth 2
./ice ontology trace claim:P42_SOLVER_NOISE_AND_FROZEN_STEP_PAIR_ARTIFACT_SUPPORTED_AT_PHI_AND_A --depth 2
./ice ontology trace claim:P42_LOCAL_HESSIAN_ACTION_IDENTITY_ANOMALY_IS_SUPPORTED_WITHOUT_PROVING_A_BUG --depth 2
./ice ontology trace claim:P42_NORMALIZED_LOCAL_MATRIX_HOMOTOPY_SUFFICIENTLY_PRESERVES_FIXED_ROOT_SIGN --depth 2
./ice ontology trace claim:P42_REFERENCE_TANGENT_REMAINS_INCONCLUSIVE_AND_GLOBAL_PROMOTION_IS_PROHIBITED --depth 2
./ice ontology trace claim:P43_INDEPENDENT_HIGH_PRECISION_LOCAL_REFERENCE_IS_CORROBORATED_AT_ALL_FROZEN_SLOTS --depth 2
./ice ontology trace claim:P43_NUMPY64_LOCAL_RHS_OUTPUT_MISMATCH_IS_SUPPORTED_WITHOUT_PROVING_A_CODE_DEFECT --depth 2
./ice ontology trace claim:P43_DOUBLE_PRECISION_FD_ARTIFACT_EXPLAINS_ALL_33_PHASE42_ANOMALIES --depth 2
./ice ontology trace claim:P43_LOCAL_ARBITRATION_DOES_NOT_TEST_INTEGRATED_TANGENT_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P44_DECLARED_SOURCE_FORMULA_IS_EXACTLY_IDENTICAL_TO_THE_INDEPENDENT_MODEL --depth 2
./ice ontology trace claim:P44_ALL_DISCLOSED_NUMPY64_MISMATCHES_FIT_THE_DECLARED_MIXED_FORWARD_ERROR_MODEL --depth 2
./ice ontology trace claim:P44_LOCAL_ARITHMETIC_DECOMPOSITION_DOES_NOT_REPAIR_THE_TANGENT_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P45_INDEPENDENT_INTEGRATED_TANGENT_IS_PRECISION_STABLE_AT_THREE_FIXED_ROOTS --depth 2
./ice ontology trace claim:P45_SOURCE_TANGENT_AND_ROOT_JACOBIAN_AGREE_WITH_INDEPENDENT_REFERENCE --depth 2
./ice ontology trace claim:P45_TANGENT_CONTROL_FAILURE_IS_STABLE_TO_LOCAL_RHS_REPLACEMENT --depth 2
./ice ontology trace claim:P45_LOCAL_STABILITY_DOES_NOT_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P46_INDEPENDENT_STATE_MAP_U2_LADDER_IS_STABLE_AND_AGREES_WITH_TANGENT --depth 2
./ice ontology trace claim:P46_LOCAL_FLOW_RHS_REPAIR_IS_SUPPORTED_UNDER_FIXED_PROJECTION --depth 2
./ice ontology trace claim:P46_LOCAL_REPAIR_DOES_NOT_PROVE_SOURCE_FORMULA_DEFECT_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P47_LOCAL_SOURCE_FLOW_TELESCOPES_CLOSE_AT_ALL_RETAINED_SLOTS --depth 2
./ice ontology trace claim:P47_GENERATED_GRADIENT_EVALUATION_IS_LARGEST_RETAINED_MIXED_ARITHMETIC_STAGE --depth 2
./ice ontology trace claim:P47_LOCAL_BUDGET_DOES_NOT_BOUND_ENDPOINT_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P48_GRADIENT_ONLY_CLONGDOUBLE_PATHS_MATCH_LOCAL_FLOW_AND_ENDPOINT_LIMITS --depth 2
./ice ontology trace claim:P48_GRADIENT_ONLY_CLONGDOUBLE_REPAIRS_THE_FULL_U2_LADDER --depth 2
./ice ontology trace claim:P48_PLATFORM_ABLATION_DOES_NOT_CLOSE_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology show policy:ordered-five-gate-advancement
./ice ontology trace open:gate5-persistent-order-and-pole-splitting --depth 5
```

Every command also accepts `--json`. `show` accepts either a full node ID or a bare stable `claim_id`;
`trace` walks incoming and outgoing relations to the requested bounded depth.

The active `policy:recursive-self-application-audit` records the user-requested no-privileged-exception
lesson. Its own audit narrows it from universal literal recursion to a type-correct audit wherever a
claim grants one candidate explanatory privilege. `concept:invariant-difference-amplitude-and-record`
and `concept:recursive-objectivity-and-world-resistance` preserve the deeper synthesis. The central
philosophy and intuitive meditation are hash-tracked artifacts, explicitly not scientific evidence.

The active `policy:ordered-five-gate-advancement` records the user-mandated promotion route from one
specified original joint relative cycle to signed global intersections, hard CFU coefficients, the full
BFV/Pfaffian/Pin line, a physical spinorial charge and common constraint domain (or a typed obstruction),
and finally a persistent order parameter with interacting pole splitting. Downstream calculations may be
explored early, but they remain conditional until the earlier gate supplies its evidence-backed typed
output. The ordering is a revisable workflow rule governed by the recursive audit; it adds no physics
evidence and predicts no gate outcome.

Phase 38 starts Gate 1 without closing it. Its finite noninjective surrogate is only a schema-level
warning: the graph supports that the current records do not license inverse reconstruction without a
physical injectivity theorem or admissible completions, not that physical relative homology is
noninjective or that the physical cycle is nonunique. The numerical extension concerns sampled points on
one tracked branch plus a real-coefficient conjugation control, not a continuous two-arm census. Gate-2
hard-CFU work may be explored in parallel, while physical promotion remains dependent on Gate 1's typed
cycle output.

Phase 39 replaces the lapse-only sign inference with a direct local full-space pilot. For one frozen
two-segment configuration action and one post-feasibility fixed metric, it resolves one positive-\(T\)
discrete joint saddle and one numerically locally transverse candidate on each of two declared cap
pieces against a finite-radius, finite-time three-real-dimensional upward-chart patch. Both direct
\(\mathbb R^6\) configuration-coordinate signs are \(+1\). The calculation does not search the
straight arms or later cap intersections, exhaust roots or upward components, certify the exact
nonlinear upward manifold or a non-Stokes chamber, or classify all relative good ends. Consequently the
bounded-chain sum, complete signed vector, and `global_n_sigma` remain null rather than zero, and Gate 1
remains open.

Phase 40 raises the local pilot to the first cutoff with a reflection-odd interior-history sector. In
one frozen \(m=3\) regulator, a rank-one phi endpoint source has a nonzero anchor-subtracted,
sign-reversing sampled odd response, while five sequentially tracked local \(\mathbb R^{10}\) cap-piece
candidates have direct declared sign \(+1\) at the five sampled delta values. The flow mobility is fixed;
the delta-dependent Morse launch ellipsoids and their radius ladder are chart data, not a metric-homotopy
test. Only three points receive the full finite-difference and sampled-flow audit, and the local
K-launch-coordinate clamp is not a full odd-sector ablation. The second source direction, \(m=4\), a
continuous branch theorem, the entire chain, exact nonlinear upward manifold, Stokes chamber and good
ends remain open, so every chain/global output stays null and Gate 1 remains open.

Phase 41 raises the local control to (m=4) and adds an independent a-only endpoint source. The
anchor-subtracted two-source susceptibility has stable numerical rank two under the frozen
dimensionless finite-precision rule, and five local (mathbb R^{14}) cap candidates are resolved with
direct declared sign (+1). Reflection, orientation, overlap-chart, launch-radius, launch-shape, and
first-cap path controls pass. The predeclared finite-difference tangent audit does not: the first
adjacent frozen step pair for `u2` changes by 22–80% at the three audited points, above the 2% threshold.
The five roots remain recorded, but both source-scoped robustness outputs are consequently
inconclusive. The m3/m4 signs are only separately audited descriptive data; no common determinant line,
cutoff limit, bounded-chain sum, complete vector, or quantum-gravity result is inferred. Six promoted
outputs remain null, null is not zero, and Gate 1 remains open.

Phase 42 recursively audits the retained Phase-41 tangent failure at the three immutable roots. Under
the frozen multi-label rules, solver noise and the old first-pair reference artifact are supported at
`phi_plus` and `a_plus`, while multiple reference-stable local Hessian-action identities exceed their
threshold at all three roots. That local anomaly is not proof of a code bug: the returned time column is
assembled at its own augmented endpoint, and its comparison with a different state-only endpoint lies
inside the cross-tier solver/state envelope, so it is excluded as independent bug evidence. A
sufficient normalized local matrix homotopy preserves sign `-1` at all three points, but the
`shared_zero` `u2` R4 neighbor change remains above the frozen reference-stability threshold. The
reference tangent therefore remains inconclusive; Phase 41 stays 8/9, sixteen prerequisites remain
false, six promoted outputs remain null, and Gate 1 remains open.

Phase 43 recursively audits the local derivative layer without rerunning a root or tangent ODE. Its
independently rebuilt exact and 80/120-decimal reference is corroborated at all 90 frozen slots. The
byte-pinned NumPy64 Hessian-action output crosses the uniform `5e-13` normwise threshold at 13/90
slots, which supports an operational pipeline mismatch but not a wrong formula, unique code defect, or
unique cause. The fixed same-step binary64 finite-difference rule is supported at 28/33 disclosed
Phase-42 anomalies, but five complete exceptions contradict the frozen all-33 sufficient claim. No
integrated tangent, ODE solver-noise, time-column, reference-tangent, local orientation, determinant,
or global-cycle result is added. Phase 41 stays 8/9, Phase 42 stays inconclusive, sixteen prerequisites
remain false, six global outputs and seven desired outputs remain null, and Gate 1 remains open.

Phase 44 decomposes that frozen NumPy64 layer without rerunning a root, ODE, or integrated tangent.
For all three declared source variants, exact canonicalization finds zero difference between the
source and independent action, gradient, and Hessian expressions. Across all 90 frozen slots, the
signed S0-to-S7 telescopes close; coefficient, state, Hessian, and contraction contributions are
nonzero and potentially cancelling, while the declared componentwise and normwise forward-error model
covers all 13 disclosed mismatches and all 77 controls. The same nonexclusive tri-state pattern occurs
in both cohorts, so no unique stage, defect, or cause is selected and no source rewrite is authorized.
Phase 41 stays 8/9, the Phase-42 reference tangent stays inconclusive, the historical Phase-43 13/90
label is preserved, sixteen prerequisites remain false, six global and seven desired outputs remain
null, and Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

## How to read a claim

Follow a claim in this order:

1. Read the claim's `state`, `summary`, and `VALID_WITHIN` scope.
2. Follow `HAS_EVIDENCE` from the claim to an evidence node and inspect the edge's `polarity`. `SUPPORTS` and `CONTRADICTS` carry the scientific direction.
3. Follow `DEFINED_IN` and `RECORDED_IN` to the executable and observed run snapshot.
4. Follow `DERIVED_FROM` for a calculation source or `CITES` for literature framing and boundary conditions.
5. Follow `BLOCKED_BY` before promoting a finite witness into a physical construction. Follow
   `MOTIVATES` for a distinct next problem suggested by a terminal result; solving it does not reverse
   that result.

A check marked `PASS` means that its named contract passed; it does **not** mean that every associated
scientific claim is true. A `FAIL` records a failed contract, not automatically a negation of the
physical proposition. In Phase 41 the tangent-control `FAIL` leaves the stronger source-robustness
outputs inconclusive while the separately accepted local-root claim remains supported. In Phase 42 one
typed `FAIL` records a local numerical identity that is not supported and one `INCONCLUSIVE` preserves
an unstable derivative reference; neither is a failed run or proof of a software defect. Conversely, a
passing counterexample check can attach to a claim with `polarity: CONTRADICTS`. In Phase 43 the two
schema-level `FAIL` records are complete, non-invalidating failures of universal sufficient predicates:
they preserve the 13/90 source-mismatch and 28/33 finite-difference outcomes without calling the run
invalid or converting a failed all-33 claim into evidence that finite-difference error is absent.
Phase 44 has no typed non-PASS record: its seven numerical `PASS` entries establish only their named
local arithmetic contracts. Forward-model coverage is compatibility on the pinned platform, not proof
of correct rounding, a unique causal stage, an integrated tangent, or a global physical construction.
Phase 45 also has no typed non-PASS record. Its integrated-tangent agreement is limited to three fixed
roots, one shared source state trajectory, and a final complex128 projection; it does not recompute the
failed state-map finite-difference ladder or promote a local Jacobian sign into global topology. Phase
46 likewise has no typed non-PASS record. Its `LOCAL_FLOW_RHS_REPAIR_SUPPORTED` classification is a
fixed local numerical comparison: an 80-digit local RHS inside a complex128 integrator repairs the
three-step ladder and agrees with the independent tangent, but this does not prove a wrong source
formula, unique arithmetic/solver cause, arbitrary-precision state theorem, or global topology.
Phase 47 also has no typed non-PASS record. Its closed retained-state and paired-Dh telescopes localize
the largest signed-stage norm to generated gradient evaluation under the frozen budget, but the stage
still combines multiple suboperations and signed terms can cancel. Because the run integrates no new
trajectory and retains no intermediate path, it does not establish a gradient-only repair, endpoint
error-transport or solver bound, unique defect, or global topology.
Phase 48 retains three typed numerical `FAIL` records without invalidating its zero-exit run. They are
failures of the universal all-root full-ladder, independent-column, and Phase-45 tangent predicates.
The simultaneously passing local-flow and endpoint-state controls make the result a useful
platform-specific negative control: the gradient-only adapter improves the integrated paths but is not
sufficient for the complete derivative ladder. It is not evidence against the Phase-46 independent
full-flow path, a portable long-double theorem, one unique defect, or global topology.

## Identifier families

| Prefix | Meaning |
| --- | --- |
| `programme:` | Overall research question |
| `phase:` | Bounded calculation cycle |
| `concept:` | Reusable definition or distinction |
| `claim:` | Scoped, falsifiable statement |
| `evidence:` | Verified check group |
| `scope:` | Assumptions and exclusions |
| `open:` | Missing construction or unresolved question |
| `source:` | Primary or technical literature source |
| `artifact:` | Repository file |
| `policy:` | Repository workflow rule; never scientific evidence |
| `edge:` | Directed graph relation |
| `result:` | Observed executable-run snapshot |

Edges are read exactly in their stored `from → relation → to` direction. The current graph has no `SUPERSEDES` relation: `EXTENDS`, `FOLLOW_UP_TO`, and `CONTRASTS_WITH` preserve narrower cross-phase meanings without silently replacing earlier claims.

## KG bridges

`kg_bridges` are lookup memory between local IDs and live external UIDs. `EXACT` means the programme identity was matched; `RELATED` means topical overlap, not claim identity. `RESOLVED` means the UID lookup succeeded, not that the external KG accepted, reviewed, or ratified this repository's evidence. `UNRESOLVED` preserves a lookup key without inventing a UID.

For the programme's claims, scopes, blockers, and bridge list, continue to the [CPT × Temporal-Folded SUSY guide](./cpt-temporal-folded-susy/README.md).
