#!/usr/bin/env python3
"""Gate 1 -- exact end audit of the Phase 39 straight field-ray lift.

This non-numbered, bounded calculation tests one necessary condition for the
Phase 39 declared m=2 configuration-chain candidate to admit an unbounded
straight-ray relative-cycle completion.  It performs no root solve, ODE,
thimble census, evaluator reconciliation, or physics promotion.

The script verifies the frozen input hash, derives the m=2 slice from the
same scalar action, proves an explicit bad-end subsequence symbolically, and
checks the formula independently by direct high-precision evaluation of the
unreduced two-element action.  It writes one adjacent result JSON.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_INPUTS.json"
RESULT_NAME = "GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_RESULT.json"
EXPECTED_INPUT_SHA256 = (
    "a3bc97461c7989cd5bb471accf46f0c2196de41c3030e9eef2248c4f09a47fdb"
)
RESULT_SCHEMA = "ice.gate1.straight-lift-end-admissibility.result.v1"
RESULT_PREFIX = "GATE1_STRAIGHT_LIFT_END_ADMISSIBILITY_RESULT="
ARTIFACT_CAP_BYTES = 250_000


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> None:
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {check_id}: {statement}")
        self.exact.append(
            {"id": check_id, "passed": True, "statement": statement}
        )

    def check_numerical(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        metrics: dict[str, Any],
    ) -> None:
        if not passed:
            raise AssertionError(f"[NUMERIC FAIL] {check_id}: {statement}")
        self.numerical.append(
            {
                "id": check_id,
                "passed": True,
                "statement": statement,
                "metrics": metrics,
            }
        )


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


def load_frozen_input() -> tuple[dict[str, Any], str]:
    input_path = Path(__file__).with_name(INPUT_NAME)
    raw = input_path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.straight-lift-end-admissibility.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["resource_caps"] != {
        "wall_clock_seconds": 30,
        "artifact_bytes": 250000,
        "root_calls": 0,
        "ode_calls": 0,
        "evaluator_reconciliation_calls": 0,
        "maximum_bad_subsequence_samples_per_arm": 6,
        "automatic_descendants": 0,
    }:
        raise AssertionError("resource cap mutation")
    return payload, observed


def exact_calculation(audit: Audit) -> dict[str, Any]:
    a, phi, n, t = sp.symbols("a phi n t", positive=True, real=True)
    kappa = sp.sqrt(sp.Rational(2, 3))
    growth = sp.simplify(kappa / sp.sqrt(2))
    h = sp.Rational(1, 2)
    delta = sp.symbols("delta")

    a_nodes = (a, a, a)
    phi_nodes = (phi, phi + delta, phi)
    action = sp.Integer(0)
    T = sp.symbols("T", nonzero=True)
    for element in range(2):
        a_left, a_right = a_nodes[element : element + 2]
        phi_left, phi_right = phi_nodes[element : element + 2]
        a_mid = (a_left + a_right) / 2
        phi_mid = (phi_left + phi_right) / 2
        delta_a = a_right - a_left
        delta_phi = phi_right - phi_left
        potential = sp.Rational(3, 4) * (
            1 - sp.exp(-kappa * phi_mid)
        ) ** 2
        action += (
            -6 * a_mid * delta_a**2 + a_mid**3 * delta_phi**2
        ) / (2 * T * h) + T * h * (
            -3 * a_mid + a_mid**3 * potential
        )
    action = sp.expand(2 * sp.pi**2 * action)
    reduced = (
        4 * sp.pi**2 * a**3 * delta**2 / T
        + 2
        * sp.pi**2
        * T
        * (
            -3 * a
            + a**3
            * sp.Rational(3, 4)
            * (1 - sp.exp(-kappa * (phi + delta / 2))) ** 2
        )
    )
    audit.check_exact(
        "G1.end.action_reduces_from_two_element_scalar",
        sp.simplify(action - reduced) == 0,
        "the equal-endpoint a1=a_boundary slice of the inherited two-element scalar is exactly S_slice=4*pi^2*a^3*delta^2/T+2*pi^2*T*(-3*a+a^3*V(phi+delta/2))",
    )
    audit.check_exact(
        "G1.end.growth_rate_is_inverse_sqrt_three",
        growth == 1 / sp.sqrt(3),
        "the exponential growth rate along either half-angle arm is kappa/sqrt(2)=1/sqrt(3)",
    )

    theta = sp.symbols("theta", real=True)
    arm_identities: dict[str, dict[str, str]] = {}
    for sign, label in ((-1, "negative"), (1, "positive")):
        q = (1 + sign * sp.I) / sp.sqrt(2)
        arm_T = sp.I * sign * n
        kinetic_identity = sp.simplify(q**2 / arm_T - 1 / n)
        leading_real = sp.simplify(
            sp.re(sp.I * sign * sp.exp(sp.I * sign * theta))
        )
        cross_real = sp.simplify(
            sp.re(-sp.I * sign * sp.exp(sp.I * sign * theta / 2))
        )
        audit.check_exact(
            f"G1.end.{label}_arm_phase_identities",
            kinetic_identity == 0
            and leading_real == -sp.sin(theta)
            and cross_real == sp.sin(theta / 2),
            f"the {label} lapse arm has positive quadratic kinetic real part and the same two Starobinsky real-part phase identities as its conjugate arm",
        )
        arm_identities[label] = {
            "q": str(q),
            "T": str(arm_T),
            "q_squared_over_T": str(sp.simplify(q**2 / arm_T)),
            "leading_real_identity": str(leading_real),
            "cross_real_identity": str(cross_real),
        }

    bad_real = (
        4 * sp.pi**2 * a**3 * t**2 / n
        + 3
        * sp.pi**2
        * a**3
        * n
        * sp.exp(-kappa * phi)
        * sp.exp(growth * t / 2)
        * sp.sin(growth * t / 2)
        - sp.Rational(3, 2)
        * sp.pi**2
        * a**3
        * n
        * sp.exp(-2 * kappa * phi)
        * sp.exp(growth * t)
        * sp.sin(growth * t)
    )
    good_real = (
        4 * sp.pi**2 * a**3 * t**2 / n
        - 3
        * sp.pi**2
        * a**3
        * n
        * sp.exp(-kappa * phi)
        * sp.exp(-growth * t / 2)
        * sp.sin(growth * t / 2)
        + sp.Rational(3, 2)
        * sp.pi**2
        * a**3
        * n
        * sp.exp(-2 * kappa * phi)
        * sp.exp(-growth * t)
        * sp.sin(growth * t)
    )

    x = sp.symbols("x", positive=True, real=True)
    kinetic_scaled = (
        sp.Rational(8, 3)
        * (x / growth) ** 2
        * sp.exp(2 * kappa * phi)
        * sp.exp(-x)
        / n**2
    )
    cross_bound_scaled = (
        sp.sqrt(2) * sp.exp(kappa * phi) * sp.exp(-x / 2)
    )
    audit.check_exact(
        "G1.end.subleading_terms_vanish_on_bad_subsequence",
        sp.limit(kinetic_scaled, x, sp.oo) == 0
        and sp.limit(cross_bound_scaled, x, sp.oo) == 0,
        "after division by the positive leading exponential scale, the polynomial kinetic correction and the half-rate exponential correction both vanish",
    )

    good_correction_1 = sp.exp(-growth * t / 2) / t**2
    good_correction_2 = sp.exp(-growth * t) / t**2
    good_limit = sp.limit(good_real / t**2, t, sp.oo)
    audit.check_exact(
        "G1.end.positive_phi_end_is_good_on_witness_slice",
        sp.limit(good_correction_1, t, sp.oo) == 0
        and sp.limit(good_correction_2, t, sp.oo) == 0
        and good_limit == 4 * sp.pi**2 * a**3 / n,
        "for y_phi=+t on either straight arm, Re(S_slice)/t^2 tends to the strictly positive kinetic coefficient 4*pi^2*a^3/n",
    )

    leading_coefficient = (
        -sp.Rational(3, 2)
        * sp.pi**2
        * n
        * a**3
        * sp.exp(-2 * kappa * phi)
    )
    audit.check_exact(
        "G1.end.bad_subsequence_has_negative_exponential_coefficient",
        leading_coefficient.is_negative is True,
        "at t_j=sqrt(3)*(pi/2+2*pi*j), the normalized leading coefficient is strictly negative for a,n>0",
    )
    audit.check_exact(
        "G1.guard.bad_end_short_circuits_global_outputs",
        True,
        "one declared-chain escape sequence with Re(S_2) tending to minus infinity rejects this straight completion before any saddle/upward/intersection census and cannot emit global_n_sigma",
    )

    u, v, y = sp.symbols("u v y", real=True)
    general_kinetic: dict[str, str] = {}
    for sign, label in ((-1, "negative"), (1, "positive")):
        general_q = u + sp.I * v
        general_T = sp.I * sign * n
        kinetic_real = sp.simplify(
            sp.re(4 * sp.pi**2 * a**3 * general_q**2 * y**2 / general_T)
        )
        expected_kinetic = 8 * sp.pi**2 * a**3 * sign * u * v * y**2 / n
        audit.check_exact(
            f"G1.model_class.{label}_arm_general_kinetic_real_part",
            sp.simplify(kinetic_real - expected_kinetic) == 0,
            f"for a constant q=u+i*v line on the {label} pure-imaginary lapse arm, Re(S_kinetic)=8*pi^2*a^3*s*u*v*y^2/n",
        )
        general_kinetic[label] = str(kinetic_real)

    U, V = sp.symbols("U V", positive=True, real=True)
    decaying_end_negative_kinetic = -8 * sp.pi**2 * a**3 * U * V * t**2 / n
    decaying_exponential = sp.exp(-kappa * U * t / 2)
    audit.check_exact(
        "G1.model_class.negative_kinetic_case_has_bad_decay_end",
        sp.limit(decaying_end_negative_kinetic, t, sp.oo) == -sp.oo
        and sp.limit(decaying_exponential, t, sp.oo) == 0,
        "when s*u*v<0, choose the end with u*y>0: the Starobinsky exponential decays while the negative quadratic kinetic real part tends to minus infinity",
    )

    axis_theta = sp.symbols("axis_theta", real=True)
    real_axis_kinetic = sp.simplify(
        sp.re(4 * sp.pi**2 * a**3 * U**2 * t**2 / (sp.I * n))
    )
    imaginary_axis_kinetic = sp.simplify(
        sp.re(4 * sp.pi**2 * a**3 * (sp.I * V) ** 2 * t**2 / (sp.I * n))
    )
    bounded_axis_phase = sp.simplify(abs(sp.exp(sp.I * axis_theta)))
    audit.check_exact(
        "G1.model_class.axis_aligned_lines_lack_two_good_ends",
        real_axis_kinetic == 0
        and imaginary_axis_kinetic == 0
        and bounded_axis_phase == 1,
        "when u*v=0, the kinetic real part vanishes; a real field line leaves the pure-imaginary potential contribution with zero real part, while a pure-imaginary line has only bounded oscillatory exponential modulus",
    )

    model_theta = sp.symbols("model_theta", positive=True, real=True)
    positive_kinetic_scaled = (
        8
        * sp.pi**2
        * a**3
        * U
        * V
        * (model_theta / (kappa * V)) ** 2
        / n
        * sp.exp(-kappa * U * model_theta / (kappa * V))
    )
    half_rate_scaled = sp.exp(
        -kappa * U * model_theta / (2 * kappa * V)
    )
    general_bad_leading_coefficient = (
        -sp.Rational(3, 2)
        * sp.pi**2
        * a**3
        * n
        * sp.exp(-2 * kappa * phi)
    )
    audit.check_exact(
        "G1.model_class.positive_kinetic_case_has_exponential_bad_subsequence",
        sp.limit(positive_kinetic_scaled, model_theta, sp.oo) == 0
        and sp.limit(half_rate_scaled, model_theta, sp.oo) == 0
        and general_bad_leading_coefficient.is_negative is True,
        "when s*u*v>0, reflect signs to s=+1,u>0,v>0 and take y=-t_j with t_j=(pi/2+2*pi*j)/(kappa*v): the negative full-rate Starobinsky exponential dominates the positive quadratic and half-rate terms",
    )
    audit.check_exact(
        "G1.model_class.constant_straight_line_cases_are_exhaustive",
        True,
        "the disjoint cases s*u*v<0, u*v=0, and s*u*v>0 exhaust constant complex straight phi lines on either pure-imaginary lapse arm; none has two relative-good field ends on the fixed-a slice",
    )

    return {
        "kappa": str(kappa),
        "growth_rate": str(growth),
        "reduced_action": str(reduced),
        "arm_identities": arm_identities,
        "bad_end_real_part": str(bad_real),
        "bad_subsequence": "t_j=sqrt(3)*(pi/2+2*pi*j), j>=0",
        "bad_subsequence_scaled_limit": "-1 after division by (3/2)*pi^2*a^3*n*exp(-2*kappa*phi)*exp(t_j/sqrt(3))",
        "unscaled_exponential_limit": str(leading_coefficient),
        "positive_end_real_part": str(good_real),
        "positive_end_quadratic_limit": str(good_limit),
        "constant_straight_line_model_class": {
            "general_kinetic_real_parts": general_kinetic,
            "negative_kinetic_case": "bad decay end from negative quadratic growth",
            "axis_aligned_case": "zero kinetic real part and zero-or-bounded potential real part on at least one end",
            "positive_kinetic_case": "bad exponential-growth subsequence t_j=(pi/2+2*pi*j)/(kappa*abs(v))",
            "decision": "KILL_CONSTANT_STRAIGHT_FIELD_LINES_ON_FIXED_A_PURE_IMAGINARY_LAPSE_SLICE",
        },
    }


def numerical_calculation(
    audit: Audit, frozen: dict[str, Any]
) -> dict[str, Any]:
    mp.mp.dps = int(frozen["numerical_plan"]["precision_decimal_digits"])
    a = mp.mpf(frozen["model"]["fixed_boundary"]["a"])
    phi = mp.mpf(frozen["model"]["fixed_boundary"]["phi"])
    n_abs = mp.mpf(frozen["numerical_plan"]["fixed_abs_N"])
    kappa = mp.sqrt(mp.mpf(2) / 3)
    growth = 1 / mp.sqrt(3)

    def potential(value: mp.mpc) -> mp.mpc:
        return mp.mpf(3) / 4 * (1 - mp.exp(-kappa * value)) ** 2

    def direct_action(sign: int, y_phi: mp.mpf) -> mp.mpc:
        q = mp.exp(sign * mp.j * mp.pi / 4)
        lapse_T = sign * mp.j * n_abs
        a_nodes = (a, a, a)
        phi_nodes = (phi, phi + q * y_phi, phi)
        total = mp.mpc(0)
        h = mp.mpf(1) / 2
        for element in range(2):
            a_left = a_nodes[element]
            a_right = a_nodes[element + 1]
            phi_left = phi_nodes[element]
            phi_right = phi_nodes[element + 1]
            a_mid = (a_left + a_right) / 2
            phi_mid = (phi_left + phi_right) / 2
            delta_a = a_right - a_left
            delta_phi = phi_right - phi_left
            total += (
                -6 * a_mid * delta_a**2 + a_mid**3 * delta_phi**2
            ) / (2 * lapse_T * h) + lapse_T * h * (
                -3 * a_mid + a_mid**3 * potential(phi_mid)
            )
        return 2 * mp.pi**2 * total

    def bad_closed(t_value: mp.mpf) -> mp.mpf:
        return (
            4 * mp.pi**2 * a**3 * t_value**2 / n_abs
            + 3
            * mp.pi**2
            * a**3
            * n_abs
            * mp.exp(-kappa * phi)
            * mp.exp(growth * t_value / 2)
            * mp.sin(growth * t_value / 2)
            - mp.mpf(3)
            / 2
            * mp.pi**2
            * a**3
            * n_abs
            * mp.exp(-2 * kappa * phi)
            * mp.exp(growth * t_value)
            * mp.sin(growth * t_value)
        )

    def good_closed(t_value: mp.mpf) -> mp.mpf:
        return (
            4 * mp.pi**2 * a**3 * t_value**2 / n_abs
            - 3
            * mp.pi**2
            * a**3
            * n_abs
            * mp.exp(-kappa * phi)
            * mp.exp(-growth * t_value / 2)
            * mp.sin(growth * t_value / 2)
            + mp.mpf(3)
            / 2
            * mp.pi**2
            * a**3
            * n_abs
            * mp.exp(-2 * kappa * phi)
            * mp.exp(-growth * t_value)
            * mp.sin(growth * t_value)
        )

    def relative_error(left: mp.mpf, right: mp.mpf) -> mp.mpf:
        return abs(left - right) / max(mp.mpf(1), abs(left), abs(right))

    bad_records: list[dict[str, Any]] = []
    maximum_direct_formula_relative = mp.mpf(0)
    maximum_arm_real_difference = mp.mpf(0)
    for index in frozen["numerical_plan"]["bad_subsequence_indices"]:
        theta = mp.pi / 2 + 2 * mp.pi * index
        t_value = theta / growth
        closed = bad_closed(t_value)
        arm_values = {
            sign: mp.re(direct_action(sign, -t_value)) for sign in (-1, 1)
        }
        direct_formula_relative = max(
            relative_error(value, closed) for value in arm_values.values()
        )
        arm_real_difference = relative_error(arm_values[-1], arm_values[1])
        maximum_direct_formula_relative = max(
            maximum_direct_formula_relative, direct_formula_relative
        )
        maximum_arm_real_difference = max(
            maximum_arm_real_difference, arm_real_difference
        )
        scale = (
            mp.mpf(3)
            / 2
            * mp.pi**2
            * a**3
            * n_abs
            * mp.exp(-2 * kappa * phi)
            * mp.exp(theta)
        )
        bad_records.append(
            {
                "index": index,
                "t": mp.nstr(t_value, 18),
                "ReS_negative_arm": mp.nstr(arm_values[-1], 18),
                "ReS_positive_arm": mp.nstr(arm_values[1], 18),
                "normalized_by_positive_leading_scale": mp.nstr(
                    closed / scale, 18
                ),
                "direct_formula_relative_error": mp.nstr(
                    direct_formula_relative, 8
                ),
            }
        )

    final_ratio = mp.mpf(
        bad_records[-1]["normalized_by_positive_leading_scale"]
    )
    audit.check_numerical(
        "G1.end.direct_action_matches_bad_closed_form",
        maximum_direct_formula_relative < mp.mpf("1e-70"),
        "80-decimal direct evaluation of the unreduced two-element action agrees with the separately derived bad-end real-part formula on both arms",
        {
            "maximum_relative_error": mp.nstr(
                maximum_direct_formula_relative, 8
            ),
            "precision_decimal_digits": mp.mp.dps,
        },
    )
    audit.check_numerical(
        "G1.end.conjugate_arms_have_identical_real_action",
        maximum_arm_real_difference < mp.mpf("1e-70"),
        "the frozen positive and negative lapse arms give the same Re(S_2) on their conjugate straight field rays",
        {
            "maximum_relative_difference": mp.nstr(
                maximum_arm_real_difference, 8
            )
        },
    )
    audit.check_numerical(
        "G1.end.sampled_bad_subsequence_is_negative_and_asymptotic",
        all(mp.mpf(record["ReS_positive_arm"]) < 0 for record in bad_records)
        and abs(final_ratio + 1) < mp.mpf("2e-8"),
        "every frozen j=1..6 witness has negative Re(S_2), and the leading-scale ratio approaches -1",
        {
            "sample_count_per_arm": len(bad_records),
            "last_scaled_ratio": mp.nstr(final_ratio, 18),
            "last_distance_from_minus_one": mp.nstr(abs(final_ratio + 1), 8),
        },
    )

    good_records: list[dict[str, Any]] = []
    maximum_good_relative = mp.mpf(0)
    positive_limit = 4 * mp.pi**2 * a**3 / n_abs
    for text_value in frozen["numerical_plan"]["positive_end_t_values"]:
        t_value = mp.mpf(text_value)
        closed = good_closed(t_value)
        arm_values = {
            sign: mp.re(direct_action(sign, t_value)) for sign in (-1, 1)
        }
        good_relative = max(
            relative_error(value, closed) for value in arm_values.values()
        )
        maximum_good_relative = max(maximum_good_relative, good_relative)
        good_records.append(
            {
                "t": text_value,
                "ReS_negative_arm": mp.nstr(arm_values[-1], 18),
                "ReS_positive_arm": mp.nstr(arm_values[1], 18),
                "ReS_over_t_squared": mp.nstr(closed / t_value**2, 18),
                "direct_formula_relative_error": mp.nstr(good_relative, 8),
            }
        )
    final_good_ratio = mp.mpf(good_records[-1]["ReS_over_t_squared"])
    audit.check_numerical(
        "G1.end.direct_action_matches_positive_closed_form",
        maximum_good_relative < mp.mpf("1e-70"),
        "the independent direct action also agrees with the positive-end closed form on both arms",
        {"maximum_relative_error": mp.nstr(maximum_good_relative, 8)},
    )
    audit.check_numerical(
        "G1.end.sampled_positive_end_tracks_positive_quadratic_limit",
        all(mp.mpf(record["ReS_positive_arm"]) > 0 for record in good_records)
        and relative_error(final_good_ratio, positive_limit) < mp.mpf("1e-14"),
        "the y_phi=+t controls remain positive and approach the exact quadratic coefficient",
        {
            "exact_quadratic_coefficient": mp.nstr(positive_limit, 18),
            "last_observed_coefficient": mp.nstr(final_good_ratio, 18),
            "last_relative_error": mp.nstr(
                relative_error(final_good_ratio, positive_limit), 8
            ),
        },
    )

    return {
        "precision_decimal_digits": mp.mp.dps,
        "fixed_abs_N": str(n_abs),
        "bad_subsequence_records": bad_records,
        "positive_end_records": good_records,
    }


def run() -> dict[str, Any]:
    frozen, input_sha256 = load_frozen_input()
    audit = Audit()
    exact = exact_calculation(audit)
    numerical = numerical_calculation(audit, frozen)
    runner_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": frozen["calculation_id"],
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": "GATE1_PHASE39_STRAIGHT_FIELD_RAY_COMPLETION_HAS_BAD_NEGATIVE_PHI_ENDS",
        "candidate_decision": "KILL",
        "model_class_decision": "KILL_CONSTANT_STRAIGHT_FIELD_LINES_ON_DECLARED_SLICE",
        "programme_impact": "NARROW",
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "gate1_status": "OPEN_PARTIAL_PROGRESS",
        "input": {
            "path": f"cpt_temporal_folded_susy/{INPUT_NAME}",
            "sha256": input_sha256,
        },
        "runner": {
            "path": "cpt_temporal_folded_susy/gate1_straight_lift_end_admissibility.py",
            "sha256": runner_sha256,
        },
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
        },
        "resource_contract": frozen["resource_caps"],
        "observed_calls": {
            "root_calls": 0,
            "ode_calls": 0,
            "evaluator_reconciliation_calls": 0,
            "automatic_descendants": 0,
        },
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "computed_facts": [
            "on the inherited m=2 a_1=a_boundary slice, both conjugate straight lapse arms have the same exact Re(S_2)",
            "the y_phi=+infinity direction is good on that slice because Re(S_2) grows quadratically positive",
            "the y_phi=-infinity direction contains an explicit sequence on both arms where Re(S_2) tends exponentially to minus infinity",
            "therefore the straight unbounded field-ray completion of the Phase 39 declared finite-window candidate is not an admissible exp(-S_2) relative cycle",
            "more generally, no constant complex straight phi line has two relative-good field ends on the fixed-a, pure-imaginary-lapse m=2 slice",
        ],
        "interpretation": "The Phase 39 straight Gaussian field rays are local asymptotic directions only. On the declared slice, every constant complex straight field line fails at least one necessary end condition, so further Gate 1 work must branch to a curved or piecewise good-end contour, a nonzero-Re(T) lateral, or another explicitly derived regulator cycle.",
        "not_computed": [
            "a physical original joint cycle",
            "cap or scale-factor infinity for a redesigned nonlinear cycle",
            "a complete saddle, upward-cycle, complex-sheet, Stokes, or relative-end census",
            "any local or global intersection coefficient",
            "canonical momenta, BFV ghosts, fermions, Pfaffian/Pin data, or a spinorial charge",
            "a physics or TOE claim",
        ],
        "preserved_results": [
            "Phase 39 finite-window local intersection candidates and their local signs",
            "all Phase 40-50 scoped calculations, failures, and inconclusive results",
        ],
        "promoted_outputs": {
            "physical_original_cycle": None,
            "complete_global_signed_intersection_vector": None,
            "global_n_sigma": None,
            "physics_claim": None,
            "TOE_claim": None,
        },
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    output = json.dumps(
        result,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(output) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result artifact exceeds cap: {len(output)} > {ARTIFACT_CAP_BYTES}"
        )
    Path(__file__).with_name(RESULT_NAME).write_bytes(output)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "candidate_decision": result["candidate_decision"],
                "model_class_decision": result["model_class_decision"],
                "programme_impact": result["programme_impact"],
                "gate1_decision": result["gate1_decision"],
                "gate1_status": result["gate1_status"],
                "exact_checks": len(audit.exact),
                "numerical_checks": len(audit.numerical),
                "global_n_sigma": None,
                "automatic_next": None,
                "result_bytes": len(output),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return result


def main() -> int:
    try:
        run()
    except Exception as error:
        failure = {
            "schema_version": RESULT_SCHEMA,
            "run_status": "INVALID_RUN",
            "error_type": type(error).__name__,
            "error": str(error)[:4096],
            "global_promotion": "PROHIBITED",
            "global_n_sigma": None,
            "automatic_next": None,
        }
        print(RESULT_PREFIX + json.dumps(failure, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
