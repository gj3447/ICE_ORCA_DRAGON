import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { iceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { Workspace } from "../workspace.ts"
import {
  decodeScientificIntuitionFlow,
  SCIENTIFIC_INTUITION_FLOW_RELPATH
} from "./model.ts"

const MAX_SIGNAL_DOCUMENT_BYTES = 1024n * 1024n

/** Reads the fixed sidecar without registering it in the canonical ontology collection. */
export const loadScientificIntuitionFlow = Effect.gen(function* () {
  const workspace = yield* Workspace
  const path = yield* Path.Path
  const fs = yield* FileSystem.FileSystem
  if (!isSafeArtifactPath(SCIENTIFIC_INTUITION_FLOW_RELPATH)) {
    return yield* Effect.fail(iceError("INTUITION_PATH_UNSAFE", "fixed intuition sidecar path is unsafe"))
  }
  const root = yield* fs.realPath(workspace.root).pipe(
    Effect.mapError((error) => iceError("INTUITION_READ_FAILED", `cannot resolve workspace root: ${String(error)}`))
  )
  const candidate = path.resolve(workspace.root, SCIENTIFIC_INTUITION_FLOW_RELPATH)
  const realPath = yield* fs.realPath(candidate).pipe(
    Effect.mapError((error) => iceError("INTUITION_READ_FAILED", `cannot resolve intuition sidecar: ${String(error)}`))
  )
  if (!isSafeArtifactPath(path.relative(root, realPath))) {
    return yield* Effect.fail(iceError("INTUITION_PATH_ESCAPES_WORKSPACE", "intuition sidecar resolves outside workspace"))
  }
  const info = yield* fs.stat(realPath).pipe(
    Effect.mapError((error) => iceError("INTUITION_READ_FAILED", `cannot inspect intuition sidecar: ${String(error)}`))
  )
  if (info.type !== "File" || info.size > MAX_SIGNAL_DOCUMENT_BYTES) {
    return yield* Effect.fail(iceError("INTUITION_READ_FAILED", "intuition sidecar must be a bounded regular file"))
  }
  const contents = yield* fs.readFileString(realPath).pipe(
    Effect.mapError((error) => iceError("INTUITION_READ_FAILED", `cannot read intuition sidecar: ${String(error)}`))
  )
  return yield* Effect.try({
    try: () => decodeScientificIntuitionFlow(contents),
    catch: (error) => iceError("INTUITION_SCHEMA_INVALID", error instanceof Error ? error.message : String(error))
  })
})
