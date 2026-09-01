import type { CollectionGraph } from "./collection-core.ts"
import type { ResearchCollection } from "./collection.ts"
import type { ResearchEdge, ResearchNode } from "./model.ts"

/** The stable JSON-LD 1.1 context for the repository-local ontology view. */
export const JSONLD_CONTEXT = {
  "@version": 1.1,
  ice: {
    "@id": "urn:ice-orca-dragon:ontology:",
    "@prefix": true
  },
  dcterms: {
    "@id": "http://purl.org/dc/terms/",
    "@prefix": true
  },
  prov: {
    "@id": "http://www.w3.org/ns/prov#",
    "@prefix": true
  },
  xsd: {
    "@id": "http://www.w3.org/2001/XMLSchema#",
    "@prefix": true
  },
  id: "@id",
  type: "@type"
} as const

export const JSONLD_PROFILE_VERSION = "ice-ontology-jsonld/1.0" as const
export const JSONLD_VOCABULARY = "urn:ice-orca-dragon:ontology:" as const
export const JSONLD_RESOURCE_BASE = "urn:ice-orca-dragon:resource:" as const

export interface JsonLdProjectionOptions {
  readonly graphKeys?: ReadonlyArray<string> | undefined
  readonly sourceDocuments?: ReadonlyArray<{
    readonly path: string
    readonly sha256: string
  }> | undefined
}

export interface JsonLdProjection {
  readonly "@context": typeof JSONLD_CONTEXT
  readonly "@id": string
  readonly "@type": "ice:ResearchCollection"
  readonly "ice:profileVersion": typeof JSONLD_PROFILE_VERSION
  readonly "ice:canonicalAuthority": "repository-json"
  readonly "ice:selectedGraphKeys": ReadonlyArray<string>
  readonly "ice:sourceDocuments": Record<string, unknown>
  readonly "@graph": ReadonlyArray<Record<string, unknown>>
}

const iriPart = (value: string): string => encodeURIComponent(value)
const resource = (...parts: ReadonlyArray<string>): string =>
  `${JSONLD_RESOURCE_BASE}${parts.map(iriPart).join(":")}`
const relationIri = (relation: string): string =>
  `${JSONLD_VOCABULARY}relation/${iriPart(relation)}`
const classIri = (type: string): string =>
  `ice:${type.replace(/(^|_)([a-z])/g, (_, prefix: string, letter: string) =>
    `${prefix}${letter.toUpperCase()}`
  )}`

const jsonValue = (value: unknown): Record<string, unknown> => ({
  "@value": value,
  "@type": "@json"
})

const ordered = (values: ReadonlyArray<unknown>): Record<string, unknown> => ({
  "@list": values
})

const nodeIri = (key: string, id: string): string => resource("graph", key, "node", id)

const nativeNodeFieldNames: Readonly<Record<string, string>> = {
  claim_id: "claimId",
  epistemic_state: "epistemicState",
  observed_status: "observedStatus",
  check_ids: "checkIds",
  content_hashes: "contentHashes",
  source_anchors: "sourceAnchors",
  introduced_in_commit: "introducedInCommit",
  artifact_kind: "artifactKind"
}

const nativeNodeFieldToProjectField = (field: string): string =>
  nativeNodeFieldNames[field] ?? field

const nodeProjection = (key: string, node: ResearchNode): Record<string, unknown> => {
  const result: Record<string, unknown> = {
    "@id": nodeIri(key, node.id),
    "@type": ["ice:ResearchNode", classIri(node.type)],
    "ice:graphKey": key,
    "ice:localId": node.id,
    "ice:nodeType": node.type,
    "ice:title": node.title,
    "ice:summary": node.summary,
    "ice:state": node.state,
    "ice:canonicalJson": jsonValue(node)
  }
  for (const [field, value] of Object.entries(node)) {
    if (["id", "type", "title", "summary", "state"].includes(field)) continue
    result[`ice:${nativeNodeFieldToProjectField(field)}`] = Array.isArray(value)
      ? ordered(value)
      : value !== null && typeof value === "object"
        ? jsonValue(value)
        : value
  }
  return Object.fromEntries(
    Object.entries(result).filter(([, value]) => value !== undefined)
  )
}

const edgeProjection = (key: string, edge: ResearchEdge): Record<string, unknown> => {
  const result: Record<string, unknown> = {
    "@id": resource("graph", key, "edge", edge.id),
    "@type": "ice:ResearchEdge",
    "ice:graphKey": key,
    "ice:localId": edge.id,
    "ice:from": { "@id": nodeIri(key, edge.from) },
    "ice:relation": { "@id": relationIri(edge.relation) },
    "ice:relationName": edge.relation,
    "ice:to": { "@id": nodeIri(key, edge.to) },
    "ice:canonicalJson": jsonValue(edge)
  }
  if (edge.polarity !== undefined) result["ice:polarity"] = edge.polarity
  if (edge.note !== undefined) result["ice:note"] = edge.note
  return result
}

/**
 * Deterministic, one-way JSON-LD 1.1 projection. Repository JSON remains the
 * canonical authority; this module deliberately provides no import or merge.
 */
export const projectCollectionToJsonLd = (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>,
  options: JsonLdProjectionOptions = {}
): JsonLdProjection => {
  const requested = options.graphKeys === undefined
    ? undefined
    : new Set(options.graphKeys)
  const selected = graphs.filter(({ descriptor }) =>
    requested === undefined || requested.has(descriptor.key)
  )
  const keys = selected.map(({ descriptor }) => descriptor.key)
  const collectionIri = resource("collection", collection.collection_id)
  const resources: Array<Record<string, unknown>> = []

  resources.push({
    "@id": collectionIri,
    "@type": "ice:ResearchCollection",
    "ice:collectionId": collection.collection_id,
    "ice:title": collection.title,
    "ice:description": collection.description,
    "ice:updatedAtUtc": { "@value": collection.updated_at_utc, "@type": "xsd:dateTime" },
    "ice:canonicalFile": collection.canonical_file,
    "ice:defaultGraph": collection.default_graph,
    "ice:canonicalJson": jsonValue(collection)
  })

  for (const descriptor of collection.graphs) {
    resources.push({
      "@id": resource("collection", collection.collection_id, "descriptor", descriptor.key),
      "@type": "ice:ResearchGraphDescriptor",
      "ice:collection": { "@id": collectionIri },
      "ice:key": descriptor.key,
      "ice:graphId": descriptor.graph_id,
      "ice:path": descriptor.path,
      "ice:guide": descriptor.guide,
      "ice:entryNodeLocalId": descriptor.entry_node,
      "ice:coverage": descriptor.coverage,
      "ice:corpusRoots": ordered(descriptor.corpus_roots),
      "ice:includes": ordered(descriptor.includes),
      "ice:excludes": ordered(descriptor.excludes),
      "ice:selected": keys.includes(descriptor.key),
      "ice:canonicalJson": jsonValue(descriptor)
    })
  }

  for (const [index, coverage] of collection.coverage_ledger.entries()) {
    resources.push({
      "@id": resource("collection", collection.collection_id, "coverage", String(index)),
      "@type": "ice:CoverageEntry",
      "ice:collection": { "@id": collectionIri },
      "ice:index": index,
      "ice:path": coverage.path,
      "ice:status": coverage.status,
      "ice:reason": coverage.reason,
      "ice:graphKey": coverage.graph ?? null,
      "ice:graphKeyNull": coverage.graph === undefined,
      "ice:canonicalJson": jsonValue(coverage)
    })
  }

  for (const [index, answer] of collection.quick_answers.entries()) {
    resources.push({
      "@id": resource("collection", collection.collection_id, "quick-answer", String(index)),
      "@type": "ice:CollectionQuickAnswer",
      "ice:collection": { "@id": collectionIri },
      "ice:index": index,
      "ice:question": answer.question,
      "ice:answer": answer.answer,
      "ice:refs": ordered(answer.refs.map((ref) => jsonValue(ref))),
      "ice:canonicalJson": jsonValue(answer)
    })
  }

  for (const path of collection.reading_paths) {
    resources.push({
      "@id": resource("collection", collection.collection_id, "reading-path", path.id),
      "@type": "ice:CollectionReadingPath",
      "ice:collection": { "@id": collectionIri },
      "ice:localId": path.id,
      "ice:title": path.title,
      "ice:summary": path.summary,
      "ice:navigationOnly": path.navigation_only,
      "ice:stops": ordered(path.stops.map((stop) => jsonValue(stop))),
      "ice:canonicalJson": jsonValue(path)
    })
  }

  for (const { descriptor, graph } of selected) {
    const graphIri = resource("graph", descriptor.key)
    resources.push({
      "@id": graphIri,
      "@type": "ice:ResearchGraph",
      "ice:collection": { "@id": collectionIri },
      "ice:key": descriptor.key,
      "ice:graphId": graph.graph_id,
      "ice:title": graph.title,
      "ice:description": graph.description,
      "ice:updatedAtUtc": { "@value": graph.updated_at_utc, "@type": "xsd:dateTime" },
      "ice:canonicalFile": graph.canonical_file,
      "ice:sourceInventory": graph.source_inventory,
      "ice:nodeTypeLegend": jsonValue(graph.node_type_legend),
      "ice:relationLegend": jsonValue(graph.relation_legend),
      "ice:canonicalJson": jsonValue(graph)
    })
    resources.push(...graph.nodes.map((node) => nodeProjection(descriptor.key, node)))
    resources.push(...graph.edges.map((edge) => edgeProjection(descriptor.key, edge)))
    for (const [index, answer] of graph.quick_answers.entries()) {
      resources.push({
        "@id": resource("graph", descriptor.key, "quick-answer", String(index)),
        "@type": "ice:GraphQuickAnswer",
        "ice:graph": { "@id": graphIri },
        "ice:index": index,
        "ice:question": answer.question,
        "ice:answer": answer.answer,
        "ice:claimIds": ordered(answer.claim_ids),
        "ice:canonicalJson": jsonValue(answer)
      })
    }
    for (const path of graph.reading_paths) {
      resources.push({
        "@id": resource("graph", descriptor.key, "reading-path", path.id),
        "@type": "ice:GraphReadingPath",
        "ice:graph": { "@id": graphIri },
        "ice:localId": path.id,
        "ice:title": path.title,
        "ice:summary": path.summary,
        "ice:nodes": ordered(path.nodes.map((id) => ({ "@id": nodeIri(descriptor.key, id) }))),
        "ice:canonicalJson": jsonValue(path)
      })
    }
    for (const [index, bridge] of graph.kg_bridges.entries()) {
      resources.push({
        "@id": resource("graph", descriptor.key, "kg-bridge", String(index)),
        "@type": "ice:KgBridge",
        "ice:graph": { "@id": graphIri },
        "ice:index": index,
        "ice:localNode": { "@id": nodeIri(descriptor.key, bridge.local_node_id) },
        "ice:system": bridge.system,
        "ice:status": bridge.status,
        "ice:checkedAtUtc": { "@value": bridge.checked_at_utc, "@type": "xsd:dateTime" },
        "ice:externalUid": bridge.external_uid === null
          ? { "@id": "ice:NoExternalUid" }
          : bridge.external_uid,
        "ice:relation": bridge.relation === null
          ? { "@id": "ice:NoRelation" }
          : bridge.relation,
        "ice:externalUidNull": bridge.external_uid === null,
        "ice:relationNull": bridge.relation === null,
        "ice:registry": bridge.registry ?? null,
        "ice:lookupKey": bridge.lookup_key ?? null,
        "ice:note": bridge.note ?? null,
        "ice:canonicalJson": jsonValue(bridge)
      })
    }
  }

  return {
    "@context": JSONLD_CONTEXT,
    "@id": collectionIri,
    "@type": "ice:ResearchCollection",
    "ice:profileVersion": JSONLD_PROFILE_VERSION,
    "ice:canonicalAuthority": "repository-json",
    "ice:selectedGraphKeys": keys,
    "ice:sourceDocuments": jsonValue(options.sourceDocuments ?? []),
    "@graph": resources
  }
}
