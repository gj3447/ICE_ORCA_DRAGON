import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { Effect } from "effect"
import { createHash } from "node:crypto"
import type { ScriptEntry } from "./catalog.ts"
import { iceError, type IceError } from "./errors.ts"
import { capture } from "./process.ts"
import { Workspace } from "./workspace.ts"

const coreResearchRoot = "cpt_temporal_folded_susy/"
const phaseToken =
  /(?:^|[/_\s-])phase[\s_-]?([0-9]+)[a-z]?(?=$|[/_\s-])/gi

export const frozenHistoricalCoreScriptSha256: ReadonlyMap<string, string> =
  new Map([
    ["cpt_temporal_folded_susy/phase11_collar_admissibility", "2b2184ec43f8e2e07bd1b07e1699112b6531a547c02be392c92db53e2a271529"],
    ["cpt_temporal_folded_susy/phase12_boundary_twist_interface", "78657ca4f906054615806578d9ee93ce52561a046ac593addf148d3ca3ab43f5"],
    ["cpt_temporal_folded_susy/phase13a_lorentzian_branch_supercharge", "3fc9c66cd5010833e98544194b1b5410479c9e6daae0fc714255a468a5eedf05"],
    ["cpt_temporal_folded_susy/phase14a_chiral_clock_charge_first", "1c92f295329d511e661f5d8b9d83b6f767e3c8aee45be86e98f6cc95c133bb2b"],
    ["cpt_temporal_folded_susy/phase15r_parent_sign_reproduction", "af3e3d021e995833a634b1fb7afda7d1cd4faace60113bb425d467301424f40d"],
    ["cpt_temporal_folded_susy/phase16_bgg_single_source", "95c9346bf4607d955692778a2bf91638a307a3563f51bff57af0635bc548f55c"],
    ["cpt_temporal_folded_susy/phase17_time_line_fold_algebra", "4723f6217f1014c52001dd989fb393e7c8547a1a0556bf7c0141c0dcaa20d615"],
    ["cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum", "01f2d5d04341093494e185529dd67630aef5896e842a4bedddc6d1309271e221"],
    ["cpt_temporal_folded_susy/phase19_closed_sugra_bounce", "5dbfccd768bb13961222c289ba0754497bec94319f8b33ff602889eaeb469341"],
    ["cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection", "a55ebfca78f07246679fd5fa8791537a0efe1d3370dfa53d8d6410ffc6a95807"],
    ["cpt_temporal_folded_susy/phase21_connected_seam_gaussian", "6ac7b2b36da9aa2eeda4c83494427c5d9f006bb9031d6b55d6678bf2ffc5b005"],
    ["cpt_temporal_folded_susy/phase22_finite_mode_seam_density", "0a4da3c60bbd2231892938cb8a74f45bd3e491d9884df4adcc86051053d58dbe"],
    ["cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density", "62408abeeec2eb11f104d984c84ffde5c2d6f287e7f07a4021ee6fb3ec202ffd"],
    ["cpt_temporal_folded_susy/phase24_connected_starobinsky_interval", "a625c9390305a0e07ea3b38977dc34b4cce725f8dd19cec1c66b90d8ccf63256"],
    ["cpt_temporal_folded_susy/phase25_connected_lapse_scan", "5fe43ec6997d6bae9c10d78ddb5d13b1806e10934140fd5080fef0dca3492ee8"],
    ["cpt_temporal_folded_susy/phase26_global_lapse_flow", "c41824d6667d38efe66f5ebf4d0e1ec572d27c78b146b7c044e2e1ffd9868d04"],
    ["cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint", "36a454ca3f98277cca2c24904a708ec67fa8f7c3556f376e6613cdc0823e0d04"],
    ["cpt_temporal_folded_susy/phase28_thimble_bfv_intersection", "496990308456bcc1d28f9649b99053d2a05499c6d3c2c0d233d5576a39a3f018"],
    ["cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel", "0fa8314d3c0385c70ad569ce1c2ad65d506580eef50ef589e7fa2da5f7fb3e76"],
    ["cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line", "4c402a50aa5f32966faa7e01d65623933ea7d9cff2b43f25b76f89b5efa36cc7"],
    ["cpt_temporal_folded_susy/phase31_homogeneous_bfv_superhessian", "f2f37ff240c1bea82a5345a549882415e5f9fde1fc7bcf3bb96abc80a2e05adb"],
    ["cpt_temporal_folded_susy/phase32_below_origin_lapse_intersection", "35e68db704f65c704a34ac4b2e9d676ad39c1bb390221b5b41d79da3e34bb6d3"],
    ["cpt_temporal_folded_susy/phase33_fold_airy_uniformization", "844c1262332c06b17def3506a0112f3230b12cbda153750d4964ca9f96a4485b"],
    ["cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation", "c35d9fd605e46d791ae74b58344565578a84a7803745481859b41b26699e9527"],
    ["cpt_temporal_folded_susy/phase35_reduced_detline_transport", "2e91813fca948735abd8226a63af4cb26cba459ac0a9897b852686d8cb33d6cb"],
    ["cpt_temporal_folded_susy/phase36_airy_gauss_manin_connection", "a82da3be27bdb903756ed8b9d511e5f3eb99e7b15eac27f13c4adad695c04bf9"],
    ["cpt_temporal_folded_susy/phase37_closed_fold_holonomy", "72dd9264a15f3910c51fe01ca608cc435f5afcf0c47797d2889df467f8b46f62"],
    ["cpt_temporal_folded_susy/phase38_joint_cycle_identifiability", "4df1c5e59404019d8fb6e278ca70b1cfee87a40d77d7288ce2720360376915a8"],
    ["cpt_temporal_folded_susy/phase39_finite_joint_intersection", "0af21171e44a688a9dd0b19b2491954467c5ceb881a97852d0eb6135ea8fce54"],
    ["cpt_temporal_folded_susy/phase40_m3_reflection_odd_intersection", "d7e71ed8a7561a586e7035366a92a3033dcb029bb9aa88ea595b38d4d7dacbc3"],
    ["cpt_temporal_folded_susy/phase41_m4_two_source_intersection", "377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530"],
    ["cpt_temporal_folded_susy/phase42_m4_fixed_root_checkpoint", "5b2492347405bef0fed26fbfe2a68648899219c8583c20b8de0b2be02419de6d"],
    ["cpt_temporal_folded_susy/phase42_m4_fixed_root_tangent_disentanglement", "1414664c3b7d3da99364d11c0b639ff99c8ecc71c141f99bfaa6c4e367893019"],
    ["cpt_temporal_folded_susy/phase43_m4_high_precision_local_rhs_arbitration", "01e0727d2269f6b2d555455157b1c49cda96fb4966fb00eab5b3635d690f3729"],
    ["cpt_temporal_folded_susy/phase44_m4_numpy64_local_rhs_error_decomposition", "220123fe069cad3e3178d7e87656cf61240d153d0762041169288c3d9cb9dc52"],
    ["cpt_temporal_folded_susy/phase45_m4_integrated_tangent_rhs_stability", "e562314282ccf58be0c39aebc2b5a07c0c8bb818ae739f24ace6cad6a8f915b2"],
    ["cpt_temporal_folded_susy/phase46_m4_u2_state_map_fd_audit", "a71badb3c49a4af44e5e4a1b8bec244593f1de5a43c3b0d71d729f92ef147d55"],
    ["cpt_temporal_folded_susy/phase47_m4_source_gradient_flow_error_budget", "945744a9f9c022f371d2516c01aa806317020d947fcaa47a0cc7f962dc82d091"],
    ["cpt_temporal_folded_susy/phase48_m4_clongdouble_gradient_repair_state_map", "63bc9f3eaf7f9d994d52898a39ae494988dfd573216385397d65fd2cae9b3986"],
    ["cpt_temporal_folded_susy/phase49_m4_clongdouble_full_flow_state_map_repair", "f7f03d8ca08c3406cfbae4825b64fb5c2cac89797ea005519fc12c489947abb2"],
    ["cpt_temporal_folded_susy/phase50_m4_m5_joint_saddle_homotopy", "77290311ad58198ace94f36e919a59fe19a330c5f49bb8c1ed8b6d15af697d90"]
  ])

export const frozenHistoricalCoreScripts: ReadonlySet<string> = new Set(
  frozenHistoricalCoreScriptSha256.keys()
)

export const terminalCloseoutRunnerSha256 =
  "083924f7f9fd0bb3baf8e681e2760cc54ef4a105f5a597b52aa3cdb58c6ac882"

export const boundedGate1Script =
  "cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility"
export const boundedGate1ScriptSha256 =
  "c2cfac73e303d0f46d86c1577fc31cc1cd2ff5e0dfd809e9bdd6b75a38aaaa7e"
export const boundedGate1InputSha256 =
  "a3bc97461c7989cd5bb471accf46f0c2196de41c3030e9eef2248c4f09a47fdb"
export const boundedGate1ExecutionEnabled: boolean = true

export const boundedGate1InvocationDecision = (
  query: string,
  relpath: string,
  args: ReadonlyArray<string>
) => {
  const normalizedQuery = canonicalResearchRelpath(query)
  const basename = relpath.split("/").at(-1) ?? relpath
  if (normalizedQuery !== relpath && normalizedQuery !== basename) {
    return { allowed: false, reason: "EXACT_NAME_REQUIRED" as const }
  }
  if (args.length > 0) {
    return { allowed: false, reason: "ARGUMENTS_FORBIDDEN" as const }
  }
  return { allowed: true, reason: "AUTHORIZED" as const }
}

export const ragnarokStatus = {
  schema: "ice-ragnarok-circuit-breaker/v2",
  effective_date: "2026-08-23",
  operational_state: "GATE1_BOUNDED_RESUME",
  pause_started_on: "2026-08-23",
  review_eligible_on: "2026-08-30",
  auto_resume: false,
  resume_authorization: {
    id: "GATE1_DIRECT_20260825_01",
    authorized_by: "USER",
    approved_on: "2026-08-25",
    effective_immediately: true,
    overrides_only: "SCHEDULED_REVIEW_WAIT_FOR_THIS_EXACT_CALCULATION",
    scope: "DIRECT_GATE1_END_ADMISSIBILITY_MODEL_CLASS_REDUCTION",
    does_not_reopen_killed_route: true
  },
  gate1_window: {
    state: "CALC_AUTHORIZED",
    automatic_next: null,
    maximum_launches: 1,
    exact_script: boundedGate1Script,
    runner_sha256: boundedGate1ScriptSha256,
    input: {
      path: "cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_INPUTS.json",
      sha256: boundedGate1InputSha256
    },
    result_path:
      "cpt_temporal_folded_susy/GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_RESULT.json",
    resource_caps: {
      wall_clock_seconds: 30,
      artifact_bytes: 250_000,
      stdout_bytes: 65_536,
      stderr_bytes: 65_536,
      root_calls: 0,
      ode_calls: 0,
      evaluator_reconciliation_calls: 0,
      automatic_descendants: 0
    },
    execution_enabled: boundedGate1ExecutionEnabled
  },
  verdicts: {
    ragnarok_pattern: "PRESENT",
    scientific_progress: "PARTIAL",
    core_gate: "NOT_CLOSED"
  },
  scientific_state: {
    gate1: "OPEN_PARTIAL_PROGRESS",
    global_promotion: "PROHIBITED",
    scientific_route: "OPEN",
    global_n_sigma: null,
    physical_original_cycle: null,
    physics_claim: null
  },
  containment: {
    continuation_route: "KILL",
    kill_scope:
      "PHASE_51_TO_56_SAVED_BACKEND_AND_RECONSTRUCTED_LAUNCH_RECONCILIATION",
    terminal_closeout_phase: 56,
    terminal_closeout_completed: true,
    terminal_closeout_completed_at_utc: "2026-08-23T19:32:42Z",
    terminal_closeout_reproduced_at_utc: "2026-08-23T19:36:16Z",
    maximum_allowed_core_phase: 50,
    blocked_from_core_phase: 51,
    next_phase: null,
    frozen_historical_run_allowlist_through_phase: 50,
    frozen_historical_run_allowlist: [...frozenHistoricalCoreScripts],
    frozen_historical_runner_sha256: Object.fromEntries(
      frozenHistoricalCoreScriptSha256
    ),
    terminal_closeout_script:
      "cpt_temporal_folded_susy/phase56_lambda_half_launch_provenance_residual_conditioning",
    terminal_closeout_runner_sha256: terminalCloseoutRunnerSha256,
    terminal_closeout_result: {
      path: "cpt_temporal_folded_susy/PHASE56_LAMBDA_HALF_LAUNCH_PROVENANCE_RESIDUAL_CONDITIONING_RESULT.json",
      sha256: "c9163319405ed4ec696076f7516c32fa8af290794a2e1cc4762090812f693d27",
      payload_sha256_without_self:
        "56c567bf60fde04b7d68ab9a5c394faaf08e73e43fe1db36b082ba58e3c010b2",
      run_status: "VALID_RUN",
      classification:
        "P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET",
      authoritative_and_reproduction_byte_identical: true,
      next_phase: null
    },
    execution_provenance:
      "PINNED_RUNNER_AND_INPUT_HASH_CLEAN_CORE_BOUNDED_GATE1_WINDOW",
    direct_python_bypass_authorized: false
  },
  repository_transport: {
    push_status: "PUSHED_WITH_GIT_LFS",
    transport_mode: "GIT_LFS_EXACT_PATH",
    ordinary_git_hosting_limit: "100 MB",
    migrated_object: {
      path: "cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json",
      pre_migration_blob_oid:
        "b7d32b0547967d39ee69decb4e186fc8b9244c8a",
      pointer_blob_oid: "d8372d861b7e7de6419c9d32d178ba716320dc1e",
      content_and_lfs_oid_sha256:
        "bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75",
      blob_bytes: 529_370_671,
      pre_migration_introduced_by:
        "4e75a4fe9ce909fa62794f5a550a3409f6e0fc9f",
      migrated_introduced_by:
        "18a17b643874e74f7486fe9e009066eba8a467cb",
      gitattributes_rule:
        "cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json filter=lfs diff=lfs merge=lfs -text"
    },
    migration: {
      user_authorized_on: "2026-08-24",
      completed: true,
      force_push_required: false,
      preserved_pre_boundary_commits: 40,
      rewritten_commits: 76,
      phase44_parent:
        "d13af382fe65cc50f74fbc83861e41c0e7236341",
      pre_migration_head:
        "42c3e92b0519c99783777a4da41346192005dbb2",
      migrated_head_before_attestation:
        "f36e84c6be3471d8202c9ccf4925f3830bd5d310",
      object_map_path:
        "docs/decisions/ICE_PHASE44_GIT_LFS_OBJECT_MAP_2026-08-24.csv",
      object_map_sha256:
        "1882806fe40f0e4858d5e985f52a12b765e9d90781ce170ba5c21c9d43c58a31",
      local_backup_ref: "backup/pre-lfs-main-20260824",
      local_bundle_path:
        ".git/migration-backups/pre-lfs-main-42c3e92-20260824.bundle",
      local_bundle_sha256:
        "6c8c7e4aefb71ccf74b7a3da1b15758ca16bc558817c9570f4c7fe9902c7a990",
      local_bundle_bytes: 136_996_036
    },
    remote_push: {
      authorized_on: "2026-08-24",
      verified: true,
      verified_at_utc: "2026-08-24T06:08:08Z",
      verified_remote_head:
        "b524abd08201699a674e723538835ee92545c966",
      lfs_readback_verified: true,
      lfs_readback_sha256:
        "bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75",
      lfs_readback_bytes: 529_370_671
    },
    history_remediation_requires_explicit_user_authorization: false
  },
  reopen_requirements: [
    "explicit user approval; any waiver of the scheduled review wait must be exact-scope and must not reopen the killed route",
    "a direct Gate-1 typed object rather than another reconciliation descendant",
    "pre-run serialization and hash pinning of the original joint cycle, orientation, singular divisor, endpoint prescription, regulator, Stokes chamber, and relative-end inputs",
    "a complete pre-run census of saddles, upward cycles, complex sheets, and asymptotic ends",
    "a new counterexample, invariant, observable discriminator, or model-class reduction",
    "a predeclared KEEP/NARROW/BRANCH/EQUIVALENCE/KILL/OPEN table plus one-phase runtime and artifact caps",
    "verified availability of the migrated Phase-44 LFS object and its provenance map"
  ],
  killed_route_recovery_policy:
    "hash-authenticated recovery of missing authoritative Phase-53 bytes may authorize a separately approved archival reproduction audit, never a new numbered continuation or automatic route reopening"
} as const

export const canonicalResearchRelpath = (
  relpath: string
): string | undefined => {
  const portable = relpath.replaceAll("\\", "/")
  if (
    portable.length === 0 ||
    portable.includes("\0") ||
    portable.startsWith("/") ||
    /^[a-z]:\//i.test(portable)
  ) {
    return undefined
  }

  const segments: Array<string> = []
  for (const segment of portable.split("/")) {
    if (segment.length === 0 || segment === ".") {
      continue
    }
    if (segment === "..") {
      if (segments.length === 0) {
        return undefined
      }
      segments.pop()
      continue
    }
    segments.push(segment)
  }
  const normalized = segments.join("/").replace(/\.py$/, "")
  return normalized.length === 0 ? undefined : normalized
}

const phaseNumbersFromText = (value: string): ReadonlyArray<number> => {
  const phases: Array<number> = []
  for (const match of value.matchAll(phaseToken)) {
    const digits = match[1]
    if (digits !== undefined) {
      phases.push(Number(digits))
    }
  }
  return phases
}

export const corePhaseNumbersFromRelpath = (
  relpath: string
): ReadonlyArray<number> => {
  const normalized = canonicalResearchRelpath(relpath)
  if (normalized === undefined || !normalized.startsWith(coreResearchRoot)) {
    return []
  }
  return phaseNumbersFromText(normalized)
}

export const maximumCorePhaseFromRelpath = (
  relpath: string
): number | undefined => {
  const phases = corePhaseNumbersFromRelpath(relpath)
  return phases.length === 0 ? undefined : Math.max(...phases)
}

export const researchRunDecision = (relpath: string) => {
  const normalized = canonicalResearchRelpath(relpath)
  if (normalized === undefined) {
    return {
      allowed: false,
      reason: "INVALID_RELATIVE_PATH" as const,
      normalized_relpath: relpath,
      maximum_phase: null,
      expected_sha256: null
    }
  }
  const maximumPhase = maximumCorePhaseFromRelpath(normalized) ?? null
  if (!normalized.startsWith(coreResearchRoot)) {
    return {
      allowed: true,
      reason: "NON_CORE" as const,
      normalized_relpath: normalized,
      maximum_phase: maximumPhase,
      expected_sha256: null
    }
  }
  if (normalized === ragnarokStatus.containment.terminal_closeout_script) {
    return {
      allowed: false,
      reason: "TERMINAL_CLOSEOUT_CONSUMED" as const,
      normalized_relpath: normalized,
      maximum_phase: maximumPhase,
      expected_sha256: null
    }
  }
  if (frozenHistoricalCoreScripts.has(normalized)) {
    return {
      allowed: true,
      reason: "FROZEN_HISTORICAL" as const,
      normalized_relpath: normalized,
      maximum_phase: maximumPhase,
      expected_sha256: frozenHistoricalCoreScriptSha256.get(normalized) ?? null
    }
  }
  if (normalized === boundedGate1Script && boundedGate1ExecutionEnabled) {
    return {
      allowed: true,
      reason: "BOUNDED_GATE1_DIRECT" as const,
      normalized_relpath: normalized,
      maximum_phase: maximumPhase,
      expected_sha256: boundedGate1ScriptSha256
    }
  }
  return {
    allowed: false,
    reason: "CORE_ROUTE_PAUSED" as const,
    normalized_relpath: normalized,
    maximum_phase: maximumPhase,
    expected_sha256: null
  }
}

const blockedRunError = (
  relpath: string,
  phase: number | null
): IceError => {
  const prefix =
    phase !== null && phase >= ragnarokStatus.containment.blocked_from_core_phase
      ? `core research phase ${phase}`
      : phase === ragnarokStatus.containment.terminal_closeout_phase
        ? `completed terminal Phase ${phase} script '${relpath}'`
        : `core research script '${relpath}'`
  return iceError(
    "RESEARCH_PHASE_PAUSED",
    `${prefix} is blocked by ${ragnarokStatus.operational_state}; the Phase ${ragnarokStatus.containment.terminal_closeout_phase} closeout has been consumed, the killed route remains closed, and execution is limited to the frozen historical allowlist plus any exact hash-pinned Gate-1 window shown by \`ice status\``,
    2
  )
}

export const guardResearchRelpath = (
  relpath: string
): Effect.Effect<void, IceError> => {
  const decision = researchRunDecision(relpath)
  return decision.allowed
    ? Effect.succeed(undefined)
    : Effect.fail(
        blockedRunError(decision.normalized_relpath, decision.maximum_phase)
      )
}

const sha256 = (bytes: Uint8Array): string =>
  createHash("sha256").update(bytes).digest("hex")

const guardCoreDirectoryClean: Effect.Effect<
  void,
  IceError,
  | Workspace
  | import("@effect/platform/CommandExecutor").CommandExecutor
> = Effect.gen(function* () {
  const workspace = yield* Workspace
  const status = yield* capture({
    command: "git",
    args: [
      "status",
      "--porcelain=v1",
      "--untracked-files=all",
      "--",
      coreResearchRoot
    ],
    cwd: workspace.root
  })
  if (status.exitCode !== 0) {
    return yield* Effect.fail(
      iceError(
        "RESEARCH_PROVENANCE_FAILED",
        `cannot verify the core worktree: ${status.stderr.trim() || `git exited ${status.exitCode}`}`
      )
    )
  }
  if (status.stdout.trim().length > 0) {
    return yield* Effect.fail(
      iceError(
        "RESEARCH_CORE_DIRTY",
        `core execution requires a clean ${coreResearchRoot} tree; commit or resolve these paths first:\n${status.stdout.trim()}`,
        2
      )
    )
  }
})

const guardPinnedCoreFile = (
  relpath: string,
  file: string,
  expectedSha256: string
): Effect.Effect<
  void,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  Effect.gen(function* () {
    yield* guardCoreDirectoryClean
    const fs = yield* FileSystem.FileSystem
    const bytes = yield* fs.readFile(file).pipe(
      Effect.mapError((error) =>
        iceError(
          "RESEARCH_PROVENANCE_FAILED",
          `cannot hash ${relpath}: ${String(error)}`
        )
      )
    )
    const observed = sha256(bytes)
    if (observed !== expectedSha256) {
      return yield* Effect.fail(
        iceError(
          "RESEARCH_RUNNER_HASH_MISMATCH",
          `${relpath} is not the frozen executable bytes (expected ${expectedSha256}, observed ${observed})`,
          2
        )
      )
    }
  })

export const guardResearchRelpaths = (
  relpaths: ReadonlyArray<string>
): Effect.Effect<
  void,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | Path.Path
  | import("@effect/platform/CommandExecutor").CommandExecutor
> =>
  Effect.gen(function* () {
    const workspace = yield* Workspace
    const path = yield* Path.Path
    for (const relpath of relpaths) {
      const decision = researchRunDecision(relpath)
      if (!decision.allowed) {
        return yield* Effect.fail(
          blockedRunError(decision.normalized_relpath, decision.maximum_phase)
        )
      }
      if (decision.expected_sha256 !== null) {
        yield* guardPinnedCoreFile(
          decision.normalized_relpath,
          path.join(workspace.root, `${decision.normalized_relpath}.py`),
          decision.expected_sha256
        )
      }
    }
  })

export const guardResearchQuery = (
  query: string
): Effect.Effect<void, IceError> => {
  const normalized = canonicalResearchRelpath(query)
  if (normalized === undefined) {
    return Effect.fail(
      iceError(
        "RESEARCH_PATH_INVALID",
        `script query must be a workspace-relative path: '${query}'`,
        2
      )
    )
  }
  const basename = normalized.split("/").at(-1) ?? normalized
  const looksLikeCoreQuery =
    normalized.startsWith(coreResearchRoot) ||
    (!normalized.includes("/") && /^phase(?:[\s_-]?[0-9])/i.test(basename))
  const phases = looksLikeCoreQuery ? phaseNumbersFromText(normalized) : []
  const maximumPhase = phases.length === 0 ? null : Math.max(...phases)
  return maximumPhase !== null &&
    maximumPhase >= ragnarokStatus.containment.blocked_from_core_phase
    ? Effect.fail(blockedRunError(normalized, maximumPhase))
    : Effect.succeed(undefined)
}

export const guardResearchRun = (
  entry: ScriptEntry
): Effect.Effect<
  ScriptEntry,
  IceError,
  | Workspace
  | FileSystem.FileSystem
  | import("@effect/platform/CommandExecutor").CommandExecutor
> => {
  const decision = researchRunDecision(entry.relpath)
  if (!decision.allowed) {
    return Effect.fail(
      blockedRunError(decision.normalized_relpath, decision.maximum_phase)
    )
  }
  return decision.expected_sha256 === null
    ? Effect.succeed(entry)
    : guardPinnedCoreFile(
        decision.normalized_relpath,
        entry.file,
        decision.expected_sha256
      ).pipe(Effect.as(entry))
}

export const formatRagnarokStatus = (json: boolean): string => {
  if (json) {
    return JSON.stringify(ragnarokStatus, null, 2)
  }

  return [
    `Ragnarok circuit breaker: ${ragnarokStatus.operational_state}`,
    `Continuation route: ${ragnarokStatus.containment.continuation_route}`,
    `Kill scope: ${ragnarokStatus.containment.kill_scope}`,
    `Executable core: ${ragnarokStatus.containment.frozen_historical_run_allowlist.length} frozen historical scripts through Phase ${ragnarokStatus.containment.frozen_historical_run_allowlist_through_phase}; Phase ${ragnarokStatus.containment.terminal_closeout_phase} closeout consumed`,
    `Execution provenance: ${ragnarokStatus.containment.execution_provenance}`,
    `Bounded Gate 1: ${ragnarokStatus.gate1_window.state}; ${ragnarokStatus.gate1_window.exact_script}; execution enabled=${String(ragnarokStatus.gate1_window.execution_enabled)}`,
    `Next phase: ${String(ragnarokStatus.containment.next_phase)}; no automatic descendant is authorized`,
    `Gate 1: ${ragnarokStatus.scientific_state.gate1}`,
    `Scientific route: ${ragnarokStatus.scientific_state.scientific_route}`,
    `Historical review date: ${ragnarokStatus.review_eligible_on}; exact-window wait override approved ${ragnarokStatus.resume_authorization.approved_on} (no automatic resume)`,
    `Repository push: ${ragnarokStatus.repository_transport.push_status}`,
    "Decision: docs/decisions/ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md"
  ].join("\n")
}
