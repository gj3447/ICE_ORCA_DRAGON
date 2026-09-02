#!/usr/bin/env python3
"""Falsify one natural product scale completion of the Phase-39 m=2 cap.

The calculation keeps the committed Phase-39 half-angle scale-factor line
and restricts to q=0, a central scalar slice retained by both that cap and
the later compact-bent scalar construction.  It derives the exact cubic
real-part coefficient on the finite nonzero-lapse domain and asks whether
both scale ends can be relative-good for the exp(-S_2) convention.

This is an unnumbered bounded calculation.  It does not rerun Phase 39,
construct a source-defined joint cycle, exhaust alternative scale tails or
mixed ends, compute a global intersection integer, or emit a physics claim.
It writes one adjacent JSON result.
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


INPUT_NAME = "GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_INPUTS.json"
RESULT_NAME = "GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_m2_scale_half_angle_end_admissibility.py"
)
EXPECTED_INPUT_SHA256 = (
    "09c9e20caad28dcde82e2b7bde318f2fb9901b850786ea9b2238af0ce156234c"
)
EXPECTED_UPSTREAM_SHA256 = {
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION_INPUTS.json": (
        "b9c36c3bfeaa63722d90d931b2e961fefd00d9b6c334f4d7e519344d467abab4"
    ),
    "cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md": (
        "0872eda0d526a707c3eb28a700ff1209d78a94a600419ee09609ac67d0047b70"
    ),
    "cpt_temporal_folded_susy/GATE1_PHASE_LOCKED_AFFINE_FIELD_END_CONSTRUCTION.md": (
        "be9d0583a7ff3599f04bf0f8c92c3dea694cf1595b15c9a5c438e789b150cd6c"
    ),
    "cpt_temporal_folded_susy/GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_RESULT.json": (
        "ddfd366af3bf8dba308c8299ac690a9aaf64d0983447b6e6a2cdf52771a18d17"
    ),
}
CALCULATION_ID = "Gate1M2ScaleHalfAngleEndAdmissibility"
RESULT_SCHEMA = "ice.gate1-m2-scale-half-angle-end-admissibility.result.v1"
RESULT_PREFIX = "GATE1_M2_SCALE_HALF_ANGLE_END_ADMISSIBILITY_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
VERDICT = (
    "KILL_PHASE39_HALF_ANGLE_PRODUCT_SCALE_RAY_COMPLETION_"
    "ON_DECLARED_FINITE_LAPSE_DOMAIN"
)


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
        "symbolic_operations": 128,
        "quadratures": 0,
        "root_calls": 0,
        "ode_calls": 0,
        "sampling_points": 32,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "admissible_full_joint_completion": None,
        "source_defined_joint_relative_cycle": None,
        "source_to_thimble_deformation": None,
        "physical_original_cycle": None,
        "mixed_end_census": None,
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


def direct_two_element_action(
    y_value: mp.mpf,
    rho_value: mp.mpf,
    psi_value: mp.mpf,
    a_boundary: mp.mpf,
    phi_boundary: mp.mpf,
) -> mp.mpc:
    """Evaluate the original two-element formula, not its cubic reduction."""

    half = mp.mpf("0.5")
    ray = mp.exp(mp.j * (psi_value / 2 - mp.pi / 2))
    a_nodes = [a_boundary, a_boundary + ray * y_value, a_boundary]
    phi_nodes = [phi_boundary, phi_boundary, phi_boundary]
    lapse = rho_value * mp.exp(mp.j * psi_value)
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
    return 2 * mp.pi**2 * total


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded audit accepts no arguments")

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
        != "ice.gate1-m2-scale-half-angle-end-admissibility.input.v1"
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
        raise AssertionError("Ragnarok execution boundary mutation")

    declared_upstream = {
        item["path"]: item["sha256"] for item in cfg["upstream_evidence"]
    }
    if declared_upstream != EXPECTED_UPSTREAM_SHA256:
        raise AssertionError("upstream manifest mutation")
    upstream_hashes: list[dict[str, str]] = []
    for relative_path, expected_sha in EXPECTED_UPSTREAM_SHA256.items():
        observed_sha = sha256_bytes((repo_root / relative_path).read_bytes())
        if observed_sha != expected_sha:
            raise AssertionError(
                f"upstream hash mismatch for {relative_path}: {observed_sha}"
            )
        upstream_hashes.append(
            {"path": relative_path, "sha256": observed_sha}
        )

    p39_input = json.loads(
        (repo_root / next(iter(EXPECTED_UPSTREAM_SHA256))).read_bytes()
    )
    candidate = p39_input["declared_original_cycle_candidate"]
    if (
        p39_input["model"]["segment_count"] != 2
        or p39_input["model"]["complex_dimension"] != 3
        or candidate["cap_radii"] != [0.3, 0.2]
        or candidate["finite_arm_cutoff_R"] != 1.2
        or candidate["relative_homology_class_proved"] is not False
        or candidate["uniform_good_end_decay_proved"] is not False
        or "exp(i*(psi/2-pi/2))*y_a" not in candidate["cap_embedding"]
    ):
        raise AssertionError("Phase-39 action or candidate semantics drift")
    incidence = json.loads(
        (
            repo_root
            / "cpt_temporal_folded_susy/GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_RESULT.json"
        ).read_bytes()
    )
    counts = incidence["independent_software_verification"]["baseline"][
        "recomputed_counts"
    ]
    if (
        incidence.get("run_status") != "VALID_RUN"
        or incidence.get("ledger_verdict") != "INCOMPLETE"
        or counts
        != {"INTEGER": 0, "OUT_OF_SCOPE": 2, "UNRESOLVED": 12, "total": 14}
    ):
        raise AssertionError("incidence-ledger boundary drift")
    phase_locked_text = (
        repo_root
        / "cpt_temporal_folded_susy/GATE1_PHASE_LOCKED_AFFINE_FIELD_END_CONSTRUCTION.md"
    ).read_text(encoding="utf-8")
    if (
        "Phase-39의 중앙 field window를 정확히 유지" not in phase_locked_text
        or "\\delta_\\psi=e^{i\\psi/2}y_\\phi" not in phase_locked_text
    ):
        raise AssertionError("phase-locked central-window semantics drift")

    if importlib.metadata.version("sympy") != "1.14.0":
        raise AssertionError("SymPy runtime version drift")
    if importlib.metadata.version("mpmath") != "1.3.0":
        raise AssertionError("mpmath runtime version drift")

    audit = Audit()
    audit.check_exact(
        "G1.m2.scale.upstream_hashes_and_scope",
        len(upstream_hashes) == 4 and counts["UNRESOLVED"] == 12,
        "The committed Phase-39 action/candidate, scalar central-window construction and fail-closed incidence ledger match their exact hashes and scoped states.",
        upstream=upstream_hashes,
    )

    a = sp.symbols("a", positive=True, real=True)
    potential = sp.symbols("V_0", nonnegative=True, real=True)
    rho = sp.symbols("rho", positive=True, real=True)
    psi, y = sp.symbols("psi y", real=True)
    half = sp.Rational(1, 2)
    ray = sp.sin(psi / 2) - sp.I * sp.cos(psi / 2)
    displacement = ray * y
    midpoint = a + displacement / 2
    lapse = rho * (sp.cos(psi) + sp.I * sp.sin(psi))
    one_element = (
        -6 * midpoint * displacement**2
    ) / (2 * lapse * half) + lapse * half * (
        -3 * midpoint + midpoint**3 * potential
    )
    original_two_element_action = 2 * sp.pi**2 * (
        one_element + one_element
    )
    reduced_action = (
        -24 * sp.pi**2 * midpoint * displacement**2 / lapse
        + 2
        * sp.pi**2
        * lapse
        * (-3 * midpoint + midpoint**3 * potential)
    )
    audit.check_exact(
        "G1.m2.scale.two_element_action_reduction",
        bool(sp.simplify(original_two_element_action - reduced_action) == 0),
        "The original equal-endpoint two-element action reduces exactly on q=0 to the single midpoint polynomial used for the asymptotic audit.",
        reduced_action=str(reduced_action),
    )

    y_phi = sp.symbols("y_phi", real=True)
    cap_scalar = sp.exp(sp.I * psi / 2) * y_phi
    audit.check_exact(
        "G1.m2.scale.central_q_zero_slice",
        bool(sp.simplify(cap_scalar.subs(y_phi, 0)) == 0),
        "The q=0 slice is exactly y_phi=0 in the Phase-39 cap and lies in the central window retained by the compact-bent scalar contour.",
    )

    complex_cubic = sp.expand(reduced_action).coeff(y, 3)
    real_cubic = sp.trigsimp(sp.simplify(sp.re(sp.expand_complex(complex_cubic))))
    expected_cubic = sp.pi**2 * (
        12 * sp.sin(psi / 2) / rho
        - potential * rho * sp.sin(5 * psi / 2) / 4
    )
    audit.check_exact(
        "G1.m2.scale.cubic_real_coefficient",
        bool(sp.trigsimp(sp.simplify(real_cubic - expected_cubic)) == 0),
        "The real action has the declared cubic scale coefficient L(psi,rho).",
        coefficient=str(expected_cubic),
    )
    audit.check_exact(
        "G1.m2.scale.cubic_coefficient_oddness",
        bool(
            sp.trigsimp(
                sp.simplify(expected_cubic.subs(psi, -psi) + expected_cubic)
            )
            == 0
        ),
        "The cubic coefficient is odd in the lapse phase, so the bad scale end is exchanged by conjugation.",
    )

    angle = sp.symbols("u", real=True)
    five_angle_identity = sp.trigsimp(
        sp.expand_trig(5 * sp.sin(angle) - sp.sin(5 * angle))
        - 4 * sp.sin(angle) ** 3 * (5 - 4 * sp.sin(angle) ** 2)
    )
    audit.check_exact(
        "G1.m2.scale.five_angle_sign_identity",
        bool(sp.simplify(five_angle_identity) == 0),
        "The exact five-angle identity bounds sin(5u) by 5 sin(u) on 0<u<=pi/4 without a sampled trigonometric sign inference.",
    )

    rho_max = sp.Rational(6, 5)
    potential_max = sp.Rational(3, 4)
    positive_phase_margin = sp.simplify(
        12 / rho_max - 5 * potential_max * rho_max / 4
    )
    audit.check_exact(
        "G1.m2.scale.uniform_positive_phase_margin",
        bool(positive_phase_margin == sp.Rational(71, 8)),
        "The pinned rho and potential bounds leave a strict 71/8 coefficient margin in the positive-phase cubic sign proof.",
        margin=str(positive_phase_margin),
    )

    center_action = sp.expand_complex(reduced_action.subs(psi, 0))
    center_quadratic = sp.simplify(sp.re(center_action).expand().coeff(y, 2))
    expected_center_quadratic = sp.pi**2 * a * (
        24 / rho - 3 * rho * potential / 2
    )
    center_margin = sp.simplify(
        24 / rho_max - 3 * rho_max * potential_max / 2
    )
    audit.check_exact(
        "G1.m2.scale.center_quadratic_goodness",
        bool(
            sp.simplify(center_quadratic - expected_center_quadratic) == 0
            and center_margin == sp.Rational(373, 20)
        ),
        "At psi=0 the cubic real part vanishes, but both scale ends are quadratically good with a uniform bracket margin 373/20.",
        coefficient=str(expected_center_quadratic),
        bracket_margin=str(center_margin),
    )

    positive_arm_coefficient = sp.simplify(
        expected_cubic.subs(psi, sp.pi / 2)
    )
    negative_arm_coefficient = sp.simplify(
        expected_cubic.subs(psi, -sp.pi / 2)
    )
    expected_positive_arm = sp.pi**2 / sp.sqrt(2) * (
        12 / rho + potential * rho / 4
    )
    audit.check_exact(
        "G1.m2.scale.opposite_arm_bad_ends",
        bool(
            sp.simplify(positive_arm_coefficient - expected_positive_arm) == 0
            and sp.simplify(negative_arm_coefficient + expected_positive_arm)
            == 0
        ),
        "On the positive lapse arm y->-infinity is bad, while on the negative arm y->+infinity is bad, with the same strict cubic magnitude.",
        positive_arm_cubic=str(expected_positive_arm),
        negative_arm_cubic=str(-expected_positive_arm),
    )

    audit.check_exact(
        "G1.m2.scale.local_sign_not_global_integer",
        incidence["required_fail_closed_outputs"][
            "complete_global_signed_intersection_vector"
        ]
        is None
        and incidence["required_fail_closed_outputs"]["global_n_sigma"]
        is None,
        "A failed scale-end prerequisite leaves every recorded local +1 separate from a global intersection integer.",
    )

    numeric_cfg = cfg["declared_conventions"]["numerical_cross_check"]
    mp.mp.dps = int(numeric_cfg["precision_digits"])
    a_value = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["a_boundary"]
    )
    phi_value = mp.mpf(
        cfg["declared_conventions"]["boundary_values"]["phi_boundary"]
    )
    kappa_value = mp.sqrt(mp.mpf(2) / 3)
    potential_value = mp.mpf(3) / 4 * (
        1 - mp.exp(-kappa_value * phi_value)
    ) ** 2
    audit.check_numerical(
        "G1.m2.scale.benchmark_potential_bound",
        bool(mp.mpf(0) < potential_value < mp.mpf(3) / 4),
        "The frozen positive boundary field gives a benchmark Starobinsky potential strictly between zero and 3/4.",
        V_0=mp_text(potential_value),
    )

    test_pairs: list[tuple[str, mp.mpf, mp.mpf]] = []
    for rho_text in numeric_cfg["rho_values"]:
        numerator, denominator = rho_text.split("/")
        rho_value = mp.mpf(numerator) / mp.mpf(denominator)
        test_pairs.extend(
            [
                (f"rho={rho_text},psi=-pi/2", rho_value, -mp.pi / 2),
                (f"rho={rho_text},psi=+pi/2", rho_value, mp.pi / 2),
            ]
        )
    rho_interior = mp.mpf(3) / 10
    test_pairs.extend(
        [
            ("rho=3/10,psi=-pi/4", rho_interior, -mp.pi / 4),
            ("rho=3/10,psi=+pi/4", rho_interior, mp.pi / 4),
        ]
    )
    tolerance = mp.mpf(
        numeric_cfg["maximum_final_relative_coefficient_error"]
    )
    asymptotic_records: list[dict[str, Any]] = []
    symmetry_values: dict[tuple[str, str, int], mp.mpf] = {}
    all_direct_negative = True
    all_final_close = True
    all_improved = True
    for label, rho_value, psi_value in test_pairs:
        predicted = mp.pi**2 * (
            12 * mp.sin(psi_value / 2) / rho_value
            - potential_value
            * rho_value
            * mp.sin(5 * psi_value / 2)
            / 4
        )
        bad_sign = -1 if psi_value > 0 else 1
        target = -abs(predicted)
        values: list[dict[str, str]] = []
        errors: list[mp.mpf] = []
        for t_integer in numeric_cfg["t_values"]:
            t_value = mp.mpf(t_integer)
            action = direct_two_element_action(
                bad_sign * t_value,
                rho_value,
                psi_value,
                a_value,
                phi_value,
            )
            normalized = mp.re(action) / t_value**3
            relative_error = abs(normalized - target) / abs(target)
            audit.count_sample()
            all_direct_negative = all_direct_negative and normalized < 0
            values.append(
                {
                    "t": str(t_integer),
                    "ReS_over_t_cubed": mp_text(normalized),
                    "relative_error": mp_text(relative_error),
                }
            )
            errors.append(relative_error)
            phase_key = "positive" if psi_value > 0 else "negative"
            symmetry_values[(mp_text(rho_value, 10), phase_key, t_integer)] = (
                normalized
            )
        all_final_close = all_final_close and errors[-1] < tolerance
        all_improved = all_improved and errors[-1] < errors[0]
        asymptotic_records.append(
            {
                "label": label,
                "predicted_bad_cubic_coefficient": mp_text(target),
                "samples": values,
            }
        )
    audit.check_numerical(
        "G1.m2.scale.direct_action_bad_end_asymptotics",
        bool(all_direct_negative and all_final_close and all_improved),
        "An independent 80-digit evaluation of the original two-element action approaches the exact negative cubic coefficient on both arms and two interior cap phases.",
        records=asymptotic_records,
        final_relative_tolerance=mp_text(tolerance),
    )

    symmetry_residuals: list[mp.mpf] = []
    for rho_text in numeric_cfg["rho_values"]:
        numerator, denominator = rho_text.split("/")
        rho_key = mp_text(mp.mpf(numerator) / mp.mpf(denominator), 10)
        for t_integer in numeric_cfg["t_values"]:
            symmetry_residuals.append(
                abs(
                    symmetry_values[(rho_key, "positive", t_integer)]
                    - symmetry_values[(rho_key, "negative", t_integer)]
                )
            )
    audit.check_numerical(
        "G1.m2.scale.arm_conjugation_control",
        bool(max(symmetry_residuals) < mp.mpf("1e-70")),
        "Conjugate lapse arms with their opposite bad y directions have the same directly evaluated real action coefficient.",
        maximum_absolute_residual=mp_text(max(symmetry_residuals)),
    )

    exact_sign_ready = all(item["passed"] for item in audit.exact)
    numerical_ready = all(item["passed"] for item in audit.numerical)
    audit.guard(
        "G1.m2.scale.guard.nonzero_phase_sign_theorem",
        verified=bool(
            exact_sign_ready
            and positive_phase_margin > 0
            and center_margin > 0
        ),
        theorem=(
            "For u=psi/2 in (0,pi/4], "
            "5*sin(u)-sin(5u)=4*sin(u)^3*(5-4*sin(u)^2)>0."
        ),
        hypotheses=(
            "0<rho<=6/5, 0<=V_0<3/4 and the exact Phase-39 "
            "half-angle scale line on q=0."
        ),
        conclusion_and_scope=(
            "L(psi,rho)>0 for psi>0 and L<0 for psi<0. "
            "The conclusion concerns only this declared scale line."
        ),
    )
    audit.guard(
        "G1.m2.scale.guard.relative_good_end_failure",
        verified=bool(exact_sign_ready and numerical_ready),
        theorem=(
            "In the exp(-S_2) relative-cycle convention, every noncompact "
            "end of the declared integration chain must enter Re(S_2)->+infinity."
        ),
        hypotheses=(
            "For every nonzero declared psi, the exact cubic term sends "
            "one of y->+/-infinity to Re(S_2)->-infinity."
        ),
        conclusion_and_scope=(
            "The Phase-39 half-angle scale line is not a two-good-ended "
            "product completion retaining q=0 over the finite nonzero-lapse "
            "cap and arms."
        ),
    )
    audit.guard(
        "G1.m2.scale.guard.central_slice_short_circuits_product_completion",
        verified=bool(exact_sign_ready),
        theorem=(
            "A claimed uniform product or fiber completion that retains a "
            "central slice fails if that slice contains a non-relative-good end."
        ),
        hypotheses=(
            "q=0 is y_phi=0 in the Phase-39 cap and is retained in the "
            "central window of the compact-bent scalar construction."
        ),
        conclusion_and_scope=(
            "Adding the known scalar good tails cannot rescue this unchanged "
            "half-angle scale line; arbitrary fibered mixed contours are untested."
        ),
    )
    audit.guard(
        "G1.m2.scale.guard.no_universal_scale_cycle_no_go",
        verified=True,
        theorem=(
            "A counterexample to one declared chain family excludes only that family."
        ),
        hypotheses=(
            "No asymmetric cubic-sector scale rays, q-dependent scale fibers, "
            "full mixed-corner census, gauge/BFV source or determinant line is tested."
        ),
        conclusion_and_scope=(
            "The result does not prove that no source-defined joint relative "
            "cycle exists and does not alter the two recorded local +1 signs."
        ),
    )

    if not all(item["verified"] for item in audit.theorem_guards):
        raise AssertionError("theorem guards did not close")

    verdict = VERDICT
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "epistemic_status": "SCOPED_FALSIFIER_OF_ONE_NATURAL_SCALE_COMPLETION",
        "programme_impact": cfg["decision_table"][0]["programme_impact"],
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "upstream_evidence": upstream_hashes,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "computed_facts": {
            "cubic_real_coefficient": (
                "L(psi,rho)=pi^2*(12*sin(psi/2)/rho"
                "-(V_0*rho/4)*sin(5*psi/2))"
            ),
            "positive_phase": "L>0; y->-infinity is bad",
            "negative_phase": "L<0; y->+infinity is bad",
            "zero_phase": (
                "L=0 and Re(S_2)/y^2 tends to "
                "pi^2*a*(24/rho-3*rho*V_0/2)>0"
            ),
            "uniform_two_good_ends": False,
            "phase39_half_angle_product_scale_ray_completion": "KILL",
            "phase39_local_intersection_signs_retained": [1, 1],
            "alternative_asymmetric_or_fibered_scale_tails": "OPEN_NOT_TESTED",
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
                "The exact Phase-39 half-angle scale line has one cubic bad end at every nonzero lapse phase on the q=0 central slice.",
                "At the isolated psi=0 slice both scale ends are quadratically good, but this does not give uniform cap admissibility.",
                "The direct original-action controls reproduce the exact bad coefficients on the two arms and at two interior cap phases."
            ],
            "interpretation": (
                "Conditional on retaining q=0 as a product slice, the natural "
                "infinite extension of the existing local cap cannot supply "
                "its missing scale-factor boundary faces."
            ),
            "still_open": [
                "Asymmetric cubic-sector or q-dependent fibered scale tails and the complete mixed-end census.",
                "A source-derived gauge/BFV joint cycle, determinant/Pfaffian orientation and regulator removal.",
                "The zero-lapse contact/gluing problem, which is orthogonal to this deliberately nonzero-lapse audit.",
                "Every complete global intersection vector, Weyl, spectral, RAQ, empirical, physics and TOE consequence."
            ],
            "killed_shortcut_only": (
                "Extend the Phase-39 half-angle scale plane to infinity, "
                "combine it with the known scalar tails and read the local +1 signs globally."
            ),
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations": 10,
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
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    runner_path.with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": "VALID_RUN",
                "verdict": verdict,
                "exact_passed": len(audit.exact),
                "exact_total": len(audit.exact),
                "numerical_passed": len(audit.numerical),
                "numerical_total": len(audit.numerical),
                "theorem_guards_verified": len(audit.theorem_guards),
                "theorem_guards_total": len(audit.theorem_guards),
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
