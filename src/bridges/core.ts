import { createHash } from "node:crypto"
import type { CollectionGraph } from "../ontology/collection-core.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"

export const BRIDGE_AUDIT_RELPATH =
  "research/benchmarks/ice-kg-bridge-resolution-audit.v1.json"

export type BridgeOutcome =
  | "NO_MATCH"
  | "ID_COLLISION"
  | "REGISTRY_UNAVAILABLE"

export interface BridgeRegistryLocator {
  readonly repository: string
  readonly commit: string
  readonly blob_oid: string
  readonly path: string
  readonly url: string
  readonly access_verification: "GH_API_AND_GIT_LS_REMOTE"
  readonly anchors: Readonly<Record<string, string>>
  readonly boundary: string
}

export interface BridgeAuditRule {
  readonly id: string
  readonly outcome: BridgeOutcome
  readonly graph: string
  readonly system: string
  readonly local_node_ids: ReadonlyArray<string>
  readonly registry_locator?: BridgeRegistryLocator
}

export interface BridgeResolutionAudit {
  readonly $schema: "../../ontology/schema/ice-kg-bridge-resolution-audit-v1.schema.json"
  readonly schema_version: "ice-kg-bridge-resolution-audit/v1"
  readonly audit_id: string
  readonly checked_at_utc: string
  readonly authority: "READ_ONLY_AUDIT_SIDECAR"
  readonly result_status: "ZERO_RESOLVED_MATCHES"
  readonly does_not_alter_canonical_bridge_status: true
  readonly scope: {
    readonly canonical_graphs: ReadonlyArray<string>
    readonly expected_unresolved_count: number
    readonly expected_keyset_sha256: string
    readonly keyset_encoding: string
  }
  readonly outcomes: Readonly<Record<BridgeOutcome, string>>
  readonly rules: ReadonlyArray<BridgeAuditRule>
  readonly default_outcome: "NO_MATCH"
  readonly non_claim: string
}

export interface AuditedBridge {
  readonly graph: string
  readonly local_node_id: string
  readonly system: string
  readonly lookup_key: string
  readonly outcome: BridgeOutcome
  readonly rule_id: string | null
  readonly registry_locator: {
    readonly repository: string
    readonly commit: string
    readonly blob_oid: string
    readonly path: string
    readonly url: string
    readonly anchor: string
    readonly boundary: string
  } | null
}

type RecordValue = Record<string, unknown>

const isRecord = (value: unknown): value is RecordValue =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const record = (value: unknown, label: string): RecordValue => {
  if (!isRecord(value)) throw new Error(`${label} must be an object`)
  return value
}

const exactKeys = (
  value: RecordValue,
  allowed: ReadonlyArray<string>,
  label: string
): void => {
  for (const key of Object.keys(value)) {
    if (!allowed.includes(key)) throw new Error(`${label} has unknown field '${key}'`)
  }
}

const text = (value: unknown, label: string): string => {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${label} must be a non-empty string`)
  }
  return value
}

const stringArray = (
  value: unknown,
  label: string
): ReadonlyArray<string> => {
  if (!Array.isArray(value) || value.length === 0) {
    throw new Error(`${label} must be a non-empty string array`)
  }
  const decoded = value.map((entry, index) =>
    text(entry, `${label}[${index}]`)
  )
  if (new Set(decoded).size !== decoded.length) {
    throw new Error(`${label} must not contain duplicates`)
  }
  return decoded
}

const decodeOutcome = (value: unknown, label: string): BridgeOutcome => {
  if (
    value !== "NO_MATCH" &&
    value !== "ID_COLLISION" &&
    value !== "REGISTRY_UNAVAILABLE"
  ) {
    throw new Error(`${label} must be a bridge outcome`)
  }
  return value
}

const validUtcDateTime = (value: string): boolean => {
  const match = /^(\d{4})-(\d{2})-(\d{2})T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.exec(value)
  if (match === null || Number.isNaN(Date.parse(value))) return false
  const parsed = new Date(value)
  return (
    parsed.getUTCFullYear() === Number(match[1]) &&
    parsed.getUTCMonth() + 1 === Number(match[2]) &&
    parsed.getUTCDate() === Number(match[3])
  )
}

const decodeLocator = (
  value: unknown,
  label: string
): BridgeRegistryLocator => {
  const item = record(value, label)
  exactKeys(
    item,
    [
      "repository",
      "commit",
      "blob_oid",
      "path",
      "url",
      "access_verification",
      "anchors",
      "boundary"
    ],
    label
  )
  const repository = text(item.repository, `${label}.repository`)
  const commit = text(item.commit, `${label}.commit`)
  const blobOid = text(item.blob_oid, `${label}.blob_oid`)
  const path = text(item.path, `${label}.path`)
  const url = text(item.url, `${label}.url`)
  if (repository !== "https://github.com/gj3447/symposium") {
    throw new Error(`${label}.repository is not the audited registry`)
  }
  if (!/^[0-9a-f]{40}$/.test(commit) || !/^[0-9a-f]{40}$/.test(blobOid)) {
    throw new Error(`${label} commit and blob_oid must be 40-character Git object IDs`)
  }
  if (!isSafeArtifactPath(path)) throw new Error(`${label}.path is unsafe`)
  if (
    url !== `${repository}/blob/${commit}/${path}` ||
    item.access_verification !== "GH_API_AND_GIT_LS_REMOTE"
  ) {
    throw new Error(`${label} URL or access verification does not match its pin`)
  }
  const anchors = record(item.anchors, `${label}.anchors`)
  const decodedAnchors: Record<string, string> = {}
  for (const [key, anchor] of Object.entries(anchors)) {
    if (
      !/^phase:p\d+$/.test(key) ||
      typeof anchor !== "string" ||
      !/^L\d+$/.test(anchor)
    ) {
      throw new Error(`${label}.anchors has an invalid phase/line locator`)
    }
    decodedAnchors[key] = anchor
  }
  if (Object.keys(decodedAnchors).length === 0) {
    throw new Error(`${label}.anchors must not be empty`)
  }
  return {
    repository,
    commit,
    blob_oid: blobOid,
    path,
    url,
    access_verification: "GH_API_AND_GIT_LS_REMOTE",
    anchors: decodedAnchors,
    boundary: text(item.boundary, `${label}.boundary`)
  }
}

const decodeRule = (value: unknown, index: number): BridgeAuditRule => {
  const label = `rules[${index}]`
  const item = record(value, label)
  exactKeys(
    item,
    ["id", "outcome", "graph", "system", "local_node_ids", "registry_locator"],
    label
  )
  const id = text(item.id, `${label}.id`)
  if (!/^rule:[a-z0-9-]+$/.test(id)) throw new Error(`${label}.id is invalid`)
  const outcome = decodeOutcome(item.outcome, `${label}.outcome`)
  const localNodeIds = stringArray(item.local_node_ids, `${label}.local_node_ids`)
  if (localNodeIds.some((nodeId) => !/^[a-z_]+:[A-Za-z0-9_.:-]+$/.test(nodeId))) {
    throw new Error(`${label}.local_node_ids contains an invalid local entity ID`)
  }
  const locator =
    item.registry_locator === undefined
      ? undefined
      : decodeLocator(item.registry_locator, `${label}.registry_locator`)
  if (outcome === "ID_COLLISION" && locator === undefined) {
    throw new Error(`${label} ID_COLLISION requires a pinned registry locator`)
  }
  if (outcome !== "ID_COLLISION" && locator !== undefined) {
    throw new Error(`${label} only ID_COLLISION may carry a registry locator`)
  }
  if (
    locator !== undefined &&
    JSON.stringify(Object.keys(locator.anchors).sort()) !==
      JSON.stringify([...localNodeIds].sort())
  ) {
    throw new Error(`${label} collision anchors must exactly match local_node_ids`)
  }
  return {
    id,
    outcome,
    graph: text(item.graph, `${label}.graph`),
    system: text(item.system, `${label}.system`),
    local_node_ids: localNodeIds,
    ...(locator === undefined ? {} : { registry_locator: locator })
  }
}

export const decodeBridgeResolutionAudit = (
  source: string,
  label = BRIDGE_AUDIT_RELPATH
): BridgeResolutionAudit => {
  let parsed: unknown
  try {
    parsed = JSON.parse(source)
  } catch (error) {
    throw new Error(`${label} is not valid JSON: ${String(error)}`)
  }
  const raw = record(parsed, label)
  exactKeys(
    raw,
    [
      "$schema",
      "schema_version",
      "audit_id",
      "checked_at_utc",
      "authority",
      "result_status",
      "does_not_alter_canonical_bridge_status",
      "scope",
      "outcomes",
      "rules",
      "default_outcome",
      "non_claim"
    ],
    label
  )
  if (
    raw.$schema !==
      "../../ontology/schema/ice-kg-bridge-resolution-audit-v1.schema.json" ||
    raw.schema_version !== "ice-kg-bridge-resolution-audit/v1" ||
    raw.authority !== "READ_ONLY_AUDIT_SIDECAR" ||
    raw.result_status !== "ZERO_RESOLVED_MATCHES" ||
    raw.does_not_alter_canonical_bridge_status !== true ||
    raw.default_outcome !== "NO_MATCH"
  ) {
    throw new Error(`${label} fixed non-resolving contract is invalid`)
  }
  const checkedAt = text(raw.checked_at_utc, `${label}.checked_at_utc`)
  if (!validUtcDateTime(checkedAt)) {
    throw new Error(`${label}.checked_at_utc must be UTC ISO-8601`)
  }
  const scope = record(raw.scope, `${label}.scope`)
  exactKeys(
    scope,
    [
      "canonical_graphs",
      "expected_unresolved_count",
      "expected_keyset_sha256",
      "keyset_encoding"
    ],
    `${label}.scope`
  )
  if (
    !Number.isInteger(scope.expected_unresolved_count) ||
    (scope.expected_unresolved_count as number) < 0
  ) {
    throw new Error(`${label}.scope.expected_unresolved_count is invalid`)
  }
  const keysetSha = text(
    scope.expected_keyset_sha256,
    `${label}.scope.expected_keyset_sha256`
  )
  if (!/^[0-9a-f]{64}$/.test(keysetSha)) {
    throw new Error(`${label}.scope.expected_keyset_sha256 is invalid`)
  }
  const outcomes = record(raw.outcomes, `${label}.outcomes`)
  exactKeys(
    outcomes,
    ["NO_MATCH", "ID_COLLISION", "REGISTRY_UNAVAILABLE"],
    `${label}.outcomes`
  )
  if (!Array.isArray(raw.rules) || raw.rules.length === 0) {
    throw new Error(`${label}.rules must be a non-empty array`)
  }
  const rules = raw.rules.map(decodeRule)
  if (new Set(rules.map(({ id }) => id)).size !== rules.length) {
    throw new Error(`${label}.rules contains duplicate rule IDs`)
  }
  const canonicalGraphs = stringArray(
    scope.canonical_graphs,
    `${label}.scope.canonical_graphs`
  )
  if (canonicalGraphs.some((path) => !isSafeArtifactPath(path))) {
    throw new Error(`${label}.scope.canonical_graphs contains an unsafe path`)
  }
  if (rules.some(({ graph }) => !canonicalGraphs.includes(graph))) {
    throw new Error(`${label}.rules names a graph outside canonical_graphs`)
  }
  return {
    $schema:
      "../../ontology/schema/ice-kg-bridge-resolution-audit-v1.schema.json",
    schema_version: "ice-kg-bridge-resolution-audit/v1",
    audit_id: text(raw.audit_id, `${label}.audit_id`),
    checked_at_utc: checkedAt,
    authority: "READ_ONLY_AUDIT_SIDECAR",
    result_status: "ZERO_RESOLVED_MATCHES",
    does_not_alter_canonical_bridge_status: true,
    scope: {
      canonical_graphs: canonicalGraphs,
      expected_unresolved_count: scope.expected_unresolved_count as number,
      expected_keyset_sha256: keysetSha,
      keyset_encoding: text(
        scope.keyset_encoding,
        `${label}.scope.keyset_encoding`
      )
    },
    outcomes: {
      NO_MATCH: text(outcomes.NO_MATCH, `${label}.outcomes.NO_MATCH`),
      ID_COLLISION: text(
        outcomes.ID_COLLISION,
        `${label}.outcomes.ID_COLLISION`
      ),
      REGISTRY_UNAVAILABLE: text(
        outcomes.REGISTRY_UNAVAILABLE,
        `${label}.outcomes.REGISTRY_UNAVAILABLE`
      )
    },
    rules,
    default_outcome: "NO_MATCH",
    non_claim: text(raw.non_claim, `${label}.non_claim`)
  }
}

const graphPath = (loaded: CollectionGraph): string => loaded.descriptor.path

export const unresolvedBridgeKey = (
  value: Pick<
    AuditedBridge,
    "graph" | "local_node_id" | "system" | "lookup_key"
  >
): string =>
  `${value.graph}\t${value.local_node_id}\t${value.system}\t${value.lookup_key}`

export const unresolvedBridgeDigest = (
  values: ReadonlyArray<
    Pick<AuditedBridge, "graph" | "local_node_id" | "system" | "lookup_key">
  >
): string =>
  createHash("sha256")
    .update(`${values.map(unresolvedBridgeKey).sort().join("\n")}\n`, "utf8")
    .digest("hex")

export const collectUnresolvedBridges = (
  graphs: ReadonlyArray<CollectionGraph>
): ReadonlyArray<AuditedBridge> =>
  graphs.flatMap((loaded) =>
    loaded.graph.kg_bridges
      .filter((bridge) => bridge.status === "UNRESOLVED")
      .map((bridge) => ({
        graph: graphPath(loaded),
        local_node_id: bridge.local_node_id,
        system: bridge.system,
        lookup_key: bridge.lookup_key ?? "",
        outcome: "NO_MATCH" as const,
        rule_id: null,
        registry_locator: null
      }))
  )

export interface BridgeAuditReport {
  readonly schema: "ice-kg-bridge-resolution-audit-report/v1"
  readonly audit_id: string
  readonly checked_at_utc: string
  readonly valid: boolean
  readonly errors: ReadonlyArray<string>
  readonly bridges: ReadonlyArray<AuditedBridge>
  readonly counts: Readonly<Record<BridgeOutcome, number>>
  readonly unresolved_bridges: number
  readonly resolved_matches: 0
  readonly actual_digest: string
  readonly does_not_alter_canonical_bridge_status: true
}

export const auditBridgeResolution = (
  audit: BridgeResolutionAudit,
  graphs: ReadonlyArray<CollectionGraph>
): BridgeAuditReport => {
  const errors: string[] = []
  const paths = graphs.map(graphPath).sort()
  if (
    JSON.stringify(paths) !==
    JSON.stringify([...audit.scope.canonical_graphs].sort())
  ) {
    errors.push("CANONICAL_GRAPH_SET_MISMATCH")
  }
  const source = collectUnresolvedBridges(graphs)
  if (source.some(({ lookup_key }) => lookup_key.length === 0)) {
    errors.push("UNRESOLVED_LOOKUP_KEY_MISSING")
  }
  if (source.length !== audit.scope.expected_unresolved_count) {
    errors.push("UNRESOLVED_COUNT_MISMATCH")
  }
  const actualDigest = unresolvedBridgeDigest(source)
  if (actualDigest !== audit.scope.expected_keyset_sha256) {
    errors.push("UNRESOLVED_KEYSET_OR_LOOKUP_KEY_MISMATCH")
  }

  const seen = new Set<string>()
  const bridges = source.map((bridge) => {
    const matches = audit.rules.filter(
      (rule) =>
        rule.graph === bridge.graph &&
        rule.system === bridge.system &&
        rule.local_node_ids.includes(bridge.local_node_id)
    )
    if (matches.length > 1) {
      errors.push(`DUPLICATE_AUDIT_RULE:${bridge.local_node_id}`)
    }
    const match = matches[0]
    if (match === undefined) return bridge
    const locator = match.registry_locator
    const anchor = locator?.anchors[bridge.local_node_id]
    return {
      ...bridge,
      outcome: match.outcome,
      rule_id: match.id,
      registry_locator:
        locator === undefined || anchor === undefined
          ? null
          : {
              repository: locator.repository,
              commit: locator.commit,
              blob_oid: locator.blob_oid,
              path: locator.path,
              url: `${locator.url}#${anchor}`,
              anchor,
              boundary: locator.boundary
            }
    }
  })

  for (const rule of audit.rules) {
    for (const localNodeId of rule.local_node_ids) {
      const key = `${rule.graph}\t${rule.system}\t${localNodeId}`
      if (seen.has(key)) errors.push(`DUPLICATE_RULE_TARGET:${key}`)
      seen.add(key)
      if (
        !source.some(
          (bridge) =>
            bridge.graph === rule.graph &&
            bridge.system === rule.system &&
            bridge.local_node_id === localNodeId
        )
      ) {
        errors.push(`AUDIT_RULE_TARGET_NOT_UNRESOLVED:${key}`)
      }
    }
  }

  const counts: Record<BridgeOutcome, number> = {
    NO_MATCH: 0,
    ID_COLLISION: 0,
    REGISTRY_UNAVAILABLE: 0
  }
  for (const bridge of bridges) counts[bridge.outcome] += 1
  return {
    schema: "ice-kg-bridge-resolution-audit-report/v1",
    audit_id: audit.audit_id,
    checked_at_utc: audit.checked_at_utc,
    valid: errors.length === 0,
    errors,
    bridges,
    counts,
    unresolved_bridges: bridges.length,
    resolved_matches: 0,
    actual_digest: actualDigest,
    does_not_alter_canonical_bridge_status: true
  }
}
