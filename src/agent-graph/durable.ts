import { createHash } from "node:crypto"
import {
  graphRagContract,
  type GraphRagSearchResult
} from "../graphrag/core.ts"
import {
  planResearchAgentWorkflow,
  researchAgentGraphContract,
  type ResearchAgentWorkflowPlan
} from "./core.ts"

export const durableResearchAgentContract = {
  schema: "ice-research-agent-durable/v1",
  mode: "OFFLINE_DURABLE_HUMAN_APPROVED_READ_ONLY",
  automatic_follow_up: false,
  execution_authorization: "NOT_GRANTED",
  core_progress_authorization: "NOT_GRANTED"
} as const

export type ResearchAgentRunStatus =
  | "AWAITING_ROUTE_REVIEW"
  | "AWAITING_EVIDENCE_REVIEW"
  | "AWAITING_DESIGN_REVIEW"
  | "STOPPED"
  | "CLOSED"

export type HumanReviewStage = "ROUTE" | "EVIDENCE" | "DESIGN"
export type HumanReviewDecision = "APPROVE" | "STOP_OR_REFRAME"

export interface Sha256PinnedDocument {
  readonly path: string
  readonly sha256: string
}

export interface ResearchAgentRevisionPin {
  /** Resolved HEAD commit, not a moving symbolic revision such as `HEAD`. */
  readonly head_commit: string
  readonly collection: Sha256PinnedDocument
  readonly graphs: ReadonlyArray<Sha256PinnedDocument>
  readonly source_documents: ReadonlyArray<Sha256PinnedDocument>
  /** Exact TypeScript source manifest below `src`, including additions and deletions. */
  readonly control_plane_sources: ReadonlyArray<Sha256PinnedDocument>
}

export interface ResearchAgentRunDecision {
  readonly sequence: number
  readonly at: string
  readonly actor: "human"
  readonly stage: HumanReviewStage | "CREATE"
  readonly decision: HumanReviewDecision | "CREATE"
  readonly rationale: string
  readonly from: ResearchAgentRunStatus | null
  readonly to: ResearchAgentRunStatus
}

export type ResearchAgentTraceKind =
  | "PLAN_CREATED"
  | "HANDOFF_CREATED"
  | "HUMAN_DECISION"
  | "POLICY_DENIED"
  | "CLOSED"

export interface ResearchAgentRunEvent {
  readonly sequence: number
  readonly at: string
  readonly kind: ResearchAgentTraceKind
  readonly input_sha256: string
  readonly output_sha256: string
  readonly previous_event_sha256: string | null
  readonly event_sha256: string
}

export interface ResearchAgentHandoff {
  readonly schema: "ice-research-agent-handoff/v1"
  readonly from: "ROUTER" | "ROUTE_REVIEW" | "EVIDENCE_REVIEW" | "DESIGN_REVIEW"
  readonly to: "ROUTE_REVIEW" | "EVIDENCE_REVIEW" | "DESIGN_REVIEW" | "CLOSED"
  readonly candidate_only: true
  readonly artifact_refs: ReadonlyArray<{
    readonly kind: "plan" | "retrieval" | "revision_pin"
    readonly sha256: string
  }>
  readonly required_human_assertions: ReadonlyArray<string>
  readonly prohibited_claims: ReadonlyArray<string>
  readonly authorization: "NOT_GRANTED"
}

export interface ResearchAgentRunV1 {
  readonly schema: "ice-research-agent-run/v1"
  readonly run_id: string
  readonly status: ResearchAgentRunStatus
  readonly contract: typeof durableResearchAgentContract
  readonly revision_pin: ResearchAgentRevisionPin
  readonly plan: ResearchAgentWorkflowPlan
  readonly handoff: ResearchAgentHandoff
  readonly decisions: ReadonlyArray<ResearchAgentRunDecision>
  readonly trace: ReadonlyArray<ResearchAgentRunEvent>
}

export interface CreateResearchAgentRunInput {
  readonly run_id: string
  readonly at: string
  readonly plan: ResearchAgentWorkflowPlan
  readonly revision_pin: ResearchAgentRevisionPin
}

export interface ApplyResearchAgentReviewInput {
  readonly at: string
  readonly stage: HumanReviewStage
  readonly decision: HumanReviewDecision
  readonly rationale: string
  /** Must be the pin observed by the reviewer immediately before resuming. */
  readonly observed_revision_pin: ResearchAgentRevisionPin
}

export interface ResearchAgentRunAudit {
  readonly schema: "ice-research-agent-run-audit/v1"
  readonly passed: boolean
  readonly status: ResearchAgentRunStatus
  readonly checks: ReadonlyArray<{
    readonly id: string
    readonly passed: boolean
    readonly detail: string
  }>
  readonly errors: ReadonlyArray<string>
  readonly guidance: ReadonlyArray<string>
}

export interface DurableWorkflowEvaluationCase {
  readonly id: string
  readonly create: CreateResearchAgentRunInput
  readonly reviews: ReadonlyArray<Omit<ApplyResearchAgentReviewInput, "observed_revision_pin">>
  readonly expected_status: ResearchAgentRunStatus
}

export interface DurableWorkflowEvaluation {
  readonly schema: "ice-research-agent-durable-evaluation/v1"
  readonly passed: boolean
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly passed: boolean
    readonly actual_status: ResearchAgentRunStatus | null
    readonly expected_status: ResearchAgentRunStatus
    readonly error: string | null
  }>
  readonly guidance: ReadonlyArray<string>
}

const sha256 = (value: string): string =>
  createHash("sha256").update(value).digest("hex")

const stableJson = (value: unknown): string => {
  if (value === null || typeof value !== "object") return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(stableJson).join(",")}]`
  const record = value as Record<string, unknown>
  return `{${Object.keys(record)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableJson(record[key])}`)
    .join(",")}}`
}

const digest = (value: unknown): string => sha256(stableJson(value))
const hashPattern = /^[a-f0-9]{64}$/
const creationRationale = "A human requested a durable read-only workflow record."
const safePath = (path: string): boolean =>
  path.length > 0 &&
  path.length <= 512 &&
  !path.startsWith("/") &&
  !path.split("/").includes("..") &&
  !path.includes("\\") &&
  !path.includes("\u0000")

const assert: (condition: unknown, message: string) => asserts condition = (condition, message) => {
  if (!condition) throw new Error(message)
}

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const hasOnlyKeys = (value: Record<string, unknown>, keys: ReadonlyArray<string>): boolean =>
  Object.keys(value).every((key) => keys.includes(key)) &&
  keys.every((key) => key in value)

const isRunStatus = (value: unknown): value is ResearchAgentRunStatus =>
  value === "AWAITING_ROUTE_REVIEW" ||
  value === "AWAITING_EVIDENCE_REVIEW" ||
  value === "AWAITING_DESIGN_REVIEW" ||
  value === "STOPPED" ||
  value === "CLOSED"

const isReviewStage = (value: unknown): value is HumanReviewStage =>
  value === "ROUTE" || value === "EVIDENCE" || value === "DESIGN"

const isReviewDecision = (value: unknown): value is HumanReviewDecision =>
  value === "APPROVE" || value === "STOP_OR_REFRAME"

const isRouteClassification = (value: unknown): boolean =>
  value === "CURRENT_BLOCKER_CANDIDATE" ||
  value === "DOWNSTREAM_BLOCKED" ||
  value === "SUPPORTING_ONLY" ||
  value === "PROFILE_SCOPE_MISMATCH" ||
  value === "INSUFFICIENT_ROUTE_EVIDENCE"

const isCanonicalUtcTimestamp = (value: unknown): value is string =>
  typeof value === "string" &&
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value) &&
  !Number.isNaN(Date.parse(value)) &&
  new Date(value).toISOString() === value

const assertDocument: (value: unknown, label: string) => asserts value is Sha256PinnedDocument = (value, label) => {
  assert(isRecord(value) && hasOnlyKeys(value, ["path", "sha256"]), `${label} must be a strict pinned document`)
  assert(typeof value.path === "string" && safePath(value.path), `${label} has an unsafe path`)
  assert(typeof value.sha256 === "string" && hashPattern.test(value.sha256), `${label} has an invalid SHA-256`)
}

const assertPin = (pin: ResearchAgentRevisionPin): void => {
  assert(isRecord(pin) && hasOnlyKeys(pin, ["head_commit", "collection", "graphs", "source_documents", "control_plane_sources"]), "revision pin has an unexpected shape")
  assert(/^[0-9a-f]{40,64}$/.test(pin.head_commit), "revision pin requires a resolved lowercase commit hash")
  assert(Array.isArray(pin.graphs) && Array.isArray(pin.source_documents) && Array.isArray(pin.control_plane_sources), "revision pin document collections must be arrays")
  const documents = [pin.collection, ...pin.graphs, ...pin.source_documents]
  assert(documents.length > 1, "revision pin requires collection and at least one pinned document")
  assert(pin.control_plane_sources.length > 0, "revision pin requires at least one control-plane source")
  const paths = new Set<string>()
  for (const document of documents) {
    assertDocument(document, "revision pin document")
    assert(!paths.has(document.path), `duplicate pinned document '${document.path}'`)
    paths.add(document.path)
  }
  const controlPlanePaths = new Set<string>()
  for (const document of pin.control_plane_sources) {
    assertDocument(document, "control-plane source")
    assert(!controlPlanePaths.has(document.path), `duplicate control-plane source '${document.path}'`)
    controlPlanePaths.add(document.path)
  }
}

const samePin = (left: ResearchAgentRevisionPin, right: ResearchAgentRevisionPin): boolean =>
  stableJson(left) === stableJson(right)

export const sameResearchAgentRevisionPin = samePin

const assertSafePlan = (plan: ResearchAgentWorkflowPlan): void => {
  assert(isRecord(plan) && hasOnlyKeys(plan, ["schema", "contract", "checkpoint", "objective_routing", "steps", "retrieval", "tool_routes", "guidance"]), "plan has an unexpected shape")
  assert(plan.schema === "ice-research-agent-workflow-plan/v2", "plan has an unexpected schema")
  assert(
    isRecord(plan.contract) &&
      hasOnlyKeys(plan.contract, Object.keys(researchAgentGraphContract)) &&
      stableJson(plan.contract) === stableJson(researchAgentGraphContract),
    "plan contract is malformed"
  )
  assert(
    isRecord(plan.checkpoint) &&
      hasOnlyKeys(plan.checkpoint, ["id", "state", "question", "graph_retrieval_ids"]) &&
      plan.checkpoint.state === "AWAITING_HUMAN_REVIEW" &&
      typeof plan.checkpoint.id === "string" &&
      plan.checkpoint.id.length > 0 &&
      typeof plan.checkpoint.question === "string" &&
      plan.checkpoint.question.trim().length > 0 &&
      plan.checkpoint.question.length <= 500 &&
      Array.isArray(plan.checkpoint.graph_retrieval_ids) &&
      plan.checkpoint.graph_retrieval_ids.every((id) => typeof id === "string"),
    "plan checkpoint is malformed"
  )
  assert(
    isRecord(plan.objective_routing) &&
      isRouteClassification(plan.objective_routing.classification),
    "plan objective routing is malformed"
  )
  assert(Array.isArray(plan.steps) && Array.isArray(plan.tool_routes) && Array.isArray(plan.guidance), "plan workflow arrays are malformed")
  assert(
    plan.steps.every(
      (step) =>
        isRecord(step) &&
        typeof step.id === "string" &&
        (step.state === "COMPLETED" ||
          step.state === "AVAILABLE" ||
          step.state === "HUMAN_REVIEW_REQUIRED" ||
          step.state === "NOT_AUTHORIZED")
    ),
    "plan workflow steps are malformed"
  )
  assert(
    isRecord(plan.retrieval) &&
      typeof plan.retrieval.query === "string" &&
      typeof plan.retrieval.graph === "string" &&
      Number.isInteger(plan.retrieval.depth) &&
      Array.isArray(plan.retrieval.hits) &&
      Array.isArray(plan.retrieval.communities) &&
      Array.isArray(plan.retrieval.guidance),
    "plan retrieval is malformed"
  )
  assert(plan.guidance.every((entry) => typeof entry === "string"), "plan guidance is malformed")
  assert(
    plan.steps.find(({ id }) => id === "execution")?.state === "NOT_AUTHORIZED",
    "plan execution step is not blocked"
  )
  const reconstruction: GraphRagSearchResult = {
    schema: "ice-evidence-graph-rag-search/v2",
    contract: graphRagContract,
    query: plan.retrieval.query,
    graph: plan.retrieval.graph,
    limit: Math.max(1, plan.retrieval.hits.length),
    depth: plan.retrieval.depth,
    index: {
      text_units: plan.retrieval.hits.length,
      communities: plan.retrieval.communities.length,
      retrieval:
        "BM25 lexical anchors + deterministic token-hash reranking + bounded graph expansion"
    },
    abstention: {
      abstained: plan.retrieval.hits.length === 0,
      reason: plan.retrieval.hits.length === 0 ? "NO_LEXICAL_ANCHOR" : null,
      lexical_anchor_count: plan.retrieval.hits.length
    },
    hits: plan.retrieval.hits,
    communities: plan.retrieval.communities,
    guidance: plan.retrieval.guidance
  }
  assert(
    stableJson(plan) ===
      stableJson(
        planResearchAgentWorkflow(plan.checkpoint.question, reconstruction)
      ),
    "plan does not match the deterministic workflow projection of its retrieval"
  )
}

const assertDecision: (value: unknown, index: number) => asserts value is ResearchAgentRunDecision = (value, index) => {
  assert(isRecord(value) && hasOnlyKeys(value, ["sequence", "at", "actor", "stage", "decision", "rationale", "from", "to"]), `decision ${index + 1} has an unexpected shape`)
  assert(typeof value.sequence === "number" && Number.isInteger(value.sequence) && value.sequence > 0, `decision ${index + 1} sequence is invalid`)
  assert(isCanonicalUtcTimestamp(value.at), `decision ${index + 1} time is invalid`)
  assert(value.actor === "human", `decision ${index + 1} actor must be human`)
  assert(typeof value.rationale === "string" && value.rationale.trim().length > 0 && value.rationale.length <= 2_000, `decision ${index + 1} rationale is invalid`)
  assert(value.from === null || isRunStatus(value.from), `decision ${index + 1} source state is invalid`)
  assert(isRunStatus(value.to), `decision ${index + 1} target state is invalid`)
  if (index === 0) {
    assert(value.stage === "CREATE" && value.decision === "CREATE" && value.from === null && value.to === "AWAITING_ROUTE_REVIEW", "creation decision is invalid")
    assert(value.rationale === creationRationale, "creation decision rationale is invalid")
  } else {
    assert(isReviewStage(value.stage) && isReviewDecision(value.decision), `decision ${index + 1} stage or decision is invalid`)
  }
}

const assertEvent: (value: unknown, index: number) => asserts value is ResearchAgentRunEvent = (value, index) => {
  assert(isRecord(value) && hasOnlyKeys(value, ["sequence", "at", "kind", "input_sha256", "output_sha256", "previous_event_sha256", "event_sha256"]), `trace event ${index + 1} has an unexpected shape`)
  assert(typeof value.sequence === "number" && Number.isInteger(value.sequence) && value.sequence > 0, `trace event ${index + 1} sequence is invalid`)
  assert(isCanonicalUtcTimestamp(value.at), `trace event ${index + 1} time is invalid`)
  assert(value.kind === "PLAN_CREATED" || value.kind === "HANDOFF_CREATED" || value.kind === "HUMAN_DECISION" || value.kind === "POLICY_DENIED" || value.kind === "CLOSED", `trace event ${index + 1} kind is invalid`)
  assert(typeof value.input_sha256 === "string" && hashPattern.test(value.input_sha256) && typeof value.output_sha256 === "string" && hashPattern.test(value.output_sha256) && (value.previous_event_sha256 === null || typeof value.previous_event_sha256 === "string" && hashPattern.test(value.previous_event_sha256)) && typeof value.event_sha256 === "string" && hashPattern.test(value.event_sha256), `trace event ${index + 1} hashes are invalid`)
}

const assertHandoff: (value: unknown) => asserts value is ResearchAgentHandoff = (value) => {
  assert(isRecord(value) && hasOnlyKeys(value, ["schema", "from", "to", "candidate_only", "artifact_refs", "required_human_assertions", "prohibited_claims", "authorization"]), "handoff has an unexpected shape")
  assert(value.schema === "ice-research-agent-handoff/v1" && value.candidate_only === true && value.authorization === "NOT_GRANTED", "handoff contract is invalid")
  assert((value.from === "ROUTER" || value.from === "ROUTE_REVIEW" || value.from === "EVIDENCE_REVIEW" || value.from === "DESIGN_REVIEW") && (value.to === "ROUTE_REVIEW" || value.to === "EVIDENCE_REVIEW" || value.to === "DESIGN_REVIEW" || value.to === "CLOSED") && Array.isArray(value.artifact_refs) && Array.isArray(value.required_human_assertions) && Array.isArray(value.prohibited_claims), "handoff fields are invalid")
}

/** Strict runtime decoder used before any stored run is audited or resumed. */
export const decodeResearchAgentRun = (value: unknown): ResearchAgentRunV1 => {
  assert(isRecord(value) && hasOnlyKeys(value, ["schema", "run_id", "status", "contract", "revision_pin", "plan", "handoff", "decisions", "trace"]), "durable run has an unexpected shape")
  assert(value.schema === "ice-research-agent-run/v1", "durable run has an unexpected schema")
  assert(typeof value.run_id === "string" && /^[a-z0-9][a-z0-9_-]{2,127}$/.test(value.run_id), "durable run id is invalid")
  assert(isRunStatus(value.status), "durable run status is invalid")
  assert(isRecord(value.contract) && hasOnlyKeys(value.contract, ["schema", "mode", "automatic_follow_up", "execution_authorization", "core_progress_authorization"]) && value.contract.schema === durableResearchAgentContract.schema && value.contract.mode === durableResearchAgentContract.mode && value.contract.automatic_follow_up === false && value.contract.execution_authorization === "NOT_GRANTED" && value.contract.core_progress_authorization === "NOT_GRANTED", "durable run contract is invalid")
  assertPin(value.revision_pin as ResearchAgentRevisionPin)
  assertSafePlan(value.plan as ResearchAgentWorkflowPlan)
  assertHandoff(value.handoff)
  assert(Array.isArray(value.decisions) && Array.isArray(value.trace), "durable run histories are invalid")
  value.decisions.forEach(assertDecision)
  value.trace.forEach(assertEvent)
  return value as unknown as ResearchAgentRunV1
}

const statusForStage = (stage: HumanReviewStage): ResearchAgentRunStatus =>
  stage === "ROUTE"
    ? "AWAITING_ROUTE_REVIEW"
    : stage === "EVIDENCE"
      ? "AWAITING_EVIDENCE_REVIEW"
      : "AWAITING_DESIGN_REVIEW"

const approvedStatus = (stage: HumanReviewStage): ResearchAgentRunStatus =>
  stage === "ROUTE"
    ? "AWAITING_EVIDENCE_REVIEW"
    : stage === "EVIDENCE"
      ? "AWAITING_DESIGN_REVIEW"
      : "CLOSED"

const handoffFor = (
  run: Pick<ResearchAgentRunV1, "plan" | "revision_pin">,
  from: ResearchAgentHandoff["from"],
  to: ResearchAgentHandoff["to"]
): ResearchAgentHandoff => ({
  schema: "ice-research-agent-handoff/v1",
  from,
  to,
  candidate_only: true,
  artifact_refs: [
    { kind: "plan", sha256: digest(run.plan) },
    { kind: "retrieval", sha256: digest(run.plan.retrieval) },
    { kind: "revision_pin", sha256: digest(run.revision_pin) }
  ],
  required_human_assertions: [
    "Treat routing and retrieval as review context, not scientific evidence.",
    "Record one bounded decision or stop; do not create an automatic successor."
  ],
  prohibited_claims: [
    "This handoff does not establish a physical claim.",
    "This handoff does not authorize numerical execution or core progress."
  ],
  authorization: "NOT_GRANTED"
})

const eventHash = (event: Omit<ResearchAgentRunEvent, "event_sha256">): string => digest(event)

const makeEvent = (
  sequence: number,
  at: string,
  kind: ResearchAgentTraceKind,
  input: unknown,
  output: unknown,
  previous: string | null
): ResearchAgentRunEvent => {
  const event = {
    sequence,
    at,
    kind,
    input_sha256: digest(input),
    output_sha256: digest(output),
    previous_event_sha256: previous
  }
  return { ...event, event_sha256: eventHash(event) }
}

const assertTime = (at: string): void =>
  assert(isCanonicalUtcTimestamp(at), "event time must be a canonical UTC ISO-8601 timestamp")

/** Creates a caller-owned, serializable workflow record. It never writes it. */
export const createResearchAgentRun = (
  input: CreateResearchAgentRunInput
): ResearchAgentRunV1 => {
  assert(/^[a-z0-9][a-z0-9_-]{2,127}$/.test(input.run_id), "run_id must be 3-128 lowercase safe characters")
  assertTime(input.at)
  assertSafePlan(input.plan)
  assertPin(input.revision_pin)
  const base = {
    schema: "ice-research-agent-run/v1" as const,
    run_id: input.run_id,
    status: "AWAITING_ROUTE_REVIEW" as const,
    contract: durableResearchAgentContract,
    revision_pin: input.revision_pin,
    plan: input.plan
  }
  const handoff = handoffFor(base, "ROUTER", "ROUTE_REVIEW")
  const decision: ResearchAgentRunDecision = {
    sequence: 1,
    at: input.at,
    actor: "human",
    stage: "CREATE",
    decision: "CREATE",
    rationale: creationRationale,
    from: null,
    to: "AWAITING_ROUTE_REVIEW"
  }
  const trace = [
    makeEvent(1, input.at, "PLAN_CREATED", input, { ...base, handoff, decision }, null),
    makeEvent(2, input.at, "HANDOFF_CREATED", base, handoff, null)
  ]
  const first = trace[0]
  assert(first !== undefined, "creation trace is unexpectedly empty")
  trace[1] = makeEvent(2, input.at, "HANDOFF_CREATED", base, handoff, first.event_sha256)
  return { ...base, handoff, decisions: [decision], trace }
}

/** Applies one typed human decision; there is deliberately no execution transition. */
export const applyResearchAgentReview = (
  run: ResearchAgentRunV1,
  input: ApplyResearchAgentReviewInput
): ResearchAgentRunV1 => {
  const audit = auditResearchAgentRun(run, input.observed_revision_pin)
  if (!audit.passed) throw new Error(`cannot resume durable run: ${audit.errors.join("; ")}`)
  assertTime(input.at)
  assert(
    Date.parse(input.at) >= Date.parse(run.trace.at(-1)?.at ?? ""),
    "review time cannot precede the latest durable event"
  )
  assert(input.rationale.trim().length > 0 && input.rationale.length <= 2_000, "review rationale must contain 1-2000 characters")
  assert(run.status === statusForStage(input.stage), `review stage ${input.stage} is not available from ${run.status}`)
  if (input.decision === "APPROVE" && input.stage === "ROUTE") {
    assert(
      run.plan.objective_routing.classification === "CURRENT_BLOCKER_CANDIDATE",
      "only a current-blocker candidate may pass route review"
    )
  }
  const nextStatus = input.decision === "STOP_OR_REFRAME" ? "STOPPED" : approvedStatus(input.stage)
  const reviewSource: ResearchAgentHandoff["from"] =
    input.stage === "ROUTE"
      ? "ROUTE_REVIEW"
      : input.stage === "EVIDENCE"
        ? "EVIDENCE_REVIEW"
        : "DESIGN_REVIEW"
  const nextHandoff = handoffFor(
    run,
    reviewSource,
    nextStatus === "AWAITING_EVIDENCE_REVIEW"
      ? "EVIDENCE_REVIEW"
      : nextStatus === "AWAITING_DESIGN_REVIEW"
        ? "DESIGN_REVIEW"
        : "CLOSED"
  )
  const decision: ResearchAgentRunDecision = {
    sequence: run.decisions.length + 1,
    at: input.at,
    actor: "human",
    stage: input.stage,
    decision: input.decision,
    rationale: input.rationale.trim(),
    from: run.status,
    to: nextStatus
  }
  const trace = [...run.trace]
  const previous = trace.at(-1)?.event_sha256 ?? null
  trace.push(makeEvent(trace.length + 1, input.at, "HUMAN_DECISION", { run, input }, decision, previous))
  if (nextStatus === "CLOSED") {
    trace.push(makeEvent(trace.length + 1, input.at, "CLOSED", decision, { status: nextStatus, authorization: "NOT_GRANTED" }, trace.at(-1)?.event_sha256 ?? null))
  } else if (nextStatus !== "STOPPED") {
    trace.push(makeEvent(trace.length + 1, input.at, "HANDOFF_CREATED", decision, nextHandoff, trace.at(-1)?.event_sha256 ?? null))
  }
  return { ...run, status: nextStatus, handoff: nextHandoff, decisions: [...run.decisions, decision], trace }
}

const expectedHandoffTarget = (status: ResearchAgentRunStatus): ResearchAgentHandoff["to"] =>
  status === "AWAITING_ROUTE_REVIEW" ? "ROUTE_REVIEW" : status === "AWAITING_EVIDENCE_REVIEW" ? "EVIDENCE_REVIEW" : status === "AWAITING_DESIGN_REVIEW" ? "DESIGN_REVIEW" : "CLOSED"

const expectedHandoffSource = (
  run: Pick<ResearchAgentRunV1, "status" | "decisions">
): ResearchAgentHandoff["from"] => {
  if (run.status === "AWAITING_ROUTE_REVIEW") return "ROUTER"
  if (run.status === "AWAITING_EVIDENCE_REVIEW") return "ROUTE_REVIEW"
  if (run.status === "AWAITING_DESIGN_REVIEW") return "EVIDENCE_REVIEW"
  const finalStage = run.decisions.at(-1)?.stage
  return finalStage === "ROUTE"
    ? "ROUTE_REVIEW"
    : finalStage === "EVIDENCE"
      ? "EVIDENCE_REVIEW"
      : "DESIGN_REVIEW"
}

/** Validates serializable integrity, allowed transitions, and optionally a newly observed pin. */
export const auditResearchAgentRun = (
  input: unknown,
  observedRevisionPin?: ResearchAgentRevisionPin
): ResearchAgentRunAudit => {
  const errors: string[] = []
  let run: ResearchAgentRunV1
  try {
    run = decodeResearchAgentRun(input)
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    return {
      schema: "ice-research-agent-run-audit/v1",
      passed: false,
      status: isRecord(input) && isRunStatus(input.status) ? input.status : "STOPPED",
      checks: [{ id: "strict-runtime-decoder", passed: false, detail: "Stored durable runs must decode before integrity checks." }],
      errors: [message],
      guidance: ["This is an offline human-review audit, not a scientific validation or execution permit."]
    }
  }
  try { assertPin(run.revision_pin) } catch (error) { errors.push(error instanceof Error ? error.message : String(error)) }
  try { assertSafePlan(run.plan) } catch (error) { errors.push(error instanceof Error ? error.message : String(error)) }
  if (run.schema !== "ice-research-agent-run/v1") errors.push("unexpected run schema")
  if (run.contract.execution_authorization !== "NOT_GRANTED" || run.contract.core_progress_authorization !== "NOT_GRANTED" || run.contract.automatic_follow_up !== false) errors.push("durable contract permits an unsafe action")
  if (run.handoff.authorization !== "NOT_GRANTED" || run.handoff.candidate_only !== true) errors.push("handoff grants authority")
  if (run.handoff.to !== expectedHandoffTarget(run.status)) errors.push("handoff target does not match run status")
  if (
    stableJson(run.handoff) !== stableJson(
      handoffFor(
        run,
        expectedHandoffSource(run),
        expectedHandoffTarget(run.status)
      )
    )
  ) {
    errors.push("handoff payload does not match the pinned plan, revision, and state")
  }
  if (observedRevisionPin !== undefined && !samePin(run.revision_pin, observedRevisionPin)) errors.push("revision drift: observed pin differs from the pinned workflow input")
  let previous: string | null = null
  let previousEventTime = Number.NEGATIVE_INFINITY
  for (const [index, event] of run.trace.entries()) {
    const { event_sha256: _eventHash, ...eventWithoutHash } = event
    const expected = eventHash(eventWithoutHash)
    if (event.sequence !== index + 1) errors.push(`trace sequence ${event.sequence} is not contiguous`)
    if (event.previous_event_sha256 !== previous) errors.push(`trace event ${event.sequence} has an invalid predecessor`)
    if (event.event_sha256 !== expected) errors.push(`trace event ${event.sequence} hash mismatch`)
    const eventTime = Date.parse(event.at)
    if (Number.isNaN(eventTime) || eventTime < previousEventTime) {
      errors.push(`trace event ${event.sequence} time is invalid or non-monotonic`)
    }
    previousEventTime = eventTime
    previous = event.event_sha256
  }
  if (run.trace.length < 2) errors.push("run is missing its creation trace")
  if (run.decisions.length < 1 || run.decisions[0]?.stage !== "CREATE") errors.push("run is missing its creation decision")
  const creationDecision = run.decisions[0]
  const creationEvent = run.trace[0]
  const creationHandoffEvent = run.trace[1]
  if (creationDecision !== undefined && creationEvent !== undefined) {
    const creationInput = {
      run_id: run.run_id,
      at: creationDecision.at,
      plan: run.plan,
      revision_pin: run.revision_pin
    }
    const creationBase = {
      schema: "ice-research-agent-run/v1" as const,
      run_id: run.run_id,
      status: "AWAITING_ROUTE_REVIEW" as const,
      contract: run.contract,
      revision_pin: run.revision_pin,
      plan: run.plan
    }
    const initialHandoff = handoffFor(
      creationBase,
      "ROUTER",
      "ROUTE_REVIEW"
    )
    if (
      creationEvent.kind !== "PLAN_CREATED" ||
      creationEvent.at !== creationDecision.at ||
      creationEvent.input_sha256 !== digest(creationInput) ||
      creationEvent.output_sha256 !==
        digest({ ...creationBase, handoff: initialHandoff, decision: creationDecision })
    ) {
      errors.push("creation trace does not bind the current plan and revision pin")
    }
    if (
      creationHandoffEvent === undefined ||
      creationHandoffEvent.kind !== "HANDOFF_CREATED" ||
      creationHandoffEvent.at !== creationDecision.at ||
      creationHandoffEvent.input_sha256 !== digest(creationBase) ||
      creationHandoffEvent.output_sha256 !== digest(initialHandoff)
    ) {
      errors.push("creation handoff trace does not bind the initial review package")
    }
  }
  const decisionEvents = run.trace.filter(({ kind }) => kind === "HUMAN_DECISION")
  const reviewedDecisions = run.decisions.slice(1)
  if (decisionEvents.length !== reviewedDecisions.length) {
    errors.push("human decision trace count does not match decision history")
  }
  for (const [index, decision] of reviewedDecisions.entries()) {
    const event = decisionEvents[index]
    if (
      event === undefined ||
      event.at !== decision.at ||
      event.output_sha256 !== digest(decision)
    ) {
      errors.push(`decision ${decision.sequence} is not bound to its trace event`)
    }
  }
  const expectedTraceKinds: ResearchAgentTraceKind[] = ["PLAN_CREATED", "HANDOFF_CREATED"]
  for (const decision of reviewedDecisions) {
    expectedTraceKinds.push("HUMAN_DECISION")
    if (decision.decision === "APPROVE") {
      expectedTraceKinds.push(decision.stage === "DESIGN" ? "CLOSED" : "HANDOFF_CREATED")
    }
  }
  if (
    run.trace.length !== expectedTraceKinds.length ||
    run.trace.some((event, index) => event.kind !== expectedTraceKinds[index])
  ) {
    errors.push("trace event sequence does not match the finite review state machine")
  }
  let traceIndex = 2
  for (const decision of reviewedDecisions) {
    const decisionEvent = run.trace[traceIndex]
    traceIndex += 1
    if (decisionEvent?.kind !== "HUMAN_DECISION") continue
    if (decision.stage === "CREATE" || decision.decision === "CREATE") continue
    if (decision.decision === "APPROVE") {
      const terminalEvent = run.trace[traceIndex]
      traceIndex += 1
      if (decision.stage === "DESIGN") {
        if (
          terminalEvent?.kind !== "CLOSED" ||
          terminalEvent.at !== decision.at ||
          terminalEvent.input_sha256 !== digest(decision) ||
          terminalEvent.output_sha256 !==
            digest({ status: "CLOSED", authorization: "NOT_GRANTED" })
        ) {
          errors.push(`decision ${decision.sequence} is not bound to its closed event`)
        }
      } else {
        const source =
          decision.stage === "ROUTE" ? "ROUTE_REVIEW" : "EVIDENCE_REVIEW"
        const target =
          decision.stage === "ROUTE" ? "EVIDENCE_REVIEW" : "DESIGN_REVIEW"
        const expectedHandoff = handoffFor(run, source, target)
        if (
          terminalEvent?.kind !== "HANDOFF_CREATED" ||
          terminalEvent.at !== decision.at ||
          terminalEvent.input_sha256 !== digest(decision) ||
          terminalEvent.output_sha256 !== digest(expectedHandoff)
        ) {
          errors.push(`decision ${decision.sequence} is not bound to its next handoff event`)
        }
      }
    }
  }
  let state: ResearchAgentRunStatus = "AWAITING_ROUTE_REVIEW"
  let previousDecisionTime = Number.NEGATIVE_INFINITY
  for (const [index, decision] of run.decisions.entries()) {
    if (decision.sequence !== index + 1) errors.push(`decision sequence ${decision.sequence} is not contiguous`)
    const decisionTime = Date.parse(decision.at)
    if (Number.isNaN(decisionTime) || decisionTime < previousDecisionTime) {
      errors.push(`decision ${decision.sequence} time is invalid or non-monotonic`)
    }
    previousDecisionTime = decisionTime
    if (index === 0) continue
    if (decision.from !== state || decision.stage === "CREATE") errors.push(`decision ${decision.sequence} has an invalid predecessor`)
    const allowedStage = decision.stage === "CREATE" ? null : statusForStage(decision.stage)
    if (allowedStage !== state) errors.push(`decision ${decision.sequence} is applied at an unavailable review stage`)
    const expected = decision.decision === "STOP_OR_REFRAME" ? "STOPPED" : decision.stage === "CREATE" ? "AWAITING_ROUTE_REVIEW" : approvedStatus(decision.stage)
    if (decision.to !== expected) errors.push(`decision ${decision.sequence} has an invalid target`)
    if (
      decision.stage === "ROUTE" &&
      decision.decision === "APPROVE" &&
      run.plan.objective_routing.classification !== "CURRENT_BLOCKER_CANDIDATE"
    ) {
      errors.push(`decision ${decision.sequence} approves a non-current route`)
    }
    state = decision.to
  }
  if (state !== run.status) errors.push("run status does not match decision history")
  const checks = [
    { id: "hash-chain", passed: !errors.some((error) => error.includes("trace") || error.includes("bound")), detail: "Every trace event is contiguous and SHA-256 chained for self-consistency; this is not a signature." },
    { id: "revision-pin", passed: !errors.some((error) => error.includes("pin") || error.includes("revision drift")), detail: "HEAD, control-plane sources, collection, graph, and local source-document inputs remain pinned." },
    { id: "finite-human-transitions", passed: !errors.some((error) => error.includes("decision") || error.includes("status")), detail: "Only typed human review transitions may advance or stop a run." },
    { id: "no-execution-authority", passed: !errors.some((error) => error.includes("authority") || error.includes("unsafe action") || error.includes("execution step")), detail: "CLOSED records design review only; it never authorizes ./ice run." }
  ]
  return {
    schema: "ice-research-agent-run-audit/v1",
    passed: errors.length === 0,
    status: run.status,
    checks,
    errors,
    guidance: [
      "This is an offline human-review audit, not a scientific validation or execution permit.",
      "The SHA-256 event chain detects accidental or partial rewrites but is not tamper-resistant against a writer who can recompute it.",
      "Revision drift requires a new workflow record; it cannot be silently resumed."
    ]
  }
}

/** Executes a representative, caller-supplied routing workflow suite without I/O. */
export const evaluateDurableWorkflowCases = (
  cases: ReadonlyArray<DurableWorkflowEvaluationCase>
): DurableWorkflowEvaluation => {
  const results = cases.map((testCase) => {
    try {
      let run = createResearchAgentRun(testCase.create)
      for (const review of testCase.reviews) {
        run = applyResearchAgentReview(run, {
          ...review,
          observed_revision_pin: run.revision_pin
        })
      }
      return { id: testCase.id, passed: run.status === testCase.expected_status, actual_status: run.status, expected_status: testCase.expected_status, error: null }
    } catch (error) {
      return { id: testCase.id, passed: false, actual_status: null, expected_status: testCase.expected_status, error: error instanceof Error ? error.message : String(error) }
    }
  })
  return {
    schema: "ice-research-agent-durable-evaluation/v1",
    passed: results.every(({ passed }) => passed),
    cases: results,
    guidance: [
      "This evaluates durable routing and authorization boundaries only; it does not evaluate scientific truth or citation quality.",
      "No case invokes a model, writes a checkpoint, or authorizes execution."
    ]
  }
}
