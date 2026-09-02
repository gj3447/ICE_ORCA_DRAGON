import { expect, it } from "vitest"
import { buildRdfDataset } from "../src/ontology/rdf.ts"
import {
  loadStandardShaclShapes,
  validateRdfDatasetWithShacl
} from "../src/ontology/shacl.ts"

it("reports SHACL results deterministically", async () => {
  const descriptor = { key: "demo", graph_id: "research-graph:demo", path: "ontology/demo/graph.json", guide: "ontology/demo/README.md", entry_node: "programme:demo", coverage: "DETAILED", corpus_roots: ["demo"], includes: [], excludes: [] }
  const collection = { schema_version: "research-collection/v1", collection_id: "research-collection:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: "ontology/collection.json", default_graph: "demo", graphs: [descriptor], quick_answers: [], reading_paths: [], coverage_ledger: [] }
  const graph = { schema_version: "research-graph/v1", graph_id: "research-graph:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: descriptor.path, source_inventory: "sources", quick_answers: [], reading_paths: [], node_type_legend: {}, relation_legend: {}, nodes: [{ id: "programme:demo", type: "programme", title: "Demo", summary: "Demo", state: "ACTIVE" }], edges: [], kg_bridges: [] }
  const built = await buildRdfDataset(collection as any, [{ descriptor, graph, validation: {} }] as any, { sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })
  const shapes = await loadStandardShaclShapes(process.cwd())
  const report = await validateRdfDatasetWithShacl(built.dataset, shapes)
  expect(report).toEqual({ schema: "ice-ontology-shacl-report/v1", conforms: true, violations: [] })
  const shaQuad = [...built.dataset].find(
    (quad) =>
      quad.subject.value === built.compatibilityProjectionIri &&
      quad.predicate.value === "urn:ice-orca-dragon:ontology:sha256"
  )
  expect(shaQuad).toBeDefined()
  if (shaQuad !== undefined) built.dataset.delete(shaQuad)
  const invalid = await validateRdfDatasetWithShacl(built.dataset, shapes)
  expect(invalid.conforms).toBe(false)
  expect(invalid.violations).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        focus_node: built.compatibilityProjectionIri,
        path: "urn:ice-orca-dragon:ontology:sha256"
      })
    ])
  )
})
