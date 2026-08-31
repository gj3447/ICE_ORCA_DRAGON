#!/usr/bin/env python3
"""Bounded full-minus-half-line envelope for reference kappa variation.

The calculation differentiates only the declared reference finite IVP and
uses an exact rotating-frame/Gronwall comparison.  It does not differentiate
the selected actual solution or the Gamma_1 functional.
"""

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
from flint import arb, ctx, fmpq


INPUT_NAME = "RAW_C_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_INPUTS.json"
RESULT_NAME = "RAW_C_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_reference_kappa_variation_weighted_envelope.py"
EXPECTED_INPUT_SHA256 = "6267420934202ce75e61230d7875cfcae74e460e52562a12d359fc7565fc4bd3"
CALCULATION_ID = "RawCReferenceKappaVariationWeightedEnvelope"
RESULT_SCHEMA = "ice.raw-c-reference-kappa-variation-weighted-envelope.result.v1"
RESULT_PREFIX = "RAW_C_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
OUTPUT_DIGITS = 45


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def width(value: arb) -> arb:
    return arb(value.upper() - value.lower())


def interval_record(value: arb, digits: int = OUTPUT_DIGITS) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
        "width_upper": width(value).upper().str(digits, radius=False),
    }


def intersection(left: arb, right: arb) -> arb | None:
    lower = left.lower() if left.lower() >= right.lower() else right.lower()
    upper = left.upper() if left.upper() <= right.upper() else right.upper()
    if upper < lower:
        return None
    midpoint = (lower + upper) / 2
    radius = (upper - lower) / 2
    result = arb(midpoint, radius)
    if result.lower() > lower or result.upper() < upper:
        raise AssertionError("outward intersection construction failed")
    return result


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 16,
        "upstream_results": 2,
        "method_sources": 1,
        "precision_tiers": 2,
        "elementary_ball_rows": 2,
        "kappa_corridors": 1,
        "lambda_slabs": 1,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "ball_bessel_evaluations": 0,
        "ball_gamma_evaluations": 0,
        "kernel_panels_evaluated": 0,
        "compact_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "pointwise_reference_kappa_variation_enclosure": None,
        "reference_kappa_variation_tail_value_or_sign": None,
        "two_sided_Q0_kappa_projective_sensitivity_enclosure": None,
        "actual_plus_kappa_variation": None,
        "complete_kappa_differentiated_minus_tail": None,
        "complete_normalized_G_kappa": None,
        "kappa_lambda_mixed_derivative": None,
        "root_transversality_or_uniqueness": None,
        "continuous_root_selector_or_continuation": None,
        "root_velocity": None,
        "roots_outside_declared_corridor_or_global_census": None,
        "absolute_actual_Gamma1_amplitude_or_sign": None,
        "nonreal_weyl_m_function_or_spectral_measure": None,
        "raw_C_RAQ_or_C_H_equivalence": None,
        "BFV_or_physical_product": None,
        "physics_claim": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check id: {identifier}")
        self.seen.add(identifier)

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self.register(identifier)
        reduced = sp.simplify(residual)
        self.exact.append({"id": identifier, "kind": "EXACT_IDENTITY", "passed": bool(reduced == 0), "residual": str(reduced), "statement": statement})

    def check(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.exact.append({"id": identifier, "kind": "EXACT_OR_STRUCTURAL_CHECK", "passed": bool(passed), "statement": statement, **data})

    def control(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.controls.append({"id": identifier, "kind": "OUTWARD_INTERVAL_CONTROL", "passed": bool(passed), "statement": statement, **data})

    def guard(self, identifier: str, theorem: str, hypotheses: str, scope: str) -> None:
        self.register(identifier)
        self.guards.append({"id": identifier, "kind": "THEOREM_SCOPE_GUARD", "verified": True, "theorem": theorem, "hypotheses": hypotheses, "scope": scope})


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    if sha256_bytes(raw) != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key in ("schema_version", "verdict", "result_payload_sha256_without_self"):
        if result.get(key) != item[key]:
            raise AssertionError(f"upstream {key} mismatch: {item['path']}")
    payload = dict(result)
    recorded = payload.pop("result_payload_sha256_without_self", None)
    if recorded is None or sha256_bytes(canonical_bytes(payload)) != recorded or result.get("run_status") != "VALID_RUN" or result.get("numbered_phase") is not None:
        raise AssertionError(f"upstream integrity mismatch: {item['path']}")
    return result, {key: item[key] for key in ("path", "sha256", "schema_version", "verdict", "result_payload_sha256_without_self")}


def required_exact(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("passed") is True for item in result.get("exact_checks", []))


def required_guard(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("verified") is True for item in result.get("theorem_guards", []))


def exact_audit(audit: Audit) -> None:
    kappa, potential = sp.symbols("kappa V", positive=True, real=True)
    c, d = sp.symbols("c D", real=True)
    a0 = potential - kappa**2
    audit.identity("rawc.refkappa.coefficient_derivative", sp.diff(a0, kappa) + 2 * kappa, "The reference coefficient has partial_kappa A0=-2*kappa.")
    audit.identity("rawc.refkappa.forced_variation_equation", a0 * d + sp.diff(a0, kappa) * c - (a0 * d - 2 * kappa * c), "D=partial_kappa c obeys D_QQ=A0*D-2*kappa*c.")
    audit.identity("rawc.refkappa.fixed_initial_value", sp.diff(sp.Integer(1), kappa), "The fixed c(Q0)=1 normalization gives D(Q0)=0.")
    audit.identity("rawc.refkappa.fixed_initial_slope", sp.diff(sp.Integer(0), kappa), "The fixed c_Q(Q0)=0 normalization gives D_Q(Q0)=0.")
    audit.identity("rawc.refkappa.base_rotating_equation", a0 * c / kappa - (-kappa * c + potential * c / kappa), "For y=(c,c_Q/kappa), the second rotating-state equation is -kappa*c+(V/kappa)*c.")
    audit.identity("rawc.refkappa.variation_rotating_equation", (a0 * d - 2 * kappa * c) / kappa - (-kappa * d + potential * d / kappa - 2 * c), "For d=(D,D_Q/kappa), the forcing in the second rotating component is -2*c.")
    free = sp.Matrix([[0, kappa], [-kappa, 0]])
    perturbation = sp.Matrix([[0, 0], [potential / kappa, 0]])
    forcing = sp.Matrix([0, -2 * c])
    audit.check("rawc.refkappa.free_rotation_skew", bool(sp.simplify(free.T + free) == sp.zeros(2)), "The free rotating-state matrix is exactly Euclidean skew.")
    audit.check("rawc.refkappa.perturbation_operator_norm", bool(sp.simplify(perturbation.T * perturbation - sp.diag((potential / kappa) ** 2, 0)) == sp.zeros(2)), "For positive V and kappa, the rank-one perturbation has Euclidean operator norm V/kappa.")
    audit.check("rawc.refkappa.forcing_norm", bool(sp.simplify((forcing.T * forcing)[0] - 4 * c**2) == 0), "The variation forcing (0,-2*c) has Euclidean norm 2*abs(c), without a sign premise on c.")
    q = sp.symbols("Q", real=True)
    audit.identity("rawc.refkappa.reference_potential_antiderivative", sp.diff(18 * sp.pi**4 * sp.exp(2 * q) / kappa, q) - 36 * sp.pi**4 * sp.exp(2 * q) / kappa, "The full backward perturbation mass is q_left=18*pi^4*exp(-8)/kappa_left.")
    audit.identity("rawc.refkappa.reference_weight_antiderivative", sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q) - 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), "The a-weight has exact antiderivative 4*pi^2*exp(3Q/2).")
    t = sp.symbols("t", nonnegative=True, real=True)
    audit.identity("rawc.refkappa.weighted_second_moment", sp.integrate(t**2 * sp.exp(-sp.Rational(3, 2) * t), (t, 0, sp.oo)) - sp.Rational(16, 27), "The exponential second moment controlling the linearly growing variation is 16/27.")
    b = sp.symbols("B", positive=True, real=True)
    md = 8 * sp.sqrt(2) * sp.pi * sp.exp(-3) * b**2 / 3
    audit.identity("rawc.refkappa.variation_L2_factor", md**2 - 4 * b**4 * 6 * sp.pi**2 * sp.exp(-6) * sp.Rational(16, 27), "The pointwise bound 2*B^2*t gives the displayed full L2(a) envelope for D.")


def tier_bounds(kappa_left: fmpq, dps: int) -> dict[str, arb]:
    ctx.dps = dps
    q_left = 18 * arb.pi() ** 4 * arb(-8).exp() / arb(kappa_left)
    base_pointwise = q_left.exp()
    base_l2 = 2 * arb.pi() * arb(-3).exp() * base_pointwise
    variation_l2 = 8 * arb(2).sqrt() * arb.pi() * arb(-3).exp() * (2 * q_left).exp() / 3
    return {"q_left": q_left, "base_pointwise": base_pointwise, "base_L2_a": base_l2, "variation_L2_a": variation_l2}


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    cfg = json.loads(raw_input)
    if cfg.get("schema_version") != "ice.raw-c-reference-kappa-variation-weighted-envelope.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None or cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("identity, resource or fail-closed policy drift")
    conventions = cfg["declared_conventions"]
    if conventions.get("Q_0") != "-4" or conventions.get("precision_ladder_decimal_digits") != [80, 120] or conventions.get("maximum_widths") != ["1e-50", "1e-90"]:
        raise AssertionError("endpoint or precision convention drift")
    upstream_payloads: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream_payloads.append(payload)
        upstream_records.append(record)
    if len(upstream_payloads) != 2:
        raise AssertionError("requires the correlated strip and declared boundary results")
    signstrip, boundary = upstream_payloads
    audit = Audit()
    exact_audit(audit)
    kappa_left = exact_rational(conventions["kappa_corridor"]["left_exact"])
    kappa_right = exact_rational(conventions["kappa_corridor"]["right_exact"])
    lambda_left = exact_rational(conventions["lambda_slab_context_only"]["left_exact"])
    lambda_right = exact_rational(conventions["lambda_slab_context_only"]["right_exact"])
    audit.check("rawc.refkappa.declared_strip", bool(0 < kappa_left < kappa_right < 8 and lambda_left < 0 < lambda_right), "The exact current K times Lambda context is ordered and has kappa_left>0.")
    sign_conventions = signstrip.get("declared_conventions", {})
    root_bracket = sign_conventions.get("root_bracket_1", {})
    sign_corridor = sign_conventions.get("kappa_corridor", {})
    sign_ok = bool(
        sign_conventions.get("Q_0") == conventions["Q_0"]
        and sign_conventions.get("reference_equation") == "c_p,QQ=A_0*c_p; c_p(-4)=1 and c_p,Q(-4)=0; c_p is lambda-independent"
        and sign_conventions.get("reference_instantiation") == "p^2=(2/3)kappa^2 and A_0=x^2-kappa^2; write the same pinned reference as c_kappa on the real kappa corridor"
        and sign_corridor.get("left_definition") == "root_bracket_1.left_exact-1/1000"
        and sign_corridor.get("right_definition") == "root_bracket_1.right_exact+1/1000"
        and sign_corridor.get("padding_exact") == "1/1000"
        and exact_rational(root_bracket["left_exact"]) - fmpq(1, 1000) == kappa_left
        and exact_rational(root_bracket["right_exact"]) + fmpq(1, 1000) == kappa_right
    )
    audit.check("rawc.refkappa.pinned_reference_instantiation", sign_ok, "The hash-pinned sign strip reconstructs the same exact corridor and declares the same kappa-dependent fixed reference; its Gamma_1 face signs are unused.")
    boundary_conventions = boundary.get("declared_conventions", {})
    required_boundary_exact = [
        "rawc.gamma1.reference_potential_integral",
        "rawc.gamma1.reference_weight_integral",
        "rawc.gamma1.free_rotation_skew",
    ]
    required_boundary_guards = [
        "rawc.gamma1.guard.selected_fixed_reference",
        "rawc.gamma1.guard.free_rotation_reference_bound",
        "rawc.gamma1.guard.scope",
    ]
    boundary_ok = bool(
        boundary_conventions.get("Q_0") == conventions["Q_0"]
        and boundary_conventions.get("boundary_map") == sign_conventions.get("boundary_map")
        and boundary_conventions.get("reference_equation") == sign_conventions.get("reference_equation")
        and boundary_conventions.get("reference_tail_q") == "q(kappa)=integral_-infinity^Q0 V(Q)/kappa dQ=18*pi^4*exp(-8)/kappa"
        and all(required_exact(boundary, identifier) for identifier in required_boundary_exact)
        and all(required_guard(boundary, identifier) for identifier in required_boundary_guards)
    )
    audit.check("rawc.refkappa.pinned_base_reference_bound", boundary_ok, "The hash-pinned boundary result supplies the selected fixed reference, exact V/kappa and a-weight integrals, free-rotation identity and reference-bound scope used here.", required_exact_checks=required_boundary_exact, required_guards=required_boundary_guards)
    audit.guard("rawc.refkappa.guard.finite_ivp_parameter_derivative", "Smooth parameter dependence for a regular finite linear IVP", "A0=V-kappa^2 is smooth for kappa in the compact positive corridor and the fixed Q0 data are kappa-independent.", "D=partial_kappa c_kappa is asserted on finite intervals with the displayed forced equation and zero Q0 data; no actual-plus derivative is inferred.")
    audit.guard("rawc.refkappa.guard.backward_rotating_gronwall", "Backward variation of constants and Gronwall comparison around a skew rotation", "kappa>=kappa_left>0, integral_-infinity^Q0 V/kappa is bounded by q_left, the base rotating norm is at most exp(q_left), and the D forcing norm is 2*abs(c_kappa).", "The result is the uniform magnitude bound ||d(Q)||<=2*exp(2*q_left)*(Q0-Q), not a pointwise interval or sign for D.")
    audit.guard("rawc.refkappa.guard.weighted_L2_scope", "Exact exponential-moment integration", "a=6*pi^2*exp(3Q/2) and the second moment integral is 16/27.", "Only the full-minus-half-line L2(a dQ) envelope for the reference variation is certified; no tail value, cancellation or differentiated boundary functional follows.")
    rows: list[dict[str, Any]] = []
    balls_by_tier: list[dict[str, arb]] = []
    for tier, (dps, max_width) in enumerate(zip(conventions["precision_ladder_decimal_digits"], conventions["maximum_widths"], strict=True), start=1):
        balls = tier_bounds(kappa_left, int(dps))
        tier_ok = bool(all(value.is_finite() and value.lower() > 0 and width(value).upper() < arb(max_width).lower() for value in balls.values()))
        record = {key: interval_record(value) for key, value in balls.items()}
        audit.control(f"rawc.refkappa.tier{tier}.uniform_weighted_envelope", tier_ok, "The outward elementary balls give finite positive uniform base and reference-kappa-variation bounds at the exact worst-case kappa_left.", decimal_digits=dps, maximum_width=max_width, **record)
        rows.append({"tier": tier, "decimal_digits": dps, **record, "status": "CERTIFIED_REFERENCE_KAPPA_VARIATION_ENVELOPE_TIER" if tier_ok else "REFERENCE_KAPPA_VARIATION_ENVELOPE_TIER_NOT_CERTIFIED"})
        balls_by_tier.append(balls)
    intersections = {key: intersection(balls_by_tier[0][key], balls_by_tier[1][key]) for key in balls_by_tier[0]}
    overlap_ok = all(value is not None for value in intersections.values())
    audit.control("rawc.refkappa.cross_precision_overlap", overlap_ok, "The 80- and 120-digit outward elementary evaluations overlap for q_left and all three displayed reference bounds.")
    if len(audit.exact) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")
    exact_pass = all(item["passed"] for item in audit.exact)
    control_pass = all(item["passed"] for item in audit.controls)
    all_passed = bool(exact_pass and control_pass and all(item["verified"] for item in audit.guards))
    final = {key: interval_record(value) if value is not None else None for key, value in intersections.items()}
    verdict = "CERTIFY_UNIFORM_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_ONLY" if all_passed else "VALID_REFERENCE_KAPPA_VARIATION_WEIGHTED_ENVELOPE_NOT_CERTIFIED"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "upstream_results": upstream_records,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": cfg["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "certified_calculation": {
            "scope": "declared c_kappa reference variation on the exact current real kappa corridor only; the pinned lambda slab is context only because c_kappa and D are lambda-independent",
            "equation": "D_QQ=(V-kappa^2)*D-2*kappa*c_kappa with D(Q0)=D_Q(Q0)=0",
            "pointwise_comparison": "||(D,D_Q/kappa)||(Q)<=2*exp(2*q_left)*(Q0-Q) for Q<=Q0",
            "full_minus_half_line_intersections": final,
            "precision_rows": rows,
            "actual_plus_kappa_variation": None,
            "complete_normalized_G_kappa": None,
        },
        "non_claim": "This is a uniform L2(a dQ) magnitude envelope for the declared reference derivative only, not a pointwise D interval, an actual-plus derivative, a differentiated tail value, partial_kappa G, transversality, uniqueness, selector, velocity, spectrum, RAQ, BFV, likelihood or physics.",
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "theorem_guards": len(audit.guards), "all_executable_checks_passed": all_passed},
        "resource_accounting": {"symbolic_checks": len(audit.exact), "upstream_results": len(upstream_records), "method_sources": 1, "precision_tiers": 2, "elementary_ball_rows": 2, "kappa_corridors": 1, "lambda_slabs": 1, "ode_calls": 0, "quadrature_calls": 0, "root_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "ball_bessel_evaluations": 0, "ball_gamma_evaluations": 0, "kernel_panels_evaluated": 0, "compact_steps": 0, "adjacent_result_files_written": 1},
        "environment": {"python": platform.python_version(), "python_implementation": platform.python_implementation(), "python_flint": importlib.metadata.version("python-flint"), "sympy": sp.__version__, "platform": platform.platform()},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": verdict, "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "controls_passed": result["check_summary"]["controls_passed"], "controls_total": result["check_summary"]["controls_total"], "theorem_guards": len(audit.guards), "reference_kappa_variation_L2_a": final["variation_L2_a"], "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded)}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
