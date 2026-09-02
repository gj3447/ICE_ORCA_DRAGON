import { NodeContext } from "@effect/platform-node"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import type { CollectionGraph } from "../src/ontology/collection-core.ts"
import {
  scientificIntuitionSearchData,
  scientificIntuitionValidateData
} from "../src/intuition/commands.ts"
import { validateScientificIntuitionFlow } from "../src/intuition/core.ts"
import {
  decodeScientificIntuitionFlow,
  ScientificIntuitionFlowError
} from "../src/intuition/model.ts"
import { WorkspaceLive } from "../src/workspace.ts"

const fixture = {
  schema_version: "scientific-intuition-flow/v1",
  graph_id: "intuition-flow:gate1",
  title: "Fixture intuition flow",
  description: "A strictly bounded test fixture.",
  updated_at_utc: "2026-09-02T00:00:00Z",
  authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
  canonical_graph_unchanged: true,
  does_not_authorize_execution: true,
  standards_alignment: [
    {
      id: "standard:rdf11",
      standard: "RDF 1.1",
      uri: "https://www.w3.org/TR/rdf11-concepts/",
      status: "Recommendation",
      boundary: "does not promote a signal into canonical ontology evidence"
    },
    {
      id: "standard:jsonld11",
      standard: "JSON-LD 1.1",
      uri: "https://www.w3.org/TR/json-ld11/",
      status: "Recommendation",
      boundary: "exchange syntax only"
    },
    {
      id: "standard:prov-o",
      standard: "PROV-O",
      uri: "https://www.w3.org/TR/prov-o/",
      status: "Recommendation",
      boundary: "provenance is not truth"
    },
    {
      id: "standard:shacl",
      standard: "SHACL",
      uri: "https://www.w3.org/TR/shacl/",
      status: "Recommendation",
      boundary: "conformance is structural"
    }
  ],
  sources: [
    {
      id: "source-ref:primary",
      kind: "PRIMARY_PAPER",
      citation: "A primary source",
      uri: "https://example.test/paper",
      version: "v1",
      retrieved_at_utc: "2026-09-02T00:00:00Z",
      pinpoint: "Section 2",
      role: "method comparator",
      boundary: "not evidence for an ICE result",
      canonical_source: { graph: "cpt", node: "source:primary" }
    }
  ],
  signals: [
    {
      id: "intuition:first",
      status: "CANDIDATE",
      kind: "MISSING_TYPED_OBJECT",
      target: { graph: "cpt", node: "open:target" },
      lens: "Which object would make the boundary explicit?",
      why_relevant: "It sharpens a missing object without asserting it exists.",
      source_refs: ["source-ref:primary"],
      assumptions: ["The cited method has a comparable boundary condition."],
      discriminating_observation: "The required object is either constructible or absent under the declared convention.",
      stop_condition: "Stop if the source assumptions do not map to the target scope.",
      principal_failure_class: "inference",
      non_claim: "This is a navigation lens, not a scientific claim.",
      does_not_authorize_execution: true
    },
    {
      id: "intuition:second",
      status: "CANDIDATE",
      kind: "SEPARATION_TEST",
      target: { graph: "cpt", node: "open:target" },
      lens: "Which observation separates local from global information?",
      why_relevant: "It proposes a falsifiable separation rather than a conclusion.",
      source_refs: ["source-ref:primary"],
      assumptions: ["The declared target retains an identifiable local/global split."],
      discriminating_observation: "A global datum changes while the local proxy is held fixed.",
      stop_condition: "Stop if no controlled separation is definable.",
      principal_failure_class: "inference",
      non_claim: "This does not establish a physical relation.",
      does_not_authorize_execution: true
    }
  ],
  boundaries: ["No signal is canonical evidence, a claim, or execution authority."]
} as const

const cptFixture = [{
  descriptor: { key: "cpt" },
  graph: {
    nodes: [
      { id: "open:target", type: "open_problem" },
      { id: "source:primary", type: "source", uri: "https://example.test/paper" }
    ]
  }
}] as unknown as ReadonlyArray<CollectionGraph>

it("strictly decodes a non-authoritative source-backed intuition flow", () => {
  const flow = decodeScientificIntuitionFlow(JSON.stringify(fixture), "fixture")
  const report = validateScientificIntuitionFlow(flow, cptFixture)
  expect(report).toMatchObject({
    valid: true,
    authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
    canonical_graph_unchanged: true,
    does_not_authorize_execution: true,
    counts: { standards_alignment: 4, sources: 1, signals: 2, candidates: 2 }
  })
})

it("rejects unknown and recursively claim-like fields", () => {
  expect(() =>
    decodeScientificIntuitionFlow(JSON.stringify({ ...fixture, score: 0.9 }), "fixture")
  ).toThrow(ScientificIntuitionFlowError)
  expect(() =>
    decodeScientificIntuitionFlow(
      JSON.stringify({
        ...fixture,
        signals: [{ ...fixture.signals[0], lens: { value: fixture.signals[0].lens, probability: 0.5 } }, fixture.signals[1]]
      }),
      "fixture"
    )
  ).toThrow("forbidden field 'probability'")
})

it("requires resolved sources, canonical open-problem targets, and two candidates", () => {
  const unknownSource = decodeScientificIntuitionFlow(
    JSON.stringify({
      ...fixture,
      signals: [{ ...fixture.signals[0], source_refs: ["source-ref:missing"] }, fixture.signals[1]]
    }),
    "fixture"
  )
  expect(validateScientificIntuitionFlow(unknownSource, cptFixture).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "SOURCE_REF_NOT_FOUND" })])
  )

  const nonOpenTarget = decodeScientificIntuitionFlow(
    JSON.stringify({
      ...fixture,
      signals: [
        { ...fixture.signals[0], target: { graph: "cpt", node: "concept:not-open" } },
        { ...fixture.signals[1], target: { graph: "cpt", node: "concept:not-open" } }
      ]
    }),
    "fixture"
  )
  const nonOpenGraphs = [{
    descriptor: { key: "cpt" },
    graph: { nodes: [{ id: "concept:not-open", type: "concept" }] }
  }] as unknown as ReadonlyArray<CollectionGraph>
  expect(validateScientificIntuitionFlow(nonOpenTarget, nonOpenGraphs).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "TARGET_NODE_NOT_OPEN_PROBLEM" })])
  )

  const oneCandidate = decodeScientificIntuitionFlow(
    JSON.stringify({ ...fixture, signals: [{ ...fixture.signals[0], status: "RETIRED" }, fixture.signals[1]] }),
    "fixture"
  )
  expect(validateScientificIntuitionFlow(oneCandidate, cptFixture).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "CANDIDATE_SIGNAL_COUNT_TOO_SMALL" })])
  )
})

it("rejects repeated graph identifiers and false canonical-source bridges", () => {
  const repeated = decodeScientificIntuitionFlow(
    JSON.stringify({
      ...fixture,
      standards_alignment: [
        fixture.standards_alignment[0],
        fixture.standards_alignment[0],
        fixture.standards_alignment[2],
        fixture.standards_alignment[3]
      ],
      signals: [
        {
          ...fixture.signals[0],
          source_refs: ["source-ref:primary", "source-ref:primary"]
        },
        fixture.signals[1]
      ]
    }),
    "fixture"
  )
  expect(validateScientificIntuitionFlow(repeated, cptFixture).errors).toEqual(
    expect.arrayContaining([
      expect.objectContaining({ code: "DUPLICATE_STANDARD_ID" }),
      expect.objectContaining({ code: "DUPLICATE_SOURCE_REF" })
    ])
  )

  const mismatchedSource = decodeScientificIntuitionFlow(
    JSON.stringify({
      ...fixture,
      sources: [{ ...fixture.sources[0], uri: "https://example.test/different" }]
    }),
    "fixture"
  )
  expect(validateScientificIntuitionFlow(mismatchedSource, cptFixture).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "CANONICAL_SOURCE_URI_MISMATCH" })])
  )
})

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("canonical scientific-intuition federation", (it) => {
  it.effect("resolves exact targets, source bridges, and non-authoritative links", () =>
    Effect.gen(function* () {
      const report = yield* scientificIntuitionValidateData
      expect(report).toMatchObject({
        valid: true,
        counts: { standards_alignment: 4, sources: 12, signals: 5, candidates: 5 }
      })

      const result = yield* scientificIntuitionSearchData(
        "Which typed object separates unresolved intersections from zero?",
        "cpt::open:gate1-original-cycle-signed-global-intersections",
        8,
        1
      )
      expect(result.canonical_target).toMatchObject({
        id: "cpt::open:gate1-original-cycle-signed-global-intersections",
        type: "open_problem"
      })
      expect(result.non_authoritative_signals.map(({ id }) => id)).toEqual([
        "intuition:gate1-regulated-relative-class-inventory",
        "intuition:gate1-explicit-incidence-unknowns"
      ])
      expect(result.signal_selection).toEqual({
        mode: "EXACT_TARGET_FILE_ORDER",
        query_ranking: false,
        matched: 2,
        returned: 2,
        limit: 20
      })
      expect(result.federated_links).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ relation: "TARGETS_CANONICAL_OPEN_PROBLEM" }),
          expect.objectContaining({ relation: "CITES_SOURCE" }),
          expect.objectContaining({ relation: "MIRRORS_CANONICAL_SOURCE" })
        ])
      )
      expect(result.contract).toMatchObject({
        authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
        canonical_graph_unchanged: true,
        does_not_authorize_execution: true
      })
    })
  )
})
