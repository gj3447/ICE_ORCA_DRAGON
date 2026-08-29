#!/usr/bin/env python3
"""Node-safe lambda-zero raw-C Green endpoint certificate; not F_lambda or RAQ."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = "RAW_C_LAMBDA_ZERO_NODE_SAFE_GREEN_TRANSPORT_INPUTS.json"
RESULT_NAME = "RAW_C_LAMBDA_ZERO_NODE_SAFE_GREEN_TRANSPORT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_lambda_zero_node_safe_green_transport.py"
EXPECTED_INPUT_SHA256 = "2fc1dfbd703d665ca8b49138f8c7ef869b7eed9c83256dde6adbb4a57e8663c7"
CALCULATION_ID = "RawCLambdaZeroNodeSafeGreenTransport"
RESULT_SCHEMA = "ice.raw-c-lambda-zero-node-safe-green-transport.result.v1"
RESULT_PREFIX = "RAW_C_LAMBDA_ZERO_NODE_SAFE_GREEN_TRANSPORT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def expected_nulls() -> dict[str, Any]:
    return {
        "raw_h_trajectory_across_nodes": None,
        "nonzero_lambda_node_safe_transport": None,
        "endpoint_F_lambda_amplitude": None,
        "declared_extension_lambda_derivative": None,
        "endpoint_root_velocity": None,
        "unique_or_complete_zero_shell_root_census": None,
        "nonreal_resolvent_or_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "absolute_bfv_measure": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 1000,
        "ball_bessel_evaluations": 100000,
        "quadrature_calls": 10,
        "quadrature_callback_evaluations": 100000,
        "root_brackets": 5,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    ball: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0
    quadrature_calls: int = 0
    quadrature_callback_evaluations: int = 0

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def identity(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self.register(ident)
        reduced = sp.simplify(residual)
        self.exact.append({"id": ident, "passed": bool(reduced == 0), "statement": statement, "residual": str(reduced)})

    def ball_check(self, ident: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(ident)
        self.ball.append({"id": ident, "passed": bool(passed), "statement": statement, **data})

    def guard(self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        self.register(ident)
        self.theorem_guards.append({"id": ident, "verified": True, "verification_mode": "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_BALL_HYPOTHESIS_SCOPE_AUDIT", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})

    def count_bessel(self) -> None:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")

    def count_callback(self) -> None:
        self.quadrature_callback_evaluations += 1
        if self.quadrature_callback_evaluations > expected_caps()["quadrature_callback_evaluations"]:
            raise AssertionError("quadrature callback cap exceeded")


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    if sha256_bytes(raw) != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key, expected in (("run_status", "VALID_RUN"), ("verdict", item["required_verdict"]), ("result_payload_sha256_without_self", item["payload_sha256_without_self"])):
        if result.get(key) != expected:
            raise AssertionError(f"upstream {key} mismatch: {item['path']}")
    if result.get("numbered_phase") is not None:
        raise AssertionError("upstream numbered-phase convention drift")
    return result, {"path": item["path"], "sha256": item["sha256"], "payload_sha256_without_self": item["payload_sha256_without_self"], "verdict": item["required_verdict"]}


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def bracket_band(left: fmpq, right: fmpq) -> arb:
    return arb(arb((left + right) / 2), arb((right - left) / 2))


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if upper < lower:
        raise AssertionError("reversed interval bounds")
    value = arb((lower + upper) / 2, (upper - lower) / 2)
    if not (value.lower() <= lower and value.upper() >= upper):
        raise AssertionError("outward interval construction failed")
    return value


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {"lower": value.lower().str(digits, radius=False), "upper": value.upper().str(digits, radius=False), "width_upper": (value.upper() - value.lower()).upper().str(digits, radius=False), "midpoint_radius": value.str(digits)}


def complex_ball_record(value: acb, digits: int) -> dict[str, Any]:
    return {"real": interval_record(value.real, digits), "imag": interval_record(value.imag, digits), "absolute_lower": value.abs_lower().str(digits, radius=False), "absolute_upper": value.abs_upper().str(digits, radius=False)}


def contains_zero(value: arb) -> bool:
    return bool(value.lower() <= 0 <= value.upper())


def bessel_k(audit: Audit, x: acb, order: acb) -> acb:
    audit.count_bessel()
    return x.bessel_k(order)


def identity_audit(audit: Audit) -> None:
    u, uq, v, vq, a0, al = sp.symbols("u u_Q v v_Q A_0 A_lambda", nonzero=True)

    def d_q(expr: sp.Expr) -> sp.Expr:
        return sp.expand(sp.diff(expr, u) * uq + sp.diff(expr, uq) * a0 * u + sp.diff(expr, v) * vq + sp.diff(expr, vq) * (a0 * v + al * u))

    wronskian = u * vq - uq * v
    h = (uq * v - u * vq) / u**2
    j = -wronskian
    audit.identity("rawc.green.wronskian_forcing", d_q(wronskian) - al * u**2, "For v_QQ=A_0*v+A_lambda*u, W_Q(u,v)=A_lambda*u^2.")
    audit.identity("rawc.green.smooth_flux", j - u**2 * h, "J=-W(u,v)=u^2*h is smooth even where the quotient h is undefined.")
    audit.identity("rawc.green.smooth_flux_equation", d_q(j) + al * u**2, "The smooth flux obeys J_Q=-A_lambda*u^2 and is propagated without a Riccati quotient.")
    c0, c1 = sp.symbols("c_0 c_1", nonzero=True)
    audit.identity("rawc.green.rescaling_J", (-(c0 * u) * (c0 * vq + c1 * uq) + (c0 * uq) * (c0 * v + c1 * u)) - c0**2 * j, "J scales by c(0)^2 under a lambda-dependent amplitude rescaling, while h=J/u^2 is invariant.")
    x, c = sp.symbols("x C", positive=True)
    density = c * (x / c) ** sp.Rational(3, 2) / x
    audit.identity("rawc.green.Q_to_x_density", density - sp.sqrt(x) / sp.sqrt(c), "A_lambda*dQ becomes C^(-1/2)*sqrt(x)*dx under x=C*exp(Q).")
    X = sp.symbols("X", positive=True)
    audit.identity("rawc.green.tail_antiderivative", sp.diff(sp.exp(-2 * X) / 2, X) + sp.exp(-2 * X), "The exponential factor in the analytic Green tail has exact antiderivative exp(-2X)/2.")
    f0 = sp.symbols("F_0")
    fl, u0, v0 = sp.symbols("F_lambda u_0 v_0", nonzero=True)
    endpoint_wronskian = u0 * fl - f0 * v0
    audit.identity("rawc.green.finite_proxy_at_zero", endpoint_wronskian.subs(f0, 0) - u0 * fl, "At a zero of the finite-Q0 proxy F_0=u_Q(Q0), endpoint evaluation gives W(u,v)=u(Q0)*partial_lambda F_0; this does not identify the proxy with the declared extension away from lambda=0.")


def h_box_from_upstream(row: dict[str, Any]) -> arb:
    record = row.get("certified_h_Qplus_intersection")
    if not isinstance(record, dict):
        raise AssertionError("missing certified h(4) intersection")
    return interval_from_bounds(arb(record["lower"]), arb(record["upper"]))


def run_tier(audit: Audit, *, root_index: int, tier_index: int, band: arb, h_plus: arb, dps: int, rel_tol: str, abs_tol: str, max_j_width: str, max_h_width: str, cfg: dict[str, Any]) -> tuple[dict[str, Any], arb | None, arb | None]:
    ctx.dps = dps
    conventions = cfg["declared_conventions"]
    digits = int(conventions["ball_output_digits"])
    c = 6 * arb.pi() ** 2
    sqrt_c = c.sqrt()
    x0 = c * arb(-4).exp()
    xplus = c * arb(4).exp()
    cutoff = arb(conventions["finite_cutoff_X"])
    order = acb(0, band)
    k0 = bessel_k(audit, acb(x0), order)
    kplus = bessel_k(audit, acb(xplus), order)
    endpoint_denominator_ok = bool(k0.is_finite() and contains_zero(k0.imag) and k0.abs_lower() > 0 and not contains_zero(k0.real))
    audit.ball_check(f"rawc.green.root{root_index}.tier{tier_index}.endpoint_denominator", endpoint_denominator_ok, "The full kappa-band K_(i*kappa)(x0) ball is real and excludes zero, so only the endpoint quotient h(Q0)=J(Q0)/u(Q0)^2 is permitted.", K_Q0=complex_ball_record(k0, digits))
    bridge = h_plus * (kplus.real ** 2)
    bridge_ok = bool(kplus.is_finite() and contains_zero(kplus.imag) and kplus.abs_lower() > 0 and bridge.lower() > 0)
    audit.ball_check(f"rawc.green.root{root_index}.tier{tier_index}.plus_end_magnitude", bridge_ok, "Using the exact real-valuedness theorem, the pinned h(4) box times the independently evaluated real u(4)^2 reconstructs a finite positive J(4) magnitude sentinel; this is not a Qplus-to-Q0 decomposition check.", J_Qplus_magnitude=interval_record(bridge, digits))
    if not (endpoint_denominator_ok and bridge_ok):
        return {"decimal_digits": dps, "status": "UNRESOLVED_DENOMINATOR_OR_BRIDGE", "J_Q0": None, "h_Q0": None}, None, None

    stats = {"analytic_true": 0, "analytic_false": 0}

    def integrand(x: acb, analytic: bool) -> acb:
        audit.count_callback()
        stats["analytic_true" if analytic else "analytic_false"] += 1
        if x.real.lower() <= 0:
            return acb("nan")
        return x.sqrt(analytic=analytic) * bessel_k(audit, x, order) ** 2

    audit.quadrature_calls += 1
    if audit.quadrature_calls > expected_caps()["quadrature_calls"]:
        raise AssertionError("quadrature call cap exceeded")
    options = conventions["quadrature_options"]
    finite = acb.integral(integrand, acb(x0), acb(cutoff), rel_tol=arb(rel_tol), abs_tol=arb(abs_tol), deg_limit=int(options["deg_limit"]), eval_limit=int(options["eval_limit_each"]), depth_limit=int(options["depth_limit"]), use_heap=bool(options["use_heap"]), verbose=False)
    finite_ok = bool(finite.is_finite() and contains_zero(finite.imag) and finite.real.lower() > 0)
    audit.ball_check(f"rawc.green.root{root_index}.tier{tier_index}.finite_green_integral", finite_ok, "The finite acb.integral imaginary enclosure contains zero and its real enclosure is strictly positive on the full band; exact real-valuedness is supplied separately by Bessel conjugation and order symmetry, and no h quotient occurs on this path.", callback_stats=stats, finite_integral=complex_ball_record(finite, digits), finite_integral_real_width_upper=(finite.real.upper() - finite.real.lower()).upper().str(digits, radius=False), requested_relative_tolerance=rel_tol, requested_absolute_tolerance=abs_tol)
    tail = arb.pi() * (-2 * cutoff).exp() / (4 * sqrt_c * cutoff.sqrt())
    tail_ok = bool(tail.is_finite() and tail.lower() >= 0 and tail.upper() < arb(conventions["tail_upper_target"]).lower() and bridge.upper() < tail.upper())
    audit.ball_check(f"rawc.green.root{root_index}.tier{tier_index}.analytic_tail_and_plus_magnitude", tail_ok, "The DLMF majorant bounds the full x>=X endpoint Green tail, while the independently reconstructed J(4) magnitude is below that coarse allowance; this is only a non-contradiction scale sentinel, not a transport equality.", tail_upper=tail.upper().str(digits, radius=False), J_Qplus_magnitude_upper=bridge.upper().str(digits, radius=False), tail_target=conventions["tail_upper_target"])
    if not (finite_ok and tail_ok):
        return {"decimal_digits": dps, "status": "UNRESOLVED_FINITE_INTEGRAL_OR_TAIL", "finite_integral": complex_ball_record(finite, digits), "J_Q0": None, "h_Q0": None}, None, None

    j_ball = interval_from_bounds(finite.real.lower() / sqrt_c.upper(), finite.real.upper() / sqrt_c.lower() + tail.upper())
    k0_sq = k0.real ** 2
    h0 = j_ball / k0_sq
    j_ok = bool(j_ball.lower() > 0 and (j_ball.upper() - j_ball.lower()).upper() < arb(max_j_width).lower())
    h_ok = bool(h0.lower() > 0 and (h0.upper() - h0.lower()).upper() < arb(max_h_width).lower())
    audit.ball_check(f"rawc.green.root{root_index}.tier{tier_index}.endpoint_boxes", j_ok and h_ok, "The direct smooth J(Q0) Green box and, using the exact Bessel reality theorem, its endpoint-only h(Q0)=J/u^2 quotient are positive and meet the declared width bounds; h was never evolved across an interior node.", J_Q0=interval_record(j_ball, digits), h_Q0=interval_record(h0, digits), maximum_J_width=max_j_width, maximum_h_width=max_h_width)
    return {"decimal_digits": dps, "status": "CERTIFIED_TIER" if j_ok and h_ok else "UNRESOLVED_WIDTH", "same_backend_repeat": True, "relative_tolerance": rel_tol, "absolute_tolerance": abs_tol, "callback_stats": stats, "K_Q0": complex_ball_record(k0, digits), "K_Qplus": complex_ball_record(kplus, digits), "J_Qplus_magnitude_sanity": interval_record(bridge, digits), "finite_integral": complex_ball_record(finite, digits), "analytic_tail_upper": tail.upper().str(digits, radius=False), "J_Q0": interval_record(j_ball, digits), "h_Q0": interval_record(h0, digits)}, j_ball if j_ok and h_ok else None, h0 if j_ok and h_ok else None


def intersect(left: arb, right: arb) -> arb | None:
    low = left.lower() if left.lower() >= right.lower() else right.lower()
    high = left.upper() if left.upper() <= right.upper() else right.upper()
    return interval_from_bounds(low, high) if low <= high else None


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    if importlib.metadata.version("python-flint") != "0.9.0":
        raise AssertionError("python-flint runtime version drift")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.raw-c-lambda-zero-node-safe-green-transport.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls() or cfg["declared_conventions"]["precision_ladder_decimal_digits"] != [80, 120]:
        raise AssertionError("resource or fail-closed mutation")
    root = Path(__file__).resolve().parent.parent
    bessel, htail = (verify_upstream(root, item) for item in cfg["upstream_results"])
    bessel_data, bessel_record = bessel
    htail_data, htail_record = htail
    bessel_rows = bessel_data["certified_calculation"]["endpoint_characteristic"]["root_rows"]
    h_rows = htail_data["certified_calculation"]["root_bracket_rows"]
    if len(bessel_rows) != expected_caps()["root_brackets"] or len(h_rows) != expected_caps()["root_brackets"]:
        raise AssertionError("five-bracket upstream count drift")
    audit = Audit()
    identity_audit(audit)
    conventions = cfg["declared_conventions"]
    ctx.dps = max(conventions["precision_ladder_decimal_digits"])
    c_guard = 6 * arb.pi() ** 2
    x0_guard = c_guard * arb(-4).exp()
    cutoff_guard = arb(conventions["finite_cutoff_X"])
    xplus_guard = c_guard * arb(4).exp()
    cutoff_order_ok = bool(x0_guard.lower() > 0 and x0_guard.upper() < cutoff_guard.lower() and cutoff_guard.upper() < xplus_guard.lower())
    audit.ball_check("rawc.green.cutoff_order", cutoff_order_ok, "The outward balls certify 0<x0<X<xplus, so the finite positive-real integration segment and the manual x>=X tail precede the separately reconstructed plus endpoint.", x0=interval_record(x0_guard, int(conventions["ball_output_digits"])), cutoff=interval_record(cutoff_guard, int(conventions["ball_output_digits"])), xplus=interval_record(xplus_guard, int(conventions["ball_output_digits"])))
    rows: list[dict[str, Any]] = []
    for index, (brow, hrow) in enumerate(zip(bessel_rows, h_rows, strict=True), start=1):
        cert = brow["certified_high_precision_bracket"]
        left, right = exact_rational(cert["left_exact"]), exact_rational(cert["right_exact"])
        if not left < right:
            raise AssertionError("upstream bracket ordering drift")
        h_bracket = hrow.get("kappa_bracket")
        if not isinstance(h_bracket, dict) or h_bracket.get("left_exact") != str(left) or h_bracket.get("right_exact") != str(right):
            raise AssertionError("upstream h-tail and Bessel bracket alignment drift")
        hplus = h_box_from_upstream(hrow)
        ctx.dps = max(conventions["precision_ladder_decimal_digits"])
        coverage = bracket_band(left, right)
        coverage_ok = bool(coverage.lower() <= left and coverage.upper() >= right)
        audit.ball_check(f"rawc.green.root{index}.band_coverage", coverage_ok, "The outward-rounded Arb parameter interval covers the exact-rational full upstream root bracket.", left_exact=str(left), right_exact=str(right), coverage=interval_record(coverage, int(conventions["ball_output_digits"])))
        tier_records: list[dict[str, Any]] = []
        j_tiers: list[arb | None] = []
        h_tiers: list[arb | None] = []
        for tier, (dps, rel, absolute, max_j, max_h) in enumerate(zip(conventions["precision_ladder_decimal_digits"], conventions["quadrature_relative_tolerances"], conventions["quadrature_absolute_tolerances"], conventions["maximum_J_widths"], conventions["maximum_endpoint_h_widths"], strict=True), start=1):
            record, j_value, h_value = run_tier(audit, root_index=index, tier_index=tier, band=bracket_band(left, right), h_plus=hplus, dps=int(dps), rel_tol=rel, abs_tol=absolute, max_j_width=max_j, max_h_width=max_h, cfg=cfg)
            tier_records.append(record)
            j_tiers.append(j_value)
            h_tiers.append(h_value)
        j_refined = intersect(j_tiers[0], j_tiers[1]) if j_tiers[0] is not None and j_tiers[1] is not None else None
        h_refined = intersect(h_tiers[0], h_tiers[1]) if h_tiers[0] is not None and h_tiers[1] is not None else None
        refinement_ok = bool(j_refined is not None and h_refined is not None and (j_tiers[1].upper() - j_tiers[1].lower()).upper() < (j_tiers[0].upper() - j_tiers[0].lower()).lower() and (h_tiers[1].upper() - h_tiers[1].lower()).upper() < (h_tiers[0].upper() - h_tiers[0].lower()).lower()) if j_tiers[0] is not None and j_tiers[1] is not None and h_tiers[0] is not None and h_tiers[1] is not None else False
        audit.ball_check(f"rawc.green.root{index}.precision_refinement", refinement_ok, "The two same-backend rigorous endpoint boxes overlap and the 120-digit boxes are strictly narrower; their intersections are retained as consistency refinements only.", J_Q0_intersection=interval_record(j_refined, int(conventions["ball_output_digits"])) if j_refined else None, h_Q0_intersection=interval_record(h_refined, int(conventions["ball_output_digits"])) if h_refined else None)
        rows.append({"root_index": index, "kappa_bracket": {"left_exact": str(left), "right_exact": str(right), "width_exact": str(right - left), "coverage_ball": interval_record(coverage, int(conventions["ball_output_digits"]))}, "h_Qplus_upstream": interval_record(hplus, int(conventions["ball_output_digits"])), "precision_tiers": tier_records, "certified_J_Q0_intersection": interval_record(j_refined, int(conventions["ball_output_digits"])) if refinement_ok and j_refined else None, "certified_h_Q0_intersection": interval_record(h_refined, int(conventions["ball_output_digits"])) if refinement_ok and h_refined else None, "finite_Q0_proxy_conditional_at_root": "partial_lambda F_0/u(Q0)=-h(Q0) only if F_0=u_Q(Q0)=0; not a declared-extension lambda derivative or eigenvalue slope"})
    audit.guard("rawc.green.guard.node_safe_flux", "Lagrange/Green identity", "J=-W(u,partial_lambda u)=u^2h and J_Q=-A_lambda*u^2 on the declared lambda-zero Bessel fiber", "The direct Green integral constructs only the smooth Wronskian endpoint and never evolves h=u^{-2}J through an interior zero of u.")
    audit.guard("rawc.green.guard.dlmf_tail", "DLMF 10.32.9 integral representation and Gaussian majorant", "x>0, kappa real, |cos(kappa t)|<=1 and cosh(t)>=1+t^2/2", "The manually added x>=64 tail is bounded by pi*exp(-2X)/(4*sqrt(C*X)); no unbounded numerical quadrature is used.")
    audit.guard("rawc.green.guard.acb_integral", "python-flint 0.9.0 acb.integral", "finite positive-real path, callback cap, unconditional Re(x)>0 rejection, and sqrt analytic flag", "Finite integral values are rigorous complex-ball enclosures over full kappa bands; same-backend tiers are not independent implementations.")
    audit.guard("rawc.green.guard.bessel_reality", "Bessel conjugation plus K-order symmetry", "x>0 and kappa is real on every full parameter band", "K_(i*kappa)(x) is exactly real; the executable complex enclosures must contain zero in their imaginary parts, after which real-part squares are used for endpoint magnitude and quotient bounds.")
    audit.guard("rawc.green.guard.finite_proxy_scope", "finite-Q0 Wronskian identity", "The declared raw-C Gamma_1 is a minus-end Wronskian limit and its equality with u_Q(Q0) was pinned only at lambda=0", "The conditional relation for the finite-Q0 lambda-zero proxy is not a declared-extension derivative, eigenvalue slope or root velocity.")
    audit.guard("rawc.green.guard.scope", "endpoint scope boundary", "Only lambda=0 five-bracket smooth Green boxes are emitted", "No raw h trajectory, nonzero-lambda transport, F_lambda amplitude, declared extension derivative, root velocity, m-function, spectrum, RAQ, physics or TOE conclusion follows.")
    passed = all(item["passed"] for item in audit.exact + audit.ball) and audit.quadrature_calls == expected_caps()["quadrature_calls"] and audit.bessel_evaluations <= expected_caps()["ball_bessel_evaluations"] and audit.quadrature_callback_evaluations <= expected_caps()["quadrature_callback_evaluations"]
    decision = cfg["decision_table"][0 if passed else 1]
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": decision["verdict"], "programme_impact": decision["programme_impact"], "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)}, "upstream_results": [bessel_record, htail_record], "primary_sources": cfg["primary_sources"], "declared_conventions": conventions, "assumptions": cfg["assumptions"], "exact_checks": audit.exact, "ball_checks": audit.ball, "theorem_guards": audit.theorem_guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "ball_passed": sum(item["passed"] for item in audit.ball), "ball_total": len(audit.ball), "theorem_guard_count": len(audit.theorem_guards), "all_executable_checks_passed": passed}, "certified_calculation": {"status": "CERTIFIED_LAMBDA_ZERO_NODE_SAFE_GREEN_WRONSKIAN_ENDPOINT_CONSTRUCTION_ON_FIVE_FULL_KAPPA_BRACKETS" if passed else "NOT_CERTIFIED", "method_scope": "direct exact Green-integral endpoint construction, not numerical propagation of the upstream Qplus datum", "smooth_variable": "J=-W(u,partial_lambda u)=u^2 h", "endpoint_formula": "J(Q0)=C^(-1/2)*integral_x0^infinity sqrt(x)K_(i*kappa)(x)^2 dx", "raw_h_evolved_across_nodes": False, "root_bracket_rows": rows, "finite_Q0_proxy_scope": "At a zero of F_0=u_Q(Q0), partial_lambda F_0/u(Q0)=-h(Q0); this is not a declared raw-C extension derivative or root velocity.", "next_mathematical_gap": "declare and validate a nonzero-lambda minus-end boundary functional before treating any finite-Q0 proxy derivative as an extension eigenvalue slope"}, "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"ball_bessel_evaluations": audit.bessel_evaluations, "ball_bessel_evaluation_cap": expected_caps()["ball_bessel_evaluations"], "quadrature_calls": audit.quadrature_calls, "quadrature_call_cap": expected_caps()["quadrature_calls"], "quadrature_callback_evaluations": audit.quadrature_callback_evaluations, "quadrature_callback_evaluation_cap": expected_caps()["quadrature_callback_evaluations"], "root_calls": 0, "finite_difference_calls": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "sympy": sp.__version__, "python_flint": importlib.metadata.version("python-flint"), "platform": platform.platform()}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": result["verdict"], "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "ball_passed": result["check_summary"]["ball_passed"], "ball_total": result["check_summary"]["ball_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "certified_brackets": sum(row["certified_J_Q0_intersection"] is not None for row in rows) if passed else 0, "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded), "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
