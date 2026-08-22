# Phase 49 — m=4 `clongdouble` full-flow state-map repair control

## Outcome

Phase 49 resolves the scoped Phase-46 source state-map finite-difference
failure on the declared NumPy long-double platform.  All eighteen frozen `u2`
paths were integrated after evaluating state formation, the generated
gradient, the `L.T` contraction, and the outer minus-conjugation together in
`clongdouble`.  The complete seven-component flow was cast once to
`complex128` at the DOP853 boundary.

The guarded run completed with

```text
run_status:       VALID_RUN
classification:  FULL_FLOW_CLONGDOUBLE_STATE_MAP_REPAIR_SUPPORTED
hybrid paths:     18 / 18 complete
trajectory probes: 90 / 90 retained
endpoint checks:  PASS at 3 / 3 roots
full ladders:     PASS at 3 / 3 roots
column controls:  PASS at 3 / 3 roots and every retained step
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The largest hybrid/independent derivative-column discrepancy is `0.001216`,
below the frozen `0.005` limit.  The largest adjacent-step plateau is
`0.001401`, below `0.02`.  The Phase-45 independent tangent comparison passes
at every root and step as well.  No step, sign, root, probe, or solver path was
dropped.

This is a platform-specific computational repair, not a new physical claim and
not a portable binary128 assertion.

## 1. Frozen inputs and provenance

Before any integrated Phase-49 output, the manifest froze

- the three immutable Phase-42 roots and zero-based `u2` index 8;
- steps `2e-6`, `5e-7`, and `1e-7`, both signs, with no post-output selection;
- DOP853 `rtol=2e-12`, `atol=2e-14`, `max_step=0.01`, and dense output;
- five trajectory fractions on every path;
- the Phase-46 independent endpoints and finite differences;
- the Phase-45 independent tangent columns and Phase-47 localization result;
- the Phase-48 gradient-only negative control;
- the NumPy long-double platform contract and all pass thresholds; and
- supported/not-sufficient/inconclusive classification rules.

The disclosed, nonauthoritative 36-state pilot selected the full-flow candidate
without observing any integrated endpoint, derivative column, or plateau.  Its
paired local derivative maxima were `6.606e-5`, `5.079e-5`, and `4.306e-5` at
`shared_zero`, `phi_plus`, and `a_plus` respectively.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `57d1431653e01969a0a136d7f847a63f81ea2daf` | `ec97937fd4643b2d3ebfccc70ff82e4348ea92086b5b0588aec33bf24fdebcc5` |
| runner | `b41e7f2b0c75b922a9fa0d775ceee5d5607e5189` | `f7f03d8ca08c3406cfbae4825b64fb5c2cac89797ea005519fc12c489947abb2` |
| raw result | `078753a9406f5e71730f7946df7ac8dcfa3a9d52` | `787e6aee62193af0b78041cae42eb38c13afef281b7d0560c07ad3a2958da531` |

The successful command was equivalent to

```bash
proxmox-scratch run ice-phase49 --timeout 7200 -- \
  ./ice run phase49_m4_clongdouble_full_flow_state_map_repair
```

The 165,513-byte result uses schema
`ice-phase49-clongdouble-full-flow-state-map-repair/v1`.  Its self-excluding
canonical digest is
`c8063283f8ac66918cbabcd3d3a71d3bfdcfdba734067306486164737d4e3c9f`;
an independent standard-library parse reproduced it exactly.  The runner hash
embedded in the result also matches the committed runner.  Scratch cleanup
completed and 117 GB remained free.

## 2. Arithmetic and comparison contract

The runtime reproduced

```text
sizeof(numpy.clongdouble): 32 bytes
sizeof(numpy.longdouble):  16 bytes
stored mantissa bits:      63
epsilon:                    1.084202172485504434e-19
```

At every RHS call, the repaired path performs

```text
xiLD = clongdouble(xi)
LLD  = clongdouble(L)
sLD  = clongdouble(saddle)
wLD  = sLD + LLD @ xiLD
gLD  = gradient_function(tuple(wLD))
FLD  = -conjugate(LLD.T @ gLD)
F128 = complex128(FLD)                 # the only flow projection
```

The generated callable is required to return actual `clongdouble`; a
complex128 value followed by an upcast is rejected.  `L.T` is an ordinary
transpose, not a Hermitian transpose.  DOP853 still integrates a complex128
state.  Chart launch, cap, coordinate scaling, residual, roots, steps, and
comparison formulas are unchanged.

Five local-flow probes on each path compare the repaired and 80-digit
exact-decimal Phase-43 flows at the same hybrid trajectory state.  Endpoints
are compared with the retained Phase-46 independent paths.  All three signed
central differences are compared both with those independent paths and the
Phase-45 tangent column.

## 3. Results

### Aggregate root metrics

| root | max local-flow relative | max endpoint-state relative | max hybrid ↔ independent column | max hybrid ↔ Phase-45 tangent | max adjacent plateau |
|---|---:|---:|---:|---:|---:|
| `shared_zero` | `1.678e-8` | `2.041e-9` | `0.00121592` | `0.00121595` | `0.00140100` |
| `phi_plus` | `1.993e-9` | `1.759e-10` | `0.000649081` | `0.000649365` | `0.000499401` |
| `a_plus` | `4.640e-10` | `1.007e-10` | `0.000643758` | `0.000643845` | `0.000822132` |

Every value passes its frozen limit: `5e-8` for local flow, `1e-8` for endpoint
state, `0.005` for both derivative controls, and `0.02` for adjacent plateaus.

### Complete step retention

| root | repaired plateaus `2e-6→5e-7`, `5e-7→1e-7` | repaired ↔ independent columns at `2e-6`, `5e-7`, `1e-7` |
|---|---|---|
| `shared_zero` | `0.000208235`, `0.00140100` | `0.0000231840`, `0.000185061`, `0.00121592` |
| `phi_plus` | `0.000140445`, `0.000499401` | `0.00000944014`, `0.000149792`, `0.000649081` |
| `a_plus` | `0.000159603`, `0.000822132` | `0.0000185603`, `0.000178106`, `0.000643758` |

All eighteen solvers completed with 15,362–15,407 RHS evaluations and
1,024–1,027 accepted steps.  Ninety trajectory probes were retained.

Residual-relative endpoint values can be as large as `0.838` because the
reference residual is near zero.  That unstable normalization was retained
for disclosure but was not a frozen pass criterion; endpoint state and the
actual residual-derived columns are the relevant controls.

### What changed relative to Phase 48

Promoting only the generated gradient did not pass.  Promoting the complete
local flow reduced the worst derivative-column discrepancies by factors of
about 21.1, 80.2, and 12.8 at `shared_zero`, `phi_plus`, and `a_plus`.  The
worst adjacent plateaus improved by factors of about 18.1, 111.8, and 7.62.

This ablation isolates the required implementation boundary: retaining
extended precision through state formation and contraction matters; casting
the gradient back to complex128 before `L.T @ g` is too early.

## 4. Interpretation

### Calculated facts

- The declared 63-mantissa-bit NumPy path completes all eighteen integrations.
- All frozen local-flow, endpoint-state, derivative-column, tangent, and
  complete-ladder checks pass without output selection.
- The full-flow path passes where the gradient-only path fails, under otherwise
  identical roots, steps, solver settings, and references.
- The exact/high-precision Phase-46 path and Phase-45 variational tangent remain
  mutually consistent references.

### Scoped inference

For this workbench and platform, the practical repair is to retain
`clongdouble` from `saddle + L @ xi` through the generated gradient and
`-conjugate(L.T @ gradient)`, then cast the completed RHS once at the solver
boundary.  This closes the Phase-48 full-flow repair control and supplies a
validated source state-map implementation recipe.

The result does not show that every platform's `clongdouble` has this precision
or that a formal endpoint error bound follows from local arithmetic.  A
portable implementation must check the frozen dtype contract or use the
Phase-43 exact/high-precision reference path.

## 5. Boundary

Phase 49 does not rewrite the historical Phase-41 calculation, alter the
Phase-44 formula audit, perform a new root search, retune parameters, or replace
the Phase-45 tangent estimator.  It provides no fundamental-matrix error bound
and makes no global cycle, determinant-line, signed-intersection, or physical
claim.

Global promotion remains prohibited and Gate 1 remains
`OPEN_PARTIAL_PROGRESS`.

## Bottom line

```text
long-double platform contract:             PASS
full-flow hybrid integrations:             18 / 18 complete
intermediate hybrid/reference probes:      90 / 90 retained; PASS
endpoint-state agreement:                  PASS at 3 / 3 roots
full three-step ladders:                    PASS at 3 / 3 roots
all-step independent-column comparison:    PASS at 3 / 3 roots
all-step Phase-45 tangent comparison:       PASS at 3 / 3 roots
classification:                            FULL_FLOW_CLONGDOUBLE_STATE_MAP_REPAIR_SUPPORTED
global promotion:                          PROHIBITED
Gate 1:                                    OPEN_PARTIAL_PROGRESS
```
