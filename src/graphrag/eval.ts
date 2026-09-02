import type { GraphRagIndex } from "./core.ts"
import { searchGraphRag } from "./core.ts"

interface GraphRagEvalCaseBase {
  readonly id: string
  readonly query: string
  readonly graph?: string | undefined
  readonly depth?: number | undefined
}

export interface GraphRagRetrievalEvalCase extends GraphRagEvalCaseBase {
  readonly expectation: "RETRIEVE"
  readonly expected_unit_ids: ReadonlyArray<string>
  readonly forbidden_unit_ids?: ReadonlyArray<string> | undefined
  readonly max_first_expected_rank: number
}

export interface GraphRagAbstentionEvalCase extends GraphRagEvalCaseBase {
  readonly expectation: "ABSTAIN"
}

export type GraphRagEvalCase = GraphRagRetrievalEvalCase | GraphRagAbstentionEvalCase

export interface GraphRagEvalResult {
  readonly schema: "ice-evidence-graph-rag-eval/v3"
  readonly passed: boolean
  readonly total_cases: number
  readonly passed_cases: number
  readonly retrieval_cases: number
  readonly abstention_cases: number
  readonly recall_at_limit: number
  readonly mean_reciprocal_rank: number
  readonly mean_expected_recall: number
  readonly abstention_accuracy: number
  readonly rank_bound_pass_rate: number
  readonly boundary_violation_cases: number
  readonly invalid_locator_cases: number
  readonly limit: number
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly query: string
    readonly graph: string
    readonly depth: number
    readonly expectation: GraphRagEvalCase["expectation"]
    readonly passed: boolean
    readonly expected_unit_ids: ReadonlyArray<string>
    readonly forbidden_unit_ids: ReadonlyArray<string>
    readonly retrieved_unit_ids: ReadonlyArray<string>
    readonly first_expected_rank: number | null
    readonly expected_recall: number | null
    readonly max_first_expected_rank: number | null
    readonly rank_bound_passed: boolean | null
    readonly forbidden_hits: ReadonlyArray<string>
    readonly unknown_expected_unit_ids: ReadonlyArray<string>
    readonly unknown_forbidden_unit_ids: ReadonlyArray<string>
    readonly abstained: boolean
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
    const expectedUnitIds = entry.expectation === "RETRIEVE" ? entry.expected_unit_ids : []
    const forbiddenUnitIds = entry.expectation === "RETRIEVE"
      ? (entry.forbidden_unit_ids ?? [])
      : []
    const matchedRanks = expectedUnitIds.flatMap((id) => {
      const position = retrieved.indexOf(id)
      return position < 0 ? [] : [position + 1]
    })
    const firstExpectedRank = matchedRanks.length === 0 ? null : Math.min(...matchedRanks)
    const expectedRecall = entry.expectation === "RETRIEVE"
      ? matchedRanks.length / expectedUnitIds.length
      : null
    const rankBoundPassed = entry.expectation === "RETRIEVE"
      ? firstExpectedRank !== null && firstExpectedRank <= entry.max_first_expected_rank
      : null
    const forbiddenHits = forbiddenUnitIds.filter((id) => retrieved.includes(id))
    const unknownExpectedUnitIds = expectedUnitIds.filter(
      (id) => !index.internal.units_by_id.has(id)
    )
    const unknownForbiddenUnitIds = forbiddenUnitIds.filter(
      (id) => !index.internal.units_by_id.has(id)
    )
    const abstained = result.abstention.abstained
    const passed = entry.expectation === "ABSTAIN"
      ? abstained
      : expectedRecall === 1 &&
        rankBoundPassed === true &&
        forbiddenHits.length === 0 &&
        unknownExpectedUnitIds.length === 0 &&
        unknownForbiddenUnitIds.length === 0
    return {
      id: entry.id,
      query: entry.query,
      graph: result.graph,
      depth: result.depth,
      expectation: entry.expectation,
      passed,
      expected_unit_ids: expectedUnitIds,
      forbidden_unit_ids: forbiddenUnitIds,
      retrieved_unit_ids: retrieved,
      first_expected_rank: firstExpectedRank,
      expected_recall: expectedRecall,
      max_first_expected_rank:
        entry.expectation === "RETRIEVE" ? entry.max_first_expected_rank : null,
      rank_bound_passed: rankBoundPassed,
      forbidden_hits: forbiddenHits,
      unknown_expected_unit_ids: unknownExpectedUnitIds,
      unknown_forbidden_unit_ids: unknownForbiddenUnitIds,
      abstained
    }
  })
  const passed = outcomes.filter(({ passed: result }) => result).length
  const retrievalOutcomes = outcomes.filter(({ expectation }) => expectation === "RETRIEVE")
  const abstentionOutcomes = outcomes.filter(({ expectation }) => expectation === "ABSTAIN")
  const totalExpectedLocators = retrievalOutcomes.reduce(
    (total, entry) => total + entry.expected_unit_ids.length,
    0
  )
  const matchedExpectedLocators = retrievalOutcomes.reduce(
    (total, entry) =>
      total + Math.round((entry.expected_recall ?? 0) * entry.expected_unit_ids.length),
    0
  )
  return {
    schema: "ice-evidence-graph-rag-eval/v3",
    passed: passed === outcomes.length,
    total_cases: outcomes.length,
    passed_cases: passed,
    retrieval_cases: retrievalOutcomes.length,
    abstention_cases: abstentionOutcomes.length,
    recall_at_limit:
      totalExpectedLocators === 0 ? 1 : matchedExpectedLocators / totalExpectedLocators,
    mean_reciprocal_rank:
      retrievalOutcomes.length === 0
        ? 1
        : retrievalOutcomes.reduce(
            (total, entry) => total + (entry.first_expected_rank === null ? 0 : 1 / entry.first_expected_rank),
            0
          ) / retrievalOutcomes.length,
    mean_expected_recall:
      retrievalOutcomes.length === 0
        ? 1
        : retrievalOutcomes.reduce((total, entry) => total + (entry.expected_recall ?? 0), 0) /
          retrievalOutcomes.length,
    abstention_accuracy:
      abstentionOutcomes.length === 0
        ? 1
        : abstentionOutcomes.filter(({ abstained }) => abstained).length /
          abstentionOutcomes.length,
    rank_bound_pass_rate:
      retrievalOutcomes.length === 0
        ? 1
        : retrievalOutcomes.filter(({ rank_bound_passed }) => rank_bound_passed === true).length /
          retrievalOutcomes.length,
    boundary_violation_cases: retrievalOutcomes.filter(
      ({ forbidden_hits }) => forbidden_hits.length > 0
    ).length,
    invalid_locator_cases: retrievalOutcomes.filter(
      ({ unknown_expected_unit_ids, unknown_forbidden_unit_ids }) =>
        unknown_expected_unit_ids.length > 0 || unknown_forbidden_unit_ids.length > 0
    ).length,
    limit,
    cases: outcomes,
    guidance: [
      "This measures deterministic retrieval of predeclared canonical locators, rank bounds, forbidden-boundary locators, and explicit abstention; it does not evaluate scientific truth or model reasoning.",
      "Add only stable, source-backed cases and reviewed negative controls, then compare changes against a baseline before changing retrieval weights or corpus coverage."
    ]
  }
}

export interface GraphRagEvaluationDiff {
  readonly schema: "ice-evidence-graph-rag-evaluation-diff/v2"
  readonly base: GraphRagEvalResult
  readonly working_tree: GraphRagEvalResult
  readonly summary: {
    readonly ranking_changed_cases: number
    readonly pass_status_changed_cases: number
    readonly abstention_changed_cases: number
    readonly boundary_status_changed_cases: number
    readonly mean_reciprocal_rank_delta: number
    readonly mean_expected_recall_delta: number
  }
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly ranking_changed: boolean
    readonly pass_status_changed: boolean
    readonly abstention_changed: boolean
    readonly boundary_status_changed: boolean
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
    const boundaryStatusChanged =
      (before.forbidden_hits.length > 0) !== (after.forbidden_hits.length > 0)
    return {
      id,
      ranking_changed: rankingChanged,
      pass_status_changed: before.passed !== after.passed,
      abstention_changed: before.abstained !== after.abstained,
      boundary_status_changed: boundaryStatusChanged,
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
    schema: "ice-evidence-graph-rag-evaluation-diff/v2",
    base,
    working_tree: workingTree,
    summary: {
      ranking_changed_cases: cases.filter(({ ranking_changed }) => ranking_changed).length,
      pass_status_changed_cases: cases.filter(({ pass_status_changed }) => pass_status_changed)
        .length,
      abstention_changed_cases: cases.filter(({ abstention_changed }) => abstention_changed).length,
      boundary_status_changed_cases: cases.filter(({ boundary_status_changed }) =>
        boundary_status_changed
      ).length,
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
