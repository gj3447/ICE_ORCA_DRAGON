import { expect, it } from "@effect/vitest"
import { Effect } from "effect"
import { compareComputed, decodeJsonObject } from "../src/repro/compare.ts"
import { reproCases, type ComparePolicy } from "../src/repro/manifest.ts"

const tight: ComparePolicy = {
  defaultNumeric: {
    kind: "close",
    relativeTolerance: 1e-12,
    absoluteTolerance: 1e-15
  }
}

it("keeps keys, arrays, booleans, strings, and integer-valued numbers exact", () => {
  const differences = compareComputed(
    { nested: { count: 42, passed: true, label: "stable", values: [1, 2] } },
    { nested: { count: 41, passed: false, label: "drift", values: [1, 2, 3] } },
    tight
  )
  expect(differences.map((difference) => difference.path)).toEqual([
    "$.nested.count",
    "$.nested.label",
    "$.nested.passed",
    "$.nested.values"
  ])
})

it("excludes only curated and nondeterministic top-level fields", () => {
  const differences = compareComputed(
    {
      verdict: "OLD",
      timestamp: "old",
      mc_evidence_ref: "curated-old",
      computed: { verdict: "inside" }
    },
    {
      verdict: "NEW",
      timestamp: "new",
      mc_evidence_ref: "curated-new",
      computed: { verdict: "changed" }
    },
    tight
  )
  expect(differences).toHaveLength(1)
  expect(differences[0]?.path).toBe("$.computed.verdict")
})

it("accepts machine-precision float drift but rejects larger drift", () => {
  expect(compareComputed({ x: 1.5 }, { x: 1.5 + 1e-13 }, tight)).toHaveLength(0)
  expect(compareComputed({ x: 1.5 }, { x: 1.5 + 1e-8 }, tight)).toHaveLength(1)
})

it("uses the S5 residual as a near-zero semantic invariant", () => {
  const s5 = reproCases.find((entry) => entry.name === "prove_s5_bv_ainfty")
  if (s5?.policy !== "portable") {
    throw new Error("S5 policy missing")
  }
  expect(
    compareComputed(
      { "S5.4": { s5_4_master_residual: 1.3e-16 } },
      { "S5.4": { s5_4_master_residual: 2.4e-16 } },
      s5.compare
    )
  ).toHaveLength(0)
})

it("limits circular optimizer tolerance to the registered queue04 paths", () => {
  const queue04 = reproCases.find(
    (entry) => entry.name === "queue_04_hosotani_toy"
  )
  if (queue04?.policy !== "portable") {
    throw new Error("queue04 policy missing")
  }
  expect(
    compareComputed(
      { case3_realistic: { best_theta: [0.0], theta_spread: 1e-7, best_V: -30.0 } },
      {
        case3_realistic: {
          best_theta: [2 * Math.PI - 8e-8],
          theta_spread: 5e-8,
          best_V: -30.0 + 1e-8
        }
      },
      queue04.compare
    ).map((difference) => difference.path)
  ).toEqual(["$.case3_realistic.best_V"])
})

it("rejects non-finite values even when both sides match", () => {
  expect(compareComputed({ x: Number.NaN }, { x: Number.NaN }, tight)).toHaveLength(1)
})

it.effect("decodes JSON through Effect Schema and rejects non-object roots", () =>
  Effect.gen(function* () {
    const decoded = yield* decodeJsonObject('{"value":42}', "fixture")
    expect(decoded).toEqual({ value: 42 })

    const failed = yield* decodeJsonObject("[1,2,3]", "fixture").pipe(Effect.either)
    expect(failed._tag).toBe("Left")
  })
)
