import { McpServer } from "@modelcontextprotocol/server"
import { NodeContext } from "@effect/platform-node"
import { Effect, Layer } from "effect"
import * as z from "zod/v4"
import {
  graphHarnessCheckData,
  graphHarnessContextData,
  graphHarnessImpactData
} from "./harness/commands.ts"
import {
  researchAgentPlanData,
  researchAgentRunAuditData,
  researchAgentWorkflowEvaluateData
} from "./agent-graph/commands.ts"
import {
  graphRagDiffData,
  graphRagEvaluateData,
  graphRagSearchData,
  graphRagSummaryData
} from "./graphrag/commands.ts"
import {
  getOpenAlexWorkNeighborhood,
  searchOpenAlexWorks
} from "./literature/openalex.ts"
import {
  ontologyCratePreviewData,
  ontologyShaclData,
  ontologySparqlData
} from "./ontology/commands.ts"
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
  schema: "ice-research-mcp-capabilities/v3",
  mode: "READ_ONLY_GRAPH_INTEROP_RESEARCH_ORCHESTRATION",
  protocol: {
    transport: "stdio",
    modern_revision: "2026-07-28",
    legacy_compatibility: "2024-10-07 through 2025-11-25",
    negotiation: "serveStdio connection-era negotiation",
    extensions: {
      tasks: false,
      skills_over_mcp: false
    }
  },
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
      name: "ice_ontology_shacl_validate",
      purpose: "Run SHACL 1.0 Core against the generated RDF named dataset."
    },
    {
      name: "ice_ontology_sparql_query",
      purpose: "Run the structurally bounded read-only local SPARQL 1.1 subset over the in-memory dataset."
    },
    {
      name: "ice_ontology_ro_crate_preview",
      purpose: "Preview RO-Crate 1.3 metadata, manifest, and SHACL status without writing files."
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
      name: "ice_graphrag_evaluate",
      purpose: "Run the fixed canonical retrieval-regression suite."
    },
    {
      name: "ice_graphrag_diff",
      purpose: "Compare fixed-suite retrieval movement with a committed graph revision."
    },
    {
      name: "ice_research_workflow_plan",
      purpose: "Create a human-review-only TOE critical-path workflow checkpoint."
    },
    {
      name: "ice_research_workflow_evaluate",
      purpose: "Run the fixed routing, durable handoff, and non-authorization suite."
    },
    {
      name: "ice_research_run_audit",
      purpose: "Read and audit one explicitly persisted local run and its revision drift."
    },
    {
      name: "ice_research_capabilities",
      purpose: "Describe this exact tool catalog, protocol support, and non-authorization boundaries."
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
    "ice_ontology_shacl_validate",
    {
      title: "ICE ontology SHACL validation",
      description:
        "Run the bundled SHACL 1.0 Core processor over a generated RDF 1.1 named dataset. Projection QA only; native hash/evidence validation remains separate.",
      inputSchema: {
        graph: z.string().min(1).max(128).default("all")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ graph }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            ontologyShaclData(graph).pipe(Effect.provide(AppLayer))
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_ontology_sparql_query",
    {
      title: "ICE ontology bounded SPARQL query",
      description:
        "Run the restricted local SELECT, ASK, CONSTRUCT, or DESCRIBE subset against the in-memory RDF dataset. Disconnected joins, complex algebra, SERVICE, remote datasets, and updates are rejected.",
      inputSchema: {
        query: z.string().min(1).max(16 * 1024),
        graph: z.string().min(1).max(128).default("all"),
        limit: z.number().int().min(1).max(500).default(100),
        timeout_ms: z.number().int().min(1).max(30_000).default(5_000)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ query, graph, limit, timeout_ms }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            ontologySparqlData(query, graph, limit, timeout_ms).pipe(
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
    "ice_ontology_ro_crate_preview",
    {
      title: "ICE ontology RO-Crate preview",
      description:
        "Return the RO-Crate 1.3 descriptor, hashed manifest, and SHACL report that would be packaged. Read-only and never copies raw result files.",
      inputSchema: {
        graph: z.string().min(1).max(128).default("all")
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ graph }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            ontologyCratePreviewData(graph).pipe(Effect.provide(AppLayer))
          )
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
        "Create a serializable TOE critical-path checkpoint from local GraphRAG context. It does not persist automatically, call models, approve core progress, or authorize ./ice run.",
      inputSchema: {
        question: z.string().min(1).max(500),
        graph: z.string().min(1).max(128).default("cpt"),
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
    "ice_research_workflow_evaluate",
    {
      title: "Research-agent workflow evaluation",
      description:
        "Run the fixed CPT routing, finite human-handoff, event-chain self-consistency, and non-authorization suite. It does not persist a run or assess scientific truth.",
      inputSchema: {},
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async () => {
      try {
        return asToolResult(
          await Effect.runPromise(
            researchAgentWorkflowEvaluateData.pipe(Effect.provide(AppLayer))
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_research_run_audit",
    {
      title: "Durable research-agent run audit",
      description:
        "Read one explicitly created local run and check event-chain self-consistency plus current HEAD, control-plane, ontology, and local-source revision pins. Read-only; the chain is not a signature and CLOSED is not execution approval.",
      inputSchema: {
        run_id: z.string().regex(/^[a-z0-9][a-z0-9_-]{2,127}$/)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ run_id }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            researchAgentRunAuditData(run_id).pipe(Effect.provide(AppLayer))
          )
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_graphrag_evaluate",
    {
      title: "GraphRAG retrieval regression evaluation",
      description:
        "Run the versioned repository-local retrieval suite. It measures canonical locator retrieval only; it does not evaluate scientific truth, citation entailment, or authorize a graph change.",
      inputSchema: {
        limit: z.number().int().min(1).max(50).default(12)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ limit }) => {
      try {
        return asToolResult(
          await Effect.runPromise(graphRagEvaluateData(limit).pipe(Effect.provide(AppLayer)))
        )
      } catch (error) {
        return asToolError(error)
      }
    }
  )

  server.registerTool(
    "ice_graphrag_diff",
    {
      title: "GraphRAG retrieval revision diff",
      description:
        "Compare the fixed retrieval suite against one safe committed Git revision and the working ontology. Read-only; rank movement requires human review and never authorizes a graph or research change.",
      inputSchema: {
        base: z.string().min(1).max(256).default("HEAD"),
        limit: z.number().int().min(1).max(50).default(12)
      },
      annotations: { readOnlyHint: true, destructiveHint: false, openWorldHint: false }
    },
    async ({ base, limit }) => {
      try {
        return asToolResult(
          await Effect.runPromise(
            graphRagDiffData(base, limit).pipe(Effect.provide(AppLayer))
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
