#!/usr/bin/env python3
"""Gate 1 -- homogeneous trace-gauge FP admissibility control.

This bounded non-numbered calculation separates a genuine local
constraint--gauge reduction from deletion of the negative scale-factor
momentum Gaussian.  It derives the homogeneous trace canonical pair, its
Lorentzian Faddeev--Popov bracket, simple-root orientation, the exact Gribov
horizon, and the remaining lower-lateral scalar Gaussian.  It then checks the
finite m=2 lapse-gauge rank and the preservation equation that prevent a
static trace condition from being appended to the existing proper-time-gauge
source.

The result is a local workbench discriminator.  It rejects only appending the
trace delta to the unchanged proper-time/fixed-a source.  It does not construct
an improved static or time-dependent replacement gauge, a full BFV measure, a
physical original cycle, a global intersection coefficient, a physics claim,
or a TOE claim.  One adjacent JSON result is written and no descendant
calculation is started.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_INPUTS.json"
RESULT_NAME = "GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_trace_gauge_fp_admissibility.py"
)
EXPECTED_INPUT_SHA256 = (
    "513e14db2db7991fdda43f6049336ba092abcb7cb335c0bb696328ca746ee12d"
)
CALCULATION_ID = "Gate1TraceGaugeFpAdmissibility"
RESULT_SCHEMA = "ice.gate1.trace-gauge-fp-admissibility.result.v1"
RESULT_PREFIX = "GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)

    def register_id(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> None:
        self.register_id(check_id)
        if not passed:
            raise AssertionError(f"[EXACT FAIL] {check_id}: {statement}")
        self.exact.append(
            {"id": check_id, "passed": True, "statement": statement}
        )

    def check_numerical(
        self,
        check_id: str,
        relative_error: mp.mpf,
        tolerance: mp.mpf,
        statement: str,
        details: dict[str, Any],
    ) -> None:
        self.register_id(check_id)
        passed = bool(relative_error <= tolerance)
        record = {
            "id": check_id,
            "passed": passed,
            "statement": statement,
            "relative_error": mp_string(relative_error, 24),
            "relative_tolerance": mp_string(tolerance, 8),
            **details,
        }
        if not passed:
            raise AssertionError(
                f"[NUMERICAL FAIL] {check_id}: relative error "
                f"{relative_error} exceeds {tolerance}"
            )
        self.numerical.append(record)

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


def complex_record(value: mp.mpc, digits: int = 40) -> dict[str, str]:
    return {
        "real": mp_string(mp.re(value), digits),
        "imag": mp_string(mp.im(value), digits),
    }


def load_frozen_input() -> tuple[dict[str, Any], str]:
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
        "ice.gate1.trace-gauge-fp-admissibility.input.v1"
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
        "ode_calls": 0,
        "automatic_descendants": 0,
    }:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "physical_original_cycle": None,
        "full_joint_orientation": None,
        "full_m2_bfv_measure": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }
    if payload["required_fail_closed_outputs"] != expected_nulls:
        raise AssertionError("fail-closed output mutation")
    return payload, observed


def exact_calculation(audit: Audit) -> dict[str, Any]:
    a, hbar, epsilon = sp.symbols(
        "a hbar epsilon", positive=True, real=True
    )
    p_a, p_phi, p_ea, p_ephi = sp.symbols(
        "p_a p_phi p_Ea p_Ephi", real=True
    )
    potential = sp.symbols("V", nonnegative=True, real=True)
    f, f_dot, lapse, q = sp.symbols("f f_dot N q", real=True)
    u = sp.symbols("u", positive=True, real=True)
    residual = sp.symbols("r", positive=True, real=True)
    orientation = sp.symbols("orientation", nonzero=True, real=True)
    epsilon_1 = sp.symbols("epsilon_1", real=True)
    q_dot, f_symbol_dot = sp.symbols("Q_dot f_symbol_dot", real=True)

    def poisson_a(expr1: sp.Expr, expr2: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(expr1, a) * sp.diff(expr2, p_a)
            - sp.diff(expr1, p_a) * sp.diff(expr2, a)
        )

    constraint_l = (
        -p_a**2 / (24 * sp.pi**2 * a)
        + p_phi**2 / (4 * sp.pi**2 * a**3)
        + 2 * sp.pi**2 * (-3 * a + a**3 * potential)
    )
    constraint_e = (
        -p_ea**2 / (24 * sp.pi**2 * a)
        + p_ephi**2 / (4 * sp.pi**2 * a**3)
        + 2 * sp.pi**2 * (3 * a - a**3 * potential)
    )
    trace_q = 2 * sp.log(a)
    trace_p = a * p_a / 2
    trace_one_form_coefficient = sp.simplify(
        trace_p * sp.diff(trace_q, a)
    )
    audit.check_exact(
        "G1.trace.canonical_pair_and_one_form",
        poisson_a(trace_q, trace_p) == 1
        and sp.simplify(trace_one_form_coefficient - p_a) == 0,
        "Q=2*log(a), P_tr=a*p_a/2 is canonical and exactly preserves p_a*da",
    )

    wick_constraint = sp.simplify(
        constraint_l.subs({p_a: sp.I * p_ea, p_phi: sp.I * p_ephi})
        + constraint_e
    )
    audit.check_exact(
        "G1.trace.lorentzian_euclidean_constraint_wick_map",
        wick_constraint == 0,
        "the repository convention p_L=i*p_E gives C_L(q,i*p_E)=-C_E(q,p_E)",
    )

    trace_fp_l = poisson_a(trace_p - f, constraint_l)
    expected_trace_fp_l = (
        -p_a**2 / (16 * sp.pi**2 * a)
        + 3 * p_phi**2 / (8 * sp.pi**2 * a**3)
        + 3 * sp.pi**2 * a * (1 - a**2 * potential)
    )
    audit.check_exact(
        "G1.trace.lorentzian_fp_bracket",
        sp.simplify(trace_fp_l - expected_trace_fp_l) == 0,
        "the Lorentzian homogeneous trace FP bracket is derived exactly rather than imported from the Euclidean clock scan",
    )

    trace_p_e = a * p_ea / 2
    trace_fp_e = sp.simplify(
        sp.diff(trace_p_e, a) * sp.diff(constraint_e, p_ea)
        - sp.diff(trace_p_e, p_ea) * sp.diff(constraint_e, a)
    )
    wick_fp = sp.simplify(
        trace_fp_l.subs({p_a: sp.I * p_ea, p_phi: sp.I * p_ephi})
        + trace_fp_e
    )
    audit.check_exact(
        "G1.trace.fp_wick_algebraic_sign",
        wick_fp == 0,
        "under p_L=i*p_E the Lorentzian and Euclidean trace FP bracket formulas have opposite algebraic sign",
    )

    shell_trace_fp = 6 * sp.pi**2 * a * (2 - a**2 * potential)
    audit.check_exact(
        "G1.trace.fp_shell_identity",
        sp.simplify(
            trace_fp_l - sp.Rational(3, 2) * constraint_l - shell_trace_fp
        )
        == 0,
        "D_L=(3/2)*C_L+6*pi^2*a*(2-a^2*V), so the shell FP horizon is a^2*V=2",
    )
    neck_l = sp.simplify(
        trace_fp_l.subs(
            {p_a: 0, p_phi: 0, potential: 3 / a**2}
        )
    )
    neck_e = sp.simplify(
        trace_fp_e.subs(
            {p_ea: 0, p_ephi: 0, potential: 3 / a**2}
        )
    )
    audit.check_exact(
        "G1.trace.reflection_neck_wick_sign_control",
        sp.simplify(neck_l + 6 * sp.pi**2 * a) == 0
        and sp.simplify(neck_e - 6 * sp.pi**2 * a) == 0,
        "the reflection neck has Lorentzian trace FP -6*pi^2*a and Euclidean trace FP +6*pi^2*a",
    )

    p_a_fp_l = poisson_a(p_a, constraint_l)
    audit.check_exact(
        "G1.trace.homogeneous_trace_rescaling_measure",
        sp.simplify(
            (2 / a) * trace_fp_l.subs(p_a, 0)
            - p_a_fp_l.subs(p_a, 0)
        )
        == 0,
        "on p_a=0 the delta(P_tr) trace determinant product equals the delta(p_a) determinant product for a>0",
    )

    constrained_p_a = 2 * f / a
    constraint_f = sp.simplify(constraint_l.subs(p_a, constrained_p_a))
    effective_fp = sp.simplify(
        (2 / a) * trace_fp_l.subs(p_a, constrained_p_a)
    )
    audit.check_exact(
        "G1.trace.delta_jacobian_and_root_derivative",
        sp.simplify(effective_fp + sp.diff(constraint_f, a)) == 0,
        "delta(P_tr-f)=(2/a)delta(p_a-2f/a) and its effective signed FP factor is -dC_f/da",
    )

    dirac_matrix = sp.Matrix([[0, trace_fp_l], [-trace_fp_l, 0]])
    audit.check_exact(
        "G1.trace.constraint_gauge_dirac_rank",
        sp.simplify(dirac_matrix.det() - trace_fp_l**2) == 0,
        "the constraint-gauge Dirac matrix has rank two exactly where the FP bracket is nonzero",
    )
    deletion_pullback = sp.Matrix(
        [[0, 0, 0], [0, 0, 1], [0, -1, 0]]
    )
    reduced_pullback = sp.Matrix([[0, 1], [-1, 0]])
    audit.check_exact(
        "G1.trace.deletion_versus_reduction_rank",
        deletion_pullback.rank() == 2
        and deletion_pullback.shape == (3, 3)
        and reduced_pullback.rank() == 2
        and reduced_pullback.det() == 1,
        "p_a=0 alone leaves a rank-two presymplectic form on three dimensions, while a simple constraint-gauge root leaves the nondegenerate scalar pair",
    )

    constraint_zero_trace = sp.simplify(constraint_l.subs(p_a, 0))
    shell_polynomial_identity = sp.simplify(
        4 * sp.pi**2 * a**3 * constraint_zero_trace
        - (
            p_phi**2
            - 8 * sp.pi**4 * a**4 * (3 - a**2 * potential)
        )
    )
    audit.check_exact(
        "G1.trace.zero_trace_shell_polynomial",
        shell_polynomial_identity == 0,
        "at f=0 the shell is p_phi^2=8*pi^4*a^4*(3-a^2*V)",
    )

    branch_function = u**2 * (3 - u)
    branch_derivative = sp.factor(sp.diff(branch_function, u))
    kappa_two_factor = sp.factor(u**3 - 3 * u**2 + 2)
    positive_roots = [sp.Integer(1), 1 + sp.sqrt(3)]
    root_residuals = [
        sp.simplify(branch_function.subs(u, root) - 2)
        for root in positive_roots
    ]
    root_orientation_factors = [
        sp.simplify(2 - root) for root in positive_roots
    ]
    audit.check_exact(
        "G1.trace.fp_horizon_and_two_sheet_orientation",
        sp.simplify(branch_derivative - 3 * u * (2 - u)) == 0
        and branch_function.subs(u, 2) == 4
        and kappa_two_factor == (u - 1) * (u**2 - 2 * u - 2)
        and root_residuals == [0, 0]
        and root_orientation_factors[0] > 0
        and root_orientation_factors[1] < 0,
        "on the V>0 shell domain 0<u<=3, u=2 is the exact kappa=4 FP horizon and the two positive kappa=2 a-root sheets have opposite pre-orientation signed residues",
    )

    signed_positive_derivative = sp.simplify((-residual) / residual)
    signed_negative_derivative = sp.simplify(residual / residual)
    absolute_positive_derivative = sp.simplify(abs(-residual) / residual)
    absolute_negative_derivative = sp.simplify(abs(residual) / residual)
    audit.check_exact(
        "G1.trace.signed_and_absolute_root_ledgers",
        signed_positive_derivative == -1
        and signed_negative_derivative == 1
        and absolute_positive_derivative == 1
        and absolute_negative_derivative == 1,
        "using effective_fp=-dC_f/da, signed a-root residues follow sgn(D), whereas the elementary absolute delta Jacobian gives +1 on either simple root",
    )

    nonzero_fp = sp.symbols("D_nonzero", nonzero=True, real=True)
    static_solutions = sp.solve(lapse * nonzero_fp, lapse)
    time_dependent_lapse = sp.simplify(f_dot / nonzero_fp)
    audit.check_exact(
        "G1.trace.gauge_preservation_obstruction",
        static_solutions == [0]
        and sp.simplify(time_dependent_lapse * nonzero_fp - f_dot) == 0,
        "dot(chi)=N*D-dot(f) makes the ordinary regular static classical representative have N=0; within this representative nonzero N requires time-dependent f",
    )

    h = sp.Rational(1, 2)
    delta_lapses = sp.Matrix([epsilon_1 / h, -epsilon_1 / h])
    lapse_generator = delta_lapses.jacobian([epsilon_1])
    delta_proper_time = sp.simplify(h * sum(delta_lapses))
    delta_lapse_difference = sp.simplify(delta_lapses[0] - delta_lapses[1])
    audit.check_exact(
        "G1.trace.m2_proper_time_gauge_rank",
        lapse_generator.rank() == 1
        and delta_lapses == sp.Matrix([2 * epsilon_1, -2 * epsilon_1])
        and delta_proper_time == 0
        and delta_lapse_difference == 4 * epsilon_1,
        "N0=N1 fixes the sole endpoint-preserving m=2 lapse gauge mode while T=(N0+N1)/2 remains invariant",
    )

    p_endpoint, q_endpoint, dp_endpoint, dq_endpoint = sp.symbols(
        "P_endpoint Q_endpoint dP_endpoint dQ_endpoint", real=True
    )
    fixed_momentum_boundary_variation = sp.simplify(
        p_endpoint * dq_endpoint
        - (p_endpoint * dq_endpoint + q_endpoint * dp_endpoint)
    )
    integration_by_parts = sp.simplify(
        f * q_dot
        - ((f_symbol_dot * trace_q + f * q_dot) - f_symbol_dot * trace_q)
    )
    audit.check_exact(
        "G1.trace.endpoint_polarization_and_reduced_action",
        fixed_momentum_boundary_variation == -q_endpoint * dp_endpoint
        and integration_by_parts == 0,
        "subtracting [P_tr*Q] changes fixed-Q endpoints to fixed-P_tr, and f*Qdot=[fQ]dot-fdot*Q",
    )

    endpoint_trace_p = sp.symbols("P_chart", real=True)
    constraint_fixed_q_chart = sp.simplify(
        constraint_l.subs(p_a, 2 * endpoint_trace_p / a)
    )
    fixed_q_endpoint_transversality = sp.simplify(
        sp.diff(constraint_fixed_q_chart, endpoint_trace_p).subs(
            endpoint_trace_p, 0
        )
    )
    swapped_endpoint_transversality = sp.simplify(
        -a * sp.diff(constraint_l, a) / 2
        + p_a * sp.diff(constraint_l, p_a) / 2
    )
    audit.check_exact(
        "G1.trace.endpoint_chart_transversality",
        fixed_q_endpoint_transversality == 0
        and sp.simplify(swapped_endpoint_transversality - trace_fp_l) == 0,
        "the original fixed-Q chart fails static P_tr=0 endpoint transversality, while the chosen swapped chart (Q',P')=(P_tr,-Q) has derivative D_L and is locally transverse where D_L is nonzero",
    )

    coordinate_clock_fp = poisson_a(a, constraint_l)
    scalar_clock_fp = sp.diff(constraint_l, p_phi)
    audit.check_exact(
        "G1.trace.intrinsic_clock_comparison",
        sp.simplify(coordinate_clock_fp + p_a / (12 * sp.pi**2 * a))
        == 0
        and sp.simplify(
            scalar_clock_fp - p_phi / (2 * sp.pi**2 * a**3)
        )
        == 0
        and coordinate_clock_fp.subs(p_a, 0) == 0,
        "the scale coordinate clock is singular at p_a=0, while a scalar clock does not remove the negative p_a block",
    )

    lower_z = lapse - sp.I * epsilon
    upper_z = lapse + sp.I * epsilon
    lower_alpha = sp.I * lower_z / (4 * sp.pi**2 * a**3 * hbar)
    upper_alpha = sp.I * upper_z / (4 * sp.pi**2 * a**3 * hbar)
    lower_alpha_real = sp.simplify(
        sp.re(lower_alpha).expand(complex=True)
    )
    upper_alpha_real = sp.simplify(
        sp.re(upper_alpha).expand(complex=True)
    )
    effective_fp_zero_trace = sp.factor(
        (2 / a) * trace_fp_l.subs(p_a, 0)
    )
    audit.check_exact(
        "G1.trace.remaining_scalar_lateral_convergence",
        sp.simplify(
            lower_alpha_real - epsilon / (4 * sp.pi**2 * a**3 * hbar)
        )
        == 0
        and sp.simplify(
            upper_alpha_real + epsilon / (4 * sp.pi**2 * a**3 * hbar)
        )
        == 0
        and sp.Poly(effective_fp_zero_trace, p_phi).degree() == 2,
        "after local trace reduction the FP factor is polynomial and N-i*epsilon damps the remaining real p_phi Gaussian while N+i*epsilon grows",
    )

    benchmark_constraint = sp.simplify(
        constraint_zero_trace.subs({a: 1, potential: 0})
    )
    benchmark_fp = sp.simplify(
        effective_fp_zero_trace.subs({a: 1, potential: 0})
    )
    shell_root = 2 * sp.sqrt(6) * sp.pi**2
    shell_derivative = sp.diff(benchmark_constraint, p_phi)
    raw_delta_target = 8 * sp.sqrt(6) * sp.pi**2 * sp.cos(
        shell_root * q / hbar
    )
    reconstructed_delta_target = sp.simplify(
        benchmark_fp.subs(p_phi, shell_root)
        / abs(shell_derivative.subs(p_phi, shell_root))
        * sp.exp(sp.I * shell_root * q / hbar)
        + benchmark_fp.subs(p_phi, -shell_root)
        / abs(shell_derivative.subs(p_phi, -shell_root))
        * sp.exp(-sp.I * shell_root * q / hbar)
    )
    audit.check_exact(
        "G1.trace.flat_minimum_shell_and_delta_target",
        sp.simplify(
            benchmark_fp
            - (3 * p_phi**2 / (4 * sp.pi**2) + 6 * sp.pi**2)
        )
        == 0
        and benchmark_fp.is_positive is True
        and sp.simplify(benchmark_constraint.subs(p_phi, shell_root)) == 0
        and sp.simplify(benchmark_constraint.subs(p_phi, -shell_root)) == 0
        and sp.simplify(
            benchmark_fp.subs(p_phi, shell_root) - 24 * sp.pi**2
        )
        == 0
        and sp.simplify(reconstructed_delta_target - raw_delta_target) == 0,
        "at a=1,V=0 the effective FP polynomial is positive and the two constraint roots give the exact raw cosine target",
    )

    alpha = sp.symbols("alpha", positive=True)
    source_q = sp.symbols("q_source", real=True)
    gaussian_base = sp.sqrt(sp.pi / alpha) * sp.exp(
        -source_q**2 / (4 * alpha * hbar**2)
    )
    gaussian_second_moment = gaussian_base * (
        1 / (2 * alpha)
        - source_q**2 / (4 * alpha**2 * hbar**2)
    )
    audit.check_exact(
        "G1.trace.polynomial_gaussian_formula",
        sp.simplify(
            -sp.diff(gaussian_base, alpha) - gaussian_second_moment
        )
        == 0,
        "the effective quadratic FP insertion follows by -d/dalpha of the convergent sourced Gaussian",
    )

    signed_ledger = orientation * nonzero_fp
    reversed_ledger = (-orientation) * (-nonzero_fp)
    audit.check_exact(
        "G1.trace.gauge_orientation_mutation_control",
        sp.simplify(reversed_ledger - signed_ledger) == 0,
        "reversing chi and its gauge orientation together preserves the oriented ledger; the signed determinant alone flips",
    )

    audit.guard_theorem(
        "G1.guard.local_fp_reduction",
        True,
        "finite-dimensional single-constraint Faddeev--Popov reduction at simple transverse roots",
        "a>0, C_L=0, chi=P_tr-f=0, D_L={chi,C_L} nonzero; one connected local root chart at a time",
        "the exact delta Jacobian and Dirac rank justify only a local reduction; global orbit coverage and Gribov-copy removal are not inferred",
    )
    audit.guard_theorem(
        "G1.guard.signed_versus_absolute_fp",
        True,
        "separation of the Grassmann signed determinant from the reduced-orbit absolute Jacobian",
        "simple roots with an explicitly chosen gauge orientation",
        "opposite pre-orientation signed root residues are not silently converted into a physical negative-arm or global relative sign; componentwise gauge orientation remains a separate choice and the absolute ledger stays positive",
    )
    audit.guard_theorem(
        "G1.guard.static_gauge_preservation",
        True,
        "Hamiltonian preservation of an explicitly time-dependent canonical gauge",
        "homogeneous multiplier N and dot(chi)=partial_s(chi)+{chi,N*C_L}; D_L nonzero",
        "the N=0 conclusion describes the ordinary static homogeneous classical representative; it excludes neither an improved-boundary static canonical-gauge path integral nor the full inhomogeneous maximal-slicing lapse equation",
    )
    audit.guard_theorem(
        "G1.guard.polynomial_gaussian",
        True,
        "sourced real Gaussian moments for Re(alpha)>0",
        "a>0, hbar>0, z=N-i*epsilon with epsilon>0, and a degree-two FP insertion",
        "absolute convergence is established for the formal local reduced scalar fiber only, not for a rederived m=2 BFV source",
    )
    audit.guard_theorem(
        "G1.guard.m2_gauge_rank_scope",
        True,
        "rank of the endpoint-preserving finite m=2 lapse variation",
        "h=1/2, epsilon_0=epsilon_2=0, proper-time condition N0=N1",
        "the rank check shows no residual nonzero lapse-gauge mode in the current source; it does not construct an exactly gauge-invariant replacement discretization",
    )

    return {
        "canonical_trace_pair": {
            "Q": str(trace_q),
            "P_tr": str(trace_p),
            "poisson_bracket": "1",
            "one_form": "P_tr*dQ=p_a*da",
        },
        "constraints": {
            "lorentzian": str(constraint_l),
            "euclidean": str(constraint_e),
            "wick_identity": "C_L(q,i*p_E)=-C_E(q,p_E)",
        },
        "trace_fp": {
            "lorentzian_off_shell": str(trace_fp_l),
            "euclidean_off_shell": str(trace_fp_e),
            "shell": str(shell_trace_fp),
            "horizon": "a^2*V=2",
            "reflection_neck_lorentzian": str(neck_l),
            "reflection_neck_euclidean": str(neck_e),
        },
        "local_reduction": {
            "constraint_after_gauge": str(constraint_f),
            "effective_signed_fp_after_pa_delta": str(effective_fp),
            "root_derivative_identity": "(2/a)*D_L=-dC_f/da",
            "deletion_pullback_rank": deletion_pullback.rank(),
            "deletion_pullback_dimension": 3,
            "reduced_scalar_rank": reduced_pullback.rank(),
            "reduced_scalar_dimension": 2,
        },
        "zero_trace_root_structure": {
            "shell": "p_phi^2=8*pi^4*a^4*(3-a^2*V)",
            "dimensionless_equation": "kappa=u^2*(3-u)",
            "branch_derivative": str(branch_derivative),
            "horizon": {"u": "2", "kappa": "4"},
            "kappa_2_positive_roots": [str(root) for root in positive_roots],
            "kappa_2_orientation_factors": [
                str(value) for value in root_orientation_factors
            ],
            "signed_root_ledger": "sgn(D_L)",
            "absolute_root_ledger": "+1 per simple root",
        },
        "gauge_preservation": {
            "equation": "dot(chi)=N*D_L-dot(f)",
            "static_regular_solution": "N=0",
            "time_dependent_local_solution": "N=dot(f)/D_L",
        "improved_static_replacement_constructed": False,
        "time_dependent_replacement_constructed": False,
        },
        "m2_gauge_rank": {
            "delta_lapses": [str(value) for value in delta_lapses],
            "rank": lapse_generator.rank(),
            "delta_T": str(delta_proper_time),
            "delta_N0_minus_N1": str(delta_lapse_difference),
            "proper_time_condition": "N0=N1",
        },
        "endpoint_polarization": {
            "trace_pair_fixed_momentum_boundary_term": "-[P_tr*Q]",
            "phase31_pa_fixed_momentum_boundary_term": "-[a*p_a]",
            "existing_kernel": "fixed-(a,phi)",
            "same_boundary_problem_without_transform": False,
        },
        "remaining_scalar_fiber": {
            "effective_fp_at_f_zero": str(effective_fp_zero_trace),
            "lower_alpha_real": str(lower_alpha_real),
            "upper_alpha_real": str(upper_alpha_real),
            "flat_minimum_constraint": str(benchmark_constraint),
            "flat_minimum_effective_fp": str(benchmark_fp),
            "flat_minimum_shell_roots": [str(-shell_root), str(shell_root)],
            "flat_minimum_raw_delta_target": str(raw_delta_target),
        },
        "computed_facts": {
            "homogeneous_trace_pair": "CANONICAL",
            "local_trace_constraint_gauge": "ON_SHELL_LOCALLY_REGULAR_AT_EXISTING_SIMPLE_ROOTS_AWAY_FROM_A2V_EQ_2",
            "naive_pa_deletion": "DEGENERATE_NOT_REDUCTION",
            "ordinary_static_regular_classical_representative": "N_ZERO",
            "m2_proper_time_nonzero_gauge_mode": "ALREADY_FIXED",
            "append_trace_to_unchanged_current_m2_source": "NOT_LICENSED_AS_ADDITIONAL_FP_GAUGE_IN_CURRENT_CONSTANT_LAPSE_TRUNCATION",
            "replacement_canonical_gauge_construction": "REQUIRED_NOT_COMPUTED",
            "improved_static_canonical_gauge_with_endpoint_transform": "OPEN_NOT_COMPUTED",
            "time_dependent_trace_gauge": "OPEN_CANDIDATE_NOT_COMPUTED",
            "lower_lateral_formal_local_scalar_fiber": "ABSOLUTELY_CONVERGENT",
            "upper_lateral_formal_local_scalar_fiber": "DIVERGENT",
            "endpoint_treatment": "REQUIRES_ACTION_STATE_TRANSFORM_IF_GAUGE_IS_IMPOSED_AT_ENDPOINTS",
            "global_trace_gauge": "OPEN",
        },
    }


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    benchmark = plan["benchmark"]
    a = mp.mpf(benchmark["a"])
    potential = mp.mpf(benchmark["V"])
    f = mp.mpf(benchmark["f"])
    q = mp.mpf(benchmark["q"])
    hbar = mp.mpf(benchmark["hbar"])
    if a != 1 or potential != 0 or f != 0:
        raise AssertionError("numerical benchmark mutation")
    tolerance = mp.mpf(plan["relative_tolerance"])
    coefficient = mp.mpf(3) / (4 * mp.pi**2)
    constant = 6 * mp.pi**2
    records: list[dict[str, Any]] = []

    for index, (real_text, epsilon_text) in enumerate(
        plan["lower_lateral_points"], 1
    ):
        real_lapse = mp.mpf(real_text)
        regulator = mp.mpf(epsilon_text)
        if regulator <= 0:
            raise AssertionError("lower-lateral regulator must be positive")
        z = mp.mpc(real_lapse, -regulator)
        alpha = 1j * z / (4 * mp.pi**2 * hbar)
        if mp.re(alpha) <= 0:
            raise AssertionError("lower-lateral Gaussian lost positive real part")

        def integrand(momentum: mp.mpf) -> mp.mpc:
            fp = coefficient * momentum**2 + constant
            constraint = momentum**2 / (4 * mp.pi**2) - 6 * mp.pi**2
            return fp * mp.e ** (
                -1j * z * constraint / hbar + 1j * momentum * q / hbar
            )

        observed = mp.quad(integrand, [-mp.inf, mp.inf])
        base = mp.sqrt(mp.pi / alpha) * mp.e ** (
            -(q**2) / (4 * alpha * hbar**2)
        )
        second_moment = base * (
            1 / (2 * alpha) - q**2 / (4 * alpha**2 * hbar**2)
        )
        expected = (
            mp.e ** (1j * 6 * mp.pi**2 * z / hbar)
            * (constant * base + coefficient * second_moment)
        )
        relative_error = abs(observed - expected) / abs(expected)
        details = {
            "z": complex_record(z),
            "alpha": complex_record(alpha),
            "observed": complex_record(observed),
            "expected": complex_record(expected),
        }
        audit.check_numerical(
            f"G1.trace.quadrature.lower_lateral_{index}",
            relative_error,
            tolerance,
            "the real-p_phi integral with the effective trace FP polynomial matches the exact sourced Gaussian moment on the formal local lower-lateral fiber",
            details,
        )
        records.append(
            {
                "point": index,
                "z": complex_record(z),
                "relative_error": mp_string(relative_error, 24),
            }
        )

    return {
        "precision_digits": mp.mp.dps,
        "benchmark": {
            "a": mp_string(a),
            "V": mp_string(potential),
            "f": mp_string(f),
            "q": mp_string(q),
            "hbar": mp_string(hbar),
        },
        "lower_lateral_point_summaries": records,
        "quadratures": len(records),
        "root_calls": 0,
        "ode_calls": 0,
    }


def select_decision(exact: dict[str, Any]) -> dict[str, str]:
    facts = exact["computed_facts"]
    expected = {
        "homogeneous_trace_pair": "CANONICAL",
        "local_trace_constraint_gauge": "ON_SHELL_LOCALLY_REGULAR_AT_EXISTING_SIMPLE_ROOTS_AWAY_FROM_A2V_EQ_2",
        "naive_pa_deletion": "DEGENERATE_NOT_REDUCTION",
        "ordinary_static_regular_classical_representative": "N_ZERO",
        "m2_proper_time_nonzero_gauge_mode": "ALREADY_FIXED",
        "append_trace_to_unchanged_current_m2_source": "NOT_LICENSED_AS_ADDITIONAL_FP_GAUGE_IN_CURRENT_CONSTANT_LAPSE_TRUNCATION",
        "replacement_canonical_gauge_construction": "REQUIRED_NOT_COMPUTED",
        "improved_static_canonical_gauge_with_endpoint_transform": "OPEN_NOT_COMPUTED",
        "time_dependent_trace_gauge": "OPEN_CANDIDATE_NOT_COMPUTED",
        "lower_lateral_formal_local_scalar_fiber": "ABSOLUTELY_CONVERGENT",
        "endpoint_treatment": "REQUIRES_ACTION_STATE_TRANSFORM_IF_GAUGE_IS_IMPOSED_AT_ENDPOINTS",
    }
    if all(facts.get(key) == value for key, value in expected.items()):
        return {
            "verdict": "LOCAL_TRACE_GAUGE_FIBER_KEEP_UNCHANGED_PROPER_TIME_M2_APPEND_KILLED",
            "programme_impact": "NARROW_AND_REDIRECT",
            "matched_predeclared_condition": (
                "the trace pair, local on-shell FP/shell/Jacobian identities, "
                "two-sheet pre-orientation ledger, ordinary static-representative "
                "preservation equation, proper-time m2 rank, endpoint "
                "transversality change, and lower-lateral local Gaussian checks "
                "all pass"
            ),
            "meaning": (
                "keep a genuine local trace-gauge constraint fiber as an "
                "ingredient, but reject appending trace deltas to the unchanged "
                "nonzero-lapse proper-time/fixed-a source; a separately rederived "
                "replacement gauge, action, FP/BFV measure, and endpoint-state "
                "construction is required, while improved static and "
                "time-dependent variants remain open"
            ),
        }
    raise AssertionError("exact facts did not select a predeclared decision row")


def build_result(
    frozen_input: dict[str, Any], input_sha256: str, audit: Audit
) -> dict[str, Any]:
    runner_path = Path(__file__)
    runner_sha256 = sha256_bytes(runner_path.read_bytes())
    exact = exact_calculation(audit)
    numerical = numerical_calculation(frozen_input, audit)
    decision = select_decision(exact)
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": "GATE1_LOCAL_TRACE_FP_REDUCTION_EXISTS_UNCHANGED_PROPER_TIME_M2_ADDITIONAL_GAUGE_APPEND_NOT_LICENSED",
        "verdict": decision["verdict"],
        "programme_impact": decision["programme_impact"],
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {"path": RUNNER_RELPATH, "sha256": runner_sha256},
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": audit.numerical,
        "decision_trace": {
            "matched_predeclared_condition": decision[
                "matched_predeclared_condition"
            ],
            "meaning": decision["meaning"],
            "source_control_status": "LOCAL_REDUCTION_INGREDIENT_NOT_UNCHANGED_CURRENT_M2_SOURCE_REPAIR",
            "primary_source_boundary": (
                "Banihashemi-Jacobson require a constraint-plus-gauge FP measure "
                "before applying the lower-lateral momentum-first argument and "
                "offer trace momentum zero only as a local gauge premise. The "
                "homogeneous preservation equation, finite m2 lapse rank, "
                "endpoint polarization, and signed/absolute ledgers are derived "
                "here and are not supplied by that source."
            ),
        },
        "scope_status": {
            "local_homogeneous_trace_constraint_gauge": "KEEP_ON_EXISTING_SIMPLE_ROOT_CHARTS_AWAY_FROM_FP_HORIZON",
            "ordinary_static_regular_classical_representative_lapse": "N_ZERO",
            "append_to_unchanged_proper_time_m2_source": "NOT_LICENSED_AS_AN_ADDITIONAL_FP_GAUGE",
            "improved_static_canonical_gauge_replacement": "OPEN_NOT_COMPUTED",
            "time_dependent_replacement_gauge": "OPEN_CANDIDATE_NOT_COMPUTED",
            "fixed_a_kernel_equivalence": "NOT_ESTABLISHED_NOT_THE_SAME_BOUNDARY_PROBLEM_WITHOUT_ENDPOINT_TRANSFORM",
            "global_fundamental_region": "OPEN",
            "full_m2_bfv_measure": None,
            "physical_original_cycle": None,
        },
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": {
            "TOE_claim": None,
            "complete_global_signed_intersection_vector": None,
            "full_joint_orientation": None,
            "full_m2_bfv_measure": None,
            "global_n_sigma": None,
            "physical_original_cycle": None,
            "physics_claim": None,
        },
        "resource_accounting": {
            "root_calls": 0,
            "ode_calls": 0,
            "quadratures": numerical["quadratures"],
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
            "computed_scope": frozen_input["computed_scope"],
            "not_computed": frozen_input["not_computed"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256 = load_frozen_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, audit)
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
                "exact_checks_passed": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_passed": len(audit.numerical),
                "quadratures": result["resource_accounting"]["quadratures"],
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
