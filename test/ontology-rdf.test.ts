import { createHash } from "node:crypto"
import { expect, it } from "vitest"
import {
  RDF_CANONICALIZATION_ALGORITHM,
  buildRdfDataset,
  serializeDatasetAsNQuads
} from "../src/ontology/rdf.ts"

const fixture = () => {
  const descriptor = { key: "demo", graph_id: "research-graph:demo", path: "ontology/demo/graph.json", guide: "ontology/demo/README.md", entry_node: "programme:demo", coverage: "DETAILED", corpus_roots: ["demo"], includes: [], excludes: [] }
  const collection = { schema_version: "research-collection/v1", collection_id: "research-collection:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: "ontology/collection.json", default_graph: "demo", graphs: [descriptor], quick_answers: [], reading_paths: [], coverage_ledger: [] }
  const graph = { schema_version: "research-graph/v1", graph_id: "research-graph:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: descriptor.path, source_inventory: "ontology/demo/sources.md", quick_answers: [], reading_paths: [{ id: "reading-path:demo", title: "Demo path", summary: "Ordered", nodes: ["claim:demo", "evidence:demo"] }], node_type_legend: {}, relation_legend: {}, nodes: [{ id: "programme:demo", type: "programme", title: "Demo", summary: "Demo", state: "ACTIVE" }, { id: "claim:demo", type: "claim", claim_id: "DEMO", title: "Claim", summary: "Claim", statement: "Finite fixture claim", epistemic_state: "SUPPORTED", state: "ACTIVE" }, { id: "evidence:demo", type: "evidence", title: "Evidence", summary: "Evidence", state: "VERIFIED", observed_status: "PASS", check_ids: ["demo.check"] }, { id: "artifact:demo", type: "artifact", title: "Artifact", summary: "Artifact", state: "TRACKED", artifact_kind: "result", path: "output/demo.json", sha256: "a".repeat(64) }], edges: [{ id: "edge:demo", from: "claim:demo", relation: "HAS_EVIDENCE", to: "evidence:demo", polarity: "SUPPORTS" }], kg_bridges: [] }
  return { collection: collection as any, graphs: [{ descriptor, graph, validation: {} }] as any, sourceDocuments: [{ path: "ontology/collection.json", sha256: "b".repeat(64) }, { path: descriptor.path, sha256: "c".repeat(64) }] }
}

it("reuses JSON-LD projection while emitting named graphs and PROV export records", async () => {
  expect(RDF_CANONICALIZATION_ALGORITHM).toBe("RDFC-1.0")
  const input = fixture()
  const first = await buildRdfDataset(input.collection, input.graphs, { sourceDocuments: input.sourceDocuments })
  const second = await buildRdfDataset(input.collection, input.graphs, { sourceDocuments: input.sourceDocuments })
  const output = serializeDatasetAsNQuads(first.dataset)
  expect(output).toBe(serializeDatasetAsNQuads(second.dataset))
  expect(output).toContain("urn:ice-orca-dragon:resource:graph:demo")
  expect(output).toContain("urn:ice-orca-dragon:ontology:ProjectionExportActivity")
  expect(output).toContain("urn:ice-orca-dragon:ontology:SourceDocument")
  expect(output).toContain("http://www.w3.org/ns/prov#wasGeneratedBy")
  expect(output).toContain("http://www.w3.org/ns/prov#Entity")
  const graphListLines = output
    .split("\n")
    .filter(
      (line) =>
        line.includes("rdf-syntax-ns#first") &&
        line.includes("graph:demo:node:")
    )
  expect(graphListLines.length).toBeGreaterThan(0)
  expect(
    graphListLines.every((line) =>
      line.includes("<urn:ice-orca-dragon:resource:graph:demo>")
    )
  ).toBe(true)
  expect(output).not.toContain(
    "<urn:ice-orca-dragon:resource:graph:demo:node:claim%3Ademo> <http://www.w3.org/ns/prov#wasDerivedFrom> <urn:ice-orca-dragon:resource:graph:demo:node:evidence%3Ademo>"
  )
  expect(first.compatibilityProjectionSha256).toBe(
    createHash("sha256")
      .update(`${JSON.stringify(first.projection, null, 2)}\n`)
      .digest("hex")
  )
  expect(output).toContain("compatibility-jsonld-projection")
  expect(output).toContain("exact bytes emitted by ontology export --format jsonld")
  await expect(
    buildRdfDataset(input.collection, input.graphs, { sourceDocuments: [] })
  ).rejects.toThrow("requires at least one")
  await expect(
    buildRdfDataset(input.collection, input.graphs, {
      sourceDocuments: [{ path: "../outside.json", sha256: "a".repeat(64) }]
    })
  ).rejects.toThrow("safe repository-relative")
  await expect(
    buildRdfDataset(input.collection, input.graphs, {
      sourceDocuments: [input.sourceDocuments[0]!, input.sourceDocuments[0]!]
    })
  ).rejects.toThrow("duplicated")
})
