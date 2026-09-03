---
title: Non-authoritative sidecar collection
status: active engineering boundary
date: 2026-09-03
---

# Non-authoritative sidecar collection

`research/sidecars/collection.v1.json` is a strict, fixed-path registry for the two scientific-
intuition documents and the external comparator protocol. It supplies a stable locator, byte hash,
declared state, and explicit non-claim boundary.

It is not an ontology collection, graph, RDF/JSON-LD export, SHACL dataset, SPARQL source, GraphRAG
corpus, planner input, or MCP surface. It cannot create a canonical node or edge, alter evidence
status, promote a physics interpretation, or authorize an execution.

The v1 intuition snapshot remains hash-pinned as frozen provenance. The active v2 intuition and
comparator-method documents are hash-checked at validation time and retain their own strict semantic
validators. `./ice sidecars validate` performs the aggregate read-only check; `summary` and `show`
are locator views only.

This adds no full knowledge-graph ingestion layer. A sidecar becomes canonical only through a
separate, justified canonical-ontology change that passes the existing ontology validation path.
