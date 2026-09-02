import { createHash } from "node:crypto"
import { Readable } from "node:stream"
import ParserN3 from "@rdfjs/parser-n3"
import type { DatasetCore, Quad, Stream as RdfStream, Term } from "@rdfjs/types"
import jsonld, { type JsonLdDocument } from "jsonld"
import rdf from "rdf-ext"
import type { QuadExt } from "rdf-ext/lib/Quad.js"
import type { CollectionGraph } from "./collection-core.ts"
import type { ResearchCollection } from "./collection.ts"
import { isSafeArtifactPath } from "./core.ts"
import {
  JSONLD_RESOURCE_BASE,
  projectCollectionToJsonLd,
  type JsonLdProjectionOptions
} from "./jsonld.ts"

/** W3C RDF Dataset Canonicalization 1.0, provided by jsonld 9/rdf-canonize. */
export const RDF_CANONICALIZATION_ALGORITHM = "RDFC-1.0" as const

export interface RdfBuildOptions extends JsonLdProjectionOptions {
  readonly sourceDocuments: ReadonlyArray<{
    readonly path: string
    readonly sha256: string
  }>
}

export interface RdfDatasetBuild {
  readonly dataset: DatasetCore
  /** Compatibility projection emitted by `ontology export --format jsonld`. */
  readonly projection: ReturnType<typeof projectCollectionToJsonLd>
  /** JSON-LD document used to create the named RDF dataset. */
  readonly datasetProjection: Readonly<Record<string, unknown>>
  /** Exact byte hash of the compatibility JSON-LD projection. */
  readonly compatibilityProjectionSha256: string
  readonly compatibilityProjectionIri: string
  readonly activityIri: string
}

const iriPart = (value: string): string => encodeURIComponent(value)
const resource = (...parts: ReadonlyArray<string>): string =>
  `${JSONLD_RESOURCE_BASE}${parts.map(iriPart).join(":")}`
const graphIri = (key: string): string => resource("graph", key)
const documentIri = (path: string): string => resource("canonical-document", path)
const sha256 = (text: string): string =>
  createHash("sha256").update(text).digest("hex")

const lexicalCompare = (left: string, right: string): number =>
  left < right ? -1 : left > right ? 1 : 0

const collectStream = async (
  stream: RdfStream<QuadExt>
): Promise<ReadonlyArray<QuadExt>> =>
  new Promise((resolveStream, reject) => {
    const values: Array<QuadExt> = []
    stream.on("data", (value: QuadExt) => values.push(value))
    stream.on("error", reject)
    stream.on("end", () => resolveStream(values))
  })

const typesOf = (record: Readonly<Record<string, unknown>>): ReadonlyArray<unknown> => {
  const value = record["@type"]
  return value === undefined ? [] : Array.isArray(value) ? value : [value]
}

const withProvEntityType = (
  record: Readonly<Record<string, unknown>>
): Readonly<Record<string, unknown>> => {
  const types = typesOf(record)
  return types.includes("ice:Artifact") || types.includes("ice:Policy")
    ? { ...record, "@type": [...types, "prov:Entity"] }
    : record
}

const graphKeyForResource = (
  record: Readonly<Record<string, unknown>>,
  keys: ReadonlyArray<string>
): string | undefined => {
  const id = record["@id"]
  if (typeof id !== "string") return undefined
  return keys.find((key) => {
    const base = graphIri(key)
    return id === base || id.startsWith(`${base}:`)
  })
}

const buildDatasetProjection = (
  projection: ReturnType<typeof projectCollectionToJsonLd>
): {
  readonly document: Readonly<Record<string, unknown>>
  readonly compatibilityProjectionSha256: string
  readonly compatibilityProjectionIri: string
  readonly activityIri: string
} => {
  const keys = projection["ice:selectedGraphKeys"]
  const nativeProjection = `${JSON.stringify(projection, null, 2)}\n`
  const compatibilityProjectionSha256 = sha256(nativeProjection)
  const activityIri = resource(
    "export",
    "projection-activity",
    compatibilityProjectionSha256
  )
  const compatibilityProjectionIri = resource(
    "export",
    "compatibility-jsonld-projection",
    compatibilityProjectionSha256
  )
  const softwareIri = resource("software", "ice-control-plane")
  const sourceDocuments = (projection["ice:sourceDocuments"]["@value"] ?? []) as ReadonlyArray<{
    readonly path: string
    readonly sha256: string
  }>
  const sourceIds = sourceDocuments.map(({ path }) => documentIri(path))

  const projectedResources = projection["@graph"].map(withProvEntityType)
  const collectionResource = projectedResources.find(
    (record) => record["@id"] === projection["@id"]
  )
  const rootResource = {
    ...(collectionResource ?? {}),
    "@id": projection["@id"],
    "@type": "ice:ResearchCollection",
    "ice:profileVersion": projection["ice:profileVersion"],
    "ice:canonicalAuthority": projection["ice:canonicalAuthority"],
    "ice:selectedGraphKeys": projection["ice:selectedGraphKeys"],
    "ice:sourceDocuments": projection["ice:sourceDocuments"]
  }
  const remaining = projectedResources.filter(
    (record) => record["@id"] !== projection["@id"]
  )
  const defaultResources = remaining.filter(
    (record) => graphKeyForResource(record, keys) === undefined
  )
  const namedGraphs = keys.map((key) => ({
    "@id": graphIri(key),
    "@graph": remaining.filter(
      (record) => graphKeyForResource(record, keys) === key
    )
  }))
  const provenanceResources: ReadonlyArray<Readonly<Record<string, unknown>>> = [
    {
      "@id": softwareIri,
      "@type": "prov:SoftwareAgent",
      "ice:name": "ICE_ORCA_DRAGON control plane"
    },
    ...sourceDocuments.map((source) => ({
      "@id": documentIri(source.path),
      "@type": ["ice:SourceDocument", "prov:Entity"],
      "ice:path": source.path,
      "ice:sha256": source.sha256
    })),
    {
      "@id": activityIri,
      "@type": ["ice:ProjectionExportActivity", "prov:Activity"],
      "ice:profileVersion": projection["ice:profileVersion"],
      "ice:format": "application/ld+json",
      "ice:serializationRole": "compatibility-projection",
      "prov:used": sourceIds.map((id) => ({ "@id": id })),
      "prov:wasAssociatedWith": { "@id": softwareIri },
      "prov:generated": { "@id": compatibilityProjectionIri }
    },
    {
      "@id": compatibilityProjectionIri,
      "@type": ["ice:ProjectionOutput", "prov:Entity"],
      "ice:name": "ICE compatibility JSON-LD projection",
      "ice:format": "application/ld+json",
      "ice:serializationRole": "compatibility-projection",
      "ice:digestScope": "exact bytes emitted by ontology export --format jsonld",
      // The enriched dataset cannot contain its own exact byte digest without
      // self-reference. This entity deliberately and explicitly identifies the
      // separate compatibility projection, which the RO-Crate also includes.
      "ice:sha256": compatibilityProjectionSha256,
      "prov:wasGeneratedBy": { "@id": activityIri },
      "prov:wasDerivedFrom": sourceIds.map((id) => ({ "@id": id }))
    }
  ]
  return {
    document: {
      "@context": projection["@context"],
      "@graph": [rootResource, ...defaultResources, ...namedGraphs, ...provenanceResources]
    },
    compatibilityProjectionSha256,
    compatibilityProjectionIri,
    activityIri
  }
}

/**
 * Converts the one authored native JSON collection into a JSON-LD 1.1 named
 * RDF dataset. JSON-LD lists remain in the same named graph as their owning
 * graph resource, while the collection envelope and build provenance remain
 * in the default graph.
 */
export const buildRdfDataset = async (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>,
  options: RdfBuildOptions
): Promise<RdfDatasetBuild> => {
  if (options.sourceDocuments.length === 0) {
    throw new Error("RDF projection requires at least one pinned source document")
  }
  const sourcePaths = new Set<string>()
  for (const source of options.sourceDocuments) {
    if (!isSafeArtifactPath(source.path) || !/^[a-f0-9]{64}$/.test(source.sha256)) {
      throw new Error("RDF projection source documents require a safe repository-relative path and lowercase SHA-256")
    }
    if (sourcePaths.has(source.path)) {
      throw new Error(`RDF projection source document is duplicated: '${source.path}'`)
    }
    sourcePaths.add(source.path)
  }
  const projection = projectCollectionToJsonLd(collection, graphs, options)
  const built = buildDatasetProjection(projection)
  // jsonld 9 delegates this option to rdf-canonize, but the installed
  // DefinitelyTyped surface has not yet declared canonizeOptions.
  const nquads = await jsonld.canonize(built.document as JsonLdDocument, {
    canonizeOptions: { algorithm: RDF_CANONICALIZATION_ALGORITHM },
    format: "application/n-quads"
  } as any)
  const parsed = new ParserN3<QuadExt>({ factory: rdf }).import(
    Readable.from([nquads])
  )
  const dataset = rdf.dataset()
  for (const quad of await collectStream(parsed)) dataset.add(quad)
  return {
    dataset,
    projection,
    datasetProjection: built.document,
    compatibilityProjectionSha256: built.compatibilityProjectionSha256,
    compatibilityProjectionIri: built.compatibilityProjectionIri,
    activityIri: built.activityIri
  }
}

const escapeLiteral = (value: string): string =>
  [...value].map((character) => {
    if (character === "\\") return "\\\\"
    if (character === '"') return '\\"'
    if (character === "\n") return "\\n"
    if (character === "\r") return "\\r"
    if (character === "\t") return "\\t"
    if (character === "\b") return "\\b"
    if (character === "\f") return "\\f"
    const point = character.codePointAt(0) ?? 0
    return point <= 0x1f || point === 0x7f
      ? `\\u${point.toString(16).padStart(4, "0")}`
      : character
  }).join("")

const termToNQuads = (term: Term): string => {
  if (term.termType === "NamedNode") return `<${term.value}>`
  // rdf-ext prefixes parser-provided blank labels with a process-global
  // counter. The suffix is the URDNA2015 canonical identifier.
  if (term.termType === "BlankNode") return `_:${term.value.replace(/^b\d+_/, "")}`
  if (term.termType === "DefaultGraph") return ""
  if (term.termType === "Literal") {
    const value = `"${escapeLiteral(term.value)}"`
    return term.language.length > 0
      ? `${value}@${term.language}`
      : term.datatype.value === "http://www.w3.org/2001/XMLSchema#string"
        ? value
        : `${value}^^<${term.datatype.value}>`
  }
  throw new Error(`unsupported RDF term type '${term.termType}'`)
}

export const serializeQuadsAsNQuads = (quads: Iterable<Quad>): string => {
  const lines = [...quads]
    .map((quad) => [
      termToNQuads(quad.subject),
      termToNQuads(quad.predicate),
      termToNQuads(quad.object),
      quad.graph.termType === "DefaultGraph" ? "" : termToNQuads(quad.graph)
    ].filter(Boolean).join(" ") + " .")
    .sort(lexicalCompare)
  return lines.length === 0 ? "" : `${lines.join("\n")}\n`
}

/** Byte-stable N-Quads serialization for interchange and crate payloads. */
export const serializeDatasetAsNQuads = (dataset: DatasetCore): string =>
  serializeQuadsAsNQuads(dataset)
