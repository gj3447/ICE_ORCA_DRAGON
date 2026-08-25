import { Console, Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
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
  loadOntologyCollectionValidation,
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
    `KG bridges: ${renderCounts(summary.kg_bridges_by_status)}`,
    `validation warnings: ${summary.validation_warning_count}`
  ].join("\n")

const renderCollectionSummary = (summary: CollectionSummary): string =>
  [
    `${summary.title} (${summary.collection_id})`,
    `schema: ${summary.schema_version}`,
    `updated: ${summary.updated_at_utc}`,
    `graphs: ${summary.graph_count}`,
    `totals: nodes=${summary.totals.nodes}, edges=${summary.totals.edges}, claims=${summary.totals.claims}, evidence=${summary.totals.evidence}, open_problems=${summary.totals.open_problems}, artifacts=${summary.totals.artifacts}, unresolved_bridges=${summary.totals.unresolved_bridges}`,
    ...summary.graphs.map(
      (graph) =>
        `graph ${graph.key} [${graph.coverage}]: nodes=${graph.node_count}, edges=${graph.edge_count}, claims=${renderCounts(graph.claims_by_epistemic_state)}`
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
