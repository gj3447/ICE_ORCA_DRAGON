import { Effect } from "effect"
import { createHash } from "node:crypto"
import { iceError } from "../errors.ts"
import { findCollectionNodes } from "../ontology/collection-core.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { readLocalReference } from "../research-context/commands.ts"
import { Workspace } from "../workspace.ts"
import { compileResearchState, parseResearchState } from "./state.ts"

export const loadResearchStateFile = (path: string, without: readonly string[] = []) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const snapshot = yield* Effect.tryPromise({
    try: async () => {
      const bytes = await readLocalReference(root, path)
      const state = parseResearchState(JSON.parse(bytes.toString("utf8")))
      for (const source of state.sources) {
        const actual = createHash("sha256").update(await readLocalReference(root, source.path)).digest("hex")
        if (actual !== source.sha256) throw new Error(`Research state source changed: ${source.path}`)
      }
      return { state, sha256: createHash("sha256").update(bytes).digest("hex"), path }
    }, catch: (error) => iceError("RESEARCH_STATE_INVALID", String(error), 2)
  })
  const collection = yield* loadValidOntologyCollectionStructure
  const graph = snapshot.state.target.split("::")[0]
  for (const anchor of new Set([snapshot.state.target, ...snapshot.state.objects.flatMap((object) => object.anchors)])) {
    if (anchor.split("::")[0] !== graph || findCollectionNodes(collection.graphs, anchor).length !== 1) {
      return yield* Effect.fail(iceError("RESEARCH_STATE_ANCHOR_INVALID", `Expected an existing same-graph anchor: ${anchor}`, 2))
    }
  }
  const view = yield* Effect.try({ try: () => compileResearchState(snapshot.state, without),
    catch: (error) => iceError("RESEARCH_STATE_VIEW_INVALID", String(error), 2) })
  return { ...snapshot, view }
})
