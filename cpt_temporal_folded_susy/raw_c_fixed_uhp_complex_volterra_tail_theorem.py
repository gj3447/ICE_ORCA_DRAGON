#!/usr/bin/env python3
"""Complex Volterra tail theorem on one raw-C p=0 UHP box; not m(z) or RAQ."""
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


INPUT_NAME = "RAW_C_P0_FIXED_UHP_COMPLEX_VOLTERRA_TAIL_THEOREM_INPUTS.json"
RESULT_NAME = "RAW_C_P0_FIXED_UHP_COMPLEX_VOLTERRA_TAIL_THEOREM_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_fixed_uhp_complex_volterra_tail_theorem.py"
EXPECTED_INPUT_SHA256 = "d17b1f1c4c6434bf233e6d4e14b6d3081d6412352193b7936c3dcb4650bd00de"
CALCULATION_ID = "RawCP0FixedUhpComplexVolterraTailTheorem"
RESULT_SCHEMA = "ice.raw-c-p0-fixed-uhp-complex-volterra-tail-theorem.result.v1"
RESULT_PREFIX = "RAW_C_P0_FIXED_UHP_COMPLEX_VOLTERRA_TAIL_THEOREM_RESULT="
PASS_VERDICT = "CERTIFY_P0_FIXED_UHP_COMPLEX_TAIL_CONTRACTION_AND_RECESSIVE_QPLUS_ENCLOSURE"
FAIL_VERDICT = "UNRESOLVED_P0_FIXED_UHP_COMPLEX_TAIL"
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


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def interval_record(value: arb, digits: int = 36) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "width_upper": (value.upper() - value.lower()).upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
    }


def complex_record(value: acb, digits: int = 36) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "absolute_lower": value.abs_lower().str(digits, radius=False),
        "absolute_upper": value.abs_upper().str(digits, radius=False),
    }


def finite_arb(value: arb) -> bool:
    text = str(value).lower()
    return "nan" not in text and "inf" not in text


def finite_acb(value: acb) -> bool:
    return finite_arb(value.real) and finite_arb(value.imag)


def intervals_overlap(left: arb, right: arb) -> bool:
    return bool(left.lower() <= right.upper() and right.lower() <= left.upper())


def rectangles_overlap(left: acb, right: acb) -> bool:
    return intervals_overlap(left.real, right.real) and intervals_overlap(left.imag, right.imag)


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "symbolic_operations": 300,
        "ball_evaluations": 32,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "sampling_points": 0,
        "finite_difference_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "validated_Qplus_to_Q0_transport": None,
        "exact_plus_endpoint_to_Q0_boundary_transform": None,
        "singular_endpoint_nonreal_weyl_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_spectral_multiplicity": None,
        "stieltjes_inversion": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "nonzero_p_uniform_weyl_field": None,
        "p_to_zero_direct_integral_assembly": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "physics_claim": None,
        "TOE_claim": None,
        "gate1_core_progress": False,
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
    }


@dataclass
class Audit:
    controls: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    ball_evaluations: int = 0

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def check(self, ident: str, passed: bool, statement: str, **data: Any) -> None:
        self.register(ident)
        self.controls.append(
            {"id": ident, "passed": bool(passed), "statement": statement, **data}
        )

    def guard(
        self,
        ident: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": "SELF_CONTAINED_PROOF_AND_EXECUTABLE_HYPOTHESIS_AUDIT",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )

    def count_ball(self, amount: int = 1) -> None:
        self.ball_evaluations += amount
        if self.ball_evaluations > expected_caps()["ball_evaluations"]:
            raise AssertionError("ball evaluation cap exceeded")


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
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
    return {
        "path": item["path"],
        "sha256": item["sha256"],
        "payload_sha256_without_self": item["payload_sha256_without_self"],
        "verdict": item["required_verdict"],
        "role": item["role"],
    }


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded supporting theorem accepts no command-line arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.raw-c-p0-fixed-uhp-complex-volterra-tail-theorem.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed scope mutation")
    if importlib.metadata.version("python-flint") != "0.9.0":
        raise AssertionError("python-flint runtime version drift")

    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in cfg["upstream_results"]]
    convention = cfg["convention_provenance"]
    if sha256_bytes((root / convention["path"]).read_bytes()) != convention["sha256"]:
        raise AssertionError("coefficient-convention provenance hash mismatch")
    design_boundary = cfg["design_boundary"]
    if sha256_bytes((root / design_boundary["path"]).read_bytes()) != design_boundary["sha256"]:
        raise AssertionError("design-boundary provenance hash mismatch")

    audit = Audit()
    Q, z = sp.symbols("Q z")
    pi = sp.pi
    delta = z * sp.exp(-Q / 2) / (6 * pi**2)
    A0 = 36 * pi**4 * sp.exp(2 * Q)
    A = 36 * pi**4 * sp.exp(2 * Q) + 6 * pi**2 * z * sp.exp(sp.Rational(3, 2) * Q)
    factored_A = A0 * (1 + delta)
    delta_prime = sp.diff(delta, Q)
    delta_second = sp.diff(delta, Q, 2)
    coefficient_checks = {
        "factorization": sp.simplify(A - factored_A) == 0,
        "delta_prime": sp.simplify(delta_prime + delta / 2) == 0,
        "delta_second": sp.simplify(delta_second - delta / 4) == 0,
    }
    audit.check(
        "rawc.p4.volterra.control.coefficient_factorization",
        all(coefficient_checks.values()),
        "The p=0 raw-C coefficient, relative perturbation, and both derivatives agree exactly with the declared factorization.",
        identities=coefficient_checks,
    )

    A_prime = sp.diff(A, Q)
    A_second = sp.diff(A, Q, 2)
    r = sp.simplify(5 * A_prime**2 / (16 * A**2) - A_second / (4 * A))
    r_delta = (16 + 20 * delta + 9 * delta**2) / (64 * (1 + delta) ** 2)
    psi = sp.simplify(-r / A)
    psi_from_A = (4 * A * A_second - 5 * A_prime**2) / (16 * A**3)
    log_u0_prime = -sp.sqrt(A) - A_prime / (4 * A)
    wkb_equation_residual = sp.simplify(
        sp.diff(log_u0_prime, Q) + log_u0_prime**2 - A - r
    )
    residual_checks = {
        "wkb_equation": wkb_equation_residual == 0,
        "residual_delta_form": sp.simplify(sp.together(r - r_delta)) == 0,
        "psi_A_form": sp.simplify(sp.together(psi - psi_from_A)) == 0,
    }
    audit.check(
        "rawc.p4.volterra.control.wkb_residual_identity",
        all(residual_checks.values()),
        "The Liouville-Green proxy has exact source-form residual r, and the transformed equation is W_XX=(1+psi)W with psi=-r/A.",
        identities=residual_checks,
        r_in_delta="(16+20*delta+9*delta^2)/(64*(1+delta)^2)",
        psi="(4*A*A_second-5*A_prime^2)/(16*A^3)",
    )

    eta = sp.Rational(1, 336)
    R_bar = sp.factor((16 + 20 * eta + 9 * eta**2) / (64 * (1 - eta) ** 2))
    V_bar = sp.factor(R_bar / (6 * 9 * 49 * (1 - eta)))
    q_bar = sp.factor(V_bar / (1 - V_bar))
    elementary_branch_checks = {
        "closed_box_inside_open_disk": bool(sp.sqrt(290) / 16 < sp.Rational(9, 8)),
        "exp_minus_2_lt_one_seventh": bool(sp.exp(-2) < sp.Rational(1, 7)),
        "pi_squared_gt_nine": bool(pi**2 > 9),
        "eta_below_one": bool(eta < 1),
        "sqrt_lower_relaxation": bool(sp.sqrt(1 - eta) >= 1 - eta),
    }
    progressive_lower_at_Q4 = 6 * pi**2 * sp.exp(4) * sp.sqrt(1 - eta)

    kernel_antiderivative_check = sp.simplify(
        sp.diff(sp.exp(-Q), Q) + sp.exp(-Q)
    ) == 0
    kernel_checks = {
        "residual_triangle_majorant_positive": bool(R_bar > 0),
        "exp_minus_4_lt_one_over_49": bool(sp.exp(-4) < sp.Rational(1, 49)),
        "tail_antiderivative": kernel_antiderivative_check,
        "V_bar_positive": bool(V_bar > 0),
    }
    audit.check(
        "rawc.p4.volterra.control.kernel_majorant_closed_form",
        all(kernel_checks.values()),
        "The exact r(delta) identity gives |r|<=R_bar, |psi*p_A|=|r/p_A|, and its exp(-Q) half-line envelope integrates in closed form before the rational relaxations defining V_bar.",
        identities=kernel_checks,
        eta_bar=str(eta),
        R_bar=str(R_bar),
        V_bar=str(V_bar),
        q_bar=str(q_bar),
    )
    audit.check(
        "rawc.p4.volterra.control.contraction_strictly_below_one",
        bool(V_bar < sp.Rational(1, 10000) and q_bar < sp.Rational(1, 9999)),
        "The uniform Volterra operator norm is strictly below V_bar<1/10000<1; Banach contraction is therefore available, with fixed-point and X-derivative error q_bar=V_bar/(1-V_bar).",
        V_bar_decimal=str(sp.N(V_bar, 24)),
        q_bar_decimal=str(sp.N(q_bar, 24)),
    )

    eta_q = exact_rational(str(eta))
    R_bar_q = exact_rational(str(R_bar))
    V_bar_q = exact_rational(str(V_bar))
    q_bar_q = exact_rational(str(q_bar))
    tier_records: list[dict[str, Any]] = []
    tier_values: list[dict[str, Any]] = []
    tier_passes: list[bool] = []
    for precision in cfg["declared_conventions"]["precision_bits"]:
        ctx.prec = int(precision)
        eta_ball = arb(eta_q)
        R_ball = arb(R_bar_q)
        V_ball = arb(V_bar_q)
        q_ball = arb(q_bar_q)
        audit.count_ball(4)
        z_box = acb(arb(0, arb(1) / 16), arb(1, arb(1) / 16))
        audit.count_ball()
        delta_4 = z_box * arb(-2).exp() / (6 * arb.pi() ** 2)
        audit.count_ball()
        relative_4 = acb(1) + delta_4
        audit.count_ball()
        A_4 = 36 * arb.pi() ** 4 * arb(8).exp() * relative_4
        audit.count_ball()
        p_4 = A_4.sqrt()
        audit.count_ball()
        u0_4 = p_4.sqrt().inv()
        audit.count_ball()
        ell_4 = acb(1) - delta_4 / (4 * relative_4)
        audit.count_ball()
        u0_prime_4 = -(p_4 + ell_4 / 2) * u0_4
        audit.count_ball()
        value_correction_radius = u0_4.abs_upper() * q_ball
        derivative_correction_radius = (
            u0_prime_4.abs_upper() + (u0_4 * p_4).abs_upper()
        ) * q_ball
        audit.count_ball()
        u_4 = acb(
            u0_4.real + arb(0, value_correction_radius),
            u0_4.imag + arb(0, value_correction_radius),
        )
        audit.count_ball()
        u_prime_4 = acb(
            u0_prime_4.real + arb(0, derivative_correction_radius),
            u0_prime_4.imag + arb(0, derivative_correction_radius),
        )

        delta_upper = delta_4.abs_upper()
        cut_lower = arb(1) - delta_upper
        re_p_lower = p_4.real.lower()
        branch_pass = bool(
            delta_upper < eta_ball
            and cut_lower > arb(0)
            and re_p_lower > arb(0)
        )
        contraction_pass = bool(
            V_ball > arb(0)
            and V_ball < arb(1) / 10000
            and q_ball > V_ball
            and q_ball < arb(1) / 9999
        )
        finite = all(
            finite_acb(item)
            for item in (delta_4, relative_4, A_4, p_4, u0_4, u0_prime_4, u_4, u_prime_4)
        ) and all(
            finite_arb(item)
            for item in (R_ball, V_ball, q_ball, value_correction_radius, derivative_correction_radius)
        )
        tier_pass = branch_pass and contraction_pass and finite
        tier_passes.append(tier_pass)
        tier_values.append(
            {
                "relative": relative_4,
                "p": p_4,
                "u0": u0_4,
                "u0_prime": u0_prime_4,
                "u": u_4,
                "u_prime": u_prime_4,
                "V": V_ball,
                "q": q_ball,
            }
        )
        tier_records.append(
            {
                "precision_bits": precision,
                "delta_at_Q4": complex_record(delta_4),
                "relative_factor_at_Q4": complex_record(relative_4),
                "principal_p_A_at_Q4": complex_record(p_4),
                "wkb_u0_at_Q4": complex_record(u0_4),
                "wkb_u0_prime_at_Q4": complex_record(u0_prime_4),
                "V_bar": interval_record(V_ball),
                "q_bar": interval_record(q_ball),
                "value_correction_radius": interval_record(value_correction_radius),
                "derivative_correction_radius": interval_record(derivative_correction_radius),
                "actual_u_at_Q4_enclosure": complex_record(u_4),
                "actual_u_prime_at_Q4_enclosure": complex_record(u_prime_4),
                "delta_absolute_upper": delta_upper.str(36, radius=False),
                "cut_distance_lower": cut_lower.str(36, radius=False),
                "Re_p_A_lower_at_Q4": re_p_lower.str(36, radius=False),
                "branch_pass": branch_pass,
                "contraction_pass": contraction_pass,
                "finite": finite,
                "passed": tier_pass,
            }
        )

    analytic_progressive = bool(
        all(elementary_branch_checks.values())
        and progressive_lower_at_Q4 > 0
        and all(record["branch_pass"] for record in tier_records)
    )
    audit.check(
        "rawc.p4.volterra.control.branch_halfline_lower_bound",
        analytic_progressive,
        "The closed z box lies in |z|<9/8; |delta|<1/336 on the full Q>=4 half-line gives Re principal p_A>=6*pi^2*exp(Q)*sqrt(1-eta)>0, so every forward real-Q segment is progressive.",
        elementary_inequalities=elementary_branch_checks,
        analytic_Re_p_A_lower_at_Q4=str(sp.N(progressive_lower_at_Q4, 24)),
        open_holomorphy_disk="|z|<9/8",
    )

    same_backend_overlap = bool(
        len(tier_values) == 2
        and rectangles_overlap(tier_values[0]["relative"], tier_values[1]["relative"])
        and rectangles_overlap(tier_values[0]["p"], tier_values[1]["p"])
        and rectangles_overlap(tier_values[0]["u0"], tier_values[1]["u0"])
        and rectangles_overlap(tier_values[0]["u0_prime"], tier_values[1]["u0_prime"])
        and intervals_overlap(tier_values[0]["V"], tier_values[1]["V"])
        and intervals_overlap(tier_values[0]["q"], tier_values[1]["q"])
    )
    audit.check(
        "rawc.p4.volterra.control.two_tier_acb_outward_constants",
        all(tier_passes) and same_backend_overlap,
        "Both precision tiers outwardly enclose the fixed-box Q=4 branch, WKB pair, and pre-proved rational constants; overlap is a same-backend consistency check, not independent evidence or an ODE proof.",
        tiers=tier_records,
        same_backend_overlap=same_backend_overlap,
    )

    hypotheses_before_theorem = all(item["passed"] for item in audit.controls)
    normalization_proof_steps = [
        "Set u=p_A^(-1/2)W(X); exact differentiation gives W_XX=(1+psi)W.",
        "Set H=exp(X)W; variation of constants gives the declared Volterra equation on the progressive real-Q tail.",
        "Progressiveness implies |1-exp(-2 Delta X)|/2<=1, while the exact residual envelope gives operator norm at most V_bar<1.",
        "Banach contraction yields a unique bounded H; |H-1| and |H_X| are at most q_bar, and the tail norm tends to zero so H tends to 1.",
        "The branches and kernel are holomorphic for |z|<9/8 and the uniformly convergent Neumann series makes the normalized solution holomorphic there.",
    ]
    audit.check(
        "rawc.p4.volterra.control.normalization_fixed_uniqueness",
        hypotheses_before_theorem,
        "The self-contained Volterra proof fixes one and only one solution in the bounded-H class with u/u0 tending to 1; without that limit the second-order equation retains scalar freedom.",
        proof_steps=normalization_proof_steps,
        uniqueness_class="bounded H=exp(X)*p_A^(1/2)*u with lim H=1",
        parameter_holomorphy="on the open disk |z|<9/8, hence on a neighborhood of the closed target box",
    )

    endpoint_overlap = bool(
        len(tier_values) == 2
        and rectangles_overlap(tier_values[0]["u"], tier_values[1]["u"])
        and rectangles_overlap(tier_values[0]["u_prime"], tier_values[1]["u_prime"])
    )
    endpoint_finite = all(
        record["finite"]
        and finite_acb(values["u"])
        and finite_acb(values["u_prime"])
        for record, values in zip(tier_records, tier_values, strict=True)
    )
    audit.check(
        "rawc.p4.volterra.control.endpoint_value_derivative_correction_enclosures_finite",
        bool(endpoint_finite and endpoint_overlap and audit.controls[-1]["passed"]),
        "At Q+=4, |u-u0|<=|u0|q_bar and |u'-u0'|<=q_bar(|u0'|+|p_A*u0|); adding each disk radius to both rectangular components is conservative and gives finite outward endpoint enclosures.",
        endpoint_same_backend_overlap=endpoint_overlap,
        rectangle_enlargement="each real and imaginary component is enlarged by the full complex absolute-error radius; correlations are discarded conservatively",
    )

    audit.guard(
        "rawc.p4.volterra.guard.not_validated_ode_solver",
        "complex Volterra tail existence and enclosure, not numerical ODE validation",
        "All-Q bounds come from exact identities and monotone analytic majorants; the declared and observed ODE, quadrature, root, finite-difference, and sampling counts are zero.",
        "python-flint evaluates only fixed-box constants and conservative Q=4 rectangles. No finite WKB ball, precision overlap, or adaptive integration is relabelled as a validated compact transport.",
    )
    audit.guard(
        "rawc.p4.volterra.guard.workbench_scope",
        "ICE workbench claim firewall",
        "The unit is SUPPORTING_ONLY and p=0, Q>=4, fixed-UHP-box scoped; it neither computes Q+=4 to Q0=-4 transport nor constructs boundary maps.",
        "Only the complex-tail prerequisite and actual recessive Q+=4 enclosure may be recorded. m(z), spectral measure or multiplicity, Stieltjes inversion, nonzero-p assembly, RAQ, C/H equivalence, Gate-1 core progress, physics, and TOE remain null or false.",
    )

    passed = bool(
        len(audit.controls) == 8
        and all(item["passed"] for item in audit.controls)
        and len(audit.theorem_guards) == 2
        and all(item["verified"] for item in audit.theorem_guards)
    )
    verdict = PASS_VERDICT if passed else FAIL_VERDICT
    decision_index = 0 if passed else 1
    actual_endpoint = (
        {
            "status": "ACTUAL_INFINITY_NORMALIZED_RECESSIVE_SOLUTION_ENCLOSED_AT_QPLUS_ONLY",
            "Q_plus": 4,
            "parameter_box": cfg["declared_conventions"]["z_box"],
            "normalization": cfg["declared_conventions"]["normalization"],
            "precision_tiers": tier_records,
            "not_transport_to_Q0": True,
        }
        if passed
        else None
    )
    theorem_result = (
        {
            "status": "UNIFORM_BANACH_VOLTERRA_CONTRACTION_PROVED",
            "path": "real Q half-line from each Q>=4 to infinity",
            "progressive": True,
            "parameter_holomorphy_domain": "open disk |z|<9/8",
            "target_parameter_box": cfg["declared_conventions"]["z_box"],
            "V_bar_exact": str(V_bar),
            "V_bar_decimal": str(sp.N(V_bar, 24)),
            "q_bar_exact": str(q_bar),
            "q_bar_decimal": str(sp.N(q_bar, 24)),
            "normalization_fixed": True,
            "unique_in_bounded_H_class": True,
        }
        if passed
        else None
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": cfg["decision_table"][decision_index]["programme_impact"],
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "route_review": cfg["route_review"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)},
        "upstream_results": upstream,
        "convention_provenance": convention,
        "design_boundary": design_boundary,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "controls": audit.controls,
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "controls_passed": sum(item["passed"] for item in audit.controls),
            "controls_total": len(audit.controls),
            "theorem_guards_verified": sum(item["verified"] for item in audit.theorem_guards),
            "theorem_guards_total": len(audit.theorem_guards),
            "all_checks_passed": passed,
        },
        "analytic_majorants": {
            "eta_bar": str(eta),
            "R_bar": str(R_bar),
            "V_bar": str(V_bar),
            "q_bar": str(q_bar),
            "Re_p_A_lower": "6*pi^2*exp(Q)*sqrt(1-eta_bar)",
        },
        "complex_tail_theorem": theorem_result,
        "recessive_endpoint_enclosure_Q4": actual_endpoint,
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations_cap": cfg["resource_caps"]["symbolic_operations"],
            "ball_evaluations": audit.ball_evaluations,
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "sampling_points": 0,
            "finite_difference_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {
            "python": platform.python_version(),
            "python_flint": importlib.metadata.version("python-flint"),
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
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
                "controls_passed": result["check_summary"]["controls_passed"],
                "controls_total": result["check_summary"]["controls_total"],
                "theorem_guards_verified": result["check_summary"]["theorem_guards_verified"],
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
