import { Effect, Schema } from "effect"
import { iceError, type IceError } from "../errors.ts"
import type { ValidationIssue } from "./core.ts"
import type { ResearchGraph, ResearchNode } from "./model.ts"

const NonEmptyString = Schema.NonEmptyString
const DateTime = Schema.String.pipe(
  Schema.pattern(
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/
  )
)
const Sha256 = Schema.String.pipe(Schema.pattern(/^[a-f0-9]{64}$/))
const CommitHash = Schema.String.pipe(Schema.pattern(/^[a-f0-9]{40}$/))

const RunCheckSchema = Schema.Struct({
  id: Schema.String.pipe(
    Schema.pattern(/^P[0-9]+[A-Z]?\.[A-Za-z0-9_.-]+$/)
  ),
  status: Schema.Literal("PASS", "FAIL", "INCONCLUSIVE"),
  statement: NonEmptyString
})

const RunPayloadSchema = Schema.asSchema(
  Schema.Struct({ exact_checks: Schema.NonNegativeInt }).pipe(
    Schema.extend(
      Schema.Record({ key: Schema.String, value: Schema.Unknown })
    )
  )
)

export const ResearchRunEvidenceSchema = Schema.Struct({
  $schema: Schema.optional(Schema.String),
  schema_version: Schema.Literal("research-run-evidence/v1"),
  result_id: Schema.String.pipe(
    Schema.pattern(/^result:[A-Za-z0-9_.:-]+$/)
  ),
  phase: Schema.String.pipe(Schema.pattern(/^P[0-9]+[A-Z]?$/)),
  observed_at_utc: DateTime,
  command: NonEmptyString,
  exit_code: Schema.Int,
  script: Schema.Struct({
    path: NonEmptyString,
    sha256: Sha256,
    introduced_in_commit: CommitHash
  }),
  exact_checks: Schema.NonNegativeInt,
  checks: Schema.Array(RunCheckSchema),
  numerical_checks: Schema.optional(Schema.NonNegativeInt),
  numerical: Schema.optional(Schema.Array(RunCheckSchema)),
  payload: RunPayloadSchema
})

const ResearchRunEvidenceFromString = Schema.parseJson(
  ResearchRunEvidenceSchema
)

export type ResearchRunEvidence = Schema.Schema.Type<
  typeof ResearchRunEvidenceSchema
>

export const decodeResearchRunEvidence = (
  source: string,
  label: string
): Effect.Effect<ResearchRunEvidence, IceError> =>
  Schema.decodeUnknown(ResearchRunEvidenceFromString)(source, {
    errors: "all",
    onExcessProperty: "error"
  }).pipe(
    Effect.mapError((error) =>
      iceError(
        "ONTOLOGY_EVIDENCE_SCHEMA_INVALID",
        `${label} does not satisfy research-run-evidence/v1: ${String(error)}`
      )
    )
  )

const issue = (
  code: string,
  message: string,
  subject: string
): ValidationIssue => ({ severity: "error", code, message, subject })

const duplicateValues = (
  values: ReadonlyArray<string>
): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const duplicates = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) {
      duplicates.add(value)
    }
    seen.add(value)
  }
  return [...duplicates].sort()
}

type EvidenceArtifact = Extract<
  ResearchNode,
  { readonly type: "artifact" }
>

export const validateEvidenceSnapshot = (
  graph: ResearchGraph,
  artifact: EvidenceArtifact,
  snapshot: ResearchRunEvidence
): ReadonlyArray<ValidationIssue> => {
  const issues: Array<ValidationIssue> = []
  const numericalRecords = snapshot.numerical ?? []
  const snapshotIds = [
    ...snapshot.checks.map((check) => check.id),
    ...numericalRecords.map((check) => check.id)
  ]

  if (snapshot.exact_checks !== snapshot.checks.length) {
    issues.push(
      issue(
        "EVIDENCE_EXACT_CHECKS_MISMATCH",
        `exact_checks is ${snapshot.exact_checks}, but checks contains ${snapshot.checks.length} entries`,
        artifact.id
      )
    )
  }
  if (snapshot.payload.exact_checks !== snapshot.exact_checks) {
    issues.push(
      issue(
        "EVIDENCE_PAYLOAD_EXACT_CHECKS_MISMATCH",
        `payload.exact_checks is ${snapshot.payload.exact_checks}, but exact_checks is ${snapshot.exact_checks}`,
        artifact.id
      )
    )
  }
  if (
    (snapshot.numerical_checks === undefined) !==
    (snapshot.numerical === undefined)
  ) {
    issues.push(
      issue(
        "EVIDENCE_NUMERICAL_LEDGER_INCOMPLETE",
        "numerical_checks and numerical must either both be present or both be absent",
        artifact.id
      )
    )
  }
  if (
    snapshot.numerical_checks !== undefined &&
    snapshot.numerical_checks !== numericalRecords.length
  ) {
    issues.push(
      issue(
        "EVIDENCE_NUMERICAL_CHECKS_MISMATCH",
        `numerical_checks is ${snapshot.numerical_checks}, but numerical contains ${numericalRecords.length} entries`,
        artifact.id
      )
    )
  }
  const payloadNumericalChecks = snapshot.payload.numerical_checks
  if (
    snapshot.numerical_checks !== undefined &&
    payloadNumericalChecks !== snapshot.numerical_checks
  ) {
    issues.push(
      issue(
        "EVIDENCE_PAYLOAD_NUMERICAL_CHECKS_MISMATCH",
        `payload.numerical_checks is ${String(payloadNumericalChecks)}, but numerical_checks is ${snapshot.numerical_checks}`,
        artifact.id
      )
    )
  }
  for (const checkId of duplicateValues(snapshotIds)) {
    issues.push(
      issue(
        "EVIDENCE_DUPLICATE_CHECK_ID",
        `snapshot check id '${checkId}' is not unique`,
        artifact.id
      )
    )
  }

  const nodesById = new Map(graph.nodes.map((node) => [node.id, node]))
  const connectedNodes = graph.edges
    .filter(
      (edge) => edge.relation === "RECORDED_IN" && edge.to === artifact.id
    )
    .flatMap((edge) => {
      const node = nodesById.get(edge.from)
      if (node === undefined || node.type !== "evidence") {
        issues.push(
          issue(
            "EVIDENCE_RECORDED_NODE_NOT_EVIDENCE",
            `RECORDED_IN source '${edge.from}' is not an evidence node`,
            edge.id
          )
        )
        return []
      }
      return [node]
    })

  for (const node of connectedNodes) {
    if (node.check_ids === undefined) {
      issues.push(
        issue(
          "EVIDENCE_GRAPH_GROUP_MISSING_CHECK_IDS",
          `connected evidence node '${node.id}' has no check_ids group`,
          artifact.id
        )
      )
    }
  }

  const graphIds = connectedNodes.flatMap((node) => node.check_ids ?? [])
  for (const checkId of duplicateValues(graphIds)) {
    issues.push(
      issue(
        "EVIDENCE_GRAPH_CHECK_ID_DUPLICATE",
        `graph check id '${checkId}' belongs to more than one connected evidence group`,
        artifact.id
      )
    )
  }

  const snapshotSet = new Set(snapshotIds)
  const graphSet = new Set(graphIds)
  const absentFromGraph = [...snapshotSet]
    .filter((checkId) => !graphSet.has(checkId))
    .sort()
  const absentFromSnapshot = [...graphSet]
    .filter((checkId) => !snapshotSet.has(checkId))
    .sort()
  if (absentFromGraph.length > 0 || absentFromSnapshot.length > 0) {
    issues.push(
      issue(
        "EVIDENCE_CHECK_IDS_MISMATCH",
        `snapshot-only check_ids: [${absentFromGraph.join(", ")}]; graph-only check_ids: [${absentFromSnapshot.join(", ")}]`,
        artifact.id
      )
    )
  }

  return issues
}
