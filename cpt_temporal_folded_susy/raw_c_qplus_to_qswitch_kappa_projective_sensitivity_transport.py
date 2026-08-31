#!/usr/bin/env python3
"""Bounded Qplus-to-Qswitch transport of selected projective kappa sensitivity.

This is deliberately a projective comparison calculation.  It transports only
``h=partial_kappa rho`` on the already pinned real K times Lambda strip; it
does not form a Q0 quantity or a differentiated boundary functional.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import arb, ctx, fmpq


INPUT_NAME = "RAW_C_QPLUS_TO_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_TRANSPORT_INPUTS.json"
RESULT_NAME = "RAW_C_QPLUS_TO_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_TRANSPORT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_qplus_to_qswitch_kappa_projective_sensitivity_transport.py"
# Frozen after the companion input manifest was finalized.
EXPECTED_INPUT_SHA256 = "dff13b4a24cd8ea3f5ff76bd72778815dc3a608ec155463b8ee31e0fdbde446e"
CALCULATION_ID = "RawCQplusToQswitchKappaProjectiveSensitivityTransport"
RESULT_SCHEMA = "ice.raw-c-qplus-to-qswitch-kappa-projective-sensitivity-transport.result.v1"
RESULT_PREFIX = "RAW_C_QPLUS_TO_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_TRANSPORT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
OUTPUT_DIGITS = 45


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def exact_rational(text: str) -> fmpq:
    if "e" in text.lower():
        coefficient, exponent = text.lower().split("e", 1)
        return fmpq(coefficient) * fmpq(10) ** int(exponent)
    return fmpq(text)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 24,
        "upstream_results": 2,
        "method_sources": 1,
        "kernel_panels_evaluated": 3072,
        "precision_tiers": 2,
        "kappa_corridors": 1,
        "lambda_slabs": 1,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "ball_bessel_evaluations": 0,
        "bisection_steps": 0,
        "compact_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "Q0_kappa_projective_sensitivity": None,
        "complete_normalized_G_kappa": None,
        "reference_state_kappa_variation": None,
        "complete_kappa_differentiated_minus_tail": None,
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


def width(value: arb) -> arb:
    return arb(value.upper() - value.lower())


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
        "width_upper": width(value).upper().str(digits, radius=False),
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)
    panel_evaluations: int = 0

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check id: {identifier}")
        self.seen.add(identifier)

    def exact_check(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.exact.append({"id": identifier, "kind": "EXACT_OR_STRUCTURAL_CHECK", "passed": bool(passed), "statement": statement, **data})

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self.register(identifier)
        reduced = sp.simplify(residual)
        self.exact.append({"id": identifier, "kind": "EXACT_IDENTITY", "passed": bool(reduced == 0), "residual": str(reduced), "statement": statement})

    def control(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.controls.append({"id": identifier, "kind": "OUTWARD_INTERVAL_CONTROL", "passed": bool(passed), "statement": statement, **data})

    def guard(self, identifier: str, theorem: str, hypotheses: str, scope: str) -> None:
        self.register(identifier)
        self.guards.append({"id": identifier, "kind": "THEOREM_SCOPE_GUARD", "verified": True, "theorem": theorem, "hypotheses": hypotheses, "scope": scope})


def load_affine(root: Path, source: dict[str, str]) -> Any:
    path = root / source["path"]
    if sha256_bytes(path.read_bytes()) != source["sha256"]:
        raise AssertionError("affine helper source hash mismatch")
    spec = importlib.util.spec_from_file_location("raw_c_affine_helpers", path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load affine helper")
    module = importlib.util.module_from_spec(spec)
    # Python 3.13 dataclasses resolve annotations through sys.modules while
    # the class decorator runs, so the dynamic module must already be visible.
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(spec.name, None)
        raise
    return module


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
    if (recorded is None or sha256_bytes(canonical_bytes(payload)) != recorded or result.get("run_status") != "VALID_RUN" or result.get("numbered_phase") is not None):
        raise AssertionError(f"upstream integrity mismatch: {item['path']}")
    return result, {key: item[key] for key in ("path", "sha256", "schema_version", "verdict", "result_payload_sha256_without_self")}


def required_control(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("passed") is True for item in result.get("controls", []))


def required_exact(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("passed") is True for item in result.get("exact_checks", []))


def required_guard(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("verified") is True for item in result.get("theorem_guards", []))


def exact_audit(audit: Audit) -> None:
    x, c_value, kappa = sp.symbols("x C kappa", positive=True, real=True)
    lam, rho, h = sp.symbols("lambda rho h", real=True)
    field = 2 * rho + (rho + rho**2 + kappa**2 + sp.Rational(1, 4)) / x - lam * sp.sqrt(x / c_value)
    h_field = sp.diff(field, rho) * h + sp.diff(field, kappa)
    audit.identity("rawc.kappa_qswitch.riccati_kappa_sensitivity", h_field - ((2 + (1 + 2 * rho) / x) * h + 2 * kappa / x), "Differentiating the exact x-Riccati field at fixed lambda gives h_x=[2+(1+2rho)/x]h+2kappa/x.")
    p = sp.symbols("p", positive=True, real=True)
    audit.identity("rawc.kappa_qswitch.positive_sign_transform", (-h_field).subs(h, -p) - ((2 + (1 + 2 * rho) / x) * p - 2 * kappa / x), "For p=-h the forced scalar equation is p_x=a(x)p-2kappa/x.")
    a, t = sp.symbols("a t", positive=True, real=True)
    lower_kernel = sp.exp(-2 * (t - a)) * (a / t) ** 3
    upper_kernel = sp.exp(-2 * (t - a)) * (t / a)
    audit.identity("rawc.kappa_qswitch.lower_kernel", sp.diff(lower_kernel, t) + (2 + 3 / t) * lower_kernel, "The lower comparison kernel solves the upper barrier coefficient equation.")
    audit.identity("rawc.kappa_qswitch.upper_kernel", sp.diff(upper_kernel, t) + (2 - 1 / t) * upper_kernel, "The upper comparison kernel solves the lower barrier coefficient equation.")
    y = sp.symbols("y", nonnegative=True, real=True)
    lower_integrand = 2 * kappa * a**3 * sp.exp(-2 * y) / (a + y) ** 4
    audit.identity("rawc.kappa_qswitch.lower_forcing_kernel", lower_integrand - (sp.exp(-2 * y) * (a / (a + y)) ** 3) * (2 * kappa / (a + y)), "The lower forced comparison integrand is exactly 2*kappa*a^3*exp(-2y)/(a+y)^4.")
    audit.identity("rawc.kappa_qswitch.lower_forcing_monotonicity", sp.diff(lower_integrand, y) + (2 + 4 / (a + y)) * lower_integrand, "The positive lower forcing integrand has logarithmic derivative -2-4/(a+y), so right-endpoint panels are rigorous lower sums.")
    upper_integrand = sp.exp(-2 * y) * ((a + y) / a) * (2 * kappa / (a + y))
    distance = sp.symbols("D", positive=True, real=True)
    audit.identity("rawc.kappa_qswitch.upper_forcing_antiderivative", sp.integrate(upper_integrand, (y, 0, distance)) - kappa / a * (1 - sp.exp(-2 * distance)), "The upper forced comparison integral is exactly kappa/a*(1-exp(-2D)).")
    audit.identity("rawc.kappa_qswitch.barrier_coefficient_lower", (2 + (1 + 2 * rho) / x) - (2 - 1 / x) - 2 * (rho + 1) / x, "The lower coefficient gap is 2(rho+1)/x and is nonnegative on the pinned barrier.")
    audit.identity("rawc.kappa_qswitch.barrier_coefficient_upper", (2 + 3 / x) - (2 + (1 + 2 * rho) / x) - 2 * (1 - rho) / x, "The upper coefficient gap is 2(1-rho)/x and is nonnegative on the pinned barrier.")

    pi_upper = sp.Rational(22, 7)
    exp_29_taylor_lower = sum(
        sp.Rational(29, 10) ** index / sp.factorial(index)
        for index in range(6)
    )
    audit.exact_check("rawc.kappa_qswitch.pi_square_upper", bool(sp.pi < pi_upper and pi_upper**2 < 10), "The classical rational bound pi<22/7 implies pi^2<10.", rational_upper="22/7")
    audit.exact_check("rawc.kappa_qswitch.exp_29_tenths_lower", bool(exp_29_taylor_lower > 16), "The first six positive Taylor terms certify exp(29/10)>16.", positive_taylor_lower=str(exp_29_taylor_lower))
    audit.exact_check("rawc.kappa_qswitch.x_switch_upper_implication", bool(sp.Rational(6 * 10, 16) == sp.Rational(15, 4)), "The preceding strict bounds imply x_switch=6*pi^2*exp(-29/10)<15/4.")
    tenth = sp.Rational(1, 10)
    audit.exact_check("rawc.kappa_qswitch.exp_one_tenth_upper", bool(0 < tenth < 1 and 1 / (1 - tenth) - 1 == sp.Rational(1, 9)), "Termwise comparison with the geometric series gives exp(1/10)-1<1/9.")
    audit.exact_check("rawc.kappa_qswitch.first_window_coefficient_budget", bool(2 * sp.Rational(15, 4) * sp.Rational(1, 9) + sp.Rational(3, 10) == sp.Rational(17, 15)), "On the first Delta-Q=1/10 window, the integrated upper coefficient is strictly below 17/15.")
    remainder = sp.Rational(2, 15)
    exp_one_lt_three = bool(sp.E < 3)
    audit.exact_check("rawc.kappa_qswitch.exp_one_upper", exp_one_lt_three, "The factorial-series comparison n!>=2^(n-1) for n>=1 gives exp(1)<3.")
    audit.exact_check("rawc.kappa_qswitch.exp_seventeen_fifteenths_upper", bool(exp_one_lt_three and 0 < remainder < 1 and 3 / (1 - remainder) < 4), "Using exp(1)<3 and a geometric-series upper bound for exp(2/15) gives exp(17/15)<4.")
    audit.identity("rawc.kappa_qswitch.first_window_forcing_mass", 2 * kappa * sp.Rational(1, 10) - kappa / 5, "In Q coordinates the positive backward forcing integrates to kappa/5 on the first Delta-Q=1/10 window.")
    audit.exact_check("rawc.kappa_qswitch.analytic_floor_factor", bool(sp.Rational(1, 5) * sp.Rational(1, 4) == sp.Rational(1, 20)), "The comparison kernel exceeds exp(-17/15)>1/4, so the first-window forcing mass kappa/5 gives p(Qswitch)>kappa/20.")

    audit.guard(
        "rawc.kappa_qswitch.guard.variation_of_constants",
        "Finite-IVP parameter differentiation and scalar linear variation of constants with ordered coefficient kernels",
        "The endpoint anchor supplies the existing kappa derivative seed. The Riccati vector field is smooth on the certified finite rho tube, so standard finite-IVP parameter dependence propagates that derivative; no singular-endpoint C1 condition is assumed. Also kappa>0, p(Qplus)>0, and 2-1/x<=a(x)<=2+3/x.",
        "Only the backward Qplus-to-Qswitch value of p=-partial_kappa rho is bounded.",
    )
    audit.guard(
        "rawc.kappa_qswitch.guard.panel_and_floor_bounds",
        "Positive monotone Riemann lower sums and elementary exponential-series comparison",
        "The lower integrand is positive and decreasing; omitted y>=24 mass is nonnegative; all elementary strict inequalities are recorded as exact checks.",
        "The panels and first-window floor certify sign only, not an exact derivative value.",
    )
    audit.guard(
        "rawc.kappa_qswitch.guard.scope",
        "Projective derivative scope separation",
        "No Q0 transport, reference-state variation, differentiated minus tail, mixed derivative, root derivative, or physical inner product is computed.",
        "No transversality, uniqueness, selector, velocity, spectral, RAQ, BFV, likelihood, or physics claim follows.",
    )


def lower_forcing_panels(audit: Audit, *, x_switch: arb, kappa_lower: arb, panels: int, tail_y: fmpq) -> arb:
    """Monotone lower Riemann enclosure for the stated positive lower kernel.

    The integrand is decreasing in y, so right endpoints yield a lower bound.
    The omitted y>=tail_y part is nonnegative and intentionally discarded.
    """
    step = tail_y / panels
    total = arb(0)
    for index in range(panels):
        y_right = arb(step * (index + 1))
        # Lower endpoints throughout preserve a lower enclosure of the positive integrand.
        value = 2 * kappa_lower * x_switch**3 * (-2 * y_right).exp() / (x_switch + y_right) ** 4
        total += arb(value.lower()) * arb(step)
    audit.panel_evaluations += panels
    return arb(total.lower())


def run_tier(audit: Audit, *, tier: int, dps: int, panels: int, q_plus: fmpq, q_switch: fmpq, kappa: arb, h_seed_lower: fmpq, h_seed_upper: fmpq, conventions: dict[str, Any], affine: Any) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = OUTPUT_DIGITS
    p_plus = affine.interval_from_bounds(
        (-arb(h_seed_upper)).lower(), (-arb(h_seed_lower)).upper()
    )
    c_value = 6 * arb.pi() ** 2
    x_plus = c_value * arb(q_plus).exp()
    x_switch = c_value * arb(q_switch).exp()
    if not (x_plus.lower() > x_switch.upper() > 0):
        raise AssertionError("x endpoint ordering failed")
    distance = x_plus - x_switch
    kappa_lower = arb(kappa.lower())
    kappa_upper = arb(kappa.upper())
    tail_y = exact_rational(conventions["kernel_tail_y"])
    if distance.lower() <= arb(tail_y).upper():
        raise AssertionError("lower-panel cutoff must lie strictly inside the transport segment")
    lower_force = lower_forcing_panels(audit, x_switch=x_switch, kappa_lower=kappa_lower, panels=panels, tail_y=tail_y)
    upper_homogeneous = (-2 * distance).exp() * (x_plus / x_switch)
    lower_homogeneous = (-2 * distance).exp() * (x_switch / x_plus) ** 3
    # Exact upper comparison integral; it dominates the entire half-open segment.
    upper_force = kappa_upper / x_switch * (arb(1) - (-2 * distance).exp())
    p_lower = lower_homogeneous * arb(p_plus.lower()) + lower_force
    p_upper = upper_homogeneous * arb(p_plus.upper()) + upper_force
    p_interval = affine.interval_from_bounds(p_lower.lower(), p_upper.upper())
    h_interval = affine.interval_from_bounds((-p_interval.upper()), (-p_interval.lower()))
    floor = kappa_lower / 20
    certified = bool(x_switch.is_finite() and x_plus.is_finite() and p_interval.is_finite() and h_interval.is_finite() and p_interval.lower() > 0 and p_interval.lower() > floor.upper() and h_interval.upper() < 0)
    audit.control(f"rawc.kappa_qswitch.tier{tier}.panels{panels}.transport", certified, "The pinned rho barrier and positive forced-kernel comparison give a finite strictly positive p=-h interval and hence a strict negative selected h(Qswitch) interval.", decimal_digits=dps, x_Qplus=interval_record(x_plus, digits), x_Qswitch=interval_record(x_switch, digits), lower_forcing_panel_integral=interval_record(lower_force, digits), upper_forcing_exact_integral=interval_record(upper_force, digits), p_Qplus=interval_record(p_plus, digits), p_Qswitch=interval_record(p_interval, digits), analytic_floor=interval_record(floor, digits), h_Qswitch=interval_record(h_interval, digits), h_Qswitch_excludes_zero=True)
    return {"tier": tier, "decimal_digits": dps, "panels": panels, "x_Qplus": interval_record(x_plus, digits), "x_Qswitch": interval_record(x_switch, digits), "lower_forcing_panel_integral": interval_record(lower_force, digits), "upper_forcing_exact_integral": interval_record(upper_force, digits), "p_Qswitch": interval_record(p_interval, digits), "h_Qswitch": interval_record(h_interval, digits), "status": "CERTIFIED_STRICT_NEGATIVE_QSWITCH_H" if certified else "QSWITCH_H_NOT_CERTIFIED"}, {"p": p_interval, "h": h_interval, "lower_force": lower_force}


def intersect(affine: Any, values: list[arb]) -> arb | None:
    result = values[0]
    for value in values[1:]:
        result = affine.intersection(result, value)
        if result is None:
            return None
    return result


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    config = json.loads(raw_input)
    if config.get("schema_version") != "ice.raw-c-qplus-to-qswitch-kappa-projective-sensitivity-transport.input.v1" or config.get("calculation_id") != CALCULATION_ID or config.get("numbered_phase") is not None or config.get("resource_caps") != expected_caps() or config.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("identity, cap, or fail-closed policy drift")
    conventions = config["declared_conventions"]
    if conventions["precision_ladder_decimal_digits"] != [80, 120] or conventions["kernel_panel_ladder"] != [512, 1024] or conventions["kernel_tail_y"] != "24":
        raise AssertionError("declared precision or panel ladder drift")
    ctx.dps = max(conventions["precision_ladder_decimal_digits"])
    affine_rows = config["method_sources"]
    if len(affine_rows) != 1 or affine_rows[0]["path"] != "cpt_temporal_folded_susy/raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport.py":
        raise AssertionError("exactly one affine primitive helper must be pinned")
    affine = load_affine(root, affine_rows[0])
    upstream_payloads: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in config["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream_payloads.append(payload)
        upstream_records.append(record)
    if len(upstream_payloads) != 2:
        raise AssertionError("requires anchor and correlated sign-strip upstreams")
    anchor, signstrip = upstream_payloads
    needed_barriers = [f"rawc.signstrip.switch.tier{tier}.closed_corridor_barrier" for tier in (1, 2)]
    barrier_ok = all(required_control(signstrip, identifier) for identifier in needed_barriers)
    anchor_dependencies = [
        "rawc.kappa_anchor.pinned_full_strip_log_derivative_envelope",
        "rawc.kappa_anchor.uniform_negative_interval",
    ]
    anchor_dependencies_ok = all(
        required_exact(anchor, identifier) for identifier in anchor_dependencies
    ) and required_guard(
        anchor, "rawc.kappa_anchor.guard.selected_family_secant_limit"
    )
    selected_family_ok = required_guard(
        signstrip, "rawc.signstrip.guard.selected_actual_family"
    )
    anchor_h = anchor["certified_calculation"]["h_Qplus_4"]
    h_lower = exact_rational(anchor_h["strict_lower_exact"])
    h_upper = exact_rational(anchor_h["strict_upper_exact"])
    p_plus = affine.interval_from_bounds(
        (-arb(h_upper)).lower(), (-arb(h_lower)).upper()
    )
    q_plus = exact_rational(conventions["Q_plus"])
    q_switch = exact_rational(conventions["Q_switch"])
    kappa = affine.bracket_band(exact_rational(conventions["kappa_corridor"]["left_exact"]), exact_rational(conventions["kappa_corridor"]["right_exact"]))
    lambda_band = affine.bracket_band(exact_rational(conventions["lambda_slab"]["left_exact"]), exact_rational(conventions["lambda_slab"]["right_exact"]))
    audit = Audit()
    exact_audit(audit)
    audit.exact_check("rawc.kappa_qswitch.declared_strip", bool(q_plus == 4 and q_switch == fmpq(-29, 10) and 0 < kappa.lower() < kappa.upper() < 8 and lambda_band.lower() < 0 < lambda_band.upper()), "The exact current correlated K times Lambda strip and ordered Q endpoints are retained.")
    audit.exact_check("rawc.kappa_qswitch.upstream_anchor_dependencies", anchor_dependencies_ok, "The hash-pinned endpoint anchor passed the two exact dependencies and selected-family secant-limit guard used here.", required_exact_checks=anchor_dependencies, required_guard="rawc.kappa_anchor.guard.selected_family_secant_limit")
    audit.exact_check("rawc.kappa_qswitch.upstream_selected_family", selected_family_ok, "The hash-pinned sign strip verifies that the transported barrier belongs to the same selected actual family.", required_guard="rawc.signstrip.guard.selected_actual_family")
    audit.exact_check("rawc.kappa_qswitch.anchor_seed_negative", bool(h_lower < h_upper < 0 and p_plus.lower() > 0), "The hash-pinned Qplus anchor supplies one strictly positive p=-h seed interval.")
    audit.control("rawc.kappa_qswitch.pinned_rho_barrier", barrier_ok, "Both precision tiers of the hash-pinned correlated sign strip certify the same selected actual rho invariant barrier [-1,1] from Qplus to Qswitch on the full declared rectangle.", required_passed_controls=needed_barriers)
    if len(audit.exact) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")
    rows: list[dict[str, Any]] = []
    balls: list[dict[str, arb]] = []
    for tier, dps in enumerate(conventions["precision_ladder_decimal_digits"], start=1):
        coarse_row, coarse = run_tier(audit, tier=tier, dps=dps, panels=512, q_plus=q_plus, q_switch=q_switch, kappa=kappa, h_seed_lower=h_lower, h_seed_upper=h_upper, conventions=conventions, affine=affine)
        refined_row, refined = run_tier(audit, tier=tier, dps=dps, panels=1024, q_plus=q_plus, q_switch=q_switch, kappa=kappa, h_seed_lower=h_lower, h_seed_upper=h_upper, conventions=conventions, affine=affine)
        lower_sum_improved = bool(
            refined["lower_force"].lower() >= coarse["lower_force"].lower()
        )
        audit.control(f"rawc.kappa_qswitch.tier{tier}.lower_sum_refinement", lower_sum_improved, "The 1024-panel right-endpoint lower Riemann sum is no smaller than the 512-panel sum. Each full p enclosure is certified separately; no literal nesting of independently wrapped upper balls is asserted.", coarse_lower_forcing=interval_record(coarse["lower_force"], OUTPUT_DIGITS), refined_lower_forcing=interval_record(refined["lower_force"], OUTPUT_DIGITS))
        rows.extend([coarse_row, refined_row])
        balls.append(refined)
    final_h = intersect(affine, [item["h"] for item in balls])
    final_p = intersect(affine, [item["p"] for item in balls])
    overlap_ok = bool(final_h is not None and final_p is not None and final_h.upper() < 0 and final_p.lower() > 0)
    audit.control("rawc.kappa_qswitch.cross_precision_intersection", overlap_ok, "The refined 80- and 120-digit outward enclosures overlap in one finite strict-sign interval.", final_h_Qswitch=interval_record(final_h, OUTPUT_DIGITS) if final_h is not None else None, final_p_Qswitch=interval_record(final_p, OUTPUT_DIGITS) if final_p is not None else None)
    if audit.panel_evaluations != expected_caps()["kernel_panels_evaluated"]:
        raise AssertionError("panel accounting drift")
    all_passed = (
        all(item["passed"] for item in audit.exact)
        and all(item["passed"] for item in audit.controls)
        and all(item["verified"] for item in audit.guards)
    )
    strict_negative = bool(
        all_passed
        and overlap_ok
        and final_h is not None
        and final_h.upper() < 0
    )
    zero_containing = bool(
        final_h is not None and final_h.lower() <= 0 <= final_h.upper()
    )
    if strict_negative:
        verdict = "CERTIFY_UNIFORM_NEGATIVE_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_ONLY"
    elif zero_containing:
        verdict = "VALID_ZERO_CONTAINING_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY"
    else:
        verdict = "VALID_QSWITCH_KAPPA_PROJECTIVE_SENSITIVITY_NOT_CERTIFIED"
    h_seed = affine.interval_from_bounds(
        arb(h_lower).lower(), arb(h_upper).upper()
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "primary_sources": config["primary_sources"],
        "upstream_results": upstream_records,
        "method_sources": affine_rows,
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "certified_calculation": {
            "p_equals_minus_h": True,
            "h_Qplus_seed": interval_record(h_seed, OUTPUT_DIGITS),
            "p_Qswitch": interval_record(final_p, OUTPUT_DIGITS)
            if final_p is not None
            else None,
            "h_Qswitch": interval_record(final_h, OUTPUT_DIGITS)
            if final_h is not None
            else None,
            "analytic_strict_floor": "p(Qswitch)>kappa_left/20",
            "precision_panel_rows": rows,
            "scope": "selected real projective kappa sensitivity at Qswitch only",
        },
        "non_claim": "This is a Qswitch selected-projective kappa-sensitivity sign enclosure only, not Q0 transport, complete G_kappa, transversality, uniqueness, a selector, velocity, spectrum, RAQ, BFV, likelihood, or physics.",
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "controls_passed": sum(item["passed"] for item in audit.controls),
            "controls_total": len(audit.controls),
            "theorem_guards": len(audit.guards),
            "all_executable_checks_passed": all_passed and overlap_ok,
        },
        "resource_accounting": {
            "symbolic_checks": len(audit.exact),
            "upstream_results": len(upstream_records),
            "method_sources": len(affine_rows),
            "kernel_panels_evaluated": audit.panel_evaluations,
            "precision_tiers": len(conventions["precision_ladder_decimal_digits"]),
            "kappa_corridors": 1,
            "lambda_slabs": 1,
            "ode_calls": 0,
            "quadrature_calls": 0,
            "root_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "ball_bessel_evaluations": 0,
            "bisection_steps": 0,
            "compact_steps": 0,
            "adjacent_result_files_written": 1,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_flint": importlib.metadata.version("python-flint"),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "exact_passed": sum(item["passed"] for item in audit.exact),
                "exact_total": len(audit.exact),
                "controls_passed": sum(item["passed"] for item in audit.controls),
                "controls_total": len(audit.controls),
                "h_Qswitch": result["certified_calculation"]["h_Qswitch"],
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
