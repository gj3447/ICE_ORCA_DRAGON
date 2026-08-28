#!/usr/bin/env python3
"""Bounded zero-shell characteristic census for declared raw-C Gamma_1=0.

For the already declared weighted raw-C differential expression and the
declared reference line Gamma_1,p=0, the plus-end L2 zero-energy solution is
K_(i*kappa)(z).  This runner fixes a finite kappa window and counts only
sign-changing grid brackets of z*d_z K_(i*kappa)(z)=0.  The result is neither
a spectral measure nor a group average, rigging map, physical inner product,
or C/H equivalence calculation.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath
from mpmath import mp
import sympy as sp


INPUT_NAME = "RAW_C_ZERO_SHELL_CHARACTERISTIC_CENSUS_INPUTS.json"
RESULT_NAME = "RAW_C_ZERO_SHELL_CHARACTERISTIC_CENSUS_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_zero_shell_characteristic_census.py"
EXPECTED_INPUT_SHA256 = "66d31a7238c5fec69ab62530829ed71923d5e4de6b3aef34f0d222a827f49ed2"
CALCULATION_ID = "RawCZeroShellCharacteristicCensus"
RESULT_SCHEMA = "ice.raw-c-zero-shell-characteristic-census.result.v1"
RESULT_PREFIX = "RAW_C_ZERO_SHELL_CHARACTERISTIC_CENSUS_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0
    root_calls: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})
        return bool(passed)

    def observe_numeric(
        self, check_id: str, value: mp.mpf, tolerance: mp.mpf, statement: str
    ) -> bool:
        self.register(check_id)
        passed = bool(value <= tolerance)
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "maximum_error": mp.nstr(value, 30),
                "tolerance": mp.nstr(tolerance, 30),
            }
        )
        return passed

    def guard(
        self, guard_id: str, theorem: str, hypotheses: str, conclusion_and_scope: str
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_NUMERICAL_PREDICATE",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def expected_nulls() -> dict[str, Any]:
    return {
        "raw_C_spectral_measure": None,
        "delta_C_derivative_weights": None,
        "zero_shell_eigenvalue_branch_transversality": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "general_p_mixing_extension_classification": None,
        "canonical_p_zero_origin_sector": None,
        "absolute_bfv_measure": None,
        "continuum_determinant_or_pfaffian_line": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_json_hash(root: Path, item: dict[str, str], require_result: bool) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"pinned source hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if require_result:
        for key, expected in (
            ("run_status", "VALID_RUN"),
            ("verdict", item["required_verdict"]),
            ("result_payload_sha256_without_self", item["payload_sha256_without_self"]),
        ):
            if payload.get(key) != expected:
                raise AssertionError(f"upstream result field mismatch: {key}")
    return {"path": item["path"], "sha256": observed}


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]], list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {input_sha}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.raw-c-zero-shell-characteristic-census.input.v1":
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("calculation identity mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 32,
        "quadratures": 0,
        "ode_calls": 0,
        "bessel_function_evaluations": 20000,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    conventions = payload["declared_conventions"]
    if (
        conventions["Q_0"] != "-4"
        or conventions["kappa_window"] != "[0,8]"
        or conventions["grid_segments"] != 2048
        or conventions["root_refinement_bisection_steps"] != 160
        or conventions["root_cap"] != 32
    ):
        raise AssertionError("census convention mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_json_hash(root, item, True) for item in payload["upstream_results"]]
    repository_sources = [verify_json_hash(root, item, False) for item in payload["repository_sources"]]
    return payload, input_sha, upstream, repository_sources


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    z, kappa = sp.symbols("z kappa", positive=True, real=True)
    K, K_z, c, c_q = sp.symbols("K K_z c c_q", real=True)
    gamma_one = -((K * c_q) - (z * K_z) * c)
    flags = {
        "boundary_reduction": audit.observe(
            "rawc.zero_shell.boundary.gamma1_of_K",
            sp.simplify(gamma_one.subs({c: 1, c_q: 0}) - z * K_z) == 0,
            "W(K,c_p)=K*c_p'-partial_Q(K)*c_p=-partial_Q(K) at Q_0, hence Gamma_1(K)=-W(K,c_p)=partial_Q K=z*partial_z K because c_p=1 and c_p'=0",
        ),
        "kappa_p_parity": audit.observe(
            "rawc.zero_shell.kappa.abs_p_parity",
            sp.simplify((sp.sqrt(sp.Rational(3, 2)) * sp.Abs(-sp.Symbol("p", real=True))) - (sp.sqrt(sp.Rational(3, 2)) * sp.Abs(sp.Symbol("p", real=True)))) == 0,
            "kappa=sqrt(3/2)*abs(p) is exactly invariant under p -> -p at hbar=1",
        ),
    }
    audit.guard(
        "rawc.zero_shell.guard.derivative_recurrence",
        "modified-Bessel K derivative recurrence",
        "z is positive and the order is i*kappa with real kappa; the same analytic K branch is used for all three orders",
        "z*d_z K_(i*kappa)(z)=-(z/2)[K_(i*kappa-1)(z)+K_(i*kappa+1)(z)]; the numerical census independently checks this recurrence against a centered z derivative",
    )
    audit.guard(
        "rawc.zero_shell.guard.wronskian_transport_to_Q0",
        "Wronskian conservation for two solutions of the same zero-energy equation without a first-derivative term",
        "K_(i*kappa)(z(Q)) and c_p(Q) solve the pinned zero-energy fiber equation, and c_p(Q0)=1, c_p'(Q0)=0",
        "the endpoint Wronskian boundary value may be evaluated at Q0, giving Gamma_1,p(K)=partial_Q K there; this does not identify a literal endpoint value of either solution",
    )
    audit.guard(
        "rawc.zero_shell.guard.plus_end_L2_solution",
        "modified-Bessel large-positive-z asymptotics plus inherited limit-point classification",
        "the pinned raw-C audit identifies the plus endpoint as limit-point and the zero-energy Bessel reduction has K_(i*kappa)(z) decaying while I_(i*kappa)(z) grows for positive z",
        "K_(i*kappa) is the unique plus-end L2 zero-energy solution up to scale in this declared fiber; this does not provide a full spectral resolution at nonzero spectral parameter",
    )
    audit.guard(
        "rawc.zero_shell.guard.p_zero_exclusion",
        "K_0'(z)=-K_1(z) and positivity of K_1 on positive real z",
        "z_0>0 and the characteristic convention is F(0)=z_0*K_0'(z_0)",
        "F(0)=-z_0*K_1(z_0)<0, so p=0 is not a root of this zero-shell boundary condition; no p=0 atom or sector conclusion follows",
    )
    audit.guard(
        "rawc.zero_shell.guard.finite_grid_scope",
        "sign-change bisection for a continuous real special-function boundary value",
        "the reported window, precision, grid, bisection count and root cap remain fixed; real F values are checked by their numerical imaginary residues",
        "the output is a census of sign-changing adjacent-grid brackets only. It does not rule out even-multiplicity, tangential, or sub-grid roots and is not a spectral measure",
    )
    return (
        {
            "zero_energy_variable": "z=6*pi^2*exp(Q)/hbar",
            "kappa": "sqrt(3/2)*abs(p)/hbar",
            "plus_end_L2_solution": "K_(i*kappa)(z)",
            "boundary_reduction": "W(K,c_p)=K*c_p'-partial_Q(K)*c_p=-partial_Q(K) at Q0; Gamma_1,p(K)=-W(K,c_p)=partial_Q K=z*partial_z K at Q0=-4",
            "characteristic_function": "F(kappa)=-(z0/2)[K_(i*kappa-1)(z0)+K_(i*kappa+1)(z0)]",
            "p_zero": "F(0)=-z0*K_1(z0)<0",
            "scope": "finite sign-changing root census only",
        },
        flags,
    )


def characteristic(audit: Audit, kappa: mp.mpf, z0: mp.mpf, cap: int) -> tuple[mp.mpf, mp.mpf]:
    audit.bessel_evaluations += 2
    if audit.bessel_evaluations > cap:
        raise AssertionError("Bessel evaluation cap exceeded")
    order = 1j * kappa
    value = -z0 * (mp.besselk(order - 1, z0) + mp.besselk(order + 1, z0)) / 2
    return mp.re(value), abs(mp.im(value))


def independent_centered_derivative(audit: Audit, kappa: mp.mpf, z0: mp.mpf, cap: int) -> tuple[mp.mpf, mp.mpf]:
    step = mp.mpf("1e-18")
    audit.bessel_evaluations += 2
    if audit.bessel_evaluations > cap:
        raise AssertionError("Bessel evaluation cap exceeded")
    order = 1j * kappa
    positive = mp.besselk(order, z0 + step)
    negative = mp.besselk(order, z0 - step)
    derivative = z0 * (positive - negative) / (2 * step)
    return mp.re(derivative), abs(mp.im(derivative))


def numerical_calculation(audit: Audit, conventions: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bool]]:
    mp.dps = conventions["precision_digits"]
    z0 = 6 * mp.pi**2 * mp.exp(-4)
    segments = int(conventions["grid_segments"])
    steps = int(conventions["root_refinement_bisection_steps"])
    root_cap = int(conventions["root_cap"])
    bessel_cap = 20000
    lower, upper = mp.mpf(0), mp.mpf(8)
    spacing = (upper - lower) / segments
    grid: list[tuple[mp.mpf, mp.mpf, mp.mpf]] = []
    for index in range(segments + 1):
        kappa = lower + index * spacing
        value, imag = characteristic(audit, kappa, z0, bessel_cap)
        grid.append((kappa, value, imag))
    brackets: list[tuple[mp.mpf, mp.mpf]] = []
    for (left, left_value, _), (right, right_value, _) in zip(grid, grid[1:]):
        if left_value == 0:
            brackets.append((left, left))
        elif left_value * right_value < 0:
            brackets.append((left, right))
    if grid[-1][1] == 0:
        brackets.append((upper, upper))
    if len(brackets) > root_cap:
        raise AssertionError("root cap exceeded")
    roots: list[dict[str, str]] = []
    max_bracket_width = mp.mpf(0)
    max_root_residual = mp.mpf(0)
    max_imaginary_residue = max(item[2] for item in grid)
    max_independent_derivative_error = mp.mpf(0)
    max_independent_imaginary_residue = mp.mpf(0)
    for left, right in brackets:
        audit.root_calls += 1
        if audit.root_calls > root_cap:
            raise AssertionError("root call cap exceeded")
        initial_left, initial_right = left, right
        left_value, _ = characteristic(audit, left, z0, bessel_cap)
        right_value, _ = characteristic(audit, right, z0, bessel_cap)
        if left != right:
            for _ in range(steps):
                middle = (left + right) / 2
                middle_value, middle_imag = characteristic(audit, middle, z0, bessel_cap)
                max_imaginary_residue = max(max_imaginary_residue, middle_imag)
                if middle_value == 0:
                    left = right = middle
                    break
                if left_value * middle_value < 0:
                    right, right_value = middle, middle_value
                else:
                    left, left_value = middle, middle_value
        root = (left + right) / 2
        recurrence_value, recurrence_imag = characteristic(audit, root, z0, bessel_cap)
        derivative_value, derivative_imag = independent_centered_derivative(audit, root, z0, bessel_cap)
        width = right - left
        max_bracket_width = max(max_bracket_width, width)
        max_root_residual = max(max_root_residual, abs(recurrence_value))
        max_imaginary_residue = max(max_imaginary_residue, recurrence_imag)
        max_independent_imaginary_residue = max(max_independent_imaginary_residue, derivative_imag)
        max_independent_derivative_error = max(max_independent_derivative_error, abs(recurrence_value - derivative_value))
        roots.append(
            {
                "kappa": mp.nstr(root, 45),
                "abs_p_at_hbar_one": mp.nstr(mp.sqrt(mp.mpf(2) / 3) * root, 45),
                "p_branches": "plus_or_minus_abs_p",
                "initial_bracket_left": mp.nstr(initial_left, 45),
                "initial_bracket_right": mp.nstr(initial_right, 45),
                "final_bracket_left": mp.nstr(left, 45),
                "final_bracket_right": mp.nstr(right, 45),
                "final_bracket_width": mp.nstr(width, 20),
                "recurrence_residual": mp.nstr(abs(recurrence_value), 20),
                "centered_derivative_difference": mp.nstr(abs(recurrence_value - derivative_value), 20),
            }
        )
    p_zero_value = -z0 * mp.besselk(1, z0)
    audit.bessel_evaluations += 1
    if audit.bessel_evaluations > bessel_cap:
        raise AssertionError("Bessel evaluation cap exceeded")
    ordered = all(mp.mpf(roots[index]["kappa"]) < mp.mpf(roots[index + 1]["kappa"]) for index in range(len(roots) - 1))
    separated = all(
        mp.mpf(roots[index + 1]["kappa"]) - mp.mpf(roots[index]["kappa"]) > 2 * max_bracket_width
        for index in range(len(roots) - 1)
    )
    flags = {
        "p_zero_negative": audit.observe(
            "rawc.zero_shell.numeric.p_zero_negative_value",
            bool(p_zero_value < 0),
            "F(0) is strictly negative in the declared positive-z convention",
        ),
        "root_residual": audit.observe_numeric(
            "rawc.zero_shell.numeric.root_recurrence_residual",
            max_root_residual,
            mp.mpf("1e-38"),
            "each reported root has small recurrence-characteristic residual",
        ),
        "independent_derivative": audit.observe_numeric(
            "rawc.zero_shell.numeric.root_independent_centered_derivative",
            max_independent_derivative_error,
            mp.mpf("1e-28"),
            "the recurrence characteristic agrees with an independent centered z derivative at every reported root",
        ),
        "bracket_width": audit.observe_numeric(
            "rawc.zero_shell.numeric.root_bracket_width",
            max_bracket_width,
            mp.mpf("1e-45"),
            "every refined sign-changing root bracket is below the fixed width threshold",
        ),
        "imaginary_residue": audit.observe_numeric(
            "rawc.zero_shell.numeric.real_characteristic_residue",
            max(max_imaginary_residue, max_independent_imaginary_residue),
            mp.mpf("1e-50"),
            "the real-kappa, positive-z characteristic and independent derivative are real within the declared precision",
        ),
        "ordering_and_separation": audit.observe(
            "rawc.zero_shell.numeric.root_ordering_and_separation",
            ordered and separated,
            "reported roots are strictly ordered and their centers are separated by more than twice the maximum refined bracket width",
        ),
    }
    return (
        {
            "precision_digits": mp.dps,
            "z_0": mp.nstr(z0, 45),
            "kappa_window": ["0", "8"],
            "grid_segments": segments,
            "root_refinement_bisection_steps": steps,
            "root_definition": conventions["root_definition"],
            "sign_change_bracket_count": len(brackets),
            "root_count": len(roots),
            "roots": roots,
            "p_zero_characteristic_value": mp.nstr(p_zero_value, 45),
            "maximum_root_residual": mp.nstr(max_root_residual, 30),
            "maximum_independent_derivative_difference": mp.nstr(max_independent_derivative_error, 30),
            "maximum_final_bracket_width": mp.nstr(max_bracket_width, 30),
            "maximum_imaginary_residue": mp.nstr(max(max_imaginary_residue, max_independent_imaginary_residue), 30),
            "bessel_function_evaluations": audit.bessel_evaluations,
            "root_calls": audit.root_calls,
            "scope": "fixed finite-window sign-changing grid census only; no claim about missed tangencies, sub-grid roots, spectral weights, or RAQ",
        },
        flags,
    )


def write_result(path: Path, payload: dict[str, Any]) -> tuple[str, int]:
    payload["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(payload))
    encoded = canonical_bytes(payload)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact byte cap exceeded")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> None:
    input_payload, input_sha, upstream, repository_sources = load_input()
    audit = Audit()
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit, input_payload["declared_conventions"])
    all_passed = all(item["passed"] for item in audit.exact + audit.numerical)
    if all_passed:
        verdict = "CENSUS_DECLARED_RAW_C_ZERO_SHELL_SIGN_CHANGING_CHARACTERISTIC_ROOTS_ONLY"
        impact = "KEEP_FINITE_CHARACTERISTIC_CENSUS_WITHOUT_PROMOTING_SPECTRAL_OR_RAQ_DATA"
    else:
        verdict = "KILL_RAW_C_ZERO_SHELL_CHARACTERISTIC_CENSUS"
        impact = "RETAIN_THE_DECLARED_BOUNDARY_LINE_BUT_DO_NOT_USE_THIS_NUMERICAL_CENSUS"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha, "numbered_phase": None},
        "upstream_results": upstream,
        "repository_sources": repository_sources,
        "primary_sources": input_payload["primary_sources"],
        "declared_conventions": input_payload["declared_conventions"],
        "assumptions": input_payload["assumptions"],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": sum(item["passed"] for item in audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guard_count": len(audit.theorem_guards),
            "all_executable_checks_passed": all_passed,
        },
        "resource_accounting": {"root_calls": audit.root_calls, "quadratures": 0, "ode_calls": 0, "bessel_function_evaluations": audit.bessel_evaluations, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__, "mpmath": mpmath.__version__},
        "audit_flags": {"exact": exact_flags, "numerical": numerical_flags},
    }
    result_sha, result_size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "root_count": numerical["root_count"], "result_sha256": result_sha, "result_size_bytes": result_size, "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
