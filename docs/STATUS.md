# ICE_ORCA_DRAGON status

> Current engineering/reproduction state followed by a bounded historical scientific ledger. This file
> reports evidence; it does not authorize KG or canon mutation.

## Current state — 2026-08-16

| Component | State |
|---|---|
| Runnable catalog | 46 entries; `./ice list --json` is authoritative |
| Control plane | strict TypeScript, Effect 3, Node 24 contract, exact `package-lock.json` |
| Numerical runtime | Python 3.13 contract with exact `uv.lock` |
| Mapped reproduction cases | 14 |
| Reproduction ledger | 12 `REPRO`, 1 `NONPORTABLE_FAIL`, 1 `SUPERSEDED` |
| Local engineering gate | `npm run check` |
| Environment gate | `./ice doctor` |
| Scientific workflow | tiered T0/T1/T2; full loop only for T2 |

Historical source/result inventories contain more files than the live CLI. Do not use an old “47” or
“60+” count as the runnable catalog.

## Reproduction status

`./ice repro` works in an Effect-scoped temporary copy and compares fresh mapped outputs with the
committed `HEAD` baseline. It is intentionally non-destructive and intentionally exits nonzero for the
current ledger.

- Twelve mappings satisfy their field-aware semantic comparators.
- `queue_03_threshold_sensitivity_scan` is `NONPORTABLE_FAIL`: its legacy entrywise commutator maximum
  changes under an arbitrary orthogonal basis of the SciPy null space. Observed categorical outcomes can
  change, so a wider tolerance is not a valid fix.
- `queue_06_cooperative_vacuum` is `SUPERSEDED`: the committed repaired result comes from a different
  later computation and is not reproducible by pretending the historical named script produced it.
- Queue04 permits `atol=1e-6` only for the verified circular optimizer-coordinate paths; structure,
  categories, and other fields keep their tighter comparator.

See [`../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](../QUEUE03_PORTABILITY_AUDIT_2026-08-14.md)
and [`../REPRODUCIBILITY_2026-06-08.md`](../REPRODUCIBILITY_2026-06-08.md).

## Current feedback contract

Assign the highest applicable tier before execution.

| Tier | Scope | Persistence |
|---|---|---|
| T0 | non-claim docs/tooling/harness/lock engineering | requested artifact and relevant checks |
| T1 | frozen-input reproduction | reproducibility receipt; no confidence change |
| T2 | work that can materially affect a scientific claim | full evidence report; material/reusable evidence may be proposed as `PENDING` |

T0/T1 escalates to T2 when the outcome materially affects a claim. T2 does not downgrade after an
unfavorable or null result is seen.

### T2 classification axes

T2 does not force a single four-way verdict. Record independent axes:

| Axis | Values |
|---|---|
| target | explicit claim plus algebra/physics fiber |
| claim relation | `SUPPORTS`, `CONTRADICTS`, `INCONCLUSIVE` |
| novelty | `REPRODUCTION`, `DISCOVERY_CANDIDATE` |
| fitting risk | `NULL_PASS`, `NUMEROLOGY_HOLD`, `NOT_APPLICABLE`, `NOT_ASSESSED` |
| registration | committed preregistration or explicit post-hoc/unknown status |

`CONTRADICTS` describes evidence before ratification. `REFUTED` is reserved for a validated
preregistered falsifier plus authorized ratification.

### Optional gates

- Null/multiplicity: required when a meaningful statistical search or fit exists; `NOT_APPLICABLE` is
  valid for exact/deductive work and `NOT_ASSESSED` when no valid null is available.
- Numerical Bayes: only with explicit `H` and `E`, frozen prior, both likelihoods, and selection/
  dependence treatment. A rerun of the same data is not a new independent `E`.
- Lakatos: only at a declared programme/fiber checkpoint with baseline and longitudinal window.
  `PROGRESSIVE` needs novel excess empirical content plus independent corroboration;
  `DEGENERATING` needs a longitudinal sequence of ad-hoc belt changes without corroborated novelty.
  Otherwise use `UNDETERMINED` or the canonical `STAGNANT`. Finding counts are not votes.

### Persistence and ratification

An ordinary T2 execution may create provenance-rich `PENDING` evidence or a proposed change. It does not
directly change confidence/status, mark a Contract refuted, create a canonical Span/Possibility, or
supersede an existing record. Ratification requires an explicit authorized ratifier and the ID of the
pending evidence being considered.

A parent report may close after classifying its evidence and recording one bounded follow-up. Discovery
does not trigger automatic `/apt-sp` recursion; any child is separately scoped and tiered.

Source: [`../.claude/skills/science-feedback-loop.md`](../.claude/skills/science-feedback-loop.md).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 12

Phase 12 is a `POST_HOC` exact/deductive cycle, not a confirmation or canon change.

- The Phase 11 homogeneous-quadratic strong class, and the weak dilation with an unrestricted lapse
  rescaling, are removable from the open-interval bulk by a time-dependent canonical frame change under
  the stated invariance/completeness assumptions. Endpoint twist, polarization, and (for momentum
  shears) a boundary generating function remain.
- An engineered, regular 4D rigid \(N=1\) Wess–Zumino spatial BPS wall gives scalar and chiralino
  components the same kinematic internal-flavor frame. Its scalar differential expressions have exact
  formal factorization; the executable does not derive the full Weyl operator or a self-adjoint domain.
  A boson-only collar fails the matched endpoint identity.
- This does **not** derive a local-supergravity seam, a cosmological observable, boson–fermion branch
  exchange, a physical endpoint detector, or “pre-Big-Bang time = SUSY.” The partial matter-coupled
  SUGRA candidate remains `INCONCLUSIVE`.
- The executable reports 38 exact positive checks and rejects 9 semantic mutants. It has no mapped
  legacy result JSON, so `./ice run phase12_boundary_twist_interface` is the applicable execution gate;
  it is not an additional case in the 14-entry reproduction ledger.

See
[`../cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md`](../cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md)
and
[`../cpt_temporal_folded_susy/PHASE12_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE12_RESEARCH_CONTRACT.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 13A

Phase 13A preregistered a direct Lorentzian local-SUGRA branch-\(Q\) kill test before its executable
was written. An independent adversarial audit found that the first run's overall `CONTRADICTS` wording
exceeded the implemented physical mapping. The original contract remains unchanged; a separate
`POST_HOC_CORRECTED` erratum records the corrected scope.

- The Moniz first-order constraint's \(\partial_a,\partial_\phi\) principal terms preserve a chosen
  formal \(e^{\pm i\lambda W}\) phase label. The implemented direct-sum labels are not relational
  expanding/contracting spectral projectors, so this control is `INCONCLUSIVE` for the physics claim.
- In a finite positive-Hilbert-space class, if \(C=\{Q,Q^\dagger\}\) and physical states are defined by
  \(\ker C\), then \(Q\) and \(Q^\dagger\) vanish on that kernel. The executable verifies a nontrivial
  off-shell sheet/parity-flipping witness whose kernel exchange map is exactly zero. This scoped shortcut
  is `CONTRADICTS`, but it is not a mapped truncation of the 4D SUGRA physical Hilbert space.
- A generic odd CAR constraint can close exactly on an even symbol while every formal-sheet cross block
  vanishes. Local constraint closure alone therefore does not imply branch exchange.
- No audited Phase 13A source model supplies a gauge-independent relational branch projector, common
  physical domain/inner product, and a nonzero fermionic charge distinct from the local gauge constraint.
  The literal “opposite time branch = superpartner” claim remains `INCONCLUSIVE/UNCONSTRUCTED`, not
  supported and not universally refuted.
- The executable reports 21 exact positive checks and rejects 8 semantic mutants. Phase 13B spatial-wall
  scattering is gated out of the core sequence; if pursued, it is a separately registered auxiliary
  interface project with zero evidence weight for the literal cosmological claim.

See
[`../cpt_temporal_folded_susy/PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md`](../cpt_temporal_folded_susy/PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md),
[`../cpt_temporal_folded_susy/PHASE13A_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE13A_RESEARCH_CONTRACT.json),
and
[`../cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json`](../cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 14A

Phase 14A preregistered a compact \(T^3\), flat-FLRW, neutral-chiral-clock charge-first template before
freezing its source packet/ledger and executable. The committed first run and two independent replays
all returned exit 0 with **24 exact checks, 7 executable mutants rejected, and 6 scope guards**.

- The exact bosonic reduction gives
  \(C_B=-p_X^2+p_T^2+p_Y^2\), \(\{T,C_B\}=2p_T\), and
  \(\alpha=(p_T^2+p_Y^2)/(2V_0^2a^6)>0\) on both \(p_T\ne0\) orientations.
- On the frozen Kallosh bosonic-flat-FLRW linear-fermion domain,
  \(\delta\upsilon/\delta\epsilon=-(\alpha/2)I_4\) has rank 4 and kernel dimension 0. This excludes a
  nonzero goldstino-unitary-gauge residual parameter; it does not remove local gauge invariance or every
  reduced/dressed charge.
- A smooth compact \(T^3\) has no actual spatial boundary or asymptotic end, so the
  Regge–Teitelboim spatial-boundary channel is `NOT_APPLICABLE_IN_THIS_ROUTE`. No temporal endpoint or
  earlier collar is substituted for that surface.
- The bulk calculation is only a formal constraint-ideal control. The differentiable graded
  matter-SUGRA Dirac generator is `NOT_DERIVED`, so template completeness and equivalence-class
  deduplication remain `DEFERRED_PENDING_CANONICAL_BRIDGE`.
- The selected nonzero-charge target is therefore `INCONCLUSIVE_UNCONSTRUCTED`; the literal
  branch-superpartner target remains `INCONCLUSIVE_OUT_OF_SCOPE`. Phase 14B is not opened.
- This kernel has no mapped legacy output. The runnable catalog rises to 45, while the mapped
  reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md`](../cpt_temporal_folded_susy/PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md),
[`../cpt_temporal_folded_susy/PHASE14A_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE14A_RESEARCH_CONTRACT.json),
and
[`../cpt_temporal_folded_susy/PHASE14A_RUN_RESULT.json`](../cpt_temporal_folded_susy/PHASE14A_RUN_RESULT.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 15R

Phase 15A was stopped as `INVALID/INCONCLUSIVE/PREREG_OR_PROVENANCE_INVALID` after a parent-sign
outcome was observed before the complete executable commit. Phase 15R disclosed that outcome as a
known prior, preregistered a fresh source-scoped reproduction, and kept the Hohl, Kallosh, and
non-evidential ADM symbolic graphs disjoint.

- The committed first run and independent replay both returned exit 0 with **47 exact checks,
  17 mutant categories / 18 fixtures rejected, 4 scope guards, and 24/24 known-prior matches**.
- Hohl's frozen source-native map gives (R_H=+6Q) and, after the unique endpoint removal,
  first-order inertia ((0,0,3)). It is `REJECT_SIGN` for the ADM-compatible Lorentzian bosonic target.
- Kallosh's source-native map gives (R_K=-6Q) and inertia ((1,0,2)), so it passes the bosonic
  target. Its frozen source coverage lacks the target old-minimal auxiliary-retaining action and
  complete required transformation family, so it is `BOSONIC_PARENT_ONLY`.
- The bosonic target is `VALID/SUPPORTS/NONE`; the full same-source target is
  `VALID/CONTRADICTS/NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS`. This is a result for exactly the two
  frozen primary candidates, not a literature-wide SUGRA no-go.
- Hohl action/transformations may not be stacked with Kallosh curvature/action signs. Phase 15
  tangency and every relational branch projector remain closed. The literal branch-superpartner core
  remains `INCONCLUSIVE/UNCONSTRUCTED` with no new observable.
- The runnable catalog is now 46; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md`](../cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md),
[`../cpt_temporal_folded_susy/PHASE15R_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE15R_RESEARCH_CONTRACT.json),
[`../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json`](../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json),
[`../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json`](../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json),
and
[`../cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json`](../cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json).

## Historical scientific ledger

The rows below summarize previously committed outputs and audits. They are historical evidence, not a
current execution policy and not proof that similarly named KG nodes exist.

| Topic | Source | Historical evidence relation / caveat |
|---|---|---|
| 42 sedenion assessors / 84 ZD pairs | `prove_higgs_results.json` | supports the L1 combinatorial count; does not by itself support a Higgs referent |
| S3 Jacobi/associator structure | `prove_s3_results.json` | structural algebra result |
| S5 BV bounded result | `prove_s5_results.json` | structural/numerical consistency result |
| Der(S) dimension 14 computation | sedenion result corpus | local numerical result; external review and precise method provenance remain separate |
| mass-ratio derivation | `derive_mass_ratios_results.json` | script self-report says 0/15 genuine |
| L-star derivation | `derive_Lstar_results.json` | script self-report says it does not uniquely predict L-star |
| naive custodial construction | queue02 result corpus | structural closure diagnostics contradict the proposed construction |
| Koide-like matches | `derive_dimensionless_results.json`, numerology judge | historical null scan found high coincidence risk |
| mp/mW search | `verify_mp_mW_results.json`, numerology judge | literal mismatch and high look-elsewhere coincidence risk |
| queue03 threshold scan | `queue_03_threshold_sensitivity_results.json` | invalid as a portable pass/fail metric because of basis dependence |
| queue08 projected g2 claim | queue08 diagnostics | method-artifact warning: projected/non-alternative construction did not establish the claimed Lie representation |
| queue09 group action | queue09 result corpus | earlier orbit-membership test was too permissive; multiplication-preservation gate remains needed |

### Workbench reframe

The 2026-05-18 position treats ICE as a `HypercomplexHypothesisTestbench`, not a completed
`PhysicsTheoryProgramme`:

- L1 algebra results may be useful independently.
- L2/L3 physical interpretations remain a separate tested belt and require external discriminators.
- User-primary mythology remains a separate narrative layer.

Historical wording such as “L1 progressive / L2-L3 stagnant” is a checkpoint assessment of those
declared fibers, not a label to recompute after every script. Statements must disclose their layer.

## Known limitations and bounded follow-ups

1. Queue03 needs a separately versioned, preregistered, basis-invariant method. A candidate must gate
   closure, nondegeneracy, and combined rank before evaluating cross-commutation; the existing ledger is
   quarantined rather than silently rewritten.
2. Queue09 needs a multiplication-preservation criterion before a group-theoretic interpretation.
3. Several historical result schemas and names differ from the live CLI; new kernels should use stable
   JSON types and cheap imports.
4. Local typecheck/tests exist, but scheduled remote reproduction is a separate operational task.
5. External peer review and formalization are separate projects; this repository cannot self-ratify them.

Each item is a bounded follow-up candidate. None automatically opens a child cycle or changes canon.
