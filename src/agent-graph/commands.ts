import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { graphRagIndexData } from "../graphrag/commands.ts"
import { searchGraphRag } from "../graphrag/core.ts"
import { planResearchAgentWorkflow } from "./core.ts"
import { assertToeNavigationProfile } from "./toe-route.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

export const researchAgentPlanData = (
  question: string,
  graph: string,
  limit: number,
  depth: number
) =>
  graphRagIndexData.pipe(
    Effect.flatMap((index) =>
      Effect.try({
        try: () => {
          assertToeNavigationProfile(index.units)
          const retrieval = searchGraphRag(index, question, { graph, limit, depth })
          return planResearchAgentWorkflow(question, retrieval)
        },
        catch: (error) =>
          iceError(
            "RESEARCH_AGENT_PLAN_FAILED",
            error instanceof Error ? error.message : String(error),
            2
          )
      })
    )
  )

export const researchAgentPlanCommand = (
  question: string,
  graph: string,
  limit: number,
  depth: number,
  json: boolean
) =>
  researchAgentPlanData(question, graph, limit, depth).pipe(
    Effect.tap((plan) =>
      json
        ? printJson(plan)
        : Console.log(
            [
              `research agent checkpoint: ${plan.checkpoint.id}`,
              `state: ${plan.checkpoint.state}`,
              `objective: ${plan.objective_routing.objective.status}`,
              `route: ${plan.objective_routing.classification}`,
              `selected lane: ${plan.objective_routing.selected_lane_id ?? "NONE"}`,
              `decision: ${plan.objective_routing.decision}`,
              `retrieved records: ${plan.checkpoint.graph_retrieval_ids.length}`,
              "execution/core-progress: NOT AUTHORIZED; human route review is required"
            ].join("\n")
          )
    )
  )
