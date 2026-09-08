import { createHash } from "node:crypto"
import { cp, lstat, mkdir, readFile, symlink, writeFile } from "node:fs/promises"
import { resolve, relative, join } from "node:path"
import { spawnSync } from "node:child_process"

const hash = async (path) => createHash("sha256").update(await readFile(path)).digest("hex")
const reviewedPatchSha256 = "20b1eecf24b954afb46330baf251975fc77e28e9d6ef7e0f1ae83cb0d266fa51"
const args = process.argv.slice(2)
const value = (flag) => { const i = args.indexOf(flag); return i < 0 ? undefined : args[i + 1] }
const hswmRoot = value("--hswm-root"), output = value("--output"), activate = args.includes("--activate")
if (!hswmRoot || !output || args.some((x) => x.startsWith("--") && !["--hswm-root", "--output", "--activate"].includes(x)) ||
    !output.startsWith(".ice/hswm-research/native/") || output.includes("..") || relative(process.cwd(), resolve(output)).startsWith("..")) throw new Error("Usage: node scripts/qualify-hswm-context-key.mjs --hswm-root PATH --output .ice/hswm-research/native/NAME [--activate]")
const sourceRoot = resolve(hswmRoot, "src/hswm/effect-runtime")
const destination = resolve(output), source = join(sourceRoot, "src/adaptive-domain.ts"), copied = join(destination, "src/adaptive-domain.ts")
const patchPath = "research/hswm/upstream/context-attempt-key-bound.patch"
if (await hash(patchPath) !== reviewedPatchSha256) throw new Error("Reviewed context-key patch bytes changed; refuse qualification")
try { await lstat(destination); throw new Error(`Output already exists: ${output}`) } catch (error) { if (error?.code !== "ENOENT") throw error }
await mkdir(destination, { recursive: true })
await cp(join(sourceRoot, "dist"), join(destination, "dist"), { recursive: true })
await mkdir(join(destination, "src")); await cp(source, copied)
await symlink(join(sourceRoot, "node_modules"), join(destination, "node_modules"))
const originalSourceSha256 = await hash(copied)
const before = await readFile(copied, "utf8")
const needle = 'const featureText = (value: unknown): value is string => typeof value === "string" && value.trim().length > 0 && value.length <= 2048;'
const validation = 'Object.entries(attempts).every(([key, value]) => text(key) && Number.isSafeInteger(value) && value >= 0)'
const added = `${needle}\n// A context-attempt key is \`context:\` plus at most MAX_FEATURES - 1 validated\n// feature keys, separated by \`|\`.  Keep its bound derived from that model\n// contract rather than the public identifier bound used for field names.\nconst MAX_CONTEXT_ATTEMPT_KEY_CHARS = "context:".length + (MAX_FEATURES - 1) * (2048 + "|".length);\nconst contextAttemptKeyText = (value: unknown): value is string => typeof value === "string" && value.trim().length > 0 && value.length <= MAX_CONTEXT_ATTEMPT_KEY_CHARS;`
if ((before.match(new RegExp(needle.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) ?? []).length !== 1 || !before.includes(validation)) throw new Error("Upstream adaptive-domain.ts does not match the reviewed patch context")
await writeFile(copied, before.replace(needle, added).replace(validation, validation.replace("text(key)", "contextAttemptKeyText(key)")))
const patchedSourceSha256 = await hash(copied)
const tsc = resolve("node_modules/typescript/bin/tsc")
const compiled = spawnSync(process.execPath, [tsc, "--target", "ES2022", "--module", "NodeNext", "--moduleResolution", "NodeNext", "--strict", "--exactOptionalPropertyTypes", "--noUncheckedIndexedAccess", "--noImplicitOverride", "--noUnusedLocals", "--noUnusedParameters", "--noPropertyAccessFromIndexSignature", "--noEmitOnError", "--forceConsistentCasingInFileNames", "--useUnknownInCatchVariables", "--verbatimModuleSyntax", "--isolatedModules", "--skipLibCheck", "--outDir", join(destination, "dist"), "--rootDir", join(destination, "src"), copied], { encoding: "utf8" })
if (compiled.status !== 0) throw new Error(`Patched TypeScript did not compile:\n${compiled.stdout}${compiled.stderr}`)
const critical = ["hswm-live-process.js", "adaptive-cli.js", "adaptive-runtime.js", "adaptive-domain.js", "adaptive-executor.js", "adaptive-store.js", "effect-bounded-subprocess.js", "effect-process-main.js"]
const files = await Promise.all(critical.map(async (name) => { const path = `${output}/dist/${name}`; return { path, sha256: await hash(join(destination, "dist", name)) } }))
const record = { schema: "ice-hswm-native-qualification/v1", entry: `${output}/dist/hswm-live-process.js`, files,
  qualification: { scope: "synthetic engineering regression; not a physics result or HSWM efficacy claim", patch: patchPath, patch_sha256: reviewedPatchSha256, original_source_sha256: originalSourceSha256, patched_source_sha256: patchedSourceSha256, original_compiled_sha256: await hash(join(sourceRoot, "dist/adaptive-domain.js")), patched_compiled_sha256: await hash(join(destination, "dist/adaptive-domain.js")), typescript: JSON.parse(await readFile("node_modules/typescript/package.json", "utf8")).version } }
await writeFile(join(destination, "native-entry.candidate.json"), `${JSON.stringify(record, null, 2)}\n`, { flag: "wx" })
if (activate) await writeFile(".ice/hswm-research/native-entry.json", `${JSON.stringify(record, null, 2)}\n`)
console.log(JSON.stringify({ output, candidate: `${output}/native-entry.candidate.json`, activated: activate, files: files.length }, null, 2))
