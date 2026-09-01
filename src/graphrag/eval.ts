import type { GraphRagIndex } from "./core.ts"
import { searchGraphRag } from "./core.ts"

export interface GraphRagEvalCase {
  readonly id: string
  readonly query: string
  readonly expected_unit_ids: ReadonlyArray<string>
  readonly graph?: string | undefined
  readonly depth?: number | undefined
}

export interface GraphRagEvalResult {
  readonly schema: "ice-evidence-graph-rag-eval/v1"
  readonly total_cases: number
  readonly passed_cases: number
  readonly recall_at_limit: number
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly passed: boolean
    readonly expected_unit_ids: ReadonlyArray<string>
    readonly retrieved_unit_ids: ReadonlyArray<string>
  }>
  readonly guidance: ReadonlyArray<string>
}

/**
 * A deterministic retrieval evaluation. The case author, not a model, fixes
 * expected node locators; callers should add a case only for stable questions.
 */
export const evaluateGraphRag = (
  index: GraphRagIndex,
  cases: ReadonlyArray<GraphRagEvalCase>,
  limit = 8
): GraphRagEvalResult => {
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 50) {
    throw new Error("limit must be an integer from 1 through 50")
  }
  const outcomes = cases.map((entry) => {
    const result = searchGraphRag(index, entry.query, {
      graph: entry.graph,
      depth: entry.depth,
      limit
    })
    const retrieved = result.hits.map(({ unit }) => unit.id)
    return {
      id: entry.id,
      passed: entry.expected_unit_ids.some((id) => retrieved.includes(id)),
      expected_unit_ids: entry.expected_unit_ids,
      retrieved_unit_ids: retrieved
    }
  })
  const passed = outcomes.filter(({ passed: result }) => result).length
  return {
    schema: "ice-evidence-graph-rag-eval/v1",
    total_cases: outcomes.length,
    passed_cases: passed,
    recall_at_limit: outcomes.length === 0 ? 1 : passed / outcomes.length,
    cases: outcomes,
    guidance: [
      "This measures deterministic retrieval of predeclared canonical locators; it does not evaluate scientific truth or model reasoning.",
      "Add only stable, source-backed cases and compare changes against a baseline before changing retrieval weights or corpus coverage."
    ]
  }
}
