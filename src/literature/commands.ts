import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import {
  OpenAlexSearchError,
  getOpenAlexWorkNeighborhood,
  searchOpenAlexWorks,
  type OpenAlexSearchResult,
  type OpenAlexWorkNeighborhood
} from "./openalex.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const renderWork = (work: OpenAlexSearchResult["works"][number]): string =>
  [
    work.title ?? "(untitled)",
    work.publication_date === null ? undefined : `date: ${work.publication_date}`,
    work.doi === null ? undefined : `doi: ${work.doi}`,
    work.source === null ? undefined : `source: ${work.source}`,
    work.cited_by_count === null ? undefined : `cited by: ${work.cited_by_count}`,
    work.authors.length === 0 ? undefined : `authors: ${work.authors.join(", ")}`,
    work.landing_page_url ?? work.open_access_url ?? work.id
  ]
    .filter((line): line is string => line !== undefined)
    .join("\n  ")

const renderSearch = (result: OpenAlexSearchResult): string =>
  [
    `OpenAlex literature search: ${result.query}`,
    `retrieved: ${result.retrieved_at_utc}`,
    `request: ${result.request_url}`,
    `works: ${result.works.length}`,
    ...result.works.flatMap((work, index) => [`${index + 1}. ${renderWork(work)}`]),
    "boundary: discovery metadata only; read the primary source before making a research statement"
  ].join("\n")

export const openAlexSearchCommand = (
  query: string,
  limit: number,
  json: boolean
) =>
  Effect.tryPromise({
    try: () => searchOpenAlexWorks(query, limit),
    catch: (error) =>
      iceError(
        "OPENALEX_SEARCH_FAILED",
        error instanceof OpenAlexSearchError ? error.message : String(error),
        2
      )
  }).pipe(
    Effect.tap((result) =>
      json ? printJson(result) : Console.log(renderSearch(result))
    )
  )

const renderNeighborhood = (result: OpenAlexWorkNeighborhood): string =>
  [
    `OpenAlex citation neighborhood: ${result.target.title ?? result.work_id}`,
    `retrieved: ${result.retrieved_at_utc}`,
    `incoming citations returned: ${result.incoming_citations.length}`,
    `outgoing reference ids returned: ${result.outgoing_reference_ids.length}`,
    `related work ids returned: ${result.related_work_ids.length}`,
    ...result.incoming_citations.flatMap((work, index) => [
      `incoming ${index + 1}. ${renderWork(work)}`
    ]),
    "boundary: discovery metadata only; verify primary sources and citation context"
  ].join("\n")

export const openAlexNeighborhoodCommand = (
  workId: string,
  limit: number,
  json: boolean
) =>
  Effect.tryPromise({
    try: () => getOpenAlexWorkNeighborhood(workId, limit),
    catch: (error) =>
      iceError(
        "OPENALEX_NEIGHBORHOOD_FAILED",
        error instanceof OpenAlexSearchError ? error.message : String(error),
        2
      )
  }).pipe(
    Effect.tap((result) =>
      json ? printJson(result) : Console.log(renderNeighborhood(result))
    )
  )
