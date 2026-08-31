import { Args, Command, Options } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Console, Effect, Layer } from "effect"
import {
  doctorCommand,
  listScripts,
  researchStatusCommand,
  reproCommand,
  runScript,
  scriptInfo,
  setExitCode
} from "./commands.ts"
import { type IceError } from "./errors.ts"
import { ontologyCommand } from "./ontology/cli.ts"
import { WorkspaceLive } from "./workspace.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)
const history = Options.boolean("history").pipe(
  Options.withDescription("include immutable historical containment and receipt detail")
)

const list = Command.make("list", { json }, ({ json }) => listScripts(json)).pipe(
  Command.withDescription("list runnable numerical-kernel scripts")
)

const status = Command.make("status", { json, history }, ({ json, history }) =>
  researchStatusCommand(json, history)
).pipe(
  Command.withDescription(
    "show current bounded-runtime status; use --history for immutable historical detail"
  )
)

const scriptName = Args.text({ name: "name" })
const scriptArgs = Args.text({ name: "arg" }).pipe(Args.repeated)

const run = Command.make(
  "run",
  { name: scriptName, scriptArgs },
  ({ name, scriptArgs }) => runScript(name, scriptArgs)
).pipe(Command.withDescription("run one locked Python numerical kernel"))

const info = Command.make("info", { name: scriptName }, ({ name }) =>
  scriptInfo(name)
).pipe(Command.withDescription("show script metadata and mapped result output"))

const doctor = Command.make("doctor", {}, () =>
  doctorCommand.pipe(
    Effect.flatMap((report) => setExitCode(report.ready ? 0 : 1))
  )
).pipe(Command.withDescription("verify both Node and Python lock contracts"))

const only = Options.text("only").pipe(
  Options.repeated,
  Options.withDescription("run one mapped script (repeatable)")
)
const timeoutSeconds = Options.integer("timeout").pipe(
  Options.withDefault(300),
  Options.withDescription("per-kernel timeout in seconds")
)
const mappingList = Options.boolean("list").pipe(
  Options.withDescription("show reproduction mappings without running kernels")
)

const repro = Command.make(
  "repro",
  { only, timeoutSeconds, list: mappingList, json },
  ({ only, timeoutSeconds, list, json }) =>
    reproCommand({ only, timeoutSeconds, list, json }).pipe(
      Effect.flatMap((summary) =>
        setExitCode(summary === undefined || summary.needsAttention === 0 ? 0 : 1)
      )
    )
).pipe(
  Command.withDescription(
    "audit mapped legacy outputs in an isolated, interruption-safe Effect scope"
  )
)

const root = Command.make("ice", {}, () =>
  Console.log("Use `ice --help` to inspect the Effect control plane.")
).pipe(
  Command.withDescription("ICE_ORCA_DRAGON functional workbench control plane"),
  Command.withSubcommands([
    status,
    list,
    run,
    info,
    doctor,
    repro,
    ontologyCommand
  ])
)

const cli = Command.run(root, {
  name: "ICE_ORCA_DRAGON",
  version: "0.1.0"
})

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

cli(process.argv).pipe(
  Effect.catchTag("IceError", (error: IceError) =>
    Console.error(`ice: ${error.code}: ${error.message}`).pipe(
      Effect.zipRight(setExitCode(error.exitCode))
    )
  ),
  Effect.provide(AppLayer),
  NodeRuntime.runMain
)
