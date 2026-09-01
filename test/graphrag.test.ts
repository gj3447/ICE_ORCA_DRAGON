import { expect, it } from "vitest"
import { type CollectionGraph } from "../src/ontology/collection-core.ts"
import { makeValidationReport } from "../src/ontology/core.ts"
import { type ResearchGraph } from "../src/ontology/model.ts"
import {
  buildGraphRagIndex,
  searchGraphRag
} from "../src/graphrag/core.ts"
import { evaluateGraphRag } from "../src/graphrag/eval.ts"

const fixture = (): CollectionGraph => {
  const graph: ResearchGraph = {
    schema_version: "research-graph/v1",
    graph_id: "research-graph:graphrag-test",
    title: "GraphRAG fixture",
    description: "A minimal deterministic evidence graph.",
    updated_at_utc: "2026-09-01T00:00:00Z",
    canonical_file: "ontology/graphrag-test/graph.json",
    source_inventory: "ontology/graphrag-test/sources.md",
    quick_answers: [],
    reading_paths: [],
    node_type_legend: { claim: "claim", evidence: "evidence", source: "source" },
    relation_legend: {
      HAS_EVIDENCE: "claim has evidence",
      DEFINED_IN: "evidence is defined in source"
    },
    nodes: [
      {
        id: "claim:ORBIT",
        type: "claim",
        title: "Bounded orbital claim",
        summary: "An orbital constraint remains a review question.",
        state: "SUPPORTED",
        claim_id: "ORBIT",
        statement: "The orbital bound is recorded by the evidence node.",
        epistemic_state: "SUPPORTED"
      },
      {
        id: "evidence:ORBIT",
        type: "evidence",
        title: "Orbital measurement evidence",
        summary: "A finite numerical measurement with a stated control.",
        state: "VERIFIED",
        observed_status: "PASS",
        check_ids: ["orbit-control"]
      },
      {
        id: "source:ORBIT",
        type: "source",
        title: "Primary orbital source",
        summary: "Primary source locator for the measurement.",
        state: "TRACKED",
        citation: "Example et al. (2026)",
        uri: "https://example.test/orbit",
        version: "2026-09-01"
      }
    ],
    edges: [
      {
        id: "edge:1",
        from: "claim:ORBIT",
        relation: "HAS_EVIDENCE",
        to: "evidence:ORBIT",
        polarity: "SUPPORTS"
      },
      {
        id: "edge:2",
        from: "evidence:ORBIT",
        relation: "DEFINED_IN",
        to: "source:ORBIT"
      }
    ],
    kg_bridges: []
  }
  return {
    descriptor: {
      key: "graphrag-test",
      graph_id: graph.graph_id,
      path: graph.canonical_file,
      guide: "ontology/graphrag-test/README.md",
      entry_node: "claim:ORBIT",
      coverage: "PARTIAL",
      corpus_roots: ["research/graphrag-test"],
      includes: ["fixture"],
      excludes: ["execution"]
    },
    graph,
    validation: makeValidationReport(graph, [])
  }
}

it("preserves canonical locators and bounded relation breadcrumbs", () => {
  const index = buildGraphRagIndex([fixture()])
  const result = searchGraphRag(index, "orbital bound", { depth: 2, limit: 6 })
  const source = result.hits.find(({ unit }) => unit.id === "graphrag-test::source:ORBIT")

  expect(index.contract.model_extracted_entities).toBe(false)
  expect(index.units).toHaveLength(3)
  expect(source).toMatchObject({
    match: "GRAPH_EXPANSION",
    distance: 2,
    traversed_edges: [{ relation: "HAS_EVIDENCE" }, { relation: "DEFINED_IN" }],
    unit: {
      source_locator: { kind: "source", uri: "https://example.test/orbit" }
    }
  })
  expect(result.guidance.join(" ")).toContain("neither authorizes execution")
})

it("has deterministic communities and a declared retrieval evaluation boundary", () => {
  const first = buildGraphRagIndex([fixture()])
  const second = buildGraphRagIndex([fixture()])
  const evaluation = evaluateGraphRag(
    first,
    [
      {
        id: "orbit-source-path",
        query: "orbital bound",
        expected_unit_ids: ["graphrag-test::source:ORBIT"],
        depth: 2
      }
    ],
    6
  )

  expect(first.communities).toEqual(second.communities)
  expect(evaluation.recall_at_limit).toBe(1)
  expect(evaluation.guidance.join(" ")).toContain("does not evaluate scientific truth")
})
