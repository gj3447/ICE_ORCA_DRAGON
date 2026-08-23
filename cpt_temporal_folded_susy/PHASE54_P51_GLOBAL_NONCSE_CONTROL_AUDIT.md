# Phase 54 — static arithmetic attribution of the Phase-51 global non-CSE control

## Outcome

Phase 54 completed a valid six-state, six-stage arithmetic audit.  On the exact
Phase-53 launch states for `phi_plus` and `phi_minus` at
`lambda=0,0.5,1`, it compared a frozen core `2 x 2` evaluator matrix and two
contextual controls with a direct-global 120-decimal reference.  It did not run
a root solve, ODE, trajectory, or continuation.

```text
run_status:       VALID_RUN
exact checks:     7 / 7 PASS
numerical checks: 4 / 8 PASS, 4 / 8 diagnostic NONPASS
classification:  P51_GLOBAL_NONCSE_ACTIVE_GRADIENT_RHS_NONPASS_CONFIRMED_ELEMENT_LOCAL_SCHEDULE_ONLY_SUFFICIENT_ON_PHASE53_SIX_SLOTS
promoted_output:  null
global_promotion: PROHIBITED
Gate 1:           OPEN_PARTIAL_PROGRESS
```

The two global non-CSE core cells failed the frozen `5e-10` selector gate:
`GN_std` passed 4/12 selector records and `GN_long` passed 4/12.  Both
element-local cells passed every selector record: `EL_std` and `EL_long` each
passed 12/12.  Therefore the predeclared label selected the
**element-local-schedule-only-sufficient** branch on these six static states.
Long-namespace arithmetic by itself did not qualify the global non-CSE cell;
the element-local schedule qualified under both standard and long arithmetic.

This is a finite evaluator-arithmetic result in the calculation workbench.  It
does not reclassify Phase 51 or Phase 53.  It is not a root, trajectory,
continuation, global-cycle, physics, or TOE result.

## 1. Corrected authoritative execution and provenance

The authoritative artifact is the corrected `p54b` rerun:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  proxmox-scratch run p54b --timeout 7200 -- \
  ./ice run phase54_p51_global_noncse_control_audit
```

It used scratch path
`/var/tmp/orca/runs/ice_orca_dragon.p54b.20260823T150547Z.EECTMb`, returned
exit `0`, and emitted exactly one `RESULT_JSON=` payload.  The retained logs
are:

| log | bytes | SHA-256 |
|---|---:|---|
| `/var/tmp/phase54-auth-rerun.qmbhSk/stdout.log` | 5,652,571 | `8790ab484d3a16f12a50de8b9981f011473c88846a20b877aace9a218da99150` |
| `/var/tmp/phase54-auth-rerun.qmbhSk/stderr.log` | 1,031 | `85e37999bc7051e126ca1afa79edcd40a0cb697e03d4100766652bf08a300982` |

The stdout file was created at `2026-08-23T15:05:47Z` and completed at
`2026-08-23T15:07:52Z` according to the retained filesystem timestamps.

| artifact | authoritative commit | Git blob OID | SHA-256 | bytes |
|---|---|---|---|---:|
| effective frozen manifest | `c020a13a0c2c7963920ca17365f27fe6544fa0d9` | `e065da49560a74008f1520eee4d73afdc8c89e97` | `4a8f6282a09659e24dc938fa4ae1383c8b5c61f4e2f231b21fcde61637b1fc97` | 28,734 |
| corrected runner | `af8600b31dfbaa46a6da4366a5486e5a2e0d641a` | `f42f1a145337278e26d87d5875bfb6145f1f651d` | `07a6c398370b701a43dfcd35e69ad1440b9978cb09bf31be1609b0d44f163879` | 129,901 |
| corrected result | `d78cf107a9cdca8caf0c5a2933e358e60d3c1a9c` | `1f3162f4f9f5a2e9f15728751ec807806289a5a7` | `daabdcf2a8f74ead3908cfa87a3a8b71befd8db57f61c4c0c47153ea948bfd32` | 5,652,559 |

The result schema is
`ice-phase54-p51-global-noncse-control-audit/v1`.  Its independently
recomputed canonical SHA-256 after removing the self field is
`7b0b98563b254e38626dc9c2cc4cf9f833ed0fa3d11c057675b6af9c94b94fa5`,
exactly equal to `result_payload_sha256_without_self`.  Strict parsing found no
duplicate key or nonfinite value.  The post-evaluation rehash checked 25
consumed artifacts and found all 25 unchanged.

### Superseded first result

Commit `0ed3d7f5c11627f7cee79d23922d9fc56e8496c1` and its result SHA-256
`24bceed9106b90c35266a133ee169e9ed5858287a1b3e2695393610131ca944d`
are superseded and are not the source of any aggregate number in this report.
The first runner parsed retained decimal strings through the ambient mpmath
context and re-rendered maxima, so seven aggregate summary fields were not the
exact decimal strings of their winning ledger records.  The underlying slots,
stage vectors, comparison records, PASS/NONPASS decisions, and scientific
classification did not drift.

Runner correction `af8600b31dfbaa46a6da4366a5486e5a2e0d641a` changed retained
decimal parsing, threshold comparisons, telescope gates, and maximum-ledger
selection to exact `Decimal` arithmetic and preserved the winning record text.
The corrected rerun differed from the superseded payload at exactly 13 expected
leaves: five runner-provenance leaves, seven aggregate maxima, and the derived
self-digest.  No scientific record changed.  Every aggregate shown below is
from corrected result commit `d78cf107` and was rechecked against its retained
ledger with exact decimal comparison.

The observed runtime remained the frozen one:

| component | observed |
|---|---|
| platform | `Linux-7.0.14-5-pve-x86_64-with-glibc2.41` |
| Python | CPython `3.13.5` |
| NumPy / SciPy / SymPy / mpmath | `2.5.2` / `1.18.0` / `1.14.0` / `1.3.0` |
| `longdouble` / `clongdouble` | 16 / 32 bytes |
| long-double mantissa bits excluding the implicit bit / epsilon | 63 / `1.084202172485504434e-19` |
| BLAS and LAPACK | scipy-openblas `0.3.34.0.0`, 64-bit integers, Haswell dynamic architecture |
| required thread variables | `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` |

## 2. Frozen question, states, matrix, and stages

The bounded question was whether the historical Phase-51 global non-CSE active
gradient or completed RHS misses the unchanged direct-global 120-decimal gate
on the six Phase-53 launch states, and whether a global-versus-element-local by
standard-versus-long `2 x 2` audit localizes the finite arithmetic mechanism.

The exact ordered state objects were consumed with these digests:

| slot | state SHA-256 |
|---|---|
| `phi_plus:lambda=0.0` | `49576b8d4d2db1df13a2c7e09e5f5308ac896a7df1fb108d50effe8f530d4fbe` |
| `phi_plus:lambda=0.5` | `873d1f1a4312be0e91b929191028b5289710fdb687fc5d0eaa653117f1c9903c` |
| `phi_plus:lambda=1.0` | `3de5756bed49ea8d51fe1b40bb603564753b8a1c0f33d03bf91385578bf6a20f` |
| `phi_minus:lambda=0.0` | `da33889eb664d4cb7accf323eed6515f6624ae258b1304c0402d3d7661265ae9` |
| `phi_minus:lambda=0.5` | `60beb5350b3cf9010f77f1dfbca2e0ae68db55abd7bf5e51dd3f2061a80026f2` |
| `phi_minus:lambda=1.0` | `45aca3aacb8652f75e6620e17e58500592419bd52570a490307f325c59f556ab` |

The core matrix held one dimension fixed at a time:

| cell | symbolic/arithmetic schedule | callable and accumulation arithmetic |
|---|---|---|
| `GN_std` | actual pinned Phase-51 unreduced global joint gradient-plus-Hessian tuple, `cse=False`; gradient slice only | standard NumPy, then the historical `clongdouble` wrapper |
| `GN_long` | the same unreduced tuple, output order, and no-CSE schedule | Phase-52 `LongNumPyPrinter`/`LONG_MODULES`, then the same wrapper boundary |
| `EL_std` | exact Phase-53 per-element canonical gradient CSE DAGs and fixed left-to-right element order | standard NumPy contributions and `complex128` accumulation, then one complete-gradient `clongdouble` boundary |
| `EL_long` | the same per-element DAGs and fixed order | Phase-53 production `clongdouble` contributions and accumulation |

The contextual controls were the actual Phase-51 global joint-CSE callable and
the Phase-52 long-namespace version of that same joint-CSE DAG.  They were
retained for diagnosis and did not select the classification.

Every evaluator then used the same downstream six-stage order:

1. `m4_raw_gradient` (dimension 7)
2. `m4_lifted_gradient` (dimension 9)
3. `m5_raw_gradient` (dimension 9)
4. `lambda_blended_gradient` (dimension 9)
5. `A_lambda_transpose_contraction` (dimension 9)
6. `outer_minus_conjugation` (dimension 9)

With the pinned basis map, the active algebra was

\[
c=B^{-1}(w_5-a_5),\qquad
w_4=a_4+c_{0:7},
\]

\[
\widetilde g_4=B^{-T}
  (g_4,\kappa_a c_7,\kappa_\phi c_8)^T,\qquad
g_\lambda=(1-\lambda)\widetilde g_4+\lambda g_5,
\]

\[
h_\lambda=A_\lambda^T g_\lambda,\qquad
F_\lambda=-\overline{h_\lambda}.
\]

The transpose is ordinary, not Hermitian, and the outer minus-conjugation is
applied exactly once.

## 3. All seven exact checks passed

| exact check | retained evidence | status |
|---|---|---|
| byte pins, commits, blobs, runtime, self-digests | 6 direct pins; 23 unique pinned artifacts validated | PASS |
| exact Phase-53 state bytes | all 6 ordered state objects and decimal pairs matched | PASS |
| core `2 x 2` bindings and controlled differences | all 4 core cells, DAG identities, generated-source distinctions, and declared contrasts matched | PASS |
| contextual bindings and stage order | both contextual cells and all 6 ordered stages matched | PASS |
| independent reference construction | direct global and symbolic-CSE paths did not consume native outputs | PASS |
| convention binding | ordinary transpose, one outer minus-conjugation, and no Hermitian spelling | PASS |
| static topology and global null guard | no solver/replay call and every global/physics/TOE output retained its required null or false value | PASS |

The Phase-53 production-gradient projection remained byte-identical with
canonical SHA-256
`8359762ba056bd7a300bceba8d4bf7e83e22149f5795c37f5b6ee0a4a212ad4e`
over 4,141 canonical bytes.  Every global and element CSE back-substitution
gate passed.

## 4. Independent reference and all numerical aggregates

The reference built `mp.mpc` state values directly from the frozen decimal-pair
strings.  It did not read `slot.state_w5`, call the inherited Phase-52
reference slot, call NumPy `lambdify`, or consume a native stage vector.  The
unreduced global expressions came from the pinned Phase-41 `m4` and Phase-50
`m5` symbolic models.  Direct `evalf` and a separate canonical symbolic-CSE
back-substitution path were evaluated at 80 and 120 decimal digits.

The symmetric normwise metric was

\[
\epsilon(x,y)=
\frac{\lVert x-y\rVert_2}
{\max(\lVert x\rVert_2,\lVert y\rVert_2,10^{-100})}.
\]

All 108 reference-stability records passed the `1e-40` threshold:

| reference comparison | records | corrected worst relative value | status |
|---|---:|---:|---|
| direct 80 vs direct 120 | 36 | `7.3824037116418428188138189248484299576050659709137e-78` | PASS |
| symbolic CSE vs unreduced direct at 80 digits | 36 | `3.8888258381866368164329540703471185093613273262753e-73` | PASS |
| symbolic CSE vs unreduced direct at 120 digits | 36 | `3.9935803789506339792012606862570854298971862468833e-113` | PASS |

The combined corrected maximum is
`3.8888258381866368164329540703471185093613273262753e-73`.
There were 72 direct reference stage vectors and 72 symbolic-CSE reference
stage vectors.

The eight numerical aggregates were:

| aggregate | active/all-stage records | corrected maximum | status |
|---|---:|---:|---|
| reference 80/120 and symbolic-CSE stability | 108 | `3.8888258381866368164329540703471185093613273262753e-73` | PASS |
| `GN_std` vs direct 120 | 30/36 | `0.0000000067626817995313780292914117169251232490579660640487` | diagnostic NONPASS |
| `GN_long` vs direct 120 | 30/36 | `0.0000000075983301847305741879882302542707909100235106454879` | diagnostic NONPASS |
| `EL_std` vs direct 120 | 30/36 | `0.00000000022425697272607489143457991687527080600161942778023` | PASS |
| `EL_long` vs direct 120 | 30/36 | `0.00000000015673027153465875826880468566090421651939816135183` | PASS |
| Phase-51 global-CSE context vs direct 120 | 30/36 | `0.000000023604573349477552451482612405489801347893366391457` | diagnostic NONPASS |
| Phase-52 long joint-CSE context vs direct 120 | 30/36 | `0.0000000076605933772517315423825682393738102359846302171826` | diagnostic NONPASS |
| core contrasts and six-stage telescopes | 144 contrasts / 180 telescopes | `0.0` maximum relative closure | PASS |

The native accuracy threshold was unchanged at `5e-10`; the telescope closure
threshold was `5e-18`.  A numerical aggregate NONPASS retained every record and
did not by itself authorize a broader repair or historical reclassification.

## 5. Selector maxima and stage localization

Only `lambda_blended_gradient` and `outer_minus_conjugation` selected a core
classification.  Each core evaluator therefore had 6 slots by 2 selector
records:

| evaluator | blended PASS | worst blended slot and relative value | outer-RHS PASS | worst outer-RHS slot and relative value |
|---|---:|---|---:|---|
| `GN_std` | 4/6 | `phi_minus:lambda=1.0`, `0.00000000073575593694862723188501292567623286810544585747905` | 0/6 | `phi_minus:lambda=1.0`, `0.0000000067626817995313780292914117169251232490579660640487` |
| `GN_long` | 4/6 | `phi_plus:lambda=1.0`, `0.0000000007148830544364652132971116926688268445023061834218` | 0/6 | `phi_minus:lambda=1.0`, `0.0000000075983301847305741879882302542707909100235106454879` |
| `EL_std` | 6/6 | `phi_minus:lambda=1.0`, `0.000000000070706392070936688478105085659806352220731892047022` | 6/6 | `phi_minus:lambda=1.0`, `0.00000000022425697272607489143457991687527080600161942778023` |
| `EL_long` | 6/6 | `phi_minus:lambda=1.0`, `0.000000000070465929054706956322859399594055824830775949883795` | 6/6 | `phi_minus:lambda=1.0`, `0.00000000015673027153465875826880468566090421651939816135183` |

Thus the selector booleans were exactly
`GN_std=false`, `GN_long=false`, `EL_std=true`, and `EL_long=true`.

The first-nonpass diagnostics further localized the observed arithmetic path.
The table reports PASS counts over active records; inactive endpoint branches
were still retained but did not enter these counts.

| evaluator | `m4 raw` | `m4 lifted` | `m5 raw` | blend | ordinary `A^T` contraction | outer RHS |
|---|---:|---:|---:|---:|---:|---:|
| `GN_std` | 4/4 | 4/4 | 2/4 | 4/6 | 0/6 | 0/6 |
| `GN_long` | 4/4 | 4/4 | 2/4 | 4/6 | 0/6 | 0/6 |
| `EL_std` | 4/4 | 4/4 | 4/4 | 6/6 | 6/6 | 6/6 |
| `EL_long` | 4/4 | 4/4 | 4/4 | 6/6 | 6/6 | 6/6 |
| Phase-51 global-CSE context | 4/4 | 4/4 | 2/4 | 4/6 | 0/6 | 0/6 |
| Phase-52 long joint-CSE context | 4/4 | 4/4 | 2/4 | 4/6 | 0/6 | 0/6 |

For all four global-schedule variants, the first active NONPASS occurred in
the two `m5_raw_gradient` records at `lambda=1`.  Those two failures persisted
in the blend.  After the ordinary transpose contraction, all six records were
NONPASS; the single outer minus-conjugation preserved the normwise relative
metric.  Both element-local cells passed every active stage.  These facts
localize this six-state discrepancy to the tested arithmetic schedule; they do
not prove behavior along a trajectory or outside the frozen matrix.

## 6. Controlled contrasts, telescopes, dtype, and convention boundaries

All 144 controlled contrast records were retained for the four declared
one-factor comparisons:

- `GN_std -> GN_long`: printer/namespace arithmetic only;
- `EL_std -> EL_long`: callable and accumulator precision only;
- `GN_std -> EL_std`: global no-CSE versus element-local fixed schedule under
  standard arithmetic;
- `GN_long -> EL_long`: the same schedule contrast under long arithmetic.

The five telescope chains used `EL_long` as the middle value and
`direct_global_120` as the reference, once for each of `GN_std`, `GN_long`,
`EL_std`, the Phase-51 global-CSE context, and the Phase-52 long joint-CSE
context.  Six slots by six stages by five chains produced 180 records.  Every
identity

\[
(L-M)+(M-R)-(L-R)=0
\]

closed with maximum relative closure `0.0`, below `5e-18`.  This verifies the
retained vector-difference bookkeeping; it does not turn any diagnostic
NONPASS into a PASS.

The 36 raw-dtype/callable-boundary records covered 6 evaluators by 6 slots:

| evaluator | audited pre-boundary arithmetic | common stage-ready boundary |
|---|---|---|
| `GN_std` | actual no-CSE joint tuple; raw scalars were not all `clongdouble` | historical wrapper produced `complex256` gradient |
| `GN_long` | all raw scalars exactly `clongdouble` | declared wrapper produced `complex256` gradient |
| `EL_std` | standard per-element outputs and fixed `complex128` accumulator | complete sum cast once to `complex256` |
| `EL_long` | all per-element temporaries/outputs and fixed accumulator exactly `clongdouble` | complete sum already `complex256` |
| Phase-51 global-CSE context | 444 `m4` and 544 `m5` temporaries; not all raw values were `clongdouble` | historical wrapper produced `complex256` gradient |
| Phase-52 long joint-CSE context | all 444 `m4` and 544 `m5` temporaries and raw values exactly `clongdouble` | declared wrapper produced `complex256` gradient |

The global joint tuples had fixed output arity 56 for `m4` and 90 for `m5`;
their Hessian slices were retained but not used in this static gradient audit.
The element-local paths used 4 `m4` and 5 `m5` elements in the exact frozen
order.  Numeric Python `id()` values were not serialized; callable relations
were evidenced by roles, source/DAG hashes, and explicit equivalence booleans.

All 36 independent convention recomputation records passed both the ordinary
transpose and single outer minus-conjugation identities.  The common boundary
was one complete-gradient `clongdouble` cast, when needed, followed by the same
Phase-52 native stage arithmetic.

## 7. Record-count, topology, and null-boundary audit

Every predeclared primary count matched exactly:

| category | actual |
|---|---:|
| slots / stages | 6 / 6 |
| core / contextual / total native evaluators | 4 / 2 / 6 |
| native stage vectors | 216 |
| direct reference stage vectors | 72 |
| symbolic-CSE reference stage vectors | 72 |
| native-to-direct-120 comparisons | 216 |
| core controlled contrasts | 144 |
| core selector records | 48 |
| telescope records | 180 |
| root solves / saddle solves | 0 / 0 |
| ODE integrations / trajectory fractions | 0 / 0 |
| continuation or classification replays | 0 |

In addition, the retained subordinate ledgers contained 108 reference
comparisons, 36 raw-dtype/callable records, and 36 convention recomputations.
The Phase-51 integration and saddle methods were not called, the source-context
node was not called, and execution performed static factor reconstruction
only.

No straight-arm or cap reintersection was searched.  Root exhaustion and
completeness of all saddles/upward components remain false.  No physical
original cycle or common determinant line was constructed.  The bounded-chain
sum, complete signed-intersection vector, global `n_sigma`, cutoff limit, and
continuum limit remain `null`.  `physics_claim`, `TOE_claim`, and
`promoted_output` remain `null`; global promotion is `PROHIBITED` and Gate 1
is `OPEN_PARTIAL_PROGRESS`.

The Phase-54 output fields for a Phase-51 reclassification, Phase-53
reclassification, and continuation reclassification are all `null`.
Historical result bytes were not mutated.  Phase 51 therefore remains its
immutable historical result, including the previously recorded
all-temporaries-`clongdouble` `NOT_UPHELD` boundary, and Phase 53 remains its
separate valid but inconclusive full replay.

## 8. Computed facts, interpretation, and open question

### Computed facts

- Exactly six fixed source-by-lambda states were evaluated through exactly six
  static algebra stages with four core and two contextual evaluators.
- The independent 80/120-decimal and symbolic-CSE reference controls passed.
- `GN_std` and `GN_long` failed the frozen selector, while `EL_std` and
  `EL_long` passed all 12 selector records.
- All five-chain telescopes, dtype/callable bindings, convention proofs,
  topology guards, and required null guards passed.

### Bounded interpretation

Within this frozen six-state matrix, element-local decomposition and fixed
summation order are sufficient to meet the existing gradient/RHS accuracy
gate under either standard or long callable arithmetic.  Switching only the
global non-CSE callable to the long namespace is not sufficient.  This
supports the predeclared schedule-only attribution at the tested static
states.  It does not establish that the schedule is a universal or unique
mechanism, and it does not validate transported states, endpoints, roots,
continuation semantics, a physical model, or a TOE.

### Phase 55 — minimal trajectory-validator qualification

The next bounded question is whether the static attribution survives the
smallest trajectory sample that can qualify a validator without replaying the
Phase-53 study:

1. Read, without solving again, the three saved Phase-53
   `phi_plus/fine_forward` roots at `lambda=0,0.5,1`.
2. Phase 53 did not serialize the intermediate states or its recomputed
   saddle/factor/launch objects.  Reconstruct three explicitly labelled
   **P50-saddle-pinned Phase-55 launches** with the P53 `EL_long` Hessian;
   do not call them exact Phase-53 launches.  Require the regenerated
   production endpoints and scaled residuals to reproduce the saved Phase-53
   targets within `2e-7` before interpreting schedule transfer.
3. Regenerate only those three state ODEs with production `EL_long` and the
   coherent `EL_std` candidate, for six ODE attempts total and zero root or
   saddle solves.
4. At the shared `3 x 5` grid of 15 trajectory-fraction slots, retain both
   evaluators' states and apply the same six-stage/direct-120 gate together
   with endpoint and residual controls.
5. Run no root solve, continuation, reflection, 68-root topology replay, or
   Phase-53 reclassification.
6. Qualify the candidate only if the Phase-54 attribution persists over all 15
   states and the candidate passes every declared gate.  Only then may a
   separately frozen Phase 56 attempt a full semantic replay.

Until that qualification is observed, trajectory behavior remains an open
numerical question.  Even a successful Phase 55 would be a validator result,
not a global-cycle, physics, or TOE claim.
