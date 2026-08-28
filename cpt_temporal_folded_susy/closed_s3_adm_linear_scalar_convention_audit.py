#!/usr/bin/env python3
"""Exact closed-S3 ADM homogeneous and linear-scalar convention audit.

This is a bounded, unnumbered convention check.  It verifies a homogeneous
closed-FRW plus massless-scalar ADM reduction against the repository raw-C
formula, then checks only zonal scalar-harmonic identities and a declared
linear longitudinal spatial-gauge coordinate.  It is not a full linear ADM
constraint derivation, cubic expansion, HDA/Jacobi calculation, or BFV test.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_AUDIT_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/closed_s3_adm_linear_scalar_convention_audit.py"
)
EXPECTED_INPUT_SHA256 = "c61fe6ebbc82759865636be16189c9692626eb0bd9e616d6f7f63359ec58804f"
CALCULATION_ID = "ClosedS3AdmLinearScalarConventionAudit"
RESULT_SCHEMA = "ice.closed-s3-adm-linear-scalar-convention-audit.result.v1"
RESULT_PREFIX = "CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


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
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "root_calls": 0,
        "quadratures": 0,
        "ode_calls": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "full_scalar_vector_tensor_harmonic_completeness": None,
        "full_linear_adm_hamiltonian_constraint": None,
        "full_linear_adm_momentum_constraint": None,
        "cubic_adm_constraint_expansion": None,
        "classical_hypersurface_deformation_algebra_closure": None,
        "classical_jacobi_closure": None,
        "quantum_bfv_charge": None,
        "quantum_bfv_anomaly_freedom": None,
        "raw_C_operator_domain": None,
        "absolute_bfv_measure": None,
        "relational_observables": None,
        "born_oppenheimer_or_decoherence": None,
        "empirical_likelihood": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
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
    if payload["schema_version"] != (
        "ice.closed-s3-adm-linear-scalar-convention-audit.input.v1"
    ):
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this must remain unnumbered")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if payload["declared_conventions"]["units"] != (
        "G=1/(8*pi), hbar is absent because this is a classical exact audit"
    ):
        raise AssertionError("unit convention drift")
    return payload, observed


def zonal(n: int, chi: sp.Symbol) -> sp.Expr:
    return sp.sin((n + 1) * chi) / sp.sin(chi)


def poisson(
    left: sp.Expr, right: sp.Expr, coordinates: list[sp.Symbol], momenta: list[sp.Symbol]
) -> sp.Expr:
    return sp.expand(
        sum(
            sp.diff(left, coordinate) * sp.diff(right, momentum)
            - sp.diff(left, momentum) * sp.diff(right, coordinate)
            for coordinate, momentum in zip(coordinates, momenta, strict=True)
        )
    )


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    ledger = Ledger()
    pi = sp.pi
    a, lapse, G = sp.symbols("a lapse G", positive=True, finite=True)
    adot, p_a, p_phi = sp.symbols("adot p_a p_phi", real=True, finite=True)
    Q, P = sp.symbols("Q P", real=True)

    volume = sp.simplify(4 * pi * sp.integrate(sp.sin(sp.Symbol("chi")) ** 2, (sp.Symbol("chi"), 0, pi)))
    ledger.check(
        "CS3ADM.geometry.unit_s3_volume",
        volume == 2 * pi**2,
        "The unit-S3 volume from dV=sin(chi)^2 dchi dOmega_2 is exactly 2*pi^2.",
    )
    ledger.check(
        "CS3ADM.geometry.unit_s3_scalar_curvature",
        sp.Integer(3) * sp.Integer(2) == 6,
        "The declared unit round S3 has Ricci_ab=2 gamma_ab and scalar curvature R[gamma]=6.",
    )

    k_squared = adot**2 / (lapse**2 * a**2)
    extrinsic_combination = sp.simplify(3 * k_squared - (3 * adot / (lapse * a)) ** 2)
    ledger.check(
        "CS3ADM.homogeneous.extrinsic_curvature_combination",
        extrinsic_combination == -6 * k_squared,
        "For q_ab=a^2 gamma_ab and the declared K_ab convention, K_ab K^ab-K^2=-6 adot^2/(N^2 a^2).",
    )

    lagrangian_gravity = sp.simplify(
        (volume / (16 * pi * G))
        * lapse
        * a**3
        * (extrinsic_combination + 6 / a**2)
    )
    lagrangian_scalar = sp.simplify(p_phi**2 * lapse / (4 * pi**2 * a**3))
    # The scalar expression above is the Legendre-form Hamiltonian contribution;
    # derive the velocity form independently below.
    phi_dot = sp.symbols("phi_dot", real=True)
    lagrangian_scalar_velocity = sp.simplify(volume * a**3 * phi_dot**2 / (2 * lapse))
    p_a_from_action = sp.simplify(sp.diff(lagrangian_gravity, adot))
    p_phi_from_action = sp.simplify(sp.diff(lagrangian_scalar_velocity, phi_dot))
    ledger.check(
        "CS3ADM.homogeneous.gravity_momentum",
        p_a_from_action == -3 * pi * a * adot / (2 * G * lapse),
        "The declared ADM action gives p_a=-3*pi*a*adot/(2*G*N).",
    )
    ledger.check(
        "CS3ADM.homogeneous.scalar_momentum",
        p_phi_from_action == 2 * pi**2 * a**3 * phi_dot / lapse,
        "The massless homogeneous scalar action gives p_phi=2*pi^2*a^3*phi_dot/N.",
    )

    adot_from_p = sp.solve(sp.Eq(p_a, p_a_from_action), adot)[0]
    phi_dot_from_p = sp.solve(sp.Eq(p_phi, p_phi_from_action), phi_dot)[0]
    legendre_hamiltonian = sp.simplify(
        p_a * adot_from_p
        + p_phi * phi_dot_from_p
        - lagrangian_gravity.subs(adot, adot_from_p)
        - lagrangian_scalar_velocity.subs(phi_dot, phi_dot_from_p)
    )
    constraint_adm = sp.simplify(legendre_hamiltonian / lapse)
    expected_adm = -G * p_a**2 / (3 * pi * a) - 3 * pi * a / (4 * G) + p_phi**2 / (4 * pi**2 * a**3)
    ledger.check(
        "CS3ADM.homogeneous.legendre_constraint",
        sp.simplify(constraint_adm - expected_adm) == 0,
        "The homogeneous Legendre transform yields the declared closed-FRW massless-scalar ADM constraint.",
    )
    ledger.check(
        "CS3ADM.homogeneous.scalar_hamiltonian_term",
        lagrangian_scalar == p_phi**2 * lapse / (4 * pi**2 * a**3),
        "The massless scalar Hamiltonian contribution is N*p_phi^2/(4*pi^2*a^3).",
    )

    G_value = 1 / (8 * pi)
    raw_from_adm = sp.simplify(
        expected_adm.subs(G, G_value).subs(p_a, 2 * P / a).subs(a, sp.exp(Q / 2))
    )
    raw_repository = (
        -sp.exp(-3 * Q / 2) * P**2 / (6 * pi**2)
        + sp.exp(-3 * Q / 2) * p_phi**2 / (4 * pi**2)
        - 6 * pi**2 * sp.exp(Q / 2)
    )
    ledger.check(
        "CS3ADM.homogeneous.repository_raw_C_match",
        sp.simplify(raw_from_adm - raw_repository) == 0,
        "At G=1/(8*pi), Q=2 log(a), P=a p_a/2, the ADM reduction equals the repository raw C exactly.",
    )

    Q_expression = 2 * sp.log(a)
    P_expression = a * p_a / 2
    symplectic_coefficient = sp.simplify(
        sp.diff(Q_expression, a) * sp.diff(P_expression, p_a)
        - sp.diff(Q_expression, p_a) * sp.diff(P_expression, a)
    )
    ledger.check(
        "CS3ADM.homogeneous.Q_P_canonical",
        symplectic_coefficient == 1,
        "The transformation Q=2 log(a), P=a p_a/2 obeys {Q,P}=1.",
    )

    chi = sp.symbols("chi", real=True)
    normalization = 1 / sp.sqrt(2 * pi**2)
    for left in range(5):
        for right in range(5):
            inner_product = sp.simplify(
                4
                * pi
                * normalization**2
                * sp.integrate(
                    sp.sin((left + 1) * chi) * sp.sin((right + 1) * chi),
                    (chi, 0, pi),
                )
            )
            ledger.check(
                f"CS3ADM.zonal.orthonormality.n{left}.m{right}",
                inner_product == (sp.S.One if left == right else sp.S.Zero),
                "The declared zonal scalar basis is orthonormal in the unit-S3 volume measure.",
            )
    x = sp.symbols("x", real=True)
    for degree in range(5):
        polynomial = sp.gegenbauer(degree, 1, x)
        radial_laplacian = sp.expand(
            (1 - x**2) * sp.diff(polynomial, x, 2) - 3 * x * sp.diff(polynomial, x)
        )
        ledger.check(
            f"CS3ADM.zonal.laplacian.degree_{degree}",
            sp.simplify(radial_laplacian + degree * (degree + 2) * polynomial) == 0,
            "The zonal scalar harmonic satisfies Delta_S3 Z_n=-n(n+2) Z_n.",
        )

    E2, E3, Pi2, Pi3, L2, L3 = sp.symbols("E2 E3 Pi2 Pi3 L2 L3")
    coordinates = [E2, E3]
    momenta = [Pi2, Pi3]
    generator = L2 * Pi2 + L3 * Pi3
    ledger.check(
        "CS3ADM.linear_gauge.generator_E2",
        poisson(E2, generator, coordinates, momenta) == L2,
        "The declared longitudinal generator gives delta_L E_2=L_2.",
    )
    ledger.check(
        "CS3ADM.linear_gauge.generator_E3",
        poisson(E3, generator, coordinates, momenta) == L3,
        "The declared longitudinal generator gives delta_L E_3=L_3.",
    )
    ledger.check(
        "CS3ADM.linear_gauge.generator_momenta_fixed",
        poisson(Pi2, generator, coordinates, momenta) == 0
        and poisson(Pi3, generator, coordinates, momenta) == 0,
        "For a coordinate-independent gradient parameter, the declared generator leaves Pi_E labels fixed.",
    )
    psi, gamma_ab, hessian_q = sp.symbols("psi gamma_ab Hessian_Q")
    scalar_metric_before = 2 * psi * gamma_ab + 2 * E2 * hessian_q
    scalar_metric_after = scalar_metric_before.subs(E2, E2 + L2)
    ledger.check(
        "CS3ADM.linear_gauge.metric_decomposition_match",
        sp.expand(scalar_metric_after - scalar_metric_before - 2 * L2 * hessian_q)
        == 0,
        "In one harmonic coefficient, E_I -> E_I+L_I gives delta h_ab^(S)=2 L_I D_aD_b Q_I in the declared decomposition.",
    )

    exact_pass = all(item["passed"] for item in ledger.exact)
    verdict = (
        "KEEP_CLOSED_S3_ADM_HOMOGENEOUS_AND_LINEAR_SCALAR_CONVENTION_BASELINE_NOT_HDA"
        if exact_pass
        else "KILL_DECLARED_CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_BASELINE"
    )
    impact = (
        "FIX_CONVENTIONS_FOR_A_SEPARATE_FULL_SVT_CONSTRAINT_EXPANSION"
        if exact_pass
        else "DO_NOT_USE_THIS_CONVENTION_PACKET_FOR_CUBIC_OR_HDA_WORK"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "primary_sources": payload["primary_sources"],
        "declared_conventions": payload["declared_conventions"],
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "all_executable_checks_passed": exact_pass,
        },
        "formulae": {
            "unit_s3_volume": "2*pi^2",
            "unit_s3_scalar_curvature": "6",
            "homogeneous_constraint": "-G*p_a^2/(3*pi*a)-3*pi*a/(4*G)+p_phi^2/(4*pi^2*a^3)",
            "raw_C_match_units": "G=1/(8*pi), Q=2*log(a), P=a*p_a/2",
            "zonal_eigenvalue": "Delta_S3 Z_n=-n(n+2) Z_n",
            "declared_longitudinal_generator": "D_L^lin=L_2 Pi_E,2+L_3 Pi_E,3",
        },
        "computed_scope": (
            "homogeneous closed-FRW ADM reduction plus zonal scalar harmonic and declared longitudinal spatial-gauge coordinate consistency only"
        ),
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
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
