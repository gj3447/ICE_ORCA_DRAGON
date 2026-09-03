/** Strict decoder for the non-authoritative external-comparator research route. */
export const COMPARATOR_PROTOCOL_RELPATH =
  "research/benchmarks/ice-comparator-protocol.v1.json"

export type ComparatorSourceKind =
  | "PRIMARY_PAPER"
  | "OFFICIAL_COLLABORATION_PAPER"
export type ComparatorModelRole =
  | "CALIBRATION_ONLY"
  | "CANDIDATE_MODEL"
  | "PARALLEL_CLASSIFICATION"
export type ComparatorLane =
  | "GEOMETRY_COMPARATOR"
  | "FOLDED_SUSY_CLASSIFICATION"
export type ComparatorStepKind =
  | "CALIBRATION"
  | "ANALYTIC_AUDIT"
  | "CROSS_DOMAIN_TEST"
  | "ADMISSION_DECISION"
  | "CLASSIFICATION"
export type ComparatorRelation =
  | "CALIBRATES"
  | "PREREQUISITE_FOR"
  | "INFORMS"
  | "INDEPENDENT_PARALLEL_TO"
export type ComparatorFailureClass =
  | "algebra"
  | "sign/unit"
  | "discretization"
  | "truncation"
  | "solver"
  | "spectrum"
  | "gauge"
  | "inference"

export interface ComparatorSourcePin {
  readonly id: string
  readonly kind: ComparatorSourceKind
  readonly citation: string
  readonly uri: string
  readonly version: string
  readonly retrieved_at_utc: string
  readonly pinpoint: string
  readonly role: string
  readonly boundary: string
}

export interface ComparatorToolPin {
  readonly id: string
  readonly name: string
  readonly repository_uri: string
  readonly observed_commit: string
  readonly observed_at_utc: string
  readonly paper_source_ref: string
  readonly role: string
  readonly license_status: string
  readonly installation_status: "NOT_INSTALLED"
  readonly boundary: string
}

export interface ComparatorModel {
  readonly id: string
  readonly role: ComparatorModelRole
  readonly name: string
  readonly action: string
  readonly convention: string
  readonly parameter_lock: string
  readonly matter_coupling: string
  readonly boundary_domain: string
  readonly source_refs: ReadonlyArray<string>
  readonly non_claim: string
}

export interface ComparatorConsumer {
  readonly id: string
  readonly domain: "BACKGROUND" | "SCALAR_GROWTH_LENSING" | "TENSOR_PROPAGATION"
  readonly observable: string
  readonly independence_boundary: string
  readonly non_claim: string
}

export interface ComparatorPlannedObject {
  readonly id: string
  readonly kind: string
  readonly specification: string
  readonly state: "PLANNED"
  readonly not_a_result: true
}

export interface ComparatorContextReference {
  readonly graph: "cpt"
  readonly node: string
  readonly relation: "CONTEXTUALIZES_NONAUTHORITATIVELY"
}

export interface ComparatorStep {
  readonly id: string
  readonly title: string
  readonly kind: ComparatorStepKind
  readonly state: "PLANNED"
  readonly lane: ComparatorLane
  readonly topic_refs: ReadonlyArray<string>
  readonly context_refs: ReadonlyArray<ComparatorContextReference>
  readonly model_refs: ReadonlyArray<string>
  readonly source_refs: ReadonlyArray<string>
  readonly tool_refs: ReadonlyArray<string>
  readonly prerequisite_outputs: ReadonlyArray<string>
  readonly inputs: ReadonlyArray<ComparatorPlannedObject>
  readonly outputs: ReadonlyArray<ComparatorPlannedObject>
  readonly choice_dimensions: ReadonlyArray<string>
  readonly mechanism_object: string
  readonly parameter_lock: string
  readonly consumer_refs: ReadonlyArray<string>
  readonly independent_check: string
  readonly acceptance_criterion: string
  readonly null_outcome: string
  readonly kill_criterion: string
  readonly principal_failure_class: ComparatorFailureClass
  readonly non_claim: string
  readonly does_not_authorize_execution: true
}

export interface ComparatorEdge {
  readonly id: string
  readonly from: string
  readonly relation: ComparatorRelation
  readonly to: string
  readonly rationale: string
  readonly non_claim: string
  readonly does_not_authorize_execution: true
}

export interface ComparatorSelectedStrategy {
  readonly calibration_step: string
  readonly first_comparator_model: string
  readonly cross_domain_step: string
  readonly ice_admission_step: string
  readonly parallel_classification_step: string
  readonly rationale: string
}

export interface IceComparatorProtocol {
  readonly $schema?: string
  readonly schema_version: "ice-comparator-protocol/v1"
  readonly protocol_id: "comparator-protocol:ice-choice-robust-cross-domain"
  readonly title: string
  readonly description: string
  readonly updated_at_utc: string
  readonly authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly result_status: "DESIGN_ONLY"
  readonly selected_strategy: ComparatorSelectedStrategy
  readonly source_pins: ReadonlyArray<ComparatorSourcePin>
  readonly tools: ReadonlyArray<ComparatorToolPin>
  readonly models: ReadonlyArray<ComparatorModel>
  readonly consumers: ReadonlyArray<ComparatorConsumer>
  readonly steps: ReadonlyArray<ComparatorStep>
  readonly edges: ReadonlyArray<ComparatorEdge>
  readonly boundaries: ReadonlyArray<string>
}

export class ComparatorProtocolError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "ComparatorProtocolError"
  }
}

type JsonRecord = Record<string, unknown>

const forbiddenFields = new Set([
  "artifact",
  "result",
  "claim",
  "evidence",
  "score",
  "probability",
  "polarity",
  "canonical_target",
  "execution_command",
  "next_step"
])
const sourceKinds = new Set<ComparatorSourceKind>([
  "PRIMARY_PAPER",
  "OFFICIAL_COLLABORATION_PAPER"
])
const modelRoles = new Set<ComparatorModelRole>([
  "CALIBRATION_ONLY",
  "CANDIDATE_MODEL",
  "PARALLEL_CLASSIFICATION"
])
const lanes = new Set<ComparatorLane>([
  "GEOMETRY_COMPARATOR",
  "FOLDED_SUSY_CLASSIFICATION"
])
const stepKinds = new Set<ComparatorStepKind>([
  "CALIBRATION",
  "ANALYTIC_AUDIT",
  "CROSS_DOMAIN_TEST",
  "ADMISSION_DECISION",
  "CLASSIFICATION"
])
const relations = new Set<ComparatorRelation>([
  "CALIBRATES",
  "PREREQUISITE_FOR",
  "INFORMS",
  "INDEPENDENT_PARALLEL_TO"
])
const failureClasses = new Set<ComparatorFailureClass>([
  "algebra",
  "sign/unit",
  "discretization",
  "truncation",
  "solver",
  "spectrum",
  "gauge",
  "inference"
])
const consumerDomains = new Set<ComparatorConsumer["domain"]>([
  "BACKGROUND",
  "SCALAR_GROWTH_LENSING",
  "TENSOR_PROPAGATION"
])
const utcDateTime = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?Z$/

const isUtcDateTime = (value: string): boolean => {
  const match = utcDateTime.exec(value)
  if (match === null) return false
  const [, yearText, monthText, dayText, hourText, minuteText, secondText] = match
  if (
    yearText === undefined || monthText === undefined || dayText === undefined ||
    hourText === undefined || minuteText === undefined || secondText === undefined
  ) return false
  const year = Number(yearText)
  const month = Number(monthText)
  const day = Number(dayText)
  const hour = Number(hourText)
  const minute = Number(minuteText)
  const second = Number(secondText)
  if (
    month < 1 || month > 12 || day < 1 || day > 31 || hour > 23 ||
    minute > 59 || second > 59
  ) return false
  const calendar = new Date(0)
  calendar.setUTCFullYear(year, month - 1, day)
  calendar.setUTCHours(hour, minute, second, 0)
  return calendar.getUTCFullYear() === year &&
    calendar.getUTCMonth() === month - 1 &&
    calendar.getUTCDate() === day &&
    calendar.getUTCHours() === hour &&
    calendar.getUTCMinutes() === minute &&
    calendar.getUTCSeconds() === second
}

const record = (value: unknown, label: string): JsonRecord => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new ComparatorProtocolError(`${label} must be an object`)
  }
  return value as JsonRecord
}

const string = (value: unknown, label: string): string => {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new ComparatorProtocolError(`${label} must be a non-empty string`)
  }
  return value
}

const stringArray = (
  value: unknown,
  label: string,
  minimum = 1
): ReadonlyArray<string> => {
  if (!Array.isArray(value) || value.length < minimum) {
    throw new ComparatorProtocolError(`${label} must contain at least ${minimum} string entries`)
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
      throw new ComparatorProtocolError(`${label} has unknown field '${key}'`)
    }
  }
}

const rejectForbiddenFields = (value: unknown, label: string): void => {
  if (Array.isArray(value)) {
    value.forEach((entry, index) => rejectForbiddenFields(entry, `${label}[${index}]`))
    return
  }
  if (typeof value !== "object" || value === null) return
  for (const [key, entry] of Object.entries(value)) {
    if (forbiddenFields.has(key)) {
      throw new ComparatorProtocolError(`${label} contains forbidden field '${key}'`)
    }
    rejectForbiddenFields(entry, `${label}.${key}`)
  }
}

const truth = (value: unknown, label: string): true => {
  if (value !== true) throw new ComparatorProtocolError(`${label} must be true`)
  return true
}

const webUri = (value: unknown, label: string): string => {
  const uri = string(value, label)
  if (!/^https?:\/\//.test(uri)) {
    throw new ComparatorProtocolError(`${label} must use a lowercase HTTP(S) scheme`)
  }
  try {
    const parsed = new URL(uri)
    if (parsed.protocol !== "https:" && parsed.protocol !== "http:") {
      throw new Error("unsupported protocol")
    }
  } catch {
    throw new ComparatorProtocolError(`${label} must be an absolute HTTP(S) URI`)
  }
  return uri
}

const enumValue = <T extends string>(
  value: unknown,
  allowed: ReadonlySet<T>,
  label: string
): T => {
  const decoded = string(value, label) as T
  if (!allowed.has(decoded)) throw new ComparatorProtocolError(`${label} is invalid`)
  return decoded
}

const plannedObject = (
  value: unknown,
  label: string,
  prefix: "route-input:" | "route-output:"
): ComparatorPlannedObject => {
  const item = record(value, label)
  exactKeys(item, ["id", "kind", "specification", "state", "not_a_result"], label)
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith(prefix)) {
    throw new ComparatorProtocolError(`${label}.id must start with '${prefix}'`)
  }
  if (item.state !== "PLANNED") {
    throw new ComparatorProtocolError(`${label}.state must be PLANNED`)
  }
  return {
    id,
    kind: string(item.kind, `${label}.kind`),
    specification: string(item.specification, `${label}.specification`),
    state: "PLANNED",
    not_a_result: truth(item.not_a_result, `${label}.not_a_result`)
  }
}

const sourcePin = (value: unknown, label: string): ComparatorSourcePin => {
  const item = record(value, label)
  exactKeys(
    item,
    ["id", "kind", "citation", "uri", "version", "retrieved_at_utc", "pinpoint", "role", "boundary"],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("source-pin:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'source-pin:'`)
  }
  const retrievedAt = string(item.retrieved_at_utc, `${label}.retrieved_at_utc`)
  if (!isUtcDateTime(retrievedAt)) {
    throw new ComparatorProtocolError(`${label}.retrieved_at_utc must be UTC ISO-8601`)
  }
  return {
    id,
    kind: enumValue(item.kind, sourceKinds, `${label}.kind`),
    citation: string(item.citation, `${label}.citation`),
    uri: webUri(item.uri, `${label}.uri`),
    version: string(item.version, `${label}.version`),
    retrieved_at_utc: retrievedAt,
    pinpoint: string(item.pinpoint, `${label}.pinpoint`),
    role: string(item.role, `${label}.role`),
    boundary: string(item.boundary, `${label}.boundary`)
  }
}

const toolPin = (value: unknown, label: string): ComparatorToolPin => {
  const item = record(value, label)
  exactKeys(
    item,
    ["id", "name", "repository_uri", "observed_commit", "observed_at_utc", "paper_source_ref", "role", "license_status", "installation_status", "boundary"],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("route-tool:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'route-tool:'`)
  }
  const commit = string(item.observed_commit, `${label}.observed_commit`)
  if (!/^[0-9a-f]{40}$/.test(commit)) {
    throw new ComparatorProtocolError(`${label}.observed_commit must be a full lowercase Git SHA-1`)
  }
  const observedAt = string(item.observed_at_utc, `${label}.observed_at_utc`)
  if (!isUtcDateTime(observedAt)) {
    throw new ComparatorProtocolError(`${label}.observed_at_utc must be UTC ISO-8601`)
  }
  if (item.installation_status !== "NOT_INSTALLED") {
    throw new ComparatorProtocolError(`${label}.installation_status must be NOT_INSTALLED`)
  }
  return {
    id,
    name: string(item.name, `${label}.name`),
    repository_uri: webUri(item.repository_uri, `${label}.repository_uri`),
    observed_commit: commit,
    observed_at_utc: observedAt,
    paper_source_ref: string(item.paper_source_ref, `${label}.paper_source_ref`),
    role: string(item.role, `${label}.role`),
    license_status: string(item.license_status, `${label}.license_status`),
    installation_status: "NOT_INSTALLED",
    boundary: string(item.boundary, `${label}.boundary`)
  }
}

const model = (value: unknown, label: string): ComparatorModel => {
  const item = record(value, label)
  exactKeys(
    item,
    ["id", "role", "name", "action", "convention", "parameter_lock", "matter_coupling", "boundary_domain", "source_refs", "non_claim"],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("route-model:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'route-model:'`)
  }
  return {
    id,
    role: enumValue(item.role, modelRoles, `${label}.role`),
    name: string(item.name, `${label}.name`),
    action: string(item.action, `${label}.action`),
    convention: string(item.convention, `${label}.convention`),
    parameter_lock: string(item.parameter_lock, `${label}.parameter_lock`),
    matter_coupling: string(item.matter_coupling, `${label}.matter_coupling`),
    boundary_domain: string(item.boundary_domain, `${label}.boundary_domain`),
    source_refs: stringArray(item.source_refs, `${label}.source_refs`),
    non_claim: string(item.non_claim, `${label}.non_claim`)
  }
}

const consumer = (value: unknown, label: string): ComparatorConsumer => {
  const item = record(value, label)
  exactKeys(item, ["id", "domain", "observable", "independence_boundary", "non_claim"], label)
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("route-consumer:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'route-consumer:'`)
  }
  return {
    id,
    domain: enumValue(item.domain, consumerDomains, `${label}.domain`),
    observable: string(item.observable, `${label}.observable`),
    independence_boundary: string(item.independence_boundary, `${label}.independence_boundary`),
    non_claim: string(item.non_claim, `${label}.non_claim`)
  }
}

const contextReference = (
  value: unknown,
  label: string
): ComparatorContextReference => {
  const item = record(value, label)
  exactKeys(item, ["graph", "node", "relation"], label)
  if (item.graph !== "cpt") {
    throw new ComparatorProtocolError(`${label}.graph must be cpt`)
  }
  const node = string(item.node, `${label}.node`)
  if (!node.startsWith("open:")) {
    throw new ComparatorProtocolError(`${label}.node must start with 'open:'`)
  }
  if (item.relation !== "CONTEXTUALIZES_NONAUTHORITATIVELY") {
    throw new ComparatorProtocolError(
      `${label}.relation must be CONTEXTUALIZES_NONAUTHORITATIVELY`
    )
  }
  return {
    graph: "cpt",
    node,
    relation: "CONTEXTUALIZES_NONAUTHORITATIVELY"
  }
}

const step = (value: unknown, label: string): ComparatorStep => {
  const item = record(value, label)
  exactKeys(
    item,
    [
      "id", "title", "kind", "state", "lane", "topic_refs", "context_refs",
      "model_refs", "source_refs", "tool_refs", "prerequisite_outputs", "inputs",
      "outputs", "choice_dimensions", "mechanism_object", "parameter_lock",
      "consumer_refs", "independent_check", "acceptance_criterion", "null_outcome",
      "kill_criterion", "principal_failure_class", "non_claim",
      "does_not_authorize_execution"
    ],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("route-step:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'route-step:'`)
  }
  if (item.state !== "PLANNED") {
    throw new ComparatorProtocolError(`${label}.state must be PLANNED`)
  }
  if (!Array.isArray(item.context_refs)) {
    throw new ComparatorProtocolError(`${label}.context_refs must be an array`)
  }
  if (!Array.isArray(item.inputs) || item.inputs.length < 1) {
    throw new ComparatorProtocolError(`${label}.inputs must contain at least one entry`)
  }
  if (!Array.isArray(item.outputs) || item.outputs.length < 1) {
    throw new ComparatorProtocolError(`${label}.outputs must contain at least one entry`)
  }
  return {
    id,
    title: string(item.title, `${label}.title`),
    kind: enumValue(item.kind, stepKinds, `${label}.kind`),
    state: "PLANNED",
    lane: enumValue(item.lane, lanes, `${label}.lane`),
    topic_refs: stringArray(item.topic_refs, `${label}.topic_refs`),
    context_refs: item.context_refs.map((entry, index) =>
      contextReference(entry, `${label}.context_refs[${index}]`)
    ),
    model_refs: stringArray(item.model_refs, `${label}.model_refs`),
    source_refs: stringArray(item.source_refs, `${label}.source_refs`),
    tool_refs: stringArray(item.tool_refs, `${label}.tool_refs`, 0),
    prerequisite_outputs: stringArray(
      item.prerequisite_outputs,
      `${label}.prerequisite_outputs`,
      0
    ),
    inputs: item.inputs.map((entry, index) =>
      plannedObject(entry, `${label}.inputs[${index}]`, "route-input:")
    ),
    outputs: item.outputs.map((entry, index) =>
      plannedObject(entry, `${label}.outputs[${index}]`, "route-output:")
    ),
    choice_dimensions: stringArray(item.choice_dimensions, `${label}.choice_dimensions`),
    mechanism_object: string(item.mechanism_object, `${label}.mechanism_object`),
    parameter_lock: string(item.parameter_lock, `${label}.parameter_lock`),
    consumer_refs: stringArray(item.consumer_refs, `${label}.consumer_refs`, 0),
    independent_check: string(item.independent_check, `${label}.independent_check`),
    acceptance_criterion: string(item.acceptance_criterion, `${label}.acceptance_criterion`),
    null_outcome: string(item.null_outcome, `${label}.null_outcome`),
    kill_criterion: string(item.kill_criterion, `${label}.kill_criterion`),
    principal_failure_class: enumValue(
      item.principal_failure_class,
      failureClasses,
      `${label}.principal_failure_class`
    ),
    non_claim: string(item.non_claim, `${label}.non_claim`),
    does_not_authorize_execution: truth(
      item.does_not_authorize_execution,
      `${label}.does_not_authorize_execution`
    )
  }
}

const edge = (value: unknown, label: string): ComparatorEdge => {
  const item = record(value, label)
  exactKeys(
    item,
    ["id", "from", "relation", "to", "rationale", "non_claim", "does_not_authorize_execution"],
    label
  )
  const id = string(item.id, `${label}.id`)
  if (!id.startsWith("route-edge:")) {
    throw new ComparatorProtocolError(`${label}.id must start with 'route-edge:'`)
  }
  return {
    id,
    from: string(item.from, `${label}.from`),
    relation: enumValue(item.relation, relations, `${label}.relation`),
    to: string(item.to, `${label}.to`),
    rationale: string(item.rationale, `${label}.rationale`),
    non_claim: string(item.non_claim, `${label}.non_claim`),
    does_not_authorize_execution: truth(
      item.does_not_authorize_execution,
      `${label}.does_not_authorize_execution`
    )
  }
}

const selectedStrategy = (
  value: unknown,
  label: string
): ComparatorSelectedStrategy => {
  const item = record(value, label)
  exactKeys(
    item,
    ["calibration_step", "first_comparator_model", "cross_domain_step", "ice_admission_step", "parallel_classification_step", "rationale"],
    label
  )
  return {
    calibration_step: string(item.calibration_step, `${label}.calibration_step`),
    first_comparator_model: string(
      item.first_comparator_model,
      `${label}.first_comparator_model`
    ),
    cross_domain_step: string(item.cross_domain_step, `${label}.cross_domain_step`),
    ice_admission_step: string(item.ice_admission_step, `${label}.ice_admission_step`),
    parallel_classification_step: string(
      item.parallel_classification_step,
      `${label}.parallel_classification_step`
    ),
    rationale: string(item.rationale, `${label}.rationale`)
  }
}

export const decodeIceComparatorProtocol = (
  sourceText: string,
  label = COMPARATOR_PROTOCOL_RELPATH
): IceComparatorProtocol => {
  let raw: unknown
  try {
    raw = JSON.parse(sourceText)
  } catch (error) {
    throw new ComparatorProtocolError(`${label} is not valid JSON: ${String(error)}`)
  }
  rejectForbiddenFields(raw, label)
  const protocol = record(raw, label)
  exactKeys(
    protocol,
    [
      "$schema", "schema_version", "protocol_id", "title", "description",
      "updated_at_utc", "authority", "canonical_graph_unchanged",
      "does_not_authorize_execution", "result_status", "selected_strategy",
      "source_pins", "tools", "models", "consumers", "steps", "edges", "boundaries"
    ],
    label
  )
  if (protocol.schema_version !== "ice-comparator-protocol/v1") {
    throw new ComparatorProtocolError(
      `${label}.schema_version must be ice-comparator-protocol/v1`
    )
  }
  if (protocol.protocol_id !== "comparator-protocol:ice-choice-robust-cross-domain") {
    throw new ComparatorProtocolError(`${label}.protocol_id is invalid`)
  }
  if (protocol.authority !== "NON_AUTHORITATIVE_METHOD_PROTOCOL") {
    throw new ComparatorProtocolError(`${label}.authority is invalid`)
  }
  if (protocol.result_status !== "DESIGN_ONLY") {
    throw new ComparatorProtocolError(`${label}.result_status must be DESIGN_ONLY`)
  }
  const updatedAt = string(protocol.updated_at_utc, `${label}.updated_at_utc`)
  if (!isUtcDateTime(updatedAt)) {
    throw new ComparatorProtocolError(`${label}.updated_at_utc must be UTC ISO-8601`)
  }
  const decodeArray = <T>(
    value: unknown,
    arrayLabel: string,
    decoder: (entry: unknown, entryLabel: string) => T,
    minimum = 1,
    maximum = 128
  ): ReadonlyArray<T> => {
    if (!Array.isArray(value) || value.length < minimum || value.length > maximum) {
      throw new ComparatorProtocolError(
        `${arrayLabel} must contain ${minimum} through ${maximum} entries`
      )
    }
    return value.map((entry, index) => decoder(entry, `${arrayLabel}[${index}]`))
  }
  return {
    ...(protocol.$schema === undefined
      ? {}
      : { $schema: string(protocol.$schema, `${label}.$schema`) }),
    schema_version: "ice-comparator-protocol/v1",
    protocol_id: "comparator-protocol:ice-choice-robust-cross-domain",
    title: string(protocol.title, `${label}.title`),
    description: string(protocol.description, `${label}.description`),
    updated_at_utc: updatedAt,
    authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL",
    canonical_graph_unchanged: truth(
      protocol.canonical_graph_unchanged,
      `${label}.canonical_graph_unchanged`
    ),
    does_not_authorize_execution: truth(
      protocol.does_not_authorize_execution,
      `${label}.does_not_authorize_execution`
    ),
    result_status: "DESIGN_ONLY",
    selected_strategy: selectedStrategy(
      protocol.selected_strategy,
      `${label}.selected_strategy`
    ),
    source_pins: decodeArray(protocol.source_pins, `${label}.source_pins`, sourcePin),
    tools: decodeArray(protocol.tools, `${label}.tools`, toolPin, 2, 16),
    models: decodeArray(protocol.models, `${label}.models`, model, 3, 16),
    consumers: decodeArray(protocol.consumers, `${label}.consumers`, consumer, 3, 16),
    steps: decodeArray(protocol.steps, `${label}.steps`, step, 5, 32),
    edges: decodeArray(protocol.edges, `${label}.edges`, edge, 1, 64),
    boundaries: stringArray(protocol.boundaries, `${label}.boundaries`)
  }
}
