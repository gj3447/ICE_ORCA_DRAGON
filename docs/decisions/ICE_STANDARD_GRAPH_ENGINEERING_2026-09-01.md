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
2. The offline interoperability export emits a generated JSON-LD 1.1/RDF 1.1
   projection and package. It uses fixed repository-local URNs and
   graph-qualified resource IRIs. Every native edge is a separate
   `ice:ResearchEdge`, preserving its local ID, endpoints, relation, polarity,
   and note. The package includes source-document SHA-256 values, SHACL 1.0
   Core validation, a structurally bounded read-only local SPARQL 1.1 subset, PROV-O
   lineage, and RO-Crate 1.3 metadata.

`npm run graph:check` runs strict TypeScript checks, the Vitest suite, the
full repository ontology validation, and all-graph SHACL projection validation. `npm run graph:review` and `npm run
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
and an explicit context that maps compact terms to IRIs. The offline export
therefore gives standards-aware consumers a graph view without introducing a
graph database or a second hand-edited serialization.

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

The accompanying [SHACL 1.0 Core](https://www.w3.org/TR/shacl/) shapes are
executed offline against the generated RDF dataset used by the projection and
package. They validate projection structure and export lineage, not native
research validity or RO-Crate metadata/files.
The package also exposes a bounded, read-only
[restricted local SPARQL 1.1 subset](https://www.w3.org/TR/sparql11-query/)
query interface and uses
[PROV-O](https://www.w3.org/TR/prov-o/) only for source-to-export lineage:
no generic provenance edge is substituted for the repository's scientific
`HAS_EVIDENCE` relation. An [RO-Crate 1.3](https://w3id.org/ro/crate/1.3),
published as a community Recommendation on 2026-06-22, packages the generated
materials and their metadata. Its enriched JSON-LD and N-Quads members are
RDF-equivalent; a separate compatibility JSON-LD member is the exact byte
payload identified by the embedded projection-output digest.

The stable interoperability target is RDF 1.1, JSON-LD 1.1, SHACL 1.0,
SPARQL 1.1, PROV-O, and RO-Crate 1.3. RDF 1.2, SHACL 1.2, and SPARQL 1.2 are
not claimed as completed conformance targets because their current W3C
publications are pre-Recommendation drafts. The read-only MCP boundary negotiates
the [MCP 2026-07-28 revision](https://blog.modelcontextprotocol.io/posts/2026-07-28/), with 2025-era
stdio compatibility: it carries bounded inspection capabilities but is neither agent execution
orchestration nor research authorization.

## Authoring workflow

```bash
./ice harness impact <registered-repository-path>
# edit a registered graph JSON and, when navigation changes, collection.json
./ice ontology review --graph <key> --base HEAD
./ice graphrag eval --limit 12 --json
./ice graphrag diff --base HEAD --limit 12 --json
npm run graph:check
./ice ontology export --format jsonld --graph <key> > /tmp/research-graph.jsonld
./ice ontology export --format dataset-jsonld --graph <key> > /tmp/research-dataset.jsonld
./ice ontology export --format nquads --graph <key> > /tmp/research-graph.nq
./ice ontology shacl --graph <key> --json
./ice ontology sparql '<bounded SELECT|ASK|CONSTRUCT|DESCRIBE>' --graph <key>
./ice ontology crate output/<new-name> --graph <key> --json
```

The versioned retrieval suite and revision-diff interpretation are defined in
[`ICE_GRAPH_RAG_RETRIEVAL_REGRESSION_2026-09-02.md`](ICE_GRAPH_RAG_RETRIEVAL_REGRESSION_2026-09-02.md).

Generated interoperability material is produced offline and is not a second
canonical graph. The review command does not write patches, mint IDs, update
timestamps, modify the collection manifest, or approve a calculation. Normal
Git review remains responsible for interpreting the diff and reviewing prose
changes.

## Explicit non-claims

- A projected IRI is a repository-local identifier, not an external KG match.
- JSON-LD/RDF serialization does not make a scientific claim true.
- SHACL conformance checks projection shape, not artifact hashes,
  evidence polarity, or physical validity.
- PROV metadata describes export lineage; it does not turn policy or citation into
  evidence.
- An RO-Crate, SHACL report, or SPARQL result is an interoperability artifact,
  not a GraphRAG reference implementation, a physical ratification, or an
  agent authorization.
- No import, merge, inference, external UID minting, graph-database write, or
  automatic successor calculation is authorized.

This is control-plane infrastructure. It changes no claim status, evidence,
scope, open problem, or physics conclusion in the research ontology.
