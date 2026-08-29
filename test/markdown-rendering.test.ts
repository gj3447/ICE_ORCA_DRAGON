import { readFileSync } from "node:fs"
import { expect, it } from "@effect/vitest"

const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8")

it("keeps public README math inside the portable macro contract", () => {
  for (const macro of ["operatorname", "rm"] as const) {
    expect(readme, `README uses downstream-forbidden \\${macro}`).not.toContain(
      `\\${macro}`
    )
  }
})
