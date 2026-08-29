#!/usr/bin/env python3
"""Exact zonal conformal-curvature cubic-vertex ledger on unit S3.

This bounded runner expands only sqrt(q) R[q] for a conformal zonal scalar
ansatz.  It is not an ADM constraint expansion, nor a bracket or HDA test.
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


INPUT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_CUBIC_VERTEX_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_CUBIC_VERTEX_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_conformal_curvature_cubic_vertex_ledger.py"
EXPECTED_INPUT_SHA256 = "48053d5248550d8908f1dceb59860021d31f5c2ebc747b829b518e0c689f68c2"
CALCULATION_ID = "ClosedS3ZonalConformalCurvatureCubicVertexLedger"
RESULT_SCHEMA = "ice.closed-s3-zonal-conformal-curvature-cubic-vertex-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_CUBIC_VERTEX_LEDGER_RESULT="
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

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})

    def guard(self, guard_id: str, theorem: str, hypotheses: str, scope: str) -> None:
        if guard_id in self.seen:
            raise AssertionError(f"duplicate guard id: {guard_id}")
        self.seen.add(guard_id)
        self.guards.append({"id": guard_id, "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": scope})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {"explicit_complete_scalar_vector_tensor_basis_functions": None, "full_gaunt_or_clebsch_gordan_ledger": None, "nonzonal_scalar_mode_couplings": None, "transverse_vector_tensor_mode_couplings": None, "full_adm_linear_constraint_expansion": None, "full_adm_cubic_constraint_expansion": None, "adm_kinetic_momentum_vertex": None, "matter_perturbation_vertex": None, "lapse_shift_elimination": None, "lapse_shift_constraint_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "raw_C_operator_domain": None, "absolute_bfv_measure": None, "relational_observables": None, "born_oppenheimer_or_decoherence": None, "empirical_likelihood": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN" or payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream status or verdict mismatch: {item['path']}")
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed, "payload_sha256_without_self": payload["result_payload_sha256_without_self"], "verdict": payload["verdict"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.closed-s3-zonal-conformal-curvature-cubic-vertex-ledger.input.v1" or payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    if payload["declared_conventions"]["hard_cutoff"] != "P_N retains zonal Q_0 through Q_N after the declared local density coefficient is formed; a density tail is a truncation diagnostic, not an ADM algebra residual":
        raise AssertionError("hard-cutoff convention drift")
    return payload, observed


def product_degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def add(*vectors: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    answer: dict[int, sp.Expr] = {}
    for vector in vectors:
        for degree, coefficient in vector.items():
            answer[degree] = sp.simplify(answer.get(degree, sp.S.Zero) + coefficient)
    return {degree: coefficient for degree, coefficient in answer.items() if coefficient != 0}


def scale(vector: dict[int, sp.Expr], factor: sp.Expr) -> dict[int, sp.Expr]:
    return {degree: sp.simplify(factor * coefficient) for degree, coefficient in vector.items() if factor * coefficient != 0}


def convolve(left: dict[int, sp.Expr], right: dict[int, sp.Expr], normalizer: sp.Expr) -> dict[int, sp.Expr]:
    terms: list[dict[int, sp.Expr]] = []
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            terms.append({degree: sp.simplify(left_coefficient * right_coefficient * normalizer) for degree in product_degrees(left_degree, right_degree)})
    return add(*terms)


def laplacian(vector: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return {degree: sp.simplify(-degree * (degree + 2) * coefficient) for degree, coefficient in vector.items()}


def project(vector: dict[int, sp.Expr], cutoff: int) -> dict[int, sp.Expr]:
    return {degree: coefficient for degree, coefficient in vector.items() if degree <= cutoff}


def subtract(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return add(left, scale(right, -1))


def norm_squared(vector: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(coefficient**2 for coefficient in vector.values()))


def pairing(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(left.get(degree, sp.S.Zero) * right.get(degree, sp.S.Zero) for degree in set(left) | set(right)))


def integral(vector: dict[int, sp.Expr], volume: sp.Expr) -> sp.Expr:
    return sp.simplify(vector.get(0, sp.S.Zero) * sp.sqrt(volume))


def printable(vector: dict[int, sp.Expr]) -> dict[str, str]:
    return {str(degree): str(vector[degree]) for degree in sorted(vector)}


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    ledger.guard("CS3ZCC.guard.conformal_curvature", "d=3 conformal scalar-curvature transformation", "q_ab=a^2 exp(2 omega) gamma_ab with spatially constant a, R[gamma]=6 and Delta=D^aD_a", "The stated local curvature-density identity is imported only for this conformal ansatz; it does not provide an ADM Hamiltonian constraint.")
    ledger.guard("CS3ZCC.guard.closed_integration_by_parts", "Stokes integration by parts on compact boundaryless S3", "psi is a smooth zonal scalar packet on the unit round S3", "Integral psi Delta psi=-Integral |Dpsi|^2 and Integral psi^2 Delta psi=-2 Integral psi|Dpsi|^2; no bracket statement follows.")
    ledger.guard("CS3ZCC.guard.zonal_product_scope", "Chebyshev-U zonal product identity", "Only normalized zonal Q_n and the upstream product convention are used", "This is not a complete scalar basis or a full Gaunt/Clebsch-Gordan ledger.")
    pi = sp.pi
    volume = 2 * pi**2
    normalizer = 1 / sp.sqrt(volume)
    constant_one = {0: sp.sqrt(volume)}
    ledger.check("CS3ZCC.normalization.constant_one", convolve(constant_one, {2: sp.S.One}, normalizer) == {2: sp.S.One} and integral(constant_one, volume) == volume, "In the orthonormal zonal basis, the constant function is sqrt(2*pi^2)Q_0 and acts as the convolution identity.")

    for n in range(5):
        qn = {n: sp.S.One}
        ledger.check(f"CS3ZCC.harmonic.n{n}.laplacian", laplacian(qn) == {n: -n * (n + 2)}, "The declared zonal harmonic has Delta Q_n=-n(n+2)Q_n.")
    for left in range(4):
        for right in range(4):
            x = sp.symbols("x")
            identity = sp.expand(sp.chebyshevu(left, x) * sp.chebyshevu(right, x) - sum(sp.chebyshevu(degree, x) for degree in product_degrees(left, right)))
            ledger.check(f"CS3ZCC.product.U{left}.U{right}", identity == 0, "The finite zonal Chebyshev-U product identity holds exactly.")

    rows: list[dict[str, Any]] = []
    for packet in payload["coefficient_packets"]:
        cutoff = int(packet["cutoff_N"])
        psi = {int(degree): sp.sympify(coefficient) for degree, coefficient in packet["coefficients"].items()}
        if any(degree < 1 or degree > cutoff for degree in psi):
            raise AssertionError("packets must be declared zero-mean and cutoff-supported")
        delta_psi = laplacian(psi)
        psi2 = convolve(psi, psi, normalizer)
        psi3 = convolve(psi2, psi, normalizer)
        # 2|D psi|^2 = Delta(psi^2)-2 psi Delta psi is exact on a scalar manifold.
        grad2 = scale(subtract(laplacian(psi2), scale(convolve(psi, delta_psi, normalizer), 2)), sp.Rational(1, 2))
        d1 = add(scale(psi, 6), scale(delta_psi, -4))
        d2 = add(scale(psi2, 3), scale(convolve(psi, delta_psi, normalizer), -4), scale(grad2, -2))
        d3 = add(psi3, scale(convolve(psi2, delta_psi, normalizer), -2), scale(convolve(psi, grad2, normalizer), -2))
        exponential_coefficients = [constant_one, psi, scale(psi2, sp.Rational(1, 2)), scale(psi3, sp.Rational(1, 6))]
        bracket_coefficients = [scale(constant_one, 6), scale(delta_psi, -4), scale(grad2, -2)]
        reconstructed: list[dict[int, sp.Expr]] = []
        for order in range(4):
            reconstructed.append(add(*(convolve(exponential_coefficients[left_order], bracket_coefficients[order - left_order], normalizer) for left_order in range(order + 1) if left_order < len(exponential_coefficients) and order - left_order < len(bracket_coefficients))))
        ledger.check(f"CS3ZCC.packet.{packet['id']}.taylor_order0", reconstructed[0] == scale(constant_one, 6), "The independently multiplied Taylor series has the correctly normalized constant curvature density 6.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.taylor_order1", reconstructed[1] == d1, "Independent zonal convolution of the exponential and curvature brackets reconstructs d1.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.taylor_order2", reconstructed[2] == d2, "Independent zonal convolution of the exponential and curvature brackets reconstructs d2.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.taylor_order3", reconstructed[3] == d3, "Independent zonal convolution of the exponential and curvature brackets reconstructs d3.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.zero_mean", integral(psi, volume) == 0, "The declared packet has no constant mode, so its integrated linear curvature coefficient vanishes.")
        ibp_quadratic = sp.simplify(pairing(psi, delta_psi) + integral(grad2, volume))
        ibp_cubic = sp.simplify(integral(convolve(psi2, delta_psi, normalizer), volume) + 2 * integral(convolve(psi, grad2, normalizer), volume))
        ledger.check(f"CS3ZCC.packet.{packet['id']}.ibp_quadratic", ibp_quadratic == 0, "The zonal coefficients obey integral psi Delta psi=-integral |Dpsi|^2.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.ibp_cubic", ibp_cubic == 0, "The zonal coefficients obey integral psi^2 Delta psi=-2 integral psi|Dpsi|^2.")
        i1, i2, i3 = integral(d1, volume), integral(d2, volume), integral(d3, volume)
        ledger.check(f"CS3ZCC.packet.{packet['id']}.integrated_linear", sp.simplify(i1 - 6 * integral(psi, volume)) == 0, "The integrated linear curvature coefficient equals 6 integral psi and vanishes for the declared zero-mean packet.")
        i2_formula = sp.simplify(3 * pairing(psi, psi) + 2 * integral(grad2, volume))
        i3_formula = sp.simplify(integral(psi3, volume) + 2 * integral(convolve(psi, grad2, normalizer), volume))
        ledger.check(f"CS3ZCC.packet.{packet['id']}.integrated_quadratic", sp.simplify(i2 - i2_formula) == 0, "The integrated quadratic curvature coefficient equals 3 integral psi^2+2 integral |Dpsi|^2.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.integrated_cubic", sp.simplify(i3 - i3_formula) == 0, "The integrated cubic curvature coefficient equals integral psi^3+2 integral psi|Dpsi|^2.")
        d2_retained, d3_retained = project(d2, cutoff), project(d3, cutoff)
        d2_tail, d3_tail = subtract(d2, d2_retained), subtract(d3, d3_retained)
        ledger.check(f"CS3ZCC.packet.{packet['id']}.quadratic_projection", d2 == add(d2_retained, d2_tail), "The quadratic local density is retained plus its exact hard-cutoff tail.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.cubic_projection", d3 == add(d3_retained, d3_tail), "The cubic local density is retained plus its exact hard-cutoff tail.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.quadratic_tail_orthogonal", pairing(d2_retained, d2_tail) == 0, "The declared zonal P_N tail is orthogonal to the retained density coefficient.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.cubic_tail_orthogonal", pairing(d3_retained, d3_tail) == 0, "The declared zonal P_N tail is orthogonal to the retained density coefficient.")
        ledger.check(f"CS3ZCC.packet.{packet['id']}.nonzero_declared_tails", norm_squared(d2_tail) > 0 and norm_squared(d3_tail) > 0, "Both declared nonlinear density coefficients have a nonzero tail beyond N=2; this is a cutoff diagnostic only.")
        rows.append({"id": packet["id"], "purpose": packet["purpose"], "cutoff_N": cutoff, "psi_coefficients": printable(psi), "d1_coefficients": printable(d1), "d2_coefficients": printable(d2), "d3_coefficients": printable(d3), "integrated_coefficients_per_a": {"I1": str(i1), "I2": str(i2), "I3": str(i3)}, "d2_retained_coefficients": printable(d2_retained), "d2_tail_coefficients": printable(d2_tail), "d2_tail_norm_squared_exact": str(norm_squared(d2_tail)), "d3_retained_coefficients": printable(d3_retained), "d3_tail_coefficients": printable(d3_tail), "d3_tail_norm_squared_exact": str(norm_squared(d3_tail)), "scope": "spatial-curvature density only; tails are truncation diagnostics, not constraint-bracket residuals"})

    passed = all(check["passed"] for check in ledger.exact)
    verdict = "KEEP_CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_CUBIC_VERTEX_NOT_ADM_CONSTRAINT_OR_HDA" if passed else "KILL_DECLARED_CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_VERTEX"
    impact = "RECORD_A_SINGLE_ZONAL_SPATIAL_CURVATURE_VERTEX_PACKET_FOR_A_SEPARATE_OFF_SHELL_ADM_EXPANSION" if passed else "DO_NOT_USE_THIS_ZONAL_CURVATURE_PACKET_IN_A_CONSTRAINT_EXPANSION"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(check["passed"] for check in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "packet_results": rows, "computed_scope": "unit-S3 zonal conformal spatial-curvature density through cubic order only", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "result": RESULT_NAME, "result_sha256": sha256_bytes(encoded), "result_bytes": len(encoded), "automatic_next": None}, sort_keys=True))


if __name__ == "__main__":
    main()
