import { Console, Effect } from "effect"
import { randomUUID, createHash } from "node:crypto"
import { promises as fs } from "node:fs"
import { join } from "node:path"
import { iceError } from "../errors.ts"
import { isSafeArtifactPath } from "../ontology/core.ts"
import { capture } from "../process.ts"
import { externalRoots, researchRuntimeStatus } from "../research-context/commands.ts"
import { asJsonObject } from "../research-context/core.ts"
import { Workspace } from "../workspace.ts"
import { loadResearchStateFile } from "./state-repository.ts"
import { renderResearchState } from "./state.ts"

export interface ResearchOptions {
  readonly question: string
  readonly target: string
  readonly references: readonly string[]
  readonly mode: "investigate" | "review" | "compute"
  readonly tier: "core" | "supporting"
  readonly runner: string
  readonly budget: number
  readonly stateFile?: string
}

const graphs = ["cpt", "hypercomplex", "legacy", "igrueqft"]
export const researchInvocation = (options: ResearchOptions) => {
  const graph = options.target.split("::")[0] ?? ""
  if (!graphs.includes(graph) || !/^[a-z0-9-]+::[a-z_]+:[A-Za-z0-9_.:-]+$/.test(options.target)) throw new Error("Use an exact qualified graph::node target")
  if (!options.question.trim() || options.question.length > 500) throw new Error("Question must contain 1–500 characters")
  if (options.references.length > 4 || new Set(options.references).size !== options.references.length || options.references.some((path) => !isSafeArtifactPath(path))) throw new Error("Provide at most four distinct repository-relative references")
  if (!Number.isInteger(options.budget) || options.budget < 30 || options.budget > 900) throw new Error("Episode budget must be an integer between 30 and 900 seconds")
  if ((options.mode === "compute") !== (options.runner.length > 0)) throw new Error("Only compute mode requires and accepts an explicit --runner")
  if (options.runner && (!isSafeArtifactPath(options.runner) || options.runner.startsWith("-") || /\s/.test(options.runner))) throw new Error("Runner must be a single ICE runner name or relative path")
  if (options.tier === "core" && graph !== "cpt") throw new Error("The declared core route belongs to CPT; use supporting for other graphs")
  return {
    context: { mode: options.mode, graph, tier: options.tier },
    task: { question: options.question, target: options.target, references: options.references, runner: options.runner || null }
  }
}

const io = <A>(run: () => Promise<A>) => Effect.tryPromise({ try: run,
  catch: (error) => iceError("HSWM_RESEARCH_IO", error instanceof Error ? error.message : String(error)) })

type Profile = "v1" | "v2"
const runtimeCall = (root: string, args: readonly string[], seconds: number, profile: Profile = "v1") => capture({
  command: "uv", args: ["run", "--locked", "--no-sync", "--project", externalRoots(root).hswm,
    "hswm-live", "--program", join(root, `config/hswm-research.${profile}.json`),
    "--state", join(root, `.ice/hswm-research/runtime${profile === "v1" ? "" : ".v2"}.sqlite3`), "--workspace", root, ...args],
  cwd: root, captureLimitCharacters: 4_194_304
}, seconds)

const emitRuntime = (result: { exitCode: number; stdout: string; stderr: string }, json: boolean) => Effect.gen(function* () {
  if (result.stdout.trim()) {
    yield* Console.log(json ? result.stdout.trim() : JSON.stringify(JSON.parse(result.stdout), null, 2))
  }
  if (result.stderr.trim()) yield* Console.error(result.stderr.trim())
  if (result.exitCode !== 0) process.exitCode = result.exitCode
})

export const researchEpisodeCommand = (action: "run" | "plan", options: ResearchOptions, json: boolean) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const invocation = yield* Effect.try({ try: () => researchInvocation(options),
    catch: (error) => iceError("HSWM_RESEARCH_INPUT", error instanceof Error ? error.message : String(error), 2) })
  const semantic = options.stateFile ? yield* loadResearchStateFile(options.stateFile) : undefined
  if (semantic && (semantic.state.target !== options.target || options.tier !== "supporting")) {
    return yield* Effect.fail(iceError("RESEARCH_STATE_SCOPE_MISMATCH", "Research state must match the exact target and supporting tier", 2))
  }
  const profile: Profile = semantic ? "v2" : "v1"
  const context = semantic ? { ...invocation.context, ...semantic.view.context } : invocation.context
  const task = { ...invocation.task, ...(semantic ? { research_state: { path: semantic.path, sha256: semantic.sha256 } } : {}) }
  const episode = randomUUID()
  const directory = join(root, ".ice/hswm-research/episodes", episode)
  if (action === "run") yield* io(() => fs.mkdir(directory, { recursive: true }))
  if (options.tier === "core") {
    const planner = yield* capture({ command: "./ice", args: ["agent", "plan", options.question, "--graph", "cpt", "--json"], cwd: root }, 90)
    if (action === "run") yield* io(() => fs.writeFile(join(directory, "core-planner.json"), planner.stdout, { flag: "wx" }))
    if (planner.exitCode !== 0) return yield* Effect.fail(iceError("HSWM_RESEARCH_CORE_PLAN_FAILED", planner.stderr || planner.stdout))
    // Candidate routing is a prerequisite for core work; it remains a proposal,
    // not evidence or an authorization to promote scientific conclusions.
    const planned: unknown = yield* Effect.try({ try: () => JSON.parse(planner.stdout), catch: () => iceError("HSWM_RESEARCH_CORE_PLAN_INVALID", "Planner did not emit JSON") })
    const routing = asJsonObject(asJsonObject(planned)?.objective_routing)
    if (routing?.classification !== "CURRENT_BLOCKER_CANDIDATE") return yield* Effect.fail(iceError("HSWM_RESEARCH_CORE_REFRAME", "Planner did not return CURRENT_BLOCKER_CANDIDATE; reformulate the bounded question or select --tier supporting"))
  }
  const args = [action, "--context", JSON.stringify(context), "--budget", String(options.budget)]
  if (action === "plan" && semantic) args.push("--cell", "semantic-review")
  if (action === "run") args.push("--task", JSON.stringify(task), "--episode", episode, "--max-calls", "4")
  if (action === "run") {
    const interfaces = yield* researchRuntimeStatus(root)
    if (!interfaces.available) return yield* Effect.fail(iceError("HSWM_RESEARCH_RUNTIME_MISSING", interfaces.missing.join("\n")))
    const program = yield* io(() => fs.readFile(join(root, `config/hswm-research.${profile}.json`)))
    yield* io(() => fs.writeFile(join(directory, "invocation.json"), JSON.stringify({ schema: "ice-hswm-episode-invocation/v1", episode,
      context, task, profile, research_state: semantic ?? null, budget_seconds: options.budget, max_calls: 4, program_sha256: createHash("sha256").update(program).digest("hex"),
      runtime_interfaces: interfaces, llm_port: "installed Codex CLI; model/auth inherited; reviewed feedback only" }, null, 2) + "\n", { flag: "wx" }))
  }
  const result = yield* runtimeCall(root, args, options.budget + 30, profile)
  if (action === "run") yield* io(() => fs.writeFile(join(directory, "runtime.json"), JSON.stringify(result, null, 2) + "\n", { flag: "wx" }))
  yield* emitRuntime(result, json)
})

export const researchStateCommand = (action: "status" | "graph", json: boolean, profile: Profile = "v1") => Effect.gen(function* () {
  const { root } = yield* Workspace
  yield* emitRuntime(yield* runtimeCall(root, [action], 30, profile), json)
})

export const researchFeedbackCommand = (episode: string, useful: "true" | "false", source: string, json: boolean) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const reviewSource = `research-usefulness-review: ${source}`
  if (!/^[A-Za-z0-9_-]{1,96}$/.test(episode) || !source.trim() || reviewSource.length > 256) return yield* Effect.fail(iceError("HSWM_RESEARCH_FEEDBACK_INPUT", "Provide a valid episode and a review rationale of at most 228 characters", 2))
  const invocation = yield* io(async () => JSON.parse(await fs.readFile(join(root, ".ice/hswm-research/episodes", episode, "invocation.json"), "utf8")) as unknown)
  const profile: Profile = asJsonObject(invocation)?.profile === "v2" ? "v2" : "v1"
  yield* emitRuntime(yield* runtimeCall(root, ["feedback", "--episode", episode, "--success", useful,
    "--source", reviewSource], 30, profile), json)
})

export const researchIntuitionCommand = (path: string, without: readonly string[], json: boolean) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const loaded = yield* loadResearchStateFile(path, without)
  const context = { mode: "investigate", graph: loaded.state.target.split("::")[0], tier: "supporting", ...loaded.view.context }
  const result = yield* runtimeCall(root, ["plan", "--context", JSON.stringify(context), "--cell", "semantic-review", "--budget", "600"], 30, "v2")
  if (result.exitCode !== 0) return yield* Effect.fail(iceError("RESEARCH_INTUITION_PLAN_FAILED", result.stderr || result.stdout))
  const plan = yield* io(async () => asJsonObject(JSON.parse(result.stdout)))
  const response = { schema: "ice-hswm-research-intuition/v1", ...loaded, hswm_plan: plan,
    scope: "Reviewed source-bound research state; candidate relations and hypothetical removals are not scientific evidence" }
  const selected = asJsonObject(plan?.selected)
  yield* Console.log(json ? JSON.stringify(response, null, 2) : `${renderResearchState(loaded.state, loaded.view, root)}\n## HSWM이 선택한 검토\n\n${String(selected?.uid ?? "WITHHOLD")}\n\n선택 입력: ${JSON.stringify(context)}\n\n현재 v2 조건은 경로별로 서로 겹치지 않는다. 이번 선택은 선언한 상태 조건에 따른 것이며, 조회는 셀을 실행하거나 학습하지 않는다.\n`)
})
