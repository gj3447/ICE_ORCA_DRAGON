import type { CollectionGraph } from "../ontology/collection-core.ts"
import { traceGraph, type TraceResult } from "../ontology/core.ts"
import type { ResearchNode } from "../ontology/model.ts"

export const graphHarnessContract = {
  schema: "ice-graph-harness/v1",
  mode: "GRAPH_AWARE_HUMAN_DIRECTED",
  raw_result_check_ledger: "SINGLE_SOURCE",
  automatic_follow_up: false,
  execution_authorization: "NOT_GRANTED"
} as const

export interface HarnessNode {
  readonly distance: number
  readonly id: string
  readonly type: ResearchNode["type"]
  readonly title: string
  readonly state: string
}

export interface GraphHarnessContext {
  readonly schema: "ice-graph-harness-context/v1"
  readonly contract: typeof graphHarnessContract
  readonly graph: string
  readonly target: HarnessNode
  readonly depth: number
  readonly limit: number
  readonly available_nodes: number
  readonly returned_nodes: number
  readonly truncated: boolean
  readonly context: {
    readonly claims: ReadonlyArray<HarnessNode>
    readonly evidence: ReadonlyArray<HarnessNode>
    readonly scopes: ReadonlyArray<HarnessNode>
    readonly open_problems: ReadonlyArray<HarnessNode>
    readonly sources: ReadonlyArray<HarnessNode>
    readonly artifacts: ReadonlyArray<HarnessNode>
    readonly policies: ReadonlyArray<HarnessNode>
  }
  readonly edges: TraceResult["edges"]
  readonly guidance: ReadonlyArray<string>
}

export type GraphImpactMatchKind =
  | "artifact"
  | "policy"
  | "graph"
  | "guide"
  | "collection"

export interface GraphHarnessImpact {
  readonly schema: "ice-graph-harness-impact/v1"
  readonly contract: typeof graphHarnessContract
  readonly path: string
  readonly matches: ReadonlyArray<{
    readonly graph: string
    readonly kind: GraphImpactMatchKind
    readonly node?: HarnessNode | undefined
    readonly context?: GraphHarnessContext | undefined
  }>
  readonly registered: boolean
  readonly guidance: ReadonlyArray<string>
}

const harnessNode = ({ distance, node }: TraceResult["nodes"][number]): HarnessNode => ({
  distance,
  id: node.id,
  type: node.type,
  title: node.title,
  state: node.state
})

const typedNodes = (
  trace: TraceResult,
  type: ResearchNode["type"]
): ReadonlyArray<HarnessNode> =>
  trace.nodes.filter((entry) => entry.node.type === type).map(harnessNode)

export const graphHarnessContext = (
  graph: CollectionGraph,
  target: ResearchNode,
  depth: number,
  limit = 64
): GraphHarnessContext => {
  const completeTrace = traceGraph(graph.graph, target, depth)
  const nodes = completeTrace.nodes.slice(0, limit)
  const included = new Set(nodes.map(({ node }) => node.id))
  const trace: TraceResult = {
    ...completeTrace,
    nodes,
    edges: completeTrace.edges.filter(
      (edge) => included.has(edge.from) && included.has(edge.to)
    ),
    kg_bridges: completeTrace.kg_bridges.filter((bridge) =>
      included.has(bridge.local_node_id)
    )
  }
  return {
    schema: "ice-graph-harness-context/v1",
    contract: graphHarnessContract,
    graph: graph.descriptor.key,
    target: harnessNode({ distance: 0, node: target }),
    depth,
    limit,
    available_nodes: completeTrace.nodes.length,
    returned_nodes: trace.nodes.length,
    truncated: completeTrace.nodes.length > trace.nodes.length,
    context: {
      claims: typedNodes(trace, "claim"),
      evidence: typedNodes(trace, "evidence"),
      scopes: typedNodes(trace, "scope"),
      open_problems: typedNodes(trace, "open_problem"),
      sources: typedNodes(trace, "source"),
      artifacts: typedNodes(trace, "artifact"),
      policies: typedNodes(trace, "policy")
    },
    edges: trace.edges,
    guidance: [
      "Use this as provenance and change-impact context, not as an execution authorization.",
      "Keep an executed calculation's full check ledger in its raw result; this view intentionally retains only graph-level locators.",
      "A listed open problem is a human review input, not an automatic next experiment.",
      ...(completeTrace.nodes.length > trace.nodes.length
        ? [
            `Context is truncated to ${trace.nodes.length}/${completeTrace.nodes.length} nodes; reduce --depth or raise --limit for a wider review.`
          ]
        : [])
    ]
  }
}

const exactPathMatches = (
  graph: CollectionGraph,
  path: string,
  depth: number,
  limit: number
): ReadonlyArray<GraphHarnessImpact["matches"][number]> => {
  const hashNodes = graph.graph.nodes.filter(
    (
      node
    ): node is Extract<ResearchNode, { readonly type: "artifact" | "policy" }> =>
      (node.type === "artifact" || node.type === "policy") && node.path === path
  )
  const matchedNodes = hashNodes.map((node) => ({
    graph: graph.descriptor.key,
    kind: node.type,
    node: harnessNode({ distance: 0, node }),
    context: graphHarnessContext(graph, node, depth, limit)
  }))
  if (matchedNodes.length > 0) return matchedNodes

  if (graph.descriptor.path === path) {
    return [{ graph: graph.descriptor.key, kind: "graph" }]
  }
  if (graph.descriptor.guide === path) {
    return [{ graph: graph.descriptor.key, kind: "guide" }]
  }
  return []
}

export const graphHarnessImpact = (
  graphs: ReadonlyArray<CollectionGraph>,
  path: string,
  depth: number,
  limit: number,
  isCollectionManifest: boolean
): GraphHarnessImpact => {
  const matches = [
    ...(isCollectionManifest
      ? graphs.map((graph) => ({
          graph: graph.descriptor.key,
          kind: "collection" as const
        }))
      : []),
    ...graphs.flatMap((graph) => exactPathMatches(graph, path, depth, limit))
  ]
  return {
    schema: "ice-graph-harness-impact/v1",
    contract: graphHarnessContract,
    path,
    matches,
    registered: matches.length > 0,
    guidance:
      matches.length > 0
        ? [
            "Review the listed graph context before changing a tracked record.",
            "If the change materially alters a claim, direct evidence, scope, or open problem, update the graph and run `./ice harness check`.",
            "This impact report does not approve a calculation or create a successor task."
          ]
        : [
            "No exact graph registration exists for this path. Record execution provenance beside the raw result when applicable.",
            "Register a result in the ontology only when it materially alters a claim, direct evidence, scope, or open problem.",
            "This unregistered path is not evidence that a new graph node is required."
          ]
  }
}
