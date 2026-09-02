import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { makeValidationReport, validateGraphSemantics } from "../ontology/core.ts"
import {
  loadResearchCollectionAtRevision,
  loadResearchGraphAtRevision,
  loadValidOntologyCollectionStructure
} from "../ontology/repository.ts"
import {
  buildGraphRagIndex,
  searchGraphRag,
  summarizeGraphRagIndex,
  type GraphRagSearchOptions
} from "./core.ts"
import {
  diffGraphRagEvaluations,
  evaluateGraphRag
} from "./eval.ts"
import { loadGraphRagEvaluationSuite } from "./suite.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const renderSearch = (result: ReturnType<typeof searchGraphRag>): string =>
  [
    `evidence GraphRAG search: ${result.query}`,
    `graph: ${result.graph}; hits: ${result.hits.length}; depth: ${result.depth}`,
    ...(result.abstention.abstained
      ? [`abstained: ${result.abstention.reason}`]
      : [`lexical anchors: ${result.abstention.lexical_anchor_count}`]),
    ...result.hits.flatMap((hit) => [
      `${hit.rank}. [${hit.match}] ${hit.unit.id} — ${hit.unit.title}`,
      `   score=${hit.scores.combined.toFixed(4)} community=${hit.community_id}`,
      `   ${hit.unit.source_locator === undefined ? "canonical ontology node" : JSON.stringify(hit.unit.source_locator)}`
    ]),
    "boundary: retrieval context only; inspect primary sources and raw results before interpretation"
  ].join("\n")

export const graphRagIndexData = Effect.gen(function* () {
  const { graphs } = yield* loadValidOntologyCollectionStructure
  return buildGraphRagIndex(graphs)
})

export const graphRagSummaryData = graphRagIndexData.pipe(
  Effect.map(summarizeGraphRagIndex)
)

const graphRagIndexAtRevisionData = (base: string) =>
  Effect.gen(function* () {
    const collection = yield* loadResearchCollectionAtRevision(base)
    const graphs = yield* Effect.forEach(
      collection.graphs,
      (descriptor) =>
        loadResearchGraphAtRevision(base, descriptor.path).pipe(
          Effect.flatMap((graph) => {
            const validation = makeValidationReport(graph, validateGraphSemantics(graph))
            // A revision diff remains useful when its historical graph has a
            // non-retrieval issue (for example, a later-corrected file hash).
            // The current working tree is still required to be valid by
            // graphRagIndexData; record the historical validation separately.
            return Effect.succeed({ descriptor, graph, validation })
          })
        ),
      { concurrency: 4 }
    )
    return {
      index: buildGraphRagIndex(graphs),
      validation: graphs.map(({ descriptor, validation }) => ({
        graph: descriptor.key,
        valid: validation.valid,
        error_codes: validation.errors.map(({ code }) => code)
      }))
    }
  })

export const graphRagSearchData = (
  query: string,
  options: GraphRagSearchOptions = {}
) =>
  graphRagIndexData.pipe(
    Effect.flatMap((index) =>
      Effect.try({
        try: () => searchGraphRag(index, query, options),
        catch: (error) =>
          iceError(
            "GRAPH_RAG_SEARCH_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const graphRagEvaluateData = (limit: number) =>
  Effect.all({ index: graphRagIndexData, loadedSuite: loadGraphRagEvaluationSuite }).pipe(
    Effect.flatMap(({ index, loadedSuite }) =>
      Effect.try({
        try: () => ({
          schema: "ice-graphrag-evaluation-report/v1" as const,
          contract: index.contract,
          suite: {
            id: loadedSuite.suite.id,
            title: loadedSuite.suite.title,
            version: loadedSuite.suite.version,
            provenance: loadedSuite.provenance
          },
          evaluation: evaluateGraphRag(index, loadedSuite.suite.cases, limit),
          guidance: loadedSuite.suite.guidance
        }),
        catch: (error) =>
          iceError(
            "GRAPH_RAG_EVALUATION_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const graphRagDiffData = (base: string, limit: number) =>
  Effect.all({
    baseLoaded: graphRagIndexAtRevisionData(base),
    workingIndex: graphRagIndexData,
    loadedSuite: loadGraphRagEvaluationSuite
  }).pipe(
    Effect.flatMap(({ baseLoaded, workingIndex, loadedSuite }) =>
      Effect.try({
        try: () => ({
          schema: "ice-graphrag-revision-diff/v1" as const,
          base,
          suite: {
            id: loadedSuite.suite.id,
            title: loadedSuite.suite.title,
            version: loadedSuite.suite.version,
            provenance: loadedSuite.provenance
          },
          index: {
            base: summarizeGraphRagIndex(baseLoaded.index),
            working_tree: summarizeGraphRagIndex(workingIndex)
          },
          base_validation: baseLoaded.validation,
          evaluation: diffGraphRagEvaluations(
            evaluateGraphRag(baseLoaded.index, loadedSuite.suite.cases, limit),
            evaluateGraphRag(workingIndex, loadedSuite.suite.cases, limit)
          ),
          guidance: [
            "This is a read-only comparison of one committed ontology revision and the working tree using the current fixed suite.",
            "A retrieval rank or pass change requires human graph review; it neither changes a claim nor authorizes work."
          ]
        }),
        catch: (error) =>
          iceError(
            "GRAPH_RAG_REVISION_DIFF_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const graphRagSummaryCommand = (json: boolean) =>
  graphRagSummaryData.pipe(
    Effect.tap((summary) =>
      json ? printJson(summary) : Console.log(JSON.stringify(summary, null, 2))
    )
  )

export const graphRagSearchCommand = (
  query: string,
  options: GraphRagSearchOptions,
  json: boolean
) =>
  graphRagSearchData(query, options).pipe(
    Effect.tap((result) =>
      json ? printJson(result) : Console.log(renderSearch(result))
    )
  )

export const graphRagEvaluateCommand = (limit: number, json: boolean) =>
  graphRagEvaluateData(limit).pipe(
    Effect.tap((report) =>
      json
        ? printJson(report)
        : Console.log(
            [
              `GraphRAG evaluation suite: ${report.suite.id} (${report.suite.version})`,
              `passed: ${report.evaluation.passed_cases}/${report.evaluation.total_cases}`,
              `locator recall@${report.evaluation.limit}: ${report.evaluation.recall_at_limit.toFixed(3)}`,
              `MRR: ${report.evaluation.mean_reciprocal_rank.toFixed(3)}`,
              `abstention accuracy: ${report.evaluation.abstention_accuracy.toFixed(3)}`,
              `boundary violations: ${report.evaluation.boundary_violation_cases}`,
              `invalid suite locators: ${report.evaluation.invalid_locator_cases}`,
              "boundary: retrieval regression only; inspect graph context and sources manually"
            ].join("\n")
          )
    )
  )

export const graphRagDiffCommand = (base: string, limit: number, json: boolean) =>
  graphRagDiffData(base, limit).pipe(
    Effect.tap((report) =>
      json
        ? printJson(report)
        : Console.log(
            [
              `GraphRAG revision diff: ${report.base} -> working-tree`,
              `suite: ${report.suite.id} (${report.suite.version})`,
              `ranking changes: ${report.evaluation.summary.ranking_changed_cases}`,
              `pass-status changes: ${report.evaluation.summary.pass_status_changed_cases}`,
              `abstention changes: ${report.evaluation.summary.abstention_changed_cases}`,
              `boundary-status changes: ${report.evaluation.summary.boundary_status_changed_cases}`,
              `MRR delta: ${report.evaluation.summary.mean_reciprocal_rank_delta.toFixed(3)}`,
              "boundary: review-only; rank movement does not authorize a graph or research change"
            ].join("\n")
          )
    )
  )
