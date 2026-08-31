#!/usr/bin/env python3
"""Finite BFV endpoint/determinant-line/gluing calibration with lapse cycle OPEN.

This is a parametrized-free-particle convention check.  It proves only that one
declared finite x-polarized endpoint pairing, two ordered nonzero ghost blocks,
and a two-slab Fresnel composition agree.  The initial lapse relative cycle is
an explicit OPEN input: this runner neither chooses a Picard--Lefschetz thimble
nor supplies a V=0/gravity absolute BFV measure.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "BFV_ENDPOINT_DETLINE_GLUING_CALIBRATION_INPUTS.json"
RESULT_NAME = "BFV_ENDPOINT_DETLINE_GLUING_CALIBRATION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/bfv_endpoint_detline_gluing_calibration.py"
EXPECTED_INPUT_SHA256 = "9afdc9c1b58e4fc6d0fa497b372b4cdb04568bcb4765c8ef30dcff7d2cc24460"
CALCULATION_ID = "BfvEndpointDetlineGluingCalibration"
RESULT_PREFIX = "BFV_ENDPOINT_DETLINE_GLUING_CALIBRATION_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def pfaffian_2x2(matrix: sp.Matrix) -> sp.Expr:
    if matrix.shape != (2, 2) or matrix + matrix.T != sp.zeros(2):
        raise ValueError("finite ghost block is not antisymmetric")
    return matrix[0, 1]


def load_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded calibration accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = digest(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed}")
    payload = json.loads(raw)
    if payload.get("schema_version") != "ice.bfv-endpoint-detline-gluing-calibration.input.v1":
        raise AssertionError("unexpected input schema")
    if payload.get("calculation_id") != CALCULATION_ID or payload.get("numbered_phase") is not None:
        raise AssertionError("calculation identity mutation")
    cycle = payload["declared_model"]["initial_lapse_relative_cycle"]
    if cycle != {
        "status": "OPEN",
        "selected_contour": None,
        "picard_lefschetz_selection": None,
        "meaning": "the calibration does not choose a relative lapse cycle, a thimble coefficient, or an above/below-origin class",
    }:
        raise AssertionError("lapse cycle must remain explicitly OPEN and unselected")
    return payload, observed


def exact_checks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    m, hbar, t1, t2 = sp.symbols("m hbar T_1 T_2", positive=True, real=True)
    xi, xm, xf = sp.symbols("x_i x_m x_f", real=True)
    ghost_1 = sp.Matrix([[0, 1], [-1, 0]])
    ghost_2 = sp.Matrix([[0, 1], [-1, 0]])
    pf_1, pf_2 = pfaffian_2x2(ghost_1), pfaffian_2x2(ghost_2)
    model = payload["declared_model"]
    endpoint_convention_preserved = (
        model["endpoint_polarization"]
        == "fixed x_i,x_f with interface x_m in the same x-polarization"
        and model["boundary_pairing"]
        == "integral_R dx psi_out_conjugate(x)*psi_in(x) on Schwartz test functions"
    )
    total = t1 + t2
    completed = sp.simplify(
        (xf - xm) ** 2 / t2 + (xm - xi) ** 2 / t1
        - (total / (t1 * t2)) * (xm - (t2 * xi + t1 * xf) / total) ** 2
        - (xf - xi) ** 2 / total
    )
    prefactor_squared = sp.simplify(
        (m / (2 * sp.pi * sp.I * hbar * t1))
        * (m / (2 * sp.pi * sp.I * hbar * t2))
        * (2 * sp.pi * sp.I * hbar * t1 * t2 / (m * total))
        - m / (2 * sp.pi * sp.I * hbar * total)
    )
    return [
        {"id": "bfv.endpoint.polarization.same_x_interface", "passed": endpoint_convention_preserved,
         "statement": "the hash-pinned input preserves one declared fixed-x endpoint/interface polarization and Schwartz pairing; this is a convention audit, not a derived gravity polarization"},
        {"id": "bfv.detline.slab_one.antisymmetric_nonzero", "passed": ghost_1 + ghost_1.T == sp.zeros(2) and ghost_1.det() != 0,
         "statement": "slab 1 ordered ghost block is antisymmetric and nondegenerate"},
        {"id": "bfv.detline.slab_two.antisymmetric_nonzero", "passed": ghost_2 + ghost_2.T == sp.zeros(2) and ghost_2.det() != 0,
         "statement": "slab 2 ordered ghost block is antisymmetric and nondegenerate"},
        {"id": "bfv.detline.concatenated_relative_orientation", "passed": pf_1 == 1 and pf_2 == 1 and sp.simplify(pf_1 * pf_2 - 1) == 0,
         "statement": "the declared concatenated finite Pfaffian reference orientation is +1"},
        {"id": "bfv.glue.phase_completion", "passed": completed == 0,
         "statement": "the two-slab x-polarized phase completes exactly to the T_1+T_2 phase"},
        {"id": "bfv.glue.prefactor_squared", "passed": prefactor_squared == 0,
         "statement": "the squared Fresnel-prefactor identity is exact; the declared common +i0 continuation supplies the remaining square-root branch choice"},
        {"id": "bfv.lapse.initial_relative_cycle_remains_open", "passed": True,
         "statement": "the input records no selected contour, Picard--Lefschetz selection, or global thimble coefficient"},
    ]


def main() -> int:
    payload, input_sha = load_input()
    checks = exact_checks(payload)
    all_passed = all(item["passed"] for item in checks)
    verdict = (
        "CALIBRATED_FINITE_ENDPOINT_DETLINE_GLUE_WITH_LAPSE_CYCLE_OPEN"
        if all_passed else "KILL_FINITE_ENDPOINT_DETLINE_GLUE_CALIBRATION"
    )
    result: dict[str, Any] = {
        "schema_version": "ice.bfv-endpoint-detline-gluing-calibration.result.v1",
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN" if all_passed else "FAIL_CLOSED",
        "verdict": verdict,
        "programme_impact": (
            "KEEP_FINITE_TOY_COMPATIBILITY_ONLY_NO_V0_ABSOLUTE_MEASURE"
            if all_passed else "DO_NOT_TRANSFER_THE_TOY_CONVENTION"
        ),
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {"path": RUNNER_RELPATH, "sha256": digest(Path(__file__).read_bytes())},
        "declared_model": payload["declared_model"],
        "assumptions": payload["assumptions"],
        "exact_checks": checks,
        "theorem_guards": [
            {
                "id": "bfv.glue.guard.common_fresnel_branch",
                "verified": True,
                "verification_mode": "ANALYTIC_HYPOTHESIS_AND_SCOPE_AUDIT_NOT_AN_EXECUTABLE_NUMERICAL_PREDICATE",
                "theorem": "damped Fresnel Gaussian composition on one continued square-root branch",
                "hypotheses": "T_1,T_2,m,hbar are positive and both slabs plus the interface Gaussian use the same +i0 continuation",
                "conclusion_and_scope": "the exact squared prefactor check lifts to the declared finite toy branch; it does not select a gravity lapse cycle, continuum determinant line, Stokes coefficient, or absolute measure",
            }
        ],
        "check_summary": {"exact_passed": sum(item["passed"] for item in checks), "exact_total": len(checks), "all_executable_checks_passed": all_passed},
        "lapse_cycle_status": "OPEN_UNSELECTED_INPUT_NOT_A_RESULT",
        "required_fail_closed_outputs": {
            "v0_absolute_bfv_measure": None,
            "gravity_or_minisuperspace_absolute_bfv_measure": None,
            "continuum_determinant_or_pfaffian_line": None,
            "global_lapse_relative_cycle": None,
            "picard_lefschetz_thimble_selection": None,
            "global_n_sigma": None,
            "physical_original_cycle": None,
            "gravity_endpoint_polarization": None,
            "gravity_two_slab_gluing_theorem": None,
            "physics_claim": None,
            "TOE_claim": None,
            "global_promotion": "PROHIBITED",
            "automatic_next": None,
        },
        "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "numerical_samples": 0, "automatic_descendants": 0},
        "environment": {"python": platform.python_version(), "sympy": sp.__version__},
    }
    result["result_payload_sha256_without_self"] = digest(canonical_bytes(result))
    encoded = canonical_bytes(result)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded + b"\n")
    print(f"{RESULT_PREFIX}{json.dumps(result, sort_keys=True)}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
