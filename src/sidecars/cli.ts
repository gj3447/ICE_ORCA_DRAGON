import { Args, Command, Options } from "@effect/cli"
import { Console, Effect } from "effect"
import { setExitCode } from "../commands.ts"
import { sidecarCollectionShowCommand, sidecarCollectionSummaryCommand, sidecarCollectionValidateCommand } from "./commands.ts"
const json = Options.boolean("json").pipe(Options.withDescription("emit machine-readable JSON"))
const id = Args.text({ name: "sidecar-id" })
const validate = Command.make("validate", { json }, () => sidecarCollectionValidateCommand().pipe(Effect.flatMap((report) => setExitCode(report.valid ? 0 : 1))))
const summary = Command.make("summary", { json }, () => sidecarCollectionSummaryCommand())
const show = Command.make("show", { id, json }, ({ id }) => sidecarCollectionShowCommand(id))
export const sidecarCollectionCommand = Command.make("sidecars", {}, () => Console.log("Use `ice sidecars --help` to inspect non-authoritative sidecars.")).pipe(Command.withDescription("read-only non-authoritative sidecar registry"), Command.withSubcommands([validate, summary, show]))
