import { expect, it } from "vitest"
import {
  diffResearchCollections,
  makeResearchCollectionReviewWarnings
} from "../src/ontology/collection-diff.ts"
import type { ResearchCollection } from "../src/ontology/collection.ts"

const collection = (): ResearchCollection => ({
  schema_version: "research-collection/v1",
  collection_id: "research-collection:collection-diff-test",
  title: "Collection diff fixture",
  description: "A deterministic collection diff fixture.",
  updated_at_utc: "2026-09-01T00:00:00Z",
  canonical_file: "ontology/collection.json",
  default_graph: "alpha",
  graphs: [
    {
      key: "alpha",
      graph_id: "research-graph:alpha",
      path: "ontology/alpha/graph.json",
      guide: "ontology/alpha/README.md",
      entry_node: "programme:alpha",
      coverage: "PARTIAL",
      corpus_roots: ["research/alpha"],
      includes: ["alpha fixture"],
      excludes: ["everything else"]
    },
    {
      key: "beta",
      graph_id: "research-graph:beta",
      path: "ontology/beta/graph.json",
      guide: "ontology/beta/README.md",
      entry_node: "programme:beta",
      coverage: "INDEX_ONLY",
      corpus_roots: ["research/beta"],
      includes: ["beta fixture"],
      excludes: ["everything else"]
    }
  ],
  quick_answers: [
    {
      question: "Where is alpha?",
      answer: "In alpha.",
      refs: [{ graph: "alpha", node: "programme:alpha" }]
    }
  ],
  reading_paths: [
    {
      id: "collection-path:alpha",
      title: "Alpha path",
      summary: "Start at alpha.",
      navigation_only: true,
      stops: [{ graph: "alpha", node: "programme:alpha" }]
    }
  ],
  coverage_ledger: [
    {
      path: "research/alpha",
      status: "PARTIAL",
      graph: "alpha",
      reason: "Fixture coverage"
    }
  ]
})

it("reports no delta for canonically equal collections", () => {
  const result = diffResearchCollections(collection(), collection())

  expect(result.summary).toEqual({
    metadata_changes: 0,
    graph_descriptors: { added: 0, removed: 0, changed: 0 },
    quick_answers: { added: 0, removed: 0, changed: 0 },
    reading_paths: { added: 0, removed: 0, changed: 0 },
    coverage_ledger: { added: 0, removed: 0, changed: 0 },
    total_changes: 0,
    has_changes: false
  })
  expect(result.metadata).toEqual([])
})

it("reports deterministic collection metadata and record deltas", () => {
  const base = collection()
  const current: ResearchCollection = {
    ...base,
    title: "Changed collection fixture",
    updated_at_utc: "2026-09-01T01:00:00Z",
    graphs: [
      {
        key: "gamma",
        graph_id: "research-graph:gamma",
        path: "ontology/gamma/graph.json",
        guide: "ontology/gamma/README.md",
        entry_node: "programme:gamma",
        coverage: "DETAILED",
        corpus_roots: ["research/gamma"],
        includes: ["gamma fixture"],
        excludes: []
      },
      {
        ...base.graphs[0]!,
        coverage: "DETAILED"
      }
    ],
    quick_answers: [{
      ...base.quick_answers[0]!,
      answer: "Still in alpha, with updated context."
    }],
    reading_paths: [{
      ...base.reading_paths[0]!,
      title: "Changed alpha path"
    }, {
      id: "collection-path:gamma",
      title: "Gamma path",
      summary: "Start at gamma.",
      navigation_only: true,
      stops: [{ graph: "gamma", node: "programme:gamma" }]
    }],
    coverage_ledger: [{
      ...base.coverage_ledger[0]!,
      reason: "Changed fixture coverage"
    }, {
      path: "research/gamma",
      status: "INDEXED",
      graph: "gamma",
      reason: "Gamma fixture coverage"
    }]
  }

  const result = diffResearchCollections(base, current)

  expect(result.metadata.map(({ field }) => field)).toEqual([
    "title",
    "updated_at_utc"
  ])
  expect(result.graph_descriptors.added.map(({ key }) => key)).toEqual(["gamma"])
  expect(result.graph_descriptors.removed.map(({ key }) => key)).toEqual(["beta"])
  expect(result.graph_descriptors.changed.map(({ id }) => id)).toEqual(["alpha"])
  expect(result.quick_answers.changed).toMatchObject([
    { key: "Where is alpha?", index: 0 }
  ])
  expect(result.reading_paths.added.map(({ id }) => id)).toEqual([
    "collection-path:gamma"
  ])
  expect(result.reading_paths.changed.map(({ id }) => id)).toEqual([
    "collection-path:alpha"
  ])
  expect(result.coverage_ledger.added).toMatchObject([
    { key: "research/gamma", index: 0 }
  ])
  expect(result.coverage_ledger.changed).toMatchObject([
    { key: "research/alpha", index: 0 }
  ])
  expect(result.summary).toMatchObject({ total_changes: 10, has_changes: true })
})

it("is order-independent for descriptors and uses canonical occurrence keys for duplicates", () => {
  const base: ResearchCollection = {
    ...collection(),
    quick_answers: [
      {
        question: "Duplicate?",
        answer: "B",
        refs: [{ graph: "alpha", node: "programme:alpha" }]
      },
      {
        question: "Duplicate?",
        answer: "A",
        refs: [{ graph: "beta", node: "programme:beta" }]
      }
    ],
    coverage_ledger: [
      { path: "shared", status: "UNINDEXED", reason: "B" },
      { path: "shared", status: "ARCHIVE", reason: "A" }
    ]
  }
  const reordered: ResearchCollection = {
    ...base,
    graphs: [base.graphs[1]!, base.graphs[0]!] as ResearchCollection["graphs"],
    quick_answers: [...base.quick_answers].reverse(),
    reading_paths: [...base.reading_paths].reverse(),
    coverage_ledger: [...base.coverage_ledger].reverse()
  }

  expect(diffResearchCollections(base, reordered).summary.has_changes).toBe(false)

  const changed: ResearchCollection = {
    ...base,
    quick_answers: [
      {
        question: "Duplicate?",
        answer: "C",
        refs: [{ graph: "alpha", node: "programme:alpha" }]
      },
      base.quick_answers[1]!
    ]
  }
  const result = diffResearchCollections(base, changed)
  expect(result.quick_answers.changed).toHaveLength(1)
  expect(result.quick_answers.changed[0]).toMatchObject({
    key: "Duplicate?",
    index: 1
  })
})

it("warns when collection content and its timestamp disagree", () => {
  const base = collection()
  const changedContent: ResearchCollection = {
    ...base,
    title: "Changed without timestamp"
  }
  expect(
    makeResearchCollectionReviewWarnings(
      base,
      changedContent,
      diffResearchCollections(base, changedContent)
    ).map(({ code }) => code)
  ).toEqual(["ONTOLOGY_COLLECTION_REVIEW_UPDATED_AT_UNCHANGED"])

  const timestampOnly: ResearchCollection = {
    ...base,
    updated_at_utc: "2026-09-01T03:00:00Z"
  }
  expect(
    makeResearchCollectionReviewWarnings(
      base,
      timestampOnly,
      diffResearchCollections(base, timestampOnly)
    ).map(({ code }) => code)
  ).toEqual(["ONTOLOGY_COLLECTION_REVIEW_TIMESTAMP_ONLY"])
})
