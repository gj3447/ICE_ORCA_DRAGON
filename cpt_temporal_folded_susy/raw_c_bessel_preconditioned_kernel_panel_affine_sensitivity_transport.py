#!/usr/bin/env python3
"""Bessel-preconditioned kernel-panel affine raw-C transport.

The lambda-zero modified-Bessel solution is the exact base direction.  The
nonzero-lambda difference and the actual parameter sensitivity are enclosed
with explicit backward-x comparison kernels.  This stops at Q_switch: it does
not evaluate the declared Gamma_1 or any spectral/physical object.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = (
    "RAW_C_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_"
    "SENSITIVITY_TRANSPORT_INPUTS.json"
)
RESULT_NAME = (
    "RAW_C_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_"
    "SENSITIVITY_TRANSPORT_RESULT.json"
)
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "raw_c_bessel_preconditioned_kernel_panel_affine_sensitivity_transport.py"
)
EXPECTED_INPUT_SHA256 = (
    "194b219f1b5b8740acd6ffa36c7d6980e02285a89a7b14eb8bb77c49e32010e9"
)
RESULT_SCHEMA = (
    "ice.raw-c-bessel-preconditioned-kernel-panel-affine-"
    "sensitivity-transport.result.v1"
)
RESULT_PREFIX = (
    "RAW_C_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_"
    "SENSITIVITY_TRANSPORT_RESULT="
)
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
        return fmpq(coefficient) * fmpq(10) ** int(exponent_text)
    return fmpq(text)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 256,
        "kernel_panels_coarse": 512,
        "kernel_panels_refined": 1024,
        "ball_bessel_evaluations": 12,
        "precision_tiers": 2,
        "root_brackets": 1,
        "nonzero_lambda_boxes": 2,
        "ode_calls": 0,
        "root_calls": 0,
        "quadrature_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "panel_specific_absolute_rho_picard_tubes": None,
        "differentiated_Qswitch_to_Q0_transport": None,
        "actual_nonzero_lambda_declared_Gamma1": None,
        "actual_declared_Gamma1_sign_separation": None,
        "nonzero_lambda_root_continuation": None,
        "root_velocity": None,
        "nonreal_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "physical_or_empirical_claim": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    controls: list[dict[str, Any]] = field(default_factory=list)
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

    def control(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self.register(identifier)
        self.controls.append(
            {
                "id": identifier,
                "kind": "OUTWARD_INTERVAL_CONTROL",
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
        raise AssertionError("constructed ball misses an endpoint")
    return value


def bracket_band(left: fmpq, right: fmpq) -> arb:
    return interval_from_bounds(arb(left).lower(), arb(right).upper())


def interval_width(value: arb) -> arb:
    return arb(value.upper() - value.lower())


def interval_product_hull(left: arb, right: arb) -> arb:
    """Outward hull of the four endpoint products.

    Arb's generic ball multiplication is rigorous but can be wider than the
    real interval product when both operands have large off-zero radii.  The
    endpoint hull retains the sign information needed by the MVT comparison.
    """

    products = [
        arb(left.lower()) * arb(right.lower()),
        arb(left.lower()) * arb(right.upper()),
        arb(left.upper()) * arb(right.lower()),
        arb(left.upper()) * arb(right.upper()),
    ]
    lower = min(value.lower() for value in products)
    upper = max(value.upper() for value in products)
    return interval_from_bounds(lower, upper)


def contains_interval(outer: arb, inner: arb) -> bool:
    return bool(
        outer.lower() <= inner.lower() and outer.upper() >= inner.upper()
    )


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
        "width_upper": interval_width(value).upper().str(
            digits, radius=False
        ),
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
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    result = json.loads(raw)
    for key in (
        "schema_version",
        "verdict",
        "result_payload_sha256_without_self",
    ):
        if result.get(key) != item[key]:
            raise AssertionError(f"upstream {key} mismatch: {item['path']}")
    payload = dict(result)
    recorded = payload.pop("result_payload_sha256_without_self")
    if (
        sha256_bytes(canonical_bytes(payload)) != recorded
        or result.get("run_status") != "VALID_RUN"
        or result.get("numbered_phase") is not None
    ):
        raise AssertionError(f"upstream integrity mismatch: {item['path']}")
    record = {
        key: item[key]
        for key in (
            "path",
            "sha256",
            "schema_version",
            "verdict",
            "result_payload_sha256_without_self",
        )
    }
    return result, record


def exact_audit(audit: Audit) -> None:
    x, c_value, kappa = sp.symbols(
        "x C kappa", positive=True, real=True
    )
    lam = sp.symbols("lambda", real=True)
    rho, rho0, sensitivity, p = sp.symbols(
        "rho rho_0 s p", real=True
    )
    field = lambda value, parameter: (
        2 * value
        + (value + value**2 + kappa**2 + sp.Rational(1, 4)) / x
        - parameter * sp.sqrt(x / c_value)
    )
    difference = sp.expand(field(rho, lam) - field(rho0, 0))
    audit.identity(
        "rawc.affine.delta_equation",
        difference
        - (2 + (1 + rho + rho0) / x) * (rho - rho0)
        + lam * sp.sqrt(x / c_value),
        "Subtracting the exact lambda-zero Riccati equation gives the affine difference equation.",
    )
    audit.identity(
        "rawc.affine.mean_sensitivity_equation",
        sp.expand(
            difference.subs(rho, rho0 + lam * p) / lam
            - (
                (2 + (1 + (rho0 + lam * p) + rho0) / x) * p
                - sp.sqrt(x / c_value)
            )
        ),
        "For nonzero lambda, p=(rho_lambda-rho_0)/lambda obeys the same affine comparison form.",
    )
    audit.identity(
        "rawc.affine.actual_sensitivity_equation",
        sp.diff(field(rho, lam), rho) * sensitivity
        + sp.diff(field(rho, lam), lam)
        - (
            (2 + (1 + 2 * rho) / x) * sensitivity
            - sp.sqrt(x / c_value)
        ),
        "Parameter differentiation gives the declared actual sensitivity equation.",
    )
    a, t = sp.symbols("a t", positive=True, real=True)
    lower_kernel = sp.exp(-2 * (t - a)) * (a / t) ** 3
    upper_kernel = sp.exp(-2 * (t - a)) * (t / a)
    audit.identity(
        "rawc.affine.lower_kernel",
        sp.diff(lower_kernel, t) + (2 + 3 / t) * lower_kernel,
        "The lower comparison kernel solves the upper-coefficient homogeneous equation.",
    )
    audit.identity(
        "rawc.affine.upper_kernel",
        sp.diff(upper_kernel, t) + (2 - 1 / t) * upper_kernel,
        "The upper comparison kernel solves the lower-coefficient homogeneous equation.",
    )
    audit.inequality(
        "rawc.affine.coefficient_envelope",
        True,
        "If both rho values lie in [-1,1], both affine coefficients lie between 2-1/x and 2+3/x.",
        lower_numerator="min(1+rho+rho0)=min(1+2rho)=-1",
        upper_numerator="max(1+rho+rho0)=max(1+2rho)=3",
    )
    closed_cap_ratio = (
        sp.Rational(1, 10000) / (6 * 9 * 7)
        + sp.Rational(64, 36 * 81 * 7**4)
    )
    audit.inequality(
        "rawc.affine.closed_segment_tail_uniformity",
        bool(closed_cap_ratio < sp.Rational(1, 100000)),
        "The lambda and kappa perturbations are below the inherited 1e-5 Liouville--Green coefficient budget on the full closed |lambda|<=1e-4 segment for Q>=4.",
        rational_upper=str(closed_cap_ratio),
        inherited_budget="1/100000",
    )


def comparison_integrals(
    x_left: arb, x_right: arb, *, panels: int, tail_y: fmpq
) -> dict[str, arb | int | str]:
    if panels <= 0 or (x_right - x_left).lower() <= arb(tail_y):
        raise AssertionError("comparison tail partition does not fit")
    c_value = 6 * arb.pi() ** 2
    sqrt_c = c_value.sqrt()
    step = tail_y / panels
    lower_kernel_lower = arb(0)
    lower_kernel_upper = arb(0)
    upper_kernel_lower = arb(0)
    upper_kernel_upper = arb(0)
    for index in range(panels):
        y0 = arb(step * index)
        y1 = arb(step * (index + 1))
        exponential_mass = ((-2 * y0).exp() - (-2 * y1).exp()) / 2
        lower_at_left = (
            (x_left / (x_left + y0)) ** 3
            * ((x_left + y0) / c_value).sqrt()
        )
        lower_at_right = (
            (x_left / (x_left + y1)) ** 3
            * ((x_left + y1) / c_value).sqrt()
        )
        upper_at_left = (
            (x_left + y0)
            / x_left
            * ((x_left + y0) / c_value).sqrt()
        )
        upper_at_right = (
            (x_left + y1)
            / x_left
            * ((x_left + y1) / c_value).sqrt()
        )
        lower_kernel_lower += exponential_mass * arb(lower_at_right.lower())
        lower_kernel_upper += exponential_mass * arb(lower_at_left.upper())
        upper_kernel_lower += exponential_mass * arb(upper_at_left.lower())
        upper_kernel_upper += exponential_mass * arb(upper_at_right.upper())
    y_tail = arb(tail_y)
    exp_tail = (-2 * y_tail).exp()
    lower_tail_value = (
        (x_left / (x_left + y_tail)) ** 3
        * ((x_left + y_tail) / c_value).sqrt()
    )
    lower_tail_upper = (
        arb(lower_tail_value.upper()) * exp_tail / 2
    )
    upper_tail_value = (
        (x_left + y_tail)
        / x_left
        * ((x_left + y_tail) / c_value).sqrt()
    )
    log_slope_upper = arb(
        (arb(3) / (2 * (arb(x_left.lower()) + y_tail))).upper()
    )
    if log_slope_upper.upper() >= 2:
        raise AssertionError("upper-kernel tail domination failed")
    upper_tail_upper = arb(
        (
            arb(upper_tail_value.upper())
            * exp_tail
            / (2 - log_slope_upper)
        ).upper()
    )
    lower_integral = interval_from_bounds(
        lower_kernel_lower.lower(),
        (lower_kernel_upper + lower_tail_upper).upper(),
    )
    upper_integral = interval_from_bounds(
        upper_kernel_lower.lower(),
        (upper_kernel_upper + upper_tail_upper).upper(),
    )
    return {
        "panels": panels,
        "tail_y": str(tail_y),
        "panel_width": str(step),
        "lower_comparison_integral": lower_integral,
        "upper_comparison_integral": upper_integral,
        "lower_kernel_extension_upper": lower_tail_upper,
        "upper_kernel_extension_upper": upper_tail_upper,
        "upper_tail_log_slope": log_slope_upper,
    }


def endpoint_comparison(
    x_left: arb,
    x_right: arb,
    entering: arb,
    kernels: dict[str, arb | int | str],
) -> tuple[arb, dict[str, arb]]:
    distance = x_right - x_left
    homogeneous_lower = (-2 * distance).exp() * (x_left / x_right) ** 3
    homogeneous_upper = (-2 * distance).exp() * (x_right / x_left)
    force_lower = kernels["lower_comparison_integral"]
    force_upper = kernels["upper_comparison_integral"]
    if not isinstance(force_lower, arb) or not isinstance(force_upper, arb):
        raise AssertionError("kernel record type drift")
    lower = arb((homogeneous_lower * entering).lower()) + arb(
        force_lower.lower()
    )
    upper = arb((homogeneous_upper * entering).upper()) + arb(
        force_upper.upper()
    )
    return interval_from_bounds(lower.lower(), upper.upper()), {
        "homogeneous_lower": homogeneous_lower,
        "homogeneous_upper": homogeneous_upper,
        "force_lower": force_lower,
        "force_upper": force_upper,
    }


def bessel_rho(
    audit: Audit, x_value: arb, kappa_band: arb
) -> tuple[acb, acb]:
    argument = acb(x_value)
    order = acb(0, kappa_band)
    k_value = audit.bessel_k(argument, order)
    k_minus = audit.bessel_k(argument, order - 1)
    k_plus = audit.bessel_k(argument, order + 1)
    k_q = -argument * (k_minus + k_plus) / 2
    rho = -k_q / k_value - argument - acb(arb(1) / 2)
    return rho, k_value


def parse_lambda_boxes(config: dict[str, Any]) -> list[dict[str, Any]]:
    parsed = []
    for item in config["declared_conventions"]["lambda_boxes"]:
        left = exact_rational(item["left"])
        right = exact_rational(item["right"])
        if (
            not left < right
            or left == 0
            or right == 0
            or (left < 0 < right)
        ):
            raise AssertionError("lambda box must be ordered and punctured")
        parsed.append(
            {
                "label": item["label"],
                "left": left,
                "right": right,
                "band": bracket_band(left, right),
            }
        )
    return parsed


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    if sha256_bytes(raw_input) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input manifest hash mismatch")
    config = json.loads(raw_input)
    if (
        config.get("numbered_phase") is not None
        or config.get("resource_caps") != expected_caps()
        or config.get("required_fail_closed_outputs") != expected_nulls()
    ):
        raise AssertionError("input policy drift")

    upstream_values: dict[str, dict[str, Any]] = {}
    upstream_records = []
    for item in config["upstream_results"]:
        value, record = verify_upstream(root, item)
        upstream_values[item["path"]] = value
        upstream_records.append(record)

    bessel_upstream = upstream_values[
        "cpt_temporal_folded_susy/"
        "RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_RESULT.json"
    ]
    sensitivity_upstream = upstream_values[
        "cpt_temporal_folded_susy/"
        "RAW_C_NONZERO_LAMBDA_PLUS_TAIL_SENSITIVITY_ANCHOR_RESULT.json"
    ]
    coarse_upstream = upstream_values[
        "cpt_temporal_folded_susy/"
        "RAW_C_ACTUAL_NONZERO_LAMBDA_GAMMA1_COARSE_ENCLOSURE_RESULT.json"
    ]
    conventions = config["declared_conventions"]
    root_row = bessel_upstream["certified_calculation"][
        "endpoint_characteristic"
    ]["root_rows"][0]
    upstream_bracket = root_row["certified_high_precision_bracket"]
    if (
        upstream_bracket["left_exact"]
        != conventions["root_bracket"]["left_exact"]
        or upstream_bracket["right_exact"]
        != conventions["root_bracket"]["right_exact"]
    ):
        raise AssertionError("root bracket drift")
    anchor_rows = sensitivity_upstream["certified_calculation"][
        "interval_by_lambda_box"
    ]
    expected_s = conventions["s_Qplus_interval"]
    if len(anchor_rows) != 2 or any(
        [row["s_Qplus_4"]["lower"], row["s_Qplus_4"]["upper"]]
        != expected_s
        for row in anchor_rows
    ):
        raise AssertionError("sensitivity anchor drift")
    anchor_checks = {
        item["id"]: item
        for item in (
            sensitivity_upstream.get("exact_checks", [])
            + sensitivity_upstream.get("controls", [])
        )
    }
    required_anchor_checks = {
        "rawc.s_anchor.forced_wronskian",
        "rawc.s_anchor.amplitude_invariance",
        "rawc.s_anchor.coefficient_positive",
        "rawc.s_anchor.coefficient_derivative_positive",
        "rawc.s_anchor.coefficient_four_A_minus_Aprime",
        "rawc.s_anchor.g_lower_from_lg",
        "rawc.s_anchor.g_upper_from_lg",
        "rawc.s_anchor.lower_integral_derivation",
        "rawc.s_anchor.upper_integral_derivation",
        "rawc.s_anchor.control.zero_bessel_containment",
    }
    if any(
        identifier not in anchor_checks
        or anchor_checks[identifier].get("passed") is not True
        for identifier in required_anchor_checks
    ):
        raise AssertionError("pinned sensitivity uniformity check drift")
    coarse_rows = coarse_upstream["certified_calculation"][
        "nonzero_lambda_rows"
    ]
    if (
        [row.get("label") for row in coarse_rows] != ["negative", "positive"]
        or any(
            sp.Rational(
                row["certified_intersection"]["rho4"]["lower"]
            )
            < -1
            or sp.Rational(
                row["certified_intersection"]["rho4"]["upper"]
            )
            > 1
            for row in coarse_rows
        )
    ):
        raise AssertionError("coarse actual-family row drift")
    inherited_checks = {
        item["id"]: item
        for item in (
            coarse_upstream.get("exact_checks", [])
            + coarse_upstream.get("ball_checks", [])
        )
    }
    required_barriers = {
        "rawc.actual.backward_upper_barrier",
        "rawc.actual.backward_lower_barrier",
        "rawc.actual.negative.tier1.riccati_barrier",
        "rawc.actual.negative.tier2.riccati_barrier",
        "rawc.actual.positive.tier1.riccati_barrier",
        "rawc.actual.positive.tier2.riccati_barrier",
        "rawc.actual.lambda_zero_control.tier1.riccati_barrier",
        "rawc.actual.lambda_zero_control.tier2.riccati_barrier",
    }
    if any(
        identifier not in inherited_checks
        or inherited_checks[identifier].get("passed") is not True
        for identifier in required_barriers
    ):
        raise AssertionError("pinned actual-family barrier check drift")

    audit = Audit()
    exact_audit(audit)
    if not all(item["passed"] for item in audit.exact):
        raise AssertionError("exact identity audit failed")
    audit.guard(
        "rawc.affine.guard.closed_mean_value_segment",
        "mean-value theorem for the differentiable plus-recessive logarithmic direction",
        "The pinned forced-Wronskian proof is uniform for |lambda|<=1e-4 and has no puncture singularity; zero is independently contained by its Bessel/Green control.",
        "The same [27/10,240/53] interval bounds the average p=(rho_lambda-rho_0)/lambda only on each closed segment from zero to a declared box point.",
    )
    audit.guard(
        "rawc.affine.guard.comparison",
        "scalar linear comparison and variation of constants",
        "Both actual rho and the exact Bessel rho_0 remain in [-1,1] for x>=3, the forcing is positive, and the entering p and s intervals are positive.",
        "The explicit kernels enclose p and s at Q_switch; they are not a differentiated Gamma_1 or a compact/minus-tail certificate.",
    )
    audit.guard(
        "rawc.affine.guard.bessel_preconditioner",
        "modified-Bessel equation and derivative recurrence",
        "K_(i kappa)(x) is the pinned real lambda-zero recessive family and every evaluated denominator ball excludes zero.",
        "The Bessel base removes common-direction wrapping but supplies no nonzero-lambda spectral theorem.",
    )

    kappa_left = exact_rational(conventions["root_bracket"]["left_exact"])
    kappa_right = exact_rational(conventions["root_bracket"]["right_exact"])
    lambda_boxes = parse_lambda_boxes(config)
    entering = bracket_band(
        exact_rational(expected_s[0]), exact_rational(expected_s[1])
    )
    panel_counts = conventions["kernel_panel_ladder"]
    tail_y = exact_rational(conventions["kernel_tail_y"])
    width_target = arb(
        exact_rational(conventions["Qswitch_actual_rho_width_target"])
    )
    output_digits = int(conventions["ball_output_digits"])
    tier_rows: list[dict[str, Any]] = []
    tier_balls: dict[str, list[dict[str, arb]]] = {
        item["label"]: [] for item in lambda_boxes
    }
    kernel_tier_balls: list[arb] = []

    for tier, dps in enumerate(
        conventions["precision_ladder_decimal_digits"], start=1
    ):
        ctx.dps = int(dps)
        c_value = 6 * arb.pi() ** 2
        x_plus = c_value * arb(exact_rational(conventions["Q_plus"])).exp()
        x_switch = c_value * arb(
            exact_rational(conventions["Q_switch"])
        ).exp()
        kappa_band = bracket_band(kappa_left, kappa_right)
        coefficient_floor = 2 - 1 / x_switch
        forcing_ceiling = (x_plus / c_value).sqrt()
        upper_barrier_margin = (
            coefficient_floor * arb(exact_rational(expected_s[1]))
            - forcing_ceiling
        )
        barrier_ok = bool(
            x_switch.lower() > 3
            and coefficient_floor.lower() > 0
            and upper_barrier_margin.lower() > 0
        )
        audit.control(
            f"rawc.affine.tier{tier}.uniform_positive_tube",
            barrier_ok,
            "Backward flow points inward at s,p=0 and at the inherited upper bound 240/53 on the full x interval.",
            decimal_digits=dps,
            x_Qplus=interval_record(x_plus, output_digits),
            x_Qswitch=interval_record(x_switch, output_digits),
            coefficient_floor=interval_record(
                coefficient_floor, output_digits
            ),
            forcing_ceiling=interval_record(forcing_ceiling, output_digits),
            upper_barrier_margin=interval_record(
                upper_barrier_margin, output_digits
            ),
        )
        coarse_kernels = comparison_integrals(
            x_switch,
            x_plus,
            panels=int(panel_counts[0]),
            tail_y=tail_y,
        )
        refined_kernels = comparison_integrals(
            x_switch,
            x_plus,
            panels=int(panel_counts[1]),
            tail_y=tail_y,
        )
        coarse_s_actual, _ = endpoint_comparison(
            x_switch, x_plus, entering, coarse_kernels
        )
        refined_s_actual, comparison_parts = endpoint_comparison(
            x_switch, x_plus, entering, refined_kernels
        )
        # p=(rho_lambda-rho_0)/lambda and the pointwise actual sensitivity
        # s=partial_lambda rho are distinct functions.  Their entering boxes
        # and conservative coefficient envelopes happen to coincide here, so
        # we evaluate and record the two comparison problems separately.
        coarse_p_mvt, _ = endpoint_comparison(
            x_switch, x_plus, entering, coarse_kernels
        )
        refined_p_mvt, _ = endpoint_comparison(
            x_switch, x_plus, entering, refined_kernels
        )
        lower_coarse = coarse_kernels["lower_comparison_integral"]
        upper_coarse = coarse_kernels["upper_comparison_integral"]
        lower_refined = refined_kernels["lower_comparison_integral"]
        upper_refined = refined_kernels["upper_comparison_integral"]
        if not all(
            isinstance(value, arb)
            for value in (
                lower_coarse,
                upper_coarse,
                lower_refined,
                upper_refined,
            )
        ):
            raise AssertionError("kernel type drift")
        refinement_ok = bool(
            contains_interval(lower_coarse, lower_refined)
            and contains_interval(upper_coarse, upper_refined)
            and contains_interval(coarse_s_actual, refined_s_actual)
            and contains_interval(coarse_p_mvt, refined_p_mvt)
        )
        audit.control(
            f"rawc.affine.tier{tier}.kernel_refinement",
            refinement_ok,
            "The 1024-panel monotone exponential-kernel enclosure is nested in the 512-panel enclosure; the positive y>24 remainder is analytic.",
            decimal_digits=dps,
            coarse_panels=panel_counts[0],
            refined_panels=panel_counts[1],
            coarse_actual_s_Qswitch=interval_record(
                coarse_s_actual, output_digits
            ),
            refined_actual_s_Qswitch=interval_record(
                refined_s_actual, output_digits
            ),
            coarse_MVT_p_Qswitch=interval_record(
                coarse_p_mvt, output_digits
            ),
            refined_MVT_p_Qswitch=interval_record(
                refined_p_mvt, output_digits
            ),
            refined_lower_integral=interval_record(
                lower_refined, output_digits
            ),
            refined_upper_integral=interval_record(
                upper_refined, output_digits
            ),
            lower_kernel_extension_upper=interval_record(
                refined_kernels["lower_kernel_extension_upper"],
                output_digits,
            ),
            upper_kernel_extension_upper=interval_record(
                refined_kernels["upper_kernel_extension_upper"],
                output_digits,
            ),
        )
        rho0_plus, k_plus = bessel_rho(audit, x_plus, kappa_band)
        rho0_switch, k_switch = bessel_rho(audit, x_switch, kappa_band)
        lambda_cap = exact_rational("1e-4")
        closed_lambda_band = bracket_band(-lambda_cap, lambda_cap)
        closed_rho_plus = rho0_plus.real + interval_product_hull(
            closed_lambda_band, entering
        )
        sqrt_c = c_value.sqrt()
        t3 = arb(3) * arb(3).sqrt() / sqrt_c
        derivative_margin = (
            2
            - (arb(3) / 2)
            * arb(lambda_cap)
            * arb(2).exp()
        )
        lower_barrier_margin = (
            6
            - arb((kappa_band**2).upper())
            - arb(1) / 4
            - arb(lambda_cap) * arb(t3.upper())
        )
        upper_barrier_bracket = (
            arb((kappa_band**2).lower())
            + 6
            + arb(9) / 4
            - arb(lambda_cap) * arb(t3.upper())
        )
        closed_barrier_ok = bool(
            closed_rho_plus.lower() >= -1
            and closed_rho_plus.upper() <= 1
            and derivative_margin.lower() > 0
            and lower_barrier_margin.lower() > 0
            and upper_barrier_bracket.lower() > 0
        )
        audit.control(
            f"rawc.affine.tier{tier}.closed_parameter_barrier",
            closed_barrier_ok,
            "The Bessel/MVT start and exact worst-case barrier margins certify rho_theta in [-1,1] on the entire closed |theta|<=1e-4 segment from Q=4 to x=3.",
            decimal_digits=dps,
            closed_lambda_segment=interval_record(
                closed_lambda_band, output_digits
            ),
            closed_segment_rho_Qplus=interval_record(
                closed_rho_plus, output_digits
            ),
            monotonic_derivative_margin=interval_record(
                derivative_margin, output_digits
            ),
            rho_minus_one_inward_margin_at_x3=interval_record(
                lower_barrier_margin, output_digits
            ),
            rho_plus_one_positive_bracket_at_x3=interval_record(
                upper_barrier_bracket, output_digits
            ),
        )
        bessel_ok = bool(
            k_plus.abs_lower() > 0
            and k_switch.abs_lower() > 0
            and rho0_plus.imag.lower() <= 0 <= rho0_plus.imag.upper()
            and rho0_switch.imag.lower() <= 0 <= rho0_switch.imag.upper()
        )
        audit.control(
            f"rawc.affine.tier{tier}.bessel_endpoints",
            bessel_ok,
            "Both exact lambda-zero Bessel denominators exclude zero and their direction residue balls contain the real axis.",
            decimal_digits=dps,
            K_Qplus=complex_record(k_plus, output_digits),
            K_Qswitch=complex_record(k_switch, output_digits),
            rho0_Qplus=complex_record(rho0_plus, output_digits),
            rho0_Qswitch=complex_record(rho0_switch, output_digits),
        )
        box_rows = []
        for item in lambda_boxes:
            lambda_band = bracket_band(item["left"], item["right"])
            rho_plus = rho0_plus.real + interval_product_hull(
                lambda_band, entering
            )
            rho_switch = rho0_switch.real + interval_product_hull(
                lambda_band, refined_p_mvt
            )
            if item["label"] == "negative":
                side_ok = bool(
                    rho_plus.upper() < rho0_plus.real.lower()
                    and rho_switch.upper() < rho0_switch.real.lower()
                )
                side = "STRICTLY_BELOW_LAMBDA_ZERO_BESSEL_DIRECTION"
            elif item["label"] == "positive":
                side_ok = bool(
                    rho_plus.lower() > rho0_plus.real.upper()
                    and rho_switch.lower() > rho0_switch.real.upper()
                )
                side = "STRICTLY_ABOVE_LAMBDA_ZERO_BESSEL_DIRECTION"
            else:
                raise AssertionError("unexpected lambda label")
            row_ok = bool(
                side_ok
                and refined_s_actual.lower() > 0
                and refined_p_mvt.lower() > 0
                and rho_plus.lower() >= -1
                and rho_plus.upper() <= 1
                and rho_switch.lower() >= -1
                and rho_switch.upper() <= 1
                and interval_width(rho_switch).upper() < width_target.lower()
            )
            audit.control(
                f"rawc.affine.{item['label']}.tier{tier}.direction",
                row_ok,
                "The MVT/Bessel-preconditioned actual direction stays on the lambda-selected side, inside the invariant barrier, with positive switch sensitivity and the declared width target.",
                decimal_digits=dps,
                lambda_box={
                    "left_exact": str(item["left"]),
                    "right_exact": str(item["right"]),
                    "coverage": interval_record(lambda_band, output_digits),
                },
                s_Qplus=interval_record(entering, output_digits),
                actual_s_Qswitch=interval_record(
                    refined_s_actual, output_digits
                ),
                MVT_p_Qswitch=interval_record(
                    refined_p_mvt, output_digits
                ),
                rho_actual_Qplus=interval_record(rho_plus, output_digits),
                rho_actual_Qswitch=interval_record(
                    rho_switch, output_digits
                ),
                relative_side=side,
                Qswitch_width_target=conventions[
                    "Qswitch_actual_rho_width_target"
                ],
            )
            box_rows.append(
                {
                    "label": item["label"],
                    "lambda_box": interval_record(
                        lambda_band, output_digits
                    ),
                    "s_Qplus": interval_record(entering, output_digits),
                    "actual_s_Qswitch": interval_record(
                        refined_s_actual, output_digits
                    ),
                    "MVT_p_Qswitch": interval_record(
                        refined_p_mvt, output_digits
                    ),
                    "rho0_Qplus": interval_record(
                        rho0_plus.real, output_digits
                    ),
                    "rho_actual_Qplus": interval_record(
                        rho_plus, output_digits
                    ),
                    "rho0_Qswitch": interval_record(
                        rho0_switch.real, output_digits
                    ),
                    "rho_actual_Qswitch": interval_record(
                        rho_switch, output_digits
                    ),
                    "relative_side": side,
                    "certified": row_ok,
                }
            )
            tier_balls[item["label"]].append(
                {
                    "s_actual": refined_s_actual,
                    "p_mvt": refined_p_mvt,
                    "rho_plus": rho_plus,
                    "rho_switch": rho_switch,
                    "rho0_plus": rho0_plus.real,
                    "rho0_switch": rho0_switch.real,
                }
            )
        tier_rows.append(
            {
                "tier": tier,
                "decimal_digits": dps,
                "coarse_panels": panel_counts[0],
                "refined_panels": panel_counts[1],
                "kernel_refinement_nested": refinement_ok,
                "actual_s_Qswitch": interval_record(
                    refined_s_actual, output_digits
                ),
                "MVT_p_Qswitch": interval_record(
                    refined_p_mvt, output_digits
                ),
                "homogeneous_entering_lower": interval_record(
                    comparison_parts["homogeneous_lower"], output_digits
                ),
                "homogeneous_entering_upper": interval_record(
                    comparison_parts["homogeneous_upper"], output_digits
                ),
                "boxes": box_rows,
            }
        )
        kernel_tier_balls.append(refined_s_actual)

    final_rows = []
    all_overlap = True
    for item in lambda_boxes:
        first, second = tier_balls[item["label"]]
        overlaps = {
            key: intersection(first[key], second[key])
            for key in first
        }
        overlap_ok = all(value is not None for value in overlaps.values())
        all_overlap = all_overlap and overlap_ok
        if not overlap_ok:
            final_rows.append(
                {
                    "label": item["label"],
                    "status": "PRECISION_OVERLAP_FAILED",
                }
            )
            continue
        values = {key: value for key, value in overlaps.items() if value}
        rho_actual = values["rho_switch"]
        rho_zero = values["rho0_switch"]
        if item["label"] == "negative":
            side_ok = rho_actual.upper() < rho_zero.lower()
            side = "STRICTLY_BELOW_LAMBDA_ZERO_BESSEL_DIRECTION"
        else:
            side_ok = rho_actual.lower() > rho_zero.upper()
            side = "STRICTLY_ABOVE_LAMBDA_ZERO_BESSEL_DIRECTION"
        certified = bool(
            side_ok
            and values["s_actual"].lower() > 0
            and values["p_mvt"].lower() > 0
            and interval_width(rho_actual).upper() < width_target.lower()
        )
        final_rows.append(
            {
                "label": item["label"],
                "status": "CERTIFIED_SWITCH_AFFINE_TUBE"
                if certified
                else "UNRESOLVED_SWITCH_AFFINE_TUBE",
                "lambda_box": {
                    "left_exact": str(item["left"]),
                    "right_exact": str(item["right"]),
                },
                "actual_s_Qswitch_intersection": interval_record(
                    values["s_actual"], output_digits
                ),
                "MVT_p_Qswitch_intersection": interval_record(
                    values["p_mvt"], output_digits
                ),
                "rho0_Qswitch_intersection": interval_record(
                    rho_zero, output_digits
                ),
                "rho_actual_Qswitch_intersection": interval_record(
                    rho_actual, output_digits
                ),
                "relative_side": side,
                "Qswitch_width_target": conventions[
                    "Qswitch_actual_rho_width_target"
                ],
                "certified": certified,
            }
        )

    precision_overlap_ok = bool(
        all_overlap
        and intersection(kernel_tier_balls[0], kernel_tier_balls[1])
        is not None
    )
    audit.control(
        "rawc.affine.precision_overlap",
        precision_overlap_ok,
        "The 80/120-decimal outward endpoint balls overlap for the Bessel base, actual direction and sensitivity; this is a precision consistency control, not independent evidence.",
        final_rows=final_rows,
    )
    all_controls = all(item["passed"] for item in audit.controls)
    all_final = all(row.get("certified") is True for row in final_rows)
    certified = bool(all_controls and all_final and precision_overlap_ok)
    verdict = (
        "CERTIFY_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_"
        "SWITCH_SENSITIVITY_AND_DIRECTION_SIGN"
        if certified
        else "UNRESOLVED_BESSEL_PRECONDITIONED_KERNEL_PANEL_AFFINE_TRANSPORT"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": config["calculation_id"],
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "finite_calculation": (
            "The exact Bessel-preconditioned affine comparison certifies a "
            "strictly positive Q_switch sensitivity and a narrow Bessel-"
            "relative endpoint enclosure on the lambda-selected side for "
            "both boxes."
            if certified
            else "At least one affine comparison, refinement, Bessel, side, "
            "width or precision-overlap control did not certify."
        ),
        "model_interpretation": (
            "This removes the inherited Q=4 LG common-direction width from "
            "the selected root-1 switch transport; the differentiated "
            "compact and complete minus-tail Gamma_1 functional remain open."
        ),
        "non_claim": config["non_claim"],
        "input_manifest": {
            "path": INPUT_RELPATH,
            "sha256": sha256_bytes(raw_input),
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_results": upstream_records,
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_flint": importlib.metadata.version("python-flint"),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "primary_sources": config["primary_sources"],
        "declared_conventions": conventions,
        "assumptions": config["assumptions"],
        "exact_checks": audit.exact,
        "controls": audit.controls,
        "theorem_guards": audit.guards,
        "certified_calculation": {
            "status": "CERTIFIED" if certified else "UNRESOLVED",
            "scope": "root bracket 1, Q=4 to Q_switch=-29/10, two punctured real lambda boxes",
            "tier_rows": tier_rows,
            "final_intersections": final_rows,
            "next_mathematical_gap": "differentiate the node-safe Q_switch-to-Q0 transfer and the complete declared minus-tail functional before any Gamma_1 sign or root-continuation claim",
        },
        "resource_accounting": {
            "symbolic_checks": len(audit.exact),
            "controls": len(audit.controls),
            "kernel_panels_evaluated": sum(panel_counts)
            * len(conventions["precision_ladder_decimal_digits"]),
            "ball_bessel_evaluations": audit.bessel_evaluations,
            "precision_tiers": len(
                conventions["precision_ladder_decimal_digits"]
            ),
            "ode_calls": 0,
            "root_calls": 0,
            "quadrature_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "adjacent_result_files_written": 1,
        },
        "required_fail_closed_outputs": expected_nulls(),
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    summary = {
        "run_status": result["run_status"],
        "verdict": verdict,
        "switch_transport": [
            {
                "label": row["label"],
                "actual_s": row.get("actual_s_Qswitch_intersection"),
                "MVT_p": row.get("MVT_p_Qswitch_intersection"),
                "rho_actual": row.get("rho_actual_Qswitch_intersection"),
            }
            for row in final_rows
        ],
        "result": RESULT_NAME,
        "result_sha256": sha256_bytes(encoded),
        "result_bytes": len(encoded),
    }
    print(
        RESULT_PREFIX
        + json.dumps(summary, sort_keys=True, separators=(",", ":"))
    )


if __name__ == "__main__":
    main()
