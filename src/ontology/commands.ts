import { Console, Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
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
import { loadOntologyValidation, loadValidOntology } from "./repository.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const failedValidationReport = (error: IceError): ValidationReport => ({
  graph_id: "unavailable",
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

const renderEdge = (
  edge: NodeView["incoming"][number]
): string =>
  `${edge.from} -${edge.relation}${
    edge.polarity === undefined ? "" : `/${edge.polarity}`
  }-> ${edge.to}`

const renderNodeView = (view: NodeView): string => {
  const node = view.node
  const details = [
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
    details.push("outgoing:", ...view.outgoing.map((edge) => `  ${renderEdge(edge)}`))
  }
  if (view.incoming.length > 0) {
    details.push("incoming:", ...view.incoming.map((edge) => `  ${renderEdge(edge)}`))
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

const renderTrace = (trace: TraceResult): string =>
  [
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

export const ontologyValidateCommand = (json: boolean) =>
  Effect.gen(function* () {
    const loaded = yield* loadOntologyValidation.pipe(Effect.either)
    const validation =
      loaded._tag === "Left"
        ? failedValidationReport(loaded.left)
        : loaded.right.validation
    yield* (json ? printJson(validation) : Console.log(renderValidation(validation)))
    return validation
  })

export const ontologySummaryCommand = (json: boolean) =>
  Effect.gen(function* () {
    const { graph, validation } = yield* loadValidOntology
    const summary = summarizeGraph(graph, validation)
    yield* (json ? printJson(summary) : Console.log(renderSummary(summary)))
  })

export const ontologyShowCommand = (id: string, json: boolean) =>
  Effect.gen(function* () {
    const { graph } = yield* loadValidOntology
    const node = resolveNode(graph, id)
    if (node === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    const view = showNode(graph, node)
    yield* (json ? printJson(view) : Console.log(renderNodeView(view)))
  })

export const ontologyTraceCommand = (
  id: string,
  depth: number,
  json: boolean
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
    const { graph } = yield* loadValidOntology
    const node = resolveNode(graph, id)
    if (node === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    const trace = traceGraph(graph, node, depth)
    yield* (json ? printJson(trace) : Console.log(renderTrace(trace)))
  })
}
