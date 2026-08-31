#!/usr/bin/env python3
"""Exact complex-S3 scalar Gaunt golden data and projection-remainder ledger.

This is a bounded SU(2) scalar-harmonic coefficient packet.  It checks a
fixed Wigner-D convention, full product associativity, and the fact that a
hard degree projection has a separately reportable associator/remainder.  It
does not form ADM constraints, any HDA bracket or Jacobiator, or a BFV charge.
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
from sympy.physics.wigner import clebsch_gordan


INPUT_NAME = "CLOSED_S3_SU2_SCALAR_GAUNT_GOLDEN_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_SU2_SCALAR_GAUNT_GOLDEN_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_su2_scalar_gaunt_golden_ledger.py"
EXPECTED_INPUT_SHA256 = "d2efca9a98869678b4ace5b1edbe1b73e3847088f154649cd8a62a38953ca9a7"
CALCULATION_ID = "ClosedS3SU2ScalarGauntGoldenLedger"
RESULT_SCHEMA = "ice.closed-s3-su2-scalar-gaunt-golden-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_SU2_SCALAR_GAUNT_GOLDEN_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000

Mode = tuple[int, int, int]
Expansion = dict[Mode, sp.Expr]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, str]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, residual: sp.Expr | bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        passed = bool(residual) if isinstance(residual, bool) else sp.simplify(residual) == 0
        self.exact.append({"id": check_id, "passed": passed, "statement": statement})

    def guard(self, guard_id: str, theorem: str, hypotheses: str, scope: str) -> None:
        if guard_id in self.seen:
            raise AssertionError(f"duplicate guard id: {guard_id}")
        self.seen.add(guard_id)
        self.guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF",
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": scope,
            }
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
        "real_scalar_harmonic_basis_translation": None,
        "complete_scalar_vector_tensor_gaunt_ledger": None,
        "vector_or_tensor_derivative_couplings": None,
        "gravitational_hamiltonian_constraint": None,
        "gravitational_momentum_constraint": None,
        "full_adm_cubic_constraint_expansion": None,
        "DD_DH_HH_constraint_brackets": None,
        "classical_hypersurface_deformation_algebra_closure": None,
        "classical_jacobi_closure": None,
        "classical_bfv_charge": None,
        "quantum_bfv_charge": None,
        "quantum_bfv_anomaly_freedom": None,
        "quantum_common_invariant_core": None,
        "absolute_bfv_measure": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    if (
        result.get("run_status") != "VALID_RUN"
        or result.get("verdict") != item["required_verdict"]
        or result.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream status, verdict, or payload mismatch: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": result["result_payload_sha256_without_self"],
        "verdict": result["verdict"],
    }


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if (
        payload.get("schema_version")
        != "ice.closed-s3-su2-scalar-gaunt-golden-ledger.input.v1"
        or payload.get("calculation_id") != CALCULATION_ID
        or payload.get("numbered_phase") is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if payload.get("resource_caps") != expected_caps() or payload.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    return payload, observed


def allowed_doubled_m(n: int) -> range:
    return range(-n, n + 1, 2)


def valid_mode(mode: Mode) -> bool:
    n, m_left2, m_right2 = mode
    return n >= 0 and m_left2 in allowed_doubled_m(n) and m_right2 in allowed_doubled_m(n)


def as_mode(value: list[int]) -> Mode:
    if len(value) != 3:
        raise AssertionError("a scalar mode must be [n, 2m_left, 2m_right]")
    mode = (int(value[0]), int(value[1]), int(value[2]))
    if not valid_mode(mode):
        raise AssertionError(f"invalid declared SU(2) scalar mode: {mode}")
    return mode


def cg(n_left: int, m_left2: int, n_right: int, m_right2: int, n_out: int, m_out2: int) -> sp.Expr:
    return clebsch_gordan(
        sp.Rational(n_left, 2),
        sp.Rational(n_right, 2),
        sp.Rational(n_out, 2),
        sp.Rational(m_left2, 2),
        sp.Rational(m_right2, 2),
        sp.Rational(m_out2, 2),
    )


def product_modes(left: Mode, right: Mode) -> Expansion:
    """Wigner-D product in the declared volume-normalized complex scalar basis."""
    n_left, m_left_l2, m_left_r2 = left
    n_right, m_right_l2, m_right_r2 = right
    result: Expansion = {}
    for n_out in range(abs(n_left - n_right), n_left + n_right + 1, 2):
        m_out_l2 = m_left_l2 + m_right_l2
        m_out_r2 = m_left_r2 + m_right_r2
        if m_out_l2 not in allowed_doubled_m(n_out) or m_out_r2 not in allowed_doubled_m(n_out):
            continue
        coefficient = sp.sqrt(
            sp.Rational((n_left + 1) * (n_right + 1), n_out + 1)
            / (2 * sp.pi**2)
        )
        coefficient *= cg(n_left, m_left_l2, n_right, m_right_l2, n_out, m_out_l2)
        coefficient *= cg(n_left, m_left_r2, n_right, m_right_r2, n_out, m_out_r2)
        coefficient = sp.simplify(coefficient)
        if coefficient != 0:
            result[(n_out, m_out_l2, m_out_r2)] = coefficient
    return result


def add(left: Expansion, right: Expansion) -> Expansion:
    result = dict(left)
    for mode, coefficient in right.items():
        result[mode] = sp.simplify(result.get(mode, sp.S.Zero) + coefficient)
        if result[mode] == 0:
            del result[mode]
    return result


def multiply(left: Expansion, right: Expansion) -> Expansion:
    result: Expansion = {}
    for left_mode, left_coefficient in left.items():
        for right_mode, right_coefficient in right.items():
            for out_mode, product_coefficient in product_modes(left_mode, right_mode).items():
                result[out_mode] = sp.simplify(
                    result.get(out_mode, sp.S.Zero) + left_coefficient * right_coefficient * product_coefficient
                )
    return {mode: coefficient for mode, coefficient in result.items() if coefficient != 0}


def singleton(mode: Mode) -> Expansion:
    return {mode: sp.S.One}


def project(expansion: Expansion, cutoff: int) -> Expansion:
    return {mode: coefficient for mode, coefficient in expansion.items() if mode[0] <= cutoff}


def subtract(left: Expansion, right: Expansion) -> Expansion:
    return add(left, {mode: -coefficient for mode, coefficient in right.items()})


def expansion_zero(expansion: Expansion) -> bool:
    return all(sp.simplify(coefficient) == 0 for coefficient in expansion.values())


def serialise(expansion: Expansion) -> list[dict[str, Any]]:
    return [
        {"mode": list(mode), "coefficient": str(sp.simplify(coefficient))}
        for mode, coefficient in sorted(expansion.items())
    ]


def expected_expansion(rows: list[dict[str, Any]]) -> Expansion:
    output: Expansion = {}
    for row in rows:
        mode = as_mode(row["mode"])
        output[mode] = sp.sympify(row["coefficient"], locals={"pi": sp.pi})
    return output


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    ledger = Ledger()
    ledger.guard(
        "CS3SU2.guard.scalar_representation_scope",
        "Scalar harmonics on S3 identified with SU(2) matrix elements",
        "The unit round S3 is identified with SU(2), Haar volume is 2*pi^2, and the complex Wigner-D basis has the declared Condon--Shortley phase convention.",
        "This pins a complex scalar basis only. It neither supplies a real-basis translation nor vector/TT modes, derivative Gaunt data, ADM constraints, or an HDA theorem.",
    )
    ledger.guard(
        "CS3SU2.guard.cg_product_scope",
        "SU(2) Clebsch--Gordan product decomposition",
        "The two left/right magnetic labels use the same SU(2) Clebsch--Gordan convention and the displayed volume normalization.",
        "The exact arithmetic evaluates only selected low-degree product coefficients. It is not a complete scalar Gaunt table and does not construct a cubic gravitational vertex.",
    )
    ledger.guard(
        "CS3SU2.guard.projected_associator_scope",
        "Hard spectral projection does not preserve a product algebra in general",
        "P_L is applied after each selected product exactly as declared; the full product is evaluated before its discarded components are classified.",
        "A projected associator is a finite projection remainder. It is neither a DD/DH/HH residual nor a classical or quantum anomaly.",
    )

    golden_rows: list[dict[str, Any]] = []
    for packet in payload["golden_packets"]:
        left = as_mode(packet["left"])
        right = as_mode(packet["right"])
        full = product_modes(left, right)
        ledger.check(
            f"CS3SU2.golden.{packet['id']}.selection_valid",
            all(valid_mode(mode) for mode in full),
            "Every nonzero output has an allowed scalar degree and doubled left/right magnetic labels.",
        )
        if "expected_full_terms" in packet:
            expected = expected_expansion(packet["expected_full_terms"])
            ledger.check(
                f"CS3SU2.golden.{packet['id']}.exact_coefficients",
                expansion_zero(subtract(full, expected)),
                "The declared low-mode Wigner-D product equals the preregistered exact complex-basis coefficient table.",
            )
        if "expected_degrees" in packet:
            ledger.check(
                f"CS3SU2.golden.{packet['id']}.degree_selection",
                sorted({mode[0] for mode in full}) == [int(value) for value in packet["expected_degrees"]],
                "The nonzero output degrees match the preregistered SU(2) triangle/parity selection rule.",
            )
        golden_rows.append(
            {"id": packet["id"], "left": list(left), "right": list(right), "full_product": serialise(full)}
        )

    assoc_packet = payload["associativity_packet"]
    left = singleton(as_mode(assoc_packet["left"]))
    middle = singleton(as_mode(assoc_packet["middle"]))
    right = singleton(as_mode(assoc_packet["right"]))
    full_left = multiply(multiply(left, middle), right)
    full_right = multiply(left, multiply(middle, right))
    full_associator = subtract(full_left, full_right)
    cutoff = int(assoc_packet["projection_cutoff_L"])
    projected_left = project(multiply(project(multiply(left, middle), cutoff), right), cutoff)
    projected_right = project(multiply(left, project(multiply(middle, right), cutoff)), cutoff)
    projected_associator = subtract(projected_left, projected_right)
    full_intermediate_left = multiply(left, middle)
    full_intermediate_right = multiply(middle, right)
    discarded_left = subtract(full_intermediate_left, project(full_intermediate_left, cutoff))
    discarded_right = subtract(full_intermediate_right, project(full_intermediate_right, cutoff))

    ledger.check(
        "CS3SU2.associativity.full_product",
        expansion_zero(full_associator) == bool(assoc_packet["expected_full_associator_zero"]),
        "The unprojected selected scalar product is associative in the declared Wigner-D realization.",
    )
    ledger.check(
        "CS3SU2.associativity.projected_nonzero",
        (not expansion_zero(projected_associator)) == bool(assoc_packet["expected_projected_associator_nonzero"]),
        "The selected repeated hard projection has the preregistered nonzero finite associator.",
    )
    ledger.check(
        "CS3SU2.associativity.discarded_left_support",
        all(mode[0] > cutoff for mode in discarded_left),
        "Every left-parenthesization discarded intermediate component lies outside P_L.",
    )
    ledger.check(
        "CS3SU2.associativity.discarded_right_support",
        all(mode[0] > cutoff for mode in discarded_right),
        "Every right-parenthesization discarded intermediate component lies outside P_L.",
    )
    ledger.check(
        "CS3SU2.associativity.full_before_projection_reconstruction",
        expansion_zero(
            subtract(
                project(full_left, cutoff),
                add(
                    projected_left,
                    project(multiply(discarded_left, right), cutoff),
                ),
            )
        ),
        "For the left parenthesization, P_L of the full product is reconstructed from the repeated-projection result plus the explicitly discarded intermediate contribution.",
    )

    passed = all(item["passed"] for item in ledger.exact)
    verdict = (
        "KEEP_UNIT_S3_SU2_COMPLEX_SCALAR_GAUNT_GOLDEN_DATA_AND_PROJECTION_REMAINDER_NOT_ADM_HDA"
        if passed
        else "KILL_DECLARED_UNIT_S3_SU2_SCALAR_GAUNT_GOLDEN_PACKET"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": (
            "FIX_A_CONVENTION_CHECKED_COMPLEX_SCALAR_GAUNT_SEED_AND_EXPLICIT_PROJECTED_PRODUCT_REMAINDER_FOR_A_LATER_FULL_SVT_AND_ADM_EXPANSION"
            if passed
            else "DO_NOT_USE_THIS_COMPLEX_SCALAR_GAUNT_CONVENTION_PACKET"
        ),
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "upstream_results": upstream,
        "primary_sources": payload["primary_sources"],
        "declared_conventions": payload["declared_conventions"],
        "theorem_guards": ledger.guards,
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(item["passed"] for item in ledger.exact),
            "exact_total": len(ledger.exact),
            "theorem_guard_count": len(ledger.guards),
            "all_executable_checks_passed": passed,
        },
        "golden_products": golden_rows,
        "associativity_packet": {
            "projection_cutoff_L": cutoff,
            "full_left": serialise(full_left),
            "full_right": serialise(full_right),
            "full_associator": serialise(full_associator),
            "P_left": serialise(projected_left),
            "P_right": serialise(projected_right),
            "P_associator": serialise(projected_associator),
            "discarded_left_intermediate": serialise(discarded_left),
            "discarded_right_intermediate": serialise(discarded_right),
            "classification": "NONZERO_UNCLASSIFIED_PROJECTION_REMAINDER_NOT_CONSTRAINT_OR_QUANTUM_ANOMALY",
        },
        "computed_scope": "exact low-degree complex scalar S3=SU(2) Clebsch--Gordan product coefficients plus full/product-projected associativity bookkeeping only",
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
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "exact_passed": result["check_summary"]["exact_passed"],
                "exact_total": result["check_summary"]["exact_total"],
                "theorem_guards": result["check_summary"]["theorem_guard_count"],
                "result": RESULT_NAME,
                "result_sha256": sha256_bytes(encoded),
                "result_bytes": len(encoded),
                "automatic_next": None,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
