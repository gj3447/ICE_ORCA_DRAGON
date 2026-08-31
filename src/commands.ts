import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Console, Effect } from "effect"
import { discoverScripts, resolveScript } from "./catalog.ts"
import { doctor } from "./doctor.ts"
import { iceError, type IceError } from "./errors.ts"
import { capture, inherit } from "./process.ts"
import {
  acquireBoundedGate1SourceLinkLaunch,
  acquireBoundedGate1ZeroLapseLaunch,
  boundedCoreRunCaps,
  boundedGate1InvocationDecision,
  coreResearchRoot,
  decodeBoundedGate1SourceLinkResult,
  decodeBoundedGate1ZeroLapseResult,
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

const nulPaths = (source: string): ReadonlyArray<string> =>
  source.split("\0").filter((value) => value.length > 0)

const inspectBoundedCoreArtifacts: Effect.Effect<
  { readonly files: ReadonlyArray<string>; readonly bytes: number },
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> = Effect.gen(function* () {
  const workspace = yield* Workspace
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  const [tracked, untracked, deleted] = yield* Effect.all(
    [
      capture({
        command: "git",
        args: ["diff", "--name-only", "-z", "--diff-filter=ACMRTUXB", "--", coreResearchRoot],
        cwd: workspace.root
      }),
      capture({
        command: "git",
        args: ["ls-files", "--others", "--exclude-standard", "-z", "--", coreResearchRoot],
        cwd: workspace.root
      }),
      capture({
        command: "git",
        args: ["diff", "--name-only", "-z", "--diff-filter=D", "--", coreResearchRoot],
        cwd: workspace.root
      })
    ],
    { concurrency: 3 }
  )
  for (const result of [tracked, untracked, deleted]) {
    if (result.exitCode !== 0) {
      return yield* Effect.fail(
        iceError(
          "RESEARCH_ARTIFACT_AUDIT_FAILED",
          `cannot inspect bounded core artifacts: ${result.stderr.trim() || `git exited ${result.exitCode}`}`,
          2
        )
      )
    }
  }
  const deletedPaths = nulPaths(deleted.stdout)
  if (deletedPaths.length > 0) {
    return yield* Effect.fail(
      iceError(
        "RESEARCH_DESTRUCTIVE_ARTIFACT_CHANGE",
        `bounded core execution deleted tracked paths: ${deletedPaths.join(", ")}`,
        2
      )
    )
  }
  const files = [...new Set([...nulPaths(tracked.stdout), ...nulPaths(untracked.stdout)])]
  let bytes = 0
  for (const file of files) {
    const info = yield* fs.stat(path.join(workspace.root, file)).pipe(
      Effect.mapError((error) =>
        iceError(
          "RESEARCH_ARTIFACT_AUDIT_FAILED",
          `cannot inspect bounded artifact ${file}: ${String(error)}`,
          2
        )
      )
    )
    if (info.type !== "File") {
      return yield* Effect.fail(
        iceError(
          "RESEARCH_ARTIFACT_AUDIT_FAILED",
          `bounded artifact ${file} is ${info.type}, expected File`,
          2
        )
      )
    }
    bytes += Number(info.size)
  }
  return { files, bytes }
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
    if (decision.reason === "BOUNDED_NEW_CORE") {
      const execution = yield* capture(
        {
          command: workspace.python,
          args: [path.basename(entry.file), ...scriptArgs],
          cwd: path.dirname(entry.file)
        },
        boundedCoreRunCaps.wall_clock_seconds
      )
      const encoder = new TextEncoder()
      const stdoutBytes = encoder.encode(execution.stdout).byteLength
      const stderrBytes = encoder.encode(execution.stderr).byteLength
      if (
        stdoutBytes > boundedCoreRunCaps.stdout_bytes ||
        stderrBytes > boundedCoreRunCaps.stderr_bytes
      ) {
        return yield* Effect.fail(
          iceError(
            "RESEARCH_OUTPUT_CAP_EXCEEDED",
            `bounded core output exceeded its cap (stdout ${stdoutBytes}/${boundedCoreRunCaps.stdout_bytes}, stderr ${stderrBytes}/${boundedCoreRunCaps.stderr_bytes})`,
            2
          )
        )
      }
      const artifacts = yield* inspectBoundedCoreArtifacts
      if (
        artifacts.files.length > boundedCoreRunCaps.changed_artifact_files ||
        artifacts.bytes > boundedCoreRunCaps.changed_artifact_bytes
      ) {
        return yield* Effect.fail(
          iceError(
            "RESEARCH_ARTIFACT_CAP_EXCEEDED",
            `bounded core artifacts exceeded their cap (${artifacts.files.length}/${boundedCoreRunCaps.changed_artifact_files} files, ${artifacts.bytes}/${boundedCoreRunCaps.changed_artifact_bytes} bytes)`,
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
      yield* setExitCode(execution.exitCode)
      return
    }
    if (
      decision.reason === "BOUNDED_GATE1_DIRECT" ||
      decision.reason === "BOUNDED_GATE1_SOURCE_LINK" ||
      decision.reason === "BOUNDED_GATE1_ZERO_LAPSE"
    ) {
      const isSourceLink = decision.reason === "BOUNDED_GATE1_SOURCE_LINK"
      const isZeroLapse = decision.reason === "BOUNDED_GATE1_ZERO_LAPSE"
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
      const window = isZeroLapse
        ? ragnarokStatus.zero_lapse_window
        : isSourceLink
          ? ragnarokStatus.source_link_window
          : ragnarokStatus.gate1_window
      if (isSourceLink) {
        yield* acquireBoundedGate1SourceLinkLaunch
      }
      if (isZeroLapse) {
        yield* acquireBoundedGate1ZeroLapseLaunch
      }
      const caps = window.resource_caps
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
          window.result_path
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
        if (isSourceLink || isZeroLapse) {
          const resultText = yield* Effect.try({
            try: () =>
              new TextDecoder("utf-8", { fatal: true }).decode(resultBytes),
            catch: (error) =>
              iceError(
                "RESEARCH_RESULT_SCHEMA_INVALID",
                `cannot decode the bounded Gate-1 result as UTF-8 JSON: ${String(error)}`,
                2
              )
          })
          if (isZeroLapse) {
            yield* decodeBoundedGate1ZeroLapseResult(resultText)
          } else {
            yield* decodeBoundedGate1SourceLinkResult(resultText)
          }
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
  json: boolean,
  history = false
): Effect.Effect<void> => Console.log(formatRagnarokStatus(json, history))

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
