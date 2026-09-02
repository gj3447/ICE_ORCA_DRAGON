import { createHash } from "node:crypto"
import {
  mkdir,
  mkdtemp,
  readFile,
  realpath,
  rename,
  rm,
  writeFile
} from "node:fs/promises"
import { basename, join, relative, resolve } from "node:path"
import type { CollectionGraph } from "./collection-core.ts"
import type { ResearchCollection } from "./collection.ts"
import {
  buildRdfDataset,
  serializeDatasetAsNQuads,
  type RdfBuildOptions
} from "./rdf.ts"
import {
  loadStandardShaclShapesText,
  parseTurtleDataset,
  validateRdfDatasetWithShacl,
  type ShaclReport
} from "./shacl.ts"

export const RO_CRATE_CONTEXT =
  "https://w3id.org/ro/crate/1.3/context" as const

const crateMembers = [
  "research-graph.jsonld",
  "research-graph-compatibility.jsonld",
  "research-graph.nq",
  "research-graph-shapes.ttl",
  "shacl-report.json",
  "manifest.json"
] as const

type CrateMember = (typeof crateMembers)[number]

export interface PrepareInteropCrateOptions extends RdfBuildOptions {
  readonly workspaceRoot: string
  readonly createdAt?: string
}

export interface CreateInteropCrateOptions extends PrepareInteropCrateOptions {
  readonly outputDirectory: string
}

export interface InteropManifestFile {
  readonly path: Exclude<CrateMember, "manifest.json">
  readonly media_type: string
  readonly bytes: number
  readonly sha256: string
}

export interface InteropCrateManifest {
  readonly schema: "ice-ontology-interop-manifest/v1"
  readonly canonical_authority: "repository-json"
  readonly package_scope: "METADATA_AND_GRAPH_EXPORT_NO_RAW_RESULTS"
  readonly selected_graph_keys: ReadonlyArray<string>
  readonly source_documents: ReadonlyArray<{
    readonly path: string
    readonly sha256: string
  }>
  readonly files: ReadonlyArray<InteropManifestFile>
}

export interface PreparedInteropCrate {
  readonly schema: "ice-ontology-ro-crate-preview/v1"
  readonly metadata: Readonly<Record<string, unknown>>
  readonly manifest: InteropCrateManifest
  readonly shacl: ShaclReport
  readonly files: Readonly<Record<CrateMember, string>>
}

export interface InteropCrateResult {
  readonly schema: "ice-ontology-ro-crate/v1"
  readonly directory: string
  readonly files: ReadonlyArray<string>
  readonly manifest_sha256: string
  readonly shacl_conforms: true
}

const stableJson = (value: unknown): string => `${JSON.stringify(value, null, 2)}\n`
const sha256 = (value: string): string =>
  createHash("sha256").update(value).digest("hex")
const bytes = (value: string): number => Buffer.byteLength(value, "utf8")
const sourceIri = (path: string): string =>
  `urn:ice-orca-dragon:resource:canonical-document:${encodeURIComponent(path)}`

const assertTimestamp = (value: string): void => {
  if (
    !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value) ||
    Number.isNaN(Date.parse(value)) ||
    new Date(value).toISOString() !== value
  ) {
    throw new Error("RO-Crate creation time must be a canonical UTC ISO-8601 timestamp")
  }
}

const mediaTypeFor = (
  path: Exclude<CrateMember, "manifest.json">
): string => {
  if (path.endsWith(".jsonld")) return "application/ld+json"
  if (path === "research-graph.nq") return "application/n-quads"
  if (path === "research-graph-shapes.ttl") return "text/turtle"
  return "application/json"
}

/** Build and validate the complete package in memory without writing files. */
export const prepareOntologyInteropCrate = async (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>,
  options: PrepareInteropCrateOptions
): Promise<PreparedInteropCrate> => {
  const createdAt = options.createdAt ?? new Date().toISOString()
  assertTimestamp(createdAt)
  const built = await buildRdfDataset(collection, graphs, options)
  const shapesText = await loadStandardShaclShapesText(options.workspaceRoot)
  const shapes = await parseTurtleDataset(shapesText)
  const shacl = await validateRdfDatasetWithShacl(built.dataset, shapes)
  // This is the enriched named-graph/provenance document from which the
  // N-Quads dataset was derived, not the compatibility-only CLI JSON-LD view.
  const graphJsonLd = stableJson(built.datasetProjection)
  const compatibilityJsonLd = stableJson(built.projection)
  const graphNQuads = serializeDatasetAsNQuads(built.dataset)
  const normalizedShapes = shapesText.endsWith("\n") ? shapesText : `${shapesText}\n`
  const shaclJson = stableJson(shacl)
  const payloads = {
    "research-graph.jsonld": graphJsonLd,
    "research-graph-compatibility.jsonld": compatibilityJsonLd,
    "research-graph.nq": graphNQuads,
    "research-graph-shapes.ttl": normalizedShapes,
    "shacl-report.json": shaclJson
  } as const
  const manifest: InteropCrateManifest = {
    schema: "ice-ontology-interop-manifest/v1",
    canonical_authority: "repository-json",
    package_scope: "METADATA_AND_GRAPH_EXPORT_NO_RAW_RESULTS",
    selected_graph_keys: built.projection["ice:selectedGraphKeys"],
    source_documents: [...options.sourceDocuments],
    files: (Object.keys(payloads) as Array<keyof typeof payloads>).map((path) => ({
      path,
      media_type: mediaTypeFor(path),
      bytes: bytes(payloads[path]),
      sha256: sha256(payloads[path])
    }))
  }
  const manifestJson = stableJson(manifest)
  const memberDetails = [
    ...manifest.files,
    {
      path: "manifest.json" as const,
      media_type: "application/json",
      bytes: bytes(manifestJson),
      sha256: sha256(manifestJson)
    }
  ]
  const sourceDocuments = options.sourceDocuments
  const metadata = {
    "@context": [
      RO_CRATE_CONTEXT,
      {
        prov: "http://www.w3.org/ns/prov#",
        sha256: "https://w3id.org/security#digestValue"
      }
    ],
    "@graph": [
      {
        "@id": "ro-crate-metadata.json",
        "@type": "CreativeWork",
        conformsTo: { "@id": "https://w3id.org/ro/crate/1.3" },
        about: { "@id": "./" }
      },
      {
        "@id": "./",
        "@type": "Dataset",
        name: "ICE ontology interoperability export",
        description:
          "Generated graph metadata and validation package; raw research result files are not bundled.",
        datePublished: createdAt,
        license: { "@id": "https://spdx.org/licenses/AGPL-3.0-or-later" },
        hasPart: crateMembers.map((id) => ({ "@id": id }))
      },
      ...memberDetails.map((file) => ({
        "@id": file.path,
        "@type": "File",
        name: file.path,
        encodingFormat: file.media_type,
        contentSize: String(file.bytes),
        sha256: file.sha256,
        "prov:wasGeneratedBy": { "@id": "#export-action" }
      })),
      ...sourceDocuments.map((source) => ({
        "@id": sourceIri(source.path),
        "@type": ["CreativeWork", "prov:Entity"],
        identifier: source.path,
        sha256: source.sha256
      })),
      {
        "@id": "#ice-control-plane",
        "@type": ["SoftwareApplication", "prov:SoftwareAgent"],
        name: "ICE_ORCA_DRAGON control plane"
      },
      {
        "@id": "#export-action",
        "@type": ["CreateAction", "prov:Activity"],
        name: "Create validated ontology interoperability package",
        actionStatus: {
          "@id": "http://schema.org/CompletedActionStatus"
        },
        endTime: createdAt,
        instrument: { "@id": "#ice-control-plane" },
        object: sourceDocuments.map(({ path }) => ({ "@id": sourceIri(path) })),
        result: crateMembers.map((id) => ({ "@id": id })),
        "prov:used": sourceDocuments.map(({ path }) => ({ "@id": sourceIri(path) })),
        "prov:generated": crateMembers.map((id) => ({ "@id": id }))
      }
    ]
  }
  return {
    schema: "ice-ontology-ro-crate-preview/v1",
    metadata,
    manifest,
    shacl,
    files: {
      ...payloads,
      "manifest.json": manifestJson
    }
  }
}

const resolveSafeTarget = async (
  workspaceRoot: string,
  outputDirectory: string
): Promise<{ readonly target: string; readonly outputRoot: string }> => {
  if (!/^output\/[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(outputDirectory)) {
    throw new Error("RO-Crate output must be one safe directory directly below output/")
  }
  const root = await realpath(workspaceRoot)
  const outputCandidate = resolve(root, "output")
  await mkdir(outputCandidate, { recursive: true })
  const outputRoot = await realpath(outputCandidate)
  const containedOutput = relative(root, outputRoot)
  if (containedOutput !== "output") {
    throw new Error("workspace output directory resolves outside the repository")
  }
  const target = resolve(outputRoot, basename(outputDirectory))
  return { target, outputRoot }
}

const reserveTarget = async (
  target: string,
  outputDirectory: string
): Promise<void> => {
  try {
    // mkdir is the target reservation: unlike check-then-rename it cannot
    // replace a crate another process created between two filesystem calls.
    await mkdir(target)
  } catch (error) {
    if (typeof error === "object" && error !== null && "code" in error && error.code === "EEXIST") {
      throw new Error(`RO-Crate output already exists: ${outputDirectory}`)
    }
    throw error
  }
}

/**
 * Reserve a validated metadata/export RO-Crate target without overwriting an
 * existing directory. Publication is intentionally not claimed to be atomic;
 * referenced raw result files are never copied.
 */
export const createOntologyInteropCrate = async (
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>,
  options: CreateInteropCrateOptions
): Promise<InteropCrateResult> => {
  const prepared = await prepareOntologyInteropCrate(collection, graphs, options)
  if (!prepared.shacl.conforms) {
    throw new Error(
      `cannot create RO-Crate from a nonconforming RDF projection (${prepared.shacl.violations.length} violation(s))`
    )
  }
  const { target, outputRoot } = await resolveSafeTarget(
    options.workspaceRoot,
    options.outputDirectory
  )
  const temporary = await mkdtemp(join(outputRoot, ".ice-ro-crate-"))
  let targetReserved = false
  try {
    await Promise.all([
      ...crateMembers.map((path) =>
        writeFile(resolve(temporary, path), prepared.files[path], { flag: "wx" })
      ),
      writeFile(
        resolve(temporary, "ro-crate-metadata.json"),
        stableJson(prepared.metadata),
        { flag: "wx" }
      )
    ])
    // Claim the final name only after every member is complete in the private
    // temporary directory. The claim itself is atomic and never overwrites.
    await reserveTarget(target, options.outputDirectory)
    targetReserved = true
    await Promise.all([
      ...crateMembers.map((path) =>
        rename(resolve(temporary, path), resolve(target, path))
      ),
      rename(
        resolve(temporary, "ro-crate-metadata.json"),
        resolve(target, "ro-crate-metadata.json")
      )
    ])
    await rm(temporary, { recursive: true, force: true })
  } catch (error) {
    await rm(temporary, { recursive: true, force: true })
    if (targetReserved) {
      // This exact directory was exclusively created by reserveTarget above.
      await rm(target, { recursive: true, force: true })
    }
    throw error
  }
  return {
    schema: "ice-ontology-ro-crate/v1",
    directory: options.outputDirectory,
    files: ["ro-crate-metadata.json", ...crateMembers],
    manifest_sha256: sha256(prepared.files["manifest.json"]),
    shacl_conforms: true
  }
}

/** Read one generated crate member for tests and external validators. */
export const readInteropCrateMember = (
  directory: string,
  member: "ro-crate-metadata.json" | CrateMember
): Promise<string> => readFile(resolve(directory, member), "utf8")
