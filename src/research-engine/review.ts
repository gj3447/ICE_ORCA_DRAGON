/**
 * Immutable review record for one HSWM research-stage artifact.
 *
 * This records usefulness or process quality only.  It is neither a scientific
 * truth verdict nor an instruction to update an ontology or a native learner.
 */
import type { ResearchStage } from "./cell.ts"

export type ResearchReviewVerdict = "useful" | "not_useful" | "inconclusive"
export type ResearchReviewDimension = "research_usefulness" | "process_quality"
export type ResearchReviewAuthor = "agent" | "user"

export interface ResearchReview {
  readonly schema: "ice-research-stage-review/v1"
  readonly id: string
  readonly author: ResearchReviewAuthor
  /** Named reviewer, for example `codex`; it does not change author kind. */
  readonly source: string
  readonly target: {
    readonly episode: string
    readonly stage: ResearchStage
    readonly output_sha256: string
    readonly trajectory: string
  }
  readonly verdict: ResearchReviewVerdict
  readonly dimension: ResearchReviewDimension
  readonly rationale: string
  readonly non_claim: string
}

const stages: readonly ResearchStage[] = ["references", "formulate", "adversary", "synthesize", "compute", "domain", "comparison", "obstruction", "connections"]
const idPattern = /^[A-Za-z][A-Za-z0-9_.:-]{0,95}$/
const episodePattern = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|[A-Za-z0-9][A-Za-z0-9_-]{0,95})$/i
const sha256Pattern = /^[a-f0-9]{64}$/
const trajectoryPattern = /^trajectory:[A-Za-z0-9_-]{1,96}:[0-9]{1,6}$/

const object = (value: unknown, label: string): Record<string, unknown> => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) throw new Error(`${label} must be an object`)
  return value as Record<string, unknown>
}

const exact = (value: Record<string, unknown>, keys: readonly string[], label: string): void => {
  const actual = Object.keys(value)
  if (actual.length !== keys.length || actual.some((key) => !keys.includes(key))) throw new Error(`${label} has unknown or missing fields`)
}

const text = (value: unknown, label: string, maximum: number): string => {
  if (typeof value !== "string" || !value.trim() || value.length > maximum) throw new Error(`${label} must be non-empty and at most ${maximum} characters`)
  return value
}

/** Parse untrusted JSON without inferring that a reviewed artifact is true. */
export const parseResearchReview = (value: unknown): ResearchReview => {
  const root = object(value, "review")
  exact(root, ["schema", "id", "author", "source", "target", "verdict", "dimension", "rationale", "non_claim"], "review")
  if (root.schema !== "ice-research-stage-review/v1") throw new Error("review schema must be ice-research-stage-review/v1")
  const id = text(root.id, "review.id", 96)
  if (!idPattern.test(id)) throw new Error("review.id must be a safe identifier")
  if (root.author !== "agent" && root.author !== "user") throw new Error("review.author must be agent or user")
  const target = object(root.target, "review.target")
  exact(target, ["episode", "stage", "output_sha256", "trajectory"], "review.target")
  const episode = text(target.episode, "review.target.episode", 96)
  if (!episodePattern.test(episode)) throw new Error("review.target.episode must be a UUID or safe slug")
  const stage = target.stage
  if (typeof stage !== "string" || !stages.includes(stage as ResearchStage)) throw new Error("review.target.stage must be an actual research stage")
  const outputSha = text(target.output_sha256, "review.target.output_sha256", 64)
  if (!sha256Pattern.test(outputSha)) throw new Error("review.target.output_sha256 must be lower-case SHA-256")
  const trajectory = text(target.trajectory, "review.target.trajectory", 160)
  if (!trajectoryPattern.test(trajectory)) throw new Error("review.target.trajectory must be an actual HSWM trajectory id")
  if (trajectory.split(":")[1] !== episode) throw new Error("review.target.trajectory must belong to review.target.episode")
  if (root.verdict !== "useful" && root.verdict !== "not_useful" && root.verdict !== "inconclusive") throw new Error("review.verdict is invalid")
  if (root.dimension !== "research_usefulness" && root.dimension !== "process_quality") throw new Error("review.dimension is invalid")
  return { schema: "ice-research-stage-review/v1", id, author: root.author, source: text(root.source, "review.source", 120),
    target: { episode, stage: stage as ResearchStage, output_sha256: outputSha, trajectory }, verdict: root.verdict,
    dimension: root.dimension, rationale: text(root.rationale, "review.rationale", 2_000), non_claim: text(root.non_claim, "review.non_claim", 2_000) }
}
