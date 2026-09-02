# Scientific intuition signal layer — 2026-09-02

## Decision

Add `research/intuition/scientific-intuition-signals.v1.json` as a versioned,
source-linked **non-authoritative hypothesis-generation sidecar** for the CPT
Gate-1 route.  Its schema is
`ontology/schema/scientific-intuition-flow-v1.schema.json`.

The sidecar is deliberately not a fifth canonical research graph.  The
canonical CPT graph remains the sole local authority for claims, evidence
status, open problems, and TOE-route navigation.  This layer cannot change
those objects, establish a mathematical or physical result, promote a claim,
or authorize a runner.  `CANDIDATE` means only that a question-shaped lens is
retained for human review.

## Why a sidecar, rather than a fifth canonical graph

A separate canonical graph would invite a false merge between (a) source-linked
questions that help generate alternative tests and (b) the evidence-bearing CPT
claim graph.  It would also turn methodological sources into apparent CPT
evidence.  The sidecar instead has a fixed target reference of the form
`{ graph: "cpt", node: "open:..." }`, carries explicit assumptions,
discriminating observations, stop conditions, and a non-claim statement, and
states `does_not_authorize_execution: true` on every signal.

This is consistent with the workbench boundary: numerical or graph structure
does not by itself constitute physics, and a candidate lens does not constitute
a calculation request.  The existing `./ice agent plan` and human review remain
the route for deciding whether a bounded question is appropriate.

## Research design represented here

The initial lenses are a small alternative set, not a claim quorum:

| Canonical target | Candidate bounded output idea | What it must not imply |
| --- | --- | --- |
| `open:gate1-original-cycle-signed-global-intersections` | A source-defined inventory plus a typed cycle-incidence ledger that keeps `INTEGER`, `UNRESOLVED`, and `OUT_OF_SCOPE` distinct. | That a global cycle or signed vector has been found, or that an unresolved entry is zero. |
| `open:p38-explicit-joint-action-cycle-and-oriented-intersections` | A conditional finite-cutoff separation test between original-cycle candidates and saddle-local data. | That a surrogate proves a physical relative-homology result. |
| `open:p34-full-joint-dual-determinant-and-global-census` | Three separately reported outputs: fold-arm connection, determinant-line transport, and sheet/end census. | That agreement of local pieces fixes a global coefficient. |
| `open:p35-absolute-detline-full-bfv-and-global-cycle` | A convention-explicit discriminator for absolute versus relative orientation. | That a relative endpoint phase fixes absolute Maslov orientation or a physical state. |

Every lens has a predeclared discriminator and stop condition.  A null,
inconclusive, or alternative-preserving output is retained rather than being
converted into a positive result.  The source list includes Chamberlin's
[multiple working hypotheses](https://doi.org/10.1126/science.ns-15.366.92),
Platt's [strong inference](https://doi.org/10.1126/science.146.3642.347),
[NINDS rigorous study-design guidance](https://www.ninds.nih.gov/funding/preparing-your-application/preparing-research-plan/rigorous-study-design-and-transparent-reporting),
Gelman and Shalizi's [model checking discussion](https://arxiv.org/abs/1006.3868),
the National Academies' [reproducibility report](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science),
Witten's [analytic-continuation treatment](https://arxiv.org/abs/1001.2933),
and Feldbrugge, Lehners, and Turok's domain-adjacent
[Lorentzian minisuperspace example](https://arxiv.org/abs/1703.02076).
Those sources constrain method or furnish a bounded mathematical analogy; none
is CPT evidence.  In particular, the minisuperspace example is not assumed to
select this repository's action, original cycle, regulator, or state.  Gottweis
et al.'s [Accelerating scientific discovery with
Co-Scientist](https://arxiv.org/abs/2502.18864) (current v2, 2026-06-29;
related [Nature article](https://doi.org/10.1038/s41586-026-10644-y)) is included
only as a contemporary, non-authoritative precedent for separating
generation/debate/evolution from acceptance.  Its biomedical scope and results,
its Auto-Elo ranking, and its scientist-in-the-loop framing do not validate
physics hypotheses, ranking, or automated execution here.

## Standards and read-only federation

The schema records a deliberately small stable-standard alignment:

- [RDF 1.1](https://www.w3.org/TR/rdf11-concepts/) named-graph separation can
  keep a future assertion graph distinct from provenance.
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) is an exchange syntax, not a
  truth mechanism.
- [PROV-O](https://www.w3.org/TR/prov-o/) can describe source and artifact
  derivation without asserting validity.
- [SHACL](https://www.w3.org/TR/shacl/) would validate a future RDF projection,
  but needs separate shapes and would provide structural conformance only.

The repository interoperability baseline is deliberately RDF 1.1, JSON-LD 1.1,
SHACL 1.0, and PROV-O.  This JSON sidecar itself uses Draft 2020-12 JSON Schema
plus canonical-reference semantic checks; it does not claim SHACL validation.
[RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) is a W3C
Candidate Recommendation Snapshot (2026-04-07), and [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/)
is a Working Draft (2026-08-28).  They are tracked for future interoperability,
not imported into the baseline, schema, or validity claims.

Search federation is a **read-only** operation, not a graph merge:

```bash
./ice intuition validate --json
./ice intuition search "signed global intersection discriminator" \
  --target cpt::open:gate1-original-cycle-signed-global-intersections --json
```

The same search is exposed to MCP clients as
`ice_scientific_intuition_search`.  A response always includes the exact
canonical target, bounded canonical GraphRAG context, matching sidecar signals,
their source records, standards alignment, and derived typed links:
`TARGETS_CANONICAL_OPEN_PROBLEM`, `CITES_SOURCE`, and, where an exact local
source node exists, `MIRRORS_CANONICAL_SOURCE`.  The stored target and source
references remain the single sidecar source of those derived links.  Signal
selection is exact target matching in file order, capped at 20; the query ranks
only canonical GraphRAG context, so no hidden intuition score is introduced.

The response labels all sidecar material
`NON_AUTHORITATIVE_HYPOTHESIS_GENERATION` and never ranks it as evidence above
canonical artifacts.  Strict decoding rejects unknown or claim-like fields;
semantic validation resolves every source and canonical target, verifies exact
canonical-source URI bridges, and keeps the canonical ontology, GraphRAG index,
and TOE planner unchanged.

No autonomous execution, task handoff, MCP task, or automatic next experiment
is introduced by this decision.
