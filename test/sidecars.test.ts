import { readFileSync } from "node:fs"
import { NodeContext } from "@effect/platform-node"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import {
  sidecarCollectionShowData,
  sidecarCollectionSummaryData,
  sidecarCollectionValidateData
} from "../src/sidecars/commands.ts"
import { SidecarCollectionError, decodeSidecarCollection } from "../src/sidecars/model.ts"
import { WorkspaceLive } from "../src/workspace.ts"

const source = readFileSync(
  new URL("../research/sidecars/collection.v1.json", import.meta.url),
  "utf8"
)

it("decodes the strict non-authoritative sidecar registry", () => {
  const raw = JSON.parse(source) as Record<string, unknown>
  expect(() => decodeSidecarCollection(JSON.stringify({ ...raw, unknown: true }))).toThrow(SidecarCollectionError)
  expect(() => decodeSidecarCollection(JSON.stringify({ ...raw, result: "claim" }))).toThrow("forbidden field 'result'")
  expect(() => decodeSidecarCollection(JSON.stringify({ ...raw, updated_at_utc: "2026-02-30T00:00:00Z" }))).toThrow("must be UTC ISO-8601")
})

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("sidecar registry CLI data", (it) => {
  it.effect("validates fixed bytes and exposes only non-authoritative locators", () =>
    Effect.gen(function* () {
      const report = yield* sidecarCollectionValidateData
      expect(report).toMatchObject({
        valid: true,
        authority: "NON_AUTHORITATIVE_SIDECAR_REGISTRY",
        canonical_graph_unchanged: true,
        does_not_authorize_execution: true,
        counts: { entries: 3, frozen_snapshots: 1, active_hypothesis_generation: 1, active_method_protocol: 1 }
      })

      const summary = yield* sidecarCollectionSummaryData
      expect(summary.entries.map(({ id }) => id)).toEqual([
        "sidecar:scientific-intuition-gate1-v1",
        "sidecar:scientific-intuition-ice-v2",
        "sidecar:external-comparator-v1"
      ])

      const shown = yield* sidecarCollectionShowData("sidecar:external-comparator-v1")
      expect(shown).toMatchObject({
        entry: { kind: "COMPARATOR_PROTOCOL_V1", does_not_authorize_execution: true },
        contract: { canonical_graph_unchanged: true }
      })

      const missing = yield* sidecarCollectionShowData("sidecar:missing").pipe(Effect.flip)
      expect(missing).toMatchObject({ code: "SIDECAR_COLLECTION_TARGET_NOT_FOUND", exitCode: 2 })
    })
  )
})
