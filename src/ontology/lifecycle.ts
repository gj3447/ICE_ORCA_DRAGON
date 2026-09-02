/** Version lifecycle is explicit: no synthetic v0 migration exists. */
export type ResearchSchemaFamily = "research-collection" | "research-graph"

export const researchSchemaLifecycle = {
  $schema: "./research-schema-lifecycle-v1.schema.json",
  schema: "ice-research-schema-lifecycle/v1",
  version: 1,
  families: {
    "research-collection": {
      current: "research-collection/v1",
      supported: ["research-collection/v1"],
      migrations: [] as const
    },
    "research-graph": {
      current: "research-graph/v1",
      supported: ["research-graph/v1"],
      migrations: [] as const
    }
  }
} as const

export const assertSupportedResearchSchemaVersion = (
  family: ResearchSchemaFamily,
  version: unknown
): void => {
  const definition = researchSchemaLifecycle.families[family]
  if (typeof version !== "string" || !definition.supported.includes(version as never)) {
    throw new Error(
      `${family} schema version '${String(version)}' is unsupported; current=${definition.current}; future versions require an explicit migration registry entry`
    )
  }
}

export const assertLifecycleDocumentMatchesRuntime = (source: string): void => {
  const parsed = JSON.parse(source) as typeof researchSchemaLifecycle
  if (JSON.stringify(parsed) !== JSON.stringify(researchSchemaLifecycle)) {
    throw new Error("research schema lifecycle document differs from the runtime registry")
  }
}
