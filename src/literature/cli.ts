import { Args, Command, Options } from "@effect/cli"
import { Console } from "effect"
import { openAlexNeighborhoodCommand, openAlexSearchCommand } from "./commands.ts"
import { MAX_OPENALEX_RESULTS } from "./openalex.ts"

const query = Args.text({ name: "query" })
const limit = Options.integer("limit").pipe(
  Options.withDefault(10),
  Options.withDescription(`maximum OpenAlex works returned (1-${MAX_OPENALEX_RESULTS})`)
)
const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)

const search = Command.make(
  "search",
  { query, limit, json },
  ({ query, limit, json }) => openAlexSearchCommand(query, limit, json)
).pipe(
  Command.withDescription(
    "query OpenAlex's public scholarly works graph for time-stamped discovery metadata"
  )
)

const workId = Args.text({ name: "work-id" })
const neighbors = Command.make(
  "neighbors",
  { workId, limit, json },
  ({ workId, limit, json }) => openAlexNeighborhoodCommand(workId, limit, json)
).pipe(
  Command.withDescription(
    "read a bounded incoming/outgoing/related citation neighborhood from OpenAlex"
  )
)

export const literatureCommand = Command.make("literature", {}, () =>
  Console.log("Use `ice literature --help` to inspect read-only literature discovery commands.")
).pipe(
  Command.withDescription(
    "read-only scholarly discovery; results are not research evidence or execution authorization"
  ),
  Command.withSubcommands([search, neighbors])
)
