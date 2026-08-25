import { Effect, Schema } from "effect"
import { iceError, type IceError } from "../errors.ts"

const NonEmptyString = Schema.NonEmptyString
const CollectionId = Schema.String.pipe(
  Schema.pattern(/^research-collection:[a-z0-9-]+$/)
)
const GraphId = Schema.String.pipe(
  Schema.pattern(/^research-graph:[a-z0-9-]+$/)
)
const GraphKey = Schema.String.pipe(
  Schema.pattern(/^(?!all$)[a-z0-9-]+$/)
)
const EntityId = Schema.String.pipe(
  Schema.pattern(/^[a-z_]+:[A-Za-z0-9_.:-]+$/)
)
const DateTime = Schema.String.pipe(
  Schema.pattern(
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/
  )
)

export const QualifiedNodeRefSchema = Schema.Struct({
  graph: GraphKey,
  node: EntityId,
  why: Schema.optional(NonEmptyString)
})

export const ResearchGraphDescriptorSchema = Schema.Struct({
  key: GraphKey,
  graph_id: GraphId,
  path: NonEmptyString,
  guide: NonEmptyString,
  entry_node: EntityId,
  coverage: Schema.Literal("DETAILED", "PARTIAL", "INDEX_ONLY"),
  corpus_roots: Schema.NonEmptyArray(NonEmptyString).pipe(Schema.maxItems(16)),
  includes: Schema.Array(Schema.String),
  excludes: Schema.Array(Schema.String)
})

const CollectionQuickAnswerSchema = Schema.Struct({
  question: NonEmptyString,
  answer: NonEmptyString,
  refs: Schema.NonEmptyArray(QualifiedNodeRefSchema).pipe(Schema.maxItems(12))
})

const CollectionReadingPathSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.pattern(/^collection-path:/)),
  title: NonEmptyString,
  summary: NonEmptyString,
  navigation_only: Schema.Literal(true),
  stops: Schema.NonEmptyArray(QualifiedNodeRefSchema).pipe(Schema.maxItems(12))
})

const CoverageEntrySchema = Schema.Struct({
  path: NonEmptyString,
  status: Schema.Literal("INDEXED", "PARTIAL", "UNINDEXED", "ARCHIVE"),
  graph: Schema.optional(GraphKey),
  reason: NonEmptyString
})

export const ResearchCollectionSchema = Schema.Struct({
  $schema: Schema.optional(Schema.String),
  schema_version: Schema.Literal("research-collection/v1"),
  collection_id: CollectionId,
  title: NonEmptyString,
  description: NonEmptyString,
  updated_at_utc: DateTime,
  canonical_file: Schema.Literal("ontology/collection.json"),
  default_graph: GraphKey,
  graphs: Schema.NonEmptyArray(ResearchGraphDescriptorSchema).pipe(
    Schema.maxItems(16)
  ),
  quick_answers: Schema.Array(CollectionQuickAnswerSchema).pipe(
    Schema.maxItems(64)
  ),
  reading_paths: Schema.Array(CollectionReadingPathSchema).pipe(
    Schema.maxItems(32)
  ),
  coverage_ledger: Schema.Array(CoverageEntrySchema).pipe(
    Schema.maxItems(256)
  )
})

const ResearchCollectionFromString = Schema.parseJson(ResearchCollectionSchema)

export type QualifiedNodeRef = Schema.Schema.Type<
  typeof QualifiedNodeRefSchema
>
export type ResearchGraphDescriptor = Schema.Schema.Type<
  typeof ResearchGraphDescriptorSchema
>
export type ResearchCollection = Schema.Schema.Type<
  typeof ResearchCollectionSchema
>

export const decodeResearchCollection = (
  source: string,
  label: string
): Effect.Effect<ResearchCollection, IceError> =>
  Schema.decodeUnknown(ResearchCollectionFromString)(source, {
    errors: "all",
    onExcessProperty: "error"
  }).pipe(
    Effect.mapError((error) =>
      iceError(
        "ONTOLOGY_COLLECTION_SCHEMA_INVALID",
        `${label} does not satisfy research-collection/v1: ${String(error)}`
      )
    )
  )
