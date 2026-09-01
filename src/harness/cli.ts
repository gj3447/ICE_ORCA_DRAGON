import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  graphHarnessCheckCommand,
  graphHarnessContextCommand,
  graphHarnessImpactCommand
} from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)

const graph = Options.text("graph").pipe(
  Options.withDefault("all"),
  Options.withDescription("graph key from ontology/collection.json; defaults to all")
)

const depth = Options.integer("depth").pipe(
  Options.withDefault(2),
  Options.withDescription("maximum undirected graph-context depth (0-32)")
)

const limit = Options.integer("limit").pipe(
  Options.withDefault(64),
  Options.withDescription("maximum context nodes returned after depth traversal (1-256)")
)

const nodeId = Args.text({ name: "id" })
const path = Args.text({ name: "path" })

const context = Command.make(
  "context",
  { id: nodeId, depth, limit, json, graph },
  ({ id, depth, limit, json, graph }) =>
    graphHarnessContextCommand(id, depth, limit, json, graph)
).pipe(
  Command.withDescription(
    "show graph-derived evidence, scope, policy, and open-problem context for one node"
  )
)

const impact = Command.make(
  "impact",
  { path, depth, limit, json, graph },
  ({ path, depth, limit, json, graph }) =>
    graphHarnessImpactCommand(path, depth, limit, json, graph)
).pipe(
  Command.withDescription(
    "locate the registered graph context affected by one repository-relative path"
  )
)

const check = Command.make(
  "check",
  { json, graph },
  ({ json, graph }) =>
    graphHarnessCheckCommand(json, graph).pipe(
      Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))
    )
).pipe(
  Command.withDescription(
    "verify graph structure, tracked hashes, and evidence-snapshot provenance"
  )
)

export const harnessCommand = Command.make("harness", {}, () =>
  Console.log("Use `ice harness --help` to inspect the graph-aware research harness.")
).pipe(
  Command.withDescription(
    "graph-aware context, impact, and integrity harness; never auto-authorizes research"
  ),
  Command.withSubcommands([context, impact, check])
)
