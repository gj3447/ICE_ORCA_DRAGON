import type {
  GraphRagSearchResult,
  GraphRagTextUnit
} from "../graphrag/core.ts"

type GateId = "G1" | "G2" | "G3" | "G4" | "G5"

interface GateRoute {
  readonly id: GateId
  readonly anchor_open_problem_id: string
  readonly prerequisites: ReadonlyArray<GateId>
  readonly question_selectors: ReadonlyArray<string>
}

interface SupportingLane {
  readonly id: "P1" | "P2_P3" | "P4" | "P5" | "P6" | "P7"
  readonly anchor_open_problem_ids: ReadonlyArray<string>
  readonly possible_consumer_gate_ids: ReadonlyArray<GateId | "TERMINAL_REVIEW">
  readonly question_selectors: ReadonlyArray<string>
}

const gateOneRoute: GateRoute = {
  id: "G1",
  anchor_open_problem_id: "open:gate1-original-cycle-signed-global-intersections",
  prerequisites: [],
  question_selectors: [
    "gate 1",
    "gate1",
    "joint cycle",
    "original cycle",
    "relative cycle",
    "signed intersection",
    "global intersection",
    "intersection vector",
    "orientation stable",
    "stokes census",
    "good end",
    "원래 사이클",
    "공동 사이클",
    "전역 교차",
    "부호 교차"
  ]
}

const gates: ReadonlyArray<GateRoute> = [
  gateOneRoute,
  {
    id: "G2",
    anchor_open_problem_id: "open:gate2-hard-cfu-airy-coefficients",
    prerequisites: ["G1"],
    question_selectors: [
      "gate 2",
      "gate2",
      "hard cfu",
      "airy coefficient",
      "airy-prime",
      "uniform kernel"
    ]
  },
  {
    id: "G3",
    anchor_open_problem_id: "open:gate3-full-bfv-pfaffian-pin-holonomy",
    prerequisites: ["G1", "G2"],
    question_selectors: [
      "gate 3",
      "gate3",
      "full bfv",
      "pfaffian line",
      "pin holonomy",
      "physical determinant"
    ]
  },
  {
    id: "G4",
    anchor_open_problem_id: "open:gate4-spinorial-charge-domain-constraint-closure",
    prerequisites: ["G1", "G2", "G3"],
    question_selectors: [
      "gate 4",
      "gate4",
      "spinorial charge",
      "common domain",
      "constraint closure",
      "anomaly free",
      "positive product"
    ]
  },
  {
    id: "G5",
    anchor_open_problem_id: "open:gate5-persistent-order-and-pole-splitting",
    prerequisites: ["G1", "G2", "G3", "G4"],
    question_selectors: [
      "gate 5",
      "gate5",
      "persistent order",
      "pole splitting",
      "interacting pole",
      "susy breaking"
    ]
  }
]

const supportingLanes: ReadonlyArray<SupportingLane> = [
  {
    id: "P1",
    anchor_open_problem_ids: [
      "open:gate1-v0-raw-c-differentiated-tail-node-safe-transport"
    ],
    possible_consumer_gate_ids: ["G4"],
    question_selectors: [
      "p1",
      "real raw-c",
      "root uniqueness",
      "transversality",
      "c1 selector",
      "root velocity"
    ]
  },
  {
    id: "P2_P3",
    anchor_open_problem_ids: ["open:gate1-v0-classical-s3-hda-closure"],
    possible_consumer_gate_ids: ["G4"],
    question_selectors: [
      "p2",
      "p3",
      "s3 harmonics",
      "svt basis",
      "cubic constraint",
      "hda closure",
      "jacobi closure"
    ]
  },
  {
    id: "P4",
    anchor_open_problem_ids: [
      "open:raw-c-fixed-box-nonreal-endpoint-certificate",
      "open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion"
    ],
    possible_consumer_gate_ids: ["G4"],
    question_selectors: [
      "p4",
      "weyl m",
      "weyl function",
      "spectral measure",
      "singular weyl",
      "nonreal endpoint",
      "raw-c raq"
    ]
  },
  {
    id: "P5",
    anchor_open_problem_ids: [
      "open:gate1-v0-quantum-inhomogeneous-bfv-nilpotency-anomaly"
    ],
    possible_consumer_gate_ids: ["G4"],
    question_selectors: [
      "p5",
      "quantum bfv",
      "common core",
      "nilpotency anomaly",
      "operator anomaly"
    ]
  },
  {
    id: "P6",
    anchor_open_problem_ids: [
      "open:gate1-v0-lapse-modulus-contour-and-absolute-bfv-measure"
    ],
    possible_consumer_gate_ids: ["G1", "G3"],
    question_selectors: [
      "p6",
      "endpoint polarization",
      "absolute bfv measure",
      "two-slab gluing",
      "determinant line",
      "lapse modulus"
    ]
  },
  {
    id: "P7",
    anchor_open_problem_ids: [
      "open:gate1-v0-relational-observables-bo-decoherence",
      "open:gate1-v0-empirical-likelihood-bridge"
    ],
    possible_consumer_gate_ids: ["TERMINAL_REVIEW"],
    question_selectors: [
      "p7",
      "physical clock",
      "normalized state",
      "reheating",
      "likelihood",
      "empirical discriminator"
    ]
  }
]

export const toeNavigationProfile = {
  schema: "ice-toe-navigation-policy/v1",
  profile_id: "cpt-toe-critical-path",
  version: "2026-09-02",
  source_boundary: "NAVIGATION_POLICY_NOT_SCIENTIFIC_EVIDENCE",
  objective: "RESOLVE_DECLARED_CPT_CANDIDATE_ROUTE_TOWARD_TOE",
  objective_status: "USER_DECLARED_NOT_ESTABLISHED",
  completion_label: "TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW",
  scope_graph: "cpt",
  current_blocker_gate_id: "G1",
  gates,
  supporting_lanes: supportingLanes,
  terminal_review_criteria: [
    "compatible independently supported G1-G5 typed outputs in one declared model scope",
    "full 3+1 local modes and arbitrary-background constraint algebra",
    "regulator-independent continuum limit or explicit UV completion",
    "positive physical states with unitary and causal dynamics",
    "general-relativity and quantum-field-theory low-energy recovery",
    "normalized convention-stable observables with an independent discriminator",
    "explicit data likelihood and independent reproducibility review"
  ]
} as const

export type ToeRouteClassification =
  | "CURRENT_BLOCKER_CANDIDATE"
  | "DOWNSTREAM_BLOCKED"
  | "SUPPORTING_ONLY"
  | "PROFILE_SCOPE_MISMATCH"
  | "INSUFFICIENT_ROUTE_EVIDENCE"

export const promotionBoundaryPolicyNodeId =
  "policy:choice-invariance-cross-domain-promotion" as const

export const promotionBoundaryCanonicalQuestion =
  "이 효과는 어떤 선택을 바꿔도 남으며, 다른 관측 영역에서도 같은 이유로 나타나는가?" as const

/**
 * A stable human-review boundary for broader interpretation.  It is emitted
 * with every route, including a current G1 candidate, so route selection can
 * never itself be mistaken for a discovery or promotion decision.
 */
export interface PromotionBoundary {
  readonly policy_node_id: typeof promotionBoundaryPolicyNodeId
  readonly canonical_question: typeof promotionBoundaryCanonicalQuestion
  readonly interpretation: "BROADER_INTERPRETATION_ONLY"
  readonly review_status: "HUMAN_REVIEW_REQUIRED"
  readonly selection_family: "REQUIRED"
  readonly mechanism_typed_object: "REQUIRED"
  readonly invariance_null: "REQUIRED"
  readonly independent_checks: "REQUIRED"
  readonly false_signal_control: "REQUIRED"
  readonly two_in_graph_consumers: {
    readonly minimum: 2
    readonly scope: "IN_GRAPH_ONLY"
    readonly status: "REQUIRED"
  }
  readonly cross_graph_evidence: "PROHIBITED"
  readonly passed: false
  readonly nonpass_disposition: "STAY_SCOPED_OR_STOP"
}

export const promotionBoundary: PromotionBoundary = {
  policy_node_id: promotionBoundaryPolicyNodeId,
  canonical_question: promotionBoundaryCanonicalQuestion,
  interpretation: "BROADER_INTERPRETATION_ONLY",
  review_status: "HUMAN_REVIEW_REQUIRED",
  selection_family: "REQUIRED",
  mechanism_typed_object: "REQUIRED",
  invariance_null: "REQUIRED",
  independent_checks: "REQUIRED",
  false_signal_control: "REQUIRED",
  two_in_graph_consumers: {
    minimum: 2,
    scope: "IN_GRAPH_ONLY",
    status: "REQUIRED"
  },
  cross_graph_evidence: "PROHIBITED",
  passed: false,
  nonpass_disposition: "STAY_SCOPED_OR_STOP"
}

export interface ToeObjectiveRouting {
  readonly schema: "ice-toe-objective-routing/v1"
  readonly profile: {
    readonly id: string
    readonly version: string
    readonly source_boundary: string
  }
  readonly objective: {
    readonly name: string
    readonly status: "USER_DECLARED_NOT_ESTABLISHED"
    readonly completion_label: "TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW"
  }
  readonly classification: ToeRouteClassification
  readonly selected_lane_id: string | null
  readonly candidate_lane_ids: ReadonlyArray<string>
  readonly selected_anchor_open_problem_ids: ReadonlyArray<string>
  readonly retrieved_anchor_ids: ReadonlyArray<string>
  readonly matched_question_terms: ReadonlyArray<string>
  readonly required_prerequisite_gate_ids: ReadonlyArray<GateId>
  readonly prerequisite_status: "ACTIVE_PROFILE_REQUIRES_HUMAN_GRAPH_REVIEW"
  readonly current_blocker: {
    readonly gate_id: "G1"
    readonly anchor_open_problem_id: string
  }
  readonly critical_path_gate_ids: ReadonlyArray<GateId>
  readonly terminal_review_criteria: ReadonlyArray<string>
  readonly promotion_boundary: PromotionBoundary
  readonly core_progress_eligibility: "HUMAN_REVIEW_REQUIRED" | "NOT_ELIGIBLE"
  readonly decision: "REVIEW_CURRENT_BLOCKER" | "STOP_OR_REFRAME"
  readonly anti_meandering: {
    readonly passed: boolean
    readonly checks: ReadonlyArray<{
      readonly id: string
      readonly passed: boolean
      readonly detail: string
    }>
  }
  readonly reasons: ReadonlyArray<string>
}

const normalize = (value: string): string =>
  value
    .normalize("NFKC")
    .toLocaleLowerCase()
    .replace(/[–—]/g, "-")
    .replace(/\s+/g, " ")
    .trim()

const matchedSelectors = (
  normalizedQuestion: string,
  selectors: ReadonlyArray<string>
): ReadonlyArray<string> => {
  const questionTokens = new Set(
    normalizedQuestion.match(/[\p{L}\p{N}_-]+/gu) ?? []
  )
  return selectors.filter((selector) => {
    const normalizedSelector = normalize(selector)
    return normalizedSelector.includes(" ")
      ? normalizedQuestion.includes(normalizedSelector)
      : questionTokens.has(normalizedSelector)
  })
}

const explicitlyNamesAnchor = (
  normalizedQuestion: string,
  anchors: ReadonlyArray<string>
): boolean => anchors.some((anchor) => normalizedQuestion.includes(normalize(anchor)))

const unique = <T>(values: ReadonlyArray<T>): ReadonlyArray<T> => [...new Set(values)]

export interface ToeNavigationProfileValidation {
  readonly schema: "ice-toe-navigation-profile-validation/v1"
  readonly passed: boolean
  readonly checked_anchor_ids: ReadonlyArray<string>
  readonly errors: ReadonlyArray<string>
}

/** Validates the checked-in route profile against a complete GraphRAG index. */
export const validateToeNavigationProfile = (
  units: ReadonlyArray<GraphRagTextUnit>
): ToeNavigationProfileValidation => {
  const errors: string[] = []
  const gateIds = gates.map(({ id }) => id)
  const laneIds = supportingLanes.map(({ id }) => id)
  if (unique(gateIds).length !== gateIds.length) errors.push("gate IDs must be unique")
  if (unique(laneIds).length !== laneIds.length) errors.push("supporting lane IDs must be unique")
  for (const gate of gates) {
    const gateIndex = gateIds.indexOf(gate.id)
    for (const prerequisite of gate.prerequisites) {
      const prerequisiteIndex = gateIds.indexOf(prerequisite)
      if (prerequisiteIndex < 0 || prerequisiteIndex >= gateIndex) {
        errors.push(`${gate.id} prerequisite ${prerequisite} must precede it`)
      }
    }
  }
  const declaredAnchors = [
    ...gates.map(({ anchor_open_problem_id: anchor }) => anchor),
    ...supportingLanes.flatMap(({ anchor_open_problem_ids: laneAnchors }) => laneAnchors)
  ]
  const anchors = unique(declaredAnchors)
  if (anchors.length !== declaredAnchors.length) {
    errors.push("route-profile anchor IDs must be unique")
  }
  for (const anchor of anchors) {
    const matches = units.filter(
      (unit) => unit.graph === toeNavigationProfile.scope_graph && unit.node_id === anchor
    )
    if (matches.length !== 1) {
      errors.push(`${anchor} must resolve exactly once in the CPT graph`)
    } else if (matches[0]?.node_type !== "open_problem") {
      errors.push(`${anchor} must resolve to an open_problem`)
    }
  }
  const current = units.find(
    (unit) =>
      unit.graph === toeNavigationProfile.scope_graph &&
      unit.node_id === gateOneRoute.anchor_open_problem_id
  )
  if (current === undefined || !current.state.startsWith("OPEN")) {
    errors.push("the declared current G1 blocker must exist in an OPEN state")
  }
  const promotionPolicies = units.filter(
    (unit) =>
      unit.graph === toeNavigationProfile.scope_graph &&
      unit.node_id === promotionBoundaryPolicyNodeId
  )
  if (promotionPolicies.length !== 1) {
    errors.push(`${promotionBoundaryPolicyNodeId} must resolve exactly once in the CPT graph`)
  } else if (promotionPolicies[0]?.node_type !== "policy") {
    errors.push(`${promotionBoundaryPolicyNodeId} must resolve to a policy`)
  }
  return {
    schema: "ice-toe-navigation-profile-validation/v1",
    passed: errors.length === 0,
    checked_anchor_ids: anchors,
    errors
  }
}

export const assertToeNavigationProfile = (
  units: ReadonlyArray<GraphRagTextUnit>
): void => {
  const validation = validateToeNavigationProfile(units)
  if (!validation.passed) {
    throw new Error(`invalid TOE navigation profile: ${validation.errors.join("; ")}`)
  }
}

/**
 * Applies a deterministic navigation policy to retrieved graph context.  It
 * does not decide scientific merit: a positive routing result is only a
 * candidate for human review, while every other result stops calculation
 * design until the question is reframed.
 */
export const routeToeObjective = (
  question: string,
  retrieval: GraphRagSearchResult
): ToeObjectiveRouting => {
  const normalizedQuestion = normalize(question)
  const scopeMatches = retrieval.graph === toeNavigationProfile.scope_graph
  const retrievedCptNodeIds = new Set(
    retrieval.hits
      .filter(({ unit }) => unit.graph === toeNavigationProfile.scope_graph)
      .map(({ unit }) => unit.node_id)
  )

  const gateCandidates = gates.map((gate) => {
    const matches = matchedSelectors(normalizedQuestion, gate.question_selectors)
    const retrievedUnit = retrieval.hits.find(
      ({ unit }) =>
        unit.graph === toeNavigationProfile.scope_graph &&
        unit.node_id === gate.anchor_open_problem_id
    )?.unit
    const retrieved = retrievedUnit !== undefined
    const open = retrievedUnit?.node_type === "open_problem" && retrievedUnit.state.startsWith("OPEN")
    const explicit = explicitlyNamesAnchor(normalizedQuestion, [gate.anchor_open_problem_id])
    return {
      gate,
      matches,
      retrieved,
      eligible: retrieved && open && (explicit || matches.length >= 2)
    }
  })
  const supportCandidates = supportingLanes.map((lane) => {
    const matches = matchedSelectors(normalizedQuestion, lane.question_selectors)
    const retrievedAnchors = lane.anchor_open_problem_ids.filter((anchor) =>
      retrieval.hits.some(
        ({ unit }) =>
          unit.graph === toeNavigationProfile.scope_graph &&
          unit.node_id === anchor &&
          unit.node_type === "open_problem" &&
          unit.state.startsWith("OPEN")
      )
    )
    const explicit = explicitlyNamesAnchor(
      normalizedQuestion,
      lane.anchor_open_problem_ids
    )
    return {
      lane,
      matches,
      retrievedAnchors,
      eligible: retrievedAnchors.length > 0 && (explicit || matches.length >= 2)
    }
  })

  const gateOne = gateCandidates.find(({ gate }) => gate.id === "G1")
  const current = scopeMatches && gateOne?.eligible === true ? gateOne : undefined
  const downstream = scopeMatches
    ? gateCandidates.find(({ gate, eligible }) => gate.id !== "G1" && eligible)
    : undefined
  const supporting = scopeMatches
    ? supportCandidates.find(({ eligible }) => eligible)
    : undefined
  const classification: ToeRouteClassification =
    !scopeMatches
      ? "PROFILE_SCOPE_MISMATCH"
      : current !== undefined
      ? "CURRENT_BLOCKER_CANDIDATE"
      : downstream !== undefined
        ? "DOWNSTREAM_BLOCKED"
        : supporting !== undefined
          ? "SUPPORTING_ONLY"
          : "INSUFFICIENT_ROUTE_EVIDENCE"
  const selectedGate = current?.gate ?? downstream?.gate
  const selectedSupport = selectedGate === undefined ? supporting?.lane : undefined
  const selectedAnchors =
    selectedGate === undefined
      ? (selectedSupport?.anchor_open_problem_ids ?? [])
      : [selectedGate.anchor_open_problem_id]
  const retrievedAnchors = selectedAnchors.filter((anchor) =>
    retrievedCptNodeIds.has(anchor)
  )
  const selectedMatches =
    selectedGate === undefined
      ? (supporting?.matches ?? [])
      : (current?.matches ?? downstream?.matches ?? [])
  const candidateLaneIds = unique([
    ...gateCandidates
      .filter(({ matches, retrieved }) => matches.length > 0 || retrieved)
      .map(({ gate }) => gate.id),
    ...supportCandidates
      .filter(({ matches, retrievedAnchors: anchors }) =>
        matches.length > 0 || anchors.length > 0
      )
      .map(({ lane }) => lane.id)
  ])
  const isCurrent = classification === "CURRENT_BLOCKER_CANDIDATE"
  const reasons = isCurrent
    ? [
        "The question and CPT graph retrieval both identify the current G1 blocker.",
        "Human review must still name one missing typed object, one bounded output, and one false-signal control before calculation design."
      ]
    : classification === "DOWNSTREAM_BLOCKED"
      ? [
          "The selected gate is downstream of unresolved claim prerequisites.",
          "Reframe toward the earliest unresolved prerequisite or label the work CONDITIONAL/SUPPORTING_METHOD."
        ]
      : classification === "SUPPORTING_ONLY"
        ? [
            "The selected P-lane is an enabling lane, not an independently advancing TOE gate.",
            "Name the exact typed object and consumer gate it changes, or keep it outside core progress."
          ]
        : classification === "PROFILE_SCOPE_MISMATCH"
          ? [
              "The active TOE route profile is scoped only to the CPT ontology graph.",
              "Run the planner with --graph cpt; other independent graphs require their own human-selected objective."
            ]
        : [
            "The question lacks both a sufficiently specific route description and a retrieved canonical CPT blocker anchor.",
            "Select a canonical open-problem node and state its path to the TOE terminal review criteria."
          ]
  const selectedLaneId = selectedGate?.id ?? selectedSupport?.id ?? null
  const anchorCheck = selectedAnchors.length > 0 && retrievedAnchors.length > 0
  const selectorCheck = explicitlyNamesAnchor(normalizedQuestion, selectedAnchors) || selectedMatches.length >= 2
  const currentBlockerCheck = selectedLaneId === toeNavigationProfile.current_blocker_gate_id

  return {
    schema: "ice-toe-objective-routing/v1",
    profile: {
      id: toeNavigationProfile.profile_id,
      version: toeNavigationProfile.version,
      source_boundary: toeNavigationProfile.source_boundary
    },
    objective: {
      name: toeNavigationProfile.objective,
      status: toeNavigationProfile.objective_status,
      completion_label: toeNavigationProfile.completion_label
    },
    classification,
    selected_lane_id: selectedLaneId,
    candidate_lane_ids: candidateLaneIds,
    selected_anchor_open_problem_ids: selectedAnchors,
    retrieved_anchor_ids: retrievedAnchors,
    matched_question_terms: selectedMatches,
    required_prerequisite_gate_ids: selectedGate?.prerequisites ?? [],
    prerequisite_status: "ACTIVE_PROFILE_REQUIRES_HUMAN_GRAPH_REVIEW",
    current_blocker: {
      gate_id: "G1",
      anchor_open_problem_id: gateOneRoute.anchor_open_problem_id
    },
    critical_path_gate_ids: gates.map(({ id }) => id),
    terminal_review_criteria: toeNavigationProfile.terminal_review_criteria,
    promotion_boundary: promotionBoundary,
    core_progress_eligibility: isCurrent ? "HUMAN_REVIEW_REQUIRED" : "NOT_ELIGIBLE",
    decision: isCurrent ? "REVIEW_CURRENT_BLOCKER" : "STOP_OR_REFRAME",
    anti_meandering: {
      passed: anchorCheck && selectorCheck && currentBlockerCheck,
      checks: [
        {
          id: "canonical-cpt-anchor-retrieved",
          passed: anchorCheck,
          detail: "The selected route must include a retrieved canonical CPT open-problem anchor."
        },
        {
          id: "question-names-route",
          passed: selectorCheck,
          detail: "The question must explicitly name the anchor or at least two route selectors."
        },
        {
          id: "earliest-blocker-first",
          passed: currentBlockerCheck,
          detail: "Core progress must target the current G1 blocker; other lanes stop or remain supporting."
        }
      ]
    },
    reasons
  }
}
