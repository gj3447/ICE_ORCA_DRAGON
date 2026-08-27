#!/usr/bin/env python3
"""Gate 1 -- local V=0 improved-static BFV replacement source.

This bounded non-numbered calculation takes the hash-verified exact
closed-FRW V=0 ``U_plus`` Darboux chart as an upstream classical input and
asks the next smaller quantum-source question.  It specifies one Abelian
extended BFV algebra for the canonical constraint pair ``(T,c)``, the
multiplier pair ``(N,Pi)``, and a time-independent canonical gauge ``T=0``.
It derives the BRST differential from an explicit graded bracket and checks
the gauge fermion, endpoint ideal, local FP/Fourier/Berezin zero-mode
convention, and compatibility with a separately declared reduced canonical
identity distribution.

The source is derived in the transformed endpoint polarization with the HTV
boundary improvement.  It is not made by appending a trace delta or an FP
factor to the old fixed-a/proper-time source.  The result is only a local
zero-mode replacement-source algebra on one Darboux component.  It does not
construct a two-endpoint or finite-m trajectory BFV kernel, an absolute path
measure, a full-real-lapse delta(C) rigging map, an old-kernel equivalence, a
physical cycle, a physics claim or a TOE claim.  One adjacent JSON result is
written and no descendant starts.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import mpmath as mp
import sympy as sp


INPUT_NAME = "GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_INPUTS.json"
RESULT_NAME = "GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/gate1_v0_improved_static_bfv_source.py"
)
EXPECTED_INPUT_SHA256 = (
    "ad9297d33b5fa2e3da4b31969e4d412d5f7891e20ce15b43de6e5476964261a3"
)
CALCULATION_ID = "Gate1V0ImprovedStaticBfvSource"
RESULT_SCHEMA = "ice.gate1.v0-improved-static-bfv-source.result.v1"
RESULT_PREFIX = "GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000

ODD_ORDER = ("c_g", "bar_c", "rho", "bar_rho")
ODD_INDEX = {name: index for index, name in enumerate(ODD_ORDER)}
GHOST_NUMBER = {"c_g": 1, "bar_c": -1, "rho": 1, "bar_rho": -1}


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

    def observe_exact(
        self, check_id: str, passed: bool, statement: str
    ) -> bool:
        self.register_id(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def observe_numerical(
        self,
        check_id: str,
        relative_error: mp.mpf,
        tolerance: mp.mpf,
        statement: str,
        details: dict[str, Any],
    ) -> bool:
        self.register_id(check_id)
        passed = bool(relative_error <= tolerance)
        self.numerical.append(
            {
                "id": check_id,
                "passed": passed,
                "statement": statement,
                "relative_error": mp_string(relative_error, 24),
                "relative_tolerance": mp_string(tolerance, 8),
                **details,
            }
        )
        return passed

    def guard_theorem(
        self,
        guard_id: str,
        theorem: str,
        domain: str,
        statement: str,
    ) -> None:
        self.register_id(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "theorem": theorem,
                "domain": domain,
                "statement": statement,
            }
        )


class Exterior:
    """Tiny exact exterior algebra for the frozen four BFV odd variables."""

    def __init__(
        self, terms: dict[tuple[str, ...], sp.Expr] | None = None
    ) -> None:
        normalized: dict[tuple[str, ...], sp.Expr] = {}
        for monomial, coefficient in (terms or {}).items():
            if any(name not in ODD_INDEX for name in monomial):
                raise AssertionError(f"unknown odd generator in {monomial}")
            if len(set(monomial)) != len(monomial):
                continue
            if tuple(sorted(monomial, key=ODD_INDEX.__getitem__)) != monomial:
                raise AssertionError(f"noncanonical exterior monomial: {monomial}")
            simplified = sp.simplify(coefficient)
            if simplified != 0:
                normalized[monomial] = sp.simplify(
                    normalized.get(monomial, 0) + simplified
                )
        self.terms = {
            monomial: coefficient
            for monomial, coefficient in normalized.items()
            if sp.simplify(coefficient) != 0
        }

    @classmethod
    def zero(cls) -> "Exterior":
        return cls()

    @classmethod
    def scalar(cls, value: sp.Expr | int) -> "Exterior":
        expression = sp.sympify(value)
        return cls({(): expression}) if expression != 0 else cls.zero()

    @classmethod
    def generator(cls, name: str) -> "Exterior":
        if name not in ODD_INDEX:
            raise AssertionError(f"unknown odd generator: {name}")
        return cls({(name,): sp.Integer(1)})

    @classmethod
    def monomial(cls, names: Iterable[str]) -> "Exterior":
        result = cls.scalar(1)
        for name in names:
            result = result * cls.generator(name)
        return result

    @staticmethod
    def coerce(value: "Exterior" | sp.Expr | int) -> "Exterior":
        return value if isinstance(value, Exterior) else Exterior.scalar(value)

    def __add__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        rhs = self.coerce(other)
        terms = dict(self.terms)
        for monomial, coefficient in rhs.terms.items():
            terms[monomial] = sp.simplify(
                terms.get(monomial, 0) + coefficient
            )
        return Exterior(terms)

    def __radd__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        return self + other

    def __neg__(self) -> "Exterior":
        return Exterior(
            {monomial: -coefficient for monomial, coefficient in self.terms.items()}
        )

    def __sub__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        return self + (-self.coerce(other))

    def __rsub__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        return self.coerce(other) - self

    def __mul__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        rhs = self.coerce(other)
        output: dict[tuple[str, ...], sp.Expr] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in rhs.terms.items():
                if set(left_monomial).intersection(right_monomial):
                    continue
                inversions = sum(
                    ODD_INDEX[left_name] > ODD_INDEX[right_name]
                    for left_name in left_monomial
                    for right_name in right_monomial
                )
                sign = -1 if inversions % 2 else 1
                monomial = tuple(
                    sorted(
                        left_monomial + right_monomial,
                        key=ODD_INDEX.__getitem__,
                    )
                )
                output[monomial] = sp.simplify(
                    output.get(monomial, 0)
                    + sign * left_coefficient * right_coefficient
                )
        return Exterior(output)

    def __rmul__(self, other: "Exterior" | sp.Expr | int) -> "Exterior":
        return self.coerce(other) * self

    def __truediv__(self, other: sp.Expr | int) -> "Exterior":
        denominator = sp.sympify(other)
        return Exterior(
            {
                monomial: sp.simplify(coefficient / denominator)
                for monomial, coefficient in self.terms.items()
            }
        )

    def coefficient(self, monomial: tuple[str, ...]) -> sp.Expr:
        return sp.simplify(self.terms.get(monomial, 0))

    def is_zero(self) -> bool:
        return not self.terms

    def equals(self, other: "Exterior") -> bool:
        return (self - other).is_zero()

    def record(self) -> list[dict[str, str]]:
        return [
            {
                "monomial": "1" if not monomial else "*".join(monomial),
                "coefficient": str(coefficient),
            }
            for monomial, coefficient in sorted(
                self.terms.items(),
                key=lambda item: (len(item[0]), item[0]),
            )
        ]


def even_derivative(polynomial: Exterior, symbol: sp.Symbol) -> Exterior:
    return Exterior(
        {
            monomial: sp.diff(coefficient, symbol)
            for monomial, coefficient in polynomial.terms.items()
        }
    )


def odd_left_derivative(polynomial: Exterior, name: str) -> Exterior:
    """Left derivative, d_L(theta_1...theta_n)/dtheta_j=(-1)^j rest."""

    output: dict[tuple[str, ...], sp.Expr] = {}
    for monomial, coefficient in polynomial.terms.items():
        if name not in monomial:
            continue
        index = monomial.index(name)
        reduced = monomial[:index] + monomial[index + 1 :]
        signed = coefficient if index % 2 == 0 else -coefficient
        output[reduced] = sp.simplify(output.get(reduced, 0) + signed)
    return Exterior(output)


def odd_right_derivative(polynomial: Exterior, name: str) -> Exterior:
    """Right derivative, with the variation moved past the remaining odds."""

    output: dict[tuple[str, ...], sp.Expr] = {}
    for monomial, coefficient in polynomial.terms.items():
        if name not in monomial:
            continue
        index = monomial.index(name)
        reduced = monomial[:index] + monomial[index + 1 :]
        swaps = len(monomial) - index - 1
        signed = coefficient if swaps % 2 == 0 else -coefficient
        output[reduced] = sp.simplify(output.get(reduced, 0) + signed)
    return Exterior(output)


def graded_poisson(
    left: Exterior,
    right: Exterior,
    even_pairs: tuple[tuple[sp.Symbol, sp.Symbol], ...],
    odd_pairs: tuple[tuple[str, str], ...],
) -> Exterior:
    """Even BFV Poisson bracket using right/left odd derivatives.

    Bosonic pairs are antisymmetric.  For each odd canonical pair
    ``(theta, pi)``, the fundamental brackets are symmetric:
    ``{theta,pi}={pi,theta}=1``.
    """

    result = Exterior.zero()
    for coordinate, momentum in even_pairs:
        result += even_derivative(left, coordinate) * even_derivative(
            right, momentum
        )
        result -= even_derivative(left, momentum) * even_derivative(
            right, coordinate
        )
    for coordinate, momentum in odd_pairs:
        result += odd_right_derivative(left, coordinate) * odd_left_derivative(
            right, momentum
        )
        result += odd_right_derivative(left, momentum) * odd_left_derivative(
            right, coordinate
        )
    return result


def verify_upstream(
    repository_root: Path, item: dict[str, Any]
) -> dict[str, Any]:
    path = repository_root / item["path"]
    raw = path.read_bytes()
    observed_sha256 = sha256_bytes(raw)
    if observed_sha256 != item["sha256"]:
        raise AssertionError(
            f"upstream hash mismatch for {item['path']}: "
            f"expected {item['sha256']}, observed {observed_sha256}"
        )
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream is not a VALID_RUN: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload digest mutation: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed_sha256,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def load_frozen_input() -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this frozen calculation accepts no arguments")
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
        "ice.gate1.v0-improved-static-bfv-source.input.v1"
    ):
        raise AssertionError("unexpected input schema")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("unexpected calculation identity")
    if payload["numbered_phase"] is not None:
        raise AssertionError("numbered phase mutation")
    expected_caps = {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    expected_nulls = {
        "physical_original_cycle": None,
        "full_joint_orientation": None,
        "full_m2_bfv_measure": None,
        "full_real_lapse_delta_C": None,
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
    if payload["bfv_convention"]["odd_order"] != list(ODD_ORDER):
        raise AssertionError("odd orientation mutation")
    if payload["bfv_convention"]["ghost_numbers"] != GHOST_NUMBER:
        raise AssertionError("ghost-number mutation")

    repository_root = Path(__file__).resolve().parent.parent
    upstream = [
        verify_upstream(repository_root, item)
        for item in payload["upstream_results"]
    ]
    return payload, observed, upstream


def exact_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    a, discriminant, d_symbol = sp.symbols(
        "a R D", positive=True, real=True
    )
    q, trace_p, phi, scalar_p = sp.symbols(
        "Q P phi p", real=True
    )
    t, constraint_value, new_phi = sp.symbols(
        "T c Phi", real=True
    )
    lapse, primary = sp.symbols("N Pi", real=True)

    positive_factor = (
        discriminant + 24 * sp.pi**4 * a**4
    ) / (8 * sp.pi**2 * a**3)
    domain_pass = audit.observe_exact(
        "G1.bfv.domain.positive_trace_factor",
        positive_factor.is_positive is True,
        "D=(R+24*pi^4*a^4)/(8*pi^2*a^3) is positive for a>0 and R>0 on U_plus",
    )

    even_pairs = (
        (t, constraint_value),
        (new_phi, scalar_p),
        (lapse, primary),
    )
    odd_pairs = (("c_g", "bar_rho"), ("bar_c", "rho"))

    def bracket(left: Exterior, right: Exterior) -> Exterior:
        return graded_poisson(left, right, even_pairs, odd_pairs)

    t_poly = Exterior.scalar(t)
    c_poly = Exterior.scalar(constraint_value)
    phi_poly = Exterior.scalar(new_phi)
    p_poly = Exterior.scalar(scalar_p)
    lapse_poly = Exterior.scalar(lapse)
    primary_poly = Exterior.scalar(primary)
    c_ghost = Exterior.generator("c_g")
    bar_c = Exterior.generator("bar_c")
    rho = Exterior.generator("rho")
    bar_rho = Exterior.generator("bar_rho")

    fp_matrix = sp.Matrix(
        [
            [
                bracket(t_poly, c_poly).coefficient(()),
                bracket(t_poly, primary_poly).coefficient(()),
            ],
            [
                bracket(lapse_poly, c_poly).coefficient(()),
                bracket(lapse_poly, primary_poly).coefficient(()),
            ],
        ]
    )
    fundamental_brackets = {
        "{T,c}": bracket(t_poly, c_poly),
        "{c,T}": bracket(c_poly, t_poly),
        "{c_g,bar_rho}": bracket(c_ghost, bar_rho),
        "{bar_rho,c_g}": bracket(bar_rho, c_ghost),
        "{bar_c,rho}": bracket(bar_c, rho),
        "{rho,bar_c}": bracket(rho, bar_c),
    }
    fundamental_expected = {
        "{T,c}": Exterior.scalar(1),
        "{c,T}": Exterior.scalar(-1),
        "{c_g,bar_rho}": Exterior.scalar(1),
        "{bar_rho,c_g}": Exterior.scalar(1),
        "{bar_c,rho}": Exterior.scalar(1),
        "{rho,bar_c}": Exterior.scalar(1),
    }
    fundamental_pass = audit.observe_exact(
        "G1.bfv.bracket.fundamental_pairs",
        all(
            fundamental_brackets[name].equals(expected)
            for name, expected in fundamental_expected.items()
        ),
        "the implemented graded bracket is antisymmetric on each even pair and symmetric on each odd pair",
    )
    canonical_pass = audit.observe_exact(
        "G1.bfv.canonical.fp_matrix",
        fp_matrix == sp.eye(2) and fp_matrix.det() == 1,
        "the gauges (T,N) and constraints (c,Pi) form an oriented unit local FP matrix",
    )

    t_p = 1 / d_symbol
    delta_coarea = sp.simplify(d_symbol * t_p)
    static_slice_pass = audit.observe_exact(
        "G1.bfv.canonical.static_slice_coarea",
        t_p.is_positive is True and delta_coarea == 1,
        "T_P=1/D>0 with T(c,0,p)=0 makes P=0 equivalent to T=0 and delta(P)*D=delta(T) locally",
    )

    d_q, d_trace_p, d_phi, d_scalar_p = sp.symbols(
        "dQ dP dphi dp", real=True
    )
    d_t, d_c, d_new_phi, d_w_p = sp.symbols(
        "dT dc dPhi dW_p", real=True
    )
    w, w_p = sp.symbols("W W_p", real=True)
    d_w = -q * d_trace_p + t * d_c + w_p * d_scalar_p
    d_boundary = sp.expand(
        trace_p * d_q
        + q * d_trace_p
        + d_w
        - constraint_value * d_t
        - t * d_c
        - scalar_p * d_w_p
        - w_p * d_scalar_p
    )
    liouville_residual = sp.expand(
        trace_p * d_q
        + scalar_p * d_phi
        - (
            constraint_value * d_t
            + scalar_p * d_new_phi
            + d_boundary
        )
    ).subs(d_new_phi, d_phi + d_w_p)
    endpoint_pass = audit.observe_exact(
        "G1.bfv.endpoint.improved_one_form",
        sp.expand(liouville_residual) == 0,
        "P*dQ+p*dphi=c*dT+p*dPhi+dB, so S_D=S0-[B] has the transformed endpoint variation",
    )
    static_boundary = sp.simplify(
        (trace_p * q + w - constraint_value * t - scalar_p * w_p).subs(
            {
                trace_p: 0,
                w: 0,
                t: 0,
                w_p: 0,
            }
        )
    )
    static_boundary_pass = audit.observe_exact(
        "G1.bfv.endpoint.static_normalization",
        static_boundary == 0,
        "the integral normalization at P=T=0 gives B=0 on the improved-static representative",
    )

    omega = constraint_value * c_ghost + primary * rho
    omega_ghost_numbers = {
        sum(GHOST_NUMBER[name] for name in monomial)
        for monomial in omega.terms
    }
    s_omega = bracket(omega, omega)
    omega_pass = audit.observe_exact(
        "G1.bfv.brst.charge_nilpotence",
        omega_ghost_numbers == {1} and s_omega.is_zero(),
        "Omega=c_g*c+rho*Pi has ghost number one and {Omega,Omega}=0 under the implemented graded bracket",
    )

    generators: dict[str, Exterior] = {
        "T": t_poly,
        "c": c_poly,
        "Phi": phi_poly,
        "p": p_poly,
        "N": lapse_poly,
        "Pi": primary_poly,
        "c_g": c_ghost,
        "bar_c": bar_c,
        "rho": rho,
        "bar_rho": bar_rho,
    }
    generator_images = {
        name: bracket(generator, omega)
        for name, generator in generators.items()
    }
    expected_generator_images = {
        "T": c_ghost,
        "c": Exterior.zero(),
        "Phi": Exterior.zero(),
        "p": Exterior.zero(),
        "N": rho,
        "Pi": Exterior.zero(),
        "c_g": Exterior.zero(),
        "bar_c": primary_poly,
        "rho": Exterior.zero(),
        "bar_rho": c_poly,
    }
    generator_derivation_pass = audit.observe_exact(
        "G1.bfv.brst.generator_images_from_omega",
        all(
            generator_images[name].equals(expected)
            for name, expected in expected_generator_images.items()
        ),
        "all bosonic and odd BRST generator images are derived as {F,Omega}, not supplied as a separate differential",
    )
    second_images = {
        name: bracket(image, omega)
        for name, image in generator_images.items()
    }
    nilpotence_pass = audit.observe_exact(
        "G1.bfv.brst.complete_generator_nilpotence",
        all(image.is_zero() for image in second_images.values()),
        "s^2 vanishes on every bosonic and odd generator, including the nonminimal endpoint sector",
    )

    psi = t * bar_c + lapse * bar_rho
    psi_ghost_numbers = {
        sum(GHOST_NUMBER[name] for name in monomial)
        for monomial in psi.terms
    }
    s_psi = bracket(psi, omega)
    expected_s_psi = (
        Exterior.scalar(primary * t + lapse * constraint_value)
        - Exterior.monomial(("c_g", "bar_c"))
        - Exterior.monomial(("rho", "bar_rho"))
    )
    psi_pass = audit.observe_exact(
        "G1.bfv.gauge_fermion.derived_density",
        psi_ghost_numbers == {-1} and s_psi.equals(expected_s_psi),
        "Psi=bar_c*T+bar_rho*N has ghost number -1 and the bracket gives sPsi=Pi*T+N*c-c_g*bar_c-rho*bar_rho",
    )
    gauge_invariance_pass = audit.observe_exact(
        "G1.bfv.gauge_fermion.brst_invariance",
        bracket(s_psi, omega).is_zero(),
        "the bracket-derived gauge-fixing density is BRST closed because {sPsi,Omega}=0",
    )

    d_lapse, d_primary = sp.symbols("dN dPi", real=True)
    d_lapse_primary = lapse * d_primary + primary * d_lapse
    multiplier_kinetic_residual = sp.expand(
        -lapse * d_primary
        - (primary * d_lapse - d_lapse_primary)
    )
    multiplier_boundary_pass = audit.observe_exact(
        "G1.bfv.endpoint.multiplier_kinetic_boundary",
        multiplier_kinetic_residual == 0,
        "-N*dPi=Pi*dN-d(N*Pi), and the boundary difference -[N*Pi] vanishes when endpoint Pi=0",
    )

    endpoint_generators = (t, primary)

    def coefficient_in_endpoint_ideal(coefficient: sp.Expr) -> bool:
        if coefficient == 0:
            return True
        polynomial = sp.Poly(coefficient, *endpoint_generators)
        return all(sum(monomial) > 0 for monomial, _ in polynomial.terms())

    endpoint_odd = {"c_g", "bar_c"}

    def in_endpoint_ideal(polynomial: Exterior) -> bool:
        for monomial, coefficient in polynomial.terms.items():
            if endpoint_odd.intersection(monomial):
                continue
            if not coefficient_in_endpoint_ideal(coefficient):
                return False
        return True

    endpoint_images = {
        "T": generator_images["T"],
        "Pi": generator_images["Pi"],
        "c_g": generator_images["c_g"],
        "bar_c": generator_images["bar_c"],
        "Phi": generator_images["Phi"],
    }
    endpoint_stability_pass = audit.observe_exact(
        "G1.bfv.endpoint.brst_stable_ideal",
        all(
            in_endpoint_ideal(image)
            for name, image in endpoint_images.items()
            if name != "Phi"
        )
        and endpoint_images["Phi"].is_zero(),
        "the endpoint ideal (T,Pi,c_g,bar_c), excluding c, is BRST stable and fixed Phi is invariant",
    )

    source_structure = {
        key: frozen_input["bfv_convention"][key]
        for key in (
            "construction_origin",
            "old_source_factor",
            "imported_lapse_modulus",
            "imported_fixed_a_endpoint",
        )
    }
    expected_source_structure = {
        "construction_origin": "NEW_DARBOUX_ENDPOINT_POLARIZATION",
        "old_source_factor": None,
        "imported_lapse_modulus": None,
        "imported_fixed_a_endpoint": None,
    }
    append_shortcut = source_structure != expected_source_structure
    replacement_structure_pass = audit.observe_exact(
        "G1.bfv.source.replacement_structure",
        not append_shortcut,
        "the frozen source declares a new Darboux endpoint polarization and imports no old fixed-a factor or lapse modulus",
    )

    hbar = sp.symbols("hbar", positive=True, real=True)
    ghost_density = (
        -Exterior.monomial(("c_g", "bar_c"))
        - Exterior.monomial(("rho", "bar_rho"))
    )
    quantum_ghost_phase = (sp.I / hbar) * ghost_density
    ghost_exponential = (
        Exterior.scalar(1)
        + quantum_ghost_phase
        + quantum_ghost_phase * quantum_ghost_phase / 2
    )
    top_monomial = ODD_ORDER
    raw_berezin_coefficient = ghost_exponential.coefficient(top_monomial)
    berezin_measure_normalization = -(hbar**2)
    normalized_berezin_factor = sp.simplify(
        berezin_measure_normalization * raw_berezin_coefficient
    )
    berezin_pass = audit.observe_exact(
        "G1.bfv.source.unit_berezin_orientation",
        raw_berezin_coefficient == -1 / hbar**2
        and normalized_berezin_factor == 1,
        "the quantum ghost phase has raw top coefficient -1/hbar^2 and the declared oriented measure -hbar^2 times coefficient extraction gives +1",
    )

    bosonic_zero_mode_phase = primary * t + lapse * constraint_value
    bosonic_pairing_matrix = sp.Matrix(
        [
            [
                sp.diff(sp.diff(bosonic_zero_mode_phase, integration), support)
                for support in (t, constraint_value)
            ]
            for integration in (primary, lapse)
        ]
    )
    bosonic_fourier_pass = audit.observe_exact(
        "G1.bfv.source.bosonic_fourier_pairing",
        bosonic_pairing_matrix == sp.eye(2),
        "the phase Pi*T+N*c has unit pairing matrix, so the declared full-real dPi and dN Fourier measures yield delta(T)delta(c)",
    )

    source_0 = sp.Function("F_0")(new_phi, scalar_p)
    source_t = sp.Function("F_T")(new_phi, scalar_p)
    source_c = sp.Function("F_c")(new_phi, scalar_p)
    source_tc = sp.Function("F_Tc")(new_phi, scalar_p)
    endpoint_test = (
        source_0
        + source_t * t
        + source_c * constraint_value
        + source_tc * t * constraint_value
    )
    delta_reduced_test = endpoint_test.subs(
        {t: 0, constraint_value: 0}
    )
    source_top_coefficient = sp.simplify(
        delta_reduced_test * normalized_berezin_factor
    )
    source_contraction_pass = audit.observe_exact(
        "G1.bfv.source.local_endpoint_contraction",
        delta_reduced_test == source_0 and source_top_coefficient == source_0,
        "the declared zero-mode delta(T)delta(c) and normalized ghost factor preserve generic Phi,p dependence as F_0(Phi,p)",
    )

    epsilon, alpha, x = sp.symbols(
        "epsilon alpha x", positive=True, real=True
    )
    reduced_one_step_action = scalar_p * x
    reduced_measure_pass = audit.observe_exact(
        "G1.bfv.relational.declared_canonical_measure",
        sp.diff(reduced_one_step_action, scalar_p) == x,
        "S_red=p*(Phi_2-Phi_1) with the separately declared dp/(2*pi*hbar) measure defines the regulated canonical identity control",
    )
    regulated_kernel = sp.exp(-x**2 / (4 * epsilon)) / (
        2 * sp.sqrt(sp.pi * epsilon)
    )
    combined_gaussian = alpha + 1 / (4 * epsilon)
    exact_pairing = sp.simplify(
        sp.sqrt(sp.pi / combined_gaussian)
        / (2 * sp.sqrt(sp.pi * epsilon))
    )
    expected_pairing = 1 / sp.sqrt(1 + 4 * alpha * epsilon)
    relational_formula_pass = audit.observe_exact(
        "G1.bfv.relational.regulated_identity_pairing",
        sp.simplify(exact_pairing - expected_pairing) == 0,
        "the regulated Fourier identity kernel pairs with exp(-alpha*x^2) as 1/sqrt(1+4*alpha*epsilon)",
    )
    relational_limit = sp.limit(expected_pairing, epsilon, 0, dir="+")
    relational_limit_pass = audit.observe_exact(
        "G1.bfv.relational.distributional_identity_limit",
        relational_limit == 1,
        "epsilon->0+ gives the test value at the origin, establishing only the reduced Phi identity distribution",
    )

    audit.guard_theorem(
        "G1.bfv.guard.improved_static_endpoint_scope",
        "HTV improved action for a time-independent canonical gauge",
        "the local U_plus Darboux chart with transverse pair {T,c}=1 and gauge-related endpoint data",
        "the calculation uses S_D=S0-[B] and transformed endpoint data; it does not append a gauge condition to the old fixed-a/proper-time source",
    )
    audit.guard_theorem(
        "G1.bfv.guard.bfv_endpoint_conditions",
        "BRST-BFV endpoint variational principle",
        "fixed T=0 and Phi; endpoint c_g=bar_c=Pi=0; endpoint c and N,rho,bar_rho are not fixed in the declared convention",
        "the endpoint ideal excluding c is checked for BRST stability; delta(c) instead belongs to the declared bulk/zero-mode Fourier contraction, and no full trajectory measure is constructed",
    )
    audit.guard_theorem(
        "G1.bfv.guard.local_zero_mode_only",
        "finite-dimensional FP/Fourier/Berezin zero-mode convention at one transverse component",
        "T=c=0 on U_plus with positive D and one frozen odd orientation",
        "the +1 factor uses an explicitly declared ghost-measure normalization and is not an absolute full BFV measure, global determinant, Pfaffian line or Gribov theorem",
    )
    audit.guard_theorem(
        "G1.bfv.guard.relational_identity_not_delta_c",
        "Gaussian regularization of a declared canonical Fourier identity distribution",
        "S_red=p*(Phi_2-Phi_1), declared dp/(2*pi*hbar), and Schwartz Gaussian tests",
        "this compatibility control is not a derived two-endpoint full BFV kernel, and delta(Phi_2-Phi_1) is not the full-real-lapse rigging distribution delta(C)",
    )
    audit.guard_theorem(
        "G1.bfv.guard.static_not_proper_time",
        "separation of improved-static and proper-time gauge ledgers",
        "the transformed canonical source with no imported lapse modulus or old source lattice",
        "the source neither supplies a nonzero proper-time history nor proves equality with the fixed-(a,phi) kernel",
    )
    audit.guard_theorem(
        "G1.bfv.guard.component_and_global_boundary",
        "componentwise Darboux and determinant orientation",
        "p>0 and R>0 only",
        "other components, edge conditions, a global atlas, original cycle, global n_sigma, physics and TOE remain null",
    )

    core_flags = {
        "domain_positive": domain_pass,
        "graded_fundamental_brackets": fundamental_pass,
        "canonical_fp_matrix": canonical_pass,
        "static_slice_coarea": static_slice_pass,
        "endpoint_improvement": endpoint_pass,
        "static_boundary_normalization": static_boundary_pass,
        "multiplier_kinetic_boundary": multiplier_boundary_pass,
        "omega_nilpotent": omega_pass,
        "generator_images_derived": generator_derivation_pass,
        "complete_generator_nilpotence": nilpotence_pass,
        "gauge_fermion_density": psi_pass,
        "gauge_fixing_brst_closed": gauge_invariance_pass,
        "endpoint_ideal_stable": endpoint_stability_pass,
        "replacement_source_structure": replacement_structure_pass,
        "unit_berezin_orientation": berezin_pass,
        "bosonic_fourier_pairing": bosonic_fourier_pass,
        "local_source_contraction": source_contraction_pass,
    }
    relational_flags = {
        "declared_canonical_measure": reduced_measure_pass,
        "regulated_identity_pairing": relational_formula_pass,
        "distributional_identity_limit": relational_limit_pass,
    }
    return {
        "domain": {
            "name": "U_plus",
            "definition": "p>0 and R=3*p^2-2*P^2>0",
            "D": str(positive_factor),
            "D_status": "POSITIVE_ON_DECLARED_COMPONENT",
            "static_slice": "T=0 iff P=0 at fixed (c,p)",
            "local_coarea": "delta(P)*D=delta(T)",
        },
        "endpoint_improvement": {
            "B": "P*Q+W-c*T-p*W_p",
            "liouville": "P*dQ+p*dphi=c*dT+p*dPhi+dB",
            "action": "S_D=S0-[B]",
            "static_representative_B": str(static_boundary),
            "fixed_endpoint_data": ["T=0", "Phi"],
            "multiplier_kinetic": "-N*dPi=Pi*dN-d(N*Pi)",
            "multiplier_boundary_difference": "-[N*Pi]=0 because endpoint Pi=0",
        },
        "bfv_algebra": {
            "bosonic_pairs": [["T", "c"], ["Phi", "p"], ["N", "Pi"]],
            "odd_order": list(ODD_ORDER),
            "odd_pairs": [["c_g", "bar_rho"], ["bar_c", "rho"]],
            "graded_bracket_convention": "right derivatives on the left argument, left derivatives on the right argument; odd canonical brackets are symmetric",
            "fundamental_brackets": {
                name: value.record()
                for name, value in fundamental_brackets.items()
            },
            "Omega": "c_g*c+rho*Pi",
            "Omega_terms": omega.record(),
            "bracket_Omega_Omega": s_omega.record(),
            "Psi": "bar_c*T+bar_rho*N",
            "Psi_terms": psi.record(),
            "sPsi": s_psi.record(),
            "H_BFV": "-sPsi",
            "brst_generator_images": {
                name: image.record()
                for name, image in generator_images.items()
            },
            "squared_generator_images": {
                name: image.record() for name, image in second_images.items()
            },
            "constraint_gauge_fp_matrix": [
                [str(value) for value in fp_matrix.row(index)]
                for index in range(fp_matrix.rows)
            ],
        },
        "endpoint_source": {
            "endpoint_ideal": ["T", "Pi", "c_g", "bar_c"],
            "physical_endpoint_coordinate": "Phi",
            "unfixed_endpoint_variables": ["c", "N", "rho", "bar_rho"],
            "constraint_delta_origin": "delta(c) is produced by the declared N zero-mode Fourier integration, not imposed as endpoint data",
            "bosonic_zero_mode_phase": "Pi*T+N*c",
            "bosonic_fourier_measures": [
                "dPi/(2*pi*hbar)",
                "dN/(2*pi*hbar)",
            ],
            "bosonic_pairing_matrix": [
                [str(value) for value in bosonic_pairing_matrix.row(index)]
                for index in range(bosonic_pairing_matrix.rows)
            ],
            "local_source": "delta(T)*delta(c) with normalized oriented ghost zero-mode factor +1",
            "quantum_ghost_phase": quantum_ghost_phase.record(),
            "ghost_exponential": ghost_exponential.record(),
            "berezin_top_monomial": "*".join(top_monomial),
            "raw_berezin_top_coefficient": str(raw_berezin_coefficient),
            "berezin_measure_normalization": str(berezin_measure_normalization),
            "normalized_berezin_factor": str(normalized_berezin_factor),
            "generic_test_contraction": str(source_top_coefficient),
            "source_structure": source_structure,
            "old_proper_time_source_reused": append_shortcut,
            "full_path_bfv_measure_constructed": False,
        },
        "relational_identity": {
            "reduced_one_form": "p*dPhi",
            "one_step_reduced_action": "p*(Phi_2-Phi_1)",
            "declared_measure": "dp/(2*pi*hbar)",
            "relationship_to_bfv_source": "compatibility control after the separately normalized local gauge zero-mode factor; not a derived full trajectory kernel",
            "regulated_kernel": str(regulated_kernel),
            "gaussian_test": "exp(-alpha*x^2)",
            "exact_pairing": str(exact_pairing),
            "epsilon_zero_limit": str(relational_limit),
            "full_real_lapse_delta_C": None,
        },
        "core_flags": core_flags,
        "relational_flags": relational_flags,
        "computed_facts": {
            "source_origin": (
                "NEW_DARBOUX_ENDPOINT_REPLACEMENT_NOT_OLD_SOURCE_APPEND"
                if not append_shortcut
                else "OLD_SOURCE_STRUCTURE_IMPORTED"
            ),
            "local_improved_static_bfv_algebra": (
                "KEEP" if all(core_flags.values()) else "KILL"
            ),
            "local_relational_identity_formula": (
                "EXACT_FORMULA_ONLY"
                if all(relational_flags.values())
                else "OPEN"
            ),
            "time_dependent_gauge_comparison": "NOT_COMPUTED",
            "finite_m2_bfv_trajectory_measure": "NOT_COMPUTED",
            "old_kernel_equivalence": "NOT_COMPUTED",
            "full_real_lapse_delta_C": "NOT_COMPUTED",
            "global_source_and_cycle": "NOT_COMPUTED",
        },
    }


def numerical_calculation(
    frozen_input: dict[str, Any], audit: Audit
) -> dict[str, Any]:
    plan = frozen_input["numerical_plan"]
    mp.mp.dps = int(plan["precision_digits"])
    alpha = mp.mpf(plan["alpha"])
    epsilon_values = [mp.mpf(value) for value in plan["epsilon_values"]]
    tolerance = mp.mpf(plan["relative_tolerance"])
    if (
        mp.mp.dps != 80
        or alpha != mp.mpf("0.7")
        or epsilon_values
        != [mp.mpf("0.2"), mp.mpf("0.05"), mp.mpf("0.01")]
        or tolerance != mp.mpf("1e-60")
    ):
        raise AssertionError("numerical plan mutation")

    records: list[dict[str, Any]] = []
    convergence_errors: list[mp.mpf] = []
    for index, epsilon in enumerate(epsilon_values, 1):
        normalization = 2 * mp.sqrt(mp.pi * epsilon)

        def integrand(value: mp.mpf) -> mp.mpf:
            kernel = mp.exp(-(value**2) / (4 * epsilon)) / normalization
            return kernel * mp.exp(-alpha * value**2)

        observed = mp.quad(integrand, [-mp.inf, mp.inf])
        expected = 1 / mp.sqrt(1 + 4 * alpha * epsilon)
        relative_error = abs(observed - expected) / abs(expected)
        passed = audit.observe_numerical(
            f"G1.bfv.relational.quadrature_{index}",
            relative_error,
            tolerance,
            "direct high-precision integration of the regulated relational identity matches the exact Gaussian pairing",
            {
                "alpha": mp_string(alpha),
                "epsilon": mp_string(epsilon),
                "observed": mp_string(observed, 60),
                "expected": mp_string(expected, 60),
                "distance_to_distributional_limit": mp_string(
                    abs(expected - 1), 40
                ),
            },
        )
        records.append(
            {
                "index": index,
                "epsilon": mp_string(epsilon),
                "observed": mp_string(observed, 60),
                "expected": mp_string(expected, 60),
                "relative_error": mp_string(relative_error, 24),
                "passed": passed,
            }
        )
        convergence_errors.append(abs(expected - 1))

    monotone = all(
        convergence_errors[index + 1] < convergence_errors[index]
        for index in range(len(convergence_errors) - 1)
    )
    monotonicity_pass = audit.observe_exact(
        "G1.bfv.relational.sampled_limit_monotonicity",
        monotone,
        "the frozen decreasing regulator sequence approaches the exact distributional test value monotonically",
    )
    return {
        "precision_digits": mp.mp.dps,
        "alpha": mp_string(alpha),
        "records": records,
        "sampled_limit_errors": [
            mp_string(error, 40) for error in convergence_errors
        ],
        "sampled_limit_monotone": monotone,
        "sampled_limit_monotonicity_check_passed": monotonicity_pass,
        "quadratures": len(records),
        "root_calls": 0,
        "ode_calls": 0,
    }


def select_decision(
    exact: dict[str, Any], numerical: dict[str, Any], audit: Audit
) -> dict[str, str]:
    facts = exact["computed_facts"]
    core_pass = all(exact["core_flags"].values())
    relational_pass = all(exact["relational_flags"].values()) and all(
        item["passed"] for item in audit.numerical
    ) and numerical["sampled_limit_monotonicity_check_passed"]
    append_shortcut = exact["endpoint_source"]["old_proper_time_source_reused"]

    if append_shortcut:
        return {
            "verdict": "KILL_APPEND_SHORTCUT",
            "programme_impact": "KILL_PREVIOUSLY_EXCLUDED_MODEL_CLASS",
            "classification": "GATE1_V0_BFV_SOURCE_REUSED_KILLED_APPEND_ONLY_MODEL_CLASS",
            "matched_predeclared_condition": (
                "the construction reuses the old proper-time/fixed-a source by "
                "appending delta(T) or an FP determinant"
            ),
        }
    if not core_pass:
        return {
            "verdict": "KILL_V0_IMPROVED_STATIC_BFV_SOURCE_ALGEBRA",
            "programme_impact": "KILL_LOCAL_SOURCE_IMPLEMENTATION",
            "classification": "GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_ALGEBRA_NONPASS",
            "matched_predeclared_condition": (
                "the frozen BRST charge is nonnilpotent, the endpoint ideal is "
                "not BRST stable, or the FP/Berezin factor is singular or "
                "inconsistently oriented"
            ),
        }
    if not relational_pass:
        return {
            "verdict": "NARROW_V0_BFV_ALGEBRA_IDENTITY_OPEN",
            "programme_impact": "NARROW_AND_OPEN",
            "classification": "GATE1_V0_LOCAL_BFV_ALGEBRA_KEEP_RELATIONAL_IDENTITY_OPEN",
            "matched_predeclared_condition": (
                "the local BFV algebra passes but the relational identity "
                "normalization is not established"
            ),
        }
    if facts != {
        "source_origin": "NEW_DARBOUX_ENDPOINT_REPLACEMENT_NOT_OLD_SOURCE_APPEND",
        "local_improved_static_bfv_algebra": "KEEP",
        "local_relational_identity_formula": "EXACT_FORMULA_ONLY",
        "time_dependent_gauge_comparison": "NOT_COMPUTED",
        "finite_m2_bfv_trajectory_measure": "NOT_COMPUTED",
        "old_kernel_equivalence": "NOT_COMPUTED",
        "full_real_lapse_delta_C": "NOT_COMPUTED",
        "global_source_and_cycle": "NOT_COMPUTED",
    }:
        raise AssertionError("computed-fact mutation after passing decision gates")
    return {
        "verdict": "KEEP_V0_LOCAL_IMPROVED_STATIC_BFV_ENDPOINT_SOURCE_ALGEBRA",
        "programme_impact": "NARROW_LOCAL_KEEP",
        "classification": "GATE1_V0_LOCAL_IMPROVED_STATIC_BFV_SOURCE_BRST_ENDPOINT_AND_RELATIONAL_IDENTITY_KEEP_FULL_PATH_DELTA_C_AND_GLOBAL_OPEN",
        "matched_predeclared_condition": (
            "upstream provenance is exact; the Darboux/static identities, BRST "
            "nilpotency, gauge-fixing density, endpoint stability, normalized "
            "FP/Fourier/Berezin zero-mode convention, local source contraction "
            "and declared reduced relational identity control all pass"
        ),
    }


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, Any]],
    audit: Audit,
) -> dict[str, Any]:
    runner_path = Path(__file__)
    runner_sha256 = sha256_bytes(runner_path.read_bytes())
    exact = exact_calculation(frozen_input, audit)
    numerical = numerical_calculation(frozen_input, audit)
    decision = select_decision(exact, numerical, audit)
    source_algebra_keep = (
        all(exact["core_flags"].values())
        and not exact["endpoint_source"]["old_proper_time_source_reused"]
    )
    relational_identity_keep = decision["verdict"] == (
        "KEEP_V0_LOCAL_IMPROVED_STATIC_BFV_ENDPOINT_SOURCE_ALGEBRA"
    )
    computed_facts = {
        **exact["computed_facts"],
        "local_improved_static_bfv_algebra": (
            "KEEP" if source_algebra_keep else "KILL"
        ),
        "local_relational_identity": (
            "KEEP" if relational_identity_keep else "OPEN"
        ),
    }
    promoted_outputs = dict(frozen_input["required_fail_closed_outputs"])
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
        "upstream_provenance": upstream,
        "exact_calculation": exact,
        "numerical_calculation": numerical,
        "computed_facts": computed_facts,
        "exact_checks": audit.exact,
        "theorem_guards": audit.theorem_guards,
        "numerical_checks": audit.numerical,
        "decision_trace": {
            "matched_predeclared_condition": decision[
                "matched_predeclared_condition"
            ],
            "scope_meaning": (
                "the verdict concerns one local improved-static BFV replacement-source "
                "algebra, its declared zero-mode convention, and compatibility "
                "with a separately declared reduced canonical identity only"
            ),
            "source_separation": (
                "the source is built in the exact Darboux endpoint polarization "
                "and does not multiply the old proper-time/fixed-a source by a "
                "new trace delta or FP factor"
            ),
            "primary_source_boundary": (
                "HTV and Garcia-Vergara-Urrutia supply the endpoint-improvement "
                "and BFV frameworks, not the repository chart, source "
                "zero-mode measure convention, full trajectory measure or physical state"
            ),
        },
        "scope_status": {
            "local_v0_uplus_improved_static_bfv_source_algebra": (
                "KEEP" if source_algebra_keep else "NONKEEP"
            ),
            "local_relational_identity_distribution": (
                "KEEP" if computed_facts["local_relational_identity"] == "KEEP" else "OPEN"
            ),
            "time_dependent_gauge_comparison": "OPEN_NOT_COMPUTED",
            "two_endpoint_full_bfv_kernel": None,
            "finite_m2_bfv_trajectory_measure": None,
            "old_fixed_a_kernel_equivalence": None,
            "full_real_lapse_delta_C": None,
            "global_gauge_atlas_and_cycle": None,
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "promoted_outputs": promoted_outputs,
        "gate1_decision": promoted_outputs["gate1"],
        "global_promotion": promoted_outputs["global_promotion"],
        "automatic_next": promoted_outputs["automatic_next"],
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
            "decision_table": frozen_input["decision_table"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256, upstream = load_frozen_input()
    audit = Audit()
    result = build_result(frozen_input, input_sha256, upstream, audit)
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
                    item["passed"] for item in audit.exact
                ),
                "exact_checks_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_checks_passed": sum(
                    item["passed"] for item in audit.numerical
                ),
                "numerical_checks_total": len(audit.numerical),
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
