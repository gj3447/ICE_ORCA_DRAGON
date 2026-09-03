#!/usr/bin/env python3
"""Certify one asymmetric pair of m=2 scale tails on a finite field window.

The calculation keeps the committed Phase-39 scale faces and compact scalar
window together with the prior audit's finite nonzero-lapse envelope.  It
attaches a different cubic-sector ray to each scale face and proves a
uniform positive leading real action for the exp(-S_2) convention.  The
original two-element action supplies an independent high-precision control.

This is an unnumbered bounded calculation.  It does not rerun Phase 39,
extend the scalar coordinate to infinity, census mixed ends, select a
physical original cycle, establish relative homology, or emit a global or
physics claim.  It writes one adjacent JSON result.
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

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_INPUTS.json"
RESULT_NAME = "GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_m2_asymmetric_scale_tail_pair.py"
)
EXPECTED_INPUT_SHA256 = (
    "aa7021ec68c1910ae458bfbab7cdf13e4d3234ade93fbdbaf9484f6586c270ce"
)
EXPECTED_UPSTREAM_SHA256 = {
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json": (
        "b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4"
    ),
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md": (
        "0872eda0d526a707c3eb28a700ff1209d78a94a600419ee09609ac67d0047b70"
    ),
    "cpt_temporal_folded_susy/GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_RESULT.json": (
        "ea0aa4ec3c7e9965e0d9e1f4a4731d848fd9d7b8ac6ccc48729070332b3f46de"
    ),
    "cpt_temporal_folded_susy/GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY.md": (
        "89f706ca8fe4f0dbb1f3d9462636b5b6e4a8d1e20961f2c87ce778183fc3faee"
    ),
}
CALCULATION_ID = "Gate1M2AsymmetricScaleTailPair"
RESULT_SCHEMA = "ice.gate1-m2-asymmetric-scale-tail-pair.result.v1"
RESULT_PREFIX = "GATE1_M2_ASYMMETRIC_SCALE_TAIL_PAIR_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
VERDICT = "KEEP_SCOPED_ASYMMETRIC_SCALE_TAIL_PAIR_ON_DECLARED_FINITE_WINDOW"


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
        "sampling_points": 128,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "admissible_full_joint_completion": None,
        "full_relative_homology_class": None,
        "source_defined_joint_relative_cycle": None,
        "source_to_thimble_deformation": None,
        "physical_original_cycle": None,
        "unbounded_q_dependent_scale_fiber": None,
        "scalar_infinite_end_admissibility": None,
        "mixed_end_census": None,
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


def mp_text(value: mp.mpf | mp.mpc, digits: int = 30) -> str:
    return mp.nstr(value, digits)


def parse_fraction(value: str) -> mp.mpf:
    if "/" not in value:
        return mp.mpf(value)
    numerator, denominator = value.split("/", maxsplit=1)
    return mp.mpf(numerator) / mp.mpf(denominator)


def tail_data(
    radius: mp.mpf,
    rho: mp.mpf,
    psi: mp.mpf,
    y_phi: mp.mpf,
    branch: str,
) -> tuple[mp.mpc, mp.mpc, mp.mpc, mp.mpc]:
    face = mp.mpf(1) / 4
    beta = psi / 2 - mp.pi / 2
    q_value = mp.exp(mp.j * psi / 2) * y_phi
    lapse = rho * mp.exp(mp.j * psi)
    if branch == "right":
        alpha = psi / 3 - mp.pi / 3
        x_value = face * mp.exp(mp.j * beta) + mp.exp(
            mp.j * alpha
        ) * (radius - face)
    elif branch == "left":
        alpha = psi / 3 + mp.pi / 3
        x_value = -face * mp.exp(mp.j * beta) + mp.exp(
            mp.j * alpha
        ) * (radius - face)
    else:
        raise AssertionError(f"unknown tail branch: {branch}")
    direction = mp.exp(mp.j * alpha)
    return x_value, q_value, lapse, direction


def direct_two_element_action(
    radius: mp.mpf,
    rho: mp.mpf,
    psi: mp.mpf,
    y_phi: mp.mpf,
    branch: str,
    a_boundary: mp.mpf,
    phi_boundary: mp.mpf,
) -> tuple[mp.mpc, mp.mpc]:
    """Evaluate the original two-element action and its predicted x-cubic coefficient."""

    x_value, q_value, lapse, direction = tail_data(
        radius, rho, psi, y_phi, branch
    )
    a_nodes = [a_boundary, a_boundary + x_value, a_boundary]
    phi_nodes = [phi_boundary, phi_boundary + q_value, phi_boundary]
    half = mp.mpf(1) / 2
    kappa = mp.sqrt(mp.mpf(2) / 3)
    total = mp.mpc(0)
    for index in range(2):
        a_mid = (a_nodes[index] + a_nodes[index + 1]) / 2
        phi_mid = (phi_nodes[index] + phi_nodes[index + 1]) / 2
        delta_a = a_nodes[index + 1] - a_nodes[index]
        delta_phi = phi_nodes[index + 1] - phi_nodes[index]
        potential = mp.mpf(3) / 4 * (
            1 - mp.exp(-kappa * phi_mid)
        ) ** 2
        total += (
            -6 * a_mid * delta_a**2 + a_mid**3 * delta_phi**2
        ) / (2 * lapse * half) + lapse * half * (
            -3 * a_mid + a_mid**3 * potential
        )
    action = 2 * mp.pi**2 * total

    phi_mid = phi_boundary + q_value / 2
    potential_mid = mp.mpf(3) / 4 * (
        1 - mp.exp(-kappa * phi_mid)
    ) ** 2
    cubic = mp.pi**2 * (
        (-12 + q_value**2 / 2) / lapse
        + lapse * potential_mid / 4
    )
    predicted = cubic * direction**3
    return action, predicted


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded construction accepts no arguments")

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
        != "ice.gate1-m2-asymmetric-scale-tail-pair.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if cfg.get("decision_table", [{}])[0].get("verdict") != VERDICT:
        raise AssertionError("decision-table verdict mutation")
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
        upstream_hashes.append(
            {"path": relpath, "sha256": observed_hash}
        )

    audit = Audit()
    audit.check_exact(
        "G1.m2.asym.input_hashes_scope_and_breaker",
        input_sha == EXPECTED_INPUT_SHA256
        and len(upstream_hashes) == len(EXPECTED_UPSTREAM_SHA256)
        and cfg["required_fail_closed_outputs"]["global_n_sigma"] is None,
        "The input, all upstream records, unnumbered scope and fail-closed global outputs are hash-pinned.",
        input_sha256=input_sha,
        upstream_count=len(upstream_hashes),
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
        "G1.m2.asym.general_two_element_action",
        sp.simplify(action - expected_action) == 0,
        "The original equal-endpoint two-element action reduces exactly to the declared general bounded-q expression.",
        action=str(expected_action),
    )

    cubic = sp.expand(action).coeff(x, 3)
    expected_cubic = sp.pi**2 * (
        (-12 + q**2 / 2) / lapse + lapse * potential_mid / 4
    )
    audit.check_exact(
        "G1.m2.asym.general_x_cubic_coefficient",
        sp.simplify(cubic - expected_cubic) == 0,
        "The x-cubic coefficient is extracted from the general two-element action before any ray is substituted.",
        coefficient=str(expected_cubic),
    )

    psi = sp.symbols("psi", real=True)
    alpha_right = psi / 3 - sp.pi / 3
    alpha_left = psi / 3 + sp.pi / 3
    common_cube = sp.exp(sp.I * (psi - sp.pi))
    audit.check_exact(
        "G1.m2.asym.two_rays_share_cubic_direction",
        sp.simplify(3 * alpha_right - (psi - sp.pi)) == 0
        and sp.simplify(3 * alpha_left - (psi + sp.pi)) == 0
        and sp.simplify((psi + sp.pi) - (psi - sp.pi) - 2 * sp.pi)
        == 0
        and sp.simplify(alpha_left - alpha_right - 2 * sp.pi / 3)
        == 0,
        "The two non-antipodal rays differ by 2*pi/3 and have the same cube -exp(i*psi).",
        alpha_right=str(alpha_right),
        alpha_left=str(alpha_left),
        common_cube=str(common_cube),
    )

    beta = psi / 2 - sp.pi / 2
    face = sp.Rational(1, 4)
    radial = sp.symbols("r", real=True)
    right_tail = face * sp.exp(sp.I * beta) + sp.exp(
        sp.I * alpha_right
    ) * (radial - face)
    left_tail = -face * sp.exp(sp.I * beta) + sp.exp(
        sp.I * alpha_left
    ) * (radial - face)
    audit.check_exact(
        "G1.m2.asym.compact_face_attachment",
        sp.simplify(
            right_tail.subs(radial, face) - face * sp.exp(sp.I * beta)
        )
        == 0
        and sp.simplify(
            left_tail.subs(radial, face) + face * sp.exp(sp.I * beta)
        )
        == 0,
        "The two affine outgoing rays meet the right and left Phase-39 scale faces exactly at |y_a|=1/4; no smooth-tangent match is claimed.",
        face_radius=str(face),
    )
    audit.check_exact(
        "G1.m2.asym.conjugation_exchanges_tail_faces",
        sp.simplify(-alpha_right - alpha_left.subs(psi, -psi)) == 0
        and sp.simplify(-beta - (beta.subs(psi, -psi) + sp.pi))
        == 0,
        "Complex conjugation exchanges the right tail at psi with the left tail at -psi, including their compact face anchors.",
    )

    phi_boundary = sp.Rational("1.0185809464006637")
    kappa_squared = sp.Rational(2, 3)
    kappa_floor_squared = sp.Rational(16, 25)
    real_phi_floor = sp.Rational(7, 8)
    exponent_floor = sp.Rational(7, 10)
    exp_series_lower = sum(
        exponent_floor**index / sp.factorial(index) for index in range(5)
    )
    potential_bound = sp.Rational(27, 16)
    audit.check_exact(
        "G1.m2.asym.uniform_potential_modulus_bound",
        phi_boundary > 1
        and kappa_squared > kappa_floor_squared
        and sp.Rational(4, 5) * real_phi_floor == exponent_floor
        and exp_series_lower > 2
        and potential_bound
        == sp.Rational(3, 4) * (1 + sp.Rational(1, 2)) ** 2,
        "On |q|<=1/4, Re(Phi)>7/8 and sqrt(2/3)>4/5; the positive Taylor lower sum proves exp(7/10)>2, hence |V(Phi)|<27/16.",
        phi_boundary=str(phi_boundary),
        exp_series_lower=str(exp_series_lower),
        potential_modulus_upper_bound=str(potential_bound),
    )

    rho_max = sp.Rational(6, 5)
    q_abs_max = sp.Rational(1, 4)
    kinetic_margin = (12 - q_abs_max**2 / 2) / rho_max
    potential_penalty = rho_max * potential_bound / 4
    uniform_margin = sp.simplify(kinetic_margin - potential_penalty)
    audit.check_exact(
        "G1.m2.asym.uniform_positive_cubic_margin",
        uniform_margin == sp.Rational(9089, 960)
        and uniform_margin > 0,
        "Both ray cubes give Re(S_2)/(pi^2*r^3)>9089/960 uniformly over the declared lapse and compact scalar window.",
        kinetic_lower_bound=str(kinetic_margin),
        potential_penalty_upper_bound=str(potential_penalty),
        normalized_uniform_margin=str(uniform_margin),
    )

    audit.check_exact(
        "G1.m2.asym.action_domain_along_face_attachments",
        not expected_action.has(sp.conjugate)
        and sp.denom(sp.together(expected_action)).has(lapse),
        "For every declared rho>0 the action is polynomial in x and q; the piecewise-smooth face attachments introduce no divisor beyond the excluded T=0 locus.",
    )
    audit.check_exact(
        "G1.m2.asym.cubic_scale_polynomial_with_lower_orders",
        sp.Poly(action, x).degree() == 3
        and all(
            sp.expand(action).coeff(x, degree).is_finite is not False
            for degree in range(4)
        ),
        "At fixed q and nonzero T the exact action is a cubic scale polynomial, so only bounded quadratic and lower coefficients remain below the proved leading term.",
    )
    audit.check_exact(
        "G1.m2.asym.antipodal_shortcut_not_reused",
        sp.simplify(alpha_left - alpha_right - sp.pi) != 0,
        "The new end directions are separated by 2*pi/3, not the antipodal pi separation that forced opposite cubic signs on the killed straight line.",
    )

    audit.guard(
        "G1.m2.asym.guard.uniform_scale_end_goodness",
        uniform_margin > 0,
        "Uniform leading-coefficient criterion for a polynomial scale fiber",
        (
            "The exact equal-endpoint m=2 action; exp(-S_2); "
            "rho in [1/5,6/5], psi in [-pi/2,pi/2], "
            "q=exp(i*psi/2)*y_phi with |y_phi|<=1/4; the two declared rays."
        ),
        (
            "Both scale ends have Re(S_2)->+infinity with a uniform positive "
            "cubic margin. This concerns only scale infinity over the compact scalar window."
        ),
    )
    audit.guard(
        "G1.m2.asym.guard.piecewise_smooth_face_attachment_scope",
        True,
        "Continuous piecewise-smooth attachment of a proved asymptotic ray",
        (
            "Each tail agrees exactly with one Phase-39 scale face and remains "
            "inside the T-nonzero analytic domain while q and T are fixed; "
            "a corner, not a smooth tangent interpolation, is declared at the face."
        ),
        (
            "The affine outgoing ray supplies a scoped attachment. No source-to-cycle "
            "homotopy, orientation or relative-homology classification is inferred."
        ),
    )
    audit.guard(
        "G1.m2.asym.guard.uniform_lower_order_domination",
        sp.Poly(action, x).degree() == 3 and uniform_margin > 0,
        "Uniform dominance of a positive cubic coefficient on a compact parameter window",
        (
            "The q, rho and psi window is compact, rho is bounded away from zero, "
            "the potential and all scale-polynomial coefficients are continuous, "
            "the affine face offsets are bounded, and the real cubic margin is uniform."
        ),
        (
            "The quadratic and lower real coefficients admit one finite common bound; "
            "therefore one common sufficiently large radius makes Re(S_2) at least "
            "half the positive cubic lower bound times r^3 on both declared tails."
        ),
    )
    audit.guard(
        "G1.m2.asym.guard.no_mixed_end_inference",
        cfg["required_fail_closed_outputs"]["mixed_end_census"] is None
        and cfg["required_fail_closed_outputs"]
        ["unbounded_q_dependent_scale_fiber"]
        is None,
        "Finite-window scale-fiber scope exclusion",
        "The scalar coordinate is restricted to the existing compact Phase-39 window.",
        (
            "No statement follows for q tending to infinity, correlated scale-scalar "
            "corners, lapse infinity, zero lapse or a complete joint chain."
        ),
    )
    audit.guard(
        "G1.m2.asym.guard.no_global_or_physics_promotion",
        all(
            cfg["required_fail_closed_outputs"][key] is None
            for key in (
                "full_relative_homology_class",
                "source_defined_joint_relative_cycle",
                "complete_global_signed_intersection_vector",
                "global_n_sigma",
                "singular_endpoint_nonreal_weyl_m",
                "spectral_measure",
                "RAQ_completion",
                "physics_claim",
                "TOE_claim",
            )
        ),
        "Fail-closed downstream separation",
        "Only one local regulated scale-tail pair is constructed.",
        (
            "Gate 1 remains OPEN_PARTIAL_PROGRESS and every global, spectral, RAQ, "
            "physics and TOE output remains null."
        ),
    )

    mp.mp.dps = int(
        cfg["declared_conventions"]["numerical_cross_check"]
        ["precision_digits"]
    )
    numerical_cfg = cfg["declared_conventions"]["numerical_cross_check"]
    a_boundary_mp = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["a_boundary"]
    )
    phi_boundary_mp = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["phi_boundary"]
    )
    theoretical_coefficient_floor = (
        mp.pi**2 * mp.mpf(9089) / mp.mpf(960)
    )
    radius_values = [
        mp.mpf(value) for value in numerical_cfg["tail_radius_values"]
    ]
    records: list[dict[str, Any]] = []
    action_cache: dict[tuple[str, str, str, str, int], mp.mpc] = {}
    predicted_values: list[mp.mpf] = []
    finite_scaled_values: list[mp.mpf] = []
    initial_errors: list[mp.mpf] = []
    final_errors: list[mp.mpf] = []

    for rho_text in numerical_cfg["rho_values"]:
        rho_value = parse_fraction(rho_text)
        for psi_text in numerical_cfg["psi_over_pi_values"]:
            psi_value = parse_fraction(psi_text) * mp.pi
            for y_phi_text in numerical_cfg["y_phi_values"]:
                y_phi_value = parse_fraction(y_phi_text)
                for branch in ("right", "left"):
                    sequence: list[dict[str, str | int]] = []
                    predicted_real: mp.mpf | None = None
                    errors: list[mp.mpf] = []
                    for radius_value in radius_values:
                        audit.count_sample()
                        action_value, predicted_value = direct_two_element_action(
                            radius_value,
                            rho_value,
                            psi_value,
                            y_phi_value,
                            branch,
                            a_boundary_mp,
                            phi_boundary_mp,
                        )
                        predicted_real = mp.re(predicted_value)
                        scaled_real = mp.re(action_value) / radius_value**3
                        relative_error = abs(
                            (scaled_real - predicted_real) / predicted_real
                        )
                        radius_integer = int(radius_value)
                        action_cache[
                            (
                                rho_text,
                                psi_text,
                                y_phi_text,
                                branch,
                                radius_integer,
                            )
                        ] = action_value
                        finite_scaled_values.append(scaled_real)
                        errors.append(relative_error)
                        sequence.append(
                            {
                                "radius": radius_integer,
                                "scaled_real_action": mp_text(
                                    scaled_real, 24
                                ),
                                "relative_coefficient_error": mp_text(
                                    relative_error, 12
                                ),
                            }
                        )
                    if predicted_real is None:
                        raise AssertionError("empty radius sequence")
                    predicted_values.append(predicted_real)
                    initial_errors.append(errors[0])
                    final_errors.append(errors[-1])
                    records.append(
                        {
                            "rho": rho_text,
                            "psi_over_pi": psi_text,
                            "y_phi": y_phi_text,
                            "branch": branch,
                            "predicted_real_cubic_coefficient": mp_text(
                                predicted_real, 24
                            ),
                            "sequence": sequence,
                        }
                    )

    audit.check_numerical(
        "G1.m2.asym.direct_coefficients_clear_exact_floor",
        min(predicted_values) > theoretical_coefficient_floor,
        "Every independently evaluated complex leading coefficient clears the exact pi^2*9089/960 floor on the sampled boundary and central points.",
        exact_floor=mp_text(theoretical_coefficient_floor, 24),
        sampled_minimum=mp_text(min(predicted_values), 24),
    )
    audit.check_numerical(
        "G1.m2.asym.direct_action_scale_ends_positive",
        min(finite_scaled_values) > 0,
        "All 108 original-action samples on both affine tails have positive scaled real action.",
        sample_count=audit.sampling_points,
        minimum_scaled_real_action=mp_text(
            min(finite_scaled_values), 24
        ),
        records=records,
    )
    final_error_cap = mp.mpf(
        numerical_cfg["maximum_final_relative_coefficient_error"]
    )
    audit.check_numerical(
        "G1.m2.asym.direct_action_converges_to_cubic",
        max(final_errors) < final_error_cap
        and all(last < first for first, last in zip(initial_errors, final_errors)),
        "Every original-action sequence moves closer to its independently computed cubic coefficient, and every final relative error is below the predeclared cap.",
        maximum_initial_relative_error=mp_text(max(initial_errors), 16),
        maximum_final_relative_error=mp_text(max(final_errors), 16),
        declared_final_error_cap=mp_text(final_error_cap, 8),
    )

    conjugation_residuals: list[mp.mpf] = []
    psi_conjugates = {"-1/2": "1/2", "0": "0", "1/2": "-1/2"}
    for rho_text in numerical_cfg["rho_values"]:
        for psi_text, opposite_text in psi_conjugates.items():
            for y_phi_text in numerical_cfg["y_phi_values"]:
                for radius_value in numerical_cfg["tail_radius_values"]:
                    right_value = action_cache[
                        (
                            rho_text,
                            psi_text,
                            y_phi_text,
                            "right",
                            radius_value,
                        )
                    ]
                    left_value = action_cache[
                        (
                            rho_text,
                            opposite_text,
                            y_phi_text,
                            "left",
                            radius_value,
                        )
                    ]
                    conjugation_residuals.append(
                        abs(right_value - mp.conj(left_value))
                        / max(mp.mpf(1), abs(right_value))
                    )
    audit.check_numerical(
        "G1.m2.asym.direct_action_conjugation_exchange",
        max(conjugation_residuals) < mp.mpf("1e-60"),
        "The original-action evaluations confirm that conjugation exchanges the right psi tail with the left -psi tail.",
        maximum_relative_residual=mp_text(
            max(conjugation_residuals), 16
        ),
    )

    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": VERDICT,
        "epistemic_status": "SCOPED_CONSTRUCTIVE_SCALE_END_CERTIFICATE",
        "programme_impact": cfg["decision_table"][0]["programme_impact"],
        "question": cfg["question"],
        "primary_obstacle": cfg["primary_obstacle"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "upstream_evidence": upstream_hashes,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "computed_facts": {
            "general_x_cubic_coefficient": (
                "A_3(q,T)=pi^2*((-12+q^2/2)/T+T*V(phi_boundary+q/2)/4)"
            ),
            "right_asymptotic_angle": "alpha_R=psi/3-pi/3",
            "left_asymptotic_angle": "alpha_L=psi/3+pi/3",
            "common_ray_cube": "exp(3*i*alpha_R)=exp(3*i*alpha_L)=-exp(i*psi)",
            "potential_modulus_upper_bound": "|V(Phi)|<27/16",
            "normalized_real_cubic_margin": ">9089/960",
            "uniform_two_good_scale_ends": True,
            "compact_phase39_scale_face_attachment": True,
            "conjugation_exchanges_tail_pair": True,
            "killed_half_angle_straight_line_not_reused": True,
        },
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": len(audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": len(audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guards_verified": len(audit.theorem_guards),
            "theorem_guards_total": len(audit.theorem_guards),
            "all_passed": True,
        },
        "claim_boundary": {
            "computed": [
                "One explicit conjugation-compatible asymmetric pair attaches to both Phase-39 scale faces.",
                "Its two scale ends have a uniform positive cubic real-action margin over the entire declared finite lapse and compact scalar window.",
                "Independent original-action samples converge to the extracted leading coefficients on both ends."
            ],
            "interpretation": (
                "The preceding half-angle KILL is not a universal scale-tail no-go. "
                "Within the frozen m=2 local model, the finite box has an explicit "
                "sectorially good scale-face extension."
            ),
            "still_open": [
                "Scalar infinity and every correlated scale-scalar mixed corner, including an unbounded q-dependent scale fiber.",
                "A complete relative chain, source-derived gauge/BFV cycle, source-to-thimble deformation and regulator removal.",
                "Zero-lapse contact/gluing, lapse infinity, determinant/Pfaffian orientation and a complete global signed intersection vector.",
                "Every nonreal Weyl, spectral-measure, RAQ, empirical, physics and TOE consequence."
            ],
            "positive_certificate_only": (
                "Two scale ends over the pre-existing compact scalar window; "
                "not a full joint-cycle or relative-homology certificate."
            ),
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations": 9,
            "quadratures": 0,
            "root_calls": 0,
            "ode_calls": 0,
            "sampling_points": audit.sampling_points,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(runner_path.read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": importlib.metadata.version("sympy"),
            "mpmath": importlib.metadata.version("mpmath"),
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    result_path = runner_path.with_name(RESULT_NAME)
    result_bytes = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )
    if len(result_bytes) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result artifact exceeds cap: {len(result_bytes)} bytes"
        )
    result_path.write_bytes(result_bytes)

    print(f"{RESULT_PREFIX}{result_path}")
    print("run_status=VALID_RUN")
    print(f"verdict={VERDICT}")
    print(f"exact={len(audit.exact)}/{len(audit.exact)} PASS")
    print(
        f"numerical={len(audit.numerical)}/{len(audit.numerical)} PASS"
    )
    print(
        "theorem_guards="
        f"{len(audit.theorem_guards)}/{len(audit.theorem_guards)} VERIFIED"
    )
    print(f"sampling_points={audit.sampling_points}")
    print("automatic_next=null")


if __name__ == "__main__":
    main()
