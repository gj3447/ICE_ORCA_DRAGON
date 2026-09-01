import { Args, Command, Options } from "@effect/cli"
import { Console } from "effect"
import { researchAgentPlanCommand } from "./commands.ts"

const question = Args.text({ name: "question" })
const graph = Options.text("graph").pipe(
  Options.withDefault("all"),
  Options.withDescription("ontology graph key; default searches all graphs")
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
    "create a serializable human-review checkpoint from graph retrieval; never invokes a runner"
  )
)

export const researchAgentCommand = Command.make("agent", {}, () =>
  Console.log("Use `ice agent --help` to inspect non-executing research-agent workflow commands.")
).pipe(
  Command.withDescription(
    "human-approved graph agent routing with no automatic calculation or successor task"
  ),
  Command.withSubcommands([plan])
)
