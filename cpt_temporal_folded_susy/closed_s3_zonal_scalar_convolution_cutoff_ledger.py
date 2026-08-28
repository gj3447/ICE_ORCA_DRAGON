#!/usr/bin/env python3
"""Exact zonal-S3 scalar convolution and nonlinear hard-cutoff ledger.

This runner works only in one zonal scalar subspace.  Its projected-product
remainders are not ADM cubic constraints, HDA/Jacobi residuals, or anomalies.
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


INPUT_NAME = "CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_CUTOFF_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_CUTOFF_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_scalar_convolution_cutoff_ledger.py"
EXPECTED_INPUT_SHA256 = "7e380dc78c84630986dcc07a49cc60b95ad5ab7819628fcd99c54fbf6b38cd1f"
CALCULATION_ID = "ClosedS3ZonalScalarConvolutionCutoffLedger"
RESULT_SCHEMA = "ice.closed-s3-zonal-scalar-convolution-cutoff-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_CUTOFF_LEDGER_RESULT="
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
        "transverse_vector_tensor_harmonic_basis": None,
        "full_gaunt_or_clebsch_gordan_ledger": None,
        "full_adm_cubic_constraint_expansion": None,
        "lapse_shift_constraint_brackets": None,
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


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError("upstream run status mismatch")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError("upstream verdict mismatch")
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError("upstream payload hash mismatch")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload["result_payload_sha256_without_self"],
        "verdict": payload["verdict"],
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
    if payload["schema_version"] != "ice.closed-s3-zonal-scalar-convolution-cutoff-ledger.input.v1":
        raise AssertionError("input schema mismatch")
    if payload["calculation_id"] != CALCULATION_ID:
        raise AssertionError("calculation id mismatch")
    if payload["numbered_phase"] is not None:
        raise AssertionError("this must remain unnumbered")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if payload["declared_basis_and_cutoff"]["hard_cutoff"] != (
        "P_N retains Q_0 through Q_N after every declared projected operation"
    ):
        raise AssertionError("hard-cutoff convention drift")
    return payload, observed


def product_degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def add_vectors(*vectors: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    total: dict[int, sp.Expr] = {}
    for vector in vectors:
        for degree, coefficient in vector.items():
            total[degree] = sp.simplify(total.get(degree, sp.S.Zero) + coefficient)
    return {degree: value for degree, value in total.items() if value != 0}


def scale(vector: dict[int, sp.Expr], factor: sp.Expr) -> dict[int, sp.Expr]:
    return {
        degree: sp.simplify(factor * coefficient)
        for degree, coefficient in vector.items()
        if factor * coefficient != 0
    }


def basis_product(left: int, right: int, normalization: sp.Expr) -> dict[int, sp.Expr]:
    return {degree: normalization for degree in product_degrees(left, right)}


def convolve(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr], normalization: sp.Expr
) -> dict[int, sp.Expr]:
    contributions = []
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            contributions.append(
                scale(
                    basis_product(left_degree, right_degree, normalization),
                    left_coefficient * right_coefficient,
                )
            )
    return add_vectors(*contributions)


def project(vector: dict[int, sp.Expr], cutoff: int) -> dict[int, sp.Expr]:
    return {degree: coefficient for degree, coefficient in vector.items() if degree <= cutoff}


def subtract(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return add_vectors(left, scale(right, -1))


def squared_norm(vector: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(coefficient**2 for coefficient in vector.values()))


def pairing(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(left.get(index, sp.S.Zero) * right.get(index, sp.S.Zero) for index in set(left) | set(right)))


def printable_vector(vector: dict[int, sp.Expr]) -> dict[str, str]:
    return {str(index): str(vector[index]) for index in sorted(vector)}


def run(payload: dict[str, Any], input_sha256: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    pi = sp.pi
    normalization = 1 / sp.sqrt(2 * pi**2)
    chi = sp.symbols("chi", real=True)
    x = sp.symbols("x", real=True)

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
                f"CS3ZC.orthonormality.n{left}.m{right}",
                inner_product == (sp.S.One if left == right else sp.S.Zero),
                "The declared normalized zonal Q_n functions are orthonormal on unit S3.",
            )

    for left in range(5):
        for right in range(5):
            product_identity = sp.expand(
                sp.chebyshevu(left, x) * sp.chebyshevu(right, x)
                - sum(sp.chebyshevu(degree, x) for degree in product_degrees(left, right))
            )
            ledger.check(
                f"CS3ZC.product.U{left}.U{right}",
                product_identity == 0,
                "The finite Chebyshev-U product identity holds exactly.",
            )

    for left in range(5):
        for right in range(5):
            allowed = set(product_degrees(left, right))
            for third in range(9):
                gaunt = normalization if third in allowed else sp.S.Zero
                reconstructed = basis_product(left, right, normalization).get(third, sp.S.Zero)
                ledger.check(
                    f"CS3ZC.gaunt.a{left}.b{right}.c{third}",
                    sp.simplify(gaunt - reconstructed) == 0,
                    "The zonal triple Gaunt coefficient is normalization iff the triangle/parity selection rule holds, and zero otherwise.",
                )

    packet_rows: list[dict[str, Any]] = []
    for packet in payload["coefficient_packets"]:
        cutoff = packet["cutoff_N"]
        phi = {int(index): sp.sympify(value) for index, value in packet["coefficients"].items()}
        if any(index > cutoff or index < 0 for index in phi):
            raise AssertionError(f"packet exceeds declared cutoff: {packet['id']}")
        square_full = convolve(phi, phi, normalization)
        square_retained = project(square_full, cutoff)
        square_remainder = subtract(square_full, square_retained)
        full_cubic_pairing = pairing(phi, square_full)
        retained_cubic_pairing = pairing(phi, square_retained)
        cubic_full_projected = project(convolve(square_full, phi, normalization), cutoff)
        cubic_iterated_projected = project(convolve(square_retained, phi, normalization), cutoff)
        cubic_iteration_residual = subtract(cubic_full_projected, cubic_iterated_projected)
        leakage_norm_squared = squared_norm(square_remainder)
        residual_norm_squared = squared_norm(cubic_iteration_residual)
        ledger.check(
            f"CS3ZC.packet.{packet['id']}.square_reconstruction",
            square_full == add_vectors(square_retained, square_remainder),
            "The full nonlinear square is exactly the retained square plus its hard-cutoff remainder.",
        )
        ledger.check(
            f"CS3ZC.packet.{packet['id']}.cubic_pairing_retention",
            sp.simplify(full_cubic_pairing - retained_cubic_pairing) == 0,
            "For phi in P_N, integral phi^3=<phi,phi^2>=<phi,P_N phi^2> exactly; this exact null does not make the full nonlinear product closed.",
        )
        ledger.check(
            f"CS3ZC.packet.{packet['id']}.iterated_cubic_reconstruction",
            cubic_full_projected == add_vectors(cubic_iterated_projected, cubic_iteration_residual),
            "The projected full cubic convolution is exactly the iterated hard-cutoff convolution plus the recorded residual.",
        )
        packet_rows.append(
            {
                "id": packet["id"],
                "purpose": packet["purpose"],
                "cutoff_N": cutoff,
                "phi_coefficients": printable_vector(phi),
                "square_full_coefficients": printable_vector(square_full),
                "square_retained_coefficients": printable_vector(square_retained),
                "square_remainder_coefficients": printable_vector(square_remainder),
                "square_remainder_norm_squared_exact": str(leakage_norm_squared),
                "square_remainder_norm_squared_50_digit": str(sp.N(leakage_norm_squared, 50)),
                "cubic_pairing_integral_phi_cubed_exact": str(full_cubic_pairing),
                "cubic_pairing_integral_phi_cubed_50_digit": str(sp.N(full_cubic_pairing, 50)),
                "retained_cubic_pairing_exact": str(retained_cubic_pairing),
                "full_cubic_projected_coefficients": printable_vector(cubic_full_projected),
                "iterated_hard_cutoff_cubic_coefficients": printable_vector(cubic_iterated_projected),
                "iterated_cubic_residual_coefficients": printable_vector(cubic_iteration_residual),
                "iterated_cubic_residual_norm_squared_exact": str(residual_norm_squared),
                "iterated_cubic_residual_norm_squared_50_digit": str(sp.N(residual_norm_squared, 50)),
            }
        )

    exact_pass = all(item["passed"] for item in ledger.exact)
    verdict = (
        "KEEP_CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_AND_HARD_CUTOFF_REMAINDER_LEDGER_NOT_ADM_OR_HDA"
        if exact_pass
        else "KILL_DECLARED_CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_CONVENTION"
    )
    impact = (
        "RECORD_SCALAR_ZONAL_CONVOLUTION_DATA_FOR_A_SEPARATE_FULL_SVT_GAUNT_AND_CONSTRAINT_EXPANSION"
        if exact_pass
        else "DO_NOT_USE_THIS_ZONAL_CONVOLUTION_PACKET_FOR_CONSTRAINT_EXPANSION"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_basis_and_cutoff": payload["declared_basis_and_cutoff"],
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "all_executable_checks_passed": exact_pass,
        },
        "packet_results": packet_rows,
        "computed_scope": "normalized unit-S3 zonal scalar Gaunt/product and nonlinear hard-cutoff convolution quantities only",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "adjacent_result_files_written": 1,
            "automatic_descendants": 0,
            "automatic_next": None,
        },
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
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
