# Phase 47 — m=4 source-gradient flow error budget

## Outcome

Phase 47 evaluates a fixed mixed-arithmetic flow telescope at the launch and
endpoint states retained by all eighteen independent Phase-46 `u2` paths.  It
does not integrate another trajectory.  The guarded run completed with

```text
run_status:       VALID_RUN
classification:  LOCAL_SOURCE_GRADIENT_MIXED_ARITHMETIC_BUDGET_SUPPORTED
state slots:      36 / 36 complete
paired Dh slots:  18 / 18 complete
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The six-stage telescope closes at every retained state and after every frozen
`1/(2h)` central-difference amplification.  The largest state-telescope residual
is `5.076e-116`; the largest paired-derivative residual is `1.363e-107`.
Independent 80- and 120-digit flow evaluations are identical after the final
complex128 projection at all 36 states.  The pinned source `gradient_at` and
`flow_xi` boundaries are reproduced bit for bit.

The numerical separation is decisive within this local audit.  The generated
NumPy gradient-evaluation delta is the largest delta norm at all 36 states and
in all 18 paired derivatives.  Its maximum state norm is `2.447e-11`, compared
with `1.139e-13` for binary64 state formation and `1.130e-16` for the final
matrix-vector contraction.  The high-precision source-symbolic delta is only
`2.114e-46`, and the outer minus-conjugation delta is zero.

This supports stabilizing the gradient evaluation kernel and projecting once
to complex128 as the first repair to test.  It does not identify a unique code
defect, bound accumulated solver error, or prove an endpoint finite-difference
repair without a corrected integrated control.

## 1. Frozen inputs and execution

The input manifest fixes

- the three Phase-42 roots and fixed real `7 x 7` linear map;
- all 36 Phase-46 `initial_xi` and `endpoint_xi` state records from the
  independent 80-digit DOP853 paths;
- target, step, sign, and location order with no post-output slot selection;
- the Phase-43 exact-decimal gradient convention and binary64-ratio lift;
- the Phase-41 source symbolic gradient and generated NumPy flow boundary;
- the Phase-44 result that leaves a source/reference formula mismatch
  `NOT_SUPPORTED` globally;
- the six stages, five signed deltas, 100-digit authoritative arithmetic,
  80/120-digit projection probe, thresholds, and fail-closed classification.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `9ad082f1b9edb66421c682545b9a35aa91e4d94c` | `a4934e2b5f45297f82921a3df7d131afffa184691551cc3c02bb516c36b9fb6e` |
| runner | `6627d585280e443aa9d3eea1f9c61b15c3e788ae` | `945744a9f9c022f371d2516c01aa806317020d947fcaa47a0cc7f962dc82d091` |
| raw result | `1d31c220257f326479d5ee0ec27cdf3e3f29a5ff` | `d58b443a5a220b93a59d2b74c86bd1a3169c40c6297a4d0b4d86eae15e61b576` |

The successful guarded command was equivalent to

```bash
proxmox-scratch run ice-phase47 --timeout 7200 -- \
  ./ice run phase47_m4_source_gradient_flow_error_budget
```

The 1,117,072-byte result has schema
`ice-phase47-source-gradient-flow-error-budget/v1`.  Its self-excluding
canonical digest is
`f81cfab8249a7584055416adbf89410ef2aca9079db1fb3f6f8b1269750236d3`;
an independent Python standard-library parse reproduced it exactly.  The run
used CPython 3.13.5, NumPy 2.5.2, SciPy 1.18.0, SymPy 1.14.0, and mpmath 1.3.0.
Scratch cleanup completed, no Phase-47 process remained, and 117 GB was free on
the backing filesystem after the run.

## 2. Fixed calculation

At each retained binary64 state `xi`, the source boundary is evaluated in its
pinned order:

```text
u64 = L @ xi
w64 = saddle + u64
g64 = gradient_at(model, w64)
y64 = L.T @ g64
F64 = -conjugate(y64)
```

`L.T` is an ordinary transpose, not a Hermitian transpose.  The independent
reference is

\[
F_0(\xi)=-\overline{L^T\nabla S_{\rm exact}(s+L\xi)},
\]

where the action constants are exact decimal rationals and every fixed
binary64 saddle, map, and state component is lifted by its exact integer ratio.

The retained stages replace one arithmetic boundary at a time:

| stage | value |
|---|---|
| `S0` | independent exact-decimal gradient, exact state formation and contraction |
| `S1` | pinned Phase-41 symbolic expression at exact `w`, evaluated with mpmath |
| `S2` | the same source symbolic expression at the exact lift of source `w64` |
| `S3` | exact lift of source `g64`, followed by an exact contraction |
| `S4` | exact lift of source `y64`, followed by exact minus-conjugation |
| `S5` | exact lift of source `F64` |

The five signed deltas are

```text
D_source_symbolic_semantics = S1 - S0
D_state_formation           = S2 - S1
D_gradient_evaluation       = S3 - S2
D_contraction               = S4 - S3
D_outer                     = S5 - S4
```

They satisfy `sum(D_i) = S5 - S0` componentwise.  `S1` is explicitly a
high-precision ideal of the pinned source SymPy expression.  Generated-callable
constant lowering, scalar operation ordering, elementary functions, and NumPy
rounding remain together in `D_gradient_evaluation`; Phase 47 does not pretend
to split those suboperations.

For each root, location, and frozen step, the same telescope is applied to

\[
D_h(S_k)=\frac{S_k(\xi_+)-S_k(\xi_-)}{2h}.
\]

Every sign and all three steps `2e-6`, `5e-7`, and `1e-7` are retained.  The
signwise source-error triangle bound and its actual cancellation utilization
are also recorded.

## 3. Results

### Local state budget

| signed stage delta | maximum norm over 36 states | largest-delta count |
|---|---:|---:|
| source symbolic semantics | `2.114e-46` | `0 / 36` |
| state formation | `1.139e-13` | `0 / 36` |
| generated gradient evaluation | `2.447e-11` | `36 / 36` |
| `L.T` contraction | `1.130e-16` | `0 / 36` |
| outer minus-conjugation | `0` | `0 / 36` |

The maximum symmetric-relative source/reference flow discrepancy is
`3.883e-8`.  It occurs at a launch state.  The per-point maxima separate
strongly by location:

| root | launch relative max | endpoint relative max |
|---|---:|---:|
| `shared_zero` | `3.883e-8` | `2.676e-11` |
| `phi_plus` | `2.572e-8` | `1.202e-11` |
| `a_plus` | `3.460e-8` | `1.534e-11` |

These are local flow comparisons at named states.  An "endpoint" row means the
flow was evaluated at a retained endpoint state; it is not a comparison of the
integrated endpoint maps.

### Paired `u2` derivative budget

| signed stage delta after `1/(2h)` | maximum norm over 18 pairs | largest-delta count |
|---|---:|---:|
| source symbolic semantics | `1.181e-47` | `0 / 18` |
| state formation | `5.350e-7` | `0 / 18` |
| generated gradient evaluation | `9.823e-5` | `18 / 18` |
| `L.T` contraction | `3.640e-10` | `0 / 18` |
| outer minus-conjugation | `0` | `0 / 18` |

The largest source/reference local-flow derivative discrepancies by point and
location are:

| root | launch relative max | endpoint relative max |
|---|---:|---:|
| `shared_zero` | `2.736e-2` | `1.399e-7` |
| `phi_plus` | `5.295e-2` | `3.766e-6` |
| `a_plus` | `2.270e-1` | `1.007e-6` |

The worst launch pair is `a_plus`, `h=1e-7`: its local derivative error norm is
`2.234e-5`, of which the gradient-evaluation delta norm is `2.234e-5`; the
state-formation delta is `1.713e-7`.  The worst absolute paired error is the
`phi_plus` endpoint at `h=1e-7`, with norm `9.832e-5`; its gradient-evaluation
delta is `9.823e-5` and its state-formation delta is `5.350e-7`.

Signed delta norms do not add like probabilities.  Their ratios can exceed one
when stages cancel.  The "largest-delta" count is therefore descriptive and is
not a causal classifier.

## 4. What the calculation establishes

### Calculated facts

- The fixed source-to-reference flow discrepancy is completely represented by
  the declared signed arithmetic telescope at all 36 retained states.
- The same representation remains closed after all 18 frozen `1/(2h)`
  amplifications.
- The exact-decimal 80/120-digit reference projection is stable at every slot.
- The source symbolic-expression ideal differs negligibly from the independent
  exact-decimal expression on this scale, consistent with Phase 44's
  `formula_mismatch = NOT_SUPPORTED` result.
- Binary64 state formation contributes a smaller but detectable term.
- The generated NumPy gradient evaluation is the largest mixed-arithmetic term
  in every retained state and paired derivative.
- The final contraction is much smaller, and the outer minus-conjugation adds no
  arithmetic error in these slots.

### Scoped repair inference

The first correction to test is a flow adapter that evaluates the frozen
gradient through the independent exact/high-precision expression and rounds it
once to complex128, while leaving the surrounding state-map conventions fixed.
That directly removes the largest observed stage without rewriting the
historical Phase-41 artifact.  A useful ablation should retain source `w64` and
source NumPy contraction first, so that a repaired gradient kernel can be
distinguished from a wholesale replacement by the Phase-43 reference flow.

The natural derivative implementation remains the variational equation

\[
\dot\xi=V(\xi),\qquad
\dot S=D_\xi V(\xi)S,
\]

with the frozen launch derivative.  Endpoint finite differences should remain
a regression control rather than the primary derivative estimator.

## 5. What remains open

Phase 47 has only launch and endpoint samples because Phase 46 did not retain
intermediate states.  It therefore does not

- integrate the gradient-only repair;
- propagate local signed errors through a fundamental/sensitivity propagator;
- separate interior solver accumulation from local RHS arithmetic;
- show that the gradient-only repair meets the Phase-46 endpoint, derivative,
  and adjacent-plateau thresholds;
- establish a unique faulty NumPy suboperation inside the generated gradient;
  or
- authorize complex-step differentiation, which is incompatible with the
  outer conjugation.

The smallest decisive follow-up is a gradient-only hybrid control on the
eighteen fixed paths.  It should compare source, gradient-repaired, and fully
independent RHS paths under the same DOP853 settings, retain intermediate
checkpoints, and integrate the variational/error-transport equation.  Success
requires the repaired path to reproduce the independent endpoint and `u2`
columns within the already frozen Phase-46 limits (`1e-8` endpoint, `0.005`
column, `0.02` adjacent plateau), with the corrected sensitivity/reference
comparison targeted at `1e-8`.

Historical Phase 41 remains 8/9, Phase 44 remains a formula-identity and
floating-arithmetic audit, and Phase 46 remains the independent full-flow repair
control.  No root search, global signed intersection, physical cycle, or
quantum-gravity conclusion follows.  Global promotion remains prohibited and
Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

## Bottom line

```text
36 retained source gradient/flow boundaries:       bitwise reproduced
80/120-dps independent complex128 projections:     36 / 36 identical
state arithmetic telescopes:                       36 / 36 closed
paired u2 derivative telescopes:                   18 / 18 closed
largest state and paired stage:                    gradient evaluation, all slots
source symbolic-expression delta:                  negligible at ~1e-46
outer minus-conjugation delta:                      exactly zero
fixed classification:                              LOCAL_SOURCE_GRADIENT_MIXED_ARITHMETIC_BUDGET_SUPPORTED
endpoint propagation / solver accumulation bound:  not yet computed
global promotion:                                  PROHIBITED
Gate 1:                                            OPEN_PARTIAL_PROGRESS
```
