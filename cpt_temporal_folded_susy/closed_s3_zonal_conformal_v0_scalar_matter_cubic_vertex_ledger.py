#!/usr/bin/env python3
"""Restricted V=0 scalar normal-constraint-density cubic vertex on zonal S3.

This bounded ledger derives only a canonical scalar Hamiltonian density on the
declared conformal-zonal submanifold.  It is not lapse/shift elimination, a
full ADM constraint expansion, or an HDA/Jacobi calculation.
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

INPUT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_V0_SCALAR_MATTER_CUBIC_VERTEX_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_CONFORMAL_V0_SCALAR_MATTER_CUBIC_VERTEX_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_conformal_v0_scalar_matter_cubic_vertex_ledger.py"
EXPECTED_INPUT_SHA256 = "d5012c4757345cb5c215b1166c8cc1a219e9bb28061d121654360dd290826db9"
CALCULATION_ID = "ClosedS3ZonalConformalV0ScalarMatterCubicVertexLedger"
RESULT_SCHEMA = "ice.closed-s3-zonal-conformal-v0-scalar-matter-cubic-vertex-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_CONFORMAL_V0_SCALAR_MATTER_CUBIC_VERTEX_LEDGER_RESULT="
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
    return {"homogeneous_a_pa_cotangent_sector": None, "tracefree_shear_momenta": None, "spatial_metric_scalar_E_or_longitudinal_gauge_completion": None, "explicit_complete_scalar_vector_tensor_basis_functions": None, "full_gaunt_or_clebsch_gordan_ledger": None, "nonzonal_scalar_mode_couplings": None, "transverse_vector_tensor_mode_couplings": None, "scalar_potential_or_mass_extension": None, "matter_momentum_constraint_or_shift_vertex": None, "lapse_shift_elimination": None, "full_adm_linear_constraint_expansion": None, "full_adm_cubic_constraint_expansion": None, "lapse_shift_constraint_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "raw_C_operator_domain": None, "absolute_bfv_measure": None, "relational_observables": None, "born_oppenheimer_or_decoherence": None, "empirical_likelihood": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


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
    if payload["schema_version"] != "ice.closed-s3-zonal-conformal-v0-scalar-matter-cubic-vertex-ledger.input.v1" or payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps or fail-closed output drift")
    if payload["declared_conventions"]["v0_scalar_hamiltonian"] != "H_perp_phi/sqrt(gamma)=(2a^3)^(-1)[exp(-3 epsilon psi)(Pibar+epsilon xi)^2+a^4 epsilon^2 exp(epsilon psi)|D vartheta|^2]":
        raise AssertionError("V=0 Hamiltonian convention drift")
    return payload, observed


def degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def add(*vectors: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    total: dict[int, sp.Expr] = {}
    for vector in vectors:
        for degree, value in vector.items():
            total[degree] = sp.simplify(total.get(degree, sp.S.Zero) + value)
    return {degree: value for degree, value in total.items() if value != 0}


def scale(vector: dict[int, sp.Expr], factor: sp.Expr) -> dict[int, sp.Expr]:
    return {degree: sp.simplify(factor * value) for degree, value in vector.items() if factor * value != 0}


def convolve(left: dict[int, sp.Expr], right: dict[int, sp.Expr], normalizer: sp.Expr) -> dict[int, sp.Expr]:
    return add(*[{degree: sp.simplify(left_value * right_value * normalizer) for degree in degrees(left_degree, right_degree)} for left_degree, left_value in left.items() for right_degree, right_value in right.items()])


def laplacian(vector: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return {degree: sp.simplify(-degree * (degree + 2) * value) for degree, value in vector.items()}


def project(vector: dict[int, sp.Expr], cutoff: int) -> dict[int, sp.Expr]:
    return {degree: value for degree, value in vector.items() if degree <= cutoff}


def subtract(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return add(left, scale(right, -1))


def pairing(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(left.get(k, sp.S.Zero) * right.get(k, sp.S.Zero) for k in set(left) | set(right)))


def norm_squared(vector: dict[int, sp.Expr]) -> sp.Expr:
    return pairing(vector, vector)


def integral(vector: dict[int, sp.Expr], volume: sp.Expr) -> sp.Expr:
    return sp.simplify(vector.get(0, sp.S.Zero) * sp.sqrt(volume))


def printable(vector: dict[int, sp.Expr]) -> dict[str, str]:
    return {str(k): str(vector[k]) for k in sorted(vector)}


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    ledger.guard("CS3V0SM.guard.scalar_legendre", "Canonical V=0 scalar Legendre transform", "The pinned scalar action has V(phi)=0 and the present subvertex omits the shift term rather than eliminating it", "It supplies only the declared scalar normal-constraint density; no matter momentum-constraint vertex, lapse/shift equation, or full ADM constraint is derived.")
    ledger.guard("CS3V0SM.guard.zonal_gradient", "Product Laplacian identity", "For smooth zonal scalar packets on unit S3, 2|D f|^2=Delta(f^2)-2f Delta f", "The identity supplies zonal local gradient coefficients only, not nonzonal Gaunt data.")
    ledger.guard("CS3V0SM.guard.positive_scale_tail", "Positive scale-factor sign", "a>0, hence a^4>0", "The displayed Q4 quadratic tail coefficient -(1/2+4a^4)/sqrt(2*pi^2) cannot vanish; this remains a truncation diagnostic.")
    a, lapse, sqrt_q = sp.symbols("a lapse sqrt_q", positive=True)
    phi_dot, pi_phi, grad_sq = sp.symbols("phi_dot pi_phi grad_sq", real=True)
    epsilon, Pibar = sp.symbols("epsilon Pibar", real=True)
    volume = 2 * sp.pi**2
    normalizer = 1 / sp.sqrt(volume)
    constant_one = {0: sp.sqrt(volume)}
    scalar_lagrangian = sqrt_q * (phi_dot**2 / (2 * lapse) - lapse * grad_sq / 2)
    momentum = sp.diff(scalar_lagrangian, phi_dot)
    velocity = sp.solve(sp.Eq(pi_phi, momentum), phi_dot)[0]
    hamiltonian = sp.simplify(pi_phi * velocity - scalar_lagrangian.subs(phi_dot, velocity))
    ledger.check("CS3V0SM.canonical.local_legendre", hamiltonian - lapse * (pi_phi**2 / (2 * sqrt_q) + sqrt_q * grad_sq / 2), "At zero shift, the V=0 local scalar Legendre transform gives N times the scalar normal-constraint density; the shift vertex is not computed.")
    ledger.check("CS3V0SM.canonical.homogeneous_match", volume * Pibar**2 / (2 * a**3) - (volume * Pibar)**2 / (4 * sp.pi**2 * a**3), "p_phi=2*pi^2 Pibar reduces the restricted homogeneous scalar term to the pinned p_phi^2/(4*pi^2*a^3).")
    ledger.check("CS3V0SM.canonical.constant_identity", convolve(constant_one, {2: sp.S.One}, normalizer) == {2: sp.S.One}, "sqrt(2*pi^2)Q0 is the multiplicative identity in the normalized zonal basis.")
    delta_phi_bar, integral_xi, integral_delta_vartheta, integral_xi_delta_vartheta = sp.symbols(
        "delta_phi_bar integral_xi integral_delta_vartheta integral_xi_delta_vartheta",
        real=True,
    )
    unrestricted_symplectic_expansion = (
        volume * Pibar * delta_phi_bar
        + epsilon * Pibar * integral_delta_vartheta
        + epsilon * delta_phi_bar * integral_xi
        + epsilon**2 * integral_xi_delta_vartheta
    )
    zero_mean_symplectic_expansion = unrestricted_symplectic_expansion.subs(
        {integral_xi: 0, integral_delta_vartheta: 0}
    )
    ledger.check(
        "CS3V0SM.canonical.formal_symplectic_order",
        zero_mean_symplectic_expansion
        - (volume * Pibar * delta_phi_bar + epsilon**2 * integral_xi_delta_vartheta),
        "When the zero-mean sector is preserved under variations, the inhomogeneous symplectic coefficient first occurs at order epsilon^2.",
    )
    for n in range(5):
        ledger.check(f"CS3V0SM.harmonic.n{n}.laplacian", laplacian({n: sp.S.One}) == {n: -n * (n + 2)}, "The declared zonal Q_n obeys Delta Q_n=-n(n+2)Q_n.")
    for left in range(4):
        for right in range(4):
            x = sp.symbols("x")
            ledger.check(f"CS3V0SM.product.U{left}.U{right}", sp.expand(sp.chebyshevu(left, x) * sp.chebyshevu(right, x) - sum(sp.chebyshevu(k, x) for k in degrees(left, right))), "The finite Chebyshev-U zonal product identity holds exactly.")
    rows: list[dict[str, Any]] = []
    for packet in payload["coefficient_packets"]:
        cutoff = int(packet["cutoff_N"])
        pbar = sp.sympify(packet["Pibar"])
        psi = {int(k): sp.sympify(v) for k, v in packet["psi_coefficients"].items()}
        xi = {int(k): sp.sympify(v) for k, v in packet["xi_coefficients"].items()}
        vartheta = {int(k): sp.sympify(v) for k, v in packet["vartheta_coefficients"].items()}
        if any(k < 1 or k > cutoff for k in set(psi) | set(xi) | set(vartheta)):
            raise AssertionError("all perturbative packets must be zero-mean and cutoff-supported")
        psi2, psi3 = convolve(psi, psi, normalizer), convolve(convolve(psi, psi, normalizer), psi, normalizer)
        xi2, psi_xi = convolve(xi, xi, normalizer), convolve(psi, xi, normalizer)
        psi2_xi, psi_xi2 = convolve(psi2, xi, normalizer), convolve(psi, xi2, normalizer)
        grad2 = scale(subtract(laplacian(convolve(vartheta, vartheta, normalizer)), scale(convolve(vartheta, laplacian(vartheta), normalizer), 2)), sp.Rational(1, 2))
        psi_grad2 = convolve(psi, grad2, normalizer)
        m0 = scale(constant_one, pbar**2)
        m1 = add(scale(xi, 2 * pbar), scale(psi, -3 * pbar**2))
        m2 = add(xi2, scale(psi_xi, -6 * pbar), scale(psi2, sp.Rational(9, 2) * pbar**2), scale(grad2, a**4))
        m3 = add(scale(psi_xi2, -3), scale(psi2_xi, 9 * pbar), scale(psi3, -sp.Rational(9, 2) * pbar**2), scale(psi_grad2, a**4))
        exp_minus = [constant_one, scale(psi, -3), scale(psi2, sp.Rational(9, 2)), scale(psi3, -sp.Rational(9, 2))]
        momentum_square = [scale(constant_one, pbar**2), scale(xi, 2 * pbar), xi2]
        reconstructed = [add(*(convolve(exp_minus[i], momentum_square[r - i], normalizer) for i in range(r + 1) if i < len(exp_minus) and r - i < len(momentum_square))) for r in range(4)]
        reconstructed[2] = add(reconstructed[2], scale(grad2, a**4))
        reconstructed[3] = add(reconstructed[3], scale(psi_grad2, a**4))
        for order, target in enumerate([m0, m1, m2, m3]):
            ledger.check(f"CS3V0SM.packet.{packet['id']}.taylor_order{order}", reconstructed[order] == target, "Independent Taylor multiplication reconstructs the declared V=0 scalar-matter coefficient.")
        ledger.check(f"CS3V0SM.packet.{packet['id']}.zero_mean", integral(psi, volume) == 0 and integral(xi, volume) == 0 and integral(vartheta, volume) == 0, "All declared perturbative fields have zero homogeneous harmonic coefficient, so p_phi=2*pi^2*Pibar and the symplectic cross terms vanish.")
        momentum_density = add(scale(constant_one, pbar), scale(xi, epsilon))
        ledger.check(f"CS3V0SM.packet.{packet['id']}.total_momentum", integral(momentum_density, volume) - volume * pbar, "The packet's zero-mean xi leaves the total scalar momentum equal to 2*pi^2*Pibar.")
        expected_gradient_integral = sum(k * (k + 2) * value**2 for k, value in vartheta.items())
        ledger.check(f"CS3V0SM.packet.{packet['id']}.gradient_integral", integral(grad2, volume) - expected_gradient_integral, "The integrated exact gradient coefficient equals the scalar spectral sum lambda_n vartheta_n^2.")
        m2_keep, m3_keep = project(m2, cutoff), project(m3, cutoff)
        m2_tail, m3_tail = subtract(m2, m2_keep), subtract(m3, m3_keep)
        for order, full, keep, tail in [(2, m2, m2_keep, m2_tail), (3, m3, m3_keep, m3_tail)]:
            ledger.check(f"CS3V0SM.packet.{packet['id']}.projection_m{order}", full == add(keep, tail), "The local coefficient is exactly retained plus hard-cutoff tail.")
            ledger.check(f"CS3V0SM.packet.{packet['id']}.tail_orthogonal_m{order}", pairing(keep, tail), "Normalized-zonal retained and tail coefficients are orthogonal.")
        aligned_m2_tail = {4: -normalizer * (sp.Rational(1, 2) + 4 * a**4)}
        aligned_m3_tail = {4: sp.Rational(3, 2) / sp.pi**2, 6: sp.Rational(3, 4) / sp.pi**2 - 2 * a**4 / sp.pi**2}
        ledger.check(f"CS3V0SM.packet.{packet['id']}.aligned_m2_tail", subtract(m2_tail, aligned_m2_tail) == {}, "The aligned Q2 quadratic tail has the exact positive-scale nonzero Q4 coefficient.")
        ledger.check(f"CS3V0SM.packet.{packet['id']}.aligned_m3_tail", subtract(m3_tail, aligned_m3_tail) == {}, "The aligned Q2 cubic tail has the exact displayed Q4 and Q6 coefficients; only Q4 is asserted nonzero for every a>0.")
        ledger.check(f"CS3V0SM.packet.{packet['id']}.aligned_m3_Q4_nonzero", m3_tail.get(4, sp.S.Zero) - sp.Rational(3, 2) / sp.pi**2, "The cubic Q4 tail is a nonzero a-independent exact coefficient.")
        rows.append({"id": packet["id"], "purpose": packet["purpose"], "cutoff_N": cutoff, "Pibar_packet_normalization": str(pbar), "external_physical_factor": "1/(2*a^3)", "psi_coefficients": printable(psi), "xi_coefficients": printable(xi), "vartheta_coefficients": printable(vartheta), "gradient_squared_coefficients": printable(grad2), "m0_coefficients": printable(m0), "m1_coefficients": printable(m1), "m2_coefficients": printable(m2), "m3_coefficients": printable(m3), "m2_retained_coefficients": printable(m2_keep), "m2_tail_coefficients": printable(m2_tail), "m2_tail_norm_squared_exact": str(norm_squared(m2_tail)), "m3_retained_coefficients": printable(m3_keep), "m3_tail_coefficients": printable(m3_tail), "m3_tail_norm_squared_exact": str(norm_squared(m3_tail)), "scope": "restricted formal V=0 scalar normal-constraint-density expansion only; the matter shift vertex is null and tails are truncation diagnostics, not constraint-bracket residuals"})
    passed = all(check["passed"] for check in ledger.exact)
    verdict = "KEEP_CLOSED_S3_ZONAL_CONFORMAL_V0_SCALAR_MATTER_CUBIC_VERTEX_NOT_FULL_ADM_OR_HDA" if passed else "KILL_DECLARED_CLOSED_S3_V0_SCALAR_MATTER_VERTEX"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": "RECORD_A_RESTRICTED_V0_SCALAR_NORMAL_CONSTRAINT_DENSITY_VERTEX_ALONGSIDE_THE_SEPARATE_CURVATURE_AND_TRACE_KINETIC_PACKETS" if passed else "DO_NOT_USE_THIS_RESTRICTED_MATTER_PACKET", "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(check["passed"] for check in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "packet_results": rows, "computed_scope": "restricted formal V=0 scalar normal-constraint-density expansion through cubic order in one normalized zonal packet", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
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
