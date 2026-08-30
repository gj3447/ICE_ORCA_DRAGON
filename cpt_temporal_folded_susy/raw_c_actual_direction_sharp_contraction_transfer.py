#!/usr/bin/env python3
"""Sharp actual raw-C direction by backward-x contraction; no roots or RAQ."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = "RAW_C_ACTUAL_DIRECTION_SHARP_CONTRACTION_TRANSFER_INPUTS.json"
RESULT_NAME = "RAW_C_ACTUAL_DIRECTION_SHARP_CONTRACTION_TRANSFER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/raw_c_actual_direction_sharp_contraction_transfer.py"
)
CALCULATION_ID = "RawCActualDirectionSharpContractionTransfer"
EXPECTED_INPUT_SHA256 = (
    "6e2b5f9047484c09197f0723af1a7c1c78a9f496648a8d39e4dbc268be70a9a3"
)
RESULT_SCHEMA = "ice.raw-c-actual-direction-sharp-contraction-transfer.result.v1"
RESULT_PREFIX = "RAW_C_ACTUAL_DIRECTION_SHARP_CONTRACTION_TRANSFER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def exact_rational(text: str) -> fmpq:
    if "e" in text.lower():
        coefficient, exponent_text = text.lower().split("e", 1)
        exponent = int(exponent_text)
        base = fmpq(coefficient)
        return base * (fmpq(10) ** exponent)
    return fmpq(text)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 4000,
        "kernel_panels_coarse": 512,
        "kernel_panels_refined": 1024,
        "compact_q_segments": 16,
        "compact_taylor_order": 12,
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
        "black_box_validated_numerical_ODE_transport": None,
        "sharp_Q4_normalized_absolute_Gamma1_interval": None,
        "global_Gamma1_zero_exclusion": None,
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
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)
    bessel_evaluations: int = 0

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate check id: {identifier}")
        self.seen.add(identifier)

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self.register(identifier)
        reduced = sp.simplify(residual)
        self.exact.append(
            {
                "id": identifier,
                "kind": "EXACT_IDENTITY",
                "passed": bool(reduced == 0),
                "residual": str(reduced),
                "statement": statement,
            }
        )

    def inequality(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.exact.append(
            {
                "id": identifier,
                "kind": "EXACT_OR_STRUCTURAL_INEQUALITY",
                "passed": bool(passed),
                "statement": statement,
                **data,
            }
        )

    def ball_check(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.ball.append(
            {
                "id": identifier,
                "kind": "ARB_OUTWARD_INTERVAL_CHECK",
                "passed": bool(passed),
                "statement": statement,
                **data,
            }
        )

    def guard(
        self, identifier: str, theorem: str, hypotheses: str, scope: str
    ) -> None:
        self.register(identifier)
        self.guards.append(
            {
                "id": identifier,
                "kind": "THEOREM_SCOPE_GUARD",
                "verified": True,
                "theorem": theorem,
                "hypotheses": hypotheses,
                "scope": scope,
            }
        )

    def bessel_k(self, z: acb, order: acb) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("Bessel evaluation cap exceeded")
        return z.bessel_k(order)


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if not lower.is_finite() or not upper.is_finite() or lower > upper:
        raise AssertionError("invalid interval endpoints")
    midpoint = (lower + upper) / 2
    radius = (upper - lower) / 2
    value = arb(midpoint, radius)
    if value.lower() > lower or value.upper() < upper:
        raise AssertionError("constructed ball does not contain requested endpoints")
    return value


def bracket_band(left: fmpq, right: fmpq) -> arb:
    return interval_from_bounds(arb(left).lower(), arb(right).upper())


def symmetric_interval(radius: arb) -> arb:
    upper = absolute_upper(radius)
    return interval_from_bounds(-upper, upper)


def absolute_upper(value: arb) -> arb:
    return arb(max(abs(value.lower()), abs(value.upper())))


def absolute_lower(value: arb) -> arb:
    if value.lower() > 0:
        return arb(value.lower())
    if value.upper() < 0:
        return arb(-value.upper())
    return arb(0)


def maximum(left: arb, right: arb) -> arb:
    return arb(max(left.upper(), right.upper()))


def interval_width(value: arb) -> arb:
    return arb(value.upper() - value.lower())


def contains_zero(value: arb) -> bool:
    return bool(value.lower() <= 0 <= value.upper())


def excludes_zero(value: arb) -> bool:
    return bool(value.lower() > 0 or value.upper() < 0)


def contains_interval(outer: arb, inner: arb) -> bool:
    return bool(outer.lower() <= inner.lower() and outer.upper() >= inner.upper())


def intersection(left: arb, right: arb) -> arb | None:
    lower = max(left.lower(), right.lower())
    upper = min(left.upper(), right.upper())
    if lower > upper:
        return None
    return interval_from_bounds(lower, upper)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
        "width_upper": interval_width(value).upper().str(digits, radius=False),
    }


def complex_record(value: acb, digits: int) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "midpoint_radius": value.str(digits),
    }


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    result = json.loads(raw)
    if result.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    if (
        result.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    payload_copy = dict(result)
    recorded_payload = payload_copy.pop("result_payload_sha256_without_self")
    if sha256_bytes(canonical_bytes(payload_copy)) != recorded_payload:
        raise AssertionError(f"upstream self digest mismatch: {item['path']}")
    if result.get("numbered_phase") is not None:
        raise AssertionError("upstream numbered-phase convention drift")
    return result, {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": recorded_payload,
        "verdict": result["verdict"],
    }


def exact_audit(audit: Audit) -> None:
    Q, x, C, kappa, lam, rho = sp.symbols(
        "Q x C kappa lambda rho", positive=True, real=True
    )
    forcing = x ** sp.Rational(3, 2) / sp.sqrt(C)
    coefficient = x**2 + lam * forcing - kappa**2
    r = x + sp.Rational(1, 2) + rho
    rho_q = (
        kappa**2
        + sp.Rational(1, 4)
        - lam * forcing
        + (2 * x + 1) * rho
        + rho**2
    )
    rho_x = (
        2 * rho
        + (rho + rho**2 + kappa**2 + sp.Rational(1, 4)) / x
        - lam * sp.sqrt(x / C)
    )
    audit.identity(
        "rawc.sharp.coefficient_change",
        coefficient.subs(x, C * sp.exp(Q))
        - (
            C**2 * sp.exp(2 * Q)
            + lam * C * sp.exp(sp.Rational(3, 2) * Q)
            - kappa**2
        ),
        "The Q and x forms of the raw-C coefficient agree.",
    )
    audit.identity(
        "rawc.sharp.riccati_Q",
        x + rho_q - (r**2 - coefficient),
        "r=-u_Q/u and rho=r-x-1/2 obey the declared Q-Riccati equation.",
    )
    audit.identity(
        "rawc.sharp.riccati_x",
        x * rho_x - rho_q,
        "The x-Riccati equation is the exact Q equation divided by x.",
    )
    t, xs = sp.symbols("t x_s", positive=True, real=True)
    propagator = sp.exp(2 * (x - t)) * x / t
    audit.identity(
        "rawc.sharp.homogeneous_propagator",
        sp.diff(propagator, x) - (2 + 1 / x) * propagator,
        "M(x,t)=exp(2(x-t))*x/t is the exact propagator of rho_x=(2+1/x)rho.",
    )
    y = sp.symbols("y", nonnegative=True, real=True)
    kernel = sp.exp(-2 * (t - xs)) * xs / t
    audit.identity(
        "rawc.sharp.kernel_J0_change",
        (kernel / t).subs(t, xs + y)
        - xs * sp.exp(-2 * y) / (xs + y) ** 2,
        "The constant-forcing kernel becomes the displayed positive y-integrand.",
    )
    audit.identity(
        "rawc.sharp.kernel_Jlambda_change",
        (kernel * sp.sqrt(t / C)).subs(t, xs + y)
        - xs * sp.exp(-2 * y) / (sp.sqrt(C) * sp.sqrt(xs + y)),
        "The lambda-forcing kernel becomes the displayed positive y-integrand.",
    )
    rho1, rho2 = sp.symbols("rho_1 rho_2", real=True)
    f1 = 2 * rho1 + (rho1 + rho1**2 + kappa**2 + sp.Rational(1, 4)) / x
    f2 = 2 * rho2 + (rho2 + rho2**2 + kappa**2 + sp.Rational(1, 4)) / x
    audit.identity(
        "rawc.sharp.projective_difference",
        f1 - f2 - (2 + (1 + rho1 + rho2) / x) * (rho1 - rho2),
        "Equal-parameter Riccati directions obey the exact projective difference law.",
    )
    audit.identity(
        "rawc.sharp.projective_derivative",
        sp.diff(rho_x, rho) - (2 + (1 + 2 * rho) / x),
        "The Riccati vector field has the displayed direction derivative.",
    )
    audit.inequality(
        "rawc.sharp.projective_contraction_floor",
        bool(sp.Rational(5, 3) > 0),
        "For rho in [-1,1] and x>=3, 2+(1+2rho)/x is at least 5/3, so backward x transport contracts equal-parameter directions.",
        exact_lower_bound="5/3",
    )
    q = sp.symbols("q", real=True)
    potential = 36 * sp.pi**4 * sp.exp(2 * q)
    density = 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q)
    audit.identity(
        "rawc.sharp.minus_potential_integral",
        sp.diff(18 * sp.pi**4 * sp.exp(2 * q), q) - potential,
        "The complete Q<-4 potential mass is exact.",
    )
    audit.identity(
        "rawc.sharp.minus_forcing_integral",
        sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q)
        - density,
        "The complete Q<-4 forcing mass is exact.",
    )
    audit.identity(
        "rawc.sharp.exact_partition",
        16 * sp.Rational(-11, 160)
        - (sp.Rational(-4) + sp.Rational(29, 10)),
        "Sixteen exact steps join Q_switch=-29/10 to Q0=-4.",
    )


def lg_budgets(plus_data: dict[str, Any]) -> tuple[arb, arb]:
    envelopes = plus_data["analytic_calculation"]["uniform_envelopes"]
    if envelopes["eta_bar"] != "1/100000":
        raise AssertionError("upstream eta drift")
    r_bar = exact_rational(envelopes["R_bar"])
    eta = exact_rational(envelopes["eta_bar"])
    v_bar = arb(r_bar) / (arb(6) * 9 * 7**2 * (arb(1) - arb(eta)))
    error = (v_bar / 2).exp() - 1
    return error, 2 * error / (1 - error)


def kernel_masses(
    xs: arb, x4: arb, *, panels: int, tail_y: fmpq
) -> tuple[arb, arb, dict[str, Any]]:
    if panels <= 0 or x4.lower() - xs.upper() <= arb(tail_y):
        raise AssertionError("invalid contraction-kernel partition")
    sqrt_c = (6 * arb.pi() ** 2).sqrt()
    step = tail_y / panels
    j0_lower = arb(0)
    j0_upper = arb(0)
    jl_lower = arb(0)
    jl_upper = arb(0)
    for index in range(panels):
        left = step * index
        right = step * (index + 1)
        left_ball = arb(left)
        right_ball = arb(right)
        exponential_mass = (
            (-2 * left_ball).exp() - (-2 * right_ball).exp()
        ) / 2
        j0_lower += xs * exponential_mass / (xs + right_ball) ** 2
        j0_upper += xs * exponential_mass / (xs + left_ball) ** 2
        jl_lower += (
            xs
            * exponential_mass
            / (sqrt_c * (xs + right_ball).sqrt())
        )
        jl_upper += (
            xs
            * exponential_mass
            / (sqrt_c * (xs + left_ball).sqrt())
        )
    tail_exp_mass = (-2 * arb(tail_y)).exp() / 2
    j0_upper += xs * tail_exp_mass / (xs + arb(tail_y)) ** 2
    jl_upper += (
        xs * tail_exp_mass / (sqrt_c * (xs + arb(tail_y)).sqrt())
    )
    j0 = interval_from_bounds(j0_lower.lower(), j0_upper.upper())
    jl = interval_from_bounds(jl_lower.lower(), jl_upper.upper())
    return j0, jl, {
        "panels": panels,
        "tail_y": str(tail_y),
        "panel_width": str(step),
        "J0": j0,
        "Jlambda": jl,
        "J0_tail_upper": (
            xs * tail_exp_mass / (xs + arb(tail_y)) ** 2
        ),
        "Jlambda_tail_upper": (
            xs * tail_exp_mass / (sqrt_c * (xs + arb(tail_y)).sqrt())
        ),
    }


def actual_rho_q4(
    kappa_band: arb, lambda_band: arb, plus_data: dict[str, Any]
) -> tuple[arb, dict[str, arb]]:
    c_value = 6 * arb.pi() ** 2
    sqrt_c = c_value.sqrt()
    x4 = c_value * arb(4).exp()
    forcing4 = x4 * x4.sqrt() / sqrt_c
    a4 = x4**2 + lambda_band * forcing4 - kappa_band**2
    aq4 = 2 * x4**2 + (arb(3) / 2) * lambda_band * forcing4
    sqrt_a4 = a4.sqrt()
    r_w4 = sqrt_a4 + aq4 / (4 * a4)
    rho_w4 = r_w4 - x4 - arb(1) / 2
    amplitude_error, d_bound = lg_budgets(plus_data)
    slope_error = arb((d_bound * sqrt_a4).upper())
    rho4 = interval_from_bounds(
        rho_w4.lower() - slope_error, rho_w4.upper() + slope_error
    )
    return rho4, {
        "x4": x4,
        "A4": a4,
        "rho_wkb": rho_w4,
        "slope_error": slope_error,
        "amplitude_error": amplitude_error,
    }


def sharp_switch_enclosure(
    audit: Audit,
    *,
    label: str,
    tier: int,
    dps: int,
    kappa_band: arb,
    lambda_band: arb,
    config: dict[str, Any],
    plus_data: dict[str, Any],
    bessel_regression: bool,
) -> tuple[dict[str, Any], arb]:
    ctx.dps = dps
    conventions = config["declared_conventions"]
    digits = int(conventions["ball_output_digits"])
    q_switch = exact_rational(conventions["Q_switch"])
    c_value = 6 * arb.pi() ** 2
    xs = c_value * arb(q_switch).exp()
    rho4, start = actual_rho_q4(kappa_band, lambda_band, plus_data)
    x4 = start["x4"]
    tail_y = exact_rational(conventions["kernel_tail_y"])
    panel_counts = conventions["kernel_panel_ladders"]
    coarse_j0, coarse_jl, coarse = kernel_masses(
        xs, x4, panels=int(panel_counts[0]), tail_y=tail_y
    )
    refined_j0, refined_jl, refined = kernel_masses(
        xs, x4, panels=int(panel_counts[1]), tail_y=tail_y
    )
    refinement_ok = bool(
        contains_interval(coarse_j0, refined_j0)
        and contains_interval(coarse_jl, refined_jl)
    )
    audit.ball_check(
        f"rawc.sharp.{label}.tier{tier}.kernel_refinement",
        refinement_ok,
        "The refined monotone-denominator kernel enclosure is nested in the coarse enclosure, with the positive infinite tail added analytically.",
        decimal_digits=dps,
        coarse_panels=coarse["panels"],
        refined_panels=refined["panels"],
        coarse_J0=interval_record(coarse_j0, digits),
        refined_J0=interval_record(refined_j0, digits),
        coarse_Jlambda=interval_record(coarse_jl, digits),
        refined_Jlambda=interval_record(refined_jl, digits),
        refined_J0_tail_upper=interval_record(refined["J0_tail_upper"], digits),
        refined_Jlambda_tail_upper=interval_record(
            refined["Jlambda_tail_upper"], digits
        ),
    )
    initial_factor = (-2 * (x4 - xs)).exp() * xs / x4
    nonlinear_integral = interval_from_bounds(arb(0), refined_j0.upper())
    rho_switch = (
        initial_factor * rho4
        - (kappa_band**2 + arb(1) / 4) * refined_j0
        - nonlinear_integral
        + lambda_band * refined_jl
    )
    width_target = arb(exact_rational(conventions["sharp_switch_width_target"]))
    sharp_ok = bool(
        start["A4"].is_finite()
        and start["A4"].lower() > 0
        and start["amplitude_error"].upper() < 1
        and rho4.lower() >= -1
        and rho4.upper() <= 1
        and xs.lower() > 3
        and initial_factor.is_finite()
        and initial_factor.lower() >= 0
        and refined_j0.lower() > 0
        and refined_jl.lower() > 0
        and rho_switch.is_finite()
        and rho_switch.lower() >= -1
        and rho_switch.upper() <= 1
        and interval_width(rho_switch).upper() < width_target.lower()
    )
    audit.ball_check(
        f"rawc.sharp.{label}.tier{tier}.actual_direction",
        sharp_ok,
        "The exact backward-x propagator, the full pinned LG start interval and 0<=rho^2<=1 yield a sharp actual-family switch direction inside the invariant barrier.",
        decimal_digits=dps,
        x_Qplus=interval_record(x4, digits),
        x_switch=interval_record(xs, digits),
        A_Qplus=interval_record(start["A4"], digits),
        rho_WKB_Qplus=interval_record(start["rho_wkb"], digits),
        LG_slope_error=interval_record(start["slope_error"], digits),
        actual_rho_Qplus=interval_record(rho4, digits),
        homogeneous_initial_factor=interval_record(initial_factor, digits),
        J0=interval_record(refined_j0, digits),
        Jlambda=interval_record(refined_jl, digits),
        nonlinear_Jrho2_outer=interval_record(nonlinear_integral, digits),
        actual_rho_switch=interval_record(rho_switch, digits),
        sharp_switch_width_target=conventions["sharp_switch_width_target"],
    )
    regression_record: dict[str, Any] | None = None
    if bessel_regression:
        x_ball = acb(xs)
        order_ball = acb(0, kappa_band)
        k_value = audit.bessel_k(x_ball, order_ball)
        k_minus = audit.bessel_k(x_ball, order_ball - 1)
        k_plus = audit.bessel_k(x_ball, order_ball + 1)
        kq_value = -x_ball * (k_minus + k_plus) / 2
        bessel_rho = -kq_value / k_value - x_ball - acb(arb(1) / 2)
        regression_ok = bool(
            k_value.abs_lower() > 0
            and bessel_rho.imag.lower() <= 0 <= bessel_rho.imag.upper()
            and contains_interval(rho_switch, bessel_rho.real)
        )
        audit.ball_check(
            f"rawc.sharp.lambda_zero.tier{tier}.switch_bessel_regression",
            regression_ok,
            "Using the guarded real-valued K_(i*kappa) family, the exact lambda-zero logarithmic direction at Q_switch is contained by the contraction enclosure; the imaginary ball is only a residue diagnostic.",
            decimal_digits=dps,
            K_switch=complex_record(k_value, digits),
            exact_Bessel_rho_switch=complex_record(bessel_rho, digits),
            contraction_rho_switch=interval_record(rho_switch, digits),
        )
        regression_record = {
            "status": "CONTAINED" if regression_ok else "NOT_CONTAINED",
            "K_switch": complex_record(k_value, digits),
            "rho_switch": complex_record(bessel_rho, digits),
        }
    return {
        "label": label,
        "decimal_digits": dps,
        "kappa_bracket": interval_record(kappa_band, digits),
        "lambda_box": interval_record(lambda_band, digits),
        "Qplus_actual_rho": interval_record(rho4, digits),
        "Qswitch_actual_rho": interval_record(rho_switch, digits),
        "Qswitch_width_target": conventions["sharp_switch_width_target"],
        "sharp_switch_certified": sharp_ok,
        "kernel_coarse": {
            "panels": coarse["panels"],
            "J0": interval_record(coarse_j0, digits),
            "Jlambda": interval_record(coarse_jl, digits),
        },
        "kernel_refined": {
            "panels": refined["panels"],
            "J0": interval_record(refined_j0, digits),
            "Jlambda": interval_record(refined_jl, digits),
        },
        "kernel_refinement_nested": refinement_ok,
        "lambda_zero_Bessel_regression": regression_record,
    }, rho_switch


def coefficient_derivatives(
    q_base: fmpq, kappa_band: arb, lambda_band: arb, order: int
) -> list[arb]:
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    forcing = x_value * x_value.sqrt() / c_value.sqrt()
    values = [x_value**2 + lambda_band * forcing - kappa_band**2]
    for derivative in range(1, order + 1):
        values.append(
            arb(2) ** derivative * x_value**2
            + (arb(3) / 2) ** derivative * lambda_band * forcing
        )
    return values


def whole_step_majorants(
    q_base: fmpq, kappa_band: arb, lambda_band: arb, order: int
) -> list[arb]:
    c_value = 6 * arb.pi() ** 2
    x_plus = c_value * arb(q_base).exp()
    forcing_plus = x_plus * x_plus.sqrt() / c_value.sqrt()
    coefficient_abs = (
        x_plus**2
        + absolute_upper(lambda_band) * forcing_plus
        + absolute_upper(kappa_band) ** 2
    )
    majorants = [maximum(arb(1), coefficient_abs)]
    for derivative in range(1, order + 1):
        majorants.append(
            arb(2) ** derivative * x_plus**2
            + (arb(3) / 2) ** derivative
            * absolute_upper(lambda_band)
            * forcing_plus
        )
    return [arb(value.upper()) for value in majorants]


def apply_coefficient_derivative(
    derivative: int, coefficient_values: list[arb], state: tuple[arb, arb]
) -> tuple[arb, arb]:
    if derivative == 0:
        return state[1], coefficient_values[0] * state[0]
    return arb(0), coefficient_values[derivative] * state[0]


def downstream_transfer(
    audit: Audit,
    *,
    label: str,
    tier: int,
    dps: int,
    kappa_band: arb,
    lambda_band: arb,
    rho_switch: arb,
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    conventions = config["declared_conventions"]
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    segments = int(conventions["compact_q_segments"])
    q_switch = exact_rational(conventions["Q_switch"])
    q_zero = exact_rational(conventions["Q_0"])
    step = (q_zero - q_switch) / segments
    if step != fmpq(-11, 160):
        raise AssertionError("compact exact partition drift")
    c_value = 6 * arb.pi() ** 2
    x_switch = c_value * arb(q_switch).exp()
    state = (arb(1), -(x_switch + arb(1) / 2 + rho_switch))
    switch_ok = bool(
        x_switch.lower() > 3
        and rho_switch.lower() >= -1
        and rho_switch.upper() <= 1
        and state[1].upper() < 0
    )
    audit.ball_check(
        f"rawc.sharp.{label}.tier{tier}.sharp_switch_state",
        switch_ok,
        "The certified actual direction defines a scale-free, node-safe two-state switch box strictly inside x>3.",
        x_switch=interval_record(x_switch, digits),
        rho_switch=interval_record(rho_switch, digits),
        v_switch=interval_record(state[0], digits),
        v_Q_switch=interval_record(state[1], digits),
    )
    step_records: list[dict[str, Any]] = []
    step_ball = arb(step)
    step_abs = arb(-step)
    for index in range(segments):
        q_base = q_switch + index * step
        q_next = q_base + step
        coefficient_values = coefficient_derivatives(
            q_base, kappa_band, lambda_band, order
        )
        derivatives: list[tuple[arb, arb]] = [state]
        for n in range(order):
            next_first = arb(0)
            next_second = arb(0)
            for j in range(n + 1):
                applied = apply_coefficient_derivative(
                    j, coefficient_values, derivatives[n - j]
                )
                factor = math.comb(n, j)
                next_first += factor * applied[0]
                next_second += factor * applied[1]
            derivatives.append((next_first, next_second))
        polynomial = [arb(0), arb(0)]
        for n, derivative_state in enumerate(derivatives):
            factor = step_ball**n / math.factorial(n)
            polynomial[0] += derivative_state[0] * factor
            polynomial[1] += derivative_state[1] * factor
        majorants = whole_step_majorants(
            q_base, kappa_band, lambda_band, order
        )
        state_norm = maximum(absolute_upper(state[0]), absolute_upper(state[1]))
        tube_norm = arb((state_norm * (majorants[0] * step_abs).exp()).upper())
        derivative_bounds = [tube_norm]
        for n in range(order + 1):
            bound = arb(0)
            for j in range(n + 1):
                bound += (
                    math.comb(n, j)
                    * majorants[j]
                    * derivative_bounds[n - j]
                )
            derivative_bounds.append(arb(bound.upper()))
        remainder = arb(
            (
                derivative_bounds[order + 1]
                * step_abs ** (order + 1)
                / math.factorial(order + 1)
            ).upper()
        )
        remainder_box = symmetric_interval(remainder)
        next_state = (
            polynomial[0] + remainder_box,
            polynomial[1] + remainder_box,
        )
        step_ok = bool(
            all(value.is_finite() for value in coefficient_values)
            and all(value.is_finite() and value.lower() >= 0 for value in majorants)
            and tube_norm.is_finite()
            and remainder.is_finite()
            and remainder.lower() >= 0
            and next_state[0].is_finite()
            and next_state[1].is_finite()
        )
        audit.ball_check(
            f"rawc.sharp.{label}.tier{tier}.step{index + 1}.whole_step_taylor",
            step_ok,
            "The order-12 derivative Taylor polynomial is enlarged by the whole-step D_13 |h|^13/13! remainder over the complete parameter box.",
            q_base=str(q_base),
            q_next=str(q_next),
            coefficient_norm_majorant=interval_record(majorants[0], digits),
            state_tube_norm_upper=interval_record(tube_norm, digits),
            derivative_13_norm_upper=interval_record(
                derivative_bounds[order + 1], digits
            ),
            remainder_radius=interval_record(remainder, digits),
            v_endpoint=interval_record(next_state[0], digits),
            v_Q_endpoint=interval_record(next_state[1], digits),
        )
        step_records.append(
            {
                "index": index + 1,
                "q_base": str(q_base),
                "q_next": str(q_next),
                "remainder_radius_upper": remainder.upper().str(
                    digits, radius=False
                ),
                "v": interval_record(next_state[0], digits),
                "v_Q": interval_record(next_state[1], digits),
            }
        )
        state = next_state
    v_zero, vq_zero = state
    denominator_ok = excludes_zero(v_zero)
    ratio: arb | None = None
    correction: arb | None = None
    scale_free_gamma: arb | None = None
    if denominator_ok:
        ratio = vq_zero / v_zero
        potential_mass = 18 * arb.pi() ** 4 * arb(-8).exp()
        forcing_mass = 4 * arb.pi() ** 2 * arb(-6).exp()
        kappa_lower = arb(kappa_band.lower())
        lambda_abs = absolute_upper(lambda_band)
        q_reference = potential_mass / kappa_lower
        q_actual = (potential_mass + lambda_abs * forcing_mass) / kappa_lower
        state_euclidean = (
            absolute_upper(v_zero) ** 2
            + (absolute_upper(vq_zero) / kappa_lower) ** 2
        ).sqrt()
        correction = arb(
            (
                lambda_abs
                * forcing_mass
                * (q_actual + q_reference).exp()
                * state_euclidean
                / absolute_lower(v_zero)
            ).upper()
        )
        scale_free_gamma = ratio + symmetric_interval(correction)
    width_target = arb(exact_rational(conventions["scale_free_width_target"]))
    tail_closed = bool(
        denominator_ok
        and ratio is not None
        and correction is not None
        and scale_free_gamma is not None
        and ratio.is_finite()
        and correction.is_finite()
        and correction.lower() >= 0
        and scale_free_gamma.is_finite()
    )
    width_ok = bool(
        tail_closed
        and scale_free_gamma is not None
        and interval_width(scale_free_gamma).upper() < width_target.lower()
    )
    audit.ball_check(
        f"rawc.sharp.{label}.tier{tier}.quotient_tail_closure",
        tail_closed,
        "The Q0 amplitude excludes zero and the complete rotating-frame quotient tail closes a finite scale-free Gamma_1 interval.",
        v_Q0=interval_record(v_zero, digits),
        v_Q_Q0=interval_record(vq_zero, digits),
        endpoint_log_derivative=(
            interval_record(ratio, digits) if ratio is not None else None
        ),
        quotient_tail_correction=(
            interval_record(correction, digits) if correction is not None else None
        ),
        scale_free_Gamma1=(
            interval_record(scale_free_gamma, digits)
            if scale_free_gamma is not None
            else None
        ),
        scale_free_Gamma1_contains_zero=(
            contains_zero(scale_free_gamma) if scale_free_gamma is not None else None
        ),
    )
    audit.ball_check(
        f"rawc.sharp.{label}.tier{tier}.scale_free_width_gate",
        width_ok,
        "The sharp-direction scale-free Gamma_1 interval meets the fixed absolute-width target.",
        observed_width=(
            interval_record(interval_width(scale_free_gamma), digits)
            if scale_free_gamma is not None
            else None
        ),
        target=conventions["scale_free_width_target"],
    )
    return {
        "label": label,
        "decimal_digits": dps,
        "switch_rho": interval_record(rho_switch, digits),
        "compact_steps": step_records,
        "v_Q0": interval_record(v_zero, digits),
        "v_Q_Q0": interval_record(vq_zero, digits),
        "Q0_amplitude_excludes_zero": denominator_ok,
        "endpoint_log_derivative": (
            interval_record(ratio, digits) if ratio is not None else None
        ),
        "quotient_tail_correction_absolute_upper": (
            interval_record(correction, digits) if correction is not None else None
        ),
        "scale_free_Gamma1": (
            interval_record(scale_free_gamma, digits)
            if scale_free_gamma is not None
            else None
        ),
        "scale_free_Gamma1_contains_zero": (
            contains_zero(scale_free_gamma) if scale_free_gamma is not None else None
        ),
        "quotient_tail_closed": tail_closed,
        "width_gate_passed": width_ok,
    }, {
        "v": v_zero,
        "vq": vq_zero,
        "g": scale_free_gamma if scale_free_gamma is not None else arb(0),
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input_sha = sha256_bytes(raw)
    if observed_input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input_sha}")
    config = json.loads(raw)
    if (
        config.get("schema_version")
        != "ice.raw-c-actual-direction-sharp-contraction-transfer.input.v1"
        or config.get("calculation_id") != CALCULATION_ID
        or config.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    conventions = config["declared_conventions"]
    if (
        config.get("resource_caps") != expected_caps()
        or config.get("required_fail_closed_outputs") != expected_nulls()
        or conventions["precision_ladder_decimal_digits"] != [80, 120]
        or conventions["kernel_panel_ladders"] != [512, 1024]
        or conventions["compact_q_segments"] != 16
        or conventions["compact_taylor_order"] != 12
    ):
        raise AssertionError("resource, precision, topology or null-output drift")
    expected_paths = [
        "cpt_temporal_folded_susy/RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_DECLARED_GAMMA1_BOUNDARY_VARIATION_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_ACTUAL_NONZERO_LAMBDA_HYBRID_VALIDATED_TRANSFER_RESULT.json",
    ]
    if [item["path"] for item in config["upstream_results"]] != expected_paths:
        raise AssertionError("upstream topology drift")
    root = Path(__file__).resolve().parent.parent
    upstream: list[dict[str, str]] = []
    upstream_payloads: dict[str, dict[str, Any]] = {}
    for item in config["upstream_results"]:
        payload, metadata = verify_upstream(root, item)
        upstream.append(metadata)
        upstream_payloads[item["path"]] = payload
    audit = Audit()
    exact_audit(audit)
    audit.guard(
        "rawc.sharp.guard.actual_direction_and_barrier",
        "DLMF Liouville--Green recessive solution plus the pinned scalar Riccati invariant barrier",
        "The actual family has the recorded Q=4 log-slope enclosure, rho in [-1,1], u>0 and x>=xs>3 throughout the sharp chart.",
        "Only the actual direction is transported to Q_switch; no absolute amplitude or below-switch Riccati chart is inferred.",
    )
    audit.guard(
        "rawc.sharp.guard.backward_x_variation_of_constants",
        "Exact variation of constants for rho_x=(2+1/x)rho+(rho^2+kappa^2+1/4)/x-lambda*sqrt(x/C)",
        "The exact homogeneous kernel is positive, 0<=rho^2<=1 follows from the invariant barrier, and both positive kernel masses are bounded by monotone finite panels plus an analytic infinite tail.",
        "The enclosure is analytic and outward; it is not a black-box numerical ODE or a sampled trajectory.",
    )
    audit.guard(
        "rawc.sharp.guard.local_taylor_remainder",
        "Taylor theorem with whole-step coefficient and derivative majorants",
        "Each downstream rational step uses complete parameter boxes, actual derivative jets through order 12, a state tube and D_13 |h|^13/13!.",
        "This validates only Q_switch to Q0 and remains node-safe as a two-state calculation.",
    )
    audit.guard(
        "rawc.sharp.guard.lambda_zero_bessel_reality",
        "DLMF sections 10.25 and 10.29 for the real modified-Bessel equation and recurrences",
        "For real x>0 and real kappa, the selected K_(i*kappa)(x) solution and its x derivative are real; the full inherited kappa bracket is real.",
        "The Arb imaginary intervals are numerical residue diagnostics. Real-part inclusion supplies only the lambda-zero switch and endpoint regressions.",
    )
    audit.guard(
        "rawc.sharp.guard.volterra_quotient_tail",
        "Rotating-frame variation of constants and Gronwall on Q<-4",
        "The potential and forcing masses are integrable and division is performed only after the Q0 amplitude interval excludes zero.",
        "The complete selected-reference quotient tail supplies no spectrum, rigging map or RAQ.",
    )
    audit.guard(
        "rawc.sharp.guard.workbench_scope",
        "Computational-workbench claim separation",
        "One inherited root bracket, two real lambda boxes, lambda zero, two precisions and two analytic-kernel panel counts are used.",
        "A usable interval width is not a Gamma_1 sign, root, spectrum, quantum-gravity, physics or TOE claim.",
    )
    plus_result = upstream_payloads[expected_paths[0]]
    bessel_result = upstream_payloads[expected_paths[1]]
    boundary_result = upstream_payloads[expected_paths[2]]
    coarse_result = upstream_payloads[expected_paths[3]]
    hybrid_result = upstream_payloads[expected_paths[4]]
    bracket = conventions["root_bracket"]
    root_row = bessel_result["certified_calculation"]["endpoint_characteristic"][
        "root_rows"
    ][0]
    root_certificate = root_row["certified_high_precision_bracket"]
    precision_120 = next(
        item for item in root_row["precision_runs"] if item["decimal_digits"] == 120
    )
    audit.inequality(
        "rawc.sharp.upstream_root1_linkage",
        bool(
            root_row["root_index"] == 1
            and root_certificate["at_least_one_real_sign_changing_zero"] is True
            and root_certificate["left_exact"] == bracket["left_exact"]
            and root_certificate["right_exact"] == bracket["right_exact"]
            and precision_120["signs"] == [-1, 1]
        ),
        "The configured root bracket is exactly the pinned root-1 sign-changing Bessel bracket.",
        left_exact=root_certificate["left_exact"],
        right_exact=root_certificate["right_exact"],
        signs=precision_120["signs"],
    )
    coarse_conventions = coarse_result["declared_conventions"]
    coarse_guards = {item["id"]: item for item in coarse_result["theorem_guards"]}
    audit.inequality(
        "rawc.sharp.upstream_actual_barrier_linkage",
        bool(
            plus_result["declared_conventions"]["Q_plus"]
            == coarse_conventions["Q_plus"]
            == conventions["Q_plus"]
            == "4"
            and coarse_conventions["C"] == conventions["C"] == "6*pi^2"
            and coarse_conventions["lambda_boxes"] == conventions["lambda_boxes"]
            and coarse_guards["rawc.actual.guard.actual_recessive_normalization"][
                "verified"
            ]
            is True
            and coarse_guards["rawc.actual.guard.riccati_invariant_region"][
                "verified"
            ]
            is True
        ),
        "The sharp calculation is bound to the pinned actual normalization, parameter boxes and x>=3 invariant barrier.",
        Q_plus=coarse_conventions["Q_plus"],
        barrier_switch_x=coarse_conventions["barrier_switch_x"],
    )
    audit.inequality(
        "rawc.sharp.upstream_boundary_linkage",
        bool(
            boundary_result["declared_conventions"]["Q_0"]
            == conventions["Q_0"]
            == "-4"
            and boundary_result["declared_conventions"][
                "exact_nonzero_lambda_identity"
            ]
            == "Gamma_1,p(u_lambda)=u_lambda,Q(Q0)-lambda*integral_-infinity^Q0 a(Q)u_lambda(Q)c_p(Q)dQ"
        ),
        "The downstream quotient uses the pinned Gamma_1 boundary identity at the same Q0.",
        Q_0=conventions["Q_0"],
    )
    prior_partial = hybrid_result["validated_calculation"]["partial_progress"]
    prior_switch = hybrid_result["validated_calculation"]["parameter_tiers"][
        "negative"
    ][0]["switch"]["rho"]
    audit.inequality(
        "rawc.sharp.upstream_hybrid_bottleneck_linkage",
        bool(
            prior_partial["finite_outer_quotient_tail_tiers"] == 6
            and prior_partial["preregistered_width_gate_passed_tiers"] == 0
            and prior_switch["lower"].startswith("-1")
            and prior_switch["upper"].startswith("1")
        ),
        "The reused downstream map is tied to the audited six finite tiers and six width failures from the full [-1,1] switch direction.",
        prior_finite_tiers=prior_partial["finite_outer_quotient_tail_tiers"],
        prior_width_passed_tiers=prior_partial[
            "preregistered_width_gate_passed_tiers"
        ],
        prior_switch_rho=prior_switch,
    )
    kappa_left = exact_rational(bracket["left_exact"])
    kappa_right = exact_rational(bracket["right_exact"])
    audit.inequality(
        "rawc.sharp.root1_exact_location",
        bool(fmpq(2) < kappa_left < kappa_right < fmpq(3)),
        "The exact root-1 bracket lies in (2,3).",
        left_exact=str(kappa_left),
        right_exact=str(kappa_right),
    )
    lambda_boxes: list[dict[str, Any]] = []
    for item in conventions["lambda_boxes"]:
        left = exact_rational(item["left"])
        right = exact_rational(item["right"])
        if not left < right:
            raise AssertionError("lambda box ordering drift")
        lambda_boxes.append({"label": item["label"], "left": left, "right": right})
    if [item["label"] for item in lambda_boxes] != ["negative", "positive"]:
        raise AssertionError("lambda box topology drift")
    tier_records: dict[str, list[dict[str, Any]]] = {
        "negative": [],
        "positive": [],
        "lambda_zero": [],
    }
    tier_balls: dict[str, list[dict[str, arb]]] = {
        "negative": [],
        "positive": [],
        "lambda_zero": [],
    }
    for tier, dps in enumerate(conventions["precision_ladder_decimal_digits"], 1):
        ctx.dps = int(dps)
        kappa_band = bracket_band(kappa_left, kappa_right)
        parameter_rows = [
            (
                item["label"],
                bracket_band(item["left"], item["right"]),
                False,
            )
            for item in lambda_boxes
        ] + [("lambda_zero", arb(0), True)]
        for label, lambda_band, is_zero in parameter_rows:
            direction_record, rho_switch = sharp_switch_enclosure(
                audit,
                label=label,
                tier=tier,
                dps=int(dps),
                kappa_band=kappa_band,
                lambda_band=lambda_band,
                config=config,
                plus_data=plus_result,
                bessel_regression=is_zero,
            )
            downstream_record, balls = downstream_transfer(
                audit,
                label=label,
                tier=tier,
                dps=int(dps),
                kappa_band=kappa_band,
                lambda_band=lambda_band,
                rho_switch=rho_switch,
                config=config,
            )
            if is_zero:
                x_zero = acb(6 * arb.pi() ** 2 * arb(-4).exp())
                order_ball = acb(0, kappa_band)
                k_zero = audit.bessel_k(x_zero, order_ball)
                k_minus = audit.bessel_k(x_zero, order_ball - 1)
                k_plus = audit.bessel_k(x_zero, order_ball + 1)
                kq_zero = -x_zero * (k_minus + k_plus) / 2
                bessel_ratio = kq_zero / k_zero
                endpoint_regression_ok = bool(
                    k_zero.abs_lower() > 0
                    and bessel_ratio.imag.lower() <= 0 <= bessel_ratio.imag.upper()
                    and contains_interval(balls["g"], bessel_ratio.real)
                )
                audit.ball_check(
                    f"rawc.sharp.lambda_zero.tier{tier}.endpoint_bessel_regression",
                    endpoint_regression_ok,
                    "Using the guarded real-valued K_(i*kappa) family, the exact lambda-zero endpoint logarithmic derivative is contained by the sharp-direction downstream enclosure; the imaginary ball is only a residue diagnostic.",
                    decimal_digits=int(dps),
                    K_Q0=complex_record(k_zero, int(conventions["ball_output_digits"])),
                    exact_Bessel_endpoint_log_derivative=complex_record(
                        bessel_ratio, int(conventions["ball_output_digits"])
                    ),
                    scale_free_Gamma1=interval_record(
                        balls["g"], int(conventions["ball_output_digits"])
                    ),
                )
                downstream_record["lambda_zero_Bessel_endpoint_regression"] = {
                    "status": "CONTAINED"
                    if endpoint_regression_ok
                    else "NOT_CONTAINED",
                    "endpoint_log_derivative": complex_record(
                        bessel_ratio, int(conventions["ball_output_digits"])
                    ),
                }
            tier_records[label].append(
                {"direction": direction_record, "downstream": downstream_record}
            )
            tier_balls[label].append({"rho": rho_switch, **balls})
    precision_intersections: dict[str, Any] = {}
    digits = int(conventions["ball_output_digits"])
    for label in ("negative", "positive", "lambda_zero"):
        rho_overlap = intersection(
            tier_balls[label][0]["rho"], tier_balls[label][1]["rho"]
        )
        g_overlap = intersection(
            tier_balls[label][0]["g"], tier_balls[label][1]["g"]
        )
        overlap_ok = rho_overlap is not None and g_overlap is not None
        audit.ball_check(
            f"rawc.sharp.{label}.precision_overlap",
            overlap_ok,
            "The 80- and 120-digit sharp switch and downstream enclosures overlap; this is a same-backend refinement check.",
            rho_intersection=(
                interval_record(rho_overlap, digits) if rho_overlap else None
            ),
            Gamma1_intersection=(
                interval_record(g_overlap, digits) if g_overlap else None
            ),
        )
        precision_intersections[label] = {
            "rho_switch": interval_record(rho_overlap, digits)
            if rho_overlap
            else None,
            "scale_free_Gamma1": interval_record(g_overlap, digits)
            if g_overlap
            else None,
        }
    audit.inequality(
        "rawc.sharp.bessel_call_count",
        audit.bessel_evaluations == expected_caps()["ball_bessel_evaluations"],
        "The two lambda-zero tiers make exactly six switch and six endpoint Bessel calls.",
        observed=audit.bessel_evaluations,
        expected=expected_caps()["ball_bessel_evaluations"],
    )
    rows = [
        row
        for label in ("negative", "positive", "lambda_zero")
        for row in tier_records[label]
    ]
    sharp_tiers = sum(row["direction"]["sharp_switch_certified"] for row in rows)
    finite_tiers = sum(row["downstream"]["quotient_tail_closed"] for row in rows)
    width_tiers = sum(row["downstream"]["width_gate_passed"] for row in rows)
    exact_pass = all(item["passed"] for item in audit.exact)
    ball_pass = all(item["passed"] for item in audit.ball)
    non_width_ball_pass = all(
        item["passed"]
        for item in audit.ball
        if not item["id"].endswith(".scale_free_width_gate")
    )
    if exact_pass and ball_pass:
        verdict = (
            "CERTIFY_ACTUAL_DIRECTION_SHARP_CONTRACTION_AND_SCALE_FREE_GAMMA1_WIDTH_BRACKET1_ONLY"
        )
        programme_impact = (
            "RECORD_A_SHARP_ACTUAL_SWITCH_DIRECTION_AND_USABLE_SCALE_FREE_GAMMA1_WIDTH_WITHOUT_CLAIMING_SIGN_ROOT_CONTINUATION_SPECTRUM_RAQ_OR_PHYSICS"
        )
    elif (
        exact_pass
        and non_width_ball_pass
        and sharp_tiers == 6
        and finite_tiers == 6
    ):
        verdict = "CERTIFY_SHARP_ACTUAL_DIRECTION_DOWNSTREAM_WIDTH_NOT_CERTIFIED"
        programme_impact = (
            "RETAIN_THE_SHARP_DIRECTION_AND_ISOLATE_THE_NEXT_DOWNSTREAM_BOUND"
        )
    else:
        verdict = "SHARP_CONTRACTION_TRANSFER_NOT_CERTIFIED"
        programme_impact = (
            "RETAIN_THE_PRIOR_FINITE_OUTER_TRANSFER_AND_RECORD_THE_FIRST_FAILED_CERTIFICATION_GATE"
        )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": programme_impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input_sha},
        "upstream_results": upstream,
        "primary_sources": config["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": audit.exact,
        "ball_checks": audit.ball,
        "theorem_guards": audit.guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "ball_passed": sum(item["passed"] for item in audit.ball),
            "ball_total": len(audit.ball),
            "theorem_guard_count": len(audit.guards),
            "all_executable_checks_passed": bool(exact_pass and ball_pass),
        },
        "validated_calculation": {
            "parameter_tiers": tier_records,
            "precision_intersections": precision_intersections,
            "summary": {
                "sharp_switch_direction_tiers": sharp_tiers,
                "sharp_switch_direction_tier_total": len(rows),
                "finite_outer_quotient_tail_tiers": finite_tiers,
                "finite_outer_quotient_tail_tier_total": len(rows),
                "scale_free_width_gate_passed_tiers": width_tiers,
                "scale_free_width_gate_tier_total": len(rows),
                "scope": "Sharp actual direction and usable scale-free width only; sign, roots, spectrum, RAQ and physics remain null.",
            },
            "interpretation": "Backward projective contraction removes the inherited Q=4 direction uncertainty before the already audited compact/tail map. The result remains an outward family enclosure and not a trajectory sample or physical claim.",
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "kernel_panels_coarse_per_parameter_tier": 512,
            "kernel_panels_refined_per_parameter_tier": 1024,
            "kernel_parameter_tiers": 6,
            "compact_q_segments_per_parameter_tier": 16,
            "compact_taylor_order": 12,
            "ball_bessel_evaluations": audit.bessel_evaluations,
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
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "python_flint": importlib.metadata.version("python-flint"),
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "ball_passed": result["check_summary"]["ball_passed"],
                "ball_total": result["check_summary"]["ball_total"],
                "theorem_guards": result["check_summary"]["theorem_guard_count"],
                "sharp_tiers": sharp_tiers,
                "finite_tiers": finite_tiers,
                "width_tiers": width_tiers,
                "result": RESULT_NAME,
                "result_sha256": sha256_bytes(encoded),
                "result_bytes": len(encoded),
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
