import type { ResearchCollection } from "./collection.ts"

type GraphDescriptor = ResearchCollection["graphs"][number]
type QuickAnswer = ResearchCollection["quick_answers"][number]
type ReadingPath = ResearchCollection["reading_paths"][number]
type CoverageEntry = ResearchCollection["coverage_ledger"][number]

/** A complete before/after record identified by a collection-local stable ID. */
export interface CollectionIdentifiedRecordChange<T> {
  readonly id: string
  readonly before: T
  readonly after: T
}

export interface CollectionIdentifiedRecordDelta<T> {
  readonly added: ReadonlyArray<T>
  readonly removed: ReadonlyArray<T>
  readonly changed: ReadonlyArray<CollectionIdentifiedRecordChange<T>>
}

/**
 * ID-less collection records use a documented semantic key plus an occurrence
 * index in canonical-record order. The index keeps duplicate semantic keys
 * deterministic without treating source-array order as meaningful.
 */
export interface CollectionKeyedRecord<T> {
  readonly key: string
  readonly index: number
  readonly value: T
}

export interface CollectionKeyedRecordChange<T> {
  readonly key: string
  readonly index: number
  readonly before: T
  readonly after: T
}

export interface CollectionKeyedRecordDelta<T> {
  readonly added: ReadonlyArray<CollectionKeyedRecord<T>>
  readonly removed: ReadonlyArray<CollectionKeyedRecord<T>>
  readonly changed: ReadonlyArray<CollectionKeyedRecordChange<T>>
}

export interface CollectionMetadataChange {
  readonly field: string
  readonly before: unknown
  readonly after: unknown
}

export interface ResearchCollectionDiffSummary {
  readonly metadata_changes: number
  readonly graph_descriptors: {
    readonly added: number
    readonly removed: number
    readonly changed: number
  }
  readonly quick_answers: {
    readonly added: number
    readonly removed: number
    readonly changed: number
  }
  readonly reading_paths: {
    readonly added: number
    readonly removed: number
    readonly changed: number
  }
  readonly coverage_ledger: {
    readonly added: number
    readonly removed: number
    readonly changed: number
  }
  readonly total_changes: number
  readonly has_changes: boolean
}

export interface ResearchCollectionDiff {
  readonly metadata: ReadonlyArray<CollectionMetadataChange>
  readonly graph_descriptors: CollectionIdentifiedRecordDelta<GraphDescriptor>
  readonly quick_answers: CollectionKeyedRecordDelta<QuickAnswer>
  readonly reading_paths: CollectionIdentifiedRecordDelta<ReadingPath>
  readonly coverage_ledger: CollectionKeyedRecordDelta<CoverageEntry>
  readonly summary: ResearchCollectionDiffSummary
}

export interface ResearchCollectionReviewWarning {
  readonly code: string
  readonly message: string
  readonly subject?: string | undefined
}

const compare = (left: string, right: string): number =>
  left < right ? -1 : left > right ? 1 : 0

const canonicalJson = (value: unknown): string => {
  if (value === null || typeof value !== "object") return JSON.stringify(value)
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`
  const record = value as Readonly<Record<string, unknown>>
  return `{${Object.keys(record)
    .sort(compare)
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(record[key])}`)
    .join(",")}}`
}

const same = (left: unknown, right: unknown): boolean =>
  canonicalJson(left) === canonicalJson(right)

const byId = <T>(
  base: ReadonlyArray<T>,
  current: ReadonlyArray<T>,
  id: (record: T) => string
): CollectionIdentifiedRecordDelta<T> => {
  const baseById = new Map(base.map((record) => [id(record), record]))
  const currentById = new Map(current.map((record) => [id(record), record]))
  const ids = [...new Set([...baseById.keys(), ...currentById.keys()])].sort(compare)
  const added: T[] = []
  const removed: T[] = []
  const changed: CollectionIdentifiedRecordChange<T>[] = []

  for (const recordId of ids) {
    const before = baseById.get(recordId)
    const after = currentById.get(recordId)
    if (before === undefined && after !== undefined) added.push(after)
    else if (before !== undefined && after === undefined) removed.push(before)
    else if (before !== undefined && after !== undefined && !same(before, after)) {
      changed.push({ id: recordId, before, after })
    }
  }
  return { added, removed, changed }
}

interface CanonicalKeyed<T> extends CollectionKeyedRecord<T> {
  readonly canonical: string
}

const keyedId = (key: string, index: number): string =>
  `${key}\u0000${String(index).padStart(8, "0")}`

const keyed = <T>(
  records: ReadonlyArray<T>,
  semanticKey: (record: T) => string
): ReadonlyArray<CanonicalKeyed<T>> => {
  const groups = new Map<string, Array<{ readonly value: T; readonly canonical: string }>>()
  for (const value of records) {
    const key = semanticKey(value)
    const entries = groups.get(key) ?? []
    entries.push({ value, canonical: canonicalJson(value) })
    groups.set(key, entries)
  }
  return [...groups.entries()]
    .sort(([left], [right]) => compare(left, right))
    .flatMap(([key, entries]) =>
      entries
        .sort((left, right) => compare(left.canonical, right.canonical))
        .map(({ value, canonical }, index) => ({ key, index, value, canonical }))
    )
}

const bySemanticKey = <T>(
  base: ReadonlyArray<T>,
  current: ReadonlyArray<T>,
  semanticKey: (record: T) => string
): CollectionKeyedRecordDelta<T> => {
  const baseById = new Map(
    keyed(base, semanticKey).map((record) => [keyedId(record.key, record.index), record])
  )
  const currentById = new Map(
    keyed(current, semanticKey).map((record) => [keyedId(record.key, record.index), record])
  )
  const ids = [...new Set([...baseById.keys(), ...currentById.keys()])].sort(compare)
  const added: CollectionKeyedRecord<T>[] = []
  const removed: CollectionKeyedRecord<T>[] = []
  const changed: CollectionKeyedRecordChange<T>[] = []

  for (const id of ids) {
    const before = baseById.get(id)
    const after = currentById.get(id)
    if (before === undefined && after !== undefined) {
      added.push({ key: after.key, index: after.index, value: after.value })
    } else if (before !== undefined && after === undefined) {
      removed.push({ key: before.key, index: before.index, value: before.value })
    } else if (before !== undefined && after !== undefined && before.canonical !== after.canonical) {
      changed.push({ key: before.key, index: before.index, before: before.value, after: after.value })
    }
  }
  return { added, removed, changed }
}

const metadataFields = [
  "$schema",
  "schema_version",
  "collection_id",
  "title",
  "description",
  "updated_at_utc",
  "canonical_file",
  "default_graph"
] as const

const count = <T>(
  delta: {
    readonly added: ReadonlyArray<T>
    readonly removed: ReadonlyArray<T>
    readonly changed: ReadonlyArray<unknown>
  }
) => ({
  added: delta.added.length,
  removed: delta.removed.length,
  changed: delta.changed.length
})

/**
 * Deterministically compares the canonical collection envelope. Graph
 * descriptors are keyed by graph key; quick answers by question; reading
 * paths by ID; and coverage entries by repository path.
 */
export const diffResearchCollections = (
  base: ResearchCollection,
  current: ResearchCollection
): ResearchCollectionDiff => {
  const metadata = metadataFields.flatMap((field) =>
    same(base[field], current[field])
      ? []
      : [{ field, before: base[field], after: current[field] }]
  )
  const graph_descriptors = byId(base.graphs, current.graphs, ({ key }) => key)
  const quick_answers = bySemanticKey(
    base.quick_answers,
    current.quick_answers,
    ({ question }) => question
  )
  const reading_paths = byId(base.reading_paths, current.reading_paths, ({ id }) => id)
  const coverage_ledger = bySemanticKey(
    base.coverage_ledger,
    current.coverage_ledger,
    ({ path }) => path
  )
  const graphDescriptorCounts = count(graph_descriptors)
  const quickAnswerCounts = count(quick_answers)
  const readingPathCounts = count(reading_paths)
  const coverageCounts = count(coverage_ledger)
  const recordCounts = [
    graphDescriptorCounts,
    quickAnswerCounts,
    readingPathCounts,
    coverageCounts
  ]
  const total_changes = metadata.length + recordCounts.reduce(
    (total, part) => total + part.added + part.removed + part.changed,
    0
  )

  return {
    metadata,
    graph_descriptors,
    quick_answers,
    reading_paths,
    coverage_ledger,
    summary: {
      metadata_changes: metadata.length,
      graph_descriptors: graphDescriptorCounts,
      quick_answers: quickAnswerCounts,
      reading_paths: readingPathCounts,
      coverage_ledger: coverageCounts,
      total_changes,
      has_changes: total_changes > 0
    }
  }
}

const warning = (
  code: string,
  message: string,
  subject?: string
): ResearchCollectionReviewWarning => ({ code, message, subject })

/** Focused collection authoring warnings; schema and semantic validation remain authoritative. */
export const makeResearchCollectionReviewWarnings = (
  base: ResearchCollection,
  current: ResearchCollection,
  diff: ResearchCollectionDiff
): ReadonlyArray<ResearchCollectionReviewWarning> => {
  const timestampChanged = base.updated_at_utc !== current.updated_at_utc
  const changesWithoutTimestamp =
    diff.summary.total_changes -
    diff.metadata.filter(({ field }) => field === "updated_at_utc").length

  if (changesWithoutTimestamp > 0 && !timestampChanged) {
    return [
      warning(
        "ONTOLOGY_COLLECTION_REVIEW_UPDATED_AT_UNCHANGED",
        "collection content changed but updated_at_utc did not"
      )
    ]
  }
  if (changesWithoutTimestamp === 0 && timestampChanged) {
    return [
      warning(
        "ONTOLOGY_COLLECTION_REVIEW_TIMESTAMP_ONLY",
        "updated_at_utc changed without another collection change"
      )
    ]
  }
  return []
}
