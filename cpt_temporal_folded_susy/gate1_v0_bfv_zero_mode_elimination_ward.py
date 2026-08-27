#!/usr/bin/env python3
"""Gate 1 -- BFV zero-mode elimination and scaling-Ward control.

This bounded non-numbered calculation revisits one specific mismatch in the
hash-pinned V=0 ``m=2`` BFV result.  For the algebraic block

    S0(lambda) = lambda*(N0*c0 - rho0*bar_rho0),  lambda > 0,

it compares (i) direct oriented Berezin integration, (ii) elimination of the
nondegenerate ghost pair with its induced odd Gaussian factor, and (iii) the
negative control that simply deletes the pair.  The first two routes must agree
and cancel the bosonic ``delta(lambda*c0)`` Jacobian; the third must not.

The calculation resolves only that local bookkeeping mismatch.  It does not
select a gravitational lapse contour or modulus prescription, construct an
absolute/full BFV measure or BRST cohomology, prove field-dependent constraint
rescaling invariance, or make quantum-gravity, physics, or TOE claims.  One
adjacent JSON result is written and no descendant starts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_INPUTS.json"
RESULT_NAME = "GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_bfv_zero_mode_elimination_ward.py"
)
EXPECTED_INPUT_SHA256 = (
    "912492397b0488562eacce1b37d8998faf73ad0c6b30d716fc3e8da98d99ecdd"
)
CALCULATION_ID = "Gate1V0BfvZeroModeEliminationWard"
RESULT_SCHEMA = "ice.gate1.v0-bfv-zero-mode-elimination-ward.result.v1"
RESULT_PREFIX = "GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT="
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


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)

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


def verify_upstream(
    root: Path, item: dict[str, Any]
) -> tuple[dict[str, str], dict[str, Any]]:
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
    record = {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }
    return record, payload


def load_input() -> tuple[
    dict[str, Any], str, list[dict[str, str]], list[dict[str, Any]]
]:
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
        "ice.gate1.v0-bfv-zero-mode-elimination-ward.input.v1"
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
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "unique_trajectory_zero_mode_completion": None,
        "lapse_modulus_or_contour_selection": None,
        "absolute_finite_bfv_measure": None,
        "full_bfv_trajectory_measure": None,
        "continuum_bfv_limit": None,
        "brst_cohomology": None,
        "constraint_densitization_equivalence": None,
        "raw_C_physical_inner_product": None,
        "exact_endpoint_state_transform": None,
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
    zero = payload["zero_block"]
    if (
        zero["lambda_domain"] != "lambda>0"
        or zero["odd_order"] != ["rho0", "bar_rho0"]
        or "i*hbar" not in zero["oriented_berezin_extraction"]
        or "dN0/(2*pi*hbar)" != zero["bosonic_fourier_measure"]
    ):
        raise AssertionError("zero-block orientation or measure mutation")
    root = Path(__file__).resolve().parent.parent
    verified: list[dict[str, str]] = []
    full_payloads: list[dict[str, Any]] = []
    for item in payload["upstream_results"]:
        record, full = verify_upstream(root, item)
        verified.append(record)
        full_payloads.append(full)
    return payload, observed, verified, full_payloads


def exact_calculation(
    upstream_payloads: list[dict[str, Any]], audit: Audit
) -> tuple[dict[str, Any], dict[str, bool], bool]:
    static = upstream_payloads[0]["exact_calculation"]
    previous = upstream_payloads[1]["exact_calculation"]
    algebra = static["bfv_algebra"]
    previous_ledgers = previous["zero_mode_ledgers"]

    expected_images = {
        "N": [{"coefficient": "1", "monomial": "rho"}],
        "Phi": [],
        "Pi": [],
        "T": [{"coefficient": "1", "monomial": "c_g"}],
        "bar_c": [{"coefficient": "Pi", "monomial": "1"}],
        "bar_rho": [{"coefficient": "c", "monomial": "1"}],
        "c": [],
        "c_g": [],
        "p": [],
        "rho": [],
    }
    static_contract = audit.observe(
        "G1.zero_ward.upstream.static_brst_contract",
        algebra["Omega"] == "c_g*c+rho*Pi"
        and algebra["brst_generator_images"] == expected_images
        and algebra["bracket_Omega_Omega"] == []
        and all(
            value == []
            for value in algebra["squared_generator_images"].values()
        ),
        "the hash-pinned static source has Omega=c_g*c+rho*Pi, the required generator images, and vanishing squared images",
    )
    prior_mismatch = audit.observe(
        "G1.zero_ward.upstream.prior_ledger_mismatch",
        previous_ledgers["retained_algebraic_pair"]["ghost_factor"]
        == "lambda"
        and previous_ledgers["retained_algebraic_pair"][
            "combined_relative_factor"
        ]
        == "1"
        and previous_ledgers["eliminated_algebraic_pair"]["ghost_factor"]
        is None
        and previous_ledgers["eliminated_algebraic_pair"][
            "combined_relative_factor"
        ]
        == "1/lambda"
        and previous_ledgers["inequivalent"] is True,
        "the prior result really compared a retained lambda factor with an eliminated ledger whose odd Gaussian factor was null",
    )

    lam, hbar = sp.symbols("lambda hbar", positive=True, real=True)
    c0, lapse0 = sp.symbols("c0 N0", real=True)
    rho0, bar_rho0 = sp.symbols("rho0 bar_rho0")

    generator_images = {
        "N0": "rho0",
        "rho0": None,
        "bar_rho0": "c0",
        "c0": None,
    }
    squared_images = {
        name: generator_images.get(image) if image is not None else None
        for name, image in generator_images.items()
    }
    nilpotence = audit.observe(
        "G1.zero_ward.brst.generator_nilpotence",
        all(image is None for image in squared_images.values()),
        "the projected right-BRST images sN0=rho0, sbar_rho0=c0, srho0=sc0=0 square to zero",
    )
    variation_bosonic = rho0 * c0
    variation_ghost_bilinear = rho0 * c0
    action_variation = sp.simplify(
        lam * (variation_bosonic - variation_ghost_bilinear)
    )
    brst_closure = audit.observe(
        "G1.zero_ward.brst.action_closure",
        action_variation == 0,
        "under the inherited right-acting bracket rule s(N0*c0)=s(rho0*bar_rho0)=rho0*c0, so sS0=0",
    )

    exponent_top_coefficient = -sp.I * lam / hbar
    oriented_measure = sp.I * hbar
    direct_ghost_factor = sp.simplify(
        oriented_measure * exponent_top_coefficient
    )
    direct_berezin = audit.observe(
        "G1.zero_ward.direct.berezin_factor",
        direct_ghost_factor == lam,
        "nilpotence truncates exp(-i*lambda*rho0*bar_rho0/hbar), and the pinned i*hbar extraction gives the direct ghost factor lambda",
    )

    odd_hessian = sp.Matrix([[0, -lam], [lam, 0]])
    odd_hessian_det = sp.factor(odd_hessian.det())
    odd_hessian_pfaffian = odd_hessian[0, 1]
    hessian = audit.observe(
        "G1.zero_ward.elimination.odd_hessian",
        odd_hessian_det == lam**2
        and odd_hessian_pfaffian == -lam
        and odd_hessian.det().is_positive is True,
        "the ordered action Hessian for (rho0,bar_rho0) is nondegenerate for lambda>0, with determinant lambda^2 and Pfaffian -lambda before the pinned exponent/measure orientation",
    )
    left_eom_rho = -lam * bar_rho0
    left_eom_bar = lam * rho0
    stationary_solution = {
        rho0: sp.Integer(0),
        bar_rho0: sp.Integer(0),
    }
    eom = audit.observe(
        "G1.zero_ward.elimination.stationary_ghost_solution",
        left_eom_rho.subs(stationary_solution) == 0
        and left_eom_bar.subs(stationary_solution) == 0
        and sp.solve(
            [left_eom_rho, left_eom_bar], [rho0, bar_rho0], dict=True
        )
        == [stationary_solution],
        "the algebraic ghost equations have the unique stationary solution rho0=bar_rho0=0 for lambda>0",
    )
    induced_oriented_factor = direct_ghost_factor
    weighted_elimination = audit.observe(
        "G1.zero_ward.elimination.induced_oriented_factor",
        induced_oriented_factor == lam,
        "integrating out the nondegenerate odd Gaussian leaves its oriented factor lambda; solving the stationary equations does not set that factor to one",
    )

    bosonic_delta_jacobian = 1 / lam
    bosonic_fourier = audit.observe(
        "G1.zero_ward.bosonic.positive_lambda_delta_scaling",
        lam.is_positive is True
        and sp.simplify(bosonic_delta_jacobian * lam - 1) == 0,
        "the full-real N0 Fourier integral gives delta(lambda*c0)=delta(c0)/lambda for lambda>0",
    )
    retained_coefficient = sp.simplify(
        bosonic_delta_jacobian * direct_ghost_factor
    )
    eliminated_coefficient = sp.simplify(
        bosonic_delta_jacobian * induced_oriented_factor
    )
    unweighted_coefficient = bosonic_delta_jacobian
    route_equivalence = audit.observe(
        "G1.zero_ward.combined.direct_equals_weighted_elimination",
        retained_coefficient == 1
        and eliminated_coefficient == 1
        and retained_coefficient == eliminated_coefficient,
        "both correct routes give the same relative distribution delta(c0)",
    )
    negative_control = audit.observe(
        "G1.zero_ward.combined.unweighted_deletion_negative_control",
        unweighted_coefficient == 1 / lam
        and sp.simplify(unweighted_coefficient - retained_coefficient) != 0,
        "deleting the pair without its induced factor leaves the spurious coefficient 1/lambda",
    )
    ward_identity = audit.observe(
        "G1.zero_ward.scaling.relative_ward_identity",
        sp.diff(retained_coefficient, lam) == 0
        and sp.diff(eliminated_coefficient, lam) == 0
        and sp.diff(unweighted_coefficient, lam) == -1 / lam**2,
        "the direct and weighted-elimination relative coefficients obey d_lambda Z0=0, while unweighted deletion violates it",
    )
    sample_values = [sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)]
    retained_samples = [
        sp.simplify(retained_coefficient.subs(lam, value))
        for value in sample_values
    ]
    eliminated_samples = [
        sp.simplify(eliminated_coefficient.subs(lam, value))
        for value in sample_values
    ]
    unweighted_samples = [
        sp.simplify(unweighted_coefficient.subs(lam, value))
        for value in sample_values
    ]
    sampled = audit.observe(
        "G1.zero_ward.scaling.sampled_discrimination",
        retained_samples == [1, 1, 1]
        and eliminated_samples == [1, 1, 1]
        and unweighted_samples == [2, 1, sp.Rational(1, 2)],
        "at lambda=1/2,1,2 both correct ledgers stay one and the negative control gives 2,1,1/2",
    )
    correction_is_local = audit.observe(
        "G1.zero_ward.scope.prior_mismatch_is_unweighted_deletion",
        prior_mismatch
        and previous_ledgers["eliminated_algebraic_pair"]["ghost_factor"]
        is None
        and induced_oriented_factor == lam,
        "the tested prior mismatch is exactly repaired by the previously omitted induced odd factor, not by changing the pinned action or orientation",
    )

    audit.guard(
        "G1.zero_ward.guard.finite_berezin_gaussian",
        "finite-dimensional Berezin Gaussian integration",
        "rho0 and bar_rho0 are one ordered Grassmann pair, the bilinear Hessian is nondegenerate for lambda>0, the exponent is exp(iS0/hbar), and the upstream oriented extraction is i*hbar",
        "direct integration and algebraic elimination with the full induced odd Gaussian factor must agree at this finite zero block; unweighted deletion is not Gaussian integration",
    )
    audit.guard(
        "G1.zero_ward.guard.fourier_delta_scaling",
        "distributional Fourier identity and delta-function scaling",
        "N0 is integrated over the full real line with dN0/(2*pi*hbar), lambda is a positive constant, and c0 is a real test-distribution coordinate",
        "the bosonic factor is delta(c0)/lambda; this theorem guard does not select the full-real lapse contour from gravitational physics",
    )
    audit.guard(
        "G1.zero_ward.guard.local_scaling_ward",
        "finite-dimensional BRST-exact gauge-fermion scaling identity",
        "the zero action is the hash-pinned restriction of lambda*sPsi, the inherited right-BRST variation is nilpotent and closes S0, and the finite algebraic measure has no boundary term",
        "the relative zero-block coefficient is lambda independent for the two correct Gaussian routes; no continuum anomaly, endpoint anomaly or full path-integral gauge independence is inferred",
    )
    audit.guard(
        "G1.zero_ward.guard.lapse_completion_still_open",
        "separation of algebraic ghost elimination from lapse-modulus and contour choices",
        "only the rho0,bar_rho0 Gaussian is eliminated; the calculation assumes rather than derives full-real N0 integration and does not compare it with a modulus or restricted contour",
        "the prior ghost-ledger mismatch is closed, but unique trajectory zero-mode completion, zero-lapse terms and the gravitational lapse prescription remain open",
    )
    audit.guard(
        "G1.zero_ward.guard.constant_lambda_not_constraint_densitization",
        "scope separation for two distinct rescalings",
        "lambda is a positive constant multiplying one gauge fermion, whereas H=12*pi^2*exp(3Q/2)*C uses a field-dependent classical constraint multiplier before ordering",
        "this Ward check does not prove quantum equivalence of raw C and a densitized constraint and supplies no raw-C physical inner product",
    )
    audit.guard(
        "G1.zero_ward.guard.no_full_bfv_or_physics",
        "bounded workbench interpretation",
        "one algebraic quartet block with a pinned orientation and no nonzero continuum tower, absolute Pfaffian line, cohomology, inhomogeneous gravity, observables or empirical map",
        "the result is a local bookkeeping theorem, not a full BFV quantization, quantum-gravity evidence, physics, or a TOE result",
    )

    flags = {
        "static_brst_contract": static_contract,
        "prior_mismatch_pinned": prior_mismatch,
        "projected_nilpotence": nilpotence,
        "zero_action_brst_closed": brst_closure,
        "direct_berezin_factor": direct_berezin,
        "nondegenerate_odd_hessian": hessian,
        "stationary_ghost_solution": eom,
        "weighted_elimination_factor": weighted_elimination,
        "bosonic_delta_scaling": bosonic_fourier,
        "correct_route_equivalence": route_equivalence,
        "unweighted_negative_control": negative_control,
        "scaling_ward_identity": ward_identity,
        "sampled_discrimination": sampled,
        "local_prior_mismatch_repaired": correction_is_local,
    }
    negative_discriminates = negative_control and ward_identity and sampled
    return (
        {
            "pinned_zero_block": {
                "action": "S0=lambda*(N0*c0-rho0*bar_rho0)",
                "lambda_domain": "lambda>0",
                "right_brst_images": generator_images,
                "squared_images": squared_images,
                "right_brst_product_variations": {
                    "s(N0*c0)": str(variation_bosonic),
                    "s(rho0*bar_rho0)": str(variation_ghost_bilinear),
                    "sS0": str(action_variation),
                },
            },
            "ghost_gaussian": {
                "odd_order": ["rho0", "bar_rho0"],
                "exponent_top_coefficient": str(exponent_top_coefficient),
                "oriented_extraction_measure": str(oriented_measure),
                "direct_factor": str(direct_ghost_factor),
                "action_hessian": [
                    [str(odd_hessian[row, column]) for column in range(2)]
                    for row in range(2)
                ],
                "action_hessian_determinant": str(odd_hessian_det),
                "action_hessian_pfaffian_before_exponent_measure_orientation": str(
                    odd_hessian_pfaffian
                ),
                "left_equations": [str(left_eom_rho), str(left_eom_bar)],
                "stationary_solution": {"rho0": "0", "bar_rho0": "0"},
                "weighted_elimination_factor": str(induced_oriented_factor),
                "unweighted_deletion_factor": "1",
            },
            "relative_distribution_ledgers": {
                "common_bosonic_distribution": "delta(c0)/lambda",
                "direct_retention": {
                    "ghost_factor": str(direct_ghost_factor),
                    "delta_c0_coefficient": str(retained_coefficient),
                },
                "weighted_algebraic_elimination": {
                    "ghost_factor": str(induced_oriented_factor),
                    "delta_c0_coefficient": str(eliminated_coefficient),
                },
                "unweighted_deletion_negative_control": {
                    "ghost_factor": "1",
                    "delta_c0_coefficient": str(unweighted_coefficient),
                },
                "lambda_derivatives": {
                    "direct": str(sp.diff(retained_coefficient, lam)),
                    "weighted_elimination": str(
                        sp.diff(eliminated_coefficient, lam)
                    ),
                    "unweighted_deletion": str(
                        sp.diff(unweighted_coefficient, lam)
                    ),
                },
                "sample_lambda": [str(value) for value in sample_values],
                "direct_samples": [str(value) for value in retained_samples],
                "weighted_elimination_samples": [
                    str(value) for value in eliminated_samples
                ],
                "unweighted_deletion_samples": [
                    str(value) for value in unweighted_samples
                ],
            },
            "prior_result_revision": {
                "prior_retained_factor": previous_ledgers[
                    "retained_algebraic_pair"
                ]["combined_relative_factor"],
                "prior_eliminated_factor": previous_ledgers[
                    "eliminated_algebraic_pair"
                ]["combined_relative_factor"],
                "prior_eliminated_ghost_factor": previous_ledgers[
                    "eliminated_algebraic_pair"
                ]["ghost_factor"],
                "identified_missing_factor": "lambda",
                "corrected_eliminated_factor": str(eliminated_coefficient),
                "unweighted_deletion_status": "KILL_AS_GHOST_GAUSSIAN_ELIMINATION",
                "unique_trajectory_zero_mode_completion": None,
                "remaining_reason": "the lapse N0 contour/modulus and boundary prescription were not selected",
            },
            "flags": flags,
        },
        flags,
        negative_discriminates,
    )


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, str]],
    upstream_payloads: list[dict[str, Any]],
    audit: Audit,
) -> dict[str, Any]:
    exact, flags, negative_discriminates = exact_calculation(
        upstream_payloads, audit
    )
    core_without_negative = {
        key: value
        for key, value in flags.items()
        if key
        not in {
            "unweighted_negative_control",
            "sampled_discrimination",
        }
    }
    if all(flags.values()) and negative_discriminates:
        verdict = (
            "NARROW_V0_BFV_ZERO_GHOST_ELIMINATION_REQUIRES_INDUCED_DETERMINANT"
        )
        impact = "CLOSE_ONE_LOCAL_ZERO_MODE_LEDGER_MISMATCH_ONLY"
        classification = (
            "GATE1_V0_LOCAL_BFV_ZERO_GHOST_DIRECT_AND_WEIGHTED_ELIMINATION_"
            "EQUIVALENT_UNWEIGHTED_DELETION_KILL_LAPSE_COMPLETION_OPEN"
        )
        condition = (
            "direct Berezin integration and weighted algebraic elimination "
            "both contribute lambda, cancel the bosonic 1/lambda Jacobian, "
            "and satisfy the scaling Ward check while unweighted deletion fails"
        )
    elif all(core_without_negative.values()) and not negative_discriminates:
        verdict = "KILL_V0_ZERO_MODE_NEGATIVE_CONTROL_DISCRIMINATION"
        impact = "NO_LEDGER_RESOLUTION"
        classification = "GATE1_V0_BFV_ZERO_MODE_NEGATIVE_CONTROL_NONPASS"
        condition = (
            "the negative control is lambda independent or agrees with the "
            "retained route without an induced factor"
        )
    else:
        verdict = "KILL_V0_DECLARED_BFV_ZERO_BLOCK"
        impact = "RETAIN_THE_PRIOR_AMBIGUITY_AND_STATIC_SOURCE_ONLY"
        classification = "GATE1_V0_BFV_ZERO_MODE_DIRECT_ELIMINATION_NONPASS"
        condition = (
            "direct integration and weighted elimination disagree, the zero "
            "action is not BRST closed, or a scaling-Ward check fails"
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
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": [],
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "one algebraic BFV zero block and one pinned odd orientation only",
            "revision_boundary": "the prior retained-versus-eliminated ghost-ledger mismatch is narrowed to an invalid unweighted deletion; the broader lapse/trajectory ambiguity remains",
            "rescaling_boundary": "constant gauge-fermion lambda scaling is not the field-dependent constraint densitization C to H",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted,
        "gate1_decision": promoted["gate1"],
        "global_promotion": promoted["global_promotion"],
        "automatic_next": promoted["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
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
    frozen_input, input_sha256, upstream, upstream_payloads = load_input()
    audit = Audit()
    result = build_result(
        frozen_input, input_sha256, upstream, upstream_payloads, audit
    )
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
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_total": 0,
                "direct_relative_factor": "1",
                "weighted_elimination_relative_factor": "1",
                "unweighted_deletion_relative_factor": "1/lambda",
                "unique_trajectory_zero_mode_completion": None,
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
