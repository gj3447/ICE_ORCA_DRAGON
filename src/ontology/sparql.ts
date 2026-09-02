import { QueryEngine } from "@comunica/query-sparql-rdfjs"
import type { Bindings, DatasetCore, Quad, Term } from "@rdfjs/types"
import { Parser } from "sparqljs"
import type { Pattern, Query, SparqlQuery, Triple } from "sparqljs"
import { serializeQuadsAsNQuads } from "./rdf.ts"

export type SparqlQueryForm = "SELECT" | "ASK" | "CONSTRUCT" | "DESCRIBE"

export interface SparqlJsonTerm {
  readonly type: "uri" | "bnode" | "literal"
  readonly value: string
  readonly "xml:lang"?: string
  readonly datatype?: string
}

export interface SparqlSelectJson {
  readonly head: { readonly vars: ReadonlyArray<string> }
  readonly results: {
    readonly bindings: ReadonlyArray<Readonly<Record<string, SparqlJsonTerm>>>
  }
}

export interface SparqlAskJson {
  readonly head: Readonly<Record<string, never>>
  readonly boolean: boolean
}

export interface SparqlResult {
  readonly schema: "ice-ontology-sparql-result/v1"
  readonly form: SparqlQueryForm
  readonly media_type: "application/sparql-results+json" | "application/n-quads"
  readonly row_count: number
  readonly truncated: boolean
  readonly result?: SparqlSelectJson | SparqlAskJson
  readonly nquads?: string
}

export interface SparqlQueryOptions {
  readonly limit?: number
  readonly timeoutMs?: number
  readonly maximumResultBytes?: number
}

const MAX_QUERY_CHARACTERS = 16 * 1024
const MAX_RESULT_ROWS = 500
const MAX_RESULT_BYTES = 1024 * 1024
const MAX_TIMEOUT_MS = 30_000
const MAX_TRIPLES = 12
const MAX_GRAPH_NESTING = 2
const MAX_DESCRIBE_TERMS = 4
const MAX_DISTINCT_VARIABLES = 24

const isVariableTerm = (value: unknown): boolean =>
  typeof value === "object" && value !== null && "termType" in value && value.termType === "Variable"

const isExplicitDescribeTerm = (value: unknown): boolean =>
  typeof value === "object" &&
  value !== null &&
  "termType" in value &&
  (value.termType === "NamedNode" || value.termType === "Variable")

const assertPlainTriple = (triple: Triple): void => {
  if (!("termType" in triple.predicate)) {
    throw new Error("SPARQL property paths are not allowed in the local subset")
  }
}

interface PatternBudget {
  triples: number
  readonly variables: Set<string>
  readonly variableSets: Array<Set<string>>
}

const variableName = (value: unknown): string | undefined =>
  typeof value === "object" &&
  value !== null &&
  "termType" in value &&
  value.termType === "Variable" &&
  "value" in value &&
  typeof value.value === "string"
    ? value.value
    : undefined

const recordTriple = (
  triple: Triple,
  graphVariables: ReadonlyArray<string>,
  budget: PatternBudget
): void => {
  assertPlainTriple(triple)
  budget.triples += 1
  if (budget.triples > MAX_TRIPLES) {
    throw new Error(`SPARQL query exceeds ${MAX_TRIPLES} triple patterns`)
  }
  const variables = new Set(
    [
      variableName(triple.subject),
      variableName(triple.predicate),
      variableName(triple.object),
      ...graphVariables
    ].filter((value): value is string => value !== undefined)
  )
  for (const variable of variables) budget.variables.add(variable)
  if (budget.variables.size > MAX_DISTINCT_VARIABLES) {
    throw new Error(`SPARQL query exceeds ${MAX_DISTINCT_VARIABLES} distinct variables`)
  }
  if (variables.size > 0) budget.variableSets.push(variables)
}

const inspectPatterns = (
  patterns: ReadonlyArray<Pattern> | undefined,
  budget: PatternBudget,
  depth = 0,
  graphVariables: ReadonlyArray<string> = []
): void => {
  if (depth > MAX_GRAPH_NESTING) {
    throw new Error(`SPARQL graph nesting exceeds ${MAX_GRAPH_NESTING}`)
  }
  for (const pattern of patterns ?? []) {
    if (pattern.type === "bgp") {
      for (const triple of pattern.triples) {
        recordTriple(triple, graphVariables, budget)
      }
      continue
    }
    if (pattern.type === "graph") {
      const graphVariable = variableName(pattern.name)
      inspectPatterns(
        pattern.patterns,
        budget,
        depth + 1,
        graphVariable === undefined
          ? graphVariables
          : [...graphVariables, graphVariable]
      )
      continue
    }
    if (pattern.type === "group") {
      inspectPatterns(pattern.patterns, budget, depth + 1, graphVariables)
      continue
    }
    throw new Error(
      `SPARQL pattern '${pattern.type}' is not allowed in the bounded local subset`
    )
  }
}

const assertConnectedJoins = (variableSets: ReadonlyArray<Set<string>>): void => {
  const [first, ...rest] = variableSets
  if (first === undefined) return
  const connected = new Set(first)
  const pending = [...rest]
  while (pending.length > 0) {
    const index = pending.findIndex((variables) =>
      [...variables].some((variable) => connected.has(variable))
    )
    if (index < 0) {
      throw new Error(
        "SPARQL disconnected variable joins are not allowed in the bounded local subset"
      )
    }
    const [next] = pending.splice(index, 1)
    for (const variable of next ?? []) connected.add(variable)
  }
}

const parseBoundedLocalQuery = (source: string): Query => {
  let parsed: SparqlQuery
  try {
    parsed = new Parser().parse(source)
  } catch (error) {
    throw new Error(`invalid SPARQL query: ${error instanceof Error ? error.message : String(error)}`)
  }
  if (parsed.type !== "query") {
    throw new Error("SPARQL update operations are not allowed")
  }
  if (parsed.base !== undefined || parsed.from !== undefined || parsed.values !== undefined) {
    throw new Error("SPARQL BASE, dataset clauses, and VALUES are not allowed in the local subset")
  }
  const budget: PatternBudget = {
    triples: 0,
    variables: new Set<string>(),
    variableSets: []
  }
  inspectPatterns(parsed.where, budget)
  assertConnectedJoins(budget.variableSets)
  if (parsed.queryType === "SELECT") {
    if (!parsed.variables.every(isVariableTerm)) {
      throw new Error("SPARQL expression projections are not allowed in the local subset")
    }
    if (
      parsed.group !== undefined ||
      parsed.having !== undefined ||
      parsed.order !== undefined ||
      parsed.limit !== undefined ||
      parsed.offset !== undefined
    ) {
      throw new Error("SPARQL grouping, ordering, and query-side pagination are not allowed in the local subset")
    }
  }
  if (parsed.queryType === "CONSTRUCT") {
    const template = parsed.template ?? []
    for (const triple of template) assertPlainTriple(triple)
    if (template.length > MAX_TRIPLES) {
      throw new Error(`SPARQL CONSTRUCT template exceeds ${MAX_TRIPLES} triples`)
    }
  }
  if (parsed.queryType === "DESCRIBE") {
    if (
      parsed.variables.length > MAX_DESCRIBE_TERMS ||
      parsed.variables.some((term) => !isExplicitDescribeTerm(term))
    ) {
      throw new Error(`SPARQL DESCRIBE accepts at most ${MAX_DESCRIBE_TERMS} explicit terms`)
    }
  }
  return parsed
}

const jsonTerm = (term: Term): SparqlJsonTerm => {
  if (term.termType === "NamedNode") return { type: "uri", value: term.value }
  if (term.termType === "BlankNode") return { type: "bnode", value: term.value }
  if (term.termType === "Literal") {
    return term.language.length > 0
      ? { type: "literal", value: term.value, "xml:lang": term.language }
      : { type: "literal", value: term.value, datatype: term.datatype.value }
  }
  throw new Error(`SPARQL result contains unsupported RDF term '${term.termType}'`)
}

const byteLength = (value: unknown): number =>
  Buffer.byteLength(JSON.stringify(value), "utf8")

const queryBounds = (
  limitOrOptions: number | SparqlQueryOptions
): Required<SparqlQueryOptions> => {
  const options = typeof limitOrOptions === "number"
    ? { limit: limitOrOptions }
    : limitOrOptions
  const limit = options.limit ?? 100
  const timeoutMs = options.timeoutMs ?? 5_000
  const maximumResultBytes = options.maximumResultBytes ?? MAX_RESULT_BYTES
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > MAX_RESULT_ROWS) {
    throw new Error(`SPARQL result limit must be an integer from 1 through ${MAX_RESULT_ROWS}`)
  }
  if (
    !Number.isSafeInteger(timeoutMs) ||
    timeoutMs < 1 ||
    timeoutMs > MAX_TIMEOUT_MS
  ) {
    throw new Error(`SPARQL timeout must be an integer from 1 through ${MAX_TIMEOUT_MS} milliseconds`)
  }
  if (
    !Number.isSafeInteger(maximumResultBytes) ||
    maximumResultBytes < 256 ||
    maximumResultBytes > MAX_RESULT_BYTES
  ) {
    throw new Error(`SPARQL result byte limit must be an integer from 256 through ${MAX_RESULT_BYTES}`)
  }
  return { limit, timeoutMs, maximumResultBytes }
}

const withTimeout = async <T>(
  milliseconds: number,
  operation: (signal: AbortSignal) => Promise<T>
): Promise<T> => {
  const controller = new AbortController()
  let timer: ReturnType<typeof setTimeout> | undefined
  const timeout = new Promise<never>((_resolve, reject) => {
    timer = setTimeout(() => {
      controller.abort()
      reject(new Error(`SPARQL query exceeded ${milliseconds} milliseconds`))
    }, milliseconds)
  })
  try {
    return await Promise.race([operation(controller.signal), timeout])
  } finally {
    if (timer !== undefined) clearTimeout(timer)
    controller.abort()
  }
}

const bindingJson = (
  binding: Bindings
): Readonly<Record<string, SparqlJsonTerm>> =>
  Object.fromEntries(
    [...binding]
      .map(([variable, term]) => [variable.value, jsonTerm(term)] as const)
      .sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0)
  )

/**
 * Execute a bounded SPARQL 1.1 query against one in-memory RDF/JS Dataset.
 * Remote dataset clauses, SERVICE, and every update form are rejected before
 * Comunica sees the query.
 */
export const queryRdfDataset = async (
  dataset: DatasetCore,
  query: string,
  limitOrOptions: number | SparqlQueryOptions = {}
): Promise<SparqlResult> => {
  if (query.length === 0 || query.length > MAX_QUERY_CHARACTERS) {
    throw new Error(`SPARQL query must contain from 1 through ${MAX_QUERY_CHARACTERS} characters`)
  }
  const parsed = parseBoundedLocalQuery(query)
  const form = parsed.queryType as SparqlQueryForm
  const bounds = queryBounds(limitOrOptions)
  return withTimeout(bounds.timeoutMs, async (signal) => {
    const engine = new QueryEngine()
    const context = {
      sources: [dataset],
      unionDefaultGraph: false,
      httpAbortSignal: signal
    }
    const result = await engine.query(query, context)
    if (result.resultType === "void") {
      throw new Error("SPARQL update operations are not allowed")
    }
    if (form === "ASK") {
      if (result.resultType !== "boolean") {
        throw new Error("SPARQL query form does not match its parsed result type")
      }
      return {
        schema: "ice-ontology-sparql-result/v1",
        form,
        media_type: "application/sparql-results+json",
        row_count: 1,
        truncated: false,
        result: { head: {}, boolean: await result.execute() }
      }
    }
    if (form === "SELECT") {
      if (result.resultType !== "bindings") {
        throw new Error("SPARQL query form does not match its parsed result type")
      }
      const metadata = await result.metadata()
      const stream = await result.execute()
      const bindings: Array<Readonly<Record<string, SparqlJsonTerm>>> = []
      let bytes = 0
      let truncated = false
      for await (const binding of stream) {
        const encoded = bindingJson(binding)
        const nextBytes = bytes + byteLength(encoded)
        if (
          bindings.length >= bounds.limit ||
          nextBytes > bounds.maximumResultBytes
        ) {
          truncated = true
          break
        }
        bindings.push(encoded)
        bytes = nextBytes
      }
      return {
        schema: "ice-ontology-sparql-result/v1",
        form,
        media_type: "application/sparql-results+json",
        row_count: bindings.length,
        truncated,
        result: {
          head: { vars: metadata.variables.map(({ value }) => value) },
          results: { bindings }
        }
      }
    }
    if (result.resultType !== "quads") {
      throw new Error("SPARQL query form does not match its parsed result type")
    }
    const stream = await result.execute()
    const quads: Array<Quad> = []
    let truncated = false
    for await (const quad of stream) {
      if (quads.length >= bounds.limit) {
        truncated = true
        break
      }
      const candidate = [...quads, quad]
      if (
        Buffer.byteLength(serializeQuadsAsNQuads(candidate), "utf8") >
        bounds.maximumResultBytes
      ) {
        truncated = true
        break
      }
      quads.push(quad)
    }
    return {
      schema: "ice-ontology-sparql-result/v1",
      form,
      media_type: "application/n-quads",
      row_count: quads.length,
      truncated,
      nquads: serializeQuadsAsNQuads(quads)
    }
  })
}
