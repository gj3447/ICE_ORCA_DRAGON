/**
 * Bounded LLM proposal format for a reviewed research state.
 *
 * A proposal may arrange named state objects into hypotheses and a next test.
 * It cannot create an object, promote an epistemic status, or serve as a
 * scientific verdict.  The parser is intentionally independent from the LLM
 * transport so the same boundary applies to every model provider.
 */
import type { ResearchObject, ResearchState } from "./state.ts"

export type ProposalStatus = "HYPOTHESIS" | "QUESTION"

export interface ResearchProposalConnection {
  readonly premises: readonly string[]
  readonly conclusion: string
  readonly explanation: string
  readonly assumptions: readonly string[]
  readonly falsifier: string
  readonly status: ProposalStatus
}

export interface ResearchProposal {
  readonly schema: "ice-research-proposal/v1"
  readonly state_id: string
  readonly summary: string
  readonly connections: readonly ResearchProposalConnection[]
  readonly next_test: {
    readonly question: string
    readonly inputs: readonly string[]
    readonly missing: readonly string[]
    readonly falsifier: string
    readonly consumer: string
    readonly non_claim: string
  }
  readonly reading_order: readonly string[]
}

const schemaObject = (properties: Record<string, unknown>, required: readonly string[]): Record<string, unknown> => ({
  type: "object",
  additionalProperties: false,
  required,
  properties
})

const stringSchema = (maxLength: number): Record<string, unknown> => ({ type: "string", minLength: 1, maxLength })
const idSchema: Record<string, unknown> = { type: "string", minLength: 1, maxLength: 96, pattern: "^[A-Za-z][A-Za-z0-9_.:-]{0,95}$" }
const idsSchema = (minimum: number, maximum: number, itemSchema: Record<string, unknown> = idSchema): Record<string, unknown> => ({
  // Provider schema omits uniqueItems; the local parser enforces uniqueness.
  type: "array", minItems: minimum, maxItems: maximum, items: itemSchema
})

const proposalSchema = (state?: ResearchState): Record<string, unknown> => {
  const stateObjectIds: Record<string, unknown> = state === undefined
    ? idSchema
    : { type: "string", enum: state.objects.map((object) => object.id) }
  const stateId: Record<string, unknown> = state === undefined
    ? stringSchema(96)
    : { type: "string", const: state.id }
  return schemaObject({
  schema: { type: "string", const: "ice-research-proposal/v1" },
  state_id: stateId,
  summary: stringSchema(2_000),
  connections: {
    type: "array", minItems: 1, maxItems: 4,
    items: schemaObject({
      premises: idsSchema(2, 8, stateObjectIds),
      conclusion: stringSchema(1_000),
      explanation: stringSchema(2_000),
      assumptions: idsSchema(0, 8, stateObjectIds),
      falsifier: stringSchema(2_000),
      status: { type: "string", enum: ["HYPOTHESIS", "QUESTION"] }
    }, ["premises", "conclusion", "explanation", "assumptions", "falsifier", "status"])
  },
  next_test: schemaObject({
    question: stringSchema(2_000),
    inputs: idsSchema(1, 8, stateObjectIds),
    missing: idsSchema(0, 8, stateObjectIds),
    falsifier: stringSchema(2_000),
    consumer: stateObjectIds,
    non_claim: stringSchema(2_000)
  }, ["question", "inputs", "missing", "falsifier", "consumer", "non_claim"]),
  reading_order: idsSchema(1, 12, stateObjectIds)
}, ["schema", "state_id", "summary", "connections", "next_test", "reading_order"])
}

/** Strict JSON-schema used only when no reviewed state has been loaded. */
export const proposalJsonSchema: Record<string, unknown> = proposalSchema()

/** Provider generation schema bound to one reviewed state and its known IDs. */
export const proposalJsonSchemaForState = (state: ResearchState): Record<string, unknown> => proposalSchema(state)

const record = (value: unknown, label: string): Record<string, unknown> => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new Error(`${label} must be an object`)
  return value as Record<string, unknown>
}

const exactKeys = (value: Record<string, unknown>, keys: readonly string[], label: string): void => {
  const actual = Object.keys(value)
  if (actual.length !== keys.length || actual.some((key) => !keys.includes(key))) throw new Error(`${label} has unknown or missing fields`)
}

const text = (value: unknown, label: string, maximum: number): string => {
  if (typeof value !== "string" || !value.trim() || value.length > maximum) throw new Error(`${label} must be non-empty and at most ${maximum} characters`)
  return value
}

const proposalId = (value: unknown, label: string): string => {
  const parsed = text(value, label, 96)
  if (!/^[A-Za-z][A-Za-z0-9_.:-]{0,95}$/.test(parsed)) throw new Error(`${label} must be a known state object id`)
  return parsed
}

const objectIds = (value: unknown, label: string, known: ReadonlySet<string>, minimum: number, maximum: number): readonly string[] => {
  if (!Array.isArray(value) || value.length < minimum || value.length > maximum) throw new Error(`${label} must contain ${minimum}–${maximum} entries`)
  const parsed = value.map((entry, index) => proposalId(entry, `${label}[${index}]`))
  if (new Set(parsed).size !== parsed.length) throw new Error(`${label} must not repeat object ids`)
  for (const entry of parsed) if (!known.has(entry)) throw new Error(`${label} references an invented or unknown state object '${entry}'`)
  return parsed
}

const unavailable = new Set(["missing", "unknown", "refuted", "withdrawn"])

/** Parse a model response against the supplied, immutable research state. */
export const parseResearchProposal = (value: unknown, state: ResearchState): ResearchProposal => {
  const root = record(value, "proposal")
  exactKeys(root, ["schema", "state_id", "summary", "connections", "next_test", "reading_order"], "proposal")
  if (root.schema !== "ice-research-proposal/v1") throw new Error("proposal schema must be ice-research-proposal/v1")
  if (root.state_id !== state.id) throw new Error("proposal state_id must exactly match the reviewed state")
  const known = new Set(state.objects.map((object) => object.id))
  const summary = text(root.summary, "proposal.summary", 2_000)
  if (!Array.isArray(root.connections) || root.connections.length < 1 || root.connections.length > 4) throw new Error("proposal.connections must contain 1–4 entries")
  const connections = root.connections.map((entry, index): ResearchProposalConnection => {
    const connection = record(entry, `proposal.connections[${index}]`)
    exactKeys(connection, ["premises", "conclusion", "explanation", "assumptions", "falsifier", "status"], `proposal.connections[${index}]`)
    const status = connection.status
    if (status !== "HYPOTHESIS" && status !== "QUESTION") throw new Error(`proposal.connections[${index}].status must be HYPOTHESIS or QUESTION`)
    return {
      premises: objectIds(connection.premises, `proposal.connections[${index}].premises`, known, 2, 8),
      conclusion: text(connection.conclusion, `proposal.connections[${index}].conclusion`, 1_000),
      explanation: text(connection.explanation, `proposal.connections[${index}].explanation`, 2_000),
      assumptions: objectIds(connection.assumptions, `proposal.connections[${index}].assumptions`, known, 0, 8),
      falsifier: text(connection.falsifier, `proposal.connections[${index}].falsifier`, 2_000),
      status
    }
  })
  const test = record(root.next_test, "proposal.next_test")
  exactKeys(test, ["question", "inputs", "missing", "falsifier", "consumer", "non_claim"], "proposal.next_test")
  const missing = objectIds(test.missing, "proposal.next_test.missing", known, 0, 8)
  const objects = new Map(state.objects.map((object) => [object.id, object] as const))
  for (const objectId of missing) {
    const object = objects.get(objectId)
    if (object === undefined || !unavailable.has(object.status)) {
      throw new Error(`proposal.next_test.missing '${objectId}' must name a missing, unknown, refuted, or withdrawn state object`)
    }
  }
  const proposal: ResearchProposal = {
    schema: "ice-research-proposal/v1",
    state_id: state.id,
    summary,
    connections,
    next_test: {
      question: text(test.question, "proposal.next_test.question", 2_000),
      inputs: objectIds(test.inputs, "proposal.next_test.inputs", known, 1, 8),
      missing,
      falsifier: text(test.falsifier, "proposal.next_test.falsifier", 2_000),
      consumer: proposalId(test.consumer, "proposal.next_test.consumer"),
      non_claim: text(test.non_claim, "proposal.next_test.non_claim", 2_000)
    },
    reading_order: objectIds(root.reading_order, "proposal.reading_order", known, 1, 12)
  }
  if (!known.has(proposal.next_test.consumer)) throw new Error("proposal.next_test.consumer references an invented or unknown state object")
  const total = [proposal.summary, ...proposal.connections.flatMap((item) => [item.conclusion, item.explanation, item.falsifier]),
    proposal.next_test.question, proposal.next_test.falsifier, proposal.next_test.non_claim].reduce((sum, item) => sum + item.length, 0)
  if (total > 12_000) throw new Error("proposal textual output exceeds 12000 characters")
  return proposal
}

const byId = (state: ResearchState, id: string): ResearchObject => {
  const object = state.objects.find((candidate) => candidate.id === id)
  if (object === undefined) throw new Error(`state object '${id}' disappeared after proposal validation`)
  return object
}

const sourceLinks = (state: ResearchState, object: ResearchObject, root?: string): string => object.sources.map((sourceId) => {
  const source = state.sources.find((candidate) => candidate.id === sourceId)
  if (source === undefined) throw new Error(`state source '${sourceId}' disappeared after proposal validation`)
  const target = root === undefined ? source.path : `${root}/${source.path}`
  return `[${source.id}](${target})`
}).join(", ")

const objectLine = (state: ResearchState, id: string, root?: string): string => {
  const object = byId(state, id)
  return `\`${object.id}\` — ${object.label} (${object.status}; ${sourceLinks(state, object, root)})`
}

/** Korean human projection. It exposes every premise, assumption and source. */
export const renderResearchProposal = (proposal: ResearchProposal, state: ResearchState, root?: string): string => {
  const checked = parseResearchProposal(proposal, state)
  // A model may omit an unavailable input from its descriptive `missing`
  // field.  The reviewed state remains authoritative about availability.
  const stateUnavailableInputs = [...new Set([
    ...checked.next_test.missing,
    ...checked.next_test.inputs.filter((id) => unavailable.has(byId(state, id).status))
  ])]
  const lines = [
    "# HSWM 연구 제안",
    "",
    `상태: \`${checked.state_id}\` · 범위: \`${state.scope}\``,
    "",
    "## 요약",
    "",
    checked.summary,
    "",
    "## 연결",
    ""
  ]
  for (const [index, connection] of checked.connections.entries()) {
    lines.push(`### ${index + 1}. ${connection.status}`, "", "전제 (모두 함께 필요):", "")
    lines.push(...connection.premises.map((id) => `- ${objectLine(state, id, root)}`))
    lines.push("", `결론: ${connection.conclusion}`, "", `설명: ${connection.explanation}`, "", "가정:", "")
    lines.push(...(connection.assumptions.length === 0 ? ["- 선언된 추가 가정 없음"] : connection.assumptions.map((id) => `- ${objectLine(state, id, root)}`)))
    lines.push("", `반증 조건: ${connection.falsifier}`, "")
  }
  lines.push("## 다음 제한 검사", "", `질문: ${checked.next_test.question}`, "", "입력:", "")
  lines.push(...checked.next_test.inputs.map((id) => `- ${objectLine(state, id, root)}`))
  lines.push("", "원본 상태에서 미확보인 검사 입력:", "")
  lines.push(...(stateUnavailableInputs.length === 0 ? ["- 없음"] : stateUnavailableInputs.map((id) => `- ${objectLine(state, id, root)}`)))
  lines.push("", `반증 조건: ${checked.next_test.falsifier}`, "", `소비자: ${objectLine(state, checked.next_test.consumer, root)}`, "", `이 제안만으로 하지 않는 주장: ${checked.next_test.non_claim}`, "", "## 읽기 순서", "")
  lines.push(...checked.reading_order.map((id, index) => `${index + 1}. ${objectLine(state, id, root)}`))
  return `${lines.join("\n")}\n`
}
