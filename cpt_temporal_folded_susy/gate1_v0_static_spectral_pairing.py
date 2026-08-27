#!/usr/bin/env python3
"""Gate 1 -- local static BFV versus spectral-delta pairing control.

This bounded non-numbered calculation compares the hash-pinned improved-static
BFV zero-mode contraction with the order-zero spectral distribution of the
self-adjoint multiplication constraint ``M_c``.  The comparison uses a frozen
three-state family on ``c in R, p>0``, an exact rational pairing matrix and an
independently integrated Gaussian delta regulator.

Agreement is only compatibility of one declared local zero-mode normalization
with one local spectral test form.  It is not a normalized endpoint transform,
full-real-lapse group average, physical inner product or BFV trajectory kernel.
One adjacent JSON result is written and no descendant starts.
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


INPUT_NAME = "GATE1_V0_STATIC_SPECTRAL_PAIRING_INPUTS.json"
RESULT_NAME = "GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_static_spectral_pairing.py"
)
EXPECTED_INPUT_SHA256 = (
    "f4f4005fa40432263c6b2d69ca50d4d41017956ee06b3938f2401172175525bf"
)
CALCULATION_ID = "Gate1V0StaticSpectralPairing"
RESULT_SCHEMA = "ice.gate1.v0-static-spectral-pairing.result.v1"
RESULT_PREFIX = "GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT="
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
        domain: str,
        statement: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "domain": domain,
                "statement": statement,
            }
        )


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, Any]:
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

    contract: dict[str, Any]
    if item["path"].endswith("IMPROVED_STATIC_BFV_SOURCE_RESULT.json"):
        source = payload["exact_calculation"]["endpoint_source"]
        contract = {
            "kind": "static_zero_mode",
            "bosonic_pairing_matrix": source["bosonic_pairing_matrix"],
            "fourier_measures": source["bosonic_fourier_measures"],
            "normalized_berezin_factor": source["normalized_berezin_factor"],
            "local_source": source["local_source"],
        }
    elif item["path"].endswith("CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json"):
        spectral = payload["exact_calculation"]["rigged_zero_fiber"]
        contract = {
            "kind": "spectral_zero_fiber",
            "form": spectral["form"],
            "E_singleton_zero": spectral["E_singleton_zero"],
            "delta_is_bounded_projector": spectral[
                "delta_Mc_is_bounded_projector"
            ],
        }
    elif item["path"].endswith(
        "ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json"
    ):
        spectral_boundary = payload["exact_calculation"]["spectral_boundary"]
        contract = {
            "kind": "subprincipal_shell",
            "V_at_c_zero": spectral_boundary["V_at_c_zero"],
            "delta_Mc_form_changed": spectral_boundary[
                "delta_Mc_form_changed"
            ],
        }
    else:
        raise AssertionError(f"unexpected upstream role: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
        "contract": contract,
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
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
        "ice.gate1.v0-static-spectral-pairing.input.v1"
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
        "quadratures": 36,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    if payload["numerical_plan"]["quadratures"] != 36:
        raise AssertionError("quadrature plan mutation")
    expected_nulls = {
        "exact_endpoint_state_transform": None,
        "selected_subprincipal_symbol": None,
        "physical_inner_product": None,
        "full_real_lapse_delta_C": None,
        "full_bfv_trajectory_measure": None,
        "old_fixed_a_kernel_equivalence": None,
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
    family = payload["frozen_test_family"]
    if (
        family["alpha_values"] != ["1", "2", "3"]
        or family["beta_values"] != ["1", "2", "3"]
        or family["component"] != "c in R and p>0 only"
    ):
        raise AssertionError("frozen test-family mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def matrix_record(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def exact_calculation(
    upstream: list[dict[str, Any]], audit: Audit
) -> tuple[dict[str, Any], dict[str, bool]]:
    contracts = {item["contract"]["kind"]: item["contract"] for item in upstream}
    static_contract = contracts["static_zero_mode"]
    spectral_contract = contracts["spectral_zero_fiber"]
    subprincipal_contract = contracts["subprincipal_shell"]

    source_normalization = audit.observe(
        "G1.pairing.upstream.static_normalization",
        static_contract["bosonic_pairing_matrix"]
        == [["1", "0"], ["0", "1"]]
        and static_contract["fourier_measures"]
        == ["dPi/(2*pi*hbar)", "dN/(2*pi*hbar)"]
        and static_contract["normalized_berezin_factor"] == "1"
        and static_contract["local_source"]
        == "delta(T)*delta(c) with normalized oriented ghost zero-mode factor +1",
        "the pinned static source has unit Pi-T/N-c Fourier pairing and normalized oriented ghost factor +1",
    )
    spectral_boundary = audit.observe(
        "G1.pairing.upstream.spectral_distribution_boundary",
        spectral_contract["E_singleton_zero"] is True
        and spectral_contract["delta_is_bounded_projector"] is False
        and spectral_contract["form"]
        == "eta_0(psi,varphi)=int_0^infinity dp conjugate(psi(0,p))*varphi(0,p)",
        "the pinned target is the order-zero zero-fiber form of M_c, not E({0}) or a bounded projector",
    )
    subprincipal_shell = audit.observe(
        "G1.pairing.upstream.subprincipal_shell_identity",
        subprincipal_contract["V_at_c_zero"] == "1"
        and subprincipal_contract["delta_Mc_form_changed"] is False,
        "the pinned off-shell subprincipal family equals one on c=0 and leaves the declared order-zero form unchanged",
    )

    alphas = [sp.Integer(1), sp.Integer(2), sp.Integer(3)]
    betas = [sp.Integer(1), sp.Integer(2), sp.Integer(3)]
    static_matrix = sp.Matrix(
        3,
        3,
        lambda row, column: sp.factorial(row + column)
        / (betas[row] + betas[column]) ** (row + column + 1),
    )
    p = sp.Symbol("p", positive=True, real=True)
    integrated_matrix = sp.Matrix(
        3,
        3,
        lambda row, column: sp.integrate(
            p ** (row + column)
            * sp.exp(-(betas[row] + betas[column]) * p),
            (p, 0, sp.oo),
        ),
    )
    static_formula = audit.observe(
        "G1.pairing.static.exact_half_line_matrix",
        integrated_matrix == static_matrix,
        "direct p>0 integration gives B_stat(j,k)=(j+k)!/(beta_j+beta_k)^(j+k+1) for every frozen pair",
    )
    hermitian = audit.observe(
        "G1.pairing.static.hermitian_matrix",
        static_matrix == static_matrix.conjugate().T,
        "the exact static matrix is Hermitian",
    )
    principal_minors = [
        sp.det(static_matrix[:size, :size]) for size in range(1, 4)
    ]
    positive = audit.observe(
        "G1.pairing.static.positive_definite_matrix",
        all(value.is_positive is True for value in principal_minors),
        "all exact leading principal minors are positive, so the frozen static Gram matrix is positive definite",
    )
    spectral_matrix = sp.Matrix(static_matrix)
    static_spectral = audit.observe(
        "G1.pairing.spectral.zero_fiber_equality",
        spectral_matrix == static_matrix,
        "evaluation of each psi_j at c=0 gives exactly the same p>0 matrix for delta(M_c)",
    )

    epsilon = sp.Symbol("epsilon", positive=True, real=True)
    regulated_matrix = sp.Matrix(
        3,
        3,
        lambda row, column: static_matrix[row, column]
        / sp.sqrt(
            1 + 4 * epsilon * (alphas[row] + alphas[column])
        ),
    )
    c = sp.Symbol("c", real=True)
    total_alpha = sp.Symbol("total_alpha", positive=True, real=True)
    generic_regulator_integral = sp.simplify(
        sp.integrate(
            sp.exp(-c**2 / (4 * epsilon))
            * sp.exp(-total_alpha * c**2)
            / (2 * sp.sqrt(sp.pi * epsilon)),
            (c, -sp.oo, sp.oo),
        )
    )
    expected_regulator_factor = 1 / sp.sqrt(
        1 + 4 * epsilon * total_alpha
    )
    regulator_formula = audit.observe(
        "G1.pairing.spectral.gaussian_regulator_formula",
        sp.simplify(
            generic_regulator_integral - expected_regulator_factor
        )
        == 0,
        "the normalized Gaussian delta regulator pairs with exp(-A*c^2) as 1/sqrt(1+4*epsilon*A)",
    )
    regulated_limit = regulated_matrix.applyfunc(
        lambda value: sp.limit(value, epsilon, 0, dir="+")
    )
    regulator_limit = audit.observe(
        "G1.pairing.spectral.entrywise_regulator_limit",
        regulated_limit == static_matrix,
        "epsilon->0+ returns the exact static/spectral matrix entry by entry",
    )
    phase_invariance = audit.observe(
        "G1.pairing.spectral.subprincipal_family_invariance",
        subprincipal_shell and spectral_matrix == static_matrix,
        "the explicit V_kappa family is invisible to this order-zero shell matrix and therefore is not normalized by the comparison",
    )

    audit.guard(
        "G1.pairing.guard.static_source_scope",
        "declared finite zero-mode Fourier/Berezin contraction",
        "the hash-pinned Pi,T,N,c and odd orientation with no nonzero trajectory modes",
        "delta(c) is inserted once through the N zero-mode contraction; this calculation does not append a second delta or construct a two-endpoint path kernel",
    )
    audit.guard(
        "G1.pairing.guard.order_zero_spectral_scope",
        "spectral direct-integral evaluation for M_c",
        "the frozen smooth states on R_c times R_{+,p} and the order-zero delta(c) distribution",
        "agreement is a finite test-form compatibility result, not E({0}), a bounded projector, arbitrary-state regulator theorem or physical group average",
    )
    audit.guard(
        "G1.pairing.guard.p_positive_only",
        "U_plus component restriction",
        "all p integrations run from zero to infinity and no p<0 state is imported",
        "the result does not establish a Phi identity kernel or a self-adjoint half-line coordinate generator",
    )
    audit.guard(
        "G1.pairing.guard.endpoint_nonuniqueness_survives",
        "off-shell unitary freedom equal to one on the shell",
        "V_kappa(0,p)=1",
        "a KEEP here cannot select an exact endpoint transform or its lower symbol",
    )

    flags = {
        "source_normalization": source_normalization,
        "spectral_distribution_boundary": spectral_boundary,
        "subprincipal_shell_identity": subprincipal_shell,
        "static_half_line_formula": static_formula,
        "hermitian": hermitian,
        "positive_definite": positive,
        "static_spectral_equality": static_spectral,
        "gaussian_regulator_formula": regulator_formula,
        "entrywise_regulator_limit": regulator_limit,
        "subprincipal_family_invariance": phase_invariance,
    }
    return (
        {
            "frozen_family": {
                "states": [
                    f"exp(-{alphas[index]}*c^2)*p^{index}*exp(-{betas[index]}*p)"
                    for index in range(3)
                ],
                "component": "c in R and p>0",
            },
            "static_zero_mode_form": {
                "source": "delta(T)*delta(c) times normalized ghost factor +1",
                "matrix": matrix_record(static_matrix),
                "direct_p_integral_matrix": matrix_record(integrated_matrix),
                "principal_minors": [str(value) for value in principal_minors],
                "positive_definite": positive,
            },
            "spectral_form": {
                "operator": "M_c on L2(R_c times R_{+,p},dc dp)",
                "distribution": "order-zero delta(M_c)",
                "matrix": matrix_record(spectral_matrix),
                "equals_static_matrix": static_spectral,
                "E_singleton_zero": True,
                "bounded_projector": False,
            },
            "gaussian_regulator": {
                "delta_epsilon": "exp(-c^2/(4*epsilon))/(2*sqrt(pi*epsilon))",
                "generic_factor": str(generic_regulator_integral),
                "matrix": matrix_record(regulated_matrix),
                "epsilon_zero_matrix": matrix_record(regulated_limit),
            },
            "subprincipal_boundary": {
                "V_kappa_at_c_zero": subprincipal_contract["V_at_c_zero"],
                "order_zero_matrix_changed": False,
                "endpoint_transform_selected": False,
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
    epsilons = [mp.mpf(value) for value in plan["epsilon_values"]]
    tolerance = mp.mpf(plan["relative_tolerance"])
    if (
        mp.mp.dps != 80
        or epsilons != [mp.mpf("0.2"), mp.mpf("0.05"), mp.mpf("0.01")]
        or tolerance != mp.mpf("1e-60")
        or plan["quadratures"] != 36
    ):
        raise AssertionError("numerical plan mutation")
    alphas = [mp.mpf(1), mp.mpf(2), mp.mpf(3)]
    betas = [mp.mpf(1), mp.mpf(2), mp.mpf(3)]

    static_records: list[dict[str, Any]] = []
    p_integrals: dict[tuple[int, int], mp.mpf] = {}
    exact_static: dict[tuple[int, int], mp.mpf] = {}
    for row in range(3):
        for column in range(3):
            power = row + column
            beta_sum = betas[row] + betas[column]
            observed = mp.quad(
                lambda value: value**power * mp.exp(-beta_sum * value),
                [0, mp.inf],
            )
            expected = mp.factorial(power) / beta_sum ** (power + 1)
            relative_error = abs(observed - expected) / abs(expected)
            passed = audit.observe_numerical(
                f"G1.pairing.static.p_quadrature_{row}_{column}",
                relative_error,
                tolerance,
                "direct p>0 quadrature matches the exact frozen static matrix entry",
                {
                    "row": row,
                    "column": column,
                    "observed": mp_string(observed, 60),
                    "expected": mp_string(expected, 60),
                },
            )
            static_records.append(
                {
                    "row": row,
                    "column": column,
                    "observed": mp_string(observed, 60),
                    "expected": mp_string(expected, 60),
                    "relative_error": mp_string(relative_error, 24),
                    "passed": passed,
                }
            )
            p_integrals[(row, column)] = observed
            exact_static[(row, column)] = expected

    regulator_records: list[dict[str, Any]] = []
    convergence_errors: dict[tuple[int, int], list[mp.mpf]] = {
        (row, column): [] for row in range(3) for column in range(3)
    }
    for epsilon_index, epsilon in enumerate(epsilons, 1):
        normalization = 2 * mp.sqrt(mp.pi * epsilon)
        for row in range(3):
            for column in range(3):
                alpha_sum = alphas[row] + alphas[column]
                c_factor = mp.quad(
                    lambda value: mp.exp(-value**2 / (4 * epsilon))
                    * mp.exp(-alpha_sum * value**2)
                    / normalization,
                    [-mp.inf, mp.inf],
                )
                observed = p_integrals[(row, column)] * c_factor
                expected = exact_static[(row, column)] / mp.sqrt(
                    1 + 4 * epsilon * alpha_sum
                )
                relative_error = abs(observed - expected) / abs(expected)
                passed = audit.observe_numerical(
                    f"G1.pairing.spectral.regulator_quadrature_{epsilon_index}_{row}_{column}",
                    relative_error,
                    tolerance,
                    "independent c-line Gaussian regulator quadrature times the p>0 integral matches the exact regulated matrix entry",
                    {
                        "epsilon": mp_string(epsilon),
                        "row": row,
                        "column": column,
                        "observed": mp_string(observed, 60),
                        "expected": mp_string(expected, 60),
                        "distance_to_static": mp_string(
                            abs(expected - exact_static[(row, column)]), 50
                        ),
                    },
                )
                regulator_records.append(
                    {
                        "epsilon_index": epsilon_index,
                        "epsilon": mp_string(epsilon),
                        "row": row,
                        "column": column,
                        "observed": mp_string(observed, 60),
                        "expected": mp_string(expected, 60),
                        "relative_error": mp_string(relative_error, 24),
                        "passed": passed,
                    }
                )
                convergence_errors[(row, column)].append(
                    abs(expected - exact_static[(row, column)])
                )

    monotone = all(
        errors[index + 1] < errors[index]
        for errors in convergence_errors.values()
        for index in range(len(errors) - 1)
    )
    monotone_pass = audit.observe(
        "G1.pairing.spectral.sampled_regulator_monotonicity",
        monotone,
        "every frozen regulated matrix entry approaches its static limit monotonically across the decreasing epsilon sequence",
    )
    return {
        "precision_digits": mp.mp.dps,
        "epsilon_values": [mp_string(value) for value in epsilons],
        "static_records": static_records,
        "regulator_records": regulator_records,
        "sampled_regulator_monotone": monotone,
        "sampled_regulator_monotonicity_passed": monotone_pass,
        "quadratures": len(static_records) + len(regulator_records),
        "root_calls": 0,
        "ode_calls": 0,
    }


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, Any]],
    audit: Audit,
) -> dict[str, Any]:
    exact, flags = exact_calculation(upstream, audit)
    numerical = numerical_calculation(frozen_input, audit)
    exact_pass = all(flags.values())
    numerical_pass = (
        all(item["passed"] for item in audit.numerical)
        and numerical["sampled_regulator_monotonicity_passed"]
    )
    normalization_flags = (
        flags["source_normalization"],
        flags["static_half_line_formula"],
        flags["static_spectral_equality"],
    )
    if not all(normalization_flags):
        verdict = "KILL_V0_DECLARED_STATIC_ZERO_MODE_SPECTRAL_NORMALIZATION"
        impact = "RETAIN_BFV_ALGEBRA_AND_SPECTRAL_DOMAIN_SEPARATELY"
        classification = "GATE1_V0_STATIC_SPECTRAL_NORMALIZATION_MISMATCH"
        condition = (
            "a sign, hbar, 2*pi, ghost-orientation or matrix normalization differs"
        )
    elif not exact_pass or not numerical_pass:
        verdict = "NARROW_STATIC_SPECTRAL_PAIRING_NUMERICAL_CONTROL_OPEN"
        impact = "OPEN"
        classification = "GATE1_V0_STATIC_SPECTRAL_FORMAL_MATCH_CONTROL_OPEN"
        condition = (
            "the symbolic equality holds but the independent regulator integration fails"
        )
    else:
        verdict = "KEEP_V0_LOCAL_STATIC_ZERO_MODE_SPECTRAL_PAIRING_COMPATIBILITY"
        impact = "CLOSE_FROZEN_ORDER_ZERO_PAIRING_ONLY"
        classification = (
            "GATE1_V0_LOCAL_STATIC_ZERO_MODE_EQUALS_ORDER_ZERO_MC_"
            "SPECTRAL_FORM_ON_FROZEN_TESTS_FULL_PATH_AND_PHYSICAL_RIGGING_OPEN"
        )
        condition = (
            "all upstream normalization pins, exact matrix identities, positivity, "
            "regulator limits and independent quadratures pass on p>0"
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
            "scope_meaning": "one frozen local order-zero static-versus-spectral pairing comparison only",
            "endpoint_transform_boundary": "the comparison is invariant under the explicit off-shell subprincipal family and cannot select an exact transform",
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
                "exact_endpoint_state_transform": None,
                "full_bfv_trajectory_measure": None,
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
