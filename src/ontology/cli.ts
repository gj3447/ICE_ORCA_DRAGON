import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  ontologyShowCommand,
  ontologySummaryCommand,
  ontologyTraceCommand,
  ontologyValidateCommand
} from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)

const validateCommand = Command.make(
  "validate",
  { json },
  ({ json }) =>
    ontologyValidateCommand(json).pipe(
      Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "validate schema, graph integrity, artifact hashes, and evidence polarity"
  )
)

const summaryCommand = Command.make(
  "summary",
  { json },
  ({ json }) => ontologySummaryCommand(json)
).pipe(Command.withDescription("summarize ontology nodes, claims, and bridges"))

const nodeId = Args.text({ name: "id" })

const showCommand = Command.make(
  "show",
  { id: nodeId, json },
  ({ id, json }) => ontologyShowCommand(id, json)
).pipe(Command.withDescription("show one node with adjacent edges and KG bridges"))

const depth = Options.integer("depth").pipe(
  Options.withDefault(2),
  Options.withDescription("maximum undirected relation depth (0-32)")
)

const traceCommand = Command.make(
  "trace",
  { id: nodeId, depth, json },
  ({ id, depth, json }) => ontologyTraceCommand(id, depth, json)
).pipe(Command.withDescription("trace the bounded relation neighborhood of one node"))

export const ontologyCommand = Command.make("ontology", {}, () =>
  Console.log("Use `ice ontology --help` to inspect ontology commands.")
).pipe(
  Command.withDescription("query and validate the repository research ontology"),
  Command.withSubcommands([
    validateCommand,
    summaryCommand,
    showCommand,
    traceCommand
  ])
)
