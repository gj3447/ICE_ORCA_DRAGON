import { createHash } from "node:crypto"
import { lstat, readFile, readdir, realpath } from "node:fs/promises"
import { relative, resolve, sep } from "node:path"
import { Effect, Schema } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { Workspace } from "../workspace.ts"
import type { CollectionGraph } from "./collection-core.ts"
import type { ResearchCollection } from "./collection.ts"
import { isSafeArtifactPath } from "./core.ts"

export const RESEARCH_FAMILY_INDEX_RELPATH =
  "ontology/research-family-index.v1.json"

const NonEmptyString = Schema.NonEmptyString
const Sha256 = Schema.String.pipe(Schema.pattern(/^[0-9a-f]{64}$/))
const SafePath = Schema.String.pipe(
  Schema.filter((value) => isSafeArtifactPath(value), {
    message: () => "must be a safe repository-relative path"
  })
)
const UtcDateTime = Schema.String.pipe(
  Schema.pattern(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/)
)

const ObservedCountsSchema = Schema.Struct({
  filesystem_files: Schema.NonNegativeInt,
  excluded_generated_files: Schema.NonNegativeInt,
  ordinary_files: Schema.NonNegativeInt
})

const DecisiveUnitSchema = Schema.Struct({
  id: Schema.String.pipe(Schema.pattern(/^decisive-unit:[a-z0-9-]+$/)),
  title: NonEmptyString,
  unit_kind: Schema.Literal(
    "RESULT_LEDGER",
    "RESULT_AND_CHECK_BUNDLE",
    "NEGATIVE_CONTROL_BUNDLE",
    "SOURCE_AND_SCOPE_BUNDLE"
  ),
  paths: Schema.NonEmptyArray(SafePath).pipe(Schema.maxItems(32)),
  canonical_evidence_refs: Schema.NonEmptyArray(
    Schema.String.pipe(Schema.pattern(/^evidence:[A-Za-z0-9_.:-]+$/))
  ).pipe(Schema.maxItems(8)),
  boundary: NonEmptyString
})

const ResearchFamilySchema = Schema.Struct({
  id: Schema.String.pipe(Schema.pattern(/^research-family:[a-z0-9-]+$/)),
  title: NonEmptyString,
  graph_key: Schema.String.pipe(Schema.pattern(/^[a-z0-9-]+$/)),
  roots: Schema.NonEmptyArray(SafePath).pipe(Schema.maxItems(8)),
  observed_counts: ObservedCountsSchema,
  inventory_sha256: Sha256,
  decisive_units: Schema.NonEmptyArray(DecisiveUnitSchema).pipe(
    Schema.maxItems(16)
  ),
  unassigned_files_disposition: Schema.Literal(
    "ARCHIVAL_SUPPORT_ONLY_NOT_INDEPENDENT_EVIDENCE"
  ),
  boundary: NonEmptyString
})

export const ResearchFamilyIndexSchema = Schema.Struct({
  $schema: Schema.Literal("schema/research-family-index-v1.schema.json"),
  schema_version: Schema.Literal("research-family-index/v1"),
  index_id: Schema.String.pipe(
    Schema.pattern(/^research-family-index:[a-z0-9-]+$/)
  ),
  title: NonEmptyString,
  description: NonEmptyString,
  updated_at_utc: UtcDateTime,
  authority: Schema.Literal("NAVIGATION_AND_PROVENANCE_ONLY"),
  coverage_status_remains: Schema.Literal("PARTIAL"),
  inventory_algorithm: Schema.Literal(
    "sha256(sorted UTF-8 lines: repository-relative-path<TAB>file-sha256<LF>)"
  ),
  generated_cache_policy: Schema.Literal(
    "EXCLUDE_ONLY_PATHS_WITH___pycache___SEGMENT_OR_PYC_SUFFIX"
  ),
  observed_totals: ObservedCountsSchema,
  families: Schema.NonEmptyArray(ResearchFamilySchema).pipe(
    Schema.maxItems(16)
  )
})

const ResearchFamilyIndexFromString = Schema.parseJson(
  ResearchFamilyIndexSchema
)

export type ResearchFamilyIndex = Schema.Schema.Type<
  typeof ResearchFamilyIndexSchema
>

export const decodeResearchFamilyIndex = (
  source: string,
  label = RESEARCH_FAMILY_INDEX_RELPATH
): Effect.Effect<ResearchFamilyIndex, IceError> =>
  Schema.decodeUnknown(ResearchFamilyIndexFromString)(source, {
    errors: "all",
    onExcessProperty: "error"
  }).pipe(
    Effect.mapError((error) =>
      iceError(
        "RESEARCH_FAMILY_INDEX_SCHEMA_INVALID",
        `${label} does not satisfy research-family-index/v1: ${String(error)}`
      )
    )
  )

export const loadResearchFamilyIndex = Effect.gen(function* () {
  const workspace = yield* Workspace
  const source = yield* Effect.tryPromise({
    try: () => readFile(resolve(workspace.root, RESEARCH_FAMILY_INDEX_RELPATH), "utf8"),
    catch: (error) =>
      iceError(
        "RESEARCH_FAMILY_INDEX_READ_FAILED",
        `cannot read ${RESEARCH_FAMILY_INDEX_RELPATH}: ${error instanceof Error ? error.message : String(error)}`
      )
  })
  return yield* decodeResearchFamilyIndex(source)
})

export interface ResearchFamilyIndexIssue {
  readonly code: string
  readonly message: string
  readonly subject?: string
}

export interface ResearchFamilyAuditEntry {
  readonly id: string
  readonly title: string
  readonly graph_key: string
  readonly roots: ReadonlyArray<string>
  readonly filesystem_files: number
  readonly excluded_generated_files: number
  readonly ordinary_files: number
  readonly decisive_units: number
  readonly decisive_files: number
  readonly unassigned_ordinary_files: number
  readonly inventory_sha256: string
  readonly boundary: string
}

export interface ResearchFamilyIndexAuditReport {
  readonly schema: "research-family-index-audit/v1"
  readonly index_id: string
  readonly valid: boolean
  readonly authority: "NAVIGATION_AND_PROVENANCE_ONLY"
  readonly coverage_status_remains: "PARTIAL"
  readonly totals: {
    readonly filesystem_files: number
    readonly excluded_generated_files: number
    readonly ordinary_files: number
    readonly decisive_files: number
    readonly unassigned_ordinary_files: number
  }
  readonly families: ReadonlyArray<ResearchFamilyAuditEntry>
  readonly errors: ReadonlyArray<ResearchFamilyIndexIssue>
  readonly boundary: string
}

const duplicateValues = (values: ReadonlyArray<string>): ReadonlyArray<string> => {
  const seen = new Set<string>()
  const duplicates = new Set<string>()
  for (const value of values) {
    if (seen.has(value)) duplicates.add(value)
    seen.add(value)
  }
  return [...duplicates].sort()
}

const isGeneratedCache = (path: string): boolean =>
  path.split("/").includes("__pycache__") || path.endsWith(".pyc")

const contained = (root: string, candidate: string): boolean => {
  const rel = relative(root, candidate)
  return (
    rel === "" ||
    (!rel.startsWith(`..${sep}`) && rel !== ".." && !rel.startsWith("/"))
  )
}

interface RootInventory {
  readonly filesystemFiles: ReadonlyArray<string>
  readonly excludedGeneratedFiles: ReadonlyArray<string>
  readonly ordinaryFiles: ReadonlyArray<string>
  readonly inventorySha256: string
}

const inventoryRoots = async (
  workspaceRoot: string,
  roots: ReadonlyArray<string>,
  issues: ResearchFamilyIndexIssue[],
  subject: string
): Promise<RootInventory> => {
  const workspaceReal = await realpath(workspaceRoot)
  const filesystemFiles: string[] = []
  const excludedGeneratedFiles: string[] = []
  const ordinaryFiles: string[] = []

  const visit = async (absolute: string, relpath: string): Promise<void> => {
    const info = await lstat(absolute)
    if (info.isSymbolicLink()) {
      issues.push({
        code: "RESEARCH_FAMILY_SYMLINK_REJECTED",
        message: "family inventories reject symlinks rather than following them",
        subject: relpath
      })
      return
    }
    const actual = await realpath(absolute)
    if (!contained(workspaceReal, actual)) {
      issues.push({
        code: "RESEARCH_FAMILY_PATH_ESCAPES_WORKSPACE",
        message: "family path resolves outside the workspace",
        subject: relpath
      })
      return
    }
    if (info.isDirectory()) {
      for (const name of (await readdir(absolute)).sort()) {
        await visit(resolve(absolute, name), `${relpath}/${name}`)
      }
      return
    }
    if (!info.isFile()) return
    filesystemFiles.push(relpath)
    if (isGeneratedCache(relpath)) excludedGeneratedFiles.push(relpath)
    else ordinaryFiles.push(relpath)
  }

  for (const root of [...roots].sort()) {
    try {
      await visit(resolve(workspaceReal, root), root)
    } catch (error) {
      issues.push({
        code: "RESEARCH_FAMILY_ROOT_READ_FAILED",
        message: error instanceof Error ? error.message : String(error),
        subject: `${subject}:${root}`
      })
    }
  }

  const digest = createHash("sha256")
  for (const path of ordinaryFiles.sort()) {
    const fileHash = createHash("sha256")
      .update(await readFile(resolve(workspaceReal, path)))
      .digest("hex")
    digest.update(`${path}\t${fileHash}\n`, "utf8")
  }
  return {
    filesystemFiles: filesystemFiles.sort(),
    excludedGeneratedFiles: excludedGeneratedFiles.sort(),
    ordinaryFiles: ordinaryFiles.sort(),
    inventorySha256: digest.digest("hex")
  }
}

const pushMismatch = (
  issues: ResearchFamilyIndexIssue[],
  subject: string,
  field: string,
  expected: number | string,
  observed: number | string
): void => {
  if (expected === observed) return
  issues.push({
    code: "RESEARCH_FAMILY_INVENTORY_MISMATCH",
    message: `${field}: recorded=${String(expected)} observed=${String(observed)}`,
    subject
  })
}

export const auditResearchFamilyIndex = async (
  workspaceRoot: string,
  index: ResearchFamilyIndex,
  collection: ResearchCollection,
  graphs: ReadonlyArray<CollectionGraph>
): Promise<ResearchFamilyIndexAuditReport> => {
  const errors: ResearchFamilyIndexIssue[] = []
  const familyReports: ResearchFamilyAuditEntry[] = []

  for (const duplicate of duplicateValues(index.families.map(({ id }) => id))) {
    errors.push({
      code: "RESEARCH_FAMILY_DUPLICATE_ID",
      message: "family IDs must be unique",
      subject: duplicate
    })
  }
  const recordedRoots = index.families.flatMap(({ roots }) => roots)
  for (const duplicate of duplicateValues(recordedRoots)) {
    errors.push({
      code: "RESEARCH_FAMILY_DUPLICATE_ROOT",
      message: "each PARTIAL corpus root must belong to exactly one family",
      subject: duplicate
    })
  }
  const expectedPartialRoots = collection.graphs
    .filter(({ coverage }) => coverage === "PARTIAL")
    .flatMap(({ corpus_roots }) => corpus_roots)
    .sort()
  const actualPartialRoots = [...recordedRoots].sort()
  if (JSON.stringify(expectedPartialRoots) !== JSON.stringify(actualPartialRoots)) {
    errors.push({
      code: "RESEARCH_FAMILY_PARTIAL_ROOT_SET_MISMATCH",
      message: `expected PARTIAL roots ${JSON.stringify(expectedPartialRoots)} but index records ${JSON.stringify(actualPartialRoots)}`
    })
  }

  for (const family of index.families) {
    const descriptor = collection.graphs.find(({ key }) => key === family.graph_key)
    if (
      descriptor === undefined ||
      descriptor.coverage !== "PARTIAL" ||
      family.roots.some((root) => !descriptor.corpus_roots.includes(root))
    ) {
      errors.push({
        code: "RESEARCH_FAMILY_GRAPH_SCOPE_MISMATCH",
        message: "family graph and roots must match one PARTIAL collection descriptor",
        subject: family.id
      })
    }

    for (const duplicate of duplicateValues(
      family.decisive_units.map(({ id }) => id)
    )) {
      errors.push({
        code: "RESEARCH_FAMILY_DUPLICATE_UNIT_ID",
        message: "decisive-unit IDs must be unique within a family",
        subject: `${family.id}:${duplicate}`
      })
    }
    const decisivePaths = family.decisive_units.flatMap(({ paths }) => paths)
    for (const duplicate of duplicateValues(decisivePaths)) {
      errors.push({
        code: "RESEARCH_FAMILY_DUPLICATE_DECISIVE_PATH",
        message: "one file cannot count as two independent decisive units",
        subject: `${family.id}:${duplicate}`
      })
    }

    const inventory = await inventoryRoots(
      workspaceRoot,
      family.roots,
      errors,
      family.id
    )
    const ordinarySet = new Set(inventory.ordinaryFiles)
    for (const path of decisivePaths) {
      if (!family.roots.some((root) => path === root || path.startsWith(`${root}/`))) {
        errors.push({
          code: "RESEARCH_FAMILY_DECISIVE_PATH_OUTSIDE_ROOT",
          message: "decisive path is outside its family roots",
          subject: `${family.id}:${path}`
        })
      } else if (!ordinarySet.has(path)) {
        errors.push({
          code: "RESEARCH_FAMILY_DECISIVE_PATH_MISSING",
          message: "decisive path is missing, non-regular, or generated cache",
          subject: `${family.id}:${path}`
        })
      }
    }

    const graph = graphs.find(({ descriptor: entry }) => entry.key === family.graph_key)
    const graphEvidence = new Set(
      graph?.graph.nodes
        .filter(({ type }) => type === "evidence")
        .map(({ id }) => id) ?? []
    )
    for (const ref of family.decisive_units.flatMap(
      ({ canonical_evidence_refs }) => canonical_evidence_refs
    )) {
      if (!graphEvidence.has(ref)) {
        errors.push({
          code: "RESEARCH_FAMILY_EVIDENCE_REF_MISSING",
          message: "canonical evidence reference is absent from the named graph",
          subject: `${family.id}:${ref}`
        })
      }
    }

    pushMismatch(
      errors,
      family.id,
      "filesystem_files",
      family.observed_counts.filesystem_files,
      inventory.filesystemFiles.length
    )
    pushMismatch(
      errors,
      family.id,
      "excluded_generated_files",
      family.observed_counts.excluded_generated_files,
      inventory.excludedGeneratedFiles.length
    )
    pushMismatch(
      errors,
      family.id,
      "ordinary_files",
      family.observed_counts.ordinary_files,
      inventory.ordinaryFiles.length
    )
    pushMismatch(
      errors,
      family.id,
      "inventory_sha256",
      family.inventory_sha256,
      inventory.inventorySha256
    )

    const decisiveFileSet = new Set(
      decisivePaths.filter((path) => ordinarySet.has(path))
    )
    familyReports.push({
      id: family.id,
      title: family.title,
      graph_key: family.graph_key,
      roots: family.roots,
      filesystem_files: inventory.filesystemFiles.length,
      excluded_generated_files: inventory.excludedGeneratedFiles.length,
      ordinary_files: inventory.ordinaryFiles.length,
      decisive_units: family.decisive_units.length,
      decisive_files: decisiveFileSet.size,
      unassigned_ordinary_files:
        inventory.ordinaryFiles.length - decisiveFileSet.size,
      inventory_sha256: inventory.inventorySha256,
      boundary: family.boundary
    })
  }

  const totals = familyReports.reduce(
    (sum, family) => ({
      filesystem_files: sum.filesystem_files + family.filesystem_files,
      excluded_generated_files:
        sum.excluded_generated_files + family.excluded_generated_files,
      ordinary_files: sum.ordinary_files + family.ordinary_files,
      decisive_files: sum.decisive_files + family.decisive_files,
      unassigned_ordinary_files:
        sum.unassigned_ordinary_files + family.unassigned_ordinary_files
    }),
    {
      filesystem_files: 0,
      excluded_generated_files: 0,
      ordinary_files: 0,
      decisive_files: 0,
      unassigned_ordinary_files: 0
    }
  )
  pushMismatch(
    errors,
    index.index_id,
    "total filesystem_files",
    index.observed_totals.filesystem_files,
    totals.filesystem_files
  )
  pushMismatch(
    errors,
    index.index_id,
    "total excluded_generated_files",
    index.observed_totals.excluded_generated_files,
    totals.excluded_generated_files
  )
  pushMismatch(
    errors,
    index.index_id,
    "total ordinary_files",
    index.observed_totals.ordinary_files,
    totals.ordinary_files
  )

  return {
    schema: "research-family-index-audit/v1",
    index_id: index.index_id,
    valid: errors.length === 0,
    authority: index.authority,
    coverage_status_remains: index.coverage_status_remains,
    totals,
    families: familyReports,
    errors,
    boundary:
      "Family indexing adds provenance density only; it creates no claim, evidence, physics promotion, or execution authority."
  }
}
