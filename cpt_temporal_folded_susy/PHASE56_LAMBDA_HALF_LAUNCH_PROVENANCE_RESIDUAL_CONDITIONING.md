# Phase 56 — lambda-half launch provenance and residual conditioning

## Outcome

Phase 56 completed the one permitted terminal diagnostic. The fresh Phase-53
saddle algorithm converged at the saved `phi_plus`, `lambda=0.5` root, and the
fresh-center/fresh-launch corner recovered the saved endpoint and scaled
residual target under both frozen solver profiles. The result is a valid,
finite-dimensional calculation:

```text
run_status:       VALID_RUN
exact checks:     8 / 8 PASS
numerical checks: 8 / 8 PASS
classification:  P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET
root calls:       1 permitted fresh saddle solve
solve_ivp calls:  8 permitted EL_long state ODEs
next_phase:       null
Gate 1:           OPEN_PARTIAL_PROGRESS
global promotion: PROHIBITED
physics claim:    null
TOE claim:        null
```

The recovery label is descriptive evidence for this single frozen diagnostic.
It is not authorization for a full replay, Phase 57, a global cycle, a physics
claim, or a TOE result. The Phase-51→56 reconciliation route is `KILL` and the
repository remains in `BOUNDED_PAUSE`.

## 1. Frozen question and conventions

The question was whether the Phase-55 lambda-half residual miss came from the
P50-pinned center, the reconstructed Hessian launch, or their interaction. The
runner consumed one saved Phase-53 `phi_plus` root and target, evaluated one
fresh saddle with the Phase-53 algorithm, and constructed the fixed factorial

```text
P50 center  × P50 launch
P50 center  × fresh launch
fresh center × P50 launch
fresh center × fresh launch
```

Each corner was integrated with production `EL_long` under two predeclared
DOP853 profiles:

| profile | `rtol` | `atol` | `max_step` |
|---|---:|---:|---:|
| primary | `2e-10` | `2e-12` | `0.04` |
| refined diagnostic | `2e-11` | `2e-13` | `0.02` |

Both profiles returned only the five frozen fractions
`0, 0.25, 0.5, 0.75, 1`. The refined profile could not replace the primary
answer. The unchanged target gates were:

- saved-endpoint relative distance at most `2e-7`;
- scaled-residual maximum at most `2e-7`;
- absolute difference from the saved residual scalar at most `2e-12`.

The saddle gates remained gradient at most `2e-8`, Hessian imaginary part at
most `5e-10`, minimum absolute real eigenvalue at least `0.1`, inertia
`(5-,4+,0)`, and distance from the pinned P50 saddle at most `1e-8`.
The element-local gradient used the frozen ordinary-transpose convention, one
outer minus-conjugation, fixed left-to-right `clongdouble` accumulation, and a
single completed `complex128` solver-boundary cast. No threshold or classifier
was changed after observation.

## 2. Execution and provenance

Validation-only was run first:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  ./ice run phase56_lambda_half_launch_provenance_residual_conditioning -- --validate-only
```

It exited `0` with `run_status=VALIDATION_ONLY`, all eight exact checks PASS,
all numerical slots `NOT_EVALUATED`, and exactly zero root and zero ODE calls.

The authoritative calculation then ran under the bounded scratch guard:

```bash
proxmox-scratch run phase56-authoritative --timeout 7200 -- \
  env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  ./ice run phase56_lambda_half_launch_provenance_residual_conditioning
```

It exited `0`. The manifest and runner identities were:

| artifact | effective commit | Git blob | SHA-256 | bytes |
|---|---|---|---|---:|
| input manifest | `24b2d6d7f207941e782dfe9ceae08af6b2d2d24b` | `0024f4e0fcdd0718c7bdc813412b348edd0589a6` | `94c2d0074e0d2a36f3ecb5d99e437ef2915948bbd059154f10098a890f30fb7c` | 28,688 |
| runner | `30ba59ff33e880065e99fa9be8d9c32b7dbd9f95` | `2eadc89a69525130e4542fc478bf52e16068a16e` | `083924f7f9fd0bb3baf8e681e2760cc54ef4a105f5a597b52aa3cdb58c6ac882` | 124,828 |
| canonical result | closeout commit | recorded after commit | `c9163319405ed4ec696076f7516c32fa8af290794a2e1cc4762090812f693d27` | 321,183 |

The result schema is
`ice-phase56-lambda-half-launch-provenance-residual-conditioning/v1`.
Canonical sorted JSON with the self field removed hashes to
`56c567bf60fde04b7d68ab9a5c394faaf08e73e43fe1db36b082ba58e3c010b2`,
exactly matching `result_payload_sha256_without_self`. All 29 recursive input
pins plus the manifest and runner were rehashed after evaluation and remained
unchanged.

The observed runtime was Linux `7.0.14-5-pve`, CPython `3.13.5`, NumPy
`2.5.2`, SciPy `1.18.0`, SymPy `1.14.0`, and mpmath `1.3.0`.
`longdouble`/`clongdouble` item sizes were 16/32 bytes with 63 explicit
mantissa bits, and all four required thread variables were `1`.

## 3. Exact checks and execution topology

All eight exact checks passed:

| check | retained fact |
|---|---|
| recursive input and runner binding | 29 recursive pins, strict JSON/self-digests, commit/blob identities, manifest ancestry, clean runner commit, and start/end hashes matched |
| single target | exactly one `phi_plus`, lambda-half root, P50 saddle, saved endpoint, saved residual, and Phase-55 baseline subtree were selected |
| solve topology | one fresh saddle solve was permitted; every other root, continuation, replay, tangent, event, finite-difference, reflection, action, and first-cap counter stayed zero |
| factorial launch topology | two centers, two launches, and four ordered corners matched the frozen construction |
| ODE topology | eight attempts and forty fraction slots were retained without omission |
| conventions | fixed `EL_long` sums, ordinary transpose, one outer conjugation, and one solver cast remained bound |
| residual identity | full 18-component interleaved residual vectors retained physical `T` at coordinate 8 / interleaved real index 16 |
| scope guard | historical classifications and every global, physics, and TOE null remained immutable |

The observed call ledger was:

```text
allowed fresh saddle root: 1
runner solve_ivp:           8
EL_long callbacks:          37,144
EL_std callbacks:           0
all forbidden root/ODE:     0
continuation/replay:         0
tangent/event/reflection:   0
action/first-cap:            0
```

All four primary attempts completed with `nfev=3101`; all four refined
attempts completed with `nfev=6185`. Every callback count equaled `nfev`, all
five requested samples were returned, and every sampled `||xi||` stayed below
the strict bound `40`.

## 4. Numerical result

The fresh saddle converged in four function evaluations:

| quantity | observed | frozen gate | status |
|---|---:|---:|---|
| distance from P50 saddle | `5.245664923524781e-13` | `<=1e-8` | PASS |
| gradient maximum | `6.895659173875024e-12` | `<=2e-8` | PASS |
| minimum absolute Hessian eigenvalue | `4.220358798890757` | `>=0.1` | PASS |
| Hessian inertia | `(5-,4+,0)` | `(5-,4+,0)` | PASS |

No exact historical Phase-53 saddle-byte identity is claimed. The static
Newton prediction solved `H_real delta=-g_real` with residual
`5.169878828456423e-25`; its predicted displacement and the actual fresh
displacement differed by relative `2.620445627091483e-4`. This comparison is
descriptive and was not used to retune a gate.

The target-gate pattern was identical under both solver profiles:

| center / launch | endpoint | residual absolute | saved-scalar difference | overall |
|---|---|---|---|---|
| P50 / P50 | PASS | NONPASS | NONPASS | NONPASS |
| P50 / fresh | PASS | NONPASS | NONPASS | NONPASS |
| fresh / P50 | PASS | PASS | PASS | PASS |
| fresh / fresh | PASS | PASS | PASS | PASS |

Representative primary-profile values show the separation:

| center / launch | endpoint relative | residual maximum | saved-scalar difference |
|---|---:|---:|---:|
| P50 / P50 | `2.633122460998128e-8` | `2.675225930464415e-7` | `2.672581705546800e-7` |
| P50 / fresh | `2.633139745503500e-8` | `2.675242977145942e-7` | `2.672598752228327e-7` |
| fresh / P50 | `1.744682340806467e-13` | `2.624466517125208e-10` | `1.975840048989014e-12` |
| fresh / fresh | `4.571942323393511e-17` | `2.641451343369080e-10` | `2.773574246017642e-13` |

The refined fresh/fresh corner also passed, with endpoint relative
`3.646286862238947e-14`, residual maximum
`2.645138076827282e-10`, and saved-scalar difference
`9.131592121838167e-14`. Cross-profile endpoint differences were at most
`3.820939246900161e-14` relative across the four corners, and cross-profile
residual differences were at most `3.686733458201459e-13` absolute. All four
gate vectors were therefore stable.

The factorial ledger associates the observed target recovery with replacing
the center: both fresh-center corners pass, while neither P50-center corner
does. The primary residual-effect maxima were approximately
`2.672601463947290e-7` for center, `1.704668152652186e-12` for launch, and
`2.041902130921287e-14` for interaction. The dominant center-effect component
was real `T`. These are finite factorial effects, not a general causal or
dominance theorem; the result explicitly records
`causal_or_dominance_label_assigned=false`.

The eight numerical aggregate checks all passed: fresh saddle/launch validity,
Newton identity, exact Phase-55 primary baseline reproduction, eight-ODE
completion, complete gate ledgers, profile stability, two-profile fresh/fresh
recovery, and residual/factorial arithmetic closure.
These are contract aggregates that include the expected negative-control gate
pattern; they do not mean that every corner passed its target. All four
P50-center profile/corner records remain `NONPASS` exactly as tabulated above.

## 5. Complex-value maximum warning

Both authoritative runs emitted a `ComplexWarning` at runner line 1400. The
generic helper casts a complex array to `longdouble` before applying `abs`, so
it can discard an imaginary component. The affected uses are two endpoint
factorial-closure maxima and six endpoint-effect maxima.

A post-run audit recomputed all six effect maxima with the complex modulus from
the serialized complex vectors. Every 24-digit reported maximum was unchanged;
the largest imaginary components were between roughly `4.6e-34` and `2.5e-27`
while the selected real maxima were between roughly `7.2e-14` and `1.9e-7`.
Both complex endpoint reconstruction closures were exactly zero in real and
imaginary parts. Consequently the observed PASS statuses, classification, and
payload self-digest are unaffected.

The helper is still a real generic implementation defect: a different
purely-imaginary closure could be understated. It is retained as a known
hardening item rather than reopening the now-consumed Phase-56 runner, because
changing that pinned runner would require a new binding and two new heavy runs
on the killed route.

The read-only audit is reproducible from the result without importing or
executing the runner:

```bash
./.venv/bin/python - <<'PY'
import json
from pathlib import Path
import numpy as np

p = Path("cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_RESULT.json")
r = json.loads(p.read_text(encoding="utf-8"))

def decode(record):
    values = [np.clongdouble(np.longdouble(a)) + 1j*np.clongdouble(np.longdouble(b))
              for a, b in record["clongdouble_decimal_pairs"]]
    return np.asarray(values, dtype=np.clongdouble).reshape(record["shape"])

def text(value):
    return np.format_float_scientific(np.longdouble(value), precision=24,
                                      unique=False, trim="k")

effects = r["ledgers"]["factorial_effects"]
effect_ok = all(
    text(np.max(np.abs(decode(x["endpoint_effect_vector"])),
                initial=np.longdouble(0))) == x["endpoint_effect_max_abs_decimal"]
    for x in effects
)
endpoints = {(x["profile"], x["corner"]): decode(x["physical_state_z"])
             for x in r["ledgers"]["endpoints"]}
closure_ok = []
for profile in ("primary", "refined_diagnostic"):
    z00 = endpoints[(profile, "P50_center__P50_launch")]
    z01 = endpoints[(profile, "P50_center__fresh_launch")]
    z10 = endpoints[(profile, "fresh_center__P50_launch")]
    z11 = endpoints[(profile, "fresh_center__fresh_launch")]
    closure = (z11-z00) - ((z10-z00) + (z01-z00) + (z11-z10-z01+z00))
    observed = text(np.max(np.abs(closure), initial=np.longdouble(0)))
    recorded = {x["endpoint_reconstruction_closure_max_abs_decimal"]
                for x in effects if x["profile"] == profile}
    closure_ok.append(recorded == {observed})
print({"all_effect_moduli_same": effect_ok,
       "all_endpoint_closures_same": all(closure_ok)})
PY
```

Observed output was
`{'all_effect_moduli_same': True, 'all_endpoint_closures_same': True}`.

## 6. Independent reproduction

The first reproduction wrapper used an overlong scratch label and failed
before Python execution because the derived `tsx` Unix socket path exceeded
the platform limit. No numerical work occurred in that attempt, and the failed
scratch was preserved by policy.

The actual independent reproduction used a shorter label:

```bash
proxmox-scratch run p56-repro --timeout 7200 -- \
  env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  ./ice run phase56_lambda_half_launch_provenance_residual_conditioning
```

It exited `0`. The authoritative and reproduction stdout records were each
321,195 bytes including the `RESULT_JSON=` framing and terminal line ending,
with identical SHA-256
`242653355f6184158f98e51631ad5cefa5936b6f78511cf76cfa5e7a751c7eb6`.
Their byte comparison exited `0`; both carried the same classification and
self-digest. The canonical result is the framing-free 321,183-byte JSON.

## 7. Computed facts, interpretation, and boundary

Computed facts:

- one fresh Phase-53-algorithm saddle and two Hessian-derived launch choices
  were evaluated at the single saved lambda-half root;
- the P50/P50 corner reproduced the complete pinned Phase-55 primary baseline;
- all eight state ODEs completed, and the primary/refined gate vectors agreed;
- both fresh-center corners recovered the saved target under both profiles;
- center, launch, interaction, residual identity, and `T`-conditioning records
  were retained without a post-observation causal label;
- the authoritative run and independent reproduction were byte-identical.

Scoped interpretation:

- within this frozen diagnostic, the Phase-55 miss tracks the P50-pinned center
  reconstruction rather than the choice between the two tested launches;
- rerunning the Phase-53 saddle algorithm recovers the saved lambda-half target
  on both tested solver profiles.

Not established:

- exact historical Phase-53 saddle or launch bytes;
- a full continuation replay or reclassification of Phase 51, 53, or 55;
- root or upward-component exhaustion, straight-arm/cap searches, a physical
  original cycle, determinant line, signed global vector, cutoff/continuum
  limit, physics claim, or TOE claim.

Operational closeout:

- `qualified_later_full_replay_launch_policy_candidate` is a descriptive result
  value, not execution authorization;
- `full_semantic_replay_performed=false`;
- `continuation_route=KILL`, `full_replay_authorized=false`, and
  `phase57_authorized=false`;
- `next_phase=null` at both the result and containment layers;
- the one-shot Phase-56 execution permission is consumed. Only the frozen
  Phase-11→50 historical allowlist remains executable during the bounded pause.
