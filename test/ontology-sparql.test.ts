import { expect, it } from "vitest"
import { buildRdfDataset } from "../src/ontology/rdf.ts"
import { queryRdfDataset } from "../src/ontology/sparql.ts"

it("executes bounded offline SPARQL and rejects remote/update forms", async () => {
  const descriptor = { key: "demo", graph_id: "research-graph:demo", path: "ontology/demo/graph.json", guide: "guide", entry_node: "programme:demo", coverage: "DETAILED", corpus_roots: ["demo"], includes: [], excludes: [] }
  const collection = { schema_version: "research-collection/v1", collection_id: "research-collection:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: "ontology/collection.json", default_graph: "demo", graphs: [descriptor], quick_answers: [], reading_paths: [], coverage_ledger: [] }
  const graph = { schema_version: "research-graph/v1", graph_id: "research-graph:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: descriptor.path, source_inventory: "sources", quick_answers: [], reading_paths: [], node_type_legend: {}, relation_legend: {}, nodes: [{ id: "programme:demo", type: "programme", title: "Demo", summary: "Demo", state: "ACTIVE" }], edges: [], kg_bridges: [] }
  const built = await buildRdfDataset(collection as any, [{ descriptor, graph, validation: {} }] as any, { sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })
  const result = await queryRdfDataset(built.dataset, "SELECT ?node WHERE { GRAPH <urn:ice-orca-dragon:resource:graph:demo> { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } }")
  expect(result.result).toMatchObject({
    head: { vars: ["node"] },
      results: { bindings: [{ node: { type: "uri" } }] }
  })
  const ask = await queryRdfDataset(
    built.dataset,
    "ASK WHERE { GRAPH <urn:ice-orca-dragon:resource:graph:demo> { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } }"
  )
  expect(ask.result).toEqual({ head: {}, boolean: true })
  const empty = await queryRdfDataset(
    built.dataset,
    "SELECT ?missing WHERE { ?missing <urn:ice-orca-dragon:ontology:notPresent> ?value }"
  )
  expect(empty.result).toEqual({
    head: { vars: ["missing"] },
    results: { bindings: [] }
  })
  const bounded = await queryRdfDataset(
    built.dataset,
    "SELECT ?subject ?predicate ?object WHERE { ?subject ?predicate ?object }",
    { limit: 1 }
  )
  expect(bounded.row_count).toBe(1)
  expect(bounded.truncated).toBe(true)
  const construct = await queryRdfDataset(
    built.dataset,
    "CONSTRUCT { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } WHERE { GRAPH <urn:ice-orca-dragon:resource:graph:demo> { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } }"
  )
  expect(construct.media_type).toBe("application/n-quads")
  expect(construct.nquads).toContain("urn:ice-orca-dragon:ontology:ResearchNode")
  await expect(queryRdfDataset(built.dataset, "SELECT * WHERE { SERVICE <https://example.invalid/> { ?s ?p ?o } }")).rejects.toThrow("not allowed")
  await expect(
    queryRdfDataset(
      built.dataset,
      "SELECT * FROM <https://example.invalid/data> WHERE { ?s ?p ?o }"
    )
  ).rejects.toThrow("not allowed")
  await expect(
    queryRdfDataset(built.dataset, "INSERT DATA { <urn:a> <urn:b> <urn:c> }")
  ).rejects.toThrow("not allowed")
  await expect(
    queryRdfDataset(built.dataset, 'SELECT ?node WHERE { ?node ?predicate "SERVICE" }')
  ).resolves.toMatchObject({ form: "SELECT" })
  await expect(
    queryRdfDataset(built.dataset, "SELECT ?node WHERE { ?node <urn:ice-orca-dragon:ontology:localId>+ ?other }")
  ).rejects.toThrow("property paths")
  await expect(
    queryRdfDataset(built.dataset, "SELECT ?node WHERE { { SELECT ?node WHERE { ?node ?predicate ?object } } }")
  ).rejects.toThrow("pattern 'query'")
  const tooManyTriples = Array.from(
    { length: 13 },
    (_, index) => `?s <urn:predicate:${index}> ?o${index} .`
  ).join(" ")
  await expect(
    queryRdfDataset(built.dataset, `SELECT ?s WHERE { ${tooManyTriples} }`)
  ).rejects.toThrow("triple patterns")
  await expect(
    queryRdfDataset(built.dataset, "SELECT ?node WHERE { ?node ?predicate ?object } ORDER BY ?node")
  ).rejects.toThrow("ordering")
  await expect(
    queryRdfDataset(
      built.dataset,
      "SELECT ?left ?right WHERE { ?left <urn:left> ?leftValue . ?right <urn:right> ?rightValue }"
    )
  ).rejects.toThrow("disconnected variable joins")
  await expect(queryRdfDataset(built.dataset, "DESCRIBE *")).rejects.toThrow(
    "explicit terms"
  )
})
