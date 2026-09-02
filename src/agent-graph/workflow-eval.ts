import type { GraphRagIndex } from "../graphrag/core.ts"
import { searchGraphRag } from "../graphrag/core.ts"
import { planResearchAgentWorkflow } from "./core.ts"
import {
  applyResearchAgentReview,
  auditResearchAgentRun,
  createResearchAgentRun,
  type ResearchAgentRevisionPin,
  type ResearchAgentRunStatus
} from "./durable.ts"
import { evaluateResearchAgentRouting } from "./eval.ts"
import type { ToeObjectiveRouting } from "./toe-route.ts"

interface WorkflowSuiteCase {
  readonly id: string
  readonly question: string
  readonly expectedClassification: ToeObjectiveRouting["classification"]
  readonly expectedStatus: ResearchAgentRunStatus
  readonly approveCurrentRoute: boolean
}

const suite: ReadonlyArray<WorkflowSuiteCase> = [
  {
    id: "current-blocker-reviewed-to-closed",
    question: "Gate 1 original joint cycle and signed global intersection vector",
    expectedClassification: "CURRENT_BLOCKER_CANDIDATE",
    expectedStatus: "CLOSED",
    approveCurrentRoute: true
  },
  {
    id: "downstream-gate-stops",
    question: "Gate 4 common domain and anomaly free constraint closure",
    expectedClassification: "DOWNSTREAM_BLOCKED",
    expectedStatus: "STOPPED",
    approveCurrentRoute: false
  },
  {
    id: "supporting-lane-stops",
    question: "P4 raw-C fixed box nonreal endpoint certificate singular Weyl",
    expectedClassification: "SUPPORTING_ONLY",
    expectedStatus: "STOPPED",
    approveCurrentRoute: false
  },
  {
    id: "classical-hda-and-quantum-bfv-supporting-stop",
    question: "P2 P3 closed S3 HDA Jacobi closure before P5 quantum BFV common-core anomaly",
    expectedClassification: "SUPPORTING_ONLY",
    expectedStatus: "STOPPED",
    approveCurrentRoute: false
  },
  {
    id: "physical-product-and-likelihood-supporting-stop",
    question: "P7 physical clock normalized state reheating empirical likelihood discriminator",
    expectedClassification: "SUPPORTING_ONLY",
    expectedStatus: "STOPPED",
    approveCurrentRoute: false
  },
  {
    id: "unanchored-question-stops",
    question: "zzzxxyy unregistered graph object",
    expectedClassification: "INSUFFICIENT_ROUTE_EVIDENCE",
    expectedStatus: "STOPPED",
    approveCurrentRoute: false
  }
]

export interface ResearchAgentWorkflowEvaluationReport {
  readonly schema: "ice-research-agent-workflow-evaluation/v1"
  readonly suite: {
    readonly id: "canonical-cpt-human-handoff"
    readonly version: "1.1.0"
    readonly case_count: number
  }
  readonly passed: boolean
  readonly cases: ReadonlyArray<{
    readonly id: string
    readonly passed: boolean
    readonly expected_classification: ToeObjectiveRouting["classification"]
    readonly actual_classification: ToeObjectiveRouting["classification"] | null
    readonly expected_status: ResearchAgentRunStatus
    readonly actual_status: ResearchAgentRunStatus | null
    readonly routing_checks_passed: boolean
    readonly durable_audit_passed: boolean
    readonly error: string | null
  }>
  readonly guidance: ReadonlyArray<string>
}

/** Fixed, versioned evaluation of routing, handoff, and terminal boundaries. */
export const evaluateResearchAgentWorkflowSuite = (
  index: GraphRagIndex,
  revisionPin: ResearchAgentRevisionPin
): ResearchAgentWorkflowEvaluationReport => {
  const cases = suite.map((testCase, caseIndex) => {
    try {
      const retrieval = searchGraphRag(index, testCase.question, {
        graph: "cpt",
        limit: 12,
        depth: 1
      })
      const plan = planResearchAgentWorkflow(testCase.question, retrieval)
      const routing = evaluateResearchAgentRouting(plan)
      let run = createResearchAgentRun({
        run_id: `eval-${String(caseIndex + 1).padStart(2, "0")}-${testCase.id}`,
        at: "2026-09-02T00:00:00.000Z",
        plan,
        revision_pin: revisionPin
      })
      if (testCase.approveCurrentRoute) {
        run = applyResearchAgentReview(run, {
          at: "2026-09-02T00:01:00.000Z",
          stage: "ROUTE",
          decision: "APPROVE",
          rationale: "Evaluation fixture approves the specifically anchored route.",
          observed_revision_pin: revisionPin
        })
        run = applyResearchAgentReview(run, {
          at: "2026-09-02T00:02:00.000Z",
          stage: "EVIDENCE",
          decision: "APPROVE",
          rationale: "Evaluation fixture records the evidence handoff.",
          observed_revision_pin: revisionPin
        })
        run = applyResearchAgentReview(run, {
          at: "2026-09-02T00:03:00.000Z",
          stage: "DESIGN",
          decision: "APPROVE",
          rationale: "Evaluation fixture closes design review without execution authority.",
          observed_revision_pin: revisionPin
        })
      } else {
        run = applyResearchAgentReview(run, {
          at: "2026-09-02T00:01:00.000Z",
          stage: "ROUTE",
          decision: "STOP_OR_REFRAME",
          rationale: "Evaluation fixture stops a non-current or unanchored route.",
          observed_revision_pin: revisionPin
        })
      }
      const durable = auditResearchAgentRun(run, revisionPin)
      const passed =
        plan.objective_routing.classification === testCase.expectedClassification &&
        run.status === testCase.expectedStatus &&
        routing.passed &&
        durable.passed &&
        run.contract.execution_authorization === "NOT_GRANTED"
      return {
        id: testCase.id,
        passed,
        expected_classification: testCase.expectedClassification,
        actual_classification: plan.objective_routing.classification,
        expected_status: testCase.expectedStatus,
        actual_status: run.status,
        routing_checks_passed: routing.passed,
        durable_audit_passed: durable.passed,
        error: null
      }
    } catch (error) {
      return {
        id: testCase.id,
        passed: false,
        expected_classification: testCase.expectedClassification,
        actual_classification: null,
        expected_status: testCase.expectedStatus,
        actual_status: null,
        routing_checks_passed: false,
        durable_audit_passed: false,
        error: error instanceof Error ? error.message : String(error)
      }
    }
  })
  return {
    schema: "ice-research-agent-workflow-evaluation/v1",
    suite: {
      id: "canonical-cpt-human-handoff",
      version: "1.1.0",
      case_count: cases.length
    },
    passed: cases.every(({ passed }) => passed),
    cases,
    guidance: [
      "This suite evaluates repository routing, human handoffs, persistence invariants, and non-authorization only.",
      "It does not evaluate model reasoning, scientific truth, citation entailment, or calculation correctness."
    ]
  }
}
