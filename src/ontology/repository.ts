import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { createHash } from "node:crypto"
import { Effect, Stream } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { Workspace } from "../workspace.ts"
import {
  makeCollectionValidationReport,
  validateCollectionManifest,
  validateCollectionSemantics,
  type CollectionGraph,
  type CollectionValidationReport
} from "./collection-core.ts"
import {
  decodeResearchCollection,
  type ResearchCollection,
  type ResearchGraphDescriptor
} from "./collection.ts"
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
export const ONTOLOGY_COLLECTION_RELPATH = "ontology/collection.json"
const MAX_ONTOLOGY_DOCUMENT_BYTES = 16n * 1024n * 1024n
const COLLECTION_GRAPH_LOAD_BLOCKING_CODES = new Set([
  "COLLECTION_DUPLICATE_GRAPH_KEY",
  "COLLECTION_DUPLICATE_GRAPH_ID",
  "COLLECTION_DUPLICATE_GRAPH_PATH",
  "COLLECTION_GRAPH_PATH_UNSAFE"
])

export interface LoadedOntology {
  readonly graph: ResearchGraph
  readonly validation: ValidationReport
}

export interface LoadedOntologyCollection {
  readonly collection: ResearchCollection
  readonly graphs: ReadonlyArray<CollectionGraph>
  readonly validation: CollectionValidationReport
}

interface ArtifactFileOutcome {
  readonly verified: boolean
  readonly issue?: ValidationIssue
}

interface EvidenceSnapshotOutcome {
  readonly issues: ReadonlyArray<ValidationIssue>
}

interface CollectionPathTarget {
  readonly key: string
  readonly relpath: string
  readonly expectedType: "File" | "Directory"
}

type ArtifactNode = Extract<ResearchNode, { readonly type: "artifact" }>

const resolveContainedWorkspacePath = (
  relpath: string,
  readErrorCode: string,
  escapeErrorCode: string
) =>
  Effect.gen(function* () {
    if (!isSafeArtifactPath(relpath)) {
      return yield* Effect.fail(
        iceError(readErrorCode, `unsafe repository-relative path '${relpath}'`)
      )
    }
    const workspace = yield* Workspace
    const path = yield* Path.Path
    const fs = yield* FileSystem.FileSystem
    const rootRealPath = yield* fs.realPath(workspace.root).pipe(
      Effect.mapError((error) =>
        iceError(
          readErrorCode,
          `cannot resolve workspace root: ${String(error)}`
        )
      )
    )
    const target = path.resolve(workspace.root, relpath)
    const realPath = yield* fs.realPath(target).pipe(
      Effect.mapError((error) =>
        iceError(readErrorCode, `cannot resolve ${relpath}: ${String(error)}`)
      )
    )
    const relativeRealPath = path.relative(rootRealPath, realPath)
    if (!isSafeArtifactPath(relativeRealPath)) {
      return yield* Effect.fail(
        iceError(
          escapeErrorCode,
          `path resolves outside the workspace: '${relpath}'`
        )
      )
    }
    return realPath
  })

const readContainedWorkspaceFileString = (
  relpath: string,
  readErrorCode: string,
  escapeErrorCode: string
) =>
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    const realPath = yield* resolveContainedWorkspacePath(
      relpath,
      readErrorCode,
      escapeErrorCode
    )
    const info = yield* fs.stat(realPath).pipe(
      Effect.mapError((error) =>
        iceError(readErrorCode, `cannot inspect ${relpath}: ${String(error)}`)
      )
    )
    if (info.type !== "File") {
      return yield* Effect.fail(
        iceError(readErrorCode, `${relpath} is ${info.type}, expected File`)
      )
    }
    if (info.size > MAX_ONTOLOGY_DOCUMENT_BYTES) {
      return yield* Effect.fail(
        iceError(
          readErrorCode,
          `${relpath} is ${String(info.size)} bytes; ontology JSON limit is ${String(MAX_ONTOLOGY_DOCUMENT_BYTES)}`
        )
      )
    }
    return yield* fs.readFileString(realPath).pipe(
      Effect.mapError((error) =>
        iceError(readErrorCode, `cannot read ${relpath}: ${String(error)}`)
      )
    )
  })

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

export const loadResearchGraphAt = (relpath: string) =>
  Effect.gen(function* () {
    const source = yield* readContainedWorkspaceFileString(
      relpath,
      "ONTOLOGY_READ_FAILED",
      "ONTOLOGY_GRAPH_PATH_ESCAPES_WORKSPACE"
    )
    return yield* decodeResearchGraph(source, relpath)
  })

export const loadResearchGraph = loadResearchGraphAt(ONTOLOGY_GRAPH_RELPATH)

export const loadResearchCollection = Effect.gen(function* () {
  const source = yield* readContainedWorkspaceFileString(
    ONTOLOGY_COLLECTION_RELPATH,
    "ONTOLOGY_COLLECTION_READ_FAILED",
    "ONTOLOGY_COLLECTION_PATH_ESCAPES_WORKSPACE"
  )
  return yield* decodeResearchCollection(source, ONTOLOGY_COLLECTION_RELPATH)
})

export const auditCollectionDescriptorPaths = (
  collection: ResearchCollection
) =>
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    const rawTargets: ReadonlyArray<CollectionPathTarget> = [
      ...collection.graphs.flatMap((descriptor) => [
        {
          key: descriptor.key,
          relpath: descriptor.guide,
          expectedType: "File" as const
        },
        ...descriptor.corpus_roots.map((relpath) => ({
          key: descriptor.key,
          relpath,
          expectedType: "Directory" as const
        }))
      ]),
      ...collection.coverage_ledger.map((entry) => ({
        key: `coverage:${entry.path}`,
        relpath: entry.path,
        expectedType: "Directory" as const
      }))
    ]
    const targets = [
      ...new Map(
        rawTargets.map((target) => [
          `${target.expectedType}:${target.relpath}`,
          target
        ])
      ).values()
    ]
    const outcomes = yield* Effect.forEach(
      targets,
      (target) =>
        resolveContainedWorkspacePath(
          target.relpath,
          "ONTOLOGY_COLLECTION_PATH_READ_FAILED",
          "ONTOLOGY_COLLECTION_PATH_ESCAPES_WORKSPACE"
        ).pipe(
          Effect.flatMap((realPath) => fs.stat(realPath)),
          Effect.map((info): ValidationIssue | undefined =>
            info.type === target.expectedType
              ? undefined
              : {
                  severity: "error",
                  code: "COLLECTION_PATH_TYPE_MISMATCH",
                  message: `'${target.relpath}' is ${info.type}, expected ${target.expectedType}`,
                  subject: target.key
                }
          ),
          Effect.catchAll((error) =>
            Effect.succeed<ValidationIssue>({
              severity: "error",
              code:
                error._tag === "IceError"
                  ? error.code
                  : "ONTOLOGY_COLLECTION_PATH_READ_FAILED",
              message:
                error._tag === "IceError"
                  ? error.message
                  : `cannot inspect '${target.relpath}': ${String(error)}`,
              subject: target.key
            })
          )
        ),
      { concurrency: 8 }
    )
    return outcomes.flatMap((outcome) =>
      outcome === undefined ? [] : [outcome]
    )
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
            return fs.stream(realPath).pipe(
              Stream.runFold(createHash("sha256"), (hash, bytes) =>
                hash.update(bytes)
              ),
              Effect.map((hash): ArtifactFileOutcome => {
                const observed = hash.digest("hex")
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
      { concurrency: 4 }
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
    const artifacts = graph.nodes.filter(isEvidenceSnapshotArtifact)

    const outcomes = yield* Effect.forEach(
      artifacts,
      (
        artifact
      ): Effect.Effect<
        EvidenceSnapshotOutcome,
        never,
        Workspace | FileSystem.FileSystem | Path.Path
      > => {
        if (!isSafeArtifactPath(artifact.path)) {
          return Effect.succeed<EvidenceSnapshotOutcome>({
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
        return readContainedWorkspaceFileString(
          artifact.path,
          "EVIDENCE_SNAPSHOT_READ_FAILED",
          "EVIDENCE_SNAPSHOT_PATH_ESCAPES_WORKSPACE"
        ).pipe(
          Effect.flatMap((source) =>
            decodeResearchRunEvidence(source, artifact.path)
          ),
          Effect.map(
            (snapshot): EvidenceSnapshotOutcome => ({
              issues: validateEvidenceSnapshot(graph, artifact, snapshot)
            })
          ),
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

export const loadOntologyValidationAt = (relpath: string) =>
  Effect.gen(function* () {
    const graph = yield* loadResearchGraphAt(relpath)
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

export const loadOntologyValidation = loadOntologyValidationAt(
  ONTOLOGY_GRAPH_RELPATH
)

const loadOntologyStructureAt = (relpath: string) =>
  Effect.gen(function* () {
    const graph = yield* loadResearchGraphAt(relpath)
    const validation = makeValidationReport(
      graph,
      validateGraphSemantics(graph)
    )
    return { graph, validation } satisfies LoadedOntology
  })

const failedGraphValidationReport = (
  descriptor: ResearchGraphDescriptor,
  error: IceError
): ValidationReport => ({
  graph_id: descriptor.graph_id,
  schema_version: "research-graph/v1",
  valid: false,
  counts: {
    nodes: 0,
    edges: 0,
    artifacts: 0,
    policies: 0,
    hash_bearing_nodes: 0,
    verified_hashes: 0
  },
  errors: [
    {
      severity: "error",
      code: error.code,
      message: error.message,
      subject: descriptor.key
    }
  ],
  warnings: []
})

type OntologyGraphLoader = (
  relpath: string
) => Effect.Effect<
  LoadedOntology,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
>

const loadOntologyCollectionWith = (loadGraphAt: OntologyGraphLoader) =>
  Effect.gen(function* () {
    const collection = yield* loadResearchCollection
    const manifestIssues = validateCollectionManifest(collection)
    if (
      manifestIssues.some(
        ({ severity, code }) =>
          severity === "error" &&
          COLLECTION_GRAPH_LOAD_BLOCKING_CODES.has(code)
      )
    ) {
      const validation = makeCollectionValidationReport(
        collection,
        [],
        manifestIssues,
        []
      )
      return {
        collection,
        graphs: [],
        validation
      } satisfies LoadedOntologyCollection
    }

    const descriptorPathIssues =
      yield* auditCollectionDescriptorPaths(collection)
    const attempts = yield* Effect.forEach(
      collection.graphs,
      (descriptor) =>
        loadGraphAt(descriptor.path).pipe(
          Effect.either,
          Effect.map((result) => ({ descriptor, result }))
        ),
      { concurrency: 2 }
    )
    const graphs: Array<CollectionGraph> = []
    const graphReports: Array<ValidationReport> = []
    for (const attempt of attempts) {
      if (attempt.result._tag === "Left") {
        graphReports.push(
          failedGraphValidationReport(attempt.descriptor, attempt.result.left)
        )
      } else {
        const loaded: CollectionGraph = {
          descriptor: attempt.descriptor,
          graph: attempt.result.right.graph,
          validation: attempt.result.right.validation
        }
        graphs.push(loaded)
        graphReports.push(loaded.validation)
      }
    }
    const collectionIssues = [
      ...descriptorPathIssues,
      ...validateCollectionSemantics(collection, graphs)
    ]
    const validation = makeCollectionValidationReport(
      collection,
      graphs,
      collectionIssues,
      graphReports
    )
    return {
      collection,
      graphs,
      validation
    } satisfies LoadedOntologyCollection
  })

export const loadOntologyCollectionValidation = loadOntologyCollectionWith(
  loadOntologyValidationAt
)

export const loadOntologyCollectionStructure = loadOntologyCollectionWith(
  loadOntologyStructureAt
)

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

export const loadValidOntologyCollection: Effect.Effect<
  LoadedOntologyCollection,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> = loadOntologyCollectionValidation.pipe(
  Effect.flatMap((loaded) =>
    loaded.validation.valid
      ? Effect.succeed(loaded)
      : Effect.fail(
          iceError(
            "ONTOLOGY_COLLECTION_INVALID",
            `${loaded.validation.errors.length} collection validation error(s): ${loaded.validation.errors
              .slice(0, 3)
              .map((entry) => entry.code)
              .join(", ")}`
          )
        )
  )
)

export const loadValidOntologyCollectionStructure: Effect.Effect<
  LoadedOntologyCollection,
  IceError,
  Workspace | FileSystem.FileSystem | Path.Path
> = loadOntologyCollectionStructure.pipe(
  Effect.flatMap((loaded) =>
    loaded.validation.valid
      ? Effect.succeed(loaded)
      : Effect.fail(
          iceError(
            "ONTOLOGY_COLLECTION_INVALID",
            `${loaded.validation.errors.length} collection validation error(s): ${loaded.validation.errors
              .slice(0, 3)
              .map((entry) => entry.code)
              .join(", ")}`
          )
        )
  )
)
