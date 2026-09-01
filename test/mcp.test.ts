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
        "ice_research_capabilities"
      ])
    )

    const result = await client.callTool({
      name: "ice_research_capabilities",
      arguments: {}
    })
    expect(result.isError).not.toBe(true)
    expect(JSON.stringify(result.content)).toContain("READ_ONLY_GRAPH_AWARE_RESEARCH_DISCOVERY")
    expect(JSON.stringify(result.content)).toContain("never authorize execution")
  } finally {
    await client.close()
    await server.close()
  }
})
