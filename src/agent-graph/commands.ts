import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { graphRagSearchData } from "../graphrag/commands.ts"
import { planResearchAgentWorkflow } from "./core.ts"

const printJson = (value: unknown): Effect.Effect<void> =>
  Console.log(JSON.stringify(value, null, 2))

export const researchAgentPlanData = (
  question: string,
  graph: string,
  limit: number,
  depth: number
) =>
  graphRagSearchData(question, { graph, limit, depth }).pipe(
    Effect.flatMap((retrieval) =>
      Effect.try({
        try: () => planResearchAgentWorkflow(question, retrieval),
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
              `retrieved records: ${plan.checkpoint.graph_retrieval_ids.length}`,
              "execution: NOT AUTHORIZED; human review is required"
            ].join("\n")
          )
    )
  )
