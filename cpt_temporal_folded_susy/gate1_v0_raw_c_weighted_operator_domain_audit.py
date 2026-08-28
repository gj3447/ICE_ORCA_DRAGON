#!/usr/bin/env python3
"""Gate 1 -- weighted raw-C operator and domain audit.

This bounded non-numbered calculation audits one explicitly declared
quantization of the undensitized closed-FRW V=0 constraint:

    H_C = L2(R_Q x R_phi, f(Q) dQ dphi),
    f(Q) = 12*pi**2*exp(3Q/2),
    C_min = f**(-1) H_hat on C_c^infinity.

It verifies the weighted symmetry, flat conjugation, Fourier fibers,
zero-energy Bessel reduction, endpoint integrability and boundary forms.
Standard Weyl, von Neumann and direct-integral theorems are used only through
explicit hypothesis/scope guards.  The result classifies the fixed-p extension
debt and records the additional measurable-field condition for a p-preserving
direct integral; it constructs no global extension and proves no raw-C/H
equivalence, rigging map, BFV measure, quantum-gravity, physics or TOE claim.
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


INPUT_NAME = "GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_INPUTS.json"
RESULT_NAME = "GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_v0_raw_c_weighted_operator_domain_audit.py"
)
EXPECTED_INPUT_SHA256 = (
    "0176dccf68298002ec598bd5acf4e1cb3b11b644a60a5644ac03bb39e800d9f6"
)
CALCULATION_ID = "Gate1V0RawCWeightedOperatorDomainAudit"
RESULT_SCHEMA = "ice.gate1.v0-raw-c-weighted-operator-domain-audit.result.v1"
RESULT_PREFIX = "GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
NUMERICAL_DPS = 70
BESSEL_FUNCTION_SAMPLE_CAP = 24


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


def decimal(value: mp.mpf, digits: int = 60) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    bessel_function_samples: int = 0
    wronskian_reuse_points: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def observe_numeric_max(
        self,
        check_id: str,
        maximum_error: mp.mpf,
        tolerance: mp.mpf,
        statement: str,
        sample_count: int,
    ) -> bool:
        self.register(check_id)
        passed = bool(maximum_error <= tolerance)
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "sample_count": sample_count,
                "maximum_error": decimal(maximum_error),
                "tolerance": decimal(tolerance),
            }
        )
        return passed

    def guard(
        self,
        guard_id: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": (
                    "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_"
                    "NUMERICAL_PREDICATE"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_repository_source(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    observed = sha256_bytes(path.read_bytes())
    if observed != item["sha256"]:
        raise AssertionError(
            f"repository source hash mismatch for {item['path']}: {observed}"
        )
    return {"path": item["path"], "sha256": observed}


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(
            f"upstream hash mismatch for {item['path']}: {observed}"
        )
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload mutation: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "selected_raw_C_self_adjoint_extension": None,
        "p_preserving_decomposable_self_adjoint_extension": None,
        "general_full_operator_extension_classification": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "quantum_constraint_rescaling_equivalence": None,
        "canonical_p_zero_origin_sector": None,
        "cross_branch_gluing_or_quotient": None,
        "exact_endpoint_state_transform": None,
        "declared_Mc_identity_equivalence": None,
        "lapse_modulus_or_contour_selection": None,
        "absolute_bfv_measure": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def load_input() -> tuple[
    dict[str, Any], str, list[dict[str, str]], list[dict[str, str]]
]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-raw-c-weighted-operator-domain-audit.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "bessel_sample_points": 24,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != caps:
        raise AssertionError("resource cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    candidate = payload["declared_candidate"]
    if (
        candidate["minimal_operator"]
        != "C_min=f(Q)^(-1)*H_hat on C_c^infinity(R_Q times R_phi)"
        or candidate["minimal_fiber_core"] != "C_c^infinity(R_Q)"
        or not candidate["extension_scope"].startswith("fixed-p self-adjoint")
        or payload["epistemic_scope"]
        != (
            "ONE_DECLARED_LEFT_WEIGHTED_RAW_C_ORDERING_ON_L2_F_DQ_DPHI_"
            "ITS_FIBER_EXTENSIONS_AND_A_CONDITIONAL_P_PRESERVING_DIRECT_"
            "INTEGRAL_RECIPE"
        )
    ):
        raise AssertionError("candidate operator or extension scope mutation")
    root = Path(__file__).resolve().parent.parent
    sources = [
        verify_repository_source(root, item)
        for item in payload["repository_sources"]
    ]
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, sources, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    Q, phi = sp.symbols("Q phi", real=True)
    P, p = sp.symbols("P p", real=True)
    hbar, x = sp.symbols("hbar x", positive=True, real=True)
    pi = sp.pi
    f = 12 * pi**2 * sp.exp(sp.Rational(3, 2) * Q)
    g = sp.exp(-sp.Rational(3, 4) * Q) / sp.sqrt(12 * pi**2)

    C_classical = (
        -sp.exp(-sp.Rational(3, 2) * Q) * P**2 / (6 * pi**2)
        + sp.exp(-sp.Rational(3, 2) * Q) * p**2 / (4 * pi**2)
        - 6 * pi**2 * sp.exp(Q / 2)
    )
    H_classical = -2 * P**2 + 3 * p**2 - 72 * pi**4 * sp.exp(2 * Q)
    flags: dict[str, bool] = {}
    flags["classical_relation"] = audit.observe(
        "G1.rawc.classical.f_positive_and_H_equals_fC",
        f.is_positive is True and sp.simplify(f * C_classical - H_classical) == 0,
        "the frozen positive multiplier f=12*pi^2*exp(3Q/2) gives H=f*C exactly",
    )

    sqrt_f = sp.sqrt(12 * pi**2) * sp.exp(sp.Rational(3, 4) * Q)
    flags["unitary_map"] = audit.observe(
        "G1.rawc.weighted.unitary_map",
        sp.simplify(f * g**2 - 1) == 0
        and sp.simplify(sqrt_f * g - 1) == 0,
        "U chi=f^(1/2) chi and U^(-1) psi=g psi are inverse isometries between L2(f dQ dphi) and flat L2 and preserve C_c^infinity",
    )

    ub = sp.Function("ub")(Q)
    v = sp.Function("v")(Q)
    q_green = sp.simplify(
        ub * sp.diff(v, Q, 2)
        - sp.diff(ub, Q, 2) * v
        - sp.diff(ub * sp.diff(v, Q) - sp.diff(ub, Q) * v, Q)
    )
    phib = sp.Function("phib")(phi)
    wphi = sp.Function("wphi")(phi)
    phi_green = sp.simplify(
        phib * sp.diff(wphi, phi, 2)
        - sp.diff(phib, phi, 2) * wphi
        - sp.diff(
            phib * sp.diff(wphi, phi)
            - sp.diff(phib, phi) * wphi,
            phi,
        )
    )
    flags["weighted_symmetry"] = audit.observe(
        "G1.rawc.weighted.symmetric_green_identity",
        q_green == 0 and phi_green == 0,
        "the f weight cancels f^(-1), and integration by parts leaves only the 2*hbar^2 Q-Wronskian and -3*hbar^2 phi-Wronskian, both zero on the compact core",
    )

    psi = sp.Function("psi")(Q, phi)
    conjugated = sp.expand(
        g
        * (
            2 * hbar**2 * sp.diff(g * psi, Q, 2)
            - 3 * hbar**2 * sp.diff(g * psi, phi, 2)
            - 72 * pi**4 * sp.exp(2 * Q) * g * psi
        )
    )
    expected_conjugated = (
        sp.exp(-sp.Rational(3, 2) * Q)
        / (12 * pi**2)
        * (
            2 * hbar**2 * sp.diff(psi, Q, 2)
            - 3 * hbar**2 * sp.diff(psi, phi, 2)
            - 3 * hbar**2 * sp.diff(psi, Q)
            + sp.Rational(9, 8) * hbar**2 * psi
            - 72 * pi**4 * sp.exp(2 * Q) * psi
        )
    )
    flags["flat_conjugate"] = audit.observe(
        "G1.rawc.flat.conjugation_and_expansion",
        sp.simplify(conjugated - expected_conjugated) == 0,
        "U*C_min*U^(-1)=g*H_hat*g has the exact expanded flat differential expression including the -3*hbar^2*d_Q and 9*hbar^2/8 terms",
    )

    u = sp.Function("u")(Q)
    plane = sp.exp(sp.I * p * phi / hbar)
    H_on_plane = sp.simplify(
        (
            2 * hbar**2 * sp.diff(u * plane, Q, 2)
            - 3 * hbar**2 * sp.diff(u * plane, phi, 2)
            - 72 * pi**4 * sp.exp(2 * Q) * u * plane
        )
        / plane
    )
    expected_fiber_numerator = (
        2 * hbar**2 * sp.diff(u, Q, 2)
        + (3 * p**2 - 72 * pi**4 * sp.exp(2 * Q)) * u
    )
    flags["fiberization"] = audit.observe(
        "G1.rawc.fourier.formal_fiber_symbol",
        sp.simplify(H_on_plane - expected_fiber_numerator) == 0,
        "on Fourier plane waves the formal raw fiber symbol is C_p=f^(-1)[2*hbar^2*d_Q^2+3*p^2-72*pi^4*exp(2Q)]; the operator direct integral is separately theorem-guarded",
    )

    z = sp.symbols("z")
    raw_fiber = expected_fiber_numerator / f
    deficiency_numerator = sp.expand(f * (raw_fiber - z * u))
    expected_deficiency = (
        2 * hbar**2 * sp.diff(u, Q, 2)
        + (
            3 * p**2
            - 72 * pi**4 * sp.exp(2 * Q)
            - 12 * pi**2 * z * sp.exp(sp.Rational(3, 2) * Q)
        )
        * u
    )
    flags["deficiency_equation"] = audit.observe(
        "G1.rawc.deficiency.weighted_equation",
        sp.simplify(deficiency_numerator - expected_deficiency) == 0,
        "(C_p-z)u=0 is exactly the recorded weighted Sturm-Liouville deficiency equation",
    )

    Y = sp.Function("Y")(x)
    a_squared = 3 * p**2 / (2 * hbar**2)
    x_of_Q = 6 * pi**2 * sp.exp(Q) / hbar
    q_second_derivative = x**2 * sp.diff(Y, x, 2) + x * sp.diff(Y, x)
    transformed_directly_from_raw = sp.simplify(
        (
            2 * hbar**2 * q_second_derivative
            + (3 * p**2 - 2 * hbar**2 * x**2) * Y
        )
        / (2 * hbar**2)
    )
    expected_transformed_equation = (
        x**2 * sp.diff(Y, x, 2)
        + x * sp.diff(Y, x)
        + (a_squared - x**2) * Y
    )
    flags["bessel_transform"] = audit.observe(
        "G1.rawc.bessel.zero_energy_transform",
        sp.simplify(
            transformed_directly_from_raw - expected_transformed_equation
        )
        == 0
        and sp.simplify(
            72 * pi**4 * sp.exp(2 * Q) - 2 * hbar**2 * x_of_Q**2
        )
        == 0,
        "substituting x=6*pi^2*exp(Q)/hbar and d_Q=x*d_x directly into the z=0 raw fiber gives the modified-Bessel equation with order squared -3*p^2/(2*hbar^2)",
    )
    p_zero_bessel = sp.simplify(expected_transformed_equation.subs(p, 0))
    expected_p_zero_bessel = (
        x**2 * sp.diff(Y, x, 2) + x * sp.diff(Y, x) - x**2 * Y
    )
    flags["p_zero_bessel"] = audit.observe(
        "G1.rawc.bessel.p_zero_order_zero_equation",
        sp.simplify(p_zero_bessel - expected_p_zero_bessel) == 0,
        "the p=0 fiber is separately the order-zero modified-Bessel equation with independent I_0 and K_0 reference solutions",
    )

    raw_weight_x = (
        12
        * pi**2
        * (hbar * x / (6 * pi**2)) ** sp.Rational(3, 2)
        / x
    )
    expected_raw_weight_x = (
        2 * hbar ** sp.Rational(3, 2) * sp.sqrt(x) / (sp.sqrt(6) * pi)
    )
    small_nonzero_integral = sp.integrate(x ** sp.Rational(1, 2), (x, 0, 1))
    flags["minus_nonzero"] = audit.observe(
        "G1.rawc.endpoint.minus_nonzero_weighted_integrability",
        sp.simplify(raw_weight_x - expected_raw_weight_x) == 0
        and sp.simplify(small_nonzero_integral - sp.Rational(2, 3)) == 0,
        "for p nonzero the two x^(+/-i*a) zero-energy modes have bounded modulus and both are integrable against the raw weight proportional to x^(1/2) dx at x=0",
    )

    small_zero_constant = small_nonzero_integral
    small_zero_log = sp.integrate(
        x ** sp.Rational(1, 2) * sp.log(x) ** 2, (x, 0, 1)
    )
    flags["minus_zero"] = audit.observe(
        "G1.rawc.endpoint.minus_zero_weighted_integrability",
        sp.simplify(small_zero_constant - sp.Rational(2, 3)) == 0
        and sp.simplify(small_zero_log - sp.Rational(16, 27)) == 0,
        "for p=0 the independent 1 and log(x), equivalently 1 and Q, modes are separately weighted-integrable at x=0",
    )

    growing_weight = sp.exp(2 * x) / sp.sqrt(x)
    decaying_weight = sp.exp(-2 * x) / sp.sqrt(x)
    decaying_integral = sp.integrate(decaying_weight, (x, 1, sp.oo))
    flags["plus_endpoint"] = audit.observe(
        "G1.rawc.endpoint.plus_one_integrable_one_nonintegrable",
        sp.limit(growing_weight, x, sp.oo) == sp.oo
        and decaying_integral.is_finite is True,
        "the weighted I asymptotic grows while the weighted K asymptotic is integrable at x=infinity, leaving one square-integrable zero-energy solution",
    )

    q = sp.symbols("q", real=True)
    k = sp.symbols("k", positive=True, real=True)
    Aub, Bub, Av, Bv = sp.symbols("Aub Bub Av Bv")
    ubar_mode = Aub * sp.exp(-sp.I * k * q) + Bub * sp.exp(sp.I * k * q)
    v_mode = Av * sp.exp(sp.I * k * q) + Bv * sp.exp(-sp.I * k * q)
    oscillatory_wronskian = sp.simplify(
        ubar_mode * sp.diff(v_mode, q)
        - sp.diff(ubar_mode, q) * v_mode
    )
    expected_oscillatory = 2 * sp.I * k * (Aub * Av - Bub * Bv)
    global_oscillatory_form = sp.simplify(
        -2 * hbar**2 * oscillatory_wronskian
    )
    expected_global_oscillatory_form = (
        -4 * sp.I * hbar**2 * k * (Aub * Av - Bub * Bv)
    )
    theta = sp.symbols("theta", real=True)
    J = sp.diag(1, -1)
    phase_vector = sp.Matrix([1, sp.exp(sp.I * theta)])
    phase_is_lagrangian = sp.simplify(
        (phase_vector.conjugate().T * J * phase_vector)[0]
    )
    flags["nonzero_boundary"] = audit.observe(
        "G1.rawc.boundary.nonzero_p_form_and_phase",
        sp.simplify(oscillatory_wronskian - expected_oscillatory) == 0
        and sp.simplify(
            global_oscillatory_form - expected_global_oscillatory_form
        )
        == 0
        and phase_is_lagrangian == 0,
        "with the global Green-form orientation [W]_-infinity^+infinity, the formal traveling-coordinate contribution is -4*i*hbar^2*k*(Abar*A-Bbar*B); its overall sign leaves B=exp(i*theta)A Lagrangian",
    )

    A0ub, B0ub, A0v, B0v = sp.symbols("A0ub B0ub A0v B0v")
    ubar_zero = A0ub + B0ub * q
    v_zero = A0v + B0v * q
    affine_wronskian = sp.simplify(
        ubar_zero * sp.diff(v_zero, q)
        - sp.diff(ubar_zero, q) * v_zero
    )
    global_affine_form = sp.simplify(-2 * hbar**2 * affine_wronskian)
    expected_global_affine_form = (
        -2 * hbar**2 * (A0ub * B0v - B0ub * A0v)
    )
    lam = sp.symbols("lam", real=True)
    J0 = sp.Matrix([[0, 1], [-1, 0]])
    projective_vector = sp.Matrix([1, lam])
    projective_is_lagrangian = sp.simplify(
        (projective_vector.conjugate().T * J0 * projective_vector)[0]
    )
    flags["zero_boundary"] = audit.observe(
        "G1.rawc.boundary.zero_p_form_and_projective_condition",
        sp.simplify(
            affine_wronskian - (A0ub * B0v - B0ub * A0v)
        )
        == 0
        and sp.simplify(global_affine_form - expected_global_affine_form) == 0
        and projective_is_lagrangian == 0,
        "with the global Green-form orientation, the p=0 affine-coordinate contribution is -2*hbar^2*(Abar*B-Bbar*A); its overall sign leaves B=lambda*A with real projective lambda Lagrangian",
    )

    theta_zero_vector = sp.Matrix([1, 1])
    theta_pi_vector = sp.Matrix([1, -1])
    flags["extension_noncanonicity"] = audit.observe(
        "G1.rawc.extension.distinct_fiber_domains",
        sp.det(sp.Matrix.hstack(theta_zero_vector, theta_pi_vector)) == -2,
        "theta=0 and theta=pi give distinct fiber boundary lines, so the differential expression does not canonically select one domain",
    )

    audit.guard(
        "G1.rawc.guard.declared_quantization_only",
        "weighted-space symmetric-operator construction",
        "f is smooth and strictly positive; C_min=f^(-1)H_hat is declared on C_c^infinity in L2(f dQ dphi), and the integration-by-parts identities are exact",
        "this constructs one closable symmetric raw-C candidate; it does not prove that the ordering or auxiliary measure is forced by the classical constraint",
    )
    audit.guard(
        "G1.rawc.guard.fourier_direct_integral_core",
        "Fourier-Plancherel decomposition of a translation-invariant differential operator and closure of its minimal fibers",
        "the coefficients are independent of phi; the phi Fourier transform is unitary; the transformed core contains C_c^infinity(R_Q) tensor Schwartz(R_p), and the formal plane-wave symbol check fixes C_p on that common algebraic core",
        "the closure is decomposable over Lebesgue p with minimal scalar fibers; the executable plane-wave calculation alone is only a symbol check and does not choose fiber extensions",
    )
    audit.guard(
        "G1.rawc.guard.weyl_alternative",
        "Weyl limit-point/limit-circle alternative for real singular Sturm-Liouville expressions",
        "after multiplying by -1, each real-p fiber has leading coefficient 2*hbar^2>0, weight f>0, real locally integrable potential 72*pi^4*exp(2Q)-3*p^2, and minimal core C_c^infinity(R)",
        "endpoint type is independent of the nonreal spectral parameter, so the separately audited z=0 Bessel integrability classifies Q=-infinity as limit-circle and Q=+infinity as limit-point",
    )
    audit.guard(
        "G1.rawc.guard.fiber_deficiency_indices",
        "Weyl deficiency-index theorem for one limit-circle and one limit-point endpoint",
        "both p nonzero and p=0 have two weighted-integrable local solutions at Q=-infinity and one at Q=+infinity",
        "the minimal scalar fiber has n_plus=n_minus=1 for every p; this is a fiber statement, not the dimension or full extension classification of the two-dimensional operator",
    )
    audit.guard(
        "G1.rawc.guard.bessel_asymptotic_boundary_coordinates",
        "DLMF small-argument modified-Bessel asymptotics plus singular Sturm-Liouville boundary-form theory",
        "for p nonzero, I_(+/-i*a)(x) is asymptotic to (x/2)^(+/-i*a)/Gamma(1+/-i*a), hence to constant multiples of exp(+/-i*k_p*Q); for p=0, I_0 and K_0 are asymptotic to 1 and -log(x), hence to 1 and an affine Q mode",
        "the executable traveling/affine Wronskian ledgers fix the oriented asymptotic sign convention, while actual maximal-domain boundary maps are Wronskian limits against a real zero-energy reference pair normalized at a finite Q_0; literal u(-infinity) and u'(-infinity) are not used",
    )
    audit.guard(
        "G1.rawc.guard.fiber_boundary_maps_and_extensions",
        "one-limit-circle one-limit-point Sturm-Liouville boundary maps and von Neumann extension theory",
        "for each fixed p choose real zero-energy c_p,s_p with W(c_p,s_p)=1 at Q_0=0; the limit-circle theorem gives Wronskian boundary limits on D(C_p,max), and the global Green form is oriented as [W]_-infinity^+infinity",
        "one real projective, equivalently U(1), boundary line gives a self-adjoint scalar-fiber extension; the exact A/B formulas are asymptotic-coordinate ledgers, not a claim that arbitrary maximal-domain functions have literal plane-wave limits",
    )
    audit.guard(
        "G1.rawc.guard.measurable_decomposable_family",
        "reduction theory for unbounded closed operators and measurable direct integrals",
        "the Fourier base is Lebesgue p; finite-Q reference solutions depend continuously on p^2, but the limiting boundary maps and chosen extension domains/resolvents must still form a measurable field, in addition to any Borel theta(p)",
        "this audit records only the conditional recipe for a p-preserving decomposable extension and does not construct or promote a measurable global self-adjoint domain; equal fiber indices and Borel theta alone are insufficient",
    )
    audit.guard(
        "G1.rawc.guard.general_full_extensions_and_p_zero",
        "von Neumann deficiency-space and direct-integral scope separation",
        "the full deficiency spaces are infinite-dimensional over p; general unitaries N_plus to N_minus can mix fibers, while the singleton p=0 has zero Lebesgue base measure",
        "the audit does not classify general p-mixing extensions, and a p=0 boundary parameter has no full direct-integral effect unless an extra atom is declared",
    )
    audit.guard(
        "G1.rawc.guard.no_raq_or_equivalence_promotion",
        "self-adjoint-domain versus refined-algebraic-quantization separation",
        "no extension theta(p), raw-C spectral resolution, zero-fiber group average, rigging map, physical product, or domain-preserving observable intertwiner is computed",
        "the fixed-p extension debt proves that extra quantum data are required and kills automatic C-to-H equivalence; it neither proves inequivalence of every extension nor supplies a measurable global extension, endpoint transform, BFV, physics, or TOE result",
    )

    endpoint_classification = {
        "Q_minus_infinity": {
            "weyl_type": "LIMIT_CIRCLE",
            "p_nonzero_asymptotic_modes": "exp(+i*k_p*Q), exp(-i*k_p*Q)",
            "p_zero_asymptotic_modes": "1, Q",
            "actual_boundary_maps": (
                "Wronskian limits against a real zero-energy pair c_p,s_p "
                "normalized at Q_0=0"
            ),
            "weighted_integrable_solution_count_at_z_zero": 2,
        },
        "Q_plus_infinity": {
            "weyl_type": "LIMIT_POINT",
            "zero_energy_reference_modes": "I_(i*a)(x), K_(i*a)(x)",
            "weighted_integrable_solution_count_at_z_zero": 1,
        },
        "fiber_deficiency_indices": "n_plus=n_minus=1 for every fixed p under the declared Weyl guards",
    }
    return (
        {
            "declared_raw_C_candidate": {
                "f": str(f),
                "weighted_auxiliary_space": "L2(R_Q times R_phi,f dQ dphi)",
                "minimal_operator": "C_min=f^(-1)*H_hat on C_c^infinity",
                "flat_unitary": "U chi=f^(1/2) chi",
                "flat_conjugate": (
                    "exp(-3Q/2)/(12*pi^2)*[2*hbar^2*d_Q^2"
                    "-3*hbar^2*d_phi^2-3*hbar^2*d_Q+9*hbar^2/8"
                    "-72*pi^4*exp(2Q)]"
                ),
            },
            "fiber_equation": {
                "raw_fiber": (
                    "C_p=f^(-1)[2*hbar^2*d_Q^2+3*p^2"
                    "-72*pi^4*exp(2Q)]"
                ),
                "deficiency_equation": (
                    "2*hbar^2*u''+[3*p^2-72*pi^4*exp(2Q)"
                    "-12*pi^2*z*exp(3Q/2)]u=0"
                ),
                "zero_energy_variable": "x=6*pi^2*exp(Q)/hbar",
                "zero_energy_bessel_order": "i*sqrt(3/2)*abs(p)/hbar",
            },
            "endpoint_classification": endpoint_classification,
            "fiber_extension_and_direct_integral_boundary": {
                "p_nonzero_boundary_form": (
                    "-4*i*hbar^2*k_p*(conjugate(A_u)*A_v"
                    "-conjugate(B_u)*B_v)"
                ),
                "p_nonzero_asymptotic_condition": "B=exp(i*theta)A",
                "p_zero_boundary_form": (
                    "-2*hbar^2*(conjugate(A_u)*B_v"
                    "-conjugate(B_u)*A_v)"
                ),
                "p_zero_asymptotic_condition": (
                    "B=lambda*A, lambda real projective"
                ),
                "actual_fiber_condition": (
                    "one real projective line in Wronskian boundary maps "
                    "Gamma_0,p and Gamma_1,p"
                ),
                "measurability_requirement": (
                    "Borel theta(p) plus a measurable field of boundary maps, "
                    "domains or resolvents, up to almost-everywhere equality"
                ),
                "conditional_p_preserving_recipe_only": True,
                "measurable_global_extension_constructed": False,
                "selected_fiber_boundary_line": None,
                "general_p_mixing_extension_classification": None,
                "p_zero_full_base_role": (
                    "Lebesgue-null unless a separate p=0 atom is declared"
                ),
            },
            "flags": flags,
        },
        flags,
    )


def numerical_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    mp.dps = NUMERICAL_DPS
    p_values = [mp.mpf(0), mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)]
    x_values = [mp.mpf("0.05"), mp.mpf(1), mp.mpf(8)]
    ode_residuals: list[mp.mpf] = []
    wronskian_errors: list[mp.mpf] = []
    rows: list[dict[str, str]] = []

    for p_value in p_values:
        order = 1j * mp.sqrt(mp.mpf(3) / 2) * abs(p_value)
        for x_value in x_values:
            functions: list[tuple[str, Callable[[mp.mpf], Any]]] = [
                ("I", lambda t, nu=order: mp.besseli(nu, t)),
                ("K", lambda t, nu=order: mp.besselk(nu, t)),
            ]
            values: dict[str, tuple[Any, Any]] = {}
            for label, function in functions:
                audit.bessel_function_samples += 1
                if audit.bessel_function_samples > BESSEL_FUNCTION_SAMPLE_CAP:
                    raise AssertionError("Bessel function sample cap exceeded")
                y = function(x_value)
                first = mp.diff(function, x_value, 1)
                second = mp.diff(function, x_value, 2)
                residual = (
                    x_value**2 * second
                    + x_value * first
                    - (x_value**2 + order**2) * y
                )
                scale = (
                    1
                    + abs(x_value**2 * second)
                    + abs(x_value * first)
                    + abs((x_value**2 + order**2) * y)
                )
                ode_residuals.append(abs(residual) / scale)
                values[label] = (y, first)
            wronskian = (
                values["I"][0] * values["K"][1]
                - values["I"][1] * values["K"][0]
            )
            wronskian_errors.append(abs(wronskian + 1 / x_value))
            audit.wronskian_reuse_points += 1
            rows.append(
                {
                    "p": decimal(p_value, 20),
                    "x": decimal(x_value, 20),
                    "normalized_I_residual": decimal(ode_residuals[-2]),
                    "normalized_K_residual": decimal(ode_residuals[-1]),
                    "I_K_wronskian_error": decimal(wronskian_errors[-1]),
                }
            )

    if audit.bessel_function_samples != BESSEL_FUNCTION_SAMPLE_CAP:
        raise AssertionError("Bessel sample count mutation")
    if audit.wronskian_reuse_points != len(p_values) * len(x_values):
        raise AssertionError("Wronskian reuse count mutation")

    ode_max = max(ode_residuals)
    wronskian_max = max(wronskian_errors)
    ode_tolerance = mp.mpf("1e-58")
    wronskian_tolerance = mp.mpf("1e-58")
    flags = {
        "bessel_equation": audit.observe_numeric_max(
            "G1.rawc.numeric.bessel_equation",
            ode_max,
            ode_tolerance,
            "I_(i*a) and K_(i*a) satisfy the transformed zero-energy modified-Bessel equation at all fixed p and x samples",
            len(ode_residuals),
        ),
        "bessel_wronskian": audit.observe_numeric_max(
            "G1.rawc.numeric.bessel_wronskian",
            wronskian_max,
            wronskian_tolerance,
            "the independent I/K evaluations satisfy W{I_nu,K_nu}=-1/x at all reused p and x samples",
            len(wronskian_errors),
        ),
    }
    return (
        {
            "precision_digits": NUMERICAL_DPS,
            "p_samples": [decimal(value, 20) for value in p_values],
            "x_samples": [decimal(value, 20) for value in x_values],
            "function_sample_count": audit.bessel_function_samples,
            "wronskian_reuse_point_count": audit.wronskian_reuse_points,
            "maximum_normalized_bessel_equation_residual": decimal(ode_max),
            "maximum_I_K_wronskian_error": decimal(wronskian_max),
            "rows": rows,
            "scope": (
                "independent finite-sample diagnostics of the exact Bessel "
                "reduction only; not a deficiency ODE solve or proof of Weyl "
                "classification"
            ),
        },
        flags,
    )


def write_result(path: Path, payload: dict[str, Any]) -> tuple[str, int]:
    payload["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(payload)
    )
    encoded = canonical_bytes(payload)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact byte cap exceeded")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> None:
    input_payload, input_sha, sources, upstream = load_input()
    audit = Audit()
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit)

    exact_pass = all(item["passed"] for item in audit.exact)
    numerical_pass = all(item["passed"] for item in audit.numerical)
    pass_all = exact_pass and numerical_pass
    if pass_all:
        verdict = (
            "NARROW_V0_RAW_C_CANDIDATE_HAS_FIBER_EXTENSION_DEBT_"
            "GLOBAL_MEASURABILITY_OPEN"
        )
        impact = (
            "KEEP_RAW_C_MINIMAL_FIBER_CLASSIFICATION_BUT_KILL_"
            "AUTOMATIC_C_H_EQUIVALENCE"
        )
    else:
        verdict = "KILL_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT"
        impact = "RETAIN_SELECTED_H_RESULTS_AND_REOPEN_THE_RAW_C_CANDIDATE_CHOICE"

    nulls = expected_nulls()
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {
            "path": INPUT_RELPATH,
            "sha256": input_sha,
            "numbered_phase": input_payload["numbered_phase"],
        },
        "repository_sources": sources,
        "upstream_results": upstream,
        "primary_sources": input_payload["primary_sources"],
        "declared_candidate": input_payload["declared_candidate"],
        "assumptions": input_payload["assumptions"],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": sum(item["passed"] for item in audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guard_count": len(audit.theorem_guards),
            "all_executable_checks_passed": pass_all,
        },
        "candidate_raw_C_operator_domain_family": {
            "minimal_operator": (
                "C_min=f^(-1)*H_hat on C_c^infinity in L2(f dQ dphi)"
            ),
            "fiber_endpoint_types": (
                "Q_minus_infinity limit-circle; Q_plus_infinity limit-point"
            ),
            "fiber_deficiency_indices": (
                "n_plus=n_minus=1 for every fixed p under theorem guards"
            ),
            "fixed_p_extensions": (
                "one real projective, equivalently U(1), boundary line per "
                "fixed p"
            ),
            "conditional_p_preserving_recipe": (
                "requires Borel theta(p) and a separately verified measurable "
                "field of boundary maps, domains or resolvents"
            ),
            "p_preserving_decomposable_extension_constructed": False,
            "selected_fiber_extension": None,
            "general_full_extension_classification": None,
            "physical_interpretation": None,
        },
        "required_fail_closed_outputs": nulls,
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "bessel_function_samples": audit.bessel_function_samples,
            "wronskian_reuse_points": audit.wronskian_reuse_points,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "mpmath": mpmath.__version__,
        },
        "audit_flags": {
            "exact": exact_flags,
            "numerical": numerical_flags,
        },
    }
    outer_sha, size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "programme_impact": impact,
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "numerical_passed": result["check_summary"]["numerical_passed"],
                "numerical_total": result["check_summary"]["numerical_total"],
                "theorem_guard_count": result["check_summary"][
                    "theorem_guard_count"
                ],
                "result_sha256": outer_sha,
                "result_size_bytes": size,
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
