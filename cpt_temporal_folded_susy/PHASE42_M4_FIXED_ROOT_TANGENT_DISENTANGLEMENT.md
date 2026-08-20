# Phase 42 — m=4 fixed-root tangent disentanglement

## Outcome

Phase 42 audits the single failed Phase-41 tangent control at three immutable
local m=4 roots. It consumes the committed post-hoc checkpoint, performs no
root, saddle, chart, sign, or step retuning, and completed with

~~~text
exact contracts:     8 / 8 PASS
numerical contracts: 6 / 8 PASS
run_status:           VALID_TYPED_RUN
process exit:         0
Phase 41:             remains 7/7 exact and 8/9 numerical
Gate 1:               OPEN_PARTIAL_PROGRESS
~~~

The two non-PASS numerical records are scientific, non-invalidating outcomes:

1. **P42.variational.local_RHS_and_time_column** returned
   **LOCAL_VARIATIONAL_IDENTITY_NOT_SUPPORTED**. Multiple complete,
   reference-stable local Hessian-action tests exceed the frozen threshold
   at each of the three roots. This supports the protocol-defined
   **VARIATIONAL_RHS_BUG_EVIDENCE** anomaly label.
2. **P42.derivative.all_column_fixed_R4** returned
   **REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE**. The shared-zero \(u_2\)
   column misses the frozen internal-neighbor stability threshold, although
   its direction and norm comparisons and the full-matrix errors are small.

The complete cause ledger supports three labels simultaneously:

~~~text
SOLVER_NOISE_EVIDENCE
STEP_PAIR_SELECTION_ARTIFACT
VARIATIONAL_RHS_BUG_EVIDENCE
~~~

This is deliberately a multi-label result. It does **not** identify one
unique cause of the Phase-41 plateau. The aggregate rule is “supported at
at least one fixed point,” not “supported at every point,” and the three
labels describe compatible numerical or implementation layers rather than
mutually exclusive physical mechanisms.

The overall Phase-42 tangent claim therefore remains
**REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE**. Phase 41 is not promoted to
9/9, and no bounded-chain, global-intersection, cutoff, continuum, SUSY, or
quantum-gravity claim follows.

## 1. Frozen scope and provenance

The diagnostic targets only

~~~text
shared_zero  (delta_a=0,      delta_phi=0)
phi_plus     (delta_a=0,      delta_phi=+0.001)
a_plus       (delta_a=+0.001, delta_phi=0)
~~~

with the Phase-41 cap radius \(10^{-4}\), shape parameter \(\lambda=1\),
fixed mobility, affine chart, and fourteen-component root parameters held
immutable. The checkpoint is explicitly post-hoc regenerated; it is not a
byte archive of the original Phase-41 stdout, and historical root-vector
identity with that stdout is not claimed. The input freeze was made after
the Phase-41 tangent failure was known, so this is a controlled diagnostic,
not a preregistration.

The authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| Phase-42 input manifest | dc21816b9fef9ad658fdd728e73453ffeee46f4d | 1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6 |
| fixed-root checkpoint | 731579c37867a2041b65359bfc649be3b66900c7 | ad51bac8eff42e4d300b7872886053c1a6110812ed43b57cdd0e4dbf961891c6 |
| checkpoint extractor | 712c54b13869b1aee26503947c60dfe34bfa2a3c | 5b2492347405bef0fed26fbfe2a68648899219c8583c20b8de0b2be02419de6d |
| Phase-42 runner | 1c0d7fed4aa99c6424ec659dae8ba6f24b791926 | 1414664c3b7d3da99364d11c0b639ff99c8ecc71c141f99bfaa6c4e367893019 |
| raw Phase-42 result | d8c2fce3eb3e72a956a34776970c15642ed88047 | 568e02cc8c4d730aba3a7a83febd3aa41cf14dfdb87b53950cc6fcc78c5bd013 |

The raw result is a 7,526,372-byte compact JSON artifact with schema
**ice-phase42-fixed-root-tangent-disentanglement/v1**. Its canonical
self-excluding payload digest is

~~~text
8d824c2c7204a6762a0e75321c285bd30339f67b244bb106a9dc4febc9da7b36
~~~

The runner also pins the Phase-41 executable at commit
**a31a8627b0e0e210dea96d1d69dad80ccaa6decd**, SHA-256
**377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530**,
and its input manifest at commit
**58181447b558fa204406b732badd5c2fd541bb47**, SHA-256
**dc17f4d25e758946fe00fec0bb209462294d4d982b1f86b59c099b8de064c92e**.

All start/end source, runner, Git HEAD, runtime, and repository-pycache
TOCTOU comparisons passed. The runtime was CPython 3.13.5 with NumPy 2.5.2,
SciPy 1.18.0, SymPy 1.14.0, and mpmath 1.3.0. The five recorded numerical
thread-control environment variables remained unset; an effective BLAS
thread count was not measured, so cross-platform last-bit identity is not
claimed.

The calculation retained 2,192 predeclared slots, including 894 endpoint
records, 447 centered-\(D_2\) records, 126 fixed-R4 vectors, 90 local-RHS
directions, 540 local perturbations, and 32 cause records. All 915 solver
attempts passed; no fallback solver was used.

## 2. Fixed derivative problem

The root parameter order is

\[
(y_{a_1},y_{\phi_1},y_{a_2},y_{\phi_2},y_{a_3},y_{\phi_3},\psi,
u_1,u_2,u_3,u_4,u_5,u_6,T),
\]

and the suspect chart coordinate is zero-based column 8, \(u_2\). The
stored root Jacobian uses

\[
J=\operatorname{diag}(\text{row scales})[V_\Gamma,-V_K],
\]

so column 13 is the negative row-scaled flow-time tangent. No sign is
chosen from an observed determinant.

For the realified residual \(F\), the independent finite differences are

\[
D_{2,j}(h)=\frac{F(p_*+he_j)-F(p_*-he_j)}{2h},
\]

\[
R_{4,j}(h)=\frac{4D_{2,j}(h/2)-D_{2,j}(h)}{3}.
\]

The primary reference is fixed in advance as \(R_{4,j}(2\times10^{-4})\),
with neighbors at \(4\times10^{-4}\) and \(10^{-4}\). The old Phase-41
steps are replayed in their original order, while a tight DOP853 tier, a
realified Radau tier, an affine-chart calculation, and a same-base,
same-first-tangent geodesic control are retained separately. No failed or
unfavorable step can be skipped in favor of a later one.

The local transported-tangent identity is tested directly in \(\xi\)-space:

\[
D\,\mathrm{flow}_\xi(\xi)[q]=-\overline{H_\xi(\xi)q}.
\]

For the orientation control, positive column normalization gives

\[
A_V=J_VD_V^{-1},\qquad A_R=J_RD_R^{-1},
\]

\[
E=A_V^{-1}(A_R-A_V),\qquad \eta=\lVert E\rVert_2,
\]

where the implementation uses a linear solve, not an explicit inverse. The
condition \(\eta<1\) is only a sufficient certificate that
\(A_V(I+tE)\) stays nonsingular for \(0\le t\le1\).

## 3. Contract ledger

All eight exact/protocol contracts passed:

| exact contract | status |
|---|---:|
| P42.freeze.two_stage_artifacts_and_environment | PASS |
| P42.checkpoint.strict_integrity_and_cross_identities | PASS |
| P42.freeze.checkpoint_only_fixed_roots_no_retune | PASS |
| P42.map.order_steps_tiers_and_root_sign | PASS |
| P42.math.fixed_Richardson_metrics_and_homotopy | PASS |
| P42.guard.chart_geodesic_and_real_directional_scope | PASS |
| P42.retention.complete_declared_slot_schema | PASS |
| P42.guard.fail_closed_global_outputs | PASS |

The eight numerical contracts are:

| numerical contract | typed status | pass |
|---|---|---:|
| P42.reproduction.fixed_checkpoint_and_three_way_J | PASS | yes |
| P42.reproduction.phase41_failed_FD_negative_control | PASS | yes |
| P42.chart.initial_tangent_and_fixed_curvature | PASS | yes |
| P42.variational.local_RHS_and_time_column | LOCAL_VARIATIONAL_IDENTITY_NOT_SUPPORTED | **no** |
| P42.derivative.all_column_fixed_R4 | REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE | **no** |
| P42.derivative.u2_solver_disentanglement | PASS | yes |
| P42.orientation.normalized_sufficient_homotopy | PASS | yes |
| P42.classification.complete_tri_state_cause_ledger | PASS | yes |

Neither non-PASS scientific contract invalidates the run. By contrast,
checkpoint/platform drift or an incomplete cause ledger would have produced
**INVALID_RUN** and exit 2; neither occurred.

## 4. Exact reproduction of the Phase-41 failure

The unchanged Phase-41 production reintegration reproduces every retained
checkpoint center state, residual, Gamma/K frame, and Jacobian with maximum
absolute discrepancy exactly \(0\) in this run. The old finite-difference
selection rule then reproduces the same sole failed column at every point:

| point | old FD / production-\(J\) operator error | old \(u_2\) plateau | failed columns | root sign |
|---|---:|---:|---:|---:|
| shared_zero | \(1.64506\times10^{-3}\) | \(2.98850\times10^{-1}\) | 8 | \(-1\) |
| phi_plus | \(7.73922\times10^{-4}\) | \(2.21993\times10^{-1}\) | 8 | \(-1\) |
| a_plus | \(1.35951\times10^{-3}\) | \(7.95272\times10^{-1}\) | 8 | \(-1\) |

The frozen plateau threshold is \(2\times10^{-2}\). Thus the old
finite-difference matrix has the correct root sign and a small whole-matrix
operator error, but its first adjacent \(u_2\) pair is decisively unstable.
This is why Phase 41 remains **TANGENT_CONTROL_FAILED** rather than being
retroactively reclassified.

The independent tight augmented integration remains close to the frozen
checkpoint Jacobian:

| point | relative operator error | relative \(u_2\)-column error | signs (checkpoint, production, tight) |
|---|---:|---:|---:|
| shared_zero | \(7.63578\times10^{-8}\) | \(1.32037\times10^{-7}\) | \((-1,-1,-1)\) |
| phi_plus | \(2.22089\times10^{-8}\) | \(1.27622\times10^{-7}\) | \((-1,-1,-1)\) |
| a_plus | \(1.02010\times10^{-7}\) | \(3.80606\times10^{-7}\) | \((-1,-1,-1)\) |

These pass the separate \(5\times10^{-3}\) three-way comparison threshold.
They do not, by themselves, validate the local variational differential
equation or select a unique explanation for the old small-step plateau.

## 5. Fixed R4 references and the one reference failure

The all-column \(R_4\) audit gives:

| point | full \(R_4\leftrightarrow J_{\rm checkpoint}\) | full \(R_4\leftrightarrow J_{\rm tight}\) | \(u_2\) neighbor stability | point result |
|---|---:|---:|---:|---:|
| shared_zero | \(1.13845\times10^{-5}\) | \(1.14249\times10^{-5}\) | \(5.97045\times10^{-3}\) | FAIL |
| phi_plus | \(1.15550\times10^{-5}\) | \(1.15542\times10^{-5}\) | \(7.52420\times10^{-4}\) | PASS |
| a_plus | \(6.15281\times10^{-6}\) | \(6.12347\times10^{-6}\) | \(3.56365\times10^{-3}\) | PASS |

The frozen internal-neighbor limit is \(5\times10^{-3}\). Only the
shared-zero \(u_2\) reference exceeds it. At that same point the primary
\(R_4\) column is nevertheless close in direction and norm to both tangent
columns:

~~~text
R4 to checkpoint symmetric relative error = 4.80909e-4
R4 to tight symmetric relative error      = 4.81038e-4
signed cosines                             = 0.9999998844, 0.9999998843
~~~

The failure is therefore specifically an internal reference-stability
failure. It is not a detected sign reversal or a gross directional
mismatch. Because the all-column contract quantifies over all three roots,
this single frozen failure makes the promoted reference-tangent conclusion
inconclusive.

The affine-chart algebra itself passes independently. The fixed curvature
envelopes \(E_{\rm chart}\) are \(3.47678\times10^{-3}\),
\(3.73767\times10^{-3}\), and \(1.21851\times10^{-3}\) at shared-zero,
phi-plus, and a-plus, respectively. The same-base and same-first-tangent
geodesic identities have zero reported error, and all 80-decimal-to-double
chart comparisons are at the \(10^{-16}\) level. Consequently chart
curvature is not supported as the cause at any point.

## 6. Protocol-defined local variational anomaly

Each root has 30 local Hessian-action tests: six transported chart directions
at five flow fractions. Twenty-nine of the thirty directions at each point
pass the frozen \(10^{-6}\) neighbor-stability prerequisite. Within those
stable records, many exceed the \(10^{-7}\) analytic-identity threshold:

| point | stable directions | stable violations | largest local identity error |
|---|---:|---:|---:|
| shared_zero | 29/30 | 12 | \(1.02182\times10^{-6}\) |
| phi_plus | 29/30 | 11 | \(6.86555\times10^{-7}\) |
| a_plus | 29/30 | 10 | \(6.84762\times10^{-7}\) |

These stable local Hessian-action violations—and only these violations—are
the evidence used in this report for the frozen
**VARIATIONAL_RHS_BUG_EVIDENCE** label. One unstable direction at each point
does not erase the existential rule because multiple other complete,
finite, reference-stable slots violate the threshold.

There is an important time-column limitation. The Phase-41 time tangent is
not an independently integrated tangent column: it is appended from
\(\mathrm{flow}_\xi\) evaluated at the final augmented endpoint. Phase 42
also evaluates the RHS at independently integrated state-only endpoints.
Their relative discrepancies are
\(2.14308\times10^{-7}\), \(1.44258\times10^{-7}\), and
\(1.36552\times10^{-7}\) at shared-zero, phi-plus, and a-plus. The
corresponding production/tight/Radau endpoint-RHS envelopes are of the same
order, \(1.17\text{--}1.50\times10^{-7}\). Those numbers diagnose
solver/endpoint-state sensitivity; they are **not** independent evidence of
an RHS implementation bug and are not used here to strengthen the label.

Accordingly, “bug evidence” is retained only as the protocol's name for a
local numerical anomaly. It neither establishes a code defect nor locates a
faulty line, and it does not prove that the underlying continuum equation is
wrong.

## 7. \(u_2\) solver and step behavior

At the exact old \(u_2\) steps \(2\times10^{-6}\), \(5\times10^{-7}\), and
\(10^{-7}\), the production-to-tight derivative discrepancies increase as
the step shrinks:

| point | \(e(2\times10^{-6})\) | \(e(5\times10^{-7})\) | \(e(10^{-7})\) |
|---|---:|---:|---:|
| shared_zero | 0.166675 | 0.384777 | 1.061281 |
| phi_plus | 0.197547 | 0.316145 | 0.758829 |
| a_plus | 0.290406 | 0.469538 | 0.551459 |

The monotone behavior and both frozen pair-envelope inequalities support
**SOLVER_NOISE_EVIDENCE** at phi-plus and a-plus. At shared-zero, the same
pattern is present, but the fixed \(R_4\) reference is not stable enough for
the cause prerequisite, so the pointwise verdict is **INCONCLUSIVE**.

At phi-plus and a-plus, the old first-pair plateau fails while all
preselected Phase-42 reference, direction, norm, cross-method, and sufficient
homotopy tests pass. This supports **STEP_PAIR_SELECTION_ARTIFACT** there. It
is **NOT_SUPPORTED** at shared-zero because the fixed reference fails its
neighbor threshold; no later favorable pair is substituted.

The two fixed central-order conditions required for
**TRUNCATION_EVIDENCE** do not hold. For example, the two leading fixed
\(q_2\) values are approximately

~~~text
shared_zero: -0.660, -3.726
phi_plus:    -2.564,  1.960
a_plus:       0.191, -1.160
~~~

rather than lying in \([1.5,2.5]\) for both declared triples. Truncation is
therefore **NOT_SUPPORTED** at all three points under the frozen rule.

## 8. Sufficient local orientation certificate

Despite the one all-column reference-stability failure, the separately
defined normalized linear-homotopy contract passes at every point:

| point | \(\eta\) | \(1-\eta\) | \(\sigma_{\min}(A_V)\) | \(\sigma_{\min}(A_R)\) | endpoint signs |
|---|---:|---:|---:|---:|---:|
| shared_zero | \(4.03348\times10^{-4}\) | 0.999597 | 0.0207717 | 0.0207720 | \(-1,-1\) |
| phi_plus | \(1.00569\times10^{-3}\) | 0.998994 | 0.0207678 | 0.0207678 | \(-1,-1\) |
| a_plus | \(7.96500\times10^{-4}\) | 0.999203 | 0.0207923 | 0.0207922 | \(-1,-1\) |

The rounding budget is \(10^{-8}\); solve backward residuals range from
\(1.84\times10^{-17}\) to \(4.72\times10^{-17}\). Positive-rescaling and
single-column-flip mutation controls pass, and no sampled \(t\) grid is used
as a proof.

This certifies only a nonsingular local path between two normalized
fourteen-by-fourteen matrices in the declared coordinate frames. It does
not construct a determinant line, orient a full upward cycle, identify the
physical original contour, or repair the failed reference-tangent contract.

## 9. Complete pointwise tri-state cause ledger

Every point/cause record has completion status **COMPLETE**. The independent
evidence status is shown below. SUP, NO, and INC mean **SUPPORTED**,
**NOT_SUPPORTED**, and **INCONCLUSIVE**.

| cause | shared-zero | phi-plus | a-plus | any-fixed-point aggregate |
|---|---:|---:|---:|---:|
| truncation | NO | NO | NO | NOT_SUPPORTED |
| solver noise | INC | SUP | SUP | **SUPPORTED** |
| chart curvature | NO | NO | NO | NOT_SUPPORTED |
| old step-pair selection artifact | NO | SUP | SUP | **SUPPORTED** |
| variational RHS anomaly evidence | SUP | SUP | SUP | **SUPPORTED** |
| original production tangent solver | INC | INC | INC | INCONCLUSIVE |
| integrated variational evolution bug | INC | INC | INC | INCONCLUSIVE |
| UNRESOLVED | NO | NO | NO | NOT_SUPPORTED |

The two downstream labels—original production tangent-solver evidence and
integrated-variational-evolution evidence—require local RHS anomaly evidence
to be **NOT_SUPPORTED**. Because it is instead supported at every root, those
labels remain inconclusive; the computation does not pretend to separate
them by conditioning on a failed prerequisite.

**UNRESOLVED=NOT_SUPPORTED** does not mean that one unique cause has been
proved. Under the frozen rule it means that each point has at least one
stable supported cause or stably excludes all declared causes. Mutual
exclusivity was never imposed. In particular, local RHS mismatch, old-step
solver noise, and first-pair selection sensitivity may all coexist.

## 10. Scientific meaning and nonclaims

Phase 42 narrows the Phase-41 failure in three useful ways:

1. It reproduces the historical small-step \(u_2\) failure without changing
   the roots, chart, solver order, or first-pair rule.
2. It shows that the old-step discrepancy grows as \(h\) shrinks and that a
   coarser, preselected R4 reference is stable at the two nonzero-source
   roots, supporting both solver-noise and step-selection diagnoses there.
3. It finds independent, reference-stable local Hessian-action violations
   at all three roots, so the issue cannot honestly be summarized as only a
   bad finite-difference step pair.

What it does **not** establish is equally important. The computation does
not choose one unique implementation defect, establish a code defect, prove
a continuum variational equation false, or establish a canonical physical
orientation. It audits three fixed roots in one finite m=4 discretization,
one metric, one chart, one launch radius, and one shape. There is no root
census, nonlinear upward manifold, complete cycle, Stokes-chamber
classification, good-end analysis, cutoff limit, or continuum limit.

The mandatory null outputs remain

~~~text
bounded_chain_signed_sum                   = null
complete_global_signed_intersection_vector = null
global_n_sigma                             = null
cutoff_limit                               = null
continuum_limit                            = null
quantum_gravity_explanation                = null
~~~

All seven frozen desired-result fields also remain null, including

~~~text
desired_cause_classification      = null
desired_global_intersection_coefficient = null
desired_homotopy_certificate      = null
desired_local_orientation_sign    = null
desired_phase42_tangent_result     = null
desired_root_jacobian_sign         = null
desired_variational_bug_verdict    = null
~~~

In particular, the protocol-named **VARIATIONAL_RHS_BUG_EVIDENCE** label is
not promoted into a frozen or global variational-bug verdict.

All sixteen promoted completion flags remain **false**, including the
m=2/m=4 action, cycle, and determinant-line identifications; m=3/m=4
canonical-sign and determinant-line identifications; arm, reintersection,
direction-coverage, and root-exhaustion searches; exact nonlinear upward
manifold and component census; non-Stokes chamber and good-end
certification; physical-cycle derivation; metric homotopy; and
BFV/Pfaffian/Pin orientation. Gate 1 remains
**OPEN_PARTIAL_PROGRESS**.

Accordingly:

~~~text
global promotion:          PROHIBITED
determinant-line claim:    false
global-cycle claim:        false
quantum-gravity claim:     false
Phase-41 retroactive 9/9:  false
~~~

## 11. Reproduction and report status

The frozen runner invocation is

~~~bash
.venv/bin/python cpt_temporal_folded_susy/phase42_m4_fixed_root_tangent_disentanglement.py
~~~

The runner writes no repository files and emits one **RESULT_JSON=**
transport record. The committed raw artifact removes that prefix, stores one
compact JSON object followed by one final LF, and preserves the full evidence
rather than only this summary.

This Markdown report was derived from the committed raw result at
**d8c2fce3eb3e72a956a34776970c15642ed88047**; it does not rerun or alter the
calculation. Numerical values in this report are rounded for readability.
The committed JSON, its outer SHA-256, and its self-excluding payload digest
are authoritative whenever a rounded report value or condensed wording is
insufficient.
