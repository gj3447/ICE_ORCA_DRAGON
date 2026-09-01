#!/usr/bin/env python3
"""Compose the real sign strip and complete kappa derivative theorems.

This bounded audit performs no new ODE, quadrature, root, Bessel or interval
calculation.  It hash-pins the two independently certified raw results, checks
that they concern the same selected Q0-normalized functional on the same exact
rectangle, and audits the hypotheses of IVT, MVT and the compactness argument
for a continuous unique selector.  No nonreal Weyl, spectral-measure, RAQ,
velocity, global-root or physics conclusion is made.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any


INPUT_NAME = "RAW_C_FIXED_LAMBDA_ROOT_THEOREM_COMPOSITION_INPUTS.json"
RESULT_NAME = "RAW_C_FIXED_LAMBDA_ROOT_THEOREM_COMPOSITION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = (
    "cpt_temporal_folded_susy/raw_c_fixed_lambda_root_theorem_composition.py"
)
EXPECTED_INPUT_SHA256 = (
    "ad549c523fb5f06d43eeccd5a7299478fd0ca3a3bff445d6cbc13cfe2b4758a5"
)
CALCULATION_ID = "RawCFixedLambdaRootTheoremComposition"
RESULT_SCHEMA = "ice.raw-c-fixed-lambda-root-theorem-composition.result.v1"
RESULT_PREFIX = "RAW_C_FIXED_LAMBDA_ROOT_THEOREM_COMPOSITION_RESULT="
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


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120,
        "stdout_bytes": 262144,
        "stderr_bytes": 262144,
        "changed_artifact_files": 12,
        "changed_artifact_bytes": 1000000,
        "upstream_results": 2,
        "structural_checks": 15,
        "theorem_guards": 6,
        "ode_calls": 0,
        "quadrature_calls": 0,
        "root_calls": 0,
        "finite_difference_calls": 0,
        "sampling_points": 0,
        "bisection_steps": 0,
        "ball_function_evaluations": 0,
        "interval_rows": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "C1_or_differentiable_root_selector": None,
        "root_velocity_or_partial_lambda_G": None,
        "kappa_lambda_mixed_derivative": None,
        "root_location_intervals_or_samples": None,
        "roots_outside_declared_corridor_or_global_census": None,
        "absolute_actual_Gamma1_amplitude_or_orientation": None,
        "nonreal_weyl_m_function": None,
        "raw_C_spectral_measure_or_multiplicity": None,
        "selected_measurable_raw_C_self_adjoint_extension": None,
        "raw_C_rigging_test_space_or_RAQ": None,
        "raw_C_to_selected_H_quantum_equivalence": None,
        "BFV_or_physical_product": None,
        "physics_claim": None,
        "automatic_next": None,
    }


@dataclass
class Audit:
    checks: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set)

    def register(self, identifier: str) -> None:
        if identifier in self.seen:
            raise AssertionError(f"duplicate audit id: {identifier}")
        self.seen.add(identifier)

    def check(
        self, identifier: str, passed: bool, statement: str, **data: Any
    ) -> bool:
        self.register(identifier)
        record = {
            "id": identifier,
            "passed": bool(passed),
            "statement": statement,
        }
        record.update(data)
        self.checks.append(record)
        return bool(passed)

    def guard(
        self,
        identifier: str,
        verified: bool,
        theorem: str,
        hypotheses: str,
        conclusion_and_scope: str,
    ) -> bool:
        self.register(identifier)
        self.guards.append(
            {
                "id": identifier,
                "verified": bool(verified),
                "verification_mode": (
                    "HASH_PINNED_SCOPE_PLUS_ANALYTIC_THEOREM_APPLICABILITY_AUDIT"
                ),
                "theorem": theorem,
                "hypotheses": hypotheses,
                "conclusion_and_scope": conclusion_and_scope,
            }
        )
        return bool(verified)


def verify_upstream(
    root: Path, item: dict[str, str]
) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256_bytes(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream raw hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("schema_version") != item["schema_version"]:
        raise AssertionError(f"upstream schema mismatch: {item['path']}")
    if payload.get("verdict") != item["verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream run status mismatch: {item['path']}")
    if payload.get("numbered_phase") is not None:
        raise AssertionError(f"upstream numbered scope mismatch: {item['path']}")
    claimed = payload.get("result_payload_sha256_without_self")
    unsigned = dict(payload)
    unsigned.pop("result_payload_sha256_without_self", None)
    recomputed = sha256_bytes(canonical_bytes(unsigned))
    if claimed != item["payload_sha256_without_self"] or recomputed != claimed:
        raise AssertionError(f"upstream payload hash mismatch: {item['path']}")
    return payload, {
        "key": item["key"],
        "path": item["path"],
        "sha256": observed,
        "schema_version": item["schema_version"],
        "verdict": item["verdict"],
        "payload_sha256_without_self": claimed,
        "role": item["role"],
    }


def guard_verified(payload: dict[str, Any], identifier: str) -> bool:
    guards = payload.get("theorem_guards", [])
    matches = [row for row in guards if row.get("id") == identifier]
    return len(matches) == 1 and matches[0].get("verified") is True


def face_by_label(payload: dict[str, Any], label: str) -> dict[str, Any]:
    faces = payload["certified_calculation"]["face_final_intersections"]
    matches = [row for row in faces if row.get("label") == label]
    if len(matches) != 1:
        raise AssertionError(f"expected one {label} face")
    return matches[0]


def upstream_record(payload: dict[str, Any], path: str) -> dict[str, Any] | None:
    matches = [row for row in payload.get("upstream_results", []) if row.get("path") == path]
    if len(matches) != 1:
        return None
    return matches[0]


def load_inputs() -> tuple[
    dict[str, Any], str, dict[str, dict[str, Any]], list[dict[str, str]]
]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded theorem audit accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    input_sha = sha256_bytes(raw)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {input_sha}")
    inputs = json.loads(raw)
    if inputs.get("schema_version") != (
        "ice.raw-c-fixed-lambda-root-theorem-composition.input.v1"
    ):
        raise AssertionError("input schema mutation")
    if inputs.get("calculation_id") != CALCULATION_ID:
        raise AssertionError("calculation identity mutation")
    if inputs.get("numbered_phase") is not None:
        raise AssertionError("numbered descendants are forbidden")
    if inputs.get("resource_caps") != expected_caps():
        raise AssertionError("resource caps mutation")
    if inputs.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed outputs mutation")

    root = Path(__file__).resolve().parent.parent
    payloads: dict[str, dict[str, Any]] = {}
    records: list[dict[str, str]] = []
    for item in inputs["upstream_results"]:
        payload, record = verify_upstream(root, item)
        if item["key"] in payloads:
            raise AssertionError(f"duplicate upstream key: {item['key']}")
        payloads[item["key"]] = payload
        records.append(record)
    if set(payloads) != {"sign_strip", "complete_kappa_derivative"}:
        raise AssertionError("unexpected upstream set")
    return inputs, input_sha, payloads, records


def audit_composition(
    audit: Audit,
    inputs: dict[str, Any],
    payloads: dict[str, dict[str, Any]],
    records: list[dict[str, str]],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    sign = payloads["sign_strip"]
    derivative = payloads["complete_kappa_derivative"]
    declared = inputs["declared_scope"]
    records_by_key = {row["key"]: row for row in records}

    sign_upstream_ok = audit.check(
        "rawc.root_theorem.upstream.sign_strip",
        records_by_key["sign_strip"]["sha256"]
        == inputs["upstream_results"][0]["sha256"],
        "The hash-pinned sign strip is a valid unnumbered run with the required schema, verdict and canonical payload digest.",
    )
    derivative_upstream_ok = audit.check(
        "rawc.root_theorem.upstream.complete_kappa_derivative",
        records_by_key["complete_kappa_derivative"]["sha256"]
        == inputs["upstream_results"][1]["sha256"],
        "The hash-pinned complete kappa derivative is a valid unnumbered run with the required schema, verdict and canonical payload digest.",
    )

    sign_conventions = sign["declared_conventions"]
    derivative_conventions = derivative["declared_conventions"]
    sign_root = sign_conventions["root_bracket_1"]
    sign_left = Fraction(sign_root["left_exact"]) - Fraction(1, 1000)
    sign_right = Fraction(sign_root["right_exact"]) + Fraction(1, 1000)
    derivative_corridor = derivative_conventions["kappa_corridor"]
    corridor_ok = audit.check(
        "rawc.root_theorem.scope.kappa_corridor",
        sign_left == Fraction(declared["kappa_corridor"]["left_exact"])
        == Fraction(derivative_corridor["left_exact"])
        and sign_right == Fraction(declared["kappa_corridor"]["right_exact"])
        == Fraction(derivative_corridor["right_exact"])
        and sign_left < sign_right,
        "The sign strip and complete derivative use the identical exact expanded root-1 kappa corridor.",
        left_exact=declared["kappa_corridor"]["left_exact"],
        right_exact=declared["kappa_corridor"]["right_exact"],
    )

    sign_lambda = sign_conventions["lambda_slab"]
    derivative_lambda = derivative_conventions["lambda_slab"]
    lambda_ok = audit.check(
        "rawc.root_theorem.scope.lambda_slab",
        sign_lambda == derivative_lambda == declared["lambda_slab"]
        and Fraction(sign_lambda["left_exact"])
        < Fraction(sign_lambda["right_exact"]),
        "The two certificates use the identical exact closed lambda slab.",
        lambda_slab=declared["lambda_slab"],
    )
    q0_ok = audit.check(
        "rawc.root_theorem.scope.Q0",
        sign_conventions["Q_0"]
        == derivative_conventions["Q_0"]
        == declared["Q_0"],
        "Both certificates use the same Q0 normalization point.",
        Q_0=declared["Q_0"],
    )
    functional_ok = audit.check(
        "rawc.root_theorem.scope.projective_functional",
        sign_conventions["projective_functional"]
        == declared["signstrip_projective_functional"]
        and derivative_conventions["projective_functional"]
        == declared["projective_functional"],
        "The sign-strip functional's explicit U normalization and the derivative certificate's base formula define exactly the same selected Q0-normalized G.",
        projective_functional=declared["projective_functional"],
    )

    corridor_charts = [
        row
        for row in sign["certified_calculation"]["q0_final_charts"]
        if row.get("label") == "corridor"
    ]
    selected_family_ok = audit.check(
        "rawc.root_theorem.scope.selected_family_and_chart",
        sign_conventions["selected_actual_family"]
        == declared["selected_actual_family"]
        and len(corridor_charts) == 1
        and corridor_charts[0].get("certified") is True
        and corridor_charts[0].get("Q0_amplitude_excludes_zero") is True
        and guard_verified(sign, "rawc.signstrip.guard.selected_actual_family")
        and guard_verified(sign, "rawc.signstrip.guard.projective_normalization")
        and guard_verified(
            derivative, "rawc.kappa_tail.guard.selected_projective_seed"
        ),
        "The same Liouville-Green selected real plus family has one uniformly nonzero Q0 projective chart throughout the rectangle.",
    )
    reference_ok = audit.check(
        "rawc.root_theorem.scope.reference_instantiation",
        sign_conventions["reference_instantiation"]
        == declared["signstrip_reference_instantiation"]
        and derivative_conventions["reference_equation"]
        == declared["combined_reference_equation"],
        "The sign-strip c_p notation is exactly instantiated as the same c_kappa reference with coefficient V-kappa^2.",
    )
    boundary_ok = audit.check(
        "rawc.root_theorem.scope.boundary_and_wronskian",
        sign_conventions["boundary_map"] == declared["signstrip_boundary_map"]
        and derivative_conventions["boundary_map"] == declared["boundary_map"]
        and derivative_conventions["wronskian"] == declared["wronskian"],
        "The p-to-kappa reference bridge preserves the declared Gamma_1 boundary line and repository Wronskian orientation.",
    )

    continuity_ok = audit.check(
        "rawc.root_theorem.hypothesis.joint_continuity",
        guard_verified(sign, "rawc.signstrip.guard.complete_tail_continuity"),
        "The sign-strip certificate supplies joint real continuity of this same complete normalized G on the closed rectangle.",
    )
    left_face = face_by_label(sign, "left_face")
    right_face = face_by_label(sign, "right_face")
    left_interval = left_face["g_Q0_normalized"]
    right_interval = right_face["g_Q0_normalized"]
    face_signs_ok = audit.check(
        "rawc.root_theorem.hypothesis.opposite_face_signs",
        left_face.get("certified") is True
        and right_face.get("certified") is True
        and left_face.get("strict_sign") == "NEGATIVE"
        and right_face.get("strict_sign") == "POSITIVE"
        and Decimal(left_interval["upper"]) < 0
        and Decimal(right_interval["lower"]) > 0
        and left_face["lambda_slab"] == declared["lambda_slab"]
        and right_face["lambda_slab"] == declared["lambda_slab"],
        "For every lambda in the shared slab, the complete left face is strictly negative and the complete right face is strictly positive.",
        left_face=left_interval,
        right_face=right_interval,
    )

    differentiability_ok = audit.check(
        "rawc.root_theorem.hypothesis.interior_kappa_differentiability",
        derivative_conventions["derivative_scope"]
        == declared["derivative_scope"]
        and guard_verified(
            derivative, "rawc.kappa_tail.guard.differentiated_improper_limit"
        ),
        "For each fixed lambda, this same G is ordinarily kappa-differentiable throughout the open corridor; face derivatives are only one-sided and are not used.",
    )
    derivative_interval = derivative["certified_calculation"][
        "partial_kappa_G_complete"
    ]
    derivative_positive_ok = audit.check(
        "rawc.root_theorem.hypothesis.uniform_positive_kappa_derivative",
        Decimal(derivative_interval["lower"]) > 0
        and Decimal(derivative_interval["lower"])
        <= Decimal(derivative_interval["upper"])
        and derivative["certified_calculation"]["partial_kappa_G_strict_sign"]
        == "POSITIVE"
        and derivative["certified_calculation"]["partial_kappa_G_zero_excluded"]
        is True,
        "The complete fixed-lambda kappa derivative has a uniform strictly positive lower bound on the shared open corridor.",
        partial_kappa_G=derivative_interval,
    )

    pinned_sign = upstream_record(
        derivative,
        "cpt_temporal_folded_susy/RAW_C_CORRELATED_KAPPA_LAMBDA_GAMMA1_SIGN_STRIP_RESULT.json",
    )
    derivative_pins_sign_ok = audit.check(
        "rawc.root_theorem.provenance.derivative_consumes_sign_strip",
        pinned_sign is not None
        and pinned_sign.get("sha256") == records_by_key["sign_strip"]["sha256"]
        and pinned_sign.get("payload_sha256_without_self")
        == records_by_key["sign_strip"]["payload_sha256_without_self"],
        "The derivative result itself pins the exact sign-strip raw artifact and canonical payload used by this composition.",
    )

    theorem_hypotheses_ok = all(
        (
            sign_upstream_ok,
            derivative_upstream_ok,
            corridor_ok,
            lambda_ok,
            q0_ok,
            functional_ok,
            selected_family_ok,
            reference_ok,
            boundary_ok,
            continuity_ok,
            face_signs_ok,
            differentiability_ok,
            derivative_positive_ok,
            derivative_pins_sign_ok,
        )
    )
    audit.check(
        "rawc.root_theorem.composition.all_hypotheses",
        theorem_hypotheses_ok,
        "All scope, continuity, sign and differentiability hypotheses needed by the declared calculus composition hold simultaneously.",
    )

    scope_guard = audit.guard(
        "rawc.root_theorem.guard.same_function_scope",
        all(
            (
                corridor_ok,
                lambda_ok,
                q0_ok,
                functional_ok,
                selected_family_ok,
                reference_ok,
                boundary_ok,
            )
        ),
        "Projective normalization and exact p-to-kappa reference instantiation",
        "Both upstream results are hash-pinned, use the identical rectangle and Q0-normalized selected plus family, and the sign-strip c_p reference is exactly the c_kappa reference after p^2=(2/3)kappa^2.",
        "The sign and derivative statements concern one and the same real normalized G. This does not establish an absolute Gamma_1 amplitude or orientation.",
    )
    ivt_guard = audit.guard(
        "rawc.root_theorem.guard.fixed_lambda_IVT",
        scope_guard and continuity_ok and face_signs_ok,
        "Intermediate value theorem",
        "For each fixed lambda, G is continuous on the closed kappa corridor and has strict opposite signs at its two faces.",
        "Every lambda in the declared closed slab has at least one G zero in the open kappa corridor.",
    )
    mvt_guard = audit.guard(
        "rawc.root_theorem.guard.fixed_lambda_MVT_uniqueness",
        ivt_guard and differentiability_ok and derivative_positive_ok,
        "Mean value theorem and strict monotonicity",
        "For each fixed lambda, G is continuous on the closed corridor, differentiable in its interior and partial_kappa G is strictly positive there.",
        "G is strictly increasing in kappa and the IVT zero is the unique zero in the declared corridor.",
    )
    transverse_guard = audit.guard(
        "rawc.root_theorem.guard.fixed_lambda_kappa_transversality",
        mvt_guard and derivative_positive_ok,
        "Simple-zero criterion in the kappa direction",
        "The unique root lies in the open corridor where the ordinary derivative exists and partial_kappa G has the displayed positive lower bound.",
        "The normalized G zero is simple and transverse with respect to kappa. This is not a two-parameter C1 submersion or a velocity statement.",
    )
    selector_guard = audit.guard(
        "rawc.root_theorem.guard.continuous_unique_selector",
        mvt_guard and continuity_ok and face_signs_ok,
        "Compactness and uniqueness of zeros under joint continuity",
        "G is jointly continuous on compact K times Lambda, every lambda has one interior root, and the face values never vanish.",
        "The unique roots define one continuous selector kappa_star(lambda) on the closed slab. No C1, differentiable or analytic selector is claimed.",
    )
    separation_guard = audit.guard(
        "rawc.root_theorem.guard.scope_separation",
        inputs["required_fail_closed_outputs"] == expected_nulls(),
        "Computational-workbench claim separation",
        "Only two real normalized certificates and elementary calculus/compactness theorems are composed; no nonreal solution, spectral transform, test space or group average is evaluated.",
        "Velocity, roots outside the corridor, absolute amplitude/orientation, Weyl m(z), spectral measure, RAQ, C/H equivalence, BFV and physics remain null.",
    )

    certified = all(
        (
            theorem_hypotheses_ok,
            scope_guard,
            ivt_guard,
            mvt_guard,
            transverse_guard,
            selector_guard,
            separation_guard,
        )
    )
    theorem = None
    if certified:
        theorem = {
            "scope": "the exact declared real K times Lambda rectangle for the selected Q0-normalized plus family",
            "projective_functional": declared["projective_functional"],
            "kappa_corridor": declared["kappa_corridor"],
            "lambda_slab": declared["lambda_slab"],
            "face_intervals": {
                "left": left_interval,
                "right": right_interval,
            },
            "partial_kappa_G_complete": derivative_interval,
            "strict_kappa_monotonicity_per_fixed_lambda": True,
            "exactly_one_open_corridor_G_zero_per_lambda": True,
            "unique_zero_is_kappa_simple_and_transverse": True,
            "normalized_G_and_selected_declared_Gamma1_have_same_unique_zero": True,
            "continuous_unique_selector_on_closed_lambda_slab": True,
            "selector_regularity_boundary": (
                "continuous only; no C1/differentiable/analytic lambda selector, "
                "partial_lambda G or velocity is certified"
            ),
        }

    facts = {
        "same_exact_function_family_rectangle": scope_guard,
        "joint_continuity": continuity_ok,
        "strict_opposite_faces": face_signs_ok,
        "ordinary_interior_kappa_derivative": differentiability_ok,
        "uniform_positive_kappa_derivative": derivative_positive_ok,
        "IVT_applicable": ivt_guard,
        "MVT_applicable": mvt_guard,
        "unique_root_kappa_transverse": transverse_guard,
        "continuous_selector_applicable": selector_guard,
    }
    return theorem, facts


def write_result(path: Path, payload: dict[str, Any]) -> tuple[str, int]:
    payload["result_payload_sha256_without_self"] = sha256_bytes(
        canonical_bytes(payload)
    )
    encoded = canonical_bytes(payload)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact byte cap exceeded")
    path.write_bytes(encoded)
    return sha256_bytes(encoded), len(encoded)


def main() -> None:
    inputs, input_sha, payloads, upstream_records = load_inputs()
    audit = Audit()
    certified_theorem, composition_facts = audit_composition(
        audit, inputs, payloads, upstream_records
    )
    if len(audit.checks) != expected_caps()["structural_checks"]:
        raise AssertionError("structural check count mismatch")
    if len(audit.guards) != expected_caps()["theorem_guards"]:
        raise AssertionError("theorem guard count mismatch")
    all_checks = all(row["passed"] for row in audit.checks)
    all_guards = all(row["verified"] for row in audit.guards)
    certified = certified_theorem is not None and all_checks and all_guards
    verdict = (
        "CERTIFY_UNIQUE_KAPPA_TRANSVERSE_NORMALIZED_G_ZERO_AND_CONTINUOUS_SELECTOR_PER_LAMBDA_ONLY"
        if certified
        else "NOT_CERTIFIED_FIXED_LAMBDA_ROOT_THEOREM_COMPOSITION"
    )

    result = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "upstream_results": upstream_records,
        "declared_scope": inputs["declared_scope"],
        "calculus_theorem": inputs["calculus_theorem"],
        "composition_facts": composition_facts,
        "structural_checks": audit.checks,
        "theorem_guards": audit.guards,
        "check_summary": {
            "structural_total": len(audit.checks),
            "structural_passed": sum(row["passed"] for row in audit.checks),
            "theorem_guards": len(audit.guards),
            "theorem_guards_verified": sum(
                row["verified"] for row in audit.guards
            ),
            "all_checks_passed": all_checks and all_guards,
        },
        "certified_theorem": certified_theorem,
        "required_fail_closed_outputs": inputs["required_fail_closed_outputs"],
        "resource_accounting": {
            "upstream_results": len(upstream_records),
            "structural_checks": len(audit.checks),
            "theorem_guards": len(audit.guards),
            "ode_calls": 0,
            "quadrature_calls": 0,
            "root_calls": 0,
            "finite_difference_calls": 0,
            "sampling_points": 0,
            "bisection_steps": 0,
            "ball_function_evaluations": 0,
            "interval_rows": 0,
            "automatic_descendants": 0,
            "adjacent_result_files_written": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "non_claim": (
            "This is a fixed-lambda real normalized root theorem on one declared "
            "corridor. It is not a root location, velocity, global census, "
            "absolute Gamma_1 orientation, nonreal Weyl function, spectral "
            "measure, RAQ/BFV result, empirical result or physics discovery."
        ),
    }
    result_path = Path(__file__).with_name(RESULT_NAME)
    result_sha, result_size = write_result(result_path, result)
    print(
        RESULT_PREFIX
        + json.dumps(
            {
                "run_status": result["run_status"],
                "verdict": verdict,
                "structural_passed": result["check_summary"]["structural_passed"],
                "structural_total": result["check_summary"]["structural_total"],
                "theorem_guards": result["check_summary"]["theorem_guards"],
                "result_sha256": result_sha,
                "result_size_bytes": result_size,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
