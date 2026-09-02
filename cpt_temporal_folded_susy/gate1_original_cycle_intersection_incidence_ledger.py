#!/usr/bin/env python3
"""Build a fail-closed Gate-1 incidence ledger from committed P38--P41 records.

The bounded audit preserves recorded local orientation signs while classifying
global-incidence eligibility as INTEGER, UNRESOLVED, or OUT_OF_SCOPE.  It does
not infer an original joint cycle, rerun a historical numbered calculation, or
emit a global Picard--Lefschetz coefficient.
"""

from __future__ import annotations

import copy
import hashlib
import json
import platform
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


INPUT_NAME = "GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_INPUTS.json"
RESULT_NAME = "GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_RESULT.json"
INPUT_RELPATH = f"cpt_temporal_folded_susy/{INPUT_NAME}"
RUNNER_RELPATH = "cpt_temporal_folded_susy/gate1_original_cycle_intersection_incidence_ledger.py"
EXPECTED_INPUT_SHA256 = "a17978a38b5e0c6df0f2788022681f0e402a0fe9bec6b02f0a3bb60e095c306f"
CALCULATION_ID = "Gate1OriginalCycleIntersectionIncidenceLedger"
RESULT_PREFIX = "GATE1_ORIGINAL_CYCLE_INTERSECTION_INCIDENCE_LEDGER_RESULT="
INPUT_SCHEMA = "ice.gate1-original-cycle-intersection-incidence-ledger.input.v1"
RESULT_SCHEMA = "ice.gate1-original-cycle-intersection-incidence-ledger.result.v1"
ARTIFACT_CAP_BYTES = 1_000_000
STATUS_VALUES = ("INTEGER", "UNRESOLVED", "OUT_OF_SCOPE")
SCOPE_VALUES = ("IN_SCOPE_RECORDED_CANDIDATE", "OUTSIDE_GLOBAL_INCIDENCE_DOMAIN")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode()


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
        "numerical_samples": 0,
    }


def expected_nulls() -> dict[str, Any]:
    return {
        "bounded_chain_signed_sum": None,
        "complete_global_signed_intersection_vector": None,
        "global_n_sigma": None,
        "original_physical_joint_cycle": None,
        "gate1_closure": None,
        "cutoff_or_continuum_limit": None,
        "physics_claim": None,
        "empirical_claim": None,
        "quantum_gravity_claim": None,
        "TOE_claim": None,
        "global_promotion": "PROHIBITED",
    }


def checked_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise AssertionError(f"unsafe repository-relative path: {value}")
    return path


def is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def load_input() -> tuple[dict[str, Any], str]:
    if len(sys.argv) != 1:
        raise AssertionError("this bounded incidence audit accepts no arguments")
    raw = Path(__file__).with_name(INPUT_NAME).read_bytes()
    observed_sha = digest(raw)
    if observed_sha != EXPECTED_INPUT_SHA256:
        raise AssertionError(f"input hash mismatch: {observed_sha}")
    payload = json.loads(raw)
    if payload.get("schema_version") != INPUT_SCHEMA:
        raise AssertionError("unexpected input schema")
    if payload.get("calculation_id") != CALCULATION_ID:
        raise AssertionError("calculation identity mutation")
    if payload.get("numbered_phase") is not None:
        raise AssertionError("this work unit must remain unnumbered")
    if payload.get("principal_failure_class") != "inference":
        raise AssertionError("principal failure class must remain inference")
    if payload.get("resource_caps") != expected_caps():
        raise AssertionError("resource-cap mutation")
    if payload.get("required_fail_closed_outputs") != expected_nulls():
        raise AssertionError("fail-closed output mutation")
    if payload["graph_contract"].get("status_change_claimed") is not False:
        raise AssertionError("this audit does not claim a graph-status change")
    if payload["graph_contract"].get("ontology_write_requested") is not False:
        raise AssertionError("this audit does not authorize an ontology write")
    return payload, observed_sha


def verify_source_artifacts(
    root: Path, payload: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    source_ids = [item["id"] for item in payload["source_artifacts"]]
    if len(source_ids) != len(set(source_ids)):
        raise AssertionError("duplicate source-artifact ID")
    verified: list[dict[str, Any]] = []
    raw_by_id: dict[str, bytes] = {}
    for item in payload["source_artifacts"]:
        relative = checked_relative_path(item["path"])
        raw = (root / relative).read_bytes()
        observed_sha = digest(raw)
        if observed_sha != item["sha256"]:
            raise AssertionError(f"source hash mismatch: {item['path']}")
        text = raw.decode("utf-8")
        missing_markers = [
            marker for marker in item["required_markers"] if marker not in text
        ]
        if missing_markers:
            raise AssertionError(
                f"source marker mismatch: {item['path']}: {missing_markers}"
            )
        raw_by_id[item["id"]] = raw
        verified.append(
            {
                "id": item["id"],
                "path": item["path"],
                "sha256": observed_sha,
                "role": item["role"],
                "required_marker_count": len(item["required_markers"]),
            }
        )
    return verified, raw_by_id


def verify_graph_and_signal(
    root: Path, payload: dict[str, Any], raw_by_id: dict[str, bytes]
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    graph = json.loads(raw_by_id["cpt_graph"])
    graph_nodes = {node["id"]: node for node in graph["nodes"]}
    verified_bindings: list[dict[str, str]] = []
    for binding in payload["graph_bindings"]:
        node = graph_nodes.get(binding["node_id"])
        if node is None:
            raise AssertionError(f"missing graph node: {binding['node_id']}")
        if node.get("type") != binding["type"] or node.get("state") != binding["state"]:
            raise AssertionError(f"graph binding drift: {binding['node_id']}")
        verified_bindings.append(dict(binding))

    graph_contract = payload["graph_contract"]
    if graph_contract["anchor_node_id"] not in graph_nodes:
        raise AssertionError("canonical Gate-1 anchor is missing")
    for node_id in graph_contract["intended_consumer_node_ids"]:
        if node_id not in graph_nodes:
            raise AssertionError(f"missing intended graph consumer: {node_id}")
    for source in payload["primary_sources"]:
        node = graph_nodes.get(source["canonical_node_id"])
        if node is None or node.get("type") != "source" or node.get("state") != "PRIMARY":
            raise AssertionError(
                f"primary-source graph binding drift: {source['canonical_node_id']}"
            )
    for entry in payload["entries"]:
        for node_id in entry["evidence_node_ids"]:
            if node_id not in graph_nodes:
                raise AssertionError(f"missing entry evidence node: {node_id}")

    signal_spec = payload["intuition_signal"]
    signal_path = checked_relative_path(signal_spec["path"])
    signal_raw = (root / signal_path).read_bytes()
    signal_sha = digest(signal_raw)
    if signal_sha != signal_spec["sha256"]:
        raise AssertionError("scientific-intuition signal artifact hash mismatch")
    signal_payload = json.loads(signal_raw)
    matching = [
        signal
        for signal in signal_payload["signals"]
        if signal["id"] == signal_spec["signal_id"]
    ]
    if len(matching) != 1:
        raise AssertionError("scientific-intuition signal must resolve exactly once")
    signal = matching[0]
    if signal.get("status") != signal_spec["required_status"]:
        raise AssertionError("scientific-intuition signal status drift")
    if signal.get("principal_failure_class") != signal_spec["required_principal_failure_class"]:
        raise AssertionError("scientific-intuition failure class drift")
    if signal.get("does_not_authorize_execution") is not True:
        raise AssertionError("scientific-intuition signal authorization boundary drift")
    if signal_spec.get("required_does_not_authorize_execution") is not True:
        raise AssertionError("input must not treat an intuition signal as execution authority")
    if signal.get("target") != {
        "graph": graph_contract["graph"],
        "node": graph_contract["anchor_node_id"],
    }:
        raise AssertionError("scientific-intuition target drift")
    signal_record = {
        "path": signal_spec["path"],
        "sha256": signal_sha,
        "signal_id": signal["id"],
        "status": signal["status"],
        "target": signal["target"],
        "principal_failure_class": signal["principal_failure_class"],
        "does_not_authorize_execution": signal["does_not_authorize_execution"],
    }
    return verified_bindings, signal_record


def validate_input_shape(payload: dict[str, Any]) -> list[str]:
    prerequisite_ids = [item["id"] for item in payload["eligibility_prerequisites"]]
    if len(prerequisite_ids) != len(set(prerequisite_ids)):
        raise AssertionError("duplicate eligibility prerequisite")
    entry_ids = [entry["id"] for entry in payload["entries"]]
    if len(entry_ids) != len(set(entry_ids)):
        raise AssertionError("duplicate predeclared entry ID")
    declared_count = payload["enumeration_boundary"]["declared_record_count"]
    if len(entry_ids) != declared_count or declared_count != 14:
        raise AssertionError("predeclared enumeration boundary mismatch")
    if payload["enumeration_boundary"]["global_census_complete"] is not False:
        raise AssertionError("record audit must not claim a global census")
    source_ids = {item["id"] for item in payload["source_artifacts"]}
    for entry in payload["entries"]:
        if entry["source_artifact_id"] not in source_ids:
            raise AssertionError(f"unknown source artifact: {entry['id']}")
        if entry["scope_relation"] not in SCOPE_VALUES:
            raise AssertionError(f"invalid scope relation: {entry['id']}")
        if set(entry["prerequisites"]) != set(prerequisite_ids):
            raise AssertionError(f"prerequisite-key drift: {entry['id']}")
        if not all(isinstance(value, bool) for value in entry["prerequisites"].values()):
            raise AssertionError(f"non-boolean prerequisite: {entry['id']}")
        if entry["local_orientation_sign"] not in (None, -1, 1):
            raise AssertionError(f"invalid local orientation sign: {entry['id']}")
        declared_integer = entry["declared_global_intersection_integer"]
        if declared_integer is not None and not is_integer(declared_integer):
            raise AssertionError(f"invalid declared intersection integer: {entry['id']}")
        if not entry["evidence_locator"]:
            raise AssertionError(f"missing evidence locator: {entry['id']}")
        if "status" in entry:
            raise AssertionError("input entries must not predeclare a derived status")
    return prerequisite_ids


def classify_entry(
    entry: dict[str, Any],
    prerequisite_ids: list[str],
    source_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    scope_relation = entry["scope_relation"]
    declared_integer = entry["declared_global_intersection_integer"]
    missing = [
        prerequisite_id
        for prerequisite_id in prerequisite_ids
        if not entry["prerequisites"][prerequisite_id]
    ]
    if entry["original_cycle_ref"] is None:
        missing.append("original_cycle_ref")
    if entry["global_upward_cycle_ref"] is None:
        missing.append("global_upward_cycle_ref")
    if entry["sheet_ref"] is None:
        missing.append("sheet_ref")
    if declared_integer is None:
        missing.append("global_intersection_integer_not_recorded")

    if scope_relation == "OUTSIDE_GLOBAL_INCIDENCE_DOMAIN":
        if declared_integer is not None:
            raise AssertionError(
                f"out-of-scope entry carries an integer: {entry['id']}"
            )
        if not isinstance(entry["out_of_scope_reason"], str) or not entry[
            "out_of_scope_reason"
        ].strip():
            raise AssertionError(f"out-of-scope reason missing: {entry['id']}")
        status = "OUT_OF_SCOPE"
        missing = []
    else:
        if entry["out_of_scope_reason"] is not None:
            raise AssertionError(f"in-scope entry has exclusion reason: {entry['id']}")
        locator_complete = all(
            entry[key] is not None
            for key in ("original_cycle_ref", "global_upward_cycle_ref", "sheet_ref")
        )
        all_prerequisites = all(entry["prerequisites"].values())
        eligible_integer = (
            all_prerequisites and locator_complete and is_integer(declared_integer)
        )
        if declared_integer is not None and not eligible_integer:
            raise AssertionError(
                f"global integer supplied without complete prerequisites: {entry['id']}"
            )
        status = "INTEGER" if eligible_integer else "UNRESOLVED"

    source = source_by_id[entry["source_artifact_id"]]
    return {
        "id": entry["id"],
        "status": status,
        "candidate_kind": entry["candidate_kind"],
        "declared_model_scope": entry["declared_model_scope"],
        "scope_relation": scope_relation,
        "out_of_scope_reason": entry["out_of_scope_reason"],
        "local_orientation_sign": entry["local_orientation_sign"],
        "global_intersection_integer": declared_integer,
        "original_cycle_ref": entry["original_cycle_ref"],
        "global_upward_cycle_ref": entry["global_upward_cycle_ref"],
        "saddle_or_candidate_ref": entry["saddle_or_candidate_ref"],
        "sheet_ref": entry["sheet_ref"],
        "prerequisites": dict(entry["prerequisites"]),
        "missing_requirements": missing,
        "evidence": {
            "path": source["path"],
            "sha256": source["sha256"],
            "locator": entry["evidence_locator"],
            "graph_node_ids": entry["evidence_node_ids"],
        },
    }


def independent_verify(result: dict[str, Any], expected_entry_count: int) -> dict[str, Any]:
    """Verify the emitted data shape without calling the classifier."""

    entries = result["incidence_ledger"]
    ids = [entry["id"] for entry in entries]
    if len(entries) != expected_entry_count or len(ids) != len(set(ids)):
        raise AssertionError("independent verifier: enumeration is not unique/exhaustive")
    if any(entry["status"] not in STATUS_VALUES for entry in entries):
        raise AssertionError("independent verifier: invalid typed state")

    recomputed = Counter(entry["status"] for entry in entries)
    expected_counts = {
        "total": expected_entry_count,
        "INTEGER": recomputed["INTEGER"],
        "UNRESOLVED": recomputed["UNRESOLVED"],
        "OUT_OF_SCOPE": recomputed["OUT_OF_SCOPE"],
    }
    if result["counts"] != expected_counts:
        raise AssertionError("independent verifier: count mismatch")

    for entry in entries:
        value = entry["global_intersection_integer"]
        if entry["status"] == "INTEGER":
            if entry["scope_relation"] != "IN_SCOPE_RECORDED_CANDIDATE":
                raise AssertionError(
                    "independent verifier: INTEGER is outside the incidence domain"
                )
            if entry["out_of_scope_reason"] is not None:
                raise AssertionError(
                    "independent verifier: INTEGER carries an exclusion reason"
                )
            if not is_integer(value):
                raise AssertionError("independent verifier: INTEGER has no integer")
            if not all(entry["prerequisites"].values()):
                raise AssertionError(
                    "independent verifier: INTEGER has an unmet prerequisite"
                )
            if any(
                entry[key] is None
                for key in ("original_cycle_ref", "global_upward_cycle_ref", "sheet_ref")
            ):
                raise AssertionError("independent verifier: INTEGER lacks a locator")
            if entry["missing_requirements"]:
                raise AssertionError("independent verifier: INTEGER lists missing data")
        elif entry["status"] == "UNRESOLVED":
            if entry["scope_relation"] != "IN_SCOPE_RECORDED_CANDIDATE":
                raise AssertionError(
                    "independent verifier: UNRESOLVED is outside the incidence domain"
                )
            if value is not None:
                raise AssertionError(
                    "independent verifier: UNRESOLVED was collapsed to an integer"
                )
            if not entry["missing_requirements"]:
                raise AssertionError(
                    "independent verifier: UNRESOLVED has no explicit missing requirement"
                )
            if entry["out_of_scope_reason"] is not None:
                raise AssertionError(
                    "independent verifier: UNRESOLVED carries an exclusion reason"
                )
        else:
            if entry["scope_relation"] != "OUTSIDE_GLOBAL_INCIDENCE_DOMAIN":
                raise AssertionError(
                    "independent verifier: OUT_OF_SCOPE is inside the incidence domain"
                )
            if value is not None:
                raise AssertionError(
                    "independent verifier: OUT_OF_SCOPE was collapsed to an integer"
                )
            reason = entry["out_of_scope_reason"]
            if not isinstance(reason, str) or not reason.strip():
                raise AssertionError(
                    "independent verifier: OUT_OF_SCOPE lacks a bounded reason"
                )
            if entry["missing_requirements"]:
                raise AssertionError(
                    "independent verifier: OUT_OF_SCOPE carries in-scope missing requirements"
                )

    coverage = result["coverage"]
    if coverage != {
        "predeclared_records": expected_entry_count,
        "classified_records": expected_entry_count,
        "unclassified_records": 0,
        "global_census_complete": False,
        "exhaustiveness_claim": result["enumeration_boundary"][
            "exhaustiveness_claim"
        ],
    }:
        raise AssertionError("independent verifier: coverage mismatch")
    if result["ledger_verdict"] != "INCOMPLETE":
        raise AssertionError("independent verifier: incomplete global census must stay open")
    if result["required_fail_closed_outputs"] != expected_nulls():
        raise AssertionError("independent verifier: promoted output mutation")
    return {
        "passed": True,
        "checked_entry_count": len(entries),
        "recomputed_counts": expected_counts,
    }


def expect_mutation_rejected(
    result: dict[str, Any], expected_entry_count: int, mutation: str
) -> dict[str, Any]:
    mutated = copy.deepcopy(result)
    if mutation == "duplicate_id":
        mutated["incidence_ledger"][1]["id"] = mutated["incidence_ledger"][0]["id"]
    elif mutation == "unresolved_null_to_zero":
        row = next(
            entry
            for entry in mutated["incidence_ledger"]
            if entry["status"] == "UNRESOLVED"
        )
        row["global_intersection_integer"] = 0
    elif mutation == "local_sign_to_global_integer":
        row = next(
            entry
            for entry in mutated["incidence_ledger"]
            if entry["status"] == "UNRESOLVED"
            and entry["local_orientation_sign"] is not None
        )
        row["status"] = "INTEGER"
        row["global_intersection_integer"] = row["local_orientation_sign"]
        mutated["counts"]["INTEGER"] += 1
        mutated["counts"]["UNRESOLVED"] -= 1
    elif mutation == "empty_out_of_scope_reason":
        row = next(
            entry
            for entry in mutated["incidence_ledger"]
            if entry["status"] == "OUT_OF_SCOPE"
        )
        row["out_of_scope_reason"] = ""
    else:
        raise AssertionError(f"unknown mutation: {mutation}")
    try:
        independent_verify(mutated, expected_entry_count)
    except AssertionError as error:
        return {
            "mutation": mutation,
            "rejected": True,
            "reason": str(error),
        }
    raise AssertionError(f"false-signal mutation was accepted: {mutation}")


def main() -> int:
    payload, input_sha = load_input()
    root = Path(__file__).resolve().parent.parent
    verified_sources, raw_by_id = verify_source_artifacts(root, payload)
    verified_bindings, signal_record = verify_graph_and_signal(
        root, payload, raw_by_id
    )
    prerequisite_ids = validate_input_shape(payload)
    source_by_id = {source["id"]: source for source in verified_sources}
    ledger = [
        classify_entry(entry, prerequisite_ids, source_by_id)
        for entry in payload["entries"]
    ]
    count_map = Counter(entry["status"] for entry in ledger)
    counts = {
        "total": len(ledger),
        "INTEGER": count_map["INTEGER"],
        "UNRESOLVED": count_map["UNRESOLVED"],
        "OUT_OF_SCOPE": count_map["OUT_OF_SCOPE"],
    }
    exact_checks = [
        {
            "id": "gate1.incidence.sources.hashes_and_markers",
            "passed": len(verified_sources) == len(payload["source_artifacts"]),
            "statement": "Every declared local source artifact matches its SHA-256 pin and required semantic markers.",
        },
        {
            "id": "gate1.incidence.graph.canonical_bindings",
            "passed": len(verified_bindings) == len(payload["graph_bindings"]),
            "statement": "Every canonical CPT graph locator resolves with the predeclared type and state.",
        },
        {
            "id": "gate1.incidence.entries.exhaustive_typed_partition",
            "passed": sum(counts[status] for status in STATUS_VALUES) == counts["total"] == 14,
            "statement": "Exactly fourteen unique predeclared records form a disjoint typed partition.",
        },
        {
            "id": "gate1.incidence.local_sign.separate_from_global_integer",
            "passed": all(
                entry["global_intersection_integer"] is None
                for entry in ledger
                if entry["local_orientation_sign"] is not None
            ),
            "statement": "Every recorded local +1 remains a local sign and no local sign is promoted to a global integer.",
        },
        {
            "id": "gate1.incidence.null.never_collapsed_to_zero",
            "passed": counts["INTEGER"] == 0
            and all(
                entry["global_intersection_integer"] is None
                for entry in ledger
                if entry["status"] != "INTEGER"
            ),
            "statement": "No unresolved or excluded null is represented as integer zero.",
        },
        {
            "id": "gate1.incidence.global_outputs.fail_closed",
            "passed": payload["enumeration_boundary"]["global_census_complete"] is False
            and payload["required_fail_closed_outputs"] == expected_nulls(),
            "statement": "An incomplete global census forces the vector, n_sigma, chain sum, cycle, closure, and promoted claims to remain null/prohibited.",
        },
    ]
    all_exact_passed = all(check["passed"] for check in exact_checks)
    result: dict[str, Any] = {
        "schema_version": RESULT_SCHEMA,
        "calculation_id": CALCULATION_ID,
        "numbered_phase": None,
        "run_status": "VALID_RUN" if all_exact_passed else "FAIL_CLOSED",
        "ledger_verdict": "INCOMPLETE",
        "programme_impact": "RETAIN_GATE1_OPEN_PARTIAL_PROGRESS_WITH_TYPED_RECORDED_INCIDENCE_UNKNOWNS",
        "question": payload["question"],
        "one_output": payload["one_output"],
        "non_claim": payload["non_claim"],
        "principal_failure_class": payload["principal_failure_class"],
        "input_manifest": {"path": INPUT_RELPATH, "sha256": input_sha},
        "runner": {
            "path": RUNNER_RELPATH,
            "sha256": digest(Path(__file__).read_bytes()),
        },
        "verified_source_artifacts": verified_sources,
        "scientific_intuition_signal": signal_record,
        "primary_sources": payload["primary_sources"],
        "graph_contract": payload["graph_contract"],
        "verified_graph_bindings": verified_bindings,
        "equation_and_conventions": payload["equation_and_conventions"],
        "assumptions": payload["assumptions"],
        "eligibility_prerequisites": payload["eligibility_prerequisites"],
        "enumeration_boundary": payload["enumeration_boundary"],
        "incidence_ledger": ledger,
        "counts": counts,
        "coverage": {
            "predeclared_records": len(ledger),
            "classified_records": len(ledger),
            "unclassified_records": 0,
            "global_census_complete": False,
            "exhaustiveness_claim": payload["enumeration_boundary"][
                "exhaustiveness_claim"
            ],
        },
        "exact_checks": exact_checks,
        "false_signal_controls": payload["false_signal_controls"],
        "required_fail_closed_outputs": expected_nulls(),
        "resource_accounting": {
            "root_calls": 0,
            "quadratures": 0,
            "ode_calls": 0,
            "numerical_samples": 0,
        },
        "execution": {
            "command": "./ice run gate1_original_cycle_intersection_incidence_ledger",
            "historical_numbered_runners_reexecuted": False,
        },
        "observed_failures": [],
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
    }
    baseline_verification = independent_verify(result, len(ledger))
    mutation_results = [
        expect_mutation_rejected(result, len(ledger), "duplicate_id"),
        expect_mutation_rejected(result, len(ledger), "unresolved_null_to_zero"),
        expect_mutation_rejected(result, len(ledger), "local_sign_to_global_integer"),
        expect_mutation_rejected(result, len(ledger), "empty_out_of_scope_reason"),
    ]
    result["independent_software_verification"] = {
        "mode": "SEPARATE_RESULT_READER_WITHOUT_CLASSIFIER_HELPER_REUSE",
        "boundary": "This is an independent software invariant check inside the bounded run, not independent scientific evidence for an intersection integer.",
        "baseline": baseline_verification,
        "mutations": mutation_results,
        "all_mutations_rejected": all(item["rejected"] for item in mutation_results),
    }
    result["check_summary"] = {
        "exact_passed": sum(check["passed"] for check in exact_checks),
        "exact_total": len(exact_checks),
        "independent_baseline_passed": baseline_verification["passed"],
        "mutations_rejected": sum(item["rejected"] for item in mutation_results),
        "mutations_total": len(mutation_results),
        "all_checks_passed": all_exact_passed
        and baseline_verification["passed"]
        and all(item["rejected"] for item in mutation_results),
    }
    result["result_payload_sha256_without_self"] = digest(canonical_bytes(result))
    encoded = canonical_bytes(result) + b"\n"
    if len(encoded) > ARTIFACT_CAP_BYTES:
        raise AssertionError("result artifact cap exceeded")
    Path(__file__).with_name(RESULT_NAME).write_bytes(encoded)
    summary = {
        "run_status": result["run_status"],
        "ledger_verdict": result["ledger_verdict"],
        "counts": counts,
        "exact_checks": f"{result['check_summary']['exact_passed']}/{result['check_summary']['exact_total']}",
        "mutations_rejected": f"{result['check_summary']['mutations_rejected']}/{result['check_summary']['mutations_total']}",
        "global_vector": None,
        "global_n_sigma": None,
        "result": RESULT_NAME,
        "result_sha256": digest(encoded),
        "result_bytes": len(encoded),
    }
    print(RESULT_PREFIX + json.dumps(summary, sort_keys=True))
    return 0 if result["check_summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
