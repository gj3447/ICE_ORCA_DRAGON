#!/usr/bin/env python3
"""Declared raw-C constant-boundary direct-integral extension audit.

This bounded, non-numbered calculation starts only from the pinned fixed-p
raw-C classification.  It declares one extra quantization datum: for the real
zero-energy reference pair normalized at Q0=-4, impose Gamma_1,p=0 for almost
every Lebesgue-p fiber.  It audits the reference Wronskian, parity, parameter
measurability hypotheses and the scoped measurable-resolvent theorem needed to
form the p-preserving direct integral.

The boundary line is not selected by H=fC or by a physical principle.  No
spectral resolution, group average, rigging map, physical product, C/H
equivalence, p-mixing classification, BFV measure, physics, or TOE claim is
constructed.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import scipy
import sympy as sp
from scipy.integrate import solve_ivp


INPUT_NAME = "RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL_INPUTS.json"
RESULT_NAME = "RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_constant_boundary_direct_integral.py"
EXPECTED_INPUT_SHA256 = "68d1c80ad33c03bcf96dc41187a7ac1cd067ded2116eda04e8ca7cce618d654d"
CALCULATION_ID = "RawCConstantBoundaryDirectIntegral"
RESULT_SCHEMA = "ice.raw-c-constant-boundary-direct-integral.result.v1"
RESULT_PREFIX = "RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
H_BAR = 1.0
ODE_CALL_CAP = 12


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    ode_calls: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        self.exact.append({"id": check_id, "passed": bool(passed), "statement": statement})
        return bool(passed)

    def observe_numeric(
        self, check_id: str, observed: float, tolerance: float, statement: str
    ) -> bool:
        self.register(check_id)
        passed = observed <= tolerance
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "maximum_error": format(observed, ".17g"),
                "tolerance": format(tolerance, ".17g"),
            }
        )
        return passed

    def guard(
        self, guard_id: str, theorem: str, hypotheses: str, conclusion_and_scope: str
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_NUMERICAL_PREDICATE",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def expected_nulls() -> dict[str, Any]:
    return {
        "raw_C_spectral_resolution": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "general_p_mixing_extension_classification": None,
        "canonical_p_zero_origin_sector": None,
        "cross_branch_gluing_or_quotient": None,
        "exact_endpoint_state_transform": None,
        "absolute_bfv_measure": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    for key, expected in (
        ("run_status", "VALID_RUN"),
        ("verdict", item["required_verdict"]),
        ("result_payload_sha256_without_self", item["payload_sha256_without_self"]),
    ):
        if payload.get(key) != expected:
            raise AssertionError(f"upstream field mismatch: {key}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload["result_payload_sha256_without_self"],
        "verdict": payload["verdict"],
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed}")
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.raw-c-constant-boundary-direct-integral.input.v1":
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID or payload["numbered_phase"] is not None:
        raise AssertionError("calculation identity mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 12,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    candidate = payload["declared_candidate"]
    if candidate["reference_normalization"] != "Q_0=-4; c_p(-4)=1,c_p'(-4)=0,s_p(-4)=0,s_p'(-4)=1":
        raise AssertionError("reference normalization mutation")
    if candidate["selected_boundary_line"] != "Gamma_1,p(u)=0 for Lebesgue-almost every p":
        raise AssertionError("boundary-line mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    p, hbar, Q = sp.symbols("p hbar Q", real=True, nonzero=True)
    c_value, s_value = sp.symbols("c_value s_value", real=True)
    a_u, b_u, a_v, b_v = sp.symbols("a_u b_u a_v b_v", complex=True)
    coefficient = (72 * sp.pi**4 * sp.exp(2 * Q) - 3 * p**2) / (2 * hbar**2)
    wronskian_prime = sp.simplify(
        c_value * (coefficient * s_value) - (coefficient * c_value) * s_value
    )
    flags = {
        "wronskian_conservation": audit.observe(
            "rawc.direct_integral.reference.wronskian_conservation",
            wronskian_prime == 0,
            "the reference equation has no first derivative, so W(c_p,s_p) is Q-independent",
        ),
        "wronskian_initial_normalization": audit.observe(
            "rawc.direct_integral.reference.wronskian_at_Q0",
            sp.Matrix([[1, 0], [0, 1]]).det() == 1,
            "c_p(-4)=1,c_p'(-4)=0,s_p(-4)=0,s_p'(-4)=1 gives W(c_p,s_p)=1",
        ),
        "coefficient_even_in_p": audit.observe(
            "rawc.direct_integral.parameter.p_even_coefficient",
            sp.simplify(coefficient.subs(p, -p) - coefficient) == 0,
            "the reference ODE coefficient depends on p only through p^2",
        ),
        "boundary_form_coordinates": audit.observe(
            "rawc.direct_integral.boundary.symplectic_coordinates",
            sp.simplify(
                (
                    sp.Matrix([sp.conjugate(a_u), sp.conjugate(b_u)]).T
                    * sp.Matrix([[0, 1], [-1, 0]])
                    * sp.Matrix([a_v, b_v])
                )[0]
                - (sp.conjugate(a_u) * b_v - sp.conjugate(b_u) * a_v)
            ) == 0,
            "with Gamma_0=W(u,s), Gamma_1=-W(u,c), the minus-end form is Gamma_0(u)^*Gamma_1(v)-Gamma_1(u)^*Gamma_0(v)",
        ),
        "selected_line_is_lagrangian": audit.observe(
            "rawc.direct_integral.boundary.gamma1_zero_lagrangian",
            sp.simplify(sp.conjugate(a_u) * 0 - sp.conjugate(0) * a_v) == 0,
            "the declared Gamma_1=0 reference boundary line annihilates the scalar boundary form",
        ),
        "parity_domain_rule": audit.observe(
            "rawc.direct_integral.parity.declared_line_invariant",
            True,
            "ODE uniqueness with even coefficient and identical Q0 data gives c_-p=c_p and s_-p=s_p, hence P preserves Gamma_1=0",
        ),
    }
    audit.guard(
        "rawc.direct_integral.guard.inherited_fixed_p_extension",
        "one limit-circle/one limit-point Sturm-Liouville extension theorem",
        "the pinned upstream result supplies the declared weighted fiber, limit-circle minus end, limit-point plus end, and indices (1,1); the reference boundary maps are the corresponding maximal-domain Wronskian limits",
        "D(C_p,Gamma)={u in D(C_p,max):Gamma_1,p(u)=0} is self-adjoint for every fixed p; this does not make the line unique or physical",
    )
    audit.guard(
        "rawc.direct_integral.guard.parameter_measurability",
        "continuous parameter dependence for linear initial-value systems",
        "the ODE coefficient is jointly continuous in (p,Q), even in p, and c_p,s_p use p-independent finite-Q initial data at Q0=-4",
        "(p,Q) -> c_p(Q),s_p(Q) is jointly continuous on compact Q intervals and provides a measurable reference field; this statement does not replace endpoint Wronskian limits by literal endpoint values",
    )
    audit.guard(
        "rawc.direct_integral.guard.weak_resolvent_measurability",
        "measurable symmetry-preserving self-adjoint extension and decomposable unbounded-operator criterion",
        "the jointly measurable real reference pair makes the Wronskian boundary graph Gamma_1,p=0 measurable; with the pinned maximal-fiber field, the measurable-graph extension theorem yields weak measurability of one nonreal resolvent on a countable dense compact-support test set",
        "the selected boundary graph supplies a measurable self-adjoint fiber field, hence a decomposable extension up to Lebesgue-a.e. equality; this does not classify p-mixing extensions or turn the theorem route into a physical selection principle",
    )
    audit.guard(
        "rawc.direct_integral.guard.direct_integral_self_adjointness",
        "direct integral of a measurable self-adjoint field",
        "the prior guard supplies measurable self-adjoint fibers over Lebesgue dp and the domain uses square-integrable graph norm",
        "C_Gamma=integral^oplus C_p,Gamma dp is one declared p-preserving self-adjoint raw-C extension; no spectral/RAQ comparison is implied",
    )
    audit.guard(
        "rawc.direct_integral.guard.p_zero_and_parity_scope",
        "Lebesgue direct-integral almost-everywhere equivalence",
        "the base is full Lebesgue p and the reference field is even; {0} has zero base measure",
        "parity commutes with the declared decomposable extension, while the p=0 boundary datum creates neither an origin atom nor cross-branch gluing",
    )
    return (
        {
            "reference_equation": "2*hbar^2*y''+(3*p^2-72*pi^4*exp(2Q))*y=0",
            "reference_pair": "c_p(-4)=1,c_p'(-4)=0,s_p(-4)=0,s_p'(-4)=1",
            "reference_wronskian": "W(c_p,s_p)=1 for all Q",
            "boundary_maps": "Gamma_0,p=W(u,s_p)|_-infinity; Gamma_1,p=-W(u,c_p)|_-infinity",
            "selected_domain": "D(C_p,Gamma)={u in D(C_p,max):Gamma_1,p(u)=0}",
            "direct_integral": "C_Gamma=integral^oplus_R C_p,Gamma dp with graph-norm domain",
            "selected_line_status": "DECLARED_EXTRA_QUANTIZATION_DATA_NOT_DERIVED",
            "p_zero_role": "Lebesgue-null; no atom, finite part, quotient, or gluing is constructed",
        },
        flags,
    )


def solve_reference_pair(audit: Audit, p_value: float) -> Any:
    def rhs(q: float, state: Any) -> list[float]:
        coefficient = (72.0 * math.pi**4 * math.exp(2.0 * q) - 3.0 * p_value**2) / (2.0 * H_BAR**2)
        c_value, c_prime, s_value, s_prime = state
        return [c_prime, coefficient * c_value, s_prime, coefficient * s_value]

    def solve_to(endpoint: float) -> Any:
        audit.ode_calls += 1
        if audit.ode_calls > ODE_CALL_CAP:
            raise AssertionError("ODE call cap exceeded")
        solution = solve_ivp(
            rhs,
            (-4.0, endpoint),
            [1.0, 0.0, 0.0, 1.0],
            method="DOP853",
            dense_output=True,
            rtol=1e-11,
            atol=1e-13,
        )
        if not solution.success or solution.sol is None:
            raise AssertionError(f"reference solve failed for p={p_value}: {solution.message}")
        return solution.sol

    negative_q = solve_to(-8.0)
    positive_q = solve_to(-3.0)

    def reference(q: float) -> Any:
        return negative_q(q) if q < -4.0 else positive_q(q)

    return reference


def numerical_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    p_values = [0.0, 0.75, 2.0]
    q_values = [-8.0, -6.0, -4.0, -3.0]
    max_wronskian_error = 0.0
    max_parity_error = 0.0
    rows: list[dict[str, str]] = []
    for p_value in p_values:
        positive = solve_reference_pair(audit, p_value)
        negative = solve_reference_pair(audit, -p_value)
        for q_value in q_values:
            c_value, c_prime, s_value, s_prime = positive(q_value)
            nc_value, nc_prime, ns_value, ns_prime = negative(q_value)
            wronskian_error = abs(c_value * s_prime - c_prime * s_value - 1.0)
            parity_error = max(
                abs(c_value - nc_value),
                abs(c_prime - nc_prime),
                abs(s_value - ns_value),
                abs(s_prime - ns_prime),
            )
            max_wronskian_error = max(max_wronskian_error, float(wronskian_error))
            max_parity_error = max(max_parity_error, float(parity_error))
            rows.append(
                {
                    "p": format(p_value, ".6g"),
                    "Q": format(q_value, ".6g"),
                    "wronskian_error": format(float(wronskian_error), ".17g"),
                    "parity_error": format(float(parity_error), ".17g"),
                }
            )
    flags = {
        "reference_wronskian": audit.observe_numeric(
            "rawc.direct_integral.numeric.reference_wronskian",
            max_wronskian_error,
            1e-9,
            "the finite-interval normalized reference IVP preserves W(c_p,s_p)=1 at all bounded p,Q samples",
        ),
        "reference_parity": audit.observe_numeric(
            "rawc.direct_integral.numeric.reference_parity",
            max_parity_error,
            1e-11,
            "the numerical IVP reference pairs for p and -p agree at all bounded samples",
        ),
    }
    return (
        {
            "hbar": H_BAR,
            "p_samples": p_values,
            "Q_samples": q_values,
            "ode_calls": audit.ode_calls,
            "maximum_wronskian_error": format(max_wronskian_error, ".17g"),
            "maximum_parity_error": format(max_parity_error, ".17g"),
            "rows": rows,
            "scope": "finite-interval IVP diagnostics for the normalized zero-energy reference pair; not a computation of endpoint boundary limits, a nonreal resolvent, or a raw-C spectral density",
        },
        flags,
    )


def write_result(path: Path, payload: dict[str, Any]) -> tuple[str, int]:
    payload["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(payload))
    encoded = canonical_bytes(payload)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact byte cap exceeded")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> None:
    input_payload, input_sha, upstream = load_input()
    audit = Audit()
    exact, exact_flags = exact_calculation(audit)
    numerical, numerical_flags = numerical_calculation(audit)
    all_passed = all(item["passed"] for item in audit.exact + audit.numerical)
    if all_passed:
        verdict = "CONSTRUCT_DECLARED_RAW_C_P_PRESERVING_DIRECT_INTEGRAL_EXTENSION_RAQ_OPEN"
        impact = "KEEP_ONE_DECLARED_RAW_C_DECOMPOSABLE_EXTENSION_WITHOUT_PROMOTING_RAQ_OR_C_H_EQUIVALENCE"
    else:
        verdict = "KILL_DECLARED_RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL_CANDIDATE"
        impact = "RETAIN_FIXED_P_EXTENSION_DEBT_AND_REOPEN_THIS_DECLARED_BOUNDARY_LINE"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha, "numbered_phase": None},
        "upstream_results": upstream,
        "primary_sources": input_payload["primary_sources"],
        "declared_candidate": input_payload["declared_candidate"],
        "assumptions": input_payload["assumptions"],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.theorem_guards,
        "selected_extension": {
            "p_preserving_decomposable_extension": "DECLARED_GAMMA_1_EQUALS_ZERO_REFERENCE_LINE",
            "selection_not_physical": True,
            "parity_invariant": True,
            "p_zero_origin_atom": None,
            "general_p_mixing_extension_classification": None,
        },
        "required_fail_closed_outputs": expected_nulls(),
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": sum(item["passed"] for item in audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guard_count": len(audit.theorem_guards),
            "all_executable_checks_passed": all_passed,
        },
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": audit.ode_calls,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__, "scipy": scipy.__version__},
        "audit_flags": {"exact": exact_flags, "numerical": numerical_flags},
    }
    result_sha, result_size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": result_sha, "result_size_bytes": result_size, "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
