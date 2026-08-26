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
  acquireBoundedGate1SourceLinkLaunch,
  acquireBoundedGate1ZeroLapseLaunch,
  boundedGate1InputSha256,
  boundedGate1InvocationDecision,
  boundedGate1Script,
  boundedGate1ScriptSha256,
  boundedGate1SourceLinkAuthorizationId,
  boundedGate1SourceLinkInputPath,
  boundedGate1SourceLinkInputSha256,
  boundedGate1SourceLinkResultPath,
  boundedGate1SourceLinkScript,
  boundedGate1SourceLinkScriptSha256,
  boundedGate1ZeroLapseAuthorizationId,
  boundedGate1ZeroLapseInputPath,
  boundedGate1ZeroLapseInputSha256,
  boundedGate1ZeroLapseResultPath,
  boundedGate1ZeroLapseScript,
  boundedGate1ZeroLapseScriptSha256,
  boundedGate1ZeroLapseUpstreamResultPath,
  boundedGate1ZeroLapseUpstreamResultSha256,
  canonicalResearchRelpath,
  corePhaseNumbersFromRelpath,
  decodeBoundedGate1SourceLinkResult,
  decodeBoundedGate1ZeroLapseResult,
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

it("uses token boundaries and opens only unnumbered core paths", () => {
  expect(
    corePhaseNumbersFromRelpath(
      "cpt_temporal_folded_susy/metaphase57_control"
    )
  ).toEqual([])
  expect(researchRunDecision("research/metaphase57_control").allowed).toBe(true)
  expect(
    researchRunDecision("cpt_temporal_folded_susy/metaphase57_control")
      .allowed
  ).toBe(true)
  expect(
    researchRunDecision("cpt_temporal_folded_susy/next_repair").allowed
  ).toBe(true)
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
  expect(direct.reason).toBe("CONSUMED_CORE_RUN")
  expect(direct.expected_sha256).toBe(null)
  expect(ragnarokStatus.gate1_window.runner_sha256).toBe(
    boundedGate1ScriptSha256
  )

  for (const blocked of [
    `${boundedGate1Script}_retry`,
    "cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility_replay"
  ]) {
    expect(researchRunDecision(blocked).allowed).toBe(false)
  }
  expect(
    researchRunDecision("cpt_temporal_folded_susy/gate1_next_calculation")
      .reason
  ).toBe("BOUNDED_NEW_CORE")
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

it("records both exact Gate-1 windows as consumed and blocks descendants", () => {
  const sourceLink = researchRunDecision(boundedGate1SourceLinkScript)
  expect(sourceLink.allowed).toBe(false)
  expect(sourceLink.reason).toBe("CONSUMED_CORE_RUN")
  expect(sourceLink.expected_sha256).toBe(null)
  expect(researchRunDecision(boundedGate1Script).allowed).toBe(false)

  const basename = boundedGate1SourceLinkScript.split("/").at(-1)!
  expect(
    boundedGate1InvocationDecision(
      boundedGate1SourceLinkScript,
      boundedGate1SourceLinkScript,
      []
    )
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision(
      basename,
      boundedGate1SourceLinkScript,
      []
    )
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision(
      "gate1_scalar",
      boundedGate1SourceLinkScript,
      []
    )
  ).toEqual({ allowed: false, reason: "EXACT_NAME_REQUIRED" })
  expect(
    boundedGate1InvocationDecision(
      basename,
      boundedGate1SourceLinkScript,
      ["--retry"]
    )
  ).toEqual({ allowed: false, reason: "ARGUMENTS_FORBIDDEN" })

  for (const blocked of [
    `${boundedGate1SourceLinkScript}_retry`,
    `${boundedGate1SourceLinkScript}_replay`,
    "cpt_temporal_folded_susy/gate1_source_link_descendant"
  ]) {
    expect(researchRunDecision(blocked).allowed).toBe(false)
  }
})

it("keeps the consumed zero-lapse one-shot and all descendants closed", () => {
  const decision = researchRunDecision(boundedGate1ZeroLapseScript)
  expect(decision.allowed).toBe(false)
  expect(decision.reason).toBe("CONSUMED_CORE_RUN")
  expect(decision.maximum_phase).toBe(null)
  expect(decision.expected_sha256).toBe(null)
  expect(researchRunDecision(boundedGate1Script).allowed).toBe(false)
  expect(researchRunDecision(boundedGate1SourceLinkScript).allowed).toBe(
    false
  )

  const basename = boundedGate1ZeroLapseScript.split("/").at(-1)!
  expect(
    boundedGate1InvocationDecision(
      boundedGate1ZeroLapseScript,
      boundedGate1ZeroLapseScript,
      []
    )
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision(
      basename,
      boundedGate1ZeroLapseScript,
      []
    )
  ).toEqual({ allowed: true, reason: "AUTHORIZED" })
  expect(
    boundedGate1InvocationDecision(
      "gate1_scalar_zero_lapse",
      boundedGate1ZeroLapseScript,
      []
    )
  ).toEqual({ allowed: false, reason: "EXACT_NAME_REQUIRED" })
  for (const nonExact of [
    `./${boundedGate1ZeroLapseScript}`,
    `research/../${boundedGate1ZeroLapseScript}`,
    `${boundedGate1ZeroLapseScript}.py`,
    boundedGate1ZeroLapseScript.replaceAll("/", "\\")
  ]) {
    expect(
      boundedGate1InvocationDecision(
        nonExact,
        boundedGate1ZeroLapseScript,
        []
      )
    ).toEqual({ allowed: false, reason: "EXACT_NAME_REQUIRED" })
  }
  expect(
    boundedGate1InvocationDecision(
      basename,
      boundedGate1ZeroLapseScript,
      ["--retry"]
    )
  ).toEqual({ allowed: false, reason: "ARGUMENTS_FORBIDDEN" })

  for (const blocked of [
    `${boundedGate1ZeroLapseScript}_retry`,
    `${boundedGate1ZeroLapseScript}_replay`,
    "cpt_temporal_folded_susy/gate1_zero_lapse_descendant"
  ]) {
    expect(researchRunDecision(blocked).allowed).toBe(false)
  }
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

it("binds the source-link runner and input to separate pre-spawn hashes", async () => {
  const runner = await readFile(
    join(process.cwd(), `${boundedGate1SourceLinkScript}.py`)
  )
  const input = await readFile(
    join(process.cwd(), boundedGate1SourceLinkInputPath)
  )
  expect(createHash("sha256").update(runner).digest("hex")).toBe(
    boundedGate1SourceLinkScriptSha256
  )
  expect(createHash("sha256").update(input).digest("hex")).toBe(
    boundedGate1SourceLinkInputSha256
  )
})

it("binds the zero-lapse runner and input to separate pre-spawn hashes", async () => {
  const runner = await readFile(
    join(process.cwd(), `${boundedGate1ZeroLapseScript}.py`)
  )
  const input = await readFile(
    join(process.cwd(), boundedGate1ZeroLapseInputPath)
  )
  const upstream = await readFile(
    join(process.cwd(), boundedGate1ZeroLapseUpstreamResultPath)
  )
  expect(createHash("sha256").update(runner).digest("hex")).toBe(
    boundedGate1ZeroLapseScriptSha256
  )
  expect(createHash("sha256").update(input).digest("hex")).toBe(
    boundedGate1ZeroLapseInputSha256
  )
  expect(createHash("sha256").update(upstream).digest("hex")).toBe(
    boundedGate1ZeroLapseUpstreamResultSha256
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

it("decodes only source-link results with the pinned identity, hashes, and null promotions", async () => {
  const valid = {
    schema_version: "ice.gate1.scalar-source-link.result.v1",
    authorization_id: boundedGate1SourceLinkAuthorizationId,
    calculation_id: "Gate1M2ScalarPhaseSpaceSourceLink",
    numbered_phase: null,
    run_status: "VALID_RUN",
    classification:
      "GATE1_NONZERO_LAPSE_SCALAR_SOURCE_LINK_MATCHES_ZERO_LAPSE_DISTRIBUTION_OPEN",
    verdict: "NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN",
    programme_impact: "NARROW",
    input: {
      path: boundedGate1SourceLinkInputPath,
      sha256: boundedGate1SourceLinkInputSha256
    },
    runner: {
      path: `${boundedGate1SourceLinkScript}.py`,
      sha256: boundedGate1SourceLinkScriptSha256
    },
    gate1_decision: "OPEN_PARTIAL_PROGRESS",
    global_promotion: "PROHIBITED",
    automatic_next: null,
    promoted_outputs: {
      TOE_claim: null,
      complete_global_signed_intersection_vector: null,
      full_joint_orientation: null,
      global_n_sigma: null,
      physical_original_cycle: null,
      physics_claim: null
    }
  } as const

  await expect(
    Effect.runPromise(
      decodeBoundedGate1SourceLinkResult(JSON.stringify(valid))
    )
  ).resolves.toMatchObject({
    verdict: "NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN",
    automatic_next: null
  })

  for (const invalid of [
    {
      ...valid,
      input: { ...valid.input, sha256: "0".repeat(64) }
    },
    {
      ...valid,
      promoted_outputs: {
        ...valid.promoted_outputs,
        physics_claim: "forbidden"
      }
    }
  ]) {
    const error = await Effect.runPromise(
      decodeBoundedGate1SourceLinkResult(JSON.stringify(invalid)).pipe(
        Effect.flip
      )
    )
    expect(error.code).toBe("RESEARCH_RESULT_SCHEMA_INVALID")
  }
})

it("preserves the frozen successful-result schema without treating INVALID_RUN as evidence", async () => {
  const valid = {
    schema_version:
      "ice.gate1.scalar-zero-lapse-extension.result.v1",
    authorization_id: boundedGate1ZeroLapseAuthorizationId,
    calculation_id: "Gate1M2ScalarZeroLapseExtension",
    numbered_phase: null,
    run_status: "VALID_RUN",
    classification:
      "GATE1_DECLARED_SCALAR_ZERO_LAPSE_CANONICAL_BOUNDARY_EXISTS",
    verdict: "UNIQUE_SCALING_DEGREE_PRESERVING_EXTENSION",
    programme_impact: "NARROW",
    input: {
      path: boundedGate1ZeroLapseInputPath,
      sha256: boundedGate1ZeroLapseInputSha256
    },
    runner: {
      path: `${boundedGate1ZeroLapseScript}.py`,
      sha256: boundedGate1ZeroLapseScriptSha256
    },
    upstream_result: {
      path: boundedGate1ZeroLapseUpstreamResultPath,
      sha256: boundedGate1ZeroLapseUpstreamResultSha256
    },
    numerical_checks: [],
    gate1_decision: "OPEN_PARTIAL_PROGRESS",
    global_promotion: "PROHIBITED",
    automatic_next: null,
    promoted_outputs: {
      TOE_claim: null,
      complete_global_signed_intersection_vector: null,
      full_joint_orientation: null,
      global_n_sigma: null,
      physical_original_cycle: null,
      physics_claim: null
    },
    resource_accounting: {
      root_calls: 0,
      ode_calls: 0,
      evaluator_reconciliation_calls: 0,
      numerical_samples: 0,
      automatic_descendants: 0,
      adjacent_result_files: 1,
      artifact_cap_bytes: 250_000
    }
  } as const

  await expect(
    Effect.runPromise(
      decodeBoundedGate1ZeroLapseResult(JSON.stringify(valid))
    )
  ).resolves.toMatchObject({
    verdict: "UNIQUE_SCALING_DEGREE_PRESERVING_EXTENSION",
    automatic_next: null
  })

  for (const invalid of [
    {
      ...valid,
      run_status: "INVALID_RUN"
    },
    {
      ...valid,
      verdict: "INCONCLUSIVE"
    },
    {
      ...valid,
      input: { ...valid.input, sha256: "0".repeat(64) }
    },
    {
      ...valid,
      resource_accounting: {
        ...valid.resource_accounting,
        numerical_samples: 1
      }
    },
    {
      ...valid,
      numerical_checks: [{ passed: true }]
    }
  ]) {
    const error = await Effect.runPromise(
      decodeBoundedGate1ZeroLapseResult(JSON.stringify(invalid)).pipe(
        Effect.flip
      )
    )
    expect(error.code).toBe("RESEARCH_RESULT_SCHEMA_INVALID")
  }

  for (const field of [
    "TOE_claim",
    "complete_global_signed_intersection_vector",
    "full_joint_orientation",
    "global_n_sigma",
    "physical_original_cycle",
    "physics_claim"
  ] as const) {
    const error = await Effect.runPromise(
      decodeBoundedGate1ZeroLapseResult(
        JSON.stringify({
          ...valid,
          promoted_outputs: {
            ...valid.promoted_outputs,
            [field]: "forbidden"
          }
        })
      ).pipe(Effect.flip)
    )
    expect(error.code).toBe("RESEARCH_RESULT_SCHEMA_INVALID")
  }
})

it("binds the consumed source-link receipt to the one-shot result", async () => {
  const resultBytes = await readFile(
    join(process.cwd(), boundedGate1SourceLinkResultPath)
  )
  const result = JSON.parse(resultBytes.toString("utf8")) as {
    readonly run_status: string
    readonly verdict: string
    readonly result_payload_sha256_without_self: string
    readonly exact_checks: ReadonlyArray<{ readonly passed: boolean }>
    readonly theorem_guards: ReadonlyArray<{ readonly verified: boolean }>
    readonly numerical_checks: ReadonlyArray<unknown>
    readonly gate1_decision: string
    readonly global_promotion: string
    readonly automatic_next: null
    readonly promoted_outputs: {
      readonly TOE_claim: null
      readonly complete_global_signed_intersection_vector: null
      readonly full_joint_orientation: null
      readonly global_n_sigma: null
      readonly physical_original_cycle: null
      readonly physics_claim: null
    }
  }
  const receipt = ragnarokStatus.source_link_window.consumed

  expect(createHash("sha256").update(resultBytes).digest("hex")).toBe(
    receipt.result_sha256
  )
  expect(resultBytes.byteLength).toBe(receipt.result_bytes)
  expect(result.result_payload_sha256_without_self).toBe(
    receipt.payload_sha256_without_self
  )
  expect(result.run_status).toBe("VALID_RUN")
  expect(result.verdict).toBe("NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN")
  expect(result.exact_checks).toHaveLength(receipt.exact_checks_passed)
  expect(result.exact_checks.every(({ passed }) => passed)).toBe(true)
  expect(result.theorem_guards).toHaveLength(
    receipt.theorem_guards_verified
  )
  expect(result.theorem_guards.every(({ verified }) => verified)).toBe(true)
  expect(result.numerical_checks).toHaveLength(0)
  expect(result.gate1_decision).toBe("OPEN_PARTIAL_PROGRESS")
  expect(result.global_promotion).toBe("PROHIBITED")
  expect(result.automatic_next).toBeNull()
  expect(result.promoted_outputs).toEqual({
    TOE_claim: null,
    complete_global_signed_intersection_vector: null,
    full_joint_orientation: null,
    global_n_sigma: null,
    physical_original_cycle: null,
    physics_claim: null
  })
})

it("acquires the source-link launch receipt atomically and rejects a second launch", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-source-link-launch-"))
  try {
    const initialized = spawnSync("git", ["init", "-q"], {
      cwd: root,
      encoding: "utf8"
    })
    expect(initialized.status).toBe(0)
    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    await expect(
      Effect.runPromise(
        acquireBoundedGate1SourceLinkLaunch.pipe(Effect.provide(TestLayer))
      )
    ).resolves.toBe(undefined)
    const second = await Effect.runPromise(
      acquireBoundedGate1SourceLinkLaunch.pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(second.code).toBe("RESEARCH_WINDOW_CONSUMED")
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("rejects a pre-existing source-link result before acquiring a launch receipt", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-source-link-stale-"))
  try {
    const researchDirectory = join(root, "cpt_temporal_folded_susy")
    await mkdir(researchDirectory)
    await writeFile(join(root, boundedGate1SourceLinkResultPath), "{}\n")
    const initialized = spawnSync("git", ["init", "-q"], {
      cwd: root,
      encoding: "utf8"
    })
    expect(initialized.status).toBe(0)
    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    const error = await Effect.runPromise(
      acquireBoundedGate1SourceLinkLaunch.pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(error.code).toBe("RESEARCH_RESULT_PREEXISTS")
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("acquires the zero-lapse launch receipt atomically and rejects a second launch", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-zero-lapse-launch-"))
  try {
    const initialized = spawnSync("git", ["init", "-q"], {
      cwd: root,
      encoding: "utf8"
    })
    expect(initialized.status).toBe(0)
    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    await expect(
      Effect.runPromise(
        acquireBoundedGate1ZeroLapseLaunch.pipe(Effect.provide(TestLayer))
      )
    ).resolves.toBe(undefined)
    const second = await Effect.runPromise(
      acquireBoundedGate1ZeroLapseLaunch.pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(second.code).toBe("RESEARCH_WINDOW_CONSUMED")
  } finally {
    await rm(root, { recursive: true, force: true })
  }
})

it("rejects a pre-existing zero-lapse result before acquiring a launch receipt", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-zero-lapse-stale-"))
  try {
    const researchDirectory = join(root, "cpt_temporal_folded_susy")
    await mkdir(researchDirectory)
    await writeFile(join(root, boundedGate1ZeroLapseResultPath), "{}\n")
    const initialized = spawnSync("git", ["init", "-q"], {
      cwd: root,
      encoding: "utf8"
    })
    expect(initialized.status).toBe(0)
    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, workspaceFromRoot(root))
    )
    const error = await Effect.runPromise(
      acquireBoundedGate1ZeroLapseLaunch.pipe(
        Effect.flip,
        Effect.provide(TestLayer)
      )
    )
    expect(error.code).toBe("RESEARCH_RESULT_PREEXISTS")
  } finally {
    await rm(root, { recursive: true, force: true })
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

it("runs a clean tracked unnumbered core script through the generic bounded shell", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-bounded-core-"))
  const runGit = (args: ReadonlyArray<string>): void => {
    const result = spawnSync("git", args, { cwd: root, encoding: "utf8" })
    if (result.status !== 0) {
      throw new Error(result.stderr || result.stdout)
    }
  }
  try {
    const researchDirectory = join(root, "cpt_temporal_folded_susy")
    await mkdir(researchDirectory)
    await writeFile(
      join(researchDirectory, "gate1_new_bounded_control.py"),
      [
        "from pathlib import Path",
        "if __name__ == '__main__':",
        "    Path('GATE1_NEW_BOUNDED_RESULT.json').write_text('\\n{}\\n'.strip() + '\\n')",
        "    print('bounded-ok')",
        ""
      ].join("\n")
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

    const base = workspaceFromRoot(root)
    const TestLayer = Layer.mergeAll(
      NodeContext.layer,
      Layer.succeed(Workspace, {
        ...base,
        python: join(process.cwd(), ".venv/bin/python")
      })
    )
    await expect(
      Effect.runPromise(
        runScript("gate1_new_bounded_control", []).pipe(
          Effect.provide(TestLayer)
        )
      )
    ).resolves.toBe(undefined)
    expect(
      await readFile(
        join(researchDirectory, "GATE1_NEW_BOUNDED_RESULT.json"),
        "utf8"
      )
    ).toBe("{}\n")
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
  expect(error.message).toContain(
    "consumed bounded Gate-1 windows remain closed"
  )
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

it("blocks the consumed zero-lapse runner before Python execution", async () => {
  const error = await Effect.runPromise(
    runScript("gate1_scalar_zero_lapse_extension", []).pipe(
      Effect.flip,
      Effect.provide(RepositoryLayer)
    )
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  expect(error.message).toContain(
    "consumed bounded Gate-1 windows remain closed"
  )
})

it("blocks the consumed source-link runner before Python execution", async () => {
  const error = await Effect.runPromise(
    runScript("gate1_scalar_source_link", []).pipe(
      Effect.flip,
      Effect.provide(RepositoryLayer)
    )
  )
  expect(error.code).toBe("RESEARCH_PHASE_PAUSED")
  expect(error.message).toContain(
    "consumed bounded Gate-1 windows remain closed"
  )
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

  const sourceLinkError = await Effect.runPromise(
    guardResearchRelpaths([`${boundedGate1SourceLinkScript}.py`]).pipe(
      Effect.flip,
      Effect.provide(RepositoryLayer)
    )
  )
  expect(sourceLinkError.code).toBe("RESEARCH_PHASE_PAUSED")

  const zeroLapseError = await Effect.runPromise(
    guardResearchRelpaths([`${boundedGate1ZeroLapseScript}.py`]).pipe(
      Effect.flip,
      Effect.provide(RepositoryLayer)
    )
  )
  expect(zeroLapseError.code).toBe("RESEARCH_PHASE_PAUSED")

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
  expect(ragnarokStatus.schema).toBe("ice-ragnarok-circuit-breaker/v3")
  expect(ragnarokStatus.operational_state).toBe(
    "BOUNDED_SCIENCE_OPEN_KILLED_RECONCILIATION_CLOSED"
  )
  expect(ragnarokStatus.bounded_science_runtime).toMatchObject({
    state: "ACTIVE",
    policy: "GENERIC_BOUNDED_UNNUMBERED_CORE",
    per_window_receipts_required: false,
    numbered_descendants_allowed: false
  })
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
  expect(ragnarokStatus.source_link_authorization.id).toBe(
    boundedGate1SourceLinkAuthorizationId
  )
  expect(ragnarokStatus.source_link_authorization.numbered_phase).toBe(null)
  expect(ragnarokStatus.source_link_authorization.phase57_authorized).toBe(
    false
  )
  expect(ragnarokStatus.source_link_window.state).toBe(
    "CONSUMED"
  )
  expect(ragnarokStatus.source_link_window.exact_script).toBe(
    boundedGate1SourceLinkScript
  )
  expect(ragnarokStatus.source_link_window.runner_sha256).toBe(
    boundedGate1SourceLinkScriptSha256
  )
  expect(ragnarokStatus.source_link_window.input).toEqual({
    path: boundedGate1SourceLinkInputPath,
    sha256: boundedGate1SourceLinkInputSha256
  })
  expect(ragnarokStatus.source_link_window.execution_enabled).toBe(false)
  expect(ragnarokStatus.source_link_window.maximum_launches).toBe(1)
  expect(ragnarokStatus.source_link_window.allowed_args).toEqual([])
  expect(ragnarokStatus.source_link_window.automatic_next).toBe(null)
  expect(ragnarokStatus.source_link_window.consumed.run_status).toBe(
    "VALID_RUN"
  )
  expect(ragnarokStatus.source_link_window.consumed.verdict).toBe(
    "NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN"
  )
  expect(
    ragnarokStatus.source_link_window.consumed
      .reduced_affine_class_nonzero_arm_source_link
  ).toBe("KEEP")
  expect(ragnarokStatus.source_link_window.consumed.zero_lapse_distribution).toBe(
    "OPEN"
  )
  expect(ragnarokStatus.source_link_window.consumed.exact_checks_passed).toBe(16)
  expect(ragnarokStatus.source_link_window.consumed.theorem_guards_verified).toBe(3)
  expect(ragnarokStatus.source_link_window.consumed.global_n_sigma).toBe(null)
  expect(ragnarokStatus.zero_lapse_authorization.id).toBe(
    boundedGate1ZeroLapseAuthorizationId
  )
  expect(ragnarokStatus.zero_lapse_authorization.numbered_phase).toBe(null)
  expect(ragnarokStatus.zero_lapse_authorization.phase57_authorized).toBe(
    false
  )
  expect(ragnarokStatus.zero_lapse_authorization.full_replay_authorized).toBe(
    false
  )
  expect(ragnarokStatus.zero_lapse_window.state).toBe("CONSUMED")
  expect(ragnarokStatus.zero_lapse_window.exact_script).toBe(
    boundedGate1ZeroLapseScript
  )
  expect(ragnarokStatus.zero_lapse_window.runner_sha256).toBe(
    boundedGate1ZeroLapseScriptSha256
  )
  expect(ragnarokStatus.zero_lapse_window.input).toEqual({
    path: boundedGate1ZeroLapseInputPath,
    sha256: boundedGate1ZeroLapseInputSha256
  })
  expect(ragnarokStatus.zero_lapse_window.upstream_result).toEqual({
    path: boundedGate1ZeroLapseUpstreamResultPath,
    sha256: boundedGate1ZeroLapseUpstreamResultSha256
  })
  expect(ragnarokStatus.zero_lapse_window.execution_enabled).toBe(false)
  expect(ragnarokStatus.zero_lapse_window.maximum_launches).toBe(1)
  expect(ragnarokStatus.zero_lapse_window.allowed_args).toEqual([])
  expect(ragnarokStatus.zero_lapse_window.allowed_outcomes).toEqual([
    "UNIQUE_SCALING_DEGREE_PRESERVING_EXTENSION",
    "INVALID_RUN"
  ])
  expect(ragnarokStatus.zero_lapse_window.resource_caps).toEqual({
    wall_clock_seconds: 30,
    artifact_bytes: 250_000,
    stdout_bytes: 65_536,
    stderr_bytes: 65_536,
    root_calls: 0,
    ode_calls: 0,
    evaluator_reconciliation_calls: 0,
    numerical_samples: 0,
    automatic_descendants: 0
  })
  expect(ragnarokStatus.zero_lapse_window.automatic_next).toBe(null)
  expect(ragnarokStatus.zero_lapse_window.consumed).toMatchObject({
    consumed_on: "2026-08-26",
    observed_at_utc: "2026-08-26T05:42:12Z",
    receipt_created_at_utc: "2026-08-26T05:42:14.025056895Z",
    receipt_contents: [],
    authorization_commit: "1f0fc7d17cc704577db601071e46563a37db24f0",
    launch_receipt:
      ".git/ice-launches/GATE1_ZERO_LAPSE_20260826_01",
    authorized_launches_observed: 1,
    run_status: "INVALID_RUN",
    exit_code: 1,
    wall_time_seconds: 2.349,
    wall_clock_source: "BASH_TIMEFORMAT",
    failed_check_id: "G1.zero.global_lower_offset",
    exact_checks_passed_before_failure: 1,
    theorem_guards_reached: 0,
    numerical_checks: 0,
    failure_observation:
      "EXCLUSIVE_LAUNCH_RECEIPT_PRESENT_RESULT_ARTIFACT_ABSENT",
    failure_interpretation:
      "HARNESS_STRUCTURAL_EQUALITY_FALSE_NEGATIVE_NOT_SCIENTIFIC_COUNTEREVIDENCE",
    result_artifact: "ABSENT",
    result_present: false,
    result_path: boundedGate1ZeroLapseResultPath,
    result_sha256: null,
    payload_sha256_without_self: null,
    result_bytes: null,
    result_schema_validation: "NOT_PERFORMED_RESULT_ABSENT",
    scientific_output_usable: false,
    verdict: null,
    decision_table_row: null,
    programme_impact: null,
    inherited_zero_lapse_distribution: "OPEN",
    gate1: "OPEN_PARTIAL_PROGRESS",
    global_promotion: "PROHIBITED",
    physical_original_cycle: null,
    full_joint_orientation: null,
    global_n_sigma: null,
    physics_claim: null,
    TOE_claim: null,
    retry_authorized: false,
    repro_authorized: false,
    automatic_next: null
  })
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
  expect(ragnarokStatus.scientific_state.TOE_claim).toBe(null)
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
    "Research runtime: BOUNDED_SCIENCE_OPEN_KILLED_RECONCILIATION_CLOSED"
  )
  expect(formatRagnarokStatus(false)).toContain(
    "New unnumbered core: bounded execution enabled; per-window receipts=false"
  )
  expect(formatRagnarokStatus(false)).toContain(
    "Scalar source link: CONSUMED"
  )
  expect(formatRagnarokStatus(false)).toContain(
    "Scalar zero-lapse extension: CONSUMED"
  )
  expect(formatRagnarokStatus(false)).toContain(
    "Scalar zero-lapse closeout: INVALID_RUN; result artifact=ABSENT; retry/repro blocked"
  )
  expect(JSON.parse(formatRagnarokStatus(true))).toEqual(ragnarokStatus)
})
