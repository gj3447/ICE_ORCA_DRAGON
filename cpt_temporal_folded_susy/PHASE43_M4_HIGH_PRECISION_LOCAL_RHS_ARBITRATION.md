# Phase 43 — m=4 high-precision local RHS arbitration

## Outcome

Phase 43 re-examines the 33 protocol-defined local Hessian-action anomalies
from Phase 42 at all 90 frozen state-and-direction slots. It compares the
byte-pinned Phase-41 NumPy64 local variational RHS with an independently
rebuilt exact-decimal action, an independently differentiated gradient
direction, and fixed 80/120-decimal finite-difference ladders. It completed
with

~~~text
exact contracts:       7 / 7 PASS
numerical contracts:   4 / 6 PASS
run_status:             VALID_TYPED_RUN
process exit:           0
reference corroborated: 90 / 90 slots
source mismatch:        13 / 90 slots
fixed FD rule:          28 / 33 disclosed anomalies
Gate 1:                 OPEN_PARTIAL_PROGRESS
~~~

The two non-PASS numerical records are complete, typed scientific outcomes,
not infrastructure failures:

1. **P43.arbitration.source_RHS_implementation** reports
   **LOCAL_RHS_IMPLEMENTATION_MISMATCH_OR_INCONCLUSIVE** because 13 of the 90
   complete NumPy64 Hessian-action outputs exceed the frozen
   \(5\times10^{-13}\) normwise relative tolerance against the corroborated
   120-decimal reference. The global local-evidence label is therefore
   **LOCAL_RHS_IMPLEMENTATION_MISMATCH_EVIDENCE: SUPPORTED** under its
   precommitted any-slot quantifier.
2. **P43.arbitration.phase42_stable_violations** reports
   **PHASE42_LOCAL_ANOMALY_MIXED_OR_INCONCLUSIVE**. Twenty-eight of the 33
   disclosed Phase-42 stable-violation slots support the fixed same-step
   binary64 finite-difference rule, but five do not because their source RHS
   outputs also cross the \(5\times10^{-13}\) threshold. The frozen global
   rule requires all 33, so its aggregate is **NOT_SUPPORTED**.

These labels are deliberately nonexclusive. In particular, the top-level
protocol label **LOCAL_RHS_IMPLEMENTATION_MISMATCH_SUPPORTED** is not a
winner-takes-all causal verdict. It does not say that one source-code defect
explains the Phase-42 anomalies, and the all-33 finite-difference aggregate
being **NOT_SUPPORTED** does not show that binary64 finite-difference error is
absent. Phase 41 remains 8/9 numerical, the Phase-42 reference tangent remains
**REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE**, and integrated tangent
evolution is still **NOT_TESTED_LOCAL_ONLY**.

## 1. Frozen scope and provenance

The only scientific inputs are the Phase-42 stored states \(\xi\) and
transported directions \(q\) at

~~~text
shared_zero  (delta_a=0,      delta_phi=0)
phi_plus     (delta_a=0,      delta_phi=+0.001)
a_plus       (delta_a=+0.001, delta_phi=0)
~~~

for five fixed flow fractions and six fixed transported directions per
point. Thus the scope is exactly

\[
3\ \text{points}\times5\ \text{fractions}\times6\ \text{directions}=90
\]

local slots. The Phase-42 result was already known when this input was
frozen. Phase 43 is a post-hoc diagnostic, not a preregistration. A disclosed
read-only design pilot preceded the production run; its values were not
imported into the result, and the thresholds were not changed after the
pilot.

The authoritative Phase-43 artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | 91a15d9a8d0c000e1ce7c7d8d83f399b600cff55 | de2c8c130e1aae6b6b93ee4c3d1137357067f9ddd5e8c68916037f2ffc325b39 |
| committed runner | 4aa3887cec14816c92ff8635d2cac703d4661d37 | 01e0727d2269f6b2d555455157b1c49cda96fb4966fb00eab5b3635d690f3729 |
| raw result | 11a8cfd7910f6b016b4dbceefd839bf6ac093f03 | 20c967ff968541402c81d5ab91394820bffd15cdd79052ee9e162cb5f39c2bd8 |

The raw result is a 50,974,375-byte compact JSON artifact with schema
**ice-phase43-high-precision-local-rhs-arbitration/v1**. Its canonical
self-excluding payload digest is

~~~text
2670f1117433c962b5d3cfe265293ad85a89571f6a06a13342471e11d8ca9fa0
~~~

The result also verifies the immutable Phase-42 raw result at commit
**d8c2fce3eb3e72a956a34776970c15642ed88047**, outer SHA-256
**568e02cc8c4d730aba3a7a83febd3aa41cf14dfdb87b53950cc6fcc78c5bd013**,
and the Phase-42 checkpoint at commit
**731579c37867a2041b65359bfc649be3b66900c7**, outer SHA-256
**ad51bac8eff42e4d300b7872886053c1a6110812ed43b57cdd0e4dbf961891c6**.
The production target is the Phase-41 executable at commit
**a31a8627b0e0e210dea96d1d69dad80ccaa6decd**, SHA-256
**377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530**.

All start/end HEAD, source, runner, runtime, worktree, and repository-pycache
comparisons passed. The production runtime was CPython 3.13.5 with NumPy
2.5.2, SciPy 1.18.0, SymPy 1.14.0, and mpmath 1.3.0. Every one of the 13,606
predeclared records terminated as **SUCCESS**:

| slot kind | count |
|---|---:|
| frozen inputs | 90 |
| source analytic / endpoints / \(D_2\) / \(R_4\) / summaries | 1,170 |
| independent analytic references | 540 |
| same-step endpoints / \(D_2\) / \(R_4\) | 3,960 |
| prospective endpoints / \(D_2\) / \(R_4\) | 7,560 |
| slot classifications | 270 |
| point and global aggregates | 14 |
| symbolic model and boundary audits | 2 |
| **total** | **13,606** |

No root, saddle, least-squares, ODE, dense-output, chart-transport, or
trajectory solver was run. No time column was evaluated. Consequently this
phase cannot test integrated tangent evolution or add new evidence about an
ODE solver-noise component.

## 2. Local derivative problem and fixed metrics

For the frozen affine map

\[
w(\xi)=w_*+L\xi,
\]

the independently rebuilt local flow and Hessian action are

\[
V(\xi)=-\overline{L^T G_w(w(\xi))},
\qquad
A_H(\xi,q)=-\overline{L^T H_w(w(\xi))Lq}.
\]

The second analytic path introduces a real \(\epsilon\), differentiates
\(L^TG_w(w_*+L(\xi+\epsilon q))\) componentwise, sets \(\epsilon=0\), and
then applies the outer conjugation. It is evaluated separately from the
constructed Hessian object. Both paths come from the same independently
rebuilt four-element action; their agreement checks differentiation and
evaluation consistency, not the physical correctness of the finite model.

The comparison metric used for every scientific threshold is the normwise
symmetric relative error

\[
\operatorname{rel}(x,y)=
\frac{\lVert x-y\rVert_2}
{\max(\lVert x\rVert_2,\lVert y\rVert_2,10^{-100})}.
\]

Maximum componentwise relative errors are retained as diagnostics but are
not acceptance metrics. This distinction matters for components close to
zero.

The frozen thresholds are:

| comparison | threshold |
|---|---:|
| Phase-42 source-vector reproduction, max absolute component | \(5\times10^{-15}\) |
| exact-decimal versus 50-digit coefficient-rounding control | \(10^{-40}\) |
| Hessian versus direct-gradient path | \(10^{-50}\) |
| 80 versus 120 decimal precision stability | \(10^{-50}\) |
| unchanged Phase-42 same-step high-precision \(R_4\) versus symbolic | \(10^{-12}\) |
| prospective primary \(h=10^{-12}\) \(R_4\) versus symbolic | \(10^{-30}\) |
| prospective primary/coarse/fine neighbor stability | \(10^{-28}\) |
| source NumPy64 Hessian action versus 120-decimal reference | \(5\times10^{-13}\) |
| reproduced Phase-42 stable-violation threshold | \(10^{-7}\) |
| reproduced Phase-42 neighbor-stability threshold | \(10^{-6}\) |

The unchanged same-step calculation uses both the Phase-42 binary64-rounded
normalization geometry and a native-mpmath normalization geometry. The
prospective ladder retains every predeclared
\(h\in\{10^{-6},10^{-8},10^{-10},10^{-12},10^{-14},10^{-16}\}\) at 80 and
120 decimal digits. No observed value selects a replacement step.

## 3. Contract ledger

All seven exact/protocol contracts passed:

| exact contract | status |
|---|---:|
| P43.freeze.committed_artifacts_runner_and_environment | PASS |
| P43.input.strict_phase42_state_identity | PASS |
| P43.scope.local_only_no_solver_or_time_column | PASS |
| P43.symbolic.independent_action_and_directional_identity | PASS |
| P43.math.binary64_lift_precision_ladders_and_metrics | PASS |
| P43.retention.complete_slot_and_classification_schema | PASS |
| P43.guard.fail_closed_gate1_and_null_outputs | PASS |

The six numerical contracts are:

| numerical contract | typed status | pass |
|---|---|---:|
| P43.reproduction.phase42_local_source_controls | PASS | yes |
| P43.reference.independent_symbolic_and_precision_agreement | PASS | yes |
| P43.reference.same_step_and_small_step_R4 | PASS | yes |
| P43.arbitration.source_RHS_implementation | LOCAL_RHS_IMPLEMENTATION_MISMATCH_OR_INCONCLUSIVE | **no** |
| P43.arbitration.phase42_stable_violations | PHASE42_LOCAL_ANOMALY_MIXED_OR_INCONCLUSIVE | **no** |
| P43.classification.complete_nonexclusive_local_ledger | PASS | yes |

The two non-PASS records are valid threshold outcomes and leave process exit
0. Artifact, source, symbolic-identity, reproduction, or retention drift
would instead have emitted **INVALID_RUN** with exit 2; none occurred.

## 4. The high-precision reference is corroborated at 90/90 slots

Every slot passes the independent analytic, precision, same-step, and
prospective-reference prerequisites. The largest normwise errors over all
90 slots are:

| control | observed maximum | frozen maximum |
|---|---:|---:|
| Hessian versus direct-gradient, 80 dps | \(4.47104\times10^{-77}\) | \(10^{-50}\) |
| Hessian versus direct-gradient, 120 dps | \(8.29849\times10^{-117}\) | \(10^{-50}\) |
| Hessian 80 versus 120 dps | \(3.48408\times10^{-77}\) | \(10^{-50}\) |
| direct-gradient 80 versus 120 dps | \(5.94033\times10^{-77}\) | \(10^{-50}\) |
| coefficient-rounding control 80 versus 120 dps | \(6.38981\times10^{-77}\) | \(10^{-50}\) |
| exact-decimal versus 50-digit coefficient-rounding control | \(3.39838\times10^{-47}\) | \(10^{-40}\) |
| same-step \(R_4\), lifted binary64 geometry | \(1.45777\times10^{-16}\) | \(10^{-12}\) |
| same-step \(R_4\), native-mpmath geometry | \(4.62718\times10^{-20}\) | \(10^{-12}\) |
| prospective primary \(h=10^{-12}\) | \(2.89199\times10^{-49}\) | \(10^{-30}\) |
| prospective neighbor stability | \(2.89199\times10^{-41}\) | \(10^{-28}\) |

The exact-decimal versus 50-digit coefficient-rounding control therefore
shows that this declared coefficient convention changes the full
Hessian-action vector by at most \(3.40\times10^{-47}\) in the frozen
normwise metric. It does not explain a \(10^{-12}\)-scale source-output
discrepancy.

The retained componentwise diagnostic needs separate wording. Its largest
exact-versus-rounding value is \(7.42360\times10^{-37}\), above
\(10^{-40}\), because some reference components are extremely small. This
does not violate the frozen contract—the acceptance metric is explicitly
normwise—but it is a useful warning that componentwise cancellation and
conditioning have not been resolved.

## 5. The operational NumPy64 source mismatch

For each slot, the production target is exactly

\[
A_{\rm source}=-\overline{
  \texttt{phase41.hessian\_xi}(\xi)q
}.
\]

The Phase-41 source calculation reproduces every stored Phase-42 analytic,
endpoint, \(D_2\), \(R_4\), stability, and violation record exactly in this
runtime; the maximum recorded reproduction error is zero. Against the
corroborated 120-decimal reference, however, 13 slots exceed the separately
frozen \(5\times10^{-13}\) normwise tolerance:

| point | fraction | direction | disclosed Phase-42 anomaly? | source/reference relative error |
|---|---:|---:|---:|---:|
| shared_zero | 0.5 | 2 | yes | \(1.04583\times10^{-12}\) |
| shared_zero | 0.75 | 2 | yes | \(5.97026\times10^{-13}\) |
| shared_zero | 1 | 2 | yes | \(3.03897\times10^{-12}\) |
| shared_zero | 1 | 3 | no | \(3.55650\times10^{-12}\) |
| shared_zero | 1 | 5 | no | \(1.62761\times10^{-12}\) |
| phi_plus | 1 | 2 | no | \(1.08037\times10^{-12}\) |
| phi_plus | 1 | 3 | no | \(1.24734\times10^{-12}\) |
| phi_plus | 1 | 5 | no | \(5.76594\times10^{-13}\) |
| a_plus | 0.25 | 2 | yes | \(1.01266\times10^{-12}\) |
| a_plus | 0.75 | 2 | yes | \(1.08038\times10^{-12}\) |
| a_plus | 1 | 2 | no | \(1.72595\times10^{-12}\) |
| a_plus | 1 | 3 | no | \(2.03467\times10^{-12}\) |
| a_plus | 1 | 5 | no | \(9.28486\times10^{-13}\) |

The remaining 77 slots are within the source threshold. Among the 13
flagged slots, the error range is
\(5.76594\times10^{-13}\) to \(3.55650\times10^{-12}\). Seven flags occur
in direction 2, while directions 3 and 5 contribute three each; nine of the
13 occur at the final fraction. This structured concentration motivates a
conditioning and operation-order audit, but it does not itself identify a
cause.

The label **implementation mismatch** must be read operationally: the
byte-pinned NumPy64 pipeline output crosses a precommitted tolerance against
the mathematical high-precision reference. The current calculation mixes
at least four possible layers:

1. binary64 construction of \(w=w_*+L\xi\),
2. binary64 evaluation of the symbolic Hessian at that state,
3. matrix contraction and association order in \(L^TH_wLq\), and
4. cancellation or conditioning in small components and directions.

Phase 43 does not separate those layers. It therefore does not establish a
wrong symbolic formula, an integrated tangent-equation bug, or a unique
source-code defect.

### Report-time symbolic cross-check, not Phase-43 production evidence

Outside the production run, a read-only in-memory report audit compared the
actual Phase-41 `hessian_expr` with the independently rebuilt 50-digit
coefficient model. The expressions are not literally componentwise identical
after simplification because the two constructions introduce finite-precision
SymPy Floats and substitutions in different orders. Evaluating the actual
Phase-41 expression at 120 decimal digits nevertheless gave these largest
90-slot normwise discrepancies:

| read-only comparison | observed maximum |
|---|---:|
| Phase-41 expression at 120 dps versus independent 50-digit model | \(5.36233\times10^{-47}\) |
| Phase-41 expression at 120 dps versus exact-decimal model | \(6.21304\times10^{-47}\) |
| independent 50-digit model versus exact-decimal model | \(3.39838\times10^{-47}\) |

This unarchived audit was not predeclared, is not in the raw result, and is
not admissible as a new Phase-43 contract pass. It only shows why the current
report must distinguish a tiny construction-order difference from the much
larger \(10^{-12}\)-scale NumPy64 output discrepancy. A committed follow-up
must perform and retain this source-expression comparison before claiming
that formula-level drift has been excluded.

## 6. Why 28/33 does not promote the all-33 finite-difference claim

The fixed finite-difference evidence rule applies only to the 33 disclosed
Phase-42 stable-violation slots. A slot is **SUPPORTED** only when all of the
following hold simultaneously:

1. the stored binary64 same-step \(R_4\) discrepancy remains above
   \(10^{-7}\),
2. the stored neighbor comparison remains at or below \(10^{-6}\),
3. the source NumPy64 Hessian action agrees with the corroborated reference
   within \(5\times10^{-13}\), and
4. the 120-decimal same-step \(R_4\) in both normalization modes agrees with
   the symbolic reference within \(10^{-12}\).

The pointwise histograms are:

| point | reference corroborated | source mismatch, all 30 | disclosed anomalies | FD SUPPORTED | FD NOT_SUPPORTED |
|---|---:|---:|---:|---:|---:|
| shared_zero | 30/30 | 5/30 | 12 | 9 | 3 |
| phi_plus | 30/30 | 3/30 | 11 | 11 | 0 |
| a_plus | 30/30 | 5/30 | 10 | 8 | 2 |
| **total** | **90/90** | **13/90** | **33** | **28** | **5** |

At phi-plus, all 11 disclosed anomalies support the fixed finite-difference
rule. Its three source-mismatch slots are all outside that 11-slot cohort.
This is a concrete example of why the any-slot source aggregate cannot be
read as the unique cause of the Phase-42 anomaly cohort.

The five all-33 failures are exactly:

| point | fraction | direction | old Phase-42 FD discrepancy | source/reference discrepancy | old/source ratio | largest HP same-step error |
|---|---:|---:|---:|---:|---:|---:|
| shared_zero | 0.5 | 2 | \(4.90725\times10^{-7}\) | \(1.04583\times10^{-12}\) | \(4.692\times10^5\) | \(8.094\times10^{-17}\) |
| shared_zero | 0.75 | 2 | \(4.97496\times10^{-7}\) | \(5.97026\times10^{-13}\) | \(8.333\times10^5\) | \(4.889\times10^{-17}\) |
| shared_zero | 1 | 2 | \(6.58678\times10^{-7}\) | \(3.03897\times10^{-12}\) | \(2.167\times10^5\) | \(2.976\times10^{-17}\) |
| a_plus | 0.25 | 2 | \(6.84762\times10^{-7}\) | \(1.01266\times10^{-12}\) | \(6.762\times10^5\) | \(1.147\times10^{-17}\) |
| a_plus | 0.75 | 2 | \(2.18247\times10^{-7}\) | \(1.08038\times10^{-12}\) | \(2.020\times10^5\) | \(1.332\times10^{-17}\) |

Thus all five fail solely because condition 3 crosses its frozen threshold;
their high-precision same-step controls pass comfortably. Moreover, their
old finite-difference discrepancies are at least \(2.02\times10^5\) times
larger than their source/reference discrepancies in the same normwise
metric. The source mismatch therefore cannot by magnitude alone explain the
old Phase-42 discrepancy. Both numerical effects may coexist.

The global finite-difference aggregate uses a universal quantifier:

~~~text
SUPPORTED     iff all 33 disclosed anomaly slots are SUPPORTED
NOT_SUPPORTED if all 33 are complete and at least one is NOT_SUPPORTED
INCONCLUSIVE  otherwise
~~~

All 33 are complete, but five are **NOT_SUPPORTED**, so the frozen aggregate
is correctly **NOT_SUPPORTED**. This is a failed sufficient all-slot claim,
not proof of the negation “binary64 finite-difference arithmetic contributed
to none of the anomalies.” The other 57 slots are retained but excluded from
this quantified anomaly claim by construction.

## 7. Allowed interpretation and forbidden promotion

The strongest result-supported statement is:

> At 13 of 90 frozen local m=4 state-and-direction slots, the byte-pinned
> Phase-41 NumPy64 Hessian-action output exceeds the precommitted
> \(5\times10^{-13}\) normwise tolerance against a corroborated 120-decimal
> reference. Under the separate frozen all-33 rule, 28 of the 33 disclosed
> Phase-42 stable finite-difference anomalies support same-step binary64
> arithmetic evidence; the global rule is not supported because five slots
> also cross the source-output tolerance.

This is a finite, local, implementation-level numerical statement. It is
not any of the following:

- proof that the Phase-41 symbolic Hessian formula is wrong;
- proof of one unique code defect or one unique cause;
- validation or falsification of integrated tangent evolution;
- a new ODE solver-noise result;
- restoration of Phase 41 from 8/9 to 9/9 numerical contracts;
- resolution of the Phase-42 reference tangent;
- a local orientation or determinant-sign computation;
- a bounded-chain or global signed-intersection coefficient;
- a construction of the original regulated joint cycle;
- a cutoff or continuum limit; or
- evidence for SUSY, holography, emergent spacetime, or quantum gravity.

The Phase-42 protocol label **VARIATIONAL_RHS_BUG_EVIDENCE** remains a
historical local anomaly label. Phase 43 narrows its interpretation: a
corroborated high-precision derivative exists, the old binary64
finite-difference anomaly is reproduced, and a smaller NumPy64 source-output
mismatch is also present at selected frozen slots. The word “bug” must not be
promoted beyond that protocol history.

## 8. Fail-closed Gate-1 boundary

All 16 promoted prerequisites remain exactly false:

1. m=2 and m=4 actions identified;
2. m=2 and m=4 upward cycles identified;
3. m=2 and m=4 common determinant line constructed;
4. m=3 and m=4 canonical sign equality proved;
5. m=3 and m=4 common determinant line constructed;
6. straight-arm intersections searched;
7. cap reintersections searched;
8. continuous direction coverage proved;
9. root exhaustion proved;
10. exact nonlinear upward manifold certified;
11. all saddles and upward components complete;
12. non-Stokes chamber certified;
13. all relative good ends classified;
14. physical original cycle derived;
15. metric homotopy tested; and
16. BFV/Pfaffian/Pin orientation computed.

All six promoted outputs remain null:

~~~text
bounded_chain_signed_sum
complete_global_signed_intersection_vector
global_n_sigma
cutoff_limit
continuum_limit
quantum_gravity_explanation
~~~

All seven desired scientific outputs in the Phase-43 input freeze also
remain null. No desired verdict, sign, or coefficient was written into the
input. The retained boundary is therefore

~~~text
Phase 41 numerical contracts:  8/9
Phase 41 tangent status:        TANGENT_CONTROL_FAILED
Phase 42 reference tangent:     REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE
integrated tangent evolution:   NOT_TESTED_LOCAL_ONLY
ODE solver-noise component:     NOT_TESTED_LOCAL_ONLY
global promotion:               PROHIBITED
Gate 1:                         OPEN_PARTIAL_PROGRESS
~~~

Local high-precision agreement is not a global intersection invariant. A
null global coefficient is not zero, and an untested integrated tangent is
not a negative result.

## 9. Minimal next calculation: Phase 44 arithmetic provenance

The next smallest admissible calculation is not another global intersection
search. It is a frozen all-90-slot arithmetic-provenance audit of the 13
NumPy64 source mismatches, with the 13 disclosed flags treated as a complete
negative-control cohort rather than a selected favorable sample.

A Phase-44 input should be committed before implementation and should fix:

1. **Source-expression identity.** Canonically rename variables and compare
   the actual Phase-41 `hessian_expr` with the independently rebuilt
   50-digit model componentwise, retaining both exact identities and any
   finite-precision construction-order residuals.
2. **Intermediate pipeline states.** Retain the exact binary64 values and
   high-precision lifts of
   \(w_{64}=\mathrm{fl}(w_*+L\xi)\), \(H_{64}(w_{64})\), \(Lq\),
   \(L^TH_{64}L\), and the final action.
3. **Fixed hybrid decomposition.** With one preregistered replacement order,
   separately measure state-formation rounding, Hessian-evaluator rounding,
   \(L^THL\) contraction rounding, and the final matrix-vector rounding.
   Because these effects can interact, the labels must remain nonexclusive.
4. **Operation-order controls.** Compare the source left-associated order,
   \((L^TH)Lq\), with \(L^T(H(Lq))\), explicit fixed-order loops, pairwise or
   compensated sums, and a pinned extended-precision control. No observed
   result may choose a preferred order retroactively.
5. **Conditioning and cancellation bounds.** Retain rowwise
   \(\sum_j|t_{ij}|/|\sum_jt_{ij}|\), a normwise absolute-condition proxy such
   as
   \(\lVert |L^T||H||L||q|\rVert_2/\lVert L^THLq\rVert_2\), and fixed
   \(\gamma_n\)-style forward-error envelopes.
6. **Tri-state, nonexclusive outcomes.** Keep separate labels for symbolic
   formula drift, state-formation rounding, Hessian-evaluation rounding,
   contraction-order/cancellation effects, and unresolved numerical
   pipeline behavior. A failed stage must not be relabeled as another cause.

Phase 44 should again perform zero root, ODE, time-column, orientation, or
global-cycle evaluations. Only after a numerically stable local RHS has been
established should a separately frozen later phase reintegrate the tangent
equation. Even that reintegration would remain local evidence and would not
close Gate 1 by itself.

## Bottom line

Phase 43 refines the broad Phase-42 local anomaly into a more
specific, fully retained numerical picture:

~~~text
high-precision local reference:        corroborated at 90/90
NumPy64 source-output tolerance:       crossed at 13/90
Phase-42 anomaly FD rule:              supported at 28/33
strict all-33 FD aggregate:            NOT_SUPPORTED
integrated tangent / root / ODE:       not tested
global cycle or intersection claim:    prohibited
Gate 1:                                OPEN_PARTIAL_PROGRESS
~~~

The result is progress because it separates local mathematical derivative
agreement from the operational binary64 pipeline. It is not yet the finite-
cutoff joint action, the original regulated cycle, or the full oriented
intersection determinant requested by Gate 1.
