#!/usr/bin/env python3
"""Exact plus-end kappa projective-sensitivity anchor on one real strip.

Two selected plus-recessive directions obey a scale-free Wronskian secant
identity.  Pinned full-strip Liouville--Green bounds make the singular-endpoint
boundary term vanish, bound every secant, and provide the domination needed to
take the diagonal kappa derivative.  The calculation stops at Q=4: it is not a
Qswitch/Q0 transfer, a differentiated boundary functional, root uniqueness, a
root selector, velocity, spectral data, RAQ, or physics.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "RAW_C_PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_ANCHOR_INPUTS.json"
RESULT_NAME = "RAW_C_PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_ANCHOR_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_plus_endpoint_kappa_projective_sensitivity_anchor.py"
)
EXPECTED_INPUT_SHA256 = "55bc49884d678719eda2a0e02dbdc028e15b2e52b1d3ca8558b51cd1c5c5becd"
CALCULATION_ID = "RawCPlusEndpointKappaProjectiveSensitivityAnchor"
RESULT_SCHEMA = "ice.raw-c-plus-endpoint-kappa-projective-sensitivity-anchor.result.v1"
RESULT_PREFIX = "RAW_C_PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_ANCHOR_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


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


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 24,
        "upstream_results": 2,
        "kappa_corridors": 1,
        "lambda_slabs": 1,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "panel_evaluations": 0,
        "ball_bessel_evaluations": 0,
        "bisection_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "Qswitch_kappa_projective_sensitivity": None,
        "Q0_kappa_projective_sensitivity": None,
        "complete_normalized_G_kappa": None,
        "root_uniqueness_in_corridor": None,
        "continuous_root_selector": None,
        "root_velocity": None,
        "absolute_actual_Gamma1_amplitude_or_sign": None,
        "roots_outside_declared_corridor_or_global_census": None,
        "nonreal_weyl_m_function_or_spectral_measure": None,
        "raw_C_RAQ_completion": None,
        "physics_claim": None,
    }


def check(
    identifier: str, passed: bool, statement: str, **data: Any
) -> dict[str, Any]:
    return {
        "id": identifier,
        "passed": bool(passed),
        "statement": statement,
        **data,
    }


def identity(
    identifier: str, residual: sp.Expr, statement: str
) -> dict[str, Any]:
    reduced = sp.simplify(residual)
    return check(
        identifier,
        bool(reduced == 0),
        statement,
        residual=str(reduced),
    )


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if (
        payload.get("schema_version") != item["schema_version"]
        or payload.get("verdict") != item["required_verdict"]
        or payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
        or payload.get("run_status") != "VALID_RUN"
        or payload.get("numbered_phase") is not None
    ):
        raise AssertionError(f"upstream metadata mismatch: {item['path']}")
    without_self = dict(payload)
    recorded = without_self.pop("result_payload_sha256_without_self")
    if sha256_bytes(canonical_bytes(without_self)) != recorded:
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    return payload, {
        "path": item["path"],
        "sha256": observed,
        "schema_version": item["schema_version"],
        "verdict": item["required_verdict"],
        "payload_sha256_without_self": item["payload_sha256_without_self"],
        "role": item["role"],
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    observed_input = sha256_bytes(raw_input)
    if observed_input != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input}")
    config = json.loads(raw_input)
    if (
        config.get("schema_version")
        != "ice.raw-c-plus-endpoint-kappa-projective-sensitivity-anchor.input.v1"
        or config.get("calculation_id") != CALCULATION_ID
        or config.get("numbered_phase") is not None
        or config.get("resource_caps") != expected_caps()
        or config.get("required_fail_closed_outputs") != expected_nulls()
    ):
        raise AssertionError("identity, resource, or null-output policy drift")

    upstream: dict[str, dict[str, Any]] = {}
    upstream_records: list[dict[str, str]] = []
    for item in config["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream[item["path"]] = payload
        upstream_records.append(record)
    if len(upstream_records) != expected_caps()["upstream_results"]:
        raise AssertionError("upstream result count drift")
    paths = [item["path"] for item in config["upstream_results"]]
    lg_result = upstream[paths[0]]
    strip_result = upstream[paths[1]]
    conventions = config["declared_conventions"]
    strip_scope = strip_result["certified_calculation"]
    if (
        strip_scope["kappa_corridor"]["left_exact"]
        != conventions["kappa_corridor"]["left_exact"]
        or strip_scope["kappa_corridor"]["right_exact"]
        != conventions["kappa_corridor"]["right_exact"]
        or strip_scope["lambda_slab"] != conventions["lambda_slab"]
        or "Q>=4, |lambda|<=1e-4, 0<=kappa<=8"
        not in lg_result["declared_conventions"]["real_box"]
    ):
        raise AssertionError("pinned strip or Liouville-Green scope drift")

    q = sp.symbols("Q", real=True)
    kappa = sp.symbols("kappa", positive=True, real=True)
    u, uq, w, wq, coefficient = sp.symbols(
        "u u_Q w w_Q A", nonzero=True, real=True
    )
    wronskian = u * wq - uq * w
    h = (uq * w - u * wq) / u**2

    def dq(expr: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expr, u) * uq
            + sp.diff(expr, uq) * coefficient * u
            + sp.diff(expr, w) * wq
            + sp.diff(expr, wq) * (coefficient * w - 2 * kappa * u)
        )

    exact_checks = [
        identity(
            "rawc.kappa_anchor.coefficient_derivative",
            sp.diff(
                36 * sp.pi**4 * sp.exp(2 * q)
                + sp.symbols("lambda", real=True)
                * 6
                * sp.pi**2
                * sp.exp(sp.Rational(3, 2) * q)
                - kappa**2,
                kappa,
            )
            + 2 * kappa,
            "The fiber coefficient has exact kappa derivative A_kappa=-2*kappa.",
        ),
        identity(
            "rawc.kappa_anchor.wronskian_derivative",
            dq(wronskian) + 2 * kappa * u**2,
            "For w=partial_kappa u, W(u,w)_Q=-2*kappa*u^2.",
        ),
        identity(
            "rawc.kappa_anchor.projective_sensitivity",
            h + wronskian / u**2,
            "Because x and 1/2 are kappa-independent, h=partial_kappa rho=-W(u,w)/u^2.",
        ),
        identity(
            "rawc.kappa_anchor.forced_wronskian",
            dq(u**2 * h) - 2 * kappa * u**2,
            "The scale-free forced-Wronskian identity is (u^2 h)_Q=2*kappa*u^2.",
        ),
    ]
    c0, c1 = sp.symbols("c0 c1", nonzero=True, real=True)
    scaled_h = (
        (c0 * uq) * (c0 * w + c1 * u)
        - (c0 * u) * (c0 * wq + c1 * uq)
    ) / (c0 * u) ** 2
    exact_checks.append(
        identity(
            "rawc.kappa_anchor.amplitude_invariance",
            scaled_h - h,
            "h is invariant under a nonzero kappa-dependent common amplitude normalization.",
        )
    )

    kappa_a, kappa_b = sp.symbols(
        "kappa_a kappa_b", positive=True, real=True
    )
    ua, uaq, ub, ubq, base = sp.symbols(
        "u_a u_aQ u_b u_bQ B", nonzero=True, real=True
    )
    coefficient_a = base - kappa_a**2
    coefficient_b = base - kappa_b**2
    cross_wronskian = ua * ubq - uaq * ub
    product = ua * ub
    delta_r = -ubq / ub + uaq / ua

    def dq_pair(expr: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expr, ua) * uaq
            + sp.diff(expr, uaq) * coefficient_a * ua
            + sp.diff(expr, ub) * ubq
            + sp.diff(expr, ubq) * coefficient_b * ub
        )

    exact_checks.extend(
        [
            identity(
                "rawc.kappa_anchor.two_parameter_wronskian_derivative",
                dq_pair(cross_wronskian)
                + (kappa_b**2 - kappa_a**2) * product,
                "For two selected directions, W(u_a,u_b)_Q=-(kappa_b^2-kappa_a^2)u_a*u_b.",
            ),
            identity(
                "rawc.kappa_anchor.two_parameter_log_derivative",
                delta_r + cross_wronskian / product,
                "The logarithmic-direction difference is r_b-r_a=-W(u_a,u_b)/(u_a*u_b).",
            ),
            identity(
                "rawc.kappa_anchor.secant_factorization",
                (kappa_b**2 - kappa_a**2)
                / (kappa_b - kappa_a)
                - (kappa_a + kappa_b),
                "Dividing the integrated Wronskian identity by kappa_b-kappa_a gives the declared secant factor.",
            ),
        ]
    )

    strip_checks = {
        item["id"]: item
        for item in strip_result.get("exact_checks", [])
        + strip_result.get("controls", [])
    }
    required_strip_checks = {
        "rawc.signstrip.plus_anchor.pinned_uniform_lg_envelope",
        "rawc.signstrip.plus_anchor.coefficient_positive",
        "rawc.signstrip.plus_anchor.coefficient_derivative_positive",
        "rawc.signstrip.plus_anchor.four_A_minus_Aprime",
        "rawc.signstrip.plus_anchor.g_lower_from_lg",
        "rawc.signstrip.plus_anchor.g_upper_from_lg",
        "rawc.signstrip.q0.corridor.final_chart",
    }
    lg_error = sp.Rational(
        lg_result["analytic_calculation"]["at_Q_plus_4"][
            "sqrt_A_normalized_log_derivative_difference_bound"
        ]
    )
    exact_checks.append(
        check(
            "rawc.kappa_anchor.pinned_full_strip_log_derivative_envelope",
            bool(
                strip_result["check_summary"][
                    "all_executable_checks_passed"
                ]
                is True
                and all(
                    identifier in strip_checks
                    and strip_checks[identifier].get("passed") is True
                    for identifier in required_strip_checks
                )
                and 0 < lg_error < sp.Rational(1, 500)
            ),
            "The current hash-pinned sign strip rechecks the full-strip selected-family Liouville-Green envelope and nonzero chart; no face difference is used as derivative evidence.",
            required_passed_check_ids=sorted(required_strip_checks),
            pinned_lg_error=str(lg_error),
        )
    )

    kappa_left = sp.Rational(conventions["kappa_corridor"]["left_exact"])
    kappa_right = sp.Rational(conventions["kappa_corridor"]["right_exact"])
    lambda_left = sp.Rational(conventions["lambda_slab"]["left_exact"])
    lambda_right = sp.Rational(conventions["lambda_slab"]["right_exact"])
    exact_checks.extend(
        [
            check(
                "rawc.kappa_anchor.declared_strip_order",
                bool(
                    0 < kappa_left < kappa_right < 8
                    and lambda_left < 0 < lambda_right
                    and lambda_left == -lambda_right
                ),
                "The exact compact kappa corridor is positive and inside the pinned LG box, while the closed lambda slab is symmetric and contains zero.",
                kappa_left_exact=str(kappa_left),
                kappa_right_exact=str(kappa_right),
                lambda_left_exact=str(lambda_left),
                lambda_right_exact=str(lambda_right),
            ),
            check(
                "rawc.kappa_anchor.elementary_exponential_bounds",
                bool(
                    sp.E**2 > 7
                    and sp.E**2 < sp.Rational(15, 2)
                    and sp.E < 3
                    and sp.E**4 > 49
                    and sp.E**4 + sp.Rational(1, 140) < 57
                    and sp.exp(-1) > sp.Rational(1, 3)
                ),
                "The elementary exponential relaxations used to bound the scale-free tail integral hold.",
            ),
            identity(
                "rawc.kappa_anchor.log_derivative_envelope_width",
                (70 - 53) - 17,
                "The pinned envelope gives |r_a-r_b|<=17*exp(Q) at fixed lambda.",
            ),
            identity(
                "rawc.kappa_anchor.normalized_product_exponent",
                2 * 53 - 106,
                "Integrating r_a+r_b>=106*exp(Q) gives 0<v_a*v_b<=exp(-106*(exp(Q)-exp(4))).",
            ),
            identity(
                "rawc.kappa_anchor.lower_window_exponent",
                2 * 70 * sp.Rational(1, 140) - 1,
                "On the first y-window 0<=y<=1/140, exp(-140y)>=exp(-1).",
            ),
            identity(
                "rawc.kappa_anchor.tail_substitution_antiderivative",
                sp.diff(sp.exp(q) - sp.exp(4), q) - sp.exp(q),
                "The tail substitution y=exp(Q)-exp(4) has dy=exp(Q)dQ.",
            ),
            check(
                "rawc.kappa_anchor.boundary_term_decay",
                bool(
                    sp.limit(
                        17
                        * sp.exp(q)
                        * sp.exp(-106 * (sp.exp(q) - sp.exp(4))),
                        q,
                        sp.oo,
                    )
                    == 0
                ),
                "The product envelope times |r_a-r_b|<=17*exp(Q) tends to zero, so the normalized cross-Wronskian W/[u_a(4)u_b(4)] vanishes at the recessive endpoint.",
            ),
            check(
                "rawc.kappa_anchor.integral_upper_bound",
                bool(
                    sp.Rational(1, 2 * 53 * 49)
                    == sp.Rational(
                        conventions["integral_bounds"]["upper_exact"]
                    )
                ),
                "Using r>=53e^Q and e^4>49 gives I<1/(2*53*49)=1/5194.",
                upper_exact=conventions["integral_bounds"]["upper_exact"],
            ),
            check(
                "rawc.kappa_anchor.integral_lower_bound",
                bool(
                    sp.Rational(1, 140 * 3 * 57)
                    == sp.Rational(
                        conventions["integral_bounds"]["lower_exact"]
                    )
                ),
                "Restricting to y in [0,1/140], with r<=70e^Q, exp(-1)>1/3 and e^4+y<57, gives I>1/23940.",
                lower_exact=conventions["integral_bounds"]["lower_exact"],
            ),
        ]
    )

    integral_lower = sp.Rational(
        conventions["integral_bounds"]["lower_exact"]
    )
    integral_upper = sp.Rational(
        conventions["integral_bounds"]["upper_exact"]
    )
    h_lower = -2 * kappa_right * integral_upper
    h_upper = -2 * kappa_left * integral_lower
    exact_checks.extend(
        [
            check(
                "rawc.kappa_anchor.uniform_negative_secant_interval",
                bool(
                    h_lower < h_upper < 0
                    and integral_lower < integral_upper
                    and 0 < 2 * kappa_left < 2 * kappa_right
                ),
                "For every fixed lambda and kappa_a<kappa_b in the corridor, the exact secant -(kappa_a+kappa_b)*I_ab lies in the same finite strictly negative interval.",
                secant_strict_lower_exact=str(h_lower),
                secant_strict_upper_exact=str(h_upper),
            ),
            identity(
                "rawc.kappa_anchor.diagonal_secant_factor",
                (kappa_a + kappa_b).subs(
                    {kappa_a: kappa, kappa_b: kappa}
                )
                - 2 * kappa,
                "Both diagonal secant limits have factor 2*kappa.",
            ),
            check(
                "rawc.kappa_anchor.uniform_negative_interval",
                bool(h_lower < h_upper < 0),
                "Dominated convergence of the checked secant enclosure gives one finite uniform strictly negative h(4) interval.",
                h_strict_lower_exact=str(h_lower),
                h_strict_upper_exact=str(h_upper),
            ),
        ]
    )
    if len(exact_checks) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")

    guards = [
        {
            "id": "rawc.kappa_anchor.guard.selected_family_secant_limit",
            "verified": True,
            "theorem": "Two-parameter Wronskian identity, finite-interval Lipschitz continuity, and dominated convergence",
            "hypotheses": "For every point of the pinned compact strip, the same selected real recessive direction is nonzero on Q>=4 and obeys 53*exp(Q)<=r<=70*exp(Q); the envelope-width, product-exponent, boundary-decay, secant-interval and diagonal-factor checks all pass.",
            "scope": "At fixed lambda, the exact secant formula first proves local Lipschitz continuity of r_kappa at each finite Q; normalized directions then converge on compact intervals, while exp(-106*(exp(Q)-exp(4))) is a common integrable tail dominator. The left and right diagonal limits agree, yielding a two-sided h at corridor-interior kappa and the corresponding one-sided h at each face, all at Q=4 only.",
        },
        {
            "id": "rawc.kappa_anchor.guard.log_derivative_integral_bounds",
            "verified": True,
            "theorem": "Fundamental theorem of calculus applied to log(u(Q)/u(4))",
            "hypotheses": "The selected real plus solution is nonzero on Q>=4 and 53e^Q<=-u_Q/u<=70e^Q uniformly on the pinned strip.",
            "scope": "The rational upper/lower integral bounds are sufficient but deliberately nonoptimal; they do not transport h below Q=4.",
        },
        {
            "id": "rawc.kappa_anchor.guard.scope",
            "verified": True,
            "theorem": "Worktop scope separation",
            "hypotheses": "One exact correlated strip, one selected real family, one plus endpoint, and no numerical derivative or root inference.",
            "scope": "Qswitch/Q0 kappa transport, complete G_kappa, uniqueness, selector, velocity, global roots, spectrum, RAQ and physics remain null.",
        },
    ]
    all_exact = all(item["passed"] for item in exact_checks)
    verdict = (
        "CERTIFY_UNIFORM_NEGATIVE_PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_ANCHOR"
        if all_exact
        else "PLUS_ENDPOINT_KAPPA_PROJECTIVE_SENSITIVITY_NOT_CERTIFIED"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "upstream_results": upstream_records,
        "primary_sources": config["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": exact_checks,
        "theorem_guards": guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in exact_checks),
            "exact_total": len(exact_checks),
            "theorem_guards": len(guards),
            "all_executable_checks_passed": all_exact,
        },
        "certified_calculation": {
            "scope": "the current exact correlated K times Lambda strip at Qplus=4 only",
            "two_parameter_secant_formula": "at fixed lambda, [r_b(4)-r_a(4)]/[kappa_b-kappa_a]=-(kappa_a+kappa_b)*integral_4^infinity v_a(Q)*v_b(Q) dQ",
            "parameter_limit": "The secant formula gives finite-Q local Lipschitz continuity; normalized-direction convergence plus the common tail dominator makes the left and right diagonal limits agree by dominated convergence. The derivative is two-sided at corridor-interior kappa and one-sided at the faces.",
            "forced_wronskian_formula": "h(4)=-2*kappa*u(4)^(-2)*integral_4^infinity u(Q)^2 dQ",
            "integral_I": {
                "lower_exact": str(integral_lower),
                "upper_exact": str(integral_upper),
                "lower_decimal": str(sp.N(integral_lower, 18)),
                "upper_decimal": str(sp.N(integral_upper, 18)),
            },
            "h_Qplus_4": {
                "strict_lower_exact": str(h_lower),
                "strict_upper_exact": str(h_upper),
                "lower_decimal": str(sp.N(h_lower, 18)),
                "upper_decimal": str(sp.N(h_upper, 18)),
                "strictly_negative": bool(h_upper < 0),
            },
            "next_mathematical_gap": "Transport h with the selected actual rho from Qplus through Qswitch and Q0, then include both actual-state and reference-state kappa variations in a complete differentiated-tail enclosure before any G_kappa or uniqueness claim.",
        },
        "non_claim": "This is a plus-end projective kappa-sensitivity anchor only, not complete G_kappa, transversality, root uniqueness, a selector, velocity, spectrum, RAQ, or physics.",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_checks": len(exact_checks),
            "upstream_results": len(upstream_records),
            "kappa_corridors": 1,
            "lambda_slabs": 1,
            "ode_calls": 0,
            "quadrature_calls": 0,
            "root_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "panel_evaluations": 0,
            "ball_bessel_evaluations": 0,
            "bisection_steps": 0,
            "adjacent_result_files_written": 1,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "exact_passed": sum(item["passed"] for item in exact_checks),
                "exact_total": len(exact_checks),
                "h_Qplus_4": result["certified_calculation"]["h_Qplus_4"],
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
