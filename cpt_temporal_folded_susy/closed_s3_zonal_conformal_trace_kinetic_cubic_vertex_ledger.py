#!/usr/bin/env python3
"""Restricted canonical conformal-trace ADM kinetic cubic-vertex ledger.

Only the trace cotangent submanifold and normalized zonal products occur here.
This is not a full ADM constraint, a lapse/shift calculation, or an HDA test.
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


INPUT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_CUBIC_VERTEX_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_CUBIC_VERTEX_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_conformal_trace_kinetic_cubic_vertex_ledger.py"
EXPECTED_INPUT_SHA256 = "9b1e840e3a2589bb53e251b9cd60bd2f6bd0b8262779e6952217fa8acd52e563"
CALCULATION_ID = "ClosedS3ZonalConformalTraceKineticCubicVertexLedger"
RESULT_SCHEMA = "ice.closed-s3-zonal-conformal-trace-kinetic-cubic-vertex-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_CUBIC_VERTEX_LEDGER_RESULT="
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

    def guard(self, guard_id: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        if guard_id in self.seen:
            raise AssertionError(f"duplicate guard id: {guard_id}")
        self.seen.add(guard_id)
        self.guards.append({"id": guard_id, "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {"homogeneous_a_pa_cotangent_sector": None, "tracefree_shear_momenta": None, "explicit_complete_scalar_vector_tensor_basis_functions": None, "full_gaunt_or_clebsch_gordan_ledger": None, "nonzonal_scalar_mode_couplings": None, "transverse_vector_tensor_mode_couplings": None, "matter_perturbation_vertex": None, "lapse_shift_elimination": None, "full_adm_linear_constraint_expansion": None, "full_adm_cubic_constraint_expansion": None, "lapse_shift_constraint_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "raw_C_operator_domain": None, "absolute_bfv_measure": None, "relational_observables": None, "born_oppenheimer_or_decoherence": None, "empirical_likelihood": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    value = json.loads(raw)
    if value.get("run_status") != "VALID_RUN" or value.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream status/verdict mismatch: {item['path']}")
    if value.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed, "payload_sha256_without_self": value["result_payload_sha256_without_self"], "verdict": value["verdict"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.closed-s3-zonal-conformal-trace-kinetic-cubic-vertex-ledger.input.v1" or payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps or fail-closed output drift")
    if payload["declared_conventions"]["deWitt_reduction"] != "H_kin/sqrt(gamma)=-(2*pi*G/(3*a^3))*exp(-3 omega)*Pi^2":
        raise AssertionError("DeWitt coefficient convention drift")
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
    ledger.guard("CS3ZCTK.guard.adm_dewitt", "ADM DeWitt kinetic density", "The ADM convention is H_kin=16*pi*G/sqrt(q)(pi^{ab}pi_ab-pi^2/2)", "This runner evaluates that density only on the declared trace cotangent submanifold; it does not derive a full constraint or its brackets.")
    ledger.guard("CS3ZCTK.guard.restricted_symplectic", "Restriction of the ADM symplectic potential", "Variations hold a fixed and vary only omega in the declared q_ab and pi^{ab} ansatz", "The resulting Pi is canonical only on this restricted trace/conformal submanifold; no full ADM canonical chart is constructed.")
    ledger.guard("CS3ZCTK.guard.zonal_product_scope", "Chebyshev-U zonal product identity", "Only normalized zonal Q_n and the pinned upstream product convention are used", "No nonzonal scalar, vector, tensor, or full Gaunt coefficient is supplied.")
    a, G, sqrt_gamma = sp.symbols("a G sqrt_gamma", positive=True, real=True)
    omega, pi_scalar = sp.symbols("omega Pi", real=True)
    q_scalar = a**2 * sp.exp(2 * omega)
    pi_factor = sqrt_gamma * pi_scalar / (6 * q_scalar)
    trace_pi = sp.simplify(3 * pi_factor * q_scalar)
    pi_ab_pi_ab = sp.simplify(3 * pi_factor**2 * q_scalar**2)
    dewitt_contraction = sp.simplify(pi_ab_pi_ab - trace_pi**2 / 2)
    sqrt_q = sqrt_gamma * a**3 * sp.exp(3 * omega)
    kinetic_per_sqrt_gamma = sp.simplify(16 * sp.pi * G * dewitt_contraction / sqrt_q / sqrt_gamma)
    symplectic_density = sp.simplify(3 * pi_factor * (2 * q_scalar))
    ledger.check("CS3ZCTK.canonical.trace_contraction", trace_pi == sqrt_gamma * pi_scalar / 2, "The declared pure-trace momentum has pi=sqrt(gamma)Pi/2.")
    ledger.check("CS3ZCTK.canonical.quadratic_contraction", pi_ab_pi_ab == sqrt_gamma**2 * pi_scalar**2 / 12, "The declared pure-trace momentum has pi^{ab}pi_ab=gamma Pi^2/12.")
    ledger.check("CS3ZCTK.canonical.dewitt_contraction", dewitt_contraction == -sqrt_gamma**2 * pi_scalar**2 / 24, "Thus pi^{ab}pi_ab-pi^2/2=-gamma Pi^2/24.")
    ledger.check("CS3ZCTK.canonical.kinetic_external_factor", kinetic_per_sqrt_gamma == -2 * sp.pi * G * sp.exp(-3 * omega) * pi_scalar**2 / (3 * a**3), "The external physical factor is -2*pi*G/(3*a^3), fixed by the canonical Pi normalization.")
    ledger.check("CS3ZCTK.canonical.restricted_symplectic", symplectic_density == sqrt_gamma * pi_scalar, "At fixed a, pi^{ab} delta_omega q_ab=sqrt(gamma)Pi delta omega exactly.")
    pi_const = sp.pi
    volume = 2 * pi_const**2
    normalizer = 1 / sp.sqrt(volume)
    constant_one = {0: sp.sqrt(volume)}
    ledger.check("CS3ZCTK.normalization.constant_one", convolve(constant_one, {2: sp.S.One}, normalizer) == {2: sp.S.One}, "sqrt(2*pi^2)Q_0 is the multiplicative identity in the normalized zonal basis.")
    for left in range(4):
        for right in range(4):
            x = sp.symbols("x")
            identity = sp.expand(sp.chebyshevu(left, x) * sp.chebyshevu(right, x) - sum(sp.chebyshevu(degree, x) for degree in product_degrees(left, right)))
            ledger.check(f"CS3ZCTK.product.U{left}.U{right}", identity == 0, "The declared finite Chebyshev-U zonal product identity holds exactly.")
    rows: list[dict[str, Any]] = []
    pbar = sp.Integer(1)
    for packet in payload["coefficient_packets"]:
        cutoff = int(packet["cutoff_N"])
        psi = {int(degree): sp.sympify(coefficient) for degree, coefficient in packet["psi_coefficients"].items()}
        chi = {int(degree): sp.sympify(coefficient) for degree, coefficient in packet["chi_coefficients"].items()}
        if any(degree < 1 or degree > cutoff for degree in set(psi) | set(chi)):
            raise AssertionError("all packet fields must be zero-mean and cutoff-supported")
        psi2, psi3 = convolve(psi, psi, normalizer), convolve(convolve(psi, psi, normalizer), psi, normalizer)
        chi2 = convolve(chi, chi, normalizer)
        psi_chi = convolve(psi, chi, normalizer)
        psi_chi2 = convolve(psi, chi2, normalizer)
        psi2_chi = convolve(psi2, chi, normalizer)
        k0 = {0: pbar**2 * sp.sqrt(volume)}
        k1 = add(scale(chi, 2 * pbar), scale(psi, -3 * pbar**2))
        k2 = add(chi2, scale(psi_chi, -6 * pbar), scale(psi2, sp.Rational(9, 2) * pbar**2))
        k3 = add(scale(psi_chi2, -3), scale(psi2_chi, 9 * pbar), scale(psi3, -sp.Rational(9, 2) * pbar**2))
        exp_coefficients = [constant_one, scale(psi, -3), scale(psi2, sp.Rational(9, 2)), scale(psi3, -sp.Rational(9, 2))]
        momentum_square = [scale(constant_one, pbar**2), scale(chi, 2 * pbar), chi2]
        reconstructed: list[dict[int, sp.Expr]] = []
        for order in range(4):
            reconstructed.append(add(*(convolve(exp_coefficients[left_order], momentum_square[order - left_order], normalizer) for left_order in range(order + 1) if left_order < len(exp_coefficients) and order - left_order < len(momentum_square))))
        for order, target in enumerate([k0, k1, k2, k3]):
            ledger.check(f"CS3ZCTK.packet.{packet['id']}.taylor_order{order}", reconstructed[order] == target, "Independent zonal multiplication of exp(-3 epsilon psi) and (Pbar+epsilon chi)^2 reconstructs the declared kinetic coefficient.")
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.zero_mean_fields", integral(psi, volume) == 0 and integral(chi, volume) == 0, "The declared psi and chi packets contain no constant perturbative mode.")
        k2_retained, k3_retained = project(k2, cutoff), project(k3, cutoff)
        k2_tail, k3_tail = subtract(k2, k2_retained), subtract(k3, k3_retained)
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.quadratic_projection", k2 == add(k2_retained, k2_tail), "The quadratic restricted kinetic coefficient is retained plus its exact hard-cutoff tail.")
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.cubic_projection", k3 == add(k3_retained, k3_tail), "The cubic restricted kinetic coefficient is retained plus its exact hard-cutoff tail.")
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.quadratic_tail_orthogonal", pairing(k2_retained, k2_tail) == 0, "The normalized-zonal quadratic tail is orthogonal to its retained coefficient.")
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.cubic_tail_orthogonal", pairing(k3_retained, k3_tail) == 0, "The normalized-zonal cubic tail is orthogonal to its retained coefficient.")
        ledger.check(f"CS3ZCTK.packet.{packet['id']}.nonzero_declared_tails", norm_squared(k2_tail) > 0 and norm_squared(k3_tail) > 0, "Both declared nonlinear restricted kinetic coefficients have nonzero cutoff tails; this is not an algebra residual.")
        rows.append({"id": packet["id"], "purpose": packet["purpose"], "cutoff_N": cutoff, "Pbar_packet_normalization": "1", "external_physical_factor": "-2*pi*G/(3*a^3)", "psi_coefficients": printable(psi), "chi_coefficients": printable(chi), "k0_coefficients": printable(k0), "k1_coefficients": printable(k1), "k2_coefficients": printable(k2), "k3_coefficients": printable(k3), "integrated_dimensionless_coefficients": {"K0": str(integral(k0, volume)), "K1": str(integral(k1, volume)), "K2": str(integral(k2, volume)), "K3": str(integral(k3, volume))}, "k2_retained_coefficients": printable(k2_retained), "k2_tail_coefficients": printable(k2_tail), "k2_tail_norm_squared_exact": str(norm_squared(k2_tail)), "k3_retained_coefficients": printable(k3_retained), "k3_tail_coefficients": printable(k3_tail), "k3_tail_norm_squared_exact": str(norm_squared(k3_tail)), "scope": "restricted trace kinetic density only; tails are truncation diagnostics, not ADM constraint-bracket residuals"})
    passed = all(check["passed"] for check in ledger.exact)
    verdict = "KEEP_CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_CUBIC_VERTEX_NOT_FULL_ADM_OR_HDA" if passed else "KILL_DECLARED_CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_VERTEX"
    impact = "RECORD_A_RESTRICTED_CANONICAL_KINETIC_VERTEX_PACKET_ALONGSIDE_THE_SEPARATE_ZONAL_CURVATURE_VERTEX" if passed else "DO_NOT_USE_THIS_RESTRICTED_KINETIC_PACKET_IN_A_CONSTRAINT_EXPANSION"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(check["passed"] for check in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "packet_results": rows, "computed_scope": "restricted canonical conformal-trace ADM kinetic density through cubic order in normalized zonal packets only", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
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
