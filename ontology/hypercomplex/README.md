# Hypercomplex hypothesis-testbench ontology

> This graph indexes the finite Cayley–Dickson and sedenion calculations separately from their proposed
> particle-physics interpretations. A recorded algebraic regularity is not automatically a Higgs field,
> gauge group, family count, observable, or TOE claim.

## Current answer

```text
ALGEBRAIC_STRUCTURE        = PARTIALLY_SUPPORTED
PROJECTED_PHYSICS_MAPS     = CONTRADICTED_OR_INCONCLUSIVE
LEGACY_METHOD_PORTABILITY  = MIXED
CLAIM_B_FINITE_ROUTE       = KILLED_WITHIN_PREREGISTERED_SCOPE
FULL_INFINITE_TOWER        = UNCONSTRUCTED
STANDARD_MODEL_EMBEDDING   = NOT_ESTABLISHED
```

The most useful intuition is a fork:

```text
Cayley–Dickson multiplication
├─ invariant finite structure
│  ├─ 42 assessor planes = 7 × 6
│  ├─ 84 signed vectors e_a ± e_b for a<b
│  ├─ 168 representations when index order is counted
│  ├─ annihilating pairs require an explicit sign/order convention
│  ├─ 7 × 6 assessor orbit organization
│  ├─ XOR/multiplication label regularity
│  ├─ finite associator/Jacobi/BV identities
│  └─ explicit S3 subgroup
│     ├─ centralizes the computed 14D derivation space
│     └─ preserves the recorded Wilmot eq-9 theta tensor
├─ infinite-tower Claim B finite route
│  ├─ n=5..7 nullity-distribution stability → contradicted
│  ├─ n=4..7 associator-distribution stability → contradicted
│  ├─ registered composite Cauchy decrease → contradicted
│  └─ infinite measure/action/gravity map → still unconstructed
└─ proposed physics map
   ├─ projected custodial closure       → contradicted
   ├─ basis-dependent Queue-03 threshold → quarantined
   ├─ projected sedenion g2             → method artifact
   ├─ toy vacuum minima                 → local toy result only
   └─ Standard Model or Higgs referent  → not established
```

## Seven reading paths

1. **What the number 42 actually counts**

   Follow the multiplication convention to the assessor taxonomy, then to the 7-by-6 orbit and XOR
   ledger. The historical result calls 42 objects “ZD pairs” and “Higgs candidates”; the current
   terminology is 42 unordered assessor axis-planes, 84 signed vectors with `a<b`, and 168
   representations when both index orders are counted. The two direct scripts separately expose
   annihilating-pair ordering (168 unordered any-sign pairs versus 336 ordered products); the bare word
   “pair” is therefore not used without a convention. The Higgs referent does not follow from a count.

2. **Where projection loses algebraic closure**

   Follow the four-dimensional null spaces to the projected left/right triples. All 42 tested
   candidates fail the declared simultaneous custodial closure; the combined rank is 3 rather than the
   required 6. Queue 03 cannot repair this because its entrywise maximum changes with the arbitrary
   null-space basis.

3. **Why the original projected g2 construction was demoted**

   The original sedenion-ambient use of an octonion derivation formula yields rank 16 rather than 14 and
   a non-scalar Casimir. A later automorphism-embedded construction recovers rank 14 and antisymmetry but
   still has failed full Lie/Casimir controls, so it is not a complete repair.

4. **What survives from the finite higher-algebra tests**

   The recorded S3 and S5 scripts support finite identities on their declared arrays. These are useful
   algebraic witnesses, not general all-dimension theorems or particle interactions.

5. **How result provenance changes interpretation**

   Queue 06's committed result came from `inconclusive_redo.py`, not its mapped historical runner.
   Queue 09's explicit S3 computation survives, while the older “Wilmot refuted” prose was later
   withdrawn. Queue 03 is deliberately `NONPORTABLE_FAIL`, not a successful reproduction.

6. **What the later S3 audits add—and do not add**

   The direct-action calculation reconstructs a 14-dimensional numerical derivation space and finds
   that conjugation by the explicit sigma and Psi generators acts as the identity on that space within
   (8.9\times10^{-16}). A separate two-convention calculation aligns the transcribed Wilmot eq-9
   theta tensor with the alternating structure constants up to a global sign and finds sigma/Psi
   preservation residuals (0) and (2.78\times10^{-17}). These are finite scoped results. They do not
   prove completeness of `Aut(S)`, integrate every component, or implement Wilmot's cross-primary
   realization.

7. **Why the finite Claim B route is sealed without becoming a universal no-go**

   The preregistered loop records total-variation distances (0.476190) and (0.488189) for the
   (n=5,6,7) nullity distributions, consecutive associator-distribution KS statistics (0.1484),
   (0.1072), and (0.1036), and a failed composite Cauchy-decreasing predicate. That kills the
   registered finite statistical-stability route. It does not define the infinite-dimensional limit,
   path-space measure, action, renormalization, or gravity observable, nor prove that every alternative
   completion is impossible.

## Quick answers

- **Are there 42 Higgs particles?** No. The robust finite count is 42 assessor planes in seven
  six-element classes; no Higgs referent or particle prediction has been derived.
- **Did custodial SU(2) × SU(2) close?** No. The frozen projected test reports 42/42
  `FAIL_BOTH_CLOSURE`.
- **Is Queue 03 portable evidence?** No. Its verdict changes under a basis rotation of the same null
  space.
- **Was g2 established inside the sedenions?** The original projected construction is a method
  artifact. The later rank-14 sidecar remains incomplete.
- **Was an S3 subgroup computed?** Yes. Its recorded action also centralizes the computed derivation
  space and preserves the implemented theta tensor. This does not prove the full global automorphism
  decomposition, refute Wilmot, or explain three particle generations.
- **Did Claim B produce a stable infinite-tower limit?** No under the stored finite-level predicates.
  The finite route is sealed, but the infinite object and physics map were never constructed by those
  tests.

## Evidence discipline

Raw JSON is retained as historical output even when its label is stale. The graph places the current
claim state on a separate claim node and links it to both the raw result and the later audit. It does not
silently rewrite generated files.

The Avenue-3 exact source and a separate reconstruction are hash-pinned beside the historical report.
They make the `42/84/168` object distinctions inspectable instead of treating the three numbers as
interchangeable labels.

The reproducibility ledger currently distinguishes:

- portable mapped reproductions;
- Queue 03 `NONPORTABLE_FAIL`;
- Queue 06 `SUPERSEDED`;
- direct-run-only results whose producer or source interpretation still needs repair.

## Query

```bash
./ice ontology summary --graph hypercomplex
./ice ontology guide --graph hypercomplex
./ice ontology show HYPER_ZD_ASSESSOR_ORBIT_CHAIN
./ice ontology trace HYPER_PROJECTED_SEDENION_G2_REPRESENTATION --depth 3
./ice ontology guide --graph hypercomplex --path hyper-claimb-sealed-finite-route
./ice ontology trace HYPER_S3_ACTION_CENTRALIZES_COMPUTED_DERIVATION_SPACE --depth 2
```

The machine record is [`graph.json`](./graph.json); source and result roles are listed in
[`references/source-inventory.md`](./references/source-inventory.md).
