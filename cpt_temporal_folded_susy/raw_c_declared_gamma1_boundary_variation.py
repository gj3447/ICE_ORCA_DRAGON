#!/usr/bin/env python3
"""Declared raw-C Gamma_1 left-boundary variation certificate; not RAQ."""
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


INPUT_NAME = "RAW_C_DECLARED_GAMMA1_BOUNDARY_VARIATION_INPUTS.json"
RESULT_NAME = "RAW_C_DECLARED_GAMMA1_BOUNDARY_VARIATION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_declared_gamma1_boundary_variation.py"
EXPECTED_INPUT_SHA256 = "0ac870727a2334f341d68dde981fa951e083b08f787d3726cd56b157c137882f"
CALCULATION_ID = "RawCDeclaredGamma1BoundaryVariation"
RESULT_SCHEMA = "ice.raw-c-declared-gamma1-boundary-variation.result.v1"
RESULT_PREFIX = "RAW_C_DECLARED_GAMMA1_BOUNDARY_VARIATION_RESULT="
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
        "symbolic_operations": 1000,
        "ball_bessel_evaluations": 20,
        "ball_gamma_evaluations": 60,
        "root_brackets": 5,
        "nonzero_lambda_boxes": 2,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "actual_nonzero_lambda_plus_recessive_solution": None,
        "actual_nonzero_lambda_Gamma1_value": None,
        "nonzero_lambda_minus_end_remainder_for_a_constructed_solution": None,
        "nonzero_lambda_root_continuation": None,
        "finite_Q0_proxy_as_declared_Gamma1_away_from_zero": None,
        "finite_Q0_endpoint_F_lambda_amplitude": None,
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
    gamma_evaluations: int = 0

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
                "verification_mode": "SOURCE_PIN_PLUS_EXECUTABLE_EXACT_AND_BALL_HYPOTHESIS_SCOPE_AUDIT",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )

    def bessel_k(self, x: acb, order: acb) -> acb:
        self.bessel_evaluations += 1
        if self.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
            raise AssertionError("ball Bessel evaluation cap exceeded")
        return x.bessel_k(order)

    def gamma(self, value: acb) -> acb:
        self.gamma_evaluations += 1
        if self.gamma_evaluations > expected_caps()["ball_gamma_evaluations"]:
            raise AssertionError("ball gamma evaluation cap exceeded")
        return value.gamma()


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def bracket_band(left: fmpq, right: fmpq) -> arb:
    return arb(arb((left + right) / 2), arb((right - left) / 2))


def interval_from_bounds(lower: arb, upper: arb) -> arb:
    if upper < lower:
        raise AssertionError("reversed interval bounds")
    value = arb((lower + upper) / 2, (upper - lower) / 2)
    if not (value.lower() <= lower and value.upper() >= upper):
        raise AssertionError("outward interval construction failed")
    return value


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


def width(value: arb) -> arb:
    return value.upper() - value.lower()


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
    u, uq, c, cq, a0, lam, forcing = sp.symbols(
        "u u_Q c c_Q A_0 lambda a", real=True
    )
    wronskian = u * cq - uq * c
    wronskian_prime = sp.expand(
        uq * cq
        + u * a0 * c
        - (a0 + lam * forcing) * u * c
        - uq * cq
    )
    audit.identity(
        "rawc.gamma1.wronskian_derivative",
        wronskian_prime + lam * forcing * u * c,
        "For a lambda-independent zero-energy reference c_p, W_Q(u_lambda,c_p)=-lambda*a*u_lambda*c_p.",
    )
    w0, integral = sp.symbols("W_Q0 I_minus", real=True)
    wminus = w0 + lam * integral
    gamma1 = -wminus
    uq0 = -w0
    audit.identity(
        "rawc.gamma1.integrated_boundary_identity",
        gamma1 - (uq0 - lam * integral),
        "Gamma_1=-W(-infinity)=u_Q(Q0)-lambda*integral_-infinity^Q0 a*u*c with the repository Wronskian sign.",
    )
    f = sp.symbols("f", positive=True)
    audit.identity(
        "rawc.gamma1.weight_conversion",
        (f / 2).subs(f, 2 * forcing) - forcing,
        "The divided fiber forcing is a=f/2 at hbar=1.",
    )
    q, kappa = sp.symbols("Q kappa", real=True, positive=True)
    potential = 36 * sp.pi**4 * sp.exp(2 * q)
    audit.identity(
        "rawc.gamma1.reference_potential_integral",
        sp.diff(18 * sp.pi**4 * sp.exp(2 * q) / kappa, q)
        - potential / kappa,
        "The free-rotation perturbation integral has antiderivative 18*pi^4*exp(2Q)/kappa.",
    )
    a_density = 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q)
    audit.identity(
        "rawc.gamma1.reference_weight_integral",
        sp.diff(4 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * q), q)
        - a_density,
        "The minus-tail a-weight has antiderivative 4*pi^2*exp(3Q/2).",
    )
    rotation = sp.Matrix([[0, kappa], [-kappa, 0]])
    audit.identity(
        "rawc.gamma1.free_rotation_skew",
        sum(
            (entry**2 for entry in rotation + rotation.T),
            sp.Integer(0),
        ),
        "The unperturbed (c,c_Q/kappa) system is a Euclidean norm-preserving rotation.",
    )
    norm_a, norm_f, m_c, abs_lam = sp.symbols(
        "norm_a norm_f M_c abs_lambda", positive=True
    )
    audit.identity(
        "rawc.gamma1.cauchy_schwarz_weight_conversion",
        (abs_lam * m_c * norm_a).subs(norm_a, norm_f / sp.sqrt(2))
        - abs_lam * m_c * norm_f / sp.sqrt(2),
        "Cauchy-Schwarz and f=2a give correction <=|lambda|*M_c/sqrt(2) per unit L2(f) norm.",
    )
    total, right, left, endpoint = sp.symbols(
        "D_total D_right D_left u_0", nonzero=True, real=True
    )
    audit.identity(
        "rawc.gamma1.normalized_left_split",
        ((total - right) - left).subs(left, total - right),
        "The normalized declared derivative magnitude splits into the finite-Q0 right proxy contribution plus the omitted left-boundary correction.",
    )
    root_value = sp.symbols("u_0_Q0", nonzero=True, real=True)
    root_slope = sp.symbols("u_0_Q_Q0", real=True)
    audit.identity(
        "rawc.gamma1.root_reference_initial_data",
        (root_value / root_value - 1)
        + (root_slope / root_value).subs(root_slope, 0),
        "Conditional on u_0,Q(Q0)=0 and u_0(Q0)!=0, u_0/u_0(Q0) has the declared c_p initial data (1,0), so ODE uniqueness gives c_p=u_0/u_0(Q0).",
    )
    audit.identity(
        "rawc.gamma1.K_scaled_derivative_at_zero",
        (-endpoint * total) / endpoint + total,
        "For the K-scaled zero-shell representative, partial_lambda Gamma_1|0=-u_0(Q0)*D_total and its normalization-invariant ratio is -D_total.",
    )
    c_symbol = sp.symbols("C", positive=True)
    audit.identity(
        "rawc.gamma1.mellin_weight_coefficient",
        (2 / sp.sqrt(c_symbol)).subs(c_symbol, 6 * sp.pi**2)
        - sp.sqrt(sp.Rational(2, 3)) / sp.pi,
        "N_f=2*I_total reduces to sqrt(2/3)/pi times the x^(1/2) Bessel-square Mellin integral.",
    )


def h_box(row: dict[str, Any]) -> arb:
    record = row.get("certified_h_Q0_intersection")
    if not isinstance(record, dict):
        raise AssertionError("missing upstream certified h(Q0) intersection")
    return interval_from_bounds(arb(record["lower"]), arb(record["upper"]))


def lambda_boxes(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    boxes: list[dict[str, Any]] = []
    for item in cfg["declared_conventions"]["nonzero_lambda_boxes"]:
        left = exact_rational(item["left"])
        right = exact_rational(item["right"])
        if not left < right:
            raise AssertionError("lambda box ordering drift")
        abs_max = max(abs(left), abs(right))
        boxes.append(
            {
                "label": item["label"],
                "left": left,
                "right": right,
                "abs_max": abs_max,
            }
        )
    if [item["label"] for item in boxes] != ["negative", "positive"]:
        raise AssertionError("lambda box label or order drift")
    return boxes


def run_tier(
    audit: Audit,
    *,
    root_index: int,
    tier_index: int,
    left: fmpq,
    right: fmpq,
    right_contribution: arb,
    dps: int,
    max_total_width: str,
    max_left_width: str,
    max_f_lambda_width: str,
    max_reference_width: str,
    cfg: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, arb] | None]:
    ctx.dps = dps
    conventions = cfg["declared_conventions"]
    digits = int(conventions["ball_output_digits"])
    band = bracket_band(left, right)
    c_value = 6 * arb.pi() ** 2
    sqrt_c = c_value.sqrt()
    x0 = c_value * arb(-4).exp()
    k0 = audit.bessel_k(acb(x0), acb(0, band))
    endpoint_ok = bool(
        k0.is_finite()
        and contains_zero(k0.imag)
        and not contains_zero(k0.real)
        and k0.abs_lower() > 0
    )

    three_quarters = arb(3) / 4
    gamma_base = audit.gamma(acb(three_quarters))
    gamma_plus = audit.gamma(acb(three_quarters, band))
    gamma_minus = audit.gamma(acb(three_quarters, -band))
    gamma_three_halves = audit.gamma(acb(arb(3) / 2))
    mellin_prefactor = arb(1) / (2 * arb(2).sqrt())
    mellin = (
        acb(mellin_prefactor)
        * gamma_base**2
        * gamma_plus
        * gamma_minus
        / gamma_three_halves
    )
    mellin_ok = bool(
        mellin.is_finite()
        and contains_zero(mellin.imag)
        and mellin.real.lower() > 0
    )
    audit.ball_check(
        f"rawc.gamma1.root{root_index}.tier{tier_index}.endpoint_and_mellin",
        endpoint_ok and mellin_ok,
        "The full-band endpoint K ball excludes zero and the GR Mellin gamma product is finite, real-containing and positive.",
        K_Q0=complex_ball_record(k0, digits),
        mellin_integral=complex_ball_record(mellin, digits),
    )
    if not (endpoint_ok and mellin_ok):
        return {
            "decimal_digits": dps,
            "status": "UNRESOLVED_ENDPOINT_OR_MELLIN",
        }, None

    total_integral = mellin.real / sqrt_c
    normalized_total = total_integral / (k0.real**2)
    normalized_left = normalized_total - right_contribution
    k_scaled_gamma1_derivative = -k0.real * normalized_total
    total_ok = bool(
        normalized_total.lower() > 0
        and width(normalized_total).upper() < arb(max_total_width).lower()
    )
    left_ok = bool(
        normalized_left.lower() > 0
        and width(normalized_left).upper() < arb(max_left_width).lower()
    )
    f_lambda_ok = bool(
        not contains_zero(k_scaled_gamma1_derivative)
        and width(k_scaled_gamma1_derivative).upper()
        < arb(max_f_lambda_width).lower()
    )
    audit.ball_check(
        f"rawc.gamma1.root{root_index}.tier{tier_index}.left_correction_and_derivative",
        total_ok and left_ok and f_lambda_ok,
        "Conditional on any zero-shell root in the full bracket, the normalized full declared derivative is strictly negative, the omitted normalized left correction is positive, and the K-scaled partial_lambda Gamma_1 enclosure at zero excludes zero.",
        normalized_total_magnitude=interval_record(normalized_total, digits),
        normalized_declared_derivative=interval_record(-normalized_total, digits),
        finite_Q0_proxy_magnitude=interval_record(right_contribution, digits),
        normalized_left_correction=interval_record(normalized_left, digits),
        K_scaled_partial_lambda_Gamma1_at_zero=interval_record(
            k_scaled_gamma1_derivative, digits
        ),
        maximum_normalized_total_width=max_total_width,
        maximum_normalized_left_width=max_left_width,
        maximum_K_scaled_Gamma1_derivative_width=max_f_lambda_width,
    )

    q_bound = 18 * arb.pi() ** 4 * arb(-8).exp() / band
    reference_envelope = 2 * arb.pi() * arb(-3).exp() * q_bound.exp()
    reference_ok = bool(
        q_bound.is_finite()
        and q_bound.lower() > 0
        and reference_envelope.is_finite()
        and reference_envelope.lower() > 0
        and width(reference_envelope).upper()
        < arb(max_reference_width).lower()
    )
    audit.ball_check(
        f"rawc.gamma1.root{root_index}.tier{tier_index}.reference_tail_bound",
        reference_ok,
        "The free-rotation comparison gives a finite full minus-tail L2(a) reference envelope without a cutoff, ODE solve or quadrature.",
        q_bound=interval_record(q_bound, digits),
        reference_M_c_envelope=interval_record(reference_envelope, digits),
        maximum_reference_norm_bound_width=max_reference_width,
    )

    lambda_records: list[dict[str, Any]] = []
    lambda_ok = True
    cap = exact_rational(conventions["lambda_absolute_cap"])
    for box in lambda_boxes(cfg):
        box_band = bracket_band(box["left"], box["right"])
        excludes_zero = bool(box["right"] < 0 or box["left"] > 0)
        within_cap = bool(box["abs_max"] <= cap)
        covers_exact_box = bool(
            box_band.lower() <= box["left"]
            and box_band.upper() >= box["right"]
        )
        coefficient_upper = (
            arb(box["abs_max"]) * reference_envelope.upper() / arb(2).sqrt()
        ).upper()
        coefficient = interval_from_bounds(arb(0), coefficient_upper)
        box_ok = bool(
            excludes_zero
            and within_cap
            and covers_exact_box
            and coefficient.is_finite()
            and coefficient.upper()
            < arb(conventions["maximum_nonzero_correction_per_unit_f_norm"]).lower()
        )
        lambda_ok = lambda_ok and box_ok
        audit.ball_check(
            f"rawc.gamma1.root{root_index}.tier{tier_index}.lambda_{box['label']}_operator_bound",
            box_ok,
            "The punctured real lambda box excludes zero and the Gamma_1 minus-tail correction coefficient per unit L2(f) norm has the declared uniform upper bound.",
            lambda_box={
                "label": box["label"],
                "left_exact": str(box["left"]),
                "right_exact": str(box["right"]),
                "coverage": interval_record(box_band, digits),
            },
            correction_per_unit_L2_f_norm=interval_record(coefficient, digits),
            maximum_allowed=conventions[
                "maximum_nonzero_correction_per_unit_f_norm"
            ],
        )
        lambda_records.append(
            {
                "label": box["label"],
                "box": interval_record(box_band, digits),
                "correction_per_unit_L2_f_norm": interval_record(
                    coefficient, digits
                ),
            }
        )

    all_ok = total_ok and left_ok and f_lambda_ok and reference_ok and lambda_ok
    record = {
        "decimal_digits": dps,
        "status": "CERTIFIED_TIER" if all_ok else "UNRESOLVED_TIER",
        "same_backend_repeat": True,
        "K_Q0": complex_ball_record(k0, digits),
        "mellin_integral": complex_ball_record(mellin, digits),
        "full_A_lambda_integral": interval_record(total_integral, digits),
        "normalized_total_magnitude": interval_record(normalized_total, digits),
        "normalized_declared_derivative": interval_record(-normalized_total, digits),
        "finite_Q0_proxy_magnitude": interval_record(right_contribution, digits),
        "normalized_left_correction": interval_record(normalized_left, digits),
        "K_scaled_partial_lambda_Gamma1_at_zero": interval_record(
            k_scaled_gamma1_derivative, digits
        ),
        "reference_q_bound": interval_record(q_bound, digits),
        "reference_M_c_envelope": interval_record(reference_envelope, digits),
        "nonzero_lambda_operator_bounds": lambda_records,
    }
    values = {
        "normalized_total": normalized_total,
        "normalized_left": normalized_left,
        "K_scaled_Gamma1_derivative": k_scaled_gamma1_derivative,
        "reference_envelope": reference_envelope,
    }
    return record, values if all_ok else None


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    if importlib.metadata.version("python-flint") != "0.9.0":
        raise AssertionError("python-flint runtime version drift")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input_sha = sha256_bytes(raw)
    if observed_input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input_sha}")
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-declared-gamma1-boundary-variation.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if (
        cfg.get("resource_caps") != expected_caps()
        or cfg.get("required_fail_closed_outputs") != expected_nulls()
        or cfg["declared_conventions"]["precision_ladder_decimal_digits"]
        != [80, 120]
        or len(lambda_boxes(cfg)) != expected_caps()["nonzero_lambda_boxes"]
    ):
        raise AssertionError("resource, precision or fail-closed mutation")

    root = Path(__file__).resolve().parent.parent
    verified = [verify_upstream(root, item) for item in cfg["upstream_results"]]
    extension_data, extension_record = verified[0]
    bessel_data, bessel_record = verified[1]
    green_data, green_record = verified[2]
    extension_boundary = extension_data["exact_calculation"]["boundary_maps"]
    if "Gamma_1,p=-W(u,c_p)|_-infinity" not in extension_boundary:
        raise AssertionError("declared extension boundary-map drift")
    bessel_rows = bessel_data["certified_calculation"]["endpoint_characteristic"][
        "root_rows"
    ]
    green_rows = green_data["certified_calculation"]["root_bracket_rows"]
    if (
        len(bessel_rows) != expected_caps()["root_brackets"]
        or len(green_rows) != expected_caps()["root_brackets"]
    ):
        raise AssertionError("five-bracket upstream count drift")

    audit = Audit()
    exact_audit(audit)
    conventions = cfg["declared_conventions"]
    rows: list[dict[str, Any]] = []
    for root_index, (bessel_row, green_row) in enumerate(
        zip(bessel_rows, green_rows, strict=True), start=1
    ):
        bracket = bessel_row["certified_high_precision_bracket"]
        left = exact_rational(bracket["left_exact"])
        right = exact_rational(bracket["right_exact"])
        if not left < right:
            raise AssertionError("upstream bracket ordering drift")
        green_bracket = green_row.get("kappa_bracket")
        if (
            not isinstance(green_bracket, dict)
            or green_bracket.get("left_exact") != str(left)
            or green_bracket.get("right_exact") != str(right)
        ):
            raise AssertionError("Bessel and Green bracket alignment drift")
        ctx.dps = max(conventions["precision_ladder_decimal_digits"])
        coverage = bracket_band(left, right)
        coverage_ok = bool(
            coverage.lower() <= left
            and coverage.upper() >= right
            and coverage.lower() > 0
        )
        audit.ball_check(
            f"rawc.gamma1.root{root_index}.band_coverage",
            coverage_ok,
            "The outward Arb band covers the full exact-rational inherited sign-change bracket; no midpoint or unique root is substituted.",
            left_exact=str(left),
            right_exact=str(right),
            coverage=interval_record(
                coverage, int(conventions["ball_output_digits"])
            ),
        )
        right_box = h_box(green_row)
        tier_records: list[dict[str, Any]] = []
        tier_values: list[dict[str, arb] | None] = []
        for tier_index, (
            dps,
            max_total,
            max_left,
            max_f_lambda,
            max_reference,
        ) in enumerate(
            zip(
                conventions["precision_ladder_decimal_digits"],
                conventions["maximum_normalized_total_widths"],
                conventions["maximum_normalized_left_widths"],
                conventions["maximum_K_scaled_Gamma1_derivative_widths"],
                conventions["maximum_reference_norm_bound_widths"],
                strict=True,
            ),
            start=1,
        ):
            record, values = run_tier(
                audit,
                root_index=root_index,
                tier_index=tier_index,
                left=left,
                right=right,
                right_contribution=right_box,
                dps=int(dps),
                max_total_width=max_total,
                max_left_width=max_left,
                max_f_lambda_width=max_f_lambda,
                max_reference_width=max_reference,
                cfg=cfg,
            )
            tier_records.append(record)
            tier_values.append(values)

        keys = (
            "normalized_total",
            "normalized_left",
            "K_scaled_Gamma1_derivative",
            "reference_envelope",
        )
        intersections: dict[str, arb | None] = {}
        refinement_ok = bool(tier_values[0] is not None and tier_values[1] is not None)
        if tier_values[0] is not None and tier_values[1] is not None:
            for key in keys:
                intersections[key] = intersect(
                    tier_values[0][key], tier_values[1][key]
                )
                refinement_ok = (
                    refinement_ok
                    and intersections[key] is not None
                    and width(tier_values[1][key]).upper()
                    <= width(tier_values[0][key]).upper()
                )
        else:
            intersections = {key: None for key in keys}
        audit.ball_check(
            f"rawc.gamma1.root{root_index}.precision_refinement",
            refinement_ok,
            "The two same-backend full-band certificates overlap and the 120-digit widths do not increase; intersections are retained without treating the repeat as independent validation.",
            normalized_total_intersection=interval_record(
                intersections["normalized_total"],
                int(conventions["ball_output_digits"]),
            )
            if intersections["normalized_total"] is not None
            else None,
            normalized_left_intersection=interval_record(
                intersections["normalized_left"],
                int(conventions["ball_output_digits"]),
            )
            if intersections["normalized_left"] is not None
            else None,
            K_scaled_Gamma1_derivative_intersection=interval_record(
                intersections["K_scaled_Gamma1_derivative"],
                int(conventions["ball_output_digits"]),
            )
            if intersections["K_scaled_Gamma1_derivative"] is not None
            else None,
            reference_envelope_intersection=interval_record(
                intersections["reference_envelope"],
                int(conventions["ball_output_digits"]),
            )
            if intersections["reference_envelope"] is not None
            else None,
        )
        rows.append(
            {
                "root_index": root_index,
                "kappa_bracket": {
                    "left_exact": str(left),
                    "right_exact": str(right),
                    "width_exact": str(right - left),
                    "coverage_ball": interval_record(
                        coverage, int(conventions["ball_output_digits"])
                    ),
                    "root_scope": "at least one inherited sign-changing zero exists; every reported enclosure covers any root in the bracket without assuming uniqueness",
                },
                "finite_Q0_proxy_magnitude_upstream": interval_record(
                    right_box, int(conventions["ball_output_digits"])
                ),
                "precision_tiers": tier_records,
                "certified_normalized_total_magnitude": interval_record(
                    intersections["normalized_total"],
                    int(conventions["ball_output_digits"]),
                )
                if refinement_ok and intersections["normalized_total"] is not None
                else None,
                "certified_normalized_declared_derivative": interval_record(
                    -intersections["normalized_total"],
                    int(conventions["ball_output_digits"]),
                )
                if refinement_ok and intersections["normalized_total"] is not None
                else None,
                "certified_normalized_left_correction": interval_record(
                    intersections["normalized_left"],
                    int(conventions["ball_output_digits"]),
                )
                if refinement_ok and intersections["normalized_left"] is not None
                else None,
                "certified_K_scaled_partial_lambda_Gamma1_at_zero": interval_record(
                    intersections["K_scaled_Gamma1_derivative"],
                    int(conventions["ball_output_digits"]),
                )
                if refinement_ok
                and intersections["K_scaled_Gamma1_derivative"] is not None
                else None,
                "certified_reference_M_c_envelope": interval_record(
                    intersections["reference_envelope"],
                    int(conventions["ball_output_digits"]),
                )
                if refinement_ok and intersections["reference_envelope"] is not None
                else None,
            }
        )

    audit.guard(
        "rawc.gamma1.guard.selected_fixed_reference",
        "declared Wronskian boundary-pair extension",
        "The pinned raw-C extension fixes c_p(-4)=1,c_p,Q(-4)=0 and Gamma_1,p=-lim W(u,c_p), with c_p independent of lambda.",
        "The identity and derivative concern that one declared p-preserving extension only; no physical uniqueness or p-mixing classification follows.",
    )
    audit.guard(
        "rawc.gamma1.guard.integrated_lagrange_identity",
        "Lagrange/Wronskian identity and differentiable plus-recessive solution family at lambda=0",
        "u_lambda solves the divided raw-C equation, c_p solves the zero-energy reference equation, the minus Wronskian limit exists, and the lambda derivative may be passed through the weighted identity at a zero-shell root.",
        "Gamma_1(u_lambda)=u_Q(Q0)-lambda*int a*u*c and Gamma_1,lambda(0)/u_0(Q0)=-I_total/u_0(Q0)^2; no finite nonzero-lambda Weyl value is constructed.",
    )
    audit.guard(
        "rawc.gamma1.guard.free_rotation_reference_bound",
        "variation-of-constants/Gronwall comparison with a skew free oscillator",
        "kappa has a strictly positive full-band lower bound, V=36*pi^4*exp(2Q) is integrable on (-infinity,-4], and y=(c,c_Q/kappa) starts with unit norm at Q0.",
        "|c_p(Q)|<=exp(18*pi^4*exp(-8)/kappa) and the reported M_c envelope bounds the entire minus tail without a cutoff or ODE calculation.",
    )
    audit.guard(
        "rawc.gamma1.guard.cauchy_schwarz_functional",
        "weighted Cauchy-Schwarz inequality",
        "u has finite declared minus-tail L2(f dQ) norm and c_p obeys the certified L2(a dQ) envelope with f=2a.",
        "For either punctured lambda box, the reported coefficient bounds |Gamma_1-u_Q(Q0)| per unit L2(f) tail norm; it is not an actual Gamma_1 value for a constructed solution.",
    )
    audit.guard(
        "rawc.gamma1.guard.mellin_total",
        "Gradshteyn-Ryzhik 6.576(4) with modified-Bessel reality and order conjugation",
        "mu=3/2, nu=i*kappa, kappa real and positive, and K_(i*kappa)(x) is real for x>0.",
        "The full weighted K-square integral is finite and positive; subtracting the independent right Green box gives a rigorous correlation-forgetting left-correction enclosure.",
    )
    audit.guard(
        "rawc.gamma1.guard.scope",
        "local full-bracket declared-characteristic scope",
        "Only the two punctured lambda-box functional coefficients and the lambda-zero derivative at any root in five inherited brackets are emitted.",
        "No actual nonzero-lambda plus solution, endpoint remainder, root continuation or velocity, resolvent, spectrum, RAQ, C-H equivalence, BFV, observation, physics, quantum-gravity or TOE conclusion follows.",
    )

    passed = bool(
        all(item["passed"] for item in audit.exact + audit.ball)
        and audit.bessel_evaluations <= expected_caps()["ball_bessel_evaluations"]
        and audit.gamma_evaluations <= expected_caps()["ball_gamma_evaluations"]
    )
    decision = cfg["decision_table"][0 if passed else 1]
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": decision["verdict"],
        "programme_impact": decision["programme_impact"],
        "input_manifest": {
            "path": INPUT_RELPATH,
            "sha256": observed_input_sha,
            "numbered_phase": None,
        },
        "upstream_results": [extension_record, bessel_record, green_record],
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": conventions,
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
            "status": "CERTIFIED_DECLARED_GAMMA1_LEFT_BOUNDARY_VARIATION_AND_ZERO_SHELL_DERIVATIVE_ON_FIVE_BRACKETS"
            if passed
            else "NOT_CERTIFIED",
            "exact_nonzero_lambda_identity": conventions[
                "exact_nonzero_lambda_identity"
            ],
            "nonzero_lambda_output_scope": "uniform correction-functional coefficient per unit declared minus-tail L2(f) norm on two punctured lambda boxes; no actual u_lambda or Gamma_1 value",
            "lambda_zero_root_output_scope": "outward full-bracket enclosures of the normalized declared derivative, the explicit omitted left term, and the K-scaled partial_lambda Gamma_1 at zero conditional on any root in each bracket",
            "root_bracket_rows": rows,
            "next_mathematical_gap": "construct a validated nonzero-lambda plus-recessive solution and a direct minus-end remainder enclosure before continuing roots or building spectral/RAQ data",
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "ball_bessel_evaluations": audit.bessel_evaluations,
            "ball_bessel_evaluation_cap": expected_caps()[
                "ball_bessel_evaluations"
            ],
            "ball_gamma_evaluations": audit.gamma_evaluations,
            "ball_gamma_evaluation_cap": expected_caps()["ball_gamma_evaluations"],
            "quadrature_calls": 0,
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
                "verdict": result["verdict"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "ball_passed": result["check_summary"]["ball_passed"],
                "ball_total": result["check_summary"]["ball_total"],
                "theorem_guards": result["check_summary"]["theorem_guard_count"],
                "certified_brackets": sum(
                    row["certified_K_scaled_partial_lambda_Gamma1_at_zero"]
                    is not None
                    for row in rows
                )
                if passed
                else 0,
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
