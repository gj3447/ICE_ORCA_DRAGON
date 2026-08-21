# Phase 45 — m=4 integrated tangent RHS stability

## Outcome

Phase 45 reintegrates the six chart-tangent columns at the three immutable
Phase-42 roots along one fixed source NumPy64 state trajectory. It compares
the Phase-41 NumPy64 Hessian-action RHS with an independently reconstructed
exact-decimal RHS evaluated at 50 and 80 decimal digits. The guarded production
run completed with

```text
run_status:       VALID_RUN
classification:  TANGENT_CONTROL_FAILURE_STABLE_TO_INDEPENDENT_RHS
targets:          3 / 3 complete
fixed tests:      18 / 18 PASS
normalized signs: -1 / -1 / -1
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The independent 50- and 80-digit paths give identical retained complex128
tangent samples at all five flow fractions. The source and 80-digit tangent
paths differ by at most `2.741e-12` in the fixed normwise metric. Their assembled
root Jacobians differ by at most `3.748e-12`, while the independent Jacobians
remain within `1.101e-5` of the Phase-42 fixed R4 matrices and retain normalized
sign `-1`.

The historical Phase-41 `u2` finite-difference plateau values remain
`0.298850`, `0.221993`, and `0.795272`, all above the frozen `0.02` failure
threshold. Those values are pinned historical inputs, not recomputed state-map
finite differences in Phase 45. The new calculation shows that replacing the
integrated tangent's local Hessian-action arithmetic does not repair or
materially change the tangent/Jacobian path at these roots.

This is a calculation-workbench result. It does not turn the finite-difference
plateau into physics, validate a global orientation, or compute a global
intersection coefficient.

## 1. Frozen inputs and execution

The pre-output input manifest was committed before the production run. It fixes

- the Phase-42 checkpoint and result;
- the byte-pinned Phase-41 source;
- the Phase-43 independent exact-decimal action construction;
- the three roots `shared_zero`, `phi_plus`, and `a_plus`;
- one source NumPy64 state-only DOP853 trajectory per root;
- source NumPy64, independent 50-digit, and independent 80-digit tangent paths;
- DOP853 `rtol=2e-12`, `atol=2e-14`, and `max_step=0.01` for state and tangent
  integrations;
- five samples at fractions `0, 1/4, 1/2, 3/4, 1`;
- all comparison thresholds and the three-way classification rule.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| input manifest | `a5eac15e54a4f6e4aec8381b526a61c22fd0570f` | `34d88f6f080b9720a056d8406c1d8e807fc0578d98f30a6aa5d010fbed5d3a87` |
| runner | `8657bb6` | `e562314282ccf58be0c39aebc2b5a07c0c8bb818ae739f24ace6cad6a8f915b2` |
| raw result | `6831c80` | `b2be69bd38cbbc22425b926de830c5750fa7ae99b00830e828a528cc491a12d5` |

The successful production command was equivalent to

```bash
proxmox-scratch run ice-phase45 --timeout 7200 -- \
  ./ice run phase45_m4_integrated_tangent_rhs_stability
```

The exact capture command piped the single `RESULT_JSON=` record into
`PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_RESULT.json`. The 143,499-byte
result has schema `ice-phase45-integrated-tangent-rhs-stability/v1`. Its
self-excluding canonical digest is
`b82ae1fdfb6b343ef5575ee8d0398500342189e801b9cce5db498ffcee931832`;
an independent post-run parse reproduced that digest exactly.

An earlier direct attempt was interrupted before producing a result after the
high-precision cost proved larger than the initial estimate. The production
runner then added progress-only telemetry, and the complete calculation ran in
bounded scratch. The scientific manifest, equations, thresholds, and retained
paths did not change.

The production runtime was CPython 3.13.5 with NumPy 2.5.2, SciPy 1.18.0,
SymPy 1.14.0, and mpmath 1.3.0.

## 2. Fixed calculation

The state trajectory is the source NumPy64 flow

\[
\dot\xi=V_{64}(\xi)
\]

integrated once per root with dense output. The tangent matrix
`Q` has the six affine-chart launch derivatives as columns and obeys

\[
\dot Q=-\overline{H_\xi(\xi)Q}.
\]

The three tangent paths differ only in the local action used on the right-hand
side:

1. the Phase-41 NumPy64 `hessian_xi @ Q` path;
2. the independently rebuilt exact-decimal action evaluated with mpmath at 50
   digits, with the complete contraction rounded once to complex128;
3. the same independent path at 80 digits.

The binary64 fixed saddle, linear map, dense state, and current tangent are
lifted exactly into mpmath. Both independent precision paths share the same
state trajectory and solver tolerances. Tangent evolution does not feed back
into the state trajectory.

At the endpoint, each tangent is mapped to the physical-coordinate K frame.
The positive flow-time column and unchanged Phase-42 cap frame then form the
same row-scaled real root Jacobian convention as Phase 42. No determinant sign
is selected from an observed preference; the normalized sign is a retained
comparison.

The symmetric relative metric is

\[
r(x,y)=\frac{\lVert x-y\rVert_2}
{\max(\lVert x\rVert_2,\lVert y\rVert_2,10^{-300})}.
\]

## 3. Results

| root | max 50↔80 tangent | max source↔80 tangent | source↔80 root J | 80-digit J↔R4 | sign | historical `u2` plateau |
|---|---:|---:|---:|---:|---:|---:|
| `shared_zero` | 0 | `1.57946e-12` | `4.98132e-13` | `1.07964e-5` | -1 | `0.298850` |
| `phi_plus` | 0 | `1.33460e-12` | `6.07599e-13` | `1.10009e-5` | -1 | `0.221993` |
| `a_plus` | 0 | `2.74036e-12` | `3.74737e-12` | `5.84132e-6` | -1 | `0.795272` |

The fixed limits were `1e-10` for 50/80 precision stability, `1e-8` for both
source/reference tangent and root-Jacobian agreement, `0.005` for the
reference/R4 Jacobian comparison, sign `-1`, and `0.02` for the historical
plateau failure. Every named test passes at every root.

The state integrations used 16,463–17,051 RHS evaluations. Each tangent path
used 15,362 or 15,407 evaluations depending on the root. Within each root the
source, 50-digit, and 80-digit tangent solvers took exactly the same accepted
step and RHS-evaluation counts.

## 4. Interpretation boundary

### Calculated facts

- The independently specified 50- and 80-digit tangent paths are stable under
  the retained complex128 projection at all sampled fractions.
- Replacing the source NumPy64 local Hessian-action arithmetic changes the
  integrated tangent and root Jacobian only at the `1e-12` scale in this fixed
  calculation.
- The independent root Jacobians retain sign `-1` and remain close to the
  Phase-42 R4 matrices.
- All three historical Phase-41 `u2` plateau values remain failed inputs.

### Scoped interpretation

The Phase-41 tangent-control failure is stable to this independently specified
local tangent RHS replacement. The Phase-44 mixed local rounding differences
do not amplify into a material integrated-tangent or root-Jacobian change at
these fixed roots. This narrows the unresolved numerical issue toward the
finite-difference state-map/step-selection layer rather than the analytic
tangent RHS.

### Not established

- Phase 45 does not recompute the finite-difference state-map ladder, so it does
  not identify the unique cause of the `u2` plateau.
- Exact equality of the stored 50/80 samples follows after final complex128
  projection; it is not a claim that their internal arbitrary-precision values
  are symbolically identical.
- The shared source state trajectory isolates tangent-RHS replacement but does
  not test an independently integrated high-precision state flow.
- The historical Phase-41 contract remains 8/9 and is not rewritten.
- No root, full chain, good-end census, Stokes chamber, determinant line,
  original physical cycle, or global intersection integer is computed.

## 5. Minimal next calculation

The smallest remaining local diagnostic is a separately frozen `u2` state-map
finite-difference audit at the same roots. It should compare the unchanged
Phase-41 step pair with an independently specified high-accuracy state-flow
reference while retaining every declared step, so solver truncation,
subtractive cancellation, and step-pair selection can be separated without
choosing a favorable replacement after observing the output.

That calculation would address the historical 8/9 tool-control record only.
Even a repaired finite-difference plateau would not close Gate 1. The physical
Gate-1 debt remains the complete regulated original cycle, all upward
components and good ends, Stokes data, determinant orientation, and signed
global intersections.

## Bottom line

```text
independent tangent precision stability: PASS at 3/3 roots
source/reference integrated tangent:     agrees within 2.741e-12
source/reference root Jacobian:           agrees within 3.748e-12
reference/R4 root Jacobian:               agrees within 1.101e-5
normalized local root signs:              -1 at 3/3 roots
historical Phase-41 u2 plateau:            still failed at 3/3 roots
local RHS replacement repairs failure:    NO
global promotion:                         PROHIBITED
Gate 1:                                   OPEN_PARTIAL_PROGRESS
```
