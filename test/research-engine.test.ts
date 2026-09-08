import { expect, it } from "vitest"
import { researchInvocation, type ResearchOptions } from "../src/research-engine/commands.ts"

const valid: ResearchOptions = {
  question: "Which declared input can falsify this supporting route?",
  target: "cpt::open:gate1-original-cycle-signed-global-intersections",
  references: ["docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md"],
  mode: "investigate",
  tier: "supporting",
  runner: "",
  budget: 120
}

it("builds the bounded HSWM task without changing caller reference order", () => {
  const actual = researchInvocation(valid)
  expect(actual).toEqual({
    context: { mode: "investigate", graph: "cpt", tier: "supporting" },
    task: {
      question: valid.question,
      target: valid.target,
      references: valid.references,
      runner: null
    }
  })
})

it("keeps the compute runner opt-in and rejects malformed bounded inputs", () => {
  expect(researchInvocation({ ...valid, mode: "compute", runner: "starobinsky_relative_primary_boundary" }).task.runner)
    .toBe("starobinsky_relative_primary_boundary")
  expect(() => researchInvocation({ ...valid, mode: "compute" })).toThrow("requires and accepts")
  expect(() => researchInvocation({ ...valid, runner: "starobinsky_relative_primary_boundary" })).toThrow("requires and accepts")
  expect(() => researchInvocation({ ...valid, references: ["../outside.md"] })).toThrow("repository-relative")
  expect(() => researchInvocation({ ...valid, budget: 29 })).toThrow("between 30 and 900")
  expect(() => researchInvocation({ ...valid, target: "cpt::claim:" })).toThrow("exact qualified")
  expect(() => researchInvocation({ ...valid, tier: "core", target: "hypercomplex::open:route" })).toThrow("declared core route")
})
