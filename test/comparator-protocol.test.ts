import { readFileSync } from "node:fs"
import { NodeContext } from "@effect/platform-node"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import {
  comparatorProtocolShowData,
  comparatorProtocolSummaryData,
  comparatorProtocolTraceData,
  comparatorProtocolValidateData
} from "../src/comparator-protocol/commands.ts"
import { validateIceComparatorProtocol } from "../src/comparator-protocol/core.ts"
import {
  ComparatorProtocolError,
  decodeIceComparatorProtocol,
  type IceComparatorProtocol
} from "../src/comparator-protocol/model.ts"
import {
  decodeScientificIntuitionFlowV2,
  type ScientificIntuitionFlowV2
} from "../src/intuition/model.ts"
import type { CollectionGraph } from "../src/ontology/collection-core.ts"
import { WorkspaceLive } from "../src/workspace.ts"

const protocolText = readFileSync(
  new URL("../research/benchmarks/ice-comparator-protocol.v1.json", import.meta.url),
  "utf8"
)
const intuitionText = readFileSync(
  new URL("../research/intuition/scientific-intuition-signals.v2.json", import.meta.url),
  "utf8"
)
const protocol = decodeIceComparatorProtocol(protocolText, "comparator-fixture")
const decodedIntuition = decodeScientificIntuitionFlowV2(intuitionText, "intuition-fixture")
const intuition = {
  ...decodedIntuition,
  sources: decodedIntuition.sources.map(({ canonical_source: _canonicalSource, ...source }) => source),
  signals: decodedIntuition.signals.map(({ canonical_target: _canonicalTarget, ...signal }) => signal)
} as ScientificIntuitionFlowV2
const cptFixture = [{
  descriptor: { key: "cpt" },
  graph: {
    nodes: [{
      id: "open:gate4-spinorial-charge-domain-constraint-closure",
      type: "open_problem"
    }]
  }
}] as unknown as ReadonlyArray<CollectionGraph>

it("decodes and semantically validates the design-only comparator DAG", () => {
  const report = validateIceComparatorProtocol(protocol, intuition, cptFixture)
  expect(report).toMatchObject({
    valid: true,
    authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL",
    canonical_graph_unchanged: true,
    does_not_authorize_execution: true,
    result_status: "DESIGN_ONLY",
    counts: {
      source_pins: 5,
      tools: 2,
      models: 3,
      consumers: 3,
      steps: 5,
      edges: 4,
      planned_inputs: 5,
      planned_outputs: 5
    }
  })
  expect(report.errors).toEqual([])
})

it("rejects unknown, claim-like, execution, and result fields recursively", () => {
  const raw = JSON.parse(protocolText) as Record<string, unknown>
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, unexpected: true }),
    "bad-comparator"
  )).toThrow(ComparatorProtocolError)
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, selected_strategy: { ...(raw.selected_strategy as object), probability: 0.8 } }),
    "bad-comparator"
  )).toThrow("forbidden field 'probability'")
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, execution_command: "python bypass.py" }),
    "bad-comparator"
  )).toThrow("forbidden field 'execution_command'")
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, result: "success" }),
    "bad-comparator"
  )).toThrow("forbidden field 'result'")
})

it("aligns strict text, UTC calendar, and lowercase HTTP scheme decoding", () => {
  const raw = JSON.parse(protocolText) as Record<string, unknown>
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, title: "   " }),
    "bad-comparator"
  )).toThrow("must be a non-empty string")
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({ ...raw, updated_at_utc: "2026-02-30T00:00:00Z" }),
    "bad-comparator"
  )).toThrow("must be UTC ISO-8601")
  const sourcePins = raw.source_pins as ReadonlyArray<Record<string, unknown>>
  expect(() => decodeIceComparatorProtocol(
    JSON.stringify({
      ...raw,
      source_pins: [{ ...sourcePins[0], uri: "HTTPS://example.test/source" }, ...sourcePins.slice(1)]
    }),
    "bad-comparator"
  )).toThrow("must use a lowercase HTTP(S) scheme")
})

it("fails closed when the referenced intuition graph is semantically invalid", () => {
  const invalidIntuition = {
    ...intuition,
    signals: intuition.signals.map((signal, index) => index === 0
      ? { ...signal, source_refs: ["source-ref:missing"] }
      : signal)
  } as ScientificIntuitionFlowV2
  expect(validateIceComparatorProtocol(protocol, invalidIntuition, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ code: "INTUITION_SOURCE_REF_NOT_FOUND" })
    ])
  )
})

it("rejects missing choice axes and incomplete cross-domain or solver coverage", () => {
  const altered = {
    ...protocol,
    steps: protocol.steps.map((step) => step.kind === "CROSS_DOMAIN_TEST"
      ? {
          ...step,
          choice_dimensions: ["gauge"],
          consumer_refs: ["route-consumer:background"],
          tool_refs: ["route-tool:h-eftcamb"]
        }
      : step)
  } as IceComparatorProtocol
  expect(validateIceComparatorProtocol(altered, intuition, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ code: "CHOICE_DIMENSION_MISSING" }),
      expect.objectContaining({ code: "CROSS_DOMAIN_COVERAGE_INCOMPLETE" }),
      expect.objectContaining({ code: "INDEPENDENT_SOLVER_COUNT_TOO_SMALL" })
    ])
  )
})

it("rejects canonical geometry targets, unresolved prerequisites, cycles, and cross-lane dependencies", () => {
  const altered = {
    ...protocol,
    steps: protocol.steps.map((step) => {
      if (step.id === "route-step:hu-sawicki-n1-cross-domain") {
        return { ...step, prerequisite_outputs: ["route-output:missing"] }
      }
      if (step.id === "route-step:jbd-gr-limit-calibration") {
        return {
          ...step,
          context_refs: [{
            graph: "cpt" as const,
            node: "open:gate4-spinorial-charge-domain-constraint-closure",
            relation: "CONTEXTUALIZES_NONAUTHORITATIVELY" as const
          }]
        }
      }
      return step
    }),
    edges: [
      ...protocol.edges.map((edge) => edge.relation === "INDEPENDENT_PARALLEL_TO"
        ? { ...edge, relation: "INFORMS" as const }
        : edge),
      {
        id: "route-edge:admission-back-to-calibration",
        from: "route-step:geometry-ice-admission-decision",
        relation: "INFORMS" as const,
        to: "route-step:jbd-gr-limit-calibration",
        rationale: "Invalid cycle fixture.",
        non_claim: "Invalid test-only edge.",
        does_not_authorize_execution: true as const
      }
    ]
  } as IceComparatorProtocol
  expect(validateIceComparatorProtocol(altered, intuition, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ code: "GEOMETRY_CANONICAL_CONTEXT_FORBIDDEN" }),
      expect.objectContaining({ code: "PREREQUISITE_OUTPUT_NOT_FOUND" }),
      expect.objectContaining({ code: "CROSS_LANE_DEPENDENCY_FORBIDDEN" }),
      expect.objectContaining({ code: "DIRECTED_ROUTE_CYCLE" })
    ])
  )
})

it("rejects ambiguous outputs and a selected comparator not used by its cross-domain step", () => {
  const firstOutput = protocol.steps[0]?.outputs[0]
  expect(firstOutput).toBeDefined()
  const altered = {
    ...protocol,
    selected_strategy: {
      ...protocol.selected_strategy,
      first_comparator_model: "route-model:jbd-calibration"
    },
    steps: protocol.steps.map((step, index) => index === 1 && firstOutput !== undefined
      ? { ...step, outputs: [firstOutput] }
      : step)
  } as IceComparatorProtocol
  expect(validateIceComparatorProtocol(altered, intuition, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ code: "DUPLICATE_OUTPUT_ID" }),
      expect.objectContaining({ code: "SELECTED_COMPARATOR_INVALID" }),
      expect.objectContaining({ code: "SELECTED_COMPARATOR_NOT_USED" })
    ])
  )
})

it("requires an explicit PREREQUISITE_FOR edge for every prerequisite output", () => {
  const altered = {
    ...protocol,
    edges: protocol.edges.map((edge) => edge.id === "route-edge:cross-domain-prerequisite-ice-admission"
      ? { ...edge, relation: "INFORMS" as const }
      : edge)
  } as IceComparatorProtocol
  expect(validateIceComparatorProtocol(altered, intuition, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({
        code: "PREREQUISITE_EDGE_NOT_FOUND",
        subject: "route-step:geometry-ice-admission-decision"
      })
    ])
  )
})

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("comparator protocol CLI data", (it) => {
  it.effect("validates, summarizes, resolves, and traces the repository route", () =>
    Effect.gen(function* () {
      const report = yield* comparatorProtocolValidateData
      expect(report.valid).toBe(true)

      const summary = yield* comparatorProtocolSummaryData
      expect(summary).toMatchObject({
        contract: {
          authority: "NON_AUTHORITATIVE_METHOD_PROTOCOL",
          canonical_graph_unchanged: true,
          does_not_authorize_execution: true,
          result_status: "DESIGN_ONLY"
        },
        by_lane: {
          GEOMETRY_COMPARATOR: 4,
          FOLDED_SUSY_CLASSIFICATION: 1
        }
      })
      expect(summary.geometry_route).toEqual([
        "route-step:jbd-gr-limit-calibration",
        "route-step:hu-sawicki-n1-action-audit",
        "route-step:hu-sawicki-n1-cross-domain",
        "route-step:geometry-ice-admission-decision"
      ])

      const shown = yield* comparatorProtocolShowData(
        "route-step:hu-sawicki-n1-cross-domain"
      )
      expect(shown).toMatchObject({
        entity_kind: "step",
        entity: {
          state: "PLANNED",
          does_not_authorize_execution: true,
          consumer_refs: [
            "route-consumer:background",
            "route-consumer:scalar-growth-lensing",
            "route-consumer:tensor-propagation"
          ]
        }
      })

      const trace = yield* comparatorProtocolTraceData(
        "route-step:geometry-ice-admission-decision"
      )
      expect(trace.ancestors).toEqual(expect.arrayContaining([
        "route-step:jbd-gr-limit-calibration",
        "route-step:hu-sawicki-n1-action-audit",
        "route-step:hu-sawicki-n1-cross-domain"
      ]))
      expect(trace.descendants).toEqual([])
      expect(trace.independent_parallel_neighbors).toEqual([])
    })
  )
})
