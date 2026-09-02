import { Client, InMemoryTransport } from "@modelcontextprotocol/client"
import { serveStdio } from "@modelcontextprotocol/server/stdio"
import { expect, it } from "vitest"
import { createIceResearchMcpServer } from "../src/mcp.ts"

const expectedTools = [
  "ice_research_context",
  "ice_research_impact",
  "ice_research_check",
  "ice_ontology_shacl_validate",
  "ice_ontology_sparql_query",
  "ice_ontology_ro_crate_preview",
  "ice_literature_neighbors",
  "ice_graphrag_summary",
  "ice_graphrag_search",
  "ice_research_workflow_plan",
  "ice_research_workflow_evaluate",
  "ice_research_run_audit",
  "ice_graphrag_evaluate",
  "ice_graphrag_diff",
  "ice_literature_search",
  "ice_research_capabilities"
] as const

it("exposes a bounded read-only MCP capability surface", async () => {
  const [serverTransport, clientTransport] = InMemoryTransport.createLinkedPair()
  const server = createIceResearchMcpServer()
  const client = new Client({ name: "ice-mcp-test", version: "0.1.0" })

  await server.connect(serverTransport)
  await client.connect(clientTransport)
  try {
    const listed = await client.listTools()
    expect(listed.tools.map(({ name }) => name)).toEqual(expectedTools)
    for (const tool of listed.tools) {
      expect(tool.annotations).toMatchObject({
        readOnlyHint: true,
        destructiveHint: false
      })
    }

    const localSearch = listed.tools.find(({ name }) => name === "ice_graphrag_search")
    const externalSearch = listed.tools.find(({ name }) => name === "ice_literature_search")
    expect(localSearch?.annotations?.openWorldHint).toBe(false)
    expect(externalSearch?.annotations?.openWorldHint).toBe(true)

    const result = await client.callTool({
      name: "ice_research_capabilities",
      arguments: {}
    })
    expect(result.isError).not.toBe(true)
    const capabilityText = result.content.find(({ type }) => type === "text")
    if (capabilityText?.type !== "text") {
      throw new Error("capability tool did not return text content")
    }
    const capabilityPayload = JSON.parse(capabilityText.text) as {
      readonly mode: string
      readonly protocol: {
        readonly modern_revision: string
        readonly extensions: { readonly skills_over_mcp: boolean }
      }
      readonly boundaries: ReadonlyArray<string>
    }
    expect(capabilityPayload.mode).toBe("READ_ONLY_GRAPH_INTEROP_RESEARCH_ORCHESTRATION")
    expect(capabilityPayload.protocol.modern_revision).toBe("2026-07-28")
    expect(capabilityPayload.protocol.extensions.skills_over_mcp).toBe(false)
    expect(capabilityPayload.boundaries.join(" ")).toContain("never authorize execution")

    const graphRagSummary = await client.callTool({
      name: "ice_graphrag_summary",
      arguments: {}
    })
    expect(graphRagSummary.isError).not.toBe(true)
    expect(JSON.stringify(graphRagSummary.content)).toContain(
      "ice-evidence-graph-rag-summary/v1"
    )

    const graphRagEvaluation = await client.callTool({
      name: "ice_graphrag_evaluate",
      arguments: { limit: 12 }
    })
    expect(graphRagEvaluation.isError).not.toBe(true)
    expect(JSON.stringify(graphRagEvaluation.content)).toContain(
      "canonical-four-graph-navigation"
    )

    const graphRagDiff = await client.callTool({
      name: "ice_graphrag_diff",
      arguments: { base: "HEAD", limit: 12 }
    })
    expect(graphRagDiff.isError).not.toBe(true)
    expect(JSON.stringify(graphRagDiff.content)).toContain(
      "ice-graphrag-revision-diff/v1"
    )

    const toePlan = await client.callTool({
      name: "ice_research_workflow_plan",
      arguments: {
        question: "Gate 1 original joint cycle and signed global intersection vector",
        graph: "cpt"
      }
    })
    expect(toePlan.isError).not.toBe(true)
    expect(JSON.stringify(toePlan.content)).toContain("CURRENT_BLOCKER_CANDIDATE")
    expect(JSON.stringify(toePlan.content)).toContain(
      "TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW"
    )

    const shacl = await client.callTool({
      name: "ice_ontology_shacl_validate",
      arguments: { graph: "cpt" }
    })
    expect(shacl.isError).not.toBe(true)
    expect(JSON.stringify(shacl.content)).toContain('\\"conforms\\": true')

    const sparql = await client.callTool({
      name: "ice_ontology_sparql_query",
      arguments: {
        graph: "cpt",
        limit: 10,
        query:
          "ASK WHERE { GRAPH <urn:ice-orca-dragon:resource:graph:cpt> { ?node a <urn:ice-orca-dragon:ontology:ResearchNode> } }"
      }
    })
    expect(sparql.isError).not.toBe(true)
    expect(JSON.stringify(sparql.content)).toContain('\\"boolean\\": true')

    const crate = await client.callTool({
      name: "ice_ontology_ro_crate_preview",
      arguments: { graph: "cpt" }
    })
    expect(crate.isError).not.toBe(true)
    expect(JSON.stringify(crate.content)).toContain(
      "https://w3id.org/ro/crate/1.3/context"
    )

    const workflowEvaluation = await client.callTool({
      name: "ice_research_workflow_evaluate",
      arguments: {}
    })
    expect(workflowEvaluation.isError).not.toBe(true)
    expect(JSON.stringify(workflowEvaluation.content)).toContain(
      '\\"passed\\": true'
    )
  } finally {
    await client.close()
    await server.close()
  }
}, 30_000)

it("negotiates the MCP 2026-07-28 era over stdio", async () => {
  const [serverTransport, clientTransport] = InMemoryTransport.createLinkedPair()
  const handle = serveStdio(createIceResearchMcpServer, { transport: serverTransport })
  const client = new Client(
    { name: "ice-modern-mcp-test", version: "0.1.0" },
    { versionNegotiation: { mode: { pin: "2026-07-28" } } }
  )

  await client.connect(clientTransport)
  try {
    expect(client.getProtocolEra()).toBe("modern")
    expect(client.getNegotiatedProtocolVersion()).toBe("2026-07-28")
    const listed = await client.listTools()
    expect(listed.tools.map(({ name }) => name)).toEqual(expectedTools)
  } finally {
    await client.close()
    await handle.close()
  }
})
