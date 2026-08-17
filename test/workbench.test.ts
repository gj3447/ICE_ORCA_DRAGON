import { expect, it, layer } from "@effect/vitest"
import * as FileSystem from "@effect/platform/FileSystem"
import { NodeContext } from "@effect/platform-node"
import * as Path from "@effect/platform/Path"
import { Effect, Layer } from "effect"
import { discoverScripts } from "../src/catalog.ts"
import { reproCases } from "../src/repro/manifest.ts"
import { Workspace, WorkspaceLive } from "../src/workspace.ts"

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("workbench live layer", (it) => {
  it.effect("discovers numerical kernels without treating tests as runnable", () =>
    Effect.gen(function* () {
      const entries = yield* discoverScripts
      expect(entries.length).toBeGreaterThanOrEqual(40)
      expect(entries.some((entry) => entry.name === "queue_03_threshold_sensitivity_scan")).toBe(true)
      expect(entries.every((entry) => !entry.relpath.startsWith("test/"))).toBe(true)
      expect(entries.every((entry) => !entry.relpath.startsWith("tests/"))).toBe(true)
    })
  )
})

it("quarantines queue03 and keeps queue06 explicitly superseded", () => {
  expect(
    reproCases.find((entry) => entry.name === "queue_03_threshold_sensitivity_scan")
      ?.policy
  ).toBe("nonportable")
  expect(
    reproCases.find((entry) => entry.name === "queue_06_cooperative_vacuum")
      ?.policy
  ).toBe("superseded")
})

layer(AppLayer)("reproduction manifest", (it) => {
  it.effect("maps every case to an adjacent tracked script and output", () =>
    Effect.gen(function* () {
      const workspace = yield* Workspace
      const fs = yield* FileSystem.FileSystem
      const path = yield* Path.Path

      for (const entry of reproCases) {
        expect(path.dirname(entry.script)).toBe(path.dirname(entry.output))
        expect(yield* fs.exists(path.join(workspace.root, entry.script))).toBe(true)
        expect(yield* fs.exists(path.join(workspace.root, entry.output))).toBe(true)
      }
    })
  )
})
