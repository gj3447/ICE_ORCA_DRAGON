#!/usr/bin/env python3
"""Certify lambda-zero raw-C h(4) tail boxes; not endpoint F_lambda or RAQ."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = "RAW_C_LAMBDA_ZERO_DIFFERENTIATED_PLUS_TAIL_INPUTS.json"
RESULT_NAME = "RAW_C_LAMBDA_ZERO_DIFFERENTIATED_PLUS_TAIL_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/raw_c_lambda_zero_differentiated_plus_tail.py"
)
EXPECTED_INPUT_SHA256 = (
    "91e8cb4ffcc8a310b6aebfddff508a70574907901cfb71a7d0807e6567c7f691"
)
CALCULATION_ID = "RawCLambdaZeroDifferentiatedPlusTail"
RESULT_SCHEMA = "ice.raw-c-lambda-zero-differentiated-plus-tail.result.v1"
RESULT_PREFIX = "RAW_C_LAMBDA_ZERO_DIFFERENTIATED_PLUS_TAIL_RESULT="
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


def expected_nulls() -> dict[str, Any]:
    return {
        "nonzero_lambda_differentiated_tail": None,
        "node_safe_Qplus_to_Q0_transport": None,
        "endpoint_F_lambda_amplitude": None,
        "endpoint_root_velocity": None,
        "unique_or_complete_zero_shell_root_census": None,
        "nonreal_resolvent_or_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "absolute_bfv_measure": None,
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


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 1000,
        "ball_bessel_evaluations": 100000,
        "quadrature_calls": 10,
        "quadrature_callback_evaluations": 100000,
        "root_brackets": 5,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    ball: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0
    quadrature_calls: int = 0
    quadrature_callback_evaluations: int = 0

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def identity(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self.register(ident)
        simplified = sp.simplify(residual)
        self.exact.append(
            {
                "id": ident,
                "passed": bool(simplified == 0),
                "statement": statement,
                "residual": str(simplified),
            }
        )

    def ball_check(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(ident)
        self.ball.append(
            {"id": ident, "passed": bool(passed), "statement": statement, **data}
        )

    def guard(
        self,
        ident: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": (
                    "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_BALL_HYPOTHESIS_SCOPE_AUDIT"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )

    def count_bessel(self) -> None:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")

    def count_callback(self) -> None:
        self.quadrature_callback_evaluations += 1
        if (
            self.quadrature_callback_evaluations
            > expected_caps()["quadrature_callback_evaluations"]
        ):
            raise AssertionError("quadrature callback cap exceeded")


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    if sha256_bytes(raw) != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key, expected in (
        ("run_status", "VALID_RUN"),
        ("verdict", item["required_verdict"]),
        ("result_payload_sha256_without_self", item["payload_sha256_without_self"]),
    ):
        if result.get(key) != expected:
            raise AssertionError(f"upstream {key} mismatch: {item['path']}")
    if result.get("numbered_phase") is not None:
        raise AssertionError("upstream numbered-phase convention drift")
    record = {
        "path": item["path"],
        "sha256": item["sha256"],
        "payload_sha256_without_self": item["payload_sha256_without_self"],
        "verdict": item["required_verdict"],
    }
    return result, record


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def bracket_band(left: fmpq, right: fmpq) -> arb:
    midpoint = (left + right) / 2
    radius = (right - left) / 2
    return arb(arb(midpoint), arb(radius))


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if upper < lower:
        raise AssertionError("reversed interval bounds")
    midpoint = (lower + upper) / 2
    radius = (upper - lower) / 2
    result = arb(midpoint, radius)
    if not (result.lower() <= lower and result.upper() >= upper):
        raise AssertionError("outward interval construction failed")
    return result


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "width_upper": (value.upper() - value.lower()).upper().str(
            digits, radius=False
        ),
        "midpoint_radius": value.str(digits),
    }


def complex_ball_record(value: acb, digits: int) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "absolute_lower": value.abs_lower().str(digits, radius=False),
        "absolute_upper": value.abs_upper().str(digits, radius=False),
    }


def contains_zero(value: arb) -> bool:
    return bool(value.lower() <= 0 <= value.upper())


def scaled_bessel_k(audit: Audit, x: acb, order: acb) -> acb:
    audit.count_bessel()
    return x.bessel_k(order, scaled=True)


def unscaled_bessel_k(audit: Audit, x: acb, order: acb) -> acb:
    audit.count_bessel()
    return x.bessel_k(order, scaled=False)


def exact_identity_audit(audit: Audit) -> None:
    u, uq, v, vq = sp.symbols("u u_Q v v_Q", nonzero=True)
    a0, a_lambda = sp.symbols("A_0 A_lambda")

    def d_q(expr: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expr, u) * uq
            + sp.diff(expr, uq) * a0 * u
            + sp.diff(expr, v) * vq
            + sp.diff(expr, vq) * (a0 * v + a_lambda * u)
        )

    g = -uq / u
    h = (uq * v - u * vq) / u**2
    wronskian = u * vq - uq * v
    audit.identity(
        "rawc.h_tail.riccati",
        d_q(g) - (g**2 - a0),
        "For u_QQ=A_0*u, g=-u_Q/u obeys g_Q=g^2-A_0.",
    )
    audit.identity(
        "rawc.h_tail.sensitivity",
        d_q(h) - (2 * g * h - a_lambda),
        "For v_QQ=A_0*v+A_lambda*u, h=partial_lambda[-u_Q/u] obeys h_Q=2*g*h-A_lambda.",
    )
    audit.identity(
        "rawc.h_tail.wronskian_derivative",
        d_q(wronskian) - a_lambda * u**2,
        "The forced Wronskian satisfies W(u,v)_Q=A_lambda*u^2.",
    )
    audit.identity(
        "rawc.h_tail.integrating_factor",
        d_q(u**2 * h) + a_lambda * u**2,
        "The scale-invariant integrating factor is (u^2*h)_Q=-A_lambda*u^2.",
    )

    c0, c1 = sp.symbols("c_0 c_1", nonzero=True)
    u_tilde = c0 * u
    uq_tilde = c0 * uq
    v_tilde = c0 * v + c1 * u
    vq_tilde = c0 * vq + c1 * uq
    h_tilde = (
        uq_tilde * v_tilde - u_tilde * vq_tilde
    ) / u_tilde**2
    audit.identity(
        "rawc.h_tail.amplitude_rescaling_invariance",
        h_tilde - h,
        "Under u_lambda -> c(lambda)u_lambda, h is invariant and the c'(0) term cancels exactly.",
    )

    x, c = sp.symbols("x C", positive=True)
    q_to_x_density = c * (x / c) ** sp.Rational(3, 2) / x
    audit.identity(
        "rawc.h_tail.Q_to_x_density",
        q_to_x_density - sp.sqrt(x) / sp.sqrt(c),
        "For x=C*exp(Q), A_lambda*dQ becomes C^(-1/2)*sqrt(x)*dx.",
    )

    x0, y = sp.symbols("x_0 y", positive=True)
    sx, s0 = sp.symbols("S_x S_0", nonzero=True)
    unscaled_ratio_integrand = (
        sp.sqrt(x0 + y)
        * (sp.exp(-(x0 + y)) * sx) ** 2
        / (sp.exp(-x0) * s0) ** 2
    )
    scaled_ratio_integrand = (
        sp.sqrt(x0 + y) * sp.exp(-2 * y) * sx**2 / s0**2
    )
    audit.identity(
        "rawc.h_tail.scaled_bessel_cancellation",
        unscaled_ratio_integrand - scaled_ratio_integrand,
        "S=exp(x)K removes the common superexponential scale without changing the h integrand.",
    )

    exp_q = sp.symbols("exp_Q", positive=True)
    leading_a = 36 * sp.pi**4 * exp_q**2
    forcing = 6 * sp.pi**2 * exp_q ** sp.Rational(3, 2)
    audit.identity(
        "rawc.h_tail.leading_growth_scale",
        forcing / (2 * sp.sqrt(leading_a)) - sp.sqrt(exp_q) / 2,
        "The leading recessive sensitivity scale grows as exp(Q/2)/2, so h(infinity)=0 is not the boundary condition.",
    )

    big_y = sp.symbols("Y", positive=True)
    audit.identity(
        "rawc.h_tail.exponential_tail_antiderivative",
        sp.diff(sp.exp(-2 * big_y) / 2, big_y) + sp.exp(-2 * big_y),
        "The exponential part of the manual improper-tail majorant integrates exactly to exp(-2Y)/2.",
    )


def run_tier(
    audit: Audit,
    *,
    root_index: int,
    tier_index: int,
    exact_left: fmpq,
    exact_right: fmpq,
    kappa_band: arb,
    dps: int,
    rel_tol_text: str,
    abs_tol_text: str,
    max_width_text: str,
    cutoff_y: int,
    tail_target_text: str,
    options: dict[str, Any],
    digits_out: int,
) -> tuple[dict[str, Any], arb | None]:
    ctx.dps = dps
    band_covers_exact = bool(
        kappa_band.lower() <= exact_left
        and kappa_band.upper() >= exact_right
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.band_coverage",
        band_covers_exact,
        "This tier's outward-rounded Arb kappa interval covers both exact-rational endpoints of the full upstream bracket.",
        decimal_digits=dps,
        left_exact=str(exact_left),
        right_exact=str(exact_right),
        coverage=interval_record(kappa_band, digits_out),
    )
    if not band_covers_exact:
        return (
            {
                "decimal_digits": dps,
                "status": "UNRESOLVED_BAND_COVERAGE",
                "h_enclosure": None,
            },
            None,
        )
    c_ball = 6 * arb.pi() ** 2
    sqrt_c = c_ball.sqrt()
    x0 = c_ball * arb(4).exp()
    y_end = arb(cutoff_y)
    order = acb(0, kappa_band)
    x0_complex = acb(x0)
    s0 = scaled_bessel_k(audit, x0_complex, order)
    s0_unscaled = unscaled_bessel_k(audit, x0_complex, order)
    scaled_direct = x0_complex.exp() * s0_unscaled
    x_end_complex = acb(x0 + y_end)
    s_end = scaled_bessel_k(audit, x_end_complex, order)
    s_end_unscaled = unscaled_bessel_k(audit, x_end_complex, order)
    scaled_end_direct = x_end_complex.exp() * s_end_unscaled

    denominator_ok = bool(
        s0.is_finite()
        and s0.real.lower() > 0
        and contains_zero(s0.imag)
        and s0.abs_lower() > 0
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.denominator",
        denominator_ok,
        "The full kappa-band scaled K ball at Qplus is real by the analytic guard and has a strictly positive real lower bound, so division is fail-closed and pole-free on this band.",
        decimal_digits=dps,
        scaled_K_Qplus=complex_ball_record(s0, digits_out),
    )
    scaled_convention_ok = bool(
        s0.overlaps(scaled_direct) and s_end.overlaps(scaled_end_direct)
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.scaled_convention",
        scaled_convention_ok,
        "At both finite endpoints, the library scaled-K balls overlap exp(x) times the unscaled-K balls as a same-backend convention sentinel, not an independent implementation check.",
        Qplus_overlap=bool(s0.overlaps(scaled_direct)),
        cutoff_overlap=bool(s_end.overlaps(scaled_end_direct)),
    )
    if not (denominator_ok and scaled_convention_ok):
        return (
            {
                "decimal_digits": dps,
                "status": "UNRESOLVED_DENOMINATOR_OR_SCALING",
                "scaled_K_Qplus": complex_ball_record(s0, digits_out),
                "h_enclosure": None,
            },
            None,
        )

    callback_stats = {"analytic_true": 0, "analytic_false": 0}

    def finite_integrand(y_value: acb, analytic: bool) -> acb:
        audit.count_callback()
        callback_stats["analytic_true" if analytic else "analytic_false"] += 1
        x_value = acb(x0) + y_value
        if x_value.real.lower() <= 0:
            return acb("nan")
        square_root = x_value.sqrt(analytic=analytic)
        scaled_k = scaled_bessel_k(audit, x_value, order)
        return square_root * (-2 * y_value).exp() * scaled_k**2

    audit.quadrature_calls += 1
    if audit.quadrature_calls > expected_caps()["quadrature_calls"]:
        raise AssertionError("quadrature call cap exceeded")
    finite_integral = acb.integral(
        finite_integrand,
        0,
        cutoff_y,
        rel_tol=arb(rel_tol_text),
        abs_tol=arb(abs_tol_text),
        deg_limit=int(options["deg_limit"]),
        eval_limit=int(options["eval_limit_each"]),
        depth_limit=int(options["depth_limit"]),
        use_heap=bool(options["use_heap"]),
        verbose=False,
    )
    quadrature_ok = bool(
        finite_integral.is_finite()
        and finite_integral.real.lower() > 0
        and contains_zero(finite_integral.imag)
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.finite_quadrature",
        quadrature_ok,
        "The rigorous finite acb.integral enclosure is finite, contains the analytically real value, and has a strictly positive real lower bound on the entire kappa band.",
        relative_tolerance=rel_tol_text,
        absolute_tolerance=abs_tol_text,
        callback_stats=callback_stats,
        finite_integral=complex_ball_record(finite_integral, digits_out),
    )
    if not quadrature_ok:
        return (
            {
                "decimal_digits": dps,
                "status": "UNRESOLVED_FINITE_QUADRATURE",
                "finite_integral": complex_ball_record(
                    finite_integral, digits_out
                ),
                "h_enclosure": None,
            },
            None,
        )

    finite_h = finite_integral / (acb(sqrt_c) * s0**2)
    denominator_lower = s0.real.lower()
    tail_upper = (
        arb.pi()
        * arb(-2 * cutoff_y).exp()
        / (
            4
            * sqrt_c
            * denominator_lower**2
            * (x0 + y_end).sqrt()
        )
    )
    tail_ok = bool(
        tail_upper.is_finite()
        and tail_upper.lower() >= 0
        and tail_upper.upper() < arb(tail_target_text).lower()
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.improper_tail",
        tail_ok,
        "The DLMF-integral Gaussian majorant bounds the manually separated improper tail below the declared target after outward denominator division.",
        cutoff_Y=cutoff_y,
        denominator_real_lower=denominator_lower.str(
            digits_out, radius=False
        ),
        x_Qplus=interval_record(x0, digits_out),
        x_cutoff=interval_record(x0 + y_end, digits_out),
        tail_upper=tail_upper.upper().str(digits_out, radius=False),
        target=tail_target_text,
    )

    h_lower = finite_h.real.lower()
    h_upper = finite_h.real.upper() + tail_upper.upper()
    h_ball = interval_from_bounds(h_lower, h_upper)
    h_width = h_ball.upper() - h_ball.lower()
    h_ok = bool(
        finite_h.is_finite()
        and contains_zero(finite_h.imag)
        and h_ball.lower() > 0
        and h_width.upper() < arb(max_width_text).lower()
    )
    audit.ball_check(
        f"rawc.h_tail.root{root_index}.tier{tier_index}.h_enclosure",
        h_ok,
        "The full h(4) interval adds a nonnegative analytic improper-tail allowance to the rigorous finite integral and is positive and narrower than the declared tier target.",
        maximum_width=max_width_text,
        finite_h=complex_ball_record(finite_h, digits_out),
        h_enclosure=interval_record(h_ball, digits_out),
    )

    status = "CERTIFIED_TIER" if tail_ok and h_ok else "UNRESOLVED_TIER"
    return (
        {
            "decimal_digits": dps,
            "status": status,
            "same_backend_repeat": True,
            "relative_tolerance": rel_tol_text,
            "absolute_tolerance": abs_tol_text,
            "callback_stats": callback_stats,
            "scaled_K_Qplus": complex_ball_record(s0, digits_out),
            "finite_integral": complex_ball_record(finite_integral, digits_out),
            "finite_h": complex_ball_record(finite_h, digits_out),
            "improper_tail_upper": tail_upper.upper().str(
                digits_out, radius=False
            ),
            "h_enclosure": interval_record(h_ball, digits_out),
        },
        h_ball if tail_ok and h_ok else None,
    )


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    if importlib.metadata.version("python-flint") != "0.9.0":
        raise AssertionError("python-flint runtime version drift")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-lambda-zero-differentiated-plus-tail.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if (
        cfg.get("resource_caps") != expected_caps()
        or cfg.get("required_fail_closed_outputs") != expected_nulls()
        or cfg["declared_conventions"]["precision_ladder_decimal_digits"]
        != [80, 120]
    ):
        raise AssertionError("resource, precision or fail-closed mutation")

    root = Path(__file__).resolve().parent.parent
    upstream, upstream_record = verify_upstream(root, cfg["upstream_results"][0])
    root_rows = upstream["certified_calculation"]["endpoint_characteristic"][
        "root_rows"
    ]
    if len(root_rows) != cfg["resource_caps"]["root_brackets"]:
        raise AssertionError("upstream certified bracket count drift")

    audit = Audit()
    exact_identity_audit(audit)
    conventions = cfg["declared_conventions"]
    precision_ladder = conventions["precision_ladder_decimal_digits"]
    rel_tolerances = conventions["quadrature_relative_tolerances"]
    abs_tolerances = conventions["quadrature_absolute_tolerances"]
    max_widths = conventions["maximum_h_widths"]
    cutoff_y = int(conventions["quadrature_cutoff_Y"])
    digits_out = int(conventions["ball_output_digits"])
    options = conventions["quadrature_options"]
    rows: list[dict[str, Any]] = []

    for root_index, upstream_row in enumerate(root_rows, start=1):
        certificate = upstream_row["certified_high_precision_bracket"]
        if not certificate.get("at_least_one_real_sign_changing_zero"):
            raise AssertionError("upstream root-existence certificate drift")
        left = exact_rational(certificate["left_exact"])
        right = exact_rational(certificate["right_exact"])
        if not left < right:
            raise AssertionError("upstream bracket ordering drift")

        ctx.dps = max(precision_ladder)
        coverage_band = bracket_band(left, right)
        band_covers_exact = bool(
            coverage_band.lower() <= left and coverage_band.upper() >= right
        )
        audit.ball_check(
            f"rawc.h_tail.root{root_index}.band_coverage",
            band_covers_exact,
            "The outward-rounded Arb kappa interval covers both exact-rational endpoints of the full upstream sign-change bracket.",
            left_exact=str(left),
            right_exact=str(right),
            coverage=interval_record(coverage_band, digits_out),
        )

        tier_records: list[dict[str, Any]] = []
        tier_balls: list[arb | None] = []
        for tier_index, (dps, rel_tol, abs_tol, max_width) in enumerate(
            zip(
                precision_ladder,
                rel_tolerances,
                abs_tolerances,
                max_widths,
                strict=True,
            ),
            start=1,
        ):
            ctx.dps = int(dps)
            kappa_band = bracket_band(left, right)
            if not (
                kappa_band.lower() <= left and kappa_band.upper() >= right
            ):
                raise AssertionError("tier kappa band lost an exact endpoint")
            record, h_ball = run_tier(
                audit,
                root_index=root_index,
                tier_index=tier_index,
                exact_left=left,
                exact_right=right,
                kappa_band=kappa_band,
                dps=int(dps),
                rel_tol_text=rel_tol,
                abs_tol_text=abs_tol,
                max_width_text=max_width,
                cutoff_y=cutoff_y,
                tail_target_text=conventions["tail_upper_target"],
                options=options,
                digits_out=digits_out,
            )
            tier_records.append(record)
            tier_balls.append(h_ball)

        low, high = tier_balls
        refinement_ok = False
        refined_ball: arb | None = None
        if low is not None and high is not None:
            lower = low.lower() if low.lower() >= high.lower() else high.lower()
            upper = low.upper() if low.upper() <= high.upper() else high.upper()
            overlap = bool(lower <= upper)
            low_width = low.upper() - low.lower()
            high_width = high.upper() - high.lower()
            narrower = bool(high_width.upper() < low_width.lower())
            refinement_ok = overlap and narrower
            if overlap:
                refined_ball = interval_from_bounds(lower, upper)
        else:
            overlap = False
            narrower = False
        audit.ball_check(
            f"rawc.h_tail.root{root_index}.precision_refinement",
            refinement_ok,
            "The two rigorous same-backend tier enclosures overlap and the higher-precision enclosure is strictly narrower; their intersection is retained without calling it independent validation.",
            overlap=overlap,
            high_precision_strictly_narrower=narrower,
            refined_h_enclosure=(
                interval_record(refined_ball, digits_out)
                if refined_ball is not None
                else None
            ),
        )
        rows.append(
            {
                "root_index": root_index,
                "kappa_bracket": {
                    "left_exact": str(left),
                    "right_exact": str(right),
                    "width_exact": str(right - left),
                    "coverage_ball": interval_record(coverage_band, digits_out),
                },
                "precision_tiers": tier_records,
                "certified_h_Qplus_intersection": (
                    interval_record(refined_ball, digits_out)
                    if refinement_ok and refined_ball is not None
                    else None
                ),
                "normalization_invariant": True,
            }
        )

    audit.guard(
        "rawc.h_tail.guard.green_identity",
        "variation-of-parameters / Lagrange identity for a parameter-differentiated second-order scalar equation",
        "u is the lambda-zero recessive K direction, v=partial_lambda u after any differentiable amplitude convention, (u^2 h)'=-A_lambda u^2, and u^2 h tends to zero although h itself grows",
        "h(Q)=u(Q)^(-2) integral_Q^infinity A_lambda u^2 is positive and invariant under u_lambda -> c(lambda)u_lambda. This guard fixes the correct plus-end condition; it does not provide node transport or an amplitude F_lambda.",
    )
    audit.guard(
        "rawc.h_tail.guard.dlmf_reality_and_tail",
        "DLMF sections 10.27 and 10.32, especially equation 10.32.9",
        "x>0 and kappa is real; K_(-nu)=K_nu and conjugation make K_(i*kappa)(x) real, while K_(i*kappa)(x)=integral exp(-x cosh t)cos(kappa t)dt and cosh t>=1+t^2/2",
        "The true real function satisfies |K_(i*kappa)(x)|<=exp(-x)sqrt(pi/(2x)), uniformly on each real kappa band. This supplies only the explicit improper-tail upper bound after the finite rigorous quadrature.",
    )
    audit.guard(
        "rawc.h_tail.guard.acb_integral",
        "python-flint 0.9.0 acb.integral backed by FLINT/Arb acb_calc_integrate",
        "the integration endpoints are finite; every callback is capped; the path has Re(x)>0; sqrt receives the analytic flag; complex-order Bessel balls, tolerances and all work limits are retained",
        "Each finite-segment output is a rigorous complex ball enclosure. Improper integration is not delegated to acb.integral and is handled by the separate DLMF majorant.",
    )
    audit.guard(
        "rawc.h_tail.guard.parameter_ball_union",
        "inclusion isotonicity of Arb/acb ball evaluation with an analytic x integrand",
        "every precision tier proves that its kappa ball contains the exact real bracket endpoints; each fixed real kappa in that interval selects an analytic positive-real-x integrand; all fixed parameters are evaluated through the same order ball",
        "The emitted finite integral ball encloses the union of the true integrals over the entire declared kappa bracket. This is not a point sample and does not extend coverage beyond the five brackets.",
    )
    audit.guard(
        "rawc.h_tail.guard.same_backend_repeat",
        "nested/refined enclosure consistency",
        "80- and 120-decimal runs use the same locked python-flint/FLINT-Arb implementation with different requested tolerances",
        "Overlap and strict width refinement are retained as implementation consistency checks only. They are not labeled an independent backend verification.",
    )
    audit.guard(
        "rawc.h_tail.guard.scope",
        "endpoint transport and normalization boundary",
        "the calculation stops at Qplus=4 and emits h=partial_lambda[-u_Q/u], not a transported variational amplitude",
        "No node-safe Qplus-to-Q0 transport, numerical F_lambda amplitude, root velocity, nonreal m-function, spectral measure, rigging map, RAQ, physics, quantum-gravity or TOE conclusion follows.",
    )

    all_exact = all(item["passed"] for item in audit.exact)
    all_ball = all(item["passed"] for item in audit.ball)
    resource_exact = bool(
        audit.quadrature_calls == expected_caps()["quadrature_calls"]
        and audit.bessel_evaluations
        <= expected_caps()["ball_bessel_evaluations"]
        and audit.quadrature_callback_evaluations
        <= expected_caps()["quadrature_callback_evaluations"]
    )
    passed = all_exact and all_ball and resource_exact
    verdict = cfg["decision_table"][0 if passed else 1]["verdict"]
    impact = cfg["decision_table"][0 if passed else 1]["programme_impact"]
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)},
        "upstream_results": [upstream_record],
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "assumptions": cfg["assumptions"],
        "exact_checks": audit.exact,
        "ball_checks": audit.ball,
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "ball_passed": sum(item["passed"] for item in audit.ball),
            "ball_total": len(audit.ball),
            "theorem_guard_count": len(audit.theorem_guards),
            "resource_accounting_passed": resource_exact,
            "all_executable_checks_passed": passed,
        },
        "certified_calculation": {
            "status": (
                "CERTIFIED_LAMBDA_ZERO_H_QPLUS_ON_FIVE_FULL_KAPPA_BRACKETS"
                if passed
                else "NOT_CERTIFIED"
            ),
            "definition": "h(4;kappa)=partial_lambda[-u_Q/u] at lambda=0",
            "exact_formula": "h(4)=C^(-1/2)*integral_xplus^infinity sqrt(x)K_(i*kappa)(x)^2 dx / K_(i*kappa)(xplus)^2",
            "correct_plus_end_condition": "u^2*h tends to zero; h itself is not set to zero",
            "normalization_invariant": True,
            "root_bracket_rows": rows,
            "certified_bracket_count": (
                sum(
                    row["certified_h_Qplus_intersection"] is not None
                    for row in rows
                )
                if passed
                else 0
            ),
            "next_mathematical_gap": "transport h from Qplus=4 to Q0=-4 through an unwrapped node-safe Pruefer/projective atlas; an amplitude F_lambda additionally needs an explicit amplitude convention away from roots",
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations_cap": cfg["resource_caps"][
                "symbolic_operations"
            ],
            "ball_bessel_evaluations": audit.bessel_evaluations,
            "ball_bessel_evaluation_cap": cfg["resource_caps"][
                "ball_bessel_evaluations"
            ],
            "quadrature_calls": audit.quadrature_calls,
            "quadrature_call_cap": cfg["resource_caps"]["quadrature_calls"],
            "quadrature_callback_evaluations": audit.quadrature_callback_evaluations,
            "quadrature_callback_evaluation_cap": cfg["resource_caps"][
                "quadrature_callback_evaluations"
            ],
            "root_brackets": len(rows),
            "root_calls": 0,
            "finite_difference_calls": 0,
            "ode_calls": 0,
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
            "sympy": sp.__version__,
            "python_flint": importlib.metadata.version("python-flint"),
            "platform": platform.platform(),
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": "VALID_RUN",
                "verdict": verdict,
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "ball_passed": result["check_summary"]["ball_passed"],
                "ball_total": result["check_summary"]["ball_total"],
                "theorem_guards": result["check_summary"][
                    "theorem_guard_count"
                ],
                "certified_brackets": result["certified_calculation"][
                    "certified_bracket_count"
                ],
                "bessel_evaluations": audit.bessel_evaluations,
                "quadrature_callbacks": audit.quadrature_callback_evaluations,
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
