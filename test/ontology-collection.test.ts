import { NodeContext } from "@effect/platform-node"
import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { expect, it, layer } from "@effect/vitest"
import { Console, Effect, Layer } from "effect"
import {
  findCollectionNodes,
  validateCollectionManifest,
  validateCollectionSemantics,
  type CollectionGraph
} from "../src/ontology/collection-core.ts"
import { decodeResearchCollection } from "../src/ontology/collection.ts"
import {
  ontologyShowCommand,
  ontologyValidateCommand
} from "../src/ontology/commands.ts"
import {
  makeValidationReport,
  validateGraphSemantics
} from "../src/ontology/core.ts"
import { decodeResearchGraph } from "../src/ontology/model.ts"
import {
  loadOntologyCollectionValidation,
  loadResearchGraphAt,
  loadResearchGraphAtRevision,
  loadResearchCollection,
  loadResearchCollectionAtRevision
} from "../src/ontology/repository.ts"
import {
  Workspace,
  WorkspaceLive,
  workspaceFromRoot
} from "../src/workspace.ts"

const graphFixture = (key: string) => ({
  $schema: "../schema/research-graph-v1.schema.json",
  schema_version: "research-graph/v1",
  graph_id: `research-graph:${key}`,
  title: `${key} graph`,
  description: "Small collection graph fixture",
  updated_at_utc: "2026-08-25T00:00:00Z",
  canonical_file: `ontology/${key}/graph.json`,
  source_inventory: `ontology/${key}/sources.md`,
  quick_answers: [
    {
      question: "Does the shared fixture claim hold?",
      answer: `Yes within the ${key} fixture.`,
      claim_ids: ["claim:SHARED"]
    }
  ],
  reading_paths: [
    {
      id: `reading-path:${key}`,
      title: `${key} fixture path`,
      summary: "Programme to claim to evidence",
      nodes: [
        `programme:${key}`,
        "claim:SHARED",
        `evidence:${key}`
      ]
    }
  ],
  node_type_legend: {
    programme: "programme boundary",
    claim: "testable statement",
    evidence: "observed fixture result",
    artifact: "tracked fixture file"
  },
  relation_legend: {
    PART_OF: "node belongs to programme",
    HAS_EVIDENCE: "claim has directional evidence",
    RECORDED_IN: "evidence is recorded in an artifact"
  },
  nodes: [
    {
      id: `programme:${key}`,
      type: "programme",
      title: `${key} programme`,
      summary: "Fixture programme boundary",
      state: "ACTIVE"
    },
    {
      id: "claim:SHARED",
      type: "claim",
      title: "Shared fixture claim",
      summary: `Supported only inside the ${key} fixture.`,
      state: "SUPPORTED",
      claim_id: "SHARED",
      statement: `The ${key} fixture contract holds.`,
      epistemic_state: "SUPPORTED"
    },
    {
      id: `evidence:${key}`,
      type: "evidence",
      title: `${key} fixture evidence`,
      summary: "One exact fixture observation",
      state: "VERIFIED",
      observed_status: "1_PASS",
      check_ids: [`${key}.check`]
    },
    {
      id: `artifact:${key}`,
      type: "artifact",
      title: `${key} fixture result`,
      summary: "Synthetic fixture artifact",
      state: "TRACKED",
      artifact_kind: "result",
      path: `fixtures/${key}.json`,
      sha256: "0".repeat(64)
    }
  ],
  edges: [
    {
      id: "edge:001",
      from: "claim:SHARED",
      relation: "PART_OF",
      to: `programme:${key}`
    },
    {
      id: "edge:002",
      from: "claim:SHARED",
      relation: "HAS_EVIDENCE",
      to: `evidence:${key}`,
      polarity: "SUPPORTS"
    },
    {
      id: "edge:003",
      from: `evidence:${key}`,
      relation: "RECORDED_IN",
      to: `artifact:${key}`
    }
  ],
  kg_bridges: []
})

const collectionFixture = () => ({
  $schema: "schema/research-collection-v1.schema.json",
  schema_version: "research-collection/v1",
  collection_id: "research-collection:test",
  title: "Test research collection",
  description: "Independent graphs joined only by navigation metadata",
  updated_at_utc: "2026-08-25T00:00:00Z",
  canonical_file: "ontology/collection.json",
  default_graph: "alpha",
  graphs: ["alpha", "beta"].map((key) => ({
    key,
    graph_id: `research-graph:${key}`,
    path: `ontology/${key}/graph.json`,
    guide: `ontology/${key}/README.md`,
    entry_node: `programme:${key}`,
    coverage: "PARTIAL",
    corpus_roots: [`research/${key}`],
    includes: ["representative claims"],
    excludes: ["exhaustive archival indexing"]
  })),
  quick_answers: [
    {
      question: "Where is the alpha claim?",
      answer: "In the alpha graph.",
      refs: [{ graph: "alpha", node: "claim:SHARED" }]
    }
  ],
  reading_paths: [
    {
      id: "collection-path:cross-fixture",
      title: "Cross-fixture navigation",
      summary: "Read the same local identifier in two independent scopes.",
      navigation_only: true,
      stops: [
        { graph: "alpha", node: "claim:SHARED" },
        { graph: "beta", node: "claim:SHARED" }
      ]
    }
  ],
  coverage_ledger: [
    {
      path: "research/alpha",
      status: "PARTIAL",
      graph: "alpha",
      reason: "Representative fixture coverage"
    },
    {
      path: "research/beta",
      status: "PARTIAL",
      graph: "beta",
      reason: "Representative fixture coverage"
    }
  ]
})

it.effect("decodes a strict collection and resolves graph-qualified nodes", () =>
  Effect.gen(function* () {
    const collection = yield* decodeResearchCollection(
      JSON.stringify(collectionFixture()),
      "collection fixture"
    )
    const alpha = yield* decodeResearchGraph(
      JSON.stringify(graphFixture("alpha")),
      "alpha fixture"
    )
    const beta = yield* decodeResearchGraph(
      JSON.stringify(graphFixture("beta")),
      "beta fixture"
    )
    const alphaDescriptor = collection.graphs.find(({ key }) => key === "alpha")
    const betaDescriptor = collection.graphs.find(({ key }) => key === "beta")
    if (alphaDescriptor === undefined || betaDescriptor === undefined) {
      return yield* Effect.fail(new Error("collection descriptors are missing"))
    }
    const graphs: ReadonlyArray<CollectionGraph> = [
      {
        descriptor: alphaDescriptor,
        graph: alpha,
        validation: makeValidationReport(alpha, validateGraphSemantics(alpha))
      },
      {
        descriptor: betaDescriptor,
        graph: beta,
        validation: makeValidationReport(beta, validateGraphSemantics(beta))
      }
    ]

    expect(validateCollectionSemantics(collection, graphs)).toEqual([])
    expect(findCollectionNodes(graphs, "SHARED")).toHaveLength(2)
    expect(findCollectionNodes(graphs, "alpha::claim:SHARED")).toMatchObject([
      { key: "alpha", node: { id: "claim:SHARED" } }
    ])

    const invalidCanonical = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        canonical_file: "ontology/not-the-canonical-file.json"
      }),
      "invalid canonical fixture"
    ).pipe(Effect.either)
    expect(invalidCanonical._tag).toBe("Left")

    const reservedAll = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        default_graph: "all",
        graphs: [
          {
            ...collectionFixture().graphs[0],
            key: "all"
          }
        ]
      }),
      "reserved all fixture"
    ).pipe(Effect.either)
    expect(reservedAll._tag).toBe("Left")

    const tooManyStops = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        reading_paths: [
          {
            ...collectionFixture().reading_paths[0],
            stops: Array.from({ length: 13 }, () => ({
              graph: "alpha",
              node: "claim:SHARED"
            }))
          }
        ]
      }),
      "thirteen-stop fixture"
    ).pipe(Effect.either)
    expect(tooManyStops._tag).toBe("Left")

    const mismatchedCoverage = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        graphs: collectionFixture().graphs.map((descriptor) =>
          descriptor.key === "alpha"
            ? { ...descriptor, coverage: "DETAILED" }
            : descriptor
        )
      }),
      "mismatched root coverage fixture"
    )
    expect(
      validateCollectionManifest(mismatchedCoverage).map(({ code }) => code)
    ).toContain("COLLECTION_CORPUS_ROOT_COVERAGE_MISSING")

    const archivedOwner = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        coverage_ledger: collectionFixture().coverage_ledger.map((entry) =>
          entry.path === "research/alpha"
            ? { ...entry, status: "ARCHIVE" }
            : entry
        )
      }),
      "archive owner fixture"
    )
    expect(
      validateCollectionManifest(archivedOwner).map(({ code }) => code)
    ).toContain("COLLECTION_NONACTIVE_GRAPH_FORBIDDEN")

    const overlappingRoots = yield* decodeResearchCollection(
      JSON.stringify({
        ...collectionFixture(),
        graphs: collectionFixture().graphs.map((descriptor) =>
          descriptor.key === "beta"
            ? { ...descriptor, corpus_roots: ["research/alpha/nested"] }
            : descriptor
        ),
        coverage_ledger: collectionFixture().coverage_ledger.map((entry) =>
          entry.graph === "beta"
            ? { ...entry, path: "research/alpha/nested" }
            : entry
        )
      }),
      "overlapping roots fixture"
    )
    expect(
      validateCollectionManifest(overlappingRoots).map(({ code }) => code)
    ).toContain("COLLECTION_OVERLAPPING_CORPUS_ROOT")
  })
)

it.effect("detects duplicate descriptors, broken references, and cross-graph hash drift", () =>
  Effect.gen(function* () {
    const collection = yield* decodeResearchCollection(
      JSON.stringify(collectionFixture()),
      "collection fixture"
    )
    const alpha = yield* decodeResearchGraph(
      JSON.stringify(graphFixture("alpha")),
      "alpha fixture"
    )
    const beta = yield* decodeResearchGraph(
      JSON.stringify(graphFixture("beta")),
      "beta fixture"
    )
    const alphaDescriptor = collection.graphs.find(({ key }) => key === "alpha")
    const betaDescriptor = collection.graphs.find(({ key }) => key === "beta")
    const firstAnswer = collection.quick_answers[0]
    if (
      alphaDescriptor === undefined ||
      betaDescriptor === undefined ||
      firstAnswer === undefined
    ) {
      return yield* Effect.fail(new Error("collection fixture is incomplete"))
    }
    const betaWithConflict = {
      ...beta,
      nodes: beta.nodes.map((node) =>
        node.type === "artifact"
          ? {
              ...node,
              path: "fixtures/alpha.json",
              sha256: "1".repeat(64)
            }
          : node
      )
    }
    const graphs: ReadonlyArray<CollectionGraph> = [
      {
        descriptor: alphaDescriptor,
        graph: alpha,
        validation: makeValidationReport(alpha, validateGraphSemantics(alpha))
      },
      {
        descriptor: betaDescriptor,
        graph: betaWithConflict,
        validation: makeValidationReport(
          betaWithConflict,
          validateGraphSemantics(betaWithConflict)
        )
      }
    ]
    const broken = yield* decodeResearchCollection(
      JSON.stringify({
        ...collection,
        graphs: [alphaDescriptor, ...collection.graphs],
        quick_answers: [
          {
            ...firstAnswer,
            refs: [{ graph: "missing", node: "claim:SHARED" }]
          }
        ],
        coverage_ledger: [
          ...collection.coverage_ledger,
          collection.coverage_ledger[0],
          {
            path: "outside/alpha",
            status: "PARTIAL",
            graph: "alpha",
            reason: "Deliberately outside the descriptor root"
          }
        ]
      }),
      "semantically broken collection fixture"
    )
    const codes = validateCollectionSemantics(broken, graphs).map(
      ({ code }) => code
    )

    expect(codes).toContain("COLLECTION_DUPLICATE_GRAPH_KEY")
    expect(codes).toContain("COLLECTION_REF_GRAPH_NOT_FOUND")
    expect(codes).toContain("COLLECTION_ARTIFACT_HASH_CONFLICT")
    expect(codes).toContain("COLLECTION_DUPLICATE_COVERAGE_PATH")
    expect(codes).toContain("COLLECTION_COVERAGE_OUTSIDE_CORPUS_ROOT")
  })
)

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("canonical ontology collection", (it) => {
  it.effect("bounds committed graph reads and rejects unsafe revision syntax", () =>
    Effect.gen(function* () {
      const unsafe = yield* loadResearchGraphAtRevision(
        "HEAD:alternate-path",
        "ontology/cpt-temporal-folded-susy/graph.json"
      ).pipe(Effect.either)
      expect(unsafe._tag).toBe("Left")
      if (unsafe._tag === "Left") {
        expect(unsafe.left.code).toBe("ONTOLOGY_GIT_REVISION_UNSAFE")
      }

      const missing = yield* loadResearchGraphAtRevision(
        "definitely-missing-ontology-revision",
        "ontology/cpt-temporal-folded-susy/graph.json"
      ).pipe(Effect.either)
      expect(missing._tag).toBe("Left")
      if (missing._tag === "Left") {
        expect(missing.left.code).toBe("ONTOLOGY_GIT_READ_FAILED")
      }
    })
  )

  it.effect("uses the same bounded revision reader for the collection manifest", () =>
    Effect.gen(function* () {
      const committed = yield* loadResearchCollectionAtRevision("HEAD")
      expect(committed.collection_id).toBe("research-collection:ice-orca-dragon")

      const unsafe = yield* loadResearchCollectionAtRevision(
        "HEAD:alternate-path"
      ).pipe(Effect.either)
      expect(unsafe._tag).toBe("Left")
      if (unsafe._tag === "Left") {
        expect(unsafe.left.code).toBe("ONTOLOGY_GIT_REVISION_UNSAFE")
      }
    })
  )

  it.effect("rejects a graph symlink that resolves outside the workspace", () =>
    Effect.scoped(
      Effect.gen(function* () {
        const workspace = yield* Workspace
        const fs = yield* FileSystem.FileSystem
        const path = yield* Path.Path
        const outside = yield* fs.makeTempDirectoryScoped({
          prefix: "ice-ontology-outside-"
        })
        const inside = yield* fs.makeTempDirectoryScoped({
          directory: workspace.root,
          prefix: ".ice-ontology-inside-"
        })
        const outsideGraph = path.join(outside, "graph.json")
        const link = path.join(inside, "graph.json")
        yield* fs.writeFileString(outsideGraph, "{}")
        yield* fs.symlink(outsideGraph, link)

        const result = yield* loadResearchGraphAt(
          path.relative(workspace.root, link)
        ).pipe(Effect.either)
        expect(result._tag).toBe("Left")
        if (result._tag === "Left") {
          expect(result.left.code).toBe(
            "ONTOLOGY_GRAPH_PATH_ESCAPES_WORKSPACE"
          )
        }
      })
    )
  )

  it.effect("keeps valid sibling diagnostics when one graph is malformed", () =>
    Effect.scoped(
      Effect.gen(function* () {
        const fs = yield* FileSystem.FileSystem
        const path = yield* Path.Path
        const temporary = yield* fs.makeTempDirectoryScoped({
          prefix: "ice-ontology-partial-"
        })
        for (const directory of [
          "ontology/alpha",
          "ontology/beta",
          "research/alpha",
          "research/beta"
        ]) {
          yield* fs.makeDirectory(path.join(temporary, directory), {
            recursive: true
          })
        }
        yield* fs.writeFileString(
          path.join(temporary, "ontology/alpha/README.md"),
          "# alpha\n"
        )
        yield* fs.writeFileString(
          path.join(temporary, "ontology/beta/README.md"),
          "# beta\n"
        )
        yield* fs.writeFileString(
          path.join(temporary, "ontology/collection.json"),
          JSON.stringify(collectionFixture())
        )
        const alpha = graphFixture("alpha")
        yield* fs.writeFileString(
          path.join(temporary, "ontology/alpha/graph.json"),
          JSON.stringify({
            ...alpha,
            nodes: alpha.nodes.filter(({ type }) => type !== "artifact"),
            edges: alpha.edges.filter(({ id }) => id !== "edge:003")
          })
        )
        yield* fs.writeFileString(
          path.join(temporary, "ontology/beta/graph.json"),
          "{ malformed"
        )

        const loaded = yield* loadOntologyCollectionValidation.pipe(
          Effect.provideService(Workspace, workspaceFromRoot(temporary))
        )
        expect(loaded.validation.valid).toBe(false)
        expect(loaded.graphs.map(({ descriptor }) => descriptor.key)).toEqual([
          "alpha"
        ])
        expect(loaded.validation.graphs).toHaveLength(2)
        expect(loaded.validation.counts.nodes).toBe(3)
        expect(
          loaded.validation.graphs
            .find(({ graph_id }) => graph_id === "research-graph:beta")
            ?.errors.map(({ code }) => code)
        ).toContain("ONTOLOGY_SCHEMA_INVALID")

        yield* fs.writeFileString(
          path.join(temporary, "ontology/collection.json"),
          JSON.stringify({
            ...collectionFixture(),
            default_graph: "missing"
          })
        )
        const nonBlockingManifestError =
          yield* loadOntologyCollectionValidation.pipe(
            Effect.provideService(Workspace, workspaceFromRoot(temporary))
          )
        expect(nonBlockingManifestError.validation.graphs).toHaveLength(2)
        expect(
          nonBlockingManifestError.validation.errors.map(({ code }) => code)
        ).toContain("COLLECTION_DEFAULT_GRAPH_NOT_FOUND")
        yield* fs.writeFileString(
          path.join(temporary, "ontology/collection.json"),
          JSON.stringify(collectionFixture())
        )

        const selectedReport = yield* Console.consoleWith((currentConsole) =>
          ontologyValidateCommand(true, "alpha").pipe(
            Effect.provideService(Workspace, workspaceFromRoot(temporary)),
            Console.withConsole({
              ...currentConsole,
              log: () => Effect.void
            })
          )
        )
        expect(selectedReport.valid).toBe(false)

        yield* fs.writeFileString(
          path.join(temporary, "ontology/beta/graph.json"),
          JSON.stringify({
            ...graphFixture("beta"),
            nodes: graphFixture("beta").nodes.filter(
              ({ type }) => type !== "artifact"
            ),
            edges: graphFixture("beta").edges.filter(
              ({ id }) => id !== "edge:003"
            )
          })
        )
        const unknown = yield* ontologyShowCommand(
          "claim:SHARED",
          false,
          "missing"
        ).pipe(
          Effect.provideService(Workspace, workspaceFromRoot(temporary)),
          Effect.either
        )
        expect(unknown._tag).toBe("Left")
        if (unknown._tag === "Left") {
          expect(unknown.left.code).toBe("ONTOLOGY_GRAPH_NOT_FOUND")
        }
        const conflict = yield* ontologyShowCommand(
          "beta::claim:SHARED",
          false,
          "alpha"
        ).pipe(
          Effect.provideService(Workspace, workspaceFromRoot(temporary)),
          Effect.either
        )
        expect(conflict._tag).toBe("Left")
        if (conflict._tag === "Left") {
          expect(conflict.left.code).toBe(
            "ONTOLOGY_GRAPH_SELECTOR_CONFLICT"
          )
        }
      })
    )
  )

  it.effect("serves read queries without opening hash-tracked artifacts", () =>
    Effect.scoped(
      Effect.gen(function* () {
        const fs = yield* FileSystem.FileSystem
        const path = yield* Path.Path
        const temporary = yield* fs.makeTempDirectoryScoped({
          prefix: "ice-ontology-structural-query-"
        })
        for (const directory of [
          "ontology/alpha",
          "ontology/beta",
          "research/alpha",
          "research/beta"
        ]) {
          yield* fs.makeDirectory(path.join(temporary, directory), {
            recursive: true
          })
        }
        yield* fs.writeFileString(
          path.join(temporary, "ontology/collection.json"),
          JSON.stringify(collectionFixture())
        )
        for (const key of ["alpha", "beta"] as const) {
          yield* fs.writeFileString(
            path.join(temporary, `ontology/${key}/README.md`),
            `# ${key}\n`
          )
          yield* fs.writeFileString(
            path.join(temporary, `ontology/${key}/graph.json`),
            JSON.stringify(graphFixture(key))
          )
        }

        const result = yield* Console.consoleWith((currentConsole) =>
          ontologyShowCommand("alpha::claim:SHARED", false, "all").pipe(
            Effect.provideService(Workspace, workspaceFromRoot(temporary)),
            Console.withConsole({
              ...currentConsole,
              log: () => Effect.void
            }),
            Effect.either
          )
        )
        expect(result._tag).toBe("Right")
      })
    )
  )

  it.effect("loads every registered graph and verifies all tracked hashes", () =>
    Effect.gen(function* () {
      const collection = yield* loadResearchCollection
      const loaded = yield* loadOntologyCollectionValidation

      expect(loaded.validation.valid).toBe(true)
      expect(loaded.validation.errors).toEqual([])
      expect(loaded.graphs).toHaveLength(collection.graphs.length)
      expect(loaded.validation.counts.verified_hashes).toBe(
        loaded.validation.counts.hash_bearing_nodes
      )
      expect(loaded.graphs.map(({ descriptor }) => descriptor.key)).toEqual(
        collection.graphs.map(({ key }) => key)
      )
    })
  )
})
