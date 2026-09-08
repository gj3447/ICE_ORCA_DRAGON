import { promises as fs } from "node:fs"
import { createHash } from "node:crypto"
import { join, resolve } from "node:path"
import { asJsonObject } from "../research-context/core.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"

/** An explicit, pinned local qualification build can precede an upstream release. */
export const resolveNativeEntry = async (root: string, hswmRoot: string) => {
  if (process.env.ICE_HSWM_NATIVE_ENTRY) return { path: resolve(process.env.ICE_HSWM_NATIVE_ENTRY), origin: "environment", pins: {} }
  const path = join(root, ".ice/hswm-research/native-entry.json")
  let bytes: string
  try { bytes = await fs.readFile(path, "utf8") }
  catch (error) {
    if (error instanceof Error && "code" in error && error.code === "ENOENT") return {
      path: join(hswmRoot, "src/hswm/effect-runtime/dist/hswm-live-process.js"), origin: "installed", pins: {}
    }
    throw error
  }
  const config = asJsonObject(JSON.parse(bytes))
  if (config?.schema !== "ice-hswm-native-qualification/v1" || typeof config.entry !== "string" ||
      !isSafeArtifactPath(config.entry) || !config.entry.startsWith(".ice/hswm-research/native/") ||
      !Array.isArray(config.files) || config.files.length < 1 || config.files.length > 16) throw new Error("Invalid local native qualification record")
  const pins: Record<string, string> = {}
  for (const raw of config.files) {
    const pin = asJsonObject(raw)
    if (typeof pin?.path !== "string" || !isSafeArtifactPath(pin.path) || !pin.path.startsWith(".ice/hswm-research/native/") ||
        typeof pin.sha256 !== "string" || !/^[a-f0-9]{64}$/.test(pin.sha256) || Object.hasOwn(pins, pin.path)) throw new Error("Invalid native qualification pin")
    const actual = createHash("sha256").update(await fs.readFile(join(root, pin.path))).digest("hex")
    if (actual !== pin.sha256) throw new Error(`Native qualification bytes changed: ${pin.path}`)
    pins[pin.path] = actual
  }
  if (!Object.hasOwn(pins, config.entry)) throw new Error("Native qualification must pin its entry")
  return { path: join(root, config.entry), origin: "local_qualification", pins }
}
