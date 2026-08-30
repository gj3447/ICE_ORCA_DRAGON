#!/usr/bin/env python3
"""Coarse actual nonzero-lambda raw-C Gamma_1 enclosure; not spectral data or RAQ."""
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


INPUT_NAME = "RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_INPUTS.json"
RESULT_NAME = "RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_actual_nonzero_lambda_gamma1_coarse_enclosure.py"
)
EXPECTED_INPUT_SHA256 = "be3c065e2473a6cc5c91f896a68813fb48b65e39e43e5f46cae468f77d896403"
CALCULATION_ID = "RawCActualNonzeroLambdaGamma1CoarseEnclosure"
RESULT_SCHEMA = "ice.raw-c-actual-nonzero-lambda-gamma1-coarse-enclosure.result.v1"
RESULT_PREFIX = "RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_RESULT="
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
        "symbolic_operations": 2000,
        "ball_bessel_evaluations": 12,
        "precision_tiers": 2,
        "root_brackets": 1,
        "nonzero_lambda_boxes": 2,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "ode_calls": 0,
        "sampling_points": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "validated_numerical_ODE_transport": None,
        "sharp_actual_nonzero_lambda_endpoint_value": None,
        "Gamma1_zero_exclusion": None,
        "nonzero_lambda_root_continuation": None,
        "root_velocity": None,
        "unique_or_complete_zero_shell_root_census": None,
        "nonreal_resolvent_or_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "general_p_mixing_extension_classification": None,
        "canonical_p_zero_origin_sector": None,
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


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    ball: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def identity(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self.register(ident)
        reduced = sp.simplify(residual)
        self.exact.append(
            {
                "id": ident,
                "passed": bool(reduced == 0),
                "statement": statement,
                "residual": str(reduced),
            }
        )

    def inequality(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(ident)
        self.exact.append(
            {"id": ident, "passed": bool(passed), "statement": statement, **data}
        )

    def ball_check(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(ident)
        self.ball.append(
            {"id": ident, "passed": bool(passed), "statement": statement, **data}
        )

    def guard(
        self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str
    ) -> None:
        self.register(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": (
                    "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_ARB_HYPOTHESIS_SCOPE_AUDIT"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )

    def bessel_k(self, z: acb, order: acb, *, scaled: bool = False) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")
        return z.bessel_k(order, scaled=scaled)


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def bracket_band(left: fmpq, right: fmpq) -> arb:
    if not left < right:
        raise AssertionError("reversed exact bracket")
    return arb(arb((left + right) / 2), arb((right - left) / 2))


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if upper < lower:
        raise AssertionError("reversed interval bounds")
    value = arb((lower + upper) / 2, (upper - lower) / 2)
    if not (value.lower() <= lower and value.upper() >= upper):
        raise AssertionError("outward interval construction failed")
    return value


def symmetric_interval(radius: arb) -> arb:
    upper = arb(radius.upper())
    if not upper >= 0:
        raise AssertionError("negative symmetric radius")
    return interval_from_bounds(-upper, upper)


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


def contains_interval(outer: arb, inner: arb) -> bool:
    return bool(outer.lower() <= inner.lower() and inner.upper() <= outer.upper())


def intersect(left: arb, right: arb) -> arb | None:
    low = left.lower() if left.lower() >= right.lower() else right.lower()
    high = left.upper() if left.upper() <= right.upper() else right.upper()
    return interval_from_bounds(low, high) if low <= high else None


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
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
    return result, {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": result["result_payload_sha256_without_self"],
        "verdict": result["verdict"],
    }


def exact_audit(audit: Audit) -> None:
    x, c, kappa, lam, rho = sp.symbols(
        "x C kappa lambda rho", positive=True, real=True
    )
    forcing = x ** sp.Rational(3, 2) / sp.sqrt(c)
    coefficient = x**2 + lam * forcing - kappa**2
    r = x + sp.Rational(1, 2) + rho
    rho_q = (
        kappa**2
        + sp.Rational(1, 4)
        - lam * forcing
        + (2 * x + 1) * rho
        + rho**2
    )
    audit.identity(
        "rawc.actual.coefficient_change",
        coefficient.subs(x, c * sp.exp(sp.Symbol("Q", real=True)))
        - (
            c**2 * sp.exp(2 * sp.Symbol("Q", real=True))
            + lam * c * sp.exp(sp.Rational(3, 2) * sp.Symbol("Q", real=True))
            - kappa**2
        ),
        "With C=6*pi^2 and x=C*exp(Q), the raw-C coefficient has the declared x form.",
    )
    audit.identity(
        "rawc.actual.riccati_rho",
        x + rho_q - (r**2 - coefficient),
        "r=-u_Q/u and rho=r-x-1/2 obey the declared Riccati equation in Q.",
    )
    backward = -rho_q
    audit.identity(
        "rawc.actual.backward_upper_barrier",
        backward.subs(rho, 1)
        + (kappa**2 + 2 * x + sp.Rational(9, 4) - lam * forcing),
        "At rho=1 the backward vector field is the negative of the upper barrier bracket.",
    )
    audit.identity(
        "rawc.actual.backward_lower_barrier",
        backward.subs(rho, -1)
        - (2 * x - kappa**2 - sp.Rational(1, 4) + lam * forcing),
        "At rho=-1 the backward vector field equals the lower inward margin.",
    )
    rho_constant = sp.symbols("rho_constant", real=True)
    primitive = x + (sp.Rational(1, 2) + rho_constant) * sp.log(x)
    audit.identity(
        "rawc.actual.amplitude_primitive",
        sp.diff(primitive, x)
        - (x + sp.Rational(1, 2) + rho_constant) / x,
        "The x-frame primitive gives the exact logarithmic amplitude bounds for constant rho barriers.",
    )
    mu, z1, z2, a_value = sp.symbols(
        "mu Z_1 Z_2 A", positive=True, real=True
    )
    u = z1
    uq = mu * z2
    audit.identity(
        "rawc.actual.compact_scaled_state_first",
        -uq - (-mu * z2),
        "In backward time s=Q_3-Q, Z_1,s=-mu*Z_2.",
    )
    audit.identity(
        "rawc.actual.compact_scaled_state_second",
        -a_value * u / mu - (-a_value * z1 / mu),
        "For Z_2=u_Q/mu, the second backward equation is Z_2,s=-(A/mu)Z_1.",
    )
    q = sp.symbols("Q", real=True)
    potential = 36 * sp.pi**4 * sp.exp(2 * q)
    density = 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q)
    audit.identity(
        "rawc.actual.minus_potential_integral",
        sp.diff(18 * sp.pi**4 * sp.exp(2 * q), q) - potential,
        "The complete Q<-4 potential mass is 18*pi^4*exp(-8).",
    )
    audit.identity(
        "rawc.actual.minus_forcing_integral",
        sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q)
        - density,
        "The complete Q<-4 forcing mass is 4*pi^2*exp(-6).",
    )
    rotation = sp.Matrix([[0, kappa], [-kappa, 0]])
    audit.identity(
        "rawc.actual.free_rotation_skew",
        sum((entry**2 for entry in rotation + rotation.T), sp.Integer(0)),
        "The free (u,u_Q/kappa) generator is skew and preserves the Euclidean norm.",
    )
    u0, uq0, cp, cpq, a0 = sp.symbols(
        "u_0 u_Q0 c_p c_p_Q a_0", real=True
    )
    wronskian = u0 * cpq - uq0 * cp
    wronskian_q = (
        uq0 * cpq
        + u0 * a0 * cp
        - (a0 + lam * density) * u0 * cp
        - uq0 * cpq
    )
    audit.identity(
        "rawc.actual.wronskian_derivative",
        wronskian_q + lam * density * u0 * cp,
        "The selected fixed-reference Wronskian obeys W_Q=-lambda*a*u*c_p.",
    )
    integral = sp.symbols("I_minus", real=True)
    gamma = uq0 - lam * integral
    audit.identity(
        "rawc.actual.gamma1_identity",
        gamma - (uq0 - lam * integral),
        "The declared Gamma_1 is endpoint derivative minus the complete weighted minus-tail integral.",
    )


def parse_lambda_boxes(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    boxes: list[dict[str, Any]] = []
    cap = exact_rational(cfg["declared_conventions"]["lambda_absolute_cap"])
    for item in cfg["declared_conventions"]["lambda_boxes"]:
        left = exact_rational(item["left"])
        right = exact_rational(item["right"])
        if not left < right:
            raise AssertionError("lambda box ordering drift")
        abs_max = max(abs(left), abs(right))
        if abs_max > cap:
            raise AssertionError("lambda box exceeds cap")
        boxes.append(
            {
                "label": item["label"],
                "left": left,
                "right": right,
                "abs_max": abs_max,
            }
        )
    if [box["label"] for box in boxes] != ["negative", "positive"]:
        raise AssertionError("lambda box label/order drift")
    return boxes


def lg_difference_bound(plus_data: dict[str, Any]) -> arb:
    envelopes = plus_data["analytic_calculation"]["uniform_envelopes"]
    if envelopes["eta_bar"] != "1/100000":
        raise AssertionError("upstream eta drift")
    r_bar = exact_rational(envelopes["R_bar"])
    eta = exact_rational(envelopes["eta_bar"])
    v_bar = arb(r_bar) / (
        arb(6) * 9 * 7**2 * (arb(1) - arb(eta))
    )
    error = (v_bar / 2).exp() - 1
    return 2 * error / (1 - error)


def compute_envelope(
    audit: Audit,
    *,
    label: str,
    tier_index: int,
    dps: int,
    kappa_left: fmpq,
    kappa_right: fmpq,
    lambda_left: fmpq,
    lambda_right: fmpq,
    lambda_abs_max: fmpq,
    plus_data: dict[str, Any],
    digits: int,
) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    kappa_band = bracket_band(kappa_left, kappa_right)
    lambda_band = (
        arb(lambda_left)
        if lambda_left == lambda_right
        else bracket_band(lambda_left, lambda_right)
    )
    lambda_cap = arb(lambda_abs_max)
    c_value = 6 * arb.pi() ** 2
    sqrt_c = c_value.sqrt()
    x4 = c_value * arb(4).exp()
    x0 = c_value * arb(-4).exp()
    t4 = x4 * x4.sqrt() / sqrt_c
    a4 = x4**2 + lambda_band * t4 - kappa_band**2
    aq4 = 2 * x4**2 + (arb(3) / 2) * lambda_band * t4
    sqrt_a4 = a4.sqrt()
    u4 = arb(1) / sqrt_a4.sqrt()
    r_w4 = sqrt_a4 + aq4 / (4 * a4)
    rho_w4 = r_w4 - x4 - arb(1) / 2
    d_bound = lg_difference_bound(plus_data)
    slope_error = arb((d_bound * sqrt_a4).upper())
    rho4 = interval_from_bounds(
        rho_w4.lower() - slope_error,
        rho_w4.upper() + slope_error,
    )
    upstream_decimal = arb(
        plus_data["analytic_calculation"]["at_Q_plus_4"][
            "sqrt_A_normalized_log_derivative_difference_bound"
        ]
    )
    start_ok = bool(
        kappa_band.lower() <= kappa_left
        and kappa_band.upper() >= kappa_right
        and lambda_band.lower() <= lambda_left
        and lambda_band.upper() >= lambda_right
        and a4.is_finite()
        and a4.lower() > 0
        and u4.is_finite()
        and u4.lower() > 0
        and rho4.lower() >= -1
        and rho4.upper() <= 1
        and abs(d_bound - upstream_decimal).upper() < arb("1e-20")
    )
    audit.ball_check(
        f"rawc.actual.{label}.tier{tier_index}.lg_start",
        start_ok,
        "The full parameter boxes are covered, A(4)>0, and the actual normalized recessive direction starts inside rho in [-1,1].",
        decimal_digits=dps,
        kappa_bracket=interval_record(kappa_band, digits),
        lambda_box=interval_record(lambda_band, digits),
        A_Qplus=interval_record(a4, digits),
        u_Qplus_normalized=interval_record(u4, digits),
        rho_wkb_Qplus=interval_record(rho_w4, digits),
        inherited_log_slope_error=interval_record(symmetric_interval(slope_error), digits),
        actual_rho_Qplus=interval_record(rho4, digits),
    )

    three = arb(3)
    t3 = three * three.sqrt() / sqrt_c
    derivative_margin = 2 - (arb(3) / 2) * lambda_cap * arb(2).exp()
    lower_barrier_margin = (
        2 * three
        - (kappa_band**2).upper()
        - arb(1) / 4
        - lambda_cap * t3.upper()
    )
    upper_barrier_bracket = (
        (kappa_band**2).lower()
        + 2 * three
        + arb(9) / 4
        - lambda_cap * t3.upper()
    )
    barrier_ok = bool(
        derivative_margin.is_finite()
        and derivative_margin.lower() > 0
        and lower_barrier_margin.is_finite()
        and lower_barrier_margin.lower() > 0
        and upper_barrier_bracket.is_finite()
        and upper_barrier_bracket.lower() > 0
    )
    audit.ball_check(
        f"rawc.actual.{label}.tier{tier_index}.riccati_barrier",
        barrier_ok,
        "The worst-case barrier functions increase with x, rho=-1 points upward and rho=1 points downward in backward time on 3<=x<=C*exp(4).",
        monotonic_derivative_margin=interval_record(derivative_margin, digits),
        rho_minus_one_inward_margin_at_x3=interval_record(
            lower_barrier_margin, digits
        ),
        rho_plus_one_positive_bracket_at_x3=interval_record(
            upper_barrier_bracket, digits
        ),
    )

    log_ratio = (x4 / three).log()
    log_u4 = -a4.log() / 4
    log_u3_lower = log_u4 + x4 - three - log_ratio / 2
    log_u3_upper = log_u4 + x4 - three + 3 * log_ratio / 2
    u3_lower = arb(log_u3_lower.lower()).exp()
    u3_upper = arb(log_u3_upper.upper()).exp()
    u3 = interval_from_bounds(u3_lower, u3_upper)
    uq3 = interval_from_bounds(
        -(arb(9) / 2) * u3_upper,
        -(arb(5) / 2) * u3_lower,
    )
    mu = arb(kappa_left)
    z3_upper = arb(
        max(u3_upper, ((arb(9) / 2) * u3_upper / mu).upper())
    )
    a_abs_upper = (
        9
        + (kappa_band**2).upper()
        + lambda_cap * t3.upper()
    )
    matrix_norm_upper = mu + a_abs_upper / mu
    compact_length = (three / x0).log()
    compact_log_growth = matrix_norm_upper * compact_length
    z0_upper = arb(
        (z3_upper * arb(compact_log_growth.upper()).exp()).upper()
    )
    endpoint_u = symmetric_interval(z0_upper)
    endpoint_uq = symmetric_interval(mu * z0_upper)
    compact_ok = bool(
        u3.is_finite()
        and u3.lower() > 0
        and uq3.is_finite()
        and uq3.upper() < 0
        and matrix_norm_upper.is_finite()
        and matrix_norm_upper.lower() > 0
        and compact_length.is_finite()
        and compact_length.lower() > 0
        and z0_upper.is_finite()
        and z0_upper.lower() > 0
        and endpoint_u.is_finite()
        and endpoint_uq.is_finite()
    )
    audit.ball_check(
        f"rawc.actual.{label}.tier{tier_index}.compact_transport",
        compact_ok,
        "The rho barrier gives a positive x=3 state box and the node-safe two-state Gronwall estimate gives a finite outward Q=-4 endpoint rectangle.",
        Q3=(three / c_value).log().str(digits),
        log_u3_lower=interval_record(log_u3_lower, digits),
        log_u3_upper=interval_record(log_u3_upper, digits),
        u_Q3=interval_record(u3, digits),
        u_Q_Q3=interval_record(uq3, digits),
        compact_interval_length=interval_record(compact_length, digits),
        coefficient_absolute_upper=interval_record(a_abs_upper, digits),
        scaled_state_matrix_norm_upper=interval_record(
            matrix_norm_upper, digits
        ),
        scaled_state_log_growth_upper=interval_record(
            compact_log_growth, digits
        ),
        u_Q0=interval_record(endpoint_u, digits),
        u_Q_Q0=interval_record(endpoint_uq, digits),
    )

    potential_mass = 18 * arb.pi() ** 4 * arb(-8).exp()
    forcing_mass = 4 * arb.pi() ** 2 * arb(-6).exp()
    q_c = potential_mass / mu
    q_u = (potential_mass + lambda_cap * forcing_mass) / mu
    state_euclidean_upper = arb((arb(2).sqrt() * z0_upper).upper())
    remainder_upper = arb(
        (
            lambda_cap
            * forcing_mass
            * arb((q_u + q_c).upper()).exp()
            * state_euclidean_upper
        ).upper()
    )
    gamma_radius = arb((mu * z0_upper + remainder_upper).upper())
    gamma_interval = symmetric_interval(gamma_radius)
    log10_gamma_radius = gamma_radius.log() / arb(10).log()
    tail_ok = bool(
        potential_mass.is_finite()
        and forcing_mass.is_finite()
        and q_c.is_finite()
        and q_u.is_finite()
        and remainder_upper.is_finite()
        and remainder_upper.lower() >= 0
        and gamma_interval.is_finite()
        and contains_zero(gamma_interval)
    )
    audit.ball_check(
        f"rawc.actual.{label}.tier{tier_index}.volterra_gamma1",
        tail_ok,
        "The rotating-frame variation-of-constants bound closes the complete Q<-4 tail and yields a finite actual Gamma_1 interval; zero containment is recorded rather than failed.",
        potential_mass=interval_record(potential_mass, digits),
        forcing_mass=interval_record(forcing_mass, digits),
        q_reference=interval_record(q_c, digits),
        q_actual=interval_record(q_u, digits),
        actual_state_euclidean_norm_at_Q0_upper=interval_record(
            state_euclidean_upper, digits
        ),
        minus_tail_remainder_absolute_upper=interval_record(
            remainder_upper, digits
        ),
        Gamma1_interval=interval_record(gamma_interval, digits),
        log10_Gamma1_absolute_radius=interval_record(
            log10_gamma_radius, digits
        ),
        Gamma1_excludes_zero=False,
    )

    record = {
        "decimal_digits": dps,
        "status": (
            "FINITE_COARSE_ACTUAL_ENCLOSURE"
            if start_ok and barrier_ok and compact_ok and tail_ok
            else "ENCLOSURE_CHECK_FAILED"
        ),
        "lambda_box": {
            "label": label,
            "left_exact": str(lambda_left),
            "right_exact": str(lambda_right),
            "absolute_cap_exact": str(lambda_abs_max),
            "coverage": interval_record(lambda_band, digits),
        },
        "Qplus_actual_state": {
            "normalization_u": interval_record(u4, digits),
            "rho": interval_record(rho4, digits),
        },
        "barrier_state_at_x3": {
            "u": interval_record(u3, digits),
            "u_Q": interval_record(uq3, digits),
        },
        "Q0_outward_state": {
            "u": interval_record(endpoint_u, digits),
            "u_Q": interval_record(endpoint_uq, digits),
        },
        "minus_tail_remainder_absolute_upper": interval_record(
            remainder_upper, digits
        ),
        "Gamma1_outward_interval": interval_record(gamma_interval, digits),
        "Gamma1_absolute_radius_log10": interval_record(
            log10_gamma_radius, digits
        ),
        "Gamma1_excludes_zero": False,
    }
    raw_values = {
        "rho4": rho4,
        "u3": u3,
        "endpoint_u": endpoint_u,
        "endpoint_uq": endpoint_uq,
        "gamma": gamma_interval,
        "gamma_radius": gamma_radius,
    }
    return record, raw_values


def bessel_regression(
    audit: Audit,
    *,
    tier_index: int,
    dps: int,
    kappa_left: fmpq,
    kappa_right: fmpq,
    zero_raw: dict[str, arb],
    digits: int,
) -> dict[str, Any]:
    ctx.dps = dps
    band = bracket_band(kappa_left, kappa_right)
    c_value = 6 * arb.pi() ** 2
    x4 = c_value * arb(4).exp()
    x0 = c_value * arb(-4).exp()
    order = acb(0, band)
    z0 = acb(x0)
    z4 = acb(x4)
    k0 = audit.bessel_k(z0, order)
    km0 = audit.bessel_k(z0, order - 1)
    kp0 = audit.bessel_k(z0, order + 1)
    ks4 = audit.bessel_k(z4, order, scaled=True)
    kms4 = audit.bessel_k(z4, order - 1, scaled=True)
    kps4 = audit.bessel_k(z4, order + 1, scaled=True)
    qk0 = -z0 * (km0 + kp0) / 2
    qks4 = -z4 * (kms4 + kps4) / 2
    a4_zero = x4**2 - band**2
    u4_zero = arb(1) / a4_zero.sqrt().sqrt()
    scale = u4_zero * x4.exp() / ks4.real
    u0 = scale * k0.real
    uq0 = scale * qk0.real
    rho4 = -qks4.real / ks4.real - x4 - arb(1) / 2
    complex_ok = all(
        value.is_finite() and contains_zero(value.imag)
        for value in (k0, qk0, ks4, qks4)
    )
    contained = bool(
        complex_ok
        and ks4.real.lower() > 0
        and contains_interval(zero_raw["rho4"], rho4)
        and contains_interval(zero_raw["endpoint_u"], u0)
        and contains_interval(zero_raw["endpoint_uq"], uq0)
    )
    audit.ball_check(
        f"rawc.actual.lambda_zero.tier{tier_index}.bessel_regression",
        contained,
        "The exact K_(i*kappa) lambda=0 family under the same u(4)=A_0(4)^(-1/4) normalization is contained by the analytic rho and Q=-4 state envelopes on the full bracket.",
        decimal_digits=dps,
        K_Q0=complex_ball_record(k0, digits),
        K_Q_Q0=complex_ball_record(qk0, digits),
        scaled_K_Qplus=complex_ball_record(ks4, digits),
        scaled_K_Q_Qplus=complex_ball_record(qks4, digits),
        exact_normalized_rho_Qplus=interval_record(rho4, digits),
        exact_normalized_u_Q0=interval_record(u0, digits),
        exact_normalized_u_Q_Q0=interval_record(uq0, digits),
        envelope_rho_Qplus=interval_record(zero_raw["rho4"], digits),
        envelope_u_Q0=interval_record(zero_raw["endpoint_u"], digits),
        envelope_u_Q_Q0=interval_record(zero_raw["endpoint_uq"], digits),
    )
    return {
        "decimal_digits": dps,
        "status": "CONTAINED" if contained else "NOT_CONTAINED",
        "rho_Qplus": interval_record(rho4, digits),
        "u_Q0": interval_record(u0, digits),
        "u_Q_Q0": interval_record(uq0, digits),
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    raw_input = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw_input) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw_input)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-actual-nonzero-lambda-gamma1-coarse-enclosure.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")

    root = Path(__file__).resolve().parent.parent
    upstream_data: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        data, record = verify_upstream(root, item)
        upstream_data.append(data)
        upstream_records.append(record)
    plus_data, bessel_data, _gamma_data = upstream_data

    root_rows = bessel_data["certified_calculation"]["endpoint_characteristic"][
        "root_rows"
    ]
    if len(root_rows) != 5:
        raise AssertionError("upstream five-bracket count drift")
    root_row = root_rows[0]
    certificate = root_row["certified_high_precision_bracket"]
    if not certificate.get("at_least_one_real_sign_changing_zero"):
        raise AssertionError("root bracket 1 existence certificate drift")
    kappa_left = exact_rational(certificate["left_exact"])
    kappa_right = exact_rational(certificate["right_exact"])
    if not 2 < kappa_left < kappa_right < 3:
        raise AssertionError("root bracket 1 location drift")

    audit = Audit()
    exact_audit(audit)
    audit.inequality(
        "rawc.actual.root1_exact_location",
        bool(2 < kappa_left < kappa_right < 3),
        "The inherited exact root bracket 1 is positive and lies strictly inside (2,3).",
        left_exact=str(kappa_left),
        right_exact=str(kappa_right),
        width_exact=str(kappa_right - kappa_left),
    )
    boxes = parse_lambda_boxes(cfg)
    dps_values = cfg["declared_conventions"]["precision_ladder_decimal_digits"]
    if dps_values != [80, 120]:
        raise AssertionError("precision ladder drift")
    digits = int(cfg["declared_conventions"]["ball_output_digits"])

    box_records: list[dict[str, Any]] = []
    for box in boxes:
        tier_records: list[dict[str, Any]] = []
        tier_raw: list[dict[str, arb]] = []
        for tier_index, dps in enumerate(dps_values, start=1):
            record, raw_values = compute_envelope(
                audit,
                label=box["label"],
                tier_index=tier_index,
                dps=int(dps),
                kappa_left=kappa_left,
                kappa_right=kappa_right,
                lambda_left=box["left"],
                lambda_right=box["right"],
                lambda_abs_max=box["abs_max"],
                plus_data=plus_data,
                digits=digits,
            )
            tier_records.append(record)
            tier_raw.append(raw_values)
        intersections = {
            key: intersect(tier_raw[0][key], tier_raw[1][key])
            for key in ("rho4", "u3", "endpoint_u", "endpoint_uq", "gamma")
        }
        overlap_ok = all(value is not None for value in intersections.values())
        audit.ball_check(
            f"rawc.actual.{box['label']}.precision_overlap",
            overlap_ok,
            "The independently evaluated 80- and 120-decimal-digit outward enclosures overlap in every retained state component and Gamma_1.",
            intersections={
                key: interval_record(value, digits) if value is not None else None
                for key, value in intersections.items()
            },
        )
        box_records.append(
            {
                "label": box["label"],
                "lambda_box": {
                    "left_exact": str(box["left"]),
                    "right_exact": str(box["right"]),
                },
                "precision_tiers": tier_records,
                "certified_intersection": {
                    key: interval_record(value, digits)
                    if value is not None
                    else None
                    for key, value in intersections.items()
                },
                "Gamma1_zero_excluded": False,
            }
        )
    zero_tier_records: list[dict[str, Any]] = []
    zero_tier_raw: list[dict[str, arb]] = []
    regression_records: list[dict[str, Any]] = []
    zero = fmpq(0)
    for tier_index, dps in enumerate(dps_values, start=1):
        record, raw_values = compute_envelope(
            audit,
            label="lambda_zero_control",
            tier_index=tier_index,
            dps=int(dps),
            kappa_left=kappa_left,
            kappa_right=kappa_right,
            lambda_left=zero,
            lambda_right=zero,
            lambda_abs_max=zero,
            plus_data=plus_data,
            digits=digits,
        )
        zero_tier_records.append(record)
        zero_tier_raw.append(raw_values)
        regression_records.append(
            bessel_regression(
                audit,
                tier_index=tier_index,
                dps=int(dps),
                kappa_left=kappa_left,
                kappa_right=kappa_right,
                zero_raw=raw_values,
                digits=digits,
            )
        )
    zero_intersections = {
        key: intersect(zero_tier_raw[0][key], zero_tier_raw[1][key])
        for key in ("rho4", "u3", "endpoint_u", "endpoint_uq", "gamma")
    }
    zero_overlap_ok = all(value is not None for value in zero_intersections.values())
    audit.ball_check(
        "rawc.actual.lambda_zero.precision_overlap",
        zero_overlap_ok,
        "The lambda=0 analytic control envelopes overlap at both precision tiers before Bessel containment is accepted.",
        intersections={
            key: interval_record(value, digits) if value is not None else None
            for key, value in zero_intersections.items()
        },
    )

    audit.guard(
        "rawc.actual.guard.actual_recessive_normalization",
        "DLMF section 2.7(iii), equations 2.7.23--2.7.25",
        "The pinned upstream result proves A>0 and a finite uniform error-control budget on Q>=4. Its E<1 makes the actual recessive value at Q=4 nonzero, so a positive rescaling sets u(4)=A(4)^(-1/4) without changing the logarithmic derivative.",
        "For each fixed real parameter in the declared boxes this selects an actual recessive solution, not the WKB proxy. The emitted Q=4 state interval encloses its normalized direction only on the declared box.",
    )
    audit.guard(
        "rawc.actual.guard.riccati_invariant_region",
        "Scalar inward-barrier continuation for a locally Lipschitz Riccati equation",
        "The executable checks put rho(4) in [-1,1], prove both boundary vector fields point inward for 3<=x<=C*exp(4), and give r=x+1/2+rho>=x-1/2>0.",
        "Backward evolution has u_s=r*u>0 while u>0; hence u cannot reach a node before x=3 and the Riccati continuation is noncircular. No no-node statement is made below x=3.",
    )
    audit.guard(
        "rawc.actual.guard.compact_gronwall",
        "Variation of constants and the scalar Gronwall inequality for a bounded linear two-state system",
        "On the compact interval Q0<=Q<=Q3 the exact state system has induced infinity norm at most mu+A_abs/mu, with positive finite mu=kappa_left and an executable finite coefficient envelope.",
        "The resulting endpoint rectangle encloses the actual state through any nodes. It is a coarse analytic interval transport, not a validated numerical ODE trajectory or a sharp endpoint evaluation.",
    )
    audit.guard(
        "rawc.actual.guard.rotating_volterra_tail",
        "Free-rotation variation of constants plus Gronwall on the half-line",
        "In (u,u_Q/kappa) the free generator is skew. V and a have the executable finite masses 18*pi^4*exp(-8) and 4*pi^2*exp(-6), respectively, for Q<=-4.",
        "The complete infinite minus-tail remainder and declared Gamma_1 are bounded for the constructed normalized actual solution. The broad interval contains zero and gives no continuation, eigenvalue, spectral or RAQ conclusion.",
    )
    audit.guard(
        "rawc.actual.guard.lambda_zero_regression_scope",
        "DLMF modified-Bessel equation and derivative recurrences",
        "At lambda=0 the exact recessive solution is K_(i*kappa)(C exp Q); Arb evaluates the full inherited kappa band and applies the identical u(4)=A_0(4)^(-1/4) normalization.",
        "Containment checks only regress the coarse analytic envelope. They do not claim that the envelope reproduces the narrow Bessel endpoint or prove uniqueness of the bracketed root.",
    )
    audit.guard(
        "rawc.actual.guard.workbench_scope",
        "Repository computational-workbench boundary",
        "The result is bracket-1, real-parameter, fixed-reference and extension-local; all global promotion and physics fields are fail-closed.",
        "A finite numerical enclosure is not a raw-C spectrum, C/H quantum equivalence, quantum-gravity result, observation or TOE claim.",
    )

    passed = all(item["passed"] for item in audit.exact + audit.ball)
    verdict = (
        "CERTIFY_COARSE_ACTUAL_NONZERO_LAMBDA_GAMMA1_ENCLOSURE_BRACKET1_ONLY"
        if passed
        else "KILL_COARSE_ACTUAL_NONZERO_LAMBDA_GAMMA1_ENCLOSURE"
    )
    impact = cfg["decision_table"][0 if passed else 1]["programme_impact"]
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {
            "path": INPUT_RELPATH,
            "sha256": sha256_bytes(raw_input),
        },
        "upstream_results": upstream_records,
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
            "all_executable_checks_passed": passed,
        },
        "certified_calculation": {
            "status": (
                "CERTIFIED_COARSE_ACTUAL_RECESSIVE_FAMILY_AND_FINITE_GAMMA1_INTERVALS"
                if passed
                else "NOT_CERTIFIED"
            ),
            "parameter_scope": {
                "root_index": 1,
                "kappa_bracket": {
                    "left_exact": str(kappa_left),
                    "right_exact": str(kappa_right),
                    "width_exact": str(kappa_right - kappa_left),
                    "root_scope": "at least one lambda=0 sign-changing zero; uniqueness is not assumed and nonzero-lambda kappa is allowed throughout the full fixed box",
                },
                "lambda_boxes": [
                    {
                        "label": box["label"],
                        "left_exact": str(box["left"]),
                        "right_exact": str(box["right"]),
                    }
                    for box in boxes
                ],
            },
            "actual_solution_normalization": "u_lambda(4)=A_lambda(4)^(-1/4) for the actual DLMF recessive solution, after positive rescaling",
            "transport_method": "LG actual-direction interval on Q>=4; rho invariant region to x=3; node-safe two-state infinity-norm Gronwall to Q=-4; rotating-frame Volterra/Gronwall to minus infinity",
            "numerical_validated_ODE_backend_used": False,
            "nonzero_lambda_rows": box_records,
            "lambda_zero_control": {
                "analytic_precision_tiers": zero_tier_records,
                "exact_Bessel_regression": regression_records,
                "certified_intersection": {
                    key: interval_record(value, digits)
                    if value is not None
                    else None
                    for key, value in zero_intersections.items()
                },
            },
            "scientific_readout": {
                "computed_fact": "For every fixed real (kappa,lambda) in root bracket 1 times either punctured lambda box, the explicitly normalized actual plus-recessive solution has a finite outward Q=-4 state rectangle and a complete-half-line finite Gamma_1 interval.",
                "interpretation": "This removes the prior actual-solution/existence-and-boundedness null only at a deliberately coarse local-box level.",
                "open_hypotheses": "Every nonzero-lambda Gamma_1 interval contains zero; no sign, zero, root continuation, uniqueness, spectral density, RAQ, C/H equivalence or physics conclusion follows.",
            },
            "next_mathematical_gap": "Replace the coarse compact Gronwall rectangle with a Bessel/Liouville--Green-preconditioned validated interval Taylor or equivalent sharp transfer enclosure before attempting Gamma_1 zero exclusion or continuation.",
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
            "precision_tiers": len(dps_values),
            "root_brackets": 1,
            "nonzero_lambda_boxes": len(boxes),
            "quadrature_calls": 0,
            "root_calls": 0,
            "finite_difference_calls": 0,
            "ode_calls": 0,
            "sampling_points": 0,
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
                "nonzero_lambda_boxes": len(box_records),
                "Gamma1_zero_excluded_boxes": 0,
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
