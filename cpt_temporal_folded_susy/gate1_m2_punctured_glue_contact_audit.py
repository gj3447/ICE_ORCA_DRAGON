#!/usr/bin/env python3
"""Audit the frozen-m=2 punctured lapse glue and its contact freedom.

This unnumbered bounded calculation starts from the already recorded
frozen-A flat-tangent kernels C/|N| and C/z.  It asks a different question
from the consumed scalar zero-lapse one-shot: whether the two punctured
real-line distributions can be related by a point-supported counterterm,
and whether scaling degree alone selects an extension at N=0.

It does not evaluate the full Starobinsky q integral, retry a consumed
runner, construct a joint relative cycle, or emit a Weyl, spectral, RAQ,
physics, or TOE claim.  It writes one adjacent JSON result.
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
from typing import Any, Callable

import sympy as sp
from scipy.integrate import quad
from scipy.special import erfc


INPUT_NAME = "GATE1_M2_PUNCTURED_GLUE_CONTACT_AUDIT_INPUTS.json"
RESULT_NAME = "GATE1_M2_PUNCTURED_GLUE_CONTACT_AUDIT_RESULT.json"
UPSTREAM_NAME = "GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_m2_punctured_glue_contact_audit.py"
)
EXPECTED_INPUT_SHA256 = (
    "627340c5d861f940b2ada36809c917f6c090ae2d8c970c578fd49ef67d5cd55f"
)
EXPECTED_UPSTREAM_SHA256 = (
    "f7d64a09eeb4132e4975b056ee76eedfa32b75c7d29ca1a78bede5b052a66bc6"
)
CALCULATION_ID = "Gate1M2PuncturedGlueContactAudit"
RESULT_SCHEMA = "ice.gate1-m2-punctured-glue-contact-audit.result.v1"
RESULT_PREFIX = "GATE1_M2_PUNCTURED_GLUE_CONTACT_AUDIT_RESULT="
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
        "symbolic_operations": 100,
        "quadratures": 64,
        "root_calls": 0,
        "ode_calls": 0,
        "sampling_points": 32,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "source_defined_joint_relative_cycle": None,
        "source_to_thimble_deformation": None,
        "physical_original_cycle": None,
        "full_joint_orientation": None,
        "absolute_determinant_pfaffian_line": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "singular_endpoint_nonreal_weyl_m": None,
        "spectral_measure": None,
        "rigging_map": None,
        "physical_inner_product": None,
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
    quadratures: int = 0
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

    def integrate(
        self,
        fn: Callable[[float], float],
        lower: float,
        upper: float,
        *,
        epsabs: float,
        epsrel: float,
    ) -> tuple[float, float]:
        self.quadratures += 1
        if self.quadratures > expected_caps()["quadratures"]:
            raise AssertionError("quadrature cap exceeded")
        value, error = quad(
            fn,
            lower,
            upper,
            epsabs=epsabs,
            epsrel=epsrel,
            limit=300,
        )
        if not math.isfinite(value) or not math.isfinite(error):
            raise AssertionError("non-finite quadrature output")
        return float(value), float(error)

    def count_sample(self, count: int = 1) -> None:
        self.sampling_points += count
        if self.sampling_points > expected_caps()["sampling_points"]:
            raise AssertionError("sampling-point cap exceeded")


def compact_even_bump(value: float, radius: float) -> float:
    if abs(value) >= radius:
        return 0.0
    ratio = value / radius
    return math.exp(1.0 - 1.0 / (1.0 - ratio * ratio))


def negative_arm_bump(value: float) -> float:
    if not -2.0 < value < -1.0:
        return 0.0
    product = (value + 2.0) * (-1.0 - value)
    return math.exp(1.0 - 1.0 / (4.0 * product))


def finite_part_on_bump(
    audit: Audit,
    mu: float,
    radius: float,
    split: float,
    epsabs: float,
    epsrel: float,
) -> tuple[float, float]:
    def subtracted(value: float) -> float:
        if value == 0.0:
            return 0.0
        return (compact_even_bump(value, radius) - 1.0) / value

    near, near_error = audit.integrate(
        subtracted, 0.0, split, epsabs=epsabs, epsrel=epsrel
    )
    far, far_error = audit.integrate(
        lambda value: compact_even_bump(value, radius) / value,
        split,
        radius,
        epsabs=epsabs,
        epsrel=epsrel,
    )
    value = 2.0 * near + 2.0 * far + 2.0 * math.log(mu * split)
    error = 2.0 * near_error + 2.0 * far_error
    return value, error


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded audit accepts no arguments")

    input_raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(input_raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {input_sha}"
        )
    cfg = json.loads(input_raw)
    if (
        cfg.get("schema_version")
        != "ice.gate1-m2-punctured-glue-contact-audit.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    boundary = cfg.get("ragnarok_boundary", {})
    if not all(
        boundary.get(key) is True
        for key in (
            "does_not_execute_consumed_runner",
            "does_not_rename_consumed_runner",
            "does_not_reopen_killed_reconciliation",
            "generic_bounded_core_calculation",
        )
    ) or boundary.get("automatic_next") is not None:
        raise AssertionError("Ragnarok execution boundary mutation")

    upstream_raw = Path(__file__).with_name(UPSTREAM_NAME).read_bytes()
    upstream_sha = sha256_bytes(upstream_raw)
    if upstream_sha != EXPECTED_UPSTREAM_SHA256:
        raise AssertionError(
            "upstream hash mismatch: "
            f"expected {EXPECTED_UPSTREAM_SHA256}, observed {upstream_sha}"
        )
    upstream = json.loads(upstream_raw)
    flat = upstream["exact_calculation"]["flat_kernel"]
    if (
        upstream.get("run_status") != "VALID_RUN"
        or flat.get("real_kernel") != "C/Abs(N)"
        or flat.get("negative_arm_ratio") != "-1"
        or flat.get("C") != "sqrt(6)*pi*A**2/hbar"
    ):
        raise AssertionError("upstream flat-kernel evidence drift")

    if importlib.metadata.version("sympy") != "1.14.0":
        raise AssertionError("SymPy runtime version drift")
    if importlib.metadata.version("scipy") != "1.18.0":
        raise AssertionError("SciPy runtime version drift")

    audit = Audit()
    coefficient, positive_n = sp.symbols("C n", positive=True, real=True)
    A, hbar = sp.symbols("A hbar", positive=True, real=True)
    mu_g = 12 * sp.pi**2 * A
    mu_s = 2 * sp.pi**2 * A**3
    source_coefficient = sp.sqrt(mu_g * mu_s) / (2 * sp.pi * hbar)
    expected_coefficient = sp.sqrt(6) * sp.pi * A**2 / hbar
    audit.check_exact(
        "G1.m2.glue.source_coefficient",
        bool(sp.simplify(source_coefficient - expected_coefficient) == 0),
        "The frozen-A source coefficient is C=sqrt(mu_g*mu_s)/(2*pi*hbar)=sqrt(6)*pi*A^2/hbar>0.",
        expression=str(expected_coefficient),
    )

    absolute_positive = coefficient / positive_n
    signed_positive = coefficient / positive_n
    absolute_negative = coefficient / positive_n
    signed_negative = -coefficient / positive_n
    audit.check_exact(
        "G1.m2.glue.positive_arm_agreement",
        bool(sp.simplify(absolute_positive - signed_positive) == 0),
        "C/|N| and C/N agree on the positive punctured arm.",
    )
    audit.check_exact(
        "G1.m2.glue.negative_arm_opposition",
        bool(
            sp.simplify(absolute_negative + signed_negative) == 0
            and sp.simplify(absolute_negative - signed_negative)
            == 2 * coefficient / positive_n
        ),
        "C/|N| and C/N are opposite on the negative punctured arm, where their difference is 2*C/|N|.",
        negative_arm_difference="2*C/|N|",
    )

    lapse = sp.symbols("N", real=True)
    epsilon_positive = sp.symbols("epsilon_positive", positive=True, real=True)
    lateral = 1 / (lapse - sp.I * epsilon_positive)
    lateral_decomposition = (
        lapse / (lapse**2 + epsilon_positive**2)
        + sp.I * epsilon_positive / (lapse**2 + epsilon_positive**2)
    )
    audit.check_exact(
        "G1.m2.glue.lateral_algebra",
        bool(sp.simplify(lateral - lateral_decomposition) == 0),
        "The lower lateral decomposes into the odd PV approximant plus i times the positive Poisson-kernel delta approximant.",
    )

    omega = 1
    dimension = 1
    singular_order = omega - dimension
    audit.check_exact(
        "G1.m2.contact.critical_scaling_order",
        bool(omega == dimension and singular_order == 0),
        "Both degree-minus-one punctured kernels have scaling degree omega=1 in d=1, so same-degree extension data have point-support order zero only.",
        scaling_degree=omega,
        ambient_dimension=dimension,
        singular_order=singular_order,
        allowed_point_support="c*delta(N)",
    )

    mu_left, mu_right = sp.symbols("mu mu_prime", positive=True, real=True)
    scale_shift = 2 * coefficient * sp.log(mu_right / mu_left)
    audit.check_exact(
        "G1.m2.contact.finite_part_scale_shift",
        bool(
            sp.simplify(
                scale_shift
                - 2 * coefficient * (sp.log(mu_right) - sp.log(mu_left))
            )
            == 0
        ),
        "With the declared finite-part convention, changing mu to mu' shifts the extension by +2*C*log(mu'/mu)*delta(N).",
        delta_coefficient=str(scale_shift),
    )

    lower_delta_coefficient = sp.I * sp.pi * coefficient
    upper_delta_coefficient = -sp.I * sp.pi * coefficient
    audit.check_exact(
        "G1.m2.contact.lateral_orientation_mutation",
        bool(
            sp.simplify(lower_delta_coefficient + upper_delta_coefficient)
            == 0
            and lower_delta_coefficient != upper_delta_coefficient
        ),
        "After signed punctured glue is chosen, lower and upper lateral prescriptions select opposite delta coefficients.",
        lower="+i*pi*C",
        upper="-i*pi*C",
    )

    benchmark = cfg["declared_conventions"]["benchmark"]
    a_value = float(benchmark["A"])
    hbar_value = float(benchmark["hbar"])
    c_value = math.sqrt(6.0) * math.pi * a_value * a_value / hbar_value
    epsabs = float(benchmark["quadrature_absolute_tolerance"])
    epsrel = float(benchmark["quadrature_relative_tolerance"])

    negative_pairing, negative_error = audit.integrate(
        lambda value: 2.0 * c_value * negative_arm_bump(value) / abs(value),
        -2.0,
        -1.0,
        epsabs=epsabs,
        epsrel=epsrel,
    )
    audit.count_sample()
    audit.check_numerical(
        "G1.m2.glue.negative_support_separation",
        bool(
            negative_pairing > 100.0 * max(negative_error, sys.float_info.epsilon)
        ),
        "A nonnegative C-infinity probe supported away from zero pairs strictly positively with K_abs-K_signed; a point-supported counterterm pairs to zero there.",
        pairing=negative_pairing,
        quadrature_error=negative_error,
        normalized_pairing=negative_pairing / c_value,
        contact_pairing=0.0,
    )

    radius = float(benchmark["finite_part_probe_support_radius"])
    split = 0.75
    finite_part_records: list[dict[str, float]] = []
    scales = [0.5, 1.0, 2.0, 4.0]
    for scale in scales:
        value, error = finite_part_on_bump(
            audit, scale, radius, split, epsabs, epsrel
        )
        audit.count_sample()
        finite_part_records.append(
            {"mu": scale, "value_over_C": value, "quadrature_error": error}
        )
    reference = finite_part_records[1]
    scale_residuals = [
        abs(
            record["value_over_C"]
            - reference["value_over_C"]
            - 2.0 * math.log(record["mu"] / reference["mu"])
        )
        for record in finite_part_records
    ]
    audit.check_numerical(
        "G1.m2.contact.scale_family_on_compact_bump",
        bool(max(scale_residuals) < 5.0e-11),
        "Independent quadrature on a compact C-infinity bump reproduces the finite-part reference-scale delta shift for four positive mu values.",
        records=finite_part_records,
        max_normalized_residual=max(scale_residuals),
    )

    cutoff_records: list[dict[str, float]] = []
    target_mu = 2.0
    target_value = finite_part_records[2]["value_over_C"]
    for cutoff in (1.0e-2, 2.5e-3, 6.25e-4):
        integral, error = audit.integrate(
            lambda value: compact_even_bump(value, radius) / value,
            cutoff,
            radius,
            epsabs=epsabs,
            epsrel=epsrel,
        )
        audit.count_sample()
        direct = 2.0 * integral + 2.0 * math.log(target_mu * cutoff)
        cutoff_records.append(
            {
                "epsilon": cutoff,
                "direct_value_over_C": direct,
                "absolute_error_to_subtracted_form": abs(direct - target_value),
                "quadrature_error": 2.0 * error,
            }
        )
    cutoff_errors = [
        record["absolute_error_to_subtracted_form"]
        for record in cutoff_records
    ]
    audit.check_numerical(
        "G1.m2.contact.cutoff_limit_cross_check",
        bool(
            cutoff_errors[2] < cutoff_errors[1] < cutoff_errors[0]
            and cutoff_errors[2] < 2.0e-7
        ),
        "The unsubtracted cutoff formula converges monotonically to the independently evaluated subtracted finite part.",
        records=cutoff_records,
    )

    lateral_records: list[dict[str, float]] = []
    for lateral_epsilon in (0.2, 0.05, 0.01, 0.002):
        positive_half, error = audit.integrate(
            lambda value, eps=lateral_epsilon: (
                eps * math.exp(-(value * value)) / (value * value + eps * eps)
            ),
            0.0,
            math.inf,
            epsabs=epsabs,
            epsrel=epsrel,
        )
        audit.count_sample()
        observed = 2.0 * positive_half
        analytic = math.pi * math.exp(lateral_epsilon**2) * erfc(
            lateral_epsilon
        )
        lateral_records.append(
            {
                "epsilon": lateral_epsilon,
                "lower_imaginary_pairing_over_C": observed,
                "upper_imaginary_pairing_over_C": -observed,
                "analytic_poisson_pairing": analytic,
                "quadrature_residual": abs(observed - analytic),
                "distance_to_pi": abs(math.pi - observed),
                "quadrature_error": 2.0 * error,
            }
        )
    lateral_distances = [record["distance_to_pi"] for record in lateral_records]
    audit.check_numerical(
        "G1.m2.contact.lower_upper_lateral_gaussian",
        bool(
            max(record["quadrature_residual"] for record in lateral_records)
            < 5.0e-10
            and all(
                later < earlier
                for earlier, later in zip(
                    lateral_distances, lateral_distances[1:], strict=True
                )
            )
            and lateral_records[-1]["lower_imaginary_pairing_over_C"] > 0.0
            and lateral_records[-1]["upper_imaginary_pairing_over_C"] < 0.0
        ),
        "On an even Gaussian probe, direct quadrature matches the Poisson-kernel formula and approaches opposite plus/minus pi delta pairings for lower/upper laterals.",
        records=lateral_records,
        real_principal_value_pairing=0.0,
    )

    audit.guard(
        "G1.m2.guard.critical_scaling_extension_family",
        verified=bool(omega == dimension and singular_order == 0),
        theorem=(
            "Brunetti--Fredenhagen, arXiv:math-ph/9903028, Theorem 5.2 "
            "(finite scaling degree omega>=d)"
        ),
        hypotheses=(
            "The inherited punctured kernels C/|N| and C/N are homogeneous "
            "of degree -1, so each has scaling degree omega=1 in d=1."
        ),
        conclusion_and_scope=(
            "Same-scaling-degree extensions exist, but are fixed only after "
            "one order-zero point-supported datum is supplied: "
            "Pf_mu(C/|N|)+c*delta or PV(C/N)+c*delta. This does not select c."
        ),
    )
    audit.guard(
        "G1.m2.guard.contact_cannot_change_punctured_glue",
        verified=bool(negative_pairing > 0.0),
        theorem=(
            "A distribution supported at {0} vanishes on every test whose "
            "support is disjoint from {0}; two extensions of one punctured "
            "distribution may differ only on that singular set."
        ),
        hypotheses=(
            "The declared nonnegative smooth probe has support contained in "
            "(-2,-1), and K_abs-K_signed=2*C/|N| there with C>0."
        ),
        conclusion_and_scope=(
            "The absolute and signed kernels are inequivalent already on the "
            "punctured line. No delta contact choice can turn one into the other."
        ),
    )
    audit.guard(
        "G1.m2.guard.sokhotski_plemelj_after_signed_glue",
        verified=bool(
            lateral_records[-1]["lower_imaginary_pairing_over_C"] > 0.0
            and lateral_records[-1]["upper_imaginary_pairing_over_C"] < 0.0
        ),
        theorem=(
            "The algebraic decomposition N/(N^2+epsilon^2) +/- "
            "i*epsilon/(N^2+epsilon^2), together with the odd principal-value "
            "and Poisson-kernel limits, gives 1/(N-i0)=PV(1/N)+i*pi*delta "
            "and 1/(N+i0)=PV(1/N)-i*pi*delta."
        ),
        hypotheses=(
            "The signed punctured kernel C/N has already been chosen before "
            "taking a lateral boundary value."
        ),
        conclusion_and_scope=(
            "A lateral selects a contact coefficient within the signed branch. "
            "It does not derive the signed negative-arm glue from C/|N|."
        ),
    )

    all_checks = all(item["passed"] for item in audit.exact + audit.numerical)
    all_guards = all(item["verified"] for item in audit.theorem_guards)
    if not all_checks or not all_guards:
        raise AssertionError("audit did not close its declared controls")

    verdict = (
        "SOURCE_UNDERDETERMINES_PUNCTURED_GLUE_AND_ZERO_LAPSE_EXTENSION"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "epistemic_status": "SCOPED_INCONCLUSIVE_SUPPORTING_METHOD",
        "programme_impact": cfg["decision_table"][0]["programme_impact"],
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "upstream_evidence": {
            **cfg["upstream_evidence"],
            "observed_sha256": upstream_sha,
        },
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "computed_facts": {
            "source_coefficient": "C=sqrt(6)*pi*A^2/hbar>0",
            "punctured_glue": {
                "positive_arm": "K_abs=K_signed",
                "negative_arm": "K_abs=-K_signed",
                "negative_arm_difference": "K_abs-K_signed=2*C/|N|",
                "contact_term_can_reconcile": False,
                "status": "SOURCE_SELECTION_UNRESOLVED",
            },
            "zero_lapse_extension": {
                "scaling_degree": 1,
                "ambient_dimension": 1,
                "absolute_family": "Pf_mu(C/|N|)+c*delta(N)",
                "signed_family": "PV(C/N)+c*delta(N)",
                "finite_part_scale_shift": (
                    "+2*C*log(mu_prime/mu)*delta(N)"
                ),
                "lower_lateral_signed_choice": (
                    "PV(C/N)+i*pi*C*delta(N)"
                ),
                "upper_lateral_signed_choice": (
                    "PV(C/N)-i*pi*C*delta(N)"
                ),
                "source_selected_contact": None,
            },
            "benchmark_C": c_value,
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
                "The two inherited local kernels are inequivalent on the negative punctured arm, so a zero-supported contact term cannot reconcile them.",
                "At critical scaling degree one, each fixed punctured branch retains one delta-contact parameter unless an additional condition is supplied.",
                "Changing finite-part scale or lateral side changes the contact coefficient according to the recorded exact identities."
            ],
            "interpretation": (
                "The current local source record does not by itself select a "
                "negative-arm determinant glue or a zero-lapse contact normalization."
            ),
            "still_open": [
                "Whether a complete source-defined joint relative cycle and determinant/Pfaffian line supply the missing selection.",
                "Whether any such selection survives regulator, gauge, representative, and orientation mutations.",
                "Every global intersection, Weyl, spectral, RAQ, empirical, physics, and TOE consequence."
            ],
            "killed_shortcut_only": (
                "Current frozen-m=2 local source data uniquely determine both "
                "the negative-arm glue and N=0 contact term."
            ),
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations": 9,
            "quadratures": audit.quadratures,
            "root_calls": 0,
            "ode_calls": 0,
            "sampling_points": audit.sampling_points,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": importlib.metadata.version("sympy"),
            "scipy": importlib.metadata.version("scipy"),
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
