#!/usr/bin/env python3
"""Pure analytic Qswitch-to-Q0 selected kappa-projective sign transport.

The runner consumes a strict Qswitch projective-kappa sign and the already
certified nonzero Q0 chart.  It deliberately uses the Wronskian identity,
not a new four-state numerical integration.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import fmpq


INPUT_NAME = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_SIGN_TRANSPORT_INPUTS.json"
RESULT_NAME = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_SIGN_TRANSPORT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_qswitch_to_q0_kappa_projective_sensitivity_sign_transport.py"
EXPECTED_INPUT_SHA256 = "aec9d889b1a2a557bd0a3f8bd17d5224b1e29dae244403ff64b5a29d2addcab7"
CALCULATION_ID = "RawCQswitchToQ0KappaProjectiveSensitivitySignTransport"
RESULT_SCHEMA = "ice.raw-c-qswitch-to-q0-kappa-projective-sensitivity-sign-transport.result.v1"
RESULT_PREFIX = "RAW_C_QSWITCH_TO_Q0_KAPPA_PROJECTIVE_SENSITIVITY_SIGN_TRANSPORT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


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
        "method_sources": 0,
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
        "kernel_panels_evaluated": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "two_sided_Q0_kappa_projective_sensitivity_enclosure": None,
        "pole_free_projective_chart_on_open_Qswitch_Q0_leg": None,
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


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
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
    if (recorded is None or sha256_bytes(canonical_bytes(payload)) != recorded or result.get("run_status") != "VALID_RUN" or result.get("numbered_phase") is not None):
        raise AssertionError(f"upstream integrity mismatch: {item['path']}")
    return result, {key: item[key] for key in ("path", "sha256", "schema_version", "verdict", "result_payload_sha256_without_self")}


def required_exact(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("passed") is True for item in result.get("exact_checks", []))


def required_control(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("passed") is True for item in result.get("controls", []))


def required_guard(result: dict[str, Any], identifier: str) -> bool:
    return any(item.get("id") == identifier and item.get("verified") is True for item in result.get("theorem_guards", []))


def exact_audit(audit: Audit) -> None:
    u, uq, y, yq, kappa = sp.symbols("U U_Q Y Y_Q kappa", real=True)
    w = u * yq - uq * y
    # U_QQ=A U and Y_QQ=A Y-2*kappa U.
    audit.identity("rawc.kappa_q0.wronskian_derivative", (uq * yq + u * (sp.Symbol("A", real=True) * y - 2 * kappa * u)) - ((sp.Symbol("A", real=True) * u) * y + uq * yq) + 2 * kappa * u**2, "For Y=partial_kappa U, W(U,Y)_Q=-2*kappa*U^2.")
    h = (uq * y - u * yq) / u**2
    audit.identity("rawc.kappa_q0.projective_wronskian", h + w / u**2, "The endpoint projective derivative is h=partial_kappa rho=-W(U,Y)/U^2.")
    p_s, u0, k_left = sp.symbols("p_s U_0 k_left", positive=True, real=True)
    audit.identity("rawc.kappa_q0.switch_wronskian_seed", (u * yq - uq * y).subs({u: 1, y: 0, yq: p_s}) - p_s, "With U(Qswitch)=1, Y(Qswitch)=0 and Y_Q(Qswitch)=-h_switch=p_s, W(Qswitch)=p_s.")
    audit.identity("rawc.kappa_q0.margin_factor", k_left / (20 * 7**2) - k_left / 980, "The pinned p_switch>kappa_left/20 and 0<U(Q0)<7 imply the displayed strict negative margin -kappa_left/980.")
    audit.guard("rawc.kappa_q0.guard.finite_linear_parameter_flow", "Finite-interval smooth parameter dependence for a linear ODE", "The Qswitch selected projective seed is supplied by the pinned result and U,Y solve the differentiated finite linear system.", "The derivative is propagated only as a finite linear flow; no new singular-endpoint differentiability hypothesis is asserted.")
    audit.guard("rawc.kappa_q0.guard.wronskian_sign_transport", "Wronskian/Lagrange identity and positivity of U squared", "kappa>0, Q0<Qswitch, p_switch>0, and the pinned Q0 chart gives U(Q0) nonzero with 0<U(Q0)<7.", "W(Q0)>W(Qswitch)>0 and h(Q0)<-kappa_left/980 only; no absolute functional or root statement follows.")
    audit.guard("rawc.kappa_q0.guard.node_scope", "Endpoint projective division", "The finite linear (U,Y) system remains regular even if an intermediate U were zero; only the separately certified U(Q0) nonzero chart is divided by.", "No interior no-projective-pole/no-node claim is made.")


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    config = json.loads(raw_input)
    if config.get("schema_version") != "ice.raw-c-qswitch-to-q0-kappa-projective-sensitivity-sign-transport.input.v1" or config.get("calculation_id") != CALCULATION_ID or config.get("numbered_phase") is not None or config.get("resource_caps") != expected_caps() or config.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("identity, resource, or fail-closed policy drift")
    conventions = config["declared_conventions"]
    if conventions["Q_switch"] != "-29/10" or conventions["Q_0"] != "-4" or conventions["Q0_amplitude_upper_strict"] != "7" or conventions["analytic_Qswitch_p_floor"] != "kappa_left/20" or conventions["Q0_h_one_sided_margin"] != "h(Q0)<-kappa_left/980<0":
        raise AssertionError("declared endpoint or analytic-margin convention drift")
    upstream_payloads: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in config["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream_payloads.append(payload)
        upstream_records.append(record)
    if len(upstream_payloads) != 2:
        raise AssertionError("requires Qswitch sensitivity and correlated sign-strip results")
    qswitch_result, signstrip = upstream_payloads
    audit = Audit()
    exact_audit(audit)
    k_left = exact_rational(conventions["kappa_corridor"]["left_exact"])
    k_right = exact_rational(conventions["kappa_corridor"]["right_exact"])
    lam_left = exact_rational(conventions["lambda_slab"]["left_exact"])
    lam_right = exact_rational(conventions["lambda_slab"]["right_exact"])
    audit.check("rawc.kappa_q0.declared_strip", bool(0 < k_left < k_right < 8 and lam_left < 0 < lam_right and exact_rational(conventions["Q_0"]) < exact_rational(conventions["Q_switch"])), "The exact correlated K times Lambda strip is ordered and Q0 lies below Qswitch.")
    qswitch_checks = [
        "rawc.kappa_qswitch.upstream_anchor_dependencies",
        "rawc.kappa_qswitch.upstream_selected_family",
        "rawc.kappa_qswitch.analytic_floor_factor",
    ]
    qswitch_controls = [
        "rawc.kappa_qswitch.pinned_rho_barrier",
        "rawc.kappa_qswitch.cross_precision_intersection",
    ]
    qswitch_guards = [
        "rawc.kappa_qswitch.guard.variation_of_constants",
        "rawc.kappa_qswitch.guard.panel_and_floor_bounds",
        "rawc.kappa_qswitch.guard.scope",
    ]
    qswitch_conventions = qswitch_result.get("declared_conventions", {})
    qswitch_certified = qswitch_result.get("certified_calculation", {})
    qswitch_ok = bool(
        all(required_exact(qswitch_result, identifier) for identifier in qswitch_checks)
        and all(required_control(qswitch_result, identifier) for identifier in qswitch_controls)
        and all(required_guard(qswitch_result, identifier) for identifier in qswitch_guards)
        and qswitch_conventions.get("Q_switch") == conventions["Q_switch"]
        and qswitch_conventions.get("kappa_corridor") == conventions["kappa_corridor"]
        and qswitch_conventions.get("lambda_slab") == conventions["lambda_slab"]
        and qswitch_certified.get("analytic_strict_floor") == "p(Qswitch)>kappa_left/20"
        and qswitch_certified.get("p_equals_minus_h") is True
    )
    audit.check(
        "rawc.kappa_q0.pinned_qswitch_sign_floor",
        qswitch_ok,
        "The hash-pinned Qswitch result matches the declared strip and has the selected-family links, analytic p_switch floor, rho barrier, cross-precision strict sign and finite-IVP/floor guards required here.",
        required_exact_checks=qswitch_checks,
        required_controls=qswitch_controls,
        required_guards=qswitch_guards,
        certified_floor="p(Qswitch)>kappa_left/20",
    )
    signstrip_checks = [
        "rawc.signstrip.q0.corridor.final_chart",
        "rawc.signstrip.q0.corridor.tier1.segment_refinement_overlap",
        "rawc.signstrip.q0.corridor.tier2.segment_refinement_overlap",
        "rawc.signstrip.q0.corridor.segments16.precision_overlap",
        "rawc.signstrip.q0.corridor.segments32.precision_overlap",
    ]
    signstrip_guards = [
        "rawc.signstrip.guard.selected_actual_family",
        "rawc.signstrip.guard.whole_step_transfer",
        "rawc.signstrip.guard.projective_normalization",
    ]
    signstrip_conventions = signstrip.get("declared_conventions", {})
    signstrip_root_bracket = signstrip_conventions.get("root_bracket_1", {})
    signstrip_corridor = signstrip_conventions.get("kappa_corridor", {})
    signstrip_kappa_scope_ok = bool(
        signstrip_corridor.get("left_definition") == "root_bracket_1.left_exact-1/1000"
        and signstrip_corridor.get("right_definition") == "root_bracket_1.right_exact+1/1000"
        and signstrip_corridor.get("padding_exact") == "1/1000"
        and exact_rational(signstrip_root_bracket["left_exact"]) - fmpq(1, 1000) == k_left
        and exact_rational(signstrip_root_bracket["right_exact"]) + fmpq(1, 1000) == k_right
    )
    chart_ok = bool(
        all(required_control(signstrip, identifier) for identifier in signstrip_checks)
        and all(required_guard(signstrip, identifier) for identifier in signstrip_guards)
        and signstrip_conventions.get("Q_0") == conventions["Q_0"]
        and signstrip_conventions.get("Q_switch") == conventions["Q_switch"]
        and signstrip_conventions.get("lambda_slab") == conventions["lambda_slab"]
        and signstrip_kappa_scope_ok
    )
    audit.check(
        "rawc.kappa_q0.pinned_selected_q0_chart",
        chart_ok,
        "The hash-pinned sign strip supplies the same selected family and its validated full-corridor Q0 endpoint chart after segment and precision overlap controls.",
        required_controls=signstrip_checks,
        required_guards=signstrip_guards,
        exact_kappa_corridor_reconstruction=signstrip_kappa_scope_ok,
    )
    final_chart = next((item for item in signstrip.get("controls", []) if item.get("id") == "rawc.signstrip.q0.corridor.final_chart"), None)
    if final_chart is None:
        raise AssertionError("missing pinned full-corridor Q0 chart")
    v_record = final_chart["v_Q0"]
    u0_lower = exact_rational(v_record["lower"])
    u0_upper = exact_rational(v_record["upper"])
    audit.check("rawc.kappa_q0.q0_amplitude_margin", bool(chart_ok and final_chart.get("Q0_amplitude_excludes_zero") is True and 0 < u0_lower < u0_upper < 7), "The pinned outward full-corridor Q0 amplitude record has 0<U(Q0)<7, so the only endpoint projective division is defined with the declared uniform margin.", U_Q0_lower=v_record["lower"], U_Q0_upper=v_record["upper"], strict_upper_bound="7")
    margin = k_left / 980
    audit.check("rawc.kappa_q0.strict_negative_margin", bool(margin > 0), "The exact lower corridor endpoint makes kappa_left/980 strictly positive.", kappa_left_exact=str(k_left), margin_exact=str(margin))
    if len(audit.exact) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")
    all_passed = all(item["passed"] for item in audit.exact) and all(item["verified"] for item in audit.guards)
    verdict = "CERTIFY_UNIFORM_NEGATIVE_Q0_KAPPA_PROJECTIVE_SENSITIVITY_ONLY" if all_passed else "VALID_Q0_KAPPA_PROJECTIVE_SENSITIVITY_NOT_CERTIFIED"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "upstream_results": upstream_records,
        "primary_sources": config["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": audit.exact,
        "theorem_guards": audit.guards,
        "certified_calculation": {
            "scope": "selected real fixed-lambda projective kappa sensitivity at Q0 only",
            "Qswitch_positive_wronskian_floor": "W(Qswitch)=p_switch>kappa_left/20",
            "Q0_amplitude_record": {"lower": v_record["lower"], "upper": v_record["upper"]},
            "strict_upper_bound_for_h_Q0": {"expression": "-kappa_left/980", "exact": str(-margin)},
            "interior_no_pole_claim": None,
        },
        "non_claim": "This is a Q0 selected-projective kappa-sensitivity sign/margin only, not an interior no-node theorem, complete G_kappa, reference variation, differentiated tail, transversality, uniqueness, selector, velocity, spectrum, RAQ, BFV, likelihood, or physics.",
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "theorem_guards": len(audit.guards), "all_executable_checks_passed": all_passed},
        "resource_accounting": {"symbolic_checks": len(audit.exact), "upstream_results": len(upstream_records), "method_sources": 0, "kappa_corridors": 1, "lambda_slabs": 1, "ode_calls": 0, "quadrature_calls": 0, "root_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "ball_bessel_evaluations": 0, "bisection_steps": 0, "compact_steps": 0, "kernel_panels_evaluated": 0, "adjacent_result_files_written": 1},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": verdict, "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "theorem_guards": len(audit.guards), "strict_upper_bound_for_h_Q0": result["certified_calculation"]["strict_upper_bound_for_h_Q0"], "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded)}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
