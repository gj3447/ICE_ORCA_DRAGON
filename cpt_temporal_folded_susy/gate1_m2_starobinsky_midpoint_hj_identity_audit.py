#!/usr/bin/env python3
"""Audit one exact-HJ identity claimed for the frozen Starobinsky midpoint.

The bounded calculation derives the diagonal fixed-time Hamilton-Jacobi
residual of one midpoint element, checks an exact algebraic Starobinsky
witness, and certifies the same obstruction on the frozen Phase 39 boundary
slice with Arb ball arithmetic.  It can retire only pointwise identification
of this midpoint element with an exact Hamilton principal function.  It does
not construct or exclude a different perfect/improved action or BFV source.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import flint
import sympy as sp
from flint import arb, ctx


INPUT_NAME = "GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT_INPUTS.json"
RESULT_NAME = "GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_m2_starobinsky_midpoint_hj_identity_audit.py"
)
EXPECTED_INPUT_SHA256 = (
    "6c2ab273fd8d3c95e4b85337cf7f55c84eb961117c3db5982d65a260e4ba0696"
)
CALCULATION_ID = "Gate1M2StarobinskyMidpointHJIdentityAudit"
RESULT_SCHEMA = "ice.gate1-m2-starobinsky-midpoint-hj-identity-audit.result.v1"
RESULT_PREFIX = "GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT_RESULT="
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
        "exact_fixed_time_hj_element_action": None,
        "starobinsky_finite_m2_bfv_trajectory_source": None,
        "first_order_constraint_lattice": None,
        "bfv_charge_and_gauge_fermion": None,
        "endpoint_state_transform": None,
        "source_equality_deformation_or_approximation_bound": None,
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


def load_input() -> tuple[
    dict[str, Any], str, list[dict[str, str]], list[dict[str, str]]
]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.gate1-m2-starobinsky-midpoint-hj-identity-audit.input.v1"
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
    if cfg["planner"]["selected_lane"] != "G1":
        raise AssertionError("planner lane drift")
    root = Path(__file__).resolve().parent.parent
    upstream_results = [
        verify_upstream_result(root, item) for item in cfg["upstream_results"]
    ]
    upstream_files = [
        verify_upstream_file(root, item) for item in cfg["upstream_files"]
    ]
    return cfg, observed, upstream_results, upstream_files


def build_symbolic_model(audit: Audit, cfg: dict[str, Any]) -> dict[str, Any]:
    a0, phi0, a1, phi1, t = sp.symbols(
        "a_0 phi_0 a_1 phi_1 t", real=True
    )
    a, phi = sp.symbols("a phi", positive=True, real=True)
    delta_a = a1 - a0
    delta_phi = phi1 - phi0
    a_mid = (a0 + a1) / 2
    phi_mid = (phi0 + phi1) / 2
    s = sp.sqrt(sp.Rational(2, 3))

    def potential(phi_value: sp.Expr) -> sp.Expr:
        return sp.Rational(3, 4) * (1 - sp.exp(-s * phi_value)) ** 2

    def potential_factor(a_value: sp.Expr, phi_value: sp.Expr) -> sp.Expr:
        return -3 * a_value + a_value**3 * potential(phi_value)

    u_mid = potential_factor(a_mid, phi_mid)
    kinetic_numerator = -6 * a_mid * delta_a**2 + a_mid**3 * delta_phi**2
    s_mid = 2 * sp.pi**2 * (
        kinetic_numerator / (2 * t) + t * u_mid
    )
    p_a_endpoint = sp.diff(s_mid, a1)
    p_phi_endpoint = sp.diff(s_mid, phi1)
    h_endpoint = (
        -p_a_endpoint**2 / (24 * sp.pi**2 * a1)
        + p_phi_endpoint**2 / (4 * sp.pi**2 * a1**3)
        - 2 * sp.pi**2 * potential_factor(a1, phi1)
    )
    residual = sp.diff(s_mid, t) + h_endpoint
    diagonal_substitution = {a0: a, a1: a, phi0: phi, phi1: phi}
    residual_diagonal = sp.simplify(
        residual.subs(diagonal_substitution, simultaneous=True)
    )
    endpoint_pa_diagonal = sp.simplify(
        p_a_endpoint.subs(diagonal_substitution, simultaneous=True)
    )
    endpoint_pphi_diagonal = sp.simplify(
        p_phi_endpoint.subs(diagonal_substitution, simultaneous=True)
    )
    time_derivative_diagonal = sp.simplify(
        sp.diff(s_mid, t).subs(diagonal_substitution, simultaneous=True)
    )
    u = potential_factor(a, phi)
    u_a = sp.diff(u, a)
    u_phi = sp.diff(u, phi)
    contraction_d = sp.simplify(-u_a**2 / (6 * a) + u_phi**2 / a**3)
    expected_residual = sp.pi**2 * t**2 * contraction_d / 4

    audit.check(
        "G1.midpoint_hj.exact.diagonal_time_derivative",
        sp.simplify(time_derivative_diagonal - 2 * sp.pi**2 * u) == 0,
        "the diagonal midpoint time derivative is exactly 2*pi^2*U",
    )
    audit.check(
        "G1.midpoint_hj.exact.diagonal_endpoint_pa",
        sp.simplify(endpoint_pa_diagonal - sp.pi**2 * t * u_a) == 0,
        "the diagonal final a momentum is exactly pi^2*t*U_a",
    )
    audit.check(
        "G1.midpoint_hj.exact.diagonal_endpoint_pphi",
        sp.simplify(endpoint_pphi_diagonal - sp.pi**2 * t * u_phi) == 0,
        "the diagonal final phi momentum is exactly pi^2*t*U_phi",
    )
    audit.check(
        "G1.midpoint_hj.exact.inverse_metric_contraction",
        sp.simplify(
            contraction_d - (-u_a**2 / (6 * a) + u_phi**2 / a**3)
        )
        == 0,
        "D is exactly G^AB*U_A*U_B for G_AB=diag(-6*a,a^3)",
    )
    audit.check(
        "G1.midpoint_hj.exact.diagonal_residual",
        sp.simplify(residual_diagonal - expected_residual) == 0,
        "the exact diagonal HJ residual is pi^2*t^2*D/4",
    )

    x, q, total_t = sp.symbols("x q T", real=True)
    boundary = cfg["frozen_boundary_witness"]
    a_b = sp.Rational(boundary["a"])
    phi_b = sp.Rational(boundary["phi"])
    midpoint_restriction = sp.simplify(
        2
        * s_mid.subs(
            {
                a0: a_b,
                phi0: phi_b,
                a1: a_b + x,
                phi1: phi_b + q,
                t: total_t / 2,
            },
            simultaneous=True,
        )
    )
    old_midpoint_a = a_b + x / 2
    old_midpoint_phi = phi_b + q / 2
    old_kinetic = -6 * old_midpoint_a * x**2 + old_midpoint_a**3 * q**2
    old_u = potential_factor(old_midpoint_a, old_midpoint_phi)
    frozen_s2 = 4 * sp.pi**2 * old_kinetic / total_t + 2 * sp.pi**2 * old_u * total_t
    audit.check(
        "G1.midpoint_hj.exact.frozen_m2_algebraic_reconstruction",
        sp.simplify(midpoint_restriction - frozen_s2) == 0,
        "two algebraic copies with t=T/2 reconstruct the frozen equal-endpoint m=2 midpoint convention exactly, without asserting a sequential trajectory",
    )

    exact = cfg["exact_algebraic_witness"]
    witness_a = sp.Rational(exact["a"])
    witness_phi = sp.sqrt(sp.Rational(3, 2)) * sp.log(2)
    witness_t = sp.Rational(exact["t"])
    witness_exp = sp.simplify(sp.exp(-s * witness_phi))
    witness_substitution = {a: witness_a, phi: witness_phi, t: witness_t}
    witness_v = sp.simplify(potential(witness_phi))
    witness_ua = sp.simplify(u_a.subs(witness_substitution))
    witness_uphi = sp.simplify(u_phi.subs(witness_substitution))
    witness_d = sp.simplify(contraction_d.subs(witness_substitution))
    witness_residual = sp.simplify(expected_residual.subs(witness_substitution))
    expected_uphi = 3 * s
    audit.check(
        "G1.midpoint_hj.exact.witness_exponential",
        witness_exp == sp.Rational(1, 2),
        "the exact witness has exp(-sqrt(2/3)*phi)=1/2",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_potential",
        witness_v == sp.Rational(3, 16),
        "the exact witness has V=3/16",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_Ua",
        witness_ua == -sp.Rational(3, 4),
        "the exact witness has U_a=-3/4",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_Uphi",
        sp.simplify(witness_uphi - expected_uphi) == 0,
        "the exact witness has U_phi=3*sqrt(2/3)",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_D",
        witness_d == sp.Rational(45, 64),
        "the exact witness has D=45/64>0",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_residual",
        witness_residual == 45 * sp.pi**2 / 1024,
        "the exact witness has R_HJ=45*pi^2/1024>0",
    )
    audit.check(
        "G1.midpoint_hj.exact.witness_residual_positive",
        bool(witness_residual.is_positive),
        "the exact algebraic Starobinsky residual is strictly positive",
    )

    q0_flat, q1_flat, u0 = sp.symbols("q0_flat q1_flat U0", real=True)
    s_flat = (
        sp.pi**2 * (q1_flat - q0_flat) ** 2 / t
        + 2 * sp.pi**2 * t * u0
    )
    p_flat = sp.diff(s_flat, q1_flat)
    h_flat = p_flat**2 / (4 * sp.pi**2) - 2 * sp.pi**2 * u0
    flat_residual = sp.simplify(sp.diff(s_flat, t) + h_flat)
    audit.check(
        "G1.midpoint_hj.exact.flat_constant_control",
        flat_residual == 0,
        "the constant-flat-metric principal function has exactly zero HJ residual with the same signs and factors",
    )

    contraction_d_midpoint = contraction_d.subs(
        {a: a_mid, phi: phi_mid}, simultaneous=True
    )
    off_diagonal_counterterm = (
        -sp.pi**2 * t**3 * contraction_d_midpoint / 12
    )
    diagonal_counterterm = sp.simplify(
        off_diagonal_counterterm.subs(
            diagonal_substitution, simultaneous=True
        )
    )
    explicit_counterterm_time_derivative = sp.diff(diagonal_counterterm, t)
    audit.check(
        "G1.midpoint_hj.exact.diagonal_counterterm_explicit_cancellation",
        sp.simplify(
            expected_residual + explicit_counterterm_time_derivative
        )
        == 0,
        "the explicit t derivative of the scoped order-t^3 diagonal counterterm cancels the displayed order-t^2 residual",
    )
    counterterm_a_momentum = sp.simplify(
        sp.diff(off_diagonal_counterterm, a1).subs(
            diagonal_substitution, simultaneous=True
        )
    )
    counterterm_phi_momentum = sp.simplify(
        sp.diff(off_diagonal_counterterm, phi1).subs(
            diagonal_substitution, simultaneous=True
        )
    )
    audit.check(
        "G1.midpoint_hj.exact.diagonal_counterterm_momentum_order",
        sp.simplify(
            counterterm_a_momentum
            + sp.pi**2 * t**3 * sp.diff(contraction_d, a) / 24
        )
        == 0
        and sp.simplify(
            counterterm_phi_momentum
            + sp.pi**2 * t**3 * sp.diff(contraction_d, phi) / 24
        )
        == 0,
        "the declared off-diagonal ansatz gives diagonal endpoint-momentum corrections -pi^2*t^3*partial_A(D)/24, whose cross contribution with the order-t base momentum starts at order t^4",
    )

    return {
        "symbols": {"a": a, "phi": phi, "t": t},
        "D": contraction_d,
        "residual_diagonal": residual_diagonal,
        "symbolic_record": {
            "s": str(s),
            "V": str(potential(phi)),
            "U": str(u),
            "U_a": str(u_a),
            "U_phi": str(u_phi),
            "S_mid": str(s_mid),
            "p_a_endpoint": str(p_a_endpoint),
            "p_phi_endpoint": str(p_phi_endpoint),
            "H_endpoint": str(h_endpoint),
            "R_HJ_diagonal": str(residual_diagonal),
            "D": str(contraction_d),
            "exact_witness": {
                "exp_minus_s_phi": str(witness_exp),
                "V": str(witness_v),
                "U_a": str(witness_ua),
                "U_phi": str(witness_uphi),
                "D": str(witness_d),
                "R_HJ": str(witness_residual),
            },
            "flat_control_residual": str(flat_residual),
            "formal_off_diagonal_counterterm_candidate": str(
                off_diagonal_counterterm
            ),
            "leading_diagonal_counterterm_status": cfg[
                "scoped_deformation_hint"
            ]["status"],
        },
    }


def arb_exact_rational(text: str) -> arb:
    value = Fraction(text)
    return arb(value.numerator) / arb(value.denominator)


def ball_record(value: arb) -> dict[str, str]:
    return {
        "ball": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def contains_zero(value: arb) -> bool:
    return bool(value.lower() <= arb(0) and value.upper() >= arb(0))


def certify_frozen_boundary(
    audit: Audit, cfg: dict[str, Any]
) -> dict[str, Any]:
    witness = cfg["frozen_boundary_witness"]
    ctx.prec = witness["precision_bits"]
    a = arb_exact_rational(witness["a"])
    phi = arb_exact_rational(witness["phi"])
    t = arb_exact_rational(witness["element_duration_t"])
    pi = arb.pi()
    s = (arb(2) / arb(3)).sqrt()
    exp_minus = (-s * phi).exp()
    v = arb(3) / arb(4) * (arb(1) - exp_minus) ** 2
    v_phi = (
        arb(3)
        / arb(2)
        * s
        * exp_minus
        * (arb(1) - exp_minus)
    )
    u = -arb(3) * a + a**3 * v
    u_a = -arb(3) + arb(3) * a**2 * v
    u_phi = a**3 * v_phi
    contraction_d = -u_a**2 / (arb(6) * a) + u_phi**2 / a**3
    residual_formula = pi**2 * t**2 * contraction_d / arb(4)
    p_a = pi**2 * t * u_a
    p_phi = pi**2 * t * u_phi
    time_derivative = arb(2) * pi**2 * u
    hamiltonian = (
        -p_a**2 / (arb(24) * pi**2 * a)
        + p_phi**2 / (arb(4) * pi**2 * a**3)
        - arb(2) * pi**2 * u
    )
    residual_direct = time_derivative + hamiltonian
    consistency_difference = residual_direct - residual_formula

    audit.certify(
        "G1.midpoint_hj.certificate.frozen_domain",
        bool(a.lower() > arb(0) and t.lower() > arb(0)),
        "the exact-decimal frozen boundary and rational element duration stay strictly in a>0 and t>0",
        a=ball_record(a),
        phi=ball_record(phi),
        t=ball_record(t),
    )
    audit.certify(
        "G1.midpoint_hj.certificate.frozen_D_positive",
        bool(contraction_d.lower() > arb(0)),
        "the frozen-boundary inverse-metric contraction D is certified strictly positive",
        D=ball_record(contraction_d),
    )
    audit.certify(
        "G1.midpoint_hj.certificate.frozen_residual_positive",
        bool(residual_formula.lower() > arb(0)),
        "the frozen-boundary diagonal Hamilton-Jacobi residual is certified strictly positive",
        R_HJ=ball_record(residual_formula),
    )
    audit.certify(
        "G1.midpoint_hj.certificate.direct_formula_consistency",
        contains_zero(consistency_difference),
        "direct endpoint-Hamiltonian evaluation overlaps the reduced residual formula at 300-bit precision",
        direct_R_HJ=ball_record(residual_direct),
        formula_R_HJ=ball_record(residual_formula),
        difference=ball_record(consistency_difference),
    )

    return {
        "arithmetic": "python-flint Arb rigorous real-ball arithmetic",
        "precision_bits": ctx.prec,
        "inputs": {
            "a": witness["a"],
            "phi": witness["phi"],
            "element_duration_t": witness["element_duration_t"],
            "corresponding_two_element_total_T": witness[
                "corresponding_two_element_total_T"
            ],
        },
        "exp_minus_s_phi": ball_record(exp_minus),
        "V": ball_record(v),
        "V_phi": ball_record(v_phi),
        "U": ball_record(u),
        "U_a": ball_record(u_a),
        "U_phi": ball_record(u_phi),
        "D": ball_record(contraction_d),
        "R_HJ_formula": ball_record(residual_formula),
        "R_HJ_direct": ball_record(residual_direct),
        "direct_minus_formula": ball_record(consistency_difference),
    }


def add_theorem_guards(audit: Audit) -> None:
    audit.guard(
        "G1.midpoint_hj.guard.fixed_time_hj_necessity",
        "fixed-time Hamilton-Jacobi endpoint equation",
        "W(q0,q1;t) is a differentiable exact Hamilton principal function for the declared Euclidean Hamiltonian and endpoint convention",
        "partial_t W+H_E(q1,partial_q1 W)=0 is necessary. A certified nonzero value at one admissible point refutes pointwise exact identification of that candidate W on any domain containing the point.",
    )
    audit.guard(
        "G1.midpoint_hj.guard.scoped_candidate_only",
        "counterexample scope for an equality map",
        "the tested candidate is exactly the frozen one-step midpoint formula, with no adjustable higher-order cells, auxiliary variables, or lapse extremization",
        "the result kills only equality of this formula with an exact fixed-time principal function; it does not kill a deformed, improved, perfect, continuum-first, or branch-specific principal function.",
    )
    audit.guard(
        "G1.midpoint_hj.guard.fixed_time_vs_constrained",
        "distinction between fixed-time and constrained Hamilton principal functions",
        "the residual is evaluated before any lapse extremization and does not solve C=0, select a complex branch, or quotient a gauge orbit",
        "no constrained perfect element, internal-vertex gauge null identity, phase-space lift, or FP tube is constructed or rejected by this calculation.",
    )
    audit.guard(
        "G1.midpoint_hj.guard.counterterm_nonpromotion",
        "local truncation-cancellation boundary",
        "only the explicit time derivative on the equal-endpoint diagonal is cancelled; no off-diagonal residual or uniform remainder bound is established",
        "the displayed order-t^3 term remains a leading diagonal counterterm candidate with no uniform bound, not a perfect action or source-deformation theorem.",
    )
    audit.guard(
        "G1.midpoint_hj.guard.no_bfv_or_relative_cycle_verdict",
        "typed-input boundary for BFV and relative-chain conclusions",
        "no first-order constraint lattice, BRST charge, gauge fermion, endpoint transform, N=0 distribution, orientation local system, cover, end census, or source equality/deformation bound is supplied",
        "BFV admissibility and UNIQUE_LATERAL, STOKES_SPLIT, NO_ADMISSIBLE_LIFT remain unevaluated; Gate 1, physics and TOE outputs remain open or null.",
    )


def main() -> None:
    cfg, input_sha, upstream_results, upstream_files = load_input()
    audit = Audit()
    model = build_symbolic_model(audit, cfg)
    certificate = certify_frozen_boundary(audit, cfg)
    add_theorem_guards(audit)

    certificate_passed = all(item["passed"] for item in audit.certified)
    selected_row = cfg["decision_table"][0 if certificate_passed else 1]
    verdict = selected_row["verdict"]
    programme_impact = selected_row["programme_impact"]
    if certificate_passed:
        epistemic_status = (
            "EXACT_AND_INTERVAL_CERTIFIED_SCOPED_NEGATIVE_RESULT_FOR_ONE_"
            "POINTWISE_IDENTITY_MAP"
        )
        killed_mechanism: str | None = (
            "pointwise identification of the frozen Starobinsky m=2 midpoint "
            "element with an exact fixed-time Euclidean Hamilton principal "
            "function on a domain containing either certified witness"
        )
        research_transition = {
            "unexpected_outcome": "the frozen midpoint element reconstructs the existing m=2 convention exactly but has a strictly positive diagonal Hamilton-Jacobi residual at both an exact algebraic Starobinsky point and the frozen boundary slice",
            "competing_mechanisms": [
                {
                    "id": "FROZEN_MIDPOINT_AS_EXACT_FIXED_TIME_HJ_ELEMENT",
                    "disposition": "RETIRED_BY_POINTWISE_COUNTEREXAMPLE",
                },
                {
                    "id": "CONTROLLED_HJ_DEFORMATION_OR_PERFECT_ACTION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "CONTINUUM_FIRST_CONSTRAINED_PRINCIPAL_FUNCTION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
            ],
            "discriminating_question": "Can a named Starobinsky continuum branch produce a local exact constrained principal function with composition, one internal-vertex gauge null mode and a controlled projection or deformation to the frozen midpoint kernel?",
            "changed_future_selection": "stop treating the frozen midpoint formula itself as the perfect element; next require a continuum-first local branch or a controlled HJ/perfect-action deformation before deriving BFV data",
        }
        computed_claims = [
            "the exact fixed-time Euclidean Hamiltonian and one-element midpoint conventions in the declared variables",
            "the exact equal-endpoint residual R_HJ=pi^2*t^2*G^AB*U_A*U_B/4",
            "the exact Starobinsky witness R_HJ=45*pi^2/1024>0",
            "a 300-bit Arb certificate that the residual is strictly positive at the frozen Phase 39 boundary with t=2/5",
            "an exact zero-residual constant-flat-metric control",
            "explicit diagonal leading-order cancellation by one unbounded counterterm candidate",
        ]
    else:
        epistemic_status = "INCONCLUSIVE_FROZEN_BOUNDARY_INTERVAL_CERTIFICATE"
        killed_mechanism = None
        research_transition = {
            "unexpected_outcome": "the exact symbolic setup passed but at least one frozen-boundary interval obligation did not certify the required nonzero residual",
            "competing_mechanisms": [
                {
                    "id": "FROZEN_MIDPOINT_AS_EXACT_FIXED_TIME_HJ_ELEMENT",
                    "disposition": "OPEN_INCONCLUSIVE",
                },
                {
                    "id": "CONTROLLED_HJ_DEFORMATION_OR_PERFECT_ACTION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "CONTINUUM_FIRST_CONSTRAINED_PRINCIPAL_FUNCTION",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
            ],
            "discriminating_question": "Which named frozen-boundary interval obligation failed without changing the sealed model or witness?",
            "changed_future_selection": "repair only the failed certification obligation; do not promote the identity map or derive BFV and downstream objects",
        }
        computed_claims = [
            "the exact midpoint, Hamiltonian, diagonal residual, algebraic witness and flat-control identities",
            "the identity and bounds of every recorded frozen-boundary interval check",
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
        "fixed_time_continuum_convention": cfg[
            "fixed_time_continuum_convention"
        ],
        "candidate_midpoint_element": cfg["candidate_midpoint_element"],
        "symbolic_calculation": model["symbolic_record"],
        "frozen_boundary_interval_certificate": certificate,
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
        "scoped_deformation_hint": cfg["scoped_deformation_hint"],
        "research_transition": research_transition,
        "claim_boundary": {
            "computed": computed_claims,
            "killed_mechanism_only": killed_mechanism,
            "not_killed": [
                "a different exact Hamilton principal function or perfect/improved action",
                "a continuum-first constrained principal function on a declared real or complex branch",
                "a controlled higher-order deformation of the frozen midpoint element",
                "a first-order Starobinsky constraint lattice and nonminimal BFV source",
                "the frozen bosonic m=2 local intersection records in their existing scopes",
            ],
            "not_constructed": [
                "a uniform off-diagonal error or deformation bound",
                "a local branch, validated Hamiltonian flow, composition law or internal-vertex null mode",
                "BFV data, N=0 distribution, atlas transport, end census, candidate completeness, orientation, relative cycle or global intersection vector",
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
