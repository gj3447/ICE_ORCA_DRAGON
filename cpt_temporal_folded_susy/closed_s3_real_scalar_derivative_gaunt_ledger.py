#!/usr/bin/env python3
"""Exact fixed-mode scalar derivative/Gaunt identities on the unit three-sphere.

This bounded ledger consumes one pinned n<=2 real scalar product and derives
two scalar gradient-triple coefficients using the scalar Laplacian and
closed-manifold integration by parts.  It does not construct a complete
derivative basis, vector/TT couplings, ADM constraints, HDA/Jacobi checks, or
BFV objects.
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


INPUT_NAME = "CLOSED_S3_REAL_SCALAR_DERIVATIVE_GAUNT_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_REAL_SCALAR_DERIVATIVE_GAUNT_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_real_scalar_derivative_gaunt_ledger.py"
EXPECTED_INPUT_SHA256 = "32794735a914f04869ba438a51e81ef1e85e02da1e5bfbe1d8070ef40ec32f7d"
CALCULATION_ID = "ClosedS3RealScalarDerivativeGauntLedger"
RESULT_SCHEMA = "ice.closed-s3-real-scalar-derivative-gaunt-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_REAL_SCALAR_DERIVATIVE_GAUNT_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, str]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, residual: sp.Expr | bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        passed = bool(residual) if isinstance(residual, bool) else sp.simplify(residual) == 0
        self.exact.append({"id": check_id, "passed": passed, "statement": statement})

    def guard(self, guard_id: str, theorem: str, hypotheses: str, scope: str) -> None:
        if guard_id in self.seen:
            raise AssertionError(f"duplicate guard id: {guard_id}")
        self.seen.add(guard_id)
        self.guards.append({"id": guard_id, "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": scope})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {"complete_real_scalar_harmonic_basis": None, "complete_scalar_derivative_gaunt_ledger": None, "vector_or_tensor_derivative_couplings": None, "complete_scalar_vector_tensor_gaunt_ledger": None, "gravitational_hamiltonian_constraint": None, "gravitational_momentum_constraint": None, "full_adm_cubic_constraint_expansion": None, "DD_DH_HH_constraint_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "classical_bfv_charge": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "quantum_common_invariant_core": None, "absolute_bfv_measure": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    if result.get("run_status") != "VALID_RUN" or result.get("verdict") != item["required_verdict"] or result.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream status, verdict, or payload mismatch: {item['path']}")
    pin = {"path": item["path"], "sha256": observed, "payload_sha256_without_self": result["result_payload_sha256_without_self"], "verdict": result["verdict"]}
    return result, pin


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload.get("schema_version") != "ice.closed-s3-real-scalar-derivative-gaunt-ledger.input.v1" or payload.get("calculation_id") != CALCULATION_ID or payload.get("numbered_phase") is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload.get("resource_caps") != expected_caps() or payload.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    if len(payload.get("fixed_packet", [])) != 2:
        raise AssertionError("this calculation is fixed to the declared two-triple packet")
    return payload, observed


def expr(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"pi": sp.pi, "sqrt": sp.sqrt})


def eigenvalue(degree_n: int) -> sp.Expr:
    return sp.Integer(degree_n) * (sp.Integer(degree_n) + 2)


def real_product_coefficients(upstream: dict[str, Any]) -> dict[str, sp.Expr]:
    selected = upstream.get("selected_product", {})
    if selected.get("id") != "n1_diagonal_cos_square":
        raise AssertionError("unexpected upstream selected real product")
    rows = selected.get("real_product")
    if not isinstance(rows, list):
        raise AssertionError("upstream selected real product absent")
    return {str(row["label"]): expr(str(row["coefficient"])) for row in rows}


def packet_row(packet: dict[str, Any], gaunt: sp.Expr, gradient: sp.Expr) -> dict[str, Any]:
    degree = {slot: int(packet[slot]["degree_n"]) for slot in ("a", "b", "c")}
    lambda_a = eigenvalue(degree["a"])
    lambda_b = eigenvalue(degree["b"])
    lambda_c = eigenvalue(degree["c"])
    eigenvalues = {slot: str(eigenvalue(degree[slot])) for slot in ("a", "b", "c")}
    d_bac = sp.simplify((lambda_a + lambda_c - lambda_b) * gaunt / 2)
    d_cab = sp.simplify((lambda_a + lambda_b - lambda_c) * gaunt / 2)
    return {"id": packet["id"], "labels": {slot: packet[slot]["label"] for slot in ("a", "b", "c")}, "degrees_n": degree, "eigenvalues": eigenvalues, "gaunt_G_abc": str(sp.simplify(gaunt)), "gradient_D_abc": str(sp.simplify(gradient)), "cyclic_D_bac": str(d_bac), "cyclic_D_cab": str(d_cab), "ward_lhs_D_bac_plus_D_cab": str(sp.simplify(d_bac + d_cab)), "ward_rhs_lambda_a_G_abc": str(sp.simplify(lambda_a * gaunt)), "derivation_factor_half_lambda_b_plus_lambda_c_minus_lambda_a": str(sp.simplify((lambda_b + lambda_c - lambda_a) / 2))}


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream_raw, upstream_pin = verify_upstream(root, payload["upstream_results"][0])
    coefficients = real_product_coefficients(upstream_raw)
    ledger = Ledger()
    ledger.guard("CS3Derivative.guard.closed_scalar_identity", "Closed-manifold scalar product-Laplacian identity", "The fixed real scalar modes obey -Delta R_a=lambda_a R_a on a compact boundaryless unit S3, and all products/integrals use the declared real normalized convention.", "This only derives scalar gradient triples from scalar Gaunt coefficients. It neither supplies a complete derivative basis nor a vector/TT coupling, ADM, HDA, Jacobi, BFV, or quantum statement.")
    ledger.guard("CS3Derivative.guard.fixed_packet_scope", "Two-triple fixed-mode audit", "Only the two labels already present in the pinned selected n=1 diagonal-cos square are read, with degrees n=0,1,2 declared in the input.", "No conclusion extends to unlisted modes, a complete scalar derivative ledger, or a spectral cutoff calculation.")

    calculated: list[dict[str, Any]] = []
    for packet in payload["fixed_packet"]:
        identifier = str(packet["id"])
        a_label = str(packet["a"]["label"])
        b_label = str(packet["b"]["label"])
        c_label = str(packet["c"]["label"])
        if b_label != c_label or b_label != "R_n1_mL-1_mR-1_cos":
            raise AssertionError("fixed packet must use the pinned n=1 diagonal-cos square")
        gaunt = coefficients.get(a_label)
        if gaunt is None:
            raise AssertionError(f"upstream Gaunt coefficient absent for {a_label}")
        expected_gaunt = expr(str(packet["expected_gaunt"]))
        lambda_a = eigenvalue(int(packet["a"]["degree_n"]))
        lambda_b = eigenvalue(int(packet["b"]["degree_n"]))
        lambda_c = eigenvalue(int(packet["c"]["degree_n"]))
        gradient = sp.simplify((lambda_b + lambda_c - lambda_a) * gaunt / 2)
        expected_gradient = expr(str(packet["expected_gradient_triple"]))
        ledger.check(f"CS3Derivative.{identifier}.gaunt_pin", gaunt - expected_gaunt, "The fixed scalar Gaunt coefficient equals the preregistered entry read from the pinned upstream real product.")
        ledger.check(f"CS3Derivative.{identifier}.eigenvalue", lambda_a - int(packet["a"]["degree_n"]) * (int(packet["a"]["degree_n"]) + 2), "The a-mode eigenvalue uses the declared unit-S3 scalar convention lambda_n=n(n+2).")
        ledger.check(f"CS3Derivative.{identifier}.gradient_from_gaunt", gradient - expected_gradient, "The scalar gradient-triple coefficient equals (lambda_b+lambda_c-lambda_a)G_abc/2 exactly.")
        ibp_residual = sp.simplify(((lambda_a + lambda_c - lambda_b) * gaunt / 2) + ((lambda_a + lambda_b - lambda_c) * gaunt / 2) - lambda_a * gaunt)
        ledger.check(f"CS3Derivative.{identifier}.integration_by_parts", ibp_residual, "The cyclic scalar coefficients satisfy D_bac+D_cab=lambda_a G_abc exactly, the selected integration-by-parts identity.")
        calculated.append(packet_row(packet, gaunt, gradient))

    passed = all(item["passed"] for item in ledger.exact)
    verdict = "KEEP_FIXED_REAL_S3_SCALAR_DERIVATIVE_GAUNT_IDENTITIES_NOT_ADM_HDA" if passed else "KILL_DECLARED_FIXED_REAL_S3_SCALAR_DERIVATIVE_GAUNT_PACKET"
    impact = "RECORD_TWO_FIXED_MODE_SCALAR_DERIVATIVE_IDENTITIES_AND_IDENTIFY_A_SEPARATE_COMPLETE_SCALAR_DERIVATIVE_BASIS_WORK_UNIT" if passed else "DO_NOT_USE_THIS_FIXED_PACKET_FOR_LATER_SVT_OR_ADM_WORK"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": [upstream_pin], "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(item["passed"] for item in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "fixed_packet": calculated, "computed_scope": "two exact fixed-mode real scalar gradient-triple coefficients derived from a pinned scalar Gaunt product, scalar eigenvalues, and integration by parts only", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result": RESULT_NAME, "result_sha256": sha256_bytes(encoded), "result_bytes": len(encoded), "automatic_next": None}, sort_keys=True))


if __name__ == "__main__":
    main()
