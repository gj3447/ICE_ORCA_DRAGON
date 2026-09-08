import { createHash } from "node:crypto"
import { expect, it, vi } from "vitest"
import {
  buildHswmRequest,
  buildResearchContextSource,
  canonicalJsonSha256,
  type JsonObject,
  type PreparedResource
} from "../src/research-context/core.ts"

const sha256 = (value: string): string =>
  createHash("sha256").update(value, "utf8").digest("hex")

const resources: ReadonlyArray<PreparedResource> = [
  { name: "kg_anchor", role: "anchor", kind: "kg", locator: "kg://ice/cpt:gate1", contentHash: "a".repeat(64) },
  { name: "file_carrier", role: "carrier", kind: "filesystem", locator: "file://dev-01/home/ice/carrier.md", contentHash: "b".repeat(64) }
]

const planFor = (): JsonObject => ({
  schema: "usl-semantic-plan/v1",
  namespace: "ice.research.context",
  resources: [
    { name: "kg_anchor", locator: { kind: "kg", source: "ice", uid: "cpt:gate1" } },
    { name: "file_carrier", locator: { kind: "filesystem", host: "dev-01", path: "/home/ice/carrier.md" } }
  ],
  links: [{
    name: "research",
    participants: [{ role: "anchor", resource: "kg_anchor" }, { role: "carrier", resource: "file_carrier" }]
  }]
})

const reportFor = (source: string, plan: JsonObject): JsonObject => ({
  schema: "usl-program-observation/v2",
  sourceDigest: `sha256:${sha256(source)}`,
  planDigest: `sha256:${sha256(JSON.stringify(plan))}`,
  semanticTruth: "NOT_EVALUATED"
})

it("hashes Korean JSON with code-point object-key ordering and retained array ordering", () => {
  const value = { 한글: ["둘", "하나"], a: { "😀": 2, "가": 1 } }
  const expected = sha256('{"a":{"가":1,"😀":2},"한글":["둘","하나"]}')
  expect(canonicalJsonSha256(value)).toBe(expected)
  expect(() => canonicalJsonSha256({ decimal: 1.5 })).toThrow("safe integers")
})

it("uses JSON string quoting for question and locator text in real USL", () => {
  const source = buildResearchContextSource({
    question: '질문"; link escape = nope',
    target: "cpt::open:gate1",
    resources: [{ ...resources[0]!, locator: 'kg://ice/cpt:quoted"\nvalue' }, resources[1]!]
  })
  expect(source).toContain('Question: 질문\\\"; link escape = nope')
  expect(source).toContain('resource kg_anchor = "kg://ice/cpt:quoted\\\"\\nvalue";')
  expect(source).toContain('check references_resolve(anchor, carrier)')
  expect(source).toContain("NOT_EXECUTED")
})

it("binds source and preserved USL plan independently, and never imports report hashes as pins", () => {
  const source = buildResearchContextSource({ question: "질문", target: "cpt::open:gate1", resources })
  const plan = planFor()
  const report = reportFor(source, plan)
  const request = buildHswmRequest({ source, plan, report, preparedResources: resources, now: 7 })
  expect(Object.keys(request)).toEqual(["plan", "report", "policy", "preview"])
  expect((request.preview as JsonObject).action).toBe("inspect-research-context")
  expect((request.preview as JsonObject).role).toBeUndefined()
  expect(((request.preview as JsonObject).domain as readonly JsonObject[])[0]!.role).toBe("usl")
  expect((request.policy as JsonObject).resources).toHaveLength(2)
  expect(() => buildHswmRequest({ source: `${source}// tamper`, plan, report, preparedResources: resources })).toThrow("source digest")
  expect(() => buildHswmRequest({
    source,
    plan: { ...plan, resources: [...(plan.resources as readonly JsonObject[])].reverse() },
    report,
    preparedResources: resources
  })).toThrow("resource order")
  expect(() => buildHswmRequest({ source, plan, report: { ...report, semanticTruth: "EVALUATED" }, preparedResources: resources })).toThrow("NOT_EVALUATED")
  const independentlyRepinned = buildHswmRequest({
    source,
    plan,
    report,
    preparedResources: [{ ...resources[0]!, contentHash: "c".repeat(64) }, resources[1]!]
  })
  expect((((independentlyRepinned.policy as JsonObject).resources as readonly JsonObject[])[0]!).content_hash).toBe("c".repeat(64))
})

it("retains subsecond observation time so a fresh reference cannot appear future-dated", () => {
  const now = vi.spyOn(Date, "now").mockReturnValue(1_789_000_000_321)
  try {
    const source = buildResearchContextSource({ question: "clock boundary", target: "cpt::open:gate1", resources })
    const plan = planFor()
    const request = buildHswmRequest({ source, plan, report: reportFor(source, plan), preparedResources: resources })
    const checks = (request.preview as JsonObject).checks as JsonObject
    expect(checks.now).toBeGreaterThanOrEqual(Date.parse("2026-09-10T00:26:40.321Z") / 1000)
    expect(checks.now).toBe(1_789_000_000.321)
  } finally {
    now.mockRestore()
  }
})
