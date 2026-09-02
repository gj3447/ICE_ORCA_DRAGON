import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { graphRagSearchData } from "../graphrag/commands.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { validateScientificIntuitionFlow } from "./core.ts"
import { loadScientificIntuitionFlow } from "./repository.ts"

const qualifiedTarget = /^([a-z0-9-]+)::([a-z_]+:[A-Za-z0-9_.:-]+)$/
const MAX_RETURNED_SIGNALS = 20
const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const loadedValidatedFlow = Effect.all({
  flow: loadScientificIntuitionFlow,
  ontology: loadValidOntologyCollectionStructure
}).pipe(
  Effect.flatMap(({ flow, ontology }) => {
    const report = validateScientificIntuitionFlow(flow, ontology.graphs)
    return report.valid
      ? Effect.succeed({ flow, ontology, report })
      : Effect.fail(
          iceError(
            "INTUITION_SEMANTICS_INVALID",
            report.errors.map(({ code }) => code).join(", ")
          )
        )
  })
)

export const scientificIntuitionValidateData = loadedValidatedFlow.pipe(
  Effect.map(({ report }) => report)
)

export const scientificIntuitionSearchData = (
  query: string,
  targetValue: string,
  limit: number,
  depth: number
) =>
  Effect.gen(function* () {
    const match = qualifiedTarget.exec(targetValue)
    const graph = match?.[1]
    const node = match?.[2]
    if (graph === undefined || node === undefined) {
      return yield* Effect.fail(
        iceError(
          "INTUITION_TARGET_INVALID",
          "target must be graph::open_problem-id",
          2
        )
      )
    }
    const { flow, ontology } = yield* loadedValidatedFlow
    const targetGraph = ontology.graphs.find(({ descriptor }) => descriptor.key === graph)
    const targetNode = targetGraph?.graph.nodes.find(({ id }) => id === node)
    if (targetNode?.type !== "open_problem") {
      return yield* Effect.fail(
        iceError(
          "INTUITION_TARGET_INVALID",
          "target must identify a canonical open_problem",
          2
        )
      )
    }
    const canonicalContext = yield* graphRagSearchData(query, { graph, limit, depth })
    const sources = new Map(flow.sources.map((source) => [source.id, source]))
    const matchingSignals = flow.signals.filter(
      (signal) => signal.target.graph === graph && signal.target.node === node
    )
    const signals = matchingSignals
      .slice(0, MAX_RETURNED_SIGNALS)
      .map((signal) => ({
        ...signal,
        sources: signal.source_refs
          .map((id) => sources.get(id))
          .filter(
            (source): source is NonNullable<typeof source> => source !== undefined
          )
      }))
    const federatedLinks = signals.flatMap((signal) => [
      {
        from: signal.id,
        relation: "TARGETS_CANONICAL_OPEN_PROBLEM" as const,
        to: `${graph}::${node}`,
        layer: flow.authority
      },
      ...signal.source_refs.map((sourceId) => ({
        from: signal.id,
        relation: "CITES_SOURCE" as const,
        to: sourceId,
        layer: flow.authority
      }))
    ])
    const referencedSourceIds = new Set(signals.flatMap(({ source_refs }) => source_refs))
    const canonicalSourceLinks = [...sources.values()].flatMap((source) =>
      !referencedSourceIds.has(source.id) || source.canonical_source === undefined
        ? []
        : [
            {
              from: source.id,
              relation: "MIRRORS_CANONICAL_SOURCE" as const,
              to: `${source.canonical_source.graph}::${source.canonical_source.node}`,
              layer: flow.authority
            }
          ]
    )
    return {
      schema: "scientific-intuition-flow-search/v1" as const,
      contract: {
        authority: flow.authority,
        canonical_graph_unchanged: flow.canonical_graph_unchanged,
        does_not_authorize_execution: flow.does_not_authorize_execution
      },
      target: { graph, node },
      canonical_target: {
        id: `${graph}::${targetNode.id}`,
        type: targetNode.type,
        title: targetNode.title,
        state: targetNode.state,
        question: targetNode.question
      },
      canonical_context: canonicalContext,
      signal_selection: {
        mode: "EXACT_TARGET_FILE_ORDER" as const,
        query_ranking: false,
        matched: matchingSignals.length,
        returned: signals.length,
        limit: MAX_RETURNED_SIGNALS
      },
      non_authoritative_signals: signals,
      federated_links: [...federatedLinks, ...canonicalSourceLinks],
      standards_alignment: flow.standards_alignment,
      boundary: [
        "Signals are source-backed hypothesis-generation lenses, not claims, evidence, probabilities, or scores.",
        "Signal selection is exact target matching in file order; the query ranks canonical context only.",
        "The canonical ontology, GraphRAG index, and TOE planner are unchanged by this read-only sidecar.",
        "Read the cited primary source and retain one bounded falsifiable question before any human research decision."
      ]
    }
  })

export const scientificIntuitionValidateCommand = (json: boolean) =>
  scientificIntuitionValidateData.pipe(
    Effect.tap((report) =>
      json ? printJson(report) : Console.log(JSON.stringify(report, null, 2))
    )
  )

export const scientificIntuitionSearchCommand = (
  query: string,
  target: string,
  limit: number,
  depth: number,
  json: boolean
) =>
  scientificIntuitionSearchData(query, target, limit, depth).pipe(
    Effect.tap((result) =>
      json ? printJson(result) : Console.log(JSON.stringify(result, null, 2))
    )
  )
