#!/usr/bin/env python3
"""Real raw-C plus-tail Liouville--Green bound; not endpoint transport or RAQ."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_INPUTS.json"
RESULT_NAME = "RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_plus_endpoint_liouville_green_tail_bound.py"
EXPECTED_INPUT_SHA256 = "f9245b6615e7cf2c00b072c0112da1632a10dd711984ed3f8c7ce36ffb649dc8"
CALCULATION_ID = "RawCPlusEndpointLiouvilleGreenTailBound"
RESULT_SCHEMA = "ice.raw-c-plus-endpoint-liouville-green-tail-bound.result.v1"
RESULT_PREFIX = "RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def expected_nulls() -> dict[str, Any]:
    return {"validated_Qplus_to_Q0_transport": None, "exact_plus_endpoint_to_Q0_boundary_transform": None, "endpoint_F_or_F_lambda": None, "nonreal_resolvent_or_weyl_m_function": None, "raw_C_spectral_measure": None, "global_delta_C_measure": None, "raw_C_rigging_test_space": None, "raw_C_rigging_map": None, "raw_C_physical_inner_product": None, "raw_C_RAQ_completion": None, "quantum_constraint_rescaling_equivalence": None, "selected_H_raw_C_unitary_intertwiner": None, "general_p_mixing_extension_classification": None, "canonical_p_zero_origin_sector": None, "absolute_bfv_measure": None, "continuum_determinant_or_pfaffian_line": None, "inhomogeneous_constraint_closure": None, "quantum_bfv_anomaly_freedom": None, "relational_observables_or_decoherence": None, "empirical_likelihood": None, "quantum_gravity_claim": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "symbolic_operations": 1000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "sampling_points": 0, "automatic_descendants": 0}


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def identity(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self.register(ident)
        simplified = sp.simplify(residual)
        self.exact.append({"id": ident, "passed": bool(simplified == 0), "statement": statement, "residual": str(simplified)})

    def inequality(self, ident: str, relation: bool, statement: str, **data: str) -> None:
        self.register(ident)
        self.exact.append({"id": ident, "passed": bool(relation), "statement": statement, **data})

    def guard(self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        self.register(ident)
        self.theorem_guards.append({"id": ident, "verified": True, "verification_mode": "SOURCE_PIN_PLUS_ANALYTIC_HYPOTHESIS_SCOPE_AUDIT_NOT_AN_ENDPOINT_TO_BOUNDARY_TRANSPORT_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    if sha256_bytes(raw) != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key, expected in (("run_status", "VALID_RUN"), ("verdict", item["required_verdict"]), ("result_payload_sha256_without_self", item["payload_sha256_without_self"])):
        if result.get(key) != expected:
            raise AssertionError(f"upstream {key} mismatch: {item['path']}")
    return {"path": item["path"], "sha256": item["sha256"], "payload_sha256_without_self": item["payload_sha256_without_self"], "verdict": item["required_verdict"]}


def as_decimal(expr: sp.Expr, digits: int = 18) -> str:
    return str(sp.N(expr, digits))


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.raw-c-plus-endpoint-liouville-green-tail-bound.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("resource cap or fail-closed mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in cfg["upstream_results"]]

    audit = Audit()
    Q, kappa, lam = sp.symbols("Q kappa lambda", real=True)
    pi = sp.pi
    A0 = 36 * pi**4 * sp.exp(2 * Q)
    lambda_term = lam * sp.exp(-Q / 2) / (6 * pi**2)
    kappa_term = kappa**2 * sp.exp(-2 * Q) / (36 * pi**4)
    relative_delta = lambda_term - kappa_term
    relative_factor = 1 + relative_delta
    A = sp.expand(A0 * relative_factor)
    expected_A = 36 * pi**4 * sp.exp(2 * Q) + 6 * pi**2 * lam * sp.exp(sp.Rational(3, 2) * Q) - kappa**2
    r = sp.simplify(5 * sp.diff(A, Q)**2 / (16 * A**2) - sp.diff(A, Q, 2) / (4 * A))
    relative_log_derivative = sp.diff(relative_factor, Q) / relative_factor
    factored_r = sp.Rational(1, 4) + relative_log_derivative / 4 + 5 * relative_log_derivative**2 / 16 - sp.diff(relative_factor, Q, 2) / (4 * relative_factor)
    log_w_prime = -sp.sqrt(A) - sp.diff(A, Q) / (4 * A)
    w_residual = sp.simplify(sp.diff(log_w_prime, Q) + log_w_prime**2 - A - r)
    positive_A = sp.symbols("positive_A", positive=True)
    A_prime, A_second = sp.symbols("A_prime A_second", real=True)
    amplitude = positive_A ** (-sp.Rational(1, 4))
    amplitude_second = sp.diff(amplitude, positive_A, 2) * A_prime**2 + sp.diff(amplitude, positive_A) * A_second
    dlmf_control_integrand = positive_A ** (-sp.Rational(1, 4)) * amplitude_second
    generic_r_over_sqrt_A = (5 * A_prime**2 / (16 * positive_A**2) - A_second / (4 * positive_A)) / sp.sqrt(positive_A)
    audit.identity("rawc.lg.coefficient", A - expected_A, "The p=sqrt(2/3)kappa raw-C real fiber coefficient is exactly the declared A.")
    audit.identity("rawc.lg.relative_delta", relative_delta - (lambda_term - kappa_term), "The relative factor is 1+delta with the declared lambda and kappa terms.")
    audit.identity("rawc.lg.relative_delta_prime", sp.diff(relative_delta, Q) - (-lambda_term / 2 + 2 * kappa_term), "The exact first derivative of delta fixes the derivative envelope coefficients.")
    audit.identity("rawc.lg.relative_delta_second", sp.diff(relative_delta, Q, 2) - (lambda_term / 4 - 4 * kappa_term), "The exact second derivative of delta fixes the second-derivative envelope coefficients.")
    audit.identity("rawc.lg.wkb_residual", w_residual, "For w=A^(-1/4) exp(-integral sqrt(A)dQ), w''/w-A equals the declared Liouville-Green residual r.")
    audit.identity("rawc.lg.factored_residual", r - factored_r, "The residual has the exact factored A=A0*(1+delta) form used for uniform bounds.")
    audit.identity("rawc.lg.dlmf_control_integrand", dlmf_control_integrand - generic_r_over_sqrt_A, "For a positive coefficient, the chain rule gives A^(-1/4)(A^(-1/4))''=r/sqrt(A), which is the f_DLMF=A, g_DLMF=0 error-control integrand.")
    audit.identity("rawc.lg.lambda_kappa_zero_baseline", sp.simplify(r.subs({lam: 0, kappa: 0}) - sp.Rational(1, 4)), "The pure lambda=kappa=0, A0=36*pi^4*exp(2Q) baseline residual is exactly 1/4.")
    baseline_control_integrand = sp.exp(-Q) / (24 * pi**2)
    baseline_tail_from_Q = sp.exp(-Q) / (24 * pi**2)
    audit.identity(
        "rawc.lg.lambda_kappa_zero_control_integrand",
        sp.simplify(
            r.subs({lam: 0, kappa: 0})
            / (6 * pi**2 * sp.exp(Q))
            - baseline_control_integrand
        ),
        "For lambda=kappa=0, the DLMF error-control integrand r/sqrt(A0) is exp(-Q)/(24*pi^2).",
    )
    audit.identity(
        "rawc.lg.lambda_kappa_zero_tail_antiderivative",
        sp.diff(baseline_tail_from_Q, Q) + baseline_control_integrand,
        "The exact lambda=kappa=0 tail variation from Q to infinity is exp(-Q)/(24*pi^2).",
    )

    # These rational envelopes apply uniformly on Q>=4.  They use only pi>3 and exp(2)>7.
    eta = sp.Rational(1, 100000)
    b_kappa = sp.Rational(64, 36 * 3**4 * 7**4)
    b_lambda = sp.Rational(1, 10000 * 6 * 3**2 * 7)
    lambda_shape = sp.exp(-Q / 2) / (6 * pi**2)
    kappa_shape = sp.exp(-2 * Q) / (36 * pi**4)
    lambda_corner_exact = sp.Rational(1, 10000) * lambda_shape.subs(Q, 4)
    kappa_corner_exact = 64 * kappa_shape.subs(Q, 4)
    d0 = b_kappa + b_lambda
    d1 = 2 * b_kappa + b_lambda / 2
    d2 = 4 * b_kappa + b_lambda / 4
    Rbar = sp.Rational(1, 4) + 3 * eta / (2 * (1 - eta)) + 5 * eta**2 / (4 * (1 - eta)**2)
    residual_envelope_from_triangle = (
        sp.Rational(1, 4)
        + (2 * eta) / (4 * (1 - eta))
        + 5 * (2 * eta) ** 2 / (16 * (1 - eta) ** 2)
        + (4 * eta) / (4 * (1 - eta))
    )
    V_analytic_upper = Rbar * sp.exp(-4) / (6 * pi**2 * sp.sqrt(1 - eta))
    V_elementary_bar = sp.simplify(Rbar / (6 * 9 * 7**2 * (1 - eta)))
    E_error_bar = sp.exp(V_elementary_bar / 2) - 1
    normalized_log_derivative_difference_bound = 2 * E_error_bar / (1 - E_error_bar)

    audit.identity("rawc.lg.lambda_shape_monotone", sp.diff(lambda_shape, Q) + lambda_shape / 2, "The positive lambda envelope shape decreases as exp(-Q/2) on Q>=4.")
    audit.identity("rawc.lg.kappa_shape_monotone", sp.diff(kappa_shape, Q) + 2 * kappa_shape, "The positive kappa envelope shape decreases as exp(-2Q) on Q>=4.")
    audit.inequality("rawc.lg.lambda_corner_lt_rational", bool(lambda_corner_exact < b_lambda), "At Q=4, |lambda|<=1e-4 is bounded by the declared rational b_lambda using pi>3 and exp(2)>7.", exact_corner=as_decimal(lambda_corner_exact), rational_bound=as_decimal(b_lambda))
    audit.inequality("rawc.lg.kappa_corner_lt_rational", bool(kappa_corner_exact < b_kappa), "At Q=4, kappa^2<=64 is bounded by the declared rational b_kappa using pi>3 and exp(8)>7^4.", exact_corner=as_decimal(kappa_corner_exact), rational_bound=as_decimal(b_kappa))
    audit.inequality("rawc.lg.d0_lt_eta", bool(d0 < eta), "The elementary bound d0 for |delta| is strictly below eta_bar.", d0=as_decimal(d0), eta_bar=as_decimal(eta))
    audit.inequality("rawc.lg.d1_le_2eta", bool(d1 <= 2 * eta), "The elementary bound d1 for |delta'| is at most 2 eta_bar.", d1=as_decimal(d1), two_eta_bar=as_decimal(2 * eta))
    audit.inequality("rawc.lg.d2_le_4eta", bool(d2 <= 4 * eta), "The elementary bound d2 for |delta''| is at most 4 eta_bar.", d2=as_decimal(d2), four_eta_bar=as_decimal(4 * eta))
    audit.inequality("rawc.lg.positivity", bool(1 - eta > 0), "Because |delta|<eta_bar<1, A=A0*(1+delta) is uniformly positive throughout the declared real tail box.", lower_relative_factor=as_decimal(1 - eta))
    audit.identity("rawc.lg.residual_envelope_algebra", Rbar - residual_envelope_from_triangle, "The triangle envelope from |delta'|<=2eta_bar, |delta''|<=4eta_bar and 1+delta>=1-eta_bar is exactly R_bar.")
    audit.inequality("rawc.lg.residual_bound_sanity", bool(Rbar > sp.Rational(1, 4)), "The uniform R_bar is a conservative perturbation of the exact lambda=kappa=0 residual 1/4.", R_bar=as_decimal(Rbar))
    audit.inequality("rawc.lg.tail_expression_le_elementary", bool(V_analytic_upper < V_elementary_bar), "The analytic tail-variation upper bound is bounded by the elementary V_bar using exp(-4)<1/7^2, pi^2>9, and 1/sqrt(1-eta)<=1/(1-eta).", V_analytic_upper=as_decimal(V_analytic_upper), V_bar=as_decimal(V_elementary_bar))
    audit.inequality("rawc.lg.error_budget_small", bool(E_error_bar < sp.Rational(1, 10000)), "The DLMF relative-amplitude error bound E_bar=exp(V_bar/2)-1 is below 1e-4 and therefore has 1-E_bar>0.", E_bar=as_decimal(E_error_bar), normalized_log_derivative_difference_bound=as_decimal(normalized_log_derivative_difference_bound))

    audit.guard("rawc.lg.guard.elementary_relaxations", "Elementary constant and monotonic exponential bounds", "pi>3, exp(2)>7, and exp(-Q/2), exp(-2Q) decrease for Q>=4", "These facts turn the declared compact real parameter box into the rational d0, d1 and d2 envelopes. They are sufficient rather than optimized bounds.")
    audit.guard("rawc.lg.guard.dlmf_2_7_23_25", "DLMF §2.7(iii), equations 2.7.23--2.7.25 (Liouville--Green error bounds including the derivative clause)", "On Q>=4, A is real C-infinity and uniformly positive by the exact coefficient and eta_bar audit; A^(-1/4)(A^(-1/4))''=r/sqrt(A), whose total variation is bounded by finite V_bar.", "For the recessive solution with the theorem's asymptotic normalization on this positive real tail only, |epsilon| and (1/2)A^(-1/2)|epsilon'| are bounded by exp(V_bar/2)-1. The recorded 2E_bar/(1-E_bar) bounds |(log u)'-(log w)'|/sqrt(A); it is not a relative error against (log w)'. It is also not a Q=4-to-Q0 transport, an F or F_lambda calculation, a nonreal m-function, a spectral measure, or RAQ.")
    audit.guard("rawc.lg.guard.no_hidden_transport", "endpoint-to-boundary propagation requirement", "The calculation has zero ODE calls and no validated interval/ball enclosure or transfer-matrix proof between Q=4 and Q0=-4.", "No endpoint F/F_lambda, boundary datum, spectral quantity, or C/H equivalence may be inferred from this tail bound.")

    passed = all(item["passed"] for item in audit.exact)
    verdict = "KEEP_REAL_RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_ONLY" if passed else "KILL_REAL_RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND"
    impact = cfg["decision_table"][0 if passed else 1]["programme_impact"]
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)}, "upstream_results": upstream, "primary_sources": cfg["primary_sources"], "declared_conventions": cfg["declared_conventions"], "assumptions": cfg["assumptions"], "exact_checks": audit.exact, "theorem_guards": audit.theorem_guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "theorem_guard_count": len(audit.theorem_guards), "all_executable_checks_passed": passed}, "analytic_calculation": {"uniform_envelopes": {"eta_bar": str(eta), "b_kappa": str(b_kappa), "b_lambda": str(b_lambda), "d0": str(d0), "d1": str(d1), "d2": str(d2), "R_bar": str(Rbar)}, "at_Q_plus_4": {"lambda_kappa_zero_tail_variation_exact": str(sp.exp(-4) / (24 * pi**2)), "lambda_kappa_zero_tail_variation_decimal": as_decimal(sp.exp(-4) / (24 * pi**2)), "V_analytic_upper": as_decimal(V_analytic_upper), "V_bar_elementary": as_decimal(V_elementary_bar), "E_bar": as_decimal(E_error_bar), "sqrt_A_normalized_log_derivative_difference_bound": as_decimal(normalized_log_derivative_difference_bound)}, "scope": "uniform real plus-end Liouville-Green tail bound only"}, "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"symbolic_operations_cap": cfg["resource_caps"]["symbolic_operations"], "root_calls": 0, "quadratures": 0, "ode_calls": 0, "sampling_points": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "sympy": sp.__version__}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded), "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
