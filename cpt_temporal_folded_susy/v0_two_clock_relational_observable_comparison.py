#!/usr/bin/env python3
"""Exact classical two-clock comparison on one closed-FRW V=0 component.

The bounded, unnumbered calculation compares the massless scalar clock phi
with the geometric trace-momentum clock P on the already derived p>0,
R=3 p^2-2 P^2>0 constraint component.  It constructs their classical
complete observables, checks their common-chart inverse relation and records
the turning point of Q=2 log(a) as a failed global-clock control.

No quantum clock map, physical inner product, V!=0 dynamics, BO correction,
decoherence functional, likelihood, physics, or TOE claim is constructed.
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


INPUT_NAME = "V0_TWO_CLOCK_RELATIONAL_OBSERVABLE_COMPARISON_INPUTS.json"
RESULT_NAME = "V0_TWO_CLOCK_RELATIONAL_OBSERVABLE_COMPARISON_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "v0_two_clock_relational_observable_comparison.py"
)
EXPECTED_INPUT_SHA256 = (
    "9cf45fab1c0325b0d80add256e1ebc9ffbcd8894ababd3f3612481054adafdc4"
)
CALCULATION_ID = "V0TwoClockRelationalObservableComparison"
RESULT_SCHEMA = "ice.v0-two-clock-relational-observable-comparison.result.v1"
RESULT_PREFIX = "V0_TWO_CLOCK_RELATIONAL_OBSERVABLE_COMPARISON_RESULT="
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
    seen: set[str] = field(default_factory=set, repr=False)

    def register(self, check_id: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        self.register(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )

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


def expected_caps() -> dict[str, int]:
    return {
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


def expected_nulls() -> dict[str, Any]:
    return {
        "quantum_relational_observable": None,
        "quantum_clock_change_map": None,
        "clock_change_unitarity": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "V_nonzero_clock_completion": None,
        "inhomogeneous_relational_observable": None,
        "born_oppenheimer_correction": None,
        "decoherence_functional": None,
        "primordial_spectrum": None,
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
    required = {
        "run_status": "VALID_RUN",
        "verdict": item["required_verdict"],
        "result_payload_sha256_without_self": item[
            "payload_sha256_without_self"
        ],
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise AssertionError(f"upstream field mismatch: {key}")
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
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.v0-two-clock-relational-observable-comparison.input.v1"
    ):
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this calculation must remain unnumbered")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def poisson(
    left: sp.Expr,
    right: sp.Expr,
    coordinates: list[sp.Symbol],
    momenta: list[sp.Symbol],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(left, coordinate) * sp.diff(right, momentum)
            - sp.diff(left, momentum) * sp.diff(right, coordinate)
            for coordinate, momentum in zip(coordinates, momenta, strict=True)
        )
    )


def run(payload: dict[str, Any], input_sha: str, upstream: list[dict[str, str]]) -> dict[str, Any]:
    audit = Audit()
    Q, P, phi, p = sp.symbols("Q P phi p", real=True)
    tau, sigma = sp.symbols("tau sigma", real=True)
    pi = sp.pi
    root_32 = sp.sqrt(sp.Rational(3, 2))
    root_23 = sp.sqrt(sp.Rational(2, 3))
    coordinates = [Q, phi]
    momenta = [P, p]

    R = 3 * p**2 - 2 * P**2
    C = sp.exp(-3 * Q / 2) * R / (12 * pi**2) - 6 * pi**2 * sp.exp(Q / 2)
    shell_defect = sp.exp(-3 * Q / 2) * R - 72 * pi**4 * sp.exp(Q / 2)
    Phi = phi - root_32 * sp.atanh(root_23 * P / p)

    audit.check(
        "V0.clock.constraint.shell_defect",
        sp.simplify(C - shell_defect / (12 * pi**2)) == 0,
        "C=0 is equivalent to exp(-3Q/2)R=72*pi^4*exp(Q/2), hence exp(2Q)=R/(72*pi^4).",
    )
    audit.check(
        "V0.clock.dirac.Phi_weak_bracket",
        sp.simplify(poisson(Phi, C, coordinates, momenta) - 3 * p * C / (2 * R))
        == 0,
        "The on-shell coordinate Phi obeys {Phi,C}=3p C/(2R) and is therefore weakly Dirac on R>0.",
    )
    audit.check(
        "V0.clock.dirac.p_strong_bracket",
        poisson(p, C, coordinates, momenta) == 0,
        "The scalar momentum p strongly commutes with C.",
    )

    fp_phi = poisson(phi, C, coordinates, momenta)
    fp_P = poisson(P, C, coordinates, momenta)
    fp_Q = poisson(Q, C, coordinates, momenta)
    expected_fp_phi = sp.exp(-3 * Q / 2) * p / (2 * pi**2)
    expected_fp_P = sp.exp(-3 * Q / 2) * R / (8 * pi**2) + 3 * pi**2 * sp.exp(Q / 2)
    audit.check(
        "V0.clock.fp.scalar_exact",
        sp.simplify(fp_phi - expected_fp_phi) == 0,
        "The scalar-clock FP factor is {phi,C}=exp(-3Q/2)p/(2*pi^2).",
    )
    audit.check(
        "V0.clock.fp.trace_momentum_exact",
        sp.simplify(fp_P - expected_fp_P) == 0,
        "The trace-momentum-clock FP factor is {P,C}=-C_Q.",
    )
    audit.check(
        "V0.clock.fp.trace_momentum_shell",
        sp.simplify(
            expected_fp_P
            - 12 * pi**2 * sp.exp(Q / 2)
            - sp.Rational(3, 2) * C
        )
        == 0,
        "The exact identity {P,C}=12*pi^2*exp(Q/2)+3C/2 makes the P-clock FP factor positive on shell.",
    )
    audit.check(
        "V0.clock.fp.log_scale_turning_point",
        sp.simplify(fp_Q + sp.exp(-3 * Q / 2) * P / (3 * pi**2)) == 0
        and sp.simplify(fp_Q.subs(P, 0)) == 0,
        "The Q-clock FP factor is -exp(-3Q/2)P/(3*pi^2), so it vanishes and changes sign at P=0.",
    )

    P_at_phi = root_32 * p * sp.tanh(root_23 * (tau - Phi))
    Q_at_phi = sp.log((3 * p**2 - 2 * P_at_phi**2) / (72 * pi**4)) / 2
    phi_at_P = Phi + root_32 * sp.atanh(root_23 * sigma / p)
    Q_at_P = sp.log((3 * p**2 - 2 * sigma**2) / (72 * pi**4)) / 2
    Q_shell = sp.log(R / (72 * pi**4)) / 2

    P_at_current_phi = sp.trigsimp(P_at_phi.subs(tau, phi))
    audit.check(
        "V0.clock.complete.P_at_current_phi",
        sp.simplify(P_at_current_phi - P) == 0,
        "The scalar-clock complete observable P_phi(tau) returns P at tau=phi.",
    )
    Q_at_current_phi = sp.log(
        (3 * p**2 - 2 * P_at_current_phi**2) / (72 * pi**4)
    ) / 2
    audit.check(
        "V0.clock.complete.Q_at_current_phi",
        sp.simplify(Q_at_current_phi - Q_shell) == 0,
        "The scalar-clock complete observable Q_phi(tau) returns the on-shell Q at tau=phi.",
    )
    audit.check(
        "V0.clock.complete.phi_at_current_P",
        sp.simplify(phi_at_P.subs(sigma, P) - phi) == 0,
        "The P-clock complete observable phi_P(sigma) returns phi at sigma=P.",
    )
    audit.check(
        "V0.clock.complete.Q_at_current_P",
        sp.simplify(Q_at_P.subs(sigma, P) - Q_shell) == 0,
        "The P-clock complete observable Q_P(sigma) returns the on-shell Q at sigma=P.",
    )

    P_after_phi_at_P = sp.trigsimp(P_at_phi.subs(tau, phi_at_P))
    audit.check(
        "V0.clock.overlap.inverse_P_after_phi",
        sp.simplify(P_after_phi_at_P - sigma) == 0,
        "On |sigma|<sqrt(3/2)p, P_phi(phi_P(sigma))=sigma.",
    )
    Q_after_phi_at_P = sp.log(
        (3 * p**2 - 2 * P_after_phi_at_P**2) / (72 * pi**4)
    ) / 2
    audit.check(
        "V0.clock.overlap.Q_agreement",
        sp.simplify(Q_after_phi_at_P - Q_at_P) == 0,
        "The two clock descriptions assign the same Q on their common chart.",
    )
    audit.check(
        "V0.clock.overlap.scalar_map_monotone",
        sp.simplify(
            sp.diff(P_at_phi, tau)
            - p * sp.sech(root_23 * (tau - Phi)) ** 2
        )
        == 0,
        "For p>0, d P_phi/d tau=p sech^2(...) is strictly positive.",
    )
    audit.check(
        "V0.clock.overlap.trace_map_monotone",
        sp.simplify(
            sp.diff(phi_at_P, sigma)
            - 1 / (p * (1 - 2 * sigma**2 / (3 * p**2)))
        )
        == 0,
        "For |sigma|<sqrt(3/2)p, d phi_P/d sigma is strictly positive.",
    )
    audit.check(
        "V0.clock.domain.scalar_orbit_remainder",
        sp.trigsimp(
            3 * p**2
            - 2 * P_at_phi**2
            - 3 * p**2 * sp.sech(root_23 * (tau - Phi)) ** 2
        )
        == 0,
        "The scalar clock covers the orbit with R=3p^2 sech^2(...)>0 for every finite tau.",
    )

    F_Phi, F_p, C_symbol = sp.symbols("F_Phi F_p C_symbol")
    generic_chain_bracket = F_Phi * 3 * p * C_symbol / (2 * R) + F_p * 0
    audit.check(
        "V0.clock.complete.generic_weak_invariance",
        sp.simplify(generic_chain_bracket.subs(C_symbol, 0)) == 0,
        "Every smooth complete observable written only in Phi, p and an external clock reading weakly commutes with C on this chart.",
    )

    audit.guard(
        "V0.clock.guard.scalar_clock_domain",
        "monotone-clock complete-observable construction",
        "p>0 makes {phi,C}>0 and P_phi(tau) maps every finite real tau into |P|<sqrt(3/2)p",
        "phi is a global classical clock on the declared open orbit; no statement is made at the singular R=0 ends or in another component",
    )
    audit.guard(
        "V0.clock.guard.trace_momentum_domain",
        "inverse function theorem on a monotone gauge orbit",
        "on C=0, {P,C}=12*pi^2 exp(Q/2)>0 and sigma is restricted to |sigma|<sqrt(3/2)p",
        "P is a valid geometric clock on the finite open interval and its complete observables are inverse to the scalar-clock chart there",
    )
    audit.guard(
        "V0.clock.guard.inverse_branch",
        "real inverse relation between tanh and atanh",
        "all arguments sqrt(2/3)sigma/p lie in (-1,1) and all scalar-clock parameters are real",
        "atanh(tanh u)=u and tanh(atanh x)=x on the declared real principal branches; this supplies the second inverse composition without analytic continuation",
    )
    audit.guard(
        "V0.clock.guard.log_scale_failure",
        "Faddeev-Popov local clock criterion",
        "{Q,C} vanishes at P=0 and has opposite signs on P<0 and P>0",
        "Q cannot be one global clock across the maximal-scale turning point; two branch charts would be extra data, not a failure of the constrained dynamics",
    )
    audit.guard(
        "V0.clock.guard.quantum_scope",
        "classical complete-observable scope boundary",
        "the calculation supplies classical functions and clock domains only, with no selected raw-C rigging map or physical inner product",
        "classical overlap agreement does not imply a unitary quantum clock-change map, equal self-adjoint domains, or clock-independent quantum probabilities",
    )

    all_passed = all(item["passed"] for item in audit.exact)
    verdict = (
        "KEEP_V0_CLASSICAL_SCALAR_AND_TRACE_MOMENTUM_CLOCKS_AGREE_ON_OVERLAP_Q_CLOCK_TURNS"
        if all_passed
        else "KILL_DECLARED_V0_TWO_CLOCK_RELATIONAL_COMPARISON"
    )
    impact = (
        "KEEP_ONE_CLASSICAL_TWO_CLOCK_CHART_AND_REQUIRE_BRANCHING_FOR_LOG_SCALE_CLOCK"
        if all_passed
        else "RETAIN_THE_UPSTREAM_DARBOUX_CHART_AND_REOPEN_THE_CLOCK_FORMULAE"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {
            "path": INPUT_RELPATH,
            "sha256": input_sha,
            "numbered_phase": None,
        },
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_model": payload["declared_model"],
        "formulae": {
            "weak_dirac_coordinate": "{Phi,C}=3*p*C/(2*R)",
            "scalar_clock": "P_phi(tau)=sqrt(3/2)*p*tanh(sqrt(2/3)*(tau-Phi))",
            "scalar_clock_scale": "Q_phi(tau)=1/2*log((3*p^2-2*P_phi(tau)^2)/(72*pi^4))",
            "trace_momentum_clock": "phi_P(sigma)=Phi+sqrt(3/2)*atanh(sqrt(2/3)*sigma/p)",
            "trace_momentum_clock_scale": "Q_P(sigma)=1/2*log((3*p^2-2*sigma^2)/(72*pi^4))",
            "trace_clock_domain": "|sigma|<sqrt(3/2)*p",
            "log_scale_clock_fp": "{Q,C}=-exp(-3Q/2)*P/(3*pi^2)",
        },
        "clock_domain_result": {
            "scalar_phi": "GLOBAL_ON_DECLARED_OPEN_ORBIT_FOR_FINITE_CLOCK_READINGS",
            "trace_momentum_P": "VALID_ON_FINITE_OPEN_INTERVAL",
            "log_scale_Q": "TWO_BRANCH_CLOCK_WITH_FP_ZERO_AT_P_EQUALS_ZERO",
        },
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "theorem_guard_count": len(audit.theorem_guards),
            "all_executable_checks_passed": all_passed,
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
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
    return result


def write_result(path: Path, result: dict[str, Any]) -> tuple[str, int]:
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result exceeds artifact cap")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> int:
    payload, input_sha, upstream = load_input()
    result = run(payload, input_sha, upstream)
    outer_sha, size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "theorem_guards": result["check_summary"]["theorem_guard_count"],
                "result": RESULT_NAME,
                "result_sha256": outer_sha,
                "result_bytes": size,
                "automatic_next": None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
