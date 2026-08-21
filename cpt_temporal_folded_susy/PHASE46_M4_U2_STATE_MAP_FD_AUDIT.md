# Phase 46 — m=4 `u2` state-map finite-difference audit

## Outcome

Phase 46 evaluates the historical three-step `u2` central-difference ladder at
the three immutable Phase-42 roots. It consumes the complete pinned Phase-42
production, tight DOP853, and realified Radau endpoint ledgers and newly
integrates all eighteen signed endpoints with the independently reconstructed
Phase-43 exact-decimal local flow RHS at 80 decimal digits.

The guarded run completed with

```text
run_status:       VALID_RUN
classification:  LOCAL_FLOW_RHS_REPAIR_SUPPORTED
targets:          3 / 3 complete
state paths:      72 / 72 retained
precision probes: 36 / 36 retained
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The independently reconstructed state path has a maximum adjacent-step plateau
of `2.019e-7`, far below the frozen `0.02` limit, across all three roots. Its three
finite-difference columns agree with the Phase-45 independent tangent column to
at worst `2.858e-7`, below the frozen `0.005` limit. The retained 50/80-digit
local RHS probes are identical after the final complex128 projection.

The source tight-DOP853 and Radau endpoints remain normwise close to the
independent endpoints, at worst `3.022e-9` and `2.071e-9`. Those small endpoint
differences are amplified by division by `2h`: source tight-DOP853 derivative
columns differ from the independent columns by as much as `0.8701`, and Radau
columns by as much as `0.02379`. Both exceed the frozen `0.005` column limit.
The pre-output classification therefore selects `LOCAL_FLOW_RHS_REPAIR_SUPPORTED`.

This is a calculation-workbench label. It supports repair under the declared
independent local flow RHS and fixed complex128 solver projection. It does not
prove that a source formula is wrong, identify one arithmetic stage as the
unique cause, rewrite the historical Phase-41 result, or establish any global
physical intersection.

## 1. Frozen inputs and execution

The final pre-output input manifest fixes

- the Phase-42 checkpoint, result, three roots, and all 54 complete source
  endpoint slots used here;
- the Phase-43 independent exact-decimal action/gradient construction;
- the Phase-45 independent 80-digit tangent Jacobian at each root;
- `u2` parameter index 8 and the steps `2e-6`, `5e-7`, and `1e-7`, with both
  signs retained;
- production DOP853, tight DOP853, realified Radau, and independent 80-digit
  DOP853 state paths;
- the historical Phase-41 plateau metric, symmetric-relative comparisons,
  all thresholds, and the fail-closed three-way classification.

The source integrations are not duplicated. The pinned Phase-42 result already
contains every requested endpoint under the identical solver settings, with
complete solver ledgers. Phase 46 validates each slot key, point, tier, chart,
column, step, sign, terminal status, residual, and complex state before reuse.
Only the eighteen independent state paths are newly integrated.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `3a7c905e1cc634b7cea40f127f2d9975ce99b78e` | `e69f31aeedc4078a9c801757399890d4c4f5ae01b1f24eb915567f3a2efe8b16` |
| runner | `45cab780121370ba3bd125ffcabfbf00a37cacc1` | `a71badb3c49a4af44e5e4a1b8bec244593f1de5a43c3b0d71d729f92ef147d55` |
| raw result | `e7a8ec45a26e4af9297ad5694111436e43c0bd6a` | `8349eb669c542dfb13555554f3f81d70f2843520240ab66ccbbca4226081fad0` |

The successful command was equivalent to

```bash
proxmox-scratch run ice-phase46 --timeout 7200 -- \
  ./ice run phase46_m4_u2_state_map_fd_audit
```

The 206,749-byte result has schema `ice-phase46-u2-state-map-fd-audit/v1`.
Its self-excluding canonical digest is
`e0cb161869ded53a727b18eec59242202c007473a2e045a3f4e96e1ee5d473cd`;
an independent standard-library parse reproduced it exactly. The final run used
CPython 3.13.5, NumPy 2.5.2, SciPy 1.18.0, SymPy 1.14.0, and mpmath 1.3.0.

Two earlier attempts produced no result. The first was stopped after the
realified Radau path lacked sufficiently frequent progress telemetry. The
second exposed approximately 245,000 Radau RHS evaluations before completion
of even one endpoint. Inspection showed that the identical complete Radau
endpoints already existed in the pinned Phase-42 ledger. Before observing any
Phase-46 numerical result, the manifest and runner were updated to consume all
three completed source tiers and reserve new work for the independent path.

## 2. Fixed calculation

For each root, step `h`, and sign, the parameter vector differs only in `u2`:

\[
p_{h,\pm}=p_*\pm h e_{u2}.
\]

The source local state flow is the pinned Phase-41 map. The independent path
evaluates the exact-decimal Phase-43 gradient after exactly lifting the fixed
binary64 saddle, linear map, and current state into mpmath at 80 digits; the
complete RHS is rounded once to complex128 for DOP853. Every independent path
uses `rtol=2e-12`, `atol=2e-14`, and `max_step=0.01`.

At each endpoint, the same cap state and coordinate scales form the real
14-component residual `R`. The retained central-difference column is

\[
D_h=\frac{R(p_*+he_{u2})-R(p_*-he_{u2})}{2h}.
\]

For adjacent steps `h_1,h_2`, the unchanged Phase-41 plateau metric is

\[
C(h_1,h_2)=\frac{\lVert D_{h_1}-D_{h_2}\rVert_2}
{\max(\lVert D_{h_1}\rVert_2,10^{-30})}.
\]

The symmetric relative comparison is

\[
r(x,y)=\frac{\lVert x-y\rVert_2}
{\max(\lVert x\rVert_2,\lVert y\rVert_2,10^{-300})}.
\]

No step is discarded or selected after observing the output. Both adjacent
pairs are retained and the classification uses the maximum where declared.

## 3. Results

### Adjacent-step plateau

| root | path | `2e-6 → 5e-7` | `5e-7 → 1e-7` |
|---|---|---:|---:|
| `shared_zero` | production | `0.298850` | `1.37964` |
|  | tight DOP853 | `0.0407453` | `0.391540` |
|  | Radau | `0.00190533` | `0.0258106` |
|  | independent 80 dps | `1.22667e-8` | `2.78470e-8` |
| `phi_plus` | production | `0.221993` | `5.73966` |
|  | tight DOP853 | `0.377118` | `1.61681` |
|  | Radau | `0.00336848` | `0.0213400` |
|  | independent 80 dps | `9.26360e-8` | `1.05570e-7` |
| `a_plus` | production | `0.795272` | `2.41918` |
|  | tight DOP853 | `0.0289793` | `1.36819` |
|  | Radau | `0.0177855` | `0.0389446` |
|  | independent 80 dps | `5.70203e-8` | `2.01838e-7` |

The production first-pair values reproduce the historical Phase-41 values
exactly. Every production and tight first pair fails the `0.02` limit. Radau's
first pair passes at every root, but its second pair fails at every root. The
independent path passes both pairs by roughly five orders of magnitude.

### Cross-path comparisons

| root | tight endpoint ↔ independent | Radau endpoint ↔ independent | max tight column ↔ independent | max Radau column ↔ independent | max independent column ↔ Phase-45 tangent |
|---|---:|---:|---:|---:|---:|
| `shared_zero` | `3.02166e-9` | `2.07052e-9` | `0.442850` | `0.0237913` | `6.80860e-8` |
| `phi_plus` | `1.72640e-9` | `2.18920e-10` | `0.870143` | `0.0180459` | `2.85784e-7` |
| `a_plus` | `1.46137e-9` | `1.66021e-10` | `0.866736` | `0.0223609` | `1.14098e-7` |

All endpoint comparisons pass their `1e-8` limits. All source derivative-column
maxima fail their `0.005` limits. All independent columns pass the `0.005`
Phase-45 tangent comparison, and all independent full ladders pass the `0.02`
plateau limit. The independent integrations used 12,290–12,326 RHS evaluations
per endpoint.

## 4. Interpretation boundary

### Calculated facts

- The independent 80-digit local flow RHS produces stable `u2` central
  differences across all three declared steps and roots under the final
  complex128 DOP853 projection.
- Those independent finite differences agree with the independently rebuilt
  Phase-45 integrated-tangent `u2` columns at the `1e-7` scale.
- The source tight-DOP853 and Radau endpoint states are close to the independent
  endpoint states, but their `u2` finite differences are not stable across the
  complete historical step ladder.
- Dividing close endpoint differences by the smallest `2h` amplifies them into
  derivative-column discrepancies above the frozen limit.
- The historical production first-pair failures are reproduced exactly.

### Scoped interpretation

Under the pre-output classification, replacing the local source flow RHS by
the independently reconstructed exact-decimal RHS repairs the failed `u2`
state-map finite-difference ladder. The Phase-45 tangent result and the new
state-map result now agree: the independently reconstructed tangent and state
derivative paths are mutually stable at the three fixed roots.

This narrows the failure to the source local-flow arithmetic plus its
interaction with complex128 endpoint integration and small-step cancellation.
It argues against interpreting the failed plateau as a property of the fixed
roots or of the independently reconstructed local dynamics.

### Not established

- The calculation does not prove the Phase-41 source flow formula is wrong;
  the declared mathematical formula may be identical while finite arithmetic
  differs.
- It does not uniquely separate source coefficient rounding, state rounding,
  gradient contraction, solver accumulation, and final subtractive
  cancellation.
- The independent RHS is evaluated internally at 80 digits but integrated as
  complex128. This is not an arbitrary-precision state integrator theorem.
- The historical Phase-41 result remains 8/9 as a provenance record. Phase 46
  supplies a new local diagnostic rather than rewriting that run.
- No root search, retuning, orientation selection, determinant line, complete
  chain, good-end census, Stokes chamber, original physical cycle, or global
  signed intersection is computed.
- Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and no physics or quantum-gravity
  conclusion follows.

## 5. Minimal next calculation

The smallest next local diagnostic is a source-gradient flow error budget along
the eighteen retained independent state paths. At frozen launch/intermediate/
endpoint samples it should compare the Phase-41 `flow_xi` output with the exact
Phase-43 gradient and decompose coefficient, state, gradient, and contraction
rounding before integration. It should then propagate the observed local bounds
to endpoint absolute error and to `D_h` amplification for all three fixed steps.

That calculation can distinguish a mixed source arithmetic budget from solver
accumulation and pure final subtraction without another root search. It still
would be a local tool-control study. The physical Gate-1 debt remains the
regulated original cycle, complete upward-component and good-end census,
Stokes data, common determinant orientation, and signed global intersections.

## Bottom line

```text
historical production first-pair plateau: exactly reproduced; FAIL at 3/3 roots
independent 80-dps full ladder:            PASS at 3/3 roots
independent 50/80 local RHS probes:        PASS at 36/36 slots
source endpoint agreement:                 PASS for tight and Radau at 3/3 roots
source derivative-column agreement:        FAIL for tight and Radau at 3/3 roots
independent column / Phase-45 tangent:      PASS at 3/3 roots
fixed classification:                      LOCAL_FLOW_RHS_REPAIR_SUPPORTED
global promotion:                          PROHIBITED
Gate 1:                                   OPEN_PARTIAL_PROGRESS
```
