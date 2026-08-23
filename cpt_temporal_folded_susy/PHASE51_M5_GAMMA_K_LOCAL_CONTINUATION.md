# Phase 51 — nonlinear m=5 Gamma–K local continuation on the frozen diagonal path

## Outcome

Phase 51 completed a valid, fully serialized calculation of one nonlinear
`m=5` Gamma–K cap candidate in `R18`.  The independently initialized
`phi_plus` branch completed its fine-forward, coarse-forward, and fine-reverse
continuations along the Phase-50 diagonal action/metric path.  The independent
`phi_minus` reflection control, three full-J finite-difference controls, the
outer lambda-tangent control, four endpoint mutations, and every action and
first-cap ledger also completed.

The frozen result is nevertheless **inconclusive**:

```text
run_status:       VALID_RUN
exact checks:     6 / 6 PASS
numerical checks: 9 / 10 PASS
non-passing check: P51.evaluator.CSE_nonCSE_pairs
classification:  PHI_PLUS_M5_GAMMA_K_LOCAL_CONTINUATION_INCONCLUSIVE
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The sole non-pass is the predeclared CSE/non-CSE same-point RHS relative-error
gate.  Its worst value was `1.6900132129978792e-8`, above the frozen `5e-10`
limit.  The paired Hessian-action, trajectory-state, endpoint-state, and
absolute residual-difference controls remained within their respective
limits, but the manifest requires every numerical check to pass before the
supported label can be selected.

This is not a contradiction and not a no-root result.  All 68 retained
main, endpoint, and outer-tangent roots were accepted.  The runner is forbidden
to select the contradiction label without a separately frozen interval,
augmented-fold, or local-degree certificate, and Phase 51 implements none.
`VALID_RUN` records that the declared calculation and provenance were valid;
it does not override the frozen scientific classification rule.

As in earlier phases, this is a finite-dimensional calculation workbench.  It
is not a global intersection count, cutoff theorem, continuum result, physical
cycle, or physics claim.

## 1. Frozen inputs and execution provenance

The Phase-51 manifest froze the source pair, `R18` root map, Phase-50 diagonal
path, meshes, nonlinear-flow evaluator, finite-difference steps, endpoint
mutations, tolerances, fail-closed classification, and global null boundary
before the runner or authoritative result was committed.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| frozen input manifest | `80dda66aa57276de6e3940c35e58e89d34d28721` | `0e9191d5c98cc1a56d7ffbcdd98ac02558457b87b6abf518ff754fbf4af7bd87` |
| runner | `24508e323c2336c33d87ecf2786a46e0edb429ee` | `eb535f5a16687dccb47399e3ff7dceefe0ecabc6417574fd2f29abc008e1d7c9` |
| raw result | `ab14d0d0eacc09da64d5c8061fa0890179cd79aa` | `b74c8b735b32790c85d7e14fbf78fe16bf437995d707268d209d4a655c3d8531` |

The authoritative command was

```bash
proxmox-scratch run phase51-production --timeout 7200 -- \
  uv run python cpt_temporal_folded_susy/phase51_m5_gamma_k_local_continuation.py
```

The 1,628,760-byte result has schema
`ice-phase51-m5-gamma-k-local-continuation/v1`.  Its self-excluding canonical
digest is
`153d2350c96114a137b0da3f2eaa37b9224a0081e602164702e28867cbd99e0d`.
An independent strict standard-library parse rejected duplicate and nonfinite
tokens, reproduced both the outer file hash and this self-digest, matched the
embedded runner hash to the committed source, counted 6 exact and 10 numerical
records, and identified exactly the one non-passing numerical check named
above.

The runtime matched the frozen Phase-49-compatible platform contract: Python
`3.13.5`, NumPy `2.5.2`, SciPy `1.18.0`, and SymPy `1.14.0`, with 16-byte
`longdouble`, 32-byte `clongdouble`, 63 explicit mantissa bits, and epsilon
`1.084202172485504434e-19`.

The manifest byte-pins the Phase-41 source and inputs, the Phase-42 fixed-root
checkpoint, the Phase-49 clongdouble flow repair, the Phase-50 action/metric
bridge and result, and both package locks.  All eleven pins and all three
upstream self-digests validated before numerical work began.

## 2. Frozen `R18` construction and conventions

The production target is the Phase-42 `phi_plus` source

\[
(\delta_a,\delta_\phi)=(0,+10^{-3}),
\]

with independently initialized reflected control `phi_minus` at
`(0,-10^{-3})`.  A reflected `phi_plus` solution is never substituted for the
independent `phi_minus` solve.

### Action, mobility, and nonlinear flow

On the diagonal Phase-50 path, `lambda=mu=t`,

\[
S_t=(1-t)S_{4,\mathrm{lift}}+tS_5,
\]

and the mobility is the frozen affine-invariant SPD geodesic

\[
M_t=M_0^{1/2}
\left(M_0^{-1/2}M_1M_0^{-1/2}\right)^tM_0^{1/2}.
\]

With Phase-50 positive-determinant common basis `B`, Phase-42 factor `L4`, and
stabilizers

\[
\kappa_a=-1.4\times10^5,
\qquad
\kappa_\phi=2.4\times10^4,
\]

the common real factor is

\[
A_0=B\,\operatorname{blockdiag}
\left(L_4,|\kappa_a|^{-1/2},\kappa_\phi^{-1/2}\right),
\]

\[
A_t=M_t^{1/2}M_0^{-1/2}A_0,
\qquad A_tA_t^T=M_t.
\]

Writing `w=w_saddle+A_t xi`, every K point is obtained from the nonlinear
holomorphic-gradient flow

\[
\dot\xi=-\overline{A_t^T\nabla_w S_t(w)}.
\]

The transpose is deliberately not Hermitian.  The implementation evaluates
the full nonlinear flow at every residual call; the transported tangent plane
is not used as a replacement intersection.

At each path node the real Hessian in factor coordinates,

\[
H_\xi=A_t^T H_t A_t,
\]

is split into its ordered five-negative and four-positive subspaces.  The
blocks are determinant-aware Procrustes-aligned to the frozen gauge, and the
signed restricted-Hessian launch shape is recomputed.  Every sampled saddle
retained inertia `(5-,4+,0)`.

### Gamma cap, K chart, and orientation

Let `P` and `q` be the pinned Phase-50 prolonged and added-mode columns.  For
each field,

\[
d_a=P y_a+q\,y_{a,\mathrm{add}},
\qquad
d_\phi=P y_\phi+q\,y_{\phi,\mathrm{add}},
\]

and at the four interior nodes

\[
a_j=\bar a_j+e^{i(\psi/2-\pi/2)}d_{a,j},
\qquad
\phi_j=\bar\phi_j+e^{i\psi/2}d_{\phi,j},
\qquad
T=0.3e^{i\psi}.
\]

The solved equation is

\[
\Gamma_5(y,\psi;\text{source})
-K_{5,t}(u,\tau;\text{source})=0\quad\text{in }\mathbb R^{18}.
\]

Gamma has nine real parameters: six prolonged field coordinates, two added
coordinates, and `psi`.  K has eight `S8` chart coordinates plus flow time
`tau`.  The residual is realified in interleaved real/imaginary order after
division by the nine frozen physical coordinate scales.  The immutable
Phase-42 `S6` chart, augmented by the two stabilizer axes, has positive `S8`
orientation.

The Gamma tangent uses the exact six `P` columns, two `q` columns, and the
analytic `psi` derivative.  The K tangent integrates eight variations

\[
\dot Z=-\overline{(A_t^T H_t A_t)Z}
\]

and appends the positive endpoint flow vector for `tau`.  The variational root
Jacobian and direct orientation are

\[
J_R=[V_\Gamma,-V_K],
\qquad
\operatorname{sign}\det_{\mathbb R}[V_\Gamma,V_K].
\]

Because K has nine columns, the frozen parity convention requires the root
Jacobian sign to be the negative of the direct sign.

The production gradient and Hessian use one joint canonical-CSE
`clongdouble` evaluator.  State formation, CSE temporaries, Hessian action,
`A_t.T` contraction, and outer conjugation remain in `clongdouble`, with one
completed RHS cast to `complex128` at `solve_ivp`; the action is evaluated from
the same pinned symbolic model in `clongdouble`.  The validation gradient and
Hessian are independently lambdified without the CSE replacement list or
output cache.

## 3. The sampled continuation itself completed

All declared continuation paths completed without fallback, random restart,
reflected-seed substitution, mesh insertion, clipping, or chart recentering.

| source/path | requested roots | retained roots | result |
|---|---:|---:|---|
| `phi_plus` fine forward | 17 | 17 | PASS |
| `phi_plus` coarse forward | 9 | 9 | PASS |
| `phi_plus` fine reverse | 17 | 17 | PASS |
| `phi_minus` independent fine forward | 17 | 17 | PASS |

The four endpoint mutations add four accepted roots.  The lambda-tangent
control independently solves four more off-mesh roots, for 68 accepted roots
in the retained result.

At lambda zero, the invariant normalized cap-state distance to the embedded
Phase-42 seed was `8.915e-12` for `phi_plus` and `1.100e-11` for `phi_minus`.
Across all common Phase-50 saddle reproductions, the maximum saddle distance
was `2.544e-12`, the maximum gradient component was `1.834e-11`, and the
minimum absolute Hessian eigenvalue was `4.19425`.  The frozen limits are
`1e-8`, `2e-8`, and `0.1`, respectively.

Across all 68 accepted roots:

| diagnostic | observed worst | frozen limit | status |
|---|---:|---:|---|
| physical residual max-absolute | `1.360e-9` | `2e-7` | PASS |
| scaled residual max-absolute | `1.943e-9` | `2e-7` | PASS |
| Gamma rank | `9` at every root | `9` | PASS |
| K rank | `9` at every root | `9` | PASS |
| direct normalized transversality `sigma_min` | `0.0646752` minimum | `2e-4` minimum | PASS |
| root-Jacobian normalized `sigma_min` | `0.0217386` minimum | descriptive companion | PASS |
| factor identity relative residual | `2.841e-15` maximum | `5e-12` | PASS |
| flow-coordinate norm | `1.30337` maximum | `<40` | PASS |

Every direct orientation sign was `+1`, every root-Jacobian sign was `-1`, and
all parameter-window margins remained well inside their frozen bounds.  The
smallest field, chart, flow-time, and flow-norm margins were `0.248859`,
`0.306996`, `2.57253`, and `38.6966`, respectively.

The invariant path and reflection comparisons were also much smaller than the
frozen state-distance gates:

| comparison | observed worst | frozen limit | status |
|---|---:|---:|---|
| `phi_plus` coarse/fine cap-state distance | `1.174e-11` | `5e-5` | PASS |
| `phi_plus` reverse/fine cap-state distance | `8.781e-12` | `5e-5` | PASS |
| independent `phi_minus` reflected cap-state distance | `6.773e-16` | `5e-5` | PASS |
| reflected saddle distance | `2.811e-12` | diagnostic | PASS |
| reflected saddle-action absolute difference | `9.381e-15` | `2e-7` | PASS |

The mesh and reverse comparisons use normalized ambient cap states and
determinant-corrected tangent gauges, not raw chart coordinates.  The
reflection comparison uses two independently solved paths and checks saddle,
action, cap state, transversality, and corrected orientation at all 17 fine
nodes.

## 4. Full-J, path-tangent, and endpoint controls passed

At lambda `0`, `0.5`, and `1`, all 18 columns of the complete `R18` state map
were central-differenced at both frozen step sizes.  No per-column step was
selected after observing the result.

| lambda | FD/variational operator relative | worst column relative | worst adjacent-step relative | frozen limits |
|---:|---:|---:|---:|---:|
| `0` | `2.462e-6` | `4.653e-4` | `3.013e-3` | `2e-2` |
| `0.5` | `1.365e-6` | `6.398e-4` | `7.619e-4` | `2e-2` |
| `1` | `4.388e-6` | `9.238e-4` | `6.453e-3` | `2e-2` |

At lambda `0.5`, the implicit path tangent includes the re-solved saddle,
metric, signed frame, chart, and nonlinear flow.  It was compared with four
independently solved off-node roots at steps `2e-4` and `5e-5`.  The worst
implicit/resolved relative error was `3.633e-8` against `1e-2`; the
adjacent-step implicit-tangent change was `1.969e-4` against `2e-2`.

At lambda `1`, the launch radius was changed from `1e-4` to `5e-5` and `2e-4`,
and the signed-Hessian shape exponent from `1` to `0.5` and `0`.  All four
mutations retained rank, transversality, corrected orientation, parameter
margins, action monotonicity, and the first-cap event.  Their normalized
cap-state distances from the primary candidate were:

| endpoint mutation | normalized cap-state distance | frozen limit |
|---|---:|---:|
| radius `5e-5` | `1.826e-14` | `5e-5` |
| radius `2e-4` | `1.804e-14` | `5e-5` |
| shape exponent `0.5` | `3.758e-24` | `5e-5` |
| shape exponent `0` | `4.360e-16` | `5e-5` |

These are same-candidate controls under the declared local chart.  They do not
show independence from arbitrary radii, launch shapes, or charts.

## 5. All 64 main/endpoint and four outer flow ledgers passed

The result retains 60 continuation ledgers and four endpoint-mutation ledgers,
for 64 main/endpoint ledgers.  The path-tangent calculation adds four outer
off-node ledgers.  Every one of the 68 ledgers contains 101 action samples and
an independent terminal `|T|=0.3` event integration.

| ledger diagnostic | observed worst | frozen limit | status |
|---|---:|---:|---|
| maximum positive sampled increment of `Re(S)` | `-3.052e-10` | at most `5e-8` | PASS |
| maximum `Im(S)` drift | `4.757e-31` | `5e-8` | PASS |
| retained/event endpoint-state match | `1.874e-9` | recorded cross-check | PASS |
| first-cap radius residual | `2.715e-16` | `2e-7` | PASS |
| first-cap flow-time difference | `5.724e-9` | `5e-6` | PASS |
| first-cap normalized endpoint-state distance | `4.885e-11` | `2e-6` | PASS |
| maximum flow-coordinate norm | `1.30337` | `<40` | PASS |

Thus every accepted primary and declared control trajectory reached the same
first cap within tolerance while `Re(S)` remained nonincreasing on its sampled
ledger.  This is a retained numerical path check, not a proof about unsampled
trajectories or other cap reintersections.

## 6. The frozen evaluator pair is the only non-pass

The exact evaluator check passed.  Canonical CSE back-substitution reproduced
the unreduced symbolic expressions exactly, all frozen `clongdouble` platform
and dtype requirements held, and the CSE and non-CSE Hessian actions agreed
well inside the `5e-10` relative limit.

The numerical paired-evaluator check did not pass because of its independent
same-point RHS relative criterion.  At the declared center/launch state, the
worst source-specific values were:

| source | worst RHS relative | worst Hessian-action relative | RHS limit | result |
|---|---:|---:|---:|---|
| `phi_plus` | `1.683e-8` | `1.356e-13` | `5e-10` | INCONCLUSIVE |
| `phi_minus` | `1.686e-8` | `1.348e-13` | `5e-10` | INCONCLUSIVE |

The runner also independently reintegrated the solved central `phi_plus`
trajectories with the non-CSE backend and compared five fixed trajectory
fractions:

| lambda | worst same-point RHS relative | worst Hessian-action relative | endpoint-state relative | scaled-residual absolute difference |
|---:|---:|---:|---:|---:|
| `0` | `6.253e-9` | `1.013e-12` | `6.371e-10` | `6.562e-9` |
| `0.5` | `1.152e-8` | `5.018e-13` | `1.135e-9` | `1.168e-8` |
| `1` | `1.690e-8` | `1.097e-13` | `1.586e-9` | `1.630e-8` |

The endpoint-state relative limit is `2e-7`, the absolute scaled-residual
difference limit is `2e-7`, and the Hessian-action relative limit is `5e-10`;
those columns pass.  The RHS relative limit is `5e-10`, so all three rows are
non-passing on that criterion.  The residual-relative comparison is explicitly
descriptive only and was not used to rescue or reject a trajectory.

No non-CSE output selected, repaired, or replaced a production root.  The
failure therefore leaves a valid serialized run with one unresolved evaluator
agreement condition.  It neither erases the accepted roots nor permits the
stronger supported label.

## 7. Frozen check ledger

All six declared exact checks passed:

| exact check | status |
|---|---|
| `P51.inputs.byte_pins_and_manifest_before_runner` | PASS |
| `P51.action.Phase50_diagonal_path_identity` | PASS |
| `P51.cap.R18_middle_dimension_and_common_coordinate_lambda0_lift` | PASS |
| `P51.evaluator.CSE_symbolic_reconstruction_and_clongdouble_contract` | PASS |
| `P51.orientation.orders_chart_and_odd_K_parity` | PASS |
| `P51.guard.local_scope_forces_global_nulls` | PASS |

Nine of ten declared numerical checks passed:

| numerical check | status |
|---|---|
| `P51.saddles.Phase50_reproduction` | PASS |
| `P51.intersections.lambda0_lifts` | PASS |
| `P51.intersections.fine_forward_both_sources` | PASS |
| `P51.intersections.coarse_and_reverse` | PASS |
| `P51.reflection.independent_phi_pair` | PASS |
| `P51.derivative.full_J_at_0_half_1` | PASS |
| `P51.tangent.lambda_half` | PASS |
| `P51.evaluator.CSE_nonCSE_pairs` | INCONCLUSIVE |
| `P51.endpoint.radius_and_shape` | PASS |
| `P51.guard.classification_and_nulls` | PASS |

The exact symbolic/dtype evaluator check and the numerical paired-evaluator
check answer different questions.  Passing the former does not waive the
frozen tolerance in the latter.

## 8. Interpretation and boundary

### Calculated facts

- The frozen `phi_plus` seed produced accepted nonlinear Gamma–K roots at all
  17 fine-forward, nine coarse-forward, and 17 fine-reverse nodes.
- An independently initialized `phi_minus` solve produced accepted reflected
  roots at all 17 fine nodes.
- All retained Gamma and K tangent matrices had rank nine; the direct and root
  orientations remained `+1` and `-1`, respectively; no sampled transversality
  or parameter-bound gate failed.
- Fine/coarse, forward/reverse, reflection, full-J finite-difference, outer
  path-tangent, radius, launch-shape, action, and first-cap controls all passed.
- All 64 main/endpoint ledgers and all four outer ledgers passed.
- Exact CSE reconstruction and dtype checks passed, while the one frozen
  numerical CSE/non-CSE RHS relative-error check did not.

### Scoped inference

The accepted roots and controls provide evidence for one numerically stable
local `phi_plus` candidate along the sampled Phase-50 diagonal path, with a
consistent independently solved reflected partner.  They materially extend
Phase 50 from tangent-plane transport to actual nonlinear K-flow intersection
solves in `R18`.

The frozen Phase-51 classification remains inconclusive because the evaluator
agreement contract was conjunctive.  It would be incorrect to report the
supported label by ignoring the RHS relative-error gate, weakening its
tolerance after observing the result, or substituting the passing endpoint and
absolute-residual comparisons.  It would also be incorrect to infer
nonexistence: every declared root solve completed, and no independent
contradiction certificate exists.

### Open numerical and physical hypotheses

- Determine, under a newly frozen diagnostic plan, why the CSE and non-CSE
  same-point RHS relative values exceed `5e-10`.  This should distinguish the
  evaluator arithmetic, contraction, normalization, and reference-value
  possibilities without retroactively changing Phase 51.
- Add an independent higher-precision or separately implemented RHS reference,
  then rerun the same paired points and three trajectory reintegrations before
  reconsidering the supported label.
- If evaluator agreement is resolved, repeat the frozen continuation as a new
  phase rather than rewriting this inconclusive result.
- Other sources, roots, charts, directions, straight arms, and cap
  reintersections remain unsearched.  Root, saddle, and upward-component
  exhaustion remain open.
- Stokes data, all relative good ends, a common physical determinant line, and
  a physical original relative cycle remain unspecified.

### Global-null boundary

Phase 51 deliberately leaves the global and physical outputs unchanged:

```text
straight_arm_intersections_searched          = false
cap_reintersections_searched                 = false
continuous_direction_coverage_proved         = false
root_exhaustion_proved                       = false
all_saddles_and_upward_components_complete   = false
non_Stokes_chamber_certified                 = false
all_relative_good_ends_classified            = false
physical_original_cycle_derived              = false
common_determinant_line_constructed           = false
required_independent_contradiction_certificate = null
bounded_chain_signed_sum                     = null
complete_global_signed_intersection_vector   = null
global_n_sigma                               = null
cutoff_limit                                 = null
continuum_limit                              = null
promoted_output                              = null
global_promotion                             = PROHIBITED
Gate 1                                       = OPEN_PARTIAL_PROGRESS
```

## Bottom line

Phase 51 successfully ran the first frozen nonlinear `m=5` Gamma–K
continuation over the Phase-50 action/metric bridge and retained strong local
path, reflection, derivative, mutation, and first-cap evidence.  The run is
valid, but its predeclared supported label is unavailable because exactly one
numerical evaluator-pair check failed.  The correct result is therefore
`PHI_PLUS_M5_GAMMA_K_LOCAL_CONTINUATION_INCONCLUSIVE`—not a contradiction,
not a no-root statement, and not a global or physical conclusion.
