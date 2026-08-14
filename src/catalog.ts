import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { iceError, type IceError } from "./errors.ts"
import { Workspace } from "./workspace.ts"

export interface ScriptEntry {
  readonly name: string
  readonly relpath: string
  readonly file: string
  readonly doc: string
}

const mainGuard = /if\s+__name__\s*==\s*["']__main__["']\s*:/
const skippedDirectories = new Set([
  ".git",
  ".venv",
  "node_modules",
  "_archive",
  "_findings",
  "papers",
  "docs",
  "tests",
  "test",
  "__pycache__"
])
const excludedFiles = new Set(["repro_check.py"])

const extractDocLine = (source: string): string => {
  const withoutShebang = source.replace(/^#![^\n]*\n/, "")
  const docstring = withoutShebang.match(/^\s*(?:[rubfRUBF]*)?(?:"""|''')([\s\S]*?)(?:"""|''')/)
  if (docstring?.[1] !== undefined) {
    return docstring[1].trim().split(/\r?\n/, 1)[0]?.trim() ?? ""
  }
  for (const line of withoutShebang.split(/\r?\n/)) {
    const trimmed = line.trim()
    if (trimmed.startsWith("#")) {
      return trimmed.replace(/^#+\s*/, "")
    }
    if (trimmed.length > 0) {
      break
    }
  }
  return ""
}

const isSkipped = (relativePath: string): boolean => {
  const parts = relativePath.split("/")
  const directories = parts.slice(0, -1)
  return (
    directories.some(
      (part) => skippedDirectories.has(part) || part.startsWith(".")
    ) ||
    relativePath.split("/").at(-1)?.startsWith("_") === true ||
    excludedFiles.has(relativePath)
  )
}

export const discoverScripts: Effect.Effect<
  ReadonlyArray<ScriptEntry>,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> = Effect.gen(function* () {
  const workspace = yield* Workspace
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  const files = yield* fs.readDirectory(workspace.root, { recursive: true }).pipe(
    Effect.mapError((error) =>
      iceError("CATALOG_READ_FAILED", `cannot scan ${workspace.root}: ${String(error)}`)
    )
  )

  const candidates = files
    .map((file) => file.replaceAll("\\", "/"))
    .filter((file) => file.endsWith(".py") && !isSkipped(file))

  const entries = yield* Effect.forEach(
    candidates,
    (relativeFile) =>
      fs.readFileString(path.join(workspace.root, relativeFile)).pipe(
        Effect.map((source): ScriptEntry | undefined => {
          if (!mainGuard.test(source)) {
            return undefined
          }
          const relpath = relativeFile.slice(0, -3)
          return {
            name: path.basename(relativeFile, ".py"),
            relpath,
            file: path.join(workspace.root, relativeFile),
            doc: extractDocLine(source)
          }
        }),
        Effect.mapError((error) =>
          iceError(
            "CATALOG_READ_FAILED",
            `cannot read ${relativeFile}: ${String(error)}`
          )
        )
      ),
    { concurrency: 16 }
  )

  return entries
    .filter((entry): entry is ScriptEntry => entry !== undefined)
    .sort((left, right) => left.relpath.localeCompare(right.relpath))
})

export const resolveScript = (
  entries: ReadonlyArray<ScriptEntry>,
  query: string
): Effect.Effect<ScriptEntry, IceError> => {
  const normalized = query.endsWith(".py") ? query.slice(0, -3) : query
  const exact = entries.filter(
    (entry) => normalized === entry.name || normalized === entry.relpath
  )
  if (exact.length === 1 && exact[0] !== undefined) {
    return Effect.succeed(exact[0])
  }
  const prefixes = entries.filter(
    (entry) =>
      entry.name.startsWith(normalized) || entry.relpath.startsWith(normalized)
  )
  if (prefixes.length === 1 && prefixes[0] !== undefined) {
    return Effect.succeed(prefixes[0])
  }
  if (prefixes.length === 0) {
    return Effect.fail(
      iceError(
        "SCRIPT_NOT_FOUND",
        `no runnable script matches '${query}' (see \`ice list\`)`,
        2
      )
    )
  }
  return Effect.fail(
    iceError(
      "SCRIPT_AMBIGUOUS",
      `ambiguous prefix '${query}' matches ${prefixes.length} scripts:\n${prefixes
        .map((entry) => `  ${entry.relpath}`)
        .join("\n")}`,
      2
    )
  )
}
