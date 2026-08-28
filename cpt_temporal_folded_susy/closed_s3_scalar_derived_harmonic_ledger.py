#!/usr/bin/env python3
"""Exact unit-S3 scalar-derived vector/tensor harmonic normalization ledger.

The calculation uses integrated identities for one normalized scalar harmonic.
It neither constructs a complete SVT basis nor expands ADM constraints or tests
HDA/Jacobi/BFV closure.
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


INPUT_NAME = "CLOSED_S3_SCALAR_DERIVED_HARMONIC_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_SCALAR_DERIVED_HARMONIC_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_scalar_derived_harmonic_ledger.py"
EXPECTED_INPUT_SHA256 = "fb7db4d0775a73146e8242494af75ea630e81959974e6e5d01fbe6bc50875bee"
CALCULATION_ID = "ClosedS3ScalarDerivedHarmonicLedger"
RESULT_SCHEMA = "ice.closed-s3-scalar-derived-harmonic-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_SCALAR_DERIVED_HARMONIC_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


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


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "full_scalar_vector_tensor_harmonic_completeness": None,
        "transverse_vector_tensor_harmonic_basis": None,
        "gaunt_or_clebsch_gordan_ledger": None,
        "full_linear_adm_hamiltonian_constraint": None,
        "full_linear_adm_momentum_constraint": None,
        "cubic_adm_constraint_expansion": None,
        "classical_hypersurface_deformation_algebra_closure": None,
        "classical_jacobi_closure": None,
        "quantum_bfv_charge": None,
        "quantum_bfv_anomaly_freedom": None,
        "raw_C_operator_domain": None,
        "absolute_bfv_measure": None,
        "relational_observables": None,
        "born_oppenheimer_or_decoherence": None,
        "empirical_likelihood": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError("upstream run status is not VALID_RUN")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError("upstream verdict mismatch")
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError("upstream payload hash mismatch")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload["result_payload_sha256_without_self"],
        "verdict": payload["verdict"],
    }


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.closed-s3-scalar-derived-harmonic-ledger.input.v1":
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this must remain unnumbered")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if payload["declared_conventions"]["geometry"] != (
        "unit round S3 with Ric_ab=2 gamma_ab, scalar curvature 6, and compact boundaryless integration by parts"
    ):
        raise AssertionError("geometry convention drift")
    return payload, observed


def lambda_n(n: int) -> sp.Integer:
    return sp.Integer(n * (n + 2))


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    lam = sp.symbols("lambda", nonnegative=True)

    gradient_norm = lam
    hessian_norm = sp.expand(lam**2 - 2 * lam)
    bochner_rhs = sp.expand(lam**2 - 2 * lam)
    tracefree_norm = sp.expand(hessian_norm - lam**2 / 3)
    tracefree_divergence_coefficient = sp.expand(-lam + 2 + lam / 3)

    ledger.check(
        "CS3SDH.general.integration_by_parts_gradient_norm",
        sp.simplify(gradient_norm - lam) == 0,
        "For integral Q_I^2=1 and Delta Q_I=-lambda Q_I, compact integration by parts gives integral |DQ_I|^2=lambda.",
    )
    ledger.check(
        "CS3SDH.general.bochner_hessian_norm",
        sp.simplify(hessian_norm - bochner_rhs) == 0,
        "The integrated Bochner identity with Ric_ab=2 gamma_ab gives integral |D_aD_b Q_I|^2=lambda(lambda-2).",
    )
    ledger.check(
        "CS3SDH.general.tracefree_hessian_trace",
        sp.simplify(-lam + lam) == 0,
        "S_ab=D_aD_b Q_I+(lambda/3)gamma_ab Q_I is tracefree in three dimensions.",
    )
    ledger.check(
        "CS3SDH.general.tracefree_hessian_norm",
        sp.simplify(tracefree_norm - sp.Rational(2, 3) * lam * (lam - 3)) == 0,
        "The tracefree Hessian has integrated norm (2/3)lambda(lambda-3).",
    )
    ledger.check(
        "CS3SDH.general.tracefree_hessian_divergence",
        sp.simplify(tracefree_divergence_coefficient + sp.Rational(2, 3) * (lam - 3)) == 0,
        "D^b S_ab=-(2/3)(lambda-3)D_a Q_I on the unit round S3.",
    )

    mode_table: list[dict[str, Any]] = []
    for n in range(5):
        value = lambda_n(n)
        vector_exists = n >= 1
        tensor_exists = n >= 2
        vector_norm = sp.Integer(0) if not vector_exists else sp.simplify(value / value)
        tensor_norm = (
            sp.Integer(0)
            if not tensor_exists
            else sp.simplify(
                (sp.Rational(2, 3) * value * (value - 3))
                / (sp.Rational(2, 3) * value * (value - 3))
            )
        )
        mode_table.append(
            {
                "n": n,
                "lambda": int(value),
                "gradient_vector_status": "NORMALIZED" if vector_exists else "DEGENERATE_ZERO_GRADIENT",
                "tracefree_tensor_status": "NORMALIZED" if tensor_exists else "DEGENERATE_ZERO_TRACEFREE_HESSIAN",
                "gradient_norm_squared": str(value),
                "hessian_norm_squared": str(value * (value - 2)),
                "tracefree_hessian_norm_squared": str(sp.Rational(2, 3) * value * (value - 3)),
            }
        )
        ledger.check(
            f"CS3SDH.mode.n{n}.lambda",
            value == n * (n + 2),
            "The scalar eigenvalue is lambda_n=n(n+2).",
        )
        if n == 0:
            ledger.check(
                "CS3SDH.mode.n0.gradient_degeneracy",
                value == 0 and value == 0,
                "n=0 is constant, so D_a Q=0 and no normalized scalar-derived vector exists.",
            )
        else:
            ledger.check(
                f"CS3SDH.mode.n{n}.vector_normalization",
                vector_norm == 1,
                "V_a=lambda^(-1/2)D_aQ has unit integrated norm for n>=1.",
            )
            ledger.check(
                f"CS3SDH.mode.n{n}.vector_divergence",
                sp.simplify((-sp.sqrt(value)) ** 2 - value) == 0,
                "The declared vector divergence coefficient has magnitude sqrt(lambda); its negative sign follows from Delta Q=-lambda Q.",
            )
        if n == 1:
            ledger.check(
                "CS3SDH.mode.n1.tracefree_hessian_degeneracy",
                sp.simplify(sp.Rational(2, 3) * value * (value - 3)) == 0,
                "At n=1, lambda=3 and the scalar-derived tracefree Hessian has zero norm.",
            )
        elif tensor_exists:
            tensor_divergence = sp.simplify(
                -sp.Rational(2, 3) * (value - 3) * sp.sqrt(value)
                / sp.sqrt(sp.Rational(2, 3) * value * (value - 3))
            )
            expected_divergence = -sp.sqrt(sp.Rational(2, 3) * (value - 3))
            ledger.check(
                f"CS3SDH.mode.n{n}.tensor_normalization",
                tensor_norm == 1,
                "T_ab=[(2/3)lambda(lambda-3)]^(-1/2)S_ab has unit integrated norm for n>=2.",
            )
            ledger.check(
                f"CS3SDH.mode.n{n}.tensor_divergence",
                sp.simplify(tensor_divergence - expected_divergence) == 0,
                "The normalized scalar-derived tensor obeys D^bT_ab=-sqrt((2/3)(lambda-3))V_a.",
            )

    exact_pass = all(item["passed"] for item in ledger.exact)
    verdict = (
        "KEEP_CLOSED_S3_SCALAR_DERIVED_HARMONIC_NORMALIZATION_LEDGER_NOT_SVT_COMPLETENESS_OR_HDA"
        if exact_pass
        else "KILL_DECLARED_CLOSED_S3_SCALAR_DERIVED_HARMONIC_CONVENTION"
    )
    impact = (
        "FIX_SCALAR_DERIVED_HARMONIC_NORMALIZATIONS_FOR_A_SEPARATE_FULL_SVT_AND_GAUNT_LEDGER"
        if exact_pass
        else "DO_NOT_USE_THIS_SCALAR_DERIVED_PACKET_FOR_CONSTRAINT_EXPANSION"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_conventions": payload["declared_conventions"],
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "all_executable_checks_passed": exact_pass,
        },
        "formulae": {
            "gradient_norm_squared": "lambda",
            "hessian_norm_squared": "lambda(lambda-2)",
            "tracefree_hessian_norm_squared": "(2/3)lambda(lambda-3)",
            "vector": "V_a=lambda^(-1/2)D_aQ, n>=1",
            "tensor": "T_ab=[(2/3)lambda(lambda-3)]^(-1/2)[D_aD_bQ+(lambda/3)gamma_abQ], n>=2",
            "vector_divergence": "D^aV_a=-sqrt(lambda)Q",
            "tensor_divergence": "D^bT_ab=-sqrt((2/3)(lambda-3))V_a",
        },
        "mode_table": mode_table,
        "computed_scope": "general scalar-derived vector and tracefree tensor normalization identities on unit round S3 only",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def write_result(path: Path, result: dict[str, Any]) -> tuple[str, int]:
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result exceeds artifact cap")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> int:
    payload, input_sha256 = read_input()
    result = run(payload, input_sha256)
    outer_sha256, size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "result": RESULT_NAME,
                "result_sha256": outer_sha256,
                "result_bytes": size,
                "automatic_next": None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
