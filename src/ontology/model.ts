import { Effect, Schema } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { assertSupportedResearchSchemaVersion } from "./lifecycle.ts"

const NonEmptyString = Schema.NonEmptyString
const GraphId = Schema.String.pipe(
  Schema.pattern(/^research-graph:[a-z0-9-]+$/)
)
const EntityId = Schema.String.pipe(
  Schema.pattern(/^[a-z_]+:[A-Za-z0-9_.:-]+$/)
)
const EdgeId = Schema.String.pipe(Schema.pattern(/^edge:[0-9]+$/))
const Sha256 = Schema.String.pipe(Schema.pattern(/^[a-f0-9]{64}$/))
const CommitHash = Schema.String.pipe(Schema.pattern(/^[a-f0-9]{40}$/))
const DateTime = Schema.String.pipe(
  Schema.pattern(
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/
  )
)
const StringArray = Schema.Array(NonEmptyString)
const StringRecord = Schema.Record({ key: Schema.String, value: Schema.String })

const commonNodeFields = {
  id: EntityId,
  title: NonEmptyString,
  summary: NonEmptyString,
  state: NonEmptyString
}

const optionalNodeFields = {
  claim_id: Schema.optional(NonEmptyString),
  statement: Schema.optional(NonEmptyString),
  epistemic_state: Schema.optional(
    Schema.Literal("SUPPORTED", "CONTRADICTED", "INCONCLUSIVE")
  ),
  observed_status: Schema.optional(NonEmptyString),
  check_ids: Schema.optional(StringArray),
  includes: Schema.optional(Schema.Array(Schema.String)),
  excludes: Schema.optional(Schema.Array(Schema.String)),
  question: Schema.optional(NonEmptyString),
  citation: Schema.optional(NonEmptyString),
  uri: Schema.optional(NonEmptyString),
  version: Schema.optional(NonEmptyString),
  content_hashes: Schema.optional(StringRecord),
  source_anchors: Schema.optional(StringArray),
  path: Schema.optional(NonEmptyString),
  sha256: Schema.optional(Sha256),
  introduced_in_commit: Schema.optional(CommitHash),
  artifact_kind: Schema.optional(NonEmptyString)
}

const BasicNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("programme", "phase", "concept")
})

const ClaimNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("claim"),
  claim_id: NonEmptyString,
  statement: NonEmptyString,
  epistemic_state: Schema.Literal("SUPPORTED", "CONTRADICTED", "INCONCLUSIVE")
})

const EvidenceNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("evidence"),
  observed_status: NonEmptyString
})

const ScopeNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("scope"),
  includes: Schema.Array(Schema.String),
  excludes: Schema.Array(Schema.String)
})

const OpenProblemNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("open_problem"),
  question: NonEmptyString
})

const SourceNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("source"),
  citation: NonEmptyString,
  uri: NonEmptyString,
  version: NonEmptyString
})

const ArtifactNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("artifact"),
  artifact_kind: NonEmptyString,
  path: NonEmptyString,
  sha256: Sha256,
  introduced_in_commit: Schema.optional(CommitHash)
})

const PolicyNodeSchema = Schema.Struct({
  ...commonNodeFields,
  ...optionalNodeFields,
  type: Schema.Literal("policy"),
  path: NonEmptyString,
  sha256: Sha256,
  introduced_in_commit: CommitHash
})

export const ResearchNodeSchema = Schema.Union(
  BasicNodeSchema,
  ClaimNodeSchema,
  EvidenceNodeSchema,
  ScopeNodeSchema,
  OpenProblemNodeSchema,
  SourceNodeSchema,
  ArtifactNodeSchema,
  PolicyNodeSchema
)

export const EvidencePolaritySchema = Schema.Literal("SUPPORTS", "CONTRADICTS")

export const RelationSchema = Schema.Literal(
  "PART_OF",
  "ABOUT",
  "HAS_EVIDENCE",
  "DEFINED_IN",
  "RECORDED_IN",
  "DERIVED_FROM",
  "DOCUMENTED_BY",
  "DOCUMENTS",
  "IMPLEMENTS",
  "RECORDS",
  "VALID_WITHIN",
  "BLOCKED_BY",
  "MOTIVATES",
  "EXTENDS",
  "FOLLOW_UP_TO",
  "CONTRASTS_WITH",
  "CITES",
  "USES_TOOLING",
  "GOVERNED_BY"
)

export const ResearchEdgeSchema = Schema.Struct({
  id: EdgeId,
  from: EntityId,
  relation: RelationSchema,
  to: EntityId,
  polarity: Schema.optional(EvidencePolaritySchema),
  note: Schema.optional(NonEmptyString)
})

const QuickAnswerSchema = Schema.Struct({
  question: NonEmptyString,
  answer: NonEmptyString,
  claim_ids: Schema.NonEmptyArray(
    Schema.String.pipe(Schema.pattern(/^claim:/))
  )
})

const ReadingPathSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.pattern(/^reading-path:/)),
  title: NonEmptyString,
  summary: NonEmptyString,
  nodes: Schema.NonEmptyArray(EntityId)
})

export const KgBridgeSchema = Schema.Struct({
  local_node_id: EntityId,
  system: NonEmptyString,
  external_uid: Schema.NullOr(Schema.String),
  relation: Schema.NullOr(Schema.String),
  status: Schema.Literal("RESOLVED", "UNRESOLVED"),
  checked_at_utc: DateTime,
  registry: Schema.optional(Schema.String),
  lookup_key: Schema.optional(Schema.String),
  note: Schema.optional(Schema.String)
})

export const ResearchGraphSchema = Schema.Struct({
  $schema: Schema.optional(Schema.String),
  schema_version: Schema.Literal("research-graph/v1"),
  graph_id: GraphId,
  title: NonEmptyString,
  description: NonEmptyString,
  updated_at_utc: DateTime,
  canonical_file: NonEmptyString,
  source_inventory: NonEmptyString,
  quick_answers: Schema.Array(QuickAnswerSchema),
  reading_paths: Schema.Array(ReadingPathSchema),
  node_type_legend: StringRecord,
  relation_legend: StringRecord,
  nodes: Schema.Array(ResearchNodeSchema),
  edges: Schema.Array(ResearchEdgeSchema),
  kg_bridges: Schema.Array(KgBridgeSchema)
})

const ResearchGraphFromString = Schema.parseJson(ResearchGraphSchema)

export type ResearchNode = Schema.Schema.Type<typeof ResearchNodeSchema>
export type ResearchEdge = Schema.Schema.Type<typeof ResearchEdgeSchema>
export type KgBridge = Schema.Schema.Type<typeof KgBridgeSchema>
export type ResearchGraph = Schema.Schema.Type<typeof ResearchGraphSchema>
export type EvidencePolarity = Schema.Schema.Type<typeof EvidencePolaritySchema>

export const decodeResearchGraph = (
  source: string,
  label: string
): Effect.Effect<ResearchGraph, IceError> =>
  Effect.try({
    try: () => {
      let parsed: { schema_version?: unknown }
      try {
        parsed = JSON.parse(source) as { schema_version?: unknown }
      } catch {
        return
      }
      if (typeof parsed.schema_version === "string") {
        assertSupportedResearchSchemaVersion(
          "research-graph",
          parsed.schema_version
        )
      }
    },
    catch: (error) => iceError("ONTOLOGY_SCHEMA_VERSION_UNSUPPORTED", `${label}: ${error instanceof Error ? error.message : String(error)}`)
  }).pipe(Effect.flatMap(() => Schema.decodeUnknown(ResearchGraphFromString)(source, {
    errors: "all",
    onExcessProperty: "error"
  }).pipe(
    Effect.mapError((error) =>
      iceError(
        "ONTOLOGY_SCHEMA_INVALID",
        `${label} does not satisfy research-graph/v1: ${String(error)}`
      )
    )
  )))
