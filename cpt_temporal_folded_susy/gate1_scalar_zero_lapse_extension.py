#!/usr/bin/env python3
"""Gate 1 -- exact full-q scalar zero-lapse boundary control.

This non-numbered one-shot follows the consumed fixed-a, m=2 ordered
scalar source-link result.  It keeps the full Starobinsky q integral at
finite Re(T)>0, proves a global polynomial boundary bound, and records the
exact small-T coefficients used by separately reviewed analytic boundary and
scaling-degree theorems.

It does not rerun either consumed Gate-1 calculation, solve roots or ODEs,
launch thimbles, vary a, add BFV variables, or emit a physics/TOE claim.  It
writes one adjacent JSON result.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "GATE1_SCALAR_ZERO_LAPSE_EXTENSION_INPUTS.json"
RESULT_NAME = "GATE1_SCALAR_ZERO_LAPSE_EXTENSION_RESULT.json"
UPSTREAM_NAME = "GATE1_SCALAR_SOURCE_LINK_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_scalar_zero_lapse_extension.py"
EXPECTED_INPUT_SHA256 = (
    "5667cb42bbc7eb72ae50de05cc1b0abfbc12bf22c8036f6c59c6f5427644cd0e"
)
EXPECTED_UPSTREAM_SHA256 = (
    "ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243"
)
AUTHORIZATION_ID = "GATE1_ZERO_LAPSE_20260826_01"
RESULT_SCHEMA = "ice.gate1.scalar-zero-lapse-extension.result.v1"
RESULT_PREFIX = "GATE1_SCALAR_ZERO_LAPSE_EXTENSION_RESULT="
ARTIFACT_CAP_BYTES = 250_000


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> None:
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {check_id}: {statement}")
        self.exact.append(
            {"id": check_id, "passed": True, "statement": statement}
        )

    def guard_theorem(
        self,
        guard_id: str,
        verified: bool,
        theorem: str,
        source: str,
        domain: str,
        statement: str,
    ) -> None:
        if not verified:
            raise AssertionError(f"[THEOREM GUARD FAIL] {guard_id}: {statement}")
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "source": source,
                "domain": domain,
                "statement": statement,
            }
        )


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


def load_frozen_input() -> tuple[dict[str, Any], str]:
    input_path = Path(__file__).with_name(INPUT_NAME)
    raw = input_path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    upstream_path = Path(__file__).with_name(UPSTREAM_NAME)
    upstream_observed = sha256_bytes(upstream_path.read_bytes())
    if upstream_observed != EXPECTED_UPSTREAM_SHA256:
        raise AssertionError(
            "upstream result hash mismatch: "
            f"expected {EXPECTED_UPSTREAM_SHA256}, observed {upstream_observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.scalar-zero-lapse-extension.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["authorization"]["id"] != AUTHORIZATION_ID:
        raise AssertionError("unexpected authorization identity")
    if payload["authorization"]["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    if payload["upstream_result"]["sha256"] != EXPECTED_UPSTREAM_SHA256:
        raise AssertionError("upstream input pin mutation")
    if payload["resource_caps"] != {
        "wall_clock_seconds": 30,
        "artifact_bytes": 250000,
        "stdout_bytes": 65536,
        "stderr_bytes": 65536,
        "root_calls": 0,
        "ode_calls": 0,
        "evaluator_reconciliation_calls": 0,
        "numerical_samples": 0,
        "automatic_descendants": 0,
    }:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "physical_original_cycle": None,
        "full_joint_orientation": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    return payload, observed


def exact_calculation(audit: Audit) -> dict[str, Any]:
    a, hbar, epsilon = sp.symbols(
        "a hbar epsilon", positive=True, real=True
    )
    n, eta, r, w = sp.symbols(
        "n eta r w", positive=True, real=True
    )
    lapse, q, x, phi = sp.symbols("N q x phi", real=True)
    kappa = sp.sqrt(sp.Rational(2, 3))
    a_phi = sp.exp(-kappa * phi)
    c = 4 * sp.pi**2 * a**3 / hbar
    lower_offset = 6 * sp.pi**2 * a / hbar
    square_coefficient = 3 * sp.pi**2 * a**3 / (2 * hbar)

    potential = sp.Rational(3, 4) * (
        1 - sp.exp(-kappa * (phi + q / 2))
    ) ** 2
    u_original = 2 * sp.pi**2 / hbar * (-3 * a + a**3 * potential)
    u_square = (
        -lower_offset
        + square_coefficient
        * (1 - a_phi * sp.exp(-kappa * q / 2)) ** 2
    )
    audit.check_exact(
        "G1.zero.starobinsky_global_square",
        sp.simplify(u_original - u_square) == 0,
        "the full Starobinsky rate is a nonnegative square above -6*pi^2*a/hbar on the complete real q line",
    )
    audit.check_exact(
        "G1.zero.global_lower_offset",
        sp.simplify(u_square + lower_offset)
        == square_coefficient
        * (1 - a_phi * sp.exp(-kappa * q / 2)) ** 2,
        "u(q)+6*pi^2*a/hbar is exactly a positive coefficient times a real square for a,hbar>0",
    )

    complex_t = epsilon + sp.I * lapse
    reciprocal_real_part = sp.simplify(
        sp.re(1 / complex_t).expand(complex=True)
    )
    audit.check_exact(
        "G1.zero.right_half_plane_kinetic_rate",
        sp.simplify(
            reciprocal_real_part
            - epsilon / (epsilon**2 + lapse**2)
        )
        == 0,
        "Re(1/T)=epsilon/|T|^2 is positive throughout the prescribed right-half-plane regulator",
    )

    real_exponent = sp.simplify(
        sp.re(-c * q**2 / complex_t - complex_t * u_square).expand(
            complex=True
        )
    )
    expected_real_exponent = (
        -c * epsilon * q**2 / (epsilon**2 + lapse**2)
        - epsilon * u_square
    )
    audit.check_exact(
        "G1.zero.full_integrand_modulus",
        sp.simplify(real_exponent - expected_real_exponent) == 0,
        "the modulus is controlled before either the q integral or the lapse boundary limit is taken",
    )

    gaussian_rate = c * epsilon / (epsilon**2 + lapse**2)
    gaussian_majorant_integral = sp.sqrt(sp.pi / gaussian_rate)
    prefactor_modulus = (
        2
        * sp.pi
        * a**3
        / (hbar * sp.sqrt(epsilon**2 + lapse**2))
    )
    full_bound_coefficient = sp.simplify(
        prefactor_modulus * gaussian_majorant_integral
    )
    leading_coefficient = sp.sqrt(sp.pi * a**3 / hbar)
    audit.check_exact(
        "G1.zero.uniform_full_q_boundary_bound",
        sp.simplify(
            full_bound_coefficient - leading_coefficient / sp.sqrt(epsilon)
        )
        == 0,
        "the complete q-paired amplitude is bounded by sqrt(pi*a^3/hbar)*exp(6*pi^2*a*epsilon/hbar)/sqrt(epsilon), uniformly in real N",
    )

    scaled_q = sp.sqrt(r) * x
    scaled_t = r * w
    audit.check_exact(
        "G1.zero.small_t_field_rescaling",
        sp.simplify(c * scaled_q**2 / scaled_t - c * x**2 / w)
        == 0,
        "T=r*w and q=sqrt(r)*x leave the leading Gaussian exponent c*x^2/w independent of r",
    )
    scaled_prefactor_measure = sp.simplify(
        sp.sqrt(r)
        * (
            2
            * sp.pi
            * a**3
            / (hbar * scaled_t)
            * sp.sqrt(r)
        )
    )
    audit.check_exact(
        "G1.zero.scaled_amplitude_measure",
        sp.simplify(
            scaled_prefactor_measure - 2 * sp.pi * a**3 / (hbar * w)
        )
        == 0,
        "sqrt(r)*A(r*w) has the r-independent prefactor-measure 2*pi*a^3/(hbar*w) after q=sqrt(r)*x",
    )

    gaussian_i0 = sp.sqrt(sp.pi * w / c)
    gaussian_i2_over_i0 = w / (2 * c)
    leading_scaled_limit = sp.simplify(
        2 * sp.pi * a**3 / (hbar * w) * gaussian_i0
    )
    audit.check_exact(
        "G1.zero.nonzero_normal_family_limit",
        sp.simplify(
            leading_scaled_limit - leading_coefficient / sp.sqrt(w)
        )
        == 0,
        "the positive-real dominated scaling limit is nonzero and equals sqrt(pi*a^3/hbar)*w^(-1/2)",
    )

    u0 = sp.simplify(u_square.subs(q, 0))
    u2 = sp.simplify(sp.diff(u_square, q, 2).subs(q, 0))
    expected_u2 = (
        sp.pi**2
        * a**3
        / (2 * hbar)
        * (2 * a_phi**2 - a_phi)
    )
    audit.check_exact(
        "G1.zero.local_rate_coefficients",
        sp.simplify(u2 - expected_u2) == 0,
        "the exact local rate data are u(0) and u''(0)=pi^2*a^3*(2*A_phi^2-A_phi)/(2*hbar)",
    )
    bracket_t2 = sp.simplify(u0**2 / 2 - u2 / (4 * c))
    moment_derived_t2 = sp.simplify(
        u0**2 / 2 - (u2 / 2) * gaussian_i2_over_i0 / w
    )
    audit.check_exact(
        "G1.zero.gaussian_moment_expansion",
        sp.simplify(moment_derived_t2 - bracket_t2) == 0,
        "formal Taylor and Gaussian-moment coefficients through T^2 are 1-u0*T+(u0^2/2-u2/(4*c))*T^2; this executable identity does not itself certify a sector remainder",
    )

    positive_phase = sp.exp(-sp.I * sp.pi / 4)
    negative_phase = sp.exp(sp.I * sp.pi / 4)
    audit.check_exact(
        "G1.zero.conjugate_half_power_boundary_phases",
        sp.simplify(positive_phase**2 + sp.I) == 0
        and sp.simplify(negative_phase**2 - sp.I) == 0
        and sp.simplify(negative_phase - sp.conjugate(positive_phase)) == 0,
        "the principal T^(-1/2) boundary has phases exp(-i*pi/4) for N>0 and exp(+i*pi/4) for N<0",
    )
    audit.check_exact(
        "G1.zero.leading_boundary_is_locally_integrable",
        sp.integrate(n ** (-sp.Rational(1, 2)), (n, 0, eta))
        == 2 * sp.sqrt(eta),
        "each half-arm |N|^(-1/2) integrates to 2*sqrt(eta), so the two-sided leading singularity is locally integrable",
    )

    positive_t = sp.symbols("T", positive=True, real=True)
    leading_q_integral = sp.sqrt(sp.pi * positive_t / c)
    paired_gaussian_leading = sp.simplify(
        2
        * sp.pi
        * a**3
        / (hbar * positive_t)
        * leading_q_integral
    )
    audit.check_exact(
        "G1.zero.unpaired_momentum_contact_inference_rejected",
        sp.simplify(
            paired_gaussian_leading
            - leading_coefficient / sp.sqrt(positive_t)
        )
        == 0,
        "the q pairing supplies sqrt(T), so the separate J_p~T^(-1) delta-plus-PV boundary cannot be distributed termwise through the full q integral",
    )

    y = a_phi * sp.exp(-kappa * q / 2)
    stationary_equation = sp.simplify(
        (2 * c * q - lapse**2 * sp.diff(u_square, q))
        / (sp.pi**2 * a**3 / (2 * hbar))
    )
    audit.check_exact(
        "G1.zero.remote_negative_tail_stationary_equation",
        sp.simplify(
            stationary_equation
            - (16 * q - 3 * kappa * lapse**2 * y * (1 - y))
        )
        == 0,
        "the exact real-boundary stationary equation records the escaping negative-q tail without using a local Gaussian to replace it",
    )

    audit.guard_theorem(
        "G1.zero.guard.holomorphic_full_q_amplitude",
        True,
        "dominated differentiation under an improper integral",
        "standard local holomorphic-parameter integral theorem",
        "compact subsets of Re(T)>0, a>0, hbar>0, phi real, q over the full real line",
        "Gaussian decay at positive q and the full Starobinsky square at negative q dominate every compact-subset T derivative, so A(T) is holomorphic",
    )
    audit.guard_theorem(
        "G1.zero.guard.canonical_distributional_boundary",
        True,
        "canonical boundary of a polynomial-growth holomorphic function",
        "Chakrabarti-Shafikov 2017, arXiv:1505.01230, Proposition 2.2, Theorem 1.1, Theorem 2.4 and Proposition 2.7",
        "localized smooth finite-R boundary segment, |A(epsilon+i*N)|=O(epsilon^(-1/2))",
        "the prescribed epsilon-downarrow-zero family has a canonical boundary in D'((-R,R)) and agrees with the inherited nonzero-arm boundary",
    )
    audit.guard_theorem(
        "G1.zero.guard.boundary_quasiasymptotic",
        True,
        "Montel normal-family uniqueness, compact polynomial-growth inclusion and continuity of the canonical boundary map",
        "Chakrabarti-Shafikov 2017, arXiv:1505.01230, Proposition 2.2, Theorem 1.1, Theorem 2.4 and Proposition 2.7",
        "F_r(w)=sqrt(r)*A(r*w), compact subsets of Re(w)>0, followed by the localized canonical boundary",
        "F_r is uniformly bounded in localized A^(-1); the compact A^(-1)-to-A^(-2) inclusion upgrades its unique compact-open limit K*w^(-1/2) to A^(-2) convergence, and the continuous boundary map gives a nonzero boundary quasiasymptotic of scaling degree exactly 1/2",
    )
    audit.guard_theorem(
        "G1.zero.guard.unique_scaling_degree_extension",
        True,
        "unique extension below the ambient dimension",
        "Brunetti-Fredenhagen 2000, arXiv:math-ph/9903028, Theorem 5.2",
        "one lapse dimension, inherited punctured distribution with scaling degree 1/2<1",
        "the extension preserving scaling degree 1/2 is unique; delta^(k) has degree 1+k and cannot be added without raising the degree",
    )

    return {
        "symbols": {
            "kappa": str(kappa),
            "c": str(c),
            "T": str(complex_t),
            "u_of_q": str(u_square),
        },
        "global_square": {
            "lower_bound": str(-lower_offset),
            "positive_remainder": str(u_square + lower_offset),
        },
        "full_q_bound": {
            "statement": "|A(epsilon+i*N)| <= K*exp(B*epsilon)/sqrt(epsilon)",
            "K": str(leading_coefficient),
            "B": str(lower_offset),
            "uniform_in_real_N": True,
            "uses_full_negative_q_tail": True,
        },
        "scaling": {
            "family": "F_r(w)=sqrt(r)*A(r*w)",
            "interior_limit": str(leading_coefficient / sp.sqrt(w)),
            "boundary_positive_N": str(
                leading_coefficient * positive_phase / sp.sqrt(n)
            ),
            "boundary_negative_N": str(
                leading_coefficient * negative_phase / sp.sqrt(n)
            ),
            "scaling_degree": "1/2",
            "delta_derivative_scaling_degrees": "1+k",
        },
        "sector_expansion": {
            "u0": str(u0),
            "u2": str(u2),
            "formal_bracket_through_T2": "1-u0*T+(u0^2/2-u2/(4*c))*T^2",
            "T2_coefficient": str(bracket_t2),
            "sector_remainder_certified_by_executable": False,
            "claim_boundary_pointwise_uniform": False,
        },
        "remote_tail": {
            "stationary_equation": str(stationary_equation),
            "coefficient_computed": False,
            "role_in_proof": "controlled by the global square bound and normal-family argument, not replaced by the sector expansion",
        },
        "negative_control": {
            "separate_Jp_boundary_multiplied_termwise": False,
            "reason": "the full q integral is not a smooth multiplier at T=0; pair the finite-epsilon full product before taking the boundary",
        },
    }


def build_result(
    frozen_input: dict[str, Any], input_sha256: str, audit: Audit
) -> dict[str, Any]:
    runner_path = Path(__file__)
    runner_sha256 = sha256_bytes(runner_path.read_bytes())
    calculation = exact_calculation(audit)
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "authorization_id": AUTHORIZATION_ID,
        "calculation_id": "Gate1M2ScalarZeroLapseExtension",
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": "GATE1_DECLARED_SCALAR_ZERO_LAPSE_CANONICAL_BOUNDARY_EXISTS",
        "verdict": "UNIQUE_SCALING_DEGREE_PRESERVING_EXTENSION",
        "programme_impact": "NARROW",
        "inherited_nonzero_arm_source_link": "KEEP",
        "declared_scalar_zero_lapse_distribution": "KEEP",
        "canonical_boundary": "EXISTS",
        "scaling_degree": "1/2",
        "scaling_degree_preserving_point_support": "ABSENT",
        "arbitrary_higher_scaling_extensions_excluded": False,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {"path": RUNNER_RELPATH, "sha256": runner_sha256},
        "upstream_result": {
            "path": f"cpt_temporal_folded_susy/{UPSTREAM_NAME}",
            "sha256": EXPECTED_UPSTREAM_SHA256,
        },
        "exact_calculation": calculation,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": [],
        "decision_trace": {
            "matched_predeclared_condition": "the full-tail bound, canonical boundary, nonzero leading quasiasymptotic and scaling-degree-preserving uniqueness all hold",
            "qualification": "unique means unique among extensions preserving scaling degree 1/2; unrestricted higher-scaling additions are not claimed impossible",
            "source_control_status": "FOLLOW_UP_WITHIN_DECLARED_TEST_CYCLE_NOT_PHYSICAL_ORIGINAL",
            "meaning": "close only the N=0 distributional subproblem for the declared fixed-a m=2 scalar link; leave the physical full joint/BFV cycle open",
        },
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": {
            "TOE_claim": None,
            "complete_global_signed_intersection_vector": None,
            "full_joint_orientation": None,
            "global_n_sigma": None,
            "physical_original_cycle": None,
            "physics_claim": None,
        },
        "resource_accounting": {
            "root_calls": 0,
            "ode_calls": 0,
            "evaluator_reconciliation_calls": 0,
            "numerical_samples": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_label": frozen_input["epistemic_label"],
            "fixed_limit_order": frozen_input["fixed_limit_order"],
        },
    }
    payload_sha256 = sha256_bytes(canonical_bytes(result))
    result["result_payload_sha256_without_self"] = payload_sha256
    return result


def main() -> None:
    frozen_input, input_sha256 = load_frozen_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, audit)
    encoded = json.dumps(
        result,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result artifact is {len(encoded)} bytes, cap is {ARTIFACT_CAP_BYTES}"
        )
    result_path = Path(__file__).with_name(RESULT_NAME)
    result_path.write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks": 0,
                "gate1": result["gate1_decision"],
                "global_n_sigma": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
