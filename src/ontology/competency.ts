import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { createHash } from "node:crypto"
import type { DatasetCore } from "@rdfjs/types"
import { Effect } from "effect"
import { iceError, type IceError } from "../errors.ts"
import { Workspace } from "../workspace.ts"
import { isSafeArtifactPath } from "./core.ts"
import { queryRdfDataset } from "./sparql.ts"

/** The only repository path accepted by the competency-suite loader. */
export const ONTOLOGY_COMPETENCY_SUITE_RELPATH =
  "ontology/research-competency-questions.json"

const MAX_SUITE_BYTES = 512n * 1024n
const MIN_CASES = 1
const MAX_CASES = 64
const MAX_QUERY_CHARACTERS = 16 * 1024

export interface OntologyCompetencyQuestionCase {
  readonly id: string
  readonly question: string
  readonly query: string
  readonly expected_boolean: boolean
  readonly rationale: string
}

export interface OntologyCompetencySuite {
  readonly schema: "ice-ontology-competency-suite/v1"
  readonly id: string
  readonly title: string
  readonly description: string
  readonly version: string
  readonly cases: ReadonlyArray<OntologyCompetencyQuestionCase>
  readonly guidance: ReadonlyArray<string>
}

export interface LoadedOntologyCompetencySuite {
  readonly suite: OntologyCompetencySuite
  readonly provenance: {
    readonly path: typeof ONTOLOGY_COMPETENCY_SUITE_RELPATH
    readonly sha256: string
    readonly byte_length: number
  }
}

export interface OntologyCompetencyReport {
  readonly schema: "ice-ontology-competency-report/v1"
  readonly suite: {
    readonly id: string
    readonly version: string
    readonly path: string
    readonly sha256: string
    readonly byte_length: number
  }
  readonly total_cases: number
  readonly passed_cases: number
  readonly failed_cases: number
  readonly passed: boolean
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly question: string
    readonly expected_boolean: boolean
    readonly observed_boolean: boolean
    readonly passed: boolean
  }>
  readonly guidance: ReadonlyArray<string>
}

export class OntologyCompetencySuiteError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "OntologyCompetencySuiteError"
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
    throw new OntologyCompetencySuiteError(
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
    throw new OntologyCompetencySuiteError(
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
    throw new OntologyCompetencySuiteError(
      `${label}.${field} must contain from 1 through ${maximumItems} strings`
    )
  }
  const result = value.map((item, index) => {
    if (typeof item !== "string" || item.trim().length === 0 || item.length > maximumLength) {
      throw new OntologyCompetencySuiteError(
        `${label}.${field}[${index}] must be a non-empty string of at most ${maximumLength} characters`
      )
    }
    return item.trim()
  })
  if (new Set(result).size !== result.length) {
    throw new OntologyCompetencySuiteError(`${label}.${field} must not contain duplicates`)
  }
  return result
}

const parseCase = (value: unknown, index: number): OntologyCompetencyQuestionCase => {
  const label = `cases[${index}]`
  const record = asRecord(value)
  if (record === undefined) {
    throw new OntologyCompetencySuiteError(`${label} must be an object`)
  }
  rejectUnknownFields(
    record,
    ["id", "question", "query", "expected_boolean", "rationale"],
    label
  )
  const id = requiredString(record, "id", label, 128)
  if (!/^[a-z][a-z0-9-]*$/.test(id)) {
    throw new OntologyCompetencySuiteError(
      `${label}.id must use lowercase letters, digits, and hyphens`
    )
  }
  const expected = record.expected_boolean
  if (typeof expected !== "boolean") {
    throw new OntologyCompetencySuiteError(`${label}.expected_boolean must be boolean`)
  }
  return {
    id,
    question: requiredString(record, "question", label, 1_500),
    query: requiredString(record, "query", label, MAX_QUERY_CHARACTERS),
    expected_boolean: expected,
    rationale: requiredString(record, "rationale", label, 1_500)
  }
}

/** Parses a versioned, fixed-shape suite of bounded graph competency questions. */
export const decodeOntologyCompetencySuite = (
  source: string,
  label = ONTOLOGY_COMPETENCY_SUITE_RELPATH
): OntologyCompetencySuite => {
  let parsed: unknown
  try {
    parsed = JSON.parse(source) as unknown
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    throw new OntologyCompetencySuiteError(`${label} is not valid JSON: ${message}`)
  }
  const record = asRecord(parsed)
  if (record === undefined) {
    throw new OntologyCompetencySuiteError(`${label} must be a JSON object`)
  }
  rejectUnknownFields(
    record,
    ["schema", "id", "title", "description", "version", "cases", "guidance"],
    label
  )
  if (record.schema !== "ice-ontology-competency-suite/v1") {
    throw new OntologyCompetencySuiteError(
      `${label}.schema must be 'ice-ontology-competency-suite/v1'`
    )
  }
  const cases = record.cases
  if (!Array.isArray(cases) || cases.length < MIN_CASES || cases.length > MAX_CASES) {
    throw new OntologyCompetencySuiteError(
      `${label}.cases must contain from ${MIN_CASES} through ${MAX_CASES} cases`
    )
  }
  const parsedCases = cases.map(parseCase)
  if (new Set(parsedCases.map(({ id }) => id)).size !== parsedCases.length) {
    throw new OntologyCompetencySuiteError(`${label}.cases must have unique ids`)
  }
  return {
    schema: "ice-ontology-competency-suite/v1",
    id: requiredString(record, "id", label, 128),
    title: requiredString(record, "title", label, 500),
    description: requiredString(record, "description", label, 1_500),
    version: requiredString(record, "version", label, 128),
    cases: parsedCases,
    guidance: stringArray(record, "guidance", label, 16, 1_500)
  }
}

const suiteFailure = (message: string): IceError =>
  iceError("ONTOLOGY_COMPETENCY_SUITE_READ_FAILED", message, 2)

/** Reads only the repository's fixed, safe, versioned competency suite. */
export const loadOntologyCompetencySuite = Effect.gen(function* () {
  const workspace = yield* Workspace
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  const root = yield* fs.realPath(workspace.root).pipe(
    Effect.mapError((error) => suiteFailure(`cannot resolve workspace root: ${String(error)}`))
  )
  const requested = path.resolve(workspace.root, ONTOLOGY_COMPETENCY_SUITE_RELPATH)
  const realPath = yield* fs.realPath(requested).pipe(
    Effect.mapError((error) =>
      suiteFailure(`cannot resolve ${ONTOLOGY_COMPETENCY_SUITE_RELPATH}: ${String(error)}`)
    )
  )
  const relative = path.relative(root, realPath)
  if (relative !== ONTOLOGY_COMPETENCY_SUITE_RELPATH || !isSafeArtifactPath(relative)) {
    return yield* Effect.fail(
      suiteFailure(`${ONTOLOGY_COMPETENCY_SUITE_RELPATH} must resolve inside the workspace`)
    )
  }
  const info = yield* fs.stat(realPath).pipe(
    Effect.mapError((error) => suiteFailure(`cannot inspect competency suite: ${String(error)}`))
  )
  if (info.type !== "File" || info.size > MAX_SUITE_BYTES) {
    return yield* Effect.fail(
      suiteFailure(
        `${ONTOLOGY_COMPETENCY_SUITE_RELPATH} must be a file no larger than ${String(MAX_SUITE_BYTES)} bytes`
      )
    )
  }
  const source = yield* fs.readFileString(realPath).pipe(
    Effect.mapError((error) => suiteFailure(`cannot read competency suite: ${String(error)}`))
  )
  let suite: OntologyCompetencySuite
  try {
    suite = decodeOntologyCompetencySuite(source)
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    return yield* Effect.fail(suiteFailure(message))
  }
  return {
    suite,
    provenance: {
      path: ONTOLOGY_COMPETENCY_SUITE_RELPATH,
      sha256: createHash("sha256").update(source).digest("hex"),
      byte_length: new TextEncoder().encode(source).byteLength
    }
  } satisfies LoadedOntologyCompetencySuite
})

/**
 * Evaluates only ASK questions against an already-built local RDF dataset.
 * The result reports graph-query regression, not scientific truth.
 */
export const evaluateOntologyCompetencySuite = async (
  dataset: DatasetCore,
  loaded: LoadedOntologyCompetencySuite
): Promise<OntologyCompetencyReport> => {
  const outcomes = []
  for (const entry of loaded.suite.cases) {
    let result
    try {
      result = await queryRdfDataset(dataset, entry.query, { limit: 1 })
    } catch (error) {
      throw new OntologyCompetencySuiteError(
        `competency case '${entry.id}' failed to execute: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
    if (result.form !== "ASK" || result.result === undefined || !("boolean" in result.result)) {
      throw new OntologyCompetencySuiteError(
        `competency case '${entry.id}' must use an ASK query`
      )
    }
    const observed = result.result.boolean
    outcomes.push({
      id: entry.id,
      question: entry.question,
      expected_boolean: entry.expected_boolean,
      observed_boolean: observed,
      passed: observed === entry.expected_boolean
    })
  }
  const passedCases = outcomes.filter(({ passed }) => passed).length
  return {
    schema: "ice-ontology-competency-report/v1",
    suite: {
      id: loaded.suite.id,
      version: loaded.suite.version,
      path: loaded.provenance.path,
      sha256: loaded.provenance.sha256,
      byte_length: loaded.provenance.byte_length
    },
    total_cases: outcomes.length,
    passed_cases: passedCases,
    failed_cases: outcomes.length - passedCases,
    passed: passedCases === outcomes.length,
    cases: outcomes,
    guidance: [
      "This checks predeclared bounded graph questions against the supplied local RDF dataset.",
      "A passing report does not validate scientific truth or authorize research execution."
    ]
  }
}
