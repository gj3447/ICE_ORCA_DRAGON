import { createHash } from "node:crypto"

export type Json = null | boolean | string | number | JsonObject | JsonArray
export interface JsonObject {
  readonly [key: string]: Json
}
export type JsonArray = ReadonlyArray<Json>

export interface PreparedResource {
  readonly name: string
  readonly role: string
  readonly kind: "kg" | "filesystem"
  readonly locator: string
  /** Independently prepared SHA-256 pin, not copied from an observation. */
  readonly contentHash: string
}

export interface ResearchContextSourceInput {
  readonly question: string
  readonly target: string
  readonly resources: ReadonlyArray<PreparedResource>
}

export interface HswmRequestInput {
  readonly source: string
  readonly plan: JsonObject
  readonly report: JsonObject
  readonly preparedResources: ReadonlyArray<PreparedResource>
  readonly now?: number
}

const NAMESPACE = "ice.research.context"
const MAX_AGE_SECONDS = 120
const SHA256 = /^(?:sha256:)?([0-9a-f]{64})$/
const IDENTIFIER = /^[A-Za-z_][A-Za-z0-9_]*$/

export const asJsonObject = (value: unknown): JsonObject | undefined =>
  typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as JsonObject)
    : undefined

const text = (value: unknown, label: string): string => {
  if (typeof value !== "string" || value.length === 0) throw new Error(`${label} must be a non-empty string`)
  return value
}

const digest = (value: string, label: string): string => {
  const match = SHA256.exec(value)
  if (match === null) throw new Error(`${label} must be a SHA-256 digest`)
  return match[1]!
}

const sha256 = (value: string): string =>
  createHash("sha256").update(value, "utf8").digest("hex")

const quote = (value: string): string => JSON.stringify(value)

const validateResources = (resources: ReadonlyArray<PreparedResource>): void => {
  if (resources.length < 2) throw new Error("USL meaning requires at least two resources")
  const names = new Set<string>()
  const roles = new Set<string>()
  for (const resource of resources) {
    text(resource.name, "resource.name")
    text(resource.role, "resource.role")
    text(resource.locator, "resource.locator")
    if (!IDENTIFIER.test(resource.name) || !IDENTIFIER.test(resource.role)) {
      throw new Error("resource names and roles must be USL identifiers")
    }
    if (resource.kind !== "kg" && resource.kind !== "filesystem") throw new Error("resource.kind is invalid")
    digest(resource.contentHash, `resource '${resource.name}' contentHash`)
    if (names.has(resource.name) || roles.has(resource.role)) throw new Error("resource names and roles must be unique")
    names.add(resource.name)
    roles.add(resource.role)
  }
}

/** Emit real USL v0.1 source; compilation and observation remain external IO. */
export const buildResearchContextSource = (input: ResearchContextSourceInput): string => {
  text(input.question, "question")
  const target = text(input.target, "target")
  if (target.split("::").filter(Boolean).length !== 2) throw new Error("target must be graph-qualified as graph::node")
  validateResources(input.resources)
  const params = input.resources.map((item) => `${item.role}: ${item.kind}`).join(", ")
  const roles = input.resources.map((item) => item.role).join(", ")
  const bindings = input.resources.map((item) => `${item.role}: ${item.name}`).join(", ")
  const description = `Question: ${input.question} Target: ${target}. Scoped read-only context is relevant for investigation, not evidence or semantic truth.`
  return [
    'usl "0.1";',
    `namespace ${quote(NAMESPACE)};`,
    ...input.resources.map((item) => `resource ${item.name} = ${quote(item.locator)};`),
    `meaning scoped_read_only_context(${params}) = ${quote(description)}`,
    '  applies "descriptive read-only investigation context"',
    `  check references_resolve(${roles}) = "all role references are descriptive and NOT_EXECUTED";`,
    `link research = scoped_read_only_context(${bindings});`,
    ""
  ].join("\n")
}

const compareCodePoints = (left: string, right: string): number => {
  const a = Array.from(left)
  const b = Array.from(right)
  for (let index = 0; index < Math.min(a.length, b.length); index += 1) {
    const difference = a[index]!.codePointAt(0)! - b[index]!.codePointAt(0)!
    if (difference !== 0) return difference
  }
  return a.length - b.length
}

const canonicalJson = (value: Json): string => {
  if (value === null || typeof value === "boolean" || typeof value === "string") return JSON.stringify(value)
  if (typeof value === "number") {
    if (!Number.isSafeInteger(value)) throw new Error("canonical HSWM JSON permits safe integers only")
    return JSON.stringify(value)
  }
  if (Array.isArray(value)) return `[${value.map((item) => canonicalJson(item as Json)).join(",")}]`
  const object = value as JsonObject
  return `{${Object.keys(object).sort(compareCodePoints).map((key) => `${JSON.stringify(key)}:${canonicalJson(object[key]!)}`).join(",")}}`
}

export const canonicalJsonSha256 = (value: Json): string =>
  createHash("sha256").update(canonicalJson(value), "utf8").digest("hex")

const objects = (value: Json | undefined, label: string): ReadonlyArray<JsonObject> => {
  if (!Array.isArray(value)) throw new Error(`${label} must be an array`)
  return value.map((item, index) => {
    const object = asJsonObject(item)
    if (object === undefined) throw new Error(`${label}[${index}] must be an object`)
    return object
  })
}

const planLocator = (value: JsonObject): string | undefined => {
  if (value.kind === "kg" && typeof value.source === "string" && typeof value.uid === "string") {
    return `kg://${value.source}/${value.uid}`
  }
  if (value.kind === "filesystem" && typeof value.host === "string" && typeof value.path === "string") {
    return `file://${value.host}${value.path}`
  }
  return undefined
}

const validatePlan = (plan: JsonObject, resources: ReadonlyArray<PreparedResource>): string => {
  if (plan.schema !== "usl-semantic-plan/v1" || plan.namespace !== NAMESPACE) throw new Error("unexpected compiled USL plan")
  const planResources = objects(plan.resources, "plan.resources")
  if (planResources.length !== resources.length) throw new Error("compiled plan resource count does not match")
  for (const [index, resource] of planResources.entries()) {
    const locator = asJsonObject(resource.locator)
    const expected = resources[index]!
    if (locator === undefined || resource.name !== expected.name || locator.kind !== expected.kind || planLocator(locator) !== expected.locator) {
      throw new Error("compiled plan resource order or locator does not match")
    }
  }
  const research = objects(plan.links, "plan.links").find((link) => link.name === "research")
  if (research === undefined) throw new Error("compiled plan has no research link")
  const participants = objects(research.participants, "research.participants")
  if (participants.length !== resources.length || participants.some((item, index) => item.role !== resources[index]!.role || item.resource !== resources[index]!.name)) {
    throw new Error("compiled plan research participant order does not match")
  }
  return sha256(JSON.stringify(plan))
}

const validateReport = (source: string, planDigest: string, report: JsonObject): void => {
  if (report.schema !== "usl-program-observation/v2") throw new Error("unexpected USL observation report")
  if (digest(text(report.sourceDigest, "report.sourceDigest"), "report.sourceDigest") !== sha256(source)) {
    throw new Error("report source digest does not match")
  }
  if (digest(text(report.planDigest, "report.planDigest"), "report.planDigest") !== planDigest) {
    throw new Error("report plan digest does not match")
  }
  if (report.semanticTruth !== "NOT_EVALUATED") throw new Error("report must keep semanticTruth NOT_EVALUATED")
}

/** Build an ICE-owned HSWM v2 request without executing a check. */
export const buildHswmRequest = (input: HswmRequestInput): JsonObject => {
  validateResources(input.preparedResources)
  const uslPlanDigest = validatePlan(input.plan, input.preparedResources)
  validateReport(input.source, uslPlanDigest, input.report)
  const policy: JsonObject = {
    schema_version: "hswm-usl-observation-policy/v2",
    namespace: NAMESPACE,
    plan_digest: canonicalJsonSha256(input.plan),
    usl_plan_digest: `sha256:${uslPlanDigest}`,
    source_digest: `sha256:${sha256(input.source)}`,
    max_age_seconds: MAX_AGE_SECONDS,
    bindings: [{ link: "research", role: "usl", field: "references_resolve" }],
    resources: input.preparedResources.map((resource) => ({
      name: resource.name,
      content_hash: digest(resource.contentHash, `resource '${resource.name}' contentHash`),
      resolved_locator: resource.locator
    }))
  }
  const now = input.now ?? Date.now() / 1000
  return {
    plan: input.plan,
    report: input.report,
    policy,
    preview: {
      domain: [{ role: "usl", field: "references_resolve", values: [false, true] }],
      relation: {
        uid: "ice-research-context-inspection",
        revision: "r1",
        ast: { op: "eq", left: { role: "usl", field: "references_resolve" }, right: true },
        source: "authored:research-context-policy"
      },
      action: "inspect-research-context",
      checks: {
        scope: NAMESPACE,
        expected_scope: NAMESPACE,
        revision: "authored-observation-r1",
        expected_revision: "authored-observation-r1",
        now,
        allowed_reads: [["usl", "references_resolve"]],
        permitted: ["inspect-research-context", "OBSERVE"],
        available: ["inspect-research-context", "OBSERVE"],
        costs: { "inspect-research-context": 1, OBSERVE: 1 },
        budget: 2,
        source: "authored:research-context-usl"
      }
    }
  }
}
