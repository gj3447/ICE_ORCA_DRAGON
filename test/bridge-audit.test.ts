import { readFileSync } from "node:fs"
import { NodeContext } from "@effect/platform-node"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import { auditBridgeResolution, decodeBridgeResolutionAudit } from "../src/bridges/core.ts"
import { bridgeAuditShowCommand, bridgeAuditSummaryCommand, bridgeAuditValidateData } from "../src/bridges/commands.ts"
import { WorkspaceLive } from "../src/workspace.ts"
import { loadValidOntologyCollectionStructure } from "../src/ontology/repository.ts"

const source = readFileSync(new URL("../research/benchmarks/ice-kg-bridge-resolution-audit.v1.json", import.meta.url), "utf8")
const audit = decodeBridgeResolutionAudit(source)
const TestLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(TestLayer)("bridge audit live layer", (it) => {
  it.effect("locks all current unresolved bridge keys and reports no fabricated match", () => Effect.gen(function* () {
    const ontology = yield* loadValidOntologyCollectionStructure
    const report = auditBridgeResolution(audit, ontology.graphs)
    expect(report).toMatchObject({ valid: true, resolved_matches: 0, counts: { NO_MATCH: 51, ID_COLLISION: 23, REGISTRY_UNAVAILABLE: 1 } })
    expect(report.bridges).toHaveLength(75)
    expect(report.bridges.find(({ local_node_id }) => local_node_id === "phase:p24")).toMatchObject({ outcome: "ID_COLLISION", rule_id: "rule:cpt-symposium-number-collision" })
  }))

  it.effect("exposes validate data and a unique local-id show path read-only", () => Effect.gen(function* () {
    const report = yield* bridgeAuditValidateData
    expect(report.valid).toBe(true)
    yield* bridgeAuditSummaryCommand(false)
    yield* bridgeAuditShowCommand("phase:p24", false)
  }))
})

it("fails closed if a lookup key or the exact bridge keyset changes", () => {
  const fixture = [{ descriptor: { path: "ontology/cpt-temporal-folded-susy/graph.json" }, graph: { kg_bridges: [{ local_node_id: "phase:p24", system: "SYMPOSIUM", status: "UNRESOLVED", lookup_key: "changed" }] } }] as never
  expect(auditBridgeResolution(audit, fixture).errors).toEqual(expect.arrayContaining(["CANONICAL_GRAPH_SET_MISMATCH", "UNRESOLVED_COUNT_MISMATCH", "UNRESOLVED_KEYSET_OR_LOOKUP_KEY_MISMATCH"]))
})

it("strictly rejects unknown audit fields and incomplete collision locators", () => {
  const parsed = JSON.parse(source) as Record<string, unknown>
  expect(() =>
    decodeBridgeResolutionAudit(
      JSON.stringify({ ...parsed, external_uid: "invented" })
    )
  ).toThrow("unknown field 'external_uid'")

  const rules = parsed.rules as ReadonlyArray<Record<string, unknown>>
  const first = rules[0]
  if (first === undefined) throw new Error("bridge audit fixture has no rules")
  const locator = first.registry_locator as Record<string, unknown>
  expect(() =>
    decodeBridgeResolutionAudit(
      JSON.stringify({
        ...parsed,
        rules: [
          {
            ...first,
            registry_locator: { ...locator, blob_oid: undefined }
          },
          ...rules.slice(1)
        ]
      })
    )
  ).toThrow("blob_oid must be a non-empty string")
})
