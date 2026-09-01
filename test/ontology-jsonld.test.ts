import { expect, it } from "vitest"
import { projectCollectionToJsonLd } from "../src/ontology/jsonld.ts"
import type { CollectionGraph } from "../src/ontology/collection-core.ts"
import type { ResearchCollection } from "../src/ontology/collection.ts"

const collection = {
  schema_version: "research-collection/v1", collection_id: "research-collection:test", title: "Test", description: "Test collection", updated_at_utc: "2026-09-01T00:00:00Z", canonical_file: "ontology/collection.json", default_graph: "one",
  graphs: [
    { key: "one", graph_id: "research-graph:one", path: "ontology/one/graph.json", guide: "ontology/one/README.md", entry_node: "programme:one", coverage: "DETAILED", corpus_roots: ["one"], includes: ["a"], excludes: ["b"] },
    { key: "two", graph_id: "research-graph:two", path: "ontology/two/graph.json", guide: "ontology/two/README.md", entry_node: "programme:two", coverage: "PARTIAL", corpus_roots: ["two"], includes: [], excludes: [] }
  ],
  quick_answers: [], reading_paths: [], coverage_ledger: []
} as unknown as ResearchCollection

const graph = (key: "one" | "two"): CollectionGraph => ({
  descriptor: collection.graphs[key === "one" ? 0 : 1] as CollectionGraph["descriptor"],
  validation: {} as CollectionGraph["validation"],
  graph: {
    schema_version: "research-graph/v1", graph_id: `research-graph:${key}`, title: key, description: key, updated_at_utc: "2026-09-01T00:00:00Z", canonical_file: `ontology/${key}/graph.json`, source_inventory: "sources.md", quick_answers: [],
    reading_paths: [{ id: `reading-path:${key}`, title: "path", summary: "ordered", nodes: ["claim:SAME", "evidence:check"] }],
    node_type_legend: { programme: "programme", claim: "claim", evidence: "evidence" }, relation_legend: { HAS_EVIDENCE: "evidence" },
    nodes: [
      { id: `programme:${key}`, type: "programme", title: key, summary: key, state: "ACTIVE" },
      { id: "claim:SAME", type: "claim", claim_id: "SAME", title: "claim", summary: "claim", statement: "claim", epistemic_state: "SUPPORTED", state: "ACTIVE" },
      { id: "evidence:check", type: "evidence", title: "evidence", summary: "evidence", state: "VERIFIED", observed_status: "PASS", check_ids: ["check.1", "check.2"] }
    ],
    edges: [{ id: "edge:1", from: "claim:SAME", relation: "HAS_EVIDENCE", to: "evidence:check", polarity: "SUPPORTS", note: "kept" }],
    kg_bridges: [{ local_node_id: "claim:SAME", system: "external", external_uid: null, relation: null, status: "UNRESOLVED", checked_at_utc: "2026-09-01T00:00:00Z" }]
  } as CollectionGraph["graph"]
})

it("projects deterministically and namespaces colliding local IDs by graph key", () => {
  const first = projectCollectionToJsonLd(collection, [graph("one"), graph("two")])
  const second = projectCollectionToJsonLd(collection, [graph("one"), graph("two")])
  expect(first).toEqual(second)
  const ids = first["@graph"].map((value) => value["@id"])
  expect(ids).toContain("urn:ice-orca-dragon:resource:graph:one:node:claim%3ASAME")
  expect(ids).toContain("urn:ice-orca-dragon:resource:graph:two:node:claim%3ASAME")
  expect(first["@context"]["@version"]).toBe(1.1)
})

it("reifies edge metadata, preserves ordered lists and unresolved null sentinels", () => {
  const output = projectCollectionToJsonLd(collection, [graph("one")])
  const edge = output["@graph"].find((value) => value["@type"] === "ice:ResearchEdge")
  expect(edge).toMatchObject({ "ice:localId": "edge:1", "ice:relationName": "HAS_EVIDENCE", "ice:polarity": "SUPPORTS", "ice:note": "kept" })
  const path = output["@graph"].find((value) => value["@type"] === "ice:GraphReadingPath")
  expect((path?.["ice:nodes"] as { "@list": Array<{ "@id": string }> })["@list"].map((value) => value["@id"])).toEqual([
    "urn:ice-orca-dragon:resource:graph:one:node:claim%3ASAME", "urn:ice-orca-dragon:resource:graph:one:node:evidence%3Acheck"
  ])
  const bridge = output["@graph"].find((value) => value["@type"] === "ice:KgBridge")
  expect(bridge).toMatchObject({
    "ice:externalUid": { "@id": "ice:NoExternalUid" },
    "ice:relation": { "@id": "ice:NoRelation" },
    "ice:externalUidNull": true,
    "ice:relationNull": true
  })
  const claim = output["@graph"].find((value) =>
    Array.isArray(value["@type"]) && value["@type"].includes("ice:Claim")
  )
  expect(claim).toMatchObject({
    "ice:claimId": "SAME",
    "ice:epistemicState": "SUPPORTED"
  })
})

it("filters graph resources while declaring the selected graph key", () => {
  const output = projectCollectionToJsonLd(collection, [graph("one"), graph("two")], {
    graphKeys: ["two"],
    sourceDocuments: [
      { path: "ontology/collection.json", sha256: "a".repeat(64) },
      { path: "ontology/two/graph.json", sha256: "b".repeat(64) }
    ]
  })
  expect(output["ice:selectedGraphKeys"]).toEqual(["two"])
  expect(output["@graph"].some((value) => value["ice:graphKey"] === "one" && Array.isArray(value["@type"]) && value["@type"].includes("ice:ResearchNode"))).toBe(false)
  expect(output["@graph"].some((value) => value["ice:graphKey"] === "two" && Array.isArray(value["@type"]) && value["@type"].includes("ice:ResearchNode"))).toBe(true)
  expect(output["ice:sourceDocuments"]).toEqual({
    "@type": "@json",
    "@value": [
      { path: "ontology/collection.json", sha256: "a".repeat(64) },
      { path: "ontology/two/graph.json", sha256: "b".repeat(64) }
    ]
  })
})
