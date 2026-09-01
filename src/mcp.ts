import { McpServer } from "@modelcontextprotocol/server"
import { NodeContext } from "@effect/platform-node"
import { Effect, Layer } from "effect"
import * as z from "zod/v4"
import {
  graphHarnessCheckData,
  graphHarnessContextData,
  graphHarnessImpactData
} from "./harness/commands.ts"
import { researchAgentPlanData } from "./agent-graph/commands.ts"
import { graphRagSearchData, graphRagSummaryData } from "./graphrag/commands.ts"
import {
  getOpenAlexWorkNeighborhood,
  searchOpenAlexWorks
} from "./literature/openalex.ts"
import { WorkspaceLive } from "./workspace.ts"

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

const asToolResult = (value: unknown) => ({
  content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }]
})

const asToolError = (error: unknown) => ({
  content: [
    {
      type: "text" as const,
      text: JSON.stringify(
        {
          error: error instanceof Error ? error.message : String(error),
          boundary:
            "The MCP server is read-only and did not run a calculation or mutate the research graph."
        },
        null,
        2
      )
    }
  ],
  isError: true
})

const capabilities = {
  schema: "ice-research-mcp-capabilities/v1",
  mode: "READ_ONLY_GRAPH_AWARE_RESEARCH_DISCOVERY",
  tools: [
    {
      name: "ice_research_context",
      purpose: "Bounded repository-local graph context for one ontology node."
    },
    {
      name: "ice_research_impact",
      purpose: "Find graph context affected by one safe repository-relative path."
    },
    {
      name: "ice_research_check",
      purpose: "Validate graph structure, tracked hashes, and evidence snapshots."
    },
    {
      name: "ice_literature_search",
      purpose: "Search OpenAlex's public scholarly works graph (maximum 20 works)."
    },
    {
      name: "ice_literature_neighbors",
      purpose: "Read one bounded OpenAlex citation neighborhood (maximum 20 works per direction)."
    },
    {
      name: "ice_graphrag_summary",
      purpose: "Describe the deterministic local evidence GraphRAG index."
    },
    {
      name: "ice_graphrag_search",
      purpose: "Hybrid-search local ontology TextUnits with bounded graph expansion."
    },
    {
      name: "ice_research_workflow_plan",
      purpose: "Create a human-review-only durable research workflow checkpoint."
    }
  ],
  boundaries: [
    "All tools are read-only: they do not change files, run numerical kernels, or write ontology records.",
    "Graph context and literature discovery are review inputs, not independent scientific evidence.",
    "Tool results never authorize execution and never create a follow-up task automatically.",
    "Use ./ice run only for a clean committed bounded numerical runner under the repository's research rules."
  ]
} as const

/** Creates the read-only stdio MCP surface for this repository. */
export const createIceResearchMcpServer = (): McpServer => {
  const server = new McpServer({
    name: "ice-orca-dragon-research",
    version: "0.1.0"
  })

  server.registerTool(
    "ice_research_context",
    {
      title: "ICE research graph context",
      description:
        "Return bounded local evidence, scope, policy, and open-problem context for an ontology node. Read-only; does not authorize research execution.",
      inputSchema: {
        id: z.string().min(1).max(256),
        graph: z.string().min(1).max(128).default("all"),
        depth: z.number().int().min(0).max(32).default(2),
        limit: z.number().int().min(1).max(256).default(64)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ id, graph, depth, limit }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            graphHarnessContextData(id, depth, limit, graph).pipe(
              Effect.provide(AppLayer)
            )
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_research_impact",
    {
      title: "ICE research graph impact",
      description:
        "Return exact registered graph context for a safe repository-relative path. Read-only; does not write the graph.",
      inputSchema: {
        path: z.string().min(1).max(512),
        graph: z.string().min(1).max(128).default("all"),
        depth: z.number().int().min(0).max(32).default(2),
        limit: z.number().int().min(1).max(256).default(64)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ path, graph, depth, limit }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            graphHarnessImpactData(path, depth, limit, graph).pipe(
              Effect.provide(AppLayer)
            )
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_research_check",
    {
      title: "ICE research graph integrity check",
      description:
        "Validate local graph structure, tracked hashes, and evidence snapshots. A passing check is not a scientific validation or an execution authorization.",
      inputSchema: { graph: z.string().min(1).max(128).default("all") },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ graph }) => {
      try {
        return asToolResult(
          await Effect.runPromise(graphHarnessCheckData(graph).pipe(Effect.provide(AppLayer)))
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_literature_neighbors",
    {
      title: "OpenAlex citation neighborhood",
      description:
        "Read a bounded incoming, outgoing, and related-work neighborhood for one OpenAlex work. It is external discovery metadata; verify primary sources and citation context before interpretation.",
      inputSchema: {
        work_id: z.string().min(1).max(256),
        limit: z.number().int().min(1).max(20).default(10)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true }
    },
    async ({ work_id, limit }) => {
      try {
        return asToolResult(await getOpenAlexWorkNeighborhood(work_id, limit))
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_graphrag_summary",
    {
      title: "Local evidence GraphRAG summary",
      description:
        "Describe the deterministic repository-local TextUnit, structural-community, and hybrid-retrieval index. Read-only; no model extraction, no automatic follow-up, and no execution authorization.",
      inputSchema: {},
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async () => {
      try {
        return asToolResult(
          await Effect.runPromise(graphRagSummaryData.pipe(Effect.provide(AppLayer)))
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_graphrag_search",
    {
      title: "Local evidence GraphRAG search",
      description:
        "Search canonical ontology TextUnits using BM25, deterministic lexical hash vectors, and bounded graph expansion. Retrieved context is not independent evidence or an execution permit.",
      inputSchema: {
        query: z.string().min(1).max(500),
        graph: z.string().min(1).max(128).default("all"),
        limit: z.number().int().min(1).max(50).default(12),
        depth: z.number().int().min(0).max(3).default(1)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ query, graph, limit, depth }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            graphRagSearchData(query, { graph, limit, depth }).pipe(
              Effect.provide(AppLayer)
            )
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_research_workflow_plan",
    {
      title: "Human-review research workflow plan",
      description:
        "Create a serializable durable workflow checkpoint from local GraphRAG context. It does not persist automatically, call models, or authorize ./ice run.",
      inputSchema: {
        question: z.string().min(1).max(500),
        graph: z.string().min(1).max(128).default("all"),
        limit: z.number().int().min(1).max(50).default(12),
        depth: z.number().int().min(0).max(3).default(1)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ question, graph, limit, depth }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            researchAgentPlanData(question, graph, limit, depth).pipe(
              Effect.provide(AppLayer)
            )
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_literature_search",
    {
      title: "OpenAlex literature graph search",
      description:
        "Search OpenAlex's public works graph for up to 20 time-stamped discovery records. Read primary sources before using a result as research evidence.",
      inputSchema: {
        query: z.string().min(1).max(500),
        limit: z.number().int().min(1).max(20).default(10)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: true }
    },
    async ({ query, limit }) => {
      try {
        return asToolResult(await searchOpenAlexWorks(query, limit))
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_research_capabilities",
    {
      title: "ICE research MCP capability boundaries",
      description:
        "Describe this MCP server's bounded read-only tool surface and non-authorization guarantees.",
      inputSchema: {},
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    () => asToolResult(capabilities)
  )

  return server
}
