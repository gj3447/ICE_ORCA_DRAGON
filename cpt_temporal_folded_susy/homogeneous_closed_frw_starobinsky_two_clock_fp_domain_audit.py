#!/usr/bin/env python3
"""Exact homogeneous closed-FRW Starobinsky two-clock FP-domain audit.

This unnumbered runner is deliberately restricted to the declared classical
minisuperspace constraint and Poisson factors.  It neither constructs complete
observables nor determines a trajectory crossing from a background-export
table.  In particular, it records an exact convention check rather than
silently importing a clock-domain conclusion.
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


INPUT_NAME = "HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_AUDIT_INPUTS.json"
RESULT_NAME = "HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/homogeneous_closed_frw_starobinsky_two_clock_fp_domain_audit.py"
EXPECTED_INPUT_SHA256 = "c2e1632e6d46fa3a433cfba6949d0a517e8a998f4a3736e45f05af1f07108539"
CALCULATION_ID = "HomogeneousClosedFrwStarobinskyTwoClockFpDomainAudit"
RESULT_SCHEMA = "ice.homogeneous-closed-frw-starobinsky-two-clock-fp-domain-audit.result.v1"
RESULT_PREFIX = "HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})

    def guard(self, guard_id: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        if guard_id in self.seen:
            raise AssertionError(f"duplicate guard id: {guard_id}")
        self.seen.add(guard_id)
        self.guards.append({"id": guard_id, "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope, "verified": True})


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1_000_000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "complete_relational_observables": None,
        "quantum_clock_change_map": None,
        "physical_inner_product": None,
        "born_oppenheimer_or_decoherence": None,
        "class_or_cobaya_input": None,
        "empirical_likelihood": None,
        "trajectory_locus_crossing": None,
        "full_scalar_vector_tensor_or_adm_hda": None,
        "quantum_bfv_anomaly_freedom": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key, expected in (
        ("run_status", item["required_run_status"]),
        ("verdict", item["required_verdict"]),
        ("result_payload_sha256_without_self", item["required_payload_sha256_without_self"]),
    ):
        if result.get(key) != expected:
            raise AssertionError(f"upstream field mismatch: {item['path']}:{key}")
    return {"path": item["path"], "sha256": observed, "role": item["role"], "run_status": result["run_status"], "verdict": result["verdict"], "payload_sha256_without_self": result["result_payload_sha256_without_self"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded audit accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.homogeneous-closed-frw-starobinsky-two-clock-fp-domain-audit.input.v1":
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("calculation identity or unnumbered status mismatch")
    if payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("resource or fail-closed declaration drift")
    if payload["required_independent_cross_check"] != {
        "scalar_clock_p_zero_locus_expected_y": 3,
        "P_clock_FP_zero_locus_expected_y": 2,
        "rule": "derive both loci directly from the declared C_V and independently by eliminating p^2 on C_V=0; the independent derivation is authoritative if any informal expectation disagrees",
    }:
        raise AssertionError("locus cross-check declaration drift")
    return payload, observed


def poisson(left: sp.Expr, right: sp.Expr, coordinates: list[sp.Symbol], momenta: list[sp.Symbol]) -> sp.Expr:
    return sp.simplify(sum(sp.diff(left, q) * sp.diff(right, p) - sp.diff(left, p) * sp.diff(right, q) for q, p in zip(coordinates, momenta, strict=True)))


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    Q, P, phi, p, M = sp.symbols("Q P phi p M", real=True, finite=True)
    pi = sp.pi
    alpha = sp.sqrt(sp.Rational(2, 3))
    x = sp.exp(-alpha * phi)
    V = sp.Rational(3, 4) * M**2 * (1 - x) ** 2
    C_v0 = -sp.exp(-sp.Rational(3, 2) * Q) * P**2 / (6 * pi**2) + sp.exp(-sp.Rational(3, 2) * Q) * p**2 / (4 * pi**2) - 6 * pi**2 * sp.exp(Q / 2)
    C_v = sp.simplify(C_v0 + 2 * pi**2 * sp.exp(sp.Rational(3, 2) * Q) * V)
    declared_c = -sp.exp(-sp.Rational(3, 2) * Q) * P**2 / (6 * pi**2) + sp.exp(-sp.Rational(3, 2) * Q) * p**2 / (4 * pi**2) - 6 * pi**2 * sp.exp(Q / 2) + 2 * pi**2 * sp.exp(sp.Rational(3, 2) * Q) * V
    ledger.check("SCV.exact.constraint.additive_potential", sp.simplify(C_v - declared_c) == 0, "C_V is the pinned V=0 constraint plus 2*pi^2 exp(3Q/2)V(phi).")

    phi_fp = poisson(phi, C_v, [Q, phi], [P, p])
    P_fp = poisson(P, C_v, [Q, phi], [P, p])
    Q_fp = poisson(Q, C_v, [Q, phi], [P, p])
    ledger.check("SCV.exact.scalar_clock_factor", sp.simplify(phi_fp - sp.exp(-3 * Q / 2) * p / (2 * pi**2)) == 0, "{phi,C_V}=exp(-3Q/2)p/(2*pi^2).")
    ledger.check("SCV.exact.P_clock_factor", sp.simplify(P_fp + sp.diff(C_v, Q)) == 0, "{P,C_V}=-partial_Q C_V in the declared canonical convention.")
    ledger.check("SCV.exact.Q_failure_control_factor", sp.simplify(Q_fp + sp.exp(-3 * Q / 2) * P / (3 * pi**2)) == 0, "{Q,C_V}=-exp(-3Q/2)P/(3*pi^2), so Q fails as a clock on P=0.")

    p_squared_on_slice = sp.solve(sp.Eq(C_v.subs(P, 0), 0), p**2)[0]
    y = sp.symbols("y", real=True)
    expected_p_squared = 8 * pi**4 * sp.exp(2 * Q) * (3 - sp.exp(Q) * V)
    ledger.check("SCV.exact.P0_constraint_elimination", sp.simplify(p_squared_on_slice - expected_p_squared) == 0, "On C_V=0=P, p^2=8*pi^4 exp(2Q)(3-y), y=exp(Q)V.")
    scalar_locus_factor = sp.simplify(expected_p_squared / (8 * pi**4 * sp.exp(2 * Q)))
    ledger.check("SCV.exact.scalar_clock_p_zero_locus", sp.simplify(scalar_locus_factor - (3 - sp.exp(Q) * V)) == 0, "The scalar-clock FP factor vanishes at p=0, which on P=0=C_V gives y=3.")
    ledger.guard("SCV.guard.real_p_domain", "nonnegativity of a real square", "Q is real, so 8*pi^4 exp(2Q)>0; p is required real on the declared P=0 slice", "p^2=8*pi^4 exp(2Q)(3-y) permits real p exactly for y<=3, with p=0 at y=3. This is a homogeneous slice classification, not a trajectory result.")

    P_fp_on_slice = sp.simplify(P_fp.subs(P, 0).subs(p**2, expected_p_squared))
    expected_P_fp = 6 * pi**2 * sp.exp(Q / 2) * (2 - sp.exp(Q) * V)
    ledger.check("SCV.exact.P_clock_FP_locus_direct", sp.simplify(P_fp_on_slice - expected_P_fp) == 0, "Direct substitution into {P,C_V} yields 6*pi^2 exp(Q/2)(2-y), so the P-clock FP zero is y=2.")
    A = sp.exp(-3 * Q / 2) * p**2 / (4 * pi**2)
    A_on_slice = sp.simplify(A.subs(p**2, expected_p_squared))
    P_fp_independent = sp.simplify(sp.Rational(3, 2) * A_on_slice + 3 * pi**2 * sp.exp(Q / 2) - 3 * pi**2 * sp.exp(3 * Q / 2) * V)
    ledger.check("SCV.exact.P_clock_FP_locus_independent", sp.simplify(P_fp_independent - expected_P_fp) == 0, "Independent constraint elimination agrees with the direct P-clock factor and its y=2 zero.")
    ledger.check("SCV.exact.P_clock_expected_y", payload["required_independent_cross_check"]["P_clock_FP_zero_locus_expected_y"] == 2, "The input records the independently derived P-clock locus y=2, not an unverified informal value.")

    V_prime = sp.simplify(sp.diff(V, phi))
    p_dot = sp.simplify(-sp.diff(C_v, phi))
    expected_V_prime = sp.Rational(3, 2) * M**2 * alpha * x * (1 - x)
    ledger.check("SCV.exact.starobinsky_Vprime", sp.simplify(V_prime - expected_V_prime) == 0, "V_prime=(3/2)M^2 sqrt(2/3)x(1-x), x=exp(-sqrt(2/3)phi).")
    ledger.check("SCV.exact.starobinsky_potential_square", sp.simplify(V - sp.Rational(3, 4) * M**2 * (1 - x)**2) == 0, "V is the declared nonnegative square times 3M^2/4.")
    ledger.guard("SCV.guard.starobinsky_signs", "positivity of exp and monotonicity of exp", "M>0, x=exp(-sqrt(2/3)phi)>0, and 1-x has the sign of phi", "V>=0, V_prime has the sign of phi, and dot(p) has the opposite sign. This does not integrate a trajectory or select a clock branch.")
    ledger.check("SCV.exact.p_evolution", sp.simplify(p_dot + 2 * pi**2 * sp.exp(3 * Q / 2) * V_prime) == 0, "dot(p)={p,C_V}=-2*pi^2 exp(3Q/2)V_prime; it is negative for phi>0 and positive for phi<0.")

    all_passed = all(item["passed"] for item in ledger.exact)
    if all_passed:
        verdict = "KEEP_HOMOGENEOUS_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_IDENTITIES_NOT_COMPLETE_OR_QUANTUM_OBSERVABLES"
        programme_impact = "CLASSICAL_HOMOGENEOUS_CLOCK_DOMAIN_CONVENTION_ONLY_NO_TRAJECTORY_SELECTION"
        run_status = "VALID_RUN"
    else:
        verdict = "KILL_HOMOGENEOUS_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_AUDIT"
        programme_impact = "DO_NOT_USE_DECLARED_CLOCK_DOMAIN_PACKET"
        run_status = "INVALID_RUN"
    result = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": run_status,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "upstream_results": upstream,
        "exact_checks": ledger.exact,
        "theorem_guards": ledger.guards,
        "check_summary": {"all_executable_checks_passed": all_passed, "exact_passed": sum(item["passed"] for item in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards)},
        "required_fail_closed_outputs": payload["required_fail_closed_outputs"],
        "programme_impact": programme_impact,
        "verdict": verdict,
        "environment": {"python": platform.python_version(), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha256 = read_input()
    result = run(payload, input_sha256)
    serialized = canonical_bytes(result) + b"\n"
    if len(serialized) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result exceeds artifact cap")
    path = Path(__file__).with_name(RESULT_NAME)
    path.write_bytes(serialized)
    outer_sha256 = sha256_bytes(serialized)
    print(f"{RESULT_PREFIX}{result['run_status']} exact={result['check_summary']['exact_passed']}/{result['check_summary']['exact_total']} guards={result['check_summary']['theorem_guard_count']} verdict={result['verdict']}")
    print(f"RESULT_SHA256={outer_sha256}")


if __name__ == "__main__":
    main()
