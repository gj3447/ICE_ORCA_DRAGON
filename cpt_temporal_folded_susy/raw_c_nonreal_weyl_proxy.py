#!/usr/bin/env python3
"""Finite-cutoff nonreal Weyl proxy for one selected raw-C extension.

This unnumbered bounded calculation does not interpolate the previously found
real characteristic roots.  For the declared Gamma_1,p=0 extension it solves
the raw-C fiber equation at a small upper-half-plane grid, forms

    M_cut(z;p) = -Gamma_1(u_plus,z) / Gamma_0(u_plus,z),

and checks the Green--Lagrange identity, the expected positive imaginary sign,
two endpoint cutoffs, p parity, and a second ODE algorithm.  The finite WKB
datum and finite boundary cutoffs make this a numerical proxy only.  No
singular-endpoint Weyl function, spectral measure, rigging map, RAQ space, or
C/H equivalence is produced.

Primary operator-theoretic baseline: Eckhardt, Gesztesy, Nichols and Teschl,
arXiv:1208.4677v2.  The paper supplies definitions and theorem scope, not the
model-specific computation below.
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


INPUT_NAME = "RAW_C_NONREAL_WEYL_PROXY_INPUTS.json"
RESULT_NAME = "RAW_C_NONREAL_WEYL_PROXY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_nonreal_weyl_proxy.py"
EXPECTED_INPUT_SHA256 = "b55e3342c32706c0cc68294b0f7361c3654a2a23b568fa876a2abcd7a2d859b0"
CALCULATION_ID = "RawCNonrealWeylProxy"
RESULT_SCHEMA = "ice.raw-c-nonreal-weyl-proxy.result.v1"
RESULT_PREFIX = "RAW_C_NONREAL_WEYL_PROXY_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


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
        "ode_calls": 80,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "singular_endpoint_nonreal_weyl_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_spectral_multiplicity": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "general_p_mixing_extension_classification": None,
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


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    ode_calls: int = 0

    def register(self, check_id: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen.add(check_id)

    def exact_check(self, check_id: str, passed: bool, statement: str) -> None:
        self.register(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )

    def numerical_check(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        **observed: str,
    ) -> None:
        self.register(check_id)
        self.numerical.append(
            {
                "id": check_id,
                "passed": bool(passed),
                "statement": statement,
                **observed,
            }
        )

    def guard(
        self,
        guard_id: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(guard_id)
        self.guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": (
                    "SOURCE_PIN_AND_ANALYTIC_HYPOTHESIS_SCOPE_AUDIT_"
                    "NOT_AN_EXECUTABLE_PROOF"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    for key, expected in (
        ("run_status", "VALID_RUN"),
        ("verdict", item["required_verdict"]),
        (
            "result_payload_sha256_without_self",
            item["payload_sha256_without_self"],
        ),
    ):
        if payload.get(key) != expected:
            raise AssertionError(f"upstream field mismatch: {item['path']}:{key}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def coefficient(q: float, p: float, z: complex) -> tuple[complex, complex]:
    e2 = np.exp(2.0 * q)
    e32 = np.exp(1.5 * q)
    value = 36.0 * np.pi**4 * e2 + 6.0 * np.pi**2 * z * e32 - 1.5 * p * p
    derivative = 72.0 * np.pi**4 * e2 + 9.0 * np.pi**2 * z * e32
    return complex(value), complex(derivative)


def weight(q: float) -> float:
    return float(12.0 * np.pi**2 * np.exp(1.5 * q))


def reference_rhs(p: float):
    def rhs(q: float, y: np.ndarray) -> np.ndarray:
        value, _ = coefficient(q, p, 0.0j)
        a = float(value.real)
        return np.array([y[1], a * y[0], y[3], a * y[2]], dtype=float)

    return rhs


def nonreal_rhs(p: float, z: complex):
    def rhs(q: float, y: np.ndarray) -> np.ndarray:
        value, _ = coefficient(q, p, z)
        ur, ui, vr, vi, _integral = y
        return np.array(
            [
                vr,
                vi,
                value.real * ur - value.imag * ui,
                value.imag * ur + value.real * ui,
                -weight(q) * (ur * ur + ui * ui),
            ],
            dtype=float,
        )

    return rhs


def initial_plus(qplus: float, p: float, z: complex) -> np.ndarray:
    value, derivative = coefficient(qplus, p, z)
    root = np.sqrt(value)
    if root.real <= 0.0:
        root = -root
    logarithmic_derivative = -(root + derivative / (4.0 * value))
    return np.array(
        [
            1.0,
            0.0,
            logarithmic_derivative.real,
            logarithmic_derivative.imag,
            0.0,
        ],
        dtype=float,
    )


def solve_reference(
    audit: Audit,
    p: float,
    qminus: float,
    method: str,
    rtol: float,
    atol: float,
    ode_cap: int,
) -> np.ndarray:
    audit.ode_calls += 1
    if audit.ode_calls > ode_cap:
        raise AssertionError("ODE-call cap exceeded")
    sol = solve_ivp(
        reference_rhs(p),
        (-4.0, qminus),
        np.array([1.0, 0.0, 0.0, 1.0], dtype=float),
        method=method,
        rtol=rtol,
        atol=atol,
        t_eval=[qminus],
    )
    if not sol.success or sol.y.shape != (4, 1):
        raise AssertionError("reference-pair propagation failed")
    state = sol.y[:, -1]
    if not np.all(np.isfinite(state)):
        raise AssertionError("non-finite reference-pair state")
    return state


def solve_proxy(
    audit: Audit,
    p: float,
    z: complex,
    qplus: float,
    qminus: float,
    reference: np.ndarray,
    method: str,
    rtol: float,
    atol: float,
    ode_cap: int,
) -> dict[str, Any]:
    yplus = initial_plus(qplus, p, z)
    audit.ode_calls += 1
    if audit.ode_calls > ode_cap:
        raise AssertionError("ODE-call cap exceeded")
    sol = solve_ivp(
        nonreal_rhs(p, z),
        (qplus, qminus),
        yplus,
        method=method,
        rtol=rtol,
        atol=atol,
        t_eval=[qminus],
    )
    if not sol.success or sol.y.shape != (5, 1):
        raise AssertionError("nonreal proxy propagation failed")
    state = sol.y[:, -1]
    if not np.all(np.isfinite(state)):
        raise AssertionError("non-finite nonreal proxy state")

    uplus = complex(yplus[0], yplus[1])
    vplus = complex(yplus[2], yplus[3])
    uminus = complex(state[0], state[1])
    vminus = complex(state[2], state[3])
    integral = float(state[4])
    if integral <= 0.0 or not np.isfinite(integral):
        raise AssertionError("non-positive or non-finite weighted norm integral")

    c, cp, s, sp_value = (float(x) for x in reference)
    gamma0 = uminus * sp_value - vminus * s
    gamma1 = vminus * c - uminus * cp
    if gamma0 == 0.0j:
        raise AssertionError("zero finite-cutoff Gamma_0 denominator")
    m_proxy = -gamma1 / gamma0

    wplus = np.conjugate(uplus) * vplus - np.conjugate(vplus) * uplus
    wminus = np.conjugate(uminus) * vminus - np.conjugate(vminus) * uminus
    identity_residual = wplus - wminus - 1j * z.imag * integral
    identity_scale = max(abs(wplus), abs(wminus), abs(z.imag * integral), 1.0)

    return {
        "M": m_proxy,
        "gamma0_abs": abs(gamma0),
        "reference_wronskian": c * sp_value - cp * s,
        "green_lagrange_relative_residual": abs(identity_residual) / identity_scale,
        "weighted_norm_integral": integral,
        "finite_plus_flux_over_gamma0_sq": float(
            abs(wplus) / max(abs(gamma0) ** 2, np.finfo(float).tiny)
        ),
    }


def relative_complex(left: complex, right: complex) -> float:
    return float(abs(left - right) / max(abs(left), abs(right), 1.0e-15))


def as_complex_record(value: complex) -> dict[str, str]:
    return {"real": format(value.real, ".17g"), "imag": format(value.imag, ".17g")}


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_input_sha = sha256_bytes(raw)
    if observed_input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_input_sha}")
    cfg = json.loads(raw)
    if (
        cfg.get("schema_version") != "ice.raw-c-nonreal-weyl-proxy.input.v1"
        or cfg.get("calculation_id") != CALCULATION_ID
        or cfg.get("numbered_phase") is not None
    ):
        raise AssertionError("calculation identity mutation")
    if cfg.get("resource_caps") != expected_caps():
        raise AssertionError("resource-cap mutation")
    if cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")

    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in cfg["upstream_results"]]
    audit = Audit()

    q, p, x, y = sp.symbols("Q p x y", real=True)
    ur, ui, a, b = sp.symbols("u_r u_i a b", real=True)
    raw_a = 36 * sp.pi**4 * sp.exp(2 * q) + 6 * sp.pi**2 * (x + sp.I * y) * sp.exp(sp.Rational(3, 2) * q) - sp.Rational(3, 2) * p**2
    declared = (
        72 * sp.pi**4 * sp.exp(2 * q)
        + 12 * sp.pi**2 * (x + sp.I * y) * sp.exp(sp.Rational(3, 2) * q)
        - 3 * p**2
    ) / 2
    audit.exact_check(
        "rawc.nonreal.ode.convention",
        sp.simplify(raw_a - declared) == 0,
        "The declared raw-C eigenvalue equation is u''=A(Q;p,z)u.",
    )
    wronskian_derivative = sp.simplify(
        2 * sp.I * (ur * (b * ur + a * ui) - (a * ur - b * ui) * ui)
    )
    audit.exact_check(
        "rawc.nonreal.green_lagrange.derivative",
        sp.simplify(wronskian_derivative - 2 * sp.I * b * (ur**2 + ui**2)) == 0,
        "For u''=(a+ib)u, W(conj(u),u)'=2*i*b*|u|^2=i*Im(z)*f*|u|^2.",
    )
    g0, g1, c, cp, s, s_prime = sp.symbols(
        "Gamma_0 Gamma_1 c c_prime s s_prime"
    )
    u_reference = g0 * c + g1 * s
    up_reference = g0 * cp + g1 * s_prime
    audit.exact_check(
        "rawc.nonreal.boundary.reference_coordinates",
        sp.simplify(
            (u_reference * s_prime - up_reference * s)
            - g0 * (c * s_prime - cp * s)
        )
        == 0
        and sp.simplify(
            (up_reference * c - u_reference * cp)
            - g1 * (c * s_prime - cp * s)
        )
        == 0,
        "The Wronskian formulas recover Gamma_0 and Gamma_1 from u=Gamma_0*c+Gamma_1*s when W(c,s)=1.",
    )
    audit.exact_check(
        "rawc.nonreal.boundary.selected_zero",
        sp.simplify((-g1 / g0).subs(g1, 0)) == 0,
        "The selected Gamma_1=0 boundary line is the zero condition M=-Gamma_1/Gamma_0=0 when Gamma_0 is nonzero.",
    )
    audit.exact_check(
        "rawc.nonreal.parameter.p_parity",
        sp.simplify(raw_a.subs(p, -p) - raw_a) == 0,
        "The nonreal fiber coefficient is even in p.",
    )
    audit.guard(
        "rawc.nonreal.guard.singular_weyl_scope",
        "singular Weyl-Titchmarsh theory for a selected self-adjoint boundary condition",
        "the upstream result pins one Gamma_1=0 extension, while this runner uses only finite endpoint proxies at Im(z)>0",
        "M_cut is a consistency diagnostic; the singular endpoint limit, analytic Weyl function, Stieltjes measure and multiplicity remain unproved",
    )
    audit.guard(
        "rawc.nonreal.guard.finite_plus_wkb",
        "leading recessive Liouville-Green direction with first amplitude derivative",
        "the principal square root has positive real part at each finite Q_plus sample",
        "the two-Q_plus comparison controls only this finite proxy and is not a recessive endpoint theorem",
    )
    audit.guard(
        "rawc.nonreal.guard.green_lagrange",
        "finite-interval Green-Lagrange identity",
        "the same nonreal solution supplies the endpoint fluxes and weighted norm integral",
        "the identity and positive Im(M_cut) test signs and normalization only; neither constructs a spectral resolution nor proves positivity of an RAQ rigging form",
    )
    audit.guard(
        "rawc.nonreal.guard.independent_solver",
        "independent adaptive Runge-Kutta discretization comparison",
        "DOP853 and RK45 use the same equation, input and double-precision arithmetic but distinct step formulas and tighter control for RK45",
        "agreement detects one implementation class of numerical error; it is not interval validation",
    )

    conv = cfg["declared_conventions"]
    tol = {key: float(value) for key, value in cfg["tolerances"].items()}
    qplus_main = float(conv["main_Q_plus"])
    qplus_control = float(conv["control_Q_plus"])
    qminus_main = float(conv["main_Q_minus"])
    qminus_control = float(conv["control_Q_minus"])
    main_method = conv["main_method"]
    independent_method = conv["independent_method"]
    main_rtol = float(conv["main_rtol"])
    main_atol = float(conv["main_atol"])
    independent_rtol = float(conv["independent_rtol"])
    independent_atol = float(conv["independent_atol"])
    ode_cap = int(cfg["resource_caps"]["ode_calls"])

    reference_cache: dict[tuple[float, float, str, float, float], np.ndarray] = {}

    def get_reference(
        p_value: float,
        qminus: float,
        method: str,
        rtol: float,
        atol: float,
    ) -> np.ndarray:
        key = (abs(p_value), qminus, method, rtol, atol)
        if key not in reference_cache:
            reference_cache[key] = solve_reference(
                audit, abs(p_value), qminus, method, rtol, atol, ode_cap
            )
        return reference_cache[key]

    rows: list[dict[str, Any]] = []
    for p_text in conv["p_samples"]:
        p_value = float(p_text)
        for z_record in conv["z_samples"]:
            z = complex(float(z_record["real"]), float(z_record["imag"]))
            if z.imag <= 0.0:
                raise AssertionError("all z samples must lie in the upper half-plane")
            main = solve_proxy(
                audit,
                p_value,
                z,
                qplus_main,
                qminus_main,
                get_reference(p_value, qminus_main, main_method, main_rtol, main_atol),
                main_method,
                main_rtol,
                main_atol,
                ode_cap,
            )
            independent = solve_proxy(
                audit,
                p_value,
                z,
                qplus_main,
                qminus_main,
                get_reference(
                    p_value,
                    qminus_main,
                    independent_method,
                    independent_rtol,
                    independent_atol,
                ),
                independent_method,
                independent_rtol,
                independent_atol,
                ode_cap,
            )
            minus_control = solve_proxy(
                audit,
                p_value,
                z,
                qplus_main,
                qminus_control,
                get_reference(
                    p_value, qminus_control, main_method, main_rtol, main_atol
                ),
                main_method,
                main_rtol,
                main_atol,
                ode_cap,
            )
            plus_control = solve_proxy(
                audit,
                p_value,
                z,
                qplus_control,
                qminus_main,
                get_reference(p_value, qminus_main, main_method, main_rtol, main_atol),
                main_method,
                main_rtol,
                main_atol,
                ode_cap,
            )
            parity = solve_proxy(
                audit,
                -p_value,
                z,
                qplus_main,
                qminus_main,
                get_reference(-p_value, qminus_main, main_method, main_rtol, main_atol),
                main_method,
                main_rtol,
                main_atol,
                ode_cap,
            )

            independent_shift = relative_complex(main["M"], independent["M"])
            minus_shift = relative_complex(main["M"], minus_control["M"])
            plus_shift = relative_complex(main["M"], plus_control["M"])
            parity_shift = relative_complex(main["M"], parity["M"])
            label = f"p{p_text.replace('-', 'm').replace('.', '_')}_z{z.real:g}_{z.imag:g}i"
            audit.numerical_check(
                f"rawc.nonreal.{label}.reference_wronskian",
                abs(main["reference_wronskian"] - 1.0)
                <= tol["reference_wronskian_absolute"],
                "The propagated zero-energy reference pair retains W(c,s)=1.",
                absolute_error=format(abs(main["reference_wronskian"] - 1.0), ".8e"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.green_lagrange",
                main["green_lagrange_relative_residual"]
                <= tol["green_lagrange_relative"],
                "Endpoint fluxes and the weighted norm obey the finite Green-Lagrange identity.",
                relative_residual=format(
                    main["green_lagrange_relative_residual"], ".8e"
                ),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.imaginary_sign",
                main["M"].imag >= tol["minimum_imag_M"],
                "With M=-Gamma_1/Gamma_0, the finite proxy has positive imaginary part in the upper half-plane.",
                imag_M=format(main["M"].imag, ".17g"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.gamma0_nonzero",
                main["gamma0_abs"] >= tol["minimum_abs_gamma0"],
                "The finite-cutoff Gamma_0 denominator is separated from zero.",
                abs_gamma0=format(main["gamma0_abs"], ".8e"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.independent_method",
                independent_shift <= tol["independent_method_relative"],
                "DOP853 and tighter RK45 proxy values agree on the declared relative scale.",
                relative_shift=format(independent_shift, ".8e"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.minus_cutoff",
                minus_shift <= tol["minus_cutoff_relative"],
                "The Q_minus=-14 and -12 boundary-coordinate proxies agree within the declared control.",
                relative_shift=format(minus_shift, ".8e"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.plus_cutoff",
                plus_shift <= tol["plus_cutoff_relative"],
                "The Q_plus=1.6 and 1.4 WKB-seeded proxies agree within the declared control.",
                relative_shift=format(plus_shift, ".8e"),
            )
            audit.numerical_check(
                f"rawc.nonreal.{label}.p_parity",
                parity_shift <= tol["p_parity_relative"],
                "Direct p and -p proxy calculations agree for the p-squared fiber equation.",
                relative_shift=format(parity_shift, ".8e"),
            )
            rows.append(
                {
                    "p": format(p_value, ".17g"),
                    "z": as_complex_record(z),
                    "M_main": as_complex_record(main["M"]),
                    "M_independent": as_complex_record(independent["M"]),
                    "M_minus_control": as_complex_record(minus_control["M"]),
                    "M_plus_control": as_complex_record(plus_control["M"]),
                    "M_parity": as_complex_record(parity["M"]),
                    "abs_gamma0_main": format(main["gamma0_abs"], ".17g"),
                    "reference_wronskian_main": format(
                        main["reference_wronskian"], ".17g"
                    ),
                    "green_lagrange_relative_residual": format(
                        main["green_lagrange_relative_residual"], ".17g"
                    ),
                    "finite_plus_flux_over_gamma0_sq": format(
                        main["finite_plus_flux_over_gamma0_sq"], ".17g"
                    ),
                    "relative_independent_method_shift": format(
                        independent_shift, ".17g"
                    ),
                    "relative_minus_cutoff_shift": format(minus_shift, ".17g"),
                    "relative_plus_cutoff_shift": format(plus_shift, ".17g"),
                    "relative_p_parity_shift": format(parity_shift, ".17g"),
                }
            )

    executable = audit.exact + audit.numerical
    passed = all(item["passed"] for item in executable)
    decision = cfg["decision_table"][0 if passed else 1]
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": decision["verdict"],
        "programme_impact": decision["programme_impact"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": observed_input_sha},
        "upstream_results": upstream,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "assumptions": cfg["assumptions"],
        "exact_checks": audit.exact,
        "numerical_checks": audit.numerical,
        "theorem_guards": audit.guards,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in audit.exact),
            "exact_total": len(audit.exact),
            "numerical_passed": sum(item["passed"] for item in audit.numerical),
            "numerical_total": len(audit.numerical),
            "theorem_guard_count": len(audit.guards),
            "all_executable_checks_passed": passed,
        },
        "numerical_calculation": {
            "rows": rows,
            "scope": (
                "finite-cutoff nonreal Weyl proxy and Green-Lagrange calibration; "
                "not a singular endpoint limit or spectral transform"
            ),
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "ode_calls": audit.ode_calls,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "exact": result["check_summary"]["exact_total"],
                "numerical": result["check_summary"]["numerical_total"],
                "theorem_guards": result["check_summary"]["theorem_guard_count"],
                "ode_calls": audit.ode_calls,
                "result_sha256": sha256_bytes(encoded),
                "result_size_bytes": len(encoded),
                "automatic_next": None,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
