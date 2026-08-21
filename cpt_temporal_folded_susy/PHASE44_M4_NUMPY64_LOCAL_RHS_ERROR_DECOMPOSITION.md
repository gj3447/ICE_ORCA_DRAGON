# Phase 44 — m=4 NumPy64 local RHS error decomposition

## Outcome

Phase 44 traces the complete Phase-41 NumPy64 Hessian-action pipeline at all
90 frozen Phase-43 state-and-direction slots. It compares an independently
rebuilt exact action with the source expression, forms the fixed eight-stage
hybrid telescope, interprets every generated Hessian AST in source order,
checks six predeclared contraction alternatives, and propagates one fixed
binary64 forward-error model. The committed production run completed with

~~~text
exact contracts:                  8 / 8 PASS
numerical contracts:              7 / 7 PASS
run_status:                        VALID_TYPED_RUN
process exit:                      0
predeclared records:               13,474 / 13,474 SUCCESS
exact formula identity:            supported at all 3 variants
declared forward-error coverage:   90 / 90 slots
disclosed Phase-43 cohort covered: 13 / 13 slots
control cohort covered:            77 / 77 slots
Gate 1:                            OPEN_PARTIAL_PROGRESS
~~~

The strongest scoped result is
**LOCAL_ROUNDING_CONTRIBUTIONS_MIXED_NONEXCLUSIVE**. All exact action,
gradient, and Hessian comparisons are identical under the declared symbolic
placeholders. Every one of the 13 Phase-43 source-output mismatches, and every
one of the 77 controls, lies inside the same preregistered componentwise and
normwise forward-error model on the pinned runtime. Coefficient formation,
state formation, scalar Hessian evaluation, and contraction arithmetic all
make nonzero resolved contributions at all 90 slots. The fixed cancellation
risk indicator also crosses the Phase-43 scale at all 90 slots.

These are deliberately nonexclusive statements. Coverage does not prove a
unique rounding cause, correct rounding of the generated callable, or absence
of a formula defect outside the exact expressions compared here. The identical
tri-state pattern in the 13-slot and 77-slot cohorts is not a classifier of the
Phase-43 threshold crossings. It instead shows that the full observed local
source/reference discrepancies are compatible with the declared binary64
model and that no residual beyond that model is supported in this frozen
sample.

No root, ODE, integrated tangent, time column, orientation, determinant line,
or global cycle was evaluated. Phase 41 therefore remains 8/9 numerical, the
Phase-42 reference tangent remains
**REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE**, the historical Phase-43
13/90 threshold labels are unchanged, and Gate 1 stays open.

## 1. Frozen scope, execution, and provenance

The input universe is unchanged from Phase 43:

\[
3\ \text{points}\times5\ \text{fractions}\times6\ \text{directions}=90
\]

with the three source variants

~~~text
shared_zero  (delta_a=0,      delta_phi=0)
phi_plus     (delta_a=0,      delta_phi=+0.001)
a_plus       (delta_a=+0.001, delta_phi=0)
~~~

and exactly the 13 disclosed Phase-43 mismatch slots plus 77 controls. The
cohort labels were joined only after the complete key set had been frozen.
Phase 44 is a disclosed post-Phase-43 diagnostic calculation, not a blind
preregistration and not a physical claim.

The authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `03943e8b2b140a5f1b8724d1e2d4439d14964552` | `4680381aae27ff2faec75960c9bc382336efec2b518098c90a257f542eda9044` |
| successful committed runner | `d13af382fe65cc50f74fbc83861e41c0e7236341` | `220123fe069cad3e3178d7e87656cf61240d153d0762041169288c3d9cb9dc52` |
| raw result | `4e75a4fe9ce909fa62794f5a550a3409f6e0fc9f` | `bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75` |

The production command was

~~~bash
./ice run phase44_m4_numpy64_local_rhs_error_decomposition
~~~

The raw result is a 529,370,671-byte compact JSON artifact with schema
**ice-phase44-numpy64-local-rhs-error-decomposition/v1**. Its canonical
self-excluding digest is

~~~text
71fbf86dec8807e6c931c1be279723ce96d91abfa1890bb0782b1cee67f5df8f
~~~

The prefix-free payload SHA-256 is
`43fd5a69e590e0190f0fc8e5c3c2bc5d8cd32848d80b6c7ef79064c08b7d886e`.
External capture validation rejected duplicate keys and nonfinite JSON,
verified 1,392,585 nonzero 120-digit mpmath strings, reproduced canonical
encoding and the self-excluding digest, and checked the full key and terminal
ledger.

An initial run of the first committed runner completed 90/90 slots but exited
2 before emitting a valid scientific result. Its independent constructor used
the local name `action_w`, while its own source denylist rejected that token.
No result from that attempt was committed. Commit `d13af38` renamed only that
local result variable to `independent_action`; the symbolic expression did not
change. A static replay then found zero denylist matches and no `SymPy.Float`
in the exact tree. The successful production result pins that corrected clean
runner and records identical start/end source, runner, runtime, HEAD, worktree,
pycache, and generated-callable fingerprints.

The production runtime was CPython 3.13.5 with NumPy 2.5.2, SciPy 1.18.0,
SymPy 1.14.0, and mpmath 1.3.0. The retained record census is:

| record kind | count |
|---|---:|
| frozen inputs and source boundaries | 180 |
| formula action / gradient / Hessian | 171 |
| callable fingerprints and AST inventories | 6 |
| local and global constant subtrees | 316 |
| whole, entry, and chunk AST trace commitments | 8,730 |
| hybrid stages and deltas | 1,350 |
| alternative contractions | 540 |
| conditioning and forward envelopes | 1,260 |
| slot completion records | 90 |
| tri-state evidence and aggregates | 816 |
| exact and numerical contracts | 15 |
| **total** | **13,474** |

All 13,474 records terminated as **SUCCESS**. The dependency graph contains
816 evidence nodes and 34,530 declared edges; it is acyclic and every target
is declared and successful.

## 2. Equations, conventions, and fixed arithmetic boundaries

The source and independent paths use the same four midpoint-element action
declared in the Phase-43 report and the Phase-44 input manifest. With

\[
w(\xi)=w_*+L\xi,
\]

the local Hessian action is

\[
A(\xi,q)=-\overline{L^T H_w(w(\xi))Lq}.
\]

The independent side rebuilds the four elements from exact `Integer` and
`Rational` constants, symbolic boundary displacements, and seven symbolic
coordinate scales. The source side imports only the byte-pinned Phase-41
pre-substitution action, maps its variables by semantic name, and
differentiates it independently. For each of the three displacement variants,
source minus independent is canonicalized in the fixed order `together`,
`cancel`, `expand` for the action, seven gradient components, and 49 Hessian
components. No machine float is allowed in this identity path.

The production NumPy64 boundaries are exactly

\[
\begin{aligned}
u_{64}&=L\xi,\\
w_{64}&=w_*+u_{64},\\
H_{64}&=H_w(w_{64}),\\
B_{1,64}&=L^T H_{64},\\
B_{2,64}&=B_{1,64}L,\\
y_{64}&=B_{2,64}q,\\
A_{64}&=-\overline{y_{64}}.
\end{aligned}
\]

The generated Hessian callable is parsed and interpreted in its original AST
order. Every operation retains binary64 hex/ratio/signbit identity, its exact
120-decimal counterpart, a local residual, and a fixed error disk. The
interpreter reproduces all 49 complex Hessian entries bit-for-bit at all 90
slots. This traces scalar expression order but makes no claim about private
BLAS or FMA reduction order inside `numpy.matmul`.

The fixed hybrid telescope is:

| stage | only replacement relative to the preceding stage |
|---|---|
| S0 | independent exact-decimal formula, exact operands, exact \(w\) |
| S1 | source coefficient/constant-subtree semantics at exact \(w\) |
| S2 | exact lift of byte-faithful \(w_{64}\) |
| S3 | exact lift of all 49 byte-faithful \(H_{64}\) entries |
| S4 | exact lift of byte-faithful \(B_{1,64}\) |
| S5 | exact lift of byte-faithful \(B_{2,64}\) |
| S6 | exact lift of byte-faithful \(y_{64}\) |
| S7 | exact lift of byte-faithful \(A_{64}\) |

Thus the ordered deltas are

\[
\begin{aligned}
D_{\rm coeff}&=S1-S0,&D_{\rm state}&=S2-S1,\\
D_{\rm Hessian}&=S3-S2,&D_{\rm mm1}&=S4-S3,\\
D_{\rm mm2}&=S5-S4,&D_{\rm mv}&=S6-S5,\\
D_{\rm outer}&=S7-S6.
\end{aligned}
\]

They are signed vectors, not positive weights. Their norms and fractions may
exceed the final discrepancy because different deltas can cancel. No largest
stage is selected as a cause.

## 3. Contract ledger

All eight exact/protocol contracts passed:

| exact contract | status |
|---|---:|
| P44.freeze.committed_artifacts_runner_runtime_and_TOCTOU | PASS |
| P44.input.all_90_phase43_slots_and_13_disclosure_identity | PASS |
| P44.scope.local_arithmetic_only | PASS |
| P44.symbolic.independent_componentwise_canonicalization | PASS |
| P44.trace.byte_faithful_numpy64_boundaries_and_AST | PASS |
| P44.math.fixed_hybrid_contractions_conditioning_and_envelopes | PASS |
| P44.retention.complete_nonexclusive_tri_state_ledger | PASS |
| P44.guard.fail_closed_gate1_and_null_outputs | PASS |

All seven numerical contracts also passed:

| numerical contract | status |
|---|---:|
| P44.reproduction.phase43_source_and_reference_vectors | PASS |
| P44.formula.exact_componentwise_identity | PASS |
| P44.decomposition.hybrid_telescoping_closure | PASS |
| P44.forward_error.all_90_declared_model_coverage | PASS |
| P44.forward_error.all_13_phase43_mismatches_covered | PASS |
| P44.contractions.complete_six_way_all_slot_comparison | PASS |
| P44.classification.complete_nonexclusive_causal_ledger | PASS |

S7 reproduces every stored Phase-43 source action bit-for-bit, S0 reproduces
every stored 120-decimal reference within \(10^{-100}\), and the independently
reconstructed threshold split is exactly 13/77 with point counts 5/3/5.

## 4. Exact formula identity is supported

Every declared exact comparison vanishes:

| comparison | variants | components per variant | nonzero differences |
|---|---:|---:|---:|
| action | 3 | 1 | 0 |
| gradient | 3 | 7 | 0 |
| Hessian | 3 | 49 | 0 |

Accordingly, formula-mismatch evidence is **NOT_SUPPORTED** at all 90 slots.
This establishes identity only for the declared four-element expressions,
symbol mapping, and conventions. It is not a proof that every surrounding
Phase-41 operation, the integrated variational solver, or a physical model is
correct.

## 5. The fixed telescope closes and retains mixed contributions

Every ordered S0-to-S7 telescope closes with zero observed residual in both
the relative and maximum-absolute metrics, inside the fixed \(10^{-100}\)
bounds. The resolved relative deltas over all 90 slots are:

| delta | nonzero slots | median | maximum |
|---|---:|---:|---:|
| \(D_{\rm coeff}\) | 90 | \(2.18324\times10^{-15}\) | \(2.83535\times10^{-12}\) |
| \(D_{\rm state}\) | 90 | \(3.24750\times10^{-15}\) | \(2.73215\times10^{-14}\) |
| \(D_{\rm Hessian}\) | 90 | \(1.15831\times10^{-14}\) | \(1.99152\times10^{-12}\) |
| \(D_{\rm mm1}\) | 90 | \(1.27688\times10^{-16}\) | \(4.37328\times10^{-16}\) |
| \(D_{\rm mm2}\) | 90 | \(8.02187\times10^{-17}\) | \(2.48109\times10^{-16}\) |
| \(D_{\rm mv}\) | 90 | \(6.05765\times10^{-17}\) | \(2.08313\times10^{-16}\) |
| \(D_{\rm outer}\) | 0 | 0 | 0 |

The corresponding fractions of the final Phase-43 discrepancy are not a
partition. For example, the maxima are about 14.06 for coefficient formation,
11.22 for state formation, and 12.97 for Hessian evaluation. Values above one
are direct evidence of cancellation among signed contribution vectors, not an
accounting failure.

The nonexclusive evidence ledger is uniform in both cohorts:

| evidence | disclosed 13 | controls 77 | all 90 |
|---|---:|---:|---:|
| formula mismatch | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED |
| coefficient rounding contribution | SUPPORTED | SUPPORTED | SUPPORTED |
| state rounding contribution | SUPPORTED | SUPPORTED | SUPPORTED |
| Hessian rounding contribution | SUPPORTED | SUPPORTED | SUPPORTED |
| contraction rounding contribution | SUPPORTED | SUPPORTED | SUPPORTED |
| cancellation capable of Phase-43 scale | SUPPORTED | SUPPORTED | SUPPORTED |
| declared forward-error coverage | SUPPORTED | SUPPORTED | SUPPORTED |
| unresolved beyond declared model | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED |

Here **SUPPORTED** for a contribution means the fixed resolved delta exceeds
the preregistered \(10^{-90}\) detection floor. It does not mean that the
stage alone explains the final discrepancy.

## 6. The declared forward-error model covers all 90 slots

The model fixes \(u=2^{-53}\) and

\[
\gamma_k=\frac{ku}{1-ku}.
\]

It uses one ulp for Python literal and NumPy-pi formation, eight ulps per
component for the pinned NumPy sqrt, exp, division, and integer-power local
models, operation-aware scalar AST disks, a state-formation disk, and three
sequential \(\gamma_{56}\) source-contraction disks. These are frozen
platform assumptions, not universal libm theorems.

The largest observed envelope utilizations are:

| envelope | max norm utilization | max component utilization | covered slots |
|---|---:|---:|---:|
| coefficient formation | 0.009951 | 0.05650 | 90/90 |
| state formation | 0.08978 | 0.34052 | 90/90 |
| scalar Hessian AST | 0.01109 | 0.05914 | 90/90 |
| first matrix product | 0.008619 | 0.02042 | 90/90 |
| second matrix product | 0.03297 | 0.03944 | 90/90 |
| matrix-vector product | 0.03351 | 0.03733 | 90/90 |
| outer conjugation/negation | 0 | 0 | 90/90 |
| **complete source chain** | **0.009768** | **0.01782** | **90/90** |

Every utilization is below the frozen limit of one. The separately retained
a-posteriori observed-residual accounting also contains every actual Hessian
error, but it is not used as the prospective coverage predicate.

The source/reference relative discrepancies themselves span:

| cohort | count | minimum | median | maximum |
|---|---:|---:|---:|---:|
| disclosed mismatch | 13 | \(5.76594\times10^{-13}\) | \(1.08038\times10^{-12}\) | \(3.55650\times10^{-12}\) |
| control | 77 | \(2.07196\times10^{-16}\) | \(5.53911\times10^{-15}\) | \(4.28522\times10^{-13}\) |
| all slots | 90 | \(2.07196\times10^{-16}\) | \(1.06276\times10^{-14}\) | \(3.55650\times10^{-12}\) |

The unchanged Phase-43 threshold is \(5\times10^{-13}\). Phase 44 does not
erase or reclassify that historical 13/77 split; it adds evidence that both
cohorts are compatible with the same declared arithmetic model.

## 7. Conditioning and contraction-order diagnostics

The expanded component cancellation index ranges from about
\(2.01\times10^2\) to \(1.01\times10^{16}\). The largest retained source dot
condition index is about \(8.68\times10^{16}\), while the normwise chain proxy
ranges from about \(1.24\times10^4\) to \(2.44\times10^4\). The fixed
\(\gamma_{56}\max\kappa_{\rm expand}\) risk indicator ranges from
\(1.25\times10^{-12}\) to about 63.0 and therefore exceeds the
\(5\times10^{-13}\) Phase-43 scale at all 90 slots.

All six predeclared association-by-summation alternatives completed at all
90 slots and passed their named local dot bounds:

~~~text
left_matrix_chain  x {explicit_naive, fixed_pairwise, componentwise_kahan}
vector_first_chain x {explicit_naive, fixed_pairwise, componentwise_kahan}
~~~

Their largest symmetric relative differences from S3 or S7 lie between about
\(5.65\times10^{-16}\) and \(1.11\times10^{-15}\), depending on the fixed
comparison path. Their largest differences from S0 remain about
\(3.56\times10^{-12}\), the same scale as the source/reference discrepancy.
This is a complete diagnostic comparison, not a best-algorithm selection and
not authorization to rewrite the production implementation.

## 8. Interpretation boundary and retained status

### Calculated facts

- The declared source and independent action, gradient, and Hessian
  expressions are exactly identical for all three variants.
- All named binary64 stages except the exact outer operation have detectable
  nonzero contributions at every frozen slot.
- The fixed forward-error model covers every component and norm at all 90
  slots, including all 13 disclosed Phase-43 mismatches.
- The same model also covers all 77 controls, and no beyond-model residual is
  supported in either cohort.
- All six contraction alternatives and all fixed trace, retention, and
  dependency contracts are complete.

### Scoped interpretation

The Phase-43 threshold crossings are compatible with mixed coefficient,
state, scalar-Hessian, and contraction rounding in a highly cancellation-
capable local pipeline on this pinned platform. This is stronger than the
Phase-43 statement that the operational outputs differ, because the exact
formula has now been checked and the whole observed difference fits a fixed
forward model. It is weaker than a unique causal diagnosis because the
contributions interact and the controls exhibit the same qualitative
evidence pattern.

### Still-open physical and integrated questions

Phase 44 does not establish a corrected integrated tangent, show that the
Phase-41 tangent failure disappears, construct a local orientation, identify
the original regulated cycle, or compute a signed global intersection. It is
a calculation-workbench result about a frozen local numerical pipeline, not a
physics claim.

The retained boundary is:

~~~text
Phase 41 numerical contracts:  8/9
Phase 41 tangent status:        TANGENT_CONTROL_FAILED
Phase 42 reference tangent:     REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE
Phase 43 local mismatch label:  SUPPORTED at 13/90, unchanged
Phase 44 arithmetic diagnosis:  LOCAL_ROUNDING_CONTRIBUTIONS_MIXED_NONEXCLUSIVE
integrated tangent evolution:   NOT_TESTED_LOCAL_ONLY
ODE solver-noise component:     NOT_TESTED_LOCAL_ONLY
global promotion:               PROHIBITED
Gate 1:                         OPEN_PARTIAL_PROGRESS
~~~

All promoted completion prerequisites remain false and all global promoted
outputs remain null. Null is not zero.

## 9. Minimal next calculation

The next smallest useful calculation is a separately frozen integrated-
tangent stability test at the existing fixed roots. It should specify before
execution one precision-stable local RHS reference and retain the unchanged
NumPy64 source path as a comparison, rather than selecting a preferred Phase-44
alternative after seeing these results. It should then reintegrate the same
variational problem and test whether the Phase-41 tangent-control failure is
stable under the independently specified local arithmetic path.

That later calculation must keep root discovery, orientation, determinant
lines, and global-cycle promotion outside scope unless they are separately
frozen and justified. A repaired or stable integrated tangent would still be
local evidence and would not close Gate 1 by itself.

## Bottom line

~~~text
exact declared source formula:          identical to independent model
named local rounding contributions:     mixed and nonexclusive at 90/90
declared forward-error model:           covers 90/90
Phase-43 disclosed mismatch cohort:     covers 13/13
negative-control cohort:                covers 77/77
unresolved beyond declared model:       NOT_SUPPORTED
integrated tangent / root / ODE:        not tested
global cycle or intersection claim:     prohibited
Gate 1:                                 OPEN_PARTIAL_PROGRESS
~~~

Phase 44 resolves the narrow arithmetic-provenance question it was designed
to answer. It does not resolve the integrated tangent or the global
intersection problem.
