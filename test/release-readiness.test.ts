import { readFileSync } from "node:fs"
import { expect, it } from "vitest"

const workflowPaths = [
  ".github/workflows/graph-control-plane.yml",
  ".github/workflows/dependency-review.yml",
  ".github/workflows/release-readiness.yml"
] as const

const workflow = (path: string): string => readFileSync(path, "utf8")

it("pins every third-party GitHub Action to a full commit SHA", () => {
  for (const path of workflowPaths) {
    const source = workflow(path)
    const actionLines = source.split("\n").filter((line) => /^\s*uses:/.test(line))
    expect(actionLines.length, path).toBeGreaterThan(0)
    for (const line of actionLines) {
      expect(line, `${path}: ${line.trim()}`).toMatch(/@[0-9a-f]{40}(?:\s+#.*)?$/)
    }
    expect(source, path).not.toContain("pull_request_target")
  }
})

it("builds both locked runtime planes before graph tests", () => {
  for (const path of [
    ".github/workflows/graph-control-plane.yml",
    ".github/workflows/release-readiness.yml"
  ]) {
    const source = workflow(path)
    expect(source, path).toContain(
      "astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d"
    )
    expect(source, path).toContain('version: "0.12.7"')
    expect(source, path).toContain('python-version: "3.13"')
    expect(source, path).toContain("run: uv sync --locked")
    expect(source, path).toContain("run: npm ci")
  }
})

it("keeps workflow permissions read-only and runs the declared gates", () => {
  const graph = workflow(".github/workflows/graph-control-plane.yml")
  const dependency = workflow(".github/workflows/dependency-review.yml")
  const release = workflow(".github/workflows/release-readiness.yml")
  expect(graph).toContain("permissions:\n  contents: read")
  expect(graph).toContain("run: npm run graph:check")
  expect(dependency).toContain("permissions:\n  contents: read\n  pull-requests: read")
  expect(release).toContain("permissions:\n  contents: read")
  expect(release).toContain("run: npm run graph:release-check")
})
