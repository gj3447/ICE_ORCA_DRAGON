#!/usr/bin/env python3
"""Fail-closed P7 readiness preflight; deliberately never calls CLASS or Cobaya."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any


INPUT_NAME = "P7_CLOSED_COSMOLOGY_LIKELIHOOD_READINESS_PREFLIGHT_INPUTS.json"
RESULT_NAME = "P7_CLOSED_COSMOLOGY_LIKELIHOOD_READINESS_PREFLIGHT_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/closed_cosmology_likelihood_readiness_preflight.py"
EXPECTED_INPUT_SHA256 = "e19eec909d32cb947b1c7e43289e987b61c05ca9ec3474bdb8f689c7ae087e1b"
CALCULATION_ID = "P7ClosedCosmologyLikelihoodReadinessPreflight"
RESULT_PREFIX = "P7_CLOSED_COSMOLOGY_LIKELIHOOD_READINESS_PREFLIGHT_RESULT="
ARTIFACT_CAP_BYTES = 1_000_000


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def load_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this preflight accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed = sha256(raw)
    if observed != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed}")
    payload = json.loads(raw)
    if payload.get("schema_version") != "ice.p7-closed-cosmology-likelihood-readiness-preflight.input.v1":
        raise AssertionError("unexpected input schema")
    if payload.get("calculation_id") != CALCULATION_ID or payload.get("numbered_phase") is not None:
        raise AssertionError("calculation identity mutation")
    if payload["resource_caps"]["external_solver_calls"] != 0:
        raise AssertionError("external solver invocation is prohibited")
    return payload, observed


def verify_upstream(root: Path, item: dict[str, str]) -> dict[str, str]:
    raw = (root / item["path"]).read_bytes()
    observed = sha256(raw)
    if observed != item["sha256"]:
        raise AssertionError(f"upstream file hash mismatch: {item['path']}")
    payload = json.loads(raw)
    if payload.get("run_status") != "VALID_RUN":
        raise AssertionError(f"upstream run not valid: {item['path']}")
    if payload.get("verdict") != item["required_verdict"]:
        raise AssertionError(f"upstream verdict mismatch: {item['path']}")
    if payload.get("result_payload_sha256_without_self") != item["payload_sha256_without_self"]:
        raise AssertionError(f"upstream payload digest mismatch: {item['path']}")
    return {"path": item["path"], "sha256": observed, "verdict": payload["verdict"]}


def main() -> int:
    payload, input_sha = load_input()
    root = Path(__file__).resolve().parent.parent
    upstream = [verify_upstream(root, item) for item in payload["upstream_results"]]
    gates = payload["readiness_gates"]
    missing = [name for name, gate in gates.items() if gate["status"] != "READY"]
    if not missing:
        raise AssertionError("this preflight is pinned to an absent-prerequisites state; do not turn it into a likelihood runner")
    mode = payload["supported_closed_s3_mode_convention"]
    expected_scalar = "n>=0, lambda_n=n(n+2), degeneracy (n+1)^2"
    expected_tensor = "TT n>=2, rough eigenvalue lambda_n-2, declared Lichnerowicz eigenvalue lambda_n+4, combined degeneracy 2(n-1)(n+3)"
    if mode["scalar"] != expected_scalar or mode["tensor"] != expected_tensor:
        raise AssertionError("mode convention exceeds or differs from pinned SVT ledger")
    result: dict[str, Any] = {
        "schema_version": "ice.p7-closed-cosmology-likelihood-readiness-preflight.result.v1",
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN",
        "verdict": "BLOCKED_P7_CLOSED_COSMOLOGY_LIKELIHOOD_NOT_READY_PREREQUISITES_ABSENT",
        "programme_impact": "DO_NOT_GENERATE_PRIMORDIAL_SPECTRA_OR_INVOKE_CLASS_COBAYA_UNTIL_EACH_NAMED_GATE_IS_READY",
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {"path": RUNNER_RELPATH, "sha256": sha256(Path(__file__).read_bytes())},
        "verified_upstream": upstream,
        "supported_closed_s3_mode_convention": mode,
        "readiness_gates": gates,
        "blocking_gate_ids": missing,
        "external_execution": {
            "CLASS_or_classy_imported": False,
            "CLASS_or_classy_invoked": False,
            "Cobaya_imported": False,
            "Cobaya_or_likelihood_invoked": False,
            "reason": "all seven prerequisite gates are absent"
        },
        "official_navigation_pins_only": payload["official_navigation_pins_only"],
        "required_null_outputs": {
            "common_raw_C_physical_product": None,
            "quantum_clock_map": None,
            "v_nonzero_background": None,
            "initial_quantum_state": None,
            "reheating_map": None,
            "primordial_normalization": None,
            "primordial_scalar_spectrum": None,
            "primordial_tensor_spectrum": None,
            "born_oppenheimer_correction": None,
            "decoherence_functional": None,
            "discrete_to_class_adapter": None,
            "CLASS_result": None,
            "Cobaya_likelihood": None,
            "posterior_or_sampling": None,
            "physics_claim": None,
            "global_promotion": "PROHIBITED",
            "automatic_next": None
        },
        "resource_accounting": {"root_calls": 0, "quadratures": 0, "ode_calls": 0, "numerical_samples": 0, "external_solver_calls": 0, "automatic_descendants": 0},
        "environment": {"python": platform.python_version()},
    }
    result["result_payload_sha256_without_self"] = sha256(canonical_bytes(result))
    encoded = canonical_bytes(result)
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded + b"\n")
    print(f"{RESULT_PREFIX}{json.dumps(result, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
