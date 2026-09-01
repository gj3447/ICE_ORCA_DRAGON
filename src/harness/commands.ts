import { Console, Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import {
  findCollectionNodes,
  type CollectionGraph,
  type CollectionValidationReport
} from "../ontology/collection-core.ts"
import { isSafeArtifactPath, type ValidationReport } from "../ontology/core.ts"
import {
  loadOntologyCollectionValidation,
  loadValidOntologyCollectionStructure
} from "../ontology/repository.ts"
import {
  graphHarnessContext,
  graphHarnessImpact,
  graphHarnessContract,
  type GraphHarnessContext
} from "./core.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const selectGraph = (
  graphs: ReadonlyArray<CollectionGraph>,
  key: string
): Effect.Effect<ReadonlyArray<CollectionGraph>, IceError> => {
  if (key === "all") return Effect.succeed(graphs)
  const graph = graphs.find(({ descriptor }) => descriptor.key === key)
  return graph === undefined
    ? Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${key}'`,
          2
        )
      )
    : Effect.succeed([graph])
}

const resolveUniqueNode = (
  graphs: ReadonlyArray<CollectionGraph>,
  id: string,
  graphKey: string
): Effect.Effect<{ readonly graph: CollectionGraph; readonly id: string }, IceError> =>
  Effect.gen(function* () {
    const qualifier = id.match(/^([a-z0-9-]+)::/)
    if (
      graphKey !== "all" &&
      qualifier?.[1] !== undefined &&
      qualifier[1] !== graphKey
    ) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_SELECTOR_CONFLICT",
          `qualified node uses graph '${qualifier[1]}' but --graph selects '${graphKey}'`,
          2
        )
      )
    }
    const selected = yield* selectGraph(graphs, graphKey)
    const matches = findCollectionNodes(selected, id)
    if (matches.length === 0) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    if (matches.length > 1) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_NODE_AMBIGUOUS",
          `ontology node '${id}' matches graphs ${matches.map(({ key }) => key).join(", ")}; pass --graph or use key::id`,
          2
        )
      )
    }
    const match = matches[0]
    if (match === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    const graph = selected.find(({ descriptor }) => descriptor.key === match.key)
    if (graph === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_GRAPH_NOT_FOUND", `no ontology graph is registered as '${match.key}'`, 2)
      )
    }
    return { graph, id: match.node.id }
  })

const renderNode = (node: GraphHarnessContext["target"]): string =>
  `[${node.distance}] ${node.id} (${node.type}, ${node.state}) — ${node.title}`

const renderContextGroup = (
  label: string,
  nodes: ReadonlyArray<GraphHarnessContext["target"]>
): ReadonlyArray<string> =>
  nodes.length === 0 ? [] : [label, ...nodes.map((node) => `  ${renderNode(node)}`)]

const renderContext = (context: GraphHarnessContext): string =>
  [
    `graph harness context: ${context.graph}`,
    `target: ${renderNode(context.target)}`,
    `depth: ${context.depth}`,
    `nodes: ${context.returned_nodes}/${context.available_nodes}${context.truncated ? " (truncated)" : ""}`,
    ...renderContextGroup("claims:", context.context.claims),
    ...renderContextGroup("evidence:", context.context.evidence),
    ...renderContextGroup("scopes:", context.context.scopes),
    ...renderContextGroup("open problems:", context.context.open_problems),
    ...renderContextGroup("sources:", context.context.sources),
    ...renderContextGroup("artifacts:", context.context.artifacts),
    ...renderContextGroup("policies:", context.context.policies),
    "boundaries:",
    `  raw result ledger: ${context.contract.raw_result_check_ledger}`,
    `  automatic follow-up: ${String(context.contract.automatic_follow_up)}`,
    `  execution authorization: ${context.contract.execution_authorization}`
  ].join("\n")

const renderImpact = (impact: ReturnType<typeof graphHarnessImpact>): string =>
  [
    `graph harness impact: ${impact.path}`,
    `registered: ${String(impact.registered)}`,
    ...(impact.matches.length === 0
      ? []
      : [
          "matches:",
          ...impact.matches.flatMap((match) => [
            `  ${match.graph}: ${match.kind}${match.node === undefined ? "" : ` ${match.node.id}`}`,
            ...(match.context === undefined
              ? []
              : match.context.context.claims.map(
                  (claim) => `    claim: ${claim.id} — ${claim.title}`
                ))
          ])
        ]),
    "boundaries:",
    `  automatic follow-up: ${String(impact.contract.automatic_follow_up)}`,
    `  execution authorization: ${impact.contract.execution_authorization}`
  ].join("\n")

const checkReport = (report: ValidationReport | CollectionValidationReport) => ({
  schema: "ice-graph-harness-check/v1",
  contract: graphHarnessContract,
  valid: report.valid,
  graph_validation: report,
  guidance: [
    "A valid harness check verifies graph structure, tracked hashes, and evidence-snapshot integrity; it does not validate a scientific interpretation.",
    "A passing check neither authorizes execution nor creates a follow-up task."
  ]
})

const renderCheck = (check: ReturnType<typeof checkReport>): string => {
  const report = check.graph_validation
  const subject =
    "graph_id" in report ? report.graph_id : report.collection_id
  return [
    `${check.valid ? "VALID" : "INVALID"} graph-aware harness`,
    `subject: ${subject}`,
    `hashes: ${report.counts.verified_hashes}/${report.counts.hash_bearing_nodes} verified`,
    `errors: ${report.errors.length}`,
    `warnings: ${report.warnings.length}`,
    `automatic follow-up: ${String(check.contract.automatic_follow_up)}`,
    `execution authorization: ${check.contract.execution_authorization}`
  ].join("\n")
}

export const graphHarnessContextCommand = (
  id: string,
  depth: number,
  limit: number,
  json: boolean,
  graphKey = "all"
) => {
  if (!Number.isSafeInteger(depth) || depth < 0 || depth > 32) {
    return Effect.fail(
      iceError("ONTOLOGY_INVALID_DEPTH", "--depth must be an integer from 0 through 32", 2)
    )
  }
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 256) {
    return Effect.fail(
      iceError("HARNESS_INVALID_LIMIT", "--limit must be an integer from 1 through 256", 2)
    )
  }
  return Effect.gen(function* () {
    const { graphs } = yield* loadValidOntologyCollectionStructure
    const resolved = yield* resolveUniqueNode(graphs, id, graphKey)
    const target = resolved.graph.graph.nodes.find((node) => node.id === resolved.id)
    if (target === undefined) {
      return yield* Effect.fail(
        iceError("ONTOLOGY_NODE_NOT_FOUND", `no ontology node matches '${id}'`, 2)
      )
    }
    const context = graphHarnessContext(resolved.graph, target, depth, limit)
    yield* (json ? printJson(context) : Console.log(renderContext(context)))
    return context
  })
}

export const graphHarnessImpactCommand = (
  path: string,
  depth: number,
  limit: number,
  json: boolean,
  graphKey = "all"
) => {
  if (!isSafeArtifactPath(path)) {
    return Effect.fail(
      iceError(
        "HARNESS_PATH_UNSAFE",
        `path must be a safe repository-relative path: '${path}'`,
        2
      )
    )
  }
  if (!Number.isSafeInteger(depth) || depth < 0 || depth > 32) {
    return Effect.fail(
      iceError("ONTOLOGY_INVALID_DEPTH", "--depth must be an integer from 0 through 32", 2)
    )
  }
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 256) {
    return Effect.fail(
      iceError("HARNESS_INVALID_LIMIT", "--limit must be an integer from 1 through 256", 2)
    )
  }
  return Effect.gen(function* () {
    const loaded = yield* loadValidOntologyCollectionStructure
    const graphs = yield* selectGraph(loaded.graphs, graphKey)
    const impact = graphHarnessImpact(
      graphs,
      path,
      depth,
      limit,
      path === "ontology/collection.json"
    )
    yield* (json ? printJson(impact) : Console.log(renderImpact(impact)))
    return impact
  })
}

export const graphHarnessCheckCommand = (json: boolean, graphKey = "all") =>
  Effect.gen(function* () {
    const loaded = yield* loadOntologyCollectionValidation
    const report =
      graphKey === "all" || !loaded.validation.valid
        ? loaded.validation
        : loaded.graphs.find(({ descriptor }) => descriptor.key === graphKey)
            ?.validation
    if (report === undefined) {
      return yield* Effect.fail(
        iceError(
          "ONTOLOGY_GRAPH_NOT_FOUND",
          `no ontology graph is registered as '${graphKey}'`,
          2
        )
      )
    }
    const check = checkReport(report)
    yield* (json ? printJson(check) : Console.log(renderCheck(check)))
    return check
  })
