import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  comparatorProtocolShowCommand,
  comparatorProtocolSummaryCommand,
  comparatorProtocolTraceCommand,
  comparatorProtocolValidateCommand
} from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)
const target = Args.text({ name: "route-entity-id" })
const step = Args.text({ name: "route-step-id" })

const validate = Command.make("validate", { json }, ({ json }) =>
  comparatorProtocolValidateCommand(json).pipe(
    Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))
  )
).pipe(
  Command.withDescription(
    "strictly validate the design-only source-pinned comparator protocol"
  )
)

const summary = Command.make("summary", { json }, ({ json }) =>
  comparatorProtocolSummaryCommand(json)
).pipe(
  Command.withDescription(
    "summarize route lanes, selected strategy, consumers, and solver pins"
  )
)

const show = Command.make("show", { target, json }, ({ target, json }) =>
  comparatorProtocolShowCommand(target, json)
).pipe(
  Command.withDescription("show one exact source, tool, model, consumer, step, or edge")
)

const trace = Command.make("trace", { step, json }, ({ step, json }) =>
  comparatorProtocolTraceCommand(step, json)
).pipe(
  Command.withDescription(
    "trace design prerequisites and descendants without crossing independent lanes"
  )
)

export const comparatorProtocolCommand = Command.make("comparator", {}, () =>
  Console.log(
    "Use `ice comparator --help` to inspect the non-authoritative comparator route."
  )
).pipe(
  Command.withDescription(
    "read-only, design-only robustness and cross-domain comparator protocol"
  ),
  Command.withSubcommands([validate, summary, show, trace])
)
