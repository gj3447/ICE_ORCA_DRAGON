import { expect, it } from "vitest"
import { compileResearchState, parseResearchState, renderResearchState } from "../src/research-engine/state.ts"

const source = { id: "src-boundary", path: "docs/research/boundary.md", sha256: "a".repeat(64) }
const raw = {
  schema: "ice-research-state/v1",
  id: "boundary-chain-map",
  target: "cpt::open:starobinsky-seam-ward-boundary-state-limit",
  scope: "SUPPORTING_METHOD",
  question: "Which typed condition decides whether the reduction can become a quantum boundary map?",
  sources: [source],
  objects: [
    { id: "domain", kind: "assumption", label: "defined domain", status: "established", summary: "A declared domain for the classical reduction.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["src-boundary"] },
    { id: "quantum-map", kind: "candidate", label: "quantum boundary map", status: "candidate", summary: "Candidate map only, not an established construction.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["src-boundary"] },
    { id: "domain-escape", kind: "counterexample", label: "BFV domain escape", status: "established", summary: "The stated boundary condition is not preserved by the operation.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["src-boundary"] },
    { id: "chain-map", kind: "missing_object", label: "chain-map condition", status: "missing", summary: "No supplied quantum chain map has been checked.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["src-boundary"] },
    { id: "sewing-test", kind: "result", label: "sewing test", status: "unknown", summary: "A downstream consumer, retained without promotion.", anchors: ["cpt::open:starobinsky-seam-ward-boundary-state-limit"], sources: ["src-boundary"] }
  ],
  links: [
    { id: "define-map", label: "define the candidate map", relation: "requires", inputs: [{ role: "domain", object: "domain" }, { role: "missing chain map", object: "chain-map" }], output: "quantum-map", explanation: "Both inputs are jointly required.", falsifier: "A domain-preserving map fails the stated chain condition.", sources: ["src-boundary"] },
    { id: "obstruction", label: "test the obstruction", relation: "obstructs", inputs: [{ role: "candidate map", object: "quantum-map" }, { role: "counterexample", object: "domain-escape" }], output: "sewing-test", explanation: "The counterexample directs a bounded test.", falsifier: "The operation preserves the declared domain in the tested convention.", sources: ["src-boundary"] },
    { id: "analogy", label: "analogy lens", relation: "analogy", inputs: [{ role: "candidate map", object: "quantum-map" }], output: "sewing-test", explanation: "A search lens only.", falsifier: "The analogy has no shared typed input.", sources: ["src-boundary"] }
  ],
  routing: { domain: "domain", map: "quantum-map", obstruction: "domain-escape" }
} as const

it("rejects unpinned sources and dangling role-bearing object references", () => {
  expect(() => parseResearchState({ ...raw, sources: [{ ...source, sha256: "bad" }] })).toThrow("SHA-256")
  expect(() => parseResearchState({ ...raw, links: [{ ...raw.links[0], inputs: [{ role: "domain", object: "missing" }] }] })).toThrow("missing object")
  expect(() => parseResearchState({ ...raw, objects: [{ ...raw.objects[0], anchors: [] }, ...raw.objects.slice(1)] })).toThrow("at least one anchor")
  expect(() => parseResearchState({ ...raw, links: [{ ...raw.links[0], sources: [] }] })).toThrow("at least 1 entry")
})

it("keeps input roles as a joint condition even when input ordering differs", () => {
  const first = parseResearchState(raw)
  const swapped = parseResearchState({ ...raw, links: [{ ...raw.links[0], inputs: [...raw.links[0].inputs].reverse() }, ...raw.links.slice(1)] })
  expect(compileResearchState(first).links[0]?.readiness).toBe("BLOCKED")
  expect(compileResearchState(swapped).links[0]?.readiness).toBe("BLOCKED")
  expect(renderResearchState(first, compileResearchState(first))).toContain("같이 필요한 조건")
})

it("propagates reviewed state changes into router context and dependent links without promoting the output", () => {
  const state = parseResearchState(raw)
  const baseline = compileResearchState(state)
  expect(baseline.context).toEqual({ domain: "declared", map: "candidate", obstruction: "present" })
  expect(baseline.links.find((link) => link.id === "define-map")?.output_status).toBe("candidate")
  expect(baseline.links.find((link) => link.id === "obstruction")?.readiness).toBe("CONDITIONAL")
  const without = compileResearchState(state, ["domain-escape"])
  expect(without.hypothetical).toBe(true)
  expect(without.context.obstruction).toBe("unknown")
  expect(without.links.find((link) => link.id === "obstruction")).toMatchObject({ readiness: "BLOCKED", available: false })
  expect(renderResearchState(state, without)).toContain("가상 반사실 보기")
  expect(renderResearchState(state, without)).toContain("status: withdrawn")
})

it("distinguishes missing and withdrawn route inputs, and does not turn analogy into proof", () => {
  const missing = parseResearchState(raw)
  const withdrawn = parseResearchState({ ...raw, objects: raw.objects.map((object) => object.id === "domain" ? { ...object, status: "withdrawn" as const } : object) })
  expect(compileResearchState(missing).context.domain).toBe("declared")
  expect(compileResearchState(withdrawn).context.domain).toBe("unknown")
  const analogy = compileResearchState(missing).links.find((link) => link.id === "analogy")
  expect(analogy).toMatchObject({ relation: "analogy", readiness: "CONDITIONAL", output_status: "unknown" })
  const rendered = renderResearchState(missing, compileResearchState(missing))
  expect(rendered).toContain("유추 관계는 탐색용 navigation")
  expect(rendered).toContain("[docs/research/boundary.md](docs/research/boundary.md)")
  expect(renderResearchState(missing, compileResearchState(missing), "/workspace/ICE")).toContain(
    "[docs/research/boundary.md](/workspace/ICE/docs/research/boundary.md)"
  )
})
