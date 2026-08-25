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
  boundedGate1InputSha256,
  boundedGate1InvocationDecision,
  boundedGate1Script,
  boundedGate1ScriptSha256,
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

it("records the consumed hash-pinned Gate-1 calculation and blocks relaunch", async () => {
  const direct = researchRunDecision(boundedGate1Script)
  expect(direct.allowed).toBe(false)
  expect(direct.reason).toBe("CORE_ROUTE_PAUSED")
  expect(direct.expected_sha256).toBe(null)
  expect(ragnarokStatus.gate1_window.runner_sha256).toBe(
    boundedGate1ScriptSha256
  )

  for (const blocked of [
    `${boundedGate1Script}_retry`,
    "cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility_replay",
    "cpt_temporal_folded_susy/gate1_next_calculation"
  ]) {
    expect(researchRunDecision(blocked).allowed).toBe(false)
  }
})

it("requires the exact bounded Gate-1 name and forbids arguments", () => {
  const basename = boundedGate1Script.split("/").at(-1)
  expect(basename).toBeDefined()
  expect(
    boundedGate1InvocationDecision(
      boundedGate1Script,
      boundedGate1Script,
      []
    )
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision(basename!, boundedGate1Script, [])
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision("gate1_straight", boundedGate1Script, [])
  ).toEqual({ allowed: false, reason: "EXACT_NAME_REQUIRED" })
  expect(
    boundedGate1InvocationDecision(basename!, boundedGate1Script, ["--fast"])
  ).toEqual({ allowed: false, reason: "ARGUMENTS_FORBIDDEN" })
})

it("binds the bounded Gate-1 runner and frozen input to their declared hashes", async () => {
  const runner = await readFile(
    join(process.cwd(), `${boundedGate1Script}.py`)
  )
  const input = await readFile(
    join(
      process.cwd(),
      "cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_INPUTS.json"
    )
  )
  expect(createHash("sha256").update(runner).digest("hex")).toBe(
    boundedGate1ScriptSha256
  )
  expect(createHash("sha256").update(input).digest("hex")).toBe(
    boundedGate1InputSha256
  )
})

it("binds the consumed Gate-1 receipt to the result and its null promotions", async () => {
  const resultBytes = await readFile(
    join(
      process.cwd(),
      "cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_RESULT.json"
    )
  )
  const receipt = ragnarokStatus.gate1_window.consumed
  const result = JSON.parse(resultBytes.toString("utf8")) as {
    readonly run_status: string
    readonly gate1_decision: string
    readonly global_promotion: string
    readonly automatic_next: null
    readonly result_payload_sha256_without_self: string
    readonly exact_checks: ReadonlyArray<{ readonly passed: boolean }>
    readonly numerical_checks: ReadonlyArray<{ readonly passed: boolean }>
    readonly promoted_outputs: {
      readonly TOE_claim: null
      readonly complete_global_signed_intersection_vector: null
      readonly global_n_sigma: null
      readonly physical_original_cycle: null
      readonly physics_claim: null
    }
  }

  expect(createHash("sha256").update(resultBytes).digest("hex")).toBe(
    receipt.result_sha256
  )
  expect(resultBytes.byteLength).toBe(receipt.result_bytes)
  expect(result.result_payload_sha256_without_self).toBe(
    receipt.payload_sha256_without_self
  )
  expect(result.run_status).toBe("VALID_RUN")
  expect(result.gate1_decision).toBe("OPEN_PARTIAL_PROGRESS")
  expect(result.global_promotion).toBe("PROHIBITED")
  expect(result.automatic_next).toBeNull()
  expect(result.exact_checks).toHaveLength(receipt.exact_checks_passed)
  expect(result.exact_checks.every(({ passed }) => passed)).toBe(true)
  expect(result.numerical_checks).toHaveLength(
    receipt.numerical_checks_passed
  )
  expect(result.numerical_checks.every(({ passed }) => passed)).toBe(true)
  expect(
    receipt.independent_review.executable_exact_identities_and_limits
  ).toBe(12)
  expect(
    receipt.independent_review.declarative_guards_reviewed_separately
  ).toBe(2)
  expect(receipt.independent_review.conclusion_changed).toBe(false)
  expect(receipt.independent_review.authoritative_decision_field).toBe(
    "top-level model_class_decision"
  )
  expect(result.promoted_outputs).toEqual({
    TOE_claim: null,
    complete_global_signed_intersection_vector: null,
    global_n_sigma: null,
    physical_original_cycle: null,
    physics_claim: null
  })
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
  expect(ragnarokStatus.schema).toBe("ice-ragnarok-circuit-breaker/v2")
  expect(ragnarokStatus.operational_state).toBe("GATE1_RESULT_REVIEW")
  expect(ragnarokStatus.resume_authorization.approved_on).toBe("2026-08-25")
  expect(ragnarokStatus.resume_authorization.overrides_only).toBe(
    "SCHEDULED_REVIEW_WAIT_FOR_THIS_EXACT_CALCULATION"
  )
  expect(ragnarokStatus.gate1_window.state).toBe("CONSUMED")
  expect(ragnarokStatus.gate1_window.exact_script).toBe(boundedGate1Script)
  expect(ragnarokStatus.gate1_window.execution_enabled).toBe(false)
  expect(ragnarokStatus.gate1_window.automatic_next).toBe(null)
  expect(ragnarokStatus.gate1_window.consumed.run_status).toBe("VALID_RUN")
  expect(ragnarokStatus.gate1_window.consumed.candidate_decision).toBe("KILL")
  expect(ragnarokStatus.gate1_window.consumed.gate1).toBe(
    "OPEN_PARTIAL_PROGRESS"
  )
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
    "PUSHED_WITH_GIT_LFS"
  )
  expect(ragnarokStatus.repository_transport.transport_mode).toBe(
    "GIT_LFS_EXACT_PATH"
  )
  expect(
    ragnarokStatus.repository_transport.migrated_object
      .content_and_lfs_oid_sha256
  ).toBe("bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75")
  expect(ragnarokStatus.repository_transport.migration.rewritten_commits).toBe(
    76
  )
  expect(ragnarokStatus.repository_transport.migration.force_push_required).toBe(
    false
  )
  expect(ragnarokStatus.repository_transport.remote_push.verified).toBe(true)
  expect(
    ragnarokStatus.repository_transport.remote_push.lfs_readback_verified
  ).toBe(true)
})

it("renders stable human and machine-readable status", () => {
  expect(formatRagnarokStatus(false)).toContain(
    "Ragnarok circuit breaker: GATE1_RESULT_REVIEW"
  )
  expect(JSON.parse(formatRagnarokStatus(true))).toEqual(ragnarokStatus)
})
