import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Console, Effect, Schema } from "effect"
import { iceError, type IceError } from "./errors.ts"
import { capture } from "./process.ts"
import { Workspace } from "./workspace.ts"

export interface DoctorCheck {
  readonly name: string
  readonly ok: boolean
  readonly detail: string
}

export interface DoctorReport {
  readonly ready: boolean
  readonly checks: ReadonlyArray<DoctorCheck>
}

const RuntimeReportFromString = Schema.parseJson(
  Schema.Struct({
    python: Schema.String,
    numpy: Schema.String,
    scipy: Schema.String,
    sympy: Schema.String
  })
)

const PackageMetadataFromString = Schema.parseJson(
  Schema.Struct({
    name: Schema.String,
    version: Schema.String
  })
)

const fileCheck = (
  fs: FileSystem.FileSystem,
  path: string,
  name: string
): Effect.Effect<DoctorCheck, IceError> =>
  fs.exists(path).pipe(
    Effect.map((exists) => ({
      name,
      ok: exists,
      detail: exists ? path : `missing ${path}`
    })),
    Effect.mapError((error) =>
      iceError("DOCTOR_FILE_CHECK_FAILED", `${path}: ${String(error)}`)
    )
  )

const installedPackageCheck = (
  fs: FileSystem.FileSystem,
  path: Path.Path,
  root: string,
  packageName: string,
  expected: string
): Effect.Effect<DoctorCheck, IceError> => {
  const packageJson = path.join(root, "node_modules", packageName, "package.json")
  return fs.readFileString(packageJson).pipe(
    Effect.flatMap(Schema.decodeUnknown(PackageMetadataFromString)),
    Effect.map((metadata) => ({
      name: packageName,
      ok: metadata.name === packageName && metadata.version === expected,
      detail: `${metadata.version} (locked ${expected})`
    })),
    Effect.catchAll((error) =>
      Effect.succeed({
        name: packageName,
        ok: false,
        detail: `missing or invalid install: ${String(error)}`
      })
    )
  )
}

const printReport = (report: DoctorReport): Effect.Effect<void> => {
  const width = Math.max(...report.checks.map((check) => check.name.length), 1)
  return Console.log(
    [
      "ICE runtime doctor",
      "",
      ...report.checks.map(
        (check) =>
          `  ${check.ok ? "OK  " : "FAIL"}  ${check.name.padEnd(width)}  ${check.detail}`
      ),
      "",
      report.ready
        ? "READY: Effect control plane and locked Python kernel are consistent"
        : "NOT READY: run `npm ci` and `uv sync --locked`, then retry"
    ].join("\n")
  )
}

export const doctor: Effect.Effect<
  DoctorReport,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> = Effect.gen(function* () {
  const workspace = yield* Workspace
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path

  const nodeMajor = Number.parseInt(process.versions.node.split(".")[0] ?? "0", 10)
  const checks: Array<DoctorCheck> = [
    {
      name: "node",
      ok: nodeMajor === workspace.runtime.nodeMajor,
      detail: `${process.versions.node} (requires ${workspace.runtime.nodeMajor}.x)`
    }
  ]

  checks.push(
    ...(yield* Effect.all([
      fileCheck(fs, path.join(workspace.root, "package-lock.json"), "npm lock"),
      fileCheck(fs, path.join(workspace.root, "uv.lock"), "uv lock"),
      fileCheck(fs, path.join(workspace.root, "pyproject.toml"), "Python project")
    ]))
  )

  checks.push(
    ...(yield* Effect.forEach(
      Object.entries(workspace.runtime.controlPackages),
      ([name, version]) =>
        installedPackageCheck(fs, path, workspace.root, name, version),
      { concurrency: "unbounded" }
    ))
  )

  const lockCheck = yield* capture({
    command: "uv",
    args: ["lock", "--check", "--project", workspace.root],
    cwd: workspace.root
  })
  checks.push({
    name: "uv lock check",
    ok: lockCheck.exitCode === 0,
    detail:
      lockCheck.exitCode === 0
        ? "pyproject.toml agrees with uv.lock"
        : (lockCheck.stderr || lockCheck.stdout).trim()
  })

  const runtime = yield* capture({
    command: "uv",
    args: [
      "run",
      "--project",
      workspace.root,
      "--locked",
      "--no-sync",
      "python",
      "-c",
      "import json,platform,numpy,scipy,sympy; print(json.dumps({'python': platform.python_version(), 'numpy': numpy.__version__, 'scipy': scipy.__version__, 'sympy': sympy.__version__}))"
    ],
    cwd: workspace.root
  })

  if (runtime.exitCode !== 0) {
    checks.push({
      name: "Python runtime",
      ok: false,
      detail: (runtime.stderr || runtime.stdout).trim()
    })
  } else {
    const decoded = yield* Schema.decodeUnknown(RuntimeReportFromString)(runtime.stdout).pipe(
      Effect.mapError((error) =>
        iceError("DOCTOR_RUNTIME_JSON_INVALID", String(error))
      )
    )
    checks.push({
      name: "python",
      ok: decoded.python.startsWith(`${workspace.runtime.pythonMajorMinor}.`),
      detail: `${decoded.python} (locked ${workspace.runtime.pythonMajorMinor}.*)`
    })
    for (const [name, expected] of Object.entries(workspace.runtime.packages)) {
      const actual = decoded[name as keyof typeof decoded]
      checks.push({
        name,
        ok: actual === expected,
        detail: `${actual} (locked ${expected})`
      })
    }
  }

  const report = {
    checks,
    ready: checks.every((check) => check.ok)
  }
  yield* printReport(report)
  return report
})
