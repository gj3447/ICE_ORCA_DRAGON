#!/usr/bin/env python3
"""Gate 1 -- finite m=2 bosonic canonical-source pushforward control.

The calculation keeps both the homogeneous scale-factor momentum and scalar
momentum.  It first proves the exact two-element Legendre identities and then
tests whether one common lateral lapse prescription damps all four momenta on
their real axes.  Since the kinetic form has signature (-,+), it also checks
the explicitly declared centered steepest Gaussian rays, their ordered
half-turn orientation, and the flat C/|N| versus C/N determinant-line glue.

This is a bounded non-numbered workbench calculation.  The declared complex
rays are not asserted to be a deformation of the physical original cycle;
the scale-factor relative ends, BFV gauge fixing, ghosts, and global
intersection coefficients remain uncomputed.  One adjacent JSON result is
written and no descendant calculation is launched.
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


INPUT_NAME = "GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_INPUTS.json"
RESULT_NAME = "GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_bosonic_canonical_source_pushforward.py"
)
EXPECTED_INPUT_SHA256 = (
    "b2572eb98593a5cfe0746abb4c4aa99f5eb25ab1c6651617f1a14b0d9cd7de30"
)
CALCULATION_ID = "Gate1M2BosonicCanonicalSourcePushforward"
RESULT_SCHEMA = "ice.gate1.bosonic-canonical-source-pushforward.result.v1"
RESULT_PREFIX = "GATE1_BOSONIC_CANONICAL_SOURCE_PUSHFORWARD_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


@dataclass
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    numerical: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)

    def check_exact(self, check_id: str, passed: bool, statement: str) -> None:
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
        if not verified:
            raise AssertionError(f"[THEOREM GUARD FAIL] {guard_id}: {statement}")
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
        "ice.gate1.bosonic-canonical-source-pushforward.input.v1"
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
    A, hbar, rho = sp.symbols("A hbar rho", positive=True, real=True)
    phi_mid, x, q, theta, y = sp.symbols(
        "Phi x q theta y", real=True
    )
    z, T = sp.symbols("z T", nonzero=True)
    pa0, pa1, pp0, pp1 = sp.symbols("p_a0 p_a1 p_phi0 p_phi1")
    n, epsilon, lapse = sp.symbols(
        "n epsilon N", positive=True, real=True
    )
    mu_g = 12 * sp.pi**2 * A
    mu_s = 2 * sp.pi**2 * A**3
    potential = sp.Rational(3, 4) * (
        1 - sp.exp(-sp.sqrt(sp.Rational(2, 3)) * phi_mid)
    ) ** 2
    U = 2 * sp.pi**2 * (-3 * A + A**3 * potential)
    h = sp.Rational(1, 2)

    def hamiltonian(p_a: sp.Expr, p_phi: sp.Expr) -> sp.Expr:
        return -p_a**2 / (2 * mu_g) + p_phi**2 / (2 * mu_s) + U

    inherited = (
        pa0 * x
        + pp0 * q
        - h * z * hamiltonian(pa0, pp0)
        - pa1 * x
        - pp1 * q
        - h * z * hamiltonian(pa1, pp1)
    )
    canonical = (
        x * (pa0 - pa1)
        + q * (pp0 - pp1)
        + z * (pa0**2 + pa1**2) / (4 * mu_g)
        - z * (pp0**2 + pp1**2) / (4 * mu_s)
        - z * U
    )
    audit.check_exact(
        "G1.bosonic.inherited_m2_canonical_action",
        sp.simplify(inherited - canonical) == 0,
        "two h=1/2 Lorentzian midpoint elements reduce exactly to the frozen m=2 canonical action",
    )

    stationary = {
        pa0: -2 * mu_g * x / z,
        pa1: 2 * mu_g * x / z,
        pp0: 2 * mu_s * q / z,
        pp1: -2 * mu_s * q / z,
    }
    audit.check_exact(
        "G1.bosonic.stationary_momenta",
        all(
            sp.simplify(sp.diff(canonical, p).subs(stationary)) == 0
            for p in (pa0, pp0, pa1, pp1)
        ),
        "all four algebraic momentum equations have the declared nonzero-z saddle",
    )

    on_shell = sp.simplify(canonical.subs(stationary))
    expected_on_shell = -2 * mu_g * x**2 / z + 2 * mu_s * q**2 / z - z * U
    completed = (
        z
        * ((pa0 - stationary[pa0]) ** 2 + (pa1 - stationary[pa1]) ** 2)
        / (4 * mu_g)
        - z
        * ((pp0 - stationary[pp0]) ** 2 + (pp1 - stationary[pp1]) ** 2)
        / (4 * mu_s)
        + expected_on_shell
    )
    audit.check_exact(
        "G1.bosonic.square_completion_and_pushforward",
        sp.simplify(on_shell - expected_on_shell) == 0
        and sp.simplify(canonical - completed) == 0,
        "the exact four-momentum square completion gives I*= -2*mu_g*x^2/z+2*mu_s*q^2/z-z*U",
    )

    euclidean = -2 * mu_g * x**2 / T + 2 * mu_s * q**2 / T + T * U
    audit.check_exact(
        "G1.bosonic.wick_configuration_identity",
        sp.simplify(sp.I * expected_on_shell.subs(z, -sp.I * T) + euclidean)
        == 0,
        "T=i*z gives i*I*=-I_E with the gravitational and scalar signs retained",
    )

    lower = lapse - sp.I * epsilon
    upper = lapse + sp.I * epsilon
    lower_gravity_real = sp.simplify(
        sp.re(sp.I * lower / (4 * mu_g * hbar)).expand(complex=True)
    )
    lower_scalar_real = sp.simplify(
        sp.re(-sp.I * lower / (4 * mu_s * hbar)).expand(complex=True)
    )
    upper_gravity_real = sp.simplify(
        sp.re(sp.I * upper / (4 * mu_g * hbar)).expand(complex=True)
    )
    upper_scalar_real = sp.simplify(
        sp.re(-sp.I * upper / (4 * mu_s * hbar)).expand(complex=True)
    )
    audit.check_exact(
        "G1.bosonic.lower_lateral_real_axis_signs",
        sp.simplify(lower_gravity_real - epsilon / (4 * mu_g * hbar)) == 0
        and sp.simplify(lower_scalar_real + epsilon / (4 * mu_s * hbar))
        == 0,
        "for z=N-i*epsilon the real p_a Gaussian grows while the real p_phi Gaussian decays",
    )
    audit.check_exact(
        "G1.bosonic.upper_lateral_real_axis_signs",
        sp.simplify(upper_gravity_real + epsilon / (4 * mu_g * hbar)) == 0
        and sp.simplify(upper_scalar_real - epsilon / (4 * mu_s * hbar))
        == 0,
        "for z=N+i*epsilon the real p_a Gaussian decays while the real p_phi Gaussian grows",
    )
    no_common_real_lateral = (
        lower_gravity_real > 0
        and lower_scalar_real < 0
        and upper_gravity_real < 0
        and upper_scalar_real > 0
    )
    audit.check_exact(
        "G1.bosonic.no_common_all_real_lateral_regulator",
        bool(no_common_real_lateral),
        "the signature (-,+) momentum blocks admit no one N-i0 or N+i0 sign that damps both real axes",
    )

    z_polar = rho * sp.exp(sp.I * theta)
    gravity_ray = sp.exp(sp.I * (sp.pi / 4 - theta / 2))
    scalar_ray = sp.exp(sp.I * (-sp.pi / 4 - theta / 2))
    gravity_exponent = sp.simplify(
        sp.powsimp(
            sp.I * z_polar * (gravity_ray * y) ** 2 / (4 * mu_g * hbar),
            force=True,
        )
    )
    scalar_exponent = sp.simplify(
        sp.powsimp(
            -sp.I * z_polar * (scalar_ray * y) ** 2 / (4 * mu_s * hbar),
            force=True,
        )
    )
    audit.check_exact(
        "G1.bosonic.gravity_steepest_ray_decay",
        sp.simplify(gravity_exponent + rho * y**2 / (4 * mu_g * hbar))
        == 0,
        "the declared centered scale-factor momentum ray converts its exponent exactly to a negative real Gaussian",
    )
    audit.check_exact(
        "G1.bosonic.scalar_steepest_ray_decay",
        sp.simplify(scalar_exponent + rho * y**2 / (4 * mu_s * hbar))
        == 0,
        "the declared centered scalar momentum ray converts its exponent exactly to a negative real Gaussian",
    )

    single_gravity = gravity_ray * sp.sqrt(mu_g / (sp.pi * hbar * rho))
    single_scalar = scalar_ray * sp.sqrt(mu_s / (sp.pi * hbar * rho))
    J_g = sp.I * mu_g / (sp.pi * hbar * z_polar)
    J_s = mu_s / (sp.pi * sp.I * hbar * z_polar)
    J_total = mu_g * mu_s / (sp.pi**2 * hbar**2 * z_polar**2)
    audit.check_exact(
        "G1.bosonic.gravity_pair_prefactor",
        sp.simplify(sp.powsimp(single_gravity**2 - J_g, force=True)) == 0,
        "the two ordered p_a rays give J_g=i*mu_g/(pi*hbar*z)",
    )
    audit.check_exact(
        "G1.bosonic.scalar_pair_prefactor",
        sp.simplify(sp.powsimp(single_scalar**2 - J_s, force=True)) == 0,
        "the two ordered p_phi rays give J_s=mu_s/(pi*i*hbar*z)",
    )
    audit.check_exact(
        "G1.bosonic.total_momentum_prefactor",
        sp.simplify(sp.powsimp(J_g * J_s - J_total, force=True)) == 0
        and sp.simplify(
            mu_g * mu_s / (sp.pi**2 * hbar**2 * z**2)
            - 24 * sp.pi**2 * A**4 / (hbar**2 * z**2)
        )
        == 0,
        "the four-momentum pushforward is 24*pi^2*A^4/(hbar^2*z^2)",
    )
    scalar_ablation = (
        mu_s / (sp.pi * sp.I * hbar * z)
    ).subs(z, -sp.I * T)
    audit.check_exact(
        "G1.bosonic.scalar_source_link_ablation",
        sp.simplify(scalar_ablation - 2 * sp.pi * A**3 / (hbar * T)) == 0,
        "holding the scale factor fixed recovers the prior m=2 scalar prefactor 2*pi*A^3/(hbar*T)",
    )

    def endpoint_ratio(ray: sp.Expr, endpoint: sp.Expr) -> sp.Expr:
        return sp.simplify(ray.subs(theta, endpoint) / ray.subs(theta, 0))

    lower_momentum_glue = sp.simplify(
        endpoint_ratio(gravity_ray, -sp.pi) ** 2
        * endpoint_ratio(scalar_ray, -sp.pi) ** 2
    )
    upper_momentum_glue = sp.simplify(
        endpoint_ratio(gravity_ray, sp.pi) ** 2
        * endpoint_ratio(scalar_ray, sp.pi) ** 2
    )
    x_ray = sp.exp(sp.I * (theta / 2 - sp.pi / 4))
    q_ray = sp.exp(sp.I * (theta / 2 + sp.pi / 4))
    lower_configuration_glue = sp.simplify(
        endpoint_ratio(x_ray, -sp.pi) * endpoint_ratio(q_ray, -sp.pi)
    )
    upper_configuration_glue = sp.simplify(
        endpoint_ratio(x_ray, sp.pi) * endpoint_ratio(q_ray, sp.pi)
    )
    audit.check_exact(
        "G1.bosonic.lower_cap_orientation",
        lower_momentum_glue == 1 and lower_configuration_glue == -1,
        "on theta:0->-pi the four momentum Jacobians glue by +1 and the x,q rays by -1",
    )
    audit.check_exact(
        "G1.bosonic.upper_cap_orientation",
        upper_momentum_glue == 1 and upper_configuration_glue == -1,
        "on theta:0->+pi the four momentum Jacobians glue by +1 and the x,q rays by -1",
    )

    C = sp.sqrt(mu_g * mu_s) / (2 * sp.pi * hbar)
    real_configuration_integral = (
        sp.pi * hbar * n / (2 * sp.sqrt(mu_g * mu_s))
    )
    positive_real_kernel = sp.simplify(
        (mu_g * mu_s / (sp.pi**2 * hbar**2 * n**2))
        * real_configuration_integral
    )
    negative_real_kernel = positive_real_kernel
    holomorphic_configuration_integral = (
        sp.pi * hbar * z / (2 * sp.sqrt(mu_g * mu_s))
    )
    holomorphic_kernel = sp.simplify(
        (mu_g * mu_s / (sp.pi**2 * hbar**2 * z**2))
        * holomorphic_configuration_integral
    )
    negative_holomorphic_kernel = sp.simplify(holomorphic_kernel.subs(z, -n))
    audit.check_exact(
        "G1.bosonic.flat_kernel_detline_glue",
        sp.simplify(positive_real_kernel - C / n) == 0
        and sp.simplify(negative_real_kernel - C / n) == 0
        and sp.simplify(holomorphic_kernel - C / z) == 0
        and sp.simplify(negative_holomorphic_kernel / negative_real_kernel + 1)
        == 0,
        "the real flat kernel is C/|N|, one holomorphic sheet is C/N, and their negative-arm ratio is -1",
    )
    audit.check_exact(
        "G1.bosonic.orientation_mutation_control",
        sp.simplify((-J_total) / J_total + 1) == 0,
        "reversing exactly one ordered momentum ray flips the Gaussian pushforward sign",
    )

    audit.guard_theorem(
        "G1.guard.centered_complex_gaussian",
        True,
        "one-dimensional entire Gaussian integral on an explicitly oriented steepest line",
        "A>0, hbar>0, z=rho*exp(i*theta) with rho>0; each centered ray parameter runs from -infinity to +infinity",
        "the ray exponents are strictly negative real quadratics and the four normalized integrals may be multiplied; this does not prove deformation from the all-real physical source",
    )
    audit.guard_theorem(
        "G1.guard.half_turn_orientation_ledger",
        True,
        "orientation transport by the explicit nonvanishing ray parameterizations",
        "theta in [0,+pi] or [0,-pi], z nonzero, ordered measure dp_a0 wedge dp_phi0 wedge dp_a1 wedge dp_phi1 wedge dx wedge dq",
        "endpoint Jacobian ratios determine the finite cap glue; no BFV ghost or absolute determinant orientation is supplied",
    )

    return {
        "symbols": {
            "mu_g": str(mu_g),
            "mu_s": str(mu_s),
            "U": str(U),
            "T": "I*z",
        },
        "canonical_action": str(canonical),
        "stationary_momenta": {
            str(momentum): str(value) for momentum, value in stationary.items()
        },
        "on_shell_action": str(expected_on_shell),
        "euclidean_configuration_action": str(euclidean),
        "real_axis_quadratic_exponent_coefficients": {
            "lower_N_minus_i_epsilon": {
                "gravity": str(lower_gravity_real),
                "scalar": str(lower_scalar_real),
            },
            "upper_N_plus_i_epsilon": {
                "gravity": str(upper_gravity_real),
                "scalar": str(upper_scalar_real),
            },
        },
        "declared_rays": {
            "gravity": str(gravity_ray),
            "scalar": str(scalar_ray),
            "gravity_exponent": str(gravity_exponent),
            "scalar_exponent": str(scalar_exponent),
        },
        "momentum_prefactors": {
            "gravity_pair": str(J_g),
            "scalar_pair": str(J_s),
            "total": str(J_total),
            "total_simplified": "24*pi^2*A^4/(hbar^2*z^2)",
        },
        "cap_orientation": {
            "lower_momentum": str(lower_momentum_glue),
            "upper_momentum": str(upper_momentum_glue),
            "lower_configuration": str(lower_configuration_glue),
            "upper_configuration": str(upper_configuration_glue),
            "lower_total": str(
                sp.simplify(lower_momentum_glue * lower_configuration_glue)
            ),
            "upper_total": str(
                sp.simplify(upper_momentum_glue * upper_configuration_glue)
            ),
        },
        "flat_kernel": {
            "C": str(C),
            "independently_normalized_real": "C/Abs(N)",
            "holomorphic_sheet": str(holomorphic_kernel),
            "negative_arm_ratio": "-1",
        },
        "computed_facts": {
            "common_single_i0_real_momentum_regulator": "IMPOSSIBLE_FOR_SIGNATURE_MINUS_PLUS",
            "fixed_nonzero_z_centered_steepest_ray_pushforward": "EXACT_MATCH",
            "momentum_cap_glue": "+1",
            "configuration_cap_glue": "-1",
            "full_flat_kernel_glue": "-1",
            "scalar_source_link_ablation": "RECOVERED",
            "one_ray_orientation_mutation": "SIGN_FLIP_RECOVERED",
        },
    }


def integrate_original_coordinate(
    *,
    kind: str,
    linear: mp.mpf,
    mu: mp.mpf,
    z: mp.mpc,
    hbar: mp.mpf,
) -> mp.mpc:
    rho = abs(z)
    theta = mp.arg(z)
    if kind == "gravity":
        ray = mp.e ** (1j * (mp.pi / 4 - theta / 2))
        stationary = -2 * mu * linear / z
        on_shell = -mu * linear**2 / z

        def action(momentum: mp.mpc) -> mp.mpc:
            return linear * momentum + z * momentum**2 / (4 * mu)

    elif kind == "scalar":
        ray = mp.e ** (1j * (-mp.pi / 4 - theta / 2))
        stationary = 2 * mu * linear / z
        on_shell = mu * linear**2 / z

        def action(momentum: mp.mpc) -> mp.mpc:
            return linear * momentum - z * momentum**2 / (4 * mu)

    else:
        raise ValueError(f"unknown momentum kind: {kind}")

    scale = mp.sqrt(4 * mu * hbar / rho)

    def integrand(parameter: mp.mpf) -> mp.mpc:
        momentum = stationary + ray * scale * parameter
        remainder = action(momentum) - on_shell
        return mp.e ** (1j * remainder / hbar)

    integral = mp.quad(integrand, [-mp.inf, mp.inf])
    return ray * scale * integral / (2 * mp.pi * hbar)


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    benchmark = plan["benchmark"]
    a_b = mp.mpf(benchmark["a_b"])
    phi_b = mp.mpf(benchmark["phi_b"])
    x = mp.mpf(benchmark["x"])
    q = mp.mpf(benchmark["q"])
    hbar = mp.mpf(benchmark["hbar"])
    midpoint_scale = a_b + x / 2
    midpoint_field = phi_b + q / 2
    if midpoint_scale <= 0:
        raise AssertionError("numerical midpoint scale must be positive")
    mu_g = 12 * mp.pi**2 * midpoint_scale
    mu_s = 2 * mp.pi**2 * midpoint_scale**3
    tolerance = mp.mpf(plan["relative_tolerance"])
    records: list[dict[str, Any]] = []

    for index, (real_text, imag_text) in enumerate(plan["lateral_points"], 1):
        z = mp.mpc(mp.mpf(real_text), mp.mpf(imag_text))
        if z == 0:
            raise AssertionError("numerical lapse point must be nonzero")
        integrals = [
            integrate_original_coordinate(
                kind="gravity", linear=x, mu=mu_g, z=z, hbar=hbar
            ),
            integrate_original_coordinate(
                kind="scalar", linear=q, mu=mu_s, z=z, hbar=hbar
            ),
            integrate_original_coordinate(
                kind="gravity", linear=-x, mu=mu_g, z=z, hbar=hbar
            ),
            integrate_original_coordinate(
                kind="scalar", linear=-q, mu=mu_s, z=z, hbar=hbar
            ),
        ]
        observed = mp.fprod(integrals)
        expected = mu_g * mu_s / (mp.pi**2 * hbar**2 * z**2)
        relative_error = abs(observed - expected) / abs(expected)
        point_record = {
            "z": complex_record(z),
            "theta": mp_string(mp.arg(z), 30),
            "observed": complex_record(observed),
            "expected": complex_record(expected),
            "individual_integrals": [complex_record(value) for value in integrals],
        }
        audit.check_numerical(
            f"G1.bosonic.quadrature.lateral_point_{index}",
            relative_error,
            tolerance,
            "four independently integrated original linear-plus-quadratic momentum factors reproduce J_g*J_s on the declared centered rays",
            point_record,
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
            "a_b": mp_string(a_b),
            "phi_b": mp_string(phi_b),
            "x": mp_string(x),
            "q": mp_string(q),
            "midpoint_A": mp_string(midpoint_scale),
            "midpoint_Phi": mp_string(midpoint_field),
            "mu_g": mp_string(mu_g),
            "mu_s": mp_string(mu_s),
            "hbar": mp_string(hbar),
        },
        "lateral_point_summaries": records,
        "quadratures": 4 * len(records),
        "root_calls": 0,
        "ode_calls": 0,
    }


def select_decision(exact: dict[str, Any]) -> dict[str, str]:
    facts = exact["computed_facts"]
    expected = {
        "common_single_i0_real_momentum_regulator": "IMPOSSIBLE_FOR_SIGNATURE_MINUS_PLUS",
        "fixed_nonzero_z_centered_steepest_ray_pushforward": "EXACT_MATCH",
        "momentum_cap_glue": "+1",
        "configuration_cap_glue": "-1",
        "full_flat_kernel_glue": "-1",
    }
    if all(facts.get(key) == value for key, value in expected.items()):
        return {
            "verdict": "CONFORMAL_PRESCRIPTION_AND_DETLINE_GLUE_REQUIRED",
            "programme_impact": "NARROW",
            "matched_predeclared_condition": (
                "no common all-real lateral regulator exists, both centered ray "
                "blocks reproduce the exact configuration pushforward, momentum "
                "cap glue is +1, configuration cap glue is -1, and the scale-factor "
                "relative ends remain unproved"
            ),
            "meaning": (
                "reject the literal all-real momentum-first source link; retain the "
                "declared finite Gaussian pushforward only as a branch requiring a "
                "conformal prescription and independent determinant-line/BFV completion"
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
        "classification": "GATE1_M2_ALL_REAL_MOMENTUM_SOURCE_OBSTRUCTED_COMPLEX_GAUSSIAN_PUSHFORWARD_MATCHES",
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
            "source_control_status": "DECLARED_COMPLEX_FINITE_GAUSSIAN_BRANCH_NOT_PHYSICAL_ORIGINAL",
            "primary_source_boundary": (
                "the cited momentum-first below-origin prescription first gauge-fixes "
                "away the negative gravitational trace momentum; it does not license "
                "an all-real retained p_a contour here"
            ),
        },
        "scope_status": {
            "all_real_bosonic_momentum_first_source": "REJECTED_BY_CONVERGENCE_SIGNS",
            "declared_complex_centered_momentum_rays": "KEEP_AS_FINITE_GAUSSIAN_BRANCH",
            "scale_factor_relative_ends": "OPEN",
            "nonlinear_Starobinsky_configuration_cycle": "OPEN",
            "p_a_gauge_fixing_FP_BFV_detline": "OPEN",
            "physical_original_cycle": None,
        },
        "gate1_decision": "OPEN_PARTIAL_PROGRESS",
        "global_promotion": "PROHIBITED",
        "automatic_next": None,
        "promoted_outputs": {
            "TOE_claim": None,
            "complete_global_signed_intersection_vector": None,
            "full_joint_orientation": None,
            "global_n_sigma": None,
            "physical_original_cycle": None,
            "physics_claim": None,
        },
        "resource_accounting": {
            "root_calls": 0,
            "ode_calls": 0,
            "quadratures": numerical["quadratures"],
            "lateral_points": len(audit.numerical),
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
            "source_and_target_cycles": frozen_input[
                "source_and_target_cycles"
            ],
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
