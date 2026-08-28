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

it("maps the V0 principal endpoint FIO as a portable committed result", () => {
  const fio = reproCases.find(
    (entry) => entry.name === "gate1_v0_principal_endpoint_fio"
  )
  expect(fio?.policy).toBe("portable")
  expect(fio?.output).toBe(
    "cpt_temporal_folded_susy/GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT.json"
  )
})

it("maps the V0 improved-static BFV source as a portable committed result", () => {
  const source = reproCases.find(
    (entry) => entry.name === "gate1_v0_improved_static_bfv_source"
  )
  expect(source?.policy).toBe("portable")
  expect(source?.output).toBe(
    "cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT.json"
  )
})

it("maps the V0 spectral-to-S3 controls as portable committed results", () => {
  const expected = new Map([
    [
      "gate1_v0_constraint_spectral_domain",
      "cpt_temporal_folded_susy/GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json"
    ],
    [
      "gate1_v0_endpoint_subprincipal_nonuniqueness",
      "cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json"
    ],
    [
      "gate1_v0_static_spectral_pairing",
      "cpt_temporal_folded_susy/GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT.json"
    ],
    [
      "gate1_v0_bfv_m2_spectral_trajectory",
      "cpt_temporal_folded_susy/GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT.json"
    ],
    [
      "gate1_v0_densitized_liouville_raq",
      "cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT.json"
    ],
    [
      "gate1_v0_densitized_raq_p_zero_boundary",
      "cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT.json"
    ],
    [
      "gate1_v0_full_p_regular_raq_completion",
      "cpt_temporal_folded_susy/GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_RESULT.json"
    ],
    [
      "gate1_v0_raw_c_weighted_operator_domain_audit",
      "cpt_temporal_folded_susy/GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_RESULT.json"
    ],
    [
      "gate1_v0_endpoint_support_restricted_spectral_intertwiner",
      "cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUPPORT_RESTRICTED_SPECTRAL_INTERTWINER_RESULT.json"
    ],
    [
      "gate1_v0_bfv_zero_mode_elimination_ward",
      "cpt_temporal_folded_susy/GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT.json"
    ],
    [
      "gate1_v0_bfv_finite_pfaffian_orientation_transport",
      "cpt_temporal_folded_susy/GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT.json"
    ],
    [
      "gate1_v0_closed_s3_scalar_harmonic_projection_ledger",
      "cpt_temporal_folded_susy/GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_RESULT.json"
    ]
  ])

  for (const [name, output] of expected) {
    const entry = reproCases.find((candidate) => candidate.name === name)
    expect(entry?.policy).toBe("portable")
    expect(entry?.output).toBe(output)
  }
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
