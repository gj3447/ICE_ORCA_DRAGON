import { serveStdio } from "@modelcontextprotocol/server/stdio"
import { createIceResearchMcpServer } from "./mcp.ts"

serveStdio(createIceResearchMcpServer, {
  // Serve the 2026-07-28 stateless era while retaining negotiated support for
  // existing 2025-era stdio hosts.
  legacy: "serve",
  onerror: (error) => console.error(`ice research MCP error: ${error.message}`)
})

console.error("ICE_ORCA_DRAGON read-only research MCP server is running on stdio")
