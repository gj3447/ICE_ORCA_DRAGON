import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import { scientificIntuitionSearchCommand, scientificIntuitionValidateCommand } from "./commands.ts"

const json = Options.boolean("json").pipe(Options.withDescription("emit machine-readable JSON"))
const query = Args.text({ name: "query" })
const target = Options.text("target").pipe(
  Options.withDescription("required canonical open-problem target: graph::open:id")
)
const limit = Options.integer("limit").pipe(
  Options.withDefault(8),
  Options.withDescription("maximum canonical context hits (1-50)")
)
const depth = Options.integer("depth").pipe(
  Options.withDefault(1),
  Options.withDescription("canonical GraphRAG expansion depth (0-3)")
)

const validate = Command.make("validate", { json }, ({ json }) =>
  scientificIntuitionValidateCommand(json).pipe(
    Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))
  )
).pipe(Command.withDescription("strictly validate the non-authoritative scientific intuition sidecar"))

const search = Command.make(
  "search",
  { query, target, limit, depth, json },
  ({ query, target, limit, depth, json }) =>
    scientificIntuitionSearchCommand(query, target, limit, depth, json)
).pipe(
  Command.withDescription(
    "retrieve source-backed intuition lenses separately from canonical graph context"
  )
)

export const intuitionCommand = Command.make("intuition", {}, () =>
  Console.log(
    "Use `ice intuition --help` to inspect non-authoritative scientific intuition signals."
  )
).pipe(
  Command.withDescription(
    "read-only source-backed hypothesis-generation lenses; never claims or authorizes research"
  ),
  Command.withSubcommands([validate, search])
)
