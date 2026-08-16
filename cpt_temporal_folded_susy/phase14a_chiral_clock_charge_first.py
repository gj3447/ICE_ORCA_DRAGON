#!/usr/bin/env python3
"""Phase 14A — compact chiral-clock charge-first template audit.

This executable evaluates a deliberately bounded structural template.  It
does not derive a complete matter-coupled FLRW canonical supergravity, a
quantum physical Hilbert space, or a relational cosmological branch.

The frozen route is a bosonic spatially-flat FLRW background with compact
Sigma=T^3, one neutral chiral scalar Z=(T+iY)/sqrt(2), canonical physical
Kahler potential, W identically zero, no vectors, periodic spin structure,
and a monotonic p_T!=0 clock patch.  Three possible representatives descended
from standard local 4D N=1 supersymmetry are audited:

1. the proper bulk first-class constraint in the classical reduced quotient;
2. a residual parameter preserving the linearized cosmological goldstino
   unitary gauge, using Kallosh--Kofman--Linde--Van Proeyen equations
   (7.15)-(7.16), hep-th/0006179v3;
3. a Regge--Teitelboim spatial-boundary improvement, using Henneaux--
   Matulich--Neogi equations (II.33)-(II.35), arXiv:2004.07299v2, only as
   the canonical boundary template.

The asymptotically-flat surface expression is never imported into FLRW.
The recent matter-free FLRW paper arXiv:2510.20072v1 is a scope control only.
An independent emergent, nonlocal, topological, dressed, defect, temporal-
boundary, or fully reduced fermionic symmetry is outside this executable.

Contract: PHASE14A_RESEARCH_CONTRACT.json, commit 86194e1, preregistered
before this file existed.  Sources and pre-run channel ledger were frozen at
commit 9dd5333 before the first run.

Verification:
    uv run --with sympy python3 phase14a_chiral_clock_charge_first.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


class Audit:
    """Exact-check recorder; no floating tolerance or numerical fallback."""

    def __init__(self) -> None:
        self.passed = 0
        self.mutants_rejected = 0
        self.semantic_guards = 0

    def check(self, check_id: str, condition: bool, statement: str) -> None:
        if not condition:
            raise AssertionError(f"{check_id}: {statement}")
        self.passed += 1
        print(f"[PASS] {check_id}: {statement}")

    def reject(self, check_id: str, condition: bool, statement: str) -> None:
        if not condition:
            raise AssertionError(f"{check_id}: mutant survived — {statement}")
        self.mutants_rejected += 1
        print(f"[MUTANT REJECTED] {check_id}: {statement}")

    def guard(self, check_id: str, condition: bool, statement: str) -> None:
        """Record a scope guard without misreporting it as a code mutant."""
        if not condition:
            raise AssertionError(f"{check_id}: semantic guard failed — {statement}")
        self.semantic_guards += 1
        print(f"[SCOPE GUARD] {check_id}: {statement}")


@dataclass(frozen=True)
class SourceState:
    """Frozen provenance and template coverage known before calculation."""

    valid: bool
    ledger_coverage: bool
    topology: dict[str, object]


@dataclass(frozen=True)
class GateState:
    """Observed Phase 14A gate values used by the verdict function."""

    invalid: bool
    g0_valid: bool
    g1_valid: bool
    qualified_positive_witness: bool
    residual_kernel_dimension: int | None
    spatial_boundary_components: int | None
    bulk_quotient_zero: bool | None
    standard_dirac_decomposition_derived: bool
    ledger_coverage: bool


INVALID = "INVALID"
SUPPORTS = "SUPPORTS_SELECTED_TEMPLATE_NONZERO_PHYSICAL_CHARGE"
CONTRADICTS = "CONTRADICTS_SELECTED_LINEARIZED_GOLDSTINO_RT_TEMPLATE"
INCONCLUSIVE = "INCONCLUSIVE_UNCONSTRUCTED"


def classify(state: GateState) -> str:
    """Implement the frozen verdict precedence without reading global state."""
    if state.invalid:
        return INVALID
    if not (state.g0_valid and state.g1_valid):
        return INCONCLUSIVE
    if state.qualified_positive_witness:
        return SUPPORTS

    template_complete = (
        state.standard_dirac_decomposition_derived and state.ledger_coverage
    )
    all_selected_channels_trivial = (
        state.residual_kernel_dimension == 0
        and state.spatial_boundary_components == 0
        and state.bulk_quotient_zero is True
    )
    if template_complete and all_selected_channels_trivial:
        return CONTRADICTS
    return INCONCLUSIVE


def mutant_negative_before_positive(state: GateState) -> str:
    """Deliberately wrong ordering used only as an executable mutant."""
    all_selected_channels_trivial = (
        state.residual_kernel_dimension == 0
        and state.spatial_boundary_components == 0
        and state.bulk_quotient_zero is True
    )
    if state.standard_dirac_decomposition_derived and all_selected_channels_trivial:
        return CONTRADICTS
    if state.qualified_positive_witness:
        return SUPPORTS
    return INCONCLUSIVE


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def poisson(
    left: sp.Expr,
    right: sp.Expr,
    coordinates: list[sp.Symbol],
    momenta: list[sp.Symbol],
) -> sp.Expr:
    return sp.expand(
        sum(
            sp.diff(left, q) * sp.diff(right, p)
            - sp.diff(left, p) * sp.diff(right, q)
            for q, p in zip(coordinates, momenta)
        )
    )


def load_frozen_json(name: str) -> dict[str, object]:
    path = Path(__file__).with_name(name)
    return json.loads(path.read_text(encoding="utf-8"))


def part_source_packet(audit: Audit) -> SourceState:
    """Verify the frozen source roles, hashes, and non-stacking guards."""
    contract = load_frozen_json("PHASE14A_RESEARCH_CONTRACT.json")
    packet = load_frozen_json("PHASE14A_SOURCE_PACKET.json")
    ledger = load_frozen_json("PHASE14A_CHARGE_LEDGER.json")
    sources = {
        source["source_id"]: source
        for source in packet["sources"]  # type: ignore[index]
    }

    expected_hashes = {
        "KALLOSH_KOFMAN_LINDE_VAN_PROEYEN_2000_V3": (
            "81c4ab799f2cd943bb53fec6f8607267a46090b222a9fc659144902862431af7"
        ),
        "HENNEAUX_MATULICH_NEOGI_2020_V2": (
            "580d701efb3068709cd1e46033425b5a9ed1fa74a40c14db3839ac11cf3ad473"
        ),
        "MARTINEZ_PEREZ_RAMIREZ_2025_V1": (
            "5f6d4195b55427163955677ac5fa87bd33b912d344b14408981146ce4a380146"
        ),
    }
    audit.check(
        "P14A.source.hashes",
        set(sources) == set(expected_hashes)
        and all(
            sources[source_id]["main_tex_sha256"] == expected_hash
            for source_id, expected_hash in expected_hashes.items()
        ),
        "the three frozen main-TeX SHA-256 values and source identities match the preregistered packet",
    )

    cycle_id = "cpt-temporal-folded-susy-2026-08-16-phase14a"
    class_id = (
        "BOSONIC_FLAT_FLRW_LINEAR_FERMION_GOLDSTINO_GAUGE_"
        "AND_RT_SPATIAL_BOUNDARY_TEMPLATE"
    )
    audit.check(
        "P14A.source.cross_file_identity",
        contract["cycle_id"] == packet["cycle_id"] == ledger["cycle_id"] == cycle_id
        and contract["registration"] == "PREREGISTERED"
        and packet["preregistered_contract"]["commit"]
        == "86194e16f9ddb585292ff6569bc415163e917c99"
        and contract["scope_lock"]["candidate_class_id"] == class_id
        and ledger["candidate_class_id"] == class_id
        and packet["packet_status"] == "FROZEN_BEFORE_FIRST_EXECUTABLE_RUN"
        and ledger["created_before_first_run"] is True,
        "contract, source packet, and pre-run ledger have one frozen cycle and candidate-class identity",
    )

    guard = packet["distinct_source_guard"]  # type: ignore[index]
    audit.check(
        "P14A.source.distinct_roles",
        guard["cross_source_single_model_derivation"] is False
        and "goldstino" in guard["kallosh_role"]
        and "boundary" in guard["henneaux_role"]
        and "matter-free" in guard["martinez_perez_ramirez_role"],
        "the three papers remain separate source gates rather than a synthetic parent model",
    )

    flrw_scope = sources["MARTINEZ_PEREZ_RAMIREZ_2025_V1"][
        "manifest_scope"
    ]
    audit.check(
        "P14A.source.modern_flrw_scope",
        all(value is False for value in flrw_scope.values()),
        "the 2025 FLRW seed supplies no matter, chiral clock, canonical algebra, quantization, T3 analysis, or physical charge",
    )

    coefficient = sp.symbols("c", real=True, nonzero=True)
    lapse, scale = sp.symbols("N a", positive=True)
    delta_lapse = coefficient * lapse
    delta_scale = coefficient * scale
    ratio_variation = sp.simplify(
        delta_lapse / scale - lapse * delta_scale / scale**2
    )
    audit.check(
        "P14A.source.flrw_ratio",
        ratio_variation == 0,
        "the imported 2025 transformations preserve N/a but do not select its constant value",
    )
    audit.reject(
        "P14A.mutant.unique_conformal_gauge",
        sp.simplify(
            (2 * coefficient * lapse) / scale
            - lapse * (coefficient * scale) / scale**2
        )
        != 0,
        "mutating delta N and delta a to unequal weights breaks preservation of N/a",
    )

    in_class = [
        candidate
        for candidate in ledger["candidates"]
        if candidate["status"] != "OUTSIDE_CANDIDATE_CLASS"
    ]
    expected_channels = {
        "LOCAL_SUSY_PROPER_BULK",
        "LOCAL_SUSY_GOLDSTINO_GAUGE_RESIDUAL",
        "LOCAL_SUSY_RT_SPATIAL_IMPROVEMENT",
    }
    ledger_coverage = (
        {candidate["provisional_channel_id"] for candidate in in_class}
        == expected_channels
        and len(in_class) == 3
        and all(
            candidate["status"] == "PENDING_EXECUTION"
            and candidate["equivalence_class_id"] == "PENDING_EXECUTION"
            and candidate["physical_representative"] == "PENDING_EXECUTION"
            for candidate in in_class
        )
        and ledger["maximum_eligible_completeness_claim"]
        == "CONTRACT_TEMPLATE_COMPLETE_CONDITIONAL_ON_STANDARD_DIRAC_DECOMPOSITION"
    )
    audit.check(
        "P14A.source.prerun_ledger",
        ledger_coverage
        and ledger["observed_completeness_status"] == "PENDING_EXECUTION"
        and ledger["observed_overall_template_verdict"] == "PENDING_EXECUTION"
        and len(ledger["candidates"]) == 4,
        "the frozen ledger has exactly three pending in-template channels, no preassigned class, and one explicit outside channel",
    )

    topology = contract["scope_lock"]["topology"]
    audit.check(
        "P14A.source.frozen_topology",
        topology["cauchy_slice"] == "T^3"
        and topology["spatial_boundary"] == "empty"
        and topology["asymptotic_end"] == "none"
        and topology["spin_structure"] == "periodic"
        and topology["temporal_endpoints_are_spatial_charge_boundaries"] is False,
        "the compact boundaryless periodic-spin topology is read from the preregistered contract",
    )
    return SourceState(valid=True, ledger_coverage=ledger_coverage, topology=topology)


def part_bosonic_clock(audit: Audit) -> dict[str, sp.Expr]:
    """Derive the exact Einstein-plus-complex-scalar FLRW clock skeleton."""
    v0, scale, lapse, planck = sp.symbols(
        "V_0 a N M_P", positive=True, finite=True
    )
    adot, xdot, tdot, ydot = sp.symbols("adot Xdot Tdot Ydot", real=True)
    p_x = sp.symbols("p_X", real=True)
    p_t = sp.symbols("p_T", real=True, nonzero=True)
    p_t_abs = sp.symbols("p_T_abs", positive=True)
    p_y = sp.symbols("p_Y", real=True)
    x, clock, spectator = sp.symbols("X T Y", real=True)

    # Begin with the standard lapse-retaining flat-FLRW Einstein kinetic term
    # plus a canonical complex scalar.  A dot is coordinate-time d/dt.
    normal_hubble = adot / (lapse * scale)
    extrinsic_square = 3 * normal_hubble**2
    trace_square = 9 * normal_hubble**2
    lagrangian_einstein_adm = sp.simplify(
        planck**2
        * lapse
        * v0
        * scale**3
        * (extrinsic_square - trace_square)
        / 2
    )
    lagrangian_einstein = -3 * planck**2 * v0 * scale * adot**2 / lapse
    zdot = (tdot + sp.I * ydot) / sp.sqrt(2)
    zbar_dot = (tdot - sp.I * ydot) / sp.sqrt(2)
    lagrangian_scalar = sp.simplify(v0 * scale**3 * zdot * zbar_dot / lapse)
    original_lagrangian = sp.expand(lagrangian_einstein + lagrangian_scalar)

    # X=sqrt(6) M_P ln(a), hence adot=a Xdot/(sqrt(6) M_P).
    lagrangian = sp.simplify(
        original_lagrangian.subs(adot, scale * xdot / (sp.sqrt(6) * planck))
    )
    expected_lagrangian = (
        v0 * scale**3 * (-xdot**2 + tdot**2 + ydot**2) / (2 * lapse)
    )
    audit.check(
        "P14A.clock.eh_kahler_reduction",
        sp.simplify(lagrangian_einstein_adm - lagrangian_einstein) == 0
        and sp.simplify(lagrangian_scalar - v0 * scale**3 * (tdot**2 + ydot**2) / (2 * lapse))
        == 0
        and sp.simplify(lagrangian - expected_lagrangian) == 0,
        "the flat-FLRW Einstein term and canonical complex-scalar kinetic term give the frozen X-normalized Lagrangian",
    )
    momenta_from_l = [
        sp.diff(lagrangian, velocity) for velocity in (xdot, tdot, ydot)
    ]
    expected_momenta = [
        -v0 * scale**3 * xdot / lapse,
        v0 * scale**3 * tdot / lapse,
        v0 * scale**3 * ydot / lapse,
    ]
    audit.check(
        "P14A.clock.legendre_momenta",
        all(
            sp.simplify(actual - expected) == 0
            for actual, expected in zip(momenta_from_l, expected_momenta)
        ),
        "the coordinate-time FLRW Lagrangian gives the frozen canonical momenta without guessed lapse factors",
    )

    velocity_solution = {
        xdot: -lapse * p_x / (v0 * scale**3),
        tdot: lapse * p_t / (v0 * scale**3),
        ydot: lapse * p_y / (v0 * scale**3),
    }
    hamiltonian = sp.simplify(
        (p_x * xdot + p_t * tdot + p_y * ydot - lagrangian).subs(
            velocity_solution
        )
    )
    constraint = sp.expand(-p_x**2 + p_t**2 + p_y**2)
    expected_hamiltonian = lapse * constraint / (2 * v0 * scale**3)
    audit.check(
        "P14A.clock.legendre_hamiltonian",
        sp.simplify(hamiltonian - expected_hamiltonian) == 0,
        "the exact Legendre transform yields a positive densitization of C_B=-p_X^2+p_T^2+p_Y^2",
    )

    clock_bracket = poisson(
        clock,
        constraint,
        [x, clock, spectator],
        [p_x, p_t, p_y],
    )
    audit.check(
        "P14A.clock.monotonic_patch",
        sp.simplify(clock_bracket - 2 * p_t) == 0
        and sp.simplify(clock_bracket.subs(p_t, p_t_abs) - 2 * p_t_abs) == 0
        and sp.simplify(clock_bracket.subs(p_t, -p_t_abs) + 2 * p_t_abs) == 0
        and clock_bracket.subs(p_t, p_t_abs).is_nonzero is True
        and clock_bracket.subs(p_t, -p_t_abs).is_nonzero is True,
        "{T,C_B}=2p_T is nonzero on both frozen p_T positive and negative clock orientations",
    )

    proper_t = sp.simplify(velocity_solution[tdot] / lapse)
    proper_y = sp.simplify(velocity_solution[ydot] / lapse)
    alpha = sp.simplify((proper_t**2 + proper_y**2) / 2)
    expected_alpha = (p_t**2 + p_y**2) / (2 * v0**2 * scale**6)
    audit.check(
        "P14A.clock.proper_time_alpha",
        sp.simplify(alpha - expected_alpha) == 0
        and sp.simplify(alpha.subs(p_t, p_t_abs) - alpha.subs(p_t, -p_t_abs))
        == 0
        and sp.ask(sp.Q.positive(alpha.subs(p_t, p_t_abs))) is True
        and sp.ask(sp.Q.positive(alpha.subs(p_t, -p_t_abs))) is True,
        "the lapse-free proper-time alpha is positive on both p_T orientations while retaining Y",
    )

    audit.reject(
        "P14A.mutant.zero_momentum_clock",
        sp.simplify(clock_bracket.subs(p_t, 0)) == 0
        and sp.simplify(alpha.subs({p_t: 0, p_y: 0})) == 0,
        "p_T=0 with p_Y=0 was called a monotonic supersymmetry-preserving clock",
    )

    z = sp.symbols("z", real=True)
    pointwise_zero_w = z
    audit.reject(
        "P14A.mutant.pointwise_W_zero",
        pointwise_zero_w.subs(z, 0) == 0
        and sp.diff(pointwise_zero_w, z).subs(z, 0) != 0,
        "W=0 at one point was treated as W identically zero with vanishing covariant derivatives",
    )

    # Keep the physical-to-dimensionless Kahler bridge explicit.  It is
    # algebraically immaterial only after W is identically zero.
    z_abs_sq = sp.symbols("Z_abs_sq", nonnegative=True)
    cal_k = z_abs_sq / planck**2
    superpotential = sp.Integer(0)
    mass_function = sp.exp(cal_k / 2) * superpotential
    audit.check(
        "P14A.clock.kahler_planck_bridge",
        mass_function == 0 and sp.diff(mass_function, z_abs_sq) == 0,
        "K_phys/M_P^2 is dimensionless and W identically zero kills m and its field derivative",
    )

    return {
        "alpha": alpha,
        "constraint": constraint,
        "clock_bracket": clock_bracket,
        "p_t": p_t,
        "proper_t": proper_t,
        "proper_y": proper_y,
        "p_y": p_y,
        "scale": scale,
        "v0": v0,
    }


def part_goldstino_residual(audit: Audit, data: dict[str, sp.Expr]) -> int:
    """Bridge the frozen complex chiral clock to the source residual gate."""
    alpha = data["alpha"]
    identity = sp.eye(4)
    proper_t = data["proper_t"]
    proper_y = data["proper_y"]

    # W is identically zero and there are no vectors, hence m=D_i m=V_D=0.
    # For the canonical complex field, the surviving Kallosh source norm is
    # |D_tau Z|^2 with both real components retained.
    proper_z = (proper_t + sp.I * proper_y) / sp.sqrt(2)
    proper_zbar = (proper_t - sp.I * proper_y) / sp.sqrt(2)
    source_alpha = sp.simplify(proper_z * proper_zbar)
    source_rhs = sp.simplify(source_alpha * identity)
    canonical_rhs = sp.simplify(alpha * identity)
    audit.check(
        "P14A.goldstino.source_to_canonical_bridge",
        sp.simplify(source_alpha - (proper_t**2 + proper_y**2) / 2) == 0
        and zero_matrix(source_rhs - canonical_rhs),
        "with W identically zero and V_D=0, the Kallosh complex-chiral source norm equals the canonical alpha including p_Y",
    )

    residual_matrix = sp.simplify(-source_alpha * identity / 2)
    audit.check(
        "P14A.goldstino.exact_sign",
        zero_matrix(-2 * residual_matrix - source_rhs),
        "the frozen sign is delta upsilon/delta epsilon=-(alpha/2) I from -2 delta upsilon=alpha epsilon",
    )
    wrong_sign_residual = sp.simplify(source_alpha * identity / 2)
    audit.reject(
        "P14A.mutant.goldstino_sign",
        not zero_matrix(-2 * wrong_sign_residual - source_rhs),
        "flipping the source sign fails -2 delta upsilon=alpha epsilon",
    )

    kernel_dimension = len(residual_matrix.nullspace())
    audit.check(
        "P14A.goldstino.full_rank",
        residual_matrix.rank() == 4
        and kernel_dimension == 0
        and sp.simplify(residual_matrix.det() - source_alpha**4 / 16) == 0,
        "alpha>0 makes the Majorana gauge-preservation matrix full rank with zero residual-parameter kernel",
    )

    hubble = sp.symbols("H", real=True, nonzero=True)
    planck = sp.symbols("M_P", positive=True)
    alpha_h = 3 * planck**2 * hubble**2
    audit.check(
        "P14A.goldstino.branch_even",
        sp.simplify(alpha_h - alpha_h.subs(hubble, -hubble)) == 0,
        "the W-identically-zero source alpha identity is even under H to -H and supplies no branch exchange map",
    )

    local_gauge_invariance_present = True
    nonzero_gauge_preserving_residual = kernel_dimension != 0
    audit.guard(
        "P14A.guard.residual_not_gauge_loss",
        local_gauge_invariance_present
        and not nonzero_gauge_preserving_residual,
        "absence of an unbroken goldstino-gauge residual parameter is kept distinct from loss of local gauge invariance",
    )
    return kernel_dimension


def part_compact_boundary(
    audit: Audit, topology: dict[str, object]
) -> int:
    """Check the RT sign template and exact T3 opposite-face cancellation."""
    epsilon = sp.symbols("epsilon", real=True)
    coefficients = sp.Matrix(sp.symbols("c0:4", real=True))
    psi = sp.Matrix(sp.symbols("psi0:4", real=True))
    delta_psi = sp.Matrix(sp.symbols("dpsi0:4", real=True))
    b_susy = sp.simplify(-sp.I * epsilon * (coefficients.T * psi)[0])
    delta_b = sp.simplify(
        sum(sp.diff(b_susy, psi[i]) * delta_psi[i] for i in range(4))
    )
    expected_delta_b = sp.simplify(
        -sp.I * epsilon * (coefficients.T * delta_psi)[0]
    )
    audit.check(
        "P14A.boundary.rt_variation_sign",
        sp.simplify(delta_b - expected_delta_b) == 0,
        "varying the frozen II.35 expression reproduces the II.34 sign; this is a source-sign control, not a FLRW differentiability derivation",
    )
    wrong_sign_b = sp.simplify(sp.I * epsilon * (coefficients.T * psi)[0])
    wrong_sign_delta = sp.simplify(
        sum(sp.diff(wrong_sign_b, psi[i]) * delta_psi[i] for i in range(4))
    )
    audit.reject(
        "P14A.mutant.rt_sign",
        sp.simplify(wrong_sign_delta - expected_delta_b) != 0,
        "the opposite sign for B_Susy fails the frozen II.34 variation",
    )

    # Oriented boundary of a fundamental cube.  After periodic quotient, the
    # opposite x, y, and z faces are identified and their coefficients cancel.
    oriented_faces = sp.Matrix([-1, 1, -1, 1, -1, 1])
    periodic_identification = sp.Matrix(
        [
            [1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 1],
        ]
    )
    quotient_boundary = periodic_identification * oriented_faces
    flux_x, flux_y, flux_z = sp.symbols("F_x F_y F_z", real=True)
    periodic_flux = sp.simplify(
        -flux_x + flux_x - flux_y + flux_y - flux_z + flux_z
    )
    audit.check(
        "P14A.boundary.t3_empty",
        zero_matrix(quotient_boundary) and periodic_flux == 0,
        "oppositely oriented periodic faces cancel exactly, so the T3 fundamental cell has no physical spatial boundary",
    )
    audit.reject(
        "P14A.mutant.six_physical_faces",
        not zero_matrix(oriented_faces) and zero_matrix(quotient_boundary),
        "removing the periodic quotient leaves fiducial faces and therefore changes the registered topology",
    )

    frozen_boundaryless = (
        topology["cauchy_slice"] == "T^3"
        and topology["spatial_boundary"] == "empty"
        and topology["asymptotic_end"] == "none"
    )
    actual_spatial_boundary_components = 0 if frozen_boundaryless else -1
    temporal_endpoints_are_spatial_boundaries = topology[
        "temporal_endpoints_are_spatial_charge_boundaries"
    ]
    audit.check(
        "P14A.boundary.channel_absent",
        actual_spatial_boundary_components == 0
        and not temporal_endpoints_are_spatial_boundaries
        and zero_matrix(quotient_boundary),
        "the RT asymptotic integration channel is absent rather than imported into compact FLRW",
    )
    audit.guard(
        "P14A.guard.temporal_endpoint_not_spatial_boundary",
        actual_spatial_boundary_components == 0
        and not temporal_endpoints_are_spatial_boundaries,
        "a temporal endpoint or prior collar is not renamed as the spatial RT charge surface",
    )
    return actual_spatial_boundary_components


def part_formal_bulk_quotient(audit: Audit) -> tuple[bool, bool]:
    """Run a formal ideal control without claiming the missing SUGRA bridge."""
    constraints = sp.symbols("S0:4")
    epsilons = sp.symbols("e0:4")
    bulk_generator = sp.I * sum(
        epsilon * constraint
        for epsilon, constraint in zip(epsilons, constraints)
    )
    decomposition_witness = sum(
        coefficient * generator
        for coefficient, generator in zip(
            [sp.I * epsilon for epsilon in epsilons], constraints
        )
    )
    quotient_remainder = sp.expand(
        bulk_generator.subs({constraint: 0 for constraint in constraints})
    )
    bulk_quotient_zero = quotient_remainder == 0
    audit.check(
        "P14A.quotient.formal_ideal_control",
        sp.simplify(bulk_generator - decomposition_witness) == 0
        and bulk_quotient_zero,
        "a generator already known to be a constraint combination has zero formal quotient class",
    )
    audit.guard(
        "P14A.guard.offshell_not_physical_charge",
        bulk_generator != 0 and quotient_remainder == 0,
        "a nonzero off-shell constraint expression is not counted as a nonzero reduced physical charge",
    )

    # Phase 14A has not derived the differentiable first-class generator of the
    # compact matter-coupled model.  The formal ideal control therefore has no
    # authority to upgrade itself to the contract's standard-Dirac bridge.
    standard_dirac_decomposition_derived = False
    audit.guard(
        "P14A.guard.formal_quotient_scope",
        bulk_quotient_zero and not standard_dirac_decomposition_derived,
        "the commuting ideal-membership control carries zero evidence for the missing graded matter-SUGRA canonical derivation",
    )
    return bulk_quotient_zero, standard_dirac_decomposition_derived


def part_observed_ledger(
    audit: Audit,
    source_state: SourceState,
    residual_kernel_dimension: int,
    spatial_boundary_components: int,
    bulk_quotient_zero: bool,
    standard_dirac_decomposition_derived: bool,
) -> dict[str, object]:
    """Build post-run candidate observations from gate outputs, not matrices."""
    residual_status = (
        "NO_NONZERO_GOLDSTINO_GAUGE_RESIDUAL"
        if residual_kernel_dimension == 0
        else "NONZERO_PARAMETER_REQUIRES_PHYSICAL_SUPPORT_GATES"
    )
    boundary_status = (
        "NOT_APPLICABLE_IN_THIS_ROUTE"
        if spatial_boundary_components == 0
        else "BOUNDARY_CHANNEL_REQUIRES_PHYSICAL_SUPPORT_GATES"
    )
    bulk_status = (
        "FORMAL_ZERO_CONDITIONAL_ON_UNDERIVED_STANDARD_DIRAC_DECOMPOSITION"
        if bulk_quotient_zero and not standard_dirac_decomposition_derived
        else "OBSERVED_STANDARD_DIRAC_QUOTIENT_ZERO"
        if bulk_quotient_zero
        else "UNCONSTRUCTED_OR_NONZERO"
    )
    observations = {
        "LOCAL_SUSY_PROPER_BULK": bulk_status,
        "LOCAL_SUSY_GOLDSTINO_GAUGE_RESIDUAL": residual_status,
        "LOCAL_SUSY_RT_SPATIAL_IMPROVEMENT": boundary_status,
    }
    audit.check(
        "P14A.ledger.derived_channel_statuses",
        residual_status == "NO_NONZERO_GOLDSTINO_GAUGE_RESIDUAL"
        and boundary_status == "NOT_APPLICABLE_IN_THIS_ROUTE"
        and bulk_status
        == "FORMAL_ZERO_CONDITIONAL_ON_UNDERIVED_STANDARD_DIRAC_DECOMPOSITION"
        and set(observations)
        == {
            "LOCAL_SUSY_PROPER_BULK",
            "LOCAL_SUSY_GOLDSTINO_GAUGE_RESIDUAL",
            "LOCAL_SUSY_RT_SPATIAL_IMPROVEMENT",
        },
        "G2 through G4 outputs, rather than preassigned zero matrices, determine the three observed channel statuses",
    )

    conditional_completeness = (
        source_state.ledger_coverage and standard_dirac_decomposition_derived
    )
    deduplication_status = (
        "COMPLETE" if conditional_completeness else "DEFERRED_PENDING_CANONICAL_BRIDGE"
    )
    audit.check(
        "P14A.ledger.completeness_not_overclaimed",
        not conditional_completeness
        and deduplication_status == "DEFERRED_PENDING_CANONICAL_BRIDGE",
        "the missing matter-SUGRA Dirac bridge prevents a post-run completeness or equivalence-class claim",
    )

    ledger = load_frozen_json("PHASE14A_CHARGE_LEDGER.json")
    outside = next(
        candidate
        for candidate in ledger["candidates"]
        if candidate["candidate_id"] == "P14A-Q-INDEPENDENT-REDUCED"
    )
    audit.guard(
        "P14A.ledger.outside_class",
        outside["status"] == "OUTSIDE_CANDIDATE_CLASS"
        and outside["physical_representative"] == "NOT_SEARCHED",
        "independent emergent or nonlocal reduced symmetries remain explicitly unsearched",
    )

    audit.guard(
        "P14A.ledger.no_branch_test",
        ledger["literal_branch_superpartner_status"]
        == "INCONCLUSIVE_OUT_OF_SCOPE",
        "no relational P_plus/P_minus or cross-branch block is introduced in Phase 14A",
    )
    return {
        "observations": observations,
        "conditional_completeness": conditional_completeness,
        "deduplication_status": deduplication_status,
    }


def part_verdict_controls(audit: Audit, observed_state: GateState) -> str:
    """Exercise all frozen precedence branches and classify the observation."""
    invalid_case = GateState(
        invalid=True,
        g0_valid=True,
        g1_valid=True,
        qualified_positive_witness=True,
        residual_kernel_dimension=0,
        spatial_boundary_components=0,
        bulk_quotient_zero=True,
        standard_dirac_decomposition_derived=True,
        ledger_coverage=True,
    )
    positive_case = GateState(
        invalid=False,
        g0_valid=True,
        g1_valid=True,
        qualified_positive_witness=True,
        residual_kernel_dimension=0,
        spatial_boundary_components=0,
        bulk_quotient_zero=True,
        standard_dirac_decomposition_derived=True,
        ledger_coverage=True,
    )
    complete_zero_case = GateState(
        invalid=False,
        g0_valid=True,
        g1_valid=True,
        qualified_positive_witness=False,
        residual_kernel_dimension=0,
        spatial_boundary_components=0,
        bulk_quotient_zero=True,
        standard_dirac_decomposition_derived=True,
        ledger_coverage=True,
    )
    incomplete_case = GateState(
        invalid=False,
        g0_valid=True,
        g1_valid=True,
        qualified_positive_witness=False,
        residual_kernel_dimension=0,
        spatial_boundary_components=0,
        bulk_quotient_zero=True,
        standard_dirac_decomposition_derived=False,
        ledger_coverage=True,
    )
    audit.check(
        "P14A.verdict.precedence",
        classify(invalid_case) == INVALID
        and classify(positive_case) == SUPPORTS
        and classify(complete_zero_case) == CONTRADICTS
        and classify(incomplete_case) == INCONCLUSIVE,
        "INVALID, qualified positive witness, complete selected-template zero, and incomplete cases follow the frozen precedence",
    )
    audit.reject(
        "P14A.mutant.negative_before_positive",
        mutant_negative_before_positive(positive_case) == CONTRADICTS
        and classify(positive_case) == SUPPORTS,
        "a qualified positive witness cannot be overwritten by the all-zero-template branch",
    )
    return classify(observed_state)


def main() -> int:
    audit = Audit()

    print("\n=== P14A-0 frozen source and scope packet ===")
    source_state = part_source_packet(audit)

    print("\n=== P14A-1 bosonic chiral-clock skeleton ===")
    clock_data = part_bosonic_clock(audit)

    print("\n=== P14A-2 cosmological goldstino residual gate ===")
    residual_kernel_dimension = part_goldstino_residual(audit, clock_data)

    print("\n=== P14A-3 compact spatial-boundary channel ===")
    spatial_boundary_components = part_compact_boundary(
        audit, source_state.topology
    )

    print("\n=== P14A-4 formal bulk quotient control ===")
    (
        bulk_quotient_zero,
        standard_dirac_decomposition_derived,
    ) = part_formal_bulk_quotient(audit)

    print("\n=== P14A-5 observed charge ledger ===")
    part_observed_ledger(
        audit,
        source_state,
        residual_kernel_dimension,
        spatial_boundary_components,
        bulk_quotient_zero,
        standard_dirac_decomposition_derived,
    )

    print("\n=== P14A-6 frozen verdict precedence ===")
    observed_state = GateState(
        invalid=False,
        g0_valid=source_state.valid,
        g1_valid=True,
        qualified_positive_witness=False,
        residual_kernel_dimension=residual_kernel_dimension,
        spatial_boundary_components=spatial_boundary_components,
        bulk_quotient_zero=bulk_quotient_zero,
        standard_dirac_decomposition_derived=standard_dirac_decomposition_derived,
        ledger_coverage=source_state.ledger_coverage,
    )
    verdict = part_verdict_controls(audit, observed_state)

    print(
        "\nALL EXACT CHECKS PASSED: "
        f"{audit.passed} positive checks; "
        f"{audit.mutants_rejected} executable mutants rejected; "
        f"{audit.semantic_guards} scope guards enforced."
    )
    print(
        "SELECTED TEMPLATE INFERENCE: "
        "P14A_SELECTED_GOLDSTINO_RT_TEMPLATE_NONZERO_PHYSICAL_CHARGE is "
        f"{verdict}. The goldstino residual kernel is zero and the compact "
        "RT boundary channel is absent, but the differentiable graded "
        "matter-SUGRA Dirac decomposition was not derived."
    )
    print(
        "BROADER CHARGE INFERENCE: INCONCLUSIVE — no full matter-coupled "
        "canonical census, independent reduced/dressed charge, nonlinear "
        "compensating sector, or quantum physical domain was constructed."
    )
    print(
        "LITERAL BRANCH INFERENCE: INCONCLUSIVE/OUT_OF_SCOPE — no relational "
        "branch projector or branch cross block was defined."
    )
    print(
        "SEQUENCING: Phase 14B is not opened. A new preregistered canonical-"
        "bridge cycle would be required before this selected template could "
        "receive either SUPPORTS or CONTRADICTS."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        raise SystemExit(1) from error
