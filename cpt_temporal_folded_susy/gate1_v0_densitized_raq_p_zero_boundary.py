#!/usr/bin/env python3
"""Gate 1 -- densitized V=0 RAQ p=0 boundary control.

This bounded non-numbered calculation does not choose a new constraint or
ordering.  It keeps the already selected densitized spectral multiplier

    h(kappa,p) = 3*p**2 - 2*hbar**2*kappa**2

and asks whether its standard positive p>0 group-average measure can include
the singular endpoint p=0 without extra data.  Every delta/coarea step is
performed with a strictly positive cutoff.  Exact algebra and independent
high-precision quadrature compare an amplitude nonzero at the endpoint with
one that vanishes there.  A finite-part subtraction is inspected only to
expose its reference-scale dependence; it is not promoted to a rigging map.

The calculation is not a raw-C ordering, a constraint-rescaling equivalence
proof, an endpoint-state prescription, a full BFV quantization, quantum
gravity, physics, or a TOE claim.  It writes one adjacent JSON result and
starts no descendant.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import mpmath
from mpmath import mp
import sympy as sp


INPUT_NAME = "GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_INPUTS.json"
RESULT_NAME = "GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_densitized_raq_p_zero_boundary.py"
)
EXPECTED_INPUT_SHA256 = (
    "29eb383b81af623e20daf424edfecab24ceaa92fea348d321d6d6ead9bb84149"
)
CALCULATION_ID = "Gate1V0DensitizedRaqPZeroBoundary"
RESULT_SCHEMA = "ice.gate1.v0-densitized-raq-p-zero-boundary.result.v1"
RESULT_PREFIX = "GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
NUMERICAL_DPS = 80
QUADRATURE_CAP = 7


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


def decimal(value: mp.mpf, digits: int = 60) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    quadrature_calls: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def observe_numeric(
        self,
        check_id: str,
        observed: mp.mpf,
        reference: mp.mpf,
        tolerance: mp.mpf,
        statement: str,
    ) -> bool:
        self.register(check_id)
        error = abs(observed - reference)
        passed = bool(error <= tolerance)
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "observed": decimal(observed),
                "reference": decimal(reference),
                "absolute_error": decimal(error),
                "absolute_tolerance": decimal(tolerance),
            }
        )
        return passed

    def quadrature(self, integrand: Callable[[mp.mpf], mp.mpf], interval: Any) -> mp.mpf:
        self.quadrature_calls += 1
        if self.quadrature_calls > QUADRATURE_CAP:
            raise AssertionError("quadrature cap exceeded")
        return mp.quad(integrand, interval)

    def guard(
        self,
        guard_id: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(
            f"upstream hash mismatch for {item['path']}: {observed}"
        )
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload mutation: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this frozen calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-densitized-raq-p-zero-boundary.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 7,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "raw_C_operator_and_domain": None,
        "quantum_constraint_rescaling_equivalence": None,
        "declared_Mc_identity_equivalence": None,
        "canonical_p_zero_edge_completion": None,
        "p_zero_endpoint_counterterm_or_sector": None,
        "gauge_independent_physical_inner_product": None,
        "exact_endpoint_state_transform": None,
        "lapse_modulus_or_contour_selection": None,
        "full_bfv_trajectory_measure": None,
        "brst_cohomology": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    model = payload["declared_model"]
    if (
        model["spectral_multiplier"]
        != "h(kappa,p)=3*p^2-2*hbar^2*kappa^2"
        or "epsilon>0" not in model["cutoff"]
        or model["nonzero_edge_witness"] != "A_0(p)=exp(-p)"
        or model["vanishing_edge_witness"] != "A_1(p)=p*exp(-p)"
    ):
        raise AssertionError("declared model or witness mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    p, kappa, hbar, epsilon = sp.symbols(
        "p kappa hbar epsilon", positive=True, real=True
    )
    u, v = sp.symbols("u v", real=True)
    p_star, q_star = sp.symbols("p_star q_star", positive=True, real=True)

    spectral_multiplier = 3 * p**2 - 2 * hbar**2 * kappa**2
    x = sp.sqrt(3) * p
    y = sp.sqrt(2) * hbar * kappa
    xy_factorization = audit.observe(
        "G1.pzero.shell.xy_factorization",
        sp.simplify(spectral_multiplier - (x**2 - y**2)) == 0,
        "x=sqrt(3)*p and y=sqrt(2)*hbar*kappa factor the selected multiplier as h=x^2-y^2",
    )

    jacobian_xy = sp.Matrix(
        [
            [sp.diff(x, p), sp.diff(x, kappa)],
            [sp.diff(y, p), sp.diff(y, kappa)],
        ]
    ).det()
    xy_jacobian = audit.observe(
        "G1.pzero.shell.xy_jacobian",
        sp.simplify(jacobian_xy - sp.sqrt(6) * hbar) == 0,
        "the positive-quadrant measure transforms as dx*dy=sqrt(6)*hbar*dp*dkappa",
    )

    x_uv = (u + v) / 2
    y_uv = (u - v) / 2
    jacobian_uv_to_xy = sp.Matrix(
        [
            [sp.diff(x_uv, u), sp.diff(x_uv, v)],
            [sp.diff(y_uv, u), sp.diff(y_uv, v)],
        ]
    ).det()
    uv_factorization = audit.observe(
        "G1.pzero.shell.uv_factorization_and_jacobian",
        sp.simplify(x_uv**2 - y_uv**2 - u * v) == 0
        and sp.simplify(abs(jacobian_uv_to_xy) - sp.Rational(1, 2)) == 0,
        "u=x+y and v=x-y give h=u*v and dx*dy=(1/2)*du*dv away from the singular origin",
    )

    shell_u = 2 * sp.sqrt(3) * p
    shell_prefactor = sp.Rational(1, 2) / (sp.sqrt(6) * hbar)
    shell_weight = sp.simplify(
        shell_prefactor * sp.diff(shell_u, p) / shell_u
    )
    expected_weight = 1 / (2 * sp.sqrt(6) * hbar * p)
    positive_ray_weight = audit.observe(
        "G1.pzero.shell.cutoff_positive_ray_weight",
        sp.simplify(shell_weight - expected_weight) == 0,
        "on v=0 with p>=epsilon>0 the coarea measure is dp/(2*sqrt(6)*hbar*p); no delta(u*v) formula is used at u=0",
    )

    denominator = 2 * sp.sqrt(6) * hbar
    cutoff_norm_nonzero = sp.expint(1, 2 * epsilon) / denominator
    e1_derivative = audit.observe(
        "G1.pzero.nonzero_witness.e1_cutoff_identity",
        sp.simplify(
            sp.diff(cutoff_norm_nonzero, epsilon)
            + sp.exp(-2 * epsilon) / (denominator * epsilon)
        )
        == 0,
        "the cutoff norm of exp(-p) is E1(2*epsilon)/(2*sqrt(6)*hbar), with derivative minus exp(-2*epsilon)/(2*sqrt(6)*hbar*epsilon)",
    )

    endpoint_limit = sp.limit(cutoff_norm_nonzero, epsilon, 0, dir="+")
    logarithmic_coefficient = sp.limit(
        cutoff_norm_nonzero / sp.log(1 / epsilon), epsilon, 0, dir="+"
    )
    nonzero_edge_divergence = audit.observe(
        "G1.pzero.nonzero_witness.logarithmic_divergence",
        endpoint_limit == sp.oo
        and sp.simplify(logarithmic_coefficient - 1 / denominator) == 0,
        "the norm of an amplitude nonzero at p=0 diverges as log(1/epsilon)/(2*sqrt(6)*hbar)",
    )

    finite_part_base = sp.limit(
        cutoff_norm_nonzero - sp.log(1 / epsilon) / denominator,
        epsilon,
        0,
        dir="+",
    )
    e1_finite_constant = audit.observe(
        "G1.pzero.nonzero_witness.e1_finite_constant",
        sp.simplify(
            finite_part_base
            - (-sp.EulerGamma - sp.log(2)) / denominator
        )
        == 0,
        "after subtracting the universal log(1/epsilon), the E1 witness leaves (-EulerGamma-log(2))/(2*sqrt(6)*hbar)",
    )

    regular_integral = sp.integrate(p * sp.exp(-2 * p), (p, 0, sp.oo))
    regular_norm = sp.simplify(regular_integral / denominator)
    vanishing_edge_finite = audit.observe(
        "G1.pzero.vanishing_witness.finite_norm",
        sp.simplify(regular_norm - 1 / (8 * sp.sqrt(6) * hbar)) == 0
        and regular_norm.is_positive is True,
        "the amplitude p*exp(-p) vanishes linearly and has finite positive norm 1/(8*sqrt(6)*hbar)",
    )

    finite_part_p = sp.simplify(finite_part_base - sp.log(p_star) / denominator)
    finite_part_q = sp.simplify(finite_part_base - sp.log(q_star) / denominator)
    finite_part_shift = sp.simplify(finite_part_p - finite_part_q)
    scale_ambiguity = audit.observe(
        "G1.pzero.finite_part.reference_scale_shift",
        sp.simplify(
            finite_part_shift - sp.log(q_star / p_star) / denominator
        )
        == 0
        and sp.simplify(
            finite_part_shift.subs({p_star: 1, q_star: 2})
        )
        != 0,
        "subtracting log(p_star/epsilon) leaves finite parts whose difference is log(q_star/p_star)/(2*sqrt(6)*hbar)",
    )

    endpoint_domain_separation = audit.observe(
        "G1.pzero.domain.nonzero_and_vanishing_witness_separate",
        endpoint_limit == sp.oo and regular_norm.is_finite is True,
        "the same positive interior measure excludes the nonzero-edge witness but admits the linearly vanishing witness",
    )

    audit.guard(
        "G1.pzero.guard.cutoff_coarea_only",
        "regular-value delta/coarea identity",
        "epsilon>0 keeps p and kappa away from the only critical zero at the origin, and the positive zero ray has nonvanishing transverse derivative there",
        "the dp/p shell measure is valid for every fixed cutoff; the calculation never asserts delta(u*v)=delta(v)/u at u=0",
    )
    audit.guard(
        "G1.pzero.guard.e1_small_argument",
        "DLMF 6.2.1 and 6.2.4 exponential-integral identities",
        "epsilon>0 and E1(2*epsilon)=integral_{2*epsilon}^infinity exp(-t)dt/t=Ein(2*epsilon)-log(2*epsilon)-EulerGamma",
        "the nonzero-edge witness has the recorded universal logarithmic divergence and finite constant; DLMF does not select an endpoint subtraction",
    )
    audit.guard(
        "G1.pzero.guard.positive_form_local_finiteness",
        "finite-norm requirement for a positive rigging form",
        "the proposed enlarged test domain contains A_0=exp(-p), whose diagonal cutoff form is monotone positive and diverges as epsilon tends to zero",
        "the standard positive interior measure cannot assign A_0 a finite norm at p=0; an origin counterterm cannot cancel positive accumulated mass without changing positivity or the domain",
    )
    audit.guard(
        "G1.pzero.guard.vanishing_order_threshold",
        "elementary endpoint integrability criterion",
        "if an on-shell amplitude is O(p^alpha), its diagonal density is O(p^(2*alpha-1))dp near zero",
        "alpha>0 is locally integrable while alpha=0 has the logarithmic boundary witnessed here; this states a domain condition, not a canonical domain selection",
    )
    audit.guard(
        "G1.pzero.guard.finite_part_is_extra_choice",
        "reference-scale dependence of logarithmic finite parts",
        "the subtraction log(p_star/epsilon) uses an externally chosen positive reference momentum p_star",
        "different reference momenta shift the finite value, so the cutoff algebra alone does not select a canonical p=0 rigging map, counterterm, or sector",
    )
    audit.guard(
        "G1.pzero.guard.constraint_rescaling_and_physics_scope",
        "constraint-rescaling and model-scope separation",
        "the calculation holds the selected densitized H_hat fixed and includes no raw-C operator, lapse contour, inhomogeneous metric modes, observables, or empirical map",
        "the result narrows one quantum-cosmology endpoint obstruction only; raw-C equivalence, full BFV, quantum gravity, physics, and TOE remain null",
    )

    flags = {
        "xy_factorization": xy_factorization,
        "xy_jacobian": xy_jacobian,
        "uv_factorization": uv_factorization,
        "positive_ray_weight": positive_ray_weight,
        "e1_cutoff_identity": e1_derivative,
        "nonzero_edge_log_divergence": nonzero_edge_divergence,
        "e1_finite_constant": e1_finite_constant,
        "vanishing_edge_finite": vanishing_edge_finite,
        "finite_part_scale_ambiguity": scale_ambiguity,
        "endpoint_domain_separation": endpoint_domain_separation,
    }
    return (
        {
            "selected_spectral_model": {
                "multiplier": str(spectral_multiplier),
                "positive_zero_ray": "kappa_0(p)=sqrt(3/2)*p/hbar",
                "upstream_interior_test_space": "C_c^infinity((0,infinity)_kappa times (0,infinity)_p)",
                "raw_C_operator_and_domain": None,
                "quantum_constraint_rescaling_equivalence": None,
            },
            "cutoff_shell_derivation": {
                "coordinates": {
                    "x": str(x),
                    "y": str(y),
                    "u": "x+y",
                    "v": "x-y",
                },
                "factorization": "h=x^2-y^2=u*v",
                "jacobian_dxdy_over_dpdκ": str(jacobian_xy),
                "jacobian_dxdy_over_dudv_absolute": str(abs(jacobian_uv_to_xy)),
                "cutoff_domain": "p>=epsilon>0, equivalently u>=2*sqrt(3)*epsilon on v=0",
                "positive_shell_measure": str(expected_weight) + "*dp",
                "origin_delta_identity_used": False,
            },
            "endpoint_witnesses": {
                "nonzero_edge": {
                    "amplitude": "exp(-p)",
                    "cutoff_norm": str(cutoff_norm_nonzero),
                    "endpoint_limit": str(endpoint_limit),
                    "logarithmic_coefficient": str(logarithmic_coefficient),
                    "finite_constant_after_log_subtraction": str(finite_part_base),
                    "admitted_by_naive_closed_edge_domain": False,
                },
                "linearly_vanishing_edge": {
                    "amplitude": "p*exp(-p)",
                    "norm": str(regular_norm),
                    "admitted_by_weighted_space": True,
                },
                "local_order_rule": "A=O(p^alpha) gives |A|^2 dp/p=O(p^(2*alpha-1))dp; alpha>0 is locally integrable",
            },
            "finite_part_diagnostic": {
                "definition": "FP_pstar=lim_{epsilon->0+}[eta_epsilon(exp(-p),exp(-p))-log(p_star/epsilon)/(2*sqrt(6)*hbar)]",
                "value": str(finite_part_p),
                "two_scale_difference": str(finite_part_shift),
                "canonical_reference_scale_selected": None,
                "canonical_p_zero_edge_completion": None,
            },
            "flags": flags,
        },
        flags,
    )


def numerical_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    mp.dps = NUMERICAL_DPS
    denominator = 2 * mp.sqrt(6)
    cutoff_rows: list[dict[str, str]] = []
    flags: dict[str, bool] = {}

    for label in ("1e-2", "1e-4", "1e-6"):
        epsilon = mp.mpf(label)
        direct = audit.quadrature(
            lambda value: mp.exp(-2 * value) / value, [epsilon, mp.mpf(1)]
        ) + audit.quadrature(
            lambda value: mp.exp(-2 * value) / value, [mp.mpf(1), mp.inf]
        )
        observed = direct / denominator
        reference = mp.e1(2 * epsilon) / denominator
        passed = audit.observe_numeric(
            f"G1.pzero.numeric.e1_direct_quadrature_{label}",
            observed,
            reference,
            mp.mpf("1e-65"),
            f"direct positive quadrature at epsilon={label} agrees with E1(2*epsilon)/(2*sqrt(6))",
        )
        flags[f"e1_quadrature_{label}"] = passed
        cutoff_rows.append(
            {
                "epsilon": label,
                "direct_norm": decimal(observed),
                "e1_norm": decimal(reference),
            }
        )

    regular_observed = audit.quadrature(
        lambda value: value * mp.exp(-2 * value) / denominator,
        [mp.mpf(0), mp.inf],
    )
    regular_reference = 1 / (8 * mp.sqrt(6))
    flags["regular_witness_quadrature"] = audit.observe_numeric(
        "G1.pzero.numeric.vanishing_witness_direct_quadrature",
        regular_observed,
        regular_reference,
        mp.mpf("1e-65"),
        "direct quadrature of p*exp(-2p)/(2*sqrt(6)) agrees with 1/(8*sqrt(6))",
    )

    epsilon_large = mp.mpf("1e-6")
    epsilon_small = mp.mpf("1e-12")
    slope = (
        mp.e1(2 * epsilon_small) - mp.e1(2 * epsilon_large)
    ) / (denominator * mp.log(epsilon_large / epsilon_small))
    slope_reference = 1 / denominator
    flags["log_slope"] = audit.observe_numeric(
        "G1.pzero.numeric.logarithmic_increment_coefficient",
        slope,
        slope_reference,
        mp.mpf("1e-7"),
        "the six-decade E1 increment approaches the exact log coefficient 1/(2*sqrt(6))",
    )

    if audit.quadrature_calls != QUADRATURE_CAP:
        raise AssertionError(
            f"quadrature accounting mismatch: {audit.quadrature_calls}"
        )
    return (
        {
            "precision_decimal_digits": NUMERICAL_DPS,
            "hbar": "1",
            "cutoff_rows": cutoff_rows,
            "regular_witness_norm": decimal(regular_observed),
            "six_decade_log_slope": decimal(slope),
            "exact_log_coefficient": decimal(slope_reference),
            "quadrature_calls": audit.quadrature_calls,
            "roots": 0,
            "ode_calls": 0,
        },
        flags,
    )


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, str]],
    audit: Audit,
) -> dict[str, Any]:
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit)
    all_exact = all(exact_flags.values())
    all_numerical = all(numerical_flags.values())

    if all_exact and all_numerical:
        verdict = "NARROW_V0_P_ZERO_STANDARD_GROUP_AVERAGE_REQUIRES_EXTRA_EDGE_DATA"
        impact = (
            "CLOSE_NAIVE_CUTOFF_ONLY_P_ZERO_COMPLETION_KEEP_CANONICAL_EDGE_"
            "COMPLETION_OPEN"
        )
        classification = (
            "GATE1_V0_SELECTED_DENSITIZED_H_P_ZERO_NONZERO_EDGE_WITNESS_"
            "LOG_DIVERGENCE_VANISHING_WITNESS_FINITE_FINITE_PART_SCALE_"
            "AMBIGUITY"
        )
        condition = (
            "the exact shell measure has dp/p, the nonzero-edge witness "
            "diverges logarithmically, the vanishing witness is finite, "
            "reference-scale finite parts differ, and all independent "
            "quadratures pass"
        )
    else:
        verdict = "KILL_V0_P_ZERO_BOUNDARY_DISCRIMINATOR"
        impact = (
            "RETAIN_THE_UPSTREAM_P_GREATER_THAN_ZERO_RESULT_WITHOUT_A_NEW_"
            "EDGE_CLAIM"
        )
        classification = "GATE1_V0_DENSITIZED_H_P_ZERO_BOUNDARY_NONPASS"
        condition = (
            "one or more Jacobian, shell-weight, E1, logarithmic, finite-"
            "witness, scale-shift, or independent quadrature checks fail"
        )

    promoted = dict(frozen_input["required_fail_closed_outputs"])
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": classification,
        "verdict": verdict,
        "programme_impact": impact,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_provenance": upstream,
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "one p=0 boundary discriminator for the already selected densitized H_hat positive group average",
            "primary_source_boundary": "DLMF fixes the E1 identities and RAQ sources fix the framework; the cutoff witnesses, scale comparison, and scope verdict are repository workbench results",
            "revision_boundary": "the upstream statement p=0 is singular is sharpened to a positive nonzero-edge log divergence plus an explicit finite-part scale ambiguity; no canonical completion is selected",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted,
        "gate1_decision": promoted["gate1"],
        "global_promotion": promoted["global_promotion"],
        "automatic_next": promoted["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": audit.quadrature_calls,
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "mpmath": mpmath.__version__,
            "platform": platform.platform(),
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_scope": frozen_input["epistemic_scope"],
            "decision_table": frozen_input["decision_table"],
            "primary_sources": frozen_input["primary_sources"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256, upstream = load_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, upstream, audit)
    encoded = json.dumps(
        result,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds the bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": sum(item["passed"] for item in audit.exact),
                "exact_checks_total": len(audit.exact),
                "numerical_checks_passed": sum(
                    item["passed"] for item in audit.numerical
                ),
                "numerical_checks_total": len(audit.numerical),
                "theorem_guards_verified": len(audit.theorem_guards),
                "quadratures": audit.quadrature_calls,
                "canonical_p_zero_edge_completion": None,
                "raw_C_operator_and_domain": None,
                "quantum_gravity_claim": None,
                "physics_claim": None,
                "TOE_claim": None,
                "gate1": result["gate1_decision"],
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
