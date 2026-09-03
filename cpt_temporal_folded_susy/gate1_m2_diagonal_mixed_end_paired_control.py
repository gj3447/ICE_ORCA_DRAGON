#!/usr/bin/env python3
"""Certify one m=2 diagonal mixed action end with a sign-flipped control.

The declared positive tail sends the scale and scalar differences to infinity
together as x=s and q=s*exp(i*psi/2), with T=rho*exp(i*psi).  Its scalar
kinetic term has an exactly positive s**5 coefficient.  Uniform direct bounds
control the remaining O(s**3) action terms.  The paired x=-s tail is required
to produce the opposite sign and prevents a phase-cancellation sign error from
passing as a positive result.  The original two-element action supplies the
independent high-precision numerical evaluator.

This is an unnumbered bounded current-blocker calculation.  It supplies only
one action-decay entry for an incomplete mixed-end census.  It does not attach
the tail to the compact chain, include an amplitude or measure, complete the
end census, select a source/relative cycle, compute intersections, or emit a
spectral, RAQ, physics or TOE claim.  It writes one adjacent JSON result.
"""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_INPUTS.json"
RESULT_NAME = "GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_m2_diagonal_mixed_end_paired_control.py"
)
EXPECTED_INPUT_SHA256 = (
    "ed4d7835c3672832b522c50b2e774afab161df45163bdd361651ea3ffdc94057"
)
EXPECTED_UPSTREAM_SHA256 = {
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json": (
        "b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4"
    ),
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md": (
        "0872eda0d526a707c3eb28a700ff1209d78a94a600419ee09609ac67d0047b70"
    ),
    "cpt_temporal_folded_susy/GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_INPUTS.json": (
        "aa7021ec68c1910ae458bfbab7cdf13e4d3234ade93fbdbaf9484f6586c270ce"
    ),
    "cpt_temporal_folded_susy/GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_RESULT.json": (
        "36fdf578fc249b154d626b8baa341907c27998562c53d346402009bad45d2930"
    ),
    "cpt_temporal_folded_susy/GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR.md": (
        "1faccd21e39c464fe12b5c1c16b887d96a898c3958680e4071673d21242ae563"
    ),
}
CALCULATION_ID = "Gate1M2DiagonalMixedEndPairedControl"
RESULT_SCHEMA = "ice.gate1-m2-diagonal-mixed-end-paired-control.result.v1"
VERDICT = "KEEP_SCOPED_DIAGONAL_MIXED_ACTION_END_WITH_SIGN_CONTROL"
CONTROL_VERDICT = "KILL_SIGN_FLIPPED_DIAGONAL_MIXED_ACTION_END"
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
        "symbolic_operations": 160,
        "quadratures": 0,
        "root_calls": 0,
        "ode_calls": 0,
        "sampling_points": 54,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "connection_to_compact_phase39_chain": None,
        "tail_amplitude_or_measure_absolute_convergence": None,
        "complete_mixed_end_census": None,
        "all_ratio_or_phase_end_admissibility": None,
        "q_dependent_scale_tail_family": None,
        "admissible_full_joint_completion": None,
        "full_relative_homology_class": None,
        "source_defined_joint_relative_cycle": None,
        "source_to_thimble_deformation": None,
        "physical_original_cycle": None,
        "lapse_infinite_end_admissibility": None,
        "zero_lapse_extension": None,
        "full_joint_orientation": None,
        "absolute_determinant_pfaffian_line": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "singular_endpoint_nonreal_weyl_m": None,
        "spectral_measure": None,
        "RAQ_completion": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    sampling_points: int = 0

    def _reserve(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate check id: {ident}")
        self.seen.add(ident)

    def check_exact(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self._reserve(ident)
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {ident}: {statement}")
        self.exact.append(
            {"id": ident, "passed": True, "statement": statement, **data}
        )

    def check_numerical(
        self, ident: str, passed: bool, statement: str, **data: Any
    ) -> None:
        self._reserve(ident)
        if not passed:
            raise AssertionError(f"[NUMERICAL FAIL] {ident}: {statement}")
        self.numerical.append(
            {"id": ident, "passed": True, "statement": statement, **data}
        )

    def guard(
        self,
        ident: str,
        verified: bool,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self._reserve(ident)
        if not verified:
            raise AssertionError(f"[THEOREM GUARD FAIL] {ident}")
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )

    def count_sample(self) -> None:
        self.sampling_points += 1
        if self.sampling_points > expected_caps()["sampling_points"]:
            raise AssertionError("sampling-point cap exceeded")


def parse_fraction(value: str) -> mp.mpf:
    if "/" not in value:
        return mp.mpf(value)
    numerator, denominator = value.split("/", maxsplit=1)
    return mp.mpf(numerator) / mp.mpf(denominator)


def mp_text(value: mp.mpf | mp.mpc, digits: int = 30) -> str:
    return mp.nstr(value, digits)


def potential_mp(phi_value: mp.mpf | mp.mpc) -> mp.mpf | mp.mpc:
    kappa = mp.sqrt(mp.mpf(2) / 3)
    return mp.mpf(3) / 4 * (1 - mp.exp(-kappa * phi_value)) ** 2


def direct_two_element_action(
    tail_parameter: mp.mpf,
    rho_value: mp.mpf,
    psi_value: mp.mpf,
    x_sign: int,
    a_boundary: mp.mpf,
    phi_boundary: mp.mpf,
) -> tuple[mp.mpc, mp.mpc, mp.mpc]:
    """Evaluate the original action and return action, q**2/T, and V(Phi)."""

    x_value = x_sign * tail_parameter
    q_value = tail_parameter * mp.exp(mp.j * psi_value / 2)
    lapse = rho_value * mp.exp(mp.j * psi_value)
    a_nodes = [a_boundary, a_boundary + x_value, a_boundary]
    phi_nodes = [phi_boundary, phi_boundary + q_value, phi_boundary]
    half = mp.mpf(1) / 2
    total = mp.mpc(0)
    potential_mid = potential_mp(phi_boundary + q_value / 2)
    for index in range(2):
        a_mid = (a_nodes[index] + a_nodes[index + 1]) / 2
        phi_mid = (phi_nodes[index] + phi_nodes[index + 1]) / 2
        delta_a = a_nodes[index + 1] - a_nodes[index]
        delta_phi = phi_nodes[index + 1] - phi_nodes[index]
        potential = potential_mp(phi_mid)
        total += (
            -6 * a_mid * delta_a**2 + a_mid**3 * delta_phi**2
        ) / (2 * lapse * half) + lapse * half * (
            -3 * a_mid + a_mid**3 * potential
        )
    action = 2 * mp.pi**2 * total
    return action, q_value**2 / lapse, potential_mid


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded mixed-end calculation accepts no arguments")

    runner_path = Path(__file__).resolve()
    repo_root = runner_path.parents[1]
    input_raw = runner_path.with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(input_raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {input_sha}"
        )
    cfg = json.loads(input_raw)
    if (
        cfg.get("schema_version")
        != "ice.gate1-m2-diagonal-mixed-end-paired-control.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    decision = cfg.get("decision_table", [{}])[0]
    if (
        decision.get("verdict") != VERDICT
        or decision.get("control_verdict") != CONTROL_VERDICT
    ):
        raise AssertionError("decision-table verdict mutation")
    route = cfg.get("graph_route_review", {})
    if (
        route.get("planner_classification") != "CURRENT_BLOCKER_CANDIDATE"
        or route.get("selected_anchor")
        != "open:gate1-original-cycle-signed-global-intersections"
        or route.get("anti_meandering_checks_passed") is not True
        or route.get("planner_grants_execution_authority") is not False
    ):
        raise AssertionError("graph-route review mutation")
    boundary = cfg.get("ragnarok_boundary", {})
    if not all(
        boundary.get(key) is True
        for key in (
            "does_not_execute_historical_runner",
            "does_not_rename_or_retry_consumed_runner",
            "does_not_reopen_killed_reconciliation",
            "generic_bounded_core_calculation",
        )
    ) or boundary.get("automatic_next") is not None:
        raise AssertionError("Ragnarok boundary mutation")

    upstream_hashes: list[dict[str, str]] = []
    for relpath, expected_hash in EXPECTED_UPSTREAM_SHA256.items():
        observed_hash = sha256_bytes((repo_root / relpath).read_bytes())
        if observed_hash != expected_hash:
            raise AssertionError(
                f"upstream hash mismatch for {relpath}: "
                f"expected {expected_hash}, observed {observed_hash}"
            )
        upstream_hashes.append({"path": relpath, "sha256": observed_hash})

    audit = Audit()
    audit.check_exact(
        "G1.m2.diagonal_mixed.input_hashes_route_scope_and_breaker",
        input_sha == EXPECTED_INPUT_SHA256
        and len(upstream_hashes) == len(EXPECTED_UPSTREAM_SHA256)
        and cfg["required_fail_closed_outputs"]["global_n_sigma"] is None,
        "The input, upstream evidence, current-blocker route, unnumbered scope and fail-closed outputs are hash-pinned.",
        input_sha256=input_sha,
        upstream_count=len(upstream_hashes),
        planner_checkpoint_id=route["planner_checkpoint_id"],
    )

    a = sp.symbols("a", positive=True, real=True)
    x, q, potential_mid = sp.symbols("x q V_Phi")
    lapse = sp.symbols("T", nonzero=True)
    midpoint_a = a + x / 2
    half = sp.Rational(1, 2)
    element_left = 2 * sp.pi**2 * (
        (-6 * midpoint_a * x**2 + midpoint_a**3 * q**2)
        / (2 * lapse * half)
        + lapse * half * (-3 * midpoint_a + midpoint_a**3 * potential_mid)
    )
    element_right = 2 * sp.pi**2 * (
        (-6 * midpoint_a * (-x) ** 2 + midpoint_a**3 * (-q) ** 2)
        / (2 * lapse * half)
        + lapse * half * (-3 * midpoint_a + midpoint_a**3 * potential_mid)
    )
    action = sp.expand(element_left + element_right)
    expected_action = (
        -24 * sp.pi**2 * midpoint_a * x**2 / lapse
        + 4 * sp.pi**2 * midpoint_a**3 * q**2 / lapse
        + 2
        * sp.pi**2
        * lapse
        * (-3 * midpoint_a + midpoint_a**3 * potential_mid)
    )
    audit.check_exact(
        "G1.m2.diagonal_mixed.general_two_element_action",
        sp.simplify(action - expected_action) == 0,
        "The general-q equal-endpoint action is rebuilt from its two elements before a tail is substituted.",
        action=str(expected_action),
    )

    s, rho = sp.symbols("s rho", positive=True, real=True)
    psi = sp.symbols("psi", real=True)
    diagonal_q = s * sp.exp(sp.I * psi / 2)
    diagonal_lapse = rho * sp.exp(sp.I * psi)
    phase_cancelled = sp.simplify(diagonal_q**2 / diagonal_lapse)
    audit.check_exact(
        "G1.m2.diagonal_mixed.scalar_kinetic_phase_cancellation",
        sp.simplify(phase_cancelled - s**2 / rho) == 0,
        "The declared q and T phases cancel exactly: q^2/T=s^2/rho>0.",
        q_squared_over_T=str(phase_cancelled),
    )

    midpoint_plus = a + s / 2
    midpoint_minus = a - s / 2
    scalar_kinetic_plus = sp.expand(
        4 * sp.pi**2 * midpoint_plus**3 * s**2 / rho
    )
    scalar_kinetic_minus = sp.expand(
        4 * sp.pi**2 * midpoint_minus**3 * s**2 / rho
    )
    plus_s5 = sp.expand(scalar_kinetic_plus).coeff(s, 5)
    minus_s5 = sp.expand(scalar_kinetic_minus).coeff(s, 5)
    audit.check_exact(
        "G1.m2.diagonal_mixed.opposite_exact_s5_coefficients",
        sp.simplify(plus_s5 - sp.pi**2 / (2 * rho)) == 0
        and sp.simplify(minus_s5 + sp.pi**2 / (2 * rho)) == 0,
        "The positive diagonal and sign-flipped control have exact opposite s^5 coefficients.",
        positive_diagonal_s5=str(plus_s5),
        sign_flipped_s5=str(minus_s5),
    )
    audit.check_exact(
        "G1.m2.diagonal_mixed.scalar_kinetic_polynomials",
        sp.simplify(
            scalar_kinetic_plus
            - sp.pi**2
            / rho
            * (
                s**5 / 2
                + 3 * a * s**4
                + 6 * a**2 * s**3
                + 4 * a**3 * s**2
            )
        )
        == 0
        and sp.simplify(
            scalar_kinetic_minus
            - sp.pi**2
            / rho
            * (
                -s**5 / 2
                + 3 * a * s**4
                - 6 * a**2 * s**3
                + 4 * a**3 * s**2
            )
        )
        == 0,
        "The full scalar-kinetic polynomials are recorded, so the leading signs are not fitted from samples.",
    )

    a_boundary_exact = sp.Rational("3.5668031935672753")
    phi_boundary_exact = sp.Rational("1.0185809464006637")
    kappa_squared = sp.Rational(2, 3)
    kappa_floor_squared = sp.Rational(16, 25)
    exponent_floor = sp.Rational(4, 5)
    exponential_series_lower = sum(
        exponent_floor**index / sp.factorial(index) for index in range(5)
    )
    potential_bound = sp.Rational(27, 16)
    audit.check_exact(
        "G1.m2.diagonal_mixed.uniform_potential_modulus_bound",
        a_boundary_exact < 4
        and phi_boundary_exact > 1
        and kappa_squared > kappa_floor_squared
        and exponential_series_lower > 2
        and potential_bound
        == sp.Rational(3, 4) * (1 + sp.Rational(1, 2)) ** 2,
        "On the declared sector Re(Phi)>1; exact rational inequalities give |exp(-kappa*Phi)|<1/2 and hence |V(Phi)|<27/16.",
        exp_4_over_5_series_lower=str(exponential_series_lower),
        potential_modulus_strict_upper=str(potential_bound),
    )

    plus_scale_remainder = 24 * sp.Rational(9, 2) * 5
    plus_lapse_linear_remainder = (
        2 * sp.Rational(6, 5) * 3 * sp.Rational(9, 2)
    )
    plus_lapse_potential_remainder = (
        2
        * sp.Rational(6, 5)
        * sp.Rational(9, 2) ** 3
        * potential_bound
    )
    minus_scale_remainder = 24 * sp.Rational(1, 2) * 5
    minus_lapse_remainder = (
        2
        * sp.Rational(6, 5)
        * (
            3 * sp.Rational(1, 2)
            + sp.Rational(1, 2) ** 3 * potential_bound
        )
    )
    audit.check_exact(
        "G1.m2.diagonal_mixed.uniform_remainder_component_ledger",
        plus_scale_remainder == 540
        and plus_lapse_linear_remainder == sp.Rational(162, 5)
        and plus_lapse_potential_remainder == sp.Rational(59049, 160)
        and minus_scale_remainder == 60
        and minus_lapse_remainder == sp.Rational(657, 160),
        "Every scale-kinetic, lapse-linear and bounded-potential remainder constant is reconstructed from the declared envelope and midpoint bounds.",
        plus_scale=str(plus_scale_remainder),
        plus_lapse_linear=str(plus_lapse_linear_remainder),
        plus_lapse_potential=str(plus_lapse_potential_remainder),
        minus_scale=str(minus_scale_remainder),
        minus_lapse=str(minus_lapse_remainder),
    )

    plus_remainder_constant = sp.simplify(
        plus_scale_remainder
        + plus_lapse_linear_remainder
        + plus_lapse_potential_remainder
    )
    plus_threshold = sp.Integer(48)
    plus_normalized_floor = sp.simplify(
        sp.Rational(5, 12)
        - plus_remainder_constant / plus_threshold**2
    )
    audit.check_exact(
        "G1.m2.diagonal_mixed.uniform_positive_bound_constants",
        plus_remainder_constant
        == 540 + sp.Rational(162, 5) + sp.Rational(59049, 160)
        and plus_normalized_floor == sp.Rational(989, 122880)
        and plus_normalized_floor > 0,
        "For s>=48, Re(S_2)/s^5 exceeds the uniform positive floor 989*pi^2/122880.",
        remainder_bound="|Re(S_2-P_plus)| < pi^2*(150633/160)*s^3",
        normalized_real_action_floor=str(plus_normalized_floor),
        threshold=str(plus_threshold),
    )

    minus_remainder_constant = sp.simplify(
        minus_scale_remainder + minus_lapse_remainder
    )
    minus_threshold = sp.Integer(36)
    minus_normalized_ceiling = sp.simplify(
        -sp.Rational(5, 96)
        + minus_remainder_constant / minus_threshold**2
    )
    audit.check_exact(
        "G1.m2.diagonal_mixed.uniform_negative_control_constants",
        minus_remainder_constant
        == 60 + sp.Rational(657, 160)
        and minus_normalized_ceiling == -sp.Rational(181, 69120)
        and minus_normalized_ceiling < 0,
        "For s>=36, Re(S_2)/s^5 is below the uniform negative ceiling -181*pi^2/69120 on the sign-flipped control.",
        remainder_bound="|Re(S_2-P_minus)| < pi^2*(10257/160)*s^3",
        normalized_real_action_ceiling=str(minus_normalized_ceiling),
        threshold=str(minus_threshold),
    )

    audit.check_exact(
        "G1.m2.diagonal_mixed.bounds_are_uniform_in_lapse_envelope",
        sp.Rational(1, 5) > 0
        and sp.Rational(6, 5) < 2
        and plus_threshold >= 1
        and minus_threshold >= 16,
        "The proof uses only rho in [1/5,6/5], |psi|<=pi/2, a_boundary<4 and the two displayed tail thresholds.",
    )

    audit.guard(
        "G1.m2.diagonal_mixed.guard.positive_tail_uniform_good_action_end",
        plus_normalized_floor > 0,
        "Uniform direct real-action lower bound",
        (
            "x=s, q=s*exp(i*psi/2), T=rho*exp(i*psi), s>=48, "
            "rho in [1/5,6/5], |psi|<=pi/2 and exp(-S_2)."
        ),
        (
            "Re(S_2)>=(989*pi^2/122880)*s^5>0, so this one "
            "declared action tail is uniformly good."
        ),
    )
    audit.guard(
        "G1.m2.diagonal_mixed.guard.sign_flipped_control_uniformly_bad",
        minus_normalized_ceiling < 0,
        "Uniform direct real-action upper bound",
        (
            "x=-s with the same q, T and lapse envelope, s>=36; the midpoint "
            "scale is negative but the polynomial action has no T-nonzero divisor there."
        ),
        (
            "Re(S_2)<=(-181*pi^2/69120)*s^5<0, so the paired "
            "control is uniformly bad and detects the expected sign reversal."
        ),
    )
    audit.guard(
        "G1.m2.diagonal_mixed.guard.bound_derivation_scope",
        a_boundary_exact < 4 and phi_boundary_exact > 1,
        "Dominant term plus uniform remainder comparison",
        (
            "The scalar kinetic term is kept exactly. The scale kinetic and "
            "Starobinsky terms are bounded using the finite lapse envelope, "
            "|V|<27/16 and the declared midpoint-scale inequalities."
        ),
        (
            "Only the two declared one-parameter tails are classified; no other "
            "projective ratio, scalar phase or coordinate face is exhausted."
        ),
    )
    audit.guard(
        "G1.m2.diagonal_mixed.guard.not_newton_or_full_relative_homology",
        "Newton" in cfg["declared_conventions"]["newton_polyhedron_exclusion"],
        "Direct tail bound without imported global homology",
        (
            "The phase contains the Starobinsky exponential and no compactification, "
            "normal-crossing divisor, good meromorphic connection or source cycle is supplied."
        ),
        (
            "The words good action end describe the proved real-part bound only; "
            "no Newton theorem, Hien rapid-decay group or Witten thimble basis is inferred."
        ),
    )
    audit.guard(
        "G1.m2.diagonal_mixed.guard.current_blocker_but_no_global_promotion",
        all(
            cfg["required_fail_closed_outputs"][key] is None
            for key in (
                "connection_to_compact_phase39_chain",
                "tail_amplitude_or_measure_absolute_convergence",
                "complete_mixed_end_census",
                "full_relative_homology_class",
                "source_defined_joint_relative_cycle",
                "physical_original_cycle",
                "complete_global_signed_intersection_vector",
                "global_n_sigma",
                "singular_endpoint_nonreal_weyl_m",
                "spectral_measure",
                "RAQ_completion",
                "physics_claim",
                "TOE_claim",
            )
        ),
        "Fail-closed current-blocker contribution",
        "The graph route identifies one scoped action-decay candidate record for the current G1 blocker.",
        (
            "The complete census, connector, amplitude/measure, source/relative cycle, "
            "global intersections and all downstream physics outputs remain null."
        ),
    )

    numerical_cfg = cfg["declared_conventions"]["numerical_cross_check"]
    mp.mp.dps = int(numerical_cfg["precision_digits"])
    a_boundary_mp = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["a_boundary"]
    )
    phi_boundary_mp = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["phi_boundary"]
    )
    max_final_error = mp.mpf(
        numerical_cfg["maximum_final_relative_leading_coefficient_error"]
    )
    max_conjugation_residual = mp.mpf(
        numerical_cfg["maximum_conjugation_residual"]
    )
    plus_c_mp = mp.mpf(150633) / 160
    minus_c_mp = mp.mpf(10257) / 160

    records: list[dict[str, Any]] = []
    action_cache: dict[tuple[str, str, int, int], mp.mpc] = {}
    phase_residuals: list[mp.mpf] = []
    potential_moduli: list[mp.mpf] = []
    plus_scaled_values: list[mp.mpf] = []
    minus_scaled_values: list[mp.mpf] = []
    plus_final_errors: list[mp.mpf] = []
    minus_final_errors: list[mp.mpf] = []
    all_sequences_decrease: list[bool] = []
    bound_margins: list[mp.mpf] = []

    for rho_text in numerical_cfg["rho_values"]:
        rho_value = parse_fraction(rho_text)
        for psi_text in numerical_cfg["psi_over_pi_values"]:
            psi_value = parse_fraction(psi_text) * mp.pi
            for x_sign, branch in ((1, "positive_diagonal"), (-1, "sign_flipped")):
                expected_leading = x_sign * mp.pi**2 / (2 * rho_value)
                sequence: list[dict[str, Any]] = []
                errors: list[mp.mpf] = []
                for tail_parameter_integer in numerical_cfg[
                    "tail_parameter_values"
                ]:
                    audit.count_sample()
                    tail_parameter = mp.mpf(tail_parameter_integer)
                    action_value, q_squared_over_t, potential_value = (
                        direct_two_element_action(
                            tail_parameter,
                            rho_value,
                            psi_value,
                            x_sign,
                            a_boundary_mp,
                            phi_boundary_mp,
                        )
                    )
                    action_cache[
                        (rho_text, psi_text, x_sign, tail_parameter_integer)
                    ] = action_value
                    target_phase_value = tail_parameter**2 / rho_value
                    phase_residual = abs(q_squared_over_t - target_phase_value) / (
                        abs(target_phase_value) or 1
                    )
                    phase_residuals.append(phase_residual)
                    potential_moduli.append(abs(potential_value))
                    scaled_real = mp.re(action_value) / tail_parameter**5
                    relative_error = abs(
                        (scaled_real - expected_leading) / expected_leading
                    )
                    errors.append(relative_error)
                    if x_sign > 0:
                        plus_scaled_values.append(scaled_real)
                        certified_bound = mp.pi**2 * (
                            mp.mpf(5) / 12
                            - plus_c_mp / tail_parameter**2
                        )
                        bound_margin = scaled_real - certified_bound
                    else:
                        minus_scaled_values.append(scaled_real)
                        certified_bound = mp.pi**2 * (
                            -mp.mpf(5) / 96
                            + minus_c_mp / tail_parameter**2
                        )
                        bound_margin = certified_bound - scaled_real
                    bound_margins.append(bound_margin)
                    sequence.append(
                        {
                            "tail_parameter": tail_parameter_integer,
                            "scaled_real_action_over_s5": mp_text(
                                scaled_real, 30
                            ),
                            "expected_leading_coefficient": mp_text(
                                expected_leading, 30
                            ),
                            "relative_leading_coefficient_error": mp_text(
                                relative_error, 20
                            ),
                            "certified_one_sided_bound": mp_text(
                                certified_bound, 30
                            ),
                            "one_sided_bound_margin": mp_text(
                                bound_margin, 20
                            ),
                        }
                    )
                decreases = all(
                    errors[index + 1] < errors[index]
                    for index in range(len(errors) - 1)
                )
                all_sequences_decrease.append(decreases)
                if x_sign > 0:
                    plus_final_errors.append(errors[-1])
                else:
                    minus_final_errors.append(errors[-1])
                records.append(
                    {
                        "rho": rho_text,
                        "psi_over_pi": psi_text,
                        "tail": branch,
                        "x_sign": x_sign,
                        "expected_leading_coefficient": mp_text(
                            expected_leading, 30
                        ),
                        "errors_strictly_decrease": decreases,
                        "sequence": sequence,
                    }
                )

    conjugation_residuals: list[mp.mpf] = []
    for rho_text in numerical_cfg["rho_values"]:
        for x_sign in (1, -1):
            for tail_parameter_integer in numerical_cfg["tail_parameter_values"]:
                negative_arm = action_cache[
                    (rho_text, "-1/2", x_sign, tail_parameter_integer)
                ]
                positive_arm = action_cache[
                    (rho_text, "1/2", x_sign, tail_parameter_integer)
                ]
                scale = max(mp.mpf(1), abs(positive_arm))
                conjugation_residuals.append(
                    abs(negative_arm - mp.conj(positive_arm)) / scale
                )

    audit.check_numerical(
        "G1.m2.diagonal_mixed.direct_phase_cancellation",
        max(phase_residuals) < mp.mpf("1e-75"),
        "Every sampled original-action input has q^2/T=s^2/rho to high precision.",
        maximum_relative_residual=mp_text(max(phase_residuals), 20),
    )
    audit.check_numerical(
        "G1.m2.diagonal_mixed.sampled_potential_clears_exact_bound",
        max(potential_moduli) < mp.mpf(27) / 16,
        "Every directly evaluated Starobinsky midpoint potential clears the exact 27/16 modulus bound.",
        maximum_modulus=mp_text(max(potential_moduli), 30),
    )
    audit.check_numerical(
        "G1.m2.diagonal_mixed.positive_tail_direct_action",
        min(plus_scaled_values) > 0
        and max(plus_final_errors) < max_final_error,
        "All positive-diagonal original-action samples are positive and converge to pi^2/(2rho).",
        minimum_scaled_real_action=mp_text(min(plus_scaled_values), 30),
        maximum_final_relative_error=mp_text(max(plus_final_errors), 20),
    )
    audit.check_numerical(
        "G1.m2.diagonal_mixed.sign_flipped_direct_action",
        max(minus_scaled_values) < 0
        and max(minus_final_errors) < max_final_error,
        "All sign-flipped original-action samples are negative and converge to -pi^2/(2rho).",
        maximum_scaled_real_action=mp_text(max(minus_scaled_values), 30),
        maximum_final_relative_error=mp_text(max(minus_final_errors), 20),
    )
    audit.check_numerical(
        "G1.m2.diagonal_mixed.one_sided_bounds_and_convergence",
        min(bound_margins) > 0 and all(all_sequences_decrease),
        "Every original-action sample lies on the certified side of its one-sided bound and every leading-coefficient error decreases strictly.",
        minimum_bound_margin=mp_text(min(bound_margins), 20),
        sequences=len(all_sequences_decrease),
    )
    audit.check_numerical(
        "G1.m2.diagonal_mixed.conjugation_and_resource_counts",
        max(conjugation_residuals) < max_conjugation_residual
        and audit.sampling_points == expected_caps()["sampling_points"],
        "The two lapse arms are conjugate within the predeclared tolerance and exactly 54 original-action samples are used.",
        maximum_relative_conjugation_residual=mp_text(
            max(conjugation_residuals), 20
        ),
        sampling_points=audit.sampling_points,
    )

    if not all(entry["passed"] for entry in audit.exact + audit.numerical):
        raise AssertionError("not all checks passed")
    if not all(entry["verified"] for entry in audit.theorem_guards):
        raise AssertionError("not all theorem guards passed")

    runner_sha = sha256_bytes(runner_path.read_bytes())
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "result_id": "GATE1_M2_DIAGONAL_MIXED_END_PAIRED_CONTROL_20260903",
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "run_status": "VALID_RUN",
        "verdict": VERDICT,
        "control_verdict": CONTROL_VERDICT,
        "programme_impact": (
            "ONE_SCOPED_MIXED_ACTION_DECAY_RECORD_SUPPORTED; "
            "COMPLETE_CENSUS_AND_SOURCE_CYCLE_OPEN"
        ),
        "scientific_status": {
            "gate1": "OPEN_PARTIAL_PROGRESS",
            "global_promotion": "PROHIBITED",
            "new_physics": False,
        },
        "graph_route_review": cfg["graph_route_review"],
        "scope": {
            "included": [
                "the exact equal-endpoint m=2 action",
                "rho in [1/5,6/5] and psi in [-pi/2,pi/2]",
                "one positive diagonal x=s, q=s*exp(i*psi/2), s>=48",
                "one sign-flipped x=-s control with identical q and T, s>=36",
                "action real-part decay and 54 original-action control samples",
            ],
            "excluded": [
                "attachment or homotopy to the compact Phase-39 chain",
                "amplitude, determinant, measure or absolute integral convergence",
                "all other projective ratios, phases, coordinate faces and lapse endpoints",
                "the complete mixed/end/singularity/Stokes census",
                "a full relative/source cycle, orientation or signed global intersections",
                "Weyl m(z), spectral measure, RAQ, physics or TOE",
            ],
        },
        "exact_calculation": {
            "action": str(expected_action),
            "phase_cancellation": "q^2/T=s^2/rho",
            "positive_scalar_kinetic_polynomial": str(scalar_kinetic_plus),
            "negative_scalar_kinetic_polynomial": str(scalar_kinetic_minus),
            "positive_leading_coefficient": str(plus_s5),
            "negative_control_leading_coefficient": str(minus_s5),
            "potential_modulus_strict_upper": str(potential_bound),
            "positive_tail_bound": (
                "Re(S_2)/s^5 >= pi^2*(5/12-(150633/160)/s^2) "
                ">= 989*pi^2/122880 for s>=48"
            ),
            "negative_control_bound": (
                "Re(S_2)/s^5 <= pi^2*(-5/96+(10257/160)/s^2) "
                "<= -181*pi^2/69120 for s>=36"
            ),
        },
        "checks": {
            "exact": audit.exact,
            "numerical": audit.numerical,
            "theorem_guards": audit.theorem_guards,
            "counts": {
                "exact_passed": len(audit.exact),
                "numerical_passed": len(audit.numerical),
                "theorem_guards_verified": len(audit.theorem_guards),
                "sampling_points": audit.sampling_points,
            },
        },
        "numerical_control": {
            "precision_digits": mp.mp.dps,
            "records": records,
        },
        "computed_facts": [
            "The declared positive diagonal has a uniform Re(S_2)>0 lower bound growing as s^5 on the finite lapse envelope.",
            "The sign-flipped diagonal has a uniform Re(S_2)<0 upper bound decreasing as -s^5 on the same envelope.",
            "The paired direct original-action evaluator reproduces the opposite leading coefficients and lapse-arm conjugation.",
        ],
        "interpretation": [
            "One scoped action-decay candidate can be recorded for the incomplete mixed-end census.",
            "The opposite-sign control reduces the chance that phase cancellation or complex-real-part bookkeeping created a false positive.",
            "One direction is not a connector, a complete census, a relative chain or an intersection number.",
        ],
        "open_problems": [
            "enumerate all weighted scale-scalar ratios, scalar phases and coordinate-face escapes",
            "construct attachments and a homotopy from a source-defined regulated original cycle",
            "include amplitude, determinant/Pfaffian line, measure and lapse endpoint data",
            "complete saddle, singularity, Stokes, upward-cycle and oriented intersection census",
            "keep Weyl, spectral measure, RAQ, observable, likelihood, physics and TOE claims separate",
        ],
        "required_fail_closed_outputs": cfg["required_fail_closed_outputs"],
        "provenance": {
            "command": "./ice run gate1_m2_diagonal_mixed_end_paired_control",
            "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
            "runner": {"path": RUNNER_RELPATH, "sha256": runner_sha},
            "upstream_evidence": upstream_hashes,
            "environment": {
                "python": platform.python_version(),
                "sympy": importlib.metadata.version("sympy"),
                "mpmath": importlib.metadata.version("mpmath"),
                "platform": platform.platform(),
            },
            "resource_caps": cfg["resource_caps"],
        },
        "primary_sources": cfg["primary_sources"],
        "automatic_next": None,
        "integrity": {
            "canonicalization": "UTF-8 JSON, sorted keys, compact separators, allow_nan=false",
        },
    }
    result["integrity"]["canonical_payload_sha256_excluding_digest"] = (
        sha256_bytes(canonical_bytes(result))
    )
    encoded = json.dumps(
        result, indent=2, ensure_ascii=False, allow_nan=False
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result exceeds artifact cap: {len(encoded)}>{ARTIFACT_CAP_BYTES}"
        )
    runner_path.with_name(RESULT_NAME).write_bytes(encoded)

    print("VALID_RUN")
    print(VERDICT)
    print(CONTROL_VERDICT)
    print(f"exact={len(audit.exact)}/{len(audit.exact)}")
    print(f"numerical={len(audit.numerical)}/{len(audit.numerical)}")
    print(
        "theorem_guards="
        f"{len(audit.theorem_guards)}/{len(audit.theorem_guards)}"
    )
    print(f"samples={audit.sampling_points}")
    print("gate1=OPEN_PARTIAL_PROGRESS")
    print("global_promotion=PROHIBITED")
    print("automatic_next=null")


if __name__ == "__main__":
    main()
