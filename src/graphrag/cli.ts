import { Args, Command, Options } from "@effect/cli"
import { Console } from "effect"
import { graphRagSearchCommand, graphRagSummaryCommand } from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)
const graph = Options.text("graph").pipe(
  Options.withDefault("all"),
  Options.withDescription("ontology graph key; default searches all graphs")
)
const limit = Options.integer("limit").pipe(
  Options.withDefault(12),
  Options.withDescription("maximum evidence bundles returned (1-50)")
)
const depth = Options.integer("depth").pipe(
  Options.withDefault(1),
  Options.withDescription("bounded explicit-relation expansion depth (0-3)")
)
const query = Args.text({ name: "query" })

const summary = Command.make("summary", { json }, ({ json }) =>
  graphRagSummaryCommand(json)
).pipe(Command.withDescription("summarize the deterministic ontology GraphRAG index"))

const search = Command.make(
  "search",
  { query, graph, limit, depth, json },
  ({ query, graph, limit, depth, json }) =>
    graphRagSearchCommand(query, { graph, limit, depth }, json)
).pipe(
  Command.withDescription(
    "retrieve bounded evidence bundles using BM25, lexical vectors, and explicit graph expansion"
  )
)

export const graphRagCommand = Command.make("graphrag", {}, () =>
  Console.log("Use `ice graphrag --help` to inspect evidence-first GraphRAG commands.")
).pipe(
  Command.withDescription(
    "deterministic local GraphRAG retrieval over canonical ontology records; never executes research"
  ),
  Command.withSubcommands([summary, search])
)
