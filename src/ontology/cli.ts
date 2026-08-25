import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  ontologyGuideCommand,
  ontologyShowCommand,
  ontologySummaryCommand,
  ontologyTraceCommand,
  ontologyValidateCommand
} from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)

const graph = Options.text("graph").pipe(
  Options.withDefault("all"),
  Options.withDescription(
    "graph key from ontology/collection.json; default searches or summarizes all"
  )
)

const validateCommand = Command.make(
  "validate",
  { json, graph },
  ({ json, graph }) =>
    ontologyValidateCommand(json, graph).pipe(
      Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "validate schema, graph integrity, artifact hashes, and evidence polarity"
  )
)

const summaryCommand = Command.make(
  "summary",
  { json, graph },
  ({ json, graph }) => ontologySummaryCommand(json, graph)
).pipe(Command.withDescription("summarize ontology nodes, claims, and bridges"))

const nodeId = Args.text({ name: "id" })

const showCommand = Command.make(
  "show",
  { id: nodeId, json, graph },
  ({ id, json, graph }) => ontologyShowCommand(id, json, graph)
).pipe(Command.withDescription("show one node with adjacent edges and KG bridges"))

const depth = Options.integer("depth").pipe(
  Options.withDefault(2),
  Options.withDescription("maximum undirected relation depth (0-32)")
)

const traceCommand = Command.make(
  "trace",
  { id: nodeId, depth, json, graph },
  ({ id, depth, json, graph }) =>
    ontologyTraceCommand(id, depth, json, graph)
).pipe(Command.withDescription("trace the bounded relation neighborhood of one node"))

const guideCommand = Command.make(
  "guide",
  {
    json,
    graph,
    path: Options.text("path").pipe(
      Options.withDefault(""),
      Options.withDescription(
        "show one collection-path or reading-path ID instead of every path"
      )
    )
  },
  ({ json, graph, path }) => ontologyGuideCommand(json, graph, path)
).pipe(
  Command.withDescription(
    "show quick answers, bounded reading paths, and honest coverage gaps"
  )
)

export const ontologyCommand = Command.make("ontology", {}, () =>
  Console.log("Use `ice ontology --help` to inspect ontology commands.")
).pipe(
  Command.withDescription("query and validate the repository research ontology"),
  Command.withSubcommands([
    validateCommand,
    summaryCommand,
    guideCommand,
    showCommand,
    traceCommand
  ])
)
