#!/usr/bin/env python3
"""Finite-cutoff nonzero-lambda raw-C F_lambda check; not RAQ.

The propagation deliberately uses scaled linear two-component systems, not a
Riccati equation: roots 2 and 4 have a negative zero-shell K value at Q_0,
and a Riccati ratio can hit a node between the finite plus cutoff and Q_0.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp

INPUT_NAME = "RAW_C_NONZERO_LAMBDA_WEYL_FLAMBDA_CHECK_INPUTS.json"
RESULT_NAME = "RAW_C_NONZERO_LAMBDA_WEYL_FLAMBDA_CHECK_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_nonzero_lambda_weyl_flambda_check.py"
EXPECTED_INPUT_SHA256 = "f98874eb7eda4a4e51649a29c50513fd6e6520ac96df057e11eb8f361e66e034"
CALCULATION_ID = "RawCNonzeroLambdaWeylFlambdaCheck"
ARTIFACT_CAP = 1_000_000


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def nulls() -> dict[str, Any]:
    return {"global_raw_C_spectral_measure": None, "global_delta_C_measure": None, "raw_C_rigging_test_space": None, "raw_C_rigging_map": None, "raw_C_physical_inner_product": None, "physical_inner_product_positivity": None, "physical_observable_action": None, "raw_C_RAQ_completion": None, "quantum_constraint_rescaling_equivalence": None, "selected_H_raw_C_unitary_intertwiner": None, "general_p_mixing_extension_classification": None, "canonical_p_zero_origin_sector": None, "absolute_bfv_measure": None, "continuum_determinant_or_pfaffian_line": None, "inhomogeneous_constraint_closure": None, "quantum_bfv_anomaly_freedom": None, "relational_observables_or_decoherence": None, "empirical_likelihood": None, "quantum_gravity_claim": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "ode_calls": 4500, "maximum_segments": 4500, "automatic_descendants": 0}


def expected_tolerances() -> dict[str, str]:
    return {"lambda_zero_characteristic": "2e-7", "delta_refinement_relative": "2e-3", "plus_cutoff_relative": "1e-2", "minus_cutoff_relative": "1e-3", "conditional_prediction_relative": "3e-2", "p_parity_relative": "1e-7", "lambda_zero_wronskian_absolute": "1e-9", "minimum_abs_normalization_at_Q0": "1e-9", "minimum_A_at_Qplus": "1"}


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    ode_calls: int = 0
    segments: int = 0

    def register(self, ident: str) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate audit id: {ident}")
        self.seen.add(ident)

    def exact_check(self, ident: str, residual: sp.Expr, statement: str) -> None:
        self.register(ident)
        simplified = sp.simplify(residual)
        self.exact.append({"id": ident, "passed": bool(simplified == 0), "statement": statement, "residual": str(simplified)})

    def check(self, ident: str, passed: bool, statement: str, **data: str) -> None:
        self.register(ident)
        self.numerical.append({"id": ident, "passed": bool(passed), "statement": statement, **data})

    def guard(self, ident: str, theorem: str, hypotheses: str, conclusion_and_scope: str) -> None:
        self.register(ident)
        self.guards.append({"id": ident, "verified": True, "verification_mode": "SOURCE_PIN_AND_ANALYTIC_HYPOTHESIS_SCOPE_AUDIT_NOT_AN_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": conclusion_and_scope})


def upstream(root: Path, item: dict[str, str]) -> dict[str, Any]:
    raw = (root / item["path"]).read_bytes()
    if digest(raw) != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    data = json.loads(raw)
    for key, want in (("result_payload_sha256_without_self", item["payload_sha256_without_self"]), ("verdict", item["required_verdict"]), ("run_status", "VALID_RUN")):
        if data.get(key) != want:
            raise AssertionError(f"upstream field mismatch {key}: {item['path']}")
    return data


def coefficient(Q: float, p: float, lam: float) -> tuple[float, float]:
    e2, e32 = np.exp(2 * Q), np.exp(1.5 * Q)
    a = (72 * np.pi**4 * e2 + 12 * np.pi**2 * lam * e32 - 3 * p * p) / 2
    ap = (144 * np.pi**4 * e2 + 18 * np.pi**2 * lam * e32) / 2
    return float(a), float(ap)


def rhs(p: float, lam: float):
    def f(Q: float, y: np.ndarray) -> np.ndarray:
        a, _ = coefficient(Q, p, lam)
        return np.array([y[1], a * y[0]], dtype=float)
    return f


def scaled_integrate(audit: Audit, y: np.ndarray, start: float, stop: float, p: float, lam: float, cfg: dict[str, Any]) -> tuple[np.ndarray, float]:
    """Piecewise propagation with rescaling and its retained log amplitude."""
    width = float(cfg["declared_conventions"]["segment_width"])
    count = max(1, int(np.ceil(abs(stop - start) / width)))
    if audit.segments + count > int(cfg["resource_caps"]["maximum_segments"]):
        raise AssertionError("segment cap exceeded")
    grid = np.linspace(start, stop, count + 1)
    current = np.asarray(y, dtype=float)
    log_amplitude = 0.0
    for left, right in zip(grid[:-1], grid[1:]):
        audit.ode_calls += 1
        if audit.ode_calls > int(cfg["resource_caps"]["ode_calls"]):
            raise AssertionError("ODE-call cap exceeded")
        sol = solve_ivp(rhs(p, lam), (float(left), float(right)), current, method=cfg["declared_conventions"]["method"], rtol=float(cfg["declared_conventions"]["rtol"]), atol=float(cfg["declared_conventions"]["atol"]), t_eval=[float(right)])
        if not sol.success or sol.y.shape != (2, 1) or not np.all(np.isfinite(sol.y[:, -1])):
            raise AssertionError("linear ODE solve failed")
        current = sol.y[:, -1]
        scale = float(np.max(np.abs(current)))
        if not np.isfinite(scale) or scale == 0.0:
            raise AssertionError("zero or non-finite propagated linear state")
        current = current / scale
        log_amplitude += float(np.log(scale))
        audit.segments += 1
    return current, log_amplitude


def w(y: np.ndarray, c: np.ndarray) -> float:
    return float(y[0] * c[1] - y[1] * c[0])


def initial_plus(Qplus: float, p: float, lam: float, tol: dict[str, str]) -> tuple[np.ndarray, float]:
    a, ap = coefficient(Qplus, p, lam)
    if not np.isfinite(a) or a <= float(tol["minimum_A_at_Qplus"]):
        raise AssertionError("finite plus-end WKB coefficient is not positive enough")
    # Decaying WKB sign.  Its finite-Q nature is controlled by the second Qplus.
    return np.array([1.0, -(np.sqrt(a) + ap / (4 * a))], dtype=float), a


def reference_pair(Qminus: float, p: float, cfg: dict[str, Any], audit: Audit) -> tuple[np.ndarray, float]:
    # c(Q0)=1,c'(Q0)=0 at lambda=0; its backward propagation is exact on this finite interval.
    return scaled_integrate(audit, np.array([1.0, 0.0]), -4.0, Qminus, p, 0.0, cfg)


def finite_characteristic(Qplus: float, Qminus: float, p: float, lam: float, cminus: tuple[np.ndarray, float], cfg: dict[str, Any], audit: Audit) -> tuple[float, float, float, float]:
    y0, aplus = initial_plus(Qplus, p, lam, cfg["tolerances"])
    at_q0, _ = scaled_integrate(audit, y0, Qplus, -4.0, p, lam, cfg)
    denominator = float(at_q0[0])
    if abs(denominator) < float(cfg["tolerances"]["minimum_abs_normalization_at_Q0"]):
        raise AssertionError("node or near-zero normalization value at Q0")
    normalized = at_q0 / denominator
    yminus, ylog = scaled_integrate(audit, normalized, -4.0, Qminus, p, lam, cfg)
    cvector, clog = cminus
    factor = float(np.exp(ylog + clog))
    if not np.isfinite(factor):
        raise AssertionError("scaled-Wronskian amplitude overflow")
    return -factor * w(yminus, cvector), denominator, aplus, float(normalized[1])


def conditional_prediction(row: dict[str, str]) -> float:
    # Upstream is F_lambda=-N_f/(2a) for unnormalized K.  Here u(Q0)=1, so divide once more by a.
    a, nf = float(row["a_at_Q0"]), float(row["N_f_mellin"])
    return -nf / (2 * a * a)


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("no command-line arguments are accepted")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if digest(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.raw-c-nonzero-lambda-weyl-flambda-check.input.v1" or cfg["calculation_id"] != CALCULATION_ID or cfg["numbered_phase"] is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if cfg["required_fail_closed_outputs"] != nulls() or cfg["resource_caps"] != expected_caps() or cfg["tolerances"] != expected_tolerances():
        raise AssertionError("identity or fail-closed mutation")
    root = Path(__file__).resolve().parent.parent
    census, jacobian = (upstream(root, item) for item in cfg["upstream_results"])
    roots = census["numerical_calculation"]["roots"]
    jrows = jacobian["numerical_calculation"]["roots"]
    if len(roots) != 5 or len(jrows) != 5:
        raise AssertionError("five-root pin failed")
    if [str(row["kappa"]) for row in roots] != [str(row["kappa"]) for row in jrows]:
        raise AssertionError("upstream root-order or kappa agreement failed")
    audit = Audit()
    Q_symbol, p_symbol, lambda_symbol = sp.symbols("Q p lambda", real=True)
    u_symbol, up_symbol, upp_symbol = sp.symbols("u up upp")
    a_symbol, nf_symbol = sp.symbols("a N_f", nonzero=True)
    A_symbol = (72 * sp.pi**4 * sp.exp(2 * Q_symbol) + 12 * sp.pi**2 * lambda_symbol * sp.exp(sp.Rational(3, 2) * Q_symbol) - 3 * p_symbol**2) / 2
    raw_equation = 2 * upp_symbol + (3 * p_symbol**2 - 72 * sp.pi**4 * sp.exp(2 * Q_symbol) - 12 * sp.pi**2 * lambda_symbol * sp.exp(sp.Rational(3, 2) * Q_symbol)) * u_symbol
    audit.exact_check("rawc.weyl.ode", raw_equation / 2 - (upp_symbol - A_symbol * u_symbol), "The declared fiber equation is algebraically the linear system u''=A(Q;p,lambda)u.")
    audit.exact_check("rawc.weyl.boundary_sign", -(u_symbol * 0 - up_symbol * 1) - up_symbol, "At Q0 only, c=1 and c'=0 imply -W(u,c)=u'.")
    audit.exact_check("rawc.weyl.normalization_conversion", (-nf_symbol / (2 * a_symbol)) / a_symbol + nf_symbol / (2 * a_symbol**2), "Dividing a solution with u(Q0)=a by a sends the conditional derivative to -N_f/(2a^2).")
    audit.exact_check("rawc.weyl.p_parity_coefficient", A_symbol - A_symbol.subs(p_symbol, -p_symbol), "The finite ODE coefficient is even under p to minus p.")
    audit.guard("rawc.weyl.guard.finite_wkb", "leading Liouville-Green/WKB decaying datum with its first amplitude correction", "A(Qplus)>0 at each evaluated finite Qplus and lambda", "This seeds a finite-cutoff proxy only; agreement of two Qplus values is not an exact plus-end Weyl theorem.")
    audit.guard("rawc.weyl.guard.finite_interval_wronskian", "linear ODE Wronskian/Lagrange identity", "u_lambda and the fixed lambda-zero reference pair are propagated on the same finite interval", "The computed characteristic is finite-Qminus data only and supplies no global spectral measure.")
    audit.guard("rawc.weyl.guard.central_difference", "symmetric finite-difference consistency", "the declared three-delta ladder is used and the two smallest estimates satisfy the plateau tolerance", "Agreement checks one local derivative near lambda=0, not analytic continuation or a root classification.")
    audit.guard("rawc.weyl.guard.linear_node_safe_route", "fundamental solution of a two-component linear system", "segmentwise rescaling multiplies both components by the same nonzero scalar and retains the log amplitude", "The propagation divides by u only once at the declared Q0 normalization check; it is not a Riccati evolution and does not prove the absence of nodes elsewhere.")
    rows: list[dict[str, Any]] = []
    qplus_main, qplus_control = (float(cfg["declared_conventions"][x]) for x in ("main_Q_plus", "control_Q_plus"))
    qminus_main, qminus_control = (float(cfg["declared_conventions"][x]) for x in ("main_Q_minus", "control_Q_minus"))
    deltas = [float(x) for x in cfg["declared_conventions"]["lambda_delta_ladder"]]
    for index, (root_row, jac_row) in enumerate(zip(roots, jrows), start=1):
        kappa, p = float(root_row["kappa"]), float(jac_row["p_positive"])
        observed: dict[str, dict[str, float]] = {}
        q0_zero_characteristics: dict[str, float] = {}
        denominators: list[float] = []
        amin = float("inf")
        c_main = reference_pair(qminus_main, p, cfg, audit)
        c_control = reference_pair(qminus_control, p, cfg, audit)
        for label, qp, qm, cminus in (("main", qplus_main, qminus_main, c_main), ("plus_control", qplus_control, qminus_main, c_main), ("minus_control", qplus_main, qminus_control, c_control)):
            values: dict[str, float] = {}
            for lam in (0.0, *[sign * delta for delta in deltas for sign in (-1.0, 1.0)]):
                value, denom, aplus, q0_characteristic = finite_characteristic(qp, qm, p, lam, cminus, cfg, audit)
                values[format(lam, ".8g")] = value
                if lam == 0.0:
                    q0_zero_characteristics[label] = q0_characteristic
                denominators.append(abs(denom)); amin = min(amin, aplus)
            derivatives = [(values[format(delta, ".8g")] - values[format(-delta, ".8g")]) / (2 * delta) for delta in deltas]
            observed[label] = {"F0": values["0"], "d1": derivatives[0], "d2": derivatives[1], "d3": derivatives[2]}
        prediction = conditional_prediction(jac_row)
        plateau = abs(observed["main"]["d3"] - observed["main"]["d2"]) / max(abs(observed["main"]["d3"]), 1e-300)
        plus_shift = abs(observed["plus_control"]["d3"] - observed["main"]["d3"]) / max(abs(observed["main"]["d3"]), 1e-300)
        minus_shift = abs(observed["minus_control"]["d3"] - observed["main"]["d3"]) / max(abs(observed["main"]["d3"]), 1e-300)
        prediction_error = abs(observed["main"]["d3"] - prediction) / max(abs(prediction), 1e-300)
        f0 = abs(observed["main"]["F0"])
        wronskian_error = abs(observed["main"]["F0"] - q0_zero_characteristics["main"])
        parity_p = -p
        # Even p^2 equation: direct one-delta parity sentinel at the main cutoffs.
        c_parity = reference_pair(qminus_main, parity_p, cfg, audit)
        fplus, _, _, _ = finite_characteristic(qplus_main, qminus_main, parity_p, deltas[-1], c_parity, cfg, audit)
        fminus, _, _, _ = finite_characteristic(qplus_main, qminus_main, parity_p, -deltas[-1], c_parity, cfg, audit)
        parity_error = abs((fplus - fminus) / (2 * deltas[-1]) - observed["main"]["d3"]) / max(abs(observed["main"]["d3"]), 1e-300)
        audit.check(f"rawc.weyl.root{index}.normalization", min(denominators) >= float(cfg["tolerances"]["minimum_abs_normalization_at_Q0"]), "all finite-cutoff initial data have a nonzero Q0 normalization denominator", minimum_abs_denominator=f"{min(denominators):.4e}")
        audit.check(f"rawc.weyl.root{index}.lambda_zero", f0 <= float(cfg["tolerances"]["lambda_zero_characteristic"]), "lambda=0 finite characteristic is small at the main cutoffs", error=f"{f0:.4e}")
        audit.check(f"rawc.weyl.root{index}.lambda_zero_wronskian", wronskian_error <= float(cfg["tolerances"]["lambda_zero_wronskian_absolute"]), "at lambda=0 the propagated finite-Qminus Wronskian agrees with -W=u' evaluated at Q0", absolute=f"{wronskian_error:.4e}")
        audit.check(f"rawc.weyl.root{index}.delta_plateau", plateau <= float(cfg["tolerances"]["delta_refinement_relative"]), "two smallest central-difference deltas agree", relative=f"{plateau:.4e}")
        audit.check(f"rawc.weyl.root{index}.plus_cutoff", plus_shift <= float(cfg["tolerances"]["plus_cutoff_relative"]), "finite Qplus control agrees with main", relative=f"{plus_shift:.4e}")
        audit.check(f"rawc.weyl.root{index}.minus_cutoff", minus_shift <= float(cfg["tolerances"]["minus_cutoff_relative"]), "finite Qminus control agrees with main", relative=f"{minus_shift:.4e}")
        audit.check(f"rawc.weyl.root{index}.conditional_prediction", prediction_error <= float(cfg["tolerances"]["conditional_prediction_relative"]), "finite-cutoff derivative agrees with separately pinned conditional identity", relative=f"{prediction_error:.4e}")
        audit.check(f"rawc.weyl.root{index}.p_parity", parity_error <= float(cfg["tolerances"]["p_parity_relative"]), "direct plus/minus-p finite difference agrees because the equation has p squared", relative=f"{parity_error:.4e}")
        rows.append({"root_index": index, "kappa": kappa, "p_positive": p, "conditional_normalized_F_lambda": prediction, "minimum_plus_A": amin, "minimum_abs_Q0_normalization": min(denominators), "main": observed["main"], "plus_control": observed["plus_control"], "minus_control": observed["minus_control"], "lambda_zero_Q0_characteristic": q0_zero_characteristics["main"], "lambda_zero_wronskian_absolute_error": wronskian_error, "relative_delta_refinement": plateau, "relative_plus_cutoff_shift": plus_shift, "relative_minus_cutoff_shift": minus_shift, "relative_conditional_prediction_error": prediction_error, "relative_p_parity_error": parity_error})
    passed = all(item["passed"] for item in audit.exact + audit.numerical)
    verdict = "KEEP_FINITE_CUTOFF_NONZERO_LAMBDA_CHECK_OF_DECLARED_RAW_C_LOCAL_FLAMBDA_ONLY" if passed else "KILL_FINITE_CUTOFF_NONZERO_LAMBDA_CHECK"
    impact = cfg["decision_table"][0 if passed else 1]["programme_impact"]
    result: dict[str, Any] = {"schema_version": "ice.raw-c-nonzero-lambda-weyl-flambda-check.result.v1", "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": impact, "input_manifest": {"path": INPUT_RELPATH, "sha256": digest(raw)}, "upstream_results": [{"path": item["path"], "sha256": item["sha256"], "payload_sha256_without_self": item["payload_sha256_without_self"], "verdict": item["required_verdict"]} for item in cfg["upstream_results"]], "primary_sources": cfg["primary_sources"], "declared_conventions": cfg["declared_conventions"], "assumptions": cfg["assumptions"], "exact_checks": audit.exact, "numerical_checks": audit.numerical, "theorem_guards": audit.guards, "check_summary": {"exact_passed": sum(item["passed"] for item in audit.exact), "exact_total": len(audit.exact), "numerical_passed": sum(item["passed"] for item in audit.numerical), "numerical_total": len(audit.numerical), "theorem_guard_count": len(audit.guards), "all_executable_checks_passed": passed}, "numerical_calculation": {"roots": rows, "scope": "finite-cutoff numerical check of one declared local characteristic derivative only"}, "required_fail_closed_outputs": nulls(), "resource_accounting": {"ode_calls": audit.ode_calls, "segments": audit.segments, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": digest(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "sympy": sp.__version__}}
    result["result_payload_sha256_without_self"] = digest(canonical(result))
    encoded = canonical(result)
    if len(encoded) > ARTIFACT_CAP:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print("RAW_C_NONZERO_LAMBDA_WEYL_FLAMBDA_CHECK_RESULT=" + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "exact": result["check_summary"]["exact_total"], "numerical": result["check_summary"]["numerical_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result_sha256": digest(encoded), "result_size_bytes": len(encoded), "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
