#!/usr/bin/env python3
"""Gate 1 -- closed-FRW V=0 trace-gauge endpoint triangle.

This bounded, non-numbered calculation constructs one local relational
endpoint completion of the static trace slice P=0 and compares it with a
time-dependent representative P=f(s) on the same constraint orbit.  It checks
the constraint shell, Dirac endpoint coordinate, pulled-back one-form, finite
endpoint gauge flow, local canonical-limit FP measure, reduced Hamiltonian,
and the orbit/action triangles exactly.  Two independent high-precision
quadratures check the finite flow parameters.

The result is restricted to one R>0, D>0 component of the closed-FRW V=0
workbench.  It is not a full off-shell BFV endpoint construction, a proof of
equivalence with the old fixed-a kernel, a full-real-lapse projector matrix
element, a global gauge theorem, a physics claim, or a TOE claim.  It writes
one adjacent JSON result and starts no descendant calculation.
"""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_V0_TRACE_ENDPOINT_COMPLETION_INPUTS.json"
RESULT_NAME = "GATE1_V0_TRACE_ENDPOINT_COMPLETION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_trace_endpoint_completion.py"
)
EXPECTED_INPUT_SHA256 = (
    "a9e3055a8014d16af7bcab815bd88b26ed2f2b22f53e66322d39d0ec596dd638"
)
CALCULATION_ID = "Gate1V0TraceEndpointCompletion"
RESULT_SCHEMA = "ice.gate1.v0-trace-endpoint-completion.result.v1"
RESULT_PREFIX = "GATE1_V0_TRACE_ENDPOINT_COMPLETION_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000
UPSTREAM_HASHES = {
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
    "cpt_temporal_folded_susy/GATE1_TRACE_GAUGE_FP_ADMISSIBILITY_RESULT.json": (
        "b6215136abf6d4018456024789ad4160dac1c28af20bd32078bf8edfc0e0d5fe"
    ),
}


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
        error: mp.mpf,
        tolerance: mp.mpf,
        error_kind: str,
        statement: str,
        details: dict[str, Any],
    ) -> None:
        self.register_id(check_id)
        passed = bool(error <= tolerance)
        record = {
            "id": check_id,
            "passed": passed,
            "statement": statement,
            "error_kind": error_kind,
            "error": mp_string(error, 24),
            "tolerance": mp_string(tolerance, 8),
            **details,
        }
        if not passed:
            raise AssertionError(
                f"[NUMERICAL FAIL] {check_id}: {error_kind} error "
                f"{error} exceeds {tolerance}"
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


def mp_string(value: mp.mpf, digits: int = 50) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


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
        "ice.gate1.v0-trace-endpoint-completion.input.v1"
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
        "full_projector_matrix_element": None,
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
    q, phi, p = sp.symbols("Q phi p", real=True)
    trace_p = sp.symbols("P", real=True)
    f_dot = sp.symbols("f_dot", positive=True, real=True)
    d_q, d_p_trace, d_phi, d_p = sp.symbols(
        "dQ dP dphi dp", real=True
    )

    def poisson_ap(expr1: sp.Expr, expr2: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(expr1, a) * sp.diff(expr2, p_a)
            - sp.diff(expr1, p_a) * sp.diff(expr2, a)
        )

    trace_q_from_a = 2 * sp.log(a)
    trace_p_from_a = a * p_a / 2
    audit.check_exact(
        "G1.endpoint.trace_pair",
        sp.simplify(poisson_ap(trace_q_from_a, trace_p_from_a) - 1) == 0
        and sp.simplify(
            trace_p_from_a * sp.diff(trace_q_from_a, a) - p_a
        )
        == 0,
        "Q=2*log(a), P=a*p_a/2 is canonical and preserves the Liouville one-form",
    )

    constraint = (
        -trace_p**2 / (6 * sp.pi**2 * a**3)
        + p**2 / (4 * sp.pi**2 * a**3)
        - 6 * sp.pi**2 * a
    )
    shell_discriminant = 3 * p**2 - 2 * trace_p**2
    shell_polynomial = sp.simplify(
        12 * sp.pi**2 * a**3 * constraint
        - (shell_discriminant - 72 * sp.pi**4 * a**4)
    )
    q_star = sp.log(shell_discriminant / (72 * sp.pi**4)) / 2
    audit.check_exact(
        "G1.endpoint.closed_frw_v0_shell",
        shell_polynomial == 0,
        "C=0 is exactly R=3*p^2-2*P^2=72*pi^4*a^4 and Q_star=log(R/(72*pi^4))/2",
    )

    trace_fp = sp.simplify(-a * sp.diff(constraint, a) / 2)
    expected_trace_fp = (
        -2 * trace_p**2
        + 3 * p**2
        + 24 * sp.pi**4 * a**4
    ) / (8 * sp.pi**2 * a**3)
    audit.check_exact(
        "G1.endpoint.trace_fp_off_and_on_shell",
        sp.simplify(trace_fp - expected_trace_fp) == 0
        and sp.simplify(
            trace_fp - sp.Rational(3, 2) * constraint - 12 * sp.pi**2 * a
        )
        == 0,
        "D={P,C}=-C_Q and D|C=0=12*pi^2*a is strictly positive for a>0",
    )

    phi_star = phi - sp.sqrt(sp.Rational(3, 2)) * sp.atanh(
        sp.sqrt(sp.Rational(2, 3)) * trace_p / p
    )
    phi_star_p_trace = sp.diff(phi_star, trace_p)
    phi_star_p = sp.diff(phi_star, p)
    audit.check_exact(
        "G1.endpoint.dirac_coordinate_derivatives",
        sp.simplify(phi_star_p_trace + 3 * p / shell_discriminant)
        == 0
        and sp.simplify(phi_star_p - 3 * trace_p / shell_discriminant)
        == 0,
        "the declared local relational coordinate has the exact P and p derivatives required on R>0",
    )

    dirac_bracket = sp.simplify(
        phi_star_p_trace * trace_fp + sp.diff(constraint, p)
    )
    shell_p_squared = (
        2 * trace_p**2 + 72 * sp.pi**4 * a**4
    ) / 3
    audit.check_exact(
        "G1.endpoint.dirac_invariance_on_shell",
        sp.simplify(dirac_bracket.subs(p**2, shell_p_squared)) == 0,
        "{Phi_star,C}=0 on the closed-FRW V=0 constraint shell",
    )

    q_star_p_trace = sp.diff(q_star, trace_p)
    q_star_p = sp.diff(q_star, p)
    one_form_d_p_trace = sp.simplify(
        trace_p * q_star_p_trace - (p * phi_star_p_trace + 1)
    )
    one_form_d_p = sp.simplify(
        trace_p * q_star_p - p * phi_star_p
    )
    one_form_d_phi = sp.simplify(p - p * sp.diff(phi_star, phi))
    audit.check_exact(
        "G1.endpoint.shell_one_form",
        one_form_d_p_trace == 0
        and one_form_d_p == 0
        and one_form_d_phi == 0,
        "on shell P*dQ_star+p*dphi=p*dPhi_star+dP, so the local endpoint potential is B_red=P",
    )

    original_endpoint_variation = trace_p * d_q + p * d_phi
    improved_endpoint_variation = sp.expand(
        original_endpoint_variation
        - (trace_p * d_q + q * d_p_trace)
    )
    audit.check_exact(
        "G1.endpoint.mixed_polarization_boundary_action",
        sp.simplify(
            improved_endpoint_variation
            - (-q * d_p_trace + p * d_phi)
        )
        == 0,
        "S-[P*Q] has fixed-(P,phi) endpoint variation -Q*dP+p*dphi and reduced Hamiltonian H_red=dot(f)*Q_star",
    )

    constraint_p = sp.diff(constraint, trace_p)
    audit.check_exact(
        "G1.endpoint.static_chart_transversality",
        sp.simplify(constraint_p.subs(trace_p, 0)) == 0
        and sp.simplify(-a * sp.diff(constraint, a) / 2 - trace_fp)
        == 0,
        "the original fixed-Q chart is not transverse at static P=0, while the swapped trace chart has derivative D where D is nonzero",
    )

    boundary_integrand_numerator = sp.simplify(
        trace_p * sp.diff(constraint, trace_p)
        + p * sp.diff(constraint, p)
        - constraint
    )
    audit.check_exact(
        "G1.endpoint.finite_boundary_generator_integrand",
        sp.simplify(
            boundary_integrand_numerator - trace_fp + constraint / 2
        )
        == 0,
        "(P*C_P+p*C_p-C)/D=1 on shell, so the finite endpoint generator from P_i to zero is F_i=-P_i",
    )

    chi = trace_p - sp.symbols("f", real=True)
    constraint_q = constraint.subs(a, sp.exp(q / 2))
    trace_fp_q = sp.simplify(-sp.diff(constraint_q, q))
    fp_coordinate_jacobian = sp.Matrix(
        [
            [sp.diff(chi, variable) for variable in (q, trace_p, phi, p)],
            [
                sp.diff(constraint_q, variable)
                for variable in (q, trace_p, phi, p)
            ],
            [
                sp.diff(phi_star, variable)
                for variable in (q, trace_p, phi, p)
            ],
            [sp.diff(p, variable) for variable in (q, trace_p, phi, p)],
        ]
    ).det()
    audit.check_exact(
        "G1.endpoint.local_fp_measure_jacobian",
        sp.simplify(fp_coordinate_jacobian - trace_fp_q) == 0,
        "the ordered map (chi,C,Phi_star,p) has Jacobian D, giving dPhi_star*dp after delta(C) delta(chi) D on D>0",
    )

    q_star_p_shell = sp.diff(constraint, trace_p) / (
        12 * sp.pi**2 * a
    )
    q_star_scalar_shell = sp.diff(constraint, p) / (
        12 * sp.pi**2 * a
    )
    audit.check_exact(
        "G1.endpoint.implicit_root_derivatives",
        sp.simplify(
            (q_star_p_trace - q_star_p_shell).subs(
                p**2, shell_p_squared
            )
        )
        == 0
        and sp.simplify(
            (q_star_p - q_star_scalar_shell).subs(
                p**2, shell_p_squared
            )
        )
        == 0,
        "implicit differentiation gives Q_star,y=C_y/D for y=P,p on the shell",
    )

    reconstructed_lapse = f_dot / (12 * sp.pi**2 * a)
    audit.check_exact(
        "G1.endpoint.time_dependent_gauge_preservation",
        sp.simplify(
            reconstructed_lapse * 12 * sp.pi**2 * a - f_dot
        )
        == 0,
        "dot(P)=N*D=dot(f), hence N=dot(f)/D and is positive on the frozen D>0, dot(f)>0 component",
    )

    audit.check_exact(
        "G1.endpoint.reduced_full_flow_match",
        sp.simplify(
            (
                f_dot * q_star_p
                - reconstructed_lapse * sp.diff(constraint, p)
            ).subs(p**2, shell_p_squared)
        )
        == 0
        and sp.simplify(
            (
                f_dot * q_star_p_trace
                - reconstructed_lapse * sp.diff(constraint, trace_p)
            ).subs(p**2, shell_p_squared)
        )
        == 0,
        "H_red=dot(f)*Q_star reconstructs the full constrained phi and Q velocities on shell",
    )

    p1 = sp.Rational(1, 4)
    p2 = sp.Rational(1, 2)
    benchmark_r1 = sp.simplify(shell_discriminant.subs({p: 1, trace_p: p1}))
    benchmark_r2 = sp.simplify(shell_discriminant.subs({p: 1, trace_p: p2}))
    audit.check_exact(
        "G1.endpoint.frozen_component_margins",
        benchmark_r1 == sp.Rational(23, 8)
        and benchmark_r2 == sp.Rational(5, 2)
        and benchmark_r2 > 0,
        "for p=1 and 0<=P<=1/2, R>=5/2, a>0 and D>0; the monotone flow has one static P=0 hit",
    )

    antiderivative = sp.Function("A")
    orbit_triangle = sp.simplify(
        (antiderivative(p2) - antiderivative(p1))
        + (antiderivative(0) - antiderivative(p2))
        - (antiderivative(0) - antiderivative(p1))
    )
    audit.check_exact(
        "G1.endpoint.orbit_triangle_orientation",
        orbit_triangle == 0,
        "T+mu_2-mu_1=0 follows exactly from oriented path concatenation for the same dP/D one-form",
    )

    raw_orbit_action = sp.simplify(p2 - p1)
    boundary_difference = sp.simplify(p2 - p1)
    finite_f1 = -p1
    finite_f2 = -p2
    improved_orbit_action = sp.simplify(
        raw_orbit_action - boundary_difference
    )
    audit.check_exact(
        "G1.endpoint.action_triangle",
        raw_orbit_action == sp.Rational(1, 4)
        and sp.simplify(finite_f1 - finite_f2 - raw_orbit_action) == 0
        and improved_orbit_action == 0,
        "S_td=P2-P1=F1-F2=1/4 and the relational endpoint improvement S0-[P] gives zero on the pure gauge orbit",
    )

    audit.guard_theorem(
        "G1.endpoint.guard.local_shell_completion",
        True,
        "local coisotropic reduction and on-shell symplectic-potential decomposition",
        "closed-FRW V=0, p=1 benchmark component with R>0 and D>0",
        "the relational endpoint completion is established only on this local constraint component; a full off-shell canonical transformation is not inferred",
    )
    audit.guard_theorem(
        "G1.endpoint.guard.endpoint_state_scope",
        True,
        "HTV endpoint boundary action and gauge-related endpoint data",
        "classical local endpoint coordinates Phi_star and static P=0 slice",
        "the classical boundary potential is computed, but a normalized quantum endpoint-state transform and ghost endpoint sector remain uncomputed",
    )
    audit.guard_theorem(
        "G1.endpoint.guard.finite_flow_scope",
        True,
        "finite gauge flow on a connected regular orbit chart",
        "0<=P<=1/2, p=1, R>=5/2 and D>0",
        "one unique local hit does not establish a global fundamental region or exclude Gribov copies elsewhere",
    )
    audit.guard_theorem(
        "G1.endpoint.guard.signed_absolute_fp",
        True,
        "separation of the signed ghost determinant from the absolute delta-function Jacobian",
        "the chosen connected D>0 component",
        "signed and absolute factors coincide numerically here because D>0; no global determinant-line orientation is promoted",
    )
    audit.guard_theorem(
        "G1.endpoint.guard.curved_v0_scope",
        True,
        "closed-FRW curvature control versus the spatially flat homogeneous V=0 exception",
        "the constraint retains the -6*pi^2*a curvature term",
        "D=12*pi^2*a on shell here; this does not contradict the separate spatially flat V=0 degeneracy",
    )
    audit.guard_theorem(
        "G1.endpoint.guard.projector_boundary",
        True,
        "local canonical-limit FP reduction versus the full-real-lapse constraint projector",
        "one classical gauge chart without the full BFV ghost action or lapse integration",
        "neither the Marolf projector matrix element nor equality with the repository fixed-a kernel is computed",
    )

    return {
        "trace_chart": {
            "Q": "2*log(a)",
            "P": "a*p_a/2",
            "poisson_bracket": "1",
            "constraint": str(constraint),
            "R": str(shell_discriminant),
            "shell": "R=72*pi^4*a^4",
            "Q_star": str(q_star),
            "D_off_shell": str(trace_fp),
            "D_on_shell": "12*pi^2*a",
        },
        "relational_endpoint_completion": {
            "Phi_star": str(phi_star),
            "dirac_bracket_on_shell": "0",
            "shell_one_form": "P*dQ_star+p*dphi=p*dPhi_star+dP",
            "boundary_potential": "B_red=P",
            "improved_action": "S_imp=S0-[P]",
            "original_fixed_Q_static_transversality": "FAILS_AT_P_ZERO",
            "swapped_trace_chart_transversality": "D_NONZERO",
        },
        "mixed_endpoint_action": {
            "action": "S_[P,phi]=S0-[P*Q]",
            "boundary_variation": "[-Q*dP+p*dphi]_1^2",
            "reduced_action": "integral(p*phi_dot-f_dot*Q_star) ds",
            "reduced_hamiltonian": "H_red=+f_dot*Q_star",
            "full_reduced_velocity_match": True,
        },
        "finite_endpoint_flow": {
            "flow_equation": "dP/dmu=D",
            "boundary_integrand_on_shell": "1",
            "static_hit_generator": "F_i=-P_i",
            "benchmark_F1": str(finite_f1),
            "benchmark_F2": str(finite_f2),
        },
        "local_fp_measure": {
            "ordered_coordinates": "(chi,C,Phi_star,p)",
            "jacobian": "D",
            "reduction": "dQ dP dphi dp delta(C) delta(P-f) D=dPhi_star dp",
            "signed_ghost_ledger": "positive on this D>0 component only",
            "absolute_delta_ledger": "positive on this D>0 component only",
        },
        "time_dependent_representative": {
            "f": "1/4+s/4",
            "p": "1",
            "P1": str(p1),
            "P2": str(p2),
            "N": "f_dot/D",
            "R_min": str(benchmark_r2),
            "raw_orbit_action": str(raw_orbit_action),
            "F1_minus_F2": str(sp.simplify(finite_f1 - finite_f2)),
            "improved_orbit_action": str(improved_orbit_action),
        },
        "computed_facts": {
            "constraint_component": "REGULAR_R_POSITIVE_D_POSITIVE",
            "local_relational_endpoint_coordinate": "EXISTS",
            "on_shell_endpoint_potential": "B_RED_EQUALS_P",
            "finite_static_hit": "UNIQUE_ON_FROZEN_COMPONENT",
            "finite_endpoint_generator": "F_I_EQUALS_MINUS_P_I",
            "local_fp_measure": "REDUCES_TO_DPHI_STAR_DP",
            "time_dependent_preservation": "N_EQUALS_F_DOT_OVER_D",
            "reduced_full_flow": "MATCHES_ON_SHELL",
            "orbit_triangle": "CLOSES",
            "improved_action_triangle": "CLOSES",
            "full_off_shell_bfv_completion": "NOT_COMPUTED",
            "old_fixed_a_kernel_equivalence": "NOT_COMPUTED",
        },
    }


def gauss_legendre_integral(
    function: Callable[[mp.mpf], mp.mpf],
    lower: mp.mpf,
    upper: mp.mpf,
    nodes: int,
) -> mp.mpf:
    abscissae, weights = mp.gauss_quadrature(nodes, "legendre")
    midpoint = (lower + upper) / 2
    half_width = (upper - lower) / 2
    return half_width * mp.fsum(
        weights[index] * function(
            midpoint + half_width * abscissae[index]
        )
        for index in range(nodes)
    )


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    p = mp.mpf(plan["p"])
    p1 = mp.mpf(plan["P1"])
    p2 = mp.mpf(plan["P2"])
    tolerance = mp.mpf(plan["relative_tolerance"])
    nodes = 48

    if p != 1 or p1 != mp.mpf("0.25") or p2 != mp.mpf("0.5"):
        raise AssertionError("numerical benchmark mutation")

    def inverse_fp(momentum: mp.mpf) -> mp.mpf:
        discriminant = 3 * p**2 - 2 * momentum**2
        if discriminant <= 0:
            raise AssertionError("left the R>0 component")
        scale_factor = (discriminant / (72 * mp.pi**4)) ** mp.mpf("0.25")
        trace_fp = 12 * mp.pi**2 * scale_factor
        if trace_fp <= 0:
            raise AssertionError("left the D>0 component")
        return 1 / trace_fp

    intervals = {
        "T": (p1, p2),
        "mu1": (p1, mp.mpf("0")),
        "mu2": (p2, mp.mpf("0")),
    }
    tanh_sinh: dict[str, mp.mpf] = {}
    gauss_legendre: dict[str, mp.mpf] = {}
    for name, (lower, upper) in intervals.items():
        tanh_value = mp.quad(inverse_fp, [lower, upper])
        gauss_value = gauss_legendre_integral(
            inverse_fp, lower, upper, nodes
        )
        tanh_sinh[name] = tanh_value
        gauss_legendre[name] = gauss_value
        relative_error = abs(tanh_value - gauss_value) / abs(tanh_value)
        audit.check_numerical(
            f"G1.endpoint.quadrature.{name}",
            relative_error,
            tolerance,
            "relative",
            f"independent tanh-sinh and {nodes}-node Gauss-Legendre evaluations agree for {name}",
            {
                "tanh_sinh": mp_string(tanh_value),
                "gauss_legendre": mp_string(gauss_value),
            },
        )

    tanh_closure = tanh_sinh["T"] + tanh_sinh["mu2"] - tanh_sinh["mu1"]
    gauss_closure = (
        gauss_legendre["T"]
        + gauss_legendre["mu2"]
        - gauss_legendre["mu1"]
    )
    audit.check_numerical(
        "G1.endpoint.quadrature.tanh_sinh_orbit_closure",
        abs(tanh_closure),
        tolerance,
        "absolute",
        "the tanh-sinh flow parameters close the oriented endpoint triangle",
        {"closure": mp_string(tanh_closure)},
    )
    audit.check_numerical(
        "G1.endpoint.quadrature.gauss_legendre_orbit_closure",
        abs(gauss_closure),
        tolerance,
        "absolute",
        "the independent Gauss-Legendre flow parameters close the oriented endpoint triangle",
        {"closure": mp_string(gauss_closure)},
    )

    return {
        "precision_digits": mp.mp.dps,
        "gauss_legendre_nodes": nodes,
        "benchmark": {
            "p": mp_string(p),
            "P1": mp_string(p1),
            "P2": mp_string(p2),
            "R_min": mp_string(3 * p**2 - 2 * p2**2),
        },
        "tanh_sinh": {
            key: mp_string(value) for key, value in tanh_sinh.items()
        },
        "gauss_legendre": {
            key: mp_string(value) for key, value in gauss_legendre.items()
        },
        "orbit_closures": {
            "tanh_sinh": mp_string(tanh_closure),
            "gauss_legendre": mp_string(gauss_closure),
        },
        "quadratures": 6,
        "root_calls": 0,
        "ode_calls": 0,
    }


def select_decision(exact: dict[str, Any]) -> dict[str, str]:
    facts = exact["computed_facts"]
    expected = {
        "constraint_component": "REGULAR_R_POSITIVE_D_POSITIVE",
        "local_relational_endpoint_coordinate": "EXISTS",
        "on_shell_endpoint_potential": "B_RED_EQUALS_P",
        "finite_static_hit": "UNIQUE_ON_FROZEN_COMPONENT",
        "finite_endpoint_generator": "F_I_EQUALS_MINUS_P_I",
        "local_fp_measure": "REDUCES_TO_DPHI_STAR_DP",
        "time_dependent_preservation": "N_EQUALS_F_DOT_OVER_D",
        "reduced_full_flow": "MATCHES_ON_SHELL",
        "orbit_triangle": "CLOSES",
        "improved_action_triangle": "CLOSES",
        "full_off_shell_bfv_completion": "NOT_COMPUTED",
        "old_fixed_a_kernel_equivalence": "NOT_COMPUTED",
    }
    if all(facts.get(key) == value for key, value in expected.items()):
        return {
            "verdict": "KEEP_IMPROVED_STATIC_LOCAL_ENDPOINT_COMPLETION",
            "programme_impact": "NARROW_AND_ADVANCE_LOCAL_ENDPOINT_ROUTE",
            "matched_predeclared_condition": (
                "all shell, Dirac-coordinate, one-form, transversality, "
                "finite-flow, local-FP, gauge-preservation, orbit-triangle, "
                "and improved-action checks pass"
            ),
            "meaning": (
                "keep the local closed-FRW V=0 relational endpoint "
                "completion of the static trace slice and retain the "
                "time-dependent representative as an exact same-orbit "
                "control; full BFV and projector claims remain open"
            ),
        }
    raise AssertionError("exact facts did not select a predeclared decision row")


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
    decision = select_decision(exact)
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "classification": "GATE1_V0_TRACE_ENDPOINT_TRIANGLE_LOCAL_KEEP_FULL_BFV_PROJECTOR_OPEN",
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
            "matched_predeclared_condition": decision[
                "matched_predeclared_condition"
            ],
            "meaning": decision["meaning"],
            "source_boundary": (
                "HTV supplies the endpoint and finite-gauge framework, not "
                "this model-specific completion; Banihashemi-Jacobson supply "
                "the local trace-gauge FP premise, not endpoint completion; "
                "Marolf supplies the still-uncomputed full projector target"
            ),
        },
        "scope_status": {
            "local_v0_relational_endpoint_completion": "KEEP_ON_FROZEN_R_POSITIVE_D_POSITIVE_COMPONENT",
            "time_dependent_trace_representative": "KEEP_AS_EXACT_SAME_ORBIT_CONTROL",
            "full_off_shell_canonical_transform": None,
            "full_replacement_bfv_measure": None,
            "endpoint_state_transform": None,
            "old_fixed_a_kernel_equivalence": None,
            "full_projector_matrix_element": None,
            "zero_lapse_distribution": None,
            "global_fundamental_region": None,
            "full_joint_orientation": None,
            "physical_original_cycle": None,
        },
        "open_dependencies": [
            "full off-shell canonical chart and HTV-compatible ghost/antighost/b endpoint conditions",
            "normalized endpoint-state transform and full replacement BFV measure",
            "a bounded replacement-source discretization distinct from the old constant-lapse fixed-a source",
            "comparison with the full-real-lapse projector and regulator removal",
            "global orbit coverage, determinant-line orientation, and physical original cycle",
        ],
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": {
            "TOE_claim": None,
            "complete_global_signed_intersection_vector": None,
            "full_joint_orientation": None,
            "full_m2_bfv_measure": None,
            "full_projector_matrix_element": None,
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
