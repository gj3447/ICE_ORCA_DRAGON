# Research ontology memory

> This directory is a human-readable memory and index over repository evidence. It is **not** a preregistration, research contract, scientific verdict, or knowledge-graph (KG) ratification. For an executed calculation, its raw `RESULT.json` is the single check-ledger source of truth; the graph retains the artifact hash, conclusion, and only the minimum check locators needed to find it. Run snapshots and prose pages are historical provenance and navigation aids, not duplicate ledgers.

Update this index only when a calculation materially changes a claim's status, direct evidence, applicable scope, or a next open problem. Do not register ordinary intermediate work, wording changes, method notes, or a verifier result merely to satisfy a process step.

## Graph-aware harness

The graph is also the bounded context source for `./ice harness`: `context <node>` groups the nearby
claims, evidence, scope, source, artifact, policy, and open-problem records; `impact <path>` locates an
exact registered artifact/policy or graph path before it is changed; and `check` runs full collection
integrity validation. The harness is human-directed and does not grant execution authorization, create
an automatic next task, or duplicate a raw result's check ledger. See the active
[graph-aware harness decision](../docs/decisions/ICE_GRAPH_AWARE_HARNESS_2026-09-01.md).

## Current collection

| Programme | Human entry point | Machine record | Evidence and sources |
| --- | --- | --- | --- |
| Hypercomplex hypothesis testbench | [Programme guide](./hypercomplex/README.md) | [Research graph](./hypercomplex/graph.json) | [Source inventory](./hypercomplex/references/source-inventory.md) |
| Legacy predictions and narrative | [Programme guide](./legacy-predictions/README.md) | [Research graph](./legacy-predictions/graph.json) | [Source inventory](./legacy-predictions/references/source-inventory.md) |
| CPT × Temporal-Folded SUSY | [Programme guide](./cpt-temporal-folded-susy/README.md) | [Research graph](./cpt-temporal-folded-susy/graph.json) | [Evidence guide](./cpt-temporal-folded-susy/references/evidence.md) · [Source inventory](./cpt-temporal-folded-susy/references/source-inventory.md) |
| IG-RUEQFT locality audit | [Programme guide](./igrueqft-locality/README.md) | [Research graph](./igrueqft-locality/graph.json) | [Source inventory](./igrueqft-locality/references/source-inventory.md) |

The [collection manifest](./collection.json) uses
[`research-collection/v1`](./schema/research-collection-v1.schema.json); each independent graph uses
[`research-graph/v1`](./schema/research-graph-v1.schema.json). The Phase 16–56 and non-numbered Gate-1 run snapshots use
[`research-run-evidence/v1`](./schema/research-run-evidence-v1.schema.json). Historical numbered
snapshots carry a `P…` phase label; independent unnumbered calculations use `phase: null` and retain
their authoritative semantic check IDs without a fabricated phase prefix.

At the recorded `2026-08-31T07:50:05Z` collection update, the four graphs have 1,478 nodes, 3,831 edges,
and 316 claims: 191 supported, 114 contradicted, and 11 inconclusive. Validation verifies all 410 stored
hashes (400 artifacts and 10 policies); 70 unresolved external bridges remain explicit warnings. The
CPT graph now also hash-indexes the Phase 11–15R historical lead-in, with Phase 15A kept strictly as an
invalid-sequence provenance break rather than scientific evidence. The independent IG-RUEQFT graph
records one finite (N=64) free-U(1) locality oracle: its registered bulk-volume predicate is
contradicted and the observed dephased entropy remains subvolume on the sampled sizes, while a general
interacting/continuum verdict stays inconclusive. In the V0 lane, one declared weighted raw-\(C\)
candidate now has a fixed-\(p\) limit-circle/limit-point classification and \((1,1)\) extension debt;
its measurable global domain and \(C/H\) equivalence remain open. The later selected-\(H\) exact map is
support-restricted, the finite BFV sign transport remains relative, and the closed-\(S^3\) lane now
separates a fixed-metric matter-only \(DH\) strain obstruction from its finite projection remainder.
One selected \(Q_2\) metric-plus-matter ambient \(DH\) packet cancels that strain while retaining its
\(L=2\) omitted \(k=3\) remainder. The graph separately indexes the \(n=1\) trace-only convention, the
raw-\(C\) \(Q=4\) entering-sensitivity anchor, and the fixed-box nonreal branch precondition. General
ADM \(DD/DH/HH\), HDA/Jacobi, the actual nonreal endpoint-to-Weyl-to-measure chain, raw-\(C\) RAQ and
anomaly problems remain open. The current physics-discovery gap map records those dependencies without
treating them as automatic successors. None of these results is a physics or TOE promotion.

The Phase 16–56 run
snapshots contain 498 named exact checks, all `PASS`, and 360 typed numerical-ledger checks: 343
`PASS`, fourteen `FAIL`, and three
`INCONCLUSIVE`. Phase 42 preserves one protocol-defined local
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
gradient-only repair; intermediate propagation and solver accumulation remain open.
Phase 48 adds three exact `PASS`, seven numerical `PASS`, and three complete non-invalidating numerical
`FAIL` records. All eighteen gradient-only clongdouble paths, ninety intermediate local-flow probes,
and endpoint-state limits pass, but only one of three full ladders is stable and every root misses both
all-step derivative-reference limits. This useful negative control contradicts sufficiency of the
gradient-only adapter without weakening the Phase-46 independent full-flow result. Phase 49 adds three
exact and eleven numerical `PASS` records: all eighteen complete-flow paths, ninety probes, endpoint
states, all full ladders, and both derivative references pass after retaining clongdouble through the
complete local flow before one solver-boundary projection. This resolves only the pinned-platform
implementation choice; formal endpoint transport, solver/subtraction separation, and portability remain
open. Phase 50 adds six exact and eight numerical `PASS` records. All five source-labelled saddles
complete the declared stabilized \(m=4\to m=5\) fine, coarse, and reverse paths with fixed inertia;
both positive metric choices and all three action/metric orderings return the same oriented local upward
nine-plane at the sampled endpoint. This is one finite-dimensional, regulator-dependent local bridge,
not a Gamma–K intersection continuation, cutoff theorem, nonlinear upward manifold, determinant line,
global cycle, or physical claim. Phase 51 adds six exact `PASS`, nine numerical `PASS`, and one
numerical `INCONCLUSIVE` record. All frozen continuation, reflection, full-J, path-tangent, endpoint,
action, and first-cap controls pass, but the CSE/non-CSE same-point RHS relative comparison reaches
`1.690e-8` against `5e-10`. The valid run is consequently local-continuation `INCONCLUSIVE`, not
no-root or contradicted; the Phase-50 continuation problem and Gate 1 remain open. The separately
recorded Phase-18 numerical control remains included in the collection totals above. Phase 52 reproduces 19 hidden binary64 temporaries in each
pinned m=4 and m=5 joint CSE evaluation and supports an element-local clongdouble repair on the six
static source/lambda slots: maximum gradient and RHS relative errors are `7.051e-11` and `1.567e-10`,
below `5e-10`. The dtype-correct joint long-namespace candidate remains a declared non-invalidating
accuracy `FAIL` at `7.625e-9`. Phase 53 then executes the complete frozen replay. All eight exact and
ten of eleven numerical gates pass, including the independent six-slot 80/120-decimal full-evaluator
reference, 54 canonical Hessian probes, 68 accepted roots, 146 retained integrations, and all
action/first-cap ledgers. The sole comparison to the saved pinned Phase-51 global non-CSE backend remains
`INCONCLUSIVE` at `6.645e-9` against `5e-10`; this narrows the next calculation to that backend rather
than authorizing straight-arm search or any global, physics, or TOE promotion. Phase 54 then runs a
static six-state schedule/arithmetic matrix. Both global non-CSE cells remain diagnostic `FAIL`, while
both element-local cells pass all 12 selector records; the worst active relative errors are respectively
`6.763e-9`, `7.598e-9`, `2.243e-10`, and `1.567e-10` against `5e-10`. This supports element-local
schedule-only sufficiency on the six launch states, not a unique primitive defect or trajectory theorem.
It runs zero roots and zero ODEs, leaves Phase 51 and Phase 53 unchanged, and opens only the bounded
Phase-55 three-root/six-ODE trajectory-validator qualification. Phase 55 completes that validator as a
valid reconstruction `NONPASS`: all six ODEs and fifteen element-local trajectory pairs pass, and the
Phase-54 schedule matrix is reproduced, but the explicitly P50-saddle-pinned lambda-half reconstruction
has scaled residual `2.675e-7` and saved-scalar difference `2.673e-7`, both above the unchanged `2e-7`
gate. The backend agreement is therefore diagnostic rather than a qualified schedule transfer. The
Phase-56 full-replay candidate remains null. Phase 56 then executes the one permitted one-root
lambda-half terminal diagnostic: all eight exact and eight numerical aggregates pass, one fresh saddle
root and eight `EL_long` ODEs complete, both P50-center corners retain residual-target `NONPASS`, and
both fresh-center corners recover the saved target under both frozen profiles. This supports a bounded
factorial association, not exact historical Phase-53 bytes or a general causal theorem. The one-shot
exception is consumed: the reconciliation route is `KILL`, full replay and Phase 57 are unauthorized,
`next_phase=null`, Gate 1 remains open, and global promotion remains prohibited. A later execution-free
exact review narrows the straight KILL to its implemented anchor-through \(\delta=qy\) class and
constructs one phase-locked affine/curved fixed-\(a\) scalar branch with two uniform good field ends
across the finite lower-bypass regulator. A second exact review expands the branch into a strict
full-rate-good horizontal-affine phase band, proves that its two-arm-admissible tails contract to one
principal reduced class, and separates exact phase cancellation from convergence: the continuous
\(0<\lambda<2\) family disproves representative uniqueness. The literal real-field arm restrictions are
the oscillatory boundary; extending \(b=0\) across the complex cap is only a candidate lift, and current
records do not establish a source-selected joint cycle. These proofs add no run-ledger checks. A later
non-numbered, consumed one-shot separately records 16 executable exact `PASS` entries, three separately
reviewed analytic theorem guards, and zero numerical checks. For a newly declared fixed-\(a\), \(m=2\)
ordered scalar control it keeps the source link with scalar orientation `+1` on lapse tests supported
away from \(N=0\), while the zero-including full \(q\)-paired distribution remains open. Those 16 entries
are not folded into the Phase 16–56 total, and the three theorem guards are not machine-check entries.
The next generic bounded, non-numbered finite \(m=2\) bosonic control separately records 17 exact
`PASS` entries, two theorem guards and four 70-digit numerical `PASS` checks. Opposite kinetic signs
show that neither one common \(N-i0\) nor \(N+i0\) absolutely damps the unchanged real
\(p_a,p_\phi\) axes. Declared centered complex momentum rays reproduce the fiberwise Gaussian
pushforward, and a standard-Fresnel frozen-\(A\) flat tangent gives the negative-arm ratio \(-1\).
That result does not prove simultaneous nonlinear configuration admissibility, source deformation,
gauge/FP/BFV completion, zero lapse or a physical original cycle. Its entries are also kept separate
from the numbered Phase 16–56 totals. The subsequent non-numbered trace-gauge control separately records
22 executable exact `PASS` entries, five reviewed analytic scope guards, and two numerical `PASS`
checks. It supports a genuine local homogeneous simple-root constraint reduction away from the FP
horizon and formal lower-lateral convergence of the remaining scalar fiber. It contradicts only the
shortcut of appending a static trace delta/FP factor to the unchanged proper-time fixed-\(a\), \(m=2\)
source. A replacement gauge, action, endpoint-state problem and BFV measure remain an open dependency,
not an automatic next run; `automatic_next=null`, Gate 1 remains open, and all physical/global/TOE
outputs remain null. Its bounded closed-FRW \(V=0\) successor then records 16 exact `PASS` entries,
seven reviewed analytic scope guards, and five numerical `PASS` checks from six high-precision
quadratures. On the frozen \(p_\phi=+1\), \(0\le P\le1/2\), \(R>0\), \(D>0\) component it supports
one classical local on-shell fixed-\(\Phi_*\) relational endpoint action, finite local static hit, local
FP reduction, and time-dependent same-orbit control. The raw-static, HTV improved-static, relational,
and auxiliary mixed-polarization actions are separate ledgers. All four frozen scientific decision
rows terminate as valid results, and scientific NONPASS no longer creates a diagnostic descendant.
At that stage the full off-shell chart, normalized quantum endpoint states, replacement ghost/BFV source, old
fixed-\(a\) equality and full-real-lapse distributional \(\delta(C)\) physical-inner-product kernel
remain open; `automatic_next=null`, Gate 1 stays open, and global/physics/TOE outputs stay null. None of
this supplies scale-factor/joint ends, regulator removal, a complete census, an original cycle,
a global coefficient, physics, or TOE. These counts describe repository records, not independent
replications or global scientific confidence.

A subsequent bounded closed-FRW \(V=0\) calculation separately records 18 executable exact `PASS`
entries, eight reviewed analytic scope guards, and three numerical `PASS` checks from six root-method
calls. It connects the on-shell result to an exact classical Darboux chart on
\(\mathcal U_+=\{p>0,3p^2-2P^2>0\}\) across arbitrary real \(c=C\), with endpoint potential
\(B=PQ+W-cT-pW_p\), and recovers \(\Phi_*\) and \(B=P\) at \(c=0\). The KEEP is componentwise and
onto an open image: other components, an all-component/global atlas, normalized quantum endpoint
states, the ghost/BFV replacement source, old fixed-\(a\) equality, full-real-lapse distributional
\(\delta(C)\) kernel, zero lapse, determinant orientation, physical original cycle and global vector
remain open or null. All five scientific decision rows terminate, `automatic_next=null`, Gate 1 stays
open, and no physics or TOE claim is promoted.

## Read and validate it

`validate` is deliberately the expensive integrity command and streams every hash-tracked artifact.
The read commands (`summary`, `show`, `trace`, and `guide`) perform structural and semantic collection
validation without reopening artifact payloads; intuitive lookup therefore does not depend on the
529 MB Phase-44 LFS object.

```bash
./ice ontology validate
./ice ontology summary
./ice ontology guide --path current-status-in-five-stops
./ice ontology guide --graph hypercomplex --path hyper-projection-failure
./ice ontology guide --graph legacy --path legacy-preregistration-provenance
./ice ontology guide --graph igrueqft --path igrueqft-negative-result-to-open-theory
./ice ontology show igrueqft::claim:IGRUEQFT_GROUP_AVERAGING_MAKES_RECORDED_ENTANGLEMENT_BULK_LOCAL
./ice ontology trace igrueqft::open:igrueqft-continuum-interacting-locality-discriminator --depth 2
./ice ontology guide --graph cpt --path collar-admissibility-to-single-source-parent-and-tangency
./ice ontology guide --graph cpt --path gate1-anchor-through-kill-to-phase-locked-branch
./ice ontology show cpt::claim:G1_SINGLE_COMMON_LATERAL_ABSOLUTELY_DAMPS_UNCHANGED_REAL_PA_PPHI_AXES
./ice ontology trace cpt::claim:G1_DECLARED_COMPLEX_BOSONIC_MOMENTUM_RAYS_REPRODUCE_FINITE_M2_PUSHFORWARD --depth 2
./ice ontology show cpt::claim:G1_STATIC_TRACE_FP_GAUGE_CAN_BE_APPENDED_TO_UNCHANGED_PROPER_TIME_M2_SOURCE
./ice ontology trace cpt::claim:G1_HOMOGENEOUS_TRACE_PAIR_GIVES_LOCAL_SIMPLE_ROOT_CONSTRAINT_REDUCTION --depth 2
./ice ontology show cpt::claim:G1_CLOSED_FRW_V0_TRACE_GAUGE_HAS_LOCAL_ON_SHELL_RELATIONAL_ENDPOINT_ACTION
./ice ontology trace cpt::claim:G1_CLOSED_FRW_V0_TRACE_GAUGE_HAS_LOCAL_ON_SHELL_RELATIONAL_ENDPOINT_ACTION --depth 2
./ice ontology show cpt::claim:G1_CLOSED_FRW_V0_P_POSITIVE_R_POSITIVE_COMPONENT_HAS_CLASSICAL_OFFSHELL_DARBOUX_CHART
./ice ontology trace cpt::claim:G1_CLOSED_FRW_V0_P_POSITIVE_R_POSITIVE_COMPONENT_HAS_CLASSICAL_OFFSHELL_DARBOUX_CHART --depth 2
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
./ice ontology trace claim:P49_FULL_FLOW_CLONGDOUBLE_PASSES_ALL_FROZEN_STATE_MAP_CONTROLS --depth 2
./ice ontology trace claim:P49_PHASE48_49_ABLATION_SUPPORTS_LATE_COMPLETE_FLOW_PROJECTION --depth 2
./ice ontology trace claim:P49_SCOPED_REPAIR_DOES_NOT_PROVE_PORTABILITY_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace claim:P50_FIVE_FROZEN_M4_SADDLES_CONTINUE_TO_M5_ON_DECLARED_STABILIZED_PATHS --depth 2
./ice ontology trace claim:P50_LOCAL_UPWARD_NINE_PLANE_TRANSPORT_HAS_CONSISTENT_ORIENTED_ENDPOINT --depth 2
./ice ontology trace claim:P50_SAMPLED_LOCAL_TRANSPORT_DOES_NOT_ESTABLISH_CUTOFF_STABILITY_OR_GLOBAL_INTERSECTION --depth 2
./ice ontology trace claim:P51_FROZEN_PHI_PLUS_GAMMA_K_CONTINUATION_REMAINS_INCONCLUSIVE_AT_CSE_NONCSE_RHS_GATE --depth 2
./ice ontology trace claim:P51_LOCAL_GAMMA_K_RUN_DOES_NOT_ESTABLISH_ROOT_EXHAUSTION_OR_GLOBAL_INTERSECTION --depth 2
./ice ontology trace open:p51-cse-noncse-clongdouble-rhs-consistency --depth 2
./ice ontology trace claim:P52_PHASE51_HIDDEN_BINARY64_CSE_CONTRACT_VIOLATION_IS_REPRODUCED --depth 2
./ice ontology trace claim:P52_ELEMENT_LOCAL_CLONGDOUBLE_RHS_REPAIR_IS_SUPPORTED_ON_SIX_STATIC_SLOTS --depth 2
./ice ontology trace claim:P52_STATIC_REPAIR_DOES_NOT_RATIFY_PHASE51_CONTINUATION_OR_GLOBAL_INTERSECTION --depth 2
./ice ontology trace claim:P53_REPAIRED_REPLAY_PASSES_INDEPENDENT_REFERENCE_AND_NONBACKEND_CONTROLS --depth 2
./ice ontology trace claim:P53_FULL_REPLAY_REMAINS_INCONCLUSIVE_AT_PINNED_PHASE51_GLOBAL_NONCSE_BACKEND --depth 2
./ice ontology trace claim:P53_VALID_LOCAL_REPLAY_DOES_NOT_LICENSE_STRAIGHT_ARM_OR_GLOBAL_PROMOTION --depth 2
./ice ontology trace open:p53-full-repaired-phase51-continuation-rerun --depth 2
./ice ontology trace open:p54-pinned-phase51-global-noncse-backend-diagnostic --depth 2
./ice ontology trace claim:P54_ELEMENT_LOCAL_SCHEDULE_ALONE_IS_SUFFICIENT_ON_SIX_STATIC_SLOTS --depth 2
./ice ontology trace open:p55-p53-trajectory-schedule-transfer-audit --depth 2
./ice ontology trace claim:P55_P50_SADDLE_PINNED_RECONSTRUCTION_MISSES_SAVED_PHASE53_RESIDUAL_AT_LAMBDA_HALF --depth 2
./ice ontology trace claim:P55_ELEMENT_LOCAL_BACKEND_AGREEMENT_IS_DIAGNOSTIC_AFTER_RECONSTRUCTION_NONPASS --depth 2
./ice ontology trace claim:P55_RECONSTRUCTION_NONPASS_DOES_NOT_QUALIFY_PHASE56_OR_RECLASSIFY_PHASE53_OR_LICENSE_GLOBAL_PROMOTION --depth 2
./ice ontology trace open:p56-lambda-half-launch-residual-provenance-audit --depth 2
./ice ontology trace claim:P56_FRESH_PHASE53_ALGORITHM_CENTER_AND_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET --depth 2
./ice ontology trace claim:P56_FROZEN_FACTORIAL_GATE_PATTERN_ASSOCIATES_TARGET_RECOVERY_WITH_FRESH_CENTER --depth 2
./ice ontology trace claim:P56_BOUNDED_RECOVERY_DOES_NOT_AUTHORIZE_FULL_REPLAY_PHASE57_OR_GLOBAL_PROMOTION --depth 2
./ice ontology show policy:ragnarok-circuit-breaker
./ice ontology show policy:ordered-five-gate-advancement
./ice ontology trace open:gate5-persistent-order-and-pole-splitting --depth 5
```

Every command also accepts `--json`. Use `--graph hypercomplex`, `--graph legacy`, or `--graph cpt` to
restrict a query; `key::node-id` is the unambiguous qualified form. `guide --path` accepts the stable ID
with or without its `collection-path:`/`reading-path:` prefix. Cross-graph paths are navigation-only;
`trace` stays inside one graph while walking incoming and outgoing relations to the requested bounded
depth.

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
Phase 49 has no typed non-PASS record. Its all-control success is scoped to the declared 63-mantissa-bit
NumPy path, fixed roots and steps, and complex128 solver state. The Phase-48 failures remain valid and
form the negative half of the paired ablation. Phase 49 does not supply a formal error propagator,
portable long-double implementation, unique formula defect, or global topology.
Phase 50 also has no typed non-PASS record. Its six exact and eight numerical checks certify only the
declared common-ambient embedding, sampled stabilized saddle paths, two SPD metric paths, local
upward-nine-plane endpoint agreement, and the frozen reflection, tangent, mesh, reverse, stabilizer,
and basis controls. The artificial stabilizers and sampled meshes do not establish action nesting,
regulator independence, an unsampled no-zero theorem, a Gamma–K intersection, nonlinear upward manifold,
physical determinant line, cutoff limit, or global topology.
Phase 51 retains one typed numerical `INCONCLUSIVE` without invalidating its zero-exit run. The CSE and
non-CSE clongdouble same-point RHS relative gate reaches `1.690013e-8`, above its frozen `5e-10`
threshold, although the paired Hessian-action, endpoint-state, residual-difference, all sampled root,
reflection, derivative, tangent, mutation, and 68 action/first-cap-ledger controls pass. This supports
the fail-closed inconclusive classification boundary, not the desired continuation label, a code-defect
claim, root nonexistence, or contradiction. The narrow backend-consistency repair is open, as are the
Phase-50 Gamma–K continuation target, root/component/end census, cutoff question, and global topology.
Phase 52 retains one typed numerical `FAIL` as a non-invalidating negative control. Runtime traces of
the actual pinned Phase-51 callables reproduce 19 binary64 temporaries in both the m=4 and m=5 joint
CSE paths; the prior all-temporaries-clongdouble protocol validity is therefore not upheld even though
the historical bytes and emitted status remain unchanged. The element-local clongdouble candidate
passes all six static gradient/RHS comparisons, while the joint long-namespace candidate misses the RHS
threshold. This resolves `open:p51-cse-noncse-clongdouble-rhs-consistency` only on the frozen six static
slots. Phase 53 has now executed the full-path replay, so
`open:p53-full-repaired-phase51-continuation-rerun` was narrowed to its sole failed evaluator comparison.
The repaired evaluator passes its independent six-slot full-evaluator reference, but comparison with the
saved pinned Phase-51 global non-CSE numerical backend remains `INCONCLUSIVE`. Phase 54 resolves the
six-launch-state diagnostic narrowly: both global schedules fail and both element-local schedules pass,
so `open:p54-pinned-phase51-global-noncse-backend-diagnostic` is closed only for that static matrix.
Phase 55 then regenerates exactly three production and three candidate paths from explicitly labelled
P50-saddle-pinned launches. All paired trajectories pass, but the lambda-half production residual does
not reproduce the saved Phase-53 scalar under the unchanged reconstruction gate. Consequently
`open:p55-p53-trajectory-schedule-transfer-audit` resolves as reconstruction `NONPASS`, not schedule
qualification. Phase 56 resolves `open:p56-lambda-half-launch-residual-provenance-audit`: both
P50-center corners retain the residual-target NONPASS pattern while both fresh-center corners pass all
three gates under both solver profiles. This is a single-root factorial association, not a causal
theorem or exact historical launch identity. The Ragnarok policy consumes the terminal exception and
kills the reconciliation route; no full replay or Phase 57 is authorized, `next_phase` is null, straight
arms remain unsearched, and all global, physical, and TOE promotions remain barred. That killed-route
stop does not close distinct clean committed unnumbered calculations under the generic bounded runtime;
each such calculation is an independent unit and does not authorize an automatic descendant.

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
