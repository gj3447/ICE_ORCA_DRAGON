import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { createHash } from "node:crypto"
import { Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { Workspace } from "../workspace.ts"
import {
  isSafeArtifactPath,
  makeValidationReport,
  validateGraphSemantics,
  type ValidationIssue,
  type ValidationReport
} from "./core.ts"
import {
  decodeResearchGraph,
  type ResearchGraph,
  type ResearchNode
} from "./model.ts"
import {
  decodeResearchRunEvidence,
  validateEvidenceSnapshot
} from "./run-evidence.ts"

export const ONTOLOGY_GRAPH_RELPATH =
  "ontology/cpt-temporal-folded-susy/graph.json"

export interface LoadedOntology {
  readonly graph: ResearchGraph
  readonly validation: ValidationReport
}

interface ArtifactFileOutcome {
  readonly verified: boolean
  readonly issue?: ValidationIssue
}

interface EvidenceSnapshotOutcome {
  readonly issues: ReadonlyArray<ValidationIssue>
}

type ArtifactNode = Extract<ResearchNode, { readonly type: "artifact" }>

const isEvidenceSnapshotArtifact = (
  node: ResearchNode
): node is ArtifactNode =>
  node.type === "artifact" && node.artifact_kind === "evidence"

const hashBearingNodes = (
  graph: ResearchGraph
): ReadonlyArray<
  Extract<ResearchNode, { readonly type: "artifact" | "policy" }>
> =>
  graph.nodes.filter(
    (node) => node.type === "artifact" || node.type === "policy"
  )

export const loadResearchGraph = Effect.gen(function* () {
  const workspace = yield* Workspace
  const path = yield* Path.Path
  const fs = yield* FileSystem.FileSystem
  const graphPath = path.join(workspace.root, ONTOLOGY_GRAPH_RELPATH)
  const source = yield* fs.readFileString(graphPath).pipe(
    Effect.mapError((error) =>
      iceError(
        "ONTOLOGY_READ_FAILED",
        `cannot read ${ONTOLOGY_GRAPH_RELPATH}: ${String(error)}`
      )
    )
  )
  return yield* decodeResearchGraph(source, ONTOLOGY_GRAPH_RELPATH)
})

export const auditHashBearingFiles = (graph: ResearchGraph) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const path = yield* Path.Path
    const fs = yield* FileSystem.FileSystem
    const rootRealPath = yield* fs.realPath(workspace.root).pipe(
      Effect.catchAll(() => Effect.succeed(workspace.root))
    )

    const outcomes = yield* Effect.forEach(
      hashBearingNodes(graph),
      (node): Effect.Effect<ArtifactFileOutcome> => {
        if (!isSafeArtifactPath(node.path)) {
          return Effect.succeed({ verified: false })
        }
        const fullPath = path.resolve(workspace.root, node.path)
        return fs.realPath(fullPath).pipe(
          Effect.flatMap((realPath) => {
            const relativeRealPath = path.relative(rootRealPath, realPath)
            if (!isSafeArtifactPath(relativeRealPath)) {
              return Effect.succeed<ArtifactFileOutcome>({
                verified: false,
                issue: {
                  severity: "error",
                  code: "HASHED_PATH_ESCAPES_WORKSPACE",
                  message: `path resolves outside the workspace: '${node.path}'`,
                  subject: node.id
                }
              })
            }
            return fs.readFile(realPath).pipe(
              Effect.map((bytes): ArtifactFileOutcome => {
                const observed = createHash("sha256").update(bytes).digest("hex")
                return observed === node.sha256
                  ? { verified: true }
                  : {
                      verified: false,
                      issue: {
                        severity: "error",
                        code: "HASH_MISMATCH",
                        message: `expected ${node.sha256}, observed ${observed}`,
                        subject: node.id
                      }
                    }
              })
            )
          }),
          Effect.catchAll((error) =>
            Effect.succeed<ArtifactFileOutcome>({
              verified: false,
              issue: {
                severity: "error",
                code: "HASHED_FILE_READ_FAILED",
                message: `cannot read '${node.path}': ${String(error)}`,
                subject: node.id
              }
            })
          )
        )
      },
      { concurrency: 8 }
    )

    return {
      verified: outcomes.filter((outcome) => outcome.verified).length,
      issues: outcomes.flatMap((outcome) =>
        outcome.issue === undefined ? [] : [outcome.issue]
      )
    }
  })

export const auditEvidenceSnapshots = (graph: ResearchGraph) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const path = yield* Path.Path
    const fs = yield* FileSystem.FileSystem
    const rootRealPath = yield* fs.realPath(workspace.root).pipe(
      Effect.catchAll(() => Effect.succeed(workspace.root))
    )
    const artifacts = graph.nodes.filter(isEvidenceSnapshotArtifact)

    const outcomes = yield* Effect.forEach(
      artifacts,
      (artifact): Effect.Effect<EvidenceSnapshotOutcome> => {
        if (!isSafeArtifactPath(artifact.path)) {
          return Effect.succeed({
            issues: [
              {
                severity: "error",
                code: "EVIDENCE_SNAPSHOT_PATH_UNSAFE",
                message: `path is not a safe repository-relative path: '${artifact.path}'`,
                subject: artifact.id
              }
            ]
          })
        }
        const fullPath = path.resolve(workspace.root, artifact.path)
        return fs.realPath(fullPath).pipe(
          Effect.flatMap((realPath) => {
            const relativeRealPath = path.relative(rootRealPath, realPath)
            if (!isSafeArtifactPath(relativeRealPath)) {
              return Effect.succeed<EvidenceSnapshotOutcome>({
                issues: [
                  {
                    severity: "error",
                    code: "EVIDENCE_SNAPSHOT_PATH_ESCAPES_WORKSPACE",
                    message: `path resolves outside the workspace: '${artifact.path}'`,
                    subject: artifact.id
                  }
                ]
              })
            }
            return fs.readFileString(realPath).pipe(
              Effect.flatMap((source) =>
                decodeResearchRunEvidence(source, artifact.path)
              ),
              Effect.map(
                (snapshot): EvidenceSnapshotOutcome => ({
                  issues: validateEvidenceSnapshot(graph, artifact, snapshot)
                })
              )
            )
          }),
          Effect.catchAll((error) =>
            Effect.succeed<EvidenceSnapshotOutcome>({
              issues: [
                {
                  severity: "error",
                  code:
                    error._tag === "IceError"
                      ? error.code
                      : "EVIDENCE_SNAPSHOT_READ_FAILED",
                  message:
                    error._tag === "IceError"
                      ? error.message
                      : `cannot read '${artifact.path}': ${String(error)}`,
                  subject: artifact.id
                }
              ]
            })
          )
        )
      },
      { concurrency: 4 }
    )

    return {
      audited: outcomes.length,
      issues: outcomes.flatMap((outcome) => outcome.issues)
    }
  })

export const loadOntologyValidation = Effect.gen(function* () {
  const graph = yield* loadResearchGraph
  const [artifactAudit, evidenceAudit] = yield* Effect.all(
    [auditHashBearingFiles(graph), auditEvidenceSnapshots(graph)],
    { concurrency: 2 }
  )
  const validation = makeValidationReport(
    graph,
    [
      ...validateGraphSemantics(graph),
      ...artifactAudit.issues,
      ...evidenceAudit.issues
    ],
    artifactAudit.verified
  )
  return { graph, validation } satisfies LoadedOntology
})

export const loadValidOntology: Effect.Effect<
  LoadedOntology,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> = loadOntologyValidation.pipe(
  Effect.flatMap((loaded) =>
    loaded.validation.valid
      ? Effect.succeed(loaded)
      : Effect.fail(
          iceError(
            "ONTOLOGY_INVALID",
            `${loaded.validation.errors.length} validation error(s): ${loaded.validation.errors
              .slice(0, 3)
              .map((issue) => issue.code)
              .join(", ")}`
          )
        )
  )
)
