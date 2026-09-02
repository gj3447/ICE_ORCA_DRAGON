import { expect, it } from "vitest"
import {
  GraphRagEvaluationSuiteError,
  decodeGraphRagEvaluationSuite
} from "../src/graphrag/suite.ts"

const fixture = {
  schema: "ice-graphrag-evaluation-suite/v2",
  id: "fixture-suite",
  title: "Fixture suite",
  description: "Stable graph retrieval locators for a unit test.",
  version: "2026-09-02",
  cases: [
    {
      id: "fixture-case",
      query: "stable locator",
      expectation: "RETRIEVE",
      expected_unit_ids: ["fixture::claim:STABLE"],
      forbidden_unit_ids: ["fixture::claim:UNRELATED"],
      max_first_expected_rank: 3,
      graph: "fixture",
      depth: 1,
      rationale: "The locator is deliberately stable for this parser test."
    }
  ],
  guidance: ["A suite is a retrieval control, not a truth test."]
}

it("decodes a bounded versioned GraphRAG suite", () => {
  const suite = decodeGraphRagEvaluationSuite(JSON.stringify(fixture), "fixture")

  expect(suite.id).toBe("fixture-suite")
  expect(suite.cases[0]).toMatchObject({
    graph: "fixture",
    depth: 1,
    expectation: "RETRIEVE",
    max_first_expected_rank: 3,
    expected_unit_ids: ["fixture::claim:STABLE"]
  })
})

it("rejects schema drift in the suite and its cases", () => {
  expect(() =>
    decodeGraphRagEvaluationSuite(JSON.stringify({ ...fixture, unreviewed: true }), "fixture")
  ).toThrow(GraphRagEvaluationSuiteError)
  expect(() =>
    decodeGraphRagEvaluationSuite(
      JSON.stringify({
        ...fixture,
        cases: [{ ...fixture.cases[0], execution_authority: "never" }]
      }),
      "fixture"
    )
  ).toThrow("unknown field(s): execution_authority")
})

it("requires explicit abstention and retrieval case contracts", () => {
  const abstention = decodeGraphRagEvaluationSuite(
    JSON.stringify({
      ...fixture,
      cases: [
        {
          id: "negative-control",
          query: "zzzxxyy qqqvvv",
          expectation: "ABSTAIN",
          graph: "fixture",
          rationale: "Known absent tokens must abstain."
        }
      ]
    }),
    "fixture"
  )
  expect(abstention.cases[0]).toMatchObject({ expectation: "ABSTAIN" })
  expect(() =>
    decodeGraphRagEvaluationSuite(
      JSON.stringify({
        ...fixture,
        cases: [{ ...fixture.cases[0], max_first_expected_rank: undefined }]
      }),
      "fixture"
    )
  ).toThrow("max_first_expected_rank")
})
