#!/usr/bin/env python3
"""Finite BFV calibration: parametrized free particle, normalization and gluing.

The model has C=p_t+p_x^2/(2m), chi=t-tau, and one affine gauge orbit.  The
calculation fixes a complete finite convention set: full-real-lapse constraint
distribution, x-polarized endpoints, ordered two-ghost Pfaffian orientation,
the +i0 Fresnel branch, and two-slab composition.  It is a toy calibration
only.  Nothing here supplies an absolute BFV measure for gravity or
minisuperspace, a continuum determinant line, or a physical claim.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "BFV_PARAMETRIZED_PARTICLE_GLUING_CALIBRATION_INPUTS.json"
RESULT_NAME = "BFV_PARAMETRIZED_PARTICLE_GLUING_CALIBRATION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/bfv_parametrized_particle_gluing_calibration.py"
EXPECTED_INPUT_SHA256 = "326c74e89eebfa2b89ee4f6e95be15346499c3ce6798fb12d7665b6d5cc80fd9"
CALCULATION_ID = "BfvParametrizedParticleGluingCalibration"
RESULT_SCHEMA = "ice.bfv-parametrized-particle-gluing-calibration.result.v1"
RESULT_PREFIX = "BFV_PARAMETRIZED_PARTICLE_GLUING_CALIBRATION_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
NUMERICAL_SAMPLE_CAP = 12


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
    numerical_samples: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})
        return bool(passed)

    def observe_numeric(
        self, check_id: str, error: float, tolerance: float, statement: str
    ) -> bool:
        self.register(check_id)
        passed = error <= tolerance
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "maximum_error": format(error, ".17g"),
                "tolerance": format(tolerance, ".17g"),
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
        "gravity_or_minisuperspace_absolute_bfv_measure": None,
        "continuum_determinant_or_pfaffian_line": None,
        "gravity_gribov_census": None,
        "gravity_lapse_contour_selection": None,
        "gravity_endpoint_polarization": None,
        "gravity_bfv_gluing_theorem": None,
        "raw_C_operator_and_domain": None,
        "raw_C_rigging_map": None,
        "quantum_constraint_rescaling_equivalence": None,
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


def load_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {input_sha}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.bfv-parametrized-particle-gluing-calibration.input.v1":
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("calculation identity mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "numerical_samples": 12,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    model = payload["declared_model"]
    if (
        model["constraint"] != "C=p_t+p_x^2/(2*m)"
        or model["gauge"] != "chi=t-tau"
        or model["faddeev_popov_bracket"] != "{chi,C}=1"
        or model["ghost_order"] != "(bar_c,c)"
        or model["ghost_orientation"] != "Pf(A_gh)=+1 in the declared order"
    ):
        raise AssertionError("declared finite model mutation")
    return payload, input_sha


def pfaffian_two_by_two(matrix: sp.Matrix) -> sp.Expr:
    if matrix.shape != (2, 2) or matrix + matrix.T != sp.zeros(2):
        raise AssertionError("expected antisymmetric two-by-two ghost block")
    return matrix[0, 1]


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    t, p_t, x, p_x, tau, epsilon = sp.symbols("t p_t x p_x tau epsilon", real=True)
    m, hbar, T_1, T_2 = sp.symbols("m hbar T_1 T_2", positive=True, real=True)
    action_coefficient, T, regulator = sp.symbols(
        "A T regulator", positive=True, real=True
    )
    lapse_parameter = sp.symbols("lambda", real=True)
    x_i, x_m, x_f = sp.symbols("x_i x_m x_f", real=True)
    constraint = p_t + p_x**2 / (2 * m)
    gauge = t - tau
    poisson = sp.diff(gauge, t) * sp.diff(constraint, p_t) - sp.diff(gauge, p_t) * sp.diff(constraint, t)
    shifted_gauge = sp.simplify((t + epsilon) - tau)
    unique_epsilon = sp.solve(sp.Eq(shifted_gauge, 0), epsilon)
    ghost_matrix = sp.Matrix([[0, 1], [-1, 0]])
    ghost_pfaffian = pfaffian_two_by_two(ghost_matrix)
    T_sum = T_1 + T_2
    quadratic_difference = sp.simplify(
        (x_f - x_m) ** 2 / T_2 + (x_m - x_i) ** 2 / T_1
        - (
            T_sum / (T_1 * T_2) * (x_m - (T_2 * x_i + T_1 * x_f) / T_sum) ** 2
            + (x_f - x_i) ** 2 / T_sum
        )
    )
    prefactor_square_difference = sp.simplify(
        (m / (2 * sp.pi * sp.I * hbar * T_1))
        * (m / (2 * sp.pi * sp.I * hbar * T_2))
        * (2 * sp.pi * sp.I * hbar * T_1 * T_2 / (m * T_sum))
        - m / (2 * sp.pi * sp.I * hbar * T_sum)
    )
    damping_log_modulus = sp.simplify(
        sp.re(sp.I * action_coefficient / (T - sp.I * regulator))
    )
    flags = {
        "fp_bracket": audit.observe(
            "bfv.particle.gauge.fp_bracket_one",
            sp.simplify(poisson - 1) == 0,
            "{t-tau,p_t+p_x^2/(2m)}=1 exactly",
        ),
        "single_intersection": audit.observe(
            "bfv.particle.gauge.single_affine_intersection",
            unique_epsilon == [tau - t],
            "the affine gauge orbit shifts chi by epsilon and reaches chi=0 at one and only one epsilon",
        ),
        "ghost_antisymmetry": audit.observe(
            "bfv.particle.ghost.ordered_block_antisymmetric",
            ghost_matrix + ghost_matrix.T == sp.zeros(2),
            "A_gh is antisymmetric in the declared (bar_c,c) order",
        ),
        "ghost_orientation": audit.observe(
            "bfv.particle.ghost.pfaffian_orientation_plus_one",
            ghost_pfaffian == 1,
            "Pf(A_gh)=+1 fixes the finite ordered ghost orientation",
        ),
        "gluing_quadratic_completion": audit.observe(
            "bfv.particle.kernel.two_slab_quadratic_completion",
            quadratic_difference == 0,
            "the two-slab phase completes to the single T_1+T_2 free-particle phase",
        ),
        "gluing_prefactor": audit.observe(
            "bfv.particle.kernel.two_slab_prefactor",
            prefactor_square_difference == 0,
            "squared Fresnel prefactors and the completed Gaussian integral equal the T_1+T_2 squared prefactor",
        ),
        "i0_damping_sign": audit.observe(
            "bfv.particle.kernel.i0_damping_sign",
            sp.simplify(
                damping_log_modulus
                + action_coefficient * regulator / (T**2 + regulator**2)
            )
            == 0,
            "for A>0 and epsilon>0, abs(exp(i*A/(T-i*epsilon)))=exp(-A*epsilon/(T^2+epsilon^2))<1",
        ),
        "clock_delta_selects_lapse": audit.observe(
            "bfv.particle.lapse.clock_delta_selects_lambda",
            sp.solve(sp.Eq(T - lapse_parameter, 0), lapse_parameter) == [T],
            "the clock kernel delta(T-lambda) has the unique lapse support lambda=T; the full-real Fourier identity remains a distribution theorem guard",
        ),
    }
    audit.guard(
        "bfv.particle.guard.affine_gribov_free_slice",
        "global affine gauge-slice argument",
        "the C flow shifts t by a free real parameter and chi=t-tau shifts with unit coefficient; the declared endpoint convention admits that full orbit",
        "this toy gauge has exactly one intersection and determinant +1; it is not a Gribov census for gravity, compact gauges, or endpoint-restricted field theory",
    )
    audit.guard(
        "bfv.particle.guard.full_real_lapse_distribution",
        "Fourier representation of the delta distribution",
        "the lapse/group parameter ranges over the full real line, with eta_C defined as the stated tempered distribution and x endpoints paired with a fixed positive clock separation",
        "the toy endpoint kernel is normalized by this declared distribution convention; eta_C is not asserted to be a bounded idempotent projector",
    )
    audit.guard(
        "bfv.particle.guard.fresnel_branch_and_gluing",
        "damped oscillatory Gaussian continuation",
        "m,hbar,T_1,T_2 are positive and each T is continued as T-i*epsilon before epsilon down to zero; all slabs use the same branch and x polarization",
        "the branch fixes the finite free kernel and its two-slab gluing. It does not determine a gravity lapse contour, Stokes data, Maslov data, or a continuum determinant line",
    )
    audit.guard(
        "bfv.particle.guard.short_time_distribution",
        "free Schrödinger kernel approximate identity",
        "the statement is tested against Schwartz functions and interpreted distributionally as T down to 0 through positive times with the declared +i0 branch",
        "K_T tends to delta(x_f-x_i) only as a distribution; no pointwise delta value or gravity endpoint contact term is claimed",
    )
    return (
        {
            "constraint": "C=p_t+p_x^2/(2*m)",
            "gauge": "chi=t-tau",
            "gauge_orbit": "t -> t+epsilon; chi -> chi+epsilon; epsilon=tau-t gives the unique slice intersection",
            "full_real_lapse_distribution": "eta_C=int_R d_lambda exp(-i*lambda*C/hbar)=2*pi*hbar*delta(C)",
            "endpoint_kernel": "K_T(x_f,x_i)=(m/(2*pi*i*hbar*(T-i0)))^(1/2)*exp(i*m*(x_f-x_i)^2/(2*hbar*(T-i0)))",
            "ghost_order_and_pfaffian": "(bar_c,c), A_gh=[[0,1],[-1,0]], Pf(A_gh)=+1",
            "two_slab_gluing": "int_R dx_m K_T2(x_f,x_m)K_T1(x_m,x_i)=K_(T1+T2)(x_f,x_i), T1,T2>0",
            "short_time_statement": "K_T -> delta(x_f-x_i) distributionally as T down to 0 through positive times",
        },
        flags,
    )


def propagated_gaussian(x: float, a: float, time: float, mass: float, hbar: float) -> complex:
    denominator = 1.0 + 2.0j * a * hbar * time / mass
    return denominator ** (-0.5) * cmath.exp(-a * x**2 / denominator)


def numerical_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    mass = 1.0
    hbar = 1.0
    a_values = [0.5, 1.0]
    time_values = [1e-5, 5e-6]
    x_values = [0.0, 0.7, 1.3]
    errors: list[float] = []
    rows: list[dict[str, str]] = []
    for a in a_values:
        for time in time_values:
            for x in x_values:
                audit.numerical_samples += 1
                if audit.numerical_samples > NUMERICAL_SAMPLE_CAP:
                    raise AssertionError("numerical sample cap exceeded")
                evolved = propagated_gaussian(x, a, time, mass, hbar)
                reference = math.exp(-a * x**2)
                error = abs(evolved - reference)
                errors.append(error)
                rows.append(
                    {
                        "a": format(a, ".6g"),
                        "T": format(time, ".6g"),
                        "x": format(x, ".6g"),
                        "absolute_error": format(error, ".17g"),
                    }
                )
    if audit.numerical_samples != NUMERICAL_SAMPLE_CAP:
        raise AssertionError("numerical sample count mutation")
    maximum_error = max(errors)
    flags = {
        "gaussian_short_time_delta": audit.observe_numeric(
            "bfv.particle.numeric.short_time_gaussian_approximate_identity",
            maximum_error,
            5e-5,
            "the declared +i0 free kernel approaches a Gaussian Schwartz test function at bounded small positive times",
        )
    }
    return (
        {
            "mass": mass,
            "hbar": hbar,
            "gaussian_a_samples": a_values,
            "positive_time_samples": time_values,
            "x_samples": x_values,
            "numerical_samples": audit.numerical_samples,
            "maximum_short_time_test_error": format(maximum_error, ".17g"),
            "rows": rows,
            "scope": "bounded Gaussian-test diagnostic of the distributional short-time normalization; no numerical lapse, ghost, or continuum determinant integration",
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
    input_payload, input_sha = load_input()
    audit = Audit()
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit)
    all_passed = all(item["passed"] for item in audit.exact + audit.numerical)
    if all_passed:
        verdict = "CALIBRATED_PARAMETRIZED_PARTICLE_FINITE_BFV_NORMALIZATION_AND_GLUE_ONLY"
        impact = "KEEP_TOY_BFV_CALIBRATION_AS_A_CONVENTION_CHECK_WITHOUT_PROMOTING_GRAVITY_ABSOLUTE_MEASURE"
    else:
        verdict = "KILL_PARAMETRIZED_PARTICLE_BFV_GLUE_CALIBRATION"
        impact = "DO_NOT_USE_THIS_TOY_NORMALIZATION_AS_A_CALIBRATION_REFERENCE"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha, "numbered_phase": None},
        "primary_sources": input_payload["primary_sources"],
        "declared_model": input_payload["declared_model"],
        "assumptions": input_payload["assumptions"],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "toy_calibration": {
            "absolute_finite_convention_normalization": "FIXED_FOR_THIS_PARAMETRIZED_PARTICLE_ONLY",
            "full_real_lapse_constraint_distribution": "eta_C=2*pi*hbar*delta(C)",
            "ordered_ghost_pfaffian_orientation": "+1",
            "fresnel_branch": "+i0",
            "x_polarized_two_slab_gluing": "EXACT_FOR_T1_T2_POSITIVE",
            "gravity_transfer": None,
        },
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": sum(item["passed"] for item in audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guard_count": len(audit.theorem_guards),
            "all_executable_checks_passed": all_passed,
        },
        "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "numerical_samples": audit.numerical_samples, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__},
        "audit_flags": {"exact": exact_flags, "numerical": numerical_flags},
    }
    result_sha, result_size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": result_sha, "result_size_bytes": result_size, "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
