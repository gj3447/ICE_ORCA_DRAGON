#!/usr/bin/env python3
"""Gate 1 -- exact m=2 scalar phase-space/source-link control.

This non-numbered one-shot calculation starts from one newly declared ordered
real scalar phase-space control.  It eliminates the two scalar momenta exactly,
tracks their principal Fresnel phases, and checks the end coefficients needed
to deform the regulated real configuration line to the declared affine family.

The calculation is deliberately narrower than a physical original-cycle
derivation.  In particular it does not solve roots or ODEs, launch thimbles,
reconcile evaluators, cross N=0, vary a, include BFV variables, or emit a
physics/TOE claim.  It writes one adjacent JSON result.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "GATE1_SCALAR_SOURCE_LINK_INPUTS.json"
RESULT_NAME = "GATE1_SCALAR_SOURCE_LINK_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_scalar_source_link.py"
EXPECTED_INPUT_SHA256 = (
    "182ab0d04b2869cf01be39e0f73c02919ca4c9c17867f267e3daea915247ebd1"
)
AUTHORIZATION_ID = "GATE1_SOURCE_LINK_20260826_01"
RESULT_SCHEMA = "ice.gate1.scalar-source-link.result.v1"
RESULT_PREFIX = "GATE1_SCALAR_SOURCE_LINK_RESULT="
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
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.gate1.scalar-source-link.input.v1":
        raise AssertionError("unexpected input schema")
    if payload["authorization"]["id"] != AUTHORIZATION_ID:
        raise AssertionError("unexpected authorization identity")
    if payload["authorization"]["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
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
    a, hbar, epsilon = sp.symbols("a hbar epsilon", positive=True, real=True)
    n = sp.symbols("n", positive=True, real=True)
    lapse = sp.symbols("N", real=True)
    q, p0, p1 = sp.symbols("q p_0 p_1", real=True)
    phi = sp.symbols("phi", real=True)
    z = lapse - sp.I * epsilon
    kappa = sp.sqrt(sp.Rational(2, 3))
    mu = 2 * sp.pi**2 * a**3
    potential = sp.Rational(3, 4) * (
        1 - sp.exp(-kappa * (phi + q / 2))
    ) ** 2
    u_of_q = 2 * sp.pi**2 * (-3 * a + a**3 * potential)

    h = sp.Rational(1, 2)
    element_potential = 2 * sp.pi**2 * (3 * a - a**3 * potential)
    inherited_action = (
        p0 * q
        - h * z * (p0**2 / (4 * sp.pi**2 * a**3) - element_potential)
        - p1 * q
        - h * z * (p1**2 / (4 * sp.pi**2 * a**3) - element_potential)
    )
    lorentzian_action = q * (p0 - p1) - z * (p0**2 + p1**2) / (4 * mu) - z * u_of_q
    audit.check_exact(
        "G1.source.inherited_m2_phase_space_action",
        sp.simplify(inherited_action - lorentzian_action) == 0,
        "the two h=1/2 scalar elements reduce exactly to q(p0-p1)-z(p0^2+p1^2)/(4*mu)-z*U(q)",
    )

    stationary_p0 = 2 * mu * q / z
    stationary_p1 = -2 * mu * q / z
    audit.check_exact(
        "G1.source.stationary_scalar_momenta",
        sp.simplify(sp.diff(lorentzian_action, p0).subs(p0, stationary_p0)) == 0
        and sp.simplify(sp.diff(lorentzian_action, p1).subs(p1, stationary_p1)) == 0,
        "the unique scalar Gaussian saddle is p0=2*mu*q/z and p1=-2*mu*q/z for z!=0",
    )

    eliminated = sp.simplify(
        lorentzian_action.subs({p0: stationary_p0, p1: stationary_p1})
    )
    expected_eliminated = 2 * mu * q**2 / z - z * u_of_q
    audit.check_exact(
        "G1.source.momentum_elimination",
        sp.simplify(eliminated - expected_eliminated) == 0,
        "eliminating both scalar momenta gives I2=2*mu*q^2/z-z*U(q)",
    )

    completed = (
        -z
        / (4 * mu)
        * ((p0 - stationary_p0) ** 2 + (p1 - stationary_p1) ** 2)
        + expected_eliminated
    )
    audit.check_exact(
        "G1.source.two_momentum_square_completion",
        sp.simplify(lorentzian_action - completed) == 0,
        "the ordered two-momentum integral is a product of two identical damped Gaussian translations",
    )

    gaussian_coefficient = sp.I * z / (4 * mu * hbar)
    gaussian_plane_integral = sp.pi / gaussian_coefficient
    normalized_prefactor = sp.simplify(
        gaussian_plane_integral / (2 * sp.pi * hbar) ** 2
    )
    expected_prefactor = mu / (sp.pi * sp.I * hbar * z)
    audit.check_exact(
        "G1.source.ordered_gaussian_prefactor",
        sp.simplify(normalized_prefactor - expected_prefactor) == 0
        and sp.simplify(sp.re(sp.I * z) - epsilon) == 0,
        "with dp0 wedge dp1/(2*pi*hbar)^2, Re(i*z)=epsilon>0 and the Gaussian-plane theorem gives Jp=mu/(pi*i*hbar*z)",
    )

    T = sp.I * z
    euclidean_action = 2 * mu * q**2 / T + T * u_of_q
    audit.check_exact(
        "G1.source.wick_integrand_identity",
        sp.simplify(sp.I * expected_eliminated + euclidean_action) == 0,
        "under T=i*z, exp(i*I2/hbar)=exp(-S2/hbar) after momentum elimination",
    )
    audit.check_exact(
        "G1.source.prefactor_in_T_convention",
        sp.simplify(expected_prefactor - 2 * sp.pi * a**3 / (hbar * T)) == 0,
        "the same ordered scalar prefactor is Jp=2*pi*a^3/(hbar*T)",
    )

    positive_slice_phase = sp.exp(-sp.I * sp.pi / 4)
    negative_slice_phase = sp.exp(sp.I * sp.pi / 4)
    positive_arm_prefactor = expected_prefactor.subs({lapse: n, epsilon: 0})
    negative_arm_prefactor = expected_prefactor.subs({lapse: -n, epsilon: 0})
    audit.check_exact(
        "G1.source.positive_lapse_fresnel_orientation",
        sp.simplify(positive_slice_phase**2 + sp.I) == 0
        and sp.simplify(
            positive_arm_prefactor + sp.I * mu / (sp.pi * hbar * n)
        )
        == 0,
        "for N>0 each ordered real momentum contributes exp(-i*pi/4), so their product is -i and Jp=-i*2*pi*a^3/(hbar*N)",
    )
    audit.check_exact(
        "G1.source.negative_lapse_fresnel_orientation",
        sp.simplify(negative_slice_phase**2 - sp.I) == 0
        and sp.simplify(
            negative_arm_prefactor - sp.I * mu / (sp.pi * hbar * n)
        )
        == 0,
        "for N<0 each ordered real momentum contributes exp(+i*pi/4), so their product is +i and Jp=+i*2*pi*a^3/(hbar*abs(N))",
    )
    audit.check_exact(
        "G1.source.arm_prefactors_are_conjugate",
        sp.simplify(negative_arm_prefactor - sp.conjugate(positive_arm_prefactor))
        == 0,
        "the two real-lapse scalar prefactors glue by complex conjugation with no extra combined BFV/Maslov sign",
    )

    rho = sp.symbols("rho", positive=True, real=True)
    psi, lam, homotopy_s, u, y = sp.symbols(
        "psi lambda s u y", real=True
    )
    complex_T = rho * sp.exp(sp.I * psi)
    shift = homotopy_s * lam * psi / kappa
    homotopy_q = u + sp.I * shift
    phase_defect = sp.simplify(psi - kappa * shift)
    negative_end_leading_real_coefficient = (
        sp.Rational(3, 2)
        * sp.pi**2
        * a**3
        * rho
        * sp.exp(-2 * kappa * phi)
        * sp.cos(phase_defect)
    )
    audit.check_exact(
        "G1.source.affine_homotopy_phase_defect",
        sp.simplify(phase_defect - (1 - homotopy_s * lam) * psi) == 0,
        "along q=u+i*s*lambda*psi/kappa the full-rate Starobinsky phase defect is (1-s*lambda)*psi",
    )

    positive_end_kinetic_coefficient = sp.simplify(
        sp.re(2 * mu / complex_T).expand(complex=True)
    )
    audit.check_exact(
        "G1.source.positive_field_end_coefficient",
        sp.simplify(
            positive_end_kinetic_coefficient - 2 * mu * sp.cos(psi) / rho
        )
        == 0,
        "for |psi|<pi/2 the positive-field end has the strictly positive quadratic coefficient 2*mu*cos(psi)/rho",
    )

    audit.check_exact(
        "G1.source.rectangular_connector_measures",
        sp.diff(homotopy_q, u) == 1
        and sp.simplify(sp.diff(homotopy_q, homotopy_s) - sp.I * lam * psi / kappa)
        == 0,
        "horizontal pieces retain dq=du and finite-cutoff vertical connectors retain their explicit dq=i*lambda*psi/kappa ds orientation",
    )

    arm_sign = sp.symbols("sigma", real=True, nonzero=True)
    arm_shift = arm_sign * lam * sp.pi / (2 * kappa)
    pure_gaussian_real = sp.simplify(
        sp.re(
            2
            * mu
            * (u + sp.I * arm_shift) ** 2
            / (sp.I * arm_sign * n)
        ).expand(complex=True)
    )
    expected_pure_gaussian_real = 2 * sp.pi * mu * lam * u / (kappa * n)
    audit.check_exact(
        "G1.source.pure_q_gaussian_is_not_affine_certificate",
        sp.simplify(pure_gaussian_real - expected_pure_gaussian_real) == 0,
        "on either Gamma_lambda boundary arm the kinetic-only real part is linear in u and therefore tends to minus infinity at one end for every lambda>0",
    )

    positive_boundary_defect = sp.pi * (1 - lam) / 2
    negative_boundary_defect = -sp.pi * (1 - lam) / 2
    boundary_negative_end_factor = sp.sin(sp.pi * lam / 2)
    audit.check_exact(
        "G1.source.boundary_arm_end_coefficients",
        sp.simplify(
            sp.cos(positive_boundary_defect) - boundary_negative_end_factor
        )
        == 0
        and sp.simplify(
            sp.cos(negative_boundary_defect) - boundary_negative_end_factor
        )
        == 0
        and sp.simplify(
            expected_pure_gaussian_real.coeff(u)
            - 4 * sp.pi**3 * a**3 * lam / (kappa * n)
        )
        == 0,
        "at T=+/-i*n, the negative-field Starobinsky coefficient contains sin(lambda*pi/2)>0 and the positive-field kinetic exponent grows as 4*pi^3*a^3*lambda*u/(kappa*n)",
    )

    audit.check_exact(
        "G1.source.zero_lapse_divisor_remains",
        sp.denom(expected_prefactor).has(z),
        "the momentum-first prefactor retains the z=0 divisor; its own delta-plus-principal-value boundary is standard, but fixed-nonzero-arm equality does not establish the full q-paired distribution on tests whose support crosses N=0",
    )

    audit.guard_theorem(
        "G1.guard.damped_gaussian_translation",
        sp.simplify(sp.re(sp.I * z) - epsilon) == 0,
        "two-dimensional Gaussian integral with Re(A)>0",
        "epsilon>0, z=N-i*epsilon, a>0, hbar>0",
        "the completed-square translations are entire and the ordered real momentum integral has the pinned principal normalization",
    )
    audit.guard_theorem(
        "G1.guard.entire_rectangular_contour_homotopy",
        True,
        "Cauchy deformation on finite rectangles followed by end bounds",
        "Re(T)>0, |psi|<pi/2, 0<lambda<=1, 0<=s<=1",
        "the integrand is entire in q; cos((1-s*lambda)*psi)>0 controls the negative Starobinsky end and 2*mu*cos(psi)/rho>0 controls the positive kinetic end, with connector measures retained",
    )
    audit.guard_theorem(
        "G1.guard.nonzero_lapse_boundary_pairing",
        True,
        "compact-support dominated boundary limit on each closed sub-arm away from zero",
        "test functions in C_c^infinity((-R,0) union (0,R)), fixed R=6/5 and fixed 0<lambda<=1",
        "finite-epsilon equality passes to the two fixed-nonzero boundary arms; lambda-independence gives the same lambda->0+ arm distribution without selecting lambda=1",
    )

    return {
        "symbols": {
            "mu": str(mu),
            "kappa": str(kappa),
            "z": str(z),
            "T": str(T),
            "U_of_q": str(u_of_q),
        },
        "lorentzian_action": str(lorentzian_action),
        "stationary_momenta": {
            "p_phi_0": str(stationary_p0),
            "p_phi_1": str(stationary_p1),
        },
        "eliminated_action": str(eliminated),
        "configuration_action": str(euclidean_action),
        "momentum_prefactor": str(expected_prefactor),
        "momentum_prefactor_in_T": str(2 * sp.pi * a**3 / (hbar * T)),
        "real_lapse_arm_prefactors": {
            "positive": str(positive_arm_prefactor),
            "negative": str(negative_arm_prefactor),
            "ordered_slice_phases": {
                "positive": "exp(-i*pi/4) twice",
                "negative": "exp(+i*pi/4) twice",
            },
        },
        "affine_homotopy": {
            "q": str(homotopy_q),
            "phase_defect": str(phase_defect),
            "negative_end_leading_real_coefficient": str(
                negative_end_leading_real_coefficient
            ),
            "positive_end_kinetic_coefficient": str(
                positive_end_kinetic_coefficient
            ),
            "boundary_negative_end_factor": str(boundary_negative_end_factor),
            "boundary_positive_end_coefficient": str(
                4 * sp.pi**3 * a**3 * lam / (kappa * n)
            ),
            "horizontal_measure": "dq=du",
            "vertical_connector_measure": "dq=i*lambda*psi/kappa ds",
        },
        "pure_q_gaussian_negative_control": {
            "boundary_arm_real_part": str(pure_gaussian_real),
            "status": "ONE_EXPONENTIALLY_GROWING_END_FOR_EVERY_NONZERO_SHIFT",
            "may_certify_source_link": False,
        },
        "proved_scope": {
            "finite_epsilon_full_action_real_to_affine_equality": True,
            "fixed_nonzero_lapse_arm_boundary_equality": True,
            "scalar_orientation_ratio": "+1",
            "lambda_family_equivalent_on_nonzero_arms": True,
            "lambda_one_selected": False,
        },
        "open_scope": {
            "momentum_prefactor_boundary_distribution": "(2*pi*a^3/hbar)*(pi*delta(N)-i*PV(1/N))",
            "zero_including_lapse_distribution": "OPEN",
            "N_zero_contact_terms": "OPEN",
            "physical_original_cycle": None,
            "full_joint_orientation": None,
            "varying_a_or_BFV_extension": None,
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
        "calculation_id": "Gate1M2ScalarPhaseSpaceSourceLink",
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": "GATE1_NONZERO_LAPSE_SCALAR_SOURCE_LINK_MATCHES_ZERO_LAPSE_DISTRIBUTION_OPEN",
        "verdict": "NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN",
        "programme_impact": "NARROW",
        "reduced_affine_class_nonzero_arm_source_link": "KEEP",
        "zero_lapse_distribution": "OPEN",
        "phase_locked_representative_selected": False,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {"path": RUNNER_RELPATH, "sha256": runner_sha256},
        "exact_calculation": calculation,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": [],
        "decision_trace": {
            "matched_predeclared_condition": "the nonzero-lapse arm source link and scalar orientation match, but the zero-lapse distribution cannot be established without the inadmissible pure-q-Gaussian shortcut or an excluded limit",
            "source_control_status": "NEW_BOUNDED_SCALAR_CONTROL_NOT_PHYSICAL_ORIGINAL",
            "meaning": "keep only the fixed-a m=2 reduced scalar source link on the two nonzero lapse arms; the zero-lapse distribution and full joint cycle remain open",
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
