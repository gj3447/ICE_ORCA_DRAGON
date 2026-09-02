import { createHash } from "node:crypto"
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import jsonld, { type JsonLdDocument } from "jsonld"
import { expect, it } from "vitest"
import { createOntologyInteropCrate, RO_CRATE_CONTEXT } from "../src/ontology/crate.ts"

it("creates a non-overwriting RO-Crate 1.3 metadata/export package", async () => {
  const root = await mkdtemp(join(tmpdir(), "ice-crate-"))
  try {
    await mkdir(join(root, "ontology", "standards"), { recursive: true })
    await writeFile(
      join(root, "ontology", "standards", "research-graph-shapes.ttl"),
      await readFile(
        join(process.cwd(), "ontology", "standards", "research-graph-shapes.ttl"),
        "utf8"
      )
    )
    const descriptor = { key: "demo", graph_id: "research-graph:demo", path: "ontology/demo/graph.json", guide: "guide", entry_node: "programme:demo", coverage: "DETAILED", corpus_roots: ["demo"], includes: [], excludes: [] }
    const collection = { schema_version: "research-collection/v1", collection_id: "research-collection:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: "ontology/collection.json", default_graph: "demo", graphs: [descriptor], quick_answers: [], reading_paths: [], coverage_ledger: [] }
    const graph = { schema_version: "research-graph/v1", graph_id: "research-graph:demo", title: "Demo", description: "Demo", updated_at_utc: "2026-09-02T00:00:00Z", canonical_file: descriptor.path, source_inventory: "sources", quick_answers: [], reading_paths: [], node_type_legend: {}, relation_legend: {}, nodes: [{ id: "programme:demo", type: "programme", title: "Demo", summary: "Demo", state: "ACTIVE" }, { id: "artifact:raw", type: "artifact", title: "Raw result locator", summary: "Not copied", state: "TRACKED", artifact_kind: "result", path: "raw/result.json", sha256: "d".repeat(64) }], edges: [], kg_bridges: [] }
    const result = await createOntologyInteropCrate(collection as any, [{ descriptor, graph, validation: {} }] as any, { workspaceRoot: root, outputDirectory: "output/crate", createdAt: "2026-09-02T00:00:00.000Z", sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })
    expect(result.files).toContain("ro-crate-metadata.json")
    expect(result.shacl_conforms).toBe(true)
    const metadata = JSON.parse(await readFile(join(root, "output", "crate", "ro-crate-metadata.json"), "utf8"))
    expect(metadata["@context"][0]).toBe(RO_CRATE_CONTEXT)
    const crateRoot = metadata["@graph"].find((entry: { "@id": string }) => entry["@id"] === "./")
    expect(crateRoot.hasPart.map(({ "@id": id }: { "@id": string }) => id)).toEqual([
      "research-graph.jsonld",
      "research-graph-compatibility.jsonld",
      "research-graph.nq",
      "research-graph-shapes.ttl",
      "shacl-report.json",
      "manifest.json"
    ])
    expect(JSON.stringify(metadata)).toContain("prov:used")
    const packagedJsonLd = JSON.parse(
      await readFile(join(root, "output", "crate", "research-graph.jsonld"), "utf8")
    )
    expect(JSON.stringify(packagedJsonLd)).toContain("ProjectionExportActivity")
    expect(JSON.stringify(packagedJsonLd)).toContain("@graph")
    const compatibilitySource = await readFile(
      join(root, "output", "crate", "research-graph-compatibility.jsonld"),
      "utf8"
    )
    expect(
      await readFile(join(root, "output", "crate", "research-graph.nq"), "utf8")
    ).toContain(
      createHash("sha256").update(compatibilitySource).digest("hex")
    )
    expect(
      await jsonld.canonize(packagedJsonLd as JsonLdDocument, {
        algorithm: "URDNA2015",
        format: "application/n-quads"
      })
    ).toBe(
      await readFile(join(root, "output", "crate", "research-graph.nq"), "utf8")
    )
    const manifestSource = await readFile(join(root, "output", "crate", "manifest.json"), "utf8")
    const manifest = JSON.parse(manifestSource)
    expect(manifest.package_scope).toBe("METADATA_AND_GRAPH_EXPORT_NO_RAW_RESULTS")
    expect(manifest.files.map(({ path }: { path: string }) => path)).toContain(
      "research-graph-shapes.ttl"
    )
    expect(result.manifest_sha256).toBe(
      createHash("sha256").update(manifestSource).digest("hex")
    )
    await expect(readFile(join(root, "output", "crate", "raw", "result.json"))).rejects.toThrow()
    await expect(createOntologyInteropCrate(collection as any, [{ descriptor, graph, validation: {} }] as any, { workspaceRoot: root, outputDirectory: "output/crate", sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })).rejects.toThrow("already exists")
    await expect(createOntologyInteropCrate(collection as any, [{ descriptor, graph, validation: {} }] as any, { workspaceRoot: root, outputDirectory: "output/invalid-date", createdAt: "September 2, 2026", sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })).rejects.toThrow("canonical UTC")
    const concurrent = await Promise.allSettled([
      createOntologyInteropCrate(collection as any, [{ descriptor, graph, validation: {} }] as any, { workspaceRoot: root, outputDirectory: "output/concurrent", sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] }),
      createOntologyInteropCrate(collection as any, [{ descriptor, graph, validation: {} }] as any, { workspaceRoot: root, outputDirectory: "output/concurrent", sourceDocuments: [{ path: "ontology/collection.json", sha256: "a".repeat(64) }] })
    ])
    expect(concurrent.filter(({ status }) => status === "fulfilled")).toHaveLength(1)
    expect(concurrent.filter(({ status }) => status === "rejected")).toHaveLength(1)
    await expect(
      readFile(join(root, "output", "concurrent", "manifest.json"), "utf8")
    ).resolves.toContain("ice-ontology-interop-manifest/v1")
  } finally { await rm(root, { recursive: true, force: true }) }
})
