import type {
  EvidencePolarity,
  KgBridge,
  ResearchEdge,
  ResearchGraph,
  ResearchNode
} from "./model.ts"

export type ValidationSeverity = "error" | "warning"

export interface ValidationIssue {
  readonly severity: ValidationSeverity
  readonly code: string
  readonly message: string
  readonly subject?: string
}

export interface ValidationReport {
  readonly graph_id: string
  readonly schema_version: string
  readonly valid: boolean
  readonly counts: {
    readonly nodes: number
    readonly edges: number
    readonly artifacts: number
    readonly policies: number
    readonly hash_bearing_nodes: number
    readonly verified_hashes: number
  }
  readonly errors: ReadonlyArray<ValidationIssue>
  readonly warnings: ReadonlyArray<ValidationIssue>
}

export interface OntologySummary {
  readonly graph_id: string
  readonly title: string
  readonly schema_version: string
  readonly updated_at_utc: string
  readonly node_count: number
  readonly edge_count: number
  readonly nodes_by_type: Readonly<Record<string, number>>
  readonly claims_by_epistemic_state: Readonly<Record<string, number>>
  readonly open_problem_count: number
  readonly artifact_count: number
  readonly kg_bridges_by_status: Readonly<Record<string, number>>
  readonly validation_warning_count: number
}

export interface NodeView {
  readonly node: ResearchNode
  readonly incoming: ReadonlyArray<ResearchEdge>
  readonly outgoing: ReadonlyArray<ResearchEdge>
  readonly kg_bridges: ReadonlyArray<KgBridge>
}

export interface TraceNode {
  readonly distance: number
  readonly node: ResearchNode
}

export interface TraceResult {
  readonly root: string
  readonly max_depth: number
  readonly nodes: ReadonlyArray<TraceNode>
  readonly edges: ReadonlyArray<ResearchEdge>
  readonly kg_bridges: ReadonlyArray<KgBridge>
}

const SHA256 = /^[0-9a-f]{64}$/

const makeIssue = (
  severity: ValidationSeverity,
  code: string,
  message: string,
  subject?: string
): ValidationIssue =>
  subject === undefined
    ? { severity, code, message }
    : { severity, code, message, subject }

const duplicateValues = (
  values: ReadonlyArray<string>
): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const duplicates = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) {
      duplicates.add(value)
    }
    seen.add(value)
  }
  return [...duplicates].sort()
}

const nodePrefix = (type: ResearchNode["type"]): string => {
  switch (type) {
    case "programme":
      return "programme:"
    case "phase":
      return "phase:"
    case "concept":
      return "concept:"
    case "claim":
      return "claim:"
    case "evidence":
      return "evidence:"
    case "scope":
      return "scope:"
    case "open_problem":
      return "open:"
    case "source":
      return "source:"
    case "artifact":
      return "artifact:"
    case "policy":
      return "policy:"
  }
}

export const isSafeArtifactPath = (value: string): boolean => {
  if (
    value.length === 0 ||
    value.includes("\0") ||
    value.includes("\\") ||
    value.startsWith("/") ||
    /^[A-Za-z]:/.test(value)
  ) {
    return false
  }
  const segments = value.split("/")
  return segments.every(
    (segment) => segment.length > 0 && segment !== "." && segment !== ".."
  )
}

const expectedPolarity = (
  node: ResearchNode
): EvidencePolarity | undefined => {
  if (node.type !== "claim") {
    return undefined
  }
  if (node.epistemic_state === "SUPPORTED") {
    return "SUPPORTS"
  }
  if (node.epistemic_state === "CONTRADICTED") {
    return "CONTRADICTS"
  }
  return undefined
}

export const validateGraphSemantics = (
  graph: ResearchGraph
): ReadonlyArray<ValidationIssue> => {
  const issues: Array<ValidationIssue> = []
  const nodesById = new Map(graph.nodes.map((node) => [node.id, node]))

  for (const id of duplicateValues(graph.nodes.map((node) => node.id))) {
    issues.push(
      makeIssue("error", "DUPLICATE_NODE_ID", `node id '${id}' is not unique`, id)
    )
  }
  for (const id of duplicateValues(graph.edges.map((edge) => edge.id))) {
    issues.push(
      makeIssue("error", "DUPLICATE_EDGE_ID", `edge id '${id}' is not unique`, id)
    )
  }
  for (const id of duplicateValues(graph.reading_paths.map((path) => path.id))) {
    issues.push(
      makeIssue(
        "error",
        "DUPLICATE_READING_PATH_ID",
        `reading-path id '${id}' is not unique`,
        id
      )
    )
  }

  const claims = graph.nodes.filter((node) => node.type === "claim")
  for (const id of duplicateValues(claims.map((claim) => claim.claim_id))) {
    issues.push(
      makeIssue("error", "DUPLICATE_CLAIM_ID", `claim_id '${id}' is not unique`, id)
    )
  }

  const checkIds = graph.nodes.flatMap((node) =>
    node.type === "evidence" ? (node.check_ids ?? []) : []
  )
  for (const id of duplicateValues(checkIds)) {
    issues.push(
      makeIssue("error", "DUPLICATE_CHECK_ID", `check id '${id}' is not unique`, id)
    )
  }

  for (const node of graph.nodes) {
    if (!node.id.startsWith(nodePrefix(node.type))) {
      issues.push(
        makeIssue(
          "error",
          "NODE_ID_PREFIX_MISMATCH",
          `node type '${node.type}' requires prefix '${nodePrefix(node.type)}'`,
          node.id
        )
      )
    }
    if (!(node.type in graph.node_type_legend)) {
      issues.push(
        makeIssue(
          "error",
          "NODE_TYPE_LEGEND_MISSING",
          `node type '${node.type}' is absent from node_type_legend`,
          node.id
        )
      )
    }
    if (node.type === "claim" && node.id !== `claim:${node.claim_id}`) {
      issues.push(
        makeIssue(
          "error",
          "CLAIM_ID_MISMATCH",
          `claim node id must equal 'claim:' plus claim_id`,
          node.id
        )
      )
    }
  }

  const matchingEvidenceClaims = new Set<string>()
  for (const edge of graph.edges) {
    const from = nodesById.get(edge.from)
    const to = nodesById.get(edge.to)
    if (from === undefined) {
      issues.push(
        makeIssue(
          "error",
          "EDGE_FROM_NOT_FOUND",
          `edge source '${edge.from}' does not exist`,
          edge.id
        )
      )
    }
    if (to === undefined) {
      issues.push(
        makeIssue(
          "error",
          "EDGE_TO_NOT_FOUND",
          `edge target '${edge.to}' does not exist`,
          edge.id
        )
      )
    }
    if (!(edge.relation in graph.relation_legend)) {
      issues.push(
        makeIssue(
          "error",
          "RELATION_LEGEND_MISSING",
          `relation '${edge.relation}' is absent from relation_legend`,
          edge.id
        )
      )
    }

    if (edge.relation === "HAS_EVIDENCE") {
      if (edge.polarity === undefined) {
        issues.push(
          makeIssue(
            "error",
            "EVIDENCE_POLARITY_MISSING",
            "HAS_EVIDENCE requires SUPPORTS or CONTRADICTS polarity",
            edge.id
          )
        )
      }
      if (from !== undefined && from.type !== "claim") {
        issues.push(
          makeIssue(
            "error",
            "EVIDENCE_SOURCE_NOT_CLAIM",
            "HAS_EVIDENCE source must be a claim node",
            edge.id
          )
        )
      }
      if (to !== undefined && to.type !== "evidence") {
        issues.push(
          makeIssue(
            "error",
            "EVIDENCE_TARGET_NOT_EVIDENCE",
            "HAS_EVIDENCE target must be an evidence node",
            edge.id
          )
        )
      }
      if (from !== undefined && from.type === "claim" && edge.polarity !== undefined) {
        const expected = expectedPolarity(from)
        if (expected !== undefined && edge.polarity !== expected) {
          issues.push(
            makeIssue(
              "error",
              "EVIDENCE_POLARITY_STATE_MISMATCH",
              `${from.epistemic_state} claim requires ${expected} evidence polarity`,
              edge.id
            )
          )
        } else if (expected === edge.polarity) {
          matchingEvidenceClaims.add(from.id)
        }
      }
    } else if (edge.polarity !== undefined) {
      issues.push(
        makeIssue(
          "error",
          "POLARITY_ON_NON_EVIDENCE_EDGE",
          `relation '${edge.relation}' must not carry evidence polarity`,
          edge.id
        )
      )
    }
  }

  for (const claim of claims) {
    if (
      expectedPolarity(claim) !== undefined &&
      !matchingEvidenceClaims.has(claim.id)
    ) {
      issues.push(
        makeIssue(
          "error",
          "CLAIM_MATCHING_EVIDENCE_MISSING",
          `${claim.epistemic_state} claim has no matching HAS_EVIDENCE edge`,
          claim.id
        )
      )
    }
  }

  for (const answer of graph.quick_answers) {
    for (const id of answer.claim_ids) {
      const node = nodesById.get(id)
      if (node === undefined || node.type !== "claim") {
        issues.push(
          makeIssue(
            "error",
            "QUICK_ANSWER_CLAIM_NOT_FOUND",
            `quick answer references missing non-claim '${id}'`,
            id
          )
        )
      }
    }
  }

  for (const readingPath of graph.reading_paths) {
    for (const id of readingPath.nodes) {
      if (!nodesById.has(id)) {
        issues.push(
          makeIssue(
            "error",
            "READING_PATH_NODE_NOT_FOUND",
            `reading path references missing node '${id}'`,
            readingPath.id
          )
        )
      }
    }
  }

  for (const bridge of graph.kg_bridges) {
    if (!nodesById.has(bridge.local_node_id)) {
      issues.push(
        makeIssue(
          "error",
          "BRIDGE_LOCAL_NODE_NOT_FOUND",
          `external bridge references missing local node '${bridge.local_node_id}'`,
          bridge.local_node_id
        )
      )
    }
    if (bridge.status === "UNRESOLVED") {
      if (bridge.external_uid !== null || bridge.relation !== null) {
        issues.push(
          makeIssue(
            "error",
            "UNRESOLVED_BRIDGE_HAS_RESOLUTION",
            "UNRESOLVED bridge must keep external_uid and relation null",
            bridge.local_node_id
          )
        )
      }
      issues.push(
        makeIssue(
          "warning",
          "EXTERNAL_BRIDGE_UNRESOLVED",
          `${bridge.system} bridge has no resolved external UID`,
          bridge.local_node_id
        )
      )
    } else if (bridge.external_uid === null || bridge.relation === null) {
      issues.push(
        makeIssue(
          "error",
          "RESOLVED_BRIDGE_TARGET_MISSING",
          "RESOLVED bridge requires external_uid and relation",
          bridge.local_node_id
        )
      )
    }
  }

  const artifacts = graph.nodes.filter((node) => node.type === "artifact")
  const hashBearingNodes = graph.nodes.filter(
    (node) => node.type === "artifact" || node.type === "policy"
  )
  for (const path of duplicateValues(artifacts.map((artifact) => artifact.path))) {
    issues.push(
      makeIssue(
        "error",
        "DUPLICATE_ARTIFACT_PATH",
        `artifact path '${path}' is not unique`,
        path
      )
    )
  }
  for (const node of hashBearingNodes) {
    if (!isSafeArtifactPath(node.path)) {
      issues.push(
        makeIssue(
          "error",
          "HASHED_PATH_UNSAFE",
          `path '${node.path}' is not a safe repository-relative path`,
          node.id
        )
      )
    }
    if (!SHA256.test(node.sha256)) {
      issues.push(
        makeIssue(
          "error",
          "HASH_FORMAT_INVALID",
          "sha256 must be 64 lowercase hexadecimal characters",
          node.id
        )
      )
    }
  }

  return issues
}

const issueOrder = (left: ValidationIssue, right: ValidationIssue): number =>
  `${left.code}\0${left.subject ?? ""}\0${left.message}`.localeCompare(
    `${right.code}\0${right.subject ?? ""}\0${right.message}`
  )

export const makeValidationReport = (
  graph: ResearchGraph,
  issues: ReadonlyArray<ValidationIssue>,
  verifiedHashes = 0
): ValidationReport => {
  const errors = issues
    .filter((issue) => issue.severity === "error")
    .sort(issueOrder)
  const warnings = issues
    .filter((issue) => issue.severity === "warning")
    .sort(issueOrder)
  return {
    graph_id: graph.graph_id,
    schema_version: graph.schema_version,
    valid: errors.length === 0,
    counts: {
      nodes: graph.nodes.length,
      edges: graph.edges.length,
      artifacts: graph.nodes.filter((node) => node.type === "artifact").length,
      policies: graph.nodes.filter((node) => node.type === "policy").length,
      hash_bearing_nodes: graph.nodes.filter(
        (node) => node.type === "artifact" || node.type === "policy"
      ).length,
      verified_hashes: verifiedHashes
    },
    errors,
    warnings
  }
}

const countBy = (
  values: ReadonlyArray<string>
): Readonly<Record<string, number>> => {
  const counts: Record<string, number> = {}
  for (const value of values) {
    counts[value] = (counts[value] ?? 0) + 1
  }
  return Object.fromEntries(
    Object.entries(counts).sort(([left], [right]) => left.localeCompare(right))
  )
}

export const summarizeGraph = (
  graph: ResearchGraph,
  validation: ValidationReport
): OntologySummary => ({
  graph_id: graph.graph_id,
  title: graph.title,
  schema_version: graph.schema_version,
  updated_at_utc: graph.updated_at_utc,
  node_count: graph.nodes.length,
  edge_count: graph.edges.length,
  nodes_by_type: countBy(graph.nodes.map((node) => node.type)),
  claims_by_epistemic_state: countBy(
    graph.nodes.flatMap((node) =>
      node.type === "claim" ? [node.epistemic_state] : []
    )
  ),
  open_problem_count: graph.nodes.filter((node) => node.type === "open_problem")
    .length,
  artifact_count: graph.nodes.filter((node) => node.type === "artifact").length,
  kg_bridges_by_status: countBy(graph.kg_bridges.map((bridge) => bridge.status)),
  validation_warning_count: validation.warnings.length
})

export const resolveNode = (
  graph: ResearchGraph,
  id: string
): ResearchNode | undefined =>
  graph.nodes.find((node) => node.id === id) ??
  graph.nodes.find((node) => node.type === "claim" && node.claim_id === id)

export const showNode = (
  graph: ResearchGraph,
  node: ResearchNode
): NodeView => ({
  node,
  incoming: graph.edges
    .filter((edge) => edge.to === node.id)
    .sort((left, right) => left.id.localeCompare(right.id)),
  outgoing: graph.edges
    .filter((edge) => edge.from === node.id)
    .sort((left, right) => left.id.localeCompare(right.id)),
  kg_bridges: graph.kg_bridges
    .filter((bridge) => bridge.local_node_id === node.id)
    .sort((left, right) =>
      `${left.system}\0${left.external_uid ?? ""}`.localeCompare(
        `${right.system}\0${right.external_uid ?? ""}`
      )
    )
})

export const traceGraph = (
  graph: ResearchGraph,
  root: ResearchNode,
  maxDepth: number
): TraceResult => {
  const nodesById = new Map(graph.nodes.map((node) => [node.id, node]))
  const distances = new Map<string, number>([[root.id, 0]])

  for (let distance = 0; distance < maxDepth; distance += 1) {
    const frontier = new Set(
      [...distances.entries()]
        .filter(([, observed]) => observed === distance)
        .map(([id]) => id)
    )
    for (const edge of graph.edges) {
      const adjacent = frontier.has(edge.from)
        ? edge.to
        : frontier.has(edge.to)
          ? edge.from
          : undefined
      if (adjacent !== undefined && !distances.has(adjacent) && nodesById.has(adjacent)) {
        distances.set(adjacent, distance + 1)
      }
    }
  }

  const nodes = [...distances.entries()]
    .flatMap(([id, distance]) => {
      const node = nodesById.get(id)
      return node === undefined ? [] : [{ distance, node }]
    })
    .sort(
      (left, right) =>
        left.distance - right.distance || left.node.id.localeCompare(right.node.id)
    )
  const included = new Set(nodes.map(({ node }) => node.id))
  const edges = graph.edges
    .filter((edge) => included.has(edge.from) && included.has(edge.to))
    .sort((left, right) => left.id.localeCompare(right.id))
  const kgBridges = graph.kg_bridges
    .filter((bridge) => included.has(bridge.local_node_id))
    .sort((left, right) =>
      `${left.local_node_id}\0${left.system}\0${left.external_uid ?? ""}`.localeCompare(
        `${right.local_node_id}\0${right.system}\0${right.external_uid ?? ""}`
      )
    )

  return {
    root: root.id,
    max_depth: maxDepth,
    nodes,
    edges,
    kg_bridges: kgBridges
  }
}
