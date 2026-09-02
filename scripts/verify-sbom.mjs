import { spawnSync } from "node:child_process"

const npmCli = process.env.npm_execpath
const command = npmCli === undefined ? "npm" : process.execPath
const args = npmCli === undefined
  ? ["sbom", "--sbom-format", "cyclonedx", "--package-lock-only"]
  : [npmCli, "sbom", "--sbom-format", "cyclonedx", "--package-lock-only"]
const generated = spawnSync(command, args, {
  cwd: process.cwd(),
  encoding: "utf8",
  maxBuffer: 16 * 1024 * 1024,
  shell: false
})

if (generated.error !== undefined) throw generated.error
if (generated.status !== 0) {
  process.stderr.write(generated.stderr)
  process.exit(generated.status ?? 1)
}

const sbom = JSON.parse(generated.stdout)
if (
  sbom.bomFormat !== "CycloneDX" ||
  sbom.specVersion !== "1.5" ||
  !Array.isArray(sbom.components) ||
  sbom.components.length === 0
) {
  throw new Error("npm sbom did not produce a non-empty CycloneDX 1.5 inventory")
}

process.stdout.write(`${JSON.stringify({
  schema: "ice-node-sbom-check/v1",
  bom_format: sbom.bomFormat,
  spec_version: sbom.specVersion,
  component_count: sbom.components.length
})}\n`)
