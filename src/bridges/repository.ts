import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { iceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { Workspace } from "../workspace.ts"
import {
  BRIDGE_AUDIT_RELPATH,
  decodeBridgeResolutionAudit
} from "./core.ts"

const MAX_BRIDGE_AUDIT_BYTES = 1024n * 1024n

export const loadBridgeResolutionAudit = Effect.gen(function* () {
  const workspace = yield* Workspace
  const path = yield* Path.Path
  const fs = yield* FileSystem.FileSystem
  if (!isSafeArtifactPath(BRIDGE_AUDIT_RELPATH)) {
    return yield* Effect.fail(
      iceError("BRIDGE_AUDIT_PATH_UNSAFE", "fixed bridge-audit path is unsafe")
    )
  }
  const root = yield* fs.realPath(workspace.root).pipe(
    Effect.mapError((error) =>
      iceError("BRIDGE_AUDIT_READ_FAILED", `cannot resolve workspace root: ${String(error)}`)
    )
  )
  const candidate = path.resolve(workspace.root, BRIDGE_AUDIT_RELPATH)
  const realPath = yield* fs.realPath(candidate).pipe(
    Effect.mapError((error) =>
      iceError("BRIDGE_AUDIT_READ_FAILED", `cannot resolve bridge audit: ${String(error)}`)
    )
  )
  if (path.relative(root, realPath) !== BRIDGE_AUDIT_RELPATH) {
    return yield* Effect.fail(
      iceError(
        "BRIDGE_AUDIT_PATH_SUBSTITUTED",
        "bridge audit must resolve to its exact fixed repository path"
      )
    )
  }
  const info = yield* fs.stat(realPath).pipe(
    Effect.mapError((error) =>
      iceError("BRIDGE_AUDIT_READ_FAILED", `cannot inspect bridge audit: ${String(error)}`)
    )
  )
  if (info.type !== "File" || info.size > MAX_BRIDGE_AUDIT_BYTES) {
    return yield* Effect.fail(
      iceError(
        "BRIDGE_AUDIT_READ_FAILED",
        "bridge audit must be a bounded regular file"
      )
    )
  }
  const source = yield* fs.readFileString(realPath).pipe(
    Effect.mapError((error) =>
      iceError("BRIDGE_AUDIT_READ_FAILED", `cannot read bridge audit: ${String(error)}`)
    )
  )
  return yield* Effect.try({
    try: () => decodeBridgeResolutionAudit(source),
    catch: (error) =>
      iceError(
        "BRIDGE_AUDIT_SCHEMA_INVALID",
        error instanceof Error ? error.message : String(error)
      )
  })
})
