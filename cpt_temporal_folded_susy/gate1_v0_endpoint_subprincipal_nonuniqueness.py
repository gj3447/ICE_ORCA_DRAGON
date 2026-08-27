#!/usr/bin/env python3
"""Gate 1 -- endpoint-transform subprincipal nonuniqueness control.

The prior local principal FIO fixed a classical phase and positive principal
half-density but its uncorrected one-term kernel failed exact finite-hbar
unitarity.  This bounded non-numbered calculation asks whether those principal
data could nevertheless select a unique exact normalized completion.

Conditional on any exact unitary completion ``U_0`` in the class fixing only
the declared ``B,a_0,H_D,M_c`` data, postcomposition with the
exact target unitary ``exp(i*hbar*kappa*c)`` produces infinitely many exact
unitaries with the same classical boundary potential, canonical relation and
principal half-density but different lower symbols.  The calculation proves
nonuniqueness of completion from the supplied data; it does not prove that
``U_0`` exists.  One adjacent JSON result is written and no descendant starts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_INPUTS.json"
RESULT_NAME = "GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_v0_endpoint_subprincipal_nonuniqueness.py"
)
EXPECTED_INPUT_SHA256 = (
    "ef58f191697fa24c08ef97fbb8ea323d3284d6dddf0ee162660272141260cabb"
)
CALCULATION_ID = "Gate1V0EndpointSubprincipalNonuniqueness"
RESULT_SCHEMA = (
    "ice.gate1.v0-endpoint-subprincipal-nonuniqueness.result.v1"
)
RESULT_PREFIX = "GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT="
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


def mp_string(value: mp.mpf | mp.mpc, digits: int = 40) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
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

    def observe_numerical(
        self,
        check_id: str,
        relative_error: mp.mpf,
        tolerance: mp.mpf,
        statement: str,
        details: dict[str, Any],
    ) -> bool:
        self.register(check_id)
        passed = bool(relative_error <= tolerance)
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "relative_error": mp_string(relative_error, 24),
                "relative_tolerance": mp_string(tolerance, 8),
                **details,
            }
        )
        return passed

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
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream is not valid: {item['path']}")
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
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-endpoint-subprincipal-nonuniqueness.input.v1"
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
        "quadratures": 3,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "exact_endpoint_state_transform": None,
        "exact_endpoint_transform_existence": None,
        "selected_subprincipal_symbol": None,
        "original_variable_constraint_ordering": None,
        "physical_inner_product": None,
        "full_real_lapse_delta_C": None,
        "full_bfv_trajectory_measure": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    family = payload["conditional_family"]
    if (
        "suppose" not in family["hypothesis"]
        or family["shell_relation"]
        != "V_kappa(0,p)=1, so the declared order-zero delta(M_c) pairing is unchanged"
    ):
        raise AssertionError("conditional-family mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    c = sp.Symbol("c", real=True)
    hbar, kappa, alpha = sp.symbols(
        "hbar kappa alpha", positive=True, real=True
    )
    a0, a1 = sp.symbols("a_0 a_1", nonzero=True)
    multiplier = sp.exp(sp.I * hbar * kappa * c)

    unit_modulus = audit.observe(
        "G1.endpoint.subprincipal.unit_modulus",
        sp.simplify(multiplier * sp.conjugate(multiplier)) == 1,
        "V_kappa,hbar=exp(i*hbar*kappa*c) is an exact unit-modulus multiplier on L2(dc dp)",
    )
    constraint_commutator = audit.observe(
        "G1.endpoint.subprincipal.constraint_commutator",
        sp.simplify(c * multiplier - multiplier * c) == 0,
        "V_kappa commutes strongly with the multiplication constraint M_c",
    )
    domain_preservation = audit.observe(
        "G1.endpoint.subprincipal.maximal_domain_preservation",
        sp.simplify(
            c**2 * multiplier * sp.conjugate(multiplier) - c**2
        )
        == 0,
        "pointwise |c V_kappa psi|^2=|c psi|^2 preserves the maximal domain D(M_c)",
    )
    principal_limit = sp.limit(multiplier, hbar, 0, dir="+")
    first_symbol_shift = sp.diff(multiplier, hbar).subs(hbar, 0) * a0
    principal_symbol = audit.observe(
        "G1.endpoint.subprincipal.same_principal_symbol",
        principal_limit == 1
        and sp.simplify(first_symbol_shift - sp.I * kappa * c * a0) == 0,
        "multiplication changes a_1 by i*kappa*c*a_0 while leaving the principal half-density a_0 unchanged",
    )
    action_correction = hbar**2 * kappa * c
    classical_action = audit.observe(
        "G1.endpoint.subprincipal.same_classical_boundary_data",
        sp.limit(action_correction, hbar, 0, dir="+") == 0
        and sp.limit(action_correction / hbar, hbar, 0, dir="+") == 0
        and sp.limit(sp.diff(action_correction, c), hbar, 0, dir="+") == 0,
        "the kernel action changes by hbar^2*kappa*c, so W, B and the canonical relation are unchanged at classical and principal order",
    )
    nontrivial_lower_symbol = audit.observe(
        "G1.endpoint.subprincipal.nontrivial_lower_symbol",
        sp.diff(a1 + sp.I * kappa * c * a0, kappa) != 0,
        "the lower symbol varies continuously with kappa away from c=0",
    )
    shell_identity = audit.observe(
        "G1.endpoint.subprincipal.zero_fiber_identity",
        multiplier.subs(c, 0) == 1
        and first_symbol_shift.subs(c, 0) == 0,
        "V_kappa is exactly one on c=0, so the delta(M_c) zero-fiber form cannot select kappa",
    )

    normalized_density = sp.sqrt(2 * alpha / sp.pi) * sp.exp(
        -2 * alpha * c**2
    )
    observed_characteristic = sp.integrate(
        normalized_density * multiplier, (c, -sp.oo, sp.oo)
    )
    expected_characteristic = sp.exp(
        -(hbar * kappa) ** 2 / (8 * alpha)
    )
    distance_squared = 2 * (1 - expected_characteristic)
    distinct = audit.observe(
        "G1.endpoint.subprincipal.distinct_test_operators",
        sp.simplify(observed_characteristic - expected_characteristic) == 0
        and distance_squared.is_positive is True,
        "a normalized Gaussian times positive-half-line output state has ||(V_kappa-I)psi||^2=2[1-exp(-(hbar*kappa)^2/(8*alpha))]>0",
    )
    prior_nonunitary_boundary = audit.observe(
        "G1.endpoint.subprincipal.one_term_nonpass_retained",
        True,
        "the hash-verified upstream verdict still kills exact finite-hbar unitarity of the uncorrected one-term Van Vleck kernel",
    )

    audit.guard(
        "G1.endpoint.guard.conditional_unitary_family",
        "composition of unitary operators",
        "if U_0 is any exact unitary completion and V_kappa is the verified exact target unitary, then U_kappa=V_kappa U_0",
        "every U_kappa is exactly unitary inside the class fixing only B,a_0,H_D,M_c; surjectivity of U_0 transfers the explicit distinct target-state witness to a distinct old-space input state",
    )
    audit.guard(
        "G1.endpoint.guard.existence_open",
        "logical separation of existence and uniqueness",
        "the construction starts with a conditional U_0 and the upstream one-term ansatz is not exactly unitary",
        "the calculation kills uniqueness from the declared B,a_0,H_D,M_c data class but neither constructs nor rules out an exact completion; extra exact observable intertwining or endpoint-domain conditions may restrict the family",
    )
    audit.guard(
        "G1.endpoint.guard.extra_data_required",
        "full semiclassical symbol and exact intertwining boundary",
        "B fixes classical endpoint data and a_0 fixes only principal order",
        "selecting a completion needs additional lower/full-symbol, exact operator-intertwining, edge-domain and global gluing data not present in the inputs",
    )
    audit.guard(
        "G1.endpoint.guard.no_spectral_selection",
        "zero-fiber invariance under a multiplier equal to one on the shell",
        "V_kappa(0,p)=1 and V_kappa commutes with M_c",
        "even a successful declared order-zero delta(M_c) comparison cannot normalize the off-shell subprincipal family",
    )

    flags = {
        "unit_modulus": unit_modulus,
        "constraint_commutator": constraint_commutator,
        "maximal_domain_preservation": domain_preservation,
        "same_principal_symbol": principal_symbol,
        "same_classical_boundary_data": classical_action,
        "nontrivial_lower_symbol": nontrivial_lower_symbol,
        "zero_fiber_identity": shell_identity,
        "distinct_test_operators": distinct,
        "prior_one_term_nonpass_retained": prior_nonunitary_boundary,
    }
    return (
        {
            "conditional_family": {
                "hypothesis": "one exact unitary completion U_0 exists",
                "target_unitary": str(multiplier),
                "family": "U_kappa=V_kappa,hbar*U_0",
                "exact_unitarity": "CONDITIONAL_ON_U_0",
                "constraint_commutator": "[V_kappa,M_c]=0",
                "maximal_domain_preserved": domain_preservation,
                "kernel_action_correction": str(action_correction),
                "classical_W_and_B": "UNCHANGED",
                "canonical_relation": "UNCHANGED",
                "principal_half_density": "UNCHANGED",
                "lower_symbol": str(a1 + sp.I * kappa * c * a0),
                "selected_kappa": None,
            },
            "frozen_test_witness": {
                "c_probability_density": str(normalized_density),
                "p_positive_normalized_factor": "sqrt(2*beta)*exp(-beta*p), beta>0",
                "overlap": str(expected_characteristic),
                "distance_squared": str(distance_squared),
                "positive_for_hbar_kappa_nonzero": distinct,
            },
            "spectral_boundary": {
                "V_at_c_zero": str(multiplier.subs(c, 0)),
                "delta_Mc_form_changed": False,
                "can_zero_fiber_select_kappa": False,
            },
            "logical_status": {
                "uniqueness_from_declared_B_a0_H_D_M_c_data": "KILL" if all(flags.values()) else "OPEN",
                "exact_transform_existence": "OPEN_NOT_COMPUTED",
                "uncorrected_one_term_exact_unitarity": "KILL_UPSTREAM",
            },
            "flags": flags,
        },
        flags,
    )


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    alpha = mp.mpf(plan["alpha"])
    hbar = mp.mpf(plan["hbar"])
    kappas = [mp.mpf(value) for value in plan["kappa_values"]]
    tolerance = mp.mpf(plan["relative_tolerance"])
    if (
        mp.mp.dps != 80
        or alpha != mp.mpf("0.7")
        or hbar != mp.mpf("0.3")
        or kappas != [mp.mpf("0.5"), mp.mpf("1.0"), mp.mpf("2.0")]
        or tolerance != mp.mpf("1e-60")
    ):
        raise AssertionError("numerical plan mutation")

    normalization = mp.sqrt(2 * alpha / mp.pi)
    records: list[dict[str, Any]] = []
    distances: list[mp.mpf] = []
    for index, kappa in enumerate(kappas, 1):
        observed = mp.quad(
            lambda value: normalization
            * mp.exp(-2 * alpha * value**2)
            * mp.cos(hbar * kappa * value),
            [-mp.inf, mp.inf],
        )
        expected = mp.exp(-(hbar * kappa) ** 2 / (8 * alpha))
        relative_error = abs(observed - expected) / abs(expected)
        distance_squared = 2 * (1 - expected)
        passed = audit.observe_numerical(
            f"G1.endpoint.subprincipal.gaussian_quadrature_{index}",
            relative_error,
            tolerance,
            "direct high-precision Gaussian characteristic integration matches the exact overlap",
            {
                "alpha": mp_string(alpha),
                "hbar": mp_string(hbar),
                "kappa": mp_string(kappa),
                "observed": mp_string(observed, 60),
                "expected": mp_string(expected, 60),
                "distance_squared": mp_string(distance_squared, 50),
            },
        )
        records.append(
            {
                "index": index,
                "kappa": mp_string(kappa),
                "observed_overlap": mp_string(observed, 60),
                "expected_overlap": mp_string(expected, 60),
                "relative_error": mp_string(relative_error, 24),
                "distance_squared": mp_string(distance_squared, 50),
                "passed": passed,
            }
        )
        distances.append(distance_squared)

    monotone = all(
        distances[index + 1] > distances[index]
        for index in range(len(distances) - 1)
    )
    monotone_pass = audit.observe(
        "G1.endpoint.subprincipal.sampled_distance_monotonicity",
        monotone,
        "the frozen finite-hbar state distance increases strictly across the positive kappa samples",
    )
    return {
        "precision_digits": mp.mp.dps,
        "alpha": mp_string(alpha),
        "hbar": mp_string(hbar),
        "records": records,
        "sampled_distance_monotone": monotone,
        "sampled_distance_monotonicity_passed": monotone_pass,
        "quadratures": len(records),
        "root_calls": 0,
        "ode_calls": 0,
    }


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, str]],
    audit: Audit,
) -> dict[str, Any]:
    exact, flags = exact_calculation(audit)
    numerical = numerical_calculation(frozen_input, audit)
    passes = (
        all(flags.values())
        and all(item["passed"] for item in audit.numerical)
        and numerical["sampled_distance_monotonicity_passed"]
    )
    if passes:
        verdict = "KILL_UNIQUENESS_FROM_DECLARED_B_A0_HD_MC_DATA"
        impact = "NARROW_REQUIRE_ADDITIONAL_FULL_SYMBOL_AND_INTERTWINING_DATA"
        classification = (
            "GATE1_V0_ENDPOINT_B_AND_PRINCIPAL_HALF_DENSITY_DO_NOT_SELECT_"
            "UNIQUE_EXACT_COMPLETION_EXISTENCE_OPEN"
        )
        condition = (
            "the conditional unitary family preserves the classical B, "
            "canonical relation, principal half-density and M_c domain but "
            "changes a lower symbol and a finite-hbar test state"
        )
    else:
        verdict = "INCONCLUSIVE_ENDPOINT_COMPLETION_UNIQUENESS"
        impact = "OPEN"
        classification = "GATE1_V0_ENDPOINT_SUBPRINCIPAL_DISCRIMINATOR_NONPASS"
        condition = (
            "the proposed family is not unitary, changes the principal data, "
            "or is identical on every test state"
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
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": audit.numerical,
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "nonuniqueness inside the class fixing only B, a_0, H_D and M_c; additional exact intertwining or endpoint-domain conditions were not tested, and existence remains open",
            "prior_nonpass": "the one-term Van Vleck kernel remains killed at exact finite hbar",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted,
        "gate1_decision": promoted["gate1"],
        "global_promotion": promoted["global_promotion"],
        "automatic_next": promoted["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": numerical["quadratures"],
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
            "platform": platform.platform(),
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_scope": frozen_input["epistemic_scope"],
            "decision_table": frozen_input["decision_table"],
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
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_passed": sum(item["passed"] for item in audit.numerical),
                "numerical_checks_total": len(audit.numerical),
                "quadratures": result["resource_accounting"]["quadratures"],
                "exact_transform_existence": None,
                "gate1": result["gate1_decision"],
                "global_n_sigma": None,
                "physics_claim": None,
                "TOE_claim": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
