import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { loadScientificIntuitionFlow } from "../intuition/repository.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { topologicalStepIds, validateIceComparatorProtocol } from "./core.ts"
import type { ComparatorEdge, ComparatorStep } from "./model.ts"
import { loadIceComparatorProtocol } from "./repository.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

const loadedProtocolInputs = Effect.all({
  protocol: loadIceComparatorProtocol,
  intuition: loadScientificIntuitionFlow,
  ontology: loadValidOntologyCollectionStructure
})

const loadedValidatedProtocol = loadedProtocolInputs.pipe(
  Effect.flatMap(({ protocol, intuition, ontology }) => {
    const report = validateIceComparatorProtocol(protocol, intuition, ontology.graphs)
    return report.valid
      ? Effect.succeed({ protocol, intuition, ontology, report })
      : Effect.fail(
          iceError(
            "COMPARATOR_PROTOCOL_SEMANTICS_INVALID",
            report.errors.map(({ code }) => code).join(", ")
          )
        )
  })
)

export const comparatorProtocolValidateData = loadedProtocolInputs.pipe(
  Effect.map(({ protocol, intuition, ontology }) =>
    validateIceComparatorProtocol(protocol, intuition, ontology.graphs)
  )
)

const countBy = <T>(
  values: ReadonlyArray<T>,
  key: (value: T) => string
): Readonly<Record<string, number>> => {
  const counts: Record<string, number> = {}
  for (const value of values) {
    const name = key(value)
    counts[name] = (counts[name] ?? 0) + 1
  }
  return counts
}

export const comparatorProtocolSummaryData = loadedValidatedProtocol.pipe(
  Effect.map(({ protocol, report }) => ({
    schema: "ice-comparator-protocol-summary/v1" as const,
    protocol_id: protocol.protocol_id,
    title: protocol.title,
    updated_at_utc: protocol.updated_at_utc,
    contract: {
      authority: protocol.authority,
      canonical_graph_unchanged: protocol.canonical_graph_unchanged,
      does_not_authorize_execution: protocol.does_not_authorize_execution,
      result_status: protocol.result_status
    },
    counts: report.counts,
    by_lane: countBy(protocol.steps, ({ lane }) => lane),
    by_step_kind: countBy(protocol.steps, ({ kind }) => kind),
    by_relation: countBy(protocol.edges, ({ relation }) => relation),
    selected_strategy: protocol.selected_strategy,
    geometry_route: topologicalStepIds(
      protocol.steps,
      protocol.edges,
      "GEOMETRY_COMPARATOR"
    ),
    parallel_route: topologicalStepIds(
      protocol.steps,
      protocol.edges,
      "FOLDED_SUSY_CLASSIFICATION"
    ),
    consumers: protocol.consumers,
    solver_pins: protocol.tools.map((tool) => ({
      id: tool.id,
      name: tool.name,
      repository_uri: tool.repository_uri,
      observed_commit: tool.observed_commit,
      observed_at_utc: tool.observed_at_utc,
      installation_status: tool.installation_status,
      license_status: tool.license_status
    })),
    boundaries: protocol.boundaries
  }))
)

const prerequisiteProducers = (
  step: ComparatorStep,
  steps: ReadonlyArray<ComparatorStep>
) => step.prerequisite_outputs.map((output) => ({
  output,
  producer: steps.find((candidate) => candidate.outputs.some(({ id }) => id === output))?.id ?? null
}))

export const comparatorProtocolShowData = (target: string) =>
  loadedValidatedProtocol.pipe(
    Effect.flatMap(({ protocol }) => {
      const source = protocol.source_pins.find(({ id }) => id === target)
      if (source !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "source_pin" as const,
          entity: source,
          referenced_by_models: protocol.models.filter(({ source_refs }) => source_refs.includes(target)).map(({ id }) => id),
          referenced_by_steps: protocol.steps.filter(({ source_refs }) => source_refs.includes(target)).map(({ id }) => id),
          boundary: "A pinned source supports protocol design only; it is not ICE evidence."
        })
      }
      const tool = protocol.tools.find(({ id }) => id === target)
      if (tool !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "tool" as const,
          entity: tool,
          paper_source: protocol.source_pins.find(({ id }) => id === tool.paper_source_ref) ?? null,
          referenced_by_steps: protocol.steps.filter(({ tool_refs }) => tool_refs.includes(target)).map(({ id }) => id),
          boundary: "A source pin is not an installation, execution, or numerical result."
        })
      }
      const model = protocol.models.find(({ id }) => id === target)
      if (model !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "model" as const,
          entity: model,
          sources: model.source_refs.map((id) => protocol.source_pins.find((sourcePin) => sourcePin.id === id)),
          referenced_by_steps: protocol.steps.filter(({ model_refs }) => model_refs.includes(target)).map(({ id }) => id),
          boundary: model.non_claim
        })
      }
      const consumer = protocol.consumers.find(({ id }) => id === target)
      if (consumer !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "consumer" as const,
          entity: consumer,
          referenced_by_steps: protocol.steps.filter(({ consumer_refs }) => consumer_refs.includes(target)).map(({ id }) => id),
          boundary: consumer.non_claim
        })
      }
      const step = protocol.steps.find(({ id }) => id === target)
      if (step !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "step" as const,
          entity: step,
          resolved: {
            topics: step.topic_refs,
            contexts: step.context_refs,
            models: step.model_refs.map((id) => protocol.models.find((candidate) => candidate.id === id)),
            sources: step.source_refs.map((id) => protocol.source_pins.find((candidate) => candidate.id === id)),
            tools: step.tool_refs.map((id) => protocol.tools.find((candidate) => candidate.id === id)),
            consumers: step.consumer_refs.map((id) => protocol.consumers.find((candidate) => candidate.id === id)),
            prerequisite_producers: prerequisiteProducers(step, protocol.steps)
          },
          incoming_edges: protocol.edges.filter(({ to }) => to === target),
          outgoing_edges: protocol.edges.filter(({ from }) => from === target),
          boundary: step.non_claim
        })
      }
      const edge = protocol.edges.find(({ id }) => id === target)
      if (edge !== undefined) {
        return Effect.succeed<unknown>({
          schema: "ice-comparator-protocol-show/v1" as const,
          entity_kind: "edge" as const,
          entity: edge,
          from_step: protocol.steps.find(({ id }) => id === edge.from),
          to_step: protocol.steps.find(({ id }) => id === edge.to),
          boundary: edge.non_claim
        })
      }
      return Effect.fail(
        iceError("COMPARATOR_PROTOCOL_TARGET_NOT_FOUND", `route entity '${target}' was not found`, 2)
      )
    })
  )

const reachable = (
  start: string,
  edges: ReadonlyArray<ComparatorEdge>,
  direction: "ancestors" | "descendants"
): ReadonlyArray<string> => {
  const selected = edges.filter(({ relation }) => relation !== "INDEPENDENT_PARALLEL_TO")
  const queue = [start]
  const visited = new Set<string>()
  while (queue.length > 0) {
    const current = queue.shift()
    if (current === undefined) continue
    const next = selected
      .filter((edge) => direction === "descendants" ? edge.from === current : edge.to === current)
      .map((edge) => direction === "descendants" ? edge.to : edge.from)
    for (const id of next) {
      if (id !== start && !visited.has(id)) {
        visited.add(id)
        queue.push(id)
      }
    }
  }
  return [...visited]
}

export const comparatorProtocolTraceData = (target: string) =>
  loadedValidatedProtocol.pipe(
    Effect.flatMap(({ protocol }) => {
      const step = protocol.steps.find(({ id }) => id === target)
      if (step === undefined) {
        return Effect.fail(
          iceError("COMPARATOR_PROTOCOL_STEP_NOT_FOUND", `route step '${target}' was not found`, 2)
        )
      }
      const ancestors = reachable(target, protocol.edges, "ancestors")
      const descendants = reachable(target, protocol.edges, "descendants")
      const included = new Set([target, ...ancestors, ...descendants])
      return Effect.succeed({
        schema: "ice-comparator-protocol-trace/v1" as const,
        target,
        contract: {
          authority: protocol.authority,
          canonical_graph_unchanged: protocol.canonical_graph_unchanged,
          does_not_authorize_execution: protocol.does_not_authorize_execution,
          result_status: protocol.result_status
        },
        ancestors,
        descendants,
        independent_parallel_neighbors: protocol.edges
          .filter(({ from, to, relation }) =>
            relation === "INDEPENDENT_PARALLEL_TO" && (from === target || to === target)
          )
          .map(({ from, to }) => from === target ? to : from),
        steps: protocol.steps.filter(({ id }) => included.has(id)),
        edges: protocol.edges.filter(({ from, to }) => included.has(from) && included.has(to)),
        prerequisite_producers: prerequisiteProducers(step, protocol.steps),
        boundary: "Trace follows design dependencies only; independent-parallel edges do not create prerequisites."
      })
    })
  )

export const comparatorProtocolValidateCommand = (_json: boolean) =>
  comparatorProtocolValidateData.pipe(Effect.tap(printJson))

export const comparatorProtocolSummaryCommand = (_json: boolean) =>
  comparatorProtocolSummaryData.pipe(Effect.tap(printJson))

export const comparatorProtocolShowCommand = (target: string, _json: boolean) =>
  comparatorProtocolShowData(target).pipe(Effect.tap(printJson))

export const comparatorProtocolTraceCommand = (target: string, _json: boolean) =>
  comparatorProtocolTraceData(target).pipe(Effect.tap(printJson))
