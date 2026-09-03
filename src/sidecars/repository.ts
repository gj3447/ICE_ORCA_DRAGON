import { createHash } from "node:crypto"
import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { iceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { Workspace } from "../workspace.ts"
import { SIDECAR_COLLECTION_RELPATH, decodeSidecarCollection } from "./model.ts"

export const SIDECAR_DOCUMENT_PATHS = [
  "research/intuition/scientific-intuition-signals.v1.json",
  "research/intuition/scientific-intuition-signals.v2.json",
  "research/benchmarks/ice-comparator-protocol.v1.json"
] as const
const MAX_BYTES = 1024n * 1024n

export const readFixedSidecarText = (relativePath: typeof SIDECAR_COLLECTION_RELPATH | typeof SIDECAR_DOCUMENT_PATHS[number]) => Effect.gen(function* () {
  const workspace = yield* Workspace
  const path = yield* Path.Path
  const fs = yield* FileSystem.FileSystem
  if (!isSafeArtifactPath(relativePath)) return yield* Effect.fail(iceError("SIDECAR_PATH_UNSAFE", "fixed sidecar path is unsafe"))
  const root = yield* fs.realPath(workspace.root).pipe(Effect.mapError((error) => iceError("SIDECAR_READ_FAILED", `cannot resolve workspace root: ${String(error)}`)))
  const target = yield* fs.realPath(path.resolve(workspace.root, relativePath)).pipe(Effect.mapError((error) => iceError("SIDECAR_READ_FAILED", `cannot resolve sidecar: ${String(error)}`)))
  if (!isSafeArtifactPath(path.relative(root, target))) return yield* Effect.fail(iceError("SIDECAR_PATH_ESCAPES_WORKSPACE", "sidecar resolves outside workspace"))
  const info = yield* fs.stat(target).pipe(Effect.mapError((error) => iceError("SIDECAR_READ_FAILED", `cannot inspect sidecar: ${String(error)}`)))
  if (info.type !== "File" || info.size > MAX_BYTES) return yield* Effect.fail(iceError("SIDECAR_READ_FAILED", "sidecar must be a bounded regular file"))
  const contents = yield* fs.readFileString(target).pipe(Effect.mapError((error) => iceError("SIDECAR_READ_FAILED", `cannot read sidecar: ${String(error)}`)))
  return { contents, sha256: createHash("sha256").update(contents).digest("hex") }
})

export const loadSidecarCollection = readFixedSidecarText(SIDECAR_COLLECTION_RELPATH).pipe(Effect.flatMap(({ contents }) => Effect.try({ try: () => decodeSidecarCollection(contents), catch: (error) => iceError("SIDECAR_COLLECTION_SCHEMA_INVALID", error instanceof Error ? error.message : String(error)) })))
