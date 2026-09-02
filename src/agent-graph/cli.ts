import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  researchAgentPlanCommand,
  researchAgentRunAuditCommand,
  researchAgentRunCreateCommand,
  researchAgentRunReviewCommand,
  researchAgentRunShowCommand,
  researchAgentWorkflowEvaluateCommand
} from "./commands.ts"

const question = Args.text({ name: "question" })
const graph = Options.text("graph").pipe(
  Options.withDefault("cpt"),
  Options.withDescription("ontology graph key; TOE routing defaults to the CPT graph")
)
const limit = Options.integer("limit").pipe(
  Options.withDefault(12),
  Options.withDescription("maximum graph retrieval records (1-50)")
)
const depth = Options.integer("depth").pipe(
  Options.withDefault(1),
  Options.withDescription("bounded relation expansion depth (0-3)")
)
const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)

const plan = Command.make(
  "plan",
  { question, graph, limit, depth, json },
  ({ question, graph, limit, depth, json }) =>
    researchAgentPlanCommand(question, graph, limit, depth, json)
).pipe(
  Command.withDescription(
    "create a TOE critical-path human-review checkpoint; never invokes a runner"
  )
)

const runId = Args.text({ name: "run-id" })
const createRunId = Options.text("id").pipe(
  Options.withDescription("new durable run id (3-128 lowercase safe characters)")
)

const createRun = Command.make(
  "create",
  { question, id: createRunId, graph, limit, depth, json },
  ({ question, id, graph, limit, depth, json }) =>
    researchAgentRunCreateCommand(id, question, graph, limit, depth, json)
).pipe(
  Command.withDescription(
    "explicitly persist one revision-pinned human-review workflow under .ice/agent-runs/"
  )
)

const reviewStage = Options.choice(
  "stage",
  ["route", "evidence", "design"] as const
).pipe(Options.withDescription("human-review stage currently awaiting a decision"))
const reviewDecision = Options.choice(
  "decision",
  ["approve", "stop"] as const
).pipe(
  Options.withDescription("advance one review stage or stop/reframe the workflow")
)
const rationale = Options.text("rationale").pipe(
  Options.withDescription("bounded human rationale recorded in the event chain")
)
const tip = Options.text("tip").pipe(
  Options.withDescription("expected SHA-256 of the currently reviewed trace tip")
)

const reviewRun = Command.make(
  "review",
  {
    id: runId,
    stage: reviewStage,
    decision: reviewDecision,
    rationale,
    tip,
    json
  },
  ({ id, stage, decision, rationale, tip, json }) =>
    researchAgentRunReviewCommand(
      id,
      stage === "route" ? "ROUTE" : stage === "evidence" ? "EVIDENCE" : "DESIGN",
      decision === "approve" ? "APPROVE" : "STOP_OR_REFRAME",
      rationale,
      tip,
      json
    )
).pipe(
  Command.withDescription(
    "append one optimistic-concurrency human decision; never authorize execution"
  )
)

const showRun = Command.make(
  "show",
  { id: runId, json },
  ({ id, json }) => researchAgentRunShowCommand(id, json)
).pipe(Command.withDescription("read one locally persisted durable workflow"))

const auditRun = Command.make(
  "audit",
  { id: runId, json },
  ({ id, json }) =>
    researchAgentRunAuditCommand(id, json).pipe(
      Effect.flatMap((result) => setExitCode(result.audit.passed ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "audit event-chain self-consistency and live code/ontology/source revision drift"
  )
)

const run = Command.make("run", {}, () =>
  Console.log("Use `ice agent run --help` to inspect durable workflow commands.")
).pipe(
  Command.withDescription(
    "explicit local persistence for finite, non-executing human-review workflows"
  ),
  Command.withSubcommands([createRun, reviewRun, showRun, auditRun])
)

const evaluate = Command.make(
  "eval",
  { json },
  ({ json }) =>
    researchAgentWorkflowEvaluateCommand(json).pipe(
      Effect.flatMap((report) => setExitCode(report.passed ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "run the fixed routing, human-handoff, and non-authorization workflow suite"
  )
)

export const researchAgentCommand = Command.make("agent", {}, () =>
  Console.log("Use `ice agent --help` to inspect non-executing research-agent workflow commands.")
).pipe(
  Command.withDescription(
    "human-approved TOE critical-path routing with no automatic calculation or successor task"
  ),
  Command.withSubcommands([plan, evaluate, run])
)
