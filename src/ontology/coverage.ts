import { lstat, readdir, realpath } from "node:fs/promises"
import { resolve, relative, sep } from "node:path"
import type { ResearchCollection } from "./collection.ts"
import { isSafeArtifactPath } from "./core.ts"

const MAX_FILES = 100_000
const MAX_DIRECTORIES = 20_000
const MAX_DEPTH = 64

export interface CoverageAuditIssue {
  readonly code:
    | "COVERAGE_UNMAPPED_FILE"
    | "COVERAGE_SYMLINK_REJECTED"
    | "COVERAGE_PATH_ESCAPES_WORKSPACE"
    | "COVERAGE_LIMIT_EXCEEDED"
    | "COVERAGE_ROOT_READ_FAILED"
  readonly path: string
  readonly message: string
}

export interface CoverageAuditReport {
  readonly schema: "ice-research-coverage-audit/v1"
  readonly roots: ReadonlyArray<string>
  readonly files: number
  readonly mapped_files: number
  readonly by_status: Readonly<Record<string, number>>
  readonly issues: ReadonlyArray<CoverageAuditIssue>
  readonly valid: boolean
}

const contained = (root: string, candidate: string): boolean => {
  const rel = relative(root, candidate)
  return rel === "" || (!rel.startsWith(`..${sep}`) && rel !== ".." && !rel.startsWith("/"))
}

const bestCoverage = (collection: ResearchCollection, path: string) =>
  collection.coverage_ledger
    .filter(({ path: prefix }) => path === prefix || path.startsWith(`${prefix}/`))
    .sort((left, right) => right.path.length - left.path.length)[0]

/** Audits only declared corpus roots; archive/output paths are never discovered implicitly. */
export const auditDeclaredResearchCoverage = async (
  workspaceRoot: string,
  collection: ResearchCollection
): Promise<CoverageAuditReport> => {
  const rootReal = await realpath(workspaceRoot)
  const roots = [...new Set(collection.graphs.flatMap(({ corpus_roots }) => corpus_roots))].sort()
  const issues: CoverageAuditIssue[] = []
  const statuses: Record<string, number> = {}
  let files = 0
  let mapped = 0
  let directories = 0

  const visit = async (absolute: string, relpath: string, depth: number): Promise<void> => {
    if (depth > MAX_DEPTH || files > MAX_FILES || directories > MAX_DIRECTORIES) {
      issues.push({ code: "COVERAGE_LIMIT_EXCEEDED", path: relpath, message: "bounded coverage traversal limit exceeded" })
      return
    }
    const stat = await lstat(absolute)
    if (stat.isSymbolicLink()) {
      issues.push({ code: "COVERAGE_SYMLINK_REJECTED", path: relpath, message: "symlinks are rejected during coverage inventory" })
      return
    }
    const actual = await realpath(absolute)
    if (!contained(rootReal, actual)) {
      issues.push({ code: "COVERAGE_PATH_ESCAPES_WORKSPACE", path: relpath, message: "path resolves outside workspace" })
      return
    }
    if (stat.isDirectory()) {
      directories += 1
      for (const name of (await readdir(absolute)).sort()) {
        await visit(resolve(absolute, name), `${relpath}/${name}`, depth + 1)
      }
      return
    }
    if (!stat.isFile()) return
    files += 1
    const coverage = bestCoverage(collection, relpath)
    if (coverage === undefined) {
      issues.push({ code: "COVERAGE_UNMAPPED_FILE", path: relpath, message: "declared research-root file has no longest-prefix coverage ledger entry" })
      return
    }
    mapped += 1
    statuses[coverage.status] = (statuses[coverage.status] ?? 0) + 1
  }

  for (const corpusRoot of roots) {
    if (!isSafeArtifactPath(corpusRoot)) {
      issues.push({ code: "COVERAGE_PATH_ESCAPES_WORKSPACE", path: corpusRoot, message: "unsafe declared corpus root" })
      continue
    }
    try {
      await visit(resolve(rootReal, corpusRoot), corpusRoot, 0)
    } catch (error) {
      issues.push({
        code: "COVERAGE_ROOT_READ_FAILED",
        path: corpusRoot,
        message: `cannot inventory declared corpus root: ${error instanceof Error ? error.message : String(error)}`
      })
    }
  }
  return { schema: "ice-research-coverage-audit/v1", roots, files, mapped_files: mapped, by_status: statuses, issues, valid: issues.length === 0 }
}
