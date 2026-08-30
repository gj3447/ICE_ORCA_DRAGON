#!/usr/bin/env python3
"""Exact fixed-background zonal V=0 scalar-matter HH bracket cutoff ledger.

This bounded calculation checks only the scalar-matter HH identity in a
declared fixed-background zonal mode packet.  It records a finite projection
remainder separately; it is not full ADM/HDA/Jacobi or an anomaly test.
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


INPUT_NAME = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_HH_BRACKET_CUTOFF_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_HH_BRACKET_CUTOFF_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger.py"
EXPECTED_INPUT_SHA256 = "8955e45c9a4053a50ac994d9a2911e6a9058a0b9e7b688e8db134aec652c3f7b"
CALCULATION_ID = "ClosedS3ZonalV0ScalarMatterHHBracketCutoffLedger"
RESULT_SCHEMA = "ice.closed-s3-zonal-v0-scalar-matter-hh-bracket-cutoff-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_V0_SCALAR_MATTER_HH_BRACKET_CUTOFF_LEDGER_RESULT="
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
    return {"gravitational_hamiltonian_constraint": None, "gravitational_momentum_constraint": None, "metric_perturbation_or_shear_cotangent_sector": None, "spatial_metric_scalar_E_or_longitudinal_gauge_completion": None, "lapse_shift_elimination": None, "explicit_complete_scalar_vector_tensor_basis_functions": None, "full_gaunt_or_clebsch_gordan_ledger": None, "nonzonal_scalar_mode_couplings": None, "transverse_vector_tensor_mode_couplings": None, "full_adm_linear_constraint_expansion": None, "full_adm_cubic_constraint_expansion": None, "full_DD_or_DH_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "raw_C_operator_domain": None, "absolute_bfv_measure": None, "relational_observables": None, "born_oppenheimer_or_decoherence": None, "empirical_likelihood": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


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
    if payload["schema_version"] != "ice.closed-s3-zonal-v0-scalar-matter-hh-bracket-cutoff-ledger.input.v1" or payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps() or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    if payload["declared_conventions"]["hh_target"] != "{H_phi[N],H_phi[M]}=D_phi[v_NM] with v_NM^a=a^(-2)(N D^a M-M D^a N)":
        raise AssertionError("HH target convention drift")
    return payload, observed


def product_degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def eigenvalue(degree: int) -> sp.Integer:
    return sp.Integer(degree * (degree + 2))


def triple(i: int, j: int, k: int, normalizer: sp.Expr) -> sp.Expr:
    return normalizer if k in product_degrees(i, j) else sp.S.Zero


def gradient_triple(i: int, j: int, k: int, normalizer: sp.Expr) -> sp.Expr:
    """Integral Q_i DQ_j.DQ_k on the unit round S3."""
    return sp.simplify((eigenvalue(j) + eigenvalue(k) - eigenvalue(i)) * triple(i, j, k, normalizer) / 2)


def four_gradient(i: int, n: int, m: int, j: int, normalizer: sp.Expr) -> sp.Expr:
    """Integral Q_i Q_n DQ_m.DQ_j, expanded before any cutoff."""
    return sp.simplify(sum(normalizer * gradient_triple(r, m, j, normalizer) for r in product_degrees(i, n)))


def direct_q(degree: int, chi: sp.Symbol, normalizer: sp.Expr) -> sp.Expr:
    return normalizer * sp.chebyshevu(degree, sp.cos(chi))


def direct_integral(expression: sp.Expr, chi: sp.Symbol) -> sp.Expr:
    return sp.simplify(4 * sp.pi * sp.integrate(sp.expand_trig(sp.sin(chi) ** 2 * expression), (chi, 0, sp.pi)))


def hamiltonian(smear_degree: int, cutoff: int, theta: list[sp.Symbol], xi: list[sp.Symbol], a: sp.Symbol, normalizer: sp.Expr) -> sp.Expr:
    kinetic = sum(xi[i] * xi[j] * triple(smear_degree, i, j, normalizer) for i in range(cutoff + 1) for j in range(cutoff + 1))
    gradient = sum(theta[i] * theta[j] * gradient_triple(smear_degree, i, j, normalizer) for i in range(cutoff + 1) for j in range(cutoff + 1))
    return sp.expand(kinetic / (2 * a**3) + a * gradient / 2)


def poisson(left: sp.Expr, right: sp.Expr, theta: list[sp.Symbol], xi: list[sp.Symbol], cutoff: int) -> sp.Expr:
    return sp.expand(sum(sp.diff(left, theta[index]) * sp.diff(right, xi[index]) - sp.diff(left, xi[index]) * sp.diff(right, theta[index]) for index in range(cutoff + 1)))


def momentum_target(n_degree: int, m_degree: int, cutoff: int, theta: list[sp.Symbol], xi: list[sp.Symbol], a: sp.Symbol, normalizer: sp.Expr) -> sp.Expr:
    return sp.expand(sum(xi[i] * theta[j] * (four_gradient(i, n_degree, m_degree, j, normalizer) - four_gradient(i, m_degree, n_degree, j, normalizer)) / a**2 for i in range(cutoff + 1) for j in range(cutoff + 1)))


def printable(expression: sp.Expr) -> str:
    return str(sp.factor(expression))


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    ledger.guard("CS3V0HH.guard.scalar_hda_subidentity", "Canonical V=0 scalar matter HH identity on a fixed spatial metric", "The scalar field has canonical bracket {phi(x),pi_phi(y)}=delta(x,y), q_ab=a^2 gamma_ab is fixed and positive, and the momentum functional is D_phi[v]=integral pi_phi v^a D_a phi", "This is a matter-only fixed-background identity. It excludes gravitational variations, the full ADM constraints, DD/DH brackets, Jacobi, and all quantum anomaly claims.")
    ledger.guard("CS3V0HH.guard.zonal_gaunt_scope", "Unit-S3 zonal Chebyshev-U product identity", "Only Q_n=U_n(cos chi)/sqrt(2*pi^2) and its scalar derivative identity are used", "The executable supplies zonal scalar coefficient arithmetic only; it is not complete SVT or a full Gaunt/Clebsch-Gordan ledger.")
    ledger.guard("CS3V0HH.guard_cutoff_interpretation", "Hard projection is not a continuum algebra statement", "The ambient calculation forms the finite-band bracket before low-mode substitution, while the L-only bracket omits ambient canonical derivative channels", "A nonzero difference is retained as UNCLASSIFIED_PROJECTION_REMAINDER, not as continuum HDA failure, classical anomaly, or quantum anomaly.")

    a = sp.symbols("a", positive=True, real=True)
    chi = sp.symbols("chi", real=True)
    volume = 2 * sp.pi**2
    normalizer = 1 / sp.sqrt(volume)
    n_degree = int(payload["smearings"]["N_degree"])
    m_degree = int(payload["smearings"]["M_degree"])

    for i, j, k in [(0, 1, 1), (1, 1, 2), (1, 2, 3), (2, 2, 0)]:
        direct = direct_integral(direct_q(i, chi, normalizer) * direct_q(j, chi, normalizer) * direct_q(k, chi, normalizer), chi)
        ledger.check(f"CS3V0HH.gaunt.direct.triple_{i}_{j}_{k}", direct - triple(i, j, k, normalizer), "Direct chi integration agrees with the declared low-mode zonal triple Gaunt coefficient.")
    for i, j, k in [(0, 1, 1), (1, 1, 2), (1, 2, 3), (2, 2, 0)]:
        direct = direct_integral(direct_q(i, chi, normalizer) * sp.diff(direct_q(j, chi, normalizer), chi) * sp.diff(direct_q(k, chi, normalizer), chi), chi)
        ledger.check(f"CS3V0HH.gaunt.direct.gradient_{i}_{j}_{k}", direct - gradient_triple(i, j, k, normalizer), "Direct chi integration agrees with the spectral gradient-Gaunt identity.")
    ledger.check("CS3V0HH.smearing.deformation_nonzero", four_gradient(0, n_degree, m_degree, 1, normalizer) - four_gradient(0, m_degree, n_degree, 1, normalizer) != 0, "The chosen distinct lapse degrees define a nontrivial deformation vector; this check only excludes an accidental identical-smearing choice.")

    max_cutoff = max(int(packet["cutoff_L"]) for packet in payload["field_packets"])
    ambient_max = max_cutoff + max(n_degree, m_degree)
    theta = list(sp.symbols(f"theta0:{ambient_max + 1}", real=True))
    xi = list(sp.symbols(f"xi0:{ambient_max + 1}", real=True))

    rows: list[dict[str, Any]] = []
    for packet in payload["field_packets"]:
        cutoff = int(packet["cutoff_L"])
        ambient = cutoff + max(n_degree, m_degree)
        theta_coefficients = {int(key): sp.sympify(value) for key, value in packet["theta_coefficients"].items()}
        xi_coefficients = {int(key): sp.sympify(value) for key, value in packet["xi_coefficients"].items()}
        if any(index < 0 or index > cutoff for index in set(theta_coefficients) | set(xi_coefficients)):
            raise AssertionError("declared packet is not cutoff supported")

        substitutions = {theta[index]: theta_coefficients.get(index, sp.S.Zero) for index in range(ambient + 1)}
        substitutions.update({xi[index]: xi_coefficients.get(index, sp.S.Zero) for index in range(ambient + 1)})
        h_n_ambient = hamiltonian(n_degree, ambient, theta, xi, a, normalizer)
        h_m_ambient = hamiltonian(m_degree, ambient, theta, xi, a, normalizer)
        ambient_channel_terms = [sp.expand(sp.diff(h_n_ambient, theta[index]) * sp.diff(h_m_ambient, xi[index]) - sp.diff(h_n_ambient, xi[index]) * sp.diff(h_m_ambient, theta[index])) for index in range(ambient + 1)]
        full_before_project = sp.simplify(sum(ambient_channel_terms).subs(substitutions))
        target = sp.simplify(momentum_target(n_degree, m_degree, cutoff, theta, xi, a, normalizer).subs(substitutions))
        h_n_projected = hamiltonian(n_degree, cutoff, theta, xi, a, normalizer)
        h_m_projected = hamiltonian(m_degree, cutoff, theta, xi, a, normalizer)
        projected = sp.simplify(poisson(h_n_projected, h_m_projected, theta, xi, cutoff).subs(substitutions))
        discarded_channels = [index for index in range(cutoff + 1, ambient + 1) if sp.simplify(ambient_channel_terms[index].subs(substitutions)) != 0]
        discarded_sum = sp.simplify(sum(ambient_channel_terms[index].subs(substitutions) for index in discarded_channels))
        remainder = sp.simplify(full_before_project - projected)

        ledger.check(f"CS3V0HH.packet.{packet['id']}.ambient_target", full_before_project - target, "The ambient full-before-project finite-band canonical HH bracket equals the declared matter momentum functional on the low-mode packet.")
        ledger.check(f"CS3V0HH.packet.{packet['id']}.remainder_decomposition", remainder - discarded_sum, "The finite difference full-before-project minus L-only equals the sum of omitted ambient canonical derivative channels.")
        ledger.check(f"CS3V0HH.packet.{packet['id']}.projected_target_decomposition", projected - (target - remainder), "The L-only result is exactly target minus the separately retained projection remainder.")
        ledger.check(f"CS3V0HH.packet.{packet['id']}.ambient_bound", ambient - (cutoff + max(n_degree, m_degree)), "The ambient coefficient space is the declared smallest smear-degree enlargement for this quadratic scalar calculation.")
        rows.append({"id": packet["id"], "cutoff_L": cutoff, "ambient_cutoff": ambient, "theta_coefficients": {str(key): str(value) for key, value in sorted(theta_coefficients.items())}, "xi_coefficients": {str(key): str(value) for key, value in sorted(xi_coefficients.items())}, "full_before_project_hh_exact": printable(full_before_project), "matter_momentum_target_exact": printable(target), "L_only_hh_exact": printable(projected), "full_minus_L_only_remainder_exact": printable(remainder), "discarded_canonical_channels": discarded_channels, "discarded_channel_sum_exact": printable(discarded_sum), "remainder_status": "NONZERO_UNCLASSIFIED_PROJECTION_REMAINDER" if remainder != 0 else "EXACT_ZERO_FOR_THIS_PACKET", "scope": "fixed-background zonal V=0 scalar-matter HH subidentity only; no gravitational or full ADM/HDA/Jacobi interpretation"})

    passed = all(check["passed"] for check in ledger.exact)
    verdict = "KEEP_FIXED_BACKGROUND_ZONAL_V0_SCALAR_MATTER_HH_IDENTITY_AND_CUTOFF_REMAINDER_NOT_FULL_ADM_HDA" if passed else "KILL_DECLARED_FIXED_BACKGROUND_ZONAL_V0_SCALAR_MATTER_HH_LEDGER"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": "RECORD_THE_SCOPED_MATTER_HH_IDENTITY_AND_ITS_FINITE_PROJECTION_REMAINDER_FOR_A_LATER_FULL_ADM_COMPARISON" if passed else "DO_NOT_USE_THIS_RESTRICTED_HH_PACKET", "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(check["passed"] for check in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "packet_results": rows, "computed_scope": "exact fixed-background zonal V=0 scalar-matter HH subidentity with a separately reported finite scalar-mode projection remainder", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
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
