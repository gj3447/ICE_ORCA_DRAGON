import { createHash } from "node:crypto"
import { createRequire } from "node:module"
import { MultiUndirectedGraph } from "graphology"
import type { CollectionGraph } from "../ontology/collection-core.ts"
import type { ResearchEdge, ResearchNode } from "../ontology/model.ts"

const require = createRequire(import.meta.url)
const louvain = require("graphology-communities-louvain") as typeof import("graphology-communities-louvain").default

const HASH_VECTOR_DIMENSIONS = 256
const MAX_REPRESENTATIVE_UNITS = 6

export const graphRagContract = {
  schema: "ice-evidence-graph-rag/v1",
  mode: "DETERMINISTIC_EVIDENCE_FIRST_HUMAN_DIRECTED",
  source_of_truth: "REPOSITORY_ONTOLOGY_JSON",
  model_extracted_entities: false,
  automatic_follow_up: false,
  execution_authorization: "NOT_GRANTED"
} as const

export interface GraphRagTextUnit {
  readonly id: string
  readonly graph: string
  readonly node_id: string
  readonly node_type: ResearchNode["type"]
  readonly state: string
  readonly title: string
  readonly text: string
  readonly source_locator?:
    | { readonly kind: "source"; readonly uri: string; readonly citation: string }
    | { readonly kind: "artifact" | "policy"; readonly path: string; readonly sha256: string }
    | undefined
}

export interface GraphRagCommunity {
  readonly id: string
  readonly graph: string
  readonly member_count: number
  readonly nodes_by_type: Readonly<Record<string, number>>
  readonly representative_unit_ids: ReadonlyArray<string>
  readonly summary: string
}

interface IndexedTextUnit extends GraphRagTextUnit {
  readonly tokens: ReadonlyArray<string>
  readonly term_frequency: ReadonlyMap<string, number>
  readonly vector: Float64Array
}

interface GraphNeighbor {
  readonly unit_id: string
  readonly edge: ResearchEdge
}

export interface GraphRagIndex {
  readonly schema: "ice-evidence-graph-rag-index/v1"
  readonly contract: typeof graphRagContract
  readonly units: ReadonlyArray<GraphRagTextUnit>
  readonly communities: ReadonlyArray<GraphRagCommunity>
  readonly graph_count: number
  readonly edge_count: number
  readonly index_notes: ReadonlyArray<string>
  readonly internal: {
    readonly indexed_units: ReadonlyArray<IndexedTextUnit>
    readonly units_by_id: ReadonlyMap<string, IndexedTextUnit>
    readonly adjacency: ReadonlyMap<string, ReadonlyArray<GraphNeighbor>>
    readonly community_by_unit: ReadonlyMap<string, string>
    readonly community_by_id: ReadonlyMap<string, GraphRagCommunity>
    readonly document_frequency: ReadonlyMap<string, number>
    readonly average_document_length: number
  }
}

export interface GraphRagSearchOptions {
  readonly graph?: string | undefined
  readonly limit?: number | undefined
  readonly depth?: number | undefined
}

export interface GraphRagHit {
  readonly unit: GraphRagTextUnit
  readonly rank: number
  readonly match: "DIRECT_HYBRID" | "GRAPH_EXPANSION"
  readonly distance: number
  readonly scores: {
    readonly bm25: number
    readonly lexical_hash_vector: number
    readonly graph_expansion: number
    readonly combined: number
  }
  readonly traversed_edges: ReadonlyArray<{
    readonly id: string
    readonly relation: string
    readonly from: string
    readonly to: string
  }>
  readonly community_id: string
}

export interface GraphRagSearchResult {
  readonly schema: "ice-evidence-graph-rag-search/v1"
  readonly contract: typeof graphRagContract
  readonly query: string
  readonly graph: string
  readonly limit: number
  readonly depth: number
  readonly index: {
    readonly text_units: number
    readonly communities: number
    readonly retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion"
  }
  readonly hits: ReadonlyArray<GraphRagHit>
  readonly communities: ReadonlyArray<GraphRagCommunity>
  readonly guidance: ReadonlyArray<string>
}

const qualifiedId = (graph: string, nodeId: string): string => `${graph}::${nodeId}`

const tokenize = (value: string): ReadonlyArray<string> =>
  (value.toLocaleLowerCase().match(/[\p{L}\p{N}_-]{2,}/gu) ?? []).slice(0, 4096)

const frequencies = (tokens: ReadonlyArray<string>): ReadonlyMap<string, number> => {
  const result = new Map<string, number>()
  for (const token of tokens) result.set(token, (result.get(token) ?? 0) + 1)
  return result
}

const tokenHash = (token: string): number => {
  let hash = 2166136261
  for (const char of token) {
    hash ^= char.codePointAt(0) ?? 0
    hash = Math.imul(hash, 16777619)
  }
  return hash >>> 0
}

const unitVector = (termFrequency: ReadonlyMap<string, number>): Float64Array => {
  const vector = new Float64Array(HASH_VECTOR_DIMENSIONS)
  for (const [token, count] of termFrequency) {
    const hash = tokenHash(token)
    const index = hash % HASH_VECTOR_DIMENSIONS
    const sign = (hash >>> 31) === 0 ? 1 : -1
    vector[index] = (vector[index] ?? 0) + sign * (1 + Math.log(count))
  }
  return vector
}

const cosine = (left: Float64Array, right: Float64Array): number => {
  let dot = 0
  let leftLength = 0
  let rightLength = 0
  for (let index = 0; index < left.length; index += 1) {
    const leftValue = left[index] ?? 0
    const rightValue = right[index] ?? 0
    dot += leftValue * rightValue
    leftLength += leftValue * leftValue
    rightLength += rightValue * rightValue
  }
  return leftLength === 0 || rightLength === 0
    ? 0
    : Math.max(0, dot / Math.sqrt(leftLength * rightLength))
}

const nodeText = (node: ResearchNode): string => {
  const parts = [node.title, node.summary, node.type, node.state]
  if (node.type === "claim") parts.push(node.statement, node.epistemic_state)
  if (node.type === "evidence") parts.push(node.observed_status, ...(node.check_ids ?? []))
  if (node.type === "scope") parts.push(...node.includes, ...node.excludes)
  if (node.type === "open_problem") parts.push(node.question)
  if (node.type === "source") parts.push(node.citation, node.uri, node.version)
  if (node.type === "artifact") parts.push(node.artifact_kind, node.path)
  if (node.type === "policy") parts.push(node.path)
  return parts.join("\n")
}

const sourceLocator = (
  node: ResearchNode
): GraphRagTextUnit["source_locator"] => {
  if (node.type === "source") {
    return { kind: "source", uri: node.uri, citation: node.citation }
  }
  if (node.type === "artifact" || node.type === "policy") {
    return { kind: node.type, path: node.path, sha256: node.sha256 }
  }
  return undefined
}

const makeIndexedUnit = (graph: string, node: ResearchNode): IndexedTextUnit => {
  const text = nodeText(node)
  const tokens = tokenize(text)
  const termFrequency = frequencies(tokens)
  const locator = sourceLocator(node)
  return {
    id: qualifiedId(graph, node.id),
    graph,
    node_id: node.id,
    node_type: node.type,
    state: node.state,
    title: node.title,
    text,
    ...(locator === undefined ? {} : { source_locator: locator }),
    tokens,
    term_frequency: termFrequency,
    vector: unitVector(termFrequency)
  }
}

const stableCommunityId = (graph: string, members: ReadonlyArray<string>): string =>
  `${graph}:community:${createHash("sha256")
    .update(members.join("\n"))
    .digest("hex")
    .slice(0, 16)}`

const createCommunities = (
  graphKey: string,
  graphNodes: ReadonlyArray<IndexedTextUnit>,
  graphEdges: ReadonlyArray<ResearchEdge>
): {
  readonly communities: ReadonlyArray<GraphRagCommunity>
  readonly communityByUnit: ReadonlyMap<string, string>
} => {
  const structural = new MultiUndirectedGraph()
  for (const unit of graphNodes) structural.addNode(unit.id)
  for (const edge of graphEdges) {
    const from = qualifiedId(graphKey, edge.from)
    const to = qualifiedId(graphKey, edge.to)
    if (!structural.hasNode(from) || !structural.hasNode(to)) continue
    structural.addEdgeWithKey(`${graphKey}:${edge.id}`, from, to, { weight: 1 })
  }
  const partition =
    graphEdges.length === 0
      ? Object.fromEntries(graphNodes.map((unit, index) => [unit.id, index]))
      : louvain(structural, { randomWalk: false, fastLocalMoves: false })
  const grouped = new Map<number, IndexedTextUnit[]>()
  for (const unit of graphNodes) {
    const label = partition[unit.id] ?? -1
    const entries = grouped.get(label) ?? []
    entries.push(unit)
    grouped.set(label, entries)
  }
  const communityByUnit = new Map<string, string>()
  const communities = [...grouped.values()]
    .map((members) => {
      const sorted = [...members].sort((left, right) => left.id.localeCompare(right.id))
      const id = stableCommunityId(graphKey, sorted.map(({ id: unitId }) => unitId))
      const nodesByType: Record<string, number> = {}
      for (const unit of sorted) {
        nodesByType[unit.node_type] = (nodesByType[unit.node_type] ?? 0) + 1
        communityByUnit.set(unit.id, id)
      }
      const representatives = [...sorted]
        .sort((left, right) => right.tokens.length - left.tokens.length || left.id.localeCompare(right.id))
        .slice(0, MAX_REPRESENTATIVE_UNITS)
      return {
        id,
        graph: graphKey,
        member_count: sorted.length,
        nodes_by_type: nodesByType,
        representative_unit_ids: representatives.map(({ id: unitId }) => unitId),
        summary: `${graphKey} structural community (${sorted.length} nodes): ${representatives
          .map(({ title }) => title)
          .join("; ")}`
      } satisfies GraphRagCommunity
    })
    .sort((left, right) => left.id.localeCompare(right.id))
  return { communities, communityByUnit }
}

/**
 * Builds a deterministic, evidence-first GraphRAG index from the canonical
 * ontology. It does not scrape files or invent entities with a language model.
 */
export const buildGraphRagIndex = (
  graphs: ReadonlyArray<CollectionGraph>
): GraphRagIndex => {
  const indexedUnits = graphs.flatMap(({ descriptor, graph }) =>
    graph.nodes.map((node) => makeIndexedUnit(descriptor.key, node))
  )
  const unitsById = new Map(indexedUnits.map((unit) => [unit.id, unit]))
  const adjacency = new Map<string, GraphNeighbor[]>()
  const communityByUnit = new Map<string, string>()
  const communities: GraphRagCommunity[] = []

  for (const { descriptor, graph } of graphs) {
    const graphUnits = indexedUnits.filter(({ graph: key }) => key === descriptor.key)
    const created = createCommunities(descriptor.key, graphUnits, graph.edges)
    communities.push(...created.communities)
    for (const [unitId, community] of created.communityByUnit) {
      communityByUnit.set(unitId, community)
    }
    for (const edge of graph.edges) {
      const from = qualifiedId(descriptor.key, edge.from)
      const to = qualifiedId(descriptor.key, edge.to)
      if (!unitsById.has(from) || !unitsById.has(to)) continue
      const forward = adjacency.get(from) ?? []
      forward.push({ unit_id: to, edge })
      adjacency.set(from, forward)
      const reverse = adjacency.get(to) ?? []
      reverse.push({ unit_id: from, edge })
      adjacency.set(to, reverse)
    }
  }

  const documentFrequency = new Map<string, number>()
  let tokenCount = 0
  for (const unit of indexedUnits) {
    tokenCount += unit.tokens.length
    for (const token of unit.term_frequency.keys()) {
      documentFrequency.set(token, (documentFrequency.get(token) ?? 0) + 1)
    }
  }
  const averageDocumentLength =
    indexedUnits.length === 0 ? 0 : tokenCount / indexedUnits.length

  return {
    schema: "ice-evidence-graph-rag-index/v1",
    contract: graphRagContract,
    units: indexedUnits.map(
      ({ tokens: _tokens, term_frequency: _termFrequency, vector: _vector, ...unit }) => unit
    ),
    communities: communities.sort((left, right) => left.id.localeCompare(right.id)),
    graph_count: graphs.length,
    edge_count: graphs.reduce((total, { graph }) => total + graph.edges.length, 0),
    index_notes: [
      "TextUnits are deterministically projected from canonical ontology nodes and preserve a stable graph/node locator.",
      "Communities use deterministic Louvain structural clustering over explicit ontology relations.",
      "The hybrid score uses BM25 plus a local token-hash vector; it does not claim semantic embedding or LLM-extracted facts.",
      "Raw result files remain the complete check ledger and are not duplicated into this retrieval index."
    ],
    internal: {
      indexed_units: indexedUnits,
      units_by_id: unitsById,
      adjacency,
      community_by_unit: communityByUnit,
      community_by_id: new Map(communities.map((community) => [community.id, community])),
      document_frequency: documentFrequency,
      average_document_length: averageDocumentLength
    }
  }
}

const validateSearchOptions = (options: GraphRagSearchOptions) => {
  const graph = options.graph ?? "all"
  const limit = options.limit ?? 12
  const depth = options.depth ?? 1
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 50) {
    throw new Error("limit must be an integer from 1 through 50")
  }
  if (!Number.isSafeInteger(depth) || depth < 0 || depth > 3) {
    throw new Error("depth must be an integer from 0 through 3")
  }
  return { graph, limit, depth }
}

const bm25 = (
  unit: IndexedTextUnit,
  queryFrequency: ReadonlyMap<string, number>,
  index: GraphRagIndex
): number => {
  if (index.internal.average_document_length === 0) return 0
  const k1 = 1.2
  const b = 0.75
  let score = 0
  for (const token of queryFrequency.keys()) {
    const frequency = unit.term_frequency.get(token) ?? 0
    if (frequency === 0) continue
    const documentFrequency = index.internal.document_frequency.get(token) ?? 0
    const idf = Math.log(
      1 + (index.units.length - documentFrequency + 0.5) / (documentFrequency + 0.5)
    )
    const denominator =
      frequency +
      k1 *
        (1 - b + (b * unit.tokens.length) / index.internal.average_document_length)
    score += idf * ((frequency * (k1 + 1)) / denominator)
  }
  return score
}

interface SearchScore {
  readonly bm25: number
  readonly vector: number
  readonly combined: number
}

const publicUnit = (unit: IndexedTextUnit): GraphRagTextUnit => {
  const { tokens: _tokens, term_frequency: _termFrequency, vector: _vector, ...result } = unit
  return result
}

/** Returns a bounded hybrid evidence bundle; it never synthesizes a claim. */
export const searchGraphRag = (
  index: GraphRagIndex,
  query: string,
  options: GraphRagSearchOptions = {}
): GraphRagSearchResult => {
  const normalizedQuery = query.trim()
  if (normalizedQuery.length === 0 || normalizedQuery.length > 500) {
    throw new Error("query must contain from 1 through 500 characters")
  }
  const { graph, limit, depth } = validateSearchOptions(options)
  const queryFrequency = frequencies(tokenize(normalizedQuery))
  if (queryFrequency.size === 0) {
    throw new Error("query must contain searchable letter or number tokens")
  }
  const queryVector = unitVector(queryFrequency)
  const candidates = index.internal.indexed_units.filter(
    (unit) => graph === "all" || unit.graph === graph
  )
  if (graph !== "all" && candidates.length === 0) {
    throw new Error(`no graph is registered as '${graph}'`)
  }
  const preliminary = candidates.map((unit) => ({
    unit,
    bm25: bm25(unit, queryFrequency, index),
    vector: cosine(unit.vector, queryVector)
  }))
  const maxBm25 = Math.max(...preliminary.map(({ bm25: score }) => score), 0)
  const direct = preliminary
    .map(({ unit, bm25: bm25Score, vector }) => ({
      unit,
      bm25: bm25Score,
      vector,
      combined: (maxBm25 === 0 ? 0 : 0.72 * (bm25Score / maxBm25)) + 0.28 * vector
    }))
    .filter(({ combined }) => combined > 0)
    .sort(
      (left, right) =>
        right.combined - left.combined || left.unit.id.localeCompare(right.unit.id)
    )
    .slice(0, Math.max(limit * 4, 20))

  const scores = new Map<string, SearchScore>()
  const paths = new Map<string, ReadonlyArray<GraphNeighbor>>()
  const distance = new Map<string, number>()
  const queue: Array<{ readonly unitId: string; readonly remainingDepth: number }> = []
  for (const result of direct) {
    scores.set(result.unit.id, {
      bm25: result.bm25,
      vector: result.vector,
      combined: result.combined
    })
    distance.set(result.unit.id, 0)
    paths.set(result.unit.id, [])
    queue.push({ unitId: result.unit.id, remainingDepth: depth })
  }
  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const current = queue[cursor]
    if (current === undefined || current.remainingDepth === 0) continue
    const currentScore = scores.get(current.unitId)
    const currentPath = paths.get(current.unitId)
    const currentDistance = distance.get(current.unitId)
    if (currentScore === undefined || currentPath === undefined || currentDistance === undefined) continue
    for (const neighbor of index.internal.adjacency.get(current.unitId) ?? []) {
      const candidate = index.internal.units_by_id.get(neighbor.unit_id)
      if (candidate === undefined || (graph !== "all" && candidate.graph !== graph)) continue
      const proposed = currentScore.combined * 0.58
      const existing = scores.get(candidate.id)
      if (existing !== undefined && existing.combined >= proposed) continue
      scores.set(candidate.id, { bm25: 0, vector: 0, combined: proposed })
      distance.set(candidate.id, currentDistance + 1)
      paths.set(candidate.id, [...currentPath, neighbor])
      queue.push({ unitId: candidate.id, remainingDepth: current.remainingDepth - 1 })
    }
  }

  const hits = [...scores.entries()]
    .map(([unitId, score]) => {
      const unit = index.internal.units_by_id.get(unitId)
      const unitDistance = distance.get(unitId)
      const path = paths.get(unitId)
      if (unit === undefined || unitDistance === undefined || path === undefined) return undefined
      return {
        unit,
        score,
        distance: unitDistance,
        path
      }
    })
    .flatMap((entry) => (entry === undefined ? [] : [entry]))
    .sort(
      (left, right) =>
        right.score.combined - left.score.combined || left.unit.id.localeCompare(right.unit.id)
    )
    .slice(0, limit)
    .map((entry, indexInResult): GraphRagHit => ({
      unit: publicUnit(entry.unit),
      rank: indexInResult + 1,
      match: entry.distance === 0 ? "DIRECT_HYBRID" : "GRAPH_EXPANSION",
      distance: entry.distance,
      scores: {
        bm25: entry.score.bm25,
        lexical_hash_vector: entry.score.vector,
        graph_expansion: entry.distance === 0 ? 0 : entry.score.combined,
        combined: entry.score.combined
      },
      traversed_edges: entry.path.map(({ edge }) => ({
        id: edge.id,
        relation: edge.relation,
        from: edge.from,
        to: edge.to
      })),
      community_id: index.internal.community_by_unit.get(entry.unit.id) ?? "unclustered"
    }))

  const communityIds = [...new Set(hits.map(({ community_id }) => community_id))]
  const matchingCommunities = communityIds.flatMap((id) => {
    const community = index.internal.community_by_id.get(id)
    return community === undefined ? [] : [community]
  })
  return {
    schema: "ice-evidence-graph-rag-search/v1",
    contract: graphRagContract,
    query: normalizedQuery,
    graph,
    limit,
    depth,
    index: {
      text_units: candidates.length,
      communities: matchingCommunities.length,
      retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion"
    },
    hits,
    communities: matchingCommunities,
    guidance: [
      "This is retrieval context, not an LLM-generated answer or a scientific claim.",
      "Each TextUnit retains a canonical ontology graph/node locator; inspect raw artifacts and primary sources before interpretation.",
      "The local hash vector is deterministic and inexpensive, not a learned semantic embedding; benchmark a learned embedding path before treating it as an upgrade.",
      "A retrieval result neither authorizes execution nor creates a follow-up task."
    ]
  }
}

export const summarizeGraphRagIndex = (index: GraphRagIndex) => ({
  schema: "ice-evidence-graph-rag-summary/v1" as const,
  contract: graphRagContract,
  graph_count: index.graph_count,
  text_units: index.units.length,
  relation_edges: index.edge_count,
  structural_communities: index.communities.length,
  text_unit_source: "canonical ontology node text",
  community_algorithm: "deterministic Louvain over explicit ontology relations",
  retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion",
  notes: index.index_notes
})
