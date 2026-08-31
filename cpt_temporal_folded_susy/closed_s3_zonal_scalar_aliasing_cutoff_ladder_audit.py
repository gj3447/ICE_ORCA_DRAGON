#!/usr/bin/env python3
"""Exact zonal-S3 aliasing versus true hard-cutoff remainder audit.

The calculation compares exact modal convolution with exact finite
Gauss-Chebyshev-U transform sums.  It is a scalar evaluator audit, not an ADM,
HDA, Jacobi, BFV, continuum, or physics calculation.
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


INPUT_NAME = "CLOSED_S3_ZONAL_SCALAR_ALIASING_CUTOFF_LADDER_AUDIT_INPUTS.json"
RESULT_NAME = "CLOSED_S3_ZONAL_SCALAR_ALIASING_CUTOFF_LADDER_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_s3_zonal_scalar_aliasing_cutoff_ladder_audit.py"
EXPECTED_INPUT_SHA256 = "c8b71f8f234787e35476e65f1ebcf285f7490a8e2da19070c0bfb77272a73d96"
CALCULATION_ID = "ClosedS3ZonalScalarAliasingCutoffLadderAudit"
RESULT_SCHEMA = "ice.closed-s3-zonal-scalar-aliasing-cutoff-ladder-audit.result.v1"
RESULT_PREFIX = "CLOSED_S3_ZONAL_SCALAR_ALIASING_CUTOFF_LADDER_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Ledger:
    exact: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, str]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)

    def check(self, check_id: str, passed: bool, statement: str) -> None:
        if check_id in self.seen:
            raise AssertionError(f"duplicate check id: {check_id}")
        self.seen.add(check_id)
        self.exact.append(
            {"id": check_id, "passed": bool(passed), "statement": statement}
        )

    def guard(
        self, guard_id: str, theorem: str, hypotheses: str, conclusion: str
    ) -> None:
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
                "conclusion_and_scope": conclusion,
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
        "complete_real_scalar_basis_at_all_degrees": None,
        "explicit_transverse_vector_basis": None,
        "explicit_transverse_traceless_tensor_basis": None,
        "full_scalar_vector_tensor_gaunt_ledger": None,
        "full_adm_cubic_constraint_expansion": None,
        "DD_DH_HH_constraint_brackets": None,
        "classical_hypersurface_deformation_algebra_closure": None,
        "classical_jacobi_closure": None,
        "classical_bfv_charge": None,
        "quantum_bfv_charge": None,
        "quantum_bfv_anomaly_freedom": None,
        "continuum_limit": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def read_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, observed {observed}"
        )
    payload = json.loads(raw)
    if (
        payload["schema_version"]
        != "ice.closed-s3-zonal-scalar-aliasing-cutoff-ladder-audit.input.v1"
        or payload["calculation_id"] != CALCULATION_ID
        or payload["numbered_phase"] is not None
    ):
        raise AssertionError("identity or unnumbered convention drift")
    if payload["resource_caps"] != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    conventions = payload["declared_basis_and_evaluators"]
    if conventions["production_rule"] != "M=N+1 nodes, audited rather than presumed dealiased":
        raise AssertionError("production-grid convention drift")
    if conventions["aliasing_defect"] != (
        "grid-evaluated retained coefficient minus exact-modal retained coefficient"
    ):
        raise AssertionError("aliasing convention drift")
    return payload, observed


def verify_upstream(
    root: Path, item: dict[str, Any]
) -> tuple[dict[str, str], dict[str, Any]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {item['path']}")
    value = json.loads(raw)
    if (
        value.get("run_status") != "VALID_RUN"
        or value.get("verdict") != item["required_verdict"]
        or value.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream status or payload mismatch: {item['path']}")
    packets = [
        packet
        for packet in value.get("packet_results", [])
        if packet.get("id") == item["required_packet_id"]
    ]
    if len(packets) != 1:
        raise AssertionError("required upstream packet missing or duplicated")
    return (
        {
            "path": item["path"],
            "sha256": observed,
            "payload_sha256_without_self": value["result_payload_sha256_without_self"],
            "verdict": value["verdict"],
            "packet_id": item["required_packet_id"],
        },
        packets[0],
    )


def parse_map(raw: dict[str, str]) -> dict[int, sp.Expr]:
    return {
        int(degree): sp.sympify(coefficient)
        for degree, coefficient in raw.items()
    }


def normalized(vector: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return {
        degree: sp.simplify(coefficient)
        for degree, coefficient in vector.items()
        if sp.simplify(coefficient) != 0
    }


def vector_equal(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> bool:
    return all(
        sp.simplify(left.get(index, 0) - right.get(index, 0)) == 0
        for index in set(left) | set(right)
    )


def subtract(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    return normalized(
        {
            index: left.get(index, 0) - right.get(index, 0)
            for index in set(left) | set(right)
        }
    )


def product_degrees(left: int, right: int) -> list[int]:
    return list(range(left + right, abs(left - right) - 1, -2))


def exact_square_factors(packet: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    factors: dict[int, sp.Expr] = {}
    for left_degree, left_coefficient in packet.items():
        for right_degree, right_coefficient in packet.items():
            for output_degree in product_degrees(left_degree, right_degree):
                factors[output_degree] = sp.simplify(
                    factors.get(output_degree, 0)
                    + left_coefficient * right_coefficient
                )
    return normalized(factors)


def discrete_sine_alias_rule(source_degree: int, target_degree: int, nodes: int) -> int:
    """Exact DST-I inner product factor at M Gauss-Chebyshev-U nodes."""
    period_half = nodes + 1
    period = 2 * period_half

    def reduce_sine_index(index: int) -> tuple[int, int]:
        residue = index % period
        if residue == 0 or residue == period_half:
            return 0, 0
        if residue > period_half:
            return period - residue, -1
        return residue, 1

    source_index, source_sign = reduce_sine_index(source_degree + 1)
    target_index, target_sign = reduce_sine_index(target_degree + 1)
    if source_sign == 0 or target_sign == 0 or source_index != target_index:
        return 0
    return source_sign * target_sign


def direct_discrete_inner(
    source_degree: int, target_degree: int, nodes: int
) -> sp.Expr:
    total = sp.S.Zero
    for node in range(1, nodes + 1):
        theta = sp.pi * node / (nodes + 1)
        total += sp.sin((source_degree + 1) * theta) * sp.sin(
            (target_degree + 1) * theta
        )
    return sp.trigsimp(sp.simplify(sp.Rational(2, nodes + 1) * total))


def grid_projection_factors(
    full_factors: dict[int, sp.Expr], cutoff: int, nodes: int
) -> dict[int, sp.Expr]:
    return normalized(
        {
            target_degree: sp.simplify(
                sum(
                    coefficient
                    * discrete_sine_alias_rule(source_degree, target_degree, nodes)
                    for source_degree, coefficient in full_factors.items()
                )
            )
            for target_degree in range(cutoff + 1)
        }
    )


def printable(vector: dict[int, sp.Expr]) -> dict[str, str]:
    return {
        str(degree): str(sp.factor(vector[degree])) for degree in sorted(vector)
    }


def run(payload: dict[str, Any], input_sha: str) -> dict[str, Any]:
    root = Path(__file__).resolve().parent.parent
    upstream_records: list[dict[str, str]] = []
    upstream_packets: list[dict[str, Any]] = []
    for item in payload["upstream_results"]:
        record, packet = verify_upstream(root, item)
        upstream_records.append(record)
        upstream_packets.append(packet)

    ledger = Ledger()
    ledger.guard(
        "CS3Alias.guard.dealiasing_scope",
        "Dealiasing separates transform-grid folding from the intended finite spectral convolution",
        "The exact modal coefficients and the finite Gauss-Chebyshev-U transform use the same normalized zonal Q_n convention and frozen source packet",
        "Agreement removes aliasing only for the retained coefficients in this packet. It does not remove or bound the exact (1-P_N) projection tail.",
    )
    ledger.guard(
        "CS3Alias.guard.quadrature_degree",
        "M-node Gauss-Chebyshev-U quadrature is exact for the weighted polynomial space through degree 2M-1",
        "The integrand for a retained Q_k coefficient of phi^2 has degree at most k+2d, with k<=N and frozen source degree d",
        "The executable checks the resulting finite degree budget. It does not transfer a Fourier 3/2 rule without this basis-specific derivation.",
    )
    ledger.guard(
        "CS3Alias.guard.physics_boundary",
        "A finite evaluator defect and a finite Galerkin tail are distinct from a continuum gauge anomaly",
        "No vector/TT basis, ADM constraints, DD/DH/HH algebra, projected Jacobiator, BFV charge, common operator core, or continuum tail theorem is present",
        "The result may classify aliasing and exact scalar projection support only; HDA, Jacobi, BFV, continuum and physics outputs remain null.",
    )

    packet = parse_map(payload["field_packet"]["coefficients"])
    maximum_source_degree = int(payload["field_packet"]["maximum_source_degree"])
    if maximum_source_degree != max(packet):
        raise AssertionError("maximum source degree mismatch")
    full_factors = exact_square_factors(packet)
    expected_full_factors = parse_map(
        payload["field_packet"]["expected_full_square_factors_in_s_units"]
    )
    ledger.check(
        "CS3Alias.packet.exact_modal_square",
        vector_equal(full_factors, expected_full_factors),
        "The frozen Q1+Q2 packet reproduces the preregistered exact modal square in units of s=(2*pi^2)^(-1/2).",
    )

    s = 1 / sp.sqrt(2 * sp.pi**2)
    upstream_square = {
        int(degree): sp.sympify(coefficient)
        for degree, coefficient in upstream_packets[0][
            "square_full_coefficients"
        ].items()
    }
    ledger.check(
        "CS3Alias.packet.upstream_modal_pin",
        vector_equal(
            upstream_square,
            {degree: sp.simplify(factor * s) for degree, factor in full_factors.items()},
        ),
        "An independent reconstruction of the exact square agrees coefficientwise with the pinned upstream convolution packet.",
    )

    rows: list[dict[str, Any]] = []
    exact_common_low: list[dict[int, sp.Expr]] = []
    over_common_low: list[dict[int, sp.Expr]] = []
    production_common_low: list[dict[int, sp.Expr]] = []
    projection_norm_factors: list[sp.Expr] = []

    for row in payload["cutoff_ladder"]:
        cutoff = int(row["cutoff_N"])
        production_nodes = int(row["production_nodes_M"])
        over_nodes = int(row["overintegrated_nodes_M"])
        prefix = f"CS3Alias.N{cutoff}"
        required_degree = cutoff + 2 * maximum_source_degree
        minimal_nodes = (required_degree + 2) // 2

        ledger.check(
            f"{prefix}.production_rule",
            production_nodes == cutoff + 1,
            "The production transform uses the preregistered M=N+1 node rule.",
        )
        ledger.check(
            f"{prefix}.overintegration_minimality",
            over_nodes == minimal_nodes
            and 2 * over_nodes - 1 >= required_degree
            and 2 * (over_nodes - 1) - 1 < required_degree,
            "The overintegrated transform uses the smallest M whose exact weighted-polynomial degree covers every retained coefficient.",
        )

        for nodes, label in ((production_nodes, "production"), (over_nodes, "over")):
            for source_degree in full_factors:
                for target_degree in range(cutoff + 1):
                    direct = direct_discrete_inner(
                        source_degree, target_degree, nodes
                    )
                    rule = discrete_sine_alias_rule(
                        source_degree, target_degree, nodes
                    )
                    ledger.check(
                        f"{prefix}.{label}.dst.r{source_degree}.k{target_degree}",
                        sp.simplify(direct - rule) == 0,
                        "The modular DST-I alias rule equals the direct exact Gauss-Chebyshev-U sine sum.",
                    )

        exact_retained = {
            degree: coefficient
            for degree, coefficient in full_factors.items()
            if degree <= cutoff
        }
        true_remainder = {
            degree: coefficient
            for degree, coefficient in full_factors.items()
            if degree > cutoff
        }
        projection_norm_factor = sp.simplify(
            sum(coefficient**2 for coefficient in true_remainder.values())
        )
        production = grid_projection_factors(
            full_factors, cutoff, production_nodes
        )
        overintegrated = grid_projection_factors(full_factors, cutoff, over_nodes)
        production_alias = subtract(production, exact_retained)
        over_alias = subtract(overintegrated, exact_retained)

        expected_support = [int(value) for value in row["expected_true_projection_support"]]
        expected_norm_factor = sp.sympify(
            row["expected_true_projection_norm_squared_factor_in_s_squared_units"]
        )
        expected_production_alias = parse_map(
            row["expected_production_alias_factors_in_s_units"]
        )
        expected_over_alias = parse_map(
            row["expected_overintegrated_alias_factors_in_s_units"]
        )
        expected_status = row["expected_production_alias_status"]

        ledger.check(
            f"{prefix}.true_projection_support",
            sorted(true_remainder) == expected_support,
            "The exact modal degrees above N match the preregistered true projection-remainder support.",
        )
        ledger.check(
            f"{prefix}.true_projection_norm",
            sp.simplify(projection_norm_factor - expected_norm_factor) == 0,
            "The exact projection-tail norm factor matches the preregistered value in s^2 units.",
        )
        ledger.check(
            f"{prefix}.overintegrated_alias",
            vector_equal(over_alias, expected_over_alias),
            "The degree-certified overintegrated transform agrees coefficientwise with exact modal convolution on retained modes.",
        )
        ledger.check(
            f"{prefix}.production_alias",
            vector_equal(production_alias, expected_production_alias),
            "The production-grid aliasing defect matches the preregistered retained-mode vector.",
        )
        ledger.check(
            f"{prefix}.production_alias_status",
            (bool(production_alias) and expected_status == "NONZERO")
            or (not production_alias and expected_status == "ZERO"),
            "The production-grid zero/nonzero alias classification matches the preregistered cutoff outcome.",
        )
        ledger.check(
            f"{prefix}.alias_projection_separation",
            set(production_alias).isdisjoint(true_remainder),
            "By the declared representation, retained-mode aliasing support and discarded exact projection support are recorded as disjoint objects rather than one residual.",
        )

        exact_common_low.append(
            {degree: exact_retained.get(degree, 0) for degree in range(3)}
        )
        over_common_low.append(
            {degree: overintegrated.get(degree, 0) for degree in range(3)}
        )
        production_common_low.append(
            {degree: production.get(degree, 0) for degree in range(3)}
        )
        projection_norm_factors.append(projection_norm_factor)

        alias_sources: list[dict[str, Any]] = []
        reconstructed_alias: dict[int, sp.Expr] = {}
        for source_degree, coefficient in full_factors.items():
            for target_degree in range(cutoff + 1):
                discrete_inner = discrete_sine_alias_rule(
                    source_degree, target_degree, production_nodes
                )
                continuum_inner = 1 if source_degree == target_degree else 0
                contribution = sp.simplify(
                    coefficient * (discrete_inner - continuum_inner)
                )
                if contribution != 0:
                    reconstructed_alias[target_degree] = sp.simplify(
                        reconstructed_alias.get(target_degree, 0) + contribution
                    )
                    alias_sources.append(
                        {
                            "source_degree": source_degree,
                            "target_degree": target_degree,
                            "discrete_inner": str(discrete_inner),
                            "continuum_inner": str(continuum_inner),
                            "alias_contribution_factor_in_s_units": str(contribution),
                        }
                    )

        reconstructed_alias = normalized(reconstructed_alias)
        ledger.check(
            f"{prefix}.production_alias_source_reconstruction",
            vector_equal(reconstructed_alias, production_alias),
            "The production-versus-exact retained discrepancy is reconstructed exactly from the recorded discrete alias source channels.",
        )

        rows.append(
            {
                "cutoff_N": cutoff,
                "required_integrand_polynomial_degree": required_degree,
                "production_nodes_M": production_nodes,
                "production_exact_degree": 2 * production_nodes - 1,
                "production_degree_certificate_sufficient": 2 * production_nodes - 1
                >= required_degree,
                "overintegrated_nodes_M": over_nodes,
                "overintegrated_exact_degree": 2 * over_nodes - 1,
                "exact_modal_retained_factors_in_s_units": printable(exact_retained),
                "overintegrated_retained_factors_in_s_units": printable(overintegrated),
                "production_retained_factors_in_s_units": printable(production),
                "overintegrated_alias_factors_in_s_units": printable(over_alias),
                "production_alias_factors_in_s_units": printable(production_alias),
                "production_alias_status": "NONZERO_ALIASING_DEFECT"
                if production_alias
                else "EXACT_ZERO_ALIASING_DEFECT",
                "production_alias_source_decomposition": alias_sources,
                "true_projection_remainder_factors_in_s_units": printable(
                    true_remainder
                ),
                "true_projection_support": sorted(true_remainder),
                "true_projection_norm_squared_factor_in_s_squared_units": str(
                    projection_norm_factor
                ),
                "true_projection_norm_squared_exact": str(
                    sp.factor(projection_norm_factor * s**2)
                ),
                "scope": "exact normalized zonal-scalar evaluator and hard-cutoff data only",
            }
        )

    ledger.check(
        "CS3Alias.ladder.exact_common_low_stability",
        all(vector_equal(exact_common_low[0], item) for item in exact_common_low[1:]),
        "The frozen packet's exact common Q0,Q1,Q2 coefficients are invariant across N=2,3,4.",
    )
    ledger.check(
        "CS3Alias.ladder.overintegrated_common_low_stability",
        all(vector_equal(over_common_low[0], item) for item in over_common_low[1:])
        and all(
            vector_equal(exact_item, over_item)
            for exact_item, over_item in zip(exact_common_low, over_common_low)
        ),
        "The degree-certified transform reproduces the stable exact common low coefficients at every cutoff.",
    )
    ledger.check(
        "CS3Alias.ladder.production_false_drift_detected",
        not vector_equal(production_common_low[0], production_common_low[1])
        and vector_equal(production_common_low[1], production_common_low[2]),
        "The underresolved N=2 production grid creates a false low-mode drift which disappears once its degree budget is sufficient.",
    )
    ledger.check(
        "CS3Alias.ladder.true_projection_closes_at_selection_bound",
        projection_norm_factors == [sp.Integer(5), sp.Integer(1), sp.Integer(0)],
        "For this frozen degree-two square only, the true tail decreases 5,1,0 in s^2 units and vanishes when N reaches the exact degree-four selection bound.",
    )

    passed = all(check["passed"] for check in ledger.exact)
    verdict = (
        "KEEP_EXACT_ZONAL_S3_ALIASING_SEPARATED_FROM_TRUE_CUTOFF_REMAINDER_NOT_HDA"
        if passed
        else "KILL_DECLARED_ZONAL_S3_ALIASING_CUTOFF_LADDER_AUDIT"
    )
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": "ESTABLISH_A_THREE_WAY_NONLINEAR_EVALUATOR_AND_FROZEN_CUTOFF_LADDER_CONTROL_BEFORE_ANY_FULL_SVT_ADM_HDA_TEST"
        if passed
        else "DO_NOT_USE_THE_DECLARED_EVALUATOR_CONTROL",
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "upstream_results": upstream_records,
        "primary_sources": payload["primary_sources"],
        "declared_basis_and_evaluators": payload[
            "declared_basis_and_evaluators"
        ],
        "field_packet": {
            "id": payload["field_packet"]["id"],
            "coefficients": payload["field_packet"]["coefficients"],
            "maximum_source_degree": maximum_source_degree,
            "exact_full_square_factors_in_s_units": printable(full_factors),
            "normalization_s": "sqrt(2)/(2*pi)",
        },
        "theorem_guards": ledger.guards,
        "exact_checks": ledger.exact,
        "check_summary": {
            "exact_passed": sum(check["passed"] for check in ledger.exact),
            "exact_total": len(ledger.exact),
            "theorem_guard_count": len(ledger.guards),
            "all_executable_checks_passed": passed,
        },
        "cutoff_results": rows,
        "computed_scope": "exact three-way zonal-scalar nonlinear evaluation and frozen N=2,3,4 projection ladder",
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "numerical_quadratures": 0,
            "exact_finite_quadrature_sums": sum(
                2
                * len(full_factors)
                * (int(row["cutoff_N"]) + 1)
                for row in payload["cutoff_ladder"]
            ),
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
