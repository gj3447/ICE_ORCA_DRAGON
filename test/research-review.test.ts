import { expect, it } from "vitest"
import { createHash } from "node:crypto"
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { Effect } from "effect"
import { parseResearchReview } from "../src/research-engine/review.ts"
import { researchReviewCommand } from "../src/research-engine/review-repository.ts"
import { Workspace, workspaceFromRoot } from "../src/workspace.ts"

const raw = {
  schema: "ice-research-stage-review/v1", id: "review-domain-1", author: "agent", source: "codex",
  target: { episode: "c8247949-b803-4620-9c2e-b235d86330d3", stage: "domain", output_sha256: "a".repeat(64), trajectory: "trajectory:c8247949-b803-4620-9c2e-b235d86330d3:3" },
  verdict: "useful", dimension: "research_usefulness",
  rationale: "The artifact names a bounded conditional candidate and its falsifier.",
  non_claim: "This review does not make the candidate physically true or update native feedback."
} as const

it("binds a review to one stage artifact and trajectory", () => {
  const review = parseResearchReview(raw)
  expect(review.author).toBe("agent")
  expect(review.target).toMatchObject({ stage: "domain", trajectory: "trajectory:c8247949-b803-4620-9c2e-b235d86330d3:3" })
  expect(review.verdict).toBe("useful")
})

it("rejects invented stages, unsafe artifact bindings, and physics verdicts", () => {
  expect(() => parseResearchReview({ ...raw, target: { ...raw.target, stage: "physics" } })).toThrow("actual research stage")
  expect(() => parseResearchReview({ ...raw, target: { ...raw.target, output_sha256: "bad" } })).toThrow("SHA-256")
  expect(() => parseResearchReview({ ...raw, target: { ...raw.target, trajectory: "relation:declare-domain" } })).toThrow("trajectory")
  expect(() => parseResearchReview({ ...raw, target: { ...raw.target, trajectory: "trajectory:other-episode:3" } })).toThrow("belong")
  expect(() => parseResearchReview({ ...raw, verdict: "true" })).toThrow("verdict")
})

it("requires explicit reviewer kind, rationale, non-claim, and strict keys", () => {
  expect(() => parseResearchReview({ ...raw, author: "model" })).toThrow("author")
  expect(() => parseResearchReview({ ...raw, rationale: "" })).toThrow("rationale")
  expect(() => parseResearchReview({ ...raw, extra: true })).toThrow("unknown or missing")
  expect(parseResearchReview({ ...raw, author: "user", source: "user" }).author).toBe("user")
})

const sha = (value: string): string => createHash("sha256").update(value).digest("hex")
const episode = "c8247949-b803-4620-9c2e-b235d86330d3"
const trajectory = `trajectory:${episode}:3`

const stageFixture = async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-stage-review-"))
  const base = join(root, ".ice/hswm-research/episodes", episode)
  const output = '{"proposal":"bounded candidate"}\n'
  await mkdir(base, { recursive: true })
  await writeFile(join(base, "runtime.json"), JSON.stringify({ stdout: JSON.stringify({ episode_id: episode,
    visits: [{ cell: "domain", trajectory, status: "SUCCEEDED" }] }) }))
  await writeFile(join(base, "domain.output.json"), output)
  await writeFile(join(base, "domain.json"), JSON.stringify({ stage: "domain", output_path: `.ice/hswm-research/episodes/${episode}/domain.output.json` }))
  return { root, outputPath: join(base, "domain.output.json"), output }
}

const writeReview = async (root: string, id: string, hash: string, rationale: string = raw.rationale): Promise<string> => {
  const path = "review-input.json"
  await writeFile(join(root, path), JSON.stringify({ ...raw, id, rationale, target: { ...raw.target, output_sha256: hash, trajectory } }))
  return path
}

const record = (root: string, path: string) => Effect.runPromise(
  researchReviewCommand(path, true).pipe(Effect.provideService(Workspace, workspaceFromRoot(root)))
)

it("binds an immutable review to the observed artifact and permits the exact replay", async () => {
  const fixture = await stageFixture()
  try {
    const path = await writeReview(fixture.root, "review-bound-1", sha(fixture.output))
    await record(fixture.root, path)
    await record(fixture.root, path)
    const receipt = JSON.parse(await readFile(join(fixture.root, ".ice/hswm-research/reviews/review-bound-1.json"), "utf8"))
    expect(receipt.artifact).toEqual({ path: `.ice/hswm-research/episodes/${episode}/domain.output.json`, sha256: sha(fixture.output) })
    expect(receipt.learning).toBe("NOT_SUBMITTED")
  } finally { await rm(fixture.root, { recursive: true, force: true }) }
})

it("rejects changed stage bytes and a different review under the same immutable id", async () => {
  const fixture = await stageFixture()
  try {
    const path = await writeReview(fixture.root, "review-bound-2", sha(fixture.output))
    await writeFile(fixture.outputPath, '{"proposal":"changed"}\n')
    await expect(record(fixture.root, path)).rejects.toThrow("Reviewed stage output hash")
    await writeFile(fixture.outputPath, fixture.output)
    await record(fixture.root, path)
    const conflict = await writeReview(fixture.root, "review-bound-2", sha(fixture.output), "A different immutable rationale.")
    await expect(record(fixture.root, conflict)).rejects.toThrow("Conflicting review ID")
  } finally { await rm(fixture.root, { recursive: true, force: true }) }
})
