import { readFile, realpath } from "node:fs/promises"
import { relative, resolve } from "node:path"
import { Readable } from "node:stream"
import ParserN3 from "@rdfjs/parser-n3"
import type { DatasetCore, Stream as RdfStream, Term } from "@rdfjs/types"
import SHACLValidator from "rdf-validate-shacl"
import rdf from "rdf-ext"
import type { QuadExt } from "rdf-ext/lib/Quad.js"

export const SHACL_SHAPES_RELPATH =
  "ontology/standards/research-graph-shapes.ttl"

export interface ShaclViolation {
  readonly focus_node: string
  readonly path: string
  readonly constraint: string
  readonly source_shape: string
  readonly severity: string
  readonly value: string
  readonly message: ReadonlyArray<string>
}

export interface ShaclReport {
  readonly schema: "ice-ontology-shacl-report/v1"
  readonly conforms: boolean
  readonly violations: ReadonlyArray<ShaclViolation>
}

const termValue = (term: Term | undefined): string => term?.value ?? ""

const lexicalCompare = (left: string, right: string): number =>
  left < right ? -1 : left > right ? 1 : 0

const collectStream = async (
  stream: RdfStream<QuadExt>
): Promise<ReadonlyArray<QuadExt>> =>
  new Promise((resolveStream, reject) => {
    const values: Array<QuadExt> = []
    stream.on("data", (quad: QuadExt) => values.push(quad))
    stream.on("error", reject)
    stream.on("end", () => resolveStream(values))
  })

export const parseTurtleDataset = async (
  source: string
): Promise<DatasetCore> => {
  const parsed = new ParserN3<QuadExt>({ factory: rdf }).import(
    Readable.from([source])
  )
  const dataset = rdf.dataset()
  for (const quad of await collectStream(parsed)) dataset.add(quad)
  return dataset
}

/** Read the checked-in shapes only if their real path remains in the workspace. */
export const loadStandardShaclShapesText = async (
  workspaceRoot: string
): Promise<string> => {
  const root = await realpath(workspaceRoot)
  const target = await realpath(resolve(root, SHACL_SHAPES_RELPATH))
  const contained = relative(root, target)
  if (contained.startsWith("..") || contained.startsWith("/")) {
    throw new Error("SHACL shapes path escapes workspace")
  }
  return readFile(target, "utf8")
}

export const loadStandardShaclShapes = async (
  workspaceRoot: string
): Promise<DatasetCore> =>
  parseTurtleDataset(await loadStandardShaclShapesText(workspaceRoot))

/** Deterministic projection QA; native ontology validation remains authoritative. */
export const validateRdfDatasetWithShacl = async (
  data: DatasetCore,
  shapes: DatasetCore
): Promise<ShaclReport> => {
  const validation = await new SHACLValidator(shapes).validate(data)
  const violations = validation.results.map((result): ShaclViolation => ({
    focus_node: termValue(result.focusNode),
    path: termValue(result.path),
    constraint: termValue(result.sourceConstraintComponent),
    source_shape: termValue(result.sourceShape),
    severity: termValue(result.severity),
    value: termValue(result.value),
    message: result.message.map((message) => termValue(message)).sort(lexicalCompare)
  })).sort((left, right) =>
    lexicalCompare(
      `${left.focus_node}\u0000${left.path}\u0000${left.constraint}\u0000${left.value}`,
      `${right.focus_node}\u0000${right.path}\u0000${right.constraint}\u0000${right.value}`
    )
  )
  return {
    schema: "ice-ontology-shacl-report/v1",
    conforms: validation.conforms,
    violations
  }
}
