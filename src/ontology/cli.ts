import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  ontologyCrateCommand,
  ontologyExportCommand,
  ontologyGuideCommand,
  ontologyReviewCommand,
  ontologyShaclCommand,
  ontologyShowCommand,
  ontologySparqlCommand,
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

const base = Options.text("base").pipe(
  Options.withDefault("HEAD"),
  Options.withDescription("committed git revision to compare with the working graph")
)

const reviewCommand = Command.make(
  "review",
  { json, graph, base },
  ({ json, graph, base }) => ontologyReviewCommand(json, graph, base)
).pipe(
  Command.withDescription(
    "review deterministic canonical-graph changes against a committed revision"
  )
)

const format = Options.choice(
  "format",
  ["jsonld", "dataset-jsonld", "nquads"] as const
).pipe(
  Options.withDefault("jsonld"),
  Options.withDescription(
    "one-way compatibility JSON-LD, named-dataset JSON-LD, or N-Quads format"
  )
)

const exportCommand = Command.make(
  "export",
  { format, graph },
  ({ format, graph }) => ontologyExportCommand(format, graph)
).pipe(
  Command.withDescription(
    "write a read-only standards projection to stdout; native JSON stays canonical"
  )
)

const shaclCommand = Command.make(
  "shacl",
  { json, graph },
  ({ json, graph }) =>
    ontologyShaclCommand(json, graph).pipe(
      Effect.flatMap((report) => setExitCode(report.conforms ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "run the bundled SHACL 1.0 Core processor against the generated RDF dataset"
  )
)

const sparqlQuery = Args.text({ name: "query" })
const sparqlLimit = Options.integer("limit").pipe(
  Options.withDefault(100),
  Options.withDescription("maximum SELECT rows or RDF quads (1-500)")
)
const timeoutMs = Options.integer("timeout-ms").pipe(
  Options.withDefault(5_000),
  Options.withDescription("in-memory query timeout in milliseconds (1-30000)")
)

const sparqlCommand = Command.make(
  "sparql",
  { query: sparqlQuery, graph, limit: sparqlLimit, timeoutMs },
  ({ query, graph, limit, timeoutMs }) =>
    ontologySparqlCommand(query, graph, limit, timeoutMs)
).pipe(
  Command.withDescription(
    "run bounded read-only SPARQL 1.1 over the generated in-memory RDF dataset"
  )
)

const crateOutput = Args.text({ name: "output-directory" })
const crateCommand = Command.make(
  "crate",
  { outputDirectory: crateOutput, graph, json },
  ({ outputDirectory, graph, json }) =>
    ontologyCrateCommand(outputDirectory, graph, json)
).pipe(
  Command.withDescription(
    "create one non-overwriting RO-Crate 1.3 metadata/export package under output/"
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
    reviewCommand,
    exportCommand,
    shaclCommand,
    sparqlCommand,
    crateCommand,
    showCommand,
    traceCommand
  ])
)
