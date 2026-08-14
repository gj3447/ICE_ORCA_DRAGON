import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Clock, Console, Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { capture } from "../process.ts"
import { Workspace } from "../workspace.ts"
import { compareComputed, decodeJsonObject, type Difference } from "./compare.ts"
import { reproCases, type ReproCase } from "./manifest.ts"

export type ReproStatus =
  | "REPRO"
  | "DRIFT"
  | "EXECUTION_FAILED"
  | "TIMEOUT"
  | "NO_FRESH_OUTPUT"
  | "INVALID_OUTPUT"
  | "NONPORTABLE_FAIL"
  | "SUPERSEDED"

export interface ReproRow {
  readonly name: string
  readonly status: ReproStatus
  readonly detail: string
  readonly durationMs: number
  readonly differences?: ReadonlyArray<Difference>
}

export interface ReproSummary {
  readonly rows: ReadonlyArray<ReproRow>
  readonly reproduced: number
  readonly nonportable: number
  readonly superseded: number
  readonly needsAttention: number
}

export interface ReproOptions {
  readonly only: ReadonlyArray<string>
  readonly timeoutSeconds: number
  readonly json: boolean
}

const statusIsFailure = (status: ReproStatus): boolean =>
  status !== "REPRO" && status !== "SUPERSEDED"

const selectCases = (
  only: ReadonlyArray<string>
): Effect.Effect<ReadonlyArray<ReproCase>, IceError> => {
  if (only.length === 0) {
    return Effect.succeed(reproCases)
  }
  const unknown = [...new Set(only)].filter(
    (name) => !reproCases.some((entry) => entry.name === name)
  )
  return unknown.length === 0
    ? Effect.succeed(
        reproCases.filter((entry) => only.includes(entry.name))
      )
    : Effect.fail(
        iceError(
          "UNKNOWN_REPRO_CASE",
          `unknown mapped script(s): ${unknown.join(", ")}`,
          2
        )
      )
}

const prepareRunRoot = (
  sourceRoot: string,
  runRoot: string
): Effect.Effect<void, IceError, FileSystem.FileSystem | Path.Path | import("@effect/platform/CommandExecutor").CommandExecutor> =>
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    const path = yield* Path.Path
    yield* fs.makeDirectory(runRoot, { recursive: true }).pipe(
      Effect.mapError((error) =>
        iceError("TEMP_COPY_FAILED", `cannot create ${runRoot}: ${String(error)}`)
      )
    )
    const manifest = yield* capture({
      command: "git",
      args: ["ls-files", "-co", "--exclude-standard", "-z"],
      cwd: sourceRoot
    })
    if (manifest.exitCode !== 0) {
      return yield* Effect.fail(
        iceError(
          "TEMP_COPY_FAILED",
          `git ls-files exited ${manifest.exitCode}: ${manifest.stderr.trim()}`
        )
      )
    }

    const files = [...new Set(manifest.stdout.split("\0").filter(Boolean))]
    yield* Effect.forEach(
      files,
      (relativeFile) => {
        const source = path.join(sourceRoot, relativeFile)
        const destination = path.join(runRoot, relativeFile)
        return fs.makeDirectory(path.dirname(destination), { recursive: true }).pipe(
          Effect.zipRight(
            fs.copy(source, destination, {
              overwrite: true,
              preserveTimestamps: true
            })
          ),
          Effect.mapError((error) =>
            iceError(
              "TEMP_COPY_FAILED",
              `cannot copy candidate ${relativeFile}: ${String(error)}`
            )
          )
        )
      },
      { concurrency: 16 }
    )
  })

const baselineFor = (
  root: string,
  entry: ReproCase
): Effect.Effect<
  import("./compare.ts").JsonObject,
  IceError,
  import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  capture({
    command: "git",
    args: ["show", `HEAD:./${entry.output}`],
    cwd: root
  }).pipe(
    Effect.flatMap((result) =>
      result.exitCode === 0
        ? decodeJsonObject(result.stdout, `HEAD:${entry.output}`)
        : Effect.fail(
            iceError(
              "BASELINE_MISSING",
              `${entry.output}: ${result.stderr.trim() || `git exited ${result.exitCode}`}`
            )
          )
    )
  )

const portableCase = (
  entry: Extract<ReproCase, { readonly policy: "portable" }>,
  runRoot: string,
  timeoutSeconds: number
): Effect.Effect<
  ReproRow,
  never,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const fs = yield* FileSystem.FileSystem
    const path = yield* Path.Path
    const started = yield* Clock.currentTimeMillis
    const baseline = yield* baselineFor(workspace.root, entry)
    const scriptPath = path.join(runRoot, entry.script)
    const outputPath = path.join(runRoot, entry.output)

    const scriptExists = yield* fs.exists(scriptPath).pipe(
      Effect.mapError((error) =>
        iceError("SCRIPT_CHECK_FAILED", `${entry.script}: ${String(error)}`)
      )
    )
    if (!scriptExists) {
      return {
        name: entry.name,
        status: "EXECUTION_FAILED" as const,
        detail: `mapped script missing: ${entry.script}`,
        durationMs: (yield* Clock.currentTimeMillis) - started
      }
    }

    yield* fs.remove(outputPath, { force: true }).pipe(
      Effect.mapError((error) =>
        iceError("OUTPUT_REMOVE_FAILED", `${entry.output}: ${String(error)}`)
      )
    )

    const execution = yield* capture(
      {
        command: workspace.python,
        args: [entry.script],
        cwd: runRoot
      },
      timeoutSeconds
    )
    const durationMs = (yield* Clock.currentTimeMillis) - started
    if (execution.exitCode !== 0) {
      const tail = (execution.stderr || execution.stdout).trim().slice(-240)
      return {
        name: entry.name,
        status: "EXECUTION_FAILED" as const,
        detail: `exit ${execution.exitCode}${tail.length > 0 ? `: ${tail}` : ""}`,
        durationMs
      }
    }

    const outputExists = yield* fs.exists(outputPath).pipe(
      Effect.mapError((error) =>
        iceError("OUTPUT_CHECK_FAILED", `${entry.output}: ${String(error)}`)
      )
    )
    if (!outputExists) {
      return {
        name: entry.name,
        status: "NO_FRESH_OUTPUT" as const,
        detail: `exit 0 but did not create ${entry.output}`,
        durationMs
      }
    }

    const source = yield* fs.readFileString(outputPath).pipe(
      Effect.mapError((error) =>
        iceError("OUTPUT_READ_FAILED", `${entry.output}: ${String(error)}`)
      )
    )
    const fresh = yield* decodeJsonObject(source, `fresh:${entry.output}`)
    const differences = compareComputed(baseline, fresh, entry.compare)
    return differences.length === 0
      ? {
          name: entry.name,
          status: "REPRO" as const,
          detail: "structure/types exact; numeric values satisfy field policy",
          durationMs
        }
      : {
          name: entry.name,
          status: "DRIFT" as const,
          detail: differences
            .slice(0, 5)
            .map((difference) => `${difference.path}: ${difference.message}`)
            .join("; "),
          durationMs,
          differences
        }
  }).pipe(
    Effect.catchAll((error: IceError) =>
      Effect.succeed({
        name: entry.name,
        status: error.code === "PROCESS_TIMEOUT" ? "TIMEOUT" : "INVALID_OUTPUT",
        detail: error.message,
        durationMs: 0
      } as const)
    )
  )

const runCase = (
  entry: ReproCase,
  runRoot: string,
  timeoutSeconds: number
): Effect.Effect<
  ReproRow,
  never,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> => {
  if (entry.policy === "nonportable") {
    return Effect.succeed({
      name: entry.name,
      status: "NONPORTABLE_FAIL",
      detail: entry.reason,
      durationMs: 0
    })
  }
  if (entry.policy === "superseded") {
    return Effect.succeed({
      name: entry.name,
      status: "SUPERSEDED",
      detail: entry.reason,
      durationMs: 0
    })
  }
  return portableCase(entry, runRoot, timeoutSeconds)
}

const summarize = (rows: ReadonlyArray<ReproRow>): ReproSummary => ({
  rows,
  reproduced: rows.filter((row) => row.status === "REPRO").length,
  nonportable: rows.filter((row) => row.status === "NONPORTABLE_FAIL").length,
  superseded: rows.filter((row) => row.status === "SUPERSEDED").length,
  needsAttention: rows.filter((row) => statusIsFailure(row.status)).length
})

const printSummary = (
  summary: ReproSummary,
  json: boolean
): Effect.Effect<void> => {
  if (json) {
    return Console.log(JSON.stringify(summary, null, 2))
  }
  const width = Math.max(...summary.rows.map((row) => row.name.length), 1)
  const lines = summary.rows.map(
    (row) =>
      `  ${row.name.padEnd(width)}  ${row.status.padEnd(17)} ${row.detail}`
  )
  return Console.log(
    [
      "ICE mapped legacy-output reproducibility (isolated Effect scope)",
      "",
      ...lines,
      "",
      `REPRO ${summary.reproduced} | NONPORTABLE ${summary.nonportable} | ` +
        `SUPERSEDED ${summary.superseded} | needs-attention ${summary.needsAttention}`
    ].join("\n")
  )
}

export const listReproCases = (json: boolean): Effect.Effect<void> =>
  json
    ? Console.log(JSON.stringify(reproCases, null, 2))
    : Console.log(
        reproCases
          .map(
            (entry) =>
              `${entry.name}.py -> ${entry.output} [${entry.policy.toUpperCase()}]`
          )
          .join("\n")
      )

export const runRepro = (
  options: ReproOptions
): Effect.Effect<
  ReproSummary,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  Effect.scoped(
    Effect.gen(function* () {
      const workspace = yield* Workspace
      const fs = yield* FileSystem.FileSystem
      const path = yield* Path.Path
      const selected = yield* selectCases(options.only)
      const temporary = yield* fs.makeTempDirectoryScoped({ prefix: "ice-repro-" }).pipe(
        Effect.mapError((error) =>
          iceError("TEMP_DIRECTORY_FAILED", `cannot create temp directory: ${String(error)}`)
        )
      )
      const runRoot = path.join(temporary, "repo")
      yield* prepareRunRoot(workspace.root, runRoot)
      const rows = yield* Effect.forEach(
        selected,
        (entry) => runCase(entry, runRoot, options.timeoutSeconds),
        { concurrency: 1 }
      )
      const summary = summarize(rows)
      yield* printSummary(summary, options.json)
      return summary
    })
  )
