# Phase 52 — Phase-51 CSE runtime-dtype audit and static element-local RHS repair

## Outcome

Phase 52 reproduced a hidden violation of the Phase-51 evaluator contract and
identified one predeclared same-platform static repair that passes the frozen
six-slot accuracy gates.

```text
run_status:                  VALID_RUN
exact checks:                7 / 7 PASS
numerical checks:            6 / 7 PASS
single numerical non-pass:   P52.repair.long_namespace_joint_CSE
classification:              P51_CSE_DTYPE_CONTRACT_VIOLATION_REPRODUCED_
                             ELEMENT_LOCAL_RHS_REPAIR_SUPPORTED_ON_FROZEN_SIX_SLOTS
Phase51 protocol validity:   NOT_UPHELD
Phase53 full rerun required: true
Gate 1:                      OPEN_PARTIAL_PROGRESS
```

The Phase-51 production joint-CSE callables had reported `complex256` after
array coercion, but runtime tracing before coercion found 19 binary64
temporaries in each of the `m4` and `m5` CSE DAGs at every one of the six
declared source-by-lambda launch states.  Each split was ten NumPy `float64`
values plus nine Python floats.  The frozen proposition that every production
CSE temporary remained `clongdouble` is therefore reproducibly false.

The primary static candidate evaluates each action element separately, keeps
every literal, elementary function, CSE temporary, raw output, fixed-order
element sum, basis lift, lambda blend, ordinary-transpose contraction, and
outer minus-conjugation in `clongdouble`.  Against the independent direct
120-decimal same-expression reference, its worst gradient relative error was
`7.0509324896283509e-11` and its worst RHS relative error was
`1.5668639302791577e-10`.  Both are below the frozen `5e-10` gates at all six
slots.

This is a **static evaluator result only**.  Phase 52 did not solve or rerun a
Gamma--K root, nonlinear flow, continuation, reflection path, finite-
difference control, tangent, endpoint mutation, orientation, or action/first-
cap ledger.  It therefore does not recover the Phase-51 supported continuation
label.  A separately frozen Phase 53 must install the repaired production
gradient path and rerun the complete unchanged Phase-51 suite first.

The immutable Phase-51 raw result still records its historical emitted
`VALID_RUN` status and was not rewritten.  Once the hidden binary64 violation
is confirmed, however, the stronger Phase-51 all-temporaries-`clongdouble`
protocol is not upheld.  This statement invalidates that protocol claim; it
does not establish that the historical roots are nonexistent or false.

As throughout this repository, this is a finite-dimensional calculation-
workbench result.  It is not a portable backend theorem, global intersection,
physical cycle, cutoff or continuum result, TOE, or physics claim.

## 1. Frozen question, scope, and provenance

The frozen question was:

> At the six immutable Phase-51 source-by-lambda launch states, did the
> production joint-CSE callable actually retain `clongdouble` in every
> temporary, and can a predeclared element-local `clongdouble` gradient path
> agree with an 80/120-decimal same-expression reference under the unchanged
> `5e-10` RHS gate?

The slots are the Cartesian product of the independently retained
`phi_plus` and `phi_minus` sources with
`lambda = 0, 0.5, 1`.  Each state is recomputed exactly as declared by
Phase 51,

\[
w_{\mathrm{launch}}
=w_{\mathrm{saddle}}
+r\,(W_{\mathrm{launch},\lambda}u_{\mathrm{center}}),
\]

with no slot selection or replacement.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| effective frozen input manifest | `75cce4131cea3a1b69eed4436caaf72ce50b9b11` | `5766d8cdaf599428d01eeb785c319ba9418e3c5e56f6275fd9d1229d4f7e0238` |
| committed runner | `3d70edab931cde249220c78f4041287a415b2eb2` | `3e2c241d3eb001cb8de79190aa3c71b86f470d4e78d03fb67200d2d20a572916` |
| raw result | `c766f0715de7b6cfabe68ea357182f2cbd8d821d` | `be29daadd7a338d4b71a445c7c364444de0c60ffb7afe45393d5419a24731ffd` |

The authoritative command was

```bash
proxmox-scratch run p52r --timeout 7200 -- \
  ./ice run phase52_m5_cse_runtime_dtype_and_rhs_repair
```

It returned exit `0`.  The 659,213-byte result has schema
`ice-phase52-m5-cse-runtime-dtype-and-rhs-repair/v1`; its self-excluding
canonical digest is
`524ddaf02568702e8a5a7f98d14e08b8ff168aab0d4b2446a32ae0d94d16ddb5`.
The generated-callable ledger fingerprint is
`ef5c95e3e864b1cfc52828e75f61c31b6b661a5ba725cba57c22e1f0d34eb060`.

A post-result independent committed-run verification used

```bash
proxmox-scratch run p52x --timeout 7200 -- \
  ./ice run phase52_m5_cse_runtime_dtype_and_rhs_repair
```

It also returned exit `0`.  The extracted `RESULT_JSON` was byte-identical to
the 659,213-byte canonical result and reproduced the same self digest.  The
control-plane gate `npm run check` also passed strict typechecking and all
22/22 tests.

The runtime matched the pinned platform contract: CPython `3.13.5`, NumPy
`2.5.2`, SciPy `1.18.0`, SymPy `1.14.0`, and mpmath `1.3.0`, with 16-byte
`longdouble`, 32-byte `clongdouble`, 63 explicit mantissa bits, and
`longdouble` epsilon `1.084202172485504434e-19`.

The runner validated the Phase-51 manifest, runner, result, all Phase-51
transitive Phase-41/42/49/50 pins, the Phase-43 high-precision precedent, the
Phase-49 full-flow dtype precedent, and both package locks.  Working bytes
matched the named committed blobs and were rehashed after the calculation.

One earlier production attempt was deliberately interrupted before it emitted
a result after a late audit found that the runner did not yet revalidate every
transitive Phase-51 pin against its named Git blob.  The runner was hardened in
commit `3d70eda`, revalidated, and only then run authoritatively.  The aborted
attempt produced no result and is not evidence.

No new external physics source is used in this phase.  The computational
sources are the byte-pinned Phase-51 symbolic evaluator and state
construction, with the Phase-43 80/120-decimal arbitration and Phase-49 raw-
dtype audit used only as implementation precedents.

## 2. Evaluator variants and conventions

The calculation keeps the Phase-51 arithmetic stages in this fixed order:

1. raw `m4` gradient;
2. lifted `m4` gradient in the common `m5` coordinates;
3. raw `m5` gradient;
4. lambda-blended gradient;
5. `A_lambda.T` contraction;
6. one outer minus-conjugation.

Writing the completed blended gradient as `g_lambda`, the static flow RHS is

\[
F_\lambda=-\overline{A_\lambda^T g_\lambda}.
\]

The transpose is the ordinary transpose, not the Hermitian transpose.  No
additional conjugation is inserted for `phi_minus`, and no `complex128` solver-
boundary cast occurs in this static phase.

Four evaluator paths are retained:

| path | role |
|---|---|
| Phase-51 joint CSE | historical production baseline: one canonical CSE DAG over gradient plus Hessian under the default NumPy lambdify namespace |
| Phase-51 non-CSE | historical unreduced gradient comparison with no CSE replacement list or output cache |
| long-namespace joint CSE | same global joint DAG, but every noninteger literal, `pi`, `sqrt`, `exp`, temporary, and raw output is forced through the long namespace; retained as an accuracy negative control |
| element-local long CSE | primary candidate: source-substitute and differentiate each of four `m4` or five `m5` midpoint elements separately, CSE each element-gradient vector, then accumulate in fixed left-to-right order |

For the element-local construction,

\[
g_m=\sum_{e=1}^{m}\nabla S_{m,e}
\]

is verified exactly in a separate exact-decimal Rational source family.  The
executable evaluator intentionally remains the frozen 50-digit SymPy Float
construction.  Changing expansion and addition order in that Float family
leaves nonzero symbolic rounding residuals; the largest deterministic probe
was `7.55048436118526e-47`.  Phase 52 records that residual instead of
mislabeling executable Float equality as exact.

The numerical error metric is the symmetric normwise relative error

\[
\epsilon(x,y)=
\frac{\lVert x-y\rVert_2}
{\max(\lVert x\rVert_2,\lVert y\rVert_2,10^{-100})}.
\]

Absolute norm and maximum-component differences are retained alongside it.
The candidate gradient and RHS thresholds are each `5e-10`; the RHS value is
inherited unchanged from Phase 51.

## 3. The hidden binary64 contract violation reproduced

All six historical Phase-51 evaluator records reproduced with maximum absolute
numeric difference `0`, against the frozen `5e-16` tolerance.  The audit then
bound the actual pinned Phase-51 production callables to their reconstructed
DAGs and inspected each local temporary before its frame disappeared.

At every source and lambda slot, the result was:

| DAG | replacement count | `complex256` temporaries | NumPy `float64` | Python float | all temporaries `clongdouble`? |
|---|---:|---:|---:|---:|---|
| `m4` joint gradient + Hessian | 444 | 425 | 10 | 9 | no |
| `m5` joint gradient + Hessian | 544 | 525 | 10 | 9 | no |

Thus both DAGs contain exactly 19 normalized binary64 temporaries per call.
The Phase-51 checks observed the final coerced output arrays as `complex256`;
that post-output dtype did not prove the dtype of the destroyed intermediate
locals.  Phase 52 treats this as the typed scientific failure
`P51_CSE_DTYPE_CONTRACT_VIOLATION_REPRODUCED`, not as an infrastructure
failure.

Both repaired variants satisfy their mandatory dtype condition: every traced
CSE temporary and every raw output scalar is `complex256`/`clongdouble` at all
six slots, and the trace count equals the generated replacement count.  Dtype
repair alone, however, does not imply reference accuracy.

## 4. Independent reference and six-slot candidate assessment

The reference directly evaluates the same pinned, source-substituted expanded
gradients with SymPy `evalf` at 80 and 120 decimal digits.  Long-double inputs
are round-tripped through unique 25-digit decimal strings into mpmath, and all
subsequent stage algebra stays in mpmath.  Neither reference path uses NumPy
`lambdify`, Python float conversion, or a native evaluator output.

As an internal control, the canonical CSE DAG is evaluated directly with
SymPy substitutions and compared with the unreduced expressions at both
precision tiers.  The worst 80-versus-120 relative discrepancy was
`6.56844604681612e-78`; the worst high-precision CSE-versus-plain discrepancy
was `2.86916660889674e-73`.  Both are far below their frozen `1e-40` limits.

The six-slot results are:

| source | lambda | historical CSE/non-CSE RHS relative | long-joint gradient / RHS relative | element-local gradient / RHS relative |
|---|---:|---:|---:|---:|
| `phi_plus` | `0` | `6.319153e-9` | `2.165653e-10` / `4.257482e-9` | `4.173036e-11` / `1.040882e-10` |
| `phi_plus` | `0.5` | `1.146011e-8` | `3.148444e-10` / `5.853026e-9` | `5.088304e-11` / `1.295854e-10` |
| `phi_plus` | `1` | `1.683350e-8` | `7.148666e-10` / `7.576909e-9` | `7.050932e-11` / `1.566387e-10` |
| `phi_minus` | `0` | `6.271640e-9` | `2.162592e-10` / `4.226303e-9` | `4.172423e-11` / `1.041846e-10` |
| `phi_minus` | `0.5` | `1.146330e-8` | `3.151181e-10` / `5.887404e-9` | `5.088392e-11` / `1.296052e-10` |
| `phi_minus` | `1` | `1.686424e-8` | `7.149553e-10` / `7.625057e-9` | `7.049981e-11` / `1.566864e-10` |

The global long-namespace joint CSE fixes the runtime dtype contract but does
not fix the frozen accuracy gate.  Its worst gradient error is
`7.14955260647903e-10` and its worst RHS error is
`7.62505691985326e-9`; the latter remains roughly fifteen times the `5e-10`
limit.  It is therefore the declared diagnostic negative control and the sole
non-passing numerical check.

The element-local candidate passes both metrics in all six rows.  The staged
baseline-to-candidate plus candidate-to-reference telescope closes with
maximum recorded relative residual `0`, below `5e-18`.  Large retained
cancellation indices in individual components warn that evaluation order
matters; they are diagnostics, not new tolerances or post-hoc slot exclusions.

## 5. Frozen check ledger

All seven exact checks passed:

| exact check | status |
|---|---|
| `P52.inputs.byte_pins_self_digests_and_manifest_before_runner` | PASS |
| `P52.slots.exact_Phase51_six_state_construction` | PASS |
| `P52.symbolic.element_gradient_sum_identity` | PASS |
| `P52.symbolic.CSE_back_substitution_and_DAG_fingerprints` | PASS |
| `P52.dtype.trace_completeness_and_raw_output_guard` | PASS |
| `P52.conventions.stage_order_transpose_and_reference_isolation` | PASS |
| `P52.guard.historical_nonrewrite_and_global_nulls` | PASS |

Six of seven numerical checks passed:

| numerical check | status |
|---|---|
| `P52.reproduction.Phase51_six_slot_evaluator_records` | PASS |
| `P52.audit.Phase51_all_CSE_temporaries_clongdouble` | PASS — the historical proposition is reproducibly false |
| `P52.reference.mpmath_80_120_and_CSE_plain_stability` | PASS |
| `P52.repair.long_namespace_joint_CSE` | `DIAGNOSTIC_NEGATIVE_CONTROL_ACCURACY_NONPASS` |
| `P52.repair.element_local_long_CSE` | PASS |
| `P52.arithmetic.stage_telescope_and_cancellation` | PASS |
| `P52.guard.classification_and_nulls` | PASS |

The single numerical non-pass does not contradict the selected classification.
The manifest froze long-namespace joint-CSE reference accuracy as a diagnostic
negative control, not as a prerequisite for the element-local classification.
Its dtype contract was mandatory and passed; its accuracy failure is retained
rather than hidden.

## 6. Interpretation and boundary

### Calculated facts

- All six historical Phase-51 center-launch evaluator records reproduced
  exactly at the recorded numeric leaves.
- The actual pinned Phase-51 `m4` and `m5` production joint-CSE callables each
  used 19 hidden binary64 temporaries at every audited slot.
- Exact CSE back-substitution, source binding, replacement counts, DAG
  fingerprints, state reconstruction, stage order, transpose convention, and
  high-precision reference stability all passed.
- Both repaired variants retained `clongdouble` in every traced temporary and
  raw output.
- The global long-namespace joint CSE failed the static reference-accuracy
  control, while the fixed-order element-local candidate passed the gradient
  and RHS `5e-10` gates at all six slots.
- The Phase-51 raw result remained byte-identical.

### Scoped interpretation

The result supports a specific same-platform implementation choice for the six
audited static states: evaluate source-substituted action elements separately,
perform element-level CSE, and accumulate their gradients in the frozen order
while retaining `clongdouble` through the completed RHS.  It also explains why
merely changing the global NumPy namespace is insufficient: it repairs dtype
retention but preserves an accuracy failure at the contraction/RHS scale.

Because the Phase-51 all-temporaries-`clongdouble` claim was conjunctive and is
now reproducibly false, its protocol validity is `NOT_UPHELD`.  The historical
emitted `VALID_RUN` string remains part of immutable provenance; it is not a
license to ignore the later contract audit.  Conversely, this audit does not
show that the previously found roots disappear under the repaired evaluator.
Only the Phase-53 replay can answer that.

### Open hypotheses and required next calculation

- Freeze a Phase-53 production runner that replaces the Phase-51 production
  gradient path with the element-local candidate without changing states,
  roots, meshes, solver settings, charts, signs, tolerances, or classification
  gates.
- Replay all three paired trajectories and the full fine/coarse/reverse
  continuation, independent reflection, full-J finite difference, outer path
  tangent, endpoint radius/shape, orientation, action, and first-cap suite.
- Compare the repaired production path with an independent reference at the
  same declared diagnostic points and preserve any root loss, sign change,
  basis dependence, or numerical null as observed.
- Do not issue any local supported continuation label until that full replay
  passes.  Cross-platform portability and a formal endpoint-error transport
  bound remain separate open numerical questions.
- Straight arms, later cap reintersections, other roots and charts, exhaustion
  of saddles/upward components, Stokes data, all relative good ends, a common
  determinant line, and a physical original cycle remain uncomputed.

### Global-null boundary

Phase 52 leaves all global and physical outputs unchanged:

```text
bounded_chain_signed_sum                   = null
complete_global_signed_intersection_vector = null
global_n_sigma                             = null
cutoff_limit                               = null
continuum_limit                            = null
promoted_output                            = null
global_promotion                           = PROHIBITED
Gate 1                                     = OPEN_PARTIAL_PROGRESS
```

## Bottom line

Phase 52 closes the narrow diagnostic question that blocked Phase 51: the
production CSE implementation did contain hidden binary64 temporaries, and one
predeclared element-local `clongdouble` evaluator meets the unchanged static
six-slot gradient/RHS gates against an independent high-precision reference.
It does **not** close the continuation question.  Phase 51's protocol validity
is not upheld, its raw historical output remains unmodified, and Phase 53 must
rerun the entire nonlinear calculation before any local result can be
reconsidered—let alone any global or physical claim.
