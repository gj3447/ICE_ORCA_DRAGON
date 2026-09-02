import { expect, it } from "vitest"
import { type CollectionGraph } from "../src/ontology/collection-core.ts"
import { makeValidationReport } from "../src/ontology/core.ts"
import { type ResearchGraph } from "../src/ontology/model.ts"
import {
  buildGraphRagIndex,
  searchGraphRag
} from "../src/graphrag/core.ts"
import { diffGraphRagEvaluations, evaluateGraphRag } from "../src/graphrag/eval.ts"

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
        expectation: "RETRIEVE",
        expected_unit_ids: ["graphrag-test::source:ORBIT"],
        max_first_expected_rank: 3,
        depth: 2
      }
    ],
    6
  )

  expect(first.communities).toEqual(second.communities)
  expect(evaluation.recall_at_limit).toBe(1)
  expect(evaluation.passed).toBe(true)
  expect(evaluation.cases[0]?.first_expected_rank).toBe(3)
  expect(evaluation.mean_reciprocal_rank).toBeCloseTo(1 / 3, 12)
  expect(evaluation.rank_bound_pass_rate).toBe(1)
  expect(evaluation.guidance.join(" ")).toContain("does not evaluate scientific truth")
})

it("reports rank movement without treating it as a research verdict", () => {
  const index = buildGraphRagIndex([fixture()])
  const cases = [
    {
      id: "orbit-source-path",
      query: "orbital bound",
      expectation: "RETRIEVE" as const,
      expected_unit_ids: ["graphrag-test::source:ORBIT"],
      max_first_expected_rank: 3,
      depth: 2
    }
  ]
  const base = evaluateGraphRag(index, cases, 1)
  const workingTree = evaluateGraphRag(index, cases, 6)
  const diff = diffGraphRagEvaluations(base, workingTree)

  expect(diff.schema).toBe("ice-evidence-graph-rag-evaluation-diff/v2")
  expect(diff.cases).toHaveLength(1)
  expect(diff.guidance.join(" ")).toContain("does not validate a scientific interpretation")
})

it("abstains without a lexical anchor and scores negative and boundary controls", () => {
  const index = buildGraphRagIndex([fixture()])
  const search = searchGraphRag(index, "zzzxxyy qqqvvv", { limit: 6 })
  const evaluation = evaluateGraphRag(
    index,
    [
      {
        id: "unknown-token-abstention",
        query: "zzzxxyy qqqvvv",
        expectation: "ABSTAIN"
      },
      {
        id: "bounded-orbit",
        query: "orbital bound",
        expectation: "RETRIEVE",
        expected_unit_ids: ["graphrag-test::claim:ORBIT"],
        forbidden_unit_ids: ["graphrag-test::source:ORBIT"],
        max_first_expected_rank: 1,
        depth: 0
      }
    ],
    1
  )

  expect(search).toMatchObject({
    schema: "ice-evidence-graph-rag-search/v2",
    abstention: {
      abstained: true,
      reason: "NO_LEXICAL_ANCHOR",
      lexical_anchor_count: 0
    },
    hits: []
  })
  expect(evaluation.passed_cases).toBe(2)
  expect(evaluation.abstention_accuracy).toBe(1)
  expect(evaluation.boundary_violation_cases).toBe(0)
  expect(evaluation.invalid_locator_cases).toBe(0)
})

it("does not let an unknown forbidden locator create a vacuous boundary pass", () => {
  const evaluation = evaluateGraphRag(
    buildGraphRagIndex([fixture()]),
    [
      {
        id: "invalid-negative-control",
        query: "orbital bound",
        expectation: "RETRIEVE",
        expected_unit_ids: ["graphrag-test::claim:ORBIT"],
        forbidden_unit_ids: ["graphrag-test::claim:DOES_NOT_EXIST"],
        max_first_expected_rank: 1,
        depth: 0
      }
    ],
    1
  )

  expect(evaluation.passed_cases).toBe(0)
  expect(evaluation.passed).toBe(false)
  expect(evaluation.invalid_locator_cases).toBe(1)
  expect(evaluation.cases[0]?.unknown_forbidden_unit_ids).toEqual([
    "graphrag-test::claim:DOES_NOT_EXIST"
  ])
})
