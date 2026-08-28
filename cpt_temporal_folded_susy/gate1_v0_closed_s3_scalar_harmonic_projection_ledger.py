#!/usr/bin/env python3
"""Gate 1 -- closed unit-S3 scalar zonal product/projection remainder ledger.

This is a deliberately kinematic, finite-cutoff control.  It uses only the
normalized scalar zonal harmonics Z_n about one pole of the unit S3, at L=2.
It proves neither a scalar constraint algebra nor scalar-vector-tensor closure,
and it constructs no ADM action, BRST charge, anomaly test, observable, state,
or likelihood.  Its sole output is an exact product/projection-remainder ledger.
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


INPUT_NAME = "GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_INPUTS.json"
RESULT_NAME = "GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_v0_closed_s3_scalar_harmonic_projection_ledger.py"
)
CALCULATION_ID = "Gate1V0ClosedS3ScalarHarmonicProjectionLedger"
RESULT_SCHEMA = "ice.gate1.v0.closed-s3-scalar-harmonic-projection-ledger.result.v1"
RESULT_PREFIX = "GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_RESULT="
EXPECTED_INPUT_SHA256 = "e43d9be06aa2ec5e11b7fc9948c2e2742fac972d658431ccfd2f08f47317380b"
ARTIFACT_CAP_BYTES = 1_000_000
L_CUTOFF = 2


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


def c_poly(n: int, x: sp.Symbol) -> sp.Expr:
    return sp.expand(sp.gegenbauer(n, 1, x))


def product_degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def z_product(left: int, right: int, normalization: sp.Expr) -> dict[int, sp.Expr]:
    return {degree: normalization for degree in product_degrees(left, right)}


def add_vectors(*vectors: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    total: dict[int, sp.Expr] = {}
    for vector in vectors:
        for degree, coefficient in vector.items():
            total[degree] = sp.simplify(total.get(degree, sp.S.Zero) + coefficient)
    return {degree: coefficient for degree, coefficient in total.items() if coefficient != 0}


def scale_vector(vector: dict[int, sp.Expr], scalar: sp.Expr) -> dict[int, sp.Expr]:
    return {
        degree: sp.simplify(scalar * coefficient)
        for degree, coefficient in vector.items()
        if scalar * coefficient != 0
    }


def projected_product(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr], normalization: sp.Expr
) -> dict[int, sp.Expr]:
    contributions: list[dict[int, sp.Expr]] = []
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            product = z_product(left_degree, right_degree, normalization)
            retained = {
                degree: coefficient
                for degree, coefficient in product.items()
                if degree <= L_CUTOFF
            }
            contributions.append(
                scale_vector(retained, left_coefficient * right_coefficient)
            )
    return add_vectors(*contributions)


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
        "full_scalar_harmonic_completeness": None,
        "scalar_vector_tensor_mode_closure": None,
        "closed_s3_adm_matter_action": None,
        "classical_hypersurface_deformation_algebra_closure": None,
        "classical_jacobi_closure": None,
        "quantum_bfv_charge": None,
        "quantum_bfv_anomaly_freedom": None,
        "raw_C_operator_domain": None,
        "absolute_bfv_measure": None,
        "relational_observables": None,
        "born_oppenheimer_or_decoherence": None,
        "empirical_likelihood": None,
        "quantum_gravity_claim": None,
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
        "ice.gate1.v0.closed-s3-scalar-harmonic-projection-ledger.input.v1"
    ):
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this must remain unnumbered")
    if payload["epistemic_scope"] != (
        "UNIT_RADIUS_S3_SCALAR_ZONAL_SUBSPACE_ABOUT_ONE_POLE_"
        "WITH_L_EQUALS_2_AND_NO_CANONICAL_CONSTRAINTS"
    ):
        raise AssertionError("epistemic scope drift")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if payload["declared_geometry_and_basis"]["cutoff"] != (
        "P_L projects onto span{Z_0,Z_1,Z_2}; L=2"
    ):
        raise AssertionError("cutoff convention drift")
    return payload, observed


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    x = sp.symbols("x", real=True)
    chi = sp.symbols("chi", real=True)
    normalization = 1 / sp.sqrt(2 * sp.pi**2)
    ledger = Ledger()

    for left in range(5):
        for right in range(5):
            trig_integral = sp.integrate(
                sp.sin((left + 1) * chi) * sp.sin((right + 1) * chi),
                (chi, 0, sp.pi),
            )
            inner_product = sp.simplify(
                4 * sp.pi * normalization**2 * trig_integral
            )
            ledger.check(
                f"G1.s3scalar.orthonormality.n{left}.m{right}",
                inner_product == (sp.S.One if left == right else sp.S.Zero),
                "The declared 4*pi*sin(chi)^2 dchi zonal inner product reduces to the exact sine orthogonality integral.",
            )

    for degree in range(5):
        polynomial = c_poly(degree, x)
        radial_laplacian = sp.expand((1 - x**2) * sp.diff(polynomial, x, 2) - 3 * x * sp.diff(polynomial, x))
        ledger.check(
            f"G1.s3scalar.laplacian.degree_{degree}",
            sp.simplify(radial_laplacian + degree * (degree + 2) * polynomial) == 0,
            "The declared zonal scalar harmonic has Delta_S3 Z_n=-n(n+2) Z_n.",
        )

    remainder_table: list[dict[str, Any]] = []
    for left in range(L_CUTOFF + 1):
        for right in range(L_CUTOFF + 1):
            degrees = product_degrees(left, right)
            polynomial_difference = sp.expand(
                c_poly(left, x) * c_poly(right, x)
                - sum(c_poly(degree, x) for degree in degrees)
            )
            normalized_product_difference = sp.expand(
                normalization**2 * c_poly(left, x) * c_poly(right, x)
                - normalization
                * sum(
                    normalization * c_poly(degree, x)
                    for degree in degrees
                )
            )
            ledger.check(
                f"G1.s3scalar.product.l{left}.m{right}",
                polynomial_difference == 0
                and normalized_product_difference == 0,
                "The Gegenbauer character identity and the normalized Z_l Z_m=N*sum Z_n product both hold exactly.",
            )
            retained = [degree for degree in degrees if degree <= L_CUTOFF]
            omitted = [degree for degree in degrees if degree > L_CUTOFF]
            remainder_norm_squared = sp.simplify(len(omitted) * normalization**2)
            remainder_table.append(
                {
                    "left": left,
                    "right": right,
                    "all_product_degrees": degrees,
                    "retained_degrees": retained,
                    "omitted_degrees": omitted,
                    "retained_coefficients": [
                        str(normalization) for _ in retained
                    ],
                    "omitted_remainder_coefficients": [
                        str(normalization) for _ in omitted
                    ],
                    "remainder_norm_squared": str(remainder_norm_squared),
                }
            )
            for degree in degrees:
                ledger.check(
                    f"G1.s3scalar.antipodal.l{left}.m{right}.n{degree}",
                    (left + right - degree) % 2 == 0
                    and sp.expand(c_poly(degree, -x) - (-1) ** degree * c_poly(degree, x)) == 0,
                    "Every product coefficient is compatible with the antipodal parity Z_n(-x)=(-1)^n Z_n.",
                )

    z2_square = z_product(2, 2, normalization)
    ledger.check(
        "G1.s3scalar.cutoff.z2_square_has_omitted_z4",
        z2_square == {4: normalization, 2: normalization, 0: normalization},
        "Z_2 Z_2 contains an explicit Z_4 term, so the L=2 scalar subspace is not product closed.",
    )

    a, b, c = ({1: sp.S.One}, {2: sp.S.One}, {2: sp.S.One})
    left_associated = projected_product(projected_product(a, b, normalization), c, normalization)
    right_associated = projected_product(a, projected_product(b, c, normalization), normalization)
    associator = add_vectors(left_associated, scale_vector(right_associated, -1))
    discarded_ab = {degree: coefficient for degree, coefficient in z_product(1, 2, normalization).items() if degree > L_CUTOFF}
    discarded_bc = {degree: coefficient for degree, coefficient in z_product(2, 2, normalization).items() if degree > L_CUTOFF}
    reconstructed = add_vectors(
        scale_vector(projected_product(discarded_ab, c, normalization), -1),
        projected_product(a, discarded_bc, normalization),
    )
    expected_associator = {1: -normalization**2}
    ledger.check(
        "G1.s3scalar.projected_product.associator_witness",
        associator == expected_associator,
        "At L=2, P(P(Z_1 Z_2) Z_2)-P(Z_1 P(Z_2 Z_2))=-Z_1/(2*pi^2), so projected multiplication is not associative.",
    )
    ledger.check(
        "G1.s3scalar.projected_product.associator_reconstructed_from_remainders",
        reconstructed == associator,
        "The finite projected-product associator equals the explicit discarded-product remainder contribution, not a constraint-algebra anomaly.",
    )

    if len(ledger.exact) == 0:
        raise AssertionError("no checks emitted")
    exact_pass = all(item["passed"] for item in ledger.exact)
    if exact_pass:
        verdict = (
            "KEEP_CLOSED_S3_SCALAR_ZONAL_FINITE_CUTOFF_PRODUCT_"
            "REMAINDER_LEDGER_NOT_HDA"
        )
        impact = "RECORD_FINITE_SCALAR_TRUNCATION_REMAINDER_ONLY"
    else:
        verdict = "KILL_CLOSED_S3_SCALAR_ZONAL_PROJECTION_LEDGER"
        impact = "NO_INFERENCE_ABOUT_CLOSED_S3_HARMONICS_OR_CONSTRAINT_CLOSURE"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "primary_sources": payload["primary_sources"],
        "declared_geometry_and_basis": payload["declared_geometry_and_basis"],
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "all_executable_checks_passed": exact_pass,
        },
        "formulae": {
            "normalization": "(2*pi^2)^(-1/2)",
            "cutoff": L_CUTOFF,
            "z2_square": "Z_2 Z_2=(2*pi^2)^(-1/2)(Z_4+Z_2+Z_0)",
            "discarded_R_12": "(2*pi^2)^(-1/2) Z_3",
            "discarded_R_22": "(2*pi^2)^(-1/2) Z_4",
            "projected_associator_witness": "P(P(Z_1 Z_2) Z_2)-P(Z_1 P(Z_2 Z_2))=-Z_1/(2*pi^2)",
            "associator_remainder_identity": "associator=-P(R_12 Z_2)+P(Z_1 R_22)",
        },
        "projection_remainder_table": remainder_table,
        "computed_scope": (
            "finite scalar zonal product/projection ledger on the unit S3 only"
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
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
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
