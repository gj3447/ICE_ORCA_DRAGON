#!/usr/bin/env python3
"""Phase 42 -- checkpoint-only fixed-root tangent disentanglement.

This executable consumes the committed Phase-42 input manifest and the
committed, post-hoc regenerated Phase-41 checkpoint.  It never searches for a
root, saddle, chart, branch, or replacement parameter.  The numerical result
is a local derivative audit at three immutable m=4 roots; all global and
quantum-gravity outputs remain fail-closed.

The program writes no files.  Progress is written to stderr and exactly one
``RESULT_JSON=`` record is written to stdout, including on an INVALID_RUN.
"""

from __future__ import annotations

import sys

# This is set before importing any repository-local module.  The production
# guard also snapshots the repository's pre-existing __pycache__ entries.
sys.dont_write_bytecode = True

import dataclasses
import hashlib
import importlib.util
import json
import math
import os
import platform
import subprocess
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, Mapping, Sequence

import mpmath
import numpy as np
import scipy
import sympy
from scipy.integrate import solve_ivp


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.resolve()
MANIFEST_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_INPUTS.json"
)
CHECKPOINT_PATH = SCRIPT_PATH.with_name(
    "PHASE42_M4_FIXED_ROOT_CHECKPOINT.json"
)
PHASE41_PATH = SCRIPT_PATH.with_name("phase41_m4_two_source_intersection.py")

MANIFEST_COMMIT = "dc21816b9fef9ad658fdd728e73453ffeee46f4d"
MANIFEST_SHA256 = (
    "1cc88c489b5240019aaf339b25d0cebac9b4a1560b09cbec9c3079ce2067afb6"
)
CHECKPOINT_COMMIT = "731579c37867a2041b65359bfc649be3b66900c7"
CHECKPOINT_SHA256 = (
    "ad51bac8eff42e4d300b7872886053c1a6110812ed43b57cdd0e4dbf961891c6"
)
CHECKPOINT_SELF_DIGEST = (
    "e05c6cae4d34cf0bc7615a4801c7c96d163f974edc70d7f6d623102ee9dd63e2"
)
PHASE41_COMMIT = "a31a8627b0e0e210dea96d1d69dad80ccaa6decd"
PHASE41_SHA256 = (
    "377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530"
)

RESULT_SCHEMA = "ice-phase42-fixed-root-tangent-disentanglement/v1"
CHECKPOINT_SCHEMA = "ice-phase42-fixed-root-checkpoint/v1"
CHECKPOINT_STATUS = "POST_HOC_REGENERATED_CHECKPOINT"
RESULT_PREFIX = "RESULT_JSON="

TARGETS = ("shared_zero", "phi_plus", "a_plus")
SADDLE_LABELS = (
    "shared_zero",
    "phi_plus_half",
    "phi_plus",
    "phi_minus_half",
    "phi_minus",
    "a_plus_half",
    "a_plus",
    "a_minus_half",
    "a_minus",
)
PRIMARY_LABELS = (
    "shared_zero",
    "phi_minus",
    "phi_plus",
    "a_minus",
    "a_plus",
)
EXACT_IDS = (
    "P42.freeze.two_stage_artifacts_and_environment",
    "P42.checkpoint.strict_integrity_and_cross_identities",
    "P42.freeze.checkpoint_only_fixed_roots_no_retune",
    "P42.map.order_steps_tiers_and_root_sign",
    "P42.math.fixed_Richardson_metrics_and_homotopy",
    "P42.guard.chart_geodesic_and_real_directional_scope",
    "P42.retention.complete_declared_slot_schema",
    "P42.guard.fail_closed_global_outputs",
)
NUMERICAL_IDS = (
    "P42.reproduction.fixed_checkpoint_and_three_way_J",
    "P42.reproduction.phase41_failed_FD_negative_control",
    "P42.chart.initial_tangent_and_fixed_curvature",
    "P42.variational.local_RHS_and_time_column",
    "P42.derivative.all_column_fixed_R4",
    "P42.derivative.u2_solver_disentanglement",
    "P42.orientation.normalized_sufficient_homotopy",
    "P42.classification.complete_tri_state_cause_ledger",
)


class InvalidRun(RuntimeError):
    """Infrastructure, frozen-input, retention, or drift contract failed."""


class SlotEvaluationError(RuntimeError):
    """One declared numerical slot could not be evaluated."""

    def __init__(self, message: str, *, payload: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.payload = dict(payload or {})


class DuplicateJSONKey(InvalidRun):
    """A strict JSON object contained the same key more than once."""


def progress(message: str) -> None:
    print(f"[Phase42] {message}", file=sys.stderr, flush=True)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _reject_constant(token: str) -> None:
    raise InvalidRun(f"nonfinite JSON token is forbidden: {token}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(raw: bytes, *, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except InvalidRun:
        raise
    except Exception as exc:
        raise InvalidRun(f"cannot strictly decode {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidRun(f"{label} is not one JSON object")
    return value


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InvalidRun(f"noncanonical/nonfinite JSON payload: {exc}") from exc


def read_pinned_json(
    path: Path, expected_sha: str, *, label: str
) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    observed = sha256_bytes(raw)
    if observed != expected_sha:
        raise InvalidRun(
            f"{label} SHA drift: expected {expected_sha}, observed {observed}"
        )
    return strict_json_bytes(raw, label=label), raw


def git_output(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise InvalidRun(
            f"git {' '.join(arguments)} failed: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def relative_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError as exc:
        raise InvalidRun(f"path is outside repository: {path}") from exc


def verify_file_pin(path: Path, commit: str, expected_sha: str) -> dict[str, Any]:
    rel = relative_repo_path(path)
    raw = path.read_bytes()
    observed_sha = sha256_bytes(raw)
    if observed_sha != expected_sha:
        raise InvalidRun(f"byte drift for {rel}")
    committed_raw = subprocess.run(
        ["git", "show", f"{commit}:{rel}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if committed_raw.returncode != 0:
        raise InvalidRun(
            f"cannot read committed pin {commit}:{rel}: "
            f"{committed_raw.stderr.decode(errors='replace').strip()}"
        )
    committed_sha = sha256_bytes(committed_raw.stdout)
    if committed_sha != expected_sha or committed_raw.stdout != raw:
        raise InvalidRun(f"commit/blob mismatch for {rel}")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if ancestor.returncode != 0:
        raise InvalidRun(f"pinned commit is not an ancestor of HEAD: {commit}")
    return {
        "path": rel,
        "commit": commit,
        "sha256": observed_sha,
        "ancestor_of_HEAD": True,
        "worktree_matches_commit_blob": True,
    }


def repository_pycache_snapshot() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    excluded = {".git", ".venv", "node_modules"}
    paths = list(REPO_ROOT.rglob("*.pyc")) + list(REPO_ROOT.rglob("*.pyo"))
    for path in sorted(set(paths)):
        relative = path.relative_to(REPO_ROOT)
        if any(part in excluded for part in relative.parts):
            continue
        stat = path.stat()
        records.append(
            {
                "path": relative.as_posix(),
                "size": int(stat.st_size),
                "mtime_ns": int(stat.st_mtime_ns),
                "sha256": sha256_bytes(path.read_bytes()),
            }
        )
    return records


def canonical_array_bytes(array: np.ndarray) -> tuple[str, bytes]:
    values = np.asarray(array)
    if np.iscomplexobj(values):
        canonical = np.ascontiguousarray(values, dtype=np.dtype("<c16"))
        return "<c16", canonical.tobytes(order="C")
    canonical = np.ascontiguousarray(values, dtype=np.dtype("<f8"))
    return "<f8", canonical.tobytes(order="C")


def is_array_record(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("shape"), list)
        and "values" in value
        and "canonical_little_endian_sha256" in value
        and "canonical_little_endian_dtype" in value
        and "runtime_dtype" in value
    )


def decode_array_record(
    record: Mapping[str, Any],
    *,
    path: str,
    expected_shape: tuple[int, ...] | None = None,
) -> np.ndarray:
    try:
        shape = tuple(int(item) for item in record["shape"])
    except Exception as exc:
        raise InvalidRun(f"invalid array shape at {path}") from exc
    if any(item < 0 for item in shape):
        raise InvalidRun(f"negative array dimension at {path}")
    if expected_shape is not None and shape != expected_shape:
        raise InvalidRun(
            f"shape mismatch at {path}: expected {expected_shape}, got {shape}"
        )

    complex_encoding = record.get("complex_encoding")
    if complex_encoding is None:
        array = np.asarray(record["values"], dtype=np.float64)
        if array.shape != shape:
            raise InvalidRun(f"decoded real shape mismatch at {path}")
        expected_runtime = "float64"
        expected_canonical = "<f8"
    elif complex_encoding == "terminal [real,imag] pairs":
        pairs = np.asarray(record["values"], dtype=np.float64)
        if pairs.shape != shape + (2,):
            raise InvalidRun(f"decoded complex-pair shape mismatch at {path}")
        # Assignment through the real and imaginary buffers is deliberate:
        # real+1j*imag can canonicalize a signed zero in either component.
        array = np.empty(shape, dtype=np.complex128)
        array.real[...] = pairs[..., 0]
        array.imag[...] = pairs[..., 1]
        expected_runtime = "complex128"
        expected_canonical = "<c16"
    else:
        raise InvalidRun(f"unknown complex encoding at {path}: {complex_encoding}")

    if str(record["runtime_dtype"]) != expected_runtime:
        raise InvalidRun(f"runtime dtype declaration mismatch at {path}")
    canonical_dtype, raw = canonical_array_bytes(array)
    if canonical_dtype != expected_canonical:
        raise InvalidRun(f"canonical dtype implementation mismatch at {path}")
    if str(record["canonical_little_endian_dtype"]) != expected_canonical:
        raise InvalidRun(f"canonical dtype declaration mismatch at {path}")
    if not np.all(np.isfinite(array.real)) or (
        np.iscomplexobj(array) and not np.all(np.isfinite(array.imag))
    ):
        raise InvalidRun(f"nonfinite decoded array at {path}")
    observed_sha = sha256_bytes(raw)
    if observed_sha != str(record["canonical_little_endian_sha256"]):
        raise InvalidRun(f"canonical array SHA mismatch at {path}")
    return array


def independently_decode_all_arrays(
    value: Any,
    *,
    path: str = "$",
    output: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    decoded = {} if output is None else output
    if is_array_record(value):
        if path in decoded:
            raise InvalidRun(f"duplicate array path: {path}")
        decoded[path] = decode_array_record(value, path=path)
        return decoded
    if isinstance(value, dict):
        for key, child in value.items():
            independently_decode_all_arrays(
                child, path=f"{path}.{key}", output=decoded
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            independently_decode_all_arrays(
                child, path=f"{path}[{index}]", output=decoded
            )
    return decoded


def json_ready(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return json_ready(dataclasses.asdict(value))
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            if not np.all(np.isfinite(value.real)) or not np.all(
                np.isfinite(value.imag)
            ):
                raise SlotEvaluationError("nonfinite complex ndarray in result")
            pairs = np.empty(value.shape + (2,), dtype=float)
            pairs[..., 0] = value.real
            pairs[..., 1] = value.imag
            return json_ready(pairs.tolist())
        if not np.all(np.isfinite(value)):
            raise SlotEvaluationError("nonfinite ndarray in result")
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, complex):
        if not math.isfinite(value.real) or not math.isfinite(value.imag):
            raise SlotEvaluationError("nonfinite complex value in result")
        return [float(value.real), float(value.imag)]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SlotEvaluationError("nonfinite float in result")
        return value
    if isinstance(value, dict):
        return {str(key): json_ready(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(child) for child in value]
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise InvalidRun(f"cannot serialize value of type {type(value).__name__}")


@dataclass
class Audit:
    exact_records: list[dict[str, Any]] = field(default_factory=list)
    numerical_records: list[dict[str, Any]] = field(default_factory=list)

    def _ensure_unique(self, check_id: str) -> None:
        if any(
            record["id"] == check_id
            for record in self.exact_records + self.numerical_records
        ):
            raise InvalidRun(f"duplicate audit id: {check_id}")

    def exact(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self._ensure_unique(check_id)
        record = {
            "id": check_id,
            "kind": "exact",
            "status": "PASS" if passed else "INVALID_RUN",
            "passed": bool(passed),
            "failure_status": "INVALID_RUN",
            "statement": statement,
            "details": json_ready(dict(details or {})),
        }
        self.exact_records.append(record)
        if not passed:
            raise InvalidRun(f"{check_id}: {statement}")

    def numerical(
        self,
        check_id: str,
        passed: bool,
        statement: str,
        *,
        failure_status: str,
        failure_invalidates_run: bool,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self._ensure_unique(check_id)
        record = {
            "id": check_id,
            "kind": "numerical",
            "status": "PASS" if passed else failure_status,
            "passed": bool(passed),
            "failure_status": failure_status,
            "failure_invalidates_run": bool(failure_invalidates_run),
            "statement": statement,
            "details": json_ready(dict(details or {})),
        }
        self.numerical_records.append(record)


@dataclass
class SlotLedger:
    slots: dict[str, dict[str, Any]] = field(default_factory=dict)

    def declare(self, key: str, **metadata: Any) -> None:
        if key in self.slots:
            raise InvalidRun(f"duplicate declared slot: {key}")
        self.slots[key] = {
            "key": key,
            "terminal_status": None,
            "metadata": json_ready(metadata),
            "payload": None,
            "error": None,
        }

    def finish(
        self,
        key: str,
        status: str,
        *,
        payload: Any = None,
        error: str | None = None,
    ) -> None:
        if key not in self.slots:
            raise InvalidRun(f"undeclared slot completed: {key}")
        slot = self.slots[key]
        if slot["terminal_status"] is not None:
            raise InvalidRun(f"slot completed more than once: {key}")
        if status not in {
            "SUCCESS",
            "EVALUATION_FAILED",
            "NOT_RUN_UPSTREAM_INVALID",
        }:
            raise InvalidRun(f"invalid terminal slot status: {status}")
        ready_payload = json_ready(payload)
        slot["terminal_status"] = status
        slot["payload"] = ready_payload
        slot["error"] = error

    def fail_unfinished(self, reason: str) -> None:
        for key, slot in self.slots.items():
            if slot["terminal_status"] is None:
                self.finish(
                    key,
                    "NOT_RUN_UPSTREAM_INVALID",
                    error=reason,
                )

    def assert_complete(self) -> None:
        missing = [
            key
            for key, slot in self.slots.items()
            if slot["terminal_status"] is None
        ]
        if missing:
            raise InvalidRun(f"unterminated slots: {missing[:5]}")


@dataclass(frozen=True)
class PointContext:
    label: str
    source_point: tuple[float, float]
    parameters: np.ndarray
    checkpoint_jacobian: np.ndarray
    model: Any
    saddle: Any
    checkpoint_target: Mapping[str, Any]


@dataclass(frozen=True)
class CheckpointContext:
    raw_payload: Mapping[str, Any]
    decoded_arrays: Mapping[str, np.ndarray]
    phase41: ModuleType
    fixed: Any
    chart: Any
    coordinate_scales: np.ndarray
    row_scales: np.ndarray
    reflection: np.ndarray
    points: Mapping[str, PointContext]
    no_solve_call_counter: Mapping[str, int]
    validation: Mapping[str, Any]


@dataclass(frozen=True)
class TierSpec:
    name: str
    method: str
    representation: str
    rtol: float
    atol: float
    max_step: float


@dataclass(frozen=True)
class FlowEvaluation:
    xi: np.ndarray
    state_z: np.ndarray
    omega: np.ndarray
    initial_xi: np.ndarray
    solver: Mapping[str, Any]


@dataclass(frozen=True)
class AugmentedEvaluation:
    xi: np.ndarray
    state_z: np.ndarray
    k_frame_z: np.ndarray
    jacobian: np.ndarray
    gamma_state_z: np.ndarray
    gamma_frame_z: np.ndarray
    residual: np.ndarray
    fraction_times: np.ndarray
    fraction_xi: np.ndarray
    fraction_tangents: np.ndarray
    positive_time_tangent_z: np.ndarray
    solver: Mapping[str, Any]


def backend_fingerprint(
    configuration: Mapping[str, Any], kind: str
) -> dict[str, Any]:
    dependencies = configuration.get("Build Dependencies")
    if not isinstance(dependencies, dict):
        raise InvalidRun("runtime build-dependency metadata is unavailable")
    backend = dependencies.get(kind)
    if not isinstance(backend, dict):
        raise InvalidRun(f"runtime {kind} metadata is unavailable")
    result: dict[str, Any] = {
        "name": backend.get("name"),
        "version": backend.get("version"),
        "openblas_configuration": backend.get("openblas configuration"),
    }
    if "has ilp64" in backend:
        result["has_ilp64"] = bool(backend["has ilp64"])
    return result


def observed_runtime_fingerprint(manifest: Mapping[str, Any]) -> dict[str, Any]:
    numpy_configuration = np.show_config(mode="dicts")
    scipy_configuration = scipy.show_config(mode="dicts")
    if not isinstance(numpy_configuration, dict) or not isinstance(
        scipy_configuration, dict
    ):
        raise InvalidRun("BLAS/LAPACK configuration is not machine-readable")
    expected = manifest["strict_runtime_environment"]["fingerprint"]
    expected_threads = expected["thread_environment"]
    observed = {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build": list(platform.python_build()),
        "python_compiler": platform.python_compiler(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "sympy_version": sympy.__version__,
        "mpmath_version": mpmath.__version__,
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "libc": list(platform.libc_ver()),
        "numpy_blas": backend_fingerprint(numpy_configuration, "blas"),
        "numpy_lapack": backend_fingerprint(numpy_configuration, "lapack"),
        "scipy_blas": backend_fingerprint(scipy_configuration, "blas"),
        "scipy_lapack": backend_fingerprint(scipy_configuration, "lapack"),
        "thread_environment": {
            name: os.environ.get(name) for name in expected_threads
        },
        "effective_BLAS_thread_count": None,
        "effective_BLAS_thread_count_scope": expected[
            "effective_BLAS_thread_count_scope"
        ],
    }
    if observed != expected:
        raise InvalidRun(
            "runtime fingerprint drift: "
            + json.dumps(
                {"expected": expected, "observed": observed},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    expected_executable = (
        REPO_ROOT / manifest["strict_runtime_environment"]["launch_executable"]
    ).resolve()
    observed_executable = Path(sys.executable).resolve()
    if observed_executable != expected_executable:
        raise InvalidRun(
            f"wrong Python executable: {observed_executable} != {expected_executable}"
        )
    if sys.dont_write_bytecode is not True:
        raise InvalidRun("sys.dont_write_bytecode is not true")
    return {
        "verified": True,
        "python_executable": str(observed_executable),
        "strict_fingerprint": observed,
    }


def source_pin_specs(manifest: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    freeze = manifest["two_stage_input_freeze"]
    closure = freeze["phase39_transitive_closure"]
    locks = freeze["dependency_locks"]
    entries: dict[str, Mapping[str, Any]] = {
        "manifest": {
            "path": relative_repo_path(MANIFEST_PATH),
            "commit": MANIFEST_COMMIT,
            "sha256": MANIFEST_SHA256,
        },
        "checkpoint": {
            "path": relative_repo_path(CHECKPOINT_PATH),
            "commit": freeze["checkpoint_artifact"]["commit"],
            "sha256": freeze["checkpoint_artifact"]["outer_file_sha256"],
        },
        "checkpoint_extractor": freeze["checkpoint_extractor"],
        "phase41_script": freeze["phase41_executable"],
        "phase41_manifest": freeze["phase41_manifest"],
        "phase41_report": freeze["phase41_report"],
        "phase39_script": closure["script"],
        "phase39_report": closure["direction_report"],
        "phase39_manifest": closure["input_manifest"],
        "pyproject": locks["pyproject"],
        "uv_lock": locks["uv_lock"],
    }
    result: dict[str, dict[str, str]] = {}
    for name, entry in entries.items():
        result[name] = {
            "path": str(entry["path"]),
            "commit": str(entry["commit"]),
            "sha256": str(entry["sha256"]),
        }
    return result


def verify_source_closure(manifest: Mapping[str, Any]) -> dict[str, Any]:
    observed: dict[str, Any] = {}
    for name, pin in source_pin_specs(manifest).items():
        observed[name] = verify_file_pin(
            REPO_ROOT / pin["path"], pin["commit"], pin["sha256"]
        )
    return {
        "git_HEAD": git_output("rev-parse", "HEAD"),
        "files": observed,
    }


def observed_runner_provenance() -> dict[str, Any]:
    rel = relative_repo_path(SCRIPT_PATH)
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if not tracked:
        raise InvalidRun("Phase42 runner must be committed before production")
    dirty = git_output("status", "--porcelain=v1", "--", rel)
    if dirty:
        raise InvalidRun("Phase42 runner path is dirty")
    latest_commit = git_output("log", "-1", "--format=%H", "--", rel)
    if not latest_commit:
        raise InvalidRun("Phase42 runner has no committed path history")
    current_raw = SCRIPT_PATH.read_bytes()
    current_sha = sha256_bytes(current_raw)
    committed = subprocess.run(
        ["git", "show", f"{latest_commit}:{rel}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if committed.returncode != 0:
        raise InvalidRun("cannot read latest committed runner blob")
    committed_sha = sha256_bytes(committed.stdout)
    if current_raw != committed.stdout:
        raise InvalidRun("runner differs from its latest committed blob")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", latest_commit, "HEAD"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    ).returncode == 0
    if not ancestor:
        raise InvalidRun("latest runner commit is not an ancestor of HEAD")
    if latest_commit == MANIFEST_COMMIT:
        raise InvalidRun("runner was not committed after Stage-1 manifest")
    manifest_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", MANIFEST_COMMIT, latest_commit],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    ).returncode == 0
    if not manifest_ancestor:
        raise InvalidRun("runner commit does not descend from manifest commit")
    return {
        "path": rel,
        "observed_sha256": current_sha,
        "git_tracked": True,
        "git_clean_for_path": True,
        "latest_path_commit": latest_commit,
        "latest_commit_blob_sha256": committed_sha,
        "latest_commit_blob_matches_current_bytes": True,
        "latest_path_commit_is_ancestor_of_HEAD": True,
        "manifest_commit_is_ancestor_of_runner_commit": True,
    }


def raw_git_observation(*arguments: str, binary: bool = False) -> dict[str, Any]:
    """Observe a git fact without enforcing it or raising on mismatch."""
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout: Any = completed.stdout if binary else completed.stdout.decode(
            errors="replace"
        ).strip()
        return {
            "returncode": int(completed.returncode),
            "ok": completed.returncode == 0,
            "stdout": stdout,
            "stderr": completed.stderr.decode(errors="replace").strip()[:2048],
        }
    except Exception as exc:
        return {
            "returncode": None,
            "ok": False,
            "stdout": b"" if binary else "",
            "stderr": f"{type(exc).__name__}: {exc}"[:2048],
        }


def observe_runner_provenance_raw() -> dict[str, Any]:
    """Nonthrowing runner ledger used when the enforcing guard itself fails."""
    try:
        rel = SCRIPT_PATH.resolve().relative_to(REPO_ROOT).as_posix()
    except Exception as exc:
        return {
            "path": None,
            "observation_error": f"{type(exc).__name__}: {exc}"[:2048],
        }
    try:
        current_raw = SCRIPT_PATH.read_bytes()
        current_sha: str | None = sha256_bytes(current_raw)
        current_size: int | None = len(current_raw)
        current_error: str | None = None
    except Exception as exc:
        current_raw = None
        current_sha = None
        current_size = None
        current_error = f"{type(exc).__name__}: {exc}"[:2048]
    tracked_record = raw_git_observation("ls-files", "--error-unmatch", rel)
    dirty_record = raw_git_observation("status", "--porcelain=v1", "--", rel)
    latest_record = raw_git_observation("log", "-1", "--format=%H", "--", rel)
    latest_commit = (
        str(latest_record["stdout"])
        if latest_record["ok"] and latest_record["stdout"]
        else None
    )
    blob_record = (
        raw_git_observation("show", f"{latest_commit}:{rel}", binary=True)
        if latest_commit is not None
        else {
            "ok": False,
            "returncode": None,
            "stdout": b"",
            "stderr": "latest path commit unavailable",
        }
    )
    blob_raw = blob_record["stdout"] if blob_record["ok"] else None
    blob_sha = sha256_bytes(blob_raw) if isinstance(blob_raw, bytes) else None
    ancestor_record = (
        raw_git_observation("merge-base", "--is-ancestor", latest_commit, "HEAD")
        if latest_commit is not None
        else {"ok": False, "returncode": None, "stderr": "latest commit unavailable"}
    )
    manifest_ancestor_record = (
        raw_git_observation(
            "merge-base", "--is-ancestor", MANIFEST_COMMIT, latest_commit
        )
        if latest_commit is not None
        else {"ok": False, "returncode": None, "stderr": "latest commit unavailable"}
    )
    return {
        "path": rel,
        "observed_sha256": current_sha,
        "observed_size_bytes": current_size,
        "current_byte_observation_error": current_error,
        "git_tracked": bool(tracked_record["ok"]),
        "git_tracked_observation": tracked_record,
        "git_clean_for_path": bool(
            dirty_record["ok"] and str(dirty_record["stdout"]) == ""
        ),
        "git_status_porcelain": (
            dirty_record["stdout"] if dirty_record["ok"] else None
        ),
        "git_status_observation_error": (
            None if dirty_record["ok"] else dirty_record["stderr"]
        ),
        "latest_path_commit": latest_commit,
        "latest_path_commit_observation_error": (
            None if latest_record["ok"] else latest_record["stderr"]
        ),
        "latest_commit_blob_sha256": blob_sha,
        "latest_commit_blob_matches_current_bytes": bool(
            current_raw is not None
            and isinstance(blob_raw, bytes)
            and current_raw == blob_raw
        ),
        "latest_commit_blob_observation_error": (
            None if blob_record["ok"] else blob_record["stderr"]
        ),
        "latest_path_commit_is_ancestor_of_HEAD": bool(ancestor_record["ok"]),
        "latest_path_ancestor_observation_error": (
            None if ancestor_record["ok"] else ancestor_record.get("stderr")
        ),
        "manifest_commit_is_ancestor_of_runner_commit": bool(
            manifest_ancestor_record["ok"]
        ),
        "manifest_ancestor_observation_error": (
            None
            if manifest_ancestor_record["ok"]
            else manifest_ancestor_record.get("stderr")
        ),
        "runner_commit_is_after_manifest_stage": bool(
            latest_commit is not None and latest_commit != MANIFEST_COMMIT
        ),
    }


def observe_source_closure_raw(
    manifest: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Observe every source pin independently; never enforce or raise."""
    head_record = raw_git_observation("rev-parse", "HEAD")
    result: dict[str, Any] = {
        "git_HEAD": head_record["stdout"] if head_record["ok"] else None,
        "git_HEAD_observation_error": (
            None if head_record["ok"] else head_record["stderr"]
        ),
        "files": {},
    }
    if manifest is None:
        result["pin_schema_error"] = "manifest unavailable"
        return result
    try:
        specs = source_pin_specs(manifest)
    except Exception as exc:
        result["pin_schema_error"] = f"{type(exc).__name__}: {exc}"[:2048]
        return result
    for name, pin in specs.items():
        path = REPO_ROOT / pin["path"]
        try:
            raw = path.read_bytes()
            observed_sha: str | None = sha256_bytes(raw)
            byte_error: str | None = None
        except Exception as exc:
            raw = None
            observed_sha = None
            byte_error = f"{type(exc).__name__}: {exc}"[:2048]
        tracked = raw_git_observation(
            "ls-files", "--error-unmatch", str(pin["path"])
        )
        dirty = raw_git_observation(
            "status", "--porcelain=v1", "--", str(pin["path"])
        )
        latest = raw_git_observation(
            "log", "-1", "--format=%H", "--", str(pin["path"])
        )
        latest_commit = (
            str(latest["stdout"])
            if latest["ok"] and latest["stdout"]
            else None
        )
        blob = raw_git_observation(
            "show", f"{pin['commit']}:{pin['path']}", binary=True
        )
        blob_raw = blob["stdout"] if blob["ok"] else None
        blob_sha = sha256_bytes(blob_raw) if isinstance(blob_raw, bytes) else None
        ancestor = raw_git_observation(
            "merge-base", "--is-ancestor", pin["commit"], "HEAD"
        )
        result["files"][name] = {
            "path": pin["path"],
            "expected_commit": pin["commit"],
            "expected_sha256": pin["sha256"],
            "observed_sha256": observed_sha,
            "current_sha_matches_expected": observed_sha == pin["sha256"],
            "current_byte_observation_error": byte_error,
            "git_tracked": bool(tracked["ok"]),
            "git_clean_for_path": bool(
                dirty["ok"] and str(dirty["stdout"]) == ""
            ),
            "git_status_porcelain": dirty["stdout"] if dirty["ok"] else None,
            "latest_path_commit": latest_commit,
            "latest_path_commit_matches_expected": latest_commit == pin["commit"],
            "expected_commit_blob_sha256": blob_sha,
            "expected_commit_blob_matches_expected_sha": blob_sha == pin["sha256"],
            "expected_commit_blob_matches_current_bytes": bool(
                raw is not None and isinstance(blob_raw, bytes) and raw == blob_raw
            ),
            "expected_commit_is_ancestor_of_HEAD": bool(ancestor["ok"]),
            "blob_observation_error": None if blob["ok"] else blob["stderr"],
            "ancestor_observation_error": (
                None if ancestor["ok"] else ancestor["stderr"]
            ),
        }
    result["all_current_sha_match"] = all(
        record["current_sha_matches_expected"]
        for record in result["files"].values()
    )
    result["all_expected_blobs_match"] = all(
        record["expected_commit_blob_matches_expected_sha"]
        for record in result["files"].values()
    )
    result["all_expected_commits_are_ancestors"] = all(
        record["expected_commit_is_ancestor_of_HEAD"]
        for record in result["files"].values()
    )
    return result


def start_provenance_guard(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source": verify_source_closure(manifest),
        "runner": observed_runner_provenance(),
        "runtime": observed_runtime_fingerprint(manifest),
        "pycache": repository_pycache_snapshot(),
        "HEAD": git_output("rev-parse", "HEAD"),
    }


def finish_provenance_guard(
    manifest: Mapping[str, Any], start: Mapping[str, Any]
) -> dict[str, Any]:
    end = {
        "source": verify_source_closure(manifest),
        "runner": observed_runner_provenance(),
        "runtime": observed_runtime_fingerprint(manifest),
        "pycache": repository_pycache_snapshot(),
        "HEAD": git_output("rev-parse", "HEAD"),
    }
    comparisons = {
        key: end[key] == start[key]
        for key in ("source", "runner", "runtime", "pycache", "HEAD")
    }
    if not all(comparisons.values()):
        raise InvalidRun(f"pre-emission TOCTOU drift: {comparisons}")
    return {"start": start, "end": end, "comparisons": comparisons}


def import_pinned_phase41(manifest: Mapping[str, Any]) -> ModuleType:
    pin = source_pin_specs(manifest)["phase41_script"]
    before = sha256_bytes(PHASE41_PATH.read_bytes())
    if before != pin["sha256"]:
        raise InvalidRun("Phase41 source drift before import")
    module_name = "ice_phase41_m4_phase42_checkpoint_consumer"
    specification = importlib.util.spec_from_file_location(module_name, PHASE41_PATH)
    if specification is None or specification.loader is None:
        raise InvalidRun("cannot construct Phase41 module spec")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    after = sha256_bytes(PHASE41_PATH.read_bytes())
    if after != before:
        raise InvalidRun("Phase41 source changed during import")
    if module.INPUT_COMMIT != manifest["two_stage_input_freeze"][
        "phase41_manifest"
    ]["commit"]:
        raise InvalidRun("Phase41 embedded manifest commit pin drift")
    if module.INPUT_SHA256 != manifest["two_stage_input_freeze"][
        "phase41_manifest"
    ]["sha256"]:
        raise InvalidRun("Phase41 embedded manifest hash pin drift")
    return module


def _array_at(payload: Mapping[str, Any], *keys: str) -> np.ndarray:
    value: Any = payload
    path = "$"
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            raise InvalidRun(f"missing checkpoint field {path}.{key}")
        value = value[key]
        path += f".{key}"
    if not is_array_record(value):
        raise InvalidRun(f"checkpoint field is not an array record: {path}")
    return decode_array_record(value, path=path)


def _complex_pair(value: Any, *, path: str) -> complex:
    pairs = np.asarray(value, dtype=np.float64)
    if pairs.shape != (2,) or not np.all(np.isfinite(pairs)):
        raise InvalidRun(f"invalid complex pair at {path}")
    result = np.empty((), dtype=np.complex128)
    result.real[...] = pairs[0]
    result.imag[...] = pairs[1]
    return complex(result)


def install_forbidden_solve_guards(phase41: ModuleType) -> dict[str, int]:
    counter: dict[str, int] = {}

    def forbidden(name: str) -> Callable[..., Any]:
        counter[name] = 0

        def reject(*_args: Any, **_kwargs: Any) -> Any:
            counter[name] += 1
            raise InvalidRun(f"forbidden Phase42 solver/build call: {name}")

        return reject

    for name in (
        "solve_signed_saddle_grids",
        "solve_main_saddle",
        "solve_primary_intersections",
        "build_fixed_metric",
        "build_nested_chart",
        "root",
        "least_squares",
    ):
        if hasattr(phase41, name):
            setattr(phase41, name, forbidden(name))
    return counter


def verify_checkpoint_envelope(
    manifest: Mapping[str, Any], checkpoint: Mapping[str, Any], raw: bytes
) -> dict[str, Any]:
    frozen = manifest["two_stage_input_freeze"]["checkpoint_artifact"]
    if len(raw) != int(frozen["size_bytes_at_freeze"]):
        raise InvalidRun("checkpoint byte length drift")
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise InvalidRun("checkpoint must end in exactly one LF")
    if checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise InvalidRun("checkpoint schema drift")
    if checkpoint.get("checkpoint_status") != CHECKPOINT_STATUS:
        raise InvalidRun("checkpoint status drift")
    embedded = checkpoint.get("checkpoint_payload_sha256_without_self")
    if embedded != CHECKPOINT_SELF_DIGEST:
        raise InvalidRun("checkpoint embedded self digest drift")
    without_self = dict(checkpoint)
    del without_self["checkpoint_payload_sha256_without_self"]
    recomputed = sha256_bytes(canonical_json_bytes(without_self))
    if recomputed != CHECKPOINT_SELF_DIGEST:
        raise InvalidRun("checkpoint self-excluding digest mismatch")
    provenance = checkpoint.get("scientific_provenance")
    if not isinstance(provenance, dict):
        raise InvalidRun("checkpoint scientific provenance missing")
    for key, expected in frozen["required_provenance_flags"].items():
        section, field_name = key.split(".", 1)
        if section != "scientific_provenance" or provenance.get(field_name) != expected:
            raise InvalidRun(f"checkpoint provenance flag mismatch: {key}")
    ledger = checkpoint.get("critical_array_shape_and_finiteness_ledger")
    if not isinstance(ledger, dict):
        raise InvalidRun("checkpoint array ledger missing")
    if ledger.get("fail_closed") is not True or ledger.get("all_passed") is not True:
        raise InvalidRun("checkpoint embedded array ledger did not pass")
    if int(ledger.get("checked_array_count", -1)) != 204:
        raise InvalidRun("checkpoint embedded array count is not 204")
    decoded = independently_decode_all_arrays(checkpoint)
    if len(decoded) != 191:
        raise InvalidRun(
            f"independent explicit array-payload count is {len(decoded)}, not 191"
        )
    ledger_validation = verify_checkpoint_shape_ledger_mapping(checkpoint)
    if tuple(checkpoint["saddles"].keys()) != SADDLE_LABELS:
        # JSON insertion order is provenance-bearing here, but label set is the
        # scientific requirement.  Retain both facts rather than reorder it.
        if set(checkpoint["saddles"]) != set(SADDLE_LABELS):
            raise InvalidRun("checkpoint saddle label set drift")
    primaries = checkpoint["primary_intersections"]
    if set(primaries["all_parameter_vectors"]) != set(PRIMARY_LABELS):
        raise InvalidRun("checkpoint primary label set drift")
    if tuple(primaries["phase42_fixed_root_targets"].keys()) != TARGETS:
        if set(primaries["phase42_fixed_root_targets"]) != set(TARGETS):
            raise InvalidRun("checkpoint diagnostic target label set drift")
    return {
        "outer_sha256": sha256_bytes(raw),
        "self_digest": recomputed,
        "decoded_explicit_array_payload_count": len(decoded),
        "mapped_critical_array_count": ledger_validation["mapped_count"],
        "decoded_arrays": decoded,
        "embedded_array_ledger_passed": True,
        "provenance_flags_passed": True,
    }


def verify_checkpoint_shape_ledger_mapping(
    checkpoint: Mapping[str, Any],
) -> dict[str, Any]:
    """Map all 204 embedded ledger labels back to independently decoded data.

    There are 191 explicit array-wrapper objects.  The shape ledger also covers
    raw duplicated arrays in ``all_phase41_results``; notably, four minus-arm
    state/J fields have no explicit wrapper.  This mapping reconstructs those
    arrays from their raw fields instead of equating the two counts or trusting
    the embedded ``passed`` flags.
    """

    actual: dict[str, np.ndarray] = {}
    conventions = checkpoint["coordinate_and_orientation_conventions"]
    actual["coordinates.scales"] = decode_array_record(
        conventions["coordinate_scales"], path="$.coordinates.scales"
    )
    actual["coordinates.row_scales"] = decode_array_record(
        conventions["row_scales"], path="$.coordinates.row_scales"
    )
    fixed_names = (
        "saddle_zero_w",
        "hessian_zero_w",
        "eigenvalues_zero",
        "oriented_eigenvectors_zero",
        "linear_map",
        "inverse_metric_mobility_w",
        "metric_tensor_w",
        "xi_reflection",
        "linear_map_z_from_xi",
    )
    for name in fixed_names:
        actual[f"fixed.{name}"] = _array_at(checkpoint, "fixed_metric", name)
    maps = checkpoint["mode_and_reflection_maps"]
    actual["modes.DST"] = decode_array_record(
        maps["DST_basis"], path="$.modes.DST"
    )
    actual["modes.nested"] = decode_array_record(
        maps["nested_basis"], path="$.modes.nested"
    )
    actual["modes.transition"] = decode_array_record(
        maps["DST_to_nested_transition"], path="$.modes.transition"
    )
    actual["reflection.w"] = decode_array_record(
        maps["reflection_w"], path="$.reflection.w"
    )
    actual["reflection.R14"] = decode_array_record(
        maps["reflection_R14_interleaved"], path="$.reflection.R14"
    )
    actual["chart.center"] = _array_at(checkpoint, "upward_chart", "center")
    actual["chart.tangent"] = _array_at(checkpoint, "upward_chart", "tangent")

    for label in SADDLE_LABELS:
        record = checkpoint["saddles"][label]
        mappings = {
            "w": record["saddle_w"],
            "z": record["saddle_z"],
            "hessian_w": record["hessian_w"],
            "hessian_eigenvalues": record["hessian_eigenvalues"],
            "hessian_xi": record["hessian_xi"],
            "hessian_xi_eigenvalues": record["hessian_xi_eigenvalues"],
            "aligned_signed_frame_xi": record["aligned_signed_frame_xi"],
            "negative_restriction": record["signed_restrictions"]["negative"],
            "positive_restriction": record["signed_restrictions"]["positive"],
            "negative_projector": record["signed_projectors"]["negative"],
            "positive_projector": record["signed_projectors"]["positive"],
            "launch_lambda_0": record["launch_matrices"]["lambda_0"],
            "launch_lambda_0.5": record["launch_matrices"]["lambda_0.5"],
            "launch_lambda_1": record["launch_matrices"]["lambda_1"],
        }
        for suffix, wrapper in mappings.items():
            actual[f"saddle.{label}.{suffix}"] = decode_array_record(
                wrapper, path=f"$.saddle.{label}.{suffix}"
            )

    primaries = checkpoint["primary_intersections"]
    for label in PRIMARY_LABELS:
        result = primaries["all_phase41_results"][label]
        actual[f"primary.{label}.parameters"] = decode_array_record(
            primaries["all_parameter_vectors"][label],
            path=f"$.primary.{label}.parameters",
        )
        actual[f"primary.{label}.intersection_state_z"] = (
            _complex_vector_from_pairs(
                result["intersection_z"],
                shape=(7,),
                path=f"$.primary.{label}.intersection_z",
            )
        )
        actual[f"primary.{label}.variational_scaled_root_jacobian"] = np.asarray(
            result["variational_scaled_root_jacobian"], dtype=np.float64
        )

    target_field_map = {
        "authoritative_J": ("variational_scaled_root_jacobian",),
        "parameters": ("parameter_vector",),
        "chart_u": ("chart_at_root", "parameters_u"),
        "omega": ("chart_at_root", "omega"),
        "domega_du": ("chart_at_root", "direction_derivative"),
        "launch_matrix": ("chart_at_root", "launch_matrix"),
        "initial_xi": ("chart_at_root", "initial_xi"),
        "scaled_residual": (
            "post_solve_strict_DOP853_reevaluation",
            "scaled_residual_interleaved",
        ),
        "physical_residual": (
            "post_solve_strict_DOP853_reevaluation",
            "physical_residual_interleaved",
        ),
        "gamma_state_z": (
            "post_solve_strict_DOP853_reevaluation",
            "gamma_state_z",
        ),
        "k_state_z": (
            "post_solve_strict_DOP853_reevaluation",
            "k_state_z",
        ),
        "gamma_frame_z": (
            "post_solve_strict_DOP853_reevaluation",
            "gamma_frame_z",
        ),
        "k_frame_z": (
            "post_solve_strict_DOP853_reevaluation",
            "k_frame_z",
        ),
        "regenerated_J": (
            "post_solve_strict_DOP853_reevaluation",
            "regenerated_scaled_root_jacobian",
        ),
    }
    for label in TARGETS:
        target = primaries["phase42_fixed_root_targets"][label]
        for suffix, key_path in target_field_map.items():
            wrapper: Any = target
            for key in key_path:
                wrapper = wrapper[key]
            actual[f"target.{label}.{suffix}"] = decode_array_record(
                wrapper, path=f"$.target.{label}.{suffix}"
            )
        actual[f"target.{label}.recorded_gamma_state_z"] = (
            _complex_vector_from_pairs(
                target["phase41_primary_result"]["intersection_z"],
                shape=(7,),
                path=f"$.target.{label}.recorded_gamma_state_z",
            )
        )

    embedded = checkpoint["critical_array_shape_and_finiteness_ledger"][
        "records"
    ]
    if set(actual) != set(embedded):
        missing = sorted(set(embedded) - set(actual))
        extra = sorted(set(actual) - set(embedded))
        raise InvalidRun(
            f"204-array mapping label drift; missing={missing}, extra={extra}"
        )
    checks: dict[str, Any] = {}
    for label, values in actual.items():
        record = embedded[label]
        expected_shape = tuple(int(item) for item in record["expected_shape"])
        actual_shape = tuple(int(item) for item in record["actual_shape"])
        if values.shape != expected_shape or values.shape != actual_shape:
            raise InvalidRun(f"mapped ledger shape mismatch at {label}")
        expected_runtime = "complex128" if np.iscomplexobj(values) else "float64"
        if str(record["runtime_dtype"]) != expected_runtime:
            raise InvalidRun(f"mapped ledger dtype mismatch at {label}")
        if not np.all(np.isfinite(values)):
            raise InvalidRun(f"mapped ledger nonfinite array at {label}")
        canonical_dtype, raw = canonical_array_bytes(values)
        digest = sha256_bytes(raw)
        if digest != str(record["canonical_little_endian_sha256"]):
            raise InvalidRun(f"mapped ledger SHA mismatch at {label}")
        if record.get("finite_numeric") is not True:
            raise InvalidRun(f"embedded finite flag false at {label}")
        if record.get("shape_matches") is not True or record.get("passed") is not True:
            raise InvalidRun(f"embedded mapped ledger status false at {label}")
        checks[label] = {
            "shape": list(values.shape),
            "runtime_dtype": expected_runtime,
            "canonical_dtype": canonical_dtype,
            "sha256": digest,
        }
    if len(checks) != 204:
        raise InvalidRun("mapped critical array count is not 204")
    return {"mapped_count": len(checks), "records": checks}


def verify_fail_closed_ledger(
    manifest: Mapping[str, Any], checkpoint: Mapping[str, Any]
) -> dict[str, Any]:
    expected = dict(manifest["required_fail_closed_outputs"])
    observed = dict(checkpoint["phase41_fail_closed_completion_ledger"])
    if observed != expected:
        raise InvalidRun("checkpoint fail-closed completion ledger drift")
    false_count = sum(value is False for value in observed.values())
    null_count = sum(value is None for value in observed.values())
    if false_count != 16 or null_count != 6:
        raise InvalidRun(
            f"fail-closed ledger count drift: false={false_count}, null={null_count}"
        )
    if observed.get("gate1_status") != "OPEN_PARTIAL_PROGRESS":
        raise InvalidRun("Gate 1 status drift")
    return {
        "false_count": false_count,
        "null_count": null_count,
        "gate1_status": observed["gate1_status"],
        "exact_match": True,
    }


def _complex_vector_from_pairs(
    values: Any, *, shape: tuple[int, ...], path: str
) -> np.ndarray:
    pairs = np.asarray(values, dtype=np.float64)
    if pairs.shape != shape + (2,) or not np.all(np.isfinite(pairs)):
        raise InvalidRun(f"invalid complex-pair vector at {path}")
    result = np.empty(shape, dtype=np.complex128)
    result.real[...] = pairs[..., 0]
    result.imag[...] = pairs[..., 1]
    return result


def _require_shape(
    array: np.ndarray, expected: tuple[int, ...], *, path: str
) -> np.ndarray:
    values = np.asarray(array)
    if values.shape != expected:
        raise InvalidRun(
            f"critical shape mismatch at {path}: {values.shape} != {expected}"
        )
    if not np.all(np.isfinite(values)):
        raise InvalidRun(f"critical nonfinite array at {path}")
    return values


def verify_critical_shapes(checkpoint: Mapping[str, Any]) -> dict[str, Any]:
    checked: dict[str, list[int]] = {}

    def require(path: str, values: np.ndarray, shape: tuple[int, ...]) -> None:
        _require_shape(values, shape, path=path)
        checked[path] = list(shape)

    conventions = checkpoint["coordinate_and_orientation_conventions"]
    require(
        "coordinate_scales",
        decode_array_record(conventions["coordinate_scales"], path="$.coordinate_scales"),
        (7,),
    )
    require(
        "row_scales",
        decode_array_record(conventions["row_scales"], path="$.row_scales"),
        (14,),
    )
    fixed_shapes = {
        "saddle_zero_w": (7,),
        "hessian_zero_w": (7, 7),
        "eigenvalues_zero": (7,),
        "oriented_eigenvectors_zero": (7, 7),
        "linear_map": (7, 7),
        "inverse_metric_mobility_w": (7, 7),
        "metric_tensor_w": (7, 7),
        "xi_reflection": (7, 7),
        "linear_map_z_from_xi": (7, 7),
    }
    for name, shape in fixed_shapes.items():
        require(
            f"fixed_metric.{name}",
            _array_at(checkpoint, "fixed_metric", name),
            shape,
        )
    map_shapes = {
        "DST_basis": (7, 7),
        "nested_basis": (7, 7),
        "DST_to_nested_transition": (7, 7),
        "reflection_w": (7, 7),
        "reflection_R14_interleaved": (14, 14),
    }
    for name, shape in map_shapes.items():
        require(
            f"mode_and_reflection_maps.{name}",
            _array_at(checkpoint, "mode_and_reflection_maps", name),
            shape,
        )
    require(
        "upward_chart.center",
        _array_at(checkpoint, "upward_chart", "center"),
        (7,),
    )
    require(
        "upward_chart.tangent",
        _array_at(checkpoint, "upward_chart", "tangent"),
        (7, 6),
    )
    for label in SADDLE_LABELS:
        base = checkpoint["saddles"][label]
        saddle_shapes = {
            "saddle_w": (7,),
            "saddle_z": (7,),
            "hessian_w": (7, 7),
            "hessian_eigenvalues": (7,),
            "hessian_xi": (7, 7),
            "hessian_xi_eigenvalues": (7,),
            "aligned_signed_frame_xi": (7, 7),
        }
        for name, shape in saddle_shapes.items():
            require(
                f"saddles.{label}.{name}",
                decode_array_record(
                    base[name], path=f"$.saddles.{label}.{name}"
                ),
                shape,
            )
        for name in ("negative", "positive"):
            dimension = 4 if name == "negative" else 3
            require(
                f"saddles.{label}.signed_restrictions.{name}",
                decode_array_record(
                    base["signed_restrictions"][name],
                    path=f"$.saddles.{label}.signed_restrictions.{name}",
                ),
                (dimension, dimension),
            )
            require(
                f"saddles.{label}.signed_projectors.{name}",
                decode_array_record(
                    base["signed_projectors"][name],
                    path=f"$.saddles.{label}.signed_projectors.{name}",
                ),
                (7, 7),
            )
        for name in ("lambda_0", "lambda_0.5", "lambda_1"):
            require(
                f"saddles.{label}.launch_matrices.{name}",
                decode_array_record(
                    base["launch_matrices"][name],
                    path=f"$.saddles.{label}.launch_matrices.{name}",
                ),
                (7, 7),
            )
    for label in PRIMARY_LABELS:
        require(
            f"all_parameter_vectors.{label}",
            _array_at(
                checkpoint,
                "primary_intersections",
                "all_parameter_vectors",
                label,
            ),
            (14,),
        )
    for label in TARGETS:
        target = checkpoint["primary_intersections"][
            "phase42_fixed_root_targets"
        ][label]
        require(
            f"targets.{label}.parameters",
            decode_array_record(
                target["parameter_vector"],
                path=f"$.targets.{label}.parameter_vector",
            ),
            (14,),
        )
        require(
            f"targets.{label}.J",
            decode_array_record(
                target["variational_scaled_root_jacobian"],
                path=f"$.targets.{label}.J",
            ),
            (14, 14),
        )
        chart_shapes = {
            "parameters_u": (6,),
            "omega": (7,),
            "direction_derivative": (7, 6),
            "launch_matrix": (7, 7),
            "initial_xi": (7,),
        }
        for name, shape in chart_shapes.items():
            require(
                f"targets.{label}.chart.{name}",
                decode_array_record(
                    target["chart_at_root"][name],
                    path=f"$.targets.{label}.chart_at_root.{name}",
                ),
                shape,
            )
        post_shapes = {
            "scaled_residual_interleaved": (14,),
            "physical_residual_interleaved": (14,),
            "gamma_state_z": (7,),
            "k_state_z": (7,),
            "gamma_frame_z": (14, 7),
            "k_frame_z": (14, 7),
            "regenerated_scaled_root_jacobian": (14, 14),
        }
        for name, shape in post_shapes.items():
            require(
                f"targets.{label}.post.{name}",
                decode_array_record(
                    target["post_solve_strict_DOP853_reevaluation"][name],
                    path=f"$.targets.{label}.post.{name}",
                ),
                shape,
            )
    return {"critical_named_array_count": len(checked), "records": checked}


def verify_target_cross_identities(
    manifest: Mapping[str, Any], checkpoint: Mapping[str, Any]
) -> dict[str, Any]:
    primaries = checkpoint["primary_intersections"]
    targets = primaries["phase42_fixed_root_targets"]
    critical_pins = manifest["checkpoint_consumer_protocol"][
        "critical_nested_array_pins"
    ]
    pin_names = {
        "shared_zero": ("shared_zero_parameter", "shared_zero_J"),
        "phi_plus": ("phi_plus_parameter", "phi_plus_J"),
        "a_plus": ("a_plus_parameter", "a_plus_J"),
    }
    point_checks: dict[str, Any] = {}
    coordinate_scales = _array_at(
        checkpoint,
        "coordinate_and_orientation_conventions",
        "coordinate_scales",
    )
    row_scales = _array_at(
        checkpoint,
        "coordinate_and_orientation_conventions",
        "row_scales",
    )
    if not np.array_equal(row_scales, np.repeat(1.0 / coordinate_scales, 2)):
        raise InvalidRun("checkpoint row scales do not equal repeated 1/scales")
    for label in TARGETS:
        target = targets[label]
        p_record = target["parameter_vector"]
        j_record = target["variational_scaled_root_jacobian"]
        p = decode_array_record(p_record, path=f"$.targets.{label}.p")
        j = decode_array_record(j_record, path=f"$.targets.{label}.J")
        pin_p, pin_j = pin_names[label]
        if p_record["canonical_little_endian_sha256"] != critical_pins[pin_p]:
            raise InvalidRun(f"{label} parameter nested SHA pin mismatch")
        if j_record["canonical_little_endian_sha256"] != critical_pins[pin_j]:
            raise InvalidRun(f"{label} J nested SHA pin mismatch")
        all_p = decode_array_record(
            primaries["all_parameter_vectors"][label],
            path=f"$.all_parameter_vectors.{label}",
        )
        result = target["phase41_primary_result"]
        result_p = np.asarray(result["parameters"], dtype=np.float64)
        result_j = np.asarray(
            result["variational_scaled_root_jacobian"], dtype=np.float64
        )
        regenerated_j = decode_array_record(
            target["post_solve_strict_DOP853_reevaluation"][
                "regenerated_scaled_root_jacobian"
            ],
            path=f"$.targets.{label}.post.regenerated_J",
        )
        if not (
            np.array_equal(p, all_p)
            and np.array_equal(p, result_p)
            and np.array_equal(j, result_j)
            and np.array_equal(j, regenerated_j)
        ):
            raise InvalidRun(f"{label} parameter/J duplicated fields differ")
        if target.get("accepted") is not True or result.get("accepted") is not True:
            raise InvalidRun(f"{label} fixed target is not accepted")
        if float(result["sphere_radius"]) != 1.0e-4:
            raise InvalidRun(f"{label} sphere radius drift")
        if float(result["shape_lambda"]) != 1.0:
            raise InvalidRun(f"{label} shape lambda drift")
        source = target["source_point"]
        expected_source = {
            "shared_zero": (0.0, 0.0),
            "phi_plus": (0.0, 0.001),
            "a_plus": (0.001, 0.0),
        }[label]
        if (float(source["delta_a"]), float(source["delta_phi"])) != expected_source:
            raise InvalidRun(f"{label} source point drift")
        chart = target["chart_at_root"]
        chart_u = decode_array_record(
            chart["parameters_u"], path=f"$.targets.{label}.chart_u"
        )
        if not np.array_equal(chart_u, p[7:13]):
            raise InvalidRun(f"{label} chart-u mismatch")
        launch = decode_array_record(
            chart["launch_matrix"], path=f"$.targets.{label}.launch"
        )
        saddle_launch = _array_at(
            checkpoint, "saddles", label, "launch_matrices", "lambda_1"
        )
        if not np.array_equal(launch, saddle_launch):
            raise InvalidRun(f"{label} launch matrix mismatch")
        post = target["post_solve_strict_DOP853_reevaluation"]
        gamma = decode_array_record(
            post["gamma_state_z"], path=f"$.targets.{label}.gamma"
        )
        k_state = decode_array_record(
            post["k_state_z"], path=f"$.targets.{label}.k_state"
        )
        gamma_frame = decode_array_record(
            post["gamma_frame_z"], path=f"$.targets.{label}.gamma_frame"
        )
        k_frame = decode_array_record(
            post["k_frame_z"], path=f"$.targets.{label}.k_frame"
        )
        scaled_residual = decode_array_record(
            post["scaled_residual_interleaved"],
            path=f"$.targets.{label}.scaled_residual",
        )
        physical_residual = decode_array_record(
            post["physical_residual_interleaved"],
            path=f"$.targets.{label}.physical_residual",
        )
        expected_physical = np.empty(14, dtype=float)
        expected_physical[0::2] = (gamma - k_state).real
        expected_physical[1::2] = (gamma - k_state).imag
        expected_scaled = row_scales * expected_physical
        assembled_j = row_scales[:, None] * np.column_stack(
            [gamma_frame, -k_frame]
        )
        recorded_gamma = _complex_vector_from_pairs(
            result["intersection_z"],
            shape=(7,),
            path=f"$.targets.{label}.phase41_result.intersection_z",
        )
        if not np.array_equal(gamma, recorded_gamma):
            raise InvalidRun(f"{label} Gamma/result state mismatch")
        if not np.array_equal(expected_physical, physical_residual):
            raise InvalidRun(f"{label} physical residual identity mismatch")
        if not np.array_equal(expected_scaled, scaled_residual):
            raise InvalidRun(f"{label} scaled residual identity mismatch")
        if not np.array_equal(assembled_j, j):
            raise InvalidRun(f"{label} [Gamma,-K] J identity mismatch")
        point_checks[label] = {
            "parameter_sha256": p_record["canonical_little_endian_sha256"],
            "J_sha256": j_record["canonical_little_endian_sha256"],
            "source_point": list(expected_source),
            "sphere_radius": 1.0e-4,
            "shape_lambda": 1.0,
            "identities_passed": True,
        }
    return {
        "row_scale_identity_passed": True,
        "points": point_checks,
    }


def rehydrate_checkpoint(
    manifest: Mapping[str, Any], checkpoint: Mapping[str, Any], raw: bytes
) -> CheckpointContext:
    envelope = verify_checkpoint_envelope(manifest, checkpoint, raw)
    critical_shapes = verify_critical_shapes(checkpoint)
    cross = verify_target_cross_identities(manifest, checkpoint)
    completion = verify_fail_closed_ledger(manifest, checkpoint)
    phase41 = import_pinned_phase41(manifest)
    no_solve_counter = install_forbidden_solve_guards(phase41)

    fixed_payload = checkpoint["fixed_metric"]
    fixed = phase41.FixedMetric(
        saddle_zero_w=_array_at(checkpoint, "fixed_metric", "saddle_zero_w"),
        hessian_zero_w=_array_at(checkpoint, "fixed_metric", "hessian_zero_w"),
        eigenvalues_zero=_array_at(checkpoint, "fixed_metric", "eigenvalues_zero"),
        oriented_eigenvectors_zero=_array_at(
            checkpoint, "fixed_metric", "oriented_eigenvectors_zero"
        ),
        linear_map=_array_at(checkpoint, "fixed_metric", "linear_map"),
        inverse_metric_mobility_w=_array_at(
            checkpoint, "fixed_metric", "inverse_metric_mobility_w"
        ),
        metric_tensor_w=_array_at(
            checkpoint, "fixed_metric", "metric_tensor_w"
        ),
        xi_reflection=_array_at(checkpoint, "fixed_metric", "xi_reflection"),
    )
    del fixed_payload
    chart_payload = checkpoint["upward_chart"]
    chart = phase41.Chart(
        center=_array_at(checkpoint, "upward_chart", "center"),
        tangent=_array_at(checkpoint, "upward_chart", "tangent"),
        orientation_determinant=float(chart_payload["orientation_determinant"]),
        provenance=dict(chart_payload["provenance"]),
    )
    if chart.orientation_determinant != 1.0:
        raise InvalidRun("upward chart orientation determinant drift")

    saddles: dict[str, Any] = {}
    launch_errors: dict[str, float] = {}
    for label in SADDLE_LABELS:
        record = checkpoint["saddles"][label]
        source = record["source_point"]
        saddle = phase41.SaddleData(
            delta_a=float(source["delta_a"]),
            delta_phi=float(source["delta_phi"]),
            saddle_w=decode_array_record(
                record["saddle_w"], path=f"$.saddles.{label}.saddle_w"
            ),
            saddle_z=decode_array_record(
                record["saddle_z"], path=f"$.saddles.{label}.saddle_z"
            ),
            action=_complex_pair(record["action"], path=f"$.saddles.{label}.action"),
            gradient_max_abs=float(record["gradient_max_abs"]),
            hessian_w=decode_array_record(
                record["hessian_w"], path=f"$.saddles.{label}.hessian_w"
            ),
            hessian_eigenvalues=decode_array_record(
                record["hessian_eigenvalues"],
                path=f"$.saddles.{label}.hessian_eigenvalues",
            ),
            hessian_inertia=tuple(int(v) for v in record["hessian_inertia"]),
            hessian_xi=decode_array_record(
                record["hessian_xi"], path=f"$.saddles.{label}.hessian_xi"
            ),
            hessian_xi_eigenvalues=decode_array_record(
                record["hessian_xi_eigenvalues"],
                path=f"$.saddles.{label}.hessian_xi_eigenvalues",
            ),
            aligned_signed_frame_xi=decode_array_record(
                record["aligned_signed_frame_xi"],
                path=f"$.saddles.{label}.aligned_signed_frame_xi",
            ),
            signed_restrictions={
                -1: decode_array_record(
                    record["signed_restrictions"]["negative"],
                    path=f"$.saddles.{label}.restrictions.negative",
                ),
                1: decode_array_record(
                    record["signed_restrictions"]["positive"],
                    path=f"$.saddles.{label}.restrictions.positive",
                ),
            },
            signed_projectors={
                -1: decode_array_record(
                    record["signed_projectors"]["negative"],
                    path=f"$.saddles.{label}.projectors.negative",
                ),
                1: decode_array_record(
                    record["signed_projectors"]["positive"],
                    path=f"$.saddles.{label}.projectors.positive",
                ),
            },
            signed_subspace_min_principal_overlap=float(
                record["signed_subspace_min_principal_overlap"]
            ),
        )
        pinned_launch = decode_array_record(
            record["launch_matrices"]["lambda_1"],
            path=f"$.saddles.{label}.launch.lambda_1",
        )
        regenerated_launch = saddle.launch_matrix(1.0)
        error = float(np.max(np.abs(regenerated_launch - pinned_launch)))
        if error > 5.0e-14:
            raise InvalidRun(f"rehydrated launch matrix drift at {label}: {error}")
        launch_errors[label] = error
        saddles[label] = saddle

    points: dict[str, PointContext] = {}
    for label in TARGETS:
        target = checkpoint["primary_intersections"][
            "phase42_fixed_root_targets"
        ][label]
        source = target["source_point"]
        point = (float(source["delta_a"]), float(source["delta_phi"]))
        points[label] = PointContext(
            label=label,
            source_point=point,
            parameters=decode_array_record(
                target["parameter_vector"], path=f"$.targets.{label}.p"
            ).copy(),
            checkpoint_jacobian=decode_array_record(
                target["variational_scaled_root_jacobian"],
                path=f"$.targets.{label}.J",
            ).copy(),
            model=phase41.numeric_model(*point),
            saddle=saddles[label],
            checkpoint_target=target,
        )
    coordinate_scales = _array_at(
        checkpoint,
        "coordinate_and_orientation_conventions",
        "coordinate_scales",
    )
    row_scales = _array_at(
        checkpoint,
        "coordinate_and_orientation_conventions",
        "row_scales",
    )
    reflection = _array_at(
        checkpoint, "mode_and_reflection_maps", "reflection_w"
    )
    validation = {
        "checkpoint_envelope": {
            key: value
            for key, value in envelope.items()
            if key != "decoded_arrays"
        },
        "critical_shapes": critical_shapes,
        "cross_field_identities": cross,
        "completion_ledger": completion,
        "launch_rehydration_max_abs": launch_errors,
    }
    return CheckpointContext(
        raw_payload=checkpoint,
        decoded_arrays=envelope["decoded_arrays"],
        phase41=phase41,
        fixed=fixed,
        chart=chart,
        coordinate_scales=coordinate_scales,
        row_scales=row_scales,
        reflection=reflection,
        points=points,
        no_solve_call_counter=no_solve_counter,
        validation=validation,
    )


def uninterleaved(values: np.ndarray) -> np.ndarray:
    real = np.asarray(values, dtype=float).reshape(-1)
    if real.size % 2:
        raise InvalidRun("cannot complex-uninterleave an odd-length vector")
    result = np.empty(real.size // 2, dtype=np.complex128)
    result.real[...] = real[0::2]
    result.imag[...] = real[1::2]
    return result


def tier_specs(manifest: Mapping[str, Any]) -> dict[str, TierSpec]:
    source = manifest["integration_tiers"]
    mapping = {
        "production_state": source["P41_production_state_map"],
        "production_augmented": source["P41_production_augmented_map"],
        "tight_state": source["P42_tight_state_map"],
        "tight_augmented": source["P42_tight_augmented_map"],
        "radau_state": source["P42_cross_method_state_map"],
    }
    result: dict[str, TierSpec] = {}
    for name, record in mapping.items():
        result[name] = TierSpec(
            name=name,
            method=str(record["method"]),
            representation=str(record["representation"]),
            rtol=float(record["rtol"]),
            atol=float(record["atol"]),
            max_step=float(record["max_step"]),
        )
    expected = {
        "production_state": ("DOP853", 2e-10, 2e-12, 0.04),
        "production_augmented": ("DOP853", 8e-11, 8e-13, 0.025),
        "tight_state": ("DOP853", 2e-12, 2e-14, 0.01),
        "tight_augmented": ("DOP853", 2e-12, 2e-14, 0.01),
        "radau_state": ("Radau", 5e-12, 5e-14, 0.01),
    }
    for name, values in expected.items():
        observed = result[name]
        if (
            observed.method,
            observed.rtol,
            observed.atol,
            observed.max_step,
        ) != values:
            raise InvalidRun(f"integration tier drift: {name}")
    return result


def parameter_margins(phase41: ModuleType, parameters: np.ndarray) -> dict[str, Any]:
    values = _require_shape(np.asarray(parameters, dtype=float), (14,), path="parameters")
    lower, upper = phase41.parameter_bounds()
    lower_margin = values - lower
    upper_margin = upper - values
    strict = bool(np.all(lower_margin > 0.0) and np.all(upper_margin > 0.0))
    return {
        "strictly_inside": strict,
        "minimum_lower_margin": float(np.min(lower_margin)),
        "minimum_upper_margin": float(np.min(upper_margin)),
        "minimum_two_sided_margin": float(
            min(np.min(lower_margin), np.min(upper_margin))
        ),
        "lower_margins": lower_margin,
        "upper_margins": upper_margin,
    }


def affine_chart_direction(
    context: CheckpointContext, parameters_u: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(parameters_u, dtype=float).reshape(6)
    vector = context.chart.center + context.chart.tangent @ values
    norm = float(np.linalg.norm(vector))
    if not math.isfinite(norm) or norm <= 0.0:
        raise SlotEvaluationError("affine chart vector vanished/nonfinite")
    omega = vector / norm
    derivative = (
        (np.eye(7) - np.outer(omega, omega))
        @ context.chart.tangent
        / norm
    )
    return omega, derivative


def geodesic_u2_direction(
    context: CheckpointContext,
    point: PointContext,
    parameters_u: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(parameters_u, dtype=float).reshape(6)
    base_u = point.parameters[7:13]
    difference = values - base_u
    if np.max(np.abs(np.delete(difference, 1))) > 5.0e-16:
        raise SlotEvaluationError("geodesic chart may vary only u2")
    omega, derivative = affine_chart_direction(context, base_u)
    tangent = derivative[:, 1]
    speed = float(np.linalg.norm(tangent))
    if speed <= 0.0 or not math.isfinite(speed):
        raise SlotEvaluationError("geodesic u2 tangent vanished")
    delta = float(difference[1])
    angle = speed * delta
    omega_geo = (
        math.cos(angle) * omega
        + math.sin(angle) * tangent / speed
    )
    # The derivative matrix is retained only to make the same-first-tangent
    # statement explicit; no geodesic augmented map is used.
    derivative_geo = derivative.copy()
    derivative_geo[:, 1] = (
        -speed * math.sin(angle) * omega
        + math.cos(angle) * tangent
    )
    return omega_geo, derivative_geo


def chart_direction(
    context: CheckpointContext,
    point: PointContext,
    parameters_u: np.ndarray,
    chart_kind: str,
) -> tuple[np.ndarray, np.ndarray]:
    if chart_kind == "affine":
        return affine_chart_direction(context, parameters_u)
    if chart_kind == "geodesic_u2":
        return geodesic_u2_direction(context, point, parameters_u)
    raise SlotEvaluationError(f"unknown chart kind: {chart_kind}")


def solver_ledger(solution: Any, xi_values: np.ndarray, tier: TierSpec) -> dict[str, Any]:
    xi_matrix = np.asarray(xi_values, dtype=np.complex128)
    if xi_matrix.ndim != 2 or xi_matrix.shape[0] != 7:
        raise SlotEvaluationError("solver xi ledger has wrong shape")
    xi_norm_raw = float(np.max(np.linalg.norm(xi_matrix, axis=0)))
    xi_norm_max: float | None = xi_norm_raw if math.isfinite(xi_norm_raw) else None
    record = {
        "success": bool(solution.success),
        "message": str(solution.message),
        "method": tier.method,
        "representation": tier.representation,
        "rtol": tier.rtol,
        "atol": tier.atol,
        "max_step": tier.max_step,
        "nfev": int(solution.nfev),
        "njev": int(getattr(solution, "njev", 0) or 0),
        "nlu": int(getattr(solution, "nlu", 0) or 0),
        "stored_time_count": int(solution.t.size),
        "accepted_step_count": int(max(0, solution.t.size - 1)),
        "xi_norm_max": xi_norm_max,
        "xi_norm_nonfinite": xi_norm_max is None,
        "flow_norm_strict_cap": 40.0,
        "fallback_used": False,
        "no_fallback_method_used": True,
    }
    if not bool(solution.success):
        raise SlotEvaluationError(str(solution.message), payload={"solver": record})
    if xi_norm_max is None or xi_norm_max >= 40.0:
        raise SlotEvaluationError(
            "flow exceeded the frozen xi-norm cap", payload={"solver": record}
        )
    return record


def integrate_state_map(
    context: CheckpointContext,
    point: PointContext,
    parameters: np.ndarray,
    tier: TierSpec,
    chart_kind: str,
) -> FlowEvaluation:
    values = np.asarray(parameters, dtype=float).reshape(14)
    margins = parameter_margins(context.phase41, values)
    if margins["strictly_inside"] is not True:
        raise SlotEvaluationError("perturbed parameter left the frozen box")
    flow_time = float(values[13])
    if not 0.1 <= flow_time <= 13.5:
        raise SlotEvaluationError("flow time left frozen interval")
    omega, _derivative = chart_direction(
        context, point, values[7:13], chart_kind
    )
    launch = point.saddle.launch_matrix(1.0)
    initial_xi = 1.0e-4 * (launch @ omega)

    if tier.name == "production_state":
        if chart_kind != "affine":
            raise SlotEvaluationError("Phase41 production map requires affine chart")
        state_z, tangent, integration = context.phase41.integrate_chart(
            point.model,
            point.saddle,
            context.fixed,
            context.chart,
            values[7:13],
            flow_time,
            1.0e-4,
            1.0,
            with_tangent=False,
            method="DOP853",
        )
        if tangent is not None:
            raise SlotEvaluationError("production state-only map returned tangents")
        final_w = state_z / context.coordinate_scales
        final_xi = np.linalg.solve(
            context.fixed.linear_map, final_w - point.saddle.saddle_w
        )
        solver = {
            "success": True,
            "message": "pinned Phase41 integrate_chart state-only map",
            "method": "DOP853",
            "representation": tier.representation,
            "rtol": tier.rtol,
            "atol": tier.atol,
            "max_step": tier.max_step,
            "nfev": None,
            "njev": None,
            "nlu": None,
            "stored_time_count": int(integration["solver_steps"]),
            "accepted_step_count": int(integration["solver_steps"]) - 1,
            "xi_norm_max": float(integration["xi_norm_max"]),
            "flow_norm_strict_cap": 40.0,
            "pinned_API_does_not_expose_function_counts": True,
            "fallback_used": False,
            "no_fallback_method_used": True,
        }
    elif tier.method == "DOP853":
        solution = solve_ivp(
            lambda _time, xi: context.phase41.flow_xi(
                point.model, point.saddle, context.fixed, xi
            ),
            (0.0, flow_time),
            initial_xi,
            method="DOP853",
            rtol=tier.rtol,
            atol=tier.atol,
            max_step=tier.max_step,
        )
        xi_values = np.asarray(solution.y, dtype=np.complex128)
        final_xi = xi_values[:, -1]
    elif tier.method == "Radau":
        real_initial = context.phase41.interleaved(initial_xi)

        def real_rhs(_time: float, real_xi: np.ndarray) -> np.ndarray:
            xi = uninterleaved(real_xi)
            return context.phase41.interleaved(
                context.phase41.flow_xi(
                    point.model, point.saddle, context.fixed, xi
                )
            )

        solution = solve_ivp(
            real_rhs,
            (0.0, flow_time),
            real_initial,
            method="Radau",
            rtol=tier.rtol,
            atol=tier.atol,
            max_step=tier.max_step,
        )
        real_y = np.asarray(solution.y, dtype=float)
        xi_values = np.empty((7, real_y.shape[1]), dtype=np.complex128)
        xi_values.real[...] = real_y[0::2]
        xi_values.imag[...] = real_y[1::2]
        final_xi = xi_values[:, -1]
    else:
        raise SlotEvaluationError(f"unsupported state solver: {tier.method}")
    if tier.name == "production_state":
        state_z = np.asarray(state_z, dtype=np.complex128)
    else:
        solver = solver_ledger(solution, xi_values, tier)
        state_z = context.coordinate_scales * (
            point.saddle.saddle_w + context.fixed.linear_map @ final_xi
        )
    return FlowEvaluation(
        xi=final_xi,
        state_z=state_z,
        omega=omega,
        initial_xi=initial_xi,
        solver={**solver, "bounds_margins": margins},
    )


def assemble_residual(
    context: CheckpointContext,
    point: PointContext,
    parameters: np.ndarray,
    k_state_z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gamma_state, gamma_tangent = context.phase41.gamma_cap(
        point.model, parameters[:6], float(parameters[6])
    )
    residual = context.phase41.interleaved(
        (gamma_state - k_state_z) / context.coordinate_scales
    )
    return residual, gamma_state, gamma_tangent


def integrate_tight_augmented(
    context: CheckpointContext,
    point: PointContext,
    tier: TierSpec,
    fractions: Sequence[float],
) -> AugmentedEvaluation:
    if tier.name != "tight_augmented":
        raise InvalidRun("tight augmented wrapper received wrong tier")
    p = point.parameters
    omega, domega = affine_chart_direction(context, p[7:13])
    launch = point.saddle.launch_matrix(1.0)
    initial_xi = 1.0e-4 * (launch @ omega)
    initial_tangent = 1.0e-4 * (launch @ domega)
    augmented_initial = np.concatenate([initial_xi, initial_tangent.reshape(-1)])

    def augmented_rhs(_time: float, augmented: np.ndarray) -> np.ndarray:
        xi = augmented[:7]
        tangent = augmented[7:].reshape(7, 6)
        derivative = -np.conjugate(
            context.phase41.hessian_xi(
                point.model, point.saddle, context.fixed, xi
            )
            @ tangent
        )
        return np.concatenate(
            [
                context.phase41.flow_xi(
                    point.model, point.saddle, context.fixed, xi
                ),
                derivative.reshape(-1),
            ]
        )

    flow_time = float(p[13])
    solution = solve_ivp(
        augmented_rhs,
        (0.0, flow_time),
        augmented_initial,
        method="DOP853",
        rtol=tier.rtol,
        atol=tier.atol,
        max_step=tier.max_step,
        dense_output=True,
    )
    if solution.sol is None:
        raise SlotEvaluationError("tight augmented dense solution unavailable")
    xi_values = np.asarray(solution.y[:7], dtype=np.complex128)
    solver = solver_ledger(solution, xi_values, tier)
    sample_fractions = np.asarray(fractions, dtype=float)
    if not np.array_equal(sample_fractions, np.array([0.0, 0.25, 0.5, 0.75, 1.0])):
        raise InvalidRun("sample fraction protocol drift")
    sample_times = flow_time * sample_fractions
    sampled = np.asarray(solution.sol(sample_times), dtype=np.complex128)
    fraction_xi = sampled[:7].T
    fraction_tangents = sampled[7:].T.reshape(5, 7, 6)
    final_xi = fraction_xi[-1]
    final_tangent = fraction_tangents[-1]
    linear_z = np.diag(context.coordinate_scales) @ context.fixed.linear_map
    state_z = context.coordinate_scales * (
        point.saddle.saddle_w + context.fixed.linear_map @ final_xi
    )
    tangent_z = linear_z @ final_tangent
    positive_time_tangent = linear_z @ context.phase41.flow_xi(
        point.model, point.saddle, context.fixed, final_xi
    )
    k_frame = context.phase41.real_frame(
        np.column_stack([tangent_z, positive_time_tangent])
    )
    residual, gamma_state, gamma_tangent = assemble_residual(
        context, point, p, state_z
    )
    gamma_frame = context.phase41.real_frame(gamma_tangent)
    jacobian = context.row_scales[:, None] * np.column_stack(
        [gamma_frame, -k_frame]
    )
    return AugmentedEvaluation(
        xi=final_xi,
        state_z=state_z,
        k_frame_z=k_frame,
        jacobian=jacobian,
        gamma_state_z=gamma_state,
        gamma_frame_z=gamma_frame,
        residual=residual,
        fraction_times=sample_times,
        fraction_xi=fraction_xi,
        fraction_tangents=fraction_tangents,
        positive_time_tangent_z=positive_time_tangent,
        solver=solver,
    )


def integrate_production_augmented(
    context: CheckpointContext, point: PointContext
) -> dict[str, Any]:
    (
        residual,
        jacobian,
        gamma_state,
        k_state,
        gamma_frame,
        k_frame,
        integration,
    ) = context.phase41.residual_and_variational_jacobian(
        point.parameters,
        point.model,
        point.saddle,
        context.fixed,
        context.chart,
        1.0e-4,
        1.0,
        "DOP853",
    )
    endpoint_w = np.asarray(k_state) / context.coordinate_scales
    endpoint_xi = np.linalg.solve(
        context.fixed.linear_map, endpoint_w - point.saddle.saddle_w
    )
    return {
        "parameters": point.parameters,
        "bounds_margins": parameter_margins(context.phase41, point.parameters),
        "residual": residual,
        "jacobian": jacobian,
        "gamma_state_z": gamma_state,
        "k_state_z": k_state,
        "gamma_frame_z": gamma_frame,
        "k_frame_z": k_frame,
        "endpoint_xi": endpoint_xi,
        "integration": integration,
        "solver": {
            "success": True,
            "message": "pinned Phase41 augmented DOP853 map",
            "method": "DOP853",
            "representation": "complex xi plus 7x6 complex chart tangent",
            "rtol": 8.0e-11,
            "atol": 8.0e-13,
            "max_step": 0.025,
            "nfev": None,
            "njev": None,
            "nlu": None,
            "stored_time_count": int(integration["solver_steps"]),
            "accepted_step_count": int(integration["solver_steps"]) - 1,
            "xi_norm_max": float(integration["xi_norm_max"]),
            "flow_norm_strict_cap": 40.0,
            "pinned_API_does_not_expose_function_counts": True,
            "fallback_used": False,
            "no_fallback_method_used": True,
        },
    }


class MapEvaluator:
    def __init__(
        self,
        context: CheckpointContext,
        tiers: Mapping[str, TierSpec],
        ledger: SlotLedger,
    ) -> None:
        self.context = context
        self.tiers = tiers
        self.ledger = ledger
        self.k_cache: dict[tuple[Any, ...], FlowEvaluation] = {}
        self.residuals: dict[str, np.ndarray] = {}

    @staticmethod
    def cache_key(
        point: PointContext,
        tier: TierSpec,
        chart_kind: str,
        parameters: np.ndarray,
    ) -> tuple[Any, ...]:
        return (
            point.label,
            tier.name,
            tier.method,
            tier.rtol,
            tier.atol,
            tier.max_step,
            chart_kind,
            *tuple(float(v) for v in parameters[7:14]),
        )

    def evaluate_slot(
        self,
        slot_key: str,
        point: PointContext,
        tier_name: str,
        chart_kind: str,
        parameters: np.ndarray,
    ) -> np.ndarray | None:
        if slot_key not in self.ledger.slots:
            raise InvalidRun(f"attempted undeclared map slot: {slot_key}")
        tier = self.tiers[tier_name]
        try:
            values = np.asarray(parameters, dtype=float).reshape(14)
            margins = parameter_margins(self.context.phase41, values)
            if margins["strictly_inside"] is not True:
                raise SlotEvaluationError("parameter perturbation is outside box")
            cache_key = self.cache_key(point, tier, chart_kind, values)
            if cache_key not in self.k_cache:
                self.k_cache[cache_key] = integrate_state_map(
                    self.context, point, values, tier, chart_kind
                )
            flow = self.k_cache[cache_key]
            residual, gamma_state, _gamma_tangent = assemble_residual(
                self.context, point, values, flow.state_z
            )
            payload = {
                "parameters": values,
                "bounds_margins": margins,
                "cache_key": list(cache_key),
                "cache_reused": sum(
                    1
                    for other in self.residuals
                    if self.ledger.slots[other]["metadata"].get("cache_key")
                    == json_ready(list(cache_key))
                )
                > 0,
                "solver": flow.solver,
                "omega": flow.omega,
                "initial_xi": flow.initial_xi,
                "endpoint_xi": flow.xi,
                "gamma_state_z": gamma_state,
                "k_state_z": flow.state_z,
                "scaled_residual": residual,
            }
            self.ledger.slots[slot_key]["metadata"]["cache_key"] = json_ready(
                list(cache_key)
            )
            self.ledger.finish(slot_key, "SUCCESS", payload=payload)
            self.residuals[slot_key] = residual
            return residual
        except InvalidRun:
            raise
        except Exception as exc:
            failure_payload = {
                "parameters": np.asarray(parameters, dtype=float).reshape(14),
                "bounds_margins": parameter_margins(
                    self.context.phase41,
                    np.asarray(parameters, dtype=float).reshape(14),
                ),
                "tier": dataclasses.asdict(tier),
                "chart_kind": chart_kind,
                "fallback_used": False,
                "no_fallback_method_used": True,
                "solver_counts_unavailable_reason": (
                    "exception occurred before a successful solver return"
                ),
            }
            if isinstance(exc, SlotEvaluationError):
                failure_payload.update(exc.payload)
            self.ledger.finish(
                slot_key,
                "EVALUATION_FAILED",
                payload=failure_payload,
                error=f"{type(exc).__name__}: {exc}",
            )
            return None


def endpoint_slot_key(
    point: str,
    tier: str,
    chart_kind: str,
    column: int,
    step: float,
    sign: int,
) -> str:
    sign_name = "plus" if sign > 0 else "minus"
    return (
        f"endpoint|{point}|{tier}|{chart_kind}|col={column}|"
        f"h={format(float(step), '.17g')}|{sign_name}"
    )


def d2_slot_key(
    point: str, tier: str, chart_kind: str, column: int, step: float
) -> str:
    return (
        f"D2|{point}|{tier}|{chart_kind}|col={column}|"
        f"h={format(float(step), '.17g')}"
    )


def center_slot_key(point: str, tier: str, chart_kind: str) -> str:
    return f"center|{point}|{tier}|{chart_kind}"


def endpoint_specifications(
    manifest: Mapping[str, Any],
) -> dict[tuple[str, str, int], tuple[float, ...]]:
    protocol = manifest["finite_difference_protocol"]
    old = {
        int(column): tuple(float(h) for h in steps)
        for column, steps in protocol[
            "phase41_production_negative_control_steps_by_zero_based_column"
        ].items()
    }
    main = tuple(float(h) for h in protocol["phase42_all_fourteen_columns_main_ladder"])
    tail = tuple(float(h) for h in protocol["u2_additional_dyadic_tail"])
    old_u2 = tuple(
        float(h)
        for h in protocol["u2_exact_phase41_reproduction_steps_across_state_tiers"]
    )

    def ordered_union(*groups: Iterable[float]) -> tuple[float, ...]:
        result: list[float] = []
        for group in groups:
            for value in group:
                number = float(value)
                if number not in result:
                    result.append(number)
        return tuple(result)

    specs: dict[tuple[str, str, int], tuple[float, ...]] = {}
    for column in range(14):
        specs[("production_state", "affine", column)] = old[column]
    specs[("production_state", "affine", 8)] = ordered_union(
        old[8], main, tail
    )
    for column in range(14):
        specs[("tight_state", "affine", column)] = main
    specs[("tight_state", "affine", 8)] = ordered_union(main, tail, old_u2)
    specs[("tight_state", "geodesic_u2", 8)] = ordered_union(
        main, tail, old_u2
    )
    specs[("radau_state", "affine", 8)] = ordered_union(main, old_u2)
    specs[("radau_state", "affine", 13)] = main
    specs[("radau_state", "geodesic_u2", 8)] = ordered_union(main, old_u2)
    pair_count = sum(len(steps) for steps in specs.values())
    if pair_count != 149:
        raise InvalidRun(f"endpoint specification pair count is {pair_count}, not 149")
    return specs


def preenumerate_slot_ledger(
    manifest: Mapping[str, Any], ledger: SlotLedger
) -> dict[str, Any]:
    specs = endpoint_specifications(manifest)
    endpoint_count = 0
    d2_count = 0
    center_kinds = (
        ("production_state", "affine"),
        ("tight_state", "affine"),
        ("tight_state", "geodesic_u2"),
        ("radau_state", "affine"),
        ("radau_state", "geodesic_u2"),
    )
    for point in TARGETS:
        for tier, chart_kind in center_kinds:
            ledger.declare(
                center_slot_key(point, tier, chart_kind),
                slot_kind="center",
                point=point,
                tier=tier,
                chart_kind=chart_kind,
            )
        for tier in ("production_augmented", "tight_augmented"):
            ledger.declare(
                f"augmented|{point}|{tier}",
                slot_kind="augmented_center",
                point=point,
                tier=tier,
            )
        for (tier, chart_kind, column), steps in specs.items():
            for step in steps:
                d2_key = d2_slot_key(point, tier, chart_kind, column, step)
                ledger.declare(
                    d2_key,
                    slot_kind="D2",
                    point=point,
                    tier=tier,
                    chart_kind=chart_kind,
                    column=column,
                    h=step,
                )
                d2_count += 1
                for sign in (-1, 1):
                    ledger.declare(
                        endpoint_slot_key(
                            point, tier, chart_kind, column, step, sign
                        ),
                        slot_kind="endpoint",
                        point=point,
                        tier=tier,
                        chart_kind=chart_kind,
                        column=column,
                        h=step,
                        sign=sign,
                    )
                    endpoint_count += 1
        for column in range(14):
            for reference in ("coarse", "primary", "fine"):
                ledger.declare(
                    f"R4|{point}|tight_state|affine|col={column}|{reference}",
                    slot_kind="fixed_R4",
                    point=point,
                    tier="tight_state",
                    chart_kind="affine",
                    column=column,
                    reference=reference,
                )
        for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            for direction in range(6):
                local_key = (
                    f"local_RHS|{point}|fraction={format(fraction,'.2g')}|"
                    f"direction={direction}"
                )
                ledger.declare(
                    local_key,
                    slot_kind="local_RHS_direction",
                    point=point,
                    fraction=fraction,
                    direction=direction,
                )
                for epsilon in (2.0e-5, 1.0e-5, 5.0e-6):
                    for sign in (-1, 1):
                        ledger.declare(
                            f"{local_key}|epsilon={format(epsilon,'.17g')}|"
                            f"{'plus' if sign > 0 else 'minus'}",
                            slot_kind="local_RHS_perturbation",
                            point=point,
                            fraction=fraction,
                            direction=direction,
                            epsilon=epsilon,
                            sign=sign,
                        )
        for control in (
            "positive_K_time_tangent",
            "checkpoint_negative_time_column",
            "production_negative_time_column",
            "state_only_R4_time_column",
        ):
            ledger.declare(
                f"time_control|{point}|{control}",
                slot_kind="time_control",
                point=point,
                control=control,
            )
        for matrix_kind in (
            "three_way_J",
            "phase41_negative_control",
            "chart",
            "local_RHS",
            "all_column_R4",
            "u2_disentanglement",
            "homotopy",
        ):
            ledger.declare(
                f"matrix|{point}|{matrix_kind}",
                slot_kind="matrix_diagnostic",
                point=point,
                diagnostic=matrix_kind,
            )
        for mutation in (
            "positive_column_rescaling",
            "single_reference_column_flip",
            "no_sampled_t_used",
        ):
            ledger.declare(
                f"mutation|{point}|{mutation}",
                slot_kind="homotopy_mutation_control",
                point=point,
                mutation=mutation,
            )
        for cause in (
            "TRUNCATION_EVIDENCE",
            "SOLVER_NOISE_EVIDENCE",
            "CHART_CURVATURE_EVIDENCE",
            "STEP_PAIR_SELECTION_ARTIFACT",
            "VARIATIONAL_RHS_BUG_EVIDENCE",
            "PRODUCTION_TANGENT_SOLVER_EVIDENCE",
            "INTEGRATED_VARIATIONAL_BUG_EVIDENCE",
            "UNRESOLVED",
        ):
            ledger.declare(
                f"cause|{point}|{cause}",
                slot_kind="cause",
                point=point,
                cause=cause,
            )
    for cause in (
        "TRUNCATION_EVIDENCE",
        "SOLVER_NOISE_EVIDENCE",
        "CHART_CURVATURE_EVIDENCE",
        "STEP_PAIR_SELECTION_ARTIFACT",
        "VARIATIONAL_RHS_BUG_EVIDENCE",
        "PRODUCTION_TANGENT_SOLVER_EVIDENCE",
        "INTEGRATED_VARIATIONAL_BUG_EVIDENCE",
        "UNRESOLVED",
    ):
        ledger.declare(
            f"cause|aggregate|{cause}",
            slot_kind="cause_aggregate",
            cause=cause,
        )
    if endpoint_count != 894 or d2_count != 447:
        raise InvalidRun(
            f"slot count drift: endpoints={endpoint_count}, D2={d2_count}"
        )
    if len(ledger.slots) != 2192:
        raise InvalidRun(
            f"total predeclared slot count is {len(ledger.slots)}, not 2192"
        )
    return {
        "endpoint_count": endpoint_count,
        "D2_count": d2_count,
        "fixed_R4_count": 126,
        "local_RHS_direction_count": 90,
        "local_RHS_perturbation_count": 540,
        "cause_count": 32,
        "homotopy_mutation_control_count": 9,
        "total_declared_slot_count": len(ledger.slots),
        "endpoint_specs": {
            f"{tier}|{chart}|{column}": list(steps)
            for (tier, chart, column), steps in specs.items()
        },
    }


def vector_rel(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left).reshape(-1)
    b = np.asarray(right).reshape(-1)
    if a.shape != b.shape or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise SlotEvaluationError("relative-vector inputs are mismatched/nonfinite")
    return float(
        np.linalg.norm(a - b)
        / max(np.linalg.norm(a), np.linalg.norm(b), 1.0e-30)
    )


def operator_rel(left: np.ndarray, right: np.ndarray) -> float:
    a = np.asarray(left)
    b = np.asarray(right)
    if a.shape != b.shape or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise SlotEvaluationError("relative-operator inputs are mismatched/nonfinite")
    return float(
        np.linalg.norm(a - b, ord=2)
        / max(np.linalg.norm(a, ord=2), np.linalg.norm(b, ord=2), 1.0e-30)
    )


def vector_direction_metrics(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    a = np.asarray(left, dtype=float).reshape(-1)
    b = np.asarray(right, dtype=float).reshape(-1)
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a <= 0.0 or norm_b <= 0.0:
        raise SlotEvaluationError("zero vector in direction comparison")
    cosine = float(np.dot(a, b) / (norm_a * norm_b))
    cosine = max(-1.0, min(1.0, cosine))
    return {
        "symmetric_relative": vector_rel(a, b),
        "signed_cosine": cosine,
        "angle_sine": float(math.sqrt(max(0.0, 1.0 - cosine * cosine))),
        "norm_left": norm_a,
        "norm_right": norm_b,
        "abs_norm_ratio_minus_one": abs(norm_a / norm_b - 1.0),
    }


def matrix_summary(matrix: np.ndarray) -> dict[str, Any]:
    values = np.asarray(matrix, dtype=float)
    if values.shape != (14, 14) or not np.all(np.isfinite(values)):
        raise SlotEvaluationError("matrix summary requires finite R14xR14 matrix")
    column_norms = np.linalg.norm(values, axis=0)
    if np.any(column_norms <= 0.0):
        raise SlotEvaluationError("matrix has zero column")
    normalized = values / column_norms
    raw_sign, raw_log_abs = np.linalg.slogdet(values)
    sign, log_abs = np.linalg.slogdet(normalized)
    singular = np.linalg.svd(normalized, compute_uv=False)
    finite_log_abs = float(log_abs) if np.isfinite(log_abs) else None
    finite_condition = (
        float(singular[0] / singular[-1]) if singular[-1] > 0.0 else None
    )
    return {
        "raw_sign": int(np.sign(raw_sign)),
        "raw_log_abs_determinant": (
            float(raw_log_abs) if np.isfinite(raw_log_abs) else None
        ),
        "sign": int(np.sign(sign)),
        "normalized_sign": int(np.sign(sign)),
        "log_abs_normalized_determinant": finite_log_abs,
        "column_norms": column_norms,
        "normalized_singular_values": singular,
        "normalized_sigma_min": float(singular[-1]),
        "normalized_condition_number": finite_condition,
        "singular_or_underflowed_determinant": bool(
            int(np.sign(sign)) == 0 or finite_log_abs is None
        ),
    }


def run_endpoint_sweep(
    manifest: Mapping[str, Any],
    context: CheckpointContext,
    tiers: Mapping[str, TierSpec],
    ledger: SlotLedger,
) -> tuple[MapEvaluator, dict[str, Any]]:
    evaluator = MapEvaluator(context, tiers, ledger)
    specs = endpoint_specifications(manifest)
    center_kinds = (
        ("production_state", "affine"),
        ("tight_state", "affine"),
        ("tight_state", "geodesic_u2"),
        ("radau_state", "affine"),
        ("radau_state", "geodesic_u2"),
    )
    d2_vectors: dict[tuple[str, str, str, int, float], np.ndarray] = {}
    per_point: dict[str, Any] = {}
    for label in TARGETS:
        progress(f"endpoint sweep: {label}")
        point = context.points[label]
        center_residuals: dict[tuple[str, str], np.ndarray | None] = {}
        for tier, chart_kind in center_kinds:
            key = center_slot_key(label, tier, chart_kind)
            center_residuals[(tier, chart_kind)] = evaluator.evaluate_slot(
                key,
                point,
                tier,
                chart_kind,
                point.parameters.copy(),
            )
        point_d2_success = 0
        point_d2_failed = 0
        for (tier, chart_kind, column), steps in specs.items():
            f0 = center_residuals[(tier, chart_kind)]
            for step in steps:
                endpoint_values: dict[int, np.ndarray | None] = {}
                for sign in (-1, 1):
                    parameters = point.parameters.copy()
                    parameters[column] += sign * step
                    key = endpoint_slot_key(
                        label, tier, chart_kind, column, step, sign
                    )
                    endpoint_values[sign] = evaluator.evaluate_slot(
                        key, point, tier, chart_kind, parameters
                    )
                d2_key = d2_slot_key(label, tier, chart_kind, column, step)
                plus = endpoint_values[1]
                minus = endpoint_values[-1]
                if f0 is None or plus is None or minus is None:
                    ledger.finish(
                        d2_key,
                        "EVALUATION_FAILED",
                        error="center or one declared signed endpoint failed",
                    )
                    point_d2_failed += 1
                    continue
                try:
                    with np.errstate(over="raise", invalid="raise", divide="raise"):
                        d2 = (plus - minus) / (2.0 * step)
                        d_plus = (plus - f0) / step
                        d_minus = (f0 - minus) / step
                        difference_norm = float(
                            np.linalg.norm(d_plus - d_minus)
                        )
                        plus_norm = float(np.linalg.norm(d_plus))
                        minus_norm = float(np.linalg.norm(d_minus))
                        asymmetry = difference_norm / max(
                            plus_norm, minus_norm, 1.0e-30
                        )
                        second = plus + minus - 2.0 * f0
                        second_norm = float(np.linalg.norm(second))
                        second_scaled = second_norm / (step * step)
                    arrays = (d2, d_plus, d_minus, second)
                    scalars = (
                        difference_norm,
                        plus_norm,
                        minus_norm,
                        asymmetry,
                        second_norm,
                        second_scaled,
                    )
                    if any(not np.all(np.isfinite(value)) for value in arrays):
                        raise SlotEvaluationError(
                            "nonfinite vector in centered D2 derivation"
                        )
                    if any(not math.isfinite(value) for value in scalars):
                        raise SlotEvaluationError(
                            "nonfinite scalar in centered D2 diagnostics"
                        )
                    payload = {
                        "vector": d2,
                        "plus_endpoint_key": endpoint_slot_key(
                            label, tier, chart_kind, column, step, 1
                        ),
                        "minus_endpoint_key": endpoint_slot_key(
                            label, tier, chart_kind, column, step, -1
                        ),
                        "center_key": center_slot_key(label, tier, chart_kind),
                        "forward_derivative": d_plus,
                        "backward_derivative": d_minus,
                        "forward_backward_asymmetry": asymmetry,
                        "second_symmetric_residual": second_norm,
                        "second_symmetric_scaled": second_scaled,
                    }
                    ledger.finish(d2_key, "SUCCESS", payload=payload)
                    d2_vectors[(label, tier, chart_kind, column, step)] = d2
                    point_d2_success += 1
                except InvalidRun:
                    raise
                except Exception as exc:
                    ledger.finish(
                        d2_key,
                        "EVALUATION_FAILED",
                        payload={
                            "plus_endpoint_key": endpoint_slot_key(
                                label, tier, chart_kind, column, step, 1
                            ),
                            "minus_endpoint_key": endpoint_slot_key(
                                label, tier, chart_kind, column, step, -1
                            ),
                            "center_key": center_slot_key(
                                label, tier, chart_kind
                            ),
                            "h": step,
                            "column": column,
                            "finite_validation_passed": False,
                        },
                        error=f"{type(exc).__name__}: {exc}",
                    )
                    point_d2_failed += 1
        per_point[label] = {
            "D2_success": point_d2_success,
            "D2_failed": point_d2_failed,
        }
    return evaluator, {
        "D2_vectors": d2_vectors,
        "per_point": per_point,
        "endpoint_success_count": sum(
            slot["terminal_status"] == "SUCCESS"
            for slot in ledger.slots.values()
            if slot["metadata"].get("slot_kind") == "endpoint"
        ),
        "endpoint_failed_count": sum(
            slot["terminal_status"] == "EVALUATION_FAILED"
            for slot in ledger.slots.values()
            if slot["metadata"].get("slot_kind") == "endpoint"
        ),
    }


def get_d2(
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
    point: str,
    tier: str,
    chart_kind: str,
    column: int,
    step: float,
) -> np.ndarray | None:
    return d2_vectors.get((point, tier, chart_kind, column, float(step)))


def richardson_from_d2(
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
    point: str,
    tier: str,
    chart_kind: str,
    column: int,
    step: float,
) -> np.ndarray | None:
    coarse = get_d2(d2_vectors, point, tier, chart_kind, column, step)
    half = get_d2(d2_vectors, point, tier, chart_kind, column, step / 2.0)
    if coarse is None or half is None:
        return None
    try:
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            result = (4.0 * half - coarse) / 3.0
        if not np.all(np.isfinite(result)):
            return None
        return result
    except (ArithmeticError, FloatingPointError):
        return None


def fixed_r4_references(
    context: CheckpointContext,
    ledger: SlotLedger,
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
) -> tuple[dict[str, dict[int, dict[str, np.ndarray]]], dict[str, Any]]:
    steps = {"coarse": 4.0e-4, "primary": 2.0e-4, "fine": 1.0e-4}
    references: dict[str, dict[int, dict[str, np.ndarray]]] = {}
    point_details: dict[str, Any] = {}
    for label in TARGETS:
        references[label] = {}
        failed: list[dict[str, Any]] = []
        for column in range(14):
            references[label][column] = {}
            for name, step in steps.items():
                slot_key = f"R4|{label}|tight_state|affine|col={column}|{name}"
                value = richardson_from_d2(
                    d2_vectors,
                    label,
                    "tight_state",
                    "affine",
                    column,
                    step,
                )
                if value is None:
                    ledger.finish(
                        slot_key,
                        "EVALUATION_FAILED",
                        payload={
                            "h": step,
                            "column": column,
                            "reference": name,
                            "finite_validation_passed": False,
                        },
                        error=(
                            "one required D2 is unavailable or the fixed R4 "
                            "derivation overflowed/became nonfinite"
                        ),
                    )
                    failed.append({"column": column, "reference": name})
                    continue
                references[label][column][name] = value
                ledger.finish(
                    slot_key,
                    "SUCCESS",
                    payload={
                        "vector": value,
                        "h": step,
                        "D2_h": d2_slot_key(
                            label, "tight_state", "affine", column, step
                        ),
                        "D2_half": d2_slot_key(
                            label, "tight_state", "affine", column, step / 2.0
                        ),
                    },
                )
        point_details[label] = {"failed_references": failed}
    return references, point_details


def run_augmented_and_three_way(
    context: CheckpointContext,
    tiers: Mapping[str, TierSpec],
    ledger: SlotLedger,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    augmented: dict[str, dict[str, Any]] = {}
    details: dict[str, Any] = {}
    for label in TARGETS:
        progress(f"augmented maps: {label}")
        point = context.points[label]
        production_key = f"augmented|{label}|production_augmented"
        tight_key = f"augmented|{label}|tight_augmented"
        production: dict[str, Any] | None = None
        tight: AugmentedEvaluation | None = None
        try:
            production = integrate_production_augmented(context, point)
            ledger.finish(
                production_key,
                "SUCCESS",
                payload={**production, "terminal_status": "SUCCESS"},
            )
        except InvalidRun:
            raise
        except Exception as exc:
            ledger.finish(
                production_key,
                "EVALUATION_FAILED",
                payload={
                    "parameters": point.parameters,
                    "bounds_margins": parameter_margins(
                        context.phase41, point.parameters
                    ),
                    "tier": dataclasses.asdict(tiers["production_augmented"]),
                    "fallback_used": False,
                    "no_fallback_method_used": True,
                    "terminal_status": "EVALUATION_FAILED",
                    "available_exception_payload": (
                        exc.payload if isinstance(exc, SlotEvaluationError) else {}
                    ),
                },
                error=f"{type(exc).__name__}: {exc}",
            )
        try:
            tight = integrate_tight_augmented(
                context,
                point,
                tiers["tight_augmented"],
                (0.0, 0.25, 0.5, 0.75, 1.0),
            )
            ledger.finish(
                tight_key,
                "SUCCESS",
                payload={
                    **dataclasses.asdict(tight),
                    "parameters": point.parameters,
                    "bounds_margins": parameter_margins(
                        context.phase41, point.parameters
                    ),
                    "tier": dataclasses.asdict(tiers["tight_augmented"]),
                    "fallback_used": False,
                    "no_fallback_method_used": True,
                    "terminal_status": "SUCCESS",
                },
            )
        except InvalidRun:
            raise
        except Exception as exc:
            ledger.finish(
                tight_key,
                "EVALUATION_FAILED",
                payload={
                    "parameters": point.parameters,
                    "bounds_margins": parameter_margins(
                        context.phase41, point.parameters
                    ),
                    "tier": dataclasses.asdict(tiers["tight_augmented"]),
                    "fallback_used": False,
                    "no_fallback_method_used": True,
                    "terminal_status": "EVALUATION_FAILED",
                    "available_exception_payload": (
                        exc.payload if isinstance(exc, SlotEvaluationError) else {}
                    ),
                },
                error=f"{type(exc).__name__}: {exc}",
            )
        matrix_key = f"matrix|{label}|three_way_J"
        if production is None:
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                payload={
                    "production_drift_passed": False,
                    "tight_scientific_completion": (
                        "COMPLETE" if tight is not None else "INCOMPLETE"
                    ),
                },
                error="unchanged production augmented map unavailable",
            )
            augmented[label] = {"production": production, "tight": tight}
            details[label] = {
                "complete": False,
                "production_drift_passed": False,
                "tight_scientific_completion": (
                    "COMPLETE" if tight is not None else "INCOMPLETE"
                ),
            }
            continue
        target = point.checkpoint_target
        post = target["post_solve_strict_DOP853_reevaluation"]
        baselines = {
            "residual": decode_array_record(
                post["scaled_residual_interleaved"],
                path=f"$.targets.{label}.post.scaled_residual",
            ),
            "gamma_state_z": decode_array_record(
                post["gamma_state_z"], path=f"$.targets.{label}.post.gamma_state"
            ),
            "k_state_z": decode_array_record(
                post["k_state_z"], path=f"$.targets.{label}.post.k_state"
            ),
            "gamma_frame_z": decode_array_record(
                post["gamma_frame_z"], path=f"$.targets.{label}.post.gamma_frame"
            ),
            "k_frame_z": decode_array_record(
                post["k_frame_z"], path=f"$.targets.{label}.post.k_frame"
            ),
            "jacobian": point.checkpoint_jacobian,
        }
        production_errors = {
            name: float(np.max(np.abs(np.asarray(production[name]) - expected)))
            for name, expected in baselines.items()
        }
        production_drift_passed = max(production_errors.values()) <= 5.0e-11
        checkpoint_j = point.checkpoint_jacobian
        production_j = np.asarray(production["jacobian"], dtype=float)
        if tight is None:
            payload = {
                "complete": False,
                "production_checkpoint_field_max_abs": production_errors,
                "production_drift_passed": production_drift_passed,
                "checkpoint_J": checkpoint_j,
                "production_J": production_j,
                "tight_J": None,
                "tight_scientific_completion": "INCOMPLETE",
            }
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                payload=payload,
                error="tight augmented map unavailable; production drift gate retained",
            )
            augmented[label] = {"production": production, "tight": tight}
            details[label] = payload
            continue
        tight_j = tight.jacobian
        comparisons = {
            "checkpoint_to_production_max_abs": production_errors["jacobian"],
            "checkpoint_to_tight_relative_operator": operator_rel(
                checkpoint_j, tight_j
            ),
            "production_to_tight_relative_operator": operator_rel(
                production_j, tight_j
            ),
            "checkpoint_to_tight_per_column": [
                vector_rel(checkpoint_j[:, j], tight_j[:, j]) for j in range(14)
            ],
            "production_to_tight_per_column": [
                vector_rel(production_j[:, j], tight_j[:, j]) for j in range(14)
            ],
            "checkpoint_minus_production_J": checkpoint_j - production_j,
            "checkpoint_minus_tight_J": checkpoint_j - tight_j,
            "production_minus_tight_J": production_j - tight_j,
        }
        tight_threshold_passed = bool(
            comparisons["checkpoint_to_tight_relative_operator"] <= 0.005
            and comparisons["production_to_tight_relative_operator"] <= 0.005
            and max(comparisons["checkpoint_to_tight_per_column"]) <= 0.005
            and max(comparisons["production_to_tight_per_column"]) <= 0.005
        )
        try:
            summaries = {
                "checkpoint": matrix_summary(checkpoint_j),
                "production": matrix_summary(production_j),
                "tight": matrix_summary(tight_j),
            }
        except Exception as exc:
            if isinstance(exc, InvalidRun):
                raise
            error = f"{type(exc).__name__}: {exc}"
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                payload={
                    "production_checkpoint_field_max_abs": production_errors,
                    "production_drift_passed": production_drift_passed,
                    "tight_scientific_completion": "INCONCLUSIVE",
                    "comparisons": comparisons,
                },
                error=error,
            )
            augmented[label] = {"production": production, "tight": tight}
            details[label] = {
                "complete": False,
                "production_drift_passed": production_drift_passed,
                "production_checkpoint_field_max_abs": production_errors,
                "tight_scientific_error": error,
            }
            continue
        payload = {
            "complete": True,
            "production_checkpoint_field_max_abs": production_errors,
            "production_drift_passed": production_drift_passed,
            "checkpoint_J": checkpoint_j,
            "production_J": production_j,
            "tight_J": tight_j,
            "comparisons": comparisons,
            "tight_scientific_threshold_passed": tight_threshold_passed,
            "matrix_summaries": summaries,
            "tight_time_column_is_assembly_only": True,
        }
        ledger.finish(matrix_key, "SUCCESS", payload=payload)
        augmented[label] = {"production": production, "tight": tight}
        details[label] = payload
    return augmented, details


def phase41_negative_control(
    manifest: Mapping[str, Any],
    context: CheckpointContext,
    ledger: SlotLedger,
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
    augmented: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    ladders = {
        int(column): tuple(float(h) for h in values)
        for column, values in manifest["finite_difference_protocol"][
            "phase41_production_negative_control_steps_by_zero_based_column"
        ].items()
    }
    disclosed = manifest["known_before_freeze"]["audited_points"]
    point_details: dict[str, Any] = {}
    all_reproduced = True
    for label in TARGETS:
        matrix_key = f"matrix|{label}|phase41_negative_control"
        production = augmented.get(label, {}).get("production")
        chosen: list[np.ndarray] = []
        per_column: list[dict[str, Any]] = []
        incomplete = False
        for column in range(14):
            ladder = ladders[column]
            evaluations = [
                get_d2(
                    d2_vectors,
                    label,
                    "production_state",
                    "affine",
                    column,
                    step,
                )
                for step in ladder
            ]
            selected_index: int | None = None
            for index in range(len(ladder) - 1):
                if evaluations[index] is not None and evaluations[index + 1] is not None:
                    selected_index = index
                    break
            if selected_index is None:
                incomplete = True
                per_column.append(
                    {
                        "column": column,
                        "complete": False,
                        "declared_steps": ladder,
                    }
                )
                continue
            first = evaluations[selected_index]
            second = evaluations[selected_index + 1]
            assert first is not None and second is not None
            plateau = float(
                np.linalg.norm(first - second)
                / max(np.linalg.norm(first), 1.0e-30)
            )
            chosen.append(first)
            per_column.append(
                {
                    "column": column,
                    "complete": True,
                    "declared_steps": ladder,
                    "selected_adjacent_indices": [selected_index, selected_index + 1],
                    "chosen_steps": [
                        ladder[selected_index],
                        ladder[selected_index + 1],
                    ],
                    "plateau_relative_difference_phase41_asymmetric": plateau,
                }
            )
        if incomplete or production is None or len(chosen) != 14:
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                error="old Phase41 FD matrix is incomplete",
            )
            point_details[label] = {"complete": False, "per_column": per_column}
            all_reproduced = False
            continue
        matrix = np.column_stack(chosen)
        production_j = np.asarray(production["jacobian"], dtype=float)
        op_error = float(
            np.linalg.norm(matrix - production_j, ord=2)
            / max(np.linalg.norm(production_j, ord=2), 1.0e-30)
        )
        orientation = context.phase41.matrix_orientation(matrix)
        failed_columns = [
            record["column"]
            for record in per_column
            if record["plateau_relative_difference_phase41_asymmetric"] >= 0.02
        ]
        u2_plateau = float(
            per_column[8]["plateau_relative_difference_phase41_asymmetric"]
        )
        known = disclosed[label]
        metric_errors = {
            "operator_absolute": abs(
                op_error
                - float(known["phase41_FD_to_variational_relative_operator_error"])
            ),
            "u2_plateau_absolute": abs(
                u2_plateau - float(known["phase41_u2_adjacent_step_relative_change"])
            ),
        }
        reproduced = bool(
            orientation["sign"] == int(known["phase41_FD_root_sign"]) == -1
            and failed_columns == [8]
            and per_column[8]["chosen_steps"] == [2.0e-6, 5.0e-7]
            and max(metric_errors.values()) <= 5.0e-6
        )
        all_reproduced = all_reproduced and reproduced
        payload = {
            "complete": True,
            "status": "TANGENT_CONTROL_FAILED",
            "historical_status_unchanged": True,
            "finite_difference_matrix": matrix,
            "matrix_orientation": orientation,
            "FD_to_production_variational_relative_operator_error": op_error,
            "failed_plateau_columns": failed_columns,
            "u2_plateau": u2_plateau,
            "per_column": per_column,
            "disclosed_metric_absolute_errors": metric_errors,
            "faithful_reproduction_passed": reproduced,
        }
        ledger.finish(matrix_key, "SUCCESS", payload=payload)
        point_details[label] = payload
    return {
        "passed": all_reproduced,
        "historical_phase41_status": "TANGENT_CONTROL_FAILED",
        "phase41_remains_8_of_9": True,
        "points": point_details,
    }


def mp_affine_chart(
    center: np.ndarray, tangent: np.ndarray, parameters_u: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    with mpmath.workdps(80):
        c = mpmath.matrix([mpmath.mpf(repr(float(value))) for value in center])
        b = mpmath.matrix(
            [
                [mpmath.mpf(repr(float(value))) for value in row]
                for row in tangent
            ]
        )
        u = mpmath.matrix(
            [mpmath.mpf(repr(float(value))) for value in parameters_u]
        )
        r = c + b * u
        norm = mpmath.sqrt(sum(r[index] ** 2 for index in range(7)))
        omega = r / norm
        derivative = mpmath.matrix(7, 6)
        for row in range(7):
            for column in range(6):
                projection = sum(
                    omega[row] * omega[k] * b[k, column] for k in range(7)
                )
                derivative[row, column] = (b[row, column] - projection) / norm
        omega_float = np.array([float(omega[index]) for index in range(7)])
        derivative_float = np.array(
            [
                [float(derivative[row, column]) for column in range(6)]
                for row in range(7)
            ]
        )
        retained = {
            "omega_decimal_strings": [
                mpmath.nstr(omega[index], 82) for index in range(7)
            ],
            "domega_decimal_strings": [
                [mpmath.nstr(derivative[row, column], 82) for column in range(6)]
                for row in range(7)
            ],
        }
    return omega_float, derivative_float, retained


def mp_launch_tangent(
    launch: np.ndarray, derivative_decimal_strings: Sequence[Sequence[str]]
) -> tuple[np.ndarray, list[list[list[str]]]]:
    with mpmath.workdps(80):
        launch_mp = mpmath.matrix(
            [
                [
                    mpmath.mpc(
                        mpmath.mpf(repr(float(value.real))),
                        mpmath.mpf(repr(float(value.imag))),
                    )
                    for value in row
                ]
                for row in np.asarray(launch, dtype=np.complex128)
            ]
        )
        derivative_mp = mpmath.matrix(
            [[mpmath.mpf(value) for value in row] for row in derivative_decimal_strings]
        )
        result_mp = mpmath.mpf("0.0001") * launch_mp * derivative_mp
        result = np.empty((7, 6), dtype=np.complex128)
        retained: list[list[list[str]]] = []
        for row in range(7):
            retained_row: list[list[str]] = []
            for column in range(6):
                value = result_mp[row, column]
                result[row, column] = complex(float(value.real), float(value.imag))
                retained_row.append(
                    [mpmath.nstr(value.real, 82), mpmath.nstr(value.imag, 82)]
                )
            retained.append(retained_row)
    return result, retained


def chart_diagnostics(
    context: CheckpointContext,
    ledger: SlotLedger,
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
) -> dict[str, Any]:
    point_details: dict[str, Any] = {}
    all_complete = True
    all_algebra_passed = True
    for label in TARGETS:
        point = context.points[label]
        matrix_key = f"matrix|{label}|chart"
        try:
            omega, derivative = affine_chart_direction(
                context, point.parameters[7:13]
            )
            p41_omega, p41_derivative = context.chart.direction(
                point.parameters[7:13]
            )
            target_chart = point.checkpoint_target["chart_at_root"]
            checkpoint_omega = decode_array_record(
                target_chart["omega"], path=f"$.target.{label}.chart.omega"
            )
            checkpoint_derivative = decode_array_record(
                target_chart["direction_derivative"],
                path=f"$.target.{label}.chart.domega",
            )
            checkpoint_initial = decode_array_record(
                target_chart["initial_xi"],
                path=f"$.target.{label}.chart.initial_xi",
            )
            mp_omega, mp_derivative, mp_retained = mp_affine_chart(
                context.chart.center,
                context.chart.tangent,
                point.parameters[7:13],
            )
            launch = point.saddle.launch_matrix(1.0)
            initial = 1.0e-4 * (launch @ omega)
            launch_tangent = 1.0e-4 * (launch @ derivative)
            phase41_launch_tangent = 1.0e-4 * (launch @ p41_derivative)
            checkpoint_launch = decode_array_record(
                target_chart["launch_matrix"],
                path=f"$.target.{label}.chart.launch_matrix",
            )
            checkpoint_launch_tangent = (
                1.0e-4 * (checkpoint_launch @ checkpoint_derivative)
            )
            mp_launch_float, mp_launch_strings = mp_launch_tangent(
                launch, mp_retained["domega_decimal_strings"]
            )
            algebra = {
                "omega_norm_error": abs(float(np.linalg.norm(omega)) - 1.0),
                "omega_dot_domega_max_abs": float(
                    np.max(np.abs(omega @ derivative))
                ),
                "to_phase41_omega_max_abs": float(
                    np.max(np.abs(omega - p41_omega))
                ),
                "to_phase41_domega_max_abs": float(
                    np.max(np.abs(derivative - p41_derivative))
                ),
                "to_checkpoint_omega_max_abs": float(
                    np.max(np.abs(omega - checkpoint_omega))
                ),
                "to_checkpoint_domega_max_abs": float(
                    np.max(np.abs(derivative - checkpoint_derivative))
                ),
                "initial_xi_to_checkpoint_max_abs": float(
                    np.max(np.abs(initial - checkpoint_initial))
                ),
                "double_to_80dps_omega_relative": vector_rel(omega, mp_omega),
                "double_to_80dps_domega_operator_relative": operator_rel(
                    derivative, mp_derivative
                ),
                "launch_tangent_to_phase41_max_abs": float(
                    np.max(np.abs(launch_tangent - phase41_launch_tangent))
                ),
                "launch_tangent_to_checkpoint_max_abs": float(
                    np.max(np.abs(launch_tangent - checkpoint_launch_tangent))
                ),
                "launch_tangent_to_80dps_max_abs": float(
                    np.max(np.abs(launch_tangent - mp_launch_float))
                ),
            }
            base_geo, geo_derivative = geodesic_u2_direction(
                context, point, point.parameters[7:13]
            )
            same_base_error = float(np.max(np.abs(base_geo - omega)))
            same_tangent_error = float(
                np.max(np.abs(geo_derivative[:, 1] - derivative[:, 1]))
            )
            r4_values = {
                "affine_production": richardson_from_d2(
                    d2_vectors, label, "production_state", "affine", 8, 2e-4
                ),
                "affine_tight": richardson_from_d2(
                    d2_vectors, label, "tight_state", "affine", 8, 2e-4
                ),
                "affine_radau": richardson_from_d2(
                    d2_vectors, label, "radau_state", "affine", 8, 2e-4
                ),
                "geodesic_tight": richardson_from_d2(
                    d2_vectors,
                    label,
                    "tight_state",
                    "geodesic_u2",
                    8,
                    2e-4,
                ),
                "geodesic_radau": richardson_from_d2(
                    d2_vectors,
                    label,
                    "radau_state",
                    "geodesic_u2",
                    8,
                    2e-4,
                ),
            }
            curvature_complete = all(value is not None for value in r4_values.values())
            if curvature_complete:
                r = {key: np.asarray(value) for key, value in r4_values.items()}
                e_chart = max(
                    vector_rel(r["affine_production"], r["affine_tight"]),
                    vector_rel(r["affine_tight"], r["affine_radau"]),
                    vector_rel(r["geodesic_tight"], r["geodesic_radau"]),
                )
                curvature = {
                    "R4": r,
                    "E_chart": e_chart,
                    "affine_to_geodesic_tight": vector_rel(
                        r["affine_tight"], r["geodesic_tight"]
                    ),
                }
            else:
                curvature = {
                    "R4": {
                        key: value for key, value in r4_values.items()
                    },
                    "E_chart": None,
                    "affine_to_geodesic_tight": None,
                }
            algebra_passed = bool(
                max(algebra.values()) <= 1.0e-11
                and same_base_error <= 1.0e-11
                and same_tangent_error <= 1.0e-11
            )
            complete = bool(curvature_complete)
            payload = {
                "complete": complete,
                "algebra_passed": algebra_passed,
                "affine_double": {"omega": omega, "domega_du": derivative},
                "affine_80_decimal": {
                    "omega": mp_omega,
                    "domega_du": mp_derivative,
                    **mp_retained,
                    "binary64_import": "exact decimal round-trip repr",
                    "decimal_precision": 80,
                },
                "initial_launch_tangent": {
                    "double": launch_tangent,
                    "phase41_derived": phase41_launch_tangent,
                    "checkpoint_derived": checkpoint_launch_tangent,
                    "80_decimal_float_projection": mp_launch_float,
                    "80_decimal_complex_strings": mp_launch_strings,
                },
                "algebra_errors": algebra,
                "geodesic_same_base_error": same_base_error,
                "geodesic_same_first_tangent_error": same_tangent_error,
                "curvature_fixed_h_0.0002": curvature,
            }
            ledger.finish(matrix_key, "SUCCESS", payload=payload)
            point_details[label] = payload
            all_complete = all_complete and complete
            all_algebra_passed = all_algebra_passed and algebra_passed
        except InvalidRun:
            raise
        except Exception as exc:
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                error=f"{type(exc).__name__}: {exc}",
            )
            point_details[label] = {
                "complete": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
            all_complete = False
            all_algebra_passed = False
    return {
        "passed": bool(all_complete and all_algebra_passed),
        "complete": all_complete,
        "algebra_passed": all_algebra_passed,
        "points": point_details,
    }


def local_rhs_diagnostics(
    context: CheckpointContext,
    tiers: Mapping[str, TierSpec],
    ledger: SlotLedger,
    evaluator: MapEvaluator,
    augmented: Mapping[str, Mapping[str, Any]],
    references: Mapping[str, Mapping[int, Mapping[str, np.ndarray]]],
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
) -> dict[str, Any]:
    point_details: dict[str, Any] = {}
    all_complete = True
    any_stable_violation = False
    all_passed = True
    for label in TARGETS:
        point = context.points[label]
        tight = augmented.get(label, {}).get("tight")
        production = augmented.get(label, {}).get("production")
        direction_records: list[dict[str, Any]] = []
        point_complete = tight is not None and production is not None
        point_stable_violation = False
        if tight is not None:
            for fraction_index, fraction in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
                xi = tight.fraction_xi[fraction_index]
                for direction in range(6):
                    local_key = (
                        f"local_RHS|{label}|fraction={format(fraction,'.2g')}|"
                        f"direction={direction}"
                    )
                    q = tight.fraction_tangents[fraction_index, :, direction]
                    q_norm = float(np.linalg.norm(q))
                    try:
                        if not math.isfinite(q_norm) or q_norm <= 0.0:
                            raise SlotEvaluationError("transported tangent vanished")
                        q_hat = q / q_norm
                        analytic = -np.conjugate(
                            context.phase41.hessian_xi(
                                point.model, point.saddle, context.fixed, xi
                            )
                            @ q
                        )
                        local_d2: dict[float, np.ndarray] = {}
                        for epsilon in (2.0e-5, 1.0e-5, 5.0e-6):
                            signed: dict[int, np.ndarray] = {}
                            for sign in (-1, 1):
                                perturb_key = (
                                    f"{local_key}|epsilon={format(epsilon,'.17g')}|"
                                    f"{'plus' if sign > 0 else 'minus'}"
                                )
                                try:
                                    value = context.phase41.flow_xi(
                                        point.model,
                                        point.saddle,
                                        context.fixed,
                                        xi + sign * epsilon * q_hat,
                                    )
                                    if not np.all(np.isfinite(value)):
                                        raise SlotEvaluationError(
                                            "nonfinite local flow evaluation"
                                        )
                                    ledger.finish(
                                        perturb_key,
                                        "SUCCESS",
                                        payload={
                                            "xi": xi + sign * epsilon * q_hat,
                                            "flow_xi": value,
                                        },
                                    )
                                    signed[sign] = value
                                except InvalidRun:
                                    raise
                                except Exception as exc:
                                    ledger.finish(
                                        perturb_key,
                                        "EVALUATION_FAILED",
                                        error=f"{type(exc).__name__}: {exc}",
                                    )
                            if set(signed) == {-1, 1}:
                                local_d2[epsilon] = (
                                    signed[1] - signed[-1]
                                ) / (2.0 * epsilon)
                        if set(local_d2) != {2.0e-5, 1.0e-5, 5.0e-6}:
                            raise SlotEvaluationError(
                                "local perturbation ladder is incomplete"
                            )
                        neighbor = q_norm * (
                            4.0 * local_d2[1.0e-5] - local_d2[2.0e-5]
                        ) / 3.0
                        fixed = q_norm * (
                            4.0 * local_d2[5.0e-6] - local_d2[1.0e-5]
                        ) / 3.0
                        stability = vector_rel(fixed, neighbor)
                        error = vector_rel(fixed, analytic)
                        stable = stability <= 1.0e-6
                        violation = bool(stable and error > 1.0e-7)
                        payload = {
                            "complete": True,
                            "fraction": fraction,
                            "direction": direction,
                            "q": q,
                            "q_norm": q_norm,
                            "analytic_hessian_action": analytic,
                            "D2": local_d2,
                            "R4_fixed_1e-5": fixed,
                            "R4_neighbor_2e-5": neighbor,
                            "neighbor_symmetric_relative": stability,
                            "fixed_to_analytic_symmetric_relative": error,
                            "stable": stable,
                            "stable_violation": violation,
                        }
                        ledger.finish(local_key, "SUCCESS", payload=payload)
                        direction_records.append(payload)
                        point_stable_violation = point_stable_violation or violation
                    except InvalidRun:
                        raise
                    except Exception as exc:
                        if ledger.slots[local_key]["terminal_status"] is None:
                            ledger.finish(
                                local_key,
                                "EVALUATION_FAILED",
                                error=f"{type(exc).__name__}: {exc}",
                            )
                        point_complete = False
        else:
            point_complete = False
        # Any unattempted local perturbation caused by an upstream augmented
        # failure is explicitly terminal rather than silently absent.
        for key, slot in ledger.slots.items():
            if (
                slot["metadata"].get("point") == label
                and slot["metadata"].get("slot_kind")
                in {"local_RHS_direction", "local_RHS_perturbation"}
                and slot["terminal_status"] is None
            ):
                ledger.finish(
                    key,
                    "NOT_RUN_UPSTREAM_INVALID",
                    error="tight augmented trajectory unavailable",
                )

        time_payload: dict[str, Any] = {}
        time_controls_complete = True
        try:
            flows = {
                name: evaluator.k_cache[
                    MapEvaluator.cache_key(
                        point, tiers[name], "affine", point.parameters
                    )
                ]
                for name in ("production_state", "tight_state", "radau_state")
            }
            positive_by_tier: dict[str, np.ndarray] = {}
            negative_by_tier: dict[str, np.ndarray] = {}
            for name, flow in flows.items():
                positive = (
                    np.diag(context.coordinate_scales)
                    @ context.fixed.linear_map
                    @ context.phase41.flow_xi(
                        point.model, point.saddle, context.fixed, flow.xi
                    )
                )
                positive_by_tier[name] = positive
                negative_by_tier[name] = -context.row_scales * (
                    context.phase41.interleaved(positive)
                )
            endpoint_rhs_cross_tier = {
                "production_to_tight": vector_rel(
                    negative_by_tier["production_state"],
                    negative_by_tier["tight_state"],
                ),
                "tight_to_Radau": vector_rel(
                    negative_by_tier["tight_state"],
                    negative_by_tier["radau_state"],
                ),
                "production_to_Radau": vector_rel(
                    negative_by_tier["production_state"],
                    negative_by_tier["radau_state"],
                ),
            }
            endpoint_rhs_cross_tier_envelope = max(
                endpoint_rhs_cross_tier.values()
            )
            direct_time_reference_stable = bool(
                endpoint_rhs_cross_tier_envelope <= 0.005
            )
            positive_key = f"time_control|{label}|positive_K_time_tangent"
            ledger.finish(
                positive_key,
                "SUCCESS",
                payload={
                    "source": "three independently integrated state-only center endpoint RHS values",
                    "positive_complex_z_tangent_by_tier": positive_by_tier,
                    "negative_scaled_root_column_by_tier": negative_by_tier,
                    "endpoint_RHS_cross_tier_symmetric_relative": endpoint_rhs_cross_tier,
                    "endpoint_RHS_cross_tier_envelope": endpoint_rhs_cross_tier_envelope,
                    "frozen_cross_tier_threshold": 0.005,
                    "direct_time_reference_stable": direct_time_reference_stable,
                    "tier_matched_endpoint_rule": True,
                },
            )
            comparisons: dict[str, Any] = {}
            for name, column, reference in (
                (
                    "checkpoint_negative_time_column",
                    point.checkpoint_jacobian[:, 13],
                    negative_by_tier["production_state"],
                ),
                (
                    "production_negative_time_column",
                    np.asarray(production["jacobian"])[:, 13]
                    if production is not None
                    else None,
                    negative_by_tier["production_state"],
                ),
            ):
                key = f"time_control|{label}|{name}"
                if column is None:
                    ledger.finish(
                        key,
                        "EVALUATION_FAILED",
                        error="comparison column unavailable",
                    )
                    point_complete = False
                    time_controls_complete = False
                else:
                    metric = vector_rel(np.asarray(column), reference)
                    passed = metric <= 1.0e-8
                    ledger.finish(
                        key,
                        "SUCCESS",
                        payload={
                            "column": column,
                            "tier_matched_independent_negative_scaled": reference,
                            "endpoint_tier": "production_state",
                            "symmetric_relative": metric,
                            "passed": passed,
                            "endpoint_RHS_cross_tier_envelope": endpoint_rhs_cross_tier_envelope,
                            "frozen_cross_tier_threshold": 0.005,
                            "reference_stable": direct_time_reference_stable,
                            "stable_violation": bool(
                                direct_time_reference_stable and not passed
                            ),
                        },
                    )
                    comparisons[name] = metric
                    point_stable_violation = point_stable_violation or bool(
                        direct_time_reference_stable and not passed
                    )
            fixed_time = references.get(label, {}).get(13, {})
            primary = fixed_time.get("primary")
            coarse = fixed_time.get("coarse")
            fine = fixed_time.get("fine")
            radau = richardson_from_d2(
                d2_vectors, label, "radau_state", "affine", 13, 2.0e-4
            )
            state_key = f"time_control|{label}|state_only_R4_time_column"
            if any(value is None for value in (primary, coarse, fine, radau)):
                ledger.finish(
                    state_key,
                    "EVALUATION_FAILED",
                    error="state-only time R4 or neighbor unavailable",
                )
                point_complete = False
                time_controls_complete = False
            else:
                assert primary is not None and coarse is not None and fine is not None
                assert radau is not None
                stability = max(vector_rel(primary, coarse), vector_rel(primary, fine))
                cross = vector_rel(primary, radau)
                tight_identity = vector_rel(
                    primary, negative_by_tier["tight_state"]
                )
                radau_identity = vector_rel(
                    radau, negative_by_tier["radau_state"]
                )
                tangent_cross = vector_rel(
                    negative_by_tier["tight_state"],
                    negative_by_tier["radau_state"],
                )
                stable = bool(
                    stability <= 0.005
                    and cross <= 0.005
                    and tangent_cross <= 0.005
                )
                passed = bool(
                    stable
                    and tight_identity <= 1.0e-8
                    and radau_identity <= 1.0e-8
                )
                ledger.finish(
                    state_key,
                    "SUCCESS",
                    payload={
                        "tight_R4_primary": primary,
                        "tight_R4_coarse": coarse,
                        "tight_R4_fine": fine,
                        "radau_R4_primary": radau,
                        "neighbor_stability": stability,
                        "tight_to_radau": cross,
                        "tight_R4_to_tight_endpoint_RHS": tight_identity,
                        "radau_R4_to_radau_endpoint_RHS": radau_identity,
                        "tight_to_radau_endpoint_RHS": tangent_cross,
                        "stable": stable,
                        "passed": passed,
                    },
                )
                comparisons["state_only_R4_time_column"] = {
                    "tight_tier_matched": tight_identity,
                    "radau_tier_matched": radau_identity,
                    "cross_method_R4": cross,
                    "cross_method_endpoint_RHS": tangent_cross,
                }
                point_stable_violation = point_stable_violation or bool(
                    stable
                    and max(tight_identity, radau_identity) > 1.0e-8
                )
            time_payload = {
                "independent_positive_tangent_by_tier": positive_by_tier,
                "independent_negative_scaled_by_tier": negative_by_tier,
                "comparisons": comparisons,
                "endpoint_RHS_cross_tier_symmetric_relative": endpoint_rhs_cross_tier,
                "endpoint_RHS_cross_tier_envelope": endpoint_rhs_cross_tier_envelope,
                "frozen_cross_tier_threshold": 0.005,
                "direct_time_reference_stable": direct_time_reference_stable,
                "tight_appended_column_excluded_from_bug_evidence": True,
                "tier_matched_endpoint_rule": True,
            }
        except InvalidRun:
            raise
        except Exception as exc:
            for control in (
                "positive_K_time_tangent",
                "checkpoint_negative_time_column",
                "production_negative_time_column",
                "state_only_R4_time_column",
            ):
                key = f"time_control|{label}|{control}"
                if ledger.slots[key]["terminal_status"] is None:
                    ledger.finish(
                        key,
                        "EVALUATION_FAILED",
                        error=f"{type(exc).__name__}: {exc}",
                    )
            point_complete = False
            time_controls_complete = False
            time_payload = {"error": f"{type(exc).__name__}: {exc}"}

        if len(direction_records) != 30:
            point_complete = False
        stable_records = [record for record in direction_records if record["stable"]]
        local_slot_prefix = f"local_RHS|{label}|"
        local_evaluations_complete = bool(
            len(direction_records) == 30
            and all(
                slot["terminal_status"] == "SUCCESS"
                for key, slot in ledger.slots.items()
                if key.startswith(local_slot_prefix)
            )
        )
        time_keys = [
            f"time_control|{label}|{control}"
            for control in (
                "positive_K_time_tangent",
                "checkpoint_negative_time_column",
                "production_negative_time_column",
                "state_only_R4_time_column",
            )
        ]
        time_evaluations_complete = all(
            ledger.slots[key]["terminal_status"] == "SUCCESS" for key in time_keys
        )
        evaluation_complete = bool(
            local_evaluations_complete and time_evaluations_complete
        )
        all_reference_checks_stable = bool(
            len(stable_records) == 30
            and time_payload.get("direct_time_reference_stable") is True
            and time_evaluations_complete
            and isinstance(
                ledger.slots[
                    f"time_control|{label}|state_only_R4_time_column"
                ]["payload"],
                dict,
            )
            and ledger.slots[
                f"time_control|{label}|state_only_R4_time_column"
            ]["payload"].get("stable")
            is True
        )
        point_passed = bool(
            evaluation_complete
            and all_reference_checks_stable
            and not point_stable_violation
        )
        matrix_key = f"matrix|{label}|local_RHS"
        ledger.finish(
            matrix_key,
            "SUCCESS" if evaluation_complete else "EVALUATION_FAILED",
            payload={
                "complete": evaluation_complete,
                "passed": point_passed,
                "stable_violation": point_stable_violation,
                "evaluation_complete": evaluation_complete,
                "all_reference_checks_stable": all_reference_checks_stable,
                "direction_records": direction_records,
                "time_controls": time_payload,
                "time_controls_complete": time_controls_complete,
            },
            error=None if evaluation_complete else "local RHS/time evaluation ledger incomplete",
        )
        point_details[label] = {
            "complete": evaluation_complete,
            "passed": point_passed,
            "stable_violation": point_stable_violation,
            "evaluation_complete": evaluation_complete,
            "all_reference_checks_stable": all_reference_checks_stable,
            "direction_records": direction_records,
            "time_controls": time_payload,
            "time_controls_complete": time_controls_complete,
        }
        all_complete = all_complete and evaluation_complete
        any_stable_violation = any_stable_violation or point_stable_violation
        all_passed = all_passed and point_passed
    return {
        "passed": all_passed,
        "complete": all_complete,
        "any_stable_violation": any_stable_violation,
        "evidence_status": (
            "SUPPORTED"
            if any_stable_violation
            else "NOT_SUPPORTED"
            if all_passed
            else "INCONCLUSIVE"
        ),
        "points": point_details,
    }


def all_column_r4_diagnostics(
    context: CheckpointContext,
    ledger: SlotLedger,
    references: Mapping[str, Mapping[int, Mapping[str, np.ndarray]]],
    augmented: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    point_details: dict[str, Any] = {}
    r4_matrices: dict[str, np.ndarray] = {}
    aggregate_passed = True
    aggregate_complete = True
    for label in TARGETS:
        matrix_key = f"matrix|{label}|all_column_R4"
        tight = augmented.get(label, {}).get("tight")
        columns = references.get(label, {})
        if tight is None:
            ledger.finish(
                matrix_key,
                "EVALUATION_FAILED",
                error="tight variational matrix incomplete",
            )
            point_details[label] = {
                "complete": False,
                "passed": False,
                "per_column": [
                    {"column": index, "complete": False, "null_reason": "tight J unavailable"}
                    for index in range(14)
                ],
            }
            aggregate_complete = False
            aggregate_passed = False
            continue
        try:
            checkpoint_j = context.points[label].checkpoint_jacobian
            tight_j = tight.jacobian
            per_column: list[dict[str, Any]] = []
            point_passed = True
            for index in range(14):
                refs = columns.get(index, {})
                if set(refs) != {"coarse", "primary", "fine"}:
                    per_column.append(
                        {
                            "column": index,
                            "complete": False,
                            "passed": False,
                            "null_reason": "one fixed R4 reference is unavailable",
                        }
                    )
                    point_passed = False
                    continue
                neighbor = max(
                    vector_rel(refs["primary"], refs["coarse"]),
                    vector_rel(refs["primary"], refs["fine"]),
                )
                checkpoint_metrics = vector_direction_metrics(
                    refs["primary"], checkpoint_j[:, index]
                )
                tight_metrics = vector_direction_metrics(
                    refs["primary"], tight_j[:, index]
                )
                checks = []
                for metrics in (checkpoint_metrics, tight_metrics):
                    checks.append(
                        metrics["symmetric_relative"] <= 0.01
                        and metrics["signed_cosine"] > 0.0
                        and metrics["angle_sine"] <= 0.01
                        and metrics["abs_norm_ratio_minus_one"] <= 0.01
                    )
                passed = bool(neighbor <= 0.005 and all(checks))
                point_passed = point_passed and passed
                per_column.append(
                    {
                        "column": index,
                        "complete": True,
                        "primary": refs["primary"],
                        "coarse": refs["coarse"],
                        "fine": refs["fine"],
                        "neighbor_stability": neighbor,
                        "to_checkpoint": checkpoint_metrics,
                        "to_tight": tight_metrics,
                        "passed": passed,
                    }
                )
            complete = all(record.get("complete") is True for record in per_column)
            r4: np.ndarray | None = None
            full_metrics: dict[str, Any]
            if complete:
                r4 = np.column_stack(
                    [columns[index]["primary"] for index in range(14)]
                )
                full_metrics = {
                    "R4_to_checkpoint_symmetric_relative_operator": operator_rel(
                        r4, checkpoint_j
                    ),
                    "R4_to_tight_symmetric_relative_operator": operator_rel(
                        r4, tight_j
                    ),
                }
                point_passed = bool(
                    point_passed and max(full_metrics.values()) <= 0.01
                )
            else:
                full_metrics = {
                    "R4_to_checkpoint_symmetric_relative_operator": None,
                    "R4_to_tight_symmetric_relative_operator": None,
                    "null_reason": "full fourteen-column R4 matrix incomplete",
                }
            payload = {
                "complete": complete,
                "passed": bool(complete and point_passed),
                "J_R4": r4,
                "per_column": per_column,
                "full_operator_metrics": full_metrics,
                "matrix_summary": matrix_summary(r4) if r4 is not None else None,
            }
            ledger.finish(
                matrix_key,
                "SUCCESS" if complete else "EVALUATION_FAILED",
                payload=payload,
                error=None if complete else "one or more fixed R4 columns unavailable",
            )
            point_details[label] = payload
            if r4 is not None:
                r4_matrices[label] = r4
            aggregate_complete = aggregate_complete and complete
            aggregate_passed = aggregate_passed and bool(complete and point_passed)
        except InvalidRun:
            raise
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            ledger.finish(matrix_key, "EVALUATION_FAILED", error=error)
            point_details[label] = {
                "complete": False,
                "passed": False,
                "error": error,
            }
            aggregate_complete = False
            aggregate_passed = False
    return {
        "passed": aggregate_passed,
        "complete": aggregate_complete,
        "points": point_details,
    }, r4_matrices


def normalized_homotopy_diagnostics(
    context: CheckpointContext,
    ledger: SlotLedger,
    r4_matrices: Mapping[str, np.ndarray],
) -> dict[str, Any]:
    point_details: dict[str, Any] = {}
    all_certified = True
    all_complete = True
    machine_epsilon = float(np.finfo(float).eps)
    for label in TARGETS:
        matrix_key = f"matrix|{label}|homotopy"
        mutation_keys = {
            name: f"mutation|{label}|{name}"
            for name in (
                "positive_column_rescaling",
                "single_reference_column_flip",
                "no_sampled_t_used",
            )
        }
        try:
            j_v = context.points[label].checkpoint_jacobian
            j_r = r4_matrices[label]
            norms_v = np.linalg.norm(j_v, axis=0)
            norms_r = np.linalg.norm(j_r, axis=0)
            if (
                np.any(~np.isfinite(norms_v))
                or np.any(~np.isfinite(norms_r))
                or np.any(norms_v <= 0.0)
                or np.any(norms_r <= 0.0)
            ):
                raise SlotEvaluationError("zero/nonfinite homotopy column norm")
            a_v = j_v / norms_v
            a_r = j_r / norms_r
            delta = a_r - a_v
            e = np.linalg.solve(a_v, delta)
            eta = float(np.linalg.norm(e, ord=2))
            solve_residual = float(
                np.linalg.norm(a_v @ e - delta, ord=2)
                / max(np.linalg.norm(delta, ord=2), 1.0e-30)
            )
            condition = float(np.linalg.cond(a_v, p=2))
            rounding_budget = max(1.0e-8, 100.0 * machine_epsilon * condition)
            summary_v = matrix_summary(j_v)
            summary_r = matrix_summary(j_r)
            column_metrics = [
                vector_direction_metrics(j_r[:, index], j_v[:, index])
                for index in range(14)
            ]
            certified = bool(
                summary_v["sign"] != 0
                and summary_v["sign"] == summary_r["sign"]
                and eta < 1.0
                and 1.0 - eta > rounding_budget
                and solve_residual <= 1.0e-10
            )

            positive_scales = np.linspace(0.5, 2.0, 14)
            scaled_v = j_v @ np.diag(positive_scales)
            scaled_r = j_r @ np.diag(positive_scales[::-1])
            scaled_av = scaled_v / np.linalg.norm(scaled_v, axis=0)
            scaled_ar = scaled_r / np.linalg.norm(scaled_r, axis=0)
            scale_error = max(
                float(np.max(np.abs(scaled_av - a_v))),
                float(np.max(np.abs(scaled_ar - a_r))),
            )
            scale_passed = bool(
                scale_error <= 5.0e-14
                and matrix_summary(scaled_v)["sign"] == summary_v["sign"]
                and matrix_summary(scaled_r)["sign"] == summary_r["sign"]
            )
            ledger.finish(
                mutation_keys["positive_column_rescaling"],
                "SUCCESS",
                payload={
                    "positive_scales_V": positive_scales,
                    "positive_scales_R": positive_scales[::-1],
                    "normalized_matrix_max_abs_error": scale_error,
                    "signs_unchanged": scale_passed,
                    "passed": scale_passed,
                },
            )

            flipped_r = j_r.copy()
            flipped_r[:, 8] *= -1.0
            flipped_ar = flipped_r / np.linalg.norm(flipped_r, axis=0)
            flipped_e = np.linalg.solve(a_v, flipped_ar - a_v)
            flipped_eta = float(np.linalg.norm(flipped_e, ord=2))
            flipped_sign = matrix_summary(flipped_r)["sign"]
            flip_passed = bool(
                flipped_sign == -summary_r["sign"] and not (flipped_eta < 1.0)
            )
            ledger.finish(
                mutation_keys["single_reference_column_flip"],
                "SUCCESS",
                payload={
                    "flipped_column": 8,
                    "original_sign": summary_r["sign"],
                    "flipped_sign": flipped_sign,
                    "flipped_eta": flipped_eta,
                    "eta_certificate_passes": bool(flipped_eta < 1.0),
                    "passed": flip_passed,
                },
            )
            ledger.finish(
                mutation_keys["no_sampled_t_used"],
                "SUCCESS",
                payload={
                    "sampled_t_values": [],
                    "proof_uses_only_norm_bound_eta_less_than_one": True,
                    "passed": True,
                },
            )
            payload = {
                "complete": True,
                "certified": certified,
                "sufficient_only": True,
                "J_V": j_v,
                "J_R": j_r,
                "D_V_column_norms": norms_v,
                "D_R_column_norms": norms_r,
                "A_V": a_v,
                "A_R": a_r,
                "Delta": delta,
                "E": e,
                "eta": eta,
                "one_minus_eta": 1.0 - eta,
                "solve_backward_residual": solve_residual,
                "rounding_budget": rounding_budget,
                "condition_A_V": condition,
                "sigma_min_A_V": float(np.linalg.svd(a_v, compute_uv=False)[-1]),
                "sigma_min_A_R": float(np.linalg.svd(a_r, compute_uv=False)[-1]),
                "matrix_summary_V": summary_v,
                "matrix_summary_R": summary_r,
                "column_metrics": column_metrics,
                "mutation_controls_passed": bool(scale_passed and flip_passed),
                "no_sampled_t_used": True,
                "scope": "local normalized matrix homotopy only",
            }
            ledger.finish(matrix_key, "SUCCESS", payload=payload)
            point_details[label] = payload
            all_certified = all_certified and certified and scale_passed and flip_passed
        except InvalidRun:
            raise
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            if ledger.slots[matrix_key]["terminal_status"] is None:
                ledger.finish(matrix_key, "EVALUATION_FAILED", error=error)
            for key in mutation_keys.values():
                if ledger.slots[key]["terminal_status"] is None:
                    ledger.finish(key, "EVALUATION_FAILED", error=error)
            point_details[label] = {"complete": False, "certified": False, "error": error}
            all_complete = False
            all_certified = False
    return {
        "passed": bool(all_complete and all_certified),
        "complete": all_complete,
        "all_three_sufficient_certificates": all_certified,
        "eta_failure_interpreted_as_sign_change": False,
        "points": point_details,
    }


def q2_value(
    first: np.ndarray | None,
    second: np.ndarray | None,
    third: np.ndarray | None,
) -> tuple[float | None, str | None]:
    if first is None or second is None or third is None:
        return None, "one D2 value is unavailable"
    numerator = float(np.linalg.norm(first - second))
    denominator = float(np.linalg.norm(second - third))
    if (
        numerator <= 0.0
        or denominator <= 0.0
        or not math.isfinite(numerator)
        or not math.isfinite(denominator)
    ):
        return None, "zero or nonfinite q2 difference norm"
    # Subtract logarithms so a finite ratio is not spuriously rounded to
    # zero/overflow before the logarithm is evaluated.
    result = math.log2(numerator) - math.log2(denominator)
    if not math.isfinite(result):
        return None, "nonfinite q2 logarithm"
    return result, None


def u2_solver_diagnostics(
    manifest: Mapping[str, Any],
    ledger: SlotLedger,
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
    references: Mapping[str, Mapping[int, Mapping[str, np.ndarray]]],
) -> dict[str, Any]:
    protocol = manifest["finite_difference_protocol"]
    main = tuple(float(v) for v in protocol["phase42_all_fourteen_columns_main_ladder"])
    tail = tuple(float(v) for v in protocol["u2_additional_dyadic_tail"])
    old = tuple(
        float(v)
        for v in protocol["u2_exact_phase41_reproduction_steps_across_state_tiers"]
    )
    point_details: dict[str, Any] = {}
    all_complete = True
    for label in TARGETS:
        key = f"matrix|{label}|u2_disentanglement"
        required: list[tuple[str, str, float]] = []
        required.extend(("production_state", "affine", h) for h in (*main, *tail, *old))
        required.extend(("tight_state", "affine", h) for h in (*main, *tail, *old))
        required.extend(("tight_state", "geodesic_u2", h) for h in (*main, *tail, *old))
        required.extend(("radau_state", "affine", h) for h in (*main, *old))
        required.extend(("radau_state", "geodesic_u2", h) for h in (*main, *old))
        missing = [
            {"tier": tier, "chart": chart, "h": h}
            for tier, chart, h in required
            if get_d2(d2_vectors, label, tier, chart, 8, h) is None
        ]
        for h in main:
            if get_d2(d2_vectors, label, "radau_state", "affine", 13, h) is None:
                missing.append({"tier": "radau_state", "chart": "affine", "column": 13, "h": h})
        complete = not missing
        q2_records: dict[str, Any] = {}
        dyadic_chain = tuple(sorted(set((*main, *tail)), reverse=True))
        for h in dyadic_chain[:-2]:
            value, reason = q2_value(
                get_d2(d2_vectors, label, "tight_state", "affine", 8, h),
                get_d2(d2_vectors, label, "tight_state", "affine", 8, h / 2.0),
                get_d2(d2_vectors, label, "tight_state", "affine", 8, h / 4.0),
            )
            q2_records[format(h, ".17g")] = {"q2": value, "null_reason": reason}
        solver_envelopes: dict[str, Any] = {}
        all_u2_steps = sorted(set((*main, *tail, *old)), reverse=True)
        for h in all_u2_steps:
            production = get_d2(
                d2_vectors, label, "production_state", "affine", 8, h
            )
            tight = get_d2(d2_vectors, label, "tight_state", "affine", 8, h)
            radau = get_d2(d2_vectors, label, "radau_state", "affine", 8, h)
            if production is not None and tight is not None:
                production_tight = vector_rel(production, tight)
                tight_radau = (
                    vector_rel(tight, radau) if radau is not None else None
                )
                solver_envelopes[format(h, ".17g")] = {
                    "production_to_tight": production_tight,
                    "tight_to_Radau": tight_radau,
                    "envelope": max(
                        [production_tight]
                        + ([tight_radau] if tight_radau is not None else [])
                    ),
                    "Radau_omitted_reason": (
                        None
                        if radau is not None
                        else (
                            "Radau coverage intentionally excludes this dyadic-tail-only h"
                            if h not in set((*main, *old))
                            else "required Radau D2 evaluation is unavailable"
                        )
                    ),
                    "required_Radau_missing": bool(
                        radau is None and h in set((*main, *old))
                    ),
                }
            else:
                solver_envelopes[format(h, ".17g")] = {
                    "production_to_tight": None,
                    "tight_to_Radau": None,
                    "envelope": None,
                    "null_reason": "production or tight D2 unavailable",
                }
        triple_metrics: dict[str, Any] = {}
        for h in (4.0e-4, 2.0e-4):
            h_values = (h, h / 2.0, h / 4.0)
            envelopes = [
                solver_envelopes[format(value, ".17g")]["envelope"]
                for value in h_values
            ]
            d_values = [
                get_d2(d2_vectors, label, "tight_state", "affine", 8, value)
                for value in h_values
            ]
            if any(value is None for value in envelopes) or any(
                value is None for value in d_values
            ):
                triple_metrics[format(h, ".17g")] = {
                    "E_triple": None,
                    "C_triple": None,
                    "null_reason": "one fixed envelope or tight D2 is unavailable",
                }
            else:
                assert all(value is not None for value in d_values)
                triple_metrics[format(h, ".17g")] = {
                    "E_triple": max(float(value) for value in envelopes),
                    "C_triple": min(
                        vector_rel(d_values[0], d_values[1]),
                        vector_rel(d_values[1], d_values[2]),
                    ),
                    "fixed_h_values": h_values,
                }
        old_pair_metrics: dict[str, Any] = {}
        production_tight_errors: dict[str, Any] = {}
        for h in old:
            production = get_d2(
                d2_vectors, label, "production_state", "affine", 8, h
            )
            tight = get_d2(d2_vectors, label, "tight_state", "affine", 8, h)
            production_tight_errors[format(h, ".17g")] = (
                vector_rel(production, tight)
                if production is not None and tight is not None
                else None
            )
        for first, second in zip(old[:-1], old[1:]):
            first_record = solver_envelopes[format(first, ".17g")]
            second_record = solver_envelopes[format(second, ".17g")]
            p_first = get_d2(
                d2_vectors, label, "production_state", "affine", 8, first
            )
            p_second = get_d2(
                d2_vectors, label, "production_state", "affine", 8, second
            )
            key_pair = f"{format(first,'.17g')}->{format(second,'.17g')}"
            if (
                first_record["envelope"] is None
                or second_record["envelope"] is None
                or p_first is None
                or p_second is None
            ):
                old_pair_metrics[key_pair] = {
                    "E_pair": None,
                    "C_pair": None,
                    "null_reason": "one old-step envelope or production D2 unavailable",
                }
            else:
                old_pair_metrics[key_pair] = {
                    "E_pair": max(
                        float(first_record["envelope"]),
                        float(second_record["envelope"]),
                    ),
                    "C_pair": vector_rel(p_first, p_second),
                    "fixed_pair": [first, second],
                }
        monotone_error = bool(
            all(production_tight_errors[format(h, ".17g")] is not None for h in old)
            and production_tight_errors[format(old[0], ".17g")]
            < production_tight_errors[format(old[1], ".17g")]
            < production_tight_errors[format(old[2], ".17g")]
        )
        geodesic_solver_envelopes: dict[str, Any] = {}
        for h in sorted(set((*main, *old)), reverse=True):
            tight_geo = get_d2(
                d2_vectors, label, "tight_state", "geodesic_u2", 8, h
            )
            radau_geo = get_d2(
                d2_vectors, label, "radau_state", "geodesic_u2", 8, h
            )
            if tight_geo is None or radau_geo is None:
                geodesic_solver_envelopes[format(h, ".17g")] = {
                    "tight_to_Radau": None,
                    "null_reason": "required geodesic tight or Radau D2 unavailable",
                }
            else:
                geodesic_solver_envelopes[format(h, ".17g")] = {
                    "tight_to_Radau": vector_rel(tight_geo, radau_geo),
                    "null_reason": None,
                }
        r4_cross: dict[str, Any] = {}
        for chart in ("affine", "geodesic_u2"):
            tight_r4 = richardson_from_d2(
                d2_vectors, label, "tight_state", chart, 8, 2.0e-4
            )
            radau_r4 = richardson_from_d2(
                d2_vectors, label, "radau_state", chart, 8, 2.0e-4
            )
            r4_cross[chart] = (
                vector_rel(tight_r4, radau_r4)
                if tight_r4 is not None and radau_r4 is not None
                else None
            )
        u2_refs = references.get(label, {}).get(8, {})
        fixed_neighbor_stability = (
            max(
                vector_rel(u2_refs["primary"], u2_refs["coarse"]),
                vector_rel(u2_refs["primary"], u2_refs["fine"]),
            )
            if set(u2_refs) == {"coarse", "primary", "fine"}
            else None
        )
        quantifiers_complete = bool(
            all(record["q2"] is not None for record in q2_records.values())
            and all(
                record.get("envelope") is not None
                and record.get("required_Radau_missing", False) is False
                for record in solver_envelopes.values()
            )
            and all(
                record.get("E_triple") is not None
                and record.get("C_triple") is not None
                for record in triple_metrics.values()
            )
            and all(
                record.get("E_pair") is not None
                and record.get("C_pair") is not None
                for record in old_pair_metrics.values()
            )
            and all(value is not None for value in production_tight_errors.values())
            and all(value is not None for value in r4_cross.values())
            and fixed_neighbor_stability is not None
            and all(
                record.get("tight_to_Radau") is not None
                for record in geodesic_solver_envelopes.values()
            )
        )
        complete = bool(complete and quantifiers_complete)
        payload = {
            "complete": complete,
            "quantifiers_complete": quantifiers_complete,
            "missing_slots": missing,
            "q2_tight_affine": q2_records,
            "solver_derivative_envelopes": solver_envelopes,
            "fixed_triple_metrics": triple_metrics,
            "fixed_old_pair_metrics": old_pair_metrics,
            "production_to_tight_exact_old_step_errors": production_tight_errors,
            "exact_old_step_error_strictly_increases_as_h_decreases": monotone_error,
            "geodesic_tight_to_Radau_derivative_envelopes": geodesic_solver_envelopes,
            "all_consecutive_dyadic_q2_chain": dyadic_chain,
            "fixed_R4_tight_to_Radau": r4_cross,
            "fixed_tight_R4_neighbor_stability": fixed_neighbor_stability,
            "fixed_reference_stable": bool(
                fixed_neighbor_stability is not None
                and fixed_neighbor_stability <= 0.005
                and all(
                    value is not None and value <= 0.005
                    for value in r4_cross.values()
                )
            ),
            "main_ladder": main,
            "dyadic_tail": tail,
            "exact_phase41_steps": old,
            "no_favorable_h_selected": True,
        }
        ledger.finish(key, "SUCCESS" if complete else "EVALUATION_FAILED", payload=payload, error=None if complete else "required u2 slot missing")
        point_details[label] = payload
        all_complete = all_complete and complete
    return {"passed": all_complete, "complete": all_complete, "points": point_details}


CAUSE_NAMES = (
    "TRUNCATION_EVIDENCE",
    "SOLVER_NOISE_EVIDENCE",
    "CHART_CURVATURE_EVIDENCE",
    "STEP_PAIR_SELECTION_ARTIFACT",
    "VARIATIONAL_RHS_BUG_EVIDENCE",
    "PRODUCTION_TANGENT_SOLVER_EVIDENCE",
    "INTEGRATED_VARIATIONAL_BUG_EVIDENCE",
)


def cause_record(
    *,
    complete: bool,
    supported: bool | None = None,
    evidence_status: str | None = None,
    metric_paths: Sequence[str],
    rationale: str,
) -> dict[str, Any]:
    if evidence_status is None:
        if supported is None:
            raise InvalidRun("cause record lacks a frozen evidence decision")
        evidence_status = (
            "SUPPORTED"
            if supported
            else "NOT_SUPPORTED"
            if complete
            else "INCONCLUSIVE"
        )
    if evidence_status not in {"SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}:
        raise InvalidRun("cause evidence status outside frozen tri-state domain")
    return {
        "completion_status": "COMPLETE" if complete else "INCOMPLETE",
        "evidence_status": evidence_status,
        "metric_paths": list(metric_paths),
        "rationale": rationale,
    }


def resolve_retained_metric_path(root: Mapping[str, Any], path: str) -> Any:
    value: Any = root
    for component in path.split("."):
        if "[" in component:
            name, suffix = component.split("[", 1)
            if not suffix.endswith("]") or not suffix[:-1].isdigit():
                raise InvalidRun(f"invalid cause metric path syntax: {path}")
            if name:
                if not isinstance(value, Mapping) or name not in value:
                    raise InvalidRun(f"unresolved cause metric path: {path}")
                value = value[name]
            index = int(suffix[:-1])
            if not isinstance(value, (list, tuple)) or index >= len(value):
                raise InvalidRun(f"unresolved cause metric path index: {path}")
            value = value[index]
        else:
            if not isinstance(value, Mapping) or component not in value:
                raise InvalidRun(f"unresolved cause metric path: {path}")
            value = value[component]
    return value


def classify_causes(
    context: CheckpointContext,
    ledger: SlotLedger,
    d2_vectors: Mapping[tuple[str, str, str, int, float], np.ndarray],
    references: Mapping[str, Mapping[int, Mapping[str, np.ndarray]]],
    three_way: Mapping[str, Any],
    negative: Mapping[str, Any],
    chart: Mapping[str, Any],
    local: Mapping[str, Any],
    r4: Mapping[str, Any],
    u2: Mapping[str, Any],
    homotopy: Mapping[str, Any],
) -> dict[str, Any]:
    per_point: dict[str, dict[str, Any]] = {}
    for label in TARGETS:
        records: dict[str, Any] = {}
        u2_point = u2["points"].get(label, {})
        triple = u2_point.get("fixed_triple_metrics", {})
        q2 = u2_point.get("q2_tight_affine", {})
        fixed_q2_keys = (format(4.0e-4, ".17g"), format(2.0e-4, ".17g"))
        fixed_q2 = {key: q2.get(key, {}) for key in fixed_q2_keys}
        tight_j = None
        three = three_way.get(label, {})
        if three.get("complete"):
            tight_j = np.asarray(three["tight_J"], dtype=float)
        d2_0001 = get_d2(
            d2_vectors, label, "tight_state", "affine", 8, 1.0e-4
        )
        r4_u2 = references.get(label, {}).get(8, {}).get("primary")
        solver_envelopes = u2_point.get("solver_derivative_envelopes", {})
        truncation_required_h = (4.0e-4, 2.0e-4, 1.0e-4, 5.0e-5)
        truncation_cross_method_complete = all(
            solver_envelopes.get(format(step, ".17g"), {}).get(
                "required_Radau_missing"
            )
            is False
            and solver_envelopes.get(format(step, ".17g"), {}).get(
                "tight_to_Radau"
            )
            is not None
            for step in truncation_required_h
        )
        trunc_complete = bool(
            tight_j is not None
            and d2_0001 is not None
            and r4_u2 is not None
            and truncation_cross_method_complete
            and all(record.get("q2") is not None for record in fixed_q2.values())
            and all(
                record.get("E_triple") is not None
                and record.get("C_triple") is not None
                for record in triple.values()
            )
        )
        trunc_supported = False
        trunc_ratio: float | None = None
        if trunc_complete:
            assert tight_j is not None and d2_0001 is not None and r4_u2 is not None
            trunc_ratio = float(
                np.linalg.norm(d2_0001 - tight_j[:, 8])
                / max(np.linalg.norm(r4_u2 - tight_j[:, 8]), 1.0e-30)
            )
            trunc_supported = bool(
                all(
                    1.5 <= float(record["q2"]) <= 2.5
                    for record in fixed_q2.values()
                )
                and all(
                    float(record["E_triple"])
                    <= 0.1 * float(record["C_triple"])
                    for record in triple.values()
                )
                and trunc_ratio >= 4.0
            )
        records["TRUNCATION_EVIDENCE"] = cause_record(
            complete=trunc_complete,
            supported=trunc_supported,
            metric_paths=(
                f"u2_disentanglement.points.{label}.q2_tight_affine",
                f"u2_disentanglement.points.{label}.fixed_triple_metrics",
                f"cause_ledger.points.{label}.cause_aux.truncation_ratio",
            ),
            rationale=f"fixed two-triple rule; truncation_ratio={trunc_ratio}",
        )

        pair_metrics = u2_point.get("fixed_old_pair_metrics", {})
        old_errors = u2_point.get("production_to_tight_exact_old_step_errors", {})
        geodesic_old = u2_point.get(
            "geodesic_tight_to_Radau_derivative_envelopes", {}
        )
        old_steps = (2.0e-6, 5.0e-7, 1.0e-7)
        affine_old_cross_method_complete = all(
            solver_envelopes.get(format(step, ".17g"), {}).get(
                "required_Radau_missing"
            )
            is False
            and solver_envelopes.get(format(step, ".17g"), {}).get(
                "tight_to_Radau"
            )
            is not None
            for step in old_steps
        )
        solver_complete = bool(
            len(pair_metrics) == 2
            and all(
                record.get("E_pair") is not None and record.get("C_pair") is not None
                for record in pair_metrics.values()
            )
            and len(old_errors) == 3
            and all(value is not None for value in old_errors.values())
            and affine_old_cross_method_complete
            and all(
                geodesic_old.get(format(step, ".17g"), {}).get(
                    "tight_to_Radau"
                )
                is not None
                for step in old_steps
            )
            and u2_point.get("fixed_tight_R4_neighbor_stability") is not None
            and all(
                value is not None
                for value in u2_point.get("fixed_R4_tight_to_Radau", {}).values()
            )
        )
        solver_supported = bool(
            solver_complete
            and u2_point.get("fixed_reference_stable") is True
            and u2_point.get(
                "exact_old_step_error_strictly_increases_as_h_decreases"
            )
            is True
            and all(
                float(record["E_pair"]) >= 0.5 * float(record["C_pair"])
                for record in pair_metrics.values()
            )
        )
        solver_evidence = (
            "INCONCLUSIVE"
            if not solver_complete
            or u2_point.get("fixed_reference_stable") is not True
            else "SUPPORTED"
            if solver_supported
            else "NOT_SUPPORTED"
        )
        records["SOLVER_NOISE_EVIDENCE"] = cause_record(
            complete=solver_complete,
            evidence_status=solver_evidence,
            metric_paths=(
                f"u2_disentanglement.points.{label}.production_to_tight_exact_old_step_errors",
                f"u2_disentanglement.points.{label}.fixed_old_pair_metrics",
                f"u2_disentanglement.points.{label}.fixed_reference_stable",
                f"u2_disentanglement.points.{label}.geodesic_tight_to_Radau_derivative_envelopes",
            ),
            rationale="fixed monotone old-step error and E_pair>=0.5*C_pair rule",
        )

        chart_point = chart["points"].get(label, {})
        curvature = chart_point.get("curvature_fixed_h_0.0002", {})
        curvature_r4 = curvature.get("R4", {})
        chart_complete = bool(
            chart_point.get("complete")
            and tight_j is not None
            and curvature.get("E_chart") is not None
            and all(
                curvature_r4.get(name) is not None
                for name in ("affine_tight", "geodesic_tight")
            )
        )
        chart_prerequisite_valid = bool(
            chart_complete
            and chart_point.get("algebra_passed") is True
            and float(chart_point.get("geodesic_same_base_error", math.inf)) <= 1e-11
            and float(
                chart_point.get("geodesic_same_first_tangent_error", math.inf)
            )
            <= 1e-11
            and float(curvature.get("E_chart", math.inf)) <= 0.005
        )
        chart_supported = False
        chart_metrics: dict[str, Any] = {}
        if chart_prerequisite_valid:
            affine = np.asarray(curvature_r4["affine_tight"])
            geodesic = np.asarray(curvature_r4["geodesic_tight"])
            assert tight_j is not None
            affine_error = vector_rel(affine, tight_j[:, 8])
            geodesic_error = vector_rel(geodesic, tight_j[:, 8])
            chart_difference = vector_rel(affine, geodesic)
            e_chart = float(curvature["E_chart"])
            chart_metrics = {
                "affine_to_tight_J": affine_error,
                "geodesic_to_tight_J": geodesic_error,
                "affine_to_geodesic": chart_difference,
                "E_chart": e_chart,
            }
            chart_supported = bool(
                affine_error >= 5.0 * geodesic_error
                and chart_difference >= 0.8 * affine_error
                and chart_difference >= 5.0 * e_chart
            )
        chart_evidence = (
            "INCONCLUSIVE"
            if not chart_prerequisite_valid
            else "SUPPORTED"
            if chart_supported
            else "NOT_SUPPORTED"
        )
        records["CHART_CURVATURE_EVIDENCE"] = cause_record(
            complete=chart_complete,
            evidence_status=chart_evidence,
            metric_paths=(
                f"chart_diagnostics.points.{label}",
                f"cause_ledger.points.{label}.cause_aux.chart_metrics",
            ),
            rationale=f"single fixed h=.0002 rule; metrics={chart_metrics}",
        )

        negative_point = negative["points"].get(label, {})
        r4_point = r4["points"].get(label, {})
        homotopy_point = homotopy["points"].get(label, {})
        r4_u2_record = (
            r4_point.get("per_column", [None] * 14)[8]
            if len(r4_point.get("per_column", [])) == 14
            else None
        )
        tight_specific_pass = False
        if isinstance(r4_u2_record, dict):
            tight_metrics = r4_u2_record.get("to_tight", {})
            tight_specific_pass = bool(
                r4_u2_record.get("neighbor_stability", math.inf) <= 0.005
                and tight_metrics.get("symmetric_relative", math.inf) <= 0.01
                and tight_metrics.get("signed_cosine", -math.inf) > 0.0
                and tight_metrics.get("angle_sine", math.inf) <= 0.01
                and tight_metrics.get("abs_norm_ratio_minus_one", math.inf) <= 0.01
            )
        step_complete = bool(
            negative_point.get("complete")
            and r4_u2_record is not None
            and isinstance(r4_u2_record.get("to_checkpoint"), dict)
            and isinstance(r4_u2_record.get("to_tight"), dict)
            and r4_u2_record.get("neighbor_stability") is not None
            and u2_point.get("fixed_tight_R4_neighbor_stability") is not None
            and all(
                value is not None
                for value in u2_point.get("fixed_R4_tight_to_Radau", {}).values()
            )
            and homotopy_point.get("complete") is True
            and homotopy_point.get("certified") is not None
            and homotopy_point.get("mutation_controls_passed") is not None
        )
        step_supported = bool(
            step_complete
            and negative_point.get("faithful_reproduction_passed") is True
            and r4_u2_record.get("passed") is True
            and u2_point.get("fixed_reference_stable") is True
            and homotopy_point.get("certified") is True
            and homotopy_point.get("mutation_controls_passed") is True
        )
        records["STEP_PAIR_SELECTION_ARTIFACT"] = cause_record(
            complete=step_complete,
            supported=step_supported,
            metric_paths=(
                f"phase41_negative_control.points.{label}",
                f"finite_difference_diagnostics.points.{label}.per_column[8]",
                f"u2_disentanglement.points.{label}",
                f"orientation_homotopy.points.{label}",
            ),
            rationale="old first-pair failure plus all preselected Phase42 references",
        )

        local_point = local["points"].get(label, {})
        local_complete = bool(local_point.get("evaluation_complete"))
        # This cause is existential: one stable threshold violation is evidence
        # even when an unrelated local slot is incomplete.
        local_supported = bool(local_point.get("stable_violation"))
        local_evidence = (
            "SUPPORTED"
            if local_supported
            else "NOT_SUPPORTED"
            if local_complete
            and local_point.get("all_reference_checks_stable") is True
            and local_point.get("passed") is True
            else "INCONCLUSIVE"
        )
        records["VARIATIONAL_RHS_BUG_EVIDENCE"] = cause_record(
            complete=local_complete,
            evidence_status=local_evidence,
            metric_paths=(f"local_variational_diagnostics.points.{label}",),
            rationale="stable local-Hessian or tier-matched endpoint-time violation",
        )

        production_solver_complete = bool(
            three.get("complete")
            and three.get("production_drift_passed") is True
            and r4_u2_record is not None
            and r4_u2_record.get("complete") is True
            and u2_point.get("fixed_tight_R4_neighbor_stability") is not None
            and all(
                value is not None
                for value in u2_point.get("fixed_R4_tight_to_Radau", {}).values()
            )
        )
        production_solver_supported = False
        production_solver_stable = bool(
            production_solver_complete
            and records["VARIATIONAL_RHS_BUG_EVIDENCE"]["evidence_status"]
            == "NOT_SUPPORTED"
            and u2_point.get("fixed_reference_stable") is True
        )
        if production_solver_stable:
            checkpoint_to_tight = float(
                three["comparisons"]["checkpoint_to_tight_per_column"][8]
            )
            r4_to_tight_pass = tight_specific_pass
            production_solver_supported = bool(
                checkpoint_to_tight > 0.005 and r4_to_tight_pass
            )
        production_solver_evidence = (
            "INCONCLUSIVE"
            if not production_solver_stable
            else "SUPPORTED"
            if production_solver_supported
            else "NOT_SUPPORTED"
        )
        records["PRODUCTION_TANGENT_SOLVER_EVIDENCE"] = cause_record(
            complete=production_solver_complete,
            evidence_status=production_solver_evidence,
            metric_paths=(
                f"three_way_J.{label}",
                f"finite_difference_diagnostics.points.{label}.per_column[8]",
            ),
            rationale="production differs from tight while tight agrees with fixed R4",
        )

        tight_u2_column_finite_nonzero = bool(
            tight_j is not None
            and np.all(np.isfinite(tight_j[:, 8]))
            and float(np.linalg.norm(tight_j[:, 8])) > 0.0
        )
        integrated_complete = bool(
            r4_u2_record is not None
            and r4_u2_record.get("complete") is True
            and three.get("complete")
            and tight_u2_column_finite_nonzero
            and u2_point.get("fixed_tight_R4_neighbor_stability") is not None
            and all(
                value is not None
                for value in u2_point.get("fixed_R4_tight_to_Radau", {}).values()
            )
        )
        integrated_stable = bool(
            integrated_complete
            and three.get("production_drift_passed") is True
            and records["VARIATIONAL_RHS_BUG_EVIDENCE"]["evidence_status"]
            == "NOT_SUPPORTED"
            and u2_point.get("fixed_reference_stable") is True
        )
        integrated_supported = bool(
            integrated_stable and not tight_specific_pass
        )
        integrated_evidence = (
            "INCONCLUSIVE"
            if not integrated_stable
            else "SUPPORTED"
            if integrated_supported
            else "NOT_SUPPORTED"
        )
        records["INTEGRATED_VARIATIONAL_BUG_EVIDENCE"] = cause_record(
            complete=integrated_complete,
            evidence_status=integrated_evidence,
            metric_paths=(
                f"finite_difference_diagnostics.points.{label}.per_column[8]",
            ),
            rationale="tight transported u2 fails stable R4 vector/direction/norm tests",
        )

        for cause in CAUSE_NAMES:
            ledger.finish(
                f"cause|{label}|{cause}", "SUCCESS", payload=records[cause]
            )
        stable_supported = any(
            records[cause]["evidence_status"] == "SUPPORTED"
            for cause in CAUSE_NAMES
        )
        any_inconclusive = any(
            records[cause]["evidence_status"] == "INCONCLUSIVE"
            for cause in CAUSE_NAMES
        )
        unresolved_supported = bool(not stable_supported and any_inconclusive)
        unresolved = {
            "completion_status": "COMPLETE",
            "evidence_status": (
                "SUPPORTED" if unresolved_supported else "NOT_SUPPORTED"
            ),
            "metric_paths": [f"cause_ledger.points.{label}"],
            "rationale": "exact deterministic UNRESOLVED rule",
        }
        ledger.finish(f"cause|{label}|UNRESOLVED", "SUCCESS", payload=unresolved)
        records["UNRESOLVED"] = unresolved
        records["cause_aux"] = {
            "truncation_ratio": trunc_ratio,
            "chart_metrics": chart_metrics,
        }
        per_point[label] = records

    aggregate: dict[str, Any] = {}
    for cause in (*CAUSE_NAMES, "UNRESOLVED"):
        statuses = [per_point[label][cause]["evidence_status"] for label in TARGETS]
        completion_statuses = [
            per_point[label][cause]["completion_status"] for label in TARGETS
        ]
        aggregate_status = (
            "SUPPORTED"
            if "SUPPORTED" in statuses
            else "NOT_SUPPORTED"
            if all(status == "NOT_SUPPORTED" for status in statuses)
            else "INCONCLUSIVE"
        )
        record = {
            "completion_status": (
                "COMPLETE"
                if all(status == "COMPLETE" for status in completion_statuses)
                else "INCOMPLETE"
            ),
            "evidence_status": aggregate_status,
            "aggregation": "any-fixed-point summary",
            "point_statuses": dict(zip(TARGETS, statuses)),
            "metric_paths": [
                f"cause_ledger.points.{label}.{cause}" for label in TARGETS
            ],
        }
        ledger.finish(f"cause|aggregate|{cause}", "SUCCESS", payload=record)
        aggregate[cause] = record
    complete = bool(
        set(per_point) == set(TARGETS)
        and all(set(records) >= set((*CAUSE_NAMES, "UNRESOLVED")) for records in per_point.values())
        and set(aggregate) == set((*CAUSE_NAMES, "UNRESOLVED"))
    )
    retained_root: dict[str, Any] = {
        "u2_disentanglement": u2,
        "chart_diagnostics": chart,
        "phase41_negative_control": negative,
        "finite_difference_diagnostics": r4,
        "local_variational_diagnostics": local,
        "three_way_J": three_way,
        "orientation_homotopy": homotopy,
        "cause_ledger": {
            "points": per_point,
            "aggregate_any_fixed_point": aggregate,
        },
    }
    allowed_completion = {"COMPLETE", "INCOMPLETE"}
    allowed_evidence = {"SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
    path_count = 0
    for label in TARGETS:
        stable_supported = any(
            per_point[label][cause]["evidence_status"] == "SUPPORTED"
            for cause in CAUSE_NAMES
        )
        any_inconclusive = any(
            per_point[label][cause]["evidence_status"] == "INCONCLUSIVE"
            for cause in CAUSE_NAMES
        )
        expected_unresolved = "SUPPORTED" if (not stable_supported and any_inconclusive) else "NOT_SUPPORTED"
        if per_point[label]["UNRESOLVED"]["evidence_status"] != expected_unresolved:
            raise InvalidRun(f"UNRESOLVED deterministic rule drift: {label}")
        for cause in (*CAUSE_NAMES, "UNRESOLVED"):
            record = per_point[label][cause]
            if record["completion_status"] not in allowed_completion:
                raise InvalidRun(f"cause completion domain drift: {label}/{cause}")
            if record["evidence_status"] not in allowed_evidence:
                raise InvalidRun(f"cause evidence domain drift: {label}/{cause}")
            for path in record["metric_paths"]:
                resolve_retained_metric_path(retained_root, str(path))
                path_count += 1
    for cause in (*CAUSE_NAMES, "UNRESOLVED"):
        statuses = [per_point[label][cause]["evidence_status"] for label in TARGETS]
        expected_status = (
            "SUPPORTED" if "SUPPORTED" in statuses
            else "NOT_SUPPORTED" if all(value == "NOT_SUPPORTED" for value in statuses)
            else "INCONCLUSIVE"
        )
        if aggregate[cause]["evidence_status"] != expected_status:
            raise InvalidRun(f"aggregate any-fixed-point rule drift: {cause}")
        for path in aggregate[cause]["metric_paths"]:
            resolve_retained_metric_path(retained_root, str(path))
            path_count += 1
    return {
        "passed": complete,
        "complete": complete,
        "multi_label_policy": True,
        "tri_state_domains_validated": True,
        "unresolved_rules_validated": True,
        "aggregate_rules_validated": True,
        "resolved_metric_path_count": path_count,
        "points": per_point,
        "aggregate_any_fixed_point": aggregate,
    }


def validate_solver_attempt_ledgers(
    ledger: SlotLedger, tiers: Mapping[str, TierSpec]
) -> dict[str, Any]:
    checked = 0
    failed_attempts = 0
    for key, slot in ledger.slots.items():
        kind = slot["metadata"].get("slot_kind")
        if kind not in {"endpoint", "center", "augmented_center"}:
            continue
        checked += 1
        payload = slot.get("payload")
        if not isinstance(payload, dict):
            raise InvalidRun(f"solver slot lacks structured payload: {key}")
        if payload.get("fallback_used") is not False:
            # Successful endpoint payload nests these under solver.
            solver = payload.get("solver")
            if not isinstance(solver, dict) or solver.get("fallback_used") is not False:
                raise InvalidRun(f"fallback flag missing/drifted: {key}")
            if solver.get("no_fallback_method_used") is not True:
                raise InvalidRun(f"no-fallback assertion missing: {key}")
        elif payload.get("no_fallback_method_used") is not True:
            raise InvalidRun(f"no-fallback assertion missing: {key}")
        parameters = np.asarray(payload.get("parameters"), dtype=float)
        if parameters.shape != (14,) or not np.all(np.isfinite(parameters)):
            raise InvalidRun(f"solver slot parameter retention invalid: {key}")
        margins = payload.get("bounds_margins")
        if not isinstance(margins, dict):
            raise InvalidRun(f"solver slot bounds ledger missing: {key}")
        if kind in {"endpoint", "center"}:
            tier_name = str(slot["metadata"]["tier"])
            solver = payload.get("solver")
            expected = tiers[tier_name]
            if slot["terminal_status"] == "SUCCESS":
                if not isinstance(solver, dict):
                    raise InvalidRun(f"successful endpoint solver ledger missing: {key}")
                if (
                    solver.get("method") != expected.method
                    or solver.get("representation") != expected.representation
                    or float(solver.get("rtol")) != expected.rtol
                    or float(solver.get("atol")) != expected.atol
                    or float(solver.get("max_step")) != expected.max_step
                ):
                    raise InvalidRun(f"endpoint solver tier drift: {key}")
            else:
                tier_record = payload.get("tier")
                if not isinstance(tier_record, dict) or (
                    tier_record.get("method") != expected.method
                    or tier_record.get("representation") != expected.representation
                    or float(tier_record.get("rtol")) != expected.rtol
                    or float(tier_record.get("atol")) != expected.atol
                    or float(tier_record.get("max_step")) != expected.max_step
                ):
                    raise InvalidRun(f"failed endpoint tier provenance drift: {key}")
                failed_attempts += 1
        else:
            tier_record = payload.get("tier")
            if tier_record is None:
                solver = payload.get("solver")
                if not isinstance(solver, dict):
                    raise InvalidRun(f"production augmented solver ledger missing: {key}")
                expected = tiers["production_augmented"]
                if (
                    solver.get("method") != expected.method
                    or solver.get("representation") != expected.representation
                    or float(solver.get("rtol")) != expected.rtol
                    or float(solver.get("atol")) != expected.atol
                    or float(solver.get("max_step")) != expected.max_step
                ):
                    raise InvalidRun(f"production augmented tier drift: {key}")
            else:
                expected = tiers[str(slot["metadata"]["tier"])]
                if (
                    tier_record.get("method") != expected.method
                    or tier_record.get("representation") != expected.representation
                    or float(tier_record.get("rtol")) != expected.rtol
                    or float(tier_record.get("atol")) != expected.atol
                    or float(tier_record.get("max_step")) != expected.max_step
                ):
                    raise InvalidRun(f"tight augmented tier drift: {key}")
            if slot["terminal_status"] != "SUCCESS":
                failed_attempts += 1
    if checked != 915:
        raise InvalidRun(f"solver attempt ledger count is {checked}, not 915")
    return {
        "checked_solver_attempt_count": checked,
        "failed_attempt_count": failed_attempts,
        "fallback_used_count": 0,
        "all_tier_and_retention_checks_passed": True,
    }


def exact_richardson_identity() -> dict[str, Any]:
    h = sympy.symbols("h", nonzero=True, real=True)
    f_m, f_mh, f_ph, f_p = sympy.symbols("f_m f_mh f_ph f_p")
    d2_h = (f_p - f_m) / (sympy.Integer(2) * h)
    d2_half = (f_ph - f_mh) / h
    r4 = (sympy.Integer(4) * d2_half - d2_h) / sympy.Integer(3)
    five = (
        f_m
        - sympy.Integer(8) * f_mh
        + sympy.Integer(8) * f_ph
        - f_p
    ) / (sympy.Integer(6) * h)
    difference = sympy.simplify(r4 - five)
    if difference != 0:
        raise InvalidRun("exact Richardson/five-point identity failed")
    return {
        "D2_formula": str(d2_h),
        "R4_formula": str(r4),
        "five_point_formula": str(five),
        "symbolic_difference": str(difference),
        "used_exact_integer_arithmetic": True,
    }


def hardcoded_endpoint_specifications() -> dict[tuple[str, str, int], tuple[float, ...]]:
    """Independent expectation for the frozen manifest's endpoint product."""
    old: dict[int, tuple[float, ...]] = {
        **{index: (2.0e-6, 5.0e-7) for index in range(7)},
        7: (2.0e-5, 1.0e-5),
        **{index: (2.0e-6, 5.0e-7, 1.0e-7) for index in range(8, 13)},
        13: (5.0e-6, 1.0e-6, 2.0e-7),
    }
    main = (4.0e-4, 2.0e-4, 1.0e-4, 5.0e-5)
    tail = (
        2.5e-5,
        1.25e-5,
        6.25e-6,
        3.125e-6,
        1.5625e-6,
        7.8125e-7,
        3.90625e-7,
        1.953125e-7,
        9.765625e-8,
    )
    old_u2 = (2.0e-6, 5.0e-7, 1.0e-7)

    def union(*groups: Iterable[float]) -> tuple[float, ...]:
        values: list[float] = []
        for group in groups:
            for value in group:
                if value not in values:
                    values.append(value)
        return tuple(values)

    result: dict[tuple[str, str, int], tuple[float, ...]] = {}
    for column in range(14):
        result[("production_state", "affine", column)] = old[column]
    result[("production_state", "affine", 8)] = union(old[8], main, tail)
    for column in range(14):
        result[("tight_state", "affine", column)] = main
    result[("tight_state", "affine", 8)] = union(main, tail, old_u2)
    result[("tight_state", "geodesic_u2", 8)] = union(main, tail, old_u2)
    result[("radau_state", "affine", 8)] = union(main, old_u2)
    result[("radau_state", "affine", 13)] = main
    result[("radau_state", "geodesic_u2", 8)] = union(main, old_u2)
    return result


def expected_slot_keys() -> set[str]:
    """Build the 2,192 expected logical keys without consulting the manifest."""
    keys: set[str] = set()
    specs = hardcoded_endpoint_specifications()
    for point in TARGETS:
        for tier, chart_kind in (
            ("production_state", "affine"),
            ("tight_state", "affine"),
            ("tight_state", "geodesic_u2"),
            ("radau_state", "affine"),
            ("radau_state", "geodesic_u2"),
        ):
            keys.add(center_slot_key(point, tier, chart_kind))
        for tier in ("production_augmented", "tight_augmented"):
            keys.add(f"augmented|{point}|{tier}")
        for (tier, chart_kind, column), steps in specs.items():
            for step in steps:
                keys.add(d2_slot_key(point, tier, chart_kind, column, step))
                for sign in (-1, 1):
                    keys.add(
                        endpoint_slot_key(
                            point, tier, chart_kind, column, step, sign
                        )
                    )
        for column in range(14):
            for reference in ("coarse", "primary", "fine"):
                keys.add(
                    f"R4|{point}|tight_state|affine|col={column}|{reference}"
                )
        for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            for direction in range(6):
                base = (
                    f"local_RHS|{point}|fraction={format(fraction,'.2g')}|"
                    f"direction={direction}"
                )
                keys.add(base)
                for epsilon in (2.0e-5, 1.0e-5, 5.0e-6):
                    for sign in (-1, 1):
                        keys.add(
                            f"{base}|epsilon={format(epsilon,'.17g')}|"
                            f"{'plus' if sign > 0 else 'minus'}"
                        )
        for control in (
            "positive_K_time_tangent",
            "checkpoint_negative_time_column",
            "production_negative_time_column",
            "state_only_R4_time_column",
        ):
            keys.add(f"time_control|{point}|{control}")
        for diagnostic in (
            "three_way_J",
            "phase41_negative_control",
            "chart",
            "local_RHS",
            "all_column_R4",
            "u2_disentanglement",
            "homotopy",
        ):
            keys.add(f"matrix|{point}|{diagnostic}")
        for mutation in (
            "positive_column_rescaling",
            "single_reference_column_flip",
            "no_sampled_t_used",
        ):
            keys.add(f"mutation|{point}|{mutation}")
        for cause in (*CAUSE_NAMES, "UNRESOLVED"):
            keys.add(f"cause|{point}|{cause}")
    for cause in (*CAUSE_NAMES, "UNRESOLVED"):
        keys.add(f"cause|aggregate|{cause}")
    if len(keys) != 2192:
        raise InvalidRun(f"independent expected slot-key count is {len(keys)}")
    return keys


def frozen_map_and_tier_guard(
    manifest: Mapping[str, Any],
    context: CheckpointContext,
    ledger: SlotLedger,
    tiers: Mapping[str, TierSpec],
) -> dict[str, Any]:
    fixed = manifest["fixed_map"]
    expected_order = [
        "y_a1", "y_phi1", "y_a2", "y_phi2", "y_a3", "y_phi3",
        "psi", "u1", "u2", "u3", "u4", "u5", "u6", "flow_time",
    ]
    expected_root = (
        "J=row_scales[:,None]*column_stack([V_Gamma,-V_K]); column 13 is "
        "the negative row-scaled K flow-time tangent."
    )
    if (
        fixed["parameter_order"] != expected_order
        or fixed["Gamma_columns_zero_based"] != list(range(7))
        or fixed["K_columns_zero_based"] != list(range(7, 14))
        or fixed["suspect_column"]
        != {"zero_based_index": 8, "K_local_index": 1, "name": "u2"}
        or fixed["root_J_sign_convention"] != expected_root
        or fixed["candidate_reoptimization_allowed"] is not False
        or fixed["determinant_sign_may_select_a_step"] is not False
        or fixed["same_cap_radius_shape_metric_chart_and_roots"] is not True
    ):
        raise InvalidRun("fixed R14 parameter/sign/root map drift")
    if not np.all(context.row_scales > 0.0):
        raise InvalidRun("row scales are not strictly positive")

    actual_specs = endpoint_specifications(manifest)
    expected_specs = hardcoded_endpoint_specifications()
    if actual_specs != expected_specs:
        raise InvalidRun("endpoint ladder/tier specification drift")
    expected_tiers = {
        "production_state": ("DOP853", "complex xi state", 2e-10, 2e-12, .04),
        "production_augmented": (
            "DOP853", "complex xi plus 7x6 complex chart tangent",
            8e-11, 8e-13, .025,
        ),
        "tight_state": ("DOP853", "complex xi state", 2e-12, 2e-14, .01),
        "tight_augmented": (
            "DOP853", "complex xi plus 7x6 complex chart tangent",
            2e-12, 2e-14, .01,
        ),
        "radau_state": (
            "Radau",
            "realified xi in interleaved [Re xi_1,Im xi_1,...,Re xi_7,Im xi_7] order",
            5e-12, 5e-14, .01,
        ),
    }
    for name, expected in expected_tiers.items():
        observed = tiers[name]
        if (
            observed.method,
            observed.representation,
            observed.rtol,
            observed.atol,
            observed.max_step,
        ) != expected:
            raise InvalidRun(f"full integration tier drift: {name}")

    expected_keys = expected_slot_keys()
    if set(ledger.slots) != expected_keys:
        missing = sorted(expected_keys - set(ledger.slots))[:5]
        extra = sorted(set(ledger.slots) - expected_keys)[:5]
        raise InvalidRun(f"logical slot-key set drift; missing={missing}, extra={extra}")
    for key, slot in ledger.slots.items():
        kind = slot["metadata"]["slot_kind"]
        if kind not in {"endpoint", "center"}:
            continue
        payload = slot["payload"]
        if not isinstance(payload, dict):
            raise InvalidRun(f"map slot lacks retained payload: {key}")
        parameters = np.asarray(payload["parameters"], dtype=float)
        point = context.points[str(slot["metadata"]["point"])]
        expected_parameters = point.parameters.copy()
        if kind == "endpoint":
            expected_parameters[int(slot["metadata"]["column"])] += (
                int(slot["metadata"]["sign"]) * float(slot["metadata"]["h"])
            )
        if not np.array_equal(parameters, expected_parameters):
            raise InvalidRun(f"endpoint was clipped/replaced/retuned: {key}")
        inside = payload["bounds_margins"]["strictly_inside"] is True
        if not inside:
            if not (
                slot["terminal_status"] == "EVALUATION_FAILED"
                and "outside box" in str(slot.get("error", ""))
            ):
                raise InvalidRun(
                    f"outside-box slot was clipped, replaced, or mistyped: {key}"
                )
            continue
        if slot["terminal_status"] == "SUCCESS":
            cache_key = payload.get("cache_key")
            if not isinstance(cache_key, list) or len(cache_key) != 14:
                raise InvalidRun(f"cache isolation key malformed: {key}")
            tier = tiers[str(slot["metadata"]["tier"])]
            expected_prefix = [
                point.label, tier.name, tier.method, tier.rtol, tier.atol,
                tier.max_step, str(slot["metadata"]["chart_kind"]),
            ]
            if cache_key[:7] != expected_prefix or cache_key[7:] != list(parameters[7:14]):
                raise InvalidRun(f"cache isolation key drift: {key}")
    return {
        "parameter_order": expected_order,
        "Gamma_columns": list(range(7)),
        "K_columns": list(range(7, 14)),
        "suspect_column": fixed["suspect_column"],
        "root_sign_convention": expected_root,
        "endpoint_spec_pair_count": sum(len(v) for v in actual_specs.values()),
        "full_expected_slot_key_set_equal": True,
        "cache_and_no_clipping_checked": True,
        "tiers": {name: dataclasses.asdict(value) for name, value in tiers.items()},
    }


def frozen_math_guard(manifest: Mapping[str, Any]) -> dict[str, Any]:
    protocol = manifest["finite_difference_protocol"]
    metrics = manifest["relative_metric_definitions"]
    homotopy = manifest["orientation_homotopy_protocol"]
    expected_formulas = {
        "D2_formula": "D2_j(h)=[F(p_star+h*e_j)-F(p_star-h*e_j)]/(2*h).",
        "R4_formula": "R4_j(h)=[4*D2_j(h/2)-D2_j(h)]/3.",
        "five_point_equivalence": "R4_j(h)=[F(-h)-8F(-h/2)+8F(h/2)-F(h)]/(6*h) around p_star.",
        "fixed_primary_reference": "R4_j(0.0002), using D2_j(0.0002) and D2_j(0.0001).",
    }
    if any(protocol[key] != value for key, value in expected_formulas.items()):
        raise InvalidRun("D2/R4/reference formula drift")
    expected_metrics = {
        "vector_symmetric_relative": "rel(x,y)=||x-y||_2/max(||x||_2,||y||_2,1e-30).",
        "operator_symmetric_relative": "rel_op(A,B)=||A-B||_2/max(||A||_2,||B||_2,1e-30).",
        "signed_cosine": "cos(x,y)=x^T*y/(||x||_2*||y||_2), with zero norms rejected before evaluation.",
        "angle_sine": "sqrt(max(0,1-cos(x,y)^2)); signed_cosine must additionally be strictly positive.",
    }
    if any(metrics[key] != value for key, value in expected_metrics.items()):
        raise InvalidRun("relative metric definition drift")
    if (
        homotopy["variational_endpoint"]
        != "J_V is exactly J_checkpoint, not an observed best of the three variational integrations."
        or homotopy["reference_endpoint"]
        != "J_R is assembled from all fourteen fixed tight R4_j(0.0002) columns."
        or homotopy["numerical_robustness"]["explicit_inverse_forbidden"] is not True
        or len(homotopy["mutation_controls"]) != 3
        or manifest["acceptance_thresholds"][
            "normalized_orientation_homotopy_eta_strict_max"
        ] != 1.0
    ):
        raise InvalidRun("fixed homotopy/reference/mutation protocol drift")
    return {
        **exact_richardson_identity(),
        "primary_h": 2.0e-4,
        "neighbor_h": {"coarse": 4.0e-4, "fine": 1.0e-4},
        "relative_metrics": expected_metrics,
        "positive_column_normalization": True,
        "eta_computed_by_solve_not_inverse": True,
        "eta_sufficient_only": True,
        "mutation_slot_schema": [
            "positive_column_rescaling",
            "single_reference_column_flip",
            "no_sampled_t_used",
        ],
    }


def expected_fail_closed_outputs() -> dict[str, Any]:
    false_keys = (
        "m2_and_m4_actions_identified",
        "m2_and_m4_upward_cycles_identified",
        "m2_and_m4_common_determinant_line_constructed",
        "m3_and_m4_canonical_sign_equality_proved",
        "m3_and_m4_common_determinant_line_constructed",
        "straight_arm_intersections_searched",
        "cap_reintersections_searched",
        "continuous_direction_coverage_proved",
        "root_exhaustion_proved",
        "exact_nonlinear_upward_manifold_certified",
        "all_saddles_and_upward_components_complete",
        "non_Stokes_chamber_certified",
        "all_relative_good_ends_classified",
        "physical_original_cycle_derived",
        "metric_homotopy_tested",
        "BFV_Pfaffian_Pin_orientation_computed",
    )
    null_keys = (
        "bounded_chain_signed_sum",
        "complete_global_signed_intersection_vector",
        "global_n_sigma",
        "cutoff_limit",
        "continuum_limit",
        "quantum_gravity_explanation",
    )
    return {
        **{key: False for key in false_keys},
        **{key: None for key in null_keys},
        "gate1_status": "OPEN_PARTIAL_PROGRESS",
    }


def retention_protocol_guard(
    manifest: Mapping[str, Any], ledger: SlotLedger
) -> dict[str, Any]:
    retention = manifest["declared_output_retention"]
    artifact = retention["result_artifact"]
    expected_artifact = {
        "path": "cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json",
        "schema": RESULT_SCHEMA,
        "stdout_prefix": RESULT_PREFIX,
        "stored_prefix": None,
    }
    if any(artifact[key] != value for key, value in expected_artifact.items()):
        raise InvalidRun("result artifact path/schema/prefix drift")
    if (
        len(retention["atomic_capture_sequence"]) != 5
        or "exactly one LF" not in artifact["stored_format"]
        or artifact["payload_digest_field_name"]
        != "result_payload_sha256_without_self"
        or "including the single final LF" not in artifact["outer_hash_convention"]
    ):
        raise InvalidRun("result retention/hash/atomic-capture protocol drift")
    kind_counts: dict[str, int] = {}
    for slot in ledger.slots.values():
        kind = str(slot["metadata"]["slot_kind"])
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
    expected_kind_counts = {
        "center": 15,
        "augmented_center": 6,
        "endpoint": 894,
        "D2": 447,
        "fixed_R4": 126,
        "local_RHS_direction": 90,
        "local_RHS_perturbation": 540,
        "time_control": 12,
        "matrix_diagnostic": 21,
        "homotopy_mutation_control": 9,
        "cause": 24,
        "cause_aggregate": 8,
    }
    if kind_counts != expected_kind_counts or set(ledger.slots) != expected_slot_keys():
        raise InvalidRun("slot kind/key schema drift")
    return {
        "result_artifact": expected_artifact,
        "atomic_capture_stage_count": 5,
        "slot_kind_counts": kind_counts,
        "slot_key_set_exact": True,
        "result_payload_digest_excludes_only_self_field": True,
        "outer_hash_includes_single_final_LF": True,
    }


def record_exact_contracts(
    audit: Audit,
    manifest: Mapping[str, Any],
    context: CheckpointContext,
    slot_summary: Mapping[str, Any],
    ledger: SlotLedger,
    provenance: Mapping[str, Any],
    immutable_before: Mapping[str, str],
    solver_validation: Mapping[str, Any],
    tiers: Mapping[str, TierSpec],
) -> None:
    exact_map, _numerical_map = manifest_contract_maps(manifest)
    audit.exact(
        EXACT_IDS[0],
        bool(
            provenance["comparisons"]
            and all(provenance["comparisons"].values())
            and provenance["start"]["runner"]["git_tracked"]
            and provenance["start"]["runner"][
                "manifest_commit_is_ancestor_of_runner_commit"
            ]
        ),
        str(exact_map[EXACT_IDS[0]]["criterion"]),
        provenance,
    )
    validation = context.validation
    audit.exact(
        EXACT_IDS[1],
        bool(
            validation["checkpoint_envelope"][
                "decoded_explicit_array_payload_count"
            ]
            == 191
            and validation["checkpoint_envelope"]["mapped_critical_array_count"]
            == 204
            and validation["cross_field_identities"][
                "row_scale_identity_passed"
            ]
        ),
        str(exact_map[EXACT_IDS[1]]["criterion"]),
        validation,
    )
    immutable_after: dict[str, str] = {}
    for label, point in context.points.items():
        immutable_after[f"{label}.p"] = sha256_bytes(
            canonical_array_bytes(point.parameters)[1]
        )
        immutable_after[f"{label}.J"] = sha256_bytes(
            canonical_array_bytes(point.checkpoint_jacobian)[1]
        )
    audit.exact(
        EXACT_IDS[2],
        bool(
            immutable_after == dict(immutable_before)
            and all(value == 0 for value in context.no_solve_call_counter.values())
        ),
        str(exact_map[EXACT_IDS[2]]["criterion"]),
        {
            "immutable_before": immutable_before,
            "immutable_after": immutable_after,
            "forbidden_call_counts": context.no_solve_call_counter,
        },
    )
    map_guard = frozen_map_and_tier_guard(manifest, context, ledger, tiers)
    audit.exact(
        EXACT_IDS[3],
        bool(
            slot_summary["endpoint_count"] == 894
            and slot_summary["D2_count"] == 447
            and solver_validation["all_tier_and_retention_checks_passed"]
        ),
        str(exact_map[EXACT_IDS[3]]["criterion"]),
        {
            "map_and_tier_guard": map_guard,
            "slot_summary": slot_summary,
            "solver_validation": solver_validation,
        },
    )
    math_identity = frozen_math_guard(manifest)
    audit.exact(
        EXACT_IDS[4],
        True,
        str(exact_map[EXACT_IDS[4]]["criterion"]),
        math_identity,
    )
    audit.exact(
        EXACT_IDS[5],
        bool(
            manifest["local_variational_rhs_protocol"]["complex_step_scope"][
                "full_residual_allowed"
            ]
            is False
            and manifest["chart_curvature_protocol"]["u2_geodesic_control"][
                "cause_decision_h"
            ]
            == 0.0002
            and manifest["chart_curvature_protocol"]["production_chart"]
            == "r(u)=c+B*u and omega_affine(u)=r(u)/||r(u)||."
            and manifest["chart_curvature_protocol"]["u2_geodesic_control"][
                "same_base_and_tangent"
            ]
            == "omega_geo(0)=omega and derivative_t omega_geo(0)=v."
        ),
        str(exact_map[EXACT_IDS[5]]["criterion"]),
        {
            "full_map_complex_step_used": False,
            "affine_chart_remains_production_map": True,
            "geodesic_scope": "same-base/same-first-tangent diagnostic",
        },
    )
    ledger.assert_complete()
    retention_guard = retention_protocol_guard(manifest, ledger)
    audit.exact(
        EXACT_IDS[6],
        bool(
            len(ledger.slots) == 2192
            and all(
                slot["terminal_status"]
                in {"SUCCESS", "EVALUATION_FAILED", "NOT_RUN_UPSTREAM_INVALID"}
                for slot in ledger.slots.values()
            )
        ),
        str(exact_map[EXACT_IDS[6]]["criterion"]),
        {
            "declared_slot_count": len(ledger.slots),
            "terminal_status_counts": {
                status: sum(
                    slot["terminal_status"] == status for slot in ledger.slots.values()
                )
                for status in (
                    "SUCCESS",
                    "EVALUATION_FAILED",
                    "NOT_RUN_UPSTREAM_INVALID",
                )
            },
            "result_schema": RESULT_SCHEMA,
            "retention_protocol_guard": retention_guard,
        },
    )
    completion = validation["completion_ledger"]
    expected_fail_closed = expected_fail_closed_outputs()
    desired = manifest["desired_outputs"]
    audit.exact(
        EXACT_IDS[7],
        bool(
            completion["false_count"] == 16
            and completion["null_count"] == 6
            and completion["gate1_status"] == "OPEN_PARTIAL_PROGRESS"
            and manifest["required_fail_closed_outputs"] == expected_fail_closed
            and len(desired) == 7
            and all(value is None for value in desired.values())
        ),
        str(exact_map[EXACT_IDS[7]]["criterion"]),
        {
            "checkpoint_completion_ledger": completion,
            "manifest_fail_closed_outputs": expected_fail_closed,
            "desired_output_count": len(desired),
            "all_desired_outputs_null": all(value is None for value in desired.values()),
        },
    )


def record_numerical_contracts(
    audit: Audit,
    manifest: Mapping[str, Any],
    three_way: Mapping[str, Any],
    negative: Mapping[str, Any],
    chart: Mapping[str, Any],
    local: Mapping[str, Any],
    r4: Mapping[str, Any],
    u2: Mapping[str, Any],
    homotopy: Mapping[str, Any],
    causes: Mapping[str, Any],
) -> None:
    _exact_map, numerical_map = manifest_contract_maps(manifest)
    production_pass = bool(
        all(
            three_way.get(label, {}).get("production_drift_passed") is True
            for label in TARGETS
        )
    )
    values = (
        (NUMERICAL_IDS[0], production_pass, three_way),
        (NUMERICAL_IDS[1], bool(negative["passed"]), negative),
        (NUMERICAL_IDS[2], bool(chart["passed"]), chart),
        (NUMERICAL_IDS[3], bool(local["passed"]), local),
        (NUMERICAL_IDS[4], bool(r4["passed"]), r4),
        (NUMERICAL_IDS[5], bool(u2["passed"]), u2),
        (NUMERICAL_IDS[6], bool(homotopy["passed"]), homotopy),
        (NUMERICAL_IDS[7], bool(causes["passed"]), causes),
    )
    for check_id, passed, details in values:
        record = numerical_map[check_id]
        audit.numerical(
            check_id,
            passed,
            str(record["criterion"]),
            failure_status=str(record["failure_status"]),
            failure_invalidates_run=bool(
                record.get("failure_invalidates_run", False)
            ),
            details=details,
        )


def manifest_contract_maps(
    manifest: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    exact = {
        str(record["id"]): record
        for record in manifest["contracts"]["exact"]
    }
    numerical = {
        str(record["id"]): record
        for record in manifest["contracts"]["numerical"]
    }
    if tuple(exact) != EXACT_IDS or tuple(numerical) != NUMERICAL_IDS:
        raise InvalidRun("manifest contract ids/order drifted from runner")
    return exact, numerical


def result_with_self_digest(payload: dict[str, Any]) -> dict[str, Any]:
    ready = json_ready(payload)
    if not isinstance(ready, dict):
        raise InvalidRun("result payload did not serialize as an object")
    ready.pop("result_payload_sha256_without_self", None)
    digest = sha256_bytes(canonical_json_bytes(ready))
    ready["result_payload_sha256_without_self"] = digest
    canonical_json_bytes(ready)
    return ready


def invalid_result_skeleton(
    manifest: Mapping[str, Any] | None,
    reason: str,
    *,
    audit: Audit | None = None,
    ledger: SlotLedger | None = None,
    observed_failure_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    exact_map: dict[str, Any] = {}
    numerical_map: dict[str, Any] = {}
    if manifest is not None:
        try:
            exact_map, numerical_map = manifest_contract_maps(manifest)
        except Exception:
            exact_map = {}
            numerical_map = {}
    existing_exact = {
        record["id"]: record for record in (audit.exact_records if audit else [])
    }
    existing_numerical = {
        record["id"]: record
        for record in (audit.numerical_records if audit else [])
    }
    exact_records: list[dict[str, Any]] = []
    for check_id in EXACT_IDS:
        exact_records.append(
            existing_exact.get(
                check_id,
                {
                    "id": check_id,
                    "kind": "exact",
                    "status": "INVALID_RUN",
                    "passed": False,
                    "failure_status": "INVALID_RUN",
                    "statement": str(
                        exact_map.get(check_id, {}).get("criterion", reason)
                    ),
                    "details": {"not_completed_reason": reason},
                },
            )
        )
    numerical_records: list[dict[str, Any]] = []
    for check_id in NUMERICAL_IDS:
        declared = numerical_map.get(check_id, {})
        numerical_records.append(
            existing_numerical.get(
                check_id,
                {
                    "id": check_id,
                    "kind": "numerical",
                    "status": "NOT_RUN_UPSTREAM_INVALID",
                    "passed": False,
                    "failure_status": str(
                        declared.get("failure_status", "INVALID_RUN")
                    ),
                    "failure_invalidates_run": bool(
                        declared.get("failure_invalidates_run", True)
                    ),
                    "statement": str(declared.get("criterion", reason)),
                    "details": {"not_completed_reason": reason},
                },
            )
        )
    if ledger is not None:
        ledger.fail_unfinished(reason)
    # Never source global-null outputs from a possibly hash-drifted manifest.
    fail_closed = expected_fail_closed_outputs()
    payload = {
        "schema": RESULT_SCHEMA,
        "phase": 42,
        "run_status": "INVALID_RUN",
        "exit_code": 2,
        "invalid_reason": reason,
        "historical_phase41_status": "TANGENT_CONTROL_FAILED",
        "counts": {
            "exact_passed": sum(bool(r["passed"]) for r in exact_records),
            "exact_total": 8,
            "numerical_passed": sum(
                bool(r["passed"]) for r in numerical_records
            ),
            "numerical_total": 8,
        },
        "exact_records": exact_records,
        "numerical_records": numerical_records,
        "slot_ledger": ledger.slots if ledger is not None else {},
        "slot_schema_summary": None,
        "solver_attempt_validation": None,
        "endpoint_sweep": None,
        "fixed_reference_summary": None,
        "three_way_J": None,
        "phase41_negative_control": None,
        "chart_diagnostics": None,
        "local_variational_diagnostics": None,
        "finite_difference_diagnostics": None,
        "u2_disentanglement": None,
        "orientation_homotopy": None,
        "cause_ledger": None,
        "claim_status": {
            "phase42_reference_tangent": None,
            "cause_classification": None,
            "phase41_retroactive_9_of_9": False,
            "global_promotion": "PROHIBITED",
        },
        "required_fail_closed_outputs": fail_closed,
        "desired_outputs": {key: None for key in (
            "desired_cause_classification",
            "desired_phase42_tangent_result",
            "desired_variational_bug_verdict",
            "desired_local_orientation_sign",
            "desired_root_jacobian_sign",
            "desired_homotopy_certificate",
            "desired_global_intersection_coefficient",
        )},
        "result_artifact_contract": (
            dict(manifest["declared_output_retention"]["result_artifact"])
            if manifest is not None
            and isinstance(manifest.get("declared_output_retention"), dict)
            else None
        ),
        "scientific_scope": {
            "fixed_root_local_only": True,
            "global_promotion": "PROHIBITED",
            "quantum_gravity_claim": False,
        },
        "provenance": {
            "manifest_commit": MANIFEST_COMMIT,
            "manifest_sha256": MANIFEST_SHA256,
            "checkpoint_commit": CHECKPOINT_COMMIT,
            "checkpoint_sha256": CHECKPOINT_SHA256,
            "runner_sha256": sha256_bytes(SCRIPT_PATH.read_bytes()),
            "failure_observations": dict(observed_failure_provenance or {}),
        },
    }
    return result_with_self_digest(payload)


def emit_result(
    payload: Mapping[str, Any],
    *,
    final_guard: Callable[[], Any] | None = None,
) -> None:
    ready = result_with_self_digest(dict(payload))
    encoded = canonical_json_bytes(ready).decode("utf-8")
    if final_guard is not None:
        # This check occurs after the potentially expensive full serialization
        # and immediately before the single stdout write.
        final_guard()
    print(f"{RESULT_PREFIX}{encoded}", flush=True)


def immutable_input_hashes(context: CheckpointContext) -> dict[str, str]:
    """Hash the immutable roots and authoritative checkpoint Jacobians."""
    result: dict[str, str] = {}
    for label in TARGETS:
        point = context.points[label]
        result[f"{label}.p"] = sha256_bytes(
            canonical_array_bytes(point.parameters)[1]
        )
        result[f"{label}.J"] = sha256_bytes(
            canonical_array_bytes(point.checkpoint_jacobian)[1]
        )
    return result


def choose_claim_status(
    audit: Audit, causes: Mapping[str, Any]
) -> dict[str, Any]:
    numerical_pass = {record["id"]: bool(record["passed"]) for record in audit.numerical_records}
    required_local = all(
        numerical_pass.get(check_id, False)
        for check_id in NUMERICAL_IDS
    )
    aggregate = causes.get("aggregate_any_fixed_point", {})
    supported_causes = sorted(
        (
            "U2_CAUSE_UNRESOLVED" if str(name) == "UNRESOLVED" else str(name)
        )
        for name, record in aggregate.items()
        if isinstance(record, dict) and record.get("evidence_status") == "SUPPORTED"
    )
    reference_status = (
        "PHASE42_REFERENCE_TANGENT_CORROBORATED"
        if required_local
        else "REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE"
    )
    return {
        "phase42_reference_tangent": reference_status,
        "cause_classification": (
            supported_causes
        ),
        "cause_classification_summary": (
            "SUPPORTED_CAUSES_RETAINED"
            if supported_causes
            else "NO_DECLARED_CAUSE_SUPPORTED"
        ),
        "phase41_retroactive_9_of_9": False,
        "phase41_historical_status": "TANGENT_CONTROL_FAILED",
        "global_promotion": "PROHIBITED",
        "scope": "three immutable local m=4 roots only",
    }


def production_result_payload(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    *,
    run_status: str,
    exit_code: int,
    slot_summary: Mapping[str, Any],
    endpoint_summary: Mapping[str, Any],
    fixed_reference_summary: Mapping[str, Any],
    three_way: Mapping[str, Any],
    negative: Mapping[str, Any],
    chart: Mapping[str, Any],
    local: Mapping[str, Any],
    r4: Mapping[str, Any],
    u2: Mapping[str, Any],
    homotopy: Mapping[str, Any],
    causes: Mapping[str, Any],
    provenance: Mapping[str, Any],
    solver_validation: Mapping[str, Any],
) -> dict[str, Any]:
    exact_passed = sum(bool(record["passed"]) for record in audit.exact_records)
    numerical_passed = sum(
        bool(record["passed"]) for record in audit.numerical_records
    )
    return {
        "schema": RESULT_SCHEMA,
        "phase": 42,
        "run_status": run_status,
        "exit_code": exit_code,
        "historical_phase41_status": "TANGENT_CONTROL_FAILED",
        "counts": {
            "exact_passed": exact_passed,
            "exact_total": len(audit.exact_records),
            "numerical_passed": numerical_passed,
            "numerical_total": len(audit.numerical_records),
        },
        "exact_records": audit.exact_records,
        "numerical_records": audit.numerical_records,
        "slot_schema_summary": slot_summary,
        "slot_ledger": ledger.slots,
        "solver_attempt_validation": solver_validation,
        "endpoint_sweep": endpoint_summary,
        "fixed_reference_summary": fixed_reference_summary,
        "three_way_J": three_way,
        "phase41_negative_control": negative,
        "chart_diagnostics": chart,
        "local_variational_diagnostics": local,
        "finite_difference_diagnostics": r4,
        "u2_disentanglement": u2,
        "orientation_homotopy": homotopy,
        "cause_ledger": causes,
        "claim_status": choose_claim_status(audit, causes),
        "desired_outputs": dict(manifest["desired_outputs"]),
        "required_fail_closed_outputs": dict(
            manifest["required_fail_closed_outputs"]
        ),
        "result_artifact_contract": dict(
            manifest["declared_output_retention"]["result_artifact"]
        ),
        "provenance": provenance,
        "scientific_scope": {
            "fixed_root_local_only": True,
            "post_hoc_checkpoint_historical_stdout_identity_verified": False,
            "eta_is_sufficient_only": True,
            "determinant_line_or_global_cycle_claim": False,
            "quantum_gravity_claim": False,
        },
    }


def run_production(
    manifest: Mapping[str, Any],
    audit: Audit,
    ledger: SlotLedger,
    run_state: dict[str, Any],
) -> int:
    """Execute the frozen numerical workflow after Stage-2 runner commit."""
    manifest_contract_maps(manifest)
    slot_summary = preenumerate_slot_ledger(manifest, ledger)
    progress("provenance/start")
    run_state["raw_provenance_start"] = {
        "runner": observe_runner_provenance_raw(),
        "source": observe_source_closure_raw(manifest),
        "HEAD": raw_git_observation("rev-parse", "HEAD"),
    }
    provenance_start = start_provenance_guard(manifest)
    run_state["provenance_start"] = provenance_start
    checkpoint, checkpoint_raw = read_pinned_json(
        CHECKPOINT_PATH, CHECKPOINT_SHA256, label="Phase42 checkpoint"
    )
    context = rehydrate_checkpoint(manifest, checkpoint, checkpoint_raw)
    immutable_before = immutable_input_hashes(context)
    tiers = tier_specs(manifest)

    progress("endpoint/D2 sweep")
    evaluator, endpoint_internal = run_endpoint_sweep(
        manifest, context, tiers, ledger
    )
    d2_vectors = endpoint_internal.pop("D2_vectors")
    references, fixed_reference_summary = fixed_r4_references(
        context, ledger, d2_vectors
    )
    progress("three-way transported Jacobians")
    augmented, three_way = run_augmented_and_three_way(
        context, tiers, ledger
    )
    negative = phase41_negative_control(
        manifest, context, ledger, d2_vectors, augmented
    )
    chart = chart_diagnostics(context, ledger, d2_vectors)
    local = local_rhs_diagnostics(
        context,
        tiers,
        ledger,
        evaluator,
        augmented,
        references,
        d2_vectors,
    )
    r4, r4_matrices = all_column_r4_diagnostics(
        context, ledger, references, augmented
    )
    u2 = u2_solver_diagnostics(manifest, ledger, d2_vectors, references)
    homotopy = normalized_homotopy_diagnostics(
        context, ledger, r4_matrices
    )
    causes = classify_causes(
        context,
        ledger,
        d2_vectors,
        references,
        three_way,
        negative,
        chart,
        local,
        r4,
        u2,
        homotopy,
    )
    ledger.assert_complete()
    solver_validation = validate_solver_attempt_ledgers(ledger, tiers)
    progress("provenance/pre-audit")
    provenance = finish_provenance_guard(manifest, provenance_start)
    run_state["provenance_pre_audit"] = provenance
    record_exact_contracts(
        audit,
        manifest,
        context,
        slot_summary,
        ledger,
        provenance,
        immutable_before,
        solver_validation,
        tiers,
    )
    record_numerical_contracts(
        audit,
        manifest,
        three_way,
        negative,
        chart,
        local,
        r4,
        u2,
        homotopy,
        causes,
    )
    if len(audit.exact_records) != 8 or len(audit.numerical_records) != 8:
        raise InvalidRun("audit record count is not exactly 8 exact plus 8 numerical")
    invalidating = [
        record["id"]
        for record in audit.numerical_records
        if not record["passed"] and record["failure_invalidates_run"]
    ]
    if invalidating:
        raise InvalidRun(
            "invalidating numerical contracts failed: " + ",".join(invalidating)
        )
    payload = production_result_payload(
        manifest,
        audit,
        ledger,
        run_status="VALID_TYPED_RUN",
        exit_code=0,
        slot_summary=slot_summary,
        endpoint_summary=endpoint_internal,
        fixed_reference_summary=fixed_reference_summary,
        three_way=three_way,
        negative=negative,
        chart=chart,
        local=local,
        r4=r4,
        u2=u2,
        homotopy=homotopy,
        causes=causes,
        provenance=provenance,
        solver_validation=solver_validation,
    )
    # Recheck all source, runner, environment, HEAD, and pycache observations
    # immediately before the only scientific stdout record.
    payload["provenance"] = finish_provenance_guard(
        manifest, provenance_start
    )
    run_state["provenance_pre_emit"] = payload["provenance"]
    emit_result(
        payload,
        final_guard=lambda: finish_provenance_guard(
            manifest, provenance_start
        ),
    )
    return 0


def emergency_finite_invalid_result(reason: str) -> dict[str, Any]:
    """Last-resort primitive-only JSON object; this path must itself be safe."""
    clean_reason = str(reason).replace("\x00", "?")[:4096]
    exact_records = [
        {
            "id": check_id,
            "kind": "exact",
            "status": "INVALID_RUN",
            "passed": False,
            "failure_status": "INVALID_RUN",
            "statement": clean_reason,
            "details": {"emergency_fallback": True},
        }
        for check_id in EXACT_IDS
    ]
    numerical_failure_contracts = (
        ("PHASE41_MAP_OR_PLATFORM_DRIFT", True),
        ("PHASE41_MAP_OR_PLATFORM_DRIFT", True),
        ("CHART_TANGENT_INVALID_OR_INCONCLUSIVE", False),
        ("LOCAL_VARIATIONAL_IDENTITY_NOT_SUPPORTED", False),
        ("REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE", False),
        ("U2_CAUSE_UNRESOLVED", False),
        ("LOCAL_ORIENTATION_DERIVATIVE_TRUST_NOT_SUPPORTED", False),
        ("CAUSE_LEDGER_INCOMPLETE", True),
    )
    numerical_records = [
        {
            "id": check_id,
            "kind": "numerical",
            "status": "NOT_RUN_UPSTREAM_INVALID",
            "passed": False,
            "failure_status": numerical_failure_contracts[index][0],
            "failure_invalidates_run": numerical_failure_contracts[index][1],
            "statement": clean_reason,
            "details": {"emergency_fallback": True},
        }
        for index, check_id in enumerate(NUMERICAL_IDS)
    ]
    try:
        observed_runner_sha: str | None = sha256_bytes(SCRIPT_PATH.read_bytes())
        runner_sha_error: str | None = None
    except Exception as exc:
        observed_runner_sha = None
        runner_sha_error = f"{type(exc).__name__}: {exc}"[:1024]
    base: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "phase": 42,
        "run_status": "INVALID_RUN",
        "exit_code": 2,
        "invalid_reason": clean_reason,
        "historical_phase41_status": "TANGENT_CONTROL_FAILED",
        "counts": {
            "exact_passed": 0,
            "exact_total": 8,
            "numerical_passed": 0,
            "numerical_total": 8,
        },
        "exact_records": exact_records,
        "numerical_records": numerical_records,
        "slot_ledger": {},
        "three_way_J": None,
        "phase41_negative_control": None,
        "chart_diagnostics": None,
        "local_variational_diagnostics": None,
        "finite_difference_diagnostics": None,
        "u2_disentanglement": None,
        "orientation_homotopy": None,
        "cause_ledger": None,
        "claim_status": {
            "phase42_reference_tangent": None,
            "cause_classification": None,
            "phase41_retroactive_9_of_9": False,
            "global_promotion": "PROHIBITED",
        },
        "required_fail_closed_outputs": expected_fail_closed_outputs(),
        "desired_outputs": {
            "desired_cause_classification": None,
            "desired_phase42_tangent_result": None,
            "desired_variational_bug_verdict": None,
            "desired_local_orientation_sign": None,
            "desired_root_jacobian_sign": None,
            "desired_homotopy_certificate": None,
            "desired_global_intersection_coefficient": None,
        },
        "provenance": {
            "manifest_commit": MANIFEST_COMMIT,
            "manifest_sha256": MANIFEST_SHA256,
            "checkpoint_commit": CHECKPOINT_COMMIT,
            "checkpoint_sha256": CHECKPOINT_SHA256,
            "runner_observed_sha256": observed_runner_sha,
            "runner_sha_observation_error": runner_sha_error,
            "emergency_minimal_provenance": True,
        },
        "emergency_fallback": True,
    }
    return result_with_self_digest(base)


def capture_failure_provenance(
    manifest: Mapping[str, Any] | None, run_state: Mapping[str, Any]
) -> dict[str, Any]:
    observations: dict[str, Any] = {
        "retained_start": run_state.get("provenance_start"),
        "retained_pre_audit": run_state.get("provenance_pre_audit"),
        "retained_pre_emit": run_state.get("provenance_pre_emit"),
        "raw_start": run_state.get("raw_provenance_start"),
    }

    def capture(name: str, operation: Callable[[], Any]) -> None:
        try:
            observations[name] = {"status": "OBSERVED", "value": operation()}
        except Exception as exc:
            observations[name] = {
                "status": "OBSERVATION_FAILED",
                "error": f"{type(exc).__name__}: {exc}",
            }

    head_raw = raw_git_observation("rev-parse", "HEAD")
    runner_raw = observe_runner_provenance_raw()
    source_raw = observe_source_closure_raw(manifest)
    observations["HEAD_at_failure"] = {
        "status": "OBSERVED_RAW",
        "value": head_raw["stdout"] if head_raw["ok"] else None,
        "observation_error": None if head_raw["ok"] else head_raw["stderr"],
    }
    observations["runner_at_failure"] = {
        "status": "OBSERVED_RAW",
        "value": runner_raw,
    }
    capture("pycache_at_failure", repository_pycache_snapshot)
    if manifest is not None:
        observations["source_at_failure"] = {
            "status": "OBSERVED_RAW",
            "value": source_raw,
        }
        capture(
            "runtime_at_failure",
            lambda: observed_runtime_fingerprint(manifest),
        )
    else:
        observations["source_at_failure"] = {
            "status": "OBSERVED_RAW",
            "value": source_raw,
        }
    raw_start = run_state.get("raw_provenance_start")
    if isinstance(raw_start, Mapping):
        observations["raw_start_to_failure_comparisons"] = {
            "runner": raw_start.get("runner") == runner_raw,
            "source": raw_start.get("source") == source_raw,
            "HEAD": (
                isinstance(raw_start.get("HEAD"), Mapping)
                and raw_start["HEAD"].get("ok") is True
                and head_raw["ok"] is True
                and raw_start["HEAD"].get("stdout") == head_raw["stdout"]
            ),
        }
    start = run_state.get("provenance_start")
    if isinstance(start, Mapping):
        comparisons: dict[str, bool | None] = {}
        for key, observed_key in (
            ("source", "source_at_failure"),
            ("runner", "runner_at_failure"),
            ("runtime", "runtime_at_failure"),
            ("pycache", "pycache_at_failure"),
            ("HEAD", "HEAD_at_failure"),
        ):
            record = observations.get(observed_key)
            if key == "runner":
                comparisons[key] = bool(
                    runner_raw.get("observed_sha256")
                    == start.get("runner", {}).get("observed_sha256")
                    and runner_raw.get("git_tracked")
                    == start.get("runner", {}).get("git_tracked")
                    and runner_raw.get("git_clean_for_path")
                    == start.get("runner", {}).get("git_clean_for_path")
                    and runner_raw.get("latest_path_commit")
                    == start.get("runner", {}).get("latest_path_commit")
                    and runner_raw.get("latest_commit_blob_sha256")
                    == start.get("runner", {}).get("latest_commit_blob_sha256")
                    and runner_raw.get("latest_path_commit_is_ancestor_of_HEAD")
                    == start.get("runner", {}).get(
                        "latest_path_commit_is_ancestor_of_HEAD"
                    )
                    and runner_raw.get(
                        "manifest_commit_is_ancestor_of_runner_commit"
                    )
                    == start.get("runner", {}).get(
                        "manifest_commit_is_ancestor_of_runner_commit"
                    )
                )
            elif key == "source":
                start_source = start.get("source", {})
                start_files = start_source.get("files", {})
                raw_files = source_raw.get("files", {})
                comparisons[key] = bool(
                    source_raw.get("git_HEAD") == start_source.get("git_HEAD")
                    and set(raw_files) == set(start_files)
                    and all(
                        raw_files[name].get("observed_sha256")
                        == start_files[name].get("sha256")
                        and raw_files[name].get("expected_commit")
                        == start_files[name].get("commit")
                        and raw_files[name].get(
                            "expected_commit_blob_matches_current_bytes"
                        )
                        is True
                        and raw_files[name].get(
                            "expected_commit_is_ancestor_of_HEAD"
                        )
                        is True
                        for name in raw_files
                    )
                )
            elif key == "HEAD":
                comparisons[key] = bool(
                    head_raw.get("ok") is True
                    and head_raw.get("stdout") == start.get("HEAD")
                )
            else:
                comparisons[key] = (
                    bool(record.get("value") == start.get(key))
                    if isinstance(record, Mapping)
                    and record.get("status") == "OBSERVED"
                    else None
                )
        observations["start_to_failure_comparisons"] = comparisons
    return observations


def main() -> int:
    manifest: dict[str, Any] | None = None
    audit = Audit()
    ledger = SlotLedger()
    run_state: dict[str, Any] = {}
    try:
        # Parse first so a syntactically valid but hash-drifted manifest can
        # still drive the complete typed INVALID_RUN envelope.  No scientific
        # field is trusted until the byte hash is checked immediately after.
        manifest_raw = MANIFEST_PATH.read_bytes()
        manifest = strict_json_bytes(manifest_raw, label="Phase42 manifest")
        observed_manifest_sha = sha256_bytes(manifest_raw)
        if observed_manifest_sha != MANIFEST_SHA256:
            raise InvalidRun(
                "Phase42 manifest SHA drift: expected "
                f"{MANIFEST_SHA256}, observed {observed_manifest_sha}"
            )
        return run_production(manifest, audit, ledger, run_state)
    except Exception as exc:
        reason = f"{type(exc).__name__}: {exc}"
        progress(reason)
        try:
            failure_provenance = capture_failure_provenance(manifest, run_state)
            emit_result(
                invalid_result_skeleton(
                    manifest,
                    reason,
                    audit=audit,
                    ledger=ledger,
                    observed_failure_provenance=failure_provenance,
                )
            )
        except Exception as fallback_exc:
            emergency_reason = (
                f"{reason}; fallback={type(fallback_exc).__name__}: "
                f"{fallback_exc}"
            )
            emergency = emergency_finite_invalid_result(emergency_reason)
            encoded = json.dumps(
                emergency,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            print(f"{RESULT_PREFIX}{encoded}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
