import { Console, Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { Workspace } from "../workspace.ts"
import {
  findCollectionNodes,
  summarizeCollection,
  type CollectionGraph,
  type CollectionSummary,
  type CollectionValidationReport,
  type ResolvedCollectionNode
} from "./collection-core.ts"
import type { ResearchCollection } from "./collection.ts"
import {
  diffResearchCollections,
  makeResearchCollectionReviewWarnings,
  type ResearchCollectionDiff,
  type ResearchCollectionReviewWarning
} from "./collection-diff.ts"
import {
  resolveNode,
  showNode,
  summarizeGraph,
  traceGraph,
  type NodeView,
  type OntologySummary,
  type TraceResult,
  type ValidationIssue,
  type ValidationReport
} from "./core.ts"
import {
  diffResearchGraphs,
  makeResearchGraphReviewWarnings,
  type ResearchGraphReviewWarning,
  type ResearchGraphDiff
} from "./diff.ts"
import {
  createOntologyInteropCrate,
  prepareOntologyInteropCrate
} from "./crate.ts"
import { buildRdfDataset, serializeDatasetAsNQuads } from "./rdf.ts"
import {
  loadStandardShaclShapes,
  validateRdfDatasetWithShacl
} from "./shacl.ts"
import { queryRdfDataset } from "./sparql.ts"
import {
  hashOntologyDocumentAt,
  loadOntologyCollectionValidation,
  loadResearchCollection,
  loadResearchCollectionAtRevision,
  loadResearchGraphAt,
  loadResearchGraphAtRevision,
  loadValidOntologyCollectionStructure
} from "./repository.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const failedCollectionValidationReport = (
  error: IceError
): CollectionValidationReport => ({
  collection_id: "unavailable",
  schema_version: "research-collection/v1",
  valid: false,
  counts: {
    graphs: 0,
    nodes: 0,
    edges: 0,
    artifacts: 0,
    policies: 0,
    hash_bearing_nodes: 0,
    verified_hashes: 0
  },
  graphs: [],
  errors: [
    {
      severity: "error",
      code: error.code,
      message: error.message
    }
  ],
  warnings: []
})

const renderIssue = (issue: ValidationIssue): string =>
  `[${issue.severity === "error" ? "ERROR" : "WARN"}] ${issue.code}${
    issue.subject === undefined ? "" : ` (${issue.subject})`
  }: ${issue.message}`

const renderValidation = (report: ValidationReport): string =>
  [
    `${report.valid ? "VALID" : "INVALID"} ${report.graph_id} (${report.schema_version})`,
    `nodes: ${report.counts.nodes}`,
    `edges: ${report.counts.edges}`,
    `hashes: ${report.counts.verified_hashes}/${report.counts.hash_bearing_nodes} verified (${report.counts.artifacts} artifacts, ${report.counts.policies} policies)`,
    `errors: ${report.errors.length}`,
    `warnings: ${report.warnings.length}`,
    ...report.errors.map(renderIssue),
    ...report.warnings.map(renderIssue)
  ].join("\n")

const renderCollectionValidation = (
  report: CollectionValidationReport
): string =>
  [
    `${report.valid ? "VALID" : "INVALID"} ${report.collection_id} (${report.schema_version})`,
    `graphs: ${report.counts.graphs}`,
    `nodes: ${report.counts.nodes}`,
    `edges: ${report.counts.edges}`,
    `hashes: ${report.counts.verified_hashes}/${report.counts.hash_bearing_nodes} verified (${report.counts.artifacts} artifacts, ${report.counts.policies} policies)`,
    `errors: ${report.errors.length}`,
    `warnings: ${report.warnings.length}`,
    ...report.graphs.map(
      (graph) =>
        `graph ${graph.graph_id}: ${graph.valid ? "VALID" : "INVALID"}; nodes=${graph.counts.nodes}; edges=${graph.counts.edges}; hashes=${graph.counts.verified_hashes}/${graph.counts.hash_bearing_nodes}`
    ),
    ...report.errors.map(renderIssue),
    ...report.warnings.map(renderIssue)
  ].join("\n")

const renderCounts = (counts: Readonly<Record<string, number>>): string =>
  Object.entries(counts)
    .map(([key, count]) => `${key}=${count}`)
    .join(", ")

const renderSummary = (summary: OntologySummary): string =>
  [
    `${summary.title} (${summary.graph_id})`,
    `schema: ${summary.schema_version}`,
    `updated: ${summary.updated_at_utc}`,
    `nodes: ${summary.node_count} (${renderCounts(summary.nodes_by_type)})`,
    `edges: ${summary.edge_count}`,
    `claims: ${renderCounts(summary.claims_by_epistemic_state)}`,
    `open problems: ${summary.open_problem_count}`,
    `artifacts: ${summary.artifact_count}`,
    `weak components: ${summary.weak_component_count}`,
    `nodes outside programme components: ${summary.nodes_outside_programme_components}`,
    `KG bridges: ${renderCounts(summary.kg_bridges_by_status)}`,
    `validation warnings: ${summary.validation_warning_count}`
  ].join("\n")

const renderCollectionSummary = (summary: CollectionSummary): string =>
  [
    `${summary.title} (${summary.collection_id})`,
    `schema: ${summary.schema_version}`,
    `updated: ${summary.updated_at_utc}`,
    `default graph: ${summary.default_graph}`,
    `graphs: ${summary.graph_count}`,
    `totals: nodes=${summary.totals.nodes}, edges=${summary.totals.edges}, claims=${summary.totals.claims}, evidence=${summary.totals.evidence}, open_problems=${summary.totals.open_problems}, artifacts=${summary.totals.artifacts}, unresolved_bridges=${summary.totals.unresolved_bridges}`,
    ...summary.graphs.map(
      (graph) =>
        `graph ${graph.key} [${graph.coverage}]: nodes=${graph.node_count}, edges=${graph.edge_count}, weak_components=${graph.weak_component_count}, outside_programme=${graph.nodes_outside_programme_components}, claims=${renderCounts(graph.claims_by_epistemic_state)}`
    ),
    "coverage:",
    ...summary.coverage.map(
      (entry) =>
        `  ${entry.status} ${entry.path}${entry.graph === undefined ? "" : ` -> ${entry.graph}`}: ${entry.reason}`
    )
  ].join("\n")

const renderEdge = (edge: NodeView["incoming"][number]): string =>
  `${edge.from} -${edge.relation}${
    edge.polarity === undefined ? "" : `/${edge.polarity}`
  }-> ${edge.to}`

const renderNodeView = (key: string, view: NodeView): string => {
  const node = view.node
  const details = [
    `graph: ${key}`,
    `id: ${node.id}`,
    `type: ${node.type}`,
    `title: ${node.title}`,
    `state: ${node.state}`,
    `summary: ${node.summary}`
  ]
  if (node.type === "claim") {
    details.push(`claim_id: ${node.claim_id}`)
    details.push(`epistemic_state: ${node.epistemic_state}`)
    details.push(`statement: ${node.statement}`)
  }
  if (node.type === "artifact" || node.type === "policy") {
    details.push(`path: ${node.path}`)
    details.push(`sha256: ${node.sha256}`)
  }
  if (node.type === "source" && node.citation !== undefined) {
    details.push(`citation: ${node.citation}`)
  }
  if (view.outgoing.length > 0) {
    details.push(
      "outgoing:",
      ...view.outgoing.map((edge) => `  ${renderEdge(edge)}`)
    )
  }
  if (view.incoming.length > 0) {
    details.push(
      "incoming:",
      ...view.incoming.map((edge) => `  ${renderEdge(edge)}`)
    )
  }
  if (view.kg_bridges.length > 0) {
    details.push(
      "KG bridges:",
      ...view.kg_bridges.map(
        (bridge) =>
          `  ${bridge.status} ${bridge.system} ${bridge.external_uid ?? bridge.lookup_key ?? "(no lookup key)"}`
      )
    )
  }
  return details.join("\n")
}

const renderTrace = (key: string, trace: TraceResult): string =>
  [
    `graph: ${key}`,
    `root: ${trace.root}`,
    `max depth: ${trace.max_depth}`,
    "nodes:",
    ...trace.nodes.map(
      ({ distance, node }) => `  [${distance}] ${node.id} — ${node.title}`
    ),
    ...(trace.edges.length === 0
      ? []
      : ["edges:", ...trace.edges.map((edge) => `  ${renderEdge(edge)}`)]),
    ...(trace.kg_bridges.length === 0
      ? []
      : [
          "KG bridges:",
          ...trace.kg_bridges.map(
            (bridge) =>
              `  ${bridge.local_node_id}: ${bridge.status} ${bridge.system} ${
                bridge.external_uid ?? bridge.lookup_key ?? "(no lookup key)"
              }`
          )
        ])
  ].join("\n")

interface OntologyGraphReview {
  readonly graph: string
  readonly graph_id: string
  readonly path: string
  readonly base: string
  readonly warnings: ReadonlyArray<ResearchGraphReviewWarning>
  readonly diff: ResearchGraphDiff
}

interface OntologyCollectionReview {
  readonly path: string
  readonly base: string
  readonly warnings: ReadonlyArray<ResearchCollectionReviewWarning>
  readonly diff: ResearchCollectionDiff
}

interface OntologyReview {
  readonly base: string
  readonly target: "working-tree"
  readonly graph_count: number
  readonly total_changes: number
  readonly has_changes: boolean
  readonly warning_count: number
  readonly collection: OntologyCollectionReview
  readonly graphs: ReadonlyArray<OntologyGraphReview>
}

const renderReviewCounts = (
  counts: ResearchGraphDiff["summary"]["nodes"]
): string => `+${counts.added} -${counts.removed} ~${counts.changed}`

const renderReview = (review: OntologyReview): string =>
  [
    `ONTOLOGY REVIEW ${review.base} -> ${review.target}`,
    `graphs: ${review.graph_count}`,
    `changes: ${review.total_changes}`,
    `warnings: ${review.warning_count}`,
    `collection: ${review.collection.diff.summary.total_changes} change(s)`,
    `  metadata: ${review.collection.diff.summary.metadata_changes}`,
    `  graph descriptors: ${renderReviewCounts(review.collection.diff.summary.graph_descriptors)}`,
    `  reading paths: ${renderReviewCounts(review.collection.diff.summary.reading_paths)}`,
    `  quick answers: ${renderReviewCounts(review.collection.diff.summary.quick_answers)}`,
    `  coverage ledger: ${renderReviewCounts(review.collection.diff.summary.coverage_ledger)}`,
    ...review.collection.warnings.map(
      (warning) =>
        `  [WARN] ${warning.code}${warning.subject === undefined ? "" : ` (${warning.subject})`}: ${warning.message}`
    ),
    ...review.graphs.flatMap((entry) => [
      `graph ${entry.graph}: ${entry.diff.summary.total_changes} change(s)`,
      `  metadata: ${entry.diff.summary.metadata_changes}`,
      `  nodes: ${renderReviewCounts(entry.diff.summary.nodes)}`,
      `  edges: ${renderReviewCounts(entry.diff.summary.edges)}`,
      `  reading paths: ${renderReviewCounts(entry.diff.summary.reading_paths)}`,
      `  quick answers: ${renderReviewCounts(entry.diff.summary.quick_answers)}`,
      `  KG bridges: ${renderReviewCounts(entry.diff.summary.kg_bridges)}`,
      ...entry.warnings.map(
        (warning) =>
          `  [WARN] ${warning.code}${warning.subject === undefined ? "" : ` (${warning.subject})`}: ${warning.message}`
      )
    ])
  ].join("\n")

const selectGraph = (
  graphs: ReadonlyArray<CollectionGraph>,
  key: string
): Effect.Effect<CollectionGraph, IceError> => {
  const selected = graphs.find(({ descriptor }) => descriptor.key === key)
  return selected === undefined
    ? Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${key}'`,
          2
        )
      )
    : Effect.succeed(selected)
}

const resolveUniqueNode = (
  graphs: ReadonlyArray<CollectionGraph>,
  id: string,
  graphKey: string
): Effect.Effect<ResolvedCollectionNode, IceError> => {
  const qualifier = id.match(/^([a-z0-9-]+)::/)
  if (
    graphKey !== "all" &&
    qualifier?.[1] !== undefined &&
    qualifier[1] !== graphKey
  ) {
    return Effect.fail(
      iceError(
        "ONTOLOGY_GRAPH_SELECTOR_CONFLICT",
        `qualified node uses graph '${qualifier[1]}' but --graph selects '${graphKey}'`,
        2
      )
    )
  }
  const selected =
    graphKey === "all"
      ? graphs
      : graphs.filter(({ descriptor }) => descriptor.key === graphKey)
  if (graphKey !== "all" && selected.length === 0) {
    return Effect.fail(
      iceError(
        "ONTOLOGY_GRAPH_NOT_FOUND",
        `no ontology graph is registered as '${graphKey}'`,
        2
      )
    )
  }
  const matches = findCollectionNodes(selected, id)
  if (matches.length === 0) {
    return Effect.fail(
      iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
    )
  }
  if (matches.length > 1) {
    return Effect.fail(
      iceError(
        "ONTOLOGY_NODE_AMBIGUOUS",
        `ontology node '${id}' matches graphs ${matches.map(({ key }) => key).join(", ")}; pass --graph or use key::id`,
        2
      )
    )
  }
  const match = matches[0]
  return match === undefined
    ? Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    : Effect.succeed(match)
}

export const ontologyValidateCommand = (
  json: boolean,
  graphKey = "all"
) =>
  Effect.gen(function* () {
    const loaded = yield* loadOntologyCollectionValidation.pipe(Effect.either)
    if (loaded._tag === "Left") {
      const report = failedCollectionValidationReport(loaded.left)
      yield* (json
        ? printJson(report)
        : Console.log(renderCollectionValidation(report)))
      return report
    }
    if (graphKey === "all") {
      const report = loaded.right.validation
      yield* (json
        ? printJson(report)
        : Console.log(renderCollectionValidation(report)))
      return report
    }
    if (
      !loaded.right.collection.graphs.some(({ key }) => key === graphKey)
    ) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${graphKey}'`,
          2
        )
      )
    }
    if (!loaded.right.validation.valid) {
      const report = loaded.right.validation
      yield* (json
        ? printJson(report)
        : Console.log(renderCollectionValidation(report)))
      return report
    }
    const selected = yield* selectGraph(loaded.right.graphs, graphKey)
    yield* (json
      ? printJson(selected.validation)
      : Console.log(renderValidation(selected.validation)))
    return selected.validation
  })

export const ontologySummaryCommand = (
  json: boolean,
  graphKey = "all"
) =>
  Effect.gen(function* () {
    const loaded = yield* loadValidOntologyCollectionStructure
    if (graphKey === "all") {
      const summary = summarizeCollection(loaded.collection, loaded.graphs)
      yield* (json
        ? printJson(summary)
        : Console.log(renderCollectionSummary(summary)))
      return
    }
    const selected = yield* selectGraph(loaded.graphs, graphKey)
    const summary = summarizeGraph(selected.graph, selected.validation)
    yield* (json ? printJson(summary) : Console.log(renderSummary(summary)))
  })

export const ontologyShowCommand = (
  id: string,
  json: boolean,
  graphKey = "all"
) =>
  Effect.gen(function* () {
    const { graphs } = yield* loadValidOntologyCollectionStructure
    const match = yield* resolveUniqueNode(graphs, id, graphKey)
    const node = resolveNode(match.graph, match.node.id)
    if (node === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    const view = showNode(match.graph, node)
    yield* (json
      ? printJson({ graph: match.key, ...view })
      : Console.log(renderNodeView(match.key, view)))
  })

export const ontologyTraceCommand = (
  id: string,
  depth: number,
  json: boolean,
  graphKey = "all"
) => {
  if (!Number.isSafeInteger(depth) || depth < 0 || depth > 32) {
    return Effect.fail(
      iceError(
        "ONTOLOGY_INVALID_DEPTH",
        "--depth must be an integer from 0 through 32",
        2
      )
    )
  }
  return Effect.gen(function* () {
    const { graphs } = yield* loadValidOntologyCollectionStructure
    const match = yield* resolveUniqueNode(graphs, id, graphKey)
    const trace = traceGraph(match.graph, match.node, depth)
    yield* (json
      ? printJson({ graph: match.key, ...trace })
      : Console.log(renderTrace(match.key, trace)))
  })
}

const renderCollectionGuide = (
  collection: ResearchCollection,
  paths = collection.reading_paths
): string =>
  [
    `${collection.title} — intuitive guide`,
    `default graph: ${collection.default_graph}`,
    "quick answers:",
    ...collection.quick_answers.flatMap((answer) => [
      `  Q: ${answer.question}`,
      `  A: ${answer.answer}`,
      `  refs: ${answer.refs.map((ref) => `${ref.graph}::${ref.node}`).join(", ")}`
    ]),
    "cross-graph reading paths (navigation only):",
    ...paths.flatMap((path) => [
      `  ${path.id} — ${path.title}`,
      `    ${path.summary}`,
      ...path.stops.map(
        (stop, index) =>
          `    ${index + 1}. ${stop.graph}::${stop.node}${stop.why === undefined ? "" : ` — ${stop.why}`}`
      )
    ]),
    "coverage ledger:",
    ...collection.coverage_ledger.map(
      (entry) =>
        `  ${entry.status} ${entry.path}${entry.graph === undefined ? "" : ` -> ${entry.graph}`}: ${entry.reason}`
    )
  ].join("\n")

const renderGraphGuide = (
  graph: CollectionGraph,
  paths = graph.graph.reading_paths
): string =>
  [
    `${graph.graph.title} — graph guide`,
    "quick answers:",
    ...graph.graph.quick_answers.flatMap((answer) => [
      `  Q: ${answer.question}`,
      `  A: ${answer.answer}`,
      `  claims: ${answer.claim_ids.join(", ")}`
    ]),
    "reading paths:",
    ...paths.flatMap((path) => [
      `  ${path.id} — ${path.title}`,
      `    ${path.summary}`,
      `    nodes: ${path.nodes.join(" -> ")}`
    ])
  ].join("\n")

const selectReadingPaths = <T extends { readonly id: string }>(
  paths: ReadonlyArray<T>,
  requested: string,
  prefix: "collection-path:" | "reading-path:"
): Effect.Effect<ReadonlyArray<T>, IceError> => {
  if (requested.length === 0) return Effect.succeed(paths)
  const id = requested.startsWith(prefix) ? requested : `${prefix}${requested}`
  const selected = paths.find((path) => path.id === id)
  return selected === undefined
    ? Effect.fail(
        iceError(
          "ONTOLOGY_READING_PATH_NOT_FOUND",
          `no reading path matches '${requested}'`,
          2
        )
      )
    : Effect.succeed([selected])
}

export const ontologyGuideCommand = (
  json: boolean,
  graphKey = "all",
  pathId = ""
) =>
  Effect.gen(function* () {
    const loaded = yield* loadValidOntologyCollectionStructure
    if (graphKey === "all") {
      const paths = yield* selectReadingPaths(
        loaded.collection.reading_paths,
        pathId,
        "collection-path:"
      )
      const guide = {
        collection_id: loaded.collection.collection_id,
        default_graph: loaded.collection.default_graph,
        quick_answers: loaded.collection.quick_answers,
        reading_paths: paths,
        coverage_ledger: loaded.collection.coverage_ledger
      }
      yield* (json
        ? printJson(guide)
        : Console.log(renderCollectionGuide(loaded.collection, paths)))
      return
    }
    const selected = yield* selectGraph(loaded.graphs, graphKey)
    const paths = yield* selectReadingPaths(
      selected.graph.reading_paths,
      pathId,
      "reading-path:"
    )
    const guide = {
      graph_id: selected.graph.graph_id,
      quick_answers: selected.graph.quick_answers,
      reading_paths: paths
    }
    yield* (json
      ? printJson(guide)
      : Console.log(renderGraphGuide(selected, paths)))
  })

export const ontologyReviewCommand = (
  json: boolean,
  graphKey = "all",
  base = "HEAD"
) =>
  Effect.gen(function* () {
    const [baseCollection, collection] = yield* Effect.all(
      [loadResearchCollectionAtRevision(base), loadResearchCollection],
      { concurrency: 2 }
    )
    const collectionDiff = diffResearchCollections(baseCollection, collection)
    const collectionReview: OntologyCollectionReview = {
      path: collection.canonical_file,
      base,
      warnings: makeResearchCollectionReviewWarnings(
        baseCollection,
        collection,
        collectionDiff
      ),
      diff: collectionDiff
    }
    const descriptors =
      graphKey === "all"
        ? collection.graphs
        : collection.graphs.filter(({ key }) => key === graphKey)
    if (descriptors.length === 0) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${graphKey}'`,
          2
        )
      )
    }
    const graphs = yield* Effect.forEach(
      descriptors,
      (descriptor) =>
        Effect.gen(function* () {
          const [before, current] = yield* Effect.all(
            [
              loadResearchGraphAtRevision(base, descriptor.path),
              loadResearchGraphAt(descriptor.path)
            ],
            { concurrency: 2 }
          )
          const diff = diffResearchGraphs(before, current)
          return {
            graph: descriptor.key,
            graph_id: current.graph_id,
            path: descriptor.path,
            base,
            warnings: makeResearchGraphReviewWarnings(before, current, diff),
            diff
          } satisfies OntologyGraphReview
        }),
      { concurrency: 2 }
    )
    const review: OntologyReview = {
      base,
      target: "working-tree",
      graph_count: graphs.length,
      total_changes:
        collectionReview.diff.summary.total_changes +
        graphs.reduce(
          (total, entry) => total + entry.diff.summary.total_changes,
          0
        ),
      has_changes:
        collectionReview.diff.summary.has_changes ||
        graphs.some(({ diff }) => diff.summary.has_changes),
      warning_count:
        collectionReview.warnings.length +
        graphs.reduce((total, entry) => total + entry.warnings.length, 0),
      collection: collectionReview,
      graphs
    }
    yield* (json ? printJson(review) : Console.log(renderReview(review)))
    return review
  })

const loadOntologyInteropInputs = (graphKey = "all") =>
  Effect.gen(function* () {
    const loaded = yield* loadValidOntologyCollectionStructure
    if (
      graphKey !== "all" &&
      !loaded.collection.graphs.some(({ key }) => key === graphKey)
    ) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${graphKey}'`,
          2
        )
      )
    }
    const sourceDocuments = yield* Effect.forEach(
      [
        loaded.collection.canonical_file,
        ...loaded.collection.graphs
          .filter(({ key }) => graphKey === "all" || key === graphKey)
          .map(({ path }) => path)
      ],
      (path) =>
        hashOntologyDocumentAt(path).pipe(
          Effect.map((sha256) => ({ path, sha256 }))
        ),
      { concurrency: 4 }
    )
    return {
      loaded,
      options: {
        ...(graphKey === "all" ? {} : { graphKeys: [graphKey] }),
        sourceDocuments
      }
    }
  })

export const ontologyRdfData = (graphKey = "all") =>
  loadOntologyInteropInputs(graphKey).pipe(
    Effect.flatMap(({ loaded, options }) =>
      Effect.tryPromise({
        try: () => buildRdfDataset(loaded.collection, loaded.graphs, options),
        catch: (error) =>
          iceError(
            "ONTOLOGY_RDF_BUILD_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const ontologyExportCommand = (
  format: "jsonld" | "dataset-jsonld" | "nquads",
  graphKey = "all"
) =>
  ontologyRdfData(graphKey).pipe(
    Effect.tap((built) =>
      format === "jsonld"
        ? printJson(built.projection)
        : format === "dataset-jsonld"
          ? printJson(built.datasetProjection)
        : Console.log(serializeDatasetAsNQuads(built.dataset).trimEnd())
    ),
    Effect.map((built) =>
      format === "jsonld"
        ? built.projection
        : format === "dataset-jsonld"
          ? built.datasetProjection
        : serializeDatasetAsNQuads(built.dataset)
    )
  )

export const ontologyShaclData = (graphKey = "all") =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const built = yield* ontologyRdfData(graphKey)
    return yield* Effect.tryPromise({
      try: async () =>
        validateRdfDatasetWithShacl(
          built.dataset,
          await loadStandardShaclShapes(workspace.root)
        ),
      catch: (error) =>
        iceError(
          "ONTOLOGY_SHACL_VALIDATION_FAILED",
          error instanceof Error ? error.message : String(error),
          2
        )
    })
  })

export const ontologyShaclCommand = (
  json: boolean,
  graphKey = "all"
) =>
  ontologyShaclData(graphKey).pipe(
    Effect.tap((report) =>
      json
        ? printJson(report)
        : Console.log(
            [
              `SHACL ${report.conforms ? "CONFORMS" : "NONCONFORMING"}`,
              `violations: ${report.violations.length}`,
              ...report.violations.map(
                (violation) =>
                  `${violation.focus_node} ${violation.path}: ${violation.message.join("; ")}`
              ),
              "boundary: projection-shape QA only; native hash/evidence validation remains separate"
            ].join("\n")
          )
    )
  )

export const ontologySparqlData = (
  query: string,
  graphKey = "all",
  limit = 100,
  timeoutMs = 5_000
) =>
  ontologyRdfData(graphKey).pipe(
    Effect.flatMap((built) =>
      Effect.tryPromise({
        try: () =>
          queryRdfDataset(built.dataset, query, { limit, timeoutMs }),
        catch: (error) =>
          iceError(
            "ONTOLOGY_SPARQL_QUERY_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const ontologySparqlCommand = (
  query: string,
  graphKey: string,
  limit: number,
  timeoutMs: number
) =>
  ontologySparqlData(query, graphKey, limit, timeoutMs).pipe(
    Effect.tap(printJson)
  )

export const ontologyCratePreviewData = (graphKey = "all") =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const { loaded, options } = yield* loadOntologyInteropInputs(graphKey)
    const prepared = yield* Effect.tryPromise({
      try: () =>
        prepareOntologyInteropCrate(loaded.collection, loaded.graphs, {
          ...options,
          workspaceRoot: workspace.root
        }),
      catch: (error) =>
        iceError(
          "ONTOLOGY_RO_CRATE_PREVIEW_FAILED",
          error instanceof Error ? error.message : String(error),
          2
        )
    })
    return {
      schema: prepared.schema,
      metadata: prepared.metadata,
      manifest: prepared.manifest,
      shacl: prepared.shacl,
      boundary:
        "read-only preview; raw results are not bundled and no file has been written"
    }
  })

export const ontologyCrateCommand = (
  outputDirectory: string,
  graphKey: string,
  json: boolean
) =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const { loaded, options } = yield* loadOntologyInteropInputs(graphKey)
    const result = yield* Effect.tryPromise({
      try: () =>
        createOntologyInteropCrate(loaded.collection, loaded.graphs, {
          ...options,
          workspaceRoot: workspace.root,
          outputDirectory
        }),
      catch: (error) =>
        iceError(
          "ONTOLOGY_RO_CRATE_CREATE_FAILED",
          error instanceof Error ? error.message : String(error),
          2
        )
    })
    yield* (json
      ? printJson(result)
      : Console.log(
          [
            `RO-Crate created: ${result.directory}`,
            `files: ${result.files.length}`,
            `manifest sha256: ${result.manifest_sha256}`,
            "scope: metadata and graph export only; raw results were not copied"
          ].join("\n")
        ))
    return result
  })
