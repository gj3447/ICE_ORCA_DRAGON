import { NodeContext } from "@effect/platform-node"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import type { CollectionGraph } from "../src/ontology/collection-core.ts"
import {
  scientificIntuitionSearchData,
  scientificIntuitionValidateData
} from "../src/intuition/commands.ts"
import {
  validateScientificIntuitionFlow,
  validateScientificIntuitionFlowV2
} from "../src/intuition/core.ts"
import {
  decodeScientificIntuitionFlow,
  decodeScientificIntuitionFlowV2,
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

const fixtureV2 = {
  schema_version: "scientific-intuition-flow/v2",
  graph_id: "intuition-flow:ice",
  title: "Fixture intuition graph",
  description: "A strictly bounded topic and canonical-context fixture.",
  updated_at_utc: "2026-09-03T00:00:00Z",
  authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
  canonical_graph_unchanged: true,
  does_not_authorize_execution: true,
  standards_alignment: fixture.standards_alignment,
  topics: [
    {
      id: "topic:first",
      title: "First topic",
      question: "Which typed object is missing?",
      scope: "Sidecar-only fixture scope.",
      non_claim: "This topic is not a claim.",
      does_not_authorize_execution: true
    },
    {
      id: "topic:second",
      title: "Second topic",
      question: "Which discriminator separates the alternatives?",
      scope: "Sidecar-only comparison scope.",
      non_claim: "This topic is not evidence.",
      does_not_authorize_execution: true
    }
  ],
  topic_links: [
    {
      id: "intuition-link:first-second",
      from: "topic:first",
      relation: "DISTINCT_FROM",
      to: "topic:second",
      rationale: "The fixture checks typed topic endpoints.",
      stop_condition: "Stop if an endpoint is unresolved.",
      non_claim: "This link is not a canonical relation.",
      does_not_authorize_execution: true
    }
  ],
  sources: fixture.sources,
  signals: fixture.signals.map(({ target, ...signal }, index) => ({
    ...signal,
    topic: index === 0 ? "topic:first" : "topic:second",
    canonical_target: target
  })),
  boundaries: ["No topic, link, or signal is canonical evidence or execution authority."]
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

it("strictly decodes v2 topic separation and optional canonical targets", () => {
  const flow = decodeScientificIntuitionFlowV2(JSON.stringify(fixtureV2), "fixture-v2")
  const report = validateScientificIntuitionFlowV2(flow, cptFixture)
  expect(report).toMatchObject({
    valid: true,
    authority: "NON_AUTHORITATIVE_HYPOTHESIS_GENERATION",
    canonical_graph_unchanged: true,
    does_not_authorize_execution: true,
    counts: {
      standards_alignment: 4,
      topics: 2,
      topic_links: 1,
      sources: 1,
      signals: 2,
      candidates: 2
    }
  })

  const missingTopic = decodeScientificIntuitionFlowV2(
    JSON.stringify({
      ...fixtureV2,
      signals: [{ ...fixtureV2.signals[0], topic: "topic:missing" }, fixtureV2.signals[1]]
    }),
    "fixture-v2"
  )
  expect(validateScientificIntuitionFlowV2(missingTopic, cptFixture).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "SIGNAL_TOPIC_NOT_FOUND" })])
  )

  const missingLinkTarget = decodeScientificIntuitionFlowV2(
    JSON.stringify({
      ...fixtureV2,
      topic_links: [{ ...fixtureV2.topic_links[0], to: "topic:missing" }]
    }),
    "fixture-v2"
  )
  expect(validateScientificIntuitionFlowV2(missingLinkTarget, cptFixture).errors).toEqual(
    expect.arrayContaining([expect.objectContaining({ code: "TOPIC_LINK_TO_NOT_FOUND" })])
  )
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

layer(AppLayer)("scientific-intuition topic and canonical federation", (it) => {
  it.effect("resolves exact targets, source bridges, and non-authoritative links", () =>
    Effect.gen(function* () {
      const report = yield* scientificIntuitionValidateData
      expect(report).toMatchObject({
        valid: true,
        counts: {
          standards_alignment: 4,
          topics: 6,
          topic_links: 6,
          sources: 27,
          signals: 19,
          candidates: 19
        }
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
        matched_by: "CANONICAL_TARGET",
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

      // Boundary-state questions stay at this exact supporting target, even when
      // query text mentions G1; the earlier G1 assertion excludes these lenses.
      const seamState = yield* scientificIntuitionSearchData(
        "Does G1 follow from carrier cohomology and boundary sewing?",
        "cpt::open:starobinsky-seam-ward-boundary-state-limit",
        8,
        1
      )
      expect(seamState.canonical_target).toMatchObject({
        id: "cpt::open:starobinsky-seam-ward-boundary-state-limit",
        type: "open_problem"
      })
      expect(seamState.non_authoritative_signals.map(({ id }) => id)).toEqual([
        "intuition:carrier-comparison-preserves-which-cohomology",
        "intuition:bulk-doublets-retain-endpoint-memory",
        "intuition:same-carrier-observable-and-positive-product"
      ])
      expect(seamState.non_authoritative_signals.every((signal) =>
        signal.status === "CANDIDATE" && signal.does_not_authorize_execution
      )).toBe(true)
      expect(seamState.federated_links).toEqual(expect.arrayContaining([
        expect.objectContaining({ relation: "MIRRORS_CANONICAL_SOURCE" }),
        expect.objectContaining({ relation: "TARGETS_CANONICAL_OPEN_PROBLEM" })
      ]))

      const geometry = yield* scientificIntuitionSearchData(
        "Which invariant separates geometry from an effective fluid?",
        "intuition::topic:geometry-energy-unification",
        8,
        1
      )
      expect(geometry.canonical_target).toBeNull()
      expect(geometry.canonical_context).toBeNull()
      expect(geometry.sidecar_target).toMatchObject({
        id: "topic:geometry-energy-unification",
        does_not_authorize_execution: true
      })
      expect(geometry.non_authoritative_signals.map(({ id }) => id)).toEqual([
        "intuition:ice-geometric-action-versus-effective-fluid-relabeling",
        "intuition:ice-vacuum-weyl-and-degree-of-freedom-check",
        "intuition:ice-geometric-sector-cross-domain-correlation"
      ])
      expect(geometry.signal_selection).toMatchObject({
        mode: "EXACT_TARGET_FILE_ORDER",
        query_ranking: false,
        matched_by: "TOPIC",
        matched: 3,
        returned: 3
      })
      expect(geometry.federated_links).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ relation: "BELONGS_TO_SIDECAR_TOPIC" }),
          expect.objectContaining({ relation: "CITES_SOURCE" })
        ])
      )
      expect(geometry.federated_links).not.toEqual(
        expect.arrayContaining([
          expect.objectContaining({ relation: "TARGETS_CANONICAL_OPEN_PROBLEM" })
        ])
      )

      const crossSheetCharge = yield* scientificIntuitionSearchData(
        "Is CPT sewing distinct from a physical fermion-odd charge?",
        "cpt::open:gate4-spinorial-charge-domain-constraint-closure",
        8,
        1
      )
      expect(crossSheetCharge.non_authoritative_signals.map(({ id }) => id)).toEqual([
        "intuition:ice-cpt-pin-sewing-versus-physical-cross-sheet-charge"
      ])

      const persistentSpectrum = yield* scientificIntuitionSearchData(
        "What survives dilution and moves an interacting retarded pole?",
        "cpt::open:gate5-persistent-order-and-pole-splitting",
        8,
        1
      )
      expect(persistentSpectrum.non_authoritative_signals.map(({ id }) => id)).toEqual([
        "intuition:ice-persistent-breaking-to-cross-domain-observable"
      ])
      expect([
        ...geometry.non_authoritative_signals,
        ...crossSheetCharge.non_authoritative_signals,
        ...persistentSpectrum.non_authoritative_signals
      ]).toEqual(expect.arrayContaining([
        expect.objectContaining({
          status: "CANDIDATE",
          does_not_authorize_execution: true
        })
      ]))
    })
  )
})
