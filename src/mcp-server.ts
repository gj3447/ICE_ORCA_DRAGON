import { serveStdio } from "@modelcontextprotocol/server/stdio"
import { createIceResearchMcpServer } from "./mcp.ts"

serveStdio(createIceResearchMcpServer, {
  onerror: (error) => console.error(`ice research MCP error: ${error.message}`)
})

console.error("ICE_ORCA_DRAGON read-only research MCP server is running on stdio")
