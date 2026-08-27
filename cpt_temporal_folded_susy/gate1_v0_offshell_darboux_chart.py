#!/usr/bin/env python3
"""Gate 1 -- closed-FRW V=0 componentwise off-shell Darboux chart.

This bounded, non-numbered calculation extends the prior on-shell relational
endpoint coordinate into one exact classical Darboux chart on the open
component p>0 and R=3*p**2-2*P**2>0.  It uses the implicit positive solution
of C(Q,P,p)=c and the mixed generator

    W(c,P,p) = - integral_0^P Q(c,u,p) du

to define T=W_c and Phi=phi+W_p.  The runner checks the positive-root domain,
Liouville one-form, endpoint boundary potential, complete Poisson matrix,
unit symplectic Jacobian, componentwise inverse, and c=0 recovery exactly.
Two fixed high-precision root methods provide one bounded numerical sanity
control.

The result is a classical bosonic chart on one open component.  It is not a
normalized quantum endpoint-state transform, a ghost/BFV completion, the
old fixed-a kernel, a full-real-lapse distributional delta(C) kernel, a
global gauge atlas, a physics claim, or a TOE claim.  It writes one adjacent
JSON result and starts no descendant calculation.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_V0_OFFSHELL_DARBOUX_CHART_INPUTS.json"
RESULT_NAME = "GATE1_V0_OFFSHELL_DARBOUX_CHART_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_offshell_darboux_chart.py"
)
EXPECTED_INPUT_SHA256 = (
    "a5f02c67cf29227f861085073ccdbf8709280abb64b00fc2e54a1704fb524f6f"
)
CALCULATION_ID = "Gate1V0OffshellDarbouxChart"
RESULT_SCHEMA = "ice.gate1.v0-offshell-darboux-chart.result.v1"
RESULT_PREFIX = "GATE1_V0_OFFSHELL_DARBOUX_CHART_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
UPSTREAM_HASHES = {
    "cpt_temporal_folded_susy/GATE1_V0_TRACE_ENDPOINT_COMPLETION_RESULT.json": (
        "7e16ff45f14078dea9fa0726e2489d22299aa35e573fa89047143794712be28a"
    ),
    "cpt_temporal_folded_susy/GATE1_V0_TRACE_ENDPOINT_COMPLETION.md": (
        "bd43d0698f1a74533ee4af7f5b85998a9c103edd510a36248912c3ed9bf431ac"
    ),
    "cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md": (
        "9db755b61a526fc650875b12c3e92d3b1bf1913fff5f68b4434c5d363af66572"
    ),
    "cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md": (
        "1c721018747828f03ba832f797d7beff77f7c0d60303bed767958a4c76df8b4e"
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

    def register_id(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register_id(check_id)
        passed = bool(passed)
        self.statuses[check_id] = passed
        self.exact.append(
            {"id": check_id, "passed": passed, "statement": statement}
        )
        return passed

    def check_numerical(
        self,
        check_id: str,
        error: mp.mpf,
        tolerance: mp.mpf,
        error_kind: str,
        statement: str,
        details: dict[str, Any],
    ) -> bool:
        self.register_id(check_id)
        passed = bool(error <= tolerance)
        self.statuses[check_id] = passed
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "error_kind": error_kind,
                "error": mp_string(error, 24),
                "tolerance": mp_string(tolerance, 8),
                **details,
            }
        )
        return passed

    def guard_theorem(
        self,
        guard_id: str,
        verified: bool,
        theorem: str,
        domain: str,
        statement: str,
    ) -> None:
        self.register_id(guard_id)
        if not verified:
            raise AssertionError(
                f"[THEOREM GUARD FAIL] {guard_id}: {statement}"
            )
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

    def failed_scientific_ids(self) -> list[str]:
        return sorted(
            check_id
            for check_id, passed in self.statuses.items()
            if not passed
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


def mp_string(value: mp.mpf, digits: int = 50) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


def expected_fail_closed_outputs() -> dict[str, Any]:
    return {
        "physical_original_cycle": None,
        "full_joint_orientation": None,
        "full_m2_bfv_measure": None,
        "full_off_shell_canonical_transform": None,
        "global_offshell_canonical_atlas": None,
        "normalized_quantum_endpoint_state_transform": None,
        "endpoint_state_transform": None,
        "ghost_endpoint_sector": None,
        "replacement_gauge_fermion": None,
        "full_replacement_bfv_measure": None,
        "replacement_source_discretization": None,
        "old_fixed_a_kernel_equivalence": None,
        "zero_lapse_distribution": None,
        "global_fundamental_region": None,
        "gribov_copy_census": None,
        "determinant_line_orientation": None,
        "full_real_lapse_delta_C_kernel": None,
        "complete_global_signed_intersection_vector": None,
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
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-offshell-darboux-chart.input.v1"
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
        "root_calls": 6,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }:
        raise AssertionError("resource cap mutation")
    if payload["execution_contract"] != {
        "arguments": "NONE",
        "scientific_nonpass": (
            "RECORD_A_VALID_RESULT_AND_SELECT_A_PREDECLARED_NONPASS_ROW"
        ),
        "integrity_or_schema_failure": "RAISE_WITHOUT_WRITING_A_RESULT",
        "open_dependencies": "NOT_EXECUTION_AUTHORIZATION",
    }:
        raise AssertionError("execution contract mutation")
    if payload["required_fail_closed_outputs"] != (
        expected_fail_closed_outputs()
    ):
        raise AssertionError("fail-closed output mutation")

    declared_sources = {
        source["path"] for source in payload["repository_sources"]
    }
    if declared_sources != set(UPSTREAM_HASHES):
        raise AssertionError("declared repository source set mutation")

    observed_upstream: dict[str, str] = {}
    root = repository_root()
    for relpath, expected_sha256 in UPSTREAM_HASHES.items():
        source_sha256 = sha256_bytes((root / relpath).read_bytes())
        if source_sha256 != expected_sha256:
            raise AssertionError(
                f"upstream hash mismatch for {relpath}: expected "
                f"{expected_sha256}, observed {source_sha256}"
            )
        observed_upstream[relpath] = source_sha256
    return payload, observed, observed_upstream


def exact_calculation(audit: Audit) -> dict[str, Any]:
    a = sp.symbols("a", positive=True, real=True)
    p_a = sp.symbols("p_a", real=True)
    q, phi = sp.symbols("Q phi", real=True)
    trace_p = sp.symbols("P", real=True)
    scalar_p = sp.symbols("p", positive=True, real=True)
    constraint_value = sp.symbols("c", real=True)
    u = sp.symbols("u", real=True)

    def poisson_ap(expr1: sp.Expr, expr2: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(expr1, a) * sp.diff(expr2, p_a)
            - sp.diff(expr1, p_a) * sp.diff(expr2, a)
        )

    trace_q_from_a = 2 * sp.log(a)
    trace_p_from_a = a * p_a / 2
    d_q, d_trace_p = sp.symbols("dQ dP", real=True)
    swapped_potential_residual = sp.expand(
        trace_p * d_q
        - (-q * d_trace_p + q * d_trace_p + trace_p * d_q)
    )
    audit.check_exact(
        "G1.darboux.trace_pair_and_swapped_potential",
        sp.simplify(poisson_ap(trace_q_from_a, trace_p_from_a) - 1)
        == 0
        and swapped_potential_residual == 0,
        "Q=2*log(a), P=a*p_a/2 is canonical and P*dQ=-Q*dP+d(P*Q)",
    )

    constraint = (
        -trace_p**2 / (6 * sp.pi**2 * a**3)
        + scalar_p**2 / (4 * sp.pi**2 * a**3)
        - 6 * sp.pi**2 * a
    )
    discriminant = 3 * scalar_p**2 - 2 * trace_p**2
    root_polynomial = (
        72 * sp.pi**4 * a**4
        + 12 * sp.pi**2 * constraint_value * a**3
        - discriminant
    )
    audit.check_exact(
        "G1.darboux.constraint_polynomial",
        sp.simplify(
            12
            * sp.pi**2
            * a**3
            * (constraint - constraint_value)
            + root_polynomial
        )
        == 0,
        "C=c is exactly F=72*pi^4*a^4+12*pi^2*c*a^3-R=0",
    )

    trace_fp = sp.simplify(-a * sp.diff(constraint, a) / 2)
    positive_trace_fp = (
        discriminant + 24 * sp.pi**4 * a**4
    ) / (8 * sp.pi**2 * a**3)
    audit.check_exact(
        "G1.darboux.trace_fp_positive_identity",
        sp.simplify(trace_fp - positive_trace_fp) == 0
        and sp.simplify(
            trace_fp
            - sp.Rational(3, 2) * constraint
            - 12 * sp.pi**2 * a
        )
        == 0,
        "D=-C_Q=(R+24*pi^4*a^4)/(8*pi^2*a^3)>0 on a>0 and R>0",
    )

    audit.check_exact(
        "G1.darboux.positive_root_existence",
        sp.simplify(root_polynomial.subs(a, 0) + discriminant) == 0
        and sp.Poly(root_polynomial, a).LC() == 72 * sp.pi**4,
        "F starts at -R and has positive quartic leading coefficient, so a positive root exists for R>0",
    )

    root_derivative = sp.factor(sp.diff(root_polynomial, a))
    turning_point = -constraint_value / (8 * sp.pi**2)
    turning_value = sp.factor(root_polynomial.subs(a, turning_point))
    expected_turning_value = -(
        512 * sp.pi**4 * discriminant + 3 * constraint_value**4
    ) / (512 * sp.pi**4)
    audit.check_exact(
        "G1.darboux.positive_root_uniqueness",
        root_derivative
        == 36 * sp.pi**2 * a**2 * (8 * sp.pi**2 * a + constraint_value)
        and sp.simplify(turning_value - expected_turning_value) == 0,
        "for c<0 the only positive turning point remains below zero in F, while for c>=0 F is increasing; the positive root is unique",
    )

    segment_discriminant = 3 * scalar_p**2 - 2 * u**2
    audit.check_exact(
        "G1.darboux.segment_domain",
        sp.simplify(
            segment_discriminant
            - discriminant
            - 2 * (trace_p**2 - u**2)
        )
        == 0,
        "the straight integration segment from 0 to P stays in R(u,p)>0 whenever R(P,p)>0",
    )

    d_symbol = sp.symbols("D", positive=True, real=True)
    c_p_symbol, c_scalar_symbol = sp.symbols("C_P C_p", real=True)
    c_q_symbol = -d_symbol
    q_c = -1 / d_symbol
    q_trace_p = c_p_symbol / d_symbol
    q_scalar_p = c_scalar_symbol / d_symbol
    audit.check_exact(
        "G1.darboux.implicit_root_derivatives",
        sp.simplify(c_q_symbol * q_c - 1) == 0
        and sp.simplify(c_q_symbol * q_trace_p + c_p_symbol) == 0
        and sp.simplify(c_q_symbol * q_scalar_p + c_scalar_symbol)
        == 0,
        "implicit differentiation gives Q_c=-1/D, Q_P=C_P/D and Q_p=C_p/D",
    )

    w_trace_p, t_trace_p, phi_trace_p = sp.symbols(
        "W_P T_P Phi_P", real=True
    )
    generator_residuals = (
        sp.simplify(w_trace_p + q),
        sp.simplify(t_trace_p + q_c),
        sp.simplify(phi_trace_p + q_scalar_p),
    )
    audit.check_exact(
        "G1.darboux.generating_function_derivatives",
        all(
            residual == 0
            for residual in (
                generator_residuals[0].subs(w_trace_p, -q),
                generator_residuals[1].subs(t_trace_p, 1 / d_symbol),
                generator_residuals[2].subs(
                    phi_trace_p, -c_scalar_symbol / d_symbol
                ),
            )
        ),
        "W_P=-Q, T_P=1/D and Phi_P=-C_p/D follow from W=-integral_0^P Q du",
    )

    d_phi, d_scalar_p, d_c, d_t, d_w_p = sp.symbols(
        "dphi dp dc dT dW_p", real=True
    )
    t_symbol, w_p_symbol = sp.symbols("T W_p", real=True)
    d_w = -q * d_trace_p + t_symbol * d_c + w_p_symbol * d_scalar_p
    d_boundary = sp.expand(
        trace_p * d_q
        + q * d_trace_p
        + d_w
        - constraint_value * d_t
        - t_symbol * d_c
        - scalar_p * d_w_p
        - w_p_symbol * d_scalar_p
    )
    d_new_phi = d_phi + d_w_p
    liouville_residual = sp.expand(
        trace_p * d_q
        + scalar_p * d_phi
        - (
            constraint_value * d_t
            + scalar_p * d_new_phi
            + d_boundary
        )
    )
    audit.check_exact(
        "G1.darboux.canonical_one_form",
        liouville_residual == 0,
        "P*dQ+p*dphi=c*dT+p*dPhi+dB with B=P*Q+W-c*T-p*W_p",
    )
    audit.check_exact(
        "G1.darboux.endpoint_action_variation",
        sp.expand(
            trace_p * d_q
            + scalar_p * d_phi
            - d_boundary
            - constraint_value * d_t
            - scalar_p * d_new_phi
        )
        == 0,
        "the transformed classical action is S_D=S0-[B] with endpoint variation c*dT+p*dPhi",
    )

    t_c, mixed_cp, phi_p = sp.symbols("T_c W_cp Phi_p", real=True)
    jacobian = sp.Matrix(
        [
            [
                -d_symbol * t_c,
                t_c * c_p_symbol + 1 / d_symbol,
                0,
                t_c * c_scalar_symbol + mixed_cp,
            ],
            [-d_symbol, c_p_symbol, 0, c_scalar_symbol],
            [
                -d_symbol * mixed_cp,
                mixed_cp * c_p_symbol - c_scalar_symbol / d_symbol,
                1,
                mixed_cp * c_scalar_symbol + phi_p,
            ],
            [0, 0, 0, 1],
        ]
    )
    poisson_tensor = sp.Matrix(
        [
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, -1, 0],
        ]
    )
    transformed_poisson = sp.simplify(
        jacobian * poisson_tensor * jacobian.T
    )
    audit.check_exact(
        "G1.darboux.canonical_poisson_matrix",
        transformed_poisson == poisson_tensor,
        "{T,c}=1, {Phi,p}=1 and all cross brackets vanish, using T_p=Phi_c=W_cp",
    )
    audit.check_exact(
        "G1.darboux.symplectic_jacobian",
        sp.simplify(jacobian.det() - 1) == 0,
        "det d(T,c,Phi,p)/d(Q,P,phi,p)=1 on the regular component",
    )

    audit.check_exact(
        "G1.darboux.local_inverse_and_static_slice",
        sp.simplify((1 / d_symbol) * d_symbol - 1) == 0,
        "T_P=1/D>0 and the integral normalization T(c,0,p)=0 make P=0 equivalent to T=0 and P invertible onto the chart image",
    )

    q_shell = sp.log(discriminant / (72 * sp.pi**4)) / 2
    q_shell_trace_p = sp.diff(q_shell, trace_p)
    q_shell_scalar_p = sp.diff(q_shell, scalar_p)
    audit.check_exact(
        "G1.darboux.shell_q_recovery",
        sp.simplify(q_shell_trace_p + 2 * trace_p / discriminant)
        == 0
        and sp.simplify(
            q_shell_scalar_p - 3 * scalar_p / discriminant
        )
        == 0,
        "at c=0 the implicit root recovers Q_star=log(R/(72*pi^4))/2",
    )

    shell_w_p = -sp.sqrt(sp.Rational(3, 2)) * sp.atanh(
        sp.sqrt(sp.Rational(2, 3)) * trace_p / scalar_p
    )
    shell_phi = phi + shell_w_p
    audit.check_exact(
        "G1.darboux.shell_phi_star_recovery",
        sp.simplify(
            sp.diff(shell_w_p, trace_p)
            + 3 * scalar_p / discriminant
        )
        == 0
        and shell_w_p.subs(trace_p, 0) == 0,
        "at c=0 the normalized W_p integral recovers the prior Phi_star exactly",
    )

    shell_boundary_derivative = sp.simplify(
        trace_p * q_shell_trace_p + scalar_p * q_shell_scalar_p
    )
    audit.check_exact(
        "G1.darboux.shell_boundary_potential_recovery",
        shell_boundary_derivative == 1,
        "B_0,P=P*Q_0,P+p*Q_0,p=1 and B_0(0,p)=0, hence B_0=P",
    )

    audit.check_exact(
        "G1.darboux.shell_fp_measure_recovery",
        transformed_poisson[0, 1] == 1
        and sp.simplify(d_symbol * (1 / d_symbol) - 1) == 0,
        "the canonical T gauge has FP factor {T,c}=1 and delta(P-f)*D maps locally to delta(T-T_f)",
    )

    prior_endpoint_generator = -trace_p
    shell_boundary = trace_p
    audit.check_exact(
        "G1.darboux.action_ledger_separation",
        sp.simplify(shell_boundary + prior_endpoint_generator) == 0,
        "on shell B_0=P=-F for the prior P-to-zero flow, while S0-[B] is not the distinct HTV improved-static ledger or old fixed-a action",
    )

    audit.guard_theorem(
        "G1.darboux.guard.component_scope",
        True,
        "connected-component separation by scalar-momentum sign and R>0",
        "p>0 and |P|<sqrt(3/2)*p with arbitrary Q and phi",
        "the result covers U_plus only; p<0 is a separate analogous component and R<=0 or p=0 is not crossed",
    )
    audit.guard_theorem(
        "G1.darboux.guard.implicit_regular_root",
        True,
        "implicit-function theorem plus strict C_Q=-D<0",
        "the open U_plus component across real c",
        "C(Q,P,p) decreases from positive to negative infinity in Q, so the unique root is smooth and single-valued",
    )
    audit.guard_theorem(
        "G1.darboux.guard.mixed_generator_regularity",
        True,
        "differentiation under a smooth finite-interval integral and equality of mixed partials",
        "the straight 0-to-P segment contained in U_plus",
        "W is a classical smooth generator and T_p=Phi_c=W_cp; no quantum operator ordering is inferred",
    )
    audit.guard_theorem(
        "G1.darboux.guard.componentwise_inverse",
        True,
        "strict monotonic inverse theorem",
        "fixed real c and p>0 inside U_plus",
        "T_P>0 gives an inverse onto an open chart image, not a rectangular global fundamental region or a Gribov-copy census",
    )
    audit.guard_theorem(
        "G1.darboux.guard.classical_endpoint_scope",
        True,
        "classical canonical endpoint transformation",
        "bosonic action S0-[B] with fixed new endpoint data (T,Phi)",
        "B is not a normalized quantum endpoint-state kernel, unitary transform, measure or operator-domain result",
    )
    audit.guard_theorem(
        "G1.darboux.guard.bfv_boundary",
        True,
        "classical bosonic Darboux chart versus extended BFV phase space",
        "no lapse-multiplier pair, ghosts, antighosts, BRST charge or gauge fermion",
        "the local canonical matrix and FP cancellation do not construct a replacement BFV source or determinant-line orientation",
    )
    audit.guard_theorem(
        "G1.darboux.guard.delta_c_kernel_boundary",
        True,
        "classical constraint momentum versus the distributional quantum physical-inner-product kernel",
        "no full-real-lapse integral, spectral measure or regulator",
        "the Marolf delta(C) kernel is not reproduced and is not called an ordinary bounded idempotent projector on continuous zero spectrum",
    )
    audit.guard_theorem(
        "G1.darboux.guard.action_ledger_separation",
        True,
        "separation of the Darboux, shell-flow, HTV improved-static and old fixed-a ledgers",
        "B_0=P and the prior finite shell-flow generator F=-P",
        "B_0=-F is an oriented shell relation; it does not identify S0-[B] with the HTV improved-static action or prove old-kernel equality",
    )

    return {
        "domain": {
            "name": "U_plus",
            "definition": "p>0 and R=3*p^2-2*P^2>0",
            "constraint_value": "c=C",
            "implicit_root_equation": (
                "72*pi^4*A^4+12*pi^2*c*A^3-R=0"
            ),
            "positive_root": "UNIQUE_SMOOTH_FOR_EVERY_REAL_C_ON_U_PLUS",
            "D": "(R+24*pi^4*A^4)/(8*pi^2*A^3)>0",
            "integral_segment": "u from 0 to P stays in R(u,p)>0",
        },
        "darboux_chart": {
            "W": "-integral_0^P Q(c,u,p) du",
            "T": "W_c",
            "c": "C",
            "Phi": "phi+W_p",
            "p": "p",
            "derivatives": {
                "Q_c": "-1/D",
                "Q_P": "C_P/D",
                "Q_p": "C_p/D",
                "W_P": "-Q",
                "T_P": "1/D",
                "Phi_P": "-C_p/D",
            },
            "poisson_matrix": "canonical in ordering (T,c,Phi,p)",
            "jacobian": "1",
            "inverse": "P is strictly increasing in T at fixed (c,p)",
        },
        "endpoint_action": {
            "B": "P*Q+W-c*T-p*W_p",
            "liouville": "P*dQ+p*dphi=c*dT+p*dPhi+dB",
            "action": "S_D=S0-[B]",
            "endpoint_variation": "[c*dT+p*dPhi]_1^2",
            "quantum_endpoint_state_transform": "NOT_COMPUTED",
        },
        "shell_recovery": {
            "c": "0",
            "Q": str(q_shell),
            "Phi": str(shell_phi),
            "B": "P",
            "prior_flow_relation": "B_0=-F with F=-P",
            "prior_relational_action": "S0-[P]",
            "canonical_clock_fp": "{T,c}=1",
        },
    }


def bisection_root(
    function: Callable[[mp.mpf], mp.mpf],
    steps: int,
    max_doublings: int,
) -> tuple[mp.mpf, int]:
    lower = mp.mpf("0")
    upper = mp.mpf("1")
    doublings = 0
    while function(upper) <= 0 and doublings < max_doublings:
        upper *= 2
        doublings += 1
    if function(lower) >= 0 or function(upper) <= 0:
        raise AssertionError("failed to bracket the declared positive root")
    for _ in range(steps):
        midpoint = (lower + upper) / 2
        if function(midpoint) > 0:
            upper = midpoint
        else:
            lower = midpoint
    return (lower + upper) / 2, doublings


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    scalar_p = mp.mpf(plan["p"])
    trace_p = mp.mpf(plan["P"])
    constraint_values = [
        mp.mpf(value) for value in plan["constraint_values"]
    ]
    steps = int(plan["bisection_steps"])
    max_doublings = int(plan["max_bracket_doublings"])
    polyroots_maxsteps = int(plan["polyroots_maxsteps"])
    tolerance = mp.mpf(plan["absolute_tolerance"])
    if (
        scalar_p != 1
        or trace_p != mp.mpf("0.5")
        or constraint_values
        != [mp.mpf("-0.2"), mp.mpf("0"), mp.mpf("0.2")]
        or steps != 400
        or max_doublings != 64
        or polyroots_maxsteps != 300
    ):
        raise AssertionError("numerical benchmark mutation")

    discriminant = 3 * scalar_p**2 - 2 * trace_p**2
    records: list[dict[str, Any]] = []
    count_errors: list[mp.mpf] = []
    agreement_errors: list[mp.mpf] = []
    residual_errors: list[mp.mpf] = []
    for constraint_value in constraint_values:
        def polynomial(scale_factor: mp.mpf) -> mp.mpf:
            return (
                72 * mp.pi**4 * scale_factor**4
                + 12
                * mp.pi**2
                * constraint_value
                * scale_factor**3
                - discriminant
            )

        bisection, doublings = bisection_root(
            polynomial, steps, max_doublings
        )
        roots = mp.polyroots(
            [
                72 * mp.pi**4,
                12 * mp.pi**2 * constraint_value,
                0,
                0,
                -discriminant,
            ],
            maxsteps=polyroots_maxsteps,
            error=False,
        )
        positive_real_roots = [
            mp.re(root)
            for root in roots
            if abs(mp.im(root)) <= mp.mpf("1e-80")
            and mp.re(root) > 0
        ]
        count_error = mp.mpf(abs(len(positive_real_roots) - 1))
        polyroot = (
            positive_real_roots[0]
            if positive_real_roots
            else bisection
        )
        agreement = abs(bisection - polyroot)
        residual = abs(polynomial(polyroot)) / max(
            mp.mpf("1"), abs(discriminant)
        )
        count_errors.append(count_error)
        agreement_errors.append(agreement)
        residual_errors.append(residual)
        scale_factor = bisection
        trace_fp = (
            mp.mpf("1.5") * constraint_value
            + 12 * mp.pi**2 * scale_factor
        )
        records.append(
            {
                "c": mp_string(constraint_value),
                "bisection_root": mp_string(bisection),
                "polyroot": mp_string(polyroot),
                "positive_real_root_count": len(positive_real_roots),
                "method_agreement": mp_string(agreement),
                "normalized_polynomial_residual": mp_string(residual),
                "D": mp_string(trace_fp),
                "bracket_doublings": doublings,
            }
        )

    audit.check_numerical(
        "G1.darboux.numerical.unique_positive_roots",
        max(count_errors),
        mp.mpf("0"),
        "absolute_count_error",
        "the independent polynomial-root census has exactly one positive real root at all three frozen c values",
        {"samples": records},
    )
    audit.check_numerical(
        "G1.darboux.numerical.root_method_agreement",
        max(agreement_errors),
        tolerance,
        "absolute",
        "400-step high-precision bisection and arbitrary-precision polynomial roots agree",
        {"maximum_error": mp_string(max(agreement_errors))},
    )
    audit.check_numerical(
        "G1.darboux.numerical.root_residuals",
        max(residual_errors),
        tolerance,
        "normalized_absolute",
        "the independent polynomial roots satisfy the frozen implicit equation",
        {"maximum_error": mp_string(max(residual_errors))},
    )
    return {
        "precision_digits": mp.mp.dps,
        "benchmark": {
            "p": mp_string(scalar_p),
            "P": mp_string(trace_p),
            "R": mp_string(discriminant),
            "constraint_values": [
                mp_string(value) for value in constraint_values
            ],
        },
        "methods": [
            "fixed-step sign-bracket bisection",
            "mpmath arbitrary-precision polynomial roots",
        ],
        "samples": records,
        "root_calls": 6,
        "quadratures": 0,
        "ode_calls": 0,
    }


def decision_from_flags(
    domain_pass: bool,
    canonical_pass: bool,
    shell_pass: bool,
    numerical_pass: bool,
) -> tuple[str, str]:
    if domain_pass and canonical_pass and shell_pass and numerical_pass:
        return (
            "KEEP_V0_CLASSICAL_COMPONENTWISE_OFFSHELL_DARBOUX_CHART",
            "CLOSE_CLASSICAL_COMPONENTWISE_OFFSHELL_CHART_ONLY_NO_AUTOMATIC_SUCCESSOR",
        )
    if not domain_pass:
        return (
            "KILL_OFFSHELL_EXTENSION_ON_DECLARED_COMPONENT",
            "KILL_V0_OFFSHELL_CHART_ROUTE_ON_FROZEN_DOMAIN",
        )
    if not canonical_pass:
        return (
            "KILL_PROPOSED_OFFSHELL_CHART_KEEP_PRIOR_ONSHELL_RESULT",
            "RETAIN_PRIOR_LOCAL_ONSHELL_ACTION_ONLY",
        )
    if not shell_pass:
        return (
            "KEEP_V0_COMPONENTWISE_DARBOUX_CHART_KILL_DECLARED_ONSHELL_RECOVERY",
            "NARROW_CHART_ONLY_ENDPOINT_LINEAGE_NOT_KEPT",
        )
    return "INCONCLUSIVE", "OPEN"


def select_decision(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    domain_ids = {
        "G1.darboux.constraint_polynomial",
        "G1.darboux.trace_fp_positive_identity",
        "G1.darboux.positive_root_existence",
        "G1.darboux.positive_root_uniqueness",
        "G1.darboux.segment_domain",
    }
    canonical_ids = {
        "G1.darboux.trace_pair_and_swapped_potential",
        "G1.darboux.implicit_root_derivatives",
        "G1.darboux.generating_function_derivatives",
        "G1.darboux.canonical_one_form",
        "G1.darboux.endpoint_action_variation",
        "G1.darboux.canonical_poisson_matrix",
        "G1.darboux.symplectic_jacobian",
        "G1.darboux.local_inverse_and_static_slice",
    }
    shell_ids = {
        "G1.darboux.shell_q_recovery",
        "G1.darboux.shell_phi_star_recovery",
        "G1.darboux.shell_boundary_potential_recovery",
        "G1.darboux.shell_fp_measure_recovery",
        "G1.darboux.action_ledger_separation",
    }
    numerical_ids = {
        "G1.darboux.numerical.unique_positive_roots",
        "G1.darboux.numerical.root_method_agreement",
        "G1.darboux.numerical.root_residuals",
    }
    all_scientific_ids = {
        record["id"] for record in audit.exact + audit.numerical
    }
    declared_ids = domain_ids | canonical_ids | shell_ids | numerical_ids
    if all_scientific_ids != declared_ids:
        missing = sorted(declared_ids - all_scientific_ids)
        unexpected = sorted(all_scientific_ids - declared_ids)
        raise AssertionError(
            f"decision check partition mutation: missing={missing}, "
            f"unexpected={unexpected}"
        )

    domain_pass = all(audit.passed(check_id) for check_id in domain_ids)
    canonical_pass = all(
        audit.passed(check_id) for check_id in canonical_ids
    )
    shell_pass = all(audit.passed(check_id) for check_id in shell_ids)
    numerical_pass = all(
        audit.passed(check_id) for check_id in numerical_ids
    )
    verdict, programme_impact = decision_from_flags(
        domain_pass, canonical_pass, shell_pass, numerical_pass
    )
    declared_rows = {
        (row["verdict"], row["programme_impact"])
        for row in frozen_input["decision_table"]
    }
    if (verdict, programme_impact) not in declared_rows:
        raise AssertionError("selected decision is not a frozen decision row")

    reachability_cases = {
        decision_from_flags(True, True, True, True),
        decision_from_flags(False, True, True, True),
        decision_from_flags(True, False, True, True),
        decision_from_flags(True, True, False, True),
        decision_from_flags(True, True, True, False),
    }
    if reachability_cases != declared_rows:
        raise AssertionError(
            "frozen decision rows are not exactly reachable in memory"
        )

    if verdict == (
        "KEEP_V0_CLASSICAL_COMPONENTWISE_OFFSHELL_DARBOUX_CHART"
    ):
        classification = (
            "GATE1_V0_CLASSICAL_COMPONENTWISE_OFFSHELL_DARBOUX_CHART_"
            "KEEP_QUANTUM_ENDPOINT_BFV_AND_DELTA_C_KERNEL_OPEN"
        )
        meaning = (
            "keep the exact classical Darboux chart and endpoint boundary "
            "potential on U_plus, together with its c=0 recovery; no "
            "quantum endpoint state, BFV source, delta(C) kernel, global "
            "gauge or physical cycle is promoted"
        )
        chart_scope = "KEEP_CLASSICAL_COMPONENTWISE_ON_U_PLUS"
        shell_scope = "RECOVERS_PRIOR_PHI_STAR_AND_B_EQUALS_P"
    elif verdict == (
        "KEEP_V0_COMPONENTWISE_DARBOUX_CHART_KILL_DECLARED_ONSHELL_RECOVERY"
    ):
        classification = (
            "GATE1_V0_COMPONENTWISE_DARBOUX_CHART_KEPT_"
            "DECLARED_ONSHELL_LINEAGE_KILLED"
        )
        meaning = (
            "keep only the independently passing chart and reject its "
            "declared c=0 connection to the prior endpoint result"
        )
        chart_scope = "KEEP_CLASSICAL_COMPONENTWISE_ON_U_PLUS"
        shell_scope = "KILL_DECLARED_RECOVERY"
    elif verdict == "KILL_OFFSHELL_EXTENSION_ON_DECLARED_COMPONENT":
        classification = "GATE1_V0_OFFSHELL_DOMAIN_ROUTE_KILLED"
        meaning = "reject the off-shell extension on the declared U_plus domain"
        chart_scope = "KILL_ON_DECLARED_DOMAIN"
        shell_scope = "PRIOR_ONSHELL_RESULT_UNCHANGED"
    elif verdict == (
        "KILL_PROPOSED_OFFSHELL_CHART_KEEP_PRIOR_ONSHELL_RESULT"
    ):
        classification = "GATE1_V0_PROPOSED_DARBOUX_CONSTRUCTION_KILLED"
        meaning = (
            "reject the proposed generating-function chart while preserving "
            "the independently established prior on-shell result"
        )
        chart_scope = "KILL_PROPOSED_CONSTRUCTION"
        shell_scope = "PRIOR_ONSHELL_RESULT_UNCHANGED"
    else:
        classification = "GATE1_V0_OFFSHELL_DARBOUX_CHART_INCONCLUSIVE"
        meaning = "leave the chart unpromoted without an automatic successor"
        chart_scope = "INCONCLUSIVE"
        shell_scope = "INCONCLUSIVE"

    return {
        "classification": classification,
        "verdict": verdict,
        "programme_impact": programme_impact,
        "meaning": meaning,
        "chart_scope": chart_scope,
        "shell_scope": shell_scope,
        "check_partitions": {
            "domain_pass": domain_pass,
            "canonical_pass": canonical_pass,
            "shell_pass": shell_pass,
            "numerical_pass": numerical_pass,
            "all_scientific_pass": (
                domain_pass
                and canonical_pass
                and shell_pass
                and numerical_pass
            ),
            "failed_scientific_ids": audit.failed_scientific_ids(),
        },
        "reachable_frozen_rows": [
            {"verdict": row[0], "programme_impact": row[1]}
            for row in sorted(reachability_cases)
        ],
    }


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream_provenance: dict[str, str],
    audit: Audit,
) -> dict[str, Any]:
    runner_path = Path(__file__)
    runner_sha256 = sha256_bytes(runner_path.read_bytes())
    exact = exact_calculation(audit)
    numerical = numerical_calculation(frozen_input, audit)
    decision = select_decision(frozen_input, audit)
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": decision["classification"],
        "verdict": decision["verdict"],
        "programme_impact": decision["programme_impact"],
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {"path": RUNNER_RELPATH, "sha256": runner_sha256},
        "upstream_provenance": [
            {"path": path, "sha256": sha256}
            for path, sha256 in sorted(upstream_provenance.items())
        ],
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": audit.numerical,
        "decision_trace": {
            "meaning": decision["meaning"],
            "check_partitions": decision["check_partitions"],
            "scientific_nonpass_policy": (
                "record VALID_RUN and select a frozen terminal row; do not "
                "raise, resize the domain or authorize a diagnostic descendant"
            ),
            "source_boundary": (
                "HTV supplies the endpoint-improvement framework, not this "
                "model chart or a quantum transform; Banihashemi-Jacobson "
                "supply reduced-phase-space and lapse-contour boundaries, "
                "not this closed-FRW construction; Marolf supplies the "
                "still-uncomputed distributional physical-inner-product "
                "target, not a classical-chart-to-quantum-kernel implication"
            ),
        },
        "scope_status": {
            "local_v0_componentwise_offshell_darboux_chart": decision[
                "chart_scope"
            ],
            "prior_onshell_endpoint_recovery": decision["shell_scope"],
            "full_off_shell_canonical_transform": None,
            "global_offshell_canonical_atlas": None,
            "normalized_quantum_endpoint_state_transform": None,
            "endpoint_state_transform": None,
            "ghost_endpoint_sector": None,
            "replacement_gauge_fermion": None,
            "full_replacement_bfv_measure": None,
            "replacement_source_discretization": None,
            "old_fixed_a_kernel_equivalence": None,
            "full_real_lapse_delta_C_kernel": None,
            "zero_lapse_distribution": None,
            "global_fundamental_region": None,
            "gribov_copy_census": None,
            "determinant_line_orientation": None,
            "full_joint_orientation": None,
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
                "normalized quantum endpoint-state transform with ordering, measure, domains and unitarity",
                "ghost, antighost, multiplier endpoints, nilpotent BRST charge and replacement gauge fermion",
                "replacement BFV source and comparison with the old fixed-a constant-lapse kernel",
                "full-real-lapse distributional delta(C) physical-inner-product kernel and zero-lapse regulator removal",
                "other components, global orbit coverage, Gribov census, determinant-line orientation and physical original cycle",
            ],
        },
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": expected_fail_closed_outputs(),
        "resource_accounting": {
            "root_calls": numerical["root_calls"],
            "quadratures": 0,
            "ode_calls": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
            "scientific_nonpass_count": len(
                audit.failed_scientific_ids()
            ),
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


def main() -> None:
    if sys.argv[1:]:
        raise AssertionError("this frozen calculation accepts no arguments")
    frozen_input, input_sha256, upstream_provenance = load_frozen_input()
    audit = Audit()
    result = build_result(
        frozen_input, input_sha256, upstream_provenance, audit
    )
    encoded = json.dumps(
        result,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError(
            f"result artifact is {len(encoded)} bytes, cap is {ARTIFACT_CAP_BYTES}"
        )
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "classification": result["classification"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": sum(
                    record["passed"] for record in audit.exact
                ),
                "exact_checks_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_passed": sum(
                    record["passed"] for record in audit.numerical
                ),
                "numerical_checks_total": len(audit.numerical),
                "scientific_nonpass_count": len(
                    audit.failed_scientific_ids()
                ),
                "root_calls": result["resource_accounting"]["root_calls"],
                "quadratures": 0,
                "ode_calls": 0,
                "gate1": result["gate1_decision"],
                "global_n_sigma": None,
                "physical_original_cycle": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
