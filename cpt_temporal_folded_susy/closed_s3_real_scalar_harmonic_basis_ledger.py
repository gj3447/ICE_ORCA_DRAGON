#!/usr/bin/env python3
"""Exact finite complex-to-real unit-S3 scalar harmonic and Gaunt ledger.

This bounded calculation translates the pinned complex Wigner-D scalar seed
through degree n=2 into one explicit real basis.  It checks the finite unitary
transform, reality, orthonormality, a selected transformed product, and a
separately classified hard-projection remainder.  It does not construct SVT
derivative data, ADM constraints, HDA/Jacobi identities, or BFV objects.
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


INPUT_NAME = "CLOSED_S3_REAL_SCALAR_HARMONIC_BASIS_LEDGER_INPUTS.json"
RESULT_NAME = "CLOSED_S3_REAL_SCALAR_HARMONIC_BASIS_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_real_scalar_harmonic_basis_ledger.py"
EXPECTED_INPUT_SHA256 = "0b70b55f356d42fcc486bcf3d2a25a8766f5fe7ab890ee8393016136622a608c"
CALCULATION_ID = "ClosedS3RealScalarHarmonicBasisLedger"
RESULT_SCHEMA = "ice.closed-s3-real-scalar-harmonic-basis-ledger.result.v1"
RESULT_PREFIX = "CLOSED_S3_REAL_SCALAR_HARMONIC_BASIS_LEDGER_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000

Mode = tuple[int, int, int]
Expansion = dict[Mode, sp.Expr]
RealExpansion = dict[str, sp.Expr]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


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
        self.guards.append({"id": guard_id, "verified": True, "verification_mode": "SOURCE_PIN_AND_SCOPE_AUDIT_NOT_EXECUTABLE_PROOF", "theorem": theorem, "hypotheses": hypotheses, "conclusion_and_scope": scope})


def expected_caps() -> dict[str, int]:
    return {"wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144, "changed_artifact_files": 12, "changed_artifact_bytes": 1000000, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "automatic_descendants": 0}


def expected_nulls() -> dict[str, Any]:
    return {"complete_real_scalar_harmonic_basis": None, "complete_scalar_vector_tensor_gaunt_ledger": None, "scalar_derivative_gaunt_ledger": None, "vector_or_tensor_derivative_couplings": None, "gravitational_hamiltonian_constraint": None, "gravitational_momentum_constraint": None, "full_adm_cubic_constraint_expansion": None, "DD_DH_HH_constraint_brackets": None, "classical_hypersurface_deformation_algebra_closure": None, "classical_jacobi_closure": None, "classical_bfv_charge": None, "quantum_bfv_charge": None, "quantum_bfv_anomaly_freedom": None, "quantum_common_invariant_core": None, "absolute_bfv_measure": None, "physics_claim": None, "TOE_claim": None, "global_promotion": "PROHIBITED", "gate1": "OPEN_PARTIAL_PROGRESS", "automatic_next": None}


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    result = json.loads(raw)
    if result.get("run_status") != "VALID_RUN" or result.get("verdict") != item["required_verdict"] or result.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream status, verdict, or payload mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed, "payload_sha256_without_self": result["result_payload_sha256_without_self"], "verdict": result["verdict"]}


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}")
    payload = json.loads(raw)
    if payload.get("schema_version") != "ice.closed-s3-real-scalar-harmonic-basis-ledger.input.v1" or payload.get("calculation_id") != CALCULATION_ID or payload.get("numbered_phase") is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if payload.get("resource_caps") != expected_caps() or payload.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("caps or fail-closed outputs drift")
    return payload, observed


def allowed_doubled_m(n: int) -> range:
    return range(-n, n + 1, 2)


def modes_through(maximum_n: int) -> list[Mode]:
    return [(n, left, right) for n in range(maximum_n + 1) for left in allowed_doubled_m(n) for right in allowed_doubled_m(n)]


def conjugate_mode(mode: Mode) -> tuple[int, Mode]:
    n, left, right = mode
    exponent = (left - right) // 2
    phase = -1 if exponent % 2 else 1
    return (phase, (n, -left, -right))


def real_label(mode: Mode, kind: str) -> str:
    n, left, right = mode
    suffix = "" if kind == "self" else f"_{kind}"
    return f"R_n{n}_mL{left}_mR{right}{suffix}"


def build_transform(maximum_n: int) -> tuple[list[str], dict[str, Expansion], dict[str, int]]:
    remaining = set(modes_through(maximum_n))
    labels: list[str] = []
    rows: dict[str, Expansion] = {}
    degrees: dict[str, int] = {}
    while remaining:
        mode = min(remaining)
        phase, partner = conjugate_mode(mode)
        if partner not in remaining:
            raise AssertionError(f"conjugate mode escaped finite basis: {mode}")
        if partner == mode:
            label = real_label(mode, "self")
            rows[label] = {mode: sp.S.One}
            labels.append(label)
            degrees[label] = mode[0]
            remaining.remove(mode)
            continue
        if mode > partner:
            raise AssertionError("lexicographic pair selection drift")
        cosine = real_label(mode, "cos")
        sine = real_label(mode, "sin")
        rows[cosine] = {mode: sp.sqrt(2) / 2, partner: phase * sp.sqrt(2) / 2}
        rows[sine] = {mode: -sp.I * sp.sqrt(2) / 2, partner: phase * sp.I * sp.sqrt(2) / 2}
        labels.extend([cosine, sine])
        degrees[cosine] = mode[0]
        degrees[sine] = mode[0]
        remaining.remove(mode)
        remaining.remove(partner)
    return labels, rows, degrees


def inner(left: Expansion, right: Expansion) -> sp.Expr:
    return sp.simplify(sum(sp.conjugate(left.get(mode, 0)) * right.get(mode, 0) for mode in set(left) | set(right)))


def cg(n_left: int, m_left2: int, n_right: int, m_right2: int, n_out: int, m_out2: int) -> sp.Expr:
    return clebsch_gordan(sp.Rational(n_left, 2), sp.Rational(n_right, 2), sp.Rational(n_out, 2), sp.Rational(m_left2, 2), sp.Rational(m_right2, 2), sp.Rational(m_out2, 2))


def product_modes(left: Mode, right: Mode) -> Expansion:
    n_left, left_l, left_r = left
    n_right, right_l, right_r = right
    result: Expansion = {}
    for n_out in range(abs(n_left - n_right), n_left + n_right + 1, 2):
        out_l, out_r = left_l + right_l, left_r + right_r
        if out_l not in allowed_doubled_m(n_out) or out_r not in allowed_doubled_m(n_out):
            continue
        coefficient = sp.sqrt(sp.Rational((n_left + 1) * (n_right + 1), n_out + 1) / (2 * sp.pi**2))
        coefficient *= cg(n_left, left_l, n_right, right_l, n_out, out_l) * cg(n_left, left_r, n_right, right_r, n_out, out_r)
        coefficient = sp.simplify(coefficient)
        if coefficient != 0:
            result[(n_out, out_l, out_r)] = coefficient
    return result


def add(left: Expansion, right: Expansion) -> Expansion:
    result = dict(left)
    for mode, coefficient in right.items():
        result[mode] = sp.simplify(result.get(mode, 0) + coefficient)
        if result[mode] == 0:
            del result[mode]
    return result


def multiply(left: Expansion, right: Expansion) -> Expansion:
    result: Expansion = {}
    for left_mode, left_coefficient in left.items():
        for right_mode, right_coefficient in right.items():
            for output, product_coefficient in product_modes(left_mode, right_mode).items():
                result[output] = sp.simplify(result.get(output, 0) + left_coefficient * right_coefficient * product_coefficient)
    return {mode: coefficient for mode, coefficient in result.items() if coefficient != 0}


def subtract(left: Expansion, right: Expansion) -> Expansion:
    return add(left, {mode: -coefficient for mode, coefficient in right.items()})


def zero(expansion: Expansion) -> bool:
    return all(sp.simplify(coefficient) == 0 for coefficient in expansion.values())


def to_real(expansion: Expansion, labels: list[str], rows: dict[str, Expansion]) -> RealExpansion:
    result = {label: sp.simplify(sum(coefficient * sp.conjugate(rows[label].get(mode, 0)) for mode, coefficient in expansion.items())) for label in labels}
    return {label: coefficient for label, coefficient in result.items() if coefficient != 0}


def from_real(expansion: RealExpansion, rows: dict[str, Expansion]) -> Expansion:
    result: Expansion = {}
    for label, coefficient in expansion.items():
        for mode, transform_coefficient in rows[label].items():
            result[mode] = sp.simplify(result.get(mode, 0) + coefficient * transform_coefficient)
    return {mode: coefficient for mode, coefficient in result.items() if coefficient != 0}


def serialise_complex(expansion: Expansion) -> list[dict[str, Any]]:
    return [{"mode": list(mode), "coefficient": str(sp.simplify(coefficient))} for mode, coefficient in sorted(expansion.items())]


def serialise_real(expansion: RealExpansion) -> list[dict[str, str]]:
    return [{"label": label, "coefficient": str(sp.simplify(coefficient))} for label, coefficient in sorted(expansion.items())]


def expected_real(rows: list[dict[str, str]]) -> RealExpansion:
    return {row["label"]: sp.sympify(row["coefficient"], locals={"pi": sp.pi}) for row in rows}


def real_difference(left: RealExpansion, right: RealExpansion) -> bool:
    labels = set(left) | set(right)
    return all(sp.simplify(left.get(label, 0) - right.get(label, 0)) == 0 for label in labels)


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    maximum_n = int(payload["basis_degree_max"])
    if maximum_n != 2:
        raise AssertionError("this finite convention ledger is fixed to n<=2")
    labels, rows, degrees = build_transform(maximum_n)
    ledger = Ledger()
    ledger.guard("CS3Real.guard.finite_scope", "Finite conjugation-paired real scalar basis", "The pinned Wigner-D convention, conjugation rule, degree bound n<=2, and explicit lexicographic pairing are fixed.", "This produces a finite scalar convention bridge, not a complete real scalar basis or any vector/TT or derivative coupling ledger.")
    ledger.guard("CS3Real.guard.transform_scope", "Unitary complex-to-real change of finite orthonormal basis", "The complex Q modes are orthonormal and the displayed rows use the stated conjugation-pair combinations.", "The calculation checks finite linear algebra and selected scalar products only; it is not an ADM, HDA, Jacobi, BFV, or quantum statement.")
    ledger.guard("CS3Real.guard.projection_scope", "Hard spectral projection bookkeeping", "P_L is imposed only after the full selected product, and its omitted real modes are retained in the output record.", "Any observed omission is a finite projection remainder, not a DD/DH/HH residual or a quantum anomaly.")

    complex_modes = modes_through(maximum_n)
    gram = sp.Matrix([[inner(rows[left], rows[right]) for right in labels] for left in labels])
    ledger.check("CS3Real.transform.square_and_cardinality", len(labels) == len(complex_modes) == sum((n + 1) ** 2 for n in range(maximum_n + 1)), "The finite real and complex basis lists have the same declared n<=2 cardinality.")
    ledger.check("CS3Real.transform.unitarity", gram - sp.eye(len(labels)), "The declared finite complex-to-real transform is unitary with respect to the pinned complex-basis inner product.")
    reality_holds = True
    for row in rows.values():
        conjugated: Expansion = {}
        for mode, coefficient in row.items():
            phase, partner = conjugate_mode(mode)
            conjugated[partner] = sp.simplify(conjugated.get(partner, 0) + sp.conjugate(coefficient) * phase)
        reality_holds = reality_holds and all(
            sp.simplify(row.get(mode, 0) - conjugated.get(mode, 0)) == 0
            for mode in set(row) | set(conjugated)
        )
    ledger.check("CS3Real.transform.reality", reality_holds, "Every declared R row is fixed by the pinned Wigner-D conjugation operation.")
    ledger.check("CS3Real.transform.inverse_roundtrip", all(zero(subtract(from_real(to_real({mode: sp.S.One}, labels, rows), rows), {mode: sp.S.One})) for mode in complex_modes), "Complex coordinate unit vectors survive complex-to-real-to-complex conversion exactly.")

    packet = payload["selected_product_packet"]
    left = rows[packet["left_real_label"]]
    right = rows[packet["right_real_label"]]
    complex_product = multiply(left, right)
    transformed = to_real(complex_product, labels, rows)
    expected = expected_real(packet["expected_real_terms"])
    ledger.check("CS3Real.gaunt.selected_coefficient", real_difference(transformed, expected), "The selected real-basis product equals the preregistered exact transformed Gaunt coefficient packet.")
    ledger.check("CS3Real.gaunt.real_coefficients", all(sp.simplify(sp.im(coefficient)) == 0 for coefficient in transformed.values()), "Every coefficient in the selected product is real in the declared real basis.")
    ledger.check("CS3Real.gaunt.inverse_reconstruction", zero(subtract(from_real(transformed, rows), complex_product)), "The transformed real product reconstructs the full complex Wigner-D product exactly.")

    projection = payload["projection_packet"]
    source = rows[projection["source_real_label"]]
    full_square = to_real(multiply(source, source), labels, rows)
    cutoff = int(projection["cutoff_L"])
    projected = {label: coefficient for label, coefficient in full_square.items() if degrees[label] <= cutoff}
    discarded = {label: coefficient for label, coefficient in full_square.items() if degrees[label] > cutoff}
    reconstructed = dict(projected)
    reconstructed.update(discarded)
    ledger.check("CS3Real.projection.discarded_support", bool(discarded) and all(degrees[label] > cutoff for label in discarded), "All recorded omitted real components are outside the declared hard degree cutoff.")
    ledger.check("CS3Real.projection.full_reconstruction", real_difference(full_square, reconstructed), "The full real product is exactly the retained projected product plus its separately recorded discarded components.")

    passed = all(item["passed"] for item in ledger.exact)
    verdict = "KEEP_FINITE_REAL_S3_SCALAR_BASIS_TRANSLATION_AND_SELECTED_GAUNT_LEDGER_NOT_ADM_HDA" if passed else "KILL_DECLARED_FINITE_REAL_S3_SCALAR_BASIS_TRANSLATION"
    result: dict[str, Any] = {"schema_version": RESULT_SCHEMA, "calculation_id": CALCULATION_ID, "numbered_phase": None, "run_status": "VALID_RUN", "verdict": verdict, "programme_impact": "RECORD_FINITE_REAL_SCALAR_CONVENTION_BRIDGE_ONLY_AND_IDENTIFY_A_SEPARATE_SCALAR_DERIVATIVE_WORK_UNIT" if passed else "DO_NOT_USE_THIS_FINITE_REAL_SCALAR_BASIS_PACKET", "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha}, "upstream_results": upstream, "primary_sources": payload["primary_sources"], "declared_conventions": payload["declared_conventions"], "theorem_guards": ledger.guards, "exact_checks": ledger.exact, "check_summary": {"exact_passed": sum(item["passed"] for item in ledger.exact), "exact_total": len(ledger.exact), "theorem_guard_count": len(ledger.guards), "all_executable_checks_passed": passed}, "real_basis": {"degree_max": maximum_n, "labels": labels, "transform_rows": [{"label": label, "complex_terms": serialise_complex(rows[label])} for label in labels]}, "selected_product": {"id": packet["id"], "complex_product": serialise_complex(complex_product), "real_product": serialise_real(transformed)}, "projection_packet": {"cutoff_L": cutoff, "full_real_square": serialise_real(full_square), "projected_real_square": serialise_real(projected), "discarded_real_components": serialise_real(discarded), "classification": "FINITE_REAL_BASIS_PROJECTION_REMAINDER_NOT_CONSTRAINT_OR_QUANTUM_ANOMALY"}, "computed_scope": "finite n<=2 real scalar basis transform and one selected exact scalar product plus hard-projection bookkeeping only", "required_fail_closed_outputs": expected_nulls(), "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "adjacent_result_files_written": 1, "automatic_descendants": 0, "automatic_next": None}, "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())}, "environment": {"python": platform.python_version(), "platform": platform.platform(), "sympy": sp.__version__}}
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    return result


def main() -> None:
    payload, input_sha = read_input()
    result = run(payload, input_sha)
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": result["run_status"], "verdict": result["verdict"], "exact_passed": result["check_summary"]["exact_passed"], "exact_total": result["check_summary"]["exact_total"], "theorem_guards": result["check_summary"]["theorem_guard_count"], "result": RESULT_NAME, "result_sha256": sha256_bytes(encoded), "result_bytes": len(encoded), "automatic_next": None}, sort_keys=True))


if __name__ == "__main__":
    main()
