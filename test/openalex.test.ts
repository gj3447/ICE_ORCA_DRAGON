import { expect, it } from "vitest"
import {
  OpenAlexSearchError,
  searchOpenAlexWorks
} from "../src/literature/openalex.ts"

it("returns a bounded, time-stamped projection of OpenAlex works", async () => {
  const requested: URL[] = []
  const fetcher: typeof fetch = async (input) => {
    requested.push(new URL(input.toString()))
    return new Response(
      JSON.stringify({
        results: [
          {
            id: "https://openalex.org/W1",
            title: "A primary work",
            publication_date: "2026-01-01",
            doi: "https://doi.org/10.1000/example",
            cited_by_count: 4,
            primary_location: {
              landing_page_url: "https://example.test/work",
              source: { display_name: "Example Journal" }
            },
            open_access: { oa_url: "https://example.test/open" },
            authorships: [{ author: { display_name: "Ada Example" } }]
          },
          { title: "missing stable identifier is ignored" }
        ]
      }),
      { status: 200, headers: { "content-type": "application/json" } }
    )
  }

  const result = await searchOpenAlexWorks(" graph engineering ", 2, {
    fetch: fetcher,
    now: () => new Date("2026-09-01T00:00:00.000Z")
  })

  expect(requested[0]?.searchParams.get("search")).toBe("graph engineering")
  expect(requested[0]?.searchParams.get("per-page")).toBe("2")
  expect(result).toMatchObject({
    schema: "ice-openalex-search/v1",
    query: "graph engineering",
    retrieved_at_utc: "2026-09-01T00:00:00.000Z",
    works: [
      {
        id: "https://openalex.org/W1",
        title: "A primary work",
        authors: ["Ada Example"]
      }
    ]
  })
  expect(result.works).toHaveLength(1)
})

it("rejects invalid OpenAlex requests before they leave the process", async () => {
  await expect(searchOpenAlexWorks("", 1)).rejects.toBeInstanceOf(
    OpenAlexSearchError
  )
  await expect(searchOpenAlexWorks("valid", 21)).rejects.toMatchObject({
    message: "limit must be an integer from 1 through 20"
  })
})

it("reports an upstream non-success response without treating it as evidence", async () => {
  const fetcher: typeof fetch = async () => new Response("busy", { status: 503 })
  await expect(searchOpenAlexWorks("valid", 1, { fetch: fetcher })).rejects.toMatchObject({
    message: "OpenAlex request failed with HTTP 503"
  })
})
