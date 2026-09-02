import { NodeContext } from "@effect/platform-node"
import * as FileSystem from "@effect/platform/FileSystem"
import * as Path from "@effect/platform/Path"
import { expect, it, layer } from "@effect/vitest"
import { Effect, Layer } from "effect"
import { createHash } from "node:crypto"
import {
  makeValidationReport,
  resolveNode,
  summarizeGraph,
  traceGraph,
  validateGraphSemantics
} from "../src/ontology/core.ts"
import {
  decodeResearchGraph,
  type ResearchEdge,
  type ResearchGraph,
  type ResearchNode
} from "../src/ontology/model.ts"
import {
  auditEvidenceSnapshots,
  auditHashBearingFiles,
  loadOntologyValidation,
  loadResearchGraph
} from "../src/ontology/repository.ts"
import {
  decodeResearchRunEvidence,
  validateEvidenceSnapshot
} from "../src/ontology/run-evidence.ts"
import {
  Workspace,
  WorkspaceLive,
  workspaceFromRoot
} from "../src/workspace.ts"

const fixture = () => ({
  $schema: "../schema/research-graph-v1.schema.json",
  schema_version: "research-graph/v1",
  graph_id: "research-graph:test",
  title: "Test graph",
  description: "Small ontology fixture",
  updated_at_utc: "2026-08-16T00:00:00Z",
  canonical_file: "ontology/test/graph.json",
  source_inventory: "ontology/test/sources.md",
  quick_answers: [
    {
      question: "Does the claim hold?",
      answer: "Yes in the fixture.",
      claim_ids: ["claim:TEST_CLAIM"]
    }
  ],
  reading_paths: [
    {
      id: "reading-path:test",
      title: "Fixture path",
      summary: "Claim to evidence",
      nodes: ["claim:TEST_CLAIM", "evidence:test"]
    }
  ],
  node_type_legend: {
    claim: "claim",
    evidence: "evidence",
    artifact: "artifact"
  },
  relation_legend: {
    HAS_EVIDENCE: "claim evidence relation"
  },
  nodes: [
    {
      id: "claim:TEST_CLAIM",
      type: "claim",
      title: "Test claim",
      summary: "Supported fixture claim",
      state: "SUPPORTED",
      claim_id: "TEST_CLAIM",
      statement: "The fixture claim holds.",
      epistemic_state: "SUPPORTED"
    },
    {
      id: "evidence:test",
      type: "evidence",
      title: "Test evidence",
      summary: "One exact fixture check",
      state: "VERIFIED",
      observed_status: "1_PASS",
      check_ids: ["TEST.check"]
    },
    {
      id: "artifact:test",
      type: "artifact",
      title: "Test artifact",
      summary: "Fixture artifact",
      state: "TRACKED",
      artifact_kind: "result",
      path: "fixtures/result.json",
      sha256: "0".repeat(64)
    }
  ],
  edges: [
    {
      id: "edge:001",
      from: "claim:TEST_CLAIM",
      relation: "HAS_EVIDENCE",
      to: "evidence:test",
      polarity: "SUPPORTS"
    }
  ],
  kg_bridges: [
    {
      local_node_id: "claim:TEST_CLAIM",
      system: "EXTERNAL",
      external_uid: null,
      relation: null,
      status: "UNRESOLVED",
      lookup_key: "TEST_CLAIM",
      checked_at_utc: "2026-08-16T00:00:00Z"
    }
  ]
})

const evidenceFixture = () => {
  const base = fixture()
  return {
    ...base,
    relation_legend: {
      ...base.relation_legend,
      RECORDED_IN: "evidence group recorded in snapshot"
    },
    nodes: base.nodes.map((node) =>
      node.id === "evidence:test"
        ? { ...node, check_ids: ["P16.check"] }
        : node.id === "artifact:test"
          ? { ...node, artifact_kind: "evidence" }
          : node
    ),
    edges: [
      ...base.edges,
      {
        id: "edge:002",
        from: "evidence:test",
        relation: "RECORDED_IN",
        to: "artifact:test"
      }
    ]
  }
}

const runEvidenceFixture = () => ({
  $schema: "../../schema/research-run-evidence-v1.schema.json",
  schema_version: "research-run-evidence/v1",
  result_id: "result:P16-test",
  phase: "P16",
  observed_at_utc: "2026-08-16T00:00:00Z",
  command: "python3 fixture.py --json",
  exit_code: 0,
  script: {
    path: "fixture.py",
    sha256: "0".repeat(64),
    introduced_in_commit: "0".repeat(40)
  },
  exact_checks: 1,
  checks: [
    {
      id: "P16.check",
      status: "PASS",
      statement: "The fixture check passed."
    }
  ],
  payload: {
    exact_checks: 1,
    phase_specific_detail: { retained: true }
  }
})

it.effect("decodes the discriminated v1 schema and rejects schema drift", () =>
  Effect.gen(function* () {
    const source = JSON.stringify(fixture())
    const graph = yield* decodeResearchGraph(source, "fixture")
    expect(graph.schema_version).toBe("research-graph/v1")

    const base = fixture()
    const motivatesGraph = yield* decodeResearchGraph(
      JSON.stringify({
        ...base,
        relation_legend: {
          ...base.relation_legend,
          MOTIVATES: "terminal result to distinct follow-up"
        },
        edges: [
          ...base.edges,
          {
            id: "edge:002",
            from: "claim:TEST_CLAIM",
            relation: "MOTIVATES",
            to: "artifact:test"
          }
        ]
      }),
      "MOTIVATES fixture"
    )
    expect(motivatesGraph.edges.some((edge) => edge.relation === "MOTIVATES"))
      .toBe(true)

    const missingEvidenceStatus = source.replace(
      '"observed_status":"1_PASS",',
      ""
    )
    const missingResult = yield* decodeResearchGraph(
      missingEvidenceStatus,
      "missing status"
    ).pipe(Effect.either)
    expect(missingResult._tag).toBe("Left")

    const unknownRelation = source.replace(
      '"relation":"HAS_EVIDENCE"',
      '"relation":"EVIDENCE_FOR"'
    )
    const relationResult = yield* decodeResearchGraph(
      unknownRelation,
      "unknown relation"
    ).pipe(Effect.either)
    expect(relationResult._tag).toBe("Left")
  })
)

it.effect("decodes compact research-run-evidence/v1 snapshots strictly", () =>
  Effect.gen(function* () {
    const snapshot = yield* decodeResearchRunEvidence(
      JSON.stringify(runEvidenceFixture()),
      "snapshot fixture"
    )
    expect(snapshot.payload.exact_checks).toBe(1)
    expect(snapshot.payload.phase_specific_detail).toEqual({ retained: true })

    const raw = runEvidenceFixture()
    const invalid = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        payload: { phase_specific_detail: true }
      }),
      "missing payload count"
    ).pipe(Effect.either)
    expect(invalid._tag).toBe("Left")

    const numerical = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        numerical_checks: 1,
        numerical: [
          {
            id: "P16.numeric.control",
            status: "PASS",
            statement: "The bounded numerical control passed."
          }
        ],
        payload: {
          ...raw.payload,
          numerical_checks: 1
        }
      }),
      "typed numerical fixture"
    )
    expect(numerical.numerical_checks).toBe(1)
    expect(numerical.numerical?.map((check) => check.id)).toEqual([
      "P16.numeric.control"
    ])

    const unnumbered = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        result_id: "result:rawc-unnumbered-fixture",
        phase: null,
        checks: [
          {
            id: "rawc.unnumbered.control",
            status: "PASS",
            statement: "The independent unnumbered control passed."
          }
        ]
      }),
      "unnumbered fixture"
    )
    expect(unnumbered.phase).toBeNull()
    expect(unnumbered.checks.map((check) => check.id)).toEqual([
      "rawc.unnumbered.control"
    ])

    const invalidPhaseAlias = yield* decodeResearchRunEvidence(
      JSON.stringify({ ...raw, phase: "UNNUMBERED" }),
      "invalid unnumbered phase alias"
    ).pipe(Effect.either)
    expect(invalidPhaseAlias._tag).toBe("Left")

    const invalidSemanticCheck = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        phase: null,
        checks: [{ ...raw.checks[0], id: "rawc..control" }]
      }),
      "invalid semantic check id"
    ).pipe(Effect.either)
    expect(invalidSemanticCheck._tag).toBe("Left")
  })
)

it.effect("cross-checks snapshot counts, uniqueness, and graph evidence groups", () =>
  Effect.gen(function* () {
    const graph = yield* decodeResearchGraph(
      JSON.stringify(evidenceFixture()),
      "evidence graph fixture"
    )
    const artifact = graph.nodes.find(
      (node) => node.type === "artifact" && node.id === "artifact:test"
    )
    if (artifact === undefined || artifact.type !== "artifact") {
      return yield* Effect.fail(new Error("fixture evidence artifact is missing"))
    }

    const valid = yield* decodeResearchRunEvidence(
      JSON.stringify(runEvidenceFixture()),
      "valid evidence fixture"
    )
    expect(validateEvidenceSnapshot(graph, artifact, valid)).toEqual([])

    const unnumberedAliasCodes = validateEvidenceSnapshot(graph, artifact, {
      ...valid,
      phase: null
    }).map((entry) => entry.code)
    expect(unnumberedAliasCodes).toContain(
      "EVIDENCE_UNNUMBERED_CHECK_ID_HAS_PHASE_ALIAS"
    )

    const numberedMismatchCodes = validateEvidenceSnapshot(graph, artifact, {
      ...valid,
      phase: "P17"
    }).map((entry) => entry.code)
    expect(numberedMismatchCodes).toContain(
      "EVIDENCE_NUMBERED_CHECK_ID_PHASE_MISMATCH"
    )

    const raw = runEvidenceFixture()
    const broken = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        exact_checks: 2,
        checks: [
          ...raw.checks,
          {
            id: "P16.check",
            status: "PASS",
            statement: "A duplicate fixture check."
          }
        ],
        payload: { ...raw.payload, exact_checks: 3 }
      }),
      "broken evidence fixture"
    )
    const brokenCodes = validateEvidenceSnapshot(graph, artifact, broken).map(
      (entry) => entry.code
    )
    expect(brokenCodes).toContain("EVIDENCE_PAYLOAD_EXACT_CHECKS_MISMATCH")
    expect(brokenCodes).toContain("EVIDENCE_DUPLICATE_CHECK_ID")

    const countMismatch = yield* decodeResearchRunEvidence(
      JSON.stringify({ ...raw, exact_checks: 2 }),
      "count mismatch fixture"
    )
    expect(
      validateEvidenceSnapshot(graph, artifact, countMismatch).map(
        (entry) => entry.code
      )
    ).toContain("EVIDENCE_EXACT_CHECKS_MISMATCH")

    const incompleteNumerical = yield* decodeResearchRunEvidence(
      JSON.stringify({ ...raw, numerical_checks: 1 }),
      "incomplete numerical fixture"
    )
    expect(
      validateEvidenceSnapshot(graph, artifact, incompleteNumerical).map(
        (entry) => entry.code
      )
    ).toContain("EVIDENCE_NUMERICAL_LEDGER_INCOMPLETE")

    const mismatchedNumerical = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        numerical_checks: 2,
        numerical: [
          {
            id: "P16.numeric.control",
            status: "PASS",
            statement: "One numerical check."
          }
        ],
        payload: { ...raw.payload, numerical_checks: 3 }
      }),
      "mismatched numerical fixture"
    )
    const numericalCodes = validateEvidenceSnapshot(
      graph,
      artifact,
      mismatchedNumerical
    ).map((entry) => entry.code)
    expect(numericalCodes).toContain("EVIDENCE_NUMERICAL_CHECKS_MISMATCH")
    expect(numericalCodes).toContain(
      "EVIDENCE_PAYLOAD_NUMERICAL_CHECKS_MISMATCH"
    )

    const otherCheck = yield* decodeResearchRunEvidence(
      JSON.stringify({
        ...raw,
        checks: [
          {
            id: "P16.other",
            status: "PASS",
            statement: "A check absent from the graph group."
          }
        ]
      }),
      "membership mismatch fixture"
    )
    expect(
      validateEvidenceSnapshot(graph, artifact, otherCheck).map(
        (entry) => entry.code
      )
    ).toContain("EVIDENCE_CHECK_IDS_MISMATCH")
  })
)

it.effect("allows unresolved external bridges as explicit warnings", () =>
  Effect.gen(function* () {
    const graph = yield* decodeResearchGraph(JSON.stringify(fixture()), "fixture")
    const report = makeValidationReport(graph, validateGraphSemantics(graph))
    expect(report.valid).toBe(true)
    expect(report.errors).toHaveLength(0)
    expect(report.warnings.map((issue) => issue.code)).toEqual([
      "EXTERNAL_BRIDGE_UNRESOLVED"
    ])
  })
)

it.effect("requires every weak component to contain a programme when present", () =>
  Effect.gen(function* () {
    const graph = yield* decodeResearchGraph(JSON.stringify(fixture()), "fixture")
    const programme: ResearchNode = {
      id: "programme:test",
      type: "programme",
      title: "Fixture programme",
      summary: "Programme anchor for the fixture.",
      state: "ACTIVE"
    }
    const partiallyConnected: ResearchGraph = {
      ...graph,
      node_type_legend: { ...graph.node_type_legend, programme: "programme" },
      relation_legend: { ...graph.relation_legend, PART_OF: "programme membership" },
      nodes: [...graph.nodes, programme],
      edges: [
        ...graph.edges,
        {
          id: "edge:002",
          from: "claim:TEST_CLAIM",
          relation: "PART_OF",
          to: "programme:test"
        }
      ]
    }
    const partialIssues = validateGraphSemantics(partiallyConnected)
    expect(
      partialIssues.filter(
        (issue) => issue.code === "GRAPH_COMPONENT_WITHOUT_PROGRAMME"
      )
    ).toMatchObject([{ subject: "artifact:test" }])

    const connected: ResearchGraph = {
      ...partiallyConnected,
      edges: [
        ...partiallyConnected.edges,
        {
          id: "edge:003",
          from: "artifact:test",
          relation: "PART_OF",
          to: "programme:test"
        }
      ]
    }
    const validation = makeValidationReport(
      connected,
      validateGraphSemantics(connected)
    )
    expect(validation.errors).toHaveLength(0)
    expect(summarizeGraph(connected, validation)).toMatchObject({
      weak_component_count: 1,
      nodes_outside_programme_components: 0
    })

    const noProgrammeValidation = makeValidationReport(
      graph,
      validateGraphSemantics(graph)
    )
    expect(summarizeGraph(graph, noProgrammeValidation)).toMatchObject({
      weak_component_count: 2,
      nodes_outside_programme_components: 0
    })
  })
)

it.effect("detects duplicate IDs, broken endpoints, unsafe paths, and polarity drift", () =>
  Effect.gen(function* () {
    const graph = yield* decodeResearchGraph(JSON.stringify(fixture()), "fixture")
    const firstNode = graph.nodes.find((node) => node.id === "claim:TEST_CLAIM")
    const firstEdge = graph.edges.find((edge) => edge.id === "edge:001")
    if (firstNode === undefined || firstEdge === undefined) {
      return yield* Effect.fail(new Error("fixture entries are missing"))
    }

    const brokenNodes: ReadonlyArray<ResearchNode> = graph.nodes.map((node) =>
      node.type === "artifact" ? { ...node, path: "../outside.json" } : node
    )
    const mismatchedEdge: ResearchEdge = {
      ...firstEdge,
      id: "edge:002",
      to: "claim:missing",
      polarity: "CONTRADICTS"
    }
    const broken: ResearchGraph = {
      ...graph,
      nodes: [...brokenNodes, firstNode],
      edges: [...graph.edges, firstEdge, mismatchedEdge]
    }
    const codes = validateGraphSemantics(broken).map((issue) => issue.code)

    expect(codes).toContain("DUPLICATE_NODE_ID")
    expect(codes).toContain("DUPLICATE_EDGE_ID")
    expect(codes).toContain("EDGE_TO_NOT_FOUND")
    expect(codes).toContain("HASHED_PATH_UNSAFE")
    expect(codes).toContain("EVIDENCE_POLARITY_STATE_MISMATCH")
  })
)

it.effect("resolves bare claim IDs and bounds an undirected trace by depth", () =>
  Effect.gen(function* () {
    const graph = yield* decodeResearchGraph(JSON.stringify(fixture()), "fixture")
    const root = resolveNode(graph, "TEST_CLAIM")
    expect(root?.id).toBe("claim:TEST_CLAIM")
    if (root === undefined) {
      return yield* Effect.fail(new Error("fixture claim is missing"))
    }

    const rootOnly = traceGraph(graph, root, 0)
    expect(rootOnly.nodes.map(({ node }) => node.id)).toEqual([
      "claim:TEST_CLAIM"
    ])
    expect(rootOnly.edges).toHaveLength(0)

    const oneHop = traceGraph(graph, root, 1)
    expect(oneHop.nodes.map(({ node }) => node.id)).toEqual([
      "claim:TEST_CLAIM",
      "evidence:test"
    ])
    expect(oneHop.edges.map((edge) => edge.id)).toEqual(["edge:001"])
  })
)

const AppLayer = Layer.mergeAll(NodeContext.layer, WorkspaceLive)

layer(AppLayer)("canonical ontology", (it) => {
  it.effect("passes semantic validation and verifies every file hash", () =>
    Effect.gen(function* () {
      const { validation } = yield* loadOntologyValidation
      const graph = yield* loadResearchGraph
      expect(validation.valid).toBe(true)
      expect(validation.errors).toHaveLength(0)
      expect(validation.counts.verified_hashes).toBe(
        validation.counts.hash_bearing_nodes
      )
      expect(validation.warnings).toHaveLength(
        graph.kg_bridges.filter((bridge) => bridge.status === "UNRESOLVED")
          .length
      )
      expect(
        validation.warnings.every(
          (issue) => issue.code === "EXTERNAL_BRIDGE_UNRESOLVED"
        )
      ).toBe(true)
    })
  )

  it.effect("keeps the raw-C handoff ordered, typed, and separate from G1", () =>
    Effect.gen(function* () {
      const graph = yield* loadResearchGraph
      const blockerChain = [
        [
          "open:raw-c-fixed-box-nonreal-endpoint-certificate",
          "open:raw-c-p0-complex-tail-theorem-prerequisite"
        ],
        [
          "open:raw-c-nonzero-p-uniform-weyl-field",
          "open:raw-c-fixed-box-nonreal-endpoint-certificate"
        ],
        [
          "open:raw-c-fiber-spectral-measure-transform",
          "open:raw-c-nonzero-p-uniform-weyl-field"
        ],
        [
          "open:raw-c-p-zero-threshold-global-spectral-assembly",
          "open:raw-c-fiber-spectral-measure-transform"
        ],
        [
          "open:raw-c-raq-rigging-map-physical-product",
          "open:raw-c-p-zero-threshold-global-spectral-assembly"
        ],
        [
          "open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion",
          "open:raw-c-raq-rigging-map-physical-product"
        ]
      ] as const

      for (const [downstream, prerequisite] of blockerChain) {
        expect(
          graph.nodes.find((node) => node.id === downstream)?.type
        ).toBe("open_problem")
        expect(
          graph.nodes.find((node) => node.id === prerequisite)?.type
        ).toBe("open_problem")
        expect(
          graph.edges.some(
            (edge) =>
              edge.from === downstream &&
              edge.relation === "BLOCKED_BY" &&
              edge.to === prerequisite
          )
        ).toBe(true)
      }

      const handoff = graph.reading_paths.find(
        (path) => path.id === "reading-path:raw-c-next-bounded-work"
      )
      expect(handoff?.nodes.slice(0, 2)).toEqual([
        "policy:toe-directed-critical-path-routing",
        "open:gate1-original-cycle-signed-global-intersections"
      ])
      expect(handoff?.nodes).toContain(
        "open:gate1-v0-raw-c-differentiated-tail-node-safe-transport"
      )
      expect(handoff?.nodes.slice(-7)).toEqual([
        "open:raw-c-p0-complex-tail-theorem-prerequisite",
        "open:raw-c-fixed-box-nonreal-endpoint-certificate",
        "open:raw-c-nonzero-p-uniform-weyl-field",
        "open:raw-c-fiber-spectral-measure-transform",
        "open:raw-c-p-zero-threshold-global-spectral-assembly",
        "open:raw-c-raq-rigging-map-physical-product",
        "open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion"
      ])

      const supportingNodes = new Set<string>([
        "open:gate1-v0-raw-c-differentiated-tail-node-safe-transport",
        ...blockerChain.flat()
      ])
      const g1 = "open:gate1-original-cycle-signed-global-intersections"
      expect(
        graph.edges.filter(
          (edge) =>
            (supportingNodes.has(edge.from) && edge.to === g1) ||
            (edge.from === g1 && supportingNodes.has(edge.to))
        )
      ).toEqual([])
      expect(
        graph.edges.some(
          (edge) =>
            edge.from ===
              "artifact:raw-c-nonreal-endpoint-interval-certificate-blocker" &&
            edge.relation === "DOCUMENTS" &&
            edge.to === "open:raw-c-p0-complex-tail-theorem-prerequisite"
        )
      ).toBe(true)

      expect(
        graph.reading_paths.find(
          ({ id }) => id === "reading-path:g1-typed-object-handoff"
        )?.nodes
      ).toEqual([
        "policy:toe-directed-critical-path-routing",
        "open:p38-explicit-joint-action-cycle-and-oriented-intersections",
        "open:gate1-phase-locked-fiber-to-source-derived-joint-cycle",
        "open:gate1-original-cycle-signed-global-intersections",
        "open:gate2-hard-cfu-airy-coefficients"
      ])
      expect(
        graph.reading_paths.find(
          ({ id }) => id === "reading-path:p1-exact-real-root-handoff"
        )?.nodes
      ).toHaveLength(4)
      expect(
        graph.reading_paths.find(
          ({ id }) => id === "reading-path:p4-weyl-measure-raq-handoff"
        )?.nodes.slice(1)
      ).toEqual([
        "open:raw-c-p0-complex-tail-theorem-prerequisite",
        "open:raw-c-fixed-box-nonreal-endpoint-certificate",
        "open:raw-c-nonzero-p-uniform-weyl-field",
        "open:raw-c-fiber-spectral-measure-transform",
        "open:raw-c-p-zero-threshold-global-spectral-assembly",
        "open:raw-c-raq-rigging-map-physical-product",
        "open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion"
      ])
    })
  )

  it.effect("keeps the choice-invariance promotion lens policy-only and navigation-only", () =>
    Effect.gen(function* () {
      const graph = yield* loadResearchGraph
      const policyId = "policy:choice-invariance-cross-domain-promotion"
      const policy = graph.nodes.find(({ id }) => id === policyId)
      const path = graph.reading_paths.find(
        ({ id }) => id === "reading-path:choice-invariance-to-observable-promotion-audit"
      )
      const answer = graph.quick_answers.find(
        ({ question }) =>
          question ===
          "이 효과는 어떤 선택을 바꿔도 남으며, 다른 관측 영역에서도 같은 이유로 나타나는가?"
      )

      expect(policy).toMatchObject({
        type: "policy",
        state: "ACTIVE_REPOSITORY_WIDE_PROMOTION_BOUNDARY_NON_EVIDENCE",
        path: "docs/decisions/ICE_CHOICE_INVARIANCE_CROSS_DOMAIN_PROMOTION_2026-09-02.md"
      })
      expect(
        graph.edges.some(
          ({ from, relation, to }) =>
            from === "programme:cpt-temporal-folded-susy" &&
            relation === "GOVERNED_BY" &&
            to === policyId
        )
      ).toBe(true)
      expect(path?.nodes).toHaveLength(12)
      expect(path?.nodes.slice(0, 6)).toEqual([
        policyId,
        "open:gate1-original-cycle-signed-global-intersections",
        "open:gate2-hard-cfu-airy-coefficients",
        "open:gate3-full-bfv-pfaffian-pin-holonomy",
        "open:gate4-spinorial-charge-domain-constraint-closure",
        "open:gate5-persistent-order-and-pole-splitting"
      ])
      expect(path?.summary).toContain("no present result passes at physics scope")
      expect(answer?.answer).toContain("아직 model/physics scope에서 두 조건을 모두 통과한 CPT 결과는 없다")
      expect(
        graph.edges.some(
          ({ from, relation, to }) =>
            (from === policyId || to === policyId) && relation === "HAS_EVIDENCE"
        )
      ).toBe(false)
    })
  )

  it.effect("audits every graph-registered evidence snapshot", () =>
    Effect.gen(function* () {
      const graph = yield* loadResearchGraph
      const audit = yield* auditEvidenceSnapshots(graph)
      const evidenceArtifacts = graph.nodes.filter(
        (node) => node.type === "artifact" && node.artifact_kind === "evidence"
      )
      expect(audit.audited).toBe(evidenceArtifacts.length)
      expect(audit.issues).toEqual([])
      expect(
        graph.nodes.find((node) => node.id === "artifact:p15r-run-result")
          ?.artifact_kind
      ).toBe("result")
    })
  )

  it.effect("rejects a snapshot when its recorded runner hash drifts", () =>
    Effect.scoped(
      Effect.gen(function* () {
        const fs = yield* FileSystem.FileSystem
        const path = yield* Path.Path
        const temporary = yield* fs.makeTempDirectoryScoped({
          prefix: "ice-ontology-script-hash-"
        })
        yield* fs.makeDirectory(path.join(temporary, "evidence"), {
          recursive: true
        })
        yield* fs.makeDirectory(path.join(temporary, "scripts"), {
          recursive: true
        })

        const runner = "print('fixture')\n"
        const runnerHash = createHash("sha256").update(runner).digest("hex")
        yield* fs.writeFileString(
          path.join(temporary, "scripts/runner.py"),
          runner
        )

        const rawGraph = evidenceFixture()
        const graph = yield* decodeResearchGraph(
          JSON.stringify({
            ...rawGraph,
            nodes: rawGraph.nodes.map((node) =>
              node.id === "artifact:test"
                ? { ...node, path: "evidence/snapshot.json" }
                : node
            )
          }),
          "runner hash graph fixture"
        )
        yield* fs.writeFileString(
          path.join(temporary, "evidence/snapshot.json"),
          JSON.stringify({
            ...runEvidenceFixture(),
            script: {
              ...runEvidenceFixture().script,
              path: "scripts/runner.py",
              sha256: runnerHash
            }
          })
        )

        const provideWorkspace = <A, E, R>(effect: Effect.Effect<A, E, R>) =>
          effect.pipe(
            Effect.provideService(Workspace, workspaceFromRoot(temporary))
          )
        const initial = yield* provideWorkspace(auditEvidenceSnapshots(graph))
        expect(initial.issues).toEqual([])

        yield* fs.writeFileString(
          path.join(temporary, "scripts/runner.py"),
          "print('drifted')\n"
        )
        const drifted = yield* provideWorkspace(auditEvidenceSnapshots(graph))
        expect(drifted.issues.map(({ code }) => code)).toContain(
          "EVIDENCE_SCRIPT_HASH_MISMATCH"
        )
      })
    )
  )

  it.effect("reports content hash mismatches against real files", () =>
    Effect.gen(function* () {
      const graph = yield* loadResearchGraph
      const changedNodes: ReadonlyArray<ResearchNode> = graph.nodes.map((node) =>
        node.type === "artifact" || node.type === "policy"
          ? { ...node, sha256: "0".repeat(64) }
          : node
      )
      const changed: ResearchGraph = { ...graph, nodes: changedNodes }
      const audit = yield* auditHashBearingFiles(changed)
      expect(audit.verified).toBe(0)
      expect(audit.issues).toHaveLength(
        graph.nodes.filter(
          (node) => node.type === "artifact" || node.type === "policy"
        ).length
      )
      expect(
        audit.issues.every((issue) => issue.code === "HASH_MISMATCH")
      ).toBe(true)
    })
  )
})
