import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Console, Effect } from "effect"
import { discoverScripts, resolveScript } from "./catalog.ts"
import { doctor } from "./doctor.ts"
import { iceError, type IceError } from "./errors.ts"
import { inherit } from "./process.ts"
import { outputForScript } from "./repro/manifest.ts"
import {
  listReproCases,
  runRepro,
  type ReproOptions,
  type ReproSummary
} from "./repro/run.ts"
import { Workspace } from "./workspace.ts"

export const setExitCode = (code: number): Effect.Effect<void> =>
  Effect.sync(() => {
    if (code !== 0) {
      process.exitCode = code
    }
  })

export const listScripts = (
  json: boolean
): Effect.Effect<
  void,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> =>
  Effect.gen(function* () {
    const entries = yield* discoverScripts
    if (json) {
      yield* Console.log(
        JSON.stringify(
          entries.map((entry) => ({
            name: entry.name,
            path: `${entry.relpath}.py`,
            doc: entry.doc
          })),
          null,
          2
        )
      )
      return
    }
    yield* Console.log(
      entries
        .map(
          (entry) =>
            `${entry.relpath}${entry.doc.length > 0 ? ` — ${entry.doc}` : ""}`
        )
        .join("\n")
    )
    yield* Console.error(`\n${entries.length} runnable scripts`)
  })

export const runScript = (
  query: string,
  args: ReadonlyArray<string>
): Effect.Effect<
  void,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const path = yield* Path.Path
    const entry = yield* discoverScripts.pipe(
      Effect.flatMap((entries) => resolveScript(entries, query))
    )
    const scriptArgs = args[0] === "--" ? args.slice(1) : args
    const exitCode = yield* inherit({
      command: workspace.python,
      args: [path.basename(entry.file), ...scriptArgs],
      cwd: path.dirname(entry.file)
    })
    yield* setExitCode(exitCode)
  })

export const scriptInfo = (
  query: string
): Effect.Effect<
  void,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> =>
  Effect.gen(function* () {
    const entry = yield* discoverScripts.pipe(
      Effect.flatMap((entries) => resolveScript(entries, query))
    )
    const output = outputForScript(entry.name)
    yield* Console.log(
      [
        `name:    ${entry.name}`,
        `path:    ${entry.relpath}.py`,
        `run:     ice run ${entry.relpath}`,
        ...(entry.doc.length > 0 ? [`doc:     ${entry.doc}`] : []),
        `results: ${output ?? "(no mapped legacy output)"}`
      ].join("\n")
    )
  })

export const doctorCommand: typeof doctor = doctor

export const reproCommand = (
  options: ReproOptions & { readonly list: boolean }
): Effect.Effect<
  ReproSummary | undefined,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> => {
  if (options.timeoutSeconds <= 0) {
    return Effect.fail(
      iceError("INVALID_TIMEOUT", "--timeout must be a positive integer", 2)
    )
  }
  return options.list
    ? listReproCases(options.json).pipe(Effect.as(undefined))
    : runRepro(options)
}
