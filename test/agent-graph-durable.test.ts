import { access, mkdtemp, rm, symlink, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { expect, it } from "vitest"
import type { GraphRagHit, GraphRagSearchResult } from "../src/graphrag/core.ts"
import { planResearchAgentWorkflow } from "../src/agent-graph/core.ts"
import {
  applyResearchAgentReview,
  auditResearchAgentRun,
  createResearchAgentRun,
  evaluateDurableWorkflowCases,
  type ResearchAgentRevisionPin
} from "../src/agent-graph/durable.ts"
import {
  readResearchAgentRun,
  updateResearchAgentRun,
  writeNewResearchAgentRun
} from "../src/agent-graph/store.ts"

const hash = (character: string): string => character.repeat(64)

const revisionPin = (): ResearchAgentRevisionPin => ({
  head_commit: "a".repeat(40),
  collection: { path: "ontology/collection.json", sha256: hash("b") },
  graphs: [{ path: "ontology/cpt-temporal-folded-susy/graph.json", sha256: hash("c") }],
  source_documents: [{ path: "docs/decisions/ICE_TOE_CRITICAL_PATH_ROUTING_2026-09-01.md", sha256: hash("d") }],
  control_plane_sources: [{ path: "src/agent-graph/core.ts", sha256: hash("e") }]
})

const gateOne = "open:gate1-original-cycle-signed-global-intersections"

const hit: GraphRagHit = {
  unit: {
    id: `cpt::${gateOne}`,
    graph: "cpt",
    node_id: gateOne,
    node_type: "open_problem",
    state: "OPEN",
    title: "Gate 1 original cycle and signed global intersections",
    text: "Gate 1 original joint cycle and signed global intersection vector"
  },
  rank: 1,
  match: "DIRECT_HYBRID",
  distance: 0,
  scores: { bm25: 1, lexical_hash_vector: 1, graph_expansion: 0, combined: 2 },
  traversed_edges: [],
  community_id: "cpt:fixture"
}

const retrieval = (hits: ReadonlyArray<GraphRagHit>): GraphRagSearchResult => ({
  schema: "ice-evidence-graph-rag-search/v1",
  contract: {
    schema: "ice-evidence-graph-rag/v1",
    mode: "DETERMINISTIC_EVIDENCE_FIRST_HUMAN_DIRECTED",
    source_of_truth: "REPOSITORY_ONTOLOGY_JSON",
    model_extracted_entities: false,
    automatic_follow_up: false,
    execution_authorization: "NOT_GRANTED"
  },
  query: "gate one",
  graph: "cpt",
  limit: 12,
  depth: 1,
  index: { text_units: 1, communities: 1, retrieval: "BM25 + deterministic lexical hash vector + bounded graph expansion" },
  hits,
  communities: [],
  guidance: []
})

const currentPlan = () =>
  planResearchAgentWorkflow(
    "Gate 1 original joint cycle and signed global intersection vector",
    retrieval([hit])
  )

const input = (run_id = "durable-g1-run") => ({
  run_id,
  at: "2026-09-02T00:00:00.000Z",
  plan: currentPlan(),
  revision_pin: revisionPin()
})

it("records only the finite human-review path and closes without execution authority", () => {
  let run = createResearchAgentRun(input())
  expect(run.status).toBe("AWAITING_ROUTE_REVIEW")
  run = applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "APPROVE", rationale: "Human confirmed the current blocker.", observed_revision_pin: run.revision_pin
  })
  expect(run.status).toBe("AWAITING_EVIDENCE_REVIEW")
  run = applyResearchAgentReview(run, {
    at: "2026-09-02T00:02:00.000Z", stage: "EVIDENCE", decision: "APPROVE", rationale: "Human scoped source review.", observed_revision_pin: run.revision_pin
  })
  run = applyResearchAgentReview(run, {
    at: "2026-09-02T00:03:00.000Z", stage: "DESIGN", decision: "APPROVE", rationale: "Human recorded a bounded design decision.", observed_revision_pin: run.revision_pin
  })
  expect(run.status).toBe("CLOSED")
  expect(run.contract.execution_authorization).toBe("NOT_GRANTED")
  expect(run.handoff.authorization).toBe("NOT_GRANTED")
  expect(auditResearchAgentRun(run, revisionPin()).passed).toBe(true)
  expect(() => applyResearchAgentReview(run, {
    at: "2026-09-02T00:04:00.000Z", stage: "DESIGN", decision: "APPROVE", rationale: "must not reopen", observed_revision_pin: run.revision_pin
  })).toThrow("not available")
})

it("stops at any review point and cannot approve a non-current route", () => {
  const run = createResearchAgentRun(input("durable-stop-run"))
  const stopped = applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "STOP_OR_REFRAME", rationale: "The proposed object is not bounded enough.", observed_revision_pin: run.revision_pin
  })
  expect(stopped.status).toBe("STOPPED")
  const nonCurrent = createResearchAgentRun({
    ...input("durable-noncurrent-run"),
    plan: planResearchAgentWorkflow("Which source constrains the bound?", retrieval([]))
  })
  expect(() => applyResearchAgentReview(nonCurrent, {
    at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "APPROVE", rationale: "not permitted", observed_revision_pin: nonCurrent.revision_pin
  })).toThrow("current-blocker")
})

it("detects trace rewrites and revision drift before a run can resume", () => {
  const run = createResearchAgentRun(input("durable-audit-run"))
  const tampered = { ...run, trace: run.trace.map((event, index) => index === 0 ? { ...event, input_sha256: hash("e") } : event) }
  expect(auditResearchAgentRun(tampered).passed).toBe(false)
  expect(auditResearchAgentRun(tampered).errors.join(" ")).toContain("hash mismatch")
  const reviewed = applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "APPROVE", rationale: "reviewed", observed_revision_pin: run.revision_pin
  })
  const decisionTampered = {
    ...reviewed,
    decisions: reviewed.decisions.map((decision, index) =>
      index === 1 ? { ...decision, rationale: "rewritten after review" } : decision
    )
  }
  expect(auditResearchAgentRun(decisionTampered).errors.join(" ")).toContain("not bound")
  const drifted = { ...revisionPin(), collection: { path: "ontology/collection.json", sha256: hash("f") } }
  expect(auditResearchAgentRun(run, drifted).errors.join(" ")).toContain("revision drift")
  expect(() => applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "APPROVE", rationale: "must fail drift", observed_revision_pin: drifted
  })).toThrow("revision drift")
})

it("rejects malformed persisted runtime values before state-machine audit", () => {
  const run = createResearchAgentRun(input("durable-runtime-decode-run"))
  const malformedActor = {
    ...run,
    decisions: run.decisions.map((decision) =>
      ({ ...decision, actor: "agent" })
    )
  }
  expect(auditResearchAgentRun(malformedActor).errors.join(" ")).toContain(
    "actor must be human"
  )
  const reviewed = applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z",
    stage: "ROUTE",
    decision: "APPROVE",
    rationale: "typed review",
    observed_revision_pin: run.revision_pin
  })
  const malformedDecision = {
    ...reviewed,
    decisions: reviewed.decisions.map((decision, index) =>
      index === 1 ? { ...decision, decision: "AUTOMATIC_APPROVE" } : decision
    )
  }
  expect(auditResearchAgentRun(malformedDecision).errors.join(" ")).toContain(
    "stage or decision is invalid"
  )
  expect(
    auditResearchAgentRun({
      ...run,
      revision_pin: { ...run.revision_pin, control_plane_sources: [] }
    }).errors.join(" ")
  ).toContain("at least one control-plane source")
})

it("rechecks route eligibility and the exact finite event sequence during audit", () => {
  const run = createResearchAgentRun(input("durable-audit-route-run"))
  const reviewed = applyResearchAgentReview(run, {
    at: "2026-09-02T00:01:00.000Z",
    stage: "ROUTE",
    decision: "APPROVE",
    rationale: "current route",
    observed_revision_pin: run.revision_pin
  })
  const forgedPlan = planResearchAgentWorkflow(
    "Which source constrains the bound?",
    retrieval([])
  )
  expect(
    auditResearchAgentRun({ ...reviewed, plan: forgedPlan }).errors.join(" ")
  ).toContain("approves a non-current route")
  const extraEvent = {
    ...run.trace.at(-1)!,
    sequence: 3,
    previous_event_sha256: run.trace.at(-1)!.event_sha256
  }
  expect(
    auditResearchAgentRun({ ...run, trace: [...run.trace, extraEvent] }).errors.join(" ")
  ).toContain("finite review state machine")
})

it("evaluates representative complete and stopped workflows without I/O", () => {
  const complete = input("durable-eval-complete")
  const stopped = input("durable-eval-stopped")
  const evaluation = evaluateDurableWorkflowCases([
    {
      id: "current-blocker-three-review-close",
      create: complete,
      reviews: [
        { at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "APPROVE", rationale: "route" },
        { at: "2026-09-02T00:02:00.000Z", stage: "EVIDENCE", decision: "APPROVE", rationale: "evidence" },
        { at: "2026-09-02T00:03:00.000Z", stage: "DESIGN", decision: "APPROVE", rationale: "design" }
      ],
      expected_status: "CLOSED"
    },
    {
      id: "human-stop-is-terminal",
      create: stopped,
      reviews: [{ at: "2026-09-02T00:01:00.000Z", stage: "ROUTE", decision: "STOP_OR_REFRAME", rationale: "stop" }],
      expected_status: "STOPPED"
    }
  ])
  expect(evaluation.passed).toBe(true)
  expect(evaluation.cases.map(({ actual_status }) => actual_status)).toEqual(["CLOSED", "STOPPED"])
})

it("persists with exclusive creation, integrity checks, and optimistic trace-tip updates", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-agent-store-"))
  try {
    const run = createResearchAgentRun(input("durable-store-run"))
    await expect(writeNewResearchAgentRun(root, run)).resolves.toBe(
      ".ice/agent-runs/durable-store-run.json"
    )
    await expect(writeNewResearchAgentRun(root, run)).rejects.toThrow()
    await expect(readResearchAgentRun(root, run.run_id)).resolves.toEqual(run)
    const tip = run.trace.at(-1)?.event_sha256
    expect(tip).toBeDefined()
    const reviewed = await updateResearchAgentRun(
      root,
      run.run_id,
      tip ?? "",
      (stored) =>
        applyResearchAgentReview(stored, {
          at: "2026-09-02T00:01:00.000Z",
          stage: "ROUTE",
          decision: "STOP_OR_REFRAME",
          rationale: "Store test records an explicit stop.",
          observed_revision_pin: stored.revision_pin
        })
    )
    expect(reviewed.status).toBe("STOPPED")
    await expect(
      updateResearchAgentRun(root, run.run_id, tip ?? "", (stored) => stored)
    ).rejects.toThrow("changed since review began")
    await writeFile(
      join(root, ".ice", "agent-runs", "durable-store-run.json"),
      JSON.stringify({ ...reviewed, status: "CLOSED" })
    )
    await expect(readResearchAgentRun(root, run.run_id)).rejects.toThrow(
      "failed integrity audit"
    )
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("does not create an agent-run directory during a read-only lookup", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-agent-readonly-"))
  try {
    await expect(readResearchAgentRun(root, "missing-run")).rejects.toThrow()
    await expect(access(join(root, ".ice"))).rejects.toThrow()
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("refuses an out-of-workspace durable state symlink before creating files", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-agent-symlink-root-"))
  const outside = await mkdtemp(join(tmpdir(), "ice-agent-symlink-outside-"))
  try {
    await symlink(outside, join(root, ".ice"), "dir")
    await expect(
      writeNewResearchAgentRun(
        root,
        createResearchAgentRun(input("durable-symlink-run"))
      )
    ).rejects.toThrow("outside the workspace")
    await expect(access(join(outside, "agent-runs"))).rejects.toThrow()
  } finally {
    await rm(root, { recursive: true, force: true })
    await rm(outside, { recursive: true, force: true })
  }
})
