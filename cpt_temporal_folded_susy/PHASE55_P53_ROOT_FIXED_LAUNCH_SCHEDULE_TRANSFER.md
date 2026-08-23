# Phase 55 — P50-saddle-pinned launch and trajectory schedule-transfer audit

## Outcome

Phase 55 completed a valid, bounded three-root calculation, but it did **not**
qualify a Phase-56 full replay.  The production `EL_long` and coherent
`EL_std` state-RHS paths agree very closely along all fifteen sampled trajectory
fractions, and the Phase-54 aggregate schedule matrix is reproduced.  The
earlier prerequisite fails instead: the P50-saddle-pinned reconstruction at
`lambda=0.5` has a scaled endpoint residual above the unchanged `2e-7` gate.

```text
run_status:       VALID_RUN
exact checks:     8 / 8 PASS
numerical checks: 6 / 8 PASS, 2 / 8 NONPASS
                  (decisive reconstruction prerequisite + retained downstream diagnostic)
classification:  P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS
Phase56 candidate: null
global promotion: PROHIBITED
Gate 1:           OPEN_PARTIAL_PROGRESS
```

This is a calculation-workbench result on three saved `phi_plus` roots and
three explicitly reconstructed launches.  Phase 53 did not serialize its
authoritative saddle, factor, launch, or intermediate trajectory states, so
the Phase-55 launches are not called exact Phase-53 launches.  The result does
not reclassify Phase 51 or Phase 53 and is not a root census, global cycle,
physics claim, or TOE result.

## 1. Frozen question and conventions

The bounded question was whether the Phase-54 element-local schedule
attribution transfers from six static launch states to the five fixed
fractions of three reconstructed paths, and whether `EL_std` can be qualified
as a later state-RHS candidate relative to production `EL_long`.

The calculation consumed the saved Phase-53 `phi_plus/fine_forward` roots at
`lambda=0,0.5,1`, the corresponding pinned Phase-50 saddles, the Phase-51
geometry and root parameters, the Phase-53 coherent element-local Hessian and
`EL_long` gradient schedule, and the Phase-54 four-cell evaluator definitions.
The byte-pinned internal source chain is the primary source for this replay;
no formula or numerical target was imported from an untracked pilot.

For a physical state `z`, the common six-stage gradient/RHS construction was

\[
c=B^{-1}(w_5-a_5),\qquad w_4=a_4+c_{0:7},
\]

\[
\widetilde g_4=B^{-T}(g_4,\kappa_a c_7,\kappa_\phi c_8)^T,
\quad g_\lambda=(1-\lambda)\widetilde g_4+\lambda g_5,
\]

\[
h_\lambda=A_\lambda^T g_\lambda,
\qquad F_\lambda=-\overline{h_\lambda}.
\]

The transpose is ordinary, not Hermitian, and the outer minus-conjugation is
applied once.  Element contributions are summed in their frozen left-to-right
order.  `EL_long` retains `clongdouble` contributions and accumulation;
`EL_std` uses the same element-local DAGs with `complex128` accumulation and
then the same complete-gradient boundary.  Each state ODE crosses one
`complex128` solver boundary.  The solver is DOP853 with `rtol=2e-10`,
`atol=2e-12`, `max_step=0.04`, and five returned fractions
`0,0.25,0.5,0.75,1`.

The physical-state transfer metric was

\[
\epsilon_z(x,y)=\frac{\lVert x-y\rVert_2}
{\max(\lVert y\rVert_2,10^{-30})},
\]

and the independent native/reference metric was the symmetric variant with
denominator `max(||x||,||y||,1e-100)`.  At an endpoint, the scaled residual was

\[
r_b=\operatorname{interleave}\!\left(
\frac{\Gamma_{\rm cap}(p_{0:9})-z_{b,\rm endpoint}}
{\mathrm{scales}_5}\right),
\qquad R_b=\max |r_b|.
\]

The material thresholds remained `1e-40` for the 80/120-decimal reference,
`5e-10` for active gradient/RHS stages and same-point backend comparisons,
`5e-18` for telescope closure, and `2e-7` for saved-endpoint,
trajectory/endpoint, and scaled-residual transfer.  Returned sample
`||xi||` had to stay strictly below `40`.  Every retained decimal gate and
reported maximum was selected with exact `Decimal` comparison.  No threshold
was relaxed after observation.

## 2. Authoritative execution and provenance

The authoritative runner was invoked inside the guarded scratch runtime as:

```bash
proxmox-scratch run phase55-authoritative -- bash -lc '
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /home/lagyeongjun/CD/ICE_ORCA_DRAGON/.venv/bin/python \
  /home/lagyeongjun/CD/ICE_ORCA_DRAGON/cpt_temporal_folded_susy/phase55_p53_root_fixed_launch_schedule_transfer.py
'
```

The Python runner itself exited `0` and emitted one `RESULT_JSON=` payload.
The wrapper's first post-parser then referenced a superseded summary key and
exited `1` after the calculation had finished.  This operational parser error
did not alter the payload.  The preserved scratch stdout was strictly parsed,
checked for duplicate keys and nonfinite values, rehashed, and captured as the
canonical result.  The parser mismatch is not a scientific NONPASS and is kept
separate from the two recorded numerical NONPASS checks.  Of those two, the
reconstruction aggregate is the decisive frozen prerequisite; the downstream
candidate-residual aggregate is retained diagnostically after that precedence
branch has already been selected.

| artifact | commit | Git blob | SHA-256 | bytes |
|---|---|---|---|---:|
| effective manifest | `10bb1ca9f735e6abc885206c049506da49c3a96e` | `bb7b9c2409528918cf8a91d7ac3265d817cbfc2c` | `7d5730252356c886671c1d9877bcbb44e49f7e3830d5307d25f6ed951418685d` | 54,905 |
| runner | `ea7df7c04a9774ecb300f4e54684c54102fb9995` | `3a332a80e04d772bb4b0bdf235ac6fc2b6dfb1dc` | `880fe68ab5a068f02045d116ab10835e72e3cc5a59793498a4b2ef245bf23dcf` | 195,098 |
| raw result | `d09b1f3c90f1a276d704c8454fe79e538baa3e57` | `b7a3574fa7fac4b98017e6bcf8571aaccb5ad8ce` | `c67ed1d3a078bbde8cd7693aa7fe8a5f377c41d6f33a64476913bca2b4748738` | 5,464,568 |

The schema is
`ice-phase55-p53-root-fixed-launch-schedule-transfer/v1`.  Removing the self
field and hashing canonical sorted JSON gives
`7409b408e9d86306c2e75fe2a175f13b36e55d978af6b3ad92c1f998995b9592`,
exactly equal to `result_payload_sha256_without_self`.  All 28 consumed paths
were rehashed after evaluation and were unchanged.

The observed platform was Linux `7.0.14-5-pve`, CPython `3.13.5`, NumPy
`2.5.2`, SciPy `1.18.0`, SymPy `1.14.0`, and mpmath `1.3.0`.
`longdouble`/`clongdouble` item sizes were 16/32 bytes with 63 explicit
mantissa bits and epsilon `1.084202172485504434e-19`; all four required thread
variables were `1`.

## 3. Exact checks and execution topology

All eight exact checks passed:

| check | retained fact |
|---|---|
| recursive pins and corrected Phase 54 | 26 consumed paths plus manifest/runner commits, blobs, sizes, self-digests, and classification matched |
| saved roots and targets | all three root, P50-saddle, intersection, endpoint, and residual-scalar digests matched |
| zero-solve launch topology | three fixed saddles and launches passed; root/saddle solves remained zero; initial backend buffers were byte-identical |
| evaluator binding | the full Phase-53 element-local projection and Phase-54 four-core bindings matched; science source was `phi_plus` only |
| preenumerated ODE/audit topology | six attempt slots, five fractions each, and every evaluated/placeholder key matched the frozen sequence |
| conventions and gates | fixed sums, exact Decimal gates, ordinary transpose, one outer conjugation, and one solver cast matched |
| independent reference | direct global 80/120-decimal evaluation was unreduced and did not consume native outputs |
| scope and null guard | historical bytes were immutable, prohibited calls stayed zero, required fields stayed null or false, and global promotion stayed `PROHIBITED` |

Exactly six `solve_ivp` calls ran: `EL_long` then `EL_std` for each lambda.
All completed successfully and returned five requested samples.

| lambda | saved flow time | nfev per backend | max returned `||xi||`, long / std | status |
|---:|---:|---:|---:|---|
| 0 | 10.269555215197657 | 3101 / 3101 | 1.303361199087 / 1.303361198946 | PASS |
| 0.5 | 10.268898121002966 | 3101 / 3101 | 1.294281284011 / 1.294281283869 | PASS |
| 1 | 10.23398118420796 | 3089 / 3089 | 1.281290669786 / 1.281290669651 | PASS |

The audit retained 30 sampled states, 540 native stage vectors, 450 active
native comparisons, 360 direct-reference stage vectors, 540 native-to-direct
comparisons, 180 selectors, 450 controlled contrasts, 360 telescopes, and 120
raw reference gradients.  It also retained 15 paired fractions, three initial
identities, three endpoint pairs, six residuals, three candidate/production
residual pairs, and three saved-endpoint comparisons.  Every slot was
evaluated; the placeholder count was zero.  The canonical key-sequence digest
was `da2807b73b226bdf6d0f04d807080dd55967d43c1916aadc53b359ab8ed9363a`.

## 4. Numerical result

The eight numerical aggregate statuses, in frozen order, were:

| check | status |
|---|---|
| 30-state direct 80/120 stability | PASS |
| `EL_long` saved Phase-53 endpoints and residuals | NONPASS |
| production-state Phase-54 schedule matrix | PASS |
| candidate-state `EL_std` and `EL_long` vs direct 120 | PASS |
| same-point `EL_std`/`EL_long` blend and completed RHS | PASS |
| all paired trajectory fractions and endpoints | PASS |
| candidate absolute and candidate/production residual transfer | NONPASS |
| telescopes, finiteness, solver completion, and sample `||xi||` | PASS |

All three reconstructed fixed saddles passed fresh Phase-53 `EL_long`
gradient, Hessian-gap, imaginary-part, and `(5-,4+,0)` inertia checks.

| lambda | gradient max | minimum absolute Hessian eigenvalue | status |
|---:|---:|---:|---|
| 0 | `1.6053260152916301e-11` | `4.194252303687439` | PASS |
| 0.5 | `6.7930962059908201e-10` | `4.220358798871558` | PASS |
| 1 | `7.5546166544704363e-12` | `4.251015820235482` | PASS |

The `EL_long` endpoints reproduce the saved Phase-53 endpoint coordinates
well inside `2e-7`, and `EL_std` and `EL_long` agree still more closely:

| lambda | `EL_long` vs saved Phase 53 | `EL_std` vs `EL_long` endpoint |
|---:|---:|---:|
| 0 | `1.8414284944451966e-9` | `7.9842811981010961e-12` |
| 0.5 | `2.6331224609981278e-8` | `7.9456909267138991e-12` |
| 1 | `8.2750675435735933e-11` | `7.4508733962679968e-12` |

Every one of the fifteen fraction comparisons passed.  The maximum paired
trajectory relative difference was `7.9842811981010961e-12`, far below
`2e-7`.  The complete production selector matrix exactly reproduced Phase 54:

```text
GN_std=false, GN_long=false, EL_std=true, EL_long=true
```

The decisive prerequisite failure is in the scaled endpoint residual:

| lambda | `EL_long` residual max | saved Phase-53 scalar | absolute scalar difference | status |
|---:|---:|---:|---:|---|
| 0 | `1.8981543162662921e-8` | `3.145540391278385e-13` | `1.8981228608623793e-8` | PASS |
| 0.5 | `2.6752259304644153e-7` | `2.644224917615098e-10` | `2.6725817055468002e-7` | NONPASS |
| 1 | `8.7059732439038438e-10` | `9.068878770466091e-14` | `8.7050663560267972e-10` | PASS |

At `lambda=0.5`, `EL_std` independently gives
`2.6744097214592699e-7`, so this is not an `EL_long`/`EL_std` trajectory
separation.  Their full residual vectors differ by only
`8.1620900514539688e-11`, and the corresponding differences at lambda 0 and 1
are `8.2156028012392469e-11` and `7.6459552974686884e-11`.  Thus the candidate
tracks the production residual, but the production reconstruction itself does
not reproduce the saved Phase-53 residual target at lambda 0.5.

The classification precedence therefore stops at
`P55_P50_SADDLE_PINNED_EL_LONG_TRAJECTORY_RECONSTRUCTION_NONPASS`.  Later
schedule-transfer predicates are retained diagnostically, but cannot qualify
`EL_std` or open a Phase-56 full replay.

## 5. Independent reproduction

A second guarded execution used the same frozen runner and thread environment:

```bash
proxmox-scratch run phase55-authoritative-repro -- bash -lc '
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /home/lagyeongjun/CD/ICE_ORCA_DRAGON/.venv/bin/python \
  /home/lagyeongjun/CD/ICE_ORCA_DRAGON/cpt_temporal_folded_susy/phase55_p53_root_fixed_launch_schedule_transfer.py
'
```

It exited `0` and produced 5,464,568 bytes exactly equal to the committed raw
result.  Its outer SHA-256 was again
`c67ed1d3a078bbde8cd7693aa7fe8a5f377c41d6f33a64476913bca2b4748738`
and its self-digest was again
`7409b408e9d86306c2e75fe2a175f13b36e55d978af6b3ad92c1f998995b9592`.

## 6. What is computed, interpreted, and still open

Computed facts:

- all three fixed saddles and zero-solve launches satisfy the frozen local
  checks;
- both ODE backends complete from identical initial solver bytes;
- their fifteen paired physical states, endpoints, and candidate/production
  residual vectors agree far inside the transfer thresholds;
- the complete production sample reproduces the Phase-54 aggregate schedule
  matrix;
- the reconstructed lambda-0.5 endpoint residual misses the frozen Phase-53
  reconstruction threshold.

Interpretation:

- element-local standard and long schedules behave coherently on these three
  reconstructed paths;
- the blocker lies before candidate qualification, in reproducing the saved
  Phase-53 residual from a P50-saddle-pinned launch that Phase 53 itself did
  not serialize;
- endpoint norm agreement alone is insufficient because the scaled cap
  residual is more sensitive in the lambda-0.5 slot.

Open hypothesis, not yet established:

- the mismatch may come from unavailable Phase-53 launch/saddle bytes, from
  the conditioning of the scaled residual relative to endpoint coordinates,
  or from another frozen reconstruction choice.  Phase 55 does not select one
  cause.

The next bounded calculation, labelled Phase 56 diagnostic only, should
therefore diagnose lambda 0.5 by decomposing endpoint-coordinate differences
through the fixed scaling and cap
residual map and by testing only predeclared launch/provenance perturbations.
It must preserve the `2e-7` gate and historical artifacts.  Phase 56 does not
itself authorize a full semantic replay.  A full replay, straight-arm search,
cap reintersection search, global intersection sum, cutoff/continuum limit,
physics claim, or TOE promotion remains unauthorized by this result.
