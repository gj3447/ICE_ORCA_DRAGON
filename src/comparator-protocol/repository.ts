import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { iceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { Workspace } from "../workspace.ts"
import {
  COMPARATOR_PROTOCOL_RELPATH,
  decodeIceComparatorProtocol
} from "./model.ts"

const MAX_COMPARATOR_PROTOCOL_BYTES = 1024n * 1024n

/** Reads the fixed design-only protocol without adding it to the canonical ontology. */
export const loadIceComparatorProtocol = Effect.gen(function* () {
  const workspace = yield* Workspace
  const path = yield* Path.Path
  const fs = yield* FileSystem.FileSystem
  if (!isSafeArtifactPath(COMPARATOR_PROTOCOL_RELPATH)) {
    return yield* Effect.fail(
      iceError("COMPARATOR_PROTOCOL_PATH_UNSAFE", "fixed comparator-protocol path is unsafe")
    )
  }
  const root = yield* fs.realPath(workspace.root).pipe(
    Effect.mapError((error) =>
      iceError("COMPARATOR_PROTOCOL_READ_FAILED", `cannot resolve workspace root: ${String(error)}`)
    )
  )
  const candidate = path.resolve(workspace.root, COMPARATOR_PROTOCOL_RELPATH)
  const realPath = yield* fs.realPath(candidate).pipe(
    Effect.mapError((error) =>
      iceError("COMPARATOR_PROTOCOL_READ_FAILED", `cannot resolve comparator protocol: ${String(error)}`)
    )
  )
  if (!isSafeArtifactPath(path.relative(root, realPath))) {
    return yield* Effect.fail(
      iceError(
        "COMPARATOR_PROTOCOL_PATH_ESCAPES_WORKSPACE",
        "comparator protocol resolves outside workspace"
      )
    )
  }
  const info = yield* fs.stat(realPath).pipe(
    Effect.mapError((error) =>
      iceError("COMPARATOR_PROTOCOL_READ_FAILED", `cannot inspect comparator protocol: ${String(error)}`)
    )
  )
  if (info.type !== "File" || info.size > MAX_COMPARATOR_PROTOCOL_BYTES) {
    return yield* Effect.fail(
      iceError("COMPARATOR_PROTOCOL_READ_FAILED", "comparator protocol must be a bounded regular file")
    )
  }
  const contents = yield* fs.readFileString(realPath).pipe(
    Effect.mapError((error) =>
      iceError("COMPARATOR_PROTOCOL_READ_FAILED", `cannot read comparator protocol: ${String(error)}`)
    )
  )
  return yield* Effect.try({
    try: () => decodeIceComparatorProtocol(contents),
    catch: (error) =>
      iceError(
        "COMPARATOR_PROTOCOL_SCHEMA_INVALID",
        error instanceof Error ? error.message : String(error)
      )
  })
})
