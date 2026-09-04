#!/usr/bin/env python3
"""Test one naive local-lapse unfixing of the frozen Starobinsky m=2 action.

The calculation first derives the exact two-local-lapse configuration action.
It then uses Arb ball arithmetic and a strict Krawczyk inclusion to certify a
unique stationary point of the proper-time action and a nonzero determinant of
the full relative-lapse-extended Hessian there.

The result can retire only this one naive configuration-space unfixing.  It
does not exclude a first-order, perfect/improved, or continuum-first BFV
construction, and it does not construct a BFV source or relative cycle.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import flint
import sympy as sp
from flint import arb, arb_mat, ctx


INPUT_NAME = "GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST_INPUTS.json"
RESULT_NAME = "GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_m2_starobinsky_naive_local_lapse_gauge_test.py"
)
EXPECTED_INPUT_SHA256 = (
    "3f7382a5ceb00ec58e8187235312eebfafc0168cd196110d82dcf1a3bb602477"
)
CALCULATION_ID = "Gate1M2StarobinskyNaiveLocalLapseGaugeTest"
RESULT_SCHEMA = "ice.gate1-m2-starobinsky-naive-local-lapse-gauge-test.result.v1"
RESULT_PREFIX = "GATE1_M2_STAROBINSKY_NAIVE_LOCAL_LAPSE_GAUGE_TEST_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 100,
        "interval_certificates": 1,
        "root_calls": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "starobinsky_finite_m2_bfv_trajectory_source": None,
        "first_order_constraint_lattice": None,
        "bfv_charge_and_gauge_fermion": None,
        "endpoint_state_transform": None,
        "source_equivalence_or_deformation": None,
        "zero_lapse_distribution": None,
        "U0_U1_U1prime_Uf_descent": None,
        "complete_end_divisor_census": None,
        "candidate_set_completeness": None,
        "absolute_bfv_orientation": None,
        "physical_original_cycle": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "physics_claim": None,
        "TOE_claim": None,
        "automatic_next": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    certified: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def reserve(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate check id: {ident}")
        self.seen.add(ident)

    def check(self, ident: str, passed: bool, statement: str, **data: Any) -> None:
        self.reserve(ident)
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {ident}: {statement}")
        self.exact.append(
            {"id": ident, "passed": True, "statement": statement, **data}
        )

    def certify(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.reserve(ident)
        self.certified.append(
            {
                "id": ident,
                "passed": bool(passed),
                "verification_mode": "ARB_RIGOROUS_BALL_ARITHMETIC",
                "statement": statement,
                **data,
            }
        )

    def guard(
        self,
        ident: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.reserve(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream_result(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream is not a valid run: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict drift: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload digest drift: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def verify_upstream_file(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed}


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]], list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.gate1-m2-starobinsky-naive-local-lapse-gauge-test.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if cfg["planner"]["classification"] != "CURRENT_BLOCKER_CANDIDATE":
        raise AssertionError("planner classification drift")
    root = Path(__file__).resolve().parent.parent
    upstream_results = [
        verify_upstream_result(root, item) for item in cfg["upstream_results"]
    ]
    upstream_files = [
        verify_upstream_file(root, item) for item in cfg["upstream_files"]
    ]
    return cfg, observed, upstream_results, upstream_files


def build_symbolic_model(
    audit: Audit, cfg: dict[str, Any]
) -> dict[str, Any]:
    x, q, t_prop, r = sp.symbols("x q T r", real=True)
    n0, n1, epsilon = sp.symbols("N0 N1 epsilon", real=True)
    boundary = cfg["frozen_model"]["boundary"]
    a_b = sp.Rational(boundary["a_b"])
    phi_b = sp.Rational(boundary["phi_b"])
    A = a_b + x / 2
    Phi = phi_b + q / 2
    potential = sp.Rational(3, 4) * (
        1 - sp.exp(-sp.sqrt(sp.Rational(2, 3)) * Phi)
    ) ** 2
    kinetic = -6 * A * x**2 + A**3 * q**2
    potential_factor = -3 * A + A**3 * potential
    s2 = 4 * sp.pi**2 * kinetic / t_prop + 2 * sp.pi**2 * potential_factor * t_prop
    s2_expanded_target = (
        -24 * sp.pi**2 * A * x**2 / t_prop
        + 4 * sp.pi**2 * A**3 * q**2 / t_prop
        + 2 * sp.pi**2 * t_prop * (-3 * A + A**3 * potential)
    )
    local_segment_form = 2 * sp.pi**2 * (
        kinetic * (1 / n0 + 1 / n1)
        + potential_factor * (n0 + n1) / 2
    )
    local_action = sp.simplify(
        local_segment_form.subs({n0: t_prop + r, n1: t_prop - r})
    )
    local_compact = (
        4 * sp.pi**2 * kinetic * t_prop / (t_prop**2 - r**2)
        + 2 * sp.pi**2 * potential_factor * t_prop
    )
    derivative_r = sp.simplify(sp.diff(local_action, r))
    expected_derivative_r = (
        8
        * sp.pi**2
        * kinetic
        * t_prop
        * r
        / (t_prop**2 - r**2) ** 2
    )
    hessian_rr_at_zero = sp.simplify(sp.diff(local_action, r, 2).subs(r, 0))
    expected_hessian_rr = 8 * sp.pi**2 * kinetic / t_prop**3
    y = (x, q, t_prop)
    gradient = sp.Matrix([sp.diff(s2, variable) for variable in y])
    hessian_s2 = gradient.jacobian(y)
    hessian_local = sp.hessian(local_action, (*y, r))
    cross_at_zero = [
        sp.simplify(hessian_local[index, 3].subs(r, 0))
        for index in range(3)
    ]

    audit.check(
        "G1.local_lapse.exact.frozen_action_reconstruction",
        sp.simplify(s2 - s2_expanded_target) == 0,
        "K and W reconstruct the frozen equal-endpoint Starobinsky m=2 action exactly",
    )
    audit.check(
        "G1.local_lapse.exact.two_lapse_compact_identity",
        sp.simplify(local_action - local_compact) == 0,
        "the two segment-local lapses give the declared compact T,r action exactly",
    )
    audit.check(
        "G1.local_lapse.exact.proper_time_restriction",
        sp.simplify(local_action.subs(r, 0) - s2) == 0,
        "the candidate local-lapse action restricts to the frozen proper-time action at r=0",
    )
    audit.check(
        "G1.local_lapse.exact.relative_lapse_derivative",
        sp.simplify(derivative_r - expected_derivative_r) == 0,
        "the relative-lapse first derivative is the declared odd function of r",
    )
    audit.check(
        "G1.local_lapse.exact.relative_lapse_stationarity",
        sp.simplify(derivative_r.subs(r, 0)) == 0,
        "every proper-time stationary point lifts to an r=0 stationary point of the candidate extension",
    )
    audit.check(
        "G1.local_lapse.exact.relative_lapse_hessian",
        sp.simplify(hessian_rr_at_zero - expected_hessian_rr) == 0,
        "the relative-lapse Hessian entry at r=0 is 8*pi^2*K/T^3",
    )
    audit.check(
        "G1.local_lapse.exact.hessian_cross_block",
        all(value == 0 for value in cross_at_zero),
        "all field/proper-time versus relative-lapse Hessian cross terms vanish at r=0",
    )
    audit.check(
        "G1.local_lapse.exact.hessian_upper_block",
        all(
            sp.simplify(hessian_local[i, j].subs(r, 0) - hessian_s2[i, j])
            == 0
            for i in range(3)
            for j in range(3)
        ),
        "the upper Hessian block at r=0 is exactly the frozen S2 Hessian",
    )
    delta_t = sp.simplify(((2 * epsilon) + (-2 * epsilon)) / 2)
    delta_r = sp.simplify(((2 * epsilon) - (-2 * epsilon)) / 2)
    audit.check(
        "G1.local_lapse.exact.endpoint_preserving_generator",
        delta_t == 0 and sp.simplify(delta_r - 2 * epsilon) == 0,
        "the declared endpoint-preserving lapse variation fixes T and has nonzero relative-lapse component delta r=2 epsilon",
    )
    audit.check(
        "G1.local_lapse.exact.new_divisor_factorization",
        sp.expand((t_prop - r) * (t_prop + r)) == t_prop**2 - r**2,
        "the candidate extension introduces the two local-lapse divisors T-r=0 and T+r=0",
    )

    return {
        "symbols": {"x": x, "q": q, "T": t_prop, "r": r},
        "A": A,
        "Phi": Phi,
        "potential": potential,
        "K": kinetic,
        "W": potential_factor,
        "S2": s2,
        "S_local": local_action,
        "gradient": gradient,
        "hessian_s2": hessian_s2,
        "hessian_rr": expected_hessian_rr,
        "symbolic_record": {
            "A": str(A),
            "Phi": str(Phi),
            "V": str(potential),
            "K": str(kinetic),
            "W": str(potential_factor),
            "S2": str(s2),
            "S_local": str(local_action),
            "partial_r_S_local": str(derivative_r),
            "partial_rr_S_local_at_r_zero": str(hessian_rr_at_zero),
            "cross_hessian_at_r_zero": [str(value) for value in cross_at_zero],
            "relative_lapse_generator": {
                "delta_T": str(delta_t),
                "delta_r": str(delta_r),
            },
        },
    }


def arb_eval(expr: sp.Expr, values: dict[sp.Symbol, arb]) -> arb:
    """Evaluate the selected exact SymPy expression tree using Arb balls."""

    if expr in values:
        return values[expr]
    if expr == sp.pi:
        return arb.pi()
    if expr.is_Integer:
        return arb(int(expr))
    if expr.is_Rational:
        return arb(int(expr.p)) / arb(int(expr.q))
    if expr.func == sp.Add:
        result = arb(0)
        for term in expr.args:
            result += arb_eval(term, values)
        return result
    if expr.func == sp.Mul:
        result = arb(1)
        for factor in expr.args:
            result *= arb_eval(factor, values)
        return result
    if expr.func == sp.Pow:
        base, power = expr.args
        base_value = arb_eval(base, values)
        if power.is_Integer:
            return base_value ** int(power)
        if power == sp.Rational(1, 2):
            return base_value.sqrt()
        if power == sp.Rational(-1, 2):
            return 1 / base_value.sqrt()
        raise TypeError(f"unsupported Arb power: {expr}")
    if expr.func == sp.exp:
        return arb_eval(expr.args[0], values).exp()
    raise TypeError(f"unsupported Arb expression: {expr} ({expr.func})")


def excludes_zero(value: arb) -> bool:
    return bool(value.lower() > arb(0) or value.upper() < arb(0))


def ball_record(value: arb) -> dict[str, str]:
    return {
        "ball": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def certify_stationary_point(
    audit: Audit, cfg: dict[str, Any], model: dict[str, Any]
) -> dict[str, Any]:
    certificate = cfg["certificate"]
    ctx.prec = certificate["precision_bits"]
    symbol_order = [model["symbols"][name] for name in certificate["center_order"]]
    # Freeze exact dyadic representatives inside the requested decimal balls.
    # The radius uses the outward upper endpoint, so the certified box is not
    # narrower than the decimal radius named in the manifest.
    radius = arb(certificate["uniform_radius"]).upper()
    center = [arb(value).mid() for value in certificate["center"]]
    box = [arb(value, radius) for value in center]
    center_values = dict(zip(symbol_order, center, strict=True))
    box_values = dict(zip(symbol_order, box, strict=True))
    gradient: sp.Matrix = model["gradient"]
    hessian: sp.Matrix = model["hessian_s2"]

    f_center = arb_mat(
        [[arb_eval(gradient[i], center_values)] for i in range(3)]
    )
    jacobian_center = arb_mat(
        [
            [arb_eval(hessian[i, j], center_values) for j in range(3)]
            for i in range(3)
        ]
    )
    jacobian_box = arb_mat(
        [
            [arb_eval(hessian[i, j], box_values) for j in range(3)]
            for i in range(3)
        ]
    )
    inverse_enclosure = jacobian_center.inv()
    preconditioner = arb_mat(
        [
            [inverse_enclosure[i, j].mid() for j in range(3)]
            for i in range(3)
        ]
    )
    identity = arb_mat(
        [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    )
    centered_box = arb_mat([[arb(0, radius)] for _ in range(3)])
    krawczyk_delta = (
        -preconditioner * f_center
        + (identity - preconditioner * jacobian_box) * centered_box
    )
    strict_inclusion = [
        bool(
            krawczyk_delta[i, 0].lower() > -radius
            and krawczyk_delta[i, 0].upper() < radius
        )
        for i in range(3)
    ]
    det_hessian_box = jacobian_box.det()
    kinetic_box = arb_eval(model["K"], box_values)
    hessian_rr_box = arb_eval(model["hessian_rr"], box_values)
    full_hessian_det_box = det_hessian_box * hessian_rr_box
    t_box = box[2]

    audit.certify(
        "G1.local_lapse.certificate.krawczyk_strict_inclusion",
        all(strict_inclusion),
        "the Krawczyk image is strictly inside the frozen x,q,T box, certifying one unique zero of grad(S2)",
        coordinate_inclusions=strict_inclusion,
        image_delta=[ball_record(krawczyk_delta[i, 0]) for i in range(3)],
        radius=certificate["uniform_radius"],
    )
    audit.certify(
        "G1.local_lapse.certificate.proper_time_away_from_divisor",
        bool(t_box.lower() > arb(0)),
        "the certified real stationary box stays strictly in T>0 and away from the T=0 proper-time divisor",
        T=ball_record(t_box),
    )
    audit.certify(
        "G1.local_lapse.certificate.s2_hessian_invertible",
        excludes_zero(det_hessian_box),
        "det(H_S2) excludes zero throughout the certified stationary box",
        determinant=ball_record(det_hessian_box),
    )
    audit.certify(
        "G1.local_lapse.certificate.kinetic_nonzero",
        excludes_zero(kinetic_box),
        "K excludes zero throughout the certified stationary box",
        K=ball_record(kinetic_box),
    )
    audit.certify(
        "G1.local_lapse.certificate.relative_lapse_curvature_nonzero",
        excludes_zero(hessian_rr_box),
        "8*pi^2*K/T^3 excludes zero throughout the certified stationary box",
        hessian_rr=ball_record(hessian_rr_box),
    )
    audit.certify(
        "G1.local_lapse.certificate.full_extended_hessian_invertible",
        excludes_zero(full_hessian_det_box),
        "the block-factorized determinant of the full x,q,T,r Hessian excludes zero at the certified r=0 stationary point",
        determinant=ball_record(full_hessian_det_box),
    )

    return {
        "method": certificate["method"],
        "arithmetic": certificate["arithmetic"],
        "precision_bits": ctx.prec,
        "center_order": certificate["center_order"],
        "center": certificate["center"],
        "uniform_radius": certificate["uniform_radius"],
        "gradient_at_center": [ball_record(f_center[i, 0]) for i in range(3)],
        "krawczyk_delta": [
            ball_record(krawczyk_delta[i, 0]) for i in range(3)
        ],
        "strict_inclusion_by_coordinate": strict_inclusion,
        "det_hessian_s2_box": ball_record(det_hessian_box),
        "kinetic_K_box": ball_record(kinetic_box),
        "relative_lapse_hessian_box": ball_record(hessian_rr_box),
        "full_extended_hessian_determinant_box": ball_record(
            full_hessian_det_box
        ),
    }


def add_theorem_guards(audit: Audit) -> None:
    audit.guard(
        "G1.local_lapse.guard.noether_hessian_necessary_condition",
        "differentiated off-shell Noether identity at a stationary point",
        "S is twice differentiable, grad(S) dot R=0 holds off shell, z_star is an exact stationary point, and the proposed gauge generator R(z_star) is nonzero",
        "H(z_star)R(z_star)=0 is necessary; if the extended Hessian is certified invertible, it contradicts the declared relative-lapse generator with R_r=2. That application is made only by the all-certificates-passed KILL terminal.",
    )
    audit.guard(
        "G1.local_lapse.guard.configuration_scope_only",
        "scope boundary between a pushed-forward configuration action and an extended first-order constrained action",
        "the tested candidate introduces only N0,N1 into the frozen midpoint configuration action and adds no canonical variables, auxiliary fields, endpoint transform, or perfect cell action",
        "the result cannot exclude a different first-order, perfect/improved, auxiliary-field, or continuum-first BFV construction",
    )
    audit.guard(
        "G1.local_lapse.guard.no_bfv_or_relative_cycle_verdict",
        "typed-input boundary for BFV and relative-chain conclusions",
        "no first-order constraint lattice, BRST charge, gauge fermion, source equivalence, N=0 distribution, common orientation local system, cover, or all-end census is constructed",
        "the Starobinsky finite-m2 BFV source, UNIQUE_LATERAL, STOKES_SPLIT, NO_ADMISSIBLE_LIFT, Gate 1 closure, physics and TOE outputs remain unevaluated or null",
    )


def main() -> None:
    cfg, input_sha, upstream_results, upstream_files = load_input()
    audit = Audit()
    model = build_symbolic_model(audit, cfg)
    certificate = certify_stationary_point(audit, cfg, model)
    add_theorem_guards(audit)

    certificate_passed = all(item["passed"] for item in audit.certified)
    selected_row = cfg["decision_table"][0 if certificate_passed else 1]
    verdict = selected_row["verdict"]
    programme_impact = selected_row["programme_impact"]
    if certificate_passed:
        epistemic_status = (
            "COMPUTER_ASSISTED_SCOPED_NEGATIVE_RESULT_FOR_ONE_NAIVE_"
            "DISCRETE_GAUGE_MECHANISM"
        )
        research_transition = {
            "unexpected_outcome": "the natural two-local-lapse extension restricts exactly to the frozen midpoint action at r=0 but has certified nonzero curvature and no gauge null direction at the certified positive-real saddle",
            "competing_mechanisms": [
                {
                    "id": "NAIVE_MIDPOINT_TWO_LOCAL_LAPSE_UNFIXING",
                    "disposition": "RETIRED_AT_CERTIFIED_PHASE39_POSITIVE_REAL_SADDLE",
                },
                {
                    "id": "PERFECT_OR_IMPROVED_DISCRETE_GAUGE_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "CONTINUUM_FIRST_TIME_DEPENDENT_TRACE_SOURCE_WITH_CONTROLLED_DISCRETIZATION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
            ],
            "discriminating_question": "Can an exact Hamilton-principal-function or otherwise proved gauge-preserving Starobinsky element action produce one same-model finite BFV source with a controlled map, rather than exact identity by naive unfixing, to the frozen midpoint kernel?",
            "changed_future_selection": "stop trying to attach BFV data to the naive local-lapse extension of the frozen midpoint action; select an exact gauge-preserving source construction before N=0, cover, end census or source-to-fold transport",
        }
        killed_mechanism: str | None = (
            "treat the natural two-local-lapse substitution in this frozen "
            "equal-endpoint midpoint configuration action as an exact "
            "endpoint-preserving reparametrization gauge unfixing near the "
            "certified saddle"
        )
        computed_claims = [
            "the exact two-local-lapse configuration extension and its r=0 restriction",
            "the exact relative-lapse derivative and block Hessian identities",
            "a strict Arb/Krawczyk certificate for one unique positive-real S2 stationary point within the frozen box",
            "certified exclusion of zero from the S2, relative-lapse and full extended Hessian determinants at that stationary point",
        ]
    else:
        epistemic_status = (
            "INCONCLUSIVE_INTERVAL_CERTIFICATE_FOR_ONE_NAIVE_DISCRETE_"
            "GAUGE_MECHANISM"
        )
        research_transition = {
            "unexpected_outcome": "the frozen symbolic identities hold but the interval certificate did not establish the nondegeneracy required to dispose of the naive local-lapse mechanism",
            "competing_mechanisms": [
                {
                    "id": "NAIVE_MIDPOINT_TWO_LOCAL_LAPSE_UNFIXING",
                    "disposition": "OPEN_INCONCLUSIVE",
                },
                {
                    "id": "PERFECT_OR_IMPROVED_DISCRETE_GAUGE_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "CONTINUUM_FIRST_TIME_DEPENDENT_TRACE_SOURCE_WITH_CONTROLLED_DISCRETIZATION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
            ],
            "discriminating_question": "Which named interval obligation failed, and can only that certificate be repaired without changing the frozen model or box after observing the outcome?",
            "changed_future_selection": "repair only the failed certificate field; do not construct BFV, N=0, cover, end or source-to-fold objects from an inconclusive result",
        }
        killed_mechanism = None
        computed_claims = [
            "the exact two-local-lapse configuration extension and its r=0 restriction",
            "the exact relative-lapse derivative and block Hessian identities",
            "the recorded interval checks and the identity of every certificate obligation that did not pass",
        ]

    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": programme_impact,
        "epistemic_status": epistemic_status,
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "planner": cfg["planner"],
        "human_review": cfg["human_review"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_results": upstream_results,
        "upstream_files": upstream_files,
        "primary_sources": cfg["primary_sources"],
        "candidate_extension": cfg["candidate_extension"],
        "symbolic_calculation": model["symbolic_record"],
        "interval_certificate": certificate,
        "exact_checks": audit.exact,
        "certified_interval_checks": audit.certified,
        "numerical_checks": [],
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": len(audit.exact),
            "exact_total": len(audit.exact),
            "certified_interval_passed": sum(
                item["passed"] for item in audit.certified
            ),
            "certified_interval_total": len(audit.certified),
            "numerical_passed": 0,
            "numerical_total": 0,
            "theorem_guards_verified": len(audit.theorem_guards),
            "theorem_guards_total": len(audit.theorem_guards),
            "all_passed": certificate_passed,
        },
        "research_transition": research_transition,
        "claim_boundary": {
            "computed": computed_claims,
            "killed_mechanism_only": killed_mechanism,
            "not_killed": [
                "a first-order Starobinsky constraint lattice with newly derived variables and endpoint terms",
                "a perfect or improved gauge-preserving discrete action",
                "a continuum-first time-dependent trace-gauge source followed by controlled discretization",
                "a Starobinsky constraint-adapted improved-static source",
                "the frozen Starobinsky m=2 bosonic action and its existing local intersection records in their own scopes",
            ],
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations": len(audit.exact),
            "interval_certificates": 1,
            "root_calls": 0,
            "ode_calls": 0,
            "numerical_samples": 0,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "python_flint": flint.__version__,
            "arb_precision_bits": ctx.prec,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "programme_impact": programme_impact,
                "exact_passed": len(audit.exact),
                "exact_total": len(audit.exact),
                "certified_interval_passed": sum(
                    item["passed"] for item in audit.certified
                ),
                "certified_interval_total": len(audit.certified),
                "theorem_guards_verified": len(audit.theorem_guards),
                "theorem_guards_total": len(audit.theorem_guards),
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
                "gate1": "OPEN_PARTIAL_PROGRESS",
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
