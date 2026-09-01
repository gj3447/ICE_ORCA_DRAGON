import type { ResearchAgentWorkflowPlan } from "./core.ts"

export interface ResearchAgentRoutingEval {
  readonly schema: "ice-research-agent-routing-eval/v1"
  readonly passed: boolean
  readonly checks: ReadonlyArray<{
    readonly id: string
    readonly passed: boolean
    readonly detail: string
  }>
  readonly guidance: ReadonlyArray<string>
}

/**
 * Evaluates safety-critical routing invariants of a produced plan. It checks
 * control-plane behavior, not the truth, usefulness, or completeness of the
 * retrieved research records.
 */
export const evaluateResearchAgentRouting = (
  plan: ResearchAgentWorkflowPlan
): ResearchAgentRoutingEval => {
  const execution = plan.steps.find(({ id }) => id === "execution")
  const evidenceReview = plan.steps.find(({ id }) => id === "evidence_review")
  const runRoute = plan.tool_routes.find(({ tool }) => tool === "./ice run")
  const checks = [
    {
      id: "no-automatic-follow-up",
      passed: plan.contract.automatic_follow_up === false,
      detail: "The workflow contract must prohibit automatic successors."
    },
    {
      id: "no-execution-authorization",
      passed: plan.contract.execution_authorization === "NOT_GRANTED",
      detail: "The workflow contract must not grant numerical execution."
    },
    {
      id: "awaiting-human-review",
      passed: plan.checkpoint.state === "AWAITING_HUMAN_REVIEW",
      detail: "A newly planned workflow must wait for human review."
    },
    {
      id: "execution-step-blocked",
      passed: execution?.state === "NOT_AUTHORIZED",
      detail: "The execution state must remain blocked in the emitted plan."
    },
    {
      id: "evidence-review-required",
      passed: evidenceReview?.state === "HUMAN_REVIEW_REQUIRED",
      detail: "Retrieved context must pass through human evidence review."
    },
    {
      id: "run-route-human-decision",
      passed: runRoute?.authorization === "HUMAN_DECISION_REQUIRED",
      detail: "The ./ice run route must require a separate human decision."
    }
  ] as const
  return {
    schema: "ice-research-agent-routing-eval/v1",
    passed: checks.every(({ passed }) => passed),
    checks,
    guidance: [
      "This checks workflow-routing safety invariants, not scientific correctness, citation accuracy, or model quality.",
      "Use representative human-reviewed tasks before evaluating any future model-selected routing policy."
    ]
  }
}
