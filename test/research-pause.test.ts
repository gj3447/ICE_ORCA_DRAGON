import { expect, it } from "@effect/vitest"
import { NodeContext } from "@effect/platform-node"
import { Effect, Layer } from "effect"
import { createHash } from "node:crypto"
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { spawnSync } from "node:child_process"
import { discoverScripts } from "../src/catalog.ts"
import { runScript } from "../src/commands.ts"
import {
  canonicalResearchRelpath,
  corePhaseNumbersFromRelpath,
  formatRagnarokStatus,
  frozenHistoricalCoreScriptSha256,
  frozenHistoricalCoreScripts,
  guardResearchQuery,
  guardResearchRelpath,
  guardResearchRelpaths,
  maximumCorePhaseFromRelpath,
  researchRunDecision,
  ragnarokStatus
} from "../src/research-pause.ts"
import { Workspace, workspaceFromRoot } from "../src/workspace.ts"

const RepositoryLayer = Layer.mergeAll(
  NodeContext.layer,
  Layer.succeed(Workspace, workspaceFromRoot(process.cwd()))
)

it("extracts core phase tokens including letter suffixes", () => {
  expect(
    maximumCorePhaseFromRelpath(
      "cpt_temporal_folded_susy/phase13a_lorentzian_branch_supercharge"
    )
  ).toBe(13)
  expect(
    maximumCorePhaseFromRelpath(
      "cpt_temporal_folded_susy/phase15R_single_source"
    )
  ).toBe(15)
  expect(maximumCorePhaseFromRelpath("research/avenue3_phase99_control")).toBe(
    undefined
  )
})

it("uses the greatest phase token so compound names cannot bypass the pause", () => {
  const relpath =
    "cpt_temporal_folded_susy/phase55_to_phase57_reconciliation"
  expect(corePhaseNumbersFromRelpath(relpath)).toEqual([55, 57])
  expect(maximumCorePhaseFromRelpath(relpath)).toBe(57)
})

it("uses token boundaries and fail-closes unclassified core paths", () => {
  expect(
    corePhaseNumbersFromRelpath(
      "cpt_temporal_folded_susy/metaphase57_control"
    )
  ).toEqual([])
  expect(researchRunDecision("research/metaphase57_control").allowed).toBe(true)
  expect(
    researchRunDecision("cpt_temporal_folded_susy/metaphase57_control")
      .allowed
  ).toBe(false)
  expect(
    researchRunDecision("cpt_temporal_folded_susy/next_repair").allowed
  ).toBe(false)
  expect(
    researchRunDecision("cpt_temporal_folded_susy/p57_repair").allowed
  ).toBe(false)
})

it("canonicalizes traversal and rejects root escape before routing", () => {
  expect(
    canonicalResearchRelpath(
      "././cpt_temporal_folded_susy/phase57_repro_bypass.py"
    )
  ).toBe("cpt_temporal_folded_susy/phase57_repro_bypass")
  expect(
    canonicalResearchRelpath(
      "research/../cpt_temporal_folded_susy/phase57_repro_bypass.py"
    )
  ).toBe("cpt_temporal_folded_susy/phase57_repro_bypass")
  expect(researchRunDecision("/tmp/phase11_escape.py").allowed).toBe(false)
  expect(researchRunDecision("../../phase11_escape.py").allowed).toBe(false)
  expect(
    researchRunDecision(
      "research/../cpt_temporal_folded_susy/phase57_repro_bypass.py"
    ).allowed
  ).toBe(false)
})

it("classifies ordinary kernels and keeps the consumed Phase 56 closeout blocked", () => {
  expect(researchRunDecision("research/hypercomplex/demo").reason).toBe(
    "NON_CORE"
  )
  const closeout = researchRunDecision(
    "cpt_temporal_folded_susy/phase56_lambda_half_launch_provenance_residual_conditioning"
  )
  expect(closeout.allowed).toBe(false)
  expect(closeout.reason).toBe("TERMINAL_CLOSEOUT_CONSUMED")
})

it("allows only frozen history through Phase 50 and blocks killed-route reruns", async () => {
  const phase50 =
    "cpt_temporal_folded_susy/phase50_m4_m5_joint_saddle_homotopy"
  expect(frozenHistoricalCoreScripts.has(phase50)).toBe(true)
  expect(researchRunDecision(phase50).reason).toBe("FROZEN_HISTORICAL")

  for (const blocked of [
    "cpt_temporal_folded_susy/phase50_new_descendant",
    "cpt_temporal_folded_susy/phase51_m5_gamma_k_local_continuation",
    "cpt_temporal_folded_susy/phase55_p53_root_fixed_launch_schedule_transfer",
    "cpt_temporal_folded_susy/phase56b_full_replay"
  ]) {
    const error = await Effect.runPromise(
      guardResearchRelpath(blocked).pipe(Effect.flip)
    )
    expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  }
})

it("freezes the complete current core catalog through Phase 50", async () => {
  const entries = await Effect.runPromise(
    discoverScripts.pipe(Effect.provide(RepositoryLayer))
  )
  const expected = entries
    .filter(
      (candidate) =>
        candidate.relpath.startsWith("cpt_temporal_folded_susy/") &&
        (maximumCorePhaseFromRelpath(candidate.relpath) ?? Number.POSITIVE_INFINITY) <=
          50
    )
    .map((candidate) => candidate.relpath)
    .sort()
  expect([...frozenHistoricalCoreScripts].sort()).toEqual(expected)
})

it("binds every frozen historical runner to its current SHA-256", async () => {
  for (const [relpath, expected] of frozenHistoricalCoreScriptSha256) {
    const bytes = await readFile(join(process.cwd(), `${relpath}.py`))
    const observed = createHash("sha256").update(bytes).digest("hex")
    expect(observed, relpath).toBe(expected)
  }
})

it("fails Phase 57 and later with the typed operational error", async () => {
  const error = await Effect.runPromise(
    guardResearchRelpath(
      "cpt_temporal_folded_susy/phase57_recursive_repair"
    ).pipe(Effect.flip)
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  expect(error.exitCode).toBe(2)
  expect(error.message).toContain("phase 57")

  const later = await Effect.runPromise(
    guardResearchRelpath(
      "cpt_temporal_folded_susy/phase560_recursive_repair"
    ).pipe(Effect.flip)
  )
  expect(later.code).toBe("RESEARCH_PHASE_PAUSED")
})

it("blocks an unclassified resolved core script before Python execution", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-ragnarok-test-"))
  try {
    const researchDirectory = join(root, "cpt_temporal_folded_susy")
    await mkdir(researchDirectory)
    await writeFile(
      join(researchDirectory, "p57_must_not_execute.py"),
      "if __name__ == \"__main__\":\n    raise RuntimeError(\"executed\")\n"
    )

    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    const error = await Effect.runPromise(
      runScript("p57_must_not_execute", []).pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
    expect(error.message).toContain("p57_must_not_execute")
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("blocks the consumed terminal runner before Python execution", async () => {
  const error = await Effect.runPromise(
    runScript(
      "phase56_lambda_half_launch_provenance_residual_conditioning",
      []
    ).pipe(Effect.flip, Effect.provide(RepositoryLayer))
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  expect(error.message).toContain("closeout has been consumed")
})

it("rejects clean but non-frozen historical bytes and any dirty core tree", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-ragnarok-provenance-"))
  const runGit = (args: ReadonlyArray<string>): void => {
    const result = spawnSync("git", args, { cwd: root, encoding: "utf8" })
    if (result.status !== 0) {
      throw new Error(result.stderr || result.stdout)
    }
  }
  try {
    const researchDirectory = join(root, "cpt_temporal_folded_susy")
    await mkdir(researchDirectory)
    const runner = join(
      researchDirectory,
      "phase50_m4_m5_joint_saddle_homotopy.py"
    )
    await writeFile(
      runner,
      "if __name__ == \"__main__\":\n    raise RuntimeError(\"executed\")\n"
    )
    runGit(["init", "-q"])
    runGit(["add", "."])
    runGit([
      "-c",
      "user.name=ICE Test",
      "-c",
      "user.email=ice-test@example.invalid",
      "commit",
      "-qm",
      "fixture"
    ])

    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    const mismatch = await Effect.runPromise(
      runScript("phase50_m4_m5_joint_saddle_homotopy", []).pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(mismatch.code).toBe("RESEARCH_RUNNER_HASH_MISMATCH")

    await writeFile(runner, `${await readFile(runner, "utf8")}# dirty\n`)
    const dirty = await Effect.runPromise(
      runScript("phase50_m4_m5_joint_saddle_homotopy", []).pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(dirty.code).toBe("RESEARCH_CORE_DIRTY")
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("blocks a raw missing Phase 57 query before catalog resolution", async () => {
  const error = await Effect.runPromise(
    guardResearchQuery("phase57_missing").pipe(Effect.flip)
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  await expect(
    Effect.runPromise(guardResearchQuery("metaphase57_control"))
  ).resolves.toBe(undefined)
})

it("applies the same fail-closed guard to reproduction script paths", async () => {
  await expect(
    Effect.runPromise(
      guardResearchRelpaths([
        "research/hypercomplex/queue_01_orbit_analysis.py"
      ]).pipe(Effect.provide(RepositoryLayer))
    )
  ).resolves.toBe(undefined)
  const error = await Effect.runPromise(
    guardResearchRelpaths([
      "cpt_temporal_folded_susy/phase57_repro_bypass.py"
    ]).pipe(Effect.flip, Effect.provide(RepositoryLayer))
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")

  for (const traversal of [
    "././cpt_temporal_folded_susy/phase57_repro_bypass.py",
    "research/../cpt_temporal_folded_susy/phase57_repro_bypass.py"
  ]) {
    const traversalError = await Effect.runPromise(
      guardResearchRelpaths([traversal]).pipe(
        Effect.flip,
        Effect.provide(RepositoryLayer)
      )
    )
    expect(traversalError.code).toBe("RESEARCH_PHASE_PAUSED")
  }
})

it("returns exit 2 and the typed pause error from the real CLI", () => {
  const result = spawnSync(join(process.cwd(), "ice"), [
    "run",
    "phase57_missing"
  ], {
    cwd: process.cwd(),
    encoding: "utf8"
  })
  expect(result.status).toBe(2)
  expect(result.stderr).toContain("RESEARCH_PHASE_PAUSED")
  expect(result.stderr).not.toContain("SCRIPT_NOT_FOUND")
})

it("keeps operational containment distinct from the scientific verdict", () => {
  expect(ragnarokStatus.operational_state).toBe("BOUNDED_PAUSE")
  expect(ragnarokStatus.containment.continuation_route).toBe("KILL")
  expect(ragnarokStatus.containment.maximum_allowed_core_phase).toBe(50)
  expect(ragnarokStatus.containment.terminal_closeout_completed).toBe(true)
  expect(ragnarokStatus.containment.terminal_closeout_result.next_phase).toBe(
    null
  )
  expect(ragnarokStatus.containment.next_phase).toBe(null)
  expect(ragnarokStatus.containment.frozen_historical_run_allowlist).toEqual([
    ...frozenHistoricalCoreScripts
  ])
  expect(ragnarokStatus.scientific_state.gate1).toBe(
    "OPEN_PARTIAL_PROGRESS"
  )
  expect(ragnarokStatus.scientific_state.scientific_route).toBe("OPEN")
  expect(ragnarokStatus.scientific_state.global_n_sigma).toBe(null)
  expect(ragnarokStatus.scientific_state.physical_original_cycle).toBe(null)
  expect(ragnarokStatus.scientific_state.physics_claim).toBe(null)
  expect(ragnarokStatus.auto_resume).toBe(false)
  expect(ragnarokStatus.repository_transport.push_status).toBe(
    "BLOCKED_OVERSIZED_GIT_OBJECT"
  )
})

it("renders stable human and machine-readable status", () => {
  expect(formatRagnarokStatus(false)).toContain(
    "Ragnarok circuit breaker: BOUNDED_PAUSE"
  )
  expect(JSON.parse(formatRagnarokStatus(true))).toEqual(ragnarokStatus)
})
