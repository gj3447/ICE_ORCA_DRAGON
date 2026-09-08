import { spawn } from "node:child_process"
import { fileURLToPath, pathToFileURL } from "node:url"
import { expect, it } from "vitest"

const moduleUrl = pathToFileURL(fileURLToPath(new URL("../src/research-engine/cell.ts", import.meta.url))).href

const readInChild = (input: string): Promise<{ readonly code: number | null; readonly stdout: string; readonly stderr: string }> => new Promise((resolve, reject) => {
  const program = `import { readResearchCellStdin } from ${JSON.stringify(moduleUrl)}; try { const value = await readResearchCellStdin(); process.stdout.write(JSON.stringify({ value, stdin: process.stdin.constructor.name })); } catch (error) { process.stderr.write(error instanceof Error ? error.message : String(error)); process.exitCode = 2; }`
  const child = spawn(process.execPath, ["--import", "tsx", "--input-type=module", "--eval", program], { stdio: ["pipe", "pipe", "pipe"] })
  let stdout = ""
  let stderr = ""
  child.stdout.setEncoding("utf8").on("data", (chunk: string) => { stdout += chunk })
  child.stderr.setEncoding("utf8").on("data", (chunk: string) => { stderr += chunk })
  child.on("error", reject)
  child.on("close", (code) => resolve({ code, stdout, stderr }))
  child.stdin.end(input)
})

it("reads JSON through a spawned Node child stdin socket", async () => {
  const result = await readInChild('{"socket":true}')
  expect(result.code).toBe(0)
  expect(JSON.parse(result.stdout)).toEqual({ value: '{"socket":true}', stdin: "Socket" })
})

it("rejects stdin beyond the bounded cell-input limit before parsing", async () => {
  const result = await readInChild("x".repeat(64 * 1024 * 4 + 1))
  expect(result.code).toBe(2)
  expect(result.stderr).toContain("cell stdin exceeds 65536 characters")
})
