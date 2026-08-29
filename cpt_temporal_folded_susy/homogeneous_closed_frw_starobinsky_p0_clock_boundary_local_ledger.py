#!/usr/bin/env python3
"""Local P=0 clock-boundary vector-field ledger; deliberately no ODE solve."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath
from mpmath import mp
import sympy as sp

INPUT_NAME = "HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_P0_CLOCK_BOUNDARY_LOCAL_LEDGER_INPUTS.json"
RESULT_NAME = "HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_P0_CLOCK_BOUNDARY_LOCAL_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/homogeneous_closed_frw_starobinsky_p0_clock_boundary_local_ledger.py"
EXPECTED_INPUT_SHA256 = "e816103e4f5c92952c7b53572e6905a176e86cde1c2d42247d9cc4efa9f4a888"
CALCULATION_ID = "HomogeneousClosedFrwStarobinskyP0ClockBoundaryLocalLedger"
ARTIFACT_CAP = 1_000_000


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def nulls() -> dict[str, Any]:
    return {"trajectory_initial_condition_selection": None, "trajectory_integration": None, "trajectory_locus_crossing": None, "complete_relational_observables": None, "quantum_clock_change_map": None, "physical_inner_product": None, "born_oppenheimer_or_decoherence": None, "class_or_cobaya_input": None, "empirical_likelihood": None, "full_scalar_vector_tensor_or_adm_hda": None, "quantum_bfv_anomaly_freedom": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def tolerances() -> dict[str, str]:
    return {"constraint_relative": "1e-50", "y_reconstruction_absolute": "1e-50", "p_sign_symmetry_relative": "1e-50", "tangent_absolute": "1e-50", "minimum_transverse_abs_ydot": "1e-30"}


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def _id(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate check id {ident}")
        self.seen.add(ident)

    def exact_check(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self._id(ident)
        simplified = sp.simplify(residual)
        self.exact.append({"id": ident, "passed": bool(simplified == 0), "statement": statement, "residual": str(simplified)})

    def numerical_check(self, ident: str, passed: bool, statement: str, **data: str) -> None:
        self._id(ident)
        self.numerical.append({"id": ident, "passed": bool(passed), "statement": statement, **data})

    def guard(self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        self._id(ident)
        self.guards.append({"id": ident, "verified": True, "verification_mode": "ANALYTIC_SCOPE_GUARD_NOT_AN_EXECUTABLE_TRAJECTORY_OR_CROSSING_PREDICATE", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})


def verified_upstream(root: Path, spec: dict[str, str]) -> dict[str, Any]:
    raw = (root / spec["path"]).read_bytes()
    if digest(raw) != spec["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {spec['path']}")
    data = json.loads(raw)
    for key, expected in (("result_payload_sha256_without_self", spec["payload_sha256_without_self"]), ("verdict", spec["required_verdict"]), ("run_status", "VALID_RUN")):
        if data.get(key) != expected:
            raise AssertionError(f"upstream field mismatch {key}: {spec['path']}")
    return data


def relative_constraint(C: mp.mpf, terms: list[mp.mpf]) -> mp.mpf:
    return abs(C) / max(mp.fsum(abs(term) for term in terms), mp.mpf(1))


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if digest(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.homogeneous-closed-frw-starobinsky-p0-clock-boundary-local-ledger.input.v1" or cfg["calculation_id"] != CALCULATION_ID or cfg["numbered_phase"] is not None:
        raise AssertionError("identity drift")
    if cfg["resource_caps"] != caps() or cfg["tolerances"] != tolerances() or cfg["required_fail_closed_outputs"] != nulls():
        raise AssertionError("cap/tolerance/fail-closed drift")
    root = Path(__file__).resolve().parent.parent
    background, domain = (verified_upstream(root, item) for item in cfg["upstream_results"])
    table = background["background_export_table"]
    if [row["N_star_input"] for row in table] != [50, 55, 60] or len(table) != 3:
        raise AssertionError("pinned pivot table mutation")
    mp.dps = int(cfg["declared_conventions"]["numeric_precision_digits"])
    M = mp.mpf(str(background["declared_model_and_units"]["mass_scale_M"]))
    audit = Audit()
    Q, P, phi, p = sp.symbols("Q P phi p", real=True)
    M_sym = sp.symbols("M", positive=True, real=True)
    alpha = sp.sqrt(sp.Rational(2, 3))
    V = 3 * M_sym**2 / 4 * (1 - sp.exp(-alpha * phi))**2
    C = -sp.exp(-3 * Q / 2) * P**2 / (6 * sp.pi**2) + sp.exp(-3 * Q / 2) * p**2 / (4 * sp.pi**2) - 6 * sp.pi**2 * sp.exp(Q / 2) + 2 * sp.pi**2 * sp.exp(3 * Q / 2) * V
    qdot, phidot, pdot, Pdot = sp.diff(C, P), sp.diff(C, p), -sp.diff(C, phi), -sp.diff(C, Q)
    y = sp.exp(Q) * V
    ydot = sp.simplify(sp.diff(y, Q) * qdot + sp.diff(y, phi) * phidot)
    expected_ydot = sp.exp(-Q / 2) * (-2 * P * V + 3 * p * sp.diff(V, phi)) / (6 * sp.pi**2)
    p0_family = 8 * sp.pi**4 * sp.exp(2 * Q) * (3 - y)
    constraint_on_family = sp.simplify(C.subs({P: 0, p**2: p0_family}))
    hamilton_preservation = sp.simplify(sp.diff(C, Q) * qdot + sp.diff(C, P) * Pdot + sp.diff(C, phi) * phidot + sp.diff(C, p) * pdot)
    audit.exact_check("p0local.exact.hamilton_Q", qdot + sp.exp(-3 * Q / 2) * P / (3 * sp.pi**2), "The N=1 Q Hamilton equation has the declared sign and coefficient.")
    audit.exact_check("p0local.exact.hamilton_phi", phidot - sp.exp(-3 * Q / 2) * p / (2 * sp.pi**2), "The N=1 phi Hamilton equation has the declared sign and coefficient.")
    audit.exact_check("p0local.exact.hamilton_p", pdot + 2 * sp.pi**2 * sp.exp(3 * Q / 2) * sp.diff(V, phi), "The N=1 p Hamilton equation has the declared sign and coefficient.")
    expected_Pdot = -sp.exp(-3 * Q / 2) * P**2 / (4 * sp.pi**2) + 3 * sp.exp(-3 * Q / 2) * p**2 / (8 * sp.pi**2) + 3 * sp.pi**2 * sp.exp(Q / 2) - 3 * sp.pi**2 * sp.exp(3 * Q / 2) * V
    audit.exact_check("p0local.exact.hamilton_P", Pdot - expected_Pdot, "The N=1 P Hamilton equation has the declared sign and coefficient.")
    audit.exact_check("p0local.exact.ydot", ydot - expected_ydot, "Chain rule plus the N=1 Hamilton equations gives the declared ydot formula.")
    audit.exact_check("p0local.exact.constraint_family", constraint_on_family, "The P=0 family p^2=8*pi^4 e^(2Q)(3-y) solves C=0 identically.")
    audit.exact_check("p0local.exact.hamilton_preservation", hamilton_preservation, "For the autonomous N=1 Hamilton vector field, dC/dt={C,C}=0.")
    p_clock_on_family = sp.simplify(Pdot.subs(P, 0).subs(p**2, p0_family))
    audit.exact_check("p0local.exact.P_clock_factor_on_family", p_clock_on_family - 6 * sp.pi**2 * sp.exp(Q / 2) * (2 - y), "On C=0=P, Pdot reduces to 6*pi^2*exp(Q/2)*(2-y).")
    y2_ydot_squared = sp.expand(expected_ydot.subs(P, 0)**2).subs(p**2, 8 * sp.pi**4 * sp.exp(2 * Q))
    audit.exact_check("p0local.exact.y2_transverse_square", y2_ydot_squared - 2 * sp.exp(Q) * sp.diff(V, phi)**2, "On the y=2 P=0 constraint representative, ydot^2=2*exp(Q)*V_prime^2 and is positive when V_prime is nonzero.")
    audit.exact_check("p0local.exact.y3_tangent", expected_ydot.subs({P: 0, p: 0}), "At P=0=p the y=3 representative has ydot=0 at that instant.")
    audit.guard("p0local.guard.derived_not_selected", "constraint-surface parametrization", "each displayed point is algebraically derived from a pinned phi_star and a declared clock-boundary label y=2 or y=3", "these are boundary representatives, not selected cosmological initial conditions and not a trajectory ensemble")
    audit.guard("p0local.guard.transversality_not_crossing", "nonzero derivative implies local level-set transversality", "the local vector field exists with p*V_prime nonzero at y=2", "this records transversality at an instantaneous representative; it does not establish that a separately selected trajectory crosses y=2")
    audit.guard("p0local.guard.tangency_not_trajectory", "vanishing first derivative", "P=p=0 at the y=3 representative", "ydot=0 is first-order tangency only; no higher-order trajectory claim is made")
    rows: list[dict[str, Any]] = []
    sqrt23 = mp.sqrt(mp.mpf(2) / 3)
    for row in table:
        phi_value = mp.mpf(str(row["phi_star"]))
        x = mp.exp(-sqrt23 * phi_value)
        potential = 3 * M**2 / 4 * (1 - x)**2
        vprime = 3 * M**2 / 2 * sqrt23 * x * (1 - x)
        audit.numerical_check(f"p0local.N{row['N_star_input']}.potential_positive", potential > 0, "the pinned positive phi_star gives positive Starobinsky V", V=f"{mp.nstr(potential, 18)}")
        audit.numerical_check(f"p0local.N{row['N_star_input']}.Vprime_positive", vprime > 0, "the pinned positive phi_star gives nonzero positive V_prime", Vprime=f"{mp.nstr(vprime, 18)}")
        derived: list[dict[str, str]] = []
        for y_value, signs in ((mp.mpf(2), (-1, 1)), (mp.mpf(3), (0,))):
            Q_value = mp.log(y_value / potential)
            p_abs = mp.sqrt(8 * mp.pi**4 * mp.exp(2 * Q_value) * (3 - y_value))
            for sign in signs:
                p_value = mp.mpf(sign) * p_abs if sign else mp.mpf(0)
                P_value = mp.mpf(0)
                terms = [-mp.exp(-3 * Q_value / 2) * P_value**2 / (6 * mp.pi**2), mp.exp(-3 * Q_value / 2) * p_value**2 / (4 * mp.pi**2), -6 * mp.pi**2 * mp.exp(Q_value / 2), 2 * mp.pi**2 * mp.exp(3 * Q_value / 2) * potential]
                constraint = mp.fsum(terms)
                reconstructed_y = mp.exp(Q_value) * potential
                ydot_value = mp.exp(-Q_value / 2) * (-2 * P_value * potential + 3 * p_value * vprime) / (6 * mp.pi**2)
                label = f"N{row['N_star_input']}.y{int(y_value)}.p{sign:+d}"
                relative_C = relative_constraint(constraint, terms)
                audit.numerical_check(f"p0local.{label}.constraint", relative_C <= mp.mpf(cfg["tolerances"]["constraint_relative"]), "derived representative satisfies the declared constraint without projection", relative=f"{mp.nstr(relative_C, 12)}")
                audit.numerical_check(f"p0local.{label}.y_reconstruction", abs(reconstructed_y - y_value) <= mp.mpf(cfg["tolerances"]["y_reconstruction_absolute"]), "derived Q reconstructs the declared y label", absolute=f"{mp.nstr(abs(reconstructed_y-y_value), 12)}")
                if y_value == 2:
                    audit.numerical_check(f"p0local.{label}.transverse", abs(ydot_value) >= mp.mpf(cfg["tolerances"]["minimum_transverse_abs_ydot"]), "y=2 representative has nonzero local ydot", abs_ydot=f"{mp.nstr(abs(ydot_value), 18)}")
                else:
                    audit.numerical_check(f"p0local.{label}.tangent", abs(ydot_value) <= mp.mpf(cfg["tolerances"]["tangent_absolute"]), "y=3,p=0 representative has zero first y derivative", abs_ydot=f"{mp.nstr(abs(ydot_value), 12)}")
                derived.append({"label": label, "y": mp.nstr(y_value, 30), "Q": mp.nstr(Q_value, 30), "P": "0", "p": mp.nstr(p_value, 30), "constraint_relative": mp.nstr(relative_C, 12), "ydot": mp.nstr(ydot_value, 30), "role": "derived instantaneous boundary representative; not an initial condition or integrated trajectory"})
        y2minus, y2plus = derived[0], derived[1]
        parity = abs(mp.mpf(y2minus["ydot"]) + mp.mpf(y2plus["ydot"])) / max(abs(mp.mpf(y2plus["ydot"])), mp.mpf("1e-100"))
        audit.numerical_check(f"p0local.N{row['N_star_input']}.y2.branch_parity", parity <= mp.mpf(cfg["tolerances"]["p_sign_symmetry_relative"]), "the two y=2 p branches have opposite local ydot", relative=f"{mp.nstr(parity, 12)}")
        rows.append({"N_star_input": row["N_star_input"], "phi_star": mp.nstr(phi_value, 30), "M": mp.nstr(M, 20), "V_phi_star": mp.nstr(potential, 30), "Vprime_phi_star": mp.nstr(vprime, 30), "representatives": derived})
    passed = all(item["passed"] for item in audit.exact + audit.numerical)
    verdict = "KEEP_LOCAL_P0_CLOCK_BOUNDARY_VECTOR_FIELD_LEDGER_NOT_TRAJECTORY_EVIDENCE" if passed else "KILL_LOCAL_P0_CLOCK_BOUNDARY_VECTOR_FIELD_LEDGER"
    result: dict[str, Any] = {"schema_version": "ice.homogeneous-closed-frw-starobinsky-p0-clock-boundary-local-ledger.result.v1", "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": cfg["decision_table"][0 if passed else 1]["programme_impact"], "input_manifest": {"path": INPUT_RELPATH, "sha256": digest(raw)}, "upstream_results": [{"path": item["path"], "sha256": item["sha256"], "payload_sha256_without_self": item["payload_sha256_without_self"], "verdict": item["required_verdict"]} for item in cfg["upstream_results"]], "primary_sources": cfg["primary_sources"], "declared_conventions": cfg["declared_conventions"], "exact_checks": audit.exact, "numerical_checks": audit.numerical, "theorem_guards": audit.guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "numerical_passed": sum(item["passed"] for item in audit.numerical), "numerical_total": len(audit.numerical), "theorem_guard_count": len(audit.guards), "all_executable_checks_passed": passed}, "numerical_calculation": {"derived_boundary_representatives": rows, "scope": "instantaneous local vector-field representatives only; no trajectory integration or crossing census"}, "required_fail_closed_outputs": nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": digest(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "sympy": sp.__version__, "mpmath": mpmath.__version__}}
    result["result_payload_sha256_without_self"] = digest(canonical(result))
    encoded = canonical(result)
    if len(encoded) > ARTIFACT_CAP:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print("HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_P0_CLOCK_BOUNDARY_LOCAL_LEDGER_RESULT=" + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": digest(encoded), "result_size_bytes": len(encoded), "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
