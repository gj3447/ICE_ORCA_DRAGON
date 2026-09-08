import { expect, it } from "vitest"
import { parseResearchState } from "../src/research-engine/state.ts"
import { parseResearchProposal, proposalJsonSchema, proposalJsonSchemaForState, renderResearchProposal } from "../src/research-engine/proposal.ts"

const state = parseResearchState({
  schema: "ice-research-state/v1", id: "boundary-state", target: "cpt::open:starobinsky-seam-ward-boundary-state-limit", scope: "SUPPORTING_METHOD", question: "Which bounded test is next?",
  sources: [{ id: "source-a", path: "docs/research/source-a.md", sha256: "a".repeat(64) }],
  objects: [
    { id: "classical", kind: "result", label: "classical reduction", status: "established", summary: "A reviewed classical result.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["source-a"] },
    { id: "counterexample", kind: "counterexample", label: "domain escape", status: "established", summary: "A reviewed obstruction.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["source-a"] },
    { id: "quantum-map", kind: "missing_object", label: "quantum map", status: "missing", summary: "No supplied map.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["source-a"] },
    { id: "consumer", kind: "candidate", label: "sewing consumer", status: "candidate", summary: "A downstream candidate.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["source-a"] }
  ],
  links: [{ id: "needs-map", label: "needs map", relation: "requires", inputs: [{ role: "input", object: "classical" }, { role: "missing", object: "quantum-map" }], output: "consumer", explanation: "The map is required.", falsifier: "A supplied construction discharges it.", sources: ["source-a"] }],
  routing: { domain: "quantum-map", map: "quantum-map", obstruction: "counterexample" }
})

const raw = {
  schema: "ice-research-proposal/v1", state_id: "boundary-state", summary: "The reviewed obstruction makes a declared quantum map the first bounded question.",
  connections: [{ premises: ["classical", "counterexample"], conclusion: "Test a named quantum map before sewing.", explanation: "The same classical reduction does not fix a quantum carrier.", assumptions: ["quantum-map"], falsifier: "A source-compatible chain map on declared domains defeats this route.", status: "HYPOTHESIS" }],
  next_test: { question: "Can a declared U preserve its named domain?", inputs: ["classical", "counterexample"], missing: ["quantum-map"], falsifier: "A domain-preserving, intertwined U is exhibited.", consumer: "consumer", non_claim: "This does not establish a physical product or CPT sewing." },
  reading_order: ["classical", "counterexample", "quantum-map", "consumer"]
} as const

it("rejects an invented reference, wrong state, and false proof status", () => {
  expect(() => parseResearchProposal({ ...raw, state_id: "other-state" }, state)).toThrow("state_id")
  expect(() => parseResearchProposal({ ...raw, connections: [{ ...raw.connections[0], premises: ["classical", "invented"] }] }, state)).toThrow("invented")
  expect(() => parseResearchProposal({ ...raw, connections: [{ ...raw.connections[0], status: "PROVEN" }] }, state)).toThrow("HYPOTHESIS or QUESTION")
})

it("only permits unavailable state objects in a missing-input role", () => {
  expect(() => parseResearchProposal({ ...raw, next_test: { ...raw.next_test, missing: ["classical"] } }, state)).toThrow("missing, unknown, refuted, or withdrawn")
  const withdrawn = parseResearchState({ ...state, objects: state.objects.map((object) => object.id === "quantum-map" ? { ...object, status: "withdrawn" as const } : object) })
  expect(parseResearchProposal(raw, withdrawn).next_test.missing).toEqual(["quantum-map"])
})

it("renders every joint premise and its pinned source link", () => {
  const proposal = parseResearchProposal(raw, state)
  const rendered = renderResearchProposal(proposal, state, "/home/lagyeongjun/CD/ICE_ORCA_DRAGON")
  expect(rendered).toContain("전제 (모두 함께 필요)")
  expect(rendered).toContain("`classical`")
  expect(rendered).toContain("`counterexample`")
  expect(rendered).toContain("[source-a](/home/lagyeongjun/CD/ICE_ORCA_DRAGON/docs/research/source-a.md)")
  expect(rendered).toContain("반증 조건")
  expect(rendered).toContain("전제 (모두 함께 필요):\n\n-")
})

it("does not let an empty model missing list hide an unavailable source-state input", () => {
  const proposal = parseResearchProposal({ ...raw, next_test: { ...raw.next_test, inputs: ["classical", "quantum-map"], missing: [] } }, state)
  const rendered = renderResearchProposal(proposal, state)
  expect(rendered).toContain("원본 상태에서 미확보인 검사 입력")
  expect(rendered).toContain("`quantum-map` — quantum map (missing;")
})

it("publishes a strict schema for every model-created object", () => {
  expect(proposalJsonSchema.additionalProperties).toBe(false)
  expect((proposalJsonSchema.properties as Record<string, Record<string, unknown>>).schema?.type).toBe("string")
  const connection = (proposalJsonSchema.properties as Record<string, unknown>).connections as Record<string, unknown>
  expect(((connection.items as Record<string, unknown>).additionalProperties)).toBe(false)
  const next = (proposalJsonSchema.properties as Record<string, unknown>).next_test as Record<string, unknown>
  expect(next.additionalProperties).toBe(false)
})

it("binds provider generation IDs and state identity to the reviewed state", () => {
  const bound = proposalJsonSchemaForState(state)
  const properties = bound.properties as Record<string, Record<string, unknown>>
  expect(properties.state_id?.const).toBe("boundary-state")
  const connectionItems = properties.connections?.items as Record<string, unknown>
  const connectionProperties = connectionItems.properties as Record<string, Record<string, unknown>>
  const premiseItems = connectionProperties.premises?.items as Record<string, unknown>
  expect(premiseItems.enum).toEqual(["classical", "counterexample", "quantum-map", "consumer"])
  expect(connectionProperties.premises?.uniqueItems).toBeUndefined()
})
