#!/usr/bin/env python3
"""Gate 1 -- local principal endpoint FIO for the V=0 Darboux chart.

This bounded calculation quantizes only the canonical graph carried by the
previously kept classical mixed generator W(c,P,p).  On compact interiors of
U_plus it checks the momentum-polarization phase -W, the positive principal
half-density D**(-1/2), the c=0 lineage, and the absence of a local twist
caustic.  It then applies an exact coarea discriminator to the uncorrected
one-term Van Vleck kernel.

The latter kernel is a principal semiclassical FIO, but its geometric-mean
composition density differs from the exact secant/coarea density.  This kills
exact finite-hbar unitarity of that one-term kernel only.  It does not kill a
separately constructed full-symbol or spectral transform and does not build a
BFV source, delta(C) rigging map, global endpoint state, physics claim, or TOE.
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


INPUT_NAME = "GATE1_V0_PRINCIPAL_ENDPOINT_FIO_INPUTS.json"
RESULT_NAME = "GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_v0_principal_endpoint_fio.py"
EXPECTED_INPUT_SHA256 = (
    "9f3bb3ff0758b0eacfd5ee6c42cd71ca1bf44c99ae822c35b768690031a4585f"
)
CALCULATION_ID = "Gate1V0PrincipalEndpointFIO"
RESULT_SCHEMA = "ice.gate1.v0-principal-endpoint-fio.result.v1"
RESULT_PREFIX = "GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
UPSTREAM_HASHES = {
    "cpt_temporal_folded_susy/GATE1_V0_OFFSHELL_DARBOUX_CHART_RESULT.json": (
        "6fcae74d9344984682c097731906ef1d4b1c01c4862c42ba54db7c464a7659f7"
    ),
    "cpt_temporal_folded_susy/GATE1_V0_OFFSHELL_DARBOUX_CHART.md": (
        "cdbe94f79b55db371e46d62455535af7d58d96ac2e6b21edae9e58b34d93e79f"
    ),
    "cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md": (
        "d3aa7abf86f4a65b98fbfd3bc9e9d8cf7d9c9cd596c2fcac34d113097e52f7ec"
    ),
    "cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md": (
        "6ab0707bd4c133c62087c90b1e0b7131609491c0e10ee004b5ef08dbf2c2760b"
    ),
}


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)
    statuses: dict[str, bool] = field(default_factory=dict, repr=False)

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> None:
        self.register(check_id)
        status = bool(passed)
        self.statuses[check_id] = status
        self.exact.append(
            {"id": check_id, "passed": status, "statement": statement}
        )

    def check_numerical(
        self,
        check_id: str,
        error: mp.mpf,
        tolerance: mp.mpf,
        error_kind: str,
        statement: str,
        details: dict[str, Any],
    ) -> None:
        self.register(check_id)
        status = bool(error <= tolerance)
        self.statuses[check_id] = status
        self.numerical.append(
            {
                "id": check_id,
                "passed": status,
                "statement": statement,
                "error_kind": error_kind,
                "error": mp_string(error, 30),
                "tolerance": mp_string(tolerance, 12),
                **details,
            }
        )

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

    def passed(self, check_id: str) -> bool:
        if check_id not in self.statuses:
            raise AssertionError(f"unknown scientific check id: {check_id}")
        return self.statuses[check_id]

    def failed_ids(self) -> list[str]:
        return sorted(
            check_id
            for check_id, status in self.statuses.items()
            if not status
        )


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


def mp_string(value: mp.mpf, digits: int = 60) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


def expected_fail_closed_outputs() -> dict[str, Any]:
    return {
        "normalized_quantum_endpoint_state_transform": None,
        "exact_quantum_endpoint_state_transform": None,
        "global_quantum_endpoint_state_transform": None,
        "coordinate_polarization_endpoint_kernel": None,
        "exact_constraint_diagonalization": None,
        "physical_endpoint_state": None,
        "physical_endpoint_measure": None,
        "ghost_endpoint_sector": None,
        "replacement_gauge_fermion": None,
        "full_replacement_bfv_measure": None,
        "replacement_source_discretization": None,
        "old_fixed_a_kernel_equivalence": None,
        "zero_lapse_distribution": None,
        "full_real_lapse_delta_C_kernel": None,
        "global_offshell_canonical_atlas": None,
        "global_maslov_orientation": None,
        "determinant_line_orientation": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def load_frozen_input() -> tuple[dict[str, Any], str, dict[str, str]]:
    input_path = Path(__file__).with_name(INPUT_NAME)
    raw = input_path.read_bytes()
    observed_input_hash = sha256_bytes(raw)
    if observed_input_hash != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            "input hash mismatch: expected "
            f"{EXPECTED_INPUT_SHA256}, observed {observed_input_hash}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-principal-endpoint-fio.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    if payload["resource_caps"] != {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 3,
        "special_function_evaluations": 3,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }:
        raise AssertionError("resource cap mutation")
    if payload["execution_contract"] != {
        "arguments": "NONE",
        "scientific_nonpass": (
            "RECORD_A_VALID_RESULT_AND_SELECT_A_PREDECLARED_TERMINAL_ROW"
        ),
        "integrity_or_schema_failure": "RAISE_WITHOUT_WRITING_A_RESULT",
        "open_dependencies": "NOT_EXECUTION_AUTHORIZATION",
    }:
        raise AssertionError("execution contract mutation")
    if payload["required_fail_closed_outputs"] != (
        expected_fail_closed_outputs()
    ):
        raise AssertionError("fail-closed output mutation")
    if {
        item["path"] for item in payload["repository_sources"]
    } != set(UPSTREAM_HASHES):
        raise AssertionError("declared repository source set mutation")

    observed_upstream: dict[str, str] = {}
    root = repository_root()
    for relpath, expected_hash in UPSTREAM_HASHES.items():
        observed_hash = sha256_bytes((root / relpath).read_bytes())
        if observed_hash != expected_hash:
            raise AssertionError(
                f"upstream hash mismatch for {relpath}: expected "
                f"{expected_hash}, observed {observed_hash}"
            )
        observed_upstream[relpath] = observed_hash
    return payload, observed_input_hash, observed_upstream


def exact_calculation(audit: Audit) -> dict[str, Any]:
    c, trace_p, scalar_p = sp.symbols("c P p", real=True)
    scalar_p_positive = sp.symbols("p_pos", positive=True, real=True)
    hbar = sp.symbols("hbar", positive=True, real=True)
    d_symbol = sp.symbols("D", positive=True, real=True)
    t_symbol, q_symbol = sp.symbols("T Q", real=True)
    phi_shift = sp.symbols("DeltaPhi", real=True)
    w_symbol = sp.Function("W")(c, trace_p, scalar_p)
    amplitude = sp.Function("A")(c, trace_p, scalar_p)
    phase = -w_symbol
    substitutions = {
        sp.diff(w_symbol, c): t_symbol,
        sp.diff(w_symbol, trace_p): -q_symbol,
        sp.diff(w_symbol, scalar_p): phi_shift,
        sp.diff(w_symbol, c, trace_p): 1 / d_symbol,
    }

    phase_relations = (
        sp.diff(phase, c).xreplace(substitutions),
        sp.diff(phase, trace_p).xreplace(substitutions),
    )
    audit.check_exact(
        "G1.fio.canonical_phase_sign",
        phase_relations == (-t_symbol, q_symbol),
        "S=-W has S_c=-T and S_P=Q, fixing exp(-iW/hbar) in the declared momentum convention",
    )

    kernel_without_normalization = amplitude * sp.exp(-sp.I * w_symbol / hbar)
    new_t_action = sp.expand(
        sp.I
        * hbar
        * sp.diff(kernel_without_normalization, c)
        / sp.exp(-sp.I * w_symbol / hbar)
    ).xreplace(substitutions)
    old_q_by_parts = sp.expand(
        -sp.I
        * hbar
        * sp.diff(kernel_without_normalization, trace_p)
        / sp.exp(-sp.I * w_symbol / hbar)
    ).xreplace(substitutions)
    audit.check_exact(
        "G1.fio.principal_operator_relations",
        sp.simplify(new_t_action.subs(hbar, 0) - amplitude * t_symbol)
        == 0
        and sp.simplify(
            old_q_by_parts.subs(hbar, 0) - amplitude * q_symbol
        )
        == 0,
        "i*hbar*d_c and integration by parts against i*hbar*d_P recover T and Q at principal order; amplitude derivatives are subprincipal",
    )

    mixed_hessian = sp.diff(phase, c, trace_p).xreplace(substitutions)
    principal_amplitude = sp.sqrt(1 / d_symbol)
    audit.check_exact(
        "G1.fio.positive_twist_and_half_density",
        mixed_hessian == -1 / d_symbol
        and sp.simplify(principal_amplitude**2 - 1 / d_symbol) == 0,
        "|S_cP|=W_cP=1/D>0 and the Lebesgue principal half-density is D^(-1/2)",
    )
    audit.check_exact(
        "G1.fio.local_maslov_branch",
        sp.sign(1 / d_symbol) == 1,
        "the twist Hessian has fixed positive magnitude on U_plus, so no local mixed-projection caustic changes the compact-interior Maslov branch",
    )

    endpoint_t, endpoint_q = sp.symbols("T_endpoint Q_endpoint", real=True)
    endpoint_phi_shift = sp.symbols("Phi_minus_phi", real=True)
    endpoint_w, endpoint_p = sp.symbols("W_endpoint p_endpoint", real=True)
    boundary = sp.symbols("B", real=True)
    psi_critical = (
        c * endpoint_t
        + endpoint_p * endpoint_phi_shift
        - trace_p * endpoint_q
        - endpoint_w
    )
    boundary_expression = (
        trace_p * endpoint_q
        + endpoint_w
        - c * endpoint_t
        - endpoint_p * endpoint_phi_shift
    )
    audit.check_exact(
        "G1.fio.endpoint_phase_critical_value",
        sp.expand(psi_critical + boundary_expression) == 0
        and sp.expand(boundary_expression - boundary).subs(
            boundary, boundary_expression
        )
        == 0,
        "Psi=c*T+p*(Phi-phi)-P*Q-W has the Darboux critical equations and critical value -B",
    )

    shell_p, shell_P = sp.symbols("p P", positive=True, real=True)
    shell_r = 3 * shell_p**2 - 2 * shell_P**2
    shell_q = sp.log(shell_r / (72 * sp.pi**4)) / 2
    alpha = sp.sqrt(sp.Rational(3, 2))
    beta = sp.sqrt(sp.Rational(2, 3))
    shell_w = (
        -shell_P * shell_q
        + shell_P
        - alpha * shell_p * sp.atanh(beta * shell_P / shell_p)
    )
    shell_shift = -alpha * sp.atanh(beta * shell_P / shell_p)
    audit.check_exact(
        "G1.fio.shell_generator_lineage",
        sp.simplify(sp.diff(shell_w, shell_P) + shell_q) == 0
        and sp.simplify(sp.diff(shell_w, shell_p) - shell_shift) == 0,
        "the explicit c=0 W0 recovers W0_P=-Q0 and W0_p=Phi_star-phi",
    )

    scale_factor = sp.symbols("A", positive=True, real=True)
    root_polynomial = (
        72 * sp.pi**4 * scale_factor**4
        + 12 * sp.pi**2 * c * scale_factor**3
        - 3 * scalar_p_positive**2
        + 2 * trace_p**2
    )
    root_derivative = sp.diff(root_polynomial, scale_factor)
    d_on_root = sp.Rational(3, 2) * c + 12 * sp.pi**2 * scale_factor
    a_pp_at_zero = -sp.diff(root_polynomial, trace_p, 2) / root_derivative
    a_pp_expected = -1 / (
        6 * sp.pi**2 * scale_factor**2 * d_on_root
    )
    m_pp = sp.simplify(-12 * sp.pi**2 * a_pp_expected / d_on_root**2)
    audit.check_exact(
        "G1.fio.coarea_local_curvature",
        sp.simplify(
            root_derivative
            - 24 * sp.pi**2 * scale_factor**2 * d_on_root
        )
        == 0
        and sp.simplify(a_pp_at_zero - a_pp_expected) == 0
        and sp.simplify(
            m_pp - 2 / (scale_factor**2 * d_on_root**3)
        )
        == 0,
        "at P_bar=0, M_P=0 and M_PP=2/(A^2*D^3)>0 for M=W_cP=1/D",
    )

    delta_p, m_zero, m_two = sp.symbols(
        "deltaP M0 M2", positive=True, real=True
    )
    m_geom_series = m_zero + m_two * delta_p**2 / 8
    m_sec_series = m_zero + m_two * delta_p**2 / 24
    ratio_series = sp.series(
        m_geom_series / m_sec_series, delta_p, 0, 4
    ).removeO()
    expected_ratio_series = 1 + m_two * delta_p**2 / (12 * m_zero)
    audit.check_exact(
        "G1.fio.coarea_geometric_vs_secant_series",
        sp.simplify(ratio_series - expected_ratio_series) == 0,
        "the one-term composition density has M_geom/M_sec=1+(M_PP/M)*deltaP^2/12+O(deltaP^4)",
    )

    shell_a0 = (scalar_p_positive**2 / (24 * sp.pi**4)) ** sp.Rational(
        1, 4
    )
    shell_d0 = 12 * sp.pi**2 * shell_a0
    shell_defect_coefficient = sp.simplify(
        1 / (6 * shell_a0**2 * shell_d0**2)
    )
    audit.check_exact(
        "G1.fio.shell_exact_unitarity_nonpass_coefficient",
        sp.simplify(
            shell_defect_coefficient - 1 / (36 * scalar_p_positive**2)
        )
        == 0,
        "at c=0 the exact-one-term coarea ratio begins 1+deltaP^2/(36*p^2), so it is not identically one",
    )

    shell_m_shape = shell_r ** (-sp.Rational(1, 4))
    shell_m_derivative = sp.factor(sp.diff(shell_m_shape, shell_P))
    expected_derivative = shell_P * shell_r ** (-sp.Rational(5, 4))
    audit.check_exact(
        "G1.fio.shell_strict_monotonicity",
        sp.simplify(shell_m_derivative - expected_derivative) == 0,
        "at c=0, M is proportional to R^(-1/4) and is strictly increasing for 0<P<sqrt(3/2)*p",
    )

    audit.guard(
        "G1.fio.guard.principal_microlocal_scope",
        "nondegenerate phase and principal FIO composition calculus",
        "smooth compact cutoffs strictly inside U_plus and its chart image",
        "the phase and half-density define a principal-order microlocally unitary FIO; no global operator norm or endpoint-boundary theorem is inferred",
    )
    audit.guard(
        "G1.fio.guard.exact_coarea_nonpass",
        "strict endpoint-versus-integral-mean inequality for a continuous increasing function",
        "c=0, p>0 and symmetric endpoints P_plus=x, P_minus=-x with 0<x<sqrt(3/2)*p",
        "M_geom=M(x) is strictly larger than M_sec=x^(-1)*integral_0^x M(u)du, so the uncorrected one-term kernel fails exact coarea delta normalization",
    )
    audit.guard(
        "G1.fio.guard.exact_transform_boundary",
        "principal symbol versus full-symbol quantization",
        "the single amplitude D^(-1/2) with no hbar-dependent corrections",
        "the nonpass kills exact unitarity only for this one-term kernel; a corrected symbol or independently defined spectral transform is not excluded",
    )
    audit.guard(
        "G1.fio.guard.polarization_boundary",
        "momentum-polarization canonical graph",
        "old (P,p) to new (c,p) with a spectator delta in p",
        "no fixed-(Q,phi) to fixed-(T,Phi) coordinate kernel, physical endpoint measure or normalizable c=0 state is constructed",
    )
    audit.guard(
        "G1.fio.guard.bfv_boundary",
        "bosonic FIO versus extended BFV phase space",
        "no multiplier momentum, ghosts, antighosts, BRST charge, gauge fermion or fermionic endpoint term",
        "the principal FIO does not supply the replacement BFV source or determinant-line orientation",
    )
    audit.guard(
        "G1.fio.guard.delta_c_boundary",
        "endpoint momentum representation versus group-averaged constraint distribution",
        "c labels the new momentum coordinate; no full-real-lapse integration or spectral measure is performed",
        "this c representation is not the Marolf delta(C) rigging map and delta(C) is not called a bounded projector on continuous zero spectrum",
    )

    return {
        "canonical_graph": {
            "phase": "S=-W(c,P,p)",
            "relations": ["T=W_c", "Q=-W_P", "Phi-phi=W_p"],
            "mixed_hessian": "S_cP=-1/D",
            "twist_magnitude": "1/D>0",
            "principal_half_density": "D^(-1/2)",
            "kernel": (
                "delta(p-p_prime)*(2*pi*hbar)^(-1/2)*D^(-1/2)"
                "*exp(-i*W/hbar)"
            ),
            "endpoint_phase_critical_value": "-B",
        },
        "shell_lineage": {
            "c": 0,
            "Q0": "log((3*p^2-2*P^2)/(72*pi^4))/2",
            "W0": (
                "-P*Q0+P-sqrt(3/2)*p*atanh(sqrt(2/3)*P/p)"
            ),
            "W0_P": "-Q0",
            "W0_p": "Phi_star-phi",
        },
        "exact_one_term_discriminator": {
            "M": "W_cP=1/D",
            "required_coarea_density": (
                "M_sec=(T(P_plus)-T(P_minus))/(P_plus-P_minus)"
            ),
            "one_term_density": (
                "M_geom=sqrt(M(P_plus)*M(P_minus))"
            ),
            "local_ratio": (
                "1+deltaP^2/(6*A0^2*D0^2)+O(deltaP^4)"
            ),
            "c_zero_ratio": "1+deltaP^2/(36*p^2)+O(deltaP^4)",
            "finite_shell_inequality": "M_geom>M_sec for symmetric nonzero endpoints",
            "conclusion": "EXACT_UNITARITY_NONPASS_FOR_UNCORRECTED_ONE_TERM_KERNEL",
        },
    }


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    scalar_p = mp.mpf(plan["p"])
    x_values = [mp.mpf(value) for value in plan["x_values"]]
    small_deltas = [mp.mpf(value) for value in plan["small_delta_values"]]
    absolute_tolerance = mp.mpf(plan["absolute_tolerance"])
    coefficient_tolerance = mp.mpf(plan["series_coefficient_tolerance"])
    if (
        scalar_p != 1
        or x_values
        != [mp.mpf("0.0125"), mp.mpf("0.025"), mp.mpf("0.05")]
        or small_deltas
        != [mp.mpf("0.1"), mp.mpf("0.05"), mp.mpf("0.025")]
    ):
        raise AssertionError("numerical benchmark mutation")
    if [2 * x for x in reversed(x_values)] != small_deltas:
        raise AssertionError("series and finite-ratio samples are not paired")

    def shell_shape(momentum: mp.mpf) -> mp.mpf:
        return (3 * scalar_p**2 - 2 * momentum**2) ** (-mp.mpf("0.25"))

    records: list[dict[str, Any]] = []
    agreement_errors: list[mp.mpf] = []
    ratio_margins: list[mp.mpf] = []
    coefficient_errors: list[mp.mpf] = []
    target_coefficient = mp.mpf(1) / (36 * scalar_p**2)
    for x in x_values:
        direct_mean = mp.quad(shell_shape, [0, x]) / x
        z = 2 * x**2 / (3 * scalar_p**2)
        hypergeometric_mean = (3 * scalar_p**2) ** (-mp.mpf("0.25")) * (
            mp.hyp2f1(mp.mpf("0.5"), mp.mpf("0.25"), mp.mpf("1.5"), z)
        )
        endpoint_value = shell_shape(x)
        ratio = endpoint_value / direct_mean
        delta_p = 2 * x
        coefficient_estimate = (ratio - 1) / delta_p**2
        agreement = abs(direct_mean - hypergeometric_mean)
        agreement_errors.append(agreement)
        ratio_margins.append(ratio - 1)
        coefficient_errors.append(abs(coefficient_estimate - target_coefficient))
        records.append(
            {
                "x": mp_string(x),
                "deltaP": mp_string(delta_p),
                "direct_secant_mean": mp_string(direct_mean),
                "hypergeometric_secant_mean": mp_string(
                    hypergeometric_mean
                ),
                "endpoint_geometric_mean": mp_string(endpoint_value),
                "M_geom_over_M_sec": mp_string(ratio),
                "series_coefficient_estimate": mp_string(
                    coefficient_estimate
                ),
            }
        )

    audit.check_numerical(
        "G1.fio.numerical.quadrature_hypergeometric_agreement",
        max(agreement_errors),
        absolute_tolerance,
        "absolute",
        "direct high-precision quadrature and the closed hypergeometric secant mean agree",
        {"maximum_error": mp_string(max(agreement_errors))},
    )
    audit.check_numerical(
        "G1.fio.numerical.finite_coarea_ratio_nonpass",
        mp.mpf("0") if min(ratio_margins) > 0 else -min(ratio_margins),
        mp.mpf("0"),
        "strict_positive_margin_failure",
        "M_geom/M_sec is strictly greater than one at every frozen nonzero symmetric shell pair",
        {"minimum_ratio_minus_one": mp_string(min(ratio_margins))},
    )
    audit.check_numerical(
        "G1.fio.numerical.local_series_coefficient",
        max(coefficient_errors),
        coefficient_tolerance,
        "absolute",
        "the frozen finite ratios approach the exact coefficient 1/(36*p^2)",
        {
            "target_coefficient": mp_string(target_coefficient),
            "maximum_error": mp_string(max(coefficient_errors)),
            "samples": records,
        },
    )
    return {
        "precision_digits": mp.mp.dps,
        "p": mp_string(scalar_p),
        "methods": [
            "mpmath arbitrary-precision quadrature",
            "Gauss hypergeometric closed antiderivative",
        ],
        "samples": records,
        "quadratures": 3,
        "special_function_evaluations": 3,
        "root_calls": 0,
        "ode_calls": 0,
    }


def decision_from_flags(
    principal_pass: bool, coarea_nonpass: bool, numerical_pass: bool
) -> tuple[str, str]:
    if not principal_pass:
        return (
            "KILL_PROPOSED_V0_PRINCIPAL_ENDPOINT_FIO",
            "RETAIN_CLASSICAL_DARBOUX_CHART_ONLY",
        )
    if not coarea_nonpass:
        return (
            "KEEP_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO_EXACT_UNITARITY_INCONCLUSIVE",
            "CLOSE_PRINCIPAL_LOCAL_FIO_ONLY_LEAVE_ONE_TERM_EXACT_NORMALIZATION_OPEN",
        )
    if not numerical_pass:
        return (
            "INCONCLUSIVE",
            "NO_PROMOTION_PENDING_INDEPENDENT_CONTROL",
        )
    return (
        "KEEP_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO_KILL_ONE_TERM_EXACT_UNITARITY",
        "CLOSE_PRINCIPAL_LOCAL_FIO_ONLY_REQUIRE_SUBPRINCIPAL_SYMBOL_AND_DOMAIN_BEFORE_ANY_EXACT_OR_BFV_LIFT",
    )


def select_decision(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    principal_ids = {
        "G1.fio.canonical_phase_sign",
        "G1.fio.principal_operator_relations",
        "G1.fio.positive_twist_and_half_density",
        "G1.fio.local_maslov_branch",
        "G1.fio.endpoint_phase_critical_value",
        "G1.fio.shell_generator_lineage",
    }
    coarea_ids = {
        "G1.fio.coarea_local_curvature",
        "G1.fio.coarea_geometric_vs_secant_series",
        "G1.fio.shell_exact_unitarity_nonpass_coefficient",
        "G1.fio.shell_strict_monotonicity",
    }
    numerical_ids = {
        "G1.fio.numerical.quadrature_hypergeometric_agreement",
        "G1.fio.numerical.finite_coarea_ratio_nonpass",
        "G1.fio.numerical.local_series_coefficient",
    }
    observed_ids = {
        item["id"] for item in audit.exact + audit.numerical
    }
    declared_ids = principal_ids | coarea_ids | numerical_ids
    if observed_ids != declared_ids:
        raise AssertionError(
            "decision check partition mutation: missing="
            f"{sorted(declared_ids - observed_ids)}, unexpected="
            f"{sorted(observed_ids - declared_ids)}"
        )
    principal_pass = all(audit.passed(item) for item in principal_ids)
    coarea_nonpass = all(audit.passed(item) for item in coarea_ids)
    numerical_pass = all(audit.passed(item) for item in numerical_ids)
    verdict, impact = decision_from_flags(
        principal_pass, coarea_nonpass, numerical_pass
    )
    declared_rows = {
        (row["verdict"], row["programme_impact"])
        for row in frozen_input["decision_table"]
    }
    reachable_rows = {
        decision_from_flags(True, True, True),
        decision_from_flags(False, True, True),
        decision_from_flags(True, False, True),
        decision_from_flags(True, True, False),
    }
    if declared_rows != reachable_rows:
        raise AssertionError("frozen decision rows are not exactly reachable")
    if (verdict, impact) not in declared_rows:
        raise AssertionError("selected decision is not frozen")
    return {
        "verdict": verdict,
        "programme_impact": impact,
        "principal_pass": principal_pass,
        "coarea_nonpass": coarea_nonpass,
        "numerical_pass": numerical_pass,
        "all_scientific_pass": (
            principal_pass and coarea_nonpass and numerical_pass
        ),
        "failed_scientific_ids": audit.failed_ids(),
        "reachable_frozen_rows": [
            {"verdict": row[0], "programme_impact": row[1]}
            for row in sorted(reachable_rows)
        ],
    }


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream_provenance: dict[str, str],
) -> dict[str, Any]:
    audit = Audit()
    exact = exact_calculation(audit)
    numerical = numerical_calculation(frozen_input, audit)
    decision = select_decision(frozen_input, audit)
    kept = decision["verdict"] == (
        "KEEP_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO_KILL_ONE_TERM_EXACT_UNITARITY"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": (
            "GATE1_V0_LOCAL_PRINCIPAL_ENDPOINT_FIO_KEPT_"
            "UNCORRECTED_ONE_TERM_EXACT_UNITARITY_KILLED"
            if kept
            else "GATE1_V0_PRINCIPAL_ENDPOINT_FIO_NONPROMOTED"
        ),
        "verdict": decision["verdict"],
        "programme_impact": decision["programme_impact"],
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_provenance": [
            {"path": path, "sha256": digest}
            for path, digest in sorted(upstream_provenance.items())
        ],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": audit.numerical,
        "decision_trace": {
            "meaning": (
                "keep the compact-interior principal momentum FIO and its "
                "fixed local Maslov branch; reject exact finite-hbar "
                "unitarity only for the uncorrected one-term Van Vleck "
                "kernel; retain full-symbol, domain, BFV and delta(C) work "
                "as open without automatic execution authority"
            ),
            "check_partitions": decision,
            "source_boundary": (
                "HTV frames endpoint canonical data; Garcia-Vergara-Urrutia "
                "frames omitted BFV boundary data; Van Vleck and Hormander "
                "frame principal semiclassical/FIO scope; Marolf frames the "
                "distinct full-real-lapse delta(C) rigging distribution. None "
                "derives this repository-specific kernel or licenses a "
                "global normalized physical endpoint state."
            ),
        },
        "scope_status": {
            "local_v0_principal_momentum_endpoint_fio": (
                "KEEP_ON_COMPACT_INTERIORS_OF_U_PLUS" if kept else None
            ),
            "local_maslov_branch": (
                "FIXED_BY_W_CP_POSITIVE_ON_U_PLUS" if kept else None
            ),
            "uncorrected_one_term_exact_unitarity": (
                "KILL_BY_EXACT_COAREA_NONPASS" if kept else None
            ),
            "normalized_quantum_endpoint_state_transform": None,
            "exact_quantum_endpoint_state_transform": None,
            "global_quantum_endpoint_state_transform": None,
            "subprincipal_full_symbol": None,
            "operator_ordering": None,
            "self_adjoint_domain": None,
            "physical_endpoint_measure": None,
            "coordinate_polarization_endpoint_kernel": None,
            "ghost_endpoint_sector": None,
            "replacement_gauge_fermion": None,
            "full_replacement_bfv_measure": None,
            "replacement_source_discretization": None,
            "old_fixed_a_kernel_equivalence": None,
            "zero_lapse_distribution": None,
            "full_real_lapse_delta_C_kernel": None,
            "global_offshell_canonical_atlas": None,
            "global_maslov_orientation": None,
            "determinant_line_orientation": None,
            "physical_original_cycle": None,
        },
        "ragnarok_termination_audit": {
            "scientific_nonpass_policy": "RECORD_VALID_TERMINAL_RESULT",
            "integrity_or_schema_failure_policy": "RAISE_WITHOUT_RESULT",
            "reachable_frozen_rows": decision["reachable_frozen_rows"],
            "arbitrary_arguments": "REJECTED",
            "open_dependencies": "NOT_EXECUTION_AUTHORIZATION",
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "open_dependencies": {
            "execution_authorization": "NONE",
            "automatic_successor": None,
            "status": "NOT_EXECUTION_AUTHORIZATION",
            "items": [
                "a subprincipal/full hbar-dependent symbol and its ordering",
                "self-adjoint domains, spectral measure and R=0/p=0 edge conditions",
                "a global normalized endpoint transform and global Maslov data",
                "ghost endpoints, BRST charge, gauge fermion and replacement BFV source",
                "old fixed-a kernel comparison, zero lapse and the full-real-lapse delta(C) rigging map",
                "other components, global atlas, determinant orientation and physical original cycle",
            ],
        },
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": expected_fail_closed_outputs(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": numerical["quadratures"],
            "special_function_evaluations": numerical[
                "special_function_evaluations"
            ],
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
            "scientific_nonpass_count": len(audit.failed_ids()),
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
            "computed_scope": frozen_input["computed_scope"],
            "not_computed": frozen_input["not_computed"],
            "execution_contract": frozen_input["execution_contract"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> int:
    if len(sys.argv) != 1:
        raise SystemExit("this frozen calculation accepts no arguments")
    frozen_input, input_sha256, upstream = load_frozen_input()
    result = build_result(frozen_input, input_sha256, upstream)
    rendered = (
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")
    if len(rendered) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result size {len(rendered)} exceeds cap {ARTIFACT_CAP_BYTES}"
        )
    result_path = Path(__file__).with_name(RESULT_NAME)
    temporary_path = result_path.with_suffix(result_path.suffix + ".tmp")
    temporary_path.write_bytes(rendered)
    temporary_path.replace(result_path)
    print(RESULT_PREFIX + json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
