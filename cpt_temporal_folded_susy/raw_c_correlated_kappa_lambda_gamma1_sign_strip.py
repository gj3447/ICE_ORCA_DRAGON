#!/usr/bin/env python3
"""Uniform real kappa-lambda sign strip for the selected raw-C boundary map.

The calculation rebuilds the actual plus-family projective chart on one
expanded kappa corridor and one closed lambda slab.  It then evaluates the
complete Q0-normalized declared Gamma_1 functional only on the two kappa
faces.  A uniformly nonzero Q0 chart, joint continuity, and strict opposite
face signs imply at least one interior zero for every lambda by the
intermediate value theorem.  No root selector, uniqueness, velocity,
nonreal Weyl datum, spectral measure, RAQ object, or physics claim is made.
"""
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

import raw_c_actual_nonzero_lambda_hybrid_validated_transfer as hybrid
import raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport as affine


INPUT_NAME = "RAW_C_CORRELATED_KAPPA_LAMBDA_GAMMA1_SIGN_STRIP_INPUTS.json"
RESULT_NAME = "RAW_C_CORRELATED_KAPPA_LAMBDA_GAMMA1_SIGN_STRIP_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_correlated_kappa_lambda_gamma1_sign_strip.py"
)
EXPECTED_INPUT_SHA256 = "114c8e65013ce8c6a63b836cb2628088330ec6ec86f0e84e0eaa101efbb31452"
CALCULATION_ID = "RawCCorrelatedKappaLambdaGamma1SignStrip"
RESULT_SCHEMA = "ice.raw-c-correlated-kappa-lambda-gamma1-sign-strip.result.v1"
RESULT_PREFIX = "RAW_C_CORRELATED_KAPPA_LAMBDA_GAMMA1_SIGN_STRIP_RESULT="
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


def exact_rational(text: str) -> fmpq:
    return hybrid.exact_rational(text)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return hybrid.interval_record(value, digits)


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    return hybrid.interval_from_bounds(lower, upper)


def bracket_band(left: fmpq, right: fmpq) -> arb:
    return hybrid.bracket_band(left, right)


def intersection(left: arb, right: arb) -> arb | None:
    return hybrid.intersection(left, right)


def absolute_upper(value: arb) -> arb:
    return hybrid.absolute_upper(value)


def maximum(left: arb, right: arb) -> arb:
    return hybrid.maximum(left, right)


def symmetric(radius: arb) -> arb:
    return hybrid.symmetric_interval(radius)


def excludes_zero(value: arb) -> bool:
    return hybrid.excludes_zero(value)


def contains_interval(outer: arb, inner: arb) -> bool:
    return hybrid.contains_interval(outer, inner)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_checks": 32,
        "kernel_panels_evaluated": 3072,
        "compact_steps": 608,
        "compact_taylor_order": 12,
        "q0_segment_rows": 12,
        "cutoff_segment_rows": 12,
        "ball_bessel_evaluations": 24,
        "precision_tiers": 2,
        "lambda_slabs": 1,
        "kappa_faces": 2,
        "root_brackets": 1,
        "ode_calls": 0,
        "root_calls": 0,
        "quadrature_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "bisection_steps": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "root_uniqueness_in_corridor": None,
        "continuous_root_selector_or_nonzero_lambda_continuation": None,
        "root_velocity_or_kappa_derivative": None,
        "global_or_complete_root_census": None,
        "roots_outside_declared_corridor": None,
        "absolute_actual_Gamma1_amplitude": None,
        "actual_Gamma1_sign_away_from_two_certified_faces_or_roots": None,
        "Q0_lambda_side_separation": None,
        "nonreal_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_RAQ_completion": None,
        "physics_claim": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    bessel_evaluations: int = 0

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate audit id: {identifier}")
        self.seen.add(identifier)

    def identity(self, identifier: str, residual: sp.Expr, statement: str) -> None:
        self.register(identifier)
        reduced = sp.simplify(residual)
        passed = (
            all(sp.simplify(item) == 0 for item in reduced)
            if isinstance(reduced, sp.MatrixBase)
            else bool(reduced == 0)
        )
        self.exact.append(
            {
                "id": identifier,
                "passed": passed,
                "statement": statement,
                "residual": str(reduced),
            }
        )

    def inequality(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.exact.append(
            {
                "id": identifier,
                "passed": bool(passed),
                "statement": statement,
                **data,
            }
        )

    def control(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.controls.append(
            {
                "id": identifier,
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
                "verified": True,
                "theorem": theorem,
                "hypotheses": hypotheses,
                "scope": scope,
            }
        )

    def bessel_k(self, z: acb, order: acb) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")
        return z.bessel_k(order)


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    result = json.loads(raw)
    expected = {
        "schema_version": item["schema_version"],
        "verdict": item["required_verdict"],
        "result_payload_sha256_without_self": item[
            "payload_sha256_without_self"
        ],
    }
    if any(result.get(key) != value for key, value in expected.items()):
        raise AssertionError(f"upstream metadata mismatch: {item['path']}")
    payload = dict(result)
    recorded = payload.pop("result_payload_sha256_without_self")
    if (
        sha256_bytes(canonical_bytes(payload)) != recorded
        or result.get("run_status") != "VALID_RUN"
        or result.get("numbered_phase") is not None
    ):
        raise AssertionError(f"upstream integrity mismatch: {item['path']}")
    return result, {
        "path": item["path"],
        "sha256": observed,
        "schema_version": item["schema_version"],
        "verdict": item["required_verdict"],
        "payload_sha256_without_self": item["payload_sha256_without_self"],
        "role": item["role"],
    }


def verify_method_sources(root: Path, rows: list[dict[str, str]]) -> None:
    expected_paths = [
        "cpt_temporal_folded_susy/raw_c_actual_nonzero_lambda_hybrid_validated_transfer.py",
        "cpt_temporal_folded_susy/raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport.py",
        "cpt_temporal_folded_susy/raw_c_q0_normalized_differentiated_rotating_tail_gamma1.py",
    ]
    if [row["path"] for row in rows] != expected_paths:
        raise AssertionError("method source topology drift")
    for row in rows:
        if sha256_bytes((root / row["path"]).read_bytes()) != row["sha256"]:
            raise AssertionError(f"method source hash mismatch: {row['path']}")
    imported = {
        Path(hybrid.__file__).resolve(),
        Path(affine.__file__).resolve(),
    }
    expected_imported = {
        (root / rows[0]["path"]).resolve(),
        (root / rows[1]["path"]).resolve(),
    }
    if imported != expected_imported:
        raise AssertionError("reused helper import path drift")


def exact_audit(audit: Audit) -> None:
    q = sp.symbols("Q", real=True)
    lam, kappa = sp.symbols("lambda kappa", real=True)
    x, c_value = sp.symbols("x C", positive=True, real=True)
    rho, rho0, p = sp.symbols("rho rho_0 p", real=True)
    field = lambda value, parameter: (
        2 * value
        + (value + value**2 + kappa**2 + sp.Rational(1, 4)) / x
        - parameter * sp.sqrt(x / c_value)
    )
    difference = sp.expand(field(rho, lam) - field(rho0, 0))
    audit.identity(
        "rawc.signstrip.affine_difference",
        difference
        - (2 + (1 + rho + rho0) / x) * (rho - rho0)
        + lam * sp.sqrt(x / c_value),
        "Subtracting the lambda-zero Riccati equation gives the affine difference equation used by the corridor comparison.",
    )
    audit.identity(
        "rawc.signstrip.affine_mean_sensitivity",
        sp.expand(
            difference.subs(rho, rho0 + lam * p) / lam
            - (
                (2 + (1 + rho0 + lam * p + rho0) / x) * p
                - sp.sqrt(x / c_value)
            )
        ),
        "The closed-segment mean sensitivity p=(rho_lambda-rho_0)/lambda obeys the displayed comparison equation away from zero and extends there by differentiability.",
    )
    u, uq, v, vq = sp.symbols("u u_Q v v_Q", nonzero=True, real=True)
    a_coefficient = 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q)
    base = 36 * sp.pi**4 * sp.exp(2 * q) - kappa**2
    actual = base + lam * a_coefficient
    g_log = -uq / u
    sensitivity = (uq * v - u * vq) / u**2

    def dq(expr: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expr, u) * uq
            + sp.diff(expr, uq) * actual * u
            + sp.diff(expr, v) * vq
            + sp.diff(expr, vq) * (actual * v + a_coefficient * u)
        )

    audit.identity(
        "rawc.signstrip.forced_wronskian_sensitivity",
        dq(u**2 * sensitivity) + a_coefficient * u**2,
        "The plus-end logarithmic sensitivity has the scale-invariant forced-Wronskian integral used for its Q=4 enclosure.",
    )
    audit.identity(
        "rawc.signstrip.riccati_sensitivity",
        dq(sensitivity) - (2 * g_log * sensitivity - a_coefficient),
        "The actual logarithmic sensitivity equation is exact.",
    )
    U, Uq, c, cq, a0 = sp.symbols("U U_Q c c_Q A_0", real=True)
    audit.identity(
        "rawc.signstrip.wronskian_derivative",
        Uq * cq
        + U * a0 * c
        - (a0 + lam * sp.Symbol("a", real=True)) * U * c
        - Uq * cq
        + lam * sp.Symbol("a", real=True) * U * c,
        "For the lambda-independent reference, W(U,c)_Q=-lambda*a*U*c.",
    )
    scale, gamma = sp.symbols("scale Gamma", nonzero=True, real=True)
    audit.identity(
        "rawc.signstrip.normalized_zero_equivalence",
        scale * (gamma / scale) - gamma,
        "Division by a certified nonzero Q0 amplitude preserves exactly the zeros of the declared boundary functional.",
    )
    audit.identity(
        "rawc.signstrip.a_tail_antiderivative",
        sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q)
        - a_coefficient,
        "The forcing tail has exact mass 4*pi^2*exp(3Q/2).",
    )
    audit.identity(
        "rawc.signstrip.v_tail_antiderivative",
        sp.diff(18 * sp.pi**4 * sp.exp(2 * q), q)
        - 36 * sp.pi**4 * sp.exp(2 * q),
        "The reference-potential tail has exact mass 18*pi^4*exp(2Q).",
    )
    k_positive, perturbation = sp.symbols(
        "k_positive perturbation", positive=True, real=True
    )
    rotating_energy = U**2 + Uq**2 / k_positive**2
    rotating_energy_q = (
        sp.diff(rotating_energy, U) * Uq
        + sp.diff(rotating_energy, Uq)
        * (-k_positive**2 + perturbation)
        * U
    )
    audit.identity(
        "rawc.signstrip.rotating_energy_identity",
        rotating_energy_q
        - 2 * perturbation * U * Uq / k_positive**2,
        "For y''=(-kappa^2+B)y, the rotating energy derivative is 2B*y*y_Q/kappa^2; 2|y*y_Q|/kappa<=R^2 gives R_Q<=|B|R/kappa and the implemented exponential tail factors.",
    )
    audit.identity(
        "rawc.signstrip.switch_partition_16",
        16 * sp.Rational(-11, 160)
        - (sp.Rational(-4) - sp.Rational(-29, 10)),
        "The 16-step switch-to-Q0 partition is exact.",
    )
    audit.identity(
        "rawc.signstrip.switch_partition_32",
        32 * sp.Rational(-11, 320)
        - (sp.Rational(-4) - sp.Rational(-29, 10)),
        "The 32-step switch-to-Q0 partition is exact.",
    )
    audit.identity(
        "rawc.signstrip.cutoff_partitions",
        sp.Matrix(
            [
                16 * sp.Rational(-1, 16) - (sp.Rational(-5) + 4),
                32 * sp.Rational(-1, 32) - (sp.Rational(-5) + 4),
                32 * sp.Rational(-1, 16) - (sp.Rational(-6) + 4),
            ]
        ),
        "All three Q0-to-cutoff partitions are exact.",
    )
    closed_cap_ratio = (
        sp.Rational(1, 10000) / (6 * 9 * 7)
        + sp.Rational(64, 36 * 81 * 7**4)
    )
    audit.inequality(
        "rawc.signstrip.lg_closed_box_budget",
        bool(closed_cap_ratio < sp.Rational(1, 100000)),
        "The full abs(lambda)<=1e-4 and kappa<=8 perturbation remains below the pinned Liouville-Green relative coefficient budget for Q>=4.",
        rational_upper=str(closed_cap_ratio),
        budget="1/100000",
    )
    lower, upper = sp.Rational(27, 10), sp.Rational(240, 53)
    b = sp.Rational(1, 500)
    audit.inequality(
        "rawc.signstrip.plus_anchor.elementary_bounds",
        bool(
            sp.E**2 > 7
            and sp.E**2 < sp.Rational(15, 2)
            and sp.pi**2 > 9
            and sp.pi**2 < 10
        ),
        "The elementary pi and exponential inequalities used in the outward plus-tail sensitivity bounds hold.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.coefficient_positive",
        bool(1 - sp.Rational(1, 100000) > 0),
        "The pinned full-box relative perturbation gives A>=A0(1-1e-5)>0.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.coefficient_derivative_positive",
        bool(2 - sp.Rational(3, 200000) > 0),
        "The same full-box bound gives A'>0.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.four_A_minus_Aprime",
        bool(2 - sp.Rational(4, 100000) > 0),
        "The same full-box bound gives 4A-A'>0, hence 0<A'/(4A)<1.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.g_lower_from_lg",
        bool(
            (1 - b)
            * 6
            * 9
            * sp.Rational(99999, 100000)
            > 53
        ),
        "A pinned sqrt(A)-normalized logarithmic-direction error below b=1/500 implies g>=53 exp(Q) throughout the widened corridor once the executable LG pin is checked.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.g_upper_from_lg",
        bool(
            (1 + b)
            * 6
            * 10
            * sp.Rational(101, 100)
            + sp.Rational(1, 54)
            < 70
        ),
        "The coefficient inequalities and the same pinned LG error imply g<=70 exp(Q) throughout the widened corridor.",
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.lower_integral",
        bool((6 * 9 * 7) / (2 * 70) >= lower),
        "The forced-Wronskian integral and g<=70 exp(Q) give the rational lower sensitivity bound 27/10.",
        lower=str(lower),
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.upper_integral",
        bool(
            60
            * (
                sp.Rational(15, 2) / (2 * 53)
                + sp.Rational(1, 14 * (2 * 53) ** 2)
            )
            < upper
        ),
        "The forced-Wronskian integral and g>=53 exp(Q) give the rational upper sensitivity bound 240/53.",
        upper=str(upper),
    )
    audit.inequality(
        "rawc.signstrip.plus_anchor.interval_order",
        bool(0 < lower < upper),
        "The rederived expanded-corridor Q=4 sensitivity interval is nonempty and strictly positive.",
        lower=str(lower),
        upper=str(upper),
    )


def all_intersection(values: list[arb | None]) -> arb | None:
    if not values or values[0] is None:
        return None
    result = values[0]
    for value in values[1:]:
        if result is None or value is None:
            return None
        result = intersection(result, value)
    return result


def apply_coefficient_derivative(
    derivative: int,
    coefficient_values: list[arb],
    state: tuple[arb, arb],
) -> tuple[arb, arb]:
    if derivative == 0:
        return state[1], coefficient_values[0] * state[0]
    return arb(0), coefficient_values[derivative] * state[0]


def propagate_q0(
    audit: Audit,
    *,
    label: str,
    tier: int,
    dps: int,
    segments: int,
    kappa: arb,
    lam: arb,
    rho_switch: arb,
    conventions: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, arb | None]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    q_switch = exact_rational(conventions["Q_switch"])
    q0 = exact_rational(conventions["Q_0"])
    step = (q0 - q_switch) / segments
    c_value = 6 * arb.pi() ** 2
    x_switch = c_value * arb(q_switch).exp()
    state = (arb(1), -(x_switch + arb(1) / 2 + rho_switch))
    step_abs = arb(-step)
    max_remainder = arb(0)
    steps_ok = True
    for index in range(segments):
        q_base = q_switch + index * step
        _, coefficient_values = hybrid.coefficient_derivatives(
            q_base, kappa, lam, order
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
            factor = arb(step) ** n / math.factorial(n)
            polynomial[0] += derivative_state[0] * factor
            polynomial[1] += derivative_state[1] * factor
        majorants = hybrid.whole_step_majorants(
            q_base, kappa, lam, order
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
        state = (
            polynomial[0] + symmetric(remainder),
            polynomial[1] + symmetric(remainder),
        )
        if remainder.upper() > max_remainder.upper():
            max_remainder = arb(remainder.upper())
        steps_ok = bool(
            steps_ok
            and remainder.is_finite()
            and remainder.lower() >= 0
            and state[0].is_finite()
            and state[1].is_finite()
        )
    v0, vq0 = state
    denominator_ok = excludes_zero(v0)
    rho0 = None
    if denominator_ok:
        x0 = c_value * arb(q0).exp()
        rho0 = -vq0 / v0 - x0 - arb(1) / 2
    certified = bool(
        steps_ok
        and denominator_ok
        and rho0 is not None
        and rho0.is_finite()
    )
    audit.control(
        f"rawc.signstrip.q0.{label}.tier{tier}.segments{segments}",
        certified,
        "The order-12 switch-to-Q0 transfer has a whole-step D13 remainder on the full declared parameter box and its selected projective amplitude excludes zero.",
        decimal_digits=dps,
        segments=segments,
        rho_Qswitch=interval_record(rho_switch, digits),
        max_step_remainder_upper=max_remainder.upper().str(
            digits, radius=False
        ),
        v_Q0=interval_record(v0, digits),
        v_Q_Q0=interval_record(vq0, digits),
        rho_Q0=interval_record(rho0, digits) if rho0 is not None else None,
        Q0_amplitude_excludes_zero=denominator_ok,
    )
    return {
        "label": label,
        "decimal_digits": dps,
        "segments": segments,
        "rho_Qswitch": interval_record(rho_switch, digits),
        "max_step_remainder_upper": max_remainder.upper().str(
            digits, radius=False
        ),
        "v_Q0": interval_record(v0, digits),
        "v_Q_Q0": interval_record(vq0, digits),
        "rho_Q0": interval_record(rho0, digits) if rho0 is not None else None,
        "Q0_amplitude_excludes_zero": denominator_ok,
        "status": "CERTIFIED_Q0_CHART_ROW" if certified else "Q0_CHART_ROW_NOT_CERTIFIED",
    }, {"v": v0, "vq": vq0, "rho": rho0}


def matrix_derivative4(
    q_base: fmpq,
    kappa: arb,
    lam: arb,
    derivative: int,
    order: int,
) -> list[list[arb]]:
    _, actual_values = hybrid.coefficient_derivatives(
        q_base, kappa, lam, order
    )
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    reference_value = (
        x_value**2 - kappa**2
        if derivative == 0
        else arb(2) ** derivative * x_value**2
    )
    zero = arb(0)
    if derivative == 0:
        return [
            [zero, arb(1), zero, zero],
            [actual_values[0], zero, zero, zero],
            [zero, zero, zero, arb(1)],
            [zero, zero, reference_value, zero],
        ]
    return [
        [zero, zero, zero, zero],
        [actual_values[derivative], zero, zero, zero],
        [zero, zero, zero, zero],
        [zero, zero, reference_value, zero],
    ]


def matrix_apply4(matrix: list[list[arb]], state: list[arb]) -> list[arb]:
    return [
        sum((matrix[i][j] * state[j] for j in range(4)), arb(0))
        for i in range(4)
    ]


def matrix_majorants4(
    q_base: fmpq, kappa: arb, lam: arb, order: int
) -> list[arb]:
    inherited = hybrid.whole_step_majorants(q_base, kappa, lam, order)
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    kappa_abs = absolute_upper(kappa)
    rows: list[arb] = []
    for derivative in range(order + 1):
        reference = (
            x_value**2 + kappa_abs**2
            if derivative == 0
            else arb(2) ** derivative * x_value**2
        )
        upper = max(inherited[derivative].upper(), reference.upper())
        if derivative == 0:
            upper = max(upper, arb(1).upper())
        rows.append(arb(upper))
    return rows


def rotating_norm(u: arb, uq: arb, kappa_lower: arb) -> arb:
    return (
        absolute_upper(u) ** 2
        + (absolute_upper(uq) / kappa_lower) ** 2
    ).sqrt()


def propagate_face_tail(
    audit: Audit,
    *,
    label: str,
    tier: int,
    dps: int,
    cutoff: dict[str, Any],
    kappa: arb,
    lam: arb,
    rho_q0: arb,
    conventions: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = int(conventions["ball_output_digits"])
    order = int(conventions["compact_taylor_order"])
    q0 = exact_rational(conventions["Q_0"])
    q_cut = exact_rational(cutoff["Q_cut"])
    segments = int(cutoff["segments"])
    step = (q_cut - q0) / segments
    if step >= 0:
        raise AssertionError("left-tail step must be negative")
    c_value = 6 * arb.pi() ** 2
    x0 = c_value * arb(q0).exp()
    state = [
        arb(1),
        -x0 - arb(1) / 2 - rho_q0,
        arb(1),
        arb(0),
    ]
    step_abs = arb(-step)
    max_remainder = arb(0)
    steps_ok = True
    for index in range(segments):
        q_base = q0 + index * step
        matrices = [
            matrix_derivative4(q_base, kappa, lam, derivative, order)
            for derivative in range(order + 1)
        ]
        derivatives: list[list[arb]] = [state]
        for n in range(order):
            next_state = [arb(0) for _ in range(4)]
            for j in range(n + 1):
                applied = matrix_apply4(matrices[j], derivatives[n - j])
                for component in range(4):
                    next_state[component] += math.comb(n, j) * applied[component]
            derivatives.append(next_state)
        polynomial = [arb(0) for _ in range(4)]
        for n, derivative_state in enumerate(derivatives):
            factor = arb(step) ** n / math.factorial(n)
            for component in range(4):
                polynomial[component] += factor * derivative_state[component]
        majorants = matrix_majorants4(q_base, kappa, lam, order)
        state_norm = max(
            (absolute_upper(value) for value in state),
            key=lambda value: value.upper(),
        )
        tube_norm = arb((state_norm * (majorants[0] * step_abs).exp()).upper())
        derivative_bounds = [tube_norm]
        for n in range(order + 1):
            derivative_bounds.append(
                arb(
                    sum(
                        (
                            math.comb(n, j)
                            * majorants[j]
                            * derivative_bounds[n - j]
                            for j in range(n + 1)
                        ),
                        arb(0),
                    ).upper()
                )
            )
        remainder = arb(
            (
                derivative_bounds[order + 1]
                * step_abs ** (order + 1)
                / math.factorial(order + 1)
            ).upper()
        )
        state = [value + symmetric(remainder) for value in polynomial]
        if remainder.upper() > max_remainder.upper():
            max_remainder = arb(remainder.upper())
        steps_ok = bool(
            steps_ok
            and remainder.is_finite()
            and remainder.lower() >= 0
            and all(value.is_finite() for value in state)
        )
    u, uq, c, cq = state
    wronskian = u * cq - uq * c
    kappa_lower = arb(kappa.lower())
    lambda_abs = absolute_upper(lam)
    a_mass = 4 * arb.pi() ** 2 * (arb(q_cut) * arb(3) / 2).exp()
    v_mass = 18 * arb.pi() ** 4 * arb(2 * q_cut).exp()
    q_u = (v_mass + lambda_abs * a_mass) / kappa_lower
    q_c = v_mass / kappa_lower
    r_u = rotating_norm(u, uq, kappa_lower) * q_u.exp()
    r_c = rotating_norm(c, cq, kappa_lower) * q_c.exp()
    tail_radius = arb((lambda_abs * a_mass * r_u * r_c).upper())
    g_value = -wronskian + symmetric(tail_radius)
    certified = bool(
        steps_ok
        and kappa_lower.lower() > 0
        and all(
            value.is_finite() and value.lower() >= 0
            for value in (a_mass, v_mass, q_u, q_c, r_u, r_c, tail_radius)
        )
        and g_value.is_finite()
    )
    audit.control(
        f"rawc.signstrip.tail.{label}.tier{tier}.{cutoff['label']}",
        certified,
        "The four-state order-12 finite-cutoff Wronskian enclosure receives a finite analytic rotating-frame radius for the complete omitted tail.",
        decimal_digits=dps,
        cutoff=cutoff,
        rho_Q0=interval_record(rho_q0, digits),
        max_step_remainder_upper=max_remainder.upper().str(
            digits, radius=False
        ),
        W_U_c_at_cutoff=interval_record(wronskian, digits),
        tail_radius=interval_record(tail_radius, digits),
        complete_g=interval_record(g_value, digits),
    )
    return {
        "label": label,
        "decimal_digits": dps,
        "cutoff": cutoff,
        "max_step_remainder_upper": max_remainder.upper().str(
            digits, radius=False
        ),
        "W_U_c_at_cutoff": interval_record(wronskian, digits),
        "tail_radius_g": interval_record(tail_radius, digits),
        "g_Q0_normalized": interval_record(g_value, digits),
        "g_zero_excluded": excludes_zero(g_value),
        "status": "CERTIFIED_COMPLETE_FACE_TIER" if certified else "FACE_TIER_NOT_CERTIFIED",
    }, {"g": g_value, "bt": tail_radius}


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
        != "ice.raw-c-correlated-kappa-lambda-gamma1-sign-strip.input.v1"
        or config.get("calculation_id") != CALCULATION_ID
        or config.get("numbered_phase") is not None
        or config.get("resource_caps") != expected_caps()
        or config.get("required_fail_closed_outputs") != expected_nulls()
    ):
        raise AssertionError("identity, resource, or null-output policy drift")
    conventions = config["declared_conventions"]
    if (
        conventions["precision_ladder_decimal_digits"] != [80, 120]
        or conventions["kernel_panel_ladder"] != [512, 1024]
        or conventions["switch_to_Q0_segment_ladder"] != [16, 32]
        or conventions["compact_taylor_order"] != 12
        or [
            (item["Q_cut"], item["segments"])
            for item in conventions["cutoff_segment_ladder"]
        ]
        != [("-5", 16), ("-5", 32), ("-6", 32)]
    ):
        raise AssertionError("precision, panel, or Taylor ladder drift")
    verify_method_sources(root, config["method_reuse"])
    upstream: dict[str, dict[str, Any]] = {}
    upstream_records: list[dict[str, str]] = []
    for item in config["upstream_results"]:
        payload, record = verify_upstream(root, item)
        upstream[item["path"]] = payload
        upstream_records.append(record)
    upstream_paths = [item["path"] for item in config["upstream_results"]]
    lg_result = upstream[upstream_paths[0]]
    bessel_result = upstream[upstream_paths[1]]
    boundary_result = upstream[upstream_paths[2]]
    previous_result = upstream[upstream_paths[3]]
    if (
        "Q>=4, |lambda|<=1e-4, 0<=kappa<=8"
        not in lg_result["declared_conventions"]["real_box"]
        or boundary_result["declared_conventions"]["boundary_map"]
        != conventions["boundary_map"]
        or boundary_result["declared_conventions"]["reference_equation"]
        != conventions["reference_equation"]
        or previous_result["check_summary"]["all_executable_checks_passed"]
        is not True
    ):
        raise AssertionError("pinned scope or boundary convention drift")

    audit = Audit()
    exact_audit(audit)
    if len(audit.exact) > expected_caps()["symbolic_checks"]:
        raise AssertionError("symbolic check cap exceeded")
    lg_checks = {
        item["id"]: item for item in lg_result.get("exact_checks", [])
    }
    required_lg_checks = {
        "rawc.lg.coefficient",
        "rawc.lg.relative_delta",
        "rawc.lg.relative_delta_prime",
        "rawc.lg.relative_delta_second",
        "rawc.lg.wkb_residual",
        "rawc.lg.factored_residual",
        "rawc.lg.dlmf_control_integrand",
        "rawc.lg.lambda_shape_monotone",
        "rawc.lg.kappa_shape_monotone",
        "rawc.lg.lambda_corner_lt_rational",
        "rawc.lg.kappa_corner_lt_rational",
        "rawc.lg.positivity",
        "rawc.lg.residual_envelope_algebra",
        "rawc.lg.tail_expression_le_elementary",
        "rawc.lg.error_budget_small",
    }
    lg_guards = {
        item["id"]: item for item in lg_result.get("theorem_guards", [])
    }
    lg_error_text = lg_result["analytic_calculation"]["at_Q_plus_4"][
        "sqrt_A_normalized_log_derivative_difference_bound"
    ]
    lg_error = sp.Rational(lg_error_text)
    lg_pin_ok = bool(
        lg_result["check_summary"]["all_executable_checks_passed"] is True
        and all(
            identifier in lg_checks
            and lg_checks[identifier].get("passed") is True
            for identifier in required_lg_checks
        )
        and "rawc.lg.guard.dlmf_2_7_23_25" in lg_guards
        and lg_guards["rawc.lg.guard.dlmf_2_7_23_25"].get("verified") is True
        and 0 < lg_error < sp.Rational(1, 500)
    )
    audit.control(
        "rawc.signstrip.plus_anchor.pinned_uniform_lg_envelope",
        lg_pin_ok,
        "The hash-pinned full real-box Liouville-Green result has all required coefficient, residual, tail and DLMF guard checks passed and its actual sqrt(A)-normalized logarithmic-direction error is below the b=1/500 constant used by this corridor sensitivity derivation.",
        pinned_real_box=lg_result["declared_conventions"]["real_box"],
        required_passed_check_ids=sorted(required_lg_checks),
        pinned_error=lg_error_text,
        local_relaxation="1/500",
    )
    audit.guard(
        "rawc.signstrip.guard.selected_actual_family",
        "Liouville-Green selected real recessive family plus forced-Wronskian logarithmic sensitivity",
        "The pinned construction is uniform on Q>=4, abs(lambda)<=1e-4 and 0<=kappa<=8; this run rechecks that the expanded corridor lies inside that box and transports its Bessel-relative actual direction through an invariant rho tube.",
        "Only the same selected real plus family and its projective direction are covered; no arbitrary compact-IVP family or complex spectral parameter is introduced.",
    )
    audit.guard(
        "rawc.signstrip.guard.whole_step_transfer",
        "Taylor theorem with full-box D13 remainder and continuous parameter dependence of finite linear ODE systems",
        "Every exact rational step uses the complete kappa/lambda interval, analytic coefficient derivatives, a Gronwall state tube and an order-13 remainder bound.",
        "This validates the finite Qswitch-to-Q0 corridor and two face transfers; it is not a black-box numerical ODE call.",
    )
    audit.guard(
        "rawc.signstrip.guard.projective_normalization",
        "Nonzero common-amplitude projective normalization",
        "The actual plus direction is nonzero at the switch and the full corridor transfer must exclude zero from its Q0 amplitude before division.",
        "Within that chart, G=Gamma_1/u(Q0) has exactly the same zeros as the selected declared Gamma_1; no absolute amplitude or sign is obtained.",
    )
    audit.guard(
        "rawc.signstrip.guard.complete_tail_continuity",
        "Wronskian identity, uniform rotating-frame domination and uniform convergence",
        "The finite-IVP states and c_kappa are jointly real-continuous, while the displayed a- and potential-mass bounds dominate the omitted half-line uniformly on the compact rectangle.",
        "The complete normalized functional G is jointly continuous on the declared rectangle only; no nonreal Weyl or spectral object follows.",
    )
    audit.guard(
        "rawc.signstrip.guard.uniform_ivt",
        "Intermediate value theorem applied separately at each fixed lambda",
        "The two exact kappa-face enclosures are strict and have opposite signs uniformly for every lambda in the same closed slab.",
        "For each lambda there is at least one interior kappa zero. Uniqueness, a continuous selector, continuation, velocity and roots outside the corridor are not conclusions.",
    )

    root_cfg = conventions["root_bracket_1"]
    root_left = exact_rational(root_cfg["left_exact"])
    root_right = exact_rational(root_cfg["right_exact"])
    padding = exact_rational(conventions["kappa_corridor"]["padding_exact"])
    kappa_left = root_left - padding
    kappa_right = root_right + padding
    lambda_left = exact_rational(conventions["lambda_slab"]["left_exact"])
    lambda_right = exact_rational(conventions["lambda_slab"]["right_exact"])
    kappa_corridor = bracket_band(kappa_left, kappa_right)
    lambda_slab = bracket_band(lambda_left, lambda_right)
    entering_cfg = conventions["plus_tail_sensitivity_Qplus"]
    entering = bracket_band(
        exact_rational(entering_cfg["lower_exact"]),
        exact_rational(entering_cfg["upper_exact"]),
    )
    audit.inequality(
        "rawc.signstrip.declared_rectangle",
        bool(
            0 < kappa_left < root_left < root_right < kappa_right < 8
            and lambda_left < 0 < lambda_right
            and lambda_left == -lambda_right
        ),
        "The exact enlarged corridor is ordered inside the pinned 0<=kappa<=8 domain and the single lambda slab is closed, symmetric and contains zero.",
        kappa_left_exact=str(kappa_left),
        root_left_exact=str(root_left),
        root_right_exact=str(root_right),
        kappa_right_exact=str(kappa_right),
        lambda_left_exact=str(lambda_left),
        lambda_right_exact=str(lambda_right),
    )
    root_row = bessel_result["certified_calculation"][
        "endpoint_characteristic"
    ]["root_rows"][0]
    root_certificate = root_row["certified_high_precision_bracket"]
    precision_120 = next(
        row for row in root_row["precision_runs"] if row["decimal_digits"] == 120
    )
    root_linked = bool(
        root_row["root_index"] == 1
        and root_certificate["left_exact"] == str(root_left)
        and root_certificate["right_exact"] == str(root_right)
        and root_certificate["at_least_one_real_sign_changing_zero"] is True
        and precision_120["signs"] == [-1, 1]
    )
    audit.inequality(
        "rawc.signstrip.lambda_zero_root1_regression",
        root_linked,
        "The exact lambda-zero sign-changing root-1 bracket is strictly inside the newly declared corridor; it is a regression anchor, not a uniqueness assumption.",
        root_index=root_row["root_index"],
        signs=precision_120["signs"],
    )

    panel_counts = conventions["kernel_panel_ladder"]
    tail_y = exact_rational(conventions["kernel_tail_y"])
    digits = int(conventions["ball_output_digits"])
    q0_records: dict[str, list[dict[str, Any]]] = {
        "corridor": [],
        "left_face": [],
        "right_face": [],
    }
    q0_balls: dict[str, list[dict[str, arb | None]]] = {
        key: [] for key in q0_records
    }
    switch_records: list[dict[str, Any]] = []
    switch_balls_by_tier: list[dict[str, arb]] = []

    for tier, dps in enumerate(
        conventions["precision_ladder_decimal_digits"], start=1
    ):
        ctx.dps = int(dps)
        c_value = 6 * arb.pi() ** 2
        x_plus = c_value * arb(exact_rational(conventions["Q_plus"])).exp()
        x_switch = c_value * arb(exact_rational(conventions["Q_switch"])).exp()
        coarse_kernels = affine.comparison_integrals(
            x_switch,
            x_plus,
            panels=int(panel_counts[0]),
            tail_y=tail_y,
        )
        refined_kernels = affine.comparison_integrals(
            x_switch,
            x_plus,
            panels=int(panel_counts[1]),
            tail_y=tail_y,
        )
        coarse_p, _ = affine.endpoint_comparison(
            x_switch, x_plus, entering, coarse_kernels
        )
        refined_p, comparison_parts = affine.endpoint_comparison(
            x_switch, x_plus, entering, refined_kernels
        )
        kernel_values = [
            coarse_kernels["lower_comparison_integral"],
            coarse_kernels["upper_comparison_integral"],
            refined_kernels["lower_comparison_integral"],
            refined_kernels["upper_comparison_integral"],
        ]
        if not all(isinstance(value, arb) for value in kernel_values):
            raise AssertionError("kernel result type drift")
        kernel_refinement_ok = bool(
            contains_interval(kernel_values[0], kernel_values[2])
            and contains_interval(kernel_values[1], kernel_values[3])
            and contains_interval(coarse_p, refined_p)
            and refined_p.lower() > 0
        )
        audit.control(
            f"rawc.signstrip.switch.tier{tier}.kernel_refinement",
            kernel_refinement_ok,
            "The 1024-panel monotone comparison enclosure is nested in the 512-panel enclosure and the positive y>24 extension is analytic.",
            decimal_digits=dps,
            coarse_p_Qswitch=interval_record(coarse_p, digits),
            refined_p_Qswitch=interval_record(refined_p, digits),
            homogeneous_entering_lower=interval_record(
                comparison_parts["homogeneous_lower"], digits
            ),
            homogeneous_entering_upper=interval_record(
                comparison_parts["homogeneous_upper"], digits
            ),
        )
        rho0_plus, bessel_plus = affine.bessel_rho(
            audit, x_plus, kappa_corridor
        )
        rho0_switch, bessel_switch = affine.bessel_rho(
            audit, x_switch, kappa_corridor
        )
        rho0_left, bessel_left = affine.bessel_rho(
            audit, x_switch, arb(kappa_left)
        )
        rho0_right, bessel_right = affine.bessel_rho(
            audit, x_switch, arb(kappa_right)
        )
        rho_plus = rho0_plus.real + affine.interval_product_hull(
            lambda_slab, entering
        )
        rho_switch_corridor_raw = rho0_switch.real + affine.interval_product_hull(
            lambda_slab, refined_p
        )
        rho_switch_left_raw = rho0_left.real + affine.interval_product_hull(
            lambda_slab, refined_p
        )
        rho_switch_right_raw = rho0_right.real + affine.interval_product_hull(
            lambda_slab, refined_p
        )
        lambda_cap = arb(lambda_right)
        sqrt_c = c_value.sqrt()
        t3 = arb(3) * arb(3).sqrt() / sqrt_c
        derivative_margin = 2 - (arb(3) / 2) * lambda_cap * arb(2).exp()
        lower_barrier_margin = (
            6
            - arb((kappa_corridor**2).upper())
            - arb(1) / 4
            - lambda_cap * arb(t3.upper())
        )
        upper_barrier_bracket = (
            arb((kappa_corridor**2).lower())
            + 6
            + arb(9) / 4
            - lambda_cap * arb(t3.upper())
        )
        barrier_ok = bool(
            x_switch.lower() > 3
            and rho_plus.lower() >= -1
            and rho_plus.upper() <= 1
            and derivative_margin.lower() > 0
            and lower_barrier_margin.lower() > 0
            and upper_barrier_bracket.lower() > 0
        )
        audit.control(
            f"rawc.signstrip.switch.tier{tier}.closed_corridor_barrier",
            barrier_ok,
            "The newly evaluated Qplus actual-family seed and exact worst-case inward vector-field margins independently prove the backward-flow invariant barrier rho in [-1,1] through the rational switch on the full expanded rectangle; no raw Qswitch interval containment is assumed.",
            decimal_digits=dps,
            rho_actual_Qplus=interval_record(rho_plus, digits),
            raw_affine_rho_Qswitch_corridor=interval_record(
                rho_switch_corridor_raw, digits
            ),
            backward_flow_orientation="rho_x at rho=-1 is strictly negative and rho_x at rho=+1 is strictly positive, so -rho_x points inward as x decreases",
            derivative_margin=interval_record(derivative_margin, digits),
            lower_barrier_margin=interval_record(lower_barrier_margin, digits),
            upper_barrier_bracket=interval_record(
                upper_barrier_bracket, digits
            ),
        )
        bessel_items = [
            ("corridor_Qplus", rho0_plus, bessel_plus),
            ("corridor_Qswitch", rho0_switch, bessel_switch),
            ("left_face_Qswitch", rho0_left, bessel_left),
            ("right_face_Qswitch", rho0_right, bessel_right),
        ]
        bessel_ok = all(
            value.abs_lower() > 0
            and rho_value.imag.lower() <= 0 <= rho_value.imag.upper()
            for _, rho_value, value in bessel_items
        )
        audit.control(
            f"rawc.signstrip.switch.tier{tier}.bessel_denominators",
            bessel_ok,
            "Every newly evaluated expanded-corridor or exact-face modified-Bessel denominator excludes zero; the imaginary enclosure of each real-parameter logarithmic-direction evaluation contains zero as a numerical consistency control.",
            decimal_digits=dps,
            evaluations={
                label: {
                    "rho": affine.complex_record(rho_value, digits),
                    "K": affine.complex_record(value, digits),
                }
                for label, rho_value, value in bessel_items
            },
        )
        invariant_barrier = interval_from_bounds(arb(-1), arb(1))
        rho_switch_corridor = intersection(
            rho_switch_corridor_raw, invariant_barrier
        )
        rho_switch_left = intersection(rho_switch_left_raw, invariant_barrier)
        rho_switch_right = intersection(
            rho_switch_right_raw, invariant_barrier
        )
        if (
            rho_switch_corridor is None
            or rho_switch_left is None
            or rho_switch_right is None
        ):
            raise AssertionError(
                "raw affine and independently proved invariant switch enclosures are disjoint"
            )
        switch_domains = {
            "corridor": (kappa_corridor, rho_switch_corridor),
            "left_face": (arb(kappa_left), rho_switch_left),
            "right_face": (arb(kappa_right), rho_switch_right),
        }
        switch_domain_ok = bool(
            barrier_ok
            and all(
                rho_value.is_finite()
                for _, rho_value in switch_domains.values()
            )
        )
        audit.control(
            f"rawc.signstrip.switch.tier{tier}.domain_seeds",
            switch_domain_ok,
            "The raw Bessel/affine and independently proved invariant-barrier enclosures have nonempty intersections; only these intersections seed the full corridor and exact-face Qswitch-to-Q0 transfers.",
            decimal_digits=dps,
            exact_invariant_set="[-1,1]",
            invariant_barrier_outward_ball=interval_record(
                invariant_barrier, digits
            ),
            outward_storage_scope="The returned balls outwardly enclose the mathematical intersections and are not required to be literal subsets of the exact invariant set.",
            raw_affine={
                "corridor": interval_record(rho_switch_corridor_raw, digits),
                "left_face": interval_record(rho_switch_left_raw, digits),
                "right_face": interval_record(rho_switch_right_raw, digits),
            },
            transfer_seed_intersection={
                "corridor": interval_record(rho_switch_corridor, digits),
                "left_face": interval_record(rho_switch_left, digits),
                "right_face": interval_record(rho_switch_right, digits),
            },
        )
        switch_records.append(
            {
                "tier": tier,
                "decimal_digits": dps,
                "MVT_p_Qswitch": interval_record(refined_p, digits),
                "rho_actual_Qplus_corridor": interval_record(rho_plus, digits),
                "raw_affine_rho_Qswitch": {
                    "corridor": interval_record(
                        rho_switch_corridor_raw, digits
                    ),
                    "left_face": interval_record(rho_switch_left_raw, digits),
                    "right_face": interval_record(rho_switch_right_raw, digits),
                },
                "exact_invariant_set": "[-1,1]",
                "invariant_barrier_outward_ball": interval_record(
                    invariant_barrier, digits
                ),
                "transfer_seed_intersection": {
                    "corridor": interval_record(rho_switch_corridor, digits),
                    "left_face": interval_record(rho_switch_left, digits),
                    "right_face": interval_record(rho_switch_right, digits),
                },
                "certified": bool(
                    kernel_refinement_ok
                    and barrier_ok
                    and bessel_ok
                    and switch_domain_ok
                ),
            }
        )
        switch_balls_by_tier.append(
            {
                "p": refined_p,
                "corridor": rho_switch_corridor,
                "left_face": rho_switch_left,
                "right_face": rho_switch_right,
            }
        )
        for label, (kappa_value, rho_value) in switch_domains.items():
            for segments in conventions["switch_to_Q0_segment_ladder"]:
                record, balls = propagate_q0(
                    audit,
                    label=label,
                    tier=tier,
                    dps=int(dps),
                    segments=int(segments),
                    kappa=kappa_value,
                    lam=lambda_slab,
                    rho_switch=rho_value,
                    conventions=conventions,
                )
                q0_records[label].append(record)
                q0_balls[label].append(balls)

    switch_overlap = all(
        intersection(switch_balls_by_tier[0][key], switch_balls_by_tier[1][key])
        is not None
        for key in ("p", "corridor", "left_face", "right_face")
    )
    audit.control(
        "rawc.signstrip.switch.precision_overlap",
        switch_overlap,
        "The two precision tiers overlap for the affine comparison and all three actual-family switch seeds.",
    )

    q0_final: dict[str, dict[str, arb | None]] = {}
    q0_final_certified: dict[str, bool] = {}
    q0_final_records: list[dict[str, Any]] = []
    for label in ("corridor", "left_face", "right_face"):
        rows = q0_balls[label]
        for tier_index in range(2):
            coarse = rows[2 * tier_index]
            refined = rows[2 * tier_index + 1]
            overlap_ok = all(
                coarse[key] is not None
                and refined[key] is not None
                and intersection(coarse[key], refined[key]) is not None
                for key in ("v", "vq", "rho")
            )
            audit.control(
                f"rawc.signstrip.q0.{label}.tier{tier_index + 1}.segment_refinement_overlap",
                overlap_ok,
                "The 16/32-step switch-to-Q0 enclosures overlap for the selected projective endpoint state.",
            )
        for ladder_index, segments in enumerate(
            conventions["switch_to_Q0_segment_ladder"]
        ):
            low = rows[ladder_index]
            high = rows[ladder_index + 2]
            overlap_ok = all(
                low[key] is not None
                and high[key] is not None
                and intersection(low[key], high[key]) is not None
                for key in ("v", "vq", "rho")
            )
            audit.control(
                f"rawc.signstrip.q0.{label}.segments{segments}.precision_overlap",
                overlap_ok,
                "The 80/120-decimal switch-to-Q0 enclosures overlap.",
            )
        final = {
            key: all_intersection([row[key] for row in rows])
            for key in ("v", "vq", "rho")
        }
        final_ok = bool(
            all(final[key] is not None for key in final)
            and final["v"] is not None
            and excludes_zero(final["v"])
            and final["rho"] is not None
            and final["rho"].is_finite()
        )
        audit.control(
            f"rawc.signstrip.q0.{label}.final_chart",
            final_ok,
            "All step and precision rows share a finite Q0 projective endpoint enclosure whose propagated switch-normalized amplitude excludes zero.",
            v_Q0=interval_record(final["v"], digits)
            if final["v"] is not None
            else None,
            v_Q_Q0=interval_record(final["vq"], digits)
            if final["vq"] is not None
            else None,
            rho_Q0=interval_record(final["rho"], digits)
            if final["rho"] is not None
            else None,
            Q0_amplitude_excludes_zero=(
                excludes_zero(final["v"]) if final["v"] is not None else False
            ),
        )
        q0_final[label] = final
        q0_final_certified[label] = final_ok
        q0_final_records.append(
            {
                "label": label,
                "certified": final_ok,
                "v_Q0": interval_record(final["v"], digits)
                if final["v"] is not None
                else None,
                "v_Q_Q0": interval_record(final["vq"], digits)
                if final["vq"] is not None
                else None,
                "rho_Q0": interval_record(final["rho"], digits)
                if final["rho"] is not None
                else None,
                "Q0_amplitude_excludes_zero": (
                    excludes_zero(final["v"])
                    if final["v"] is not None
                    else False
                ),
                "status": "CERTIFIED_Q0_CHART"
                if final_ok
                else "Q0_CHART_NOT_CERTIFIED",
            }
        )

    tail_records: dict[str, list[dict[str, Any]]] = {
        "left_face": [],
        "right_face": [],
    }
    tail_balls: dict[str, list[dict[str, arb]]] = {
        key: [] for key in tail_records
    }
    face_specs = {
        "left_face": arb(kappa_left),
        "right_face": arb(kappa_right),
    }
    tail_ready = all(
        q0_final_certified.get(label) is True
        and q0_final[label]["rho"] is not None
        and q0_final[label]["v"] is not None
        and excludes_zero(q0_final[label]["v"])
        for label in face_specs
    )
    if tail_ready:
        for tier, dps in enumerate(
            conventions["precision_ladder_decimal_digits"], start=1
        ):
            for label, kappa_value in face_specs.items():
                rho_value = q0_final[label]["rho"]
                if rho_value is None:
                    raise AssertionError("tail readiness drift")
                for cutoff in conventions["cutoff_segment_ladder"]:
                    record, balls = propagate_face_tail(
                        audit,
                        label=label,
                        tier=tier,
                        dps=int(dps),
                        cutoff=cutoff,
                        kappa=kappa_value,
                        lam=lambda_slab,
                        rho_q0=rho_value,
                        conventions=conventions,
                    )
                    tail_records[label].append(record)
                    tail_balls[label].append(balls)
    else:
        audit.control(
            "rawc.signstrip.tail.q0_seed_availability",
            False,
            "Both face Q0 charts must certify before the complete-tail calculation can start.",
        )

    face_intersections: dict[str, arb | None] = {
        "left_face": None,
        "right_face": None,
    }
    face_final_records: list[dict[str, Any]] = []
    if tail_ready:
        for label in ("left_face", "right_face"):
            rows = tail_balls[label]
            for tier_index in range(2):
                offset = 3 * tier_index
                coarse, refined, deeper = rows[offset : offset + 3]
                refinement_ok = intersection(coarse["g"], refined["g"]) is not None
                audit.control(
                    f"rawc.signstrip.tail.{label}.tier{tier_index + 1}.minus5_refinement_overlap",
                    refinement_ok,
                    "The Qc=-5 16/32-step complete-functional enclosures overlap.",
                )
                cutoff_ok = bool(
                    intersection(coarse["g"], deeper["g"]) is not None
                    and deeper["bt"].upper() < coarse["bt"].upper()
                )
                audit.control(
                    f"rawc.signstrip.tail.{label}.tier{tier_index + 1}.cutoff_overlap_and_tail_decrease",
                    cutoff_ok,
                    "The Qc=-5 and Qc=-6 complete-functional enclosures overlap and the analytic omitted-tail radius decreases at the deeper cutoff.",
                )
            for ladder_index, cutoff in enumerate(
                conventions["cutoff_segment_ladder"]
            ):
                low = rows[ladder_index]
                high = rows[ladder_index + 3]
                precision_ok = intersection(low["g"], high["g"]) is not None
                audit.control(
                    f"rawc.signstrip.tail.{label}.{cutoff['label']}.precision_overlap",
                    precision_ok,
                    "The 80/120-decimal complete-functional face enclosures overlap.",
                )
            final_g = all_intersection([row["g"] for row in rows])
            final_ok = bool(final_g is not None and excludes_zero(final_g))
            audit.control(
                f"rawc.signstrip.tail.{label}.strict_final_sign",
                final_ok,
                "All cutoff, step and precision rows share one strict complete Q0-normalized face-sign enclosure.",
                g_Q0_normalized=interval_record(final_g, digits)
                if final_g is not None
                else None,
            )
            face_intersections[label] = final_g
            face_final_records.append(
                {
                    "label": label,
                    "kappa_exact": str(
                        kappa_left if label == "left_face" else kappa_right
                    ),
                    "lambda_slab": {
                        "left_exact": str(lambda_left),
                        "right_exact": str(lambda_right),
                    },
                    "g_Q0_normalized": interval_record(final_g, digits)
                    if final_g is not None
                    else None,
                    "strict_sign": (
                        "POSITIVE"
                        if final_g is not None and final_g.lower() > 0
                        else (
                            "NEGATIVE"
                            if final_g is not None and final_g.upper() < 0
                            else "UNRESOLVED"
                        )
                    ),
                    "certified": final_ok,
                }
            )

    left_g = face_intersections["left_face"]
    right_g = face_intersections["right_face"]
    opposite_faces = bool(
        left_g is not None
        and right_g is not None
        and (
            (left_g.upper() < 0 and right_g.lower() > 0)
            or (left_g.lower() > 0 and right_g.upper() < 0)
        )
    )
    corridor_chart = q0_final["corridor"]["v"]
    uniform_ivt_ok = bool(
        opposite_faces
        and corridor_chart is not None
        and excludes_zero(corridor_chart)
    )
    audit.control(
        "rawc.signstrip.uniform_ivt_hypotheses",
        uniform_ivt_ok,
        "The entire KxLambda Q0 chart is nonzero and the two complete-functional kappa faces have strict opposite signs, so the fixed-lambda IVT hypotheses hold uniformly on the one closed slab.",
        corridor_v_Q0=interval_record(corridor_chart, digits)
        if corridor_chart is not None
        else None,
        left_face_g=interval_record(left_g, digits)
        if left_g is not None
        else None,
        right_face_g=interval_record(right_g, digits)
        if right_g is not None
        else None,
        opposite_strict_signs=opposite_faces,
    )

    kernel_panels_evaluated = sum(panel_counts) * len(
        conventions["precision_ladder_decimal_digits"]
    )
    q0_segment_rows = sum(len(rows) for rows in q0_records.values())
    cutoff_segment_rows = sum(len(rows) for rows in tail_records.values())
    q0_compact_steps = sum(
        int(row["segments"])
        for rows in q0_records.values()
        for row in rows
    )
    tail_compact_steps = sum(
        int(row["cutoff"]["segments"])
        for rows in tail_records.values()
        for row in rows
    )
    compact_steps = q0_compact_steps + tail_compact_steps
    if (
        kernel_panels_evaluated > expected_caps()["kernel_panels_evaluated"]
        or q0_segment_rows > expected_caps()["q0_segment_rows"]
        or cutoff_segment_rows > expected_caps()["cutoff_segment_rows"]
        or compact_steps > expected_caps()["compact_steps"]
        or audit.bessel_evaluations
        > expected_caps()["ball_bessel_evaluations"]
    ):
        raise AssertionError("measured calculation resource cap exceeded")

    exact_pass = all(item["passed"] for item in audit.exact)
    controls_pass = all(item["passed"] for item in audit.controls)
    certified = bool(exact_pass and controls_pass and uniform_ivt_ok)
    verdict = (
        "CERTIFY_CONNECTED_LAMBDA_SLAB_AT_LEAST_ONE_DECLARED_BOUNDARY_ZERO_PER_LAMBDA"
        if certified
        else "CORRELATED_GAMMA1_SIGN_STRIP_NOT_CERTIFIED"
    )
    existence_statement = (
        "For every lambda in [-1/10000,1/10000], at least one kappa in the open declared corridor has G(kappa,lambda)=0; because the selected actual u_plus(Q0) is uniformly nonzero, the same point is a zero of the selected declared Gamma_1 boundary functional."
        if certified
        else None
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input},
        "upstream_results": upstream_records,
        "method_reuse": config["method_reuse"],
        "primary_sources": config["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "controls_passed": sum(item["passed"] for item in audit.controls),
            "controls_total": len(audit.controls),
            "theorem_guards": len(audit.guards),
            "all_executable_checks_passed": bool(exact_pass and controls_pass),
        },
        "certified_calculation": {
            "scope": "one expanded root-1 kappa corridor times the single closed real lambda slab [-1e-4,1e-4]",
            "kappa_corridor": {
                "left_exact": str(kappa_left),
                "right_exact": str(kappa_right),
                "root_bracket_1_strictly_inside": True,
            },
            "lambda_slab": {
                "left_exact": str(lambda_left),
                "right_exact": str(lambda_right),
            },
            "switch_rows": switch_records,
            "q0_transfer_rows": q0_records,
            "q0_final_charts": q0_final_records,
            "face_tail_rows": tail_records,
            "face_final_intersections": face_final_records,
            "root_existence_each_lambda_in_declared_strip_certified": certified,
            "existence_statement": existence_statement,
            "proof_mode": "UNIFORM_NONZERO_Q0_CHART_PLUS_STRICT_OPPOSITE_COMPLETE_FACE_SIGNS_PLUS_FIXED_LAMBDA_INTERMEDIATE_VALUE_THEOREM",
            "next_mathematical_gap": "A separate question must establish kappa transversality or another injectivity mechanism before uniqueness, a continuous root selector, continuation or velocity; roots outside this corridor remain uncounted.",
        },
        "non_claim": "This is a real projective IVT existence strip in a computational workbench, not an absolute amplitude, unique/continuous root curve, Weyl function, spectral measure, RAQ result, empirical result, or physics discovery.",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_checks": len(audit.exact),
            "kernel_panels_evaluated": kernel_panels_evaluated,
            "compact_steps": compact_steps,
            "q0_compact_steps": q0_compact_steps,
            "tail_compact_steps": tail_compact_steps,
            "q0_segment_rows": q0_segment_rows,
            "cutoff_segment_rows": cutoff_segment_rows,
            "ball_bessel_evaluations": audit.bessel_evaluations,
            "precision_tiers": 2,
            "lambda_slabs": 1,
            "kappa_faces": 2,
            "root_brackets": 1,
            "ode_calls": 0,
            "root_calls": 0,
            "quadrature_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "bisection_steps": 0,
            "adjacent_result_files_written": 1,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_flint": importlib.metadata.version("python-flint"),
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
                "exact_passed": sum(item["passed"] for item in audit.exact),
                "exact_total": len(audit.exact),
                "controls_passed": sum(
                    item["passed"] for item in audit.controls
                ),
                "controls_total": len(audit.controls),
                "Q0_corridor_amplitude": (
                    interval_record(corridor_chart, digits)
                    if corridor_chart is not None
                    else None
                ),
                "left_face_g": (
                    interval_record(left_g, digits) if left_g is not None else None
                ),
                "right_face_g": (
                    interval_record(right_g, digits)
                    if right_g is not None
                    else None
                ),
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
