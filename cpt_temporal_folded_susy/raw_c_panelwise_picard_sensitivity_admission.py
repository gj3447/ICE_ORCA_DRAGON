#!/usr/bin/env python3
"""Fail-closed admission audit for raw-C panelwise Picard sensitivity work.

This never manufactures a lambda derivative from a real-axis
Liouville--Green direction bound. DLMF 2.7(iii) supplies the inherited scope;
Eckhardt--Gesztesy--Nichols--Teschl (arXiv:1208.4677) supplies no
repository-specific enclosure. SymPy is used only for exact identities.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


INPUT_NAME = "RAW_C_PANELWISE_PICARD_SENSITIVITY_ADMISSION_INPUTS.json"
RESULT_NAME = "RAW_C_PANELWISE_PICARD_SENSITIVITY_ADMISSION_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/raw_c_panelwise_picard_sensitivity_admission.py"
CALCULATION_ID = "RawCPanelwisePicardSensitivityAdmission"
RESULT_PREFIX = "RAW_C_PANELWISE_PICARD_SENSITIVITY_ADMISSION_RESULT="
EXPECTED_INPUT_SHA256 = "3723adce4fe1d149ce576e7207704f108be828935994501919d3278fcb804227"
ARTIFACT_CAP_BYTES = 1_000_000


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_upstream(root: Path, pin: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
    raw = (root / pin["path"]).read_bytes()
    observed = digest(raw)
    if observed != pin["sha256"]:
        raise AssertionError(f"upstream hash mismatch: {pin['path']}")
    value = json.loads(raw)
    payload = dict(value)
    recorded = payload.pop("result_payload_sha256_without_self", None)
    if value.get("verdict") != pin["required_verdict"] or recorded != pin["payload_sha256_without_self"]:
        raise AssertionError(f"upstream verdict or payload pin mismatch: {pin['path']}")
    if digest(canonical_bytes(payload)) != recorded or value.get("numbered_phase") is not None:
        raise AssertionError(f"upstream self-digest or phase mismatch: {pin['path']}")
    return value, {"path": pin["path"], "sha256": observed, "payload_sha256_without_self": recorded, "verdict": value["verdict"]}


MISSING = object()


def value_at(value: Any, path: list[str]) -> Any:
    current = value
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return MISSING
        current = current[key]
    return current


def present_nonnull(value: Any, path: list[str]) -> bool:
    observed = value_at(value, path)
    return observed is not MISSING and observed is not None


def exact_identities() -> list[dict[str, Any]]:
    x, C = sp.symbols("x C", positive=True, real=True)
    kappa, lam, rho, s = sp.symbols("kappa lambda rho s", real=True)
    field = (2 + 1 / x) * rho + (rho**2 + kappa**2 + sp.Rational(1, 4)) / x - lam * sp.sqrt(x / C)
    a = 2 + (1 + 2 * rho) / x
    work = [
        ("rawc.picard.admission.riccati_linearization", sp.diff(field, rho) - a, "The rho derivative of the declared Riccati field is the affine sensitivity coefficient."),
        ("rawc.picard.admission.lambda_forcing", sp.diff(field, lam) + sp.sqrt(x / C), "The fixed-normalization lambda forcing has the declared sign."),
        (
            "rawc.picard.admission.sensitivity_equation",
            sp.diff(field, rho) * s
            + sp.diff(field, lam)
            - (a * s - sp.sqrt(x / C)),
            "Differentiating the Riccati field gives s_x=a*s-sqrt(x/C); numerical use still requires normalization-fixed entering data.",
        ),
    ]
    records = []
    for identifier, residual, statement in work:
        simplified = sp.simplify(residual)
        records.append({"id": identifier, "kind": "EXACT_IDENTITY", "passed": bool(simplified == 0), "residual": str(simplified), "statement": statement})
    return records


def endpoint_rows(sharp: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    tiers = sharp["validated_calculation"]["parameter_tiers"]
    if not isinstance(tiers, dict):
        raise AssertionError("parameter_tiers must be a label-to-entry-list mapping")
    for tier_label, entries in tiers.items():
        if not isinstance(entries, list):
            raise AssertionError(f"parameter tier is not a list: {tier_label}")
        for entry in entries:
            interval = entry["downstream"]["scale_free_Gamma1"]
            lower, upper = float(interval["lower"]), float(interval["upper"])
            rows.append({"tier": tier_label, "label": entry["direction"]["label"], "decimal_digits": entry["direction"]["decimal_digits"], "lower": interval["lower"], "upper": interval["upper"], "contains_zero": lower <= 0 <= upper})
    return rows


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    raw_input = (root / INPUT_RELPATH).read_bytes()
    if digest(raw_input) != EXPECTED_INPUT_SHA256:
        raise AssertionError("input manifest hash mismatch")
    config = json.loads(raw_input)
    caps = config["resource_caps"]
    if config.get("numbered_phase") is not None or any(caps[key] != 0 for key in ("ode_calls", "quadrature_calls", "root_calls", "finite_difference_calls", "sampling_points")):
        raise AssertionError("this audit must remain unnumbered and non-computational")

    values: dict[str, dict[str, Any]] = {}
    upstream = []
    for pin in config["upstream_results"]:
        result, record = verify_upstream(root, pin)
        values[pin["path"]] = result
        upstream.append(record)
    sharp, boundary, plus = (values[pin["path"]] for pin in config["upstream_results"])
    schema_checks = {
        path: values[path].get("schema_version") == expected
        for path, expected in config["authoritative_upstream_schemas"].items()
    }
    if not all(schema_checks.values()):
        raise AssertionError("authoritative upstream schema mismatch")
    exact = exact_identities()
    if not all(check["passed"] for check in exact):
        raise AssertionError("exact sensitivity identity failed")
    endpoints = endpoint_rows(sharp)
    if len(endpoints) != 6 or not all(row["contains_zero"] for row in endpoints):
        raise AssertionError("expected six inherited zero-containing endpoint intervals")

    admission_paths = config["authoritative_admission_paths"]
    prerequisite_presence = {
        "actual_nonzero_lambda_plus_normalized_sensitivity_at_Qplus": present_nonnull(
            sharp,
            admission_paths["actual_nonzero_lambda_plus_normalized_sensitivity_at_Qplus"],
        ),
        "panelwise_actual_rho_tubes": present_nonnull(
            sharp, admission_paths["panelwise_actual_rho_tubes"]
        ),
        "actual_nonzero_lambda_declared_Gamma1_remainder": (
            present_nonnull(
                boundary, admission_paths["actual_nonzero_lambda_Gamma1_value"]
            )
            and present_nonnull(
                boundary,
                admission_paths["actual_nonzero_lambda_minus_tail_remainder"],
            )
        ),
    }
    admitted = all(prerequisite_presence.values())
    negative_controls = {
        "lambda_zero_boundary_derivative_is_not_actual_family": boundary["required_fail_closed_outputs"]["actual_nonzero_lambda_plus_recessive_solution"] is None,
        "plus_tail_exact_transform_is_explicitly_null": plus[
            "required_fail_closed_outputs"
        ]["exact_plus_endpoint_to_Q0_boundary_transform"]
        is None,
    }
    guards = [
        {"id": "rawc.picard.admission.guard.normalization", "verified": True, "theorem": "parameter differentiation of normalized Riccati families", "hypotheses": "The same lambda-dependent plus-end amplitude normalization fixes s at panel entry.", "scope": "No s(Q_plus) interval is inferred from a direction-only result."},
        {"id": "rawc.picard.admission.guard.panel_remainder", "verified": True, "theorem": "Picard/affine enclosure prerequisite", "hypotheses": "Each panel has a rho tube, s input and explicit remainder.", "scope": "The global nonlinear bound is not promoted to panelwise evidence."},
        {"id": "rawc.picard.admission.guard.sign", "verified": True, "theorem": "interval sign exclusion", "hypotheses": "Actual declared Gamma_1 plus complete left-tail remainder is available.", "scope": "All six inherited endpoint intervals contain zero; no sign or root claim is emitted."},
    ]
    verdict = "PANELWISE_PICARD_AFFINE_SENSITIVITY_ADMISSION_READY" if admitted else "PANELWISE_PICARD_AFFINE_SENSITIVITY_NOT_ADMITTED"
    result: dict[str, Any] = {
        "schema_version": "ice.raw-c-panelwise-picard-sensitivity-admission.result.v1",
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": verdict,
        "programme_impact": "NO_PANELWISE_SENSITIVITY_OR_SIGN_CALCULATION_IS_AUTHORIZED_BY_THIS_RESULT; MISSING_NORMALIZATION_FIXED_INPUTS_ARE_RECORDED." if not admitted else "A separately specified bounded panelwise calculation may be proposed; this audit does not execute it.",
        "input_manifest": {"path": INPUT_RELPATH, "sha256": digest(raw_input)},
        "runner": {"path": RUNNER_RELPATH, "sha256": digest(Path(__file__).read_bytes())},
        "upstream_results": upstream,
        "exact_checks": exact,
        "theorem_guards": guards,
        "validated_calculation": {"inherited_scale_free_endpoint_intervals": endpoints, "all_inherited_intervals_contain_zero": True, "authoritative_upstream_schema_checks": schema_checks, "authoritative_admission_paths": admission_paths, "prerequisite_presence": prerequisite_presence, "missing_prerequisites": [key for key, present in prerequisite_presence.items() if not present], "negative_controls": negative_controls, "admitted": admitted, "interpretation": "The exact affine equation identifies necessary inputs but supplies no numerical sensitivity interval without a normalization-fixed entering enclosure and panel remainders."},
        "resource_accounting": {"symbolic_operations": len(exact), "ode_calls": 0, "quadrature_calls": 0, "root_calls": 0, "finite_difference_calls": 0, "sampling_points": 0, "automatic_descendants": 0, "adjacent_result_files_written": 1},
        "required_fail_closed_outputs": config["required_fail_closed_outputs"],
    }
    result["result_payload_sha256_without_self"] = digest(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact exceeds byte cap")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    summary = {"run_status": result["run_status"], "verdict": verdict, "exact_passed": len(exact), "exact_total": len(exact), "admitted": admitted, "missing_prerequisites": result["validated_calculation"]["missing_prerequisites"], "result": RESULT_NAME, "result_sha256": digest(encoded), "result_bytes": len(encoded)}
    print(RESULT_PREFIX + json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
