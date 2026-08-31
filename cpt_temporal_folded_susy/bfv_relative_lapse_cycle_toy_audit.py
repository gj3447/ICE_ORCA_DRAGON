#!/usr/bin/env python3
"""Exact audit of one declared relative lapse ray in a finite C* toy.

This unnumbered work unit does not choose an initial lapse cycle for gravity.
It checks only a separately declared, damped C* toy ray and its positive-domain
two-slab coordinate/branch compatibility.  It supplies neither a quantum
BV--BFV pushforward nor an absolute measure.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "BFV_RELATIVE_LAPSE_CYCLE_TOY_AUDIT_INPUTS.json"
RESULT_NAME = "BFV_RELATIVE_LAPSE_CYCLE_TOY_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/bfv_relative_lapse_cycle_toy_audit.py"
EXPECTED_INPUT_SHA256 = "83622c4902ea43adbf82be7e0204fbaac7b5300d6e5e1575c0a4bda235d18d17"
CALCULATION_ID = "BfvRelativeLapseCycleToyAudit"
RESULT_PREFIX = "BFV_RELATIVE_LAPSE_CYCLE_TOY_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "numerical_samples": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {"relative_homology_class_of_declared_ray": None, "physical_initial_lapse_relative_cycle": None, "global_relative_homology_basis": None, "picard_lefschetz_thimble_coefficients": None, "quantum_bv_bfv_pushforward": None, "v0_or_gravity_absolute_bfv_measure": None, "continuum_determinant_or_pfaffian_line": None, "gravity_two_slab_gluing_theorem": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "automatic_next": None}


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = digest(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    if result.get("run_status") != "VALID_RUN" or result.get("verdict") != item["required_verdict"] or result.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream status, verdict, or payload mismatch: {item['path']}")
    if result.get("lapse_cycle_status") != "OPEN_UNSELECTED_INPUT_NOT_A_RESULT":
        raise AssertionError("upstream lapse-cycle field is not the pinned open state")
    return {"path": item["path"], "sha256": observed, "payload_sha256_without_self": result["result_payload_sha256_without_self"], "verdict": result["verdict"], "lapse_cycle_status": result["lapse_cycle_status"]}


def load_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded audit accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = digest(raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {input_sha}")
    payload = json.loads(raw)
    if payload.get("schema_version") != "ice.bfv-relative-lapse-cycle-toy-audit.input.v1":
        raise AssertionError("unexpected input schema")
    if payload.get("calculation_id") != CALCULATION_ID or payload.get("numbered_phase") is not None:
        raise AssertionError("calculation identity mutation")
    if payload["declared_toy"]["declared_open_rapid_decay_ray"] != "Gamma_plus: N=r for r in (0,infinity), oriented from 0_plus to +infinity; no relative-homology group or class is asserted":
        raise AssertionError("declared rapid-decay ray mutation")
    if payload.get("resource_caps") != expected_caps() or payload.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    return payload, input_sha


def exact_calculation() -> tuple[list[dict[str, Any]], dict[str, str]]:
    a, b, r, r_1, r_2, T, s = sp.symbols("a b r r_1 r_2 T s", positive=True, real=True)
    endpoint_weight_exponent = a / r + b * r
    inverse_map_r1 = s * T
    inverse_map_r2 = (1 - s) * T
    jacobian = sp.det(sp.Matrix([[sp.diff(inverse_map_r1, T), sp.diff(inverse_map_r1, s)], [sp.diff(inverse_map_r2, T), sp.diff(inverse_map_r2, s)]]))
    forward_T = r_1 + r_2
    forward_s = r_1 / forward_T
    forward_after_inverse = [
        sp.simplify(inverse_map_r1 + inverse_map_r2 - T),
        sp.simplify(inverse_map_r1 / (inverse_map_r1 + inverse_map_r2) - s),
    ]
    inverse_after_forward = [
        sp.simplify(forward_s * forward_T - r_1),
        sp.simplify((1 - forward_s) * forward_T - r_2),
    ]
    branch_residuals = [
        sp.simplify(sp.sqrt(r_1) * sp.sqrt(r_2) - sp.sqrt(r_1 * r_2)),
        sp.simplify(sp.sqrt(r_1) * sp.sqrt(r_2) - forward_T * sp.sqrt(forward_s * (1 - forward_s))),
    ]
    checks = [
        {
            "id": "bfv.lapse.toy.gamma_plus.endpoint_damping",
            "passed": sp.limit(endpoint_weight_exponent, r, 0, dir="+") == sp.oo and sp.limit(endpoint_weight_exponent, r, sp.oo) == sp.oo,
            "statement": "on the declared ray, exp(-(a/r+b*r)) decays at both stated ends for a,b>0",
        },
        {
            "id": "bfv.lapse.toy.two_slab.coordinate_inverse_and_jacobian",
            "passed": all(item == 0 for item in forward_after_inverse + inverse_after_forward) and jacobian == -T,
            "statement": "the forward and inverse coordinate formulas compose algebraically and det(partial(r_1,r_2)/partial(T,s))=-T; positivity is a separate declared-domain guard",
        },
        {
            "id": "bfv.lapse.toy.principal_branch.positive_product",
            "passed": all(item == 0 for item in branch_residuals),
            "statement": "the principal square-root product and its (T,s) coordinate form agree on the positive domain without crossing the cut",
        },
    ]
    orientation = {"declared_ray": "dN=dr from 0_plus to +infinity", "two_slab_product": "dr_1_wedge_dr_2", "coordinate_pullback": "dr_1_wedge_dr_2 = -T*dT_wedge_ds = T*ds_wedge_dT", "absolute_jacobian": "T"}
    return checks, orientation


def declared_guards(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if payload["epistemic_scope"] != "DECLARED_CSTAR_OPEN_RAPID_DECAY_RAY_ONLY_NOT_A_RELATIVE_HOMOLOGY_CLASS_NOT_A_GLOBAL_OR_GRAVITY_LAPSE_CYCLE":
        raise AssertionError("scope firewall mutation")
    return [
        {"id": "bfv.lapse.toy.guard.ray_orientation_is_declared", "verified": True, "verification_mode": "HASH_PINNED_DECLARATION_NOT_A_DERIVED_HOMOLOGY_CLASS", "statement": "Gamma_plus orientation is an input convention for this toy open ray."},
        {"id": "bfv.lapse.toy.guard.positive_two_slab_domain_is_declared", "verified": True, "verification_mode": "HASH_PINNED_DOMAIN_DECLARATION", "statement": "The inequalities r_1,r_2,T>0 and 0<s<1 are declared hypotheses; the executable check verifies the inverse formulas and Jacobian, not the inequalities themselves."},
        {"id": "bfv.lapse.toy.guard.no_relative_homology_or_gravity_transfer", "verified": True, "verification_mode": "HASH_PINNED_SCOPE_FIREWALL", "statement": "No relative-homology group/class, physical lapse cycle, or gravity cycle is selected."},
        {"id": "bfv.lapse.toy.guard.classical_bv_bfv_sources_only", "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "statement": "The cited BV-BFV sources frame classical boundary compatibility only and do not supply this toy ray, a quantum pushforward, or an absolute measure."},
    ]


def main() -> int:
    payload, input_sha = load_input()
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    checks, orientation = exact_calculation()
    guards = declared_guards(payload)
    all_passed = all(check["passed"] for check in checks)
    result: dict[str, Any] = {
        "schema_version": "ice.bfv-relative-lapse-cycle-toy-audit.result.v1",
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN" if all_passed else "FAIL_CLOSED",
        "verdict": "CALIBRATED_DECLARED_OPEN_RAPID_DECAY_LAPSE_TOY_RAY_ONLY" if all_passed else "KILL_DECLARED_OPEN_RAPID_DECAY_LAPSE_TOY_RAY_AUDIT",
        "programme_impact": "RECORD_TOY_RAPID_DECAY_RAY_AND_POSITIVE_DOMAIN_BOOKKEEPING_WITHOUT_SELECTING_A_RELATIVE_HOMOLOGY_CLASS_OR_GRAVITY_CYCLE" if all_passed else "DO_NOT_USE_THE_DECLARED_TOY_RAY_AS_POSITIVE_DOMAIN_BOOKKEEPING",
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {"path": RUNNER_RELPATH, "sha256": digest(Path(__file__).read_bytes())},
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_toy": payload["declared_toy"],
        "assumptions": payload["assumptions"],
        "exact_checks": checks,
        "declared_scope_guards": guards,
        "check_summary": {"derived_exact_passed": sum(check["passed"] for check in checks), "derived_exact_total": len(checks), "declared_scope_guard_count": len(guards), "all_executable_checks_passed": all_passed},
        "orientation_ledger": orientation,
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "numerical_samples": 0, "automatic_descendants": 0},
        "environment": {"python": platform.python_version(), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = digest(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "derived_exact_passed": result["check_summary"]["derived_exact_passed"], "derived_exact_total": result["check_summary"]["derived_exact_total"], "declared_scope_guards": result["check_summary"]["declared_scope_guard_count"], "result": RESULT_NAME, "result_sha256": digest(encoded), "result_bytes": len(encoded), "automatic_next": None}, sort_keys=True))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
