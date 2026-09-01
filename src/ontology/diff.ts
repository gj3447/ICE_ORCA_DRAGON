import type {
  KgBridge,
  ResearchEdge,
  ResearchGraph,
  ResearchNode
} from "./model.ts"

type ReadingPath = ResearchGraph["reading_paths"][number]
type QuickAnswer = ResearchGraph["quick_answers"][number]

/** A complete before/after record identified by a graph-local stable ID. */
export interface IdentifiedRecordChange<T> {
  readonly id: string
  readonly before: T
  readonly after: T
}

export interface IdentifiedRecordDelta<T> {
  readonly added: ReadonlyArray<T>
  readonly removed: ReadonlyArray<T>
  readonly changed: ReadonlyArray<IdentifiedRecordChange<T>>
}

/**
 * ID-less records use a documented semantic key plus an occurrence index in
 * canonical-record order. The index is needed because questions or bridge
 * identities are not schema-level unique IDs.
 */
export interface KeyedRecord<T> {
  readonly key: string
  readonly index: number
  readonly value: T
}

export interface KeyedRecordChange<T> {
  readonly key: string
  readonly index: number
  readonly before: T
  readonly after: T
}

export interface KeyedRecordDelta<T> {
  readonly added: ReadonlyArray<KeyedRecord<T>>
  readonly removed: ReadonlyArray<KeyedRecord<T>>
  readonly changed: ReadonlyArray<KeyedRecordChange<T>>
}

export interface MetadataChange {
  readonly field: string
  readonly before: unknown
  readonly after: unknown
}

export interface ResearchGraphDiffSummary {
  readonly metadata_changes: number
  readonly nodes: { readonly added: number; readonly removed: number; readonly changed: number }
  readonly edges: { readonly added: number; readonly removed: number; readonly changed: number }
  readonly reading_paths: { readonly added: number; readonly removed: number; readonly changed: number }
  readonly quick_answers: { readonly added: number; readonly removed: number; readonly changed: number }
  readonly kg_bridges: { readonly added: number; readonly removed: number; readonly changed: number }
  readonly total_changes: number
  readonly has_changes: boolean
}

export interface ResearchGraphDiff {
  readonly metadata: ReadonlyArray<MetadataChange>
  readonly nodes: IdentifiedRecordDelta<ResearchNode>
  readonly edges: IdentifiedRecordDelta<ResearchEdge>
  readonly reading_paths: IdentifiedRecordDelta<ReadingPath>
  readonly quick_answers: KeyedRecordDelta<QuickAnswer>
  readonly kg_bridges: KeyedRecordDelta<KgBridge>
  readonly summary: ResearchGraphDiffSummary
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

const byId = <T extends { readonly id: string }>(
  base: ReadonlyArray<T>,
  current: ReadonlyArray<T>
): IdentifiedRecordDelta<T> => {
  const baseById = new Map(base.map((record) => [record.id, record]))
  const currentById = new Map(current.map((record) => [record.id, record]))
  const ids = [...new Set([...baseById.keys(), ...currentById.keys()])].sort(compare)
  const added: Array<T> = []
  const removed: Array<T> = []
  const changed: Array<IdentifiedRecordChange<T>> = []

  for (const id of ids) {
    const before = baseById.get(id)
    const after = currentById.get(id)
    if (before === undefined && after !== undefined) added.push(after)
    else if (before !== undefined && after === undefined) removed.push(before)
    else if (before !== undefined && after !== undefined && !same(before, after)) {
      changed.push({ id, before, after })
    }
  }
  return { added, removed, changed }
}

interface CanonicalKeyed<T> extends KeyedRecord<T> {
  readonly canonical: string
}

const keyId = (key: string, index: number): string =>
  `${key}\u0000${String(index).padStart(8, "0")}`

const keyed = <T>(
  records: ReadonlyArray<T>,
  stableKey: (record: T) => string
): ReadonlyArray<CanonicalKeyed<T>> => {
  const grouped = new Map<string, Array<{ readonly value: T; readonly canonical: string }>>()
  for (const value of records) {
    const key = stableKey(value)
    const group = grouped.get(key) ?? []
    group.push({ value, canonical: canonicalJson(value) })
    grouped.set(key, group)
  }
  return [...grouped.entries()]
    .sort(([left], [right]) => compare(left, right))
    .flatMap(([key, group]) =>
      group
        .sort((left, right) => compare(left.canonical, right.canonical))
        .map(({ value, canonical }, index) => ({ key, index, value, canonical }))
    )
}

const byStableKey = <T>(
  base: ReadonlyArray<T>,
  current: ReadonlyArray<T>,
  stableKey: (record: T) => string
): KeyedRecordDelta<T> => {
  const baseById = new Map(keyed(base, stableKey).map((record) => [keyId(record.key, record.index), record]))
  const currentById = new Map(keyed(current, stableKey).map((record) => [keyId(record.key, record.index), record]))
  const ids = [...new Set([...baseById.keys(), ...currentById.keys()])].sort(compare)
  const added: Array<KeyedRecord<T>> = []
  const removed: Array<KeyedRecord<T>> = []
  const changed: Array<KeyedRecordChange<T>> = []

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
  "graph_id",
  "title",
  "description",
  "updated_at_utc",
  "canonical_file",
  "source_inventory",
  "node_type_legend",
  "relation_legend"
] as const

const count = <T>(delta: { readonly added: ReadonlyArray<T>; readonly removed: ReadonlyArray<T>; readonly changed: ReadonlyArray<unknown> }) => ({
  added: delta.added.length,
  removed: delta.removed.length,
  changed: delta.changed.length
})

/**
 * Deterministically compare two decoded canonical research graphs without
 * mutating either input. Nodes, edges and reading paths are matched by ID.
 * Quick answers are matched by question plus canonical occurrence index;
 * KG bridges by local node, system and lookup key plus canonical occurrence
 * index. A changed identity key is intentionally represented as remove/add.
 */
export const diffResearchGraphs = (
  base: ResearchGraph,
  current: ResearchGraph
): ResearchGraphDiff => {
  const metadata = metadataFields.flatMap((field) =>
    same(base[field], current[field])
      ? []
      : [{ field, before: base[field], after: current[field] }]
  )
  const nodes = byId(base.nodes, current.nodes)
  const edges = byId(base.edges, current.edges)
  const reading_paths = byId(base.reading_paths, current.reading_paths)
  const quick_answers = byStableKey(base.quick_answers, current.quick_answers, ({ question }) => question)
  const kg_bridges = byStableKey(
    base.kg_bridges,
    current.kg_bridges,
    ({ local_node_id, system, lookup_key }) =>
      `${local_node_id}\u0000${system}\u0000${lookup_key ?? ""}`
  )
  const nodeCounts = count(nodes)
  const edgeCounts = count(edges)
  const readingPathCounts = count(reading_paths)
  const quickAnswerCounts = count(quick_answers)
  const kgBridgeCounts = count(kg_bridges)
  const summaryParts = [
    nodeCounts,
    edgeCounts,
    readingPathCounts,
    quickAnswerCounts,
    kgBridgeCounts
  ]
  const total_changes = metadata.length + summaryParts.reduce(
    (total, part) => total + part.added + part.removed + part.changed,
    0
  )

  return {
    metadata,
    nodes,
    edges,
    reading_paths,
    quick_answers,
    kg_bridges,
    summary: {
      metadata_changes: metadata.length,
      nodes: nodeCounts,
      edges: edgeCounts,
      reading_paths: readingPathCounts,
      quick_answers: quickAnswerCounts,
      kg_bridges: kgBridgeCounts,
      total_changes,
      has_changes: total_changes > 0
    }
  }
}
