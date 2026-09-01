import type {
  ResearchCollection,
  ResearchGraphDescriptor
} from "./collection.ts"
import {
  isSafeArtifactPath,
  summarizeGraph,
  type OntologySummary,
  type ValidationIssue,
  type ValidationReport
} from "./core.ts"
import type { ResearchGraph, ResearchNode } from "./model.ts"

export interface CollectionGraph {
  readonly descriptor: ResearchGraphDescriptor
  readonly graph: ResearchGraph
  readonly validation: ValidationReport
}

export interface CollectionValidationReport {
  readonly collection_id: string
  readonly schema_version: "research-collection/v1"
  readonly valid: boolean
  readonly counts: {
    readonly graphs: number
    readonly nodes: number
    readonly edges: number
    readonly artifacts: number
    readonly policies: number
    readonly hash_bearing_nodes: number
    readonly verified_hashes: number
  }
  readonly graphs: ReadonlyArray<ValidationReport>
  readonly errors: ReadonlyArray<ValidationIssue>
  readonly warnings: ReadonlyArray<ValidationIssue>
}

export interface CollectionSummary {
  readonly collection_id: string
  readonly title: string
  readonly schema_version: "research-collection/v1"
  readonly updated_at_utc: string
  readonly default_graph: string
  readonly graph_count: number
  readonly graphs: ReadonlyArray<
    OntologySummary & {
      readonly key: string
      readonly coverage: "DETAILED" | "PARTIAL" | "INDEX_ONLY"
    }
  >
  readonly totals: {
    readonly nodes: number
    readonly edges: number
    readonly claims: number
    readonly evidence: number
    readonly open_problems: number
    readonly artifacts: number
    readonly unresolved_bridges: number
  }
  readonly coverage: ReadonlyArray<{
    readonly path: string
    readonly status: "INDEXED" | "PARTIAL" | "UNINDEXED" | "ARCHIVE"
    readonly graph?: string | undefined
    readonly reason: string
  }>
}

export interface ResolvedCollectionNode {
  readonly key: string
  readonly graph: ResearchGraph
  readonly node: ResearchNode
}

const issue = (
  severity: "error" | "warning",
  code: string,
  message: string,
  subject?: string
): ValidationIssue =>
  subject === undefined
    ? { severity, code, message }
    : { severity, code, message, subject }

const duplicates = (
  values: ReadonlyArray<string>
): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const repeated = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) repeated.add(value)
    seen.add(value)
  }
  return [...repeated].sort()
}

const safeCollectionPath = (value: string): boolean =>
  isSafeArtifactPath(value)

const graphMap = (
  graphs: ReadonlyArray<CollectionGraph>
): ReadonlyMap<string, CollectionGraph> =>
  new Map(graphs.map((loaded) => [loaded.descriptor.key, loaded]))

const pathBelongsToRoot = (value: string, root: string): boolean =>
  value === root || value.startsWith(`${root}/`)

export const validateCollectionManifest = (
  collection: ResearchCollection
): ReadonlyArray<ValidationIssue> => {
  const issues: Array<ValidationIssue> = []

  for (const key of duplicates(collection.graphs.map(({ key }) => key))) {
    issues.push(
      issue("error", "COLLECTION_DUPLICATE_GRAPH_KEY", `duplicate graph key '${key}'`, key)
    )
  }
  for (const id of duplicates(collection.graphs.map(({ graph_id }) => graph_id))) {
    issues.push(
      issue("error", "COLLECTION_DUPLICATE_GRAPH_ID", `duplicate graph id '${id}'`, id)
    )
  }
  for (const path of duplicates(collection.graphs.map(({ path }) => path))) {
    issues.push(
      issue("error", "COLLECTION_DUPLICATE_GRAPH_PATH", `duplicate graph path '${path}'`, path)
    )
  }
  for (const id of duplicates(collection.reading_paths.map(({ id }) => id))) {
    issues.push(
      issue("error", "COLLECTION_DUPLICATE_READING_PATH", `duplicate path id '${id}'`, id)
    )
  }
  for (const root of duplicates(collection.graphs.flatMap(({ corpus_roots }) => corpus_roots))) {
    issues.push(
      issue(
        "error",
        "COLLECTION_DUPLICATE_CORPUS_ROOT",
        `corpus root '${root}' is assigned more than once`,
        root
      )
    )
  }
  const assignedRoots = collection.graphs.flatMap(({ key, corpus_roots }) =>
    corpus_roots.map((root) => ({ key, root }))
  )
  for (let leftIndex = 0; leftIndex < assignedRoots.length; leftIndex += 1) {
    const left = assignedRoots[leftIndex]
    if (left === undefined) continue
    for (
      let rightIndex = leftIndex + 1;
      rightIndex < assignedRoots.length;
      rightIndex += 1
    ) {
      const right = assignedRoots[rightIndex]
      if (
        right === undefined ||
        left.root === right.root ||
        (!pathBelongsToRoot(left.root, right.root) &&
          !pathBelongsToRoot(right.root, left.root))
      ) {
        continue
      }
      issues.push(
        issue(
          "error",
          "COLLECTION_OVERLAPPING_CORPUS_ROOT",
          `corpus roots '${left.root}' (${left.key}) and '${right.root}' (${right.key}) overlap`,
          left.root
        )
      )
    }
  }
  for (const path of duplicates(collection.coverage_ledger.map(({ path }) => path))) {
    issues.push(
      issue(
        "error",
        "COLLECTION_DUPLICATE_COVERAGE_PATH",
        `coverage path '${path}' is recorded more than once`,
        path
      )
    )
  }

  if (!collection.graphs.some(({ key }) => key === collection.default_graph)) {
    issues.push(
      issue(
        "error",
        "COLLECTION_DEFAULT_GRAPH_NOT_FOUND",
        `default graph '${collection.default_graph}' is not registered`,
        collection.default_graph
      )
    )
  }

  for (const descriptor of collection.graphs) {
    const expectedRootCoverage =
      descriptor.coverage === "PARTIAL" ? "PARTIAL" : "INDEXED"
    if (!safeCollectionPath(descriptor.path)) {
      issues.push(
        issue(
          "error",
          "COLLECTION_GRAPH_PATH_UNSAFE",
          `graph path is not a safe repository-relative path: '${descriptor.path}'`,
          descriptor.key
        )
      )
    }
    if (!safeCollectionPath(descriptor.guide)) {
      issues.push(
        issue(
          "error",
          "COLLECTION_GUIDE_PATH_UNSAFE",
          `guide path is not a safe repository-relative path: '${descriptor.guide}'`,
          descriptor.key
        )
      )
    }
    for (const root of descriptor.corpus_roots) {
      if (!safeCollectionPath(root)) {
        issues.push(
          issue(
            "error",
            "COLLECTION_CORPUS_ROOT_UNSAFE",
            `corpus root is not a safe repository-relative path: '${root}'`,
            descriptor.key
          )
        )
      }
      if (
        !collection.coverage_ledger.some(
          (entry) =>
            entry.path === root &&
            entry.graph === descriptor.key &&
            entry.status === expectedRootCoverage
        )
      ) {
        issues.push(
          issue(
            "error",
            "COLLECTION_CORPUS_ROOT_COVERAGE_MISSING",
            `corpus root '${root}' has no matching ${expectedRootCoverage} coverage entry`,
            descriptor.key
          )
        )
      }
    }
  }

  for (const coverage of collection.coverage_ledger) {
    if (!safeCollectionPath(coverage.path)) {
      issues.push(
        issue(
          "error",
          "COLLECTION_COVERAGE_PATH_UNSAFE",
          `coverage path is not safe: '${coverage.path}'`,
          coverage.path
        )
      )
    }
    const descriptor =
      coverage.graph === undefined
        ? undefined
        : collection.graphs.find(({ key }) => key === coverage.graph)
    if (coverage.graph !== undefined && descriptor === undefined) {
      issues.push(
        issue(
          "error",
          "COLLECTION_COVERAGE_GRAPH_NOT_FOUND",
          `coverage entry names missing graph '${coverage.graph}'`,
          coverage.path
        )
      )
    }
    if (
      (coverage.status === "INDEXED" || coverage.status === "PARTIAL") &&
      coverage.graph === undefined
    ) {
      issues.push(
        issue(
          "error",
          "COLLECTION_COVERAGE_GRAPH_REQUIRED",
          `${coverage.status} coverage requires a graph key`,
          coverage.path
        )
      )
    }
    if (
      (coverage.status === "UNINDEXED" || coverage.status === "ARCHIVE") &&
      coverage.graph !== undefined
    ) {
      issues.push(
        issue(
          "error",
          "COLLECTION_NONACTIVE_GRAPH_FORBIDDEN",
          `${coverage.status} coverage must not claim ownership by a graph`,
          coverage.path
        )
      )
    }
    if (
      descriptor !== undefined &&
      (coverage.status === "INDEXED" || coverage.status === "PARTIAL") &&
      !descriptor.corpus_roots.some((root) =>
        pathBelongsToRoot(coverage.path, root)
      )
    ) {
      issues.push(
        issue(
          "error",
          "COLLECTION_COVERAGE_OUTSIDE_CORPUS_ROOT",
          `coverage path '${coverage.path}' is outside every root for '${descriptor.key}'`,
          coverage.path
        )
      )
    }
  }

  return issues
}

export const validateCollectionSemantics = (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>
): ReadonlyArray<ValidationIssue> => {
  const issues: Array<ValidationIssue> = [
    ...validateCollectionManifest(collection)
  ]
  const byKey = graphMap(graphs)

  for (const descriptor of collection.graphs) {
    const loaded = byKey.get(descriptor.key)
    if (loaded === undefined) {
      issues.push(
        issue(
          "error",
          "COLLECTION_GRAPH_NOT_LOADED",
          `registered graph '${descriptor.key}' was not loaded`,
          descriptor.key
        )
      )
      continue
    }
    if (loaded.graph.graph_id !== descriptor.graph_id) {
      issues.push(
        issue(
          "error",
          "COLLECTION_GRAPH_ID_MISMATCH",
          `descriptor ${descriptor.graph_id} does not match loaded ${loaded.graph.graph_id}`,
          descriptor.key
        )
      )
    }
    if (loaded.graph.canonical_file !== descriptor.path) {
      issues.push(
        issue(
          "error",
          "COLLECTION_CANONICAL_PATH_MISMATCH",
          `graph canonical_file '${loaded.graph.canonical_file}' does not match '${descriptor.path}'`,
          descriptor.key
        )
      )
    }
    const entry = loaded.graph.nodes.find(({ id }) => id === descriptor.entry_node)
    if (entry === undefined) {
      issues.push(
        issue(
          "error",
          "COLLECTION_ENTRY_NODE_NOT_FOUND",
          `entry node '${descriptor.entry_node}' does not exist`,
          descriptor.key
        )
      )
    } else if (entry.type !== "programme") {
      issues.push(
        issue(
          "error",
          "COLLECTION_ENTRY_NODE_NOT_PROGRAMME",
          `entry node '${descriptor.entry_node}' has type '${entry.type}'`,
          descriptor.key
        )
      )
    }
  }

  const validateRef = (
    ref: { readonly graph: string; readonly node: string },
    subject: string
  ): void => {
    const loaded = byKey.get(ref.graph)
    if (loaded === undefined) {
      const registered = collection.graphs.some(({ key }) => key === ref.graph)
      issues.push(
        issue(
          "error",
          registered
            ? "COLLECTION_REF_GRAPH_NOT_LOADED"
            : "COLLECTION_REF_GRAPH_NOT_FOUND",
          registered
            ? `qualified reference uses graph '${ref.graph}' which could not be loaded`
            : `qualified reference uses missing graph '${ref.graph}'`,
          subject
        )
      )
      return
    }
    if (!loaded.graph.nodes.some(({ id }) => id === ref.node)) {
      issues.push(
        issue(
          "error",
          "COLLECTION_REF_NODE_NOT_FOUND",
          `qualified reference '${ref.graph}::${ref.node}' does not exist`,
          subject
        )
      )
    }
  }

  for (const answer of collection.quick_answers) {
    for (const ref of answer.refs) validateRef(ref, answer.question)
  }
  for (const path of collection.reading_paths) {
    if (path.stops.length > 12) {
      issues.push(
        issue(
          "error",
          "COLLECTION_READING_PATH_TOO_LONG",
          `reading path has ${path.stops.length} stops; maximum is 12`,
          path.id
        )
      )
    }
    for (const ref of path.stops) validateRef(ref, path.id)
  }

  const artifactHashes = new Map<string, Set<string>>()
  for (const loaded of graphs) {
    for (const node of loaded.graph.nodes) {
      if (node.type !== "artifact" && node.type !== "policy") continue
      const hashes = artifactHashes.get(node.path) ?? new Set<string>()
      hashes.add(node.sha256)
      artifactHashes.set(node.path, hashes)
    }
  }
  for (const [path, hashes] of artifactHashes) {
    if (hashes.size > 1) {
      issues.push(
        issue(
          "error",
          "COLLECTION_ARTIFACT_HASH_CONFLICT",
          `the same artifact path has ${hashes.size} different SHA-256 values across graphs`,
          path
        )
      )
    }
  }

  return issues
}

export const makeCollectionValidationReport = (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>,
  collectionIssues: ReadonlyArray<ValidationIssue>,
  graphReports: ReadonlyArray<ValidationReport> = graphs.map(
    ({ validation }) => validation
  )
): CollectionValidationReport => {
  const graphIssues = graphReports.flatMap((validation) => [
    ...validation.errors,
    ...validation.warnings
  ])
  const allIssues = [...collectionIssues, ...graphIssues]
  const errors = allIssues.filter(({ severity }) => severity === "error")
  const warnings = allIssues.filter(({ severity }) => severity === "warning")
  return {
    collection_id: collection.collection_id,
    schema_version: "research-collection/v1",
    valid: errors.length === 0,
    counts: {
      graphs: graphReports.length,
      nodes: graphReports.reduce((sum, validation) => sum + validation.counts.nodes, 0),
      edges: graphReports.reduce((sum, validation) => sum + validation.counts.edges, 0),
      artifacts: graphReports.reduce(
        (sum, validation) => sum + validation.counts.artifacts,
        0
      ),
      policies: graphReports.reduce(
        (sum, validation) => sum + validation.counts.policies,
        0
      ),
      hash_bearing_nodes: graphReports.reduce(
        (sum, validation) => sum + validation.counts.hash_bearing_nodes,
        0
      ),
      verified_hashes: graphReports.reduce(
        (sum, validation) => sum + validation.counts.verified_hashes,
        0
      )
    },
    graphs: graphReports,
    errors,
    warnings
  }
}

export const summarizeCollection = (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>
): CollectionSummary => {
  const summaries = graphs.map(({ descriptor, graph, validation }) => ({
    ...summarizeGraph(graph, validation),
    key: descriptor.key,
    coverage: descriptor.coverage
  }))
  return {
    collection_id: collection.collection_id,
    title: collection.title,
    schema_version: "research-collection/v1",
    updated_at_utc: collection.updated_at_utc,
    default_graph: collection.default_graph,
    graph_count: summaries.length,
    graphs: summaries,
    totals: {
      nodes: summaries.reduce((sum, value) => sum + value.node_count, 0),
      edges: summaries.reduce((sum, value) => sum + value.edge_count, 0),
      claims: summaries.reduce(
        (sum, value) =>
          sum +
          Object.values(value.claims_by_epistemic_state).reduce(
            (subtotal, count) => subtotal + count,
            0
          ),
        0
      ),
      evidence: summaries.reduce(
        (sum, value) => sum + (value.nodes_by_type.evidence ?? 0),
        0
      ),
      open_problems: summaries.reduce(
        (sum, value) => sum + value.open_problem_count,
        0
      ),
      artifacts: summaries.reduce(
        (sum, value) => sum + value.artifact_count,
        0
      ),
      unresolved_bridges: summaries.reduce(
        (sum, value) => sum + (value.kg_bridges_by_status.UNRESOLVED ?? 0),
        0
      )
    },
    coverage: collection.coverage_ledger
  }
}

export const findCollectionNodes = (
  graphs: ReadonlyArray<CollectionGraph>,
  query: string,
  graphKey?: string
): ReadonlyArray<ResolvedCollectionNode> => {
  const selected =
    graphKey === undefined
      ? graphs
      : graphs.filter(({ descriptor }) => descriptor.key === graphKey)
  const exactQualified = query.match(/^([a-z0-9-]+)::(.+)$/)
  const key = exactQualified?.[1]
  const id = exactQualified?.[2] ?? query
  const candidates =
    key === undefined
      ? selected
      : selected.filter(({ descriptor }) => descriptor.key === key)

  const exact = candidates.flatMap(({ descriptor, graph }) => {
    const node = graph.nodes.find((candidate) => candidate.id === id)
    return node === undefined ? [] : [{ key: descriptor.key, graph, node }]
  })
  if (exact.length > 0) return exact

  const normalizedClaim = id.startsWith("claim:") ? id.slice(6) : id
  return candidates.flatMap(({ descriptor, graph }) =>
    graph.nodes.flatMap((node) =>
      node.type === "claim" && node.claim_id === normalizedClaim
        ? [{ key: descriptor.key, graph, node }]
        : []
    )
  )
}
