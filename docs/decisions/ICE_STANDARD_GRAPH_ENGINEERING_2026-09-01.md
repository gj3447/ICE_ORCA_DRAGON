# Standard graph engineering without a second source of truth

Date: 2026-09-01

Status: accepted

## Decision

The repository-local `research-collection/v1` manifest and registered
`research-graph/v1` JSON documents remain the only authored graph records.
Their strict Effect decoders, semantic checks, evidence-ledger checks, and
repository-file hashes remain authoritative.

Two read-only engineering surfaces are added around that authority:

1. `./ice ontology review --graph <key|all> --base <revision>` compares the
   decoded committed collection manifest and selected graphs with the working
   tree. The result is a deterministic record-level diff for collection
   metadata, descriptors, coverage, collection paths and answers, plus graph
   nodes, edges, paths, answers and KG bridges, with focused authoring warnings.
2. `./ice ontology export --format jsonld --graph <key|all>` emits a generated
   JSON-LD 1.1 projection to stdout. It uses fixed repository-local URNs and
   graph-qualified resource IRIs. Every native edge is a separate
   `ice:ResearchEdge`, preserving its local ID, endpoints, relation, polarity,
   and note. The projection manifest includes working-tree SHA-256 values for
   the canonical collection document and selected graph documents.

`npm run graph:check` runs strict TypeScript checks, the Vitest suite, and the
full repository ontology validation. `npm run graph:review` and `npm run
graph:export` provide collection-wide shortcuts.

## Current navigation and cohesion rule

Live collection counts, graph coverage, and hash status belong to
`./ice ontology summary --json`; documentation must not treat copied totals as
an authority. The collection contains four independent research graphs. A
collection-aware review or reading path is navigation across those boundaries,
not an evidence merge, a theory synthesis, or an external KG operation.

For the active CPT candidate route, the graph records
`policy:toe-directed-critical-path-routing` and its default current blocker,
`open:gate1-original-cycle-signed-global-intersections`. The G1--G5 path is
the core navigation route. The P1--P7 V0 work is a supporting portfolio unless
a review identifies the exact canonical blocker, missing typed output, and
evidence edge changed by a proposed calculation. Neither a graph lookup nor a
reading path approves execution, progress, or a physics claim.

Graph cohesion means one canonical record per material claim, policy, blocker,
artifact, or scope; explicit typed edges for actual relations; and reading
paths or quick answers for alternate views. Do not clone claims into another
graph, manufacture a cross-graph bridge from topical similarity, or rewrite
historical provenance to flatten a current route. Validation rejects any
component without a programme anchor, summary exposes weak-component cohesion,
and `ontology review` includes the collection manifest as well as graph records.

## Why this shape

[RDF 1.1](https://www.w3.org/TR/rdf11-concepts/) defines graphs as sets of
subject-predicate-object triples and datasets as collections of graphs.
[JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) supplies a JSON serialization
and an explicit context that maps compact terms to IRIs. The export therefore
gives standards-aware consumers a graph view without introducing a graph
database or a second hand-edited serialization.

Native edges must be reified because they carry identity and optional metadata;
a bare RDF shortcut triple would lose that record boundary. Ordered native
arrays are emitted as JSON-LD lists. Native JSON records are also retained as
JSON typed values in the projection, making its one-way provenance explicit.
Local IDs are qualified by collection graph key so equal local IDs in different
research scopes never collide.

A graph selector limits graph-specific bodies, while the complete collection
envelope remains present for navigation context. It is not a disclosure or
redaction filter. The export lists selected graph keys and source-document
hashes so a consumer can distinguish the envelope from the selected bodies.

The accompanying [SHACL Core](https://www.w3.org/TR/shacl/) shapes are an
optional downstream projection contract. They do not replace the native
validator, and no SHACL processor is bundled. [PROV-O](https://www.w3.org/TR/prov-o/)
is reserved for a future named lineage consumer; no generic provenance edge is
substituted for the repository's scientific `HAS_EVIDENCE` relation.

## Authoring workflow

```bash
./ice harness impact <registered-repository-path>
# edit a registered graph JSON and, when navigation changes, collection.json
./ice ontology review --graph <key> --base HEAD
npm run graph:check
./ice ontology export --format jsonld --graph <key> > /tmp/research-graph.jsonld
```

The export is stdout-only by design. A downstream consumer may store it, but a
generated export is not committed here as another canonical graph. The review
command does not write patches, mint IDs, update timestamps, modify the
collection manifest, or approve a calculation. Normal Git review remains
responsible for interpreting the diff and reviewing prose changes.

## Explicit non-claims

- A projected IRI is a repository-local identifier, not an external KG match.
- JSON-LD/RDF serialization does not make a scientific claim true.
- SHACL conformance would check projection shape, not artifact hashes,
  evidence polarity, or physical validity.
- PROV metadata would describe lineage, not turn policy or citation into
  evidence.
- No import, merge, inference, external UID minting, graph-database write, or
  automatic successor calculation is authorized.

This is control-plane infrastructure. It changes no claim status, evidence,
scope, open problem, or physics conclusion in the research ontology.
