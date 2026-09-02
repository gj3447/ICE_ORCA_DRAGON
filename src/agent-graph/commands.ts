import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { graphRagIndexData } from "../graphrag/commands.ts"
import { searchGraphRag } from "../graphrag/core.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { Workspace } from "../workspace.ts"
import { planResearchAgentWorkflow } from "./core.ts"
import {
  applyResearchAgentReview,
  auditResearchAgentRun,
  createResearchAgentRun,
  sameResearchAgentRevisionPin,
  type HumanReviewDecision,
  type HumanReviewStage
} from "./durable.ts"
import {
  captureResearchAgentRevisionPin,
  observeResearchAgentRevisionPin
} from "./revision.ts"
import {
  readResearchAgentRun,
  updateResearchAgentRun,
  writeNewResearchAgentRun
} from "./store.ts"
import { assertToeNavigationProfile } from "./toe-route.ts"
import { evaluateResearchAgentWorkflowSuite } from "./workflow-eval.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

export const researchAgentPlanData = (
  question: string,
  graph: string,
  limit: number,
  depth: number
) =>
  graphRagIndexData.pipe(
    Effect.flatMap((index) =>
      Effect.try({
        try: () => {
          assertToeNavigationProfile(index.units)
          const retrieval = searchGraphRag(index, question, { graph, limit, depth })
          return planResearchAgentWorkflow(question, retrieval)
        },
        catch: (error) =>
          iceError(
            "RESEARCH_AGENT_PLAN_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const researchAgentPlanCommand = (
  question: string,
  graph: string,
  limit: number,
  depth: number,
  json: boolean
) =>
  researchAgentPlanData(question, graph, limit, depth).pipe(
    Effect.tap((plan) =>
      json
        ? printJson(plan)
        : Console.log(
            [
              `research agent checkpoint: ${plan.checkpoint.id}`,
              `state: ${plan.checkpoint.state}`,
              `objective: ${plan.objective_routing.objective.status}`,
              `route: ${plan.objective_routing.classification}`,
              `selected lane: ${plan.objective_routing.selected_lane_id ?? "NONE"}`,
              `decision: ${plan.objective_routing.decision}`,
              `retrieved records: ${plan.checkpoint.graph_retrieval_ids.length}`,
              "execution/core-progress: NOT AUTHORIZED; human route review is required"
            ].join("\n")
          )
    )
  )

const durableFailure = (operation: string, error: unknown) =>
  iceError(
    "RESEARCH_AGENT_DURABLE_RUN_FAILED",
    `${operation}: ${error instanceof Error ? error.message : String(error)}`,
    2
  )

export const researchAgentRunCreateData = (
  runId: string,
  question: string,
  graph: string,
  limit: number,
  depth: number,
  at = new Date().toISOString()
) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const [initialPlan, { collection }] = yield* Effect.all(
      [
        researchAgentPlanData(question, graph, limit, depth),
        loadValidOntologyCollectionStructure
      ],
      { concurrency: 2 }
    )
    const preRevisionPin = yield* Effect.tryPromise({
      try: () =>
        captureResearchAgentRevisionPin(workspace.root, collection, initialPlan),
      catch: (error) => durableFailure("cannot capture revision pin", error)
    })
    const [plan, { collection: currentCollection }] = yield* Effect.all(
      [
        researchAgentPlanData(question, graph, limit, depth),
        loadValidOntologyCollectionStructure
      ],
      { concurrency: 2 }
    )
    const revisionPin = yield* Effect.tryPromise({
      try: () =>
        captureResearchAgentRevisionPin(workspace.root, currentCollection, plan),
      catch: (error) => durableFailure("cannot re-capture revision pin", error)
    })
    if (!sameResearchAgentRevisionPin(preRevisionPin, revisionPin)) {
      return yield* Effect.fail(
        durableFailure("cannot create consistent run", "workspace changed while planning; retry on a stable revision")
      )
    }
    const run = yield* Effect.try({
      try: () =>
        createResearchAgentRun({
          run_id: runId,
          at,
          plan,
          revision_pin: revisionPin
        }),
      catch: (error) => durableFailure("cannot create run", error)
    })
    const path = yield* Effect.tryPromise({
      try: () => writeNewResearchAgentRun(workspace.root, run),
      catch: (error) => durableFailure("cannot persist run", error)
    })
    return {
      schema: "ice-research-agent-run-create/v1" as const,
      path,
      trace_tip_sha256: run.trace.at(-1)?.event_sha256 ?? null,
      run
    }
  })

export const researchAgentRunReviewData = (
  runId: string,
  stage: HumanReviewStage,
  decision: HumanReviewDecision,
  rationale: string,
  expectedTipSha256: string,
  at = new Date().toISOString()
) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const run = yield* Effect.tryPromise({
      try: () =>
        updateResearchAgentRun(
          workspace.root,
          runId,
          expectedTipSha256,
          async (stored) => {
            const before = await observeResearchAgentRevisionPin(
              workspace.root,
              stored.revision_pin
            )
            const next = applyResearchAgentReview(stored, {
              at,
              stage,
              decision,
              rationale,
              observed_revision_pin: before
            })
            const after = await observeResearchAgentRevisionPin(
              workspace.root,
              stored.revision_pin
            )
            if (!sameResearchAgentRevisionPin(before, after)) {
              throw new Error("workspace changed during locked review; reload and retry")
            }
            const audit = auditResearchAgentRun(next, after)
            if (!audit.passed) {
              throw new Error(`review failed post-update revision audit: ${audit.errors.join("; ")}`)
            }
            return next
          }
        ),
      catch: (error) => durableFailure("cannot apply review", error)
    })
    return {
      schema: "ice-research-agent-run-review/v1" as const,
      path: `.ice/agent-runs/${run.run_id}.json`,
      trace_tip_sha256: run.trace.at(-1)?.event_sha256 ?? null,
      run
    }
  })

export const researchAgentRunAuditData = (runId: string) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const run = yield* Effect.tryPromise({
      try: () => readResearchAgentRun(workspace.root, runId),
      catch: (error) => durableFailure("cannot read run", error)
    })
    const observedRevisionPin = yield* Effect.tryPromise({
      try: () =>
        observeResearchAgentRevisionPin(workspace.root, run.revision_pin),
      catch: (error) => durableFailure("cannot observe revision pin", error)
    })
    return {
      run_id: run.run_id,
      trace_tip_sha256: run.trace.at(-1)?.event_sha256 ?? null,
      audit: auditResearchAgentRun(run, observedRevisionPin)
    }
  })

export const researchAgentRunShowData = (runId: string) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    return yield* Effect.tryPromise({
      try: () => readResearchAgentRun(workspace.root, runId),
      catch: (error) => durableFailure("cannot read run", error)
    })
  })

export const researchAgentRunCreateCommand = (
  runId: string,
  question: string,
  graph: string,
  limit: number,
  depth: number,
  json: boolean
) =>
  researchAgentRunCreateData(runId, question, graph, limit, depth).pipe(
    Effect.tap((result) =>
      json
        ? printJson(result)
        : Console.log(
            [
              `durable run created: ${result.run.run_id}`,
              `path: ${result.path}`,
              `status: ${result.run.status}`,
              `trace tip: ${result.trace_tip_sha256}`,
              "execution/core-progress: NOT AUTHORIZED"
            ].join("\n")
          )
    )
  )

export const researchAgentRunReviewCommand = (
  runId: string,
  stage: HumanReviewStage,
  decision: HumanReviewDecision,
  rationale: string,
  expectedTipSha256: string,
  json: boolean
) =>
  researchAgentRunReviewData(
    runId,
    stage,
    decision,
    rationale,
    expectedTipSha256
  ).pipe(
    Effect.tap((result) =>
      json
        ? printJson(result)
        : Console.log(
            [
              `durable run reviewed: ${result.run.run_id}`,
              `status: ${result.run.status}`,
              `trace tip: ${result.trace_tip_sha256}`,
              "execution/core-progress: NOT AUTHORIZED"
            ].join("\n")
          )
    )
  )

export const researchAgentRunAuditCommand = (
  runId: string,
  json: boolean
) =>
  researchAgentRunAuditData(runId).pipe(
    Effect.tap((result) =>
      json
        ? printJson(result)
        : Console.log(
            [
              `durable run audit: ${result.run_id}`,
              `passed: ${result.audit.passed}`,
              `status: ${result.audit.status}`,
              `trace tip: ${result.trace_tip_sha256}`,
              ...result.audit.errors.map((error) => `[ERROR] ${error}`),
              "execution/core-progress: NOT AUTHORIZED"
            ].join("\n")
          )
    )
  )

export const researchAgentRunShowCommand = (
  runId: string,
  json: boolean
) =>
  researchAgentRunShowData(runId).pipe(
    Effect.tap((run) =>
      json
        ? printJson(run)
        : Console.log(
            [
              `durable run: ${run.run_id}`,
              `status: ${run.status}`,
              `decisions: ${run.decisions.length}`,
              `trace events: ${run.trace.length}`,
              `trace tip: ${run.trace.at(-1)?.event_sha256 ?? "NONE"}`,
              "execution/core-progress: NOT AUTHORIZED"
            ].join("\n")
          )
    )
  )

export const researchAgentWorkflowEvaluateData = Effect.gen(function* () {
  const workspace = yield* Workspace
  const [index, { collection }] = yield* Effect.all(
    [graphRagIndexData, loadValidOntologyCollectionStructure],
    { concurrency: 2 }
  )
  const question =
    "Gate 1 original joint cycle and signed global intersection vector"
  assertToeNavigationProfile(index.units)
  const plan = planResearchAgentWorkflow(
    question,
    searchGraphRag(index, question, { graph: "cpt", limit: 12, depth: 1 })
  )
  const revisionPin = yield* Effect.tryPromise({
    try: () =>
      captureResearchAgentRevisionPin(workspace.root, collection, plan, {
        includeRetrievedDocuments: false
      }),
    catch: (error) => durableFailure("cannot capture evaluation revision pin", error)
  })
  return evaluateResearchAgentWorkflowSuite(index, revisionPin)
})

export const researchAgentWorkflowEvaluateCommand = (json: boolean) =>
  researchAgentWorkflowEvaluateData.pipe(
    Effect.tap((report) =>
      json
        ? printJson(report)
        : Console.log(
            [
              `research-agent workflow suite: ${report.suite.id} (${report.suite.version})`,
              `passed: ${report.cases.filter(({ passed }) => passed).length}/${report.cases.length}`,
              ...report.cases.map(
                (entry) =>
                  `${entry.passed ? "PASS" : "FAIL"} ${entry.id}: ${entry.actual_classification ?? entry.error} -> ${entry.actual_status ?? "ERROR"}`
              ),
              "boundary: routing/handoff evaluation only; no execution or scientific verdict"
            ].join("\n")
          )
    )
  )
