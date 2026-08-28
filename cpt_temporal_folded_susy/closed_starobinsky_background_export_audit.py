#!/usr/bin/env python3
"""Bounded leading-slow-roll Starobinsky background export.

The runner hash-pins historical Phase-19 evidence but never invokes its runner
or reconstructs its closed-bounce ODE calculation.  N_star is a new input to a
flat leading potential-slow-roll pivot equation, not Phase-19 N_acc.
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

import scipy.optimize
import sympy as sp


INPUT_NAME = "CLOSED_STAROBINSKY_BACKGROUND_EXPORT_AUDIT_INPUTS.json"
RESULT_NAME = "CLOSED_STAROBINSKY_BACKGROUND_EXPORT_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_starobinsky_background_export_audit.py"
EXPECTED_INPUT_SHA256 = "a40cfa5a8d1eafff152f80cd4ec2d19f1d94ca584db7f015ff2eb69e42691008"
CALCULATION_ID = "ClosedStarobinskyBackgroundExportAudit"
RESULT_SCHEMA = "ice.closed-starobinsky-background-export-audit.result.v1"
RESULT_PREFIX = "CLOSED_STAROBINSKY_BACKGROUND_EXPORT_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
ROOT_RESIDUAL_BOUND = 1.0e-11


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
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def _register(self, check_id: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        self._register(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )

    def numerical_check(
        self, check_id: str, passed: bool, statement: str, observed: float, bound: float
    ) -> None:
        self._register(check_id)
        self.numerical.append(
            {
                "id": check_id,
                "passed": bool(passed),
                "statement": statement,
                "observed": observed,
                "bound": bound,
            }
        )


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 3,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "phase19_bounce_replay_or_reproduction": None,
        "closed_background_evolution": None,
        "reheating_history": None,
        "closed_mode_evolution": None,
        "born_oppenheimer_or_decoherence": None,
        "relational_observables": None,
        "class_or_cobaya_input": None,
        "public_likelihood": None,
        "observational_fit_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, Any]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"historical evidence hash mismatch: {item['path']}")
    payload = json.loads(raw)
    for key, expected in (
        ("result_id", item["required_result_id"]),
        ("exit_code", item["required_exit_code"]),
        ("exact_checks", item["required_exact_checks"]),
        ("numerical_checks", item["required_numerical_checks"]),
    ):
        if payload.get(key) != expected:
            raise AssertionError(f"historical evidence field mismatch: {key}")
    return {
        "path": item["path"],
        "sha256": observed,
        "result_id": payload["result_id"],
        "exit_code": payload["exit_code"],
        "exact_checks": payload["exact_checks"],
        "numerical_checks": payload["numerical_checks"],
        "role": item["role"],
    }


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != "ice.closed-starobinsky-background-export-audit.input.v1":
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this must remain unnumbered")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    model = payload["declared_model_and_units"]
    if model["units"] != "reduced Planck units M_Pl=1":
        raise AssertionError("unit convention drift")
    if model["pivot_efolds"] != [50, 55, 60] or model["mass_scale_M"] != 1.3e-05:
        raise AssertionError("declared background export inputs drift")
    return payload, observed


def solve_pivot_t(n_star: float, t_end: float) -> tuple[float, float]:
    target = t_end - math.log(t_end) + 4.0 * n_star / 3.0

    def residual(t: float) -> float:
        return t - math.log(t) - target

    lower = t_end
    upper = max(4.0 * n_star, 2.0 * t_end)
    while residual(upper) <= 0.0:
        upper *= 2.0
        if upper > 1.0e8:
            raise AssertionError("failed to establish bounded monotone root bracket")
    root = scipy.optimize.brentq(residual, lower, upper, xtol=1.0e-13, rtol=1.0e-14)
    return root, residual(root)


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    phi, M, x, t = sp.symbols("phi M x t", positive=True, finite=True)
    alpha = sp.sqrt(sp.Rational(2, 3))
    potential_x = sp.Rational(3, 4) * M**2 * (1 - x) ** 2
    d_d_phi = lambda expression: sp.simplify(-alpha * x * sp.diff(expression, x))
    v_prime = d_d_phi(potential_x)
    ratio = sp.simplify(v_prime / potential_x)
    epsilon = sp.simplify(sp.Rational(1, 2) * ratio**2)
    eta = sp.simplify(d_d_phi(v_prime) / potential_x)
    expected_ratio = 2 * alpha * x / (1 - x)
    expected_epsilon = sp.Rational(4, 3) * x**2 / (1 - x) ** 2
    expected_eta = sp.Rational(4, 3) * x * (2 * x - 1) / (1 - x) ** 2
    ledger.check(
        "CSBE.exact.Vprime_over_V",
        sp.simplify(ratio - expected_ratio) == 0,
        "For x=exp(-sqrt(2/3)phi), V_prime/V=2 sqrt(2/3) x/(1-x).",
    )
    ledger.check(
        "CSBE.exact.epsilon_V",
        sp.simplify(epsilon - expected_epsilon) == 0,
        "epsilon_V=(4/3)x^2/(1-x)^2.",
    )
    ledger.check(
        "CSBE.exact.eta_V",
        sp.simplify(eta - expected_eta) == 0,
        "eta_V=(4/3)x(2x-1)/(1-x)^2.",
    )
    t_end_exact = 1 + 2 / sp.sqrt(3)
    endpoint_epsilon = sp.simplify(expected_epsilon.subs(x, 1 / t_end_exact))
    ledger.check(
        "CSBE.exact.epsilon_one_endpoint",
        endpoint_epsilon == 1,
        "epsilon_V=1 gives t_end=exp(alpha phi_end)=1+2/sqrt(3).",
    )
    primitive_t = sp.Rational(3, 4) * (t - sp.log(t))
    primitive_derivative = sp.simplify(alpha * t * sp.diff(primitive_t, t))
    ratio_t = sp.simplify((t - 1) / (2 * alpha))
    ledger.check(
        "CSBE.exact.N_primitive",
        sp.simplify(primitive_derivative - ratio_t) == 0,
        "The N primitive is (3/4)(t-log t), with t=exp(alpha phi).",
    )
    ledger.check(
        "CSBE.exact.unit_status",
        payload["declared_model_and_units"]["units"] == "reduced Planck units M_Pl=1",
        "All exported quantities use the declared reduced-Planck convention; no observational normalization is inferred.",
    )

    model = payload["declared_model_and_units"]
    mass_scale = float(model["mass_scale_M"])
    alpha_float = math.sqrt(2.0 / 3.0)
    t_end = 1.0 + 2.0 / math.sqrt(3.0)
    phi_end = math.log(t_end) / alpha_float
    table: list[dict[str, float | int]] = []
    for n_star in model["pivot_efolds"]:
        t_star, root_residual = solve_pivot_t(float(n_star), t_end)
        phi_star = math.log(t_star) / alpha_float
        x_star = 1.0 / t_star
        potential = 0.75 * mass_scale**2 * (1.0 - x_star) ** 2
        epsilon_star = (4.0 / 3.0) * x_star**2 / (1.0 - x_star) ** 2
        eta_star = (4.0 / 3.0) * x_star * (2.0 * x_star - 1.0) / (1.0 - x_star) ** 2
        h_star = math.sqrt(potential / 3.0)
        scalar_power = potential / (24.0 * math.pi**2 * epsilon_star)
        tensor_power = 2.0 * h_star**2 / math.pi**2
        n_s = 1.0 - 6.0 * epsilon_star + 2.0 * eta_star
        r = 16.0 * epsilon_star
        h_equation_residual = abs(3.0 * h_star**2 - potential)
        consistency_residual = abs(tensor_power / scalar_power - r)
        ledger.numerical_check(
            f"CSBE.N{n_star}.pivot_root_residual",
            abs(root_residual) <= ROOT_RESIDUAL_BOUND,
            "The bounded monotone pivot root satisfies its declared N_star equation.",
            abs(root_residual),
            ROOT_RESIDUAL_BOUND,
        )
        ledger.numerical_check(
            f"CSBE.N{n_star}.H_equation_residual",
            h_equation_residual <= ROOT_RESIDUAL_BOUND,
            "The exported H_star satisfies 3H_star^2=V_star within floating residual.",
            h_equation_residual,
            ROOT_RESIDUAL_BOUND,
        )
        ledger.numerical_check(
            f"CSBE.N{n_star}.power_ratio_residual",
            consistency_residual <= ROOT_RESIDUAL_BOUND,
            "The exported leading spectra obey P_T/P_R=r within floating residual.",
            consistency_residual,
            ROOT_RESIDUAL_BOUND,
        )
        table.append(
            {
                "N_star_input": int(n_star),
                "phi_star": phi_star,
                "t_star": t_star,
                "H_star": h_star,
                "epsilon_V_star": epsilon_star,
                "eta_V_star": eta_star,
                "P_R_leading_slow_roll": scalar_power,
                "P_T_leading_slow_roll": tensor_power,
                "n_s_leading_slow_roll": n_s,
                "r_leading_slow_roll": r,
                "pivot_root_residual": root_residual,
                "H_equation_residual": h_equation_residual,
                "power_ratio_residual": consistency_residual,
            }
        )

    exact_pass = all(item["passed"] for item in ledger.exact)
    numerical_pass = all(item["passed"] for item in ledger.numerical)
    passed = exact_pass and numerical_pass
    verdict = (
        "KEEP_STAROBINSKY_LEADING_SLOW_ROLL_BACKGROUND_EXPORT_NOT_CLOSED_EVOLUTION_OR_LIKELIHOOD"
        if passed
        else "KILL_DECLARED_STAROBINSKY_BACKGROUND_EXPORT"
    )
    impact = "EXPORT_DECLARED_BACKGROUND_INPUT_TABLE_ONLY" if passed else "DO_NOT_USE_THIS_BACKGROUND_PACKET_DOWNSTREAM"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_model_and_units": model,
        "exact_checks": ledger.exact,
        "numerical_checks": ledger.numerical,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "numerical_passed": sum(item["passed"] for item in ledger.numerical),
            "numerical_total": len(ledger.numerical),
            "all_executable_checks_passed": passed,
        },
        "formulae": {
            "Vprime_over_V": "2*sqrt(2/3)*x/(1-x)",
            "epsilon_V": "(4/3)*x^2/(1-x)^2",
            "eta_V": "(4/3)*x*(2*x-1)/(1-x)^2",
            "t_end": "1+2/sqrt(3)",
            "N_pivot": "(3/4)*[(t_star-log(t_star))-(t_end-log(t_end))]",
        },
        "endpoint": {"t_end": t_end, "phi_end": phi_end, "epsilon_V_end": 1.0},
        "background_export_table": table,
        "computed_scope": "leading potential-slow-roll background export at independently supplied N_star values only",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": len(model["pivot_efolds"]),
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def write_result(path: Path, result: dict[str, Any]) -> tuple[str, int]:
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result exceeds artifact cap")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> int:
    payload, input_sha256 = read_input()
    result = run(payload, input_sha256)
    outer_sha256, size = write_result(Path(__file__).with_name(RESULT_NAME), result)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "numerical_passed": result["check_summary"]["numerical_passed"],
                "numerical_total": result["check_summary"]["numerical_total"],
                "result": RESULT_NAME,
                "result_sha256": outer_sha256,
                "result_bytes": size,
                "automatic_next": None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
