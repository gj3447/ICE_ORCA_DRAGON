import { mkdtemp, mkdir, rm, symlink, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { describe, expect, it } from "vitest"
import type { ResearchCollection } from "../src/ontology/collection.ts"
import { auditDeclaredResearchCoverage } from "../src/ontology/coverage.ts"
import {
  assertLifecycleDocumentMatchesRuntime,
  assertSupportedResearchSchemaVersion
} from "../src/ontology/lifecycle.ts"

const coverageCollection = (
  corpusRoots: ReadonlyArray<string>,
  coverageLedger: ReadonlyArray<{ path: string; status: "INDEXED" | "PARTIAL"; reason: string }>
): ResearchCollection =>
  ({
    graphs: corpusRoots.map((corpus_roots, index) => ({ corpus_roots, key: `g${index}` })),
    coverage_ledger: coverageLedger
  }) as unknown as ResearchCollection

describe("research schema lifecycle", () => {
  it("accepts only registered versions and keeps the checked-in lifecycle in sync", async () => {
    const source = await (await import("node:fs/promises")).readFile(
      "ontology/schema/research-schema-lifecycle.json",
      "utf8"
    )
    expect(() => assertLifecycleDocumentMatchesRuntime(source)).not.toThrow()
    expect(() =>
      assertSupportedResearchSchemaVersion("research-graph", "research-graph/v1")
    ).not.toThrow()
    expect(() =>
      assertSupportedResearchSchemaVersion("research-graph", "research-graph/v2")
    ).toThrow("explicit migration registry entry")
  })
})

describe("declared research coverage audit", () => {
  it("uses the longest matching coverage prefix deterministically", async () => {
    const root = await mkdtemp(join(tmpdir(), "ice-coverage-"))
    try {
      await mkdir(join(root, "research", "nested"), { recursive: true })
      await writeFile(join(root, "research", "nested", "note.md"), "fixture")
      const report = await auditDeclaredResearchCoverage(
        root,
        coverageCollection(["research"], [
          { path: "research", status: "PARTIAL", reason: "broad" },
          { path: "research/nested", status: "INDEXED", reason: "specific" }
        ])
      )
      expect(report).toMatchObject({ valid: true, files: 1, mapped_files: 1 })
      expect(report.by_status).toEqual({ INDEXED: 1 })
    } finally {
      await rm(root, { recursive: true, force: true })
    }
  })

  it("fails closed for unmapped files and symlinks", async () => {
    const root = await mkdtemp(join(tmpdir(), "ice-coverage-"))
    try {
      await mkdir(join(root, "research"), { recursive: true })
      await writeFile(join(root, "research", "note.md"), "fixture")
      await symlink("note.md", join(root, "research", "link.md"))
      const report = await auditDeclaredResearchCoverage(
        root,
        coverageCollection(["research"], [])
      )
      expect(report.valid).toBe(false)
      expect(report.issues.map(({ code }) => code)).toEqual([
        "COVERAGE_SYMLINK_REJECTED",
        "COVERAGE_UNMAPPED_FILE"
      ])
    } finally {
      await rm(root, { recursive: true, force: true })
    }
  })
})
