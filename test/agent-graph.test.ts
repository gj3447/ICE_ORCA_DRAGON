import { expect, it } from "vitest"
import type { GraphRagSearchResult } from "../src/graphrag/core.ts"
import { planResearchAgentWorkflow } from "../src/agent-graph/core.ts"
import { evaluateResearchAgentRouting } from "../src/agent-graph/eval.ts"

const retrieval = (): GraphRagSearchResult =>
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
    graph: "fixture",
    limit: 12,
    depth: 1,
    index: {
      text_units: 1,
      communities: 1,
      retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion"
    },
    hits: [],
    communities: [],
    guidance: []
  })

it("creates a durable checkpoint without automatic execution or persistence", () => {
  const first = planResearchAgentWorkflow("Which source constrains the bound?", retrieval())
  const second = planResearchAgentWorkflow("Which source constrains the bound?", retrieval())

  expect(first.checkpoint).toEqual(second.checkpoint)
  expect(first.contract.automatic_follow_up).toBe(false)
  expect(first.contract.execution_authorization).toBe("NOT_GRANTED")
  expect(first.checkpoint.state).toBe("AWAITING_HUMAN_REVIEW")
  expect(first.steps.find(({ id }) => id === "execution")?.state).toBe("NOT_AUTHORIZED")
  expect(first.guidance.join(" ")).toContain("does not persist it automatically")

  const evaluation = evaluateResearchAgentRouting(first)
  expect(evaluation.passed).toBe(true)
  expect(evaluation.checks).toHaveLength(6)
  expect(evaluation.guidance.join(" ")).toContain("not scientific correctness")
})
