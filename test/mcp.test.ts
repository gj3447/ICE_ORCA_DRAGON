import { Client, InMemoryTransport } from "@modelcontextprotocol/client"
import { expect, it } from "vitest"
import { createIceResearchMcpServer } from "../src/mcp.ts"

it("exposes a bounded read-only MCP capability surface", async () => {
  const [serverTransport, clientTransport] = InMemoryTransport.createLinkedPair()
  const server = createIceResearchMcpServer()
  const client = new Client({ name: "ice-mcp-test", version: "0.1.0" })

  await server.connect(serverTransport)
  await client.connect(clientTransport)
  try {
    const listed = await client.listTools()
    expect(listed.tools.map(({ name }) => name)).toEqual(
      expect.arrayContaining([
        "ice_research_context",
        "ice_research_impact",
        "ice_research_check",
        "ice_literature_search",
        "ice_literature_neighbors",
        "ice_graphrag_summary",
        "ice_graphrag_search",
        "ice_research_workflow_plan",
        "ice_research_capabilities"
      ])
    )

    const localSearch = listed.tools.find(({ name }) => name === "ice_graphrag_search")
    const externalSearch = listed.tools.find(({ name }) => name === "ice_literature_search")
    expect(localSearch?.annotations?.openWorldHint).toBe(false)
    expect(externalSearch?.annotations?.openWorldHint).toBe(true)

    const result = await client.callTool({
      name: "ice_research_capabilities",
      arguments: {}
    })
    expect(result.isError).not.toBe(true)
    expect(JSON.stringify(result.content)).toContain("READ_ONLY_GRAPH_AWARE_RESEARCH_DISCOVERY")
    expect(JSON.stringify(result.content)).toContain("never authorize execution")

    const graphRagSummary = await client.callTool({
      name: "ice_graphrag_summary",
      arguments: {}
    })
    expect(graphRagSummary.isError).not.toBe(true)
    expect(JSON.stringify(graphRagSummary.content)).toContain(
      "ice-evidence-graph-rag-summary/v1"
    )
  } finally {
    await client.close()
    await server.close()
  }
})
