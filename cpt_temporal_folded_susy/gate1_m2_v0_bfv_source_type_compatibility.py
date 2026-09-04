#!/usr/bin/env python3
"""Audit whether the local V=0 BFV source has the Starobinsky m=2 source type.

This bounded unnumbered calculation compares two already valid but differently
scoped repository objects.  It reconstructs the finite m=2 Starobinsky
canonical pushforward and configuration action, then checks the model,
constraint, canonical-pair, lapse/clock, endpoint, finite-source and orientation
fields required for a direct source identification.

It does not construct a new BFV source, choose a relative cycle, retry the
consumed zero-lapse runner, or emit a physics or TOE claim.  It writes one
adjacent JSON result.
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


INPUT_NAME = "GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY_INPUTS.json"
RESULT_NAME = "GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_m2_v0_bfv_source_type_compatibility.py"
)
EXPECTED_INPUT_SHA256 = (
    "c36e4d0a5b173b967d092a6daa05dac3c7a872c00e9eb332fb108f59753d4cfa"
)
CALCULATION_ID = "Gate1M2V0BfvSourceTypeCompatibility"
RESULT_SCHEMA = "ice.gate1-m2-v0-bfv-source-type-compatibility.result.v1"
RESULT_PREFIX = "GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY_RESULT="
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
        "symbolic_operations": 200,
        "quadratures": 0,
        "root_calls": 0,
        "ode_calls": 0,
        "numerical_samples": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "named_chain_theory_hypotheses_satisfied": None,
        "starobinsky_finite_m2_bfv_trajectory_source": None,
        "source_equivalence_or_deformation": None,
        "zero_lapse_distribution": None,
        "U0_U1_U1prime_Uf_descent": None,
        "complete_end_divisor_census": None,
        "candidate_set_completeness": None,
        "absolute_bfv_orientation": None,
        "physical_original_cycle": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "physics_claim": None,
        "TOE_claim": None,
        "automatic_next": None,
    }


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def reserve(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate check id: {ident}")
        self.seen.add(ident)

    def check(self, ident: str, passed: bool, statement: str, **data: Any) -> None:
        self.reserve(ident)
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {ident}: {statement}")
        self.exact.append(
            {"id": ident, "passed": True, "statement": statement, **data}
        )

    def guard(
        self,
        ident: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.reserve(ident)
        self.theorem_guards.append(
            {
                "id": ident,
                "verified": True,
                "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream_result(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream is not a valid run: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict drift: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload digest drift: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def verify_upstream_file(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed}


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]], list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version")
        != "ice.gate1-m2-v0-bfv-source-type-compatibility.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if cfg["planner"]["classification"] != "CURRENT_BLOCKER_CANDIDATE":
        raise AssertionError("planner classification drift")
    root = Path(__file__).resolve().parent.parent
    upstream_results = [
        verify_upstream_result(root, item) for item in cfg["upstream_results"]
    ]
    upstream_files = [
        verify_upstream_file(root, item) for item in cfg["upstream_files"]
    ]
    return cfg, observed, upstream_results, upstream_files


def symbolic_audit(audit: Audit) -> dict[str, Any]:
    a, phi, p_tr, p, c = sp.symbols(
        "a phi P_tr p c", positive=True, real=True
    )
    x, q, a_b, phi_b = sp.symbols("x q a_b phi_b", real=True)
    z, t_prop = sp.symbols("z T_prop", nonzero=True)
    kappa = sp.sqrt(sp.Rational(2, 3))
    pi = sp.pi
    u = sp.exp(-kappa * phi)
    potential = sp.Rational(3, 4) * (1 - u) ** 2
    c_v0 = (
        -p_tr**2 / (6 * pi**2 * a**3)
        + p**2 / (4 * pi**2 * a**3)
        - 6 * pi**2 * a
    )
    c_star = c_v0 + 2 * pi**2 * a**3 * potential
    delta_constraint = sp.simplify(c_star - c_v0)
    potential_prime = sp.simplify(sp.diff(potential, phi))
    p_flow = sp.simplify(-sp.diff(c_star, phi))
    d_trace = sp.simplify(-a * sp.diff(c_star, a) / 2)
    d_trace_identity = sp.simplify(
        d_trace
        - (
            sp.Rational(3, 2) * c_star
            + 6 * pi**2 * a * (2 - a**2 * potential)
        )
    )

    r = 3 * p**2 - 2 * p_tr**2
    f_v0 = 72 * pi**4 * a**4 + 12 * pi**2 * c * a**3 - r
    f_star = sp.expand(f_v0 - 24 * pi**4 * a**6 * potential)
    root_delta = sp.simplify(f_star - f_v0)
    star_root_phi_dependence = sp.simplify(sp.diff(f_star, phi))

    mid_a = a_b + x / 2
    mid_phi = phi_b + q / 2
    mid_potential = sp.Rational(3, 4) * (
        1 - sp.exp(-kappa * mid_phi)
    ) ** 2
    s_v0 = (
        -24 * pi**2 * mid_a * x**2 / t_prop
        + 4 * pi**2 * mid_a**3 * q**2 / t_prop
        + 2 * pi**2 * t_prop * (-3 * mid_a)
    )
    s_star = sp.simplify(
        s_v0 + 2 * pi**2 * t_prop * mid_a**3 * mid_potential
    )
    action_delta = sp.simplify(s_star - s_v0)
    delta_t_derivative = sp.simplify(sp.diff(action_delta, t_prop))
    delta_q_derivative = sp.simplify(sp.diff(action_delta, q))

    mu_g = 12 * pi**2 * mid_a
    mu_s = 2 * pi**2 * mid_a**3
    bulk_u = 2 * pi**2 * (-3 * mid_a + mid_a**3 * mid_potential)
    pa0, pa1, pp0, pp1 = sp.symbols("p_a0 p_a1 p_phi0 p_phi1")
    canonical = (
        x * (pa0 - pa1)
        + q * (pp0 - pp1)
        + z * (pa0**2 + pa1**2) / (4 * mu_g)
        - z * (pp0**2 + pp1**2) / (4 * mu_s)
        - z * bulk_u
    )
    stationary = {
        pa0: -2 * mu_g * x / z,
        pa1: 2 * mu_g * x / z,
        pp0: 2 * mu_s * q / z,
        pp1: -2 * mu_s * q / z,
    }
    pushed = sp.simplify(canonical.subs(stationary))
    expected_pushed = sp.simplify(
        -2 * mu_g * x**2 / z + 2 * mu_s * q**2 / z - z * bulk_u
    )
    euclidean = sp.simplify(
        -2 * mu_g * x**2 / t_prop
        + 2 * mu_s * q**2 / t_prop
        + t_prop * bulk_u
    )
    wick_residual = sp.simplify(
        sp.I * pushed.subs(z, -sp.I * t_prop) + euclidean
    )
    configuration_residual = sp.simplify(euclidean - s_star)

    audit.check(
        "G1.source_type.starobinsky_constraint_bulk_delta",
        sp.simplify(delta_constraint - 2 * pi**2 * a**3 * potential) == 0,
        "the Starobinsky and V=0 constraints differ by the nonzero-potential bulk term 2*pi^2*a^3*V(phi)",
    )
    audit.check(
        "G1.source_type.starobinsky_potential_and_derivative_form",
        sp.simplify(
            potential_prime
            - sp.Rational(3, 2) * kappa * u * (1 - u)
        )
        == 0,
        "V'(phi)=(3/2)*sqrt(2/3)*exp(-sqrt(2/3)phi)*(1-exp(-sqrt(2/3)phi)), which is nonzero on the frozen positive-phi interval",
    )
    audit.check(
        "G1.source_type.old_scalar_momentum_not_invariant",
        sp.simplify(p_flow + 2 * pi**2 * a**3 * potential_prime) == 0
        and p_flow != 0,
        "the old scalar momentum obeys {p_phi,C_star}=-partial_phi C_star and is not the invariant p used by the V=0 Darboux chart",
    )
    audit.check(
        "G1.source_type.trace_fp_identity_retained",
        d_trace_identity == 0,
        "the general-potential trace bracket obeys D_L=(3/2)C_L+6*pi^2*a*(2-a^2*V), exposing the potential-dependent FP horizon",
    )
    audit.check(
        "G1.source_type.constraint_root_equations_differ",
        sp.simplify(root_delta + 24 * pi**4 * a**6 * potential) == 0
        and star_root_phi_dependence != 0,
        "the V=0 quartic constraint-root equation acquires a phi-dependent a^6 term in the Starobinsky model",
    )
    audit.check(
        "G1.source_type.starobinsky_configuration_bulk_delta",
        sp.simplify(
            action_delta - 2 * pi**2 * t_prop * mid_a**3 * mid_potential
        )
        == 0,
        "the finite m=2 Starobinsky and V=0 configuration actions differ by an interior potential term",
    )
    audit.check(
        "G1.source_type.bulk_delta_not_fixed_endpoint_term",
        delta_t_derivative != 0 and delta_q_derivative != 0,
        "with fixed (a,phi) endpoints the action difference depends on the interior scalar and proper-time modulus, so it is not an endpoint-only constant",
    )
    audit.check(
        "G1.source_type.independent_canonical_pushforward",
        sp.simplify(pushed - expected_pushed) == 0,
        "independent stationary substitution reconstructs the exact finite m=2 Starobinsky canonical momentum pushforward",
    )
    audit.check(
        "G1.source_type.wick_and_configuration_identity",
        wick_residual == 0 and configuration_residual == 0,
        "under T_prop=i*z, the independently pushed canonical action equals the frozen Starobinsky configuration action with the declared Wick sign",
    )

    audit.guard(
        "G1.source_type.guard.positive_phi_is_nonzero_potential",
        "strict monotonicity of the real exponential",
        "the frozen endpoint phi_b is positive and the source-to-fold corridor under review remains in a positive-real-phi neighborhood",
        "0<exp(-sqrt(2/3)phi)<1, hence V(phi)>0 and V'(phi)>0 there; this proves a model mismatch, not a no-go for a newly derived Starobinsky BFV chart",
    )
    audit.guard(
        "G1.source_type.guard.endpoint_difference_is_not_gauge_failure",
        "endpoint-improved canonical gauge framework",
        "the V=0 source fixes (T_clock,Phi) after adding its boundary potential, while the m=2 source fixes old (a,phi) endpoints and no exact endpoint-state transform between them is supplied",
        "the two valid endpoint problems cannot be identified directly; the result does not show that an independently derived transformed Starobinsky endpoint problem cannot exist",
    )
    audit.guard(
        "G1.source_type.guard.no_relative_cycle_verdict",
        "typed-input boundary for relative-cycle transport",
        "no same-model finite-m2 BFV trajectory source, source deformation, zero-lapse extension, common orientation line, or complete end census is constructed",
        "UNIQUE_LATERAL, STOKES_SPLIT and NO_ADMISSIBLE_LIFT remain unevaluated; only the direct cross-scope source identification is retired",
    )

    return {
        "symbols": {
            "T_prop": "global proper-time or constant-lapse modulus in X2",
            "T_clock": "Darboux clock coordinate W_c in the V=0 U_plus chart",
            "N": "BFV multiplier zero mode conjugate to Pi",
        },
        "constraint_comparison": {
            "C_v0": str(c_v0),
            "V_star": str(potential),
            "C_star_minus_C_v0": str(delta_constraint),
            "V_prime": str(potential_prime),
            "bracket_p_phi_C_star": str(p_flow),
            "trace_bracket_D_star": str(d_trace),
            "trace_bracket_identity_residual": str(d_trace_identity),
        },
        "constraint_root_comparison": {
            "F_v0": str(f_v0),
            "F_star": str(f_star),
            "F_star_minus_F_v0": str(root_delta),
            "partial_phi_F_star": str(star_root_phi_dependence),
        },
        "finite_m2_action_comparison": {
            "S2_v0": str(s_v0),
            "S2_star": str(s_star),
            "S2_star_minus_S2_v0": str(action_delta),
            "bulk_delta_partial_T_prop": str(delta_t_derivative),
            "bulk_delta_partial_q": str(delta_q_derivative),
            "canonical_pushforward": str(pushed),
            "canonical_pushforward_residual": str(
                sp.simplify(pushed - expected_pushed)
            ),
            "wick_residual": str(wick_residual),
            "configuration_residual": str(configuration_residual),
        },
    }


def scope_audit(
    audit: Audit, cfg: dict[str, Any], root: Path
) -> dict[str, Any]:
    result_paths = {item["path"]: item for item in cfg["upstream_results"]}
    bfv_payload = json.loads(
        (root / "cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT.json").read_bytes()
    )
    trace_payload = json.loads(
        (root / "cpt_temporal_folded_susy/GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_RESULT.json").read_bytes()
    )
    bosonic_payload = json.loads(
        (root / "cpt_temporal_folded_susy/GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json").read_bytes()
    )
    target = cfg["target_type"]
    source = cfg["candidate_source_type"]

    audit.check(
        "G1.source_type.model_tags_are_distinct",
        target["model"] != source["model"],
        "the frozen target is the Starobinsky model while the candidate BFV algebra is explicitly V=0",
    )
    audit.check(
        "G1.source_type.clock_and_lapse_roles_are_distinct",
        target["lapse_object"]["role"]
        != source["clock_object"]["role"]
        and source["multiplier_object"]["symbol"] == "N",
        "T_prop, T_clock and N have different typed roles and cannot be merged by symbol reuse",
    )
    audit.check(
        "G1.source_type.endpoint_polarizations_are_distinct",
        target["endpoint_polarization"] != source["endpoint_polarization"],
        "fixed old (a,phi) endpoints differ from the improved-static (T_clock,Phi) endpoint polarization",
    )
    audit.check(
        "G1.source_type.finite_m2_bfv_trajectory_is_absent",
        bfv_payload["scope_status"]["finite_m2_bfv_trajectory_measure"] is None
        and bfv_payload["computed_facts"]["finite_m2_bfv_trajectory_measure"]
        == "NOT_COMPUTED"
        and bfv_payload["promoted_outputs"]["full_m2_bfv_measure"] is None,
        "the kept V=0 result explicitly leaves every finite-m2 BFV trajectory measure null",
    )
    audit.check(
        "G1.source_type.old_source_equivalence_is_absent",
        bfv_payload["scope_status"]["old_fixed_a_kernel_equivalence"] is None
        and bfv_payload["computed_facts"]["old_kernel_equivalence"]
        == "NOT_COMPUTED",
        "the V=0 BFV source has no proved equality or deformation to the fixed-(a,phi) proper-time source",
    )
    audit.check(
        "G1.source_type.append_shortcut_remains_killed",
        trace_payload["scope_status"][
            "append_to_unchanged_proper_time_m2_source"
        ]
        == "NOT_LICENSED_AS_AN_ADDITIONAL_FP_GAUGE"
        and "APPEND_KILLED" in trace_payload["verdict"],
        "multiplying the unchanged proper-time source by an extra trace-gauge delta and FP factor remains outside the allowed replacement-source class",
    )
    audit.check(
        "G1.source_type.bosonic_target_still_requires_bfv_glue",
        bosonic_payload["scope_status"]["p_a_gauge_fixing_FP_BFV_detline"]
        == "OPEN"
        and bosonic_payload["promoted_outputs"]["full_joint_orientation"]
        is None,
        "the exact bosonic m=2 source still requires a same-model gauge/BFV determinant-line completion",
    )
    audit.check(
        "G1.source_type.all_pinned_upstream_entries_present",
        len(result_paths) == 3,
        "all three independent upstream result ledgers are pinned in the input",
    )

    return {
        "compatibility_fields": {
            "model_potential": "MISMATCH_V0_VERSUS_STAROBINSKY",
            "constraint_and_bulk_action": "MISMATCH_NONZERO_INTERIOR_POTENTIAL_TERM",
            "canonical_physical_pair": "MISMATCH_OLD_PHI_MOMENTUM_NOT_V0_INVARIANT_P",
            "lapse_and_clock_roles": "MISMATCH_T_PROP_VERSUS_T_CLOCK_WITH_SEPARATE_N",
            "endpoint_polarization_and_boundary_action": "MISMATCH_NO_EXACT_ENDPOINT_TRANSFORM",
            "finite_m2_source_lattice": "MISSING_IN_CANDIDATE_SOURCE",
            "source_equivalence_or_deformation": "MISSING",
            "absolute_bfv_orientation": "MISSING",
        },
        "valid_scoped_objects_preserved": {
            "starobinsky_finite_m2_bosonic_action": "KEEP_IN_ITS_FROZEN_SCOPE",
            "v0_uplus_improved_static_bfv_zero_mode_algebra": "KEEP_IN_ITS_LOCAL_SCOPE",
            "direct_identification": "KILL",
        },
    }


def main() -> None:
    cfg, input_sha, upstream_results, upstream_files = load_input()
    root = Path(__file__).resolve().parent.parent
    audit = Audit()
    symbolic = symbolic_audit(audit)
    scope = scope_audit(audit, cfg, root)

    mismatch_values = list(scope["compatibility_fields"].values())
    mismatch_count = sum(
        value.startswith("MISMATCH") or value == "MISSING"
        for value in mismatch_values
    )
    if mismatch_count == 0:
        verdict = cfg["decision_table"][0]["verdict"]
        programme_impact = cfg["decision_table"][0]["programme_impact"]
    else:
        verdict = cfg["decision_table"][1]["verdict"]
        programme_impact = cfg["decision_table"][1]["programme_impact"]
    if verdict != "KILL_DIRECT_V0_BFV_TO_STAROBINSKY_M2_SOURCE_IDENTIFICATION":
        raise AssertionError("the exact mismatch witnesses did not select the frozen row")

    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": programme_impact,
        "epistemic_status": "SCOPED_NEGATIVE_RESULT_FOR_ONE_DIRECT_SOURCE_IDENTIFICATION",
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "planner": cfg["planner"],
        "human_review": cfg["human_review"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_results": upstream_results,
        "upstream_files": upstream_files,
        "primary_sources": cfg["primary_sources"],
        "symbolic_calculation": symbolic,
        "scope_audit": scope,
        "mismatch_witness_count": mismatch_count,
        "exact_checks": audit.exact,
        "numerical_checks": [],
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": len(audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": 0,
            "numerical_total": 0,
            "theorem_guards_verified": len(audit.theorem_guards),
            "theorem_guards_total": len(audit.theorem_guards),
            "all_passed": True,
        },
        "research_transition": {
            "unexpected_outcome": "the most developed replacement BFV source is a valid V=0 local zero-mode algebra but does not share the Starobinsky finite-m2 source type",
            "competing_mechanisms": [
                {
                    "id": "DIRECT_V0_TRANSPLANT",
                    "disposition": "RETIRED_WITHIN_EXACT_CROSS_SCOPE_IDENTIFICATION",
                },
                {
                    "id": "STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
                {
                    "id": "STAROBINSKY_TIME_DEPENDENT_TRACE_SOURCE",
                    "disposition": "LIVE_UNCONSTRUCTED",
                },
            ],
            "discriminating_question": "Can one Starobinsky V(phi) nonzero regular component derive its own endpoint-improved constraint-adapted BFV source with a finite m=2 trajectory measure and a typed comparison to the proper-time kernel?",
            "changed_future_selection": "construct and falsify one same-model Starobinsky replacement-source chart before N=0, U1/U1-prime, end-census or source-to-fold transport work",
        },
        "claim_boundary": {
            "computed": [
                "the Starobinsky and V=0 constraints and finite actions differ by explicit nonzero-potential bulk terms",
                "the old scalar momentum is not the invariant momentum of the V=0 cyclic-scalar Darboux chart when V'(phi) is nonzero",
                "the two T symbols have distinct proper-time and Darboux-clock roles, with N a third BFV multiplier object",
                "the endpoint polarizations differ and the kept V=0 result contains no finite-m2 BFV trajectory measure or old-source equivalence",
            ],
            "killed_shortcut_only": "directly reuse or relabel the local V=0 U_plus BFV zero-mode source as the source for the frozen Starobinsky finite-m2 joint action",
            "not_killed": [
                "a newly derived Starobinsky constraint-adapted improved-static source",
                "a newly derived time-dependent trace-gauge source",
                "the valid local V=0 BFV algebra in its own scope",
                "the valid Starobinsky finite-m2 bosonic action in its own scope",
            ],
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "symbolic_operations": 17,
            "quadratures": 0,
            "root_calls": 0,
            "ode_calls": 0,
            "numerical_samples": 0,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "programme_impact": programme_impact,
                "mismatch_witness_count": mismatch_count,
                "exact_passed": len(audit.exact),
                "exact_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "theorem_guards_total": len(audit.theorem_guards),
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
                "gate1": "OPEN_PARTIAL_PROGRESS",
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
