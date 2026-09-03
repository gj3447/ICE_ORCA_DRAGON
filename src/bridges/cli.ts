import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import {
  bridgeAuditShowCommand,
  bridgeAuditSummaryCommand,
  bridgeAuditValidateCommand
} from "./commands.ts"

const json = Options.boolean("json").pipe(
  Options.withDescription("emit machine-readable JSON")
)
const target = Args.text({ name: "local-id" })

const validate = Command.make("validate", { json }, ({ json }) =>
  bridgeAuditValidateCommand(json).pipe(
    Effect.flatMap((value) => setExitCode(value.valid ? 0 : 1))
  )
).pipe(
  Command.withDescription(
    "verify the read-only unresolved-bridge audit against canonical graphs"
  )
)

const summary = Command.make("summary", { json }, ({ json }) =>
  bridgeAuditSummaryCommand(json)
).pipe(
  Command.withDescription(
    "summarize NO_MATCH, ID_COLLISION, and registry-unavailable outcomes"
  )
)

const show = Command.make("show", { target, json }, ({ target, json }) =>
  bridgeAuditShowCommand(target, json)
).pipe(
  Command.withDescription(
    "show a current unresolved bridge and its non-resolving audit outcome"
  )
)

export const bridgeAuditCommand = Command.make("bridges", {}, () =>
  Console.log("Use `ice bridges --help` to inspect the read-only bridge audit.")
).pipe(
  Command.withDescription("read-only external bridge-resolution audit"),
  Command.withSubcommands([validate, summary, show])
)
