const OPENALEX_WORKS_URL = "https://api.openalex.org/works"
const OPENALEX_TIMEOUT_MS = 10_000
const MAX_QUERY_LENGTH = 500
export const MAX_OPENALEX_RESULTS = 20
const MAX_AUTHORS_PER_WORK = 20

export class OpenAlexSearchError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "OpenAlexSearchError"
  }
}

export interface OpenAlexWork {
  readonly id: string
  readonly title: string | null
  readonly publication_date: string | null
  readonly doi: string | null
  readonly cited_by_count: number | null
  readonly source: string | null
  readonly landing_page_url: string | null
  readonly open_access_url: string | null
  readonly authors: ReadonlyArray<string>
}

export interface OpenAlexSearchResult {
  readonly schema: "ice-openalex-search/v1"
  readonly provider: "OpenAlex"
  readonly query: string
  readonly limit: number
  readonly retrieved_at_utc: string
  readonly request_url: string
  readonly works: ReadonlyArray<OpenAlexWork>
  readonly guidance: ReadonlyArray<string>
}

export interface OpenAlexSearchOptions {
  readonly fetch?: typeof fetch
  readonly now?: () => Date
}

type JsonRecord = Readonly<Record<string, unknown>>

const asRecord = (value: unknown): JsonRecord | undefined =>
  typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as JsonRecord)
    : undefined

const asString = (value: unknown): string | null =>
  typeof value === "string" && value.length > 0 ? value : null

const asNumber = (value: unknown): number | null =>
  typeof value === "number" && Number.isFinite(value) ? value : null

const readAuthors = (value: unknown): ReadonlyArray<string> => {
  if (!Array.isArray(value)) return []
  return value.flatMap((authorship) => {
    const author = asRecord(asRecord(authorship)?.author)
    const name = asString(author?.display_name)
    return name === null ? [] : [name]
  }).slice(0, MAX_AUTHORS_PER_WORK)
}

const decodeWork = (value: unknown): OpenAlexWork | undefined => {
  const record = asRecord(value)
  if (record === undefined) return undefined
  const id = asString(record.id)
  if (id === null) return undefined
  const primaryLocation = asRecord(record.primary_location)
  const source = asRecord(primaryLocation?.source)
  const openAccess = asRecord(record.open_access)
  return {
    id,
    title: asString(record.title),
    publication_date: asString(record.publication_date),
    doi: asString(record.doi),
    cited_by_count: asNumber(record.cited_by_count),
    source: asString(source?.display_name),
    landing_page_url: asString(primaryLocation?.landing_page_url),
    open_access_url: asString(openAccess?.oa_url),
    authors: readAuthors(record.authorships)
  }
}

const validateQuery = (query: string, limit: number): string => {
  const trimmed = query.trim()
  if (trimmed.length === 0) {
    throw new OpenAlexSearchError("query must not be empty")
  }
  if (trimmed.length > MAX_QUERY_LENGTH) {
    throw new OpenAlexSearchError(
      `query must be at most ${MAX_QUERY_LENGTH} characters`
    )
  }
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > MAX_OPENALEX_RESULTS) {
    throw new OpenAlexSearchError(
      `limit must be an integer from 1 through ${MAX_OPENALEX_RESULTS}`
    )
  }
  return trimmed
}

/**
 * Searches OpenAlex's public works endpoint. This is discovery metadata, not
 * an evidentiary or execution-authorizing research result.
 */
export const searchOpenAlexWorks = async (
  query: string,
  limit: number,
  options: OpenAlexSearchOptions = {}
): Promise<OpenAlexSearchResult> => {
  const normalizedQuery = validateQuery(query, limit)
  const requestUrl = new URL(OPENALEX_WORKS_URL)
  requestUrl.searchParams.set("search", normalizedQuery)
  requestUrl.searchParams.set("per-page", String(limit))
  requestUrl.searchParams.set(
    "select",
    "id,title,publication_date,doi,cited_by_count,primary_location,open_access,authorships"
  )

  const fetcher = options.fetch ?? fetch
  let response: Response
  try {
    response = await fetcher(requestUrl, {
      headers: { accept: "application/json" },
      signal: AbortSignal.timeout(OPENALEX_TIMEOUT_MS)
    })
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    throw new OpenAlexSearchError(`OpenAlex request failed: ${message}`)
  }
  if (!response.ok) {
    throw new OpenAlexSearchError(
      `OpenAlex request failed with HTTP ${response.status}`
    )
  }

  let payload: unknown
  try {
    payload = await response.json()
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    throw new OpenAlexSearchError(`OpenAlex returned invalid JSON: ${message}`)
  }
  const results = asRecord(payload)?.results
  if (!Array.isArray(results)) {
    throw new OpenAlexSearchError("OpenAlex response did not contain a works list")
  }
  const now = options.now ?? (() => new Date())
  return {
    schema: "ice-openalex-search/v1",
    provider: "OpenAlex",
    query: normalizedQuery,
    limit,
    retrieved_at_utc: now().toISOString(),
    request_url: requestUrl.toString(),
    works: results.slice(0, limit).flatMap((work) => {
      const decoded = decodeWork(work)
      return decoded === undefined ? [] : [decoded]
    }),
    guidance: [
      "This is a time-stamped discovery result from OpenAlex, not independent scientific evidence.",
      "Read and cite the relevant primary source before using any work to support a research statement.",
      "A literature search neither authorizes execution nor creates a follow-up task."
    ]
  }
}
