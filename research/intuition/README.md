# Scientific-intuition sidecar

This directory carries source-linked questions that may help a human sharpen a
canonical open problem. It is deliberately outside `ontology/collection.json`:
none of its records is a claim, evidence, a score, or execution authority.

The [whole-research intuition map](../../docs/research/ICE_RESEARCH_INTUITION_KG_MAP_2026-09-07.md)
adds a recent CPT case study: carrier comparison and cohomology, bulk reduction and endpoint
data, and common-domain observables with a positive product. Three new question lenses reuse
the existing boundary-amplitude topic and target the current seam-state open problem:

```bash
./ice intuition search "Which state and endpoint data survive a carrier change?" \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit --json
```

The canonical concept links in that guide are separately reviewed navigation changes; the
sidecar itself still creates no canonical claim or evidence.

The [abstraction and intuition connectivity map](./ICE_ABSTRACTION_CONNECTIVITY_MAP_2026-09-06.md)
now provides three human reading routes: local root to boundary/source structure,
boundary amplitude to physical state, and reduced model to full-parent scope. It
explains the six implemented v2 question lenses without turning their links into
canonical evidence. The earlier [implementation plan](../../docs/research/ICE_ABSTRACTION_INTUITION_CONNECTIVITY_PLAN_2026-09-06.md)
remains provenance for the bounded design.

The [geometry–CPT–SUSY intuition map](./ICE_GEOMETRY_CPT_SUSY_INTUITION_MAP_2026-09-03.md)
connects the discussed “curvature is energy” and “SUSY on the other side” ideas
without identifying them. It keeps equation-side relabeling, vacuum Weyl
curvature, CPT/Pin sewing, a physical fermion-odd charge, state asymmetry, pole
splitting, and cross-domain observables as separately typed tests. The map is a
human view over this sidecar and existing canonical open problems; it does not
add canonical evidence.

[`scientific-intuition-signals.v1.json`](./scientific-intuition-signals.v1.json)
is the immutable Gate-1 snapshot pinned by an existing result hash. The active
[`scientific-intuition-signals.v2.json`](./scientific-intuition-signals.v2.json)
copies those lenses into a general ICE sidecar, adds typed `topic:*` nodes and
topic links, and permits an optional `canonical_target` only where an existing
`open_problem` has matching scope. In particular, the geometry–energy topic has
no fabricated link to the V=0 closed-FRW likelihood lane.

Validate the strict file and resolve every target/source bridge against the
current canonical collection:

```bash
./ice intuition validate --json
```

Federate one canonical open problem with bounded GraphRAG context and matching
question lenses:

```bash
./ice intuition search "Which typed object separates unknown from zero?" \
  --target cpt::open:gate1-original-cycle-signed-global-intersections \
  --limit 8 --depth 1 --json
```

The broader candidate lenses can be retrieved by exact canonical target:

```bash
./ice intuition search "Which invariant separates geometry from an effective fluid?" \
  --target intuition::topic:geometry-energy-unification --json
./ice intuition search "Is CPT sewing distinct from a physical fermion-odd charge?" \
  --target cpt::open:gate4-spinorial-charge-domain-constraint-closure --json
./ice intuition search "What survives dilution and moves an interacting retarded pole?" \
  --target cpt::open:gate5-persistent-order-and-pole-splitting --json
```

The response contains either an exact `sidecar_target` or `canonical_target`,
`non_authoritative_signals`, typed topic context, and derived
`federated_links`. `canonical_context` is `null` for a sidecar-topic query. The
stored `topic`, optional `canonical_target`, `source_refs`, and optional exact
`canonical_source` bridge remain authoritative for sidecar linkage. A consumer
must preserve these distinctions. Signal selection is exact target matching in
file order and is capped at 20; the free-text query ranks canonical context
only for a canonical-target query, never the intuition records:

- `INTEGER` is a located computed intersection value.
- `UNRESOLVED` means the value or required object is missing.
- `OUT_OF_SCOPE` means an explicit bounded exclusion.
- Numerical zero is never inferred from either non-numerical state.

Read the cited primary source before selecting at most one bounded question for
human review. Then run `./ice agent plan`; do not send a sidecar signal directly
to `./ice run` or treat it as a reason to modify the canonical ontology.
