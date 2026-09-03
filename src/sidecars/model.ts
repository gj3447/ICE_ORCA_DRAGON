/** Strict registry for non-authoritative research sidecars. */
export const SIDECAR_COLLECTION_RELPATH = "research/sidecars/collection.v1.json"

export type SidecarKind =
  | "SCIENTIFIC_INTUITION_V1"
  | "SCIENTIFIC_INTUITION_V2"
  | "COMPARATOR_PROTOCOL_V1"
export type SidecarState =
  | "FROZEN_SNAPSHOT"
  | "ACTIVE_HYPOTHESIS_GENERATION"
  | "ACTIVE_METHOD_PROTOCOL"

export interface SidecarRegistryEntry {
  readonly id: string
  readonly title: string
  readonly kind: SidecarKind
  readonly path: string
  readonly schema_path: string
  readonly schema_version: string
  readonly document_sha256: string
  readonly state: SidecarState
  readonly authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION" | "NON_AUTHORITATIVE_METHOD_PROTOCOL"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly non_claim: string
  readonly boundary: string
}

export interface SidecarCollection {
  readonly $schema: "../../ontology/schema/non-authoritative-sidecar-collection-v1.schema.json"
  readonly schema_version: "non-authoritative-sidecar-collection/v1"
  readonly collection_id: "sidecar-collection:ice-orca-dragon"
  readonly title: string
  readonly description: string
  readonly updated_at_utc: string
  readonly authority: "NON_AUTHORITATIVE_SIDECAR_REGISTRY"
  readonly canonical_graph_unchanged: true
  readonly does_not_authorize_execution: true
  readonly entries: ReadonlyArray<SidecarRegistryEntry>
  readonly boundaries: ReadonlyArray<string>
}

export class SidecarCollectionError extends Error {
  constructor(message: string) { super(message); this.name = "SidecarCollectionError" }
}

type RecordValue = Record<string, unknown>
const forbidden = new Set(["claim", "evidence", "score", "probability", "polarity", "canonical_target", "execution_command", "next_step", "artifact", "result"])
const utc = /^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?Z$/
const kinds = new Set<SidecarKind>(["SCIENTIFIC_INTUITION_V1", "SCIENTIFIC_INTUITION_V2", "COMPARATOR_PROTOCOL_V1"])
const states = new Set<SidecarState>(["FROZEN_SNAPSHOT", "ACTIVE_HYPOTHESIS_GENERATION", "ACTIVE_METHOD_PROTOCOL"])

const record = (value: unknown, label: string): RecordValue => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new SidecarCollectionError(`${label} must be an object`)
  return value as RecordValue
}
const text = (value: unknown, label: string): string => {
  if (typeof value !== "string" || value.trim().length === 0) throw new SidecarCollectionError(`${label} must be a non-empty string`)
  return value
}
const truth = (value: unknown, label: string): true => {
  if (value !== true) throw new SidecarCollectionError(`${label} must be true`)
  return true
}
const exact = (value: RecordValue, keys: ReadonlyArray<string>, label: string): void => {
  for (const key of Object.keys(value)) if (!keys.includes(key)) throw new SidecarCollectionError(`${label} has unknown field '${key}'`)
}
const rejectForbidden = (value: unknown, label: string): void => {
  if (Array.isArray(value)) return value.forEach((item, index) => rejectForbidden(item, `${label}[${index}]`))
  if (typeof value !== "object" || value === null) return
  for (const [key, item] of Object.entries(value)) {
    if (forbidden.has(key)) throw new SidecarCollectionError(`${label} contains forbidden field '${key}'`)
    rejectForbidden(item, `${label}.${key}`)
  }
}
const stringArray = (value: unknown, label: string): ReadonlyArray<string> => {
  if (!Array.isArray(value) || value.length < 1) throw new SidecarCollectionError(`${label} must be a non-empty string array`)
  return value.map((item, index) => text(item, `${label}[${index}]`))
}
const validUtcDateTime = (value: string): boolean => {
  if (!utc.test(value) || Number.isNaN(Date.parse(value))) return false
  const match = /^(\d{4})-(\d{2})-(\d{2})T/.exec(value)
  if (match === null) return false
  const parsed = new Date(value)
  return parsed.getUTCFullYear() === Number(match[1]) && parsed.getUTCMonth() + 1 === Number(match[2]) && parsed.getUTCDate() === Number(match[3])
}

const entry = (value: unknown, label: string): SidecarRegistryEntry => {
  const item = record(value, label)
  exact(item, ["id", "title", "kind", "path", "schema_path", "schema_version", "document_sha256", "state", "authority", "canonical_graph_unchanged", "does_not_authorize_execution", "non_claim", "boundary"], label)
  const id = text(item.id, `${label}.id`)
  if (!/^sidecar:[a-z0-9][a-z0-9-]{2,127}$/.test(id)) throw new SidecarCollectionError(`${label}.id is invalid`)
  const kind = text(item.kind, `${label}.kind`) as SidecarKind
  if (!kinds.has(kind)) throw new SidecarCollectionError(`${label}.kind is invalid`)
  const state = text(item.state, `${label}.state`) as SidecarState
  if (!states.has(state)) throw new SidecarCollectionError(`${label}.state is invalid`)
  const hash = text(item.document_sha256, `${label}.document_sha256`)
  if (!/^[0-9a-f]{64}$/.test(hash)) throw new SidecarCollectionError(`${label}.document_sha256 must be lowercase SHA-256`)
  const authority = text(item.authority, `${label}.authority`)
  if (authority !== "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION" && authority !== "NON_AUTHORITATIVE_METHOD_PROTOCOL") throw new SidecarCollectionError(`${label}.authority is invalid`)
  return { id, title: text(item.title, `${label}.title`), kind, path: text(item.path, `${label}.path`), schema_path: text(item.schema_path, `${label}.schema_path`), schema_version: text(item.schema_version, `${label}.schema_version`), document_sha256: hash, state, authority, canonical_graph_unchanged: truth(item.canonical_graph_unchanged, `${label}.canonical_graph_unchanged`), does_not_authorize_execution: truth(item.does_not_authorize_execution, `${label}.does_not_authorize_execution`), non_claim: text(item.non_claim, `${label}.non_claim`), boundary: text(item.boundary, `${label}.boundary`) }
}

export const decodeSidecarCollection = (source: string, label = SIDECAR_COLLECTION_RELPATH): SidecarCollection => {
  let raw: unknown
  try { raw = JSON.parse(source) } catch (error) { throw new SidecarCollectionError(`${label} is not valid JSON: ${String(error)}`) }
  rejectForbidden(raw, label)
  const item = record(raw, label)
  exact(item, ["$schema", "schema_version", "collection_id", "title", "description", "updated_at_utc", "authority", "canonical_graph_unchanged", "does_not_authorize_execution", "entries", "boundaries"], label)
  if (item.$schema !== "../../ontology/schema/non-authoritative-sidecar-collection-v1.schema.json") throw new SidecarCollectionError(`${label}.$schema is invalid`)
  if (item.schema_version !== "non-authoritative-sidecar-collection/v1") throw new SidecarCollectionError(`${label}.schema_version is invalid`)
  if (item.collection_id !== "sidecar-collection:ice-orca-dragon") throw new SidecarCollectionError(`${label}.collection_id is invalid`)
  if (item.authority !== "NON_AUTHORITATIVE_SIDECAR_REGISTRY") throw new SidecarCollectionError(`${label}.authority is invalid`)
  const updated = text(item.updated_at_utc, `${label}.updated_at_utc`)
  if (!validUtcDateTime(updated)) throw new SidecarCollectionError(`${label}.updated_at_utc must be UTC ISO-8601`)
  if (!Array.isArray(item.entries) || item.entries.length < 3 || item.entries.length > 16) throw new SidecarCollectionError(`${label}.entries must contain 3 through 16 entries`)
  return { $schema: "../../ontology/schema/non-authoritative-sidecar-collection-v1.schema.json", schema_version: "non-authoritative-sidecar-collection/v1", collection_id: "sidecar-collection:ice-orca-dragon", title: text(item.title, `${label}.title`), description: text(item.description, `${label}.description`), updated_at_utc: updated, authority: "NON_AUTHORITATIVE_SIDECAR_REGISTRY", canonical_graph_unchanged: truth(item.canonical_graph_unchanged, `${label}.canonical_graph_unchanged`), does_not_authorize_execution: truth(item.does_not_authorize_execution, `${label}.does_not_authorize_execution`), entries: item.entries.map((value, index) => entry(value, `${label}.entries[${index}]`)), boundaries: stringArray(item.boundaries, `${label}.boundaries`) }
}
