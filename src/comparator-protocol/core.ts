import type { CollectionGraph } from "../ontology/collection-core.ts"
import { validateScientificIntuitionFlowV2 } from "../intuition/core.ts"
import type { ScientificIntuitionFlowV2 } from "../intuition/model.ts"
import type {
  ComparatorEdge,
  ComparatorLane,
  ComparatorStep,
  IceComparatorProtocol
} from "./model.ts"

export interface ComparatorProtocolValidationIssue {
  readonly code: string
  readonly message: string
  readonly subject?: string
}

export interface ComparatorProtocolValidationReport {
  readonly schema: "ice-comparator-protocol-validation/v1"
  readonly valid: boolean
  readonly authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly result_status: "DESIGN_ONLY"
  readonly counts: {
    readonly source_pins: number
    readonly tools: number
    readonly models: number
    readonly consumers: number
    readonly steps: number
    readonly edges: number
    readonly planned_inputs: number
    readonly planned_outputs: number
  }
  readonly errors: ReadonlyArray<ComparatorProtocolValidationIssue>
  readonly boundaries: ReadonlyArray<string>
}

const requiredChoiceDimensions = new Set([
  "gauge",
  "basis",
  "field_parametrization",
  "cutoff",
  "boundary_domain"
])
const geometryTopic = "topic:geometry-energy-unification"
const foldedTopic = "topic:cpt-folded-susy-synthesis"
const foldedContextNode = "open:gate4-spinorial-charge-domain-constraint-closure"

const duplicates = (values: ReadonlyArray<string>): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const repeated = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) repeated.add(value)
    seen.add(value)
  }
  return [...repeated].sort()
}

const issue = (
  errors: ComparatorProtocolValidationIssue[],
  code: string,
  message: string,
  subject?: string
): void => {
  errors.push(subject === undefined ? { code, message } : { code, message, subject })
}

const directedEdges = (edges: ReadonlyArray<ComparatorEdge>): ReadonlyArray<ComparatorEdge> =>
  edges.filter(({ relation }) => relation !== "INDEPENDENT_PARALLEL_TO")

const pathExists = (
  from: string,
  to: string,
  edges: ReadonlyArray<ComparatorEdge>
): boolean => {
  const adjacency = new Map<string, string[]>()
  for (const edge of directedEdges(edges)) {
    const values = adjacency.get(edge.from) ?? []
    values.push(edge.to)
    adjacency.set(edge.from, values)
  }
  const queue = [from]
  const visited = new Set<string>()
  while (queue.length > 0) {
    const current = queue.shift()
    if (current === undefined || visited.has(current)) continue
    if (current === to) return true
    visited.add(current)
    queue.push(...(adjacency.get(current) ?? []))
  }
  return false
}

const cyclicNodes = (
  steps: ReadonlyArray<ComparatorStep>,
  edges: ReadonlyArray<ComparatorEdge>
): ReadonlyArray<string> => {
  const adjacency = new Map(steps.map(({ id }) => [id, [] as string[]]))
  const indegree = new Map(steps.map(({ id }) => [id, 0]))
  for (const edge of directedEdges(edges)) {
    if (!adjacency.has(edge.from) || !indegree.has(edge.to)) continue
    adjacency.get(edge.from)?.push(edge.to)
    indegree.set(edge.to, (indegree.get(edge.to) ?? 0) + 1)
  }
  const queue = [...indegree.entries()]
    .filter(([, degree]) => degree === 0)
    .map(([id]) => id)
    .sort()
  const visited = new Set<string>()
  while (queue.length > 0) {
    const current = queue.shift()
    if (current === undefined) continue
    visited.add(current)
    for (const next of adjacency.get(current) ?? []) {
      const degree = (indegree.get(next) ?? 0) - 1
      indegree.set(next, degree)
      if (degree === 0) queue.push(next)
    }
  }
  return steps.map(({ id }) => id).filter((id) => !visited.has(id)).sort()
}

const checkDuplicateRefs = (
  errors: ComparatorProtocolValidationIssue[],
  subject: string,
  field: string,
  refs: ReadonlyArray<string>
): void => {
  for (const ref of duplicates(refs)) {
    issue(errors, "DUPLICATE_REFERENCE", `${field} repeats '${ref}'`, subject)
  }
}

export const validateIceComparatorProtocol = (
  protocol: IceComparatorProtocol,
  intuition: ScientificIntuitionFlowV2,
  graphs: ReadonlyArray<CollectionGraph>
): ComparatorProtocolValidationReport => {
  const errors: ComparatorProtocolValidationIssue[] = []
  const intuitionReport = validateScientificIntuitionFlowV2(intuition, graphs)
  for (const intuitionIssue of intuitionReport.errors) {
    issue(
      errors,
      `INTUITION_${intuitionIssue.code}`,
      `referenced intuition sidecar is invalid: ${intuitionIssue.message}`,
      intuitionIssue.subject
    )
  }
  const entityGroups: ReadonlyArray<readonly [string, ReadonlyArray<string>]> = [
    ["source pin", protocol.source_pins.map(({ id }) => id)],
    ["tool", protocol.tools.map(({ id }) => id)],
    ["model", protocol.models.map(({ id }) => id)],
    ["consumer", protocol.consumers.map(({ id }) => id)],
    ["step", protocol.steps.map(({ id }) => id)],
    ["edge", protocol.edges.map(({ id }) => id)]
  ]
  for (const [kind, ids] of entityGroups) {
    for (const id of duplicates(ids)) {
      issue(errors, "DUPLICATE_ENTITY_ID", `${kind} id '${id}' is not unique`, id)
    }
  }

  const plannedInputs = protocol.steps.flatMap(({ inputs }) => inputs)
  const plannedOutputs = protocol.steps.flatMap(({ outputs }) => outputs)
  for (const id of duplicates(plannedInputs.map(({ id }) => id))) {
    issue(errors, "DUPLICATE_INPUT_ID", `planned input id '${id}' is not unique`, id)
  }
  for (const id of duplicates(plannedOutputs.map(({ id }) => id))) {
    issue(errors, "DUPLICATE_OUTPUT_ID", `planned output id '${id}' has multiple producers`, id)
  }
  const allEntityIds = entityGroups.flatMap(([, ids]) => ids)
  for (const id of duplicates(allEntityIds)) {
    issue(errors, "CROSS_KIND_ID_COLLISION", `entity id '${id}' is ambiguous across kinds`, id)
  }

  const sourceIds = new Set(protocol.source_pins.map(({ id }) => id))
  const toolIds = new Set(protocol.tools.map(({ id }) => id))
  const modelIds = new Set(protocol.models.map(({ id }) => id))
  const consumerIds = new Set(protocol.consumers.map(({ id }) => id))
  const stepById = new Map(protocol.steps.map((step) => [step.id, step]))
  const topicIds = new Set(intuition.topics.map(({ id }) => id))
  const graphByKey = new Map(graphs.map((graph) => [graph.descriptor.key, graph]))
  const outputProducer = new Map<string, string>()
  for (const step of protocol.steps) {
    for (const output of step.outputs) {
      if (!outputProducer.has(output.id)) outputProducer.set(output.id, step.id)
    }
  }

  for (const tool of protocol.tools) {
    if (!sourceIds.has(tool.paper_source_ref)) {
      issue(errors, "TOOL_PAPER_SOURCE_NOT_FOUND", `tool paper source '${tool.paper_source_ref}' is missing`, tool.id)
    }
  }
  for (const model of protocol.models) {
    checkDuplicateRefs(errors, model.id, "source_refs", model.source_refs)
    for (const ref of model.source_refs) {
      if (!sourceIds.has(ref)) {
        issue(errors, "MODEL_SOURCE_NOT_FOUND", `model source '${ref}' is missing`, model.id)
      }
    }
  }

  for (const step of protocol.steps) {
    checkDuplicateRefs(errors, step.id, "topic_refs", step.topic_refs)
    checkDuplicateRefs(errors, step.id, "model_refs", step.model_refs)
    checkDuplicateRefs(errors, step.id, "source_refs", step.source_refs)
    checkDuplicateRefs(errors, step.id, "tool_refs", step.tool_refs)
    checkDuplicateRefs(errors, step.id, "prerequisite_outputs", step.prerequisite_outputs)
    checkDuplicateRefs(errors, step.id, "choice_dimensions", step.choice_dimensions)
    checkDuplicateRefs(errors, step.id, "consumer_refs", step.consumer_refs)
    for (const ref of step.topic_refs) {
      if (!topicIds.has(ref)) {
        issue(errors, "TOPIC_REF_NOT_FOUND", `intuition topic '${ref}' is missing`, step.id)
      }
    }
    for (const ref of step.model_refs) {
      if (!modelIds.has(ref)) issue(errors, "MODEL_REF_NOT_FOUND", `model '${ref}' is missing`, step.id)
    }
    for (const ref of step.source_refs) {
      if (!sourceIds.has(ref)) issue(errors, "SOURCE_REF_NOT_FOUND", `source '${ref}' is missing`, step.id)
    }
    for (const ref of step.tool_refs) {
      if (!toolIds.has(ref)) issue(errors, "TOOL_REF_NOT_FOUND", `tool '${ref}' is missing`, step.id)
    }
    for (const ref of step.consumer_refs) {
      if (!consumerIds.has(ref)) issue(errors, "CONSUMER_REF_NOT_FOUND", `consumer '${ref}' is missing`, step.id)
    }
    for (const ref of step.prerequisite_outputs) {
      const producer = outputProducer.get(ref)
      if (producer === undefined) {
        issue(errors, "PREREQUISITE_OUTPUT_NOT_FOUND", `prerequisite output '${ref}' has no producer`, step.id)
      } else if (!protocol.edges.some(({ from, relation, to }) =>
        from === producer && relation === "PREREQUISITE_FOR" && to === step.id
      )) {
        issue(errors, "PREREQUISITE_EDGE_NOT_FOUND", `producer '${producer}' lacks a PREREQUISITE_FOR edge to the consumer of '${ref}'`, step.id)
      }
    }

    const expectedTopic = step.lane === "GEOMETRY_COMPARATOR" ? geometryTopic : foldedTopic
    if (step.topic_refs.length !== 1 || step.topic_refs[0] !== expectedTopic) {
      issue(errors, "LANE_TOPIC_MISMATCH", `${step.lane} must reference only '${expectedTopic}'`, step.id)
    }
    if (step.lane === "GEOMETRY_COMPARATOR" && step.context_refs.length !== 0) {
      issue(errors, "GEOMETRY_CANONICAL_CONTEXT_FORBIDDEN", "geometry steps cannot target canonical CPT nodes", step.id)
    }
    if (step.lane === "FOLDED_SUSY_CLASSIFICATION") {
      if (step.kind !== "CLASSIFICATION") {
        issue(errors, "FOLDED_LANE_KIND_INVALID", "folded-SUSY lane is classification-only", step.id)
      }
      if (
        step.context_refs.length !== 1 ||
        step.context_refs[0]?.graph !== "cpt" ||
        step.context_refs[0]?.node !== foldedContextNode
      ) {
        issue(errors, "FOLDED_CONTEXT_INVALID", `folded classification may context-link only cpt::${foldedContextNode}`, step.id)
      }
    }
    for (const context of step.context_refs) {
      const graph = graphByKey.get(context.graph)
      const node = graph?.graph.nodes.find(({ id }) => id === context.node)
      if (graph === undefined) {
        issue(errors, "CONTEXT_GRAPH_NOT_FOUND", `context graph '${context.graph}' is missing`, step.id)
      } else if (node === undefined) {
        issue(errors, "CONTEXT_NODE_NOT_FOUND", `context node '${context.node}' is missing`, step.id)
      } else if (node.type !== "open_problem") {
        issue(errors, "CONTEXT_NODE_NOT_OPEN_PROBLEM", "context must identify a canonical open_problem", step.id)
      }
    }

    if (step.kind === "CROSS_DOMAIN_TEST") {
      const domains = new Set(
        step.consumer_refs
          .map((ref) => protocol.consumers.find(({ id }) => id === ref)?.domain)
          .filter((domain): domain is NonNullable<typeof domain> => domain !== undefined)
      )
      if (domains.size !== 3) {
        issue(errors, "CROSS_DOMAIN_COVERAGE_INCOMPLETE", "cross-domain test must cover background, scalar, and tensor consumers", step.id)
      }
      if (new Set(step.tool_refs).size < 2) {
        issue(errors, "INDEPENDENT_SOLVER_COUNT_TOO_SMALL", "cross-domain test requires two pinned solver implementations", step.id)
      }
      for (const dimension of requiredChoiceDimensions) {
        if (!step.choice_dimensions.includes(dimension)) {
          issue(errors, "CHOICE_DIMENSION_MISSING", `cross-domain test omits '${dimension}'`, step.id)
        }
      }
    }
  }

  for (const edge of protocol.edges) {
    const from = stepById.get(edge.from)
    const to = stepById.get(edge.to)
    if (from === undefined) issue(errors, "EDGE_FROM_NOT_FOUND", `edge source '${edge.from}' is missing`, edge.id)
    if (to === undefined) issue(errors, "EDGE_TO_NOT_FOUND", `edge target '${edge.to}' is missing`, edge.id)
    if (edge.from === edge.to) issue(errors, "EDGE_SELF_REFERENCE", "edge endpoints must be distinct", edge.id)
    if (from !== undefined && to !== undefined) {
      if (edge.relation === "INDEPENDENT_PARALLEL_TO") {
        if (from.lane === to.lane) {
          issue(errors, "PARALLEL_EDGE_SAME_LANE", "independent-parallel endpoints must be in different lanes", edge.id)
        }
      } else if (from.lane !== to.lane) {
        issue(errors, "CROSS_LANE_DEPENDENCY_FORBIDDEN", "dependency-like edges cannot cross lanes", edge.id)
      }
      if (edge.relation === "CALIBRATES" && from.kind !== "CALIBRATION") {
        issue(errors, "CALIBRATION_EDGE_SOURCE_INVALID", "CALIBRATES must originate at a calibration step", edge.id)
      }
    }
  }
  for (const triple of duplicates(protocol.edges.map(({ from, relation, to }) => `${from}|${relation}|${to}`))) {
    issue(errors, "DUPLICATE_EDGE_TRIPLE", `edge triple '${triple}' is repeated`, triple)
  }
  const cycles = cyclicNodes(protocol.steps, protocol.edges)
  if (cycles.length > 0) {
    issue(errors, "DIRECTED_ROUTE_CYCLE", `directed route contains a cycle involving ${cycles.join(", ")}`)
  }

  const strategy = protocol.selected_strategy
  const calibration = stepById.get(strategy.calibration_step)
  const crossDomain = stepById.get(strategy.cross_domain_step)
  const admission = stepById.get(strategy.ice_admission_step)
  const parallel = stepById.get(strategy.parallel_classification_step)
  const comparator = protocol.models.find(({ id }) => id === strategy.first_comparator_model)
  if (calibration?.kind !== "CALIBRATION" || calibration.lane !== "GEOMETRY_COMPARATOR") {
    issue(errors, "SELECTED_CALIBRATION_INVALID", "selected calibration_step must identify a geometry calibration")
  }
  if (comparator?.role !== "CANDIDATE_MODEL") {
    issue(errors, "SELECTED_COMPARATOR_INVALID", "selected first_comparator_model must identify a candidate model")
  }
  if (crossDomain?.kind !== "CROSS_DOMAIN_TEST" || crossDomain.lane !== "GEOMETRY_COMPARATOR") {
    issue(errors, "SELECTED_CROSS_DOMAIN_INVALID", "selected cross_domain_step must identify a geometry cross-domain test")
  } else if (!crossDomain.model_refs.includes(strategy.first_comparator_model)) {
    issue(errors, "SELECTED_COMPARATOR_NOT_USED", "selected cross-domain step does not reference the selected comparator", crossDomain.id)
  }
  if (admission?.kind !== "ADMISSION_DECISION" || admission.lane !== "GEOMETRY_COMPARATOR") {
    issue(errors, "SELECTED_ADMISSION_INVALID", "selected ice_admission_step must identify a geometry admission decision")
  }
  if (parallel?.kind !== "CLASSIFICATION" || parallel.lane !== "FOLDED_SUSY_CLASSIFICATION") {
    issue(errors, "SELECTED_PARALLEL_INVALID", "selected parallel_classification_step must identify the folded-SUSY classification lane")
  }
  if (
    calibration !== undefined && crossDomain !== undefined &&
    !pathExists(calibration.id, crossDomain.id, protocol.edges)
  ) {
    issue(errors, "CALIBRATION_PATH_MISSING", "selected calibration does not reach the cross-domain test")
  }
  if (
    crossDomain !== undefined && admission !== undefined &&
    !pathExists(crossDomain.id, admission.id, protocol.edges)
  ) {
    issue(errors, "ADMISSION_PATH_MISSING", "selected cross-domain test does not reach ICE admission")
  }
  if (
    parallel !== undefined && admission !== undefined &&
    (pathExists(parallel.id, admission.id, protocol.edges) || pathExists(admission.id, parallel.id, protocol.edges))
  ) {
    issue(errors, "PARALLEL_LANE_DEPENDENCY_FORBIDDEN", "folded-SUSY classification must remain independent of ICE admission")
  }

  return {
    schema: "ice-comparator-protocol-validation/v1",
    valid: errors.length === 0,
    authority: protocol.authority,
    canonical_graph_unchanged: protocol.canonical_graph_unchanged,
    does_not_authorize_execution: protocol.does_not_authorize_execution,
    result_status: protocol.result_status,
    counts: {
      source_pins: protocol.source_pins.length,
      tools: protocol.tools.length,
      models: protocol.models.length,
      consumers: protocol.consumers.length,
      steps: protocol.steps.length,
      edges: protocol.edges.length,
      planned_inputs: plannedInputs.length,
      planned_outputs: plannedOutputs.length
    },
    errors,
    boundaries: protocol.boundaries
  }
}

export const topologicalStepIds = (
  steps: ReadonlyArray<ComparatorStep>,
  edges: ReadonlyArray<ComparatorEdge>,
  lane?: ComparatorLane
): ReadonlyArray<string> => {
  const selected = lane === undefined ? steps : steps.filter((step) => step.lane === lane)
  const ids = new Set(selected.map(({ id }) => id))
  const adjacency = new Map(selected.map(({ id }) => [id, [] as string[]]))
  const indegree = new Map(selected.map(({ id }) => [id, 0]))
  for (const edge of directedEdges(edges)) {
    if (!ids.has(edge.from) || !ids.has(edge.to)) continue
    adjacency.get(edge.from)?.push(edge.to)
    indegree.set(edge.to, (indegree.get(edge.to) ?? 0) + 1)
  }
  const queue = selected.filter(({ id }) => indegree.get(id) === 0).map(({ id }) => id)
  const ordered: string[] = []
  while (queue.length > 0) {
    const current = queue.shift()
    if (current === undefined) continue
    ordered.push(current)
    for (const next of adjacency.get(current) ?? []) {
      const degree = (indegree.get(next) ?? 0) - 1
      indegree.set(next, degree)
      if (degree === 0) queue.push(next)
    }
  }
  return ordered
}
