# CPT × Temporal-Folded SUSY ontology guide

> This page is a human-readable memory and index generated from the current repository graph and evidence. It is **not** a preregistration, research contract, substitute for the calculations, scientific canon, or KG ratification.

Canonical machine record: [`graph.json`](./graph.json) (`research-graph/v1`, updated
`2026-08-28T01:51:25Z`; 976 nodes, 2929 edges). Run and analytic-evidence details live in the
[evidence guide](./references/evidence.md);
literature coverage lives in the [source inventory](./references/source-inventory.md). The validator
verifies 233/233 stored hashes (225 artifacts and 8 policies).

## Quick answers

| Question | Current scoped answer | Trace |
| --- | --- | --- |
| What happened between the collar calculation and Phase 16? | Phases 11–14A produced scoped exact collar, rigid-interface, formal-WKB and compact-T3 charge controls. Phase 15A is only an invalid sequencing receipt and licenses no science. Its independently frozen Phase 15R repair found one bosonic-only parent, but no full off-shell single parent, inside a two-source census. | `reading-path:collar-admissibility-to-single-source-parent-and-tangency`; `evidence:p15a-sequence-breach`; `evidence:p15r-run-result` |
| Did the bosonic parent work? | Yes, for the BGG `(X,T,Y)` velocity block after one endpoint removal. This does not include lapse or algebraic auxiliary constraints. | `claim:P16_BGG_BOSONIC_KINETIC_PARENT` |
| Did the specified strict off-shell FLRW truncation work? | No. Exact clean-point witnesses give nonzero discarded `b_i` and spin-3/2 normal components. | `claim:P16_SPECIFIED_OFF_SHELL_FLRW_GAMMA_TRACE_TANGENCY` |
| Does the scoped rolling clock preserve a nonzero SUSY parameter? | No on the declared `W=0`, `F=0`, nonzero-rate Lorentzian-real slice; the parameter map has rank two. This does not remove the underlying local gauge symmetry. | `claim:P16_ROLLING_CHIRAL_CLOCK_BACKGROUND_PRESERVED_SUSY` |
| Can standard support-local `Q` exchange bare `t<0` and `t>0` halves? | No. Both open-half cross blocks vanish by support locality. | `claim:P17_STANDARD_LOCAL_Q_HALF_EXCHANGE` |
| Does composing `Q` with `t→-t` fix that? | It gives a finite-fiber algebra witness, but on the unfolded line it is nonlocal and anticommutes with signed time momentum, so it is not a standard local conserved charge. | `claim:P17_REFLECTION_COMPOSED_Q_IS_STANDARD_LOCAL_CHARGE` |
| What is the most promising surviving route? | A **fundamental internal doubled sheet** admits bidirectional exchange algebra, and a separate doubled-real sheet-mixing projector exists. Their common action, domain, conserved charge, compatibility, positivity, and physical sheet anchor remain open. | `claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA`; `claim:P17_DOUBLED_REAL_SHEET_PROJECTOR_WITNESS` |
| Does one-way exchange close? | No under the standard physical adjoint. | `claim:P17_ONE_WAY_SHEET_ARROW_STANDARD_CLOSURE` |
| Does the superalgebra select a unique sheet basis? | No. A continuous unitary mixing family and parity-controlled basis equivalence remain. | `claim:P17_SUPERALGEBRA_SELECTS_SHEET_BASIS` |
| Does an ordinary real temporal seam preserve a nonzero SUSY subalgebra? | No in the single-copy real projector calculation; `v^0` vanishes only for the zero parameter. | `claim:P17_ORDINARY_REAL_TEMPORAL_SEAM_PRESERVES_SUSY` |
| Is physical time reversal itself the supercharge? | No in this analysis. Its anti-complex-linearity and grading make it a discrete operation, not the tested complex-linear fermionic `Q`. | `claim:P17_TIME_REVERSAL_IS_SUPERCHARGE` |
| What role remains for CPT/Pin? | CPT/Pin sewing is retained as a distinct bosonic discrete pairing or real structure between histories, not as the computed supercharge claim. | `concept:cpt-pin-sewing` |
| Is Schwinger–Keldysh BRST particle supersymmetry? | No. The checked quartet is cohomological/ghost graded and is not a positive-energy particle-SUSY construction. | `claim:P17_SK_BRST_IS_PARTICLE_SUPERSYMMETRY` |
| Does elapsed time itself break supersymmetry? | No in the conserved-charge control. If `[H,Q]=0`, a state annihilated by `Q` stays in that kernel under time evolution. | `claim:P18_ELAPSED_TIME_ALONE_BREAKS_SUSY` |
| Can one free instantaneous canonical seam explain missing superpartner pole masses? | No in the frozen Phase 18 class. It can prepare a non-SUSY state, but the post-post retarded B/F poles remain degenerate, and a sharp local kick has divergent energy density. | `claim:P18_FREE_CANONICAL_SEAM_GENERATES_POLE_SPLITTING`; `claim:P18_FREE_SEAM_CAN_PREPARE_NONSUSY_STATE`; `claim:P18_SHARP_SEAM_IS_UV_ADMISSIBLE` |
| Do the displayed closed SUGRA models admit 50–60 accelerated e-folds? | Yes conditionally. Six homogeneous (k=+1) target-shot backgrounds pass the exact turning-point and numerical constraint checks. | `claim:P19_DISPLAYED_TARGET_SHOT_BOUNCES_REACH_50_55_60_NACC` |
| Does time symmetry now predict \(\phi_0\), universe size, or a present SUSY spectrum? | No. The bosonic symmetry data leave \(\phi_0\) free, the radius is conditional, and the displayed stabilizer F directions vanish at their endpoints. | `claim:P19_BOSONIC_TIME_REFLECTION_DATA_LEAVE_PHI0_FREE`; `claim:P19_DISPLAYED_STABILIZER_F_DIRECTIONS_VANISH_AT_ENDPOINT` |
| Does the leading two-sheet WDW control select \(\phi_0=5.442969\)? | No in the constant-field de Sitter envelope. The standard \(e^{2sI}\) history weight and conditional independent-pair \(e^{4sI}\) joint probability are monotone there. This is not an exact two-sheet SUGRA WDW no-go. | `claim:P20_LEADING_DE_SITTER_WDW_ENVELOPE_SELECTS_5P44`; `claim:P20_INDEPENDENT_PAIR_WEIGHT_FOLLOWS_FROM_CPT_SEWING` |
| Is the displayed \(\Omega_{K0}\)–\(T_{\rm reh}\) value a seam prediction? | No. The conversion is reproducible only after fixing the Phase 19 branch, reheating history, units, entropy data, and late-time parameters. | `claim:P20_CONDITIONAL_CURVATURE_REHEATING_CONVERSION_IS_REPRODUCIBLE`; `claim:P20_CURVATURE_REHEATING_NUMBER_IS_A_SEAM_PREDICTION` |
| Does Gaussian normalization automatically give the physical flux probability? | No. It fixes the no-seam baseline at one. A chosen exclusion gives \(R-1\), while \(\log R\) is connected; the physical sector measure and decoherence rule remain open. | `claim:P21_NORMALIZATION_FORCES_ZERO_BRIDGE_SUBTRACTION`; `claim:P21_LOG_R_IS_CONNECTED_VACUUM_GENERATOR`; `claim:P21_R_MINUS_ONE_ALONE_FIXES_PHYSICAL_FLUX_PROBABILITY` |
| Does a positive finite-mode seam density exist? | Yes for one free SUSY oscillator with \(\omega,\beta>0\). The exact purification is normalized and positive, its reduced Gibbs density commutes with the fixed-mode charges, and it passes the equal-source SK trace identity. This is not an unbroken thermal vacuum or a 4D Pin/SUGRA state. | `claim:P22_POSITIVE_FREQUENCY_TFD_LIKE_DENSITY_IS_NORMALIZED_AND_POSITIVE`; `claim:P22_REDUCED_GIBBS_DENSITY_COMMUTES_WITH_FIXED_MODE_SUPERCHARGES`; `claim:P22_FINITE_DENSITY_SATISFIES_EQUAL_SOURCE_SK_NORMALIZATION` |
| Does the same free Gaussian normalize the homogeneous mode? | No in the noncompact \(L^2(\mathbb R)\), \(\omega\to0^+\) limit: the bosonic partition and covariance diverge while the stiffness vanishes. Compact or interacting constrained inflaton modes are not decided. | `claim:P22_FREE_NONCOMPACT_ZERO_MODE_HAS_TRACE_CLASS_TFD_LIMIT` |
| Does the Phase 23 constraint alone determine a physical cosmological seam density? | No. Full-lapse averaging gives a distributional rigging map, an explicit clock and frequency orientation give a positive integrated norm, and only a separately supplied compact bridge gives the regulated trace-class density. CPT-like reality and zero signed current do not select its weights; the quadratic zero root is singular and the massless decompactification limit is not trace class. | `claim:P23_FULL_REAL_LAPSE_AVERAGE_DEFINES_DISTRIBUTIONAL_RIGGING_MAP`; `claim:P23_EXPLICIT_CLOCK_AND_POSITIVE_FREQUENCY_GIVE_POSITIVE_INTEGRATED_NORM`; `claim:P23_CPT_REALITY_AND_ZERO_SIGNED_CURRENT_UNIQUELY_SELECT_A_DENSITY`; `claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY`; `claim:P23_REGULATED_DENSITY_HAS_TRACE_CLASS_DECOMPACTIFICATION_LIMIT` |
| Does the Phase 24 connected interval already define a physical entangled seam density? | No. The supplied real saddle has a nonzero cross-boundary response and one constraint-preserving mixed direction. A fixed-scale scalar subblock gives a conditional positive Gaussian, but the full real boundary Hessian and real-contour scalar Schur complement are indefinite; no gravitational thimble, physical boundary measure, trace-class density, or entropy has been constructed. | `claim:P24_CONNECTED_PRINCIPAL_FUNCTION_HAS_NONZERO_CROSS_BOUNDARY_RESPONSE`; `claim:P24_CONSTRAINT_PRESERVING_MIXED_HESSIAN_HAS_RANK_ONE`; `claim:P24_FIXED_SCALE_SCALAR_SUBBLOCK_DEFINES_A_CONDITIONAL_POSITIVE_GAUSSIAN`; `claim:P24_REAL_BOUNDARY_HESSIAN_DEFINES_A_POSITIVE_NORMALIZABLE_GAUSSIAN_PRECISION` |
| Do Phases 25–28 determine the physical gravitational thimble coefficient? | No. They establish a stationary fixed-boundary lapse saddle, a bounded long constant-phase arm, one real Airy fold, raw zero-lapse endpoint scaling, bounded constructed crossings, and a reduced homogeneous BFV diagnostic. The original-cycle relative homology, endpoint-completed kernel, and full determinant remain open. | `claim:P25_FROZEN_BOUNDARY_HAS_STATIONARY_LAPSE_SADDLE`; `claim:P26_LONG_CONSTANT_PHASE_ARM_EXISTS_ON_RECORDED_SHEET`; `claim:P27_EQUAL_BOUNDARY_RAW_FIXED_T_KERNEL_IS_FINITE_AT_ZERO_LAPSE`; `claim:P28_BOUNDED_VERTICAL_CYCLES_CROSS_RECORDED_DUAL_BRANCH` |
| Does the Phase 28 BFV/string route already explain missing superpartners? | No. The homogeneous Dirichlet ghost does not remove the proper-length modulus, the local lapse factor is conditional, and the string/three-form material is a completion design gate. No seam-selected sector rule, persistent F-type order parameter, soft spectrum, or physical state is derived; D-type breaking would need a separate vector/gauging sector. | `claim:P28_DIRICHLET_BFV_GHOST_REMOVES_PROPER_LENGTH_ZERO_MODE`; `claim:P28_LOCAL_LAPSE_GAUSSIAN_FACTOR_IS_CONDITIONAL`; `open:p28-string-three-form-soft-spectrum` |
| Does Phase 29 remove the zero-lapse pole or produce a physical state? | No. The normalized frozen leading real-lapse kernel still has a pointwise `1/N` pole but converges to a `delta_flat` identity distribution under the declared local `da dphi` measure. The reduced BFV modulus factor is T-independent; the physical WDW measure, conformal contour, all-orders kernel, full determinant, state, and global PL coefficient remain open. | `claim:P29_FROZEN_QUADRATIC_KERNEL_HAS_DELTA_FLAT_IDENTITY_LIMIT`; `claim:P29_EQUAL_ENDPOINT_POINTWISE_ZERO_LAPSE_LIMIT_IS_FINITE`; `claim:P29_FIXED_PARAMETER_BFV_MODULUS_FACTOR_IS_T_INDEPENDENT`; `claim:P29_DISTRIBUTIONAL_IDENTITY_IS_TRACE_CLASS_DENSITY` |
| Does Phase 30 finish the conformal thimble or BFV determinant? | No. It supports a finite-cutoff local field–lapse **coupled** Gaussian cycle and records a declared-measure relative magnitude. The tested independent product rotation fails; cutoff parity obstructs a bare absolute determinant sign; one holomorphic lapse sheet cannot normalize both real sides. No full BFV super-Hessian, determinant-line phase, global integer PL coefficient, or physical state was computed. | `claim:P30_FINITE_CUTOFF_LOCAL_COUPLED_FIELD_LAPSE_CYCLE_EXISTS`; `claim:P30_TESTED_STANDARD_PRODUCT_ROTATION_IS_SUFFICIENT`; `claim:P30_DECLARED_MIDPOINT_RELATIVE_MAGNITUDE_HAS_RECORDED_LIMIT`; `claim:P30_BARE_ABSOLUTE_LATTICE_SIGN_IS_CUTOFF_INDEPENDENT`; `claim:P30_ONE_HOLOMORPHIC_LAPSE_SHEET_NORMALIZES_BOTH_REAL_SIDES` |
| Does Phase 31 provide the physical BFV determinant or a SUSY/SUGRA Hessian? | No. Exact momentum elimination reproduces the Phase-30 configuration Hessian, the unreduced canonical sign is stable, and nonzero homogeneous quartets cancel only in a same-regulator relative normalization. The bare bosonic BFV sign still alternates, and “super-Hessian” here is BFV grading rather than a local-SUSY fluctuation operator. | `claim:P31_PHASE30_CONFIGURATION_HESSIAN_IS_CANONICAL_MOMENTUM_SCHUR_COMPLEMENT`; `claim:P31_PROPER_TIME_CANONICAL_DETERMINANT_SIGN_IS_STABLE`; `claim:P31_NONZERO_BFV_QUARTETS_CANCEL_IN_SAME_REGULATOR_RELATIVE_NORMALIZATION`; `claim:P31_FULL_BOSONIC_BFV_SIGN_EQUALS_CANONICAL_DETERMINANT_LINE` |
| Does Phase 32 fix the signed local or global connected-saddle PL coefficient? | No. A separately specified below-origin full real lapse contour has one recorded finite-radius **projected lapse-base crossing**; its coordinate sign is `+1` only under declared orientation conventions. The positive half-line has endpoint contact. The signed full-joint local intersection, continuous-arc proof, complete dual census, determinant-line trivialization, CPT/Pin contour selection, global coefficient, and state remain open. | `claim:P32_SPECIFIED_BELOW_ORIGIN_FULL_LINE_HAS_RECORDED_PROJECTED_BASE_CROSSING`; `claim:P32_POSITIVE_HALF_LINE_HAS_ORDINARY_TRANSVERSE_INTERSECTION`; `claim:P32_ABOVE_ORIGIN_FULL_LINE_HAS_SAME_POSITIVE_DUAL_INTERSECTION`; `open:p28-global-relative-homology-and-intersection`; `open:p32-cpt-pin-lapse-class-selection` |
| Does Phase 33 complete the uniform fold kernel or fix the global connected-saddle coefficient? | No. It confirms a transverse simple Dirichlet fold, its two-branch Airy action scale, and a regular rank-two local Ai/Bi space despite divergent separate Van Vleck terms. The fold is not a lapse saddle and its local chart adds no Phase-32 crossing. The contour/Stokes multiplier, analytic amplitude, determinant line, full dual census, global `n_sigma`, and physical state remain open. | `claim:P33_RECORDED_DIRICHLET_CAUSTIC_HAS_SIMPLE_FOLD_AIRY_SCALE`; `claim:P33_RECORDED_DIRICHLET_FOLD_IS_ADDITIONAL_LAPSE_SADDLE`; `claim:P33_SEPARATE_VAN_VLECK_DIVERGENCE_FORCES_EXACT_KERNEL_DIVERGENCE`; `claim:P33_LOCAL_AIRY_REGULARITY_UNIQUELY_SELECTS_UNIFORM_KERNEL`; `claim:P33_LOCAL_FOLD_PATCH_ADDS_PHASE32_LAPSE_INTERSECTION` |
| Does Phase 34 transport the incoming cycle through the fold or fix the global coefficient? | No. It records 47 incoming real points directed toward the fold and separately constructs a conjugate pair of reduced constant-phase branches beyond it through `Re T=13`. It does not decide which outgoing arm, if either, carries the incoming cycle. The Airy connection, determinant line, full joint field–lapse flow, complete sheet/end census, global `n_sigma`, and state remain open. | `claim:P34_RECORDED_INCOMING_REAL_SEGMENT_IS_DIRECTED_TOWARD_FOLD`; `claim:P34_BOUNDED_DIRECTED_CONSTANT_PHASE_PAIR_EXISTS_BEYOND_FOLD`; `open:p34-full-joint-dual-determinant-and-global-census` |
| Does Phase 35 provide the physical Van Vleck determinant or fix the Maslov phase and global coefficient? | No. It transports the declared endpoint-Jacobi `det B_v` section relatively on the sampled Phase-34 table, records finite-resolution consistency with the oriented near-fold square-root law, and finds conjugate reduced endpoint phases cancel. The sampled data are insufficient to fix an absolute orientation. A zero-free continuum lift, the physical block and measure, absolute sign/Maslov orientation, incoming-to-outgoing connection, full BFV/SUGRA superdeterminant, all sheets and good ends, global `n_sigma`, and state remain open. | `claim:P35_TRACKED_REDUCED_ENDPOINT_DETERMINANT_LINE_IS_TRANSPORTABLE`; `claim:P35_RECORDED_UPPER_NEAR_FOLD_PHASE_IS_CONSISTENT_WITH_MINUS_PI_OVER_2`; `claim:P35_CONJUGATE_REDUCED_BOSONIC_ENDPOINT_PHASES_CANCEL_RELATIVELY`; `claim:P35_RELATIVE_ENDPOINT_TRANSPORT_FIXES_ABSOLUTE_MASLOV_ORIENTATION`; `open:p35-absolute-detline-full-bfv-and-global-cycle` |
| Does Phase 36 transport one physical upward cycle through the fold or select an outgoing arm? | No. It fixes exact identities only in separately ordered CW and CCW Airy bases. Their first duals use different companion cycles, while the numerical calculation tracks BVP root sheets rather than the formal upward cycles. Both root-sheet laterals pass sampled gates on three finite radii, so Phase 32 plus Phase 35 is insufficient by itself within those local gates. A complete original cycle may still select one arm globally. | `claim:P36_EXACT_LOCAL_AIRY_GAUSS_MANIN_CONNECTION_IS_FIXED`; `claim:P36_TRACKED_AI_ROOT_HAS_REGULAR_CW_U_AND_CCW_L_CONTINUATIONS`; `claim:P36_PHASE32_PLUS_PHASE35_UNIQUELY_SELECTS_ONE_OUTGOING_FOLD_ARM`; `open:p36-original-cycle-hard-determinant-and-global-bfv-state` |
| Does Phase 37 make the local sheet exchange physical or establish a Pin/Pfaffian supercharge holonomy? | No. Both tracked BVP roots exchange on three finite enclosing loops, and the sampled reduced bosonic half-form has a conditional order-four conjugacy class with \(L^2=-I\). Bare root monodromy still preserves the Phase-17 parity-controlled basis equivalence. No original relative cycle, hard CFU coefficients, spacetime Pin lift, fermion Pfaffian line, full BFV/SUGRA operator, conserved spinorial charge, quantum constraint, or state is computed. | `claim:P37_LOCAL_BVP_ROOT_COVER_HAS_NONTRIVIAL_Z2_MONODROMY`; `claim:P37_SAMPLED_REDUCED_HALF_FORM_HAS_CONDITIONAL_ORDER_FOUR_HOLONOMY`; `claim:P37_ROOT_MONODROMY_ALONE_BREAKS_PHASE17_BASIS_EQUIVALENCE`; `open:p37-global-cycle-hard-cfu-full-bfv-pfaffian-gate` |
| Does Phase 38 close Gate 1 or determine the global signed intersection vector? | No. It supports that the recorded projected/local data do not license inverse reconstruction without a physical injectivity theorem or admissible completions; its noninjective example is only a finite surrogate, not a physical relative-homology theorem. The conditional \(\Gamma_0\) local map is exact, and one tracked branch plus its conjugation control remains disjoint at sampled points through \(\operatorname{Re}T=16\), but no continuous census, complete joint cycle, full-joint sign, good-end classification, or global vector is obtained. Gate-2 hard-CFU work may run in parallel; only its physical promotion depends on Gate 1. | `claim:P38_RECORDED_DATA_DO_NOT_LICENSE_INVERSE_JOINT_CYCLE_RECONSTRUCTION`; `claim:P38_ROOT_SWAP_CAN_REPLACE_GAUSS_MANIN_CYCLE_TRANSPORT`; `claim:P38_CONDITIONAL_GAMMA0_INPUT_MAPS_TO_BOTH_LOCAL_ARMS`; `claim:P38_SAMPLED_TRACKED_ARMS_REMAIN_PROJECTED_DISJOINT_THROUGH_RET16`; `claim:P38_BOUNDED_LEDGER_SUFFICES_TO_FIX_GLOBAL_INTERSECTION_VECTOR`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 39 directly compute a full-joint intersection sign and close Gate 1? | It directly computes two **local** six-real-dimensional signs: for one frozen \(m=2\) configuration action and one finite-radius, finite-time upward-chart patch, a numerically locally transverse candidate on each declared cap piece has configuration-coordinate sign `+1`. This no longer infers the sign from the lapse projection. It does not pair the entire bounded chain: straight arms and later cap reintersections are unsearched, root/upward-component exhaustion and the exact nonlinear upward manifold are uncertified, all recorded real saddles are critical-phase degenerate without a certified lateral chamber, and the good ends are incomplete. Thus `bounded_chain_signed_sum`, the complete vector, and `global_n_sigma` remain null; Gate 1 stays open. | `claim:P39_FROZEN_M2_ACTION_HAS_GENUINE_POSITIVE_T_DISCRETE_JOINT_SADDLE`; `claim:P39_DECLARED_M2_CAP_PIECES_HAVE_LOCAL_SIX_REAL_PLUS_ONE_CANDIDATES_ON_ONE_FROZEN_K_PATCH`; `claim:P39_TWO_FROZEN_CAP_LOCAL_CANDIDATES_SUFFICE_TO_FIX_GLOBAL_INTERSECTION_VECTOR`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 40 establish an odd history sector or close Gate 1 at \(m=3\)? | It supports a nonzero anchor-subtracted, sign-reversing response of the first two-dimensional reflection-odd \((a,\phi)\) block to one rank-one antisymmetric **phi-only** endpoint source. It also records five sampled local full-\(\mathbb R^{10}\) candidates with direct declared signs `+1`, using one fixed delta-zero flow mobility and delta-dependent local Morse launch ellipsoids. The source does not probe the full odd sector; the five samples are not a continuous branch theorem; and the local K-launch clamp is neither a full odd-sector ablation nor a no-root result. All chain/global outputs remain null, meaning uncomputed rather than zero, and Gate 1 stays open. | `claim:P40_RANK_ONE_PHI_SOURCE_HAS_ANCHOR_SUBTRACTED_SIGN_REVERSING_ODD_RESPONSE`; `claim:P40_FIVE_SAMPLED_M3_CAP_CANDIDATES_HAVE_LOCAL_FULL_R10_SIGN_PLUS_ONE`; `claim:P40_RECORDED_LOCAL_M3_DATA_DO_NOT_LICENSE_BOUNDED_CHAIN_OR_GLOBAL_INTERSECTION_INFERENCE`; `concept:fixed-flow-mobility-versus-delta-dependent-morse-launch-ellipsoid`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 41 establish robust m=4 source branches, cutoff convergence, or close Gate 1? | No. It supports stable numerical rank two for the two-source odd susceptibility in one frozen normalization and resolves five local full-\(\mathbb R^{14}\) candidates with direct declared sign `+1`. The frozen `u2` finite-difference plateau fails at all three audited points, so phi-only and a-only robustness remain inconclusive even though the roots and other controls are retained. The m3/m4 signs are only separately audited descriptive data; no common determinant line, cutoff limit, chain sum, global vector, or quantum-gravity result follows. | `claim:P41_TWO_SOURCE_ODD_SUSCEPTIBILITY_HAS_STABLE_NUMERICAL_RANK_TWO`; `claim:P41_FIVE_PRIMARY_M4_CAP_CANDIDATES_HAVE_LOCAL_FULL_R14_SIGN_PLUS_ONE`; `claim:P41_RETAINED_TANGENT_CONTROL_FAILURE_LEAVES_BOTH_SOURCE_ROBUSTNESS_CLAIMS_INCONCLUSIVE`; `claim:P41_RECORDED_LOCAL_M4_DATA_DO_NOT_LICENSE_CANONICAL_CROSS_CUTOFF_OR_GLOBAL_INTERSECTION_INFERENCE`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 42 repair the tangent or prove a variational code bug? | No. It supports solver-noise and old-step-pair evidence at `phi_plus` and `a_plus`, and separately supports a protocol-defined local Hessian-action identity anomaly at all three fixed roots. The time-column discrepancy is an endpoint solver/state comparison, not independent bug evidence. A sufficient normalized local matrix homotopy preserves sign `-1`, but the `shared_zero` `u2` reference is not stable under its frozen neighbor rule, so the reference tangent remains inconclusive. Phase 41 stays 8/9, all global outputs remain fail-closed, and Gate 1 stays open. | `claim:P42_SOLVER_NOISE_AND_FROZEN_STEP_PAIR_ARTIFACT_SUPPORTED_AT_PHI_AND_A`; `claim:P42_LOCAL_HESSIAN_ACTION_IDENTITY_ANOMALY_IS_SUPPORTED_WITHOUT_PROVING_A_BUG`; `claim:P42_NORMALIZED_LOCAL_MATRIX_HOMOTOPY_SUFFICIENTLY_PRESERVES_FIXED_ROOT_SIGN`; `claim:P42_REFERENCE_TANGENT_REMAINS_INCONCLUSIVE_AND_GLOBAL_PROMOTION_IS_PROHIBITED`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 43 prove one local code bug, repair the integrated tangent, or close Gate 1? | No. It corroborates an independent high-precision local reference at all 90 frozen slots. The byte-pinned NumPy64 Hessian action crosses the frozen tolerance at 13 slots, but that operational mismatch does not identify a wrong formula or unique defect. Same-step binary64 finite-difference evidence is supported at 28/33 disclosed anomalies, while five complete exceptions contradict the frozen all-33 claim. No root, ODE, integrated tangent, time column, orientation, or global cycle is tested; Phase 41 stays 8/9, the Phase-42 reference remains inconclusive, and Gate 1 stays open. | `claim:P43_INDEPENDENT_HIGH_PRECISION_LOCAL_REFERENCE_IS_CORROBORATED_AT_ALL_FROZEN_SLOTS`; `claim:P43_NUMPY64_LOCAL_RHS_OUTPUT_MISMATCH_IS_SUPPORTED_WITHOUT_PROVING_A_CODE_DEFECT`; `claim:P43_DOUBLE_PRECISION_FD_ARTIFACT_EXPLAINS_ALL_33_PHASE42_ANOMALIES`; `claim:P43_LOCAL_ARBITRATION_DOES_NOT_TEST_INTEGRATED_TANGENT_OR_LICENSE_GLOBAL_PROMOTION`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 44 identify a wrong formula or one rounding cause, repair the tangent, or close Gate 1? | No. The declared source and independent action, gradient, and Hessian formulas are exactly identical componentwise. All 90 signed arithmetic telescopes close, and one fixed forward-error model covers all 13 disclosed mismatches and all 77 controls. Coefficient, state, Hessian, and contraction contributions are mixed, nonexclusive, and potentially cancelling in both cohorts, so no unique stage or defect is selected. No root, ODE, integrated tangent, time column, orientation, determinant line, or global cycle is tested; the Phase-43 label is preserved and Gate 1 remains `OPEN_PARTIAL_PROGRESS`. | `claim:P44_DECLARED_SOURCE_FORMULA_IS_EXACTLY_IDENTICAL_TO_THE_INDEPENDENT_MODEL`; `claim:P44_ALL_DISCLOSED_NUMPY64_MISMATCHES_FIT_THE_DECLARED_MIXED_FORWARD_ERROR_MODEL`; `claim:P44_LOCAL_ARITHMETIC_DECOMPOSITION_DOES_NOT_REPAIR_THE_TANGENT_OR_LICENSE_GLOBAL_PROMOTION`; `open:gate1-original-cycle-signed-global-intersections` |
| Does Phase 45 repair the Phase-41 tangent control by replacing the local tangent RHS? | No. The independent 50/80-digit tangent paths are stable and agree with the source tangent and root Jacobian at the `1e-12` scale, while the historical `u2` plateaus remain failed. Phase 45 narrows the issue to the state-map finite-difference layer without recomputing it or closing Gate 1. | `claim:P45_INDEPENDENT_INTEGRATED_TANGENT_IS_PRECISION_STABLE_AT_THREE_FIXED_ROOTS`; `claim:P45_SOURCE_TANGENT_AND_ROOT_JACOBIAN_AGREE_WITH_INDEPENDENT_REFERENCE`; `claim:P45_TANGENT_CONTROL_FAILURE_IS_STABLE_TO_LOCAL_RHS_REPLACEMENT`; `claim:P45_LOCAL_STABILITY_DOES_NOT_LICENSE_GLOBAL_PROMOTION` |
| Does Phase 46 repair the failed `u2` state-map ladder or prove a source formula bug? | It repairs the ladder under the frozen independent local-flow comparison, but does not prove a formula bug. Independent plateaus are at most `2.019e-7` and agree with Phase-45 tangents; close source endpoints amplify into tight/Radau derivative-column failures. The mixed source arithmetic, solver accumulation, and subtraction budget remains open, Phase 41 stays 8/9 as provenance, and Gate 1 stays open. | `claim:P46_INDEPENDENT_STATE_MAP_U2_LADDER_IS_STABLE_AND_AGREES_WITH_TANGENT`; `claim:P46_LOCAL_FLOW_RHS_REPAIR_IS_SUPPORTED_UNDER_FIXED_PROJECTION`; `claim:P46_LOCAL_REPAIR_DOES_NOT_PROVE_SOURCE_FORMULA_DEFECT_OR_LICENSE_GLOBAL_PROMOTION`; `open:p46-source-gradient-flow-error-budget` |
| Does Phase 47 prove that changing only the generated gradient fixes the integrated paths? | No. It closes the declared mixed-arithmetic telescope at all 36 retained launch/endpoint states and all 18 paired derivatives, and generated gradient evaluation has the largest stage norm in every slot. That prioritizes a gradient-only hybrid test but does not select one unique suboperation, integrate a repaired path, sample the interior, or bound endpoint/solver accumulation. Phase 41 remains 8/9; Phases 44 and 46 are unchanged; Gate 1 stays open. | `claim:P47_LOCAL_SOURCE_FLOW_TELESCOPES_CLOSE_AT_ALL_RETAINED_SLOTS`; `claim:P47_GENERATED_GRADIENT_EVALUATION_IS_LARGEST_RETAINED_MIXED_ARITHMETIC_STAGE`; `claim:P47_LOCAL_BUDGET_DOES_NOT_BOUND_ENDPOINT_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION`; `open:p46-source-gradient-flow-error-budget`; `open:p48-gradient-hybrid-error-transport-control` |
| Does Phase 48's gradient-only clongdouble adapter repair the full `u2` ladder? | No. All eighteen paths, ninety intermediate local-flow probes, and endpoint-state limits pass on the pinned platform, but only `a_plus` has a stable full ladder and every root fails the all-step `0.005` derivative limits against both the Phase-46 independent columns and Phase-45 tangents. This is a useful negative control: promoting only the generated gradient materially improves the paths but is not sufficient. The propagation/solver budget and Gate 1 remain open. | `claim:P48_GRADIENT_ONLY_CLONGDOUBLE_PATHS_MATCH_LOCAL_FLOW_AND_ENDPOINT_LIMITS`; `claim:P48_GRADIENT_ONLY_CLONGDOUBLE_REPAIRS_THE_FULL_U2_LADDER`; `claim:P48_PLATFORM_ABLATION_DOES_NOT_CLOSE_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION`; `open:p46-source-gradient-flow-error-budget`; `open:p48-gradient-hybrid-error-transport-control` |
| Does Phase 49 repair the frozen `u2` ladder with a practical NumPy implementation? | Yes within the pinned long-double platform contract. Retaining clongdouble through state formation, generated gradient, `L.T` contraction, and outer minus-conjugation before one complete-flow complex128 projection makes all eighteen paths, ninety probes, endpoint states, full ladders, independent columns, and tangent comparisons pass. The worst derivative discrepancy is `0.001216`, below `0.005`. This resolves the scoped implementation choice, not formal endpoint transport, portability, a formula defect, or Gate 1. | `claim:P49_FULL_FLOW_CLONGDOUBLE_PASSES_ALL_FROZEN_STATE_MAP_CONTROLS`; `claim:P49_PHASE48_49_ABLATION_SUPPORTS_LATE_COMPLETE_FLOW_PROJECTION`; `claim:P49_SCOPED_REPAIR_DOES_NOT_PROVE_PORTABILITY_OR_LICENSE_GLOBAL_PROMOTION`; `open:p49-formal-endpoint-transport-and-portable-flow-adapter` |
| Does Phase 50 establish a cutoff-stable \(m=4\to m=5\) cycle transport? | No. It supports one explicitly stabilized, sampled common-ambient route for five frozen source-labelled saddles and their local upward nine-planes. All fine/coarse/reverse, tangent, reflection, metric-path, stabilizer, and basis controls pass, with no sampled Hessian zero or inertia change. The action bridge is not an exact nesting, and no Phase-41 Gamma–K intersection, nonlinear upward manifold, physical determinant line, cutoff limit, global cycle, or physics result is continued. | `claim:P50_FIVE_FROZEN_M4_SADDLES_CONTINUE_TO_M5_ON_DECLARED_STABILIZED_PATHS`; `claim:P50_LOCAL_UPWARD_NINE_PLANE_TRANSPORT_HAS_CONSISTENT_ORIENTED_ENDPOINT`; `claim:P50_SAMPLED_LOCAL_TRANSPORT_DOES_NOT_ESTABLISH_CUTOFF_STABILITY_OR_GLOBAL_INTERSECTION`; `open:p50-frozen-m5-gamma-k-local-intersection-continuation` |
| Does Phase 51 support the frozen phi-plus \(m=5\) Gamma–K continuation? | Not yet. The run is valid and all 17/9/17 phi-plus path nodes, 17 independent phi-minus reflection nodes, three full-J controls, the path tangent, four endpoint mutations, and 68 action/first-cap ledgers pass. But the frozen CSE/non-CSE RHS relative gate reaches `1.690e-8` against `5e-10`, so the only licensed local label is `INCONCLUSIVE`. This is not no-root or contradicted, and it does not resolve the Phase-50 open problem or establish a global intersection. | `claim:P51_FROZEN_PHI_PLUS_GAMMA_K_CONTINUATION_REMAINS_INCONCLUSIVE_AT_CSE_NONCSE_RHS_GATE`; `claim:P51_LOCAL_GAMMA_K_RUN_DOES_NOT_ESTABLISH_ROOT_EXHAUSTION_OR_GLOBAL_INTERSECTION`; `open:p51-cse-noncse-clongdouble-rhs-consistency` |
| Does Phase 52 repair the evaluator and support the Phase-51 continuation? | It resolves only the static evaluator layer. The actual Phase-51 m=4 and m=5 joint CSE callables each execute 19 hidden binary64 temporaries. The element-local clongdouble candidate passes all six frozen gradient/RHS comparisons (`7.051e-11`/`1.567e-10` maxima below `5e-10`); the joint long-namespace candidate remains a declared accuracy negative control. Phase 52 itself ran no repaired root or flow path and did not reclassify Phase 51. Phase 53 has since executed the full replay and is indexed in the next row. | `claim:P52_PHASE51_HIDDEN_BINARY64_CSE_CONTRACT_VIOLATION_IS_REPRODUCED`; `claim:P52_ELEMENT_LOCAL_CLONGDOUBLE_RHS_REPAIR_IS_SUPPORTED_ON_SIX_STATIC_SLOTS`; `claim:P52_STATIC_REPAIR_DOES_NOT_RATIFY_PHASE51_CONTINUATION_OR_GLOBAL_INTERSECTION`; `open:p53-full-repaired-phase51-continuation-rerun` |
| Does Phase 53 support the repaired phi-plus continuation or establish a global intersection? | No. The complete replay is a `VALID_RUN`: 8/8 exact and 10/11 numerical gates pass, including 68 accepted roots, 146 retained integrations, all 68 action/first-cap ledgers, and an independent six-slot 80/120-decimal full-evaluator reference with 54 canonical Hessian probes. The sole inherited comparison to the saved pinned Phase-51 global non-CSE numerical backend remains `INCONCLUSIVE` (`6.645e-9` versus `5e-10`). Straight arms were not searched and every global, cutoff, continuum, physics, and TOE output remains null. | `claim:P53_REPAIRED_REPLAY_PASSES_INDEPENDENT_REFERENCE_AND_NONBACKEND_CONTROLS`; `claim:P53_FULL_REPLAY_REMAINS_INCONCLUSIVE_AT_PINNED_PHASE51_GLOBAL_NONCSE_BACKEND`; `claim:P53_VALID_LOCAL_REPLAY_DOES_NOT_LICENSE_STRAIGHT_ARM_OR_GLOBAL_PROMOTION`; `open:p54-pinned-phase51-global-noncse-backend-diagnostic` |
| What did Phase 54 resolve about that backend discrepancy? | On the exact six launch states, both global schedules miss the `5e-10` selector while both element-local schedules pass all 12 selector records. Long arithmetic alone is insufficient; the tested element-local schedule is sufficient on this finite matrix. No trajectory was run, Phase 51 and Phase 53 remain unchanged, and every global/physics/TOE output stays null. | `claim:P54_PHASE51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_IS_CONFIRMED_ON_SIX_STATIC_SLOTS`; `claim:P54_ELEMENT_LOCAL_SCHEDULE_ALONE_IS_SUFFICIENT_ON_SIX_STATIC_SLOTS`; `claim:P54_STATIC_ARITHMETIC_ATTRIBUTION_DOES_NOT_RECLASSIFY_PHASE51_OR_PHASE53_OR_LICENSE_GLOBAL_PROMOTION`; `open:p55-p53-trajectory-schedule-transfer-audit` |
| Did Phase 55 qualify the element-local schedule on reconstructed trajectories? | No. All six ODEs completed, all fifteen `EL_std`/`EL_long` trajectory pairs passed, and the Phase-54 aggregate schedule matrix was reproduced. However, the explicitly P50-saddle-pinned reconstruction at `lambda=0.5` gave an `EL_long` scaled residual of `2.675e-7`, above the unchanged `2e-7` prerequisite; its saved-scalar difference was `2.673e-7`. The valid run therefore stops at reconstruction `NONPASS`; Phase 56 separately diagnoses that miss without rewriting it. | `claim:P55_P50_SADDLE_PINNED_RECONSTRUCTION_MISSES_SAVED_PHASE53_RESIDUAL_AT_LAMBDA_HALF`; `claim:P55_ELEMENT_LOCAL_BACKEND_AGREEMENT_IS_DIAGNOSTIC_AFTER_RECONSTRUCTION_NONPASS`; `claim:P55_RECONSTRUCTION_NONPASS_DOES_NOT_QUALIFY_PHASE56_OR_RECLASSIFY_PHASE53_OR_LICENSE_GLOBAL_PROMOTION`; `open:p56-lambda-half-launch-residual-provenance-audit` |
| What did terminal Phase 56 recover, and does it authorize another phase? | At the single saved `phi_plus`, `lambda=0.5` root, both P50-center corners retain `[PASS, NONPASS, NONPASS]` while both fresh-center corners pass all three target gates under both frozen profiles. This supports a bounded association with the fresh center, not exact historical Phase-53 bytes or a general causal theorem. The one-shot closeout is consumed: route `KILL`, full replay and Phase 57 unauthorized, `next_phase=null`, Gate 1 open, and global promotion prohibited. | `claim:P56_FRESH_PHASE53_ALGORITHM_CENTER_AND_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET`; `claim:P56_FROZEN_FACTORIAL_GATE_PATTERN_ASSOCIATES_TARGET_RECOVERY_WITH_FRESH_CENTER`; `claim:P56_BOUNDED_RECOVERY_DOES_NOT_AUTHORIZE_FULL_REPLAY_PHASE57_OR_GLOBAL_PROMOTION`; `policy:ragnarok-circuit-breaker` |
| Did the straight-lift KILL eliminate every affine or curved field-end completion? | No. The executed case split exhausts the anchor-through homogeneous ansatz \(\delta=qy\). An execution-free exact derivation gives \(\delta=x+i\arg(T)/\kappa\) two uniform good ends, and the follow-up phase-band theorem shows that every continuous horizontal affine tail with a strictly positive full-rate coefficient and two good arm ends is contractible to it inside one principal fixed-\(a\) scalar-fiber class. This is not a full joint/original cycle; all joint and global obligations remain open or null. | `claim:G1_PHASE_LOCKED_AFFINE_PHI_FIBER_HAS_TWO_UNIFORM_GOOD_ENDS`; `claim:G1_ANCHORED_LINEAR_KILL_IS_NOT_AN_AFFINE_OR_CURVED_NO_GO`; `claim:G1_ROBUST_HORIZONTAL_AFFINE_PHI_TAILS_FORM_ONE_PRINCIPAL_REDUCED_CLASS`; `open:gate1-phase-locked-fiber-to-source-derived-joint-cycle` |
| Do good-end convergence or the bounded scalar source link uniquely select phase lock? | No. Exact positive-real cancellation uniquely picks \(b(\psi)=\psi/\kappa\), but convergence admits \(b_\lambda=\lambda\psi/\kappa\) for every \(0<\lambda<2\), all in the same reduced class. The consumed source-link one-shot supplies a path- and order-specified comparison for a **newly declared** fixed-\(a\), \(m=2\) scalar phase-space control: exact momentum elimination and full-action homotopy directly match the declared \(0<\lambda\le1\) \(\Gamma_\lambda\) representatives with scalar orientation `+1` on lapse tests supported away from \(N=0\). The later zero-lapse one-shot was `INVALID_RUN` at a SymPy structural-equality false negative and wrote no result, so it neither contradicts the square identity nor constructs the zero-including full \(q\)-paired distribution. The scoped reduced-class `KEEP` remains nonzero-arm only; \(\lambda=1\) and the physical original joint cycle remain unselected. | `claim:G1_EXACT_FULL_RATE_CANCELLATION_SELECTS_PRINCIPAL_PHASE_LOCK_REPRESENTATIVE`; `claim:G1_UNIFORM_GOODNESS_UNIQUELY_SELECTS_EXACT_PHASE_LOCK`; `claim:G1_DECLARED_SCALAR_SOURCE_LINK_MATCHES_ON_NONZERO_LAPSE_ARMS_WITH_ZERO_LAPSE_EXTENSION_OPEN`; `claim:G1_ZERO_LAPSE_ONE_SHOT_INVALID_AND_DOES_NOT_ESTABLISH_EXTENSION`; `claim:G1_CURRENT_RECORDS_DO_NOT_ESTABLISH_PHASE_LOCKED_JOINT_CYCLE` |
| Can one common lapse lateral make the unchanged real \(p_a,p_\phi\) source absolutely convergent? | No in the finite \(m=2\) control: \(N-i0\) damps the scalar block but grows the negative-kinetic scale block, and \(N+i0\) reverses them. Declared centered complex momentum rays exactly reproduce the fiberwise Gaussian pushforward, while the negative-arm \(-1\) comes from a standard-Fresnel frozen-\(A\) flat-tangent comparison. This does not derive source-to-thimble deformation, simultaneous nonlinear configuration admissibility, \(p_a\) gauge fixing, FP/BFV orientation, zero lapse or a physical original cycle. | `claim:G1_SINGLE_COMMON_LATERAL_ABSOLUTELY_DAMPS_UNCHANGED_REAL_PA_PPHI_AXES`; `claim:G1_DECLARED_COMPLEX_BOSONIC_MOMENTUM_RAYS_REPRODUCE_FINITE_M2_PUSHFORWARD`; `scope:gate1-m2-bosonic-nonzero-lapse-source-pushforward` |
| Does the homogeneous trace gauge remove the local negative momentum direction, and can it simply be appended to the old \(m=2\) source? | The first answer is locally yes away from the FP horizon \(a^2V=2\): \(Q=2\log a\), \(P_{\rm tr}=ap_a/2\) is canonical, and the constraint plus trace gauge reduces rather than merely deletes \(p_a\). The second answer is no: the inherited endpoint-preserving constant-lapse condition already fixes its sole nonzero lapse-gauge mode, the ordinary static trace representative has \(N=0\) where regular, and endpoint transversality changes the action/state problem. The formal lower-lateral scalar fiber remains convergent, but a replacement improved-static or time-dependent BFV source must be rederived. | `claim:G1_HOMOGENEOUS_TRACE_PAIR_GIVES_LOCAL_SIMPLE_ROOT_CONSTRAINT_REDUCTION`; `claim:G1_STATIC_TRACE_FP_GAUGE_CAN_BE_APPENDED_TO_UNCHANGED_PROPER_TIME_M2_SOURCE`; `claim:G1_LOCAL_TRACE_REDUCTION_LEAVES_LOWER_LATERAL_REAL_SCALAR_FIBER_CONVERGENT` |
| Did the first closed-FRW \(V=0\) follow-up construct that replacement endpoint problem? | It constructs one narrower piece: on the frozen \(p_\phi=+1\), \(0\le P\le1/2\), \(R>0\), \(D>0\) component, the weak relational coordinate \(\Phi_*\), on-shell potential \(B=P\), finite local static hit, local FP measure and time-dependent same-orbit control are mutually consistent. The KEEP is only the classical local fixed-\(\Phi_*\) action \(S_0-[P]\). The raw static action after endpoint flow, HTV improved-static action, and auxiliary fixed-\((P,\phi)\) action are separate ledgers. That result alone supplied no off-shell chart, quantum endpoint states, ghost/BFV replacement source, old fixed-\(a\) equality, full-real-lapse \(\delta(C)\) kernel, global cycle, physics or TOE. | `claim:G1_CLOSED_FRW_V0_TRACE_GAUGE_HAS_LOCAL_ON_SHELL_RELATIONAL_ENDPOINT_ACTION`; `scope:gate1-closed-frw-v0-local-on-shell-trace-endpoint-action`; `open:gate1-phase-locked-fiber-to-source-derived-joint-cycle` |
| Is that on-shell \(\Phi_*\) result now connected to an off-shell chart? | Yes, but only classically and componentwise. On \(\mathcal U_+=\{p>0,\,3p^2-2P^2>0\}\) and every real \(c=C\), the unique positive constraint root and \(W=-\int_0^P Q(c,u,p)du\) define the exact Darboux chart \((T,c,\Phi,p)=(W_c,C,\phi+W_p,p)\) onto its open image. Its boundary potential gives \(S_0-[B]\), and \(c=0\) recovers \(\Phi_*\) and \(B=P\). Other components, a global atlas, normalized quantum endpoints, ghost/BFV source, the Marolf \(\delta(C)\) kernel, old fixed-\(a\) equality, physical cycle, physics and TOE remain open or null. | `claim:G1_CLOSED_FRW_V0_P_POSITIVE_R_POSITIVE_COMPONENT_HAS_CLASSICAL_OFFSHELL_DARBOUX_CHART`; `scope:gate1-closed-frw-v0-p-positive-r-positive-componentwise-offshell-darboux-chart`; `evidence:gate1-v0-offshell-darboux-chart`; `open:gate1-phase-locked-fiber-to-source-derived-joint-cycle` |
| Does that Darboux chart now have a quantum endpoint transform? | It has one sharply limited quantum layer. On compact interiors of \(\mathcal U_+\), \(S=-W\) and \(D^{-1/2}\) define the old-\((P,p)\) to new-\((c,p)\) principal momentum-polarization FIO with a fixed local Maslov branch and exact \(c=0\) lineage. The uncorrected one-term kernel is not exactly unitary: in \(U_\hbar^*U_\hbar\), its endpoint geometric-mean density differs from the required secant/coarea density; on symmetric \(c=0\) pairs the ratio is strictly above one and starts as \(1+\delta P^2/(36p^2)\). This KILL is only for that one-term amplitude. A corrected full symbol or spectral transform is not excluded, while ordering, domains, global normalization, coordinate polarization, BFV, \(\delta(C)\), the physical cycle, physics and TOE remain open or null. | `claim:G1_CLOSED_FRW_V0_DARBOUX_GRAPH_ADMITS_LOCAL_PRINCIPAL_MOMENTUM_ENDPOINT_FIO`; `claim:G1_V0_UNCORRECTED_ONE_TERM_VAN_VLECK_KERNEL_IS_EXACTLY_UNITARY`; `scope:gate1-v0-compact-interior-principal-momentum-endpoint-fio`; `evidence:gate1-v0-principal-endpoint-fio`; `open:gate1-phase-locked-fiber-to-source-derived-joint-cycle` |
| How far does the \(\mathcal U_+\) spectral-to-\(m=2\) BFV chain go? | The improved-static source remains one local algebraic convention. A selected densitization \(H=12\pi^2e^{3Q/2}C\), flat ordering, and Fourier--Kontorovich--Lebedev construction give a \(p>0\) RAQ model with \(\kappa_0=\sqrt{3/2}\,p/\hbar\) and physical measure \(dp/(2\sqrt6\hbar p)\); it is not the prior static \(dp\) fiber measure. A cutoff boundary control excludes a nonzero-edge witness by positive logarithmic divergence, admits \(p e^{-p}\), and finds reference-scale finite-part ambiguity; it does not select a canonical \(p=0\) completion. Raw \(C\), quantum rescaling equivalence, and the canonical edge remain open. In the local BFV zero block, direct Berezin integration equals elimination only when the induced determinant is retained; unweighted deletion is KILL. The lapse modulus, contour, and absolute measure remain unselected, so this does not complete a unique full trajectory. No exact endpoint transform, arbitrary-state/full-real-lapse rigging map, global cycle, physics or TOE result follows. | `claim:G1_V0_SELECTED_DENSITIZED_LIOUVILLE_CONSTRAINT_HAS_KL_RAQ_POSITIVE_PHYSICAL_FIBER`; `claim:G1_V0_SELECTED_DENSITIZED_RAQ_PHYSICAL_MEASURE_EQUALS_PRIOR_DP_STATIC_FIBER_MEASURE`; `claim:G1_V0_SELECTED_DENSITIZED_H_STANDARD_POSITIVE_MEASURE_EXTENDS_TO_NONZERO_P_ZERO_EDGE`; `claim:G1_V0_SELECTED_DENSITIZED_H_P_ZERO_FINITE_PART_HAS_CANONICAL_REFERENCE_SCALE`; `claim:G1_V0_DIRECT_BEREZIN_AND_WEIGHTED_ZERO_GHOST_ELIMINATION_AGREE`; `claim:G1_V0_UNWEIGHTED_ZERO_GHOST_DELETION_IS_A_VALID_TRAJECTORY_LEDGER`; `open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion`; `open:gate1-v0-lapse-modulus-contour-and-absolute-bfv-measure` |
| Where are the V0 formulas, philosophical implications, and next research bridges organized? | The formula chain, evidence/interpretation/open-layer separation, philosophical scope, and dependency-labelled route toward raw-constraint equivalence, global spectral completion, exact endpoint intertwining, an absolute BFV measure, inhomogeneous constraint closure, and relational-observable recovery are collected in one non-evidential ontology map. | `artifact:gate1-v0-quantum-cosmology-ontology-map`; `reading-path:gate1-v0-formula-philosophy-to-quantum-gravity-frontier` |
| Does any of this show that SUSY does not exist? | No. The graph rules out only the stated truncations and identifications. Phases 16–24 retain their declared bounds; Phases 25–56 advance one homogeneous lapse/thimble/BFV/local-workbench route without deriving a global saddle coefficient, positive state, flux-sector rule, or persistent soft spectrum. | Phase 16–56 scope guards |

### V0 formula, philosophy, and quantum-gravity frontier

[`GATE1_V0_QUANTUM_COSMOLOGY_ONTOLOGY_MAP.md`](../../cpt_temporal_folded_susy/GATE1_V0_QUANTUM_COSMOLOGY_ONTOLOGY_MAP.md)
is the compact human entry point. It gives the full selected formula ledger, then separates computed
facts from philosophical interpretation and open hypotheses. The corresponding reading path ends at
six dependency-labelled problems; those edges are navigation and planning memory only, with no
automatic execution, external KG ratification, physics promotion, or TOE promotion.

### Gate-1 straight KILL to trace-gauge redirect

The graph's `reading-path:gate1-anchor-through-kill-to-phase-locked-branch` should be read in this
order:

1. Phase 39 retains two bounded local cap witnesses; it does not supply good ends or a global signed
   vector.
2. The executed straight audit kills the declared rays and the full **anchor-through**
   \(\delta=qy\) class on its fixed-\(a\), pure-imaginary-lapse slice.
3. The later exact analytic identity for \(T=\rho e^{i\psi}\),
   \(\delta=x+i\psi/\kappa\) gives a positive full-rate negative-\(x\) end and positive kinetic
   positive-\(x\) end uniformly on a fixed finite lower-bypass regulator.
4. A smooth compact bend can equal the original Phase-39 field line throughout
   \(|y_\phi|\leq0.25\) and use the phase-locked affine ends outside. This is a genuine `BRANCH`, not
   `EQUIVALENCE` and not a reversal of the scoped straight KILL.
5. For general \(\delta=x+i b(\psi)\), strict positivity of the full-rate coefficient plus the two
   positive-\(x\) arm ends forces the principal band \(|\psi-\kappa b|<\pi/2\). An explicit uniform
   homotopy contracts that band to phase lock while retaining the same central window.
6. Goodness does not pick one representative: \(b_\lambda=\lambda\psi/\kappa\), \(0<\lambda<2\), is
   a continuous counterfamily. Exact phase cancellation alone selects \(\lambda=1\).
7. The consumed scalar-source one-shot fixes one newly declared real \((p_0,p_1,q)\) order and measure.
   Exact momentum elimination plus a finite-\(\epsilon\) full-action rectangular homotopy identifies its
   nonzero-lapse arms with the declared \(\Gamma_\lambda\) family and scalar orientation `+1`; this is a
   scoped `KEEP`, not a recovered physical original cycle and not a selection of \(\lambda=1\).
8. The sole zero-lapse extension invocation passed the square rewrite, then stopped at an asymmetric
   SymPy structural-equality guard before theorem guards or result emission. Treat this as `INVALID_RUN`,
   not as a scientific contradiction and not as a zero-lapse extension verdict.
9. The finite full-bosonic control retains both \(p_a\) and \(p_\phi\). Opposite quadratic signs rule
   out absolute convergence of their unchanged real axes under either one common lateral sign. The
   declared complex rays pass the fiberwise Gaussian check, but their \(-1\) negative-arm ledger is a
   frozen-\(A\) flat tangent, not a simultaneous nonlinear joint-cycle theorem.
10. The bounded trace-gauge discriminator derives the integrated homogeneous trace pair, its exact
   Lorentzian FP bracket, the on-shell horizon \(a^2V=2\), and genuine local simple-root reduction.
   Signed root residues remain pre-orientation data; the elementary delta ledger uses their absolute
   Jacobians.
11. Appending that static trace delta/FP factor to the inherited proper-time, fixed-\(a\), \(m=2\)
   source is `KILL`. Its endpoint-preserving constant-lapse condition already fixes the sole nonzero
   lapse-gauge mode, and a transverse endpoint chart requires a transformed action/state problem. This
   does not kill a separately rederived improved-static or time-dependent trace gauge.
12. The closed-FRW \(V=0\) follow-up keeps one classical local on-shell fixed-\(\Phi_*\)
   relational action on a frozen \(p_\phi=+1\), \(R>0\), \(D>0\) component. Its finite endpoint
   flow, local FP measure and time-dependent same-orbit control close, while the raw static, HTV
   improved-static, relational and mixed-polarization ledgers remain distinct.
13. The next bounded \(V=0\) calculation extends that shell coordinate across arbitrary real \(c=C\)
   on \(\mathcal U_+=\{p>0,R>0\}\). Its mixed generator gives a classical componentwise Darboux
   chart, endpoint potential \(B\), and exact \(c=0\) recovery of \(\Phi_*\) and \(B=P\).
14. The following bounded calculation keeps the phase \(-W\), half-density \(D^{-1/2}\), canonical
   relation and local Maslov branch only as a compact-interior principal momentum FIO. Its exact
   coarea discriminator kills finite-\(\hbar\) unitarity of the uncorrected one-term amplitude because
   the geometric endpoint density differs from the secant mean. It does not kill a corrected
   full-symbol or spectral transform.
15. The next bounded calculation separately keeps one improved-static finite BFV zero-mode
   replacement-source algebra on \(\mathcal U_+\). Its graded bracket, endpoint ideal, declared
   Fourier \(\delta(T)\delta(c)\), oriented ghost factor and reduced-identity compatibility pass. This
   does not repair the one-term FIO or construct a normalized endpoint transform or full trajectory
   measure.
16. The first user-directed continuation declares the local Darboux momentum convention
   \(H_D=L^2(\mathbb R_c\times\mathbb R_{+,p},dc\,dp)\). On that declared space,
   \(\widehat C_D=M_c\) with maximal multiplication domain is self-adjoint; \(E(\{0\})=0\) in
   Lebesgue \(L^2\), while \(\delta(M_c)\) is only a distributional \(c=0\) fiber form on the test
   space. This does not derive an original-variable ordering, physical measure or half-line edge theory.
17. Conditional on existence of any exact endpoint completion \(U_0\) in the declared mixed data
   class, \(e^{i\hbar\kappa c}U_0\) gives distinct exact-unitary completions with unchanged
   \(B\), canonical graph, \(a_0\), \(H_D\) and \(M_c\). Thus those data do not select a unique
   completion. Additional exact intertwining, full-symbol, domain or gluing data may restrict the
   family, and existence of \(U_0\) remains open.
18. The static source and order-zero \(\delta(M_c)\) fiber agree entrywise on one frozen three-state
   \(p>0\) test family. The exact positive-definite \(3\times3\) matrix and 36 independent
   quadratures pass. This is not an arbitrary-state regulator theorem or physical group average.
19. A separate selected densitization \(H=12\pi^2e^{3Q/2}C\), flat \(L^2(dQ\,d\phi)\) ordering and
   Fourier--Kontorovich--Lebedev transform give one \(p>0\) RAQ model. Its positive shell is
   \(\kappa_0=\sqrt{3/2}\,p/\hbar\) and its coarea measure is \(dp/(2\sqrt6\hbar p)\), not the
   earlier static \(dp\) fiber measure. This selects neither raw \(C\), constraint-rescaling
   equivalence nor the singular \(p=0\) sector.
20. The local BFV zero-block Ward control resolves the earlier bookkeeping mismatch: direct oriented
   Berezin integration and ghost-pair elimination agree when the induced odd determinant \(\lambda\)
   is retained, cancelling the bosonic \(\delta(\lambda c_0)\) Jacobian. Unweighted deletion leaves
   \(1/\lambda\) and is KILL. This still selects no lapse modulus, contour, absolute measure or unique
   full trajectory completion. Stop at `open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion`,
   `open:gate1-v0-lapse-modulus-contour-and-absolute-bfv-measure` and
   `open:gate1-phase-locked-fiber-to-source-derived-joint-cycle`: exact endpoint construction,
   selected lower/full symbol, original-variable ordering and edge domains, an arbitrary-state or
   full-real-lapse rigging map, global normalization and Maslov gluing, charts on other components,
   a global atlas, coordinate-polarization endpoints, a full BFV trajectory measure, absolute contour
   and Pfaffian orientation, \(N=0\) contact terms and the zero-including full \(q\)-paired distribution
   remain unconstructed. Complex scale-factor/mixed ends, regulator removal, new intersections,
   complete saddle/upward/sheet/Stokes census, determinant/BFV orientation and the global vector remain
   missing.

### Phase 23 reading path

The graph's `reading-path:minisuperspace-rigging-to-density` should be read in this order:

1. `concept:distributional-rigging-map-versus-bounded-projector` leads to `claim:P23_FULL_REAL_LAPSE_AVERAGE_DEFINES_DISTRIBUTIONAL_RIGGING_MAP` and `claim:P23_FULL_REAL_LAPSE_RIGGING_KERNEL_IS_A_BOUNDED_KINEMATICAL_PROJECTOR`.
2. `concept:induced-product-versus-signed-wdw-current` leads to `claim:P23_EXPLICIT_CLOCK_AND_POSITIVE_FREQUENCY_GIVE_POSITIVE_INTEGRATED_NORM` and `claim:P23_POSITIVE_FREQUENCY_LOCAL_CURRENT_IS_POINTWISE_POSITIVE`.
3. `concept:constraint-rigging-versus-state-preparation-bridge` separates imposing the constraint from supplying spectral weights; follow `claim:P23_CPT_REALITY_AND_ZERO_SIGNED_CURRENT_UNIQUELY_SELECT_A_DENSITY` and `claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY`.
4. `claim:P23_REGULATED_DENSITY_HAS_TRACE_CLASS_DECOMPACTIFICATION_LIMIT` and `claim:P23_QUADRATIC_ZERO_ROOT_HAS_A_REGULAR_INTRINSIC_CLOCK_GAUGE` lead to `open:p23-cap-derived-regulator-independent-density`, while `open:p22-gauge-fixed-local-sugra-seam-density` remains the later local-SUGRA gate.

### Phase 24 reading path

The graph's `reading-path:connected-starobinsky-response-to-physical-density` should be read in this order:

1. `concept:connected-boundary-response-versus-quantum-entanglement` leads from the supported real saddle to `claim:P24_CONNECTED_PRINCIPAL_FUNCTION_HAS_NONZERO_CROSS_BOUNDARY_RESPONSE`; a nonzero mixed principal-function Hessian is a classical response statement, not yet quantum entanglement.
2. `concept:constraint-preserving-versus-fixed-length-hessian` separates the rank-one constrained mixed block from the full-rank fixed-length mutation. Follow `claim:P24_CONSTRAINT_PRESERVING_MIXED_HESSIAN_HAS_RANK_ONE` and the contradicted `claim:P24_SMALL_MIXED_SINGULAR_VALUE_IS_A_PHYSICAL_MODE`.
3. `concept:conditional-fixed-scale-gaussian-versus-physical-gravitational-state` leads to the supported conditional scalar Gaussian and the contradicted claim that the full real boundary precision is positive and normalizable.
4. `concept:boundary-response-hessian-versus-bulk-morse-spectrum` leads to `open:p24-gravitational-thimble-and-bulk-determinant`; `open:p24-physical-two-boundary-density-and-entropy` separately requires a physical factorization, measure, inner product, positivity, and trace test.

### Phase 25–28 reading path

The graph's `reading-path:connected-lapse-thimble-to-bfv` should be read in this order:

1. Phase 25 promotes the supplied Phase-24 interval to a stationary fixed-boundary lapse saddle and finds a local complex convergent tangent, while keeping the distinct real Dirichlet caustic separate.
2. Phase 26 continues one bounded analytic arm through a projection turn and verifies Airy scaling at the real fold; neither the cutoff endpoint nor the turn is a global thimble coefficient.
3. Phase 27 fixes the Lorentzian–Euclidean convention and proves a raw fixed-T `1/|T|` endpoint behavior, then separates the positive-half-line resolvent from full-line constraint support. The raw kernel is not the full BFV kernel.
4. Phase 28 records bounded constructed crossings and a reduced Euclidean-continued homogeneous BFV control. Dirichlet ghosts have no zero mode, but proper length remains BRST invariant; the local Gaussian is conditional.
5. The path ends at `open:p28-global-relative-homology-and-intersection`, `open:p28-zero-lapse-uniform-bfv-kernel`, `open:p28-full-gauge-reduced-superdeterminant`, `open:p28-physical-state-and-density`, and `open:p28-string-three-form-soft-spectrum`.

### Phase 29 reading path

The graph's `reading-path:zero-lapse-distribution-and-measure` keeps five layers separate:

1. the normalized frozen leading real-lapse Fresnel kernel converges to `delta_flat` only as a distribution under the declared local `da dphi` endpoint measure;
2. its coincident-endpoint pointwise amplitude still diverges as `1/N`;
3. after fixed-parameter BFV rescaling and the matching gauge-condition normalization, the nonzero-mode ghost factor is T-independent and proper time remains a modulus;
4. inserting an ad hoc lapse power changes the half-line resolvent and full-line rigging distribution rather than merely canceling a normalization;
5. the indefinite kinetic sign still requires a separately derived conformal contour, and the physical WDW endpoint measure, all-orders uniform parametrix, full determinant, global coefficient, and trace-class state remain open.

### Phase 30 reading path

The graph's `reading-path:coupled-conformal-cycle-and-determinant-line` separates local convergence, relative magnitude, and global phase:

1. `concept:fibered-field-lapse-cycle-versus-product-rotation` leads to the supported finite-cutoff Schur-shifted cycle and the contradicted sufficiency of the tested independent field/lapse rotation;
2. `concept:relative-determinant-magnitude-versus-determinant-line-phase` separates the recorded midpoint-measure relative magnitude from the contradicted cutoff-independent bare lattice sign;
3. `concept:real-lapse-maslov-gluing-versus-single-holomorphic-sheet` records that the real-axis identity kernel needs `1/|N|`, whereas a single holomorphic `1/N` sheet has the wrong sign on the negative side;
4. the pointwise common limit of shifted positive-imaginary rays does not fix an integer Picard–Lefschetz coefficient because the singular endpoint and global upward cycle remain unresolved;
5. the path returns to `open:p29-conformal-bfv-uniform-parametrix`: the full phase-space BFV super-Hessian, primed superdeterminant, determinant line through `N=0`, all upward intersections, and regulator removal were not computed in Phase 30.

### Phase 31 reading path

The graph's `reading-path:canonical-bfv-hybrid-to-physical-determinant` keeps a canonical lift distinct from a physical determinant:

1. exact momentum elimination reproduces the independently assembled Phase-30 configuration-plus-`T` Hessian;
2. the unreduced proper-time-gauge canonical block has stable positive sign over the recorded odd/even cutoffs, but this does not choose its momentum contour;
3. nonzero homogeneous alpha=0 BFV quartet factors are background-independent only in the declared finite-dimensional factorization and cancel in a same-regulator benchmark/reference ratio;
4. the bare full bosonic BFV sign still alternates with gauge-pair parity, so it cannot be identified with the physical determinant line;
5. the local `p_a` clock scan changes endpoint polarization, and the path ends at the still-open gauge-reduced determinant, endpoint measure, global contour, and state problems.

### Phase 32 reading path

The graph's `reading-path:lapse-prescription-to-local-intersection` separates a projected lapse-base crossing from signed joint and global coefficients:

1. the causal positive half-line is a sourced resolvent and meets the recorded dual only at its regulated endpoint;
2. the separately specified below-origin full real line maps to a right `T` semicircle and has one recorded finite-radius projected crossing, whose coordinate sign is `+1` only under the declared ambient, column, dual-flow, and Gaussian-lift orientations; the upper bypass maps left and misses that positive dual;
3. the declared signature-(-,+) momentum rays are locally convergent, but comparing analytic `C/N` transport to the negative-real `C/|N|` identity kernel needs additional orientation-line gluing not derived as a Maslov index;
4. the complex BVP was sampled at five angles on each of four lower arcs. Those samples support the projected crossing but do not exclude between-sample sheet jumps or Jacobi zeros, orient the full joint BFV cycle, or enumerate other dual components, sheets, ends, and Stokes jumps;
5. `open:p28-global-relative-homology-and-intersection` and `open:p32-cpt-pin-lapse-class-selection` remain open, so neither global `n_sigma=+1` nor CPT/Pin selection is asserted.

### Phase 33 reading path

The graph's `reading-path:simple-fold-to-global-airy-cycle` separates local uniformization from a selected physical kernel:

1. the Phase-25 caustic is resolved into two actual real fixed-boundary branches whose action gap and soft Jacobi direction have the universal simple-fold scaling;
2. `claim:P33_RECORDED_DIRICHLET_FOLD_IS_ADDITIONAL_LAPSE_SADDLE` is contradicted by nonzero `W_T`, so endpoint-projection coalescence is kept distinct from lapse stationarity;
3. the divergent separate Van Vleck proxies diagnose failure of isolated-saddle asymptotics, while the canonical Airy equation supplies a regular local solution space without proving the uncomputed physical measure finite;
4. Ai/Bi regularity does not choose the relative cycle, Stokes multiplier, analytic amplitude, or determinant line, and the radius-one fold chart is locally disjoint from the Phase-32 lapse pieces;
5. `open:p33-airy-cycle-amplitude-and-global-continuation` returns the path to the still-open global relative-homology, full superdeterminant, endpoint-measure, and physical-state gates.

### Phase 34 reading path

The graph's `reading-path:reduced-fold-dual-to-global-joint-cycle` keeps branch existence separate from an oriented cycle connection:

1. `claim:P34_RECORDED_INCOMING_REAL_SEGMENT_IS_DIRECTED_TOWARD_FOLD` records 47 post-saddle real points with `W_T<0`;
2. `claim:P34_BOUNDED_DIRECTED_CONSTANT_PHASE_PAIR_EXISTS_BEYOND_FOLD` separately supports conjugate reduced branches beyond the fold through `Re T=13`;
3. the declared flat-`T` flow direction and bounded BVP table do not connect the incoming cycle to either outgoing arm because the `T-T_c~u^2` chart degenerates at the fold;
4. the sampled Jacobi and lapse-base exclusions are bounded statements, not a complete sheet, good-end, or intersection census;
5. `open:p34-full-joint-dual-determinant-and-global-census` requires the Airy connection, determinant-line orientation, full joint field–lapse flow, and global relative cycle before assigning `n_sigma` or a physical state.

### Phase 35 reading path

The graph's `reading-path:reduced-detline-transport-to-physical-prefactor` keeps a reduced endpoint section separate from a physical determinant:

1. `claim:P35_TRACKED_REDUCED_ENDPOINT_DETERMINANT_LINE_IS_TRANSPORTABLE` records a nonzero 57-point table and recursively transported sampled phase/square-root lifts in the declared endpoint basis, not a proved zero-free interpolation;
2. `claim:P35_RECORDED_UPPER_NEAR_FOLD_PHASE_IS_CONSISTENT_WITH_MINUS_PI_OVER_2` records finite-resolution coordinate-normalized consistency only after freezing row, column, soft-vector, and sheet orientations; it is not a proved limit;
3. `claim:P35_CONJUGATE_REDUCED_BOSONIC_ENDPOINT_PHASES_CANCEL_RELATIVELY` is a reduced determinant-section statement, not a Gaussian or full superdeterminant cancellation;
4. `concept:relative-endpoint-detline-transport-versus-absolute-orientation` keeps sampled transport distinct from the uncomputed physical Van Vleck block, endpoint measure, continuum lift, and absolute Maslov orientation; `claim:P35_RELATIVE_ENDPOINT_TRANSPORT_FIXES_ABSOLUTE_MASLOV_ORIENTATION` is contradicted as a sufficient-data claim;
5. `open:p35-absolute-detline-full-bfv-and-global-cycle` retains the incoming-to-outgoing fold connection, absolute determinant/Maslov orientation, complete joint cycle, regulated BFV/SUGRA superdeterminant, and global `n_sigma` as open gates.

### Phase 36 reading path

The graph's `reading-path:local-airy-connection-to-global-original-cycle` keeps declared basis algebra and numerical root continuation separate from physical cycle transport:

1. `claim:P36_EXACT_LOCAL_AIRY_GAUSS_MANIN_CONNECTION_IS_FIXED` supports exact contour and basis-change identities only in separately ordered CW and CCW local bases;
2. `concept:cycle-map-versus-bvp-root-permutation` records that the two first duals depend on different companion cycles, so they are not two images of one common physical upward dual;
3. `claim:P36_TRACKED_AI_ROOT_HAS_REGULAR_CW_U_AND_CCW_L_CONTINUATIONS` supports two sampled root-sheet laterals on three finite radii, not realizations of the formal `K_U` and `K_L` cycles or a zero-radius theorem;
4. `claim:P36_PHASE32_PLUS_PHASE35_UNIQUELY_SELECTS_ONE_OUTGOING_FOLD_ARM` is contradicted only as a sufficient inference within the recorded local gates; a complete original contour and its homotopy may still select one arm globally;
5. `open:p36-original-cycle-hard-determinant-and-global-bfv-state` retains common-dual transport, the original relative cycle, hard determinant quotient and Airy/Airy-prime amplitudes, absolute signs, full BFV/SUGRA determinant, global `n_sigma`, and the physical state.

### Phase 37 reading path

The graph's `reading-path:closed-fold-holonomy-to-full-pfaffian-line` keeps local same-basepoint transport separate from a physical global line:

1. `claim:P37_LOCAL_BVP_ROOT_COVER_HAS_NONTRIVIAL_Z2_MONODROMY` supports the exchange of both tracked roots on three sampled finite enclosing loops, while the numerical nonenclosing loop follows only its tracked control root and the exact winding-zero model is trivial;
2. `concept:root-cover-monodromy-versus-airy-solution-and-cycle-monodromy` prevents the root permutation from being substituted for the single-valued Ai/Bi solution map or a Gauss--Manin map on a specified relative-cycle space;
3. `claim:P37_SAMPLED_REDUCED_HALF_FORM_HAS_CONDITIONAL_ORDER_FOUR_HOLONOMY` retains only the same-basepoint conjugacy invariants of the nonzero minimal-jump sampled lift, conditional on no unresolved intersample zero or alias winding;
4. `claim:P37_ROOT_MONODROMY_ALONE_BREAKS_PHASE17_BASIS_EQUIVALENCE` is contradicted in the exact finite-fiber control: a physical sheet anchor or distinct derived fermionic holonomy would be additional input, not a consequence of the bare swap;
5. `concept:reduced-bosonic-half-form-versus-fermion-pfaffian-and-pin` and `open:p37-global-cycle-hard-cfu-full-bfv-pfaffian-gate` retain the original cycle, hard CFU coefficients, spacetime Pin lift, fermion Pfaffian line, complete BFV/SUGRA operator, supercharge, quantum constraint, and physical state as open.

### Ordered five-gate reading path

The graph's `reading-path:ordered-five-gate-global-cycle-to-pole-spectrum` decomposes the Phase-37
omnibus frontier into five typed promotion gates:

1. `open:gate1-original-cycle-signed-global-intersections` transports one pre-specified regulated joint
   lapse--field--gauge relative cycle and fixes its complete oriented integer intersection vector;
2. `open:gate2-hard-cfu-airy-coefficients` derives the regular hard quotient and absolute Airy/Airy-prime
   coefficients for the Gate-1 cycle without double-counting the soft factor;
3. `open:gate3-full-bfv-pfaffian-pin-holonomy` computes the selected saddle combination's complete
   gauge-reduced boson--fermion--ghost determinant/Pfaffian line, Pin lift, and closed holonomy;
4. `open:gate4-spinorial-charge-domain-constraint-closure` either constructs a conserved spinorial
   charge on one positive common domain with anomaly-free constraint closure or records the typed global
   obstruction instead;
5. `open:gate5-persistent-order-and-pole-splitting` derives a finite-energy persistent order parameter
   and a nonzero late-time interacting boson--fermion retarded-pole difference against matched controls.

The `BLOCKED_BY` chain is a claim-promotion dependency, not a ban on exploratory calculation. A later
calculation performed early remains `CONDITIONAL` until every earlier gate supplies its compatible
evidence-backed typed output. A complete stable zero vector, a proved obstruction, or another scoped
negative answer can resolve a gate epistemically, but it unlocks the preferred downstream route only when
the next gate's required input actually exists. This roadmap does not alter any Phase-37 claim or scope,
and it stops before asserting a physical state, a completed quantum-cosmology model, or quantum gravity.

### Phase 38 reading path

The graph's `reading-path:projected-lapse-data-to-joint-cycle-identifiability` starts Gate 1 but keeps
data sufficiency, surrogate algebra, and physical topology separate:

1. `claim:P38_RECORDED_DATA_DO_NOT_LICENSE_INVERSE_JOINT_CYCLE_RECONSTRUCTION` is supported only as a
   boundary on what follows from the current record: neither a physical injectivity theorem nor
   admissible physical completions have been supplied. The noninjective \(1\times3\) map is a finite
   surrogate and does not prove that physical relative homology is noninjective or nonunique;
2. `claim:P38_ROOT_SWAP_CAN_REPLACE_GAUSS_MANIN_CYCLE_TRANSPORT` is contradicted by the typed mutation:
   the root permutation and the relative-cycle coefficient map have different domains and give different
   outputs for the declared conditional input;
3. `claim:P38_CONDITIONAL_GAMMA0_INPUT_MAPS_TO_BOTH_LOCAL_ARMS` supports
   \(G^T(1,0)^T=(-1,-1)^T\) only as a local representation. It neither selects the physical incoming
   coefficient nor computes hard CFU data;
4. `claim:P38_SAMPLED_TRACKED_ARMS_REMAIN_PROJECTED_DISJOINT_THROUGH_RET16` concerns three new sampled
   checkpoints of one continued upper root/basin and real-coefficient conjugation controls. It is not a
   continuous no-crossing theorem, an integration-mesh theorem, or an independently continued lower arm;
5. `claim:P38_BOUNDED_LEDGER_SUFFICES_TO_FIX_GLOBAL_INTERSECTION_VECTOR` is contradicted because the
   original joint cycle and full-joint sign are absent and all three recorded ends remain unresolved.
   `open:p38-explicit-joint-action-cycle-and-oriented-intersections` is the next concrete Gate-1 debt.

Gate-2 hard-CFU functions may be calculated conditionally in parallel. What remains blocked is their
promotion into a physical uniform kernel before Gate 1 supplies the actual typed cycle vector and the two
outputs pass a joint consistency check.

### Phase 39 reading path

Phase 39 begins the explicit full-space calculation while keeping a local chart witness separate from a
relative-homology pairing:

1. `claim:P39_FROZEN_M2_ACTION_HAS_GENUINE_POSITIVE_T_DISCRETE_JOINT_SADDLE` is supported for the
   frozen two-segment configuration action. The recorded positive-\(T\) root has a small gradient
   residual and nonzero Hessian inertia, while the four-root bounded ledger explicitly prevents a
   uniqueness or complete-census claim;
2. `claim:P39_DECLARED_M2_CAP_PIECES_HAVE_LOCAL_SIX_REAL_PLUS_ONE_CANDIDATES_ON_ONE_FROZEN_K_PATCH`
   is supported only for two cap pieces and one finite-radius, finite-time three-real-dimensional
   upward-chart patch. Both candidates are solved in all six real coordinates and their direct declared
   configuration-coordinate determinant signs are \(+1\); the projected lapse signs are not used to
   infer them;
3. `claim:P39_TWO_FROZEN_CAP_LOCAL_CANDIDATES_SUFFICE_TO_FIX_GLOBAL_INTERSECTION_VECTOR` is
   contradicted by the unsearched straight arms and cap reintersections, incomplete root and upward-cycle
   census, uncertified exact nonlinear manifold and non-Stokes chamber, and unresolved relative good
   ends. Its null outputs mean "not computed," not a zero intersection number.

At the Phase-39 boundary, the next controlled lift was an \(m=3\) or \(m=4\) endpoint-asymmetric
calculation exposing the first reflection-odd history mode, followed by \(m=5\), complete
chain/dual-component searches, lateral Stokes data, good-end classification, and
cutoff/metric/homotopy stability. Phases 40–50 now cover the local steps described later, but the
complete object required for Gate 1's signed global vector remains missing.

### Phase 40 reading path

Phase 40 performs the first \(m=3\) endpoint-asymmetric local pilot but preserves the distinction between
a source response, a launch-coordinate choice, and a global relative-cycle result:

1. `claim:P40_RANK_ONE_PHI_SOURCE_HAS_ANCHOR_SUBTRACTED_SIGN_REVERSING_ODD_RESPONSE` is supported for
   one frozen saddle family and one rank-one phi-only endpoint source. Exact reflection covariance and a
   resolved two-dimensional odd Hessian block make the sampled response meaningful, but the unprobed
   independent odd source prevents a full-odd-sector or physical-time-arrow inference;
2. `concept:fixed-flow-mobility-versus-delta-dependent-morse-launch-ellipsoid` keeps the delta-zero
   inverse-metric mobility fixed across the run. The delta-dependent Procrustes-aligned signed-subspace
   frames and launch ellipsoids parameterize local initial data; their variation is not a metric-homotopy
   test or an exact unstable-manifold certificate;
3. `claim:P40_FIVE_SAMPLED_M3_CAP_CANDIDATES_HAVE_LOCAL_FULL_R10_SIGN_PLUS_ONE` is supported only at
   the five declared delta values. All five direct mode-orientation-corrected signs are \(+1\), while
   full finite-difference, variational, flow, and orientation audits are confined to three primary
   points. No continuous branch or intersample nonzero-determinant theorem follows;
4. the converged K-launch-coordinate clamp misses its local fit tolerance, but it freezes one launch
   coordinate rather than spanning the full two-dimensional odd field sector. It therefore supplies a
   scoped mutation diagnostic, not an ablation theorem and not a no-root claim;
5. `claim:P40_RECORDED_LOCAL_M3_DATA_DO_NOT_LICENSE_BOUNDED_CHAIN_OR_GLOBAL_INTERSECTION_INFERENCE`
   records an evidential-sufficiency boundary. The absent \(m=4\)/cutoff comparison, arms,
   reintersections, exhaustive components, exact nonlinear K, Stokes chamber, and good ends keep the
   bounded-chain sum, complete vector, and `global_n_sigma` null. Gate 1 remains open.

### Phase 41 reading path

Phase 41 adds the missing independent endpoint-source axis at (m=4), while separating a computed
local root from the stronger robustness claim that requires every frozen tangent control:

1. `claim:P41_TWO_SOURCE_ODD_SUSCEPTIBILITY_HAS_STABLE_NUMERICAL_RANK_TWO` is supported under the
   declared dimensionless normalization and finite-precision rule. Its smallest singular value exceeds
   ten times the step-plus-solver stability estimate by a factor of about 28.28; exact algebraic rank
   two, a physical time arrow, and continuum response are not inferred;
2. `claim:P41_FIVE_PRIMARY_M4_CAP_CANDIDATES_HAVE_LOCAL_FULL_R14_SIGN_PLUS_ONE` records five accepted
   local candidates at the shared, signed phi, and signed a endpoints. All have direct sign (+1),
   root-Jacobian sign (-1), and pass the declared residual, transversality, reflection, orientation,
   overlap-chart, launch, and path checks;
3. `claim:P41_RETAINED_TANGENT_CONTROL_FAILURE_LEAVES_BOTH_SOURCE_ROBUSTNESS_CLAIMS_INCONCLUSIVE`
   preserves the failed test rather than choosing a favorable post-result step. The aggregate
   finite-difference operator errors pass, but the first frozen `u2` adjacent pair changes by 22–80%,
   above 2%, at all three audited points. Thus both source robustness outputs remain inconclusive while
   the five roots remain recorded;
4. `claim:P41_RECORDED_LOCAL_M4_DATA_DO_NOT_LICENSE_CANONICAL_CROSS_CUTOFF_OR_GLOBAL_INTERSECTION_INFERENCE`
   keeps affine m2/m4 cycle embedding distinct from equality of their actions or upward cycles, and
   keeps the nonnested m3/m4 `+1` signs descriptive rather than canonical. The incomplete chain,
   census, Stokes, end, and physical-cycle data force six promoted outputs to null and leave Gate 1
   open.

### Phase 42 reading path

Phase 42 applies the same fail-closed method to the retained Phase-41 tangent failure:

1. `claim:P42_SOLVER_NOISE_AND_FROZEN_STEP_PAIR_ARTIFACT_SUPPORTED_AT_PHI_AND_A` records two
   compatible numerical/procedural labels at `phi_plus` and `a_plus`; `shared_zero` does not satisfy
   those frozen quantifiers, and no unique cause is selected;
2. `claim:P42_LOCAL_HESSIAN_ACTION_IDENTITY_ANOMALY_IS_SUPPORTED_WITHOUT_PROVING_A_BUG` records 12,
   11, and 10 stable local Hessian-action violations at the three roots. The frozen classifier's
   `VARIATIONAL_RHS_BUG_EVIDENCE` name is not promoted into proof of a software defect. In particular,
   the returned time column is assembled at its own endpoint, while the compared state-only RHS uses a
   different solver endpoint; its discrepancy lies inside the cross-tier solver/state envelope;
3. `claim:P42_NORMALIZED_LOCAL_MATRIX_HOMOTOPY_SUFFICIENTLY_PRESERVES_FIXED_ROOT_SIGN` retains the
   three eta-less-than-one sufficient certificates and sign `-1`, but only for the sampled normalized
   matrices. It does not establish reference correctness or global determinant-line transport;
4. `claim:P42_REFERENCE_TANGENT_REMAINS_INCONCLUSIVE_AND_GLOBAL_PROMOTION_IS_PROHIBITED` keeps the
   shared-zero `u2` neighbor-stability miss visible. Phase 41 remains 8/9; sixteen prerequisites remain
   false, six promoted fields remain null, and Gate 1 remains open.

### Phase 43 reading path

Phase 43 freezes every local slot before arbitrating the Phase-42 anomaly layer:

1. `claim:P43_INDEPENDENT_HIGH_PRECISION_LOCAL_REFERENCE_IS_CORROBORATED_AT_ALL_FROZEN_SLOTS`
   records exact symbolic, direct-gradient, 80/120-decimal, unchanged-step, and prospective small-step
   agreement at all 90 slots. This is a local finite-model derivative reference, not a physical or
   integrated-tangent theorem;
2. `claim:P43_NUMPY64_LOCAL_RHS_OUTPUT_MISMATCH_IS_SUPPORTED_WITHOUT_PROVING_A_CODE_DEFECT`
   records that 13/90 byte-pinned NumPy64 outputs cross the uniform `5e-13` normwise threshold. The
   operational label does not separate state formation, Hessian evaluation, contraction order,
   matrix-vector rounding, cancellation, or conditioning and therefore proves no unique defect;
3. `claim:P43_DOUBLE_PRECISION_FD_ARTIFACT_EXPLAINS_ALL_33_PHASE42_ANOMALIES` is contradicted only as
   the frozen universal sufficient claim. The fixed finite-difference rule is supported at 28/33
   disclosed anomalies, but five complete direction-2 slots are exceptions. That does not negate a
   finite-difference contribution at the 28 supported slots;
4. `claim:P43_LOCAL_ARBITRATION_DOES_NOT_TEST_INTEGRATED_TANGENT_OR_LICENSE_GLOBAL_PROMOTION` keeps
   zero root, ODE, integrated-tangent, time-column, reference-tangent, orientation, and global-cycle
   evaluations visible. Phase 41 stays 8/9, Phase 42 stays inconclusive, sixteen prerequisites remain
   false, six global and seven desired outputs remain null, and Gate 1 remains open.

### Phase 44 reading path

Phase 44 freezes the Phase-43 13/77 split before decomposing every local arithmetic slot:

1. `claim:P44_DECLARED_SOURCE_FORMULA_IS_EXACTLY_IDENTICAL_TO_THE_INDEPENDENT_MODEL` records exact
   zero source-minus-independent differences for three actions, 21 gradient components, and 147
   Hessian components. This excludes a mismatch between the two declared formulas; it does not prove
   physical-model, state, rounding, or integrated-solver correctness;
2. `claim:P44_ALL_DISCLOSED_NUMPY64_MISMATCHES_FIT_THE_DECLARED_MIXED_FORWARD_ERROR_MODEL` records
   closed signed telescopes at 90/90 slots and fixed componentwise/normwise forward-model coverage at
   13/13 disclosed mismatches and 77/77 controls. Coefficient, state, Hessian, and contraction evidence
   is nonexclusive in both cohorts, signed contributions can cancel, and no unique cause or best
   algorithm is selected;
3. `claim:P44_LOCAL_ARITHMETIC_DECOMPOSITION_DOES_NOT_REPAIR_THE_TANGENT_OR_LICENSE_GLOBAL_PROMOTION`
   keeps zero root, ODE, integrated-tangent, time-column, orientation, determinant-line, and global-cycle
   evaluations visible. Phase 41 stays 8/9, Phase 42 stays inconclusive, the historical Phase-43 label
   is not rewritten, sixteen prerequisites remain false, six global and seven desired outputs remain
   null, and Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

### Phase 45 reading path

Phase 45 follows the Phase-44 arithmetic result into the integrated tangent at the three fixed roots:

1. `claim:P45_INDEPENDENT_INTEGRATED_TANGENT_IS_PRECISION_STABLE_AT_THREE_FIXED_ROOTS` records that the
   independent 50- and 80-digit tangent paths agree at all retained fractions after complex128
   projection. It does not claim symbolic identity of internal arbitrary-precision states;
2. `claim:P45_SOURCE_TANGENT_AND_ROOT_JACOBIAN_AGREE_WITH_INDEPENDENT_REFERENCE` records source/reference
   tangent agreement within `2.741e-12`, root-Jacobian agreement within `3.748e-12`, reference/R4
   agreement within `1.101e-5`, and normalized sign `-1` at all three roots;
3. `claim:P45_TANGENT_CONTROL_FAILURE_IS_STABLE_TO_LOCAL_RHS_REPLACEMENT` records that the pinned
   historical `u2` plateaus remain failed while source tangent-RHS repair is not supported. The
   state-map finite-difference ladder is not recomputed, so its unique cause stays open;
4. `claim:P45_LOCAL_STABILITY_DOES_NOT_LICENSE_GLOBAL_PROMOTION` keeps Phase 41 at 8/9 and records zero
   new roots, orientations, determinant lines, complete chains, physical cycles, or global intersection
   integers. Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

### Phase 46 reading path

Phase 46 follows the Phase-45 tangent result into the complete historical `u2` state-map ladder:

1. `claim:P46_INDEPENDENT_STATE_MAP_U2_LADDER_IS_STABLE_AND_AGREES_WITH_TANGENT` records both adjacent
   plateau pairs below `2.019e-7`, 36/36 stable 50/80-digit probes after complex128 projection, and
   agreement with the Phase-45 independent tangent columns below `2.858e-7` at all three roots;
2. `claim:P46_LOCAL_FLOW_RHS_REPAIR_IS_SUPPORTED_UNDER_FIXED_PROJECTION` records exact reproduction of
   the historical production failures, source endpoint agreement at the `1e-9` scale, and tight/Radau
   derivative-column disagreement above `0.005`, yielding the frozen scoped repair classification;
3. `claim:P46_LOCAL_REPAIR_DOES_NOT_PROVE_SOURCE_FORMULA_DEFECT_OR_LICENSE_GLOBAL_PROMOTION` keeps the
   80-digit-local-RHS/complex128-integrator boundary explicit. It does not identify one coefficient,
   state, gradient, solver, or subtraction cause, rewrite Phase 41, or compute a global object;
4. `open:p46-source-gradient-flow-error-budget` is the next local diagnostic. The distinct physical
   Gate-1 original-cycle and global-intersection debt remains open.

### Phase 47 reading path

Phase 47 partially follows the Phase-46 source-gradient budget without closing its propagation half:

1. `claim:P47_LOCAL_SOURCE_FLOW_TELESCOPES_CLOSE_AT_ALL_RETAINED_SLOTS` records bitwise source-boundary
   reproduction, stable 80/120-digit projections, and closed signed telescopes at all 36 states and all
   18 paired derivatives;
2. `claim:P47_GENERATED_GRADIENT_EVALUATION_IS_LARGEST_RETAINED_MIXED_ARITHMETIC_STAGE` records the
   generated-gradient delta as the largest stage norm in 36/36 and 18/18 slots. This is a descriptive
   signed-budget result, not a unique-cause or faulty-suboperation verdict;
3. `claim:P47_LOCAL_BUDGET_DOES_NOT_BOUND_ENDPOINT_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION` preserves
   the missing intermediate-path, repaired-integration, sensitivity-propagator, solver-accumulation, and
   global-cycle boundaries. Phase 41 remains 8/9; Phases 44 and 46 remain unchanged;
4. `open:p46-source-gradient-flow-error-budget` stays open for the complete intermediate propagation
   and solver budget. `open:p48-gradient-hybrid-error-transport-control` narrows the next calculation to
   a gradient-only hybrid path with retained checkpoints and error transport. Gate 1 remains separately
   `OPEN_PARTIAL_PROGRESS`.

### Phase 48 reading path

Phase 48 executes the gradient-only integrated ablation and retains its negative result:

1. `claim:P48_GRADIENT_ONLY_CLONGDOUBLE_PATHS_MATCH_LOCAL_FLOW_AND_ENDPOINT_LIMITS` records all eighteen
   successful DOP853 paths, all ninety local-flow probes below `5e-8`, and every endpoint state below
   the `1e-8` Phase-46 comparison limit on the pinned NumPy long-double platform;
2. `claim:P48_GRADIENT_ONLY_CLONGDOUBLE_REPAIRS_THE_FULL_U2_LADDER` is contradicted by the frozen
   all-root predicate: only one full ladder is stable, and every root misses both all-step `0.005`
   derivative-reference limits. No failed step is discarded;
3. `claim:P48_PLATFORM_ABLATION_DOES_NOT_CLOSE_PROPAGATION_OR_LICENSE_GLOBAL_PROMOTION` keeps the
   missing variational propagation, state-formation, contraction, solver-accumulation, subtraction,
   portability, and global-cycle boundaries explicit;
4. `open:p48-gradient-hybrid-error-transport-control` was the then-open implementation problem. Phase 49
   subsequently resolves only its gradient-only-versus-late-projection choice and leaves formal
   transport/portability under `open:p49-formal-endpoint-transport-and-portable-flow-adapter`, nested
   inside the broader source/solver budget. Historical Phases 41 and 44–47 are unchanged, global
   promotion is prohibited, and Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

### Phase 49 reading path

Phase 49 completes the paired implementation ablation without closing the formal numerical or physical
debts:

1. `claim:P49_FULL_FLOW_CLONGDOUBLE_PASSES_ALL_FROZEN_STATE_MAP_CONTROLS` records all eighteen paths,
   ninety probes, endpoint states, full ladders, and both derivative references below their frozen
   limits, with no dropped root, step, sign, probe, or path;
2. `claim:P49_PHASE48_49_ABLATION_SUPPORTS_LATE_COMPLETE_FLOW_PROJECTION` compares the retained
   Phase-48 gradient-only failures with the otherwise fixed Phase-49 success. It supports keeping
   clongdouble through complete-flow contraction before one solver-boundary projection on this platform;
3. `open:p48-gradient-hybrid-error-transport-control` is resolved only as that implementation choice.
   `open:p49-formal-endpoint-transport-and-portable-flow-adapter` keeps the formal propagator,
   solver/subtraction separation, and cross-platform adapter contract open;
4. `claim:P49_SCOPED_REPAIR_DOES_NOT_PROVE_PORTABILITY_OR_LICENSE_GLOBAL_PROMOTION` preserves Phase 41
   at 8/9, Phases 44–48 unchanged, global promotion prohibited, and Gate 1
   `OPEN_PARTIAL_PROGRESS`.

### Phase 50 reading path

Phase 50 leaves the (m=4) arithmetic-repair branch and tests one declared finite-cutoff saddle and
local-plane bridge without promoting it into a cycle theorem:

1. `claim:P50_FIVE_FROZEN_M4_SADDLES_CONTINUE_TO_M5_ON_DECLARED_STABILIZED_PATHS` records all five
   fine, coarse, and reverse saddle paths, fixed `(5-,4+,0)` sampled inertia, reflection covariance,
   and the two-step tangent controls. The added stabilizers define the bridge; the exact nonnesting
   witness prevents identifying it with equality of the (m=4) and (m=5) actions;
2. `claim:P50_LOCAL_UPWARD_NINE_PLANE_TRANSPORT_HAS_CONSISTENT_ORIENTED_ENDPOINT` records the two
   positive metric choices and three action/metric orderings. Their endpoint planes agree with positive
   orientation under the frozen convention, but only local tangent planes—not Gamma or K manifolds—are
   transported;
3. `claim:P50_SAMPLED_LOCAL_TRANSPORT_DOES_NOT_ESTABLISH_CUTOFF_STABILITY_OR_GLOBAL_INTERSECTION`
   retains the artificial-stabilizer, sampled-mesh, unsampled-degeneracy, nonlinear-manifold,
   determinant-line, physical-cycle, cutoff, and global-promotion boundaries. Phase 49's formal
   endpoint/portable-adapter debt remains a separate open problem;
4. `open:p50-frozen-m5-gamma-k-local-intersection-continuation` is the next local calculation: continue
   one actual frozen (m=5) Gamma–K candidate over the declared bridge with residual,
   transversality, path, tangent, reflection, and stabilizer controls. The broader component/end census,
   Stokes data, original cycle, and Gate 1 remain open independently.

### Phase 51 reading path

Phase 51 executes one frozen version of the Phase-50 next calculation, but the immutable evaluator
gate prevents promotion of the desired local label:

1. `claim:P51_FROZEN_PHI_PLUS_GAMMA_K_CONTINUATION_REMAINS_INCONCLUSIVE_AT_CSE_NONCSE_RHS_GATE`
   records a valid `6/6` exact and `9/10` numerical run. The sampled phi-plus fine/coarse/reverse paths,
   independent phi-minus reflection path, full-J, path-tangent, endpoint-mutation, orientation, action,
   and first-cap controls pass, while the CSE/non-CSE same-point RHS relative comparison reaches
   `1.690013e-8` against the frozen `5e-10` limit;
2. the failed evaluator predicate is retained as `INCONCLUSIVE`. It is not evidence that a sampled root
   is false and cannot select the protocol's unimplemented contradicted label, which required an
   independent interval, augmented-fold, or local-degree certificate;
3. `open:p51-cse-noncse-clongdouble-rhs-consistency` asks for a narrow evaluator-ordering or
   precision-boundary repair under the same formulas, states, paths, and thresholds. The historical
   Phase-51 result must remain unchanged;
4. `claim:P51_LOCAL_GAMMA_K_RUN_DOES_NOT_ESTABLISH_ROOT_EXHAUSTION_OR_GLOBAL_INTERSECTION` preserves
   unsearched roots, charts, arms, cap reintersections, upward components, Stokes data, relative good
   ends, determinant line, cutoff/continuum limits, original cycle, and global vector. The Phase-50
   open problem and Gate 1 therefore remain open.

### Phase 52 reading path

Phase 52 resolves the narrow static evaluator question but deliberately stops before a continuation
label:

1. `claim:P52_PHASE51_HIDDEN_BINARY64_CSE_CONTRACT_VIOLATION_IS_REPRODUCED` records the actual-callable
   trace: both m=4 and m=5 joint CSE evaluations contain 10 NumPy float64 plus nine Python binary64
   temporaries at every frozen slot. Final complex256 outputs did not satisfy the all-temporaries
   clongdouble contract, so Phase-51 protocol validity is not upheld while its raw bytes remain intact;
2. `claim:P52_ELEMENT_LOCAL_CLONGDOUBLE_RHS_REPAIR_IS_SUPPORTED_ON_SIX_STATIC_SLOTS` records exact
   symbolic identities and six same-state comparisons. The element-local candidate passes the frozen
   `5e-10` gradient and RHS gates; the dtype-correct joint long-namespace candidate remains a typed,
   non-invalidating negative-control `FAIL`;
3. the old `open:p51-cse-noncse-clongdouble-rhs-consistency` is therefore resolved only on the six
   static pinned-platform slots. `open:p53-full-repaired-phase51-continuation-rerun` carries the full
   production replay, with no root, path, threshold, or classification retuning;
4. `claim:P52_STATIC_REPAIR_DOES_NOT_RATIFY_PHASE51_CONTINUATION_OR_GLOBAL_INTERSECTION` keeps every
   unexecuted flow/path/control and every root/component/end, determinant, cutoff, continuum, global,
   physical, and TOE promotion explicitly outside scope. Gate 1 remains open.

### Phase 53 reading path

Phase 53 executes the previously open full replay and narrows, rather than erases, the remaining issue:

1. `claim:P53_REPAIRED_REPLAY_PASSES_INDEPENDENT_REFERENCE_AND_NONBACKEND_CONTROLS` records a complete
   frozen replay: all eight exact checks, 68 roots, 146 retained integrations, reflection, full-J,
   tangent, endpoint mutations, orientations, and every action/first-cap and no-fallback ledger pass;
2. the separately constructed six-slot global-expression reference passes at 80/120 decimal digits,
   including all 54 canonical Hessian probes. The repaired production evaluator is therefore directly
   supported on those slots without treating the saved Phase-51 numerical control as the reference;
3. `claim:P53_FULL_REPLAY_REMAINS_INCONCLUSIVE_AT_PINNED_PHASE51_GLOBAL_NONCSE_BACKEND` preserves the
   sole nonpass: maximum trajectory RHS disagreement with that immutable control is `6.645e-9` against
   `5e-10`. This does not prove which backend operation is defective;
4. `open:p53-full-repaired-phase51-continuation-rerun` was first narrowed to that sole comparison.
   Phase 54 has now executed the six-state diagnostic without ODE, root, trajectory, transport, or
   reintegration; the next section records its narrower result and the separate Phase-55 question.
   Straight arms are not yet authorized;
5. `claim:P53_VALID_LOCAL_REPLAY_DOES_NOT_LICENSE_STRAIGHT_ARM_OR_GLOBAL_PROMOTION` retains every
   root-exhaustion, component/end, determinant, cutoff, continuum, global, physical, and TOE null. Gate 1
   remains `OPEN_PARTIAL_PROGRESS`.

### Phase 54 reading path

Phase 54 resolves the six-state backend question narrowly and opens a distinct trajectory validator:

1. `claim:P54_PHASE51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_IS_CONFIRMED_ON_SIX_STATIC_SLOTS`
   records that `GN_std` and `GN_long` exceed `5e-10`, first at active `m5_raw_gradient`, while the
   independent direct/symbolic 80/120-decimal reference controls pass;
2. `claim:P54_ELEMENT_LOCAL_SCHEDULE_ALONE_IS_SUFFICIENT_ON_SIX_STATIC_SLOTS` records that both
   `EL_std` and `EL_long` pass all 12 selector records. Precision alone does not repair the global
   schedule; changing to the tested element-local order is sufficient only on this finite matrix;
3. `open:p54-pinned-phase51-global-noncse-backend-diagnostic` is resolved only at that static scope.
   No unique primitive floating-point operation or portable correct-rounding result is claimed;
4. `open:p55-p53-trajectory-schedule-transfer-audit` requires six newly regenerated ODEs because the
   fifteen Phase-53 fraction states and authoritative recomputed launch objects were not serialized.
   It uses pinned Phase-50 saddles and the Phase-53 `EL_long` Hessian for explicitly labelled Phase-55
   launch reconstructions, gates their production endpoints/residuals against saved Phase-53 targets at
   `2e-7`, then runs three production `EL_long` and three coherent candidate `EL_std` paths, with no
   root or saddle solve, continuation, reflection, or 68-root replay;
5. `claim:P54_STATIC_ARITHMETIC_ATTRIBUTION_DOES_NOT_RECLASSIFY_PHASE51_OR_PHASE53_OR_LICENSE_GLOBAL_PROMOTION`
   preserves both historical labels and all global, cutoff, continuum, physics, and TOE nulls. Gate 1
   remains `OPEN_PARTIAL_PROGRESS`.

### Phase 55 reading path

Phase 55 runs the bounded trajectory validator but stops at its earlier reconstruction prerequisite:

1. `claim:P55_P50_SADDLE_PINNED_RECONSTRUCTION_MISSES_SAVED_PHASE53_RESIDUAL_AT_LAMBDA_HALF`
   records that all three saved endpoints pass the unchanged `2e-7` coordinate gate, while the
   lambda-half production residual (`2.6752259304644153e-7`) and saved-scalar difference
   (`2.6725817055468002e-7`) do not. Endpoint proximity is therefore insufficient to reproduce the
   saved residual scalar;
2. `claim:P55_ELEMENT_LOCAL_BACKEND_AGREEMENT_IS_DIAGNOSTIC_AFTER_RECONSTRUCTION_NONPASS` retains
   all fifteen trajectory-pair passes, all three endpoint-pair passes, residual-vector differences at
   the `8.22e-11` scale, and the exact Phase-54 aggregate schedule matrix. Under the frozen precedence,
   these are diagnostics and do not qualify schedule transfer after the reconstruction NONPASS;
3. `open:p55-p53-trajectory-schedule-transfer-audit` is resolved by the valid reconstruction-NONPASS
   branch. It does not become a negative theorem about every possible faithful Phase-53 reconstruction;
4. `open:p56-lambda-half-launch-residual-provenance-audit` is now resolved by the terminal Phase-56
   calculation. It reran the Phase-53 saddle algorithm at the one failing root, separated center and
   launch choices in a fixed factorial, and retained both frozen solver profiles without favorable
   selection. The next section records the bounded recovery and its nonauthorization boundary;
5. `claim:P55_RECONSTRUCTION_NONPASS_DOES_NOT_QUALIFY_PHASE56_OR_RECLASSIFY_PHASE53_OR_LICENSE_GLOBAL_PROMOTION`
   keeps the Phase-56 full-replay candidate, historical reclassifications, global signed vector,
   cutoff/continuum limits, physics claim, and TOE claim null. Gate 1 remains
   `OPEN_PARTIAL_PROGRESS`.

### Phase 56 terminal reading path

Phase 56 consumes the sole Ragnarok closeout exception and closes without an offspring phase:

1. `claim:P56_FRESH_PHASE53_ALGORITHM_CENTER_AND_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET`
   records one accepted fresh saddle and fresh/fresh target recovery under both frozen profiles, without
   claiming exact historical Phase-53 bytes;
2. `claim:P56_FROZEN_FACTORIAL_GATE_PATTERN_ASSOCIATES_TARGET_RECOVERY_WITH_FRESH_CENTER` retains the
   full pattern: both P50-center corners have `[true,false,false]`, while both fresh-center corners have
   `[true,true,true]` under both profiles. Center, launch, interaction, and real-`T` records are retained,
   but `causal_or_dominance_label_assigned=false` prevents a general causal theorem;
3. `evidence:p56-lambda-half-launch-provenance-residual-conditioning` preserves 8/8 exact and 8/8
   numerical aggregate passes, one root call, eight ODEs, zero forbidden replay calls, and byte-identical
   authoritative/reproduction stdout. The expected P50-center `NONPASS` records are data inside passing
   completeness and stability aggregates, not hidden failures;
4. `claim:P56_BOUNDED_RECOVERY_DOES_NOT_AUTHORIZE_FULL_REPLAY_PHASE57_OR_GLOBAL_PROMOTION` and
   `policy:ragnarok-circuit-breaker` separate science from operation: the candidate label is descriptive,
   the reconciliation route is `KILL`, full replay and Phase 57 are unauthorized, `next_phase=null`, and
   the Phase-56 execution exception is consumed;
5. `open:p53-full-repaired-phase51-continuation-rerun` remains a scientific question but cannot be
   executed by reviving the killed reconciliation route. Gate 1 remains `OPEN_PARTIAL_PROGRESS`, global
   promotion is `PROHIBITED`, and physics/TOE claims remain null.

## Historical Phase 11 → 15R bridge

The graph now preserves the previously implicit lead-in to Phase 16 as one provenance-safe path:

1. **Phase 11:** exact homogeneous quadratic collar classification. Strong preservation gives the
   `so(1,2)` mixed block plus an arbitrary symmetric momentum-quadratic block; weak preservation adds
   a dilation. The 4D SUGRA origin and observable map remain open.
2. **Phase 12:** one declared collar reduces to an endpoint twist, and an engineered rigid N=1 wall
   exists only with matched multiplet data. A boson-only completion is contradicted; a local-SUGRA
   uplift is unconstructed.
3. **Phase 13A:** the declared principal operator retains formal WKB phases, while two finite-algebra
   branch-exchange surrogates fail. The committed erratum prevents these finite controls from being
   promoted to a physical supercharge theorem.
4. **Phase 14A:** the rolling-goldstino residual and compact-T3 spatial-boundary charge shortcuts fail.
   The selected physical charge and literal branch-superpartner claim remain inconclusive because the
   matter-SUGRA canonical bridge is absent.
5. **Phase 15A:** the frozen artifact order was breached before a valid scientific observation. The
   graph records this as procedural provenance only—no `k2`, tangency or parent-sign conclusion is
   derived from it.
6. **Phase 15R:** a fresh Hohl/Kallosh census independently repairs the scoped question: Kallosh gives
   the only bosonic-sign match, but neither source gives both that sign and the required full off-shell
   coverage. This is a two-source census result, not a literature-wide no-go.

Continue through `reading-path:collar-admissibility-to-single-source-parent-and-tangency` to see how
that valid census motivates, but does not predetermine, Phase 16's independent BGG bosonic-parent and
strict-tangency tests. No node in this path promotes a calculation to a physics or TOE claim.

## Concept map

```mermaid
flowchart TD
  Programme["CPT × Temporal-Folded SUSY programme"]

  Programme --> P16["Phase 16 · BGG parent and tangency"]
  P16 --> C16A["Bosonic kinetic parent<br/>SUPPORTED"]
  P16 --> C16B["Strict off-shell FLRW tangency<br/>CONTRADICTED"]
  P16 --> C16C["Rolling-clock preserved SUSY<br/>CONTRADICTED"]
  C16A -->|"HAS_EVIDENCE · SUPPORTS"| E16A["13 exact checks"]
  C16B -->|"HAS_EVIDENCE · CONTRADICTS"| E16B["6 exact checks"]
  C16C -->|"HAS_EVIDENCE · CONTRADICTS"| E16C["1 exact check"]
  E16A -->|DERIVED_FROM| BGG["BGG hep-th/0005225v1"]
  E16B -->|DERIVED_FROM| BGG
  E16C -->|DERIVED_FROM| BGG

  Programme --> P17["Phase 17 · literal time versus internal sheet"]
  P17 --> Literal["Literal coordinate-time line"]
  Literal --> L1["Support-local half exchange<br/>CONTRADICTED"]
  Literal --> L2["Reflection-composed local charge<br/>CONTRADICTED"]
  Literal --> L3["Ordinary real temporal seam<br/>CONTRADICTED"]

  P17 --> Double["Fundamental doubled sheet"]
  Double --> D1["Bidirectional exchange algebra<br/>SUPPORTED as finite witness"]
  Double --> D2["Doubled-real projector<br/>SUPPORTED as finite witness"]
  D1 --> Gaps["OPEN: action · domain · charge<br/>compatibility · physical anchor"]
  D2 --> Gaps
  D2 --> Pin["OPEN: Pin/Clifford lift<br/>reality · positivity · junction"]

  P17 --> Alt["Alternative fold languages"]
  Alt --> TR["Physical time reversal ≠ tested Q"]
  Alt --> CPT["CPT/Pin sewing · distinct concept"]
  Alt --> SK["SK BRST ≠ particle SUSY"]

  Programme --> P18["Phase 18 · free temporal-seam spectrum"]
  P18 --> T18["Elapsed time alone breaks SUSY<br/>CONTRADICTED"]
  P18 --> Pole18["Free seam moves B/F poles<br/>CONTRADICTED"]
  P18 --> State18["Free seam prepares non-SUSY state<br/>SUPPORTED as finite witness"]
  P18 --> UV18["Sharp local seam is UV admissible<br/>CONTRADICTED"]
  Pole18 --> Frontier18["OPEN: interacting self-energies · persistent carrier<br/>FRW backreaction · Higgs power sensitivity"]
  State18 --> Frontier18
  UV18 --> Frontier18

  Programme --> P19["Phase 19 · closed SUGRA backgrounds"]
  P19 --> Shift19["Shift trajectory → quadratic potential<br/>SUPPORTED"]
  P19 --> Star19["Cecotti trajectory → Starobinsky potential<br/>SUPPORTED"]
  P19 --> Bounce19["Six target-shot 50/55/60 Nacc backgrounds<br/>SUPPORTED"]
  P19 --> Phi19["Time-reflection data leave phi0 free<br/>SUPPORTED"]
  P19 --> R19["Quadratic r below current limit<br/>CONTRADICTED"]
  P19 --> SR19["Starobinsky first-order r below limit<br/>SUPPORTED"]
  Phi19 --> Open19["OPEN: minisuperspace phi0 measure"]
  SR19 --> Pert19["OPEN: S3 state · perturbations · reheating"]

  Programme --> P20["Phase 20 · leading WDW selection control"]
  P20 --> Peak20["Leading envelope selects 5.44<br/>CONTRADICTED"]
  P20 --> Pair20["CPT automatically gives exp(4sI)<br/>CONTRADICTED"]
  P20 --> Int20["Coherent sum only rescales probability<br/>CONTRADICTED"]
  P20 --> F20["Cecotti 5.44 point is F-flat<br/>CONTRADICTED"]
  P20 --> Curv20["Conditional curvature–reheating map<br/>SUPPORTED"]
  Peak20 --> Exact20["OPEN: exact complex WDW state · current · measure"]
  Pair20 --> Sheet20["OPEN: CPT/Pin sheet inner product"]
  F20 --> Tree20["OPEN: tree-level local-SUGRA WDW constraints"]
  Peak20 --> Loop20["OPEN: local-SUGRA one-loop determinant"]

  Programme --> P21["Phase 21 · connected Gaussian seam"]
  P21 --> Base21["R(C=0)=1 baseline<br/>SUPPORTED"]
  P21 --> Force21["Normalization forces R-1<br/>CONTRADICTED"]
  P21 --> Conn21["R-1 is connected<br/>CONTRADICTED"]
  P21 --> Log21["log R is connected generator<br/>SUPPORTED"]
  P21 --> Tail21["Constant-absolute one-flux sum<br/>SUPPORTED as toy"]
  P21 --> Prob21["R-1 alone fixes WDW probability<br/>CONTRADICTED"]
  Tail21 --> Kernel21["OPEN: three-form SUGRA kernel"]
  Prob21 --> Measure21["OPEN: physical flux measure"]

  Programme --> P22["Phase 22 · finite-mode seam density"]
  P22 --> Dens22["Positive-frequency purification<br/>SUPPORTED as finite control"]
  P22 --> Theta22["Graded anti-linear involution<br/>SUPPORTED as toy real structure"]
  P22 --> SK22["Equal-source SK normalization<br/>SUPPORTED as unitarity"]
  P22 --> Zero22["Free noncompact zero mode is trace class<br/>CONTRADICTED"]
  Dens22 --> Full22["OPEN: homogeneous WDW density · local-SUGRA kernel"]
  Zero22 --> Full22

  Programme --> P23["Phase 23 · constrained minisuperspace density control"]
  P23 --> Rig23["Full-lapse distributional rigging map<br/>SUPPORTED"]
  P23 --> Cur23["Positive-frequency local current is pointwise positive<br/>CONTRADICTED"]
  P23 --> Dens23["Supplied compact bridge gives trace-class density<br/>SUPPORTED"]
  P23 --> Sel23["CPT-like reality + zero current select weights<br/>CONTRADICTED"]
  P23 --> Zero23["Quadratic zero root has regular intrinsic clock<br/>CONTRADICTED"]
  P23 --> Dec23["Trace class survives massless decompactification<br/>CONTRADICTED"]
  Rig23 --> Gate23["OPEN: cap-derived regulator-independent density"]
  Dens23 --> Gate23
  Zero23 --> Gate23

  Programme --> P24["Phase 24 · connected Starobinsky interval response"]
  P24 --> Saddle24["Supplied real connected saddle exists<br/>SUPPORTED"]
  P24 --> Resp24["Cross-boundary principal response is nonzero<br/>SUPPORTED"]
  P24 --> Rank24["Constraint-preserving mixed block is rank one<br/>SUPPORTED"]
  P24 --> Mode24["Small singular value is physical<br/>CONTRADICTED"]
  P24 --> Cond24["Fixed-scale scalar Gaussian is conditionally positive<br/>SUPPORTED"]
  P24 --> Full24["Full real-boundary Gaussian is positive<br/>CONTRADICTED"]
  P24 --> Select24["Saddle selects phi0 or a SUSY-breaking scale<br/>CONTRADICTED"]
  Resp24 --> Thimble24["OPEN: gravitational thimble · bulk determinant"]
  Rank24 --> Thimble24
  Cond24 --> Density24["OPEN: physical two-boundary density · entropy"]
  Full24 --> Density24

  Programme --> P25["Phase 25 · lapse saddle and local segment"]
  P25 --> Saddle25["Fixed-boundary lapse saddle<br/>SUPPORTED"]
  P25 --> Local25["Local constant-phase segment<br/>SUPPORTED"]
  P25 --> Fold25["Tracked Dirichlet caustic<br/>SUPPORTED"]

  Programme --> P26["Phase 26 · bounded arm and Airy fold"]
  P26 --> Arm26["Long bounded constant-phase arm<br/>SUPPORTED on recorded sheet"]
  P26 --> Airy26["Real fold Airy scaling<br/>SUPPORTED"]
  P26 --> Real26["Positive real sheet is convergent cycle<br/>CONTRADICTED on recorded sheet"]

  Programme --> P27["Phase 27 · Wick map and zero-lapse endpoint"]
  P27 --> Raw27["Raw fixed-T kernel finite at T=0<br/>CONTRADICTED"]
  P27 --> Res27["Positive half-line is sourced resolvent<br/>SUPPORTED"]
  P27 --> Proj27["Positive half-line is WDW projector<br/>CONTRADICTED"]

  Programme --> P28["Phase 28 · bounded crossings and homogeneous BFV"]
  P28 --> Cross28["Finite cycles cross recorded dual branch<br/>SUPPORTED as bounded geometry"]
  P28 --> Ghost28["Dirichlet ghost removes proper length<br/>CONTRADICTED"]
  P28 --> Pref28["Local lapse Gaussian factor<br/>SUPPORTED conditionally"]
  Cross28 --> Global28["OPEN: global relative homology · coefficient"]
  Ghost28 --> Uniform28["OPEN: zero-lapse-uniform BFV kernel"]
  Pref28 --> Det28["OPEN: full gauge-reduced superdeterminant"]
  Det28 --> State28["OPEN: physical state · density"]
  State28 --> String28["OPEN: string/three-form soft-spectrum completion"]

  Programme --> P29["Phase 29 · zero-lapse distribution and BFV measure"]
  P29 --> Delta29["Frozen kernel tends to delta_flat<br/>SUPPORTED distributionally"]
  P29 --> Pole29["Pointwise zero-lapse limit is finite<br/>CONTRADICTED"]
  P29 --> Measure29["Reduced BFV modulus factor is T-independent<br/>SUPPORTED in frozen gauge"]
  P29 --> Weight29["Inserted N is harmless normalization<br/>CONTRADICTED"]
  P29 --> Wick29["One imaginary rotation damps both signs<br/>CONTRADICTED"]
  P29 --> Density29["Identity distribution is trace-class density<br/>CONTRADICTED"]
  Wick29 --> Param29["OPEN: conformal/BFV uniform parametrix"]
  Delta29 --> WDW29["OPEN: physical endpoint measure · ordering"]

  Programme --> P30["Phase 30 · coupled conformal cycle and determinant line"]
  P30 --> Coupled30["Finite-cutoff local coupled cycle<br/>SUPPORTED"]
  P30 --> Product30["Tested product rotation is sufficient<br/>CONTRADICTED"]
  P30 --> Relative30["Declared-measure relative magnitude<br/>SUPPORTED at recorded cutoffs"]
  P30 --> Parity30["Bare sign is cutoff independent<br/>CONTRADICTED"]
  P30 --> Sheet30["One holomorphic sheet works on both real sides<br/>CONTRADICTED"]
  P30 --> Ray30["Pointwise shifted-ray limit fixes integer coefficient<br/>CONTRADICTED"]
  Coupled30 --> Param29
  Parity30 --> Param29
  Sheet30 --> Param29
  Ray30 --> Param29

  Programme --> P31["Phase 31 · homogeneous canonical/BFV hybrid"]
  P31 --> Schur31["Canonical momentum Schur reduction<br/>SUPPORTED"]
  P31 --> Sign31["Unreduced canonical sign stable<br/>SUPPORTED at recorded cutoffs"]
  P31 --> Rel31["Nonzero quartet relative cancellation<br/>SUPPORTED in same regulator"]
  P31 --> Bare31["Bare bosonic sign fixes determinant line<br/>CONTRADICTED"]
  Bare31 --> Det28

  Programme --> P32["Phase 32 · lapse bypass and projected crossing"]
  P32 --> Half32["Positive half-line has interior crossing<br/>CONTRADICTED: endpoint contact"]
  P32 --> Low32["Below-origin full line projected crossing<br/>SUPPORTED · coordinate sign +1 is conditional"]
  P32 --> Up32["Upper bypass has same crossing<br/>CONTRADICTED on tracked branch"]
  P32 --> Mom32["Lower-bypass momentum cycle converges<br/>SUPPORTED locally"]
  P32 --> Maslov32["Analytic transport alone fixes real normalization<br/>CONTRADICTED · orientation gluing missing"]
  Low32 --> Global28
  Up32 --> Pin32["OPEN: CPT/Pin lapse-class selection"]
  Mom32 --> Det28

  Programme --> P33["Phase 33 · simple-fold Airy gate"]
  P33 --> Fold33["Transverse simple fold and Airy scale<br/>SUPPORTED"]
  P33 --> Lapse33["Fold is an extra lapse saddle<br/>CONTRADICTED"]
  P33 --> VV33["Separate Van Vleck divergence forces exact divergence<br/>CONTRADICTED in canonical fold"]
  P33 --> Rank33["Local regularity selects one Airy kernel<br/>CONTRADICTED: rank two"]
  P33 --> Patch33["Fold patch adds Phase-32 crossing<br/>CONTRADICTED locally"]
  Fold33 --> AiryOpen33["OPEN: cycle · amplitude · global continuation"]
  Rank33 --> AiryOpen33
  Patch33 --> Global28

  Programme --> P34["Phase 34 · reduced fold branches"]
  P34 --> In34["Incoming real segment aims at fold<br/>SUPPORTED on 47 points"]
  P34 --> Out34["Conjugate directed branches beyond fold<br/>SUPPORTED through Re T=13"]
  P34 --> Jac34["Sampled arm has another Jacobi zero<br/>CONTRADICTED at frozen points"]
  P34 --> Cross34["Bounded arms add Phase-32 crossing<br/>CONTRADICTED on tracked bases"]
  In34 --> Join34["OPEN: oriented Airy connection · determinant line"]
  Out34 --> Join34
  Join34 --> Global28

  Programme --> P35["Phase 35 · relative reduced determinant line"]
  P35 --> Det35["Sampled endpoint det line transportable<br/>SUPPORTED through Re T=13"]
  P35 --> Fold35["Recorded near-fold phase ~ -pi/2<br/>SUPPORTED at finite resolution"]
  P35 --> Pair35["Conjugate reduced endpoint phases cancel<br/>SUPPORTED relatively"]
  P35 --> Abs35["Sampled transport fixes absolute Maslov phase<br/>CONTRADICTED as sufficient data"]
  Det35 --> Open35["OPEN: physical Van Vleck · Maslov · full BFV"]
  Fold35 --> Open35
  Pair35 --> Open35
  Abs35 --> Open35
  Open35 --> Global28

  Programme --> P36["Phase 36 · declared local Airy bases"]
  P36 --> Basis36["Separate CW/CCW basis identities<br/>SUPPORTED exactly"]
  P36 --> Root36["Both tracked root-sheet laterals regular<br/>SUPPORTED on three finite radii"]
  P36 --> Select36["Phase 32 + 35 alone select one arm<br/>CONTRADICTED within local gates"]
  Basis36 --> Warn36["Different first dual bases<br/>not one transported physical dual"]
  Root36 --> Open36["OPEN: original cycle · hard amplitudes · full BFV"]
  Select36 --> Open36
  Warn36 --> Open36
  Open36 --> Global28

  Programme --> P37["Phase 37 · closed local fold holonomy"]
  P37 --> Root37["Tracked BVP root cover exchanges<br/>SUPPORTED on three finite loops"]
  P37 --> Half37["Reduced sampled half-form L²=-I<br/>SUPPORTED conditionally"]
  P37 --> Basis37["Root monodromy breaks Phase-17 equivalence<br/>CONTRADICTED in finite-fiber control"]
  Root37 --> Typed37["Root ≠ Airy solution ≠ relative cycle"]
  Half37 --> Guard37["Bosonic reduced half-form<br/>≠ Pin/Pfaffian line"]
  Basis37 --> Open37["OPEN: original cycle · hard CFU · full BFV/Pfaffian"]
  Typed37 --> Open37
  Guard37 --> Open37
  Open37 --> Global28

  Programme --> P38["Phase 38 · Gate-1 identifiability and bounded ledger"]
  P38 --> Data38["Recorded data do not license inverse reconstruction<br/>SUPPORTED boundary"]
  P38 --> Map38["Root swap replaces cycle map<br/>CONTRADICTED"]
  P38 --> Cond38["Conditional Gamma0 → two local arms<br/>SUPPORTED exactly"]
  P38 --> Bound38["Sampled projected disjointness to Re T=16<br/>SUPPORTED on bounded table"]
  P38 --> Global38["Bounded ledger fixes global vector<br/>CONTRADICTED"]
  Data38 --> Gate1_38["OPEN Gate 1 · physical joint cycle and signs"]
  Map38 --> Open38["OPEN: explicit joint action · tangent frames · ends"]
  Bound38 --> Open38
  Global38 --> Gate1_38
  Gate1_38 --> Open38
  Cond38 --> Gate2_38["Gate 2 hard CFU may run conditionally<br/>physical promotion still depends on Gate 1"]

  Programme --> P39["Phase 39 · frozen m=2 local joint pilot"]
  P39 --> Saddle39["Positive-T discrete joint saddle<br/>SUPPORTED at frozen m=2"]
  P39 --> Local39["Two cap-piece R6 signs = +1<br/>SUPPORTED locally"]
  P39 --> Global39["Two local signs fix global vector<br/>CONTRADICTED"]
  Local39 --> Guard39["Finite-radius/time K-chart patch<br/>not exact complete upward cycle"]
  Global39 --> Gate1_39["OPEN Gate 1 · chain sum, ends, Stokes, stability"]
  Guard39 --> Gate1_39

  Programme --> P40["Phase 40 · frozen m=3 odd-response and local R10 pilot"]
  P40 --> Odd40["Rank-one phi source gives sampled<br/>anchor-subtracted odd response · SUPPORTED"]
  P40 --> Geometry40["Fixed flow mobility ≠ delta-dependent<br/>Morse launch ellipsoid"]
  P40 --> Local40["Five sampled local R10 signs = +1<br/>SUPPORTED locally"]
  P40 --> Boundary40["Local records do not license<br/>chain/global inference · SUPPORTED boundary"]
  Geometry40 --> Local40
  Local40 --> Boundary40
  Boundary40 --> Gate1_40["OPEN Gate 1 · m=4/cutoff, full chain,<br/>ends, Stokes, stability"]

  Programme --> P41["Phase 41 · frozen m=4 two-source local R14 control"]
  P41 --> Rank41["Two-source odd susceptibility<br/>stable numerical rank two · SUPPORTED"]
  P41 --> Local41["Five local R14 signs = +1<br/>SUPPORTED as computed candidates"]
  P41 --> Tangent41["Frozen u2 tangent plateau fails<br/>source robustness INCONCLUSIVE"]
  P41 --> Boundary41["Cross-cutoff comparison descriptive;<br/>global promotion unlicensed"]
  Local41 --> Tangent41
  Tangent41 --> Boundary41
  Boundary41 --> Gate1_41["OPEN Gate 1 · full chain, census,<br/>Stokes, ends, physical cycle"]

  Programme --> P42["Phase 42 · fixed-root tangent diagnosis"]
  P42 --> Cause42["Solver noise + old step-pair evidence<br/>SUPPORTED at phi/a only"]
  P42 --> RHS42["Stable local Hessian-action anomaly<br/>SUPPORTED · not bug proof"]
  P42 --> Hom42["Normalized local homotopy<br/>sufficient sign certificate"]
  P42 --> Ref42["Reference tangent<br/>INCONCLUSIVE"]
  Cause42 --> Ref42
  RHS42 --> Ref42
  Hom42 --> Ref42
  Ref42 --> Gate1_42["OPEN Gate 1 · independent tangent arbitration,<br/>full chain, census, Stokes, ends"]

  Programme --> P43["Phase 43 · frozen local high-precision arbitration"]
  P43 --> Ref43["Independent local reference<br/>CORROBORATED at 90/90"]
  P43 --> RHS43["NumPy64 source tolerance crossed<br/>SUPPORTED at 13/90 · not defect proof"]
  P43 --> FD43["All-33 finite-difference explanation<br/>CONTRADICTED · 28/33 supported"]
  P43 --> Boundary43["Integrated tangent and ODE<br/>NOT TESTED · global promotion prohibited"]
  Ref43 --> RHS43
  RHS43 --> FD43
  FD43 --> Boundary43
  Boundary43 --> Gate1_43["OPEN Gate 1 · arithmetic provenance first,<br/>then separately frozen tangent reintegration"]

  Programme --> P44["Phase 44 · NumPy64 local RHS error decomposition"]
  P44 --> Formula44["Declared source and independent formula<br/>EXACTLY IDENTICAL"]
  P44 --> Mixed44["Mixed nonexclusive rounding contributions<br/>90/90 complete telescopes"]
  P44 --> Cover44["Declared forward model covers<br/>13/13 mismatches and 77/77 controls"]
  P44 --> Boundary44["Integrated tangent and global cycle<br/>NOT TESTED · no rewrite authorized"]
  Formula44 --> Mixed44
  Mixed44 --> Cover44
  Cover44 --> Boundary44
  Boundary44 --> Gate1_44["OPEN_PARTIAL_PROGRESS Gate 1 · separately frozen<br/>integrated-tangent stability remains next"]
```

The two supported Phase 17 nodes are distinct witnesses. One proves a finite doubled exchange algebra; the other proves a finite real sheet-mixing projector. The graph does not claim that they already coexist in one theory.

Phase 18 makes a different separation: an instantaneous free canonical seam can alter occupations and Wightman data without changing the common post-post retarded pole. This is a state-preparation witness, not a permanent soft-mass mechanism, and the unsmoothed local scalar kick is UV inadmissible.

Phase 19 adds gravity only at the homogeneous classical-background level. It verifies two exact one-field SUGRA reductions and six conditional closed-FRW shooting solutions. The rows prove existence after choosing a target \(N_{\rm acc}\); they do not show that CPT/Pin selects \(\phi_0\), construct a quantum state, or predict a parameter-free universe size.

Phase 20 tests one leading selection proposal rather than solving the exact WDW problem. The constant-field de Sitter envelope is monotone at the Phase 19 benchmark under both the standard \(e^{2sI}\) history weight and a separately assumed independent-pair \(e^{4sI}\) joint probability. Coherent phases, a WDW current, the sheet inner product, the exact complex saddle, and local-SUGRA loop sectors remain outside that result.

Phase 21 replaces a guessed pair weight by an explicit positive finite Gaussian ratio. It proves that normalization identifies a unit no-seam term, but also proves that subtracting it is not forced and that \(R-1\) is not the connected functional. The one-flux convergence witness remains a toy because the kernel, sector measure, WDW inner product/current, and joint \((n,\phi)\) peak are not derived.

Phase 22 constructs a different finite witness: a normalized thermofield-double-like purification of one
supersymmetric oscillator. Its Gibbs covariance, graded occupation-space real structure, DtN density
correlation, and equal-source SK trace identity are exact. Finite temperature has positive energy, so this
is not an unbroken positive-Hamiltonian SUSY vacuum; the toy involution is not a spacetime Pin lift. The
same noncompact free ansatz fails at \(\omega=0\), leaving the constrained homogeneous WDW and
gravitino–Goldstino–ghost completions open.

Phase 23 moves one step into a constrained KG-type minisuperspace normal form. Full-real-lapse averaging
defines a distributional rigging map, not a bounded kinematical projector, and a chosen clock/frequency
orientation gives a positive integrated norm even though an exact two-mode local current becomes negative.
A separate supplied bridge \(B_L=e^{-L\sqrt h}\) yields a positive trace-class density only at the compact
regulator. Group averaging does not derive \(L\) or the weights, CPT-like reality plus zero signed current
does not select them uniquely, the quadratic \(E=0\) root is singular, and the massless box loses trace
class as it is decompactified. The continuous seed calibration and compact density calibration remain
separate; neither is the closed Starobinsky/Cecotti cap or a local-SUGRA/BRST seam state.

Phase 24 replaces the disconnected control by one supplied real connected Starobinsky
\(S^3\times I\) saddle. Its Hamilton principal function has a nonzero cross-boundary response, and
constraint-preserving endpoint variations leave one nonzero mixed homogeneous direction; the second
singular value converges away along the Hamilton–Jacobi null direction. Holding the proper length fixed
is a distinct off-constraint mutation and restores full mixed rank. At fixed boundary scale factors, a
supplied flat scalar measure gives a positive conditional two-real-mode Gaussian, but the complete
real-boundary Hessian and the formal real-contour scalar Schur complement are indefinite. These finite
boundary-response signs are not the gauge-fixed bulk Morse spectrum. No lapse/conformal thimble,
primed determinant, physical factorization, trace-class density, entropy, initial-amplitude selection,
or SUSY-breaking scale follows from this benchmark.

Phase 25 makes the proper length dynamical at fixed boundary data. The supplied Phase-24 interval is a stationary lapse saddle with negative lapse curvature, so the convergent local tangent for `exp(-W)` is imaginary rather than real. One reflection-symmetric real branch reaches a simple Dirichlet caustic, while a distinct local complex branch keeps `Im W` fixed. These are local and bounded statements, not a global thimble decomposition.

Phase 26 continues one analytic upper arm far beyond the local segment, through a turn in its `T`-plane projection and onto a bounded return segment, with a conjugate lower control. A separate real Dirichlet fold has nonzero `W_T` and generic Airy scaling. The recorded cutoff is not proved to be an endpoint, and the positive real tracked sheet is not the recorded convergent relative cycle.

Phase 27 fixes the declared Wick map and resolves the leading equal-boundary raw fixed-lapse asymptotics. The two-coordinate Van Vleck magnitude behaves as `1/|T|`, while the positive lapse half-line is a sourced resolvent rather than the full-line constraint projector. This raw endpoint statement is deliberately not a claim about an endpoint-completed gauge-reduced BFV kernel.

Phase 28 continues the bounded upper arm past its imaginary-lapse turn, records four finite constructed crossings with one real dual branch, and adds an Abelian Euclidean-continued homogeneous BFV control. Intrinsic neck clocks are singular, `p_a` is locally regular, and Dirichlet ghosts have no zero mode, yet proper length remains BRST invariant. The determinant `2` is scheme-normalized and the local imaginary Gaussian factor is conditional on the still-open global coefficient and full superdeterminant. The cited string/three-form sources only define a completion route: direct three-form sources motivate F-type breaking, D-type breaking needs a separate vector/gauging sector, and no temporal-seam sector rule or soft spectrum has been derived.

Phase 29 resolves one narrow endpoint question at leading quadratic order. With the frozen kinetic matrix and a declared local flat `da dphi` endpoint measure, the normalized real-lapse Fresnel kernel tends distributionally to the identity delta kernel even though its equal-endpoint pointwise amplitude still behaves as `1/N`. Fixed-parameter BFV rescaling leaves a T-independent nonzero-mode ghost normalization and a gauge-invariant proper-time modulus; inserting an extra lapse power changes the spectral object. The indefinite kinetic form prevents one imaginary-lapse rotation from damping both directions. None of this derives the physical WDW endpoint measure, all-orders uniform kernel, conformal contour, full determinant, global PL coefficient, or trace-class density.

Phase 30 supplies the first finite-cutoff local contour that treats the homogeneous conformal field direction and the lapse fluctuation together. The Schur-shifted field fiber cancels the mixed block and gives a positive real quadratic form at every tested cutoff, whereas the tested direct-product rotations retain one negative direction. A declared midpoint configuration measure also stabilizes one relative endpoint magnitude at `1.01502655703`; the naked Hessian ratio and absolute determinant sign do not have the same status, and the latter alternates with cutoff parity. On the real lapse axis, `1/|N|` identity normalization requires Maslov/determinant-line gluing that a single holomorphic `1/N` sheet cannot provide. This is a local homogeneous quadratic result only: Phase 30 evaluates no new BFV ghost complex and no full phase-space BFV super-Hessian, primed superdeterminant, global upward-cycle census, integer PL coefficient, or physical state.

Phase 31 lifts that finite-cutoff control to an unreduced canonical midpoint system and adds all declared
nonzero homogeneous alpha=0 BFV quartets. Momentum Schur reduction is exact, and the proper-time-gauge
canonical block has stable positive sign over the recorded odd/even cutoffs. The nonzero quartet factors
are background independent in the finite-dimensional block identity and drop out of a same-regulator
benchmark/reference ratio, but the bare full bosonic BFV sign still alternates. Absolute contour phases,
zero-mode normalization, gauge-parameter independence, continuum reduction, and inhomogeneous fields are
not computed. The bounded `p_a` scan is only a local clock diagnostic because endpoint polarization changes.

Phase 32 then declares and compares different lapse objects rather than treating them as one contour. The
causal positive half-line has a singular endpoint contact, not an ordinary interior intersection. A full
real lapse contour separately declared to pass below zero has one recorded finite-radius projected
lapse-base crossing; its coordinate sign `+1` is conditional on the declared orientations. The upper bypass
misses that positive-real dual. The principal momentum lift is locally convergent, but its negative-real
normalization needs orientation-line gluing not derived as a Maslov index. Five sampled angles on each of
four arcs do not prove continuous continuation between samples. This result assigns neither a signed
full-joint local intersection nor a global coefficient, and complex conjugation alone does not construct a
CPT/Pin bra--ket lift selecting the contour class.

Phase 33 resolves the recorded positive-real caustic more sharply. Two actual branches give last-four-point
log slopes consistent with the `delta^(3/2)` action gap, linear invariant Airy action scale, square-root
soft Jacobi mode, and quarter-power separate-saddle divergence, together with opposite endpoint-determinant
signs. The quoted ratios are finite-resolution measurements, not error-certified asymptotic coefficients.
This is not another lapse saddle because `W_T` is nonzero. The declared local Airy ODE has two regular
independent solutions, so local finiteness removes no contour ambiguity and does not establish that either
basis exhausts admissible lifted gravitational cycles. An off-real canonical-map/exponent branch, relative
cycle, and oriented determinant line must still determine the contour/Stokes combination, while the
analytic even/odd amplitude is separate data. A radius-one fold chart is locally disjoint from the Phase-32
contour pieces, but no arm outside that chart has been censused. The global coefficient, uniform
gauge-reduced kernel, physical endpoint product, and trace-class state therefore remain open.

## Core distinctions

| Distinction | Meaning in this graph |
| --- | --- |
| Bosonic parent vs off-shell SUSY truncation | Recovering the target bosonic kinetic block does not make a discarded-field locus SUSY-tangent. |
| Gauge symmetry vs preserved background SUSY | A rolling background can have no nonzero Killing parameter while the underlying local SUSY gauge symmetry remains present. |
| Coordinate-time half vs internal sheet | `t<0` and `t>0` are supports on one translated line; a doubled sheet is a new internal degree of freedom carrying complete multiplets. |
| Linear reflection vs physical time reversal | Bare history pullback is complex-linear; Wigner time reversal is anti-complex-linear. Neither fact turns the operation into a conventional fermionic charge. |
| Finite algebra witness vs physical theory | Matrix closure or projector rank is necessary evidence for a route, not an action, self-adjoint domain, conserved charge, or observable. |
| SK BRST vs particle SUSY | SK charges are ghost-odd cohomological controls; the checked signed contour spectrum is not a positive physical Hamiltonian. |
| Elapsed time vs SUSY-breaking dynamics | Conserved evolution with `[H,Q]=0` does not break SUSY. A seam can fail to preserve a SUSY domain, but that is a property of the seam data, not of time passing. |
| Free canonical temporal seam (`concept:free-canonical-temporal-seam`) | An instantaneous standard Cauchy-data map preserves scalar symplectic flux or the finite-mode fermion CAR while leaving the future bulk operators unchanged. |
| Initial state vs spectral pole (`concept:initial-state-versus-spectral-pole`) | Occupations, anomalous correlators, and Wightman functions can remember a seam while the free retarded commutator keeps the unchanged bulk pole. |
| One-time excitation vs persistent carrier (`concept:persistent-susy-breaking-carrier`) | A non-SUSY state does not by itself supply a nondecaying `F`/`D` order parameter, memory sector, vacuum selection, or bulk soft spurion. |
| Sharp kick vs admissible smoothing | The spatially local delta kick has linearly divergent number density and quadratically divergent energy density; the Gaussian result is only a bounded Born/numerical control, not a constructed UV completion. |
| Potential scale vs geometric Hubble rate | \(H_V^2=V/3\) is used in the transverse SUGRA masses; the closed-FRW \(H(t)^2\) vanishes at the symmetric bounce. |
| Background existence vs initial-amplitude selection | Target shooting can prove a branch exists while leaving \(\phi_0\) unselected. A perturbation Gaussian state and a minisuperspace/background measure are separate constructions. |
| \(N_{\rm acc}\) vs \(N_*\) | Bounce-to-end accelerated e-folds are not automatically the CMB pivot e-fold count without reheating and scale matching. |
| Standard history vs independent-pair probability | \(e^{2sI}\) is the recorded standard semiclassical one-history weight. \(e^{4sI}\) is a conditional joint probability for an independently factorized pair; CPT sewing alone does not derive it. |
| Envelope monotonicity vs exact WDW no-go | A nonzero slope in the constant-field de Sitter control rules out a peak in that envelope, not every complex Starobinsky saddle, WDW measure, sheet overlap, or loop-corrected local-SUGRA state. |
| Constant normalization vs coherent interference | A constant factor cannot move an envelope slope, but an order-one phase-dependent \(\cos^2S\) term can create nodes and local extrema until a current/decoherence prescription is supplied. |
| Conditional conversion vs prediction | Reproducing \(\Omega_{K0}(T_{\rm reh})\) after fixing \(N\), \(M_s\), \(w_{\rm reh}\), entropy, and late-time inputs does not mean the seam selected any of them. |
| Unit baseline vs forced subtraction | Decoupled-sheet normalization gives \(R(0)=1\); using \(R-1\) additionally chooses to exclude the zero-insertion term. |
| Remainder vs connected generator | \(R-1=\exp(\log R)-1\) includes products of connected rings; \(\log R\) is the linked-cluster generator. |
| Finite determinant vs universe probability | A regulated or summable positive sequence still needs a physical sector measure, WDW current/inner product or decoherence functional before it can be called a probability. |
| Gibbs covariance vs unbroken vacuum SUSY | \([\rho,Q]=0\) and equal multiplet weights do not make a finite-temperature state a zero-energy SUSY vacuum; Phase 22 checks \(\langle H\rangle>0\). |
| Occupation-space real structure vs Pin lift | The graded anti-linear toy involution fixes the displayed finite state, but omits spacetime Clifford reflection, spin structure, reflection square, and local-SUGRA gluing. |
| DtN amplitude vs density covariance | If the Euclidean amplitude is \(e^{-q^TKq/2}\), the probability density has covariance \((2K)^{-1}\), not \(K^{-1}\). |
| Free noncompact zero mode vs inflaton minisuperspace | Divergence of the \(L^2(\mathbb R)\) free oscillator limit does not decide a compact mode or an interacting constrained \((a,\phi)\) wavefunction. |
| Distributional rigging map vs bounded projector | The full-real-lapse delta sequence imposes one constraint distributionally; its divergent supremum prevents treating it as an ordinary bounded kinematical projector or density matrix. |
| Induced norm vs signed local WDW current | A branch/clock choice can give a positive integrated physical norm while the conserved local Klein–Gordon current remains pointwise sign-indefinite. |
| Constraint rigging vs state-preparation bridge | Group averaging places data on the constraint shell. The separately supplied \(B_L=e^{-L\sqrt h}\) fixes relative weights; the first operation does not derive the second. |
| Compact trace class vs continuum limit | The supplied density is trace class on the compact spectrum for \(L>0\), but the massless box partition grows as \(R/(2L)\) under decompactification. |
| Quadratic zero root vs regular clock gauge | At \(E=0\), the quadratic shell root is double, the regulated integral diverges, and the intrinsic-clock Faddeev–Popov determinant vanishes. Linearizing the constraint preselects an orientation. |
| Connected boundary response vs quantum entanglement | A nonzero mixed Hessian of the Hamilton principal function proves nonfactorizing classical boundary response; it does not supply a bipartite Hilbert-space state, density operator, or entanglement measure. |
| Constraint-preserving vs fixed-length Hessian | Solving the proper length as a modulus preserves the Hamiltonian constraint and exposes Hamilton–Jacobi null directions. Freezing the length during endpoint variation is a distinct off-constraint mutation and can change the mixed rank. |
| Conditional fixed-scale Gaussian vs physical gravitational state | Positivity of the scalar subblock after fixing both boundary scale factors and supplying a flat measure is a conditional diagnostic, not positivity or trace class of the full gravitational kernel. |
| Boundary-response Hessian vs bulk Morse spectrum | Signs of the finite boundary Hessian or a formal Schur complement do not determine the gauge-fixed primed bulk fluctuation spectrum, thimble intersection number, ghost determinant, or contour phase. |
| Lapse saddle vs Dirichlet caustic | `W_T=0` is stationarity in the proper-length modulus; a singular fixed-length endpoint map can occur elsewhere with nonzero `W_T`. |
| Separate Van Vleck divergence vs uniform fold kernel | The two isolated saddle proxies can diverge as `delta^(-1/4)` while the canonical Airy equation has regular solutions. That local fact does not establish finiteness of an uncomputed physical measure or amplitude. |
| Local Airy regularity vs cycle selection | Ai and Bi are both regular and independent at the fold. A physical contour/Stokes multiplier and its analytic amplitude require the original relative cycle and oriented determinant line. |
| Local fold chart vs global dual census | Disjointness of one fold chart from the recorded lapse pieces excludes a crossing only there; it does not enumerate arms after they leave the chart or other complex sheets. |
| Bounded thimble arm vs global relative cycle | Constant phase and monotone `Re W` on a monitored segment do not determine its asymptotic endpoint, original contour, Stokes jumps, or integer coefficient. |
| Raw fixed-T kernel vs BFV kernel | The Phase 27 `1/|T|` Van Vleck behavior is unreduced; endpoint factors, ghosts, zero modes, and the uniform full determinant can change the gauge-reduced kernel. |
| Positive half-lapse resolvent vs projector | A sourced positive-half-line spectral object is not the full-line group-averaged constraint distribution. |
| Bounded crossing vs global intersection number | Four declared finite cycle crossings are local geometry, not the relative-homology coefficient of the physical original contour. |
| BFV ghost zero mode vs lapse negative mode | The chosen Dirichlet ghost operator has no zero mode while proper length remains BRST invariant, so the local lapse negative direction is not automatically ghost-cancelled. |
| String completion vs seam derivation | Three-form/flux, membrane, boundary-state, and modular structures constrain a possible UV completion but do not derive the temporal seam or sector weights; the direct three-form route is F-type, while D-type breaking needs extra vector/gauging data. |
| Pointwise pole vs distributional identity | The normalized leading kernel can retain a coincident-point `1/N` pole while converging to `delta_flat` on test functions under the declared local endpoint measure. |
| Fixed-parameter BFV modulus vs standalone ghost determinant | Coordinate-length ghost scaling is canceled by the matching rescaling and gauge-condition delta; proper time remains a modulus with a T-independent reduced factor in the frozen control. |
| Lapse-weight insertion vs operator object | An inserted factor of `N` changes a half-line resolvent to a double pole and a full-line constraint delta to a derivative distribution; it is not a neutral subtraction. |
| Real-lapse Fresnel vs conformal contour | Oscillatory distributional normalization on real lapse does not solve the opposite-sign conformal damping problem or choose the gravitational thimble. |
| Root-cover vs Airy-solution vs relative-cycle monodromy | A permutation of local stationary roots, analytic continuation of the exact Ai/Bi solution space, and a Gauss--Manin map on specified relative cycles act on different typed spaces even when matrix representatives are conjugate. |
| Closed conjugacy invariant vs sheet label | Local root names and off-diagonal phases are trivialization dependent; same-basepoint trace, determinant, characteristic polynomial, and central square survive constant rephasing, subject here to the sampled-lift caveat. |
| Reduced bosonic half-form vs Pin/Pfaffian line | The sampled inverse square root of one endpoint-Jacobi block omits the fermion operator, spectral flow, Clifford reflection data, ghost and other modes, common domain, anomaly test, and BFV/BV quantum structure. |

## Method policy — no privileged exception

`policy:recursive-self-application-audit` stores the user-requested lesson inspired by Greg Egan's
recursive mode of thought. It does not treat the novel's ideas or their interpretation as physics
evidence. Its self-audit verdict is `NARROW`: literal recursion is required only when type-correct;
otherwise the policy audits the justification for a privilege-bearing edge. The active audit is:

1. classify the proposed `A → B` bridge and quotient gauge/basis redundancy;
2. freeze its exact conditions;
3. seek a minimal counterexample;
4. remove `A` and reverse the arrow;
5. perform type-correct self-application or a meta-audit of the preferred branch;
6. demand a basis-independent invariant and discriminating observable;
7. check whether the result silently changed the original definitions;
8. finish with `KEEP`, `NARROW`, `BRANCH`, `EQUIVALENCE`, `KILL`, or an explicit `OPEN`.

Applied to the current frontier, “global selection is required” becomes two questions: what derives the
relative coefficients, and must one arm be selected at all? A convenient lapse bypass, Airy contour, or
sector prior has no privileged status. The result may be one invariant cycle, a fixed CPT-real sum,
physically distinct underweighted branches, or an observational equivalence class. The two concepts
`concept:invariant-difference-amplitude-and-record` and
`concept:recursive-objectivity-and-world-resistance` record this deeper boundary. The central philosophy
and intuitive meditation document them without evidential polarity. The policy is attached to the
programme through `GOVERNED_BY`; it cannot support or contradict a scientific claim. Its SYMPOSIUM bridge
is deliberately `UNRESOLVED` because no authorized external UID or writer is available.

## Programme policy — ordered five-gate advancement

`policy:ordered-five-gate-advancement` hash-tracks the user-mandated route in
[`ICE_ORDERED_FIVE_GATE_PROGRAMME_2026-08-20.md`](../../docs/decisions/ICE_ORDERED_FIVE_GATE_PROGRAMME_2026-08-20.md).
It turns the large Phase-37 frontier into five explicit typed debts and records which output may support
which later inference. It is workflow metadata, not preregistration, evidence, or a forecast that any gate
will succeed. The policy is itself `GOVERNED_BY` the recursive self-application audit: if a more direct
formulation changes the dependency structure, the order must be justified and revised rather than treated
as a natural law. The five gate nodes stay `OPEN`; no scientific claim state changes in this integration.

## IDs and claim states

IDs use stable semantic prefixes: `programme:`, `phase:`, `concept:`, `claim:`, `evidence:`, `scope:`, `open:`, `source:`, `artifact:`, and `policy:`. `edge:` IDs identify directed relations; `result:` IDs identify observed run snapshots.

Claim `state` has the following local meaning:

| State | Meaning |
| --- | --- |
| `SUPPORTED` | The attached evidence supports the claim only inside its declared scope. |
| `CONTRADICTED` | The attached evidence contradicts the claim inside its declared scope. |
| `HISTORICAL` | Retained for provenance. Read its summary and attached evidence rather than projecting a current global verdict onto it. |

Historical nodes are retained without turning their `HISTORICAL` state into a new verdict:

| Historical claim ID | Recorded interpretation |
| --- | --- |
| `claim:P15R_BOSONIC_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS` | Supporting evidence inside the frozen two-source census; not a literature-wide existence theorem |
| `claim:P15R_FULL_OFFSHELL_SINGLE_SOURCE_PARENT_EXISTS_IN_FROZEN_CENSUS` | Contradicting evidence only inside that census |
| `claim:P14A_LITERAL_BRANCH_SUPERPARTNER` | Inconclusive/unconstructed; Phase 17 tests sharper coordinate-time versions |

## Edge semantics

Every edge is read in stored `from → relation → to` direction.

| Relation | Meaning |
| --- | --- |
| `PART_OF` | Node belongs to a programme or phase. |
| `ABOUT` | Claim concerns a reusable concept. |
| `HAS_EVIDENCE` | Claim points to an evidence group; the edge's `polarity` is `SUPPORTS` or `CONTRADICTS`. |
| `DEFINED_IN` | Evidence checks are implemented in an executable. |
| `RECORDED_IN` | Run evidence is persisted in a result snapshot. |
| `DERIVED_FROM` | Evidence uses a source directly in the calculation. |
| `DOCUMENTED_BY` | Claim has a human-readable report. |
| `DOCUMENTS` | Artifact documents a source or phase. |
| `IMPLEMENTS` | Artifact implements a phase calculation. |
| `RECORDS` | Artifact records a phase result. |
| `VALID_WITHIN` | Claim is bounded by a scope node. |
| `BLOCKED_BY` | Claim cannot be promoted until the named open problem is solved. |
| `MOTIVATES` | A terminal scoped result suggests a distinct follow-up; solving it does not reverse that result. |
| `EXTENDS` | New result adds a scoped case without overwriting an older claim. |
| `FOLLOW_UP_TO` | New claim tests a continuation of an older target. |
| `CONTRASTS_WITH` | New claim sharpens a distinction from an older one. |
| `CITES` | Claim, concept, or open problem cites a primary or technical source for framing or a boundary. |
| `USES_TOOLING` | Programme points to a tooling reference. |
| `GOVERNED_BY` | Repository workflow relation; never scientific evidence. |

`HAS_EVIDENCE` deliberately runs claim → evidence. A `PASS` inside the evidence means the check succeeded; only edge `polarity` says whether that result supports or contradicts the claim. There is no `SUPERSEDES` edge in the current vocabulary, so no claim should be treated as silently erased.

## Scope ledger

| Scope ID | Included | Important exclusion |
| --- | --- | --- |
| `scope:p15r-frozen-two-source-census` | Hohl and Kallosh as evidential candidates | ADM is only a zero-weight internal control; no literature-wide theorem |
| `scope:p16-bosonic-kinetic` | `(X,T,Y)` velocity block after exactly one endpoint removal | Lapse and algebraic auxiliary constraints |
| `scope:p16-strict-flrw-tangency` | Exact clean-point counterexample on the declared off-shell FLRW/gamma-trace locus | Other truncations or a full all-fermion residual |
| `scope:p16-rolling-clock` | Bosonic `W=0`, `F=0`, nonzero real proper-time rate and Lorentzian-conjugate parameters | Other potentials, auxiliary choices, or Killing-spinor slices |
| `scope:p17-fixed-positive-energy-fiber` | Generic massive rest-frame CAR fiber with `E>0` | Sharp coordinate-time projector representation |
| `scope:p17-literal-time-line` | Unfolded `t∈R`, signed `P_t`, sharp seam at `t=0` | A new internal sheet or nonlocal theory |
| `scope:p17-fundamental-doubled-sheet` | New internal two-sheet degree with complete multiplets | Identification with bare coordinate-time halves |
| `scope:p17-temporal-seam-projector` | Finite real/projector algebra | Pin lift, action, domain, charge, and observable |
| `scope:p17-sk-quartet` | Four-state cohomological control | Completed physical contour Hilbert space and ghost metric |
| `scope:p18-free-instantaneous-seam` | Flat 3+1-dimensional equal-mass free Wess–Zumino mode control; instantaneous canonical Cauchy-data map; unchanged future bulk operators; post-post retarded-pole mass | Energy/time-nonlocal kernels, higher-time-derivative data, persistent carrier or bath, interactions, a full doubled Wess–Zumino Pin/common-domain construction, absolute scale, and Standard Model Higgs physics |
| `scope:p18-uv-and-conditional-controls` | Sharp-kick cutoff integrals, Gaussian Born/numerical control, collisionless FRW dilution, and an inserted soft-term benchmark | Interacting Wigner self-energies, backreaction, thermalization, an absolute mass prediction, and a computed Higgs cancellation |
| `scope:p19-exact-one-field-sugra-trajectories` | Exact F-term reductions, recorded path-local Hessians, \(H_V\) convention, endpoint F directions | Full covariant multifield stability, fermionic/off-shell CPT/Pin seam, present soft spectrum |
| `scope:p19-classical-homogeneous-closed-frw-shooting` | Classical \(k=+1\) turning-point data, target shooting, constraint monitoring | \(\phi_0\) selection, quantum state, perturbations, uniqueness, parameter-free universe size |
| `scope:p19-first-order-potential-slow-roll-r` | First-order potential slow-roll \(r\) at selected \(N_*\) | Reheating map, closed-\(S^3\) perturbations, full \(n_s,r\) likelihood viability |
| `scope:p20-leading-de-sitter-wdw-control` | Constant-field hemisphere exponent, standard history weight, conditional independent-pair joint probability, exact slopes, coherent-sum identity | Exact complex Starobinsky saddle, WDW current/measure/factor ordering, CPT/Pin sheet inner product, local-SUGRA sectors, exact no-go |
| `scope:p20-cecotti-path-f-flatness` | Classical \(D_SW\), inverse metric, \(F^S\), and positive-real static F-flat point on the displayed path | Quantum local-SUSY wavefunction support, closed-bounce Killing spinor, fermionic CPT/Pin boundary condition |
| `scope:p20-conditional-curvature-reheating-benchmark` | One Phase 19 branch, \(w_{\rm reh}=0\), entropy conservation, explicit units, signed \(\Omega_K\) | Seam-selected amplitude/reheating, curvature detection, uncertainties/global likelihood, other thermal histories |
| `scope:p21-positive-euclidean-gaussian` | Positive finite real-boson Gaussian determinant, covariance, Schur and linked-cluster algebra | Lorentzian/OS field theory, fermionic phases, SUGRA kernel, WDW probability |
| `scope:p21-single-flux-tail-toy` | One integer flux, two explicit kernel scalings, tail and prior comparisons | Derived sector measure, joint \((n,\phi)\), membrane rate, inflationary selection |
| `scope:p22-positive-frequency-finite-mode-density` | One free SUSY oscillator, \(\omega,\beta>0\), explicit doubled purification and finite trace functional | Infinite-mode UV product, 4D Pin, BRST, WDW measure, observables |
| `scope:p22-noncompact-zero-mode-limit` | Fixed \(\beta>0\), \(\omega\to0^+\) in the original noncompact \(L^2(\mathbb R)\) oscillator representation | Compact regulators and interacting/gravitational inflaton minisuperspace |
| `scope:p23-single-constraint-rigging-and-current` | One 1+1-dimensional KG-type constraint, full-real-lapse regulators, compact Dirichlet normal form, explicit \(T\)-clock branch, and integrated/local currents | Actual closed Starobinsky/Cecotti WDW operator, contour, ordering/clock independence, Born measure, Pin or local-SUGRA/BRST sectors |
| `scope:p23-supplied-bridge-compact-density` | Compact positive-frequency spectrum with supplied \(L>0\), \(B_L=e^{-L\sqrt h}\), two constrained copies, and a toy anti-linear pairing | Derivation of \(L\) or \(B_L\), unique CPT/Pin selection, regulator independence, cosmological parameter selection, and fermion/ghost sectors |
| `scope:p23-zero-root-and-decompactification` | Abel-regulated quadratic \(E=0\) root, intrinsic-clock determinant, oriented linear comparison, and massless box at \(R\to\infty\) | A universal no-go, proof that \(\phi_0\) is gauge, or an actual saddle zero-mode/Jacobian/modulus measure |
| `scope:p24-connected-homogeneous-starobinsky-interval` | One supplied real reflection-symmetric homogeneous \(S^3\times I\) saddle, constrained endpoint response, principal Hessian, Hamilton–Jacobi null directions, and a fixed-length mutation | Global thimble, bulk determinant, inhomogeneous/local-SUGRA modes, physical density or entropy, and initial-value or SUSY-scale selection |
| `scope:p24-fixed-scale-flat-measure-scalar-gaussian` | The two scalar boundary variables at fixed \(a_\pm\), density precision \(2K_\phi\), covariance, correlation, Schmidt magnitude, and entropy under a supplied flat measure | Dynamical scale-factor integration, full gravitational positivity, a derived factorization, WDW/BFV measure, trace-class state, and local-SUGRA modes |
| `scope:p24-real-boundary-contour-diagnostic` | Eigenvalue signs of the finite \(4\times4\) real-boundary Hessian and the formal scalar Schur complement | Gauge-fixed bulk Morse spectrum, lapse/conformal thimble, intersection number, determinant/ghost phase, and physical-state positivity |
| `scope:p25-fixed-boundary-lapse-and-local-complex-flow` | Supplied Phase-24 endpoints, fixed-lapse off-constraint action, one real symmetric branch/fold, and one local complex segment | Global cycle, branch completeness, BFV/FP measure, bulk determinant, state, or parameter selection |
| `scope:p26-bounded-analytic-sheet-and-fold` | One bounded reflection-symmetric analytic sheet, conjugate control, real Airy fold, and frozen plateau comparison | Proven asymptotic endpoint, physical original contour, Stokes matrix, integer coefficient, determinant, or state |
| `scope:p27-declared-wick-map-and-raw-zero-lapse-control` | Declared Wick convention, equal-boundary short-time action, raw two-coordinate Van Vleck scaling, and spectral lapse proxies | Endpoint-completed BFV kernel, conformal contour, global PL coefficient, physical product, or state |
| `scope:p28-bounded-pl-and-homogeneous-bfv` | Bounded upper arm, one real dual branch, four constructed finite cycles, and Euclidean-continued Abelian homogeneous BFV | Complete saddle/cycle census, endpoint prescription, full superdeterminant, physical density, Pin, soft spectrum, or string embedding |
| `scope:p29-frozen-leading-kernel-and-reduced-bfv-measure` | Frozen two-coordinate leading kernel, declared local flat `da dphi` measure, fixed-parameter ghost reduction, and spectral lapse distributions | Physical WDW measure/ordering, all-orders kernel, conformal contour, full determinant, global coefficient, or density |
| `scope:p30-frozen-coupled-cycle-and-relative-determinant` | Frozen Phase-24 homogeneous interval, finite midpoint cutoffs, coupled field–lapse Gaussian tangent, declared midpoint measure, relative endpoint magnitude, and real-lapse principal/Maslov controls | Nonlinear global contour, original-cycle relative homology, integer PL coefficient, continuum determinant-line phase, full BFV super-Hessian/ghost complex, regulator-independent superdeterminant, physical state, or SUSY spectrum |
| `scope:p31-unreduced-proper-time-hybrid-bfv-control` | Continuum saddle sampled on midpoint lattices, unreduced homogeneous `(q,p,T)` canonical Hessians, truncated continuum gauge harmonics, nonzero alpha=0 BFV quartets, and one bounded local `p_a` scan | Exact finite-lattice critical point, absolute BFV phase/measure, constraint reduction, gauge independence, global clock/kernel transform, inhomogeneous modes, physical state, or SUSY/SUGRA Hessian |
| `scope:p32-specified-lapse-bypasses-and-tracked-dual` | Inherited connected saddle, causal half-line and full-real-line prescriptions, finite lower/upper bypasses, declared principal momentum lift, and bounded real/complex continuation near zero lapse | CPT/Pin contour selection, complete upward-cycle census, oriented inhomogeneous superdeterminant, global PL coefficient, physical state, or SUSY spectrum |
| `scope:p33-frozen-simple-fold-airy-control` | Inherited fixed-boundary real branch near its positive-real Dirichlet fold, two actual solutions at seven `delta` values, canonical Airy normal form, and radius-one local contour comparison | Selected Airy contour/amplitude, absolute determinant line, full dual continuation, global `n_sigma`, physical WDW measure/kernel/state, or SUSY spectrum |
| `scope:p34-frozen-reduced-stationary-family-continuation` | Forty-seven incoming real samples, deterministic fold soft orientation, conjugate constant-`Im W` stationary sheets, and fourteen upper-arm endpoint-Jacobi samples through `Re T=13` in the declared flat complex-`T` metric | Oriented incoming-to-outgoing connection, full joint field–lapse flow, determinant-line transport, all sheets/good ends, global `n_sigma`, physical WDW state, or SUSY spectrum |
| `scope:p35-sampled-reduced-endpoint-detline-transport` | Ordered 57-point endpoint-Jacobi table on the Phase-34 branch pair, declared endpoint basis and orientation, recursive sampled phase/square-root transport, conjugate-input controls, and finite-resolution near-fold comparison | Zero-free continuum interpolation, physical Van Vleck block or measure, absolute sign/Maslov orientation, incoming-to-outgoing cycle connection, full BFV/SUGRA superdeterminant, all sheets/good ends, global `n_sigma`, physical state, or SUSY spectrum |
| `scope:p36-local-airy-connection-and-finite-radius-laterals` | Separately ordered CW/CCW Airy contour bases, exact contour/basis identities and conditional determinant bookkeeping, plus twelve tracked BVP root paths on three finite semicircle radii | Transport of one common physical upward dual, realization of formal \(K_U/K_L\) cycles by BVP roots, original-cycle arm selection, analytic hard quotient and Airy/Airy-prime amplitudes, zero-radius or between-sample theorem, absolute signs, full BFV/SUGRA determinant, global `n_sigma`, physical state, or SUSY scale |
| `scope:p37-closed-local-root-and-reduced-half-form-holonomy` | Exact typed-map and finite-intertwiner controls, six enclosing BVP-root paths on three finite radii, thirteen determinant samples per path, and a same-basepoint minimal-jump reduced-half-form lift | Intersample zero/alias-winding theorem, original relative cycle or global intersection, hard CFU coefficients, spacetime Pin lift, fermion Pfaffian, full BFV/SUGRA operator or quantum master equation, conserved spinorial charge, physical state, or SUSY scale |
| `scope:p38-finite-surrogate-and-bounded-reduced-ledger` | Finite schema surrogate, exact local cycle/dual law and conditional \(\Gamma_0\) representation, sampled reduced real ledger, one upper root/basin continued to three new checkpoints through \(\operatorname{Re}T=16\), and real-coefficient conjugation controls | Physical noninjectivity or nonuniqueness theorem, admissible physical completions, exact joint action/cycle/tangent frames, continuous no-crossing or independent lower-arm continuation, all sheets and good ends, global vector, promoted hard CFU kernel, BFV/Pfaffian/Pin line, charge, state, or spectrum |
| `scope:p39-frozen-m2-configuration-local-joint-candidates` | One frozen two-segment configuration action, one positive-\(T\) saddle, two declared cap pieces, and one finite-radius, finite-time three-real-dimensional Morse-whitened K-chart patch in ambient \(\mathbb R^6\) | Entire bounded-chain pairing, arms/reintersections, exhaustive roots or upward components, exact nonlinear K, certified Stokes chamber/good ends, cutoff/metric/homotopy stability, global vector, BFV/Pfaffian/Pin data, charge, state, or spectrum |
| `scope:p40-frozen-m3-rank-one-phi-source-local-r10-ledger` | One frozen three-segment action, one rank-one antisymmetric phi endpoint-source grid, one fixed delta-zero flow mobility, delta-dependent local Morse launch ellipsoids, one declared cap piece, and five sampled finite-time K-chart candidates in ambient \(\mathbb R^{10}\) | Independent odd source/full odd-sector probe, time-arrow or CPT-breaking inference, \(m=4\)/cutoff convergence, continuous branch or exhaustive census, metric homotopy, exact nonlinear K, entire chain/ends/Stokes data, global vector, BFV/Pfaffian/Pin data, charge, state, spectrum, observable prediction, or quantum gravity |

## Open construction ledger

All entries below have state `OPEN` in the graph.

| Open ID | Missing result |
| --- | --- |
| `open:p17-pin-clifford-lift` | Source-defined reflection lift, square, cocycle, and Majorana bilinear |
| `open:p17-doubled-action` | One real quadratic doubled bulk-plus-interface Lorentzian action |
| `open:p17-gluing-domain` | Variationally admissible `t=0` junction data and a self-adjoint common domain |
| `open:p17-conserved-charge` | Complex-linear fermionic charge acting on that domain with a positive physical adjoint |
| `open:p17-projector-charge-compatibility` | One-domain compatibility of the doubled reality projector and exchange charge |
| `open:p17-physical-sheet-anchor` | Basis-invariant observable distinguishing geometric sheets from internal relabeling |
| `open:p17-reality-positivity-junction` | Simultaneous Majorana reality, positive inner product, and junction consistency |
| `open:p17-sk-full-completion` | Full contour operator algebra and ghost metric |
| `open:full-4d-sugra-interface` | Complete local-SUGRA interface, conserved seam charge, and anomaly-free constraint algebra |
| `open:p18-interacting-wigner-self-energies` | Late-time interacting boson and fermion retarded Wigner self-energies after an admissible seam state |
| `open:p18-persistent-order-parameter` | A finite-energy CPT/Pin-compatible nondecaying `F`/`D` order parameter, memory sector, or vacuum-selection mechanism |
| `open:p18-frw-backreaction` | Expansion with interactions, thermalization, and backreaction beyond the conditional collisionless `a^-2` and `a^-3` controls |
| `open:p18-higgs-power-sensitivity` | Regulator-independent Higgs power-sensitivity calculation in a consistent interacting doubled parent |
| `open:p19-minisuperspace-phi0-measure` | A background wavefunction, seam path integral, or measure that predictively weights \(\phi_0\) |
| `open:p19-cpt-pin-perturbation-state` | A CPT/Pin-compatible Hadamard/Wronskian perturbation state on a fixed background |
| `open:p19-closed-s3-perturbations` | Discrete scalar/tensor propagation through the closed bounce |
| `open:p19-reheating-pivot-map` | Reheating and the map from \(N_{\rm acc}\) to observational \(N_*\) |
| `open:p19-full-covariant-multifield-stability` | Complete covariant scalar and fermionic SUGRA stability along the bounce |
| `open:p20-exact-starobinsky-wdw-state` | Exact complex scalar-gravity saddle, WDW current or decoherent-histories measure, and fixed factor ordering |
| `open:p20-cpt-pin-sheet-inner-product` | A doubled Hilbert space and sewing action that derive normalization, overlap, and the physical joint-probability rule |
| `open:p20-local-sugra-wdw-constraint` | Tree-level Cecotti local-SUGRA Hamiltonian/SUSY constraints, wavefunction components, factor ordering, and sheet boundary data |
| `open:p20-local-sugra-one-loop-selection` | Gauge-fixed boson–fermion–gravitino determinant including ghosts, zero modes, and renormalization |
| `open:p20-quantized-four-form-selection` | UV-fixed discrete flux selection without tuning couplings to \(5.44\) |
| `open:p20-seam-reheating-curvature-prediction` | Joint seam derivation of initial amplitude, reheating dynamics, and a present curvature distribution |
| `open:p21-three-form-seam-kernel` | Flux- and harmonic-dependent cross-sheet kernel derived from compact three-form SUGRA or a charged-membrane saddle |
| `open:p21-physical-flux-measure` | Physical sector measure and WDW current/inner product or decoherence functional yielding a finite joint \((n,\phi)\) distribution |
| `open:p22-homogeneous-minisuperspace-density` | Constrained complex-cap homogeneous density with zero-mode measure, collective-coordinate Jacobian, and physical WDW current |
| `open:p22-gauge-fixed-local-sugra-seam-density` | Coupled gravitino–Goldstino–ghost boundary operator, physical projector, positivity, and trace-class test |
| `open:p23-cap-derived-regulator-independent-density` | Replace the normal form and supplied \(B_L\) by the actual closed Starobinsky/Cecotti constraint, contour, physical product, ordering, clock patches, and zero-mode measure; test regulator-independent positivity |
| `open:p24-gravitational-thimble-and-bulk-determinant` | Determine the contributing lapse/conformal Picard–Lefschetz thimble, intersection number, gauge-fixed primed bulk operator, ghosts, zero modes, determinant, and phase |
| `open:p24-physical-two-boundary-density-and-entropy` | Supply the boundary factorization or Choi prescription, physical measure and WDW/BFV product, then test positivity, trace class, and physical entropy |
| `open:p28-global-relative-homology-and-intersection` | Complete the saddle/dual-cycle census, endpoints and Stokes data, then calculate the integer coefficient of the specified physical original contour |
| `open:p28-zero-lapse-uniform-bfv-kernel` | Combine endpoint factors, BFV/FP measure, zero modes, and a uniform determinant across zero lapse |
| `open:p28-full-gauge-reduced-superdeterminant` | Compute the primed nonzero-mode metric, matter, gravitino, Goldstino, and ghost superdeterminant with phases and renormalization |
| `open:p28-physical-state-and-density` | Specify the WDW/BFV product and boundary factorization, then test normalization, positivity, and trace class |
| `open:p28-string-three-form-soft-spectrum` | Derive a compact seam kernel, local-EFT sector rule, persistent F-type breaking, and soft spectrum; a D-type route needs extra vector/gauging data |
| `open:p29-conformal-bfv-uniform-parametrix` | Extend the Phase-30 tangent, Phase-31 unreduced homogeneous BFV hybrid, Phase-32 local bypass, and Phase-33 fold chart into an endpoint-uniform nonlinear cycle with constraint reduction, fixed oriented determinant line, and full primed inhomogeneous superdeterminant |
| `open:p29-physical-endpoint-measure-and-ordering` | Derive the physical WDW endpoint measure, factor ordering, and inner product rather than supplying local flat `da dphi` |
| `open:p32-cpt-pin-lapse-class-selection` | Construct a complete CPT/Pin bra--ket lift and determine whether it selects the below-origin full-line ket class, its conjugate bra, and their oriented determinant data |
| `open:p33-airy-cycle-amplitude-and-global-continuation` | Transport one regulated relative cycle into the fold chart to fix its Airy contour/Stokes multiplier and analytic amplitude; separately orient the determinant-line prefactor, then continue every joint dual arm before assigning a uniform physical kernel or global `n_sigma` |
| `open:p34-full-joint-dual-determinant-and-global-census` | Determine which outgoing fold arm, if either, carries the incoming cycle; transport the determinant line, compute the full joint field–lapse flow, enumerate every sheet and good end, and only then assign global `n_sigma` or a physical state |
| `open:p35-absolute-detline-full-bfv-and-global-cycle` | Prove a zero-free continuum determinant section, identify the physical canonical block and endpoint measure, fix the absolute determinant/Maslov orientation separately from the Airy cycle connection, compute the regulated full BFV/SUGRA superdeterminant, and complete the global cycle before assigning `n_sigma` or a physical state |
| `open:p36-original-cycle-hard-determinant-and-global-bfv-state` | Transport one specified incoming physical dual and the complete original relative cycle through the Airy chart to every good end; realize the relevant upward cycles, derive the analytic hard quotient and even/odd Airy amplitudes, orient the regulated determinant, and only then assign an arm, global `n_sigma`, or a physical BFV/SUGRA state |
| `open:p37-global-cycle-hard-cfu-full-bfv-pfaffian-gate` | Transport one regulated original lapse-field relative cycle through the fold, compute its signed global intersections and hard CFU coefficients, then lift the selected saddle combination to the complete boson--fermion--ghost BFV/SUGRA determinant/Pfaffian line before testing Pin, a global intertwiner or anomaly, the quantum constraints, or a state |
| `open:gate1-original-cycle-signed-global-intersections` | Pre-specify and transport the regulated joint lapse--field--gauge relative cycle through every relevant saddle, upward cycle, sheet, singularity, Stokes jump, and good end; compute a complete orientation-stable integer intersection vector |
| `open:gate2-hard-cfu-airy-coefficients` | Convert the Gate-1 cycle vector into regular hard Airy/Airy-prime coefficients, match both outer saddles and the absolute phase, and avoid double-counting the soft fold factor |
| `open:gate3-full-bfv-pfaffian-pin-holonomy` | Compute the full gauge-reduced boson--fermion--ghost BFV/SUGRA determinant/Pfaffian line, zero modes, omitted sectors, Pin lift, spectral flow, and basis-independent closed holonomy on the selected saddle combination |
| `open:gate4-spinorial-charge-domain-constraint-closure` | Construct a conserved fermion-odd Lorentz-spinor charge on one positive common domain with anomaly-free BFV/local-SUGRA closure, or establish and correctly name the typed global obstruction |
| `open:gate5-persistent-order-and-pole-splitting` | Derive a finite-energy persistent gauge-invariant order parameter and a late-time interacting boson--fermion retarded-pole difference against trivial-holonomy, zero-order, seam-off, dilution, and backreaction controls |
| `open:p38-explicit-joint-action-cycle-and-oriented-intersections` | Build an explicit finite-cutoff holomorphic joint action, re-solve its discrete saddle and fold, embed separately specified admissible original-cycle candidates, transport full tangent/orientation frames, compute isolated full-space signs, and classify every end before testing regulator stability |
| Canonical BFV sign vs physical determinant line | A stable unreduced `(q,p,T)` determinant sign and same-regulator quartet cancellation do not fix momentum-contour orientation, zero modes, absolute phase, or the constraint-reduced inhomogeneous superdeterminant. |
| Positive lapse half-line vs full real lapse | The former is a causal sourced resolvent with endpoint contact; the latter is a separate group-averaging contour whose relative-homology bypass must be specified. |
| Projected coordinate sign vs signed joint/global coefficient | A finite-radius projected crossing on one tracked lapse base has coordinate sign `+1` only under the declared orientations; it is neither a signed full-joint local intersection nor the sum over every complete upward component, complex sheet, end, Stokes jump, and determinant-line orientation. |
| Lateral conjugation vs CPT/Pin selection | Complex conjugation exchanges lower and upper lateral loci but does not by itself construct the physical Pin lift, select the ket contour, or prove positivity. |
| Directed branch pair vs oriented cycle transport | Incoming and outgoing reduced branches may each follow the local dual direction while the degenerate fold chart still leaves their oriented Airy connection and determinant-line matching unknown. |
| Lateralized first duals vs one transported physical dual | The first dual of \((\Gamma_0,\Gamma_L)\) is not the same input element as the first dual of \((\Gamma_0,\Gamma_U)\). Exact inverse-transpose identities in those bases do not transport one specified physical upward cycle. |
| BVP root sheets vs formal upward cycles | Numerical root permutations and regular sampled CW/U and CCW/L endpoints do not realize the formal \(K_U\) and \(K_L\) cycles or determine their intersection with the original contour. |

The shortest honest statement of the research frontier is therefore: **the programme now has a supplied connected Starobinsky interval, a stationary lapse saddle, bounded reduced constant-phase branches, a measured simple-fold Airy scale, zero-lapse distributional and finite-cutoff BFV controls, one local improved-static BFV zero-mode replacement-source algebra on \(\mathcal U_+\), one declared local self-adjoint \(M_c\) realization, a frozen static/order-zero spectral-form match, one relative nonzero \(m=2\) determinant/Pfaffian control, one recorded projected lapse-base crossing, sampled endpoint-Jacobi transport, exact local Airy basis identities, and a same-basepoint closed continuation of both local BVP roots. On three finite enclosing loops the roots exchange, and conditional on the recorded nonzero minimal-jump sampled lift with no unresolved intersample zero or alias winding, the reduced bosonic inverse-square-root section has an order-four conjugacy class with \(L^2=-I\). Those invariants make the local closed transport stronger than separately trivialized open laterals, but they do not identify the root map with Airy-solution or relative-cycle monodromy. Bare root monodromy does not break the Phase-17 local/exchange basis equivalence, and the reduced bosonic half-form is not a spacetime Pin lift or fermion Pfaffian line. The declared \(M_c\) domain and frozen \(c=0\) test form are not an exact endpoint transform, original-variable ordering, arbitrary-state/full-real-lapse physical rigging map, full trajectory measure or physical state. The declared endpoint data fail to select a unique exact completion, and the pinned trajectory inputs fail to select a unique zero-mode completion. No original physical relative cycle, signed global intersection coefficient, analytic hard CFU Airy/Airy-prime amplitude, zero-free continuum determinant lift, full boson--fermion--ghost BFV/SUGRA operator or Pfaffian line, conserved spinorial supercharge, quantum master equation, WDW/BFV state, seam sector rule, or persistent soft spectrum has been derived.**

Phase 38 sharpens the first missing step rather than weakening that boundary. The current records do not
license inverse reconstruction of a physical joint cycle, but the finite noninjective surrogate does not
prove physical noninjectivity or nonuniqueness. The correct conditional local coefficient map uses
Gauss--Manin transport rather than the root swap. One upper root/basin and its conjugation control are
sampled through \(\operatorname{Re}T=16\), with no sampled projected crossing, while the origin limit and
both box exits stay unresolved. Gate 1 is therefore `OPEN_PARTIAL_PROGRESS`; conditional Gate-2
calculation may proceed in parallel, but a physical uniform-kernel claim still needs the Gate-1 cycle
vector and a joint consistency check.

Phase 39 supplies the first explicit nonlinear finite-cutoff configuration action and direct local
full-\(\mathbb R^6\) orientation calculation in this route. One positive-\(T\) discrete saddle and one
candidate on each of two declared cap pieces are numerically resolved; the two direct local signs are
\(+1\) in the frozen configuration-coordinate orientations. This is stronger than the Phase-32
projected lapse-base sign but remains a cap-piece witness against one finite-radius, finite-time chart
patch, not a complete upward cycle or bounded-chain pairing. The unsearched arms and reintersections,
incomplete root/component census, unresolved Stokes chamber and ends, and absent cutoff/metric/homotopy
stability keep every chain/global integer null and Gate 1 open.

Phase 40 raises the cutoff to \(m=3\) and introduces one rank-one antisymmetric phi endpoint source. It
supports a nonzero anchor-subtracted, sign-reversing sampled response in the first resolved two-dimensional
reflection-odd \((a,\phi)\) block, but does not probe its independent direction or establish a physical
time arrow. With the delta-zero flow mobility held fixed and delta-dependent Morse launch ellipsoids used
only to seed local charts, five sampled full-\(\mathbb R^{10}\) candidates have direct sign \(+1\).
Only three primary points receive the full finite-difference/flow audit, the five samples do not prove a
continuous branch, and the K-launch clamp is strictly local. With \(m=4\), cutoff stability, the complete
chain/component census, exact nonlinear K, Stokes data, and good ends absent, all chain/global outputs
remain null and Gate 1 remains open.

Phase 41 raises the cutoff to (m=4) and adds the independent a-only endpoint source. The
anchor-subtracted two-source response passes the frozen stable numerical rank-two rule, and five local
full-(mathbb R^{14}) cap candidates have direct declared sign (+1). This adds a real second response
direction and higher-cutoff local roots, but not a robust source branch: the predeclared `u2`
finite-difference plateau fails at all three audited points, so both source robustness outputs are
inconclusive. The exact affine m2/m4 grid and cap embedding does not identify their nonlinear actions,
upward cycles, or determinant lines; the nonnested m3/m4 sign agreement is descriptive only. The full
chain, exhaustive components, exact nonlinear K, Stokes chamber, good ends, physical original cycle,
and BFV/Pfaffian/Pin line remain absent. Six promoted outputs stay null and Gate 1 stays open.

Phase 42 does not search another root or replace the failed step pair. It reloads the three immutable
checkpoint roots and applies fixed production, tight, and Radau tiers, fixed fourth-order real finite
differences, local Hessian-action identities, and a sufficient normalized matrix homotopy. Solver noise
and the old first-pair reference artifact are supported at `phi_plus` and `a_plus`; stable local
Hessian-action anomalies are supported at all three roots without proving a code bug. The time-column
comparison is limited by distinct solver endpoints and is excluded as independent bug evidence. All
three normalized local homotopies retain root sign `-1`, but `shared_zero` misses the frozen `u2`
reference-neighbor threshold. The reference tangent remains inconclusive, Phase 41 stays 8/9, and the
six null global outputs keep Gate 1 open.

Phase 43 does not reintegrate that tangent or inspect another root. It consumes all 90 frozen local
state-and-direction slots directly and rebuilds the four-element action and its Hessian/directional
derivative independently at 80 and 120 decimal digits. The local reference is corroborated at 90/90
slots. Against it, 13/90 byte-pinned NumPy64 Hessian-action outputs cross the frozen `5e-13` normwise
threshold; this is an operational pipeline mismatch, not proof of a wrong formula or unique code
defect. Under the separate disclosed-anomaly rule, same-step binary64 finite-difference evidence is
supported at 28/33 slots, but five complete direction-2 exceptions make the universal all-33 claim
false. No root, ODE, integrated tangent, time column, local orientation, determinant line, or global
cycle is evaluated. Phase 41 therefore remains 8/9, the Phase-42 reference remains inconclusive, all
six global outputs and seven desired outputs remain null, and Gate 1 remains open.

Phase 44 preserves those historical labels while resolving a narrower arithmetic-provenance question.
Exact canonicalization finds no componentwise difference between the declared source and independently
constructed actions, gradients, or Hessians. All 90 signed S0-to-S7 telescopes close, and the fixed
forward-error model covers all 13 disclosed mismatches and all 77 controls. Coefficient, state,
Hessian, and contraction contributions are all detectably present at every slot, can cancel, and give
the same nonexclusive tri-state pattern in both cohorts; the calculation therefore selects no unique
cause, best contraction algorithm, or source rewrite. It evaluates no root, ODE, integrated tangent,
time column, local orientation, determinant line, or global cycle. Phase 41 remains 8/9, the Phase-42
reference remains inconclusive, all six global outputs and seven desired outputs remain null, and
Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

## Repository artifacts

| Phase | Executable | Report | Observed evidence |
| --- | --- | --- | --- |
| 11 | [`phase11_collar_admissibility.py`](../../cpt_temporal_folded_susy/phase11_collar_admissibility.py) | [`PHASE11_COLLAR_ADMISSIBILITY.md`](../../cpt_temporal_folded_susy/PHASE11_COLLAR_ADMISSIBILITY.md) | historical exact assertions; no named result recorder |
| 12 | [`phase12_boundary_twist_interface.py`](../../cpt_temporal_folded_susy/phase12_boundary_twist_interface.py) | [`PHASE12_BOUNDARY_TWIST_INTERFACE.md`](../../cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md) | report plus frozen historical contract |
| 13A | [`phase13a_lorentzian_branch_supercharge.py`](../../cpt_temporal_folded_susy/phase13a_lorentzian_branch_supercharge.py) | [`PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md`](../../cpt_temporal_folded_susy/PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md) | [`PHASE13A_ADVERSARIAL_ERRATUM.json`](../../cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json) is the authoritative scope correction |
| 14A | [`phase14a_chiral_clock_charge_first.py`](../../cpt_temporal_folded_susy/phase14a_chiral_clock_charge_first.py) | [`PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md`](../../cpt_temporal_folded_susy/PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md) | [`PHASE14A_RUN_RESULT.json`](../../cpt_temporal_folded_susy/PHASE14A_RUN_RESULT.json) |
| 15A | no valid executable/result | provenance packets only | [`PHASE15A_SEQUENCE_BREACH.json`](../../cpt_temporal_folded_susy/PHASE15A_SEQUENCE_BREACH.json); procedural evidence, no science |
| 15R | [`phase15r_parent_sign_reproduction.py`](../../cpt_temporal_folded_susy/phase15r_parent_sign_reproduction.py) | [`PHASE15R_PARENT_SIGN_REPAIR.md`](../../cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md) | [`PHASE15R_RUN_RESULT.json`](../../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json) · [`PHASE15R_REPLAY_RECEIPT.json`](../../cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json) |
| 16 | [`phase16_bgg_single_source.py`](../../cpt_temporal_folded_susy/phase16_bgg_single_source.py) | [`PHASE16_BGG_SINGLE_SOURCE.md`](../../cpt_temporal_folded_susy/PHASE16_BGG_SINGLE_SOURCE.md) · [`PHASE16_BGG_SOURCE_NOTES.md`](../../cpt_temporal_folded_susy/PHASE16_BGG_SOURCE_NOTES.md) | [`phase16-result.json`](./evidence/phase16-result.json) |
| 17 | [`phase17_time_line_fold_algebra.py`](../../cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py) | [`PHASE17_TIME_LINE_FOLD_ALGEBRA.md`](../../cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md) | [`phase17-result.json`](./evidence/phase17-result.json) |
| 18 | [`phase18_gaussian_seam_spectrum.py`](../../cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py) | [`PHASE18_GAUSSIAN_SEAM_SPECTRUM.md`](../../cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md) | [`phase18-result.json`](./evidence/phase18-result.json) |
| 19 | [`phase19_closed_sugra_bounce.py`](../../cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py) | [`PHASE19_CLOSED_SUGRA_BOUNCE.md`](../../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md) | [`phase19-result.json`](./evidence/phase19-result.json) |
| 20 | [`phase20_two_sheet_wdw_selection.py`](../../cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py) | [`PHASE20_TWO_SHEET_WDW_SELECTION.md`](../../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md) | [`phase20-result.json`](./evidence/phase20-result.json) |
| 21 | [`phase21_connected_seam_gaussian.py`](../../cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py) | [`PHASE21_CONNECTED_SEAM_GAUSSIAN.md`](../../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md) | [`phase21-result.json`](./evidence/phase21-result.json) |
| 22 | [`phase22_finite_mode_seam_density.py`](../../cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py) | [`PHASE22_FINITE_MODE_SEAM_DENSITY.md`](../../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md) | [`phase22-result.json`](./evidence/phase22-result.json) |
| 23 | [`phase23_homogeneous_minisuperspace_density.py`](../../cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py) | [`PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md`](../../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md) | [`phase23-result.json`](./evidence/phase23-result.json) |
| 24 | [`phase24_connected_starobinsky_interval.py`](../../cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py) | [`PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md`](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md) | [`phase24-result.json`](./evidence/phase24-result.json) |
| 25 | [`phase25_connected_lapse_scan.py`](../../cpt_temporal_folded_susy/phase25_connected_lapse_scan.py) | [`PHASE25_CONNECTED_LAPSE_SCAN.md`](../../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md) | [`phase25-result.json`](./evidence/phase25-result.json) |
| 26 | [`phase26_global_lapse_flow.py`](../../cpt_temporal_folded_susy/phase26_global_lapse_flow.py) | [`PHASE26_GLOBAL_LAPSE_FLOW.md`](../../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md) | [`phase26-result.json`](./evidence/phase26-result.json) |
| 27 | [`phase27_lorentzian_lapse_endpoint.py`](../../cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py) | [`PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md`](../../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md) | [`phase27-result.json`](./evidence/phase27-result.json) |
| 28 | [`phase28_thimble_bfv_intersection.py`](../../cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py) | [`PHASE28_THIMBLE_BFV_INTERSECTION.md`](../../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md) | [`phase28-result.json`](./evidence/phase28-result.json) |
| 29 | [`phase29_zero_lapse_uniform_kernel.py`](../../cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py) | [`PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md`](../../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md) | [`phase29-result.json`](./evidence/phase29-result.json) |
| 30 | [`phase30_conformal_bfv_determinant_line.py`](../../cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py) | [`PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md`](../../cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md) | [`phase30-result.json`](./evidence/phase30-result.json) |
| 31 | [`phase31_homogeneous_bfv_superhessian.py`](../../cpt_temporal_folded_susy/phase31_homogeneous_bfv_superhessian.py) | [`PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md`](../../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md) | [`phase31-result.json`](./evidence/phase31-result.json) |
| 32 | [`phase32_below_origin_lapse_intersection.py`](../../cpt_temporal_folded_susy/phase32_below_origin_lapse_intersection.py) | [`PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md`](../../cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md) | [`phase32-result.json`](./evidence/phase32-result.json) |
| 33 | [`phase33_fold_airy_uniformization.py`](../../cpt_temporal_folded_susy/phase33_fold_airy_uniformization.py) | [`PHASE33_FOLD_AIRY_UNIFORMIZATION.md`](../../cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md) | [`phase33-result.json`](./evidence/phase33-result.json) |
| 34 | [`phase34_directed_fold_dual_continuation.py`](../../cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py) | [`PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md`](../../cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md) | [`phase34-result.json`](./evidence/phase34-result.json) |
| 35 | [`phase35_reduced_detline_transport.py`](../../cpt_temporal_folded_susy/phase35_reduced_detline_transport.py) | [`PHASE35_REDUCED_DETLINE_TRANSPORT.md`](../../cpt_temporal_folded_susy/PHASE35_REDUCED_DETLINE_TRANSPORT.md) | [`phase35-result.json`](./evidence/phase35-result.json) |
| 36 | [`phase36_airy_gauss_manin_connection.py`](../../cpt_temporal_folded_susy/phase36_airy_gauss_manin_connection.py) | [`PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md`](../../cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md) | [`phase36-result.json`](./evidence/phase36-result.json) |
| 37 | [`phase37_closed_fold_holonomy.py`](../../cpt_temporal_folded_susy/phase37_closed_fold_holonomy.py) | [`PHASE37_CLOSED_FOLD_HOLONOMY.md`](../../cpt_temporal_folded_susy/PHASE37_CLOSED_FOLD_HOLONOMY.md) | [`phase37-result.json`](./evidence/phase37-result.json) |
| 38 | [`phase38_joint_cycle_identifiability.py`](../../cpt_temporal_folded_susy/phase38_joint_cycle_identifiability.py) | [`PHASE38_JOINT_CYCLE_IDENTIFIABILITY.md`](../../cpt_temporal_folded_susy/PHASE38_JOINT_CYCLE_IDENTIFIABILITY.md) | [`phase38-result.json`](./evidence/phase38-result.json) |
| 39 | [`phase39_finite_joint_intersection.py`](../../cpt_temporal_folded_susy/phase39_finite_joint_intersection.py) | [`PHASE39_FINITE_JOINT_INTERSECTION.md`](../../cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md) · [`PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json) | [`phase39-result.json`](./evidence/phase39-result.json) |
| 40 | [`phase40_m3_reflection_odd_intersection.py`](../../cpt_temporal_folded_susy/phase40_m3_reflection_odd_intersection.py) | [`PHASE40_M3_REFLECTION_ODD_INTERSECTION.md`](../../cpt_temporal_folded_susy/PHASE40_M3_REFLECTION_ODD_INTERSECTION.md) · [`PHASE40_M3_REFLECTION_ODD_INTERSECTION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE40_M3_REFLECTION_ODD_INTERSECTION_INPUTS.json) | [`phase40-result.json`](./evidence/phase40-result.json) |
| 41 | [`phase41_m4_two_source_intersection.py`](../../cpt_temporal_folded_susy/phase41_m4_two_source_intersection.py) | [`PHASE41_M4_TWO_SOURCE_INTERSECTION.md`](../../cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION.md) · [`PHASE41_M4_TWO_SOURCE_INTERSECTION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION_INPUTS.json) | [`phase41-result.json`](./evidence/phase41-result.json) |
| 42 | [`phase42_m4_fixed_root_tangent_disentanglement.py`](../../cpt_temporal_folded_susy/phase42_m4_fixed_root_tangent_disentanglement.py) · [`phase42_m4_fixed_root_checkpoint.py`](../../cpt_temporal_folded_susy/phase42_m4_fixed_root_checkpoint.py) | [`PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT.md`](../../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT.md) · [`PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json) · [`PHASE42_M4_FIXED_ROOT_CHECKPOINT.json`](../../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_CHECKPOINT.json) | [`phase42-result.json`](./evidence/phase42-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json) |
| 43 | [`phase43_m4_high_precision_local_rhs_arbitration.py`](../../cpt_temporal_folded_susy/phase43_m4_high_precision_local_rhs_arbitration.py) | [`PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION.md`](../../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION.md) · [`PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_INPUTS.json) | [`phase43-result.json`](./evidence/phase43-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_RESULT.json) |
| 44 | [`phase44_m4_numpy64_local_rhs_error_decomposition.py`](../../cpt_temporal_folded_susy/phase44_m4_numpy64_local_rhs_error_decomposition.py) | [`PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION.md`](../../cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION.md) · [`PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_INPUTS.json) | [`phase44-result.json`](./evidence/phase44-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json) |
| 51 | [`phase51_m5_gamma_k_local_continuation.py`](../../cpt_temporal_folded_susy/phase51_m5_gamma_k_local_continuation.py) | [`PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION.md`](../../cpt_temporal_folded_susy/PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION.md) · [`PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_INPUTS.json) | [`phase51-result.json`](./evidence/phase51-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE51_M5_GAMMA_K_LOCAL_CONTINUATION_RESULT.json) |
| 52 | [`phase52_m5_cse_runtime_dtype_and_rhs_repair.py`](../../cpt_temporal_folded_susy/phase52_m5_cse_runtime_dtype_and_rhs_repair.py) | [`PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR.md`](../../cpt_temporal_folded_susy/PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR.md) · [`PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_INPUTS.json) | [`phase52-result.json`](./evidence/phase52-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE52_M5_CSE_RUNTIME_DTYPE_AND_RHS_REPAIR_RESULT.json) |
| 53 | [`phase53_m5_element_local_full_continuation.py`](../../cpt_temporal_folded_susy/phase53_m5_element_local_full_continuation.py) | [`PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_INPUTS.json) | [`phase53-result.json`](./evidence/phase53-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE53_M5_ELEMENT_LOCAL_FULL_CONTINUATION_RESULT.json) |
| 54 | [`phase54_p51_global_noncse_control_audit.py`](../../cpt_temporal_folded_susy/phase54_p51_global_noncse_control_audit.py) | [`PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT_INPUTS.json) · [`PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT.md`](../../cpt_temporal_folded_susy/PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT.md) | [`phase54-result.json`](./evidence/phase54-result.json) · [corrected full raw result](../../cpt_temporal_folded_susy/PHASE54_P51_GLOBAL_NONCSE_CONTROL_AUDIT_RESULT.json) |
| 55 | [`phase55_p53_root_fixed_launch_schedule_transfer.py`](../../cpt_temporal_folded_susy/phase55_p53_root_fixed_launch_schedule_transfer.py) | [`PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER_INPUTS.json) · [`PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER.md`](../../cpt_temporal_folded_susy/PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER.md) | [`phase55-result.json`](./evidence/phase55-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE55_P53_ROOT_FIXED_LAUNCH_SCHEDULE_TRANSFER_RESULT.json) |
| 56 | [`phase56_lambda_half_launch_provenance_residual_conditioning.py`](../../cpt_temporal_folded_susy/phase56_lambda_half_launch_provenance_residual_conditioning.py) | [`PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_INPUTS.json`](../../cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_INPUTS.json) · [`PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING.md`](../../cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING.md) | [`phase56-result.json`](./evidence/phase56-result.json) · [full raw result](../../cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_RESULT.json) |
| Gate 1 bosonic canonical source (non-numbered) | [`gate1_bosonic_canonical_source_pushforward.py`](../../cpt_temporal_folded_susy/gate1_bosonic_canonical_source_pushforward.py) | [`GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_INPUTS.json) · [`GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md`](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD.md) | [`gate1-bosonic-canonical-source-pushforward-result.json`](./evidence/gate1-bosonic-canonical-source-pushforward-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json) |
| Gate 1 trace-gauge FP admissibility (non-numbered) | [`gate1_trace_gauge_fp_admissibility.py`](../../cpt_temporal_folded_susy/gate1_trace_gauge_fp_admissibility.py) | [`GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_INPUTS.json) · [`GATE1_TRACE_GAUGE_FP_ADMISSIBILITY.md`](../../cpt_temporal_folded_susy/GATE1_TRACE_GAUGE_FP_ADMISSIBILITY.md) | [`gate1-trace-gauge-fp-admissibility-result.json`](./evidence/gate1-trace-gauge-fp-admissibility-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) trace endpoint action (non-numbered) | [`gate1_v0_trace_endpoint_completion.py`](../../cpt_temporal_folded_susy/gate1_v0_trace_endpoint_completion.py) | [`GATE1_V0_TRACE_ENDPOINT_COMPLETION_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_TRACE_ENDPOINT_COMPLETION_INPUTS.json) · [`GATE1_V0_TRACE_ENDPOINT_COMPLETION.md`](../../cpt_temporal_folded_susy/GATE1_V0_TRACE_ENDPOINT_COMPLETION.md) | [`gate1-v0-trace-endpoint-action-result.json`](./evidence/gate1-v0-trace-endpoint-action-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_TRACE_ENDPOINT_COMPLETION_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) componentwise off-shell Darboux chart (non-numbered) | [`gate1_v0_offshell_darboux_chart.py`](../../cpt_temporal_folded_susy/gate1_v0_offshell_darboux_chart.py) | [`GATE1_V0_OFFSHELL_DARBOUX_CHART_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_OFFSHELL_DARBOUX_CHART_INPUTS.json) · [`GATE1_V0_OFFSHELL_DARBOUX_CHART.md`](../../cpt_temporal_folded_susy/GATE1_V0_OFFSHELL_DARBOUX_CHART.md) | [`gate1-v0-offshell-darboux-chart-result.json`](./evidence/gate1-v0-offshell-darboux-chart-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_OFFSHELL_DARBOUX_CHART_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) principal endpoint FIO (non-numbered) | [`gate1_v0_principal_endpoint_fio.py`](../../cpt_temporal_folded_susy/gate1_v0_principal_endpoint_fio.py) | [`GATE1_V0_PRINCIPAL_ENDPOINT_FIO.md`](../../cpt_temporal_folded_susy/GATE1_V0_PRINCIPAL_ENDPOINT_FIO.md) | [`gate1-v0-principal-endpoint-fio-result.json`](./evidence/gate1-v0-principal-endpoint-fio-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) improved-static BFV zero-mode source (non-numbered) | [`gate1_v0_improved_static_bfv_source.py`](../../cpt_temporal_folded_susy/gate1_v0_improved_static_bfv_source.py) | [`GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_INPUTS.json) · [`GATE1_V0_IMPROVED_STATIC_BFV_SOURCE.md`](../../cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE.md) | [`gate1-v0-improved-static-bfv-source-result.json`](./evidence/gate1-v0-improved-static-bfv-source-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) constraint spectral domain (non-numbered) | [`gate1_v0_constraint_spectral_domain.py`](../../cpt_temporal_folded_susy/gate1_v0_constraint_spectral_domain.py) | [`GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_INPUTS.json) · [chain report](../../cpt_temporal_folded_susy/GATE1_V0_SPECTRAL_TO_M2_BFV_CHAIN.md) | [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) endpoint subprincipal nonuniqueness (non-numbered) | [`gate1_v0_endpoint_subprincipal_nonuniqueness.py`](../../cpt_temporal_folded_susy/gate1_v0_endpoint_subprincipal_nonuniqueness.py) | [`GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_INPUTS.json) · [chain report](../../cpt_temporal_folded_susy/GATE1_V0_SPECTRAL_TO_M2_BFV_CHAIN.md) | [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) frozen static-spectral pairing (non-numbered) | [`gate1_v0_static_spectral_pairing.py`](../../cpt_temporal_folded_susy/gate1_v0_static_spectral_pairing.py) | [`GATE1_V0_STATIC_SPECTRAL_PAIRING_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_STATIC_SPECTRAL_PAIRING_INPUTS.json) · [chain report](../../cpt_temporal_folded_susy/GATE1_V0_SPECTRAL_TO_M2_BFV_CHAIN.md) | [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) minimal \(m=2\) spectral BFV trajectory control (non-numbered) | [`gate1_v0_bfv_m2_spectral_trajectory.py`](../../cpt_temporal_folded_susy/gate1_v0_bfv_m2_spectral_trajectory.py) | [`GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_INPUTS.json) · [chain report](../../cpt_temporal_folded_susy/GATE1_V0_SPECTRAL_TO_M2_BFV_CHAIN.md) | [`gate1-v0-spectral-to-m2-bfv-chain-result.json`](./evidence/gate1-v0-spectral-to-m2-bfv-chain-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) selected densitized Liouville--KL RAQ control (non-numbered) | [`gate1_v0_densitized_liouville_raq.py`](../../cpt_temporal_folded_susy/gate1_v0_densitized_liouville_raq.py) | [`GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_INPUTS.json) · [derivation report](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_QUANTUM_COSMOLOGY_DERIVATION.md) | [`gate1-v0-densitized-liouville-raq-result.json`](./evidence/gate1-v0-densitized-liouville-raq-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) selected densitized RAQ \(p=0\) boundary control (non-numbered) | [`gate1_v0_densitized_raq_p_zero_boundary.py`](../../cpt_temporal_folded_susy/gate1_v0_densitized_raq_p_zero_boundary.py) | [`GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_INPUTS.json) · [boundary report](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY.md) | [`gate1-v0-densitized-raq-p-zero-boundary-result.json`](./evidence/gate1-v0-densitized-raq-p-zero-boundary-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) BFV zero-mode elimination Ward control (non-numbered) | [`gate1_v0_bfv_zero_mode_elimination_ward.py`](../../cpt_temporal_folded_susy/gate1_v0_bfv_zero_mode_elimination_ward.py) | [`GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_INPUTS.json`](../../cpt_temporal_folded_susy/GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_INPUTS.json) · [derivation report](../../cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_QUANTUM_COSMOLOGY_DERIVATION.md) | [`gate1-v0-bfv-zero-mode-elimination-ward-result.json`](./evidence/gate1-v0-bfv-zero-mode-elimination-ward-result.json) · [full raw result](../../cpt_temporal_folded_susy/GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT.json) |
| Gate 1 closed-FRW \(V=0\) formula/philosophy/roadmap map (non-evidential) | — | [`GATE1_V0_QUANTUM_COSMOLOGY_ONTOLOGY_MAP.md`](../../cpt_temporal_folded_susy/GATE1_V0_QUANTUM_COSMOLOGY_ONTOLOGY_MAP.md) | ontology navigation only; it cites existing evidence and introduces no new calculation verdict |

The graph also indexes [`docs/SCIENTIFIC_CLI_MANUAL.md`](../../docs/SCIENTIFIC_CLI_MANUAL.md) as tooling. Policy nodes and `GOVERNED_BY` edges describe workflow only; they cannot support or contradict a physics claim.

## External KG bridge memory

The programme has one `EXACT`, `RESOLVED` SYMPOSIUM bridge:

- `programme:cpt-temporal-folded-susy` → `sym:LakatosTree:lakatostree_cpttemporalfoldedsusy_20260809`

Several claim and concept bridges are `RELATED`, `RESOLVED` pointers to older nodes. In the table, each suffix expands to `sym:LakatosNode:lakatostree_cpttemporalfoldedsusy_20260809/<suffix>`.

| Local node | External UID suffix |
| --- | --- |
| `claim:P17_STANDARD_LOCAL_Q_HALF_EXCHANGE` | `standard-susy-translation-closure` |
| `claim:P17_REFLECTION_COMPOSED_Q_IS_STANDARD_LOCAL_CHARGE` | `hls-local-supercharge-no-go` |
| `claim:P17_REFLECTION_COMPOSED_Q_IS_STANDARD_LOCAL_CHARGE` | `sheet-locality-unfolded-bilocality` |
| `claim:P17_SUPERALGEBRA_SELECTS_SHEET_BASIS` | `exact-unitary-fold-equivalence` |
| `claim:P17_ORDINARY_REAL_TEMPORAL_SEAM_PRESERVES_SUSY` | `fixed-spacelike-seam-rigid-susy-no-go` |
| `claim:P17_DOUBLED_REAL_SHEET_PROJECTOR_WITNESS` | `modified-reality-temporal-projector-route` |
| `concept:cpt-pin-sewing` | `bft-cpt-not-supercharge` |

The two Phase 15R claim lookups and the Phase 17 SK claim lookup remain `UNRESOLVED`. Phase 18 adds four more unresolved lookups, one for each scoped claim:

- `claim:P18_ELAPSED_TIME_ALONE_BREAKS_SUSY`
- `claim:P18_FREE_CANONICAL_SEAM_GENERATES_POLE_SPLITTING`
- `claim:P18_FREE_SEAM_CAN_PREPARE_NONSUSY_STATE`
- `claim:P18_SHARP_SEAM_IS_UV_ADMISSIBLE`

Phase 24 adds a further unresolved bridge at `phase:p24`. The older
`sym:LakatosElement:lakatostree_cpttemporalfoldedsusy_20260809::p24` is a distinct 2026-08-09
planning node and was deliberately not reused. Phases 25–40 add sixteen fresh unresolved phase lookups;
similarly numbered historical planning nodes were not reused. The recursive-audit policy and the ordered
five-gate policy add two separate repository-workflow lookups. Phases 44, 46, 47, 51, 52, and 53 add six
further repository-local phase lookups. The invalid scalar zero-lapse control, finite bosonic
single-lateral claim, unchanged-source trace-gauge append claim, and closed-FRW \(V=0\) local
relational endpoint-action claim add four more local lookups. The later V0 Darboux, principal-FIO,
one-term exact-unitarity and improved-static BFV zero-mode nodes add four; the Phase 14A historical
calculation and Phase 15A sequence-breach evidence add two. The V0 spectral-to-\(m=2\) chain adds five
claim lookups for the declared multiplication domain, endpoint-completion uniqueness, frozen spectral
form, relative nonzero quartet and trajectory zero-mode uniqueness. The subsequent selected densitized
RAQ and local zero-mode Ward controls add repository-local lookups. These bridges remain local because no authorized external UID or
writer exists; no identity was invented for the roadmap.
A resolved UID proves only that the target exists; it is not an evidence receipt, equivalence assertion,
review outcome, or KG ratification.
