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
        "ice_ontology_shacl_validate",
        "ice_ontology_sparql_query",
        "ice_ontology_ro_crate_preview",
        "ice_literature_search",
        "ice_literature_neighbors",
        "ice_graphrag_summary",
        "ice_graphrag_search",
        "ice_graphrag_evaluate",
        "ice_graphrag_diff",
        "ice_research_workflow_plan",
        "ice_research_workflow_evaluate",
        "ice_research_run_audit",
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
    expect(JSON.stringify(result.content)).toContain(
      "READ_ONLY_GRAPH_INTEROP_RESEARCH_ORCHESTRATION"
    )
    expect(JSON.stringify(result.content)).toContain("never authorize execution")

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
