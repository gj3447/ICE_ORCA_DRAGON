import { createHash } from "node:crypto"
import type { GraphRagSearchResult } from "../graphrag/core.ts"
import { routeToeObjective, toeNavigationProfile, type ToeObjectiveRouting } from "./toe-route.ts"

export const researchAgentGraphContract = {
  schema: "ice-research-agent-graph/v2",
  mode: "DURABLE_HUMAN_APPROVED_READ_ONLY",
  automatic_follow_up: false,
  execution_authorization: "NOT_GRANTED",
  core_progress_authorization: "NOT_GRANTED",
  persistence: "CALLER_MAY_STORE_SERIALIZED_CHECKPOINT"
} as const

export type ResearchWorkflowStepState =
  | "COMPLETED"
  | "AVAILABLE"
  | "HUMAN_REVIEW_REQUIRED"
  | "NOT_AUTHORIZED"

export interface ResearchWorkflowStep {
  readonly id:
    | "intake"
    | "graph_retrieval"
    | "objective_route_review"
    | "literature_neighborhood"
    | "evidence_review"
    | "calculation_design"
    | "execution"
  readonly state: ResearchWorkflowStepState
  readonly purpose: string
  readonly inputs: ReadonlyArray<string>
  readonly outputs: ReadonlyArray<string>
  readonly next: ReadonlyArray<string>
}

export interface ResearchAgentWorkflowPlan {
  readonly schema: "ice-research-agent-workflow-plan/v2"
  readonly contract: typeof researchAgentGraphContract
  readonly checkpoint: {
    readonly id: string
    readonly state: "AWAITING_HUMAN_REVIEW"
    readonly question: string
    readonly graph_retrieval_ids: ReadonlyArray<string>
  }
  readonly objective_routing: ToeObjectiveRouting
  readonly steps: ReadonlyArray<ResearchWorkflowStep>
  readonly retrieval: Pick<
    GraphRagSearchResult,
    "query" | "graph" | "depth" | "hits" | "communities" | "guidance"
  >
  readonly tool_routes: ReadonlyArray<{
    readonly tool: string
    readonly condition: string
    readonly authorization: "READ_ONLY" | "HUMAN_DECISION_REQUIRED"
  }>
  readonly guidance: ReadonlyArray<string>
}

const workflowId = (
  question: string,
  graph: string,
  retrieved: ReadonlyArray<string>
): string =>
  `research-agent:${createHash("sha256")
    .update(
      `${toeNavigationProfile.version}\n${graph}\n${question}\n${retrieved.join("\n")}`
    )
    .digest("hex")
    .slice(0, 20)}`

/**
 * Produces a serializable, durable state-machine checkpoint for an agent host.
 * It deliberately leaves source expansion and all calculation work to human
 * review instead of calling a model or a numerical runner by itself.
 */
export const planResearchAgentWorkflow = (
  question: string,
  retrieval: GraphRagSearchResult
): ResearchAgentWorkflowPlan => {
  const normalizedQuestion = question.trim()
  if (normalizedQuestion.length === 0 || normalizedQuestion.length > 500) {
    throw new Error("question must contain from 1 through 500 characters")
  }
  const retrieved = retrieval.hits.map(({ unit }) => unit.id)
  const objectiveRouting = routeToeObjective(normalizedQuestion, retrieval)
  const currentBlockerCandidate =
    objectiveRouting.classification === "CURRENT_BLOCKER_CANDIDATE"
  return {
    schema: "ice-research-agent-workflow-plan/v2",
    contract: researchAgentGraphContract,
    checkpoint: {
      id: workflowId(normalizedQuestion, retrieval.graph, retrieved),
      state: "AWAITING_HUMAN_REVIEW",
      question: normalizedQuestion,
      graph_retrieval_ids: retrieved
    },
    objective_routing: objectiveRouting,
    steps: [
      {
        id: "intake",
        state: "COMPLETED",
        purpose: "Freeze one user-stated question and its graph-selection input.",
        inputs: ["question"],
        outputs: ["bounded question", "non-authorization boundary"],
        next: ["graph_retrieval"]
      },
      {
        id: "graph_retrieval",
        state: "COMPLETED",
        purpose: "Retrieve canonical ontology evidence bundles with an inspectable hybrid query.",
        inputs: ["question", "ontology graph"],
        outputs: ["ranked node locators", "community context"],
        next: ["objective_route_review"]
      },
      {
        id: "objective_route_review",
        state: "HUMAN_REVIEW_REQUIRED",
        purpose: "Confirm one current-blocker typed object and its dependency path to the TOE terminal review criteria, or stop and reframe.",
        inputs: ["question", "CPT graph context", "TOE navigation policy"],
        outputs: ["human-selected G1 blocker path or explicit non-core classification"],
        next: currentBlockerCandidate
          ? ["literature_neighborhood", "evidence_review"]
          : []
      },
      {
        id: "literature_neighborhood",
        state: currentBlockerCandidate ? "AVAILABLE" : "NOT_AUTHORIZED",
        purpose: "Optionally inspect a bounded primary-source neighborhood only for the human-selected blocker.",
        inputs: ["human-selected paper identifier"],
        outputs: ["time-stamped discovery metadata"],
        next: ["evidence_review"]
      },
      {
        id: "evidence_review",
        state: currentBlockerCandidate ? "HUMAN_REVIEW_REQUIRED" : "NOT_AUTHORIZED",
        purpose: "Separate retrieved records, source authority, numerical limits, and any proposed interpretation.",
        inputs: ["graph context", "optional primary-source reading"],
        outputs: ["one scoped question or an explicit stop"],
        next: currentBlockerCandidate ? ["calculation_design"] : []
      },
      {
        id: "calculation_design",
        state: currentBlockerCandidate ? "HUMAN_REVIEW_REQUIRED" : "NOT_AUTHORIZED",
        purpose: "Only for a reviewed current blocker, prepare a core-labelled design with one missing typed object, one bounded output, one non-claim, and proportionate controls.",
        inputs: ["human-reviewed blocker path"],
        outputs: ["clean committed runner proposal or no-run decision"],
        next: ["execution"]
      },
      {
        id: "execution",
        state: "NOT_AUTHORIZED",
        purpose: "A separate human decision may invoke ./ice run only for a reviewed current-blocker calculation and a clean committed bounded runner.",
        inputs: ["explicit user authorization", "reviewed blocker path", "clean committed runner"],
        outputs: ["raw result outside this workflow planner"],
        next: []
      }
    ],
    retrieval: {
      query: retrieval.query,
      graph: retrieval.graph,
      depth: retrieval.depth,
      hits: retrieval.hits,
      communities: retrieval.communities,
      guidance: retrieval.guidance
    },
    tool_routes: [
      {
        tool: "ice_graphrag_search",
        condition: "A CPT question needs a canonical blocker and dependency-path review.",
        authorization: "READ_ONLY"
      },
      {
        tool: "ice_literature_search",
        condition: "A human selects a current blocker whose primary-source boundary needs discovery.",
        authorization: "READ_ONLY"
      },
      {
        tool: "ice_literature_neighbors",
        condition: "A human selects a current-blocker paper whose citation neighborhood needs review.",
        authorization: "READ_ONLY"
      },
      {
        tool: "./ice run",
        condition: "Only after separate human review confirms a current-blocker path and repository execution rules are met.",
        authorization: "HUMAN_DECISION_REQUIRED"
      }
    ],
    guidance: [
      "The checkpoint is durable JSON that an agent host may store and resume, but this repository does not persist it automatically.",
      "The routing graph is not a research contract, an automatic successor generator, or an execution permit.",
      "Only CURRENT_BLOCKER_CANDIDATE may proceed through this core-labelled calculation-design path; separately reviewed supporting work remains governed by the lean rules and cannot claim core progress.",
      "The TOE objective and terminal criteria are navigation policy, not evidence that a TOE exists or has been completed.",
      "Treat retrieved text and external literature metadata as potentially incomplete; preserve primary-source and raw-result review."
    ]
  }
}
