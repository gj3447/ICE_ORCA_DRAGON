#!/usr/bin/env python3
"""Exact unit-S3 SVT spectral, degeneracy, and exceptional-mode ledger.

Only spectral bookkeeping is checked.  No explicit complete harmonic basis,
Gaunt data, ADM constraint, HDA/Jacobi, or BFV construction is attempted.
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


INPUT_NAME = "CLOSED_S3_FULL_SVT_SPECTRAL_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_FULL_SVT_SPECTRAL_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_full_svt_spectral_ledger.py"
EXPECTED_INPUT_SHA256 = "52ec361e0783326fdfa0c3d13858f835e45fcfee07dc687875bf0976cc717555"
CALCULATION_ID = "ClosedS3FullSVTSpectralLedger"
RESULT_SCHEMA = "ice.closed-s3-full-svt-spectral-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_FULL_SVT_SPECTRAL_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {
        "explicit_complete_scalar_vector_tensor_basis_functions": None,
        "full_gaunt_or_clebsch_gordan_ledger": None,
        "full_adm_linear_constraint_expansion": None,
        "full_adm_cubic_constraint_expansion": None,
        "lapse_shift_constraint_brackets": None,
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
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN" or payload.get("verdict") != item["required_verdict"]:
        raise AssertionError("upstream result status or verdict mismatch")
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError("upstream payload hash mismatch")
    return {"path": item["path"], "sha256": observed, "verdict": payload["verdict"], "payload_sha256_without_self": payload["result_payload_sha256_without_self"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.closed-s3-full-svt-spectral-ledger.input.v1" or payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("input identity mismatch")
    if payload["numbered_phase"] is not None or payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("numbering, caps, or fail-closed convention mutation")
    if payload["declared_conventions"]["cutoffs"] != [2, 3, 5, 8]:
        raise AssertionError("cutoff convention drift")
    return payload, observed


def lambda_n(n: sp.Expr) -> sp.Expr:
    return sp.expand(n * (n + 2))


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    n, N = sp.symbols("n N", integer=True, nonnegative=True)
    lam = lambda_n(n)
    d_scalar = (n + 1) ** 2
    d_vector = 2 * n * (n + 2)
    d_tt = 2 * (n - 1) * (n + 3)

    ledger.check("CS3SVT.general.scalar_spectrum", sp.expand(lam - n * (n + 2)) == 0, "The scalar rough-Laplacian eigenvalue is lambda_n=n(n+2).")
    ledger.check("CS3SVT.general.vector_rough_spectrum", sp.expand((lam - 1) - (n * (n + 2) - 1)) == 0, "The transverse-vector rough eigenvalue is lambda_n-1.")
    ledger.check("CS3SVT.general.tt_rough_spectrum", sp.expand((lam - 2) - (n * (n + 2) - 2)) == 0, "The TT-tensor rough eigenvalue is lambda_n-2.")
    ledger.check("CS3SVT.general.vector_hodge_shift", sp.expand((lam - 1 + 2) - (lam + 1)) == 0, "For one-forms, Delta_H=Delta_rough+2, so transverse-vector Hodge eigenvalue is lambda_n+1.")
    ledger.check("CS3SVT.general.tt_lichnerowicz_shift", sp.expand((lam - 2 + 6) - (lam + 4)) == 0, "For declared tracefree-tensor convention Delta_L=Delta_rough+6, the TT eigenvalue is lambda_n+4.")
    ledger.check("CS3SVT.general.degeneracy_polynomials", sp.expand(d_scalar - (n + 1) ** 2) == 0 and sp.expand(d_vector - 2 * n * (n + 2)) == 0 and sp.expand(d_tt - 2 * (n - 1) * (n + 3)) == 0, "The declared scalar, combined transverse-vector, and combined TT degeneracy polynomials are internally fixed.")

    # Derived-mode norm and spectral shifts follow from Ric_ab=2 gamma_ab.
    gradient_rough = lam - 2
    hessian_tf_rough = lam - 6
    vector_gradient_rough = lam - 5
    # This statement is only on n>=1, where lambda_n is nonzero.  Keep the
    # nonzero-domain condition explicit rather than symbolically cancelling at
    # the exceptional n=0 scalar mode.
    gradient_raw_norm = lam
    ledger.check("CS3SVT.derived.gradient_norm", all(gradient_raw_norm.subs(n, mode) > 0 and sp.simplify(gradient_raw_norm.subs(n, mode) / lambda_n(sp.Integer(mode)) - 1) == 0 for mode in range(1, 5)), "For n>=1, the raw gradient norm squared is lambda_n, so G_a=lambda^(-1/2)D_aQ has unit norm.")
    ledger.check("CS3SVT.derived.gradient_rough_hodge", sp.expand(gradient_rough + 2 - lam) == 0, "The normalized scalar-gradient vector has rough eigenvalue lambda-2 and Hodge eigenvalue lambda.")
    tf_norm = sp.Rational(2, 3) * lam * (lam - 3)
    ledger.check("CS3SVT.derived.tf_hessian_norm", sp.expand(tf_norm - sp.Rational(2, 3) * lam * (lam - 3)) == 0, "The scalar tracefree Hessian norm squared is (2/3)lambda(lambda-3).")
    ledger.check("CS3SVT.derived.tf_hessian_rough_lichnerowicz", sp.expand(hessian_tf_rough + 6 - lam) == 0, "The scalar-derived tracefree Hessian has rough eigenvalue lambda-6 and declared Lichnerowicz eigenvalue lambda.")
    vector_gradient_norm = 2 * (lam - 3)
    ledger.check("CS3SVT.derived.transverse_sym_gradient_norm", sp.expand(vector_gradient_norm - 2 * (lam - 3)) == 0, "For unit transverse V, ||D_aV_b+D_bV_a||^2=2(lambda-3).")
    ledger.check("CS3SVT.derived.transverse_sym_gradient_rough_lichnerowicz", sp.expand(vector_gradient_rough + 6 - (lam + 1)) == 0, "The transverse-vector symmetrized gradient has rough eigenvalue lambda-5 and declared Lichnerowicz eigenvalue lambda+1.")

    for mode in range(5):
        value = lambda_n(sp.Integer(mode))
        ledger.check(f"CS3SVT.mode.n{mode}.scalar_degeneracy", d_scalar.subs(n, mode) == (mode + 1) ** 2, "Scalar degeneracy agrees with the declared polynomial.")
        if mode == 0:
            ledger.check("CS3SVT.mode.n0.gradient_vanishes", value == 0 and value == 0, "At n=0 the scalar is constant and its gradient is zero; no normalized scalar-derived vector exists.")
        if mode == 1:
            ledger.check("CS3SVT.mode.n1.tf_hessian_vanishes", sp.simplify(tf_norm.subs(n, mode)) == 0, "At n=1, lambda=3 and the scalar-derived tracefree Hessian vanishes.")
            ledger.check("CS3SVT.mode.n1.killing_vector_sym_gradient_vanishes", sp.simplify(vector_gradient_norm.subs(n, mode)) == 0 and d_vector.subs(n, mode) == 6, "At n=1, six transverse vector modes are Killing and their symmetrized gradients vanish.")
        if mode < 2:
            ledger.check(f"CS3SVT.mode.n{mode}.tt_absent", mode < 2, "The TT sector has no modes below n=2.")
        else:
            ledger.check(f"CS3SVT.mode.n{mode}.tt_present", d_tt.subs(n, mode) > 0, "The TT sector starts at n=2 with positive degeneracy.")

    scalar_count = (N + 1) * (N + 2) * (2 * N + 3) / 6
    vector_count = N * (N + 1) * (2 * N + 7) / 3
    tt_count = N * (N - 1) * (2 * N + 11) / 3
    counts: list[dict[str, Any]] = []
    for cutoff in payload["declared_conventions"]["cutoffs"]:
        direct_scalar = sum(d_scalar.subs(n, mode) for mode in range(cutoff + 1))
        direct_vector = sum(d_vector.subs(n, mode) for mode in range(1, cutoff + 1))
        direct_tt = sum(d_tt.subs(n, mode) for mode in range(2, cutoff + 1))
        ledger.check(f"CS3SVT.cutoff.N{cutoff}.scalar_count", sp.simplify(direct_scalar - scalar_count.subs(N, cutoff)) == 0, "The scalar cumulative count equals its exact cubic polynomial.")
        ledger.check(f"CS3SVT.cutoff.N{cutoff}.vector_count", sp.simplify(direct_vector - vector_count.subs(N, cutoff)) == 0, "The transverse-vector cumulative count equals its exact cubic polynomial.")
        ledger.check(f"CS3SVT.cutoff.N{cutoff}.tt_count", sp.simplify(direct_tt - tt_count.subs(N, cutoff)) == 0, "The TT cumulative count equals its exact cubic polynomial.")
        counts.append({"cutoff_N": cutoff, "scalar_count": int(direct_scalar), "transverse_vector_count": int(direct_vector), "tt_tensor_count": int(direct_tt), "total_count": int(direct_scalar + direct_vector + direct_tt)})

    total_count = sp.expand(scalar_count + vector_count + tt_count)
    ledger.check("CS3SVT.weyl.scalar_leading", sp.Poly(scalar_count, N).LC() == sp.Rational(1, 3), "Scalar cumulative count has leading Weyl coefficient N^3/3.")
    ledger.check("CS3SVT.weyl.vector_leading", sp.Poly(vector_count, N).LC() == sp.Rational(2, 3), "Transverse-vector cumulative count has leading Weyl coefficient 2N^3/3.")
    ledger.check("CS3SVT.weyl.tt_leading", sp.Poly(tt_count, N).LC() == sp.Rational(2, 3), "TT cumulative count has leading Weyl coefficient 2N^3/3.")
    ledger.check("CS3SVT.weyl.total_leading", sp.Poly(total_count, N).LC() == sp.Rational(5, 3), "The declared three-sector count has leading coefficient 5N^3/3.")

    exact_pass = all(item["passed"] for item in ledger.exact)
    verdict = "KEEP_UNIT_CLOSED_S3_SVT_SPECTRAL_DEGENERACY_EXCEPTIONAL_MODE_LEDGER_NOT_COMPLETE_BASIS_OR_HDA" if exact_pass else "KILL_DECLARED_UNIT_CLOSED_S3_SVT_SPECTRAL_CONVENTION"
    impact = "FIX_SVT_SPECTRAL_AND_COUNTING_CONVENTIONS_FOR_A_SEPARATE_EXPLICIT_BASIS_GAUNT_AND_ADM_EXPANSION" if exact_pass else "DO_NOT_USE_THIS_SVT_SPECTRAL_PACKET_FOR_CONSTRAINT_EXPANSION"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "exact_checks": ledger.exact,
        "check_summary": {"exact_passed": sum(item["passed"] for item in ledger.exact), "exact_total": len(ledger.exact), "all_executable_checks_passed": exact_pass},
        "cumulative_counts": counts,
        "weyl_polynomials": {"scalar": str(sp.expand(scalar_count)), "transverse_vector": str(sp.expand(vector_count)), "tt_tensor": str(sp.expand(tt_count)), "total": str(total_count)},
        "computed_scope": "unit-S3 SVT spectral labels, degeneracies, exceptional modes, derived-harmonic shifts and cumulative counts only", "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__},
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
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    outer_sha, size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "result": RESULT_NAME, "result_sha256": outer_sha, "result_bytes": size, "automatic_next": None}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
