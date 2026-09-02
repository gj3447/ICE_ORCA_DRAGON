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
  readonly schema: "ice-evidence-graph-rag-eval/v2"
  readonly total_cases: number
  readonly passed_cases: number
  readonly recall_at_limit: number
  readonly mean_reciprocal_rank: number
  readonly mean_expected_recall: number
  readonly limit: number
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly query: string
    readonly graph: string
    readonly depth: number
    readonly passed: boolean
    readonly expected_unit_ids: ReadonlyArray<string>
    readonly retrieved_unit_ids: ReadonlyArray<string>
    readonly first_expected_rank: number | null
    readonly expected_recall: number
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
    const matchedRanks = entry.expected_unit_ids.flatMap((id) => {
      const position = retrieved.indexOf(id)
      return position < 0 ? [] : [position + 1]
    })
    const firstExpectedRank = matchedRanks.length === 0 ? null : Math.min(...matchedRanks)
    return {
      id: entry.id,
      query: entry.query,
      graph: result.graph,
      depth: result.depth,
      passed: firstExpectedRank !== null,
      expected_unit_ids: entry.expected_unit_ids,
      retrieved_unit_ids: retrieved,
      first_expected_rank: firstExpectedRank,
      expected_recall: matchedRanks.length / entry.expected_unit_ids.length
    }
  })
  const passed = outcomes.filter(({ passed: result }) => result).length
  return {
    schema: "ice-evidence-graph-rag-eval/v2",
    total_cases: outcomes.length,
    passed_cases: passed,
    recall_at_limit: outcomes.length === 0 ? 1 : passed / outcomes.length,
    mean_reciprocal_rank:
      outcomes.length === 0
        ? 1
        : outcomes.reduce(
            (total, entry) => total + (entry.first_expected_rank === null ? 0 : 1 / entry.first_expected_rank),
            0
          ) / outcomes.length,
    mean_expected_recall:
      outcomes.length === 0
        ? 1
        : outcomes.reduce((total, entry) => total + entry.expected_recall, 0) / outcomes.length,
    limit,
    cases: outcomes,
    guidance: [
      "This measures deterministic retrieval of predeclared canonical locators; it does not evaluate scientific truth or model reasoning.",
      "Add only stable, source-backed cases and compare changes against a baseline before changing retrieval weights or corpus coverage."
    ]
  }
}

export interface GraphRagEvaluationDiff {
  readonly schema: "ice-evidence-graph-rag-evaluation-diff/v1"
  readonly base: GraphRagEvalResult
  readonly working_tree: GraphRagEvalResult
  readonly summary: {
    readonly ranking_changed_cases: number
    readonly pass_status_changed_cases: number
    readonly mean_reciprocal_rank_delta: number
    readonly mean_expected_recall_delta: number
  }
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly ranking_changed: boolean
    readonly pass_status_changed: boolean
    readonly added_unit_ids: ReadonlyArray<string>
    readonly removed_unit_ids: ReadonlyArray<string>
    readonly base_first_expected_rank: number | null
    readonly working_tree_first_expected_rank: number | null
  }>
  readonly guidance: ReadonlyArray<string>
}

/** Compares the same fixed suite against a committed graph and the working graph. */
export const diffGraphRagEvaluations = (
  base: GraphRagEvalResult,
  workingTree: GraphRagEvalResult
): GraphRagEvaluationDiff => {
  const baseById = new Map(base.cases.map((entry) => [entry.id, entry]))
  const workingById = new Map(workingTree.cases.map((entry) => [entry.id, entry]))
  const ids = [...new Set([...baseById.keys(), ...workingById.keys()])].sort()
  if (ids.length !== base.cases.length || ids.length !== workingTree.cases.length) {
    throw new Error("GraphRAG evaluations must contain the same unique case ids")
  }
  const cases = ids.map((id) => {
    const before = baseById.get(id)
    const after = workingById.get(id)
    if (before === undefined || after === undefined) {
      throw new Error(`GraphRAG evaluation case '${id}' is missing from one side`)
    }
    const rankingChanged =
      before.retrieved_unit_ids.length !== after.retrieved_unit_ids.length ||
      before.retrieved_unit_ids.some((unitId, index) => unitId !== after.retrieved_unit_ids[index])
    return {
      id,
      ranking_changed: rankingChanged,
      pass_status_changed: before.passed !== after.passed,
      added_unit_ids: after.retrieved_unit_ids.filter(
        (unitId) => !before.retrieved_unit_ids.includes(unitId)
      ),
      removed_unit_ids: before.retrieved_unit_ids.filter(
        (unitId) => !after.retrieved_unit_ids.includes(unitId)
      ),
      base_first_expected_rank: before.first_expected_rank,
      working_tree_first_expected_rank: after.first_expected_rank
    }
  })
  return {
    schema: "ice-evidence-graph-rag-evaluation-diff/v1",
    base,
    working_tree: workingTree,
    summary: {
      ranking_changed_cases: cases.filter(({ ranking_changed }) => ranking_changed).length,
      pass_status_changed_cases: cases.filter(({ pass_status_changed }) => pass_status_changed)
        .length,
      mean_reciprocal_rank_delta:
        workingTree.mean_reciprocal_rank - base.mean_reciprocal_rank,
      mean_expected_recall_delta:
        workingTree.mean_expected_recall - base.mean_expected_recall
    },
    cases,
    guidance: [
      "This reports deterministic retrieval movement for one fixed suite; it does not validate a scientific interpretation or authorize a graph change.",
      "Review every pass-status loss and material rank movement before changing retrieval weights, corpus coverage, or graph records."
    ]
  }
}
