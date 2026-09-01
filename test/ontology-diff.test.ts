import { expect, it } from "vitest"
import { diffResearchGraphs } from "../src/ontology/diff.ts"
import type { ResearchGraph } from "../src/ontology/model.ts"

const graph = (): ResearchGraph => ({
  schema_version: "research-graph/v1",
  graph_id: "research-graph:diff-test",
  title: "Diff fixture",
  description: "A deterministic graph diff fixture.",
  updated_at_utc: "2026-09-01T00:00:00Z",
  canonical_file: "ontology/diff-test/graph.json",
  source_inventory: "ontology/diff-test/sources.md",
  quick_answers: [{ question: "What changed?", answer: "Nothing.", claim_ids: ["claim:BASE"] }],
  reading_paths: [{
    id: "reading-path:base",
    title: "Base path",
    summary: "Reach the base claim.",
    nodes: ["programme:diff-test", "claim:BASE"]
  }],
  node_type_legend: { programme: "programme", claim: "claim", evidence: "evidence" },
  relation_legend: { PART_OF: "membership", HAS_EVIDENCE: "evidence" },
  nodes: [
    { id: "programme:diff-test", type: "programme", title: "Programme", summary: "Fixture programme.", state: "ACTIVE" },
    {
      id: "claim:BASE",
      type: "claim",
      title: "Base claim",
      summary: "A base claim.",
      state: "SUPPORTED",
      claim_id: "BASE",
      statement: "The base claim holds.",
      epistemic_state: "SUPPORTED"
    },
    { id: "evidence:base", type: "evidence", title: "Base evidence", summary: "One observation.", state: "VALID", observed_status: "PASS" }
  ],
  edges: [
    { id: "edge:2", from: "claim:BASE", relation: "HAS_EVIDENCE", to: "evidence:base", polarity: "SUPPORTS" },
    { id: "edge:1", from: "claim:BASE", relation: "PART_OF", to: "programme:diff-test" }
  ],
  kg_bridges: [{
    local_node_id: "claim:BASE",
    system: "TEST",
    external_uid: null,
    relation: null,
    status: "UNRESOLVED",
    lookup_key: "base",
    checked_at_utc: "2026-09-01T00:00:00Z"
  }]
})

it("reports no delta for canonically equal graphs", () => {
  const result = diffResearchGraphs(graph(), graph())
  expect(result.summary).toEqual({
    metadata_changes: 0,
    nodes: { added: 0, removed: 0, changed: 0 },
    edges: { added: 0, removed: 0, changed: 0 },
    reading_paths: { added: 0, removed: 0, changed: 0 },
    quick_answers: { added: 0, removed: 0, changed: 0 },
    kg_bridges: { added: 0, removed: 0, changed: 0 },
    total_changes: 0,
    has_changes: false
  })
  expect(result.metadata).toEqual([])
})

it("reports deterministic add, remove, change, and metadata deltas", () => {
  const base = graph()
  const current: ResearchGraph = {
    ...base,
    title: "Changed fixture",
    updated_at_utc: "2026-09-01T01:00:00Z",
    nodes: [
      { id: "concept:ADDED", type: "concept", title: "Added", summary: "New concept.", state: "DOCUMENTED" },
      ...base.nodes
        .filter(({ id }) => id !== "evidence:base")
        .map((node) => node.id === "claim:BASE" ? { ...node, summary: "An edited base claim." } : node)
    ],
    edges: [
      { id: "edge:3", from: "concept:ADDED", relation: "PART_OF", to: "programme:diff-test" },
      ...base.edges.filter(({ id }) => id !== "edge:2")
    ],
    reading_paths: [{ ...base.reading_paths[0]!, title: "Changed path" }, {
      id: "reading-path:added",
      title: "Added path",
      summary: "Reach the added concept.",
      nodes: ["programme:diff-test", "concept:ADDED"]
    }],
    quick_answers: [{ question: "What changed?", answer: "The base claim changed.", claim_ids: ["claim:BASE"] }],
    kg_bridges: [{ ...base.kg_bridges[0]!, status: "RESOLVED", external_uid: "uid:base", relation: "sameAs" }]
  }

  const result = diffResearchGraphs(base, current)

  expect(result.metadata.map(({ field }) => field)).toEqual(["title", "updated_at_utc"])
  expect(result.nodes.added.map(({ id }) => id)).toEqual(["concept:ADDED"])
  expect(result.nodes.removed.map(({ id }) => id)).toEqual(["evidence:base"])
  expect(result.nodes.changed.map(({ id }) => id)).toEqual(["claim:BASE"])
  expect(result.edges.added.map(({ id }) => id)).toEqual(["edge:3"])
  expect(result.edges.removed.map(({ id }) => id)).toEqual(["edge:2"])
  expect(result.reading_paths.added.map(({ id }) => id)).toEqual(["reading-path:added"])
  expect(result.reading_paths.changed.map(({ id }) => id)).toEqual(["reading-path:base"])
  expect(result.quick_answers.changed).toMatchObject([{ key: "What changed?", index: 0 }])
  expect(result.kg_bridges.changed).toMatchObject([{ key: "claim:BASE\u0000TEST\u0000base", index: 0 }])
  expect(result.summary).toMatchObject({ total_changes: 11, has_changes: true })
})

it("is order-independent and disambiguates ID-less duplicates by canonical occurrence index", () => {
  const base: ResearchGraph = {
    ...graph(),
    quick_answers: [
      { question: "Duplicate?", answer: "B", claim_ids: ["claim:BASE"] },
      { question: "Duplicate?", answer: "A", claim_ids: ["claim:BASE"] }
    ],
    kg_bridges: [
      { ...graph().kg_bridges[0]!, checked_at_utc: "2026-09-01T02:00:00Z" },
      { ...graph().kg_bridges[0]!, checked_at_utc: "2026-09-01T01:00:00Z" }
    ]
  }
  const reordered: ResearchGraph = {
    ...base,
    nodes: [...base.nodes].reverse(),
    edges: [...base.edges].reverse(),
    reading_paths: [...base.reading_paths].reverse(),
    quick_answers: [...base.quick_answers].reverse(),
    kg_bridges: [...base.kg_bridges].reverse()
  }

  expect(diffResearchGraphs(base, reordered).summary.has_changes).toBe(false)

  const changed: ResearchGraph = {
    ...base,
    quick_answers: [
      { question: "Duplicate?", answer: "C", claim_ids: ["claim:BASE"] },
      base.quick_answers[1]!
    ]
  }
  const delta = diffResearchGraphs(base, changed)
  expect(delta.quick_answers.changed).toHaveLength(1)
  expect(delta.quick_answers.changed[0]).toMatchObject({ key: "Duplicate?", index: 1 })
})
