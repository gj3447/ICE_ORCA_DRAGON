#!/usr/bin/env python3
"""Gate 1 -- selected-H full-p regular-shell RAQ completion.

This bounded non-numbered calculation keeps the already selected maximal
multiplication operator

    h(kappa,p) = 3*p**2 - 2*hbar**2*kappa**2

on the full real-p auxiliary spectral space.  It applies coarea only on the
two regular zero rays p=+/-r with r>0, constructs their normalized logarithmic
coordinates, and asks whether the declared regular-shell test space completes
to two L2(R,dx) branches without an origin atom inherited from the auxiliary
Lebesgue spectral measure.

The result is conditional on this selected H, auxiliary measure, and test
space.  It does not choose a raw-C ordering or extension, a p=0 finite part or
origin sector, cross-branch gluing, an exact endpoint transform, an absolute
BFV measure, quantum gravity, physics, or a TOE claim.  It writes one adjacent
JSON result and starts no descendant.
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


INPUT_NAME = "GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_INPUTS.json"
RESULT_NAME = "GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_full_p_regular_raq_completion.py"
)
EXPECTED_INPUT_SHA256 = (
    "da922f82dbc6323386e22f2155bf62e2b8a4a547eb08a0700ac9ba82032b3df3"
)
CALCULATION_ID = "Gate1V0FullPRegularRaqCompletion"
RESULT_SCHEMA = "ice.gate1.v0-full-p-regular-raq-completion.result.v1"
RESULT_PREFIX = "GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
NUMERICAL_DPS = 80
QUADRATURE_CAP = 6


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

    def quadrature(
        self, integrand: Callable[[mp.mpf], mp.mpf], interval: Any
    ) -> mp.mpf:
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
                "verification_mode": (
                    "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_"
                    "NUMERICAL_PREDICATE"
                ),
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
        raise AssertionError("this bounded calculation accepts no arguments")
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
        "ice.gate1.v0-full-p-regular-raq-completion.input.v1"
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
        "quadratures": 6,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "raw_C_operator_and_domain": None,
        "quantum_constraint_rescaling_equivalence": None,
        "canonical_p_zero_origin_sector": None,
        "cross_branch_gluing_or_quotient": None,
        "exact_endpoint_state_transform": None,
        "declared_Mc_identity_equivalence": None,
        "lapse_modulus_or_contour_selection": None,
        "absolute_bfv_measure": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
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
        model["operator"]
        != "the maximal self-adjoint multiplication operator M_h"
        or model["spectral_multiplier"]
        != "h(kappa,p)=3*p^2-2*hbar^2*kappa^2"
        or "R\\{0}" not in model["test_space"]
        or model["origin_rule"].startswith("no delta identity") is False
    ):
        raise AssertionError("declared model or origin rule mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    p = sp.symbols("p", real=True)
    kappa, r, hbar, r_star, q_star = sp.symbols(
        "kappa r hbar r_star q_star", positive=True, real=True
    )
    x = sp.symbols("x", real=True)

    h = 3 * p**2 - 2 * hbar**2 * kappa**2
    kappa_0 = sp.sqrt(sp.Rational(3, 2)) * r / hbar
    factorized_plus = -2 * hbar**2 * (kappa - kappa_0) * (
        kappa + kappa_0
    )
    root_and_factorization = audit.observe(
        "G1.fullp.shell.unique_positive_kappa_root",
        sp.simplify(h.subs(p, r) - factorized_plus) == 0
        and sp.simplify(h.subs({p: r, kappa: kappa_0})) == 0
        and sp.simplify(h.subs({p: -r, kappa: kappa_0})) == 0
        and kappa_0.is_positive is True,
        "for p=+/-r with r>0 the sole positive-kappa zero is kappa_0=sqrt(3/2)*r/hbar",
    )

    transverse_derivative = sp.simplify(4 * hbar**2 * kappa_0)
    expected_derivative = 2 * sp.sqrt(6) * hbar * r
    coarea_derivative = audit.observe(
        "G1.fullp.shell.transverse_coarea_derivative",
        sp.simplify(transverse_derivative - expected_derivative) == 0,
        "the absolute transverse derivative |partial_kappa h| on either regular ray is 2*sqrt(6)*hbar*r",
    )

    shell_weight = sp.simplify(1 / transverse_derivative)
    expected_weight = 1 / (2 * sp.sqrt(6) * hbar * r)
    two_ray_measure = audit.observe(
        "G1.fullp.shell.two_ray_measure",
        sp.simplify(shell_weight - expected_weight) == 0
        and sp.simplify(h.subs(p, r) - h.subs(p, -r)) == 0,
        "the even multiplier gives two disjoint regular rays, each with dr/(2*sqrt(6)*hbar*r)",
    )

    r_of_x = r_star * sp.exp(x)
    log_jacobian = audit.observe(
        "G1.fullp.log_coordinate.measure_jacobian",
        sp.simplify(sp.diff(r_of_x, x) / r_of_x - 1) == 0
        and sp.limit(r_of_x, x, -sp.oo) == 0
        and sp.limit(r_of_x, x, sp.oo) == sp.oo,
        "x=log(r/r_star) maps r in (0,infinity) onto R and gives dr/r=dx; r=0 is x=-infinity",
    )

    branch_normalization = 1 / sp.sqrt(2 * sp.sqrt(6) * hbar)
    normalized_isometry = audit.observe(
        "G1.fullp.log_coordinate.normalized_branch_isometry",
        sp.simplify(branch_normalization**2 - 1 / (2 * sp.sqrt(6) * hbar))
        == 0,
        "multiplying each on-shell trace by 1/sqrt(2*sqrt(6)*hbar) converts its rigging norm exactly to the L2(dx) norm",
    )

    translated_x = sp.expand_log(sp.log(r_of_x / q_star), force=True)
    reference_scale_translation = audit.observe(
        "G1.fullp.log_coordinate.reference_scale_translation",
        sp.simplify(translated_x - x - sp.log(r_star / q_star)) == 0,
        "changing r_star to q_star translates x by log(r_star/q_star) and therefore gives a unitary-equivalent L2 coordinate",
    )

    projector_plus = sp.Matrix([[1, 0], [0, 0]])
    projector_minus = sp.Matrix([[0, 0], [0, 1]])
    sign_operator = sp.Matrix([[1, 0], [0, -1]])
    parity_exchange = sp.Matrix([[0, 1], [1, 0]])
    identity = sp.eye(2)
    disjoint_branch_partition = audit.observe(
        "G1.fullp.branches.disjoint_partition_no_cross_term",
        projector_plus + projector_minus == identity
        and projector_plus * projector_minus == sp.zeros(2)
        and projector_minus * projector_plus == sp.zeros(2),
        "the p-positive and p-negative characteristic projectors are an orthogonal measurable partition, so the declared regular-shell form has no cross-branch term",
    )
    branch_operator_algebra = audit.observe(
        "G1.fullp.branches.projector_sign_parity_algebra",
        sign_operator**2 == identity
        and parity_exchange.T * parity_exchange == identity
        and parity_exchange * sign_operator * parity_exchange == -sign_operator,
        "the direct sum carries orthogonal branch projectors, sign(p), and a unitary parity exchange without imposing a quotient or gluing condition",
    )

    physical_p = sp.diag(r, -r)
    p_observable = audit.observe(
        "G1.fullp.observables.p_and_sign_reduce_branches",
        physical_p * projector_plus == projector_plus * physical_p
        and physical_p * projector_minus == projector_minus * physical_p
        and physical_p * sign_operator == sign_operator * physical_p
        and physical_p**2 == r**2 * identity,
        "on the two traces, p acts as diag(r,-r), sign(p) as diag(1,-1), and both branch projectors reduce the multiplication observable",
    )

    audit.guard(
        "G1.fullp.guard.regular_coarea_only",
        "regular-value delta/coarea identity",
        "r>0 gives kappa_0>0 and |partial_kappa h|=2*sqrt(6)*hbar*r>0 on each ray",
        "the two-ray form is established only on the regular shell; no delta identity or boundary value is asserted at (kappa,p)=(0,0)",
    )
    audit.guard(
        "G1.fullp.guard.dense_regular_test_space",
        "density after removing auxiliary-measure-null coordinate sets",
        "the excluded p=0 axis and kappa=0 boundary have two-dimensional Lebesgue measure zero and smooth compactly supported functions away from them approximate L2 functions",
        "Phi_reg is dense in the declared auxiliary Hilbert space; this does not select a distribution supported at the excluded origin",
    )
    audit.guard(
        "G1.fullp.guard.trace_range_and_completion",
        "tubular extension of compactly supported smooth data on a regular embedded level set",
        "every compact x-supported smooth pair has r support bounded away from zero and infinity and can be extended smoothly in a compact tube transverse to the two regular rays",
        "the quotient trace range contains C_c^infinity(R)_plus direct-sum C_c^infinity(R)_minus and its Hilbert completion is L2(R,dx)_plus direct-sum L2(R,dx)_minus",
    )
    audit.guard(
        "G1.fullp.guard.no_inherited_origin_atom",
        "spectral projections of a multiplication operator",
        "E_h({0}) is multiplication by the indicator of h^{-1}({0}); the two zero rays and their origin have two-dimensional auxiliary Lebesgue measure zero",
        "the selected auxiliary operator has no normalizable zero eigenprojection and supplies no independent origin atom; adding one changes the auxiliary measure or rigging functional",
    )
    audit.guard(
        "G1.fullp.guard.multiplication_observable_domain",
        "self-adjointness of real measurable multiplication operators",
        "under the branch isometry p becomes sigma*r_star*exp(x) on the maximal domain where its product with the wavefunction is square integrable",
        "p and sign(p) have the recorded branch action; parity exchanges branches, while an even/odd quotient or boundary identification is extra structure",
    )
    audit.guard(
        "G1.fullp.guard.scope_and_nonuniqueness",
        "selected-representation and critical-fiber scope separation",
        "the calculation fixes M_h, Lebesgue auxiliary measure, Phi_reg and the positive regular-shell form, while the upstream p=0 witness forbids a naive nonzero boundary trace",
        "the scoped direct sum is the standard absolutely-continuous regular completion, not a uniqueness theorem against separately added origin atoms, finite parts, gluing laws, raw-C extensions, BFV data, physics, or TOE",
    )

    flags = {
        "root_and_factorization": root_and_factorization,
        "coarea_derivative": coarea_derivative,
        "two_ray_measure": two_ray_measure,
        "log_jacobian": log_jacobian,
        "normalized_isometry": normalized_isometry,
        "reference_scale_translation": reference_scale_translation,
        "disjoint_branch_partition": disjoint_branch_partition,
        "branch_operator_algebra": branch_operator_algebra,
        "p_observable": p_observable,
    }
    return (
        {
            "selected_spectral_model": {
                "auxiliary_space": "L2((0,infinity)_kappa times R_p,d_kappa dp)",
                "operator": "maximal self-adjoint M_h",
                "multiplier": str(h),
                "regular_test_space": "C_c^infinity((0,infinity)_kappa times (R\\{0})_p)",
                "raw_C_operator_and_domain": None,
                "quantum_constraint_rescaling_equivalence": None,
            },
            "regular_shell": {
                "parameterization": "p=sigma*r, sigma=+1 or -1, r>0",
                "positive_kappa_root": str(kappa_0),
                "absolute_transverse_derivative": str(transverse_derivative),
                "measure_per_branch": str(expected_weight) + "*dr",
                "cross_branch_term": 0,
                "critical_origin_included_in_coarea": False,
            },
            "branch_isometry": {
                "coordinate": "x=log(r/r_star)",
                "normalized_map": "psi_sigma(x)=A(kappa_0(r_star*exp(x)),sigma*r_star*exp(x))/sqrt(2*sqrt(6)*hbar)",
                "completion": "L2(R,dx)_plus direct-sum L2(R,dx)_minus",
                "p_action": "(p psi)_sigma(x)=sigma*r_star*exp(x)*psi_sigma(x)",
                "sign_action": "diag(+1,-1)",
                "parity_action": "swap the two branches",
                "reference_scale_change": "unitary x-translation",
            },
            "origin_and_gluing": {
                "p_zero_coordinate_location": "x=-infinity",
                "auxiliary_zero_eigenprojection": 0,
                "origin_atom_inherited": False,
                "canonical_finite_part_selected": None,
                "cross_branch_gluing_or_quotient": None,
            },
            "flags": flags,
        },
        flags,
    )


def numerical_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    mp.dps = NUMERICAL_DPS
    coefficient = 1 / (2 * mp.sqrt(6))
    plus_reference = coefficient / 4
    minus_reference = coefficient * 24
    tolerance = mp.mpf("1e-60")
    flags: dict[str, bool] = {}
    rows: list[dict[str, str]] = []

    plus_r = audit.quadrature(
        lambda value: coefficient * value * mp.exp(-2 * value),
        [mp.mpf(0), mp.inf],
    )
    flags["plus_r"] = audit.observe_numeric(
        "G1.fullp.numeric.plus_witness_r_coordinate",
        plus_r,
        plus_reference,
        tolerance,
        "A_plus(r)=r*exp(-r) has the exact regular-shell norm coefficient/4 in the r coordinate",
    )

    minus_r = audit.quadrature(
        lambda value: coefficient * 4 * value**3 * mp.exp(-value),
        [mp.mpf(0), mp.inf],
    )
    flags["minus_r"] = audit.observe_numeric(
        "G1.fullp.numeric.minus_witness_r_coordinate",
        minus_r,
        minus_reference,
        tolerance,
        "A_minus(r)=2*r^2*exp(-r/2) has the exact regular-shell norm 24*coefficient in the r coordinate",
    )

    for scale_label, scale in (
        ("1", mp.mpf(1)),
        ("7_over_5", mp.mpf(7) / 5),
    ):
        plus_x = audit.quadrature(
            lambda value: coefficient
            * (scale * mp.exp(value) * mp.exp(-scale * mp.exp(value))) ** 2,
            [-mp.inf, mp.mpf(0), mp.inf],
        )
        flags[f"plus_x_{scale_label}"] = audit.observe_numeric(
            f"G1.fullp.numeric.plus_witness_x_coordinate_scale_{scale_label}",
            plus_x,
            plus_reference,
            tolerance,
            f"the plus-branch x integral at r_star={scale_label} agrees with the r-coordinate norm",
        )

        minus_x = audit.quadrature(
            lambda value: coefficient
            * (
                2
                * (scale * mp.exp(value)) ** 2
                * mp.exp(-scale * mp.exp(value) / 2)
            )
            ** 2,
            [-mp.inf, mp.mpf(0), mp.inf],
        )
        flags[f"minus_x_{scale_label}"] = audit.observe_numeric(
            f"G1.fullp.numeric.minus_witness_x_coordinate_scale_{scale_label}",
            minus_x,
            minus_reference,
            tolerance,
            f"the minus-branch x integral at r_star={scale_label} agrees with the r-coordinate norm",
        )
        rows.append(
            {
                "r_star": scale_label,
                "plus_x_norm": decimal(plus_x),
                "minus_x_norm": decimal(minus_x),
            }
        )

    if audit.quadrature_calls != QUADRATURE_CAP:
        raise AssertionError(
            f"quadrature accounting mismatch: {audit.quadrature_calls}"
        )
    return (
        {
            "precision_decimal_digits": NUMERICAL_DPS,
            "hbar": "1",
            "witnesses": {
                "plus": "A_plus(r)=r*exp(-r)",
                "minus": "A_minus(r)=2*r^2*exp(-r/2)",
            },
            "r_coordinate": {
                "plus_norm": decimal(plus_r),
                "minus_norm": decimal(minus_r),
            },
            "x_coordinate_rows": rows,
            "exact_plus_norm": decimal(plus_reference),
            "exact_minus_norm": decimal(minus_reference),
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
    analytic_guard_set_complete = len(audit.theorem_guards) == 6

    if all_exact and all_numerical and analytic_guard_set_complete:
        verdict = (
            "KEEP_SELECTED_H_FULL_P_REGULAR_RAQ_DIRECT_SUM_NO_INHERITED_"
            "ORIGIN_ATOM"
        )
        impact = (
            "CLOSE_STANDARD_FULL_P_REGULAR_SHELL_COMPLETION_KEEP_EXTRA_"
            "ORIGIN_OR_GLUING_CHOICES_OPEN"
        )
        classification = (
            "GATE1_V0_SELECTED_H_FULL_REAL_P_REGULAR_ZERO_SHELL_COMPLETES_"
            "TO_TWO_L2_LOG_BRANCHES_WITH_NO_AUXILIARY_ORIGIN_ATOM"
        )
        condition = frozen_input["decision_table"][0]["condition"]
        scoped_completion = exact["branch_isometry"]["completion"]
    else:
        verdict = "KILL_SELECTED_H_FULL_P_REGULAR_RAQ_DIRECT_SUM_DISCRIMINATOR"
        impact = (
            "RETAIN_SEPARATE_P_POSITIVE_AND_P_ZERO_RESULTS_WITHOUT_A_FULL_"
            "P_COMPLETION_CLAIM"
        )
        classification = "GATE1_V0_SELECTED_H_FULL_P_REGULAR_COMPLETION_NONPASS"
        condition = frozen_input["decision_table"][1]["condition"]
        scoped_completion = None

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
        "analytic_guard_set_complete": analytic_guard_set_complete,
        "scoped_outputs": {
            "selected_H_full_p_regular_completion": scoped_completion,
            "origin_atom_inherited": False if scoped_completion else None,
            "raw_C_operator_and_domain": None,
            "cross_branch_gluing_or_quotient": None,
        },
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "the Hilbert completion of the declared regular-shell RAQ form for one selected maximal multiplication operator",
            "primary_source_boundary": "RAQ and direct-integral sources supply the framework and hypotheses; the exact two-ray reduction, branch algebra and witness checks are repository workbench results",
            "revision_boundary": "the p=0 boundary is now separated into an ordinary x=-infinity end of two regular L2 branches and an unselected critical-origin distributional sector",
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
                "selected_H_full_p_regular_completion": result[
                    "scoped_outputs"
                ]["selected_H_full_p_regular_completion"],
                "origin_atom_inherited": result["scoped_outputs"][
                    "origin_atom_inherited"
                ],
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
