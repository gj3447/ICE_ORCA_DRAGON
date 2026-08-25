import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Console, Effect } from "effect"
import { discoverScripts, resolveScript } from "./catalog.ts"
import { doctor } from "./doctor.ts"
import { iceError, type IceError } from "./errors.ts"
import { capture, inherit } from "./process.ts"
import {
  boundedGate1InvocationDecision,
  formatRagnarokStatus,
  guardResearchQuery,
  guardResearchRun,
  researchRunDecision,
  ragnarokStatus
} from "./research-pause.ts"
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
    const fs = yield* FileSystem.FileSystem
    const path = yield* Path.Path
    yield* guardResearchQuery(query)
    const entry = yield* discoverScripts.pipe(
      Effect.flatMap((entries) => resolveScript(entries, query)),
      Effect.flatMap(guardResearchRun)
    )
    const scriptArgs = args[0] === "--" ? args.slice(1) : args
    const decision = researchRunDecision(entry.relpath)
    if (decision.reason === "BOUNDED_GATE1_DIRECT") {
      const invocation = boundedGate1InvocationDecision(
        query,
        entry.relpath,
        scriptArgs
      )
      if (!invocation.allowed) {
        return yield* Effect.fail(
          iceError(
            invocation.reason === "EXACT_NAME_REQUIRED"
              ? "RESEARCH_EXACT_NAME_REQUIRED"
              : "RESEARCH_ARGUMENTS_FORBIDDEN",
            invocation.reason === "EXACT_NAME_REQUIRED"
              ? `bounded Gate-1 execution requires the exact name or relpath '${entry.relpath}'`
              : `bounded Gate-1 execution accepts no script arguments`,
            2
          )
        )
      }
      const caps = ragnarokStatus.gate1_window.resource_caps
      const execution = yield* capture(
        {
          command: workspace.python,
          args: [path.basename(entry.file)],
          cwd: path.dirname(entry.file)
        },
        caps.wall_clock_seconds
      )
      const encoder = new TextEncoder()
      const stdoutBytes = encoder.encode(execution.stdout).byteLength
      const stderrBytes = encoder.encode(execution.stderr).byteLength
      if (stdoutBytes > caps.stdout_bytes || stderrBytes > caps.stderr_bytes) {
        return yield* Effect.fail(
          iceError(
            "RESEARCH_OUTPUT_CAP_EXCEEDED",
            `bounded Gate-1 output exceeded its cap (stdout ${stdoutBytes}/${caps.stdout_bytes}, stderr ${stderrBytes}/${caps.stderr_bytes})`,
            2
          )
        )
      }
      if (execution.stdout.trim().length > 0) {
        yield* Console.log(execution.stdout.trimEnd())
      }
      if (execution.stderr.trim().length > 0) {
        yield* Console.error(execution.stderr.trimEnd())
      }
      if (execution.exitCode === 0) {
        const resultFile = path.join(
          workspace.root,
          ragnarokStatus.gate1_window.result_path
        )
        const resultBytes = yield* fs.readFile(resultFile).pipe(
          Effect.mapError((error) =>
            iceError(
              "RESEARCH_RESULT_MISSING",
              `bounded Gate-1 runner exited zero without a readable result: ${String(error)}`,
              2
            )
          )
        )
        if (resultBytes.byteLength > caps.artifact_bytes) {
          return yield* Effect.fail(
            iceError(
              "RESEARCH_ARTIFACT_CAP_EXCEEDED",
              `bounded Gate-1 result exceeded ${caps.artifact_bytes} bytes (observed ${resultBytes.byteLength})`,
              2
            )
          )
        }
      }
      yield* setExitCode(execution.exitCode)
      return
    }
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

export const researchStatusCommand = (
  json: boolean
): Effect.Effect<void> => Console.log(formatRagnarokStatus(json))

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
