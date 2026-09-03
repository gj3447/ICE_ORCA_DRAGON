import { readFileSync } from "node:fs"
import { NodeContext } from "@effect/platform-node"
import { expect, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import {
  auditResearchFamilyIndex,
  decodeResearchFamilyIndex,
  type ResearchFamilyIndex
} from "../src/ontology/family-index.ts"
import { ontologyFamilyIndexData } from "../src/ontology/commands.ts"
import { loadValidOntologyCollectionStructure } from "../src/ontology/repository.ts"
import { Workspace, WorkspaceLive } from "../src/workspace.ts"

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)
const source = readFileSync("ontology/research-family-index.v1.json", "utf8")

layer(AppLayer)("PARTIAL-corpus research family index", (it) => {
  it.effect("covers every PARTIAL root with stable family and decisive-unit metadata", () =>
    Effect.gen(function* () {
      const report = yield* ontologyFamilyIndexData
      expect(report.valid).toBe(true)
      expect(report.coverage_status_remains).toBe("PARTIAL")
      expect(report.families).toHaveLength(6)
      expect(report.totals).toEqual({
        filesystem_files: 190,
        excluded_generated_files: 50,
        ordinary_files: 140,
        decisive_files: 59,
        unassigned_ordinary_files: 81
      })
      expect(report.errors).toEqual([])
    })
  )

  it.effect("fails when a recorded family digest no longer matches the files", () =>
    Effect.gen(function* () {
      const index = yield* decodeResearchFamilyIndex(source)
      const loaded = yield* loadValidOntologyCollectionStructure
      const workspace = yield* Workspace
      const first = index.families[0]
      const altered = {
        ...index,
        families: [
          { ...first, inventory_sha256: "0".repeat(64) },
          ...index.families.slice(1)
        ]
      } as ResearchFamilyIndex
      const report = yield* Effect.promise(() =>
        auditResearchFamilyIndex(
          workspace.root,
          altered,
          loaded.collection,
          loaded.graphs
        )
      )
      expect(report.valid).toBe(false)
      expect(report.errors).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            code: "RESEARCH_FAMILY_INVENTORY_MISMATCH",
            subject: first.id
          })
        ])
      )
    })
  )

  it.effect("rejects unknown registry fields", () =>
    decodeResearchFamilyIndex(
      JSON.stringify({ ...JSON.parse(source), claim: "forbidden promotion" }),
      "altered family index"
    ).pipe(
      Effect.either,
      Effect.map((result) => expect(result._tag).toBe("Left"))
    )
  )
})
