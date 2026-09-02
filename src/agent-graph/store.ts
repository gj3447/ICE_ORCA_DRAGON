import {
  constants,
} from "node:fs"
import {
  mkdir,
  open,
  realpath,
  rename,
  rm,
  writeFile
} from "node:fs/promises"
import { join, relative, resolve } from "node:path"
import {
  auditResearchAgentRun,
  decodeResearchAgentRun,
  type ResearchAgentRunV1
} from "./durable.ts"

export const RESEARCH_AGENT_RUNS_RELPATH = ".ice/agent-runs" as const
const MAX_RUN_BYTES = 8 * 1024 * 1024
const runIdPattern = /^[a-z0-9][a-z0-9_-]{2,127}$/
const sha256Pattern = /^[a-f0-9]{64}$/

export const isSafeResearchAgentRunId = (runId: string): boolean =>
  runIdPattern.test(runId)

const assertSafeRunId = (runId: string): void => {
  if (!isSafeResearchAgentRunId(runId)) {
    throw new Error("run id must be 3-128 lowercase letters, digits, '_' or '-'")
  }
}

const assertContainedStore = (root: string, store: string): void => {
  if (relative(root, store) !== RESEARCH_AGENT_RUNS_RELPATH) {
    throw new Error("durable agent-run store resolves outside the workspace")
  }
}

const resolveExistingStore = async (workspaceRoot: string): Promise<string> => {
  const root = await realpath(workspaceRoot)
  const candidate = resolve(root, RESEARCH_AGENT_RUNS_RELPATH)
  const store = await realpath(candidate)
  assertContainedStore(root, store)
  return store
}

const resolveWritableStore = async (workspaceRoot: string): Promise<string> => {
  const root = await realpath(workspaceRoot)
  const stateCandidate = resolve(root, ".ice")
  await mkdir(stateCandidate, { recursive: true })
  const stateRoot = await realpath(stateCandidate)
  if (relative(root, stateRoot) !== ".ice") {
    throw new Error("durable agent state directory resolves outside the workspace")
  }
  const candidate = resolve(stateRoot, "agent-runs")
  await mkdir(candidate, { recursive: true })
  const store = await realpath(candidate)
  assertContainedStore(root, store)
  return store
}

const runPath = (store: string, runId: string): string =>
  join(store, `${runId}.json`)

const decodeRun = (source: string, expectedRunId: string): ResearchAgentRunV1 => {
  const run = decodeResearchAgentRun(JSON.parse(source))
  if (run.run_id !== expectedRunId) {
    throw new Error("durable run file does not match the requested run id")
  }
  const audit = auditResearchAgentRun(run)
  if (!audit.passed) {
    throw new Error(`durable run file failed integrity audit: ${audit.errors.join("; ")}`)
  }
  return run
}

const readRunAt = async (store: string, runId: string): Promise<ResearchAgentRunV1> => {
  const candidate = runPath(store, runId)
  const handle = await open(candidate, constants.O_RDONLY | constants.O_NOFOLLOW)
  try {
    const info = await handle.stat()
    if (!info.isFile() || info.size > MAX_RUN_BYTES) {
      throw new Error(`durable run file must be a regular file no larger than ${MAX_RUN_BYTES} bytes`)
    }
    return decodeRun((await handle.readFile()).toString("utf8"), runId)
  } finally {
    await handle.close()
  }
}

export const readResearchAgentRun = async (
  workspaceRoot: string,
  runId: string
): Promise<ResearchAgentRunV1> => {
  assertSafeRunId(runId)
  return readRunAt(await resolveExistingStore(workspaceRoot), runId)
}

export const writeNewResearchAgentRun = async (
  workspaceRoot: string,
  run: ResearchAgentRunV1
): Promise<string> => {
  assertSafeRunId(run.run_id)
  const audit = auditResearchAgentRun(run)
  if (!audit.passed) {
    throw new Error(`refusing to persist invalid durable run: ${audit.errors.join("; ")}`)
  }
  const store = await resolveWritableStore(workspaceRoot)
  const target = runPath(store, run.run_id)
  await writeFile(target, `${JSON.stringify(run, null, 2)}\n`, { flag: "wx" })
  return `${RESEARCH_AGENT_RUNS_RELPATH}/${run.run_id}.json`
}

export const updateResearchAgentRun = async (
  workspaceRoot: string,
  runId: string,
  expectedTipSha256: string,
  update: (run: ResearchAgentRunV1) => ResearchAgentRunV1 | Promise<ResearchAgentRunV1>
): Promise<ResearchAgentRunV1> => {
  assertSafeRunId(runId)
  if (!sha256Pattern.test(expectedTipSha256)) {
    throw new Error("expected trace tip must be a lowercase SHA-256")
  }
  const store = await resolveWritableStore(workspaceRoot)
  const lockPath = join(store, `${runId}.lock`)
  const lock = await open(lockPath, "wx")
  try {
    const current = await readRunAt(store, runId)
    if (current.trace.at(-1)?.event_sha256 !== expectedTipSha256) {
      throw new Error("durable run changed since review began; reload and review the new trace tip")
    }
    const next = await update(current)
    const audit = auditResearchAgentRun(next)
    if (!audit.passed) {
      throw new Error(`refusing to persist invalid durable run: ${audit.errors.join("; ")}`)
    }
    const temporary = join(
      store,
      `.${runId}.${process.pid}.${Date.now()}.tmp`
    )
    try {
      await writeFile(temporary, `${JSON.stringify(next, null, 2)}\n`, {
        flag: "wx"
      })
      await rename(temporary, runPath(store, runId))
    } catch (error) {
      await rm(temporary, { force: true })
      throw error
    }
    return next
  } finally {
    await lock.close()
    await rm(lockPath, { force: true })
  }
}
