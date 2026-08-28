#!/usr/bin/env python3
"""Gate 1 -- finite positive-lambda BFV Pfaffian orientation transport.

This bounded non-numbered calculation combines only the already pinned
algebraic BFV zero ghost block with one pinned m=2 nonzero ghost block.  It
tests relative odd-line orientation transport on a declared positive lambda
interval from the inherited lambda=1 basis orientation.  A bosonic Gaussian
contour, an absolute BFV measure, endpoint polarization, Gribov data, gluing,
and continuum statements are deliberately outside the calculation.
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


INPUT_NAME = "GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_INPUTS.json"
RESULT_NAME = "GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/"
    "gate1_v0_bfv_finite_pfaffian_orientation_transport.py"
)
EXPECTED_INPUT_SHA256 = (
    "d88968a8193342a3ec6130b3a1a811b2e2f763cdf47cece58078a85326c21a79"
)
CALCULATION_ID = "Gate1V0BfvFinitePfaffianOrientationTransport"
RESULT_SCHEMA = "ice.gate1.v0-bfv-finite-pfaffian-orientation-transport.result.v1"
RESULT_PREFIX = "GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT="
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
class Audit:
    exact: list[dict[str, Any]] = field(default_factory=list)
    theorem_guards: list[dict[str, Any]] = field(default_factory=list)
    seen_ids: set[str] = field(default_factory=set, repr=False)

    def register(self, check_id: str) -> None:
        if check_id in self.seen_ids:
            raise AssertionError(f"duplicate audit id: {check_id}")
        self.seen_ids.add(check_id)

    def observe(self, check_id: str, passed: bool, statement: str) -> bool:
        self.register(check_id)
        observed = bool(passed)
        self.exact.append(
            {"id": check_id, "passed": observed, "statement": statement}
        )
        return observed

    def guard(
        self,
        guard_id: str,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> None:
        self.register(guard_id)
        self.theorem_guards.append(
            {
                "id": guard_id,
                "verified": True,
                "verification_mode": (
                    "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_"
                    "NUMERICAL_PREDICATE"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )


def verify_upstream(root: Path, item: dict[str, Any]) -> dict[str, str]:
    path = root / item["path"]
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(
            f"upstream hash mismatch for {item['path']}: {observed}"
        )
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mutation: {item['path']}")
    if (
        payload.get("result_payload_sha256_without_self")
        != item["payload_sha256_without_self"]
    ):
        raise AssertionError(f"upstream payload mutation: {item['path']}")
    return {
        "path": item["path"],
        "sha256": observed,
        "payload_sha256_without_self": payload[
            "result_payload_sha256_without_self"
        ],
        "verdict": payload["verdict"],
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "absolute_finite_bfv_measure": None,
        "full_bfv_trajectory_measure": None,
        "bosonic_contour_or_maslov_phase": None,
        "lapse_modulus_or_contour_selection": None,
        "zero_lapse_contact_terms": None,
        "endpoint_polarization_for_full_trajectory": None,
        "gribov_copy_census_or_global_gauge_slice": None,
        "two_slab_gluing": None,
        "continuum_determinant_or_pfaffian_line": None,
        "brst_cohomology": None,
        "raw_C_operator_and_domain": None,
        "quantum_constraint_rescaling_equivalence": None,
        "exact_endpoint_state_transform": None,
        "inhomogeneous_constraint_closure": None,
        "quantum_bfv_anomaly_freedom": None,
        "relational_observables_or_decoherence": None,
        "empirical_likelihood": None,
        "physical_original_cycle": None,
        "global_n_sigma": None,
        "quantum_gravity_claim": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


def load_input() -> tuple[dict[str, Any], str, list[dict[str, str]]]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calculation accepts no arguments")
    path = Path(__file__).with_name(INPUT_NAME)
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"input hash mismatch: expected {EXPECTED_INPUT_SHA256}, "
            f"observed {observed}"
        )
    payload = json.loads(raw)
    if payload["schema_version"] != (
        "ice.gate1.v0-bfv-finite-pfaffian-orientation-transport.input.v1"
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
        "quadratures": 0,
        "ode_calls": 0,
        "numerical_samples": 0,
        "automatic_descendants": 0,
    }
    if payload["resource_caps"] != expected_caps:
        raise AssertionError("resource cap mutation")
    if payload["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    family = payload["declared_finite_family"]
    if (
        family["lambda_interval"] != "lambda in [1/2,2]"
        or family["zero_block_hessian"]
        != "A0(lambda)=[[0,-lambda],[lambda,0]]"
        or family["nonzero_block_order"] != ["g1", "b1", "rho1", "br1"]
        or family["combined_order"]
        != ["rho0", "bar_rho0", "g1", "b1", "rho1", "br1"]
        or family["contour_rule"]
        != "no bosonic Gaussian contour or square-root branch is selected"
    ):
        raise AssertionError("declared finite family mutation")
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    return payload, observed, upstream


def pfaffian(matrix: sp.Matrix) -> sp.Expr:
    if matrix.rows != matrix.cols or matrix.rows % 2:
        raise AssertionError("Pfaffian requires an even square matrix")
    if matrix.rows == 0:
        return sp.Integer(1)
    result = sp.Integer(0)
    for column in range(1, matrix.cols):
        keep = [index for index in range(matrix.rows) if index not in (0, column)]
        minor = matrix.extract(keep, keep)
        result += (-1) ** (column + 1) * matrix[0, column] * pfaffian(minor)
    return sp.simplify(result)


def exact_calculation(audit: Audit) -> tuple[dict[str, Any], dict[str, bool]]:
    lam = sp.symbols("lambda", positive=True, real=True)
    real_lam = sp.symbols("ell", real=True)
    pi = sp.pi
    interval_left = sp.Rational(1, 2)
    interval_right = sp.Integer(2)

    a0 = sp.Matrix([[0, -lam], [lam, 0]])
    a1 = sp.Matrix(
        [
            [0, -lam, 0, pi],
            [lam, 0, pi, 0],
            [0, -pi, 0, -lam],
            [-pi, 0, lam, 0],
        ]
    )
    bosonic = sp.Matrix([[pi, lam], [lam, -pi]])
    combined = sp.diag(a0, a1)

    pf_a0 = pfaffian(a0)
    pf_a1 = pfaffian(a1)
    pf_combined = pfaffian(combined)
    det_a0 = sp.simplify(a0.det())
    det_a1 = sp.simplify(a1.det())
    det_bosonic = sp.simplify(bosonic.det())
    flags: dict[str, bool] = {}

    flags["antisymmetric_blocks"] = audit.observe(
        "G1.bfv.orientation.ordered_odd_blocks_antisymmetric",
        a0.T == -a0 and a1.T == -a1 and combined.T == -combined,
        "the pinned zero, m=2 and concatenated odd Hessians are exactly antisymmetric in their declared basis orders, so their Pfaffians are defined",
    )

    flags["zero_block"] = audit.observe(
        "G1.bfv.orientation.zero_block_pfaffian_and_determinant",
        sp.simplify(pf_a0 + lam) == 0
        and sp.simplify(det_a0 - lam**2) == 0,
        "in the inherited (rho0,bar_rho0) order, Pf(A0)=-lambda and det(A0)=lambda^2",
    )
    flags["nonzero_block"] = audit.observe(
        "G1.bfv.orientation.m2_block_pfaffian_and_determinant",
        sp.simplify(pf_a1 - (lam**2 + pi**2)) == 0
        and sp.simplify(det_a1 - (lam**2 + pi**2) ** 2) == 0,
        "in the inherited (g1,b1,rho1,br1) order, Pf(A1)=lambda^2+pi^2 and det(A1)=(lambda^2+pi^2)^2",
    )
    flags["direct_sum"] = audit.observe(
        "G1.bfv.orientation.block_direct_sum_pfaffian",
        sp.simplify(pf_combined - pf_a0 * pf_a1) == 0
        and sp.simplify(pf_combined + lam * (lam**2 + pi**2)) == 0,
        "the concatenated six-odd-variable order gives Pf(A0 direct-sum A1)=-lambda*(lambda^2+pi^2)",
    )

    reference_pf = sp.simplify(pf_combined.subs(lam, 1))
    relative_pf = sp.simplify(pf_combined / reference_pf)
    interval_positive = (
        relative_pf.is_positive is True
        and sp.simplify(relative_pf.subs(lam, interval_left)) > 0
        and sp.simplify(relative_pf.subs(lam, interval_right)) > 0
    )
    flags["positive_interval"] = audit.observe(
        "G1.bfv.orientation.positive_interval_relative_transport",
        interval_positive,
        "Pf(A(lambda))/Pf(A(1))=lambda*(lambda^2+pi^2)/(1+pi^2) is strictly positive on the declared [1/2,2] interval",
    )

    flags["zero_degeneracy"] = audit.observe(
        "G1.bfv.orientation.lambda_zero_degeneracy",
        sp.limit(pf_combined, lam, 0, dir="+") == 0
        and sp.simplify(det_a0.subs(lam, 0)) == 0
        and sp.simplify(det_a1.subs(lam, 0) - pi**4) == 0,
        "lambda tends to zero degenerates A0 while A1 remains nondegenerate, so the positive-interval transport does not extend through zero",
    )

    signed_control = -real_lam * (real_lam**2 + pi**2)
    real_zeros = sp.solve(signed_control, real_lam)
    flags["negative_control"] = audit.observe(
        "G1.bfv.orientation.negative_lambda_crossing_control",
        sp.simplify(pf_combined.subs(lam, interval_left)) < 0
        and sp.simplify(signed_control.subs(real_lam, -interval_left)) > 0
        and real_zeros == [0],
        "the lambda=-1/2 control reverses the Pfaffian sign, and every real continuation to it crosses the sole real zero lambda=0",
    )

    flags["bosonic_separation"] = audit.observe(
        "G1.bfv.orientation.bosonic_contour_phase_separation",
        sp.simplify(det_bosonic + (lam**2 + pi**2)) == 0
        and det_bosonic.is_negative is True,
        "det(M1)=-(lambda^2+pi^2)<0, so the odd Pfaffian transport does not select a bosonic Gaussian contour, Maslov phase, or square-root branch",
    )

    audit.guard(
        "G1.bfv.orientation.guard.relative_reference_only",
        "Pfaffian line orientation of a nonvanishing finite family",
        "the odd basis order and lambda=1 reference orientation are declared inputs, and the combined Pfaffian has no zero on [1/2,2]",
        "the calculation transports one relative sign only; it does not produce an orientation independent of its declared basis or reference",
    )
    audit.guard(
        "G1.bfv.orientation.guard.contour_endpoints_gribov_and_gluing_null",
        "separation of finite odd Gaussian algebra from a BFV trajectory measure",
        "no bosonic contour, lapse modulus, endpoint polarization, gauge-slice admissibility, Gribov analysis, or interface measure is included",
        "absolute measure, contour, endpoints, Gribov data and two-slab gluing remain null",
    )
    audit.guard(
        "G1.bfv.orientation.guard.no_continuum_or_physics_promotion",
        "bounded workbench interpretation",
        "the calculation contains two finite ghost blocks, no regulator removal, no BRST cohomology, and no raw-C, inhomogeneous, observable or empirical construction",
        "it supplies no continuum determinant line, anomaly conclusion, quantum gravity, physics or TOE claim",
    )

    return (
        {
            "ordered_finite_blocks": {
                "zero_block_order": ["rho0", "bar_rho0"],
                "nonzero_block_order": ["g1", "b1", "rho1", "br1"],
                "combined_order": ["rho0", "bar_rho0", "g1", "b1", "rho1", "br1"],
                "A0": str(a0),
                "A1": str(a1),
                "M1": str(bosonic),
            },
            "pfaffian_line": {
                "Pf_A0": str(pf_a0),
                "det_A0": str(det_a0),
                "Pf_A1": str(pf_a1),
                "det_A1": str(det_a1),
                "Pf_combined": str(pf_combined),
                "Pf_reference_lambda_1": str(reference_pf),
                "relative_Pf_to_lambda_1": str(relative_pf),
                "transport_interval": "[1/2,2]",
                "relative_orientation_fixed": True,
                "lambda_zero_degeneracy": True,
                "negative_lambda_transport_without_crossing": False,
            },
            "bosonic_boundary": {
                "det_M1": str(det_bosonic),
                "bosonic_contour_or_maslov_phase": None,
                "absolute_finite_bfv_measure": None,
            },
            "flags": flags,
        },
        flags,
    )


def build_result(
    frozen_input: dict[str, Any],
    input_sha256: str,
    upstream: list[dict[str, str]],
    audit: Audit,
) -> dict[str, Any]:
    exact, flags = exact_calculation(audit)
    all_exact = all(flags.values())
    if all_exact:
        verdict = (
            "KEEP_V0_FINITE_POSITIVE_LAMBDA_ODD_PFAFFIAN_RELATIVE_"
            "ORIENTATION_TRANSPORT"
        )
        impact = (
            "CLOSE_ONE_FINITE_RELATIVE_ODD_ORIENTATION_TRANSPORT_ONLY_KEEP_"
            "ABSOLUTE_BFV_MEASURE_OPEN"
        )
        condition = frozen_input["decision_table"][0]["condition"]
    else:
        verdict = "KILL_V0_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_DISCRIMINATOR"
        impact = (
            "RETAIN_PRIOR_RELATIVE_GHOST_DETERMINANTS_WITHOUT_A_COMBINED_"
            "ORIENTATION_TRANSPORT_CLAIM"
        )
        condition = frozen_input["decision_table"][1]["condition"]
    nulls = expected_nulls()
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": impact,
        "input": {"path": INPUT_RELPATH, "sha256": input_sha256},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": sha256_bytes(Path(__file__).read_bytes()),
        },
        "upstream_provenance": upstream,
        "exact_calculation": exact,
        "exact_checks": audit.exact,
        "numerical_checks": [],
        "theorem_guards": audit.theorem_guards,
        "decision_trace": {
            "matched_predeclared_condition": condition,
            "scope_meaning": "one finite relative odd-line sign transport on a declared positive lambda interval",
            "primary_source_boundary": "determinant-line sources frame the distinction between a relative finite orientation and an absolute measure; the finite matrices and exact checks are repository workbench results",
            "revision_boundary": "the earlier relative zero and m=2 factors are combined only to transport their declared odd-basis sign; contour, gluing and absolute normalization remain unselected",
        },
        "computed_scope": frozen_input["computed_scope"],
        "not_computed": frozen_input["not_computed"],
        "required_fail_closed_outputs": nulls,
        "gate1_decision": nulls["gate1"],
        "global_promotion": nulls["global_promotion"],
        "automatic_next": nulls["automatic_next"],
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "numerical_samples": 0,
            "automatic_descendants": 0,
            "adjacent_result_files": 1,
            "artifact_cap_bytes": ARTIFACT_CAP_BYTES,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
        "frozen_input_contract": {
            "question": frozen_input["question"],
            "kind": frozen_input["kind"],
            "epistemic_scope": frozen_input["epistemic_scope"],
            "decision_table": frozen_input["decision_table"],
            "primary_sources": frozen_input["primary_sources"],
        },
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(result)
    )
    return result


def main() -> None:
    frozen_input, input_sha256, upstream = load_input()
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
        raise AssertionError("result artifact exceeds the bounded cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": result["verdict"],
                "programme_impact": result["programme_impact"],
                "exact_checks_passed": sum(
                    item["passed"] for item in audit.exact
                ),
                "exact_checks_total": len(audit.exact),
                "theorem_guards_verified": len(audit.theorem_guards),
                "numerical_samples": 0,
                "absolute_finite_bfv_measure": None,
                "bosonic_contour_or_maslov_phase": None,
                "two_slab_gluing": None,
                "automatic_next": None,
                "result": RESULT_NAME,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
