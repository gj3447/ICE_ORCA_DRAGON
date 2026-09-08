import { createHash } from "node:crypto"
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { expect, it } from "vitest"
import { resolveNativeEntry } from "../src/research-engine/native-entry.ts"

const sha = (value: string): string => createHash("sha256").update(value).digest("hex")
const withoutEntryEnvironment = async <A>(run: () => Promise<A>): Promise<A> => {
  const prior = process.env.ICE_HSWM_NATIVE_ENTRY
  delete process.env.ICE_HSWM_NATIVE_ENTRY
  try { return await run() }
  finally {
    if (prior === undefined) delete process.env.ICE_HSWM_NATIVE_ENTRY
    else process.env.ICE_HSWM_NATIVE_ENTRY = prior
  }
}

const fixture = async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-native-entry-"))
  const native = ".ice/hswm-research/native"
  await mkdir(join(root, native), { recursive: true })
  await writeFile(join(root, `${native}/entry.js`), "export const live = true\n")
  await writeFile(join(root, `${native}/peer.js`), "export const peer = true\n")
  return { root, native }
}

const qualify = async (root: string, native: string, files: readonly string[]) => {
  const pins = await Promise.all(files.map(async (path) => {
    const bytes = await readFile(join(root, path), "utf8")
    return { path, sha256: sha(bytes) }
  }))
  await writeFile(join(root, ".ice/hswm-research/native-entry.json"), JSON.stringify({
    schema: "ice-hswm-native-qualification/v1", entry: `${native}/entry.js`, files: pins
  }))
}

it("falls back to the installed entry when no local qualification exists", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-native-fallback-"))
  try {
    await withoutEntryEnvironment(async () => {
      await expect(resolveNativeEntry(root, "/installed-hswm")).resolves.toEqual({
        path: "/installed-hswm/src/hswm/effect-runtime/dist/hswm-live-process.js", origin: "installed", pins: {}
      })
    })
  } finally { await rm(root, { recursive: true, force: true }) }
})

it("accepts a qualified entry with every pinned peer", async () => {
  const { root, native } = await fixture()
  try {
    await qualify(root, native, [`${native}/entry.js`, `${native}/peer.js`])
    await withoutEntryEnvironment(async () => {
      const result = await resolveNativeEntry(root, "/installed-hswm")
      expect(result).toMatchObject({ path: join(root, `${native}/entry.js`), origin: "local_qualification" })
      expect(Object.keys(result.pins)).toEqual([`${native}/entry.js`, `${native}/peer.js`])
    })
  } finally { await rm(root, { recursive: true, force: true }) }
})

it("rejects a changed peer and a record that omits the entry pin", async () => {
  const { root, native } = await fixture()
  try {
    await qualify(root, native, [`${native}/entry.js`, `${native}/peer.js`])
    await writeFile(join(root, `${native}/peer.js`), "export const peer = false\n")
    await withoutEntryEnvironment(async () => await expect(resolveNativeEntry(root, "/installed-hswm")).rejects.toThrow("bytes changed"))
    await qualify(root, native, [`${native}/peer.js`])
    await withoutEntryEnvironment(async () => await expect(resolveNativeEntry(root, "/installed-hswm")).rejects.toThrow("must pin its entry"))
  } finally { await rm(root, { recursive: true, force: true }) }
})

it("rejects a local qualification path outside the .ice native prefix", async () => {
  const { root, native } = await fixture()
  try {
    await writeFile(join(root, ".ice/hswm-research/native-entry.json"), JSON.stringify({
      schema: "ice-hswm-native-qualification/v1", entry: "native/entry.js",
      files: [{ path: `${native}/entry.js`, sha256: sha("export const live = true\n") }]
    }))
    await withoutEntryEnvironment(async () => await expect(resolveNativeEntry(root, "/installed-hswm")).rejects.toThrow("Invalid local native qualification"))
  } finally { await rm(root, { recursive: true, force: true }) }
})
