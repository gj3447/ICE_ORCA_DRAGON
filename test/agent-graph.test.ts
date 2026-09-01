import { expect, it } from "vitest"
import type { GraphRagHit, GraphRagSearchResult } from "../src/graphrag/core.ts"
import { planResearchAgentWorkflow } from "../src/agent-graph/core.ts"
import { evaluateResearchAgentRouting } from "../src/agent-graph/eval.ts"

const hit = (nodeId: string, title: string): GraphRagHit => ({
  unit: {
    id: `cpt::${nodeId}`,
    graph: "cpt",
    node_id: nodeId,
    node_type: "open_problem",
    state: "OPEN",
    title,
    text: `${title}\n${nodeId}`
  },
  rank: 1,
  match: "DIRECT_HYBRID",
  distance: 0,
  scores: {
    bm25: 1,
    lexical_hash_vector: 1,
    graph_expansion: 0,
    combined: 2
  },
  traversed_edges: [],
  community_id: "cpt:community:fixture"
})

const retrieval = (hits: ReadonlyArray<GraphRagHit> = []): GraphRagSearchResult =>
  ({
    schema: "ice-evidence-graph-rag-search/v1",
    contract: {
      schema: "ice-evidence-graph-rag/v1",
      mode: "DETERMINISTIC_EVIDENCE_FIRST_HUMAN_DIRECTED",
      source_of_truth: "REPOSITORY_ONTOLOGY_JSON",
      model_extracted_entities: false,
      automatic_follow_up: false,
      execution_authorization: "NOT_GRANTED"
    },
    query: "bounded evidence",
    graph: "cpt",
    limit: 12,
    depth: 1,
    index: {
      text_units: 1,
      communities: 1,
      retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion"
    },
    hits,
    communities: [],
    guidance: []
  })

it("creates a durable checkpoint without automatic execution or persistence", () => {
  const first = planResearchAgentWorkflow("Which source constrains the bound?", retrieval())
  const second = planResearchAgentWorkflow("Which source constrains the bound?", retrieval())

  expect(first.checkpoint).toEqual(second.checkpoint)
  expect(first.contract.automatic_follow_up).toBe(false)
  expect(first.contract.execution_authorization).toBe("NOT_GRANTED")
  expect(first.contract.core_progress_authorization).toBe("NOT_GRANTED")
  expect(first.checkpoint.state).toBe("AWAITING_HUMAN_REVIEW")
  expect(first.objective_routing.classification).toBe(
    "INSUFFICIENT_ROUTE_EVIDENCE"
  )
  expect(first.objective_routing.decision).toBe("STOP_OR_REFRAME")
  expect(first.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "NOT_AUTHORIZED"
  )
  expect(first.steps.find(({ id }) => id === "execution")?.state).toBe("NOT_AUTHORIZED")
  expect(first.guidance.join(" ")).toContain("does not persist it automatically")

  const evaluation = evaluateResearchAgentRouting(first)
  expect(evaluation.passed).toBe(true)
  expect(evaluation.checks).toHaveLength(11)
  expect(evaluation.guidance.join(" ")).toContain("not scientific correctness")
})

it("routes only a specifically anchored Gate 1 question to blocker review", () => {
  const gateOne = "open:gate1-original-cycle-signed-global-intersections"
  const plan = planResearchAgentWorkflow(
    "Gate 1 original joint cycle and signed global intersection vector",
    retrieval([hit(gateOne, "Gate 1 original cycle and signed global intersections")])
  )

  expect(plan.objective_routing.classification).toBe("CURRENT_BLOCKER_CANDIDATE")
  expect(plan.objective_routing.selected_lane_id).toBe("G1")
  expect(plan.objective_routing.retrieved_anchor_ids).toEqual([gateOne])
  expect(plan.objective_routing.anti_meandering.passed).toBe(true)
  expect(plan.objective_routing.core_progress_eligibility).toBe(
    "HUMAN_REVIEW_REQUIRED"
  )
  expect(plan.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "HUMAN_REVIEW_REQUIRED"
  )
  expect(evaluateResearchAgentRouting(plan).passed).toBe(true)
})

it("does not trust an explicitly typed anchor that retrieval did not return", () => {
  const plan = planResearchAgentWorkflow(
    "open:gate1-original-cycle-signed-global-intersections",
    retrieval()
  )

  expect(plan.objective_routing.classification).toBe(
    "INSUFFICIENT_ROUTE_EVIDENCE"
  )
  expect(plan.objective_routing.decision).toBe("STOP_OR_REFRAME")
  expect(plan.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "NOT_AUTHORIZED"
  )
})

it("blocks a downstream Gate 4 question behind its typed prerequisites", () => {
  const gateFour = "open:gate4-spinorial-charge-domain-constraint-closure"
  const plan = planResearchAgentWorkflow(
    "Gate 4 common domain and anomaly free constraint closure",
    retrieval([hit(gateFour, "Gate 4 common domain and constraint closure")])
  )

  expect(plan.objective_routing.classification).toBe("DOWNSTREAM_BLOCKED")
  expect(plan.objective_routing.required_prerequisite_gate_ids).toEqual([
    "G1",
    "G2",
    "G3"
  ])
  expect(plan.objective_routing.decision).toBe("STOP_OR_REFRAME")
  expect(plan.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "NOT_AUTHORIZED"
  )
  expect(evaluateResearchAgentRouting(plan).passed).toBe(true)
})

it("stops when the retrieval graph does not match the CPT route profile", () => {
  const source = retrieval([
    hit(
      "open:gate1-original-cycle-signed-global-intersections",
      "Gate 1 original cycle and signed global intersections"
    )
  ])
  const plan = planResearchAgentWorkflow(
    "Gate 1 original joint cycle and signed global intersection vector",
    { ...source, graph: "all" }
  )

  expect(plan.objective_routing.classification).toBe("PROFILE_SCOPE_MISMATCH")
  expect(plan.objective_routing.decision).toBe("STOP_OR_REFRAME")
  expect(plan.checkpoint.id).not.toBe(
    planResearchAgentWorkflow(
      "Gate 1 original joint cycle and signed global intersection vector",
      source
    ).checkpoint.id
  )
  expect(plan.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "NOT_AUTHORIZED"
  )
})

it("keeps a Weyl and RAQ enabling lane outside core progress", () => {
  const p4 = "open:raw-c-fixed-box-nonreal-endpoint-certificate"
  const plan = planResearchAgentWorkflow(
    "P4 singular Weyl spectral measure and raw-C RAQ endpoint",
    retrieval([hit(p4, "Raw-C nonreal endpoint certificate")])
  )

  expect(plan.objective_routing.classification).toBe("SUPPORTING_ONLY")
  expect(plan.objective_routing.selected_lane_id).toBe("P4")
  expect(plan.objective_routing.core_progress_eligibility).toBe("NOT_ELIGIBLE")
  expect(plan.steps.find(({ id }) => id === "calculation_design")?.state).toBe(
    "NOT_AUTHORIZED"
  )
})

it("rejects a plan mutation that bypasses a blocked route", () => {
  const base = planResearchAgentWorkflow(
    "Gate 4 common domain and anomaly free constraint closure",
    retrieval([
      hit(
        "open:gate4-spinorial-charge-domain-constraint-closure",
        "Gate 4 common domain and constraint closure"
      )
    ])
  )
  const mutated = {
    ...base,
    steps: base.steps.map((step) =>
      step.id === "calculation_design"
        ? { ...step, state: "HUMAN_REVIEW_REQUIRED" as const }
        : step
    )
  }

  const evaluation = evaluateResearchAgentRouting(mutated)
  expect(evaluation.passed).toBe(false)
  expect(
    evaluation.checks.find(
      ({ id }) => id === "noncritical-route-cannot-design-calculation"
    )?.passed
  ).toBe(false)
})
