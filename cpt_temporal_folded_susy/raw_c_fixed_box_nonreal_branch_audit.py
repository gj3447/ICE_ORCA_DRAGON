#!/usr/bin/env python3
"""Outward branch precondition on one nonreal raw-C box; not m(z) or RAQ."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp
from flint import acb, arb, ctx, fmpq


INPUT_NAME = "RAW_C_FIXED_BOX_NONREAL_BRANCH_AUDIT_INPUTS.json"
RESULT_NAME = "RAW_C_FIXED_BOX_NONREAL_BRANCH_AUDIT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_fixed_box_nonreal_branch_audit.py"
EXPECTED_INPUT_SHA256 = "332055b17292d2793d702528b58f94ebf544608b42b0f5f96950f719857f5a15"
CALCULATION_ID = "RawCFixedBoxNonrealBranchAudit"
RESULT_SCHEMA = "ice.raw-c-fixed-box-nonreal-branch-audit.result.v1"
RESULT_PREFIX = "RAW_C_FIXED_BOX_NONREAL_BRANCH_AUDIT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def exact_rational(text: str) -> fmpq:
    value = Fraction(text)
    return fmpq(value.numerator, value.denominator)


def interval_record(value: arb, digits: int = 36) -> dict[str, str]:
    return {
        "lower": value.lower().str(digits, radius=False),
        "upper": value.upper().str(digits, radius=False),
        "width_upper": (value.upper() - value.lower()).upper().str(digits, radius=False),
        "midpoint_radius": value.str(digits),
    }


def complex_record(value: acb, digits: int = 36) -> dict[str, Any]:
    return {
        "real": interval_record(value.real, digits),
        "imag": interval_record(value.imag, digits),
        "absolute_lower": value.abs_lower().str(digits, radius=False),
        "absolute_upper": value.abs_upper().str(digits, radius=False),
    }


def expected_caps() -> dict[str, int]:
    return {
        "wall_clock_seconds": 120, "stdout_bytes": 262144, "stderr_bytes": 262144,
        "changed_artifact_files": 12, "changed_artifact_bytes": 1000000,
        "symbolic_operations": 100, "ball_evaluations": 16, "root_calls": 0,
        "quadratures": 0, "ode_calls": 0, "sampling_points": 0,
        "automatic_descendants": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "actual_recessive_endpoint_data": None,
        "singular_endpoint_nonreal_weyl_function": None,
        "raw_C_spectral_measure": None,
        "raw_C_spectral_multiplicity": None,
        "stieltjes_inversion": None,
        "raw_C_rigging_test_space": None,
        "raw_C_rigging_map": None,
        "raw_C_physical_inner_product": None,
        "raw_C_RAQ_completion": None,
        "quantum_constraint_rescaling_equivalence": None,
        "selected_H_raw_C_unitary_intertwiner": None,
        "physics_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
        "gate1": "OPEN_PARTIAL_PROGRESS",
        "automatic_next": None,
    }


@dataclass
class Audit:
    controls: list[dict[str, Any]] = field(default_factory=list)
    seen: set[str] = field(default_factory=set, repr=False)
    ball_evaluations: int = 0

    def check(self, ident: str, passed: bool, statement: str, **data: Any) -> None:
        if ident in self.seen:
            raise AssertionError(f"duplicate control id: {ident}")
        self.seen.add(ident)
        self.controls.append({"id": ident, "passed": bool(passed), "statement": statement, **data})

    def count_ball(self) -> None:
        self.ball_evaluations += 1
        if self.ball_evaluations > expected_caps()["ball_evaluations"]:
            raise AssertionError("ball evaluation cap exceeded")


def finite_complex(value: acb) -> bool:
    text = str(value).lower()
    return "nan" not in text and "inf" not in text


def main() -> None:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded audit accepts no command-line arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    if sha256_bytes(raw) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input hash mismatch")
    cfg = json.loads(raw)
    if cfg.get("schema_version") != "ice.raw-c-fixed-box-nonreal-branch-audit.input.v1" or cfg.get("calculation_id") != CALCULATION_ID or cfg.get("numbered_phase") is not None:
        raise AssertionError("identity or unnumbered convention drift")
    if cfg.get("resource_caps") != expected_caps() or cfg.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("resource cap or null-scope mutation")
    if importlib.metadata.version("python-flint") != "0.9.0":
        raise AssertionError("python-flint runtime version drift")
    root = Path(__file__).resolve().parent.parent
    provenance = cfg["convention_provenance"]
    proxy_raw = (root / provenance["path"]).read_bytes()
    if sha256_bytes(proxy_raw) != provenance["sha256"]:
        raise AssertionError("convention provenance hash mismatch")

    audit = Audit()
    Q, z = sp.symbols("Q z", real=True)
    delta = z * sp.exp(-Q / 2) / (6 * sp.pi**2)
    A = 36 * sp.pi**4 * sp.exp(2 * Q) + 6 * sp.pi**2 * z * sp.exp(sp.Rational(3, 2) * Q)
    factor = 36 * sp.pi**4 * sp.exp(2 * Q) * (1 + delta)
    audit.check(
        "rawc.nonreal.branch.control1.factorization_and_halfline_envelope",
        bool(sp.simplify(A - factor) == 0 and sp.simplify(sp.diff(sp.exp(-Q / 2), Q) + sp.exp(-Q / 2) / 2) == 0),
        "Exact factorization and the decreasing exp(-Q/2) factor make the Q=4 z box a bound for all Q>=4.",
    )

    eta_bar = exact_rational(cfg["declared_conventions"]["analytic_eta_bar"])
    cut_bar = exact_rational(cfg["declared_conventions"]["analytic_cut_distance_lower"])
    analytic_delta_bound = arb(eta_bar)
    analytic_cut_bound = arb(cut_bar)
    tier_records: list[dict[str, Any]] = []
    tier_bounds: list[tuple[arb, arb]] = []
    tier_passes: list[bool] = []
    for precision in cfg["declared_conventions"]["precision_bits"]:
        ctx.prec = int(precision)
        z_box = acb(arb(0, arb(1) / 16), arb(1, arb(1) / 16))
        audit.count_ball()
        delta_4 = z_box * arb(-2).exp() / (6 * arb.pi() ** 2)
        audit.count_ball()
        relative = acb(1) + delta_4
        audit.count_ball()
        A_4 = 36 * arb.pi() ** 4 * arb(8).exp() * relative
        audit.count_ball()
        sqrt_A_4 = A_4.sqrt()
        audit.count_ball()
        delta_upper = delta_4.abs_upper()
        cut_lower = arb(1) - delta_upper
        re_sqrt_lower = sqrt_A_4.real.lower()
        finite = all(finite_complex(item) for item in (delta_4, relative, A_4, sqrt_A_4))
        passed = bool(
            finite
            and delta_upper < arb(1)
            and cut_lower > arb(0)
            and re_sqrt_lower > arb(0)
        )
        tier_passes.append(passed)
        tier_bounds.append((delta_upper, cut_lower))
        tier_records.append({
            "precision_bits": precision,
            "delta_at_Q4": complex_record(delta_4),
            "relative_factor_at_Q4": complex_record(relative),
            "A_at_Q4": complex_record(A_4),
            "principal_sqrt_A_at_Q4": complex_record(sqrt_A_4),
            "delta_absolute_upper": delta_upper.str(36, radius=False),
            "cut_distance_lower": cut_lower.str(36, radius=False),
            "Re_principal_sqrt_A_lower": re_sqrt_lower.str(36, radius=False),
            "finite": finite,
            "passed": passed,
        })
    audit.check(
        "rawc.nonreal.branch.control2.two_tier_outward_acb",
        all(tier_passes),
        "At both precision tiers, outward acb rectangles are finite, stay inside the unit branch disc, have positive cut distance, and give Re principal sqrt(A)>0 at Q=4.",
        tiers=tier_records,
    )

    # |z| < 9/8, exp(-2) < 1/7, pi^2 > 9 imply |delta| < 1/336.
    ball_eta_ok = all(delta_upper < analytic_delta_bound for delta_upper, _ in tier_bounds)
    ball_cut_ok = all(cut_lower > analytic_cut_bound for _, cut_lower in tier_bounds)
    halfline_re_lower = 6 * arb.pi() ** 2 * arb(4).exp() * (arb(1) - analytic_delta_bound).sqrt()
    audit.check(
        "rawc.nonreal.branch.control3.independent_elementary_separation",
        bool(eta_bar < fmpq(1, 1) and cut_bar == fmpq(1, 1) - eta_bar and ball_eta_ok and ball_cut_ok and halfline_re_lower > arb(0)),
        "The independent elementary eta and cut-distance bounds agree with both ball tiers and give a strictly positive all-Q>=4 lower bound for Re principal sqrt(A).",
        eta_bar=str(eta_bar),
        cut_distance_lower_bar=str(cut_bar),
        Re_principal_sqrt_A_lower_all_Q_ge_4=halfline_re_lower.str(36, radius=False),
    )

    passed = all(control["passed"] for control in audit.controls)
    verdict = "KEEP_FIXED_UHP_BOX_BRANCH_PRECONDITION_ONLY" if passed else "UNRESOLVED_FIXED_BOX"
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": cfg["decision_table"][0 if passed else 1]["programme_impact"],
        "question": cfg["question"],
        "primary_failure": cfg["primary_failure"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": sha256_bytes(raw)},
        "convention_provenance": provenance,
        "primary_sources": cfg["primary_sources"],
        "declared_conventions": cfg["declared_conventions"],
        "controls": audit.controls,
        "check_summary": {"controls_passed": sum(item["passed"] for item in audit.controls), "controls_total": 3, "all_controls_passed": passed},
        "branch_precondition": {
            "scope": "fixed UHP box branch separation and principal-square-root real-part positivity only",
            "all_Q_ge_4_Re_principal_sqrt_A_lower": audit.controls[2]["Re_principal_sqrt_A_lower_all_Q_ge_4"],
            "actual_recessive_endpoint_data_enclosed": False,
        },
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {"symbolic_operations": 2, "ball_evaluations": audit.ball_evaluations, "root_calls": 0, "quadratures": 0, "ode_calls": 0, "sampling_points": 0, "automatic_descendants": 0, "automatic_next": None},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256_bytes(Path(__file__).read_bytes())},
        "environment": {"python": platform.python_version(), "python_flint": importlib.metadata.version("python-flint"), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = sha256_bytes(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    print(RESULT_PREFIX + json.dumps({"run_status": "VALID_RUN", "verdict": verdict, "controls_passed": result["check_summary"]["controls_passed"], "controls_total": 3, "result_sha256": sha256_bytes(encoded), "result_size_bytes": len(encoded), "automatic_next": None}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
