import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import {
  buildGraphRagIndex,
  searchGraphRag,
  summarizeGraphRagIndex,
  type GraphRagSearchOptions
} from "./core.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const renderSearch = (result: ReturnType<typeof searchGraphRag>): string =>
  [
    `evidence GraphRAG search: ${result.query}`,
    `graph: ${result.graph}; hits: ${result.hits.length}; depth: ${result.depth}`,
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
