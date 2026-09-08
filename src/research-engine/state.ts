/**
 * A small, read-only projection of a reviewed research situation.  This is
 * deliberately not an ontology writer, a truth-maintenance system, or a
 * scientific verdict.  Its job is to make the roles in an n-ary research
 * relation visible to the HSWM router and to a human reader.
 */

export type ResearchObjectKind = "assumption" | "result" | "counterexample" | "missing_object" | "candidate"
export type ResearchObjectStatus = "established" | "candidate" | "missing" | "refuted" | "unknown" | "withdrawn"
export type ResearchLinkRelation = "requires" | "motivates" | "obstructs" | "analogy"
export type ResearchReadiness = "BLOCKED" | "CONDITIONAL" | "INPUTS_PRESENT"

export interface ResearchSource {
  readonly id: string
  readonly path: string
  readonly sha256: string
}

export interface ResearchObject {
  readonly id: string
  readonly kind: ResearchObjectKind
  readonly label: string
  readonly status: ResearchObjectStatus
  readonly summary: string
  readonly anchors: readonly string[]
  readonly sources: readonly string[]
}

export interface ResearchLinkInput {
  readonly role: string
  readonly object: string
}

export interface ResearchLink {
  readonly id: string
  readonly label: string
  readonly relation: ResearchLinkRelation
  readonly inputs: readonly ResearchLinkInput[]
  readonly output: string
  readonly explanation: string
  readonly falsifier: string
  readonly sources: readonly string[]
}

export interface ResearchState {
  readonly schema: "ice-research-state/v1"
  readonly id: string
  readonly target: string
  readonly scope: "SUPPORTING_METHOD"
  readonly question: string
  readonly sources: readonly ResearchSource[]
  readonly objects: readonly ResearchObject[]
  readonly links: readonly ResearchLink[]
  readonly routing: { readonly domain: string; readonly map: string; readonly obstruction: string }
}

export interface CompiledResearchLink extends ResearchLink {
  readonly readiness: ResearchReadiness
  readonly available: boolean
  readonly absent_inputs: readonly ResearchLinkInput[]
  /** The listed output remains the declared consumer; this never promotes it. */
  readonly output_status: ResearchObjectStatus
}

export interface ResearchRouterContext {
  readonly domain: "declared" | "missing" | "unknown"
  readonly map: "candidate" | "missing" | "unknown"
  readonly obstruction: "present" | "not_recorded" | "unknown"
}

export interface CompiledResearchState {
  readonly schema: "ice-research-state-compiled/v1"
  readonly stateid: string
  readonly target: string
  readonly scope: "SUPPORTING_METHOD"
  readonly without: readonly string[]
  readonly hypothetical: boolean
  readonly context: ResearchRouterContext
  readonly links: readonly CompiledResearchLink[]
}

const isRecord = (value: unknown): value is Record<string, unknown> => typeof value === "object" && value !== null && !Array.isArray(value)
const idPattern = /^[A-Za-z][A-Za-z0-9_.:-]{0,95}$/
const targetPattern = /^[a-z0-9-]+::[a-z_]+:[A-Za-z0-9_.:-]+$/
const sha256Pattern = /^[a-f0-9]{64}$/
const objectKinds: readonly ResearchObjectKind[] = ["assumption", "result", "counterexample", "missing_object", "candidate"]
const objectStatuses: readonly ResearchObjectStatus[] = ["established", "candidate", "missing", "refuted", "unknown", "withdrawn"]
const relations: readonly ResearchLinkRelation[] = ["requires", "motivates", "obstructs", "analogy"]

const fail = (message: string): never => { throw new Error(`Invalid ice research state: ${message}`) }
const string = (value: unknown, label: string, maximum = 1_000): string => {
  if (typeof value !== "string" || !value.trim() || value.length > maximum) fail(`${label} must be a non-empty string of at most ${maximum} characters`)
  return value as string
}
const id = (value: unknown, label: string): string => {
  const actual = string(value, label, 96)
  if (!idPattern.test(actual)) fail(`${label} must be a safe identifier`)
  return actual
}
const array = (value: unknown, label: string, maximum: number): readonly unknown[] => {
  if (!Array.isArray(value) || value.length > maximum) fail(`${label} must be an array of at most ${maximum} entries`)
  return value as readonly unknown[]
}
const named = <T extends string>(value: unknown, label: string, permitted: readonly T[]): T => {
  if (typeof value !== "string" || !permitted.includes(value as T)) fail(`${label} is invalid`)
  return value as T
}
const distinct = (values: readonly string[], label: string): readonly string[] => {
  if (new Set(values).size !== values.length) fail(`${label} must be distinct`)
  return values
}
const references = (value: unknown, label: string, known: ReadonlySet<string>, minimum = 0): readonly string[] => {
  const entries = array(value, label, 12)
  if (entries.length < minimum) fail(`${label} must contain at least ${minimum} entry`)
  return distinct(entries.map((entry, index) => {
    const actual = id(entry, `${label}[${index}]`)
    if (!known.has(actual)) fail(`${label}[${index}] references missing source '${actual}'`)
    return actual
  }), label)
}

export const parseResearchState = (value: unknown): ResearchState => {
  if (!isRecord(value)) fail("root must be an object")
  const root = value as Record<string, unknown>
  if (root.schema !== "ice-research-state/v1") fail("schema must be ice-research-state/v1")
  const stateId = id(root.id, "id")
  const target = string(root.target, "target", 300)
  if (!targetPattern.test(target)) fail("target must be an exact qualified graph::node id")
  if (root.scope !== "SUPPORTING_METHOD") fail("scope must be SUPPORTING_METHOD")
  const question = string(root.question, "question", 500)
  const sourceEntries = array(root.sources, "sources", 12).map((entry, index): ResearchSource => {
    if (!isRecord(entry)) fail(`sources[${index}] must be an object`)
    const sourceRecord = entry as Record<string, unknown>
    const source = { id: id(sourceRecord.id, `sources[${index}].id`), path: string(sourceRecord.path, `sources[${index}].path`, 500), sha256: string(sourceRecord.sha256, `sources[${index}].sha256`, 64) }
    if (!sha256Pattern.test(source.sha256)) fail(`sources[${index}].sha256 must be lower-case SHA-256`)
    return source
  })
  distinct(sourceEntries.map((entry) => entry.id), "sources ids")
  const sourceIds = new Set(sourceEntries.map((entry) => entry.id))
  const objectEntries = array(root.objects, "objects", 32).map((entry, index): ResearchObject => {
    if (!isRecord(entry)) fail(`objects[${index}] must be an object`)
    const objectRecord = entry as Record<string, unknown>
    const rawAnchors = array(objectRecord.anchors, `objects[${index}].anchors`, 12)
    if (rawAnchors.length === 0) fail(`objects[${index}].anchors must contain at least one anchor`)
    const anchors = distinct(rawAnchors.map((anchor, anchorIndex) => {
      const actual = string(anchor, `objects[${index}].anchors[${anchorIndex}]`, 300)
      if (!targetPattern.test(actual)) fail(`objects[${index}].anchors[${anchorIndex}] must be an exact qualified KG id`)
      return actual
    }), `objects[${index}].anchors`)
    return { id: id(objectRecord.id, `objects[${index}].id`), kind: named(objectRecord.kind, `objects[${index}].kind`, objectKinds),
      label: string(objectRecord.label, `objects[${index}].label`, 240), status: named(objectRecord.status, `objects[${index}].status`, objectStatuses),
      summary: string(objectRecord.summary, `objects[${index}].summary`, 2_000), anchors,
      sources: references(objectRecord.sources, `objects[${index}].sources`, sourceIds, 1) }
  })
  distinct(objectEntries.map((entry) => entry.id), "objects ids")
  const objectIds = new Set(objectEntries.map((entry) => entry.id))
  const linkEntries = array(root.links, "links", 32).map((entry, index): ResearchLink => {
    if (!isRecord(entry)) fail(`links[${index}] must be an object`)
    const linkRecord = entry as Record<string, unknown>
    const inputs = array(linkRecord.inputs, `links[${index}].inputs`, 8).map((input, inputIndex): ResearchLinkInput => {
      if (!isRecord(input)) fail(`links[${index}].inputs[${inputIndex}] must be an object`)
      const inputRecord = input as Record<string, unknown>
      const object = id(inputRecord.object, `links[${index}].inputs[${inputIndex}].object`)
      if (!objectIds.has(object)) fail(`links[${index}].inputs[${inputIndex}] references missing object '${object}'`)
      return { role: string(inputRecord.role, `links[${index}].inputs[${inputIndex}].role`, 120), object }
    })
    if (inputs.length === 0) fail(`links[${index}].inputs must contain at least one role-bearing input`)
    const output = id(linkRecord.output, `links[${index}].output`)
    if (!objectIds.has(output)) fail(`links[${index}].output references missing object '${output}'`)
    return { id: id(linkRecord.id, `links[${index}].id`), label: string(linkRecord.label, `links[${index}].label`, 240),
      relation: named(linkRecord.relation, `links[${index}].relation`, relations), inputs, output,
      explanation: string(linkRecord.explanation, `links[${index}].explanation`, 2_000),
      falsifier: string(linkRecord.falsifier, `links[${index}].falsifier`, 1_000), sources: references(linkRecord.sources, `links[${index}].sources`, sourceIds, 1) }
  })
  distinct(linkEntries.map((entry) => entry.id), "links ids")
  if (!isRecord(root.routing)) fail("routing must be an object")
  const routingRecord = root.routing as Record<string, unknown>
  const routing = { domain: id(routingRecord.domain, "routing.domain"), map: id(routingRecord.map, "routing.map"), obstruction: id(routingRecord.obstruction, "routing.obstruction") }
  for (const [role, object] of Object.entries(routing)) if (!objectIds.has(object)) fail(`routing.${role} references missing object '${object}'`)
  return { schema: "ice-research-state/v1", id: stateId, target, scope: "SUPPORTING_METHOD", question, sources: sourceEntries, objects: objectEntries, links: linkEntries, routing }
}

const absent = (status: ResearchObjectStatus, without: ReadonlySet<string>, object: string): boolean =>
  without.has(object) || status === "missing" || status === "refuted" || status === "unknown" || status === "withdrawn"

const routeStatus = <T extends string>(object: ResearchObject | undefined, without: ReadonlySet<string>, rules: Readonly<Record<ResearchObjectStatus, T>>): T =>
  object === undefined || without.has(object.id) ? rules.unknown : rules[object.status]

export const compileResearchState = (state: ResearchState, without: readonly string[] = []): CompiledResearchState => {
  const objects = new Map(state.objects.map((object) => [object.id, object]))
  const removed = new Set(without)
  for (const object of removed) if (!objects.has(object)) throw new Error(`Unknown counterfactual object '${object}'`)
  const context: ResearchRouterContext = {
    domain: routeStatus(objects.get(state.routing.domain), removed, { established: "declared", candidate: "declared", missing: "missing", refuted: "unknown", unknown: "unknown", withdrawn: "unknown" }),
    map: routeStatus(objects.get(state.routing.map), removed, { established: "candidate", candidate: "candidate", missing: "missing", refuted: "unknown", unknown: "unknown", withdrawn: "unknown" }),
    obstruction: routeStatus(objects.get(state.routing.obstruction), removed, { established: "present", candidate: "unknown", missing: "unknown", refuted: "not_recorded", unknown: "unknown", withdrawn: "unknown" })
  }
  const links = state.links.map((link): CompiledResearchLink => {
    const absentInputs = link.inputs.filter((input) => absent(objects.get(input.object)?.status ?? "unknown", removed, input.object))
    const hasCandidate = link.inputs.some((input) => objects.get(input.object)?.status === "candidate" && !removed.has(input.object))
    const readiness: ResearchReadiness = absentInputs.length > 0 ? "BLOCKED" : hasCandidate ? "CONDITIONAL" : "INPUTS_PRESENT"
    return { ...link, readiness, available: readiness !== "BLOCKED", absent_inputs: absentInputs,
      output_status: removed.has(link.output) ? "withdrawn" : objects.get(link.output)?.status ?? "unknown" }
  })
  return { schema: "ice-research-state-compiled/v1", stateid: state.id, target: state.target, scope: state.scope,
    without: [...removed].sort(), hypothetical: removed.size > 0, context, links }
}

const mermaidText = (text: string): string => text.replace(/["\\\n\r]/g, " ")

/**
 * `repositoryRoot` is optional because a stored state is portable.  Callers
 * which know the checkout can pass its actual path for clickable local links;
 * otherwise the authored repository-relative locator remains intact.
 */
export const renderResearchState = (state: ResearchState, view: CompiledResearchState, repositoryRoot?: string): string => {
  if (view.stateid !== state.id || view.target !== state.target) throw new Error("Compiled state does not belong to supplied state")
  const objects = new Map(state.objects.map((object) => [object.id, object]))
  const objectIndex = new Map(state.objects.map((object, index) => [object.id, index]))
  const objectNode = (object: string): string => `object_${objectIndex.get(object) ?? "unknown"}`
  const effectiveStatus = (object: string): ResearchObjectStatus => view.without.includes(object)
    ? "withdrawn" : objects.get(object)?.status ?? "unknown"
  const rolePairs: readonly (readonly [string, string])[] = [
    ["domain", state.routing.domain], ["map", state.routing.map], ["obstruction", state.routing.obstruction]
  ]
  const roles = rolePairs.map(([role, object]) => `- ${role}: **${objects.get(object)?.label ?? object}** (${effectiveStatus(object)})`).join("\n")
  const links = view.links.map((link) => {
    const inputs = link.inputs.map((input) => `${input.role}=${objects.get(input.object)?.label ?? input.object}`).join(" + ")
    const blocked = link.absent_inputs.length === 0 ? "" : `\n  - 막힌 입력: ${link.absent_inputs.map((input) => `${input.role}=${objects.get(input.object)?.label ?? input.object}`).join(", ")}`
    const navigation = link.relation === "analogy"
      ? "\n  - 유추 관계는 탐색용 navigation이며, 출력의 추론·증명 근거가 아니다."
      : ""
    const noPromotion = link.readiness === "INPUTS_PRESENT"
      ? "\n  - 입력이 갖춰졌다는 표기일 뿐, 다음 소비자의 성립·증명·승격을 뜻하지 않는다."
      : ""
    return `- **${link.label}** [${link.relation}; ${link.readiness}]\n  - 같이 필요한 조건: ${inputs}\n  - 왜 이 관계를 보는가: ${link.explanation}\n  - 다음 소비자: ${objects.get(link.output)?.label ?? link.output} (${link.output_status})${blocked}\n  - 반증 조건: ${link.falsifier}${navigation}${noPromotion}`
  }).join("\n")
  const graphObjects = state.objects.map((object, index) =>
    `object_${index}["${mermaidText(object.label)}\\nstatus: ${effectiveStatus(object.id)}"]`)
  const graph = view.links.flatMap((link, index) => {
    const relation = `relation_${index}`
    const output = objectNode(link.output)
    return [
      `${relation}["${mermaidText(link.label)}\\n${link.relation} · ${link.readiness}"]`,
      ...link.inputs.map((input) => `${objectNode(input.object)} -->|${mermaidText(input.role)}| ${relation}`),
      `${relation} -->|output| ${output}`
    ]
  }).join("\n")
  const sourceUrl = (path: string): string => repositoryRoot === undefined || !repositoryRoot.trim()
    ? path
    : `${repositoryRoot.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`
  const sources = state.sources.map((source) => `- [${source.path}](${sourceUrl(source.path)}) · \`${source.sha256}\``).join("\n")
  const hypothetical = view.hypothetical
    ? `\n> 가상 반사실 보기: ${view.without.join(", ")}을(를) 기록에서 제거한 것으로 가정했다. 이는 반증·부정·물리적 결론이 아니며 canonical KG를 바꾸지 않는다.\n`
    : ""
  return `# 연구 상태: ${state.id}\n\n대상: \`${state.target}\` · 범위: \`${state.scope}\`\n\n질문: ${state.question}\n${hypothetical}\n## 지금 연구의 세 역할\n\n${roles}\n\nHSWM router 문맥: domain=${view.context.domain}, map=${view.context.map}, obstruction=${view.context.obstruction}. 이 상태는 경로 선택용이며 연구 결과의 참·증명 판정이 아니다.\n\n## 같이 필요한 조건과 다음 소비자\n\n${links}\n\n## 역할을 가진 관계 구조\n\n\`\`\`mermaid\nflowchart LR\n${[...graphObjects, graph].join("\n")}\n\`\`\`\n\n## 고정한 출처\n\n${sources}\n`
}
