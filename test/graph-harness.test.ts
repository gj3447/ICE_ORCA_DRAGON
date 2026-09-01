import { expect, it } from "vitest"
import { type CollectionGraph } from "../src/ontology/collection-core.ts"
import { makeValidationReport } from "../src/ontology/core.ts"
import { type ResearchGraph } from "../src/ontology/model.ts"
import {
  graphHarnessContext,
  graphHarnessImpact
} from "../src/harness/core.ts"

const fixture = (): CollectionGraph => {
  const graph: ResearchGraph = {
    schema_version: "research-graph/v1",
    graph_id: "research-graph:harness-test",
    title: "Harness fixture",
    description: "Minimal graph-aware harness fixture",
    updated_at_utc: "2026-09-01T00:00:00Z",
    canonical_file: "ontology/harness-test/graph.json",
    source_inventory: "ontology/harness-test/sources.md",
    quick_answers: [],
    reading_paths: [],
    node_type_legend: {
      claim: "claim",
      evidence: "evidence",
      artifact: "artifact",
      scope: "scope",
      open_problem: "open problem",
      policy: "policy"
    },
    relation_legend: {
      HAS_EVIDENCE: "claim has evidence",
      RECORDED_IN: "evidence recorded in artifact",
      VALID_WITHIN: "claim bounded by scope",
      MOTIVATES: "claim motivates open problem",
      GOVERNED_BY: "claim governed by policy"
    },
    nodes: [
      {
        id: "claim:HARNESS_CONTEXT",
        type: "claim",
        title: "Context is a review input",
        summary: "The graph informs a human decision but does not authorize execution.",
        state: "SUPPORTED",
        claim_id: "HARNESS_CONTEXT",
        statement: "Graph context is review-only.",
        epistemic_state: "SUPPORTED"
      },
      {
        id: "evidence:harness",
        type: "evidence",
        title: "Harness evidence",
        summary: "One fixture observation.",
        state: "VERIFIED",
        observed_status: "PASS"
      },
      {
        id: "artifact:harness",
        type: "artifact",
        title: "Harness result",
        summary: "Hash-tracked fixture result.",
        state: "TRACKED",
        artifact_kind: "result",
        path: "output/harness-result.json",
        sha256: "0".repeat(64)
      },
      {
        id: "scope:harness",
        type: "scope",
        title: "Harness scope",
        summary: "The fixture scope.",
        state: "DECLARED",
        includes: ["fixture"],
        excludes: ["execution authorization"]
      },
      {
        id: "open:harness-review",
        type: "open_problem",
        title: "Human review remains required",
        summary: "No graph traversal can select an experiment by itself.",
        state: "OPEN",
        question: "Which independently scoped question is worth opening?"
      },
      {
        id: "policy:harness",
        type: "policy",
        title: "Harness policy",
        summary: "Fixture policy record.",
        state: "ACTIVE",
        path: "docs/decisions/HARNESS_FIXTURE.md",
        sha256: "1".repeat(64),
        introduced_in_commit: "2".repeat(40)
      }
    ],
    edges: [
      {
        id: "edge:1",
        from: "claim:HARNESS_CONTEXT",
        relation: "HAS_EVIDENCE",
        to: "evidence:harness",
        polarity: "SUPPORTS"
      },
      {
        id: "edge:2",
        from: "evidence:harness",
        relation: "RECORDED_IN",
        to: "artifact:harness"
      },
      {
        id: "edge:3",
        from: "claim:HARNESS_CONTEXT",
        relation: "VALID_WITHIN",
        to: "scope:harness"
      },
      {
        id: "edge:4",
        from: "claim:HARNESS_CONTEXT",
        relation: "MOTIVATES",
        to: "open:harness-review"
      },
      {
        id: "edge:5",
        from: "claim:HARNESS_CONTEXT",
        relation: "GOVERNED_BY",
        to: "policy:harness"
      }
    ],
    kg_bridges: []
  }
  return {
    descriptor: {
      key: "harness-test",
      graph_id: "research-graph:harness-test",
      path: "ontology/harness-test/graph.json",
      guide: "ontology/harness-test/README.md",
      entry_node: "claim:HARNESS_CONTEXT",
      coverage: "PARTIAL",
      corpus_roots: ["research/harness-test"],
      includes: ["fixture"],
      excludes: ["everything else"]
    },
    graph,
    validation: makeValidationReport(graph, [])
  }
}

it("builds bounded graph context without granting execution or a successor", () => {
  const graph = fixture()
  const target = graph.graph.nodes.find(
    (node) => node.id === "claim:HARNESS_CONTEXT"
  )
  if (target === undefined) throw new Error("fixture target is missing")

  const context = graphHarnessContext(graph, target, 1, 64)

  expect(context.contract.automatic_follow_up).toBe(false)
  expect(context.contract.execution_authorization).toBe("NOT_GRANTED")
  expect(context.context.evidence.map(({ id }) => id)).toEqual([
    "evidence:harness"
  ])
  expect(context.context.open_problems.map(({ id }) => id)).toEqual([
    "open:harness-review"
  ])
  expect(context.context.policies.map(({ id }) => id)).toEqual(["policy:harness"])
})

it("maps exact registered paths and keeps unregistered paths non-prescriptive", () => {
  const graph = fixture()
  const registered = graphHarnessImpact(
    [graph],
    "output/harness-result.json",
    2,
    64,
    false
  )
  const unregistered = graphHarnessImpact([graph], "notes/local.md", 1, 64, false)

  expect(registered.registered).toBe(true)
  expect(registered.matches).toMatchObject([
    {
      graph: "harness-test",
      kind: "artifact",
      node: { id: "artifact:harness" }
    }
  ])
  expect(registered.matches[0]?.context?.context.claims.map(({ id }) => id)).toEqual([
    "claim:HARNESS_CONTEXT"
  ])
  expect(unregistered.registered).toBe(false)
  expect(unregistered.guidance.join(" ")).toContain("not evidence")
})

it("keeps a hub context explicitly bounded by its requested node limit", () => {
  const graph = fixture()
  const target = graph.graph.nodes.find(
    (node) => node.id === "claim:HARNESS_CONTEXT"
  )
  if (target === undefined) throw new Error("fixture target is missing")

  const context = graphHarnessContext(graph, target, 1, 2)

  expect(context.available_nodes).toBeGreaterThan(2)
  expect(context.returned_nodes).toBe(2)
  expect(context.truncated).toBe(true)
  expect(context.guidance.join(" ")).toContain("truncated")
})
