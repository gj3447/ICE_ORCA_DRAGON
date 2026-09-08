import { Console, Effect } from "effect"
import { createHash, randomUUID } from "node:crypto"
import { promises as fs } from "node:fs"
import { hostname } from "node:os"
import { join, relative, resolve } from "node:path"
import { iceError } from "../errors.ts"
import { graphHarnessContext } from "../harness/core.ts"
import { findCollectionNodes } from "../ontology/collection-core.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { capture } from "../process.ts"
import { Workspace } from "../workspace.ts"
import { asJsonObject, buildHswmRequest, buildResearchContextSource, type PreparedResource } from "./core.ts"
import { observeResearchReferences } from "./usl.ts"
import { resolveNativeEntry } from "../research-engine/native-entry.ts"

const maxReferenceBytes = 1_000_000
const sha = (bytes: string | Uint8Array): string => createHash("sha256").update(bytes).digest("hex")
const jsonObject = (value: unknown) => {
  const object = asJsonObject(value)
  if (object === undefined) throw new Error("Expected a JSON object")
  return object
}
const io = <A>(f: () => Promise<A>) => Effect.tryPromise({
  try: f,
  catch: (error) => iceError("RESEARCH_CONTEXT_ERROR", error instanceof Error ? error.message : String(error))
})

export const externalRoots = (root: string) => ({
  hswm: resolve(process.env.ICE_HSWM_ROOT ?? join(root, "../HSWM")),
  usl: resolve(process.env.ICE_USL_ROOT ?? join(root, "../USL"))
})

const runtimeFiles = {
  hswm: ["pyproject.toml", "uv.lock", "src/hswm/infrastructure/usl_cli.py",
    "src/hswm/infrastructure/usl_adapter.py", "src/hswm/infrastructure/usl_observation_v2.py",
    "src/hswm/cells/conditional.py",
    "src/hswm/effect-runtime/package.json", "src/hswm/effect-runtime/package-lock.json",
    ...["adaptive-cli", "adaptive-runtime", "adaptive-domain", "adaptive-executor", "adaptive-store",
      "hswm-live-process", "effect-bounded-subprocess", "effect-process-main"].flatMap((name) => [
      `src/hswm/effect-runtime/src/${name}.ts`, `src/hswm/effect-runtime/dist/${name}.js`
    ])],
  usl: ["package.json", "package-lock.json", "src/language/index.ts",
    "src/language/compiler.ts", "src/language/runtime.ts", "src/language/digest.ts",
    "src/language/observation-schema.ts", "src/language/parser.ts", "src/language/model.ts",
    "src/locator.ts", "src/resolve.ts", "src/domain.ts"]
} as const

export const researchRuntimeStatus = (root: string) => io(async () => {
  const roots = externalRoots(root)
  const fingerprints: Record<string, string> = {}
  const missing: string[] = []
  for (const kind of ["hswm", "usl"] as const) {
    for (const file of runtimeFiles[kind]) {
      const path = join(roots[kind], file)
      try { fingerprints[`${kind}/${file}`] = sha(await fs.readFile(path)) }
      catch { missing.push(path) }
    }
  }
  for (const path of [join(roots.hswm, ".venv/bin/python"),
    join(roots.usl, "node_modules/effect/dist/esm/index.js")]) {
    try { await fs.access(path) } catch { missing.push(path) }
  }
  const nativeEntry = await resolveNativeEntry(root, roots.hswm)
  try { fingerprints["native_entry"] = sha(await fs.readFile(nativeEntry.path)) } catch { missing.push(nativeEntry.path) }
  Object.assign(fingerprints, nativeEntry.pins)
  return {
    schema: "ice-hswm-usl-runtime/v1", available: missing.length === 0, roots, backend: "typescript-effect", native_entry: nativeEntry.path, native_entry_origin: nativeEntry.origin,
    missing, fingerprints,
    fingerprint_scope: "Listed interface sources, executed native build files and lockfiles; not source-build equivalence or full dependency attestation",
    mode: "HSWM_ADAPTIVE_RESEARCH_WITH_USL_CONTEXT",
    semantic_truth: "NOT_EVALUATED", learning: "EXPLICIT_REVIEW_FEEDBACK",
    execution: "HSWM_COMMAND_CELLS_WITH_CODEX_LLM_AND_ICE_RUN",
    llm_auth: "Inherited from installed Codex CLI; this source inspection does not test login"
  }
})

export const researchStatusCommand = (json: boolean) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const status = yield* researchRuntimeStatus(root)
  yield* Console.log(json ? JSON.stringify(status, null, 2) : [
    `HSWM / USL research interfaces: ${status.available ? "AVAILABLE" : "UNAVAILABLE"}`,
    `HSWM: ${status.roots.hswm}`, `USL: ${status.roots.usl}`,
    "Mode: HSWM route selection → USL context → LLM research cells → reviewed route feedback",
    ...status.missing.map((path) => `missing: ${path}`)
  ].join("\n"))
  if (!status.available) process.exitCode = 2
})

export const readLocalReference = async (root: string, path: string): Promise<Buffer> => {
  if (!isSafeArtifactPath(path)) throw new Error(`Expected a repository-relative reference path: ${path}`)
  const realRoot = await fs.realpath(root)
  const real = await fs.realpath(join(realRoot, path))
  if (!isSafeArtifactPath(relative(realRoot, real))) throw new Error(`Reference escapes ICE workspace: ${path}`)
  const stat = await fs.stat(real)
  if (!stat.isFile() || stat.size > maxReferenceBytes) {
    throw new Error(`Reference must be a regular file no larger than ${maxReferenceBytes} bytes: ${path}`)
  }
  const bytes = await fs.readFile(real)
  if (bytes.length > maxReferenceBytes) throw new Error(`Reference grew beyond the read limit: ${path}`)
  return bytes
}

const localFileLocator = (path: string): string => {
  if (/[\s#?%]/u.test(path)) throw new Error("Current USL file locator grammar cannot represent whitespace, #, ? or % in this path")
  return `file://${hostname()}${path}`
}

export const researchPrepareCommand = (
  question: string, targetId: string, references: ReadonlyArray<string>, json: boolean
) => Effect.gen(function* () {
  const { root } = yield* Workspace
  if (!/^[a-z0-9-]+::[a-z_]+:[A-Za-z0-9_.:-]+$/.test(targetId)) {
    return yield* Effect.fail(iceError("RESEARCH_TARGET_INVALID", "Use an exact qualified graph::node target", 2))
  }
  if (!question.trim() || question.length > 500 || references.length > 4 || new Set(references).size !== references.length) {
    return yield* Effect.fail(iceError("RESEARCH_INPUT_INVALID", "Use a 1–500 character question and at most four distinct reference paths", 2))
  }
  const status = yield* researchRuntimeStatus(root)
  if (!status.available) return yield* Effect.fail(iceError("RESEARCH_RUNTIME_UNAVAILABLE",
    `Set ICE_HSWM_ROOT / ICE_USL_ROOT to installed checkouts; missing: ${status.missing.join(", ")}`, 2))
  const loaded = yield* loadValidOntologyCollectionStructure
  const matches = findCollectionNodes(loaded.graphs, targetId)
  const match = matches[0]
  const graph = loaded.graphs.find((item) => item.descriptor.key === match?.key)
  if (matches.length !== 1 || match === undefined || graph === undefined) {
    return yield* Effect.fail(iceError("RESEARCH_TARGET_NOT_FOUND", `No unique canonical node: ${targetId}`, 2))
  }
  const context = graphHarnessContext(graph, match.node, 1, 32)
  const prepared = yield* io(async () => {
    const realRoot = await fs.realpath(root)
    const readTarget = async () => {
      const path = join(realRoot, graph.descriptor.path)
      if ((await fs.stat(path)).size > 8_000_000) throw new Error("Native graph exceeds context read limit")
      const native = jsonObject(JSON.parse(await fs.readFile(path, "utf8")))
      if (!Array.isArray(native.nodes)) throw new Error("Native graph has no nodes")
      const node = native.nodes.find((node) => node !== null && typeof node === "object" && !Array.isArray(node) && node.id === match.node.id)
      if (node === undefined) throw new Error(`Canonical node no longer resolves: ${targetId}`)
      return sha(JSON.stringify(node))
    }
    const targetPin = await readTarget()
    // Check explicit references before creating a session. The observed bytes
    // are read again by USL's local resolver; these are independent policy pins.
    const pins = await Promise.all(references.map(async (path) => {
      const bytes = await readLocalReference(realRoot, path)
      const canonical = graph.graph.nodes.find((node) => node.path === path && node.sha256 !== undefined)
      const contentHash = sha(bytes)
      if (canonical?.sha256 !== undefined && canonical.sha256 !== contentHash) {
        throw new Error(`Tracked graph hash differs from reference bytes: ${path}`)
      }
      return { path, contentHash, locator: localFileLocator(await fs.realpath(join(realRoot, path))) }
    }))
    const parent = join(realRoot, ".ice/research-context")
    await fs.mkdir(parent, { recursive: true })
    if (await fs.realpath(parent) !== parent) throw new Error("Research context directory must not redirect through a symlink")
    const session = join(parent, randomUUID())
    await fs.mkdir(session)
    const contextPath = join(session, "context.json")
    const contextText = JSON.stringify({ question, target: match.node, context }, null, 2)+"\n"
    await fs.writeFile(contextPath, contextText, { flag: "wx" })
    const targetLocator = `kg://ice-${match.key}/${match.node.id}`
    const resources: PreparedResource[] = [
      { name: "target", role: "target", kind: "kg", locator: targetLocator, contentHash: targetPin },
      { name: "context", role: "context", kind: "filesystem", locator: localFileLocator(contextPath), contentHash: sha(contextText) },
      ...pins.map((pin, index): PreparedResource => ({ name: `reference_${index}`, role: `reference_${index}`,
        kind: "filesystem", locator: pin.locator, contentHash: pin.contentHash }))
    ]
    const allowedFiles = new Map([
      [localFileLocator(contextPath), relative(realRoot, contextPath)],
      ...pins.map((pin): [string, string] => [pin.locator, relative(realRoot, new URL(pin.locator).pathname)])
    ])
    const readSnapshot = async (locator: string) => {
      if (locator === targetLocator) {
        // Re-read the actual native graph node, rather than returning its pin.
        return { contentHash: await readTarget() }
      }
      const path = allowedFiles.get(locator)
      if (path === undefined) throw new Error(`Undeclared reference: ${locator}`)
      return { contentHash: sha(await readLocalReference(realRoot, path)) }
    }
    return { session, resources, readSnapshot }
  })
  const source = yield* io(async () => buildResearchContextSource({ question, target: targetId, resources: prepared.resources }))
  yield* io(() => fs.writeFile(join(prepared.session, "references.usl"), source, { flag: "wx" }))
  const observation = yield* io(() => observeResearchReferences(status.roots.usl, source, prepared.resources, prepared.readSnapshot))
  const request = yield* io(async () => buildHswmRequest({ source, plan: observation.plan, report: observation.report,
    preparedResources: prepared.resources }))
  const requestPath = join(prepared.session, "hswm-request.json")
  yield* io(async () => {
    await fs.writeFile(requestPath, JSON.stringify(request, null, 2)+"\n", { flag: "wx" })
  })
  const preview = yield* capture({ command: "uv", args: ["run", "--locked", "--no-sync", "--project",
    status.roots.hswm, "hswm-usl", "preview", "--request", requestPath], cwd: root,
    captureLimitCharacters: 1_048_576 }, 30)
  yield* io(() => fs.writeFile(join(prepared.session, "hswm-process.json"), JSON.stringify(preview, null, 2)+"\n", { flag: "wx" }))
  if (preview.exitCode !== 0) return yield* Effect.fail(iceError("HSWM_PREVIEW_FAILED",
    `hswm-usl exited ${preview.exitCode}; diagnostics: ${join(prepared.session, "hswm-process.json")}`, preview.exitCode))
  const hswm = yield* io(async () => jsonObject(JSON.parse(preview.stdout)))
  const finalRuntime = yield* researchRuntimeStatus(root)
  if (JSON.stringify(finalRuntime.fingerprints) !== JSON.stringify(status.fingerprints)) {
    return yield* Effect.fail(iceError("RESEARCH_RUNTIME_CHANGED", "External interface files changed during preparation; inspect the saved session"))
  }
  const result = {
    schema: "ice-hswm-usl-research-context/v1", question, target: targetId,
    session: relative(root, prepared.session), context, resources: prepared.resources,
    runtime: status, usl_observation: observation.report, hswm,
    scope: "Research reference preparation; semantic truth and scientific checks remain unevaluated",
    next_commands: [["./ice", "harness", "context", targetId],
      ...(match.key === "cpt" ? [["./ice", "agent", "plan", question, "--graph", "cpt", "--json"]] : [])],
    scientific_execution: "NOT_INVOKED", learning: "NOT_CONNECTED", external_kg_write: "NOT_INVOKED"
  }
  yield* io(() => fs.writeFile(join(prepared.session, "session.json"), JSON.stringify(result, null, 2)+"\n", { flag: "wx" }))
  yield* Console.log(json ? JSON.stringify(result, null, 2) : [
    `Prepared HSWM / USL research context: ${targetId}`,
    `Observed ${prepared.resources.length} local references; HSWM returned a proposal preview.`,
    `Session: ${join(prepared.session, "session.json")}`,
    "Read the context and inspect the proposal before designing the bounded research calculation."
  ].join("\n"))
})
