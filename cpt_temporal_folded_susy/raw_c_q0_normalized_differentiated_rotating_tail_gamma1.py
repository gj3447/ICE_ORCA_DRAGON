#!/usr/bin/env python3
"""Complete cutoff-plus-tail enclosure of a Q0-normalized Gamma_1 functional.

This is a bounded six-state interval-Taylor calculation.  It forms the
declared boundary Wronskians at a finite left cutoff and adds analytic
rotating-frame radii for both the Gamma_1 tail and its local lambda derivative.
It never constructs an absolute actual Gamma_1 amplitude or a root.
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


INPUT_NAME = "RAW_C_Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_GAMMA1_INPUTS.json"
RESULT_NAME = "RAW_C_Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_GAMMA1_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_q0_normalized_differentiated_rotating_tail_gamma1.py"
EXPECTED_INPUT_SHA256 = "183a7c4fd1e2f5823338203ef9143212c572f5ca3a74f2e7450713e4a0b5dbdd"
CALCULATION_ID = "RawCQ0NormalizedDifferentiatedRotatingTailGamma1"
RESULT_SCHEMA = "ice.raw-c-q0-normalized-differentiated-rotating-tail-gamma1.result.v1"
RESULT_PREFIX = "RAW_C_Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_GAMMA1_RESULT="
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
    return hybrid.interval_from_bounds(
        arb(exact_rational(value["lower"])),
        arb(exact_rational(value["upper"])),
    )


def symmetric(radius: arb) -> arb:
    return hybrid.symmetric_interval(radius)


def intersect(left: arb, right: arb) -> arb | None:
    return hybrid.intersection(left, right)


def interval_width(value: arb) -> arb:
    return hybrid.interval_width(value)


def excludes_zero(value: arb) -> bool:
    return hybrid.excludes_zero(value)


def absolute_upper(value: arb) -> arb:
    return hybrid.absolute_upper(value)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144,
        "changed_artifact_files": 12, "changed_artifact_bytes": 1000000,
        "symbolic_operations": 768, "compact_steps": 480,
        "compact_taylor_order": 12, "cutoff_segment_rows": 18,
        "precision_tiers": 2, "root_brackets": 1, "nonzero_lambda_boxes": 2,
        "ball_bessel_evaluations": 0, "ode_calls": 0, "root_calls": 0,
        "quadrature_calls": 0, "finite_difference_calls": 0, "sampling_points": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "actual_nonzero_lambda_declared_Gamma1_value": None,
        "actual_declared_Gamma1_sign_separation": None,
        "nonzero_lambda_root_continuation": None, "root_velocity": None,
        "nonreal_weyl_m_function": None, "raw_C_spectral_measure": None,
        "raw_C_RAQ_completion": None, "physical_or_empirical_claim": None,
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
        value = sp.simplify(residual)
        self.exact.append({"id": identifier, "passed": bool(value == 0), "statement": statement, "residual": str(value)})

    def inequality(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.exact.append({"id": identifier, "passed": bool(passed), "statement": statement, **data})

    def control(self, identifier: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(identifier)
        self.controls.append({"id": identifier, "passed": bool(passed), "statement": statement, **data})

    def guard(self, identifier: str, theorem: str, hypotheses: str, scope: str) -> None:
        self.register(identifier)
        self.guards.append({"id": identifier, "verified": True, "theorem": theorem, "hypotheses": hypotheses, "scope": scope})


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload self-hash mismatch: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    return payload, {"path": item["path"], "sha256": observed, "payload_sha256_without_self": item["payload_sha256_without_self"], "role": item["role"]}


def exact_audit(audit: Audit) -> None:
    q = sp.symbols("Q", real=True)
    u, uq, z, zq, c, cq, a, lam = sp.symbols("u uq z zq c cq a lambda", real=True)
    A0 = sp.symbols("A0", real=True)
    wu = u * cq - uq * c
    wz = z * cq - zq * c
    audit.identity("rawc.q0tail.wronskian_identity", sp.diff(wu, u) * uq + sp.diff(wu, uq) * (A0 + lam * a) * u + sp.diff(wu, c) * cq + sp.diff(wu, cq) * A0 * c + lam * a * u * c, "W(U,c)_Q=-lambda*a*U*c for the lambda-independent reference c.")
    audit.identity("rawc.q0tail.differentiated_wronskian_identity", sp.diff(wz, z) * zq + sp.diff(wz, zq) * ((A0 + lam * a) * z + a * u) + sp.diff(wz, c) * cq + sp.diff(wz, cq) * A0 * c + a * u * c + lam * a * z * c, "W(Z,c)_Q=-(a*U*c+lambda*a*Z*c).")
    rho, x0, sensitivity = sp.symbols("rho x0 s", real=True)
    r = -rho - x0 - sp.Rational(1, 2)
    audit.identity("rawc.q0tail.projective_seed", sp.diff(r, rho) * sensitivity + sensitivity, "For r=U_Q(Q0), partial_lambda r=-s(Q0) under U(Q0)=1.")
    audit.identity("rawc.q0tail.a_tail_antiderivative", sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q) - 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), "The forcing-tail mass has the exact antiderivative 4*pi^2*exp(3Q/2).")
    audit.identity("rawc.q0tail.v_tail_antiderivative", sp.diff(18 * sp.pi**4 * sp.exp(2 * q), q) - 36 * sp.pi**4 * sp.exp(2 * q), "The reference-potential tail mass has the exact antiderivative 18*pi^4*exp(2Q).")
    audit.identity("rawc.q0tail.cutoff_partition", 16 * sp.Rational(-1, 16) - (sp.Rational(-5) - sp.Rational(-4)), "The coarse cutoff partition is exact.")
    audit.identity("rawc.q0tail.cutoff_partition_refined", 32 * sp.Rational(-1, 32) - (sp.Rational(-5) - sp.Rational(-4)), "The refined cutoff partition is exact.")
    audit.identity("rawc.q0tail.cutoff_partition_deep", 32 * sp.Rational(-1, 16) - (sp.Rational(-6) - sp.Rational(-4)), "The deeper cutoff partition is exact.")


def matrix_derivative(q_base: fmpq, kappa: arb, lam: arb, derivative: int, order: int) -> list[list[arb]]:
    _, a_values = hybrid.coefficient_derivatives(q_base, kappa, lam, order)
    c_value = 6 * arb.pi() ** 2
    x = c_value * arb(q_base).exp()
    force = x * x.sqrt() / c_value.sqrt()
    a0 = x**2 - kappa**2 if derivative == 0 else arb(2) ** derivative * x**2
    av = a_values[derivative]
    force_d = (arb(3) / 2) ** derivative * force
    zero = arb(0)
    if derivative == 0:
        return [[zero, arb(1), zero, zero, zero, zero], [av, zero, zero, zero, zero, zero], [zero, zero, zero, arb(1), zero, zero], [force, zero, av, zero, zero, zero], [zero, zero, zero, zero, zero, arb(1)], [zero, zero, zero, zero, a0, zero]]
    return [[zero] * 6, [av, zero, zero, zero, zero, zero], [zero] * 6, [force_d, zero, av, zero, zero, zero], [zero] * 6, [zero, zero, zero, zero, a0, zero]]


def matrix_apply(matrix: list[list[arb]], state: list[arb]) -> list[arb]:
    return [sum((matrix[i][j] * state[j] for j in range(6)), arb(0)) for i in range(6)]


def matrix_majorants(q_base: fmpq, kappa: arb, lam: arb, order: int) -> list[arb]:
    inherited = hybrid.whole_step_majorants(q_base, kappa, lam, order)
    c_value = 6 * arb.pi() ** 2
    x = c_value * arb(q_base).exp()
    force = x * x.sqrt() / c_value.sqrt()
    kabs = absolute_upper(kappa)
    result: list[arb] = []
    for derivative in range(order + 1):
        a0 = x**2 + kabs**2 if derivative == 0 else arb(2) ** derivative * x**2
        ad = inherited[derivative]
        force_d = (arb(3) / 2) ** derivative * force
        row = ad + force_d
        if derivative == 0:
            row += arb(1)
        result.append(arb(max(row.upper(), a0.upper())))
    return result


def rotating_norm(u: arb, uq: arb, kappa_lower: arb) -> arb:
    return (absolute_upper(u) ** 2 + (absolute_upper(uq) / kappa_lower) ** 2).sqrt()


def propagate(audit: Audit, *, label: str, tier: int, dps: int, cutoff: dict[str, Any], kappa: arb, lam: arb, rho: arb, sensitivity: arb, conventions: dict[str, Any]) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    q0 = exact_rational(conventions["Q_0"])
    qc = exact_rational(cutoff["Q_cut"])
    segments = int(cutoff["segments"])
    step = (qc - q0) / segments
    if step >= 0:
        raise AssertionError("left-tail step must be negative")
    x0 = 6 * arb.pi() ** 2 * arb(q0).exp()
    state = [arb(1), -x0 - arb(1) / 2 - rho, arb(0), -sensitivity, arb(1), arb(0)]
    audit.control(f"rawc.q0tail.{label}.tier{tier}.{cutoff['label']}.seed", bool(state[1].is_finite() and state[3].is_finite()), "The Q0 projective seed has U=1, Z=0 and Z_Q=-s on the full inherited box.", rho_Q0=interval_record(rho, digits), s_Q0=interval_record(sensitivity, digits), U_Q_Q0=interval_record(state[1], digits), Z_Q_Q0=interval_record(state[3], digits))
    abs_step = arb(-step)
    remainder_max = arb(0)
    for index in range(segments):
        q_base = q0 + index * step
        matrices = [matrix_derivative(q_base, kappa, lam, derivative, order) for derivative in range(order + 1)]
        jets: list[list[arb]] = [state]
        for n in range(order):
            nxt = [arb(0) for _ in range(6)]
            for j in range(n + 1):
                applied = matrix_apply(matrices[j], jets[n - j])
                for component in range(6):
                    nxt[component] += math.comb(n, j) * applied[component]
            jets.append(nxt)
        poly = [arb(0) for _ in range(6)]
        for n, jet in enumerate(jets):
            factor = arb(step) ** n / math.factorial(n)
            for component in range(6):
                poly[component] += factor * jet[component]
        majorants = matrix_majorants(q_base, kappa, lam, order)
        state_norm = max((absolute_upper(value) for value in state), key=lambda value: value.upper())
        tube_norm = arb((state_norm * (majorants[0] * abs_step).exp()).upper())
        bounds = [tube_norm]
        for n in range(order + 1):
            bounds.append(arb(sum((math.comb(n, j) * majorants[j] * bounds[n - j] for j in range(n + 1)), arb(0)).upper()))
        remainder = arb((bounds[order + 1] * abs_step ** (order + 1) / math.factorial(order + 1)).upper())
        state = [item + symmetric(remainder) for item in poly]
        remainder_max = arb(max(remainder_max.upper(), remainder.upper()))
        audit.control(f"rawc.q0tail.{label}.tier{tier}.{cutoff['label']}.step{index + 1}", bool(remainder.is_finite() and remainder.lower() >= 0 and all(value.is_finite() for value in state)), "The six-state order-12 Taylor step has a full-box D13 remainder bound.", q_base=str(q_base), q_next=str(q_base + step), remainder_radius_upper=remainder.upper().str(digits, radius=False))
    u, uq, z, zq, c, cq = state
    wu = u * cq - uq * c
    wz = z * cq - zq * c
    k_lower = arb(kappa.lower())
    lambda_abs = absolute_upper(lam)
    a_mass = 4 * arb.pi() ** 2 * (arb(qc) * arb(3) / 2).exp()
    v_mass = 18 * arb.pi() ** 4 * arb(2 * qc).exp()
    q_u = (v_mass + lambda_abs * a_mass) / k_lower
    q_c = v_mass / k_lower
    ru_inf = rotating_norm(u, uq, k_lower) * q_u.exp()
    rc_inf = rotating_norm(c, cq, k_lower) * q_c.exp()
    rz_inf = (rotating_norm(z, zq, k_lower) + a_mass * ru_inf / k_lower) * q_u.exp()
    b_t = arb((lambda_abs * a_mass * ru_inf * rc_inf).upper())
    b_z = arb((a_mass * (ru_inf + lambda_abs * rz_inf) * rc_inf).upper())
    g = -wu + symmetric(b_t)
    gp = -wz + symmetric(b_z)
    tail_ok = bool(all(value.is_finite() and value.lower() >= 0 for value in (a_mass, v_mass, q_u, q_c, ru_inf, rc_inf, rz_inf, b_t, b_z)) and g.is_finite() and gp.is_finite())
    audit.control(f"rawc.q0tail.{label}.tier{tier}.{cutoff['label']}.complete_tail", tail_ok, "The finite-cutoff Wronskians receive analytic rotating-frame radii for the complete Gamma_1 quotient tail and its differentiated tail.", tail_radius_g=interval_record(b_t, digits), tail_radius_gprime=interval_record(b_z, digits), g=interval_record(g, digits), gprime=interval_record(gp, digits))
    return {"label": label, "decimal_digits": dps, "cutoff": cutoff, "max_step_remainder_upper": remainder_max.upper().str(digits, radius=False), "W_U_c_at_cutoff": interval_record(wu, digits), "W_Z_c_at_cutoff": interval_record(wz, digits), "tail_radius_g": interval_record(b_t, digits), "tail_radius_gprime": interval_record(b_z, digits), "g": interval_record(g, digits), "gprime": interval_record(gp, digits), "g_zero_excluded": excludes_zero(g), "gprime_zero_excluded": excludes_zero(gp), "status": "CERTIFIED_COMPLETE_TAIL_TIER" if tail_ok else "TAIL_TIER_NOT_CERTIFIED"}, {"g": g, "gp": gp, "bt": b_t, "bz": b_z}


def all_intersection(values: list[arb]) -> arb | None:
    value = values[0]
    for candidate in values[1:]:
        value = intersect(value, candidate)
        if value is None:
            return None
    return value


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input = sha256_bytes(raw)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.raw-c-q0-normalized-differentiated-rotating-tail-gamma1.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None or cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("identity, resource or null-output drift")
    reuse = cfg["method_reuse"]
    helper_path = Path(__file__).with_name(Path(reuse["path"]).name)
    if sha256_bytes(helper_path.read_bytes()) != reuse["sha256"]:
        raise AssertionError("reused helper source hash drift")
    if helper_path.resolve() != Path(hybrid.__file__).resolve():
        raise AssertionError("reused helper import path drift")
    conventions = cfg["declared_conventions"]
    if conventions["precision_ladder_decimal_digits"] != [80, 120] or conventions["compact_taylor_order"] != 12 or [(row["Q_cut"], row["segments"]) for row in conventions["cutoff_segment_ladder"]] != [("-5", 16), ("-5", 32), ("-6", 32)]:
        raise AssertionError("ladder drift")
    root = Path(__file__).resolve().parent.parent
    upstream: dict[str, dict[str, Any]] = {}
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream[item["path"]] = payload
        upstream_records.append(record)
    q0_path, boundary_path = [item["path"] for item in cfg["upstream_results"]]
    q0_result = upstream[q0_path]
    boundary = upstream[boundary_path]
    if boundary["declared_conventions"]["boundary_map"] != conventions["boundary_map"] or boundary["declared_conventions"]["reference_equation"] != conventions["reference_equation"]:
        raise AssertionError("declared boundary convention drift")
    audit = Audit()
    exact_audit(audit)
    audit.guard("rawc.q0tail.guard.q0_projective_normalization", "Projective normalization", "The upstream Q0 result excludes zero from v(Q0), so U=u/u(Q0) is defined for its finite projective state.", "The output is Gamma_1/u(Q0), never an absolute actual Gamma_1 value.")
    audit.guard("rawc.q0tail.guard.whole_step_taylor", "Taylor theorem with whole-step D13 majorant", "All six-state coefficient derivatives and induced-infinity matrix majorants cover the full kappa/lambda boxes on each exact rational step.", "This is an analytic interval calculation, not a black-box ODE solve.")
    audit.guard("rawc.q0tail.guard.complete_rotating_tail", "Rotating-frame variation bound", "The a and reference-potential masses are integrated analytically beyond Q_cut, including the Z forcing contribution.", "The tail radii bound magnitude only; they do not imply a Gamma_1 sign, root or spectral statement.")
    bracket = conventions["root_bracket"]
    kappa = hybrid.bracket_band(exact_rational(bracket["left_exact"]), exact_rational(bracket["right_exact"]))
    q0_rows = {row["label"]: row for row in q0_result["certified_calculation"]["final_intersections"]}
    if set(q0_rows) != {"negative", "positive", "lambda_zero"} or not all(row["certified"] for row in q0_rows.values()):
        raise AssertionError("Q0 result topology drift")
    digits = int(conventions["ball_output_digits"])
    boxes = [{"label": "negative", "left": exact_rational("-1/10000"), "right": exact_rational("-1/100000000")}, {"label": "positive", "left": exact_rational("1/100000000"), "right": exact_rational("1/10000")}, {"label": "lambda_zero", "left": fmpq(0), "right": fmpq(0)}]
    records: dict[str, list[dict[str, Any]]] = {item["label"]: [] for item in boxes}
    balls: dict[str, list[dict[str, arb]]] = {item["label"]: [] for item in boxes}
    for tier, dps in enumerate(conventions["precision_ladder_decimal_digits"], start=1):
        for box in boxes:
            row = q0_rows[box["label"]]
            rho = interval_from_record(row["rho_Q0"])
            sensitivity = interval_from_record(row["s_Q0"])
            lam = arb(0) if box["label"] == "lambda_zero" else hybrid.bracket_band(box["left"], box["right"])
            for cutoff in conventions["cutoff_segment_ladder"]:
                record, result_balls = propagate(audit, label=box["label"], tier=tier, dps=int(dps), cutoff=cutoff, kappa=kappa, lam=lam, rho=rho, sensitivity=sensitivity, conventions=conventions)
                records[box["label"]].append(record)
                balls[box["label"]].append(result_balls)
    for label in records:
        for tier_index in range(2):
            offset = 3 * tier_index
            coarse, refined, deeper = balls[label][offset:offset + 3]
            audit.control(f"rawc.q0tail.{label}.tier{tier_index + 1}.minus5_refinement_overlap", all(intersect(coarse[key], refined[key]) is not None for key in ("g", "gp")), "The -5 cutoff 16/32-step completed functional enclosures overlap.")
            g_tail_decreases = (
                deeper["bt"].upper() < coarse["bt"].upper()
                if label != "lambda_zero"
                else deeper["bt"].upper() <= coarse["bt"].upper()
            )
            audit.control(f"rawc.q0tail.{label}.tier{tier_index + 1}.cutoff_overlap_and_tail_decrease", bool(all(intersect(coarse[key], deeper[key]) is not None for key in ("g", "gp")) and g_tail_decreases and deeper["bz"].upper() < coarse["bz"].upper()), "The completed -5 and -6 cutoff enclosures overlap and the analytic tail radii decrease (or stay exactly zero for the lambda-zero g tail) at the earlier cutoff.")
        for ladder_index, cutoff in enumerate(conventions["cutoff_segment_ladder"]):
            low, high = balls[label][ladder_index], balls[label][ladder_index + 3]
            audit.control(f"rawc.q0tail.{label}.{cutoff['label']}.precision_overlap", all(intersect(low[key], high[key]) is not None for key in ("g", "gp")), "The 80/120-digit same-backend completed functional enclosures overlap.")
    declared_rows = boundary["certified_calculation"]["root_bracket_rows"]
    declared_root1 = declared_rows[0]["certified_normalized_declared_derivative"]
    declared_derivative = interval_from_record(declared_root1)
    lambda_zero_gp = all_intersection([item["gp"] for item in balls["lambda_zero"]])
    audit.control("rawc.q0tail.lambda_zero.declared_derivative_containment", bool(lambda_zero_gp is not None and lambda_zero_gp.lower() <= declared_derivative.lower() and lambda_zero_gp.upper() >= declared_derivative.upper()), "The lambda-zero differentiated complete quotient enclosure contains the separately certified declared normalized derivative on any root in bracket 1.", declared_normalized_derivative=interval_record(declared_derivative, digits), tail_gprime_intersection=interval_record(lambda_zero_gp, digits) if lambda_zero_gp else None)
    final_rows: list[dict[str, Any]] = []
    width_target = arb(exact_rational(conventions["local_derivative_width_target"]))
    for label in ("negative", "positive", "lambda_zero"):
        g = all_intersection([item["g"] for item in balls[label]])
        gp = all_intersection([item["gp"] for item in balls[label]])
        final_ok = bool(g is not None and gp is not None and g.is_finite() and gp.is_finite() and interval_width(gp).upper() < width_target.lower())
        audit.control(f"rawc.q0tail.{label}.final_intersection_and_derivative_width", final_ok, "All cutoff, step and precision rows have a common complete functional intersection with local derivative width below 1/4.", g=interval_record(g, digits) if g else None, gprime=interval_record(gp, digits) if gp else None, gprime_width_target="1/4")
        final_rows.append({"label": label, "certified": final_ok, "g_Q0_normalized": interval_record(g, digits) if g else None, "gprime_local": interval_record(gp, digits) if gp else None, "g_zero_excluded": excludes_zero(g) if g else None, "gprime_zero_excluded": excludes_zero(gp) if gp else None, "gprime_width_target": "1/4", "status": "CERTIFIED_COMPLETE_NORMALIZED_FUNCTIONAL" if final_ok else "FUNCTIONAL_NOT_CERTIFIED"})
    exact_pass = all(item["passed"] for item in audit.exact)
    control_pass = all(item["passed"] for item in audit.controls)
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": cfg["calculation_id"], "numbered_phase": None, "run_status": "VALID_RUN", "verdict": "CERTIFY_COMPLETE_Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_FUNCTIONAL" if exact_pass and control_pass else "Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_NOT_CERTIFIED", "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input}, "upstream_results": upstream_records, "method_reuse": cfg["method_reuse"], "primary_sources": cfg["primary_sources"], "declared_conventions": conventions, "assumptions": cfg["assumptions"], "exact_checks": audit.exact, "controls": audit.controls, "theorem_guards": audit.guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "theorem_guards": len(audit.guards), "all_executable_checks_passed": bool(exact_pass and control_pass)}, "certified_calculation": {"scope": "root bracket 1, two punctured real lambda boxes and lambda-zero regression", "outputs": "complete Q0-normalized Gamma_1 quotient functional g and local derivative gprime only", "final_intersections": final_rows, "next_mathematical_gap": "Any future sign/zero or root question requires a separately justified parameter/root localization; this result does not authorize it."}, "non_claim": "No absolute actual Gamma_1 value or sign, root continuation/velocity, Weyl function, spectral measure, RAQ or physical claim.", "required_fail_closed_outputs": cfg["required_fail_closed_outputs"], "resource_accounting": {"compact_steps": 480, "cutoff_segment_rows": 18, "precision_tiers": 2, "ball_bessel_evaluations": 0, "ode_calls": 0, "root_calls": 0, "quadrature_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "adjacent_result_files_written": 1}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "sympy": sp.__version__, "python_flint": importlib.metadata.version("python-flint"), "platform": platform.platform()}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": len(audit.controls), "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded)}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
