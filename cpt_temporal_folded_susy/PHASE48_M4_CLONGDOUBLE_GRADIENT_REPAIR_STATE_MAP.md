# Phase 48 — m=4 `clongdouble` gradient-only state-map repair control

## Outcome

Phase 48 integrates all eighteen frozen `u2` paths after changing only the
generated Phase-41 gradient-callable evaluation from complex128 to NumPy
`clongdouble`.  The seven-component gradient is projected once to complex128;
source state formation, `L.T` contraction, DOP853 integration, cap, residual,
roots, and the complete three-step ladder remain fixed.

The guarded run completed with

```text
run_status:       VALID_RUN
classification:  GRADIENT_ONLY_CLONGDOUBLE_STATE_MAP_REPAIR_NOT_SUFFICIENT
hybrid paths:     18 / 18 complete
trajectory probes: 90 / 90 retained
endpoint checks:  PASS at 3 / 3 roots
full-ladder check: PASS at 1 / 3 roots
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The ablation materially improves the source state-map control but does not meet
the fixed all-step criteria.  All intermediate local-flow probes pass the
`5e-8` limit and all hybrid endpoint states agree with the Phase-46 independent
endpoints within `2.061e-9`, below the `1e-8` limit.  Nevertheless, dividing
the remaining signed endpoint error by the smallest `2h` produces maximum
column discrepancies of `0.02562`, `0.05208`, and `0.008222`; all exceed the
frozen `0.005` limit.  The `shared_zero` and `phi_plus` second adjacent plateaus
also exceed `0.02`.

This is a useful negative control.  It confirms that the generated gradient
evaluation is a major contributor, but a 64-bit-mantissa `clongdouble` gradient
alone is not enough to reproduce the exact-reference state derivative across
the full ladder.

## 1. Frozen inputs and disclosed pilot

Before any integrated Phase-48 output, the manifest froze

- the three immutable Phase-42 roots and `u2` parameter index 8;
- steps `2e-6`, `5e-7`, and `1e-7`, both signs, and no post-output selection;
- one gradient-only hybrid path using source complex128 state formation and
  contraction around a `clongdouble` generated gradient evaluation;
- DOP853 `rtol=2e-12`, `atol=2e-14`, `max_step=0.01`, and dense output;
- five trajectory fractions `0, 1/4, 1/2, 3/4, 1` on every path;
- the Phase-46 independent endpoints and Phase-45 independent tangent columns;
- the NumPy long-double platform contract and all comparison thresholds; and
- a three-way supported/not-sufficient/inconclusive classification.

The manifest also discloses the nonauthoritative 36-state candidate-selection
pilot.  That pilot observed paired local-flow derivative maxima below `0.005`
at all roots after promoting only the gradient evaluation.  It selected the
candidate but did not observe an integrated endpoint, column, or plateau.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `2ba73ec37408c09be10578a6b3a009d75e9408aa` | `5604456ece8f542500cafd19b1429fe439514f780c2c8556195ddb934796f335` |
| runner | `1137832f08a9ee625e4a84e0cfa754a52858f778` | `63bc9f3eaf7f9d994d52898a39ae494988dfd573216385397d65fd2cae9b3986` |
| raw result | `8260ea2fc23a6141de5e1efca91a760bfebfa703` | `4c5eeb004724c08a4f5d08368d425c885f1ecf2ef02a0bbb0d915d122c2df5fc` |

The successful guarded command was equivalent to

```bash
proxmox-scratch run ice-phase48 --timeout 7200 -- \
  ./ice run phase48_m4_clongdouble_gradient_repair_state_map
```

The 165,031-byte result has schema
`ice-phase48-clongdouble-gradient-repair-state-map/v1`.  Its self-excluding
canonical digest is
`10fc01de6eb8ab85c31cc48a0163a2599106d01f9e0699cfc062549cb0fce73b`;
an independent Python standard-library parse reproduced it exactly.  The run
used CPython 3.13.5, NumPy 2.5.2, SciPy 1.18.0, SymPy 1.14.0, and mpmath 1.3.0.
Scratch cleanup completed with no residual Phase-48 process and 117 GB free.

## 2. Fixed platform and flow convention

The platform contract reproduced

```text
sizeof(numpy.clongdouble): 32 bytes
sizeof(numpy.longdouble):  16 bytes
stored mantissa bits:      63
epsilon:                    1.084202172485504434e-19
```

At every RHS call, the hybrid performs

```text
xi64 = complex128(xi)
u64  = L64 @ xi64
w64  = saddle64 + u64
gLD  = gradient_function(tuple(clongdouble(w64)))
g128 = complex128(gLD)                 # one gradient projection
F    = -conjugate(L64.T @ g128)
```

The raw generated callable is required to return actual `clongdouble`, not a
complex128 result upcast after evaluation.  `L.T` remains an ordinary transpose.
The calculation is therefore a single-stage ablation, not a full Phase-43 flow
replacement and not a portable binary128 claim.

Every new path uses the original chart launch and the fixed cap/residual map.
For each of five dense trajectory samples the hybrid flow is compared at the
same state with the 80-digit exact-decimal Phase-43 reference.  At the endpoint,
the hybrid state and residual are compared with the retained independent
Phase-46 path.  Central-difference columns and adjacent plateaus are then built
from all three fixed step pairs.

## 3. Results

### Aggregate root metrics

| root | max local-flow relative | max endpoint-state relative | max hybrid ↔ independent column | max hybrid ↔ Phase-45 tangent | max adjacent plateau |
|---|---:|---:|---:|---:|---:|
| `shared_zero` | `1.679e-8` | `2.060e-9` | `0.0256173` | `0.0256172` | `0.0253056` |
| `phi_plus` | `2.018e-9` | `2.084e-10` | `0.0520823` | `0.0520826` | `0.0558288` |
| `a_plus` | `6.451e-10` | `1.324e-10` | `0.00822221` | `0.00822232` | `0.00626181` |

All local-flow values pass `5e-8`; all endpoint-state values pass `1e-8`.
Every root fails the all-column `0.005` comparison.  Only `a_plus` passes both
adjacent plateaus under `0.02`.

### Complete step retention

| root | hybrid plateaus `2e-6→5e-7`, `5e-7→1e-7` | per-step hybrid ↔ independent columns |
|---|---|---|
| `shared_zero` | `0.0003450`, `0.0253056` | `0.0006220`, `0.0003514`, `0.0256173` |
| `phi_plus` | `0.0031408`, `0.0558288` | `0.0006362`, `0.0037742`, `0.0520823` |
| `a_plus` | `0.0062618`, `0.0051772` | `0.0019621`, `0.0082222`, `0.0031426` |

The first two `shared_zero` columns and first two `phi_plus` columns are within
the fixed limit, but their smallest-step columns fail.  `a_plus` has a stable
full ladder but its middle-step column misses the reference threshold.  No step
is dropped to obtain a preferred conclusion.

The hybrid/reference and hybrid/Phase-45 tangent comparisons are nearly
identical.  This reaffirms the Phase-45 independent tangent as a stable primary
derivative reference while exposing the remaining state-map subtraction error.

All eighteen solvers completed with 15,362–15,407 RHS evaluations and
1,024–1,027 accepted steps.  Ninety intermediate local-flow probes were
retained.

## 4. Interpretation

### Calculated facts

- Actual complex256 gradient evaluation reduces the local-flow discrepancy and
  produces normwise-close integrated endpoints at every root.
- The resulting derivative columns are much closer to the independent control
  than the Phase-46 tight source columns, but the complete frozen ladder still
  fails.
- Small endpoint errors that are harmless in a state norm remain large after
  signed subtraction and division by `2h`.
- Agreement with the Phase-45 tangent fails by the same amount as agreement
  with the independent Phase-46 finite difference, so the reference derivative
  paths remain mutually consistent.

### Scoped inference

The Phase-47 generated-gradient stage is a major contributor, but promoting
only that callable to 63 stored mantissa bits leaves too much correlated
state-formation, contraction, gradient, or accumulated integration error for
the smallest central differences.  Phase 48 does not determine which remaining
term dominates after the ablation.

The next minimal control should promote state formation, gradient evaluation,
and `L.T` contraction together to the same long-double arithmetic and project
the complete flow only once to complex128.  If that remains insufficient, the
already passing Phase-46 exact/high-precision full-flow path is the appropriate
reference implementation, with the Phase-45 variational equation retained as
the primary derivative estimator.

## 5. Boundary

Phase 48 does not provide a formal fundamental-matrix endpoint error bound or a
solver-accumulation decomposition.  It does not rewrite Phase 41, alter the
Phase-44 formula audit, replace the Phase-46 exact-flow result, or promote the
platform-specific `clongdouble` adapter as a universal implementation.  No root
search, retuning, global cycle, determinant line, signed intersection, or
physical claim is made.

Global promotion remains prohibited and Gate 1 remains
`OPEN_PARTIAL_PROGRESS`.

## Bottom line

```text
long-double platform contract:             PASS
hybrid integrations:                       18 / 18 complete
intermediate hybrid/reference probes:      90 / 90 retained; PASS
endpoint-state agreement:                  PASS at 3 / 3 roots
full three-step ladder:                    PASS at 1 / 3 roots
all-step independent-column comparison:    FAIL at 3 / 3 roots
all-step Phase-45 tangent comparison:       FAIL at 3 / 3 roots
classification:                            GRADIENT_ONLY_CLONGDOUBLE_STATE_MAP_REPAIR_NOT_SUFFICIENT
global promotion:                          PROHIBITED
Gate 1:                                    OPEN_PARTIAL_PROGRESS
```
