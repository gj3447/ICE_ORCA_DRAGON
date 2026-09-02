# Scientific-intuition sidecar

This directory carries source-linked questions that may help a human sharpen a
canonical open problem. It is deliberately outside `ontology/collection.json`:
none of its records is a claim, evidence, a score, or execution authority.

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

The response contains an exact `canonical_target`, retrieval-only
`canonical_context`, `non_authoritative_signals`, and derived
`federated_links`. The stored `target`, `source_refs`, and optional exact
`canonical_source` bridge remain authoritative for sidecar linkage. A consumer
must preserve these distinctions. Signal selection is exact target matching in
file order and is capped at 20; the free-text query ranks canonical context
only, never the intuition records:

- `INTEGER` is a located computed intersection value.
- `UNRESOLVED` means the value or required object is missing.
- `OUT_OF_SCOPE` means an explicit bounded exclusion.
- Numerical zero is never inferred from either non-numerical state.

Read the cited primary source before selecting at most one bounded question for
human review. Then run `./ice agent plan`; do not send a sidecar signal directly
to `./ice run` or treat it as a reason to modify the canonical ontology.
