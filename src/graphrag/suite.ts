import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { createHash } from "node:crypto"
import { Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { Workspace } from "../workspace.ts"
import type { GraphRagEvalCase } from "./eval.ts"

export const GRAPH_RAG_EVAL_SUITE_RELPATH = "ontology/graphrag-evaluation-suite.json"
const MAX_SUITE_BYTES = 512n * 1024n
const MAX_CASES = 128

export interface GraphRagEvaluationSuiteCase extends GraphRagEvalCase {
  readonly rationale: string
}

export interface GraphRagEvaluationSuite {
  readonly schema: "ice-graphrag-evaluation-suite/v1"
  readonly id: string
  readonly title: string
  readonly description: string
  readonly version: string
  readonly cases: ReadonlyArray<GraphRagEvaluationSuiteCase>
  readonly guidance: ReadonlyArray<string>
}

export interface LoadedGraphRagEvaluationSuite {
  readonly suite: GraphRagEvaluationSuite
  readonly provenance: {
    readonly path: typeof GRAPH_RAG_EVAL_SUITE_RELPATH
    readonly sha256: string
    readonly byte_length: number
  }
}

export class GraphRagEvaluationSuiteError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "GraphRagEvaluationSuiteError"
  }
}

type JsonRecord = Readonly<Record<string, unknown>>

const asRecord = (value: unknown): JsonRecord | undefined =>
  typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as JsonRecord)
    : undefined

const rejectUnknownFields = (
  record: JsonRecord,
  allowed: ReadonlyArray<string>,
  label: string
): void => {
  const unknown = Object.keys(record).filter((field) => !allowed.includes(field))
  if (unknown.length > 0) {
    throw new GraphRagEvaluationSuiteError(
      `${label} has unknown field(s): ${unknown.sort().join(", ")}`
    )
  }
}

const requiredString = (
  record: JsonRecord,
  field: string,
  label: string,
  maximum = 1_000
): string => {
  const value = record[field]
  if (typeof value !== "string" || value.trim().length === 0 || value.length > maximum) {
    throw new GraphRagEvaluationSuiteError(
      `${label}.${field} must be a non-empty string of at most ${maximum} characters`
    )
  }
  return value.trim()
}

const stringArray = (
  record: JsonRecord,
  field: string,
  label: string,
  maximumItems: number,
  maximumLength: number
): ReadonlyArray<string> => {
  const value = record[field]
  if (!Array.isArray(value) || value.length === 0 || value.length > maximumItems) {
    throw new GraphRagEvaluationSuiteError(
      `${label}.${field} must contain from 1 through ${maximumItems} strings`
    )
  }
  const result = value.map((item, index) => {
    if (typeof item !== "string" || item.trim().length === 0 || item.length > maximumLength) {
      throw new GraphRagEvaluationSuiteError(
        `${label}.${field}[${index}] must be a non-empty string of at most ${maximumLength} characters`
      )
    }
    return item.trim()
  })
  if (new Set(result).size !== result.length) {
    throw new GraphRagEvaluationSuiteError(`${label}.${field} must not contain duplicates`)
  }
  return result
}

const isQualifiedUnitId = (value: string): boolean =>
  /^[a-z0-9-]+::[a-z_]+:[A-Za-z0-9_.:-]+$/.test(value)

const parseCase = (value: unknown, index: number): GraphRagEvaluationSuiteCase => {
  const label = `cases[${index}]`
  const record = asRecord(value)
  if (record === undefined) {
    throw new GraphRagEvaluationSuiteError(`${label} must be an object`)
  }
  rejectUnknownFields(
    record,
    ["id", "query", "expected_unit_ids", "graph", "depth", "rationale"],
    label
  )
  const id = requiredString(record, "id", label, 128)
  if (!/^[a-z][a-z0-9-]*$/.test(id)) {
    throw new GraphRagEvaluationSuiteError(
      `${label}.id must use lowercase letters, digits, and hyphens`
    )
  }
  const expectedUnitIds = stringArray(record, "expected_unit_ids", label, 16, 512)
  for (const unitId of expectedUnitIds) {
    if (!isQualifiedUnitId(unitId)) {
      throw new GraphRagEvaluationSuiteError(
        `${label}.expected_unit_ids contains invalid graph-qualified unit id '${unitId}'`
      )
    }
  }
  const graph = record.graph
  if (graph !== undefined && (typeof graph !== "string" || !/^[a-z0-9-]{1,128}$/.test(graph))) {
    throw new GraphRagEvaluationSuiteError(
      `${label}.graph must be an omitted value or a registered-key-shaped string`
    )
  }
  const depthValue = record.depth
  if (
    depthValue !== undefined &&
    (typeof depthValue !== "number" ||
      !Number.isSafeInteger(depthValue) ||
      depthValue < 0 ||
      depthValue > 3)
  ) {
    throw new GraphRagEvaluationSuiteError(`${label}.depth must be an integer from 0 through 3`)
  }
  const depth = depthValue === undefined ? undefined : depthValue
  return {
    id,
    query: requiredString(record, "query", label, 500),
    expected_unit_ids: expectedUnitIds,
    ...(graph === undefined ? {} : { graph }),
    ...(depth === undefined ? {} : { depth }),
    rationale: requiredString(record, "rationale", label, 1_500)
  }
}

/** Parses a versioned, reviewable retrieval suite without accepting unknown shape. */
export const decodeGraphRagEvaluationSuite = (
  source: string,
  label = GRAPH_RAG_EVAL_SUITE_RELPATH
): GraphRagEvaluationSuite => {
  let parsed: unknown
  try {
    parsed = JSON.parse(source) as unknown
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    throw new GraphRagEvaluationSuiteError(`${label} is not valid JSON: ${message}`)
  }
  const record = asRecord(parsed)
  if (record === undefined) {
    throw new GraphRagEvaluationSuiteError(`${label} must be a JSON object`)
  }
  rejectUnknownFields(
    record,
    ["schema", "id", "title", "description", "version", "cases", "guidance"],
    label
  )
  if (record.schema !== "ice-graphrag-evaluation-suite/v1") {
    throw new GraphRagEvaluationSuiteError(
      `${label}.schema must be 'ice-graphrag-evaluation-suite/v1'`
    )
  }
  const cases = record.cases
  if (!Array.isArray(cases) || cases.length === 0 || cases.length > MAX_CASES) {
    throw new GraphRagEvaluationSuiteError(
      `${label}.cases must contain from 1 through ${MAX_CASES} cases`
    )
  }
  const parsedCases = cases.map(parseCase)
  if (new Set(parsedCases.map(({ id }) => id)).size !== parsedCases.length) {
    throw new GraphRagEvaluationSuiteError(`${label}.cases must have unique ids`)
  }
  return {
    schema: "ice-graphrag-evaluation-suite/v1",
    id: requiredString(record, "id", label, 128),
    title: requiredString(record, "title", label, 500),
    description: requiredString(record, "description", label, 1_500),
    version: requiredString(record, "version", label, 128),
    cases: parsedCases,
    guidance: stringArray(record, "guidance", label, 16, 1_500)
  }
}

const suiteFailure = (message: string): IceError =>
  iceError("GRAPH_RAG_EVAL_SUITE_READ_FAILED", message, 2)

/** Reads only the repository's fixed, safe, versioned standard evaluation suite. */
export const loadGraphRagEvaluationSuite = Effect.gen(function* () {
  const workspace = yield* Workspace
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  const root = yield* fs.realPath(workspace.root).pipe(
    Effect.mapError((error) => suiteFailure(`cannot resolve workspace root: ${String(error)}`))
  )
  const requested = path.resolve(workspace.root, GRAPH_RAG_EVAL_SUITE_RELPATH)
  const realPath = yield* fs.realPath(requested).pipe(
    Effect.mapError((error) =>
      suiteFailure(`cannot resolve ${GRAPH_RAG_EVAL_SUITE_RELPATH}: ${String(error)}`)
    )
  )
  const relative = path.relative(root, realPath)
  if (relative !== GRAPH_RAG_EVAL_SUITE_RELPATH || !isSafeArtifactPath(relative)) {
    return yield* Effect.fail(
      suiteFailure(`${GRAPH_RAG_EVAL_SUITE_RELPATH} must resolve inside the workspace`)
    )
  }
  const info = yield* fs.stat(realPath).pipe(
    Effect.mapError((error) => suiteFailure(`cannot inspect evaluation suite: ${String(error)}`))
  )
  if (info.type !== "File" || info.size > MAX_SUITE_BYTES) {
    return yield* Effect.fail(
      suiteFailure(
        `${GRAPH_RAG_EVAL_SUITE_RELPATH} must be a file no larger than ${String(MAX_SUITE_BYTES)} bytes`
      )
    )
  }
  const source = yield* fs.readFileString(realPath).pipe(
    Effect.mapError((error) => suiteFailure(`cannot read evaluation suite: ${String(error)}`))
  )
  let suite: GraphRagEvaluationSuite
  try {
    suite = decodeGraphRagEvaluationSuite(source)
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    return yield* Effect.fail(suiteFailure(message))
  }
  return {
    suite,
    provenance: {
      path: GRAPH_RAG_EVAL_SUITE_RELPATH,
      sha256: createHash("sha256").update(source).digest("hex"),
      byte_length: new TextEncoder().encode(source).byteLength
    }
  } satisfies LoadedGraphRagEvaluationSuite
})
