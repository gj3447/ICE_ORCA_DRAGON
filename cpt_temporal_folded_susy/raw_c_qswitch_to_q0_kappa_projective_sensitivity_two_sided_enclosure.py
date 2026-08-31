#!/usr/bin/env python3
"""Bounded two-sided Qswitch-to-Q0 kappa projective-sensitivity enclosure.

The runner transports the selected actual U state together with the scalar
integral J_Q=-U^2.  The exact Wronskian identity then encloses h(Q0) without
constructing the pointwise kappa variation Y or a differentiated tail.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import arb, ctx, fmpq

import raw_c_actual_nonzero_lambda_hybrid_validated_transfer as hybrid


INPUT_NAME = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_TWO_SIDED_ENCLOSURE_INPUTS.json"
RESULT_NAME = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_TWO_SIDED_ENCLOSURE_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_qswitch_to_q0_kappa_projective_sensitivity_two_sided_enclosure.py"
EXPECTED_INPUT_SHA256 = "18718b766da4cc7d4dc57163bb2d92236a882f5aa99b3eeaaa4a95934e8a27cb"
CALCULATION_ID = "RawCQswitchToQ0KappaProjectiveSensitivityTwoSidedEnclosure"
RESULT_SCHEMA = "ice.raw-c-qswitch-to-q0-kappa-projective-sensitivity-two-sided-enclosure.result.v1"
RESULT_PREFIX = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_TWO_SIDED_ENCLOSURE_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def exact_rational(text: str) -> fmpq:
    return hybrid.exact_rational(text)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return hybrid.interval_record(value, digits)


def interval_from_record(value: dict[str, str]) -> arb:
    return hybrid.interval_from_bounds(arb(exact_rational(value["lower"])), arb(exact_rational(value["upper"])))


def intersection(left: arb, right: arb) -> arb | None:
    return hybrid.intersection(left, right)


def all_intersection(values: list[arb | None]) -> arb | None:
    if not values or values[0] is None:
        return None
    result = values[0]
    for value in values[1:]:
        if result is None or value is None:
            return None
        result = intersection(result, value)
    return result


def absolute_upper(value: arb) -> arb:
    return hybrid.absolute_upper(value)


def maximum(left: arb, right: arb) -> arb:
    return hybrid.maximum(left, right)


def symmetric(radius: arb) -> arb:
    return hybrid.symmetric_interval(radius)


def excludes_zero(value: arb) -> bool:
    return hybrid.excludes_zero(value)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 18,
        "upstream_results": 3,
        "method_sources": 1,
        "precision_tiers": 2,
        "segment_ladder_rows": 2,
        "transfer_rows": 4,
        "compact_steps": 96,
        "compact_taylor_order": 12,
        "kappa_corridors": 1,
        "lambda_slabs": 1,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "kernel_panels_evaluated": 0,
        "ball_bessel_evaluations": 0,
        "bisection_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "absolute_actual_plus_amplitude_or_kappa_derivative": None,
        "pointwise_actual_kappa_variation_on_open_Qswitch_Q0_leg": None,
        "pole_free_or_no_node_chart_on_open_Qswitch_Q0_leg": None,
        "actual_kappa_variation_full_minus_half_line": None,
        "reference_kappa_variation_or_differentiated_reference_tail": None,
        "complete_kappa_differentiated_minus_tail": None,
        "complete_normalized_G_kappa_or_Gamma1_kappa_derivative": None,
        "kappa_lambda_mixed_derivative": None,
        "root_transversality_or_monotonicity_or_uniqueness": None,
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
        passed = all(sp.simplify(item) == 0 for item in reduced) if isinstance(reduced, sp.MatrixBase) else bool(reduced == 0)
        self.exact.append({"id": identifier, "kind": "EXACT_IDENTITY", "passed": passed, "residual": str(reduced), "statement": statement})

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
    keys = ("path", "sha256", "schema_version", "verdict", "result_payload_sha256_without_self")
    return result, {key: item[key] for key in keys}


def required_pass(result: dict[str, Any], collection: str, identifier: str, field: str) -> bool:
    return any(item.get("id") == identifier and item.get(field) is True for item in result.get(collection, []))


def exact_audit(audit: Audit) -> None:
    kappa, potential, u, uq, y, yq = sp.symbols("kappa A U U_Q Y Y_Q", real=True)
    w = u * yq - uq * y
    wq = uq * yq + u * (potential * y - 2 * kappa * u) - potential * u * y - uq * yq
    audit.identity("rawc.kappa_q0_twosided.wronskian_derivative", wq + 2 * kappa * u**2, "For Y=partial_kappa U, W(U,Y)_Q=-2*kappa*U^2.")
    p = sp.symbols("p_switch", real=True)
    j_q = -u**2
    audit.identity("rawc.kappa_q0_twosided.wronskian_J_conservation", wq - 2 * kappa * j_q, "Because J_Q=-U^2, W-2*kappa*J is constant; W(Qswitch)=p_switch and J(Qswitch)=0 give W(Q0)=p_switch+2*kappa*J(Q0).")
    h_expression = (uq * y - u * yq) / u**2
    audit.identity("rawc.kappa_q0_twosided.projective_wronskian", h_expression + w / u**2, "Differentiating -U_Q/U gives the projective derivative h=-W/U^2 wherever the endpoint U is nonzero.")
    audit.identity("rawc.kappa_q0_twosided.switch_wronskian_seed", (sp.Integer(1) * p - uq * 0) - p, "Switch normalization U=1, Y=0 and Y_Q=p_switch gives W(Qswitch)=p_switch.")
    audit.identity("rawc.kappa_q0_twosided.J_equation", sp.diff(-u**2, u) * uq + 2 * u * uq, "The derivative of -U^2 is the first exact jet identity used for J_Q=-U^2.")
    audit.identity("rawc.kappa_q0_twosided.normalized_endpoint_value", y / u - u * y / u**2, "Differentiating Z(Q0)=U(Q0)/U(Q0)=1 gives Z_kappa(Q0)=0.")
    normalized_derivative_slope = (u * yq - uq * y) / u**2
    audit.identity("rawc.kappa_q0_twosided.normalized_tail_seed", normalized_derivative_slope + h_expression, "For Z=U/U(Q0), Z_kappa(Q0)=0 and Z_kappa,Q(Q0)=-h(Q0).")
    audit.identity("rawc.kappa_q0_twosided.partition16", 16 * sp.Rational(-11, 160) - (sp.Rational(-4) - sp.Rational(-29, 10)), "Sixteen exact backward steps join Qswitch to Q0.")
    audit.identity("rawc.kappa_q0_twosided.partition32", 32 * sp.Rational(-11, 320) - (sp.Rational(-4) - sp.Rational(-29, 10)), "Thirty-two exact backward steps join Qswitch to Q0.")


def apply_coefficient_derivative(derivative: int, coefficient_values: list[arb], state: tuple[arb, arb]) -> tuple[arb, arb]:
    if derivative == 0:
        return state[1], coefficient_values[0] * state[0]
    return arb(0), coefficient_values[derivative] * state[0]


def nonnegative_part(value: arb) -> arb | None:
    if not value.is_finite() or value.upper() < 0:
        return None
    lower = value.lower() if value.lower() > 0 else arb(0).lower()
    return hybrid.interval_from_bounds(arb(lower), arb(value.upper()))


def propagate_row(
    audit: Audit,
    *,
    tier: int,
    dps: int,
    segments: int,
    conventions: dict[str, Any],
    rho_record: dict[str, str],
) -> tuple[dict[str, Any], dict[str, arb | None]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    q_switch = exact_rational(conventions["Q_switch"])
    q0 = exact_rational(conventions["Q_0"])
    step = (q0 - q_switch) / segments
    if step >= 0:
        raise AssertionError("Qswitch-to-Q0 transfer must be backward")
    kappa = hybrid.bracket_band(exact_rational(conventions["kappa_corridor"]["left_exact"]), exact_rational(conventions["kappa_corridor"]["right_exact"]))
    lam = hybrid.bracket_band(exact_rational(conventions["lambda_slab"]["left_exact"]), exact_rational(conventions["lambda_slab"]["right_exact"]))
    rho_switch = interval_from_record(rho_record)
    x_switch = 6 * arb.pi() ** 2 * arb(q_switch).exp()
    u_state = (arb(1), -(x_switch + arb(1) / 2 + rho_switch))
    j_state = arb(0)
    step_abs = arb(-step)
    max_u_remainder = arb(0)
    max_j_remainder = arb(0)
    steps_ok = True
    for index in range(segments):
        q_base = q_switch + index * step
        _, coefficient_values = hybrid.coefficient_derivatives(q_base, kappa, lam, order)
        derivatives: list[tuple[arb, arb]] = [u_state]
        for n in range(order):
            next_u = arb(0)
            next_uq = arb(0)
            for derivative in range(n + 1):
                applied = apply_coefficient_derivative(derivative, coefficient_values, derivatives[n - derivative])
                factor = math.comb(n, derivative)
                next_u += factor * applied[0]
                next_uq += factor * applied[1]
            derivatives.append((next_u, next_uq))
        j_derivatives = [j_state]
        for n in range(order):
            j_derivatives.append(-sum((math.comb(n, derivative) * derivatives[derivative][0] * derivatives[n - derivative][0] for derivative in range(n + 1)), arb(0)))
        u_polynomial = [arb(0), arb(0)]
        j_polynomial = arb(0)
        for n in range(order + 1):
            factor = arb(step) ** n / math.factorial(n)
            u_polynomial[0] += factor * derivatives[n][0]
            u_polynomial[1] += factor * derivatives[n][1]
            j_polynomial += factor * j_derivatives[n]
        majorants = hybrid.whole_step_majorants(q_base, kappa, lam, order)
        state_norm = maximum(absolute_upper(u_state[0]), absolute_upper(u_state[1]))
        tube_norm = arb((state_norm * (majorants[0] * step_abs).exp()).upper())
        derivative_bounds = [tube_norm]
        for n in range(order + 1):
            bound = sum((math.comb(n, derivative) * majorants[derivative] * derivative_bounds[n - derivative] for derivative in range(n + 1)), arb(0))
            derivative_bounds.append(arb(bound.upper()))
        u_remainder = arb((derivative_bounds[order + 1] * step_abs ** (order + 1) / math.factorial(order + 1)).upper())
        j_d13_bound = sum((math.comb(order, derivative) * derivative_bounds[derivative] * derivative_bounds[order - derivative] for derivative in range(order + 1)), arb(0))
        j_remainder = arb((j_d13_bound * step_abs ** (order + 1) / math.factorial(order + 1)).upper())
        u_state = (u_polynomial[0] + symmetric(u_remainder), u_polynomial[1] + symmetric(u_remainder))
        j_state = j_polynomial + symmetric(j_remainder)
        if u_remainder.upper() > max_u_remainder.upper():
            max_u_remainder = arb(u_remainder.upper())
        if j_remainder.upper() > max_j_remainder.upper():
            max_j_remainder = arb(j_remainder.upper())
        steps_ok = bool(steps_ok and u_remainder.is_finite() and j_remainder.is_finite() and all(value.is_finite() for value in (*u_state, j_state)))
    j_nonnegative = nonnegative_part(j_state)
    row_ok = bool(steps_ok and excludes_zero(u_state[0]) and u_state[0].lower() > 0 and j_nonnegative is not None)
    audit.control(
        f"rawc.kappa_q0_twosided.tier{tier}.segments{segments}.transfer",
        row_ok,
        "The order-12 U,U_Q,J interval-Taylor transfer has full-step D13 bounds, a positive Q0 endpoint chart and a nonnegative J enclosure.",
        decimal_digits=dps,
        segments=segments,
        rho_Qswitch=interval_record(rho_switch, digits),
        max_U_remainder_upper=max_u_remainder.upper().str(digits, radius=False),
        max_J_remainder_upper=max_j_remainder.upper().str(digits, radius=False),
        U_Q0=interval_record(u_state[0], digits),
        U_Q_Q0=interval_record(u_state[1], digits),
        J_Q0=interval_record(j_nonnegative, digits) if j_nonnegative is not None else None,
    )
    return {
        "tier": tier,
        "decimal_digits": dps,
        "segments": segments,
        "U_Q0": interval_record(u_state[0], digits),
        "U_Q_Q0": interval_record(u_state[1], digits),
        "J_Q0": interval_record(j_nonnegative, digits) if j_nonnegative is not None else None,
        "max_U_remainder_upper": max_u_remainder.upper().str(digits, radius=False),
        "max_J_remainder_upper": max_j_remainder.upper().str(digits, radius=False),
        "status": "CERTIFIED_FINITE_U_J_TRANSFER_ROW" if row_ok else "U_J_TRANSFER_ROW_NOT_CERTIFIED",
    }, {"u": u_state[0], "uq": u_state[1], "j": j_nonnegative}


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    cfg = json.loads(raw_input)
    if cfg.get("schema_version") != "ice.raw-c-qswitch-to-q0-kappa-projective-sensitivity-two-sided-enclosure.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None or cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("identity, resource or fail-closed policy drift")
    conventions = cfg["declared_conventions"]
    if conventions.get("Q_switch") != "-29/10" or conventions.get("Q_0") != "-4" or conventions.get("compact_taylor_order") != 12 or conventions.get("compact_q_segment_ladder") != [16, 32] or conventions.get("precision_ladder_decimal_digits") != [80, 120]:
        raise AssertionError("endpoint or transfer convention drift")
    method = cfg["method_reuse"]
    method_path = root / method["path"]
    if sha256_bytes(method_path.read_bytes()) != method["sha256"] or method_path.resolve() != Path(hybrid.__file__).resolve():
        raise AssertionError("interval-Taylor helper path or hash drift")
    upstream_payloads: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream_payloads.append(payload)
        upstream_records.append(record)
    if len(upstream_payloads) != 3:
        raise AssertionError("requires Qswitch two-sided, sign-strip chart and Q0 sign results")
    qswitch, signstrip, q0_sign = upstream_payloads
    audit = Audit()
    exact_audit(audit)
    kappa_left = exact_rational(conventions["kappa_corridor"]["left_exact"])
    kappa_right = exact_rational(conventions["kappa_corridor"]["right_exact"])
    lambda_left = exact_rational(conventions["lambda_slab"]["left_exact"])
    lambda_right = exact_rational(conventions["lambda_slab"]["right_exact"])
    audit.check("rawc.kappa_q0_twosided.declared_strip", bool(0 < kappa_left < kappa_right < 8 and lambda_left < 0 < lambda_right), "The exact current K times Lambda strip is ordered and has positive kappa.")
    qswitch_required_exact = ["rawc.kappa_qswitch.riccati_kappa_sensitivity", "rawc.kappa_qswitch.upstream_anchor_dependencies", "rawc.kappa_qswitch.upstream_selected_family"]
    qswitch_required_controls = ["rawc.kappa_qswitch.pinned_rho_barrier", "rawc.kappa_qswitch.tier2.lower_sum_refinement", "rawc.kappa_qswitch.cross_precision_intersection"]
    qswitch_required_guards = ["rawc.kappa_qswitch.guard.variation_of_constants", "rawc.kappa_qswitch.guard.panel_and_floor_bounds", "rawc.kappa_qswitch.guard.scope"]
    qswitch_ok = bool(
        qswitch.get("declared_conventions", {}).get("kappa_corridor") == conventions["kappa_corridor"]
        and qswitch.get("declared_conventions", {}).get("lambda_slab") == conventions["lambda_slab"]
        and all(required_pass(qswitch, "exact_checks", identifier, "passed") for identifier in qswitch_required_exact)
        and all(required_pass(qswitch, "controls", identifier, "passed") for identifier in qswitch_required_controls)
        and all(required_pass(qswitch, "theorem_guards", identifier, "verified") for identifier in qswitch_required_guards)
    )
    audit.check("rawc.kappa_q0_twosided.pinned_two_sided_qswitch_seed", qswitch_ok, "The hash-pinned Qswitch result supplies the same selected family, exact strip and finite two-sided p_switch box with its required checks and guards.")
    sign_required_controls = ["rawc.signstrip.q0.corridor.tier1.segment_refinement_overlap", "rawc.signstrip.q0.corridor.tier2.segment_refinement_overlap", "rawc.signstrip.q0.corridor.segments16.precision_overlap", "rawc.signstrip.q0.corridor.segments32.precision_overlap", "rawc.signstrip.q0.corridor.final_chart"]
    sign_required_guards = ["rawc.signstrip.guard.selected_actual_family", "rawc.signstrip.guard.whole_step_transfer", "rawc.signstrip.guard.projective_normalization"]
    sign_conventions = signstrip.get("declared_conventions", {})
    sign_ok = bool(
        sign_conventions.get("Q_switch") == conventions["Q_switch"]
        and sign_conventions.get("Q_0") == conventions["Q_0"]
        and sign_conventions.get("kappa_corridor") == conventions["kappa_corridor"]
        and sign_conventions.get("lambda_slab") == conventions["lambda_slab"]
        and all(required_pass(signstrip, "controls", identifier, "passed") for identifier in sign_required_controls)
        and all(required_pass(signstrip, "theorem_guards", identifier, "verified") for identifier in sign_required_guards)
    )
    audit.check("rawc.kappa_q0_twosided.pinned_selected_q0_chart", sign_ok, "The hash-pinned sign strip supplies the same switch-normalized selected family, switch rho seed and nonzero full-corridor Q0 chart; its Gamma_1 face signs are unused.")
    q0_required_exact = ["rawc.kappa_q0.wronskian_derivative", "rawc.kappa_q0.projective_wronskian", "rawc.kappa_q0.strict_negative_margin"]
    q0_required_guards = ["rawc.kappa_q0.guard.wronskian_sign_transport", "rawc.kappa_q0.guard.node_scope"]
    q0_conventions = q0_sign.get("declared_conventions", {})
    q0_ok = bool(
        q0_conventions.get("Q_switch") == conventions["Q_switch"]
        and q0_conventions.get("Q_0") == conventions["Q_0"]
        and q0_conventions.get("kappa_corridor") == conventions["kappa_corridor"]
        and q0_conventions.get("lambda_slab") == conventions["lambda_slab"]
        and all(required_pass(q0_sign, "exact_checks", identifier, "passed") for identifier in q0_required_exact)
        and all(required_pass(q0_sign, "theorem_guards", identifier, "verified") for identifier in q0_required_guards)
    )
    audit.check("rawc.kappa_q0_twosided.pinned_one_sided_crosscheck", q0_ok, "The independent hash-pinned Q0 Wronskian result supplies only the prior one-sided strict margin used as a consistency cross-check.")
    ctx.dps = 120
    p_switch = interval_from_record(qswitch["certified_calculation"]["p_Qswitch"])
    switch_rows = signstrip["certified_calculation"]["switch_rows"]
    rho_switch = all_intersection([interval_from_record(row["transfer_seed_intersection"]["corridor"]) for row in switch_rows])
    q0_chart = next(item for item in signstrip["controls"] if item.get("id") == "rawc.signstrip.q0.corridor.final_chart")
    pinned_u_q0 = interval_from_record(q0_chart["v_Q0"])
    seed_ok = bool(rho_switch is not None and p_switch.is_finite() and p_switch.lower() > 0 and pinned_u_q0.lower() > 0)
    audit.check("rawc.kappa_q0_twosided.seed_intervals", seed_ok, "The pinned two-sided p_switch, selected rho_switch and Q0 amplitude records are finite, with p_switch>0 and U(Q0)>0.", p_switch=interval_record(p_switch, int(conventions["ball_output_digits"])), rho_switch=interval_record(rho_switch, int(conventions["ball_output_digits"])) if rho_switch is not None else None, pinned_U_Q0=interval_record(pinned_u_q0, int(conventions["ball_output_digits"])))
    audit.guard("rawc.kappa_q0_twosided.guard.finite_U_J_flow", "Finite regular interval-Taylor IVP and exact quadrature-state augmentation", "U solves the regular selected finite IVP and J_Q=-U^2 is appended without feeding back into U; every exact rational substep has a full-step D13 remainder.", "Only finite switch-normalized U,U_Q,J endpoint boxes are auxiliary outputs; no pointwise Y or open-leg no-node theorem follows.")
    audit.guard("rawc.kappa_q0_twosided.guard.wronskian_endpoint", "Lagrange/Wronskian identity", "The selected family is differentiable in kappa at fixed lambda, p_switch is the pinned two-sided switch seed, kappa>0, J>=0 and U(Q0) is separately certified positive.", "Only a finite two-sided scale-invariant h(Q0) enclosure and normalized endpoint seed -h(Q0) follow.")
    audit.guard("rawc.kappa_q0_twosided.guard.scope", "Computational-workbench claim separation", "The exact current real K times Lambda strip and selected projective family are hash-pinned.", "No differentiated tail, G_kappa, transversality, monotonicity, uniqueness, selector, velocity, spectrum, RAQ, BFV or physics follows.")
    if rho_switch is None:
        raise AssertionError("switch rho precision records do not overlap")
    rho_record = interval_record(rho_switch, int(conventions["ball_output_digits"]))
    row_records: list[dict[str, Any]] = []
    row_balls: list[dict[str, arb | None]] = []
    for tier, dps in enumerate(conventions["precision_ladder_decimal_digits"], start=1):
        for segments in conventions["compact_q_segment_ladder"]:
            record, balls = propagate_row(audit, tier=tier, dps=int(dps), segments=int(segments), conventions=conventions, rho_record=rho_record)
            row_records.append(record)
            row_balls.append(balls)
    for tier in (1, 2):
        selected = [balls for record, balls in zip(row_records, row_balls, strict=True) if record["tier"] == tier]
        overlaps = {key: all_intersection([row[key] for row in selected]) for key in ("u", "uq", "j")}
        audit.control(f"rawc.kappa_q0_twosided.tier{tier}.segment_refinement_overlap", all(value is not None for value in overlaps.values()), "The 16- and 32-segment endpoint enclosures overlap for U,U_Q and J at this precision.")
    for segments in (16, 32):
        selected = [balls for record, balls in zip(row_records, row_balls, strict=True) if record["segments"] == segments]
        overlaps = {key: all_intersection([row[key] for row in selected]) for key in ("u", "uq", "j")}
        audit.control(f"rawc.kappa_q0_twosided.segments{segments}.precision_overlap", all(value is not None for value in overlaps.values()), "The 80- and 120-decimal endpoint enclosures overlap for U,U_Q and J at this partition.")
    final_u = all_intersection([row["u"] for row in row_balls])
    final_uq = all_intersection([row["uq"] for row in row_balls])
    final_j = all_intersection([row["j"] for row in row_balls])
    if final_u is not None:
        final_u = intersection(final_u, pinned_u_q0)
    final_transfer_ok = bool(final_u is not None and final_uq is not None and final_j is not None and final_u.lower() > 0 and final_j.lower() >= 0)
    audit.control("rawc.kappa_q0_twosided.final_transfer_intersection", final_transfer_ok, "All four transfer rows intersect, J is nonnegative, and U(Q0) also intersects the independently pinned positive chart.", U_Q0=interval_record(final_u, int(conventions["ball_output_digits"])) if final_u is not None else None, U_Q_Q0=interval_record(final_uq, int(conventions["ball_output_digits"])) if final_uq is not None else None, J_Q0=interval_record(final_j, int(conventions["ball_output_digits"])) if final_j is not None else None)
    h_q0: arb | None = None
    w_q0: arb | None = None
    normalized_seed: arb | None = None
    endpoint_ok = False
    if final_transfer_ok and final_u is not None and final_j is not None:
        ctx.dps = 120
        kappa = hybrid.bracket_band(kappa_left, kappa_right)
        w_q0 = p_switch + 2 * kappa * final_j
        h_q0 = -w_q0 / (final_u * final_u)
        normalized_seed = -h_q0
        prior_upper = -arb(kappa_left) / 980
        endpoint_ok = bool(w_q0.lower() > 0 and h_q0.is_finite() and h_q0.upper() < prior_upper.lower() < 0 and normalized_seed.lower() > 0)
    audit.control("rawc.kappa_q0_twosided.two_sided_endpoint", endpoint_ok, "The Wronskian-integral formula gives a finite two-sided h(Q0) interval whose upper endpoint is strictly below the prior one-sided -kappa_left/980 margin.", W_Q0=interval_record(w_q0, int(conventions["ball_output_digits"])) if w_q0 is not None else None, h_Q0=interval_record(h_q0, int(conventions["ball_output_digits"])) if h_q0 is not None else None, normalized_Z_kappa_Q_Q0=interval_record(normalized_seed, int(conventions["ball_output_digits"])) if normalized_seed is not None else None, prior_strict_upper="-kappa_left/980")
    if len(audit.exact) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")
    exact_pass = all(item["passed"] for item in audit.exact)
    control_pass = all(item["passed"] for item in audit.controls)
    all_passed = bool(exact_pass and control_pass and all(item["verified"] for item in audit.guards))
    verdict = "CERTIFY_FINITE_TWO_SIDED_Q0_KAPPA_PROJECTIVE_SENSITIVITY_ENCLOSURE_ONLY" if all_passed else "VALID_TWO_SIDED_Q0_KAPPA_PROJECTIVE_SENSITIVITY_NOT_CERTIFIED"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "method_reuse": method,
        "upstream_results": upstream_records,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": cfg["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "certified_calculation": {
            "scope": "selected real fixed-lambda projective kappa sensitivity at Q0 on the exact current K times Lambda strip only",
            "switch_seed": {"p_Qswitch": interval_record(p_switch, int(conventions["ball_output_digits"])), "rho_Qswitch": rho_record},
            "transfer_rows": row_records,
            "final_U_Q0": interval_record(final_u, int(conventions["ball_output_digits"])) if final_u is not None else None,
            "final_U_Q_Q0": interval_record(final_uq, int(conventions["ball_output_digits"])) if final_uq is not None else None,
            "final_J_Q0": interval_record(final_j, int(conventions["ball_output_digits"])) if final_j is not None else None,
            "final_W_Q0": interval_record(w_q0, int(conventions["ball_output_digits"])) if w_q0 is not None else None,
            "two_sided_h_Q0": interval_record(h_q0, int(conventions["ball_output_digits"])) if h_q0 is not None else None,
            "normalized_tail_initial_data": {"Z_kappa_Q0": "0", "Z_kappa_Q_Q0": interval_record(normalized_seed, int(conventions["ball_output_digits"])) if normalized_seed is not None else None},
            "pointwise_Y_or_open_leg_no_node_claim": None,
            "complete_kappa_differentiated_tail_or_G_kappa": None,
        },
        "non_claim": "This is a finite two-sided selected-projective h(Q0) enclosure and normalized endpoint seed only, not an absolute actual-plus derivative, pointwise Y, pole-free open-leg chart, differentiated tail, G_kappa, transversality, monotonicity, uniqueness, selector, velocity, spectrum, RAQ, BFV, likelihood or physics.",
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "theorem_guards": len(audit.guards), "all_executable_checks_passed": all_passed},
        "resource_accounting": {"symbolic_checks": len(audit.exact), "upstream_results": len(upstream_records), "method_sources": 1, "precision_tiers": 2, "segment_ladder_rows": 2, "transfer_rows": 4, "compact_steps": 96, "compact_taylor_order": 12, "kappa_corridors": 1, "lambda_slabs": 1, "ode_calls": 0, "quadrature_calls": 0, "root_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "kernel_panels_evaluated": 0, "ball_bessel_evaluations": 0, "bisection_steps": 0, "adjacent_result_files_written": 1},
        "environment": {"python": platform.python_version(), "python_implementation": platform.python_implementation(), "python_flint": importlib.metadata.version("python-flint"), "sympy": sp.__version__, "platform": platform.platform()},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": verdict, "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "controls_passed": result["check_summary"]["controls_passed"], "controls_total": result["check_summary"]["controls_total"], "theorem_guards": len(audit.guards), "two_sided_h_Q0": result["certified_calculation"]["two_sided_h_Q0"], "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded)}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
