export const RO_CRATE_13_CONTEXT = "https://w3id.org/ro/crate/1.3/context" as const
export const RO_CRATE_13_SPECIFICATION = "https://w3id.org/ro/crate/1.3" as const

export interface RoCrateBaseProfileViolation {
  readonly code: string
  readonly path: string
  readonly message: string
}

export interface RoCrateBaseProfileReport {
  readonly schema: "ice-ro-crate-1.3-base-profile-report/v1"
  readonly conforms: boolean
  readonly violations: ReadonlyArray<RoCrateBaseProfileViolation>
}

type JsonRecord = Readonly<Record<string, unknown>>

const isRecord = (value: unknown): value is JsonRecord =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const values = (value: unknown): ReadonlyArray<unknown> =>
  Array.isArray(value) ? value : value === undefined ? [] : [value]

const hasType = (entity: JsonRecord, expected: string): boolean =>
  values(entity["@type"]).includes(expected)

const idOf = (value: unknown): string | undefined =>
  isRecord(value) && typeof value["@id"] === "string" ? value["@id"] : undefined

const nonemptyString = (value: unknown): value is string =>
  typeof value === "string" && value.trim().length > 0

/**
 * Validate the RO-Crate 1.3 base-profile records emitted by this repository.
 *
 * This is a structural, offline base-profile check. It deliberately does not
 * dereference the remote context or claim validation of RO-Crate extensions,
 * workflow profiles, packaging media, or every schema.org recommendation.
 */
export const validateRoCrate13BaseProfile = (
  metadata: unknown
): RoCrateBaseProfileReport => {
  const violations: Array<RoCrateBaseProfileViolation> = []
  const add = (code: string, path: string, message: string): void => {
    violations.push({ code, path, message })
  }
  if (!isRecord(metadata)) {
    add("METADATA_NOT_OBJECT", "$", "RO-Crate metadata must be a JSON object")
    return {
      schema: "ice-ro-crate-1.3-base-profile-report/v1",
      conforms: false,
      violations
    }
  }

  const context = metadata["@context"]
  if (!Array.isArray(context) || context[0] !== RO_CRATE_13_CONTEXT) {
    add(
      "MISSING_RO_CRATE_13_CONTEXT",
      "$.@context",
      "the first @context entry must be the RO-Crate 1.3 context"
    )
  }
  const graph = metadata["@graph"]
  if (!Array.isArray(graph)) {
    add("MISSING_GRAPH", "$.@graph", "RO-Crate metadata must contain an @graph array")
    return {
      schema: "ice-ro-crate-1.3-base-profile-report/v1",
      conforms: false,
      violations
    }
  }

  const entities = new Map<string, JsonRecord>()
  for (const [index, value] of graph.entries()) {
    if (!isRecord(value) || !nonemptyString(value["@id"])) {
      add("ENTITY_MISSING_ID", `$.@graph[${index}]`, "each graph entity must have a nonempty @id")
      continue
    }
    if (entities.has(value["@id"])) {
      add("DUPLICATE_ENTITY_ID", `$.@graph[${index}].@id`, "graph entity @id values must be unique")
      continue
    }
    entities.set(value["@id"], value)
  }

  const descriptor = entities.get("ro-crate-metadata.json")
  if (descriptor === undefined) {
    add("MISSING_METADATA_DESCRIPTOR", "$.@graph", "missing ro-crate-metadata.json CreativeWork")
  } else {
    if (!hasType(descriptor, "CreativeWork")) {
      add("METADATA_DESCRIPTOR_TYPE", "ro-crate-metadata.json.@type", "metadata descriptor must be a CreativeWork")
    }
    if (idOf(descriptor.conformsTo) !== RO_CRATE_13_SPECIFICATION) {
      add("METADATA_DESCRIPTOR_CONFORMS_TO", "ro-crate-metadata.json.conformsTo", "metadata descriptor must declare RO-Crate 1.3")
    }
    if (idOf(descriptor.about) !== "./") {
      add("METADATA_DESCRIPTOR_ABOUT", "ro-crate-metadata.json.about", "metadata descriptor must describe the root data entity './'")
    }
  }

  const root = entities.get("./")
  if (root === undefined) {
    add("MISSING_ROOT_DATASET", "$.@graph", "missing root data entity './'")
  } else {
    if (!hasType(root, "Dataset")) {
      add("ROOT_TYPE", "./.@type", "root data entity must be a Dataset")
    }
    if (!nonemptyString(root.name)) {
      add("ROOT_NAME", "./.name", "root Dataset must have a nonempty name")
    }
    if (!nonemptyString(root.description)) {
      add("ROOT_DESCRIPTION", "./.description", "root Dataset must have a nonempty description")
    }
    for (const [index, part] of values(root.hasPart).entries()) {
      const id = idOf(part)
      if (id === undefined) {
        add("ROOT_HAS_PART_REFERENCE", `./.hasPart[${index}]`, "hasPart entries must be @id references")
        continue
      }
      const entity = entities.get(id)
      if (entity === undefined) {
        add("ROOT_HAS_PART_DANGLING", `./.hasPart[${index}]`, `hasPart target '${id}' is absent from @graph`)
      } else if (!hasType(entity, "File")) {
        add("ROOT_HAS_PART_NOT_FILE", `./.hasPart[${index}]`, `hasPart target '${id}' must be a File entity`)
      }
    }
  }

  return {
    schema: "ice-ro-crate-1.3-base-profile-report/v1",
    conforms: violations.length === 0,
    violations
  }
}
