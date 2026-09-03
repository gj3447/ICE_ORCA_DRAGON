import { validateScientificIntuitionFlow, validateScientificIntuitionFlowV2 } from "../intuition/core.ts"
import { decodeScientificIntuitionFlow, decodeScientificIntuitionFlowV2 } from "../intuition/model.ts"
import { validateIceComparatorProtocol } from "../comparator-protocol/core.ts"
import { decodeIceComparatorProtocol } from "../comparator-protocol/model.ts"
import type { CollectionGraph } from "../ontology/collection-core.ts"
import type { SidecarCollection, SidecarKind, SidecarState } from "./model.ts"

export interface SidecarValidationIssue { readonly code: string; readonly message: string; readonly subject?: string }
export interface SidecarValidationReport { readonly schema: "non-authoritative-sidecar-collection-validation/v1"; readonly valid: boolean; readonly authority: "NON_AUTHORITATIVE_SIDECAR_REGISTRY"; readonly canonical_graph_unchanged: true; readonly does_not_authorize_execution: true; readonly counts: { readonly entries: number; readonly frozen_snapshots: number; readonly active_hypothesis_generation: number; readonly active_method_protocol: number }; readonly errors: ReadonlyArray<SidecarValidationIssue>; readonly boundaries: ReadonlyArray<string> }

interface FixedSidecarContract {
  readonly id: string
  readonly path: string
  readonly schema: string
  readonly version: string
  readonly authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION" | "NON_AUTHORITATIVE_METHOD_PROTOCOL"
  readonly state: SidecarState
  readonly hash?: string
}

const expected: Readonly<Record<SidecarKind, FixedSidecarContract>> = {
  SCIENTIFIC_INTUITION_V1: { id: "sidecar:scientific-intuition-gate1-v1", path: "research/intuition/scientific-intuition-signals.v1.json", schema: "ontology/schema/scientific-intuition-flow-v1.schema.json", version: "scientific-intuition-flow/v1", authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION", state: "FROZEN_SNAPSHOT", hash: "5f347af1d795743f03c4c096a14c34bcb18ee436ee32b7c968ad97c57c373781" },
  SCIENTIFIC_INTUITION_V2: { id: "sidecar:scientific-intuition-ice-v2", path: "research/intuition/scientific-intuition-signals.v2.json", schema: "ontology/schema/scientific-intuition-flow-v2.schema.json", version: "scientific-intuition-flow/v2", authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION", state: "ACTIVE_HYPOTHESIS_GENERATION" },
  COMPARATOR_PROTOCOL_V1: { id: "sidecar:external-comparator-v1", path: "research/benchmarks/ice-comparator-protocol.v1.json", schema: "ontology/schema/ice-comparator-protocol-v1.schema.json", version: "ice-comparator-protocol/v1", authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL", state: "ACTIVE_METHOD_PROTOCOL" }
} as const
const add = (errors: SidecarValidationIssue[], code: string, message: string, subject?: string) => errors.push(subject === undefined ? { code, message } : { code, message, subject })

export const validateSidecarCollection = (collection: SidecarCollection, documents: Readonly<Record<string, { readonly contents: string; readonly sha256: string }>>, graphs: ReadonlyArray<CollectionGraph>): SidecarValidationReport => {
  const errors: SidecarValidationIssue[] = []
  const ids = new Set<string>()
  const kinds = new Set<string>()
  for (const entry of collection.entries) {
    if (ids.has(entry.id)) add(errors, "DUPLICATE_ENTRY_ID", `entry '${entry.id}' is not unique`, entry.id); ids.add(entry.id)
    if (kinds.has(entry.kind)) add(errors, "DUPLICATE_ENTRY_KIND", `kind '${entry.kind}' is not unique`, entry.id); kinds.add(entry.kind)
    const required = expected[entry.kind]
    if (entry.id !== required.id || entry.path !== required.path || entry.schema_path !== required.schema || entry.schema_version !== required.version || entry.authority !== required.authority || entry.state !== required.state) add(errors, "ENTRY_STATIC_CONTRACT_MISMATCH", "entry does not match its fixed sidecar contract", entry.id)
    if (required.hash !== undefined && entry.document_sha256 !== required.hash) add(errors, "FROZEN_V1_HASH_MISMATCH", "frozen v1 registry hash is not the durable provenance hash", entry.id)
    const document = documents[entry.kind]
    if (document === undefined) { add(errors, "DOCUMENT_NOT_LOADED", "fixed sidecar document is unavailable", entry.id); continue }
    if (document.sha256 !== entry.document_sha256) add(errors, "DOCUMENT_HASH_MISMATCH", "registry digest does not match sidecar bytes", entry.id)
    try {
      if (entry.kind === "SCIENTIFIC_INTUITION_V1") {
        const report = validateScientificIntuitionFlow(decodeScientificIntuitionFlow(document.contents), graphs)
        for (const issue of report.errors) add(errors, `INTUITION_V1_${issue.code}`, issue.message, entry.id)
      } else if (entry.kind === "SCIENTIFIC_INTUITION_V2") {
        const report = validateScientificIntuitionFlowV2(decodeScientificIntuitionFlowV2(document.contents), graphs)
        for (const issue of report.errors) add(errors, `INTUITION_V2_${issue.code}`, issue.message, entry.id)
      } else {
        const v2 = documents.SCIENTIFIC_INTUITION_V2
        if (v2 === undefined) add(errors, "INTUITION_V2_REQUIRED", "comparator validation requires the v2 intuition sidecar", entry.id)
        else {
          const report = validateIceComparatorProtocol(decodeIceComparatorProtocol(document.contents), decodeScientificIntuitionFlowV2(v2.contents), graphs)
          for (const issue of report.errors) add(errors, `COMPARATOR_${issue.code}`, issue.message, entry.id)
        }
      }
    } catch (error) { add(errors, "DOCUMENT_SCHEMA_INVALID", error instanceof Error ? error.message : String(error), entry.id) }
  }
  for (const kind of Object.keys(expected)) if (!kinds.has(kind)) add(errors, "REQUIRED_ENTRY_MISSING", `required sidecar kind '${kind}' is missing`)
  return { schema: "non-authoritative-sidecar-collection-validation/v1", valid: errors.length === 0, authority: collection.authority, canonical_graph_unchanged: collection.canonical_graph_unchanged, does_not_authorize_execution: collection.does_not_authorize_execution, counts: { entries: collection.entries.length, frozen_snapshots: collection.entries.filter(({ state }) => state === "FROZEN_SNAPSHOT").length, active_hypothesis_generation: collection.entries.filter(({ state }) => state === "ACTIVE_HYPOTHESIS_GENERATION").length, active_method_protocol: collection.entries.filter(({ state }) => state === "ACTIVE_METHOD_PROTOCOL").length }, errors, boundaries: collection.boundaries }
}
