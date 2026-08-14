# ICE_ORCA_DRAGON status

> Current engineering/reproduction state followed by a bounded historical scientific ledger. This file
> reports evidence; it does not authorize KG or canon mutation.

## Current state — 2026-08-14

| Component | State |
|---|---|
| Runnable catalog | 42 entries; `./ice list --json` is authoritative |
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
