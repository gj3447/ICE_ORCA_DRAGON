import { createHash } from "node:crypto"
import { expect, it } from "vitest"
import rdf from "rdf-ext"
import {
  OntologyCompetencySuiteError,
  decodeOntologyCompetencySuite,
  evaluateOntologyCompetencySuite,
  ONTOLOGY_COMPETENCY_SUITE_RELPATH,
  type LoadedOntologyCompetencySuite
} from "../src/ontology/competency.ts"

const fixture = {
  schema: "ice-ontology-competency-suite/v1",
  id: "ontology-core-questions",
  title: "Ontology core questions",
  description: "Stable bounded graph questions for an RDF projection fixture.",
  version: "2026-09-02",
  cases: [
    {
      id: "known-fact",
      question: "Is the fixture fact present?",
      query: "ASK { <urn:test:subject> <urn:test:predicate> <urn:test:object> }",
      expected_boolean: true,
      rationale: "The fixture asserts this one graph fact."
    },
    {
      id: "absent-fact",
      question: "Is the fixture missing fact absent?",
      query: "ASK { <urn:test:subject> <urn:test:predicate> <urn:test:missing> }",
      expected_boolean: false,
      rationale: "The fixture deliberately omits this object."
    }
  ],
  guidance: ["Competency cases are graph-query regression controls."]
}

const loadedFixture = (): LoadedOntologyCompetencySuite => {
  const source = JSON.stringify(fixture)
  return {
    suite: decodeOntologyCompetencySuite(source, "fixture"),
    provenance: {
      path: ONTOLOGY_COMPETENCY_SUITE_RELPATH,
      sha256: createHash("sha256").update(source).digest("hex"),
      byte_length: new TextEncoder().encode(source).byteLength
    }
  }
}

it("decodes and evaluates fixed ASK competency questions deterministically", async () => {
  const dataset = rdf.dataset()
  dataset.add(
    rdf.quad(
      rdf.namedNode("urn:test:subject"),
      rdf.namedNode("urn:test:predicate"),
      rdf.namedNode("urn:test:object")
    )
  )

  const report = await evaluateOntologyCompetencySuite(dataset, loadedFixture())

  expect(report).toMatchObject({
    schema: "ice-ontology-competency-report/v1",
    total_cases: 2,
    passed_cases: 2,
    failed_cases: 0,
    passed: true,
    suite: { path: ONTOLOGY_COMPETENCY_SUITE_RELPATH }
  })
  expect(report.cases).toEqual([
    expect.objectContaining({ id: "known-fact", observed_boolean: true, passed: true }),
    expect.objectContaining({ id: "absent-fact", observed_boolean: false, passed: true })
  ])
  expect(report.guidance.join(" ")).toContain("does not validate scientific truth")
})

it("rejects unknown fields and non-ASK competency queries", async () => {
  expect(() =>
    decodeOntologyCompetencySuite(JSON.stringify({ ...fixture, unreviewed: true }), "fixture")
  ).toThrow(OntologyCompetencySuiteError)
  expect(() =>
    decodeOntologyCompetencySuite(
      JSON.stringify({
        ...fixture,
        cases: [{ ...fixture.cases[0], expected_boolean: "true" }]
      }),
      "fixture"
    )
  ).toThrow("expected_boolean must be boolean")

  const dataset = rdf.dataset()
  const source = JSON.stringify({
    ...fixture,
    cases: [{ ...fixture.cases[0], query: "SELECT ?s WHERE { ?s ?p ?o }" }]
  })
  const loaded: LoadedOntologyCompetencySuite = {
    suite: decodeOntologyCompetencySuite(source, "fixture"),
    provenance: {
      path: ONTOLOGY_COMPETENCY_SUITE_RELPATH,
      sha256: createHash("sha256").update(source).digest("hex"),
      byte_length: new TextEncoder().encode(source).byteLength
    }
  }
  await expect(evaluateOntologyCompetencySuite(dataset, loaded)).rejects.toThrow(
    "must use an ASK query"
  )
})
