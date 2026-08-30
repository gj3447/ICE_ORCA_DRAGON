#!/usr/bin/env python3
"""Scale-free validated interval-Taylor outer transfer for the raw-C family.

The inherited Liouville--Green theorem selects the actual plus-recessive
direction, and its Riccati barrier transports that direction to a rational
switch with x>3.  This runner then removes the nonzero common amplitude and
propagates the full barrier-admissible rho box by local Arb Taylor enclosures
with whole-step remainders before closing the Q<-4 quotient tail.  The box
contains the selected actual direction but does not newly localize that
direction between Q=4 and the switch.  It is not a black-box numerical ODE
solve, a root continuation, spectral data, or RAQ.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = "RAW_C_ACTUAL_NONZERO_LAMBDA_HYBRID_VALIDATED_TRANSFER_INPUTS.json"
RESULT_NAME = "RAW_C_ACTUAL_NONZERO_LAMBDA_HYBRID_VALIDATED_TRANSFER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_actual_nonzero_lambda_hybrid_validated_transfer.py"
)
EXPECTED_INPUT_SHA256 = "131ffcbe20accf17ec65ed30a5ccbbc3d01fc0cb59386553da9953163cd77da0"
CALCULATION_ID = "RawCActualNonzeroLambdaHybridValidatedTransfer"
RESULT_SCHEMA = (
    "ice.raw-c-actual-nonzero-lambda-hybrid-validated-transfer.result.v1"
)
RESULT_PREFIX = "RAW_C_ACTUAL_NONZERO_LAMBDA_HYBRID_VALIDATED_TRANSFER_RESULT="
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
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 3000,
        "compact_q_segments": 16,
        "compact_taylor_order": 12,
        "ball_bessel_evaluations": 6,
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
            all(sp.simplify(entry) == 0 for entry in reduced)
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
            {"id": identifier, "passed": bool(passed), "statement": statement, **data}
        )

    def ball_check(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.ball.append(
            {"id": identifier, "passed": bool(passed), "statement": statement, **data}
        )

    def guard(
        self, identifier: str, theorem: str, hypotheses: str, scope: str
    ) -> None:
        self.register(identifier)
        self.guards.append(
            {
                "id": identifier,
                "verified": True,
                "verification_mode": (
                    "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_ARB_HYPOTHESIS_AUDIT"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": scope,
            }
        )

    def bessel_k(self, z: acb, order: acb) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")
        return z.bessel_k(order)


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if upper < lower:
        raise AssertionError("reversed interval bounds")
    value = arb((lower + upper) / 2, (upper - lower) / 2)
    if not (value.lower() <= lower and value.upper() >= upper):
        raise AssertionError("outward interval construction failed")
    return value


def bracket_band(left: fmpq, right: fmpq) -> arb:
    if not left < right:
        raise AssertionError("reversed exact bracket")
    return arb(arb((left + right) / 2), arb((right - left) / 2))


def symmetric_interval(radius: arb) -> arb:
    upper = arb(radius.upper())
    if upper < 0:
        raise AssertionError("negative symmetric radius")
    return interval_from_bounds(-upper, upper)


def absolute_upper(value: arb) -> arb:
    lower_abs = -value.lower() if value.lower() < 0 else value.lower()
    upper_abs = -value.upper() if value.upper() < 0 else value.upper()
    return arb(lower_abs if lower_abs >= upper_abs else upper_abs)


def absolute_lower(value: arb) -> arb:
    if value.lower() <= 0 <= value.upper():
        return arb(0)
    lower_abs = -value.lower() if value.lower() < 0 else value.lower()
    upper_abs = -value.upper() if value.upper() < 0 else value.upper()
    return arb(lower_abs if lower_abs <= upper_abs else upper_abs)


def maximum(left: arb, right: arb) -> arb:
    return arb(left.upper() if left.upper() >= right.upper() else right.upper())


def interval_width(value: arb) -> arb:
    return arb((value.upper() - value.lower()).upper())


def contains_zero(value: arb) -> bool:
    return bool(value.lower() <= 0 <= value.upper())


def excludes_zero(value: arb) -> bool:
    return bool(value.lower() > 0 or value.upper() < 0)


def contains_interval(outer: arb, inner: arb) -> bool:
    return bool(outer.lower() <= inner.lower() and inner.upper() <= outer.upper())


def intersection(left: arb, right: arb) -> arb | None:
    low = left.lower() if left.lower() >= right.lower() else right.lower()
    high = left.upper() if left.upper() <= right.upper() else right.upper()
    return interval_from_bounds(low, high) if low <= high else None


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "width_upper": interval_width(value).str(digits, radius=False),
        "midpoint_radius": value.str(digits),
    }


def complex_record(value: acb, digits: int) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "absolute_lower": value.abs_lower().str(digits, radius=False),
        "absolute_upper": value.abs_upper().str(digits, radius=False),
    }


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
        - lam * sp.sqrt(x) / sp.sqrt(C)
    )
    audit.identity(
        "rawc.hybrid.coefficient_change",
        coefficient.subs(x, C * sp.exp(Q))
        - (
            C**2 * sp.exp(2 * Q)
            + lam * C * sp.exp(sp.Rational(3, 2) * Q)
            - kappa**2
        ),
        "The Q and x forms of the actual raw-C coefficient agree.",
    )
    audit.identity(
        "rawc.hybrid.rho_x",
        x * rho_x - rho_q,
        "The x-frame Riccati equation is the exact Q equation divided by x.",
    )
    ell_x = -1 - (sp.Rational(1, 2) + rho) / x
    audit.identity(
        "rawc.hybrid.log_amplitude_sign",
        ell_x + r / x,
        "For ell=log u and r=-u_Q/u, ell_x=-r/x.",
    )
    audit.identity(
        "rawc.hybrid.coefficient_first_derivative",
        sp.diff(coefficient.subs(x, C * sp.exp(Q)), Q)
        - (
            2 * C**2 * sp.exp(2 * Q)
            + sp.Rational(3, 2)
            * lam
            * C
            * sp.exp(sp.Rational(3, 2) * Q)
        ),
        "The first whole-step coefficient derivative used by the Taylor majorant is exact.",
    )
    audit.identity(
        "rawc.hybrid.coefficient_second_derivative",
        sp.diff(coefficient.subs(x, C * sp.exp(Q)), Q, 2)
        - (
            4 * C**2 * sp.exp(2 * Q)
            + sp.Rational(9, 4)
            * lam
            * C
            * sp.exp(sp.Rational(3, 2) * Q)
        ),
        "The second whole-step coefficient derivative used by the Taylor majorant is exact.",
    )
    v, vq, a0, aq = sp.symbols("v v_Q A A_Q", real=True)
    first = sp.Matrix([vq, a0 * v])
    second = sp.Matrix([a0 * v, aq * v + a0 * vq])
    B = sp.Matrix([[0, 1], [a0, 0]])
    Bq = sp.Matrix([[0, 0], [aq, 0]])
    audit.identity(
        "rawc.hybrid.state_derivative_recurrence",
        second - (Bq * sp.Matrix([v, vq]) + B * first),
        "The actual-derivative Leibniz recurrence gives the displayed second state derivative.",
    )
    scale = sp.symbols("scale", nonzero=True, real=True)
    audit.identity(
        "rawc.hybrid.scale_free_log_derivative",
        (scale * vq) * v - (scale * v) * vq,
        "A nonzero common amplitude rescaling preserves v_Q/v.",
    )
    integral = sp.symbols("I_minus", real=True)
    gamma = vq - lam * integral
    audit.identity(
        "rawc.hybrid.scale_free_gamma_identity",
        gamma / v - (vq / v - lam * integral / v),
        "When v(Q0) is nonzero, Gamma_1(v)/v(Q0) has the declared quotient form.",
    )
    audit.identity(
        "rawc.hybrid.exact_partition",
        16 * sp.Rational(-11, 160) - (sp.Rational(-4) + sp.Rational(29, 10)),
        "Sixteen exact steps h=-11/160 join Q_switch=-29/10 to Q0=-4.",
    )


def coefficient_derivatives(
    q_base: fmpq, kappa_band: arb, lambda_band: arb, order: int
) -> tuple[arb, list[arb]]:
    c_value = 6 * arb.pi() ** 2
    x_value = c_value * arb(q_base).exp()
    forcing = x_value * x_value.sqrt() / c_value.sqrt()
    values = [x_value**2 + lambda_band * forcing - kappa_band**2]
    for derivative in range(1, order + 1):
        values.append(
            arb(2) ** derivative * x_value**2
            + (arb(3) / 2) ** derivative * lambda_band * forcing
        )
    return x_value, values


def whole_step_majorants(
    q_base: fmpq, kappa_band: arb, lambda_band: arb, order: int
) -> list[arb]:
    c_value = 6 * arb.pi() ** 2
    x_plus = c_value * arb(q_base).exp()
    forcing_plus = x_plus * x_plus.sqrt() / c_value.sqrt()
    lambda_abs = absolute_upper(lambda_band)
    kappa_abs = absolute_upper(kappa_band)
    coefficient_abs = x_plus**2 + lambda_abs * forcing_plus + kappa_abs**2
    majorants = [maximum(arb(1), coefficient_abs)]
    for derivative in range(1, order + 1):
        majorants.append(
            arb(2) ** derivative * x_plus**2
            + (arb(3) / 2) ** derivative * lambda_abs * forcing_plus
        )
    return [arb(value.upper()) for value in majorants]


def apply_coefficient_derivative(
    derivative: int, coefficient_values: list[arb], state: tuple[arb, arb]
) -> tuple[arb, arb]:
    if derivative == 0:
        return state[1], coefficient_values[0] * state[0]
    return arb(0), coefficient_values[derivative] * state[0]


def propagate_box(
    audit: Audit,
    *,
    label: str,
    tier: int,
    dps: int,
    kappa_band: arb,
    lambda_band: arb,
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, arb]]:
    ctx.dps = dps
    digits = int(config["declared_conventions"]["ball_output_digits"])
    order = int(config["declared_conventions"]["compact_taylor_order"])
    segments = int(config["declared_conventions"]["compact_q_segments"])
    q_switch = exact_rational(config["declared_conventions"]["Q_switch"])
    q_zero = exact_rational(config["declared_conventions"]["Q_0"])
    step = (q_zero - q_switch) / segments
    if step != fmpq(-11, 160):
        raise AssertionError("compact exact partition drift")

    c_value = 6 * arb.pi() ** 2
    x_switch = c_value * arb(q_switch).exp()
    rho_switch = arb(0, 1)
    state = (arb(1), -(x_switch + arb(1) / 2 + rho_switch))
    switch_ok = bool(
        x_switch.is_finite()
        and x_switch.lower() > 3
        and state[1].is_finite()
        and state[1].upper() < 0
    )
    audit.ball_check(
        f"rawc.hybrid.{label}.tier{tier}.switch_barrier",
        switch_ok,
        "The rational switch remains inside the inherited x>=3 no-node barrier and gives the full barrier-admissible scale-free two-state outer box.",
        decimal_digits=dps,
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
        _, coefficient_values = coefficient_derivatives(
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
            and tube_norm.lower() >= 0
            and remainder.is_finite()
            and remainder.lower() >= 0
            and next_state[0].is_finite()
            and next_state[1].is_finite()
        )
        audit.ball_check(
            f"rawc.hybrid.{label}.tier{tier}.step{index + 1}.whole_step_taylor",
            step_ok,
            "The order-12 actual-derivative Taylor polynomial is enlarged by the whole-step D_13 |h|^13/13! remainder over the full parameter boxes.",
            q_base=str(q_base),
            q_next=str(q_next),
            derivative_convention=(
                "ACTUAL_DERIVATIVES_WITH_SINGLE_ENDPOINT_TAYLOR_FACTORIAL"
            ),
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
                "coefficient_norm_upper": majorants[0].str(digits, radius=False),
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

    width_target = arb(
        exact_rational(config["declared_conventions"]["scale_free_width_target"])
    )
    endpoint_ok = bool(
        denominator_ok
        and ratio is not None
        and correction is not None
        and scale_free_gamma is not None
        and ratio.is_finite()
        and correction.is_finite()
        and correction.lower() >= 0
        and scale_free_gamma.is_finite()
        and interval_width(scale_free_gamma).upper() < width_target.lower()
    )
    audit.ball_check(
        f"rawc.hybrid.{label}.tier{tier}.scale_free_gamma",
        endpoint_ok,
        "The Q0 amplitude excludes zero, the complete rotating-frame quotient tail is finite, and the scale-free Gamma_1 interval meets the preregistered absolute-width gate.",
        v_Q0=interval_record(v_zero, digits),
        v_Q_Q0=interval_record(vq_zero, digits),
        Q0_amplitude_excludes_zero=denominator_ok,
        endpoint_log_derivative=(
            interval_record(ratio, digits) if ratio is not None else None
        ),
        quotient_tail_correction_absolute_upper=(
            interval_record(correction, digits) if correction is not None else None
        ),
        scale_free_Gamma1=(
            interval_record(scale_free_gamma, digits)
            if scale_free_gamma is not None
            else None
        ),
        scale_free_width_target=str(
            config["declared_conventions"]["scale_free_width_target"]
        ),
        scale_free_Gamma1_contains_zero=(
            contains_zero(scale_free_gamma)
            if scale_free_gamma is not None
            else None
        ),
    )

    record = {
        "label": label,
        "decimal_digits": dps,
        "kappa_bracket": interval_record(kappa_band, digits),
        "lambda_box": interval_record(lambda_band, digits),
        "switch": {
            "Q": str(q_switch),
            "x": interval_record(x_switch, digits),
            "rho": interval_record(rho_switch, digits),
            "state_scope": "FULL_INHERITED_BARRIER_ADMISSIBLE_OUTER_BOX_CONTAINING_SELECTED_ACTUAL_DIRECTION",
        },
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
            contains_zero(scale_free_gamma)
            if scale_free_gamma is not None
            else None
        ),
        "status": "CERTIFIED_TIER" if endpoint_ok else "TIER_NOT_CERTIFIED",
    }
    return record, {
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
        != "ice.raw-c-actual-nonzero-lambda-hybrid-validated-transfer.input.v1"
        or config.get("calculation_id") != CALCULATION_ID
        or config.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if (
        config.get("resource_caps") != expected_caps()
        or config.get("required_fail_closed_outputs") != expected_nulls()
        or config["declared_conventions"]["precision_ladder_decimal_digits"]
        != [80, 120]
        or config["declared_conventions"]["compact_q_segments"] != 16
        or config["declared_conventions"]["compact_taylor_order"] != 12
    ):
        raise AssertionError("resource, precision, topology or null-output drift")

    expected_upstream_paths = [
        "cpt_temporal_folded_susy/RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_DECLARED_GAMMA1_BOUNDARY_VARIATION_RESULT.json",
        "cpt_temporal_folded_susy/RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_RESULT.json",
    ]
    if [item["path"] for item in config["upstream_results"]] != expected_upstream_paths:
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
        "rawc.hybrid.guard.actual_direction_and_barrier",
        "DLMF Liouville--Green actual recessive solution plus the pinned rho invariant-region proof",
        "The selected actual family is normalized at Q=4 and has rho in [-1,1] with u>0 while x>=3.",
        "The full inherited rho box is reused at the rational switch. It outer-encloses the actual direction but neither substitutes a WKB proxy nor newly sharpens the Q=4-to-switch transport.",
    )
    audit.guard(
        "rawc.hybrid.guard.local_taylor_remainder",
        "Taylor theorem with whole-step derivative majorants",
        "Each exact-rational step uses full kappa/lambda boxes, actual derivative jets through order 12, a Gronwall state tube and D_13 |h|^13/13! remainder.",
        "This is a validated analytic local transfer, not a SciPy or black-box numerical ODE call.",
    )
    audit.guard(
        "rawc.hybrid.guard.scale_free_denominator",
        "Nonzero rescaling and quotient identity",
        "The barrier makes the actual switch amplitude positive; the propagated full outer box must exclude zero at Q0 before division.",
        "The resulting g has the same zeros as Gamma_1 only within the certified parameter boxes; no root continuation is inferred.",
    )
    audit.guard(
        "rawc.hybrid.guard.volterra_quotient_tail",
        "Rotating-frame variation of constants and Gronwall on Q<-4",
        "The potential and forcing masses are integrable and the Q0 scale-free state is finite with nonzero first component.",
        "The bound closes the complete selected-reference left tail only; it supplies no spectral measure or RAQ.",
    )
    audit.guard(
        "rawc.hybrid.guard.scope",
        "Worktop scope separation",
        "One inherited kappa bracket, two real lambda boxes, the full barrier-admissible switch box, one fixed extension reference and same-backend 80/120-digit refinements.",
        "Absolute Q4-normalized Gamma_1 sharpness, global zeros, spectrum, RAQ, quantum gravity, physics and TOE remain null.",
    )

    conventions = config["declared_conventions"]
    bracket = conventions["root_bracket"]
    bessel_result = upstream_payloads[expected_upstream_paths[1]]
    root_row = bessel_result["certified_calculation"]["endpoint_characteristic"][
        "root_rows"
    ][0]
    root_certificate = root_row["certified_high_precision_bracket"]
    precision_120 = next(
        item
        for item in root_row["precision_runs"]
        if item["decimal_digits"] == 120
    )
    bessel_root_linked = bool(
        root_row["root_index"] == 1
        and root_certificate["at_least_one_real_sign_changing_zero"] is True
        and root_certificate["left_exact"] == bracket["left_exact"]
        and root_certificate["right_exact"] == bracket["right_exact"]
        and root_certificate["width_exact"]
        == "1/20282409603651670423947251286016"
        and precision_120["left_exact"] == root_certificate["left_exact"]
        and precision_120["right_exact"] == root_certificate["right_exact"]
        and precision_120["signs"] == [-1, 1]
    )
    audit.inequality(
        "rawc.hybrid.upstream_bessel_root1_linkage",
        bessel_root_linked,
        "The configured root bracket is exactly the upstream root-1 120-digit sign-changing Bessel bracket, not merely a subinterval of (2,3).",
        root_index=root_row["root_index"],
        at_least_one_real_sign_changing_zero=root_certificate[
            "at_least_one_real_sign_changing_zero"
        ],
        left_exact=root_certificate["left_exact"],
        right_exact=root_certificate["right_exact"],
        signs=precision_120["signs"],
    )

    plus_result = upstream_payloads[expected_upstream_paths[0]]
    coarse_result = upstream_payloads[expected_upstream_paths[3]]
    coarse_conventions = coarse_result["declared_conventions"]
    coarse_scope = coarse_result["certified_calculation"]["parameter_scope"]
    coarse_guards = {
        item["id"]: item for item in coarse_result["theorem_guards"]
    }
    expected_coarse_normalization = (
        "For each fixed real (kappa,lambda), rescale the actual DLMF recessive "
        "solution so u_lambda(4)=A_lambda(4)^(-1/4)>0; this fixes amplitude and "
        "leaves its logarithmic derivative unchanged."
    )
    expected_riccati_frame = (
        "r=-u_Q/u and rho=r-x-1/2, used only on x>=3 where the barrier proves "
        "rho in [-1,1] and u>0"
    )
    coarse_linked = bool(
        plus_result["declared_conventions"]["Q_plus"]
        == coarse_conventions["Q_plus"]
        == conventions["Q_plus"]
        == "4"
        and coarse_conventions["Q_0"] == conventions["Q_0"] == "-4"
        and coarse_conventions["C"] == conventions["C"] == "6*pi^2"
        and coarse_conventions["x"] == "x=C*exp(Q)"
        and coarse_conventions["barrier_switch_x"] == "3"
        and coarse_conventions["root_bracket_index"] == 1
        and coarse_conventions["lambda_boxes"] == conventions["lambda_boxes"]
        and coarse_conventions["plus_normalization"]
        == expected_coarse_normalization
        and coarse_conventions["riccati_frame"] == expected_riccati_frame
        and coarse_scope["root_index"] == 1
        and coarse_scope["kappa_bracket"]["left_exact"]
        == bracket["left_exact"]
        and coarse_scope["kappa_bracket"]["right_exact"]
        == bracket["right_exact"]
        and coarse_guards["rawc.actual.guard.actual_recessive_normalization"][
            "verified"
        ]
        is True
        and coarse_guards["rawc.actual.guard.riccati_invariant_region"][
            "verified"
        ]
        is True
    )
    audit.inequality(
        "rawc.hybrid.upstream_actual_barrier_linkage",
        coarse_linked,
        "The compact outer transfer is bound to the upstream Q endpoints, root box, lambda boxes, actual-recessive normalization and x>=3 rho-barrier convention.",
        Q_plus=coarse_conventions["Q_plus"],
        Q_0=coarse_conventions["Q_0"],
        barrier_switch_x=coarse_conventions["barrier_switch_x"],
        root_index=coarse_scope["root_index"],
        actual_recessive_normalization_guard=coarse_guards[
            "rawc.actual.guard.actual_recessive_normalization"
        ]["verified"],
        riccati_invariant_region_guard=coarse_guards[
            "rawc.actual.guard.riccati_invariant_region"
        ]["verified"],
    )

    boundary_result = upstream_payloads[expected_upstream_paths[2]]
    boundary_conventions = boundary_result["declared_conventions"]
    audit.inequality(
        "rawc.hybrid.upstream_gamma_boundary_linkage",
        bool(
            boundary_conventions["Q_0"] == conventions["Q_0"] == "-4"
            and boundary_conventions["C"] == conventions["C"] == "6*pi^2"
            and boundary_conventions["exact_nonzero_lambda_identity"]
            == "Gamma_1,p(u_lambda)=u_lambda,Q(Q0)-lambda*integral_-infinity^Q0 a(Q)u_lambda(Q)c_p(Q)dQ"
        ),
        "The quotient-tail calculation uses the pinned nonzero-lambda Gamma_1 boundary identity at the same Q0 and C convention.",
        Q_0=boundary_conventions["Q_0"],
        identity=boundary_conventions["exact_nonzero_lambda_identity"],
    )
    kappa_left = exact_rational(bracket["left_exact"])
    kappa_right = exact_rational(bracket["right_exact"])
    audit.inequality(
        "rawc.hybrid.root1_exact_location",
        bool(fmpq(2) < kappa_left < kappa_right < fmpq(3)),
        "The full inherited root-1 exact bracket lies in (2,3).",
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
        raise AssertionError("lambda box label/order drift")

    digits = int(conventions["ball_output_digits"])
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
    for tier, dps in enumerate(
        conventions["precision_ladder_decimal_digits"], start=1
    ):
        ctx.dps = int(dps)
        kappa_band = bracket_band(kappa_left, kappa_right)
        for box in lambda_boxes:
            lambda_band = bracket_band(box["left"], box["right"])
            record, balls = propagate_box(
                audit,
                label=box["label"],
                tier=tier,
                dps=int(dps),
                kappa_band=kappa_band,
                lambda_band=lambda_band,
                config=config,
            )
            tier_records[box["label"]].append(record)
            tier_balls[box["label"]].append(balls)

        zero_record, zero_balls = propagate_box(
            audit,
            label="lambda_zero",
            tier=tier,
            dps=int(dps),
            kappa_band=kappa_band,
            lambda_band=arb(0),
            config=config,
        )
        x_zero = acb(6 * arb.pi() ** 2 * arb(-4).exp())
        order_ball = acb(0, kappa_band)
        k_zero = audit.bessel_k(x_zero, order_ball)
        k_minus = audit.bessel_k(x_zero, order_ball - 1)
        k_plus = audit.bessel_k(x_zero, order_ball + 1)
        kq_zero = -x_zero * (k_minus + k_plus) / 2
        bessel_ratio = kq_zero / k_zero
        regression_ok = bool(
            zero_record["status"] == "CERTIFIED_TIER"
            and k_zero.abs_lower() > 0
            and bessel_ratio.imag.lower() <= 0 <= bessel_ratio.imag.upper()
            and contains_interval(zero_balls["g"], bessel_ratio.real)
        )
        audit.ball_check(
            f"rawc.hybrid.lambda_zero.tier{tier}.bessel_regression",
            regression_ok,
            "The exact lambda-zero K_(i kappa) endpoint logarithmic derivative is contained by the scale-free local-Taylor enclosure on the full root bracket.",
            decimal_digits=int(dps),
            K_Q0=complex_record(k_zero, digits),
            exact_Bessel_endpoint_log_derivative=complex_record(
                bessel_ratio, digits
            ),
            Taylor_scale_free_Gamma1=interval_record(zero_balls["g"], digits),
        )
        zero_record["exact_Bessel_regression"] = {
            "status": "CONTAINED" if regression_ok else "NOT_CONTAINED",
            "K_Q0": complex_record(k_zero, digits),
            "endpoint_log_derivative": complex_record(bessel_ratio, digits),
        }
        tier_records["lambda_zero"].append(zero_record)
        tier_balls["lambda_zero"].append(zero_balls)

    intersections: dict[str, Any] = {}
    for label in ("negative", "positive", "lambda_zero"):
        overlap = intersection(tier_balls[label][0]["g"], tier_balls[label][1]["g"])
        overlap_ok = overlap is not None
        audit.ball_check(
            f"rawc.hybrid.{label}.precision_overlap",
            overlap_ok,
            "The same-backend 80/120-digit scale-free enclosures overlap; this is a refinement check, not independent validation.",
            tier1=interval_record(tier_balls[label][0]["g"], digits),
            tier2=interval_record(tier_balls[label][1]["g"], digits),
            intersection=interval_record(overlap, digits) if overlap else None,
        )
        intersections[label] = interval_record(overlap, digits) if overlap else None

    audit.inequality(
        "rawc.hybrid.lambda_zero.bessel_call_count",
        audit.bessel_evaluations == expected_caps()["ball_bessel_evaluations"],
        "Both lambda-zero precision tiers make exactly the declared three Bessel calls.",
        observed=audit.bessel_evaluations,
        expected=expected_caps()["ball_bessel_evaluations"],
    )
    exact_pass = all(item["passed"] for item in audit.exact)
    ball_pass = all(item["passed"] for item in audit.ball)
    all_pass = bool(exact_pass and ball_pass)
    verdict = (
        "CERTIFY_HYBRID_VALIDATED_BARRIER_ADMISSIBLE_OUTER_TRANSFER_SCALE_FREE_GAMMA1_BRACKET1_ONLY"
        if all_pass
        else "HYBRID_VALIDATED_TRANSFER_NOT_CERTIFIED"
    )
    programme_impact = (
        "RECORD_A_USABLE_SCALE_FREE_OUTER_ENDPOINT_ENCLOSURE_CONTAINING_THE_ACTUAL_FAMILY_WITHOUT_CLAIMING_SHARP_Q4_TO_SWITCH_TRANSPORT_ROOT_CONTINUATION_SPECTRUM_RAQ_OR_PHYSICS"
        if all_pass
        else "RETAIN_THE_COARSE_ANALYTIC_ENCLOSURE_AND_RECORD_THE_FIRST_FAILED_CERTIFICATION_GATE"
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
            "all_executable_checks_passed": all_pass,
        },
        "validated_calculation": {
            "parameter_tiers": tier_records,
            "precision_intersections": intersections,
            "interpretation": (
                "The output is a scale-free endpoint and complete selected-reference quotient-tail outer enclosure for every barrier-admissible switch state. It contains the selected actual family but does not newly sharpen its Q4-to-switch direction, make Q4-normalized absolute Gamma_1 narrow, or continue roots."
            ),
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "compact_q_segments_per_parameter_tier": 16,
            "compact_taylor_order": 12,
            "precision_tiers": 2,
            "nonzero_lambda_boxes": 2,
            "lambda_zero_controls": 2,
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
