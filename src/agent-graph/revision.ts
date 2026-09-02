import { createHash } from "node:crypto"
import { execFile } from "node:child_process"
import { constants } from "node:fs"
import { open, readdir, realpath } from "node:fs/promises"
import { relative, resolve } from "node:path"
import type { ResearchCollection } from "../ontology/collection.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import type { ResearchAgentWorkflowPlan } from "./core.ts"
import type {
  ResearchAgentRevisionPin,
  Sha256PinnedDocument
} from "./durable.ts"

const resolveHead = (
  workspaceRoot: string
): Promise<string> =>
  new Promise((resolveHeadCommit, reject) => {
    execFile(
      "git",
      ["rev-parse", "--verify", "HEAD"],
      { cwd: workspaceRoot, encoding: "utf8", maxBuffer: 4096 },
      (error, stdout, stderr) => {
        if (error !== null) {
          reject(new Error(`cannot resolve HEAD: ${stderr.trim() || error.message}`))
          return
        }
        const head = stdout.trim()
        if (!/^[a-f0-9]{40,64}$/.test(head)) {
          reject(new Error("git returned an invalid resolved HEAD commit"))
          return
        }
        resolveHeadCommit(head)
      }
    )
  })

const hashWorkspaceFile = async (
  workspaceRoot: string,
  path: string
): Promise<Sha256PinnedDocument> => {
  if (!isSafeArtifactPath(path)) {
    throw new Error(`unsafe revision-pin path '${path}'`)
  }
  const root = await realpath(workspaceRoot)
  const candidate = resolve(root, path)
  const target = await realpath(candidate)
  if (relative(root, target) !== path) {
    throw new Error(`revision-pin path resolves outside the workspace: '${path}'`)
  }
  // Open the caller-visible path with O_NOFOLLOW after containment checking so
  // a final-component symlink is not silently accepted between review steps.
  const handle = await open(candidate, constants.O_RDONLY | constants.O_NOFOLLOW)
  try {
    const info = await handle.stat()
    if (!info.isFile()) {
      throw new Error(`revision-pin path is not a regular file: '${path}'`)
    }
    const hash = createHash("sha256")
    for await (const chunk of handle.createReadStream()) hash.update(chunk)
    return { path, sha256: hash.digest("hex") }
  } finally {
    await handle.close()
  }
}

const captureControlPlaneSources = async (
  workspaceRoot: string
): Promise<ReadonlyArray<Sha256PinnedDocument>> => {
  const root = await realpath(workspaceRoot)
  const sourceRoot = await realpath(resolve(root, "src"))
  if (relative(root, sourceRoot) !== "src") {
    throw new Error("control-plane source root resolves outside the workspace")
  }
  const paths: string[] = []
  const visit = async (directory: string, relpath: string): Promise<void> => {
    const entries = await readdir(directory, { withFileTypes: true })
    for (const entry of entries) {
      const childRelpath = relpath.length === 0 ? entry.name : `${relpath}/${entry.name}`
      const child = resolve(directory, entry.name)
      if (entry.isSymbolicLink()) {
        throw new Error(`control-plane source may not be a symlink: 'src/${childRelpath}'`)
      }
      if (entry.isDirectory()) {
        await visit(child, childRelpath)
      } else if (entry.isFile() && entry.name.endsWith(".ts")) {
        paths.push(`src/${childRelpath}`)
      }
    }
  }
  await visit(sourceRoot, "")
  paths.push("ice", "package.json", "package-lock.json", "tsconfig.json")
  return Promise.all(
    [...new Set(paths)].sort().map((path) => hashWorkspaceFile(root, path))
  )
}

const uniqueSourceLocators = (
  plan: ResearchAgentWorkflowPlan
): ReadonlyArray<Sha256PinnedDocument> => {
  const byPath = new Map<string, Sha256PinnedDocument>()
  for (const { unit } of plan.retrieval.hits) {
    const locator = unit.source_locator
    if (
      locator === undefined ||
      locator.kind === "source" ||
      byPath.has(locator.path)
    ) {
      continue
    }
    byPath.set(locator.path, { path: locator.path, sha256: locator.sha256 })
  }
  return [...byPath.values()].sort((left, right) =>
    left.path < right.path ? -1 : left.path > right.path ? 1 : 0
  )
}

/** Capture the exact control plane, ontology, and retrieved local-document revision. */
export const captureResearchAgentRevisionPin = async (
  workspaceRoot: string,
  collection: ResearchCollection,
  plan: ResearchAgentWorkflowPlan,
  options: { readonly includeRetrievedDocuments?: boolean } = {}
): Promise<ResearchAgentRevisionPin> => {
  const descriptors = collection.graphs.filter(
    ({ key }) => plan.retrieval.graph === "all" || key === plan.retrieval.graph
  )
  if (descriptors.length === 0) {
    throw new Error(`no ontology graph matches '${plan.retrieval.graph}'`)
  }
  const recordedSources = options.includeRetrievedDocuments === false
    ? []
    : uniqueSourceLocators(plan)
  const [headCommit, collectionPin, graphPins, sourcePins, controlPlanePins] = await Promise.all([
    resolveHead(workspaceRoot),
    hashWorkspaceFile(workspaceRoot, collection.canonical_file),
    Promise.all(
      descriptors.map(({ path }) => hashWorkspaceFile(workspaceRoot, path))
    ),
    Promise.all(
      recordedSources.map(({ path }) => hashWorkspaceFile(workspaceRoot, path))
    ),
    captureControlPlaneSources(workspaceRoot)
  ])
  for (const observed of sourcePins) {
    const recorded = recordedSources.find(({ path }) => path === observed.path)
    if (recorded?.sha256 !== observed.sha256) {
      throw new Error(
        `retrieved source hash drift for '${observed.path}': expected ${recorded?.sha256}, observed ${observed.sha256}`
      )
    }
  }
  return {
    head_commit: headCommit,
    collection: collectionPin,
    graphs: graphPins,
    source_documents: sourcePins,
    control_plane_sources: controlPlanePins
  }
}

/** Re-observe exactly the paths carried by an existing durable run. */
export const observeResearchAgentRevisionPin = async (
  workspaceRoot: string,
  pin: ResearchAgentRevisionPin
): Promise<ResearchAgentRevisionPin> => {
  const [headCommit, collection, graphs, sourceDocuments, controlPlaneSourcePins] = await Promise.all([
    resolveHead(workspaceRoot),
    hashWorkspaceFile(workspaceRoot, pin.collection.path),
    Promise.all(
      pin.graphs.map(({ path }) => hashWorkspaceFile(workspaceRoot, path))
    ),
    Promise.all(
      pin.source_documents.map(({ path }) => hashWorkspaceFile(workspaceRoot, path))
    ),
    captureControlPlaneSources(workspaceRoot)
  ])
  return {
    head_commit: headCommit,
    collection,
    graphs,
    source_documents: sourceDocuments,
    control_plane_sources: controlPlaneSourcePins
  }
}
