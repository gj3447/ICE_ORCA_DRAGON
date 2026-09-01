import { createHash } from "node:crypto"
import type { GraphRagSearchResult } from "../graphrag/core.ts"

export const researchAgentGraphContract = {
  schema: "ice-research-agent-graph/v1",
  mode: "DURABLE_HUMAN_APPROVED_READ_ONLY",
  automatic_follow_up: false,
  execution_authorization: "NOT_GRANTED",
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
  readonly schema: "ice-research-agent-workflow-plan/v1"
  readonly contract: typeof researchAgentGraphContract
  readonly checkpoint: {
    readonly id: string
    readonly state: "AWAITING_HUMAN_REVIEW"
    readonly question: string
    readonly graph_retrieval_ids: ReadonlyArray<string>
  }
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

const workflowId = (question: string, retrieved: ReadonlyArray<string>): string =>
  `research-agent:${createHash("sha256")
    .update(`${question}\n${retrieved.join("\n")}`)
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
  return {
    schema: "ice-research-agent-workflow-plan/v1",
    contract: researchAgentGraphContract,
    checkpoint: {
      id: workflowId(normalizedQuestion, retrieved),
      state: "AWAITING_HUMAN_REVIEW",
      question: normalizedQuestion,
      graph_retrieval_ids: retrieved
    },
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
        next: ["literature_neighborhood", "evidence_review"]
      },
      {
        id: "literature_neighborhood",
        state: "AVAILABLE",
        purpose: "Optionally inspect a bounded OpenAlex citation neighborhood for primary-source discovery.",
        inputs: ["human-selected paper identifier"],
        outputs: ["time-stamped discovery metadata"],
        next: ["evidence_review"]
      },
      {
        id: "evidence_review",
        state: "HUMAN_REVIEW_REQUIRED",
        purpose: "Separate retrieved records, source authority, numerical limits, and any proposed interpretation.",
        inputs: ["graph context", "optional primary-source reading"],
        outputs: ["one scoped question or an explicit stop"],
        next: ["calculation_design"]
      },
      {
        id: "calculation_design",
        state: "HUMAN_REVIEW_REQUIRED",
        purpose: "If justified, select one principal failure mode and proportionate controls under lean research rules.",
        inputs: ["human-reviewed scope"],
        outputs: ["clean committed runner proposal or no-run decision"],
        next: ["execution"]
      },
      {
        id: "execution",
        state: "NOT_AUTHORIZED",
        purpose: "A separate human decision may invoke ./ice run for a clean committed bounded runner.",
        inputs: ["explicit user authorization", "clean committed runner"],
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
        condition: "A question needs repository-local context.",
        authorization: "READ_ONLY"
      },
      {
        tool: "ice_literature_search",
        condition: "A human decides that external source discovery is useful.",
        authorization: "READ_ONLY"
      },
      {
        tool: "ice_literature_neighbors",
        condition: "A human selects a paper whose citation neighborhood needs review.",
        authorization: "READ_ONLY"
      },
      {
        tool: "./ice run",
        condition: "Only after separate human review and repository execution rules are met.",
        authorization: "HUMAN_DECISION_REQUIRED"
      }
    ],
    guidance: [
      "The checkpoint is durable JSON that an agent host may store and resume, but this repository does not persist it automatically.",
      "The routing graph is not a research contract, an automatic successor generator, or an execution permit.",
      "Treat retrieved text and external literature metadata as potentially incomplete; preserve primary-source and raw-result review."
    ]
  }
}
