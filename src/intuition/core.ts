import type { CollectionGraph } from "../ontology/collection-core.ts"
import type { ScientificIntuitionFlow } from "./model.ts"

export interface IntuitionValidationIssue {
  readonly code: string
  readonly message: string
  readonly subject?: string
}

export interface IntuitionValidationReport {
  readonly schema: "scientific-intuition-flow-validation/v1"
  readonly valid: boolean
  readonly authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly counts: {
    readonly standards_alignment: number
    readonly sources: number
    readonly signals: number
    readonly candidates: number
  }
  readonly errors: ReadonlyArray<IntuitionValidationIssue>
  readonly boundaries: ReadonlyArray<string>
}

const duplicateIds = (values: ReadonlyArray<string>): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const duplicates = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) duplicates.add(value)
    seen.add(value)
  }
  return [...duplicates].sort()
}

export const validateScientificIntuitionFlow = (
  flow: ScientificIntuitionFlow,
  graphs: ReadonlyArray<CollectionGraph>
): IntuitionValidationReport => {
  const errors: IntuitionValidationIssue[] = []
  for (const id of duplicateIds(flow.standards_alignment.map(({ id }) => id))) {
    errors.push({
      code: "DUPLICATE_STANDARD_ID",
      message: `standard id '${id}' is not unique`,
      subject: id
    })
  }
  for (const id of duplicateIds(flow.sources.map(({ id }) => id))) {
    errors.push({
      code: "DUPLICATE_SOURCE_ID",
      message: `source id '${id}' is not unique`,
      subject: id
    })
  }
  for (const id of duplicateIds(flow.signals.map(({ id }) => id))) {
    errors.push({
      code: "DUPLICATE_SIGNAL_ID",
      message: `signal id '${id}' is not unique`,
      subject: id
    })
  }
  const sourceIds = new Set(flow.sources.map(({ id }) => id))
  const graphByKey = new Map(graphs.map(({ descriptor, graph }) => [descriptor.key, graph]))
  for (const source of flow.sources) {
    if (source.canonical_source === undefined) continue
    const graph = graphByKey.get(source.canonical_source.graph)
    const node = graph?.nodes.find(({ id }) => id === source.canonical_source?.node)
    if (graph === undefined) {
      errors.push({
        code: "CANONICAL_SOURCE_GRAPH_NOT_FOUND",
        message: `source graph '${source.canonical_source.graph}' is not canonical`,
        subject: source.id
      })
    } else if (node === undefined) {
      errors.push({
        code: "CANONICAL_SOURCE_NODE_NOT_FOUND",
        message: `source node '${source.canonical_source.node}' is not canonical`,
        subject: source.id
      })
    } else if (node.type !== "source") {
      errors.push({
        code: "CANONICAL_SOURCE_NODE_NOT_SOURCE",
        message: "canonical_source must identify a canonical source node",
        subject: source.id
      })
    } else if (node.uri !== source.uri) {
      errors.push({
        code: "CANONICAL_SOURCE_URI_MISMATCH",
        message: `sidecar URI does not match canonical source '${source.canonical_source.node}'`,
        subject: source.id
      })
    }
  }
  for (const signal of flow.signals) {
    for (const sourceId of duplicateIds(signal.source_refs)) {
      errors.push({
        code: "DUPLICATE_SOURCE_REF",
        message: `signal repeats source '${sourceId}'`,
        subject: signal.id
      })
    }
    for (const sourceId of signal.source_refs) {
      if (!sourceIds.has(sourceId)) {
        errors.push({
          code: "SOURCE_REF_NOT_FOUND",
          message: `signal references missing source '${sourceId}'`,
          subject: signal.id
        })
      }
    }
    const graph = graphByKey.get(signal.target.graph)
    const target = graph?.nodes.find(({ id }) => id === signal.target.node)
    if (graph === undefined) {
      errors.push({
        code: "TARGET_GRAPH_NOT_FOUND",
        message: `target graph '${signal.target.graph}' is not canonical`,
        subject: signal.id
      })
    } else if (target === undefined) {
      errors.push({
        code: "TARGET_NODE_NOT_FOUND",
        message: `target node '${signal.target.node}' is not canonical`,
        subject: signal.id
      })
    } else if (target.type !== "open_problem") {
      errors.push({
        code: "TARGET_NODE_NOT_OPEN_PROBLEM",
        message: "intuition targets must be canonical open_problem nodes",
        subject: signal.id
      })
    }
  }
  const candidates = flow.signals.filter(({ status }) => status === "CANDIDATE").length
  if (candidates < 2) {
    errors.push({
      code: "CANDIDATE_SIGNAL_COUNT_TOO_SMALL",
      message: "the sidecar requires at least two CANDIDATE signals"
    })
  }
  return {
    schema: "scientific-intuition-flow-validation/v1",
    valid: errors.length === 0,
    authority: flow.authority,
    canonical_graph_unchanged: flow.canonical_graph_unchanged,
    does_not_authorize_execution: flow.does_not_authorize_execution,
    counts: {
      standards_alignment: flow.standards_alignment.length,
      sources: flow.sources.length,
      signals: flow.signals.length,
      candidates
    },
    errors,
    boundaries: flow.boundaries
  }
}
