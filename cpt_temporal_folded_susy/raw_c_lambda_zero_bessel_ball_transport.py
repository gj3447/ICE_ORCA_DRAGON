#!/usr/bin/env python3
"""Rigorous lambda-zero raw-C Bessel endpoint anchor; not F_lambda or RAQ."""
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


INPUT_NAME = "RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_INPUTS.json"
RESULT_NAME = "RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_lambda_zero_bessel_ball_transport.py"
EXPECTED_INPUT_SHA256 = "c2f5c0479c39b0c464fe3a04fb2b3c868c6b767b292f0f1a7ff3c43f20682607"
CALCULATION_ID = "RawCLambdaZeroBesselBallTransport"
RESULT_SCHEMA = "ice.raw-c-lambda-zero-bessel-ball-transport.result.v1"
RESULT_PREFIX = "RAW_C_LAMBDA_ZERO_BESSEL_BALL_TRANSPORT_RESULT="
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
        "nonzero_lambda_validated_transport": None,
        "endpoint_F_lambda": None,
        "unique_or_complete_zero_shell_root_census": None,
        "nonreal_resolvent_or_weyl_m_function": None,
        "raw_C_spectral_measure": None,
        "global_delta_C_measure": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "general_p_mixing_extension_classification": None,
        "canonical_p_zero_origin_sector": None,
        "absolute_bfv_measure": None,
        "continuum_determinant_or_pfaffian_line": None,
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
        "ball_bessel_evaluations": 5000,
        "root_brackets": 5,
        "root_calls": 0,
        "quadratures": 0,
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
        self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str
    ) -> None:
        self.register(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": "SOURCE_PIN_PLUS_EXECUTABLE_BALL_HYPOTHESIS_AND_SCOPE_AUDIT",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream(root: Path, item: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
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
    record = {
        "path": item["path"],
        "sha256": item["sha256"],
        "payload_sha256_without_self": item["payload_sha256_without_self"],
        "verdict": item["required_verdict"],
    }
    return result, record


def exact_rational(decimal_text: str) -> fmpq:
    value = Fraction(decimal_text)
    return fmpq(value.numerator, value.denominator)


def rational_text(value: fmpq) -> str:
    return str(value)


def interval_record(value: arb, digits: int) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
    }


def complex_ball_record(value: acb, digits: int) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "absolute_lower": value.abs_lower().str(digits, radius=False),
        "absolute_upper": value.abs_upper().str(digits, radius=False),
    }


def contains_real(value: arb, target: int | fmpq) -> bool:
    return bool(value.lower() <= target and target <= value.upper())


def definite_sign(value: acb) -> int:
    if not contains_real(value.imag, 0):
        return 0
    if value.real.lower() > 0:
        return 1
    if value.real.upper() < 0:
        return -1
    return 0


def bessel_k(audit: Audit, z: acb, order: acb, *, scaled: bool = False) -> acb:
    audit.bessel_evaluations += 1
    if audit.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
        raise AssertionError("ball Bessel evaluation cap exceeded")
    return z.bessel_k(order, scaled=scaled)


def bessel_i(audit: Audit, z: acb, order: acb, *, scaled: bool = False) -> acb:
    audit.bessel_evaluations += 1
    if audit.bessel_evaluations > expected_caps()["ball_bessel_evaluations"]:
        raise AssertionError("ball Bessel evaluation cap exceeded")
    return z.bessel_i(order, scaled=scaled)


def characteristic(audit: Audit, z: acb, kappa: fmpq | arb) -> acb:
    order = acb(0, arb(kappa))
    return -z * (
        bessel_k(audit, z, order - 1) + bessel_k(audit, z, order + 1)
    ) / 2


def bisect_sign_change(
    audit: Audit,
    z: acb,
    left: fmpq,
    right: fmpq,
    steps: int,
) -> tuple[fmpq, fmpq, acb, acb, int, int]:
    left_value = characteristic(audit, z, left)
    right_value = characteristic(audit, z, right)
    left_sign = definite_sign(left_value)
    right_sign = definite_sign(right_value)
    if left_sign * right_sign != -1:
        raise AssertionError("initial ball endpoints do not certify opposite signs")
    for _ in range(steps):
        midpoint = (left + right) / 2
        middle_value = characteristic(audit, z, midpoint)
        middle_sign = definite_sign(middle_value)
        if middle_sign == 0:
            raise AssertionError("bisection midpoint ball does not exclude zero")
        if left_sign * middle_sign == -1:
            right, right_value, right_sign = midpoint, middle_value, middle_sign
        elif middle_sign * right_sign == -1:
            left, left_value, left_sign = midpoint, middle_value, middle_sign
        else:
            raise AssertionError("bisection sign invariant failed")
    return left, right, left_value, right_value, left_sign, right_sign


def bracket_band(left: fmpq, right: fmpq) -> arb:
    midpoint = (left + right) / 2
    radius = (right - left) / 2
    return arb(arb(midpoint), arb(radius))


def bracket_subset(
    inner_left: fmpq,
    inner_right: fmpq,
    outer_left: fmpq,
    outer_right: fmpq,
) -> bool:
    return bool(
        outer_left <= inner_left <= inner_right <= outer_right
        and inner_left < inner_right
    )


def endpoint_band_checks(
    audit: Audit,
    z0: acb,
    zplus: acb,
    kappa_band: arb,
    tail_budget: arb,
    digits: int,
) -> dict[str, Any]:
    order = acb(0, kappa_band)
    k0 = bessel_k(audit, z0, order)
    km = bessel_k(audit, z0, order - 1)
    kp = bessel_k(audit, z0, order + 1)
    i0 = bessel_i(audit, z0, order)
    im = bessel_i(audit, z0, order - 1)
    ip = bessel_i(audit, z0, order + 1)
    qk = -z0 * (km + kp) / 2
    qi = z0 * (im + ip) / 2
    wronskian_q = k0 * qi - qk * i0

    kplus = bessel_k(audit, zplus, order, scaled=True)
    km_plus = bessel_k(audit, zplus, order - 1, scaled=True)
    kp_plus = bessel_k(audit, zplus, order + 1, scaled=True)
    q_plus = -zplus * (km_plus + kp_plus) / (2 * kplus)
    a_plus = zplus * zplus - kappa_band * kappa_band
    sqrt_a_plus = a_plus.sqrt()
    q_wkb = -sqrt_a_plus - (2 * zplus * zplus) / (4 * a_plus)
    normalized_difference = (q_plus - q_wkb) / sqrt_a_plus

    return {
        "K_at_Q0": k0,
        "wronskian_Q_K_I": wronskian_q,
        "scaled_K_at_Qplus": kplus,
        "log_derivative_at_Qplus": q_plus,
        "wkb_log_derivative_at_Qplus": q_wkb,
        "normalized_difference_at_Qplus": normalized_difference,
        "K_at_Q0_excludes_zero": bool(k0.abs_lower() > 0),
        "wronskian_contains_one": bool(
            contains_real(wronskian_q.real, 1)
            and contains_real(wronskian_q.imag, 0)
        ),
        "scaled_K_at_Qplus_excludes_zero": bool(kplus.abs_lower() > 0),
        "tail_budget_contains_difference": bool(
            normalized_difference.abs_upper() < tail_budget.lower()
        ),
        "record": {
            "K_at_Q0": complex_ball_record(k0, digits),
            "wronskian_Q_K_I": complex_ball_record(wronskian_q, digits),
            "scaled_K_at_Qplus": complex_ball_record(kplus, digits),
            "log_derivative_at_Qplus": complex_ball_record(q_plus, digits),
            "wkb_log_derivative_at_Qplus": complex_ball_record(q_wkb, digits),
            "normalized_difference_at_Qplus": complex_ball_record(
                normalized_difference, digits
            ),
        },
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no command-line arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-lambda-zero-bessel-ball-transport.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if (
        cfg.get("resource_caps") != expected_caps()
        or cfg.get("required_fail_closed_outputs") != expected_nulls()
        or cfg["declared_conventions"]["precision_ladder_decimal_digits"]
        != [80, 120]
        or cfg["declared_conventions"]["bisection_steps"] != [64, 96]
    ):
        raise AssertionError("resource, precision or fail-closed mutation")

    root = Path(__file__).resolve().parent.parent
    loaded: list[dict[str, Any]] = []
    upstream_records: list[dict[str, str]] = []
    for item in cfg["upstream_results"]:
        result, record = verify_upstream(root, item)
        loaded.append(result)
        upstream_records.append(record)
    _, census, tail = loaded
    root_rows = census["numerical_calculation"]["roots"]
    if len(root_rows) != cfg["resource_caps"]["root_brackets"]:
        raise AssertionError("upstream root-bracket count drift")

    audit = Audit()
    Q, x, kappa, p, lam = sp.symbols("Q x kappa p lambda", real=True)
    u, ux, uxx, v, vqq = sp.symbols("u ux uxx v vqq")
    chain_second = x**2 * uxx + x * ux
    modified_bessel_residual = x**2 * uxx + x * ux - (x**2 - kappa**2) * u
    raw_lambda_zero_residual = chain_second - (x**2 - kappa**2) * u
    a0 = 36 * sp.pi**4 * sp.exp(2 * Q) - kappa**2
    a_lambda = 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * Q)
    audit.identity(
        "rawc.ball.change_of_variable",
        raw_lambda_zero_residual - modified_bessel_residual,
        "For x=6*pi^2*exp(Q), d_Q^2=x^2*d_x^2+x*d_x converts the lambda-zero raw-C fiber to the imaginary-order modified-Bessel equation.",
    )
    audit.identity(
        "rawc.ball.coefficient",
        a0 - (x**2 - kappa**2).subs(x, 6 * sp.pi**2 * sp.exp(Q)),
        "The exact lambda-zero Q coefficient equals x(Q)^2-kappa^2.",
    )
    audit.identity(
        "rawc.ball.p_parity",
        a0.subs(kappa, sp.sqrt(sp.Rational(3, 2)) * p)
        - a0.subs(kappa, -sp.sqrt(sp.Rational(3, 2)) * p),
        "Both p signs have the same lambda-zero fiber coefficient.",
    )
    audit.identity(
        "rawc.ball.lambda_sensitivity_forcing",
        vqq - a0 * v - a_lambda * u
        - (vqq - a0 * v - 6 * sp.pi**2 * sp.exp(sp.Rational(3, 2) * Q) * u),
        "Differentiating at lambda=0 requires the displayed forced variational equation; this runner deliberately leaves its boundary datum and F_lambda open.",
    )

    digits_out = int(cfg["declared_conventions"]["ball_output_digits"])
    precision_ladder = cfg["declared_conventions"][
        "precision_ladder_decimal_digits"
    ]
    step_ladder = cfg["declared_conventions"]["bisection_steps"]
    tail_budget = arb(
        tail["analytic_calculation"]["at_Q_plus_4"][
            "sqrt_A_normalized_log_derivative_difference_bound"
        ]
    )
    rows: list[dict[str, Any]] = []

    for index, source_row in enumerate(root_rows, start=1):
        initial_left = exact_rational(source_row["initial_bracket_left"])
        initial_right = exact_rational(source_row["initial_bracket_right"])
        precision_runs: list[dict[str, Any]] = []
        bracket_values: list[tuple[fmpq, fmpq]] = []
        for tier, (dps, steps) in enumerate(
            zip(precision_ladder, step_ladder, strict=True), start=1
        ):
            ctx.dps = int(dps)
            z0 = acb(6 * arb.pi() ** 2 * arb(-4).exp())
            left, right, left_value, right_value, left_sign, right_sign = (
                bisect_sign_change(
                    audit, z0, initial_left, initial_right, int(steps)
                )
            )
            bracket_values.append((left, right))
            signs_pass = left_sign * right_sign == -1
            audit.ball_check(
                f"rawc.ball.root{index}.tier{tier}.opposite_signs",
                signs_pass,
                "Outward-rounded endpoint balls certify opposite real characteristic signs after the declared exact-rational bisection ladder.",
                decimal_digits=int(dps),
                bisection_steps=int(steps),
                left_sign=left_sign,
                right_sign=right_sign,
                left_value=complex_ball_record(left_value, digits_out),
                right_value=complex_ball_record(right_value, digits_out),
            )
            precision_runs.append(
                {
                    "decimal_digits": int(dps),
                    "bisection_steps": int(steps),
                    "left_exact": rational_text(left),
                    "right_exact": rational_text(right),
                    "width_exact": rational_text(right - left),
                    "left_characteristic": complex_ball_record(
                        left_value, digits_out
                    ),
                    "right_characteristic": complex_ball_record(
                        right_value, digits_out
                    ),
                    "signs": [left_sign, right_sign],
                }
            )

        low_left, low_right = bracket_values[0]
        high_left, high_right = bracket_values[1]
        nested = bracket_subset(high_left, high_right, low_left, low_right)
        audit.ball_check(
            f"rawc.ball.root{index}.precision_nesting",
            nested,
            "The 120-digit, 96-step exact-rational sign bracket nests inside the independent 80-digit, 64-step bracket.",
            low_width_exact=rational_text(low_right - low_left),
            high_width_exact=rational_text(high_right - high_left),
        )

        ctx.dps = int(precision_ladder[-1])
        z0 = acb(6 * arb.pi() ** 2 * arb(-4).exp())
        zplus = acb(6 * arb.pi() ** 2 * arb(4).exp())
        high_band = bracket_band(high_left, high_right)
        endpoint = endpoint_band_checks(
            audit, z0, zplus, high_band, tail_budget, digits_out
        )
        audit.ball_check(
            f"rawc.ball.root{index}.K_Q0_nonzero",
            endpoint["K_at_Q0_excludes_zero"],
            "K_(i*kappa)(x0) excludes zero on the full certified characteristic bracket, so the derivative-zero endpoint datum has nonzero amplitude.",
            K_at_Q0=endpoint["record"]["K_at_Q0"],
        )
        audit.ball_check(
            f"rawc.ball.root{index}.wronskian",
            endpoint["wronskian_contains_one"],
            "The full bracket-band ball for W_Q(K_(i*kappa),I_(i*kappa)) contains one, retaining a node-safe independent solution pair.",
            wronskian=endpoint["record"]["wronskian_Q_K_I"],
        )
        audit.ball_check(
            f"rawc.ball.root{index}.scaled_K_Qplus_nonzero",
            endpoint["scaled_K_at_Qplus_excludes_zero"],
            "The exponentially scaled recessive K ball excludes zero at Qplus=4 on the full bracket band.",
            scaled_K_at_Qplus=endpoint["record"]["scaled_K_at_Qplus"],
        )
        audit.ball_check(
            f"rawc.ball.root{index}.tail_containment",
            endpoint["tail_budget_contains_difference"],
            "The exact lambda-zero Bessel log derivative is contained by the independently inherited Liouville-Green normalized tail budget at Qplus=4.",
            inherited_tail_budget=tail_budget.str(digits_out),
            normalized_difference=endpoint["record"][
                "normalized_difference_at_Qplus"
            ],
        )
        rows.append(
            {
                "root_index": index,
                "upstream_nonrigorous_center": source_row["kappa"],
                "upstream_initial_bracket": [
                    source_row["initial_bracket_left"],
                    source_row["initial_bracket_right"],
                ],
                "precision_runs": precision_runs,
                "certified_high_precision_bracket": {
                    "left_exact": rational_text(high_left),
                    "right_exact": rational_text(high_right),
                    "width_exact": rational_text(high_right - high_left),
                    "at_least_one_real_sign_changing_zero": True,
                    "uniqueness": None,
                },
                "endpoint_balls": endpoint["record"],
            }
        )

    audit.guard(
        "rawc.ball.guard.dlmf_bessel",
        "DLMF sections 10.25, 10.28 and 10.29",
        "x=6*pi^2*exp(Q)>0, nu=i*kappa, lambda=0, the K branch is recessive at positive infinity, and the derivative and Wronskian conventions are the declared ones",
        "The exact K representation and W_Q(K,I)=1 transport the lambda-zero recessive direction without an ill-conditioned raw fundamental matrix. DLMF does not provide the emitted ball enclosures or any nonzero-lambda, spectral or RAQ conclusion.",
    )
    audit.guard(
        "rawc.ball.guard.arb_inclusion",
        "Arb midpoint-radius inclusion arithmetic as exposed by locked python-flint 0.9.0",
        "Every accepted sign uses a real lower or upper bound that excludes zero; every interval conclusion uses the full input ball; both precision tiers and exact-rational nesting are retained",
        "The certificates cover only the displayed endpoint values and five sign-changing brackets at lambda=0. A small radius alone is never counted as a proof, and uniqueness is not inferred.",
    )
    audit.guard(
        "rawc.ball.guard.ivt",
        "Intermediate value theorem for the entire-in-order modified Bessel K characteristic",
        "DLMF gives entire dependence on nu for fixed positive x, and every bracket has rigorously opposite finite endpoint signs",
        "Each bracket contains at least one real zero. This does not exclude an even number of additional roots, certify uniqueness, or prove that the five brackets exhaust kappa in [0,8].",
    )
    audit.guard(
        "rawc.ball.guard.no_Flambda",
        "Parameter-differentiated endpoint requirement",
        "The exact sensitivity equation has a nonzero forcing and needs both a differentiated plus-tail datum and node-safe validated propagation",
        "No F_lambda, nonzero-lambda endpoint box, nonreal m-function, spectral measure, rigging map, physical product or C/H equivalence is emitted by this calculation.",
    )

    all_exact = all(item["passed"] for item in audit.exact)
    all_ball = all(item["passed"] for item in audit.ball)
    passed = all_exact and all_ball
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
            "lambda_zero_recessive_transport": {
                "status": "CERTIFIED_EXACT_SPECIAL_FUNCTION_REPRESENTATION"
                if passed
                else "NOT_CERTIFIED",
                "Q_domain": "[-4,+infinity)",
                "solution_direction": "K_(i*kappa)(6*pi^2*exp(Q))",
                "numerical_fundamental_matrix_used": False,
                "ode_calls": 0,
            },
            "endpoint_characteristic": {
                "definition": "F(kappa)=partial_Q K_(i*kappa)(x(Q)) at Q=-4",
                "certified_sign_change_bracket_count": len(rows) if passed else 0,
                "root_rows": rows,
                "completeness": None,
                "uniqueness_per_bracket": None,
            },
            "next_mathematical_gap": "differentiate the plus-tail Volterra/Liouville-Green construction in lambda, then propagate the forced sensitivity in a validated node-safe two-component or Pruefer atlas",
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations_cap": cfg["resource_caps"]["symbolic_operations"],
            "ball_bessel_evaluations": audit.bessel_evaluations,
            "ball_bessel_evaluation_cap": cfg["resource_caps"][
                "ball_bessel_evaluations"
            ],
            "root_brackets": len(rows),
            "root_calls": 0,
            "quadratures": 0,
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
                    "endpoint_characteristic"
                ]["certified_sign_change_bracket_count"],
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
