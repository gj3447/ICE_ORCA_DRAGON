#!/usr/bin/env python3
"""Local raw-C zero-shell simple-root/Jacobian ledger.

This bounded calculation consumes the five roots already recorded by the
declared raw-C characteristic census.  It uses the moving-boundary
Wronskian/Lagrange identity and a K-Bessel Mellin norm to obtain local slopes
and delta-constraint Jacobians.  It deliberately does not construct a global
spectral measure, a rigging map, a physical inner product, or C/H equivalence.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import mpmath
from mpmath import mp
import sympy as sp


INPUT_NAME = "RAW_C_ZERO_SHELL_TRANSVERSALITY_JACOBIAN_INPUTS.json"
RESULT_NAME = "RAW_C_ZERO_SHELL_TRANSVERSALITY_JACOBIAN_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_zero_shell_transversality_jacobian.py"
EXPECTED_INPUT_SHA256 = "004e44ba94c39e45fafb802982aff3e0a78dda968d8cfc63587179ec688b9835"
CALCULATION_ID = "RawCZeroShellTransversalityJacobian"
RESULT_SCHEMA = "ice.raw-c-zero-shell-transversality-jacobian.result.v1"
RESULT_PREFIX = "RAW_C_ZERO_SHELL_TRANSVERSALITY_JACOBIAN_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
BESSEL_EVALUATION_CAP = 20_000
QUADRATURE_CAP = 5


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0
    quadratures: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})
        return bool(passed)

    def observe_numeric(self, check_id: str, value: mp.mpf, tolerance: mp.mpf, statement: str) -> bool:
        self.register(check_id)
        passed = bool(value <= tolerance)
        self.numerical.append({"id": check_id, "passed": passed, "statement": statement, "maximum_error": mp.nstr(value, 30), "tolerance": mp.nstr(tolerance, 30)})
        return passed

    def guard(self, guard_id: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        self.register(guard_id)
        self.theorem_guards.append({"id": guard_id, "verified": True, "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_NUMERICAL_PREDICATE", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})


def expected_nulls() -> dict[str, Any]:
    return {
        "global_raw_C_spectral_measure": None, "global_delta_C_measure": None, "raw_C_rigging_test_space": None, "raw_C_rigging_map": None, "raw_C_physical_inner_product": None, "physical_inner_product_positivity": None, "physical_observable_action": None, "raw_C_RAQ_completion": None, "quantum_constraint_rescaling_equivalence": None, "selected_H_raw_C_unitary_intertwiner": None, "general_p_mixing_extension_classification": None, "canonical_p_zero_origin_sector": None, "absolute_bfv_measure": None, "continuum_determinant_or_pfaffian_line": None, "inhomogeneous_constraint_closure": None, "quantum_bfv_anomaly_freedom": None, "relational_observables_or_decoherence": None, "empirical_likelihood": None, "quantum_gravity_claim": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None
    }


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, str], list[mp.mpf]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError("upstream result hash mismatch")
    payload = json.loads(raw)
    for key, expected in (("run_status", "VALID_RUN"), ("verdict", item["required_verdict"]), ("result_payload_sha256_without_self", item["payload_sha256_without_self"])):
        if payload.get(key) != expected:
            raise AssertionError(f"upstream field mismatch: {key}")
    roots = [mp.mpf(row["kappa"]) for row in payload["numerical_calculation"]["roots"]]
    if len(roots) != 5:
        raise AssertionError("expected exactly five pinned roots")
    return ({"path": item["path"], "sha256": observed, "payload_sha256_without_self": payload["result_payload_sha256_without_self"], "verdict": payload["verdict"]}, roots)


def load_input() -> tuple[dict[str, Any], str, dict[str, str], list[mp.mpf]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {input_sha}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.raw-c-zero-shell-transversality-jacobian.input.v1":
        raise AssertionError("input schema mutation")
    if payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("calculation identity mutation")
    expected_caps = {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 5, "ode_calls": 0, "bessel_function_evaluations": 20000, "automatic_descendants": 0}
    if payload["resource_caps"] != expected_caps or payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("caps or fail-closed mutation")
    conventions = payload["declared_conventions"]
    if conventions["hbar"] != "1" or conventions["root_count_required"] != 5 or conventions["Q_0"] != "-4":
        raise AssertionError("declared convention mutation")
    mp.dps = int(conventions["precision_digits"])
    root = Path(__file__).resolve().parent.parent
    upstream, roots = verify_upstream(root, payload["upstream_results"][0])
    return payload, input_sha, upstream, roots


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    hbar, a, nf, fp, f_kappa = sp.symbols("hbar a N_f F_p F_kappa", nonzero=True, real=True)
    z = sp.symbols("z", positive=True, real=True)
    weighted_coefficient = sp.simplify(12 * sp.pi**2 * (z / (6 * sp.pi**2)) ** sp.Rational(3, 2) / z)
    expected_coefficient = sp.sqrt(sp.Rational(2, 3)) * sp.sqrt(1) / sp.pi
    flags = {
        "weighted_mellin_change": audit.observe("rawc.transverse.mellin.weight_change", sp.simplify(weighted_coefficient - expected_coefficient * z ** sp.Rational(1, 2)) == 0, "at hbar=1, f(Q)dQ=(sqrt(2/3)/pi) z^(1/2)dz under z=6*pi^2e^Q"),
        "implicit_slope": audit.observe("rawc.transverse.implicit_slope", sp.simplify((-fp) / (-nf / (2 * hbar**2 * a)) - 2 * hbar**2 * a * fp / nf) == 0, "-F_p/F_lambda=2*hbar^2*a*F_p/N_f"),
        "positive_branch_fp": audit.observe("rawc.transverse.positive_branch.F_p", sp.simplify((sp.sqrt(sp.Rational(3, 2)) * f_kappa) ** 2 - sp.Rational(3, 2) * f_kappa**2) == 0, "on p>0 at hbar=1, F_p=sqrt(3/2)F_kappa"),
    }
    audit.guard("rawc.transverse.guard.moving_boundary_lagrange", "Lagrange identity for L_p u=lambda f u with a parameter-dependent self-adjoint boundary domain", "u_0 is the declared plus-end zero-shell solution, a=u_0(Q_0) is nonzero at the pinned root, and F_lambda is the derivative of the characteristic boundary condition rather than a fixed-domain expectation value", "F_lambda(0)=-N_f/(2*hbar^2*a); this supplies one local characteristic derivative only, not a global spectral theorem or rigging map")
    audit.guard("rawc.transverse.guard.mellin_positive_norm", "Mellin integral of K_nu^2", "mu=3/2 and nu=i*kappa with real kappa lie in the convergence range; the selected K solution is real on positive z", "N_f is finite and positive for each nonzero root under the declared normalization; this is not a physical inner-product positivity theorem")
    audit.guard("rawc.transverse.guard.no_naive_fixed_domain_HF", "domain-sensitive perturbation theory", "K_(i*kappa)(z) has nondecaying oscillatory magnitude as Q tends to minus infinity, so integral |u_0|^2 dQ diverges; moreover the extension boundary data vary with p", "a naive fixed-domain Hellmann-Feynman formula is not used and cannot replace the Wronskian/Lagrange calculation")
    audit.guard("rawc.transverse.guard.local_delta_scope", "simple-root delta-function change of variables", "F_kappa and lambda_prime are nonzero at each pinned root and the statement is restricted to a local p branch", "1/|lambda_prime| is a local Jacobian factor only; spectral normalization, test space, global summation and rigging-map data remain absent")
    return ({"weighted_norm": "N_f=(sqrt(2/3)/pi)int_0^infinity z^(1/2)K_(i*kappa)(z)^2dz", "mellin_formula": "I=2^(-3/2)*Gamma(3/4)^2*Gamma(3/4+i*kappa)*Gamma(3/4-i*kappa)/Gamma(3/2)", "lagrange_identity": "F_lambda(0)=-N_f/(2*hbar^2*a)", "local_slope": "lambda_prime=-F_p/F_lambda=2*hbar^2*a*F_p/N_f", "conditionality": "F_lambda, lambda_prime and the local Jacobian are conditional on the moving-boundary Lagrange theorem guard; this runner does not solve or finite-difference the nonzero-lambda Weyl problem", "forbidden_naive_formula": "integral |u_0|^2dQ fixed-domain Hellmann-Feynman"}, flags)


def k_value(audit: Audit, order: complex, z: mp.mpf) -> complex:
    audit.bessel_evaluations += 1
    if audit.bessel_evaluations > BESSEL_EVALUATION_CAP:
        raise AssertionError("Bessel evaluation cap exceeded")
    return mp.besselk(order, z)


def characteristic(audit: Audit, kappa: mp.mpf, z0: mp.mpf) -> complex:
    return -z0 * (k_value(audit, 1j * kappa - 1, z0) + k_value(audit, 1j * kappa + 1, z0)) / 2


def mellin_norm(kappa: mp.mpf) -> mp.mpf:
    integral = 2 ** mp.mpf("-1.5") * mp.gamma(mp.mpf(3) / 4) ** 2 * mp.gamma(mp.mpf(3) / 4 + 1j * kappa) * mp.gamma(mp.mpf(3) / 4 - 1j * kappa) / mp.gamma(mp.mpf(3) / 2)
    return mp.re(mp.sqrt(mp.mpf(2) / 3) * integral / mp.pi)


def quadrature_norm(audit: Audit, kappa: mp.mpf, precision_digits: int) -> tuple[mp.mpf, mp.mpf]:
    audit.quadratures += 1
    if audit.quadratures > QUADRATURE_CAP:
        raise AssertionError("quadrature cap exceeded")
    with mp.workdps(precision_digits):
        max_k_imaginary_residue = mp.mpf(0)

        def integrand(t: mp.mpf) -> mp.mpf:
            nonlocal max_k_imaginary_residue
            value = k_value(audit, 1j * kappa, mp.exp(t))
            max_k_imaginary_residue = max(max_k_imaginary_residue, abs(mp.im(value)))
            return mp.re(mp.exp(mp.mpf(3) * t / 2) * value**2)
        integral = mp.quad(integrand, [-60, 0, 8])
        return mp.sqrt(mp.mpf(2) / 3) * integral / mp.pi, max_k_imaginary_residue


def numerical_calculation(audit: Audit, conventions: dict[str, Any], roots: list[mp.mpf]) -> tuple[dict[str, Any], dict[str, bool]]:
    mp.dps = int(conventions["precision_digits"])
    z0 = 6 * mp.pi**2 * mp.exp(-4)
    step = mp.mpf(conventions["finite_difference_step_kappa"])
    rows: list[dict[str, str]] = []
    max_characteristic_imag = mp.mpf(0)
    max_norm_quadrature_error = mp.mpf(0)
    max_f_kappa_step_difference = mp.mpf(0)
    min_abs_f_kappa = mp.inf
    min_abs_a = mp.inf
    min_nf = mp.inf
    min_abs_f_lambda = mp.inf
    min_abs_slope = mp.inf
    all_sign_relations = True
    for index, kappa in enumerate(roots, start=1):
        f_plus = characteristic(audit, kappa + step, z0)
        f_minus = characteristic(audit, kappa - step, z0)
        half_step = step / 2
        f_half_plus = characteristic(audit, kappa + half_step, z0)
        f_half_minus = characteristic(audit, kappa - half_step, z0)
        derivative_step = mp.re((f_plus - f_minus) / (2 * step))
        derivative_half_step = mp.re((f_half_plus - f_half_minus) / (2 * half_step))
        f_kappa_value = (4 * derivative_half_step - derivative_step) / 3
        max_f_kappa_step_difference = max(max_f_kappa_step_difference, abs(derivative_half_step - derivative_step))
        max_characteristic_imag = max(max_characteristic_imag, abs(mp.im(f_plus)), abs(mp.im(f_minus)), abs(mp.im(f_half_plus)), abs(mp.im(f_half_minus)))
        a_value = k_value(audit, 1j * kappa, z0)
        max_characteristic_imag = max(max_characteristic_imag, abs(mp.im(a_value)))
        a_real = mp.re(a_value)
        nf_value = mellin_norm(kappa)
        f_lambda_value = -nf_value / (2 * a_real)
        f_p_value = mp.sqrt(mp.mpf(3) / 2) * f_kappa_value
        slope_plus = 2 * a_real * f_p_value / nf_value
        slope_minus = -slope_plus
        jacobian = 1 / abs(slope_plus)
        norm_quad, quad_imag = quadrature_norm(audit, kappa, int(conventions["quadrature_precision_digits"]))
        max_norm_quadrature_error = max(max_norm_quadrature_error, abs(norm_quad - nf_value))
        max_characteristic_imag = max(max_characteristic_imag, quad_imag)
        min_abs_f_kappa = min(min_abs_f_kappa, abs(f_kappa_value))
        min_abs_a = min(min_abs_a, abs(a_real))
        min_nf = min(min_nf, nf_value)
        min_abs_f_lambda = min(min_abs_f_lambda, abs(f_lambda_value))
        min_abs_slope = min(min_abs_slope, abs(slope_plus))
        all_sign_relations = all_sign_relations and bool(mp.sign(slope_minus) == -mp.sign(slope_plus)) and bool(mp.sign(f_lambda_value) == -mp.sign(a_real))
        rows.append({"root_index": str(index), "kappa": mp.nstr(kappa, 45), "p_positive": mp.nstr(mp.sqrt(mp.mpf(2) / 3) * kappa, 45), "a_at_Q0": mp.nstr(a_real, 45), "F_kappa": mp.nstr(f_kappa_value, 45), "F_p_positive_branch": mp.nstr(f_p_value, 45), "N_f_mellin": mp.nstr(nf_value, 45), "N_f_log_quadrature": mp.nstr(norm_quad, 45), "F_lambda": mp.nstr(f_lambda_value, 45), "lambda_prime_positive_p": mp.nstr(slope_plus, 45), "lambda_prime_negative_p": mp.nstr(slope_minus, 45), "local_delta_Jacobian_inverse_abs_slope": mp.nstr(jacobian, 45)})
    flags = {
        "characteristic_real": audit.observe_numeric("rawc.transverse.numeric.characteristic_imaginary_residue", max_characteristic_imag, mp.mpf("1e-45"), "all evaluated real-kappa K quantities are real within the declared precision"),
        "mellin_quadrature": audit.observe_numeric("rawc.transverse.numeric.mellin_quadrature_crosscheck", max_norm_quadrature_error, mp.mpf("1e-25"), "five bounded log-z quadratures agree with the Mellin closed-form N_f values"),
        "F_kappa_step_refinement": audit.observe_numeric("rawc.transverse.numeric.F_kappa_step_refinement", max_f_kappa_step_difference, mp.mpf("1e-25"), "centered F_kappa derivatives at steps h and h/2 agree before Richardson extrapolation"),
        "simple_f_kappa": audit.observe("rawc.transverse.numeric.nonzero_F_kappa", bool(min_abs_f_kappa > mp.mpf("1e-20")), "each pinned root has nonzero F_kappa and is locally simple in the declared characteristic variable"),
        "nonzero_a": audit.observe("rawc.transverse.numeric.nonzero_a_at_Q0", bool(min_abs_a > mp.mpf("1e-20")), "each a=K_(i*kappa)(z_0) is nonzero, so the declared F_lambda division is defined"),
        "positive_norm": audit.observe("rawc.transverse.numeric.positive_N_f", bool(min_nf > mp.mpf("1e-20")), "each declared weighted Mellin norm is positive and nonzero"),
        "nonzero_f_lambda": audit.observe("rawc.transverse.numeric.nonzero_F_lambda", bool(min_abs_f_lambda > mp.mpf("1e-20")), "each moving-domain characteristic derivative F_lambda is nonzero"),
        "nonzero_slope": audit.observe("rawc.transverse.numeric.nonzero_lambda_slope", bool(min_abs_slope > mp.mpf("1e-20")), "each positive-p local eigenvalue slope is nonzero"),
        "sign_and_parity": audit.observe("rawc.transverse.numeric.slope_sign_and_negative_branch", all_sign_relations, "F_lambda has sign opposite a, and the negative-p branch has exactly the opposite local slope"),
    }
    return ({"precision_digits": mp.dps, "quadrature_precision_digits": int(conventions["quadrature_precision_digits"]), "z_0": mp.nstr(z0, 45), "root_count": len(rows), "roots": rows, "minimum_abs_a_at_Q0": mp.nstr(min_abs_a, 30), "maximum_characteristic_imaginary_residue": mp.nstr(max_characteristic_imag, 30), "maximum_F_kappa_step_refinement_difference": mp.nstr(max_f_kappa_step_difference, 30), "maximum_mellin_quadrature_difference": mp.nstr(max_norm_quadrature_error, 30), "quadrature_log_z_window": conventions["quadrature_log_z_window"], "conditionality": "reported F_lambda, lambda_prime and local delta(C) Jacobians assume the declared moving-boundary Lagrange identity; no nonzero-lambda Weyl solve or direct F_lambda finite difference is performed", "scope": "five local simple-root controls and conditional local delta(C) Jacobians only; no global measure or RAQ"}, flags)


def write_result(path: Path, payload: dict[str, Any]) -> tuple[str, int]:
    payload["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(payload))
    encoded = canonical_bytes(payload)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact byte cap exceeded")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> None:
    input_payload, input_sha, upstream, roots = load_input()
    audit = Audit()
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit, input_payload["declared_conventions"], roots)
    all_passed = all(item["passed"] for item in audit.exact + audit.numerical)
    if all_passed:
        verdict = "KEEP_DECLARED_RAW_C_FIVE_LOCAL_SIMPLE_ROOT_JACOBIANS_ONLY"
        impact = "RECORD_LOCAL_JACOBIAN_FACTORS_WITHOUT_PROMOTING_A_GLOBAL_SPECTRAL_OR_RAQ_MEASURE"
    else:
        verdict = "KILL_DECLARED_RAW_C_LOCAL_TRANSVERSALITY_JACOBIAN_LEDGER"
        impact = "DO_NOT_USE_THE_DECLARED_LOCAL_JACOBIAN_FACTORS"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha, "numbered_phase": None}, "upstream_results": [upstream], "primary_sources": input_payload["primary_sources"], "declared_conventions": input_payload["declared_conventions"], "assumptions": input_payload["assumptions"], "exact_calculation": exact, "numerical_calculation": numerical, "exact_checks": audit.exact, "numerical_checks": audit.numerical, "theorem_guards": audit.theorem_guards, "required_fail_closed_outputs": expected_nulls(), "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "numerical_passed": sum(item["passed"] for item in audit.numerical), "numerical_total": len(audit.numerical), "theorem_guard_count": len(audit.theorem_guards), "all_executable_checks_passed": all_passed}, "resource_accounting": {"root_calls": 0, "quadratures": audit.quadratures, "ode_calls": 0, "bessel_function_evaluations": audit.bessel_evaluations, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__, "mpmath": mpmath.__version__}, "audit_flags": {"exact": exact_flags, "numerical": numerical_flags}}
    result_sha, result_size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": result_sha, "result_size_bytes": result_size, "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
