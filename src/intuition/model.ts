/** Strict, non-authoritative source-backed research-navigation cue records. */
export const SCIENTIFIC_INTUITION_FLOW_RELPATH =
  "research/intuition/scientific-intuition-signals.v1.json"

export type IntuitionSourceKind = "PRIMARY_PAPER" | "OFFICIAL_GUIDANCE" | "STANDARD"
export type IntuitionSignalStatus = "CANDIDATE" | "REJECTED" | "RETIRED"
export type IntuitionSignalKind =
  | "MISSING_TYPED_OBJECT"
  | "METHOD_ANALOGY"
  | "SEPARATION_TEST"
  | "DISCRIMINATOR"
export type PrincipalFailureClass =
  | "algebra"
  | "sign/unit"
  | "discretization"
  | "truncation"
  | "solver"
  | "spectrum"
  | "gauge"
  | "inference"

export interface IntuitionCanonicalReference {
  readonly graph: string
  readonly node: string
}

export interface IntuitionSourceReference {
  readonly id: string
  readonly kind: IntuitionSourceKind
  readonly citation: string
  readonly uri: string
  readonly version: string
  readonly retrieved_at_utc: string
  readonly pinpoint: string
  readonly role: string
  readonly boundary: string
  readonly canonical_source?: IntuitionCanonicalReference
}

export type IntuitionTarget = IntuitionCanonicalReference

export interface ScientificIntuitionSignal {
  readonly id: string
  readonly status: IntuitionSignalStatus
  readonly kind: IntuitionSignalKind
  readonly target: IntuitionTarget
  readonly lens: string
  readonly why_relevant: string
  readonly source_refs: ReadonlyArray<string>
  readonly assumptions: ReadonlyArray<string>
  readonly discriminating_observation: string
  readonly stop_condition: string
  readonly principal_failure_class: PrincipalFailureClass
  readonly non_claim: string
  readonly does_not_authorize_execution: true
}

export interface IntuitionStandardsAlignment {
  readonly id: string
  readonly standard: string
  readonly uri: string
  readonly status: string
  readonly boundary: string
}

export interface ScientificIntuitionFlow {
  readonly $schema?: string
  readonly schema_version: "scientific-intuition-flow/v1"
  readonly graph_id: "intuition-flow:gate1"
  readonly title: string
  readonly description: string
  readonly updated_at_utc: string
  readonly authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly standards_alignment: ReadonlyArray<IntuitionStandardsAlignment>
  readonly sources: ReadonlyArray<IntuitionSourceReference>
  readonly signals: ReadonlyArray<ScientificIntuitionSignal>
  readonly boundaries: ReadonlyArray<string>
}

export class ScientificIntuitionFlowError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "ScientificIntuitionFlowError"
  }
}

type JsonRecord = Record<string, unknown>

const forbiddenFields = new Set(["claim", "evidence", "score", "probability", "polarity"])
const sourceKinds = new Set<IntuitionSourceKind>([
  "PRIMARY_PAPER",
  "OFFICIAL_GUIDANCE",
  "STANDARD"
])
const signalStatuses = new Set<IntuitionSignalStatus>(["CANDIDATE", "REJECTED", "RETIRED"])
const signalKinds = new Set<IntuitionSignalKind>([
  "MISSING_TYPED_OBJECT",
  "METHOD_ANALOGY",
  "SEPARATION_TEST",
  "DISCRIMINATOR"
])
const failureClasses = new Set<PrincipalFailureClass>([
  "algebra",
  "sign/unit",
  "discretization",
  "truncation",
  "solver",
  "spectrum",
  "gauge",
  "inference"
])
const dateTime = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/

const record = (value: unknown, label: string): JsonRecord => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new ScientificIntuitionFlowError(`${label} must be an object`)
  }
  return value as JsonRecord
}

const string = (value: unknown, label: string): string => {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new ScientificIntuitionFlowError(`${label} must be a non-empty string`)
  }
  return value
}

const webUri = (value: unknown, label: string): string => {
  const uri = string(value, label)
  try {
    const parsed = new URL(uri)
    if (parsed.protocol !== "https:" && parsed.protocol !== "http:") {
      throw new Error("unsupported protocol")
    }
  } catch {
    throw new ScientificIntuitionFlowError(`${label} must be an absolute HTTP(S) URI`)
  }
  return uri
}

const stringArray = (value: unknown, label: string): ReadonlyArray<string> => {
  if (!Array.isArray(value) || value.length === 0) {
    throw new ScientificIntuitionFlowError(`${label} must be a non-empty string array`)
  }
  return value.map((entry, index) => string(entry, `${label}[${index}]`))
}

const exactKeys = (
  value: JsonRecord,
  allowed: ReadonlyArray<string>,
  label: string
): void => {
  for (const key of Object.keys(value)) {
    if (!allowed.includes(key)) {
      throw new ScientificIntuitionFlowError(`${label} has unknown field '${key}'`)
    }
  }
  for (const key of Object.keys(value)) {
    if (forbiddenFields.has(key)) {
      throw new ScientificIntuitionFlowError(`${label} contains forbidden field '${key}'`)
    }
  }
}

const rejectForbiddenFieldsRecursively = (value: unknown, label: string): void => {
  if (Array.isArray(value)) {
    value.forEach((entry, index) => rejectForbiddenFieldsRecursively(entry, `${label}[${index}]`))
    return
  }
  if (typeof value !== "object" || value === null) return
  for (const [key, entry] of Object.entries(value)) {
    if (forbiddenFields.has(key)) {
      throw new ScientificIntuitionFlowError(`${label} contains forbidden field '${key}'`)
    }
    rejectForbiddenFieldsRecursively(entry, `${label}.${key}`)
  }
}

const truth = (value: unknown, label: string): true => {
  if (value !== true) throw new ScientificIntuitionFlowError(`${label} must be true`)
  return true
}

const canonicalReference = (
  value: unknown,
  label: string
): IntuitionCanonicalReference => {
  const item = record(value, label)
  exactKeys(item, ["graph", "node"], label)
  const graph = string(item.graph, `${label}.graph`)
  const node = string(item.node, `${label}.node`)
  if (!/^[a-z0-9-]+$/.test(graph)) {
    throw new ScientificIntuitionFlowError(`${label}.graph is invalid`)
  }
  if (!/^[a-z_]+:[A-Za-z0-9_.:-]+$/.test(node)) {
    throw new ScientificIntuitionFlowError(`${label}.node is invalid`)
  }
  return { graph, node }
}

const source = (value: unknown, label: string): IntuitionSourceReference => {
  const item = record(value, label)
  exactKeys(
    item,
    [
      "id",
      "kind",
      "citation",
      "uri",
      "version",
      "retrieved_at_utc",
      "pinpoint",
      "role",
      "boundary",
      "canonical_source"
    ],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!/^source-ref:[A-Za-z0-9_.:-]+$/.test(id)) {
    throw new ScientificIntuitionFlowError(`${label}.id must match ^source-ref:`)
  }
  const kind = string(item.kind, `${label}.kind`) as IntuitionSourceKind
  if (!sourceKinds.has(kind)) throw new ScientificIntuitionFlowError(`${label}.kind is invalid`)
  const retrievedAt = string(item.retrieved_at_utc, `${label}.retrieved_at_utc`)
  if (!dateTime.test(retrievedAt)) {
    throw new ScientificIntuitionFlowError(`${label}.retrieved_at_utc must be UTC ISO-8601`)
  }
  return {
    id,
    kind,
    citation: string(item.citation, `${label}.citation`),
    uri: webUri(item.uri, `${label}.uri`),
    version: string(item.version, `${label}.version`),
    retrieved_at_utc: retrievedAt,
    pinpoint: string(item.pinpoint, `${label}.pinpoint`),
    role: string(item.role, `${label}.role`),
    boundary: string(item.boundary, `${label}.boundary`),
    ...(item.canonical_source === undefined
      ? {}
      : {
          canonical_source: canonicalReference(
            item.canonical_source,
            `${label}.canonical_source`
          )
        })
  }
}

const standardsAlignment = (
  value: unknown,
  label: string
): IntuitionStandardsAlignment => {
  const item = record(value, label)
  exactKeys(item, ["id", "standard", "uri", "status", "boundary"], label)
  const id = string(item.id, `${label}.id`)
  if (!/^standard:[A-Za-z0-9_.:-]+$/.test(id)) {
    throw new ScientificIntuitionFlowError(`${label}.id must match ^standard:`)
  }
  return {
    id,
    standard: string(item.standard, `${label}.standard`),
    uri: webUri(item.uri, `${label}.uri`),
    status: string(item.status, `${label}.status`),
    boundary: string(item.boundary, `${label}.boundary`)
  }
}

const signal = (value: unknown, label: string): ScientificIntuitionSignal => {
  const item = record(value, label)
  exactKeys(
    item,
    [
      "id",
      "status",
      "kind",
      "target",
      "lens",
      "why_relevant",
      "source_refs",
      "assumptions",
      "discriminating_observation",
      "stop_condition",
      "principal_failure_class",
      "non_claim",
      "does_not_authorize_execution"
    ],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!/^intuition:[A-Za-z0-9_.:-]+$/.test(id)) {
    throw new ScientificIntuitionFlowError(`${label}.id must match ^intuition:`)
  }
  const status = string(item.status, `${label}.status`) as IntuitionSignalStatus
  if (!signalStatuses.has(status)) throw new ScientificIntuitionFlowError(`${label}.status is invalid`)
  const kind = string(item.kind, `${label}.kind`) as IntuitionSignalKind
  if (!signalKinds.has(kind)) throw new ScientificIntuitionFlowError(`${label}.kind is invalid`)
  const target = canonicalReference(item.target, `${label}.target`)
  const lens = string(item.lens, `${label}.lens`)
  if (!lens.endsWith("?")) {
    throw new ScientificIntuitionFlowError(`${label}.lens must end with '?'`)
  }
  const failure = string(
    item.principal_failure_class,
    `${label}.principal_failure_class`
  ) as PrincipalFailureClass
  if (!failureClasses.has(failure)) {
    throw new ScientificIntuitionFlowError(`${label}.principal_failure_class is invalid`)
  }
  return {
    id,
    status,
    kind,
    target,
    lens,
    why_relevant: string(item.why_relevant, `${label}.why_relevant`),
    source_refs: stringArray(item.source_refs, `${label}.source_refs`),
    assumptions: stringArray(item.assumptions, `${label}.assumptions`),
    discriminating_observation: string(
      item.discriminating_observation,
      `${label}.discriminating_observation`
    ),
    stop_condition: string(item.stop_condition, `${label}.stop_condition`),
    principal_failure_class: failure,
    non_claim: string(item.non_claim, `${label}.non_claim`),
    does_not_authorize_execution: truth(
      item.does_not_authorize_execution,
      `${label}.does_not_authorize_execution`
    )
  }
}

export const decodeScientificIntuitionFlow = (
  sourceText: string,
  label = SCIENTIFIC_INTUITION_FLOW_RELPATH
): ScientificIntuitionFlow => {
  let raw: unknown
  try {
    raw = JSON.parse(sourceText)
  } catch (error) {
    throw new ScientificIntuitionFlowError(`${label} is not valid JSON: ${String(error)}`)
  }
  rejectForbiddenFieldsRecursively(raw, label)
  const flow = record(raw, label)
  exactKeys(
    flow,
    [
      "$schema",
      "schema_version",
      "graph_id",
      "title",
      "description",
      "updated_at_utc",
      "authority",
      "canonical_graph_unchanged",
      "does_not_authorize_execution",
      "standards_alignment",
      "sources",
      "signals",
      "boundaries"
    ],
    label
  )
  if (flow.schema_version !== "scientific-intuition-flow/v1") {
    throw new ScientificIntuitionFlowError(`${label}.schema_version must be scientific-intuition-flow/v1`)
  }
  if (flow.graph_id !== "intuition-flow:gate1") {
    throw new ScientificIntuitionFlowError(`${label}.graph_id must be intuition-flow:gate1`)
  }
  const updatedAt = string(flow.updated_at_utc, `${label}.updated_at_utc`)
  if (!dateTime.test(updatedAt)) {
    throw new ScientificIntuitionFlowError(`${label}.updated_at_utc must be UTC ISO-8601`)
  }
  if (flow.authority !== "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION") {
    throw new ScientificIntuitionFlowError(`${label}.authority is invalid`)
  }
  if (
    !Array.isArray(flow.standards_alignment) ||
    flow.standards_alignment.length !== 4
  ) {
    throw new ScientificIntuitionFlowError(
      `${label}.standards_alignment must contain exactly four entries`
    )
  }
  if (
    !Array.isArray(flow.sources) ||
    flow.sources.length < 1 ||
    flow.sources.length > 128
  ) {
    throw new ScientificIntuitionFlowError(
      `${label}.sources must contain 1 through 128 entries`
    )
  }
  if (
    !Array.isArray(flow.signals) ||
    flow.signals.length < 1 ||
    flow.signals.length > 64
  ) {
    throw new ScientificIntuitionFlowError(
      `${label}.signals must contain 1 through 64 entries`
    )
  }
  return {
    ...(flow.$schema === undefined ? {} : { $schema: string(flow.$schema, `${label}.$schema`) }),
    schema_version: "scientific-intuition-flow/v1",
    graph_id: "intuition-flow:gate1",
    title: string(flow.title, `${label}.title`),
    description: string(flow.description, `${label}.description`),
    updated_at_utc: updatedAt,
    authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
    canonical_graph_unchanged: truth(
      flow.canonical_graph_unchanged,
      `${label}.canonical_graph_unchanged`
    ),
    does_not_authorize_execution: truth(
      flow.does_not_authorize_execution,
      `${label}.does_not_authorize_execution`
    ),
    standards_alignment: flow.standards_alignment.map((entry, index) =>
      standardsAlignment(entry, `${label}.standards_alignment[${index}]`)
    ),
    sources: flow.sources.map((entry, index) =>
      source(entry, `${label}.sources[${index}]`)
    ),
    signals: flow.signals.map((entry, index) =>
      signal(entry, `${label}.signals[${index}]`)
    ),
    boundaries: stringArray(flow.boundaries, `${label}.boundaries`)
  }
}
