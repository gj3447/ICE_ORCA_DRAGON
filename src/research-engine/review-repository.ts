import { Console, Effect } from "effect"
import { createHash } from "node:crypto"
import { promises as fs } from "node:fs"
import { join } from "node:path"
import { iceError } from "../errors.ts"
import { readLocalReference } from "../research-context/commands.ts"
import { asJsonObject } from "../research-context/core.ts"
import { Workspace } from "../workspace.ts"
import { parseResearchReview } from "./review.ts"

export const researchReviewCommand = (path: string, json: boolean) => Effect.gen(function* () {
  const { root } = yield* Workspace
  const receipt = yield* Effect.tryPromise({ try: async () => {
    const review = parseResearchReview(JSON.parse((await readLocalReference(root, path)).toString("utf8")))
    const base = `.ice/hswm-research/episodes/${review.target.episode}/`
    const process = asJsonObject(JSON.parse((await readLocalReference(root, `${base}runtime.json`)).toString("utf8")))
    const runtime = typeof process?.stdout === "string" ? asJsonObject(JSON.parse(process.stdout)) : undefined
    if (runtime?.episode_id !== review.target.episode || !Array.isArray(runtime.visits)) throw new Error("Review must refer to an observed episode")
    const visits = runtime.visits.map(asJsonObject).filter((visit) => visit?.cell === review.target.stage)
    const visit = visits[0]
    if (visits.length !== 1 || visit?.trajectory !== review.target.trajectory || !["SUCCEEDED", "FAILED", "UNKNOWN", "WITHHOLD"].includes(String(visit.status))) {
      throw new Error("Review must target the unique completed stage trajectory from this episode")
    }
    const stagePath = `${base}${review.target.stage}.json`
    const stageBytes = await readLocalReference(root, stagePath)
    const stage = asJsonObject(JSON.parse(stageBytes.toString("utf8")))
    if (stage?.stage !== review.target.stage) throw new Error("Stage artifact does not match the review")
    const outputPath = typeof stage.output_path === "string" ? stage.output_path : stagePath
    if (!outputPath.startsWith(base)) throw new Error("Stage output belongs to a different episode")
    const bytes = outputPath === stagePath ? stageBytes : await readLocalReference(root, outputPath)
    const sha256 = createHash("sha256").update(bytes).digest("hex")
    if (sha256 !== review.target.output_sha256) throw new Error("Reviewed stage output hash differs from actual bytes")
    const record = { schema: "ice-research-stage-review-receipt/v1", review, artifact: { path: outputPath, sha256 },
      observed_stage_status: visit.status, delivery: "LOCAL_STAGE_REVIEW_RECORDED", learning: "NOT_SUBMITTED",
      scope: "Explicit stage review; native episode feedback currently targets only the root relation. This record does not assign causal credit or scientific truth." }
    const directory = join(root, ".ice/hswm-research/reviews")
    await fs.mkdir(directory, { recursive: true })
    if (await fs.realpath(directory) !== join(await fs.realpath(root), ".ice/hswm-research/reviews")) throw new Error("Review directory must not redirect through a symlink")
    const destination = join(directory, `${review.id}.json`)
    const serialized = JSON.stringify(record, null, 2) + "\n"
    try { await fs.writeFile(destination, serialized, { flag: "wx" }) }
    catch (error) {
      if (!(error instanceof Error) || !("code" in error) || error.code !== "EEXIST") throw error
      if (await fs.readFile(destination, "utf8") !== serialized) throw new Error("Conflicting review ID; existing review is immutable")
    }
    return { ...record, path: `.ice/hswm-research/reviews/${review.id}.json` }
  }, catch: (error) => iceError("RESEARCH_REVIEW_INVALID", String(error), 2) })
  yield* Console.log(json ? JSON.stringify(receipt, null, 2) : `Recorded ${receipt.review.author}(${receipt.review.source}) stage review: ${receipt.path}\n${receipt.delivery}; ${receipt.learning}.`)
})
