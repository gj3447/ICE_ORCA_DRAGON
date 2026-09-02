# Research-graph interoperability boundary

The repository-local JSON collection, its runtime Effect schemas, and the
repository semantic validator are authoritative.  In particular, raw result
artifacts remain the authoritative check ledgers described in
[`../README.md`](../README.md).  Nothing in this directory changes the native
schema or validator.

Any JSON-LD is a generated, read-only, one-way projection of that native
record:

- Native JSON is the only import source.  JSON-LD/RDF is never imported or
  merged back into it.
- A projection does not promote a local node to an external identity and does
  not resolve, mint, or merge external KG identifiers.
- Use `urn:ice-orca-dragon:ontology:` for projected ontology resources and
  `urn:ice-orca-dragon:resource:` for projected repository resources.  These
  are local namespace bases, not assertions of external identity.
- Keep source paths and SHA-256 values as projected values from the native
  record.  A JSON-LD serialization or RDF normalization is not a replacement
  for the native artifact hash, path, command, environment, or check ledger.
- The export manifest records the working-tree SHA-256 of the canonical
  collection document and each selected graph document. It binds an export to
  its input bytes but does not certify the artifacts referenced by those
  documents; `./ice ontology validate` remains that integrity gate.

`--graph <key>` selects the graph-specific bodies (nodes, edges, graph reading
paths, and bridges) but deliberately retains the complete collection envelope,
including its descriptors and navigation metadata. It is a contextual query,
not an access-control or redaction boundary. The selected body keys and only
the selected canonical graph-document hashes are listed explicitly.

The offline interoperability package additionally records the projection's
input source documents, export activity, and generated output with PROV-O.
`prov:used` identifies the immutable input records, while
`prov:wasGeneratedBy` connects an emitted output to its export activity. This
is operational lineage only: it neither replaces the native check ledger nor
turns a `HAS_EVIDENCE` relation, a citation, or a numerical result into a
scientific conclusion.

The projection reifies every graph edge as a `project:ResearchEdge` resource.
The native edge has its own stable `localId` and may carry metadata such as
`polarity` and `note`; representing only its relation as an RDF predicate
would not retain that record as a resource with its metadata.  The edge shape
therefore requires exactly one `from`, `relation`, and `to` value.

`research-graph-shapes.ttl` is a minimal SHACL 1.0 Core contract for the
offline RDF/JSON-LD projection and package: it checks the projection
collection, source documents, export activity, output entity, native records,
and reified edges. The offline validator emits a validation result for the
generated package; it is projection QA only. It does not replace the local
semantic validator or add an execution or research gate.

RDF has no JSON `null`.  For an unresolved KG bridge, a projection must retain
the explicit native nulls by emitting one value for both `externalUid` and
`relation`: use `project:NoExternalUid` and `project:NoRelation`, respectively.
The bridge shape requires those properties to be present, rather than allowing
the missing values to be silently dropped.

## Standards used by this boundary

- [RDF 1.1 Concepts and Abstract Syntax — W3C Recommendation, 25 February 2014](https://www.w3.org/TR/rdf11-concepts/)
- [JSON-LD 1.1 — W3C Recommendation, 16 July 2020](https://www.w3.org/TR/2020/REC-json-ld11-20200716/)
- [Shapes Constraint Language (SHACL) — W3C Recommendation, 20 July 2017](https://www.w3.org/TR/shacl/)
- [SPARQL 1.1 Query Language — W3C Recommendation, 21 March 2013](https://www.w3.org/TR/sparql11-query/)
- [PROV-O: The PROV Ontology — W3C Recommendation, 30 April 2013](https://www.w3.org/TR/prov-o/)
- [RO-Crate Metadata Specification 1.3 — community Recommendation, 22 June 2026](https://w3id.org/ro/crate/1.3)
- [Model Context Protocol, version 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)

The offline package contains RDF/JSON-LD, SHACL validation material, a
read-only SPARQL 1.1 query surface, PROV-O lineage, and an RO-Crate 1.3
metadata descriptor. It is a portable inspection and validation boundary, not
a GraphRAG reference implementation, a graph database, an agent runtime, or
an authorization to execute research work. MCP is the separate read-only
transport for bounded inspection tools; its protocol version is pinned above.

RDF 1.2, SHACL 1.2, and SPARQL 1.2 are deliberately not conformance targets:
their current W3C publications are still pre-Recommendation. The stable
RDF 1.1, SHACL 1.0, and SPARQL 1.1 requirements above are the implemented
offline compatibility baseline.

SKOS and DCAT are deliberately not part of this minimal contract.  Add SKOS
only for a frozen controlled vocabulary shared with another consumer; add DCAT
only for a stable, explicitly released dataset catalogue.
